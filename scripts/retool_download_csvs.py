#!/usr/bin/env python3
"""Download Retool QBO CSVs via Playwright.

Navigates to Retool, clears filters on both Staging and Production tabs,
and downloads the CSV exports to knowledge-base/access/.

Usage:
    python scripts/retool_download_csvs.py             # headless (needs prior login)
    python scripts/retool_download_csvs.py --headed     # visible browser
    python scripts/retool_download_csvs.py --login      # headed + pauses for manual login
"""

import argparse
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCESS_DIR = os.path.join(BASE, "knowledge-base", "access")

RETOOL_URL = "https://retool.testbox.com/apps/026deb70-a16f-11ef-962b-7bc1e6ce9bc6/Integrations/Quickbooks/Quickbooks"

# Persistent profile for Retool sessions
PROFILE_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright", "retool-sync")


def download_csvs(headed=False, login_mode=False):
    """Open Retool, clear filters, download both CSVs. Returns dict with results."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "success": False,
            "error": "playwright not installed. Run: pip install playwright && playwright install chromium",
        }

    results = {"staging": None, "production": None, "success": False, "error": None}

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=not (headed or login_mode),
            accept_downloads=True,
            viewport={"width": 1280, "height": 900},
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            print("  Opening Retool...")
            page.goto(RETOOL_URL, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(3000)

            # Check if we need to log in
            if "login" in page.url.lower() or "sign-in" in page.url.lower():
                if login_mode:
                    print("  >> Log in to Retool in the browser window...")
                    print("  >> Press ENTER here once you're logged in.")
                    input()
                    page.wait_for_timeout(2000)
                    # Verify login worked
                    if "login" in page.url.lower():
                        results["error"] = "Still on login page after manual login."
                        browser.close()
                        return results
                else:
                    results["error"] = (
                        "Retool session expired. Run once with --login to authenticate: "
                        "python scripts/retool_download_csvs.py --login"
                    )
                    browser.close()
                    return results

            # --- STAGING TAB ---
            print("  Switching to Staging tab...")
            staging_radio = page.locator("text=Staging").first
            staging_radio.click()
            page.wait_for_timeout(3000)

            stg_result = _clear_filters_and_download(page, "staging")
            results["staging"] = stg_result

            # --- PRODUCTION TAB ---
            print("  Switching to Production tab...")
            prod_radio = page.locator("text=Production").first
            prod_radio.click()
            page.wait_for_timeout(3000)

            prod_result = _clear_filters_and_download(page, "production")
            results["production"] = prod_result

            results["success"] = True

        except Exception as e:
            results["error"] = str(e)
        finally:
            browser.close()

    return results


def _clear_filters_and_download(page, env_name):
    """Clear filters on current tab and download CSV. Returns dict."""
    info = {
        "rows_before": None,
        "rows_after": None,
        "filters_cleared": False,
        "downloaded": False,
    }

    # Get current row count
    count_match = page.evaluate(
        "() => { const m = document.body.innerText.match(/(\\d+)\\s*results?/i); return m ? parseInt(m[1]) : 0; }"
    )
    info["rows_before"] = count_match

    # Check if filters are active (aria-label like "2 Filters", "1 Filter")
    filter_btn = page.locator('button[aria-label*="Filter"]').first
    filter_label = filter_btn.get_attribute("aria-label") or ""

    if "Filter" in filter_label and filter_label != "Filter":
        # Has active filters — open panel and clear
        print(f"  [{env_name}] Active filters: {filter_label}")
        filter_btn.click()
        page.wait_for_timeout(1000)

        # Try class-based selector first, then text-based
        clear_btn = page.locator("button:has-text('Clear filters')").first
        if clear_btn.is_visible(timeout=2000):
            clear_btn.click()
            page.wait_for_timeout(2000)
            info["filters_cleared"] = True
            print(f"  [{env_name}] Filters cleared")
        else:
            print(f"  [{env_name}] WARNING: Could not find Clear filters button")
    else:
        print(f"  [{env_name}] No active filters")

    # Get new row count
    count_after = page.evaluate(
        "() => { const m = document.body.innerText.match(/(\\d+)\\s*results?/i); return m ? parseInt(m[1]) : 0; }"
    )
    info["rows_after"] = count_after

    # Download CSV
    save_path = os.path.join(ACCESS_DIR, f"retool_{env_name}_export.csv")
    print(f"  [{env_name}] Downloading CSV ({count_after} rows)...")

    with page.expect_download(timeout=15000) as download_info:
        dl_btn = page.locator('button[aria-label="Download"]').first
        dl_btn.scroll_into_view_if_needed()
        dl_btn.click()

    download = download_info.value
    download.save_as(save_path)
    info["downloaded"] = True
    print(f"  [{env_name}] Saved: {os.path.basename(save_path)}")

    return info


def main():
    parser = argparse.ArgumentParser(description="Download Retool QBO CSVs")
    parser.add_argument("--headed", action="store_true", help="Show browser window")
    parser.add_argument(
        "--login",
        action="store_true",
        help="Open headed browser and pause for manual Retool login",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("RETOOL CSV DOWNLOAD")
    print("=" * 60)

    results = download_csvs(headed=args.headed, login_mode=args.login)

    if not results["success"]:
        print(f"\nERROR: {results['error']}", file=sys.stderr)
        sys.exit(1)

    print("\n=== SUMMARY ===")
    for env in ("staging", "production"):
        r = results[env]
        if r:
            delta = ""
            if r["rows_before"] and r["rows_after"] and r["rows_before"] != r["rows_after"]:
                delta = f" (was {r['rows_before']} with filters)"
            status = "downloaded" if r["downloaded"] else "FAILED"
            print(f"  {env}: {r['rows_after']} rows{delta} — {status}")

    # Output JSON for dashboard consumption
    print("\n__DOWNLOAD_RESULT_JSON__")
    print(json.dumps(results))


if __name__ == "__main__":
    main()
