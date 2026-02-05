import csv
import sys
import random
import re

sys.stdout.reconfigure(encoding='utf-8')

INPUT_FILE = r'C:\Users\adm_r\Downloads\PLA-3261_TIME_ENTRIES_FIXED.csv'
OUTPUT_FILE = r'C:\Users\adm_r\Downloads\PLA-3261_TIME_ENTRIES_FINAL.csv'

# Projects in dataset with their periods (month numbers, 0-indexed from Jan)
PROJECTS = {
    19: {'name': 'Azure Pines', 'start_mon': 5, 'end_mon': 14, 'customer_id': 19},
    20: {'name': 'GaleGuardian', 'start_mon': 2, 'end_mon': 8, 'customer_id': 33},
    21: {'name': 'Intuit Dome', 'start_mon': 1, 'end_mon': 13, 'customer_id': 15},  # Full year
    22: {'name': 'Leap Labs', 'start_mon': 4, 'end_mon': 10, 'customer_id': 42},
}

# Remap invalid project IDs
PROJECT_REMAP = {
    23: 19,
    24: 20,
    25: 21,
    26: 22,
}

def parse_relative_date(date_str):
    """Extract month number from relative date like '5 mons 3 days 11:15:00'"""
    if not date_str:
        return 1
    match = re.match(r'(\d+)\s*mons?', date_str)
    if match:
        return int(match.group(1)) + 1  # Convert to 1-indexed month
    return 1

def get_projects_for_month(month):
    """Get list of valid project IDs for a given month"""
    valid = []
    for pid, proj in PROJECTS.items():
        if proj['start_mon'] <= month <= proj['end_mon']:
            valid.append(pid)
    # Fallback to Intuit Dome (covers full year)
    if not valid:
        valid = [21]
    return valid

def adjust_date_for_project(date_str, project_id):
    """Adjust date to fit within project period if needed"""
    month = parse_relative_date(date_str)
    proj = PROJECTS.get(project_id)

    if not proj:
        return date_str

    # If month is within project period, keep as is
    if proj['start_mon'] <= month <= proj['end_mon']:
        return date_str

    # Adjust month to fit within project period
    if month < proj['start_mon']:
        new_month = proj['start_mon']
    else:
        new_month = proj['end_mon']

    # Replace month in date string
    new_date = re.sub(r'^\d+\s*mons?', f'{new_month - 1} mons', date_str)
    return new_date

def main():
    print("=" * 70)
    print("FIXING TIME ENTRIES - PROJECTS AND DATES")
    print("=" * 70)

    rows = []
    stats = {
        'remapped': 0,
        'assigned': 0,
        'date_adjusted': 0,
        'already_ok': 0,
    }

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        fieldnames = reader.fieldnames

        for row in reader:
            original_proj = row.get('project_id', '').strip()
            original_date = row.get('start_date_relative', '')
            month = parse_relative_date(original_date)

            # Step 1: Determine project_id
            if original_proj:
                proj_id = int(original_proj)
                # Remap invalid IDs
                if proj_id in PROJECT_REMAP:
                    proj_id = PROJECT_REMAP[proj_id]
                    stats['remapped'] += 1
                else:
                    stats['already_ok'] += 1
            else:
                # Assign project based on month
                valid_projects = get_projects_for_month(month)
                proj_id = random.choice(valid_projects)
                stats['assigned'] += 1

            row['project_id'] = str(proj_id)

            # Step 2: Adjust date if needed
            new_date = adjust_date_for_project(original_date, proj_id)
            if new_date != original_date:
                row['start_date_relative'] = new_date
                # Also adjust end_date_relative if present
                if row.get('end_date_relative'):
                    row['end_date_relative'] = adjust_date_for_project(
                        row['end_date_relative'], proj_id
                    )
                stats['date_adjusted'] += 1

            # Step 3: Update customer_id to match project's customer (optional - for consistency)
            # Keeping original customer_id as it represents who the work was for

            rows.append(row)

    # Write output
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nTotal rows: {len(rows)}")
    print(f"Already OK (valid project): {stats['already_ok']}")
    print(f"Remapped (23-26 → 19-22): {stats['remapped']}")
    print(f"Assigned (was empty): {stats['assigned']}")
    print(f"Date adjusted: {stats['date_adjusted']}")
    print(f"\n✅ Output saved to: {OUTPUT_FILE}")

    # Show project distribution
    print("\n" + "-" * 70)
    print("PROJECT DISTRIBUTION IN OUTPUT:")
    print("-" * 70)

    from collections import Counter
    proj_counts = Counter(row['project_id'] for row in rows)
    for pid, count in sorted(proj_counts.items(), key=lambda x: int(x[0])):
        proj_name = PROJECTS.get(int(pid), {}).get('name', 'Unknown')
        print(f"  Project {pid} ({proj_name}): {count} entries")

if __name__ == '__main__':
    main()
