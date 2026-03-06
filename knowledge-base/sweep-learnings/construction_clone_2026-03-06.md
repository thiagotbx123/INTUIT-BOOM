# Construction Clone — QBO Sweep Report (v1)
**Date:** 2026-03-06 ~23:00-23:15 UTC
**Account:** quickbooks-testuser-construction-clone@tbxofficial.com
**Password:** TestBox123!
**TOTP Secret:** FV2K7O3V4XH7AZ2J3OLMXROHCBQNOTVQ
**Environment:** Production IES (Intuit Enterprise Suite)
**Industry:** Construction
**Overall Score: 7.5/10**

---

## Environment Overview

| Property | Value |
|----------|-------|
| Entities | 9 (1 Parent + 7 Children + Consolidated View) |
| Consolidated View | AVAILABLE (in entity selector) |
| Industry | Construction (all entities) |
| Business Type | Corporation (Form 1120) |
| User Name | Intuit Account (Q initial) |
| Login MFA | TOTP required + Passkey (skipped via "Ignorar") |
| Account Selector | "Restaure sua empresa" heading, 9 entities under "Intuit Enterprise Suite" |

---

## Companies Discovered

| Entity | Type | Notes |
|--------|------|-------|
| Keystone Construction (Parent) | parent | Main entity |
| Keystone BlueCraft | child | Has Payroll |
| KeyStone Canopy | child | Not audited this session |
| KeyStone Ecocraft | child | Not audited this session |
| KeyStone Ironcraft | child | Not audited this session |
| KeyStone Stonecraft | child | Not audited this session |
| Keystone Terra (Child) | child | Has Payroll |
| KeyStone Volt | child | Not audited this session |
| Consolidated View | consolidated | Via entity switcher |

**Note:** Entity naming is inconsistent — "Keystone" vs "KeyStone" (capital S) on child entities (Canopy, Ecocraft, Ironcraft, Stonecraft, Volt).

---

## Entity Audit Results

### Keystone Construction (Parent) — Score: 8/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | GOOD | P&L: Income $1.96M, Expenses $1.41M, Net +$554,782 (28% margin, up 10% from FY24) |
| Bank | PARTIAL | Total $11.39M. 1010 Checking: Bank $460K / QB $998K. Guardian Growth MMA: $10.9M (P1 systemic). |
| Invoices | GOOD | $994,048 unpaid, **$0 overdue** (all not due yet). $200K paid last 30 days. |
| AR | GOOD | $1,031,016 (100% Current — zero aging) |
| AP | GOOD | $1,538,443 ($1.25M current + $285K 1-30 days) |
| Sales | GOOD | $1,663,796 (6 months) |
| Expenses | PARTIAL | -$1,718,293 (30d, down 205% — spike). Categories: Job supplies, Purchases, Legal. |
| Settings | GOOD | Name correct, Industry=Construction, Corp 1120. |
| Content Safety | PASS | All clean. |

**Settings Detail:**
- Name: Keystone Construction (Parent) ✅
- Legal business name: Keystone Construction (Parent) ✅ (no swap)
- Email: contact@keystone-constructions.com
- Phone: 180012345670 (P2 — malformed)
- Address: 7535 Torrey Santa Fe Rd, San Diego, CA 92129-5704
- Legal address: 2600 Marine Way, Mountain View, CA 94043-1126 ✅ (correct ZIP)
- Customer address: 2600 Marine Way, Mountain View, California 92129 ⚠️ (P2 — ZIP mismatch)
- EIN: None listed
- Website: None listed
- i18n keys: NONE (clean)

**Bank accounts:** 1050 PayPal Bank ($0), 1030 Amazon Credit ($0), 1020 BOI Business Checking ($0), 1010 Checking (Bank $460K / QB $998K), Guardian Growth MMA ($10.9M/$10.9M), 1000 Petty Cash ($0), Cash ($0), 1810 Integra Arborists ($0)

**Features visible:** Accounting, Expenses, Sales, Customers, Payroll, Team, Time, Projects, Inventory, Sales Tax, Business Tax, Lending, Customer Hub

**Integrations:** 1 connected

---

### Keystone BlueCraft — Score: 7/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | GOOD | P&L: Income $1.93M, Expenses $1.62M, Net +$315,324 (16% margin, up 10% from FY24) |
| Bank | CRITICAL | BOI Business Checking: Bank $0 / QB **-$987,404** (NEGATIVE balance, P1). 1010 Checking: Bank $460K / QB $1.99M. Guardian Growth MMA: $10.9M (P1). |
| Invoices | GOOD | $438,974 unpaid, **$0 overdue**. $206K paid last 30 days. |
| Sales | GOOD | $683,951 (6 months) |
| Expenses | PARTIAL | $439,926 (FY25, down 73%). Categories: Purchases, Insurance, COGS. |
| Content Safety | PASS | All clean. |

**Bank accounts:** PayPal Bank ($0), Amazon Credit ($0), Guardian Growth MMA ($10.9M/$10.9M), 1010 Checking (Bank $460K / QB $1.99M), BOI Business Checking (Bank $0 / QB **-$987K**), Petty Cash ($0), Integra Arborists ($0)

**Key issues:**
- BOI Business Checking **NEGATIVE** QB balance (-$987K) — P1
- 488 transactions to review on BOI — highest in environment
- 56 + 16 additional txns to categorize

---

### Keystone Terra (Child) — Score: 8/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | GOOD | P&L: Income $755K, Expenses $439K, Net +$316,152 (42% margin, up 19% from FY25) |
| Bank | PARTIAL | 1010 Checking: Bank $460K / QB $1.67M. BOI: Bank $0 / QB $97K. Guardian Growth MMA: $10.9M (P1). |
| Invoices | GOOD | $111,940 unpaid, **$0 overdue**. $313K paid last 30 days. |
| Sales | GOOD | $348,519 (6 months) |
| Expenses | GOOD | $117,308 (30d, down 53%). Categories: Payroll, Purchases, Contractors. |
| Content Safety | PASS | All clean. |

**Bank accounts:** PayPal Bank ($0), Amazon Credit ($0), 1010 Checking (Bank $460K / QB $1.67M), BOI Business Checking (Bank $0 / QB $97K), Guardian Growth MMA ($10.9M/$10.9M), Petty Cash ($0), Integra Arborists ($0)

---

## Cross-Entity Comparison (3 Audited Entities)

| Metric | Construction (Par.) | BlueCraft | Terra |
|--------|---------------------|-----------|-------|
| **Score** | 8/10 | 7/10 | **8/10** |
| Income | $1,962,245 | $1,933,779 | $755,331 |
| Expenses | $1,407,463 | $1,618,455 | $439,179 |
| Net Income | **$554,782** | **$315,324** | **$316,152** |
| Margin | 28% | 16% | 42% |
| P&L Trend | Up 10% | Up 10% | Up 19% |
| Bank (Total) | $11.39M | $11.39M | $11.39M |
| 1010 Checking (QB) | $998K | $1.99M | $1.67M |
| 1010 Checking (Bank) | $460K | $460K | $460K |
| BOI Checking (QB) | $0 | **-$987K** | $97K |
| Guardian MMA | $10.9M | $10.9M | $10.9M |
| Invoices Unpaid | $994K | $439K | $112K |
| % Overdue | **0%** | **0%** | **0%** |
| AR | $1,031K | — | — |
| AP | $1,538K | — | — |
| Sales (6mo) | $1,664K | $684K | $349K |
| Txns to review | 36 + 16 | 488 + 56 + 16 | 80 + 47 + 18 |
| **TOTAL Income** | | **$3,651,355** | |
| **TOTAL Net** | | **$1,186,258** | |

---

## Findings (Priority Order)

### P1 — HIGH
1. **Guardian Growth MMA $10.9M — ALL entities**
   - Same systemic inflation seen across ALL IES environments (QSP, Product Events, Mid Market, NV3, now Construction Clone)
   - Bank balance = QB balance ($10.9M/$10.9M) — technically "reconciled" but inflated

2. **BlueCraft BOI Business Checking NEGATIVE (-$987K)**
   - QB balance is -$987,403.75 while Bank shows $0
   - This is worse than inflation — it's a negative ghost balance
   - 488 unreviewed transactions on this account

3. **1010 Checking QB inflation — ALL entities**
   - Parent: QB $998K vs Bank $460K (2.2x)
   - BlueCraft: QB $1.99M vs Bank $460K (4.3x)
   - Terra: QB $1.67M vs Bank $460K (3.6x)
   - All show Bank $460K — likely same connected bank account

### P2 — MEDIUM
4. **Customer address ZIP mismatch** — Mountain View, California 92129 (should be 94043). Same as ALL other IES environments.

5. **Malformed phone** — 180012345670 (extra digits, no formatting). Same as all IES environments.

6. **Entity naming inconsistency** — "Keystone" (Parent, BlueCraft, Terra) vs "KeyStone" (Canopy, Ecocraft, Ironcraft, Stonecraft, Volt). Capital S in 5 of 7 children.

7. **Missing EIN** — Parent has no EIN listed.

8. **High uncategorized transaction count** — BlueCraft 560 total (488 BOI + 56 + 16), Terra 145 total, Parent 52 total = **757 total across 3 entities**

### P3 — LOW
9. **Expense spike on Parent** — -$1,718,293 in last 30 days (down 205% from prior 30 days). May be seasonal or data population artifact.

10. **5 unaudited children** — Canopy, Ecocraft, Ironcraft, Stonecraft, Volt not audited this session. May have unique issues.

---

## Content Safety: ZERO VIOLATIONS

All 3 audited entities scanned for:
- Profanity/slurs
- Placeholder data (TBX, Test, Lorem, FLDN)
- PII
- Cultural gaffes
- Real person names in sensitive contexts

**Result: ALL CLEAN**

---

## Strengths

1. **ALL P&L positive** — Every audited entity has healthy positive net income ($316K-$555K)
2. **ZERO overdue invoices** — $0 overdue across all 3 entities (best of any IES environment)
3. **Healthy margins** — 16-42% across entities (realistic for construction)
4. **AR fully current** — $1.03M AR on Parent, 100% in "Current" bucket
5. **AP aging reasonable** — $1.54M AP with $1.25M current + $285K 1-30 days (no 90+ day aging)
6. **Correct legal names** — No name swaps (unlike QSP Events)
7. **Legal address ZIP correct** — Mountain View, CA 94043-1126 (only customer address has wrong ZIP)
8. **Rich feature set** — Full Construction IES with Payroll, Projects, Inventory, Customer Hub, Lending, Business Tax, Sales Tax
9. **8 entities** — Largest entity count of any audited environment

---

## Comparison: Construction Clone vs Other Environments

| Feature | Construction Clone | QSP Events | NV3 Manufacturing | Mid Market |
|---------|-------------------|------------|-------------------|------------|
| Score | **7.5/10** | 7.5/10 | 7.5/10 | 5.5/10 |
| Entities | **8 + Consolidated** | 3 + Consolidated | 3 + Consolidated | 1 (single) |
| Revenue (3 entities) | $3.65M | $14.2M | $40M+ | -$214K |
| Net Income | **+$1.19M** | +$5.03M | +$37.8M | -$214K |
| % Overdue | **0%** | ~30% | 93-100% | N/A |
| Content Safety | **CLEAN** | CLEAN | CLEAN | 10 test names |
| Legal Name Swap | **NO** | YES (BLOCKED) | NO | N/A |
| MMA Inflation | $10.9M (all) | $10.9M (all) | N/A | $10.9M |
| Negative Bank Balance | **BlueCraft -$987K** | BlueCraft $148.5M | N/A | Checking -$1.83M |
| Entity Naming | Inconsistent K/k | Correct | Correct | N/A |

---

## Login Flow Notes

- Email → Password (TestBox123!) → TOTP (via pyotp, secret FV2K7O3V4XH7AZ2J3OLMXROHCBQNOTVQ) → Passkey prompt (skipped "Ignorar") → Intuit Account Manager → QuickBooks → Terms dialog ("Continuar") → Entity Selector (9 entities) → QBO
- **TOTP REQUIRED** (MFA enforced)
- Entity selector page heading: "Restaure sua empresa" (Restore your company)
- Entity selector shows entities under "Intuit Enterprise Suite" heading

---

## Entity Switching Technical Notes

- Same pattern as other IES environments
- `page.evaluate` with `getComputedStyle(div).cursor === 'pointer'` to find entity name div
- `page.getByRole('menuitem', { name: '...', exact: true })` to select target entity
- Entity switching is session-sticky — works reliably between all entities
- No industry confirmation dialogs on entity switch

---

## Next Steps

1. **Audit remaining 5 children** — Canopy, Ecocraft, Ironcraft, Stonecraft, Volt (may have unique issues)
2. **Investigate BlueCraft BOI -$987K** — Why negative? Likely needs journal entry or reconciliation
3. **Fix entity naming** — Standardize "KeyStone" → "Keystone" on 5 children (or vice versa)
4. **Fix ZIP mismatch** — Customer address 92129 → 94043
5. **Verify Consolidated View** — Check if consolidated reports work correctly
6. **Categorize transactions** — 757 uncategorized across 3 entities

---

## Session Metadata
- Sweep started: ~23:00 UTC
- Sweep completed: ~23:15 UTC
- Stations audited: Dashboard (3 entities) + Settings (Parent) + Bank/Invoices/AR/AP/Sales (Parent)
- Entity switches: 3 (Construction → BlueCraft → Terra)
- Content scans: 3 (one per audited entity)
- Violations: 0
- Unaudited entities: 5 (Canopy, Ecocraft, Ironcraft, Stonecraft, Volt)
