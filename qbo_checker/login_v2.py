# qbo_checker/login_v2.py
"""
QBO Login v2 - Complete Flow Handler
Handles ALL possible states and navigates to QBO homepage.

Flow:
1. Start Chrome with CDP
2. Check current state
3. Navigate through: account-manager -> companysel -> homepage
"""

import time
import socket
import subprocess
import os
from playwright.sync_api import sync_playwright

# Configuration
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "tsa_qbo_chrome_profile")
CDP_PORT = 9222

# Account info
TCO_EMAIL = "quickbooks-testuser-tco-tbxdemo@tbxofficial.com"


def is_port_open(port):
    """Check if port is open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def start_chrome():
    """Start Chrome with CDP if not running."""
    if is_port_open(CDP_PORT):
        print("  [OK] Chrome already running on port 9222")
        return True

    print("  [INFO] Starting Chrome...")
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    cmd = [
        CHROME_PATH,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={USER_DATA_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-blink-features=AutomationControlled",
        "--start-maximized",
    ]

    DETACHED_PROCESS = 0x00000008
    CREATE_BREAKAWAY_FROM_JOB = 0x01000000

    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=DETACHED_PROCESS | CREATE_BREAKAWAY_FROM_JOB,
        start_new_session=True,
        close_fds=True,
    )

    # Wait for Chrome
    for i in range(30):
        if is_port_open(CDP_PORT):
            time.sleep(1)
            print("  [OK] Chrome started")
            return True
        time.sleep(0.5)

    print("  [FAIL] Could not start Chrome")
    return False


def detect_state(page):
    """Detect current page state."""
    url = page.url
    content = page.content().lower()

    # Already in QBO homepage
    if "qbo.intuit.com/app/homepage" in url:
        return "QBO_HOMEPAGE"

    # In QBO but not homepage
    if "qbo.intuit.com/app/" in url:
        return "QBO_INSIDE"

    # Company selection screen
    if "companysel" in url or "qbo.intuit.com" in url and ("select" in content or "empresa" in content):
        return "COMPANY_SELECT"

    # Account manager (need to click QuickBooks)
    if "account-manager" in url or "acesse seus produtos" in content or "access your products" in content:
        return "ACCOUNT_MANAGER"

    # Sign-in page
    if "sign-in" in url:
        return "SIGN_IN"

    # Intuit accounts but not sign-in
    if "accounts.intuit.com" in url:
        return "INTUIT_ACCOUNTS"

    # Unknown
    return "UNKNOWN"


def handle_sign_in(page):
    """Handle sign-in page - click saved account or enter credentials."""
    print("  [STATE] Sign-in page")

    # Wait for page to fully load
    time.sleep(2)

    # Debug: print page content to see what's there
    try:
        content = page.content()
        if "Apex" in content:
            print("  [DEBUG] Found 'Apex' in page")
        if "tbxofficial" in content:
            print("  [DEBUG] Found 'tbxofficial' in page")
        if "Testbox" in content or "testbox" in content.lower():
            print("  [DEBUG] Found 'Testbox' in page")
    except Exception:
        # Erro ao acessar conteúdo da página - não crítico para debug
        pass

    # Look for saved account - expanded selectors for Intuit sign-in page
    selectors = [
        # Email-based selectors
        f'text="{TCO_EMAIL}"',
        f'[data-testid="account-chip"]:has-text("{TCO_EMAIL}")',
        f'button:has-text("{TCO_EMAIL}")',
        # Company name selectors - Apex Tire
        'text="Apex Tire"',
        "text=Apex Tire",
        '[data-testid="account-chip"]:has-text("Apex")',
        'button:has-text("Apex")',
        'div[role="button"]:has-text("Apex")',
        # Testbox selectors
        'text="Testbox"',
        "text=Testbox",
        '[data-testid="account-chip"]:has-text("Testbox")',
        'button:has-text("Testbox")',
        'div[role="button"]:has-text("Testbox")',
        # tbxofficial selectors
        'text="tbxofficial"',
        'div:has-text("tbxofficial")',
        '[data-testid="account-chip"]:has-text("tbxofficial")',
        # Generic account chip/card selectors
        '[data-testid="account-chip"]',
        ".account-chip",
        ".saved-account",
        '[class*="account-card"]',
        '[class*="AccountCard"]',
        '[class*="saved-user"]',
        # Role-based selectors for clickable elements with account info
        'div[role="button"][class*="account"]',
        'button[class*="account"]',
        # List item that might contain account
        'li:has-text("Apex")',
        'li:has-text("Testbox")',
        'li:has-text("tbxofficial")',
    ]

    for sel in selectors:
        try:
            elem = page.locator(sel).first
            if elem.is_visible(timeout=1500):
                print(f"  [DEBUG] Found element with selector: {sel[:40]}...")
                elem.click()
                print("  [OK] Clicked saved account!")
                time.sleep(4)
                return True
        except Exception:
            continue

    # Try JavaScript click on any visible account element
    print("  [INFO] Trying JavaScript approach...")
    try:
        result = page.evaluate("""
            () => {
                // Look for any element containing account email or name
                const texts = ['Apex', 'Testbox', 'tbxofficial', 'tco-tbxdemo'];
                for (const text of texts) {
                    const elements = document.querySelectorAll('*');
                    for (const el of elements) {
                        if (el.innerText && el.innerText.includes(text) && el.offsetParent !== null) {
                            // Check if it's clickable (button, link, or has click handler)
                            if (el.tagName === 'BUTTON' || el.tagName === 'A' ||
                                el.getAttribute('role') === 'button' ||
                                el.onclick || el.className.includes('account')) {
                                el.click();
                                return 'clicked: ' + text;
                            }
                        }
                    }
                }
                return 'not found';
            }
        """)
        if result and "clicked" in result:
            print(f"  [OK] {result}")
            time.sleep(4)
            return True
    except Exception as e:
        print(f"  [DEBUG] JS approach failed: {str(e)[:30]}")

    print("  [WARN] No saved account found - trying direct QBO navigation")
    # If no saved account, try going directly to QBO
    page.goto("https://qbo.intuit.com/app/homepage")
    time.sleep(5)
    return True


def handle_account_manager(page):
    """Handle account-manager page - click QuickBooks link."""
    print("  [STATE] Account Manager page")

    # Look for QuickBooks link
    selectors = [
        'text="QuickBooks"',
        "text=QuickBooks",
        'a:has-text("QuickBooks")',
        'button:has-text("QuickBooks")',
        '[href*="qbo"]',
        '[href*="quickbooks"]',
        'text="Acesse seus produtos"',
        'text="Access your products"',
    ]

    for sel in selectors:
        try:
            elem = page.locator(sel).first
            if elem.is_visible(timeout=2000):
                elem.click()
                print("  [OK] Clicked QuickBooks link")
                time.sleep(5)
                return True
        except Exception:
            # Link não encontrado neste seletor - tentar próximo
            continue

    # Try direct navigation
    print("  [INFO] Trying direct navigation to QBO...")
    page.goto("https://qbo.intuit.com/app/homepage")
    time.sleep(5)
    return True


def handle_company_select(page, company="apex"):
    """Handle company selection page."""
    print("  [STATE] Company Selection page")

    company_map = {
        "apex": ['text="Apex Tire"', "text=Apex", 'div:has-text("Apex")'],
        "consolidated": ['text="Vista consolidada"', "text=Consolidated", "text=Vista"],
        "global": ['text="Global"', 'div:has-text("Global")'],
        "traction": ['text="Traction"', 'div:has-text("Traction")'],
    }

    selectors = company_map.get(company, company_map["apex"])

    for sel in selectors:
        try:
            elem = page.locator(sel).first
            if elem.is_visible(timeout=3000):
                elem.click()
                print(f"  [OK] Selected company: {company}")
                time.sleep(8)
                return True
        except Exception:
            # Empresa não encontrada neste seletor - tentar próximo
            continue

    # Try clicking first available company
    print("  [INFO] Trying first available company...")
    try:
        first = page.locator('[class*="company"], [role="button"], .company-card').first
        if first.is_visible(timeout=2000):
            first.click()
            time.sleep(8)
            return True
    except Exception:
        # Nenhuma empresa disponível para seleção
        pass

    print("  [WARN] Could not select company")
    return False


def navigate_to_qbo(page, target_company="apex", max_attempts=5):
    """Navigate through all states to reach QBO homepage."""

    for attempt in range(max_attempts):
        print(f"\n  [Attempt {attempt + 1}/{max_attempts}]")

        state = detect_state(page)
        print(f"  Current state: {state}")
        print(f"  URL: {page.url[:60]}...")

        if state == "QBO_HOMEPAGE":
            print("  [SUCCESS] Already at QBO Homepage!")
            return True

        if state == "QBO_INSIDE":
            print("  [INFO] Inside QBO, navigating to homepage...")
            page.goto("https://qbo.intuit.com/app/homepage")
            time.sleep(3)
            continue

        if state == "COMPANY_SELECT":
            handle_company_select(page, target_company)
            time.sleep(3)
            continue

        if state == "ACCOUNT_MANAGER":
            handle_account_manager(page)
            time.sleep(3)
            continue

        if state == "SIGN_IN":
            handle_sign_in(page)
            time.sleep(3)
            continue

        if state == "INTUIT_ACCOUNTS":
            print("  [INFO] On Intuit accounts, navigating to QBO...")
            page.goto("https://qbo.intuit.com/app/homepage")
            time.sleep(5)
            continue

        if state == "UNKNOWN":
            print("  [INFO] Unknown state, trying QBO homepage...")
            page.goto("https://qbo.intuit.com/app/homepage")
            time.sleep(5)
            continue

    # Final check
    final_state = detect_state(page)
    if final_state in ["QBO_HOMEPAGE", "QBO_INSIDE"]:
        print("  [SUCCESS] Reached QBO!")
        return True

    print(f"  [FAIL] Could not reach QBO. Final state: {final_state}")
    return False


def full_login(company="apex"):
    """Complete login flow - start Chrome, connect, navigate to QBO.

    Args:
        company: 'apex', 'consolidated', 'global', or 'traction'

    Returns:
        Tuple of (playwright, browser, page) or raises Exception
    """
    print("\n" + "=" * 50)
    print("  QBO LOGIN v2 - Full Flow")
    print("=" * 50)

    # Step 1: Start Chrome
    print("\n[Step 1] Starting Chrome...")
    if not start_chrome():
        raise ConnectionError("Could not start Chrome")

    # Step 2: Connect via CDP
    print("\n[Step 2] Connecting via CDP...")
    pw = sync_playwright().start()

    try:
        browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
        print("  [OK] CDP connected")

        # Get or create page
        if browser.contexts and browser.contexts[0].pages:
            page = browser.contexts[0].pages[0]
            print("  [OK] Using existing page")
        else:
            context = browser.new_context()
            page = context.new_page()
            print("  [OK] Created new page")

        # Step 3: Navigate to QBO
        print("\n[Step 3] Navigating to QBO...")

        # First, go to sign-in to trigger the flow
        current_url = page.url
        if "qbo.intuit.com" not in current_url and "accounts.intuit.com" not in current_url:
            print("  [INFO] Starting from sign-in page...")
            page.goto(
                "https://accounts.intuit.com/app/sign-in?app_group=QBO&asset_alias=Intuit.accounting.core.qbowebapp&app_environment=prod"
            )
            time.sleep(3)

        # Navigate through all states
        success = navigate_to_qbo(page, company)

        if success:
            print("\n" + "=" * 50)
            print("  LOGIN SUCCESSFUL!")
            print(f"  Company: {company}")
            print(f"  URL: {page.url}")
            print("=" * 50 + "\n")
        else:
            print("\n  [WARN] Login may not be complete. Check browser.")

        return pw, browser, page

    except Exception as e:
        pw.stop()
        raise e


# Aliases for compatibility
def login_apex():
    """Login and select Apex Tire company."""
    return full_login("apex")


def login_consolidated():
    """Login and select Consolidated View."""
    return full_login("consolidated")


def login_tco(company="apex"):
    """Login to TCO project."""
    return full_login(company)


if __name__ == "__main__":
    # Test
    pw, browser, page = full_login("apex")
    print(f"Final URL: {page.url}")
    input("Press Enter to close...")
    pw.stop()
