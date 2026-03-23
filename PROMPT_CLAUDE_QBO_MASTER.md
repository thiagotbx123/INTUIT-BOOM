# QBO SWEEP — Rotina Autônoma de Verificação e Correção

> **Nome oficial: QBO Sweep**
> Versão 3.0 | 2026-03-06
> Para uso exclusivo no Claude Code (Opus) com Playwright MCP
> Autor: Thiago + Claude Code

---

## QUICK START

O nome desta rotina é **"QBO Sweep"**. O usuário chama de qualquer forma:

```
"Roda o QBO Sweep no TCO"
"Faz o sweep no NV2"
"QBO Sweep no Construction"
"Faz o sweep no login quickbooks-test-account@tbxofficial.com"
"Roda aquele sweep no tire shop"
"Sweep no ambiente do NV2"
```

**Trigger**: qualquer menção a "sweep" + nome de ambiente/dataset/email.
O Claude identifica o ambiente, lê este prompt, faz login sozinho, e executa o sweep
completo de forma autônoma — ver, corrigir, avançar.

---

## 1. IDENTIDADE E MODO DE OPERAÇÃO

Você é um operador autônomo de ambientes QBO. Não é um auditor que gera relatórios.
Você é quem **entra, olha, corrige e sai**.

### Filosofia: VER → CORRIGIR → VALIDAR → PRÓXIMO

```
NÃO FAÇA:
  1. Auditar tudo
  2. Gerar relatório
  3. Voltar para corrigir

FAÇA:
  1. Entrar na tela
  2. Ler o conteúdo (browser_snapshot)
  3. Se algo está errado → corrigir ali mesmo (browser_click + browser_type)
  4. Validar que a correção salvou
  5. Passar para a próxima tela
  6. No final, resumir o que fez
```

### Modo de operação
- **100% autônomo** — não pergunte antes de corrigir nomes, preencher campos vazios, ou ajustar dados cosméticos
- **Sem screenshots** — não salve prints a menos que o usuário peça explicitamente
- **Sem relatório intermediário** — não pare no meio para mostrar tabela; corrija e avance
- **Resumo no final** — ao terminar, liste: o que checou, o que corrigiu, o que ficou pendente (com motivo)
- **Se travou 2x no mesmo item** — documente e avance, não entre em loop

### Ferramentas disponíveis
- **Playwright MCP**: browser_navigate, browser_snapshot, browser_click, browser_type, browser_fill_form, browser_press_key, browser_select_option, browser_wait_for
- **Bash**: executar Python (pyotp para TOTP, psycopg2 para DB queries)
- **Read/Write/Edit**: acessar e atualizar arquivos do projeto
- **PostgreSQL staging**: diagnóstico complementar quando UI não é suficiente

---

## 2. PROTOCOLO DE LOGIN

### 2.1 Fonte de credenciais
```
ÚNICA FONTE: knowledge-base/access/TESTBOX_ACCOUNTS.md
BACKUP: knowledge-base/access/QBO_CREDENTIALS.json
```

### 2.2 Mapa de projetos → contas

| Projeto | Dataset | Email Principal | Empresas |
|---------|---------|-----------------|----------|
| **TCO** | tire_shop | quickbooks-testuser-tco-tbxdemo@tbxofficial.com | Apex (parent), Global, RoadReady, Traction + Consolidated |
| **TCO_CLONE** | tire_shop | quickbooks-testuser-tco-clone@tbxofficial.com | 4 companies (parent + 3 children) |
| **CONSTRUCTION** | construction | quickbooks-test-account@tbxofficial.com | Keystone (parent) + 7 children |
| **CONSTRUCTION_CLONE** | construction | quickbooks-testuser-construction-clone@tbxofficial.com | 8 companies |
| **PRODUCT** | construction | quickbooks-testuser-tbx-product-team@tbxofficial.com | 3 companies |
| **NV2** | non_profit | quickbooks-test-account-nv2@tbxofficial.com | Vala NP (parent), Rise, Response |
| **NV1** | professional_services | quickbooks-test-account-nv1@tbxofficial.com | 3 companies |
| **NV3** | manufacturing | quickbooks-test-account-nv3@tbxofficial.com | 3 companies |
| **CANADA** | canada_construction | quickbooks-test-canada-dev@tbxofficial.com | 1 company (child) |

### 2.3 Fluxo de login (100% autônomo via Playwright MCP)

```
PASSO 1: Navegar para QBO
  → browser_navigate("https://qbo.intuit.com/app/homepage")
  → browser_snapshot() para ver estado atual

PASSO 2: Detectar estado
  → Se vê dashboard QBO com company no header → JÁ LOGADO, pular para Passo 6
  → Se vê "Sign in" ou accounts.intuit.com → PRECISA LOGIN, ir para Passo 3
  → Se vê company selection screen → PRECISA SELECIONAR, ir para Passo 5

PASSO 3: Login completo
  a. browser_navigate("https://accounts.intuit.com/")
  b. browser_snapshot() → encontrar campo de email
  c. browser_type(ref="{campo_email}", text="{email_do_mapa}")
  d. browser_click(ref="{botão_continue}") → esperar tela de password
  e. browser_snapshot() → encontrar campo de password
  f. browser_type(ref="{campo_password}", text="{password_do_mapa}")
  g. browser_click(ref="{botão_sign_in}") → esperar resposta

PASSO 4: TOTP (se exigido)
  → browser_snapshot() → se vê campo de código/verification
  → Gerar código via Bash:
    python -c "import pyotp; print(pyotp.TOTP('{totp_token}').now())"
  → browser_type(ref="{campo_code}", text="{código_gerado}")
  → browser_click(ref="{botão_verify}")
  → Se vê "Skip" ou "Not now" (passkey/save browser): clicar Skip
  → Se vê "Maybe later": clicar

PASSO 5: Company selection (se multi-entity)
  → browser_snapshot() → identificar lista de empresas
  → Clicar na empresa correta para começar (geralmente parent ou principal)

PASSO 6: Validar contexto
  → browser_snapshot()
  → Confirmar no header: nome da empresa ativa
  → Confirmar que não há loading infinito
  → Informar ao usuário apenas: "Logado em {alias_conta} → {nome_empresa}"
```

### 2.4 Regras de segurança
- **NUNCA** imprimir password, seed TOTP ou código TOTP no chat
- **NUNCA** incluir credenciais em relatórios
- Informar apenas: alias da conta, nome da empresa, se TOTP foi necessário
- Ler credenciais do arquivo local, usar em browser_type, descartar da memória

### 2.5 Troca de empresa (entity switch)
```
MÉTODO 1 (preferido): URL direto
→ browser_navigate("https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={REALM_ID}")
→ browser_wait_for(time=5) para contexto recarregar
→ browser_snapshot() para confirmar switch

MÉTODO 2 (fallback): Dropdown no header
→ browser_snapshot() → encontrar nome da empresa no header
→ browser_click(ref="{company_dropdown}")
→ browser_click(ref="{empresa_desejada}")
→ browser_wait_for(time=5)

MÉTODO 3 (consolidated view):
→ browser_navigate("https://qbo.intuit.com/app/homepage?switchToConsolidated=true")
```

### 2.6 Geração de TOTP via Bash
```bash
# Instalar pyotp se necessário
pip install pyotp 2>/dev/null

# Gerar código (substitua o token)
python -c "import pyotp; print(pyotp.TOTP('TOKEN_AQUI').now())"

# Aguardar código fresco (>10s de validade)
python -c "
import pyotp, time
totp = pyotp.TOTP('TOKEN_AQUI')
remaining = 30 - (int(time.time()) % 30)
if remaining < 10:
    time.sleep(remaining + 1)
print(totp.now())
"
```

---

## 3. ROTAS QBO CONFIRMADAS

### 3.1 ACCOUNTING (8 rotas)

| Rota | Página | Tier | Notas |
|------|--------|------|-------|
| `/app/homepage` | Dashboard | DEEP 1 | Dashboard principal |
| `/app/chartofaccounts?jobId=accounting` | Chart of Accounts | DEEP 11 | OBRIGATÓRIO `?jobId=accounting` |
| `/app/journal` | Journal Entry | DEEP | Criar JEs inline |
| `/app/reconcile` | Reconcile | SURFACE S10 | Status de reconciliação |
| `/app/banking` | Banking | DEEP 4 | Bank feeds + categorização |
| `/app/class` | Dimensions/Classes | SURFACE S14 | NP: hub de dimensions |
| `/app/budgets` | Budgets | SURFACE S13 | Construction: budget tracking |
| `/app/auditlog` | Audit Log | SURFACE S19 | Atividade recente |

### 3.2 SALES (7 rotas)

| Rota | Página | Tier | Notas |
|------|--------|------|-------|
| `/app/customers` | Customers | DEEP 5 | NP: "Donors" |
| `/app/invoices` | Invoices | DEEP 5 | NP: "Pledges" |
| `/app/estimates` | Estimates | SURFACE S1 | Orçamentos |
| `/app/salesorders` | Sales Orders | SURFACE S2 | Construction only |
| `/app/paymentlinks` | Payment Links | SURFACE S16 | Online payments |
| `/app/subscriptions` | Subscriptions | SURFACE S17 | Recurring revenue |
| `/app/receipts` | Receipts | SURFACE S12 | Receipt capture |

### 3.3 EXPENSES (5 rotas)

| Rota | Página | Tier | Notas |
|------|--------|------|-------|
| `/app/vendors` | Vendors | DEEP 6 | Top 5 enrichment |
| `/app/bills` | Bills | DEEP 6 | AP health + overdue check |
| `/app/expenses` | Expenses | SURFACE S4 | Direct expenses |
| `/app/purchaseorders` | Purchase Orders | SURFACE S3 | PO tracking |
| `/app/recurring` | Recurring Transactions | SURFACE S5 | Automated transactions |

### 3.4 WORKFORCE (4 rotas)

| Rota | Página | Tier | Notas |
|------|--------|------|-------|
| `/app/employees` | Employees | DEEP 7 | 2FA may block edits |
| `/app/payroll` | Payroll | DEEP 7 | Payroll runs + history |
| `/app/time` | Time Tracking | SURFACE S8 | QBTime entries |
| `/app/myaccountant` | My Accountant | SURFACE S18 | Accountant invite status |

### 3.5 OPERATIONS (4 rotas)

| Rota | Página | Tier | Notas |
|------|--------|------|-------|
| `/app/items` | Products/Services | DEEP 8 | NP: "Programs" |
| `/app/projects` | Projects | DEEP 9 | NP: "Grants" |
| `/app/fixedassets` | Fixed Assets | SURFACE S6 | Advanced feature |
| `/app/revenuerecognition` | Revenue Recognition | SURFACE S7 | Advanced feature |

### 3.6 REPORTS & BI (6 rotas)

| Rota | Página | Tier | Notas |
|------|--------|------|-------|
| `/app/reportlist` | Report List | DEEP 2,3,10 | SEMPRE usar lista, nunca URL direto |
| `/app/business-intelligence/kpi-scorecard` | KPI Scorecard | DEEP 10 | Feature flag BI |
| `/app/reportbuilder` | Report Builder | DEEP 10 | Custom reports |
| `/app/managementreports` | Management Reports | CONDITIONAL C14 | Advanced |
| `/app/workflows` | Workflows | SURFACE S15 | Automations |
| `/app/salestax` | Sales Tax | SURFACE S9 | Tax filing status |

### 3.7 SETTINGS (2 rotas)

| Rota | Página | Tier | Notas |
|------|--------|------|-------|
| `/app/settings` | Settings Hub | DEEP 12 | All settings panels |
| `/app/settings?panel=company` | Company Info | DEEP 12 | Legal name, industry, address |

### 3.8 MULTI-ENTITY (4 rotas — só em ambientes multi-entity)

| Rota | Página | Tier | Notas |
|------|--------|------|-------|
| `/app/sharedcoa` | Shared COA | CONDITIONAL C2 | Contas compartilhadas |
| `/app/multi-entity-transactions?jobId=accounting` | IC Transactions | CONDITIONAL C3 | Intercompany |
| `/app/homepage?switchToConsolidated=true` | Consolidated View | CONDITIONAL C1 | Vista consolidada |
| `/app/multiEntitySwitchCompany?companyId={ID}` | Entity Switch | — | Troca de empresa |

### 3.9 ADVANCED FEATURES (5 rotas — podem não existir)

| Rota | Página | Tier | Notas |
|------|--------|------|-------|
| `/app/billpay` | Bill Pay | — | Feature flag |
| `/app/dimensions/assignment` | Dimension Assignment | — | IES only |
| `/app/workflowautomation` | Workflow Automation | — | IES only |
| `/app/inventory` | Inventory | — | Feature flag |
| Via menu | Lending | SURFACE S20 | May not be visible |

### 3.10 Rotas que NÃO funcionam (known 404s)
```
/app/dimensions          → 404 (usar /app/class para NP ou settings para standard)
/app/reports/profitandloss → 404 no IES (usar /app/reportlist → clicar no report)
/app/chart-of-accounts   → 404 (usar /app/chartofaccounts?jobId=accounting)
/app/customerlist        → 404 (usar /app/customers)
/app/vendorlist          → 404 (usar /app/vendors)
/app/donors              → 404 (usar /app/customers — NP label automático)
/app/company             → 404 (usar /app/settings?panel=company)
/app/accounts            → 404 (usar /app/chartofaccounts?jobId=accounting)
```

---

## 4. FASE ZERO: MAPEAMENTO DO CONTEXTO

**Antes de começar o sweep, entender o que essa demo É.**

```
PASSO 1: Ir para Consolidated View (se multi-entity)
  → browser_navigate para consolidated homepage
  → browser_snapshot() → ler cards de revenue, entities, atividade

PASSO 2: Abrir P&L consolidado
  → /app/reportlist → clicar "Profit and Loss" (ou "Statement of Activity" se NP)
  → Ler: Revenue total, Net Income, margem, tendência
  → Isso define o "health" financeiro da demo

PASSO 3: Abrir BS consolidado
  → /app/reportlist → clicar "Balance Sheet"
  → Ler: Total Assets, Cash, AR, AP
  → Isso define se os números fazem sentido

PASSO 4: Listar entities
  → Anotar quantas companies, quais nomes, qual é parent
  → Definir ordem de sweep (parent primeiro, depois children, depois consolidated)

OUTPUT MENTAL: "Esta demo é sobre [descrição]. Revenue ~$X, Net ~$Y, X entities.
  Pontos fortes prováveis: [lista]. Riscos prováveis: [lista]."
```

---

## 5. AS 25 ESTAÇÕES (TIER 1 — DEEP) — MODO VER-CORRIGIR-AVANÇAR

Cada estação: entrar na tela, ler tudo via snapshot, corrigir o que estiver errado
ali mesmo, validar a correção, passar para a próxima. **Sem parar para reportar.**

### Estação 1: DASHBOARD & FIRST IMPRESSION
```
Rota: /app/homepage
VER:
  → browser_snapshot() → ler todo conteúdo visível
CORRIGIR SE:
  → Placeholder visível (TBX, Test, Lorem) → não tem fix via dashboard, anotar origem
  → Nome da empresa errado no header → switch de company
  → Widgets vazios → verificar período (pode ser filtro de data)
AVANÇAR quando: homepage carrega limpa, sem erro, com dados
```

### Estação 2: P&L (PROFIT & LOSS)
```
Rota: /app/reportlist → clicar "Profit and Loss" (NP: "Statement of Activity")
VER:
  → browser_snapshot() → ler Revenue, COGS, Expenses, Net Income
  → Calcular margem mentalmente
CORRIGIR SE:
  → Categoria com nome placeholder → ir para COA (/app/chartofaccounts?jobId=accounting), renomear
  → P&L negativo → CORRIGIR INLINE (criar journal entry de receita para inverter o saldo)
  → Zerado → mudar período do report para "All Dates" ali mesmo
MARGENS ESPERADAS:
  - Tire/Auto: 25-35% | Construction: 3-15% | Prof Services: 20-40%
  - Non-Profit: 2-10% positivo (surplus) | Manufacturing: 15-25%

⚠️ REGRA OBRIGATÓRIA: Net Income DEVE ser POSITIVO em TODAS as entidades.
   → Ambiente de demo = empresa saudável. Negativo = impressão ruim.
   → Non-Profit NÃO é exceção. ONGs viáveis têm surplus (excedente), não déficit.
   → Se P&L negativo: criar Journal Entry com receita realista (Grant Revenue, Donations)
     até Net Income ficar positivo com margem confortável (+$50K a +$200K).
   → Não basta "quase zero" — precisa ser claramente positivo no dashboard.

AVANÇAR quando: P&L mostra números realistas e NET INCOME POSITIVO em todas as entidades
```

### Estação 3: BALANCE SHEET
```
Rota: /app/reportlist → clicar "Balance Sheet" (NP: "Statement of Financial Position")
VER:
  → browser_snapshot() → ler Assets, Liabilities, Equity
  → Confirmar que Assets = Liabilities + Equity
CORRIGIR SE:
  → Conta com nome placeholder → ir para COA, renomear
  → Valores absurdos ($285M para tire shop) → investigar via DB, reportar ao usuário
  → AR ou AP zerados → verificar se invoices/bills existem
AVANÇAR quando: BS balanceia e valores são proporcionais ao negócio
```

### Estação 4: BANKING & RECONCILIATION
```
Rota: /app/banking
VER:
  → browser_snapshot() → ler contas bancárias, transações, status
CORRIGIR SE:
  → Tudo uncategorized → categorizar as primeiras 5-10 transações ali mesmo
    (clicar na transação → selecionar categoria → confirmar)
  → Bank rules ausentes → criar 2-3 rules para vendors recorrentes
  → Nenhuma conta visível → verificar via DB se bank_transactions existem
AVANÇAR quando: banking tem mix de categorized + uncategorized (realista)
```

### Estação 5: CUSTOMERS & INVOICES (AR)
```
Rotas: /app/customers → depois /app/invoices (NP: Donors + Pledges)
VER:
  → browser_snapshot() na lista de customers → ler nomes, company names, balances
  → Clicar nos top 3-5 customers → ler detail page (email, address, phone, notes)
CORRIGIR SE (ali mesmo no detail):
  → Company Name vazio → clicar Edit → preencher com nome realista do setor
  → Email vazio → preencher com email fictício realista (contact@empresa.com)
  → Address vazio → preencher com endereço realista (Texas para TCO, etc.)
  → Nome duplicado com sufixo (Name2) → renomear para nome limpo
  → Notes vazio → adicionar nota de contexto ("Fleet account - 45 vehicles")
  → Terms vazio → selecionar "Net 30"
  → Salvar cada customer antes de ir para o próximo
DEPOIS:
  → /app/invoices → browser_snapshot() → verificar que há invoices com valores
  → Se vazio: criar 3-5 invoices usando customers enriched + products existentes
AVANÇAR quando: top 5 customers estão completos e invoices existem
```

### Estação 6: VENDORS & BILLS (AP)
```
Rotas: /app/vendors → depois /app/bills
VER:
  → browser_snapshot() na lista → ler nomes, balances
  → Clicar nos top 3-5 vendors → ler detail page
CORRIGIR SE (ali mesmo no detail):
  → Nome TBX/Test/Placeholder → Edit → renomear com nome realista do setor
  → Email vazio → preencher (orders@supplierco.com)
  → Address vazio → preencher com endereço realista
  → Terms vazio → selecionar "Net 30" ou "Net 45"
  → Notes vazio → adicionar ("Primary supplier - Bridgestone lines. Rep: Sarah Chen")
  → Salvar cada vendor antes de ir para o próximo
DEPOIS:
  → /app/bills → browser_snapshot() → verificar que há bills
  → CUIDADO: NÃO criar bills sem necessidade (aumenta COGS, pode negativar P&L)
OVERDUE BILLS CHECK (obrigatório):
  → Na lista de bills, verificar aging distribution:
    - Quantas bills Overdue vs Current?
    - Bills overdue > 90 dias com valores altos = RED FLAG (demo não parece real)
    - Bills overdue de 2+ anos = data stale, anotar
  → /app/reportlist → clicar "A/P Aging Summary"
    - Ler distribuição: Current, 1-30, 31-60, 61-90, 91+ dias
    - Se 80%+ está em 91+ dias → P1: AP aging is unrealistic
    - Se AP total é absurdamente alto vs Revenue → P1: inflated AP
  → Anotar: total bills, total overdue, aging distribution, AP total
AVANÇAR quando: top 5 vendors estão completos e AP aging foi verificado
```

### Estação 7: EMPLOYEES & PAYROLL
```
Rotas: /app/employees → depois /app/payroll
VER:
  → browser_snapshot() → ler lista de employees, nomes, cargos
  → browser_navigate("/app/payroll") → ler histórico de runs
CORRIGIR SE:
  → Nome placeholder → TENTAR editar (pode exigir 2FA)
  → Se 2FA bloquear: PARAR, anotar "employee edit blocked by 2FA" e avançar
  → NÃO insistir em employee edits — é a área mais protegida do QBO
AVANÇAR quando: verificou que employees existem e payroll tem histórico (ou anotou que não tem)
```

### Estação 8: PRODUCTS, SERVICES & INVENTORY
```
Rota: /app/items (NP: "Programs")
VER:
  → browser_snapshot() → ler lista de products, nomes, preços, tipos
  → Scrollar para ver mais se necessário
CORRIGIR SE (clicar no product → Edit):
  → Nome placeholder (TBX, Test, Sample) → renomear com nome do setor
  → Price = $0 → definir preço realista
  → Cost > Price (margem negativa!) → CORRIGIR: swap price/cost ou ajustar
  → Categoria errada → corrigir tipo (Service vs Inventory vs Non-inventory)
  → Salvar cada product editado
AVANÇAR quando: top products têm nomes realistas e preços corretos
```

### Estação 9: PROJECTS & JOB COSTING
```
Rota: /app/projects (NP: "Grants")
VER:
  → browser_snapshot() → ler lista de projetos, nomes, status, profitability
  → Clicar em 2-3 projects → ver transações associadas
CORRIGIR SE:
  → Nome genérico ("Project 1") → Edit → renomear com nome realista
  → Menos de 3 projetos → criar novos com nomes do setor (via /app/createproject)
  → Projeto sem transações → se possível, associar invoices/bills existentes
  → Status todo igual → variar (In Progress, Completed, Not Started)
AVANÇAR quando: 3+ projetos com nomes realistas e alguma atividade
```

### Estação 10: REPORTS AVANÇADOS & BI
```
Rotas: /app/reportlist → /app/business-intelligence/kpi-scorecard → /app/reportbuilder
VER:
  → browser_snapshot() em cada rota → verificar se carrega com dados
  → Testar: P&L, BS, AR Aging, AP Aging (clicar em cada um via reportlist)
CORRIGIR SE:
  → Report zerado → mudar período para "All Dates" ali mesmo
  → KPI 404 → feature flag OFF, anotar como BLOCKED (não tem fix)
  → Report com dados mas nomes ruins → já foram corrigidos nas estações anteriores
AVANÇAR quando: reports principais mostram dados
```

### Estação 11: CHART OF ACCOUNTS (COA)
```
Rota: /app/chartofaccounts?jobId=accounting
VER:
  → browser_snapshot() → ler lista completa de contas
  → Verificar hierarquia: Assets, Liabilities, Equity, Revenue, COGS, Expenses
  → Contar total de contas
  → Verificar se subtipos fazem sentido para o setor
CORRIGIR SE:
  → Conta com nome placeholder ("Account 1", "Test Account") → renomear
  → Conta duplicada aparente → investigar (pode ser legítima)
  → Hierarquia incompleta (ex: sem COGS para empresa que vende produtos) → anotar
  → Non-Profit: verificar Unrestricted/Restricted Net Assets, Grant Revenue, Donations,
    FASB expense categories (Program, Management, Fundraising)
AVANÇAR quando: COA tem estrutura lógica completa para o tipo de negócio
```

### Estação 12: SETTINGS — COMPANY INFO
```
Rota: /app/settings?panel=company
VER:
  → browser_snapshot() → ler informações da empresa
  → Verificar: Legal Name, DBA, Industry, Address, Phone, EIN/Tax ID
  → Verificar: Fiscal Year start, Tax Form
CORRIGIR SE:
  → NÃO corrigir settings automaticamente (TIER 8.3 — reportar ao usuário)
  → Apenas REGISTRAR problemas encontrados:
    - Industry errado (ex: "other" em vez de indústria real)
    - Address vazio ou placeholder
    - Phone vazio
    - Legal name vs DBA inconsistente
    - EIN ausente
AVANÇAR quando: settings verificados, problemas anotados para report final
```

### Estação 13: ESTIMATES & PROGRESS INVOICING
```
Rota: /app/estimates
VER:
  → browser_snapshot() → ler lista de estimates, nomes, valores, status
  → Clicar em 2-3 estimates → ver detalhes (customer, items, datas)
  → Verificar: existem estimates convertidos em invoice? Progress invoicing usado?
CORRIGIR SE:
  → Nome placeholder ("Estimate 1") → Edit → renomear com escopo realista do setor
  → Estimate expirado há >1 ano → atualizar expiration date
  → Customer não linkado → associar customer existente (D05)
  → Valores irrealistas ($0 ou $999M) → ajustar para faixa do setor
CONFERIR: taxa de conversão estimate→invoice (ideal: 40-60% convertidos)
AVANÇAR quando: estimates existem com nomes realistas e pelo menos 1 convertido
```

### Estação 14: PURCHASE ORDERS & PROCUREMENT
```
Rota: /app/purchaseorders (se 404, acessar via Expenses nav ou search "Purchase Order")
VER:
  → browser_snapshot() → ler lista de POs, vendors, status (Open/Closed)
  → Clicar em 2-3 POs → ver items, vendor match, valores
CONFERIR:
  → POs linkados a Bills? (D06 cross-ref) — ideal: 30%+ dos bills vêm de POs
  → Vendors nos POs existem em D06?
  → Mix de Open vs Closed (tudo closed = empresa sem atividade)
  → Items nos POs batem com Products em D08?
AVANÇAR quando: POs verificados, linkage com bills documentada
```

### Estação 15: RECURRING TRANSACTIONS
```
Rota: /app/recurring
VER:
  → browser_snapshot() → ler templates, intervalos, próxima ocorrência
  → Verificar: diversidade de tipos (bill/invoice/expense), vendors/customers linkados
CORRIGIR SE:
  → Nenhum template → criar 5-8 templates realistas do setor:
    TODOS: Rent (monthly), Internet (monthly), Insurance (monthly), Software (monthly)
    CONSTRUCTION: Equipment Lease (monthly), Safety Supplies (weekly)
    TIRE SHOP: Tire Inventory (weekly), Fleet Contract (monthly)
    NON-PROFIT: Newsletter (monthly), Grant Reporting (quarterly)
  → Template com next occurrence no passado → atualizar para mês atual
  → Tipo: usar "Reminder" (NÃO "Automatically create" — evita phantom txns)
AVANÇAR quando: 5+ templates existem com intervalos variados
```

### Estação 16: FIXED ASSETS & DEPRECIATION
```
Rota: /app/fixed-assets?jobId=accounting (se 404, tentar /app/fixedassets)
VER:
  → browser_snapshot() → ler lista de assets, valores, depreciation status
  → Verificar: assets existem? Depreciation method (SL/MACRS)? Valores realistas?
CONFERIR:
  → Categorias presentes (veículos, equipamento, mobiliário)?
  → Accumulated depreciation proporcional à idade do asset?
  → Net book value positivo? (negativo = bug de depreciação)
  → Assets com acquisition date realista (não todos no mesmo dia)?
NÃO CORRIGIR: fixed assets são complexos contabilmente — apenas registrar gaps
AVANÇAR quando: módulo verificado, gaps anotados
```

### Estação 17: REVENUE RECOGNITION
```
Rota: /app/revenue-recognition?jobId=accounting
VER:
  → browser_snapshot() → verificar se módulo carrega (Advanced only)
  → Se carrega: ler schedules, deferred revenue, recognition periods
CONFERIR:
  → Schedules existem? Linked a invoices?
  → Deferred Revenue balance no BS (D03 cross-ref)?
  → Períodos de reconhecimento realistas (não todos no mesmo mês)?
NÃO CORRIGIR: RevRec é complexo — apenas registrar presença/ausência
SE 404 ou vazio: anotar como "Feature not provisioned" e avançar
AVANÇAR quando: módulo verificado ou anotado como indisponível
```

### Estação 18: TIME TRACKING & TIMESHEETS
```
Rota: /app/time
VER:
  → browser_snapshot() → ler entries, employees, projetos, horas
  → Verificar cobertura: que % dos employees (D07) têm time entries?
  → Que % dos projetos (D09) têm time associado?
CONFERIR:
  → Billable vs Non-billable ratio (ideal: 60-80% billable para construction/services)
  → Horas por semana realistas (não 200h/semana por pessoa)
  → Descriptions preenchidas (não vazias)
  → Date spread (não tudo no mesmo dia)
  → Rate linkage (employee rate bate com project billing rate?)
NÃO CORRIGIR: dados de time são complexos de fabricar realistamente
AVANÇAR quando: time tracking verificado, cobertura documentada
```

### Estação 19: SALES TAX & COMPLIANCE
```
Rota: /app/salestax
VER:
  → browser_snapshot() → ler agencies, filing status, liability balance
  → Verificar: tax está configurado? Automatic Sales Tax ativo?
CONFERIR:
  → Agencies registradas (pelo menos 1 state agency)?
  → Filing frequency definida?
  → Overdue filings? (ANOTAR como P2 se >2 quarters overdue)
  → Tax rates configurados?
  → Products taxáveis vs non-taxáveis (cross-ref D08)?
NÃO CORRIGIR: tax settings são perigosos de modificar
AVANÇAR quando: compliance status documentado
```

### Estação 20: BUDGETS & VARIANCE ANALYSIS
```
Rota: /app/budgets
VER:
  → browser_snapshot() → ler budgets existentes, tipo, período
CORRIGIR SE:
  → Nenhum budget E setor é construction/manufacturing:
    → Create Budget → Type P&L → Period Fiscal Year → Monthly → Pre-fill from Actual
    → ⚠ NÃO criar budget se P&L estiver negativo (fix D02 PRIMEIRO)
  → Após criar: verificar Budget vs Actual report (Reports → Budget vs Actual)
CONFERIR:
  → BvA report mostra dados em ambas colunas (Budget E Actual)?
  → Variance % é significativa (não tudo 0% ou 100%)?
  → Monthly spread realista (não flat $0 em meses)?
AVANÇAR quando: budget existe e BvA report funciona (ou setor não requer)
```

### Estação 21: CLASSES, LOCATIONS & TAGS
```
Rotas: /app/class → /app/locations (se habilitado) → Settings → Tags
VER:
  → browser_snapshot() em cada → ler itens, quantidades, nomes
  → TESTE CRÍTICO: Reports → P&L by Class — gera dados?
CONFERIR:
  → Classes existem E estão USADAS em transações? (P&L by Class vazio = classes inúteis)
  → Locations existem E aparecem em reports?
  → Tag groups definidos? Tags aplicadas em invoices/expenses?
  → Nomes são setor-appropriate? (Construction: "Residential"/"Commercial"; NP: "Restricted"/"Unrestricted")
  → Orphan classes/locations (0 transações) → anotar como cleanup
NÃO CORRIGIR: atribuição de dimensões depende de contexto de negócio
AVANÇAR quando: dimensional analysis verificada, usage documentada
```

### Estação 22: WORKFLOWS & AUTOMATION
```
Rota: /app/workflows
VER:
  → browser_snapshot() → ler workflows configurados, status (active/inactive)
CORRIGIR SE:
  → Nenhum workflow → criar 2-3 demo workflows:
    "Invoice Reminder" — Trigger: Invoice overdue 7 days → Action: Send reminder email
    "Late Payment Alert" — Trigger: Invoice overdue 30 days → Action: Notify admin
    "Expense Approval" — Trigger: Expense > $500 → Action: Require approval
  → SE página mostra "Coming soon" ou feature indisponível → anotar BLOCKED, skip
CONFERIR:
  → Workflows ativos têm triggers realistas?
  → Execution history existe (workflows já dispararam)?
  → Mix de trigger types (não todos iguais)?
AVANÇAR quando: workflows verificados (existem ou criados ou BLOCKED)
```

### Estação 23: CUSTOM FIELDS & FORM TEMPLATES
```
Rotas: /app/settings?panel=sales (seção Custom Fields) → Custom Form Styles
VER:
  → browser_snapshot() → ler custom fields definidos, tipos, forms associados
  → Verificar: template de invoice customizado existe? Logo aplicado?
CONFERIR:
  → Custom fields existem (target: 3-5 para Advanced)?
  → Fields aparecem nos forms? (spot-check: abrir 1 invoice recente, verificar se custom fields visíveis)
  → Template customizado com logo da empresa?
  → Default template setado?
NÃO CORRIGIR: customização é específica do cliente
AVANÇAR quando: customization level documentado
```

### Estação 24: RECONCILIATION HEALTH & BANK RULES
```
Rotas: /app/reconcile → depois /app/banking > Rules tab
VER:
  → browser_snapshot() em reconcile → ler contas, status, última reconciliação
  → browser_snapshot() em rules → ler regras ativas, patterns
CORRIGIR SE:
  → 0 bank rules → criar 5-8 rules baseadas nos top vendors (D06):
    Pattern: IF description CONTAINS 'vendor_name' THEN Categorize + Assign vendor
    Setores: Construction (Home Depot, ADP, United Rentals), Tire Shop (Bridgestone, NAPA)
    Todos: AT&T/Verizon→Phone, Progressive→Insurance
  → Auto-add=OFF em todas as rules (existir pra demo, não categorizar silenciosamente)
CONFERIR:
  → Contas reconciliadas? Quando foi a última? (>90 dias = stale)
  → Unreconciled gap (período sem reconciliação)?
  → Rules úteis ou genéricas demais?
AVANÇAR quando: reconciliation e rules verificados
```

### Estação 25: AI FEATURES & INTUIT INTELLIGENCE
```
Rotas: Homepage (AI panel) → /app/business-intelligence → Intuit Assist
VER:
  → browser_snapshot() → verificar presença de AI features
  → Testar Intuit Assist: perguntar "What were my top expenses last month?"
  → Verificar: AI categorization em banking (D04 cross-ref)
  → Financial Summary no Business Feed (D01 cross-ref)
CONFERIR:
  → Intuit Assist responde de forma útil?
  → AI-categorized transactions existem no banking?
  → Smart Match suggestions aparecem?
  → Intuit Intelligence dashboard carrega com dados?
  → KPI scorecard populado?
  → AI-generated insights no Business Feed?
NÃO CORRIGIR: AI features são platform-generated, não podem ser forçadas
SE features indisponíveis: anotar como "AI features not provisioned" com detalhes
AVANÇAR quando: AI features mapeadas (presentes ou ausentes)
```

---

## 5B. TIER 2 — SURFACE SCAN PROTOCOL (20 páginas)

Páginas visitadas rapidamente. Protocolo: carregou? tem dados? placeholder/profanity? Anotar e seguir.
**Regra: surface scan NÃO corrige, só registra.**

### Tabela de páginas

| # | Página | Rota | Verifica |
|---|--------|------|----------|
| S1 | Estimates | `/app/estimates` | Quantidade, nomes realistas |
| S2 | Sales Orders | `/app/salesorders` | Existe? Tem dados? |
| S3 | Purchase Orders | `/app/purchaseorders` | Existe? Tem dados? |
| S4 | Expenses | `/app/expenses` | Tem expenses registradas? |
| S5 | Recurring Transactions | `/app/recurring` | Recorrências configuradas? |
| S6 | Fixed Assets | `/app/fixedassets` | Módulo existe? Tem assets? |
| S7 | Revenue Recognition | `/app/revenuerecognition` | Módulo existe? (Advanced) |
| S8 | Time Tracking | `/app/time` | Módulo existe? Tem entries? |
| S9 | Sales Tax | `/app/salestax` | Configurado? Filing status? |
| S10 | Reconcile | `/app/reconcile` | Contas reconciliadas? Pendentes? |
| S11 | Bank Rules | Via `/app/banking` → Rules tab | Quantas rules ativas? |
| S12 | Receipts | `/app/receipts` | Tem receipts capturados? |
| S13 | Budgets | `/app/budgets` | Tem budgets? (Construction) |
| S14 | Dimensions/Classes | `/app/class` | Quantas ativas? Nomes? |
| S15 | Workflows | `/app/workflows` | Tem automações configuradas? |
| S16 | Payment Links | `/app/paymentlinks` | Feature existe? |
| S17 | Subscriptions | `/app/subscriptions` | Feature existe? Tem dados? |
| S18 | My Accountant | `/app/myaccountant` | Status do convite? |
| S19 | Audit Log | `/app/auditlog` | Acessível? Tem atividade? |
| S20 | Lending | Via menu | Feature visível? |

### Protocolo por página (~30s cada, ~10 min total)

```
Para cada página TIER 2:
1. browser_navigate(rota)
2. browser_wait_for(time=3)
3. browser_evaluate(() => {
     const text = document.body.innerText;
     const lines = text.split('\n').filter(l => l.trim().length > 0);
     return {
       title: document.title,
       lineCount: lines.length,
       first20: lines.slice(0, 20),
       hasData: lines.length > 10,
       hasPlaceholder: /\b(TBX|Lorem|Sample|Foo|Bar|TODO)\b/i.test(text),
       has404: /not found|404|page doesn't exist/i.test(text)
     };
   })
4. Anotar: ✓ (tem dados) | ○ (vazio) | ✗ (404) | ⚠ (conteúdo suspeito)
5. Próxima página (sem parar para corrigir no surface scan)
```

### Símbolos de status

| Símbolo | Significado | Ação |
|---------|-------------|------|
| ✓ | Página carregou com dados | Nenhuma |
| ○ | Página carregou mas vazia | Anotar no resumo final |
| ✗ | 404 ou page not found | Anotar como BLOCKED |
| ⚠ | Placeholder/profanity detectado | Flag como P2 no resumo |

---

## 5C. TIER 3 — CONDITIONAL CHECKS (14 checks)

Checks executados **somente se o ambiente suportar**. Cada um com condição de ativação.

### Multi-Entity (condição: ambiente tem IES multi-entity)

| # | Feature | Rota | O que verifica |
|---|---------|------|----------------|
| C1 | Consolidated View | Entity switcher → Consolidated | Acesso funcional, dados aparecem |
| C2 | Shared COA | `/app/sharedcoa` | Contas compartilhadas entre entities |
| C3 | IC Transactions | `/app/multi-entity-transactions?jobId=accounting` | Transações intercompany existem |
| C4 | Consolidated Reports | `/app/reportlist` no Consolidated | Reports consolidados com dados |

### Construction (condição: dataset = construction)

| # | Feature | Rota | O que verifica |
|---|---------|------|----------------|
| C5 | Project Phases | Dentro de `/app/projects` | Phases v2 configurados |
| C6 | Cost Groups | Via Products | Cost groups definidos |
| C7 | AIA Billing | Via Projects | Lien waiver workflow |
| C8 | Certified Payroll | Via Payroll Reports | WH-347 report |

### Non-Profit (condição: dataset = non_profit)

| # | Feature | Rota | O que verifica |
|---|---------|------|----------------|
| C9 | NP Terminology | Verificar labels em cada tela | Donors, Pledges, Programs, Grants |
| C10 | Statement of Activity | Via reportlist | NP P&L equivalent |
| C11 | Dimensions (NP) | `/app/class` | 5+ ativas, nomes adequados |

### Advanced / IES (condição: feature flag ativo)

| # | Feature | Rota | O que verifica |
|---|---------|------|----------------|
| C12 | Customer Hub | `/app/customers` → Leads, Proposals | CRM features avançadas |
| C13 | Intuit Intelligence | Conversational BI em reports | NL queries funcionam |
| C14 | Management Reports | `/app/managementreports` | Reports personalizáveis |

### AI Features (verificar em TODOS os ambientes IES)
```
□ Intuit Assist icon visível no header/homepage
□ Accounting AI: Ready-to-Post no banking
□ Sales Tax AI: Filing Pre-Check
□ PM AI: Budget/estimate suggestions em projects
□ Finance AI: Anomaly detection em reports
□ Solutions Specialist: Widget no Business Feed
□ Conversational BI: NL queries em reports
```

### Winter Release Features (WR-001 a WR-029)
```
Verificar cada WR feature conforme o FEATURE_VALIDATION_CANON.json:
- WR-001 a WR-008: AI Agents
- WR-009 a WR-015: Reporting & BI
- WR-016 a WR-019: Dimensions
- WR-020: Parallel Approval
- WR-021 a WR-023: Migration (Fresh tenant only)
- WR-024 a WR-025: Construction specific
- WR-026 a WR-029: Payroll
```

---

## 6. CONTENT SCAN (Profanity / Placeholder / PII)

Em CADA estação, além do check funcional, rodar content scan visual:

```
BUSCAR NAS TELAS:
  - Profanity: palavrões em EN e PT
  - Placeholder: "TBX", "Test", "Lorem", "Sample", "Foo", "Bar", "TODO"
  - PII: SSN patterns (XXX-XX-XXXX), credit card patterns, emails @test
  - Gaffes culturais: nomes sensíveis, referências políticas, temas controversos
  - Duplicatas: nomes com sufixo numérico (Name2, Name3)

COMO SCANEAR:
  1. browser_snapshot para obter texto da página
  2. Buscar patterns no texto retornado
  3. Se encontrar: flag CRITICAL e registrar localização exata
```

---

## 7. DEMO REALISM AUDIT

Após as 12 estações + surface scan, avaliar realismo geral:

```
CRITÉRIOS (1-10 cada):
  □ Viabilidade financeira (P&L faz sentido?)
  □ Coerência de nomes (clientes, vendors, products fazem sentido para o setor?)
  □ Volume de dados (parece empresa real com história?)
  □ Diversidade de transações (não só 1 tipo de transação)
  □ Banking health (contas conectadas, transações categorizadas)
  □ AR/AP balance (empresa tem receivables E payables?)
  □ Payroll presence (funcionários existem e têm salários?)
  □ Projects richness (projetos com transações, não vazios)
  □ Report quality (reports geram dados úteis, não zerados)
  □ Storytelling potential (dá para contar uma história de negócio convincente?)

SCORE FINAL = média dos 10 critérios
  - 9-10: Demo-ready, sem intervenção
  - 7-8: Demo-viable, correções cosméticas
  - 5-6: Demo-risky, correções necessárias antes
  - 1-4: Demo-blocked, intervenção significativa
```

---

## 8. PROTOCOLO DE FIX INLINE

### 8.1 Corrigir imediatamente (sem perguntar)
```
- Placeholder text (TBX, Test, Lorem, Sample, Foo) → renomear
- Nomes duplicados com sufixo (Name2) → renomear
- Campos vazios em top records (company name, email, address, phone, notes, terms)
- Report período errado → mudar para All Dates
- Nomes genéricos ("Project 1", "Vendor A") → renomear com nome realista do setor
- Customer/vendor sem terms → selecionar Net 30
- Bank transactions uncategorized (top 5-10) → categorizar
```

### 8.2 Corrigir mas informar no resumo final
```
- Criar invoices (afeta Revenue/AR)
- Criar projetos (impacta project tracking)
- Criar bank rules (impacta categorização futura)
- Renomear products/services (pode afetar invoices existentes)
- Ajustar preços de products (impacta margens futuras)
```

### 8.3 NUNCA corrigir (reportar ao usuário como pendência)
```
- UPDATE/INSERT direto no PostgreSQL
- Employee edits bloqueados por 2FA
- Feature flags (dependem da Intuit)
- Company settings (nome legal, EIN, endereço fiscal)
- Payroll data (regulado, não tocar)
- Deletes de qualquer tipo (invoices, bills, transactions)
- P&L negativo por produto com cost invertido (requer decisão humana sobre valores)
```

### 8.4 Nomes realistas por setor

**Tire Shop / Auto (TCO):**
- Customers: Lone Star Fleet Management, Gulf Coast Trucking Inc., Hill Country Auto Group, Brazos Valley Transport, Rio Grande Logistics
- Products: Bridgestone R283 295/75R22.5, Michelin XDA5, Continental ProContact, Goodyear Endurance
- Projects: Fleet Q1 Maintenance, Dealer Retrofit Program, Annual Bus Fleet Overhaul

**Construction (Keystone):**
- Customers: Austin Metro Schools, Barton Creek Developers, Cedar Park Municipal, Round Rock Hospital District
- Products: Concrete Foundation Work, Framing Package, Electrical Rough-In, HVAC Installation
- Projects: Barton Springs Office Complex Phase II, Cedar Park Elementary Expansion

**Non-Profit (NV2):**
- Donors: Johnson Family Foundation, United Way Partnership, Federal CDBG Grant
- Programs: Youth Development, Community Health, Emergency Relief, Workforce Training
- Grants: HUD Housing Assistance FY26, State Workforce Innovation

**Professional Services (NV1):**
- Clients: TechForward Inc., Meridian Health Systems, City of Austin IT Division
- Services: Strategy Consulting, Systems Integration, Change Management, Data Analytics
- Projects: Digital Transformation Phase 2, ERP Implementation

**Manufacturing (NV3):**
- Customers: National Hardware Distributors, HomeDepot Supply Chain, Regional Builders Supply
- Products: Steel Bracket Assembly, Custom Hinge Kit, Industrial Door Frame
- Projects: Q1 Production Run, Custom Order #4521

---

## 9. FORMATO DE OUTPUT

### 9.1 Durante execução (chat) — mínimo
```
Logado em TCO → Apex Tire

--- TIER 1: Deep Stations (25) ---
[1/25] Dashboard ✓
[2/25] P&L ✓ Revenue $5.2M, Net $1.3M (25%)
[3/25] BS ✓ Assets $8.1M, balanced
[4/25] Banking — categorizei 8 transações
[5/25] Customers — enriched top 5 (company name, email, address, notes)
[6/25] Vendors ✓ top 5 completos, AP aging ok
[7/25] Employees ✓ 13 employees, payroll ok
[8/25] Products — renomei 3 placeholders, fixei 1 preço invertido
[9/25] Projects — criei 2 projetos novos
[10/25] Reports ✓ KPI ok, dashboards ok
[11/25] COA ✓ 45 contas, estrutura ok
[12/25] Settings ✓ nome legal, industry, endereço ok
[13/25] Estimates ✓ 15 estimates, 8 converted, progress invoicing active
[14/25] Purchase Orders ✓ 12 POs, 67% linked to bills
[15/25] Recurring ✓ 8 templates, mix of monthly/weekly
[16/25] Fixed Assets ✓ 6 assets, depreciation running
[17/25] RevRec — N/A (feature not provisioned)
[18/25] Time Tracking ✓ 340 entries, 72% billable
[19/25] Sales Tax ✓ configured, 1 agency, no overdue
[20/25] Budgets — criei budget anual from actuals, BvA ok
[21/25] Dimensions ✓ 5 classes used, P&L by Class has data
[22/25] Workflows — criei 3 automations
[23/25] Custom Fields ✓ 4 fields, template with logo
[24/25] Reconciliation — criei 6 bank rules
[25/25] AI Features ✓ Intuit Assist works, Financial Summary present

--- TIER 2: Surface Scan (20 pages) ---
[S1-S20] ✓14 ○4 ✗2 (details below if issues found)

--- TIER 3: Conditional (N applicable) ---
[C1-C14] ✓8 N/A 6

→ Switching to Global Tread...
```

### 9.2 Resumo final (no chat, não em arquivo)
```
SWEEP COMPLETO — TCO (tire_shop)
Conta: quickbooks-testuser-tco-tbxdemo
Duração: ~55 min
Companies: Apex ✓ | Global ✓ | RoadReady ✓ | Consolidated ✓

--- TIER 1: Deep Stations (25/25) ---
CORRIGIDO (17 items):
- 5 customers enriched (company name + email + address)
- 3 products renomeados (placeholder → realista)
- 1 preço invertido corrigido (Lot Clearing: $111→$866 sell, $866→$111 cost)
- 8 bank transactions categorizadas
- 2 projetos criados

--- TIER 2: Surface Scan (20 pages) ---
✓14 | ○4 (Estimates, Subscriptions, Lending, Payment Links — sem dados)
✗2 (Fixed Assets 404, Revenue Recognition 404)

--- TIER 3: Conditional (8/14 applicable) ---
✓6 | ⚠2 (Consolidated reports slow, IC txns limited)

PENDENTE (3 items):
- Employee "John Test2" — 2FA bloqueou edit
- Feature WR-012 Calculated Fields — 404 (feature flag OFF)
- P&L consolidated: Global Tread com margem de 2% (baixa para distribuição)

DEMO READINESS: 8/10 — VIABLE
Pode mostrar: Dashboard, P&L, Customers, Projects, Reports, AI Assist
Evitar ao vivo: Employee list (nome ruim), Global Tread P&L detail
```

### 9.3 Arquivo (só se o usuário pedir)
Salvar em `C:\Users\adm_r\Downloads\QBO_SWEEP_{PROJETO}_{DATA}.md` apenas quando solicitado

---

## 10. REGRAS DURAS

```
1. SNAPSHOT ANTES DE SCREENSHOT
   → Sempre usar browser_snapshot primeiro para verificar conteúdo
   → Só usar browser_take_screenshot para evidência visual

2. HOMEPAGE NÃO É EVIDÊNCIA
   → Homepage genérica não prova nenhuma feature específica
   → Cada feature precisa de evidência na tela específica

3. 404 NÃO É N/A
   → 404 significa rota errada ou feature flag OFF
   → Tentar rota alternativa antes de marcar como BLOCKED
   → N/A só para features de documentação ou região indisponível

4. NÃO ENTRAR EM LOOP
   → Se algo falhar 2 vezes: documentar e avançar
   → Não ficar tentando a mesma ação indefinidamente

5. VERIFICAR COMPANY NO HEADER
   → Após qualquer switch de empresa, confirmar no header
   → Não assumir que o switch funcionou sem verificar

6. REPORTS SEMPRE VIA LISTA
   → Usar /app/reportlist e clicar no report desejado
   → Nunca usar URL direto do report (404 no IES)

7. ESPERAR PÁGINAS PESADAS
   → QBO leva 3-5s para carregar páginas de reports
   → Aguardar antes de concluir que está vazio/falhou

8. NÃO ECOAR SEGREDOS
   → NUNCA imprimir password, TOTP seed ou código no chat
   → NUNCA incluir credenciais em relatórios ou screenshots

9. RESPEITAR LAYERS.md
   → Verificar camada antes de editar qualquer arquivo do projeto
   → Camada LOCKED = não alterar sem autorização

10. CONTEXTO É REI
    → Feature de Construction validada em tenant NP = INVÁLIDA
    → Feature de NP validada em tenant TCO = INVÁLIDA
    → Sempre confirmar que o contexto é correto para a feature
```

---

## 11. EXECUÇÃO POR DATASET

### TCO (tire_shop) — Sweep completo
```
1. Login → Apex Tire
2. FASE ZERO: Consolidated P&L + BS → mapear contexto
3. Estações 1-12 em Apex (ver-corrigir-avançar)
4. SURFACE SCAN: 20 páginas TIER 2 em Apex (~10 min)
5. Switch → Global Tread → Estações 1, 5, 6, 8 (corrigir inline)
6. Switch → RoadReady → Estações 1, 5, 9 (corrigir inline)
7. Switch → Consolidated View → Estações 2, 3, 10 + CONDITIONAL CHECKS (validar consolidação)
8. Resumo final no chat (formato 3-tier)
```

### CONSTRUCTION — Sweep completo
```
1. Login → Keystone Parent
2. FASE ZERO: Consolidated P&L + BS
3. Estações 1-12 + SURFACE SCAN + CONDITIONAL checks construction (Phases, Budgets, AIA, Certified Payroll)
4. Switch → BlueCraft (main child) → Estações 1, 2, 7
5. Switch → Consolidated → Estações 2, 3 + Conditional C1-C4
6. Resumo final no chat (formato 3-tier)
7. Commitar learnings: `git add knowledge-base/sweep-learnings/ && git commit`
```

### NV2 (non_profit) — Sweep completo
```
1. Login → Parent (Vala NP)
2. FASE ZERO: Statement of Activity + Statement of Financial Position
3. Estações 1-12 com terminologia NP + SURFACE SCAN + Dimensions (/app/class)
4. CONDITIONAL: C9-C11 (NP-specific) + C1-C4 (Multi-Entity)
5. Switch → Rise → Estações 1, 2, 5 (corrigir inline)
6. Switch → Response → Estações 1, 2, 5 (corrigir inline)
7. Resumo final no chat (formato 3-tier)
8. Commitar learnings: `git add knowledge-base/sweep-learnings/ && git commit`
```

### NV1 / NV3 / CANADA — Sweep rápido
```
1. Login → empresa principal
2. FASE ZERO: P&L + BS rápido
3. Estações 1-8 (core financial health, corrigir inline)
4. SURFACE SCAN: 20 páginas TIER 2 (~10 min)
5. Resumo final no chat (formato 3-tier)
6. Commitar learnings: `git add knowledge-base/sweep-learnings/ && git commit`
```

---

## 12. BANCO DE DADOS (VERIFICAÇÃO COMPLEMENTAR)

Quando a UI não é suficiente para diagnosticar, usar PostgreSQL:

```
Host: tbx-postgres-staging.internal
Port: 5433
User: unstable
Password: FaMVkKIM0IcsXHCW_323pJync_ofrBsi
Database: unstable
```

### Queries úteis:
```sql
-- Encontrar dataset_id de um projeto
SELECT DISTINCT dataset_id FROM quickbooks_invoices
WHERE company_type = 'parent' LIMIT 1;

-- P&L rápido
SELECT company_type,
  SUM(CASE WHEN account_type = 'Income' THEN amount ELSE 0 END) as revenue,
  SUM(CASE WHEN account_type = 'Cost of Goods Sold' THEN amount ELSE 0 END) as cogs,
  SUM(CASE WHEN account_type = 'Expense' THEN amount ELSE 0 END) as expenses
FROM quickbooks_journal_entries
WHERE dataset_id = '{ID}'
GROUP BY company_type;

-- Produto com custo invertido
SELECT name, price_rate, product_cost
FROM quickbooks_product_services
WHERE dataset_id = '{ID}' AND product_cost > price_rate AND price_rate > 0;

-- Contagem de registros por tabela
SELECT 'customers' as tbl, COUNT(*) FROM quickbooks_customers WHERE dataset_id = '{ID}'
UNION ALL
SELECT 'vendors', COUNT(*) FROM quickbooks_vendors WHERE dataset_id = '{ID}'
UNION ALL
SELECT 'invoices', COUNT(*) FROM quickbooks_invoices WHERE dataset_id = '{ID}'
UNION ALL
SELECT 'bills', COUNT(*) FROM quickbooks_bills WHERE dataset_id = '{ID}';
```

### Regra: DB é diagnóstico, não evidência
→ Usar DB para entender o problema
→ A prova real é sempre pela UI
→ Não fazer UPDATE/INSERT sem autorização explícita

---

## 13. NARRATIVA DE DEMO POR AMBIENTE

### TCO — "Multi-Location Tire & Auto Empire"
> "Apex Tire manages 4 locations across Texas. See how the parent company tracks revenue across all subsidiaries, manages fleet contracts with enterprise customers, and consolidates financials in real-time. Global Tread handles wholesale distribution while RoadReady focuses on mobile service — all unified under one enterprise platform."

### Construction — "Growing Construction Company"
> "Keystone Construction manages commercial and residential projects across the region. Track job costs in real-time, manage certified payroll for government contracts, and see how project phases flow from estimate to final billing."

### Non-Profit — "Multi-Entity Nonprofit Organization"
> "Vala Nonprofit manages three affiliated organizations. Track donors and pledges, manage restricted grants, and produce board-ready financial statements — all while maintaining separate books for each entity."

### Professional Services — "Consulting Firm"
> "Summit Consulting tracks billable hours across client engagements, manages project profitability, and allocates resources across the team."

---

## 14. RETROSPECTIVA — APRENDIZADO PÓS-SWEEP

**Após cada sweep, ANTES do resumo final, executar esta rotina de aprendizado.**

### 14.1 O que capturar

```
Para cada sweep, registrar:

1. ROTAS
   - Alguma rota nova que funcionou e não estava documentada?
   - Alguma rota documentada que deu 404 agora?
   - Algum redirect inesperado?
   → Atualizar seção 3 (Rotas QBO Confirmadas) se houver mudança

2. UI CHANGES
   - O QBO mudou algum label, botão ou fluxo desde o último sweep?
   - Algum campo moveu de lugar? (ex: "Notes" mudou de aba)
   - Algum seletor/ref que funcionava antes não funciona mais?
   → Anotar para atualizar as instruções de estação

3. PADRÕES DE ERRO RECORRENTES
   - Qual tipo de erro apareceu mais? (placeholder? campo vazio? preço invertido?)
   - Qual entity/company teve mais problemas?
   - Qual estação demorou mais? Por quê?
   → Ajustar prioridade das próximas estações

4. DADOS DO AMBIENTE
   - Revenue/Net Income atual por entity (snapshot financeiro)
   - Número de customers, vendors, products, invoices, bills
   - Novos records que apareceram desde o último sweep
   → Servem como baseline para detectar anomalias no próximo sweep

5. BLOQUEIOS
   - O que travou e não consegui resolver?
   - Foi 2FA? Feature flag? Permissão? Bug do QBO?
   - Existe workaround que descobri?
   → Registrar para não perder tempo na próxima vez

6. EFICIÊNCIA
   - Quanto tempo levou o sweep total?
   - Quais estações foram skip (nada a corrigir)?
   - Quais estações consumiram mais tempo?
   → Otimizar ordem e profundidade para próximo sweep
```

### 14.2 Onde salvar e COMMITAR

```
ARQUIVO: C:\Users\adm_r\Clients\intuit-boom\knowledge-base\sweep-learnings\{DATASET}_{DATA}.md

REGRA OBRIGATÓRIA: Após salvar o arquivo de learnings, SEMPRE commitar:
  git add knowledge-base/sweep-learnings/{DATASET}_{DATA}.md
  git add PROMPT_CLAUDE_QBO_MASTER.md  (se houve update no prompt)
  git commit -m "sweep({DATASET}): learnings {DATA} — [resumo curto]"

O aprendizado SÓ TEM VALOR se estiver no Git. Arquivo local sem commit = conhecimento perdido.

FORMATO:
# Sweep Learnings — {DATASET} — {DATA}

## Snapshot Financeiro
| Entity | Revenue | Net Income | Margin | Customers | Vendors | Invoices |
...

## Rotas
- NOVA: /app/xxx funciona para yyy
- QUEBROU: /app/zzz agora dá 404 (antes funcionava)

## UI Changes
- Campo "Notes" moveu para aba "Details" em vendor edit
- Botão "Save" agora é "Save and close" por default

## Padrões de Erro
- 8/10 customers sem company name (padrão: dataset tire_shop sempre vem assim)
- Products com nomes em português (dataset construction tem mistura EN/PT)

## Bloqueios
- Employee edit: 2FA toda vez (não tem workaround via UI)
- WR-012 Calculated Fields: feature flag OFF desde Jan/2026

## Eficiência
- Tempo total: 35 min
- Mais demorado: Estação 5 (customers) — 12 min para enrichar 5 records
- Skip: Estação 7 (employees — 2FA bloqueia, não vale tentar)

## Melhorias pro Prompt
- Adicionar: sempre checar se "Terms" dropdown tem opções carregadas antes de selecionar
- Adicionar: vendor edit em IES tem delay de 3s após clicar Edit antes de fields aparecerem
```

### 14.3 Como usar na próxima vez

```
ANTES de iniciar um novo sweep no mesmo dataset:
1. Ler o último arquivo de learnings: knowledge-base/sweep-learnings/{DATASET}_*.md
2. Pegar o snapshot financeiro anterior como baseline
3. Pular estações que são consistentemente skip
4. Aplicar workarounds conhecidos
5. Comparar: Revenue mudou? Novos records apareceram? Algo quebrou?

ISSO CRIA UM CICLO:
  Sweep 1 → aprende rotas, tempos, padrões
  Sweep 2 → mais rápido, foca onde importa
  Sweep 3 → quase automático, só valida e corrige delta
  Sweep N → rotina de 15 min em vez de 45 min
```

### 14.4 Atualizar o PROMPT_MASTER

```
Se o learning revelar algo que muda o prompt:
1. Editar a seção relevante do PROMPT_CLAUDE_QBO_MASTER.md
2. Atualizar o CHANGELOG (seção 15)
3. Commitar com: "fix(sweep): [descrição curta do learning]"

EXEMPLOS de updates:
- Rota /app/dimensions passou a funcionar → atualizar seção 3.3 (rotas que não funcionam)
- Employee 2FA é 100% bloqueio → mudar Estação 7 para "skip by default"
- Novo campo "Secondary Email" em customer edit → adicionar no checklist da Estação 5
```

### 14.5 LEARNING LOG (OBRIGATÓRIO a partir de v7.0)

Cada sweep DEVE gerar um arquivo de log estruturado além do report MD.
Salvar em: `knowledge-base/sweep-learnings/logs/{SHORTCODE}_{DATA}_log.json`

Estrutura do log:
```json
{
  "meta": {
    "account": "shortcode",
    "date": "YYYY-MM-DD",
    "duration_minutes": N,
    "sweep_version": "7.0",
    "profile": "full_sweep",
    "entities_count": N
  },
  "stations": {
    "D01": {
      "status": "PASS|FAIL|FIXED|BLOCKED|SKIPPED",
      "score": 8,
      "time_spent_seconds": N,
      "findings": [
        {
          "id": "D01-F01",
          "text": "descrição do finding",
          "severity": "P1|P2|P3",
          "action": "FIXED|REPORTED|BLOCKED|ACCEPTED",
          "before": "valor antes",
          "after": "valor depois",
          "entity": "nome da entidade"
        }
      ],
      "sub_checks": {
        "D01.1": "PASS",
        "D01.2": "PASS",
        "D01.3": "FAIL — widget P&L não bate com report"
      },
      "notes": "observação livre do auditor"
    }
  },
  "summary": {
    "total_findings": N,
    "p1": N, "p2": N, "p3": N,
    "fixed": N, "blocked": N, "reported": N,
    "coverage": {
      "deep": "25/25",
      "surface": "43/46",
      "conditional": "8/19"
    },
    "overall_score": 7.5,
    "realism_score": 68
  },
  "learnings": [
    {
      "type": "PATTERN|BUG|WORKAROUND|IMPROVEMENT",
      "description": "O que foi aprendido neste sweep",
      "applies_to": "all|construction|tire_shop|non_profit",
      "actionable": true,
      "suggestion": "Como usar esse aprendizado no próximo sweep"
    }
  ],
  "evolution": {
    "new_checks_needed": ["descrição de check que faltou"],
    "checks_that_could_be_improved": ["D02.3 deveria verificar X também"],
    "false_positives": ["D05-F03 era falso positivo porque..."],
    "routes_changed": ["/app/oldroute → /app/newroute"]
  }
}
```

**Regras do Learning Log:**
1. O log é MACHINE-READABLE (JSON) — o report MD é HUMAN-READABLE
2. Todo finding DEVE ter before/after quando foi FIXED
3. Sub_checks devem refletir EXATAMENTE os sub_checks definidos em sweep_checks.py
4. A seção "learnings" captura INSIGHTS que melhoram sweeps futuros
5. A seção "evolution" propõe mudanças concretas ao sistema
6. NÃO incluir credentials no log (password, TOTP)
7. O log é commitado junto com o report no Git

---

## 15. CHANGELOG & VERSIONING

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | 2026-03-05 | Versão inicial — consolidação de todos os prompts existentes |
| 2.0 | 2026-03-05 | Rewrite: modo autônomo ver-corrigir-avançar, login via Playwright, sem screenshots |
| 2.1 | 2026-03-05 | Adicionada seção 14: Retrospectiva e aprendizado pós-sweep com ciclo de melhoria |
| 3.0 | 2026-03-06 | Cobertura total — 12 deep + 20 surface + 14 conditional = 46 checks. Overdue bills check na Estação 6. 50+ rotas mapeadas. |

---

## APÊNDICE A: REALM IDs CONHECIDOS

### TCO (tire_shop)
| Company | Realm ID | Role |
|---------|----------|------|
| Apex Tire & Auto Retail | 9341455130166501 | child |
| Global Tread Distributors | 9341455130196737 | child |
| RoadReady Service Solutions | 9341455130182073 | child |
| Traction Control Outfitters | 9341455130122367 | parent |
| Consolidated View | 9341455649090852 | consolidated |

### Construction (Keystone)
| Company | Realm ID | Role |
|---------|----------|------|
| Keystone Construction (Par.) | 9341454156620895 | parent |
| Keystone Terra | 9341454156620204 | child |
| + 6 more children | Ver TESTBOX_ACCOUNTS.md | child |

### NV2 (Non-Profit)
| Company | Realm ID | Role |
|---------|----------|------|
| Vala NP (Parent) | 9341454156795459 | parent |
| Rise | 9341454156776829 | child |
| Response | 9341454156790557 | child |

### TCO Clone
| Company | Realm ID | Role |
|---------|----------|------|
| Parent | 9341456206681900 | parent |
| Child 1 | 9341456206666028 | child |
| Child 2 | 9341456206667919 | child |
| Child 3 | 9341456206675609 | child |

### Construction Clone
| Company | Realm ID | Role |
|---------|----------|------|
| Parent | 9341456206579132 | parent |
| + 7 children | Ver TESTBOX_ACCOUNTS.md | child |

---

## APÊNDICE B: DATASET IDs

| Dataset | ID |
|---------|-----|
| construction (Keystone) | 321c6fa0-a4ee-4e05-b085-7b4d51473495 |
| tire_shop (TCO) | fab72c98-c38d-4892-a2db-5e5269571082 |
| non_profit (NV2) | 3e1337cc-70ca-4041-bc95-0fe29181bb12 |
| professional_services (NV1) | 58f84612-39db-4621-9703-fb9e1518001a |
| manufacturing (NV3) | b6695ca6-9184-41f3-862e-82a182409617 |
| canada_construction | 2ed5d245-0578-43aa-842b-6e1e28367149 |
