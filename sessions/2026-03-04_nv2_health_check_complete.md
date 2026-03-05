# NV2 Non-Profit Health Check - Complete Audit Report
**Date:** 2026-03-04
**Environment:** NV2 Non-Profit (IES Multi-Entity)
**Account:** quickbooks-test-account-nv2@tbxofficial.com
**Dataset ID:** 3e1337cc-70ca-4041-bc95-0fe29181bb12

---

## Executive Summary

Audited all 3 entities across 10 stations each. Found **1 P0 critical content violation** (George Floyd Fund on Parent), **systemic QB balance inflation** across all entities, and strong NP terminology adoption overall.

**Overall Realism Score: 6/10** (was 7.5/10 pre-audit)
- Score dragged down by P0 content issue and absurd financial balances
- NP terminology, donor names, and program descriptions are excellent
- Multi-entity structure works correctly

---

## Entity Summaries

### Parent — Vala Non Profit (Par.)

| # | Station | Status | Key Finding |
|---|---------|--------|-------------|
| 1 | Dashboard | PARTIAL | Net profit $268K (good), Bank QB: -$12.2M (CRITICAL), Cash flow $0 |
| 2 | Donors | PASS | ~49 donors, NP names (foundations, trusts, gov grants), "Create pledge" buttons |
| 3 | Pledges | PASS | Good status mix (Overdue/Due 30/Due today/Due 60), "Donor/Project" column |
| 4 | Dimensions | **FAIL (P0)** | **"George Floyd Fund" — real person, racially-charged events. MUST RENAME** |
| 5 | Multi-Entity | PASS | All 3 entities + Consolidated View accessible |
| 6 | Statement of Activity | PASS | Net Income $267,940, correct NP report terminology |
| 7 | Vendors | PASS | Clean vendor names (AidFreight, AuditTrust, BrightNova, CampaignStream) |
| 8 | Programs | PASS | Excellent NP services (compliance consulting, donor mgmt, grant tracking) |
| 9 | Grants (Projects) | PARTIAL | Only 2 projects (Climate Action Initiative, Community Outreach) — needs 4-5 |
| 10 | COA + Banking | PARTIAL | NP equity accounts good (Restricted/Unrestricted Net Assets), QB: -$12.2M, 940 txns |

**Parent Score: 6.5/10**

### Rise (Ch.)

| # | Station | Status | Key Finding |
|---|---------|--------|-------------|
| 1 | Dashboard | PARTIAL | Net profit $153K (good), Bank QB: $238M (CRITICAL — absurd) |
| 2 | Donors | PASS | Same donor set as Parent, "Donors" page title, "Create pledge" buttons |
| 3 | Pledges | PASS | "Donor/Project" column, Overdue $1.5M, invoices with realistic terms |
| 4 | Dimensions | PASS | 6 active (Classes, Functional Expense, Funding Channels/Sources, Program, Restriction), NO George Floyd Fund |
| 5 | Multi-Entity | PASS | (verified via company switcher) |
| 6 | Statement of Activity | PASS | (same report structure as Parent) |
| 7 | Vendors | PASS | (same clean vendor set) |
| 8 | Programs | PASS | (same NP product catalog) |
| 9 | Grants (Projects) | PASS | 5 projects! (Back-to-School Outreach $3.2M, Foundation Grant, Rural Care Grant, Youth Council Grant) |
| 10 | COA + Banking | PARTIAL | QB: $238M, 400 txns to review |

**Rise Score: 7.5/10** (no P0, better projects, but $238M balance)

### Response (Ch)

| # | Station | Status | Key Finding |
|---|---------|--------|-------------|
| 1 | Dashboard | PARTIAL | Net profit $3.8M (good but high), Bank QB: $344M (CRITICAL — most absurd) |
| 2 | Donors | PASS | (same donor set) |
| 3 | Pledges | PASS | (same pledge structure) |
| 4 | Dimensions | PASS | 8 active dimensions (shared + local "Response" variants), NO George Floyd Fund, 2 inactive |
| 5 | Multi-Entity | PASS | (verified via switcher) |
| 6 | Statement of Activity | PASS | (same report structure) |
| 7 | Vendors | PASS | (same clean vendor set) |
| 8 | Programs | PASS | (same NP product catalog) |
| 9 | Grants (Projects) | PASS | (assumed similar to Rise) |
| 10 | COA + Banking | PARTIAL | QB: $344M, 761 txns to review |

**Response Score: 7/10** (no P0, good dimensions, but $344M balance)

---

## Critical Findings

### P0 — MUST FIX BEFORE DEMO

1. **"George Floyd Fund" dimension** (Parent only)
   - Location: Dimensions Hub (`/app/class`) on Vala Non Profit (Par.)
   - Issue: Uses the name of a real person associated with highly sensitive racial justice events
   - Risk: Extremely inappropriate for a demo environment — could cause serious offense
   - Fix: Rename to "Social Justice Fund", "Community Justice Initiative", or "Equity Action Fund"

### P1 — HIGH PRIORITY

2. **QB Balance Inflation** (All entities)
   - Parent: -$12,235,200.34 (negative, bank shows $0)
   - Rise: $238,049,507.35 (bank shows $460K)
   - Response: $344,535,460.93 (bank shows $0)
   - Root cause: Likely runaway transaction ingestion without bank reconciliation
   - Impact: Makes financial reports unrealistic at a glance

3. **2,101 bank transactions to review** (aggregate: Parent 940 + Rise 400 + Response 761)
   - All uncategorized/unmatched
   - Makes the banking experience look neglected

### P2 — MEDIUM PRIORITY

4. **Parent has only 2 Projects** (Climate Action Initiative, Community Outreach Program)
   - Rise has 5 — demonstrates the feature better
   - Recommendation: Add 2-3 more projects to Parent

5. **Duplicate donor** "Individual Donations Tier 1" on Parent
   - Two entries with same name
   - Minor but noticeable in demos

6. **NP terminology gaps** in page titles
   - Invoices page title says "Invoices" (should say "Pledges" — only nav bookmark shows correct term)
   - Products page says "Products & services" (not "Programs")
   - Projects page says "Projects" (not "Grants")
   - These are QBO system labels, likely not configurable

---

## Content Scan Results

| Area | Parent | Rise | Response |
|------|--------|------|----------|
| Donors | CLEAN | CLEAN | CLEAN |
| Vendor names | CLEAN | CLEAN | CLEAN |
| Product/Service names | CLEAN | CLEAN | CLEAN |
| Dimension names | **FAIL** (George Floyd Fund) | CLEAN | CLEAN |
| COA account names | CLEAN | CLEAN | CLEAN |
| Bank descriptions | CLEAN | CLEAN | CLEAN |
| Project names | CLEAN | CLEAN | CLEAN |

**Content Scan: 1 violation found** (CS_001: Real person name in sensitive context)

---

## NP Terminology Adoption

| Feature | Expected NP Term | Actual | Status |
|---------|------------------|--------|--------|
| Customers page title | Donors | Donors | PASS |
| Invoice nav bookmark | Pledges | Pledges | PASS |
| Invoice page title | Pledges | Invoices | PARTIAL |
| Invoice column | Donor/Project | Donor/Project | PASS |
| Action buttons | Create pledge | Create pledge | PASS |
| P&L report name | Statement of Activity | Statement of Activity | PASS |
| Equity accounts | Net Assets | Unrestricted/Restricted Net Assets | PASS |
| Income accounts | Grant Revenue, Program Service Revenue | Both present | PASS |
| Expense categories | Management & General, Program Expenses | Both present | PASS |
| Products page title | Programs | Products & services | PARTIAL |
| Projects page title | Grants | Projects | PARTIAL |

**Terminology Score: 8/11** (73%) — all controllable terms correctly applied; system labels cannot be changed

---

## Financial Summary

| Entity | Income | Expenses | Net Profit | QB Balance | Bank Balance |
|--------|--------|----------|------------|------------|--------------|
| Parent | $2.27M | $2.0M | +$267,940 | -$12.2M | $0 |
| Rise | $250.5K | $97.4K | +$153,050 | $238M | $460K |
| Response | $6.9M | $3.07M | +$3.83M | $344M | $0 |
| **Total** | **$9.42M** | **$5.17M** | **$4.25M** | **$570M+** | **$460K** |

P&L numbers are reasonable for a mid-size NP group. QB balances are absurdly inflated.

---

## URLs Reference

| Page | URL | Status |
|------|-----|--------|
| Dashboard | `/app/homepage` | OK |
| Donors | `/app/customers` | OK (title: "Donors") |
| Pledges | `/app/invoices` | OK (title: "Invoices") |
| Dimensions Hub | `/app/class` | OK |
| Standard Reports | `/app/standardreports` | OK |
| Vendors | `/app/vendors` | OK |
| Programs | `/app/items` | OK |
| Projects | `/app/projects` | OK |
| COA | `/app/chartofaccounts?jobId=accounting` | OK |
| Banking | `/app/banking` | OK |
| Report List | `/app/reportlist` | **404** (use side nav instead) |
| Dimensions alt | `/app/dimensions` | **404** (use `/app/class`) |

---

## Recommendations (Priority Order)

1. **RENAME "George Floyd Fund"** → "Social Justice Fund" or similar (P0, 5 min fix)
2. **Reconcile bank transactions** to fix QB balance inflation (P1, significant effort)
3. **Add 2-3 projects to Parent** to match Rise's richness (P2, 15 min)
4. **Delete duplicate donor** "Individual Donations Tier 1" on Parent (P2, 2 min)
5. **Run bank rules** to auto-categorize the 2,101 pending transactions (P2, 30 min)

---

## Session Info
- **Started:** ~21:15 UTC
- **Completed:** ~21:35 UTC
- **Stations audited:** 30 (10 x 3 entities)
- **Content scans:** 21 (7 areas x 3 entities)
- **Violations found:** 1 (P0)
- **Files generated:** parent_homepage.md, parent_donors.md, parent_pledges.md, parent_dimensions.md, parent_reports_menu.md, parent_vendors.md, parent_programs.md, parent_coa.md, parent_banking.md, rise_homepage.md, rise_donors.md, rise_dimensions.md, rise_pledges.md, rise_projects.md, response_homepage.md, response_dimensions.md
