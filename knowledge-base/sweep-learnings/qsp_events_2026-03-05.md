# QSP Construction Events — QBO Sweep Report
**Date:** 2026-03-05
**Account:** quickbooks-test-account-qsp@tbxofficial.com
**Password:** TestBox123!
**TOTP Secret:** J4NUWKE7OZTIBOXI3MP42Z4QVBDDNITH (REQUIRED — MFA was enforced)
**Environment:** Production IES (Intuit Enterprise Suite)
**Industry:** Construction

---

## Environment Overview

| Property | Value |
|----------|-------|
| Entities | 4 (Construction parent + BlueCraft child + Terra child + Consolidated View) |
| Consolidated View | AVAILABLE (Vista consolidada) |
| Industry | Construction (all 3 operating entities) |
| Business Type | Corporation (Form 1120) — all entities |
| Company Address | 183 Berwick Way, Sunnyvale, CA 94087-3204 (Construction) |
| Email | contact@keystone-constructions.com |
| Phone | 8473470269 (Construction) / 180012345670 (children — MALFORMED) |

---

## Companies Discovered

| Entity | CID | Type | Priority |
|--------|-----|------|----------|
| Keystone Construction (Event) | 9341454796804202 | parent | P0 |
| Keystone BlueCraft (Event) | 9341454842756096 | child | P0 |
| Keystone Terra (Event) | 9341454842738078 | child | P0 |
| Vista consolidada | TBD | consolidated | P0 |

**NOTE:** QBO_CREDENTIALS.json previously listed only 3 companies. Consolidated View was discovered during this sweep.

---

## Entity Audit Results

### Keystone Construction (Event) — Parent — Score: 7.5/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PASS | P&L: Net $2,513,501 (81% margin), Income $3,447,139, Expenses $933,638. Bank $11,392,356. Project Profit Margin 100%. Operating Cash Flow -$238,880. Project Income $80,160 YTD. Project Backlog $220. |
| Customers | PASS | Ali Gold (FLDN), Ali Khan (Beacon $177K), Sophia Chang (Tropic Beacon $109K), Amelia Patel (Temet Nova $177K), Aryan Patel (Aegis $59K), Ava Kaur (Vented Dev $103K). Content CLEAN. |
| Vendors | PASS | Aetna, Assignar, AT&T, Blue Bird Insurance, Concrete Depot, Concrete Solutions, Construction Materials Inc. Unpaid $10.6K (3 overdue), Paid $18.5K. Content CLEAN. |
| Projects | PASS | TidalWave Farmer's Market ($640K), Azure Pines Playground (4 years x $560K), BMH Landscaping (3 years x $800K). All 100% margin. |
| Dimensions | PASS | 3 active (Classes ORIGINAL, 5 Service unit, Customer Type) + 4 inactive. Content CLEAN. |
| Banking | PASS | 1010 Checking: Bank $460K, Posted $10.5M, 42 pending. Guardian Growth MMA: $10.9M (inflation). |
| Settings | PASS | Industry="Industrial building construction", Corp Form 1120, Sunnyvale CA. Phone 8473470269 (OK). |
| Tasks | PASS | Multiple overdue tasks: Intuit Dome 2025/2026 expense reviews, invoice reviews, David Kiser House. |
| Create Menu | PASS | Full construction features: Project estimate, Change order, Project budget, Sales order, Contract, Item receipt (NEW). |
| Content Safety | PASS | "FLDN" company name noted (P2 — suspicious abbreviation). |

### Keystone BlueCraft (Event) — Child — Score: 6.5/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PARTIAL | P&L: -$1,978,572 (100% expenses, $0 income). Cash flow -$165K. Bank $11,392,356. Invoices $17.7M unpaid ($5.9M overdue). Sales $6,632,480 YTD. Estimates vs actual $4,138,112. |
| Banking Detail | PARTIAL | 1010 Checking: Bank $460K vs **QB $148,457,999.97** (P1 — EXTREME inflation). Guardian Growth MMA: $10.9M. 9 txns to review. |
| Settings | FAIL | **P1: Legal name = "Keystone Terra2"** (should be "Keystone BlueCraft"). Address: San Diego CA. Phone: 180012345670 (malformed). Industry: Construction. **P2: ZIP mismatch** — Customer address says Mountain View 92129 (San Diego ZIP for Mountain View). |
| Expenses | PASS | COGS $1,798,572, Job supplies $150K, Legal $15K, Consultancy $12K, Contract labor $3K. |
| Content Safety | PASS | All clean. |

### Keystone Terra (Event) — Child — Score: 7/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PASS | P&L: +$267,176 (83%), Income $4,960,057, Expenses $4,692,880. Down 94% from FY25. Sales $19,993,189 (last 6 months — HIGHEST). Cash flow $3,975,731. Estimates vs actual $3,929,785. |
| Banking Detail | PARTIAL | Bank $11,392,356 (same inflation). 40 + 82 = 122 txns to categorize. |
| Settings | FAIL | **P1: Legal name = "Keystone BlueCraft2"** (should be "Keystone Terra"). **P2: Raw i18n keys** everywhere (business_name, edit_details, legal_info_header, company_tax_form_1120_settings). Phone: 180012345670 (malformed). **P2: ZIP mismatch** — Customer address says Mountain View 92129. |
| AI Features | PASS | AI-forecasted cash flow active. Actual income vs cost widget. Estimates vs actual cost widget. |
| Content Safety | PASS | All clean. |

---

## Cross-Entity Comparison

| Metric | Construction | BlueCraft | Terra |
|--------|-------------|-----------|-------|
| Score | 7.5/10 | 6.5/10 | 7/10 |
| Income | $3,447,139 | $0 | $4,960,057 |
| Expenses | $933,638 | $1,978,572 | $4,692,880 |
| Net Income | +$2,513,501 | -$1,978,572 | +$267,176 |
| Bank QB Total | $11,392,356 | $11,392,356 | $11,392,356 |
| 1010 Checking QB | $10,545,205 | **$148,457,999** | — |
| Bank Actual | $460,000 | $460,000 | — |
| Guardian Growth MMA | $10,932,356 | $10,892,356 | — |
| Sales YTD | — | $6,632,480 | $19,993,189 |
| Invoices Unpaid | — | $17.7M | — |
| Pending Txns | 42 | 9 | 122 |
| Industry | Industrial building construction | Construction | Construction |
| Business Type | Corp (1120) | Corp (1120) | Corp (1120) |
| Legal Name | Keystone Construction Event | **Keystone Terra2** (WRONG) | **Keystone BlueCraft2** (WRONG) |
| Phone | 8473470269 | 180012345670 | 180012345670 |
| Address | Sunnyvale, CA 94087 | San Diego, CA 92129 | San Diego, CA 92129 |
| i18n Keys | Normal | Normal | **RAW KEYS** |
| Estimates Widget | — | YES | YES |
| Project Income Widget | YES | — | — |
| Payroll | YES | YES | YES |

---

## Findings (Priority Order)

### P1 — HIGH
1. **Legal names SWAPPED between children** — BlueCraft shows "Keystone Terra2", Terra shows "Keystone BlueCraft2". These are cross-contaminated and need immediate correction.
2. **BlueCraft P&L negative** (-$1,978,572) — 100% expenses, $0 income. Needs revenue fix for demos.
3. **BlueCraft 1010 Checking QB balance $148.5M** vs $460K actual — extreme inflation, 300x the real balance.
4. **Guardian Growth MMA $10.9M** across all entities — inflating bank balances (same issue as product-events environment).

### P2 — MEDIUM
5. **Terra raw i18n keys** in Settings — Labels show untranslated keys (business_name, edit_details, legal_info_header, etc.).
6. **Malformed phone** 180012345670 on BlueCraft and Terra (parent has correct 8473470269).
7. **ZIP code mismatch** on children — Customer address says "Mountain View, California 92129" but Mountain View ZIP is 94043. 92129 is San Diego.
8. **"FLDN" company name** in customer list — suspicious placeholder/abbreviation (same as product-events).
9. **All projects show 100% profit margin** — no costs recorded against projects.
10. **No Consolidated View audited** — discovered but not swept in this session.

### P3 — LOW
11. **Industry inconsistency** — Parent says "Industrial building construction", children say "Construction".
12. **122 transactions to categorize** on Terra (40 + 82).

---

## AI Features Observed

| Feature | Entity | Status |
|---------|--------|--------|
| AI-forecasted cash flow | BlueCraft, Terra | Active |
| Construction dashboard | Construction | Active (Project Profit Margin, Operating Cash Flow, Project Income, Project Backlog) |
| Estimates vs actual cost | BlueCraft, Terra | Active |
| Actual income vs cost | Terra | Active |
| Create menu: Item receipt (NEW) | Construction | Present |
| Task management | Construction | Active (overdue tasks for Intuit Dome, David Kiser House) |

---

## Content Safety: ZERO VIOLATIONS

All stations across all 3 entities scanned for:
- Profanity/slurs
- Placeholder data (TBX, Test, Lorem)
- PII
- Cultural gaffes
- Real person names in sensitive contexts

**Result: ALL CLEAN** (FLDN noted as P2 but not a safety violation)

---

## Login Flow Notes

- **TOTP WAS REQUIRED** — Unlike product-events (which skipped MFA), QSP enforced MFA
- **TOTP Secret:** J4NUWKE7OZTIBOXI3MP42Z4QVBDDNITH confirmed working
- **Phone verification offered** (skipped via "Ignorar por agora")
- **Passkey prompt** appeared (skipped via "Ignorar")
- **Account selector** showed 4 entities (Consolidated View + 3 operating entities)
- **No industry confirmation dialogs** (unlike product-events)

---

## Comparison: QSP vs Product-Events

| Metric | QSP (this sweep) | Product-Events (earlier) |
|--------|------------------|-------------------------|
| Overall Score | **7/10** | 5/10 |
| Revenue | $3.4M+ (Construction), $20M (Terra) | $0 across all |
| Projects | Rich (TidalWave, Azure Pines, BMH) | 0 visible |
| Vendors | Active ($10.6K unpaid) | Present but dormant |
| Consolidated View | YES | NO |
| MFA Required | YES (TOTP) | NO (skipped) |
| Tasks | Multiple overdue (active env) | None |
| Construction Dashboard | YES (project metrics) | Partial |
| i18n Keys | Terra only | Construction entity |
| Legal Name Bug | SWAPPED (P1) | Not present |

**Conclusion:** QSP is a significantly richer and more realistic Construction IES environment than Product-Events. Best suited for demos requiring active financial data, construction project tracking, and multi-entity workflows.

---

## Screenshots Captured

| File | Description |
|------|-------------|
| qsp-construction-dashboard.png | Construction dashboard with P&L, Bank, Project metrics |
| qsp-construction-customers-clean.png | Customers list with Create menu overlay |
| qsp-construction-projects.png | Projects page (TidalWave, Azure Pines, BMH) |
| qsp-construction-dimensions.png | Dimensions Hub (3 active + 4 inactive) |
| qsp-construction-settings.png | Settings (Industry, Corp Form 1120) |
| qsp-construction-vendors.png | Vendors list (Aetna, AT&T, etc.) |
| qsp-construction-banking.png | Banking (1010 Checking + Guardian Growth MMA) |
| qsp-bluecraft-dashboard.png | BlueCraft dashboard (P&L -$1.98M) |
| qsp-terra-dashboard.png | Terra dashboard (P&L +$267K, Sales $20M) |

---

## Overall Assessment

**Realism Score: 7/10** — This is a well-populated Construction IES environment with real financial data, active projects, overdue tasks, and construction-specific features. The P1 legal name swap between children is the most critical issue. BlueCraft's negative P&L and extreme QB balance inflation ($148.5M) are also significant. Terra is the strongest entity with $20M in sales and positive net income.

**Best use case:** Construction IES demos with multi-entity workflows, project tracking, estimates vs actual cost analysis, and task management. Fix legal name swap before any client-facing demo.

---

## Session Metadata
- Sweep started: ~01:30 UTC (2026-03-06)
- Sweep completed: ~01:45 UTC
- Stations audited: ~15 (10 Construction + 3 BlueCraft + 3 Terra)
- Content scans: 9
- Violations: 0
- Login: Email + Password + TOTP (MFA enforced)
