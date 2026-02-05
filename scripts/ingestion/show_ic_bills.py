import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\adm_r\Downloads\INGESTION_PLANS\SALES_BILLS.csv', encoding='utf-8') as f:
    data = list(csv.DictReader(f))

ic_bills = [b for b in data if b['is_ic'] == 'True']

print(f"IC Bills encontrados: {len(ic_bills)}\n")
print(f"{'Vendor':<45} | {'Company':<25} | {'Bill #':<20} | {'Amount':>12}")
print("-" * 110)
for b in ic_bills:
    print(f"{b['vendor']:<45} | {b['company']:<25} | {b['bill_number']:<20} | ${float(b['amount']):>11,.2f}")
