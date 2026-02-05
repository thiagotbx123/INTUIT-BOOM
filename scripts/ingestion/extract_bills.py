import csv
import sys
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Company type mapping
COMPANY_TYPE_MAP = {
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

def parse_amount(amount_str):
    """Parse amount string to float"""
    if not amount_str:
        return 0.0
    cleaned = amount_str.replace('"', '').replace('$', '').replace(',', '').strip()
    if not cleaned or cleaned == '-':
        return 0.0
    try:
        return float(cleaned)
    except:
        return 0.0

def parse_date(date_str):
    """Parse date string MM/DD/YYYY to YYYY-MM-DD"""
    if not date_str:
        return ''
    try:
        parsed = datetime.strptime(date_str.strip(), '%m/%d/%Y')
        return parsed.strftime('%Y-%m-%d')
    except:
        return date_str

def is_ic_vendor(vendor_name):
    """Check if vendor is an IC vendor"""
    if not vendor_name:
        return False
    ic_patterns = ['(IC Vendor)', 'IC Vendor']
    return any(p in vendor_name for p in ic_patterns)

def main():
    input_file = r'C:\Users\adm_r\Downloads\Consolidated View_Consolidated A_P detail.csv'
    output_bills = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_BILLS.csv'
    output_vendor_credits = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_VENDOR_CREDITS.csv'

    bills = []
    vendor_credits = []
    other_transactions = []

    current_vendor = None

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 8:
                continue

            # Skip header rows
            if 'Vendor' in str(row) and 'Transaction type' in str(row):
                continue
            if 'Consolidated A/P detail' in str(row):
                continue
            if 'All Dates' in str(row):
                continue

            # Check if this is a vendor header row (vendor name in first col, rest empty)
            first_col = row[0].strip() if row[0] else ''
            second_col = row[1].strip() if len(row) > 1 and row[1] else ''

            # Vendor header: has text in first col, empty or minimal in others
            if first_col and not second_col and first_col not in ['TOTAL', 'Eliminations']:
                if not first_col.startswith('Total for'):
                    current_vendor = first_col
                continue

            # Skip total rows
            if first_col.startswith('Total for') or first_col == 'TOTAL':
                continue
            if second_col == 'TOTAL' or second_col == 'Eliminations':
                continue

            # Skip empty rows
            if not any(row):
                continue

            # Parse transaction row
            # Structure: empty, Vendor, Transaction type, Company, Num, Due date, Past due, Amount, Open balance
            vendor = row[1].strip() if len(row) > 1 else ''
            txn_type = row[2].strip() if len(row) > 2 else ''
            company = row[3].strip() if len(row) > 3 else ''
            bill_num = row[4].strip() if len(row) > 4 else ''
            due_date = row[5].strip() if len(row) > 5 else ''
            past_due = row[6].strip() if len(row) > 6 else ''
            amount = row[7].strip() if len(row) > 7 else ''
            open_balance = row[8].strip() if len(row) > 8 else ''

            if not vendor or not txn_type:
                continue

            # Get company type
            company_type = COMPANY_TYPE_MAP.get(company, 'unknown')

            # Check if IC
            is_ic = is_ic_vendor(vendor)

            record = {
                'vendor': vendor,
                'transaction_type': txn_type,
                'company': company,
                'company_type': company_type,
                'bill_number': bill_num,
                'due_date': parse_date(due_date),
                'due_date_original': due_date,
                'past_due_days': past_due,
                'amount': parse_amount(amount),
                'open_balance': parse_amount(open_balance),
                'is_ic': is_ic
            }

            if txn_type == 'Bill':
                bills.append(record)
            elif txn_type == 'Vendor Credit':
                vendor_credits.append(record)
            else:
                other_transactions.append(record)

    # Write Bills CSV
    with open(output_bills, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['vendor', 'transaction_type', 'company', 'company_type', 'bill_number',
                      'due_date', 'due_date_original', 'past_due_days', 'amount', 'open_balance', 'is_ic']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bills)

    # Write Vendor Credits CSV
    with open(output_vendor_credits, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['vendor', 'transaction_type', 'company', 'company_type', 'bill_number',
                      'due_date', 'due_date_original', 'past_due_days', 'amount', 'open_balance', 'is_ic']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(vendor_credits)

    # Print summary
    print("=" * 60)
    print("BILLS EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"\nTotal Bills: {len(bills)}")
    print(f"Total Vendor Credits: {len(vendor_credits)}")
    print(f"Other Transactions: {len(other_transactions)}")

    # Bills by company
    print("\n--- Bills by Company ---")
    from collections import Counter
    company_counts = Counter(b['company'] for b in bills)
    for company, count in sorted(company_counts.items(), key=lambda x: -x[1]):
        print(f"  {company}: {count}")

    # Bills IC vs Regular
    ic_bills = [b for b in bills if b['is_ic']]
    regular_bills = [b for b in bills if not b['is_ic']]
    print(f"\n--- IC vs Regular ---")
    print(f"  Regular Bills: {len(regular_bills)}")
    print(f"  IC Bills: {len(ic_bills)}")

    # Total amounts
    total_amount = sum(b['amount'] for b in bills)
    total_open = sum(b['open_balance'] for b in bills)
    print(f"\n--- Totals ---")
    print(f"  Total Amount: ${total_amount:,.2f}")
    print(f"  Total Open Balance: ${total_open:,.2f}")

    # IC Vendors found
    ic_vendors = set(b['vendor'] for b in ic_bills)
    if ic_vendors:
        print(f"\n--- IC Vendors ({len(ic_vendors)}) ---")
        for v in sorted(ic_vendors):
            print(f"  - {v}")

    # Top vendors by amount
    vendor_amounts = {}
    for b in bills:
        vendor_amounts[b['vendor']] = vendor_amounts.get(b['vendor'], 0) + b['amount']

    print(f"\n--- Top 10 Vendors by Amount ---")
    for vendor, amount in sorted(vendor_amounts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {vendor}: ${amount:,.2f}")

    print(f"\n--- Output Files ---")
    print(f"  Bills: {output_bills}")
    print(f"  Vendor Credits: {output_vendor_credits}")

    if other_transactions:
        print(f"\n--- Other Transactions (not Bills/Credits) ---")
        for t in other_transactions:
            print(f"  {t['transaction_type']}: {t['vendor']} - ${t['amount']:,.2f}")

if __name__ == '__main__':
    main()
