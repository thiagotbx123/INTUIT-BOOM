"""
Insert 93 cash flow fix invoices + 422 line items into V2 quickbooks database.
Target: tbx-postgres-v2-unstable.flycast:5432 / database: quickbooks

Requires: psycopg2-binary, V2 credentials from AWS Secrets Manager
          (dataset-v2/unstable/postgres-connection-string)
          Tailscale VPN must be connected.

Usage:
  python insert_cashflow_invoices_v2.py               # dry-run (default)
  python insert_cashflow_invoices_v2.py --execute      # actually insert
  python insert_cashflow_invoices_v2.py --rollback     # delete inserted rows
"""

import csv
import sys
import os
import argparse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.expanduser("~/Downloads")

INVOICES_CSV = os.path.join(CSV_DIR, "CASHFLOW_FIX_INVOICES_DB.csv")
LINE_ITEMS_CSV = os.path.join(CSV_DIR, "CASHFLOW_FIX_LINE_ITEMS_DB.csv")

INVOICE_ID_RANGE = (45470, 45562)
LINE_ITEM_ID_RANGE = (121414, 121835)
DATASET_ID = "321c6fa0-a4ee-4e05-b085-7b4d51473495"

V2_CONN = {
    "host": "tbx-postgres-v2-unstable.flycast",
    "port": 5432,
    "user": os.environ.get("V2_DB_USER", ""),
    "dbname": "quickbooks",
    "password": os.environ.get("V2_DB_PASSWORD", ""),
    "connect_timeout": 15,
    "sslmode": "disable",
}


def load_invoices():
    with open(INVOICES_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 93, f"Expected 93 invoices, got {len(rows)}"
    return rows


def load_line_items():
    with open(LINE_ITEMS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        rows = list(reader)
    assert len(rows) == 422, f"Expected 422 line items, got {len(rows)}"
    return rows


def check_no_conflicts(cur):
    cur.execute(
        "SELECT COUNT(*) FROM quickbooks_invoices WHERE id >= %s AND id <= %s",
        INVOICE_ID_RANGE,
    )
    count = cur.fetchone()[0]
    if count > 0:
        print(f"WARNING: {count} invoices already exist in ID range {INVOICE_ID_RANGE}")
        return False

    cur.execute(
        "SELECT COUNT(*) FROM quickbooks_invoice_line_items WHERE id >= %s AND id <= %s",
        LINE_ITEM_ID_RANGE,
    )
    count = cur.fetchone()[0]
    if count > 0:
        print(f"WARNING: {count} line items already exist in ID range {LINE_ITEM_ID_RANGE}")
        return False

    print("No conflicts found - ID ranges are clear.")
    return True


def check_dataset_exists(cur):
    cur.execute(
        "SELECT COUNT(*) FROM datasets WHERE id = %s",
        (DATASET_ID,),
    )
    count = cur.fetchone()[0]
    if count == 0:
        print(f"ERROR: Dataset {DATASET_ID} not found in V2 database!")
        return False
    print(f"Dataset {DATASET_ID} exists in V2.")
    return True


def insert_invoices(cur, rows):
    cols = rows[0].keys()
    placeholders = ", ".join(["%s"] * len(cols))
    col_names = ", ".join(cols)
    sql = f"INSERT INTO quickbooks_invoices ({col_names}) VALUES ({placeholders})"

    inserted = 0
    for row in rows:
        values = []
        for c in cols:
            v = row[c]
            if v == "" or v is None:
                values.append(None)
            elif v.lower() in ("true", "false"):
                values.append(v.lower() == "true")
            else:
                values.append(v)
        cur.execute(sql, values)
        inserted += 1

    return inserted


def insert_line_items(cur, rows):
    cols = rows[0].keys()
    placeholders = ", ".join(["%s"] * len(cols))
    col_names = ", ".join(cols)
    sql = f"INSERT INTO quickbooks_invoice_line_items ({col_names}) VALUES ({placeholders})"

    inserted = 0
    for row in rows:
        values = []
        for c in cols:
            v = row[c]
            if v == "" or v is None:
                values.append(None)
            else:
                values.append(v)
        cur.execute(sql, values)
        inserted += 1

    return inserted


def rollback_data(cur):
    cur.execute(
        "DELETE FROM quickbooks_invoice_line_items WHERE id >= %s AND id <= %s",
        LINE_ITEM_ID_RANGE,
    )
    li_deleted = cur.rowcount
    cur.execute(
        "DELETE FROM quickbooks_invoices WHERE id >= %s AND id <= %s",
        INVOICE_ID_RANGE,
    )
    inv_deleted = cur.rowcount
    return inv_deleted, li_deleted


def main():
    parser = argparse.ArgumentParser(description="Insert cash flow fix invoices into V2")
    parser.add_argument("--execute", action="store_true", help="Actually insert data")
    parser.add_argument("--rollback", action="store_true", help="Delete inserted rows")
    args = parser.parse_args()

    if not V2_CONN["user"] or not V2_CONN["password"]:
        print("ERROR: Set V2_DB_USER and V2_DB_PASSWORD environment variables.")
        print("  Credentials from AWS Secrets Manager: dataset-v2/unstable/postgres-connection-string")
        print("  Or ask Augusto for the connection string.")
        sys.exit(1)

    import psycopg2

    print(f"Connecting to V2: {V2_CONN['host']}:{V2_CONN['port']}/{V2_CONN['dbname']}")
    conn = psycopg2.connect(**V2_CONN)

    if args.rollback:
        cur = conn.cursor()
        inv_del, li_del = rollback_data(cur)
        conn.commit()
        print(f"Rollback complete: {inv_del} invoices, {li_del} line items deleted.")
        conn.close()
        return

    if not args.execute:
        conn.set_session(readonly=True, autocommit=True)
        cur = conn.cursor()
        print("\n=== DRY RUN (read-only) ===")
        check_dataset_exists(cur)
        check_no_conflicts(cur)

        invoices = load_invoices()
        line_items = load_line_items()
        print(f"\nReady to insert: {len(invoices)} invoices + {len(line_items)} line items")
        print("Run with --execute to actually insert.")
        conn.close()
        return

    cur = conn.cursor()
    print("\n=== EXECUTING INSERT ===")

    if not check_dataset_exists(cur):
        conn.close()
        sys.exit(1)

    if not check_no_conflicts(cur):
        print("Aborting due to conflicts. Use --rollback first if needed.")
        conn.close()
        sys.exit(1)

    invoices = load_invoices()
    line_items = load_line_items()

    inv_count = insert_invoices(cur, invoices)
    print(f"Inserted {inv_count} invoices")

    li_count = insert_line_items(cur, line_items)
    print(f"Inserted {li_count} line items")

    conn.commit()
    print(f"\nDONE: {inv_count} invoices + {li_count} line items committed to V2.")

    cur.execute(
        "SELECT COUNT(*) FROM quickbooks_invoices WHERE id >= %s AND id <= %s",
        INVOICE_ID_RANGE,
    )
    verify = cur.fetchone()[0]
    print(f"Verification: {verify} invoices in range (expected 93)")

    conn.close()


if __name__ == "__main__":
    main()
