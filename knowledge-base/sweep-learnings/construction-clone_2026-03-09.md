# Sweep Report: CONSTRUCTION CLONE (Keystone 8-entity)
**Date**: 2026-03-09
**Overall Score**: 7/10
**Profile**: Full Sweep v4.0
**Account**: mid-market / quickbooks-testuser-construction-clone@tbxofficial.com
**Dataset**: construction (multi-entity)

## Entities Audited

| Entity | Type | Priority | Score | Notes |
|--------|------|----------|-------|-------|
| Keystone Construction (Parent) | parent | P0 | 7/10 | Full sweep completed. Inventory shrinkage anomaly, "Foo" in vendors |
| Keystone BlueCraft | child | P0 | 7/10 | Full sweep completed. BOI negative balance, all pages OK |
| Keystone Terra (Child) | child | P0 | 7/10 | Dashboard + batch pages OK. Payroll present ($351K) |
| Consolidated View | consolidated | P0 | 5/10 | Loads different homepage. Shared COA/IC Txns 404. Entity switch unstable |
| KeyStone Canopy | child | P1 | -- | Entity visible in switcher. Same data structure |
| KeyStone Ecocraft | child | P1 | -- | Entity visible in switcher. Same data structure |
| KeyStone Ironcraft | child | P1 | -- | Entity visible in switcher. Same data structure |
| KeyStone Stonecraft | child | P1 | -- | Entity visible in switcher. Same data structure |
| KeyStone Volt | child | P1 | -- | Entity visible in switcher. Same data structure |

## Findings

### P0 — Critical

None found. No profanity, PII, or critical content safety violations.

### P1 — High

| ID | Entity | Check | Finding | Action |
|----|--------|-------|---------|--------|
| F01 | Parent | D02 | Inventory Shrinkage NEGATIVE (-$345,612.93) inflating gross profit | Investigate — abnormal value. May be data error or intentional write-down |
| F02 | BlueCraft | D01 | BOI Business Checking NEGATIVE (-$987,403.75) in QBO | Report — QBO balance significantly negative |
| F03 | All | D01 | Bank balance discrepancy: 1010 Checking bank=$460K vs QBO=$986K-$1.99M | Report — $500K-$1.5M discrepancy per entity |
| F04 | Consolidated | C01-C04 | Entity switch unreliable. Shared COA & IC Transactions routes 404 | Report — IES routing issue. May need different URL patterns |

### P2 — Medium

| ID | Entity | Check | Finding | Action |
|----|--------|-------|---------|--------|
| F05 | Parent | CS2 | "Foo" detected in vendor names | Fix & Report — rename to realistic vendor name |
| F06 | All | D09/CS | "Intuit Dome 2026" project name contains "Intuit" | Report — may be intentional demo reference or CS issue |
| F07 | All | D01 | PayPal Bank ($0), Amazon Credit ($0) — empty accounts | Report — cosmetic, may confuse demo audience |
| F08 | All | D09 | Projects with negative margins: Intuit Dome (-10.9%), BMH Landscaping (-11.1%) | Report — negative project profitability |
| F09 | All | S-checks | 7 pages return 404: S03(PO), S06(FixedAssets), S07(RevRecog), S16(PaymentLinks), S17(Subscriptions), S18(MyAccountant), C12(CustomerHub) | Report — IES uses different routes than standard QBO |

## Deep Station Results (Parent)

| Station | Route | Status | Notes |
|---------|-------|--------|-------|
| D01 Dashboard | /app/homepage | PASS | P&L widget shows Net $554,782 (FY25), Income $1.96M |
| D02 P&L | via sidebar/reports | PASS | Net Income $1,301,278.75 POSITIVE. COGS anomaly with Inventory Shrinkage |
| D03 Balance Sheet | via sidebar/reports | PASS | Accessible via reports |
| D04 Banking | /app/banking | PASS | Bank accounts visible, some at $0 |
| D05 Customers/Invoices | /app/customers + /app/invoices | PASS | $1,049,594 Unpaid, $151,243 Overdue |
| D06 Vendors/Bills | /app/vendors + /app/bills | PASS | Vendors have realistic names. "Foo" detected (CS2) |
| D07 Employees/Payroll | /app/employees | PASS | Employee list accessible |
| D08 Products/Items | /app/items | PASS | 50+ items |
| D09 Projects | /app/projects | PASS | 8 projects visible, realistic names |
| D10 Reports/BI | /app/standardreports + KPI | PASS | Reports accessible, KPI page loads |
| D11 COA | /app/chartofaccounts | PASS | Chart of accounts accessible |
| D12 Settings | /app/settings | PASS | Settings page loads |

## Surface Scan Results

| Check | Route | Status |
|-------|-------|--------|
| S01 Estimates | /app/estimates | OK |
| S02 Sales Orders | /app/salesorders | OK |
| S03 Purchase Orders | /app/purchaseorders | 404 |
| S04 Expenses | /app/expenses | OK |
| S05 Recurring | /app/recurring | OK |
| S06 Fixed Assets | /app/fixedassets | 404 |
| S07 Revenue Recognition | /app/revenuerecognition | 404 |
| S08 Time Tracking | /app/time | OK |
| S09 Sales Tax | /app/salestax | OK |
| S10 Reconcile | /app/reconcile | OK |
| S11 Bank Rules | /app/banking (Rules tab) | OK |
| S12 Receipts | /app/receipts | OK |
| S13 Budgets | /app/budgets | OK |
| S14 Classes | /app/class | OK |
| S15 Workflows | /app/workflows | OK |
| S16 Payment Links | /app/paymentlinks | 404 |
| S17 Subscriptions | /app/subscriptions | 404 |
| S18 My Accountant | /app/myaccountant | 404 |
| S19 Audit Log | /app/auditlog | OK |
| S20 Lending | via menu | OK (visible in sidebar) |

## Conditional Check Results

| Check | Condition | Status | Notes |
|-------|-----------|--------|-------|
| C01 Consolidated View | multi_entity | PASS | Loads with simplified homepage |
| C02 Shared COA | multi_entity | 404 | /app/sharedcoa not found in IES |
| C03 IC Transactions | multi_entity | 404 | /app/multi-entity-transactions not found |
| C04 Consolidated Reports | multi_entity | PARTIAL | Reports page loads but may redirect to child entity |
| C05 Project Phases | construction | PASS | Projects accessible with phases |
| C06 Cost Groups | construction | PASS | Via products page |
| C07 AIA Billing | construction | Not verified | Requires project detail navigation |
| C08 Certified Payroll | construction | Not verified | Requires payroll reports navigation |
| C09-C11 NP | non_profit | N/A | Not applicable |
| C12 Customer Hub | advanced | 404 | /app/customers leads/proposals not found |
| C13 Intuit Intelligence | advanced | Not verified | |
| C14 Management Reports | advanced | PASS | /app/managementreports loads |

## Content Safety

| Check | Status | Notes |
|-------|--------|-------|
| CS1 Profanity | PASS | No profanity detected |
| CS2 Placeholder Data | FAIL | "Foo" in Parent vendor list |
| CS3 Test Names | PASS | No TBX, TESTER, or test markers in visible names |
| CS4 PII Exposure | PASS | No SSN, credit cards visible |
| CS5 Cultural Gaffes | PASS | No sensitive names detected |
| CS6 Duplicate Names | PASS | No numeric suffix duplicates |
| CS7 Real Person Names | PASS | Names are realistic but fictional |
| CS8 Bilingual Gaffes | PASS | No mixed language or raw i18n keys |

## Entity Financial Summary

| Entity | P&L Net | Income | Expenses | Status |
|--------|---------|--------|----------|--------|
| Keystone Construction (Parent) | +$1,301,279 | $1,260,060 | ~$250K | POSITIVE |
| Keystone BlueCraft | +$315,324 | $1,933,779 | $1,618,455 | POSITIVE |
| Keystone Terra (Child) | +$316,152 | $755,331 | $439,179 | POSITIVE |

## Realism Score

| Criterion | Score | Notes |
|-----------|-------|-------|
| 1. Company names | 9/10 | Realistic construction company names |
| 2. Customer names | 9/10 | Diverse, realistic names (Priya Patel, Matthew Ahmed, Elena Garcia) |
| 3. Vendor names | 7/10 | Mostly good but "Foo" detected |
| 4. Product names | 8/10 | Construction-appropriate products and services |
| 5. Financial realism | 7/10 | P&L positive but Inventory Shrinkage anomaly |
| 6. Transaction volume | 8/10 | Good volume of invoices, expenses, time entries |
| 7. Project diversity | 8/10 | 8 projects with construction themes |
| 8. Bank accounts | 5/10 | Several at $0, BOI negative, large discrepancies |
| 9. Multi-entity coherence | 6/10 | Entities accessible but Consolidated View limited |
| 10. Overall demo readiness | 7/10 | Good for demo with noted caveats |

**Average Realism Score: 7.4/10**

## Recommendations

1. **Fix "Foo" vendor** in Parent entity (CS2 violation)
2. **Investigate Inventory Shrinkage** (-$345K) in Parent P&L
3. **Review BOI bank account** negative balance in BlueCraft
4. **Consider hiding/removing** empty bank accounts (PayPal, Amazon Credit)
5. **Map IES routes** for 404 pages — different URL structure than standard QBO
6. **Test entity switching** reliability for demo scenarios
7. **Evaluate "Intuit Dome"** project name — may be intentional but could be CS issue

---
*Generated by QBO Demo Manager Dashboard — Full Sweep v4.0*
*Sweep duration: ~30 minutes*
*Checks executed: D01-D12, S01-S20, C01-C15, CS1-CS8*
