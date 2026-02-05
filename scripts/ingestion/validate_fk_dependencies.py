import sqlite3
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Database connection
DB_PATH = r'C:\Users\adm_r\Clients\intuit-boom\data\qbo_database_part1.db'
DATASET_ID = '321c6fa0-a4ee-4e05-b085-7b4d51473495'

# Extracted files
BILLS_FILE = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_BILLS.csv'
INVOICES_FILE = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_INVOICES.csv'

def get_dataset_vendors():
    """Get all vendor names from the dataset"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, display_name
        FROM vendors
        WHERE dataset_id = ?
    ''', (DATASET_ID,))
    vendors = {}
    for row in cursor.fetchall():
        vendors[row[1].lower().strip() if row[1] else ''] = row[0]
        if row[2]:
            vendors[row[2].lower().strip()] = row[0]
    conn.close()
    return vendors

def get_dataset_customers():
    """Get all customer names from the dataset"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, customer_display_name, first_name, last_name
        FROM customers
        WHERE dataset_id = ?
    ''', (DATASET_ID,))
    customers = {}
    for row in cursor.fetchall():
        if row[1]:
            customers[row[1].lower().strip()] = row[0]
        # Also try first_name + last_name
        if row[2] and row[3]:
            full_name = f"{row[2]} {row[3]}".lower().strip()
            customers[full_name] = row[0]
    conn.close()
    return customers

def get_extracted_bill_vendors():
    """Get unique vendor names from extracted bills"""
    vendors = set()
    with open(BILLS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['vendor']:
                vendors.add(row['vendor'].strip())
    return vendors

def get_extracted_invoice_customers():
    """Get unique customer names from extracted invoices"""
    customers = set()
    with open(INVOICES_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['customer']:
                customers.add(row['customer'].strip())
    return customers

def main():
    print("=" * 70)
    print("FK DEPENDENCY VALIDATION")
    print("=" * 70)

    # Get dataset entities
    dataset_vendors = get_dataset_vendors()
    dataset_customers = get_dataset_customers()

    print(f"\nDataset Vendors: {len(dataset_vendors)} (unique names)")
    print(f"Dataset Customers: {len(dataset_customers)} (unique names)")

    # Get extracted entities
    bill_vendors = get_extracted_bill_vendors()
    invoice_customers = get_extracted_invoice_customers()

    print(f"\nExtracted Bill Vendors: {len(bill_vendors)}")
    print(f"Extracted Invoice Customers: {len(invoice_customers)}")

    # Find missing vendors
    print("\n" + "=" * 70)
    print("VENDORS: Missing from Dataset")
    print("=" * 70)
    missing_vendors = []
    matched_vendors = []
    for vendor in sorted(bill_vendors):
        vendor_lower = vendor.lower().strip()
        if vendor_lower in dataset_vendors:
            matched_vendors.append((vendor, dataset_vendors[vendor_lower]))
        else:
            missing_vendors.append(vendor)

    print(f"\n✅ Matched: {len(matched_vendors)}")
    print(f"❌ Missing: {len(missing_vendors)}")

    if missing_vendors:
        print("\nMissing Vendors (need to add to dataset):")
        for v in sorted(missing_vendors):
            print(f"  - {v}")

    # Find missing customers
    print("\n" + "=" * 70)
    print("CUSTOMERS: Missing from Dataset")
    print("=" * 70)
    missing_customers = []
    matched_customers = []
    for customer in sorted(invoice_customers):
        customer_lower = customer.lower().strip()
        if customer_lower in dataset_customers:
            matched_customers.append((customer, dataset_customers[customer_lower]))
        else:
            missing_customers.append(customer)

    print(f"\n✅ Matched: {len(matched_customers)}")
    print(f"❌ Missing: {len(missing_customers)}")

    if missing_customers:
        print("\nMissing Customers (need to add to dataset):")
        for c in sorted(missing_customers):
            print(f"  - {c}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
Bills:
  - Total unique vendors in bills: {len(bill_vendors)}
  - Vendors already in dataset: {len(matched_vendors)}
  - Vendors MISSING (must add first): {len(missing_vendors)}

Invoices:
  - Total unique customers in invoices: {len(invoice_customers)}
  - Customers already in dataset: {len(matched_customers)}
  - Customers MISSING (must add first): {len(missing_customers)}
""")

    if missing_vendors or missing_customers:
        print("⚠️  ACTION REQUIRED: Add missing Vendors/Customers BEFORE Bills/Invoices!")
    else:
        print("✅ All FK dependencies satisfied! Ready to transform Bills/Invoices.")

if __name__ == '__main__':
    main()
