# NV2 Non-Profit Health Check v2 — Complete Audit Report
**Date:** 2026-03-04
**Environment:** NV2 Non-Profit (IES Multi-Entity)
**Account:** quickbooks-test-account-nv2@tbxofficial.com
**Dataset ID:** 3e1337cc-70ca-4041-bc95-0fe29181bb12
**Comparison baseline:** v1 audit from same date

---

## Executive Summary

Re-audited all 3 entities across 10 stations each (30 stations total). All v1 findings confirmed — **no regressions, no improvements**. The P0 content violation (George Floyd Fund on Parent) remains. QB balance inflation persists across all entities.

**Overall Realism Score: 6/10** (unchanged from v1 post-audit)

---

## v2 vs v1 Comparison

| Finding | v1 | v2 | Delta |
|---------|----|----|-------|
| George Floyd Fund (Parent) | PRESENT | PRESENT | NO CHANGE |
| George Floyd Fund (Rise) | ABSENT | ABSENT | OK |
| George Floyd Fund (Response) | ABSENT | ABSENT | OK |
| Parent QB Balance | -$12.2M | -$12,235,200.34 | SAME |
| Rise QB Balance | $238M | $238,049,507.35 | SAME |
| Response QB Balance | $344M | $344,535,460.93 | SAME |
| Parent Projects | 2 | 2 | SAME |
| Rise Projects | 5 | 5 | SAME |
| Response Projects | 2 visible | 2 visible (In Progress) | SAME |
| NP Terminology | 8/11 | 8/11 | SAME |
| Content Violations | 1 (CS_001) | 1 (CS_001) | SAME |

**Conclusion:** Environment is stable. No drift detected between v1 and v2.

---

## Entity Summaries

### Parent — Vala Non Profit (Par.)

| # | Station | Status | v2 Key Finding |
|---|---------|--------|----------------|
| 1 | Dashboard | PARTIAL | Net profit $268K, Bank QB: -$12,235,200.34, Cash flow $0 |
| 2 | Donors | PASS | ~49 donors, NP names, "Create pledge" buttons, "New donor" button |
| 3 | Pledges | PASS | Status mix (Overdue/Due 30/Due today/Due 60), "Donor/Project" column |
| 4 | Dimensions | **FAIL (P0)** | **"George Floyd Fund" still present. 5 active, 2 inactive.** |
| 5 | Multi-Entity | PASS | All 3 entities + Consolidated View accessible |
| 6 | Reports | PASS | Standard reports, Custom reports, KPIs, Dashboards, Financial planning |
| 7 | Vendors | PASS | Clean vendor names (AidFreight Express confirmed) |
| 8 | Programs | PASS | NP services catalog present |
| 9 | Projects | PARTIAL | Only 2 projects (Climate Action Initiative, Community Outreach) |
| 10 | Banking | PARTIAL | QB: -$12,235,200.34, 940 txns to review |

**Parent Score: 6.5/10** (unchanged)

### Rise (Ch.)

| # | Station | Status | v2 Key Finding |
|---|---------|--------|----------------|
| 1 | Dashboard | PARTIAL | Net profit $153,050, Cash $32.1M, Bank QB: $238,049,507.35 |
| 2 | Donors | PASS | "Donors" page title, Atlantic Conservation Trust, "Create pledge" |
| 3 | Pledges | PASS | AI-drafted reminders feature, "Donor/Project" column |
| 4 | Dimensions | PASS | 6 active (Classes, Functional Expense, Funding Channels/Sources, Program, Restriction), 4 inactive, NO George Floyd Fund |
| 5 | Multi-Entity | PASS | Verified via company switcher |
| 6 | Reports | PASS | Full report suite with KPIs, Dashboards, Financial planning |
| 7 | Vendors | PASS | AidFreight Express confirmed, clean names |
| 8 | Programs | PASS | Same NP product catalog |
| 9 | Projects | PASS | 5 projects (Back-to-School Outreach, Foundation Grant, Foundation Grant Summer 2025, Rural Care Grant, Youth Council Grant) |
| 10 | Banking | PARTIAL | QB: $238,049,507.35, Bank: $460,000, 400 txns to review |

**Rise Score: 7.5/10** (unchanged)

### Response (Ch)

| # | Station | Status | v2 Key Finding |
|---|---------|--------|----------------|
| 1 | Dashboard | PARTIAL | Net profit $3,833,154.34, Cash $33.3M, Bank QB: $344,535,460.93 |
| 2 | Donors | PASS | "Donors" page title, "New donor" button, "Donor types" button |
| 3 | Pledges | PASS | $3.3M overdue, AI drafted 1 reminder ($500), "Create pledge" |
| 4 | Dimensions | PASS | 8 active dimensions (shared + local Response variants), 2 inactive, NO George Floyd Fund |
| 5 | Multi-Entity | PASS | Verified via company switcher |
| 6 | Reports | PASS | Full report suite (Standard, Custom, Management, KPIs, Dashboards, Financial planning) |
| 7 | Vendors | PASS | AidFreight Express ($2,021,192.39 balance), clean names |
| 8 | Programs | PASS | "Products and services" page (system label), same NP catalog |
| 9 | Projects | PASS | 2 projects visible (Wildfire Response Emergency Relief 2025, Youth Council Grant) |
| 10 | Banking | PARTIAL | QB: $344,535,460.93, Bank: $0.00, 761 txns to review |

**Response Score: 7/10** (unchanged)

---

## Critical Findings (Unchanged from v1)

### P0 — MUST FIX BEFORE DEMO
1. **"George Floyd Fund" dimension** (Parent only, `/app/class`)
   - Still present in v2 audit
   - Fix: Rename to "Social Justice Fund" or "Community Justice Initiative"

### P1 — HIGH PRIORITY
2. **QB Balance Inflation** (All entities)
   - Parent: -$12,235,200.34
   - Rise: $238,049,507.35
   - Response: $344,535,460.93
   - Total inflated: ~$570M vs ~$460K actual bank balances

3. **2,101 bank transactions to review** (940 + 400 + 761)

### P2 — MEDIUM PRIORITY
4. **Parent has only 2 Projects** (Rise has 5)
5. **Duplicate donor** "Individual Donations Tier 1" on Parent
6. **NP terminology gaps** in system page titles (Invoices, Products & services, Projects)

---

## Content Scan Results

| Area | Parent | Rise | Response |
|------|--------|------|----------|
| Donors | CLEAN | CLEAN | CLEAN |
| Vendor names | CLEAN | CLEAN | CLEAN |
| Product/Service names | CLEAN | CLEAN | CLEAN |
| Dimension names | **FAIL** (George Floyd Fund) | CLEAN | CLEAN |
| Project names | CLEAN | CLEAN | CLEAN |

**Content Scan: 1 violation** (CS_001: Real person name in sensitive context) — unchanged

---

## Financial Summary

| Entity | Net Profit | QB Balance | Bank Balance | Pending Txns |
|--------|------------|------------|--------------|-------------|
| Parent | +$267,940 | -$12,235,200.34 | $0 | 940 |
| Rise | +$153,050 | $238,049,507.35 | $460,000 | 400 |
| Response | +$3,833,154 | $344,535,460.93 | $0 | 761 |
| **Total** | **$4,254,144** | **$570M+** | **$460K** | **2,101** |

---

## NP Terminology Adoption (8/11 — 73%)

| Feature | Expected | Actual | Status |
|---------|----------|--------|--------|
| Customers page title | Donors | Donors | PASS |
| Invoice nav bookmark | Pledges | Pledges | PASS |
| Invoice page title | Pledges | Invoices | PARTIAL |
| Invoice column | Donor/Project | Donor/Project | PASS |
| Action buttons | Create pledge | Create pledge | PASS |
| Report name | Statement of Activity | Statement of Activity | PASS |
| Equity accounts | Net Assets | Unrestricted/Restricted | PASS |
| Income accounts | Grant/Program Revenue | Both present | PASS |
| Expense categories | Mgmt & General, Program | Both present | PASS |
| Products page title | Programs | Products & services | PARTIAL |
| Projects page title | Grants | Projects | PARTIAL |

---

## New Observations in v2 (not in v1)

1. **AI-drafted reminders**: Both Rise and Response show AI-drafted payment reminders feature (Rise: 3 reminders worth $10,135, Response: 1 reminder worth $500)
2. **Response Projects detail**: Wildfire Response Emergency Relief 2025 (customer: OR Wildfire Recovery Grant, dates: Mar-Dec 2025) — well-crafted NP project name
3. **Response vendor balance**: AidFreight Express shows $2,021,192.39 — very high for a non-profit vendor relationship

---

## Recommendations (Priority Order — Unchanged)

1. **RENAME "George Floyd Fund"** → "Social Justice Fund" (P0, 5 min)
2. **Reconcile bank transactions** to fix QB balance inflation (P1)
3. **Add 2-3 projects to Parent** (P2, 15 min)
4. **Delete duplicate donor** on Parent (P2, 2 min)
5. **Run bank rules** to categorize 2,101 pending transactions (P2)

---

## Session Info
- **v2 audit started:** ~21:50 UTC
- **v2 audit completed:** ~22:05 UTC
- **Stations audited:** 30 (10 x 3 entities)
- **Content scans:** 15 (5 areas x 3 entities)
- **Violations found:** 1 (P0 — George Floyd Fund, Parent only)
- **Environment stability:** CONFIRMED — no drift between v1 and v2
- **Snapshot files:** v2_rise_homepage.md, v2_rise_donors.md, v2_rise_dimensions.md, v2_rise_vendors.md, v2_response_homepage.md, v2_response_dimensions.md, v2_response_vendors.md
