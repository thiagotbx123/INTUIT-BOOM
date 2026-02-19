import os
import requests
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY", "")
url = "https://api.linear.app/graphql"
headers = {"Content-Type": "application/json", "Authorization": LINEAR_API_KEY}

title = "[IES Construction Clone] Data QA Validation - Consolidated View Not Visible in Staging"

description = """## 1. Context

The **UAT IES Construction Clone** staging environment (Replica Keystone) does not display the **Consolidated View** feature, despite Intuit devs confirming it is enabled for the parent CID. This environment is critical for the **February IES Release** data validation and must replicate the production IES Construction environment, which includes Consolidated View.

**Environment:** UAT IES Construction Clone (Staging)
**Parent CID:** `9341456206579132`
**Dataset ID:** `321c6fa0-a4ee-4e05-b085-7b4d51473495`
**Login User (TestBox):** `quickbooks-testuser-construction-clone@tbxofficial.com`
**Non-Test User:** `quickbooks-construction-clone@tbxofficial.com`

### Company IDs in Scope
```
9341456206579132  (Parent - Keystone Construction)
9341456206626657
9341456206637825
9341456206632404
9341456206638768
9341456206644170
9341456206653434
9341456206642022
9341456206681900
9341456206675609
9341456206667919
9341456206666028
```

### Why This Matters
This environment is used for staging and data validation for the **February IES Release**. The full ingestion pipeline has **15 CSVs ready (10,831 rows), 189/189 audit checks PASS**, and is pending ingestion. Without Consolidated View, we cannot validate multi-entity features (IC transactions, consolidated P&L, intercompany eliminations) that are core to the Construction dataset.

**Ingestion Summary:**
| Entity | Rows | ID Range |
|--------|------|----------|
| Invoices | 335 | 45135-45469 |
| Invoice Line Items | 1,686 | 119728-121413 |
| Expenses | 650 | 9645-10294 |
| Expense Line Items | 1,006 | 8016-9021 |
| Bills | 96 | 4903-4998 |
| Bills Line Items | 149 | 5567-5715 |
| Estimates | 75 | 766-840 |
| Estimate Line Items | 410 | 4079-4488 |
| Estimate LI Classifications | 1,640 | 5626-7265 |
| Bank Transactions | 155 | 1321-1475 |
| Time Entries (supplement) | 3,996 | 73993-77988 |
| Project Tasks | 65 | 121-185 |
| Purchase Orders | 48 | 280-327 |
| PO Line Items | 104 | 1148-1251 |
| PO LI Classifications | 416 | 3381-3796 |
| **TOTAL** | **10,831** | |

---

## 2. Steps to Reproduce

1. Access the UAT IES Construction environment through TestBox.
2. TestBox routes to user `quickbooks-testuser-construction-clone@tbxofficial.com`.
3. Navigate to the environment-switcher page (company selector).
4. **Expected:** Consolidated View option should appear (as it does in prod IES Construction).
5. **Actual:** Consolidated View UI is **not present** in the environment-switcher.
6. Impersonating `lawton_ursrey@intuit.com` (who has Consolidated View access) via TestBox also does **not** show Consolidated View.
7. Logging in directly (not through TestBox) has not been tested yet.

**Loom Evidence:**
- [TestBox UAT - No Consolidated View (Marcus impersonation)](https://www.loom.com/share/f24d0e4278204257a4346f78938d7216)
- [TestBox UAT - No Consolidated View (Lawton impersonation)](https://www.loom.com/share/6b09674a0e604a1f9bc64d528fdf622c)

---

## 3. Acceptance Criteria

- [ ] Consolidated View UI appears in the environment-switcher page for the UAT IES Construction Clone.
- [ ] The test user (`quickbooks-testuser-construction-clone@tbxofficial.com`) has access to Consolidated View.
- [ ] The non-test user (`quickbooks-construction-clone@tbxofficial.com`) has access to Consolidated View.
- [ ] Behavior matches production IES Construction environment.
- [ ] Multi-entity reports (consolidated P&L, IC transactions) are accessible.

---

## 4. Business Rules

1. The staging environment must replicate the production IES Construction environment feature-for-feature, including Consolidated View.
2. Consolidated View access is controlled per-user; currently only `lawton_ursrey@intuit.com` and `quickbooks-construction-clone@tbxofficial.com` have access (per Intuit dev ksur).
3. The TEST user (`quickbooks-testuser-construction-clone@tbxofficial.com`) is the one used by TestBox for the UAT environment -- this user also needs Consolidated View access.
4. A migration may be required to enable Consolidated View on the clone (per sgeorge3), though Intuit devs (Ramasubramani) say it is already enabled for the parent hierarchy.
5. Direct login to the instance (bypassing TestBox) may be needed for Intuit devs to debug. Solution: create a separate admin user in the QBO instance for the Intuit dev (ksur) per Lucas Soranzo's guidance.

---

## 5. Notes & Attachments

### Investigation Timeline
| When | Who | What |
|------|-----|------|
| Feb 8 | sgeorge3 | Identified migration needed, pointed to Iqbal + mjain8 |
| Feb 8 | Kat | Requested urgent migration, shared 12 CIDs |
| Feb 8 | mjain8 | Said migration done, asked for Company ID confirmation |
| Feb 9 | Ramasubramani | Checked -- says Consolidated View is enabled, NTTF |
| Feb 9 | Kat | Shared Loom showing it still doesn't appear |
| Feb 9 | ksur | Confirmed only 2 users have access; asked for direct creds |
| Feb 9 | Kat | Tested impersonating Lawton -- still no Consolidated View |
| Feb 9 | Lucas Soranzo | Suggested creating separate user directly in QBO instance |
| Feb 9 | Kat | Requested Thiago/Alexandra create admin user for ksur |

### Root Cause Hypotheses
1. **User mapping mismatch:** TestBox uses the TEST user, but Consolidated View is only on the non-test user.
2. **TestBox impersonation limitation:** Even when impersonating a user with access, TestBox may not pass through the Consolidated View permission.
3. **Migration incomplete:** Despite Intuit saying NTTF, the feature flag may not be fully propagated.

### Related Tickets / Processes
- **Data Ingestion Handoff:** SESSION_HANDOFF_2026-02-08.md -- 15 CSVs ready, 189/189 audit PASS
- **Ingestion Guide:** GUIA_INGESTION_AUGUSTO.md -- Full step-by-step for Augusto
- **Validation Rules:** 59 rules documented (21 QB + 13 BIZ + 14 RL + 11 PIPE)
- **Post-Ingestion Checklist:** Includes P&L verification ($10.93M income, $2.93M net, 26.8% margin), employee duplication check, IC Balance Sheet validation
- **Slack Thread:** testbox-intuit-mm-external channel, Feb 8-9 2026

### Immediate Action Required
1. **Create admin user** in QBO Construction Clone instance for Intuit dev (ksur) to debug directly.
2. **Request ksur** to grant Consolidated View access to TEST user (`quickbooks-testuser-construction-clone@tbxofficial.com`).
3. **Verify** if TestBox impersonation passes Consolidated View permissions correctly.
"""

query = """
mutation CreateIssue($input: IssueCreateInput!) {
    issueCreate(input: $input) {
        success
        issue {
            id
            identifier
            url
            title
        }
    }
}
"""

payload = {
    "query": query,
    "variables": {
        "input": {
            "teamId": "b3fb1317-885c-47a0-b87d-85a77252d994",  # Opossum
            "title": title,
            "description": description,
            "assigneeId": "0879df15-56d6-477f-944d-df033121641a",  # Thais Linzmaier
            "labelIds": [
                "59234e85-ca51-4c41-8d94-7781ae2676b7",  # Customer Issues
                "c892d25f-944b-4afa-84fa-54824569d8d8",  # blocker
            ],
            "priority": 1,  # Urgent
        }
    },
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2))

if result.get("data", {}).get("issueCreate", {}).get("success"):
    issue = result["data"]["issueCreate"]["issue"]
    print("\nTicket criado com sucesso!")
    print(f"  ID: {issue['identifier']}")
    print(f"  URL: {issue['url']}")
    print(f"  Title: {issue['title']}")
else:
    print(f"\nFalha ao criar ticket: {json.dumps(result, indent=2)}")
