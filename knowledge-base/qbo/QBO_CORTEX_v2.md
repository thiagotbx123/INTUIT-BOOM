# QBO Cortex para Intuit BOOM

**Versao:** 2.0
**Criado em:** 2025-12-19
**Proprietario:** Thiago Rodrigues (TSA, Data Architect)
**Proposito:** Base de conhecimento pratica para validacao de features, manutencao de ambientes demo, e suporte tecnico rapido.

---

## INDICE

1. Visao Geral do QuickBooks
2. Glossario de Termos e Siglas
3. Mapa de Navegacao da UI
4. Matriz de Features por Plano
5. Guia de Integracoes e APIs
6. Modelo de Dados Conceitual
7. Autenticacao, Roles e Permissoes
8. Runbooks de Validacao
9. Troubleshooting e Problemas Comuns
10. Gaps e Perguntas Abertas
11. Indice de Fontes

---

## 1. Visao Geral do QuickBooks

### 1.1 O que e QuickBooks Online (QBO)
QuickBooks Online e uma plataforma de contabilidade e gestao financeira em nuvem da Intuit.

**Principio fundamental:** Double-entry accounting (debito = credito)

### 1.2 Planos Disponiveis (US)

| Plano | Preco/mes | Usuarios | Recursos Chave |
|-------|-----------|----------|----------------|
| Simple Start | $30 | 1 | Invoicing, expenses, reports basicos |
| Essentials | $60 | 3 | + Bills, time tracking, multi-currency |
| Plus | $90 | 5 | + Projects, inventory, classes, locations |
| Advanced | $200 | 25+ | + Multi-entity, custom reports, workflows |

### 1.3 QBO Advanced - Foco do Projeto

Features exclusivos do Advanced:
- Multi-Entity consolidation
- Custom Reports com Fathom
- Workflows de aprovacao
- Batch Transactions
- Custom User Roles
- Priority Support

### 1.4 Ambientes TestBox - TCO

| Company | Tipo | Company ID |
|---------|------|------------|
| TCO Parent | Parent | 9341455130188547 |
| Apex Tire | Child (Retail) | 9341455130166501 |
| Global Tread | Child (Wholesale) | 9341455130196737 |
| RoadReady | Child (Service) | 9341455130170608 |
| Consolidated | Consolidated | 9341455649090852 |

Login: quickbooks-testuser-tco-tbxdemo@tbxofficial.com

### 1.5 Ambientes TestBox - Construction

| Company | Login |
|---------|-------|
| Keystone Construction | quickbooks-test-account@tbxofficial.com |

---

## 2. Glossario de Termos

| Termo | Definicao |
|-------|-----------|
| QBO | QuickBooks Online |
| IES | Intuit Enterprise Suite |
| CoA | Chart of Accounts |
| AR | Accounts Receivable |
| AP | Accounts Payable |
| COGS | Cost of Goods Sold |
| FIFO | First-In First-Out |
| TCO | Traction Control Outfitters |
| ME | Multi-Entity |
| DTM | Desktop-to-Mobile |

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
| Vendors | /app/vendors |
| Bills | /app/billpayment |
| Reports | /app/reportlist |
| Chart of Accounts | /app/chartofaccounts |
| Settings | /app/settings |
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
| Locations | - | - | Y | Y |
| Custom Reports | - | - | - | Y |
| Multi-Entity | - | - | - | Y |
| Workflows | - | - | - | Y |
| Custom Roles | - | - | - | Y |

---

## 5. Guia de APIs

### 5.1 URLs

| Ambiente | URL |
|----------|-----|
| Production | https://quickbooks.api.intuit.com |
| Sandbox | https://sandbox-quickbooks.api.intuit.com |

### 5.2 OAuth 2.0

| Parametro | Valor |
|-----------|-------|
| Access Token TTL | 1 hora |
| Refresh Token TTL | 100 dias |
| Scope | com.intuit.quickbooks.accounting |

### 5.3 Rate Limits

| Tipo | Limite |
|------|--------|
| Requests/minuto | 500 por company |
| Concurrent | 10 por app |
| Batch | 40/minuto |
| Query response | Max 1,000 entities |

### 5.4 Objetos Principais

| Objeto UI | Endpoint API |
|-----------|--------------|
| Customer | /v3/company/{id}/customer |
| Vendor | /v3/company/{id}/vendor |
| Invoice | /v3/company/{id}/invoice |
| Bill | /v3/company/{id}/bill |
| Account | /v3/company/{id}/account |
| Item | /v3/company/{id}/item |
| Class | /v3/company/{id}/class |


---

## 6. Modelo de Dados

### 6.1 Chart of Accounts - Tipos

| Tipo | Categoria | Exemplo |
|------|-----------|---------|
| Bank | Asset | Checking Account |
| Accounts Receivable | Asset | Trade Receivables |
| Fixed Asset | Asset | Equipment |
| Accounts Payable | Liability | Trade Payables |
| Credit Card | Liability | Business Credit Card |
| Equity | Equity | Retained Earnings |
| Income | Income | Sales Revenue |
| Cost of Goods Sold | COGS | Material Costs |
| Expense | Expense | Rent, Utilities |

### 6.2 Dimensoes

| Dimensao | Proposito | Atribuicao |
|----------|-----------|------------|
| Class | Linha de negocio | Por linha ou transacao |
| Location | Local fisico | Uma por transacao |
| Project | Agrupar transacoes | Por transacao |

### 6.3 Inventory

QBO Online usa FIFO automaticamente.

| Conceito | Descricao |
|----------|-----------|
| On Hand | Quantidade em estoque |
| Reorder Point | Alerta de reposicao |
| FIFO | First-In First-Out valuation |

---

## 7. Roles e Permissoes

### 7.1 Tipos de Usuario

| Role | Acesso |
|------|--------|
| Primary Admin | Total (dono da conta) |
| Company Admin | Total exceto billing |
| Standard All Access | Tudo exceto users |
| Standard Limited | Configuravel |
| Reports Only | Apenas reports |

### 7.2 Problemas Comuns

| Problema | Solucao |
|----------|---------|
| Tela branca | Verificar role |
| Feature off | Verificar plano |
| Login loop | Limpar cookies |
| Settings bloqueado | Precisa Admin |

---

## 8. Runbooks de Validacao

### 8.1 Invoice (AR)

1. + New > Invoice
2. Select Customer
3. Add line items
4. Save

Verificar:
- Invoice em Sales > Invoices
- AR Aging atualizado
- Customer balance atualizado

### 8.2 Bill (AP)

1. + New > Bill
2. Select Vendor
3. Add line items
4. Save

Verificar:
- Bill em Expenses > Bills
- AP Aging atualizado
- Vendor balance atualizado

### 8.3 Reconciliacao

1. Banking > Reconcile
2. Select Account
3. Enter Statement date/balance
4. Match transactions
5. Difference = 0
6. Finish

ATENCAO: NAO forcar se Difference != 0

---

## 9. Troubleshooting

### 9.1 Bank Feed

| Problema | Solucao |
|----------|---------|
| Nao atualiza | Banking > Update |
| Match falha | Verificar valores |
| Duplicata | Usar Exclude |

### 9.2 Reconciliacao

| Problema | Solucao |
|----------|---------|
| Difference != 0 | Comparar com statement |
| Saldo errado | Ajustar opening balance |

### 9.3 Demo

| Problema | Solucao |
|----------|---------|
| Overdues antigas | Limpar invoices |
| Feature off | Verificar settings |
| Login falha | Limpar cookies |

---

## 10. Gaps Conhecidos

| ID | Gap | Status |
|----|-----|--------|
| GAP-001 | Vendor CC/BCC | Blocked |
| GAP-002 | Intercompany mapping | Em progresso |
| GAP-003 | KPIs Monday.com | Intuit owned |
| GAP-004 | API Projects | Nao existe |

---

## 11. Fontes

### Internas

| ID | Fonte |
|----|-------|
| SRC-001 | QBO_DEEP_MASTER_v1.txt |
| SRC-002 | Fall Release Tracker |

### Externas

| ID | Fonte | URL |
|----|-------|-----|
| SRC-003 | QuickBooks Pricing | quickbooks.intuit.com/pricing |
| SRC-004 | Developer Portal | developer.intuit.com |
| SRC-005 | Help Center | quickbooks.intuit.com/learn-support |

---

Ultima atualizacao: 2025-12-19
