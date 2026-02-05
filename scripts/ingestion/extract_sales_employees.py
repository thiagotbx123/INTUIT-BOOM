import csv
import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

SALES_FILE = r'C:\Users\adm_r\Downloads\employee_hours_by_day_2024-01-01_thru_2026-02-04 (1).csv'
DB_PATH = r'C:\Users\adm_r\Clients\intuit-boom\data\qbo_database_part1.db'
DATASET_ID = '321c6fa0-a4ee-4e05-b085-7b4d51473495'
INGESTION_FILE = r'C:\Users\adm_r\Downloads\EMPLOYEES_INGESTION.csv'

def get_sales_employees():
    """Extract unique employees from SALES hours file"""
    employees = set()
    with open(SALES_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp = row.get('Employee', '').strip()
            if emp:
                employees.add(emp)
    return sorted(employees)

def get_dataset_employees():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, first_name, last_name
        FROM employees
        WHERE dataset_id = ?
        ORDER BY first_name, last_name
    ''', (DATASET_ID,))
    employees = {}
    for row in cursor.fetchall():
        name = f"{row[1]} {row[2]}".strip()
        employees[name.lower()] = {'id': row[0], 'name': name}
    conn.close()
    return employees

def get_ingestion_employees():
    employees = {}
    with open(INGESTION_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = f"{row['first_name']} {row['last_name']}".strip()
            employees[name.lower()] = {'name': name, 'email': row.get('email', '')}
    return employees

def normalize_name(name):
    """Normalize name for comparison (Last, First -> First Last)"""
    if ',' in name:
        parts = name.split(',')
        if len(parts) == 2:
            return f"{parts[1].strip()} {parts[0].strip()}".lower()
    return name.lower()

def main():
    print("=" * 70)
    print("SALES vs DATASET vs INGESTION - EMPLOYEES COMPARISON")
    print("=" * 70)

    sales_emps = get_sales_employees()
    dataset_emps = get_dataset_employees()
    ingestion_emps = get_ingestion_employees()

    print(f"\nSALES employees (from hours report): {len(sales_emps)}")
    print(f"Dataset employees: {len(dataset_emps)}")
    print(f"INGESTION file employees: {len(ingestion_emps)}")

    # Normalize SALES names for comparison
    sales_normalized = {normalize_name(n): n for n in sales_emps}

    print("\n" + "=" * 70)
    print("SALES EMPLOYEES LIST (Source of Truth)")
    print("=" * 70)
    for name in sales_emps:
        normalized = normalize_name(name)
        in_dataset = "✅ Dataset" if normalized in dataset_emps else "❌"
        in_ingestion = "✅ INGESTION" if normalized in ingestion_emps else "❌"
        print(f"  {name:<25} | {in_dataset:<12} | {in_ingestion}")

    # Find SALES employees not in Dataset
    print("\n" + "=" * 70)
    print("⚠️  SALES EMPLOYEES NOT IN DATASET")
    print("=" * 70)
    missing_from_dataset = []
    for name in sales_emps:
        normalized = normalize_name(name)
        if normalized not in dataset_emps:
            missing_from_dataset.append(name)
            in_ingestion = "✅ In INGESTION" if normalized in ingestion_emps else "❌ NOT in INGESTION"
            print(f"  {name:<25} | {in_ingestion}")

    # Find Dataset employees not in SALES
    print("\n" + "=" * 70)
    print("⚠️  DATASET EMPLOYEES NOT IN SALES")
    print("=" * 70)
    for name_lower, emp in dataset_emps.items():
        if name_lower not in sales_normalized:
            print(f"  ID {emp['id']}: {emp['name']}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
SALES: {len(sales_emps)} employees
Dataset: {len(dataset_emps)} employees
INGESTION: {len(ingestion_emps)} employees

Missing from Dataset: {len(missing_from_dataset)}
""")

    if missing_from_dataset:
        print("Employees to ADD to Dataset:")
        for name in missing_from_dataset:
            print(f"  - {name}")

if __name__ == '__main__':
    main()
