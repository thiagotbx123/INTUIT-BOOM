# QBO Operation Router

> Maps every QBO operation to the right engine.
> Updated incrementally as we learn from each job.
> Last updated: 2026-02-13

---

## ENGINE DEFINITIONS

| Engine | When to Use | Speed | Reliability |
|--------|-------------|-------|-------------|
| **API** (python-quickbooks) | Standard CRUD on supported entities | Fast (< 1s per op) | High (if token valid) |
| **MCP** (Intuit MCP Server) | Same as API, via Claude Desktop | Fast | High (needs valid tokens in config) |
| **PLAYWRIGHT** (browser automation) | Everything API can't do | Slow (30-60s per op) | Medium (UI changes can break) |

---

## ENTITY ROUTING TABLE

### Full CRUD via API (python-quickbooks + MCP)

| Entity | Create | Read | Update | Delete | Query | Notes |
|--------|--------|------|--------|--------|-------|-------|
| Account | API | API | API | API | API | ChartOfAccounts |
| Bill | API | API | API | API | API | AP |
| BillPayment | API | API | API | API | API | AP |
| Customer | API | API | API | API | API | |
| Employee | API | API | API | - | API | No delete via API |
| Estimate | API | API | API | API | API | |
| Invoice | API | API | API | API | API | |
| Item | API | API | API | - | API | Products/Services |
| JournalEntry | API | API | API | API | API | |
| Purchase | API | API | API | API | API | Expenses/Checks |
| Vendor | API | API | API | API | API | |

### API-capable but NOT in MCP server (python-quickbooks only)

| Entity | Create | Read | Update | Delete | Query | Notes |
|--------|--------|------|--------|--------|-------|-------|
| Payment | API | API | API | API | API | Customer payments (AR) |
| Deposit | API | API | API | API | API | Bank deposits |
| SalesReceipt | API | API | API | API | API | |
| CreditMemo | API | API | API | API | API | |
| RefundReceipt | API | API | API | API | API | |
| Transfer | API | API | API | API | API | Bank-to-bank |
| VendorCredit | API | API | API | API | API | |
| PurchaseOrder | API | API | API | API | API | |
| TimeActivity | API | API | API | API | API | Time entries |
| Attachable | API | API | API | API | API | File attachments |
| Class | API | API | API | - | API | Tracking categories |
| Department | API | API | API | - | API | Locations |
| TaxCode | - | API | - | - | API | Read-only |
| TaxRate | - | API | - | - | API | Read-only |
| Term | API | API | API | - | API | Payment terms |
| Preferences | - | API | API | - | - | Company settings (limited) |
| CompanyInfo | - | API | API | - | - | Company details |

### Reports via API (read-only)

| Report | Engine | Endpoint |
|--------|--------|----------|
| ProfitAndLoss | API | `/reports/ProfitAndLoss` |
| BalanceSheet | API | `/reports/BalanceSheet` |
| CashFlow | API | `/reports/CashFlow` |
| TrialBalance | API | `/reports/TrialBalance` |
| GeneralLedger | API | `/reports/GeneralLedger` |
| ARAgingSummary | API | `/reports/AgedReceivables` |
| APAgingSummary | API | `/reports/AgedPayables` |
| CustomerBalance | API | `/reports/CustomerBalance` |
| VendorBalance | API | `/reports/VendorBalance` |
| Custom Reports | PLAYWRIGHT | IES-specific, no API |

### Playwright ONLY (no API available)

| Entity/Feature | Create | Read | Update | Delete | Notes |
|----------------|--------|------|--------|--------|-------|
| **Project** | PW | PW | PW | PW | Premium API exists (GraphQL) but requires Silver+ tier |
| **Budget** | PW | PW | PW | PW | ZERO API. Browser only |
| **Consolidated View** | - | PW | - | - | Switch entity + view consolidated reports |
| **Settings** | - | PW | PW | - | Most settings have no API |
| **Workflows** | PW | PW | PW | PW | Automation rules |
| **Banking Rules** | PW | PW | PW | PW | |
| **Recurring Transactions** | PW | PW | PW | PW | Templates for auto-creation |
| **Custom Fields** | PW | PW | PW | PW | IES-specific |
| **Dimensions** | PW | PW | PW | PW | IES multi-entity |
| **Sales Orders** | PW | PW | PW | PW | IES-specific |
| **Payroll** | PW | PW | PW | - | Separate API (not QBO REST) |
| **HR/Mineral** | PW | PW | - | - | Third-party integration |

---

## OPERATION RECIPES

### Recipe: Create a Project
```
Engine: PLAYWRIGHT
Steps:
1. Login (use QBO_CREDENTIALS.json)
2. Navigate to /app/projects
3. Click "New project"
4. Fill form (name, customer, status)
5. Save
Evidence: Screenshot
```

### Recipe: Create an Invoice
```
Engine: API (python-quickbooks)
Code:
  from quickbooks import QuickBooks
  from quickbooks.objects.invoice import Invoice
  from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail

  invoice = Invoice()
  invoice.CustomerRef = {"value": customer_id}
  line = SalesItemLine()
  line.Amount = amount
  line.SalesItemLineDetail = SalesItemLineDetail()
  line.SalesItemLineDetail.ItemRef = {"value": item_id}
  invoice.Line = [line]
  invoice.save(qb=client)
```

### Recipe: Create a Budget inside a Project
```
Engine: PLAYWRIGHT
Steps:
1. Login
2. Navigate to /app/projects
3. Open project
4. Click "Budget" tab
5. Fill budget amounts
6. Save
Note: Budget v3 may work even when expected to be blocked by feature flag
```

### Recipe: Generate P&L Report
```
Engine: API (python-quickbooks)
Code:
  from quickbooks import QuickBooks
  report = client.get_report('ProfitAndLoss', params={
      'start_date': '2025-01-01',
      'end_date': '2025-12-31'
  })
```

### Recipe: Switch Company (Multi-Entity)
```
Engine: PLAYWRIGHT
URL: https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={CID}
Steps:
1. Navigate to URL
2. Wait 30-45s for QBO SPA to load
3. Verify entity name in header
```

### Recipe: Batch Create Customers
```
Engine: API (python-quickbooks)
Code:
  from quickbooks.batch import batch_create
  customers = [Customer(...), Customer(...), ...]
  # Up to 25 per batch call
  results = batch_create(customers, qb=client)
```

---

## AUTH FLOW (for Claude)

```
START:
  1. Ask user: "Qual email de acesso QBO?"
  2. Read QBO_CREDENTIALS.json
  3. Lookup email in accounts

  IF FOUND:
    4a. For PLAYWRIGHT: use email + password + TOTP to login via browser
    4b. For API: check if refresh_token exists and is valid
        - If valid: use it
        - If expired/missing: run OAuth flow via qb-oauth-manager
    5. Log success, update last_successful_login

  IF NOT FOUND:
    4. Ask user: "Nao encontrei esse email. Pode me passar: senha, TOTP secret, e empresas?"
    5. Add new entry to QBO_CREDENTIALS.json
    6. Proceed with auth

  IF AUTH FAILS:
    7. Ask user: "Login falhou. A senha ou TOTP mudou?"
    8. If user provides new credentials: UPDATE QBO_CREDENTIALS.json
    9. Retry
```

---

## LEARNING LOG

> Every time we execute a new operation, document it here.

| Date | Operation | Engine | Result | Recipe Added? |
|------|-----------|--------|--------|---------------|
| 2026-02-13 | Foundation created | - | - | Initial recipes |
| | | | | |

---

## PYTHON-QUICKBOOKS SETUP

```python
from quickbooks import QuickBooks
from intuitlib.client import AuthClient

auth_client = AuthClient(
    client_id='ABBCXphnRbl3SISytJ1KBYhqqasfE3HGUd9FBn9SISUOQdiE6V',
    client_secret='2fMdCRacJa6EyrJNu8SjZPtVHdeRqZbxHvZE4vrn',
    environment='production',
    redirect_uri='http://localhost:8000/callback',
)
auth_client.refresh(refresh_token=REFRESH_TOKEN)

client = QuickBooks(
    auth_client=auth_client,
    refresh_token=REFRESH_TOKEN,
    company_id=REALM_ID,
)

# Now use client for any operation
from quickbooks.objects.customer import Customer
customers = Customer.all(qb=client)
```

---

## SUPPORTED ENTITIES (python-quickbooks 0.9.12)

Full list: Account, Attachable, Bill, BillPayment, Budget, Class, CompanyInfo, CreditMemo,
Customer, CustomerType, Department, Deposit, Employee, Estimate, ExchangeRate, Invoice,
Item, JournalEntry, Payment, PaymentMethod, Preferences, Purchase, PurchaseOrder,
RecurringTransaction, RefundReceipt, SalesReceipt, TaxCode, TaxRate, Term, TimeActivity,
Transfer, Vendor, VendorCredit

**Total: 34 entities** (vs 11 in MCP server)
