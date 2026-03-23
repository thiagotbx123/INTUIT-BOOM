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

**REGRA #0 — AUTONOMIA TOTAL (MAIS IMPORTANTE QUE TODAS AS OUTRAS)**
Este sweep e 100% AUTONOMO do inicio ao fim.
- NUNCA perguntar "Want me to continue?", "Shall I proceed?", "Do you want me to..."
- NUNCA parar entre entities para pedir confirmacao ou reportar progresso parcial
- NUNCA inventar "time constraint" como desculpa para pular checks
- NUNCA agrupar stations em bloco ("D16-D25 ✓ accessible") — CADA station INDIVIDUAL
- TODAS as entities (P0 + P1 + Consolidated) DEVEM ser processadas em sequencia
- O sweep SO PARA quando: (1) TODAS entities processadas, (2) login falhou 3x, ou (3) browser crashou
- Se ficou em duvida: DOCUMENTAR e CONTINUAR. Nunca pausar.
- Se um fix falhou: RETENTAR 1x. Se falhar de novo: documentar e avancar (REGRA #5).

**REGRA #2 — TOKEN MANAGEMENT**
- NUNCA retornar innerText > 500 chars
- NUNCA ler output de browser_navigate (13K+ tokens)
- Apos navigate: IMEDIATAMENTE browser_evaluate com extrator JS
- Se estourar: refazer com extrator menor. NAO ler arquivo salvo.

**REGRA #3 — ANTI-SKIP (TOLERANCIA ZERO)**
Cada Deep Station DEVE ter report INDIVIDUAL com dados reais:
  `[D01] ✓ Net $292K | Income $256K`
  `[D02] CORRIGIDO: JE $200K, Net agora +$285K`
  `[D07] BLOQUEADO: 2FA exigido`
  `[D16] ✓ 6 fixed assets, depreciation SL, net book $430K`
PROIBIDO agrupar stations: `[D16-D25] ✓` e FRAUDE. Cada D tem que ter SUA linha.
Se a station nao tem dados (ex: RevRec vazio): `[D17] N/A — modulo sem dados`
Se 404: `[D16] 404 — tentei /app/fixed-assets?jobId=accounting, fallback sidebar`

**REGRA #4 — COBERTURA POR ENTITY (PROCESSAR TODAS SEM PARAR)**
MINIMO OBRIGATORIO:
- P0 (Parent): D01-D25 TODOS + Surface TODAS 46 + Conditional aplicaveis
- P0 (Top 2 children): D01-D25 TODOS + Surface
- P1 (Demais children): D01+D02+D05+D06 (rapido mas INDIVIDUAL)
- Consolidated (se existir): D01+D02+D10+D11 + C01-C04
ORDEM: Parent → Child 1 → Child 2 → Consolidated → P1 children (rapido)
IMPORTANTE: NAO existe "time constraint". Execute TUDO.
Se o context window estiver grande: use /compact e continue. NAO pare.

**REGRA #5 — ANTI-LOOP**
Se falhar 2x no mesmo item → documentar e avancar. NAO entrar em loop.
Se um fix falhou 1x → RETENTAR 1x com abordagem diferente. Se falhar de novo → documentar.

**REGRA #5B — SESSION KEEPALIVE**
A cada 15min: navigate homepage + extrator E01 para confirmar sessao.
Se redirecionar para accounts.intuit.com → re-login (max 3 tentativas).

**REGRA #6 — CORRECAO OBRIGATORIA (FIX, NAO APENAS REPORT)**
Findings de CS2 (placeholder) e CS3 (test names): CORRIGIR IMEDIATAMENTE, nao apenas anotar.
- Vendor "test jones" → Edit → renomear para nome realista do setor → Save
- Project "Test Delete" → Edit → renomear para nome de projeto real → Save
- Estimate "#1" → Edit → dar titulo descritivo → Save
Se ENCONTROU um problema fixavel (tier fix_immediately): CORRIJA antes de avancar.
Sweep que DETECTA mas NAO CORRIGE e inutil — qualquer um pode ler uma tela.
O VALOR do sweep e CORRIGIR, nao listar.

**REGRA #7 — QUALIDADE DO REPORT**
O report final (MD) DEVE ter no header EXATAMENTE:
```
Overall Score: X.X/10
Realism Score: YY/100
```
Sem esses campos o dashboard NAO parseia o score e aparece "--" na UI.
NUNCA usar "Realism Score" sozinho no header — SEMPRE incluir "Overall Score: X/10".

**REGRA #8 — PROFUNDIDADE OBRIGATORIA (DRILL INTO GOD)**
O CHAT mostra 1 linha por station (progresso rapido durante execucao).
O REPORT MD mostra o DEPTH PROTOCOL completo (secao 8.5 abaixo).
Um one-liner "[D05] ✓ 70 customers" NO REPORT e FRAUDE — isso so serve pro chat.
CHAT = indicador de progresso. REPORT = analise profunda com metricas, records, cross-refs.
Para cada D station no REPORT: seguir o template e MINIMOS da tabela na secao 8.5.
Se o station tem dados: MINIMO 8 linhas com metricas, top records nomeados, e cross-reference.
Se o station e N/A ou vazio: 1 linha com razao e suficiente.

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

**ORDEM OBRIGATORIA (SEM PULAR NENHUMA ETAPA):**
1. P0 Parent: D01-D25 completo + Surface 46 pages + Conditional
2. P0 Child 1: D01-D25 completo + Surface
3. P0 Child 2: D01-D25 completo + Surface
4. Consolidated View (se existir): D01+D02+D10+D11 + C01-C04
5. P1 Children (rapido): D01+D02+D05+D06 para CADA um individualmente
NAO existe "time constraint". Execute TUDO. Se context grande: /compact e continue.
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
CS2 (placeholder): CORRIGIR INLINE — Edit → nome realista → Save. NAO apenas anotar.
CS3 (test names): CORRIGIR INLINE — "test jones" → "Johnson & Associates". NAO deixar pra report.
DETECTAR sem CORRIGIR e INACEITAVEL. O valor do sweep e a correcao, nao a lista de problemas.

## 7. FIX RULES

{chr(10).join(fix_desc)}
Corrigir: placeholders, campos vazios, P&L negativo, nomes genericos, bank txns.
NUNCA: company settings, employee edits com 2FA, feature flags, payroll, deletes.

## 8. REALISM SCORING

{"HABILITADO — pontuar 10 criterios de 1-10 ao final." if profile_data.get("realism_scoring", True) else "DESABILITADO"}

## 8.5 DEPTH PROTOCOL — FORMATO OBRIGATORIO DO REPORT

O REPORT MD (arquivo salvo) DEVE seguir este protocolo. One-liners sao para o CHAT, nao para o report.

### TEMPLATE POR DEEP STATION (copiar para cada D):
```
### DXX — [Name] — Score: X/10

**Metrics:**
| Metric | Value |
|--------|-------|
| [primary count] | [number] |
| [primary dollar] | [$amount] |
| [sector KPI] | [value] |

**Top Records (drill-in):**
1. **[Name]** — [metric], fields: [complete/gaps], [action if any]
2. **[Name]** — [metric], fields: [complete/gaps]
3. **[Name]** — [metric], fields: [complete/gaps]

**Cross-Ref:** [DXX vs DYY]: [match/mismatch + numbers]
**Findings:** [P1/P2 with names and amounts, or CLEAN]
**Fixes:** [action + before→after verified, or NONE]
```

### MINIMOS POR STATION (OBRIGATORIO):

| Station | Min Records Nomeados | Min Metricas | Cross-Ref | KPI Obrigatorio |
|---------|---------------------|-------------|-----------|-----------------|
| D01 Dashboard | 0 (widgets) | 4 (Income,Expense,Net,Bank) | D02 | Data recency (dias) |
| D02 P&L | 3 (top revenue lines) | 5 (Rev,COGS,Gross,Net,Margin%) | D01,D03,D08 | Margin % |
| D03 BS | 3 (top balance accounts) | 4 (Assets,Liab,Equity,AR) | D02,D04 | A=L+E check |
| D04 Banking | 3 (bank accounts) | 4 (QBbal,Bankbal,Pending,Cat%) | D03 | Categorized % |
| D05 Customers | 5 (top by AR, com nome) | 5 (Count,AR,Top5,Overdue,DSO) | D03 | DSO (dias) |
| D06 Vendors | 5 (top by AP, com nome) | 5 (Count,AP,Aging,Overdue%,Conc%) | D02,D03 | Concentration % |
| D07 Employees | 3 (nomes + cargo) | 3 (Count,AvgSalary,OverdueFilings) | D02 | Payroll/Rev % |
| D08 Products | 5 (top por volume) | 4 (Count,AvgPrice,Margin%,DescFill%) | D02 | Avg margin % |
| D09 Projects | 3 (com Income/Cost/Margin) | 4 (Count,TotalValue,AvgMargin,Status) | D02,D05 | Budget vs Actual |
| D10 Reports | 0 (lista) | 3 (ReportsAvailable,Core4,KPI) | D02,D03 | P&L by Class? |
| D11 COA | 3 (sample accounts) | 3 (Total,HierarchyOK?,Orphans) | D02,D03 | Classification % |
| D12 Settings | 0 (config) | 5 (Industry,Address,Phone,Legal,EIN) | D05,D06 | Completeness % |
| D13 Estimates | 3 (com valor + status) | 4 (Count,Conversion%,AvgAmt,Expiry) | D05 | Conversion % |
| D14 POs | 2 (com vendor + valor) | 3 (Count,POBillLink%,StatusDist) | D06,D08 | Linkage % |
| D15 Recurring | 2 (com tipo + interval) | 3 (Count,TypeDiversity,NextDate) | D05,D06 | Active % |
| D16 Fixed Assets | 2 (com valor + method) | 3 (Count,TotalNBV,DeprecRunning?) | D03 | NBV vs BS |
| D17 RevRec | 1 (schedule) | 2 (Count,DeferredBal) | D02,D03 | Recognized % |
| D18 Time | 3 (entries com employee) | 4 (Count,EmpCoverage%,Billable%,Hrs) | D07,D09 | Billable % |
| D19 Tax | 0 (config) | 3 (Agencies,FilingFreq,Overdue) | D05,D08 | Taxable item % |
| D20 Budgets | 1 (budget detail) | 3 (Exists?,BvARange,Period) | D02 | BvA populated? |
| D21 Dimensions | 3 (classes com txn count) | 3 (ClassCount,TxnCoverage%,Orphan%) | D02 | P&L by Class? |
| D22 Workflows | 2 (com trigger + status) | 3 (Count,Active%,ExecHistory?) | D05 | Execution count |
| D23 Custom Fields | 2 (com tipo + form) | 3 (Count,TypeVariety,Population%) | D05 | Population % |
| D24 Reconciliation | 2 (rules com pattern) | 3 (RuleCount,LastReconcile,Coverage%) | D04,D06 | Reconciled? |
| D25 AI | 0 (features) | 3 (Assist?,AICategorization?,Summary?) | D01,D04 | Insight count |

### PROFUNDIDADE POR TIER DE ENTITY:
- **P0 Parent**: 15-25 linhas por D station (FULL depth — metricas + records nomeados + cross-ref + findings)
- **P0 Children (top 2)**: 8-12 linhas por D station (D01-D12 completo, D13-D25 se relevante)
- **P1 Children**: 3-5 linhas por station (D01+D02+D05+D06 apenas — rapido mas com metricas)
- **Consolidated**: 8-12 linhas (D01+D02+D10+D11 + C01-C04 cross-entity)
- **Se N/A ou vazio**: 1 linha com razao ("D17 — RevRec — N/A: modulo sem dados/nao provisionado")

---

## 9. OUTPUT

### 9.1 CHAT (durante execucao — progresso rapido)
```
[D01] ✓ Income $375K | Net $153K | Bank $82M
[D02] CORRIGIDO: JE $75K → Net agora +$20K (margin 5.4%)
[D05] ✓ 70 customers | Top: Ali Khan $289K | DSO 45d
```

### 9.2 REPORT MD (arquivo salvo — DEPTH PROTOCOL COMPLETO)

**HEADER OBRIGATORIO (dashboard parser depende destes campos EXATAMENTE assim):**
```
# SWEEP REPORT — [LABEL]
**Date:** YYYY-MM-DD
**Overall Score:** X.X/10
**Realism Score:** YY/100
**Status:** PASS|FAIL
**Fixes Applied:** N
**Entities:** N
**Profile:** [profile name]
**Account:** [email]
**Dataset:** [dataset]
```
⚠ "**Overall Score:**" DEVE estar EXATAMENTE nesse formato ou o dashboard mostra "--"

**EXEMPLO D01 (NIVEL ESPERADO — parent P0):**
```
### D01 — Dashboard & First Impression — Score: 8/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Income Widget | $375K |
| Expense Widget | $222K |
| Net Income | $153K (margin 40.8%) |
| Bank Balance | $82.4M (AR inflation from prior cycle) |
| Data Recency | Current month ✓ |
| AI Agent Presence | Finance AI active, 3 monthly summaries |

**Widget Drill-In:**
- P&L widget → clicked, drills to full P&L report ✓, numbers match
- Invoice widget → 12 unpaid ($186K), 5 overdue ($53K)
- Business Feed → 3 AI tiles (Jan/Feb/Mar summaries), newest 3 days old ✓

**Cross-Ref:** D02 P&L report shows same $153K Net ✓
**Findings:** CLEAN
**Fixes:** NONE
```

**EXEMPLO D05 (NIVEL ESPERADO — parent P0):**
```
### D05 — Customers & AR — Score: 7/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Total Customers | 70 |
| AR Total | $4.38M |
| Overdue Invoices | 12 ($186K) |
| DSO | 45 days |
| Top Concentration | Ali Khan = 6.6% of AR |

**Top 5 Customers (by AR):**
1. **Ali Khan / Beacon Investments** — $289K AR, email ✓, address ✓, phone ✗, notes ✗ → ENRICHED (added phone + notes)
2. **Sophia Chang / Chang Design** — $177K AR, all fields ✓
3. **National Guard Bureau** — $142K AR, email ✗ (govt entity), address ✓
4. **Metro Dev Corp** — $98K AR, all fields ✓
5. **Riverside Holdings** — $76K AR, notes ✗ → ENRICHED (added notes)

**Invoice Sample (1 random):**
- INV-2026-0412: Ali Khan, $28,500, 3 line items (Framing $15K, Electrical $8.5K, Materials $5K), Paid ✓, payment linked ✓

**Cross-Ref:** AR $4.38M vs BS AR line (D03) = $4.38M ✓ match
**Content Safety:** CS3: "12345 Auction" → FIXED: renamed to "Harbor Point Estates"
**Findings:**
- P2: 3/70 customers missing phone (4%)
- P2: 1 placeholder name fixed (12345 Auction)
**Fixes:** Enriched Ali Khan (phone+notes), Riverside (notes), renamed 12345 Auction
```

**MESMO NIVEL DE PROFUNDIDADE para D02-D25 (seguir template + minimos da tabela 8.5)**

### TABELA-RESUMO POR ENTITY (OBRIGATORIA — parser do dashboard precisa):

Ao FINAL de cada entity, incluir tabela compacta:
```
| Station | Status | Key Metric |
|---------|--------|------------|
| D01 | ✓ | Net $153K |
| D02 | ✓ | Margin 54% |
| D03 | ✓ | A=L+E balanced |
| D04 | ✓ | 85% categorized |
| D05 | ✓ | 70 customers, DSO 45d |
| D06 | ⚠ | AP $1M, concentration 22% |
...D07-D25...
```
Esta tabela e a que o dashboard le para contabilizar stations PASS/FAIL.

### SECOES OBRIGATORIAS DO REPORT (apos todas entities):

1. **## P1 FINDINGS** — Lista priorizada (P1/P2/P3) com entity, station, nome, valor, acao
2. **## CONTENT SAFETY** — Tabela CS1-CS9: violations found, fixed, remaining
3. **## FIXES APPLIED** — Tabela: Station | Entity | Before | After | Verified?
4. **## CROSS-ENTITY COMPARISON** (se multi-entity) — Matriz com metricas por entity
5. **## REALISM SCORING** — 10 criterios com score e evidencia
6. **## SESSION METADATA** — Data, duracao, versao, stations auditados, entities processados

Report path: `{dashboard_path}/../knowledge-base/sweep-learnings/{{shortcode}}_YYYY-MM-DD.md`
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
