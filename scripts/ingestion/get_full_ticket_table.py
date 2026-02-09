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


def search_all_tickets():
    """Search for all Keystone/QBO ingestion tickets"""
    query = """
    {
      searchIssues(term: "QuickBooks Dataset Ingestion", first: 50) {
        nodes {
          id
          identifier
          title
          url
          state { name type }
        }
      }
    }
    """
    result = graphql_request(query)
    return result.get("data", {}).get("searchIssues", {}).get("nodes", [])


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
        }
      }
    }
    """
    result = graphql_request(query, {"term": identifier})
    nodes = result.get("data", {}).get("searchIssues", {}).get("nodes", [])
    return nodes[0] if nodes else None


def main():
    # All tickets for this project
    ticket_ids = [
        "PLA-3251",  # Employees
        "PLA-3252",  # Customers
        "PLA-3253",  # Vendors
        "PLA-3254",  # Chart of Accounts
        "PLA-3255",  # Products/Services (if exists)
        "PLA-3256",  # Classifications (if exists)
        "PLA-3257",  # Invoices IC
        "PLA-3258",  # Bills IC
        "PLA-3259",  # Expenses (if exists)
        "PLA-3260",  # Bank Transactions (if exists)
        "PLA-3261",  # Time Entries
        "PLA-3262",  # Projects (if exists)
        "PLA-3263",  # Estimates (if exists)
        "PLA-3264",  # New Employees
        "PLA-3212",  # Winter Release Staging
    ]

    print("Fetching tickets...\n")

    tickets = []
    for tid in ticket_ids:
        ticket = get_ticket(tid)
        if ticket:
            tickets.append(ticket)

    # Manual status mapping based on what we know
    status_map = {
        "PLA-3251": {"manual": "✅ Sim", "ingestion": "⏳ Parcial (44/58)"},
        "PLA-3252": {"manual": "⏳ Não", "ingestion": "⏳ Parcial (50/75)"},
        "PLA-3253": {"manual": "✅ Sim", "ingestion": "⏳ Parcial (33/53)"},
        "PLA-3254": {"manual": "❓", "ingestion": "✅ OK (121)"},
        "PLA-3255": {"manual": "❓", "ingestion": "❓"},
        "PLA-3256": {"manual": "❓", "ingestion": "✅ OK (37)"},
        "PLA-3257": {"manual": "⏳ Não", "ingestion": "⏳ Parcial (93/243)"},
        "PLA-3258": {"manual": "⏳ Não", "ingestion": "⏳ Parcial (26/332)"},
        "PLA-3259": {"manual": "❓", "ingestion": "❓"},
        "PLA-3260": {"manual": "⏳ Não", "ingestion": "⏳ Parcial (56/5087)"},
        "PLA-3261": {"manual": "⏳ Não", "ingestion": "⏳ Aguarda Employees"},
        "PLA-3262": {"manual": "❓", "ingestion": "✅ OK (8)"},
        "PLA-3263": {"manual": "❓", "ingestion": "✅ OK (8)"},
        "PLA-3264": {"manual": "⏳ Backlog", "ingestion": "⏳ Pendente"},
        "PLA-3212": {"manual": "N/A", "ingestion": "N/A"},
    }

    # Sort by identifier
    tickets.sort(key=lambda x: x["identifier"])

    # Print table
    print("\n## 📋 Tickets do Projeto de Ingestão - Keystone Construction\n")
    print("| Ticket | Status | Manual | Ingestion |")
    print("|--------|--------|--------|-----------|")

    for t in tickets:
        identifier = t["identifier"]
        title = (
            t["title"]
            .replace("[QuickBooks] ", "")
            .replace("Dataset Ingestion - ", "")
            .replace("Dataset ", "")
        )
        url = t["url"]
        state = t["state"]["name"]

        status = status_map.get(identifier, {"manual": "❓", "ingestion": "❓"})
        manual = status["manual"]
        ingestion = status["ingestion"]

        # Create hyperlink
        link = f"[{identifier} - {title[:35]}]({url})"

        print(f"| {link} | {state} | {manual} | {ingestion} |")


if __name__ == "__main__":
    main()
