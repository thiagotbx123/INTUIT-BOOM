# QBO Dataset Mastery — Complete Analysis
**Date**: 2026-04-15
**Source**: Legacy Postgres `tbx-postgres-staging.internal:5433/unstable` (live query)
**Author**: Thiago Rodrigues (automated analysis)

---

## 1. DATASET INVENTORY (Phase 1)

### 1.1 Dataset Registry

| Alias | Dataset ID | Industry | Accounts | Entities | Last Sweep | Score |
|-------|-----------|----------|----------|----------|------------|-------|
| **CONSTRUCTION** | `321c6fa0` | Construction | construction, clone, mid-market, qsp, keystone-se | 22 | Apr 15 | 9.0 (clone) |
| **CONSULTING** | `58f84612` | Prof. Services | summit | 3 | Mar 12 | 6.3 realism |
| **NONPROFIT** | `3e1337cc` | Non-Profit | nv2 | 3 | Mar 5 | No score |
| **CANADA** | `2ed5d245` | Canada Construction | (blocked PLA-2969) | 1 | Never | N/A |
| **MANUFACTURING** | `b6695ca6` | Manufacturing | nv3 | 3 | Mar 11 | 64 realism |
| **TCO** | `fab72c98` | Tire Shop | tco | 5 | Mar 23 | 7.5/10 |

### 1.2 Row Counts — Core Transaction Tables

| Table | CONSTRUCTION | CONSULTING | NONPROFIT | CANADA | MANUFACTURING | TCO |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| invoices | **428** | 135 | 1,920 | 247 | 18,793 | 23,635 |
| invoice_line_items* | ~1,686+ | ~500+ | ~8K+ | ~1K+ | ~40K+ | ~60K+ |
| bills | **96** | 155 | 3,060 | 536 | 783 | 144 |
| bills_line_items* | ~149+ | ~300+ | ~4K+ | ~600+ | ~1K+ | ~300+ |
| expenses | **650** | 253 | 548 | 741 | 1,300 | 804 |
| expense_line_items* | ~1,006+ | ~500+ | ~1K+ | ~1K+ | ~2K+ | ~1K+ |
| estimates | **75** | 10 | **0** | 6 | 500 | **0** |
| bank_transactions | **155** | 168 | **0** | **0** | **0** | 210 |
| time_entries | **5,519** | 2,006 | 31,751 | 232 | **0** | 22,300 |
| payroll_expenses | **288** | 303 | **0** | **0** | **0** | **0** |
| project_tasks | **65** | **0** | **0** | **0** | **0** | **0** |
| purchase_orders | **48** | **0** | **0** | 18 | **0** | 144 |
| projects | **8** | 10 | 2 | 6 | 3 | 10 |
| project_budgets | **6** | 10 | 2 | **0** | 3 | **0** |
| mileage | **2,052** | **0** | **0** | **0** | **0** | 2,052 |
| contractors | **27** | **0** | 250 | 25 | **0** | **0** |
| fixed_assets | **11** | 18 | **0** | **0** | 20 | 113 |
| forecast | **1** | **0** | **0** | **0** | **0** | 1 |
| vehicles | **8** | **0** | **0** | **0** | **0** | 75 |
| time_schedule | **31** | **0** | **0** | **0** | **0** | 131 |
| recurring_transaction | **3** | **0** | **0** | **0** | **0** | **0** |
| intercompany_JE | **12** | 12 | **0** | **0** | 24 | 24 |

*Line item tables don't have dataset_id — counts estimated from parent relationship.*

### 1.3 Reference Data Tables

| Table | CONSTRUCTION | CONSULTING | NONPROFIT | CANADA | MANUFACTURING | TCO |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| customers | 50 | 25 | 66 | 50 | 24 | 10,400 |
| product_services | 83 | 37 | 93 | 83 | 47 | 122 |
| employees | 45 | 45 | 1,200 | 45 | 110 | 250 |
| vendors | 33 | 20 | 43 | 33 | 19 | 113 |
| chart_of_accounts | 121 | 99 | 163 | 105 | 118 | 73 |
| classifications | 37 | 39 | 47 | 36 | 55 | 51 |

### 1.4 Company Type Distribution

| Dataset | parent | main_child | secondary_child | other |
|---------|:---:|:---:|:---:|:---:|
| **CONSTRUCTION** | inv:123, bill:43, exp:220 | inv:190, bill:16, exp:230 | inv:115, bill:37, exp:200 | - |
| **CONSULTING** | inv:85, exp:63 | inv:30, bill:60, exp:100 | inv:20, bill:95, exp:90 | - |
| **NONPROFIT** | inv:1416, bill:756, exp:134 | inv:225, bill:999, exp:295 | inv:279, bill:1305, exp:119 | - |
| **CANADA** | - | - | - | all=247 inv, 536 bill, 741 exp |
| **MANUFACTURING** | inv:509, bill:55, exp:162 | inv:6865, bill:167, exp:434 | inv:11419, bill:561, exp:704 | - |
| **TCO** | bank:47 | inv:22155, bill:60, exp:268 | inv:606, bill:36, exp:268 | child_3: inv:874, bill:48, exp:268 |

### 1.5 Global MAX IDs (for future ingestion)

| Table | MAX ID | Total Rows | Next Available |
|-------|--------|-----------|---------------|
| invoices | 45,562 | 45,158 | 45,563 |
| invoice_line_items | 121,835 | 117,164 | 121,836 |
| bills | 4,998 | 4,774 | 4,999 |
| bills_line_items | 5,715 | 5,258 | 5,716 |
| expenses | 10,294 | 4,296 | 10,295 |
| expense_line_items | 9,021 | 4,652 | 9,022 |
| estimates | 840 | 591 | 841 |
| estimate_line_items | 4,488 | 2,767 | 4,489 |
| bank_transactions | 1,475 | 533 | 1,476 |
| time_entries | 77,889 | 61,808 | 77,890 |
| project_tasks | 185 | 65 | 186 |
| projects | 63 | 39 | 64 |
| purchase_order | 327 | 210 | 328 |
| purchase_order_line_items | 1,251 | 844 | 1,252 |
| payroll_expenses | 591 | 591 | 592 |
| customers | 10,615 | 10,615 | 10,616 |
| product_services | 467 | 465 | 468 |
| employees | 1,700 | 1,695 | 1,701 |
| vendors | 261 | 261 | 262 |

### 1.6 Full Schema: 78 Tables

**78 quickbooks_* tables** in the database (17 documented, 61 undocumented in REGRAS_MASTER):

**Documented (core):** invoices, invoice_line_items, bills, bills_line_items, expenses, expense_line_items, estimates, estimate_line_items, bank_transactions, time_entries, project_tasks, purchase_order, purchase_order_line_items, payroll_expenses, payroll_expense_line_items, classifications, product_services_classifications

**Newly discovered (undocumented):**
- `annual_mappings` (12) — year-mapping config
- `bank_accounts` (5) — BOI and checking setup per dataset
- `bills_review` (10) — bill approval workflow (Construction only)
- `break_rules` (18) — payroll break rules
- `budgets` (1) — budget feature
- `bundles` (3) / `bundles_line_items` (15) — product bundles (Construction only)
- `change_orders` (0) / `change_orders_*` (0) — construction change orders (EMPTY)
- `contractors` (302) / `contractors_documents` (4) — 1099 contractors
- `custom_fields` (5) / `custom_report_templates` (21) / `custom_reports` (3) — customization
- `customer_notes` (2) / `vendor_notes` (0) — CRM notes
- `dimensions` (49) — classification dimensions
- `expense_claims` (47) — expense reimbursements (Construction only)
- `expense_templates` (32) — receipt/expense templates
- `fixed_assets` (162) — asset management
- `forecast` (2) / `forecast_rules` (4) — cash flow forecast
- `intercompany_*` (72 JE + 384 lines) — IC transactions
- `mileage` (4,104) — mileage tracking
- `payroll_dimensions` (225) — payroll cost allocation
- `project_attachments` (1) / `project_budgets` (21) / `project_budget_line` (933) / `project_milestones` (202) — PM features
- `pto_policy` (1) — paid time off
- `receipts` (0) / `receipts_line_items` (0) — receipt capture (EMPTY)
- `recurring_transaction` (3) — scheduled transactions
- `revenue_recognition_templates` (7) — rev rec (Construction + Consulting)
- `template_tasks` (90) — project task templates
- `time_schedule` (162) — employee schedules
- `transaction_rules` (4) / `transaction_rule_conditions` (6) — bank rules
- `user_settings` (17) / `users` (23) — user/access config
- `vehicles` (83) — fleet management
- `workflow_automations` (8) — approval workflows

---

## 2. CROSS-DATASET GAP ANALYSIS (Phase 2)

### 2.1 Feature Coverage Matrix

Features that populate UI screens. **"X"** = has data, **"--"** = EMPTY (gap).

| Feature / Screen | CONSTRUCTION | CONSULTING | NONPROFIT | CANADA | MANUFACTURING | TCO |
|-----------------|:---:|:---:|:---:|:---:|:---:|:---:|
| **Invoices** | X (428) | X (135) | X (1920) | X (247) | X (18793) | X (23635) |
| **Bills** | X (96) | X (155) | X (3060) | X (536) | X (783) | X (144) |
| **Expenses** | X (650) | X (253) | X (548) | X (741) | X (1300) | X (804) |
| **Estimates** | X (75) | X (10) | **--** | X (6) | X (500) | **--** |
| **Purchase Orders** | X (48) | **--** | **--** | X (18) | **--** | X (144) |
| **Bank Transactions** | X (155) | X (168) | **--** | **--** | **--** | X (210) |
| **Payroll** | X (288) | X (303) | **--** | **--** | **--** | **--** |
| **Time Entries** | X (5519) | X (2006) | X (31751) | X (232) | **--** | X (22300) |
| **Project Tasks** | X (65) | **--** | **--** | **--** | **--** | **--** |
| **Projects** | X (8) | X (10) | X (2) | X (6) | X (3) | X (10) |
| **Project Budgets** | X (6) | X (10) | X (2) | **--** | X (3) | **--** |
| **Project Milestones** | X | ? | ? | ? | ? | ? |
| **Mileage** | X (2052) | **--** | **--** | **--** | **--** | X (2052) |
| **Contractors** | X (27) | **--** | X (250) | X (25) | **--** | **--** |
| **Fixed Assets** | X (11) | X (18) | **--** | **--** | X (20) | X (113) |
| **Forecast** | X (1) | **--** | **--** | **--** | **--** | X (1) |
| **Vehicles** | X (8) | **--** | **--** | **--** | **--** | X (75) |
| **Time Schedule** | X (31) | **--** | **--** | **--** | **--** | X (131) |
| **Recurring Txns** | X (3) | **--** | **--** | **--** | **--** | **--** |
| **Intercompany JE** | X (12) | X (12) | **--** | **--** | X (24) | X (24) |
| **Bundles** | X (3) | **--** | **--** | **--** | **--** | **--** |
| **Revenue Rec** | X (5) | X (2) | **--** | **--** | **--** | **--** |
| **Expense Claims** | X (47) | **--** | **--** | **--** | **--** | **--** |
| **Bills Review** | X (10) | **--** | **--** | **--** | **--** | **--** |
| **Bank Rules** | X (4) | **--** | **--** | **--** | **--** | **--** |
| **Workflow Auto** | shared | shared | shared | shared | shared | shared |

### 2.2 Gap Severity Score (0-10, where 10 = Construction-level completeness)

| Dataset | Score | Critical Gaps | Why |
|---------|:-----:|---------------|-----|
| **CONSTRUCTION** | **10** | None | Reference dataset, all features populated |
| **TCO** | **7** | No estimates, payroll, project tasks, contractors, recurring | Good volume but missing key features |
| **CONSULTING** | **5** | No POs, mileage, contractors, vehicles, time schedule, project tasks | Low transaction volume, missing operational features |
| **NONPROFIT** | **4** | No estimates, bank txns, payroll, POs, mileage, assets, vehicles | Large volume in invoices/bills but missing breadth |
| **MANUFACTURING** | **3** | No bank txns, time entries, payroll, project tasks, POs, mileage | High invoice volume but hollow — missing critical operational data |
| **CANADA** | **2** | No bank txns, payroll, project tasks, mileage, assets, vehicles | Single entity, missing most operational features, BLOCKED |

### 2.3 Sector Benchmark Compliance

| Dataset | Target Margin | Actual State | Bank Txns | Payroll | Projects | Assessment |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|
| **CONSTRUCTION** | 3-15% | 26.8% (HIGH) | 155 | 288 | 8 w/ tasks | Above target but functional |
| **TCO** | 25-35% | Unknown (no P&L audit) | 210 | **ZERO** | 10 (no tasks) | Missing payroll = unrealistic for tire shop |
| **CONSULTING** | 20-40% | Unknown | 168 | 303 | 10 (no tasks) | Has payroll but low txn volume |
| **NONPROFIT** | 2-10% surplus | Unknown | **ZERO** | **ZERO** | 2 | No banking = invisible cash flow |
| **MANUFACTURING** | 15-25% | Unknown | **ZERO** | **ZERO** | 3 | Hollow — high invoice count but no costs visible |
| **CANADA** | 3-15% | Unknown | **ZERO** | **ZERO** | 6 | Blocked, minimal data |

---

## 3. SWEEP FINDINGS → DATA ROOT CAUSE MAP (Phase 3)

Cross-referencing 33 sweep reports with the DB inventory above.

### 3.1 Common P1 Findings Traced to Data Gaps

| Sweep Finding | Frequency | Root Cause | Dataset(s) Affected | DB Fix |
|--------------|:---------:|-----------|---------------------|--------|
| **D02: P&L negative** | HIGH | expenses > income for some CTs/months | Construction (main), Summit, NV2 | Rebalance invoice amounts or reduce expense rows |
| **D02: Margin too high** | MEDIUM | Construction entities at 25-28% vs 3-15% target | Construction | Add more expenses/bills to bring margin down |
| **D04: Banking empty** | HIGH | bank_transactions = 0 | NP, Canada, Manufacturing | Create bank_transactions CSVs |
| **D07: Payroll missing** | HIGH | payroll_expenses = 0 | NP, Canada, Manufacturing, TCO | Create payroll CSVs (requires activity plans) |
| **D09: Project margin irreal** | MEDIUM | Projects lack expenses, only invoices visible | Construction clone (GaleGuardian 92.9%) | Add project-specific expenses |
| **S-pages 404 / empty** | MEDIUM | Feature tables have 0 rows → UI shows empty | Varies by dataset | Populate missing tables |
| **CS3: Placeholder names** | LOW | Entity names from template data | Construction (fixed in clone) | UI-level fix via sweep |
| **D05: Estimates empty** | MEDIUM | estimates = 0 | NP, TCO | Create estimates CSVs |
| **D06: POs empty** | MEDIUM | purchase_order = 0 | Consulting, NP, Manufacturing | Create PO CSVs |
| **D08: Time entries zero** | LOW | time_entries = 0 | Manufacturing | Create time entries CSVs |

### 3.2 Per-Dataset Root Cause Summary

**TCO (Tire Shop) — Score 7.5, 72 realism:**
- MISSING: estimates (buyers need to see quotes), payroll (unrealistic for auto shop), project tasks
- WEAK: Low bill count (144), no contractors
- FIX PRIORITY: Payroll first (biggest realism gap), then estimates, then project tasks

**CONSULTING (Summit) — Score 6.3 realism:**
- MISSING: POs, mileage, contractors, vehicles, time schedule, project tasks
- WEAK: Only 135 invoices (thin), P&L likely negative (known from sweep)
- FIX PRIORITY: Increase invoice volume, add POs, project tasks, fix P&L balance

**NONPROFIT (NV2) — No score:**
- MISSING: estimates, bank_transactions, payroll, POs, mileage, assets, vehicles
- CRITICAL: No banking = cash flow screens empty, no bank feed demo
- ANOMALY: Heavy bill volume (3060) suggests cost structure dominates
- FIX PRIORITY: Bank transactions first (core demo flow), then estimates, then payroll

**MANUFACTURING (NV3) — 64 realism:**
- MISSING: bank_transactions, time_entries, payroll, project_tasks, POs, mileage
- ANOMALY: 18,793 invoices but 0 time entries = hollow production data
- CRITICAL: Manufacturing demo needs COGS, WIP, production tracking
- FIX PRIORITY: Time entries (production tracking), then bank txns, then POs, then payroll

**CANADA — Blocked:**
- Status: PLA-2969 blocks all work
- Single entity (company_type = "all")
- Minimal data across all tables
- DECISION: Skip until PLA-2969 resolves

---

## 4. MAY RELEASE FEATURE-DATA DEPENDENCIES (Phase 4)

### 4.1 Features Requiring New Data

| MR ID | Feature | Dataset(s) Affected | Data Required | DB Table | Status |
|-------|---------|---------------------|--------------|----------|--------|
| MR-020 | QBDT→QBO Migration | Construction (IES) | Migration demo data | Various | Not started |
| MR-021 | Solution Specialist | All IES | Specialist interaction data | TBD | Not started |
| MR-053 | Omni PM AI (IES) | Construction | Rich project data | projects, project_budgets, time_entries | Partial (Construction has data) |
| WIS-27 | Background Checks | WFS tenants | Employee background data | employees + new table? | Not started |
| WIS-31 | Time Off | WFS tenants | PTO policies + requests | pto_policy, time_entries | pto_policy has 1 row |
| WIS-46 | PM Cost Allocation | Construction | Cost allocation dimensions | project_budget_line_dimensions | 933 rows exist |
| WIS-48 | Manufacturing Orders | Manufacturing | Production orders | change_orders (currently 0) | EMPTY — needs new data |

### 4.2 Feature-Data Readiness Matrix

| Feature Category | OOTB? | Construction | TCO | Consulting | NP | Manufacturing |
|-----------------|:-----:|:-----------:|:---:|:---------:|:--:|:------------:|
| Cash Flow (D01 widget) | Yes | OK | OK | OK | WEAK (no bank) | WEAK (no bank) |
| P&L Report | Yes | OK | Needs audit | Needs audit | Needs audit | Needs audit |
| Balance Sheet | Yes | OK | OK | OK | OK | OK |
| Banking module | Yes | OK | OK | OK | **BLOCKED** (0 txns) | **BLOCKED** (0 txns) |
| Invoicing | Yes | OK | OK | OK | OK | OK |
| Bills/AP | Yes | OK | OK | OK | OK | OK |
| Expenses | Yes | OK | OK | OK | OK | OK |
| Projects | Yes | OK | OK | OK | WEAK (2) | WEAK (3) |
| Payroll | Yes | OK | OK | OK | **BLOCKED** | **BLOCKED** |
| Time Tracking | Yes | OK | OK | OK | OK | **BLOCKED** |
| Estimates | Yes | OK | **BLOCKED** | WEAK (10) | **BLOCKED** | OK |
| Purchase Orders | Yes | OK | OK | **BLOCKED** | **BLOCKED** | **BLOCKED** |
| Inventory/Assets | Yes | OK | OK | OK | **BLOCKED** | OK |
| PM Cost Allocation (WIS-46) | No | Partial | N/A | N/A | N/A | N/A |
| Manufacturing Orders (WIS-48) | No | N/A | N/A | N/A | N/A | **NEEDS DATA** |

### 4.3 Timeline Alignment

| Milestone | Date | What Must Be Ready |
|-----------|------|-------------------|
| Code lock | ~Apr 10 | Done |
| Feature flags in UAT | ~Apr 30 | Need data for MR-020, MR-021, MR-053 features |
| **Data build window** | **Apr 10-30** | **CSVs must be generated, validated, and ingested** |
| UAT validation | May 1-9 | Sweeps run against all datasets |
| GA | May 13 | Production environments ready |
| Seller environments | May 15 | All demo accounts fully functional |

---

## 5. CSV GENERATION & INGESTION PLAN (Phase 5)

### 5.1 Priority Order

| Priority | Dataset | Why | Effort | Impact |
|:--------:|---------|-----|:------:|:------:|
| **P0** | TCO (Tire Shop) | Flagship, P0 in Linear, closest to good | MEDIUM | HIGH |
| **P1** | MANUFACTURING | May release MR-050, currently hollow | HIGH | HIGH |
| **P1** | NONPROFIT | Core demo flow broken (no banking) | MEDIUM | MEDIUM |
| **P2** | CONSULTING | P&L issues, missing features | MEDIUM | MEDIUM |
| **P3** | CONSTRUCTION | Gate 2 unblock for PLA-3416 | LOW (already done) | HIGH |
| **SKIP** | CANADA | Blocked by PLA-2969 | N/A | N/A |

### 5.2 TCO (Tire Shop) — Ingestion Plan

**Dataset ID**: `fab72c98-c38d-4892-a2db-5e5269571082`
**FK boundaries**: customers 216-10615, products 346-467, vendors 149-261, projects 54-63, employees 1451-1700

| # | Table | Action | Est. Rows | Why |
|---|-------|--------|:---------:|-----|
| 1 | estimates | **INSERT** | ~80 | Tire shop needs quotes for fleet work |
| 2 | estimate_line_items | INSERT | ~320 | 4 LIs avg per estimate |
| 3 | payroll_expenses | INSERT | ~240 | 20 employees x 12 months (biweekly) |
| 4 | payroll_expense_line_items | INSERT | ~480 | 2 LIs per payroll entry |
| 5 | project_tasks | INSERT | ~40 | 4 tasks per 10 projects |
| 6 | contractors | INSERT | ~15 | Subcontracted mechanics |
| 7 | recurring_transaction | INSERT | ~5 | Monthly parts orders, rent |

**Sector benchmarks to hit:**
- Net margin 25-35%
- Inventory turnover 6-12x
- Service vs parts revenue 40-60%
- Customer retention 60-80%

### 5.3 MANUFACTURING (NV3) — Ingestion Plan

**Dataset ID**: `b6695ca6-9184-41f3-862e-82a182409617`
**FK boundaries**: customers 142-165, products 216-262, vendors 97-115, projects 45-47, employees 1296-1405

| # | Table | Action | Est. Rows | Why |
|---|-------|--------|:---------:|-----|
| 1 | bank_transactions | **INSERT** | ~120 | Banking module is empty |
| 2 | time_entries | INSERT | ~3,000 | Production tracking (critical for mfg) |
| 3 | payroll_expenses | INSERT | ~264 | 22 employees x 12 months |
| 4 | payroll_expense_line_items | INSERT | ~528 | 2 LIs per payroll |
| 5 | purchase_order | INSERT | ~60 | Raw material procurement |
| 6 | purchase_order_line_items | INSERT | ~180 | 3 LIs per PO |
| 7 | project_tasks | INSERT | ~12 | Production tasks per project |
| 8 | mileage | INSERT | ~200 | Delivery fleet |
| 9 | contractors | INSERT | ~10 | External specialists |
| 10 | change_orders (MR-050) | INSERT | ~20 | Manufacturing orders (May release!) |

**Sector benchmarks to hit:**
- Gross margin 25-40%
- COGS 55-75% of revenue
- Inventory days 30-60
- WIP 20-40% of inventory

### 5.4 NONPROFIT (NV2) — Ingestion Plan

**Dataset ID**: `3e1337cc-70ca-4041-bc95-0fe29181bb12`
**FK boundaries**: customers 76-141, products 122-215, vendors 54-96, projects 37-38, employees 96-1295

| # | Table | Action | Est. Rows | Why |
|---|-------|--------|:---------:|-----|
| 1 | bank_transactions | **INSERT** | ~100 | Banking module completely empty |
| 2 | estimates | INSERT | ~30 | Grant proposals / project estimates |
| 3 | estimate_line_items | INSERT | ~120 | 4 LIs per estimate |
| 4 | payroll_expenses | INSERT | ~300 | Large employee base (1200) |
| 5 | payroll_expense_line_items | INSERT | ~600 | 2 LIs per payroll |
| 6 | purchase_order | INSERT | ~25 | Program procurement |
| 7 | purchase_order_line_items | INSERT | ~75 | 3 LIs per PO |
| 8 | project_tasks | INSERT | ~10 | Grant milestones |
| 9 | fixed_assets | INSERT | ~15 | Office/program equipment |

**Sector benchmarks to hit:**
- Program expense ratio 65-85%
- Fundraising efficiency <25% of donations
- Grant dependency <50%
- Surplus margin 2-10%

### 5.5 CONSULTING (Summit) — Ingestion Plan

**Dataset ID**: `58f84612-39db-4621-9703-fb9e1518001a`
**FK boundaries**: customers 51-75, products 84-121, vendors 34-53, projects 27-36, employees 51-95

| # | Table | Action | Est. Rows | Why |
|---|-------|--------|:---------:|-----|
| 1 | purchase_order | **INSERT** | ~20 | Software/tool procurement |
| 2 | purchase_order_line_items | INSERT | ~60 | 3 LIs per PO |
| 3 | project_tasks | INSERT | ~40 | 4 tasks per 10 projects |
| 4 | mileage | INSERT | ~100 | Client site visits |
| 5 | contractors | INSERT | ~10 | Subcontracted consultants |
| 6 | invoices (supplement) | APPEND | ~100 | Increase volume from 135 → 235 |
| 7 | invoice_line_items (supp.) | APPEND | ~400 | For supplemental invoices |

**Sector benchmarks to hit:**
- Utilization 65-80%
- Revenue per employee $150K-$300K
- Net margin 20-40%
- DSO 30-45 days

### 5.6 CONSTRUCTION — Pending Actions

**Already done (CSVs ready):** 15 CSVs, 10,831 rows, 189/189 audit PASS.
**Blocked:** PLA-3416 — activity plans for 93 cash flow invoices need Augusto.
**Action needed:** Unblock Gate 2 with valid TMS JWT, then validate.

---

## 6. ACTIVITY PLAN & CRON REQUIREMENTS (Phase 6)

### 6.1 Activity Plan Lifecycle

```
DB INSERT → Activity Plans Generated → Ingestion Pipeline → QBO
                    ↓
              Cron (weekly) → confirm_bank_transactions > 30d → Expenses
```

**Owner**: Augusto Gunsch (platform team)
**Dependency**: After TSA inserts data, Augusto must generate activity plans before data appears in QBO.

### 6.2 Per-Dataset Activity Plan Status

| Dataset | Current State (TESTBOX_ACCOUNTS) | Bank Txns Need Cron? | Activity Plans Generated? | Next Step |
|---------|--------------------------------|:---:|:---:|-----------|
| **CONSTRUCTION** | Wait For Next Activity | Yes (155 txns) | Partial (PLA-3416 stuck) | Unblock Gate 2, generate plans for 93 invoices |
| **TCO** | Various (Ingest/Wait) | Yes (210 txns) | Yes (active) | Generate plans for new estimates + payroll |
| **CONSULTING** | Wait For Next Activity | Yes (168 txns) | Yes | Generate plans for new POs + tasks |
| **NONPROFIT** | Wait For Next Activity | **NO** (0 txns) | Yes (for existing) | INSERT bank txns → generate plans → cron picks up |
| **MANUFACTURING** | Create Next Year Activities | **NO** (0 txns) | Partial | INSERT all missing tables → generate plans |
| **CANADA** | Various | **NO** (0 txns) | N/A | BLOCKED (PLA-2969) |

### 6.3 Cron: `confirm_bank_transactions`

- **Tickets**: PLA-1727 (created Oct 2024), PLA-2810
- **Schedule**: Weekly
- **Logic**: Bank transactions > 30 days old with status "pending" → auto-confirmed → creates Expense records
- **Impact**: Keeps banking module alive — without this, pending transactions accumulate forever
- **Datasets actively using cron**: Construction (155), TCO (210), Consulting (168)
- **Datasets that NEED cron but have 0 bank txns**: NP, Manufacturing, Canada

### 6.4 Post-Ingestion Checklist (per dataset)

After ANY data insertion:
1. Verify row counts match expected
2. Check FK integrity (no orphan line items)
3. Verify dataset_id matches target
4. Check company_type distribution
5. Confirm no ID range conflicts
6. **Request Augusto to generate activity plans**
7. **Wait for pipeline to process** (check Retool State changes)
8. **Run Gate 2** with valid TMS JWT
9. **Run sweep** to validate UI appearance
10. Document results in sweep-learnings/

---

## 7. CYCLICAL AUDIT & TRIANGULATION (Phase 7)

### 7.1 Monthly Sweep Protocol

**Pre-sweep (data layer):**
1. Connect to Postgres → verify row counts haven't changed
2. Check if any activity plans failed (Retool State)
3. Verify cron ran (bank txns confirmed → expenses created)

**Sweep execution (UI layer):**
1. Run sweep v9.2 (dual-engine) per account
2. Deep stations D01-D25 + Surface S01-S46
3. Fix what's fixable via browser
4. Document blocked items

**Post-sweep (analysis layer):**
1. Compare scores vs previous month
2. Map new findings to DB root causes
3. Propose data fixes (CSV gen or direct UPDATE)
4. Update ROOT_CAUSE_MATRIX
5. Feed improvements into sweep_checks.py

### 7.2 Triangulation Matrix

| Signal | Source | What It Tells Us | Tool |
|--------|--------|-----------------|------|
| Empty UI pages | Sweep (S-stations) | Table has 0 rows for this dataset | Browser snapshot |
| P&L negative | Sweep (D02) | Income < Costs in DB data | DB query |
| Feature not working | Sweep (D-stations) | Activity plan didn't run or data missing | Retool State check |
| Gate 2 errors | Retool Validator | Data violates backend rules | Retool JWT + refresh |
| Score regression | Sweep delta | External data mutation or cron side effects | Compare sweep reports |
| Balance drift | Sweep D03/D04 | Cron created expenses or data was refreshed | DB query + sweep compare |

### 7.3 Critical Data Relationships (Fragility Points)

```
Invoice → Invoice LI → Product Service (FK)
                     → Customer (FK)
                     → Project (FK)
Bill → Bill LI → Vendor (FK) → Product Service (FK)
              → Chart of Account (FK)
Expense → Expense LI → Vendor/Employee (FK)
                     → Chart of Account (FK)
Bank Transaction → Bank Account (FK)
               → (cron) → Expense (auto-created)
Payroll → Payroll LI → Employee (FK)
Time Entry → Employee (FK) → Project (FK)
Estimate → Estimate LI → Product Service (FK) → Customer (FK)
Purchase Order → PO LI → Vendor (FK) → Product Service (FK)
```

Any missing FK target = broken reference in QBO UI.

### 7.4 Durability Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Dataset refresh resets QBO data** | All sweep fixes lost | Run full sweep after any refresh |
| **Cron creates unexpected expenses** | Balance/P&L drift | Monitor 1010 Checking balance monthly |
| **Activity plan failure** | Data doesn't appear in QBO | Check Retool State after insertion |
| **ID collision on new ingestion** | Duplicate records | Always query MAX(id) before generating CSVs |
| **Third-party data contamination** | Intuit SEs create records in demo | Content safety checks in sweep |
| **Employee duplication on API retry** | 90 dupes seen previously | Count employees post-ingestion |
| **Gateway timeout on large CSVs** | Partial ingestion | Split CSVs >3K rows |

---

## 8. EXECUTIVE SUMMARY & RECOMMENDED ACTIONS

### Immediate Actions (This Week)

| # | Action | Owner | Impact |
|---|--------|-------|--------|
| 1 | Unblock PLA-3416 Gate 2 (get TMS JWT) | Thiago → Augusto | Construction cash flow fix |
| 2 | Generate TCO estimates CSV (~80 rows) | Thiago | Fix empty estimates screen |
| 3 | Generate Manufacturing bank_transactions CSV | Thiago | Fix empty banking module |
| 4 | Audit TCO P&L from DB | Thiago | Understand current margin health |

### Short-term (Apr 15-30 — Data Build Window)

| # | Action | Dataset | Effort |
|---|--------|---------|--------|
| 5 | TCO payroll + project tasks CSVs | TCO | 2 days |
| 6 | Manufacturing full ingestion (bank, time, payroll, POs) | MFG | 3 days |
| 7 | NonProfit bank + estimates CSVs | NP | 2 days |
| 8 | Consulting POs + invoice supplement | Consulting | 1 day |
| 9 | Run Gate 1 on all new CSVs | All | 0.5 day |
| 10 | Request Augusto: activity plans for all new data | All | Platform |

### Medium-term (May 1-9 — UAT Validation)

| # | Action |
|---|--------|
| 11 | Run sweeps on ALL 9 accounts after data lands in QBO |
| 12 | Fix UI issues found (dual-engine sweep v9.2) |
| 13 | Validate MR-020, MR-021, MR-053 features have required data |
| 14 | Generate sweep reports for Intuit sign-off |

### Long-term (Monthly Cadence)

| # | Action |
|---|--------|
| 15 | Monthly sweep cycle: pre-check DB → sweep all accounts → report → fix |
| 16 | Evolve sweep_checks.py with new findings |
| 17 | Monitor cron health (bank transaction confirmation) |
| 18 | Track durability risks and data drift |

---

## 9. CYCLICAL AUDIT RESULTS (Phase 7 — Live DB Validation)

### 9.1 FK Integrity (PASS)

| Check | Result |
|-------|--------|
| Orphan invoice_line_items | **0** (PASS) |
| Orphan bills_line_items | **0** (PASS) |
| Orphan expense_line_items | **0** (PASS) |
| Orphan estimate_line_items | **0** (PASS) |
| Construction FK contamination (customers) | **0** (PASS) |
| Construction FK contamination (projects) | **0** (PASS) |
| Invoices without line items | **0 across all datasets** (PASS) |

### 9.2 QB-03 Date Violations (dates > 365 days)

| Dataset | Violations | Severity |
|---------|-----------|:--------:|
| **CONSTRUCTION** | NONE | PASS |
| **CONSULTING** | inv_create=20, inv_due=27, bill_date=23, bill_due=29, exp_due=14 | **HIGH** |
| **NONPROFIT** | inv_due=315, bill_due=266, exp_due=5 | **CRITICAL** |
| **MANUFACTURING** | inv_due=**934** | **CRITICAL** |
| **TCO** | inv_create=3, inv_due=129, bill_due=8 | **MEDIUM** |

**Impact**: Dates > 365 days break activity plan regeneration (annual cycle). Manufacturing has 934 invoices with due dates exceeding the year boundary.

### 9.3 QB-04 Month Coverage

| Dataset | Invoices | Bills | Expenses | Assessment |
|---------|---------|-------|----------|:----------:|
| **CONSTRUCTION** | 11/12 (missing Dec) | 11/12 | 11/12 | OK |
| **CONSULTING** | 11/12 | 11/12 | 11/12 | OK |
| **NONPROFIT** | **2/12** (only month 0 + 2) | 11/12 | 11/12 | **CRITICAL** |
| **MANUFACTURING** | 11/12 | 11/12 | 11/12 | OK |
| **TCO** | 11/12 | 11/12 | 11/12 | OK |

**NONPROFIT CRITICAL**: 1,918 of 1,920 invoices have `relative_invoice_create_date` near interval '0 days' (all cluster at year start). This means the QBO environment shows all income in January only.

### 9.4 Income Estimates (qty x price_rate from DB)

| Dataset | parent | main_child | secondary_child | other | TOTAL |
|---------|--------|-----------|----------------|-------|-------|
| **CONSTRUCTION** | $4.66M | $7.31M | $4.42M | - | **$16.39M** |
| **TCO** | - | $63.13M | $51.92M | child_3: $179.71M | **$294.75M** |
| **MANUFACTURING** | $22.97M | $60.45M | $200.32M | - | **$283.73M** |

**CONSTRUCTION note**: DB now shows $16.39M vs documented $10.93M. Delta = +$5.46M from PLA-3416 cash flow invoices (93 invoices added).

**TCO/MANUFACTURING**: Very high income volumes. Need cost-side analysis to verify margin health.

### 9.5 Triangulation Summary

| Signal | DB Says | Sweep Says | Coherent? |
|--------|---------|-----------|:---------:|
| Construction P&L | $16.4M income | 9.0/10, 87 realism (clone) | YES (clone uses subset) |
| TCO features | No estimates, no payroll | 7.5/10, 72 realism | YES (explains score ceiling) |
| NP invoice clustering | 98% in month 0 | "Heavy financial anomalies" | YES (root cause identified) |
| MFG date violations | 934 invoices > 365d | 64 realism | YES (explains low score) |
| Consulting low volume | 135 invoices, QB-03 violations | 6.3 realism | YES (thin data + violations) |
| All datasets FK integrity | 0 orphans, 0 contamination | No FK-related sweep findings | YES |

**All signals triangulate coherently.** The DB analysis confirms and explains every sweep finding.

---

## APPENDIX: FK Boundary Map (All Datasets)

| Entity | CONSTRUCTION | CONSULTING | NONPROFIT | CANADA | MANUFACTURING | TCO |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| customer_id | 1-50 | 51-75 | 76-141 | 166-215 | 142-165 | 216-10615 |
| product_id | 2-83, 212 | 84-121 | 122-215 | 263-345 | 216-262 | 346-467 |
| vendor_id | 1-33 | 34-53 | 54-96 | 116-148 | 97-115 | 149-261 |
| project_id | 19-26 | 27-36 | 37-38 | 48-53 | 45-47 | 54-63 |
| employee_id | 1-50 | 51-95 | 96-1295 | 1406-1450 | 1296-1405 | 1451-1700 |
| CoA range | 4-702 | 221-319 | 320-710 | 596-700 | 483-718 | 719-803 |
| bank_acct_id | 5 (Chk), 6 (BOI) | TBD | TBD | TBD | TBD | TBD |
