import sqlite3
import csv
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

DATASET_ID = '321c6fa0-a4ee-4e05-b085-7b4d51473495'
DB_PATH = r'C:\Users\adm_r\Clients\intuit-boom\data\qbo_database_part1.db'

# Starting IDs
BILL_START_ID = 105
INVOICE_START_ID = 2460
BILL_LINE_ITEM_START_ID = 1  # Need to check this

# Input files
BILLS_FILE = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_BILLS.csv'
INVOICES_FILE = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_INVOICES.csv'

# Output files
OUTPUT_BILLS = r'C:\Users\adm_r\Downloads\INGESTION_BILLS.csv'
OUTPUT_INVOICES = r'C:\Users\adm_r\Downloads\INGESTION_INVOICES.csv'

def get_vendor_mapping():
    """Get complete vendor name -> id mapping"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, display_name FROM vendors WHERE dataset_id = ?', (DATASET_ID,))
    mapping = {}
    for row in cursor.fetchall():
        if row[1]:
            mapping[row[1].lower().strip()] = row[0]
        if row[2]:
            mapping[row[2].lower().strip()] = row[0]
    conn.close()

    # Add new vendors (IDs 34-53)
    new_vendors = [
        (34, 'Abdi Structural Engineering'),
        (35, 'Al-Farsi Security Services'),
        (36, 'Andersen Lars'),
        (37, 'Blueshield'),
        (38, 'Daniel Green'),
        (39, 'Elite Contracting'),
        (40, 'HVAC Supply Store'),
        (41, 'Hassan Ahmed'),
        (42, 'Home Depot'),
        (43, 'John'),
        (44, 'KeyStone Canopy (IC Vendor)'),
        (45, 'KeyStone Ecocraft (IC Vendor)'),
        (46, 'Keystone Construction (Par.) (IC Vendor)'),
        (47, 'Keystone Construction (Par.) (IC Vendor) ( 356 )'),
        (48, 'Keystone Terra (Ch.) (IC Vendor)'),
        (49, 'Pakistani Insurance'),
        (50, 'Safety Equipment Inc.'),
        (51, 'Terzi'),
        (52, 'dougherty'),
        (53, 'samantha'),
    ]
    for vid, name in new_vendors:
        mapping[name.lower().strip()] = vid

    return mapping

def get_customer_mapping():
    """Get complete customer name -> id mapping"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, customer_display_name, first_name, last_name FROM customers WHERE dataset_id = ?', (DATASET_ID,))
    mapping = {}
    for row in cursor.fetchall():
        if row[1]:
            mapping[row[1].lower().strip()] = row[0]
        if row[2] and row[3]:
            full_name = f"{row[2]} {row[3]}".lower().strip()
            mapping[full_name] = row[0]
    conn.close()

    # Add new customers (IDs 51-75)
    new_customers = [
        (51, 'Alan Brown'),
        (52, 'Austin Enterprise'),
        (53, 'Azure Pines - Playground Construction'),
        (54, 'Azure Pines - Playground Construction 2022'),
        (55, 'BMH Landscaping 2025'),
        (56, 'Casa Bonita'),
        (57, 'Construction- Test Delete'),
        (58, 'Donald Duck'),
        (59, 'GaleGuardian - Turbine Installation'),
        (60, 'Government  Agency'),
        (61, 'Intuit Dome'),
        (62, 'KeyStone Canopy (IC Customer)'),
        (63, 'KeyStone Ironcraft (IC Customer) ( 358 )'),
        (64, 'KeyStone Volt (IC Customer)'),
        (65, 'Keystone Construction (Par.) (IC Customer) ( 354 )'),
        (66, 'La Hacienda Event Center'),
        (67, 'Leap Labs - Solar Array Installation'),
        (68, 'Lot Clearing'),
        (69, 'Maintenance'),
        (70, 'Meredith Walker'),
        (71, "TidalWave - Farmer's Market (Lot Build)"),
        (72, "TidalWave - Farmer's Market (Lot Build) 2024"),
        (73, 'Trent Kennedy'),
        (74, 'Walker Draperies - Jacqueline Brinkerhoff'),
        (75, 'Wezlee Norriz'),
    ]
    for cid, name in new_customers:
        mapping[name.lower().strip()] = cid

    return mapping

def get_company_type_map():
    return {
        'Keystone Construction (Par)': 'parent',
        'Keystone Construction (Par.)': 'parent',
        'Keystone BlueCraft': 'main_child',
        'Keystone Terra (Ch.)': 'secondary_child',
        'KeyStone Volt': 'secondary_child',
        'KeyStone Stonecraft': 'secondary_child',
        'KeyStone Ironcraft': 'secondary_child',
        'KeyStone Ecocraft': 'secondary_child',
        'KeyStone Canopy': 'secondary_child',
    }

def transform_bills():
    """Transform extracted bills to ingestion format"""
    vendor_map = get_vendor_mapping()
    company_type_map = get_company_type_map()

    bills = []
    unmapped_vendors = set()
    current_id = BILL_START_ID

    with open(BILLS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vendor_name = row['vendor'].strip()
            vendor_id = vendor_map.get(vendor_name.lower().strip())

            if not vendor_id:
                unmapped_vendors.add(vendor_name)
                continue

            company = row['company']
            company_type = company_type_map.get(company, 'secondary_child')

            # Parse dates
            due_date = row['due_date']  # Already in YYYY-MM-DD format

            bill = {
                'id': current_id,
                'vendor_id': vendor_id,
                'terms': 'Net 30',
                'relative_bill_date': due_date,
                'relative_due_date': due_date,
                'bill_no': current_id,
                'tag_id': '',
                'memo': '',
                'image_url': '',
                'base_date': '2024-01-01',
                'bill_paid': 0,
                'status': 'open',
                'bank_transaction_description': '',
                'purchase_order_id': '',
                'relative_paid_date': '',
                'dataset_id': DATASET_ID,
                'company_type': company_type,
                'bank_transaction_account_id': '',
                # Extra fields for reference
                '_vendor_name': vendor_name,
                '_amount': row['amount'],
                '_company': company,
            }
            bills.append(bill)
            current_id += 1

    # Write output
    fieldnames = ['id', 'vendor_id', 'terms', 'relative_bill_date', 'relative_due_date',
                  'bill_no', 'tag_id', 'memo', 'image_url', 'base_date', 'bill_paid',
                  'status', 'bank_transaction_description', 'purchase_order_id',
                  'relative_paid_date', 'dataset_id', 'company_type', 'bank_transaction_account_id']

    with open(OUTPUT_BILLS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(bills)

    print(f"✅ BILLS: {OUTPUT_BILLS}")
    print(f"   Records: {len(bills)}")
    print(f"   ID range: {BILL_START_ID} - {current_id - 1}")

    if unmapped_vendors:
        print(f"   ⚠️  Unmapped vendors ({len(unmapped_vendors)}):")
        for v in sorted(unmapped_vendors):
            print(f"      - {v}")

    return bills

def transform_invoices():
    """Transform extracted invoices to ingestion format"""
    customer_map = get_customer_mapping()
    company_type_map = get_company_type_map()

    invoices = []
    unmapped_customers = set()
    current_id = INVOICE_START_ID

    with open(INVOICES_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customer_name = row['customer'].strip()
            customer_id = customer_map.get(customer_name.lower().strip())

            if not customer_id:
                unmapped_customers.add(customer_name)
                continue

            company = row['company']
            company_type = company_type_map.get(company, 'secondary_child')

            # Parse dates
            due_date = row['due_date']  # Already in YYYY-MM-DD format

            invoice = {
                'id': current_id,
                'customer_id': customer_id,
                'project_id': '',
                'online_payment_card': 1,
                'online_payment_banktransfer': 1,
                'terms': 'Net 30',
                'relative_invoice_create_date': due_date,
                'relative_invoice_due_date': due_date,
                'ship_via': '',
                'relative_shipping_create_date': '',
                'tracking_no': '',
                'invoice_no': current_id,
                'store': '',
                'tag_id': '',
                'note_to_customer': '',
                'memo_on_statement': '',
                'attachments': '',
                'base_date': '2024-01-01',
                'relative_invoice_paid_date': '',
                'invoice_template_id': '',
                'viewed_invoice': 0,
                'paid_invoice': 0,
                'relative_invoice_issue_date': due_date,
                'relative_invoice_date': due_date,
                'bank_transaction_description': '',
                'invoice_order': '',
                'dataset_id': DATASET_ID,
                'company_type': company_type,
                'bank_transaction_account_id': '',
                # Extra fields for reference
                '_customer_name': customer_name,
                '_amount': row['amount'],
                '_company': company,
            }
            invoices.append(invoice)
            current_id += 1

    # Write output
    fieldnames = ['id', 'customer_id', 'project_id', 'online_payment_card', 'online_payment_banktransfer',
                  'terms', 'relative_invoice_create_date', 'relative_invoice_due_date', 'ship_via',
                  'relative_shipping_create_date', 'tracking_no', 'invoice_no', 'store', 'tag_id',
                  'note_to_customer', 'memo_on_statement', 'attachments', 'base_date',
                  'relative_invoice_paid_date', 'invoice_template_id', 'viewed_invoice', 'paid_invoice',
                  'relative_invoice_issue_date', 'relative_invoice_date', 'bank_transaction_description',
                  'invoice_order', 'dataset_id', 'company_type', 'bank_transaction_account_id']

    with open(OUTPUT_INVOICES, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(invoices)

    print(f"\n✅ INVOICES: {OUTPUT_INVOICES}")
    print(f"   Records: {len(invoices)}")
    print(f"   ID range: {INVOICE_START_ID} - {current_id - 1}")

    if unmapped_customers:
        print(f"   ⚠️  Unmapped customers ({len(unmapped_customers)}):")
        for c in sorted(unmapped_customers):
            print(f"      - {c}")

    return invoices

def main():
    print("=" * 70)
    print("TRANSFORMING BILLS & INVOICES FOR INGESTION")
    print("=" * 70)
    print(f"\nDataset ID: {DATASET_ID}")
    print(f"Starting IDs: Bills={BILL_START_ID}, Invoices={INVOICE_START_ID}")
    print()

    bills = transform_bills()
    invoices = transform_invoices()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
Files generated in Downloads:
  - INGESTION_BILLS.csv ({len(bills)} records)
  - INGESTION_INVOICES.csv ({len(invoices)} records)
""")

if __name__ == '__main__':
    main()
