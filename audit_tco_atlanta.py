# -*- coding: utf-8 -*-
"""
TCO (Apex Tire) - Atlanta Demo Audit
Audits all 5 entities across 10 stations each.
Uses existing qbo_checker/login.py infrastructure.
"""

import sys

sys.stdout.reconfigure(encoding="utf-8")

import json
import time
import re
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from qbo_checker.login import start_round, is_in_qbo, ACCOUNTS

# ============================================================
# CONFIG
# ============================================================
PROJECT = "TCO"
SCREENSHOT_DIR = Path(r"C:\Users\adm_r\Downloads\TCO_AUDIT_SCREENSHOTS")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = Path(r"C:\Users\adm_r\Downloads\TCO_AUDIT_UI_REPORT_2026-02-26.md")

# Entity mapping: key -> (company_key_for_url, display_name, db_company_type)
ENTITIES = {
    "apex": {
        "key": "apex",
        "company_id": "9341455130166501",
        "name": "Apex Tire & Auto Retail, LLC",
        "db_type": "main_child",
        "role": "Parent (Retail)",
    },
    "global": {
        "key": "global",
        "company_id": "9341455130196737",
        "name": "Global Tread Distributors, LLC",
        "db_type": "child_3",
        "role": "Child (Wholesale)",
    },
    "traction": {
        "key": "traction",
        "company_id": "9341455130188547",
        "name": "Traction Control Outfitters, LLC",
        "db_type": "parent",
        "role": "Child (Specialty)",
    },
    "roadready": {
        "key": "roadready",
        "company_id": "9341455130170608",
        "name": "RoadReady Service Solutions, LLC",
        "db_type": "secondary_child",
        "role": "Child (Fleet Service)",
    },
    "consolidated": {
        "key": "consolidated",
        "company_id": "9341455649090852",
        "name": "Consolidated View (Vista Consolidada)",
        "db_type": "all",
        "role": "Consolidated View",
    },
}

# Update ACCOUNTS with all company IDs (some may be missing)
ACCOUNTS["TCO"]["company_ids"] = {
    "apex": "9341455130166501",
    "global": "9341455130196737",
    "traction": "9341455130188547",
    "roadready": "9341455130170608",
    "consolidated": "9341455649090852",
}

# Also update the TCO DEMO account credentials if needed
# The plan says: quickbooks-tco-tbxdemo@tbxofficial.com / TestBox!23 / UGGQO4EAKKZTOK7XVXGOXHLUYZHBDXV7
# But login.py has a different email. Let's add TCO_DEMO as alternate.
ACCOUNTS["TCO_DEMO"] = {
    "name": "TCO DEMO",
    "email": "quickbooks-tco-tbxdemo@tbxofficial.com",
    "password": "TestBox!23",
    "totp_secret": "UGGQO4EAKKZTOK7XVXGOXHLUYZHBDXV7",
    "companies": {
        "apex": "Apex Tire",
        "global": "Global",
        "traction": "Traction Control Outfitters, LLC",
        "roadready": "RoadReady",
        "consolidated": "Vista consolidada",
    },
    "company_ids": {
        "apex": "9341455130166501",
        "global": "9341455130196737",
        "traction": "9341455130188547",
        "roadready": "9341455130170608",
        "consolidated": "9341455649090852",
    },
    "default_company": "apex",
}


# ============================================================
# HELPERS
# ============================================================
def screenshot(page, entity_key, station_name):
    """Take screenshot and save with organized naming."""
    ts = datetime.now().strftime("%H%M%S")
    fname = f"{entity_key}_{station_name}_{ts}.png"
    fpath = SCREENSHOT_DIR / fname
    try:
        page.screenshot(path=str(fpath), full_page=False)
        print(f"    [SCREENSHOT] {fname}")
    except Exception as e:
        print(f"    [SCREENSHOT ERROR] {e}")
    return str(fpath)


def safe_text(page, selector, timeout=3000):
    """Safely get text from a selector."""
    try:
        el = page.locator(selector).first
        if el.is_visible(timeout=timeout):
            return el.inner_text().strip()
    except Exception:
        pass
    return ""


def safe_count(page, selector, timeout=3000):
    """Count visible elements matching selector."""
    try:
        return page.locator(selector).count()
    except Exception:
        return 0


def get_page_text(page):
    """Get all visible text on page."""
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def wait_for_qbo_load(page, timeout=15):
    """Wait for QBO page to finish loading."""
    for _ in range(timeout):
        try:
            # Check for loading indicators
            loading = page.locator('[class*="loading"], [class*="spinner"]').count()
            if loading == 0:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def navigate_to(page, path, wait=5):
    """Navigate to a QBO path and wait for load."""
    url = f"https://qbo.intuit.com{path}"
    try:
        page.goto(url, timeout=30000)
        time.sleep(wait)
        wait_for_qbo_load(page)
    except Exception as e:
        print(f"    [NAV ERROR] {path}: {e}")


def verify_current_entity(page, expected_name, timeout=10):
    """Verify which company we're currently in by checking header text."""
    # The company name appears in the top-left header of Enterprise Suite
    for attempt in range(timeout):
        try:
            # Try multiple selectors for company name
            for selector in [
                'header [class*="company"]',
                '[data-testid="company-name"]',
                ".company-name",
                'button:has-text("LLC")',
                "header button",
            ]:
                elements = page.locator(selector)
                if elements.count() > 0:
                    for i in range(elements.count()):
                        text = elements.nth(i).inner_text().strip()
                        if text and len(text) > 3:
                            print(f"    [VERIFY] Header text: '{text}'")
                            # Partial match on key words from expected name
                            expected_words = expected_name.lower().split()[:2]  # First 2 words
                            if any(w in text.lower() for w in expected_words if len(w) > 3):
                                return True
                            else:
                                # Found a company name but it doesn't match
                                return False

            # Fallback: check page title or URL for company hints
            title = page.title()
            if expected_name.split(",")[0].split("LLC")[0].strip().lower() in title.lower():
                return True

        except Exception:
            pass
        time.sleep(1)

    # Last resort: try to get text from the top area
    try:
        body_text = page.locator("body").first.inner_text()[:500]
        expected_short = expected_name.split(",")[0].strip()
        if expected_short.lower() in body_text.lower():
            print(f"    [VERIFY] Found '{expected_short}' in page body")
            return True
    except Exception:
        pass

    print(f"    [VERIFY] Could not confirm entity: {expected_name}")
    return None  # Unknown - couldn't determine


def switch_entity(page, entity_key):
    """Switch to entity using URL-based method with verification."""
    entity = ENTITIES[entity_key]
    cid = entity["company_id"]
    expected_name = entity["name"]
    url = f"https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={cid}"

    print(f"\n  === Switching to: {expected_name} ===")

    for attempt in range(3):  # Up to 3 attempts
        try:
            if attempt > 0:
                print(f"  [RETRY {attempt}] Attempting switch again...")
                # Go to homepage first to reset state
                page.goto("https://qbo.intuit.com/app/homepage", timeout=30000)
                time.sleep(3)

            page.goto(url, timeout=60000)

            # Wait for redirect to complete - the switch URL redirects to dashboard
            time.sleep(10)

            # Wait for page to settle (no more loading)
            wait_for_qbo_load(page, timeout=10)

            # Verify we're on QBO
            if not is_in_qbo(page):
                print(f"  [WARN] Not in QBO after switch. URL: {page.url}")
                continue

            # Verify the correct company by checking the header
            verification = verify_current_entity(page, expected_name)
            if verification is True:
                print(f"  [OK] Confirmed: Now in {expected_name}")
                return True
            elif verification is False:
                print(f"  [WARN] Wrong company! Expected '{expected_name}', got different entity.")
                # Try clicking the company switcher directly
                continue
            else:
                # Couldn't verify - take screenshot of header area and proceed with caution
                print("  [WARN] Could not verify company. Proceeding with caution.")
                # Navigate to homepage and check header
                page.goto("https://qbo.intuit.com/app/homepage", timeout=30000)
                time.sleep(5)
                verification = verify_current_entity(page, expected_name)
                if verification is True:
                    print(f"  [OK] Confirmed on homepage: {expected_name}")
                    return True
                elif verification is False:
                    print("  [WARN] Still wrong company after homepage check.")
                    continue
                else:
                    # Can't verify but we're in QBO - proceed
                    print("  [INFO] Proceeding without firm verification.")
                    return True

        except Exception as e:
            print(f"  [ERROR] Switch attempt {attempt + 1} failed: {e}")

    print(f"  [FAILED] Could not switch to {expected_name} after 3 attempts")
    return False


# ============================================================
# STATION AUDITORS
# ============================================================


def audit_station_1_dashboard(page, entity_key, results):
    """Station 1: Dashboard (/app/homepage)"""
    print("  [Station 1] Dashboard...")
    navigate_to(page, "/app/homepage", wait=12)
    # Extra wait for dashboard widgets to render
    wait_for_qbo_load(page, timeout=10)

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "01_dashboard")

    data = {
        "station": "Dashboard",
        "screenshot": shots,
        "findings": [],
        "raw_text_snippet": text[:2000],
    }

    # Check for negative numbers
    negatives = re.findall(r"-\$[\d,]+\.?\d*", text)
    if negatives:
        data["findings"].append(
            {
                "id": f"UI-DASH-{entity_key}",
                "severity": "CRITICAL",
                "detail": f"Negative values visible on dashboard: {negatives[:5]}",
            }
        )

    # Check for error banners
    errors = re.findall(r"(?i)(error|failed|unavailable|something went wrong)", text)
    if errors:
        data["findings"].append(
            {
                "id": f"UI-DASH-ERR-{entity_key}",
                "severity": "CRITICAL",
                "detail": f"Error messages on dashboard: {errors[:3]}",
            }
        )

    # Look for key KPIs
    for kpi in ["Net Income", "Profit", "Revenue", "Sales", "Bank", "Cash"]:
        if kpi.lower() in text.lower():
            data[f"has_{kpi.lower().replace(' ', '_')}"] = True

    results[entity_key]["stations"]["dashboard"] = data
    print(f"    Findings: {len(data['findings'])}")


def audit_station_2_pnl(page, entity_key, results):
    """Station 2: Profit & Loss Report"""
    print("  [Station 2] P&L Report...")
    # Enterprise Suite uses different report URLs than standard QBO
    # Try multiple paths - the standard /app/reports/profitandloss returns 404
    report_paths = [
        "/app/reports/profitandloss",
        "/app/report/profitandloss",
        "/app/reportv2/profitandloss",
    ]

    loaded = False
    for rpath in report_paths:
        navigate_to(page, rpath, wait=8)
        text = get_page_text(page)
        if "sorry" not in text.lower() and "can't find" not in text.lower():
            loaded = True
            break
        print(f"    [INFO] {rpath} returned 404, trying next...")

    if not loaded:
        # Fallback: try navigating via Reports sidebar
        print("    [INFO] Direct URLs failed. Using sidebar navigation...")
        navigate_to(page, "/app/homepage", wait=5)
        try:
            # Click "Reports" in left sidebar
            reports_link = page.locator('a:has-text("Reports"), [data-testid*="report"]').first
            if reports_link.is_visible(timeout=3000):
                reports_link.click()
                time.sleep(3)
                # Look for "Profit and Loss" link in reports list
                pnl_link = page.locator('a:has-text("Profit and Loss"), a:has-text("Profit & Loss")').first
                if pnl_link.is_visible(timeout=5000):
                    pnl_link.click()
                    time.sleep(8)
        except Exception as e:
            print(f"    [WARN] Sidebar navigation failed: {e}")

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "02_pnl")

    data = {
        "station": "P&L",
        "screenshot": shots,
        "findings": [],
        "raw_text_snippet": text[:3000],
    }

    # Try to extract key P&L numbers
    for metric in [
        "Total Income",
        "Gross Profit",
        "Total Expenses",
        "Net Income",
        "Net Operating Income",
        "Cost of Goods Sold",
        "Total COGS",
    ]:
        pattern = rf"{metric}\s*[\$\s]*(-?[\d,]+\.?\d*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val_str = match.group(1).replace(",", "")
            try:
                val = float(val_str)
                data[metric.lower().replace(" ", "_")] = val
                if "net" in metric.lower() and "income" in metric.lower() and val < 0:
                    data["findings"].append(
                        {
                            "id": f"FIN-PNL-NEG-{entity_key}",
                            "severity": "CRITICAL",
                            "detail": f"Net Income is NEGATIVE: ${val:,.2f}",
                        }
                    )
            except ValueError:
                data[metric.lower().replace(" ", "_")] = val_str

    # Check for empty report
    if "no data" in text.lower() or "no transactions" in text.lower() or len(text.strip()) < 100:
        data["findings"].append(
            {
                "id": f"FIN-PNL-EMPTY-{entity_key}",
                "severity": "CRITICAL",
                "detail": "P&L report appears EMPTY",
            }
        )

    results[entity_key]["stations"]["pnl"] = data
    print(f"    Findings: {len(data['findings'])}")


def audit_station_3_balance_sheet(page, entity_key, results):
    """Station 3: Balance Sheet"""
    print("  [Station 3] Balance Sheet...")
    # Enterprise Suite uses different report URLs
    report_paths = [
        "/app/reports/balancesheet",
        "/app/report/balancesheet",
        "/app/reportv2/balancesheet",
    ]

    loaded = False
    for rpath in report_paths:
        navigate_to(page, rpath, wait=8)
        text = get_page_text(page)
        if "sorry" not in text.lower() and "can't find" not in text.lower():
            loaded = True
            break
        print(f"    [INFO] {rpath} returned 404, trying next...")

    if not loaded:
        # Fallback: sidebar navigation
        print("    [INFO] Direct URLs failed. Using sidebar navigation...")
        navigate_to(page, "/app/homepage", wait=5)
        try:
            reports_link = page.locator('a:has-text("Reports"), [data-testid*="report"]').first
            if reports_link.is_visible(timeout=3000):
                reports_link.click()
                time.sleep(3)
                bs_link = page.locator('a:has-text("Balance Sheet")').first
                if bs_link.is_visible(timeout=5000):
                    bs_link.click()
                    time.sleep(8)
        except Exception as e:
            print(f"    [WARN] Sidebar navigation failed: {e}")

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "03_balance_sheet")

    data = {
        "station": "Balance Sheet",
        "screenshot": shots,
        "findings": [],
        "raw_text_snippet": text[:3000],
    }

    # Extract key BS numbers
    for metric in [
        "Total Assets",
        "Total Liabilities",
        "Total Equity",
        "Total Liabilities and Equity",
        "Cash",
        "Accounts Receivable",
        "Inventory",
        "Accounts Payable",
    ]:
        pattern = rf"{metric}\s*[\$\s]*(-?[\d,]+\.?\d*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val_str = match.group(1).replace(",", "")
            try:
                data[metric.lower().replace(" ", "_")] = float(val_str)
            except ValueError:
                data[metric.lower().replace(" ", "_")] = val_str

    # Check A = L + E
    assets = data.get("total_assets", 0)
    liab_eq = data.get("total_liabilities_and_equity", 0)
    if assets and liab_eq and isinstance(assets, (int, float)) and isinstance(liab_eq, (int, float)):
        if abs(assets - liab_eq) > 1:
            data["findings"].append(
                {
                    "id": f"FIN-BS-UNBAL-{entity_key}",
                    "severity": "CRITICAL",
                    "detail": f"Balance Sheet UNBALANCED: Assets={assets:,.0f} vs L+E={liab_eq:,.0f}",
                }
            )

    results[entity_key]["stations"]["balance_sheet"] = data
    print(f"    Findings: {len(data['findings'])}")


def audit_station_4_customers(page, entity_key, results):
    """Station 4: Customers"""
    print("  [Station 4] Customers...")
    navigate_to(page, "/app/customers", wait=8)

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "04_customers")

    data = {
        "station": "Customers",
        "screenshot": shots,
        "findings": [],
    }

    # Try to get customer count from page
    count_match = re.search(r"(\d+)\s*(?:customers?|results?|of\s+\d+)", text, re.IGNORECASE)
    if count_match:
        data["customer_count_visible"] = count_match.group(0)

    # Check for test names
    test_names = re.findall(r"(?i)(test|delete|sample|dummy|xxx|fake)", text)
    if test_names:
        data["findings"].append(
            {
                "id": f"DATA-CUST-TEST-{entity_key}",
                "severity": "HIGH",
                "detail": f"Possible test customer names found: {set(test_names)}",
            }
        )

    results[entity_key]["stations"]["customers"] = data
    print(f"    Findings: {len(data['findings'])}")


def audit_station_5_vendors(page, entity_key, results):
    """Station 5: Vendors"""
    print("  [Station 5] Vendors...")
    navigate_to(page, "/app/vendors", wait=8)

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "05_vendors")

    data = {
        "station": "Vendors",
        "screenshot": shots,
        "findings": [],
    }

    count_match = re.search(r"(\d+)\s*(?:vendors?|results?)", text, re.IGNORECASE)
    if count_match:
        data["vendor_count_visible"] = count_match.group(0)

    results[entity_key]["stations"]["vendors"] = data
    print(f"    Findings: {len(data['findings'])}")


def audit_station_6_projects(page, entity_key, results):
    """Station 6: Projects"""
    print("  [Station 6] Projects...")
    navigate_to(page, "/app/projects", wait=8)

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "06_projects")

    data = {
        "station": "Projects",
        "screenshot": shots,
        "findings": [],
    }

    # Check if projects feature is enabled
    if "turn on" in text.lower() or "enable" in text.lower() or "get started" in text.lower():
        data["findings"].append(
            {
                "id": f"UI-PROJ-DISABLED-{entity_key}",
                "severity": "HIGH",
                "detail": "Projects feature appears DISABLED or not set up",
            }
        )

    # Check for empty
    if "no projects" in text.lower() or len(text.strip()) < 50:
        data["findings"].append(
            {
                "id": f"DATA-PROJ-EMPTY-{entity_key}",
                "severity": "HIGH",
                "detail": "Projects page is EMPTY",
            }
        )

    results[entity_key]["stations"]["projects"] = data
    print(f"    Findings: {len(data['findings'])}")


def audit_station_7_invoices(page, entity_key, results):
    """Station 7: Invoices/Sales"""
    print("  [Station 7] Invoices...")
    navigate_to(page, "/app/invoices", wait=8)

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "07_invoices")

    data = {
        "station": "Invoices",
        "screenshot": shots,
        "findings": [],
    }

    # Look for overdue indicators
    overdue_match = re.findall(r"(?i)overdue", text)
    if overdue_match:
        data["has_overdue"] = True
        data["overdue_mentions"] = len(overdue_match)

    # Look for totals
    for label in ["Open", "Overdue", "Paid"]:
        pattern = rf"{label}\s*[\$\s]*(-?[\d,]+\.?\d*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[f"invoices_{label.lower()}"] = match.group(0)

    results[entity_key]["stations"]["invoices"] = data
    print(f"    Findings: {len(data['findings'])}")


def audit_station_8_bills(page, entity_key, results):
    """Station 8: Bills"""
    print("  [Station 8] Bills...")
    navigate_to(page, "/app/bills", wait=8)

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "08_bills")

    data = {
        "station": "Bills",
        "screenshot": shots,
        "findings": [],
    }

    if "no bills" in text.lower() or len(text.strip()) < 50:
        data["findings"].append(
            {
                "id": f"DATA-BILLS-EMPTY-{entity_key}",
                "severity": "HIGH",
                "detail": "Bills page is EMPTY",
            }
        )

    results[entity_key]["stations"]["bills"] = data
    print(f"    Findings: {len(data['findings'])}")


def audit_station_9_banking(page, entity_key, results):
    """Station 9: Banking"""
    print("  [Station 9] Banking...")
    navigate_to(page, "/app/banking", wait=8)

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "09_banking")

    data = {
        "station": "Banking",
        "screenshot": shots,
        "findings": [],
    }

    # Check for connected accounts
    if "connect" in text.lower() and "account" in text.lower():
        data["findings"].append(
            {
                "id": f"UI-BANK-NOCONN-{entity_key}",
                "severity": "MEDIUM",
                "detail": "Banking may not have connected accounts",
            }
        )

    # Look for bank balances
    balance_matches = re.findall(r"\$[\d,]+\.?\d*", text)
    if balance_matches:
        data["visible_balances"] = balance_matches[:10]

    # Check for "For Review" count
    review_match = re.search(r"(?i)for\s+review\s*[\(:]?\s*(\d+)", text)
    if review_match:
        data["for_review_count"] = int(review_match.group(1))

    results[entity_key]["stations"]["banking"] = data
    print(f"    Findings: {len(data['findings'])}")


def audit_station_10_payroll(page, entity_key, results):
    """Station 10: Payroll"""
    print("  [Station 10] Payroll...")
    navigate_to(page, "/app/payroll", wait=8)

    text = get_page_text(page)
    shots = screenshot(page, entity_key, "10_payroll")

    data = {
        "station": "Payroll",
        "screenshot": shots,
        "findings": [],
    }

    # Check if payroll is set up
    if any(x in text.lower() for x in ["set up", "get started", "subscribe", "turn on", "enable"]):
        data["findings"].append(
            {
                "id": f"UI-PAY-NOTSETUP-{entity_key}",
                "severity": "HIGH",
                "detail": "Payroll is NOT SET UP for this entity",
            }
        )
    elif "no employees" in text.lower() or "no payroll" in text.lower():
        data["findings"].append(
            {
                "id": f"DATA-PAY-EMPTY-{entity_key}",
                "severity": "HIGH",
                "detail": "Payroll page shows no data",
            }
        )

    results[entity_key]["stations"]["payroll"] = data
    print(f"    Findings: {len(data['findings'])}")


# ============================================================
# MAIN AUDIT ORCHESTRATOR
# ============================================================


def run_audit():
    """Run full TCO audit across all entities."""
    print("\n" + "=" * 60)
    print("  TCO AUDIT - ATLANTA DEMO READINESS")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = {}
    all_findings = []

    # Initialize results structure
    for ek, ev in ENTITIES.items():
        results[ek] = {
            "entity": ev,
            "stations": {},
            "audit_status": "pending",
        }

    # Try TCO_DEMO first (plan credentials), fallback to TCO
    login_project = "TCO_DEMO"
    try:
        print(f"\n  Logging in with {login_project} account...")
        pw, browser, page = start_round(login_project, "apex")
    except Exception as e1:
        print(f"  [WARN] {login_project} login failed: {e1}")
        print("  Trying TCO account...")
        login_project = "TCO"
        try:
            pw, browser, page = start_round(login_project, "apex")
        except Exception as e2:
            print(f"  [FATAL] Both logins failed: {e2}")
            print("  Make sure Chrome is closed and try again.")
            return

    print(f"\n  Logged in via {login_project}")

    # Audit each entity
    # Skip entities already audited successfully (apex, global done in run 1)
    # Only audit remaining: traction, roadready, consolidated
    entity_order = ["traction", "roadready", "consolidated"]

    for entity_key in entity_order:
        entity = ENTITIES[entity_key]
        print(f"\n{'=' * 60}")
        print(f"  AUDITING: {entity['name']}")
        print(f"  Role: {entity['role']}")
        print(f"{'=' * 60}")

        # Switch to entity
        if not switch_entity(page, entity_key):
            results[entity_key]["audit_status"] = "SWITCH_FAILED"
            print(f"  [ERROR] Could not switch to {entity_key}. Skipping.")
            continue

        results[entity_key]["audit_status"] = "auditing"

        # Run all 10 stations
        stations = [
            audit_station_1_dashboard,
            audit_station_2_pnl,
            audit_station_3_balance_sheet,
            audit_station_4_customers,
            audit_station_5_vendors,
            audit_station_6_projects,
            audit_station_7_invoices,
            audit_station_8_bills,
            audit_station_9_banking,
            audit_station_10_payroll,
        ]

        # For consolidated view, skip some stations
        if entity_key == "consolidated":
            # Consolidated only has Dashboard, P&L, BS, and some reports
            stations = [
                audit_station_1_dashboard,
                audit_station_2_pnl,
                audit_station_3_balance_sheet,
            ]

        for station_fn in stations:
            try:
                station_fn(page, entity_key, results)
            except Exception as e:
                station_name = station_fn.__name__.replace("audit_station_", "")
                print(f"    [ERROR] Station {station_name} failed: {e}")
                results[entity_key]["stations"][station_name] = {
                    "station": station_name,
                    "error": str(e),
                    "findings": [
                        {
                            "id": f"UI-ERR-{entity_key}-{station_name}",
                            "severity": "CRITICAL",
                            "detail": f"Station crashed: {str(e)[:100]}",
                        }
                    ],
                }

        results[entity_key]["audit_status"] = "complete"
        print(f"\n  [DONE] {entity['name']} audit complete")

    # Compile findings
    print(f"\n{'=' * 60}")
    print("  COMPILING RESULTS")
    print(f"{'=' * 60}")

    for ek, er in results.items():
        for sk, sv in er.get("stations", {}).items():
            for f in sv.get("findings", []):
                f["entity"] = ek
                f["station"] = sk
                all_findings.append(f)

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_findings.sort(key=lambda x: severity_order.get(x.get("severity", "LOW"), 99))

    # Print summary
    print(f"\n  Total Findings: {len(all_findings)}")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = sum(1 for f in all_findings if f.get("severity") == sev)
        if count:
            print(f"    {sev}: {count}")

    # Save results JSON
    json_path = SCREENSHOT_DIR / "audit_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        # Clean up non-serializable data
        clean_results = {}
        for k, v in results.items():
            clean_results[k] = {
                "entity": v["entity"],
                "audit_status": v["audit_status"],
                "stations": {},
            }
            for sk, sv in v.get("stations", {}).items():
                clean_sv = {kk: vv for kk, vv in sv.items() if kk != "raw_text_snippet"}
                clean_results[k]["stations"][sk] = clean_sv

        json.dump(
            {
                "audit_date": datetime.now().isoformat(),
                "results": clean_results,
                "findings": all_findings,
                "summary": {
                    "total_findings": len(all_findings),
                    "critical": sum(1 for f in all_findings if f.get("severity") == "CRITICAL"),
                    "high": sum(1 for f in all_findings if f.get("severity") == "HIGH"),
                    "medium": sum(1 for f in all_findings if f.get("severity") == "MEDIUM"),
                    "low": sum(1 for f in all_findings if f.get("severity") == "LOW"),
                },
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n  Results saved: {json_path}")
    print(f"  Screenshots in: {SCREENSHOT_DIR}")

    # Generate markdown report
    generate_report(results, all_findings)

    # Cleanup
    try:
        pw.stop()
    except Exception:
        pass

    print(f"\n{'=' * 60}")
    print("  AUDIT COMPLETE")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 60}\n")


def generate_report(results, all_findings):
    """Generate markdown report from audit results."""
    lines = []
    lines.append("# TCO AUDIT - UI VERIFICATION REPORT")
    lines.append(f"\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("**Method:** Playwright UI automation")
    lines.append(f"**Total Findings:** {len(all_findings)}")
    lines.append("")

    # Summary table
    lines.append("## FINDINGS SUMMARY")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|---|---|")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = sum(1 for f in all_findings if f.get("severity") == sev)
        lines.append(f"| {sev} | {count} |")
    lines.append("")

    # Per-entity results
    for ek in ["apex", "global", "traction", "roadready", "consolidated"]:
        er = results.get(ek, {})
        entity = er.get("entity", {})
        lines.append(f"## {entity.get('name', ek)}")
        lines.append(f"**Role:** {entity.get('role', 'N/A')}")
        lines.append(f"**Audit Status:** {er.get('audit_status', 'N/A')}")
        lines.append("")

        stations = er.get("stations", {})
        if not stations:
            lines.append("*No station data collected.*\n")
            continue

        for sk, sv in stations.items():
            findings = sv.get("findings", [])
            lines.append(f"### Station: {sv.get('station', sk)}")

            # Show extracted metrics
            for key, val in sv.items():
                if key in (
                    "station",
                    "screenshot",
                    "findings",
                    "raw_text_snippet",
                    "error",
                ):
                    continue
                lines.append(f"- **{key}:** {val}")

            if findings:
                lines.append("\n**Findings:**")
                for f in findings:
                    lines.append(f"- [{f['severity']}] {f['id']}: {f['detail']}")
            else:
                lines.append("- No findings (CLEAN)")
            lines.append("")

    # All findings sorted
    lines.append("## ALL FINDINGS (sorted by severity)")
    lines.append("")
    lines.append("| # | Severity | Entity | Station | ID | Detail |")
    lines.append("|---|---|---|---|---|---|")
    for i, f in enumerate(all_findings, 1):
        lines.append(f"| {i} | **{f['severity']}** | {f['entity']} | {f['station']} | {f['id']} | {f['detail'][:80]} |")
    lines.append("")

    report_text = "\n".join(lines)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"  Report saved: {REPORT_PATH}")


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    run_audit()
