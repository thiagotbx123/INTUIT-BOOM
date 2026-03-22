# Sweep Report: MID MARKET (Construction single-entity)

**Date:** 2026-03-16
**Account:** mid-market
**Entity:** Keystone Construction (CID: 9341452713218633)
**Dataset:** construction
**Profile:** Full Sweep v5.5 Release Coverage
**Type:** Single entity

---

## EXECUTIVE SUMMARY

**Overall Score: 6/10 (Moderate — Functional with Data Quality Gaps)**

Keystone Construction presents as a $1M+ revenue construction company with 20 projects, 112 products, 51 customers, 50 vendors, and active payroll. The core accounting backbone (P&L, BS, Banking, CoA) functions but has significant data quality issues: $7.66B AR inflation from prior cycles, multiple placeholder project names, negative bank balances, and missing construction-specific features (Change Orders, Cost Groups). The environment is demo-ready for general QBO features but falls short for construction-specific demonstrations.

---

## DEEP STATIONS (D01-D12)

### D01 — Dashboard
- **Status:** PASS
- Company: Keystone Construction
- Income: ~$298K (dashboard widget)
- Bank: $11.3M (MMA Guardian Growth)
- AI Financial Summary: Present in Business Feed
- No placeholders detected

### D02 — Profit & Loss
- **Status:** PASS with concerns
- Income: $1.07M | Expenses: $250K | Net: +$818K
- **Margin: 76.5%** — HIGH for construction (expected 3-15%)
- COGS: Only $78 (negligible despite inventory products existing)
- Revenue diversity needs verification

### D03 — Balance Sheet
- **Status:** WARN
- Bank total: ~$28M
- **AR: $7.66B** — INFLATED artifact from prior dataset cycles (known, not fixable via DB)
- AP: $9.88M
- Negative balances: Checking -$1.84M, Cash -$1.46M
- Uncategorized Asset: $4.81M

### D04 — Banking
- **Status:** WARN
- 1010 Checking: 257 pending transactions
- MMA Guardian Growth: $10.9M
- **Stale feed:** Last updated 12/11/2024
- Categorization: BLOCKED (Post dialog not appearing)

### D05 — Customers
- **Status:** WARN
- 51 customers, 35 open invoices ($1.91M)
- **CS issues:** "Alan Somebody" (placeholder), "FLDN" (abbreviation), "Blakey's Bin Liners" (non-construction)

### D06 — Vendors
- **Status:** PASS
- 50 vendors, construction-appropriate supply chain
- Minor gaps: Some missing company name and phone fields

### D07 — Employees
- **Status:** PASS
- Payroll module: Active with full suite
- Employee details: Not extractable (embedded UI)

### D08 — Products & Services
- **Status:** PASS
- 112 products across 3 pages
- Types: Service (~57), Inventory (~22), Non-Inventory, Bundle (~5)
- Categories well-organized: 1000-Preparation, 2000-Excavation, 3000-Supplies, 4000-Safety, 5000-Work Site, 7000-Bundles
- **Issues:**
  - "1 hr", "2 hrs", "3 hrs" — generic time items
  - "4x4 post" — generic item
  - "1209 Paralegal Services" price=$0
  - "1100 Lot Clearing" price=$0.70 (unrealistic)
  - CS8: "Jonathan Scott (Partner)", "Harrison Scott (Paralegal)" in descriptions

### D09 — Projects
- **Status:** WARN
- 20 projects total
- Good projects: "BMH Landscaping - Phase 1" ($3.58M, 62.4%), "GaleGuardian | Turbine Installation" ($4.95M, 56.6%), "Intuit Dome - Phase 2" ($1.78M, 22.7%)
- **Critical issues:**
  - Placeholder names: "Test" (x2), "Example Proj", "IDT TEST", "Project 1", "Project A", "Title 1", "lot clearing" (lowercase)
  - "Patio and Deck for Customer" — "for Customer" placeholder
  - Negative margins: Contract A (-2,249%), Sawgrass (-2,060%), Project A (-809%)
  - **CS8:** "Intuit Dome" is a real venue (LA Clippers)
  - Duplicate: "Sawgrass residence" appears twice

### D10 — Reports
- **Status:** PASS
- Full report suite: P&L (multiple variants), BS, AR Aging, Cash Flows, Budget, Forecasts, Fixed Assets
- Custom reports, Management reports, KPIs (new), Dashboards (new), Spreadsheet sync available

### D11 — Chart of Accounts
- **Status:** WARN
- 75 accounts (page 1 of unknown)
- Construction-appropriate numbering (1000-series)
- **Issues:**
  - Petty Cash: $20.8M (unrealistically high)
  - Checking: -$1.84M (negative)
  - Cash: -$1.46M (negative)
  - Uncategorized Asset: $4.81M
  - "Bank of Intuit" — platform name as bank

### D12 — Settings
- **Status:** PASS
- Company: Keystone Construction, LLC
- Industry: Construction
- Address: 2700 Coast Ave, Mountain View, CA 94043
- EIN: •••••8735 | Business type: Corporation (Form 1120)
- **Issues:**
  - Customer address: "ABC New Court, Sunnyvale, CO 94087-3204" — "CO" should be "CA", "ABC" looks placeholder
  - Website: None listed

---

## SURFACE SCAN (S01-S46)

```
[S01-S06] ✓✓⚠⚠✓✓ (S03 PO warn placeholder, S04 Expenses warn placeholder)
[S07-S12] ✓✓✓✓✓✓
[S13-S18] ✓✓✓✗✗✓ (S16 Payment Links 404-IES, S17 Subscriptions 404-IES)
[S19-S24] ✓—✓✓✓—  (S20 Lending via menu, S24 Quick Create skipped)
[S25-S30] ✗✓✓✗✓✓  (S25 Custom Forms 404-IES, S28 Cash Flow 404-IES)
[S31-S36] ✓✓✓✓✓✓
[S37-S42] ✗✓✓———  (S37 Expense Claims 404-IES, S40-S42 UI interaction skipped)
[S43-S46] ——✓✗     (S43-S44 skipped, S46 Dashboards 404)
```

**404s (expected on IES):** S16, S17, S25, S28, S37
**404s (unexpected):** S46 Analytics Dashboards
**Warnings:** S03 (Purchase Orders), S04 (Expenses) — placeholder text detected

---

## CONDITIONAL CHECKS (C01-C19)

| Check | Feature | Status | Notes |
|-------|---------|--------|-------|
| C01-C04 | Multi-entity | SKIP | Single entity |
| C05 | Project Phases | PARTIAL | "Phase 1" in name but no Phases v2 tab |
| C06 | Cost Groups | NOT FOUND | No cost groups in products |
| C07 | AIA Billing | NOT FOUND | No Change Orders tab |
| C08 | Certified Payroll | UNVERIFIED | Payroll active, WH-347 not checked |
| C09-C11 | Non-profit | SKIP | Construction dataset |
| C12 | Customer Hub | PASS | Overview page loads |
| C13 | Intuit Intelligence | PASS | Chat button confirmed on all pages |
| C14 | Management Reports | PASS | Page loads, reports available |
| C15 | Contractors/1099 | PASS | Page loads with data |
| C16 | Time Approvals | PASS | Approval workflow functional |
| C17 | Change Orders | **CRITICAL GAP** | No Change Orders tab on project detail |
| C18 | Project Budgets | PARTIAL | Estimates vs Actuals shown, no formal budget tab |
| C19 | Smart Dimensions v2 | 404 | Feature not active on tenant |

---

## CONTENT SAFETY (CS1-CS9)

| Check | Rule | Status | Findings |
|-------|------|--------|----------|
| CS1 | Profanity | PASS | None detected |
| CS2 | Placeholders | **FAIL** | "Alan Somebody", "ABC New Court", "for Customer", "Test" projects |
| CS3 | Test names | **FAIL** | "Test" (x2), "Example Proj", "IDT TEST", "Project 1", "Title 1" |
| CS4 | PII | PASS | No real PII detected |
| CS5 | Cultural gaffes | PASS | None detected |
| CS6 | Duplicates | WARN | "Sawgrass residence" appears twice, "Test" appears twice |
| CS7 | i18n keys | PASS | No untranslated keys |
| CS8 | Real persons | **WARN** | "Intuit Dome" (real venue), "Jonathan Scott", "Harrison Scott" in products |
| CS9 | Spam | PASS | No spam patterns |

---

## REALISM SCORING (1-10 per criterion)

| # | Criterion | Score | Notes |
|---|-----------|-------|-------|
| 1 | Revenue realism | 5 | $1M+ revenue but 76.5% margin unrealistic for construction |
| 2 | Expense diversity | 6 | Multiple categories but COGS nearly $0 despite inventory |
| 3 | Customer quality | 5 | 51 customers but "Alan Somebody", "FLDN", non-construction names |
| 4 | Vendor quality | 7 | 50 construction-appropriate vendors |
| 5 | Product catalog | 7 | 112 well-categorized construction products |
| 6 | Project health | 4 | 20 projects but 7+ have placeholder names, 3 deeply negative |
| 7 | Banking realism | 4 | Stale feed (12/2024), 257 pending, negative balances |
| 8 | Report accuracy | 5 | Reports function but AR $7.66B, Petty Cash $20.8M distort |
| 9 | Sector fit | 5 | Construction industry set but missing Change Orders, Cost Groups |
| 10 | Content safety | 5 | Multiple placeholder names, test projects, real venue name |

**Total Realism Score: 53/100**

---

## FIXES APPLIED

None — no fixes were applied during this sweep. The sweep was observational only per the "never_fix" tier for settings and the lack of straightforward fix opportunities.

---

## RECOMMENDATIONS (Priority Order)

1. **CRITICAL:** Rename placeholder projects: "Test" → "Riverside Commercial Build", "Example Proj" → "Harbor District Renovation", "IDT TEST" → "Downtown Office Complex", etc.
2. **CRITICAL:** Add Change Orders feature to projects (construction differentiator)
3. **HIGH:** Fix customer names: "Alan Somebody" → real construction client name, remove "FLDN"
4. **HIGH:** Address COGS gap — $78 COGS with 22 inventory products is unrealistic
5. **HIGH:** Fix customer address: "ABC New Court, Sunnyvale, CO" → valid CA address
6. **MEDIUM:** Categorize 257 pending bank transactions
7. **MEDIUM:** Address negative bank balances (Checking -$1.84M, Cash -$1.46M)
8. **MEDIUM:** Reduce Petty Cash from $20.8M to realistic level
9. **LOW:** Add Cost Groups to products for job costing demos
10. **LOW:** Rename "Intuit Dome" project to avoid real venue reference

---

## PROJECT DETAIL SAMPLE: BMH Landscaping - Phase 1

- **Customer:** Emily Wong
- **Status:** In progress (0%)
- **Income:** $3,580,465.81 (actual) vs $2,432,872.92 (estimated) — $1.15M OVER estimated
- **Costs:** $1,347,119.91 (actual) vs $2,208,729.89 (estimated)
- **Profit:** $2,233,345.90 (62.38% margin)
- **Tabs:** Summary, Transactions, Time Activity, Project Reports, Project Details, Change Log, Attachments
- **Missing:** Phases tab, Budget tab, Change Orders tab
- **Hours:** 2,239:30

---

*Generated by Claude Opus 4.6 — Full Sweep v5.5*
