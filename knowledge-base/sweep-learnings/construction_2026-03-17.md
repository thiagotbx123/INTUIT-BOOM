# Sweep Report: CONSTRUCTION SALES (Keystone 8-entity)

**Date:** 2026-03-17
**Profile:** Full Sweep v5.5 Release Coverage
**Account:** construction (Keystone 8-entity)
**Duration:** ~60 minutes (19:33 - 20:32 UTC-3)
**Verdict:** PASS (with 1 fix applied)

---

## Entity Coverage

| # | Entity | CID | Type | Priority | D01 | D02 | Full Sweep |
|---|--------|-----|------|----------|-----|-----|------------|
| 1 | Keystone Construction (Par.) | 9341454156620895 | parent | P0 | OK(97) | OK(210) | D01-D12 + S + C |
| 2 | Keystone Terra (Ch.) | 9341454156620204 | child | P0 | OK(112) | OK(210) | D-batch + S-batch |
| 3 | Keystone BlueCraft (Ch.) | 9341454156621045 | child | P0 | OK(111) | OK(211) | D-batch |
| 4 | Keystone Ironcraft | 9341454156643813 | child | P1 | OK(97) | OK(195) | D01+D02 |
| 5 | Keystone Stonecraft | 9341454156640324 | child | P1 | OK(113) | OK(181) | D01+D02 |
| 6 | Keystone Canopy | 9341454156634620 | child | P1 | OK(113) | OK(212) | D01+D02 |
| 7 | Keystone Ecocraft | 9341454156644492 | child | P1 | OK(86) | OK(190) | D01+D02 |
| 8 | Keystone Volt | 9341454156629550 | child | P1 | OK(93) | OK(188) | D01+D02 |

## Fixes Applied (1)

### Fix 1: JE #67 — Negative P&L on Parent Entity
- **Station:** D02 (P&L Review)
- **Entity:** Keystone Construction (Par.) — CID 9341454156620895
- **Issue:** P&L was negative (-$229,635.32)
- **Action:** Created Journal Entry #67
  - DR Accounts Receivable $300,000
  - CR Consulting Services $300,000
  - Customer: BACAR Constructors
  - Date: 03/01/2026
- **Result:** P&L flipped to +$70,364.68
- **RV01 Reverification:** PASS

## Deep Station Results (Parent - P0)

| Station | Route | Status | Lines | Notes |
|---------|-------|--------|-------|-------|
| D01 | /app/homepage | OK | 97 | Money values present |
| D02 | standardreports > P&L | OK | 210 | Fixed via JE #67 |
| D03 | standardreports > BS | OK | ~200 | IES routing required |
| D04 | /app/banking?jobId=accounting | OK | ~180 | Banking page loaded |
| D05 | /app/customers | OK | ~300 | Customer list present |
| D06 | /app/vendors | OK | ~350 | Vendor list present |
| D07 | /app/employees?jobId=team | OK | ~40 | Team page loaded |
| D08 | /app/items | OK | ~250 | Products/services list |
| D09 | /app/projects | OK | ~150 | Projects listed |
| D10 | /app/standardreports | OK | ~167 | Reports hub accessible |
| D11 | /app/chartofaccounts?jobId=accounting | OK | ~400 | Full COA |
| D12 | Gear > Account and Settings | OK | ~100 | Settings accessible |

## Surface Scan Results (Parent - P0)

- **Total S checks:** S01-S46
- **Passed:** 40/46
- **IES 404s (expected):** S03, S16, S17, S25, S28, S37
  - S03: /app/paymentlinks (404)
  - S16: /app/subscriptions (404)
  - S17: /app/customformstyles (404)
  - S25: /app/cashflow (404)
  - S28: /app/expenseclaims (404)
  - S37: /app/paymentlinks (duplicate, 404)

## Conditional Check Results (Parent - P0)

| Check | Status | Notes |
|-------|--------|-------|
| C01-C08 | OK | All applicable checks passed |
| C09-C11 | N/A | NP-only (not applicable to IES) |
| C12-C19 | OK | All applicable checks passed |

## Cross-Entity Validation (X01-X07)

| Check | Description | Status | Notes |
|-------|-------------|--------|-------|
| X01 | P&L Consolidation | PASS | P&L verified on all 8 entities |
| X02 | Legal Name Integrity | PASS | All names unique and professional |
| X03 | Industry Consistency | PASS | All entities: Construction |
| X04 | IC Entity Existence | PASS | All 8 entities visible in switcher |
| X05 | COA Alignment | PASS | Shared COA with 425 lines |
| X06 | Data Freshness Parity | PASS | All entities show current money values |
| X07 | Transaction Chain | PASS | Invoices/bills/vendors consistent across P0 entities |

## Content Safety (CS1-CS9)

| Check | Status | Notes |
|-------|--------|-------|
| CS1: Offensive names | PASS | No offensive content found |
| CS2: PII exposure | PASS | No real PII detected |
| CS3: Placeholder content | FLAG | "Construction- Test Delete" project name found |
| CS4: Profanity | PASS | No profanity detected |
| CS5: Sensitive data | PASS | No sensitive data exposed |
| CS6: Unrealistic amounts | PASS | All amounts within realistic range |
| CS7: Duplicate entities | PASS | No duplicate entity names |
| CS8: Empty critical fields | PASS | All critical fields populated |
| CS9: Date anomalies | PASS | No date anomalies detected |

## Realism Score: 79/100

| Criterion | Score (1-10) |
|-----------|-------------|
| Data Volume | 8 |
| Data Variety | 8 |
| Naming Quality | 7 |
| Financial Coherence | 8 |
| Temporal Distribution | 7 |
| Entity Relationships | 9 |
| Industry Alignment | 9 |
| UI Completeness | 7 |
| Cross-Entity Consistency | 8 |
| Professional Appearance | 8 |
| **TOTAL** | **79/100** |

**Naming Quality (7):** CS3 flag for "Construction- Test Delete" project name brings this down.
**UI Completeness (7):** IES 404 routes are expected but reduce completeness perception.
**Temporal Distribution (7):** base_date=first_of_year means limited "past" data visible.

## IES Routing Notes

- Parent entity has 115 plugins (consolidated view)
- Child entities have 413-414 plugins (full QBO feature set)
- `/app/reportlist` → 404, use `/app/standardreports` instead
- `/app/paymentlinks`, `/app/subscriptions`, `/app/customformstyles`, `/app/cashflow`, `/app/expenseclaims` → all 404 on IES
- Entity switch via: `/app/multiEntitySwitchCompany?companyId={CID}`
- NEVER do entity switches inside `browser_run_code` batches — causes "Execution context was destroyed"

## Key Learnings

1. **8-entity sweep is viable** — completed in ~60 min with P0 full + P1 minimal strategy
2. **JE fix pattern works** — negative P&L auto-fixed with JE, verified immediately
3. **IES consolidated view** has very limited pages (COA, IC Transactions, Consolidated Reports only)
4. **S01 false positive on Terra** — regex `/not found|404/i` matched content on a legitimate 468-line page
5. **Context compaction** — sweep spanned 2 conversation contexts due to token limits, but state preserved via LATEST_SWEEP.json progress tracking
