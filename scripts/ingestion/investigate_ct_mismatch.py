"""Investigate QB_COMPANY_TYPES_MATCH errors from Retool validator."""

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

# 1. EXPENSES: company_type mismatch between expenses and line items
print("=== EXPENSES vs EXPENSE LINE ITEMS: company_type mismatch ===")
cur.execute(
    """
    SELECT e.id, e.company_type as exp_ct, el.id as li_id, el.company_type as li_ct
    FROM quickbooks_expenses e
    JOIN quickbooks_expense_line_items el ON el.expense_id = e.id
    WHERE e.dataset_id = %s
    AND e.company_type <> el.company_type
    ORDER BY e.id
    LIMIT 30
""",
    (DS,),
)
rows = cur.fetchall()
if rows:
    print(f"Found {len(rows)}+ mismatches:")
    for r in rows:
        print(f"  Expense {r[0]} (CT={r[1]}) -> LI {r[2]} (CT={r[3]})")
else:
    print("No mismatch between expenses and line items")

# 2. Check the specific error expense IDs
print()
print("=== SAMPLE ERROR EXPENSE IDs ===")
error_ids = [9673, 10230, 10069, 10062, 9816, 9793, 10196, 10102]
for eid in error_ids:
    cur.execute(
        "SELECT id, company_type, vendor_id FROM quickbooks_expenses WHERE id = %s",
        (eid,),
    )
    exp = cur.fetchone()
    if exp:
        cur.execute(
            "SELECT id, company_type FROM quickbooks_expense_line_items WHERE expense_id = %s",
            (eid,),
        )
        lis = cur.fetchall()
        li_cts = set(li[1] for li in lis)
        print(f"  Expense {exp[0]}: CT={exp[1]}, vendor={exp[2]} | LIs: {len(lis)}, CTs={li_cts}")
    else:
        print(f"  Expense {eid}: NOT FOUND in DB")

# 3. What company_types exist in expenses?
print()
print("=== EXPENSES: company_type distribution ===")
cur.execute(
    """
    SELECT company_type, COUNT(*)
    FROM quickbooks_expenses
    WHERE dataset_id = %s
    GROUP BY company_type
    ORDER BY company_type
""",
    (DS,),
)
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")

print()
print("=== EXPENSE LINE ITEMS: company_type distribution ===")
cur.execute(
    """
    SELECT el.company_type, COUNT(*)
    FROM quickbooks_expense_line_items el
    JOIN quickbooks_expenses e ON e.id = el.expense_id
    WHERE e.dataset_id = %s
    GROUP BY el.company_type
    ORDER BY el.company_type
""",
    (DS,),
)
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")

# 4. TIME ENTRIES: check what they relate to
print()
print("=== TIME ENTRIES: error IDs ===")
te_ids = [77873, 77833, 77825, 77862]
for tid in te_ids:
    cur.execute(
        """
        SELECT te.id, te.company_type, te.employee_id, te.project_id
        FROM quickbooks_time_entries te
        WHERE te.id = %s
    """,
        (tid,),
    )
    r = cur.fetchone()
    if r:
        # Check employee CT
        cur.execute(
            "SELECT company_type FROM quickbooks_employees WHERE id = %s AND dataset_id = %s",
            (r[2], DS),
        )
        emp = cur.fetchone()
        # Check project CT
        cur.execute(
            "SELECT company_type FROM quickbooks_projects WHERE id = %s AND dataset_id = %s",
            (r[3], DS) if r[3] else (0, DS),
        )
        proj = cur.fetchone()
        print(
            f"  TE {r[0]}: CT={r[1]}, emp_id={r[2]} (emp_CT={emp[0] if emp else 'N/A'}), proj_id={r[3]} (proj_CT={proj[0] if proj else 'N/A'})"
        )
    else:
        print(f"  TE {tid}: NOT FOUND")

# 5. INTERCOMPANY ACCOUNT MAPPING
print()
print("=== INTERCOMPANY ACCOUNT MAPPING ===")
try:
    cur.execute(
        """
        SELECT id, company_type, dataset_id
        FROM quickbooks_intercompany_account_mapping
        WHERE dataset_id = %s
        ORDER BY id
    """,
        (DS,),
    )
    rows = cur.fetchall()
    print(f"Total: {len(rows)} rows")
    for r in rows:
        print(f"  ID={r[0]}, CT={r[1]}")

    # Check what related objects it references
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'quickbooks_intercompany_account_mapping'
        ORDER BY ordinal_position
    """
    )
    cols = [r[0] for r in cur.fetchall()]
    print(f"Columns: {cols}")

    cur.execute(
        "SELECT * FROM quickbooks_intercompany_account_mapping WHERE dataset_id = %s ORDER BY id",
        (DS,),
    )
    for row in cur.fetchall():
        print(f"  {dict(zip(cols, row))}")
except Exception as e:
    print(f"Error: {e}")

conn.close()
print("\nDone.")
