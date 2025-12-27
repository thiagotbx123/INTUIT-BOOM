# OUTPUT D - Keyword Map e Receitas de Busca

> Mapeamento de termos e queries prontas para Drive e Linear
> Generated: 2025-12-27 00:35 America/Sao_Paulo
> Linear Access: No (recipes for manual use)

---

## 1. KEYWORD MAP POR TEMA

### WFS / Workforce Solutions
```
Termos Primarios (EN):
wfs, workforce, workforce solutions, hcm, human capital management
goco, mineral, mineralhr, hr advisor
payroll, hr, benefits, time tracking

Termos Primarios (PT):
solucoes de forca de trabalho, gestao de capital humano
folha de pagamento, recursos humanos, beneficios

Sinonimos e Variacoes:
- workforce = work force, work-force
- hcm = human capital, talent management
- goco = go co, go-co
- mineral = mineral hr, mineralhr

Erros Comuns:
- wfs = wsf, wfss
- workforce = workforse, worforce
- payroll = payrool, payrol
```

### QuickBooks / QBO
```
Termos Primarios (EN):
quickbooks, qbo, qboa, quickbooks online, quickbooks advanced
intuit, ies, intuit enterprise solutions

Termos Primarios (PT):
livros rapidos (nao usado)

Sinonimos e Variacoes:
- quickbooks = quick books, quick-books, QB
- qbo = qb online
- qboa = qbo advanced

Erros Comuns:
- quickbooks = quickboooks, quikbooks, quickbook
- intuit = intuti, intuiit
```

### Dataset / Dados
```
Termos Primarios (EN):
dataset, data set, seed, snapshot, refresh, reset
golden, synthetic data, demo data, sample data
data dictionary, mapping, schema

Termos Primarios (PT):
conjunto de dados, massa de dados, dados sinteticos
dicionario de dados, mapeamento, esquema

Sinonimos e Variacoes:
- dataset = data set, data-set
- seed = seeding, seeded
- golden = golden environment, golden demo

Erros Comuns:
- dataset = data sat, dateset
- synthetic = sintetic, synthethic
```

### Ingest / Pipeline
```
Termos Primarios (EN):
ingest, ingestion, pipeline, sync, connector
integration, transform, validation, reconcile
backfill, rerun, job, webhook

Termos Primarios (PT):
ingestao, pipeline, sincronizacao, conector
integracao, transformacao, validacao, reconciliacao

Sinonimos e Variacoes:
- ingest = ingestion, data ingestion
- pipeline = data pipeline, ETL
- sync = synchronization, synchronize

Erros Comuns:
- ingest = injest, ingist
- pipeline = piepline, pipelnie
```

### TCO / Tire
```
Termos Primarios (EN):
tco, traction control, traction control outfitters
tire, tire shop, fleet, fleet management
apex tire, global tread, roadready

Variacoes:
- tco = traction control outfitters
- fleet = fleet services, fleet management

Erros Comuns:
- traction = tration, tracton
```

### Construction
```
Termos Primarios (EN):
construction, keystone, job costing
wip, work in progress, change order
progress invoicing, retainage, contractor

Termos Primarios (PT):
construcao, custeio por projeto
trabalho em andamento, ordem de mudanca
faturamento progressivo, retencao

Variacoes:
- keystone = keystone construction
- wip = work in progress, work-in-progress

Erros Comuns:
- construction = contruction, constuction
- keystone = keyston, keystonee
```

### Canada
```
Termos Primarios (EN):
canada, canadian, cra, canada revenue agency
gst, pst, hst, provincial tax
provinces, ontario, quebec, bc, alberta

Termos Primarios (PT):
canada, canadense, agencia de receita do canada

Variacoes:
- cra = canada revenue, revenue canada
- gst = goods and services tax
- hst = harmonized sales tax

Erros Comuns:
- canada = canda, cananda
```

### Manufacturing
```
Termos Primarios (EN):
manufacturing, inventory, bom, bill of materials
assembly, work order, sku, cogs
production, warehouse, stock

Termos Primarios (PT):
manufatura, inventario, lista de materiais
montagem, ordem de trabalho, producao

Variacoes:
- manufacturing = mfg, manuf
- bom = bill of materials
- cogs = cost of goods sold

Erros Comuns:
- manufacturing = manufactoring, manifacturing
- inventory = inventroy, inventry
```

### Contratos
```
Termos Primarios (EN):
sow, statement of work, contract, agreement
msa, master service agreement
dpa, data processing agreement
nda, non disclosure, confidentiality
scope, assumptions, out of scope
change control, amendment, pricing

Termos Primarios (PT):
declaracao de trabalho, contrato, acordo
acordo de servico principal
acordo de processamento de dados
acordo de confidencialidade
escopo, premissas, fora do escopo

Variacoes:
- sow = statement of work
- msa = master services agreement
- dpa = data processing addendum
```

### Security / Compliance
```
Termos Primarios (EN):
soc, soc2, security, compliance
access control, data retention, encryption
audit, certification, penetration test

Termos Primarios (PT):
seguranca, conformidade, controle de acesso
retencao de dados, criptografia, auditoria

Variacoes:
- soc = soc 2, soc2, soc-2
- pentest = penetration test, pen test
```

---

## 2. RECEITAS DE BUSCA - GOOGLE DRIVE

### Por Tema Principal
```
# WFS - todos os documentos
"WFS" OR "Workforce" OR "HCM" OR "GoCo" OR "Mineral"

# QuickBooks/QBO
"QuickBooks" OR "QBO" OR "Intuit" OR "IES"

# TCO
"TCO" OR "Traction Control" OR "Tire" OR "Fleet"

# Construction
"Construction" OR "Keystone" OR "Job Costing"

# Canada
"Canada" OR "Canadian" OR "CRA" OR "GST"

# Manufacturing
"Manufacturing" OR "Inventory" OR "BOM" OR "Assembly"
```

### Por Tipo de Documento
```
# SOWs e Contratos
"SOW" OR "Statement of Work" OR "Contract" type:document

# Trackers e Status
"Tracker" OR "Status" OR "Progress" type:spreadsheet

# Roadmaps e Estrategia
"Roadmap" OR "Strategy" OR "Plan" type:presentation

# Health Checks
"Health Check" OR "Checklist" OR "Validation" type:spreadsheet

# Runbooks e Documentacao Tecnica
"Runbook" OR "Architecture" OR "Design" type:document
```

### Por Periodo
```
# Ultimos 7 dias
modifieddate:today-7d

# Ultimos 30 dias
modifieddate:today-30d

# Dezembro 2025
modifieddate:2025-12-01..2025-12-31

# Fall Release period (Out-Nov 2025)
modifieddate:2025-10-01..2025-11-30 "fall release"
```

### Por Owner
```
# Documentos do Thiago
owner:thiago@testbox.com

# Documentos da Katherine
owner:katherine

# Documentos compartilhados por Intuit
from:intuit.com
```

### Queries Compostas Recomendadas
```
# WFS SOW atual
"WFS" "SOW" modifieddate:today-30d type:document

# TCO Health Status
"TCO" ("health" OR "status" OR "checklist") type:spreadsheet

# Fall Release Evidence
"Fall Release" ("tracker" OR "evidence" OR "UAT") modifieddate:2025-11..2025-12

# Contratos Intuit
"Intuit" ("contract" OR "SOW" OR "agreement") type:pdf

# Datasets e Ingest
"dataset" OR "ingest" type:spreadsheet modifieddate:today-90d
```

---

## 3. RECEITAS DE BUSCA - LINEAR

### Estrutura do Linear (Inferida)
```
Teams Provaveis:
- Platform (ou Engineering)
- TSA (Technical Solutions Architects)
- Data (ou Data Engineering)
- Product

Labels Provaveis:
- bug, feature, improvement
- tco, wfs, qbo, construction, canada
- p0, p1, p2, p3 (prioridade)
- blocked, in-progress, done

Projects Provaveis:
- TCO
- WFS
- Fall Release
- Winter Release
- Ingest/Pipeline
```

### Por Tema
```
# WFS issues
project:WFS OR label:wfs

# TCO issues
project:TCO OR label:tco

# QuickBooks/QBO
label:qbo OR label:quickbooks OR title:"QuickBooks"

# Construction
label:construction OR title:"Construction" OR title:"Keystone"

# Canada
label:canada OR title:"Canada"

# Ingest/Pipeline
label:ingest OR label:pipeline OR title:"ingest"
```

### Por Status
```
# Abertos e em progresso
status:in-progress OR status:todo

# Bloqueados
status:blocked OR label:blocked

# Recentemente fechados
status:done updated:>2025-12-01

# Backlog
status:backlog
```

### Por Prioridade
```
# P0/P1 - Criticos
label:p0 OR label:p1

# Bugs ativos
label:bug status:in-progress

# High priority
priority:urgent OR priority:high
```

### Por Texto Exato
```
# Negative inventory issue
"negative inventory"

# Login failure
"login" "ECS" OR "login" "task"

# SOW relacionado
"SOW" OR "Statement of Work"

# Health check
"health check" OR "health-check"
```

### Por Assignee
```
# Tickets do Thiago
assignee:thiago

# Tickets nao atribuidos
assignee:none

# Tickets do time Platform
team:Platform
```

### Por Data
```
# Criados esta semana
created:>2025-12-20

# Atualizados nos ultimos 30 dias
updated:>2025-11-27

# Criados em Dezembro
created:2025-12-01..2025-12-31
```

### Queries Compostas para Linear
```
# TCO bugs ativos
project:TCO label:bug status:in-progress

# WFS implementation tasks
project:WFS label:feature status:todo

# P0/P1 bloqueados
(label:p0 OR label:p1) status:blocked

# Ingest issues recentes
label:ingest updated:>2025-12-01

# Fall Release remaining
project:"Fall Release" status:in-progress

# Tickets sem assignee de alta prioridade
(label:p0 OR label:p1) assignee:none
```

---

## 4. MAPEAMENTO DRIVE <-> LINEAR

### Pattern para Conectar
```
Quando encontrar no Drive:
- Ticket ID no formato: PLA-XXXX, ENG-XXXX, TSA-XXXX
- Link do Linear: https://linear.app/testbox/issue/XXX
- Referencia: "See ticket", "Related issue", "Linear"

Buscar no Linear:
- Title match com nome do documento
- Description com link do Drive
- Comments com referencias cruzadas
```

### Gaps Comuns
```
Documentos que precisam de tickets:
- SOW drafts sem ticket de tracking
- Scope plans sem implementation tickets
- Runbooks sem incident tickets

Tickets que precisam de docs:
- Bugs sem RCA/postmortem
- Features sem PRD
- Incidents sem runbook
```

---

## 5. MONITORAMENTO CONTINUO

### Queries para Executar Diariamente
| Query | Fonte | Proposito |
|-------|-------|-----------|
| `modifieddate:today-1d` | Drive | Novos/modificados hoje |
| `status:blocked` | Linear | Tickets bloqueados |
| `label:p0 OR label:p1` | Linear | Alta prioridade |

### Queries para Executar Semanalmente
| Query | Fonte | Proposito |
|-------|-------|-----------|
| `"WFS" modifieddate:today-7d` | Drive | Progress WFS |
| `project:WFS updated:>-7d` | Linear | WFS tickets |
| `"SOW" type:document` | Drive | Novos contratos |
| `label:bug status:in-progress` | Linear | Bugs ativos |

### Queries para Executar Mensalmente
| Query | Fonte | Proposito |
|-------|-------|-----------|
| `"Roadmap" OR "Strategy"` | Drive | Strategic docs |
| `status:done created:>-30d` | Linear | Completed work |
| `assignee:none` | Linear | Unassigned cleanup |

---

Documento gerado automaticamente
Fonte: Analise de 20,426 arquivos do Drive
Linear: Sem acesso direto - receitas para uso manual
