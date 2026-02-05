import sqlite3
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r'C:\Users\adm_r\Clients\intuit-boom\data\qbo_database_part1.db'
DATASET_ID = '321c6fa0-a4ee-4e05-b085-7b4d51473495'
INGESTION_FILE = r'C:\Users\adm_r\Downloads\EMPLOYEES_INGESTION.csv'

def get_dataset_employees():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, first_name, last_name
        FROM employees
        WHERE dataset_id = ?
        ORDER BY id
    ''', (DATASET_ID,))
    employees = {f"{r[1]} {r[2]}".strip().lower(): {'id': r[0], 'first': r[1], 'last': r[2]}
                 for r in cursor.fetchall()}
    conn.close()
    return employees

def get_ingestion_employees():
    employees = {}
    with open(INGESTION_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = f"{row['first_name']} {row['last_name']}".strip().lower()
            employees[name] = {'first': row['first_name'], 'last': row['last_name'], 'email': row.get('email', '')}
    return employees

def main():
    print("=" * 70)
    print("EMPLOYEES CONSISTENCY CHECK")
    print("=" * 70)

    dataset_emps = get_dataset_employees()
    ingestion_emps = get_ingestion_employees()

    print(f"\nDataset employees: {len(dataset_emps)}")
    print(f"INGESTION file employees: {len(ingestion_emps)}")

    # Find differences
    dataset_names = set(dataset_emps.keys())
    ingestion_names = set(ingestion_emps.keys())

    only_in_dataset = dataset_names - ingestion_names
    only_in_ingestion = ingestion_names - dataset_names
    in_both = dataset_names & ingestion_names

    print(f"\n✅ In both: {len(in_both)}")
    print(f"❓ Only in Dataset: {len(only_in_dataset)}")
    print(f"❓ Only in INGESTION: {len(only_in_ingestion)}")

    if only_in_dataset:
        print("\n" + "-" * 70)
        print("⚠️  ONLY IN DATASET (not in INGESTION file):")
        print("-" * 70)
        for name in sorted(only_in_dataset):
            emp = dataset_emps[name]
            print(f"  ID {emp['id']}: {emp['first']} {emp['last']}")

    if only_in_ingestion:
        print("\n" + "-" * 70)
        print("⚠️  ONLY IN INGESTION (not in Dataset):")
        print("-" * 70)
        for name in sorted(only_in_ingestion):
            emp = ingestion_emps[name]
            print(f"  {emp['first']} {emp['last']} ({emp['email']})")

    # Check for similar names (possible typos)
    print("\n" + "-" * 70)
    print("POSSIBLE MATCHES (similar names):")
    print("-" * 70)

    for name1 in only_in_dataset:
        for name2 in only_in_ingestion:
            # Check if first name or last name matches
            parts1 = name1.split()
            parts2 = name2.split()
            if len(parts1) >= 1 and len(parts2) >= 1:
                if parts1[0] == parts2[0] or (len(parts1) > 1 and len(parts2) > 1 and parts1[-1] == parts2[-1]):
                    print(f"  Dataset: '{name1}' <-> INGESTION: '{name2}'")

    # Summary by ID
    print("\n" + "-" * 70)
    print("DATASET IDs USED:")
    print("-" * 70)
    ids_used = sorted([e['id'] for e in dataset_emps.values()])
    print(f"  IDs: {ids_used}")
    print(f"  MIN: {min(ids_used)}, MAX: {max(ids_used)}")

    # Find gaps in IDs
    all_ids = set(range(min(ids_used), max(ids_used) + 1))
    missing_ids = all_ids - set(ids_used)
    if missing_ids:
        print(f"  Missing IDs (gaps): {sorted(missing_ids)}")

    print("\n" + "=" * 70)
    print("RECOMMENDATION")
    print("=" * 70)

    if only_in_ingestion:
        print(f"""
{len(only_in_ingestion)} employees in INGESTION file not in Dataset.
These may be NEW employees Alexandra added or need to be ingested.

Next IDs available: {max(ids_used) + 1}+
""")

if __name__ == '__main__':
    main()
