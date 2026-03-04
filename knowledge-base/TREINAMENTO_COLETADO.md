# Conhecimento Coletado para Treinamento

> Consolidacao de informacoes extraidas da pasta Downloads
> Data: 2024-12-26
> Fonte: 416 arquivos analisados

---

## 1. PROJETOS INTUIT/TESTBOX

### 1.1 Universo Principal

| Projeto | Descricao | Status |
|---------|-----------|--------|
| **TCO (Traction Control Outfitters)** | Simulacao multi-entity QBO Advanced. Parent + 3 children (Apex Tire, Global Tread, RoadReady) | Ativo |
| **Construction Sales** | Ambiente IES para construction e desktop parity | Ativo |
| **Construction Events** | Ambiente IES para eventos (Intuit Dome) | Ativo |
| **Manufacturing** | Dataset para stress test de activity plans | Ativo |
| **Tire Shop** | Dataset high volume (10k+ customers) | Ativo |
| **Canada Construction** | Instancias canadenses com datasets localizados | Ativo |

### 1.2 Datasets Disponiveis

```
QuickBooks Segments:
- canada_construction
- construction
- non_profit
- professional_services
- manufacturing
- tire_shop
```

### 1.3 Papel do Thiago (TSA)

- Technical Solutions Architect e Data Architect
- Design de datasets e joins
- Regras de validacao
- Tickets Linear e worklogs
- Coordenacao com Engineering e Intuit PMs
- Fall Release tracker e UAT

---

## 2. FALL RELEASE FEATURES

### 2.1 Catalogo de Features

| Feature | Notas |
|---------|-------|
| **Payments Agent** | Invoice screen carrega Assist suggestions |
| **Finance Agent** | Mostra margin dips, late payments |
| **Accounting Agent** | Bank Transactions mostra suggested matches |
| **Project Management Agent** | Spreadsheet upload quando nao tem Estimate |
| **Certified Payroll** | Requer payroll runs, weekly pay schedule |
| **Shared Chart of Accounts** | Interface carrega, conflicting accounts flagged |
| **Dimension Assignment** | Missing dimensions detectadas, AI suggestions |
| **Intercompany Sales Enforcement** | Blocking entre invoice e bill status |
| **Intercompany Cost Allocations** | Allocations via Allocate flow |
| **KPI Library** | 3P dependent KPIs escondidos sem apps conectados |
| **Custom KPIs** | Formula builder funciona |
| **Dashboard Enhancements** | Charts renderizam, customization funciona |
| **A/R Aging Summary** | Report carrega com dados populados |
| **Quarterly Reporting Package** | Cover page e charts |
| **Bill Payment Approval Workflow** | Depende de Bill Pay Elite |
| **Instant Payments** | So visivel com payment rail enabled |

### 2.2 Intercompany Expense Allocations (Guia)

Setup:
1. Go to Multi-entity > Overview tab
2. In Resources widget: Intercompany account mapping
3. Select source company
4. Add new > target company, receivable account, payable account
5. Repeat for all mappings

Allocate:
1. Go to Bank transactions, Expenses, Checks, or Bills
2. Select Allocate in transaction
3. Choose entities for allocation
4. Set Category/Item and Percentage/Amount per company
5. Save

---

## 3. WFS (WORKFORCE SOLUTIONS)

### 3.1 Overview

**Intuit Workforce Solutions** - Plataforma HCM para SMBs
- Combina: Payroll + HR + Benefits + Time
- Integracao com QuickBooks
- Powered by: GoCo + QuickBooks Payroll

### 3.2 Timeline

| Fase | Data | Scope |
|------|------|-------|
| **Alpha** | Dez 2025 | ~100 customers |
| **Beta** | Fev 2026 | Expansao features |
| **GA** | Mai 2026 | Lancamento geral (2026-05-01) |

### 3.3 Tracks por Fase

#### ALPHA (6/2/2025 - 11/14/2025)
- Audit Service Integration V1
- Documents Management V1 (I-9, offer letter)
- New Hire Onboarding V1
- Time Off V1 (PTO: Sick, Vacation, Personal, Unpaid)
- Worker Profile V1
- Effective Dating / Employment Changes V1
- Inbox / Notifications V1
- Employee Web App V1
- Manager Role V1
- Checkr Background Check V1

#### BETA (11/3/2025 - 2/23/2026)
- Worker Profile V2
- Worker List V1
- Workforce Overview Page V1
- Offboarding V1
- Performance Management V1
- Workflow Management V1
- Employee Mobile App V1
- Applicant Tracking (ATS) V0
- Benefits Admin V0

#### GA (3/2/2026 - 5/1/2026)
- Team Overview Page V1
- Reports & Analytics V1
- Data Governance V1
- Benefits Admin V1
- Applicant Tracking (ATS) V1
- New Company Onboarding V1

### 3.4 Feature Flags Importantes

| Flag | Proposito |
|------|-----------|
| `ENABLE-HCM-ROUTES` | Master flag para HCM features |
| `ENABLE-BETA-HCM-ROUTES` | Master flag para Beta |
| `SBSEG-QBO-Enable_Worker_Profile_Experience` | Worker Profile |
| `SBSEG-QBO-employee-future-effective-dating` | Effective dating |
| `enable-workforce-new-skin` | Employee Web App |

### 3.5 GoCo Features no WFS

Principais features migrando do GoCo:
- Org Chart (After GA)
- Team Directory (After GA)
- Employee Profile (Alpha)
- Employee Timeline (After GA)
- User Home Page (Alpha)
- Multi-entity support (Alpha)
- Employment history (Alpha)
- Effective dates (Alpha)
- Emergency contact (Alpha)
- Inbox & Notifications (Alpha)
- Termination wizard (Beta)
- Digital I-9 (Alpha)
- Digital W4 (Alpha)
- Pre-built reports (GA)
- Custom report builder (GA)
- iOS/Android mobile app (Beta)

---

## 4. CANADA CONSTRUCTION

### 4.1 Dataset Canada Construction

ID: `2ed5d245-0578-43aa-842b-6e1e28367149`

### 4.2 Estrutura de Customers (Canada)

| Campo | Exemplo |
|-------|---------|
| email | @tbxofficial.com |
| phone | Formato canadense |
| billing_address | Enderecos canadenses |
| city | Regina, Calgary, Toronto, Vancouver, Montreal, etc |
| state | SK, AB, ON, BC, QC, PE, NL, MB, NS, NB |
| country | Canada |
| terms | Net 30 |
| language | English |
| customer_type | Commercial, Government, Residential |

### 4.3 Empresas Fake (Canada Demo)

- FLDN
- Clove Logistics
- Concrete Solutions
- JJ Home Solutions
- Skye West Coast Properties
- Summit Realty Group
- Horizon Infrastructure Solutions
- Keystone Holdings
- Pioneer Development Corporation
- Apex Enterprises Inc.
- Skyline Ventures
- Crestline Holdings
- Pacific Capital Associates
- Atlas Development Corporation
- Genesis Holdings
- Terra Firma Solutions
- Aegis Holdings

---

## 5. TCO MILESTONES (Tire Projects)

### Projetos por Regiao

| ID | Projeto | Regiao |
|----|---------|--------|
| 54 | SAIA Southwest | Southwest |
| 55 | Prairie Line Distribution | OK/AR |
| 56 | Bayou Interstate Logistics | Gulf (Heavy Haul) |
| 57 | Trinity Fleet Services | Pull-In |
| 58 | Emergency Response | Gulf |
| 59 | RedHawk Fleet Services | Central |
| 60 | Prairie Line Distribution | General |

### Tipos de Milestones

1. Intake & VIN Audit
2. Tread & Safety Baseline
3. Rotation Plan A Published
4. Parts Staging & Rebate Setup
5. Midterm SLA & Cost Review
6. Rotation Plan B Executed
7. Final QC & Road Test
8. Closeout & Acceptance

---

## 6. STAKEHOLDERS

### TestBox
| Nome | Papel |
|------|-------|
| Thiago Rodrigues | TSA, Data Architect |
| Lucas Soranzo | Engineering Lead |
| Lucas Torresan | Data Engineer |
| Eyji Koike Cuff | Engineer |
| Marcelo Andriolli | Engineer |
| Sam | Leadership, GTM |
| Katherine Lu | Account/Program Lead |
| Lucas Wakigawa | Product/GTM Lead |

### Intuit
| Nome | Papel |
|------|-------|
| Lawton Ursrey | Product Leader (IES) |
| Jason | PM |
| Crystal | PMM |
| Ben Hale | Sales Enablement (WFS) |
| Nikki Behn | Marketing (WFS) |
| Kyla Ellerd | Sales Program Management (WFS) |
| Christina Duarte | Leadership, Scoping (WFS) |

---

## 7. TICKETS LINEAR IMPORTANTES

| ID | Titulo | Status |
|----|--------|--------|
| PLA-2862 | Data Ingest Chart of Accounts | open |
| PLA-2866 | Data Ingest Products and Services | open |
| PLA-2869 | Data Ingest Vendors | open |
| PLA-2871 | Data Ingest Customers | closed |
| PLA-2916 | TCO Automation Inventory Prevent negative stock | open |
| PLA-2933 | Normalize and Clean Overdue TCO Invoices | ongoing |
| PLA-3023 | TCO Add shipping columns | ongoing |
| PLA-3024 | TCO Re-ingestion shipping fields | ongoing |
| PLA-3083 | TCO Manual Re-ingestion Customer Notes | ongoing |
| PLA-3090 | Construction Manual Ingestion Credit Card Credit | ongoing |
| PLA-3051 | Build Visibility and Weekly reports | ongoing |
| PLA-3013 | Login task failing for TCO | blocked |

---

## 8. DECISOES IMPORTANTES

| Data | Decisao |
|------|---------|
| 2025-10-29 | Vendor CC/BCC blocked ate Intuit expor campos |
| 2025-10-21 | Fall Release prioridade sobre outros trabalhos |
| 2025-11-04 | Deadline: 20 Nov para todos ambientes atualizados |
| 2025-11-13 | KPIs Monday.com = responsabilidade Intuit |
| 2025-11-17 | Particionar ambientes em partner vs internal |

---

## 9. INCIDENTES CONHECIDOS

| Data | Incidente | Status |
|------|-----------|--------|
| 2025-10-27 | TCO login ECS task failing | Workaround: manual login |
| 2025-10-21 | Validator timeouts em datasets grandes | Batching/caching em progresso |
| 2025-09-23 | Negative inventory em TCO products | PLA-2916 em progresso |

---

## 10. LINKS IMPORTANTES

| Doc | URL |
|-----|-----|
| Fall Release Tracker | https://docs.google.com/spreadsheets/d/11qrIM0M5MUZLfs0aNvOVWCszdTb4XQKbvKpw3F5r_0I |
| TCO Core Requirements | https://docs.google.com/spreadsheets/d/1iyEuYAD-AThXsR5E9rItwx14rdpRTSsBT2gvH4-lexs |
| Big Numbers Deck | https://docs.google.com/presentation/d/1qgLfj-lTNGFpKHCEad9Er7xoj7GEaNYb |

---

## PROXIMOS PASSOS

1. [ ] Processar mais arquivos Excel via Python
2. [ ] Extrair conteudo dos PDFs WFS
3. [ ] Mapear scripts Python de login/automacao
4. [ ] Consolidar knowledge-base/qbo existente

---

Documento gerado automaticamente pela Camada de Coleta
Fonte: /c/Users/adm_r/Downloads/
