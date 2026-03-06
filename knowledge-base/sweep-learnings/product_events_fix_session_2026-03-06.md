# Product Events — Revenue Fix Session
**Date:** 2026-03-06 ~20:00-20:35 UTC
**Account:** quickbooks-tbx-product-events-team-test@tbxofficial.com
**Previous Score:** 5/10 (all entities $0 income)
**Post-Fix Score:** **6/10** (Construction verified, BlueCraft/Terra JEs saved pending dashboard refresh)

---

## Purpose

Fix the #1 P1 issue across all Product Events entities: **zero revenue**. All 3 entities had $0 income making the environment unusable for financial demos.

**Method:** Journal Entries (DR 1110 Accounts Receivable / CR 4000 Sales Income) with customer "Apex" as payee.

---

## Journal Entries Created

| Entity | JE # | Date | Debit (AR) | Credit (Sales) | Payee | Status |
|--------|-------|------|------------|----------------|-------|--------|
| Construction (Parent) | #1 | 02/15/2026 | $500,000 | $500,000 | Apex | SAVED ✅ |
| Construction (Parent) | #2 | 03/01/2026 | $500,000 | $500,000 | Apex | SAVED + VERIFIED ✅ |
| BlueCraft (Child) | #1 | 03/01/2026 | $300,000 | $300,000 | Apex | SAVED ✅ |
| Terra (Child) | #31 | 03/01/2026 | $200,000 | $200,000 | Apex | SAVED ✅ |

**Total revenue injected: $1,500,000** ($1M Construction + $300K BlueCraft + $200K Terra)

---

## Dashboard Verification

### Construction (Parent) — VERIFIED ✅
- **P&L Income:** $500,000 (was $0)
- **P&L Net:** $500,000 (was $0)
- **Dashboard text:** "Up 100% from prior month"
- **AR:** $4,410,383 (was $3,910,383 — increased by $500K from JE #1)
- **JE #2 ($500K) reflected on dashboard** — the $500K income shown is from JE #2 (dated 03/01/2026, current month)
- **JE #1 ($500K, dated 02/15)** likely shows in February period (not visible on current month dashboard card)

### BlueCraft (Child) — JE SAVED, DASHBOARD NOT VERIFIED
- JE #1 saved successfully ("Journal Entry 1 saved")
- Entity switch from Construction to BlueCraft required `page.evaluate` with `getComputedStyle(div).cursor === 'pointer'` to open entity menu, then `getByRole('menuitem')` to select
- Dashboard verification blocked — could not switch back to BlueCraft after moving to Terra
- **Expected P&L:** Income $300,000, Net $300,000

### Terra (Child) — JE SAVED, DASHBOARD SHOWS STALE DATA
- JE #31 saved successfully ("Journal Entry 31 saved")
- Dashboard after save still shows: Income $0, Expenses $4,791, Net -$4,791
- **Root cause (likely):** Dashboard P&L card period filter doesn't include March 1 JE date, OR dashboard data is cached and hasn't refreshed
- Same issue as QSP Events BlueCraft JE regression (JE exists in system but P&L card doesn't show it)
- **Expected P&L:** Income $200,000, Net $195,209

---

## Updated Entity Scores

| Entity | Pre-Fix | Post-Fix | Change |
|--------|---------|----------|--------|
| Construction (Parent) | 5/10 | **6.5/10** | +1.5 (positive P&L verified) |
| BlueCraft (Child) | 4.5/10 | **5.5/10** (expected) | +1 (JE saved, pending verification) |
| Terra (Child) | 5/10 | **5.5/10** (expected) | +0.5 (JE saved, stale dashboard) |
| **Overall** | **5/10** | **6/10** | **+1** |

---

## Technical Findings (Playwright MCP)

### Entity Switching in Product Events IES
1. **`companyId` URL parameter does NOT work** — navigating to `?companyId=XXXX` does not switch entities
2. **Entity switcher requires two-step approach:**
   - Step 1: `page.evaluate` to find the company name div with `getComputedStyle(div).cursor === 'pointer'` and click it
   - Step 2: Wait for menu, then `page.getByRole('menuitem')` to select target entity
3. **Entity switching is SESSION-STICKY** — once you switch, all subsequent navigations stay on that entity
4. **Switching back can fail** — after switching Construction→BlueCraft→Terra, switching back to BlueCraft failed despite using the same technique

### JE Form Quirks (Product Events)
1. **"Apex" customer exists** — created during Construction JE #1 in previous session. Available on all entities via shared customer list.
2. **Row activation required** — JE form rows are lazy-loaded. Must click `read-only-account-holder-row-N` to activate line N.
3. **Auto-balance works** — When Row 1 has a debit, Row 2 credits auto-populate after selecting an account.
4. **ModalDialog--wrapper interference** — QBO modals intercept Playwright clicks. Must use `{ force: true }` or remove via DOM manipulation.
5. **JE numbering across entities** — Construction got #1 and #2, BlueCraft got #1, Terra got #31 (pre-existing JEs in the system).
6. **"Clear transaction?" modal** — Clicking Clear button triggers confirmation dialog inside `[data-testid="ModalDialog--container"]`. Requires force-click on "Clear transaction" button.

### Known 404s on Product Events
- `/app/reportlist` → 404 on Terra (may be entity-specific)
- `/app/dimensions` → use `/app/class` instead
- `/app/chart-of-accounts` → use `/app/chartofaccounts?jobId=accounting`

---

## Open Issues (Updated)

### P1 — HIGH (partially resolved)
1. ~~**Zero revenue across ALL entities**~~ → **PARTIALLY FIXED** — JEs created on all 3, Construction verified
2. **Guardian Growth MMA $10.9M** — Construction entity only (systemic, no fix available)
3. **BlueCraft/Terra JE dashboard verification pending** — JEs saved but P&L cards show stale data

### P2 — MEDIUM (unchanged)
4. **FLDN customer** — Still present on Construction
5. **Malformed phone** 180012345670 — All 3 entities
6. **Customer address ZIP mismatch** — Mountain View, CA 92129 on Construction
7. **No Consolidated View** — Unlike QSP Events
8. **0 projects** visible on Construction
9. **AR $3.9M shared** between Construction and BlueCraft

### P3 — LOW (unchanged)
10. **Business type** — All entities show Corporation (Form 1120)

---

## Next Steps

1. **Re-verify BlueCraft and Terra dashboards** — Wait for cache refresh or next session
2. **Create projects on Construction** — Currently 0 visible (need 3+ realistic construction projects)
3. **Consider additional JEs** — If dashboard period is "This month", Feb 15 JE won't show. May need all JEs dated in current month.
4. **FLDN customer cleanup** — Rename or delete suspicious placeholder

---

## Session Metadata
- Fix session started: ~20:00 UTC
- Fix session completed: ~20:35 UTC
- JEs created: 4 (2 Construction + 1 BlueCraft + 1 Terra)
- Total revenue injected: $1,500,000
- Dashboard verifications: 1/3 (Construction only)
- Entity switches: 3 (Construction → BlueCraft → Terra)
- Content violations: 0
