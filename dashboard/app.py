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
from data import compute_sweep_delta, get_account, load_accounts, load_sweep_history
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
    # Compute deltas for trend indicators in the table
    deltas = {}
    for acct in accounts:
        d = compute_sweep_delta(acct.shortcode)
        if d:
            deltas[acct.shortcode] = d
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "accounts": accounts,
            "total_entities": total_entities,
            "active_sweep": active_sweep,
            "deltas": deltas,
        },
    )


@app.get("/account/{shortcode}", response_class=HTMLResponse)
async def account_detail(request: Request, shortcode: str):
    account = get_account(shortcode)
    if not account:
        return HTMLResponse(f"<h2>Account '{shortcode}' not found</h2>", status_code=404)
    history = load_sweep_history(shortcode)
    delta = compute_sweep_delta(shortcode)
    # Build sparkline data (only entries with health)
    sparkline = [{"date": e.date, "health": e.health} for e in history if e.health is not None]
    return templates.TemplateResponse(
        "account.html",
        {
            "request": request,
            "account": account,
            "history": history,
            "delta": delta,
            "sparkline": sparkline,
        },
    )


@app.get("/api/accounts/{shortcode}/history")
async def account_history(shortcode: str):
    """API: return sweep history + delta for an account."""
    history = load_sweep_history(shortcode)
    delta = compute_sweep_delta(shortcode)
    return {"history": [e.model_dump() for e in history], "delta": delta}


# ─── Config Panel ───


@app.get("/config", response_class=HTMLResponse)
async def config_panel(request: Request, profile: str = "", account: str = ""):
    accounts = load_accounts()
    profiles = load_profiles()

    # If account is specified and no explicit profile override, use account's saved profile
    acct_cfg = get_account_config(account) if account else {}
    if not profile and acct_cfg.get("profile") and acct_cfg["profile"] in profiles:
        active_profile = acct_cfg["profile"]
    else:
        active_profile = profile if profile and profile in profiles else "full_sweep"
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
    if "key" not in body or "profile" not in body:
        return JSONResponse({"error": "Missing required fields: key, profile"}, status_code=422)
    save_profile(body["key"], body["profile"])
    return JSONResponse({"status": "ok"})


@app.post("/api/config/save-account")
async def api_save_account(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=422)
    if "shortcode" not in body or "config" not in body:
        return JSONResponse({"error": "Missing required fields: shortcode, config"}, status_code=422)
    save_account_config(body["shortcode"], body["config"])
    return JSONResponse({"status": "ok"})


def _get_sector_expectations(dataset):
    """Return sector-specific expectations for FASE ZERO context mapping."""
    expectations = {
        "construction": (
            "- Margin 3-15% (thin margins, high volume)\n"
            "- Projects with phases, budgets, job costing\n"
            "- Subcontractors as vendors, lien waivers, certified payroll\n"
            "- Customers are developers, municipalities, school districts\n"
            "- Products are services (Framing, Electrical, HVAC) + some inventory (materials)"
        ),
        "tire_shop": (
            "- Margin 25-35% (retail + service markup)\n"
            "- Fleet customers with maintenance contracts\n"
            "- Vendors are tire manufacturers/distributors (Bridgestone, Michelin, Goodyear)\n"
            "- Mix of service (tire rotation, alignment) + inventory (tires, wheels)\n"
            "- Projects relate to fleet maintenance cycles and dealer programs"
        ),
        "non_profit": (
            "- Margin 2-10% (surplus, not profit — NP terminology)\n"
            "- Donors (not customers), Pledges (not invoices), Programs (not products), Grants (not projects)\n"
            "- Revenue from grants, donations, program fees\n"
            "- Dimensions/classes for program tracking (Youth, Health, Emergency)\n"
            "- Statement of Activity (not P&L), Statement of Financial Position (not BS)"
        ),
        "professional_services": (
            "- Margin 20-40% (high-value consulting)\n"
            "- Clients are enterprises (IT, Health, Government)\n"
            "- Products are service lines (Strategy, Integration, Analytics)\n"
            "- Projects tied to SOWs with milestones\n"
            "- Time tracking is critical (billable hours)"
        ),
        "manufacturing": (
            "- Margin 15-25% (product-based with COGS)\n"
            "- Customers are distributors, retailers, OEM buyers\n"
            "- Vendors are raw material suppliers (steel, components)\n"
            "- Inventory management is central (materials, WIP, finished goods)\n"
            "- Projects relate to production runs, custom orders"
        ),
    }
    return expectations.get(dataset, expectations.get("construction", ""))


def _build_cross_entity_block():
    """Build the cross-entity validation block for SWEEP_ORDER.md."""
    from sweep_checks import CROSS_ENTITY_CHECKS

    lines = []
    for x in CROSS_ENTITY_CHECKS:
        items = "\n".join(f"  - {item}" for item in x["what_to_check"])
        refs = ", ".join(x.get("cross_refs", []))
        lines.append(f"**{x['id']} — {x['name']}**\n{x['description']}\n{items}\nCross-ref: {refs}\n")
    return "\n".join(lines)


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

    # Build enabled deep checks with FULL fix protocols + drill-in + enrichment
    deep_lines = []
    for s in DEEP_STATIONS:
        if not checks.get(s["id"], True):
            continue
        check_items = "\n".join(f"  - {item}" for item in s["what_to_check"])
        fix_items = (
            "\n".join(f"  - {a}" for a in s["fix_actions"]) if s["fix_actions"] else "  - Report only (no auto-fix)"
        )
        # Build optional drill-in section
        drill_block = ""
        if s.get("drill_in"):
            drill_items = "\n".join(f"  - {item}" for item in s["drill_in"])
            drill_block = f"**DRILL-IN** (entrar nos records — OBRIGATORIO):\n{drill_items}\n"
        # Build optional enrichment section
        enrich_block = ""
        if s.get("enrichment"):
            enrich_items = "\n".join(f"  - {item}" for item in s["enrichment"])
            enrich_block = f"**ENRIQUECER** (proativo — nao espere erro, MELHORE o conteudo):\n{enrich_items}\n"
        # Build optional sub_checks section (analytical deep-dive questions)
        sub_block = ""
        if s.get("sub_checks"):
            sub_items = "\n".join(f"  - {item}" for item in s["sub_checks"])
            sub_block = (
                f"**ANALISE CONTEXTUAL** (responder CADA pergunta usando seu conhecimento do setor):\n{sub_items}\n"
            )
        # Build optional cross_refs section
        xref_block = ""
        if s.get("cross_refs"):
            xref_block = f"**CROSS-REF**: Dados desta estacao conectam com {', '.join(s['cross_refs'])}. Anotar valores-chave para comparar depois.\n"
        deep_lines.append(
            f"### {s['id']} — {s['name']}\n"
            f"**Route**: `{s['route']}`\n"
            f"**VER** (ler via EXTRATOR JS):\n{check_items}\n"
            f"{drill_block}"
            f"{sub_block}"
            f"**CORRIGIR** ({'OBRIGATORIO' if s['auto_fix'] and can_fix else 'Reportar apenas'}):\n{fix_items}\n"
            f"{enrich_block}"
            f"{xref_block}"
            f"**AVANCAR**: Só passe ao proximo quando top records estao completos e contextualizados.\n"
        )

    # Build enabled surface checks (with enrichment actions when available)
    surface_lines = []
    for s in SURFACE_SCAN:
        if checks.get(s["id"], True):
            ies_tag = " ⚠IES:404" if s.get("ies_known_404") else ""
            line = f"- **{s['id']}** {s['name']} → `{s['route']}`{ies_tag} — {s['description']}"
            if s.get("auto_fix") and can_fix and s.get("fix_actions"):
                fix_items = chr(10).join(f"    - {a}" for a in s["fix_actions"])
                line += f"\n  **ENRIQUECER SE VAZIO:**\n{fix_items}"
            surface_lines.append(line)

    # Build enabled conditional checks
    cond_lines = []
    for s in CONDITIONAL_CHECKS:
        if checks.get(s["id"], True):
            line = f"- **{s['id']}** {s['name']} (if {s['condition']}) → `{s['route']}` — {s['description']}"
            cond_lines.append(line)

    # Build content safety (with guidance when available)
    safety_lines = []
    for s in CONTENT_SAFETY:
        if safety.get(s["id"], True):
            line = f"- **{s['id']}** {s['name']}: `{s['pattern']}` [{s['severity']}]"
            if s.get("guidance"):
                line += f"\n  _{s['guidance']}_"
            safety_lines.append(line)

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

    # Sector-specific enrichment context (notes templates for D05/D06)
    sector_notes = {
        "construction": (
            "Customer notes: 'General contractor — 12 active job sites in Austin metro. Prefers lump-sum billing.'\n"
            "Customer notes: 'Municipal client — Net 45 required by procurement policy. Primary contact: David Chen, PM.'\n"
            "Vendor notes: 'Primary lumber supplier since 2024. Rep: Maria Santos. Volume discount 8% on orders >$50K.'\n"
            "Vendor notes: 'Concrete supplier — delivers within 48h. Minimum order $5K. Terms: Net 30.'"
        ),
        "tire_shop": (
            "Customer notes: 'Fleet account — 45 vehicles. Quarterly rotation schedule. Contact: Jim Peters, Fleet Mgr.'\n"
            "Customer notes: 'Dealership group — 3 locations. Volume pricing. Annual contract renewal in Q4.'\n"
            "Vendor notes: 'Bridgestone distributor — Southeast region. Rep: Sarah Chen. 5% rebate on quarterly targets.'\n"
            "Vendor notes: 'Equipment supplier — hydraulic lifts and balancers. Service contract included.'"
        ),
        "non_profit": (
            "Donor notes: 'Foundation grant — $250K/year, restricted to Youth Development programs. Report due Q4.'\n"
            "Donor notes: 'Corporate partner since 2023. Sponsors annual gala. Contact: VP of CSR.'\n"
            "Vendor notes: 'Program materials supplier. Bulk pricing for educational kits. Net 30.'\n"
            "Vendor notes: 'Facility management company. Monthly contract $4,500. Includes janitorial + HVAC.'"
        ),
        "professional_services": (
            "Client notes: 'Retainer client — $35K/month. SOW covers digital transformation advisory. Champion: CTO.'\n"
            "Client notes: 'Project-based engagement. Current phase: ERP implementation. Go-live target Q3 2026.'\n"
            "Vendor notes: 'Subcontractor — cloud infrastructure specialists. Rate: $185/hr. NDA on file.'\n"
            "Vendor notes: 'Software licensing reseller. Annual renewals. Handles Microsoft + Salesforce stack.'"
        ),
        "manufacturing": (
            "Customer notes: 'Distribution partner — 6 warehouses. Min order 500 units. Pricing tier A.'\n"
            "Customer notes: 'OEM client — custom brackets per spec #4521. Lead time 3 weeks. QC cert required.'\n"
            "Vendor notes: 'Steel supplier — coil and sheet. Pricing tied to LME index. Net 45.'\n"
            "Vendor notes: 'Tooling vendor — CNC maintenance and replacement parts. Service contract active.'"
        ),
    }
    notes_for_sector = sector_notes.get(acct.dataset, sector_notes.get("construction", ""))

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

    md = f"""# ⚠ ANTES DE QUALQUER ACAO — LEIA ISTO ⚠

```
CHECKPOINT OBRIGATORIO — Execute este comando AGORA, ANTES de login/navegacao/qualquer coisa:

python -c "import json; d=json.loads(open('C:/Users/adm_r/Clients/intuit-boom/dashboard/pending/LATEST_SWEEP.json',encoding='utf-8').read()); p=d.get('progress',{{}}); print('COMPLETED:', p.get('completed_stations',[])); print('FIXES:', p.get('fixes_applied',[])); print('ENTITY:', p.get('current_entity','none'))"

TABELA DE DECISAO (seguir EXATAMENTE):
┌─────────────────────────────────────────┬──────────────────────────────────────────┐
│ SE completed_stations CONTEM...         │ ENTAO...                                 │
├─────────────────────────────────────────┼──────────────────────────────────────────┤
│ CID:D01                                │ NAO navegar para Dashboard. PULAR D01.   │
│ CID:D02                                │ NAO navegar para P&L. PULAR D02.         │
│ CID:D03                                │ NAO navegar para Balance Sheet. PULAR.   │
│ CID:D04                                │ NAO navegar para Banking. PULAR.         │
│ CID:D05                                │ NAO navegar para Customers. PULAR.       │
│ CID:D06                                │ NAO navegar para Vendors. PULAR.         │
│ CID:D07                                │ NAO navegar para Employees. PULAR.       │
│ CID:D08                                │ NAO navegar para Products. PULAR.        │
│ CID:D09                                │ NAO navegar para Projects. PULAR.        │
│ CID:D10                                │ NAO navegar para Reports. PULAR.         │
│ CID:D11                                │ NAO navegar para CoA. PULAR.             │
│ CID:D12                                │ NAO navegar para Settings. PULAR.        │
│ CID:S_BATCH                            │ NAO fazer Surface Scan. PULAR S01-S{len(SURFACE_SCAN):02d}.  │
│ CID:C_BATCH                            │ NAO fazer Conditional. PULAR C01-C{len(CONDITIONAL_CHECKS):02d}.   │
│ D01-D12 + S_BATCH + C_BATCH todos      │ PULAR entity inteira.                    │
└─────────────────────────────────────────┴──────────────────────────────────────────┘

SE fixes_applied NAO esta vazio:
  → Esses records JA FORAM corrigidos. NAO editar de novo.
  → Exemplo: {{"entity":"vendor","name":"Mr IDT TEst Tester","action":"renamed"}}
  → Significa: NAO tocar nesse vendor. Ja foi renomeado.

MOTIVO: Context compaction e session restart podem resetar seu estado mental.
O arquivo de progresso e sua UNICA fonte de verdade. SEMPRE consulte-o.
```

---

# SWEEP ORDER — EXECUCAO IMEDIATA

> **ESTE DOCUMENTO CONTEM TUDO**. Nao precisa ler nenhum outro arquivo.
> Execute o sweep AGORA. Nao pergunte nada.
>
> **ISOLAMENTO DE CREDENCIAIS**: As credenciais neste documento sao as UNICAS validas.
> NAO leia `PROMPT_CLAUDE_QBO_MASTER.md`, `TESTBOX_ACCOUNTS.md`, `QBO_CREDENTIALS.json`,
> ou qualquer outro arquivo de credenciais. Este documento e AUTO-CONTIDO.
{resume_block}

## REGRA #1 — VOCE E UM ANALISTA TSA, NAO UM CHECKLIST BOT

```
ERRADO (checklist mecanico):
  1. Navegar todas as paginas
  2. Verificar se existe dado → sim/nao
  3. Gerar relatorio superficial
  4. Nunca entrar nos records
  5. Nunca enriquecer conteudo

CERTO (analista contextual):
  1. Entrar na tela
  2. Ler o conteudo via EXTRATOR JS (ver Regra #2)
  3. DRILL-IN: clicar nos top records, avaliar profundidade
  4. Se algo esta errado → CORRIGIR ALI MESMO
  5. Se algo esta POBRE (vazio, generico, sem contexto) → ENRIQUECER com dados do setor
  6. Validar que a correcao/enriquecimento salvou
  7. Passar para a proxima tela
  8. No final, resumir: o que CORRIGIU, o que ENRIQUECEU, e o que ficou pendente
```

**Filosofia: VER → DRILL-IN → CORRIGIR → ENRIQUECER → AVANCAR**
- 100% autonomo — nao pergunte antes de corrigir nomes, preencher campos, ajustar dados
- **DRILL-IN obrigatorio**: nao basta ver a lista — clique nos top 3-5 records e avalie o detalhe
- **Enriquecimento proativo**: campo vazio nao e "ok" — e oportunidade de adicionar contexto do setor
- Sem screenshots — nao salve prints a menos que o usuario peca
- Sem relatorio intermediario — corrija, enriqueca e avance
- Se travou 2x no mesmo item → documente e avance, nao entre em loop

**Pergunta-chave em CADA tela**: "Se um prospect visse esta tela agora, acreditaria que e uma empresa real?"

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

=== SUAS RESPOSTAS NO CHAT (CRITICO — EVITAR CONTEXT COMPACTION) ===
Context compaction APAGA seu historico e forca re-leitura de tudo.
Para EVITAR compaction, suas respostas devem ser CURTAS:

FORMATO OBRIGATORIO por station:
  [D01] ✓ Net $292K | Income $256K | Bank $11.3M | No placeholders

FORMATO PROIBIDO (desperdiça tokens):
  "Excellent! The dashboard loaded successfully. I can see the following data:
   - Net Profit: $292,418 (which is positive, that's good)
   - Income: $256,840 (for February)
   ... [20 linhas de analise]"

REGRA: 1 linha por station. Detalhes SÓ se houver PROBLEMA ou FIX.
NAO reexplicar dados ja capturados. NAO narrar cada tool call.
NAO dizer "Let me..." ou "Now I'll..." — apenas FACA.

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
  const income = t.match(/Total\\s+(?:for\\s+)?Income[\\s\\S]{{0,20}}\\$([\\d,.]+)/i)?.[1] || t.match(/Gross\\s+(?:for\\s+)?Income[\\s\\S]{{0,20}}\\$([\\d,.]+)/i)?.[1] || 'N/A';
  const expenses = t.match(/Total\\s+(?:for\\s+)?Expenses[\\s\\S]{{0,20}}\\$([\\d,.]+)/i)?.[1] || 'N/A';
  const net = t.match(/Net\\s+(?:Income|Operating\\s+Income|Profit)[\\s\\S]{{0,20}}\\$?([\\-]?[\\d,.]+)/i)?.[1] || 'N/A';
  const neg = t.includes('-$') || /Net\\s+(?:Income|Profit).*-/.test(t);
  const cogs = t.match(/Cost\\s+of\\s+Goods\\s+Sold[\\s\\S]{{0,20}}\\$([\\d,.]+)/i)?.[1] || null;
  return JSON.stringify({{income, expenses, net, cogs, negative: !!neg, title: document.title.substring(0,60)}});
}}
```

> **ATENCAO**: Este extrator busca "Total Income" ou "Total for Income" (QBO pode usar ambos os formatos dependendo do locale). Valide que o valor faz sentido (>$10K para mid-market). Se retornar N/A, use fallback: `document.querySelectorAll('tr')` e procure a row com "Total" + "Income".

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

**EXTRATOR 4 — Surface Scan Generico (S01-S{len(SURFACE_SCAN):02d}):**
```javascript
() => {{
  const t = document.body.innerText || '';
  const lines = t.split('\\n').filter(l => l.trim().length > 2);
  return JSON.stringify({{
    title: document.title.substring(0,50),
    lines: lines.length,
    hasData: lines.length > 10,
    has404: /not found|404|page doesn't exist/i.test(t),
    hasPH: /\\b(TBX|Lorem|Foo|TODO)\\b/i.test(t),
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

**EXTRATOR 8 — Banking Categorization Helper (D04):**
```javascript
() => {{
  // Get all visible transaction rows with their pre-filled categories
  const rows = [...document.querySelectorAll('tr, [role="row"]')].filter(r => {{
    const t = r.innerText || '';
    return t.includes('Categorize') || t.includes('Match');
  }});
  const txns = rows.slice(0, 10).map((r, i) => {{
    const cells = [...r.querySelectorAll('td, [role="cell"], [role="gridcell"], div[class*="cell"]')];
    if (cells.length < 3) return null;
    return {{
      idx: i,
      date: (cells[1]?.innerText || '').substring(0, 12),
      desc: (cells[2]?.innerText || '').substring(0, 40),
      amount: (cells[3]?.innerText || cells[4]?.innerText || '').substring(0, 15),
      account: (cells[5]?.innerText || cells[6]?.innerText || '').split('\\n')[0]?.substring(0, 40) || '',
      vendor: (cells[7]?.innerText || '').substring(0, 30),
      hasPost: !!(r.querySelector('button') && [...r.querySelectorAll('button')].find(b => b.innerText?.trim() === 'Post'))
    }};
  }}).filter(Boolean);
  const pending = document.body.innerText.match(/(\\d+)\\s*(?:for review|pending|uncategorized)/i)?.[1] || '?';
  return JSON.stringify({{pending, txnCount: txns.length, txns}});
}}
```
> **USO**: Apos abrir Banking, rodar este extrator para ver transacoes pendentes COM categorias pre-preenchidas.
> Para postar: click na description cell (NAO vendor cell — evita popover), esperar form expandir, click Post, handle dialog "Post without class" → click "Post anyway".
> **IMPORTANTE**: Apos CADA post, refs ficam stale. Rodar extrator de novo antes do proximo post.

**EXTRATOR 9 — Balance Sheet Universal (D03):**
```javascript
() => {{
  const rows = [...document.querySelectorAll('tr')];
  const data = {{}};
  rows.forEach(r => {{
    const text = (r.innerText || '').replace(/\\n/g, ' ').trim();
    const match = text.match(/^(Total\\s+(?:for\\s+)?[\\w\\s&\\/()-]+?)\\s+\\$?(-?[\\d,.]+)/i);
    if (match) data[match[1].trim().substring(0, 50)] = match[2];
  }});
  // Fallback: try key accounts directly
  const t = document.body.innerText || '';
  const fallbacks = {{
    'AR': t.match(/Accounts\\s+Receivable[\\s\\S]{{0,30}}\\$([\\d,.]+)/i)?.[1],
    'AP': t.match(/Accounts\\s+Payable[\\s\\S]{{0,30}}\\$([\\d,.]+)/i)?.[1],
    'Bank': t.match(/(?:Total for )?Bank Accounts[\\s\\S]{{0,20}}\\$([\\d,.]+)/i)?.[1],
    'OBE': t.match(/Opening\\s+Balance\\s+Equity[\\s\\S]{{0,20}}\\$([\\d,.]+)/i)?.[1],
    'Retained': t.match(/Retained\\s+Earnings[\\s\\S]{{0,20}}\\$?(-?[\\d,.]+)/i)?.[1],
    'NetIncome': t.match(/Net\\s+Income[\\s\\S]{{0,20}}\\$?(-?[\\d,.]+)/i)?.[1]
  }};
  const negatives = t.match(/-\\$[\\d,.]+/g)?.slice(0, 5) || [];
  const period = t.match(/As of[\\s\\S]{{0,30}}/i)?.[0]?.substring(0, 40) || 'N/A';
  const totalRows = rows.length;
  return JSON.stringify({{totals: data, fallbacks, negatives, period, totalRows}});
}}
```
> **USO**: Rodar UMA VEZ apos BS carregar. Captura TODOS os "Total for X" de uma vez.
> Se totalRows < 40, a pagina pode estar truncada — scroll para baixo e rodar de novo.
> NAO tente regex no body inteiro — use as rows da tabela.

**EXTRATOR 10 — Surface Scan Batch (verificar pagina carregou com dados):**
```javascript
() => {{
  const t = document.body.innerText || '';
  const lines = t.split('\\n').filter(l => l.trim().length > 2);
  const is404 = /not found|404|page doesn't exist|we can't find/i.test(t);
  const isEmpty = lines.length < 5;
  const hasPH = /\\b(TBX|Lorem|Foo|TODO|Test Company)\\b/i.test(t);
  const hasData = lines.length > 10 && !is404;
  return JSON.stringify({{
    status: is404 ? 'X' : isEmpty ? 'EMPTY' : hasPH ? 'WARN' : 'OK',
    lines: lines.length,
    title: document.title.substring(0, 40),
    snippet: lines.slice(2, 5).map(l => l.substring(0, 40)).join(' | ')
  }});
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
  → S01-S{len(SURFACE_SCAN):02d} Surface Scan completo
  → C01-C{len(CONDITIONAL_CHECKS):02d} Conditional completo

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

## REGRA #5B — SESSION KEEPALIVE E RECOVERY

```
=== PREVENCAO (fazer DURANTE o sweep) ===
A cada 15 minutos de sweep (ou entre blocos de estacoes):
  → browser_navigate("https://qbo.intuit.com/app/homepage")
  → browser_evaluate com EXTRATOR 1 para confirmar sessao ativa
  → Se retornar dados normais → sessao OK, continuar
  → Se redirecionar para accounts.intuit.com → sessao expirou, fazer RECOVERY

MOMENTOS IDEAIS para keepalive:
  - Entre D06 e D07 (meio dos deep stations)
  - Antes de iniciar Surface Scan (transicao de fase)
  - Antes de trocar de entity (se multi-entity)

=== RECOVERY (sessao expirou) ===
1. NAO tente manipular o challenge picker via JS (nao funciona)
2. Seguir o MESMO fluxo de login da Secao 1 (cookie clear → email → password → TOTP)
3. Se challenge picker congelar (botoes nao transicionam):
   a. browser_navigate para URL completamente nova: https://accounts.intuit.com/app/sign-in
   b. Esperar 5 segundos
   c. Se aparecer "Welcome back" → clicar na conta
   d. Se pedir password → digitar password
   e. Se pedir TOTP → gerar via python e digitar
   f. Se pedir "Skip phone verification" → clicar Skip
4. Se NADA funcionar apos 3 tentativas:
   a. Salvar progresso (LATEST_SWEEP.json ja esta atualizado se seguiu Regra #10)
   b. Reportar BLOCKED: "Session expired, re-auth failed after 3 attempts"
   c. O dashboard vai oferecer "Retomar Sweep" na proxima execucao
   d. NAO perca 15+ tool calls tentando — 3 tentativas e o maximo

=== DETECCAO AUTOMATICA ===
Se QUALQUER browser_evaluate retornar pagina com "Sign in" ou "Intuit Accounts":
  → Sessao expirou. Executar RECOVERY imediatamente.
  → NAO tente continuar navegando em outras paginas.
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
0. **LIMPAR SESSAO ANTERIOR** (OBRIGATORIO — evita cached login de outra conta):
   PRIMEIRO: `browser_navigate` para `https://accounts.intuit.com/app/sign-in`
   DEPOIS: `browser_evaluate` com: `() => {{ try {{ document.cookie.split(';').forEach(c => {{ document.cookie = c.trim().split('=')[0] + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=.intuit.com'; }}); return 'cookies_cleared'; }} catch(e) {{ return 'cookie_clear_skipped: ' + e.message; }} }}`
   Se cookie clear falhar (SecurityError): ignorar e continuar — o login novo sobrescreve a sessao anterior.
   Se aparecer tela de "Welcome back [outro email]" ou auto-login: clicar "Sign in with a different account" ou "Switch account"
1. (Ja navegado acima) Verificar que esta em `accounts.intuit.com/app/sign-in`
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

## FASE ZERO — CONTEXTO DO NEGOCIO (ANTES das stations)

```
Apos login bem-sucedido e ANTES de iniciar D01, entenda o negocio:

1. Usar EXTRATOR 1 no homepage → anotar mentalmente:
   - Revenue total (widget P&L)
   - Cash position (widget bank)
   - Invoices pendentes (widget invoices)
   - Nome da empresa no header

2. Formular o CONTEXTO em 1 frase:
   "Esta e uma [tipo de empresa] com ~$[X]M de revenue, [N] entities,
    setor [dataset]. Espero ver [expectativas do setor]."

3. Este contexto guia TODAS as decisoes de enriquecimento:
   - Notas de customers/vendors devem refletir este setor
   - Nomes de projetos devem fazer sentido para este negocio
   - Valores de transacoes devem ser proporcionais ao revenue

SETOR: {acct.dataset}
EXPECTATIVAS:
```
{_get_sector_expectations(acct.dataset)}

---

## 3. DEEP STATIONS ({len(deep)} habilitados) — VER/DRILL-IN/CORRIGIR/ENRIQUECER/AVANCAR

{"".join(deep_lines) if deep_lines else "Nenhum deep check habilitado."}

### IES URL MAP (MAPA COMPLETO — SEGUIR A RISCA)

```
=== DOMINIO CORRETO ===
SEMPRE usar: qbo.intuit.com (sem "app." no subdominio)
ERRADO: app.qbo.intuit.com/app/customers  → pode funcionar MAS redireciona e perde sessao
CERTO:  qbo.intuit.com/app/customers

=== ROTAS FUNCIONAIS NO IES (usar EXATAMENTE como estao) ===
Dashboard:        /app/homepage
Banking:          /app/banking?jobId=accounting
Bank Rules:       /app/olbrules?jobId=accounting
Customers:        /app/customers
Customer Hub:     /app/customers-overview?jobId=customers
Vendors:          /app/vendors
Expenses:         /app/expense-overview?jobId=expenses
Employees:        /app/employees?jobId=team
Employees (alt):  /app/employees
Products:         /app/items
Inventory:        /app/inventory/overview?jobId=inventory
Projects:         /app/projects
Reports Hub:      /app/standardreports  ← UNICO ponto de entrada para reports
Chart of Accts:   /app/chartofaccounts?jobId=accounting  ← sem hyphens + jobId
Settings:         Gear icon → "Account and settings" → /app/accountsettings
Estimates:        /app/estimates
Purchase Orders:  /app/purchaseorders
Sales Receipts:   /app/salesreceipts
Invoices:         /app/invoices
Bills:            /app/bills
Journal Entry:    /app/journal
Reconcile:        /app/reconcile?jobId=accounting

=== ROTAS QUE DAO 404 NO IES (NUNCA usar) ===
/app/reportlist           → usar /app/standardreports
/app/reports/profitandloss → click no link dentro de standardreports
/app/balance-sheet        → click no link dentro de standardreports
/app/chart-of-accounts    → /app/chartofaccounts?jobId=accounting
/app/company              → gear icon → Account and settings
/app/companysettings      → gear icon → Account and settings

=== WORKAROUND PARA REPORTS ===
P&L e Balance Sheet NAO tem URL direta no IES.
1. browser_navigate("https://qbo.intuit.com/app/standardreports")
2. browser_wait_for(time=3)
3. browser_evaluate com EXTRATOR 6 para encontrar links
4. browser_click no link de "Profit and Loss" ou "Balance Sheet"
   (link tera formato /app/report/builder?rptId=...&token=PANDL)
5. browser_wait_for(time=5)
6. browser_evaluate com EXTRATOR 2 (P&L) ou EXTRATOR 9 (BS)
DICA: Na PRIMEIRA visita a standardreports, extrair TODOS os hrefs
de reports e SALVAR mentalmente. Reutilizar nas proximas estacoes.

=== DETECCAO DE SESSAO EXPIRADA ===
Se browser_navigate redirecionar para accounts.intuit.com:
  → Sessao expirou. Ver REGRA #5B para recovery.
Se pagina retornar "We're sorry, we can't find the page":
  → Pode ser 404 (URL errada) OU sessao expirada.
  → Testar: navegar para /app/homepage primeiro.
  → Se homepage funciona → URL estava errada, usar mapa acima.
  → Se homepage TAMBEM falha → sessao expirou, fazer re-login.
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

**Categorizar Bank Transactions (D04 — PROTOCOLO OTIMIZADO):**
```
ANTES: ~14 tool calls por transacao (visto em sweep real)
AGORA: ~4 tool calls por transacao

PROTOCOLO PARA CADA TRANSACAO:
1. browser_evaluate com EXTRATOR 8 → ver transacoes pendentes
2. browser_click na DESCRIPTION CELL da transacao (NAO na vendor cell!)
   MOTIVO: clicar no vendor cell dispara AI Vendor Suggestion popover que bloqueia tudo
3. Esperar form expandir (browser_wait_for time=2)
4. browser_evaluate: () => {{
     const btns = [...document.querySelectorAll('button')];
     const post = btns.find(b => b.innerText?.trim() === 'Post' && b.offsetParent);
     if (post) {{ post.click(); return 'posted'; }}
     return 'no-post-btn';
   }}
5. browser_wait_for(time=2) — dialog "Post without class" VAI aparecer (100% das vezes)
6. browser_evaluate: () => {{
     const btns = [...document.querySelectorAll('button')];
     const pa = btns.find(b => b.innerText?.trim() === 'Post anyway');
     if (pa) {{ pa.click(); return 'confirmed'; }}
     return 'no-dialog';
   }}
7. PROXIMO: Rodar EXTRATOR 8 de novo (refs ficam stale apos post)

PARA 5 TRANSACOES: ~20 tool calls total (antes: ~70)

IMPORTANTE: Escolher transacoes com CATEGORIAS VARIADAS (nao 5x o mesmo account).
Buscar: Contract labor, Supplies, Insurance, Utilities, Taxes & Licenses, etc.
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

**Notas de contexto para enriquecimento (D05 customers, D06 vendors):**
```
{notes_for_sector}
```

### IES ROUTE CHEATSHEET (CONSULTAR ANTES DE CADA browser_navigate)

```
D01=/app/homepage  D02=standardreports>P&L  D03=standardreports>BS
D04=/app/banking?jobId=accounting  D05=/app/customers  D06=/app/vendors
D07=/app/employees?jobId=team  D08=/app/items  D09=/app/projects
D10=/app/standardreports  D11=/app/chartofaccounts?jobId=accounting
D12=Gear icon>Account and settings (NAO /app/company!)
Reports: SEMPRE via /app/standardreports > clicar link (nao tem URL direta)
404 CONFIRMADOS SEM ALT: paymentlinks, subscriptions, customformstyles, cashflow, expenseclaims
```

> **REGRA #6 — POS-COMPACTION RECOVERY**
> Se voce perdeu contexto (compaction aconteceu), ANTES de continuar:
> 1. Consultar este CHEATSHEET para rotas corretas
> 2. NAO inventar URLs curtos — usar EXATAMENTE a rota do header da estacao
> 3. Se em duvida, rodar: `Read(dashboard/pending/SWEEP_ORDER.md)` linhas 1-50 para re-ler rotas
> 4. Stations com `⚠IES:404` → marcar como ✗ e pular (nao navegar, economizar tempo)

## 4. SURFACE SCAN ({len(surface)} habilitados) — RAPIDO, SEM CORRECAO

{chr(10).join(surface_lines) if surface_lines else "Nenhum surface check habilitado."}

**Protocolo**: `browser_navigate` → `browser_wait_for(time=3)` → `browser_evaluate` com **EXTRATOR 4** → anotar ✓/○/✗/⚠ → proximo
- ✓ = tem dados | ○ = vazio | ✗ = 404 | ⚠ = placeholder/problema
- ⚠IES:404 = PULAR — 404 confirmado em IES, nao gastar tool calls

**OTIMIZACAO**: Agrupar 5-6 surface scans consecutivos, reportar em lote:
```
[S01-S06] ✓✓✓○✗✓ (S04 vazio, S05 404)
[S07-S12] ✓✓✓✓✓✗ (S12 404)
...
```

**SE USAR browser_run_code para batching:**
```
PROIBIDO: browser_run_code com Node.js context (require, fetch, etc.)
OBRIGATORIO: usar APENAS browser_evaluate com page.evaluate() context

Para batch de 5-6 URLs, faca um loop SEQUENCIAL:
  Para cada URL:
    1. browser_navigate(url)
    2. browser_wait_for(time=3)
    3. browser_evaluate com EXTRATOR 4
    4. Anotar resultado (OK/X/EMPTY)

NAO tente fazer batch em um unico browser_run_code.
browser_evaluate roda no CONTEXTO DA PAGINA (document, window).
browser_run_code roda no CONTEXTO NODE.JS (nao tem document!).

TRUNCAR TODOS os textos para 50 chars max.
Retornar APENAS status (OK/X/EMPTY) + snippet curto.
NAO retornar bodyText.substring(0, 300) — isso estoura o limite.

Se o resultado estourar o limite, NAO leia o arquivo salvo.
Refaca com snippets ainda menores (30 chars).
```

## 5. CONDITIONAL ({len(cond)} habilitados)

{chr(10).join(cond_lines) if cond_lines else "Nenhum conditional check habilitado."}

**BATCHING**: Fazer conditional checks em grupos de 3-4 (NAO todos de uma vez).
Checkpoint `CID:C_BATCH` somente quando TODOS os conditional checks estiverem feitos.
Se context compaction acontecer durante conditional: reler LATEST_SWEEP.json e continuar de onde parou.

## 5.1 CROSS-ENTITY VALIDATION (apenas multi-entity — rodar APOS todas entities individuais)

{"APLICAVEL — " + str(len(acct.companies)) + " entities detectadas. Executar APOS completar sweep de cada entity individual." if is_multi else "NAO APLICAVEL — entity unica, pular esta secao."}
{_build_cross_entity_block() if is_multi else ""}

## 5.2 REVALIDATION RULES (OBRIGATORIO apos cada fix)

Toda correcao aplicada DEVE ser revalidada ANTES de avancar para a proxima estacao:
- **RV01** — JE criado → voltar ao P&L e confirmar Net Income mudou. Se nao mudou, data do JE esta fora do periodo. Ajustar para 1o do mes atual.
- **RV02** — Nome renomeado → voltar a lista e confirmar novo nome aparece. Checar 1 transacao vinculada.
- **RV03** — Transacoes bancarias categorizadas → verificar que 'For Review' diminuiu. Checar 1 registro.
- **RV04** — Projeto criado/renomeado → navegar a /app/projects e confirmar existencia + detalhe abre.
- **RV05** — Campos enriquecidos (notes, terms, email, address) → voltar ao detalhe do record e confirmar campos persistiram.
- **RV06** — Periodo do report alterado → confirmar report agora mostra dados nao-zero. Se $0 com All Dates, e gap de dados real.

**REGRA**: Se a revalidacao FALHAR, NAO avance. Corrija primeiro.

## 6. CONTENT SAFETY (aplicar em TODAS as paginas)

{chr(10).join(safety_lines) if safety_lines else "Content safety desabilitado."}

**Se encontrar CS1 (profanity) ou CS4 (PII)**: PARAR e corrigir IMEDIATAMENTE.
**Se encontrar CS2 (placeholder como "Foo", "TBX")**: corrigir inline com nome realista.
**Se encontrar CS9 (spam/nonsense)**: corrigir inline — renomear keyboard mash, truncar strings absurdas.

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
CONTEXTO: [tipo empresa] ~$[X]M revenue, [N] entities, setor {acct.dataset}

--- ENTITY 1: [nome] (parent) ---
[D01] Dashboard ✓ Income $X | Drill: P&L widget links to report ✓
[D02] P&L ✓ Revenue $X, Net $Y, Margin Z% | Drill: 3 income sources ✓
[D04] Banking ✓ | ENRICHED: categorized 8 txns, created 2 bank rules
[D05] Customers ✓ | DRILL: 5/5 checked | ENRICHED: 4 notes added, terms varied
[D06] Vendors ✓ | DRILL: 5/5 checked | ENRICHED: 3 notes added
[D08] Products ✓ | DRILL: 5 checked | ENRICHED: 2 descriptions added
[D09] Projects ✓ | DRILL: 3 projects | ENRICHED: created 1 project
...
[D12] Settings ✓

--- SURFACE SCAN ({len(surface)} pages) ---
[S01-S06] ✓✓✓○✗✓
[S07-S12] ✓✓✓✓✓✗
[S13-S18] ✓✓✓✓○✓
[S19-S24] ✓✓✓✓✓✓
[S25-S{len(surface):02d}] ✓✓✓✓✓✓

--- CONDITIONAL ({len(cond)}) ---
[C01-C04] ✓✓✓✓
[C05-...] N/A N/A ...

→ Switching to Entity 2: [nome]...
--- ENTITY 2: [nome] (child) ---
[D01] Dashboard ✓ ...
[D02] P&L ✓ ...
[D05] Customers ✓ | DRILL: 3/3 checked | ENRICHED: 2 notes
[D06] Vendors ✓ | DRILL: 3/3 checked
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

**REGISTRAR FIXES APLICADOS** (OBRIGATORIO — evita duplicacao apos compaction):
Apos CADA fix (rename, email change, JE, etc.), registre no LATEST_SWEEP.json:
```bash
python -c "
import json; f='C:/Users/adm_r/Clients/intuit-boom/dashboard/pending/LATEST_SWEEP.json'
d=json.loads(open(f,encoding='utf-8').read())
p=d.get('progress',{{}})
fixes=p.get('fixes_applied',[])
fixes.append({{'entity':'customer','name':'Andrew Allen Test','station':'D05','action':'renamed to Andrew Callahan'}})
p['fixes_applied']=fixes
d['progress']=p
open(f,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=True))
"
```
**ANTES de aplicar qualquer fix**: checar se `fixes_applied` ja contem esse record.
Se ja contem → PULAR (ja foi corrigido). NAO editar de novo.

## 11. CHECKLIST PRE-REPORT (OBRIGATORIO)

```
ANTES de salvar o report, confirme TODOS os items abaixo.
Se algum esta faltando → VOLTE e complete antes de salvar.

COBERTURA:
- [ ] Parent: D01-D12 todos reportados individualmente com dados?
- [ ] Consolidated (se existir): D01+D02+D10+D11 verificados?
- [ ] CADA child: D01+D02+D05+D06 verificados INDIVIDUALMENTE?
      (NAO vale "same platform as Parent")

ENRICHMENT (v5.0):
- [ ] D04: categorizou 5+ bank transactions? (OBRIGATORIO)
- [ ] D05: fez drill-in em 3+ customers? Notes preenchidas com contexto do setor?
- [ ] D06: fez drill-in em 3+ vendors? Notes preenchidas com contexto?
- [ ] D08: top 5 products tem descriptions contextuais?
- [ ] D09: tem 3+ projects? Se nao, criou? Cada um com customer atribuido?

QUALITY:
- [ ] Content Safety: CS1-CS8 verificados em TODAS entities?
- [ ] Progress tracking: todas stations gravadas com CID:STATION?
- [ ] Pergunta final: "Um prospect acreditaria que esta e uma empresa real?"
```

{f"## 12. NOTAS{chr(10)}{chr(10)}{notes}" if notes else ""}

---
*Gerado em {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} pelo QBO Demo Manager Dashboard v5.6*
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

    # Build enabled check lists for SWEEP_ORDER generation
    checks = p.get("checks", {})
    deep = [s for s in DEEP_STATIONS if checks.get(s["id"], True)]
    surface = [s for s in SURFACE_SCAN if checks.get(s["id"], True)]
    cond = [s for s in CONDITIONAL_CHECKS if checks.get(s["id"], True)]

    # Generate SWEEP_ORDER.md — comprehensive instructions for new Claude session
    _generate_sweep_order_md(pending_dir, acct, p, profile, deep, surface, cond)

    # Launch Claude autonomously via batch file + start (reliable visible window)
    import os
    import subprocess as sp

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)  # Allow spawning Claude from within Claude sessions

    # Sanitize label for cmd.exe (strip parens and special chars)
    safe_label = "".join(c for c in acct.label if c.isalnum() or c in " -_.")
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

    # Build enabled check lists for SWEEP_ORDER generation
    checks = p.get("checks", {})
    deep = [s for s in DEEP_STATIONS if checks.get(s["id"], True)]
    surface = [s for s in SURFACE_SCAN if checks.get(s["id"], True)]
    cond = [s for s in CONDITIONAL_CHECKS if checks.get(s["id"], True)]

    # Regenerate SWEEP_ORDER.md with resume info
    _generate_sweep_order_md(pending_dir, acct, p, profile_key, deep, surface, cond, resume_from=progress)

    # Update status back to pending
    data["status"] = "pending"
    data["resumed_at"] = datetime.datetime.now().isoformat()

    # Sanitize label for cmd.exe
    safe_label = "".join(c for c in acct.label if c.isalnum() or c in " -_.")
    sweep_title = f"QBO Sweep - {safe_label}"

    # Write batch file
    bat_file = pending_dir / "run_sweep.bat"
    bat_file.write_text(
        f"@echo off\n"
        f"title {sweep_title}\n"
        f"cd /d {BASE.parent}\n"
        f'claude "Retomar sweep interrompido. Read dashboard/pending/SWEEP_ORDER.md and execute from where it left off. Use ONLY the credentials in SWEEP_ORDER.md."'
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

    uvicorn.run("app:app", host="127.0.0.1", port=8082, reload=True)
