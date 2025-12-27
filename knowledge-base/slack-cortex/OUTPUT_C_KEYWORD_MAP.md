# OUTPUT C - Keyword Map e Slack Search Recipes

> Mapeamento de termos e queries prontas para busca no Slack
> Gerado: 2025-12-26

---

## KEYWORD FREQUENCY MAP

### Tier 1 - Alta Frequencia (50+ mencoes)
| Keyword | Contexto | Canais Principais |
|---------|----------|-------------------|
| `TCO` | Ambiente multi-entity, Traction Control Outfitters | C06PSSGEK8T, D09GQC60JBC |
| `Fall Release` | Release Nov 2025, deadline 11/20 | C09QC6096G7, D09N49AG4TV |
| `WFS` | Workforce Solutions, HCM platform | D09N49AG4TV, C06PSSGEK8T |
| `environment` | Demo environments, staging | Todos |
| `dataset` | Dados de demo, ingestao | C06PSSGEK8T, D09GQC60JBC |

### Tier 2 - Media Frequencia (20-49 mencoes)
| Keyword | Contexto | Canais Principais |
|---------|----------|-------------------|
| `Construction` | Construction Sales, Keystone | C06PSSGEK8T, C09DKMB4NAE |
| `Intuit` | Cliente, stakeholder | Todos |
| `Canada` | Datasets canadenses | C09DKMB4NAE, C0762U2S3JN |
| `staging` | Ambiente de dev | C0762U2S3JN |
| `SOW` | Statement of Work | D09N49AG4TV |
| `login` | Login issues, automation | C0762U2S3JN, C072MQDJRJS |
| `Manufacturing` | Dataset manufacturing | C06PSSGEK8T |
| `MineralHR` | HR compliance integration | D09N49AG4TV |
| `Alpha` | WFS Alpha phase | D09N49AG4TV |

### Tier 3 - Baixa Frequencia (10-19 mencoes)
| Keyword | Contexto | Canais Principais |
|---------|----------|-------------------|
| `Fusion` | Fusion UI migration | C09SGBFBC02 |
| `negative inventory` | Bug TCO products | C06PSSGEK8T |
| `Keystone` | Keystone Construction (priority) | C06PSSGEK8T |
| `validator` | Data validator | C0762U2S3JN |
| `captcha` | Login captcha issues | C072MQDJRJS |
| `Apex Tire` | TCO child entity | C06PSSGEK8T |
| `GoCo` | HR platform | D09N49AG4TV |
| `PSC` | Professional Services | C091ZCL7371 |
| `rollout` | Deployment planning | D09N49AG4TV |
| `deadline` | Delivery dates | C09QC6096G7, D09N49AG4TV |

---

## SEARCH RECIPES

### 1. Status de Projetos

```
# Fall Release status
in:#intuit-quickbooks-testbox Fall Release status

# WFS progress
in:#wfs-testbox WFS OR "Workforce Solutions"

# TCO environment issues
TCO environment OR staging OR login
```

### 2. Blockers e Issues

```
# Bugs e blockers ativos
blocker OR blocked OR issue OR bug

# Negative inventory especifico
"negative inventory" OR "negative stock"

# Login problems
login OR captcha OR "ECS task"
```

### 3. Decisoes e Alinhamentos

```
# Decisoes documentadas
from:@katherine decision OR decided OR confirmed

# Alinhamentos com Intuit
from:@thiago Intuit OR Lawton OR Jason

# SOW discussions
SOW OR "Statement of Work" OR scope
```

### 4. Timelines e Deadlines

```
# Deadlines
deadline OR "due date" OR ETA

# Release timelines
"Fall Release" OR "Winter Release" deadline

# WFS timeline
WFS Alpha OR Beta OR GA 2026
```

### 5. Ambientes e Datasets

```
# Dataset info
dataset OR ingest OR ingestion

# Environment status
environment status OR health

# Canada specific
Canada dataset OR construction
```

### 6. Pessoas e Atribuicoes

```
# O que Thiago esta fazendo
from:@thiago

# Updates da Katherine
from:@katherine update OR status

# Engineering discussions
from:@lucassoranzo OR from:@eyji OR from:@marcelo
```

### 7. Integracao e APIs

```
# API issues
API OR integration OR captcha

# MineralHR
MineralHR OR Mineral OR "HR advisor"

# GoCo features
GoCo OR "worker profile" OR onboarding
```

---

## SEMANTIC CLUSTERS

### Cluster: Environment Health
```
Keywords: environment, health, staging, production, demo, data, validator
Query: (environment OR staging) AND (health OR status OR issue)
```

### Cluster: Release Management
```
Keywords: release, deadline, delivery, UAT, testing, validation
Query: (Fall Release OR Winter Release) AND (deadline OR status OR delivered)
```

### Cluster: WFS Implementation
```
Keywords: WFS, Workforce, HCM, payroll, HR, benefits, GoCo, Mineral
Query: WFS AND (SOW OR scope OR implementation OR Alpha OR Beta)
```

### Cluster: Data Operations
```
Keywords: dataset, ingest, ingestion, data, validator, negative, inventory
Query: (dataset OR ingest) AND (status OR issue OR update)
```

### Cluster: Engineering
```
Keywords: staging, PR, deploy, code, fix, bug, ECS, task
Query: staging AND (use OR available OR blocked)
```

---

## CHANNEL-SPECIFIC RECIPES

### C06PSSGEK8T (Main Intuit Channel)
```
in:C06PSSGEK8T Fall Release
in:C06PSSGEK8T TCO status
in:C06PSSGEK8T dataset update
```

### D09N49AG4TV (Thiago-Katherine DM)
```
in:D09N49AG4TV WFS SOW
in:D09N49AG4TV deadline
in:D09N49AG4TV feedback
```

### C0762U2S3JN (Engineering Staging)
```
in:C0762U2S3JN staging
in:C0762U2S3JN review OR PR
in:C0762U2S3JN login OR captcha
```

### C09QC6096G7 (Fall Release)
```
in:C09QC6096G7 delivery
in:C09QC6096G7 blocker
in:C09QC6096G7 UAT
```

---

## ENTITY ALIASES

Para melhorar buscas, considerar sinonimos:

| Entidade | Aliases |
|----------|---------|
| TCO | "Traction Control", "multi-entity", "parent company" |
| WFS | "Workforce Solutions", "HCM", "workforce" |
| Construction | "Keystone", "construction sales", "IES" |
| Canada | "Canadian", "canada_construction" |
| Fall Release | "Nov release", "11/20", "November deadline" |
| Winter Release | "Feb release", "February 2026" |
| MineralHR | "Mineral", "HR advisor", "HR compliance" |
| GoCo | "worker profile", "employee app" |
| Staging | "dev environment", "test environment" |

---

## ADVANCED QUERIES

### Ultimos 7 dias de uma pessoa
```
from:@thiago after:2025-12-19
```

### Threads com muita atividade
```
has:thread after:2025-12-01
```

### Mensagens com arquivos/links
```
has:link after:2025-12-01 in:#intuit-quickbooks-testbox
```

### Busca por data especifica
```
on:2025-11-20 Fall Release
on:2025-12-15 WFS
```

---

## MONITORING QUERIES (Recomendado)

Queries para monitoramento continuo:

| Query | Frequencia | Proposito |
|-------|------------|-----------|
| `blocker OR blocked` | Diario | Detectar novos blockers |
| `deadline` | Diario | Tracking de prazos |
| `from:@katherine decision` | Semanal | Novas decisoes |
| `WFS AND (update OR status)` | Semanal | Progress WFS |
| `staging AND (down OR issue)` | Diario | Health staging |

---

Documento gerado para consumo por Slack Cortex
Fonte: Analise de 180 dias de mensagens
Canais: 10 monitorados
