# GUIA CANONICO - INTUIT / QUICKBOOKS ONLINE
## Base de Conhecimento Completa para Analistas TestBox

> **DOCUMENTO CRITICO - LEITURA OBRIGATORIA**
>
> Este documento consolida TODO o conhecimento adquirido sobre Intuit/QuickBooks Online
> dos projetos intuit-boom, GOD_EXTRACT e TSA_CORTEX.
>
> **Gerado em:** 2026-01-07
> **Fonte:** Claude Code - Exploracao profunda de 3 projetos

---

# PARTE 1: VISAO GERAL EXECUTIVA

## 1.1 O que e a TestBox

**TestBox** e uma plataforma de demo automation SaaS que permite que equipes de vendas demonstrem produtos de software usando ambientes com dados reais e cenarios pre-configurados.

### Dados da Empresa
| Campo | Valor |
|-------|-------|
| Fundacao | 2020 |
| Sede | Boulder, Colorado, USA |
| CEO | Sam Senior (ex-Bain) |
| CRO | James Kaikis (ex-Salesforce, co-founder PreSales Collective) |
| Revenue 2024 | $5.7M (crescimento 235% YoY) |
| Funding Total | $12.7M |
| Time Brasil | 20+ engenheiros em 4 squads |

### Clientes Principais
- **Intuit/QuickBooks** (MAIOR CLIENTE - ~25-30% revenue)
- Gong, Zendesk, Apollo, Tropic, Brevo
- Gem, Zuper, Staircase, Mailchimp

### Por que Intuit e Critico
- Maior cliente da TestBox
- 5+ desenvolvedores dedicados
- 60 licencas adicionais assinadas em 12/23
- Concentracao de revenue = RISCO se entregas falharem

---

## 1.2 O que e QuickBooks Online (QBO)

**QuickBooks Online** e a plataforma de contabilidade em nuvem da Intuit, usada por pequenas e medias empresas para:
- Contabilidade e faturamento
- Folha de pagamento (Payroll)
- Gestao de despesas
- Relatorios financeiros
- Multi-entity (multiplas empresas)

### Versoes do Produto
| Versao | Publico | Features |
|--------|---------|----------|
| **Simple Start** | Freelancers | Basico |
| **Essentials** | Pequenas empresas | + Bills, multi-user |
| **Plus** | Empresas medias | + Inventory, Projects, Classes |
| **Advanced** | Empresas maiores | + Multi-entity, Custom reports, Workflows |
| **IES (Intuit Enterprise Suite)** | Enterprise | + Construction, Manufacturing, Nonprofit verticais |

### O que e IES (Intuit Enterprise Suite)
IES e a versao enterprise do QuickBooks para empresas com:
- Faturamento acima de $3M/ano
- Multiplas entidades legais
- Necessidades de verticais especificas (Construction, Manufacturing)
- Integracao com terceiros (3P apps)

---

## 1.3 Timeline de Releases FY26

```
         Jul    Ago    Set    Out    Nov    Dez    Jan    Fev    Mar    Abr    Mai    Jun
         |------|------|------|------|------|------|------|------|------|------|------|
                                      FALL 2025         WINTER FY26      FEBRUARY FY26
                                      (Nov 2025)        (Fev 2026)       (Fev+ 2026)
                                          |                 |                 |
AI Agents                              Base           Enhanced         Conversational BI
Reporting                              KPIs           Dashboards       3P Data + Benchmarks
Multi-Entity                           Hub            Allocations+     Consolidated AI
Dimensions                             v1             v2 + AI          Cross-entity
Construction                           Basic          Certified Pay    Projects AI
Payroll                                Core           Multi-Entity     Payroll Agent
```

### Datas Criticas
| Data | Evento |
|------|--------|
| 2025-11-20 | Fall Release ENTREGUE |
| 2026-01-15 | Sales Tax AI Early Access |
| 2026-02-04 | Winter Release Early Access |
| 2026-05-01 | WFS GA (General Availability) |

---

# PARTE 2: AMBIENTES E CREDENCIAIS

## 2.1 Contas de Acesso QBO

### TCO (Traction Control Outfitters) - PRINCIPAL
| Campo | Valor |
|-------|-------|
| Email | quickbooks-testuser-tco-tbxdemo@tbxofficial.com |
| Password | TestBox!23 |
| TOTP Secret | RP4MFT45ZY5EYGMRIPEANJA6YFKHV5O7 |
| Tipo | Multi-Entity (Parent + 3 Children) |

**Empresas TCO:**
| Nome | Realm ID | Tipo |
|------|----------|------|
| Vista Consolidada | 9341455649090852 | Consolidated View |
| Apex Tire & Auto Retail, LLC | 9341455130166501 | Child (Principal) |
| Global Tread Distributors, LLC | 9341455130196737 | Child |
| RoadReady Service Solutions, LLC | 9341455130170608 | Child |

### Construction (Keystone)
| Campo | Valor |
|-------|-------|
| Email | quickbooks-test-account@tbxofficial.com |
| Password | TestBox123! |
| TOTP Secret | 23CIWY3QYCOXJRKZYG6YKR7HUYVPLPEL |
| Tipo | IES Construction |

**Empresas Construction:**
- Keystone Construction (Par.) - Principal
- Keystone BlueCraft, Canopy, Ecocraft, Ironcraft, Stonecraft - Children

### WFS / GoQuick Alpha Retail
| Campo | Valor |
|-------|-------|
| Realm ID | 9341455848423964 |
| Billing Plan | PR_ELITE |
| Uso | APENAS EXPLORACAO (nao e ambiente final de demo) |
| Employees | 3 (Jim Halpert, Mary Jane, Michael Philbin) |

### Outras Contas
| Projeto | Email | Uso |
|---------|-------|-----|
| PRODUCT | quickbooks-tbx-product-team-test@tbxofficial.com | Produto |
| TCO_DEMO | quickbooks-tco-tbxdemo@tbxofficial.com | Demo |

---

## 2.2 URLs e Navegacao

### URLs Principais QBO
```
Base:           https://qbo.intuit.com
Homepage:       https://qbo.intuit.com/app/homepage
Banking:        https://qbo.intuit.com/app/banking
Payroll:        https://qbo.intuit.com/app/payroll
Employees:      https://qbo.intuit.com/app/employees
Time:           https://qbo.intuit.com/app/timetracking
Projects:       https://qbo.intuit.com/app/projects
Reports:        https://qbo.intuit.com/app/reportlist
HR Advisor:     https://qbo.intuit.com/app/hr
```

### Troca de Company (Multi-Entity)
```
URL Pattern: https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={REALM_ID}

Exemplo Apex:  https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId=9341455130166501
Exemplo Vista: https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId=9341455649090852
```

### Mineral HR (Acesso via QBO)
```
Base:           https://apps.trustmineral.com
Acesso:         QBO > HR Advisor > "Go to Mineral" (nova aba)
Dashboard:      https://apps.trustmineral.com/dashboard
Compliance:     https://apps.trustmineral.com/hr-compliance
Training:       https://apps.trustmineral.com/training
```

### APIs
```
QBO REST:       https://quickbooks.api.intuit.com/v3/company/{realmId}/
QBO GraphQL:    https://qb.api.intuit.com/graphql
Sandbox:        https://sandbox-quickbooks.api.intuit.com
```

---

## 2.3 Conexao via Playwright CDP

O acesso automatizado ao QBO usa **Chrome DevTools Protocol (CDP)** na porta 9222:

```python
from playwright.sync_api import sync_playwright

# Iniciar Chrome com CDP
chrome_cmd = [
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "--remote-debugging-port=9222",
    "--user-data-dir=C:\\Temp\\tsa_qbo_chrome_profile",
    "--no-first-run",
    "--disable-blink-features=AutomationControlled",
    "--start-maximized"
]

# Conectar Playwright
pw = sync_playwright().start()
browser = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
page = browser.contexts[0].pages[0]

# Navegar
page.goto("https://qbo.intuit.com/app/homepage")
```

**Script de Login Completo:** `C:\Users\adm_r\intuit-boom\layer1_login.py`

---

# PARTE 3: TCO (TRACTION CONTROL OUTFITTERS)

## 3.1 Historia do Negocio (Ficticio)

**Traction Control Outfitters (TCO)** e uma empresa diversificada de pneus operando em 3 bracos:
1. **Global Tread Distributors** - Wholesale (distribuicao atacado)
2. **Apex Tire & Auto Retail** - Retail (lojas de varejo)
3. **RoadReady Service Solutions** - Servicos + Roadside 24/7

### Dados do Negocio
| Campo | Valor |
|-------|-------|
| Fundacao | 1998 |
| Sede | Dallas, TX |
| Localizacoes | 9 locais, 4 estados (US) |
| Funcionarios | 250 |
| Board | 7 membros |
| Banco | Wells Fargo |
| Caixa Medio | $15-20M |
| Orcamento Anual | $250M |
| Fiscal Year End | 31 de Janeiro |

### Lideranca
| Nome | Cargo | Uso do IES |
|------|-------|-----------|
| Brooks | CEO | Multi-Entity Hub, AI Cash Flow, KPI Scorecard |
| Lisa | CFO | AR/AP Consolidation, Finance Agent, Intercompany |
| Jared | COO | Project Management, Job Costing, Payroll Integration |

## 3.2 Features IES que TCO Usa

| Feature | Para que serve | Quem usa |
|---------|---------------|----------|
| Multi-Entity Hub | Ver todas empresas em um lugar | Brooks, Lisa |
| Consolidated P&L/BS | Relatorios consolidados | Lisa |
| AI 13-week Cash Flow | Previsao de caixa | Brooks |
| 3-way Planning | Cash + P&L + Balance Sheet | Brooks |
| Finance Agent | Detecta anomalias | Lisa |
| Payments Agent | Coleta mais rapida | Lisa |
| AR/AP Consolidation | Visao unificada | Lisa |
| Intercompany Allocations | Ratear custos compartilhados | Lisa |
| Project Management Agent | Visao de projetos | Jared |
| Cost Rate Calculator | Calcular custo real de mao de obra | Jared |
| Payroll Integration | Custos de trabalho por projeto | Jared |

## 3.3 Dados Disponiveis no TCO

Extraidos do PostgreSQL (GOD_EXTRACT):

| Tabela | Registros | Uso |
|--------|-----------|-----|
| quickbooks_invoice_line_items | 115,725 | Faturamento |
| quickbooks_time_entries | 62,997 | Controle de tempo |
| quickbooks_customers | 10,615 | Clientes |
| quickbooks_bills | 4,704 | Contas a pagar |
| quickbooks_expenses | 4,277 | Despesas |
| quickbooks_employees | 1,695 | Funcionarios |
| quickbooks_projects | 60 | Projetos |
| quickbooks_dimensions | 49 | Dimensoes |

**Tamanho Total:** 172.57 MB (74 tabelas)

---

# PARTE 4: WINTER RELEASE FY26 (29 Features)

## 4.1 Resumo da Validacao

| Metrica | TCO | Construction |
|---------|-----|--------------|
| Features Validadas | 29/29 | 25/29 |
| Taxa de Sucesso | 100% | 86% |
| Screenshots EXCELLENT | 11 (38%) | 13 (42%) |
| Screenshots GOOD | 11 (38%) | 10 (32%) |
| Paginas 404 | 0 | 5 |

## 4.2 Lista Completa das 29 Features

### AI Agents (8 features)
| Ref | Feature | Status | Notas |
|-----|---------|--------|-------|
| WR-001 | Accounting AI | PASS | Bank feeds, suggested matches |
| WR-002 | Sales Tax AI | PASS | Pre-file validation |
| WR-003 | Project Management AI | PASS | Budget creation |
| WR-004 | Finance AI | PASS | Anomaly detection |
| WR-005 | Solutions Specialist | PASS | IES recommendations |
| WR-006 | Customer Agent | PASS | Gmail/Outlook integration |
| WR-007 | Omni/Intuit Intelligence | PASS | Beta |
| WR-008 | Conversational BI | PASS | Part of Intelligence |

### Reporting (6 features)
| Ref | Feature | Status | Notas |
|-----|---------|--------|-------|
| WR-009 | KPIs Customizados | PASS | 100+ KPIs library |
| WR-010 | Dashboards | PASS | AI summaries |
| WR-011 | 3P Data Integrations | PASS/404 | Apps marketplace |
| WR-012 | Calculated Fields | PASS | Reports customization |
| WR-013 | Management Reports | PASS | Full financials |
| WR-014 | Benchmarking | PASS | Performance Center |

### Dimensions (4 features)
| Ref | Feature | Status | Notas |
|-----|---------|--------|-------|
| WR-015 | Multi-Entity Reports | PASS | Consolidated view |
| WR-016 | Dimension Assignment v2 | PASS/PARTIAL | AI sparkles TCO, sem dados Construction |
| WR-017 | Hierarchical Dimension Reporting | PASS | Hierarchy |
| WR-018 | Dimensions on Workflow | PASS/404 | Workflow automation |

### Workflow (2 features)
| Ref | Feature | Status | Notas |
|-----|---------|--------|-------|
| WR-019 | Dimensions on Balance Sheet | PASS | Dimensions em transacoes |
| WR-020 | Parallel Approval | PASS/404 | Workflow automation |

### Migration (3 features)
| Ref | Feature | Status | Notas |
|-----|---------|--------|-------|
| WR-021 | Seamless Desktop Migration | PASS | Fresh tenant |
| WR-022 | DFY Migration | PASS | Done-For-You |
| WR-023 | Feature Compatibility | N/A | Documentacao, sem UI |

### Construction (2 features)
| Ref | Feature | Status | Notas |
|-----|---------|--------|-------|
| WR-024 | Certified Payroll Report | PASS | WH-347 |
| WR-025 | Tech Stack Assessment | PASS | Assessment |

### Payroll (4 features)
| Ref | Feature | Status | Notas |
|-----|---------|--------|-------|
| WR-026 | Multi-Entity Payroll Hub | PASS/404 | URL nao existe em Construction |
| WR-027 | Garnishments Child Support | PASS | Employee garnishments |
| WR-028 | Assignments in QBTime | PASS | Time tracking |
| WR-029 | Enhanced Amendments (CA) | N/A | Requer CA-specific tenant |

## 4.3 Framework de Validacao

### Principios Fundamentais
1. **Screenshot DEVE provar a feature** - Nao aceitar homepage generico
2. **Contexto correto OBRIGATORIO** - Multi-entity = Consolidated View
3. **Ambiente determina disponibilidade** - Nem toda feature em todo ambiente
4. **404 = Investigar, nao aceitar** - Tentar navegacao alternativa
5. **Organizar por contexto** - Agrupar capturas pelo mesmo contexto

### Criterios de Qualidade de Screenshot
| Qualidade | Tamanho | Significado |
|-----------|---------|-------------|
| EXCELLENT | >= 250 KB | Conteudo completo |
| GOOD | 150-250 KB | Conteudo adequado |
| ACCEPTABLE | 100-150 KB | Conteudo minimo |
| WEAK | 50-100 KB | Provavelmente loading |
| INVALID | < 50 KB | Erro ou loading |
| ERROR_PAGE | ~139 KB | Pagina 404 |

### Template de Evidence Notes
```
FEATURE: [WR-XXX] - [Nome]
AMBIENTE: [TCO/Construction/etc]
EMPRESA: [Nome no header]
CONTEXTO: [Individual/Consolidated/Fresh/Regional]

URL_NAVEGADA: [URL ou menu path]
TEMPO_ESPERA: [Xs]
ARQUIVO: [nome.png]
TAMANHO: [XXX KB]

O QUE FOI CAPTURADO:
- [Elemento 1 visivel]
- [Elemento 2 visivel]

STATUS: [PASS/PARTIAL/NOT_AVAILABLE/N/A]
JUSTIFICATIVA: [Porque este status]
```

---

# PARTE 5: WFS (WORKFORCE SOLUTIONS)

## 5.1 O que e WFS

**Intuit Workforce Solutions** e uma plataforma HCM (Human Capital Management) que combina:
- **GoCo capabilities** - HR, onboarding, benefits
- **QuickBooks Payroll** - Folha de pagamento
- **MineralHR** - Compliance e documentos

### Timeline WFS
| Fase | Data | Customers |
|------|------|-----------|
| Alpha | Dez 2025 | ~100 |
| Beta | Fev 2026 | Expandido |
| GA | 1 Mai 2026 | Geral |

## 5.2 Demo Stories Prioritizadas

### Story A: Unified PTO
- **User flow:** Employee > Manager > Payroll Admin
- **Steps:** Submit request > Approve > Balance updates > Payroll reflects
- **Dados:** 3 PTO policies, 5-10 pending requests
- **Ambiente:** Keystone (tem AVAILABLE VACATION)

### Story B: Magic Docs
- **User:** HR Admin
- **Steps:** Generate template > Smart fields > E-signature > Auto-save
- **Dados:** Complete profiles, doc templates
- **Ambiente:** GoQuick (tem Intuit Intelligence BETA)

### Story C: Hire to Fire Lifecycle
- **Flow:** Recruiting > Onboarding > Benefits > Payroll
- **Diferenciadores:** Unlimited templates, job costing
- **Ambiente:** Keystone

### Story D: Job Costing
- **Proof point:** Labor cost attributed to project/job code
- **Ambiente:** Keystone Construction

## 5.3 Stakeholders WFS

### Intuit
| Nome | Papel |
|------|-------|
| Ben Hale | Sales enablement |
| Nikki Behn | Marketing lead (GoCo) |
| Kyla Ellerd | Sales program management |
| Christina Duarte | Leadership, scoping |
| Nir | Headcount forecast |
| Kev Lubega | Mineral/WFS integration |

### TestBox
| Nome | Papel |
|------|-------|
| Katherine Lu | Program lead, SOW |
| Thiago Rodrigues | TSA, data architect |

## 5.4 Decisoes Importantes WFS

| Data | Decisao | Owner |
|------|---------|-------|
| 2025-12-17 | GoQuick Alpha != sales demo final | Katherine |
| 2025-12-15 | Staged rollout WFS obrigatorio | Katherine |
| 2025-12-10 | Health Check pode virar service | Thiago |

---

# PARTE 6: CONVERSATIONAL BI (February Release)

## 6.1 O que e

**Conversational BI** e a feature principal do February Release - uma IA conversacional que permite fazer perguntas em linguagem natural sobre dados do negocio.

### Exemplos de Perguntas
**Simples:**
- "Qual foi minha receita mes passado?"
- "Quantos clientes novos em dezembro?"

**Intermediarias:**
- "Analise minha receita e diga pontos importantes"
- "Compare minha receita com dados do clima"

**Complexas:**
- "Quao preditivo foi meu pipeline de CRM vs receita?"
- "Sugira formas de melhorar receita e lucros"

## 6.2 Diferencas vs ChatGPT

| Aspecto | ChatGPT/Gemini | Intuit Intelligence |
|---------|----------------|---------------------|
| Dados | Upload manual (stale) | Tempo real (live) |
| Precisao | "As vezes certo" | 100% para dados QBO |
| Seguranca | Dados externos | Dados ficam no Intuit |
| Joins | Fuzzy, error-prone | Nativo, accounting-aware |

## 6.3 Gaps Identificados (Comentarios Internos Intuit)

| Questao | Status | Impacto |
|---------|--------|---------|
| Payroll awareness? | Em duvida | Pode nao responder sobre payroll |
| Multi-entity aware? | Incerto | Pode nao funcionar em consolidated |
| 3P aware em Feb? | Incerto | Integracao 3rd party pode atrasar |
| ChatGPT partnership? | Nao documentada | Messaging pode mudar |

---

# PARTE 7: BANCO DE DADOS POSTGRESQL

## 7.1 Conexao

| Parametro | Valor |
|-----------|-------|
| Host | tbx-postgres-staging.internal |
| Port | 5433 |
| Database | unstable |
| User | unstable |
| Versao | PostgreSQL 15.2 |

**Acesso:** Via Tailscale VPN

## 7.2 Estrutura

- **36 databases** (unstable, dataset, snapshots versionados)
- **74 tabelas** quickbooks_*
- **172.57 MB** tamanho total
- **~178k registros** aproximado

## 7.3 Top 10 Tabelas

| Tabela | Tamanho | Rows |
|--------|---------|------|
| quickbooks_invoice_line_item_classifications | 64.93 MB | 776k+ |
| quickbooks_invoices | 30.94 MB | 44k+ |
| quickbooks_invoice_line_items | 27.19 MB | 115k |
| quickbooks_time_entries | 22.19 MB | 62k |
| quickbooks_customers | 10.45 MB | 10k |
| quickbooks_bills | 1.86 MB | 4.7k |
| quickbooks_expense_line_item_classifications | 1.52 MB | 14k |
| quickbooks_bills_line_item_classifications | 1.48 MB | 17k |
| quickbooks_employees | 1.43 MB | 1.6k |
| quickbooks_expenses | 1.34 MB | 4k |

## 7.4 Comandos Uteis

### Dump PostgreSQL
```powershell
$env:PGPASSWORD = "FaMVkKIM0IcsXHCW_323pJync_ofrBsi"

"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe" `
    -h tbx-postgres-staging.internal `
    -p 5433 `
    -U unstable `
    -d unstable `
    --format=c `
    --file="qbo_backup.dump" `
    --table="quickbooks_*"
```

### Smoke Queries
```sql
-- Contar tabelas
SELECT COUNT(*) FROM information_schema.tables
WHERE table_name LIKE 'quickbooks_%';

-- Top 5 por rows
SELECT 'quickbooks_customers', COUNT(*) FROM quickbooks_customers
UNION ALL SELECT 'quickbooks_invoice_line_items', COUNT(*) FROM quickbooks_invoice_line_items;

-- Sample customers
SELECT id, first_name, company_name FROM quickbooks_customers LIMIT 5;
```

---

# PARTE 8: RISCOS E BLOCKERS

## 8.1 Riscos Estrategicos Ativos

| # | Risco | Prioridade | Status |
|---|-------|------------|--------|
| 1 | WFS Environment Decision | P0 | PENDING |
| 2 | Negative Inventory TCO | P1 | PLA-2916 |
| 3 | Login ECS Task Failing | P1 | PLA-3013 |
| 4 | Canada Data Ingest | P1 | PLA-2969 |
| 5 | WFS SOW Finalization | P1 | IN PROGRESS |
| 6 | Manufacturing Visibility | P2 | GAP |
| 7 | Demo Load Time >20s | P2 | KLA-2337 |
| 8 | Winter Release Planning | P3 | NOT STARTED |

## 8.2 Blockers Linear

| Issue | Titulo | Assignee |
|-------|--------|----------|
| PLA-3013 | Login task failing TCO | Augusto Gunsch |
| PLA-2969 | Canada Data Ingest Bills | Lucas Torresan |
| PLA-2883 | Error ingesting activities | Augusto Gunsch |
| PLA-2724 | Dimensions in Payroll | Eyji Koike Cuff |

## 8.3 Anti-Patterns de Validacao (EVITAR!)

### Anti-Pattern 1: Screenshot Generico
```
ERRADO: Screenshot do Dashboard Homepage para provar Customer Agent
CERTO:  Screenshot de Customers > Leads tab com import Gmail/Outlook
```

### Anti-Pattern 2: Contexto Errado
```
ERRADO: Screenshot de Reports em "Apex Tire" para Multi-Entity Reports
CERTO:  Screenshot de Reports em "Vista Consolidada"
```

### Anti-Pattern 3: Aceitar 404
```
ERRADO: Capturar pagina 404 e marcar PASS
CERTO:  Investigar navegacao alternativa ou marcar NOT_AVAILABLE
```

### Anti-Pattern 4: N/A para Falhas
```
ERRADO: Marcar N/A porque a captura falhou
CERTO:  N/A e apenas para features de documentacao (sem UI)
```

---

# PARTE 9: ARQUIVOS E LOCALIZACOES

## 9.1 Projeto intuit-boom

```
C:\Users\adm_r\intuit-boom\
├── CLAUDE.md                         <- Instrucoes Claude
├── LAYERS.md                         <- Arquitetura de camadas
├── layer1_login.py                   <- Script de login automatizado
├── knowledge-base/
│   ├── INDEX.md                      <- LEIA PRIMEIRO
│   ├── UNIVERSAL_VALIDATION_FRAMEWORK.md
│   ├── qbo/
│   │   ├── QBO_DEEP_MASTER_v1.txt    <- 11k+ linhas de conhecimento
│   │   ├── QBO_MASTER.md
│   │   └── FEATURE_SURFACE_MAP.md
│   ├── wfs/
│   │   ├── WFS_CORTEX_v1.md          <- Memoria WFS
│   │   ├── WFS_NAVIGATION_MAP.md     <- 47 rotas QBO
│   │   └── WFS_POV_SOW_FRAMEWORK.md
│   └── strategic-cortex/
│       └── OUTPUT_A_EXECUTIVE_SNAPSHOT.md  <- STATUS ATUAL
├── docs/
│   ├── WINTER_RELEASE_MASTER_PLAN.md
│   ├── DEEP_ANALYSIS_REPORT_WINTER_RELEASE.md
│   └── TSA_ONBOARDING_MASTER_GUIDE.md
└── sessions/                         <- Historico de sessoes
```

## 9.2 Projeto GOD_EXTRACT

```
C:\Users\adm_r\GOD_EXTRACT\
├── QBO_EXTRACTION_PLAN.md            <- Plano de extracao
├── complete_extraction.py            <- Script extracao completa
├── inventory_qbo.py                  <- Inventario PostgreSQL
├── export_qbo_to_excel.py            <- Export para Excel
├── qbo_tables.csv                    <- Lista de 74 tabelas
├── qbo_inventory.json                <- Inventario JSON
├── knowledge-base/
│   ├── POSTGRESQL_QBO_EXTRACTION.md  <- Documentacao tecnica
│   └── testbox_company_profile.md    <- Perfil TestBox
└── qbo_dataset_package_v1/           <- Pacote extraido
    ├── dump/                         <- pg_dump
    ├── exports_optional/csv/         <- CSVs
    └── manifest/                     <- Metadados
```

## 9.3 Projeto TSA_CORTEX

```
C:\Users\adm_r\Projects\TSA_CORTEX\
├── src/
│   ├── collectors/                   <- 5 coletores
│   │   ├── slack.ts                  <- Slack API
│   │   ├── linear.ts                 <- Linear SDK
│   │   ├── drive.ts                  <- Google Drive
│   │   ├── local.ts                  <- Arquivos locais
│   │   └── claude.ts                 <- Claude sessions
│   ├── spinehub/                     <- Knowledge Graph
│   └── worklog/                      <- Geracao de narrativa
├── config/
│   └── default.json                  <- Configuracao central
├── knowledge-base/
│   └── learnings/                    <- Aprendizados
└── data/
    └── spinehub.json                 <- Knowledge graph
```

---

# PARTE 10: CHECKLIST PARA NOVA ANALISTA

## 10.1 Antes de Qualquer Trabalho

- [ ] Ler este documento COMPLETO
- [ ] Acessar `.claude/memory.md` do projeto
- [ ] Verificar `sessions/` para historico recente
- [ ] Consultar `knowledge-base/INDEX.md`
- [ ] Verificar riscos ativos no Linear

## 10.2 Para Validacao de Features

- [ ] Confirmar qual ambiente usar (TCO vs Construction)
- [ ] Verificar se feature requer contexto especial
- [ ] Usar UNIVERSAL_VALIDATION_FRAMEWORK.md
- [ ] Esperar 30-60 segundos antes de screenshot
- [ ] Validar tamanho do arquivo (>100KB)
- [ ] Documentar evidence notes completas

## 10.3 Para Acesso ao QBO

- [ ] Chrome com CDP na porta 9222
- [ ] Usar layer1_login.py ou login manual
- [ ] Verificar empresa correta no header
- [ ] Salvar screenshots com nomes descritivos

## 10.4 Para Extracao de Dados

- [ ] Conectar via Tailscale
- [ ] Usar credenciais PostgreSQL documentadas
- [ ] Rodar smoke queries antes de dump
- [ ] Gerar checksums SHA256

## 10.5 Ao Finalizar Trabalho

- [ ] Executar `/consolidar` no Claude
- [ ] Atualizar memory.md
- [ ] Criar arquivo de sessao
- [ ] Commit e push para Git

---

# PARTE 11: GLOSSARIO

| Termo | Definicao |
|-------|-----------|
| **QBO** | QuickBooks Online |
| **IES** | Intuit Enterprise Suite |
| **TCO** | Traction Control Outfitters (empresa ficticia) |
| **WFS** | Workforce Solutions (HCM) |
| **Multi-Entity** | Multiplas empresas sob um parent |
| **Consolidated View** | Vista consolidada de todas as empresas |
| **Realm ID** | Company ID no QBO |
| **CDP** | Chrome DevTools Protocol |
| **Dimension** | Categoria para classificar transacoes |
| **Feature Flag** | Toggle para habilitar features |
| **pg_dump** | Utility PostgreSQL para backup |
| **Smoke Test** | Teste basico de validacao |
| **PII** | Personally Identifiable Information |
| **TSA** | Technical Solutions Architect |
| **SOW** | Statement of Work |
| **UAT** | User Acceptance Testing |
| **Early Access** | Acesso antecipado a features |
| **GA** | General Availability |
| **3P** | Third Party (terceiros) |
| **Intercompany** | Entre empresas do mesmo grupo |
| **TOTP** | Time-based One-Time Password |

---

# PARTE 12: CONTATOS E ESCALACAO

## TestBox
| Nome | Papel | Quando contatar |
|------|-------|-----------------|
| Katherine Lu | Program Lead | Decisoes de escopo, SOW |
| Thiago Rodrigues | TSA Lead | Tecnico, dados, validacao |
| Sam Senior | CEO | Escalacao executiva |

## Intuit
| Nome | Papel | Quando contatar |
|------|-------|-----------------|
| Lawton Ursrey | Product Leader | IES, Fall Release |
| Jason/Crystal | Product/PMM | TCO, Construction feedback |
| Ben Hale | Sales Enablement | WFS demos |
| Kev Lubega | Integration | Mineral/WFS |

---

**FIM DO DOCUMENTO**

*Gerado por Claude Code em 2026-01-07*
*Fonte: Exploracao profunda de intuit-boom, GOD_EXTRACT, TSA_CORTEX*
*Total de arquivos analisados: 100+*
*Conhecimento consolidado: ~50,000 linhas de documentacao*
