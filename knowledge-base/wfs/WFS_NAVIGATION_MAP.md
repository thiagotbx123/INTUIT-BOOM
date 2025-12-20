# WFS Navigation Map - Mapa de Navegacao Autonoma

**Data:** 2025-12-19
**Objetivo:** Permitir navegacao autonoma completa nos sistemas QBO e Mineral
**Uso:** Claude Code + Playwright para automacao

---

## 1. QuickBooks Online - Rotas Principais

### Base URL
```
https://qbo.intuit.com
```

### Rotas Core (22 testadas, 100% funcionando)

| Rota | Modulo | Descricao |
|------|--------|-----------|
| `/app/homepage` | Dashboard | Pagina inicial |
| `/app/banking` | Banking | Transacoes bancarias |
| `/app/reconcile` | Banking | Reconciliacao |
| `/app/customers` | Sales | Lista de clientes |
| `/app/vendors` | Expenses | Lista de fornecedores |
| `/app/invoices` | Sales | Faturas |
| `/app/estimates` | Sales | Orcamentos |
| `/app/expenses` | Expenses | Despesas |
| `/app/bills` | Expenses | Contas a pagar |
| `/app/payroll` | Payroll | Folha de pagamento |
| `/app/employees` | Team | Funcionarios |
| `/app/contractors` | Payroll | Contratados |
| `/app/timetracking` | Time | Controle de tempo |
| `/app/projects` | Projects | Projetos |
| `/app/items` | Products | Produtos e servicos |
| `/app/inventory` | Inventory | Inventario |
| `/app/reportlist` | Reports | Lista de relatorios |
| `/app/chartofaccounts` | Accounting | Plano de contas |
| `/app/journal` | Accounting | Lancamentos |
| `/app/settings` | Settings | Configuracoes |
| `/app/taxes` | Taxes | Impostos |
| `/app/hr` | HR | HR Advisor (Mineral) |

---

## 2. Rotas WFS-Especificas (25 testadas, 100% funcionando)

### Payroll Sub-Routes
| Rota | Descricao |
|------|-----------|
| `/app/payroll/overview` | Visao geral payroll |
| `/app/payroll/employees` | Employees no payroll |
| `/app/payroll/contractors` | Contractors |
| `/app/payroll/taxes` | Impostos payroll |
| `/app/payroll/benefits` | Beneficios |
| `/app/payroll/settings` | Config payroll |

### Team/Employees
| Rota | Descricao |
|------|-----------|
| `/app/employees/list` | Lista de employees |
| `/app/employees/directory` | Diretorio |
| `/app/employees/orgchart` | Organograma |

### Time
| Rota | Descricao |
|------|-----------|
| `/app/time` | Time module |
| `/app/timeactivity` | Time activities |
| `/app/timesheets` | Timesheets |

### HR Advisor
| Rota | Descricao |
|------|-----------|
| `/app/hr` | HR Advisor main |
| `/app/hr/advisor` | HR Advisor |
| `/app/hradvisor` | HR Advisor (alias) |

### Reports WFS
| Rota | Descricao |
|------|-----------|
| `/app/reports/payroll` | Relatorios payroll |
| `/app/reports/employees` | Relatorios employees |
| `/app/reports/time` | Relatorios time |

### Settings
| Rota | Descricao |
|------|-----------|
| `/app/settings/payroll` | Config payroll |
| `/app/settings/company` | Config empresa |
| `/app/settings/users` | Config usuarios |
| `/app/settings/advanced` | Config avancadas |

### Create Forms
| Rota | Descricao |
|------|-----------|
| `/app/invoice` | Criar invoice |
| `/app/expense` | Criar expense |
| `/app/bill` | Criar bill |
| `/app/employee` | Criar employee |

---

## 3. Mineral HR - Estrutura

### Base URL
```
https://apps.trustmineral.com
```

### Acesso via QBO
```
QBO: /app/hr > "Go to Mineral" > nova aba
```

### Rotas Mineral
| Rota | Modulo | Descricao |
|------|--------|-----------|
| `/dashboard` | Dashboard | Pagina inicial |
| `/hr-compliance` | Compliance | HR Compliance |
| `/hr-compliance/law-alerts/*` | Alerts | Alertas de leis |
| `/company-policies` | Policies | Politicas |
| `/safety` | Safety | Seguranca |
| `/training` | Training | Treinamentos |
| `/hr-tools` | Tools | Ferramentas HR |
| `/templates` | Templates | Modelos |
| `/resources` | Resources | Recursos |
| `/community` | Community | Comunidade |
| `/my-cases` | Cases | Meus casos |
| `/todo` | Todo | Lista de tarefas |
| `/featured-content/*` | Content | Conteudo destaque |

---

## 4. QuickBooks Online API

### Base URLs
```
Production: https://quickbooks.api.intuit.com
Sandbox: https://sandbox-quickbooks.api.intuit.com
GraphQL: https://qb.api.intuit.com/graphql
```

### Endpoints Principais

#### Accounting API (REST)
| Endpoint | Metodo | Descricao |
|----------|--------|-----------|
| `/v3/company/{realmId}/account` | GET/POST | Contas |
| `/v3/company/{realmId}/customer` | GET/POST | Clientes |
| `/v3/company/{realmId}/vendor` | GET/POST | Fornecedores |
| `/v3/company/{realmId}/employee` | GET/POST | Funcionarios |
| `/v3/company/{realmId}/invoice` | GET/POST | Faturas |
| `/v3/company/{realmId}/bill` | GET/POST | Bills |
| `/v3/company/{realmId}/item` | GET/POST | Itens |
| `/v3/company/{realmId}/timeactivity` | GET/POST | Time Activities |

#### Time API (Premium)
| Endpoint | Metodo | Descricao |
|----------|--------|-----------|
| `/v3/company/{realmId}/timeactivity` | POST | Criar time entry |
| `/timeactivity/{id}/approve` | POST | Aprovar time |
| `/timeactivity/{id}/project` | POST | Associar a projeto |

#### Payroll API (GraphQL)
```graphql
endpoint: https://qb.api.intuit.com/graphql
```

### OAuth 2.0
| Parametro | Valor |
|-----------|-------|
| Auth URL | https://appcenter.intuit.com/connect/oauth2 |
| Token URL | https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer |
| Access Token Life | 1 hora |
| Refresh Token Life | 100 dias |
| Scope | com.intuit.quickbooks.accounting |

### Rate Limits
| Limite | Valor |
|--------|-------|
| Requests/minuto | 500 |
| Requests/segundo | 10 |
| Batch operations | 30 max |

---

## 5. Metodo de Navegacao Autonoma

### Script Base (Python + Playwright)
```python
from playwright.sync_api import sync_playwright

def connect_qbo():
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
    page = browser.contexts[0].pages[0]
    return pw, browser, page

def navigate_qbo(page, route):
    url = f'https://qbo.intuit.com{route}'
    page.goto(url, timeout=30000, wait_until='domcontentloaded')
    return page.url

def navigate_mineral(page):
    # Ir para HR Advisor
    page.goto('https://qbo.intuit.com/app/hr')
    # Clicar em Go to Mineral
    page.locator('text=Go to Mineral').click()
    # Aguardar nova aba
    time.sleep(5)
```

### Funcoes de Exploracao
```python
def explore_page(page):
    # Extrair todos os links
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a'))
            .map(a => ({text: a.innerText, href: a.href}))
            .filter(l => l.href && l.text);
    }''')
    return links

def capture_module(page, route, output_dir):
    navigate_qbo(page, route)
    time.sleep(3)
    page.screenshot(path=f'{output_dir}/{route.replace("/", "_")}.png')
    return explore_page(page)
```

---

## 6. Ambientes Disponiveis

### GoQuick Alpha Retail
| Atributo | Valor |
|----------|-------|
| Company ID | (verificar no QBO) |
| Mineral Access | **SIM** |
| Payroll | Ativo |
| Employees | 3 |
| HR Advisor | Habilitado |

### Keystone Construction Canada
| Atributo | Valor |
|----------|-------|
| Company ID | (verificar no QBO) |
| Mineral Access | NAO |
| Payroll | Ativo |
| Employees | 7+ |
| PTO Tracking | Visivel |
| Celebrations | Visivel |

---

## 7. Checklist de Navegacao

### QBO
- [ ] Login via Chrome CDP (porta 9222)
- [ ] Verificar empresa atual no header
- [ ] Navegar para modulo desejado via rota
- [ ] Capturar screenshots se necessario
- [ ] Extrair dados via JavaScript

### Mineral
- [ ] Acessar QBO primeiro
- [ ] Ir para /app/hr
- [ ] Clicar "Go to Mineral"
- [ ] Aguardar nova aba
- [ ] Navegar por menu ou URLs diretas

---

## 8. Links de Referencia

### Documentacao
- [QBO API Docs](https://developer.intuit.com/app/developer/qbo/docs/develop)
- [Payroll API](https://developer.intuit.com/app/developer/qbo/docs/workflows/integrate-with-payroll-api)
- [Time API](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/timeactivity)
- [Employee API](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/employee)

### Mineral
- [Mineral Platform](https://trustmineral.com/)
- [Mitratech](https://mitratech.com/products/mineral/)

---

Ultima atualizacao: 2025-12-19 13:30
