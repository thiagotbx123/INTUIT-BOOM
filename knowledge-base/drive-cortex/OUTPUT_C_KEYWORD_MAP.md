# OUTPUT C - Keyword Map (Drive Cortex)

> Mapeamento de termos e queries para busca no Drive e Slack
> Gerado: 2025-12-27

---

## KEYWORD FREQUENCY (Do Inventario Drive)

### Tier 1 - Alta Frequencia (100+ arquivos)
| Keyword | Arquivos | Temas Principais |
|---------|----------|------------------|
| `tco` | 421 | Ambiente TCO, Tire, Fleet |
| `quickbooks` | 415 | QBO, Contratos, Releases |
| `testbox` | 350+ | Plataforma, Integracao |
| `intuit` | 300+ | Cliente, Todos projetos |
| `sow` | 149 | Contratos, Scope |

### Tier 2 - Media Frequencia (20-99 arquivos)
| Keyword | Arquivos | Temas Principais |
|---------|----------|------------------|
| `wfs` | 61 | Workforce Solutions, HCM |
| `dataset` | 41 | Dados, Ingestao |
| `construction` | 29 | Keystone, IES |
| `fall release` | 19 | Release Nov 2025 |
| `canada` | 19 | Datasets canadenses |

### Tier 3 - Baixa Frequencia (5-19 arquivos)
| Keyword | Arquivos | Temas Principais |
|---------|----------|------------------|
| `goco` | 7 | Plataforma HR |
| `mineral` | 5 | MineralHR |
| `alpha` | 10+ | WFS Alpha phase |
| `keystone` | 8 | Construction customer |

---

## LEXICO EXPANDIDO POR TEMA

### WFS / Workforce Solutions
```
Termos primarios:
- wfs, workforce, workforce solutions
- hcm, human capital management
- goco, mineral, mineralhr
- payroll, hr, benefits, time

Termos secundarios:
- onboarding, offboarding
- worker profile, employee
- time off, pto, vacation
- digital i9, w4
- effective dating
- manager role, admin
```

### QuickBooks / QBO
```
Termos primarios:
- quickbooks, qbo, qboa
- intuit, ies
- advanced, payroll elite

Termos secundarios:
- chart of accounts, coa
- class, location, dimension
- p&l, profit and loss
- balance sheet
- consolidated view
- multi entity
```

### Datasets e Ingestao
```
Termos primarios:
- dataset, data set, massa
- ingest, ingestao, reingest
- sync, pipeline, validator

Termos secundarios:
- seed, snapshot, refresh
- golden environment
- data dictionary
- mapping, rules
```

### Releases
```
Termos primarios:
- fall release, winter release
- uat, tracker
- feature flag, rollout

Termos secundarios:
- alpha, beta, ga
- evidence, screenshot
- regression
```

### Contratos
```
Termos primarios:
- sow, statement of work
- proposal, scope
- contract, agreement

Termos secundarios:
- assumptions, out of scope
- change control, pricing
- entregaveis, deliverables
```

---

## SEARCH RECIPES - GOOGLE DRIVE

### Buscar SOWs e Contratos
```
# SOW de qualquer cliente
"SOW" OR "Statement of Work" type:document

# SOW WFS especifico
"Workforce Solutions" "SOW" type:document

# Contratos assinados
"signed" OR "assinado" type:pdf

# Propostas
"proposal" OR "proposta" type:document
```

### Buscar Datasets e Dados
```
# Datasets gerais
"dataset" OR "data set" type:spreadsheet

# Arquivos de ingestao
"ingest" OR "ingestao" type:spreadsheet

# CSVs de dados
type:csv "customer" OR "product" OR "invoice"

# Mappings
"mapping" OR "schema" type:spreadsheet
```

### Buscar por Projeto
```
# WFS
"WFS" OR "Workforce" owner:me

# TCO
"TCO" OR "Tire" OR "Traction Control"

# Construction
"Construction" OR "Keystone"

# Canada
"Canada" OR "Canadian" type:spreadsheet
```

### Buscar por Periodo
```
# Ultimos 30 dias
modifieddate:today-30d

# Dezembro 2025
modifieddate:2025-12-01..2025-12-31

# Fall Release period
modifieddate:2025-10-01..2025-11-30 "fall release"
```

### Buscar por Tipo
```
# Apresentacoes
type:presentation "intuit" OR "quickbooks"

# Planilhas de tracking
type:spreadsheet "tracker" OR "tracking"

# PDFs (manuais, contratos)
type:pdf "quickbooks" OR "user manual"

# Meeting notes
"meeting notes" OR "notes" type:document
```

---

## SEARCH RECIPES - SLACK

### Buscar Decisoes
```
# Decisoes de Katherine
from:@katherine decision OR decided OR confirmed

# Decisoes sobre WFS
WFS AND (decision OR decided)

# Decisoes sobre scope
scope AND (approved OR rejected OR changed)
```

### Buscar Blockers
```
# Blockers ativos
blocker OR blocked OR issue OR bug

# Problemas de ambiente
environment AND (down OR issue OR error)

# Problemas de login
login OR captcha OR "ECS task"
```

### Buscar por Projeto
```
# WFS discussions
in:#testbox-intuit-wfs WFS OR "Workforce"

# TCO environment
TCO environment OR health

# Fall Release
"Fall Release" AND (status OR tracker OR deadline)
```

### Buscar Arquivos Compartilhados
```
# Links do Drive
has:link "drive.google.com"

# Arquivos anexados
has:file

# Sheets compartilhados
has:link "docs.google.com/spreadsheets"
```

### Buscar por Periodo
```
# Ultimos 7 dias
after:2025-12-20

# Dezembro
after:2025-12-01 before:2025-12-31

# Data especifica
on:2025-11-20 "Fall Release"
```

---

## ALIASES E SINONIMOS

| Termo Principal | Aliases |
|-----------------|---------|
| TCO | Traction Control Outfitters, tire shop, fleet |
| WFS | Workforce Solutions, HCM, workforce |
| Construction | Keystone, construction sales, IES |
| GoCo | goco platform, hr platform |
| MineralHR | Mineral, HR advisor, HR compliance |
| Fall Release | Nov release, 11/20, November deadline |
| SOW | Statement of Work, escopo, scope document |
| Dataset | massa de dados, dados sinteticos, seed |
| Ingest | ingestao, data pipeline, sync |
| UAT | User Acceptance Testing, validation |

---

## QUERIES COMPOSTAS RECOMENDADAS

### Para Reunioes
```
DRIVE: "meeting notes" OR "notes" modifieddate:today-7d
SLACK: from:@katherine OR from:@thiago after:2025-12-20
```

### Para Status de Projeto
```
DRIVE: "tracker" OR "status" type:spreadsheet modifieddate:today-30d
SLACK: status OR update after:2025-12-01
```

### Para Contratos e SOW
```
DRIVE: "SOW" OR "contract" type:document modifieddate:today-90d
SLACK: SOW OR scope OR "statement of work"
```

### Para Problemas e Bugs
```
DRIVE: "issue" OR "bug" OR "incident" type:document
SLACK: blocker OR issue OR bug OR error
```

---

## MONITORAMENTO CONTINUO

| Query | Fonte | Frequencia | Proposito |
|-------|-------|------------|-----------|
| `"SOW" modifieddate:today-7d` | Drive | Semanal | Novos contratos |
| `"WFS" modifieddate:today-7d` | Drive | Semanal | Updates WFS |
| `blocker OR blocked` | Slack | Diario | Novos blockers |
| `from:@katherine decision` | Slack | Semanal | Decisoes |
| `type:spreadsheet "tracker"` | Drive | Semanal | Trackers atualizados |

---

Documento gerado para consumo por Drive Cortex
Fonte: 1442 arquivos relevantes de 20426 escaneados
Periodo: 180 dias
