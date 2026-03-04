# TCO Project Company IDs
# For use with https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId=<ID>
#
# Discovered by capturing cookies during company switching:
# - qbo.currentcompanyid cookie stores the current company ID
#
# Usage:
#   page.goto(f'https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={TCO_COMPANY_IDS["apex"]}')

TCO_COMPANY_IDS = {
    # Company IDs discovered from browser sessions
    "consolidated": "9341455649090852",  # Vista consolidada (Multi-entity consolidated view)
    "global": "9341455130196737",  # Global (captured from API request)
    "apex": "9341455130166501",  # Apex Tire (captured from cookie before Global switch)
    # "traction": "PENDING",  # Traction Control Outfitters, LLC - needs to be captured
}

# Company names mapping
TCO_COMPANY_NAMES = {
    "consolidated": "Vista consolidada",
    "global": "Global",
    "apex": "Apex Tire",
    "traction": "Traction Control Outfitters, LLC",
}


def get_switch_url(company_key):
    """Get the URL to switch to a specific company.

    Args:
        company_key: One of 'consolidated', 'global', 'apex', 'traction'

    Returns:
        URL string or None if company ID not known
    """
    company_id = TCO_COMPANY_IDS.get(company_key)
    if company_id and company_id != "PENDING":
        return f"https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={company_id}"
    return None
