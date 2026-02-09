"""Post Bug #24 fix to Linear"""

import requests
import time

API_URL = "https://api.linear.app/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "REDACTED_LINEAR_KEY_1",
}


def get_issue_id(identifier):
    query = "query ($filter: IssueFilter) { issues(filter: $filter, first: 1) { nodes { id identifier title } } }"
    number = int(identifier.split("-")[1])
    variables = {
        "filter": {
            "number": {"eq": number},
            "team": {"key": {"eq": identifier.split("-")[0]}},
        }
    }
    nodes = (
        requests.post(
            API_URL, headers=HEADERS, json={"query": query, "variables": variables}
        )
        .json()
        .get("data", {})
        .get("issues", {})
        .get("nodes", [])
    )
    if nodes:
        print(f"  Found: {nodes[0]['identifier']}")
        return nodes[0]["id"]
    return None


def post_comment(issue_id, body, identifier):
    query = "mutation CommentCreate($input: CommentCreateInput!) { commentCreate(input: $input) { success } }"
    success = (
        requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "query": query,
                "variables": {"input": {"issueId": issue_id, "body": body}},
            },
        )
        .json()
        .get("data", {})
        .get("commentCreate", {})
        .get("success", False)
    )
    print(f"  {'OK' if success else 'FAIL'} - {identifier}")
    return success


COMMENT_3261 = """# Bug #24 FIXED: Time Entries Outside Project Date Range (Feb 9, 2026)

## What happened
Time entry ID 77764 has date "11 mons 15 days" (December) but references project 20 (GaleGuardian) which is only active **March through August**. Same issue affects all 6 projects.

## Root cause
The generation script fills months 1, 2, 12 (Jan, Feb, Dec) for projects 19-22, and all 12 months for projects 23-24, **without checking each project's actual start date and length**.

## Project active periods (from DB)

| Project | Name | Start | Length | Active Months |
|---|---|---|---|---|
| 19 | Azure Pines | 5 mons | 9 mons | Jun-Dec |
| 20 | GaleGuardian | 2 mons | 6 mons | Mar-Aug |
| 21 | Intuit Dome | 1 mon | 12 mons | Feb-Dec |
| 22 | Leap Labs | 4 mons | 6 mons | May-Oct |
| 23 | BMH Landscaping | 3 mons | 9 mons | Apr-Dec |
| 24 | TidalWave | 4 mons | 12 mons | May-Dec |

## What was removed

| Project | Invalid Months | Rows Removed |
|---|---|---|
| 19 Azure Pines | Jan(27), Feb(36) | 63 |
| 20 GaleGuardian | Jan(27), Feb(36), Dec(36) | 99 |
| 21 Intuit Dome | Jan(27) | 27 |
| 22 Leap Labs | Jan(27), Feb(36), Dec(36) | 99 |
| 23 BMH | Jan(27), Feb(36), Mar(63) | 126 |
| 24 TidalWave | Jan(27), Feb(36), Mar(63), Apr(81) | 207 |
| **Total** | | **621 rows** |

## File history
- Original v5: 3,996 rows
- After Bug #22 fix (cancelled projects): 2,196 rows
- After Bug #24 fix (date ranges): **1,575 rows** (final)

## What remains
| Project | Rows | Months |
|---|---|---|
| 19 Azure Pines | 36 | Dec only |
| 21 Intuit Dome | 72 | Feb, Dec |
| 23 BMH | 774 | Apr-Dec |
| 24 TidalWave | 693 | May-Dec |

Note: Projects 20 and 22 have 0 supplement rows because the supplement was filling Jan/Feb/Dec gaps and those months are all outside the project's active period. Their existing time entries (from v4) already cover the valid months.

## Action for Augusto
Re-download `PLA-3261_TIME_ENTRIES_v5_supplement.csv`. New file has **1,575 rows**. All entries are now within their project's active date range.
"""

COMMENT_3212 = """# Bug #24 FIXED: Time Entries Date Range (Feb 9, 2026)

## Summary of all fixes today (Bugs #21-24)

| Bug | File | Issue | Rows Fixed |
|---|---|---|---|
| #21 | Expenses (file 03) | Employee FK - 6 invalid IDs | 8 remapped |
| #22 | Time Entries (file 11) | Cancelled projects 25, 26 | 1,800 removed |
| #24 | Time Entries (file 11) | Dates outside project period | 621 removed |

## Updated files for Augusto

| File | Original Rows | Final Rows |
|---|---|---|
| 03_REPLACE_INGESTION_EXPENSES_v4.csv | 650 | 650 (8 IDs remapped) |
| 11_APPEND_PLA-3261_TIME_ENTRIES_v5_supplement.csv | 3,996 | **1,575** |

All other 13 CSVs are unchanged.

## New checklist rules added today
- #24: QB_EMPLOYEE_FK_ACTUAL
- #25: QB_PROJECT_STATUS_ACTIVE
- #26: QB_FK_VALIDATE_FROM_DB
- #27: QB_TE_WITHIN_PROJECT_DATES

## Total bug count: 24 (all fixed)
"""

for ident, comment in [("PLA-3261", COMMENT_3261), ("PLA-3212", COMMENT_3212)]:
    print(f"\n--- {ident} ---")
    iid = get_issue_id(ident)
    if iid:
        post_comment(iid, comment, ident)
    time.sleep(0.5)
