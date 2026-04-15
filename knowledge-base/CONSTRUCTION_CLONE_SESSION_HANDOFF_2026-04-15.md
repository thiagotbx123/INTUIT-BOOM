# Construction-Clone Session Handoff — 2026-04-15

> **PURPOSE**: If the session drops, a new Claude can read this + memory.md and have FULL context.

## TL;DR

Construction-clone dataset was "marretado" (unrealistic margins 56-78%, missing costs). In a 6-hour session we:
1. Investigated the ingestion pipeline deeply (Postgres V2 → Hasura → Platypus → QBO)
2. Inserted 493 bills + 731 payroll + 5716 classifications into V2 DB
3. Fixed 120 date violations, 103 canceled project references, inventory gaps, PO links
4. Audited against ALL 60 checklist rules — 66/66 automated checks PASS
5. Margin is now 18.6% (target 18-28%) — REALISTIC for construction

## Current State: COMMITTED, AWAITING ACTIVITY PLANS

All data is IN the V2 Postgres database. But it's INVISIBLE in QBO until Augusto generates activity plans. This is the ONLY remaining blocker.

## DB Connection (V2 — THE ONLY ONE TO USE)

```
Host: tbx-postgres-v2-unstable.flycast:5432
Database: quickbooks
User: postgres
Password: Urdq28HxbFabZc5
Dataset ID: 321c6fa0-a4ee-4e05-b085-7b4d51473495
```

Legacy DB (5433/unstable) is ABANDONED — never use it.

## What Was Inserted (exact counts)

| Table | Rows Added | ID Range | Notes |
|-------|-----------|----------|-------|
| quickbooks_bills | 493 | 4999-5507 | 16 gaps from margin fix deletions |
| quickbooks_bills_line_items | 1,429 | ~5574-7002 | Includes 31 Fill Dirt LIs |
| quickbooks_bills_line_item_classifications | 5,716 | sequenced | 4 per LI (customer_type, earthwork, utilities, concrete) |
| quickbooks_payroll_expenses | 731 | ~593-1346 | parent=356, secondary_child=375 |
| quickbooks_user_settings | 3 updates | existing rows | legal_name + website for 3 company types |

## What Was Modified (exact counts)

| Table | Rows Modified | What Changed |
|-------|--------------|-------------|
| quickbooks_bills | 41+27+8 | relative_due_date/paid_date clamped to ≤365, 8 moved Dec→Jun-Aug |
| quickbooks_bills_line_items | 19 | project_id from P25/P26 → active projects |
| quickbooks_bills | 76 | purchase_order_id added |
| quickbooks_payroll_expenses | 52 | relative_payment_due_date clamped (includes 17 pre-existing) |
| quickbooks_invoices | 84 | project_id from P25/P26 → active projects |
| quickbooks_invoice_line_items | 438 | project_id changed with parent invoice |
| quickbooks_bills | 16 deleted | Smallest bills removed for margin target |

## Known Issues NOT Fixed

1. **RL-48**: Vendor-product affinity — Blue Bird Insurance assigned 52 different products. Cosmetic only.
2. **RL-46**: PO link at 16% (target 22%) — acceptable.
3. **QB-08**: bill_no has 16 sequence gaps — unknown if engine cares.
4. **Terms distribution**: 31% DueOnReceipt (from date clamping) — slightly high but functional.

## Final P&L Margins

| Company Type | Margin |
|-------------|--------|
| parent | 13.7% |
| main_child | 23.7% |
| secondary_child | 15.1% |
| **CONSOLIDATED** | **18.6%** |

## Scripts (all in ~/Downloads/CONSTRUCTION_CLONE_DELIVERY/scripts/)

**Execution order** (already ran — do NOT re-run unless rolling back):
1. `fix_inline_classifications.py --execute`
2. `fix_purchasing_flag.py --execute`
3. `fix_junction_classifications.py --execute`
4. `populate_cost_gap.py --execute`
5. `fix_blockers.py --execute`
6. Month 12 rebalance (inline)
7. `fix_remaining_issues.py --execute`
8. `fix_margin.py`

**Audit scripts** (safe to re-run anytime):
- `full_checklist_audit.py` — 38 checks (bills, payroll, P&L, FKs)
- `audit_remaining_rules.py` — 31 checks (invoices, expenses, estimates, PIPE)

## Checklist Reference

`~/Downloads/CHECKLIST_INGESTION_CONSTRUCTION (5).xlsx` — 60 rules:
- QB (1-21, 60): Technical DB integrity
- BIZ (22-33): Business realism
- RL (34-48): UI realism
- PIPE (49-59): Pipeline runtime

## Critical Schema Gotchas

- Table names: `quickbooks_purchase_order` (singular), `quickbooks_bills_line_items` (plural)
- Products: "1150 Fill Dirt" has DB id=75 (not 1150)
- Payroll: `id` and `amount` — id is NOT auto-increment, amount does NOT exist in DB
- Bills: `bill_no` is NOT auto-increment
- Invoices: date columns have `_invoice_` prefix (e.g., `relative_invoice_due_date`)
- Bills LIs: `billable` column is NOT NULL

## Next Steps (for new session)

1. Ask Augusto to generate activity plans for construction-clone
2. After QBO propagation, run a sweep to validate UI state
3. Decide on bill_no gap renumbering (ask Augusto if engine tolerates gaps)
4. Move to other datasets: TCO, NonProfit, Manufacturing, Consulting (see DATASET_MASTERY doc)
