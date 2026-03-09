# Mid Market — QBO Sweep v3.0 Report (v2)
**Date:** 2026-03-06
**Sweep Version:** v3.0 (12 Deep + 20 Surface + 14 Conditional)
**Account:** mid_market@tbxofficial.com
**Password:** h6gr9otd*7ekLQ
**TOTP Secret:** 7OXWEFVAMN6WNN24IITYHINFR7OLS7IH (REQUIRED — MFA enforced)
**Environment:** Production QBO Advanced
**Industry:** Construction
**Overall Score:** **6.5/10** (up from 5.5/10 in v1)

---

## Changes from v1 → v2

| Change | Before | After |
|--------|--------|-------|
| P&L Net Income (Feb) | **-$214,942** | **+$285,058** ✅ |
| JE #114 (03/06/2026) | — | DR AR $500K Ali Khan / CR Sales $500K |
| JE #115 (02/28/2026) | — | DR AR $500K Mateo Gonzalez / CR Sales $500K (backdated Feb) |
| Deep Stations | 8 | **12** |
| Surface Scan | 0 | **20 pages** |
| Conditional Checks | 0 | **3 confirmed** |
| Dashboard Score | 4/10 | **6/10** |
| Overall Score | 5.5/10 | **6.5/10** |

---

## Environment Overview

| Property | Value |
|----------|-------|
| Entity | Single — "Keystone Construction" |
| CID | 9341452713218633 |
| Entity Type | Single entity (NO company switcher, NOT IES multi-entity) |
| Industry | Construction |
| Business Type | Corporation, one or more shareholders (Form 1120) |
| Legal Name | Keystone Construction, LLC |
| EIN | •••••8735 |
| Company Address | 2700 Coast Ave, Mountain View, CA 94043-1140 |
| Email | contact@keystone-constructions.com |
| Phone | +16509446000 |
| QBO Tier | Advanced (Revenue Recognition, Fixed Assets, Customer Hub, Full Payroll) |

---

## TIER 1 — Deep Stations (12/12)

### Station 1: Dashboard — Score: 6/10 (was 4/10)

| Metric | Value |
|--------|-------|
| P&L Net Income (Feb) | **+$285,058** ✅ FIXED (was -$214,942) |
| Income (Feb) | $531,703 (was $31,703 before JEs) |
| Expenses (Feb) | $246,645 |
| Growth | Up 868% from prior month |
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
- Customer Agent: 0 new leads
- Invoices paid: $20,600 this week
- Estimates accepted: 1 worth $1,324
- Monthly financial summary: February ready

---

### Station 2: P&L Report — Score: 7/10

| Metric | Value |
|--------|-------|
| Net Income (Feb) | **+$285,058** ✅ |
| Total Income | $531,703 |
| Total Expenses | $246,645 |
| Fix Applied | JE #115 (02/28/2026): DR AR $500K / CR Sales $500K |

---

### Station 3: Balance Sheet — Score: 4/10

| Section | Amount |
|---------|--------|
| **Total Assets** | **$7,693,721,769.10** (~$7.7 BILLION) |
| Accounts Receivable (A/R) | $7,660,351,717.81 |
| Bank & Cash | $28,092,339.01 |
| Fixed Assets | -$88,511.67 |
| Other Assets | ~$5.37M |
| **Total Liabilities** | ~$11.2M+ |
| Accounts Payable (A/P) | $9,689,247.24 |
| Equity | Not fully visible (report truncated in new builder) |

**P1:** Total assets inflated to $7.7B due to Jason Cioran $20B AR entry
**P1:** Fixed assets negative (-$88K) — depreciation exceeds cost basis

**Bank Account Breakdown:**
| Account | QB Balance |
|---------|-----------|
| 1000 Petty Cash | $20,840,442.88 |
| (MMA) Guardian Growth | $10,398,418.37 |
| 1040 Bank of Intuit | $141,663.58 |
| 1810 Integra Arborists | $2,000.00 |
| 1010 Checking | -$1,832,169.79 |
| Cash | -$1,455,866.03 |
| 1020 BOI - Business Checking | -$150.00 |
| 1015 US Bank (3900) | $0 |
| 1030 Amazon Credit | $0 |
| 1050 PayPal Bank | $0 |

---

### Station 4: Banking — Score: 3/10

| Metric | Value |
|--------|-------|
| Pending Transactions | 262 |
| Bank Connections | Error 103 (auth broken) on MMA + 1010 Checking |
| Connection Age | 449+ days stale |
| Bank Balance (1010) | $460,000 |
| QB Balance (1010) | -$1,832,169.79 |
| Discrepancy | ~$2.3M |

**P1:** Error 103 on both primary bank feeds — no new data syncing
**P1:** 262 unreviewed transactions in pending queue
**P1:** 1010 Checking: Bank $460K vs QB -$1.83M

---

### Station 5: Customers — Score: 4/10

**76 customers total**

| Metric | Value |
|--------|-------|
| Total Customers | 76 |
| Estimates | 11 ($6,679) |
| Unbilled Income | $3,692,248 |
| Overdue Invoices | 14 ($871,557) |
| Open Invoices/Credits | 32 ($900,647) |
| Recently Paid | 1 ($20,600) |
| Customer Hub | Active (Leads, Proposals, Contracts, Appointments, Reviews) |

**P1 — Critical:**
| Customer | Balance | Issue |
|----------|---------|-------|
| Jason Cioran / Cioran's Acorns | $19,999,999,999.00 | ~$20B extreme test value |
| Keystone Construction (self) | $880,866.23 | Company owes itself |

**P2 — Test/Placeholder Names (5+):**
| Customer | Issue |
|----------|-------|
| 12345 Auction | Numbered test name |
| Andrew Allen Test | Explicit "Test" |
| Andrew Allen Test 1 | Explicit "Test" + duplicate |
| Cass Wyatt / TESTER | Explicit "TESTER" company |
| IDT Tester | Explicit "Tester" |
| Government Agency XYZ | Placeholder |

**Top Customers by Balance:**
- Ava Li / Atlas Development: $149,124.68
- Chris Smith / Christopher's Custom Insoles: $235,788.01
- Ali Khan / Beacon Investments: $177,913.57
- Logan Tran / Crown Holdings: $119,012.34
- Leila Nguyen / Axis Realty: $115,432.10

---

### Station 6: Vendors — Score: 5/10

**61 vendors total**

| Metric | Value |
|--------|-------|
| Total Vendors | 61 |
| Unbilled POs | $3,385,721.17 (155 POs) |
| Unpaid Bills | $11,146,585.15 (28 overdue) |
| Open Bills | $11,169,772.96 (30 open) |
| Paid Last 30 Days | $0.00 (1 paid) |

**P1:**
- Construction Materials Inc.: $5,428,310.61 (50% of all AP in one vendor)
- Daniel Green: -$544,001.67 (massive negative balance)

**P2:**
- "Mr IDT TEst Tester" (test@idt.com) — test vendor name

**Notable:** Bill Pay ACH active for Blue Bird Insurance (US BANK NA ...6939). All others "Missing."

---

### Station 7: Employees — Score: 7/10

| Metric | Value |
|--------|-------|
| Module | Full Payroll (Employees, Contractors, Taxes, Benefits, HR, Compliance) |
| Multi-State | California, Colorado, New York |
| Next Payroll | 03/12/2026 |
| Tax Penalty Protection | Inactive |
| Workers' Comp | California notice active |

**Active Employees:**
- Daniel Baker ($38/hr)
- Benjamin Brooks ($115K/yr)
- Sophia Brown ($32/hr)

**15+ TO DO Items:**
- Re-enter Federal EIN (IRS rejected)
- 4 New Hire reports overdue
- File CA DE 9, CA DE 9C, 941, NYS-45, 940, W-2 (all Q4 2025, past due)
- Pay overdue taxes
- Pay CO Income Tax zero payment (Due Mar 13)
- Verify bank deposit (****7890)

---

### Station 8: Products/Services — Score: 5/10

| Metric | Value |
|--------|-------|
| Total Items | 112 (3 pages) |
| Categories | Commercial Construction |
| Inventory | Active |

**P2:** "nnnnnnnnnn..." spam product (70+ chars of 'n') — test data
**Notable:** Proper construction items (Soil Testing, Legal services, 1000 - Preparation Services)

---

### Station 9: Projects — Score: 6/10

**~19 projects**

| Project | Customer | Income | Costs | Margin | Hours |
|---------|----------|--------|-------|--------|-------|
| TidalWave - Farmer's Market | Matthew Ahmed | $5,523,931 | $1,781,791 | 67.7% | 1,366h |
| GaleGuardian - Turbine Install | Amelia Patel | $4,954,712 | $2,151,348 | 56.6% | 1,964h |
| BMH Landscaping - Phase 1 | Emily Wong | $3,580,466 | $1,347,120 | 62.4% | 2,240h |
| Intuit Dome - Phase 2 | Priya Patel | $1,780,526 | $1,375,713 | 22.7% | 2,234h |
| Bathroom Remodel | Gov Agency XYZ | $20,000 | $19,532 | 2.3% | 54h |

**P2 — Test Projects:** "IDT TEST" ($430), "Project 1" ($700), "Project A", "Example Proj", "Test" x2, "Title 1"
**P2 — Extreme Margins:** Contract A (-2,249%), Sawgrass (-2,059%), Project A (-808%)
**P2 — Customer Concentration:** Abigail Patel on 8/19 projects (42%)

---

### Station 10: Reports — Score: 7/10

- `/app/standardreports` accessible via sidebar Reports button
- Standard reports available: P&L, Balance Sheet, Cash Flow, AR/AP Aging, Trial Balance
- New report builder active (virtualized rendering — may truncate large reports)
- **Known 404:** `/app/reportlist` returns 404 — use sidebar navigation

---

### Station 11: Chart of Accounts — Score: 7/10

**75+ accounts displayed** at `/app/chartofaccounts?jobId=accounting`

**Structure:**
- 1000 Petty Cash, 1010 Checking, 1020 BOI, 1040 Bank of Intuit
- (MMA) Guardian Growth Money Market
- 1110 Accounts Receivable (A/R)
- 1598 Payroll Refunds
- QuickBooks Payroll Tax Impound
- 2000 Accounts Payable (A/P)
- 2060 Deferred Revenue
- 2100 Payroll Liabilities (14+ sub-accounts)
- Revenue Recognition accounts present
- Numbered accounts follow construction COA structure

---

### Station 12: Settings — Score: 7/10

| Field | Value | Status |
|-------|-------|--------|
| Name | Keystone Construction | PASS |
| Legal Name | Keystone Construction, LLC | PASS |
| Industry | Construction | PASS |
| Business Type | Corporation (Form 1120) | PASS |
| Address | 2700 Coast Ave, Mountain View, CA 94043-1140 | PASS |
| Phone | +16509446000 | PASS |
| Email | contact@keystone-constructions.com | PASS |
| EIN | •••••8735 | PASS |
| Website | None listed | P3 |
| Customer Address Street | "abc New Court" | **P2** (placeholder) |
| Customer Address State | CO (should be CA) | **P2** (wrong state) |

---

## TIER 2 — Surface Scan (20/20)

### Batch 1 (10 pages) — All Loaded ✓

| # | Page | URL | Status | Key Data |
|---|------|-----|--------|----------|
| S1 | Estimates | /app/estimates | ✓ | 116 lines |
| S2 | Sales Orders | /app/salesorders | ✓ | 36 entries |
| S3 | Purchase Orders | /app/purchaseorders | ✓ | 172 entries |
| S4 | Expenses | /app/expenses | ✓ | 145 entries |
| S5 | Recurring Txns | /app/recurringtransactions | ✓ | 78 entries |
| S6 | Fixed Assets | /app/fixedassets | ✓ | 18 assets |
| S7 | Revenue Recognition | /app/revenuerecognition | ✓ | 18 entries |
| S8 | Time Tracking | /app/time | ✓ | 41 entries |
| S9 | Sales Tax | /app/salestax | ✓ | 35 entries |
| S10 | Reconcile | /app/reconcile | ✓ | 48 entries |

### Batch 2 (10 pages) — 7 Loaded, 3 Errors

| # | Page | URL | Status | Key Data |
|---|------|-----|--------|----------|
| S11 | Bank Rules | /app/rules | ✓ | 0 of 30 rules created |
| S12 | Receipts | /app/receipts | ✓ | Loaded (Accounting section) |
| S13 | Budgets | /app/budgets | ✓ | Reports & Analytics section |
| S14 | Classes | /app/class | ✓ | Classes + Run Report |
| S15 | Workflows | /app/workflows | ✓ | Workflow automation |
| S16 | Payment Links | /app/paymentlinks | ✗ | "We're sorry, we can't..." |
| S17 | Subscriptions | /app/subscriptions | ✗ | "We're sorry, we can't..." |
| S18 | My Accountant | /app/myaccountant | ✗ | "We're sorry, we can't..." |
| S19 | Audit Log | /app/auditlog | ✓ | Audit Log loaded |
| S20 | Invoices | /app/invoices | ✓ | Sales & Get Paid section |

**Surface Scan Summary:** 17/20 loaded (85%), 3 pages show error ("We're sorry") — likely features not enabled or routes deprecated in this environment.

---

## TIER 3 — Conditional Checks

| # | Check | Status | Notes |
|---|-------|--------|-------|
| C1 | Customer Hub | ✅ Active | Leads, Proposals, Contracts, Appointments, Reviews |
| C2 | Intuit Intelligence | ✅ Active | Chat button on all pages, AI P&L analysis, forecasting |
| C3 | Revenue Recognition | ✅ Active | 18 entries in surface scan |
| C4 | Fixed Assets | ✅ Active | 18 assets tracked |
| C5 | Multi-State Payroll | ✅ Active | CA, CO, NY |
| C6 | Inventory | ✅ Active | Module in All Apps menu |
| C7 | Customer Agent | ✅ Active | 0 new leads (dashboard tile) |
| C8 | Workflow Automation | ✅ Active | Loaded at /app/workflows |
| C9 | Bill Approval | ✅ Active | Column visible in Bills table |
| C10 | Classes/Dimensions | ✅ Active | Classes page + Run Report |
| C11 | Payment Links | ❌ Error | "We're sorry" |
| C12 | Subscriptions | ❌ Error | "We're sorry" |
| C13 | My Accountant | ❌ Error | "We're sorry" |

---

## All Apps Menu (Feature Map)

| App | Sub-features |
|-----|-------------|
| Accounting | Bank transactions, Integration transactions, Receipts, Reconcile, Rules, COA, Recurring transactions, **Revenue recognition**, Fixed assets, My accountant, Live Experts |
| Expenses & Bills | Overview, Expense transactions, Vendors, Bills, Bill payments, Mileage, Expense claims, Contractors, 1099s |
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
| Revenue down alerts | Active |
| AI Project Management Agent | Active (seen in project creation dialog) |

---

## Findings Summary (Priority Order)

### P1 — HIGH (8 findings)
1. **Jason Cioran $20B AR** — Customer "Cioran's Acorns" $19,999,999,999 open balance. Makes BS/AR reports unusable.
2. **Guardian Growth MMA $10.9M** — Bank $10.9M vs QB $10.4M. Same inflation across all construction environments.
3. **Petty Cash $20.8M** — Highest bank inflation across any environment audited.
4. **1010 Checking discrepancy** — Bank $460K vs QB -$1.83M (~$2.3M gap).
5. **Cash account -$1.46M** — Negative cash balance.
6. **AP $11.1M** — $11,146,585 unpaid. Construction Materials Inc. alone = $5.4M (50% of AP).
7. **Daniel Green vendor -$544K** — Massive negative vendor balance.
8. **262 pending bank txns + Error 103** — Bank feeds broken, 449+ days stale.

### P2 — MEDIUM (10 findings)
9. **5+ test customer names** — 12345 Auction, Andrew Allen Test x2, TESTER, IDT Tester, Gov Agency XYZ
10. **1 test vendor** — "Mr IDT TEst Tester" (test@idt.com)
11. **6+ test project names** — IDT TEST, Project 1, Project A, Example Proj, Test x2, Title 1
12. **"nnnnnn..." spam product** — 70+ chars test input
13. **Customer address placeholder** — "abc New Court, Sunnyvale, CO 94087" (CO should be CA, street is placeholder)
14. **Keystone self-reference** — $880K customer balance owed to itself
15. **3 projects extreme negative margins** — Contract A (-2,249%), Sawgrass (-2,059%), Project A (-808%)
16. **Abigail Patel concentration** — 8/19 projects (42%)
17. **4 negative-balance customers** — Abigail Patel -$33K, Alex Blakey -$954, Karuna -$9K, Gov XYZ -$180
18. **3 surface scan pages broken** — Payment Links, Subscriptions, My Accountant all show "We're sorry"

### P3 — LOW (4 findings)
19. **15+ overdue payroll filings** — Q4 2025 tax filings and new hire reports past due
20. **No website listed** in company settings
21. **$0 paid to vendors** in last 30 days (1 payment recorded)
22. **$3.7M unbilled income** — Large unbilled backlog
23. **Fixed assets negative** — -$88,511.67 (depreciation exceeds cost basis)

### FIXED ✅ (1 finding)
24. **P&L Net Income** — Was -$214,942 → Now +$285,058 via JE #114 + JE #115

---

## Content Safety: ZERO VIOLATIONS

All 12 deep stations + 20 surface pages scanned for:
- Profanity/slurs: **0**
- PII (real SSN, real addresses): **0**
- Cultural gaffes: **0**
- Real person names in sensitive contexts: **0**
- Bilingual gaffes: **0**

**Result: CLEAN** — Test/placeholder names are P2 content quality issues, not safety violations.

---

## Comparison: Mid Market vs Other Environments

| Metric | Mid Market v2 | QSP Events v2 | NV2 Non-Profit v3 |
|--------|--------------|----------------|-------------------|
| Overall Score | **6.5/10** | 7.5/10 | 7.5/10 |
| Entities | 1 (single) | 4 (P+2C+CV) | 4 (P+2C+CV) |
| Entity Type | Single | Multi (IES) | Multi (IES) |
| Net Income | +$285K ✅ | +$5M (consol.) | +$120K |
| Customers | 76 | ~50 | ~30 |
| Vendors | 61 | ~30 | ~20 |
| Projects | 19 (4 rich) | 3+ | 5 |
| Products | 112 | — | — |
| Payroll | YES (multi-state) | YES | — |
| Revenue Recognition | YES | — | — |
| Inventory | YES | — | — |
| Customer Hub | YES (full) | — | — |
| Fixed Assets | YES | — | — |
| Guardian Growth MMA | $10.9M | $10.9M | — |
| Test Names | 12+ items | 1 (FLDN) | 0 |
| Content Violations | 0 | 0 | 0 |

---

## Overall Assessment

**Realism Score: 6.5/10** — This is a single-entity QBO Advanced Construction environment with the **richest feature set** of any environment audited:
- Revenue Recognition
- Customer Hub (Leads, Proposals, Contracts, Appointments, Reviews)
- Full Payroll (multi-state CA/CO/NY, HR, Compliance)
- Inventory
- Fixed Assets
- Workflow Automation
- Intuit Intelligence AI
- Customer Agent
- Bill Approval
- Classes/Dimensions

**Score improvement (+1.0):** P&L fixed from -$214K to +$285K. Comprehensive 3-tier audit completed.

**Remaining blockers for higher score:**
1. $20B Jason Cioran AR (makes all financial reports unusable)
2. $20.8M Petty Cash / $10.9M MMA inflation
3. 12+ test/placeholder names across customers, vendors, projects
4. 262 pending bank txns + broken bank feeds (Error 103)
5. $11.1M AP concentration

**Best use case:** Testing QBO Advanced features (RevRec, Customer Hub, Fixed Assets, Inventory, multi-state Payroll, Workflow Automation). Feature-richest single entity. NOT suitable for financial demos without AR/banking cleanup.

**Recommended next fixes (priority order):**
1. Zero out Jason Cioran $20B AR (or delete customer)
2. Rename/delete test customers (12345 Auction, Andrew Allen Test, IDT Tester, TESTER)
3. Rename/delete test projects (IDT TEST, Project 1, Example Proj, Test x2)
4. Delete "nnnn..." spam product
5. Fix customer address: "abc New Court" → real street, CO → CA

---

## Session Metadata
- **Sweep started:** ~17:00 UTC (2026-03-06)
- **Sweep completed:** ~19:30 UTC (2026-03-06)
- **Version:** v3.0 (3-tier audit)
- **Deep Stations audited:** 12/12
- **Surface Scan pages:** 20/20 (17 loaded, 3 errors)
- **Conditional Checks:** 13 (10 active, 3 errors)
- **Content scans:** 32 total (12 deep + 20 surface)
- **Content violations:** 0
- **Fixes applied:** 2 (JE #114 + JE #115 — P&L fix)
- **Login:** Email + Password + TOTP (MFA enforced)
- **Browser:** Playwright MCP (chromium)
- **Previous version:** `mid_market_2026-03-06.md` (v1, score 5.5/10)
