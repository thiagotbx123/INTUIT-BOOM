# WFS Alpha Retail - Mapeamento de UI

**Data:** 2025-12-19
**Ambiente:** GoQuick Alpha Retail
**Conta:** thiago@testbox.com
**Objetivo:** Mapear funcionalidades QBO relevantes para WFS

---

## 1. Company Info

| Campo | Valor |
|-------|-------|
| Name | GoQuick Alpha Retail |
| Address | 660 4th Ave, Seattle, WA 98104-1822 |
| Email | saubhagya_jena@intuit.com |
| Industry | Miscellaneous store retailers |

---

## 2. Modulos Mapeados

### 2.1 Payroll Overview

**Rota:** `/app/payroll`

**Submenu:**
- Overview
- Employees
- Contractors
- Payroll taxes
- HR advisor
- Compliance

**Features Identificadas:**
- Pay my team (paper checks ou direct deposit)
- Setup tasks: "Get ready to pay your team"
- Payday is set (configurado)
- Tax Penalty Protection (Inactive)
- Payroll expert setup disponivel

**Setup Resources:**
- View setup guide
- Set up your team (video 4:32)
- Connect your bank account (video 1:51)
- Run payroll with direct deposit (video 2:34)

---

### 2.2 Employees

**Rota:** `/app/employees`

**Tabs:**
- List (default)
- Directory
- Org chart

**Colunas da Lista:**
- NAME
- PAY RATE
- PAY METHOD
- STATUS

**Employees Existentes:**
| Nome | Pay Rate | Pay Method | Status |
|------|----------|------------|--------|
| Halpert, Jim | $55,000.00/year | Paper check | Active |
| Jane, Mary | $25,000.00/year | Paper check | Active |
| Philbin, Michael | $90,000.00/year | Paper check | Active |

**Acoes Disponiveis:**
- Find an employee (search)
- Filter: Active Employees
- Edit payroll items
- **Invite to Workforce** (integracao WFS!)
- Add an employee
- Privacy toggle

---

### 2.3 Time Tracking

**Rota:** `/app/timetracking`

**Interface:** Weekly Timesheet

**Campos por Entry:**
- Name (Select a team member)
- Week selector (ex: 12/14/2025 to 12/20/2025)
- Customers (dropdown)
- Service (dropdown)
- Billable (per hour) checkbox
- Grid de horas: Sun-Sat + Total + Billable
- Notes

**Acoes:**
- Cancel
- Copy last timesheet
- Save
- Save and new

**Integracao AI:**
- **Intuit Intelligence BETA** visivel
- "What can I do for you today?"
- Sugestoes: quarterly taxes, profit, customers, analyze files

---

### 2.4 Projects

**Rota:** `/app/projects`

**Status:** Modulo disponivel (carregando durante captura)

**Relevancia WFS:** Job costing - atribuir labor cost a projetos

---

### 2.5 Settings

**Rota:** `/app/settings`

**Categorias:**
- Company
- Usage
- Payments
- QuickBooks Checking
- Accounting
- Sales
- Expenses
- Time
- Advanced

---

## 3. Menu Lateral (MY APPS)

**Modulos Disponiveis:**
- Accounting
- Expenses & Bills
- Sales & Get Paid
- Customer Hub
- **Payroll** (expandido)
- **Team**
- **Time**
- **Projects**
- Inventory
- Sales Tax
- Business Tax
- Lending

**PINNED:**
- Accounting
- Expenses
- Sales

---

## 4. Pontos de Integracao WFS

### 4.1 Invite to Workforce
- Botao visivel em Employees
- Permite convidar employees para WFS
- Ponto de entrada para demo story

### 4.2 Payroll -> WFS Flow
- Employee criado em QBO
- Payroll configurado
- Invite to Workforce
- Employee acessa WFS

### 4.3 Time -> Payroll
- Timesheet preenchido
- Linked to Customer/Service
- Billable hours tracked
- Flows to payroll

### 4.4 Job Costing
- Projects module
- Time entries com Customer/Service
- Labor cost attribution

---

## 5. Dados para Demo

### Employees Disponiveis
- 3 employees ativos
- Todos com Paper check (pode mudar para Direct deposit)
- Mix de salarios ($25k, $55k, $90k)

### Timesheet
- Weekly view
- Pronto para entrada de horas
- Integracao com Customers e Services

---

## 6. Screenshots Capturados

| Arquivo | Descricao |
|---------|-----------|
| homepage.png | Dashboard principal |
| payroll.png | Payroll Overview |
| employees.png | Lista de employees |
| time.png | Weekly timesheet |
| projects.png | Projects module |
| reports.png | Lista de reports |
| settings.png | Company settings |

---

## 7. Proximos Passos

1. [ ] Mapear Org chart em detalhe
2. [ ] Verificar fluxo "Invite to Workforce"
3. [ ] Testar Time entry completo
4. [ ] Verificar Projects/Job costing
5. [ ] Mapear Reports relevantes para WFS
6. [ ] Acessar Mineral HR para comparacao

---

## 8. Observacoes

- **Intuit Intelligence BETA** ativo - AI assistant integrado
- **GoQuick** parece ser ambiente de teste/demo
- 3 employees ja configurados - bom para demos
- Payroll setup parcialmente completo
- Paper check como metodo de pagamento (pode ser mudado)

---

Ultima atualizacao: 2025-12-19 11:30
