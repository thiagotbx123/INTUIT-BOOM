"""QBO Demo Manager — FastAPI Web Dashboard."""

import sys
from pathlib import Path

# Ensure dashboard package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from actions import generate_sweep_prompt, sync_retool, test_login
from config import (
    get_account_config,
    load_profiles,
    save_account_config,
    save_profile,
)
from data import get_account, load_accounts
from sweep_checks import (
    CONDITIONAL_CHECKS,
    CONTENT_SAFETY,
    DEEP_STATIONS,
    DEMO_REALISM_CRITERIA,
    FIX_TIERS,
    SURFACE_SCAN,
)

app = FastAPI(title="QBO Demo Manager")

BASE = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE / "templates"))


# ─── Dashboard ───


def _get_active_sweep() -> dict | None:
    """Read LATEST_SWEEP.json and return data if status is pending.

    Also detects crashed sweeps (status=pending but process dead) and marks
    them as 'interrupted' so the dashboard can show a Resume button.
    """
    import json as json_mod

    sweep_file = BASE / "pending" / "LATEST_SWEEP.json"
    if not sweep_file.exists():
        return None
    try:
        data = json_mod.loads(sweep_file.read_text(encoding="utf-8"))
        if data.get("status") == "pending":
            # Check if process is actually alive
            pid = data.get("pid")
            if pid:
                import subprocess as _sp

                check = _sp.run(
                    ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if str(pid) not in check.stdout:
                    # Process dead — mark as interrupted
                    data["status"] = "interrupted"
                    sweep_file.write_text(
                        json_mod.dumps(data, indent=2, ensure_ascii=False),
                        encoding="utf-8",
                    )
            return data
        if data.get("status") == "interrupted":
            return data
    except Exception:
        pass
    return None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    accounts = load_accounts()
    total_entities = sum(len(a.companies) for a in accounts)
    active_sweep = _get_active_sweep()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "accounts": accounts,
            "total_entities": total_entities,
            "active_sweep": active_sweep,
        },
    )


@app.get("/account/{shortcode}", response_class=HTMLResponse)
async def account_detail(request: Request, shortcode: str):
    account = get_account(shortcode)
    if not account:
        return HTMLResponse(f"<h2>Account '{shortcode}' not found</h2>", status_code=404)
    return templates.TemplateResponse(
        "account.html",
        {
            "request": request,
            "account": account,
        },
    )


# ─── Config Panel ───


@app.get("/config", response_class=HTMLResponse)
async def config_panel(request: Request, profile: str = "full_sweep", account: str = ""):
    accounts = load_accounts()
    profiles = load_profiles()

    active_profile = profile if profile in profiles else "full_sweep"
    p = profiles[active_profile]

    # Merge account config overrides
    acct_cfg = get_account_config(account) if account else {}
    if acct_cfg.get("profile") and acct_cfg["profile"] in profiles and not profile:
        active_profile = acct_cfg["profile"]
        p = profiles[active_profile]

    return templates.TemplateResponse(
        "config.html",
        {
            "request": request,
            "accounts": accounts,
            "profiles": profiles,
            "active_profile": active_profile,
            "target_shortcode": account,
            "profile": p,
            "profile_checks": p.get("checks", {}),
            "profile_fix": p.get("fix_tiers", {}),
            "profile_safety": p.get("content_safety", {}),
            "deep_stations": DEEP_STATIONS,
            "surface_scan": SURFACE_SCAN,
            "conditional_checks": CONDITIONAL_CHECKS,
            "content_safety": CONTENT_SAFETY,
            "fix_tiers": FIX_TIERS,
            "realism_criteria": DEMO_REALISM_CRITERIA,
            "account_notes": acct_cfg.get("notes", ""),
        },
    )


# ─── Config API ───


@app.post("/api/config/save-profile")
async def api_save_profile(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=422)
    save_profile(body["key"], body["profile"])
    return JSONResponse({"status": "ok"})


@app.post("/api/config/save-account")
async def api_save_account(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=422)
    save_account_config(body["shortcode"], body["config"])
    return JSONResponse({"status": "ok"})


def _generate_sweep_order_md(pending_dir, acct, profile_data, profile_key, deep, surface, cond, resume_from=None):
    """Generate a comprehensive SWEEP_ORDER.md the new Claude session can follow.

    Args:
        resume_from: dict with 'completed_stations', 'current_entity' if resuming.

    This is the ONLY document the sweep session needs. It embeds all methodology,
    fix protocols, and Playwright actions inline — no external references needed.
    """
    from sweep_checks import DEEP_STATIONS, SURFACE_SCAN, CONDITIONAL_CHECKS, CONTENT_SAFETY
    import datetime

    checks = profile_data.get("checks", {})
    fix = profile_data.get("fix_tiers", {})
    safety = profile_data.get("content_safety", {})
    can_fix = fix.get("fix_immediately", True) or fix.get("fix_and_report", True)

    # Build companies table
    companies_lines = []
    for c in acct.companies:
        companies_lines.append(f"| {c.name} | {c.cid} | {c.type} | {c.priority} |")

    is_multi = len(acct.companies) > 1

    # Build enabled deep checks with FULL fix protocols
    deep_lines = []
    for s in DEEP_STATIONS:
        if not checks.get(s["id"], True):
            continue
        check_items = "\n".join(f"  - {item}" for item in s["what_to_check"])
        fix_items = (
            "\n".join(f"  - {a}" for a in s["fix_actions"]) if s["fix_actions"] else "  - Report only (no auto-fix)"
        )
        deep_lines.append(
            f"### {s['id']} — {s['name']}\n"
            f"**Route**: `{s['route']}`\n"
            f"**VER** (browser_snapshot → ler tudo):\n{check_items}\n"
            f"**CORRIGIR** ({'OBRIGATORIO' if s['auto_fix'] and can_fix else 'Reportar apenas'}):\n{fix_items}\n"
            f"**AVANCAR**: Só passe ao proximo quando corrigiu ou documentou por que nao pôde.\n"
        )

    # Build enabled surface checks
    surface_lines = []
    for s in SURFACE_SCAN:
        if checks.get(s["id"], True):
            surface_lines.append(f"- **{s['id']}** {s['name']} → `{s['route']}` — {s['description']}")

    # Build enabled conditional checks
    cond_lines = []
    for s in CONDITIONAL_CHECKS:
        if checks.get(s["id"], True):
            cond_lines.append(f"- **{s['id']}** {s['name']} (if {s['condition']}) → `{s['route']}`")

    # Build content safety
    safety_lines = []
    for s in CONTENT_SAFETY:
        if safety.get(s["id"], True):
            safety_lines.append(f"- **{s['id']}** {s['name']}: `{s['pattern']}` [{s['severity']}]")

    # Fix tiers description
    fix_desc = []
    if fix.get("fix_immediately", True):
        fix_desc.append("**FIX IMMEDIATELY** — corrigir sem perguntar")
    if fix.get("fix_and_report", True):
        fix_desc.append("**FIX & REPORT** — corrigir e documentar no report")
    if fix.get("never_fix", False):
        fix_desc.append("**NEVER FIX** — apenas reportar (settings, legal name, payroll)")

    notes = profile_data.get("notes", "") or ""

    # Entity switch instructions
    if is_multi:
        switch_block = """
**Troca de entity** (em ordem):
```
METODO 1 (preferido): URL direto
→ browser_navigate("https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={CID}")
→ browser_wait_for(time=5)
→ browser_evaluate com EXTRATOR 5 para confirmar switch

METODO 2 (fallback): Dropdown no header
→ browser_click no nome da empresa no header
→ browser_click na empresa desejada
→ browser_wait_for(time=5)

METODO 3 (consolidated):
→ browser_navigate("https://qbo.intuit.com/app/homepage?switchToConsolidated=true")
```
"""
    else:
        switch_block = "**Entity unica** — sem necessidade de troca."

    # Sector-specific realistic names
    sector_names = {
        "construction": "Customers: Austin Metro Schools, Barton Creek Developers | Vendors: Summit Supply Co, ProBuild Materials | Projects: Office Complex Phase II, Cedar Park Expansion",
        "tire_shop": "Customers: Lone Star Fleet, Gulf Coast Trucking | Vendors: Bridgestone Direct, Michelin Supply | Projects: Fleet Q1 Maintenance, Dealer Retrofit",
        "non_profit": "Donors: Johnson Family Foundation, United Way | Programs: Youth Development, Emergency Relief | Grants: HUD Housing FY26, State Workforce",
        "professional_services": "Clients: TechForward Inc, Meridian Health | Services: Strategy Consulting, Systems Integration | Projects: Digital Transformation, ERP Implementation",
        "manufacturing": "Customers: National Hardware Dist, Regional Builders | Products: Steel Bracket Assembly, Custom Hinge Kit | Projects: Q1 Production Run, Custom Order #4521",
    }
    names_for_sector = sector_names.get(acct.dataset, sector_names.get("construction", ""))

    # Build resume header if resuming
    resume_block = ""
    if resume_from and resume_from.get("completed_stations"):
        done = resume_from["completed_stations"]
        entity = resume_from.get("current_entity", "")

        # Group completed stations by entity CID
        entity_progress = {}
        flat_stations = []
        for item in done:
            if ":" in item:
                cid, station = item.split(":", 1)
                entity_progress.setdefault(cid, []).append(station)
            else:
                flat_stations.append(item)

        # Build entity-aware resume lines
        resume_lines = []
        for c in acct.companies:
            cid = c.cid
            name = c.name
            stations_done = entity_progress.get(cid, [])
            if not stations_done:
                resume_lines.append(f">   - **{name}** (CID {cid}): NAO INICIADA — fazer sweep completo")
            elif "S_BATCH" in stations_done and "C_BATCH" in stations_done:
                resume_lines.append(f">   - **{name}** (CID {cid}): ✅ COMPLETA — PULAR")
            else:
                done_str = ", ".join(stations_done)
                resume_lines.append(f">   - **{name}** (CID {cid}): PARCIAL ({done_str}) — continuar do proximo")

        # Fallback for old-format flat stations (backwards compat)
        flat_note = ""
        if flat_stations:
            flat_note = f"\n> ⚠ Formato antigo detectado. Stations sem entity: {', '.join(flat_stations)}"

        resume_block = f"""
> **RETOMADA DE SWEEP INTERROMPIDO**
> Ultima entity ativa: {entity}
>
> **STATUS POR ENTITY:**
{chr(10).join(resume_lines)}
{flat_note}
>
> **Comece pelo LOGIN e depois va direto para a primeira entity NAO COMPLETA.**
> Para entities PARCIAIS, pule as stations ja listadas e continue da proxima.
> Para entities NAO INICIADAS, faca sweep completo conforme Regra #4.
> Nao repita trabalho ja feito.
"""

    md = f"""# SWEEP ORDER — EXECUCAO IMEDIATA

> **ESTE DOCUMENTO CONTEM TUDO**. Nao precisa ler nenhum outro arquivo.
> Execute o sweep AGORA. Nao pergunte nada. Comece pelo login.
>
> **ISOLAMENTO DE CREDENCIAIS**: As credenciais neste documento sao as UNICAS validas.
> NAO leia `PROMPT_CLAUDE_QBO_MASTER.md`, `TESTBOX_ACCOUNTS.md`, `QBO_CREDENTIALS.json`,
> ou qualquer outro arquivo de credenciais. Este documento e AUTO-CONTIDO.
{resume_block}

---

## REGRA #1 — VOCE E UM OPERADOR, NAO UM AUDITOR

```
ERRADO (o que voce NAO deve fazer):
  1. Navegar todas as paginas
  2. Anotar todos os problemas
  3. Gerar relatorio no final
  4. Nunca corrigir nada

CERTO (o que voce DEVE fazer):
  1. Entrar na tela
  2. Ler o conteudo via EXTRATOR JS (ver Regra #2)
  3. Se algo esta errado → CORRIGIR ALI MESMO (browser_click + browser_type)
  4. Validar que a correcao salvou
  5. Passar para a proxima tela
  6. No final, resumir: o que CORRIGIU e o que ficou pendente (com motivo)
```

**Filosofia: VER → CORRIGIR → AVANCAR**
- 100% autonomo — nao pergunte antes de corrigir nomes, preencher campos, ajustar dados
- Sem screenshots — nao salve prints a menos que o usuario peca
- Sem relatorio intermediario — corrija e avance
- Se travou 2x no mesmo item → documente e avance, nao entre em loop

## REGRA #2 — TOKEN MANAGEMENT (CRITICO — SEGUIR A RISCA)

```
=== LIMITES ABSOLUTOS ===
1. NUNCA retornar innerText bruto com substring > 500 chars
2. NUNCA ler o output de browser_navigate — ele retorna HTML gigante (13K+ tokens)
3. Apos QUALQUER browser_navigate, fazer IMEDIATAMENTE um browser_evaluate com extrator
4. Se precisa mais dados, fazer 2 evaluates PEQUENOS — nunca 1 grande
5. Se browser_evaluate estourar limite, NAO leia o arquivo salvo — refaca com extrator menor

=== PROIBIDO ===
- browser_snapshot() em paginas longas (gera 90KB+ de output)
- document.body.innerText.substring(0, N) onde N > 500
- Retornar JSON com campo "text" ou "snippet" longo

=== OBRIGATORIO: USAR EXTRATORES PRE-PRONTOS ===
Copie e cole os extratores abaixo EXATAMENTE como estao. NAO improvise JS.
```

### EXTRATORES JS PRE-PRONTOS (copiar e colar)

**EXTRATOR 1 — Dashboard (D01):**
```javascript
() => {{
  const t = document.body.innerText || '';
  const co = document.querySelector('[class*="company"]')?.innerText || t.match(/^.*LLC|^.*Inc|^.*Corp/m)?.[0] || '';
  const nums = t.match(/\\$[\\d,.]+[KMB]?/g)?.slice(0, 8) || [];
  return JSON.stringify({{co: co.substring(0,80), nums, has404: /not found|404/i.test(t), hasTBX: /\\bTBX\\b/.test(t)}});
}}
```

**EXTRATOR 2 — P&L / Financial Report (D02):**
```javascript
() => {{
  const t = document.body.innerText || '';
  const income = t.match(/(?:Total |Net )?Income[\\s:]*\\$?([\\d,.]+)/i)?.[1] || 'N/A';
  const expenses = t.match(/(?:Total )?Expenses[\\s:]*\\$?([\\d,.]+)/i)?.[1] || 'N/A';
  const net = t.match(/Net (?:Income|Profit)[\\s:]*\\-?\\$?([\\d,.\\-]+)/i)?.[1] || 'N/A';
  const neg = t.includes('-$') || t.match(/Net.*-/);
  return JSON.stringify({{income, expenses, net, negative: !!neg, title: document.title.substring(0,60)}});
}}
```

**EXTRATOR 3 — Lista de Entidades (Customers/Vendors/Employees/Products):**
```javascript
() => {{
  const t = document.body.innerText || '';
  const count = t.match(/(\\d[\\d,]*)\\s*(?:results|customers|vendors|employees|items)/i)?.[1] || '0';
  const rows = t.match(/^.{{3,60}}$/gm)?.filter(l => !l.match(/Home|Feed|Create|Bookmarks|Skip/))?.slice(0, 8) || [];
  const hasPH = /\\b(TBX|Test|TESTER|Lorem|Sample|Foo)\\b/i.test(t);
  return JSON.stringify({{count, first8: rows, hasPlaceholder: hasPH, has404: /not found|404/i.test(t)}});
}}
```

**EXTRATOR 4 — Surface Scan Generico (S01-S30):**
```javascript
() => {{
  const t = document.body.innerText || '';
  const lines = t.split('\\n').filter(l => l.trim().length > 2);
  return JSON.stringify({{
    title: document.title.substring(0,50),
    lines: lines.length,
    hasData: lines.length > 10,
    has404: /not found|404|page doesn't exist/i.test(t),
    hasPH: /\\b(TBX|Lorem|Sample|Foo|Bar|TODO)\\b/i.test(t),
    first5: lines.slice(2, 7).map(l => l.substring(0, 60))
  }});
}}
```

**EXTRATOR 5 — Verificar Entity Apos Switch:**
```javascript
() => {{
  const t = (document.body.innerText || '').substring(0, 300);
  return JSON.stringify({{
    url: window.location.href.substring(0, 80),
    company: t.match(/^.*(?:LLC|Inc|Corp|Ltd|Group|Solutions|Outfitters|Tire|Retail)/m)?.[0]?.substring(0, 60) || 'unknown',
    loaded: !(/loading|please wait/i.test(t))
  }});
}}
```

**EXTRATOR 6 — Balance Sheet via Sidebar (D03 — IES WORKAROUND):**
```javascript
() => {{
  const links = [...document.querySelectorAll('a, button')];
  const bsLink = links.find(l => /balance.?sheet/i.test(l.innerText));
  const reports = links.filter(l => /profit|loss|aging|cash.?flow|balance/i.test(l.innerText)).map(l => l.innerText.substring(0,40));
  return JSON.stringify({{bsLink: bsLink?.innerText?.substring(0,50) || null, bsHref: bsLink?.href?.substring(0,120) || null, reports}});
}}
```

**EXTRATOR 7 — JE Form (antes de salvar — verificar campos):**
```javascript
() => {{
  const inputs = [...document.querySelectorAll('input[type="text"], input[type="number"], textarea')];
  const vals = inputs.slice(0, 10).map(i => ({{id: i.id?.substring(0,30), val: i.value?.substring(0,30), ph: i.placeholder?.substring(0,20)}}));
  const saveBtn = !!document.querySelector('[data-automation-id*="save"], button[class*="save"]');
  return JSON.stringify({{fields: vals, saveVisible: saveBtn}});
}}
```

## REGRA #2B — POS-NAVEGACAO (OBRIGATORIO)

```
Apos QUALQUER browser_navigate():
1. NAO leia o resultado do navigate (ele vem com HTML gigante)
2. Espere 3-5 segundos (browser_wait_for)
3. NAO leia o resultado do wait_for (ele TAMBEM retorna snapshot gigante, 14K+ tokens)
4. Faca browser_evaluate com o EXTRATOR apropriado
5. Se a pagina ainda esta carregando, espere mais 3s e repita

ATENCAO: browser_wait_for() retorna um snapshot completo da pagina.
Este output vai DIRETO pro contexto e consome tokens massivamente.
NUNCA dependa do output do wait_for — use APENAS para esperar.
```

## REGRA #3 — ANTI-SKIP

```
Para CADA Deep Station voce DEVE reportar no chat:
  [D01] Dashboard ✓ (ou: CORRIGIDO: mudei periodo para All Dates)
  [D02] P&L ✓ Revenue $X, Net $Y (ou: CORRIGIDO: criei JE de $200K)

NAO ACEITO:
  - "Verificado" sem dizer o que viu
  - "Encontrei problema X" sem ter tentado corrigir
  - Pular estacao sem reportar
  - "Same platform as Entity 1" sem ter verificado pelo menos D01+D02+D05+D06

SE NAO CONSEGUIU CORRIGIR, explique POR QUE:
  [D07] Employees — BLOQUEADO: 2FA exigido para editar nomes
```

## REGRA #4 — COBERTURA MINIMA POR ENTITY (OBRIGATORIO)

```
Entity tipo PARENT:
  → D01 a D12 COMPLETO (todos os Deep Stations habilitados)
  → S01-S30 Surface Scan completo
  → C01-C15 Conditional completo

Entity tipo CONSOLIDATED:
  → D01 (Dashboard), D02 (P&L), D10 (Reports), D11 (CoA)
  → C01-C04 (Consolidated-specific)
  → Demais: marcar N/A com justificativa

Entity tipo CHILD:
  → MINIMO OBRIGATORIO: D01 + D02 + D05 + D06 INDIVIDUAL
  → D03-D04, D07-D12: podem ser inferidos SE mesma plataforma
  → Para inferir, deve ter verificado pelo menos 4 stations individualmente
  → NUNCA escrever "Same platform" sem ter feito os 4 checks minimos

PROIBIDO:
  - Marcar child entity como PASS sem ter feito D01+D02+D05+D06
  - Copiar scores do Parent para Children sem verificacao
```

## REGRA #5 — ANTI-LOOP E RECUPERACAO

```
Se browser_evaluate retornar erro "exceeds maximum allowed tokens":
  → NAO leia o arquivo salvo (desperdia tokens)
  → Faca NOVO evaluate com extrator MENOR (use Extrator 5 generico)
  → Se falhar 2x: documente e avance

Se browser_navigate retornar pagina de erro/404:
  → Tente rota alternativa (ver workarounds abaixo)
  → Se falhar 2x: marque BLOCKED e avance

Se JE form travar (IDs dinamicos):
  → browser_snapshot() APENAS para ver o form
  → Preencha UM campo por vez, re-query apos cada field
  → Se travar 2x: documente valores necessarios e avance
  → NAO recarregue a pagina — perdera dados preenchidos
```

---

## 1. LOGIN

| Campo | Valor |
|-------|-------|
| URL | https://accounts.intuit.com/app/sign-in |
| Email | `{acct.email}` |
| Password | `{acct.password}` |
| TOTP Secret | `{acct.totp_secret}` |
| Dataset | {acct.dataset} |

**Procedimento:**
1. `browser_navigate` para `https://accounts.intuit.com/app/sign-in`
2. `browser_snapshot` para ver o formulario (UNICO uso permitido de snapshot para login)
3. `browser_type` no campo de email → clicar next/continue
4. `browser_type` no campo de password → clicar sign in
5. Gerar TOTP via Bash: `python -c "import pyotp,time; t=pyotp.TOTP('{acct.totp_secret}'); r=30-int(time.time())%30; time.sleep(r+1) if r<10 else None; print(t.now())"`
6. `browser_type` no campo de codigo → submit
7. Se "Skip"/"Not now"/"Maybe later" aparecer → clicar para dispensar
8. `browser_evaluate` com **EXTRATOR 1** para confirmar que esta no QBO homepage

**IMPORTANTE: Use APENAS Playwright (browser_*). NAO use QuickBooks MCP API.**

## 2. ENTITIES ({len(acct.companies)})

| Nome | CID | Tipo | Prioridade |
|------|-----|------|------------|
{chr(10).join(companies_lines)}

**Ordem**: P0 primeiro (Deep + Surface + Conditional completo), depois P1 (apenas Deep D01-D02 rapido).
{switch_block}
**Apos trocar entity**: usar **EXTRATOR 5** para confirmar switch. NAO use browser_snapshot.

## 3. DEEP STATIONS ({deep} habilitados) — VER/CORRIGIR/AVANCAR

{"".join(deep_lines) if deep_lines else "Nenhum deep check habilitado."}

### IES WORKAROUNDS (rotas que dao 404 no IES)

```
PROBLEMA: /app/reportlist retorna 404 no IES (Intuit Enterprise Suite)

WORKAROUND para P&L e Balance Sheet:
1. browser_navigate("https://qbo.intuit.com/app/standardreports")
2. browser_wait_for(time=3)
3. browser_evaluate com EXTRATOR 6 para encontrar links de reports
4. browser_click no link de "Profit and Loss" ou "Balance Sheet"
5. browser_wait_for(time=5)
6. browser_evaluate com EXTRATOR 2 para ler numeros

ROTAS FUNCIONAIS NO IES:
- /app/homepage — Dashboard
- /app/banking?jobId=accounting — Banking
- /app/customers-overview?jobId=customers — Customer Hub
- /app/customers — Customer list
- /app/vendors — Vendor list
- /app/expense-overview?jobId=expenses — Expenses
- /app/employees?jobId=team — Employees
- /app/inventory/overview?jobId=inventory — Inventory
- /app/projects-overview?jobId=projects — Projects
- /app/standardreports — Reports (sidebar, click links)
- /app/chartofaccounts?jobId=accounting — Chart of Accounts
- /app/settings?panel=company — Settings

ROTAS QUE DAO 404 NO IES (NUNCA usar):
- /app/reportlist
- /app/reports/profitandloss
- /app/balance-sheet
- /app/chart-of-accounts (sem jobId)
```

### PROTOCOLOS DE FIX COMUNS (referencia rapida)

**Criar Journal Entry (para corrigir P&L negativo):**
```
1. browser_navigate("/app/journal")
2. browser_wait_for(time=3)
3. browser_snapshot() → encontrar form (UNICO uso permitido)
4. Linha 1: Account = "Accounts Receivable" | Amount (Debit) = $200000 | Name = cliente existente
5. Linha 2: Account = "Sales" ou "Revenue" ou "Grant Revenue" (NP) | Amount (Credit) auto-preenche
6. Memo: "Revenue adjustment - [motivo realista]"
7. IMPORTANTE: Preencher UM campo, verificar com EXTRATOR 7, depois proximo campo
8. browser_click("Save and close")
9. browser_wait_for(time=3)
10. Verificar P&L com EXTRATOR 2 para confirmar Net Income positivo
```

**Renomear placeholder (customer/vendor/product):**
```
1. browser_click no nome do record na lista
2. browser_wait_for(time=2)
3. browser_evaluate com EXTRATOR 3 para ver estado atual
4. browser_click("Edit")
5. browser_type no campo de nome → novo nome realista
6. browser_click("Save")
```

**Preencher campo vazio (email, address, notes, terms):**
```
1. Dentro do detail do record → browser_click("Edit")
2. browser_type nos campos vazios
3. browser_click("Save")
```

**Nomes realistas para {acct.dataset}:**
{names_for_sector}

## 4. SURFACE SCAN ({surface} habilitados) — RAPIDO, SEM CORRECAO

{chr(10).join(surface_lines) if surface_lines else "Nenhum surface check habilitado."}

**Protocolo**: `browser_navigate` → `browser_wait_for(time=3)` → `browser_evaluate` com **EXTRATOR 4** → anotar ✓/○/✗/⚠ → proximo
- ✓ = tem dados | ○ = vazio | ✗ = 404 | ⚠ = placeholder/problema

**OTIMIZACAO**: Agrupar 5-6 surface scans consecutivos, reportar em lote:
```
[S01-S06] ✓✓✓○✗✓ (S04 vazio, S05 404)
[S07-S12] ✓✓✓✓✓✗ (S12 404)
...
```

**SE USAR browser_run_code para batching:**
```
OBRIGATORIO: truncar TODOS os textos para 50 chars max.
Retornar APENAS status (OK/X/EMPTY) + snippet curto.
NAO retornar bodyText.substring(0, 300) — isso estoura o limite.

Exemplo correto:
  results[id] = {{ status: is404 ? 'X' : hasData ? 'OK' : 'EMPTY', snippet: bodyText.substring(0, 50) }};

NUNCA retornar campos longos como 'title', 'fullText', 'content'.
Se o resultado do run_code estourar o limite, NAO leia o arquivo salvo.
Refaca com snippets ainda menores (30 chars).
```

## 5. CONDITIONAL ({cond} habilitados)

{chr(10).join(cond_lines) if cond_lines else "Nenhum conditional check habilitado."}

## 6. CONTENT SAFETY (aplicar em TODAS as paginas)

{chr(10).join(safety_lines) if safety_lines else "Content safety desabilitado."}

**Se encontrar CS1 (profanity) ou CS4 (PII)**: PARAR e corrigir IMEDIATAMENTE.
**Se encontrar CS2 (placeholder como "Foo", "TBX")**: corrigir inline com nome realista.

## 7. FIX RULES

{chr(10).join(fix_desc)}

Corrigir imediatamente (sem perguntar):
- Placeholder text (TBX, Test, Lorem, Foo, Bar) → renomear
- Campos vazios em top records (company name, email, address, phone, notes, terms)
- P&L negativo → criar JE (DR AR / CR Revenue) ate ficar positivo
- Report periodo errado → mudar para All Dates
- Nomes genericos ("Project 1", "Vendor A") → renomear com nome do setor
- Bank transactions uncategorized (top 5-10) → categorizar

NUNCA corrigir:
- Company settings (nome legal, EIN, endereco fiscal)
- Employee edits bloqueados por 2FA
- Feature flags (dependem da Intuit)
- Payroll data
- Deletes de qualquer tipo

## 8. REALISM SCORING

{"HABILITADO — ao final, pontuar 10 criterios de 1-10 (viabilidade financeira, coerencia de nomes, volume de dados, diversidade de transacoes, banking health, AR/AP balance, payroll, projects, reports, storytelling)." if profile_data.get("realism_scoring", True) else "DESABILITADO"}

## 9. OUTPUT

**No chat** durante execucao (formato minimo):
```
Logado em {acct.label} → [nome empresa]

--- ENTITY 1: [nome] (parent) ---
[D01] Dashboard ✓ Income $X
[D02] P&L ✓ Revenue $X, Net $Y, Margin Z%
[D03] Balance Sheet ✓ Assets $X (via sidebar workaround)
...
[D12] Settings ✓

--- SURFACE SCAN ({surface} pages) ---
[S01-S06] ✓✓✓○✗✓
[S07-S12] ✓✓✓✓✓✗
[S13-S18] ✓✓✓✓○✓
[S19-S24] ✓✓✓✓✓✓
[S25-S{surface:02d}] ✓✓✓✓✓✓

--- CONDITIONAL ({cond}) ---
[C01-C04] ✓✓✓✓
[C05-...] N/A N/A ...

→ Switching to Entity 2: [nome]...
--- ENTITY 2: [nome] (child) ---
[D01] Dashboard ✓ ...
[D02] P&L ✓ ...
[D05] Customers ✓ ...
[D06] Vendors ✓ ...
```

**Salvar report** em: `C:/Users/adm_r/Clients/intuit-boom/knowledge-base/sweep-learnings/{acct.shortcode}_YYYY-MM-DD.md`

**Atualizar LATEST_SWEEP.json**: ao terminar, atualizar status para "completed" e preencher overall_score, realism_score, findings_count.

## 10. PROGRESS TRACKING (OBRIGATORIO)

**Apos CADA Deep Station completada**, atualize o arquivo de progresso.
**FORMATO: CID:STATION** (ex: `9341455130122367:D01`) — NUNCA station sem CID.

```bash
python -c "
import json; f='C:/Users/adm_r/Clients/intuit-boom/dashboard/pending/LATEST_SWEEP.json'
d=json.loads(open(f,encoding='utf-8').read())
p=d.get('progress',{{}})
done=p.get('completed_stations',[])
done.append('CID:STATION_ID')  # ex: 9341455130122367:D01, 9341455130122367:S_BATCH
p['completed_stations']=done
p['current_entity']='ENTITY_NAME (CID)'
p['last_update']=__import__('datetime').datetime.now().isoformat()
d['progress']=p
open(f,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=True))
"
```

**Regras de progresso:**
- **SEMPRE** prefixar com CID da entity atual: `CID:D01`, `CID:D02`, `CID:S_BATCH`, `CID:C_BATCH`
- Atualize `current_entity` ao trocar de entity (incluir CID)
- Surface Scan: registre como `CID:S_BATCH` (um registro por entity)
- Conditional: registre como `CID:C_BATCH` (um registro por entity)
- Se o sweep for interrompido, o dashboard detecta e oferece "Retomar Sweep"
- Na retomada, voce recebera progresso POR ENTITY — pule apenas as entities/stations ja feitas
- **NUNCA** registrar station sem CID (formato antigo `D01` nao funciona no resume)

## 11. CHECKLIST PRE-REPORT (OBRIGATORIO)

```
ANTES de salvar o report, confirme TODOS os items abaixo.
Se algum esta faltando → VOLTE e complete antes de salvar.

- [ ] Parent: D01-D12 todos reportados individualmente com dados?
- [ ] Consolidated (se existir): D01+D02+D10+D11 verificados?
- [ ] CADA child: D01+D02+D05+D06 verificados INDIVIDUALMENTE?
      (NAO vale "same platform as Parent")
- [ ] D04: categorizou 5+ bank transactions? (OBRIGATORIO)
- [ ] D09: tem 3+ projects? Se nao, criou? (OBRIGATORIO)
- [ ] Content Safety: CS1-CS8 verificados em TODAS entities?
- [ ] Progress tracking: todas stations gravadas com CID:STATION?
```

{f"## 12. NOTAS{chr(10)}{chr(10)}{notes}" if notes else ""}

---
*Gerado em {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} pelo QBO Demo Manager Dashboard v4.2*
"""

    order_file = pending_dir / "SWEEP_ORDER.md"
    order_file.write_text(md.strip(), encoding="utf-8")


@app.post("/api/config/activate-sweep", response_class=HTMLResponse)
async def api_activate_sweep(request: Request, profile: str = "full_sweep", account: str = "", force: str = ""):
    """Save sweep config to pending file. Claude Code reads it on 'roda'."""
    import datetime
    import json as json_mod

    if not account:
        return HTMLResponse("<div class='error'>No account selected</div>", status_code=400)

    acct = get_account(account)
    if not acct:
        return HTMLResponse(f"<div class='error'>Account '{account}' not found</div>", status_code=404)

    # Save structured config (not just text prompt)
    pending_dir = BASE / "pending"
    pending_dir.mkdir(exist_ok=True)

    # --- SWEEP LOCK: prevent double activation ---
    latest_file = pending_dir / "LATEST_SWEEP.json"
    if latest_file.exists() and force != "1":
        try:
            existing = json_mod.loads(latest_file.read_text(encoding="utf-8"))
            if existing.get("status") == "pending" and existing.get("pid"):
                # Verify sweep process is actually running before blocking
                import subprocess as _sp

                check = _sp.run(
                    ["tasklist", "/FI", f"PID eq {existing['pid']}", "/NH"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if str(existing["pid"]) in check.stdout:
                    # Process alive — redirect to dashboard where banner shows status
                    from fastapi.responses import RedirectResponse

                    return RedirectResponse(url="/", status_code=303)
                # Process dead — stale lock, proceed with new sweep
        except (json_mod.JSONDecodeError, KeyError):
            pass  # corrupted file, proceed normally

    profiles = load_profiles()
    p = profiles.get(profile, profiles["full_sweep"])

    sweep_order = {
        "activated_at": datetime.datetime.now().isoformat(),
        "account": {
            "shortcode": acct.shortcode,
            "email": acct.email,
            "label": acct.label,
            "password": acct.password,
            "totp_secret": acct.totp_secret,
            "dataset": acct.dataset,
            "companies": [c.model_dump() for c in acct.companies],
        },
        "profile": profile,
        "profile_name": p["name"],
        "checks": p.get("checks", {}),
        "fix_tiers": p.get("fix_tiers", {}),
        "content_safety": p.get("content_safety", {}),
        "realism_scoring": p.get("realism_scoring", True),
        "notes": get_account_config(account).get("notes", ""),
        "status": "pending",
    }

    latest_file = pending_dir / "LATEST_SWEEP.json"
    latest_file.write_text(json_mod.dumps(sweep_order, indent=2, ensure_ascii=False), encoding="utf-8")

    # Count enabled checks
    deep = sum(1 for k, v in p.get("checks", {}).items() if k.startswith("D") and v)
    surface = sum(1 for k, v in p.get("checks", {}).items() if k.startswith("S") and v)
    cond = sum(1 for k, v in p.get("checks", {}).items() if k.startswith("C") and v)

    # Generate SWEEP_ORDER.md — comprehensive instructions for new Claude session
    _generate_sweep_order_md(pending_dir, acct, p, profile, deep, surface, cond)

    # Launch Claude autonomously via batch file + start (reliable visible window)
    import os
    import subprocess as sp

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)  # Allow spawning Claude from within Claude sessions

    # Sanitize label for cmd.exe (strip parens and special chars)
    safe_label = acct.label.replace("(", "").replace(")", "").replace("&", "").replace("|", "")
    sweep_title = f"QBO Sweep - {safe_label}"

    # Write batch file — avoids all quoting issues
    bat_file = pending_dir / "run_sweep.bat"
    bat_file.write_text(
        f"@echo off\n"
        f"title {sweep_title}\n"
        f"cd /d {BASE.parent}\n"
        f'claude "Pending sweep detected. Read dashboard/pending/SWEEP_ORDER.md and execute it. Use ONLY the credentials in SWEEP_ORDER.md. Do NOT read PROMPT_CLAUDE_QBO_MASTER.md or TESTBOX_ACCOUNTS.md."'
        f" --permission-mode bypassPermissions\n"
        f"echo.\n"
        f"echo === SWEEP FINALIZADO ===\n"
        f"pause\n",
        encoding="utf-8",
    )

    # CREATE_NEW_CONSOLE opens a visible window AND gives us the real PID
    proc = sp.Popen(
        ["cmd", "/c", str(bat_file)],
        creationflags=sp.CREATE_NEW_CONSOLE,
        env=env,
    )

    # Store PID + window title for stop-sweep
    sweep_order["pid"] = proc.pid
    sweep_order["window_title"] = sweep_title
    latest_file.write_text(json_mod.dumps(sweep_order, indent=2, ensure_ascii=False), encoding="utf-8")

    # Redirect to dashboard — sweep status banner will show there
    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/", status_code=303)


@app.post("/api/config/stop-sweep", response_class=HTMLResponse)
async def api_stop_sweep():
    """Kill running Claude sweep process and reset LATEST_SWEEP.json status."""
    import json as json_mod
    import subprocess as sp

    pending_dir = BASE / "pending"
    latest_file = pending_dir / "LATEST_SWEEP.json"
    data = None
    # 1. Reset JSON status
    if latest_file.exists():
        try:
            data = json_mod.loads(latest_file.read_text(encoding="utf-8"))
            data["status"] = "cancelled"
            latest_file.write_text(json_mod.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    # 2. Kill sweep process tree by PID (reliable) + fallback by window title
    pid = data.get("pid") if data else None
    if pid:
        try:
            sp.run(
                f"taskkill /F /PID {pid} /T",
                shell=True,
                capture_output=True,
                timeout=10,
            )
        except Exception:
            pass
    # Fallback: also kill any remaining QBO Sweep windows
    try:
        sp.run(
            'taskkill /F /FI "WINDOWTITLE eq QBO Sweep*" /T',
            shell=True,
            capture_output=True,
            timeout=10,
        )
    except Exception:
        pass

    # Redirect to dashboard — banner will be gone since status is now cancelled
    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/", status_code=303)


@app.post("/api/config/resume-sweep", response_class=HTMLResponse)
async def api_resume_sweep():
    """Resume an interrupted sweep from where it left off."""
    import datetime
    import json as json_mod
    import os
    import subprocess as sp

    pending_dir = BASE / "pending"
    latest_file = pending_dir / "LATEST_SWEEP.json"

    if not latest_file.exists():
        return HTMLResponse("<div class='error'>No sweep to resume</div>", status_code=400)

    data = json_mod.loads(latest_file.read_text(encoding="utf-8"))
    if data.get("status") not in ("interrupted", "cancelled"):
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url="/", status_code=303)

    # Get account and profile
    acct_info = data.get("account", {})
    acct = get_account(acct_info.get("shortcode", ""))
    if not acct:
        return HTMLResponse("<div class='error'>Account not found</div>", status_code=404)

    profiles = load_profiles()
    profile_key = data.get("profile", "full_sweep")
    p = profiles.get(profile_key, profiles["full_sweep"])

    # Extract progress
    progress = data.get("progress", {})

    # Count enabled checks
    deep = sum(1 for k, v in p.get("checks", {}).items() if k.startswith("D") and v)
    surface = sum(1 for k, v in p.get("checks", {}).items() if k.startswith("S") and v)
    cond = sum(1 for k, v in p.get("checks", {}).items() if k.startswith("C") and v)

    # Regenerate SWEEP_ORDER.md with resume info
    _generate_sweep_order_md(pending_dir, acct, p, profile_key, deep, surface, cond, resume_from=progress)

    # Update status back to pending
    data["status"] = "pending"
    data["resumed_at"] = datetime.datetime.now().isoformat()

    # Sanitize label for cmd.exe
    safe_label = acct.label.replace("(", "").replace(")", "").replace("&", "").replace("|", "")
    sweep_title = f"QBO Sweep - {safe_label}"

    # Write batch file
    bat_file = pending_dir / "run_sweep.bat"
    bat_file.write_text(
        f"@echo off\n"
        f"title {sweep_title}\n"
        f"cd /d {BASE.parent}\n"
        f'claude "Retomar sweep interrompido conforme protocolo CLAUDE.md - continuar de onde parou"'
        f" --permission-mode bypassPermissions\n"
        f"echo.\n"
        f"echo === SWEEP FINALIZADO ===\n"
        f"pause\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    proc = sp.Popen(
        ["cmd", "/c", str(bat_file)],
        creationflags=sp.CREATE_NEW_CONSOLE,
        env=env,
    )

    data["pid"] = proc.pid
    data["window_title"] = sweep_title
    latest_file.write_text(json_mod.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/", status_code=303)


# ─── Action API ───


@app.post("/api/test-login/{shortcode}", response_class=HTMLResponse)
async def api_test_login(request: Request, shortcode: str):
    account = get_account(shortcode)
    if not account:
        return HTMLResponse("<div class='error'>Account not found</div>", status_code=404)
    result = test_login(account)
    return templates.TemplateResponse(
        "partials/action_log.html",
        {
            "request": request,
            "action": "login",
            "result": result,
        },
    )


@app.post("/api/sweep/{shortcode}", response_class=HTMLResponse)
async def api_sweep(request: Request, shortcode: str):
    account = get_account(shortcode)
    if not account:
        return HTMLResponse("<div class='error'>Account not found</div>", status_code=404)
    prompt = generate_sweep_prompt(account)
    return templates.TemplateResponse(
        "partials/action_log.html",
        {
            "request": request,
            "action": "sweep",
            "prompt": prompt,
        },
    )


@app.post("/api/sync-retool", response_class=HTMLResponse)
async def api_sync_retool(request: Request):
    result = sync_retool()
    return templates.TemplateResponse(
        "partials/action_log.html",
        {
            "request": request,
            "action": "retool",
            "result": result,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
