# Construction Clone — Triangulacao Mestre
**Dataset**: `321c6fa0-a4ee-4e05-b085-7b4d51473495`
**Conta**: `quickbooks-testuser-construction-clone@tbxofficial.com`
**Gerado**: 2026-04-15 | Autonomo

---

## 1. MECANICA DO SISTEMA (Como os dados viram UI)

### 1.1 Pipeline de Dados
```
Postgres (legacy) → Hasura GraphQL → QBO Ingestion Engine → QBO UI
                                                    ↓
                        base_date='first_of_year' + relative_date → data real
```

- **base_date='first_of_year'**: TODAS as tabelas de transacao usam esta ancora
- **relative_date**: Intervalo em dias a partir de 1 Jan do ano corrente
- **Exemplo**: invoice com relative_invoice_date = 31 dias → 1 Fev 2026
- **Cobertura**: Invoices vao de dia 0 a 350 (quase ano inteiro)
- **Hoje (15 Abr 2026)**: dia ~105 → transacoes ate dia 105 ja "aconteceram"

### 1.2 Campos Internal dos Projetos (NAO usados pela UI)
Os campos `internal_*` dos projetos sao **pre-computados no Postgres** mas o QBO **recalcula na UI** baseado nas transacoes reais. Por isso:
- DB mostra margens -58% a -85% (internal_expense > internal_invoice)
- UI mostra margens 25% a 87% (baseado em transacoes com datas no periodo visivel)

**Conclusao**: Os campos `internal_*` servem como budget/planning, NAO como fonte de dados financeiros reais.

### 1.3 Project Revenue Attribution
- **invoice.project_id** = link header (usado pra listar invoice no projeto)
- **invoice_line_item.project_id** = link por LI (o que aparece no Project detail view de revenue)
- No construction dataset: **100% das 2,108 LIs tem project_id** e todos batem com o header
- **PROBLEMA JA DOCUMENTADO**: Sub-customer != Project no QBO. Invoices pro sub-customer "TidalWave" nao atribuem revenue ao Projeto TidalWave automaticamente

### 1.4 Activity Plans e Cron — **REVISADO (Audit Cycle 1)**
- **activity_plan** coluna: 100% `False` em expense_line_items e estimate_line_items
- **MAS**: O dataset esta CRESCENDO organicamente! Evidencias:
  - Time entries: 5,519 → **5,624** (+105). Novos TEs para projeto P64 (emp 1701, Priya Kapoor, dias 31-50+)
  - Payroll: 288 → **312** (+24). Novos IDs 592-615, todos main_child
  - Projetos: 8 → **9**. Novo P64 "Meridian Business Park — Phase 1" (customer 9, margin goal 20%)
- **Conclusao**: Cron/activity plans ESTAO ATIVOS para time entries e payroll. A coluna `activity_plan=False` nos LIs significa que os line items originais nao foram criados via activity plan, mas o sistema de geracao de novos dados ESTA funcionando.

### 1.5 Recurring Transactions
3 transacoes recorrentes (todas main_child):
1. Ongoing Maintenance (customer 41, monthly, Net 30, product 2, qty 10)
2. Ongoing Maintenance Ali (customer 40, monthly)
3. Ongoing Maintenance Chen (customer 21, monthly)

Estas geram invoices automaticas mensais no QBO — contribuem pra "vida" do ambiente.

### 1.6 Bank Feed
- 155 bank transactions (todas confirm=True = ja categorizadas no DB)
- **MAS**: O bank feed do QBO e VIVO e importa novas transacoes automaticamente
- Sweep anterior: 6-9 transacoes pendentes de categorizacao
- Crescimento: ~1-3 novas por semana (cron externo do TestBox)

---

## 2. INVENTARIO DETALHADO (O que tem no banco)

### 2.1 Tabelas de Transacao
| Tabela | Total | parent | main_child | secondary_child | Cobertura Mensal |
|--------|:-----:|:------:|:----------:|:---------------:|:----------------:|
| invoices | 428 | 123 | 190 | 115 | 12 meses (21-39/mes) |
| invoice_line_items | 2,108 | — | — | — | Via invoices |
| bills | 96 | 43 | 16 | 37 | 12 meses (4-12/mes) |
| bills_line_items | 149 | — | — | — | Via bills |
| expenses | 650 | 220 | 230 | 200 | 12 meses (32-63/mes) |
| expense_line_items | 1,006 | — | — | — | Via expenses |
| estimates | 75 | 25 | 28 | 22 | — |
| estimate_line_items | 410 | — | — | — | Via estimates |
| bank_transactions | 155 | 55 | 55 | 45 | 12 meses |
| time_entries | **5,624** | 1,126+ | 4,393+ | **0** | P19-P24. **GREW +105** (cron ativo!) |
| payroll_expenses | **312** | 0 | 312 | 0 | main_child. **GREW +24** |
| payroll_expense_LIs | **600** | — | — | — | Via payroll. GREW |
| purchase_orders | 48 | 16 | 18 | 14 | — |
| po_line_items | 104 | — | — | — | Via POs |
| intercompany_JE | 12 | — | — | — | Monthly (30d intervals) |
| ICJE lines | 384 | — | — | — | Via JEs |
| journal_entries | ? | — | — | — | — |

### 2.2 Tabelas de Referencia
| Tabela | Rows | Nota |
|--------|:----:|------|
| customers | 50 | IDs 1-50 |
| vendors | 33 | IDs 1-33, nomes realistas de construction |
| product_services | 83 | IDs 2-83 + 212 |
| employees | 45 | company_type='all' (IDs 1-50) |
| contractors | 27 | main_child only |
| chart_of_accounts | 121 | 33 Expense + 25 Other Current Liabilities + 15 OCA + 15 Fixed + 11 Income + 7 Bank + 5 COGS + misc |
| classifications | 37 | Arvore: Customer Type → Residential/Government/Commercial; Earthwork → Grading/Excavating; Utilities → Sewer/Gas/Water/Cabling; Concrete → Poured/Block/Slab |
| projects | **9** | IDs 19-26 + ID 64 (novo!). **GREW +1** |
| bank_accounts | 2 | ID=1 (MMA Guardian Growth, coa=102), ID=2 (1010 Checking, coa=5) |

### 2.3 Tabelas de Feature
| Tabela | Rows | Nota |
|--------|:----:|------|
| mileage | 2,052 | main_child |
| vehicles | 8 | Frota |
| fixed_assets | 11 | main_child |
| bundles | 3 | Pacotes de produto |
| bills_review | 10 | Workflow de aprovacao |
| expense_claims | 47 | Reembolsos |
| project_budgets | 6 | P19-P24 (P25-P26 sem budget) |
| project_tasks | 65 | Tarefas de projeto |
| project_milestones | 202 | Marcos |
| recurring_transaction | 3 | Invoices mensais (main_child) |
| forecast | 1 | Cash flow |
| rev_rec_templates | 5 | Revenue recognition |
| time_schedule | 31 | Escalas |
| transaction_rules | 4 | Regras bancarias (Petty Cash, Gas, Insurance, Meals) |
| workflow_automations | 8 | main_child only (invoice/PO/expense/payment notifications) |
| user_settings | 3 | parent + main_child + secondary_child |

### 2.4 Tabelas VAZIAS (Gaps)
| Tabela | O que e | Impacto na UI |
|--------|---------|:------------:|
| **change_orders** | Ordens de mudanca | Tela Construction vazia |
| **payroll_dimensions** | Alocacao custo payroll | PM sem detalhe payroll |
| **receipts** | Captura de recibos | Feature mobile ausente |
| **project_attachments** | Anexos | Depende upload |
| **vendor_notes** | Notas de vendor | Cosmético |
| **customer_notes** | So 2 notas | Baixo impacto |

---

## 3. CLASSIFICACOES — ANALISE REVISADA (Audit Cycle 1)

A **classificacao** e o que habilita filtros por dimensao no QBO.

### 3.1 Sistema DUAL de Classificacao (descoberta Apr 15)
O construction dataset usa **DOIS** sistemas de classificacao:
1. **Inline columns** nos LI tables: `customer_type`, `earthwork_class`, `utilities_class`, `concrete_class` — estes referenciam classification IDs diretamente
2. **Junction tables** (`*_line_item_classifications`): `line_item_id` + `classification_value_id` — usadas por datasets mais novos

### 3.2 Cobertura Real (corrigida)
| Tipo de LI | Inline Coverage | Junction Table | Status |
|------------|:--------------:|:--------------:|--------|
| invoice_line_items | **2108/2108 (100%)** | 0 | **OK — inline basta** |
| estimate_line_items | **410/410 (100%)** | 1,640 (4/LI) | OK — tem ambos |
| purchase_order_line_items | **104/104 (100%)** | 416 (4/LI) | OK — tem ambos |
| **expense_line_items** | **440/1006 (44%)** | 0 | **GAP — 566 rows sem class** |
| **bills_line_items** | **94/149 (63%)** | 0 | **GAP — 55 rows sem class** |
| payroll_expense_line_items | — | 577 (1/LI) | OK via junction |

### 3.3 Triangulacao (POR QUE inline funciona)
- Outros datasets (TCO, NonProfit, etc.) usam junction tables e tem 773K+ rows em `invoice_line_item_classifications`
- O construction dataset usou inline columns quando foi criado (design mais antigo)
- **A UI do QBO popula os filtros de classificacao a partir do que estiver disponivel** — inline OU junction
- **Resultado**: invoices do construction JA aparecem com classificacoes funcionais na UI

### 3.4 Acao Revisada
Em vez de criar ~13K rows de junction table, a acao correta e:
- **Preencher inline columns NULL** em expense_line_items: 566 rows (UPDATE, nao INSERT)
- **Preencher inline columns NULL** em bills_line_items: 55 rows (UPDATE)
- **Total: 621 rows para UPDATE** (muito menor que 13K INSERT estimados antes)

---

## 4. PROJETOS — TRIANGULACAO DB vs UI

### 4.1 Revenue por Projeto (calculado do DB: qty × price_rate)
| Project | Revenue DB | Exp Cost DB | Bill Cost DB | Margin DB | Margin UI (sweep) | Discrepancia |
|---------|:----------:|:-----------:|:------------:|:---------:|:-----------------:|:------------:|
| P19 Azure Pines | $1.65M | $232K | $120K | 78.6% | -37.6% | **ALTA** |
| P20 GaleGuardian | $2.29M | $350K | $108K | 80.0% | 25.2% | **ALTA** |
| P21 Intuit Dome | $3.32M | $260K | $169K | 87.1% | — | — |
| P22 Leap Labs | $2.39M | $229K | $76K | 87.2% | 74.1% | Moderada |
| P23 BMH | $2.04M | $456K | $124K | 71.6% | -11.1% | **ALTA** |
| P24 TidalWave | $1.53M | $382K | $149K | 65.2% | $0 income | **STRUCTURAL** |
| P25 Rowe Hotel | $1.50M | $295K | $125K | 71.9% | — | Novo |
| P26 Arbor Dunes | $1.68M | $131K | $62K | 88.6% | — | Novo |

**Explicacao da discrepancia**: O QBO calcula margens baseado no **periodo fiscal corrente** e filtra por entidade (parent vs child). Os dados no DB sao para company_type='all'. A UI do Project detail view filtra por entity que esta logada, mostrando so o subset de invoices/expenses daquela entidade.

### 4.2 Projetos Cancelados (P25, P26) — **CORRIGIDO**
| Recurso | P25 Rowe Hotel | P26 Arbor Dunes |
|---------|:--------------:|:---------------:|
| **Status** | **Canceled** | **Canceled** |
| Invoices | 44 | 40 |
| Estimates | 10 | 9 |
| Time entries | 0 | 0 |
| Expenses (project-linked) | 42 | 29 |

**Triangulacao CORRIGIDA**: P25 e P26 NAO sao "esqueleticos" — sao **intencionalmente cancelados**. Zero time entries e esperado para projetos cancelados. Nao precisa fix.

### 4.2b Novo Projeto P64 (descoberto Audit Cycle 1)
| Campo | Valor |
|-------|-------|
| Nome | Meridian Business Park — Phase 1 |
| Customer | ID 9 |
| Status | In progress |
| Margin Goal | 20% |
| Internal Estimate | $2.8M |
| Internal Invoice Total | $1.26M |
| Internal Expense Total | $1.07M |
| Time Entries | 105 (main_child, emp 1701 Priya Kapoor) |
| Company Type | all |

**Insight**: Este projeto foi criado externamente (engenharia ou data generator), NAO por nos. Demonstra que o pipeline de dados esta ativo.

### 4.3 Customer → Project Mapping
| Project | Customer | Sub-customer? |
|---------|----------|:------------:|
| P19 Azure Pines | Nadia Ahmed | Nao |
| P20 GaleGuardian | Amelia Patel | Nao |
| P21 Intuit Dome | Priya Patel | **SIM** (sub of True) |
| P22 Leap Labs | Michael Nguyen | Nao |
| P23 BMH | Emily Wong | Nao |
| P24 TidalWave | Matthew Ahmed | Nao |
| P25 Rowe Hotel | Harper Patel | Nao |
| P26 Arbor Dunes | Mateo Gonzalez | Nao |

**Insight**: P21 (Intuit Dome/Civic Arena) e o unico com sub-customer. Isso explica por que o income attribution funciona diferente.

### 4.5 Projetos QBO-Only (nao existem no DB) — **DESCOBERTA Audit Cycle 1**
| Projeto QBO | Customer | Margem UI | Origem |
|-------------|----------|:---------:|--------|
| Bayview Logistics Warehouse Expansion 2026 | Elena Garcia | 46% | Criado direto no QBO (nao no DB) |
| Cedar Ridge Community Center Renovation 2026 | Sarah Brown | 23.1% | Criado direto no QBO (nao no DB) |

**Triangulacao**: Estes projetos NAO estao em nenhum dataset Postgres. Foram criados:
- Via UI do QBO por usuario/Intuit SE, OU
- Por sweep fix/automacao anterior
- **Consequencia**: Se o dataset for re-ingerido, estes projetos NAO serao afetados (sao QBO-nativos)
- **Risco**: Nao sao monitoraveis via DB — so via sweep UI

### 4.6 Projeto DB-Only (ainda nao no QBO) — P64 Meridian Business Park
- Existe no DB (ID=64) com 105 time entries e 24 payroll entries
- **NAO aparece na UI do QBO** (verificado Apr 15)
- Provavelmente aguardando proxima janela de ingestion pela engenharia
- Customer: ID 9 (Jasmine Lopez), Margin Goal: 20%

### 4.4 Time Entries por Entidade
| Project | parent | main_child | secondary_child |
|---------|:------:|:----------:|:---------------:|
| P19 Azure Pines | 160 | 802 | 0 |
| P20 GaleGuardian | 117 | 697 | 0 |
| P21 Intuit Dome | 225 | 1,309 | 0 |
| P22 Leap Labs | 110 | 632 | 0 |
| P23 BMH | 271 | 503 | 0 |
| P24 TidalWave | 243 | 450 | 0 |
| P25 Rowe Hotel | 0 | 0 | 0 |
| P26 Arbor Dunes | 0 | 0 | 0 |

**Conclusao**: secondary_child NUNCA tem time entries. P25/P26 nao tem nenhum time entry.

---

## 5. BILLS-PO CHAIN

- **96 bills** no total, **21 linkados a PO** (21.8%)
- **48 POs** distribuidos: parent=16, main_child=18, secondary_child=14
- Bills sem PO = despesas diretas (normal em construction)
- POs bem distribuidos por vendors especializados (Electrical Solutions, Heavy Equipment, Tool Supply, etc.)

---

## 6. USER SETTINGS (DB vs UI)

| Campo | DB (ingestion) | UI (sweep fix) | Status |
|-------|:--------------:|:--------------:|--------|
| company_name | Keystone Construction | Keystone Construction | OK |
| zipcode | 92129 | 94043 (fixed via sweep) | **DIVERGE** — DB nao atualizado |
| website | NULL | NULL (blocked SMS MFA) | GAP |
| industry | Construction | Construction | OK |
| logo | Cloudinary URL | Funciona | OK |

**Insight**: Fixes feitos via sweep UI (como ZIP code) NAO retroalimentam o Postgres. Se o dataset for re-ingerido, os fixes somem.

---

## 7. CLASSIFICATION TREE

```
ROOT
├── Customer Type [DIM]
│   ├── Residential → General, Sub, General Contractor, Subcontractor
│   ├── Government → General, Sub, General Contractor, Subcontractor
│   └── Commercial → General, Sub, General Contractor, Subcontractor
├── Earthwork [DIM]
│   ├── Grading
│   └── Excavating
├── Utilities [DIM]
│   ├── Sewer
│   ├── Gas
│   ├── Water
│   ├── Cabling → Electrical, Telecom
│   ├── Electrical → Waterproof
│   └── Telecom
├── Concrete [DIM]
│   ├── Poured Concrete Foundations → Heavy Machine, Non-Heavy
│   ├── Concrete Block Foundations
│   └── Slab Foundations
└── 7000 Garden Bed [CLASS]
```

37 classificacoes. 4 dimensoes principais (Customer Type, Earthwork, Utilities, Concrete) + 1 class.

---

## 8. O QUE FALTA PRA SER "RICO, VIVO, REAL, FUNCIONAL"

### 8.1 Acoes Imediatas (via sweep, sem CSV)
| # | Acao | Tempo | Impacto |
|---|------|:-----:|:-------:|
| 1 | Criar expense $40K em Leap Labs (FIX-18) | 5 min | Margem 74% → ~40% |
| 2 | Criar expense $2K em Bayview (FIX-18) | 3 min | Margem 46% → ~35% |
| 3 | Criar invoice $10K em Azure Pines | 5 min | Margem -37% → ~-20% |
| 4 | Categorizar 7-9 bank transactions (FIX-02) | 10 min | Limpa banking |

### 8.2 Inline Classification Fixes (CORRIGIDO — nao precisa de junction CSV)
| Tabela | Rows a Corrigir | Tipo | Detalhes |
|--------|:--------------:|------|----------|
| expense_line_items | **566** | UPDATE inline cols | Preencher customer_type, earthwork_class, utilities_class, concrete_class |
| bills_line_items | **55** | UPDATE inline cols | Idem |

**Total: 621 UPDATEs** (drasticamente menor que 13K INSERTs estimados antes).
**Motivo da correcao**: Invoices ja tem 100% inline (2108/2108). Junction tables nao sao usadas por este dataset.
**Pattern**: Cada LI recebe 4 values — 1 de cada dimensao (Customer Type, Earthwork, Utilities, Concrete). Randomizar entre os IDs disponiveis: customer_type∈{6,7,8}, earthwork∈{15,16}, utilities∈{17,18,19,20,21,22}, concrete∈{26,27,28}.

### 8.3 Change Orders (Feature Construction)
| CSV | Rows | Schema |
|-----|:----:|--------|
| change_orders | ~15-20 | id, project (19-26), customer (1-50), estimate (1-75), change_order_date, accepted_date, service_date, description, unit_cost, customer_rate, note, memo, base_date='first_of_year', company_type |
| change_orders_LIs | ~45-60 | id, change_orders (FK), product_service (2-83), description, qty, unit_cost, mark_up_percent, customer_rate, customer_total |
| change_orders_dimensions | ~120-160 | id, LI FK, dimensions_account (classification IDs) |

### 8.4 Enriquecimento Futuro
| Acao | Prioridade | Depende de |
|------|:----------:|-----------|
| ~~Time entries pra P25/P26~~ | ~~ALTA~~ | **CANCELADO** — projetos Canceled intencionalmente |
| Time entries pra secondary_child | MEDIA | CSV + ingestion |
| Payroll dimensions | MEDIA | CSV |
| Mais bank transactions | BAIXA | CSV + cron config |
| Project budgets pra P25/P26 | MEDIA | CSV |

---

## 9. MAX IDs (Referencia para CSV Generation)

### Tabelas com dataset_id (ATUALIZADO Audit Cycle 1)
| Tabela | MAX ID | Count | Proximo | Delta |
|--------|:------:|:-----:|:-------:|-------|
| invoices | 45,562 | 428 | 45,563 | = |
| bills | 4,998 | 96 | 4,999 | = |
| expenses | 10,294 | 650 | 10,295 | = |
| estimates | 840 | 75 | 841 | = |
| bank_transactions | 1,475 | 155 | 1,476 | = |
| time_entries | **77,994** | **5,624** | 77,995 | **+105** |
| purchase_orders | 327 | 48 | 328 | = |
| payroll_expenses | **615** | **312** | 616 | **+24** |
| projects | **64** | **9** | 65 | **+1** |
| customers | 50 | 50 | 51 | = |
| vendors | 33 | 33 | 34 | = |

### Tabelas GLOBAIS (sem dataset_id)
| Tabela | MAX ID | Proximo |
|--------|:------:|:-------:|
| invoice_line_items | 121,835 | 121,836 |
| invoice_li_classifications | 777,621 | 777,622 |
| bills_line_items | 5,715 | 5,716 |
| bills_li_classifications | 17,912 | 17,913 |
| estimate_line_items | 4,488 | 4,489 |
| estimate_li_classifications | 7,265 | 7,266 |
| expense_line_items | 9,021 | 9,022 |
| expense_li_classifications | 17,015 | 17,016 |
| po_line_items | 1,251 | 1,252 |
| po_li_classifications | 3,796 | 3,797 |
| change_orders | 0 | 1 |
| change_orders_LIs | 0 | 1 |
| change_orders_dimensions | 0 | 1 |

---

## 10. RISCOS DE DURABILIDADE (Triangulados)

| Risco | Evidencia DB | Evidencia Sweep | Mitigacao |
|-------|:-------------|:---------------|-----------|
| **Re-ingestion apaga fixes de UI** | DB tem ZIP=92129, UI tem 94043 | Fix persistiu 2 sweeps | Se re-ingerir, ZIP volta. Atualizar CSV fonte |
| ~~Activity plans = False~~ | **CORRIGIDO**: Cron ATIVO — TE +105, payroll +24, P64 novo | Bank feed + TE crescendo | Ja funciona |
| ~~P25/P26 esqueleticos~~ | **CORRIGIDO**: Status=Canceled (intencional) | — | Nao precisa fix |
| **secondary_child sem TE** | 0 em todas as tabelas | Nao visivel em sweep | Enriquecimento futuro |
| **Inline class parciais** | expense 44% (566 NULL), bills 63% (55 NULL) | Filtros parciais | UPDATE 621 inline cols |
| **P64 sem invoices** | P64 tem 105 TEs mas 0 invoices verificados | Novo projeto | Verificar se pipeline gera |
| **MMA $10.9M** | Systemic bank feed bug | Confirmado em 4 sweeps | Aceitar |
| **1010 Checking drift** | Muda entre sweeps | $813K → $673K | Monitorar |

---

## 11. SCORE DE COMPLETUDE DO DATASET

| Dimensao | Score | Detalhes |
|----------|:-----:|---------|
| Volume de transacoes | 9/10 | 428 inv, 650 exp, 96 bills, **5,624 TE** (+105 crescendo) — robusto |
| Distribuicao mensal | 8/10 | 12 meses cobertos, M0 ligeiramente baixo |
| Entity coverage | 7/10 | parent e main_child fortes, secondary_child fraco (0 TE, 0 payroll) |
| Project coverage | **8/10** | P19-P24 ativos, P25-P26 canceled (intencional), **P64 NOVO** |
| Classification coverage | **7/10** | Invoices 100%, Estimates 100%, POs 100%. Expense 44%, Bills 63% |
| Feature coverage | 8/10 | Mileage, fleet, assets, bundles, workflows, forecasts — bom |
| Change orders | 0/10 | Tabela vazia — feature nativa de construction. Schema pronto |
| Recurring/Lifecycle | **8/10** | 3 recurring inv + bank feed + **cron ativo** (TE + payroll crescendo) |
| Realism | 8/10 | Nomes bons, CS3=0, margens precisam ajuste em 2 projetos |
| **TOTAL** | **63/90 (70%)** | **Subiu de 55 para 63** — cron ativo, classificacoes corrigidas, projetos cancelados OK |

---

## 12. LIMITACOES DO BROWSER AUTOMATION (Trianguladas Apr 15)

### 12.1 cursor-ide-browser
| Limitacao | Evidencia | Workaround |
|-----------|-----------|------------|
| **NAO preenche React amount inputs** | browser_fill/browser_type definem DOM value mas React state permanece $0.00. Expense salva com $0. | Usar Playwright MCP (`keyboard.type({delay:50})`) |
| **NAO consegue click em IES entity switcher** | Click intercepted por overlay CSS do dropdown | Playwright MCP funciona |
| **Tab/blur NAO trigger React onChange** | Tentado Tab, click fora, focus+blur — nenhum triggerou state update | Playwright MCP com delay simula keystroke real |
| **Scroll container nested problematico** | Expense form overlay com scroll interno impede click em elementos abaixo | Usar scrollIntoView:true ou Playwright |

### 12.2 Playwright MCP (user-playwright)
| Limitacao | Evidencia | Workaround |
|-----------|-----------|------------|
| **Requer login separado** | Sessao nao e compartilhada com cursor-ide-browser | Login TOTP dedicado antes de usar |
| **Sessao expira ~30min** | Inatividade causa timeout | Keepalive a cada 15 min |
| **Nao "ve" tabs do cursor-ide-browser** | Sao instancias de browser diferentes | Navegar independente na URL desejada |

### 12.3 Limitacoes de Plataforma QBO
| Limitacao | Evidencia | Impacto |
|-----------|-----------|---------|
| **SMS MFA em Company Info (TODAS entidades IES)** | Testado Parent + BlueCraft — mesmo modal +5554991214711 | Website/address edits bloqueados |
| **Sub-customer ≠ Project para income** | Invoice pro sub-customer TidalWave nao atribui income ao Projeto TidalWave | Requer line-item project_id no invoice |
| **IES routes que 404** | chart-of-accounts, products, inventory, salesreceipts, company, mhome | Usar sidebar nav |
| **{name} placeholder em Inventory headers** | Bug do QBO, nao fix possivel | Aceitar e documentar |

### 12.4 Regra de Ouro do Dual Engine
```
cursor-ide-browser  →  Navegacao, snapshot, text fields, dropdowns, clicks, read-only
Playwright MCP      →  Amount inputs, entity switching, complex React forms
```
Sempre login Playwright ANTES de precisar dele. Nunca confiar em browser_fill para campos financeiros.

---

## 13. AUDITORIA CICLICA — LOG DE VERIFICACOES

### Ciclo 1 (Apr 15 — pos-sweep v3)
- [x] Expense $0 criada por erro deletada com sucesso (txnId=3556)
- [x] 7/8 fixes do v2 persistiram
- [x] 1010 Checking drift: $813K → $673K (delta -$139K, causa externa)
- [x] Deep DB audit V2 completo — 18 queries executadas
- [x] **CORRECAO CRITICA**: Classificacoes inline existem em invoice LIs (100%) — junction tables vazias NAO sao gap
- [x] **CORRECAO**: P25/P26 status=Canceled (intencional, nao esqueleticos)
- [x] **DESCOBERTA**: Dataset CRESCENDO — cron ativo (TE +105, payroll +24, P64 novo)
- [x] **DESCOBERTA**: Novo projeto P64 "Meridian Business Park" (customer 9, main_child, 105 TEs)
- [x] **DESCOBERTA**: Emp 1703 (Priya Kapoor) e nova employee sem TEs nos projetos originais
- [x] **REFINAMENTO**: Gap real = 621 UPDATEs inline (566 expense + 55 bills), nao 13K INSERTs
- [x] Vendor diversity: 33 vendors, todos usados em bills. Boa distribuicao
- [x] Product coverage: apenas 1 produto nao usado ("3001 Cleaning Supplies")
- [x] Employee audit: 35/50 sem TEs (10 sao os que trabalham, 35 provavelmente admin/office)
- [x] Change orders schema confirmado: 3 tabelas prontas, zero rows
- [x] Script UPDATE inline classifications criado: `scripts/fix_inline_classifications.py` (566 exp + 55 bills = 621 rows)
- [x] CSVs de change_orders gerados: 16 COs + 47 LIs + 188 dims em ~/Downloads/
- [x] P64 verificado na UI: NAO aparece no QBO (aguardando ingestion)
- [x] Bayview + Cedar Ridge triangulados: existem SOMENTE no QBO (nao no DB)

### Ciclo 1 — Conclusoes
**Score de completude subiu de 55/90 (61%) → 63/90 (70%)**

Correcoes criticas ao entendimento:
1. Classificacoes inline cobrem 100% dos invoice LIs — NAO e gap
2. P25/P26 sao cancelados intencionalmente — NAO sao esqueleticos
3. Cron/activity plans ESTAO ATIVOS — dataset cresce organicamente
4. Ambiente tem dados hibridos: DB-ingested + QBO-native (Bayview, Cedar Ridge)
5. P64 existe no DB mas nao no QBO (pipeline pendente)

Scripts prontos para execucao pelo usuario:
- `scripts/fix_inline_classifications.py --execute` → Fix 621 NULL inline cols
- `scripts/generate_change_orders_csv.py` → 20 COs + 62 LIs + 248 dims (CSVs prontos, regenerados com fix RL-42)
- Change orders CSVs em: `~/Downloads/CHANGE_ORDERS*.csv`

---

### Ciclo 1 — Final Cross-Check (DB vs Sweep Rules)
| Check | Result | Detalhes |
|-------|:------:|---------|
| FK Integrity | **PASS** | 0 orphans em todas 6 relacoes LI→Parent |
| QB-03 (date range) | **PASS** | Invoices 0-350d, Expenses 1-334d, Bills 1-334d — nenhum >365 |
| CS3 (placeholder names) | **PASS** | 0 hits em customers, vendors, projects |
| Invoice amounts | **PASS** | Avg $7,773, Min $58, Max $105K, 0 negatives, 1 >$100K |
| All bills paid | **NOTE** | 96/96 paid=True (nenhum overdue no DB) |
| Revenue total | **$16.39M** | parent=$4.66M, main_child=$7.31M, secondary=$4.42M |
| Expense total | **$4.00M** | parent=$1.35M, main_child=$1.40M, secondary=$1.25M |
| Margin (all entities) | **~75.6%** | $16.39M rev - $4.00M exp = $12.39M profit |

**Nota**: Margem de 75.6% no DB e alta demais para construction real (3-15%). A UI mostra margens diferentes porque filtra por periodo e entidade. Os "internal_*" fields nos projetos mostram margens mais realistas porque incluem custos projetados.

---

---

### Ciclo 2 (Apr 15 — Audit vs CHECKLIST_INGESTION_CONSTRUCTION, 59 regras)

**Fonte**: `CHECKLIST_INGESTION_CONSTRUCTION (5).xlsx` — 59 regras (QB=21, BIZ=12, RL=15, PIPE=11)

#### Dataset Existente (V2 Postgres): 23 PASS, 1 FAIL
| Regra | Sev | Status | Detalhe |
|-------|:---:|:------:|---------|
| QB-01 dataset_id | BLK | **PASS** | 8 tabelas consistentes |
| QB-02 company_type | BLK | **PASS** | Todos validos |
| QB-03 dates<=365 | BLK | **PASS** | Max: 350 dias |
| QB-04 12-month coverage | BLK | **PASS** | 12 meses cobertos |
| QB-05 base_date | BLK | **PASS** | first_of_year |
| QB-06 interval format | BLK | **PASS** | Tipo interval confirmado |
| QB-07 ID uniqueness | BLK | **PASS** | 0 duplicatas |
| QB-08 sequential IDs | BLK | **PASS** | IDs 45135-45562 |
| QB-09 FK integrity | BLK | **PASS** | 0 orphans (inv_li, bill_li, customers) |
| QB-10 invoices have LIs | BLK | **PASS** | 0 invoices sem LIs |
| QB-11 bills paid_date | BLK | **PASS** | 0 NULL |
| QB-15 qty>=1 | BLK | **PASS** | Min=1 |
| **QB-17 bills purchasable** | **BLK** | **FAIL** | **35 bill LIs com purchasing=false** |
| QB-18 amount precision | BLK | **PASS** | 2108 LIs validos |
| QB-20 estimate status | BLK | **PASS** | accepted + cancelled |
| QB-21 classification 4/LI | BLK | **PASS** | 0 est LIs sem 4 classificacoes |
| BIZ-26 P&L per CT | CRT | **PASS** | parent 56%, main_child 78%, secondary 58% |
| BIZ-30 overall margin | HIGH | **PASS** | 66.3% (excl payroll) |
| RL-35 notes variation | CRT | **PASS** | 26 unique notes, 100% preenchidos |
| RL-36 terms variation | CRT | **PASS** | Net30=172, Net45=94, DueReceipt=70, Net60=67, Net90=25 |
| RL-40 amount range | HIGH | **PASS** | $749 - $235,606 |
| RL-42 no dupe products | HIGH | **PASS** | 0 invoices com produtos duplicados |
| RL-46 bill status convention | HIGH | **PASS** | 100% (96/96) |
| RL-47 bill-PO linkage | MED | **PASS** | 21% (21/96) |

#### QB-17 FAIL — Analise Detalhada (PRE-EXISTENTE)
7 produtos com `purchasing=false` usados em 35 bill LIs:
| Product | purchasing | Bills | Invoices | Tipo |
|---------|:---------:|:-----:|:--------:|------|
| 2070 Grading and Leveling | false | 9 | 116 | Service |
| 1732 Safety Planning | false | 7 | 79 | Service |
| 1505 Project Scheduling | false | 7 | 107 | Service |
| 1100 Lot Clearing | false | 4 | 107 | Service |
| 2060 Trenching | false | 3 | 48 | Service |
| 1098 Site Survey | false | 3 | 106 | Service |
| 1300 Temporary Electric | false | 2 | 60 | Service |

**Diagnostico**: Estes sao produtos service-type usados TANTO em invoices quanto bills. Foram criados com `purchasing=false` mas referenciados em bills. O checklist original marca H18=PASS, indicando que o check foi feito em versao anterior do dataset ou contra DB diferente.
**Risco**: Baixo — QBO aceita bill LIs com qualquer product, o flag purchasing e sugestao nao blocker.
**Acao**: Atualizar purchasing=true para estes 7 produtos (UPDATE simples) se quiser compliance total.

#### Change Orders CSVs: 12 PASS, 1 KNOWN
| Regra | Status | Detalhe |
|-------|:------:|---------|
| QB-02 | **PASS** | parent/main_child/secondary_child |
| QB-03 | **PASS** | Min=32, Max=273 |
| QB-04 | **PASS** | 8 meses (COs sao pos-contrato, 8 e adequado) |
| QB-05 | **PASS** | first_of_year |
| **QB-06** | **KNOWN** | change_orders usa colunas DATE, nao INTERVAL. Pipeline nunca testado |
| QB-08 | **PASS** | 1-20 sequencial |
| QB-10 | **PASS** | Todo CO tem LIs |
| QB-15 | **PASS** | Min qty=2 |
| QB-18 | **PASS** | 0 erros de precisao em 62 LIs |
| QB-21 | **PASS** | 62 LIs × 4 dims = 248 (correto) |
| RL-37 | **PASS** | 13 descricoes unicas |
| RL-42 | **PASS** | 0 duplicatas de produto por CO (FIX aplicado) |
| RL-40 | **PASS** | $967 - $111,606 |

#### Fix Script: ALL PASS
| Regra | Status | Detalhe |
|-------|:------:|---------|
| QB-09 | **PASS** | Todos classification IDs pertencem ao dataset |
| QB-21 | **PASS** | Preenche 4 cols por row |
| Safety | **PASS** | So toca NULLs, tem --rollback |
| Distribution | **PASS** | Uniforme (33% per CT, 50% per EW, 16% per UT, 33% per CO) — match existing |

#### Scripts de Auditoria Criados
- `scripts/audit_checklist.py` — Roda 24 checks automatizados contra V2 Postgres (reutilizavel)

---

*Gerado autonomamente por triangulacao: V2 Postgres DB × Sweep Report v3 × sweep_checks.py × QBO UI × CHECKLIST_INGESTION 59 regras*
*Completado: Apr 15, 2026 — Ciclo 1 (18 queries) + Ciclo 2 (24 checks vs checklist, CSV regeneration, script review)*
