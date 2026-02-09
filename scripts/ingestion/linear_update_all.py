import requests
import sys

sys.stdout.reconfigure(encoding="utf-8")

LINEAR_API_KEY = "REDACTED_LINEAR_KEY_1"
LINEAR_URL = "https://api.linear.app/graphql"

HEADERS = {"Content-Type": "application/json", "Authorization": LINEAR_API_KEY}


def graphql_request(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(LINEAR_URL, headers=HEADERS, json=payload)
    return response.json()


def get_issue_by_identifier(identifier):
    query = """
    query($term: String!) {
      searchIssues(term: $term, first: 1) {
        nodes { id identifier title url }
      }
    }
    """
    result = graphql_request(query, {"term": identifier})
    nodes = result.get("data", {}).get("searchIssues", {}).get("nodes", [])
    return nodes[0] if nodes else None


def update_issue(issue_id, description):
    mutation = """
    mutation($id: String!, $description: String!) {
      issueUpdate(id: $id, input: { description: $description }) {
        success
        issue { identifier title url }
      }
    }
    """
    return graphql_request(mutation, {"id": issue_id, "description": description})


def add_comment(issue_id, body):
    mutation = """
    mutation($issueId: String!, $body: String!) {
      commentCreate(input: { issueId: $issueId, body: $body }) {
        success
      }
    }
    """
    return graphql_request(mutation, {"issueId": issue_id, "body": body})


# Ticket descriptions
VENDORS_DESC = """# Vendors Ingestion - Keystone Construction
**Dataset ID:** `321c6fa0-a4ee-4e05-b085-7b4d51473495`

## 📦 File: `INGESTION_VENDORS_NEW.csv`

| Metric | Value |
|--------|-------|
| Records | 20 |
| ID Range | 34 → 53 |
| Location | `C:\\Users\\adm_r\\Downloads\\` |

---

## 🗂️ Vendors List

### IC Vendors (IDs 44-48)
- 44: KeyStone Canopy (IC Vendor)
- 45: KeyStone Ecocraft (IC Vendor)
- 46: Keystone Construction (Par.) (IC Vendor)
- 47: Keystone Construction (Par.) (IC Vendor) ( 356 )
- 48: Keystone Terra (Ch.) (IC Vendor)

### Regular Vendors (IDs 34-43, 49-53)
- 34: Abdi Structural Engineering
- 35: Al-Farsi Security Services
- 36: Andersen Lars
- 37: Blueshield
- 38: Daniel Green
- 39: Elite Contracting
- 40: HVAC Supply Store
- 41: Hassan Ahmed
- 42: Home Depot
- 43: John
- 49: Pakistani Insurance
- 50: Safety Equipment Inc.
- 51: Terzi
- 52: dougherty
- 53: samantha

---

## ⚠️ Dependency
Bills (332) depend on these vendors via `vendor_id` FK.
**Ingest vendors BEFORE bills!**

---

**Updated:** 2026-02-05 (WAR ROOM)
"""

CUSTOMERS_DESC = """# Customers Ingestion - Keystone Construction
**Dataset ID:** `321c6fa0-a4ee-4e05-b085-7b4d51473495`

## 📦 File: `INGESTION_CUSTOMERS_NEW.csv`

| Metric | Value |
|--------|-------|
| Records | 25 |
| ID Range | 51 → 75 |
| Location | `C:\\Users\\adm_r\\Downloads\\` |

---

## 🗂️ Customers List

### IC Customers (IDs 62-65)
- 62: KeyStone Canopy (IC Customer)
- 63: KeyStone Ironcraft (IC Customer) ( 358 )
- 64: KeyStone Volt (IC Customer)
- 65: Keystone Construction (Par.) (IC Customer) ( 354 )

### Project Customers
- 53: Azure Pines - Playground Construction
- 54: Azure Pines - Playground Construction 2022
- 55: BMH Landscaping 2025
- 59: GaleGuardian - Turbine Installation
- 61: Intuit Dome
- 67: Leap Labs - Solar Array Installation
- 71: TidalWave - Farmer's Market (Lot Build)
- 72: TidalWave - Farmer's Market (Lot Build) 2024

### Regular Customers
- 51: Alan Brown
- 52: Austin Enterprise
- 56: Casa Bonita
- 57: Construction- Test Delete
- 58: Donald Duck
- 60: Government Agency
- 66: La Hacienda Event Center
- 68: Lot Clearing
- 69: Maintenance
- 70: Meredith Walker
- 73: Trent Kennedy
- 74: Walker Draperies - Jacqueline Brinkerhoff
- 75: Wezlee Norriz

---

## ⚠️ Dependency
Invoices (243) depend on these customers via `customer_id` FK.
**Ingest customers BEFORE invoices!**

---

**Updated:** 2026-02-05 (WAR ROOM)
"""

INVOICES_DESC = """# Invoices Ingestion - Keystone Construction
**Dataset ID:** `321c6fa0-a4ee-4e05-b085-7b4d51473495`

## 📦 File: `INGESTION_INVOICES.csv`

| Metric | Value |
|--------|-------|
| Records | 243 |
| ID Range | 2460 → 2702 |
| Location | `C:\\Users\\adm_r\\Downloads\\` |

---

## 📊 Invoices by Company

| Company | Invoices |
|---------|----------|
| Keystone Terra (Ch.) | 117 |
| Keystone Construction (Par) | 64 |
| Keystone BlueCraft | 60 |
| KeyStone Volt | 1 |
| KeyStone Canopy | 1 |
| **TOTAL** | **243** |

---

## IC vs Regular

| Type | Count |
|------|-------|
| Regular Invoices | 235 |
| IC Invoices | 8 |

---

## 🏆 Top Customers by Amount
1. Intuit Dome - $17.3M
2. BMH Landscaping 2025 - $11.6M
3. GaleGuardian - Turbine Installation - $4.6M
4. Azure Pines - Playground Construction - $4.3M
5. TidalWave - Farmer's Market - $2.7M

---

## ⚠️ Dependency
Requires `INGESTION_CUSTOMERS_NEW.csv` ingested first!
FK: `customer_id` → `customers.id`

---

**Updated:** 2026-02-05 (WAR ROOM)
"""


def main():
    print("=" * 70)
    print("UPDATING ALL RELATED TICKETS")
    print("=" * 70)

    updates = [
        ("PLA-3253", VENDORS_DESC, "Vendors"),
        ("PLA-3252", CUSTOMERS_DESC, "Customers"),
        ("PLA-3257", INVOICES_DESC, "Invoices IC"),
    ]

    for identifier, description, name in updates:
        print(f"\n📝 Updating {identifier} ({name})...")
        issue = get_issue_by_identifier(identifier)
        if issue:
            result = update_issue(issue["id"], description)
            if result.get("data", {}).get("issueUpdate", {}).get("success"):
                print(f"  ✅ Updated {identifier}")
            else:
                print(f"  ❌ Failed: {result}")
        else:
            print("  ❌ Ticket not found")

    print("\n" + "=" * 70)
    print("ALL TICKETS UPDATED!")
    print("=" * 70)
    print("""
Summary of all tickets:

PHASE 1 (Master Data):
- PLA-3253: Vendors (20 records, IDs 34-53)
- PLA-3252: Customers (25 records, IDs 51-75)

PHASE 2 (Transactions):
- PLA-3258: Bills (332 records, IDs 105-436)
- PLA-3257: Invoices (243 records, IDs 2460-2702)

BACKLOG:
- PLA-3264: New Employees (pending QBO IDs)
- PLA-3261: Time Entries (depends on employees)
""")


if __name__ == "__main__":
    main()
