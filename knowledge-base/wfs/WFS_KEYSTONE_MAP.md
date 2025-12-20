# WFS Keystone Construction - Mapeamento de UI

**Data:** 2025-12-19
**Ambiente:** Keystone Construction Canada
**Conta:** thiago@testbox.com
**Objetivo:** Mapear funcionalidades QBO relevantes para WFS

---

## 1. Company Overview

| Metrica | Valor |
|---------|-------|
| Profit & Loss | -$346,508 (down 545%) |
| Expenses (30d) | $388,438 |
| Payroll expenses | $381,739 |
| Invoices unpaid | $1,666,730 |
| Invoices overdue | $1,665,263 |
| Bank balance | $11,392,356 |

**Tipo:** Empresa de construcao (ideal para job costing)

---

## 2. Payroll Overview

**Rota:** `/app/payroll`

**Submenu:**
- Overview
- Employees
- Payroll taxes
- Compliance

**TO DO LIST:**
- Pay overdue taxes (botao Pay)

**CELEBRATE Panel (WFS Feature!):**
| Employee | Evento | Data |
|----------|--------|------|
| Aiden Harris | Work anniversary | Dec 20th |
| Tyler Frazer | Work anniversary | Dec 21st |
| Sophia Brown | Birthday | Dec 21st |
| Chloe Nguyen | Birthday | Dec 26th |
| Varun Babar | Work anniversary | Dec 26th |

---

## 3. Employees

**Rota:** `/app/employees`

**Tabs:**
- List
- Directory
- Org chart

**Colunas:**
- NAME
- PAY RATE
- PAY METHOD
- **AVAILABLE VACATION** (PTO!)
- STATUS

**Employees (amostra):**
| Nome | Pay Rate | Tipo | Method | Status |
|------|----------|------|--------|--------|
| Acosta, Nita | $56.00/hour | Hourly | Paper cheque | Active |
| Ali, Anika | $75,000.00/y | Salary | Paper cheque | Active |
| Babar, Varun | $43,400.00/y | Salary | Paper cheque | Active |
| Benedict | $64,000.00/y | Salary | Paper cheque | Active |
| Birch, Vicki | $65.00/hour | Hourly | Paper cheque | Active |
| Brown, Sophia | $56.00/hour | Hourly | Paper cheque | Active |
| Cheng, Dan | $85,000.00/y | Salary | Paper cheque | Active |

**Caracteristicas:**
- Mix de hourly e salary employees
- Vacation tracking ativo
- Todos com Paper cheque
- Muitos mais employees que GoQuick

---

## 4. Diferenciais vs GoQuick Alpha Retail

| Feature | GoQuick Alpha | Keystone Construction |
|---------|---------------|----------------------|
| Employees | 3 | 7+ |
| Pay types | Salary only | Hourly + Salary |
| Vacation tracking | Nao visivel | **AVAILABLE VACATION** |
| Celebrations | Nao visivel | **Birthdays + Anniversaries** |
| Payroll expenses | Baixo | $381,739 |
| Industry | Retail | Construction |
| Job costing | Basico | **Ideal** |

---

## 5. Relevancia para WFS

### 5.1 PTO/Time Off
- Coluna AVAILABLE VACATION visivel
- Tracking de vacation days
- Ideal para demo story "Unified PTO"

### 5.2 Celebrations
- Panel CELEBRATE no Payroll
- Work anniversaries
- Birthdays
- Engajamento de funcionarios

### 5.3 Job Costing
- Empresa de construcao
- Mix de hourly/salary
- Projects module disponivel
- Time tracking por projeto

### 5.4 Scale
- Mais employees para demos realistas
- Dados financeiros significativos
- Payroll expenses altos ($381k)

---

## 6. Screenshots Capturados

| Arquivo | Descricao |
|---------|-----------|
| keystone_home.png | Dashboard com metricas |
| keystone/payroll.png | Payroll overview + Celebrations |
| keystone/employees.png | Lista de employees com PTO |

---

## 7. Recomendacao

**Para demos WFS, usar Keystone Construction porque:**
1. Mais employees (realismo)
2. Vacation tracking visivel
3. Celebrations panel (engagement)
4. Mix hourly/salary (complexidade)
5. Construction = job costing nativo
6. Dados financeiros robustos

**GoQuick Alpha Retail serve para:**
- Demos simples de payroll
- Setup inicial de WFS
- Cenarios de retail

---

Ultima atualizacao: 2025-12-19 11:45
