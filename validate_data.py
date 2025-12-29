"""
Data Validation Script for Winter Release FY26
Validates data prerequisites for each feature by querying the QBO dataset
"""

import pandas as pd
import os

# Load the Excel with all QBO data
EXCEL_PATH = r"C:\Users\adm_r\GOD_EXTRACT\QBO_DATABASE_COMPLETO.xlsx"
OUTPUT_PATH = r"C:\Users\adm_r\intuit-boom\docs\DATA_VALIDATION_RESULTS.csv"


def count_rows_in_sheet(excel_path, sheet_name):
    """Count rows in a specific Excel sheet"""
    try:
        df_full = pd.read_excel(excel_path, sheet_name=sheet_name)
        return len(df_full)
    except Exception:
        return 0


def get_sheet_names(excel_path):
    """Get all sheet names from Excel file"""
    try:
        xl = pd.ExcelFile(excel_path)
        return xl.sheet_names
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return []


def validate_feature_data(feature_id, tables, excel_path, sheets):
    """Validate if data exists for a feature"""
    results = []
    total_rows = 0
    tables_found = 0

    for table in tables:
        # Map table name to sheet name (remove 'quickbooks_' prefix)
        sheet_candidates = [
            table,
            table.replace("quickbooks_", ""),
            table.replace("_", " ").title().replace(" ", ""),
        ]

        found = False
        for sheet in sheets:
            sheet_lower = sheet.lower().replace("_", "").replace(" ", "")
            for candidate in sheet_candidates:
                cand_lower = candidate.lower().replace("_", "").replace(" ", "")
                if cand_lower in sheet_lower or sheet_lower in cand_lower:
                    try:
                        df = pd.read_excel(excel_path, sheet_name=sheet)
                        rows = len(df)
                        total_rows += rows
                        tables_found += 1
                        results.append(f"{sheet}: {rows} rows")
                        found = True
                        break
                    except Exception:
                        pass
            if found:
                break

        if not found:
            results.append(f"{table}: NOT FOUND")

    # Determine data check result
    if tables_found == 0:
        data_result = "Missing"
    elif total_rows == 0:
        data_result = "Weak"
    elif total_rows < 10:
        data_result = "Weak"
    elif total_rows >= 10 and tables_found == len(tables):
        data_result = "Strong"
    else:
        data_result = "Inconclusive"

    return data_result, total_rows, "; ".join(results)


# Feature to table mapping
feature_tables = {
    "WR-001": ["quickbooks_bank_transactions"],
    "WR-002": ["quickbooks_invoices"],
    "WR-003": ["quickbooks_projects", "quickbooks_project_budgets"],
    "WR-004": ["quickbooks_chart_of_accounts", "quickbooks_invoices"],
    "WR-005": ["quickbooks_dimensions"],
    "WR-006": ["quickbooks_customers"],
    "WR-007": [],  # Beta - UI only
    "WR-008": ["quickbooks_custom_reports"],
    "WR-009": ["quickbooks_custom_report_templates"],
    "WR-010": ["quickbooks_custom_reports"],
    "WR-011": [],  # 3P integration - UI only
    "WR-012": ["quickbooks_custom_report_templates"],
    "WR-013": ["quickbooks_custom_reports"],
    "WR-014": [],  # Benchmarking - external service
    "WR-015": ["quickbooks_intercompany_journal_entry"],
    "WR-016": ["quickbooks_dimensions", "quickbooks_product_services_classifications"],
    "WR-017": ["quickbooks_dimensions"],
    "WR-018": ["quickbooks_workflow_automations"],
    "WR-019": ["quickbooks_chart_of_accounts"],
    "WR-020": ["quickbooks_workflow_automations"],
    "WR-021": [],  # Migration - fresh tenant
    "WR-022": [],  # Migration - fresh tenant
    "WR-023": [],  # Documentation
    "WR-024": ["quickbooks_payroll_expenses"],
    "WR-025": ["quickbooks_invoices", "quickbooks_estimates"],
    "WR-026": ["quickbooks_employees"],
    "WR-027": ["quickbooks_employees"],
    "WR-028": ["quickbooks_time_entries"],
    "WR-029": ["quickbooks_payroll_expenses"],
}


def main():
    print("=" * 60)
    print("DATA VALIDATION - Winter Release FY26")
    print("=" * 60)

    # Check if Excel file exists
    if not os.path.exists(EXCEL_PATH):
        print(f"ERROR: Excel file not found at {EXCEL_PATH}")
        return

    # Get sheet names
    print(f"\nReading Excel file: {EXCEL_PATH}")
    sheets = get_sheet_names(EXCEL_PATH)
    print(f"Found {len(sheets)} sheets")

    # Validate each feature
    results = []
    for feature_id, tables in feature_tables.items():
        if not tables:
            # UI-only or N/A features
            data_result = "NotApplicable"
            total_rows = 0
            details = "UI-only or external service"
        else:
            data_result, total_rows, details = validate_feature_data(
                feature_id, tables, EXCEL_PATH, sheets
            )

        results.append(
            {
                "Feature_id": feature_id,
                "Tables_checked": ", ".join(tables) if tables else "N/A",
                "Data_check_result": data_result,
                "Row_count": total_rows,
                "Details": details,
            }
        )

        status_icon = {
            "Strong": "[OK]",
            "Weak": "[!]",
            "Missing": "[X]",
            "Inconclusive": "[?]",
            "NotApplicable": "[-]",
        }.get(data_result, "[?]")

        print(f"{status_icon} {feature_id}: {data_result} ({total_rows} rows)")

    # Save results
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nResults saved to: {OUTPUT_PATH}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    summary = df["Data_check_result"].value_counts()
    for status, count in summary.items():
        print(f"  {status}: {count}")


if __name__ == "__main__":
    main()
