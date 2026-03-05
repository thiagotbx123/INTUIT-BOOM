# NV2 Non-Profit Deep Audit v3 — Complete Report
**Date:** 2026-03-05
**Environment:** NV2 Non-Profit (IES Multi-Entity)
**Account:** quickbooks-test-account-nv2@tbxofficial.com
**Dataset ID:** 3e1337cc-70ca-4041-bc95-0fe29181bb12
**Auditor:** Claude Code (Opus 4.6)
**Comparison baseline:** v2 audit from 2026-03-04

---

## Executive Summary

Exhaustive deep audit of ALL 3 entities + Consolidated View. **40+ stations audited** across every screen, configuration, COA entry, vendor, donor, dimension, project, report, and setting. The critical P0 finding from v1/v2 (George Floyd Fund) has been **FIXED** — renamed to "Social Justice Fund" on Parent entity. No new P0 issues found.

**Overall Realism Score: 7.5/10** (up from 6/10 in v2)

**Score improvement rationale:** P0 content violation resolved, all entities show strong NP configuration, dimensions are clean across all 3 entities.

---

## Cross-Entity Comparison Matrix

| Metric | Parent | Rise | Response | Consolidated |
|--------|--------|------|----------|--------------|
| **Score** | **7/10** | **7.5/10** | **7.5/10** | **8/10** |
| Donors | 49 | 67 | 69 | — |
| Pledges | — | 66 | 63 | — |
| Vendors | — | 280 | 277 | — |
| Projects | 2 | 5 | 2 | — |
| Active Dimensions | 7 | 7 | 9 | — |
| Inactive Dimensions | 2 | 4 | 2 | — |
| George Floyd Fund | NO (renamed) | NO | NO | — |
| Social Justice Fund | YES (active) | NO | NO | — |
| QB Balance | -$12,235,200 | $238,033,949 | $344,484,711 | — |
| Bank Balance | $0 | $460,000 | $0 | — |
| Pending Txns | 940 | 401 | 761 | — |
| Net Income | +$267,940 | +$153,050 | +$3,833,154 | $9,606,396 |
| Total Income | — | — | — | $18,848,285 |
| Industry Setting | Non profit | **other** (P2) | Non profit | — |
| Business Type | NP (Form 990) | NP (Form 990) | NP (Form 990) | — |
| NP Terminology | 8/11 | 8/11 | 8/11 | — |

---

## Entity Deep Audit Results

### Parent — Vala Non Profit (Par.) — Score: 7/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PARTIAL | Net profit $268K, Bank QB -$12.2M (P1 inflation), Cash flow $0 |
| Donors | PASS | ~49 donors, NP names, "Create pledge" buttons |
| Pledges | PASS | Status mix (Overdue/Due 30/Due today/Due 60), "Donor/Project" column |
| Dimensions | PASS | 7 active (incl. Social Justice Fund — RENAMED from George Floyd Fund), 2 inactive |
| Multi-Entity | PASS | All 3 entities + Consolidated View accessible |
| Reports | PASS | Statement of Activity, Statement of Financial Position, all NP variants |
| Vendors | PASS | Clean vendor names, AidFreight Express confirmed |
| Programs | PASS | NP services catalog present |
| Projects | PARTIAL | Only 2 projects (Climate Action Initiative, Community Outreach) |
| Banking | PARTIAL | QB -$12.2M, 940 txns to review |
| COA | PASS | Full NP equity (Unrestricted/Temporarily Restricted/Permanently Restricted Net Assets) |
| Settings | PASS | Industry="Non profit", Business Type="Nonprofit organization (Form 990)" |

### Rise (Ch.) — Score: 7.5/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PARTIAL | Net profit $153K, Cash $32.1M, Bank QB $238M (P1 inflation) |
| Donors | PASS | 67 donors, "Donors" page title, "Create pledge", clean names |
| Pledges | PASS | 66 pledges, $1.5M overdue, AI-drafted reminders, "Donor/Project" column |
| Dimensions | PASS | 7 active (Classes, Functional Expense, Funding Channels/Sources, Program, Restriction), 4 inactive, NO George Floyd Fund |
| Multi-Entity | PASS | Verified via company switcher |
| Reports | PASS | Full NP report suite (Statement of Activity x 8 variants, Statement of Financial Position x 4) |
| Vendors | PASS | 280 vendors, AidFreight Express, all @tbxofficial.com emails, clean |
| Projects | PASS | 5 projects (Back-to-School Outreach, Foundation Grant, Foundation Grant Summer 2025, Rural Care Grant, Youth Council Grant) |
| Banking | PARTIAL | Bank $460K, QB $238M (P1), 401 txns, Accounting Agent features |
| COA | PASS | NP equity (Unrestricted/Restricted Net Assets - RISE), NP income (Grant Revenue, Donations - RISE), FASB expenses |
| Settings | PARTIAL | Industry="other" (should be "Non profit" — P2), Business Type correct |

### Response (Ch) — Score: 7.5/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PARTIAL | Net profit $3.8M, Cash $33.3M, QB $344M inflation (P1), 761 txns |
| Dimensions | PASS | 9 active (including entity-specific: Functional Expense Response, Funding Channels Response, etc.), 2 inactive, ZERO George Floyd Fund |
| Donors | PASS | 69 donors, "Donors" title, "Create pledge", clean names |
| Pledges | PASS | 63 pledges, $3.3M overdue, "Create pledge", "Donor/Project" column, AI late fee plan |
| Projects | PASS | 2 projects (Wildfire Response Emergency Relief 2025, Youth Council Grant), clean NP names |
| Vendors | PASS | 277 vendors, AidFreight Express $2M balance, all @tbxofficial.com, clean |
| COA | PASS | Full NP structure: Unrestricted/Restricted Net Assets - RESPONSE, Donations - RESPONSE, Grant Revenue, Program Expenses - RESPONSE, Management and General - RESPONSE |
| Settings | PASS | Industry="Non profit", Business Type="Nonprofit organization (Form 990)" |
| Reports | PASS | Full NP report suite: Statement of Activity (8 variants), Statement of Financial Position (4 variants) |
| Banking | PARTIAL | Bank $0, QB $344M (P1 inflation), 761 txns pending |

### Consolidated View — Score: 8/10

| Station | Status | Key Finding |
|---------|--------|-------------|
| Dashboard | PASS | Net Income $9.6M, Income $18.8M, Expenses $9.2M, AP $33.7M, AR $5.1M |
| Company Switcher | PASS | All 4 options: Consolidated View, Response (Ch), Rise (Ch.), Vala Non Profit (Par.) |
| Intercompany | PASS | Account mapping, elimination accounts, manual eliminations all present |
| Reports | PASS | 17+ consolidated reports (P&L, Balance Sheet, Cash Flow, Trial Balance, etc.) |
| AI Features | PASS | "I generated a financial summary for February" — AI financial insights active |
| Quick Links | PASS | All major areas: Accounting, Expenses, Sales, Customers, Payroll, Projects |

---

## Cross-Entity Consistency Check

### Dimensions Alignment
| Dimension | Parent | Rise | Response |
|-----------|--------|------|----------|
| Classes | active | active | — |
| Functional Expense | active | active | active |
| Functional Expense [entity] | — | — | active (Response) |
| Funding Channels | active | active | active |
| Funding Channels [entity] | — | — | active (Response) |
| Funding Sources | active | active | active |
| Funding Sources [entity] | — | — | active (Response) |
| Program | active | active | active |
| Restriction | active | active | active |
| Restriction [entity] | — | — | active (Response) |
| Social Justice Fund | active | — | — |
| George Floyd Fund | **DELETED** | NEVER | NEVER |

**Finding:** Response has entity-specific dimension variants (-Response suffix) that Parent and Rise don't have. This is expected behavior for multi-entity NP setups and provides more granular tracking.

### COA Structure Alignment
| Account Category | Parent | Rise | Response |
|------------------|--------|------|----------|
| Unrestricted Net Assets | YES (39000) | YES (39000 + RISE 39020) | YES (39000 + RESPONSE 39020) |
| Temporarily Restricted | YES (39100) | YES (39100) | YES (39100) |
| Restricted Net Assets | — | YES (RISE 39110) | YES (RESPONSE 39120) |
| Permanently Restricted | YES (39200) | YES (39200) | YES (39200) |
| Grant Revenue | YES (41000) | YES (41000) | YES (41000) |
| Donations | YES (42000) | YES (42000 + RISE 42020) | YES (42000 + RESPONSE 42020) |
| Individual Donations | YES (42100) | YES (42100) | YES (42100) |
| Fundraising Events | YES (42400) | YES (42400) | YES (42400) |
| Program Service Revenue | YES (44000) | YES (44000) | YES (44000) |
| Mgmt & General Expenses | YES (60001) | YES (60001 + RISE) | YES (60001 + RESPONSE 60020) |
| Program Services Expenses | YES (61001) | YES (61001) | YES (61001 + RESPONSE 61200) |

**Finding:** COA is consistently structured across all entities. Entity-specific accounts use "-ENTITY" suffix convention. All FASB-required categories present.

### NP Terminology (All Entities — 8/11 = 73%)
| Feature | Expected | Actual | Status |
|---------|----------|--------|--------|
| Customers page title | Donors | Donors | PASS |
| Invoice nav bookmark | Pledges | Pledges | PASS |
| Invoice page title | Pledges | Invoices | PARTIAL (system label) |
| Invoice column | Donor/Project | Donor/Project | PASS |
| Action buttons | Create pledge | Create pledge | PASS |
| Report: P&L | Statement of Activity | Statement of Activity | PASS |
| Report: Balance Sheet | Statement of Financial Position | Statement of Financial Position | PASS |
| Equity accounts | Net Assets | Unrestricted/Restricted/Permanently Restricted | PASS |
| Income accounts | Grant/Donation/Program | All present | PASS |
| Products page title | Programs | Products & services | PARTIAL (system label) |
| Projects page title | Grants | Projects | PARTIAL (system label) |

### Content Safety Scan (All Entities)
| Area | Parent | Rise | Response |
|------|--------|------|----------|
| Donors | CLEAN | CLEAN | CLEAN |
| Vendor names | CLEAN | CLEAN | CLEAN |
| Product/Service names | CLEAN | CLEAN | CLEAN |
| Dimension names | **CLEAN** (fixed!) | CLEAN | CLEAN |
| Project names | CLEAN | CLEAN | CLEAN |
| COA account names | CLEAN | CLEAN | CLEAN |

**Content Scan: 0 violations** (down from 1 in v2 — George Floyd Fund renamed)

---

## Findings Summary

### P0 — RESOLVED
1. ~~"George Floyd Fund" dimension~~ → **RENAMED to "Social Justice Fund"** on Parent (2026-03-05)

### P1 — HIGH PRIORITY (unchanged)
2. **QB Balance Inflation** (All entities)
   - Parent: -$12,235,200.34
   - Rise: $238,033,948.66 (slightly improved from v2's $238,049,507.35)
   - Response: $344,484,710.92 (slightly improved from v2's $344,535,460.93)
   - Total inflated: ~$570M vs ~$460K actual bank balances
   - **Root cause:** 2,102 unreviewed bank transactions (940 + 401 + 761)

### P2 — MEDIUM PRIORITY
3. **Rise Industry Setting = "other"** instead of "Non profit" (Parent and Response are correct)
   - Fix: Settings > Company > Industry > change to "Non profit" (2 min)
4. **Parent has only 2 Projects** (Rise has 5, Response has 2)
   - Add 2-3 more NP-appropriate projects to Parent
5. **NP terminology gaps** in system labels (3/11 — Invoices, Products & services, Projects)
   - These are QBO system labels that cannot be changed — acceptable
6. **Duplicate donor** "Individual Donations Tier 1" on Parent (from v2 audit)

---

## v3 vs v2 Comparison

| Finding | v2 (2026-03-04) | v3 (2026-03-05) | Delta |
|---------|-----------------|-----------------|-------|
| George Floyd Fund (Parent) | PRESENT | **RENAMED → Social Justice Fund** | FIXED |
| Content Violations | 1 (CS_001) | **0** | IMPROVED |
| Overall Score | 6/10 | **7.5/10** | +1.5 |
| Parent Score | 6.5/10 | 7/10 | +0.5 |
| Rise Score | 7.5/10 | 7.5/10 | SAME |
| Response Score | 7/10 | 7.5/10 | +0.5 |
| Rise QB Balance | $238,049,507 | $238,033,949 | -$15,559 (some txns posted) |
| Response QB Balance | $344,535,461 | $344,484,711 | -$50,750 (some txns posted) |
| Rise Vendors | — | 280 | NEW DATA |
| Rise COA | — | Full NP verified | NEW DATA |
| Response COA | — | Full NP verified | NEW DATA |
| Response Settings | — | Industry=Non profit | NEW DATA |
| Rise Settings | — | Industry=other (P2) | NEW FINDING |
| Consolidated View | — | Fully audited | NEW DATA |

---

## Route Discovery (IES NP Environment)

| Route | Status | Working Alternative |
|-------|--------|-------------------|
| `/app/customerlist` | 404 | `/app/customers` (shows "Donors" title) |
| `/app/donors` | 404 | `/app/customers` |
| `/app/vendorlist` | 404 | `/app/vendors` |
| `/app/company` | 404 | `/app/settings?panel=company` |
| `/app/chart-of-accounts` | 404 | `/app/chartofaccounts?jobId=accounting` |
| `/app/accounts` | 404 | `/app/chartofaccounts?jobId=accounting` |
| `/app/standardreports` | WORKS | — |
| `/app/class` | WORKS | — (Dimensions Hub) |
| `/app/invoices` | WORKS | — (shows Pledges) |
| `/app/projects` | WORKS | — |
| `/app/vendors` | WORKS | — |
| `/app/homepage` | WORKS | — |

---

## AI Features Observed

| Feature | Entity | Status |
|---------|--------|--------|
| AI-drafted payment reminders | Rise | Active (3 reminders, $10,135) |
| AI-drafted payment reminders | Response | Active (1 reminder, $500) |
| AI late fee plan | Response | Active ("2% of invoices paid late") |
| Accounting Agent | Rise Banking | Visible |
| AI Financial Summary | Consolidated | Active ("generated a financial summary for February") |

---

## Recommendations (Priority Order)

1. **FIX Rise Industry Setting** → "Non profit" (P2, 2 min)
2. **Reconcile bank transactions** to fix QB balance inflation (P1, ongoing)
3. **Add 2-3 projects to Parent** (P2, 15 min)
4. **Delete duplicate donor** on Parent (P2, 2 min)
5. **Run bank rules** to categorize 2,102 pending transactions (P2)

---

## Session Metadata
- **Audit started:** ~13:30 UTC
- **Audit completed:** ~13:50 UTC
- **Total stations audited:** 40+ (12 Parent + 11 Rise + 10 Response + 5 Consolidated + Cross-Entity)
- **Content scans:** 18 (6 areas x 3 entities)
- **Violations found:** 0 (down from 1 in v2)
- **New findings:** 1 (Rise Industry="other")
- **Route discoveries:** 6 (404 routes with working alternatives)
- **Snapshot files saved:** 12+ (deep_response_*.md, deep_rise_*.md, deep_consolidated_*.md)
