"""
Create Master Validation Sheet for Winter Release FY26
"""

import pandas as pd
import json

# Load existing feature tracker
with open(r"C:\Users\adm_r\intuit-boom\qbo_checker\features_winter.json", "r") as f:
    data = json.load(f)

features = data["features"]

# Data check mappings - which tables prove the feature prerequisite exists
data_signals = {
    "WR-001": {
        "signal": "quickbooks_bank_transactions",
        "steps": "SELECT COUNT(*) FROM quickbooks_bank_transactions WHERE status IS NOT NULL",
    },
    "WR-002": {
        "signal": "quickbooks_invoices + tax",
        "steps": "Check invoices with tax amounts > 0",
    },
    "WR-003": {
        "signal": "quickbooks_projects, quickbooks_project_budgets",
        "steps": "SELECT COUNT(*) FROM quickbooks_projects; SELECT COUNT(*) FROM quickbooks_project_budgets",
    },
    "WR-004": {
        "signal": "quickbooks_chart_of_accounts, quickbooks_invoices",
        "steps": "Financial data exists in CoA and transactions",
    },
    "WR-005": {
        "signal": "quickbooks_dimensions",
        "steps": "SELECT COUNT(*) FROM quickbooks_dimensions",
    },
    "WR-006": {
        "signal": "quickbooks_customers",
        "steps": "SELECT COUNT(*) FROM quickbooks_customers WHERE email IS NOT NULL",
    },
    "WR-007": {
        "signal": "N/A - Beta feature",
        "steps": "Check Intuit Assist icon visibility",
    },
    "WR-008": {
        "signal": "quickbooks_custom_reports",
        "steps": "Check reports with AI interface",
    },
    "WR-009": {
        "signal": "quickbooks_custom_report_templates",
        "steps": "SELECT COUNT(*) FROM quickbooks_custom_report_templates",
    },
    "WR-010": {
        "signal": "quickbooks_custom_reports",
        "steps": "Dashboard data in custom reports",
    },
    "WR-011": {
        "signal": "N/A - 3P integration",
        "steps": "Check Apps marketplace for connected apps",
    },
    "WR-012": {
        "signal": "quickbooks_custom_report_templates",
        "steps": "Reports with calculated fields",
    },
    "WR-013": {
        "signal": "quickbooks_custom_reports",
        "steps": "Management report templates exist",
    },
    "WR-014": {
        "signal": "N/A - Benchmarking service",
        "steps": "Industry comparison data",
    },
    "WR-015": {
        "signal": "quickbooks_intercompany_journal_entry",
        "steps": "SELECT COUNT(*) FROM quickbooks_intercompany_journal_entry",
    },
    "WR-016": {
        "signal": "quickbooks_dimensions, quickbooks_product_services_classifications",
        "steps": "SELECT COUNT(*) FROM quickbooks_dimensions; SELECT COUNT(*) FROM quickbooks_product_services_classifications",
    },
    "WR-017": {
        "signal": "quickbooks_dimensions hierarchy",
        "steps": "Dimensions with parent/child relationships",
    },
    "WR-018": {
        "signal": "quickbooks_workflow_automations",
        "steps": "SELECT COUNT(*) FROM quickbooks_workflow_automations",
    },
    "WR-019": {
        "signal": "quickbooks_chart_of_accounts + dimensions",
        "steps": "BS accounts with dimension tags",
    },
    "WR-020": {
        "signal": "quickbooks_workflow_automations",
        "steps": "Approval workflows configured",
    },
    "WR-021": {"signal": "N/A - Migration feature", "steps": "Fresh tenant required"},
    "WR-022": {"signal": "N/A - Migration feature", "steps": "DFY setup wizard"},
    "WR-023": {"signal": "N/A - Documentation", "steps": "Compatibility docs review"},
    "WR-024": {
        "signal": "quickbooks_payroll_expenses",
        "steps": "SELECT COUNT(*) FROM quickbooks_payroll_expenses",
    },
    "WR-025": {
        "signal": "quickbooks_invoices, quickbooks_estimates",
        "steps": "Sales order flow in transactions",
    },
    "WR-026": {
        "signal": "quickbooks_employees (multi-entity)",
        "steps": "Employees across multiple entities",
    },
    "WR-027": {
        "signal": "quickbooks_employees payroll",
        "steps": "Employee garnishment deductions",
    },
    "WR-028": {
        "signal": "quickbooks_time_entries",
        "steps": "SELECT COUNT(*) FROM quickbooks_time_entries WHERE project_id IS NOT NULL",
    },
    "WR-029": {
        "signal": "quickbooks_payroll_expenses (CA)",
        "steps": "CA-specific payroll amendments",
    },
}

# Expected behaviors
expected_behaviors = {
    "WR-001": "AI suggests categories for bank transactions, batch posting available, anomaly detection flags unusual items",
    "WR-002": "Pre-file check identifies discrepancies between P&L and Sales Tax Liability, AI explains issues",
    "WR-003": "AI assists with project budget creation, profitability analysis, and closing summaries",
    "WR-004": "Finance AI provides KPI summary, budget analysis, and monthly insights",
    "WR-005": "Dimensions widget appears in Business Feed with IES-exclusive recommendations",
    "WR-006": "Import leads from Gmail/Outlook, draft estimates and email responses via AI",
    "WR-007": "Intuit Assist conversational interface available for cross-product queries",
    "WR-008": "Natural language queries generate reports with AI-powered insights",
    "WR-009": "Custom KPI formulas with library of 27+ metrics, KPI Scorecard view",
    "WR-010": "Pre-built and custom dashboards with visual analytics",
    "WR-011": "CRM data integration from Salesforce, HubSpot, Monday.com for cross-platform KPIs",
    "WR-012": "Formula builder for custom calculations in reports",
    "WR-013": "Combined financial statements with custom text, formatting, publish/share",
    "WR-014": "Industry benchmarks for performance comparison",
    "WR-015": "Consolidated reporting across entities with intercompany eliminations",
    "WR-016": "AI-suggested dimension values with sparkle icon, bulk assignment UI",
    "WR-017": "Roll-up reporting by dimension hierarchy with drill-down",
    "WR-018": "Dimension-based workflow triggers and conditions",
    "WR-019": "Balance Sheet filterable by dimension values",
    "WR-020": "Multiple simultaneous approvers in parallel approval paths",
    "WR-021": "Seamless Desktop to QBO migration with PBB customer support",
    "WR-022": "Done-For-You migration with guided setup",
    "WR-023": "Desktop feature parity documentation available",
    "WR-024": "WH-347 format Certified Payroll Report for government projects",
    "WR-025": "Sales order creation with order-to-invoice flow",
    "WR-026": "Centralized employee management across entities",
    "WR-027": "Child support garnishment with automatic deductions",
    "WR-028": "Assignment field in time entries for project/task tracking",
    "WR-029": "CA-specific amendment handling with enhanced correction workflow",
}

# Evidence requirements
evidence_types = {
    "WR-001": "Print,Query",
    "WR-002": "Print,Query",
    "WR-003": "Print,Query",
    "WR-004": "Print",
    "WR-005": "Print",
    "WR-006": "Print",
    "WR-007": "Print",
    "WR-008": "Print",
    "WR-009": "Print,Query",
    "WR-010": "Print",
    "WR-011": "Print",
    "WR-012": "Print",
    "WR-013": "Print",
    "WR-014": "Print",
    "WR-015": "Print,Query",
    "WR-016": "Print,Query",
    "WR-017": "Print,Query",
    "WR-018": "Print,Query",
    "WR-019": "Print",
    "WR-020": "Print,Config",
    "WR-021": "Print",
    "WR-022": "Print",
    "WR-023": "Export",
    "WR-024": "Print,Query",
    "WR-025": "Print",
    "WR-026": "Print,Query",
    "WR-027": "Print,Config",
    "WR-028": "Print,Query",
    "WR-029": "Print,Config",
}

# Create master validation sheet
rows = []
for f in features:
    ref = f["ref"]
    ds = data_signals.get(ref, {"signal": "TBD", "steps": "TBD"})
    row = {
        "Feature_id": ref,
        "Feature_name": f["name"],
        "Product_area": f["category"],
        "Tenant_or_Env": ",".join(f["environment"]),
        "Priority": f["priority"],
        "Expected_behavior": expected_behaviors.get(ref, ""),
        "Preconditions": f.get("setup_details", "") or "No setup needed",
        "UI_check_steps": " > ".join(f["navigation"].get("steps", [])),
        "UI_check_result": "Pass" if f["validation"].get("status") == "pass" else "",
        "Data_check_signal": ds["signal"],
        "Data_check_steps": ds["steps"],
        "Data_check_result": "",
        "Evidence_required": evidence_types.get(ref, "Print"),
        "Evidence_links": "",
        "Notes": f["validation"].get("notes", ""),
        "Final_status": "",
        "Action_recommendation": "",
        "Ticket_link_if_any": "",
    }
    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(
    r"C:\Users\adm_r\intuit-boom\docs\WINTER_RELEASE_MASTER_VALIDATION.csv", index=False
)
df.to_excel(
    r"C:\Users\adm_r\intuit-boom\docs\WINTER_RELEASE_MASTER_VALIDATION.xlsx",
    index=False,
)
print(f"Master validation sheet created with {len(rows)} features")
print("Files: WINTER_RELEASE_MASTER_VALIDATION.csv and .xlsx")
