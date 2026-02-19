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


def get_ticket(identifier):
    query = """
    query($term: String!) {
      searchIssues(term: $term, first: 1) {
        nodes {
          id
          identifier
          title
          url
          state { name type }
          labels { nodes { name } }
          assignee { name }
        }
      }
    }
    """
    result = graphql_request(query, {"term": identifier})
    nodes = result.get("data", {}).get("searchIssues", {}).get("nodes", [])
    return nodes[0] if nodes else None


def main():
    # All relevant tickets for Keystone ingestion
    ticket_ids = [
        "PLA-3251",  # Employees
        "PLA-3252",  # Customers
        "PLA-3253",  # Vendors
        "PLA-3254",  # Chart of Accounts
        "PLA-3257",  # Invoices IC
        "PLA-3258",  # Bills IC
        "PLA-3261",  # Time Entries
        "PLA-3264",  # New Employees
    ]

    print("Fetching ticket status from Linear...\n")

    tickets = []
    for tid in ticket_ids:
        ticket = get_ticket(tid)
        if ticket:
            tickets.append(ticket)
            print(f"  ✅ {tid}: {ticket['title'][:40]}...")
        else:
            print(f"  ❌ {tid}: Not found")

    # Output as markdown table
    print("\n\n" + "=" * 100)
    print("MARKDOWN TABLE FOR USER")
    print("=" * 100 + "\n")

    print("| Ticket | Entidade | Status Linear | Ingestão Manual | Ingestão Dataset |")
    print("|--------|----------|---------------|-----------------|------------------|")

    for t in tickets:
        identifier = t["identifier"]
        title = (
            t["title"]
            .replace("[QuickBooks] Dataset Ingestion - ", "")
            .replace("[QuickBooks] ", "")[:30]
        )
        url = t["url"]
        state = t["state"]["name"]

        # Determine manual/dataset status based on what we know
        manual_status = "❓"
        dataset_status = "❓"

        if identifier == "PLA-3251":  # Employees
            manual_status = "✅ Alexandra fazendo"
            dataset_status = "44 de 58"
        elif identifier == "PLA-3252":  # Customers
            manual_status = "⏳ Pendente"
            dataset_status = "50 de 75 (CSV pronto)"
        elif identifier == "PLA-3253":  # Vendors
            manual_status = "✅ Alexandra fazendo"
            dataset_status = "33 de 53 (CSV pronto)"
        elif identifier == "PLA-3254":  # CoA
            manual_status = "❓"
            dataset_status = "121 (OK)"
        elif identifier == "PLA-3257":  # Invoices
            manual_status = "⏳ Pendente"
            dataset_status = "93 de 243 (CSV pronto)"
        elif identifier == "PLA-3258":  # Bills
            manual_status = "⏳ Pendente"
            dataset_status = "26 de 332 (CSV pronto)"
        elif identifier == "PLA-3261":  # Time Entries
            manual_status = "⏳ Aguarda Employees"
            dataset_status = "6708 (+ 80 pendentes)"
        elif identifier == "PLA-3264":  # New Employees
            manual_status = "⏳ Backlog"
            dataset_status = "4 novos pendentes"

        print(
            f"| [{identifier}]({url}) | {title} | {state} | {manual_status} | {dataset_status} |"
        )

    # Also output raw data for reference
    print("\n\n" + "=" * 100)
    print("RAW TICKET DATA")
    print("=" * 100 + "\n")

    for t in tickets:
        labels = [lb["name"] for lb in t.get("labels", {}).get("nodes", [])]
        assignee = t.get("assignee", {})
        assignee_name = assignee.get("name", "Unassigned") if assignee else "Unassigned"
        print(f"{t['identifier']}: {t['title']}")
        print(f"  URL: {t['url']}")
        print(f"  State: {t['state']['name']} ({t['state']['type']})")
        print(f"  Assignee: {assignee_name}")
        print(f"  Labels: {labels}")
        print()


if __name__ == "__main__":
    main()
