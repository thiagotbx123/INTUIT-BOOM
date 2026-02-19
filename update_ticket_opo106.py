import os
import requests
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY", "")
url = "https://api.linear.app/graphql"
headers = {"Content-Type": "application/json", "Authorization": LINEAR_API_KEY}

new_title = "[QuickBooks] Refine Data Ingestion QA Checklist"

new_description = """## 1. Context

To ingest data into QBO, there is a series of validation rules that need to be followed. These rules are documented in the current checklist (attached) and shared across the team. During a routine sync with Thais, she suggested some actions to improve the process, and short-term we agreed to refine the checklist so it becomes more efficient and easier to use.

---

## 2. Steps to Reproduce

1. Access the current ingestion checklist (see attachments).
2. Review the existing validation rules (59 total across QB, BIZ, and RL categories).
3. Identify redundancies, unclear steps, or rules that can be simplified.
4. Propose a refined version.

---

## 3. Acceptance Criteria

- [ ] Checklist is reviewed and simplified where possible.
- [ ] Rules are clear and actionable without needing external context.
- [ ] Checklist is efficient for day-to-day use by the ingestion team.
- [ ] Updated checklist is shared with the team.

---

## 4. Business Rules

1. Current checklist has 59 rules: 21 system (QB), 13 business logic (BIZ), 14 realism (RL), 11 pipeline (PIPE).
2. All 189 automated audit checks must still pass after refinement.
3. Rules must cover the full ingestion lifecycle: pre-ingestion validation, ingestion order, and post-ingestion verification.

---

## 5. Notes & Attachments

- Current checklist and validation rules are attached / shared in the ingestion docs.
- Action items came out of routine sync with Thais.
- Goal: make the checklist leaner and more practical without losing coverage.
"""

mutation = """
mutation($id: String!, $title: String!, $description: String!, $priority: Int) {
    issueUpdate(id: $id, input: { title: $title, description: $description, priority: $priority }) {
        success
        issue {
            identifier
            title
            url
        }
    }
}
"""

payload = {
    "query": mutation,
    "variables": {
        "id": "85656113-eb40-47e3-b932-83bb11a7d7ce",
        "title": new_title,
        "description": new_description,
        "priority": 2,
    },
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

if result.get("data", {}).get("issueUpdate", {}).get("success"):
    issue = result["data"]["issueUpdate"]["issue"]
    print("\nTicket atualizado!")
    print(f"  {issue['identifier']}: {issue['title']}")
    print(f"  {issue['url']}")
else:
    print("\nFalha ao atualizar")
