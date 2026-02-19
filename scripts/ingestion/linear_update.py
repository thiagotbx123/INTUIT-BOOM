import os
import requests
import sys

sys.stdout.reconfigure(encoding="utf-8")

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY", "")
LINEAR_URL = "https://api.linear.app/graphql"

HEADERS = {"Content-Type": "application/json", "Authorization": LINEAR_API_KEY}


def graphql_request(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(LINEAR_URL, headers=HEADERS, json=payload)
    return response.json()


def search_tickets(search_term):
    """Search for tickets"""
    query = """
    query($term: String!) {
      searchIssues(term: $term, first: 20) {
        nodes {
          id
          identifier
          title
          state { name }
          description
        }
      }
    }
    """
    result = graphql_request(query, {"term": search_term})
    return result.get("data", {}).get("searchIssues", {}).get("nodes", [])


def get_issue_by_identifier(identifier):
    """Get issue by identifier like PLA-3258"""
    query = """
    query($term: String!) {
      searchIssues(term: $term, first: 1) {
        nodes {
          id
          identifier
          title
          state { name }
          description
          url
        }
      }
    }
    """
    result = graphql_request(query, {"term": identifier})
    nodes = result.get("data", {}).get("searchIssues", {}).get("nodes", [])
    return nodes[0] if nodes else None


def update_issue(issue_id, description):
    """Update issue description"""
    mutation = """
    mutation($id: String!, $description: String!) {
      issueUpdate(id: $id, input: { description: $description }) {
        success
        issue {
          identifier
          title
          url
        }
      }
    }
    """
    result = graphql_request(mutation, {"id": issue_id, "description": description})
    return result


def add_comment(issue_id, body):
    """Add comment to issue"""
    mutation = """
    mutation($issueId: String!, $body: String!) {
      commentCreate(input: { issueId: $issueId, body: $body }) {
        success
        comment {
          id
        }
      }
    }
    """
    result = graphql_request(mutation, {"issueId": issue_id, "body": body})
    return result


def main():
    print("=" * 70)
    print("LINEAR TICKET UPDATE")
    print("=" * 70)

    # Search for Keystone/ingestion related tickets
    print("\n🔍 Searching for existing tickets...")

    search_terms = [
        "Keystone ingestion",
        "PLA-3258",
        "PLA-3261",
        "PLA-3264",
        "Bills IC",
        "Dataset",
    ]

    found_tickets = {}
    for term in search_terms:
        results = search_tickets(term)
        for r in results:
            if r["identifier"] not in found_tickets:
                found_tickets[r["identifier"]] = r
                print(f"  Found: {r['identifier']} - {r['title'][:50]}...")

    # Get specific tickets
    print("\n📋 Getting specific tickets...")

    ticket_ids = ["PLA-3258", "PLA-3261", "PLA-3264"]
    tickets = {}

    for tid in ticket_ids:
        issue = get_issue_by_identifier(tid)
        if issue:
            tickets[tid] = issue
            print(f"  ✅ {tid}: {issue['title'][:50]}...")
        else:
            print(f"  ❌ {tid}: Not found")

    # Update PLA-3258 (Bills IC) with complete info
    if "PLA-3258" in tickets:
        print("\n📝 Updating PLA-3258 (Bills IC)...")

        new_description = """# Bills IC + Full Bills Ingestion
## Keystone Construction Dataset

**Dataset ID:** `321c6fa0-a4ee-4e05-b085-7b4d51473495`

---

## 📦 Files Ready for Ingestion

### Phase 1: Master Data (Ingest First!)
| File | Records | ID Range |
|------|---------|----------|
| `INGESTION_VENDORS_NEW.csv` | 20 | 34-53 |
| `INGESTION_CUSTOMERS_NEW.csv` | 25 | 51-75 |

### Phase 2: Bills & Invoices
| File | Records | ID Range |
|------|---------|----------|
| `INGESTION_BILLS.csv` | 332 | 105-436 |
| `INGESTION_INVOICES.csv` | 243 | 2460-2702 |

---

## 🔗 FK Dependencies
```
vendors.id ←── bills.vendor_id
customers.id ←── invoices.customer_id
```

**⚠️ IMPORTANT:** Ingest Phase 1 before Phase 2!

---

## 📊 Bills Breakdown

| Company | Bills |
|---------|-------|
| Keystone Construction (Par) | 188 |
| Keystone Terra (Ch.) | 127 |
| KeyStone Canopy | 8 |
| Keystone BlueCraft | 5 |
| KeyStone Stonecraft | 3 |
| KeyStone Ecocraft | 1 |
| **TOTAL** | **332** |

### IC Bills: 16
### Regular Bills: 316

---

## 🗂️ IC Vendors Added (IDs 44-48)
- KeyStone Canopy (IC Vendor)
- KeyStone Ecocraft (IC Vendor)
- Keystone Construction (Par.) (IC Vendor)
- Keystone Construction (Par.) (IC Vendor) ( 356 )
- Keystone Terra (Ch.) (IC Vendor)

---

## 📁 Files Location
`C:\\Users\\adm_r\\Downloads\\`

**Updated:** 2026-02-05 (WAR ROOM session)
"""

        result = update_issue(tickets["PLA-3258"]["id"], new_description)
        if result.get("data", {}).get("issueUpdate", {}).get("success"):
            print("  ✅ Updated PLA-3258")
        else:
            print(f"  ❌ Failed: {result}")

    # Update PLA-3264 (Employees) with comment
    if "PLA-3264" in tickets:
        print("\n📝 Adding comment to PLA-3264 (Employees)...")

        comment = """## Update 2026-02-05 (WAR ROOM)

FK Dependencies resolved for Bills/Invoices ingestion.

### Related Files Generated:
- `INGESTION_VENDORS_NEW.csv` (20 vendors, IDs 34-53)
- `INGESTION_CUSTOMERS_NEW.csv` (25 customers, IDs 51-75)
- `INGESTION_BILLS.csv` (332 bills, IDs 105-436)
- `INGESTION_INVOICES.csv` (243 invoices, IDs 2460-2702)

**Note:** Time entries for new employees (PLA-3261) still pending employee IDs from QBO.
"""

        result = add_comment(tickets["PLA-3264"]["id"], comment)
        if result.get("data", {}).get("commentCreate", {}).get("success"):
            print("  ✅ Added comment to PLA-3264")
        else:
            print(f"  ❌ Failed: {result}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
Tickets Updated:
- PLA-3258: Bills IC + Full ingestion details
- PLA-3264: Added comment with update

Files in Downloads ready for Engineering:
1. INGESTION_VENDORS_NEW.csv (20 records, IDs 34-53)
2. INGESTION_CUSTOMERS_NEW.csv (25 records, IDs 51-75)
3. INGESTION_BILLS.csv (332 records, IDs 105-436)
4. INGESTION_INVOICES.csv (243 records, IDs 2460-2702)
""")


if __name__ == "__main__":
    main()
