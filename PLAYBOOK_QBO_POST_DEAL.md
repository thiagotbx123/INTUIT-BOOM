# PLAYBOOK QBO POST-DEAL — Guia Completo de Implementação Intuit/QBO no TestBox

> **Versão:** 1.0 | **Data:** 2026-03-08 | **Autor:** Thiago (TSA Lead)
> **Audiência:** TSAs, CEs, novos membros, leadership
> **Fonte de verdade:** Este documento consolida 10+ fontes em um único guia E2E.

---

## Como Usar Este Playbook

```
Estou em...                          → Vá para...
─────────────────────────────────────────────────────
Deal acabou de fechar                → Cap 1 (Contrato & Intake)
Preciso entender o escopo            → Cap 2 (Discovery & Sizing)
Vou criar Linear tickets             → Cap 3 (Planning & Kick-off)
Preciso acessar contas QBO           → Cap 4 (Account Provisioning)
Vou carregar dados                   → Cap 5 (Dataset & Ingestion)
Preciso entender crons/activities    → Cap 6 (Automation)
Vou validar features                 → Cap 7 (Feature Validation)
Vou rodar um Sweep                   → Cap 8 (QBO Sweep)
Preciso coletar evidências           → Cap 9 (Evidence Collection)
Demo amanhã                          → Cap 10 (Launch & Go-Live)
Vou transferir o projeto             → Cap 11 (Hypercare & Handoff)
Preciso das tools do dia-a-dia       → Cap 12 (TSA Daily Ops)
```

---

## Glossário Rápido

| Termo | Definição |
|-------|-----------|
| **TSA** | Technical Solutions Architect — responsável pela implementação técnica |
| **CE** | Customer Engineer — foco em engajamento e demos |
| **QBO** | QuickBooks Online — produto Intuit sendo implementado no TestBox |
| **Sweep** | Validação autônoma de 46 checks em um ambiente QBO |
| **Gate** | Ponto de validação obrigatório antes de avançar para próxima fase |
| **DoR** | Definition of Ready — pré-requisitos para iniciar uma fase |
| **DoD** | Definition of Done — critérios de saída de uma fase |
| **RACI** | Responsible, Accountable, Consulted, Informed |
| **IES** | Intuit Ecosystem — rotas internas QBO (algumas retornam 404) |
| **CV** | Consolidated View — visão multi-entity no QBO |
| **COA** | Chart of Accounts — plano de contas |
| **TOTP** | Time-based One-Time Password — 2FA das contas TestBox |
| **Activity Plan** | Plano de ações automatizadas por dataset no DynamoDB |
| **Retool** | Dashboard interno TestBox para validação e operações |

---

## Diagrama E2E — Ciclo de Vida Completo

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CICLO DE VIDA INTUIT/QBO NO TESTBOX                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DEAL CLOSED                                                            │
│      │                                                                  │
│      ▼                                                                  │
│  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  ┌──────────┐     │
│  │ Phase 0│→ │ Phase 1  │→ │Phase 2-3 │→ │Phase 4 │→ │ Phase 5  │     │
│  │ Intake │  │Discovery │  │Planning/ │  │Account │  │ Dataset  │     │
│  │& Qual  │  │& Sizing  │  │Kick-off  │  │ Setup  │  │& Ingest  │     │
│  │ 1-3d   │  │ 5-10d    │  │ 4-6d     │  │ 5-7d   │  │ 10-20d   │     │
│  └────────┘  └──────────┘  └──────────┘  └────────┘  └──────────┘     │
│      Gate 0      Gate 1      Gates 2-3     Gate 4       Gate 5         │
│                                                                         │
│  ┌──────────┐  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Phase 6  │→ │Phase 7 │→ │ Phase 8  │→ │ Phase 9  │→ │Phase 10  │   │
│  │ Feature  │  │Validate│  │ Launch   │  │Hypercare │  │Closeout  │   │
│  │Validation│  │ QA+UAT │  │& Go-Live │  │& Handoff │  │& Retro   │   │
│  │ 5-10d    │  │ 5-10d  │  │ 1-3d     │  │ 5-10d    │  │ 2-3d     │   │
│  └──────────┘  └────────┘  └──────────┘  └──────────┘  └──────────┘   │
│      Gate 6      Gate 7       Gate 8        Gate 9       Gate 10       │
│                                                                         │
│  ════════════════════════════════════════════════════════════════════    │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │              OPERAÇÃO CONTÍNUA (pós Go-Live)                     │   │
│  │  22 Crons │ 15 Activities │ Weekly Sweeps │ Daily Health Check   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

Timeline total: 44-73 dias úteis (S/M/L sizing)
```

---

## RACI Matrix — Quem Faz o Quê

| Fase | Commercial Lead | Data TSA | Eng Lead | Data Gen Lead | PM | Executive |
|------|:-:|:-:|:-:|:-:|:-:|:-:|
| 0 - Intake | **R/A** | C | I | I | C | I |
| 1 - Discovery | C | **R/A** | C | C | R | I |
| 2 - Planning | I | R | C | C | **R/A** | I |
| 3 - Kick-off | C | R | R | R | **R/A** | C |
| 4 - Foundation | I | **R/A** | R | C | C | I |
| 5 - Build | I | C | R | **R/A** | C | I |
| 6 - Feature Setup | I | **R/A** | C | C | C | I |
| 7 - Validate | I | **R/A** | C | C | C | I |
| 8 - Go-Live | C | R | R | I | **R/A** | C |
| 9 - Hypercare | C | **R/A** | R | I | C | I |
| 10 - Closeout | C | C | C | C | **R/A** | R |

> **R** = Responsible | **A** = Accountable | **C** = Consulted | **I** = Informed

---

# Cap 0: Overview & Quick Reference

## O Que É Este Playbook

Este documento cobre o ciclo **completo** de uma implementação Intuit/QBO no TestBox — desde o momento em que o deal é assinado até a operação diária do TSA. Ele consolida e **referencia** (sem duplicar) os seguintes documentos fonte:

| # | Documento Fonte | Path Relativo | Contribuição |
|---|----------------|---------------|-------------|
| 1 | Full Implementation Process | `../../Tools/TSA_CORTEX/deliverables/full-implementation-process/FULL_IMPLEMENTATION_PROCESS.md` | 10 fases, RACI, gates, sizing |
| 2 | QBO Sweep Master | `PROMPT_CLAUDE_QBO_MASTER.md` | 46 checks, login, fix protocol |
| 3 | Evidence Collection | `knowledge-base/EVIDENCE_COLLECTION_PLAYBOOK.md` | 6-phase pipeline |
| 4 | Ingestion 3 Gates | `knowledge-base/INGESTION_3_GATES.md` | Validação de dados |
| 5 | TSA Onboarding | `docs/TSA_ONBOARDING_MASTER_GUIDE.md` | 90-day program |
| 6 | Retool Exports | `knowledge-base/access/retool_*_export.csv` | 16 prod + 70 staging |
| 7 | Automation Map | `build_qbo_automation_map.py` | 22 crons + 15 activities |
| 8 | Credentials | `knowledge-base/access/TESTBOX_ACCOUNTS.md` | 70+ contas |
| 9 | Transfer Package | `INTUIT_BOOM_TRANSFER/` | 11 docs de handoff |
| 10 | Sweep Learnings | `knowledge-base/sweep-learnings/*.md` | 12 sweep reports |

## Números-Chave

| Métrica | Valor |
|---------|-------|
| Fases de implementação | 10 (0-10) |
| Gates de validação | 11 (Gate 0-10) |
| Checks no Sweep | 46 (12 deep + 20 surface + 14 conditional) |
| Regras de ingestion | 59 (21 QB + 13 BIZ + 14 RL + 11 PIPE) |
| Crons automatizados | 22 |
| Activities por dataset | 15 |
| Contas TestBox | 70+ (58 CSV + 12 Linear) |
| Datasets ativos | 7 |
| Docs de transferência | 11 |
| Sweep reports existentes | 12 |

---

# Cap 1: Contrato & Intake (Fase 0)

**Duração:** 1-3 dias | **Owner:** Commercial Lead | **TSA:** Consulted

## Contexto

Quando um deal Intuit/QBO é fechado, o Commercial Lead inicia o processo de intake. O TSA é consultado para validar viabilidade técnica.

## Procedimento

1. **SOW recebido** — Commercial Lead distribui o Statement of Work
2. **Discovery form** — Preenchido com: produto, volume, features requeridas, timeline
3. **Fit assessment** — TSA avalia se o QBO TestBox suporta os requisitos
4. **Sizing preliminar** — S/M/L baseado em complexidade (veja Cap 2)

## Gate 0 Checklist

- [ ] SOW assinado e distribuído
- [ ] Discovery form preenchido
- [ ] Fit assessment: QBO cobre os requisitos?
- [ ] Timeline preliminar alinhada com capacity
- [ ] Stakeholders identificados (TestBox + cliente)
- [ ] Kickoff date proposta

## Decisões Críticas Nesta Fase

| Decisão | Quem Decide | Impacto |
|---------|-------------|---------|
| Aceitar/rejeitar implementação | Commercial + Executive | Go/No-Go |
| Dataset a usar | TSA (recomenda) | Determina entities, features, volume |
| Timeline | PM + Commercial | Commitment externo |

> **Ref:** `INTUIT_BOOM_TRANSFER/03_SOW_AND_SCOPE.md` para exemplos de SOW e escopo

---

# Cap 2: Discovery & Sizing (Fase 1)

**Duração:** 5-10 dias | **Owner:** Data TSA | **Gate:** Requirements approved

## Procedimento

1. **Levantar requisitos** — Features, volume de dados, entities, indústrias
2. **Mapear APIs** — Quais APIs QBO serão necessárias
3. **Sizing assessment:**

| Size | Entities | Features | Dados | Timeline |
|------|----------|----------|-------|----------|
| **S** (Small) | 1 | ≤20 | Seed only | 4-6 semanas |
| **M** (Medium) | 2-4 | 20-35 | Seed + Generated | 6-10 semanas |
| **L** (Large) | 5-8+ | 35-50 | Seed + Gen + Ingest | 10-16 semanas |

4. **Identificar riscos** — Dependencies, blockers, feature flags
5. **Documentar** — Requirements doc, data specs, sizing spreadsheet

## Gate 1 Checklist

- [ ] Requirements doc completo e aprovado
- [ ] Data volume specs definidos
- [ ] APIs mapeadas
- [ ] Sizing (S/M/L) definido
- [ ] Riscos documentados
- [ ] Architecture aprovada
- [ ] Customer kickoff date confirmada

## Datasets Disponíveis (7 ativos)

| Dataset | Indústria | Entities | Tipo |
|---------|-----------|----------|------|
| `construction` | Construção | 8 (parent + 7 children) | Multi-entity |
| `non_profit` | ONG | 3 (parent + 2 children) | Multi-entity |
| `professional_services` | Serviços | 3 | Multi-entity |
| `manufacturing` | Manufatura | 3 | Multi-entity |
| `tire_shop` / TCO | Varejo Auto | 4-5 | Multi-entity |
| `canada_construction` | Construção (CA) | 2-3 | Multi-entity |
| `mid_market` | Construção (Mid) | 1 | Single entity |

> **Ref:** `knowledge-base/access/TESTBOX_ACCOUNTS.md` para lista completa de 70+ contas

---

# Cap 3: Planning & Kick-off (Fases 2-3)

**Duração:** 4-6 dias | **Owner:** PM/Delivery | **Gates:** Kickoff ready + Team ready

## Fase 2: Pre-Project Planning (3-5 dias)

1. **Criar Linear tickets** — Epics por fase, stories por feature/task
2. **Montar GANTT** — Baseado no sizing, com milestones por gate
3. **Alocar recursos** — TSA lead, engineering support, data gen
4. **Configurar ambiente** — Channels Slack, Coda hub, Drive folder

### Linear Ticket Template

```
Title: [Phase X] - [Feature/Task Name]
Labels: intuit-boom, qbo, phase-X
Priority: [Urgent|High|Normal|Low]
Estimate: [Xpt]
Description:
  ## Context
  [What and why]
  ## Acceptance Criteria
  - [ ] Criterion 1
  - [ ] Criterion 2
  ## Dependencies
  - Blocked by: [ticket]
```

## Fase 3: Kick-off (1 dia)

1. **Team alignment** — Todos entendem scope, timeline, responsabilidades
2. **Customer sync** — Apresentar plano, confirmar milestones
3. **Launch agenda** — Distribuir RACI, meeting cadence, escalation path

## Gates 2 & 3 Checklist

- [ ] Linear board populated com todos os tickets
- [ ] GANTT criado com milestones por gate
- [ ] Resource plan aprovado
- [ ] Slack channel criado
- [ ] Coda hub configurado
- [ ] Drive folder estruturado
- [ ] Team alignment meeting realizada
- [ ] Customer kickoff executado

> **Ref:** `../../Tools/TSA_CORTEX/deliverables/full-implementation-process/FULL_IMPLEMENTATION_PROCESS.md` — Section 4 (Templates)

---

# Cap 4: Account Provisioning & Setup (Fase 4)

**Duração:** 5-7 dias | **Owner:** Data TSA | **Gate:** Infrastructure ready

## Hierarquia de Contas QBO

```
Account (email)
├── Company 1 (Parent)  ← CID (Company ID)
│   ├── Company 2 (Child)
│   ├── Company 3 (Child)
│   └── ...
└── Consolidated View (CV)
    ├── Shared COA
    ├── IC Transactions
    └── Consolidated Reports
```

## Login Protocol

1. Navegar para `https://app.qbo.intuit.com`
2. Inserir email da conta
3. Inserir senha
4. Resolver 2FA:
   - **TOTP** → Usar secret da conta para gerar código
   - **SMS** → Usar número cadastrado (pode ser blocker se +1 917-555-xxxx)
5. Verificar dashboard carregou
6. Confirmar entity correta (Company Switcher → nome da empresa)

### Known Login Issues

| Problema | Solução |
|----------|---------|
| SMS 2FA para número fictício | BLOCKED — precisa trocar para TOTP via settings |
| "Industry confirmation" dialog | Selecionar indústria correta e prosseguir |
| Passkey prompt | Cron `delete_passkey` roda MON 08:00 UTC |
| Session expired | Re-login, TOTP é regenerado |

## Retool Dashboard

**URL:** `https://retool.testbox.com/.../Integrations/Quickbooks/...`

- 16 contas em **production**, 70+ em **staging**
- Verificar environment (yellow dot = staging, green = production)
- TMS JWT necessário (expira periodicamente)

## Credenciais por Dataset

> **NUNCA commitar credenciais no Git.**
> Consulte: `knowledge-base/access/TESTBOX_ACCOUNTS.md` (70+ contas)
> Senha padrão: Documentada no TESTBOX_ACCOUNTS.md
> TOTP: Armazenados em DynamoDB `tbx-totp-secrets`

### Estrutura de Contas por Dataset

| Dataset | Account Pattern | # Companies |
|---------|----------------|-------------|
| Construction | `quickbooks-testuser-construction-*` | 8 (parent + 7 children) |
| TCO/Tire Shop | `quickbooks-testuser-tco-*` | 4-5 |
| Non-Profit (NV2) | `quickbooks-test-account-nv2` | 3 |
| Manufacturing (NV3) | `quickbooks-test-account-nv3` | 3 |
| Professional Services (NV1) | `quickbooks-test-account-nv1` | 3 |
| Mid Market | `mid_market@tbxofficial.com` | 1 |
| QSP Events | `quickbooks-test-account-qsp` | 3 |

## Gate 4 Checklist

- [ ] Todas as contas acessíveis (login + 2FA funcional)
- [ ] Company hierarchy verificada (parent + children)
- [ ] Retool dashboard acessível
- [ ] Datasets corretos vinculados às contas
- [ ] Industry settings corretos por entity

> **Ref:** `INTUIT_BOOM_TRANSFER/05_TECHNICAL_REFERENCE.md` para ambientes e APIs
> **Ref:** `INTUIT_BOOM_TRANSFER/09_CREDENTIALS_CHECKLIST.md` para checklist de acessos

---

# Cap 5: Dataset & Ingestion (Fase 5)

**Duração:** 10-20 dias | **Owner:** Data Generation Lead + Engineering | **Gate:** Data loaded

## Pipeline de Ingestion

```
  CSVs Preparados
       │
       ▼
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   GATE 1    │     │   GATE 2     │     │   GATE 3     │
│ validate_   │ ──► │   Retool     │ ──► │   Claude     │
│ csvs.py     │     │  Validator   │     │   Audit      │
│ (Pre-INSERT)│     │(Post-INSERT) │     │(Post-INSERT) │
└─────────────┘     └──────────────┘     └──────────────┘
  189 checks          Automated rules     5 auditors
  59 rules            0 errors required   PASS/FAIL/WARN
```

## Gate 1: validate_csvs.py (Pre-INSERT)

**Script:** `scripts/ingestion/validation/validate_csvs.py`
**Spec:** `scripts/ingestion/validation/VALIDATION_SPEC_CONSTRUCTION.xlsx`

**59 Regras em 4 Categorias:**

| Categoria | # Regras | Exemplos |
|-----------|----------|----------|
| **QB** (System) | 21 | Foreign keys, sequential IDs, date formats, NULL handling |
| **BIZ** (Business) | 13 | P&L logic, margins, COGS calculation |
| **RL** (Realism) | 14 | Data distribution, norms, seasonality, naming |
| **PIPE** (Pipeline) | 11 | CSV structure, encoding, row counts |

**Critério:** PASS=100%, FAIL=0, WARN aceitável com justificativa

## Gate 2: Retool Validator (Post-INSERT)

**Procedimento:**
1. Verificar environment = **staging** (yellow dot, bottom-left)
2. Obter TMS JWT válido
3. Colar JWT no campo "TMS Jwt"
4. Selecionar dataset segment
5. Click **Refresh BLUE** → aguardar SUCCESS
6. Click **Refresh TABLE** (upper) → Rule slugs
7. Click **Refresh TABLE** (lower) → Resumo

**Critério:** 0 errors em ambas tabelas

### Ciclo de Correção (Iterativo)

```
LOCATE error → INVESTIGATE (PostgreSQL) → CONTEXTUALIZE →
CORRECT (CSV ou DB UPDATE) → RE-INGEST → RE-VALIDATE → ASSESS
```

**DB Connection (Tailscale VPN required):**
- Host: `tbx-postgres-staging.internal:5433`
- User: `unstable` | DB: `unstable`
- Perms: INSERT/SELECT/UPDATE/DELETE em 17 tabelas

## Gate 3: Claude Audit (Post-INSERT)

**5 Auditores Especializados (simultâneos):**
1. **Financial** — P&L, margins, COGS, income vs expenses
2. **Integrity** — FKs, orphans, duplicates, sequential IDs
3. **Realism** — Distribution, variation, patterns
4. **Cross-Table** — Consistency entre tabelas relacionadas
5. **Schema** — Types, NULLs, constraints, formats

**Critério:** All PASS, no critical FAILs, WARNs documentados

## FK Dependency Order

```
Ao ingerir, respeitar a ordem de dependências:
1. customers
2. vendors
3. products_services (read-only, pré-existente)
4. accounts (COA)
5. invoices → invoice_lines
6. bills → bill_lines
7. expenses → expense_lines
8. time_entries
9. projects → project_tasks
10. bank_transactions
11. journal_entries
```

## Rollback

Se uma ingestion falha após INSERT parcial:
1. Identificar tabelas afetadas
2. `DELETE FROM table WHERE batch_id = X`
3. Corrigir CSVs
4. Re-ingerir na ordem correta
5. Re-validar (Gate 2 + Gate 3)

## Gate 5 Checklist

- [ ] Gate 1 PASS (validate_csvs.py)
- [ ] Gate 2 PASS (Retool — 0 errors)
- [ ] Gate 3 PASS (Claude Audit — all 5 auditors)
- [ ] P&L positivo em todas entities
- [ ] FK integrity verificada
- [ ] Volume de dados conforme sizing

> **Ref completa:** `knowledge-base/INGESTION_3_GATES.md`

---

# Cap 6: Automation — Activities & Crons

Este capítulo documenta TODA a automação que mantém os ambientes QBO vivos após ingestion.

## 15 Activities (Ações por Dataset)

Activities são ações ativadas por dataset via Activity Plans no DynamoDB.

| # | Activity | Categoria | Impacto QBO |
|---|----------|-----------|-------------|
| 1 | `INGEST_EXPENSES` | Expenses | Novos expenses, afeta P&L e banco |
| 2 | `INGEST_TRANSACTIONS` | Banking | Novas transações no bank feed |
| 3 | `INGEST_BILLS` | AP / Bills | Novos bills, afeta Balance Sheet |
| 4 | `INGEST_PROJECT_ESTIMATES` | Projects | Novos estimates vinculados a projetos |
| 5 | `ACCEPT_AND_CANCEL_PROJECT_ESTIMATES` | Projects | Muda status (Accepted/Cancelled) |
| 6 | `ACCEPT_AND_CONVERT_ESTIMATE_TO_INVOICE` | AR / Invoices | Novos invoices criados de estimates |
| 7 | `MILEAGE` | Expenses | Registros de mileage para veículos |
| 8 | `PURCHASE_ORDER` | AP / Purchase Orders | Novos POs no pipeline de vendor |
| 9 | `INGEST_INVOICES` | AR / Invoices | Novos invoices, afeta AR e Revenue |
| 10 | `INGEST_PROJECT` | Projects | Novos projetos com tasks e budgets |
| 11 | `ADD_GOAL_TO_PROJECT` | Projects | Atualiza goals/targets de projetos |
| 12 | `PAY_BILL` | AP / Bills | Marca como Paid, cria payment, afeta Cash |
| 13 | `PAY_INVOICE` | AR / Invoices | Marca como Paid, cria payment, afeta Cash |
| 14 | `INGEST_TIME_ENTRIES` | Time Tracking | Novos time entries em projetos |
| 15 | `JOURNAL_ENTRIES` | General Ledger | Impacto direto no GL |

### Activity Plan Flags

| Flag | Significado |
|------|------------|
| `all` | Executa em todos os datasets |
| `legacy_ingest` | Apenas datasets com ingestão legada |
| `construction_dataset_legacy` | Apenas construction legado |

## 22 Crons (Jobs Agendados)

Crons rodam em schedule fixo, independente de Activity Plans.

| # | Cron | Categoria | Schedule | Condição |
|---|------|-----------|----------|----------|
| 1 | `approve_time_entries` | Time Tracking | FRI 01:00 UTC | all |
| 2 | `ingest_bills_for_review` | AP / Bills | MON,FRI 18:00 UTC | all |
| 3 | `send_invoices` | AR / Invoices | Daily 16:00 UTC | all |
| 4 | `pay_invoices` | AR / Invoices | Daily 17:00 UTC | legacy only |
| 5 | `view_invoices` | AR / Invoices | Daily 17:00 UTC | all |
| 6 | `ingest_time_entries` | Time Tracking | TUE-SAT 17:00 UTC | construction legacy |
| 7 | `ingest_project_tasks` | Projects | TUE,THU 07:00 UTC | all |
| 8 | `mark_project_tasks_completed` | Projects | TUE 08:00 UTC | all |
| 9 | `create_annual_forecasts` | Forecasts | Jan 1 10:00 UTC | all |
| 10 | `create_expense_claims` | Expenses | MON,FRI 18:00 UTC | all |
| 11 | `review_expense_claims` | Expenses | FRI 18:30 UTC | all |
| 12 | `run_dimensions_backfill` | Dimensions | Daily 15:00 UTC | legacy only |
| 13 | `create_random_purchase_orders` | AP / PO | MON,FRI 18:00 UTC | legacy only |
| 14 | `run_payroll_last_day_of_month` | Payroll | 1st of month 12:30 UTC | all |
| 15 | `run_payroll_for_fifteenth` | Payroll | 16th of month 12:30 UTC | all |
| 16 | `create_next_year_activity_plan` | System | Dec 1 15:00 UTC | all |
| 17 | `bill_payment` | AP / Bills | FRI 07:00 UTC | legacy only |
| 18 | `confirm_bank_transactions` | Banking | FRI 01:00 UTC | all |
| 19 | `run_health_checks` | System | MON 00:00 UTC | all |
| 20 | `match_transactions` | Banking | FRI 00:00 UTC | all |
| 21 | `delete_passkey` | System | MON 08:00 UTC | all |
| 22 | `fix_negative_inventory_items` | Inventory | MON 06:00 UTC | all |

### Crons por Dia da Semana

```
MON: run_health_checks(00:00), fix_negative_inventory(06:00),
     delete_passkey(08:00), ingest_bills(18:00),
     create_expense_claims(18:00), create_random_POs(18:00)

TUE: ingest_project_tasks(07:00), mark_tasks_completed(08:00),
     ingest_time_entries(17:00)

WED: ingest_time_entries(17:00)

THU: ingest_project_tasks(07:00), ingest_time_entries(17:00)

FRI: match_transactions(00:00), approve_time_entries(01:00),
     confirm_bank_transactions(01:00), bill_payment(07:00),
     send_invoices(16:00), pay_invoices(17:00),
     view_invoices(17:00), ingest_time_entries(17:00),
     ingest_bills(18:00), create_expense_claims(18:00),
     create_random_POs(18:00), review_expense_claims(18:30)

SAT: ingest_time_entries(17:00)

MONTHLY: run_payroll (1st + 16th), create_annual_forecasts (Jan 1)
```

### Como Visualizar no Retool

1. Abrir Retool → Integrations → QuickBooks → Activity Plans
2. Selecionar account/dataset
3. Verificar `next_execution_at` (se >24h atrás → **alert**)
4. Ver CloudWatch logs para erros

### Legacy vs New Ingest

| Flag | Crons Afetados | Datasets |
|------|---------------|----------|
| `legacy_ingest` | pay_invoices, run_dimensions_backfill, create_random_POs, bill_payment | Older construction, TCO |
| `all` | Os demais 18 crons | Todos |
| `construction_dataset_legacy` | ingest_time_entries (cron) | Construction antigo |

> **Ref:** `build_qbo_automation_map.py` para dados completos

---

# Cap 7: Feature Validation (Fase 6)

**Duração:** 5-10 dias | **Owner:** Data TSA | **Gate:** Features configured

## Framework Universal de Validação

### Status Definitions

| Status | Significado | Ação |
|--------|------------|------|
| **VALIDATED** | Todos checks passam, evidência capturada | Nenhuma |
| **PARTIAL** | Alguns checks passam, prereqs faltam | Documentar o que falta |
| **NOT TESTABLE** | Requer novo tenant, QBDT, feature flag | Escalar para Eng |
| **NOT AVAILABLE** | Flag OFF, sem UI entry | Reportar para Intuit |
| **INTUIT PENDING** | Aguardando enablement | Follow up com Intuit |
| **BLOCKED** | Issue de engineering | Linear ticket |

### Playwright MCP Navigation

URLs que **funcionam** no QBO:

| Feature | URL | Notas |
|---------|-----|-------|
| Dashboard | `/app/homepage` | Ponto de entrada |
| Invoices | `/app/invoices` | AR |
| Expenses | `/app/expenses` | |
| Banking | `/app/register` | Bank feed |
| Customers | `/app/customers` | (Donors em NP) |
| Vendors | `/app/vendors` | |
| Projects | `/app/projects` | Customer Hub |
| Standard Reports | `/app/standardreports` | **NÃO** `/app/reportlist` |
| P&L Report | `/app/pnlreport` | |
| Balance Sheet | `/app/balancesheet` | |
| Chart of Accounts | `/app/chartofaccounts?jobId=accounting` | **NÃO** `/app/chart-of-accounts` |
| Company Settings | `/app/settings?panel=company` | **NÃO** `/app/company` |
| Classes | `/app/class` | |
| Locations | `/app/location` | |
| IC Account Mapping | `/app/ic-accountdefaults` | CV only |
| IC Transactions | `/app/multi-entity-transactions` | CV sidebar |
| Shared COA | `/app/sharedcoa` | CV only |

### Known 404 Routes (NÃO usar)

```
/app/dimensions          → usar /app/class + /app/location
/app/chart-of-accounts   → usar /app/chartofaccounts?jobId=accounting
/app/reportlist          → usar /app/standardreports
/app/customerlist        → usar /app/customers
/app/vendorlist          → usar /app/vendors
/app/company             → usar /app/settings?panel=company
/app/accounts            → usar /app/chartofaccounts?jobId=accounting
/app/donors              → usar /app/customers (em NP)
```

## Processo de Validação por Feature

1. **Navegar** para a URL da feature
2. **Aguardar** 30-45s (QBO SPA é lento)
3. **Verificar** se a feature renderizou corretamente
4. **Capturar** evidência (screenshot)
5. **Documentar** status (VALIDATED/PARTIAL/etc.)
6. **Reportar** issues encontrados

## Gate 6 Checklist

- [ ] Todas features do scope validadas
- [ ] Status documentado para cada feature
- [ ] Screenshots/evidências capturadas
- [ ] Issues reportados em Linear
- [ ] Blockers escalados

> **Ref:** `PROMPT_NV2_FEATURE_CHECKER.md` e `PROMPT_TCO_FEATURE_CHECKER.md` para prompts especializados

---

# Cap 8: QBO Sweep (Verificação Autônoma)

**Owner:** TSA (via Claude Code) | **Trigger:** "sweep" + ambiente

## Filosofia: VER → CORRIGIR → AVANÇAR

O Sweep é uma verificação **autônoma** de 46 checks que corrige inline sem parar para reportar. 100% hands-off.

## Arquitetura de Validação

```
┌──────────────────────────────────────────────────────┐
│                   QBO SWEEP v3.0                      │
├──────────────────────────────────────────────────────┤
│                                                       │
│  TIER 1: Deep Checks (12)                            │
│  ┌─────────────────────────────────────────────┐     │
│  │ Dashboard, P&L, Balance Sheet, Banking,     │     │
│  │ Customers, Revenue Distribution, COGS,      │     │
│  │ Margins, Net Income, Tax, COA, Projects     │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  TIER 2: Surface Checks (20)                         │
│  ┌─────────────────────────────────────────────┐     │
│  │ Settings, Navigation, Estimates, Inventory, │     │
│  │ Payroll, Workflows, RevRec, Fixed Assets,   │     │
│  │ Intercompany, Dimensions, Reports, etc.     │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  TIER 3: Conditional Checks (14)                     │
│  ┌─────────────────────────────────────────────┐     │
│  │ Multi-entity, Consolidated View, Balance    │     │
│  │ Reconciliation, Category Validation,        │     │
│  │ IC Transactions, Shared COA, etc.           │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
└──────────────────────────────────────────────────────┘
```

## 10 Estações do Sweep

| # | Estação | Checks | O que valida |
|---|---------|--------|-------------|
| 1 | **Dashboard** | 3 | P&L widget, revenue, company info |
| 2 | **P&L Report** | 4 | Income, COGS, expenses, net income (MUST be >0) |
| 3 | **Balance Sheet** | 3 | Assets, liabilities, equity balance |
| 4 | **Banking** | 3 | Bank accounts, pending txns, matching |
| 5 | **Customers/Donors** | 2 | Records, duplicates, naming |
| 6 | **Vendors** | 2 | Records, categories |
| 7 | **Projects** | 3 | Active projects, tasks, budgets |
| 8 | **COA** | 3 | Account structure, NP terminology, categories |
| 9 | **Settings** | 2 | Company info, industry, features enabled |
| 10 | **Content Safety** | 1 | No offensive/inappropriate content |

## Financial Health Rules

| Tipo de Entity | Net Income Target | Margin |
|---------------|-------------------|--------|
| Construction | Positivo | >20% |
| Non-Profit | Positivo | 2-10% surplus |
| Professional Services | Positivo | >15% |
| Manufacturing | Positivo | >10% |
| Tire Shop (TCO) | Positivo | >10% |

**Regra #1: Net Income MUST be positive em TODAS entities.**

## Fix Protocol (Inline)

Quando o Sweep encontra P&L negativo:
1. Criar Journal Entry (`/app/journal`)
2. DR: Accounts Receivable (escolher donor) → montante que inverte o deficit
3. CR: Revenue/Sales (ou Grant Revenue em NP) → mesmo montante
4. Salvar e verificar P&L novamente
5. Documentar JE no sweep learning

### Playwright Selectors para Journal Entry

```
Account:     aria-label="Choose an account N"  (N=line number)
Amount:      aria-label="Amount"                (auto-balances)
Description: aria-label="account_line_descriptionV3_N"
Name/Donor:  aria-label="Choose a payee line N" (REQUIRED for AR)
Memo:        textarea (footer area)
Save:        "Save and close" button (exact: true)
```

> **IMPORTANTE:** Rows são **lazy-activated** — line 2+ inputs não existem até clicar na row.

## Content Safety Scan

Verificar todas entities para:
- [ ] Nomes ofensivos ou insensíveis
- [ ] Referências a eventos reais controversos
- [ ] Dados pessoais reais (PII)
- [ ] Linguagem inapropriada

**Precedente:** "George Floyd Fund" renomeado para "Social Justice Fund" (2026-03-05)

## Post-Sweep Learning Loop

**OBRIGATÓRIO após cada sweep:**
1. Criar/atualizar arquivo em `knowledge-base/sweep-learnings/`
2. Formato: `{dataset}_{version}_{date}.md`
3. Incluir: score, findings, fixes aplicados, P1s pendentes
4. Commit no Git

## Sweep Report Format

```markdown
# {Dataset} Sweep — {Date}
## Version: v{X} | Score: {N}/10
## Account: {email}
## Entity: {name} (CID {id})

### Changes from Prior Version
| Metric | Before | After |
|--------|--------|-------|
| ... | ... | ... |

### TIER 1 — Deep Stations
#### Station 1: Dashboard
- Score: X/10
- P&L: $XXX (positive/negative)
- Findings: ...

### TIER 2 — Surface Scan
| Page | Status | Error |
|------|--------|-------|
| ... | Loaded/Error | ... |

### TIER 3 — Conditional
...

### Summary
- Overall: X/10
- P0: ...
- P1: ...
- Content: 0 violations
```

> **Ref completa:** `PROMPT_CLAUDE_QBO_MASTER.md` (1,163 linhas)
> **Sweep reports:** `knowledge-base/sweep-learnings/` (12 reports existentes)

---

# Cap 9: Evidence Collection & QA (Fase 7)

**Duração:** 5-10 dias | **Owner:** Data TSA | **Gate:** UAT passed

## Pipeline de 6 Fases

```
LOGIN → NAVIGATE → SCREENSHOT → UPLOAD → GROUP → XLSX
  │        │          │            │        │       │
  ▼        ▼          ▼            ▼        ▼       ▼
 2FA    30-45s     >100KB PNG   Drive    PNG→PDF  Hyperlinks
 TOTP   wait SPA   NOT 140KB   folder   per feat  + styling
```

### Fase 1: Login
- Playwright: preencher email/senha, resolver MFA (TOTP/SMS)
- Verificar dashboard carregou

### Fase 2: Navigate
- Ir para URL da feature
- **Aguardar 30-45 segundos** (QBO SPA render é lento — NÃO usar 10s)
- Verificar conteúdo renderizou

### Fase 3: Screenshot
- `browser_take_screenshot` → PNG
- **Validar tamanho:** >100KB = válido | ~140KB = possível 404 error page
- Naming: `{FEATURE_PREFIX}_{SEQ}_{description}.png`
- Exemplo: `F1_ME_REPORTS_01_CV_homepage.png`

### Fase 4: Upload
- Google Drive API → `MediaFileUpload`
- Verificar duplicatas antes de upload
- Lazy load — arquivo pode não aparecer imediatamente

### Fase 5: Group
- PIL/Pillow: PNGs → Multi-page PDF (1 feature per PDF)
- Stitching vertical com 50px gap
- Naming: `F1_ME_REPORTS.pdf`

### Fase 6: XLSX
- openpyxl: criar hyperlinks para PDFs no Drive
- Color palette:

| Status | Cor | Hex |
|--------|-----|-----|
| Header | Dark Blue + white text | `#2F5496` |
| VALIDATED | Green | `#C6EFCE` |
| PARTIAL | Yellow | `#FFEB9C` |
| NOT TESTABLE | Gray | `#D9D9D9` |
| Hyperlinks | Blue underlined | `#0563C1` |

## Google Drive Folder Structure

```
PROJECT_FOLDER/
├── screenshots/          (all individual PNGs)
├── F1_{FEATURE}.pdf      (grouped per feature)
├── F2_{FEATURE}.pdf
└── Evidence_Links.xlsx   (master with hyperlinks)
```

## Validation Criteria

- **VALIDATED:** Todos checks passam, evidência visual capturada
- **PARTIAL:** Funciona parcialmente, prereqs faltam
- **NOT TESTABLE:** Requer novo tenant/QBDT/feature flag
- **NOT AVAILABLE:** Flag OFF, sem UI entry
- **INTUIT PENDING:** Aguardando enablement Intuit
- **BLOCKED:** Issue de engineering

## Scripts Reutilizáveis

| Script | Função |
|--------|--------|
| `upload_to_drive.py` | Batch PNG upload |
| `merge_and_link.py` | PNGs → PDFs + upload + XLSX |
| `update_gsheet.py` | Download/modify/re-upload Google Sheets |
| `create_evidence_xlsx.py` | Standalone XLSX builder |
| `group_screenshots.py` | Vertical stitch PNGs |

## Gate 7 Checklist

- [ ] Todas features validadas com evidência
- [ ] PNGs capturados e uploaded para Drive
- [ ] PDFs agrupados por feature
- [ ] XLSX master com hyperlinks
- [ ] Defects resolvidos ou documentados
- [ ] UAT sign-off obtido

> **Ref completa:** `knowledge-base/EVIDENCE_COLLECTION_PLAYBOOK.md`

---

# Cap 10: Launch, Demo & Go-Live (Fase 8)

**Duração:** 1-3 dias | **Owner:** PM + TSA | **Gate:** Live

## Demo Prep Checklist (1 dia antes)

- [ ] Login funcional em todas entities
- [ ] P&L positivo em todas entities
- [ ] Dashboard widgets carregando
- [ ] Features-chave navegáveis (Projects, Reports, Banking)
- [ ] Content safety: 0 violações
- [ ] Crons rodando (check Retool → last execution)
- [ ] Bank transactions matching

## Daily Health Check (20 pontos)

Executar **1 hora antes de qualquer demo:**

| # | Check | Pts | Como verificar |
|---|-------|-----|---------------|
| 1 | Login funcional | 2 | Login + 2FA |
| 2 | Dashboard carrega | 2 | `/app/homepage` |
| 3 | P&L positivo | 2 | `/app/pnlreport` |
| 4 | Revenue > 0 | 1 | P&L: Income section |
| 5 | Balance Sheet balanceia | 2 | `/app/balancesheet` |
| 6 | Banking: pending txns | 1 | `/app/register` |
| 7 | Customers existem | 1 | `/app/customers` |
| 8 | Vendors existem | 1 | `/app/vendors` |
| 9 | Projects ativos | 1 | `/app/projects` |
| 10 | Invoices existem | 1 | `/app/invoices` |
| 11 | Reports carregam | 1 | `/app/standardreports` |
| 12 | Company info correto | 1 | `/app/settings?panel=company` |
| 13 | Industry correto | 1 | Settings → Company |
| 14 | No content violations | 1 | Visual scan |
| 15 | Multi-entity switch | 1 | Company switcher |
| 16 | Consolidated View (se app.) | 1 | CV entity |
| **Total** | | **20** | |

**Scoring:**
- 18-20: GO — demo seguro
- 15-17: GO com caveats — documentar issues
- <15: NO GO — fix antes da demo

## 1h Before Demo Verification

```
1. Login em TODAS entities (não só parent)
2. Verificar P&L: income > expenses
3. Verificar dashboard widgets
4. Abrir 3 features-chave da demo
5. Testar company switcher
6. Verificar se crons rodaram (Retool)
7. Preparar backup: screenshot de cada feature caso QBO fique lento
```

## Gate 8 Checklist

- [ ] Health check score ≥18/20
- [ ] Demo script preparado
- [ ] Backup screenshots prontos
- [ ] Customer notificado
- [ ] Go-live communication enviada

> **Ref:** `INTUIT_BOOM_TRANSFER/06_RUNBOOKS.md` para procedimentos operacionais

---

# Cap 11: Hypercare, Handoff & Closeout (Fases 9-10)

**Duração:** 7-13 dias | **Owner:** TSA (hypercare) + PM (closeout)

## Fase 9: Hypercare & Handover (5-10 dias)

### Monitoramento Diário
- Health check matinal (Cap 10 — 20 pts)
- Verificar alerts em `#dev-alerts` (>24h activity alert)
- Responder tickets em <4h

### Activity Alert "24h Behind"

**O que é:** Alerta interno TestBox quando `next_execution_at` > 24h atrás.
**Canais:** PROD → `#dev-alerts` | Staging → `#dev-info`
**Runbook:** Retool dashboard → Coda HOWTO unstick → Re-create golden → CloudWatch

### 6 Root Causes Comuns do Alert

1. Plans stuck (SMS fail blocks all — WOM-192/235/478)
2. Weekend false positives (PLA-2006)
3. Auth/IDP key errors (WOM-236/446/520)
4. DynamoDB scan limit (WOM-328 — fixed)
5. Golden activities expired ~14 days (WOM-417/479)
6. CallRail anti-abuse flagging (WOM-480)

## Transfer Package (11 docs)

O `INTUIT_BOOM_TRANSFER/` contém tudo que um novo operador precisa:

| # | Documento | Conteúdo |
|---|-----------|----------|
| 00 | `START_HERE.md` | Overview, glossário, reading order |
| 01 | `CLAUDE_MD_TRANSFER.md` | CLAUDE.md adaptado para novo operador |
| 02 | `MEGA_MEMORY.md` | 816 linhas de memória consolidada |
| 03 | `SOW_AND_SCOPE.md` | Escopo, releases, datasets |
| 04 | `ECOSYSTEM_MAP.md` | Projetos conectados ao INTUIT-BOOM |
| 05 | `TECHNICAL_REFERENCE.md` | Ambientes, login, APIs, databases |
| 06 | `RUNBOOKS.md` | Procedimentos step-by-step |
| 07 | `CONTACTS_AND_STAKEHOLDERS.md` | Who's who (TestBox + Intuit) |
| 08 | `RISK_MATRIX_AND_BLOCKERS.md` | Riscos e blockers |
| 09 | `CREDENTIALS_CHECKLIST.md` | Acessos a transferir |
| 10 | `DECISIONS_LOG.md` | Log de decisões com contexto |

## Fase 10: Closeout & Retrospective (2-3 dias)

1. **Métricas finais** — Features delivered, P&L health, defects resolved
2. **Lessons learned** — O que funcionou, o que não funcionou
3. **Playbook updates** — Atualizar este playbook com learnings
4. **Retro meeting** — Team + stakeholders

### Retrospective Template

```markdown
## Retrospective: [Project/Release Name]
### Date: YYYY-MM-DD

### What Went Well
- ...

### What Didn't Go Well
- ...

### Action Items
| Action | Owner | Deadline |
|--------|-------|----------|
| ... | ... | ... |

### Metrics
- Timeline: planned vs actual
- Features: planned vs delivered
- Defects: found vs fixed
- Sweep scores: initial vs final
```

## Gates 9 & 10 Checklist

- [ ] Hypercare: 0 P0 issues abertos
- [ ] All alerts resolved
- [ ] Transfer package completo (11 docs)
- [ ] Knowledge transfer executado
- [ ] Retro realizada
- [ ] Métricas finais documentadas
- [ ] Playbook atualizado com learnings
- [ ] Closeout doc assinado

> **Ref:** `INTUIT_BOOM_TRANSFER/` (11 documentos completos)

---

# Cap 12: TSA Daily Operations & Tools

## Ferramentas do Dia-a-Dia

| Ferramenta | Localização | Uso |
|-----------|-------------|-----|
| **TSA_CORTEX** | `../../Tools/TSA_CORTEX/` | Worklog automation, extraction |
| **REPORT_CHECK** | `../../Tools/REPORT_CHECK/` | QA de reports |
| **SpineHUB** | `../../Tools/SpineHUB/` | Template metodológico |
| **LINEAR_AUTO** | `../../Tools/LINEAR_AUTO/` | Automação Linear |
| **RETRO-TSA** | `../../Tools/RETRO-TSA/` | Retrospectivas |
| **STANDUP_AUDITOR** | `../../Tools/STANDUP_AUDITOR/` | Auditoria de standups |
| **TSA_FEEDBACK** | `../../Tools/TSA_FEEDBACK/` | Feedback reports |
| **TSA_DAILY_REPORT** | `../../Tools/TSA_DAILY_REPORT/` | Resumo dailies do time |

## Slash Commands Disponíveis

| Comando | Função |
|---------|--------|
| `/status` | Visão geral do estado do projeto |
| `/consolidar` | Consolidação de sessão (fim de trabalho) |
| `/weekly-ppt` | Gera PPT executivo do weekly standup |

## Meeting Cadence (TSA)

| Reunião | Frequência | Duração |
|---------|-----------|---------|
| Solutions Standup | Diário 9:00 AM | 15 min |
| 1:1 Manager | Semanal (Mon) | 30 min |
| Team Planning | Semanal (Mon) | 45 min |
| Cross-team Sync | Semanal (Wed) | 30 min |
| QBO Project Sync | Semanal (Thu) | 30 min |
| Team Retro | Bi-weekly (Fri) | 45 min |
| All-Hands | Mensal (1st Mon) | 60 min |

## Learnings Loop

```
SWEEP → LEARNING → COMMIT → IMPROVE
  │         │          │         │
  ▼         ▼          ▼         ▼
Execute   Document   Push to   Update
46 checks  findings   GitHub   playbook
            in sweep-           & sweep
            learnings/          master
```

**Regra:** Todo sweep DEVE gerar um learning report e commit no Git.

## TSA Onboarding Reference

Para novos membros, o programa de 90 dias está documentado em:
`docs/TSA_ONBOARDING_MASTER_GUIDE.md`

| Fase | Período | Foco |
|------|---------|------|
| Foundation | Week 1 | Cultura, tools, team |
| Deep Dive | Week 2 | QBO, customer context, shadow |
| Hands-on | Week 3-4 | Supervised execution |
| 30-Day | Checkpoint | Independent on basics |
| 60-Day | Checkpoint | Own relationships |
| 90-Day | Checkpoint | Full autonomy |

### Day 30 Milestones (novo TSA deve atingir)
- Explicar value prop em 2 minutos
- Nomear top 10 customers e use cases
- Navegar todas tools internas
- Set up demo environment independente
- Seguir protocolos de segurança/dados

### Day 90 Milestones
- Expert em assigned customers
- Pode treinar outros
- Gerencia relationships end-to-end
- Contribui para melhorias de processo

> **Ref completa:** `docs/TSA_ONBOARDING_MASTER_GUIDE.md` (90-day program)

---

## Apêndice A: Sweep Scores Históricos

| Dataset | Score | Date | Report |
|---------|-------|------|--------|
| Non-Profit (NV2) | 7.5/10 | 2026-03-05 | `sweep-learnings/non_profit_2026-03-05.md` |
| Mid Market | 6.5/10 | 2026-03-06 | `sweep-learnings/mid_market_v2_2026-03-06.md` |
| QSP Events | 7.5/10 | 2026-03-06 | `sweep-learnings/qsp_events_v2_2026-03-06.md` |
| Product Events | 5/10 | 2026-03-06 | `sweep-learnings/product_events_revalidation_2026-03-06.md` |
| Construction Clone | — | 2026-03-06 | `sweep-learnings/construction_clone_2026-03-06.md` |
| Manufacturing (NV3) | — | 2026-03-06 | `sweep-learnings/nv3_manufacturing_2026-03-06.md` |

## Apêndice B: Release History

| Release | Date | Status | Features |
|---------|------|--------|----------|
| **Fall Release** | 2025-11-20 | DELIVERED (100% PASS) | — |
| **Winter Release** | 2026-02 | VALIDATED (50/50: 46 PASS, 2 PARTIAL, 2 N/A) | — |
| **WAR ROOM** | 2026-02-05 | COMPLETE | Keystone dataset final (5,087 bank txns, 332 bills, 243 invoices) |

## Apêndice C: Key Contacts

> Consultar `INTUIT_BOOM_TRANSFER/07_CONTACTS_AND_STAKEHOLDERS.md` para lista completa.

## Apêndice D: Escalation Path

```
TSA (você)
  │ não resolveu em 4h?
  ▼
Senior TSA / TSA Lead
  │ não resolveu em 8h?
  ▼
Engineering Lead (via Linear P1/P0)
  │ requer Intuit?
  ▼
Commercial Lead → Intuit contact
```

---

> **Este playbook é um documento vivo.** Atualize-o após cada release, sweep, ou retrospective.
> **Última atualização:** 2026-03-08 | **Próxima revisão:** Após próximo release ou sweep cycle
