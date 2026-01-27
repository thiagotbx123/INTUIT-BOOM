import requests
import json
import os

url = 'https://api.linear.app/graphql'
headers = {
    'Content-Type': 'application/json',
    'Authorization': os.environ.get('LINEAR_API_KEY', '')
}

description = """## Summary

Massive employee duplication discovered in Keystone Construction payroll - 90 employees showing errors, with some names appearing 15+ times. Issue was investigated, root cause identified (QBO-side anomaly), and resolved via manual cleanup.

## Environment

- Ambiente: Keystone Construction (IES Multi-Entity)
- Dataset: construction_demo
- Dataset ID: 2ed5d245-0578-43aa-842b-6e1e28367149
- CID Parent: 9341454156620895
- CID Terra: 9341454156620204

## Problem Description

Rachel reported payroll errors in Keystone Construction. Investigation revealed:

1. **90 employees with errors** in the system
2. **Massive duplication** - employees like Babar, Varun appearing 15+ times
3. **Corrupted record** found: name "Babar, Varun, Babar, Varun" with Intuit test email (@mailinator)
4. **External employees** - Spencer Hiko and Laura Frank exist in environment but NOT in our original dataset

## Root Cause Analysis

**Primary Hypothesis:** QBO-side automatic recovery creating duplicates

**Evidence:**
- Corrupted name suggests payload concatenation from retry/recovery
- Test email (@mailinator) indicates Intuit internal process
- TBX error handling confirmed working correctly (per Soranzo)
- Original dataset is clean (45 unique employees, no duplicates)

**Conclusion:** Problem is NOT in TBX code. QBO may have recovered failed API calls and created duplicate records.

## Resolution

**Action taken:** Manual deletion of ~86 duplicate records

**Process:**
1. Identified all duplicates in Payroll > Employees
2. Deleted duplicates one by one
3. Preserved only original/cleanest record for each employee
4. Validated with payroll preview test

**Time to resolve:** ~2 hours (investigation + cleanup)

## Validation

Payroll preview test after cleanup:
- Employees: 4 (unique)
- Total Hours: 320h
- Gross Pay: $14,676.91
- Total Payroll Cost: $16,433.44
- Status: Ready to submit, no errors

## Key Findings

| Finding | Implication |
|---------|-------------|
| Name corruption pattern | QBO recovery concatenating payloads |
| @mailinator test email | Intuit internal process leaked to environment |
| Spencer Hiko / Laura Frank | Created outside TBX flow - unknown source |
| TBX code OK | Not our bug |

## Documentation

Full worklog: `docs/WORKLOG_KEYSTONE_PAYROLL_DUPLICATION_2026-01-27.md`

## Related Issues

- PLA-3201 (IC Balance Sheet out of balance) - same environment family
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
    'query': query,
    'variables': {
        'input': {
            'teamId': 'fd21180c-8619-4014-98c6-ac9eb8d47975',
            'title': '[BUG] Keystone Construction - Employee Duplication in Payroll (RESOLVED)',
            'description': description,
            'labelIds': [
                'a270d38a-bb97-4240-9b75-05a316d24864',  # Bug
                '59234e85-ca51-4c41-8d94-7781ae2676b7',  # Customer Issues
            ],
            'priority': 2
        }
    }
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2))

if result.get('data', {}).get('issueCreate', {}).get('success'):
    issue = result['data']['issueCreate']['issue']
    print(f"\n✓ Ticket criado com sucesso!")
    print(f"  ID: {issue['identifier']}")
    print(f"  URL: {issue['url']}")
