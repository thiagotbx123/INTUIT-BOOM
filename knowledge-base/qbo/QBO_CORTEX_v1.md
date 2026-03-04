# QBO Cortex para Intuit BOOM

**Versao:** 1.0
**Criado em:** 2025-12-19
**Proprietario:** Thiago Rodrigues (TSA, Data Architect)

---

## INDICE

1. Visao Geral do QuickBooks
2. Glossario de Termos e Siglas
3. Mapa de Navegacao da UI por Modulo
4. Matriz de Features por Plano
5. Guia de Integracoes e APIs
6. Modelo de Dados Conceitual
7. Autenticacao, Roles e Permissoes
8. Runbooks de Validacao
9. Gaps e Perguntas Abertas
10. Indice de Fontes

---

## 1. Visao Geral do QuickBooks

### 1.1 O que e QuickBooks Online
QuickBooks Online (QBO) e uma plataforma de contabilidade e gestao financeira em nuvem da Intuit.

### 1.2 Planos Disponiveis
| Plano | Recursos Chave |
|-------|----------------|
| Simple Start | Invoicing, expenses, reports basicos |
| Essentials | + Bills, time tracking, 3 usuarios |
| Plus | + Projects, inventory, 5 usuarios |
| Advanced | + Multi-entity, custom reports, 25+ usuarios |

### 1.3 QBO Advanced - Foco do Projeto
Projeto Intuit BOOM foca em QBO Advanced e cenarios multi-entity:
- TCO (Traction Control Outfitters): Parent + 3 children
- Construction Sales/Events: Cenarios de construcao

### 1.4 TCO - Traction Control Outfitters
Empresa demo principal:
- Fundada 1998, HQ Dallas TX
- 9 locations, 4 estados, 250 employees
- Budget anual $250M
- Fiscal year end: 31 Janeiro
- 3 divisoes: Wholesale (Global Tread), Retail (Apex Tire), Service (RoadReady)

---

## 2. Glossario de Termos

| Termo | Definicao |
|-------|-----------|
| QBO | QuickBooks Online |
| IES | Intuit Enterprise Suite |
| CoA | Chart of Accounts (Plano de Contas) |
| AR | Accounts Receivable |
| AP | Accounts Payable |
| TCO | Traction Control Outfitters |
| DTM | Desktop-to-Mobile |
| ME | Multi-Entity |
| GST | Goods and Services Tax (AU) |
| BAS | Business Activity Statement (AU) |
| RevRec | Revenue Recognition |

---

## 3. Mapa de Navegacao da UI

### 3.1 Rotas Principais
| Modulo | Rota |
|--------|------|
| Dashboard | /app/homepage |
| Banking | /app/banking |
| Reconcile | /app/reconcile |
| Customers | /app/customers |
| Invoices | /app/invoices |
| Bills | /app/billpayment |
| Reports | /app/reportlist |
| Settings | /app/settings |
| Chart of Accounts | /app/chartofaccounts |
| Products | /app/items |

---

## 4. Matriz de Features por Plano

| Feature | Simple | Essentials | Plus | Advanced |
|---------|:------:|:----------:|:----:|:--------:|
| Invoicing | Y | Y | Y | Y |
| Bills | - | Y | Y | Y |
| Projects | - | - | Y | Y |
| Inventory | - | - | Y | Y |
| Classes | - | - | Y | Y |
| Custom Reports | - | - | - | Y |
| Multi-Entity | - | - | - | Y |
| Workflows | - | - | - | Y |

---

## 5. Guia de APIs

### 5.1 QuickBooks Online API
- Base URL: https://quickbooks.api.intuit.com
- Sandbox: https://sandbox-quickbooks.api.intuit.com

### 5.2 OAuth 2.0
- Token Lifetime: Access 1h, Refresh 100 dias
- Scopes: com.intuit.quickbooks.accounting

### 5.3 Rate Limits
- 500 requests/minuto
- 10 requests/segundo
- Max 30 ops/batch

### 5.4 Objetos Principais
| Objeto | Endpoint |
|--------|----------|
| Customer | /v3/company/{id}/customer |
| Vendor | /v3/company/{id}/vendor |
| Invoice | /v3/company/{id}/invoice |
| Bill | /v3/company/{id}/bill |
| Account | /v3/company/{id}/account |
| Item | /v3/company/{id}/item |

---

## 6. Modelo de Dados

### 6.1 Entidades Principais
- Company > Locations > Classes > Accounts
- Customers > Invoices > Payments
- Vendors > Bills > Bill Payments
- Items (Inventory, Non-Inventory, Service)
- Employees > Time Activities
- Projects > Transactions

### 6.2 Dimensoes (Advanced)
| Dimensao | Proposito |
|----------|-----------|
| Class | Linha de negocio |
| Location | Local fisico |
| Project | Agrupar por projeto |

### 6.3 Regras Contabeis
- Double-entry: debito = credito
- AR requer Customer
- AP requer Vendor
- Inventory: FIFO padrao

---

## 7. Roles e Permissoes

### 7.1 Tipos de Usuario
| Tipo | Acesso |
|------|--------|
| Master Admin | Total |
| Company Admin | Total exceto billing |
| Standard User | Configuravel |
| Reports Only | Apenas reports |

### 7.2 Problemas Comuns
| Problema | Solucao |
|----------|---------|
| Tela branca | Verificar role |
| Login loop | Limpar cookies |
| Feature off | Verificar plano |

---

## 8. Runbooks de Validacao

### 8.1 Invoice
1. Sales > Create Invoice
2. Selecionar Customer
3. Adicionar linhas
4. Save
Verificar: AR Aging atualizado

### 8.2 Bill
1. Expenses > Create Bill
2. Selecionar Vendor
3. Adicionar linhas
4. Save
Verificar: AP Aging atualizado

### 8.3 Reconciliacao
1. Categorizar transacoes
2. Banking > Reconcile
3. Match ate Difference = 0
4. Finish
ATENCAO: NAO forcar se Difference != 0

---

## 9. Gaps e Perguntas

### Gaps Conhecidos
- GAP-001: Vendor CC/BCC nao exposto (Construction Sales)
- GAP-002: Intercompany mapping incompleto
- GAP-003: KPIs Monday.com blocked on Intuit

### Perguntas para Intuit
1. Vendor CC/BCC timeline?
2. Consolidated View behavior parcial?
3. API para Intercompany Allocations?

---

## 10. Fontes

| ID | Fonte |
|----|-------|
| SRC-001 | QBO_DEEP_MASTER_v1.txt (interno) |
| SRC-002 | QBO_MASTER.md (interno) |
| SRC-003 | quickbooks.intuit.com |
| SRC-004 | developer.intuit.com |

---

## APENDICE: Ambientes TestBox

### TCO
| Company | ID |
|---------|-----|
| Apex Tire | 9341455130166501 |
| Consolidated | 9341455649090852 |
| Global Tread | 9341455130196737 |
| TCO Parent | 9341455130188547 |
| RoadReady | 9341455130170608 |

Login: quickbooks-testuser-tco-tbxdemo@tbxofficial.com

### Construction
| Company | Login |
|---------|-------|
| Keystone | quickbooks-test-account@tbxofficial.com |

---
Ultima atualizacao: 2025-12-19
