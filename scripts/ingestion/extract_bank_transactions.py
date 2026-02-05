import csv
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Company mapping
COMPANY_MAP = {
    'Keystone Construction (Par)': {'company_type': 'parent', 'qbo_company': 'Keystone Construction (Par)'},
    'Keystone BlueCraft': {'company_type': 'main_child', 'qbo_company': 'Keystone BlueCraft'},
    'Keystone Terra (Ch.)': {'company_type': 'secondary_child', 'qbo_company': 'Keystone Terra (Ch.)'},
    'KeyStone Volt': {'company_type': 'secondary_child', 'qbo_company': 'KeyStone Volt'},
    'KeyStone Stonecraft': {'company_type': 'secondary_child', 'qbo_company': 'KeyStone Stonecraft'},
}

# Bank account patterns to identify bank transactions
BANK_ACCOUNT_PATTERNS = [
    '1010 Checking',
    'Checking',
    'Cash',
    'Petty Cash',
    '10100 Business Operation Main',
    '10101 Patient Register',
    '10102 Patient Register',
]

# Files to process
FILES = [
    (r'C:\Users\adm_r\Downloads\Keystone Construction (Par)_Transaction Detail by Account.csv', 'Keystone Construction (Par)'),
    (r'C:\Users\adm_r\Downloads\Keystone BlueCraft_Transaction Detail by Account.csv', 'Keystone BlueCraft'),
    (r'C:\Users\adm_r\Downloads\Keystone Terra (Ch.)_Transaction Detail by Account.csv', 'Keystone Terra (Ch.)'),
    (r'C:\Users\adm_r\Downloads\KeyStone Volt_Transaction Detail by Account (1).csv', 'KeyStone Volt'),
    (r'C:\Users\adm_r\Downloads\KeyStone Stonecraft_Transaction Detail by Account.csv', 'KeyStone Stonecraft'),
]

def is_bank_account(account_name):
    """Check if the account is a bank account"""
    if not account_name:
        return False
    account_lower = account_name.lower()
    for pattern in BANK_ACCOUNT_PATTERNS:
        if pattern.lower() in account_lower:
            return True
    return False

def parse_amount(amount_str):
    """Parse amount string to float"""
    if not amount_str:
        return 0.0
    # Remove quotes, dollar signs, commas
    cleaned = amount_str.replace('"', '').replace('$', '').replace(',', '').strip()
    if not cleaned or cleaned == '-':
        return 0.0
    try:
        return float(cleaned)
    except:
        return 0.0

def extract_bank_transactions(file_path, company_name):
    """Extract bank transactions from a Transaction Detail by Account file"""
    transactions = []

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except:
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()

    current_account = None
    in_bank_section = False
    header_row = None

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Parse CSV
        try:
            reader = csv.reader([line])
            row = next(reader)
        except:
            continue

        if len(row) < 2:
            continue

        # Check if this is an account header (first column empty, second has account name, rest mostly empty)
        first_col = row[0].strip() if row[0] else ''

        # Detect account section headers - they have account name in first non-empty position
        # and look like "1010 Checking,,,,,,,," or ",1010 Checking,,,,,,"

        # Check for account header patterns
        potential_account = None
        if first_col and not any(c.isdigit() and c != '0' for c in first_col[:2]) and 'Total' not in first_col and 'Transaction' not in first_col:
            # Could be account name in first column
            if len(row) > 2 and all(not r.strip() for r in row[1:] if r):
                potential_account = first_col

        # Also check if it's a section like "1010 Checking" with commas after
        if not potential_account and first_col:
            # Check patterns like "1010 Checking", "Cash", "Petty Cash", etc.
            for pattern in BANK_ACCOUNT_PATTERNS:
                if pattern.lower() in first_col.lower():
                    potential_account = first_col
                    break

        if potential_account:
            current_account = potential_account
            in_bank_section = is_bank_account(current_account)
            continue

        # Check for "Total for X" which ends the section
        if first_col.startswith('Total for') or (len(row) > 1 and row[0] == '' and row[1] and 'Total for' in str(row[1])):
            if in_bank_section:
                in_bank_section = False
            continue

        # Skip header rows
        if 'Transaction date' in line or 'Transaction type' in line:
            header_row = row
            continue

        # If we're in a bank section, extract the transaction
        if in_bank_section and current_account:
            # Try to parse as transaction row (first col empty, has date in second col)
            if row[0] == '' and len(row) > 2:
                date_str = row[1].strip() if len(row) > 1 else ''

                # Validate date format MM/DD/YYYY
                if date_str and '/' in date_str:
                    try:
                        # Parse date
                        parsed_date = datetime.strptime(date_str, '%m/%d/%Y')

                        # Extract fields - structure varies by company
                        # Common structure: empty, date, type, num, name, ..., amount, balance
                        txn_type = row[2].strip() if len(row) > 2 else ''
                        txn_num = row[3].strip() if len(row) > 3 else ''
                        name = row[4].strip() if len(row) > 4 else ''

                        # Find amount - usually second to last non-empty field
                        amount = 0.0
                        for j in range(len(row) - 1, 0, -1):
                            val = row[j].strip()
                            if val and val != '-':
                                # Skip balance (last value), get amount (second to last)
                                amount = parse_amount(row[j-1]) if j > 1 else parse_amount(val)
                                break

                        # Get memo/description - varies by position
                        memo = ''
                        for j in range(5, min(len(row)-2, 8)):
                            if row[j].strip() and row[j].strip() not in ['Checking', '-']:
                                memo = row[j].strip()
                                break

                        transactions.append({
                            'company': company_name,
                            'company_type': COMPANY_MAP[company_name]['company_type'],
                            'account': current_account,
                            'date': date_str,
                            'type': txn_type,
                            'num': txn_num,
                            'name': name,
                            'memo': memo,
                            'amount': amount,
                        })
                    except ValueError:
                        pass

    return transactions

def main():
    all_transactions = []

    print("Extracting bank transactions from 5 companies...\n")

    for file_path, company_name in FILES:
        if os.path.exists(file_path):
            txns = extract_bank_transactions(file_path, company_name)
            print(f"  {company_name}: {len(txns)} bank transactions")
            all_transactions.extend(txns)
        else:
            print(f"  {company_name}: FILE NOT FOUND")

    print(f"\nTotal: {len(all_transactions)} bank transactions")

    # Write consolidated CSV
    output_path = r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_BANK_TRANSACTIONS.csv'

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'company', 'company_type', 'account', 'date', 'type', 'num', 'name', 'memo', 'amount'
        ])
        writer.writeheader()
        writer.writerows(all_transactions)

    print(f"\nSaved to: {output_path}")

    # Summary by company
    print("\n=== Summary by Company ===")
    from collections import Counter
    company_counts = Counter(t['company'] for t in all_transactions)
    for company, count in sorted(company_counts.items()):
        print(f"  {company}: {count}")

    # Summary by type
    print("\n=== Summary by Transaction Type ===")
    type_counts = Counter(t['type'] for t in all_transactions)
    for txn_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {txn_type}: {count}")

if __name__ == '__main__':
    main()
