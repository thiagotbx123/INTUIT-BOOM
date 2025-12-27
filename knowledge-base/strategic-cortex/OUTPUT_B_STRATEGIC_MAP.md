# OUTPUT B - Mapa Estrategico do Projeto

> Conexoes entre estrategia, requisitos, datasets, ingest, ambientes e validacao
> Generated: 2025-12-27 00:25 America/Sao_Paulo
> Todas as conexoes possuem ponteiros para evidencia

---

## 1. ESTRATEGIA DO CLIENTE E DA TESTBOX

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INTUIT STRATEGY                               │
├─────────────────────────────────────────────────────────────────────┤
│ OBJETIVO: Demonstrar valor do QuickBooks e WFS para prospects       │
│                                                                      │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│ │  QBO/IES     │  │     WFS      │  │   Verticais  │                │
│ │  (Atual)     │  │  (Novo 2026) │  │  (Expansao)  │                │
│ └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                │
│        │                 │                 │                         │
│        ▼                 ▼                 ▼                         │
│   Fall Release      Alpha/Beta/GA     Canada, Construction          │
│   Nov 2025          Dez 25-Mai 26     Manufacturing                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       TESTBOX STRATEGY                               │
├─────────────────────────────────────────────────────────────────────┤
│ OBJETIVO: Ser plataforma de demo preferida para Intuit sellers      │
│                                                                      │
│ Pilares:                                                            │
│ 1. Ambientes realistas (TCO, Construction, Canada)                  │
│ 2. Datasets de alta qualidade (validados, sem bugs)                 │
│ 3. Ingest automatizado e confiavel                                  │
│ 4. Health checks e monitoramento                                    │
│                                                                      │
│ Evidencia: TestBox 3.0 doc, SOW drafts, Health Check Checklist      │
└─────────────────────────────────────────────────────────────────────┘
```

### Documentos Chave - Estrategia
| Documento | Link | Role |
|-----------|------|------|
| TestBox 3.0 | [Drive](https://docs.google.com/document/d/1mhC8gg3rDuRMrPBa5573wSGmaDpayZogg3CgagPqQn8/edit) | Product roadmap |
| WFS HCM Transformation FY26 | [Drive](https://docs.google.com/presentation/d/1w91J8oiSfgWB-V_O60uDaPfXRDwmB5NHaI53dsqoBLk/edit) | Intuit roadmap |
| WFS_TSA_SCOPE_PLAN.xlsx | [Drive](https://docs.google.com/spreadsheets/d/19kAAYS3ppGra7GtsU2wOhwTKHE2J1oQk/edit) | Scope planning |

---

## 2. REQUISITOS E ESCOPO

```
┌─────────────────────────────────────────────────────────────────────┐
│                      REQUISITOS POR PROJETO                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ WFS (Novo)                                                   │    │
│  │ ├─ Worker Profile V1                                         │    │
│  │ ├─ Time Off V1 (PTO: Sick, Vacation, Personal)              │    │
│  │ ├─ Onboarding V1 (Digital I-9, Offer Letter)                │    │
│  │ ├─ Manager Role V1                                           │    │
│  │ ├─ MineralHR Integration                                     │    │
│  │ └─ GoCo Platform Features                                    │    │
│  │                                                               │    │
│  │ Evidencia: GoCo Platform Comprehensive Feature List          │    │
│  │            Testbox - SOW - Intuit WFS v1.1                   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ QBO/IES (Atual)                                              │    │
│  │ ├─ Payments Agent                                            │    │
│  │ ├─ Finance Agent                                             │    │
│  │ ├─ Accounting Agent                                          │    │
│  │ ├─ Shared Chart of Accounts                                  │    │
│  │ ├─ Intercompany Allocations                                  │    │
│  │ ├─ KPI Library / Custom KPIs                                 │    │
│  │ └─ Dashboard Enhancements                                    │    │
│  │                                                               │    │
│  │ Evidencia: Fall Release Tracker, Big Numbers deck            │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Documentos Chave - Requisitos
| Documento | Link | Role |
|-----------|------|------|
| Testbox - SOW - Intuit WFS v1.1 | [Drive](https://docs.google.com/document/d/1h-vDGqmJRlJsndobYq9cXlrv18bEc5S0TT4GLBT9Qt0/edit) | WFS scope |
| GoCo Platform Feature List | [Drive](https://docs.google.com/spreadsheets/d/1wVgrO7wzsorGlxKiqjUy_bZFcXwZeKN-5QBql1MLEuo/edit) | Feature requirements |
| Fall Release Tracker | Drive | QBO features |

---

## 3. DATASETS E NARRATIVA DO DEMO

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATASET UNIVERSE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────┐                        │
│  │ TCO (Traction Control Outfitters)       │ ◄── Multi-entity       │
│  │ ├─ Parent Company                        │                        │
│  │ ├─ Apex Tire (Southwest)                │                        │
│  │ ├─ Global Tread (Distribution)          │                        │
│  │ └─ RoadReady (Fleet Services)           │                        │
│  │                                          │                        │
│  │ Narrativa: Fleet management + tire retail│                        │
│  │ Volume: High (10k+ customers)            │                        │
│  │ Status: ACTIVE, negative inventory bug   │                        │
│  └─────────────────────────────────────────┘                        │
│                                                                      │
│  ┌─────────────────────────────────────────┐                        │
│  │ Construction Sales                       │ ◄── IES                │
│  │ ├─ Keystone Construction (priority)     │                        │
│  │ ├─ Job Costing                          │                        │
│  │ └─ Progress Invoicing                   │                        │
│  │                                          │                        │
│  │ Narrativa: Construction company workflow │                        │
│  │ Status: ACTIVE                           │                        │
│  └─────────────────────────────────────────┘                        │
│                                                                      │
│  ┌─────────────────────────────────────────┐                        │
│  │ Canada Construction                      │                        │
│  │ ├─ Dataset ID: 2ed5d245-0578-43aa-...   │                        │
│  │ ├─ Provinces: ON, BC, AB, QC, etc.      │                        │
│  │ └─ Tax: GST/PST/HST                     │                        │
│  │                                          │                        │
│  │ Narrativa: Canadian market               │                        │
│  │ Status: ACTIVE                           │                        │
│  └─────────────────────────────────────────┘                        │
│                                                                      │
│  ┌─────────────────────────────────────────┐                        │
│  │ Manufacturing                            │ ◄── LOW VISIBILITY    │
│  │ ├─ Inventory, BOM, Assembly             │                        │
│  │ └─ Status: UNKNOWN (6 files only)       │                        │
│  └─────────────────────────────────────────┘                        │
│                                                                      │
│  ┌─────────────────────────────────────────┐                        │
│  │ WFS / GoQuick Alpha Retail              │ ◄── NOVO               │
│  │ ├─ Realm ID: 9341455848423964           │                        │
│  │ ├─ Billing Plan: PR_ELITE               │                        │
│  │ └─ MineralHR Integration                │                        │
│  │                                          │                        │
│  │ Narrativa: HR/Payroll demo               │                        │
│  │ Status: EXPLORATION (not sales demo)    │                        │
│  └─────────────────────────────────────────┘                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Documentos Chave - Datasets
| Documento | Link | Role |
|-----------|------|------|
| Datasets inventory | Drive CSVs | Data definitions |
| TCO Core Requirements | Tracker | TCO specifics |
| Canada Construction dataset | Drive | Canada data |

---

## 4. INGEST E ARQUITETURA

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INGEST ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐   │
│  │  Source  │────▶│ Pipeline │────▶│ Validate │────▶│   QBO    │   │
│  │  (CSV/   │     │ (ECS)    │     │ (Hasura/ │     │ (Demo    │   │
│  │   API)   │     │          │     │  Dynamo) │     │  Env)    │   │
│  └──────────┘     └──────────┘     └──────────┘     └──────────┘   │
│       │                │                │                │          │
│       │                │                │                │          │
│       ▼                ▼                ▼                ▼          │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐   │
│  │ Datasets │     │ Logging  │     │ Health   │     │ Retool   │   │
│  │ (Drive)  │     │ (Cloud   │     │ Check    │     │ (Admin)  │   │
│  │          │     │  Watch)  │     │          │     │          │   │
│  └──────────┘     └──────────┘     └──────────┘     └──────────┘   │
│                                                                      │
│  Componentes:                                                       │
│  ├─ ECS Tasks: Login, Ingest, Sync                                  │
│  ├─ Hasura: GraphQL API                                             │
│  ├─ DynamoDB: Estado e validacoes                                   │
│  ├─ Retool: Admin interface                                         │
│  └─ CloudWatch: Logging e alertas                                   │
│                                                                      │
│  Issues Conhecidos:                                                 │
│  ├─ Login ECS Task failing (workaround: manual)                     │
│  ├─ Negative inventory (PLA-2916)                                   │
│  └─ Validator timeouts em datasets grandes                          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Documentos Chave - Ingest
| Documento | Link | Role |
|-----------|------|------|
| MCP_QuickBooks_Spike_.xlsx | Drive | API integration |
| Data Ingest tickets | Linear | Implementation |
| Runbooks | Drive | Operations |

---

## 5. AMBIENTES E HEALTH CHECKS

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ENVIRONMENT MAP                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ PRODUCTION ENVIRONMENTS (Sellers)                            │    │
│  │                                                               │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │    │
│  │  │   TCO    │  │ Constr.  │  │  Canada  │  │ Non-Prof │     │    │
│  │  │   OK     │  │   OK     │  │   OK     │  │   95%    │     │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │    │
│  │                                                               │    │
│  │  ┌──────────┐  ┌──────────┐                                  │    │
│  │  │ Manufac. │  │   WFS    │ ◄── PENDING (not sales demo)    │    │
│  │  │  95%     │  │ PENDING  │                                  │    │
│  │  └──────────┘  └──────────┘                                  │    │
│  │                                                               │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ EXPLORATION/DEV ENVIRONMENTS                                 │    │
│  │                                                               │    │
│  │  ┌──────────────────┐  ┌──────────────────┐                  │    │
│  │  │ GoQuick Alpha    │  │ TestBox Staging  │                  │    │
│  │  │ Retail (WFS)     │  │ (Engineering)    │                  │    │
│  │  │ Realm: 9341...   │  │ Shared           │                  │    │
│  │  └──────────────────┘  └──────────────────┘                  │    │
│  │                                                               │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  HEALTH CHECK PROCESS:                                              │
│  1. Data Validator (Hasura/Dynamo)                                  │
│  2. QBO_Health_Check_Checklist_TCO_v2.xlsx                         │
│  3. Manual spot checks                                              │
│  4. Selenium/automation tests                                       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Documentos Chave - Environments
| Documento | Link | Role |
|-----------|------|------|
| QBO_Health_Check_Checklist_TCO_v2.xlsx | Drive | Health check |
| Fall Readiness Environment CIDs | Drive | Environment IDs |
| QBO_Health_Check_Presentation.pptx | Drive | Overview |

---

## 6. VALIDACAO E EVIDENCIAS

```
┌─────────────────────────────────────────────────────────────────────┐
│                       VALIDATION FRAMEWORK                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ VALIDATION LAYERS                                            │    │
│  │                                                               │    │
│  │  Layer 1: Data Integrity                                     │    │
│  │  ├─ assert_data_err (dynamic reporting)                      │    │
│  │  ├─ Type hints enforcement (GitHub pipeline)                 │    │
│  │  └─ Negative stock prevention (PLA-2916)                     │    │
│  │                                                               │    │
│  │  Layer 2: Feature Validation                                 │    │
│  │  ├─ Fall Release Tracker (spreadsheet)                       │    │
│  │  ├─ UAT evidence (screenshots)                               │    │
│  │  └─ Manual spot checks                                       │    │
│  │                                                               │    │
│  │  Layer 3: Environment Health                                 │    │
│  │  ├─ Health Check Checklist (TCO v2)                         │    │
│  │  ├─ Consolidated view validation                             │    │
│  │  └─ Multi-entity balance checks                              │    │
│  │                                                               │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  EVIDENCE COLLECTION:                                               │
│  ├─ Screenshots (Drive)                                             │
│  ├─ Tracker spreadsheets                                            │
│  ├─ Slack threads                                                   │
│  └─ Linear tickets                                                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. RISCOS E TRADEOFFS

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RISK MATRIX                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│             │ Low Impact  │ Medium Impact │ High Impact             │
│  ───────────┼─────────────┼───────────────┼─────────────            │
│  High       │             │ Fusion UI     │ WFS Env     │            │
│  Likelihood │             │ Delays        │ Decision    │            │
│  ───────────┼─────────────┼───────────────┼─────────────            │
│  Medium     │ Manufacturing│ Login ECS    │ Negative    │            │
│  Likelihood │ Visibility  │ Failure       │ Inventory   │            │
│  ───────────┼─────────────┼───────────────┼─────────────            │
│  Low        │ Winter      │ SOW          │             │            │
│  Likelihood │ Planning    │ Delays       │             │            │
│  ───────────┴─────────────┴───────────────┴─────────────            │
│                                                                      │
│  TRADEOFFS ATIVOS:                                                  │
│                                                                      │
│  1. Speed vs Quality (WFS)                                          │
│     ├─ Trade: Entregar Alpha com features limitadas                 │
│     └─ Risk: Feedback negativo de sellers                           │
│                                                                      │
│  2. Automation vs Manual (Login)                                    │
│     ├─ Trade: Manual login como workaround                          │
│     └─ Risk: Nao escalavel                                          │
│                                                                      │
│  3. Staged vs Big Bang (WFS Rollout)                               │
│     ├─ Trade: Staged para proteger sellers existentes               │
│     └─ Risk: Timeline mais longa                                    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## CONEXOES ENTRE CAMADAS

```
ESTRATEGIA ──────────────────────────────────────────────────────────┐
    │                                                                 │
    ▼                                                                 │
REQUISITOS ──► WFS Alpha Features                                    │
    │          QBO Fall Release                                       │
    ▼                                                                 │
DATASETS ────► TCO (multi-entity)                                    │
    │          Construction (Keystone)                                │
    │          Canada (GST/PST)                                       │
    │          WFS (GoQuick Alpha)                                    │
    ▼                                                                 │
INGEST ──────► ECS Pipeline                                          │
    │          Hasura Validation                                      │
    │          DynamoDB State                                         │
    ▼                                                                 │
ENVIRONMENTS ► TCO, Construction, Canada (PROD)                      │
    │          GoQuick Alpha (DEV)                                    │
    │          Staging (SHARED)                                       │
    ▼                                                                 │
VALIDATION ──► Health Check Checklist                                │
    │          Fall Release Tracker                                   │
    │          UAT Evidence                                           │
    ▼                                                                 │
EVIDENCIA ───► Drive (docs, sheets, pdfs)                            │
               Slack (decisions, discussions)                         │
               Linear (tickets, status)                               │
└────────────────────────────────────────────────────────────────────┘
```

---

Documento gerado automaticamente
Fonte: Google Drive (20,426 arquivos), Slack (10 canais)
Linear: Sem acesso direto
