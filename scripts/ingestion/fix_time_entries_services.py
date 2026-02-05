import csv
import sys
import random

sys.stdout.reconfigure(encoding='utf-8')

INPUT_FILE = r'C:\Users\adm_r\Downloads\PLA-3261_TIME_ENTRIES_SYNTHETIC (1).csv'
OUTPUT_FILE = r'C:\Users\adm_r\Downloads\PLA-3261_TIME_ENTRIES_FIXED.csv'

# Valid service IDs with their categories
VALID_SERVICES = {
    # Planning & Coordination (more common for office/billable work)
    'planning': [3, 4, 5, 9, 10, 11, 12, 13, 14, 21],
    # Field Work (more common for non-billable/field employees)
    'field': [22, 23, 24, 25, 26, 74, 76, 77],
    # Management (for senior/management entries)
    'management': [2, 212],
    # Technical/Specialized
    'technical': [6, 7, 8, 15, 16, 17, 18, 19, 20],
}

ALL_VALID_IDS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 74, 76, 77, 212]

def get_logical_service(row, current_id):
    """Get a logical service ID based on row characteristics"""

    # If current ID is already valid, keep it with 70% probability
    if current_id in ALL_VALID_IDS:
        if random.random() < 0.7:
            return current_id

    billable = row.get('billable', '0')
    company_type = row.get('company_type', 'main_child')
    has_project = bool(row.get('project_id', '').strip())

    # Logic for service selection
    if billable == '1':
        # Billable work - more likely planning/technical
        if has_project:
            # Project work - technical or field
            pool = VALID_SERVICES['technical'] + VALID_SERVICES['field']
        else:
            # General billable - planning or management
            pool = VALID_SERVICES['planning'] + VALID_SERVICES['management']
    else:
        # Non-billable - could be anything, slightly favor field work
        if company_type == 'parent':
            # Parent company - more management/planning
            pool = VALID_SERVICES['management'] + VALID_SERVICES['planning']
        else:
            # Child company - more field work
            pool = VALID_SERVICES['field'] + VALID_SERVICES['technical']

    return random.choice(pool)

def main():
    print("=" * 70)
    print("FIXING TIME ENTRIES - PRODUCT_SERVICE_ID")
    print("=" * 70)
    print(f"\nValid service IDs: {len(ALL_VALID_IDS)}")
    print(f"IDs: {ALL_VALID_IDS}")

    # Read input file
    rows = []
    invalid_count = 0
    valid_count = 0

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        # Detect delimiter
        first_line = f.readline()
        f.seek(0)
        delimiter = ';' if ';' in first_line else ','
        print(f"\nDetected delimiter: '{delimiter}'")

        reader = csv.DictReader(f, delimiter=delimiter)
        fieldnames = reader.fieldnames

        for row in reader:
            current_id = row.get('product_service_id', '')

            # Try to convert to int
            try:
                current_id_int = int(current_id) if current_id else 0
            except:
                current_id_int = 0

            # Check if valid
            if current_id_int in ALL_VALID_IDS:
                valid_count += 1
                new_id = current_id_int
            else:
                invalid_count += 1
                new_id = get_logical_service(row, current_id_int)

            row['product_service_id'] = str(new_id)
            rows.append(row)

    print(f"\nTotal rows: {len(rows)}")
    print(f"Already valid: {valid_count}")
    print(f"Fixed (invalid → valid): {invalid_count}")

    # Write output file
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Output saved to: {OUTPUT_FILE}")

    # Show distribution of services
    print("\n" + "-" * 70)
    print("SERVICE DISTRIBUTION IN OUTPUT:")
    print("-" * 70)

    from collections import Counter
    service_counts = Counter(row['product_service_id'] for row in rows)
    for sid, count in sorted(service_counts.items(), key=lambda x: int(x[0])):
        print(f"  ID {sid}: {count} entries")

if __name__ == '__main__':
    main()
