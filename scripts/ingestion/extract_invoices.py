import csv
import sys
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

def is_ic_customer(customer_name):
    """Check if customer is an IC customer"""
    if not customer_name:
        return False
    ic_patterns = ['(IC Customer)', 'IC Customer']
    return any(p in customer_name for p in ic_patterns)

def main():
    input_file = r'C:\Users\adm_r\Downloads\Consolidated View_Consolidated A_R detail.csv'
    output_invoices = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_INVOICES.csv'
    output_credits = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_CUSTOMER_CREDITS.csv'

    invoices = []
    credits = []
    other_transactions = []

    current_customer = None
    parent_customer = None  # For sub-customers

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 8:
                continue

            # Skip header rows
            if 'Customer' in str(row) and 'Transaction type' in str(row):
                continue
            if 'Consolidated A/R detail' in str(row):
                continue
            if 'All Dates' in str(row):
                continue

            first_col = row[0].strip() if row[0] else ''
            second_col = row[1].strip() if len(row) > 1 and row[1] else ''

            # Customer header: has text in first col, empty or minimal in others
            if first_col and not second_col and first_col not in ['TOTAL', 'Eliminations']:
                if not first_col.startswith('Total for'):
                    # Check if this might be a sub-customer (indented under parent)
                    current_customer = first_col
                    # If it's a known project pattern, keep track of parent
                    if any(x in first_col for x in [' - ', 'Installation', 'Landscaping', 'Market', 'Playground', 'Array', 'Dome']):
                        # This is likely a sub-customer/project
                        pass
                    else:
                        parent_customer = first_col
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
            # Structure: empty, Customer, Transaction type, Company, Num, Due date, Past due, Amount, Open balance
            customer = row[1].strip() if len(row) > 1 else ''
            txn_type = row[2].strip() if len(row) > 2 else ''
            company = row[3].strip() if len(row) > 3 else ''
            invoice_num = row[4].strip() if len(row) > 4 else ''
            due_date = row[5].strip() if len(row) > 5 else ''
            past_due = row[6].strip() if len(row) > 6 else ''
            amount = row[7].strip() if len(row) > 7 else ''
            open_balance = row[8].strip() if len(row) > 8 else ''

            if not customer or not txn_type:
                continue

            # Get company type
            company_type = COMPANY_TYPE_MAP.get(company, 'unknown')

            # Check if IC
            is_ic = is_ic_customer(customer)

            record = {
                'customer': customer,
                'parent_customer': parent_customer if parent_customer != customer else '',
                'transaction_type': txn_type,
                'company': company,
                'company_type': company_type,
                'invoice_number': invoice_num,
                'due_date': parse_date(due_date),
                'due_date_original': due_date,
                'past_due_days': past_due,
                'amount': parse_amount(amount),
                'open_balance': parse_amount(open_balance),
                'is_ic': is_ic
            }

            if txn_type == 'Invoice':
                invoices.append(record)
            elif txn_type in ['Credit Memo', 'Customer Credit']:
                credits.append(record)
            else:
                other_transactions.append(record)

    # Write Invoices CSV
    with open(output_invoices, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['customer', 'parent_customer', 'transaction_type', 'company', 'company_type',
                      'invoice_number', 'due_date', 'due_date_original', 'past_due_days',
                      'amount', 'open_balance', 'is_ic']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(invoices)

    # Write Credits CSV (if any)
    if credits:
        with open(output_credits, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['customer', 'parent_customer', 'transaction_type', 'company', 'company_type',
                          'invoice_number', 'due_date', 'due_date_original', 'past_due_days',
                          'amount', 'open_balance', 'is_ic']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(credits)

    # Print summary
    print("=" * 60)
    print("INVOICES EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"\nTotal Invoices: {len(invoices)}")
    print(f"Total Customer Credits: {len(credits)}")
    print(f"Other Transactions: {len(other_transactions)}")

    # Invoices by company
    print("\n--- Invoices by Company ---")
    from collections import Counter
    company_counts = Counter(i['company'] for i in invoices)
    for company, count in sorted(company_counts.items(), key=lambda x: -x[1]):
        print(f"  {company}: {count}")

    # IC vs Regular
    ic_invoices = [i for i in invoices if i['is_ic']]
    regular_invoices = [i for i in invoices if not i['is_ic']]
    print(f"\n--- IC vs Regular ---")
    print(f"  Regular Invoices: {len(regular_invoices)}")
    print(f"  IC Invoices: {len(ic_invoices)}")

    # Total amounts
    total_amount = sum(i['amount'] for i in invoices)
    total_open = sum(i['open_balance'] for i in invoices)
    print(f"\n--- Totals ---")
    print(f"  Total Amount: ${total_amount:,.2f}")
    print(f"  Total Open Balance: ${total_open:,.2f}")

    # IC Customers found
    ic_customers = set(i['customer'] for i in ic_invoices)
    if ic_customers:
        print(f"\n--- IC Customers ({len(ic_customers)}) ---")
        for c in sorted(ic_customers):
            print(f"  - {c}")

    # Top customers by amount
    customer_amounts = {}
    for i in invoices:
        customer_amounts[i['customer']] = customer_amounts.get(i['customer'], 0) + i['amount']

    print(f"\n--- Top 10 Customers by Amount ---")
    for customer, amount in sorted(customer_amounts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {customer}: ${amount:,.2f}")

    # Unique customers count
    unique_customers = set(i['customer'] for i in invoices)
    print(f"\n--- Unique Customers: {len(unique_customers)} ---")

    print(f"\n--- Output Files ---")
    print(f"  Invoices: {output_invoices}")
    if credits:
        print(f"  Customer Credits: {output_credits}")

    if other_transactions:
        print(f"\n--- Other Transactions (not Invoices/Credits) ---")
        for t in other_transactions[:10]:  # Show first 10
            print(f"  {t['transaction_type']}: {t['customer']} - ${t['amount']:,.2f}")
        if len(other_transactions) > 10:
            print(f"  ... and {len(other_transactions) - 10} more")

if __name__ == '__main__':
    main()
