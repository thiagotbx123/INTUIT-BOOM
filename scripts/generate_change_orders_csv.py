"""
Generate Change Orders CSVs for construction-clone dataset.

Tables:
  1. quickbooks_change_orders (header) — NO dataset_id column; scoped via project/customer FKs
  2. quickbooks_change_orders_product_and_service_line_item (line items) — qty is INTEGER
  3. quickbooks_change_orders_product_item_dimensions (classification per LI)

Schema (from V2 DB — verified Apr 15 2026):
  change_orders: id, project, customer, estimate, change_order_date(DATE), accepted_date(DATE),
                 service_date(DATE), description, unit_cost, customer_rate, note_to_customer,
                 memo, attachments, base_date(VARCHAR), company_id(INT), company_type(TEXT)
  LIs: id, change_orders (FK), product_service, description, qty(INTEGER), unit_cost,
       mark_up_percent, customer_rate, customer_total
  Dimensions: id, change_orders_product_and_service_line_item (FK), dimensions_account

IMPORTANT — Date handling:
  Unlike invoices/estimates (which use interval columns like 'relative_invoice_date'),
  change_orders uses actual DATE columns ('change_order_date', 'accepted_date', 'service_date').
  BUT the table has a 'base_date' column (varchar), following the same pattern.
  The ingestion pipeline should compute: first_of_year + N days → actual DATE.
  CSV stores the integer number of days for the pipeline to convert.
  If pipeline doesn't support this for DATE columns, engineering ticket needed.

Usage:
  python generate_change_orders_csv.py                # Generate CSVs
  python generate_change_orders_csv.py --insert       # Insert into V2
"""

import sys
import csv
import os
import random
import argparse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATASET_ID = "321c6fa0-a4ee-4e05-b085-7b4d51473495"
OUTPUT_DIR = os.path.expanduser("~/Downloads")

PROJECT_CUSTOMER_MAP = {
    19: 19,  # Azure Pines → Nadia Ahmed
    20: 33,  # GaleGuardian → Amelia Patel
    21: 15,  # Intuit Dome → Priya Patel
    22: 42,  # Leap Labs → Michael Nguyen
    23: 43,  # BMH → Emily Wong
    24: 44,  # TidalWave → Matthew Ahmed
}

PRODUCTS_CONSTRUCTION = [3, 5, 7, 8, 9, 11, 12, 13, 14, 15, 16, 19, 22, 23, 24, 25, 74, 75, 76]

DESCRIPTIONS_CO = [
    "Scope expansion: additional excavation for utility relocation",
    "Material upgrade: switch to high-grade concrete mix",
    "Schedule acceleration: weekend crew for foundation pour",
    "Design revision: updated structural reinforcement plan",
    "Weather delay mitigation: temporary drainage installation",
    "Regulatory compliance: additional environmental testing",
    "Client-requested: extended landscaping and grading",
    "Unforeseen condition: rock removal and disposal",
    "Safety upgrade: enhanced fall protection system",
    "Permit modification: revised drainage plan submittal",
    "Additional scope: retaining wall extension",
    "Change in specification: upgraded electrical conduit",
    "Site access improvement: temporary road construction",
    "Subcontractor substitution: replacement crew mobilization",
    "Quality enhancement: additional soil compaction testing",
]

DESCRIPTIONS_LI = [
    "Additional excavation labor",
    "Premium concrete mix (4000 PSI)",
    "Weekend overtime crew",
    "Structural steel reinforcement",
    "Temporary drainage pump rental",
    "Environmental soil sampling",
    "Extended grading area",
    "Rock removal and hauling",
    "Safety harness system",
    "Drainage plan revision",
    "Retaining wall materials",
    "Electrical conduit upgrade",
    "Gravel for temporary road",
    "Replacement crew mobilization",
    "Compaction testing services",
    "Rebar and tie wire",
    "Formwork rental (extended)",
    "Backfill material",
    "Traffic control signage",
    "Survey stakes and marking",
]

random.seed(2026)


def generate():
    co_rows = []
    li_rows = []
    dim_rows = []

    co_id = 1
    li_id = 1
    dim_id = 1

    entity_cycle = ["parent", "main_child", "secondary_child"]
    entity_idx = 0

    for project_id, customer_id in PROJECT_CUSTOMER_MAP.items():
        num_cos = random.randint(2, 4)
        for i in range(num_cos):
            co_date_days = random.randint(30, 280)
            accepted_offset = random.randint(3, 14)
            service_offset = random.randint(7, 30)

            company_type = entity_cycle[entity_idx % len(entity_cycle)]
            entity_idx += 1

            co_row = {
                "id": co_id,
                "project": project_id,
                "customer": customer_id,
                "estimate": "",
                "change_order_date": co_date_days,
                "accepted_date": co_date_days + accepted_offset,
                "service_date": co_date_days + service_offset,
                "description": random.choice(DESCRIPTIONS_CO),
                "unit_cost": "",
                "customer_rate": "",
                "note_to_customer": f"CO-{co_id:03d}: Approved change order for project scope adjustment",
                "memo": "",
                "attachments": "",
                "base_date": "first_of_year",
                "company_id": "",
                "company_type": company_type,
            }
            co_rows.append(co_row)

            num_lis = random.randint(2, 4)
            co_products_used = set()
            for j in range(num_lis):
                qty = random.randint(1, 50)
                unit_cost = round(random.uniform(50, 2000), 2)
                markup = random.choice([10, 15, 20, 25, 30])
                cust_rate = round(unit_cost * (1 + markup / 100), 2)
                cust_total = round(qty * cust_rate, 2)

                available = [p for p in PRODUCTS_CONSTRUCTION if p not in co_products_used]
                product = random.choice(available)
                co_products_used.add(product)

                li_row = {
                    "id": li_id,
                    "change_orders": co_id,
                    "product_service": product,
                    "description": random.choice(DESCRIPTIONS_LI),
                    "qty": qty,
                    "unit_cost": unit_cost,
                    "mark_up_percent": markup,
                    "customer_rate": cust_rate,
                    "customer_total": cust_total,
                }
                li_rows.append(li_row)

                for cls_id in [
                    random.choice([6, 7, 8]),
                    random.choice([15, 16]),
                    random.choice([17, 18, 19, 20, 21, 22]),
                    random.choice([26, 27, 28]),
                ]:
                    dim_rows.append(
                        {
                            "id": dim_id,
                            "change_orders_product_and_service_line_item": li_id,
                            "dimensions_account": cls_id,
                        }
                    )
                    dim_id += 1

                li_id += 1
            co_id += 1

    return co_rows, li_rows, dim_rows


def write_csvs(co_rows, li_rows, dim_rows):
    co_path = os.path.join(OUTPUT_DIR, "CHANGE_ORDERS.csv")
    li_path = os.path.join(OUTPUT_DIR, "CHANGE_ORDERS_LINE_ITEMS.csv")
    dim_path = os.path.join(OUTPUT_DIR, "CHANGE_ORDERS_DIMENSIONS.csv")

    with open(co_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=co_rows[0].keys())
        w.writeheader()
        w.writerows(co_rows)
    print(f"Wrote {len(co_rows)} change orders → {co_path}")

    with open(li_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=li_rows[0].keys())
        w.writeheader()
        w.writerows(li_rows)
    print(f"Wrote {len(li_rows)} line items → {li_path}")

    with open(dim_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=dim_rows[0].keys())
        w.writeheader()
        w.writerows(dim_rows)
    print(f"Wrote {len(dim_rows)} dimensions → {dim_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--insert", action="store_true", help="Insert CSVs into V2 DB")
    args = parser.parse_args()

    co_rows, li_rows, dim_rows = generate()
    write_csvs(co_rows, li_rows, dim_rows)

    print(f"\nSummary: {len(co_rows)} COs, {len(li_rows)} LIs, {len(dim_rows)} dimensions")
    print(f"Projects covered: {sorted(set(r['project'] for r in co_rows))}")
    print(f"Company types: {sorted(set(r['company_type'] for r in co_rows))}")

    if args.insert:
        print("\n--insert not yet implemented. Use manual INSERT or adapt insert_cashflow_invoices_v2.py pattern.")


if __name__ == "__main__":
    main()
