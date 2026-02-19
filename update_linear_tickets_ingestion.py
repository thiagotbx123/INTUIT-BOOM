"""
Update Linear tickets with ingestion status, CSVs, and orientations.
Posts clear English comments to each relevant ticket for Augusto and the team.
"""

import os
import requests
import json
import time

API_URL = "https://api.linear.app/graphql"
API_KEY = os.environ.get("LINEAR_API_KEY", "")
HEADERS = {"Content-Type": "application/json", "Authorization": API_KEY}

DRIVE_FOLDER = (
    "https://drive.google.com/drive/folders/1UbG-jxeF8l-b5cOA9MGlJKFfOR6AvQ-p"
)
DATASET_ID = "321c6fa0-a4ee-4e05-b085-7b4d51473495"


def get_issue_id(identifier: str) -> str:
    """Get Linear issue UUID from identifier like PLA-3212"""
    query = """
    query ($filter: IssueFilter) {
      issues(filter: $filter, first: 1) {
        nodes { id identifier title state { name } }
      }
    }
    """
    number = int(identifier.split("-")[1])
    variables = {
        "filter": {
            "number": {"eq": number},
            "team": {"key": {"eq": identifier.split("-")[0]}},
        }
    }
    resp = requests.post(
        API_URL, headers=HEADERS, json={"query": query, "variables": variables}
    )
    data = resp.json()
    nodes = data.get("data", {}).get("issues", {}).get("nodes", [])
    if nodes:
        node = nodes[0]
        print(
            f"  Found: {node['identifier']} - {node['title']} [{node['state']['name']}]"
        )
        return node["id"]
    print(f"  WARNING: {identifier} not found!")
    return None


def post_comment(issue_id: str, body: str, identifier: str) -> bool:
    """Post a comment to a Linear issue"""
    query = """
    mutation CommentCreate($input: CommentCreateInput!) {
        commentCreate(input: $input) {
            success
            comment { id }
        }
    }
    """
    variables = {"input": {"issueId": issue_id, "body": body}}
    resp = requests.post(
        API_URL, headers=HEADERS, json={"query": query, "variables": variables}
    )
    result = resp.json()
    success = result.get("data", {}).get("commentCreate", {}).get("success", False)
    if success:
        print(f"  OK - Comment posted to {identifier}")
    else:
        print(f"  FAIL - {identifier}: {json.dumps(result, indent=2)}")
    return success


# ============================================================
# COMMENTS PER TICKET
# ============================================================

TICKET_COMMENTS = {
    # ---- MAIN ORCHESTRATION TICKET ----
    "PLA-3212": """# Construction Dataset Ingestion - Status Update (Feb 9, 2026)

## Current Status: READY FOR INGESTION

All **15 CSV files** (10,831 rows total) have been generated, audited (**189/189 checks PASS**), and organized.

**Google Drive folder with all files:** """
    + DRIVE_FOLDER
    + """

---

## What We Built

We generated a complete financial dataset for Keystone Construction over 9 sessions. Here is what is ready:

| # | File | Table | Rows | Action | Delimiter |
|---|------|-------|------|--------|-----------|
| 01 | INGESTION_INVOICES_v12.csv | quickbooks_invoices | 335 | REPLACE | , |
| 02 | INGESTION_INVOICE_LINE_ITEMS_v8.csv | quickbooks_invoice_line_items | 1,686 | REPLACE | **;** |
| 03 | INGESTION_EXPENSES_v4.csv | quickbooks_expenses | 650 | REPLACE | , |
| 04 | INGESTION_EXPENSE_LINE_ITEMS_v4.csv | quickbooks_expense_line_items | 1,006 | REPLACE | , |
| 05 | INGESTION_BILLS_v5.csv | quickbooks_bills | 96 | REPLACE | , |
| 06 | INGESTION_BILLS_LINE_ITEMS_v5.csv | quickbooks_bills_line_items | 149 | REPLACE | , |
| 07 | INGESTION_ESTIMATES_v1.csv | quickbooks_estimates | 75 | REPLACE | , |
| 08 | INGESTION_ESTIMATE_LINE_ITEMS_v1.csv | quickbooks_estimate_line_items | 410 | REPLACE | , |
| 09 | INGESTION_ESTIMATE_LI_CLASSIFICATIONS_v1.csv | quickbooks_estimate_line_item_classifications | 1,640 | REPLACE | , |
| 10 | INGESTION_BANK_TRANSACTIONS_v1.csv | quickbooks_bank_transactions | 155 | REPLACE | , |
| 11 | PLA-3261_TIME_ENTRIES_v5_supplement.csv | quickbooks_time_entries | 3,996 | **APPEND** | **;** |
| 12 | INGESTION_PROJECT_TASKS_v1.csv | quickbooks_project_tasks | 65 | INSERT | , |
| 13 | INGESTION_PURCHASE_ORDERS_v1.csv | quickbooks_purchase_orders | 48 | INSERT | , |
| 14 | INGESTION_PO_LINE_ITEMS_v1.csv | quickbooks_purchase_order_line_items | 104 | INSERT | , |
| 15 | INGESTION_PO_LI_CLASSIFICATIONS_v1.csv | quickbooks_purchase_order_line_item_classifications | 416 | INSERT | , |

---

## 3-Phase Ingestion Plan

### Phase 1 - DELETE old data (children first, then parents)
Delete all rows for dataset `"""
    + DATASET_ID
    + """` in this order:
1. quickbooks_estimate_line_item_classifications (417 rows - delete by line_item_id, see guide)
2. quickbooks_invoice_line_items (1,407 rows)
3. quickbooks_invoices (270 rows)
4. quickbooks_expense_line_items (667 rows)
5. quickbooks_expenses (667 rows)
6. quickbooks_bills_line_items (134 rows)
7. quickbooks_bills (62 rows)
8. quickbooks_estimate_line_items (104 rows)
9. quickbooks_estimates (8 rows)
10. quickbooks_bank_transactions (56 rows)

**DO NOT DELETE:** payroll tables, time_entries, classifications, customers, vendors, employees, COA, products.

### Phase 2 - INSERT new data (parents first, then children)
Follow CSV numbering 01 through 15. Time entries (#11) is APPEND ONLY.

### Phase 3 - VERIFY row counts
Check each table matches the expected rows listed above.

---

## P&L Targets (for post-ingestion health check)

| Company Type | Income | Net Profit | Margin |
|---|---|---|---|
| parent (Keystone Construction) | $3.02M | +$766K | 25.4% |
| main_child (BlueCraft) | $5.11M | +$1.46M | 28.5% |
| secondary_child (Terra, Volt, etc) | $2.80M | +$700K | 25.0% |
| **TOTAL** | **$10.93M** | **+$2.93M** | **26.8%** |

---

## Important Warnings

1. **Delimiter:** Files #02 (Invoice LIs) and #11 (Time Entries) use **semicolon (;)** delimiter. All others use comma.
2. **Time Entries is APPEND only** - do NOT delete existing time entries. Only add the 3,996 new rows.
3. **Purchase Orders table** may need to be created if it does not exist yet. Check if table name is singular or plural.
4. **Bills v5 was fixed** on Feb 8 for bug TXN-13131 (bill-PO product mismatch). Make sure you use the latest version.
5. **20 bugs were found and fixed** during generation. All are documented in the handoff guide.

---

## Post-Ingestion Checklist

After ingestion, please verify:
- [ ] Employee count (watch for duplicates from QBO API retry)
- [ ] P&L is positive per company type per month
- [ ] Bank accounts match cross-entity (parent=5, child=6)
- [ ] IC transactions appear on both sides
- [ ] Balance Sheet has no warnings
- [ ] Project count matches (6 projects)
- [ ] Inventory has no large negatives
- [ ] Activity plans executed successfully

---

## Risks to Watch

1. **Employee duplication**: QBO sometimes creates duplicates on API retry (we saw 90 dupes before)
2. **Third-party contamination**: Intuit SEs with admin access may create records
3. **Gateway timeout**: CSVs with 3K+ rows may timeout (Time Entries has 3,996)

Full step-by-step guide: `GUIA_INGESTION_AUGUSTO.md` (in the Drive folder)
Checklist with 59 rules: `CHECKLIST_INGESTION_CONSTRUCTION.xlsx` (in the Drive folder)

**Contact Thiago if you have any questions or blockers.**
""",
    # ---- INVOICES ----
    "PLA-3257": """# Invoices - Ingestion Update (Feb 9, 2026)

## Status: CSV READY - Waiting for ingestion

### What is ready
- **File 01:** `INGESTION_INVOICES_v12.csv` - 335 invoices (IDs 45135-45469), delimiter: comma
- **File 02:** `INGESTION_INVOICE_LINE_ITEMS_v8.csv` - 1,686 line items (IDs 119728-121413), delimiter: **semicolon (;)**

### How to ingest
1. DELETE existing invoices and invoice line items for dataset `"""
    + DATASET_ID
    + """`
2. Delete line items FIRST (1,407 rows), then invoices (270 rows)
3. INSERT invoices (file 01), then insert line items (file 02)
4. Verify: 335 invoices, 1,686 line items

### Important notes
- Invoice line items use **semicolon (;)** as delimiter, not comma
- Includes 8 IC (intercompany) invoices linking parent/child entities
- All invoices have dates within 365 days (relative_date format)
- Each invoice has 1-25 line items (realistic log-normal distribution)
- Amount range: $500 - $200K
- Customer-project affinity maintained (1-2 projects per customer)

### Dependencies
- Customers table must exist (50 customers already in DB - no changes needed)
- Products table must exist (83 products already in DB - no changes needed)

### Quality
- Passed all 189/189 audit checks
- 12 versions of iteration to reach production quality
- P&L contribution: Total invoice income = $10.93M across 3 company types

**Files in Google Drive:** """
    + DRIVE_FOLDER
    + """
""",
    # ---- BILLS ----
    "PLA-3258": """# Bills - Ingestion Update (Feb 9, 2026)

## Status: CSV READY - Waiting for ingestion (Bug TXN-13131 FIXED)

### What is ready
- **File 05:** `INGESTION_BILLS_v5.csv` - 96 bills (IDs 4903-4998), delimiter: comma
- **File 06:** `INGESTION_BILLS_LINE_ITEMS_v5.csv` - 149 line items (IDs 5567-5715), delimiter: comma

### How to ingest
1. DELETE existing bills line items (134 rows), then bills (62 rows) for dataset `"""
    + DATASET_ID
    + """`
2. INSERT bills (file 05), then insert line items (file 06)
3. Verify: 96 bills, 149 line items

### Bug Fix Applied (Feb 8, 2026)
**TXN-13131:** 15 out of 30 bills linked to POs had ZERO products in common with their PO. QBO rejects this with error "To link lines between a purchase order and a transaction, you'll need the lines to have the same account and item details."

Fix: 6 bills reassigned to matching POs, 9 bills unlinked, 3 bills improved. Now 21 bills have valid PO links with 0 risk.

### Important notes
- 21 bills are linked to Purchase Orders (~22% of total)
- All bills have `paid_date` filled (NOT NULL required)
- Bank account: parent=5, main_child=6, secondary_child=6
- Bill status is empty string when paid (QBO convention)
- Terms distribution: Net 30 (40%), Net 45 (25%), Net 60 (20%), Due on Receipt (10%), Net 90 (5%)
- Bills only reference purchasable products
- Vendor-product affinity maintained (consistent vendor specialization)

### Dependencies
- Vendors table must exist (33 vendors already in DB - no changes needed)
- Products table must exist (83 products already in DB - no changes needed)

### P&L contribution
Total bills cost = $1.52M across all company types

**Files in Google Drive:** """
    + DRIVE_FOLDER
    + """
""",
    # ---- EXPENSES ----
    "PLA-3259": """# Expenses - Ingestion Update (Feb 9, 2026)

## Status: CSV READY - Waiting for ingestion

### What is ready
- **File 03:** `INGESTION_EXPENSES_v4.csv` - 650 expenses (IDs 9645-10294), delimiter: comma
- **File 04:** `INGESTION_EXPENSE_LINE_ITEMS_v4.csv` - 1,006 line items (IDs 8016-9021), delimiter: comma

### How to ingest
1. DELETE existing expense line items (667 rows), then expenses (667 rows) for dataset `"""
    + DATASET_ID
    + """`
2. INSERT expenses (file 03), then insert line items (file 04)
3. Verify: 650 expenses, 1,006 line items

### Important notes
- ~7-10% of expenses are linked to estimates (cross-table reference)
- `billed_project_id` populated from line item project IDs
- All expenses have valid account references
- Budget caps enforced (costs < income per company type per month)
- 5-8 note templates with 40% having no notes (realistic variation)

### Dependencies
- Customers/Vendors tables must exist (already in DB - no changes needed)
- Estimates should be ingested first if you want the cross-links to work

### P&L contribution
Total expenses cost = $4.00M across all company types

**Files in Google Drive:** """
    + DRIVE_FOLDER
    + """
""",
    # ---- TIME ENTRIES ----
    "PLA-3261": """# Time Entries Data Quality - Ingestion Update (Feb 9, 2026)

## Status: CSV READY - APPEND ONLY (do NOT delete existing)

### What is ready
- **File 11:** `PLA-3261_TIME_ENTRIES_v5_supplement.csv` - 3,996 new rows (IDs 73993-77988), delimiter: **semicolon (;)**

### How to ingest
1. **DO NOT delete** existing time entries (3,944 rows with IDs from v4)
2. **APPEND** the 3,996 new rows from file 11
3. Verify total: 7,940 time entries (3,944 existing + 3,996 new)

### Why this supplement exists
Projects 23-26 had **zero time entries** in the original dataset. Also, the original v4 only covered March through November - missing January, February, and December. This supplement fills those gaps.

### Important notes
- Uses **semicolon (;)** as delimiter
- Has trailing semicolons on each row (same format as v4, the ingestion tool handles this)
- May have `#N/D` values in some columns (same as v4 format)
- IDs start at 73993 to avoid collision with existing entries

### What to watch after ingestion
- Time entries should cover all 12 months (Jan-Dec)
- All 6 projects should have time entries
- No duplicate entries (check by employee + date + project combination)

### Risk
This is a large CSV (3,996 rows). If you get a **gateway timeout (504)**, try splitting it into smaller batches (e.g., 1,000 rows each).

**File in Google Drive:** """
    + DRIVE_FOLDER
    + """
""",
    # ---- EMPLOYEES ----
    "PLA-3251": """# Employees - Status Update (Feb 9, 2026)

## Status: NO CSV CHANGES NEEDED - Reference data already correct

### Current state
- 45 employees already in the database for this dataset
- Data is clean and correct
- No new CSV needed for employees

### Important context
On Jan 27, we found and fixed **90 duplicate employees** in the Keystone Payroll (see PLA-3227). Root cause was QBO-side API retry creating duplicates. All duplicates were manually deleted.

### What to verify after full ingestion
- Employee count should remain at 45
- Watch for new duplicates (QBO retry risk)
- If duplicates appear, delete manually (same process as PLA-3227)

### Company distribution
- parent (Keystone Construction): 4 employees in payroll
- main_child (BlueCraft): all payroll employees ($1.78M payroll cost)
- secondary_child: no direct employees

**No action needed on this ticket for the current ingestion cycle.**
""",
    # ---- CUSTOMERS ----
    "PLA-3252": """# Customers - Status Update (Feb 9, 2026)

## Status: NO CSV CHANGES NEEDED - Reference data already correct

### Current state
- 50 customers already in the database for this dataset
- Data is clean and correct
- No new CSV needed for customers

### Dependencies
Customers must be present BEFORE ingesting invoices (file 01). Since they are already in DB, invoices can be ingested immediately.

### What to verify
- All 50 customers exist and have correct IDs
- Customer-project affinity is maintained (1-2 projects per customer)

**No action needed on this ticket for the current ingestion cycle.**
""",
    # ---- VENDORS ----
    "PLA-3253": """# Vendors - Status Update (Feb 9, 2026)

## Status: NO CSV CHANGES NEEDED - Reference data already correct

### Current state
- 33 vendors already in the database for this dataset
- Data is clean and correct
- No new CSV needed for vendors

### Dependencies
Vendors must be present BEFORE ingesting bills (file 05) and expenses (file 03). Since they are already in DB, those files can be ingested immediately.

### What to verify
- All 33 vendors exist and have correct IDs
- Vendor-product affinity is maintained (each vendor has consistent product specialization)

**No action needed on this ticket for the current ingestion cycle.**
""",
    # ---- CHART OF ACCOUNTS ----
    "PLA-3254": """# Chart of Accounts - Status Update (Feb 9, 2026)

## Status: NO CSV CHANGES NEEDED - Reference data already correct

### Current state
- 121 accounts already in the database for this dataset
- Data is clean and correct
- No new CSV needed for COA

### Key accounts to verify after ingestion
- Bank accounts: parent uses account 5, child entities use account 6
- COGS accounts: FIFO-based (38 inventory products generate COGS on invoice creation)
- IC accounts: Account 1083 was created manually for intercompany mappings (see PLA-3201)

### Note about SALES divergence
The ticket description mentions 102 accounts in SALES vs 121 in dataset. This is expected - the Construction dataset has more accounts because it includes construction-specific categories (project costing, certified payroll, equipment depreciation, etc.).

**No action needed on this ticket for the current ingestion cycle.**
""",
    # ---- PRODUCTS & SERVICES ----
    "PLA-3260": """# Products & Services - Status Update (Feb 9, 2026)

## Status: NO CSV CHANGES NEEDED - Reference data already correct

### Current state
- 83 products/services already in the database for this dataset
- Includes 38 inventory products + 45 service products
- Data is clean and correct
- No new CSV needed

### Important context
- 38 inventory products generate COGS via FIFO when invoices are created
- Products are mapped to projects via marketplace trades (8 project affiliations)
- Bills only reference purchasable products (validated in our audit)
- No duplicate products per invoice (validated)

### Note about SALES divergence
The ticket mentions 188 products in SALES vs 83 in dataset. The difference is expected - SALES has products from ALL datasets, while our dataset only has Construction-specific products.

**No action needed on this ticket for the current ingestion cycle.**
""",
}


def main():
    print("=" * 60)
    print("LINEAR TICKET UPDATER - Construction Ingestion")
    print("=" * 60)
    print()

    success_count = 0
    fail_count = 0
    skip_count = 0

    for identifier, comment in TICKET_COMMENTS.items():
        print(f"\n--- {identifier} ---")
        issue_id = get_issue_id(identifier)
        if not issue_id:
            print(f"  SKIPPED: Could not find {identifier}")
            skip_count += 1
            continue

        if post_comment(issue_id, comment, identifier):
            success_count += 1
        else:
            fail_count += 1

        time.sleep(0.5)  # Rate limit respect

    print()
    print("=" * 60)
    print(f"DONE: {success_count} posted, {fail_count} failed, {skip_count} skipped")
    print("=" * 60)


if __name__ == "__main__":
    main()
