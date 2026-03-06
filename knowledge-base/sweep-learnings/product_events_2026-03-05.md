# Product Events Team Test — QBO Sweep Report (v1)
> **REVALIDATED** — See `product_events_revalidation_2026-03-06.md` for latest (Score: 5/10 CONFIRMED)

**Date:** 2026-03-05
**Account:** quickbooks-tbx-product-events-team-test@tbxofficial.com
**Password:** TestBox123!
**TOTP Secret:** EPDEN7IRD4QG7M5A4WI5FJ2QWAK7W4WH (stored but NOT required — login skipped MFA)
**Environment:** Production IES (Intuit Enterprise Suite)
**Industry:** Construction

---

## Environment Overview

| Property | Value |
|----------|-------|
| Entities | 3 (OLD-Construction, OLD-BlueCraft, OLD-Terra) |
| Consolidated View | NOT AVAILABLE |
| Industry | Construction (all 3 entities) |
| Business Type | Corporation or S-Corporation |
| Company Address | 2632 Marine Way, Mountain View, CA 94043 |
| Email | quickbooks-tbx-product-events-team-test@tbxofficial.com |
| Phone | 180012345670 (malformed — P2) |

---

## Companies Discovered

| Entity | CID | Type | Priority |
|--------|-----|------|----------|
| OLD - Construction | 9341455474166259 | parent | P0 |
| OLD - BlueCraft | 9341455474197696 | child | P0 |
| OLD - Terra | 9341455474179575 | child | P0 |

---

## Entity Audit Results

### OLD - Construction (Parent) — Score: 5/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PARTIAL | P&L: Income $0, Expenses $0, Net $0. Bank QB $11.4M (inflated). AR $3.9M. Sales $0. |
| Customers | PASS | Multiple construction customers (Apex Contractors, Crestline Developers, Irongate Properties, etc.) |
| Vendors | PASS | Realistic vendor names (Aetna, AT&T, Concrete Depot, Lennar) |
| COA | PARTIAL | 75 accounts. Guardian Growth MMA $10.9M inflating bank balance (P1). |
| Projects | PARTIAL | 0 visible with current filter (may have projects under different filter) |
| Dimensions | PASS | 7 dimensions: Classes (Original), 7000 Garden Bed, Concrete, Customer Type, Earthwork, Electrical, Utilities. All shared with 3 companies. |
| Reports | PASS | Rich report page: Favorites, 17+ Consolidated Reports, Custom Report Builder, Financial Planning |
| Banking | PASS | Fresh environment. Accounting Agent visible. Ready to Post (BETA) present. |
| Settings | PARTIAL | Raw i18n key labels instead of translated text (P2). Industry=Construction. Business type=S-Corporation (Form 1120-S). |
| Content Safety | PASS | All clean. "FLDN" company name is suspicious placeholder (P2). |

### OLD - BlueCraft (Child) — Score: 4.5/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PARTIAL | P&L: $0/$0. Bank $0 (PayPal, Amazon Credit, BOI). AR $3.9M (same as parent). Sales $0. Inventory module present. |
| Settings | PASS | Industry=Construction. Business Type=Corporation (Form 1120). Same address as parent. Legal address: Sunnyvale, CA. |
| Content Safety | PASS | All clean. |

### OLD - Terra (Child) — Score: 5/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PARTIAL | P&L: Income $0, Expenses $4,791 (Depreciation, up 100%). Cash flow $0. Bank $0 (8 bank accounts, all $0). Sales $0. |
| Unique Widget | PASS | "Estimates vs actual cost" widget present (unique to Terra). |
| Bank Accounts | PASS | 8 accounts: PayPal, Amazon Credit, BOI Business Checking, Checking, Guardian Growth MMA, Petty Cash, Cash, Integra Arborists. |
| Content Safety | PASS | All clean. |

---

## Cross-Entity Comparison

| Metric | Construction | BlueCraft | Terra |
|--------|-------------|-----------|-------|
| Score | 5/10 | 4.5/10 | 5/10 |
| Income | $0 | $0 | $0 |
| Expenses | $0 | $0 | $4,791 |
| Net Income | $0 | $0 | -$4,791 |
| Bank QB | $11.4M | $0 | $0 |
| Bank Actual | $0 | $0 | $0 |
| AR | $3.9M | $3.9M | — |
| Sales YTD | $0 | $0 | $0 |
| Industry | Construction | Construction | Construction |
| Business Type | S-Corp (1120-S) | Corp (1120) | Construction |
| Dimensions | 7 (shared) | 7 (shared) | 7 (shared) |
| Inventory Module | — | YES | — |
| Estimates Widget | — | — | YES |

---

## Findings (Priority Order)

### P1 — HIGH
1. **Guardian Growth MMA $10.9M** — Construction entity has this Money Market Account inflating total bank balance to $11.4M vs $0 actual. Other entities show it at $0.
2. **Zero revenue across ALL entities** — No income, no sales on any entity. Environment appears fresh/unpopulated.
3. **Terra Net Income negative** (-$4,791) — Only entity with any P&L activity, all from Depreciation expenses.

### P2 — MEDIUM
4. **"FLDN" company name** in customer list — suspicious placeholder/abbreviation.
5. **Malformed phone** 180012345670 — Missing formatting, extra digit (should be 1-800-123-4567 or similar).
6. **Raw i18n keys** in Construction settings — Labels show untranslated keys instead of text.
7. **No Consolidated View** — Unlike other IES environments, this one has no consolidated reporting entity.
8. **0 projects** visible on Construction with current filter.
9. **AR $3.9M shared** between Construction and BlueCraft — suggests intercompany or data inheritance.

### P3 — LOW
10. **Business type inconsistency** — Construction is S-Corp (1120-S), BlueCraft is Corp (1120).
11. **Industry confirmation dialogs** triggered on every entity switch (first-time setup not complete).

---

## AI Features Observed

| Feature | Entity | Status |
|---------|--------|--------|
| AI-forecasted cash flow | All 3 | Active (showing $0 flat line) |
| Accounting Agent | Construction Banking | Visible |
| Ready to Post (BETA) | Construction Banking | Present |

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

- **TOTP was NOT required** — Login went: email → password → passkey prompt (skipped via "Ignorar") → Dashboard
- **Autofilled email** from previous session had to be cleared (triple-click + retype)
- **Industry confirmation** required on first access to each entity
- **"Unlock more clarity"** promo dialog appeared on BlueCraft and Terra
- **"Phishing warning"** banner appeared on BlueCraft and Terra

---

## Dimensions (Shared Across All 3 Entities)

| # | Dimension | Status | Companies |
|---|-----------|--------|-----------|
| 1 | Classes (Original) | Active | 3 |
| 2 | 7000 Garden Bed | Active | 3 |
| 3 | Concrete | Active | 3 |
| 4 | Customer Type | Active | 3 |
| 5 | Earthwork | Active | 3 |
| 6 | Electrical | Active | 3 |
| 7 | Utilities | Active | 3 |

---

## Screenshots Captured

| File | Description |
|------|-------------|
| product-events-dashboard-construction.png | Construction dashboard with P&L, Bank, AR |
| product-events-customers.png | Customers list |
| product-events-vendors.png | Vendors list |
| product-events-coa.png | Chart of Accounts with Guardian Growth |
| product-events-projects.png | Projects page (empty) |
| product-events-dimensions.png | Dimensions Hub with welcome dialog |
| product-events-dimensions-clean.png | Dimensions Hub clean |
| product-events-reports.png | Reports page |
| product-events-banking.png | Banking with Accounting Agent |
| product-events-bluecraft-dashboard.png | BlueCraft dashboard |
| product-events-terra-dashboard.png | Terra dashboard |

---

## Overall Assessment

**Realism Score: 5/10** — This is a mostly empty Construction IES environment. While the structure is correct (3 entities, proper dimensions, construction-appropriate customers/vendors), the zero-revenue state across all entities makes it unsuitable for any demo without significant data population. The Guardian Growth MMA balance inflation on Construction is the main anomaly. Terra's depreciation expense is the only P&L activity in the entire environment.

**Best use case:** Testing IES multi-entity navigation, dimension sharing, and construction-specific features (Estimates widget on Terra, Inventory on BlueCraft).

---

## Session Metadata
- Sweep started: ~21:00 UTC
- Sweep completed: ~21:50 UTC
- Stations audited: ~15 (10 Construction + 3 BlueCraft + 2 Terra)
- Content scans: 6
- Violations: 0
- Industry confirmation dialogs: 3 (one per entity)
