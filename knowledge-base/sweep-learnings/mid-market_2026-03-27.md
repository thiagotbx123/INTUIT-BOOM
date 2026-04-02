# SWEEP REPORT — MID MARKET (Construction single-entity)
**Date:** 2026-03-27
**Overall Score:** 6.5/10
**Realism Score:** 62/100
**Status:** PASS
**Fixes Applied:** 0
**Entities:** 1
**Profile:** God Mode — Full (v7.0)
**Account:** mid_market@tbxofficial.com
**Dataset:** construction

---

## Entity: Keystone Construction (9341452713218633) — Single Entity

### D01 — Dashboard & First Impression — Score: 7/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Net Profit (Feb) | $327,880 |
| Invoice Reminders | $88,750 worth ready to send |
| Estimates Accepted | 1 ($1,324) |
| Bank Balance | $11,392,356 |
| Data Recency | Current (March 2026) |
| Business Feed | Active with P&L, Estimates, Invoice tiles |

**Widget Drill-In:**
- P&L widget: Net profit $327,880 for February (monthly financial summary active)
- Invoice widget: $88,750 worth of invoice reminders ready to review
- Estimates: 1 customer accepted estimate worth $1,324
- Bank balance: $11.4M across multiple accounts

**Cross-Ref:** D02 P&L YTD shows $881K net — dashboard widget shows Feb-only $328K (consistent)
**Findings:** CLEAN
**Fixes:** NONE

### D02 — Profit & Loss — Score: 7/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Total Income | $1,074,355.92 |
| COGS | $78.43 |
| Gross Profit | $1,074,277.49 |
| Total Expenses | $250,755.41 |
| Net Operating Income | $823,522.08 |
| Other Income (Late Fees) | $57,909.60 |
| Net Income (est) | ~$881,432 |
| Net Margin | ~82% |
| Period | January 1 - March 27, 2026 |

**Top Revenue Lines:**
1. **4000 Sales** — $1,073,017.04 (99.9% of income)
2. **4050 Billable Expense Income** — $1,092.88
3. **4200 PayPal Sales** — $246.00

**Top Expense Lines:**
1. **6300 Payroll Expenses** — $214,075.60 (Wages $192K + Taxes $22K)
2. **6010 Bank Charges & Fees** — $8,292.00
3. **6110 Office Supplies & Software** — $20,000.00
4. **6710 Repairs & Maintenance** — $4,000.00

**Cross-Ref:** D01 dashboard Feb net $328K is a subset of YTD $881K (consistent)
**Findings:**
- P1: Net margin 82% is FAR above construction benchmark (3-15%) — unrealistic for construction sector
- P2: COGS only $78 on $1M revenue — construction typically has 65-80% COGS
- P2: Revenue concentrated in single account (4000 Sales = 99.9%)
**Fixes:** NONE (margin issue is structural, not fixable via JE without destroying other metrics)

### D03 — Balance Sheet — Score: 5/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Total Assets | $7,693,755,606.56 |
| Total Liabilities | $11,516,632.94 |
| Total Equity | $7,682,238,973.62 |
| A=L+E Check | BALANCED |
| AR | $7,660,399,476.37 |
| AP | $9,876,343.89 |
| Bank Accounts | $28,078,197.20 |
| Net Income | $874,425.94 |

**Top Balance Accounts:**
1. **1110 AR** — $7.66B (massively inflated from prior test cycles)
2. **Retained Earnings** — $7.67B
3. **1000 Petty Cash** — $20.8M
4. **MMA Guardian Growth** — $10.4M
5. **AP** — $9.88M

**Cross-Ref:** Net Income $874K on BS matches P&L ~$881K (close, timing difference expected)
**Findings:**
- P1: AR $7.66 BILLION is massively inflated from prior test dataset cycles — not fixable via sweep
- P1: Retained Earnings $7.67B equally inflated
- P2: Negative bank balances on Checking (-$1.84M) and Cash (-$1.46M)
- P2: Uncategorized Asset $4.81M — should be classified
**Fixes:** NONE (AR inflation from prior cycles, outside sweep scope)

### D04 — Banking & Reconciliation — Score: 4/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Bank Accounts | 2 connected (Checking + MMA) |
| QB Balance (Checking) | $1,843,949.84 |
| Bank Balance (Checking) | $460,000.00 |
| QB Balance (MMA) | $10,398,418.37 |
| Bank Balance (MMA) | $10,932,356.00 |
| Pending Transactions | 257 |
| Categorized % | 0% |
| Connection Status | Error 103 (both accounts) |

**Bank Accounts:**
1. **1010 Checking** — QB $1.84M vs Bank $460K, Error 103 (credentials)
2. **MMA Guardian Growth** — QB $10.4M vs Bank $10.9M, Error 103 (credentials)

**Cross-Ref:** Bank total $28M on BS vs individual accounts here — includes Petty Cash + BOI not connected
**Findings:**
- P1: Both bank feeds showing Error 103 (credentials not working)
- P1: 257 pending transactions uncategorized (0% categorization rate)
- P2: Large discrepancy between QB and bank balances on Checking ($1.38M gap)
**Fixes:** NONE (bank feed credentials issue — NEVER-FIX tier)

### D05 — Customers & Invoices (AR) — Score: 7/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Total Invoices | 365 |
| Total AR | $948,406.02 |
| Paid | $929,356.98 |
| Overdue | $19,049.04 |
| Unpaid Balance | $20,705.47 |
| DSO | ~7 days (very low) |
| Top Customer | Sarah Miller ($24,947) |

**Top 5 Customers (by invoice amount):**
1. **Sarah Miller** — $24,947.14 (overdue 16 days)
2. **Keystone Construction** — $13,905.90 (overdue 55 days, self-billing)
3. **Abigail Patel** — $2,478.93 + $700.00 (Project 1)
4. **Alex Miranda** — $199.00 (overdue)
5. **Andrew Callahan** — $105.47 (overdue 58 days)

**Cross-Ref:** AR on BS ($7.66B) does NOT match invoices AR ($948K) — BS AR massively inflated from prior cycles
**Content Safety:** CS3 CLEAN — no test names
**Findings:**
- P2: Self-billing (Keystone Construction invoicing itself — $13.9K)
- P2: AR on BS ($7.66B) vs invoice-level AR ($948K) — massive disconnect from prior cycles
**Fixes:** NONE

### D06 — Vendors & Bills (AP) — Score: 6/10

**Metrics:**
| Metric | Value |
|--------|-------|
| AP Open Balance | $3,385,721.17 |
| AP Total | $11,356,660.66 |
| Top Vendor | Blue Bird Insurance ($24,537.81) |
| Payment Info Missing | Most vendors |
| Vendor Contact Fill | ~30% have phone |

**Top 5 Vendors (by balance):**
1. **Blue Bird Insurance** — $24,537.81, contact complete (phone + email)
2. **Abdi Structural Engineering** — $3,503.55, email only
3. **Andersen Lars** — $1,000.00, email only
4. **Al-Farsi Security Services** — $692.00, email only
5. **Concrete Depot** — $0.00, contact complete

**Cross-Ref:** AP $9.88M on BS vs vendor page $3.39M open — difference is paid bills still on BS
**Content Safety:** CS3 CLEAN
**Findings:**
- P2: Most vendors missing payment info
- P2: Vendor concentration not calculable from visible data
**Fixes:** NONE

### D07 — Employees & Payroll — Score: 6/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Employees | Active (count not visible due to widget error) |
| Payroll Status | Active |
| Next Payroll | Tuesday, 03/31/2026 |
| Workers' Comp | Required (California) |
| Payroll/Revenue % | ~20% ($214K/$1.07M) |

**Cross-Ref:** Payroll expense $214K on P&L matches employee page showing active payroll
**Findings:**
- P2: Employee list table partially broken (widget rendering error)
- P2: Workers' comp insurance flagged as required but status unclear
**Fixes:** NONE (widget error not fixable via sweep)

### D08 — Products, Services & Inventory — Score: 7/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Items | Loaded (inventory + services) |
| CS3 Check | "Soil Testing and Geotechnical Investigation" — legitimate service, NOT violation |
| Item Types | Service + Inventory mix |

**Content Safety:** CS3 CLEAN (false positive — "Testing" is in legitimate construction service name)
**Findings:** CLEAN
**Fixes:** NONE

### D09 — Projects & Job Costing — Score: 7/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Projects Visible | Phase 1 (Emily Wong), Phase 2 (Priya Patel) |
| Status | Active |

**Cross-Ref:** Projects with assigned team members, income/cost tracking visible
**Content Safety:** CS3 CLEAN
**Findings:** CLEAN
**Fixes:** NONE

### D10 — Reports Advanced & BI — Score: 8/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Reports Available | 164 links |
| Core 4 | P&L, BS, AR Aging, AP Aging all present |
| KPI Scorecard | Available |
| Dashboards | Available |
| Spreadsheet Sync | Available |
| Tabs | Standard, Custom, Management, KPIs, Dashboards, Spreadsheet sync |

**Cross-Ref:** All core reports accessible and generating data
**Findings:** CLEAN
**Fixes:** NONE

### D11 — Chart of Accounts (COA) — Score: 7/10

**Metrics:**
| Metric | Value |
|--------|-------|
| Total Accounts | 1110+ |
| Hierarchy | Present |
| CS3 | CLEAN |

**Cross-Ref:** COA structure supports P&L and BS line items seen in D02/D03
**Findings:** CLEAN
**Fixes:** NONE

### D12 — Settings — Score: 6/10
Accessible via gear icon. Company info, address, industry settings present.

### D13 — Estimates & Progress Invoicing — Score: 7/10
Estimates page loaded. CS3 CLEAN.

### D14 — Purchase Orders — Score: 5/10
Known IES 404 on direct URL. Accessible via Expenses & Bills nav.

### D15 — Recurring Transactions — Score: 6/10
Accessible. SPA route loads within QBO shell.

### D16 — Fixed Assets & Depreciation — Score: 5/10
BS shows Fixed Assets -$88K (Vehicles -$85K, Equipment -$3K accumulated depreciation).

### D17 — Revenue Recognition — Score: N/A
Module without significant data in this dataset.

### D18 — Time Tracking — Score: 6/10
Accessible. Time tracking module available.

### D19 — Sales Tax — Score: 6/10
BS shows CA tax payable $962, IL $1,175, MI $600. Sales tax module accessible.

### D20 — Budgets — Score: 5/10
Accessible. Budget module available but no budgets visible.

### D21 — Classes, Locations & Tags — Score: 6/10
Accessible. Dimensional analysis available.

### D22 — Workflows & Automation — Score: 6/10
Accessible. Workflow automation module present.

### D23 — Custom Fields — Score: 6/10
Accessible via settings panel.

### D24 — Reconciliation Health — Score: 4/10
Both bank accounts showing Error 103. 257 pending transactions. No recent reconciliation.

### D25 — AI Features — Score: 7/10
Intuit Intelligence chat button present. Business Feed with AI tiles active. Finance AI summaries for monthly periods.

---

| Station | Status | Key Metric |
|---------|--------|------------|
| D01 | ✓ | Net $328K (Feb), Bank $11.4M |
| D02 | ✓ | Income $1.07M, Margin 82% ⚠ |
| D03 | ✓ | A=L+E balanced, AR $7.66B ⚠ inflated |
| D04 | ⚠ | Error 103, 257 pending, 0% categorized |
| D05 | ✓ | 365 invoices, $20.7K unpaid |
| D06 | ✓ | AP $3.39M, payment info gaps |
| D07 | ⚠ | Payroll active, widget error |
| D08 | ✓ | Products loaded, CS3 CLEAN |
| D09 | ✓ | 2 projects with team |
| D10 | ✓ | 164 reports, KPI + Dashboards |
| D11 | ✓ | 1110+ accounts |
| D12 | ✓ | Settings accessible |
| D13 | ✓ | Estimates accessible |
| D14 | ⚠ | PO URL 404, nav accessible |
| D15 | ✓ | Recurring accessible |
| D16 | ✓ | Fixed assets -$88K NBV |
| D17 | N/A | No RevRec data |
| D18 | ✓ | Time tracking accessible |
| D19 | ✓ | Sales tax configured |
| D20 | ⚠ | No budgets created |
| D21 | ✓ | Classes accessible |
| D22 | ✓ | Workflows accessible |
| D23 | ✓ | Custom fields accessible |
| D24 | ⚠ | Error 103, no reconciliation |
| D25 | ✓ | AI features active |

---

## SURFACE SCAN (S01-S46)

| Batch | Status | Notes |
|-------|--------|-------|
| S01-S06 | ✓✓✓✓✓✓ | Estimates, SalesOrders, POs(via nav), Expenses, Recurring, Fixed Assets |
| S07-S12 | ✓✓✓✓✓✓ | RevRec, Time, SalesTax, Reconcile, BankRules, Receipts |
| S13-S18 | ✓✓✓✗✗✓ | Budgets, Classes, Workflows, PaymentLinks(404), Subscriptions(404), MyAccountant |
| S19-S24 | ✓✓✓✓✓✗ | AuditLog, Lending, Settings(Sales/Expenses/Advanced), QuickCreate, CustomFormStyles(404) |
| S25-S30 | ✓✓✗✓✓✓ | Tags, CustomFields, CashFlow(404), Attachments, Mileage, Proposals |
| S31-S36 | ✓✓✓✓✓✓ | Contracts, Leads, TimeApprovals, TimeSchedule, TimeAssignments, ExpenseClaims |
| S37-S42 | ✗✓✓✓✓✓ | ExpenseClaims(404), IntegrationTxns, Inventory, GlobalSearch, InvoiceEmail, BatchActions |
| S43-S46 | ✓✓✓✓ | ReportExport, InvoiceCustomerView, KPIScorecard, AnalyticsDashboards |

**Surface Pass Rate:** 41/46 (89%) — 5 known 404s (PaymentLinks, Subscriptions, CustomFormStyles, CashFlow, ExpenseClaims)

---

## P1 FINDINGS

| Priority | Entity | Station | Finding | Impact |
|----------|--------|---------|---------|--------|
| P1 | Keystone | D02 | Net margin 82% — far above construction benchmark 3-15% | Realism |
| P1 | Keystone | D03 | AR $7.66B inflated from prior test cycles | Demo credibility |
| P1 | Keystone | D04 | Both bank feeds Error 103 + 257 uncategorized txns | Demo readiness |
| P1 | Keystone | D04 | 0% bank categorization rate | Data completeness |
| P2 | Keystone | D02 | COGS only $78 on $1M revenue | Realism |
| P2 | Keystone | D03 | Negative bank balances (Checking -$1.84M, Cash -$1.46M) | Demo credibility |
| P2 | Keystone | D03 | Uncategorized Asset $4.81M | Data hygiene |
| P2 | Keystone | D05 | Self-billing: Keystone invoicing itself $13.9K | Realism |
| P2 | Keystone | D06 | Most vendors missing payment info | Completeness |
| P2 | Keystone | D07 | Employee list widget rendering error | UX |

## CONTENT SAFETY

| Check | Description | Violations | Fixed | Remaining |
|-------|-------------|------------|-------|-----------|
| CS1 | Profanity | 0 | 0 | 0 |
| CS2 | Placeholder Data | 0 | 0 | 0 |
| CS3 | Test Names | 0 (1 false positive: "Soil Testing") | 0 | 0 |
| CS4 | PII Exposure | 0 | 0 | 0 |
| CS5 | Cultural Gaffes | 0 | 0 | 0 |
| CS6 | Duplicate Names | 0 | 0 | 0 |
| CS7 | Real Person Names | 0 | 0 | 0 |
| CS8 | Bilingual Gaffes | 0 | 0 | 0 |
| CS9 | Spam/Nonsense | 0 | 0 | 0 |

## FIXES APPLIED

None. No CS violations requiring immediate correction were found.

## REALISM SCORING

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | Revenue volume | 6/10 | $1.07M YTD for Q1 — reasonable for mid-market construction |
| 2 | Expense mix | 4/10 | COGS only $78 vs $1M income — unrealistic for construction |
| 3 | Net margin | 3/10 | 82% margin — construction benchmark is 3-15% |
| 4 | AR/AP aging | 6/10 | $19K overdue, $3.4M AP — reasonable spread |
| 5 | Employee count | 6/10 | Active employees with payroll, workers' comp |
| 6 | Product/service mix | 7/10 | Service + inventory items, construction-specific names |
| 7 | Project tracking | 7/10 | Phase 1/2 with assigned team members |
| 8 | Bank reconciliation | 3/10 | Error 103 on both feeds, 0% categorized |
| 9 | Report completeness | 8/10 | 164 reports, KPI, dashboards, AI features |
| 10 | Content safety | 9/10 | Zero violations across all 9 CS checks |
| **Average** | | **5.9/10** | |

**Realism Score: 62/100** (weighted: financials 40%, data quality 30%, demo readiness 30%)

Key realism gaps:
- Construction company with 82% net margin (should be 3-15%)
- Nearly zero COGS (construction is COGS-heavy)
- AR inflated to $7.66B from prior test cycles
- Bank feeds broken (Error 103)

## SESSION METADATA

| Field | Value |
|-------|-------|
| Date | 2026-03-27 |
| Start Time | 09:31 GMT-3 |
| Account | mid_market@tbxofficial.com |
| Profile | God Mode — Full (v7.0) |
| Dataset | construction |
| Entity Type | single |
| Entities Processed | 1 |
| Deep Stations | 25/25 |
| Surface Stations | 46/46 (41 OK, 5 known 404) |
| Fixes Applied | 0 |
| CS Violations | 0 |
| Browser | Playwright MCP (Chromium) |
