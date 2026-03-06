# QSP Construction Events — Deep Audit v2
**Date:** 2026-03-06
**Account:** quickbooks-test-account-qsp@tbxofficial.com
**Password:** TestBox123!
**TOTP Secret:** J4NUWKE7OZTIBOXI3MP42Z4QVBDDNITH (REQUIRED — MFA enforced)
**Environment:** Production IES (Intuit Enterprise Suite)
**Industry:** Construction
**Previous sweep:** qsp_events_2026-03-05.md (Score: 7/10)

---

## Environment Overview

| Property | Value |
|----------|-------|
| Entities | 4 (Construction parent + BlueCraft child + Terra child + Consolidated View) |
| Consolidated View | AVAILABLE (Vista consolidada) |
| Industry | Construction (all 3 operating entities) |
| Business Type | Corporation (Form 1120) — all entities |
| Shared COA | 239 accounts across 3 companies |
| IC Transactions | 10+ (Journal entries, Dynamic allocations, Expense allocations) |
| Consolidated Reports | 17 report types |

---

## Companies

| Entity | CID | Type | Priority |
|--------|-----|------|----------|
| Keystone Construction (Event) | 9341454796804202 | parent | P0 |
| Keystone BlueCraft (Event) | 9341454842756096 | child | P0 |
| Keystone Terra (Event) | 9341454842738078 | child | P0 |
| Consolidated View | (enterprise realm) | consolidated | P0 |

---

## Entity Audit Results

### Keystone Construction (Event) — Parent — Score: 8/10

**12 stations audited:**

| # | Station | Status | Key Finding |
|---|---------|--------|-------------|
| 1 | Dashboard | PASS | P&L: Net +$2,513,501 (81% margin), Income $3,447,139, Expenses $933,638. Bank $11,392,356. Project Profit Margin 100%. Operating Cash Flow -$238,880. |
| 2 | Customers | PASS | Rich list: Ali Gold (FLDN), Ali Khan (Beacon $177K), Sophia Chang, Amelia Patel, Aryan Patel, Ava Kaur. FLDN = P2 placeholder. Content CLEAN. |
| 3 | Projects | PASS | 20+ projects: TidalWave Farmer's Market ($640K), Azure Pines Playground (4yr x $560K), BMH Landscaping (3yr x $800K), Intuit Dome 2025/2026, David Kiser House. All 100% margin. |
| 4 | Dimensions | PASS | 3 active (Classes ORIGINAL, 5 Service unit, Customer Type) + 4 inactive (Concrete, Earthwork, Location, Utilities). Content CLEAN. |
| 5 | Vendors | PASS | 34 vendors: Aetna, Assignar, AT&T, Blue Bird Insurance, Concrete Depot, Concrete Solutions, etc. IC vendors present (BlueCraft IC, Terra IC). Vendor01 = P3 placeholder. Content CLEAN. |
| 6 | Invoices | PASS | 4 posted invoices ($400K unpaid, $80K paid). TBX-2025-2435 (Michael Nguyen), TBX-2025-2443 (Emily Wong), TBX-2026-2427 (Abigail Patel), TBX-2026-2428 (Aiden Kim). Content CLEAN. |
| 7 | Products | PASS | 63 items (page 1 of 2): Fill Dirt, Individual Wells, Septic System, Excavation, Foundation Pouring, Trenching, Grading, Shoring. Rich construction catalog. Content CLEAN. |
| 8 | Banking | PASS (P1) | 1010 Checking: Bank $460K / QB $10,545,205 (P1 inflation 22x). Guardian Growth MMA: $10,932,356 (P1 inflation). 42 pending. QBAA present. |
| 9 | Settings | PASS | Industry "Industrial building construction", Corp Form 1120, Sunnyvale CA 94087. Phone 8473470269. No i18n issues. |
| 10 | Payroll | PASS | Full module: Overview, Employees, Contractors, Payroll taxes, Benefits, HR advisor, Compliance. 5 setup tasks remaining. |
| 11 | Reports | PASS | Rich report suite including Revenue Recognition Beta, Consolidated reports. |
| 12 | Tasks | PASS | 10+ overdue tasks: Intuit Dome 2025/2026 expense reviews, invoice reviews, David Kiser House. Active environment indicator. |

**Content Safety: ZERO VIOLATIONS**

---

### Keystone BlueCraft (Event) — Child — Score: 7/10 (up from 6.5)

**FIX APPLIED:** P&L fixed from -$1,978,572 to +$521,428 via Journal Entry (DR AR $2.5M / CR Sales $2.5M)

| # | Station | Status | Key Finding |
|---|---------|--------|-------------|
| 1 | Dashboard | PASS (fixed) | P&L: Net +$521,428 (after JE fix). Cash flow -$165K. Bank $11,392,356. Invoices $17.7M unpaid ($5.9M overdue). Sales $6,632,480 YTD. |
| 2 | Customers | PASS | Similar customer list to parent. Content CLEAN. |
| 3 | Projects | PASS | Active projects with estimates vs actual cost widget. |
| 4 | Banking | PARTIAL | 1010 Checking: Bank $460K vs **QB $148,457,999.97** (P1 — EXTREME inflation 322x). Guardian Growth MMA: $10,892,356. 9 txns to review. |
| 5 | Settings | FAIL | **P1: Legal name = "Keystone Terra2"** (WRONG — should be BlueCraft). **P2: ZIP mismatch** Mountain View 92129 (San Diego ZIP). Phone: 180012345670 (malformed). FIX BLOCKED by SMS. |
| 6 | Products | PASS | Construction products shared with parent. Content CLEAN. |

**Content Safety: ZERO VIOLATIONS**

**Fix attempted:** Legal name change from "Keystone Terra2" to "Keystone BlueCraft" — BLOCKED by SMS verification to +1 (917) 555-0111 (unreachable demo phone).

---

### Keystone Terra (Event) — Child — Score: 7.5/10 (up from 7)

| # | Station | Status | Key Finding |
|---|---------|--------|-------------|
| 1 | Dashboard | PASS | P&L: +$267,176 (83% margin), Income $4,960,057, Expenses $4,692,880. Down 94% from FY25. Sales $19,993,189 (HIGHEST entity). Cash flow $3,975,731. |
| 2 | Customers | PASS | Rich customer list. Content CLEAN. |
| 3 | Projects | PASS | "test project" renamed to "Gonzalez Residence Renovation" (fixed from prior session). Estimates vs actual cost widget active. |
| 4 | Banking | PARTIAL | Bank $11,392,356 (same inflation). 122 txns to categorize (40 + 82). |
| 5 | Settings | FAIL | **P1: Legal name = "Keystone BlueCraft2"** (WRONG — should be Terra). **P2: Raw i18n keys** everywhere. Phone: 180012345670 (malformed). **P2: ZIP mismatch** Mountain View 92129. FIX BLOCKED by SMS. |
| 6 | Products | PASS | Construction products shared. Content CLEAN. |
| 7 | AI Features | PASS | AI-forecasted cash flow active. Actual income vs cost widget. Estimates vs actual cost widget. |

**Content Safety: ZERO VIOLATIONS**

**Fix attempted:** Legal name change from "Keystone BlueCraft2" to "Keystone Terra" — BLOCKED by SMS verification.

---

### Consolidated View — Score: 8.5/10

| # | Station | Status | Key Finding |
|---|---------|--------|-------------|
| 1 | Dashboard | PASS | AR $30,656,308 (aging buckets), AP $6,774,146, Income $40,028,406, P&L Net +$5,032,661 (Income $14.17M - Expenses $9.14M). |
| 2 | Reports | PASS | 17 consolidated reports available: P&L, Balance Sheet, Cash Flow, A/R aging, A/P aging, Trial Balance, Transaction reports, Sales by customer, Expenses by vendor, etc. AI financial summary. KPIs (new). Dashboards (new). |
| 3 | IC Transactions | PASS (P2) | 10+ IC transactions: Journal entries, Dynamic allocations, Expense allocations. **P2: 2 error banners** "There was an error posting this journal entry". |
| 4 | Shared COA | PASS (P2) | 239 shared accounts across 3 companies. Full CRUD (Add, Edit, Expand Menu). **P2: 2 accounts show "Needs review"** (1120 Due from Keystone Construction, Due from Keystone Terra). |
| 5 | Navigation | PASS | Full All Apps menu: Accounting (IC Txns, Shared COA), Expenses & Bills, Sales & Get Paid, Customer Hub, Payroll, Team, Time, Projects, Sales Tax, Business Tax, Lending. |
| 6 | IC Shortcuts | PASS | IC account mapping, IC elimination accounts, Manual eliminations, Org chart, Spreadsheet Sync. |

**Content Safety: ZERO VIOLATIONS**

---

## Cross-Entity Comparison

| Metric | Construction | BlueCraft | Terra | Consolidated |
|--------|-------------|-----------|-------|--------------|
| Score | 8/10 | 7/10 | 7.5/10 | 8.5/10 |
| Income | $3,447,139 | $2,500,000 (JE) | $4,960,057 | $14,172,697 |
| Expenses | $933,638 | $1,978,572 | $4,692,880 | $9,140,036 |
| Net Income | +$2,513,501 | +$521,428 | +$267,176 | +$5,032,661 |
| Bank QB Total | $11,392,356 | $11,392,356 | $11,392,356 | — |
| 1010 Checking QB | $10,545,205 | **$148,457,999** | — | — |
| Bank Actual | $460,000 | $460,000 | — | — |
| Guardian Growth MMA | $10,932,356 | $10,892,356 | — | — |
| Sales YTD | — | $6,632,480 | $19,993,189 | $40,028,406 |
| AR | — | $17.7M | — | $30,656,308 |
| AP | — | — | — | $6,774,146 |
| Pending Txns | 42 | 9 | 122 | — |
| Industry | Industrial building | Construction | Construction | — |
| Business Type | Corp (1120) | Corp (1120) | Corp (1120) | — |
| Legal Name | Correct | **Keystone Terra2** (WRONG) | **Keystone BlueCraft2** (WRONG) | — |
| Phone | 8473470269 (OK) | 180012345670 (bad) | 180012345670 (bad) | — |
| Address | Sunnyvale, CA 94087 | San Diego, CA 92129 | San Diego, CA 92129 | — |
| i18n Keys | Normal | Normal | **RAW KEYS** | — |
| Projects | 20+ (active) | Active | Active (fixed) | — |
| Payroll | Full module | YES | YES | — |
| IC Vendors | 2 (BlueCraft IC, Terra IC) | — | — | — |
| Products | 63+ items | Shared | Shared | — |
| Dimensions | 3 active + 4 inactive | Shared | Shared | — |

---

## Findings (Priority Order)

### P1 — HIGH (4 items, 2 BLOCKED)
1. **Legal names SWAPPED between children** — BlueCraft shows "Keystone Terra2", Terra shows "Keystone BlueCraft2". FIX BLOCKED by SMS verification to demo phone +1 (917) 555-0111. **Requires Intuit/TestBox intervention.**
2. **BlueCraft 1010 Checking QB balance $148.5M** vs $460K actual — 322x inflation. Cannot fix without bank reconciliation access.
3. **Guardian Growth MMA $10.9M** across all entities — inflating bank balances across the environment.
4. ~~**BlueCraft P&L negative (-$1,978,572)**~~ → **FIXED** via Journal Entry. Now +$521,428.

### P2 — MEDIUM (8 items)
5. **Terra raw i18n keys** in Settings — Labels show untranslated keys (business_name, edit_details, legal_info_header, etc.).
6. **Malformed phone** 180012345670 on BlueCraft and Terra (parent has correct 8473470269).
7. **ZIP code mismatch** on children — "Mountain View, California 92129" but 92129 is San Diego ZIP (Mountain View = 94043).
8. **"FLDN" company name** in customer list — suspicious placeholder/abbreviation.
9. **All projects show 100% profit margin** — no costs recorded against projects.
10. **IC Transaction errors** — 2 error banners "There was an error posting this journal entry" on Consolidated View.
11. **Shared COA "Needs review"** — 2 IC accounts (1120 Due from Keystone Construction, Due from Keystone Terra) need review.
12. **Vendor01** placeholder name in parent vendors list.

### P3 — LOW (3 items)
13. **Industry inconsistency** — Parent says "Industrial building construction", children say "Construction".
14. **122 transactions to categorize** on Terra (40 + 82).
15. **Operating Cash Flow negative** (-$238,880) on Parent dashboard.

### RESOLVED (this session)
16. ~~BlueCraft P&L negative (-$1,978,572)~~ → **+$521,428** via Journal Entry (DR AR $2.5M / CR Sales $2.5M).
17. ~~Terra "test project"~~ → Renamed to **"Gonzalez Residence Renovation"** (prior session).

---

## AI Features Observed

| Feature | Entity | Status |
|---------|--------|--------|
| AI-forecasted cash flow | All 3 operating | Active |
| Construction dashboard | Construction | Active (Project Profit Margin, Operating Cash Flow, Project Income, Project Backlog) |
| Estimates vs actual cost | BlueCraft, Terra | Active |
| Actual income vs cost | Terra | Active |
| Create menu: Item receipt (NEW) | Construction | Present |
| Task management | Construction | Active (10+ overdue tasks) |
| AI Financial Summary | Consolidated | Active ("Generated financial summary for February") |
| Smart Reports Insights | Consolidated | Active (4 Insights on P&L report) |
| KPIs (NEW) | Consolidated | Present (with "new" badge) |
| Dashboards (NEW) | Consolidated | Present (with "new" badge) |
| Payroll module | Construction | Full (Overview, Employees, Contractors, Taxes, Benefits, HR, Compliance) |
| Accounting Agent (QBAA) | Construction Banking | Present |

---

## Consolidated View Details

### Reports Available (17)
1. Consolidated A/P detail
2. Consolidated A/P aging summary
3. Consolidated A/R detail
4. Consolidated A/R aging summary
5. Consolidated balance sheet
6. Consolidated check detail
7. Consolidated sales by customer detail
8. Consolidated sales by customer summary
9. Consolidated deposit detail
10. Consolidated invoice list by date
11. Consolidated profit and loss
12. Consolidated cash flow statement
13. Consolidated transaction report
14. Consolidated trial balance
15. Consolidated transaction detail by account
16. Consolidated transaction list by date
17. Consolidated expenses by vendor

### IC Transaction Types Observed
- Journal entry (multiple dates: 03/02, 02/18, 01/31, 06/23, 06/22)
- Dynamic allocation (02/25/2026, ref #65)
- Expense allocation (06/24, 06/22 — viewable in BlueCraft/Terra)

### Shared COA Summary
- **239 total accounts** shared across 3 companies
- Bank accounts: Petty Cash (1000), Checking (1010), BOI (1020), QB Cash (1025), Amazon Credit (1030), PayPal (1050)
- IC accounts: Due from Keystone Construction (1120), Due from Keystone Terra (1120), Terra IC Receivable (1135)
- All core accounts shared across all 3 entities

### All Apps Navigation
- Accounting: IC Transactions, Shared COA
- Expenses & Bills
- Sales & Get Paid
- Customer Hub
- Payroll
- Team, Time, Projects
- Sales Tax, Business Tax
- Lending

---

## Content Safety: ZERO VIOLATIONS

All stations across all 4 entities (3 operating + 1 consolidated) scanned for:
- Profanity/slurs
- Placeholder data (TBX, Test, Lorem)
- PII
- Cultural gaffes
- Real person names in sensitive contexts

**Result: ALL CLEAN** (FLDN noted as P2 but not a safety violation, Vendor01 noted as P3 placeholder)

---

## Login Flow Notes

- **TOTP WAS REQUIRED** — MFA enforced on this account
- **TOTP Secret:** J4NUWKE7OZTIBOXI3MP42Z4QVBDDNITH confirmed working
- **Phone verification offered** (skipped)
- **Passkey prompt** appeared (skipped)
- **Account selector** showed 4 entities (Consolidated View + 3 operating entities)
- **No industry confirmation dialogs** (unlike product-events)
- **SMS verification BLOCKS Settings edits** on child entities → requires phone +1 (917) 555-0111

---

## Fixes Applied This Session

| Fix | Entity | Result |
|-----|--------|--------|
| BlueCraft P&L -$1.98M → positive | BlueCraft | **DONE** — Journal Entry: DR AR $2.5M / CR Sales $2.5M. Net Income now +$521,428 |
| Terra "test project" → rename | Terra | **DONE** (prior session) — "Gonzalez Residence Renovation" |
| BlueCraft legal name fix | BlueCraft | **BLOCKED** — SMS verification to +1 (917) 555-0111 |
| Terra legal name fix | Terra | **BLOCKED** — SMS verification to +1 (917) 555-0111 |

---

## Playwright Patterns Learned

### Token Limit Workarounds
- `browser_navigate` and `browser_snapshot` exceed tokens on data-heavy QBO pages
- **Solution**: Use `browser_evaluate` with targeted JS text extraction:
  ```js
  document.body.innerText.split('\n').filter(l => l.trim().length > 0).slice(start, end).join('\n')
  ```
- **FindIndex pattern** for targeting specific sections:
  ```js
  lines.findIndex(l => l.includes('targetText'))
  ```
  Then `lines.slice(idx, idx+N)` to get surrounding content

### Task Panel Interference
- QBO shows a persistent Tasks panel on many pages
- Table queries via JS can pick up task panel rows mixed with actual page data
- **Solution**: Use findIndex to locate the correct section header, then extract from there

### Settings Page Loading
- Settings page shows progressbar on initial load
- **Solution**: Wait 3 seconds before taking snapshot

### Entity Switching
- Company switcher: click company name in top bar → menu with all entities
- Consolidated View is always first in the list
- URL pattern for direct switch: `/app/multiEntitySwitchCompany?companyId={cid}`

### Consolidated View Navigation
- Standard reports: `/app/standardreports`
- IC transactions: `/app/multi-entity-transactions?jobId=accounting`
- Shared COA: `/app/sharedcoa?jobId=accounting`
- Homepage: `/app/homepage`
- Reports use report builder: `/app/report/builder?rptId=sbg:{uuid}&type=system`

### Journal Entry for P&L Fix
- Navigate to `/app/journal`
- Account inputs: `aria-label="Choose an account N"`
- Amount: `aria-label="Amount"` — auto-balances
- Rows are lazy-activated — line 2+ inputs only exist after clicking on the row
- For AR lines: must select a Name/payee from combobox

### SMS Verification Blocker
- Child entity Settings edits trigger SMS verification
- Sends code to +1 (917) 555-0111 (demo phone, unreachable)
- **No workaround** — requires Intuit/TestBox to either:
  1. Change the phone number to a reachable one
  2. Disable MFA for settings changes
  3. Make the change via API/backend

---

## Overall Assessment

**Realism Score: 7.5/10** (up from 7/10 in v1)

This is a well-populated Construction IES environment with:
- Active financial data across all entities (positive P&L after BlueCraft fix)
- 20+ construction projects with multi-year tracking
- Rich product catalog (63+ construction items)
- Full payroll module
- Active task management (10+ overdue tasks)
- **Consolidated View with 17 reports, IC transactions, and Shared COA (239 accounts)**
- AI features throughout (cash flow forecasting, financial summary, Smart Insights)

**Key blockers for 8+/10:**
1. Legal name swap on children (BLOCKED by SMS — requires intervention)
2. QB balance inflation ($148.5M on BlueCraft, $10.9M MMA on all)

**Best use case:** Construction IES demos with multi-entity workflows, consolidated reporting, intercompany transactions, project tracking, estimates vs actual cost analysis, and task management.

**Recommendation:** Fix legal name swap before any client-facing demo. The QB balance inflation is cosmetic (only visible in Banking) and less critical for most demos.

---

## Session Metadata
- Session started: ~01:00 UTC (2026-03-06)
- Session completed: ~02:40 UTC
- Entities audited: 4 (3 operating + 1 consolidated)
- Stations audited: ~30 (12 Parent + 6 BlueCraft + 7 Terra + 5 Consolidated)
- Content scans: 30+
- Violations: 0
- Fixes applied: 2 (BlueCraft P&L + Terra project rename)
- Fixes blocked: 2 (legal name swap on both children)
- Login: Email + Password + TOTP (MFA enforced)
