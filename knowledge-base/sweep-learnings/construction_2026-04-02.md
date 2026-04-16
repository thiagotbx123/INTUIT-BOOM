# QBO Sweep Report — Mid-Market Construction (Single Entity)
## Keystone Construction | 2026-04-02

---

## Executive Summary

| Field | Value |
|-------|-------|
| Account | mid_market@tbxofficial.com |
| Shortcode | mid-market |
| Dataset | construction |
| Profile | God Complete v8.0 |
| Entity | Keystone Construction (single, CID: 9341452713218633) |
| Sweep Date | 2026-04-02 |
| Screens Swept | 46/46 (T01-T46) |
| Overall Score | **5.5/10** |
| Realism Score | **38/100** |

### Score Rationale
- Single-entity QBO Advanced account with payroll, projects, inventory, budgets, custom fields, and fixed assets enabled
- P&L shows $688K net income on $1.075M revenue with 64% net margin — far above construction benchmark of 3-15%
- COGS is only $78 on $1M+ revenue (0.007%) — catastrophically unrealistic for construction (should be 40-85%)
- Balance sheet inflated to $7.69B total assets, driven by $7.66B AR from historical test data accumulation
- Bank feeds broken (Error 103 on both accounts since Dec 2024), never reconciled
- 64 overdue sales tax returns, 100% overdue bills, 96.6% overdue invoices
- Multiple CS3 violations: {name} placeholder, "Alan Somebody", "Test Testerson", "Mrs Marge Simpson", @tbxofficial.com emails, test class names
- Strong positives: 21 active projects, 29 contractors, 120 products/services, 11 fixed assets, 8 budgets, rich custom fields

---

## Financial Summary

### Profit & Loss (Jan 1 - Apr 2, 2026, Accrual)

| Line | Amount |
|------|--------|
| Total Income | $1,075,066.93 |
| 4000 Sales | $1,073,728.05 (99.9%) |
| Total COGS | **$78.43** |
| Gross Profit | $1,074,988.50 |
| Gross Margin | **99.99%** (benchmark: 15-60%) |
| Total Expenses | $457,837.46 |
| Payroll Expenses | $420,657.65 (91.9% of expenses) |
| Net Operating Income | $617,151.04 |
| Other Income (incl. Late Fees) | $82,098.58 |
| Net Income | **$688,741.01** |
| Net Margin | **64.07%** (benchmark: 3-15%) |

### Balance Sheet (As of Apr 2, 2026, Accrual)

| Line | Amount |
|------|--------|
| Total Assets | **$7,693,647,920.33** |
| Accounts Receivable | **$7,660,424,364.95** |
| Bank Accounts | $27,948,904.55 |
| Petty Cash | **$20,840,442.88** |
| Checking (1010) | -$1,972,421.78 (bank: $460K) |
| (MMA) Guardian Growth | $10,398,418.37 (bank: $10.9M) |
| Fixed Assets (net) | -$92,014.54 |
| Total Liabilities | $11,594,631.64 |
| Accounts Payable | $9,876,243.89 |
| Total Equity | $7,682,053,288.69 |
| Retained Earnings | $7,671,074,739.85 |
| A = L + E | **Balanced** |

---

## Findings by Severity

### P0 — Critical (Demo-Breaking)

| # | Screen | Finding |
|---|--------|---------|
| 1 | T02 P&L | COGS $78 on $1.075M revenue (0.007%). Construction COGS should be 40-85%. |
| 2 | T02 P&L | Gross margin 99.99% — construction benchmark 3-15%. |
| 3 | T02 P&L | Net margin 64% — way above construction typical 3-15%. |
| 4 | T03 BS | AR = $7.66 BILLION — catastrophically inflated from historical test data. |
| 5 | T03 BS | Retained Earnings = $7.67B mirrors inflated AR. Never cleaned. |
| 6 | T04 Banking | Error 103 on BOTH bank accounts — connections broken since 12/11/2024. |
| 7 | T04 Banking | 257 pending transactions in Checking — massive uncategorized backlog. |
| 8 | T04 Banking | Bank says $460K but QBO says -$1.97M for Checking — $2.43M discrepancy. |
| 9 | T01 Dashboard | Overdue ratio: $537K not paid vs $20.7K paid (96% unpaid). |
| 10 | T10 Invoices | $940K overdue (96.6% of unpaid). Almost nothing being collected. |
| 11 | T06 Vendors | 35 overdue bills totaling $11.36M = 100% overdue rate. |
| 12 | T14 COA | Petty Cash = $20.8M — absurdly high for petty cash. |
| 13 | T19 Sales Tax | 64 overdue sales tax returns ($2,087.45) — massive compliance failure. |
| 14 | T36 Inventory | ALL products show COS $0 and Gross Profit $0 — zero cost tracking. |

### CS3 — Customer Story Violations (Placeholder/Test Data)

| # | Screen | Finding |
|---|--------|---------|
| 1 | T01 Dashboard | Referral widget shows `{name}` placeholder — template variable not rendered. |
| 2 | T05 Customers | "Alan Somebody" = test/placeholder customer name. |
| 3 | T05 Customers | Multiple customers with 555-666-7777 = fake phone numbers. |
| 4 | T06 Vendors | Multiple vendors use @tbxofficial.com emails (TBX marker). |
| 5 | T09 Projects | "Patio and Deck for Customer" has customer = "Keystone Construction" (self-referencing). |
| 6 | T10 Invoices | "Mrs Marge Simpson" — fictional character name used as customer. |
| 7 | T17 Contractors | "Test Testerson" — obvious test/placeholder contractor name. |
| 8 | T18 Time | "Alan Somebody" appears again in time entry. |
| 9 | T24 Classes | Classes "2", "3", "Test 1" — test/placeholder class names. |

### P1 — High Priority

| # | Screen | Finding |
|---|--------|---------|
| 1 | T01 Dashboard | No Income/Expense/Net Profit/Bank Balance widgets — only Sales funnel visible. |
| 2 | T02 P&L | No subcontractor expenses visible — unusual for construction. |
| 3 | T02 P&L | Revenue 99.87% in single 4000 Sales account — no breakdown. |
| 4 | T02 P&L | Late Fee Income = 7.6% of revenue — very high. |
| 5 | T03 BS | Negative bank balances: Checking (-$1.97M), Cash (-$1.46M). |
| 6 | T03 BS | Fixed Assets fully depreciated to -$92K net — no positive value. |
| 7 | T04 Banking | Bank feeds not updated for ~4 months. |
| 8 | T05 Customers | 33 overdue invoices ($940K) — high overdue ratio. |
| 9 | T05 Customers | $3.69M unbilled income. |
| 10 | T06 Vendors | 157 unbilled POs ($3.45M) — large backlog. |
| 11 | T09 Projects | 3 projects with deeply negative margins (-808% to -2113%). |
| 12 | T12 Expenses | Purchase Order amounts extremely repetitive — same amounts every 2-5 days. |
| 13 | T13 Estimates | Estimate amounts ($11-$3,575) trivially small for multi-million-dollar construction company. |
| 14 | T13 Estimates | Only 1 accepted estimate in 12 months — extremely low conversion. |
| 15 | T14 COA | QB vs bank discrepancies: Checking ($460K vs -$1.97M), MMA ($10.9M vs $10.4M). |
| 16 | T15 Settings | Business type "Corporation (Form 1120)" conflicts with LLC legal name. |
| 17 | T16 Payroll | Payroll tax setup incomplete — 2 tasks pending. |
| 18 | T16 Payroll | Tax Penalty Protection is Inactive. |
| 19 | T18 Time | Time entry shows 168.95 hours for a 57-minute session. |
| 20 | T19 Sales Tax | 6 returns "ready to file" but not filed. |
| 21 | T20 Recurring | Weekly recurring PO ($3,719.17) explains repetitive expense pattern. |
| 22 | T26 Custom Fields | Invoice custom fields at 12/12 — limit reached. |
| 23 | T30 Reconciliation | No reconciliation history — accounts never reconciled. |
| 24 | T34 POs | Highly repetitive PO pattern — same 3 vendors/amounts rotating every 2-3 days. |

### P2 — Medium Priority

| # | Screen | Finding |
|---|--------|---------|
| 1 | T02 P&L | Office Expenses = -$100 (negative). Employee retirement = -$5. |
| 2 | T03 BS | Uncategorized Asset = $4.81M. Lines of credit negative. |
| 3 | T04 Banking | Only 2 of 6 bank accounts connected to feeds. |
| 4 | T05 Customers | "Blakeys Bin Liners" — non-construction customer. |
| 5 | T06 Vendors | Email mismatch: Concrete Solutions uses @concretedepot.com. |
| 6 | T07 Employees | All employees Paper check — no direct deposit. |
| 7 | T07 Employees | Davis, Olivia at $350K/year — very high. |
| 8 | T08 Products | Duplicate item numbers 1100 and 1209. |
| 9 | T09 Projects | Generic names: "Project 1", "Contract A/B/C", "Title 1", "lot clearing". |
| 10 | T09 Projects | 7 of 21 projects have zero income and zero costs. |
| 11 | T09 Projects | "Melissa's Press Fleet Q1" not construction-related. |
| 12 | T10 Invoices | Invoice numbers machine-generated (20250212100XXX). |
| 13 | T10 Invoices | "Oreilly Auto" — unlikely construction customer. |
| 14 | T11 Bills | All 14 unpaid bills overdue — zero on-time payments in 2026. |
| 15 | T12 Expenses | PO numbers use "TBX-2025" prefix — system-generated. |
| 16 | T13 Estimates | Abigail Patel in 7+ of 15 estimates — over-represented. |
| 17 | T14 COA | "Bank of Intuit" — fictional bank name. |
| 18 | T15 Settings | Customer address "ABC New Court" — placeholder. |
| 19 | T15 Settings | Customer address state "CO" with CA ZIP 94087. |
| 20 | T15 Settings | Website "None listed" — incomplete for demo. |
| 21 | T17 Contractors | "Contractor's Warehouse" missing W-9. |
| 22 | T19 Sales Tax | Sales tax accruing only $1.30 on $1M+ revenue. |
| 23 | T20 Recurring | "1234 Auction" — test template with $0 amount. |
| 24 | T21 Fixed Assets | "Client Car" at $120K — unusual naming. 7/11 fully depreciated. |
| 25 | T23 Budgets | Generic sequential budget names (P&L_3 through P&L_8). |
| 26 | T24 Classes | "Amazon" as a class — not construction-related. |
| 27 | T25 Workflows | No workflows configured. |
| 28 | T26 Custom Fields | "Tester" custom field — test name. |
| 29 | T43 Audit Log | Timestamps in "Brasilia Standard Time" — inconsistent with CA company. |

---

## Positive Highlights

| # | Screen | Finding |
|---|--------|---------|
| 1 | T07 Employees | Realistic, diverse employee names. No test/placeholder names. |
| 2 | T08 Products | 120 construction-specific products/services with categories. |
| 3 | T09 Projects | Good mix of residential, commercial, civil, government construction projects. |
| 4 | T09 Projects | Time tracking active with realistic hour counts (2000+ on major projects). |
| 5 | T11 Bills | Vendor names construction-appropriate (structural, masonry, security). |
| 6 | T12 Expenses | Construction-appropriate vendors: Landscaping, Lumber, Concrete. |
| 7 | T14 COA | Well-numbered COA with 1000-series structure. |
| 8 | T15 Settings | Industry correctly set to Construction. Logo present. |
| 9 | T17 Contractors | 29 contractors with diverse construction trade names. |
| 10 | T21 Fixed Assets | Construction-appropriate assets (Crane, Forklift, Excavation Trailer). |
| 11 | T23 Budgets | Active budgets with class and customer subdivisions. |
| 12 | T26 Custom Fields | Rich construction fields (Tonnage, Workers Comp Code, Claims). |

---

## Feature Coverage Summary

| Feature | Status | Notes |
|---------|--------|-------|
| Dashboard | Active | Missing financial widgets |
| P&L / Balance Sheet | Active | Inflated, unrealistic margins |
| Banking | **BROKEN** | Error 103, not updated since Dec 2024 |
| Customers | Active | 33 overdue, CS3 names |
| Vendors | Active | 100% overdue, CS3 emails |
| Employees | Active | 11+ employees, payroll active |
| Products/Services | Active | 120 items, well-categorized |
| Projects | Active | 21 projects with time tracking |
| Invoices | Active | 45 invoices, 96.6% overdue |
| Bills | Active | 14 unpaid, all overdue |
| Expenses | Active | 50+ transactions, POs |
| Estimates | Active | 15 estimates, low conversion |
| Chart of Accounts | Active | 75+ accounts, well-numbered |
| Company Settings | Complete | Logo, address, industry set |
| Payroll | Active | Tax setup incomplete |
| Contractors | Active | 29 contractors, 2 missing W-9 |
| Time Tracking | Active | Bug: incorrect hours |
| Sales Tax | **CRITICAL** | 64 overdue returns |
| Recurring Transactions | Active | 5 templates |
| Fixed Assets | Active | 11 assets with depreciation |
| Budgets | Active | 8+ budgets |
| Classes | Active | CS3 test names mixed in |
| Workflows | Empty | Not configured |
| Custom Fields | Active | Invoice fields at limit (12/12) |
| Reconciliation | **NEVER DONE** | Zero history |
| Purchase Orders | Active | 157 open POs |
| Inventory | Active | COS tracking broken ($0) |
| Audit Log | Active | Multiple users |

---

## Recommended Remediation Priority

### Immediate (before any demo)
1. Clean AR: Delete/void historical test invoices driving $7.66B AR
2. Fix COGS: Add cost amounts to products/services so P&L shows realistic construction margins
3. Fix bank connections (Error 103) or remove stale connected accounts
4. Rename CS3 items: "Alan Somebody", "Test Testerson", "Mrs Marge Simpson", {name} template, test classes
5. File or clear 64 overdue sales tax returns

### High Priority
6. Add subcontractor expenses to P&L
7. Reconcile bank accounts at least once
8. Complete payroll tax setup (2 remaining tasks)
9. Fix time entry hours bug (168.95h for 57-minute session)
10. Diversify estimates with larger, construction-realistic amounts

### Medium Priority
11. Clean up generic project names ("Project 1", "Contract A/B/C", "Title 1")
12. Remove or rename test custom field ("Tester")
13. Replace @tbxofficial.com vendor emails with realistic domains
14. Add company website to settings
15. Fix customer address state mismatch (CO vs CA)
16. Configure at least 1-2 workflow automations

---

*Report generated: 2026-04-02 | Sweep agent: automated | 46 screens | Entity: Keystone Construction (9341452713218633)*
