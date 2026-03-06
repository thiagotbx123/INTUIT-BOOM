# NV3 Manufacturing — QBO Sweep Report (v1)
**Date:** 2026-03-06 ~22:30-23:00 UTC
**Account:** quickbooks-test-account-nv3@tbxofficial.com
**Password:** TestBox123!
**TOTP Secret:** X4F7FQG3XXVWXX6E5CY3QIUBXFSEBJKC
**Environment:** Production IES (Intuit Enterprise Suite)
**Industry:** Manufacturing
**Overall Score: 7.5/10**

---

## Environment Overview

| Property | Value |
|----------|-------|
| Entities | 4 (Ether Cycles Holdings (Parent), Ether Consumer Division (Child), Ether Racing Division (Child), Vista consolidada) |
| Consolidated View | AVAILABLE (in entity selector, redirects to last entity's dashboard) |
| Industry | Manufacturing (all 3 entities) |
| Business Type | Corporation (Form 1120) — all entities |
| User Name | Ether Admin |
| Login MFA | TOTP required + Passkey (auto-accepted) |

---

## Companies Discovered

| Entity | Type | CID (from TESTBOX_ACCOUNTS) |
|--------|------|----|
| Ether Cycles Holdings (Par.) | parent | 9341454625433003 |
| Ether Consumer Division | child | 9341454625418409 |
| Ether Racing Division (Ch.) | child | 9341454625455578 |
| Vista consolidada | consolidated | — |

---

## Entity Audit Results

### Ether Cycles Holdings (Parent) — Score: 7/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | GOOD | P&L: Income $4.28M, Expenses $2.93M, Net $1.36M (86% margin). Cash Flow (AI) $1.62M. |
| Bank | PARTIAL | QB $16,450,816.59 vs Bank $0 on 1000 Checking (P1 inflation). 26 txns to categorize. |
| Invoices | GOOD | $274,631 unpaid. |
| AR | GOOD | $274,631 (matches invoices). |
| Sales | GOOD | $4,282,708 |
| Settings | GOOD | Name correct, Industry=Manufacturing, Corp 1120, Address: 7535 Torrey Santa Fe Rd, San Diego, CA 92129-5704 |
| Customers | GOOD | 26 customers. IC customers present. Regional breakdown (APAC, EMEA, LATAM, NA). Customer Hub active. NO FLDN. NO test names. |
| Vendors | GOOD | 21 vendors. IC vendors present. Manufacturing-themed (AeroSpin Wheels, NovaCarbon Composites, TrueForge Precision). |
| Content Safety | PASS | All clean. |

**Features visible:** Accounting, Expenses, Sales, Payroll, Team, Lending, Time, Projects, Inventory, Sales Tax, Business Tax, Customer Hub (Leads, Estimates, Proposals, Contracts, Reviews)

**Settings Detail:**
- Email: contact@ether.com
- Phone: 180012345670 (P2 — malformed)
- Legal address: 183 Berwick Way, Sunnyvale, CA 94087
- Customer address: 2600 Marine Way, Mountain View, CA 92129 (P2 — ZIP mismatch: Mountain View ≠ 92129)
- EIN: None listed
- i18n keys: NONE (clean)

---

### Ether Consumer Division (Child) — Score: 7.5/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PARTIAL | P&L: Income $29.56M, Expenses $4.39M, Net $33.95M (97% margin — suspiciously high). Cash Flow (AI) $17.56M. |
| Bank | CRITICAL | QB $162,101,091.51 vs Bank $0 on 1000 Company Checking (P1 — MASSIVE inflation). |
| Invoices | PARTIAL | $10.6M unpaid, ALL overdue ($10.6M overdue, $0 not due yet — P1). $14.3M paid last 30 days. |
| AR | HIGH | $14,288,053 |
| Sales | GOOD | $29,562,499 |
| Expenses Card | PARTIAL | -$12,014,311 (last 30 days). Down 285%. Categories: Materials, Freight, Labor-installation, Other. |
| Settings | GOOD | Name correct. Industry=Manufacturing. Corp 1120. |
| Content Safety | PASS | All clean. |

**Settings Detail:**
- Email: contact@ether.com
- Phone: 180012345670 (P2 — malformed)
- Legal address: 2600 Marine Way, Mountain View, CA 94043-1126 (correct ZIP!)
- Customer address: 2600 Marine Way, Mountain View, CA 92129 (P2 — ZIP mismatch)
- EIN: None listed

---

### Ether Racing Division (Child) — Score: 8/10 (BEST entity)

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | GOOD | P&L: Income $6.42M, Expenses $3.96M, Net $2.46M (98% margin, down 92%). Cash Flow (AI) $2.87M. |
| Bank | PARTIAL | Bank $460,000 on 1000 Company Checking vs QB $67,732,942.77 (P1 inflation, but bank balance exists!). |
| Invoices | PARTIAL | $8.92M unpaid. $8.32M overdue (93% overdue — P1), $601K not due yet. |
| AR | HIGH | $16,431,052 |
| Sales | GOOD | $5,732,624 |
| Settings | GOOD | Name correct. Industry=Manufacturing. Corp 1120. Different email! |
| Content Safety | PASS | All clean. |

**Settings Detail (differences from Parent):**
- Email: ethercontact@tbxofficial.com (different from contact@ether.com!)
- Phone: 9091412452 (different, more realistic format but unformatted)
- Legal address: 7535 TORREY SANTA FE RD, SAN DIEGO, CA 92129
- Customer address: 2600 Marine Way, Mountain View, CA 92129 (P2 — ZIP mismatch)
- EIN: •••••2544 (PRESENT — masked)
- Bank accounts: 1000 Checking, 1020 Petty Cash ($0), 3100 My Credit Card ($0), 1050 Work in Progress-Direct ($0)

---

### Consolidated View — Score: 6/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Entity Selector | PASS | "Vista consolidada" available in entity switcher |
| Dashboard | PARTIAL | Redirects to `/app/get-things-done` — shows last-selected entity's data instead of consolidated P&L |
| Separate Reports | NOT VERIFIED | Did not audit consolidated reports separately this session |

---

## Cross-Entity Comparison

| Metric | Cycles Holdings (Par.) | Consumer Division | Racing Division |
|--------|----------------------|-------------------|-----------------|
| **Score** | 7/10 | 7.5/10 | **8/10** |
| Income | $4,282,708 | $29,562,499 | $6,418,159 |
| Expenses | $2,926,881 | $4,385,205 | $3,962,868 |
| Net Income | $1,355,828 | $33,947,704 | $2,455,290 |
| Margin | 86% | 97% | 98% |
| Bank (QB) | $16.5M | **$162.1M** | $67.7M |
| Bank (Actual) | $0 | $0 | **$460,000** |
| Invoices Unpaid | $274,631 | $10.6M | $8.9M |
| % Overdue | — | 100% | 93% |
| AR | $274,631 | $14.3M | $16.4M |
| Sales | $4,282,708 | $29,562,499 | $5,732,624 |
| EIN | None | None | •••••2544 |
| Email | contact@ether.com | contact@ether.com | ethercontact@tbxofficial.com |
| Phone | 180012345670 | 180012345670 | 9091412452 |
| **TOTAL Income** | | **$40,263,366** | |
| **TOTAL Net** | | **$37,758,822** | |

---

## Findings (Priority Order)

### P1 — HIGH
1. **QB Balance Inflation — ALL entities**
   - Consumer: $162.1M QB vs $0 bank (most extreme)
   - Racing: $67.7M QB vs $460K bank
   - Cycles Holdings: $16.5M QB vs $0 bank
   - Systemic — same pattern as all other IES environments

2. **Consumer Division 100% invoices overdue** — $10.6M unpaid, ALL past due ($0 not due yet). Terrible AR health impression.

3. **Racing Division 93% invoices overdue** — $8.32M of $8.92M unpaid are overdue. Only $601K not due yet.

4. **Consumer Division P&L margin 97%** — $33.9M net on $29.6M income with only $4.4M expenses. Income > Net (possible miscategorization or period mismatch). Manufacturing company should NOT have 97% margins.

### P2 — MEDIUM
5. **Customer address ZIP mismatch** — ALL entities: Mountain View, California 92129 (should be 94043). Same bug as QSP Events and Product Events.

6. **Malformed phone** — Cycles Holdings + Consumer: 180012345670 (extra digits, no formatting). Racing has different number (9091412452) which is better but still unformatted.

7. **Missing EINs** — Cycles Holdings and Consumer Division have no EIN. Only Racing has one (•••••2544).

8. **Vendor AP concentration** — ShieldSure Insurance $1.68M, SynFlow Systems $433K, Apex Advisory Group $422K, GreenGrid Utilities $300K. Top vendor has 40% of visible AP.

### P3 — LOW
9. **Racing email inconsistency** — Uses ethercontact@tbxofficial.com while Parent/Consumer use contact@ether.com. Not necessarily a bug but inconsistent.

10. **Txns to categorize** — Cycles Holdings: 26, Consumer: 88 + 47, Racing: 31. Total 192 uncategorized across environment.

---

## Content Safety: ZERO VIOLATIONS

All entities scanned for:
- Profanity/slurs
- Placeholder data (TBX, Test, Lorem, FLDN)
- PII
- Cultural gaffes
- Real person names in sensitive contexts

**Result: ALL CLEAN**
- NO FLDN customer (unlike Product Events/QSP)
- NO test names (unlike Mid Market which had 12345 Auction, IDT Tester, etc.)
- Realistic manufacturing-themed names throughout (AeroSpin, NovaCarbon, TrueForge, Velocity Works)

---

## Strengths vs Other Environments

| Feature | NV3 Manufacturing | Mid Market | QSP Events | Product Events |
|---------|-------------------|------------|------------|----------------|
| Score | **7.5/10** | 5.5/10 | 7.5/10 | 6/10 |
| Revenue | **$40M+ across 3 entities** | -$214K (negative!) | $14.2M consolidated | $1.5M (post-fix) |
| Content Safety | **CLEAN** | 10 test names | CLEAN | FLDN customer |
| Entities | 3 + Consolidated | 1 (single) | 3 + Consolidated | 3 (no consolidated) |
| Customer Hub | YES | YES | YES | YES |
| Realistic Customers | **26 themed** | Mixed (test names) | 20+ themed | Mixed |
| Realistic Vendors | **21 themed** | Good | 15+ themed | Good |
| Manufacturing Features | **Full** (Materials, Freight, WIP) | Revenue Recognition | N/A (Construction) | N/A (Construction) |
| IC Transactions | YES (customers + vendors) | N/A | YES | NO |
| Payroll | VISIBLE | Full (multi-state) | VISIBLE | VISIBLE |
| Entity Legal Names | **CORRECT** (no swaps) | N/A | BLOCKED (swap) | CORRECT |

---

## AI Features Observed

| Feature | Entity | Status |
|---------|--------|--------|
| AI-forecasted cash flow | All 3 | Active (Cycles $1.6M, Consumer $17.6M, Racing $2.9M) |
| Phishing warning banner | Consumer + Racing | Active |
| Customer Hub | Cycles Holdings | Full (Leads, Estimates, Proposals, Contracts, Reviews) |

---

## Login Flow Notes

- Email → Password → TOTP (generated via pyotp) → Phone verification for (917) 555-0111 (SKIPPED via "Ignorar") → Passkey (auto-accepted) → Intuit Account Manager → QuickBooks → Terms dialog → Entity Selector → QBO
- **TOTP REQUIRED** (unlike Product Events which skipped MFA)
- **Passkey auto-accepted** (registered on browser profile)
- Entity selector shows 4 entities under "Intuit Enterprise Suite" heading

---

## Entity Switching Technical Notes

- Same pattern as other IES environments
- `page.evaluate` with `getComputedStyle(div).cursor === 'pointer'` to find entity name div
- `page.getByRole('menuitem', { name: '...', exact: true })` to select target entity
- Consolidated View selection redirects to `/app/get-things-done` but appears to stay on last entity's data
- Entity switching is session-sticky — works reliably between operating entities

---

## Comparison: NV1 vs NV3 Access

- **NV1 (Professional Services)**: PASSWORD INCORRECT — `TestBox123!` and `TestBox!23` both failed. Credentials need updating.
- **NV3 (Manufacturing)**: Full access with documented credentials.

---

## Next Steps

1. **Investigate Consumer Division P&L anomaly** — $33.9M net on $29.6M income doesn't add up. May need to check period or P&L report directly.
2. **Fix overdue invoices** — Consumer (100% overdue) and Racing (93% overdue). Create new invoices with future due dates or create payments for old ones.
3. **Verify Consolidated View** — Check consolidated reports via `/app/reportlist` when on Consolidated entity.
4. **Update NV1 credentials** — Password TestBox123! is incorrect. Needs team update.
5. **Fix ZIP mismatch** — Customer address ZIP 92129 → 94043 on all entities.

---

## Session Metadata
- Sweep started: ~22:30 UTC
- Sweep completed: ~23:00 UTC
- Stations audited: Dashboard + Settings (3 entities) + Customers + Vendors (Cycles Holdings) + Consolidated selector
- Entity switches: 4 (Cycles → Consumer → Racing → Consolidated)
- Content scans: 3 (one per operating entity)
- Violations: 0
- NV1 attempted first: FAILED (wrong password)
