import csv
import sys
import random
import re
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

INPUT_FILE = r'C:\Users\adm_r\Downloads\PLA-3261_TIME_ENTRIES_FINAL.csv'
OUTPUT_FILE = r'C:\Users\adm_r\Downloads\PLA-3261_TIME_ENTRIES_v3.csv'

# IDs com erro de company_type (vamos remover esses - são só 21)
COMPANY_TYPE_ERROR_IDS = {
    '70533', '72951', '71275', '73726', '72228', '72098', '72359', '70638',
    '72409', '72554', '73859', '70077', '73298', '73323', '71753', '72276',
    '73639', '71818', '72842', '71213', '70940'
}

# Projects with CORRECT period calculation
# relative_start_date "X mons" = Jan + X months
PROJECTS = {
    19: {'name': 'Azure Pines', 'start_mon': 6, 'end_mon': 12},      # Jun-Dec (safe)
    20: {'name': 'GaleGuardian', 'start_mon': 3, 'end_mon': 8},      # Mar-Aug
    21: {'name': 'Intuit Dome', 'start_mon': 2, 'end_mon': 12},      # Feb-Dec (safe, avoid Jan edge)
    22: {'name': 'Leap Labs', 'start_mon': 5, 'end_mon': 10},        # May-Oct
}

# Realistic work hours distribution
WORK_START_TIMES = ['07:00', '07:15', '07:30', '07:45', '08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30']
WORK_DURATIONS = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]  # Hours

def parse_relative_date(date_str):
    """Parse '7 mons 15 days 09:45:00' -> month number (1=Jan, 8=Aug)"""
    if not date_str:
        return 1
    match = re.match(r'(\d+)\s*mons?', date_str)
    return int(match.group(1)) + 1 if match else 1

def get_safe_month_for_project(project_id):
    """Get a safe month well within the project period (avoid edges)"""
    proj = PROJECTS.get(project_id)
    if not proj:
        return 6
    # Pick from middle 60% of the range to avoid edge cases
    start = proj['start_mon']
    end = proj['end_mon']
    margin = max(1, (end - start) // 4)
    safe_start = start + margin
    safe_end = end - margin
    if safe_start >= safe_end:
        safe_start = start
        safe_end = end
    return random.randint(safe_start, safe_end)

def randomize_day():
    """Random day 1-28 (safe for all months)"""
    return random.randint(1, 28)

def adjust_date_smart(date_str, project_id):
    """Adjust date to be safely within project period with some randomization"""
    month = parse_relative_date(date_str)
    proj = PROJECTS.get(project_id)

    if not proj:
        return date_str

    # Check if month is safely within range (with 1 month buffer)
    safe_start = proj['start_mon'] + 1
    safe_end = proj['end_mon'] - 1

    if safe_start <= month <= safe_end:
        # Month is safe, maybe randomize day a bit
        return date_str

    # Need to adjust - pick a safe month
    new_month = get_safe_month_for_project(project_id)
    new_day = randomize_day()
    new_mons = new_month - 1  # Convert to mons format

    # Extract time from original
    time_match = re.search(r'(\d{2}:\d{2})', date_str)
    time_str = time_match.group(1) if time_match else random.choice(WORK_START_TIMES)

    return f'{new_mons} mons {new_day} days {time_str}:00'

def calculate_end_time(start_time, duration_hours):
    """Calculate end time from start time and duration"""
    h, m = map(int, start_time.split(':'))
    total_minutes = h * 60 + m + int(duration_hours * 60)
    end_h = (total_minutes // 60) % 24
    end_m = total_minutes % 60
    return f'{end_h:02d}:{end_m:02d}'

def randomize_times(row):
    """Add some realistic variation to work times"""
    # 30% chance to slightly adjust times
    if random.random() < 0.3:
        new_start = random.choice(WORK_START_TIMES)
        duration = random.choice(WORK_DURATIONS)
        new_end = calculate_end_time(new_start, duration)

        row['start_time'] = new_start
        row['end_time'] = new_end
        row['total_time'] = str(round(duration, 2))

    return row

def main():
    print("=" * 70)
    print("FIXING TIME ENTRIES v3 - SMART MODE")
    print("=" * 70)
    print("\nStrategy:")
    print("  1. Remove 21 entries with company_type errors")
    print("  2. Keep original company_type (main_child/parent)")
    print("  3. Fix dates to be SAFELY within project periods")
    print("  4. Add slight variation to make data more realistic")

    rows = []
    removed = 0
    date_fixed = 0
    times_varied = 0

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        fieldnames = reader.fieldnames

        for row in reader:
            # Remove entries with company_type errors
            if row['id'] in COMPANY_TYPE_ERROR_IDS:
                removed += 1
                continue

            proj_id = int(row['project_id'])
            original_date = row.get('start_date_relative', '')

            # Fix date if needed
            new_date = adjust_date_smart(original_date, proj_id)
            if new_date != original_date:
                row['start_date_relative'] = new_date
                # Also fix end_date_relative
                if row.get('end_date_relative'):
                    row['end_date_relative'] = adjust_date_smart(row['end_date_relative'], proj_id)
                date_fixed += 1

            # Add realistic variation (10% of entries)
            if random.random() < 0.1:
                row = randomize_times(row)
                times_varied += 1

            rows.append(row)

    # Write output
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n" + "=" * 70)
    print("RESULTS:")
    print("=" * 70)
    print(f"Original entries: 3993")
    print(f"Removed (company_type errors): {removed}")
    print(f"Final entries: {len(rows)}")
    print(f"Dates fixed: {date_fixed}")
    print(f"Times varied: {times_varied}")
    print(f"\n✅ Output saved to: {OUTPUT_FILE}")

    # Validate
    print("\n" + "-" * 70)
    print("VALIDATION:")
    print("-" * 70)

    errors = 0
    for row in rows:
        proj_id = int(row['project_id'])
        proj = PROJECTS.get(proj_id)
        month = parse_relative_date(row['start_date_relative'])

        if not (proj['start_mon'] <= month <= proj['end_mon']):
            print(f"ERROR: ID {row['id']}: month {month} not in {proj['start_mon']}-{proj['end_mon']}")
            errors += 1

    if errors == 0:
        print(f"✅ All {len(rows)} entries have valid dates!")
    else:
        print(f"❌ Found {errors} date errors")

    # Distribution
    print("\n" + "-" * 70)
    print("PROJECT DISTRIBUTION:")
    print("-" * 70)
    proj_counts = Counter(row['project_id'] for row in rows)
    for pid, count in sorted(proj_counts.items(), key=lambda x: int(x[0])):
        proj_name = PROJECTS.get(int(pid), {}).get('name', 'Unknown')
        pct = count / len(rows) * 100
        print(f"  Project {pid} ({proj_name}): {count} entries ({pct:.1f}%)")

    # Company type distribution
    print("\n" + "-" * 70)
    print("COMPANY TYPE DISTRIBUTION:")
    print("-" * 70)
    type_counts = Counter(row['company_type'] for row in rows)
    for ctype, count in type_counts.most_common():
        pct = count / len(rows) * 100
        print(f"  {ctype}: {count} entries ({pct:.1f}%)")

    # Employee distribution (top 10)
    print("\n" + "-" * 70)
    print("TOP 10 EMPLOYEES:")
    print("-" * 70)
    emp_counts = Counter(row['employee_id'] for row in rows)
    for emp_id, count in emp_counts.most_common(10):
        print(f"  Employee {emp_id}: {count} entries")

if __name__ == '__main__':
    main()
