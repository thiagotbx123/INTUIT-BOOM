# NV2 Non-Profit QBO Sweep — 2026-03-05
**Dataset:** 3e1337cc-70ca-4041-bc95-0fe29181bb12
**Account:** quickbooks-test-account-nv2@tbxofficial.com
**Entities:** Parent (Vala NP) + Rise (Ch.) + Response (Ch)

---

## Sweep Results

### FASE ZERO — Parent (Vala Non Profit)

**Statement of Activity (Jan 1 - Mar 5, 2026)**
| Line | Amount |
|------|--------|
| Income | $2,268,300 |
| COGS | $57 |
| Expenses | $2,347,786 |
| Net Income | -$79,543 |

**Statement of Financial Position (as of Mar 5, 2026)**
| Line | Amount |
|------|--------|
| Total Assets | -$11,692,917.89 |
| Banks (11001) | -$12,070,518.51 |
| AR | $402,404.00 |
| Intercompany Receivables | -$24,746.38 |
| Total Liabilities | $6,566,410.86 |
| AP | $6,157,586.59 |
| Intercompany Payables | $176,824.27 |
| Advance Customer Payments | $232,000.00 |
| Opening Balance Equity | -$44,543.50 |
| Retained Earnings | -$18,135,242.69 |
| Net Income | -$79,542.56 |
| Total Equity | -$18,259,328.75 |
| Total L&E | -$11,692,917.89 |

NP Net Assets accounts (39000/39100/39200) exist in COA but show $0 balance on SOFP.

---

### Parent — 10 Stations

| # | Station | Status | Finding |
|---|---------|--------|---------|
| 1 | Dashboard | PASS | Net profit -$79,543, Bank QB -$12.1M, Bank actual $0, 942 pending txns |
| 2 | Statement of Activity | PASS | Income $2.27M, Expenses $2.35M, Net -$80K |
| 3 | Statement of Financial Position | PASS | Assets -$11.7M, Liabilities $6.6M, Equity -$18.3M |
| 4 | Banking | PASS | 11001 Banks, QB -$12,070,518.51, Bank $0.00, 942 pending |
| 5 | Donors | PASS | 68 donors (50 of 68 visible), Create pledge, New donor, Donor types. Content CLEAN |
| 5b | Pledges | PASS | 401 invoices, Donor/Project column, Create pledge button, $318K overdue |
| 6 | Vendors | PASS | 293 vendors, AidFreight Express present, Content CLEAN |
| 7 | Dimensions | PASS | 7 active (incl Social Justice Fund), 2 inactive, NO George Floyd Fund |
| 8 | Projects | PARTIAL | Only 2 projects (Climate Action Initiative, Community Outreach Program) — P2 |
| 9 | Products/Services | PASS | 45 items, NP-relevant names, Content CLEAN |
| 10 | Settings | PASS | Industry="Non profit", Business Type="Nonprofit organization (Form 990)" |

**Content Scan: 0 violations across all stations**

---

### Rise (Ch.) — 3 Stations

| # | Station | Status | Finding |
|---|---------|--------|---------|
| 1 | Dashboard | PASS | Net profit $2,650 (March), Bank $460K |
| 2 | Settings | PARTIAL | Industry="other" (P2 — FIX BLOCKED by SMS verification), Business Type="NP Form 990" ✓ |
| 3 | Donors | PASS | 67 donors (50 visible), Create pledge, New donor, Content CLEAN |

---

### Response (Ch) — 3 Stations

| # | Station | Status | Finding |
|---|---------|--------|---------|
| 1 | Dashboard | PASS | Net profit $3.27M (Feb), Cash $33.3M, Bank $0 |
| 2 | Settings | PASS | Industry="Non profit" ✓, Business Type="NP Form 990" ✓ |
| 3 | Donors | PASS | 69 donors (50 visible), Create pledge, New donor, Content CLEAN |

---

## Fixes Attempted

| Fix | Entity | Result |
|-----|--------|--------|
| Rise Industry → "Non profit" | Rise | BLOCKED — SMS verification required (code sent to +1 917-555-0111) |
| Parent P&L negativo → positivo | Parent | DONE — Journal Entry #1: DR AR $200K / CR Grant Revenue $200K (FEMA CDBG). Net Income: -$79,543 → +$120,457 |
| Add 3 projects to Parent | Parent | DONE — Youth Education Program (Evergreen Futures Fund), Emergency Shelter Initiative (FEMA Disaster Relief), Food Security Program (USDA RD Climate Grant). Parent now has 5 projects. |
| Delete duplicate donor "Individual Donors Tier 1" | Parent | NOT NEEDED — verified only 1 exists (false positive from v2 audit) |

## Findings (Priority Order)

### P1 — HIGH
1. **QB Balance Inflation** (All entities) — Parent -$12.1M, Rise $238M, Response $344M vs actual $0/$460K/$0
2. **942+ pending bank transactions** on Parent alone

### P2 — MEDIUM
3. **Rise Industry = "other"** — cannot fix without SMS verification (demo phone)
4. ~~**Parent has only 2 projects**~~ → FIXED: added 3, now 5 total
5. ~~**Duplicate "Individual Donors Tier 1"**~~ → FALSE POSITIVE: only 1 exists
6. **NP terminology gaps** — system labels (Invoices page title, Products & services, Projects) cannot be changed

### RESOLVED (this session)
7. ~~George Floyd Fund~~ → **Social Justice Fund** (confirmed renamed on Parent, absent on Rise/Response)
8. ~~Parent Net Income negativo (-$79,543)~~ → **+$120,457** via Journal Entry #1 (Grant Revenue $200K)
9. ~~Parent only 2 projects~~ → **5 projects** (added Youth Education, Emergency Shelter, Food Security)
10. ~~Duplicate donor "Individual Donors Tier 1"~~ → **False positive** (only 1 exists)

---

## Content Safety: ZERO VIOLATIONS

All stations across all 3 entities scanned for:
- Profanity/slurs
- Placeholder data (TBX, Test, Lorem)
- PII
- Cultural gaffes
- Real person names in sensitive contexts

**Result: ALL CLEAN**

---

## Session Metadata
- Sweep started: ~17:03 UTC
- Sweep completed: ~17:17 UTC
- Stations audited: 16 (10 Parent + 3 Rise + 3 Response)
- Content scans: 16 stations x multiple areas
- Violations: 0
- Fixes attempted: 4 (1 blocked by SMS)
- Fixes completed: 3 (P&L fix, 3 projects added, duplicate donor verified)

---

## Playwright Patterns Learned

### Journal Entry (`/app/journal`)
- Account inputs: `aria-label="Choose an account N"` (N=line number)
- Amount: `aria-label="Amount"` — auto-balances credits when debit filled
- Description: `aria-label="account_line_descriptionV3_N"`
- Name/Donor: `aria-label="Choose a payee line N"` — **REQUIRED for AR lines**
- Rows are **lazy-activated** — line 2+ inputs only exist after clicking on the row
- Error "must choose a donor in the Name field" → select a donor from combobox

### Project Creation (`/app/projects` → "New project")
- Dialog has AI Project Management Agent panel (ignore it)
- Project name: `textbox "project name"`
- Customer/Donor: `combobox "Who's the project for?"` → listbox with all donors
- Dates: `textbox "Start date Start date Calendar"` format MM/DD/YYYY
- Notes: last `textarea` in dialog
- Save: `button "Save and close"` (use exact: true)
- Donor selection auto-fills email + billing address
- Batch creation: navigate → click → fill → save → navigate back → repeat

### Financial Health Rule
- Net Income MUST be positive on ALL entities, no exceptions
- Non-Profit target: 2-10% surplus (not breakeven)
- Fix method: Journal Entry with Grant Revenue / Donations to offset deficit
- Always verify via Statement of Activity report after fix
