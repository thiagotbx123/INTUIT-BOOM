# May 2026 Release — Joint Project Plan DRAFT
**Source:** Google Doc (fetched via API 2026-04-13)
**Doc URL:** https://docs.google.com/document/d/18DHVep4NPY4FZSap5ECC8EugMMmrTtQlNxJZFgaG90o/edit
**As of:** April 9, 2026
**Status:** DRAFT — To be reviewed and finalized together

---

## Key Dates

| Milestone | Target Date | Status |
|-----------|------------|--------|
| Write It Straight locked | Done | 51 features with green (down from 108) |
| Code lock | April 10? | Pending — need confirmation |
| Feature flags on in UAT | ~April 30 | Pending code lock |
| UAT validation complete | TBD | Pending feature flags |
| Feature flags on in Production | May 13 | GA release date |
| Seller environments ready | May 15 (target) | 2-day turnover post-GA |

---

## Phase 1: Pre-Build (Now — Code Lock) — April 8-10

| # | Task | Owner | Dependency | Status |
|---|------|-------|------------|--------|
| 1.1 | Confirm code lock date with product team | Intuit | None | |
| 1.2 | Review WIS — identify which of 45 features need new data | TestBox | 1.1 | Done |
| 1.3 | Identify WFS-specific vs QBO-general features | TestBox + Intuit | 1.2 | Done |
| 1.4 | Confirm UAT environment is clean and ready | TestBox | None | UAT exists from Feb release |
| 1.5 | Confirm UAT validation resources are committed | Intuit | None | Open |

## Phase 2: Feature Access + Data Build (Code Lock — UAT Ready) — April 10-30

| # | Task | Owner | Dependency | Status |
|---|------|-------|------------|--------|
| 2.1 | Request feature flags turned on in UAT | TestBox → Intuit Product | 1.1 (code lock) | Not started |
| 2.2 | Confirm feature flags are live in UAT | Intuit (Product / tech TBD) | 2.1 | Not started |
| 2.3 | Feature-by-feature validation in UAT | TestBox | 2.2 | Not started |
| 2.4 | Identify features requiring new/updated data | TestBox | 2.3 | Not started |
| 2.5 | Generate and ingest new data for features | TestBox | 2.4 | Not started |
| 2.6 | Populate UAT tracker with per-feature status | TestBox | 2.3 | Not started |
| 2.7 | Provide click paths for features not in WIS | Intuit | 2.2 | Not started |

## Phase 3: UAT Validation (UAT Ready — Sign-off) — ~May 1-9

| # | Task | Owner | Dependency | Status |
|---|------|-------|------------|--------|
| 3.1 | Grant UAT access to validation team | TestBox | 2.5 complete | In Progress pending validation users |
| 3.2 | Team validates data story per feature | Intuit | 3.1 | Not started |
| 3.3 | Capture feedback, fix data issues | TestBox | 3.2 | Not started |
| 3.4 | UAT sign-off — all features "ready" in tracker | TestBox + Intuit | 3.3 | Not started |
| 3.5 | Prepare seller comms — what's new, where to go | Intuit + TestBox | 3.4 | Not started |
| 3.6 | Update banner announcement in TestBox app | TestBox | 3.5 | Not started |

## Phase 4: Production Rollout (GA — Seller Ready) — May 13-15

| # | Task | Owner | Dependency | Status |
|---|------|-------|------------|--------|
| 4.1 | Feature flags on in production seller environments | Intuit (Product) | May 13 GA | Not started |
| 4.2 | Migrate validated data from UAT → production | TestBox | 4.1 | Not started |
| 4.3 | Spot-check production environments post-migration | TestBox | 4.2 | Not started |
| 4.4 | Final spot-check in production | Intuit | 4.3 | Not started |
| 4.5 | Declare seller-ready — remove banners | TestBox + Intuit | 4.4 | Not started |
| 4.6 | Send seller comms — new features available | Intuit (Matt/Marcus) | 4.5 | Not started |

## WFS-Specific Tasks (Parallel Track)

| # | Task | Owner | Dependency | Status |
|---|------|-------|------------|--------|
| W.1 | Finalize data design doc (pending Sandra PMM input) | TestBox + Intuit (Sandra) | None | Nearly complete |
| W.2 | Confirm WFS feature flags in May code lock | Intuit (Rama) | 1.1 | Pending |
| W.3 | Validate WFS features in UAT | TestBox | 2.2 + W.2 | Not started |
| W.4 | WFS-specific data generation and ingestion | TestBox | W.3 | Not started |
| W.5 | Reinstate weekly WFS cadence meeting | TestBox + Intuit | None | Dropped when Kyla rolled off |

## Open Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Code lock slips past April 10 | Compresses entire timeline | |
| Feature flags not turned on in UAT on time | Delays data build + validation | Need confirmed tech contact (Siji replacement) |
| Intuit PM coverage resources may not be available | No Intuit PM for release coordination | Donna stepping in; Gayathri being introduced |
| Intuit-side validation resources not confirmed | Can't sign off on data quality | Donna to confirm |
| WFS features not in May code lock | WFS launch decoupled | Rama to confirm |

## Key Contacts

| Role | Person | Team |
|------|--------|------|
| TestBox | Katherine Lu, Gayathri, Alexandra, Thiago | TestBox |
| Release coordination (Intuit) | Christina Duarte → Donna Seapoe | Sales Enablement |
| Sales enablement | Matt Hrabinski / Marcus Cramer | Sales Enablement |
| Seller comms | Marcus Cramer | Mid-Market |
| Product/feature flags | TBD (Siji replacement needed) | Product |
| WFS product | Rama Ghanta | WFS Product |
| WFS PMM | Sandra Bledsoe | WFS PMM |
