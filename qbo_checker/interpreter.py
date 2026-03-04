# qbo_checker/interpreter.py
"""AI interpretation module for screenshot analysis and notes generation

Generates technical notes comparing screenshot evidence against feature requirements.
Notes follow TestBox professional style for Intuit communications.
"""

import base64
from pathlib import Path
from datetime import datetime


def encode_image(filepath: Path) -> str:
    """Encode image to base64 for API."""
    with open(filepath, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


# Feature-specific note templates for technical explanations
FEATURE_NOTE_TEMPLATES = {
    "Consolidated View": {
        "yes": "The consolidated multi-entity Fusion view is enabled and accessible. The screenshot shows the unified dashboard displaying data across all {company} entities with the 'Business at a glance' section visible, confirming the Fusion UI architecture is active.",
        "partial": "The Consolidated View UI is accessible but some elements may require additional configuration. Screenshot shows the current state for review.",
        "no": "Unable to access the Consolidated View. The Fusion multi-entity dashboard did not load as expected.",
    },
    "Reporting Enhancements": {
        "yes": "Reporting enhancements are fully functional in {project} {company}. The screenshot confirms access to Standard reports, KPI dashboards, and the ability to run consolidated reports across entities.",
        "partial": "The Reports page is accessible but some enhanced features may need verification. The screenshot shows the current reporting interface.",
        "no": "Unable to access the enhanced reporting features. The Standard reports page did not load correctly.",
    },
    "Intercompany Account Mapping": {
        "yes": "Intercompany account mapping interface is accessible in the Fusion multi-entity view. Users can configure IC mappings between {company} entities as shown in the screenshot.",
        "partial": "The Intercompany account mapping page is accessible but mappings may need configuration. If the banner 'Disabled target companies do not have mapping' appears, IC mappings need to be configured for all entities.",
        "no": "Unable to access Intercompany account mapping. The feature may require additional permissions.",
    },
    "Intercompany Expense Allocations": {
        "yes": "Intercompany expense allocations are active in the Fusion multi-entity view. From Consolidated View, users can access IC allocations under Accounting > Intercompany transactions.",
        "partial": "IC expense allocations UI is accessible but shows configuration warning. Could Intuit either grant permission to manage Intercompany account mappings, or configure the mappings for all {project} entities?",
        "no": "Unable to access Intercompany Expense Allocations feature.",
    },
    "Dynamic Allocations": {
        "yes": "Dynamic Allocations feature is fully functional. Users can create and manage dynamic allocation rules from the Consolidated View.",
        "partial": "Dynamic Allocation screen is accessible but shows banner about missing account mappings. Could you enable the 'Intercompany account mapping' permission or complete the mappings for all {project} entities?",
        "no": "Unable to access Dynamic Allocations feature.",
    },
    "Advanced Reporting": {
        "yes": "Advanced Reporting features are enabled and functional in {project} {company}. The screenshot shows access to visual customization, custom formulas, and management report capabilities.",
        "partial": "Advanced Reporting is partially accessible. Some features may require additional configuration or permissions.",
        "no": "Unable to access Advanced Reporting features.",
    },
    "KPIs": {
        "yes": "The KPI Library is working correctly. All native KPIs load as expected including Growth KPIs, Sales KPIs, Net Sales, and performance metrics.",
        "partial": "The KPI Library is accessible but KPIs requiring third-party data (Monday.com, CRM sources) are not available. Could you confirm if 3P integrations can be enabled or provide a preconfigured connection?",
        "no": "Unable to access the KPI Library.",
    },
}

# Default template for features not in the mapping
DEFAULT_NOTE_TEMPLATE = {
    "yes": "Feature '{feature_name}' is enabled and accessible in {project} {company}. The screenshot provides visual evidence of the feature working as expected per the Fall Release requirements.",
    "partial": "Feature '{feature_name}' is accessible but may require additional configuration or manual verification. See screenshot for current state.",
    "no": "Unable to access '{feature_name}'. The feature did not load as expected. May require feature flag activation or additional permissions.",
}


def get_feature_note(
    feature_name: str,
    status: str,
    project: str,
    company: str,
    feature_description: str = "",
) -> str:
    """Generate technical note based on feature type and status."""
    status_key = status.lower()
    if status_key not in ["yes", "partial", "no"]:
        status_key = "partial"

    # Find matching template
    template = None
    for key, templates in FEATURE_NOTE_TEMPLATES.items():
        if key.lower() in feature_name.lower():
            template = templates.get(status_key)
            break

    if not template:
        template = DEFAULT_NOTE_TEMPLATE.get(status_key, DEFAULT_NOTE_TEMPLATE["partial"])

    # Format template with variables
    note = template.format(feature_name=feature_name, project=project, company=company)

    return note


def interpret_screenshot(
    filepath: Path,
    feature_name: str,
    feature_description: str,
    project: str,
    company: str,
    nav_success: bool = True,
    nav_details: str = "",
) -> dict:
    """Generate status and technical notes based on navigation results."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if nav_success:
        status = "YES"
        intuit_notes = get_feature_note(feature_name, "YES", project, company, feature_description)
        internal_notes = (
            f"Auto-validated at {timestamp}. Navigation successful. {nav_details}. Screenshot saved as evidence."
        )
    else:
        status = "PARTIAL"
        intuit_notes = get_feature_note(feature_name, "PARTIAL", project, company, feature_description)
        internal_notes = f"Partial validation at {timestamp}. {nav_details}. Screenshot saved for manual review."

    return {
        "status": status,
        "intuit_notes": intuit_notes,
        "internal_notes": internal_notes,
    }


def generate_worklog_note(feature_name: str, status: str, action: str = "validated") -> str:
    """Generate a short worklog note."""
    return f"{action.capitalize()} {feature_name}, marked as {status}."
