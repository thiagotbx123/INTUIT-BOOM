import sqlite3
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

DATASET_ID = '321c6fa0-a4ee-4e05-b085-7b4d51473495'
DB_PATH = r'C:\Users\adm_r\Clients\intuit-boom\data\qbo_database_part1.db'

# Starting IDs (MAX + 1)
VENDOR_START_ID = 34
CUSTOMER_START_ID = 51
BILL_START_ID = 105
INVOICE_START_ID = 2460

# Missing entities to add
MISSING_VENDORS = [
    'Abdi Structural Engineering',
    'Al-Farsi Security Services',
    'Andersen Lars',
    'Blueshield',
    'Daniel Green',
    'Elite Contracting',
    'HVAC Supply Store',
    'Hassan Ahmed',
    'Home Depot',
    'John',
    'KeyStone Canopy (IC Vendor)',
    'KeyStone Ecocraft (IC Vendor)',
    'Keystone Construction (Par.) (IC Vendor)',
    'Keystone Construction (Par.) (IC Vendor) ( 356 )',
    'Keystone Terra (Ch.) (IC Vendor)',
    'Pakistani Insurance',
    'Safety Equipment Inc.',
    'Terzi',
    'dougherty',
    'samantha',
]

MISSING_CUSTOMERS = [
    'Alan Brown',
    'Austin Enterprise',
    'Azure Pines - Playground Construction',
    'Azure Pines - Playground Construction 2022',
    'BMH Landscaping 2025',
    'Casa Bonita',
    'Construction- Test Delete',
    'Donald Duck',
    'GaleGuardian - Turbine Installation',
    'Government  Agency',
    'Intuit Dome',
    'KeyStone Canopy (IC Customer)',
    'KeyStone Ironcraft (IC Customer) ( 358 )',
    'KeyStone Volt (IC Customer)',
    'Keystone Construction (Par.) (IC Customer) ( 354 )',
    'La Hacienda Event Center',
    'Leap Labs - Solar Array Installation',
    'Lot Clearing',
    'Maintenance',
    'Meredith Walker',
    'TidalWave - Farmer\'s Market (Lot Build)',
    'TidalWave - Farmer\'s Market (Lot Build) 2024',
    'Trent Kennedy',
    'Walker Draperies - Jacqueline Brinkerhoff',
    'Wezlee Norriz',
]

def is_ic_vendor(name):
    return '(IC Vendor)' in name

def is_ic_customer(name):
    return '(IC Customer)' in name

def generate_vendors_csv():
    """Generate vendors ingestion CSV with sequential IDs"""
    output_path = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\INGESTION_VENDORS_NEW.csv'

    vendors = []
    current_id = VENDOR_START_ID

    for name in MISSING_VENDORS:
        vendor = {
            'id': current_id,
            'name': name,
            'display_name': name,
            'contact_first_name': '',
            'contact_last_name': '',
            'contact_email': '',
            'contact_phone': '',
            'address': '',
            'city': '',
            'state': '',
            'zipcode': '',
            'terms': 'Net 30',
            'dataset_id': DATASET_ID,
            'company_type': 'all',
            'is_ic': is_ic_vendor(name)
        }
        vendors.append(vendor)
        current_id += 1

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'name', 'display_name', 'contact_first_name', 'contact_last_name',
                      'contact_email', 'contact_phone', 'address', 'city', 'state', 'zipcode',
                      'terms', 'dataset_id', 'company_type', 'is_ic']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(vendors)

    print(f"✅ Generated: {output_path}")
    print(f"   Records: {len(vendors)}")
    print(f"   ID range: {VENDOR_START_ID} - {current_id - 1}")

    return {v['name'].lower(): v['id'] for v in vendors}

def generate_customers_csv():
    """Generate customers ingestion CSV with sequential IDs"""
    output_path = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\INGESTION_CUSTOMERS_NEW.csv'

    customers = []
    current_id = CUSTOMER_START_ID

    for name in MISSING_CUSTOMERS:
        # Parse name into first/last if possible
        parts = name.split()
        if len(parts) >= 2 and not is_ic_customer(name) and '-' not in name:
            first_name = parts[0]
            last_name = ' '.join(parts[1:])
        else:
            first_name = name
            last_name = ''

        customer = {
            'id': current_id,
            'customer_display_name': name,
            'first_name': first_name,
            'last_name': last_name,
            'email': '',
            'phone': '',
            'billing_address': '',
            'city': '',
            'state': '',
            'zip_code': '',
            'country': 'United States',
            'terms': 'Net 30',
            'sub_customer': 0,
            'dataset_id': DATASET_ID,
            'company_type': 'all',
            'is_ic': is_ic_customer(name)
        }
        customers.append(customer)
        current_id += 1

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'customer_display_name', 'first_name', 'last_name', 'email',
                      'phone', 'billing_address', 'city', 'state', 'zip_code', 'country',
                      'terms', 'sub_customer', 'dataset_id', 'company_type', 'is_ic']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(customers)

    print(f"✅ Generated: {output_path}")
    print(f"   Records: {len(customers)}")
    print(f"   ID range: {CUSTOMER_START_ID} - {current_id - 1}")

    return {c['customer_display_name'].lower(): c['id'] for c in customers}

def get_existing_vendor_mapping():
    """Get existing vendor name -> id mapping from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, display_name FROM vendors WHERE dataset_id = ?
    ''', (DATASET_ID,))
    mapping = {}
    for row in cursor.fetchall():
        if row[1]:
            mapping[row[1].lower().strip()] = row[0]
        if row[2]:
            mapping[row[2].lower().strip()] = row[0]
    conn.close()
    return mapping

def get_existing_customer_mapping():
    """Get existing customer name -> id mapping from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, customer_display_name, first_name, last_name FROM customers WHERE dataset_id = ?
    ''', (DATASET_ID,))
    mapping = {}
    for row in cursor.fetchall():
        if row[1]:
            mapping[row[1].lower().strip()] = row[0]
        if row[2] and row[3]:
            full_name = f"{row[2]} {row[3]}".lower().strip()
            mapping[full_name] = row[0]
    conn.close()
    return mapping

def main():
    print("=" * 70)
    print("GENERATING INGESTION CSVs WITH SEQUENTIAL IDs")
    print("=" * 70)
    print(f"\nDataset ID: {DATASET_ID}")
    print(f"\nStarting IDs:")
    print(f"  Vendors: {VENDOR_START_ID}")
    print(f"  Customers: {CUSTOMER_START_ID}")
    print(f"  Bills: {BILL_START_ID}")
    print(f"  Invoices: {INVOICE_START_ID}")

    print("\n" + "-" * 70)
    print("PHASE 1: Master Data")
    print("-" * 70)

    # Generate vendors
    new_vendor_mapping = generate_vendors_csv()

    # Generate customers
    new_customer_mapping = generate_customers_csv()

    # Combine with existing mappings
    print("\n" + "-" * 70)
    print("COMPLETE MAPPINGS (Existing + New)")
    print("-" * 70)

    existing_vendors = get_existing_vendor_mapping()
    existing_customers = get_existing_customer_mapping()

    all_vendors = {**existing_vendors, **new_vendor_mapping}
    all_customers = {**existing_customers, **new_customer_mapping}

    print(f"\nTotal Vendors available: {len(all_vendors)}")
    print(f"Total Customers available: {len(all_customers)}")

    # Save mappings for later use
    mapping_file = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\FK_MAPPINGS.py'
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write(f"# FK Mappings for Bills/Invoices transformation\n")
        f.write(f"# Generated automatically\n\n")
        f.write(f"DATASET_ID = '{DATASET_ID}'\n\n")
        f.write(f"VENDOR_MAPPING = {repr(all_vendors)}\n\n")
        f.write(f"CUSTOMER_MAPPING = {repr(all_customers)}\n\n")
        f.write(f"BILL_START_ID = {BILL_START_ID}\n")
        f.write(f"INVOICE_START_ID = {INVOICE_START_ID}\n")

    print(f"\n✅ Saved FK mappings to: {mapping_file}")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("""
1. Review INGESTION_VENDORS_NEW.csv (20 records, IDs 34-53)
2. Review INGESTION_CUSTOMERS_NEW.csv (25 records, IDs 51-75)
3. Send to Engineering for ingestion
4. After ingestion, run Bills/Invoices transformation
""")

if __name__ == '__main__':
    main()
