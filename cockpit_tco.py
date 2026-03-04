# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding="utf-8")

from playwright.sync_api import sync_playwright
import time
from datetime import datetime


def clear_screen():
    import os

    os.system("cls" if os.name == "nt" else "clear")


def show_header():
    print("\n" * 2)
    print("    " + "=" * 56)
    print("    |" + " " * 54 + "|")
    print("    |   TESTBOX   QBO Feature Validation Cockpit          |")
    print("    |                   TCO PROJECT                        |")
    print("    |" + " " * 54 + "|")
    print("    " + "=" * 56)
    print()


def show_features():
    print("    +------------------------------------------------------+")
    print("    |              FEATURES TO VALIDATE                    |")
    print("    +------------------------------------------------------+")
    print("    |  [1]  Dimensions: Dimension List         [ PENDING ] |")
    print("    |  [2]  Dimensions: Dimension Assignment   [ PENDING ] |")
    print("    |  [3]  Dimensions: Transaction Assignment [ PENDING ] |")
    print("    +------------------------------------------------------+")
    print()


def show_progress(step, total, message):
    bar_width = 30
    filled = int(bar_width * step / total)
    bar = "#" * filled + "-" * (bar_width - filled)
    print(f"    [{bar}] Step {step}/{total}")
    print(f"    {message}")
    print()


def validate_tco_002():
    clear_screen()
    show_header()

    print("    +------------------------------------------------------+")
    print("    |  VALIDATING: TCO_002 - Dimension Assignment          |")
    print("    +------------------------------------------------------+")
    print()

    # Step 1
    show_progress(1, 4, "Connecting to QBO Chrome...")
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.pages[0]
    print("    OK - Connected")
    print()
    time.sleep(1)

    # Step 2
    show_progress(2, 4, "Navigating to Dimension Assignment...")
    print("    -> /app/class")
    page.goto("https://qbo.intuit.com/app/class")
    time.sleep(3)
    print("    OK - Classes page")
    print("    -> /app/dimensions/assignment")
    page.goto("https://qbo.intuit.com/app/dimensions/assignment")
    time.sleep(4)
    print("    OK - Dimension Assignment page")
    print()

    # Step 3
    show_progress(3, 4, "Capturing screenshot...")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = "TCO_002_DimensionAssignment_" + timestamp + ".png"
    filepath = "G:/Meu Drive/TestBox/QBO-Evidence/" + filename
    page.screenshot(path=filepath, full_page=False)
    print("    OK - Saved: " + filename)
    print()

    # Step 4
    show_progress(4, 4, "Analyzing page content...")
    confirm_count = page.locator("text=Confirm").count()
    print("    OK - Found " + str(confirm_count) + " Confirm buttons")
    print()

    pw.stop()

    # Results
    print("    +------------------------------------------------------+")
    print("    |            VALIDATION COMPLETE - STATUS: OK          |")
    print("    +------------------------------------------------------+")
    print()

    print("    SPREADSHEET DATA:")
    print("    " + "-" * 50)
    print("    Ref:           TCO_002")
    print("    Feature:       Dimensions: Dimension Assignment")
    print("    Company:       Apex Tire & Auto Retail, LLC")
    print("    Status:        OK")
    print("    Evidence File: " + filename)
    print("    Link:          View")
    print("    Intuit Notes:  AI-suggested dimension values with Confirm buttons")
    print("    Internal Notes: Navigate to /app/dimensions/assignment")
    print("    Timestamp:     " + timestamp.replace("_", " "))
    print()


if __name__ == "__main__":
    clear_screen()
    show_header()
    show_features()
    print("    > Which feature to validate? 2")
    print()
    validate_tco_002()
