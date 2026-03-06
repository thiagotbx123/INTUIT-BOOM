# Mid Market — QBO Sweep Report
**Date:** 2026-03-06
**Account:** mid_market@tbxofficial.com
**Password:** h6gr9otd*7ekLQ
**TOTP Secret:** 7OXWEFVAMN6WNN24IITYHINFR7OLS7IH (REQUIRED — MFA enforced)
**Environment:** Production QBO Advanced
**Industry:** Construction

---

## Environment Overview

| Property | Value |
|----------|-------|
| Entity | Single (child) — "Keystone Construction" |
| CID | 9341452713218633 |
| Entity Type | Child (construction dataset) |
| Multi-Entity | NO (single entity, no company switcher) |
| Industry | Construction |
| Business Type | Corporation, one or more shareholders (Form 1120) |
| Legal Name | Keystone Construction, LLC |
| EIN | •••••8735 |
| Company Address | 2700 Coast Ave, Mountain View, CA 94043-1140 |
| Email | contact@keystone-constructions.com |
| Phone | +16509446000 |
| QBO Tier | Advanced (Revenue Recognition, Fixed Assets, Live Experts) |

---

## Station Audit Results

### Dashboard — Score: 4/10

| Metric | Value |
|--------|-------|
| P&L Net Income (Feb) | **-$214,942** (P1 NEGATIVE) |
| Income (Feb) | $31,703 |
| Expenses (Feb) | $246,645 |
| Down % | 830% from prior month |
| Bank Total | $11,392,356 |
| Cash Flow | $11,392,356 (12-month projected) |
| Invoices Unpaid | $900,647 (32 open) |
| Invoices Overdue | $871,557 (14 overdue) |
| Invoices Paid | $20,600 (1 last 30 days) |
| Estimates | $6,679 (11 estimates) |
| Unbilled Income | $3,692,248 |

**Expense Breakdown (Last 30 Days):**
| Category | Amount | % |
|----------|--------|---|
| Payroll expenses | $214,076 | 87% |
| Office supplies & software | $20,000 | 8% |
| Repairs & maintenance | $4,000 | 2% |
| Depreciation | $3,503 | 1% |
| Other | $3,966 | 2% |

**Business Feed Tiles:**
- Action Item: 2 transactions to identify
- Overdue invoices: $33,576 worth of reminders ready
- P&L summary: Net -$214,942
- Customer Agent: 0 new leads
- Invoices paid: $20,600 this week
- Estimates accepted: 1 worth $1,324
- Monthly financial summary: February ready

---

### Settings — Score: 7/10

| Field | Value | Status |
|-------|-------|--------|
| Name | Keystone Construction | PASS |
| Legal Name | Keystone Construction, LLC | PASS |
| Industry | Construction | PASS |
| Business Type | Corporation (Form 1120) | PASS |
| Address | 2700 Coast Ave, Mountain View, CA 94043-1140 | PASS |
| Phone | +16509446000 | PASS (properly formatted) |
| Email | contact@keystone-constructions.com | PASS |
| EIN | •••••8735 | PASS |
| Website | None listed | P3 |
| Customer Address | abc New Court, Sunnyvale, **CO** 94087-3204 | **P2** (state should be CA, not CO) |
| Customer Address Street | "abc New Court" | **P2** (placeholder) |

---

### Customers — Score: 4/10

**76 customers total (1-50 on page 1, 26 on page 2)**

| Metric | Value |
|--------|-------|
| Total Customers | 76 |
| Estimates | 11 ($6,679) |
| Unbilled Income | $3,692,248 |
| Overdue Invoices | 14 ($871,557) |
| Open Invoices/Credits | 32 ($900,647) |
| Recently Paid | 1 ($20,600) |

**P1 — CRITICAL Customer Issues:**
| Customer | Company | Balance | Issue |
|----------|---------|---------|-------|
| Jason Cioran | Cioran's Acorns | **$19,999,999,999.00** | ~$20B — extreme test value |
| Keystone Construction | (self) | $880,866.23 | Company owes itself |

**P2 — Test/Placeholder Customer Names:**
| Customer | Company | Issue |
|----------|---------|-------|
| 12345 Auction | — | Numbered test name |
| Andrew Allen Test | — | Explicit "Test" |
| Andrew Allen Test 1 | Andrew Allen Test 1 | Explicit "Test" + duplicate |
| Cass Wyatt | TESTER | Explicit "TESTER" company |
| IDT Tester | — | Explicit "Tester" |
| Government Agency XYZ | Government Agency XYZ | Placeholder |
| Alan Somebody | — | Placeholder surname |
| Bill Smith | ACME Ltd | Generic test names |
| Ali Gold | FLDN | Suspicious abbreviation |

**Negative Balance Customers:**
- Abigail Patel / Haven Realty Holdings: -$33,057.62
- Alex Blakey / Blakey's Bin Liners: -$953.97
- Karuna Ramachandran: -$9,000.00
- Government Agency XYZ: -$180.22

**Top Customers by Balance:**
- Ava Li / Atlas Development Corporation: $149,124.68
- Leila Nguyen / Axis Realty Ventures: $115,432.10
- Logan Tran / Crown Holdings LLC: $119,012.34
- Chris Smith / Christopher's Custom Insoles: $235,788.01
- Ali Khan / Beacon Investments Inc.: $177,913.57

**Content Safety: PASS** (no profanity, PII, or cultural gaffes — test names are P2)

---

### Vendors — Score: 5/10

**61 vendors total (1-50 on page 1)**

| Metric | Value |
|--------|-------|
| Total Vendors | 61 |
| Unbilled (POs) | $3,385,721.17 (155 POs) |
| Unpaid | $11,146,585.15 (28 overdue) |
| Open Bills | $11,169,772.96 (30 open) |
| Paid (Last 30 Days) | $0.00 (1 paid) |

**P1 Issues:**
| Vendor | Balance | Issue |
|--------|---------|-------|
| Construction Materials Inc. | $5,428,310.61 | Single vendor = 50% of AP |
| Daniel Green | -$544,001.67 | Massive negative balance |

**Notable Vendors:**
- Abdi Structural Engineering, Al-Farsi Security Services, Blue Bird Insurance, Concrete Depot/Solutions, Contractor's Warehouse, Costa Masonry, Electrical Solutions/Supply Co., Elite Contracting, Heavy Equipment Depot, Hope Guard Insurance, HVAC Supply Store, IRS, CA EDD, Johnson Electrical Services, Kofi Structural Engineering, Landscaping Solutions, Lin Interior Designs

**Vendor Emails:** Mix of @tbxofficial.com and realistic domains
**Bill Pay ACH:** Only Blue Bird Insurance has bank info (US BANK NA ...6939). All others "Missing."

**Content Safety: PASS**

---

### Projects — Score: 6/10

**~19 projects**

| Project | Customer | Income | Costs | Margin | Hours |
|---------|----------|--------|-------|--------|-------|
| TidalWave - Farmer's Market | Matthew Ahmed | $5,523,931 | $1,781,791 | 67.7% | 1,366h |
| GaleGuardian - Turbine Installation | Amelia Patel | $4,954,712 | $2,151,348 | 56.6% | 1,964h |
| BMH Landscaping - Phase 1 | Emily Wong | $3,580,466 | $1,347,120 | 62.4% | 2,240h |
| Intuit Dome - Phase 2 | Priya Patel | $1,780,526 | $1,375,713 | 22.7% | 2,234h |
| Sawgrass residence | Abigail Patel | $27,248 | $5,065 | 81.4% | 12h |
| Bathroom Remodel | Gov Agency XYZ | $20,000 | $19,532 | 2.3% | 54h |

**P2 — Test/Placeholder Project Names:**
- "Example Proj" ($0/$0), "IDT TEST" ($430/$200), "Project 1" ($700/$0), "Test" x2 ($0/$0), "Title 1" ($0/$0), "lot clearing" ($0/$0)

**P2 — Extreme Negative Margins:**
- Contract A (Gov Agency XYZ): -2,249.4%
- Sawgrass residence - Abigail Patel: -2,059.5%
- Project A (Abigail Patel): -808.7%

**P2 — Customer Concentration:**
- Abigail Patel appears on 8 of 19 projects (42%)

---

### Products/Services — Score: 5/10

| Metric | Value |
|--------|-------|
| Total Products/Services | 112 (1-50 of 112) |
| Category | Commercial Construction |

**P1 Issues:**
- One product has description "nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn..." (70+ 'n' chars — spam/test data)

**Notable Items:**
- Legal services (Jonathan Scott, Harrison Scott paralegal)
- Construction-relevant categories

**Content Safety: PASS** (except "nnn..." spam)

---

### Payroll — Score: 7/10

| Metric | Value |
|--------|-------|
| Module | Full Payroll (Employees, Contractors, Taxes, Benefits, HR, Compliance) |
| States | California, Colorado, New York (multi-state) |
| Tax Penalty Protection | Inactive |

**TO DO Items (15+):**
- Re-enter Federal EIN (IRS rejected)
- 4 New Hire reports overdue (Logan Parker, Daniel Moreno, Michael Williams, Benjamin Brooks)
- File CA DE 9, CA DE 9C (Q4 2025) — Due Jan 29
- File 941 (Q4 2025) — Due Jan 29
- File NYS-45 (Q4 2025) — Due Jan 29
- File 940 (2025) — Due Jan 29
- File W-2 Copies A&D (2025) — Due Jan 29
- Pay overdue taxes
- Pay CO Income Tax zero payment — Due Mar 13
- Verify bank deposit (****7890)
- Provide critical tax information

**Employee Birthdays (Celebrate):**
- Ethan Jones: Mar 7
- Amelia Hernandez: Mar 10
- Henry Hill: Mar 12

---

### Banking — Score: 3/10

**10 bank accounts**

| Account | Bank Balance | QB Balance | Issue |
|---------|-------------|-----------|-------|
| 1000 Petty Cash | — | $20,840,442.88 | **P1 EXTREME** |
| 1010 Checking | $460,000 | -$1,832,169.79 | **P1 DISCREPANCY** |
| 1015 US Bank (3900) | — | $0 | — |
| 1020 BOI - Business Checking | — | -$150.00 | P2 negative |
| 1030 Amazon Credit | — | $0 | — |
| 1040 Bank of Intuit | — | $141,663.58 | — |
| 1050 PayPal Bank | — | $0 | — |
| (MMA) Guardian Growth | $10,932,356 | $10,398,418.37 | **P1 INFLATION** |
| Cash | — | -$1,455,866.03 | **P1 NEGATIVE** |
| 1810 Integra Arborists | — | $2,000.00 | — |

**P1:** Guardian Growth MMA $10.9M (same inflation as all construction environments)
**P1:** Petty Cash $20.8M (extreme — higher than any other environment)
**P1:** 1010 Checking Bank $460K vs QB -$1.83M (massive discrepancy)
**P1:** Cash account -$1.46M (negative)
**P2:** Bank connections updated 449 days ago (stale)

---

### Chart of Accounts — Score: 7/10

**Structure confirmed:**
- 1000 Petty Cash, 1010 Checking, 1020 BOI, (MMA) Guardian Growth
- 1110 Accounts Receivable (A/R)
- 1598 Payroll Refunds
- QuickBooks Payroll Tax Impound
- 2000 Accounts Payable (A/P)
- 2060 Deferred Revenue
- 2100 Payroll Liabilities (14+ sub-accounts)
- Numbered accounts (proper construction COA)
- Revenue Recognition feature present

---

## All Apps Menu (QBO Advanced Features)

| App | Sub-features |
|-----|-------------|
| Accounting | Bank transactions, Integration transactions, Receipts, Reconcile, Rules, COA, Recurring transactions, **Revenue recognition**, Fixed assets, My accountant, Live Experts |
| Expenses & Bills | — |
| Sales & Get Paid | Invoices, Payment links, Recurring payments, QuickBooks payouts, Products & services |
| Customer Hub | Overview, Leads, Customers, Estimates, Proposals, Contracts, Appointments, Reviews |
| Payroll | Overview, Employees, Contractors, Payroll taxes, Benefits, HR advisor, Compliance |
| Team | — |
| Time | — |
| Projects | — |
| Inventory | — |
| Sales Tax | — |
| Business Tax | — |
| Lending | — |

---

## AI Features Observed

| Feature | Status |
|---------|--------|
| Intuit Intelligence (Beta) | Active — chat, revenue analysis, bookkeeping optimization |
| Customer Agent | Active (0 new leads) |
| AI-powered P&L analysis | "Analyze my profit & loss" link |
| AI-powered invoice reminders | Active ($33,576 worth) |
| Monthly financial summary | Active (February ready) |
| AI-forecasted cash flow | Active (12-month projection) |
| Revenue down alerts | Active ("down 830% from prior month") |

---

## Findings (Priority Order)

### P1 — HIGH
1. **Net Income NEGATIVE** (-$214,942 Feb) — 830% down from prior month. Expenses $246K vs Income $32K.
2. **Jason Cioran $20B open balance** — Customer "Cioran's Acorns" has $19,999,999,999 open balance. Extreme test/dummy value.
3. **Guardian Growth MMA $10.9M** — Same inflation issue across all construction environments.
4. **Petty Cash $20.8M** — Highest across any environment. Extreme QB balance.
5. **1010 Checking discrepancy** — Bank $460K vs QB -$1.83M (nearly $2.3M difference).
6. **Cash account -$1.46M** — Negative cash balance.
7. **Vendor AP $11.1M** — $11,146,585 in unpaid vendor bills. Construction Materials Inc. alone = $5.4M.
8. **Daniel Green vendor -$544K** — Massive negative vendor balance.

### P2 — MEDIUM
9. **9 test/placeholder customer names** — 12345 Auction, Andrew Allen Test x2, Cass Wyatt/TESTER, IDT Tester, Gov Agency XYZ, Alan Somebody, Bill Smith/ACME, FLDN.
10. **6 test/placeholder project names** — Example Proj, IDT TEST, Project 1, Test x2, Title 1.
11. **Product "nnnn..." spam** — 70+ character test input in product description.
12. **Customer address state = CO** — Should be CA (Sunnyvale, CA 94087).
13. **Customer address = "abc New Court"** — Placeholder street.
14. **Keystone Construction self-reference** — $880K customer balance owed to itself.
15. **3 projects with extreme negative margins** (>-800%).
16. **Abigail Patel on 42% of projects** — Customer concentration.
17. **4 negative-balance customers** — Abigail Patel -$33K, Alex Blakey -$954, Karuna -$9K, Gov XYZ -$180.
18. **Bank connections 449 days stale** — Not updated in over a year.

### P3 — LOW
19. **15+ overdue payroll filings** — Q4 2025 tax filings and new hire reports past due.
20. **No website listed** in settings.
21. **$0 paid to vendors** in last 30 days.
22. **$3.7M unbilled income** — Large unbilled backlog.

---

## Content Safety: ZERO VIOLATIONS

All stations scanned for:
- Profanity/slurs
- PII (real SSN, real addresses)
- Cultural gaffes
- Real person names in sensitive contexts

**Result: CLEAN** (test/placeholder names are P2 content issues, not safety violations)

---

## Login Flow Notes

- **Password UPDATED** — Old password "Testbox123!" was rejected. New password `h6gr9otd*7ekLQ` confirmed working.
- **TOTP REQUIRED** — MFA enforced, code generated from `7OXWEFVAMN6WNN24IITYHINFR7OLS7IH`
- **Passkey prompt appeared** — Skipped via "Ignorar" → Redirected to Account Manager
- **QBO tab opened automatically** — No entity selector (single entity)
- **No industry confirmation dialogs** — Environment already configured
- **Intuit Intelligence chat** auto-opened on some pages

---

## Comparison: Mid Market vs Other Construction Environments

| Metric | Mid Market | QSP Events | Product Events |
|--------|-----------|-----------|---------------|
| Overall Score | **5.5/10** | 7.5/10 | 5/10 |
| Entities | 1 (child) | 4 (P+2C+CV) | 3 (P+2C) |
| Revenue (Feb) | $31,703 | $3.4M+ | $0 |
| Net Income | **-$214,942** | +$5M (consol.) | $0 |
| Customers | 76 | ~50 | ~50 |
| Vendors | 61 | ~30 | ~30 |
| Projects | 19 (4 rich) | 3+ | 0 |
| Products | 112 | — | — |
| Payroll | YES (active) | YES | YES |
| Revenue Recognition | YES | — | — |
| Inventory Module | YES | — | YES |
| Customer Hub | YES (full) | — | — |
| Guardian Growth MMA | $10.9M | $10.9M | $10.9M |
| Test/Placeholder Names | 15+ items | 1 (FLDN) | 1 (FLDN) |
| MFA Required | YES | YES | NO |
| QBO Tier | Advanced | Advanced (IES) | Advanced (IES) |

---

## Overall Assessment

**Realism Score: 5.5/10** — This is a single-entity QBO Advanced Construction environment with the RICHEST feature set of any environment audited (Revenue Recognition, Customer Hub with Leads/Proposals/Contracts/Reviews, full Payroll with multi-state filing, Inventory, Fixed Assets). However, it is severely impacted by:

1. **$20B customer balance** (Jason Cioran) — makes any financial report or demo unusable
2. **Negative net income** (-$215K) — down 830%, needs revenue injection
3. **$20.8M Petty Cash** — highest bank inflation across all environments
4. **15+ test/placeholder names** across customers, projects, and products
5. **$11M in unpaid vendor bills** — unrealistic for a child entity
6. **All payroll tax filings overdue** since Q4 2025

**Best use case:** Testing QBO Advanced features (Revenue Recognition, Customer Hub, Fixed Assets, Inventory, multi-state Payroll). NOT suitable for financial demos without significant cleanup.

**Recommended fixes (priority order):**
1. Delete Jason Cioran customer OR zero out the $20B balance
2. Create Journal Entry: DR Revenue / CR Expenses to make Net Income positive
3. Delete/rename test customers (Andrew Allen Test, IDT Tester, TESTER, etc.)
4. Delete/rename test projects (Example Proj, IDT TEST, Test x2, Title 1)
5. Fix "nnnn..." product description
6. Fix customer address state CO → CA

---

## Session Metadata
- Sweep started: ~17:00 UTC (2026-03-06)
- Sweep completed: ~17:15 UTC
- Stations audited: 8 (Dashboard, Settings, Customers, Vendors, Projects, Products, Payroll, COA/Banking)
- Content scans: 8
- Violations: 0
- Fixes attempted: 0 (reconnaissance only — no edits made)
- Login: Email + Password (NEW) + TOTP (MFA enforced)
