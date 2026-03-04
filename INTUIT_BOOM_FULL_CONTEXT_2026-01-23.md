# INTUIT-BOOM - CONTEXTO COMPLETO PARA IA
## Documento de Transferencia de Conhecimento

> **PROPOSITO:** Este documento consolida TODO o conhecimento do projeto intuit-boom
> para que outra IA possa continuar o trabalho com contexto completo.
>
> **Gerado:** 2026-01-23
> **Score do Projeto:** 92/100 (Production)
> **Fonte:** SpineHUB + Strategic Cortex + Memory Files + Sessions

---

# PARTE 1: VISAO GERAL DO PROJETO

## 1.1 O que e o Projeto INTUIT-BOOM

**INTUIT-BOOM** e um projeto de validacao de features do QuickBooks Online (QBO) para a TestBox, focado em:
- Validacao automatizada de features de releases (Fall, Winter, February)
- Captura de screenshots como evidencia
- Geracao de trackers Excel com hyperlinks do Google Drive
- Automacao de login via Playwright CDP

### Dados do Projeto

| Campo | Valor |
|-------|-------|
| Cliente | Intuit (QuickBooks Online) |
| Tipo | Feature Validation + QA Automation |
| Linguagem | Python + Playwright |
| Score | 92/100 (Production) |
| Owner | Thiago Rodrigues (TSA Lead) |
| Localizacao | `C:\Users\adm_r\intuit-boom` |

### Por que este Projeto Existe

A TestBox fornece ambientes de demo para Intuit (maior cliente ~25-30% revenue).
Cada release do QBO (Fall, Winter, February) precisa ser validado nos ambientes TestBox.
Este projeto automatiza esse processo de validacao.

---

## 1.2 TestBox - Contexto da Empresa

**TestBox** e uma plataforma de demo automation SaaS:
- Fundada em 2020, sede em Boulder, Colorado
- CEO: Sam Senior (ex-Bain)
- Revenue 2024: $5.7M (crescimento 235% YoY)
- Time Brasil: 20+ engenheiros em 4 squads

### Clientes Principais
- **Intuit/QuickBooks** (MAIOR CLIENTE)
- Gong, Zendesk, Apollo, Tropic, Brevo
- Gem, Zuper, Staircase, Mailchimp

---

## 1.3 QuickBooks Online (QBO) - Contexto do Produto

**QuickBooks Online** e a plataforma de contabilidade em nuvem da Intuit:

### Versoes do Produto
| Versao | Publico | Features |
|--------|---------|----------|
| Simple Start | Freelancers | Basico |
| Essentials | Pequenas empresas | + Bills, multi-user |
| Plus | Empresas medias | + Inventory, Projects, Classes |
| Advanced | Empresas maiores | + Multi-entity, Custom reports, Workflows |
| **IES** | Enterprise | + Construction, Manufacturing, Nonprofit |

### IES (Intuit Enterprise Suite)
Versao enterprise para empresas com:
- Faturamento acima de $3M/ano
- Multiplas entidades legais
- Verticais especificas (Construction, Manufacturing)

---

# PARTE 2: ARQUITETURA DO PROJETO

## 2.1 Estrutura de Diretorios

```
C:\Users\adm_r\intuit-boom\
├── CLAUDE.md                 <- Instrucoes para Claude (LEIA PRIMEIRO)
├── LAYERS.md                 <- Sistema de camadas protegidas
├── GUIA_CANONICO_INTUIT_QBO.md <- Documentacao completa
├── .claude/
│   ├── memory.md             <- Estado persistente (LEIA NO INICIO)
│   ├── settings.local.json   <- Configuracoes
│   └── commands/             <- Slash commands (/status, /consolidar)
├── sessions/                 <- Historico de sessoes
├── knowledge-base/           <- Base de conhecimento
│   ├── INDEX.md              <- Catalogo de fontes
│   ├── strategic-cortex/     <- Visao consolidada
│   ├── slack-cortex/         <- Inteligencia Slack
│   ├── drive-cortex/         <- Inventario Drive
│   ├── qbo/                  <- Conhecimento QBO
│   └── wfs/                  <- Conhecimento WFS
├── docs/                     <- Documentacao e reports
├── qbo_checker/              <- Modulos Python
│   ├── feature_validator.py  <- Validador v2.0
│   ├── features_winter.json  <- Features Winter Release
│   └── FEATURE_VALIDATION_CANON.json <- Regras canonicas
├── data/                     <- Cache e dados
├── evidence/                 <- Screenshots
└── layer1_login.py           <- Script de login (LOCKED)
```

---

## 2.2 Sistema de Camadas Protegidas

O projeto usa sistema de camadas para proteger codigo estavel:

| Camada | Status | Responsabilidade |
|--------|--------|------------------|
| 1 - Login | **LOCKED** | Autenticacao Intuit + CDP |
| 2 - Navegacao | OPEN | Rotas e troca de companies |
| 3 - Screenshot | OPEN | Captura de evidencias |
| 4 - Planilha | OPEN | Geracao Excel + hyperlinks |
| 5 - Orquestracao | OPEN | Fluxo completo coordenado |

### Regras de Alteracao
- **LOCKED** = NAO ALTERAR sem autorizacao explicita
- **OPEN** = Pode alterar livremente
- **REVIEW** = Consultar antes de alterar

Para alterar camada LOCKED: Usuario deve dizer "Autorizo alteracao na CAMADA X"

---

## 2.3 Slash Commands Disponiveis

| Comando | Funcao |
|---------|--------|
| `/status` | Ver estado do projeto, camadas e ultimas atividades |
| `/consolidar` | Salvar aprendizados da sessao + commit GitHub |

---

# PARTE 3: AMBIENTES E CREDENCIAIS

## 3.1 Contas de Acesso QBO

### TCO (Traction Control Outfitters) - PRINCIPAL
| Campo | Valor |
|-------|-------|
| Email | quickbooks-testuser-tco-tbxdemo@tbxofficial.com |
| Password | TestBox!23 |
| TOTP Secret | RP4MFT45ZY5EYGMRIPEANJA6YFKHV5O7 |
| Tipo | Multi-Entity (Parent + 4 Children) |

**Empresas TCO:**
| Nome | Realm ID | Tipo |
|------|----------|------|
| Vista Consolidada | 9341455649090852 | Consolidated View |
| Apex Tire & Auto Retail, LLC | 9341455130166501 | Child (Principal) |
| Global Tread Distributors, LLC | 9341455130196737 | Child |
| Traction Control Outfitters, LLC | 9341455130188547 | Child |
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

### Outras Contas
| Projeto | Email |
|---------|-------|
| PRODUCT | quickbooks-tbx-product-team-test@tbxofficial.com |
| TCO_DEMO | quickbooks-tco-tbxdemo@tbxofficial.com |

---

## 3.2 URLs e Navegacao QBO

### URLs Principais
```
Base:           https://qbo.intuit.com
Homepage:       https://qbo.intuit.com/app/homepage
Banking:        https://qbo.intuit.com/app/banking
Payroll:        https://qbo.intuit.com/app/payroll
Employees:      https://qbo.intuit.com/app/employees
Projects:       https://qbo.intuit.com/app/projects
Reports:        https://qbo.intuit.com/app/reportlist
```

### Troca de Company (Multi-Entity)
```
URL Pattern: https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={REALM_ID}
```

---

## 3.3 Conexao via Playwright CDP

O acesso automatizado usa Chrome DevTools Protocol na porta 9222:

```python
from playwright.sync_api import sync_playwright

# Conectar ao Chrome com CDP
pw = sync_playwright().start()
browser = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
page = browser.contexts[0].pages[0]

# Usar layer1_login.py
from layer1_login import login, connect_qbo, PROJECTS
pw, browser, page = login("TCO", "apex")
```

**Script Oficial:** `layer1_login.py` (LOCKED)

---

# PARTE 4: RELEASES E FEATURES

## 4.1 Timeline de Releases FY26

```
         Nov 2025      Fev 2026      Mai 2026
            |             |             |
       FALL RELEASE  WINTER RELEASE  FEBRUARY RELEASE
       (ENTREGUE)    (Em validacao)  (Planejamento)
```

### Datas Criticas
| Data | Evento |
|------|--------|
| 2025-11-20 | Fall Release ENTREGUE |
| 2026-01-15 | Sales Tax AI Early Access |
| 2026-02-04 | Winter Release Early Access |
| 2026-02-25 | Winter Release Launch |
| 2026-05-01 | WFS GA (General Availability) |

---

## 4.2 Winter Release FY26 (29 Features)

### Status da Validacao
| Metrica | TCO | Construction |
|---------|-----|--------------|
| Features Validadas | 29/29 | 25/29 |
| Taxa de Sucesso | 100% | 86% |
| Screenshots EXCELLENT | 11 (38%) | 13 (42%) |

### Lista Completa (7 Categorias)

**AI AGENTS (WR-001 a WR-008):**
- WR-001: Accounting AI
- WR-002: Sales Tax AI
- WR-003: Project Management AI
- WR-004: Finance AI
- WR-005: Solutions Specialist
- WR-006: Customer Agent
- WR-007: Omni/Intuit Intelligence
- WR-008: Conversational BI

**REPORTING (WR-009 a WR-014):**
- WR-009: KPIs Customizados
- WR-010: Dashboards
- WR-011: 3P Data Integrations
- WR-012: Calculated Fields
- WR-013: Management Reports
- WR-014: Benchmarking

**DIMENSIONS (WR-015 a WR-019):**
- WR-015: Multi-Entity Reports
- WR-016: Dimension Assignment v2
- WR-017: Hierarchical Dimension Reporting
- WR-018: Dimensions on Workflow
- WR-019: Dimensions on Balance Sheet

**WORKFLOW (WR-020):**
- WR-020: Parallel Approval

**MIGRATION (WR-021 a WR-023):**
- WR-021: Seamless Desktop Migration
- WR-022: DFY Migration
- WR-023: Feature Compatibility (N/A - Documentacao)

**CONSTRUCTION (WR-024 a WR-025):**
- WR-024: Certified Payroll Report
- WR-025: Tech Stack Assessment

**PAYROLL (WR-026 a WR-029):**
- WR-026: Multi-Entity Payroll Hub
- WR-027: Garnishments Child Support
- WR-028: Assignments in QBTime
- WR-029: Enhanced Amendments (CA) - N/A

---

## 4.3 Gantt Chart - Post-Launch Winter Release 2026

### Estrutura (7 Phases + 2 Gates)
```
GATE 1: READINESS CONFIRMATION (Jan 02-06)
  - Environment Setup
  - CID Validation
  - Team Assignment

PHASE 2.1: FEATURE VALIDATION (Jan 20 - Feb 05)
  - AI AGENTS (Jan 20-30)
  - REPORTING (Jan 22 - Feb 03)
  - DIMENSIONS (Jan 27 - Feb 03)
  - WORKFLOW (Jan 29 - Feb 03)
  - MIGRATION (Jan 29 - Feb 04)
  - CONSTRUCTION (Jan 30 - Feb 04)
  - PAYROLL (Jan 31 - Feb 05)

PHASE 2.2: DATA & EVIDENCE PIPELINE (Feb 03-10)
PHASE 2.3: REVIEW & HANDOFF (Feb 10-14)
GATE 2: CUSTOMER APPROVAL (Feb 14-18)
PHASE 3: LAUNCH (Feb 18-25)
POST-LAUNCH: MONITORING (Feb 25+)
```

---

# PARTE 5: FRAMEWORK DE VALIDACAO

## 5.1 Principios Fundamentais

### PRINCIPIO 1: Screenshot DEVE provar a feature
- NAO aceitar homepage generica
- Pergunta: "Alguem olhando este screenshot entenderia a feature?"

### PRINCIPIO 2: Contexto correto e OBRIGATORIO
- Multi-entity = Consolidated View
- Regional = Tenant especifico (CA, Canada)

### PRINCIPIO 3: Ambiente determina disponibilidade
| Status | Significado |
|--------|-------------|
| PASS | Feature funciona como esperado |
| PARTIAL | Feature existe com limitacoes |
| NOT_AVAILABLE | Feature nao habilitada no ambiente |
| N/A | Feature e documentacao (sem UI) |

### PRINCIPIO 4: 404 = Investigar, nao aceitar
- Tentar navegacao alternativa
- Pesquisar documentacao
- Se nao existe: NOT_AVAILABLE com justificativa

### PRINCIPIO 5: Organizar por contexto
- Agrupar capturas pelo mesmo contexto
- Evitar troca frequente de empresa

---

## 5.2 Criterios de Qualidade de Screenshot

| Qualidade | Tamanho | Significado |
|-----------|---------|-------------|
| EXCELLENT | >= 250 KB | Conteudo completo |
| GOOD | 150-250 KB | Conteudo adequado |
| ACCEPTABLE | 100-150 KB | Conteudo minimo |
| WEAK | 50-100 KB | Provavelmente loading |
| INVALID | < 50 KB | Erro ou loading |
| ERROR_PAGE | ~139 KB | Pagina 404 |

---

## 5.3 Template de Evidence Notes

```
FEATURE: [WR-XXX] - [Nome]
AMBIENTE: [TCO/Construction/etc]
EMPRESA: [Nome da empresa no header]
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

# PARTE 6: TCO (TRACTION CONTROL OUTFITTERS)

## 6.1 Historia do Negocio (Ficticio)

**TCO** e uma empresa diversificada de pneus:
1. **Global Tread Distributors** - Wholesale (atacado)
2. **Apex Tire & Auto Retail** - Retail (varejo)
3. **RoadReady Service Solutions** - Servicos + Roadside 24/7

### Dados do Negocio
| Campo | Valor |
|-------|-------|
| Fundacao | 1998 |
| Sede | Dallas, TX |
| Funcionarios | 250 |
| Caixa Medio | $15-20M |
| Orcamento Anual | $250M |
| Fiscal Year End | 31 de Janeiro |

### Lideranca
| Nome | Cargo | Uso do IES |
|------|-------|-----------|
| Brooks | CEO | Multi-Entity Hub, AI Cash Flow |
| Lisa | CFO | AR/AP Consolidation, Intercompany |
| Jared | COO | Project Management, Job Costing |

---

## 6.2 Features IES que TCO Usa

| Feature | Para que serve |
|---------|---------------|
| Multi-Entity Hub | Ver todas empresas em um lugar |
| Consolidated P&L/BS | Relatorios consolidados |
| AI 13-week Cash Flow | Previsao de caixa |
| Finance Agent | Detecta anomalias |
| Payments Agent | Coleta mais rapida |
| Intercompany Allocations | Ratear custos compartilhados |
| Project Management Agent | Visao de projetos |

---

# PARTE 7: WFS (WORKFORCE SOLUTIONS)

## 7.1 O que e WFS

**Intuit Workforce Solutions** e uma plataforma HCM:
- **GoCo capabilities** - HR, onboarding, benefits
- **QuickBooks Payroll** - Folha de pagamento
- **MineralHR** - Compliance e documentos

### Timeline WFS
| Fase | Data | Customers |
|------|------|-----------|
| Alpha | Dez 2025 | ~100 |
| Beta | Fev 2026 | Expandido |
| GA | 1 Mai 2026 | Geral |

## 7.2 Demo Stories Prioritizadas

### Story A: Unified PTO
- **Flow:** Employee > Manager > Payroll Admin
- **Ambiente:** Keystone

### Story B: Magic Docs
- **Feature:** AI document generation + e-signature
- **Ambiente:** GoQuick (tem Intuit Intelligence BETA)

### Story C: Job Costing
- **Proof:** Labor cost attributed to project/job code
- **Ambiente:** Keystone Construction

---

# PARTE 8: RISCOS E BLOCKERS

## 8.1 Riscos Estrategicos Ativos

| # | Risco | Prioridade | Status |
|---|-------|------------|--------|
| 1 | Test Users para clone environments | **P0** | PENDING |
| 2 | IC Balance Sheet bug | P1 | Escalado (PLA-3201) |
| 3 | Login ECS Task Failing | P1 | PLA-3013 |
| 4 | Timeline GTM vs Eng desalinhado | P0 | In progress |

## 8.2 Blockers Linear (Ativos)

| Issue | Titulo | Assignee |
|-------|--------|----------|
| PLA-3201 | IC Balance Sheet Consolidated View | Engineering |
| PLA-3013 | Login task failing TCO | Augusto Gunsch |
| PLA-2969 | Canada Data Ingest Bills | Lucas Torresan |

## 8.3 Tickets Winter Release Criados

| Ticket | Descricao |
|--------|-----------|
| PLA-3212 | Construction Clone (8 CIDs) |
| PLA-3213 | TCO Clone (4 CIDs) |

---

# PARTE 9: BASE DE DADOS POSTGRESQL

## 9.1 Conexao

| Parametro | Valor |
|-----------|-------|
| Host | tbx-postgres-staging.internal |
| Port | 5433 |
| Database | unstable |
| User | unstable |
| Acesso | Via Tailscale VPN |

## 9.2 Estrutura

- **74 tabelas** quickbooks_*
- **172.57 MB** tamanho total
- **~178k registros** aproximado

## 9.3 Top 10 Tabelas

| Tabela | Tamanho | Rows |
|--------|---------|------|
| quickbooks_invoice_line_item_classifications | 64.93 MB | 776k+ |
| quickbooks_invoices | 30.94 MB | 44k+ |
| quickbooks_invoice_line_items | 27.19 MB | 115k |
| quickbooks_time_entries | 22.19 MB | 62k |
| quickbooks_customers | 10.45 MB | 10k |
| quickbooks_bills | 1.86 MB | 4.7k |
| quickbooks_employees | 1.43 MB | 1.6k |

---

# PARTE 10: CORTEX SYSTEM

## 10.1 Estrutura do Cortex

```
knowledge-base/
├── slack-cortex/     <- Comunicacao (10 canais)
├── drive-cortex/     <- Documentos (20,426 -> 1,926)
├── strategic-cortex/ <- Consolidado (5 outputs)
```

## 10.2 Os 5 Outputs do Strategic Cortex

| Output | Arquivo | Uso |
|--------|---------|-----|
| A | OUTPUT_A_EXECUTIVE_SNAPSHOT.md | Status rapido - **LER PRIMEIRO** |
| B | OUTPUT_B_STRATEGIC_MAP.md | Conexoes e arquitetura |
| C | OUTPUT_C_KNOWLEDGE_BASE.json | Dados estruturados |
| D | OUTPUT_D_KEYWORD_MAP_LINEAR_RECIPES.md | Busca rapida |
| E | OUTPUT_E_DELTA_SUMMARY.md | Mudancas recentes |

## 10.3 Metricas de Visibilidade

| Fonte | Total | Relevantes |
|-------|-------|------------|
| Google Drive | 20,426 | 1,926 (9.4%) |
| Linear | 1,546 | 443 Intuit (28.7%) |
| Slack | 10 canais | Coletado |

---

# PARTE 11: ULTIMAS SESSOES E ACOES

## 11.1 Sessao Mais Recente: 2026-01-20

**Trabalho Realizado:**
- Winter Release Gantt v9 Final criado (29 features, 7 categorias)
- IC Balance Sheet Investigation - Bug identificado e escalado (PLA-3201)
- Google Sheets integration via gspread
- Auditoria completa (10 issues, 44 warnings)

**Arquivos Criados:**
- `create_post_launch_gantt_v9_FINAL.py`
- `POST_LAUNCH_WINTER_RELEASE_2026_GSHEETS.xlsx`
- `FEATURE_VALIDATION_CONSOLIDATED.xlsx`

## 11.2 Historico de Sessoes

| Data | Foco | Resultado |
|------|------|-----------|
| 2026-01-20 | Gantt v9 + IC Investigation | Bug escalado, Gantt criado |
| 2026-01-12 | Validation Matrix v4 | Matrix completa |
| 2026-01-07 | Guia Canonico | Documentacao completa |
| 2025-12-29 | Winter Release Validation | 100% PASS TCO, 86% Construction |

---

# PARTE 12: DECISOES IMPORTANTES

| Data | Decisao | Owner | Por que Importa |
|------|---------|-------|-----------------|
| 2025-12-22 | Fall Release = process improvement | Katherine | Reclassifica como manutencao |
| 2025-12-17 | GoQuick Alpha != sales demo | Katherine | Evita confusao ambiente WFS |
| 2025-12-15 | Staged rollout WFS obrigatorio | Katherine | Protege sellers existentes |
| 2025-12-06 | Sistema de camadas LOCKED/OPEN | Rafael | Protege codigo estavel |
| 2025-12-06 | layer1_login.py standalone | Rafael | Reutilizacao multi-projeto |

---

# PARTE 13: CONTATOS E STAKEHOLDERS

## 13.1 TestBox

| Nome | Papel |
|------|-------|
| **Thiago Rodrigues** | TSA Lead, Data Architect, Owner deste projeto |
| Katherine Lu | Program Lead, SOW |
| Sam Senior | CEO |

## 13.2 Intuit

| Nome | Papel |
|------|-------|
| Lawton Ursrey | Product Leader |
| Ben Hale | Sales Enablement (WFS) |
| Kat (Katherine Lu) | Account Lead |
| Christina Duarte | Decision owner (environment) |

## 13.3 Equipe TSA (reporta para Thiago)

| Pessoa | Foco Atual |
|--------|------------|
| Diego | Brevo, CallRail, People.ai |
| Gabrielle | Dixa, Zendesk, Mailchimp |
| Carlos | Apollo, Gong |
| Alexandra | mParticle, Syncari, WFS |

---

# PARTE 14: PROTOCOLO DE SESSAO

## 14.1 Ao Iniciar Sessao

1. **Ler `.claude/memory.md`** - Recuperar estado persistente
2. **Verificar `sessions/`** - Ultimas sessoes
3. **Consultar `knowledge-base/strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md`** - Status atual
4. **Verificar `LAYERS.md`** - Camadas protegidas

## 14.2 Durante o Trabalho

- Verificar LAYERS.md antes de editar qualquer arquivo
- Se camada LOCKED: PARAR e perguntar
- Documentar decisoes importantes

## 14.3 Ao Finalizar Sessao

1. **Executar `/consolidar`** - Salvar aprendizados
2. **Atualizar memory.md** - Estado atual
3. **Criar arquivo de sessao** - Historico
4. **Commit e push para Git** - Versionamento

---

# PARTE 15: GLOSSARIO

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
| **TSA** | Technical Solutions Architect |
| **SOW** | Statement of Work |
| **UAT** | User Acceptance Testing |
| **Early Access** | Acesso antecipado a features |
| **GA** | General Availability |
| **TOTP** | Time-based One-Time Password |
| **SpineHUB** | Sistema de memoria persistente |
| **Cortex** | Sistema de inteligencia consolidada |

---

# PARTE 16: CHECKLIST PARA NOVA IA

## Antes de Qualquer Trabalho

- [ ] Ler este documento COMPLETO
- [ ] Acessar `.claude/memory.md`
- [ ] Verificar `sessions/` para historico recente
- [ ] Consultar `knowledge-base/INDEX.md`
- [ ] Verificar LAYERS.md (camadas protegidas)

## Para Validacao de Features

- [ ] Confirmar qual ambiente usar (TCO vs Construction)
- [ ] Verificar se feature requer contexto especial
- [ ] Usar UNIVERSAL_VALIDATION_FRAMEWORK.md
- [ ] Esperar 30-60 segundos antes de screenshot
- [ ] Validar tamanho do arquivo (>100KB)

## Para Acesso ao QBO

- [ ] Chrome com CDP na porta 9222
- [ ] Usar layer1_login.py ou login manual
- [ ] Verificar empresa correta no header

## Ao Finalizar Trabalho

- [ ] Executar `/consolidar`
- [ ] Atualizar memory.md
- [ ] Criar arquivo de sessao

---

# PARTE 17: ARQUIVOS CRITICOS

| Arquivo | Funcao | Quando Ler |
|---------|--------|------------|
| `CLAUDE.md` | Instrucoes gerais | **SEMPRE no inicio** |
| `.claude/memory.md` | Estado persistente | **SEMPRE no inicio** |
| `LAYERS.md` | Camadas protegidas | Antes de editar |
| `GUIA_CANONICO_INTUIT_QBO.md` | Documentacao completa | Para consulta |
| `knowledge-base/INDEX.md` | Catalogo de fontes | Para busca |
| `strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md` | Status atual | Para contexto |
| `layer1_login.py` | Script de login | LOCKED - nao editar |
| `qbo_checker/features_winter.json` | Features Winter | Para validacao |
| `qbo_checker/FEATURE_VALIDATION_CANON.json` | Regras canonicas | Para validacao |

---

**FIM DO DOCUMENTO**

*Gerado por Claude Code em 2026-01-23*
*Projeto: INTUIT-BOOM (Score 92/100)*
*Fontes: SpineHUB + Strategic Cortex + Memory Files + Sessions*
*Total de linhas consolidadas: ~1,500*
