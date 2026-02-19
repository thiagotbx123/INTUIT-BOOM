"""Post Bug #22 fix update to Linear tickets PLA-3261 (Time Entries) and PLA-3212 (Master)"""

import os
import requests
import time

API_URL = "https://api.linear.app/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": os.environ.get("LINEAR_API_KEY", ""),
}


def get_issue_id(identifier):
    query = """
    query ($filter: IssueFilter) {
      issues(filter: $filter, first: 1) {
        nodes { id identifier title }
      }
    }
    """
    number = int(identifier.split("-")[1])
    variables = {
        "filter": {
            "number": {"eq": number},
            "team": {"key": {"eq": identifier.split("-")[0]}},
        }
    }
    resp = requests.post(
        API_URL, headers=HEADERS, json={"query": query, "variables": variables}
    )
    nodes = resp.json().get("data", {}).get("issues", {}).get("nodes", [])
    if nodes:
        print(f"  Found: {nodes[0]['identifier']} - {nodes[0]['title']}")
        return nodes[0]["id"]
    return None


def post_comment(issue_id, body, identifier):
    query = """
    mutation CommentCreate($input: CommentCreateInput!) {
        commentCreate(input: $input) { success comment { id } }
    }
    """
    resp = requests.post(
        API_URL,
        headers=HEADERS,
        json={
            "query": query,
            "variables": {"input": {"issueId": issue_id, "body": body}},
        },
    )
    success = resp.json().get("data", {}).get("commentCreate", {}).get("success", False)
    print(f"  {'OK' if success else 'FAIL'} - Comment posted to {identifier}")
    return success


COMMENT_3261 = """# Bug #22 FIXED: Cancelled Projects in Time Entries (Feb 9, 2026)

## What happened
Augusto tried to ingest time entries and got errors because some entries reference **projects 25 and 26, which are Canceled** in the database.

## Root cause
The generation script hardcoded `for proj in [23, 24, 25, 26]` without checking project status. Projects 25 (Rowe Hotel - Parking Lot) and 26 (Arbor Dunes - Garden Walk) have status `Canceled` in the DB.

## What was fixed
**1,800 rows removed** (45% of the original 3,996). All entries for projects 25 and 26 were deleted.

| Project | Name | Status | Rows | Action |
|---|---|---|---|---|
| 19 | Azure Pines | In progress | 99 | KEPT |
| 20 | GaleGuardian Turbine | In progress | 99 | KEPT |
| 21 | Intuit Dome | In progress | 99 | KEPT |
| 22 | Leap Labs Solar | In progress | 99 | KEPT |
| 23 | BMH Landscaping | In progress | 900 | KEPT |
| 24 | TidalWave Farmer's Market | In progress | 900 | KEPT |
| **25** | **Rowe Hotel Parking Lot** | **Canceled** | **900** | **REMOVED** |
| **26** | **Arbor Dunes Garden Walk** | **Canceled** | **900** | **REMOVED** |

## Updated file
- New row count: **2,196** (was 3,996)
- ID range still: 73993-77988 (but with gaps where cancelled rows were removed)
- File: `PLA-3261_TIME_ENTRIES_v5_supplement.csv` - ready for re-download

## Date check
Our CSV is clean - max interval is 363 days (within the 365 limit). However, there are **823 pre-existing entries in the DB** (from prior ingestion) with dates > 365 days (up to month 17). These are NOT from our CSV - they are a separate data quality issue that may need cleanup.

## New audit rules added
- **QB_PROJECT_STATUS_ACTIVE**: project_id must reference a project with status 'In progress'
- **QB_FK_VALIDATE_FROM_DB**: All FKs must be validated against actual DB records, never assumed ranges

## Action for Augusto
Re-download the time entries file and retry. The fixed file has 2,196 rows, all referencing active projects only.

About the dates > 365 days: those 823 entries are already in the DB from a previous ingestion. If they are causing issues, they need to be cleaned up separately (they are not from our CSV).
"""

COMMENT_3212 = """# Bugs #22/#23 FIXED: Time Entries - Cancelled Projects (Feb 9, 2026)

## Issues found and fixed today

### Bug #21 (Expenses) - FIXED earlier today
- 8 expenses referenced non-existent employee IDs (gaps in 1-50 range)
- File 03 patched, ready for re-download

### Bug #22 (Time Entries) - FIXED now
- 1,800 rows referenced cancelled projects 25, 26
- Removed from file 11. New count: **2,196 rows** (was 3,996)

### Bug #23 (Dates) - VERIFIED CLEAN
- Our CSV max date = 363 days (within limit)
- 823 entries already in DB with dates > 365 days are from prior ingestion, not ours

## Updated files to re-download
| # | File | Old Rows | New Rows | Change |
|---|------|----------|----------|--------|
| 03 | INGESTION_EXPENSES_v4.csv | 650 | 650 | 8 employee IDs remapped |
| 11 | PLA-3261_TIME_ENTRIES_v5_supplement.csv | 3,996 | 2,196 | 1,800 cancelled project rows removed |

All other 13 CSVs are unchanged and ready.

## New audit rules (total now: 26 QB rules)
- #24: QB_EMPLOYEE_FK_ACTUAL
- #25: QB_PROJECT_STATUS_ACTIVE
- #26: QB_FK_VALIDATE_FROM_DB

## Bug count: 23 total (all fixed)
"""


def main():
    for identifier, comment in [("PLA-3261", COMMENT_3261), ("PLA-3212", COMMENT_3212)]:
        print(f"\n--- {identifier} ---")
        issue_id = get_issue_id(identifier)
        if issue_id:
            post_comment(issue_id, comment, identifier)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
