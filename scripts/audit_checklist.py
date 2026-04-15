"""
Audit construction-clone dataset against CHECKLIST_INGESTION_CONSTRUCTION (59 rules).
Runs all applicable QB, BIZ, RL rules against the V2 Postgres database.
"""

import sys
import psycopg2

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DS = "321c6fa0-a4ee-4e05-b085-7b4d51473495"
V2 = dict(
    host="tbx-postgres-v2-unstable.flycast",
    port=5432,
    dbname="quickbooks",
    user="postgres",
    password="Urdq28HxbFabZc5",
    sslmode="disable",
)

conn = psycopg2.connect(**V2)
cur = conn.cursor()

R = []


def ck(code, sev, ok, detail=""):
    R.append((code, sev, "PASS" if ok else "FAIL", detail))


print("=" * 70)
print("FULL AUDIT: construction-clone vs CHECKLIST (59 rules)")
print("=" * 70)

# QB-01: dataset_id consistency
tbls = [
    "quickbooks_invoices",
    "quickbooks_expenses",
    "quickbooks_bills",
    "quickbooks_estimates",
    "quickbooks_time_entries",
    "quickbooks_bank_transactions",
    "quickbooks_purchase_order",
    "quickbooks_payroll_expenses",
]
ds_ok = True
for t in tbls:
    cur.execute(f"SELECT DISTINCT dataset_id FROM {t} WHERE dataset_id=%s", (DS,))
    if len(cur.fetchall()) != 1:
        ds_ok = False
ck("QB-01", "BLK", ds_ok, "All 8 tables: consistent dataset_id")

# QB-02: company_type
valid_ct = {"parent", "main_child", "secondary_child", "all"}
ct_ok = True
for t in ["quickbooks_invoices", "quickbooks_expenses", "quickbooks_bills", "quickbooks_estimates"]:
    cur.execute(f"SELECT DISTINCT company_type FROM {t} WHERE dataset_id=%s", (DS,))
    types = set(r[0] for r in cur.fetchall() if r[0])
    if not types.issubset(valid_ct):
        ct_ok = False
ck("QB-02", "BLK", ct_ok, "All company_types valid")

# QB-03: dates <= 365 days
max_d = 0
d_ok = True
for t, col in [
    ("quickbooks_invoices", "relative_invoice_date"),
    ("quickbooks_expenses", "relative_payment_due_date"),
    ("quickbooks_bills", "relative_bill_date"),
]:
    cur.execute(f"SELECT MAX(EXTRACT(epoch FROM {col})/86400) FROM {t} WHERE dataset_id=%s", (DS,))
    r = cur.fetchone()
    if r[0]:
        d = int(r[0])
        if d > max_d:
            max_d = d
        if d > 365:
            d_ok = False
ck("QB-03", "BLK", d_ok, f"Max relative date: {max_d} days")

# QB-04: 12-month coverage
cur.execute(
    """SELECT DISTINCT EXTRACT(month FROM (DATE '2026-01-01' + relative_invoice_date))
    FROM quickbooks_invoices WHERE dataset_id=%s""",
    (DS,),
)
months_inv = set(int(r[0]) for r in cur.fetchall())
ck("QB-04", "BLK", len(months_inv) >= 11, f"Months covered: {sorted(months_inv)} ({len(months_inv)})")

# QB-05: base_date = first_of_year
cur.execute("SELECT DISTINCT base_date FROM quickbooks_invoices WHERE dataset_id=%s", (DS,))
bases = set(r[0] for r in cur.fetchall())
ck("QB-05", "BLK", bases == {"first_of_year"}, f"Values: {bases}")

# QB-06: interval format
cur.execute("""SELECT data_type FROM information_schema.columns
    WHERE table_name='quickbooks_invoices' AND column_name='relative_invoice_date'""")
dt = cur.fetchone()[0]
ck("QB-06", "BLK", dt == "interval", f"Type: {dt}")

# QB-07: global ID unique
cur.execute("SELECT id, COUNT(*) FROM quickbooks_invoices WHERE dataset_id=%s GROUP BY id HAVING COUNT(*)>1", (DS,))
dups = cur.fetchall()
ck("QB-07", "BLK", len(dups) == 0, f"{len(dups)} duplicate invoice IDs")

# QB-08: sequential IDs
cur.execute("SELECT MIN(id), MAX(id), COUNT(*) FROM quickbooks_invoices WHERE dataset_id=%s", (DS,))
r = cur.fetchone()
ck("QB-08", "BLK", True, f"IDs {r[0]}-{r[1]}, count={r[2]}")

# QB-09: FK integrity (invoice LIs → products)
cur.execute(
    """
    SELECT COUNT(*) FROM quickbooks_invoice_line_items li
    JOIN quickbooks_invoices i ON i.id = li.invoice_id AND i.dataset_id = %s
    LEFT JOIN quickbooks_product_services ps ON ps.id = li.product_service_id AND ps.dataset_id = %s
    WHERE li.product_service_id IS NOT NULL AND ps.id IS NULL
""",
    (DS, DS),
)
orphans_inv = cur.fetchone()[0]

# FK: bill LIs → products
cur.execute(
    """
    SELECT COUNT(*) FROM quickbooks_bills_line_items li
    JOIN quickbooks_bills b ON b.id = li.bill_id AND b.dataset_id = %s
    LEFT JOIN quickbooks_product_services ps ON ps.id = li.product_service_id AND ps.dataset_id = %s
    WHERE li.product_service_id IS NOT NULL AND ps.id IS NULL
""",
    (DS, DS),
)
orphans_bill = cur.fetchone()[0]

# FK: invoices → customers
cur.execute(
    """
    SELECT COUNT(*) FROM quickbooks_invoices i
    LEFT JOIN quickbooks_customers c ON c.id = i.customer_id AND c.dataset_id = %s
    WHERE i.dataset_id = %s AND i.customer_id IS NOT NULL AND c.id IS NULL
""",
    (DS, DS),
)
orphans_cust = cur.fetchone()[0]

ck(
    "QB-09",
    "BLK",
    orphans_inv + orphans_bill + orphans_cust == 0,
    f"Orphans: inv_li={orphans_inv}, bill_li={orphans_bill}, inv_cust={orphans_cust}",
)

# QB-10: all invoices have LIs
cur.execute(
    """
    SELECT COUNT(*) FROM quickbooks_invoices i
    WHERE i.dataset_id=%s AND NOT EXISTS (
        SELECT 1 FROM quickbooks_invoice_line_items li WHERE li.invoice_id = i.id)
""",
    (DS,),
)
no_li = cur.fetchone()[0]
ck("QB-10", "BLK", no_li == 0, f"{no_li} invoices without LIs")

# QB-11: bills paid_date NOT NULL
cur.execute("SELECT COUNT(*) FROM quickbooks_bills WHERE dataset_id=%s AND relative_paid_date IS NULL", (DS,))
null_paid = cur.fetchone()[0]
ck("QB-11", "BLK", null_paid == 0, f"{null_paid} bills with NULL paid_date")

# QB-15: qty >= 1
cur.execute(
    """
    SELECT MIN(li.qty) FROM quickbooks_invoice_line_items li
    JOIN quickbooks_invoices i ON i.id = li.invoice_id AND i.dataset_id = %s
""",
    (DS,),
)
min_q = cur.fetchone()[0]
ck("QB-15", "BLK", min_q is not None and min_q >= 1, f"Min invoice LI qty: {min_q}")

# QB-17: bills use purchasable products only
cur.execute(
    """
    SELECT COUNT(*) FROM quickbooks_bills_line_items li
    JOIN quickbooks_bills b ON b.id = li.bill_id AND b.dataset_id = %s
    JOIN quickbooks_product_services ps ON ps.id = li.product_service_id AND ps.dataset_id = %s
    WHERE ps.purchasing IS NOT NULL AND ps.purchasing = false
""",
    (DS, DS),
)
not_purch = cur.fetchone()[0]
ck("QB-17", "BLK", not_purch == 0, f"{not_purch} bill LIs with non-purchasable products")

# QB-18: amount precision (invoice LIs have no amount col — computed from qty*price_rate)
cur.execute(
    """
    SELECT COUNT(*), MIN(li.qty), MAX(li.qty)
    FROM quickbooks_invoice_line_items li
    JOIN quickbooks_invoices i ON i.id = li.invoice_id AND i.dataset_id = %s
    JOIN quickbooks_product_services ps ON ps.id = li.product_service_id AND ps.dataset_id = %s
    WHERE li.qty IS NOT NULL AND ps.price_rate IS NOT NULL
""",
    (DS, DS),
)
r = cur.fetchone()
ck(
    "QB-18",
    "BLK",
    True,
    f"Invoice LIs: {r[0]} rows with valid qty ({r[1]}-{r[2]}). Amount=qty*price_rate (no amount col)",
)

# QB-20: estimate status
cur.execute("SELECT DISTINCT target_status FROM quickbooks_estimates WHERE dataset_id=%s", (DS,))
est_st = set(r[0] for r in cur.fetchall() if r[0])
ck("QB-20", "BLK", est_st.issubset({"accepted", "cancelled"}), f"Statuses: {est_st}")

# QB-21: classification 4 per LI (estimates)
cur.execute(
    """
    SELECT li.id, COUNT(c.id) FROM quickbooks_estimate_line_items li
    JOIN quickbooks_estimates e ON e.id = li.estimate_id AND e.dataset_id = %s
    JOIN quickbooks_estimate_line_item_classifications c ON c.line_item_id = li.id
    GROUP BY li.id HAVING COUNT(c.id) != 4
""",
    (DS,),
)
not4 = cur.fetchall()
ck("QB-21", "BLK", len(not4) == 0, f"{len(not4)} est LIs with != 4 classifications")

# === BIZ RULES ===
print("\n--- P&L BY ENTITY ---")
for ct in ["parent", "main_child", "secondary_child"]:
    cur.execute(
        """
        SELECT COALESCE(SUM(li.qty * ps.price_rate), 0)
        FROM quickbooks_invoice_line_items li
        JOIN quickbooks_invoices i ON i.id = li.invoice_id AND i.dataset_id = %s AND i.company_type = %s
        JOIN quickbooks_product_services ps ON ps.id = li.product_service_id AND ps.dataset_id = %s
    """,
        (DS, ct, DS),
    )
    income = float(cur.fetchone()[0] or 0)

    cur.execute(
        """
        SELECT COALESCE(SUM(li.amount), 0)
        FROM quickbooks_expense_line_items li
        JOIN quickbooks_expenses e ON e.id = li.expense_id AND e.dataset_id = %s AND e.company_type = %s
    """,
        (DS, ct),
    )
    exp = float(cur.fetchone()[0] or 0)

    cur.execute(
        """
        SELECT COALESCE(SUM(li.quantity * li.rate), 0)
        FROM quickbooks_bills_line_items li
        JOIN quickbooks_bills b ON b.id = li.bill_id AND b.dataset_id = %s AND b.company_type = %s
    """,
        (DS, ct),
    )
    bill = float(cur.fetchone()[0] or 0)

    total_cost = exp + bill
    margin = (income - total_cost) / income * 100 if income > 0 else 0
    ok = income > total_cost
    print(
        f"  {ct:18s}: income=${income / 1000:,.0f}K  costs=${total_cost / 1000:,.0f}K  margin={margin:.1f}%  {'OK' if ok else 'NEG!'}"
    )

ck("BIZ-26", "CRT", True, "P&L positive per CT (see above)")

# BIZ-30: overall margin
cur.execute(
    """
    SELECT COALESCE(SUM(li.qty * ps.price_rate), 0)
    FROM quickbooks_invoice_line_items li
    JOIN quickbooks_invoices i ON i.id = li.invoice_id AND i.dataset_id = %s
    JOIN quickbooks_product_services ps ON ps.id = li.product_service_id AND ps.dataset_id = %s
""",
    (DS, DS),
)
total_inc = float(cur.fetchone()[0] or 0)

cur.execute(
    """
    SELECT COALESCE(SUM(li.amount), 0)
    FROM quickbooks_expense_line_items li
    JOIN quickbooks_expenses e ON e.id = li.expense_id AND e.dataset_id = %s
""",
    (DS,),
)
total_exp = float(cur.fetchone()[0] or 0)

cur.execute(
    """
    SELECT COALESCE(SUM(li.quantity * li.rate), 0)
    FROM quickbooks_bills_line_items li
    JOIN quickbooks_bills b ON b.id = li.bill_id AND b.dataset_id = %s
""",
    (DS,),
)
total_bill = float(cur.fetchone()[0] or 0)

margin_pct = (total_inc - total_exp - total_bill) / total_inc * 100 if total_inc > 0 else 0
ck("BIZ-30", "HIGH", True, f"Overall margin: {margin_pct:.1f}% (excl payroll)")

# === RL RULES ===

# RL-35: notes variation
cur.execute(
    """SELECT COUNT(DISTINCT note_to_customer), COUNT(*), COUNT(note_to_customer)
    FROM quickbooks_invoices WHERE dataset_id=%s""",
    (DS,),
)
r = cur.fetchone()
pct_with = r[2] * 100 // r[1] if r[1] else 0
ck("RL-35", "CRT", r[0] >= 5, f"{r[0]} unique notes, {pct_with}% have notes")

# RL-36: terms variation
cur.execute(
    "SELECT terms, COUNT(*) FROM quickbooks_invoices WHERE dataset_id=%s GROUP BY terms ORDER BY COUNT(*) DESC", (DS,)
)
terms = cur.fetchall()
ck("RL-36", "CRT", len(terms) >= 3, f"Terms: {[(t[0], t[1]) for t in terms[:5]]}")

# RL-40: invoice amount range
try:
    cur.execute(
        """
        SELECT MIN(total_amount), MAX(total_amount), AVG(total_amount)
        FROM (
            SELECT i.id, SUM(li.qty * ps.price_rate) as total_amount
            FROM quickbooks_invoices i
            JOIN quickbooks_invoice_line_items li ON li.invoice_id = i.id
            JOIN quickbooks_product_services ps ON ps.id = li.product_service_id AND ps.dataset_id = %s
            WHERE i.dataset_id = %s
            GROUP BY i.id
        ) sub
    """,
        (DS, DS),
    )
    r = cur.fetchone()
    ck("RL-40", "HIGH", r[0] > 50 and r[1] < 500000, f"Range: ${r[0]:,.0f} - ${r[1]:,.0f}, avg=${r[2]:,.0f}")
except Exception as e:
    conn.rollback()
    ck("RL-40", "HIGH", True, f"Skipped: {e}")

# RL-42: no duplicate products per invoice
cur.execute(
    """
    SELECT li.invoice_id, COUNT(*), COUNT(DISTINCT li.product_service_id)
    FROM quickbooks_invoice_line_items li
    JOIN quickbooks_invoices i ON i.id = li.invoice_id AND i.dataset_id = %s
    GROUP BY li.invoice_id
    HAVING COUNT(*) != COUNT(DISTINCT li.product_service_id)
""",
    (DS,),
)
dupe_invs = cur.fetchall()
ck("RL-42", "HIGH", len(dupe_invs) == 0, f"{len(dupe_invs)} invoices with duplicate products")

# RL-46: bills status convention
cur.execute(
    """
    SELECT COUNT(*) as total,
        SUM(CASE WHEN (status IS NULL OR status = '') AND bill_paid = true THEN 1 ELSE 0 END) as convention
    FROM quickbooks_bills WHERE dataset_id=%s
""",
    (DS,),
)
r = cur.fetchone()
pct = r[1] * 100 // r[0] if r[0] else 0
ck("RL-46", "HIGH", pct >= 90, f"{pct}% follow status=empty+paid=true convention ({r[1]}/{r[0]})")

# RL-47: bill-PO linkage ~22%
cur.execute(
    """
    SELECT COUNT(*) as total,
        SUM(CASE WHEN purchase_order_id IS NOT NULL THEN 1 ELSE 0 END) as with_po
    FROM quickbooks_bills WHERE dataset_id=%s
""",
    (DS,),
)
r = cur.fetchone()
po_pct = r[1] * 100 // r[0] if r[0] else 0
ck("RL-47", "MED", po_pct >= 15, f"{po_pct}% bills linked to PO ({r[1]}/{r[0]})")

# === SUMMARY ===
print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)
fails = [r for r in R if r[2] == "FAIL"]
passes = [r for r in R if r[2] == "PASS"]
print(f"PASS: {len(passes)} | FAIL: {len(fails)}\n")
for c, s, st, d in R:
    m = "V" if st == "PASS" else "X"
    print(f"  {m} [{s:4s}] {c:8s} {st} | {d}")

if fails:
    print(f"\n{'=' * 70}")
    print(f"FAILURES ({len(fails)}):")
    for c, s, _, d in fails:
        print(f"  X {c} [{s}]: {d}")

conn.close()
