# Construction Clone — Plano Focado
**Conta**: `quickbooks-testuser-construction-clone@tbxofficial.com`
**Dataset**: `321c6fa0-a4ee-4e05-b085-7b4d51473495` (Construction / Keystone)
**Ambiente**: IES (Intuit Enterprise Suite), 8 entidades
**Ultimo Sweep**: 9.0/10, Realism 87/100 (Apr 15, 2026)
**Atualizado**: 2026-04-15

---

## O Ecossistema (Corrigido)

```
1. Thiago + LLM criam CSVs com dados realistas
           |
2. Gate 1: validate_csvs.py (189 checks locais)
           |
3. Ingestao: INSERT no Postgres V2 (quickbooks DB)
           |
4. Gate 2: Retool Validator (pos-INSERT, 0 erros = PASS)
           |
5. Engenharia: Ticket p/ carregar no QuickBooks (activity plans)
           |
6. Config UI: Verificar se subiu correto no ambiente QBO
           |
7. Aguardar: Cron + activity plans rodam no periodo programado
           |
8. Sweep: Validacao visual do ambiente (bugs, realismo, funcionalidade)
```

**Ticket pra engenharia (quando CSVs prontos):**
1. Ticket com as bases ingeridas no dataset → engenharia carrega no QBO
2. Ticket pra cron/activities plan configurar a rotina de "vida" dos dados

---

## O Que Tem Hoje no Banco (Construction Dataset)

### Tabelas de Transacao (o que gera P&L e popula telas)

| Tabela | Total | parent | main_child | secondary_child |
|--------|:-----:|:------:|:----------:|:---------------:|
| **invoices** | **428** | 123 | 190 | 115 |
| invoice_line_items | 2,108 | - | - | - |
| invoice_li_classifications | 0 | - | - | - |
| **bills** | **96** | 43 | 16 | 37 |
| bills_line_items | 149 | - | - | - |
| **expenses** | **650** | 220 | 230 | 200 |
| expense_line_items | 1,006 | - | - | - |
| **estimates** | **75** | 25 | 28 | 22 |
| estimate_line_items | 410 | - | - | - |
| estimate_li_classifications | 1,640 | - | - | - |
| **bank_transactions** | **155** | 55 | 55 | 45 |
| **time_entries** | **5,624** | 1,126+ | 4,393+ | 0 |
| **payroll_expenses** | **312** | 0 | 312 | 0 |
| payroll_expense_li | 600+ | - | - | - |
| **purchase_orders** | **48** | 16 | 18 | 14 |
| po_line_items | 104 | - | - | - |
| po_li_classifications | 416 | - | - | - |
| **project_tasks** | **65** | 25 | 18 | 22 |

### Tabelas de Referencia (dados fixos, raramente mudam)

| Tabela | Rows | Nota |
|--------|:----:|------|
| customers | 50 | IDs 1-50 |
| product_services | 83 | IDs 2-83 + 212 |
| vendors | 33 | IDs 1-33 |
| employees | 45 | IDs 1-50 |
| projects | 9 | IDs 19-26 + 64 (P64 new, cron-generated) |
| chart_of_accounts | 121 | IDs 4-702 |
| classifications | 37 | Categorias de custo |

### Tabelas de Feature (funcionalidades extras)

| Tabela | Rows | Nota |
|--------|:----:|------|
| contractors | 27 | 1099 contractors (main_child) |
| contractors_documents | 4 | Documentos |
| mileage | 2,052 | Quilometragem (main_child) |
| vehicles | 8 | Frota |
| fixed_assets | 11 | Ativos fixos (main_child) |
| bundles | 3 | Pacotes de produto |
| bills_review | 10 | Workflow de aprovacao |
| expense_claims | 47 | Reembolsos |
| project_budgets | 6 | Orcamento de projetos |
| recurring_transaction | 3 | Transacoes recorrentes |
| forecast | 1 | Cash flow forecast |
| revenue_recognition_templates | 5 | Rev rec |
| time_schedule | 31 | Escalas (main_child) |
| intercompany_JE | 12 | Transacoes intercompany |
| transaction_rules | 4 | Regras bancarias |

### Tabelas VAZIAS (oportunidade de enriquecimento)

| Tabela | O que e | Vale criar? |
|--------|---------|:-----------:|
| change_orders | Ordens de mudanca (construction) | SIM — feature especifica do setor |
| receipts / receipts_line_items | Captura de recibos | TALVEZ — feature mobile |
| payroll_dimensions | Alocacao de custo payroll | SIM — melhora PM |
| project_attachments | Anexos de projeto | NAO — depende de upload |
| ~~invoice_li_classifications~~ | ~~Classificacao por invoice LI~~ | **CANCELADO** — invoices 100% inline |

### Income (calculado do banco: qty x price_rate)

| Entity | Income | Invoices |
|--------|--------|:--------:|
| parent | $4.66M | 123 |
| main_child | $7.31M | 190 |
| secondary_child | $4.42M | 115 |
| **TOTAL** | **$16.39M** | **428** |

Nota: Era $10.93M antes. Diferenca = +$5.46M das 93 invoices do PLA-3416 cash flow fix.

---

## O Que o Sweep Encontrou (Estado Atual do Ambiente)

### O Que Funciona Bem (nao mexer)

- Nomes de entidades: todos "Keystone" (fix permanente)
- CS3 (placeholders): ZERO violacoes
- Projeto "Civic Arena" (renomeado): fix persistiu
- GaleGuardian margem: 25.2% (fix persistiu)
- Volume de transacoes: bom (50+ expenses, 26+ estimates, 14 pagamentos)
- Multi-entity: 8 entidades acessiveis, nomes consistentes
- Overdue invoices: $0 (excelente)

### O Que Precisa de Atencao (P2)

| # | Problema | Causa Raiz | Acao |
|---|---------|-----------|------|
| 1 | **Leap Labs margem 74.1%** | Muita receita, pouco custo no projeto | Criar expense de ~$40K via sweep (FIX-18) |
| 2 | **Bayview margem 46%** | Idem | Criar expense de ~$2K via sweep (FIX-18) |
| 3 | **Azure Pines margem -37.6%** | Mais custo que receita | Criar invoice de ~$10K via sweep |
| 4 | **TidalWave $0 income no Projects** | QBO: Sub-customer != Project | Limitacao da plataforma. Precisaria recriar invoices com project assignment no LI |
| 5 | **Website faltando (todas entidades)** | SMS MFA bloqueia Company Info | Precisa de acesso ao telefone +5554991214711 |
| 6 | **1010 Checking inflado** ($673K QBO vs $460K Bank) | Atividade externa (Retool sync ou SE) | Monitorar, nao tem fix autonomo |
| 7 | **MMA Guardian Growth $10.9M** | Bug da engenharia no bank feed | Aceitar e documentar |

### O Que Muda Sozinho (volatil — sweep mensal necessario)

- Bank transactions to categorize: cresce ~1-3 por semana (cron ativo)
- Widgets "Last 30 days": mudam conforme calendario
- 1010 Checking balance: pode driftar por atividade externa

---

## Plano: O Que Criar Pra Enriquecer

### Nivel 1 — Correcoes de Margem (via sweep, sem CSV)

Essas sao fixes que voce faz direto no QBO durante o sweep usando o dual-engine:

| Fix | O que | Tempo |
|-----|-------|:-----:|
| Leap Labs expense $40K | Cria expense no QBO via Playwright | 5 min |
| Bayview expense $2K | Idem | 3 min |
| Azure Pines invoice $10K | Cria invoice via Playwright | 5 min |
| Categorizar bank txns | Categorizar as 9 pendentes | 10 min |

### Nivel 2 — Novas Bases (CSV + Ingestao) — **ATUALIZADO Apr 15**

| Prioridade | O que | Tabela | Rows | Status |
|:----------:|-------|--------|:----:|--------|
| **ALTA** | Change Orders | change_orders + LIs + dims | 20+62+248 | **CSVs PRONTOS** em ~/Downloads/ ⚠ ver nota DATE |
| **ALTA** | Fix inline classifications | expense_li + bills_li | 621 UPDATEs | **Script PRONTO** (fix_inline_classifications.py) |
| ~~ALTA~~ | ~~Invoice LI Classifications~~ | — | — | **CANCELADO** — invoices ja tem 100% inline |
| MEDIA | Payroll Dimensions | payroll_dimensions | ~100 | Pendente |
| MEDIA | Mais bank transactions | bank_transactions | +50 | Pendente |
| BAIXA | Receipts | receipts + LIs | ~20 + ~40 | Baixa prioridade |

### Nivel 3 — Evolucao do Dataset (futuro)

- Time entries pro secondary_child (hoje = 0, so parent e main_child tem)
- Mais bills pro main_child (so 16 vs 43 do parent — desproporcional)
- ~~Mais projetos~~ → Agora 9 com P64 crescendo organicamente via cron
- ~~P25/P26 precisam TEs~~ → Cancelados intencionalmente, nao precisa

---

## Workflow Pra Fazer Acontecer

### Passo 1: Fixes de Margem (AGORA, sem depender de ninguem)
Rodar sweep no construction-clone e aplicar FIX-18 em Leap Labs, Bayview, Azure Pines.

### Passo 2: Gerar CSVs (eu + LLM)
Criar CSVs de change_orders seguindo:
- `REGRAS_MASTER_DATABASE.md` para regras de validacao
- FK boundaries: customers 1-50, products 2-83+212, vendors 1-33, projects 19-26
- IDs: consultar MAX no banco antes (change_orders = 0, proximo = 1)

### NOTA — Change Orders Date Format
A tabela `quickbooks_change_orders` usa colunas de tipo `DATE` (nao `INTERVAL` como invoices/estimates).
CSVs armazenam dias inteiros (ex: `111` = dia 111 do ano). O pipeline precisa converter:
`base_date='first_of_year'` + `change_order_date=111` → `2026-04-21` (data real).
Se o pipeline nao suportar essa conversao para colunas DATE, abrir ticket com engenharia.
Tabela e GLOBALMENTE vazia (0 rows em TODOS os datasets) — feature nunca foi usada.

### Passo 3: Gate 1
Rodar `validate_csvs.py` nos CSVs gerados. 0 FAIL = pronto.

### Passo 4: Ingestao
INSERT no Postgres V2 (`quickbooks` DB).

### Passo 5: Gate 2
Abrir Retool, selecionar construction segment, validar 0 erros.

### Passo 6: Ticket pra Engenharia
Mensagem: "Inseri X rows nas tabelas Y e Z do dataset construction. Preciso:
1. Ticket pra carregar essas bases no QBO
2. Ticket pra configurar cron/activities plan se necessario"

### Passo 7: Verificar no QBO
Depois que engenharia confirmar, abrir o ambiente e verificar se os dados apareceram.

### Passo 8: Sweep
Rodar sweep completo pra validar tudo.

---

## IDs de Referencia

| O que | Valor |
|-------|-------|
| Dataset ID | `321c6fa0-a4ee-4e05-b085-7b4d51473495` |
| DB Host (V2) | `tbx-postgres-v2-unstable.flycast:5432` |
| DB Name | `quickbooks` |
| DB Host (Legacy) | `tbx-postgres-staging.internal:5433` |
| DB Name (Legacy) | `unstable` |
| Customer IDs | 1-50 |
| Product IDs | 2-83, 212 |
| Vendor IDs | 1-33 |
| Project IDs | 19-26, 64 |
| Employee IDs | 1-50 |
| Bank accounts | parent=5, main_child/secondary=6 |
| Invoice MAX ID | 45,562 (proximo: 45,563) |
| Invoice LI MAX ID | 121,835 (proximo: 121,836) |
| Bill MAX ID | 4,998 (proximo: 4,999) |
| Expense MAX ID | 10,294 (proximo: 10,295) |
| Estimate MAX ID | 840 (proximo: 841) |
| Bank Txn MAX ID | 1,475 (proximo: 1,476) |
| Time Entry MAX ID | 77,994 (proximo: 77,995) — growing via cron |
| Payroll MAX ID | 615 (proximo: 616) — growing via cron |
| PO MAX ID | 327 (proximo: 328) |
| Change Order MAX ID | 0 (proximo: 1) |

## PROXIMOS PASSOS (ATUALIZADO Apr 15, priorizado)

### Imediato (voce faz)
| # | Acao | Comando/Local | Tempo |
|---|------|---------------|:-----:|
| 1 | Executar fix inline classifications | `python scripts/fix_inline_classifications.py --execute` | 2 min |
| 2 | Verificar no Retool: expense/bills LI agora 100% classified | Retool | 5 min |
| 3 | Ingerir change_orders CSVs | `~/Downloads/CHANGE_ORDERS*.csv` → INSERT no V2 | 10 min |
| 4 | Gate 2: validar 0 erros no Retool pos-insert | Retool | 5 min |
| 5 | Ticket eng: carregar change_orders no QBO + cron/activity plan | Linear | 5 min |

### Proximo sweep (apos eng confirmar carga)
| # | Acao | Engine | Tempo |
|---|------|:------:|:-----:|
| 1 | Fix Leap Labs margin (expense $40K) | Playwright MCP | 5 min |
| 2 | Fix Bayview margin (expense $2K) | Playwright MCP | 3 min |
| 3 | Fix Azure Pines margin (invoice $10K) | Playwright MCP | 5 min |
| 4 | Categorizar bank txns pendentes | cursor-ide-browser | 10 min |

### Backlog (quando tiver oportunidade)
| # | O que | Prioridade |
|---|-------|:----------:|
| 1 | Time entries pra secondary_child | MEDIA |
| 2 | Mais bills pra main_child (16 → 40) | MEDIA |
| 3 | Payroll dimensions CSV | MEDIA |
| 4 | Bank transactions +50 | BAIXA |
| 5 | Receipts CSV | BAIXA |

### Bloqueados (precisa de acesso externo)
| Item | Bloqueio | Quem resolve |
|------|---------|:------------:|
| Website em Company Info | SMS MFA +5554991214711 | Acesso ao telefone |
| TidalWave $0 income nos Projects | Sub-customer != Project (limitacao QBO) | Re-design invoices com project_id no LI |
| MMA $10.9M bank feed bug | Bug da engenharia no bank feed | Eng |

---

## Artefatos Gerados nesta Sessao (Apr 15)

| Artefato | Local | O que faz |
|----------|-------|-----------|
| `scripts/fix_inline_classifications.py` | intuit-boom/scripts/ | UPDATE 621 inline cols (dry-run + --execute + --rollback) |
| `scripts/generate_change_orders_csv.py` | intuit-boom/scripts/ | Gera 3 CSVs de change orders (16 COs, 47 LIs, 188 dims) |
| `scripts/audit_cycle1.py` | intuit-boom/scripts/ | Deep DB audit (18 queries, V2 postgres) |
| `CHANGE_ORDERS.csv` | ~/Downloads/ | Change orders header CSV |
| `CHANGE_ORDERS_LINE_ITEMS.csv` | ~/Downloads/ | Line items CSV |
| `CHANGE_ORDERS_DIMENSIONS.csv` | ~/Downloads/ | Classification dimensions CSV |
| `CONSTRUCTION_CLONE_TRIANGULATION.md` | knowledge-base/ | 500-line triangulation master doc |
| `CONSTRUCTION_CLONE_PLAN.md` | knowledge-base/ | Este arquivo — plano focado |

---

## Bugs Encontrados nos Outros Datasets (Contexto — NAO e acao)

Esses servem pra aprender e melhorar o sweep/check, nao pra corrigir agora:

- **NonProfit**: 98% invoices no dia 0 (QB-04 violacao critica de cobertura mensal)
- **Manufacturing**: 934 invoices com datas >365d (QB-03 violacao)
- **Consulting**: 113 registros com datas >365d + volume baixo (135 invoices)
- **TCO**: Sem payroll, sem estimates
- **Todos**: Mes 12 (dezembro) com zero transacoes em quase todos datasets

**Aprendizado pro check**: Adicionar validacao de distribuicao mensal e QB-03 no validate_csvs.py.

---

## Score de Completude: 63/90 (70%)
| Dimensao | Score | Nota |
|----------|:-----:|------|
| Volume de transacoes | 9/10 | 428 inv, 650 exp, 96 bills, 5,624 TE |
| Distribuicao mensal | 8/10 | 12 meses, M0 low |
| Entity coverage | 7/10 | parent/main_child fortes, secondary_child fraco |
| Project coverage | 8/10 | P19-P24 ativos, P25-P26 canceled (ok), P64 novo |
| Classification coverage | 7/10 | Invoice 100%, Expense 44%, Bills 63% |
| Feature coverage | 8/10 | Mileage, fleet, assets, bundles, workflows |
| Change orders | 0/10 | Tabela vazia — CSVs prontos |
| Recurring/Lifecycle | 8/10 | 3 recurring + cron ativo |
| Realism | 8/10 | CS3=0, margens precisam fix em 2-3 projetos |

**Projecao apos fixes**: 71-75/90 (79-83%) com inline classifications + change orders + margin fixes.
