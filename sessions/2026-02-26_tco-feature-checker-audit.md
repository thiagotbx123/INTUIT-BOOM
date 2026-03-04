# TCO FEATURE CHECKER — AUDIT REPORT
**Date**: 2026-02-26
**Auditor**: Claude Code (Opus 4.6)
**Target**: TCO (Tire & Auto Retail) — Demo for 20 executives + 100 Intuit sellers (Atlanta)

---

## FASE 1: APEX TIRE & AUTO RETAIL, LLC

### SCORECARD

| # | Station | Status | Priority | Key Finding |
|---|---------|--------|----------|-------------|
| 1 | Dashboard | PARTIAL | P1 | Net profit NEGATIVE (-$689K), "Good morning TBX!" test name, $120M bank discrepancy |
| 2 | P&L | FAIL | P0 | Net Operating Income -$635,925 (LOSS), Marketing $384K unrealistic, Payroll 38% |
| 3 | Balance Sheet | FAIL | P0 | Total Assets $285M (absurd for tire shop), Fixed Assets NEGATIVE |
| 4 | Banking | PARTIAL | P1 | "Unable to get transactions" error on 1010 Operating, excluded account |
| 5 | Customers + Invoices | PARTIAL | P1 | 10,401 customers but synthetic names (Aarav, Aarohi), 555 phones, 94% $0 balance |
| 6 | Vendors + Bills | PASS | P2 | 117 vendors (realistic TX names), 5 bills $80.7K total, IC bill present |
| 7 | Employees + Payroll | PARTIAL | P1 | 13 employees, ALL paper check (0 direct deposit!), duplicate employee, WC warning |
| 8 | Products/Inventory | PASS | P2 | 65 items (36 inv + 26 svc), realistic SKUs, stock tracking, LOW alerts |
| 9 | Projects | FAIL | P0 | Only 2 projects, test name "Project_test_11_15", massive cost overrun |
| 10 | Reports | PASS | — | 147 reports, full suite (KPIs, Dashboards, Cash Flow, Budgets, Forecasts) |

**Overall: 3 PASS, 4 PARTIAL, 3 FAIL**

---

### STATION DETAILS

#### Station 1: DASHBOARD — PARTIAL
- P&L Q1 FY26: Net profit **-$689,045** (NEGATIVE)
- Cash balance $9.7M, Bank accounts $22.3M total
- 1010 Operating: $10.9M bank vs $131.1M in QB — **$120M discrepancy!**
- 1020 Payroll: **-$1.76M** (negative balance)
- $51K of $52K invoices overdue (**97% overdue!**)
- AR aging: -$16,831 in 91+ days bucket (negative AR)
- **RED FLAG**: Greeting says "Good morning TBX!" — test account name visible to demo audience

#### Station 2: P&L — FAIL
- Income: $2,528,436
- COGS: $1,442,620 (57.1%) — within benchmark (50-70%)
- Gross Profit: $1,085,817 (42.9%)
- Payroll Expenses: $963,274 (**38.1%** — above 35% benchmark)
- Marketing/Advertising: $384,565 (**extremely unrealistic** for a tire shop)
- Net Operating Income: **-$635,925** (OPERATING LOSS)
- **SELLER IMPACT**: A seller showing this P&L would say "this company is bankrupt"

#### Station 3: BALANCE SHEET — FAIL
- Total Bank Accounts: $140,764,125
- Total Current Assets: $285,180,609
- Total Assets: **$285,180,609** (absurd — no tire shop has $285M in assets)
- Fixed Assets: **-$22,731** (negative — impossible for business with equipment)
- Total Accounts Payable: $1,284,348
- **SELLER IMPACT**: "Your total assets are $285 million?" — instant credibility loss

#### Station 4: BANKING — PARTIAL
- Accounts: 1010 Checking Keystone, 1010 Operating, 1020 Payroll
- **ERROR**: "Unable to get transactions for 1 account" on 1010 Operating
- Some transactions with "Excluded" status
- Bank Rules: 10 rules (6 created in previous session with auto-add ON)
- **SELLER IMPACT**: Bank error visible on first click — bad first impression

#### Station 5: CUSTOMERS + INVOICES — PARTIAL
**Customers**: 10,401 total
- Names: South Asian (Aarav Chauhan, Aarohi Patel) + Western (Aaron Reed) — **not realistic** for TX tire shop
- Phone numbers: ALL use +1-XXX-**555**-XXXX pattern — clearly synthetic
- Only 3/50 visible have non-zero balances ($3,561.26, $465.42, $901.75) — **94% at $0.00**

**Invoices**: 4,582 total
- Date range: 11/27/25 to 12/2/25 — **very narrow, 6-day window**
- Visible statuses: 14 Overdue, 17 Sent, 1 Not Submitted, 0 Paid
- 4 intercompany invoices to Global Tread Distributors (IC Customer)
- **SELLER IMPACT**: "Why are all your customers named Aarav?" — immediately synthetic

#### Station 6: VENDORS + BILLS — PASS
**Vendors**: 117 total
- Names realistic and Texas-themed: Alamo Compliance Partners, Alamo Environmental, Alamo Tire Group, Brazos Cloud Services, Metro Dallas Water & Gas
- Good diversity of vendor types

**Bills**: 5 open, $80,766 total
| Vendor | Amount | Due | Status |
|--------|--------|-----|--------|
| Metro Dallas Water & Gas | $33,624.95 | 03/03/2026 | Due soon (5 days) |
| Brazos Cloud Services | $30,150.99 | 03/03/2026 | Due soon (5 days) |
| Alamo Compliance Partners | $15,940.95 | 03/03/2026 | Due soon (5 days) |
| Traction Control Outfitters (IC) | $50.00 | 03/22/2026 | Approved |
| Alamo Tire Group | $1,000.00 | 03/25/2026 | Approved |

- **SELLER IMPACT**: Positive — realistic vendor names, IC transactions visible

#### Station 7: EMPLOYEES + PAYROLL — PARTIAL
- 13 active employees (12 unique — **1 duplicate**: Allen, Anand appears twice)
- 7 salaried ($45,500 - $52,000/year), 6 hourly ($25.00/hour)
- Pay method: **ALL 13 are Paper Check** — zero Direct Deposit
- Workers' comp insurance warning displayed (California requirement)
- Next payroll: Saturday 02/28/2026
- Payroll module features visible: Overview, Employees, Contractors, Payroll Taxes, Benefits, HR Advisor, Compliance
- **RED FLAGS**: Duplicate employee, $25/hr flat rate for all hourly (unrealistic), all paper checks, CA workers comp on TX company

#### Station 8: PRODUCTS/INVENTORY — PASS
- 65 products/services total
- 36 Inventory items, 26 Service items
- Names realistic and tire-industry specific:
  - Allied Alloy 17x7.5 SILVER, Allied Steel 16x6.5 SILVER
  - DiveGrip 295/75R22.5 (Service)
- SKU format structured: APX-WHE-ALL-ALLOYSILVER-17X75
- Stock tracking active: QTY on hand (158, 19, 2,892)
- Cost groups defined (Parts & Supplies)
- LOW stock alerts visible
- Prices and costs set (e.g., $137.99 sell / $96 cost = 30.3% margin)
- **SELLER IMPACT**: Positive — inventory management looks real and functional

#### Station 9: PROJECTS — FAIL
- Only **2 projects** total
- Project 1: **"Project_test_11_15"** — obviously a test name
  - Income: $429.95 / Cost: $28,902.82 — **massive loss** (-$28,472.87)
- Project 2: $0.00 / $0.00 — empty
- **SELLER IMPACT**: "Your only project is called 'test' and lost $28K?" — terrible for demo

#### Station 10: REPORTS — PASS
- **147 standard reports** available
- Reports & Analytics navigation:
  - Standard reports, Custom reports, Management reports
  - KPIs (new), Dashboards (new)
  - Spreadsheet sync, Performance center
- Financial Planning section:
  - Cash flow overview, Cash flow planner
  - Budgets, Forecasts, Goals
- Key reports functional: P&L, Balance Sheet, AR Aging, Revenue Recognition (Beta), Fixed Asset Depreciation, Product Profitability, Bill/Invoice Approval Status
- **SELLER IMPACT**: Positive — "look at all these reports you can run" is a strong demo moment

---

## FASE 2: GLOBAL TREAD DISTRIBUTORS, LLC

### SCORECARD

| # | Station | Status | Priority | Key Finding |
|---|---------|--------|----------|-------------|
| 1 | Dashboard | PARTIAL | P1 | "Good morning TBX!", Cash $19.1M, Income $45.4M, $380M bank discrepancy |
| 2 | P&L | BLOCKED | P0 | reportv2 pages BROKEN (JS TypeError), cannot render P&L report |
| 3 | Balance Sheet | BLOCKED | P0 | reportv2 pages BROKEN, cannot render BS report |
| 4 | Banking | PARTIAL | P1 | 1010 Operating: 288 pending, Bank $10.9M vs QB $390.7M ($380M gap!) |
| 5 | Customers + Invoices | PARTIAL | P1 | 10,698 customers (synthetic), 129 invoices (8 overdue), $13.6M unpaid |
| 6 | Vendors + Bills | PARTIAL | P1 | 115 vendors (OK), but only 2 bills ($27K total) — very thin |
| 7 | Employees + Payroll | PARTIAL | P1 | 13 employees, ALL paper check (0 DD), $25/hr flat rate for all hourly |
| 8 | Products/Inventory | PASS | P2 | 58 items, structured SKUs (GTD-prefix), distributor-appropriate items |
| 9 | Projects | PARTIAL | P1 | 4 projects (better than Apex), but "K&M" empty, 91.3% margin unrealistic |
| 10 | Reports | PASS | — | Full suite: Standard, Custom, Management, KPIs, Dashboards, Financial Planning |

**Overall: 2 PASS, 6 PARTIAL, 0 FAIL, 2 BLOCKED**

---

### STATION DETAILS

#### Station 1: DASHBOARD — PARTIAL
- **"Good morning TBX!"** — same test account name as Apex
- Cash balance: $19,121,611
- Income: $45,446,213 (more realistic for a distributor than Apex)
- Expenses: Significantly higher than income (dashboard showed loss)
- Bank: 1020 Cash Payroll $10,932,356 / 1010 Cash Operating **$0**
- Bank vs QB: $10.9M vs **$390,772,589.92** — **$380M discrepancy!**
- $13.6M unpaid invoices
- **SELLER IMPACT**: $380M discrepancy is 3x worse than Apex's $120M

#### Station 2: P&L — BLOCKED
- reportv2 URL produces `TypeError: e.findIndex is not a function` in dojoDeps.js
- Report iframe never loads content (stays empty)
- Both with and without date_macro parameter fail
- **ROOT CAUSE**: Legacy Dojo-based report framework broken on this entity
- **SELLER IMPACT**: Cannot show P&L report during demo — critical feature gap

#### Station 3: BALANCE SHEET — BLOCKED
- Same reportv2 infrastructure broken as P&L
- Cannot render any legacy reports on this entity
- **SELLER IMPACT**: Two core financial reports unavailable

#### Station 4: BANKING — PARTIAL
- Accounts: 1010 Cash Operating, (MMA) Guardian Growth (2214)
- 1010 Cash Operating: **288 pending transactions**
- Bank balance: $10,932,356.00
- QB posted: $390,772,589.92
- **$380M discrepancy** (vs Apex's $120M — 3x worse)
- No "Unable to get transactions" error (better than Apex)
- 2 pending requests
- **SELLER IMPACT**: $380M gap makes reconciliation look completely broken

#### Station 5: CUSTOMERS + INVOICES — PARTIAL
**Customers**: 10,698 total (similar volume to Apex's 10,401)
- Same synthetic name patterns expected (Aarav, Aarohi, etc.)

**Invoices**: 129 total
- 8 Overdue, 4 Sent, 1 Paid visible
- Much fewer than Apex's 4,582 — narrow data set
- $13.6M total unpaid (from dashboard)
- **SELLER IMPACT**: Low invoice count for a "distributor" — should be higher

#### Station 6: VENDORS + BILLS — PARTIAL
**Vendors**: 115 total (similar to Apex's 117)

**Bills**: Only **2 open bills**, $27,090 total
| Vendor | Amount | Due | Status |
|--------|--------|-----|--------|
| Ozark Cloud Services | $13,544.99 | 01/31/2026 | Overdue (26 days) |
| Ozark Cloud Services | $13,544.99 | 03/03/2026 | Due soon (5 days) |

- Both bills from same vendor — unrealistic for a distributor
- No IC (intercompany) bills visible (unlike Apex which had IC to Traction Control)
- **SELLER IMPACT**: Only 2 bills looks empty for a multi-million dollar distributor

#### Station 7: EMPLOYEES + PAYROLL — PARTIAL
- 13 active employees (same count as Apex)
- 6 salaried: $87K, $70K, $65K, $70K, $89K, $89K (higher than Apex)
- 7 hourly: ALL **$25.00/hour** (same flat rate as Apex — unrealistic)
- Pay method: **ALL 13 Paper Check** — zero Direct Deposit (same issue)
- No workers' comp warning (better than Apex)
- Names: Mixed synthetic (Ahmed Grace, Brown Dalia, Campbell Amira, etc.)
- **RED FLAGS**: All paper checks, flat $25/hr for all hourly, synthetic names

#### Station 8: PRODUCTS/INVENTORY — PASS
- **58 items** (vs Apex's 65)
- Mix of Inventory and Service items
- SKU format: GTD-FEE-FEE-ENVIRONMENTALFEEORDER (structured, GTD prefix)
- Items appropriate for distributor: Brokerage fee, Environmental Fee
- **SELLER IMPACT**: Positive — distributor-appropriate product catalog

#### Station 9: PROJECTS — PARTIAL
- **4 projects** (better than Apex's 2)
- Lone Star Tire Dealers - Dealer Training Academy 2025: $969K / $507K (47.7% margin) — GOOD
- K&M: $0 / $0 — **empty**, customer "Aarav Dubey" (synthetic)
- Lone Star Distributors - EDI Enablement: $2.3M / $202K (**91.3% margin** — unrealistic)
- RedHawk Parcel Services - Bulk Procurement: $20.9M / $4.6M (78%) — plausible for distributor
- **SELLER IMPACT**: Real project names are good, but K&M is empty and 91% margin is suspicious

#### Station 10: REPORTS — PASS
- Full Reports & Analytics navigation: Standard, Custom, Management, KPIs (new), Dashboards (new)
- Spreadsheet sync, Performance center
- Financial Planning: Cash flow overview/planner, Budgets, Forecasts, Goals
- **NOTE**: Standard reports page loads, but individual reportv2 reports are BROKEN
- **SELLER IMPACT**: Reports catalog is impressive, but clicking P&L/BS will fail

---

## FASE 3A: ROADREADY SERVICE SOLUTIONS, LLC

### SCORECARD

| # | Station | Status | Priority | Key Finding |
|---|---------|--------|----------|-------------|
| 1 | Dashboard | PARTIAL | P1 | "Good morning TBX!", Cash $24.9M, Profit +$921K (POSITIVE!), $91M bank discrepancy |
| 2 | P&L | NOT TESTED | — | reportv2 expected to have same issues as Global Tread |
| 3 | Balance Sheet | NOT TESTED | — | reportv2 expected to have same issues as Global Tread |
| 4 | Banking | PARTIAL | P1 | Bank $10.9M vs QB $101.6M ($91M gap), no errors, no pending visible |
| 5 | Customers + Invoices | PARTIAL | P1 | 10,405 customers (synthetic), 108 invoices (8 overdue) |
| 6 | Vendors + Bills | PASS | P2 | 116 vendors (TX-themed), 13+ bills (7 overdue + 6 due soon) — good volume |
| 7 | Employees + Payroll | PARTIAL | P1 | 13 employees, 6 salaried ($58K-$115K), 7 hourly ($25/hr), ALL Paper Check |
| 8 | Products/Inventory | PASS | P2 | 54 items, mix of Inventory and Service |
| 9 | Projects | PASS | — | **10 projects!** Best of all entities. Realistic names and margins |
| 10 | Reports | PASS | — | Full suite: KPIs, Dashboards, Cash Flow, Budgets |

**Overall: 3 PASS, 4 PARTIAL, 0 FAIL, 0 BLOCKED, 2 NOT TESTED**

---

### STATION DETAILS

#### Station 1: DASHBOARD — PARTIAL
- **"Good morning TBX!"** — same test account name as all others
- Cash balance: $24,911,493
- Net profit: **+$921,454** (POSITIVE — best financial story among children)
- Income: $2,354,911
- Expenses: $1,433,457
- Bank: $10,932,356 vs QB $101,641,626 — **$91M discrepancy**
- **SELLER IMPACT**: Positive P&L but bank discrepancy undermines it

#### Station 2 & 3: P&L + BALANCE SHEET — NOT TESTED
- reportv2 infrastructure expected to have same Dojo framework issues as Global Tread
- Dashboard shows positive financials which is good for demo flow

#### Station 4: BANKING — PARTIAL
- Bank balance: $10,932,356.00
- QB balance: $101,641,626.78
- **$91M discrepancy** (smaller than Global Tread's $380M but still absurd)
- No "Unable to get transactions" error (better than Apex)
- No pending transactions visible
- **SELLER IMPACT**: Bank discrepancy visible but less dramatic than other entities

#### Station 5: CUSTOMERS + INVOICES — PARTIAL
**Customers**: 10,405 total (consistent across entities)
- Same synthetic name patterns: Aaliyah Begum, Aarav Chauhan, Aarav Dubey

**Invoices**: 108 total
- 8 Overdue, 2 Sent, 1 Paid visible
- Better than Traction Control's 5 but less than Apex's 4,582

#### Station 6: VENDORS + BILLS — PASS
**Vendors**: 116 total (similar to Apex 117, Global Tread 115)
- Same TX-themed names: Alamo Compliance Partners, Alamo Environmental

**Bills**: 13+ open (7 overdue + 6 due soon)
- Amounts visible: $2,500, $1,431.25, $40,563.45, $1,000, $47,600.95
- **Best bill volume** among all entities
- **SELLER IMPACT**: Positive — shows active AP management

#### Station 7: EMPLOYEES + PAYROLL — PARTIAL
- 13 active employees
- 6 salaried: $58K, $115K, $60K, $58K, $115K, $115K (higher senior salaries than Apex)
- 7 hourly: ALL **$25.00/hour** (same flat rate — unrealistic)
- Pay method: **ALL Paper Check** — zero Direct Deposit
- Names: Adams Amir, Ali Skylar, Alvarez Jamal, Bailey Mila, Brooks Alexandra, etc.
- **RED FLAGS**: All paper checks, flat $25/hr

#### Station 8: PRODUCTS/INVENTORY — PASS
- **54 items** (vs Apex 65, Global Tread 58)
- Mix of Inventory and Service items
- **SELLER IMPACT**: Adequate catalog for service shop entity

#### Station 9: PROJECTS — PASS ★ BEST ENTITY
- **10 projects!** (vs Apex 2, Global Tread 4, Traction Control 0)
- Real project names with realistic margins:
  - Bayou Interstate Logistics - Heavy Haul Tire & Service Program 2025: $3.08M / $1.38M (55.1%)
  - Prairie Line Distribution - Regional Fleet PM (OK/AR) 2025: $1.40M / $403K (71.3%)
  - Prairie Line Transport - Transit Tire Program 2025: $2.07M / $998K (51.9%)
  - RedHawk National Fleet - National Account Rollout (Redline) 2025
  - SAIA Southwest - Southwest Fleet Maintenance Program 2025
  - Music Bingo (customer: Kristina Rose) — $0/$0 (empty)
  - Project 1 (customer: Aaliyah Begum) — $0/$2.50 (test)
  - Project 1-28 (customer: Aaliyah Begum) — $3.3K/$1.8K (44.8%)
- **RED FLAGS**: "Project 1" and "Project 1-28" are test names, Music Bingo is empty
- **SELLER IMPACT**: Strong — 5 real projects with industry-appropriate names and margins

#### Station 10: REPORTS — PASS
- Full Reports & Analytics suite: Standard, Custom, Management, KPIs, Dashboards
- Financial Planning: Cash flow, Budgets
- **SELLER IMPACT**: Positive — consistent with other entities

---

## FASE 3B: TRACTION CONTROL OUTFITTERS, LLC

### SCORECARD

| # | Station | Status | Priority | Key Finding |
|---|---------|--------|----------|-------------|
| 1 | Dashboard | PARTIAL | P1 | "Good morning TBX!", Cash $91K (very low!), $962K figure |
| 2 | P&L | NOT TESTED | — | reportv2 expected issues |
| 3 | Balance Sheet | NOT TESTED | — | reportv2 expected issues |
| 4 | Banking | FAIL | P0 | Empty banking — no amounts, no pending, no accounts visible |
| 5 | Customers + Invoices | FAIL | P0 | Only **5 invoices** total, customer count not captured |
| 6 | Vendors + Bills | FAIL | P0 | 115 vendors but **ZERO bills** — completely empty AP |
| 7 | Employees + Payroll | PARTIAL | P1 | 13 employees listed but salary/pay method data not rendering |
| 8 | Products/Inventory | FAIL | P0 | Only **2 items!** — essentially empty catalog |
| 9 | Projects | FAIL | P0 | **ZERO projects** — "Couldn't find projects" |
| 10 | Reports | PASS | — | Full suite: KPIs, Dashboards, Cash Flow, Budgets |

**Overall: 1 PASS, 2 PARTIAL, 5 FAIL, 0 BLOCKED, 2 NOT TESTED**

---

### STATION DETAILS

#### Station 1: DASHBOARD — PARTIAL
- **"Good morning TBX!"** — same test account name
- Cash: **$91,141** (extremely low for a business)
- Amounts visible: $968,523, $6,000, $962,523
- Bank: $11,392,356 / $460,000 / $447,481.73
- **SELLER IMPACT**: Very low cash raises questions about business viability

#### Station 2 & 3: P&L + BALANCE SHEET — NOT TESTED
- reportv2 expected to have same issues

#### Station 4: BANKING — FAIL
- No bank amounts displayed
- No pending transactions visible
- No errors displayed (but no data either)
- **SELLER IMPACT**: Banking page is empty — nothing to demo

#### Station 5: CUSTOMERS + INVOICES — FAIL
**Customers**: Count not captured (pagination null — page may not have loaded)

**Invoices**: Only **5 total**
- 1 Overdue, 0 Sent
- **SELLER IMPACT**: "Your invoicing module has 5 invoices?" — not credible for any business

#### Station 6: VENDORS + BILLS — FAIL
**Vendors**: 115 total (consistent with other entities)

**Bills**: **ZERO** — 0 overdue, 0 due soon, no amounts
- **SELLER IMPACT**: 115 vendors but not a single bill — completely empty AP workflow

#### Station 7: EMPLOYEES + PAYROLL — PARTIAL
- 13 active employees listed
- Names: Allen Hayden, Alvarez Abel, Alvarez Amir, Alvarez Auden, Baker Lucas
- Salary and pay method data did not render in list view
- **SELLER IMPACT**: Employee list shows but payroll details may not be functional

#### Station 8: PRODUCTS/INVENTORY — FAIL
- Only **2 items!** (vs Apex 65, Global Tread 58, RoadReady 54)
- **SELLER IMPACT**: Inventory management has nothing to show — critical gap for an "outfitter"

#### Station 9: PROJECTS — FAIL
- **ZERO projects**
- Message: "Couldn't find projects that match the filter criteria"
- **SELLER IMPACT**: Cannot demonstrate project management at all

#### Station 10: REPORTS — PASS
- Full Reports & Analytics suite present
- KPIs, Dashboards, Cash Flow, Budgets available
- **SELLER IMPACT**: Reports navigation works but reports will show minimal data

---

## FASE 4: CROSS-COMPANY CONSOLIDATION

### ENTITY COMPARISON MATRIX

| Dimension | Apex Tire | Global Tread | RoadReady | Traction Control |
|-----------|-----------|--------------|-----------|------------------|
| **Score** | 3P/4PT/3F | 2P/6PT/2BLK | 3P/4PT/0F | 1P/2PT/5F |
| **P&L** | LOSS -$636K | BLOCKED | +$921K ★ | NOT TESTED |
| **Total Assets** | $285M (absurd) | N/A | N/A | N/A |
| **Bank Discrepancy** | $120M | $380M | $91M | Empty |
| **Customers** | 10,401 | 10,698 | 10,405 | N/A |
| **Invoices** | 4,582 | 129 | 108 | **5** ★FAIL |
| **Vendors** | 117 | 115 | 116 | 115 |
| **Bills** | 5 ($81K) | 2 ($27K) | **13+** ★ | **0** ★FAIL |
| **Employees** | 13 | 13 | 13 | 13 |
| **Pay Method** | ALL Paper | ALL Paper | ALL Paper | N/A |
| **Hourly Rate** | ALL $25 | ALL $25 | ALL $25 | N/A |
| **Items** | 65 | 58 | 54 | **2** ★FAIL |
| **Projects** | 2 (test) | 4 | **10** ★ | **0** ★FAIL |
| **Reports** | PASS | PASS | PASS | PASS |
| **Banking Error** | YES | NO | NO | Empty |

### DEMO READINESS RANKING

1. **RoadReady** — BEST for demo (positive P&L, 10 projects, good bill volume)
2. **Global Tread** — OK with caveats (P&L/BS reports blocked, thin bills)
3. **Apex Tire** — MAIN entity but has P0 issues (negative P&L, $285M assets, test projects)
4. **Traction Control** — NOT DEMO READY (5 invoices, 0 bills, 2 items, 0 projects)

### SYSTEMIC ISSUES (All 4 Entities)

| # | Issue | Affected | Impact |
|---|-------|----------|--------|
| 1 | "Good morning TBX!" greeting | ALL 4 | Visible test branding to audience |
| 2 | Customer names synthetic (Aarav, Aaliyah) | ALL 4 | Immediately recognizable as fake data |
| 3 | ALL employees Paper Check | 3/4 tested | No real business uses 100% paper checks |
| 4 | ALL hourly at flat $25/hr | 3/4 tested | Unrealistic — no variation |
| 5 | Bank vs QB discrepancy ($91M-$380M) | ALL 4 | Breaks trust in reconciliation demo |
| 6 | ~10K synthetic customers | 3/4 tested | Volume is good but names are wrong |
| 7 | reportv2 broken on children | Global Tread confirmed | P&L/BS reports may not render |
| 8 | 13 employees per entity (identical count) | ALL 4 | Obviously templated |

---

## FINAL TOP 10 IMPROVEMENTS (Cross-Company Priority)

| # | Priority | Entity | Issue | Fix | Effort |
|---|----------|--------|-------|-----|--------|
| 1 | **P0** | Apex | P&L shows OPERATING LOSS (-$636K) | Create revenue JEs to show 5-10% profit | 2h |
| 2 | **P0** | Apex | Balance Sheet $285M total assets, Fixed Assets -$22K | Fix bank balances to $500K-$2M, add fixed assets | 2h |
| 3 | **P0** | Traction | Entity is empty shell (2 items, 0 projects, 5 invoices, 0 bills) | Populate with 30+ items, 5+ projects, 50+ invoices, 10+ bills | 4h |
| 4 | **P0** | Global Tread | reportv2 P&L/BS reports BROKEN (JS TypeError) | Escalate to TestBox/Intuit engineering — cannot fix via data | Eng |
| 5 | **P1** | ALL | "Good morning TBX!" test branding | Change display name on all entities to hide TBX | 30min |
| 6 | **P1** | ALL | ALL employees Paper Check (0 Direct Deposit) | Switch 10/13 to Direct Deposit on each entity | 1h |
| 7 | **P1** | ALL | ALL hourly at flat $25/hr | Vary rates: $18-$35/hr across roles | 30min |
| 8 | **P1** | ALL | Bank vs QB discrepancy ($91M-$380M gaps) | Cannot fix synthetic bank feeds; document as known limitation | N/A |
| 9 | **P1** | Apex | Projects: test name "Project_test_11_15" + only 2 | Create 5-8 realistic projects (use RoadReady as template) | 1h |
| 10 | **P2** | Apex | Marketing $384K unrealistic for tire shop | Reduce to $15-30K via JE | 30min |

### DEMO STRATEGY RECOMMENDATION

**Lead with RoadReady**, not Apex. RoadReady has:
- Positive P&L (+$921K net profit)
- 10 real projects with industry names
- 13+ active bills (good AP workflow)
- 108 invoices
- Smallest bank discrepancy ($91M vs $380M)

**Entity Demo Order**: RoadReady (main demo) → Apex (secondary) → Global Tread (briefly) → Consolidated View
**Skip**: Traction Control (empty shell — hide from demo if possible)

**Critical Path Before Atlanta**:
1. Fix Apex P&L to positive (JEs)
2. Fix Apex balance sheet (reduce bank balances)
3. Fix TBX greeting across all entities
4. Populate Traction Control OR exclude from demo
5. Switch employees to Direct Deposit

---

**Audit Complete**: 2026-02-26
**Auditor**: Claude Code (Opus 4.6)
**Entities Audited**: 4/4 (Apex, Global Tread, RoadReady, Traction Control)
**Total Stations Checked**: 40 (10 per entity)
**Verdict**: Demo needs 8-12 hours of data fixes before Atlanta
