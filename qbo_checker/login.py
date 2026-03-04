# qbo_checker/login.py
"""QBO Login module - integrated from intuit_login_v2_4.py"""

import hmac
import hashlib
import struct
import time
import base64
import os
import subprocess
import socket
from playwright.sync_api import sync_playwright

from .config import CHROME_DEBUG_PORT

# ============================================================
# CONFIGURATION
# ============================================================

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "tsa_qbo_chrome_profile")

# Account credentials
ACCOUNTS = {
    "TCO": {
        "name": "TCO",
        "email": "quickbooks-testuser-tco-tbxdemo@tbxofficial.com",
        "password": "TestBox!23",
        "totp_secret": "RP4MFT45ZY5EYGMRIPEANJA6YFKHV5O7",
        "companies": {
            "apex": "Apex Tire",
            "global": "Global",
            "traction": "Traction Control Outfitters, LLC",
            "consolidated": "Vista consolidada",
        },
        # Company IDs for URL-based switching
        # URL format: https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId=<ID>
        "company_ids": {
            "consolidated": "9341455649090852",  # Vista consolidada
            "global": "9341455130196737",
            "apex": "9341455130166501",
            # "traction": "PENDING",  # TODO: Capture this ID
        },
        "default_company": "apex",  # Default to Apex Tire for this round
    },
    "Construction": {
        "name": "CONSTRUCTION SALES",
        "email": "quickbooks-test-account@tbxofficial.com",
        "password": "TestBox123!",
        "totp_secret": "23CIWY3QYCOXJRKZYG6YKR7HUYVPLPEL",
        "companies": {},
        "company_ids": {},
        "default_company": None,
    },
}

# ============================================================
# TOTP Generator
# ============================================================


def generate_totp(secret: str) -> str:
    """Generate TOTP code from secret."""
    padding = "=" * ((8 - len(secret) % 8) % 8)
    key = base64.b32decode(secret.upper() + padding)
    counter = int(time.time() // 30)
    counter_bytes = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    truncated = struct.unpack(">I", hmac_hash[offset : offset + 4])[0]
    code = (truncated & 0x7FFFFFFF) % 1000000
    return str(code).zfill(6)


# ============================================================
# Chrome Helper
# ============================================================


def is_port_open(port):
    """Check if port is open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def check_chrome_profile():
    """Check Chrome profile health."""
    lock_file = os.path.join(USER_DATA_DIR, "lockfile")
    if os.path.exists(lock_file) and not is_port_open(CHROME_DEBUG_PORT):
        try:
            os.remove(lock_file)
            print("  \033[93m[INFO] Removed orphan lockfile\033[0m")
        except OSError:
            # Arquivo pode estar em uso ou sem permissão
            pass
    return True


def start_chrome():
    """Start Chrome as independent process."""
    check_chrome_profile()

    if is_port_open(CHROME_DEBUG_PORT):
        print("  \033[93m[INFO] Chrome already open, connecting...\033[0m")
        return True

    print("  \033[90mStarting Chrome...\033[0m")
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    cmd = [
        CHROME_PATH,
        f"--remote-debugging-port={CHROME_DEBUG_PORT}",
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

    print("  \033[90mWaiting for Chrome to start...\033[0m")
    for i in range(30):
        if is_port_open(CHROME_DEBUG_PORT):
            time.sleep(0.5)
            return True
        time.sleep(0.5)

    return False


# ============================================================
# Login Function
# ============================================================


def is_in_qbo(page) -> bool:
    """Check if already in QBO (not just logged into Intuit)."""
    current_url = page.url
    # Check for QBO dashboard or app URLs
    if any(x in current_url for x in ["qbo.intuit.com", "c/bkg/"]):
        return True
    return False


def is_company_selection_screen(page) -> bool:
    """Check if on company selection screen."""
    try:
        page_content = page.content().lower()
        indicators = [
            "restaure sua empresa",  # Portuguese
            "restore your company",  # English
            "intuit enterprise suite",
            "vista consolidada",
            "consolidated view",
        ]
        for indicator in indicators:
            if indicator in page_content:
                return True
    except Exception:
        # Página pode não estar carregada ou erro de acesso
        pass
    return False


def select_company(page, company_name: str) -> bool:
    """Select a specific company from the company selection screen.

    Args:
        page: Playwright page
        company_name: Exact name of the company to select (e.g., "Apex Tire")
    """
    print(f"  \033[90mSelecting company: {company_name}...\033[0m")

    # Build selectors for the specific company
    selectors = [
        f'text="{company_name}"',
        f"text={company_name}",
        f'div:has-text("{company_name}")',
        f'[class*="company"]:has-text("{company_name}")',
        f'button:has-text("{company_name}")',
        f'a:has-text("{company_name}")',
    ]

    for selector in selectors:
        try:
            element = page.locator(selector).first
            if element.is_visible(timeout=3000):
                element.click()
                print(f"  \033[93m[INFO] Clicked: {selector}\033[0m")
                time.sleep(8)  # Wait for QBO to load

                # Close any open dropdowns by pressing Escape
                try:
                    page.keyboard.press("Escape")
                    time.sleep(0.5)
                except Exception:
                    # Teclado pode não estar disponível
                    pass

                # Verify we're in QBO
                if is_in_qbo(page):
                    print(f"  \033[92m[OK] Company '{company_name}' selected!\033[0m")
                    return True
        except Exception:
            # Elemento não encontrado ou timeout - tentar próximo seletor
            continue

    print(f"  \033[91m[ERROR] Could not select company: {company_name}\033[0m")
    return False


def switch_company(page, company_name: str) -> bool:
    """Switch to a different company from within QBO.

    Uses the company dropdown in the header to switch companies.
    """
    print(f"  \033[90mSwitching to company: {company_name}...\033[0m")

    # Click the company dropdown in header
    dropdown_selectors = [
        '[data-testid="company-picker"]',
        '[aria-label*="company"]',
        ".company-picker",
        'button:has-text("Traction Control")',  # Current company name
        'button:has-text("Apex")',
        'header button:has-text("LLC")',
    ]

    clicked_dropdown = False
    for selector in dropdown_selectors:
        try:
            dropdown = page.locator(selector).first
            if dropdown.is_visible(timeout=2000):
                dropdown.click()
                clicked_dropdown = True
                print(f"  \033[93m[INFO] Opened dropdown: {selector}\033[0m")
                time.sleep(2)
                break
        except Exception:
            # Dropdown não encontrado neste seletor - tentar próximo
            continue

    if not clicked_dropdown:
        print("  \033[91m[ERROR] Could not find company dropdown\033[0m")
        return False

    # Now select the target company
    return select_company(page, company_name)


def switch_company_by_url(page, project: str, company_key: str) -> bool:
    """Switch to a company using direct URL navigation.

    This is the PREFERRED method - faster and more reliable than UI navigation.

    Args:
        page: Playwright page
        project: Project name (TCO, Construction)
        company_key: Company key (apex, global, traction, consolidated)

    Returns:
        True if switch successful, False otherwise

    Example:
        switch_company_by_url(page, 'TCO', 'apex')  # Switch to Apex Tire
    """
    account = ACCOUNTS.get(project)
    if not account:
        print(f"  \033[91m[ERROR] Unknown project: {project}\033[0m")
        return False

    company_ids = account.get("company_ids", {})
    company_id = company_ids.get(company_key)

    if not company_id:
        # Fallback to UI-based switching
        company_name = account.get("companies", {}).get(company_key, company_key)
        print(f"  \033[93m[INFO] No company ID for '{company_key}', using UI switch\033[0m")
        return select_company(page, company_name)

    # Use URL-based switching
    url = f"https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={company_id}"
    print(f"  \033[90mSwitching via URL to {company_key}...\033[0m")

    try:
        page.goto(url, timeout=60000)
        time.sleep(5)  # Wait for switch to complete

        # Verify we're in QBO
        if is_in_qbo(page):
            print(f"  \033[92m[OK] Switched to {company_key} via URL!\033[0m")
            return True
        else:
            print("  \033[91m[ERROR] URL switch did not complete properly\033[0m")
            return False
    except Exception as e:
        print(f"  \033[91m[ERROR] URL switch failed: {e}\033[0m")
        return False


def is_logged_in(page) -> bool:
    """Check if logged into Intuit (may need to navigate to QBO).

    Note: This returns False if on company selection screen - we need to select a company first.
    """
    # If on company selection screen, we're logged in but not ready
    if is_company_selection_screen(page):
        return False

    current_url = page.url
    # Check for QBO or account manager
    if any(x in current_url for x in ["qbo.intuit.com", "app/homepage", "app/dashboard", "c/bkg/"]):
        return True
    # Check for account manager (logged in but not in QBO)
    if "account-manager" in current_url:
        return True
    return False


def do_login(project: str, page=None, pw=None) -> tuple:
    """Perform QBO login for specified project.

    Args:
        project: Project name (TCO, Construction)
        page: Optional existing Playwright page
        pw: Optional existing Playwright instance

    Returns:
        Tuple of (playwright, browser, page) or raises Exception
    """
    account = ACCOUNTS.get(project)
    if not account:
        raise ValueError(f"Unknown project: {project}. Available: {list(ACCOUNTS.keys())}")

    # Start Chrome if needed
    if not start_chrome():
        raise ConnectionError("Could not start Chrome")

    # Connect to Chrome
    own_pw = pw is None
    if own_pw:
        pw = sync_playwright().start()

    try:
        print("  \033[90mConnecting to Chrome...\033[0m")
        browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{CHROME_DEBUG_PORT}")

        # Get context and page
        if browser.contexts:
            context = browser.contexts[0]
            if context.pages:
                page = context.pages[0]
            else:
                page = context.new_page()
        else:
            context = browser.new_context()
            page = context.new_page()

        # Check if already in QBO
        if is_in_qbo(page):
            print("  \033[92m[OK] Already in QBO!\033[0m")
            return pw, browser, page

        # Check if on company selection screen - need to select company first
        if is_company_selection_screen(page):
            print("  \033[93m[INFO] On company selection screen\033[0m")
            if select_company(page, "Vista consolidada"):
                if is_in_qbo(page):
                    print("  \033[92m[OK] Now in QBO!\033[0m")
                    return pw, browser, page

        # Check if logged into Intuit but not in QBO
        if is_logged_in(page):
            print("  \033[90mLogged into Intuit, navigating to QBO...\033[0m")
            page.goto("https://qbo.intuit.com/app/homepage")
            time.sleep(5)
            if is_in_qbo(page):
                print("  \033[92m[OK] Now in QBO!\033[0m")
                return pw, browser, page
            # May have redirected to company selection
            if is_company_selection_screen(page):
                if select_company(page, "Vista consolidada"):
                    if is_in_qbo(page):
                        print("  \033[92m[OK] Now in QBO!\033[0m")
                        return pw, browser, page

        # Navigate to login
        print("  \033[90mNavigating to login page...\033[0m")
        page.goto("https://accounts.intuit.com/app/sign-in")
        time.sleep(2)

        # Try to find saved account
        try:
            saved_account = page.locator(f'text="{account["email"]}"').first
            if saved_account.is_visible(timeout=2000):
                print("  \033[93m[INFO] Found saved account, selecting...\033[0m")
                saved_account.click()
                time.sleep(2)
            else:
                raise Exception("Account not visible")
        except Exception:
            # Conta salva não encontrada - tentar "use another account"
            try:
                other_btn = page.locator(
                    'button:has-text("Use a different account"), button:has-text("Utilize uma conta diferente")'
                ).first
                if other_btn.is_visible(timeout=1000):
                    other_btn.click()
                    time.sleep(1.5)
            except Exception:
                # Botão "use another account" não disponível
                pass

            # Fill email
            try:
                email_input = page.get_by_test_id("IdentifierFirstIdentifierInput")
                email_input.wait_for(state="visible", timeout=5000)
                email_input.fill(account["email"])
                time.sleep(0.3)
                page.get_by_test_id("IdentifierFirstSubmitButton").click()
                time.sleep(2)
            except Exception:
                # Campo de email não encontrado - pode já estar logado
                pass

        # Check if already in
        if is_logged_in(page):
            print("  \033[92m[OK] Logged in!\033[0m")
            return pw, browser, page

        # Enter password
        try:
            password_input = page.get_by_test_id("currentPasswordInput")
            password_input.wait_for(state="visible", timeout=8000)
            print("  \033[90mEntering password...\033[0m")
            password_input.fill(account["password"])
            time.sleep(0.5)
            page.get_by_test_id("passwordVerificationContinueButton").click()
            time.sleep(4)
        except Exception:
            # Campo de senha não encontrado - pode não precisar de senha
            pass

        # Check if already in
        if is_logged_in(page):
            print("  \033[92m[OK] Logged in!\033[0m")
            return pw, browser, page

        # Enter TOTP
        try:
            totp_input = page.get_by_test_id("VerifySoftTokenInput")
            totp_input.wait_for(state="visible", timeout=5000)

            # Wait for fresh TOTP if close to expiry
            remaining = 30 - (int(time.time()) % 30)
            if remaining < 5:
                print("  \033[90mWaiting for fresh TOTP code...\033[0m")
                time.sleep(remaining + 1)

            code = generate_totp(account["totp_secret"])
            print("  \033[90mEntering TOTP code...\033[0m")
            totp_input.fill(code)
            time.sleep(0.5)
            page.get_by_test_id("VerifySoftTokenSubmitButton").click()
            time.sleep(3)
        except Exception:
            # TOTP não solicitado - sessão pode já estar válida
            pass

        # Skip passkey prompt if present
        try:
            skip = page.locator('button:has-text("Ignorar"), button:has-text("Skip")')
            if skip.is_visible(timeout=2000):
                skip.click()
                time.sleep(1)
        except Exception:
            # Prompt de passkey não apareceu
            pass

        # Wait for login to complete
        time.sleep(3)

        # Navigate to QBO
        current_url = page.url
        if "account-manager" in current_url or ("accounts.intuit.com" in current_url and "sign-in" not in current_url):
            print("  \033[90mNavigating to QuickBooks Online...\033[0m")
            page.goto("https://app.qbo.intuit.com")
            time.sleep(5)

        # Check if company selection screen appears
        current_url = page.url
        page_content = page.content().lower()

        # Detect company selection screen (various URL patterns and page content)
        is_company_selection = (
            "sign-in" in current_url
            or "restaure" in page_content  # Portuguese "Restaure sua empresa"
            or "restore" in page_content  # English "Restore your company"
            or "select" in page_content  # "Select a company"
            or "intuit enterprise suite" in page_content
        )

        if is_company_selection and "qbo.intuit.com" not in current_url:
            # Company selection screen - select Vista consolidada (Consolidated View)
            try:
                print("  \033[90mCompany selection screen detected, selecting company...\033[0m")
                # Try to find consolidated view or first company
                selectors = [
                    "text=Vista consolidada",
                    "text=Consolidated View",
                    "text=Consolidated view",
                    'div:has-text("Vista consolidada")',
                    'div:has-text("Consolidated")',
                    "text=Apex Tire",  # Fallback to first company
                    "text=Apex",
                ]
                clicked = False
                for selector in selectors:
                    try:
                        company = page.locator(selector).first
                        if company.is_visible(timeout=2000):
                            company.click()
                            clicked = True
                            print(f"  \033[93m[INFO] Selected company via: {selector}\033[0m")
                            time.sleep(10)  # Wait for QBO to fully load
                            break
                    except Exception:
                        # Empresa não encontrada neste seletor - tentar próximo
                        continue

                if not clicked:
                    # Try clicking the first visible company option
                    try:
                        first_company = page.locator('[class*="company"], [class*="account"], [role="button"]').first
                        if first_company.is_visible(timeout=2000):
                            first_company.click()
                            print("  \033[93m[INFO] Selected first available company\033[0m")
                            time.sleep(10)
                    except Exception:
                        # Nenhuma empresa visível para clicar
                        pass
            except Exception as e:
                print(f"  \033[93m[WARN] Company selection failed: {str(e)[:50]}\033[0m")

        # Final check
        current_url = page.url
        if "qbo.intuit.com" in current_url:
            print("  \033[92m[OK] Login successful - QBO ready!\033[0m")
        else:
            print("  \033[93m[WARN] May need manual navigation to QBO\033[0m")
            print(f"  Current URL: {current_url[:60]}...")

        return pw, browser, page

    except Exception as e:
        if own_pw:
            pw.stop()
        raise e


def ensure_logged_in(project: str) -> tuple:
    """Ensure user is logged in, performing login if needed.

    Args:
        project: Project name

    Returns:
        Tuple of (playwright, browser, page)
    """
    print(f"\n  \033[97mEnsuring login for: {project}\033[0m")
    pw, browser, page = do_login(project)

    # Check if we need to select a company
    if is_company_selection_screen(page):
        select_company(page, "Vista consolidada")

    return pw, browser, page


def start_round(project: str, company: str = None) -> tuple:
    """Start a new test round with login and company selection.

    This is the CANONICAL entry point for all test sessions.
    A "round" is defined as: Login + Company Selection

    Args:
        project: Project name (TCO, Construction)
        company: Company key (apex, global, traction, consolidated) or None for default

    Returns:
        Tuple of (playwright, browser, page)

    Example:
        # Start round with Apex Tire
        pw, browser, page = start_round('TCO', 'apex')

        # Start round with default company
        pw, browser, page = start_round('TCO')
    """
    account = ACCOUNTS.get(project)
    if not account:
        raise ValueError(f"Unknown project: {project}. Available: {list(ACCOUNTS.keys())}")

    # Get target company name
    if company is None:
        company = account.get("default_company", "consolidated")

    companies = account.get("companies", {})
    company_name = companies.get(company, company)  # Use key as fallback

    print(f"\n{'=' * 50}")
    print("  STARTING ROUND")
    print(f"  User: {account['email']}")
    print(f"  Company: {company_name}")
    print(f"{'=' * 50}\n")

    # Step 1: Login
    print("  \033[97m[Step 1/2] Login...\033[0m")
    pw, browser, page = do_login(project)

    # Step 2: Select company (prefer URL-based switching)
    print(f"  \033[97m[Step 2/2] Select company: {company_name}...\033[0m")

    # Check if we have a company ID for URL-based switching
    company_ids = account.get("company_ids", {})
    has_company_id = company in company_ids

    if has_company_id and is_in_qbo(page):
        # PREFERRED: Use URL-based company switching
        switch_company_by_url(page, project, company)
    elif is_company_selection_screen(page):
        # On company selection screen - select directly (UI method)
        if not select_company(page, company_name):
            print("  \033[91m[ERROR] Failed to select company from selection screen\033[0m")
    elif is_in_qbo(page):
        # Already in QBO - try URL switch first, fallback to UI
        if has_company_id:
            switch_company_by_url(page, project, company)
        else:
            # Check if we need to switch by looking at current company in header
            try:
                current_company = page.locator("header").inner_text()
                if company_name.lower() not in current_company.lower():
                    print("  \033[93m[INFO] Need to switch company...\033[0m")
                    switch_company(page, company_name)
            except Exception:
                # Header não acessível - continuar sem verificar empresa atual
                pass

    # Verify we're in QBO
    if is_in_qbo(page):
        print("\n  \033[92m[OK] Round started successfully!\033[0m")
        print(f"  \033[92m    User: {account['email']}\033[0m")
        print(f"  \033[92m    Company: {company_name}\033[0m\n")
    else:
        print("\n  \033[91m[ERROR] Could not complete round setup\033[0m")
        print(f"  Current URL: {page.url}\n")

    return pw, browser, page
