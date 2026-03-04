# Feature and Surface Map - QBO/Intuit BOOM

**Versao:** 1.0
**Criado em:** 2025-12-19

---

## Sales / AR

| Area | Feature | UI Path | Pre-req | Validar | Evidencia | Fonte |
|------|---------|---------|---------|---------|-----------|-------|
| Sales | Create Invoice | + New > Invoice | Customer | Criar, ver AR Aging | Screenshot AR | QBO |
| Sales | Receive Payment | + New > Receive Payment | Invoice | Receber, AR zera | Screenshot Payment | QBO |
| Sales | AR Aging | Reports > AR Aging | Invoices | Rodar report | Screenshot | QBO |
| Sales | Recurring Invoice | + New > Recurring | Template | Verificar execucao | Screenshot | QBO |
| Sales | Credit Memo | + New > Credit Memo | Invoice | Aplicar credito | Screenshot | QBO |

---

## Expenses / AP

| Area | Feature | UI Path | Pre-req | Validar | Evidencia | Fonte |
|------|---------|---------|---------|---------|-----------|-------|
| Expenses | Create Bill | + New > Bill | Vendor | Criar, ver AP Aging | Screenshot AP | QBO |
| Expenses | Pay Bills | + New > Pay Bills | Bills | Pagar, AP reduz | Screenshot | QBO |
| Expenses | Expense | + New > Expense | Account | Criar expense | Screenshot | QBO |
| Expenses | AP Aging | Reports > AP Aging | Bills | Rodar report | Screenshot | QBO |
| Expenses | Bill Approval | Workflows | Advanced | Submeter aprovacao | Screenshot | Adv |

---

## Banking

| Area | Feature | UI Path | Pre-req | Validar | Evidencia | Fonte |
|------|---------|---------|---------|---------|-----------|-------|
| Banking | Connect | Banking > Add | Credenciais | Ver transacoes | Screenshot | QBO |
| Banking | Categorize | Banking > Review | Transacoes | Categorizar | Screenshot | QBO |
| Banking | Match | Banking > Review | Transacao | Match successful | Screenshot | QBO |
| Banking | Rules | Banking > Rules | Recorrentes | Criar rule | Screenshot | QBO |
| Banking | Reconcile | Banking > Reconcile | Categorizadas | Difference=0 | Screenshot | QBO |

---

## Inventory (Plus+)

| Area | Feature | UI Path | Pre-req | Validar | Evidencia | Fonte |
|------|---------|---------|---------|---------|-----------|-------|
| Inventory | Create Item | Settings > Products | Tracking on | Criar item | Screenshot | Plus |
| Inventory | Adjustment | + New > Qty Adj | Items | Ajustar qty | Screenshot | Plus |
| Inventory | Stock Status | Reports > Stock | Items | Ver report | Screenshot | Plus |
| Inventory | Valuation | Reports > Valuation | Transacoes | FIFO correct | Screenshot | Plus |

---

## Classes/Locations (Plus+)

| Area | Feature | UI Path | Pre-req | Validar | Evidencia | Fonte |
|------|---------|---------|---------|---------|-----------|-------|
| Tracking | Enable | Settings > Categories | Plus+ | Habilitar | Screenshot | Plus |
| Tracking | Create Class | Settings > Classes | Enabled | Criar class | Screenshot | Plus |
| Tracking | P&L by Class | Reports | Classes used | Ver report | Screenshot | Plus |
| Tracking | P&L by Location | Reports | Locations used | Ver report | Screenshot | Plus |

---

## Multi-Entity (Advanced)

| Area | Feature | UI Path | Pre-req | Validar | Evidencia | Fonte |
|------|---------|---------|---------|---------|-----------|-------|
| ME | Consolidated View | Company switcher | Entities | Acessar | Screenshot | Adv |
| ME | Intercompany | Accounting > IC | IC trans | Ver alocacoes | Screenshot | Adv |
| ME | Combined Reports | Reports | Data all | Report combina | Screenshot | Adv |

---

## Reports

| Area | Feature | UI Path | Pre-req | Validar | Evidencia | Fonte |
|------|---------|---------|---------|---------|-----------|-------|
| Reports | P&L | Reports > P&L | Transacoes | Numeros corretos | Screenshot | QBO |
| Reports | Balance Sheet | Reports > BS | Transacoes | Debits=Credits | Screenshot | QBO |
| Reports | Cash Flow | Reports > CF | Transacoes | Ver fluxo | Screenshot | QBO |
| Reports | Custom | Reports > Custom | Advanced | Criar custom | Screenshot | Adv |

---

## Users

| Area | Feature | UI Path | Pre-req | Validar | Evidencia | Fonte |
|------|---------|---------|---------|---------|-----------|-------|
| Users | Add User | Settings > Users | Admin | Adicionar | Screenshot | QBO |
| Users | Permissions | Settings > Users | User | Configurar | Screenshot | QBO |
| Users | Custom Role | Settings > Roles | Advanced | Criar role | Screenshot | Adv |

---

Ultima atualizacao: 2025-12-19
