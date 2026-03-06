# Product Events — Revalidation Report (Sweep v3.0)
**Date:** 2026-03-06 ~19:45 UTC
**Account:** quickbooks-tbx-product-events-team-test@tbxofficial.com
**Previous Sweep:** product_events_2026-03-05.md (Score: 5/10)
**Revalidation Score:** **5/10** (CONFIRMED — no regression)
> **UPDATE:** Revenue fix applied — See `product_events_fix_session_2026-03-06.md` (Score: 5/10 → 6/10)

---

## Purpose

Revalidate all Product Events entities against the latest v3.0 sweep commit to confirm:
1. Previous findings persisted
2. No data regression from TestBox activity plans
3. Financial health consistent across entities

---

## Entity Revalidation Results

### OLD - Construction (Parent) — 5/10 ✅ CONSISTENT

| Metric | v1 Sweep (2026-03-05) | Revalidation | Status |
|--------|----------------------|--------------|--------|
| P&L Net Income | $0 | $0 | ✅ Match |
| Income | $0 | $0 | ✅ Match |
| Expenses | $0 | $0 | ✅ Match |
| Bank Total | $11,392,356 | $11,392,356 | ✅ Match |
| 1010 Checking QB | $460,000 | $460,000 | ✅ Match |
| Guardian Growth MMA | $10,932,356 | $10,932,356 | ⚠️ P1 inflation |
| AR | $3,910,383 | $3,910,383 | ✅ Match |
| Invoices Unpaid | $0 | $0 | ✅ Match |
| Sales | $0 | $0 | ✅ Match |
| FLDN customer | Present (P2) | Present (P2) | ⚠️ Still there |

**Settings:**
- Name: OLD - Construction ✅
- Legal business name: OLD - Construction ✅
- Industry: Construction ✅
- Business type: Corporation (Form 1120) — v1 noted S-Corp 1120-S, revalidation shows Corp 1120. Possible v1 misread or change.
- Address: 7535 Torrey Santa Fe Rd, San Diego, CA 92129-5704
- Legal address: 183 Berwick Way, Sunnyvale, CA 94087
- Customer address: 2600 Marine Way, Mountain View, CA 92129 ⚠️ ZIP mismatch (Mountain View≠92129)
- Phone: 180012345670 (P2 malformed)
- Email: contact@keystone-constructions.com
- i18n keys: NONE (clean)

**Feature inventory (from nav):** Customer Hub (Leads, Estimates, Proposals, Contracts, Reviews), Payroll, Lending, Time, Projects, Inventory, Sales Tax, Business Tax, AI-forecasted cash flow.

---

### OLD - BlueCraft (Child) — 4.5/10 ✅ CONSISTENT

| Metric | v1 Sweep (2026-03-05) | Revalidation | Status |
|--------|----------------------|--------------|--------|
| P&L Net Income | $0 | $0 | ✅ Match |
| Income | $0 | $0 | ✅ Match |
| Expenses | $0 | $0 | ✅ Match |
| Bank Total | $0 | $0 | ✅ Match |
| Guardian Growth MMA | $0 | $0 | ✅ Match (no inflation here) |
| 1010 Checking | $0 | $0 | ✅ Match |
| AR | $3,910,383 | $3,910,383 | ✅ Match |
| Invoices Unpaid | $0 | $0 | ✅ Match |
| Sales | $0 | $0 | ✅ Match |

**Settings:**
- Name: OLD - BlueCraft ✅
- Legal business name: OLD - BlueCraft ✅ (NO name swap — unlike QSP Events)
- Industry: Construction ✅
- Address: 7535 Torrey Santa Fe Rd, San Diego, CA 92129-5704
- Phone: 180012345670 (P2 malformed)

---

### OLD - Terra (Child) — 5/10 ✅ CONSISTENT

| Metric | v1 Sweep (2026-03-05) | Revalidation | Status |
|--------|----------------------|--------------|--------|
| P&L Net Income | -$4,791 | -$4,791 | ✅ Match |
| Income | $0 | $0 | ✅ Match |
| Expenses | $4,791 (Depreciation) | $4,791 (Depreciation) | ✅ Match |
| Bank Total | $0 | $0 | ✅ Match |
| Guardian Growth MMA | $0 | $0 | ✅ Match (no inflation) |
| 1010 Checking | $0 | $0 | ✅ Match |
| Invoices Unpaid | $0 | $0 | ✅ Match |
| Sales | $0 | $0 | ✅ Match |

**Settings:**
- Name: OLD - Terra ✅
- Legal business name: Keystone Terra BI (different from display name but NOT swapped)
- EIN: ****8735 (present, partially masked)
- Business type: Corporation (Form 1120)
- Legal address: 2700 COAST AVE, MOUNTAIN VIEW, CA 94043 (correct ZIP for Mountain View ✅)
- Address: 7535 Torrey Santa Fe Rd, San Diego, CA 92129-5704
- Phone: 180012345670 (P2 malformed)
- i18n keys: NONE ✅ (v1 reported raw keys — now clean, possible fix or v1 was different entity)

---

## Revalidation Summary

| Entity | v1 Score | Revalidation | Regression? |
|--------|----------|-------------|-------------|
| Construction (Parent) | 5/10 | 5/10 | NO ✅ |
| BlueCraft (Child) | 4.5/10 | 4.5/10 | NO ✅ |
| Terra (Child) | 5/10 | 5/10 | NO ✅ |
| **Overall** | **5/10** | **5/10** | **NO** ✅ |

---

## Key Differences: Product Events vs QSP Events

| Metric | Product Events | QSP Events |
|--------|---------------|------------|
| Overall Score | 5/10 | 7.5/10 |
| Revenue (any entity) | $0 across all | $3.4M+ (Parent), $5M (Terra) |
| Entity prefix | "OLD - " | "Keystone ... (Event)" |
| Consolidated View | NO | YES (Vista consolidada) |
| Legal name swap | NO (correct) | YES (BlueCraft↔Terra swapped, BLOCKED) |
| MMA inflation | Parent only ($10.9M) | ALL entities ($10.9M) |
| i18n keys | NONE now | NONE |
| AR | $3.9M (Construction + BlueCraft) | $4.3M (Construction) |
| Depreciation expense | Terra only ($4,791) | None notable |
| Customer Hub features | YES (Leads, Proposals, Contracts) | YES |
| Login MFA | NOT required | TOTP required |

---

## Open Issues (unchanged from v1)

### P1 — HIGH
1. **Guardian Growth MMA $10.9M** — Construction entity only (P1, systemic)
2. **Zero revenue across ALL entities** — No income, no sales. Environment unusable for revenue demos without population.
3. **Terra Net Income negative** (-$4,791) — Only expense is Depreciation.

### P2 — MEDIUM
4. **FLDN customer** — Present on Construction (P2)
5. **Malformed phone** 180012345670 — All 3 entities
6. **Customer address ZIP mismatch** — Mountain View, CA 92129 (should be 94043) on Construction
7. **No Consolidated View** — Unlike QSP Events
8. **0 projects** visible on Construction
9. **AR $3.9M shared** between Construction and BlueCraft — intercompany or data inheritance

### P3 — LOW
10. **Business type** — All entities now show Corporation (Form 1120)

---

## Improvements Found vs v1

1. **i18n keys RESOLVED** — Terra Settings no longer shows raw i18n key labels (was P2 in v1)
2. **No legal name swap** — Unlike QSP Events, this environment has correct legal names on all entities
3. **Terra legal address correct** — 2700 COAST AVE, MOUNTAIN VIEW, CA 94043 (ZIP matches city)

---

## Conclusion

**Product Events environment is STABLE at 5/10.** No data regression from TestBox activity plans. All financial metrics consistent across all 3 entities. This remains a mostly empty Construction IES environment — structure is correct but zero-revenue state makes it unsuitable for financial demos without significant data population.

**Best use case:** Testing IES multi-entity navigation, entity switching, and construction-specific feature availability (Customer Hub, Inventory, Estimates widget).

**Content safety: 0 violations** (confirmed across all 3 entities).

---

## Login Flow Notes (Revalidation)
- Email → Password → Passkey prompt (skipped "Ignorar") → Entity selector → QBO
- **TOTP NOT required** (consistent with v1)
- **No industry confirmation dialogs** this time (v1 had them on every entity switch)
- Entity selector shows 3 entities under "Intuit Enterprise Suite" heading

---

## Session Metadata
- Sweep started: ~19:45 UTC
- Sweep completed: ~19:55 UTC
- Stations audited: Dashboard + Settings (all 3 entities), Customers, Vendors, Projects, COA (Construction)
- Content scans: 3 (one per entity)
- Violations: 0
