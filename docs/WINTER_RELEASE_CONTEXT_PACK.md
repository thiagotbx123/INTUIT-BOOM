# CONTEXT PACK - Intuit Winter Release (Feb 2026)
**Versao**: 1.0
**Gerado**: 2025-12-29
**Owner**: Thiago Rodrigues (TSA)

---

## 1. INVENTARIO DE AMBIENTES

### Ambientes Confirmados

| Ambiente | Tipo | Email Login | Status |
|----------|------|-------------|--------|
| **TCO** | Multi-Entity (Parent + 3 children) | quickbooks-testuser-tco-tbxdemo@tbxofficial.com | ACTIVE |
| **Construction Sales** | IES Construction | quickbooks-test-account@tbxofficial.com | ACTIVE |
| **Construction Events** | IES Events | TBD | PARTIAL 95% |
| **Manufacturing** | IES Manufacturing | TBD | GAP |
| **Nonprofit** | IES Nonprofit | TBD | PARTIAL 95% |
| **Canada** | QBO Canada | TBD | ACTIVE |

### Estrutura Multi-Entity TCO

- Traction Control Outfitters (Parent)
  - Apex Tire (Child 1) - ID: 9341455130166501
  - Global Tread (Child 2) - ID: 9341455130196737
  - RoadReady (Child 3) - ID: 9341455130170608
  - Consolidated View - ID: 9341455649090852

---

## 2. DATASETS DISPONIVEIS

### JSON Files
- metrics_tco_group.json
- table_tco_group_customers/vendors/employees/invoices/bills/projects.json
- metrics_construction_demo.json
- table_construction_demo_*.json

### SQLite Database
- qbo_database_TCO_Construction.db
- qbo_database (1).db (~40MB)

---

## 3. WINTER RELEASE FEATURES (30 total)

### AGENTS (AI) - 8 features
1. Accounting AI
2. Sales Tax AI (Early Access 15/Jan)
3. Project Management AI
4. Solutions Specialist
5. Finance AI
6. Omni/Intuit Intelligence (Beta)
7. Customer Agent
8. Conversational BI

### REPORTING - 6 features
9. KPIs and Dashboards
10. 3P Data
11. Calculated Fields on Reports
12. Management Reports
13. Benchmarking
14. New Multi-Entity Reports

### DIMENSIONS - 4 features
15. Dimension Assignment Enhancement v2
16. Hierarchical Dimension Reporting
17. Dimensions on Workflow Automation
18. Dimensions on Balance Sheet

### WORKFLOW - 1 feature
19. Parallel Approval in Workflow Automation

### MIGRATION - 3 features
20. Seamless Desktop Migration
21. DFY Migration Experience
22. Feature Compatibility

### CONSTRUCTION - 3 features
23. Certified Payroll Report (CPR)
24. Tech Stack Assessment
25. Sales Order

### PAYROLL - 4 features
26. Multi-Entity Payroll Employee Hub
27. Garnishments Child Support
28. Assignments in QBTime
29. BETA Enhanced Amendments CA only

---

## 4. BLOCKERS ATIVOS (Linear)

| Issue | Titulo | Impacto |
|-------|--------|---------|
| PLA-3013 | Login task failing TCO | P0 |
| PLA-2969 | Canada Data Ingest Bills | P1 |
| PLA-2883 | Error ingesting activities | P1 |
| PLA-2724 | Dimensions in Payroll | P1 |
| PLA-2916 | Negative Inventory TCO | P1 |

---

## 5. TOOLING

### Camadas de Automacao
- Camada 1 - Login: LOCKED (layer1_login.py)
- Camada 2 - Navegacao: OPEN (qbo_checker/navigator.py)
- Camada 3 - Captura: OPEN (qbo_checker/screenshot.py)
- Camada 4 - Planilha: OPEN (qbo_checker/spreadsheet.py)
- Camada 5 - Orquestracao: OPEN (run_validation_v2.py)

---

## 6. TIMELINE

| Data | Marco |
|------|-------|
| 2025-11-20 | Fall Release ENTREGUE |
| 2025-12-19 | Winter Release anunciado |
| 2026-01-15 | Sales Tax AI Early Access |
| 2026-02-04 | Winter Release Early Access (pendente) |

---

## 7. FONTES DE VERDADE

- Winter Release Doc: docs.google.com/document/d/1lc-G-ehRWO0C9hdSglj-idNbrFy6SGP-Pq3PaSzNpjY
- Strategic Cortex: knowledge-base/strategic-cortex/OUTPUT_A
- Slack: Canal C06PSSGEK8T
- Linear: 443 issues Intuit-related
- features_rich.json: qbo_checker/features_rich.json
