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
    """Read LATEST_SWEEP.json and return data if status is pending."""
    import json as json_mod

    sweep_file = BASE / "pending" / "LATEST_SWEEP.json"
    if not sweep_file.exists():
        return None
    try:
        data = json_mod.loads(sweep_file.read_text(encoding="utf-8"))
        if data.get("status") == "pending":
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


def _generate_sweep_order_md(pending_dir, acct, profile_data, profile_key, deep, surface, cond):
    """Generate a comprehensive SWEEP_ORDER.md the new Claude session can follow.

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
→ browser_snapshot() para confirmar switch

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

    md = f"""# SWEEP ORDER — EXECUCAO IMEDIATA

> **ESTE DOCUMENTO CONTEM TUDO**. Nao precisa ler nenhum outro arquivo.
> Execute o sweep AGORA. Nao pergunte nada. Comece pelo login.

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
  2. Ler o conteudo (browser_snapshot)
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

## REGRA #2 — TOKEN MANAGEMENT

```
PROIBIDO: usar browser_snapshot() em paginas longas (gera 90KB+ de output)

OBRIGATORIO para Surface Scan: usar browser_evaluate() com JS extraction:
  browser_evaluate(function="() => {{
    const text = document.body.innerText;
    const lines = text.split('\\n').filter(l => l.trim().length > 0);
    return {{
      title: document.title,
      lineCount: lines.length,
      first20: lines.slice(0, 20),
      hasData: lines.length > 10,
      hasPlaceholder: /\\b(TBX|Lorem|Sample|Foo|Bar|TODO)\\b/i.test(text),
      has404: /not found|404|page doesn't exist/i.test(text)
    }};
  }}")

PERMITIDO: browser_snapshot() APENAS em Deep Stations onde precisa interagir
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

SE NAO CONSEGUIU CORRIGIR, explique POR QUE:
  [D07] Employees — BLOQUEADO: 2FA exigido para editar nomes
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
2. `browser_snapshot` para ver o formulario
3. `browser_type` no campo de email → clicar next/continue
4. `browser_type` no campo de password → clicar sign in
5. Gerar TOTP via Bash: `python -c "import pyotp,time; t=pyotp.TOTP('{acct.totp_secret}'); r=30-int(time.time())%30; time.sleep(r+1) if r<10 else None; print(t.now())"`
6. `browser_type` no campo de codigo → submit
7. Se "Skip"/"Not now"/"Maybe later" aparecer → clicar para dispensar
8. `browser_snapshot` para confirmar que esta no QBO homepage

**IMPORTANTE: Use APENAS Playwright (browser_*). NAO use QuickBooks MCP API.**

## 2. ENTITIES ({len(acct.companies)})

| Nome | CID | Tipo | Prioridade |
|------|-----|------|------------|
{chr(10).join(companies_lines)}

**Ordem**: P0 primeiro (Deep + Surface + Conditional completo), depois P1 (apenas Deep D01-D02 rapido).
{switch_block}

## 3. DEEP STATIONS ({deep} habilitados) — VER/CORRIGIR/AVANCAR

{"".join(deep_lines) if deep_lines else "Nenhum deep check habilitado."}

### PROTOCOLOS DE FIX COMUNS (referencia rapida)

**Criar Journal Entry (para corrigir P&L negativo):**
```
1. browser_navigate("/app/journal")
2. browser_snapshot() → encontrar form
3. Linha 1: Account = "Accounts Receivable" | Amount (Debit) = $200000 | Name = cliente existente
4. Linha 2: Account = "Sales" ou "Revenue" ou "Grant Revenue" (NP) | Amount (Credit) auto-preenche
5. Memo: "Revenue adjustment - [motivo realista]"
6. browser_click("Save and close")
7. Voltar para P&L e confirmar que Net Income ficou positivo
```

**Renomear placeholder (customer/vendor/product):**
```
1. browser_click no nome do record na lista
2. browser_snapshot() → encontrar botao Edit
3. browser_click("Edit")
4. browser_type no campo de nome → novo nome realista
5. browser_click("Save")
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

**Protocolo**: `browser_navigate` → `browser_evaluate` (JS extraction, NAO snapshot) → anotar ✓/○/✗/⚠ → proximo
- ✓ = tem dados | ○ = vazio | ✗ = 404 | ⚠ = placeholder/problema

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

--- DEEP STATIONS ({deep}) ---
[D01] Dashboard ✓ (ou CORRIGIDO: ...)
[D02] P&L ✓ Revenue $X, Net $Y, Margin Z%
...
→ Switching to [proxima entity]...

--- SURFACE SCAN ({surface} pages) ---
[S01-S{surface:02d}] ✓X ○Y ✗Z

--- CONDITIONAL ({cond}) ---
[C01-...] ✓X N/A Y
```

**Salvar report** em: `C:/Users/adm_r/Clients/intuit-boom/knowledge-base/sweep-learnings/{acct.shortcode}_YYYY-MM-DD.md`

**Atualizar LATEST_SWEEP.json**: ao terminar, atualizar status para "completed" e preencher overall_score, realism_score, findings_count.

{f"## 10. NOTAS{chr(10)}{chr(10)}{notes}" if notes else ""}

---
*Gerado em {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} pelo QBO Demo Manager Dashboard*
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
            if existing.get("status") == "pending":
                # Already running — redirect to dashboard where banner shows status
                from fastapi.responses import RedirectResponse

                return RedirectResponse(url="/", status_code=303)
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
    # 1. Reset JSON status
    if latest_file.exists():
        try:
            data = json_mod.loads(latest_file.read_text(encoding="utf-8"))
            data["status"] = "cancelled"
            latest_file.write_text(json_mod.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    # 2. Kill Claude processes spawned by sweep (cmd.exe windows running claude)
    killed = 0
    try:
        result = sp.run(
            ["tasklist", "/V", "/FI", "WINDOWTITLE eq Claude*", "/FO", "CSV"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        for line in result.stdout.strip().split("\n")[1:]:
            if "Claude" in line:
                parts = line.strip('"').split('","')
                if len(parts) >= 2:
                    pid = parts[1]
                    sp.run(
                        ["taskkill", "/F", "/PID", pid, "/T"],
                        capture_output=True,
                        timeout=5,
                    )
                    killed += 1
    except Exception:
        pass

    # Redirect to dashboard — banner will be gone since status is now cancelled
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
