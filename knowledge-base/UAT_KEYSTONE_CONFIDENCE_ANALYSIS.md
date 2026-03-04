# UAT Keystone - Analise de Confianca e Gaps Estrategicos

> Documento gerado: 2026-02-03
> Fonte: Testbook_Keystone_UAT_v.1.0.xlsx (58 testes)
> Cruzamento: Strategic Cortex + QBO_DEEP_MASTER + memory.md + LAYERS.md

---

## RESUMO EXECUTIVO

| Categoria | Testes | Confianca Media | Status |
|-----------|--------|-----------------|--------|
| **Acesso/Autenticacao** | 1 | 95% | COBERTO |
| **Navegacao Global** | 4 | 85% | COBERTO |
| **Home/Dashboard** | 8 | 75% | PARCIAL |
| **Multi-Entity** | 6 | 90% | COBERTO |
| **Accounting** | 5 | 80% | COBERTO |
| **Banking** | 3 | 70% | PARCIAL |
| **Sales & Get Paid** | 3 | 75% | PARCIAL |
| **Customers** | 1 | 85% | COBERTO |
| **Expenses & Pay Bills** | 3 | 80% | COBERTO |
| **Projects** | 3 | 90% | COBERTO |
| **Payroll** | 4 | 85% | COBERTO |
| **Team/Employees** | 2 | 80% | PARCIAL |
| **Time** | 2 | 75% | PARCIAL |
| **Reports** | 8 | 90% | COBERTO |
| **Settings** | 3 | 70% | PARCIAL |
| **Dimensions/Classes** | 1 | 85% | COBERTO |
| **Attachments** | 1 | 60% | GAP |
| **Performance/KPIs** | 1 | 70% | PARCIAL |

**Confianca Geral: 79%**

---

## ANALISE DETALHADA POR CATEGORIA

### 1. ACESSO / AUTENTICACAO
**Confianca: 95%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Login QBO + Keystone | CAMADA 1 LOCKED, layer1_login.py funcional | 95% | LAYERS.md |

**O que ja sabemos:**
- Login via CDP porta 9222 (Playwright)
- Email: quickbooks-test-account@tbxofficial.com (CONSTRUCTION)
- TOTP: 000000 para test users
- Company ID Keystone Parent: 9341454156620895
- Company ID Keystone Terra: 9341454156620204

**Gap (5%):**
- [ ] Confirmar se UAT usa mesmo email ou outro test user
- [ ] Validar se ambiente UAT e diferente do ambiente atual

---

### 2. NAVEGACAO GLOBAL
**Confianca: 85%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Barra superior (chips) | Validado em Winter Release | 90% | Evidence Pack |
| Menu lateral | Home, Feed, Reports, All apps documentados | 85% | QBO_DEEP_MASTER |
| Busca global | Funciona em TCO, nao testado Keystone | 75% | Inferencia |
| Create actions | Lista de acoes conhecida | 90% | QBO Manual |

**O que ja sabemos:**
- Chips: Accounting, Expenses, Sales, Customers, Payroll, Team, Time
- Menu lateral: Home, Feed, Reports, All apps
- Busca funciona com nome parcial

**Gap (15%):**
- [ ] Confirmar que busca global funciona em Keystone especifico
- [ ] Documentar lista exata de Create actions disponiveis no Keystone

---

### 3. HOME / DASHBOARD
**Confianca: 75%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Cash flow card | Validado em TCO | 80% | Winter Release |
| Profit and loss card | Validado em TCO | 85% | Winter Release |
| Bank accounts card | Validado em TCO | 80% | Winter Release |
| AR/AP cards | Validado em TCO | 85% | Winter Release |
| Invoices widget | Validado em TCO | 75% | Winter Release |
| Expenses widget | Validado em TCO | 70% | Winter Release |
| My integrations card | NAO DOCUMENTADO | 50% | - |
| Mileage card | NAO DOCUMENTADO | 40% | - |
| Feed | Existe no menu, nao detalhado | 65% | QBO Manual |

**O que ja sabemos:**
- Dashboard TCO bem documentado
- Cards Cash flow, P&L, Bank, AR/AP funcionais
- Keystone Construction DEVE ter mesmos cards (IES)

**Gap (25%):**
- [ ] **URGENTE:** Documentar My integrations card - nao temos info
- [ ] **URGENTE:** Verificar se Mileage existe em Construction
- [ ] Confirmar se Keystone tem TODOS os cards do TCO
- [ ] Feed: documentar estrutura e tipos de eventos

---

### 4. MULTI-ENTITY
**Confianca: 90%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Switch company | DOCUMENTADO (layer1_login.py) | 95% | LAYERS.md |
| Vista Consolidada | DOCUMENTADO e VALIDADA | 95% | Winter Release |
| P&L Consolidated | VALIDADO com screenshots | 95% | Evidence Pack |
| Balance Sheet Consolidated | VALIDADO (bug conhecido PLA-3201) | 85% | memory.md |
| Transicao ida/volta | TESTADO em validacao | 90% | Winter Release |
| Permissoes Consolidated | PARCIAL - 6 usuarios Intuit mapeados | 80% | memory.md |

**O que ja sabemos:**
- Keystone: Parent + Terra (child) + Vista Consolidada
- CIDs: 9341454156620895 (Parent), 9341454156620204 (Terra)
- Vista consolidada funciona
- Bug conhecido: IC Balance Sheet (PLA-3201 - ESCALATED)
- Usuarios Intuit com admin: qbdemoteam@intuit.com, akshit_agarwal, garrett_lusk, lawton, austin_alexander, sumit_kumar1

**Gap (10%):**
- [ ] Confirmar se bug PLA-3201 foi resolvido (impacta Balance Sheet Consolidated)
- [ ] Documentar permissoes especificas para cada tipo de usuario

---

### 5. ACCOUNTING
**Confianca: 80%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Chart of Accounts | 51 classifications TCO confirmadas | 85% | SQLite + memory.md |
| Registers | Funcional em TCO | 80% | Winter Release |
| Journal/General Ledger | Funcional em TCO | 80% | Winter Release |
| Tax/Sales Tax | PARCIAL - depende do tenant | 70% | QBO Manual |
| Company settings | DOCUMENTADO | 85% | QBO Manual |

**O que ja sabemos:**
- COA: Shared COA funcional (conta 1083 criada para IC)
- Registers: funcionam com filtros
- TCO tem 51 classifications em 8/9 facets

**Gap (20%):**
- [ ] Confirmar se Keystone Construction tem Sales Tax habilitado
- [ ] Documentar quais accounts sao especificas de Construction

---

### 6. BANKING
**Confianca: 70%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Lista de contas | Funcional em TCO | 75% | Winter Release |
| Reconciliation | Funcional em TCO | 70% | Winter Release |
| Rules | POUCO DOCUMENTADO | 60% | Linear PLA-2949 |

**O que ja sabemos:**
- Banking funciona em TCO
- Bank Rules: ticket PLA-2949 (BACKLOG)

**Gap (30%):**
- [ ] **IMPORTANTE:** Documentar Bank Rules no Keystone
- [ ] Confirmar ultimo reconcile disponivel
- [ ] Verificar se estados (For review, Categorized, Excluded) existem

---

### 7. SALES & GET PAID
**Confianca: 75%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Invoices | Overdue invoices normalizados TCO | 80% | QBO_DEEP_MASTER |
| Payments | Funcional em TCO | 75% | Winter Release |
| Estimates | POUCO DOCUMENTADO | 60% | - |

**O que ja sabemos:**
- Invoices: curated set com dias overdue realisticos (TCO)
- Payments: vinculacao com invoice funciona

**Gap (25%):**
- [ ] Documentar Estimates no Keystone Construction
- [ ] Verificar se existe filtro por status (Open, Overdue, Paid)

---

### 8. CUSTOMERS
**Confianca: 85%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Customer list + perfil | Shipping address columns adicionadas | 85% | QBO_DEEP_MASTER |

**O que ja sabemos:**
- Customer profiles com shipping address
- Customer notes re-ingested
- Tire Shop: 10K+ customers (teste de escala)

**Gap (15%):**
- [ ] Confirmar se Keystone tem customers suficientes para demo

---

### 9. EXPENSES & PAY BILLS
**Confianca: 80%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Bills | Canada: 474 PAID, 50 UNPAID selecionados | 85% | memory.md |
| Vendors | Vendor notes, CC/BCC (blocked on Intuit) | 80% | QBO_DEEP_MASTER |
| Expenses | Funcional em TCO | 75% | Winter Release |

**O que ja sabemos:**
- Bills: Canada dataset com 524 bills (474 PAID, 50 UNPAID)
- Vendors: notes adicionados, CC/BCC aguarda Intuit
- IC Expense Allocations: credit card credits manuais

**Gap (20%):**
- [ ] Confirmar status do vendor CC/BCC no Keystone
- [ ] Documentar expenses com attachments

---

### 10. PROJECTS
**Confianca: 90%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Projects list + dashboard | 6 projetos no dataset | 95% | memory.md |
| Project profitability | Funcional em Construction | 90% | Winter Release |
| Time entries vinculadas | PARCIAL | 80% | Linear PLA-2795 |

**O que ja sabemos:**
- 6 projetos: GaleGuardian, Sobey Stadium, Leap Labs, BMH, TidalWave, Azure Pines
- 45 employees no dataset
- Project profitability funciona

**Gap (10%):**
- [ ] Verificar ticket PLA-2795 (No time entries for IES Construction)

---

### 11. PAYROLL
**Confianca: 85%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Payroll overview | Funcional em Construction | 90% | Winter Release |
| Pay runs | Funcional em TCO | 85% | Winter Release |
| Employees list | 45 employees + duplicacao resolvida | 85% | memory.md |
| Payroll reports | Funcional em TCO | 80% | Winter Release |

**O que ja sabemos:**
- Payroll module habilitado
- Certified Payroll Report validado (WR-024)
- Keystone: 90 employees com erro -> ~86 duplicados deletados (2026-01-27)

**Gap (15%):**
- [ ] Confirmar se duplicacao foi 100% resolvida
- [ ] Validar Gross to Net report no Keystone

---

### 12. TEAM / EMPLOYEES
**Confianca: 80%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Employees list + perfil | 45 employees no dataset | 85% | memory.md |
| Org/Directory | NAO DOCUMENTADO | 60% | - |

**O que ja sabemos:**
- 45 employees no dataset Construction
- Profiles com employment info

**Gap (20%):**
- [ ] **URGENTE:** Documentar se Org Chart/Directory existe no Keystone
- [ ] Confirmar campos do employee profile

---

### 13. TIME
**Confianca: 75%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Time entries list | Ticket PLA-2795 (issues) | 70% | Linear |
| Approvals/Timesheets | NAO DOCUMENTADO | 60% | - |

**O que ja sabemos:**
- Time entries existem (PTO realistico mencionado)
- Ticket PLA-2795: No time entries for IES Construction (NEEDS REVIEW)

**Gap (25%):**
- [ ] **IMPORTANTE:** Resolver PLA-2795 antes do UAT
- [ ] Documentar Timesheets/Approvals workflow

---

### 14. REPORTS
**Confianca: 90%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Report list + busca | Funcional | 95% | Winter Release |
| P&L com filtros | Validado extensivamente | 95% | Evidence Pack |
| Balance Sheet | Validado (bug IC conhecido) | 85% | Winter Release |
| Cash Flows | Validado | 90% | Winter Release |
| AR/AP Aging | Funcional | 85% | Winter Release |
| Custom/Saved reports | 3 rows (weak data) | 70% | Evidence Pack |
| Exportacao PDF/Excel | Funcional | 90% | QBO Manual |
| Benchmarking/Performance | Loading issues conhecidos | 75% | Winter Release |

**O que ja sabemos:**
- Reports bem documentados
- P&L, Balance Sheet, Cash Flows funcionais
- Custom reports: dados fracos (3 rows) - precisa PopulateData

**Gap (10%):**
- [ ] Povoar custom_reports com mais dados
- [ ] Confirmar exportacao funciona no Keystone

---

### 15. SETTINGS
**Confianca: 70%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| All apps | Funcional | 80% | Winter Release |
| Connected apps | NAO DOCUMENTADO | 55% | - |
| Audit log | NAO DOCUMENTADO | 60% | - |

**O que ja sabemos:**
- All apps lista modulos
- Custom role "Project Custom" criado 1/20/2026 (descoberto investigacao)

**Gap (30%):**
- [ ] **URGENTE:** Documentar Connected apps no Keystone
- [ ] **URGENTE:** Documentar Audit log functionality

---

### 16. DIMENSIONS / CLASSES
**Confianca: 85%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Dimensions em reports | TCO: 51 classifications, 8/9 facets | 85% | memory.md |

**O que ja sabemos:**
- Classifications via EAV table
- Facets: class, store, division, location, product category, product type, customer type, service timing, retail auto service

**Gap (15%):**
- [ ] Confirmar se Keystone tem mesmos facets que TCO

---

### 17. ATTACHMENTS
**Confianca: 60%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Anexos em transacoes | POUCO DOCUMENTADO | 60% | QBO_DEEP_MASTER |

**O que ja sabemos:**
- Project attachments mencionados
- Contractor documents PDFs suportados

**Gap (40%):**
- [ ] **URGENTE:** Documentar workflow de attachments
- [ ] Testar abertura de anexo existente
- [ ] Confirmar tipos de arquivo suportados

---

### 18. PERFORMANCE / KPIs
**Confianca: 70%**

| Teste | Conhecimento Existente | Confianca | Fonte |
|-------|------------------------|-----------|-------|
| Performance Center | WR-014 com loading issues | 70% | Winter Release |

**O que ja sabemos:**
- Performance Center existe
- BI KPIs from Monday.com = Intuit responsibility
- Loading spinner conhecido (WR-014)

**Gap (30%):**
- [ ] Confirmar se Performance Center esta estavel
- [ ] Documentar KPIs disponiveis no Keystone

---

## MATRIZ DE GAPS PRIORITARIOS

### P0 - URGENTE (Impacta UAT diretamente)

| # | Gap | Area | Confianca Atual | Acao Necessaria |
|---|-----|------|-----------------|-----------------|
| 1 | Time entries IES Construction | Time | 70% | Resolver PLA-2795 |
| 2 | My integrations card | Home | 50% | Documentar se existe |
| 3 | Audit log | Settings | 60% | Documentar funcionalidade |
| 4 | Connected apps | Settings | 55% | Documentar lista e status |
| 5 | Attachments workflow | Attachments | 60% | Testar e documentar |

### P1 - IMPORTANTE (Pode impactar demonstracao)

| # | Gap | Area | Confianca Atual | Acao Necessaria |
|---|-----|------|-----------------|-----------------|
| 6 | Bank Rules | Banking | 60% | Verificar PLA-2949 |
| 7 | Org Chart/Directory | Team | 60% | Verificar se existe |
| 8 | Estimates | Sales | 60% | Documentar workflow |
| 9 | Mileage card | Home | 40% | Verificar se existe em Construction |
| 10 | IC Balance Sheet bug | Multi-Entity | 85% | Confirmar PLA-3201 status |

### P2 - DESEJAVEL (Melhora confianca)

| # | Gap | Area | Confianca Atual | Acao Necessaria |
|---|-----|------|-----------------|-----------------|
| 11 | Custom reports data | Reports | 70% | Povoar mais dados |
| 12 | Performance Center loading | KPIs | 70% | Verificar estabilidade |
| 13 | Timesheets/Approvals | Time | 60% | Documentar workflow |
| 14 | Feed structure | Home | 65% | Documentar tipos de eventos |
| 15 | Sales Tax em Construction | Accounting | 70% | Confirmar habilitacao |

---

## RECOMENDACOES DE ADICAO AO CONHECIMENTO ESTRATEGICO

### 1. Adicionar ao Strategic Cortex (OUTPUT_A)

```markdown
### Keystone UAT Readiness (2026-02-03)
| Aspecto | Status | Confianca |
|---------|--------|-----------|
| Login/Auth | READY | 95% |
| Multi-Entity | READY | 90% |
| Reports | READY | 90% |
| Projects | READY | 90% |
| Payroll | READY | 85% |
| **Time Entries** | **BLOCKED** | **70%** |
| **Attachments** | **GAP** | **60%** |
| **Settings (Audit)** | **GAP** | **60%** |
```

### 2. Adicionar ao memory.md

```markdown
### UAT Keystone Gaps (2026-02-03)
- PLA-2795: Time entries blocker - RESOLVER ANTES DO UAT
- Attachments: workflow nao documentado
- Audit log: funcionalidade nao testada
- My integrations: confirmar existencia
- Mileage: confirmar se existe em Construction
```

### 3. Criar novo arquivo: knowledge-base/UAT_KEYSTONE_CHECKLIST.md

Com checklist executavel baseado nos 58 testes do Excel, cruzado com os gaps identificados.

---

## COMO AUMENTAR A CONFIANCA

| De | Para | Acao |
|----|------|------|
| 79% | 85% | Resolver os 5 gaps P0 |
| 85% | 90% | Resolver os 5 gaps P1 |
| 90% | 95% | Documentar todos os P2 |

**Proximos passos para voce me ajudar:**
1. Confirmar status do PLA-2795 (Time entries)
2. Confirmar status do PLA-3201 (IC Balance Sheet)
3. Me dar acesso a testar: My integrations, Audit log, Attachments
4. Confirmar se Mileage e Org Chart existem em Construction

---

Documento gerado com base em triangulacao de fontes.
Confianca metodologica: 85% (fontes cruzadas: UAT, Strategic Cortex, memory.md, LAYERS.md, QBO_DEEP_MASTER)
