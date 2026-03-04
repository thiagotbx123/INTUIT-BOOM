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
| **IC Account Mapping** | PW | PW | PW | PW | CV only, `/app/ic-accountdefaults` |
| **IC Elimination Accounts** | PW | PW | PW | PW | CV only |
| **Shared COA** | PW | PW | PW | PW | CV only, `/app/sharedcoa` |

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

### Recipe: Copy Sales Order to Invoice/PO
```
Engine: PLAYWRIGHT
Steps:
1. Open Sales Order detail: /app/commerce/orders/view?detailId={ID}&detailType=salesOrder
2. Click "Copy" button (top right, "Duplicate or copy data to another transaction")
3. "Copy options" panel opens on right side
4. Open "Copy to" dropdown → select target: Invoice, Purchase Order, Estimate, etc.
   (15 options: Bill, Check, CC Credit, Credit Memo, Delayed Charge/Credit, Estimate,
    Expense, Invoice, Journal Entry, PO, Refund Receipt, Sales Order, Sales Receipt, Vendor Credit)
5. Click "Copy" button
6. New transaction form opens pre-populated with SO data
Note: This is "Copy" not "Convert" - original SO remains unchanged
Note: For SO→Invoice, a "Suggested transactions" panel shows linked Estimates with "Add" buttons
Note: Linked transactions visible via "Linked transactions (N)" button at top of SO detail
```

### Recipe: View/Edit IC Account Mapping
```
Engine: PLAYWRIGHT
URL: /app/ic-accountdefaults (CV ONLY)
Access: CV Homepage → SHORTCUTS section → "Intercompany account mapping"
Steps:
1. Login to QBO
2. Switch to Consolidated View (company switcher in header)
3. On CV Homepage, click "Intercompany account mapping" in SHORTCUTS section
4. Dialog opens showing company pairs (Parent↔Child)
5. Click expand arrow (>) on a pair to see 4 account fields:
   - Due to company 2 → Due from company 1
   - Due from company 2 → Due to company 1
6. Click combobox to change account (typeahead search)
7. Click "Done" to save, "Cancel" to discard
WARNING: DO NOT use Settings → "Switch company" - it causes logout!
WARNING: Use header company switcher dropdown only for entity switching
```

### Recipe: Evidence Check (full investigation + evidence + response)
```
Engine: PLAYWRIGHT
Trigger: "Evidence check: {problem description} no/na {entity}"
Example: "Evidence check: cliente não encontra item receipt na Terra"

Steps:
  1. LOGIN: Use QBO_CREDENTIALS.json → email + password + TOTP
  2. NAVIGATE: Switch to correct entity (multiEntitySwitchCompany?companyId={cid})
  3. INVESTIGATE: Go to feature URL, verify settings, check data exists
  4. SCREENSHOT: Capture evidence in logical sequence:
     - Settings proof (feature is enabled)
     - List/overview (data exists)
     - Detail view (richest example, e.g. with linked PO)
     - Additional details (standalone, edge cases)
  5. CONSOLIDATE: Combine into multi-page PDF (1 page per screenshot, navigable)
     Output: EvidencePack/{feature_snake_case}_evidence.pdf
     Method: PIL Image.save(pdf, "PDF", resolution=150, save_all=True, append_images=[...])
  6. RESPOND: Draft response for whoever needs it (team, client, etc.)
     Tone: natural, humble, concise, basic English

Naming: evidence_{nn}_{description}.png → {feature}_evidence.pdf
Reference: EVIDENCE_COLLECTION_PLAYBOOK.md (full pipeline details)
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
| 2026-02-19 | Evidence Check: Item Receipt Terra | PLAYWRIGHT | VALIDATED (3 receipts found) | Yes - Evidence Check recipe |
| 2026-02-19 | Evidence Check: AIA Billing Terra | PLAYWRIGHT | VALIDATED (Progress Invoicing ON, estimate→invoice with % per line) | No (same recipe) |
| 2026-02-19 | Evidence Check: Sales Orders Terra | PLAYWRIGHT | VALIDATED (4 SOs, Copy→Invoice/PO/Estimate, Linked Transactions popover) | Yes - SO Copy recipe |
| 2026-02-23 | IC Account Mapping: View/Investigate | PLAYWRIGHT | 2 pairs found (Parent↔BlueCraft, Parent↔Terra), all accounts mapped | Yes - IC Mapping recipe |
| 2026-02-23 | Shared COA: Add Terra to account 2030 | PLAYWRIGHT | SUCCESS - Terra added to "Due to Keystone BlueCraft" shared account | No |
| 2026-02-23 | Calculated Field: Balance Sheet | PLAYWRIGHT | CREATED - custom calculated field visible in report | No |
| 2026-02-23 | Bank Rules: Create 6 rules + auto-add | PLAYWRIGHT | 6 rules created, ~120 txns auto-posted, Ready to Post still 0 | No |
| 2026-02-23 | Ready to Post: Final validation | PLAYWRIGHT | CONFIRMED IMPOSSIBLE on TestBox - 4 approaches tested, all 0 | No |

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
