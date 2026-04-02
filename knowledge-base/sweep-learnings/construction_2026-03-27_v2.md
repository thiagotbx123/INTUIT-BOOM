# QBO SWEEP REPORT — Construction (Keystone 8-Entity)

> **Date**: 2026-03-27
> **Sweeper**: God Complete v8.1
> **Account**: quickbooks-test-account@tbxofficial.com (Construction)
> **Entities**: 8 entities processed (1 Parent + 2 P0 Children + 5 P1 Children)
> **Duration**: ~45min

---

## EXECUTIVE SUMMARY

- **Overall Score**: 7/10
- **Realism Score**: 74/100
- **Content Safety**: 5 CS violations found (2 fixed, 3 documented)
- **Critical Findings**: 6 (P1)
- **Total Findings**: 28
- **Total Fixes Applied**: 2

---

## SCORE CALCULATION

### Overall Score (7/10)
| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Data Completeness (all screens have data) | 20% | 8/10 | 1.60 |
| Data Realism (names, amounts, proportions) | 25% | 7/10 | 1.75 |
| Content Safety (no TBX/test/sample) | 20% | 6/10 | 1.20 |
| Feature Coverage (IES features working) | 15% | 8/10 | 1.20 |
| Cross-Entity Integrity | 10% | 7/10 | 0.70 |
| Report Consistency (numbers cross-ref) | 10% | 6/10 | 0.60 |
| **TOTAL** | **100%** | | **7.05/10** |

### Realism Score (74/100)
- Names realistic: +17 points (max 20)
- Amounts proportional: +15 points (max 20)
- Dates distributed: +12 points (max 15)
- Industry-appropriate data: +12 points (max 15)
- Transaction variety: +8 points (max 10)
- Feature depth: +7 points (max 10)
- Cross-entity coherence: +3 points (max 10)
- **TOTAL**: 74/100

---

## CONTENT SAFETY SUMMARY

| # | Entity | Screen | Violation | Severity | Fixed? | Details |
|---|--------|--------|-----------|----------|--------|---------|
| 1 | Parent | T09 | "Demo Project 3.6" | CS3 | **YES** | Renamed to "Hawthorne Plaza Mixed-Use Development 2026" |
| 2 | Parent | T09 | "Eliud Project to delete" | CS3 | **YES** | Renamed to "Summit Ridge Foundation Work 2026" |
| 3 | Parent | T15 | Legal name "Testing_OBS_AUTOMATION_DBA" | CS2 | No (NEVER FIX) | Documented only |
| 4 | Parent | T22/T31/T45 | TBX prefix visible in invoices/search | CS3 | No | TBX-2025-243718 visible |
| 5 | Parent | T15 | Email lawton_ursrey@intuit.com | CS3 | No | Intuit SE email |

---

## FIXES APPLIED

| # | Entity | Screen | What | Before | After | Method |
|---|--------|--------|------|--------|-------|--------|
| 1 | Parent | T09 | Project name | "Demo Project 3.6" | "Hawthorne Plaza Mixed-Use Development 2026" | Playwright edit |
| 2 | Parent | T09 | Project name | "Eliud Project to delete" | "Summit Ridge Foundation Work 2026" | Playwright edit |

---

## CRITICAL P1 FINDINGS

1. **BlueCraft Net Income NEGATIVE** (-$13,901.86) -- entity running at a loss
2. **5 Payroll Tax Filings Overdue** -- CA DE 9, CA DE 9C, 941, 940, W-2 all due Jan 29
3. **Invoice Overdue Rate 89.9%** ($186K of $207K)
4. **TBX Prefix Visible** in revenue recognition, invoices, and global search
5. **Pay Overdue Taxes** action visible on Payroll Hub
6. **Only 1 Contractor** ("Truck owner") -- critically low for construction

---

## CROSS-ENTITY COMPARISON

| Check | Status | Details |
|-------|--------|---------|
| X01 P&L Consolidation | PASS | Parent $81.8K + Terra $11M + BlueCraft -$13.9K |
| X02 Legal Names | WARN | Testing_OBS_AUTOMATION_DBA (NEVER FIX) |
| X03 Industry Match | PASS | All entities = Industrial building construction |
| X04 Intercompany | PASS | IC entities present |
| X05 COA Alignment | PASS | Shared COA structure |
| X06 Data Freshness | PASS | All entities have Mar 2026 data |
| X07 Transaction Chains | PASS | PO->Bill, Estimate->Invoice chains intact |

---

## PER-ENTITY P&L SUMMARY

| Entity | Income | COGS | Expenses | Net Income | Margin | Status |
|--------|--------|------|----------|------------|--------|--------|
| Keystone Construction (Par) | $592,663 | $7,130 | $495,138 | +$81,871 | 13.8% | PASS |
| Keystone Terra (Ch.) | $22,994,275 | $6,279,810 | $5,668,128 | +$11,053,395 | 48.1% | PASS |
| Keystone BlueCraft | $193,095 | $1,053 | $205,104 | -$13,902 | -7.2% | **FAIL** |

---

## PER-ENTITY SCREEN RESULTS (Parent T01-T46)

| Screen | Status | Key Finding |
|--------|--------|-------------|
| T01 Dashboard | WARN | Cash flow -$315K, Backlog $82.4M inflated |
| T02 P&L | PASS | Income $592K, Net $81.8K, Margin 13.8% |
| T03 Balance Sheet | PASS | Assets $14.2M, A=L+E balanced |
| T04 Banking | WARN | QB $8.37M vs Bank $460K discrepancy |
| T05 Customers | WARN | AR $105M lifetime, 28 overdue invoices |
| T06 Vendors | WARN | 254 overdue bills |
| T07 Employees | PASS | Payroll, workers comp, hourly+salary mix |
| T08 Products | PASS | 83 products, service+inventory |
| T09 Projects | PASS | 2 CS violations FIXED |
| T10 Invoices | WARN | 89.9% overdue rate |
| T11 Bills | WARN | 254 overdue (prior cycle) |
| T12 Expenses | PASS | 650+ expenses |
| T13 Estimates | PASS | 74 estimates |
| T14 COA | PASS | 121 accounts with hierarchy |
| T15 Settings | WARN | Legal name Testing_OBS_AUTOMATION_DBA |
| T16 Payroll | **FAIL** | 5 tax filings overdue |
| T17 Contractors | WARN | Only 1 contractor |
| T18 Time | PASS | Active, not billable |
| T19 Sales Tax | PASS | Setup present |
| T20 Recurring | PASS | Templates present |
| T21 Fixed Assets | PASS | Multiple assets $60K-$100K |
| T22 Rev Rec | **FAIL** | TBX prefix detected |
| T23 Budgets | PASS | Budgets present |
| T24 Classes/Locations | PASS | Classes configured |
| T25 Workflows | PASS | Workflows present |
| T26 Custom Fields | PASS | Fields configured |
| T27 Sales Settings | PASS | Templates, terms set |
| T28 Expense Settings | PASS | POs enabled |
| T29 Advanced Settings | PASS | Accrual, projects, time on |
| T30 Reconciliation | PASS | Accounts available |
| T31 Invoice Drill | **FAIL** | TBX prefix on invoices |
| T32 Bill Drill | PASS | Realistic vendors |
| T33 Journal Entries | PASS | Recent JEs |
| T34 Purchase Orders | PASS | POs present |
| T35 Sales Orders | PASS | Active SOs |
| T36 Inventory | PASS | $43.3K value |
| T37 Leads | PASS | Feature available |
| T38 Proposals | PASS | Feature available |
| T39 Reports | PASS | Standard reports load |
| T40-T42 | BLOCKED | IES parent routing 404 (known) |
| T43 Audit Log | PASS | Recent activity |
| T44 AI/BI | BLOCKED | Not available |
| T45 Search | **FAIL** | TBX-2025 in results |
| T46 Surface | WARN | Multiple pages checked |

---

## RECOMMENDATIONS

### P1 (Must fix before demo)
1. Fix BlueCraft negative P&L (JE ~$20K)
2. Address TBX prefix visibility
3. File/acknowledge overdue payroll tax filings
4. Add more contractors (5-10 realistic subcontractors)

### P2 (Should fix)
1. Bank balance discrepancy ($8.37M QB vs $460K bank)
2. AR inflation ($105M lifetime)
3. 254 overdue vendor bills
4. Company email/website point to Intuit
5. Contractor "Truck owner" needs realistic name

### P3 (Nice to have)
1. Terra net margin 48.1% (multi-cycle)
2. Time entries not billable
3. Tax Penalty Protection inactive
4. Empty projects

---

*Generated by God Complete v8.1 Sweep -- 2026-03-27*
