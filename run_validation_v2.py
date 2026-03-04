# run_validation_v2.py
# QBO Feature Validation - TCO Project
# Based on prompt v2: uses Ref as primary key, clean screenshots (no annotations)

import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Users\adm_r\intuit-boom")

import json
import time

# Force reload modules to get latest changes
for mod_name in list(sys.modules.keys()):
    if "qbo_checker" in mod_name:
        del sys.modules[mod_name]

from qbo_checker.login import ensure_logged_in
from qbo_checker.screenshot import generate_filename, capture_screenshot
from qbo_checker.config import FEATURES_JSON, EVIDENCE_DIR


def is_on_company_selection_screen(page):
    """Check if we're on the company selection screen."""
    try:
        # Check for common company selection indicators
        if page.locator("text=Restaure sua empresa").is_visible(timeout=1000):
            return True
        if page.locator("text=Restore your company").is_visible(timeout=1000):
            return True
        if page.locator("text=Intuit Enterprise Suite").is_visible(timeout=1000):
            # This could be company selection OR home - check for company list
            if page.locator("text=Vista consolidada").is_visible(timeout=500):
                return True
    except Exception:
        pass
    return False


def ensure_in_company(page, company_name="Apex Tire"):
    """Make sure we're inside a company, not on selection screen."""
    if is_on_company_selection_screen(page):
        print(f"  [INFO] On company selection screen, selecting {company_name}...")
        # Click on Apex Tire company
        try:
            page.locator(f"text={company_name}").first.click(timeout=5000)
            time.sleep(3)
            return True
        except Exception:
            # Try alternative selector
            try:
                page.locator("text=Apex Tire & Auto Retail").first.click(timeout=3000)
                time.sleep(3)
                return True
            except Exception:
                print(f"  [ERROR] Could not select company {company_name}")
                return False
    return True


def load_features():
    """Load features from JSON file."""
    with open(FEATURES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["features"]


def navigate_to_feature(page, feature):
    """Navigate to feature URL."""
    nav = feature.get("navigation", {})
    steps = nav.get("steps", [])

    for step in steps:
        action = step.get("action")

        if action == "goto":
            url = step.get("url")
            try:
                page.goto(url, timeout=30000)
                return True, f"Navigated to {url}"
            except Exception as e:
                return False, f"Failed to navigate: {str(e)}"

        elif action == "wait":
            seconds = step.get("seconds", 2)
            time.sleep(seconds)

    return True, "Navigation complete"


def run_validation():
    """Main validation flow."""
    print("=" * 60)
    print("QBO FEATURE VALIDATION - TCO PROJECT")
    print("Based on Prompt v2 - Using Ref as Primary Key")
    print("=" * 60)
    print()

    # Load features
    features = load_features()
    print(f"Loaded {len(features)} features from {FEATURES_JSON}")
    print()

    # Login
    print("Connecting to Chrome via CDP...")
    pw, browser, page = ensure_logged_in("TCO")
    time.sleep(2)
    print("Connected!")
    print()

    # Ensure we're in a company (not on selection screen)
    if not ensure_in_company(page, "Apex Tire"):
        print("ERROR: Could not enter company. Exiting.")
        pw.stop()
        return

    print("Starting feature validation...")
    print()

    results = []

    for i, feature in enumerate(features, 1):
        ref = feature.get("ref", f"UNKNOWN_{i}")
        name = feature.get("name", "Unknown Feature")
        company = feature.get("company", "Apex Tire")

        print(f"[{i}/{len(features)}] {ref}: {name}")

        # Navigate to feature
        success, details = navigate_to_feature(page, feature)

        if success:
            # Wait for page to load
            time.sleep(3)

            # Check if we got redirected to company selection
            if is_on_company_selection_screen(page):
                print("  [WARN] Redirected to company selection, re-entering...")
                ensure_in_company(page, company)
                # Re-navigate
                navigate_to_feature(page, feature)
                time.sleep(3)

            status = "OK"
        else:
            status = "FAIL"
            print(f"  [ERROR] {details}")

        print(f"  Status: {status}")

        # Generate filename with Ref
        filename = generate_filename(ref=ref, project="TCO", company=company.replace(" ", ""), feature_name=name)

        # Capture clean screenshot (no annotations)
        capture_screenshot(page, filename)
        print(f"  Screenshot: {filename}")

        results.append({"ref": ref, "name": name, "status": status, "file": filename})

        print()

    # Cleanup
    pw.stop()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    ok_count = sum(1 for r in results if r["status"] == "OK")
    fail_count = len(results) - ok_count
    print(f"Total: {len(results)} | OK: {ok_count} | FAIL: {fail_count}")
    print()

    print("Results by Ref:")
    for r in results:
        print(f"  {r['status']:4} | {r['ref']:8} | {r['name'][:50]}")

    # Save results to JSON for later use
    results_file = EVIDENCE_DIR / "validation_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "project": "TCO",
                "total": len(results),
                "ok": ok_count,
                "fail": fail_count,
                "results": results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"\nResults saved to: {results_file}")


if __name__ == "__main__":
    run_validation()
