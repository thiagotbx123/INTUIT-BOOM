"""Post Bug #21 fix update to Linear tickets PLA-3259 (Expenses) and PLA-3212 (Master)"""

import requests
import time

API_URL = "https://api.linear.app/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "REDACTED_LINEAR_KEY_1",
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


# Comment for PLA-3259 (Expenses)
COMMENT_3259 = """# Bug #21 FIXED: Employee FK Violation (Feb 9, 2026)

## What happened
Augusto tried to ingest expenses and got a **foreign key error**: the CSV referenced employee IDs that do not exist in the database.

## Root cause
Our CSV generator used `range(1, 51)` assuming all IDs from 1 to 50 exist. But the employee table has **44 employees with 6 gaps** - IDs 4, 6, 38, 42, 46, 48 were never created.

## What was fixed
8 expense rows (out of 650) were remapped to valid nearby employee IDs:

| Expense ID | Old employee_id (invalid) | New employee_id (valid) | Employee Name |
|---|---|---|---|
| 9667 | 42 | 41 | Elizabeth Kim |
| 9731 | 4 | 3 | Emma Johnson |
| 9736 | 48 | 49 | James Jacobes |
| 9738 | 4 | 3 | Emma Johnson |
| 9840 | 38 | 37 | Tyler Frazer |
| 9918 | 6 | 7 | Olivia Davis |
| 9994 | 46 | 45 | Zoe Lewis |
| 10234 | 46 | 45 | Zoe Lewis |

## Updated file
`03_REPLACE_INGESTION_EXPENSES_v4.csv` has been patched (backup saved). The fixed version is ready for re-ingestion.

**No other CSVs are affected** - only expenses reference employee_id. Time entries supplement (file 11) was already clean.

## New audit rule added
**QB_EMPLOYEE_FK_ACTUAL**: employee_id must reference an ID that actually exists in the employees table, not just be within the ID range. Always query the DB for actual IDs.

## Action for Augusto
Please re-download `03_REPLACE_INGESTION_EXPENSES_v4.csv` from the shared folder and retry the ingestion. The file is now fixed.
"""

# Comment for PLA-3212 (Master)
COMMENT_3212 = """# Bug #21 FIXED: Employee FK Violation in Expenses (Feb 9, 2026)

## Issue
Augusto reported FK error when inserting expenses: employee IDs 4, 6, 38, 42, 46, 48 do not exist in the employee table (gaps in the 1-50 range).

## Fix applied
8 rows in `03_REPLACE_INGESTION_EXPENSES_v4.csv` remapped to valid employee IDs. All other CSVs verified clean.

## Updated file
Only **file 03** (expenses) needs to be re-downloaded. All 14 other CSVs are unchanged.

## New rule added to checklist
**QB_EMPLOYEE_FK_ACTUAL** (rule #24): Always validate employee_id against actual DB records, never use range().

## Bug count: 21 total (all fixed)
"""


def main():
    for identifier, comment in [("PLA-3259", COMMENT_3259), ("PLA-3212", COMMENT_3212)]:
        print(f"\n--- {identifier} ---")
        issue_id = get_issue_id(identifier)
        if issue_id:
            post_comment(issue_id, comment, identifier)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
