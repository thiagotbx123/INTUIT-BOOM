"""Sweep order generation engine — produces compact SWEEP_ORDER.md.

v6.0 — Compact Architecture (2026-03-23)
Changes from v5.6:
- SWEEP_ORDER.md reduced from ~100KB to ~15KB
- JS extractors moved to dashboard/extractors/*.js (read on demand)
- Check details moved to dashboard/configs/checks.json (read per station)
- Sector expectations and fix protocols stay inline (small, frequently needed)
- All methodology rules preserved — only the DELIVERY FORMAT changed
"""

import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent


def get_sector_expectations(dataset: str) -> str:
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


def _build_resume_block(acct, resume_from: dict | None) -> str:
    """Build the resume header if resuming an interrupted sweep."""
    if not resume_from or not resume_from.get("completed_stations"):
        return ""

    done = resume_from["completed_stations"]
    entity = resume_from.get("current_entity", "")

    entity_progress = {}
    flat_stations = []
    for item in done:
        if ":" in item:
            cid, station = item.split(":", 1)
            entity_progress.setdefault(cid, []).append(station)
        else:
            flat_stations.append(item)

    resume_lines = []
    for c in acct.companies:
        cid = c.cid
        name = c.name
        stations_done = entity_progress.get(cid, [])
        if not stations_done:
            resume_lines.append(f">   - **{name}** (CID {cid}): NAO INICIADA — fazer sweep completo")
        elif "S_BATCH" in stations_done and "C_BATCH" in stations_done:
            resume_lines.append(f">   - **{name}** (CID {cid}): COMPLETA — PULAR")
        else:
            done_str = ", ".join(stations_done)
            resume_lines.append(f">   - **{name}** (CID {cid}): PARCIAL ({done_str}) — continuar do proximo")

    flat_note = ""
    if flat_stations:
        flat_note = f"\n> Formato antigo detectado. Stations sem entity: {', '.join(flat_stations)}"

    return f"""
> **RETOMADA DE SWEEP INTERROMPIDO**
> Ultima entity ativa: {entity}
>
> **STATUS POR ENTITY:**
{chr(10).join(resume_lines)}
{flat_note}
>
> **Comece pelo LOGIN e depois va direto para a primeira entity NAO COMPLETA.**
"""


def generate_sweep_order_md(pending_dir, acct, profile_data, profile_key, deep, surface, cond, resume_from=None):
    """Generate a compact SWEEP_ORDER.md (~15KB instead of ~100KB).

    Key change: check details and JS extractors are in separate files.
    Claude reads them on demand per station instead of loading everything upfront.
    """
    fix = profile_data.get("fix_tiers", {})
    safety = profile_data.get("content_safety", {})
    can_fix = fix.get("fix_immediately", True) or fix.get("fix_and_report", True)

    # Companies table
    companies_lines = []
    for c in acct.companies:
        companies_lines.append(f"| {c.name} | {c.cid} | {c.type} | {c.priority} |")

    is_multi = len(acct.companies) > 1

    # Deep station summary (ID + name + route — NO sub_checks/drill_in/fix_actions inline)
    deep_summary = []
    for s in deep:
        auto_tag = "FIX" if s.get("auto_fix") and can_fix else "REPORT"
        deep_summary.append(f"- **{s['id']}** {s['name']} → `{s['route']}` [{auto_tag}]")

    # Surface summary (compact)
    surface_summary = []
    for s in surface:
        ies_tag = " ⚠404" if s.get("ies_known_404") else ""
        surface_summary.append(f"- **{s['id']}** {s['name']} → `{s['route']}`{ies_tag}")

    # Conditional summary (compact)
    cond_summary = []
    for s in cond:
        cond_summary.append(f"- **{s['id']}** {s['name']} (if {s['condition']})")

    # Content safety (compact)
    from sweep_checks import CONTENT_SAFETY

    safety_lines = []
    for s in CONTENT_SAFETY:
        if safety.get(s["id"], True):
            safety_lines.append(f"- **{s['id']}** {s['name']}: `{s['pattern']}` [{s['severity']}]")

    # Fix tiers
    fix_desc = []
    if fix.get("fix_immediately", True):
        fix_desc.append("FIX IMMEDIATELY — corrigir sem perguntar")
    if fix.get("fix_and_report", True):
        fix_desc.append("FIX & REPORT — corrigir e documentar")

    notes = profile_data.get("notes", "") or ""

    # Entity switch block
    if is_multi:
        switch_block = """**Troca de entity**: `browser_navigate("https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={CID}")` → wait 5s → EXTRATOR E05
Fallback: header dropdown click. Consolidated: `?switchToConsolidated=true`"""
    else:
        switch_block = "**Entity unica** — sem necessidade de troca."

    resume_block = _build_resume_block(acct, resume_from)

    # Paths for reference files
    dashboard_path = str(BASE.as_posix())

    md = f"""# SWEEP ORDER — EXECUCAO IMEDIATA

> **ESTE DOCUMENTO + arquivos de referencia = TUDO que voce precisa.**
> NAO leia PROMPT_CLAUDE_QBO_MASTER.md, TESTBOX_ACCOUNTS.md, ou QBO_CREDENTIALS.json.
{resume_block}

---

## CHECKPOINT (executar ANTES de qualquer acao)

```bash
python -c "import json; d=json.loads(open('{dashboard_path}/pending/LATEST_SWEEP.json',encoding='utf-8').read()); p=d.get('progress',{{}}); print('COMPLETED:', p.get('completed_stations',[])); print('FIXES:', p.get('fixes_applied',[])); print('ENTITY:', p.get('current_entity','none'))"
```
Se completed_stations contem `CID:DXX` → PULAR essa station nessa entity.
Se fixes_applied contem um record → NAO editar de novo.

---

## ARQUIVOS DE REFERENCIA (ler sob demanda, NAO tudo de uma vez)

| Arquivo | O que contem | Quando ler |
|---------|-------------|------------|
| `{dashboard_path}/configs/checks.json` | Detalhes de TODOS checks (sub_checks, drill_in, fix_actions, cross_refs) | Ao chegar em cada Deep Station: `Read(path, offset=X)` para o check especifico |
| `{dashboard_path}/extractors/index.json` | Mapa de extractors E01-E10 | Uma vez no inicio |
| `{dashboard_path}/extractors/e01_dashboard.js` | JS para D01 | Ao chegar em D01 |
| `{dashboard_path}/extractors/e02_pnl.js` | JS para D02 | Ao chegar em D02 |
| ... (e03-e10 seguem o mesmo padrao) | | |

**COMO USAR**: Ao chegar em D05 (Customers), faca:
1. `Read("{dashboard_path}/extractors/e03_entity_list.js")` → copiar JS
2. Para sub_checks/drill_in: `Read("{dashboard_path}/configs/checks.json")` e buscar `"id": "D05"`
3. Executar a station usando as instrucoes lidas

---

## REGRAS CORE (memorizar)

**REGRA #1 — ANALISTA, NAO CHECKLIST BOT**
VER → DRILL-IN (top 3-5 records) → CORRIGIR → ENRIQUECER → AVANCAR
100% autonomo. Sem screenshots. Sem relatorio intermediario. 1 linha por station no chat.

**REGRA #2 — TOKEN MANAGEMENT**
- NUNCA retornar innerText > 500 chars
- NUNCA ler output de browser_navigate (13K+ tokens)
- Apos navigate: IMEDIATAMENTE browser_evaluate com extrator JS
- Se estourar: refazer com extrator menor. NAO ler arquivo salvo.

**REGRA #3 — ANTI-SKIP**
Cada Deep Station DEVE ter report: `[D01] ✓ Net $292K | Income $256K`
Se corrigiu: `[D02] CORRIGIDO: JE $200K, Net agora +$285K`
Se bloqueado: `[D07] BLOQUEADO: 2FA exigido`

**REGRA #4 — COBERTURA POR ENTITY**
- Parent: D01-D12 completo + Surface + Conditional
- Child: MINIMO D01+D02+D05+D06 individual
- Consolidated: D01+D02+D10+D11 + C01-C04

**REGRA #5 — ANTI-LOOP**
Se falhar 2x no mesmo item → documentar e avancar. NAO entrar em loop.

**REGRA #5B — SESSION KEEPALIVE**
A cada 15min: navigate homepage + extrator E01 para confirmar sessao.
Se redirecionar para accounts.intuit.com → re-login (max 3 tentativas).

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
0. `browser_navigate("https://accounts.intuit.com/app/sign-in")` → limpar cookies (JS)
1. `browser_snapshot` → ver form
2. `browser_type` email → next → password → sign in
3. TOTP: `python -c "import pyotp,time; t=pyotp.TOTP('{acct.totp_secret}'); r=30-int(time.time())%30; time.sleep(r+1) if r<10 else None; print(t.now())"`
4. `browser_type` codigo → submit
5. Skip prompts (passkey, 2FA) se aparecer
6. `browser_evaluate` com E01 para confirmar QBO homepage

**Use APENAS Playwright (browser_*). NAO use QuickBooks MCP API.**

## 2. ENTITIES ({len(acct.companies)})

| Nome | CID | Tipo | Prioridade |
|------|-----|------|------------|
{chr(10).join(companies_lines)}

Ordem: P0 primeiro (Deep+Surface+Conditional), depois P1 (D01+D02 rapido).
{switch_block}

## FASE ZERO — CONTEXTO DO NEGOCIO

Apos login, rodar E01 no homepage. Formular: "Esta e uma [tipo] com ~$[X]M revenue, setor {acct.dataset}."

**SETOR: {acct.dataset}**
{get_sector_expectations(acct.dataset)}

---

## 3. DEEP STATIONS ({len(deep)} habilitados)

{chr(10).join(deep_summary)}

**Para CADA station**: Read o extrator JS correspondente → Read checks.json para sub_checks/drill_in → executar → report 1 linha.

### IES ROUTE CHEATSHEET
```
D01=/app/homepage  D02=standardreports>P&L  D03=standardreports>BS
D04=/app/banking?jobId=accounting  D05=/app/customers  D06=/app/vendors
D07=/app/employees?jobId=team  D08=/app/items  D09=/app/projects
D10=/app/standardreports  D11=/app/chartofaccounts?jobId=accounting
D12=Gear icon>Account and settings
Reports: SEMPRE via /app/standardreports > clicar link
404 CONFIRMADOS: paymentlinks, subscriptions, customformstyles, cashflow, expenseclaims
```

### FIX PROTOCOLS (referencia rapida)

**JE para P&L negativo**: /app/journal → DR AR $200K / CR Revenue $200K → memo realista → Save → re-check P&L. Data: 1o do mes atual.
**Categorizar Bank Txns**: /app/banking → E08 → click DESCRIPTION cell (NAO vendor!) → Post → "Post anyway" → E08 novamente. ~4 calls/txn.
**Renomear placeholder**: click record → Edit → novo nome realista → Save.
**Pagar bills antigos (AP fix)**: /app/bills → sort oldest → Mark as paid (data = 3-7 dias apos due date, checking account). NAO pagar todos — manter 20-40% abertos.

---

## 4. SURFACE SCAN ({len(surface)} habilitados)

{chr(10).join(surface_summary)}

**Protocolo**: navigate → wait 3s → E04 ou E10 → anotar ✓/○/✗/⚠
Agrupar em lotes: `[S01-S06] ✓✓✓○✗✓`

## 5. CONDITIONAL ({len(cond)} habilitados)

{chr(10).join(cond_summary)}

{"## 5.1 CROSS-ENTITY (rodar APOS todas entities)" if is_multi else ""}
{"Para detalhes: Read checks.json secao cross_entity_checks" if is_multi else ""}

## 6. CONTENT SAFETY

{chr(10).join(safety_lines)}

CS1 (profanity) ou CS4 (PII): PARAR e corrigir IMEDIATAMENTE.
CS2 (placeholder): corrigir inline com nome realista.

## 7. FIX RULES

{chr(10).join(fix_desc)}
Corrigir: placeholders, campos vazios, P&L negativo, nomes genericos, bank txns.
NUNCA: company settings, employee edits com 2FA, feature flags, payroll, deletes.

## 8. REALISM SCORING

{"HABILITADO — pontuar 10 criterios de 1-10 ao final." if profile_data.get("realism_scoring", True) else "DESABILITADO"}

## 9. OUTPUT

```
Logado em {acct.label} → [nome empresa]
CONTEXTO: [tipo] ~$[X]M revenue, {len(acct.companies)} entities, {acct.dataset}

--- ENTITY 1: [nome] (parent) ---
[D01] Dashboard ✓ Income $X | Bank $Y
[D02] P&L ✓ Revenue $X, Net $Y, Margin Z%
...
--- SURFACE ({len(surface)} pages) ---
[S01-S06] ✓✓✓○✗✓
...
```

Report: `C:/Users/adm_r/Clients/intuit-boom/knowledge-base/sweep-learnings/{{shortcode}}_YYYY-MM-DD.md`
Ao terminar: LATEST_SWEEP.json status → "completed" + overall_score + realism_score.

## 10. PROGRESS TRACKING (OBRIGATORIO)

Apos CADA Deep Station, atualizar LATEST_SWEEP.json:
```bash
python -c "
import json; f='{dashboard_path}/pending/LATEST_SWEEP.json'
d=json.loads(open(f,encoding='utf-8').read())
p=d.get('progress',{{}})
done=p.get('completed_stations',[])
done.append('CID:STATION_ID')
p['completed_stations']=done
p['current_entity']='ENTITY_NAME (CID)'
p['last_update']=__import__('datetime').datetime.now().isoformat()
d['progress']=p
open(f,'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=True))
"
```

Registrar fixes: `fixes_applied.append({{"entity":"X","name":"Y","station":"DXX","action":"Z"}})`
ANTES de fixar: checar se ja esta em fixes_applied → se sim, PULAR.

{f"## NOTAS{chr(10)}{notes}" if notes else ""}

---
*Gerado em {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} pelo QBO Demo Manager v6.0 (Compact)*
"""

    order_file = pending_dir / "SWEEP_ORDER.md"
    order_file.write_text(md.strip(), encoding="utf-8")
