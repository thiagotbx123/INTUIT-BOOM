import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg2

DS = "321c6fa0-a4ee-4e05-b085-7b4d51473495"
conn = psycopg2.connect(
    host="tbx-postgres-v2-unstable.flycast",
    port=5432,
    dbname="quickbooks",
    user="postgres",
    password="Urdq28HxbFabZc5",
    sslmode="disable",
    options="-c statement_timeout=60000",
)
cur = conn.cursor()

print("=== AUDIT CYCLE 1: DEEP DATA QUALITY (V2) ===\n")

# --- VENDOR DISTRIBUTION ---
print("--- 5. VENDOR DISTRIBUTION FOR BILLS ---")
cur.execute(f"""
    SELECT b.vendor_id, v.display_name, COUNT(*) as cnt,
           STRING_AGG(DISTINCT b.company_type, ',') as ctypes
    FROM quickbooks_bills b
    JOIN quickbooks_vendors v ON v.id = b.vendor_id AND v.dataset_id = '{DS}'
    WHERE b.dataset_id = '{DS}'
    GROUP BY b.vendor_id, v.display_name
    ORDER BY cnt DESC
""")
for r in cur.fetchall():
    print(f"  V{r[0]:>3d} ({r[1]:>35s}): {r[2]:>3d} bills  [{r[3]}]")

# --- TOP PRODUCTS ---
print("\n--- 6. TOP 20 PRODUCTS IN INVOICE LINE ITEMS ---")
cur.execute(f"""
    SELECT li.product_service_id, ps.name, COUNT(*) as cnt
    FROM quickbooks_invoice_line_items li
    JOIN quickbooks_invoices i ON i.id = li.invoice_id AND i.dataset_id = '{DS}'
    JOIN quickbooks_product_services ps ON ps.id = li.product_service_id AND ps.dataset_id = '{DS}'
    GROUP BY li.product_service_id, ps.name
    ORDER BY cnt DESC
    LIMIT 20
""")
for r in cur.fetchall():
    print(f"  P{r[0]:>3d} ({r[1]:>45s}): {r[2]:>4d} LIs")

# --- UNUSED PRODUCTS ---
print("\n--- 7. PRODUCTS NEVER USED IN ANY TRANSACTION ---")
cur.execute(f"""
    SELECT ps.id, ps.name
    FROM quickbooks_product_services ps
    WHERE ps.dataset_id = '{DS}'
    AND ps.id NOT IN (
        SELECT DISTINCT li.product_service_id FROM quickbooks_invoice_line_items li
        JOIN quickbooks_invoices i ON i.id = li.invoice_id AND i.dataset_id = '{DS}'
        UNION SELECT DISTINCT li.product_service_id FROM quickbooks_bills_line_items li
        JOIN quickbooks_bills b ON b.id = li.bill_id AND b.dataset_id = '{DS}'
        UNION SELECT DISTINCT li.product_service_id FROM quickbooks_estimate_line_items li
        JOIN quickbooks_estimates e ON e.id = li.estimate_id AND e.dataset_id = '{DS}'
        UNION SELECT DISTINCT li.product_service_id FROM quickbooks_purchase_order_line_items li
        JOIN quickbooks_purchase_order p ON p.id = li.purchase_order_id AND p.dataset_id = '{DS}'
    )
    ORDER BY ps.id
""")
unused = cur.fetchall()
print(f"  {len(unused)} products never used (excl expense LIs which have no product_service_id):")
for r in unused:
    print(f"    ID {r[0]:>3d}: {r[1]}")

# --- EMPLOYEES TOP 15 ---
print("\n--- 8. EMPLOYEES IN TIME ENTRIES (TOP 15) ---")
cur.execute(f"""
    SELECT te.employee_id, e.first_name || ' ' || e.last_name as name, COUNT(*) as cnt,
           te.company_type
    FROM quickbooks_time_entries te
    JOIN quickbooks_employees e ON e.id = te.employee_id AND e.dataset_id = '{DS}'
    WHERE te.dataset_id = '{DS}'
    GROUP BY te.employee_id, e.first_name, e.last_name, te.company_type
    ORDER BY cnt DESC
    LIMIT 15
""")
for r in cur.fetchall():
    print(f"  Emp {r[0]:>3d} ({r[1]:>25s}) [{r[3]}]: {r[2]:>4d} entries")

# --- EMPLOYEES WITHOUT TE ---
print("\n--- 9. EMPLOYEES WITHOUT TIME ENTRIES ---")
cur.execute(f"""
    SELECT e.id, e.first_name || ' ' || e.last_name
    FROM quickbooks_employees e
    WHERE e.dataset_id = '{DS}'
    AND e.id NOT IN (
        SELECT DISTINCT te.employee_id FROM quickbooks_time_entries te
        WHERE te.dataset_id = '{DS}'
    )
    ORDER BY e.id
""")
no_te = cur.fetchall()
print(f"  {len(no_te)} employees with zero time entries:")
for r in no_te:
    print(f"    Emp {r[0]:>3d}: {r[1]}")

# --- COA ---
print("\n--- 10. CHART OF ACCOUNTS BY TYPE ---")
cur.execute(f"""
    SELECT account_type, COUNT(*) as cnt
    FROM quickbooks_chart_of_accounts
    WHERE dataset_id = '{DS}'
    GROUP BY account_type
    ORDER BY cnt DESC
""")
for r in cur.fetchall():
    print(f"  {r[0]:>35s}: {r[1]:>3d}")

# --- INVOICE LIs PER PROJECT ---
print("\n--- 11. INVOICE LIs PER PROJECT ---")
cur.execute(f"""
    SELECT li.project_id, p.name as pname, COUNT(*) as cnt,
           SUM(COALESCE(li.qty, 0) * COALESCE(li.price_rate, 0)) as revenue
    FROM quickbooks_invoice_line_items li
    JOIN quickbooks_invoices i ON i.id = li.invoice_id AND i.dataset_id = '{DS}'
    LEFT JOIN quickbooks_projects p ON p.id = li.project_id AND p.dataset_id = '{DS}'
    GROUP BY li.project_id, p.name
    ORDER BY cnt DESC
""")
for r in cur.fetchall():
    pname = r[1] or "NO PROJECT"
    print(f"  P{r[0] or 0:>3d} ({pname:>42s}): {r[2]:>4d} LIs, rev=${r[3]:>12,.2f}")

# --- CLASSIFICATION COVERAGE ---
print("\n--- 12. CLASSIFICATION COVERAGE ---")
pairs = [
    (
        "quickbooks_estimate_line_item_classifications",
        "quickbooks_estimate_line_items",
        "quickbooks_estimates",
        "estimate_id",
    ),
    (
        "quickbooks_purchase_order_line_item_classifications",
        "quickbooks_purchase_order_line_items",
        "quickbooks_purchase_order",
        "purchase_order_id",
    ),
    (
        "quickbooks_invoice_line_item_classifications",
        "quickbooks_invoice_line_items",
        "quickbooks_invoices",
        "invoice_id",
    ),
    ("quickbooks_bills_line_item_classifications", "quickbooks_bills_line_items", "quickbooks_bills", "bill_id"),
    (
        "quickbooks_expense_line_item_classifications",
        "quickbooks_expense_line_items",
        "quickbooks_expenses",
        "expense_id",
    ),
    (
        "quickbooks_payroll_expense_line_item_classifications",
        "quickbooks_payroll_expense_line_items",
        "quickbooks_payroll_expenses",
        "payroll_expense_id",
    ),
]
for class_t, li_t, parent_t, fk_col in pairs:
    cur.execute(
        f"SELECT COUNT(DISTINCT li.id) FROM {li_t} li JOIN {parent_t} p ON p.id = li.{fk_col} AND p.dataset_id = %s",
        (DS,),
    )
    total_li = cur.fetchone()[0]
    cur.execute(
        f"SELECT COUNT(c.id) FROM {class_t} c JOIN {li_t} li ON li.id = c.line_item_id JOIN {parent_t} p ON p.id = li.{fk_col} AND p.dataset_id = %s",
        (DS,),
    )
    our_class = cur.fetchone()[0]
    ratio = our_class / total_li if total_li > 0 else 0
    gap = " *** GAP ***" if our_class == 0 and total_li > 0 else ""
    short = class_t.replace("quickbooks_", "")
    print(f"  {short:>55s}: {our_class:>6d} for {total_li:>5d} LIs (ratio={ratio:.1f}){gap}")

# --- EXPENSE LI COA USAGE ---
print("\n--- 13. EXPENSE LI COA USAGE (TOP 15) ---")
cur.execute(f"""
    SELECT li.chart_of_account_id, coa.name, coa.account_type, COUNT(*) as cnt,
           SUM(li.amount) as total_amount
    FROM quickbooks_expense_line_items li
    JOIN quickbooks_expenses e ON e.id = li.expense_id AND e.dataset_id = '{DS}'
    JOIN quickbooks_chart_of_accounts coa ON coa.id = li.chart_of_account_id AND coa.dataset_id = '{DS}'
    GROUP BY li.chart_of_account_id, coa.name, coa.account_type
    ORDER BY cnt DESC
    LIMIT 15
""")
for r in cur.fetchall():
    print(f"  COA {r[0]:>3d} ({r[1]:>30s} [{r[2]:>15s}]): {r[3]:>4d} LIs, ${r[4]:>10,.2f}")

# --- BILL-PO LINKAGE ---
print("\n--- 14. BILL-PO LINKAGE ---")
cur.execute(f"""
    SELECT COUNT(*) as total, COUNT(b.purchase_order_id) as with_po
    FROM quickbooks_bills b WHERE b.dataset_id = '{DS}'
""")
r = cur.fetchone()
print(f"  Total bills: {r[0]}, With PO: {r[1]} ({r[1] / r[0] * 100:.0f}%), Without PO: {r[0] - r[1]}")

# --- ESTIMATE LI CLASSIFICATION PATTERN ---
print("\n--- 15. CLASSIFICATION PATTERN (reference for CSV gen) ---")
cur.execute(f"""
    SELECT c.line_item_id, COUNT(*) as num_class,
           STRING_AGG(cls.name, ', ') as class_names
    FROM quickbooks_estimate_line_item_classifications c
    JOIN quickbooks_estimate_line_items li ON li.id = c.line_item_id
    JOIN quickbooks_estimates e ON e.id = li.estimate_id AND e.dataset_id = '{DS}'
    JOIN quickbooks_classifications cls ON cls.id = c.classification_value_id AND cls.dataset_id = '{DS}'
    GROUP BY c.line_item_id
    ORDER BY num_class DESC
    LIMIT 10
""")
for r in cur.fetchall():
    print(f"  LI {r[0]:>5d}: {r[1]} classifications -> {r[2][:120]}")

# --- CLASSIFICATION IDS ---
print("\n--- 16. CLASSIFICATIONS HIERARCHY ---")
cur.execute(f"""
    SELECT id, name, parent_id, is_class FROM quickbooks_classifications
    WHERE dataset_id = '{DS}' ORDER BY parent_id NULLS FIRST, id
""")
all_cls = cur.fetchall()
roots = [r for r in all_cls if r[2] is None]
children = {r[0]: r for r in all_cls}
for root in roots:
    flag = " [CLASS]" if root[3] else " [DIM]"
    print(f"  ID={root[0]:>3d}: {root[1]}{flag}")
    kids = [r for r in all_cls if r[2] == root[0]]
    for kid in kids:
        flag2 = " [CLASS]" if kid[3] else ""
        print(f"    ID={kid[0]:>3d}: {kid[1]}{flag2}")
        grandkids = [r for r in all_cls if r[2] == kid[0]]
        for gk in grandkids:
            flag3 = " [CLASS]" if gk[3] else ""
            print(f"      ID={gk[0]:>3d}: {gk[1]}{flag3}")

# --- MAX IDS REFRESH ---
print("\n--- 17. MAX IDS (REFRESHED) ---")
for tbl in [
    "quickbooks_invoices",
    "quickbooks_bills",
    "quickbooks_expenses",
    "quickbooks_estimates",
    "quickbooks_bank_transactions",
    "quickbooks_time_entries",
    "quickbooks_purchase_order",
    "quickbooks_payroll_expenses",
    "quickbooks_projects",
    "quickbooks_customers",
    "quickbooks_vendors",
]:
    cur.execute(f"SELECT MAX(id), COUNT(*) FROM {tbl} WHERE dataset_id = '{DS}'")
    mx, cnt = cur.fetchone()
    print(f"  {tbl.replace('quickbooks_', ''):>25s}: max={mx or 0:>8}, count={cnt}")

for tbl in [
    "quickbooks_invoice_line_items",
    "quickbooks_bills_line_items",
    "quickbooks_expense_line_items",
    "quickbooks_estimate_line_items",
    "quickbooks_purchase_order_line_items",
    "quickbooks_estimate_line_item_classifications",
    "quickbooks_purchase_order_line_item_classifications",
    "quickbooks_invoice_line_item_classifications",
    "quickbooks_bills_line_item_classifications",
    "quickbooks_expense_line_item_classifications",
]:
    cur.execute(f"SELECT MAX(id), COUNT(*) FROM {tbl}")
    mx, cnt = cur.fetchone()
    print(f"  {tbl.replace('quickbooks_', ''):>55s}: max={mx or 0:>8}, count={cnt} (global)")

conn.close()
print("\n=== AUDIT CYCLE 1 COMPLETE ===")
