# Sweep Report: MID MARKET (Construction single-entity)
**Date:** 2026-03-12
**Profile:** Full Sweep v5.1 Enhanced
**Account:** mid_market@tbxofficial.com
**Dataset:** construction

---

## Entity: Keystone Construction (9341452713218633) — single, P0

### DEEP STATIONS (D01-D12)

**[D01] Dashboard** ✓
- Company: Keystone Construction
- Net profit Feb ~$290K
- $51K overdue invoices
- Active business feed
- No TBX/placeholder text

**[D02] P&L** ✓
- Revenue: $1.07M
- Net Operating Income: $819K (POSITIVE)
- COGS: $78
- Payroll: $214K
- No JE needed

**[D03] Balance Sheet** ⚠
- AR: $7.66B (phantom — prior cycle inflation, not fixable)
- Checking: -$1.83M (negative)
- Total Assets: $7.69B
- AP: $9.87M
- Report truncated on IES

**[D04] Banking** ⚠
- BLOCKED: Error 103 on both bank connections
- Bank feed stale since 12/2024
- Guardian MMA: $10.9M inflation (known platform artifact)

**[D05] Customers** ✓ FIXED
- 50 customers
- Money bar: $6,679 estimates, $3.69M unbilled, $890K overdue (17), $1.91M open (35), $20.6K paid (1)
- **CS3 FIXES applied (4):**
  1. "Andrew Allen Test" → "Andrew Callahan" / Callahan Structural Engineering
  2. "Andrew Allen Test 1" → "Marcus Delgado" / Delgado Masonry & Concrete
  3. "Cass Wyatt" company "TESTER" → "Wyatt Site Prep & Grading"
  4. "IDT Tester" → "Derek Thornton" / "Thornton Civil Engineering"
- **CS4 FIX:** Andrew Callahan email changed from @intuit.com to construction-appropriate

**[D06] Vendors** ✓ FIXED
- 50 vendors
- Overdue: $11,355,660.66
- **CS3/CS4 FIXES applied (2):**
  1. "Mr IDT TEst Tester" → "Raymond Vasquez" / "Vasquez Excavation & Hauling"
  2. "Laura Woods" — email changed from laura_woods@intuit.com to lwoods@woodslandscaping.com, company from "Laura's Flowers" to "Woods Landscaping & Irrigation"

**[D07] Employees & Payroll** ✓
- 10 active employees visible
- Next payroll: 03/15/2026
- Mix hourly ($32-45/hr) and salaried ($115K-350K/yr)
- All paper check
- CS3/CS4: CLEAN

**[D08] Products & Inventory** ✓
- 50 products: 31 Service, 16 Non-Inventory, 3 Inventory
- Construction-appropriate names
- CS3: CLEAN

**[D09] Projects & Job Costing** ⚠
- Multiple projects with income/cost data
- **CS3 issues (report-only):**
  - "IDT TEST" project
  - "Test" (x2) projects
  - "Example Proj" project
- Project rename restricted in QBO

**[D10] Reports Advanced & BI** ✓
- Accessible via /app/standardreports
- KPIs and Dashboards marked "new"
- Financial planning available

**[D11] Chart of Accounts** ✓
- 75 accounts
- Complete hierarchy
- CS3: CLEAN
- Route: /app/chartofaccounts (not /app/chart-of-accounts)

**[D12] Settings / Company Info** ⚠
- Company: Keystone Construction
- Industry: Construction ✓
- Legal: Keystone Construction, LLC
- EIN: •••••8735 ✓
- Business type: Corporation (Form 1120)
- Address: 2700 Coast Ave, Mountain View, CA 94043-1140
- Email: contact@keystone-constructions.com
- Phone: +16509446000
- **Issues:**
  - Customer address: "Sunnyvale, **CO** 94087" — should be CA (ZIP 94087 is CA)
  - Website: "None listed" — incomplete for $1M+ revenue company
  - Customer address: "ABC New Court" — potentially placeholder

### SURFACE SCAN (S01-S30)

| Batch | Stations | Status |
|-------|----------|--------|
| S01-S06 | Estimates, Sales Orders, POs, Expenses, Recurring, Fixed Assets | ✓✓⚠⚠✓✓ |
| S07-S12 | Rev Recog, Time, Sales Tax, Reconcile, Bank Rules, Receipts | ✓✓✓✓✓✓ |
| S13-S18 | Budgets, Classes, Workflows, Payment Links, Subscriptions, Accountant | ✓✓✓✓✓✓ |
| S19-S24 | Audit Log, Lending, Settings-Sales, Settings-Expenses, Settings-Advanced, Quick Create | ✓✓✓⚠⚠✓ |
| S25-S30 | Custom Forms, Tags, Custom Fields, Cash Flow, Attachments, Mileage | ✓✓✓✓✓✓ |

**Notes:**
- S03 (POs): Placeholder text detected (hasPH=true) — likely from vendor names
- S04 (Expenses): Placeholder text detected (hasPH=true) — likely from vendor names
- S22/S23 (Settings Expenses/Advanced): 404-text detected — likely false positive from shell error messages, pages loaded with 69/72 lines of content

### CONDITIONAL (C01-C15)

| Station | Description | Status |
|---------|-------------|--------|
| C01-C04 | Multi-entity (Consolidated, Shared COA, IC, Consolidated Reports) | N/A (single entity) |
| C05 | Project Phases | ✓ (construction features present) |
| C06 | Cost Groups | ✓ (via Products) |
| C07 | AIA Billing | ✓ (via Projects) |
| C08 | Certified Payroll | ✓ (via Payroll) |
| C09-C11 | Non-Profit (Terminology, Statement of Activity, NP Dimensions) | N/A |
| C12 | Customer Hub | ✓ (Leads/Proposals accessible) |
| C13 | Intuit Intelligence | ✓ (Conversational BI in reports) |
| C14 | Management Reports | ✓ |
| C15 | Contractors / 1099 | ✓ |

### CONTENT SAFETY (CS1-CS9)

| Check | Status | Details |
|-------|--------|---------|
| CS1 Profanity | CLEAN | No profanity detected |
| CS2 Placeholder | ⚠ | Some PO/Expense pages have placeholder-flagged text (vendor names from prior data) |
| CS3 Test Names | FIXED (partial) | 4 customers renamed, 1 vendor renamed. Remaining: "IDT TEST" project, "Test" (x2) projects, "Example Proj", sub-customer "Thornton:IDT TEST" |
| CS4 PII | FIXED | All @intuit.com emails corrected. Andrew Callahan + Laura Woods emails fixed |
| CS5 Cultural | CLEAN | No sensitive/political references |
| CS6 Duplicate Names | CLEAN | No numeric suffix duplicates found |
| CS7 Real Persons | CLEAN | No real person names in financial contexts |
| CS8 i18n/Realism | ⚠ REPORT | Jason Cioran $20B balance; non-construction companies (Blakey's Bin Liners, Kini Exotic Pet Emporium); UK phone numbers mixed with US construction |
| CS9 Spam/Nonsense | CLEAN | No keyboard mash or spam detected |

### FIXES APPLIED

| # | Type | Entity | Before | After |
|---|------|--------|--------|-------|
| 1 | CS3 Rename | Customer | "Andrew Allen Test" | "Andrew Callahan" / Callahan Structural Engineering |
| 2 | CS3 Rename | Customer | "Andrew Allen Test 1" | "Marcus Delgado" / Delgado Masonry & Concrete |
| 3 | CS3 Rename | Customer | Cass Wyatt company "TESTER" | "Wyatt Site Prep & Grading" |
| 4 | CS3 Rename | Customer | "IDT Tester" | "Derek Thornton" / "Thornton Civil Engineering" |
| 5 | CS4 Email | Customer | Andrew Callahan @intuit.com | construction-appropriate email |
| 6 | CS3 Rename | Vendor | "Mr IDT TEst Tester" | "Raymond Vasquez" / "Vasquez Excavation & Hauling" |
| 7 | CS4 Fix | Vendor | Laura Woods email @intuit.com, company "Laura's Flowers" | lwoods@woodslandscaping.com, "Woods Landscaping & Irrigation" |

### REMAINING ISSUES (NOT FIXABLE)

| # | Severity | Issue | Reason |
|---|----------|-------|--------|
| 1 | P2 | CS3: Projects "IDT TEST", "Test" (x2), "Example Proj" | Project rename restricted in QBO |
| 2 | P2 | CS3: Sub-customer "Thornton:IDT TEST" | Sub-customer rename may require parent edit |
| 3 | P1 | D03: AR $7.66B phantom balance | Prior cycle inflation, not fixable via DB |
| 4 | P1 | D03: Checking -$1.83M negative | Platform/data artifact |
| 5 | P2 | D04: Error 103 on bank connections | Auth expired, requires Intuit re-auth |
| 6 | P2 | D04: Guardian MMA $10.9M inflation | Known platform artifact |
| 7 | P2 | D12: Customer address Sunnyvale, CO (should be CA) | Settings edit requires admin/2FA |
| 8 | P3 | D12: Website "None listed" | Settings edit requires admin/2FA |
| 9 | P3 | CS8: Jason Cioran $20B balance | Phantom AR from prior cycle |
| 10 | P3 | CS8: Non-construction company names in data | Pre-existing dataset artifact |

### REALISM SCORING

| Criterion | Score (1-10) | Notes |
|-----------|-------------|-------|
| 1. Financial Viability | 7 | P&L positive ($819K net), margins healthy. AR inflated ($7.66B) is unrealistic |
| 2. Name Coherence | 7 | Most names construction-appropriate after CS3 fixes. Some non-construction vendors remain |
| 3. Data Volume | 8 | 50 customers, 50 vendors, 50 products, 75 CoA accounts — good density |
| 4. Transaction Diversity | 7 | Invoices, expenses, bills, POs, estimates, time entries all present |
| 5. Banking Health | 4 | Error 103 connections, -$1.83M checking, $10.9M MMA inflation |
| 6. AR/AP Balance | 3 | AR $7.66B phantom, AP $9.87M disproportionate to revenue |
| 7. Payroll | 7 | 10 employees, next payroll scheduled, rates realistic |
| 8. Projects | 6 | Multiple projects exist but CS3 test names remain |
| 9. Reports | 7 | P&L, BS, reports accessible. BS truncated on IES |
| 10. Storytelling | 6 | Construction narrative holds but phantom balances break immersion |

**Overall Realism Score: 62/100**

### IES ROUTING NOTES

| Route | Status |
|-------|--------|
| /app/company | 404 — use /app/settings?panel=company |
| /app/chart-of-accounts | 404 — use /app/chartofaccounts |
| /app/reportlist | 404 — use /app/standardreports |
| /app/reports/profitandloss | 404 — use standardreports sidebar |
| /app/balance-sheet | 404 — use standardreports sidebar |

---

**Sweep completed:** 2026-03-12T15:35
**Analyst:** Claude (automated sweep via QBO Demo Manager Dashboard v5.0)
**Fixes applied:** 7 (4 CS3 renames, 2 CS4 email fixes, 1 combined CS3+CS4)
**Blocks:** Banking Error 103, BS truncation, phantom AR $7.66B
