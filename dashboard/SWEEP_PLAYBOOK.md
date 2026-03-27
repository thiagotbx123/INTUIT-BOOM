# QBO SWEEP PLAYBOOK — God Complete v8.1

> **Versao:** 8.1 (2026-03-27)
> **Profile:** God Complete (unico — nao existe outro modo)
> **Principio:** Abra cada tela, olhe TUDO como um especialista humano, corrija na hora.

---

## REGRAS ABSOLUTAS

1. **NUNCA marque uma tela como "acessivel" ou "HTTP 200"** — extraia dados concretos ou documente POR QUE nao conseguiu
2. **Se algo parece errado, PARE e corrija ANTES de avancar** — nao documente pra depois
3. **Cada tela tem output obrigatorio** — se falta algum campo, a tela NAO esta completa
4. **Interprete como humano** — "Client 1" nao e nome real. "$82M bank balance" pra construtora pequena nao e realista. Margem de 48% em construction nao existe.
5. **Corrija test/placeholder names SEMPRE** — qualquer coisa com "Test", "Sample", "Demo 3.5", "Example", "Foo", "TBX", "Lorem", "Client 1", "Vendor 1", "Account 1" deve ser renomeada para nome realista do setor. **TBX prefixes** em invoices, estimates, ou records indicam dados de teste — se o campo e editavel, renomear. Se nao e editavel (ex: invoice number gerado pelo sistema), documentar como CS3 finding com nota "system-generated, not editable". Se encontrou = PARAR e CORRIGIR AGORA. Nao documentar pra depois. O VALOR do sweep e CORRIGIR, nao listar.
6. **Company Settings (Legal Name, DBA) = NUNCA CORRIGIR** — mesmo que tenha "Testing_OBS_AUTOMATION", documentar mas NAO alterar
7. **Use QBO API para validar numeros do UI** — se UI diz $590K income mas API diz $500K, isso e finding
8. **Output compacto** — max 10 linhas JSON por tela

## REGRAS ANTI-SKIP (CRITICAS)

9. **TODAS as 46 telas sao OBRIGATORIAS** — T01 ate T46, sem excecao. O sweep NAO esta completo se parou no T15. T16-T46 cobrem Payroll, Time, Tax, Recurring, Fixed Assets, Revenue Recognition, Budgets, Classes, Workflows, Custom Fields, Settings, Reconciliation, Invoice/Bill detail, POs, Reports, AI Features, Surface Scan. TODAS devem ser executadas.
10. **Child entities P0 devem ter metricas REAIS em T03-T15** — NAO copiar "shared data model" ou "same as parent". Cada entity tem seus proprios numeros. Navegar ate a tela, extrair dados, registrar JSON. Se os numeros forem iguais ao parent, ISSO e um finding (dados compartilhados indevidamente).
11. **Child entities P0: T01-T15 COMPLETO com dados** — mesma profundidade que parent. Nao reduzir. Nao resumir. Cada tela visitada individualmente com output JSON.
12. **P1 entities: minimo T01+T02+T05+T06 com metricas** — rapido mas com dados reais, nao "PASS".
13. **Se o contexto estiver grande: usar /compact e CONTINUAR** — nunca parar no meio. Se preciso, dividir em fases (T01-T15 numa sessao, T16-T46 na proxima), mas NUNCA pular telas.
14. **Gerar report SOMENTE apos T46 completo** — o report final so pode ser escrito depois que TODAS as telas foram verificadas. Report gerado antes de T46 e INCOMPLETO.
15. **NUNCA usar Agent tool para telas do sweep** — subagents/background agents NAO tem acesso ao browser (Playwright MCP). Toda navegacao, extracao e fix deve ser feita na sessao principal, sequencialmente. Delegar telas para subagents = telas nao executadas.

## FERRAMENTAS DISPONIVEIS

| Ferramenta | Quando Usar | Como |
|------------|-------------|------|
| Playwright MCP | Navegacao, clicks, forms, screenshots | browser_navigate, browser_evaluate, browser_click |
| QBO API MCP | Validar dados financeiros, buscar records | search_accounts, search_invoices, search_customers, etc. |
| JS Extractors | Extracao rapida de dados da pagina | browser_evaluate com funcao do extractor |
| Python (Bash) | Tracking de progresso, calculos | python -c "..." |

## BENCHMARKS POR SETOR

### Construction
- Margem: 3-15% (thin margins, high volume)
- Bank balance: $50K-$5M (proporcional ao porte)
- AR aging: < 60 days ideal, > 90 days = problema
- AP: overdue < 30% do total
- Employees: 5-50 tipico
- Products: services (Framing, Electrical, HVAC) + materials inventory
- Projects: com fases, budgets, job costing
- Customers: developers, municipios, school districts
- Vendors: subcontractors, material suppliers

### Tire Shop / Auto Retail
- Margem: 25-35% (retail + service markup)
- Bank balance: $20K-$500K
- Customers: fleet accounts, walk-in retail
- Products: tires (inventory) + services (rotation, alignment)
- Vendors: Bridgestone, Michelin, Goodyear (distributors)

### Non-Profit
- Margem: 2-10% (surplus, NOT profit — usar terminologia NP)
- Donors (not customers), Pledges (not invoices), Programs (not products)
- Revenue: grants, donations, program fees
- Classes: program tracking (Youth, Health, Emergency)
- Reports: Statement of Activity (not P&L)

### Professional Services
- Margem: 20-40% (high-value consulting)
- Clients: enterprises (IT, Health, Government)
- Products: service lines (Strategy, Integration, Analytics)
- Time tracking: billable hours critical
- Projects: SOWs with milestones

### Manufacturing
- Margem: 15-25% (product-based with COGS)
- Customers: distributors, retailers, OEM buyers
- Vendors: raw material suppliers
- Inventory: materials, WIP, finished goods

---

## FASE 0: LOGIN E CONTEXTO

### Procedimento
1. Ler credenciais do SWEEP_ACTIVATION.md (email, referencia ao QBO_CREDENTIALS.json)
2. Gerar TOTP: `python -c "import pyotp; print(pyotp.TOTP('SECRET').now())"`
3. Navegar para https://accounts.intuit.com/app/sign-in
4. Login com email + TOTP
5. Selecionar entity no company picker
6. Confirmar entity ativa no header

### Context Mapping
- Identificar o setor do dataset (construction/tire/nonprofit/etc)
- Carregar benchmarks correspondentes (secao acima)
- Listar todas entities do account (parent + children)

### Ordem de Execucao por Entity (OBRIGATORIA)
```
1. PARENT ENTITY: T01-T46 COMPLETO (todas 46 telas com output JSON)
2. P0 CHILD 1:    T01-T15 COMPLETO com metricas reais (nao copiar do parent)
3. P0 CHILD 2:    T01-T15 COMPLETO com metricas reais (nao copiar do parent)
4. P1 CHILDREN:   T01+T02+T05+T06 com dados reais para CADA um
5. CROSS-ENTITY:  X01-X07 validacao
6. REPORT FINAL:  SOMENTE apos tudo acima completo
```

**PROIBIDO:**
- Marcar T03-T15 de child entity como "shared data model" ou "same as parent" — CADA entity tem seus numeros
- Parar no T15 e gerar report — T16-T46 sao OBRIGATORIAS para parent
- Detectar CS violation e NAO corrigir — se "Client 1" aparece, RENOMEAR na hora

**PROFUNDIDADE OBRIGATORIA EM CHILD ENTITIES P0:**
Para cada child entity P0 (ex: Terra, BlueCraft), as telas T03-T15 DEVEM ter metricas extraidas via navegacao real no browser:
- T03 Balance Sheet: totalAssets, totalLiabilities, totalEquity, a_equals_le (NAO "1 metric")
- T04 Banking: accounts, balances, pending_txns (NAO "1 metric")
- T05 Customers: customer_count, overdue, ar_total (NAO "1 metric")
- T06 Vendors: vendor_count, overdue_bills, ap_total (NAO "1 metric")
- T07 Employees: employee_count, payroll_enabled (NAO "1 metric")
- T08 Products: product_count, types (NAO "1 metric")
- T09-T15: cada tela com MINIMO 2 metricas reais

Se uma tela de child entity tem apenas 1 metrica no JSON, ela NAO esta completa. Navegar de novo e extrair dados reais.

### Output:
```json
{"phase": "LOGIN", "entity": "NAME", "cid": "CID", "sector": "SECTOR", "entity_count": N}
```

---

## TELA 1: DASHBOARD (/app/homepage)

### Como navegar
URL: `https://qbo.intuit.com/app/homepage`
Esperar: 10s para widgets carregarem

### O que olhar (checklist visual)
- [ ] **Income widget**: valor positivo? Proporcional ao setor?
- [ ] **Expenses widget**: existe? Proporcional ao income?
- [ ] **Net Profit widget**: POSITIVO obrigatorio (empresa nao funciona com prejuizo consistente)
- [ ] **Bank Balance widget**: proporcional ao porte da empresa?
- [ ] **P&L chart**: periodo correto? (Last 30 days, This Year?) Grafico com dados?
- [ ] **Invoices widget**: tem invoices? Overdue ratio < 30%?
- [ ] **Cash flow graph**: presente? Positivo?
- [ ] **AI Agent tiles**: presentes? (IES feature)
- [ ] **Business Feed**: tem atividade recente?
- [ ] **Graficos vazios**: NENHUM grafico deve estar completamente vazio
- [ ] **TBX/Test markers**: qualquer texto "TBX", "Test", "Sample" = CS3 violation

### Julgamento critico
- Net Profit negativo em Construction/Tire/Services = PROBLEMA GRAVE. Empresa real nao opera com prejuizo.
  - Excecao: Non-Profit pode ter deficit temporario em alguns periodos
- Bank Balance > $50M para construtora media = INFLACAO de ciclo anterior. Documentar como P2.
- Income = $0 = entity vazia. Precisa de dados. Criar JE se necessario.
- Todos os widgets devem ter numeros. Widget mostrando "$0" ou vazio = investigar.

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Net Profit negativo | Criar JE: DR Accounts Receivable / CR Revenue | Playwright → /app/journalentry |
| Grafico vazio | Verificar periodo (mudar pra "This Year"). Se ainda vazio, criar transacoes | Playwright |
| Bank inflado ($50M+) | Documentar como P2 — nao fixavel via UI | Nenhuma |
| Widget de Income = $0 | Criar invoices/revenue via JE | Playwright |
| TBX/Test text visivel | Identificar source e renomear | Playwright |

### Extractor JS (colar no browser_evaluate)
```javascript
() => {
  const t = document.body.innerText || '';
  const nums = t.match(/\$[\d,.]+[KMB]?/g)?.slice(0, 8) || [];
  const hasTBX = /\bTBX\b/i.test(t);
  const hasTest = /\b(test|sample|demo\s*\d|example|foo|lorem|placeholder)\b/i.test(t);
  const has404 = /not found|404/i.test(t);
  const filter = t.match(/(Last 30 days|This month|This quarter|This year|Last fiscal year)/i)?.[1] || 'unknown';
  return JSON.stringify({nums, hasTBX, hasTest, has404, filter, bodyLen: t.length});
}
```

### Validacao API
- `search_accounts` com filter "Bank" → confirmar bank balance matches widget
- Se divergencia > 10% → finding

### Output obrigatorio
```json
{
  "screen": "T01_DASHBOARD",
  "entity": "...",
  "metrics": {"income": X, "expenses": Y, "net_profit": Z, "bank_balance": W, "period_filter": "..."},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 2: PROFIT & LOSS (/app/standardreports → Profit and Loss)

### Como navegar
1. URL: `https://qbo.intuit.com/app/standardreports`
2. Esperar 5s
3. Clicar no link "Profit and Loss"
4. Esperar 10s para report carregar
5. **IMPORTANTE**: Resize viewport para 1400x8000 para forcar virtual scroll a renderizar tudo

### O que olhar (checklist visual)
- [ ] **Total Income**: valor positivo? Proporcional ao setor?
- [ ] **COGS**: existe? (obrigatorio para manufacturing, tire_shop, construction com materials)
- [ ] **Gross Profit**: Income - COGS = positivo?
- [ ] **Total Expenses**: proporcional ao income? (tipico: 60-90% do income)
- [ ] **Net Operating Income**: POSITIVO obrigatorio
- [ ] **Net Income**: POSITIVO obrigatorio
- [ ] **Margin**: dentro do benchmark do setor?
- [ ] **Expense line items**: nomes realistas? Nenhum "Test Expense", "Account 1"?
- [ ] **Revenue lines**: diversificados? (nao so 1 conta de revenue)
- [ ] **Other Income/Expenses**: se existem, proporcionais?
- [ ] **Negative line items**: alguma despesa negativa? (reversal ou erro?)
- [ ] **Report period**: "January - March 2026" ou similar (nao "All Dates" infinito)

### Julgamento critico
- Margin > 50% em Construction = IRREALISTA. Construtoras operam em 3-15%.
- Income < $10K para empresa com 50+ projects = DESPROPORCIONAL
- Single revenue line = pouco realista. Empresa real tem 2-5 fontes de receita.
- Payroll Expenses negativos = ERRO (nao existe payroll negativo em operacao normal)
- COGS = $0 mas tem Inventory products = INCONSISTENTE (verificar em D08)

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Net Income negativo | Criar JE: DR AR / CR Revenue por valor suficiente | Playwright → /app/journalentry |
| Margin fora do setor | Documentar como finding. Se muito fora (>2x), ajustar via JE | Playwright |
| Conta com nome "Test" | Nao renomear COA (afeta reports). Documentar como CS3 | Documentar |
| Expense negativo | Investigar source. Se reversal incorreto, criar JE corretivo | Playwright |
| Income = $0 | Criar JE de receita compativel com setor | Playwright |

### Extractor JS
```javascript
() => {
  const t = document.body.innerText || '';
  const lines = t.split('\n');
  const result = {};
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i].trim();
    const getAmt = (idx) => { const next = lines.slice(idx, idx+3).join(' '); const m = next.match(/-?\$[\d,.]+/); return m ? m[0] : null; };
    if (/^Total\s+(for\s+)?Income$/i.test(l)) result.totalIncome = getAmt(i);
    if (/^Total\s+(for\s+)?Expenses$/i.test(l)) result.totalExpenses = getAmt(i);
    if (/^Net Operating Income$/i.test(l)) result.netOperating = getAmt(i);
    if (/^Net Income$/i.test(l)) result.netIncome = getAmt(i);
    if (/^Gross Profit$/i.test(l)) result.grossProfit = getAmt(i);
    if (/^Total.*Cost of Goods/i.test(l)) result.cogs = getAmt(i);
  }
  const testNames = t.match(/\b(test|sample|demo\s*\d|example|foo|placeholder)\b/gi) || [];
  result.csViolations = [...new Set(testNames)];
  return JSON.stringify(result);
}
```

### Validacao API
- `search_accounts` com AccountType "Income" → somar balances → comparar com Total Income do report
- Divergencia > 5% → finding

### Output obrigatorio
```json
{
  "screen": "T02_PNL",
  "entity": "...",
  "metrics": {"total_income": X, "cogs": Y, "gross_profit": Z, "total_expenses": W, "net_operating": V, "net_income": U, "margin_pct": M},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 3: BALANCE SHEET (/app/standardreports → Balance Sheet)

### Como navegar
1. URL: `https://qbo.intuit.com/app/standardreports`
2. Clicar "Balance Sheet"
3. Esperar 12s (BS carrega mais lento que P&L)
4. Resize viewport 1400x8000

### O que olhar
- [ ] **Total Assets**: valor positivo
- [ ] **Total Liabilities**: existe? Proporcional?
- [ ] **Total Equity**: positivo? (equity negativa = empresa tecnicamente insolvente)
- [ ] **A = L + E**: OBRIGATORIO que bata. Se nao bate = BUG CRITICO
- [ ] **Bank Accounts**: valor compativel com D01 dashboard
- [ ] **Accounts Receivable**: compativel com D05 customers
- [ ] **Accounts Payable**: compativel com D06 vendors
- [ ] **Fixed Assets**: se negativo, aceitavel por depreciacao acumulada
- [ ] **Retained Earnings**: existe? Proporcional ao historico da empresa?
- [ ] **Net Income (na secao Equity)**: deve bater com P&L net income (T02)

### Julgamento critico
- A ≠ L+E = BUG CRITICO. Nunca deve acontecer em QBO.
- Equity negativa = empresa insolvente. Se nao e intencional, precisa de JE de capital contribution.
- AR na BS deve bater com total de invoices abertas (cross-check T02↔T05)
- AP na BS deve bater com bills em aberto (cross-check T02↔T06)
- Bank na BS deve bater com Banking page (cross-check T01↔T04)

### Extractor JS
```javascript
() => {
  const t = document.body.innerText || '';
  const lines = t.split('\n');
  const r = {};
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i].trim();
    const getAmt = (idx) => { const next = lines.slice(idx, idx+3).join(' '); const m = next.match(/-?\$[\d,.]+/); return m ? m[0] : null; };
    if (/^Total\s+(for\s+)?Assets$/i.test(l)) r.totalAssets = getAmt(i);
    if (/^Total\s+(for\s+)?Liabilities$/i.test(l)) r.totalLiabilities = getAmt(i);
    if (/^Total\s+(for\s+)?Equity$/i.test(l)) r.totalEquity = getAmt(i);
    if (/^Total Liabilities and Equity$/i.test(l)) r.totalLiabEquity = getAmt(i);
    if (/^Total\s+(for\s+)?Accounts Receivable/i.test(l)) r.ar = getAmt(i);
    if (/^Total\s+(for\s+)?Accounts Payable/i.test(l)) r.ap = getAmt(i);
    if (/^Total\s+(for\s+)?Bank Accounts/i.test(l)) r.bank = getAmt(i);
    if (/^Retained Earnings/i.test(l)) r.retainedEarnings = getAmt(i);
    if (/^Net Income/i.test(l)) r.netIncome = getAmt(i);
  }
  return JSON.stringify(r);
}
```

### Validacao cruzada
- r.netIncome DEVE = T02.net_income (P&L cross-ref)
- r.bank DEVE ≈ T01.bank_balance (Dashboard cross-ref)
- A = L + E (calcular: totalLiabilities + totalEquity == totalAssets)

### Output obrigatorio
```json
{
  "screen": "T03_BALANCE_SHEET",
  "entity": "...",
  "metrics": {"total_assets": X, "total_liabilities": Y, "total_equity": Z, "a_equals_le": true/false, "ar": A, "ap": B, "bank": C, "net_income_equity": D},
  "cross_refs": {"pnl_net_match": true/false, "dashboard_bank_match": true/false},
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 4: BANKING (/app/banking?jobId=accounting)

### Como navegar
URL: `https://qbo.intuit.com/app/banking?jobId=accounting`
Esperar: 6s

### O que olhar
- [ ] **Account list**: quais contas bancarias existem?
- [ ] **QB Balance vs Bank Balance**: discrepancia grande?
- [ ] **Pending transactions**: quantas? (0 = nao tem bank feed ou tudo categorizado)
- [ ] **For Review tab**: transacoes aguardando categorizacao?
- [ ] **Categorized tab**: transacoes categorizadas aguardando aprovacao?
- [ ] **Bank feed status**: conectado? Error 103 (stale)? Ultimo sync?
- [ ] **Bank Rules**: existem? (5-10 regras = bom demo)
- [ ] **Reconciliation status**: ultima reconciliacao quando?

### Julgamento critico
- QB Balance $460K vs Bank Balance $8.4M = DISCREPANCIA MASSIVA. Prior cycle artifact.
- Error 103 = bank feed desconectado ha 449+ days. Comum em envs de teste.
- 0 pending + 0 categorized = bank feed inativo (nao necessariamente problema)
- Bank Rules = 0 → feature nunca configurada (oportunidade pra melhorar score)

### Se encontrar problema
| Problema | Acao |
|----------|------|
| Error 103 | Tentar reconectar. Se falhar, documentar |
| QB vs Bank discrepancia > $1M | Documentar como P2 |
| 0 bank rules | Criar 3-5 rules basicas se tempo permitir |

### Output obrigatorio
```json
{
  "screen": "T04_BANKING",
  "entity": "...",
  "metrics": {"accounts": [{"name": "...", "qb_balance": X, "bank_balance": Y}], "pending_txns": N, "bank_rules": N, "bank_feed_status": "connected|error_103|disconnected", "last_reconciled": "date"},
  "cross_refs": {"bs_bank_match": true/false},
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 5: CUSTOMERS (/app/customers)

### Como navegar
URL: `https://qbo.intuit.com/app/customers`
Esperar: 6s

### O que olhar
- [ ] **Customer count**: quantos? (proporcional ao setor)
- [ ] **Customer names**: TODOS realistas? Nenhum "Test", "Client 1", "TESTER", "12345 Auction", "Foo"?
- [ ] **Balances**: algum com $0? Algum com valor absurdo ($20B)?
- [ ] **Contact info**: emails e phones preenchidos? (top 5 pelo menos)
- [ ] **Overdue invoices**: quantas? % do total?
- [ ] **Open invoices**: quantas? Valores proporcionais?
- [ ] **Customer Hub widgets**: estimates count, unbilled income
- [ ] **Phone numbers**: formato realista? (nao "000-000-0000")
- [ ] **Emails**: dominio realista? (nao test@test.com)

### Julgamento critico (Construction)
- Customers devem ser: developers, municipios, school districts, HOAs, property managers
- Nomes como "Client 1", "Test Customer", "John Doe" = CS3 → RENOMEAR
- AR total $105M para construtora media = INFLACAO (prior cycle). Documentar P2.
- < 5 customers para empresa com 30+ projects = DESPROPORCIONAL

### Validacao API
- `search_customers` → comparar count e top balances com UI
- `search_invoices` com filter "overdue" → comparar com widget

### Output obrigatorio
```json
{
  "screen": "T05_CUSTOMERS",
  "entity": "...",
  "metrics": {"customer_count": N, "overdue_invoices": N, "overdue_amount": X, "open_invoices": N, "open_amount": Y, "ar_total": Z, "estimates": N},
  "cs_violations": ["Test Customer renamed to...", ...],
  "cross_refs": {"bs_ar_match": true/false},
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 6: VENDORS (/app/vendors)

### Como navegar
URL: `https://qbo.intuit.com/app/vendors`
Esperar: 6s

### O que olhar
- [ ] **Vendor count**: proporcional ao setor
- [ ] **Vendor names**: TODOS realistas? Nenhum "Foo Vendor", "Vendor1", "Test Supplier"?
- [ ] **Overdue bills**: quantas? Valor total?
- [ ] **Open bills**: quantas? Proporcional ao AP da BS?
- [ ] **1099 vendors**: algum marcado como contractor?
- [ ] **Contact info**: emails/phones nos top 5?
- [ ] **Balances**: algum absurdo?

### Julgamento critico (Construction)
- Vendors devem ser: subcontractors (electrician, plumber), material suppliers (ProBuild, HD Supply), equipment rental
- "Foo Materials", "Test Vendor" = CS3 → RENOMEAR para nome realista
- 254 overdue bills = provavel prior cycle data. Se AP na BS < $2M, aceitavel.
- Vendor sem bills = fantasma. Se > 30% sem transacoes, considerar inativar.

### Validacao API
- `search_vendors` → comparar count e names
- `search_bills` com filter "overdue" → comparar com UI widget

### Output obrigatorio
```json
{
  "screen": "T06_VENDORS",
  "entity": "...",
  "metrics": {"vendor_count": N, "overdue_bills": N, "overdue_amount": X, "open_bills": N, "open_amount": Y, "ap_total": Z, "contractor_1099": N},
  "cs_violations": [],
  "cross_refs": {"bs_ap_match": true/false},
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 7: EMPLOYEES (/app/employees?jobId=team)

### Como navegar
URL: `https://qbo.intuit.com/app/employees?jobId=team`
Esperar: 6s

### O que olhar
- [ ] **Employee count**: proporcional ao setor
- [ ] **Employee names**: TODOS realistas? Nenhum "Test Employee", "John Doe"?
- [ ] **Pay rates**: preenchidos? Proporcionais? ($20/hr hourly, $80-150K salary)
- [ ] **Pay method**: paper check vs direct deposit (mix realista)
- [ ] **Status**: Active vs Terminated? (100% active = ok para demo)
- [ ] **Warnings**: "Missing" pay rate? "Missing" direct deposit info?
- [ ] **Payroll**: Run Payroll button disponivel?
- [ ] **Next payroll due**: data visivel?
- [ ] **Workers comp**: banner presente? (California entities)

### Julgamento critico
- Pay rate "Missing" = PROBLEMA. Todo employee deve ter rate definido.
- 0 employees em entity com payroll ativado = INCONSISTENTE
- Salary de $1M/year para construction worker = IRREALISTA
- Mix de hourly ($15-50/hr) + salary ($60-150K) = realista para construction

### Se encontrar problema
| Problema | Acao |
|----------|------|
| Employee name "Test" | Renomear via Edit employee |
| Missing pay rate | Editar employee, definir rate realista |
| 0 employees mas Payroll ON | Documentar inconsistencia |

### Output obrigatorio
```json
{
  "screen": "T07_EMPLOYEES",
  "entity": "...",
  "metrics": {"employee_count": N, "active": N, "hourly": N, "salary": N, "missing_pay_rate": N, "pay_methods": {"paper_check": N, "direct_deposit": N}, "payroll_enabled": true/false, "run_payroll_available": true/false, "next_payroll_due": "date"},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 8: PRODUCTS & SERVICES (/app/items)

### Como navegar
URL: `https://qbo.intuit.com/app/items`
Esperar: 5s

### O que olhar
- [ ] **Product count**: proporcional ao setor (15-50 typical)
- [ ] **Product types**: Service, Inventory, Non-inventory, Bundle — diversidade?
- [ ] **Product names**: TODOS realistas? Nenhum "Test Product", "Item 1", "Sample Widget"?
- [ ] **Prices**: definidos? Proporcionais ao setor?
- [ ] **Descriptions**: preenchidas? (top 5 pelo menos)
- [ ] **SKUs**: preenchidos? (para inventory items)
- [ ] **Categories**: organizados por categoria?
- [ ] **Inactive items**: algum? Proporcional?

### Julgamento critico (Construction)
- Products devem ser: Framing, Electrical, HVAC, Plumbing, Concrete, etc. (services)
- Materials: Lumber, Drywall, Pipe, Wire (inventory)
- "Product 1", "Test Service" = CS3 → RENOMEAR
- 0 inventory items mas COGS > $0 na P&L = INCONSISTENTE
- Price = $0 para todos = POUCO REALISTA

### Validacao API
- `search_items` → comparar count e tipos com UI

### Output obrigatorio
```json
{
  "screen": "T08_PRODUCTS",
  "entity": "...",
  "metrics": {"product_count": N, "types": {"service": N, "inventory": N, "non_inventory": N, "bundle": N}, "with_price": N, "with_description": N},
  "cs_violations": [],
  "cross_refs": {"pnl_cogs_has_inventory": true/false},
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 9: PROJECTS (/app/projects)

### Como navegar
URL: `https://qbo.intuit.com/app/projects`
Esperar: 6s

### O que olhar
- [ ] **Project count**: proporcional (10-40 para construction)
- [ ] **Project names**: TODOS realistas? NENHUM com "Test", "Demo", "Example", "TestProjectPMAgent", "Test 123"?
- [ ] **Income vs Costs**: projects com dados financeiros?
- [ ] **Profit margins**: algum negativo? (project perdendo dinheiro?)
- [ ] **Status diversity**: In Progress, Completed, Not Started — mix realista?
- [ ] **Customers linked**: cada project tem customer associado?
- [ ] **Date ranges**: datas realistas? (nao 2019 em project "2025")
- [ ] **Time tracked**: projetos com horas registradas?
- [ ] **Budget**: projetos com budget definido? (construction = sim)

### Julgamento critico (Construction)
- Project names devem ser: "Cedar Ridge Community Center Renovation 2026", "Intuit Dome 2025", etc.
- "Test 123", "TestProjectPMAgent", "Nadia's Test Project" = CS3 → RENOMEAR IMEDIATAMENTE
  - Use nomes realistas: "Hawthorne Plaza Renovation 2025", "Summit Ridge Foundation Work", "Riverside Commons Phase II"
- Project com $0 income E $0 costs = vazio. Se > 50% estao vazios, finding.
- Margin negativa > -20% = investigar (project perdendo muito dinheiro)

### ATENCAO ESPECIAL: Test Name Detection
```
Regex expandido para detectar ALL test names:
/\b(test\s*\d|test[_\-\s]\w|test[A-Z]\w|testing\b|tester\b|demo\s*\d|demo\s+project|example\s+proj|sample\b|dummy\b|fake\b|temp\b|tmp\b)\b/gi
```
Se o regex encontrar QUALQUER match:
1. Click no project
2. Click "Edit"
3. Mudar nome para nome realista do setor
4. Save and close
5. Verificar que rename funcionou

### Output obrigatorio
```json
{
  "screen": "T09_PROJECTS",
  "entity": "...",
  "metrics": {"project_count": N, "with_income": N, "with_costs": N, "negative_margin": N, "empty_projects": N, "status": {"in_progress": N, "completed": N, "not_started": N}},
  "cs_violations": ["Renamed 'Test 123' to 'Hawthorne Plaza Renovation 2025'", ...],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 10: INVOICES (/app/invoices?jobId=sales-payments)

### Como navegar
URL: `https://qbo.intuit.com/app/invoices?jobId=sales-payments`
Esperar: 5s

### O que olhar
- [ ] **Invoice count**: proporcional ao setor
- [ ] **Status mix**: Paid, Open, Overdue, Partial — diversidade?
- [ ] **Customer names on invoices**: realistas?
- [ ] **Amounts**: proporcionais? (construction: $5K-$500K per invoice typical)
- [ ] **Dates**: distribuidas no tempo? (nao tudo no mesmo dia)
- [ ] **Line items**: preenchidos? Nomes realistas?
- [ ] **Invoice numbers**: sequenciais? Formato profissional?
- [ ] **Overdue %**: < 30% ideal, > 50% = problema

### Validacao API
- `search_invoices` → confirmar count e status breakdown

### Output obrigatorio
```json
{
  "screen": "T10_INVOICES",
  "entity": "...",
  "metrics": {"total_invoices": N, "status": {"paid": N, "open": N, "overdue": N, "partial": N}, "overdue_pct": P, "total_amount": X, "avg_amount": Y},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 11: BILLS (/app/bills)

### Como navegar
URL: `https://qbo.intuit.com/app/bills`
Esperar: 5s

### O que olhar
- [ ] **Bill count**: proporcional
- [ ] **Status**: Paid, Open, Overdue — mix realista?
- [ ] **Vendor names**: realistas?
- [ ] **Amounts**: proporcionais ao setor
- [ ] **Due dates**: distribuidas?
- [ ] **Overdue %**: < 30% ideal

### Output obrigatorio
```json
{
  "screen": "T11_BILLS",
  "entity": "...",
  "metrics": {"total_bills": N, "status": {"paid": N, "open": N, "overdue": N}, "overdue_pct": P, "total_amount": X},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 12: EXPENSES (/app/expenses)

### Como navegar
URL: `https://qbo.intuit.com/app/expenses`
Esperar: 5s

### O que olhar
- [ ] **Expense count**: proporcional
- [ ] **Categories**: diversos? (Office, Equipment, Travel, etc.)
- [ ] **Amounts**: proporcionais
- [ ] **Payment methods**: credit card, check, cash — mix?
- [ ] **Vendors on expenses**: realistas?
- [ ] **Receipts attached**: algum? (feature check)

### Output obrigatorio
```json
{
  "screen": "T12_EXPENSES",
  "entity": "...",
  "metrics": {"expense_count": N, "categories": N, "payment_methods": N, "with_receipts": N, "total_amount": X},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 13: ESTIMATES (/app/estimates)

### Como navegar
URL: `https://qbo.intuit.com/app/estimates`
Esperar: 5s

### O que olhar
- [ ] **Estimate count**: proporcional (construction: 10-50)
- [ ] **Status diversity**: Pending, Accepted, Closed, Expired, Converted — mix?
- [ ] **Customer names**: realistas?
- [ ] **Amounts**: proporcionais ao setor
- [ ] **Converted to invoice %**: alguma conversao aconteceu?
- [ ] **Names/descriptions**: realistas? Nenhum "Estimate 1"?

### Output obrigatorio
```json
{
  "screen": "T13_ESTIMATES",
  "entity": "...",
  "metrics": {"estimate_count": N, "status": {"pending": N, "accepted": N, "closed": N, "expired": N, "converted": N}, "total_amount": X},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 14: CHART OF ACCOUNTS (/app/chartofaccounts?jobId=accounting)

### Como navegar
URL: `https://qbo.intuit.com/app/chartofaccounts?jobId=accounting`
Esperar: 6s

### O que olhar
- [ ] **Account count**: 40-100 typical
- [ ] **Account types**: Bank, AR, AP, Fixed Assets, Equity, Income, COGS, Expense, Other — completude?
- [ ] **Account names**: TODOS realistas? Nenhum "Account 1", "Test Account", "TBX"?
- [ ] **Hierarchy**: sub-accounts existem? (2-3 levels typical)
- [ ] **Negative balances**: quais? Justificaveis? (depreciation = ok, revenue negativa = problema)
- [ ] **Inactive accounts**: quantas? Proporcional?
- [ ] **Account numbers**: habilitados? Sequenciais?
- [ ] **Descriptions**: top accounts tem descricao?

### Julgamento critico
- COA e a espinha dorsal. Contas com nomes genericos degradam toda a experiencia.
- "Miscellaneous" sozinha com 90% dos expenses = POUCA DIVERSIDADE
- Construction deve ter: 4xxx Income (Sales, Billable), 5xxx COGS, 6xxx Expense (Payroll, Equipment, Office, Insurance)

### Output obrigatorio
```json
{
  "screen": "T14_COA",
  "entity": "...",
  "metrics": {"account_count": N, "types": {"bank": N, "ar": N, "ap": N, "fixed_assets": N, "equity": N, "income": N, "cogs": N, "expense": N, "other": N}, "negative_balances": N, "inactive": N, "with_numbers": true/false, "hierarchy_depth": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 15: COMPANY SETTINGS (/app/settings?panel=company)

### Como navegar
URL: `https://qbo.intuit.com/app/settings?panel=company`
Esperar: 4s (modal dialog)

### O que olhar
- [ ] **Company Name**: realista? Nao "Test Company"?
- [ ] **Legal Name**: pode conter "Testing_OBS_AUTOMATION" — NUNCA CORRIGIR (REGRA #6)
- [ ] **Industry**: definido? Compativel com setor?
- [ ] **Address**: preenchido? Realista? (nao "123 Test St")
- [ ] **Email**: dominio profissional? (nao test@test.com)
- [ ] **Phone**: formato valido?
- [ ] **EIN/Tax ID**: preenchido?
- [ ] **Business Type**: definido? (S-Corp, LLC, Sole Proprietor)
- [ ] **Fiscal Year**: January para maioria
- [ ] **Accounting Method**: Accrual (typical para IES)

### REGRA CRITICA: NUNCA modificar Company Settings
Mesmo que Legal Name seja "Testing_OBS_AUTOMATION_DBA", apenas DOCUMENTAR. Settings de empresa sao tier "never-fix".

### Output obrigatorio
```json
{
  "screen": "T15_SETTINGS_COMPANY",
  "entity": "...",
  "metrics": {"company_name": "...", "legal_name": "...", "industry": "...", "address": "...", "email": "...", "phone": "...", "ein": "...", "business_type": "...", "fiscal_year": "...", "accounting_method": "..."},
  "cs_violations_documented": ["Legal name contains 'Testing_OBS_AUTOMATION' - NEVER FIX tier"],
  "findings": [],
  "fixes": [],
  "status": "PASS|WARN"
}
```

---

## TRACKING DE PROGRESSO

Apos cada tela, salvar resultado em `dashboard/pending/phase_results.json`:

```python
import json
f = 'C:/Users/adm_r/Clients/intuit-boom/dashboard/pending/phase_results.json'
try:
    data = json.loads(open(f).read())
except:
    data = {"results": [], "entity": "", "phase": 1}
data["results"].append(SCREEN_OUTPUT_JSON)
open(f, 'w').write(json.dumps(data, indent=2))
```

---

## ⚠ CHECKPOINT OBRIGATORIO (apos T15)

**NAO gere report ainda. NAO pule para a proxima entity.**

Voce completou T01-T15 (financeiro + operacional). Agora DEVE continuar com T16-T46 (advanced + settings + reports + surface) ANTES de trocar de entity.

Checklist:
- [ ] T01-T15 completos com output JSON? → Continuar para T16
- [ ] Algum fix pendente (CS3/CS5 encontrado mas nao corrigido)? → CORRIGIR AGORA antes de continuar
- [ ] Context window grande? → Usar /compact e continuar. NAO parar.

**Telas T16-T46 cobrem:** Payroll, Contractors, Time, Sales Tax, Recurring, Fixed Assets, Revenue Recognition, Budgets, Classes, Workflows, Custom Fields, 3 paineis de Settings, Reconciliation, Invoice/Bill drill-in, Journal Entries, POs, Sales Orders, Inventory, Customer Hub CRM, Reports completos (Standard, P&L by Class, AR Aging, AP Aging), Audit Log, AI Features, Global Search, e Surface Scan de 16 paginas restantes.

**Se voce parar aqui, o sweep esta 33% completo (15 de 46 telas). Continue.**

**⛔ PROIBIDO AVANCAR PARA CHILD ENTITIES ANTES DE COMPLETAR T16-T46 NO PARENT.**
**⛔ PROIBIDO GERAR REPORT ANTES DE COMPLETAR T16-T46 NO PARENT.**
**⛔ PROIBIDO USAR AGENTS/SUBAGENTS PARA TELAS** — subagents NAO tem acesso ao Playwright/browser. TODAS as telas devem ser executadas na sessao principal, sequencialmente. Nunca delegar telas para Agent tool.
**⛔ A ORDEM E: Parent T01→T46 COMPLETO, depois Child 1 T01-T15, depois Child 2 T01-T15, depois P1, depois Cross-Entity, depois Report.**
**Se voce pulou T16-T46 no parent: VOLTAR AGORA e completar antes de qualquer outra acao.**

---

## TELA 16: PAYROLL HUB (/app/payroll?jobId=payroll)

### Como navegar
URL: `https://qbo.intuit.com/app/payroll?jobId=payroll`
Esperar: 8s (payroll hub carrega widgets de historico e schedule)
Alternativa: Left nav → Payroll → Overview

### O que olhar
- [ ] **Payroll history**: ultimas 6+ payroll runs visiveis? Datas distribuidas?
- [ ] **Recent payrolls**: valores brutos (gross pay) proporcionais ao porte? Construction 5-50 empregados = $5K-$150K por run
- [ ] **Tax filings**: federal (941) e state filings em dia? Nenhum "Overdue" ou "Past Due"?
- [ ] **Payroll schedule**: definido? Bi-weekly ou weekly (construction tipico)? Proximo run date no futuro?
- [ ] **Tax deposits**: depositos em dia? Federal e state? Nenhum penalty visivel?
- [ ] **Employee count**: widget mostra quantos employees? Compativel com setor?
- [ ] **Net pay**: nenhum payroll com $0 net pay (indica run vazio ou erro)
- [ ] **Pay types**: mix de hourly + salary? Construction = maioria hourly
- [ ] **Payroll deductions**: health insurance, 401k, garnishments presentes?
- [ ] **Direct deposit**: habilitado para maioria dos employees?
- [ ] **TBX/Test markers**: nenhum employee com nome "Test Employee" ou "TBX Worker"

### Julgamento critico
- Construction com 8 entities deve ter 5-50 employees na parent entity, 2-15 por child
- Payroll run de $500K para empresa com 10 funcionarios = INFLADO (media $50K gross = $5K/employee/run bi-weekly)
- Missing payroll runs (gap > 30 dias sem run) = PROBLEMA — empresa real paga semanalmente ou bi-weekly sem falha
- Tax filings overdue = RED FLAG grave. IRS penalties sao reais e viewer expert nota imediatamente.
- $0 net pay em qualquer run indica payroll fantasma ou erro de configuracao
- Payroll sem deductions (zero benefits) em empresa de 20+ employees = IRREALISTA

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Tax filings overdue | Documentar como P1 finding. NAO tentar filing via UI | Documentar |
| Missing payroll runs (gap) | Documentar como P2. Payroll run nao pode ser criado retroativamente sem risco | Documentar |
| $0 net pay em algum run | Investigar: abrir payroll detail. Se employee com $0, documentar | Playwright → click no run |
| Employee com nome "Test" | Renomear para nome realista do setor (ex: "Maria Santos", "Carlos Pereira") | Playwright → /app/employees/edit |
| Payroll inflado ($500K+ para 10 emp) | Documentar como P2 inflation finding | Documentar |
| No payroll schedule defined | Documentar como P1 — demonstracao fica incompleta | Documentar |

### Extractor JS
```javascript
() => {
  const t = document.body.innerText || '';
  const runs = (t.match(/\$[\d,.]+/g) || []).slice(0, 10);
  const hasOverdue = /overdue|past due|penalty/i.test(t);
  const hasTBX = /\bTBX\b/i.test(t);
  const hasTest = /\b(test|sample|demo\s*\d|example|foo)\b/i.test(t);
  const empCount = t.match(/(\d+)\s*employee/i)?.[1] || 'unknown';
  const schedule = t.match(/(weekly|bi-?weekly|semi-?monthly|monthly)/i)?.[1] || 'unknown';
  return JSON.stringify({runs, hasOverdue, hasTBX, hasTest, empCount, schedule, bodyLen: t.length});
}
```

### Output obrigatorio
```json
{
  "screen": "T16_PAYROLL_HUB",
  "entity": "...",
  "metrics": {"employee_count": N, "recent_runs": N, "schedule": "bi-weekly|weekly|...", "last_run_date": "...", "last_run_gross": N, "tax_filings_current": true/false, "overdue_filings": N, "net_pay_zero_runs": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 17: CONTRACTORS (/app/contractors?jobId=team)

### Como navegar
URL: `https://qbo.intuit.com/app/contractors?jobId=team`
Esperar: 5s
Alternativa: Left nav → Payroll → Contractors

### O que olhar
- [ ] **Contractor count**: 5-30 typical para Construction (subcontractors sao core do business)
- [ ] **Contractor names**: TODOS realistas? Nenhum "Test Contractor", "Vendor 1"?
- [ ] **Payment history**: cada contractor tem pagamentos recentes?
- [ ] **W-9 info**: status W-9 indicado? (Received, Missing, Requested)
- [ ] **Total paid YTD**: valores proporcionais? Subcontractor de framing recebe $20K-$200K/ano
- [ ] **Email addresses**: profissionais? (nao test@test.com)
- [ ] **1099 status**: eligible for 1099? Threshold ($600+ = obrigatorio)
- [ ] **Business names**: contractor business names realistas? (ex: "Ramirez Electrical LLC")
- [ ] **Active vs inactive**: proporcao? 80%+ ativos

### Julgamento critico
- Construction SEM contractors = ALTAMENTE SUSPEITO. Subcontractors sao 40-60% do custo em construction.
- Contractor com $1M+ pago mas nome "John Doe" = IRREALISTA
- W-9 todos "Missing" = problema de compliance que viewer expert nota
- Contractor names genericos ("Sub 1", "Sub 2") destroem a experiencia realista
- Construction entities: subcontractors de cada specialty (Electrical, Plumbing, HVAC, Framing, Concrete, Drywall)

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Contractor com nome generico | Renomear para nome realista (ex: "Martinez Framing Services") | Playwright → edit contractor |
| Zero contractors em Construction | Documentar como P1 — gap grave | Documentar |
| W-9 todos Missing | Documentar como P2 compliance finding | Documentar |
| Contractor com $0 paid | Verificar se tem bills associados. Se nao, documentar | QBO API → search_bills |
| Test email addresses | Atualizar para email profissional | Playwright → edit contractor |

### Output obrigatorio
```json
{
  "screen": "T17_CONTRACTORS",
  "entity": "...",
  "metrics": {"contractor_count": N, "active": N, "inactive": N, "total_paid_ytd": N, "w9_received": N, "w9_missing": N, "eligible_1099": N, "generic_names": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 18: TIME TRACKING (/app/time)

### Como navegar
URL: `https://qbo.intuit.com/app/time`
Esperar: 5s
Alternativa: Left nav → Time → Time Entries

### O que olhar
- [ ] **Time entries existem?**: pelo menos 20-50 entries recentes
- [ ] **Billable vs non-billable**: mix proporcional? Construction = 70-90% billable
- [ ] **Approval status**: entries approved? Pending review? (workflow maturity indicator)
- [ ] **Employee names on entries**: realistas? Nenhum "Test User"?
- [ ] **Project/Customer tied**: entries linkadas a projetos/clientes?
- [ ] **Hours distribution**: 6-10 hours/day typical. Entries de 24h = ERRO
- [ ] **Date distribution**: entries espalhadas ao longo de semanas, nao todas no mesmo dia
- [ ] **Descriptions/notes**: presentes? Realistas? ("Framing 2nd floor", nao "test entry")
- [ ] **Rate visible?**: hourly rate definido?

### Julgamento critico
- Construction = time tracking e CRITICO. Horas billable tied to projects = job costing accuracy
- Zero time entries em Professional Services ou Construction = GAP GRAVE (significa que feature nao esta sendo demonstrada)
- Todas entries no mesmo dia = batch artificial, nao parece real
- 100% non-billable em Construction = ERRO de configuracao
- Entries sem project linkado = perda de job costing capability na demo

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Zero time entries | Documentar como P1. Criar 5-10 entries via UI se possivel | Playwright → /app/time |
| All same date | Documentar como P2 — pouca distribuicao temporal | Documentar |
| 24h entries | Editar para horas realistas (6-10h) | Playwright → edit entry |
| No project linkage | Documentar como finding — job costing gap | Documentar |
| Test descriptions | Renomear para descricoes realistas do setor | Playwright → edit entry |

### Output obrigatorio
```json
{
  "screen": "T18_TIME_TRACKING",
  "entity": "...",
  "metrics": {"total_entries": N, "billable": N, "non_billable": N, "approved": N, "pending": N, "unique_employees": N, "unique_projects": N, "date_range": "start - end", "avg_hours_per_entry": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 19: SALES TAX (/app/tax/home?jobId=sales-tax)

### Como navegar
URL: `https://qbo.intuit.com/app/tax/home?jobId=sales-tax`
Esperar: 6s (tax module pode ser pesado)
Alternativa: Left nav → Taxes → Sales Tax

### O que olhar
- [ ] **Tax setup complete?**: wizard finalizado ou ainda em setup?
- [ ] **Tax rates**: rates definidas? Nomes realistas? (State, County, City)
- [ ] **Nexus states**: quais states tem nexus? Proporcional ao negocio?
- [ ] **Filing status**: current? Overdue? (OVERDUE = PROBLEMA GRAVE)
- [ ] **Tax liability**: valores calculados? Proporcionais ao revenue?
- [ ] **Filing frequency**: monthly, quarterly, annually — definido?
- [ ] **Auto-filing**: habilitado? (indica maturidade)
- [ ] **Tax agencies**: configuradas? Nomes reais? (IRS, State Dept of Revenue)
- [ ] **Exemptions**: definidas? (non-profit, resale certificates)
- [ ] **Recent filings**: historico de filings visivel?

### Julgamento critico
- Sales tax overdue = RED FLAG IMMEDIATO. Um auditor do IRS vendo filings atrasados na demo = desastre.
- Construction: sales tax varia MUITO por state. Alguns states isentam labor, outros nao. Tax setup deve refletir isso.
- Tire Shop: 100% taxable (products). Rate deve ser ~6-10% dependendo do state.
- Non-Profit: pode ter exemptions. Tax setup deve refletir tax-exempt status.
- Zero tax liability com $500K+ revenue = ERRO de configuracao (a menos que 100% services em state isento)

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Filing overdue | Documentar como P1. NAO tentar filing via UI (risco legal) | Documentar |
| Tax not set up | Documentar como P1 — feature nao demonstravel | Documentar |
| Zero liability com alto revenue | Verificar tax codes nas invoices. Se missing, documentar | QBO API → search_invoices |
| Wrong nexus states | Documentar como P2 | Documentar |
| No tax rates defined | Documentar como P1 | Documentar |

### Output obrigatorio
```json
{
  "screen": "T19_SALES_TAX",
  "entity": "...",
  "metrics": {"setup_complete": true/false, "nexus_states": N, "tax_rates_defined": N, "filing_status": "current|overdue|not_setup", "tax_liability_current_period": N, "filing_frequency": "...", "auto_filing": true/false, "overdue_filings": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 20: RECURRING TRANSACTIONS (/app/recurring?jobId=accounting)

### Como navegar
URL: `https://qbo.intuit.com/app/recurring?jobId=accounting`
Esperar: 5s
Alternativa: Left nav → Settings gear → Recurring Transactions

### O que olhar
- [ ] **Template count**: 5-15 templates = good demo. Zero = feature vazia. 50+ = suspeito
- [ ] **Template types**: mix de Invoice, Bill, Expense, JE? Nao so 1 tipo
- [ ] **Frequency**: weekly, monthly, quarterly — mix realista?
- [ ] **Next date**: datas futuras? (scheduled = ativo). Todas no passado = templates mortos
- [ ] **Status**: Scheduled, Reminder, Unscheduled — proporcao?
- [ ] **Template names**: realistas? "Monthly Rent", "Weekly Supplies Order", nao "Test Recurring"
- [ ] **Amounts**: proporcionais ao negocio? Rent $2K-$10K/month, nao $500K
- [ ] **Customer/Vendor tied**: templates linkados a entidades reais?
- [ ] **End date**: definido ou indefinido? Mix e realista.

### Julgamento critico
- Zero recurring templates = empresa que nao usa automacao. Em demo de IES, isso e GAP porque recurring e feature key.
- Construction tipico: Recurring rent, insurance, equipment lease, monthly subcontractor bills
- Todos templates "Unscheduled" = ninguem ativou. Feature vazia na pratica.
- Template com $1M monthly recurring para empresa de 10 funcionarios = INFLADO

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Zero templates | Criar 3-5 templates realistas (rent, insurance, supplies) | Playwright → /app/recurring/new |
| All unscheduled | Ativar 2-3 como "Scheduled" | Playwright → edit template |
| Test names | Renomear para nomes realistas | Playwright → edit template |
| Inflated amounts | Ajustar para valores proporcionais | Playwright → edit template |
| All same type | Diversificar: add invoice + bill + expense templates | Playwright |

### Output obrigatorio
```json
{
  "screen": "T20_RECURRING",
  "entity": "...",
  "metrics": {"template_count": N, "by_type": {"invoice": N, "bill": N, "expense": N, "je": N, "other": N}, "scheduled": N, "reminder": N, "unscheduled": N, "future_next_dates": N, "past_next_dates": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 21: FIXED ASSETS (/app/fixed-assets?jobId=accounting)

### Como navegar
URL: `https://qbo.intuit.com/app/fixed-assets?jobId=accounting`
Esperar: 5s
Nota: Feature pode nao estar habilitada em todos os tiers. Se 404 ou "feature not available", documentar e pular.

### O que olhar
- [ ] **Asset list**: pelo menos 3-10 assets para Construction (equipment-heavy industry)
- [ ] **Asset names**: realistas? ("2024 Ford F-250", "CAT 320 Excavator", nao "Asset 1")
- [ ] **Depreciation method**: Straight-line, MACRS, Declining Balance — definido para cada?
- [ ] **Original cost**: proporcional? Truck = $40K-$80K. Excavator = $100K-$500K. Office furniture = $2K-$10K
- [ ] **Accumulated depreciation**: calculado? Proporcional a idade do asset?
- [ ] **Net book value**: Cost - Accumulated Depreciation = faz sentido?
- [ ] **Asset categories**: vehicles, equipment, furniture, leasehold improvements — mix realista
- [ ] **Purchase date**: distribuido ao longo de anos, nao todos comprados no mesmo dia
- [ ] **Status**: in service, disposed, sold — mix?

### Julgamento critico
- Construction SEM fixed assets = ALTAMENTE SUSPEITO. Construtoras investem pesado em equipamentos.
- Asset de $10M para empresa com $500K revenue = DESPROPORCIONAL
- Todos assets com mesma purchase date = criacao batch artificial
- Zero depreciation em asset de 3+ anos = ERRO de configuracao
- Net book value negativo = ERRO matematico

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Zero assets (Construction) | Documentar como P1 gap grave | Documentar |
| Generic asset names | Renomear para nomes realistas do setor | Playwright → edit asset |
| No depreciation method | Documentar como P2 — setup incompleto | Documentar |
| Disproportionate costs | Documentar como P2 finding | Documentar |
| Feature not available | Documentar como N/A — tier limitation | Documentar |

### Output obrigatorio
```json
{
  "screen": "T21_FIXED_ASSETS",
  "entity": "...",
  "metrics": {"asset_count": N, "total_cost": N, "total_accumulated_depreciation": N, "total_net_book_value": N, "categories": {"vehicles": N, "equipment": N, "furniture": N, "other": N}, "depreciation_methods": ["..."], "feature_available": true/false},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN|N/A"
}
```

---

## TELA 22: REVENUE RECOGNITION (/app/revenue-recognition?jobId=accounting)

### Como navegar
URL: `https://qbo.intuit.com/app/revenue-recognition?jobId=accounting`
Esperar: 5s
Nota: Advanced-tier feature. Pode nao estar disponivel em todos os planos. Se 404 ou "upgrade required", documentar e pular.

### O que olhar
- [ ] **Feature enabled?**: sim/nao. Se nao, registrar como N/A
- [ ] **Rev rec rules**: regras definidas? Pelo menos 1-2 rules?
- [ ] **ASC 606 compliance**: configuracao indica compliance com ASC 606?
- [ ] **Revenue schedules**: schedules criados? Linked to products/services?
- [ ] **Deferred revenue**: conta de deferred revenue existe no COA?
- [ ] **Recognition method**: point-in-time vs over-time — definido?
- [ ] **Active contracts**: contracts com rev rec rules aplicadas?

### Julgamento critico
- Rev rec e feature PREMIUM. Para demo de IES Advanced, deve estar habilitado e configurado.
- Construction com contratos longos (6+ meses) = over-time recognition e obrigatorio para ASC 606
- Se feature existe mas zero rules = setup incompleto, feature nao demonstravel
- Professional Services: milestone-based recognition comum

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Feature not available | Documentar como N/A. Nao e erro — e limitacao de tier | Documentar |
| Feature enabled but no rules | Documentar como P2 — setup incompleto | Documentar |
| No deferred revenue account | Documentar como P2 finding | Documentar |
| TBX prefix visible | Investigar source. Se e nome de record editavel → renomear. Se e system-generated → documentar como CS3 "system-generated, not editable" | Playwright → Edit record |

### Output obrigatorio
```json
{
  "screen": "T22_REVENUE_RECOGNITION",
  "entity": "...",
  "metrics": {"feature_available": true/false, "feature_enabled": true/false, "rules_count": N, "recognition_method": "...", "deferred_revenue_account": true/false, "active_contracts": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN|N/A"
}
```

---

## TELA 23: BUDGETS (/app/budgets)

### Como navegar
URL: `https://qbo.intuit.com/app/budgets`
Esperar: 5s
Alternativa: Left nav → Reports → Budgets (pode estar em Reports section)

### O que olhar
- [ ] **Budget count**: pelo menos 1 budget ativo = good demo. Zero = feature vazia
- [ ] **Budget type**: P&L budget? Expense-only? Revenue?
- [ ] **Budget period**: FY2026? Monthly breakdown?
- [ ] **Budget vs actual**: comparison disponivel? Variances calculadas?
- [ ] **Budget amounts**: proporcionais ao revenue real? Budget de $10M para empresa de $500K = IRREALISTA
- [ ] **Account coverage**: budget cobre main accounts (Revenue, COGS, major expenses)?
- [ ] **Subdivided by**: class? Location? Customer? (advanced usage)
- [ ] **Status**: active? (nao archived ou deleted)

### Julgamento critico
- Budget e feature de maturidade. Uma empresa "real" em Construction teria pelo menos 1 annual budget.
- Budget amounts devem ser ~10-20% variance do actual (nao 500% acima ou abaixo)
- Budget sem monthly breakdown = setup minimal (menos impressionante na demo)
- Multiple budgets (by project, by department) = ADVANCED usage, excelente para demo

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Zero budgets | Criar 1 P&L budget para FY2026 com valores baseados no actual | Playwright → /app/budgets/new |
| Budget amounts way off | Ajustar para ~10% acima do actual YTD extrapolated | Playwright → edit budget |
| Archived/inactive budget only | Reativar ou criar novo | Playwright |

### Output obrigatorio
```json
{
  "screen": "T23_BUDGETS",
  "entity": "...",
  "metrics": {"budget_count": N, "active": N, "types": ["P&L", "..."], "period": "...", "budget_vs_actual_available": true/false, "total_budgeted_revenue": N, "total_budgeted_expenses": N, "subdivided_by": "none|class|location|customer"},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 24: CLASSES & LOCATIONS (/app/class + dimensions)

### Como navegar
URL Classes: `https://qbo.intuit.com/app/class`
URL Locations: `https://qbo.intuit.com/app/location`
Esperar: 4s cada
Nota: Classes e Locations devem estar habilitados em Advanced Settings. Se nao existem, verificar T29.

### O que olhar
- [ ] **Class count**: 3-8 ideal para demo. Zero = feature desabilitada. 20+ = potencialmente confuso
- [ ] **Class names**: realistas? Construction: "Residential", "Commercial", "Government", "Renovation"
- [ ] **Class hierarchy**: sub-classes existem? (ex: Commercial > Office > Tenant Improvements)
- [ ] **Location count**: 1-5 typical (office locations, job sites)
- [ ] **Location names**: realistas? ("Main Office - Austin", "Warehouse - Dallas")
- [ ] **Tag groups**: custom tags definidos? (Project Phase, Region, etc.)
- [ ] **Usage**: classes/locations sendo usadas em transacoes? (verificar via P&L by Class em T40)
- [ ] **Active status**: todas ativas? Nenhuma "Test Class" ou "DELETE ME"?

### Julgamento critico
- Classes sao FUNDAMENTAIS para multi-dimensional reporting. Demo sem classes perde funcionalidade key.
- Construction ideal: classes por tipo de projeto (Residential, Commercial, Infrastructure) ou por departamento (Field, Office, Management)
- Locations por job site ou office = usage avancado que impressiona
- Muitas classes (20+) sem hierarquia = flat list confusa
- Classes com nomes genericos ("Class 1", "Cat A") = CS violation

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Zero classes | Habilitar em Settings e criar 3-5 classes realistas | Playwright → Settings → Advanced → enable, then /app/class/new |
| Generic class names | Renomear para nomes do setor | Playwright → edit class |
| Test/Delete classes | Remover ou renomear | Playwright |
| Zero locations | Criar 2-3 locations realistas | Playwright → /app/location/new |
| Classes not used in transactions | Documentar como P2 — feature habilitada mas vazia | Documentar |

### Output obrigatorio
```json
{
  "screen": "T24_CLASSES_LOCATIONS",
  "entity": "...",
  "metrics": {"class_count": N, "class_hierarchy_depth": N, "location_count": N, "tag_groups": N, "classes_active": N, "locations_active": N, "generic_names_found": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 25: WORKFLOWS (/app/workflows)

### Como navegar
URL: `https://qbo.intuit.com/app/workflows`
Esperar: 5s
Nota: Advanced-tier feature. Pode nao estar disponivel em todos os planos.

### O que olhar
- [ ] **Workflow count**: 2-5 ideal para demo. Zero = feature nao demonstravel
- [ ] **Trigger types**: on invoice create, on payment received, on bill due, on expense created — diversidade?
- [ ] **Action types**: send email, create task, notify user — definidos?
- [ ] **Status**: active? Enabled? Paused?
- [ ] **Execution history**: workflows executaram? Ou sao templates vazios?
- [ ] **Workflow names**: descritivos? "Auto-send invoice reminder", nao "Workflow 1"
- [ ] **Conditions**: condicoes configuradas? (amount > $1000, customer = VIP)
- [ ] **Feature available?**: se 404 ou "upgrade required", registrar N/A

### Julgamento critico
- Workflows demonstram automacao — diferencial key do IES vs. QBO Simple Start
- Zero workflows com feature disponivel = oportunidade perdida na demo
- Workflows sem execution history = nunca executaram, feature e "decorativa"
- Construction use case: auto-reminders para invoices 30+ days, auto-notify PM quando bill > budget

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Feature not available | Documentar como N/A | Documentar |
| Zero workflows | Criar 2 workflows simples (invoice reminder, payment notification) | Playwright → /app/workflows/new |
| All paused/inactive | Ativar pelo menos 2 | Playwright → edit workflow |
| Generic names | Renomear para descricoes claras | Playwright → edit workflow |

### Output obrigatorio
```json
{
  "screen": "T25_WORKFLOWS",
  "entity": "...",
  "metrics": {"feature_available": true/false, "workflow_count": N, "active": N, "paused": N, "trigger_types": ["..."], "action_types": ["..."], "total_executions": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN|N/A"
}
```

---

## TELA 26: CUSTOM FIELDS (/app/customfields)

### Como navegar
URL: `https://qbo.intuit.com/app/customfields`
Esperar: 4s
Alternativa: Settings gear → Custom Fields

### O que olhar
- [ ] **Field count**: 3-5 ideal para demo. Zero = feature vazia. 15+ = pode confundir
- [ ] **Field types**: dropdown, text, number, date — mix?
- [ ] **Field names**: realistas para o setor? Construction: "Project Phase", "Permit Number", "Job Site", "Foreman"
- [ ] **Applied to which transactions**: invoices, estimates, bills, POs? Wide coverage = better demo
- [ ] **Required fields?**: algum marcado como required?
- [ ] **Dropdown options**: se dropdown, options realistas? (nao "Option 1", "Option 2")
- [ ] **Active/inactive**: todos ativos?
- [ ] **Default values**: definidos?

### Julgamento critico
- Custom fields mostram que a empresa personaliza o QBO para seu workflow. Feature key para IES.
- Construction sem "Project Phase" ou "Permit Number" = oportunidade perdida
- Fields genericos ("Custom Field 1") = CS violation — pior que nao ter
- Fields aplicados a invoices + estimates + POs = cross-workflow usage, excelente
- Fields com dropdown sem options definidas = setup incompleto

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Zero custom fields | Criar 3 fields realistas para o setor | Playwright → /app/customfields |
| Generic field names | Renomear para nomes do setor (ex: "Project Phase") | Playwright → edit field |
| Dropdown sem options | Adicionar 3-5 options realistas | Playwright → edit field |
| Fields on single transaction type only | Expandir para mais tipos se possivel | Playwright → edit field |

### Output obrigatorio
```json
{
  "screen": "T26_CUSTOM_FIELDS",
  "entity": "...",
  "metrics": {"field_count": N, "by_type": {"dropdown": N, "text": N, "number": N, "date": N}, "applied_to": ["invoice", "estimate", "..."], "required_fields": N, "generic_names": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 27: SALES SETTINGS (/app/settings?panel=sales)

### Como navegar
URL: `https://qbo.intuit.com/app/settings?panel=sales`
Esperar: 4s (Settings modal abre)
Custom Form Styles: `https://qbo.intuit.com/app/customformstyles`

### O que olhar
- [ ] **Custom invoice template**: existe? Logo presente? Cores personalizadas?
- [ ] **Payment terms**: default definido? (Net 30, Net 15, Due on receipt)
- [ ] **Default messages**: invoice email message personalizado? (nao template generico)
- [ ] **Online payments enabled?**: credit card, bank transfer (ACH)? KEY feature for demo
- [ ] **Shipping**: habilitado? (se aplicavel ao setor)
- [ ] **Discounts**: habilitados? (common em Construction — volume discounts)
- [ ] **Deposits**: pre-payment settings? (Construction = 50% deposit common)
- [ ] **Estimates**: enabled? Convert to invoice option?
- [ ] **Custom Form Styles**: quantos templates? Pelo menos 1 customizado
- [ ] **Service date**: tracking habilitado?

### Julgamento critico
- Online payments DESABILITADO = oportunidade perdida. Feature numero 1 que prospects perguntam.
- Default "Net 30" e standard para Construction. "Due on receipt" pode ser agressivo.
- Custom invoice template com logo = demonstra profissionalismo. Sem logo = setup incompleto.
- Construction: deposits/pre-payments sao padrao da industria. Se desabilitado, feature gap.

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Online payments disabled | Documentar como P1 finding — NAO habilitar (requer merchant account) | Documentar |
| No custom template | Documentar como P2 | Documentar |
| Generic email messages | Documentar como P3 finding | Documentar |
| Estimates disabled | Habilitar se possivel (toggle em Settings) | Playwright |
| No payment terms set | Documentar como P2 | Documentar |

### Output obrigatorio
```json
{
  "screen": "T27_SALES_SETTINGS",
  "entity": "...",
  "metrics": {"custom_template_exists": true/false, "default_payment_terms": "...", "online_payments": true/false, "estimates_enabled": true/false, "discounts_enabled": true/false, "deposits_enabled": true/false, "shipping_enabled": true/false, "custom_form_styles_count": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 28: EXPENSE SETTINGS (/app/settings?panel=expenses)

### Como navegar
URL: `https://qbo.intuit.com/app/settings?panel=expenses`
Esperar: 4s

### O que olhar
- [ ] **Purchase orders enabled?**: sim/nao. Construction = OBRIGATORIO (PO→Bill→Payment chain)
- [ ] **Bills payment terms**: default definido? (Net 30 typical)
- [ ] **Default expense categories**: categorias definidas para despesas comuns?
- [ ] **Default bill payment terms**: Net 30, Net 60?
- [ ] **Track expenses by customer**: habilitado? (job costing em Construction)
- [ ] **Track billable expenses**: habilitado? (passar custo para cliente)
- [ ] **Make expenses and items billable**: ativado?
- [ ] **Default markup rate**: definido? Construction = 10-20% markup common
- [ ] **Receipt matching**: habilitado?

### Julgamento critico
- POs DESABILITADOS em Construction = GAP GRAVE. PO chain e workflow core.
- "Track expenses by customer" desabilitado = job costing impossivel na demo
- "Billable expenses" desabilitado = nao pode demonstrar cost pass-through
- Construction SEM markup rate = nao pode demonstrar profitability por projeto

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| POs disabled (Construction) | Habilitar POs em Settings | Playwright → toggle PO setting |
| Billable expenses off | Habilitar se disponivel | Playwright → toggle |
| Track by customer off | Habilitar para job costing | Playwright → toggle |
| No default markup | Definir 15% (Construction standard) | Playwright → set markup |

### Output obrigatorio
```json
{
  "screen": "T28_EXPENSE_SETTINGS",
  "entity": "...",
  "metrics": {"po_enabled": true/false, "default_bill_terms": "...", "track_by_customer": true/false, "billable_expenses": true/false, "default_markup_rate": "N%|none", "receipt_matching": true/false},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 29: ADVANCED SETTINGS (/app/settings?panel=advanced)

### Como navegar
URL: `https://qbo.intuit.com/app/settings?panel=advanced`
Esperar: 4s

### O que olhar
- [ ] **Accounting method**: Accrual (standard para IES) vs Cash? Se Cash, documentar — pode ser intencional
- [ ] **Fiscal year**: January (default) ou custom? (some Construction companies use non-calendar FY)
- [ ] **Class tracking**: HABILITADO? (obrigatorio para multi-dimensional reporting)
- [ ] **Location tracking**: HABILITADO? (util para multi-office ou job sites)
- [ ] **Currency**: multi-currency habilitado? (se nao, single currency = ok para domestic)
- [ ] **Automation**: auto-apply credits, auto-invoice unbilled, auto-recall — habilitados?
- [ ] **Chart of accounts**: account numbers habilitados?
- [ ] **Categories**: habilitadas? (product/service categories)
- [ ] **Projects**: habilitados? (OBRIGATORIO para Construction)
- [ ] **Time tracking**: habilitado? (link com T18)
- [ ] **Tax form**: selecionado? (C-Corp, S-Corp, Sole Proprietor, Partnership, Non-profit)
- [ ] **Close the books**: password protegido? Closing date definida?

### Julgamento critico
- Cash accounting em empresa com Inventory/POs = INCONSISTENTE. Accrual e obrigatorio para accrual-based features.
- Class tracking OFF com classes definidas = CONTRADICAO (feature habilitada mas tracking desligado)
- Projects OFF em Construction = DEALBREAKER. Sem projects, nao tem job costing.
- Close the books sem data = livros nunca fechados. Para demo madura, deve ter closing date.
- Account numbers OFF = ok, mas ON mostra maturidade.

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Class tracking OFF | Habilitar (toggle em Advanced Settings) | Playwright → toggle |
| Location tracking OFF | Habilitar se necessario | Playwright → toggle |
| Projects OFF (Construction) | Habilitar — CRITICAL | Playwright → toggle |
| Cash method com accrual features | Documentar como finding — NAO mudar (pode quebrar reports) | Documentar |
| Time tracking OFF | Habilitar | Playwright → toggle |

### Output obrigatorio
```json
{
  "screen": "T29_ADVANCED_SETTINGS",
  "entity": "...",
  "metrics": {"accounting_method": "accrual|cash", "fiscal_year_start": "January|...", "class_tracking": true/false, "location_tracking": true/false, "multi_currency": true/false, "projects_enabled": true/false, "time_tracking_enabled": true/false, "account_numbers": true/false, "close_the_books": true/false, "closing_date": "...", "tax_form": "..."},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 30: RECONCILIATION (/app/reconcile?jobId=accounting)

### Como navegar
URL: `https://qbo.intuit.com/app/reconcile?jobId=accounting`
Esperar: 5s
Alternativa: Left nav → Accounting → Reconcile

### O que olhar
- [ ] **Accounts list**: quais contas bancarias aparecem para reconciliar?
- [ ] **Last reconciled date**: cada conta — quando foi a ultima reconciliacao?
- [ ] **Reconciled within 30 days?**: pelo menos 1 conta reconciliada recentemente = good demo
- [ ] **Difference**: $0 = reconciliado. Qualquer valor != $0 = pendente
- [ ] **Pending items**: quantas transacoes pendentes de reconciliacao?
- [ ] **Account count**: todas as bank accounts e credit cards aparecem?
- [ ] **Historical reconciliations**: historico visivel? Demonstra maturidade
- [ ] **Auto-reconciliation**: habilitado? (bank feed feature)

### Julgamento critico
- Empresa com ZERO reconciliacoes = red flag. Significa que bank feeds nunca foram processados.
- Last reconciled > 90 days ago = empresa negligente com controle financeiro
- Construction: deve ter pelo menos checking account reconciliada mensalmente
- Difference != $0 em reconciliacao fechada = ERRO GRAVE de contabilidade
- Credit card accounts tambem devem ser reconciliados

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Zero reconciliations | Documentar como P1 — NAO tentar reconciliar via UI (complexo e arriscado) | Documentar |
| Last reconciled > 90 days | Documentar como P2 finding | Documentar |
| Difference != $0 | Investigar: quais transacoes causam diferenca? Documentar | Playwright → drill into account |
| Missing accounts | Verificar se bank accounts existem no COA (T14) | QBO API → search_accounts |

### Output obrigatorio
```json
{
  "screen": "T30_RECONCILIATION",
  "entity": "...",
  "metrics": {"accounts_available": N, "accounts_reconciled": N, "last_reconciled_dates": {"account_name": "date", "...": "..."}, "most_recent_reconciliation": "...", "days_since_last": N, "pending_items": N, "all_differences_zero": true/false},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 31: INVOICES DETAIL (drill into 3-5 invoices)

### Como navegar
1. URL: `https://qbo.intuit.com/app/invoices` (lista de invoices)
2. Esperar: 5s
3. Abrir 3-5 invoices recentes (clicar no invoice number)
4. Para cada invoice, esperar 3s para carregar completamente

### O que olhar (PARA CADA INVOICE)
- [ ] **Customer name**: realista? Nao "Customer 1", "Test Client", "TBX"
- [ ] **Line items**: descricoes realistas? ("Framing labor - 2nd floor addition", nao "Item 1")
- [ ] **Amounts**: proporcionais? Construction invoice = $5K-$500K tipico
- [ ] **Dates**: distribuidas? Nao todas no mesmo dia
- [ ] **Invoice number**: sequencia logica? (1001, 1002, 1003)
- [ ] **Terms**: Net 30, Net 15, etc. Definidos?
- [ ] **Due date**: futuro ou passado? Overdue invoices em proporcao razoavel
- [ ] **Custom fields**: preenchidos? (Project Phase, Permit Number se definidos em T26)
- [ ] **Tax**: sales tax aplicado? (se applicavel no state)
- [ ] **Project/Class linked**: invoice associado a project? Class?
- [ ] **Attachments**: algum anexo? (optional mas mostra maturidade)
- [ ] **Status**: Open, Paid, Overdue — mix?

### Julgamento critico
- Invoices sao o CORE da experiencia AR. Se 3 invoices aleatórios tem nomes falsos, toda a demo cai.
- Construction invoice sem line item descriptions detalhadas = nao parece real
- Invoice de $2M para single customer em empresa de $500K annual = INFLADO
- Todos invoices no status "Paid" = nao demonstra AR aging workflow
- Todos invoices com mesma data = criacao batch artificial

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Customer name generico | Renomear customer (cuidado: afeta TODAS transacoes do customer) | Playwright → /app/customerdetail/edit |
| Line item "Item 1" | Editar invoice, renomear line items | Playwright → edit invoice |
| All same date | Documentar como P2 finding | Documentar |
| Missing terms/due date | Editar invoice, add terms | Playwright → edit invoice |
| Inflated amounts | Documentar como P2 | Documentar |
| TBX prefix on invoice/customer | Se customer name tem TBX → ir em Customers e renomear. Se invoice number tem TBX → system-generated, documentar. Se invoice description tem TBX → editar invoice e renomear | Playwright |

### Output obrigatorio
```json
{
  "screen": "T31_INVOICES_DETAIL",
  "entity": "...",
  "invoices_sampled": N,
  "metrics": {"realistic_customers": N, "realistic_line_items": N, "dates_distributed": true/false, "terms_set": N, "tax_applied": N, "project_linked": N, "custom_fields_filled": N, "status_mix": {"open": N, "paid": N, "overdue": N}},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 32: BILLS DETAIL (drill into 3-5 bills)

### Como navegar
1. URL: `https://qbo.intuit.com/app/bills` (lista de bills)
2. Esperar: 5s
3. Abrir 3-5 bills recentes (clicar no bill)
4. Para cada bill, esperar 3s

### O que olhar (PARA CADA BILL)
- [ ] **Vendor name**: realista? Construction: "Home Depot", "Ferguson Plumbing Supply", "Acme Concrete"
- [ ] **Line items**: descricoes realistas? ("Lumber - 2x4x8 SPF (500 pcs)", nao "Material 1")
- [ ] **Amounts**: proporcionais? Material bill = $1K-$50K. Subcontractor bill = $5K-$100K
- [ ] **Dates**: distribuidas ao longo de semanas/meses
- [ ] **Bill number**: vendor invoice reference? Realista?
- [ ] **Terms**: Net 30, Net 60 definidos?
- [ ] **Due date**: razoavel?
- [ ] **Category/Account**: expense account correto? (COGS for materials, Subcontractor Expense, etc.)
- [ ] **Project/Class linked**: bill associado a projeto?
- [ ] **Payment status**: Open, Paid, Overdue — mix?
- [ ] **Linked to PO?**: se PO habilitado (T28), bill referencia PO?

### Julgamento critico
- Bills sao o CORE da experiencia AP. Vendor names falsos destroem credibilidade.
- Construction sem bills de material suppliers = IRREALISTA (construtora compra materiais todo dia)
- Bill sem expense account definido = miscategorized, afeta P&L accuracy
- 100% bills Paid = nao demonstra AP aging, perdendo oportunidade de demo
- Bill linkado a PO = advanced workflow chain, excelente para demo

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Vendor name generico | Renomear vendor (cuidado: afeta TODAS transacoes do vendor) | Playwright → /app/vendordetail/edit |
| Line item generico | Editar bill, renomear line items | Playwright → edit bill |
| Wrong expense account | Recategorizar para account correto | Playwright → edit bill |
| No PO linkage (PO enabled) | Documentar como finding — PO chain incompleto | Documentar |

### Output obrigatorio
```json
{
  "screen": "T32_BILLS_DETAIL",
  "entity": "...",
  "bills_sampled": N,
  "metrics": {"realistic_vendors": N, "realistic_line_items": N, "dates_distributed": true/false, "terms_set": N, "correct_accounts": N, "project_linked": N, "po_linked": N, "status_mix": {"open": N, "paid": N, "overdue": N}},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 33: JOURNAL ENTRIES (/app/journalentry list)

### Como navegar
URL: `https://qbo.intuit.com/app/journal` ou `https://qbo.intuit.com/app/journalentries`
Esperar: 5s
Alternativa: Left nav → Accounting → Chart of Accounts → Journal Entries (ou procurar via search)

### O que olhar
- [ ] **Recent JEs**: pelo menos 5-10 JEs visiveis?
- [ ] **Memo/descriptions**: REALISTAS? ("Monthly depreciation", "Accrued payroll", nao "test je", "asdf")
- [ ] **Balanced entries**: debits = credits em cada JE?
- [ ] **No test JEs**: nenhum JE com memo "test", "sample", "TBX", "delete me"
- [ ] **Amounts**: proporcionais? JE de $10M em empresa de $500K = INFLADO
- [ ] **Dates**: distribuidas?
- [ ] **Accounts used**: accounts realistas? (nao "Account 1" DR / "Account 2" CR)
- [ ] **JE numbers**: sequenciais?
- [ ] **Created by**: user name visivel? (nao "automation_bot" ou "test_user")
- [ ] **Adjusting entries**: JEs marcados como "adjusting" existem? (mature accounting)

### Julgamento critico
- JEs sao vistos por contadores/CFOs em demos. Memos falsos = desastre de credibilidade.
- JE com memo "Created by sweep" ou "Auto-generated" = nosso proprio rastro. REMOVER.
- Balanced = obrigatorio. QBO nao permite JE unbalanced, mas verificar anyway.
- Muitos JEs recentes do mesmo user = pode indicar cleanup batch (nao necessariamente ruim, mas nota-se)

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Test memos | Editar JE, update memo para descricao realista | Playwright → edit JE |
| "sweep" or "auto-generated" memos | OBRIGATORIO renomear — nao pode ter rastro de automacao | Playwright → edit JE |
| Inflated amounts | Documentar como P2 | Documentar |
| Generic account names in JE | Problema e no COA (T14), nao no JE | Documentar → refer T14 |

### Output obrigatorio
```json
{
  "screen": "T33_JOURNAL_ENTRIES",
  "entity": "...",
  "metrics": {"je_count_visible": N, "realistic_memos": N, "test_memos_found": N, "sweep_traces_found": N, "date_range": "start - end", "balanced": true, "adjusting_entries": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 34: PURCHASE ORDERS (/app/purchaseorders)

### Como navegar
URL: `https://qbo.intuit.com/app/purchaseorders`
Esperar: 5s
Nota: Pode retornar 404 no IES se PO feature nao estiver habilitada. Verificar T28 primeiro.
Alternativa nav: Expenses & Bills dropdown → Purchase Orders

### O que olhar
- [ ] **PO count**: 5-20 POs = good demo para Construction. Zero = feature vazia
- [ ] **PO status**: Open, Closed, Partially Received — mix?
- [ ] **Vendor names**: realistas? (material suppliers, equipment vendors)
- [ ] **Line items**: detalhados? ("500 bags Portland Cement 94lb", nao "Material")
- [ ] **Amounts**: proporcionais? Material PO = $2K-$50K, Equipment PO = $10K-$200K
- [ ] **Dates**: distribuidas ao longo de semanas/meses
- [ ] **Linked to bills?**: POs convertidos para bills? (PO→Bill chain)
- [ ] **Project linked**: PO associado a projeto?
- [ ] **Approval workflow**: POs com approval status?
- [ ] **Ship-to address**: definido? (job site address em Construction)

### Julgamento critico
- Construction SEM POs = IRREALISTA. Toda construtora emite POs para materiais e subcontractors.
- PO→Bill→Payment chain e o WORKFLOW PRINCIPAL de AP em Construction. Se chain quebrado, demo falha.
- POs todos "Open" (nenhum Closed) = nunca foram recebidos/convertidos = chain incompleto
- POs sem vendor = erro de criacao
- PO de $1M para "Office Supplies" = categoria errada ou inflado

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Zero POs (Construction) | Criar 3-5 POs realistas com line items detalhados | Playwright → /app/purchaseorder/new |
| PO feature 404 | Habilitar em T28 (Expense Settings) | Playwright → Settings → Expenses |
| All Open (none closed) | Converter 1-2 POs para Bills para demonstrar chain | Playwright → Convert to Bill |
| Generic line items | Editar PO, add descricoes detalhadas | Playwright → edit PO |
| No project linkage | Associar POs a projetos | Playwright → edit PO |

### Output obrigatorio
```json
{
  "screen": "T34_PURCHASE_ORDERS",
  "entity": "...",
  "metrics": {"po_count": N, "status_mix": {"open": N, "closed": N, "partial": N}, "linked_to_bills": N, "project_linked": N, "realistic_vendors": N, "realistic_line_items": N, "date_range": "start - end", "feature_available": true/false},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN|N/A"
}
```

---

## TELA 35: SALES ORDERS (/app/salesorders)

### Como navegar
URL: `https://qbo.intuit.com/app/salesorders`
Esperar: 5s
Nota: Sales Orders sao feature especifica de certos tiers. Pode nao estar disponivel.

### O que olhar
- [ ] **Sales order count**: 3-10 ideal. Zero = feature nao usada (ok se nao disponivel)
- [ ] **Linked to estimates?**: SO criado a partir de estimate? Chain Estimate→SO→Invoice
- [ ] **Customer names**: realistas?
- [ ] **Line items**: detalhados?
- [ ] **Amounts**: proporcionais?
- [ ] **Status**: open, closed, partially fulfilled — mix?
- [ ] **Dates**: distribuidas?
- [ ] **Feature available?**: se 404, documentar N/A

### Julgamento critico
- Sales Orders nao sao comuns em Construction (mais usado em Wholesale/Distribution)
- Se feature disponivel e vazia, e ok — nao e critico para Construction demo
- Se tem SOs, devem ter line items detalhados e linked to customers reais
- Estimate→SO→Invoice chain = advanced workflow, excelente se presente

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Feature not available | Documentar como N/A | Documentar |
| SOs with generic data | Renomear se vale o esforco. Prioridade BAIXA | Playwright → edit SO |
| Zero SOs (feature available) | Ok para Construction. Documentar feature status | Documentar |

### Output obrigatorio
```json
{
  "screen": "T35_SALES_ORDERS",
  "entity": "...",
  "metrics": {"feature_available": true/false, "so_count": N, "linked_to_estimates": N, "status_mix": {"open": N, "closed": N, "partial": N}, "realistic_customers": N, "realistic_line_items": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN|N/A"
}
```

---

## TELA 36: INVENTORY OVERVIEW (/app/inventory/overview?jobId=inventory)

### Como navegar
URL: `https://qbo.intuit.com/app/inventory/overview?jobId=inventory`
Esperar: 6s
Alternativa: Left nav → Sales → Products & Services → Inventory tab

### O que olhar
- [ ] **Inventory items**: count? Nomes realistas? Construction = materials (Lumber, Cement, Rebar, Pipe)
- [ ] **Quantities on hand**: valores positivos? Zero qty = needs restock or setup issue
- [ ] **Reorder points**: definidos para items criticos? (mature inventory management)
- [ ] **Value on hand**: total value proporcional ao porte?
- [ ] **Cost per unit**: realista? (2x4 Lumber = $3-6/pc, Bag of Cement = $8-15)
- [ ] **SKUs**: definidos? (mostra maturidade)
- [ ] **Categories**: items organizados por categoria?
- [ ] **Low stock alerts**: algum item abaixo do reorder point?
- [ ] **Inventory tracking**: FIFO, Average Cost?

### Julgamento critico
- Construction usa inventory MODERADAMENTE (materials sao comprados per-project, nao mantidos em estoque grande)
- Manufacturing/Retail = inventory e CRITICO. Zero inventory items = DEALBREAKER
- Tire Shop = inventory e CORE (tires, wheels, accessories com qty e cost tracking)
- Inventory value > total annual revenue = INFLADO (nao mantem mais que 3-6 months of COGS)
- Items com qty negativa = ERRO GRAVE (sold more than purchased)

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Zero inventory (Manufacturing/Retail) | Documentar como P1 CRITICAL gap | Documentar |
| Negative quantities | Investigar: adjustment needed. Documentar como P1 | Documentar |
| Generic item names | Renomear para nomes realistas do setor | Playwright → edit item |
| No reorder points | Documentar como P3 (nice to have) | Documentar |
| Inflated value | Documentar como P2 finding | Documentar |

### Output obrigatorio
```json
{
  "screen": "T36_INVENTORY",
  "entity": "...",
  "metrics": {"item_count": N, "total_value_on_hand": N, "items_with_qty": N, "items_zero_qty": N, "items_negative_qty": N, "reorder_points_set": N, "tracking_method": "FIFO|Average", "categories": N, "skus_defined": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 37: CUSTOMER HUB - LEADS (/app/leads)

### Como navegar
URL: `https://qbo.intuit.com/app/leads`
Esperar: 5s
Nota: Advanced-tier CRM feature. Pode nao estar disponivel.

### O que olhar
- [ ] **Lead count**: 5-20 = good demo. Zero = feature vazia
- [ ] **Lead names**: realistas? Business names ou person names do setor
- [ ] **Sources**: defined? (Referral, Website, Phone, Trade Show)
- [ ] **Statuses**: New, Contacted, Qualified, Lost — mix?
- [ ] **Contact info**: email/phone preenchidos?
- [ ] **Notes/activities**: alguma activity logged?
- [ ] **Conversion**: leads convertidos para customers?
- [ ] **Feature available?**: se 404, documentar N/A

### Julgamento critico
- Leads e feature CRM do QBO Advanced. Para IES demo, mostra que QBO e mais que contabilidade.
- Construction: leads sao prospects de projetos (developers, property managers)
- Zero leads com feature disponivel = oportunidade perdida, mas nao critico
- Leads com "Test Lead" = CS violation

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Feature not available | Documentar como N/A | Documentar |
| Zero leads (feature available) | Criar 3-5 leads realistas se tempo permitir | Playwright → /app/leads/new |
| Generic lead names | Renomear para nomes realistas | Playwright → edit lead |

### Output obrigatorio
```json
{
  "screen": "T37_LEADS",
  "entity": "...",
  "metrics": {"feature_available": true/false, "lead_count": N, "by_status": {"new": N, "contacted": N, "qualified": N, "lost": N}, "sources_defined": N, "converted_to_customer": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN|N/A"
}
```

---

## TELA 38: CUSTOMER HUB - PROPOSALS (/app/proposals)

### Como navegar
URL: `https://qbo.intuit.com/app/proposals`
Esperar: 5s
Nota: Advanced-tier feature. Pode nao estar disponivel.

### O que olhar
- [ ] **Proposal count**: 3-10 = good demo
- [ ] **Proposal templates**: customizados? Com logo? Professional appearance?
- [ ] **Sent proposals**: algum foi enviado? Status = Sent, Viewed, Accepted, Declined?
- [ ] **Customer names**: realistas?
- [ ] **Amounts**: proporcionais? Construction proposal = $50K-$5M
- [ ] **Line items**: detalhados com scope of work?
- [ ] **Expiration dates**: definidas?
- [ ] **Feature available?**: se 404, documentar N/A

### Julgamento critico
- Proposals sao feature premium que demonstra sales workflow completo: Proposal→Estimate→Invoice
- Construction: proposals sao bids para projetos. Contem scope, timeline, pricing.
- Zero proposals com feature disponivel = feature nao demonstravel
- Proposal sem line items detalhados = parece generico, perde impacto

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Feature not available | Documentar como N/A | Documentar |
| Zero proposals | Documentar como P2 — feature vazia | Documentar |
| Generic content | Documentar como P3 | Documentar |

### Output obrigatorio
```json
{
  "screen": "T38_PROPOSALS",
  "entity": "...",
  "metrics": {"feature_available": true/false, "proposal_count": N, "by_status": {"draft": N, "sent": N, "viewed": N, "accepted": N, "declined": N}, "templates_customized": true/false, "realistic_content": true/false},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN|N/A"
}
```

---

## TELA 39: REPORTS - STANDARD (/app/standardreports or /app/reportlist)

### Como navegar
URL: `https://qbo.intuit.com/app/reportlist`
Esperar: 6s (report list pode ser longa)
Alternativa: `https://qbo.intuit.com/app/standardreports`
KPI Scorecard: `https://qbo.intuit.com/app/business-intelligence/kpi-scorecard`

### O que olhar
- [ ] **Report categories present**: Business Overview, Who Owes You, Sales & Customers, Expenses & Vendors, Employees, For My Accountant
- [ ] **Core 4 reports accessible**: Profit & Loss, Balance Sheet, Statement of Cash Flows, Trial Balance
- [ ] **P&L accessible and loads?**: quick click-test
- [ ] **Balance Sheet accessible and loads?**: quick click-test
- [ ] **Cash Flow Statement accessible?**: loads with data?
- [ ] **Trial Balance accessible?**: loads with data?
- [ ] **KPI Scorecard available?**: navigate to /app/business-intelligence/kpi-scorecard
- [ ] **Analytics dashboards**: Business Performance, Cash Flow? AI-powered insights?
- [ ] **Custom reports**: any saved custom reports?
- [ ] **Report export**: PDF/Excel export working?
- [ ] **Total report count**: typical IES has 60-80+ reports available

### Julgamento critico
- Reports sao a ESSENCIA do QBO. Se P&L ou BS nao carregam, todo o dataset e suspeito.
- Core 4 reports devem carregar com DADOS — nao templates vazios.
- KPI Scorecard e feature premium. Se disponivel e com dados = excelente differentiator.
- Cash Flow Statement vazio quando P&L tem income = INCONSISTENCIA (investigar accrual vs cash issues)
- Trial Balance deve balancear (debits = credits). Se nao, contabilidade esta quebrada.

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Core report nao carrega | Documentar como P1 CRITICAL | Documentar |
| Cash Flow Statement empty | Verificar accounting method (T29). Se accrual, checar JEs | QBO API |
| Trial Balance off-balance | Documentar como P1 CRITICAL — contabilidade quebrada | Documentar |
| KPI Scorecard empty | Documentar como P2 | Documentar |
| Reports missing categories | Documentar como P2 — tier limitation? | Documentar |

### Output obrigatorio
```json
{
  "screen": "T39_REPORTS_STANDARD",
  "entity": "...",
  "metrics": {"total_reports_available": N, "core_4_accessible": true/false, "pl_loads": true/false, "bs_loads": true/false, "cash_flow_loads": true/false, "trial_balance_loads": true/false, "trial_balance_balanced": true/false, "kpi_scorecard_available": true/false, "custom_reports_saved": N, "report_categories": N},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 40: REPORTS - P&L BY CLASS/LOCATION

### Como navegar
1. URL: `https://qbo.intuit.com/app/reportlist`
2. Procurar "Profit and Loss by Class" ou "Profit and Loss by Location"
3. Clicar no report
4. Esperar 10s (report pesado)
5. Resize viewport para capturar dados completos

**IES Workaround (se URL direta retorna 404 ou BLOCKED):**
- Alternativa 1: Ir para /app/standardreports → procurar "Profit and Loss by Class" na lista → clicar
- Alternativa 2: Ir para /app/standardreports → clicar em P&L normal → dentro do report, usar o filtro/dropdown "Rows: Class" se disponivel
- Alternativa 3: Usar Global Search → digitar "Profit and Loss by Class" → clicar no resultado
- Se todas alternativas falham: marcar como BLOCKED com nota "IES routing — 3 alternatives attempted"

### O que olhar
- [ ] **Classes showing data**: classes definidas em T24 mostram dados? Ou todas em $0?
- [ ] **Amounts cross-ref**: total income no P&L by Class = total income no P&L (T02)?
- [ ] **Unclassified column**: existe? Grande? (transacoes sem class assigned)
- [ ] **Distribution across classes**: balanced? Ou 95% em 1 class e 5% no resto?
- [ ] **All classes present**: classes criadas em T24 aparecem no report?
- [ ] **Report period**: matching T02 period?
- [ ] **Location version**: se locations habilitadas, verificar P&L by Location tambem
- [ ] **Cross-ref total**: sum of all classes = grand total?

### Julgamento critico
- "Unclassified" com 90% do valor = classes foram habilitadas mas nao usadas. Feature decorativa.
- Classes com $0 = criadas mas sem transacoes associadas. Nao agrega valor na demo.
- Total por class != Total P&L = INCONSISTENCIA no QBO. Documentar como finding.
- Construction ideal: Residential 40%, Commercial 35%, Government 15%, Other 10%

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| All Unclassified (90%+) | Documentar como P1 — classes nao estao sendo usadas | Documentar |
| Class with $0 | Documentar como P2 — class vazia | Documentar |
| Total mismatch | Documentar como P1 — inconsistencia | Documentar |
| Report not available | Verificar se class tracking esta ON (T29) | Playwright → Settings |

### Output obrigatorio
```json
{
  "screen": "T40_PL_BY_CLASS",
  "entity": "...",
  "metrics": {"classes_with_data": N, "classes_total": N, "unclassified_pct": "N%", "total_income_by_class": N, "total_income_pl": N, "match": true/false, "distribution": {"class_name": "N%", "...": "..."}},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 41: REPORTS - AR AGING (/app/reportlist -> AR Aging)

### Como navegar
1. URL: `https://qbo.intuit.com/app/reportlist`
2. Procurar "Accounts Receivable Aging" ou "A/R Aging Summary"
3. Clicar no report
4. Esperar 8s
5. Alternativa direta: search "AR Aging" no report list

**IES Workaround (se URL direta retorna 404 ou BLOCKED):**
- Alternativa 1: Ir para /app/standardreports → procurar "A/R Aging Summary" ou "Accounts Receivable Aging" → clicar
- Alternativa 2: Ir para /app/reportlist → categoria "What you owe" ou "Who owes you" → clicar AR Aging
- Se todas alternativas falham: marcar como BLOCKED com nota "IES routing — 2 alternatives attempted"

### O que olhar
- [ ] **Aging buckets**: Current, 1-30, 31-60, 61-90, 90+ — todas com dados?
- [ ] **Customer breakdown**: customers realistas nos buckets?
- [ ] **Total AR**: cross-ref com T05 Customers AR total — DEVE BATER
- [ ] **Current %**: ideal > 60% em Current (healthy AR)
- [ ] **90+ days %**: < 10% ideal. > 20% = collection problem
- [ ] **Customer concentration**: 1 customer com 80%+ do AR = concentration risk
- [ ] **Negative amounts**: customer com AR negativo? (overpayment ou credit)
- [ ] **Zero total**: $0 AR total = no receivables = entity sem invoices

### Julgamento critico
- AR Aging e report #1 que CFOs olham. Deve ser IMPECAVEL.
- 90+ days > 30% do total = collection disaster. Real companies dont let this happen.
- Total AR aqui DEVE bater com o AR do Balance Sheet (T03) e com T05 Customers tab.
- Se nao bate = inconsistencia nos dados. Investigar.
- Construction: AR aging 30-60 days e common (progress billing). >90 days = retainage ou problema.

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Total mismatch com T05 | Documentar como P1 — investigar diferenca | QBO API → search_invoices |
| 90+ > 30% | Documentar como P2 finding | Documentar |
| Zero AR | Documentar como P1 — no invoices? | Documentar |
| Negative customer AR | Investigar: overpayment? Credit memo? | QBO API → search_invoices |
| Single customer concentration | Documentar como P2 risk finding | Documentar |

### Output obrigatorio
```json
{
  "screen": "T41_AR_AGING",
  "entity": "...",
  "metrics": {"total_ar": N, "current": N, "days_1_30": N, "days_31_60": N, "days_61_90": N, "days_90_plus": N, "current_pct": "N%", "days_90_plus_pct": "N%", "customer_count": N, "top_customer_pct": "N%", "cross_ref_t05_match": true/false},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 42: REPORTS - AP AGING

### Como navegar
1. URL: `https://qbo.intuit.com/app/reportlist`
2. Procurar "Accounts Payable Aging" ou "A/P Aging Summary"
3. Clicar no report
4. Esperar 8s

**IES Workaround (se URL direta retorna 404 ou BLOCKED):**
- Alternativa 1: Ir para /app/standardreports → procurar "A/P Aging Summary" ou "Accounts Payable Aging" → clicar
- Alternativa 2: Ir para /app/reportlist → categoria "What you owe" → clicar AP Aging
- Se todas alternativas falham: marcar como BLOCKED com nota "IES routing — 2 alternatives attempted"

### O que olhar
- [ ] **Aging buckets**: Current, 1-30, 31-60, 61-90, 90+ — todas com dados?
- [ ] **Vendor breakdown**: vendors realistas nos buckets?
- [ ] **Total AP**: cross-ref com T06 Vendors AP total — DEVE BATER
- [ ] **Current %**: ideal > 70% em Current (company pays on time)
- [ ] **90+ days %**: < 5% ideal. > 15% = cash flow or management problem
- [ ] **Vendor concentration**: 1 vendor com 80%+ do AP = dependency risk
- [ ] **Negative amounts**: vendor com AP negativo? (prepayment ou credit)
- [ ] **Overdue ratio**: < 30% overdue = healthy. >50% = red flag

### Julgamento critico
- AP Aging mostra disciplina de pagamento. Empresa "saudavel" paga a maioria no prazo.
- Construction: subcontractor payments em 30-45 days e normal. >90 days = subcontractors vao reclamar (e viewer sabe disso)
- Total AP aqui DEVE bater com AP do Balance Sheet (T03) e T06 Vendors tab.
- Vendor concentration > 50% em 1 vendor = dependency. Documentar mas nao necessariamente problema.

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Total mismatch com T06 | Documentar como P1 — inconsistencia | QBO API → search_bills |
| 90+ > 20% | Documentar como P2 finding | Documentar |
| Zero AP | Documentar como P1 — no bills? | Documentar |
| Single vendor concentration | Documentar como P2 | Documentar |

### Output obrigatorio
```json
{
  "screen": "T42_AP_AGING",
  "entity": "...",
  "metrics": {"total_ap": N, "current": N, "days_1_30": N, "days_31_60": N, "days_61_90": N, "days_90_plus": N, "current_pct": "N%", "days_90_plus_pct": "N%", "vendor_count": N, "top_vendor_pct": "N%", "cross_ref_t06_match": true/false},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 43: AUDIT LOG (/app/auditlog)

### Como navegar
URL: `https://qbo.intuit.com/app/auditlog`
Esperar: 6s (audit log pode ser pesado com muitos entries)

### O que olhar
- [ ] **Recent activity**: entries nos ultimos 7 dias?
- [ ] **User names**: quem fez as mudancas? Nomes reais? (nao "test_user", "admin_bot")
- [ ] **Event types**: Login, Create, Edit, Delete — mix normal?
- [ ] **Data integrity**: nenhum pattern de mass-deletion ou mass-creation suspeito
- [ ] **No test/automation entries visible**: nenhum "Created by automation", "Sweep bot", "TBX script"
- [ ] **IP addresses**: se visivel, IPs consistentes? (nao 100 different IPs in 1 hour)
- [ ] **Entity types modified**: invoices, bills, JEs — activity across modules?
- [ ] **Deletion events**: muitos deletes recentes? (pode indicar cleanup — ok, mas nota-se)
- [ ] **Time distribution**: atividade distribuida ao longo de dias/semanas?

### Julgamento critico
- Audit log e onde TUDO aparece. Se fez edits em massa (sweep!), audit log mostra.
- Viewer expert OLHA o audit log. Se 50 edits no mesmo minuto por "automation_user" = BUSTED.
- Ideal: atividade de 2-3 users ao longo de semanas, com mix de creates/edits/logins
- Mass creates no mesmo timestamp = ingestion batch. Documentar se obvio.
- "Admin" user fazendo tudo = ok para small business (owner does everything)

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Automation/sweep entries visible | NAO PODE APAGAR AUDIT LOG. Documentar como risk. | Documentar |
| Test user names | NAO PODE EDITAR AUDIT LOG. Documentar como risk. | Documentar |
| Mass deletion pattern | Documentar como P1 risk | Documentar |
| Zero recent activity | Documentar como finding — stale entity | Documentar |

### NOTA CRITICA: Audit Log NAO pode ser editado. Ele e immutable. Qualquer rastro de sweep/automation la e PERMANENTE. A unica mitigacao e minimizar acoes que criam entries suspeitas durante o sweep.

### Output obrigatorio
```json
{
  "screen": "T43_AUDIT_LOG",
  "entity": "...",
  "metrics": {"recent_entries_7d": N, "unique_users": N, "user_names": ["..."], "event_types": {"login": N, "create": N, "edit": N, "delete": N}, "automation_traces_found": N, "mass_action_patterns": N, "date_range_of_activity": "start - end"},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 44: AI & INTELLIGENCE FEATURES (/app/business-intelligence)

### Como navegar
URL: `https://qbo.intuit.com/app/business-intelligence`
Esperar: 6s
Alternativa URLs:
- KPI Scorecard: `https://qbo.intuit.com/app/business-intelligence/kpi-scorecard`
- Cash Flow Planner: `https://qbo.intuit.com/app/cashflow`
Nota: IES Advanced feature. Muitas sub-features podem nao estar disponiveis.

**IES Workaround (se URL direta retorna 404 ou BLOCKED):**
- Alternativa 1: Ir para /app/business-intelligence/kpi-scorecard (KPI Scorecard direto)
- Alternativa 2: Ir para /app/standardreports → procurar "KPI" ou "Scorecard" ou "Dashboard" na lista
- Alternativa 3: Abrir qualquer report (P&L) → verificar se icones de AI (sparkle) aparecem → documentar presenca
- Se todas alternativas falham: marcar como BLOCKED com nota "IES routing — 3 alternatives attempted"

### O que olhar
- [ ] **AI categorization**: transacoes sendo auto-categorized? (bank feed matching)
- [ ] **Smart Match**: suggested matches presentes na banking feed?
- [ ] **Conversational BI**: "Ask Intuit Assist" feature disponivel? Funcional?
- [ ] **AI sparkle icons**: icones de AI visiveis em reports e dashboards?
- [ ] **KPI Scorecard**: metricas calculadas? Revenue growth, profit margin, cash runway?
- [ ] **Cash Flow Planner**: previsao de cash flow disponivel? Com dados?
- [ ] **Business Performance dashboard**: grafico de performance over time?
- [ ] **Insights/recommendations**: AI generating insights? ("Your expenses grew 15%...")
- [ ] **Feature availability**: quais AI features estao presentes vs. missing?

### Julgamento critico
- AI features sao o DIFERENCIAL #1 do IES vs. competitors. Se nenhuma AI feature funciona, demo perde impacto.
- KPI Scorecard com dados reais = EXCELENTE. Vazio = oportunidade perdida.
- "Ask Intuit Assist" e a flagship feature. Se disponivel e funcional, testar com 1-2 questions.
- AI sparkle icons em reports = visual indicator que AI esta ativa. Se ausentes, tier pode nao incluir.
- Cash Flow Planner precisa de dados historicos (3+ meses) para gerar previsao.

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| No AI features available | Documentar como N/A — tier limitation | Documentar |
| KPI Scorecard empty | Verificar se ha dados suficientes (3+ months) | Documentar |
| Intuit Assist broken/missing | Documentar como P2 | Documentar |
| Cash Flow Planner empty | Documentar — needs historical data | Documentar |

### Output obrigatorio
```json
{
  "screen": "T44_AI_INTELLIGENCE",
  "entity": "...",
  "metrics": {"ai_categorization": true/false, "smart_match": true/false, "intuit_assist": true/false, "kpi_scorecard": true/false, "kpi_scorecard_has_data": true/false, "cash_flow_planner": true/false, "ai_sparkle_icons": true/false, "insights_generated": true/false, "business_performance_dashboard": true/false},
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN|N/A"
}
```

---

## TELA 45: GLOBAL SEARCH (search bar top)

### Como navegar
1. Clicar na search bar no topo da pagina (magnifying glass icon)
2. Esperar search bar abrir
3. Executar 3-5 searches diferentes

### O que olhar
- [ ] **Search 1 — Customer name**: buscar nome de customer conhecido (de T05). Retorna resultados relevantes?
- [ ] **Search 2 — Invoice number**: buscar invoice number (de T31). Encontra o invoice?
- [ ] **Search 3 — Account name**: buscar account do COA (de T14). Retorna a conta?
- [ ] **Search 4 — Vendor name**: buscar vendor conhecido (de T06). Encontra?
- [ ] **Search 5 — Dollar amount**: buscar "$5,000" ou amount especifico. Retorna transacoes?
- [ ] **Result relevance**: resultados sao relevantes? Ou lixo?
- [ ] **Result speed**: < 3s para retornar? Ou slow?
- [ ] **No errors**: search nao retorna erro 500 ou "something went wrong"?
- [ ] **Cross-module results**: busca retorna invoices + bills + customers? (nao so 1 tipo)

### Julgamento critico
- Global search e feature de usabilidade. Se nao funciona, usuario fica frustrado na demo.
- Search que retorna "No results" para customer que EXISTE = BUG ou index stale
- Search que retorna resultados irrelevantes = poor relevance
- Speed > 5s = UX problem
- Search funcional com cross-module results = demonstrates system integration

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Search returns no results | Documentar como P2 — search index may be stale | Documentar |
| Search returns errors | Documentar como P1 — functional bug | Documentar |
| Slow search (>5s) | Documentar como P3 — performance issue | Documentar |
| Irrelevant results | Documentar como P2 | Documentar |

### Se encontrar TBX em resultados
- Identificar a SOURCE do TBX (invoice? customer? product?)
- Navegar ate o record original
- Se editavel: renomear
- Se system-generated (ex: invoice number): documentar como CS3 "not editable"

### Output obrigatorio
```json
{
  "screen": "T45_GLOBAL_SEARCH",
  "entity": "...",
  "metrics": {"searches_performed": N, "searches_successful": N, "searches_failed": N, "avg_response_time_ms": N, "cross_module_results": true/false},
  "search_tests": [
    {"query": "...", "result_count": N, "relevant": true/false, "time_ms": N},
    {"query": "...", "result_count": N, "relevant": true/false, "time_ms": N}
  ],
  "cs_violations": [],
  "findings": [],
  "fixes": [],
  "status": "PASS|FAIL|WARN"
}
```

---

## TELA 46: SURFACE SCAN BATCH (remaining pages)

### Como navegar
Para CADA pagina abaixo, navegar e verificar em < 30 segundos:
1. Loads? (nao 404, nao "something went wrong")
2. Has data? (nao completamente vazio)
3. Any TBX/test text visible?
4. Any obvious problems?

### Pages to scan
| # | Page | URL | Critical? |
|---|------|-----|-----------|
| 1 | Receipts | `/app/receipts` | Low |
| 2 | Mileage | `/app/mileage` | Low |
| 3 | Attachments | `/app/attachments` | Low |
| 4 | Tags | `/app/tags` | Medium |
| 5 | Subscriptions & Billing | `/app/subscriptions` | Low |
| 6 | Lending | `/app/lending` | Low |
| 7 | Workers Comp | `/app/workerscomp` | Medium (Construction) |
| 8 | Benefits | `/app/benefits` | Medium |
| 9 | Tax Center | `/app/tax/home` | Medium |
| 10 | Apps Marketplace | `/app/apps` | Low |
| 11 | Bank Connections | `/app/bankconnections` | Medium |
| 12 | Currency Settings | `/app/currency` | Low |
| 13 | Users & Roles | `/app/users` | Medium |
| 14 | Privacy & Data | `/app/privacy` | Low |
| 15 | Payment Methods | `/app/paymentmethods` | Low |
| 16 | Account & Settings Overview | `/app/settings` | Low |

### O que olhar (quick check per page)
- [ ] **Page loads**: HTTP 200, no error message, no 404
- [ ] **Has data**: not completely empty. At least placeholder content if feature unused.
- [ ] **No TBX/Test text**: no "TBX", "Test", "Sample", "Demo 3.5" visible
- [ ] **No broken UI**: no missing images, broken layouts, infinite spinners
- [ ] **Workers Comp (Construction)**: policy active? Coverage amounts realistic?
- [ ] **Bank Connections**: accounts connected? Last sync recent?
- [ ] **Users & Roles**: user names realistic? No "test_user@intuit.com"?
- [ ] **Tags**: if tags exist, names realistic?

### Julgamento critico
- Surface scan e catch-all. Nao precisa de deep analysis — so quick health check.
- Se Workers Comp 404 em Construction entity = missing critical industry feature
- Bank Connections sem sync recent = bank feeds mortos, afeta categorization
- Users com test names = CS violation visivel em user management

### Se encontrar problema
| Problema | Acao | Ferramenta |
|----------|------|------------|
| Page 404 | Documentar qual page, qual URL, qual entity | Documentar |
| TBX/Test text | Renomear se possivel. Se not editable, documentar | Playwright or Documentar |
| Broken UI | Screenshot + documentar | Playwright → screenshot |
| Workers Comp missing (Construction) | Documentar como P2 | Documentar |
| Bank connections dead | Documentar como P2 — bank feeds not syncing | Documentar |

### Output obrigatorio
```json
{
  "screen": "T46_SURFACE_SCAN",
  "entity": "...",
  "pages_scanned": N,
  "results": [
    {"page": "Receipts", "url": "/app/receipts", "loads": true/false, "has_data": true/false, "cs_violations": [], "issues": []},
    {"page": "...", "url": "...", "loads": true/false, "has_data": true/false, "cs_violations": [], "issues": []}
  ],
  "total_issues": N,
  "total_cs_violations": N,
  "status": "PASS|FAIL|WARN"
}
```

---

## ⚠ CHECKPOINT OBRIGATORIO (apos T46 da ULTIMA entity)

**Voce completou T01-T46 para todas as entities? Verifique:**
- [ ] Parent: T01-T46 com output JSON? (46 telas)
- [ ] P0 Child 1: T01-T15 com metricas reais? (15 telas, NAO shallow)
- [ ] P0 Child 2: T01-T15 com metricas reais? (15 telas, NAO shallow)
- [ ] P1 Children: T01+T02+T05+T06 com dados? (4 telas cada)
- [ ] Todos os CS violations encontrados foram CORRIGIDOS? (nao apenas documentados)
- [ ] phase_results.json tem output JSON para CADA tela de CADA entity?

**Se algum item acima nao foi feito: VOLTAR e completar antes de gerar report.**

---

## CROSS-ENTITY VALIDATION (after all entities processed)

> **QUANDO EXECUTAR**: Somente apos completar T01-T46 para TODAS as entities do account.
> **OBJETIVO**: Validar consistencia e integridade entre entities do mesmo account (parent + children).

### X01: P&L Consolidation

**Verificacao**: Soma do Net Income de todas child entities deve ser coerente com parent entity (se consolidated view existir).

- Extrair Net Income de cada entity (coletado em T02)
- Somar todos children
- Comparar com parent consolidated P&L
- Tolerancia: 5% variance (diferenca de timing, IC eliminations)

**Se problema**: Documentar qual entity tem discrepancia e valor. NAO tentar corrigir — pode ser IC elimination.

### X02: Legal Names Consistency

**Verificacao**: Legal names nao devem estar trocados entre entities.

- Listar todos legal names de T15 para cada entity
- Verificar: "Entity A" nao tem legal name de "Entity B" e vice-versa
- Verificar: DBA names fazem sentido para cada entity
- Cross-ref com entity picker names

**Se problema**: Documentar como P1 CRITICAL. Legal name swap = entidade inteira esta errada. NAO corrigir (REGRA #6).

### X03: Industry Match

**Verificacao**: Todas entities do mesmo account devem ter industria compativel.

- Parent entity = Construction → children devem ser Construction ou sub-specialty (Electrical, Plumbing, General)
- Entity com "Retail" industry em account de Construction = SUSPECT
- Exceptions: holding company com diversified subsidiaries (rare no demo context)

**Se problema**: Documentar como P2 finding. Industry mismatch pode ser intencional mas merece nota.

### X04: Intercompany Entities

**Verificacao**: IC (intercompany) entities devem existir como BOTH customer AND vendor across entities.

- Se Entity A paga Entity B → Entity B deve ser VENDOR em Entity A e CUSTOMER em Entity B
- Verificar: IC vendor/customer names match
- Verificar: IC balances are reasonable (nao $0 e nao $100M)
- Missing IC entity = transactions cant flow between entities

**Se problema**: Criar missing IC vendor/customer se apropriado. Documentar chain.

### X05: COA Alignment

**Verificacao**: Chart of Accounts deve ser ALINHADO entre entities (nao identico, mas consistente).

- Same account naming convention across entities
- Same account number ranges (se account numbers habilitados)
- No entity missing critical accounts (Bank, AR, AP, Revenue, COGS, Expense)
- Sub-accounts consistent where applicable

**Se problema**: Documentar discrepancias. COA differences podem ser intentional (entity-specific accounts) mas naming convention deve ser consistent.

### X06: Data Freshness Parity

**Verificacao**: Todas entities devem ter dados recentes (nao so parent ativo e children mortos).

- Para cada entity: quando foi a ultima transacao? (coletado em T01 dashboard dates)
- Freshness gap: se parent tem transacoes de Mar 2026 mas child parou em Dec 2025 = STALE CHILD
- Ideal: todas entities com transacoes dentro de 30 days da data do sweep
- Tolerancia: 60 days max gap entre entity mais recente e mais antiga

**Se problema**: Documentar quais children sao stale. Pode precisar de data injection (JEs) para refresh.

### X07: Transaction Chains Intact

**Verificacao**: Workflow chains principais estao intactos ACROSS entities.

- Estimate → Invoice chain: estimates em entity A geraram invoices?
- PO → Bill → Payment chain: POs convertidos em bills? Bills pagos?
- IC chain: entity A invoice → entity B bill (intercompany flow)
- Time → Invoice chain: time entries convertidos em billable invoices?
- Project chain: projects com estimates, invoices, bills, time entries linkados?

**Se problema**: Documentar chains quebrados. Priority depende do chain:
- IC chain broken = P1
- PO→Bill chain broken (Construction) = P1
- Estimate→Invoice broken = P2
- Time→Invoice broken = P2

### Cross-Entity Output obrigatorio
```json
{
  "screen": "CROSS_ENTITY_VALIDATION",
  "account": "...",
  "entities_validated": N,
  "checks": {
    "X01_pl_consolidation": {"status": "PASS|FAIL", "variance_pct": "N%", "details": "..."},
    "X02_legal_names": {"status": "PASS|FAIL", "swaps_found": N, "details": "..."},
    "X03_industry_match": {"status": "PASS|FAIL", "mismatches": N, "details": "..."},
    "X04_intercompany": {"status": "PASS|FAIL", "ic_pairs_expected": N, "ic_pairs_found": N, "missing": ["..."]},
    "X05_coa_alignment": {"status": "PASS|FAIL", "naming_consistent": true/false, "missing_critical_accounts": ["..."]},
    "X06_data_freshness": {"status": "PASS|FAIL", "freshest_entity": "...", "stalest_entity": "...", "gap_days": N},
    "X07_transaction_chains": {"status": "PASS|FAIL", "chains_checked": N, "chains_intact": N, "chains_broken": ["..."]}
  },
  "overall_status": "PASS|FAIL|WARN"
}
```

---

## REPORT GENERATION

> **QUANDO EXECUTAR**: Apos completar ALL screens (T01-T46) para ALL entities + Cross-Entity Validation.
> **OUTPUT**: Final sweep report in Markdown format.

### Report Template

```markdown
# QBO SWEEP REPORT — [DATASET_NAME]

> **Date**: YYYY-MM-DD
> **Sweeper**: God Complete v8.0
> **Account**: [ACCOUNT_NAME]
> **Entities**: N entities processed
> **Duration**: Xh Ym

---

## EXECUTIVE SUMMARY

- **Overall Score**: X/10
- **Realism Score**: YY/100
- **Content Safety**: ZZ violations found (N fixed, M documented)
- **Critical Findings**: N (P1)
- **Total Findings**: N
- **Total Fixes Applied**: N

---

## SCORE CALCULATION

### Overall Score (X/10)
| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Data Completeness (all screens have data) | 20% | /10 | |
| Data Realism (names, amounts, proportions) | 25% | /10 | |
| Content Safety (no TBX/test/sample) | 20% | /10 | |
| Feature Coverage (IES features working) | 15% | /10 | |
| Cross-Entity Integrity | 10% | /10 | |
| Report Consistency (numbers cross-ref) | 10% | /10 | |
| **TOTAL** | **100%** | | **X/10** |

### Realism Score (YY/100)
- Names realistic: +N points (max 20)
- Amounts proportional: +N points (max 20)
- Dates distributed: +N points (max 15)
- Industry-appropriate data: +N points (max 15)
- Transaction variety: +N points (max 10)
- Feature depth: +N points (max 10)
- Cross-entity coherence: +N points (max 10)
- **TOTAL**: YY/100

---

## CONTENT SAFETY SUMMARY

| # | Entity | Screen | Violation | Severity | Fixed? | Details |
|---|--------|--------|-----------|----------|--------|---------|
| 1 | ... | T01 | TBX text in widget | CS3 | Yes | Renamed to realistic |
| 2 | ... | T15 | Legal name "Testing_OBS" | CS2 | No (NEVER FIX) | Documented only |

---

## FIXES APPLIED

| # | Entity | Screen | What | Before | After | Method |
|---|--------|--------|------|--------|-------|--------|
| 1 | Entity A | T01 | Customer name | "Test Client" | "Riverside Developers" | Playwright edit |
| 2 | Entity A | T02 | Net Income | -$15,000 | +$45,000 | JE created |

---

## CROSS-ENTITY COMPARISON

| Check | Status | Details |
|-------|--------|---------|
| X01 P&L Consolidation | PASS/FAIL | Variance: N% |
| X02 Legal Names | PASS/FAIL | N swaps found |
| X03 Industry Match | PASS/FAIL | N mismatches |
| X04 Intercompany | PASS/FAIL | N/N pairs found |
| X05 COA Alignment | PASS/FAIL | Naming consistent: Y/N |
| X06 Data Freshness | PASS/FAIL | Gap: N days |
| X07 Transaction Chains | PASS/FAIL | N/N chains intact |

---

## PER-ENTITY RESULTS

### Entity: [NAME] (CID: [CID])
| Screen | Status | Key Metrics | Findings | Fixes |
|--------|--------|-------------|----------|-------|
| T01 Dashboard | PASS | Income $X, Net Profit $Y | 0 | 0 |
| T02 P&L | WARN | Margin 8% (ok for construction) | 1 | 0 |
| ... | ... | ... | ... | ... |

(Repeat for each entity)

---

## RECOMMENDATIONS

1. **P1 (Must fix before demo)**: [list]
2. **P2 (Should fix)**: [list]
3. **P3 (Nice to have)**: [list]
4. **N/A (Tier limitation)**: [list]
```

### Score Calculation Rules

**Overall Score (X/10)**:
- 9-10: Exceptional — ready for premium demo
- 7-8: Good — minor issues, acceptable for demo
- 5-6: Fair — noticeable issues, needs improvement
- 3-4: Poor — significant problems, demo risky
- 1-2: Critical — not demo-ready

**Realism Score (YY/100)**:
- 90-100: Indistinguishable from real company
- 70-89: Very realistic with minor tells
- 50-69: Noticeable artificial patterns
- 30-49: Clearly synthetic data
- 0-29: Obviously fake/test data

**Content Safety Severity Levels**:
- CS1: Test data visible in primary screens (Dashboard, P&L) — CRITICAL
- CS2: Test data in secondary screens (Settings, Audit Log) — HIGH
- CS3: Test data in tertiary screens (deep drill-down) — MEDIUM
- CS4: Test data only visible via API/search — LOW

---

## END OF PLAYBOOK

> **SWEEP PLAYBOOK v8.0** — God Complete
> Covers: 46 screens + Cross-Entity Validation + Report Generation
> Created: 2026-03-27
> Maintainer: Thiago (TSA)
>
> Este playbook e a referencia UNICA para execucao de sweeps.
> Qualquer desvio deve ser documentado e justificado.
> Nenhuma tela pode ser pulada sem justificativa.
> O output de cada tela e OBRIGATORIO.
> O report final e OBRIGATORIO.
