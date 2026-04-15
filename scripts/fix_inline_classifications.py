"""
Fix inline classification columns for expense_line_items and bills_line_items.

Target: construction-clone dataset (321c6fa0-...)
Action: UPDATE NULL customer_type/earthwork_class/utilities_class/concrete_class
Pattern: Randomize from existing valid IDs (same distribution as populated rows)

Classification IDs:
  customer_type: 6 (Residential), 7 (Government), 8 (Commercial)
  earthwork_class: 15 (Grading), 16 (Excavating)
  utilities_class: 17 (Sewer), 18 (Gas), 19 (Water), 20 (Cabling), 21 (Other), 22 (Electrical)
  concrete_class: 26 (Poured), 27 (Block), 28 (Slab)

Usage:
  python fix_inline_classifications.py               # dry-run
  python fix_inline_classifications.py --execute      # apply changes
  python fix_inline_classifications.py --rollback     # set back to NULL
"""

import sys
import argparse
import random

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATASET_ID = "321c6fa0-a4ee-4e05-b085-7b4d51473495"

CUSTOMER_TYPES = [6, 7, 8]
EARTHWORK = [15, 16]
UTILITIES = [17, 18, 19, 20, 21, 22]
CONCRETE = [26, 27, 28]

V2_CONN = {
    "host": "tbx-postgres-v2-unstable.flycast",
    "port": 5432,
    "user": "postgres",
    "dbname": "quickbooks",
    "password": "Urdq28HxbFabZc5",
    "connect_timeout": 15,
    "sslmode": "disable",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()

    import psycopg2

    conn = psycopg2.connect(**V2_CONN)
    cur = conn.cursor()

    if args.rollback:
        print("=== ROLLBACK: Setting classifications back to NULL ===")
        for tbl, fk, parent in [
            ("quickbooks_expense_line_items", "expense_id", "quickbooks_expenses"),
            ("quickbooks_bills_line_items", "bill_id", "quickbooks_bills"),
        ]:
            cur.execute(
                f"""
                UPDATE {tbl} li SET customer_type = NULL, earthwork_class = NULL,
                    utilities_class = NULL, concrete_class = NULL
                FROM {parent} p
                WHERE p.id = li.{fk} AND p.dataset_id = %s
                AND li.customer_type IS NOT NULL
            """,
                (DATASET_ID,),
            )
            print(f"  {tbl}: {cur.rowcount} rows reset to NULL")
        if args.execute:
            conn.commit()
            print("COMMITTED rollback")
        else:
            conn.rollback()
            print("DRY-RUN rollback (not committed)")
        conn.close()
        return

    random.seed(42)

    for tbl, fk, parent in [
        ("quickbooks_expense_line_items", "expense_id", "quickbooks_expenses"),
        ("quickbooks_bills_line_items", "bill_id", "quickbooks_bills"),
    ]:
        cur.execute(
            f"""
            SELECT li.id FROM {tbl} li
            JOIN {parent} p ON p.id = li.{fk} AND p.dataset_id = %s
            WHERE li.customer_type IS NULL
            ORDER BY li.id
        """,
            (DATASET_ID,),
        )
        null_ids = [r[0] for r in cur.fetchall()]
        print(f"\n{tbl}: {len(null_ids)} rows with NULL classifications")

        if not null_ids:
            continue

        updated = 0
        for li_id in null_ids:
            ct = random.choice(CUSTOMER_TYPES)
            ew = random.choice(EARTHWORK)
            ut = random.choice(UTILITIES)
            co = random.choice(CONCRETE)

            cur.execute(
                f"""
                UPDATE {tbl} SET customer_type = %s, earthwork_class = %s,
                    utilities_class = %s, concrete_class = %s
                WHERE id = %s
            """,
                (ct, ew, ut, co, li_id),
            )
            updated += 1

        print(f"  Updated: {updated} rows")
        print(
            f"  Sample: id={null_ids[0]} → ct={random.choice(CUSTOMER_TYPES)}, ew={random.choice(EARTHWORK)}, ut={random.choice(UTILITIES)}, co={random.choice(CONCRETE)}"
        )

    if args.execute:
        conn.commit()
        print("\n=== COMMITTED ===")
    else:
        conn.rollback()
        print("\n=== DRY-RUN (not committed) ===")
        print("Run with --execute to apply changes")

    cur.execute(
        """
        SELECT 'expense_line_items' as tbl, COUNT(*), COUNT(customer_type)
        FROM quickbooks_expense_line_items li
        JOIN quickbooks_expenses e ON e.id = li.expense_id AND e.dataset_id = %s
        UNION ALL
        SELECT 'bills_line_items', COUNT(*), COUNT(customer_type)
        FROM quickbooks_bills_line_items li
        JOIN quickbooks_bills b ON b.id = li.bill_id AND b.dataset_id = %s
    """,
        (DATASET_ID, DATASET_ID),
    )
    print("\n=== VERIFICATION ===")
    for r in cur.fetchall():
        pct = r[2] / r[1] * 100 if r[1] > 0 else 0
        print(f"  {r[0]}: {r[2]}/{r[1]} ({pct:.0f}%) classified")

    conn.close()


if __name__ == "__main__":
    main()
