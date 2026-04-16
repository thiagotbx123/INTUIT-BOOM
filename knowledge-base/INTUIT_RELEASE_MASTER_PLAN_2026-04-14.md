# INTUIT QBO RELEASE MASTER PLAN — FY26 Completo v3.0
**Reconstruído:** 2026-04-14 | **Autor:** Thiago Rodrigues + Claude
**Método:** Extração programática do Excel + triangulação com 6 fontes

---

## CADEIA DE RELEASES

```
FALL 2025        WINTER FY26       FEB FY26          MAY FY26
(Nov 20)         (Feb 4)           (Feb+)            (May 13)
    │                │                │                  │
 ENTREGUE         ENTREGUE         ENTREGUE         EM PREPARAÇÃO
 100% PASS        28/29 PASS       Validado         53 features
                  1 follow-up      (extensão)       52 ativas
```

---

## 1. FALL RELEASE 2025

**GA:** 2025-11-20 | **Status:** ENTREGUE — 100% PASS
**Ambientes:** TCO + Construction (full), Manufacturing/Non-Profit (~95%)
**Fonte:** fall_release_catalog.md + PLAYBOOK appendix + SOW

| # | Feature | Tipo | Status |
|---|---------|------|--------|
| 1 | Payments Agent | AI | PASS |
| 2 | Finance Agent | AI | PASS |
| 3 | Accounting Agent | AI | PASS |
| 4 | Project Management Agent | AI | PASS |
| 5 | Certified Payroll | Construction | PASS |
| 6 | Shared Chart of Accounts | Multi-Entity | PASS |
| 7 | Dimension Assignment | Dimensions | PASS |
| 8 | Intercompany Sales Enforcement | Multi-Entity | PASS |
| 9 | Intercompany Cost Allocations | Multi-Entity | PASS |
| 10 | KPI Library | Reporting | PASS |
| 11 | Custom KPIs | Reporting | PASS |
| 12 | Dashboard Enhancements | Reporting | PASS |
| 13 | AR Aging Summary | Reporting | PASS |
| 14 | Formatting Changes in Reports | Reporting | PASS |
| 15 | Quarterly Reporting Package | Reporting | PASS |
| 16 | Bill Payment Approval Workflow | Workflow | PASS |
| 17 | Instant Payments | Payments | PASS (limited) |
| 18 | Payroll Performance Enhancements | Payroll | PASS |
| 19 | Payroll Correction Consolidation | Payroll | PASS |

**Confiança:** ALTA. **Lição:** Pre-build data before flags funciona. ~58% do Winter veio do Fall (reuse).

---

## 2. WINTER RELEASE FY26

**Early Access:** 2026-02-04 | **Status:** ENTREGUE — 28/29 PASS, 1 follow-up (WR-016)
**Ambientes validados:** 6/8
**Fonte:** WINTER_RELEASE_EXECUTIVE_REPORT.md + DEEP_ANALYSIS_REPORT.md

| WR-ID | Feature | Categoria | Status |
|-------|---------|-----------|--------|
| WR-001 | Accounting AI | AI Agents | PASS |
| WR-002 | Sales Tax AI (Pre-file) | AI Agents | PASS |
| WR-003 | Project Management AI | AI Agents | PASS |
| WR-004 | Finance AI | AI Agents | PASS |
| WR-005 | Solutions Specialist | AI Agents | PASS |
| WR-006 | Customer Agent | AI Agents | PASS |
| WR-007 | Omni/Intuit Intelligence | AI Agents | PASS |
| WR-008 | Conversational BI | AI Agents | PASS |
| WR-009 | KPIs Customizados | Reporting | PASS |
| WR-010 | Dashboards | Reporting | PASS |
| WR-011 | 3P Data Integrations | Reporting | PASS (404 Construction) |
| WR-012 | Calculated Fields | Reporting | PASS |
| WR-013 | Management Reports | Reporting | PASS |
| WR-014 | Benchmarking | Reporting | PASS |
| WR-015 | Multi-Entity Reports | Reporting | PASS |
| WR-016 | Dimension Assignment v2 | Dimensions | FOLLOW-UP |
| WR-017 | Hierarchical Dimension Reporting | Dimensions | PASS |
| WR-018 | Dimensions on Workflow | Dimensions | PASS (404 Construction) |
| WR-019 | Dimensions on Balance Sheet | Dimensions | PASS |
| WR-020 | Parallel Approval | Workflow | PASS (404 Construction) |
| WR-021 | Seamless Desktop Migration | Migration | PASS |
| WR-022 | DFY Migration Experience | Migration | PASS |
| WR-023 | Feature Compatibility | Migration | PASS |
| WR-024 | Certified Payroll Report | Construction | PASS |
| WR-025 | Sales Order | Construction | PASS |
| WR-026 | Multi-Entity Payroll Hub | Payroll | PASS |
| WR-027 | Garnishments - Child Support | Payroll | PASS |
| WR-028 | Assignments in QBTime | Payroll | PASS |
| WR-029 | Enhanced Amendments (CA) | Payroll | PASS |

**Confiança:** ALTA. **Gaps herdados:** WR-011/018/020 = 404 em Construction.

---

## 3. FEBRUARY RELEASE FY26

**Tema:** Conversational BI / Intuit Intelligence
**Status:** Validado como parte do Winter (features overlapping)
**Fonte:** IES_FEBRUARY_RELEASE_FY26_ANALISE_CRITICA.md

Features adicionais vs Winter:
- Conversational BI com 3P data
- Intuit Benchmarks exclusivos
- IAS (Intuit Accountant Suite)
- AI Ready to Post batch
- Sales Tax Pre-file Check
- Budget creation IES

**Confiança:** MÉDIA — sem tracker PASS/FAIL separado. Scope esteve "in flux" (Casey Roeder).

---

## 4. MAY RELEASE FY26

**GA:** May 13, 2026 | **Seller Ready:** May 15 (target)
**Total:** 53 features (52 ativas + 1 descoped)
**Fontes:** Excel v4.0 (canônico) + WIS Analysis + May Release Plan DRAFT + WFS Scoping + Bank Linking Research

### Números do Ground Truth (extração programática do Excel)

| Metric | Valor |
|--------|-------|
| Total | 53 |
| Active | 52 (51 Not Started + 1 On Hold) |
| Descoped | 1 (MR-014) |
| OOTB Yes | 48 |
| OOTB No | 3 (MR-020, MR-021, MR-053) |
| OOTB N/A | 1 (MR-036) |
| Click path PRESENT (active) | 31 |
| Click path MISSING (active) | 20 |
| Click path N/A (active) | 1 (MR-043) |
| Data Prep YES | 3 (MR-020, MR-021, MR-053) |
| Effort (active) | 20S + 25M + 6L + 1TBD |

### Risk Scorecard

| Grupo | Tot | GREEN | YELLOW | RED | D/H |
|-------|-----|-------|--------|-----|-----|
| Multi-Entity | 10 | 5 | 5 | 0 | 0 |
| Reporting | 4 | 2 | 1 | 0 | 1 |
| Dimensions | 5 | 2 | 3 | 0 | 0 |
| AI | 3 | 0 | 1 | 1 | 1 |
| Payments/Workflow | 3 | 1 | 2 | 0 | 0 |
| WFS/HR | 12 | 0 | 10 | 2 | 0 |
| Payroll | 5 | 1 | 2 | 2 | 0 |
| Construction | 8 | 2 | 6 | 0 | 0 |
| Manufacturing | 3 | 0 | 3 | 0 | 0 |
| **TOTAL** | **53** | **13** | **33** | **5** | **2** |

**Detalhes por feature:** ver `OUTPUT_MAY_RELEASE_TRACKER.md`

---

## 5. BLOCKERS ATIVOS (CROSS-RELEASE)

| # | Blocker | Ticket | Owner | Impact | Status |
|---|---------|--------|-------|--------|--------|
| B1 | Payroll bank verification stuck | PLA-3431 | Augusto | WFS payroll, bill pay, tax e-filing | Payments app submitted 04/14, awaiting Risk Ops |
| B2 | Cash flow invoices gate 2 | PLA-3416 | Augusto | QBO cash flow feature | Confusion on Retool process |
| B3 | Scope not locked | — | Intuit | All May features | Apr 17 deadline |
| B4 | 21 click paths missing | — | Intuit PMs | WFS+Payroll+Construction | 14/21 são WFS+Payroll |
| B5 | Feature flags not in UAT | — | Intuit (Siji replacement?) | Blocks Phase 2 | Code lock ~Apr 10, flags ~Apr 30 |
| B6 | Health check reports ~50% accurate | — | Augusto | False positives | Calibrating |
| B7 | QSP 2FA blocked | — | — | 2 entities inaccessible | No fix path |
| B8 | Manufacturing tenant undefined | — | TestBox | MR-050 | Carry-over from Feb |
| B9 | WFS data migration | — | Rama (Intuit) | GoCo features | "Once migrated works" — no ETA |
| B10 | PM coverage gap | — | Donna Seapoe | Release coordination | Christina→Donna unconfirmed |

---

## 6. TIMELINE DO MAY RELEASE (May Plan DRAFT Apr 9)

| Fase | Período | Status |
|------|---------|--------|
| Phase 1: Pre-Build | Apr 8-10 | Code lock pendente (era Apr 10) |
| Phase 2: Feature Access + Data Build | Apr 10-30 | Not started |
| Phase 3: UAT Validation | May 1-9 | Not started |
| Phase 4: Production Rollout | May 13-15 | Not started |
| WFS Parallel Track | Contínuo | 6 perguntas Rama pendentes |

---

## 7. OWNERSHIP MAP

| Pessoa | Responsabilidade | Load |
|--------|-----------------|------|
| **Alexandra** | Primary TSA — feature validation, data build, WFS lead | HEAVY |
| **Thiago** | Sweep system, infra, coordination, Construction, Manufacturing, blockers | HEAVY |
| **Kat** | Intuit relationship, escalations, Rama/Donna contacts | MEDIUM |
| **Gayathri** | PM coordination, tracker updates | MEDIUM |
| **Augusto** | PLA-3431 payroll, ingestion, PLA-3416 gate 2 | HEAVY (blocked) |
| **Rama (Intuit)** | WFS flags, Payroll Hub, 6 perguntas pendentes | CRITICAL |
| **Donna (Intuit)** | Release coordination (replacing Christina) | UNCONFIRMED |

---

## 8. RISCOS E MITIGAÇÕES

| # | Risco | Prob | Impacto | Mitigação | Owner |
|---|-------|------|---------|-----------|-------|
| R1 | Code lock slips past Apr 10 | ALTA | Comprime timeline | Confirmar ASAP com Kat/Gayathri | Kat |
| R2 | Feature flags UAT atrasam | ALTA | Bloqueia data build | Identificar Siji replacement | Kat/Gayathri |
| R3 | WFS features não no May code lock | MÉDIA | WFS desacoplado | Rama confirmar | Kat |
| R4 | 21 click paths nunca chegam | ALTA | WFS validation impossível | Assumir click paths + escalar | Alexandra/Kat |
| R5 | Intuit validation resources indisponíveis | MÉDIA | Sem sign-off | Donna to confirm | Gayathri |
| R6 | Payroll bank verification falha | MÉDIA | WFS demos limitados | Payments app review ~Apr 16 | Thiago |
| R7 | Manufacturing tenant indefinido | ALTA | MR-050 blocked | Definir com Augusto ASAP | Thiago |
| R8 | Alexandra sobrecarregada (WFS 17 features solo) | ALTA | Validação incompleta | Priorizar ME+Dimensions primeiro; WFS por tiers | Thiago/Kat |

---

## 9. CADEIA DE CONFIANÇA

### ALTA (triangulado em 2+ fontes)

| Dado | Fontes |
|------|--------|
| 53 features | Excel + WIS + May Plan |
| 52 ativas (51 green + 1 on hold) | Excel + WIS |
| GA May 13 | Excel + Plan + Slack |
| OOTB: 48 Yes + 3 No + 1 N/A | Excel (extração programática) |
| 21 CP missing (14 WFS+Payroll) | Excel (extração programática) |
| Effort: 20S+25M+6L+1TBD | Excel (extração programática) |
| Fall = 100% PASS | Playbook + SOW + memory.md |
| Winter = 28/29 PASS | Exec Report + Deep Analysis |
| PLA-3431 payroll stuck | Bank Linking Research + memory + Slack |
| Alexandra = primary TSA | memory + May Plan + WFS memory |

### MÉDIA (1 fonte ou DRAFT)

| Dado | Fonte | Gap |
|------|-------|-----|
| Code lock ~Apr 10 | May Plan DRAFT | Não confirmado (hoje é Apr 14) |
| Flags UAT ~Apr 30 | May Plan DRAFT | Depende code lock |
| Siji replacement needed | May Plan DRAFT | Quem? |
| Donna Seapoe ativa | May Plan DRAFT | Não confirmado |
| Manufacturing tenant TBD | Tracker notes | Indefinido desde Feb |

### BAIXA / GAPS

| Gap | Ação |
|-----|------|
| Exact Fall feature count | fall_release_catalog pode ser parcial |
| Feb PASS/FAIL formal | Tratar como extensão Winter |
| WFS data migration ETA | Kat cobrar Rama |
| MR-053 Omni Pilot status final | Monitorar WIS |
| Effort Tracker v1 (Google Sheet) | Alexandra tem |

---

## 10. PREMISSAS DECLARADAS

| # | Premissa | Base | Risco se errada |
|---|----------|------|-----------------|
| P1 | May Plan DRAFT é o plano vigente | Google Doc Apr 9 | Timeline pode ter mudado |
| P2 | 51 Not Started features serão mantidas | WIS locked | Podem ser removidas Apr 17 |
| P3 | Alexandra continua como primary TSA | memory.md | Pode estar sobrecarregada |
| P4 | Keystone Construction é o environment principal | memory.md | Sem mudança esperada |
| P5 | WFS features estão no May code lock | May Plan W.2 | Rama precisa confirmar |
| P6 | Sweep system v8.1 será usado para validação | memory.md | Checks precisam update |
| P7 | Excel v4.0 é mais recente que WIS v2 | Filename + user provided | Interno diz v3.0 |

---

## 11. WIS vs EXCEL — DIVERGÊNCIAS DOCUMENTADAS

O Excel (fonte canônica) e o WIS (análise derivada) divergem em 10 features:

| Feature | Excel OOTB | WIS OOTB | Decisão |
|---------|-----------|----------|---------|
| MR-019 | Yes | Blank | Usar Yes |
| MR-021 | No | Not sure | Usar No |
| MR-025 | Yes | Blank | Usar Yes |
| MR-029 | Yes | No | Usar Yes, validar empiricamente |
| MR-033 | Yes | No | Usar Yes, validar empiricamente |
| MR-034 | Yes | Not sure | Usar Yes |
| MR-036 | N/A | Not sure | Usar N/A |
| MR-037 | Yes | Not sure | Usar Yes |
| MR-038 | Yes | Not sure | Usar Yes |
| MR-050 | Yes | No | Usar Yes, validar empiricamente |

**Nota:** WIS conta 51 features (exclui MR-014 descoped + MR-053 on hold). Excel conta 53.

---

## 12. DOCUMENTOS DE REFERÊNCIA

### Locais
| Doc | Path |
|-----|------|
| Excel Tracker | `Downloads/IES_May_Release_FY26_Feature_Tracking_v4.0.xlsx` |
| Ground Truth JSON | `intuit-boom/knowledge-base/_may_release_ground_truth.json` |
| May Release Plan DRAFT | `intuit-boom/knowledge-base/MAY_RELEASE_PLAN_2026.md` |
| WIS Feature Analysis | `intuit-boom/knowledge-base/WIS_FEATURE_ANALYSIS_MAY_2026.md` |
| WFS Scoping | `Downloads/WFS_UAT_Report/May_Release_Validation/WFS_MAY_RELEASE_SCOPING.md` |
| Bank Linking Research | `intuit-boom/knowledge-base/BANK_LINKING_DEEP_RESEARCH_2026-04-14.md` |
| Winter Master Plan | `intuit-boom/docs/WINTER_RELEASE_MASTER_PLAN.md` |
| Feb Analysis | `intuit-boom/knowledge-base/IES_FEBRUARY_RELEASE_FY26_ANALISE_CRITICA.md` |
| Fall Catalog | `Downloads/INTUIT BOOM DOWNLOAD/fall_release_catalog.md` |

### Google Docs
| Doc | URL |
|-----|-----|
| Effort Tracker v1 | https://docs.google.com/spreadsheets/d/1wVAb_WWl3BaT0m0F0uaPbn3CXShwB9Ll/edit |
| Action Plan Playbook | https://docs.google.com/document/d/1WaBY26WM9DzMPanhVMPgdF528zW2RxhD/edit |
| May Release Plan | https://docs.google.com/document/d/18DHVep4NPY4FZSap5ECC8EugMMmrTtQlNxJZFgaG90o/edit |
| WIS Google Sheet | https://docs.google.com/spreadsheets/d/1GNQdhMtV09v6quuF3AVJD9fvanq6eYvVq1Uz3VZcrYY/edit |
| UAT Doc (click paths) | Google Sheet `1AppjXKZu5PG5urv-mtPTM6NjguedQ1L7WVfd941UvB4` |
| Siji Working Doc | Google Sheet `1PPEdIMsmtkkLA_GfDK6m7vkfKvcpasL6CVx1oxOvvb0` |
| WFS Milestone | https://docs.google.com/spreadsheets/d/1aP3o4biKOmEPtnDjvXSWRpXK2oaPCAKE/edit |

### Intuit Contacts
| Pessoa | Role | Para quê |
|--------|------|---------|
| Donna Seapoe | Release coordination | PM coverage (replacing Christina) |
| Matt Hrabinski / Marcus Cramer | Sales Enablement | Seller comms |
| Rama Ghanta | WFS Product | Feature flags + WFS enablement |
| Sandra Bledsoe | WFS PMM | Data design doc |
| TBD (Siji replacement) | Product/tech | Feature flag activation |

---

*v3.0 | Reconstruído do zero com extração programática | Confiança ALTA nos dados quantitativos, MÉDIA nas premissas de timeline*
