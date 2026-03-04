"""Investigate QB_COMPANY_TYPES_MATCH v2 - find the actual FK mismatch."""

import psycopg2
import sys

sys.stdout.reconfigure(encoding="utf-8")

CONN = {
    "host": "tbx-postgres-staging.internal",
    "port": 5433,
    "user": "unstable",
    "dbname": "unstable",
    "password": "FaMVkKIM0IcsXHCW_323pJync_ofrBsi",
    "connect_timeout": 10,
}
conn = psycopg2.connect(**CONN)
conn.set_session(readonly=True, autocommit=True)
cur = conn.cursor()

DS = "321c6fa0-a4ee-4e05-b085-7b4d51473495"

# 1. Schema of expenses
print("=== EXPENSE COLUMNS ===")
cur.execute(
    """SELECT column_name FROM information_schema.columns
    WHERE table_name = 'quickbooks_expenses' ORDER BY ordinal_position"""
)
exp_cols = [r[0] for r in cur.fetchall()]
print(exp_cols)

# 2. Schema of expense_line_items
print("\n=== EXPENSE LINE ITEM COLUMNS ===")
cur.execute(
    """SELECT column_name FROM information_schema.columns
    WHERE table_name = 'quickbooks_expense_line_items' ORDER BY ordinal_position"""
)
eli_cols = [r[0] for r in cur.fetchall()]
print(eli_cols)

# 3. Check a sample error expense - full record
print("\n=== SAMPLE EXPENSE 9673 (full) ===")
cur.execute("SELECT * FROM quickbooks_expenses WHERE id = 9673")
if cur.description:
    cols = [d[0] for d in cur.description]
    row = cur.fetchone()
    if row:
        for c, v in zip(cols, row):
            if v is not None:
                print(f"  {c}: {v}")

# 4. Expenses CT vs Vendors CT
print("\n=== EXPENSES vs VENDORS: company_type mismatch ===")
cur.execute(
    """
    SELECT e.id, e.company_type as exp_ct, e.vendor_id, v.company_type as vendor_ct
    FROM quickbooks_expenses e
    JOIN quickbooks_vendors v ON v.id = e.vendor_id AND v.dataset_id = e.dataset_id
    WHERE e.dataset_id = %s
    AND e.company_type <> v.company_type
    ORDER BY e.id
    LIMIT 20
""",
    (DS,),
)
rows = cur.fetchall()
if rows:
    print(f"Found {len(rows)}+ vendor CT mismatches:")
    for r in rows:
        print(f"  Expense {r[0]} (CT={r[1]}) -> Vendor {r[2]} (CT={r[3]})")
else:
    print("No vendor CT mismatch")

# 5. Expenses CT vs Chart of Accounts CT
print("\n=== EXPENSES vs CHART OF ACCOUNTS: company_type mismatch ===")
cur.execute(
    """SELECT column_name FROM information_schema.columns
    WHERE table_name = 'quickbooks_expenses' AND column_name LIKE '%%account%%'"""
)
acc_cols = [r[0] for r in cur.fetchall()]
print(f"Account columns in expenses: {acc_cols}")

if acc_cols:
    for acc_col in acc_cols:
        cur.execute(
            f"""
            SELECT e.id, e.company_type as exp_ct, e.{acc_col}, a.company_type as acc_ct
            FROM quickbooks_expenses e
            JOIN quickbooks_chart_of_accounts a ON a.id = e.{acc_col} AND a.dataset_id = e.dataset_id
            WHERE e.dataset_id = %s
            AND e.company_type <> a.company_type
            ORDER BY e.id
            LIMIT 20
        """,
            (DS,),
        )
        rows = cur.fetchall()
        if rows:
            print(f"  {acc_col}: Found {len(rows)}+ mismatches:")
            for r in rows:
                print(f"    Expense {r[0]} (CT={r[1]}) -> Account {r[2]} (CT={r[3]})")
        else:
            print(f"  {acc_col}: No mismatch")

# 6. TIME ENTRIES - check related objects
print("\n=== TIME ENTRY COLUMNS ===")
cur.execute(
    """SELECT column_name FROM information_schema.columns
    WHERE table_name = 'quickbooks_time_entries' ORDER BY ordinal_position"""
)
te_cols = [r[0] for r in cur.fetchall()]
print(te_cols)

print("\n=== TIME ENTRIES: error IDs vs related objects ===")
te_ids = [77873, 77833, 77825, 77862]
for tid in te_ids:
    cur.execute(
        "SELECT id, company_type, employee_id, project_id, customer_id FROM quickbooks_time_entries WHERE id = %s",
        (tid,),
    )
    r = cur.fetchone()
    if r:
        mismatches = []
        te_ct = r[1]
        # Employee
        if r[2]:
            cur.execute(
                "SELECT company_type FROM quickbooks_employees WHERE id = %s AND dataset_id = %s",
                (r[2], DS),
            )
            emp = cur.fetchone()
            if emp and emp[0] != te_ct:
                mismatches.append(f"emp_id={r[2]} CT={emp[0]}")
        # Project
        if r[3]:
            cur.execute(
                "SELECT company_type FROM quickbooks_projects WHERE id = %s AND dataset_id = %s",
                (r[3], DS),
            )
            proj = cur.fetchone()
            if proj and proj[0] != te_ct:
                mismatches.append(f"proj_id={r[3]} CT={proj[0]}")
        # Customer
        if r[4]:
            cur.execute(
                "SELECT company_type FROM quickbooks_customers WHERE id = %s AND dataset_id = %s",
                (r[4], DS),
            )
            cust = cur.fetchone()
            if cust and cust[0] != te_ct:
                mismatches.append(f"cust_id={r[4]} CT={cust[0]}")
        print(f"  TE {r[0]}: CT={te_ct} | Mismatches: {mismatches if mismatches else 'NONE found in emp/proj/cust'}")

# 7. INTERCOMPANY ACCOUNT MAPPING
print("\n=== INTERCOMPANY ACCOUNT MAPPING ===")
cur.execute(
    """SELECT column_name FROM information_schema.columns
    WHERE table_name = 'quickbooks_intercompany_account_mapping' ORDER BY ordinal_position"""
)
ic_cols = [r[0] for r in cur.fetchall()]
print(f"Columns: {ic_cols}")

cur.execute(
    "SELECT * FROM quickbooks_intercompany_account_mapping WHERE dataset_id = %s ORDER BY id",
    (DS,),
)
rows = cur.fetchall()
print(f"Total: {len(rows)} rows")
for row in rows:
    d = dict(zip(ic_cols, row))
    print(f"  ID={d.get('id')} CT={d.get('company_type')} | {d}")

# 8. Vendor company_types
print("\n=== VENDORS: company_type distribution ===")
cur.execute(
    "SELECT company_type, COUNT(*) FROM quickbooks_vendors WHERE dataset_id = %s GROUP BY company_type",
    (DS,),
)
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")

# 9. Expenses company_types
print("\n=== EXPENSES: company_type distribution ===")
cur.execute(
    "SELECT company_type, COUNT(*) FROM quickbooks_expenses WHERE dataset_id = %s GROUP BY company_type",
    (DS,),
)
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")

conn.close()
print("\nDone.")
