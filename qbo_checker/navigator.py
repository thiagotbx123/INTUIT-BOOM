# qbo_checker/navigator.py
"""QBO navigation engine using Playwright - with error protection"""

import json
import time
from playwright.sync_api import sync_playwright, Page

from .config import CHROME_DEBUG_PORT, CHROME_DEBUG_URL, FEATURES_JSON

# QBO Homepage URL
QBO_HOMEPAGE = "https://qbo.intuit.com/app/homepage"

# Company name for tests (TCO project) - focusing on single company for simplicity
COMPANY_NAME = "Apex Tire & Auto Retail, LLC"

# Error indicators on page - must be VERY specific phrases that indicate actual page errors
# These should only match actual error pages, not normal content
# Note: "this page isn't available" removed - appears in QBO help text
ERROR_INDICATORS = [
    "we're sorry, we can't find the page you requested",
    "page not found",
    "error loading page",
    "404 error",
    "500 error",
    "oops! something went wrong",
]


def load_features() -> list:
    """Load features from JSON config."""
    with open(FEATURES_JSON) as f:
        data = json.load(f)
    return data["features"]


def get_features_for_project(project: str) -> list:
    """Get features filtered by project."""
    features = load_features()
    return [f for f in features if project in f["projects"]]


def connect_to_chrome() -> tuple:
    """Connect to existing Chrome debug session."""
    pw = sync_playwright().start()

    try:
        browser = pw.chromium.connect_over_cdp(CHROME_DEBUG_URL)
    except Exception as e:
        pw.stop()
        raise ConnectionError(
            f"Could not connect to Chrome on port {CHROME_DEBUG_PORT}. "
            "Please run intuit_login_v2_4.py first to start Chrome."
        ) from e

    if browser.contexts:
        context = browser.contexts[0]
        if context.pages:
            page = context.pages[0]
        else:
            page = context.new_page()
    else:
        context = browser.new_context()
        page = context.new_page()

    return pw, browser, page


def is_error_page(page: Page) -> bool:
    """Check if current page shows an error."""
    try:
        page_text = page.content().lower()
        for indicator in ERROR_INDICATORS:
            if indicator.lower() in page_text:
                return True
    except Exception:
        # Erro ao acessar conteúdo da página
        pass
    return False


def is_page_loaded(page: Page, timeout: int = 5000) -> bool:
    """Wait for page to be fully loaded."""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
        return True
    except Exception:
        # Timeout ou erro de rede - página pode estar parcialmente carregada
        return False


def go_to_homepage(page: Page) -> bool:
    """Navigate to QBO homepage to reset state."""
    try:
        # Check if already on homepage
        if "/homepage" in page.url:
            print("    Already on homepage")
            return True

        print("    Resetting to homepage...")
        try:
            page.goto(QBO_HOMEPAGE, wait_until="domcontentloaded", timeout=10000)
        except Exception:
            # Timeout no primeiro método - tentar abordagem mais simples
            try:
                page.goto(QBO_HOMEPAGE, timeout=8000)
            except Exception:
                # Timeout persistente - verificar se página carregou parcialmente
                print("    [WARN] Goto timeout, checking page state...")
                if "qbo.intuit.com" in page.url:
                    print(f"    On QBO page: {page.url}")
                    return True
                return False

        time.sleep(2)
        return not is_error_page(page)
    except Exception as e:
        print(f"    [WARN] Homepage navigation failed: {str(e)[:50]}")
        # Even if failed, if we're on QBO, continue
        return "qbo.intuit.com" in page.url


def execute_click_path(page: Page, click_path: list) -> tuple:
    """Execute a series of navigation actions with error recovery."""
    for i, action in enumerate(click_path):
        action_type = action.get("action")
        selector = action.get("selector")
        timeout = action.get("timeout", 10000)

        try:
            if action_type == "wait":
                page.wait_for_selector(selector, timeout=timeout)

            elif action_type == "click":
                element = page.locator(selector).first
                element.wait_for(state="visible", timeout=timeout)
                element.click()
                time.sleep(1)

                if is_error_page(page):
                    return False, f"Error page after clicking: {selector}"

            elif action_type == "fill":
                value = action.get("value", "")
                element = page.locator(selector).first
                element.wait_for(state="visible", timeout=timeout)
                element.fill(value)

            elif action_type == "wait_for_text":
                text = action.get("text", "")
                page.wait_for_selector(f"text={text}", timeout=timeout)

        except Exception as e:
            return (
                False,
                f"Step {i + 1} failed ({action_type} on {selector}): {str(e)[:50]}",
            )

    return True, "Click path completed"


def validate_feature(page: Page, validation: dict) -> tuple:
    """Validate that feature elements exist on page."""
    if is_error_page(page):
        return False, "Error page detected"

    must_exist = validation.get("must_exist", [])
    must_contain = validation.get("must_contain_text", [])

    missing_elements = []
    missing_text = []

    for selector in must_exist:
        try:
            if not page.locator(selector).first.is_visible(timeout=3000):
                missing_elements.append(selector)
        except Exception:
            # Elemento não encontrado ou timeout
            missing_elements.append(selector)

    try:
        page_text = page.content()
        for text in must_contain:
            if text.lower() not in page_text.lower():
                missing_text.append(text)
    except Exception:
        # Erro ao acessar conteúdo da página para validação de texto
        pass

    if missing_elements or missing_text:
        details = []
        if missing_elements:
            details.append(f"Missing: {missing_elements}")
        if missing_text:
            details.append(f"Text not found: {missing_text}")
        return False, "; ".join(details)

    return True, "Validation passed"


def navigate_via_sidebar(page: Page, menu_items: list) -> tuple:
    """Navigate using the QBO left sidebar menu."""
    for item in menu_items:
        try:
            selectors = [
                f"nav >> text={item}",
                f"[role='navigation'] >> text={item}",
                f".left-nav >> text={item}",
                f"text={item}",
            ]

            clicked = False
            for selector in selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible(timeout=2000):
                        element.click()
                        clicked = True
                        time.sleep(1.5)
                        break
                except Exception:
                    # Seletor não encontrado - tentar próximo
                    continue

            if not clicked:
                return False, f"Could not find menu item: {item}"

            if is_error_page(page):
                return False, f"Error after clicking: {item}"

        except Exception as e:
            return False, f"Sidebar navigation failed at '{item}': {str(e)[:50]}"

    return True, "Sidebar navigation completed"


def navigate_via_url(page: Page, url: str) -> tuple:
    """Navigate directly to a URL."""
    try:
        print(f"    Going to URL: {url}")
        page.goto(url, wait_until="networkidle", timeout=20000)
        time.sleep(2)

        if is_error_page(page):
            return False, f"Error page at URL: {url}"

        return True, "URL navigation complete"
    except Exception as e:
        return False, f"URL navigation failed: {str(e)[:50]}"


def navigate_via_sidebar_click(page: Page, click_text: str) -> tuple:
    """Navigate by clicking a link in the left sidebar."""
    try:
        print(f"    Looking for sidebar link: '{click_text}'")

        # Give page time to be interactive
        time.sleep(1)

        # Try multiple strategies to find and click in sidebar
        selectors = [
            # QBO specific selectors
            f"[data-testid*='nav'] >> text={click_text}",
            f"[data-automation*='nav'] >> text={click_text}",
            # Role-based navigation
            f"nav >> text={click_text}",
            f"[role='navigation'] >> text={click_text}",
            f"[role='menuitem']:has-text('{click_text}')",
            # Class-based navigation
            f".left-nav >> text={click_text}",
            f"[class*='sidebar'] >> text={click_text}",
            f"[class*='nav'] >> text={click_text}",
            f"[class*='menu'] >> text={click_text}",
            # Generic elements with text
            f"a:has-text('{click_text}')",
            f"button:has-text('{click_text}')",
            f"li:has-text('{click_text}')",
            f"div[class*='nav']:has-text('{click_text}')",
            # Last resort - any text match
            f"text={click_text}",
            f"text='{click_text}'",
        ]

        clicked = False
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=1500):
                    element.click()
                    clicked = True
                    print(f"    Clicked sidebar: {selector}")
                    time.sleep(2)
                    break
            except Exception:
                # Seletor de sidebar não encontrado - tentar próximo
                continue

        # If still not clicked, try get_by_role or get_by_text
        if not clicked:
            try:
                element = page.get_by_role("link", name=click_text).first
                if element.is_visible(timeout=1500):
                    element.click()
                    clicked = True
                    print("    Clicked via role=link")
                    time.sleep(2)
            except Exception:
                # Link por role não encontrado
                pass

        if not clicked:
            try:
                element = page.get_by_text(click_text, exact=False).first
                if element.is_visible(timeout=1500):
                    element.click()
                    clicked = True
                    print("    Clicked via get_by_text")
                    time.sleep(2)
            except Exception:
                # Elemento por texto não encontrado
                pass

        if not clicked:
            return False, f"Could not find sidebar element: {click_text}"

        if is_error_page(page):
            return False, f"Error page after clicking sidebar: {click_text}"

        return True, "Sidebar click navigation complete"
    except Exception as e:
        return False, f"Sidebar click failed: {str(e)[:50]}"


def navigate_via_homepage_click(page: Page, click_text: str) -> tuple:
    """Navigate by clicking a link on the homepage."""
    try:
        # First ensure we're on the homepage
        if "homepage" not in page.url:
            print("    Navigating to homepage first...")
            page.goto(QBO_HOMEPAGE, wait_until="networkidle", timeout=15000)
            time.sleep(2)

        print(f"    Looking for link: '{click_text}'")

        # Try multiple strategies to find and click the text
        selectors = [
            f"text='{click_text}'",
            f"text={click_text}",
            f"a:has-text('{click_text}')",
            f"button:has-text('{click_text}')",
            f"[role='link']:has-text('{click_text}')",
            f"div:has-text('{click_text}')",
        ]

        clicked = False
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=3000):
                    element.click()
                    clicked = True
                    print(f"    Clicked: {selector}")
                    time.sleep(2)
                    break
            except Exception:
                # Seletor não encontrado na homepage - tentar próximo
                continue

        if not clicked:
            return False, f"Could not find clickable element: {click_text}"

        if is_error_page(page):
            return False, f"Error page after clicking: {click_text}"

        return True, "Homepage click navigation complete"
    except Exception as e:
        return False, f"Homepage click failed: {str(e)[:50]}"


def navigate_multi_step(page: Page, steps: list) -> tuple:
    """Execute multi-step navigation with detailed actions."""
    for i, step in enumerate(steps):
        action = step.get("action", "")

        try:
            if action == "goto":
                url = step.get("url", "")
                # Check if already on the target page
                current_url = page.url
                target_path = url.split("intuit.com")[-1] if "intuit.com" in url else url
                if target_path in current_url:
                    print(f"    Step {i + 1}: Already on {target_path}")
                    continue

                print(f"    Step {i + 1}: Going to {url}")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                except Exception:
                    # Timeout no goto - tentar abordagem alternativa
                    try:
                        page.goto(url, timeout=10000)
                        time.sleep(2)
                    except Exception:
                        # Timeout persistente - verificar se carregou parcialmente
                        print("    [WARN] Goto timeout, checking if page loaded anyway...")
                        if "qbo.intuit.com" in page.url:
                            print(f"    Page appears loaded: {page.url}")
                        else:
                            return False, f"Could not navigate to {url}"

            elif action == "wait":
                seconds = step.get("seconds", 2)
                print(f"    Step {i + 1}: Waiting {seconds}s")
                time.sleep(seconds)

            elif action == "verify_text":
                text = step.get("text", "")
                print(f"    Step {i + 1}: Verifying text '{text}'")
                if text.lower() not in page.content().lower():
                    return False, f"Text not found: {text}"

            elif action == "sidebar_click":
                text = step.get("text", "")
                print(f"    Step {i + 1}: Clicking sidebar '{text}'")
                success, details = navigate_via_sidebar_click(page, text)
                if not success:
                    return False, details

            elif action == "click":
                text = step.get("text", "")
                selector = step.get("selector", "")

                clicked = False

                # First try custom selector if provided (comma separated for multiple attempts)
                if selector:
                    print(f"    Step {i + 1}: Trying selector(s) for '{text or selector}'")
                    for sel in selector.split(", "):
                        try:
                            element = page.locator(sel.strip()).first
                            if element.is_visible(timeout=2000):
                                element.click()
                                clicked = True
                                print(f"    Clicked via selector: {sel.strip()}")
                                time.sleep(1.5)
                                break
                        except Exception:
                            # Seletor específico não encontrado - tentar próximo
                            continue

                # If selector didn't work, try text-based approach
                if not clicked and text:
                    print(f"    Step {i + 1}: Clicking '{text}' via text search")

                    # More comprehensive selectors for QBO UI
                    selectors = [
                        # Exact text matches first
                        f"text='{text}'",
                        f"text={text}",
                        # Links and buttons
                        f"a:has-text('{text}')",
                        f"button:has-text('{text}')",
                        # Role-based
                        f"[role='link']:has-text('{text}')",
                        f"[role='button']:has-text('{text}')",
                        f"[role='menuitem']:has-text('{text}')",
                        f"[role='option']:has-text('{text}')",
                        # Navigation specific
                        f"nav >> text={text}",
                        f"[class*='nav'] >> text={text}",
                        f"[class*='menu'] >> text={text}",
                        f"[class*='sidebar'] >> text={text}",
                        # Generic elements
                        f"li:has-text('{text}')",
                        f"div:has-text('{text}')",
                        f"span:has-text('{text}')",
                    ]

                    for sel in selectors:
                        try:
                            element = page.locator(sel).first
                            if element.is_visible(timeout=2000):
                                element.click()
                                clicked = True
                                print(f"    Clicked via: {sel}")
                                time.sleep(1.5)
                                break
                        except Exception:
                            # Seletor de texto não encontrado - tentar próximo
                            continue

                if not clicked:
                    fallback = step.get("fallback_text", "")
                    if fallback:
                        print(f"    Step {i + 1}: Trying fallback '{fallback}'")
                        try:
                            page.locator(f"text={fallback}").first.click()
                            clicked = True
                            time.sleep(1.5)
                        except Exception:
                            # Texto de fallback também não encontrado
                            pass

                if not clicked:
                    # Last resort: try scrolling and clicking
                    if text:
                        try:
                            print(f"    Step {i + 1}: Last resort - scroll and click '{text}'")
                            loc = page.get_by_text(text, exact=False).first
                            loc.scroll_into_view_if_needed()
                            time.sleep(0.5)
                            loc.click()
                            clicked = True
                            time.sleep(1.5)
                        except Exception:
                            # Último recurso falhou - elemento não clicável
                            pass

                if not clicked:
                    return False, f"Could not click: {text or selector}"

            if is_error_page(page):
                return False, f"Error page after step {i + 1}"

        except Exception as e:
            return False, f"Step {i + 1} failed: {str(e)[:50]}"

    return True, "Multi-step navigation complete"


def navigate_to_feature(page: Page, feature: dict) -> tuple:
    """Navigate to a feature with full error protection."""
    feature_name = feature["name"]
    navigation = feature.get("navigation", {})
    validation = feature.get("validation", {})
    wait_after_nav = feature.get("wait_after_nav", 3)

    print(f"  Navigating to {feature_name}...")

    nav_type = navigation.get("type", "")
    success = False
    details = "No navigation defined"

    # Strategy based on navigation type
    if nav_type == "multi_step":
        steps = navigation.get("steps", [])
        if steps:
            success, details = navigate_multi_step(page, steps)
        else:
            success, details = False, "No steps defined"

    elif nav_type == "url":
        url = navigation.get("url", "")
        if url:
            success, details = navigate_via_url(page, url)
        else:
            success, details = False, "No URL specified"

    elif nav_type == "homepage_click":
        click_text = navigation.get("click_text", "")
        if click_text:
            success, details = navigate_via_homepage_click(page, click_text)
        else:
            success, details = False, "No click_text specified"

    elif nav_type == "sidebar_click":
        click_text = navigation.get("click_text", "")
        if click_text:
            success, details = navigate_via_sidebar_click(page, click_text)
        else:
            success, details = False, "No click_text specified"

    elif nav_type == "sidebar":
        sidebar_items = navigation.get("items", [])
        if sidebar_items:
            success, details = navigate_via_sidebar(page, sidebar_items)
        else:
            success, details = False, "No sidebar items specified"

    # Legacy support for old click_path format
    elif feature.get("click_path"):
        success, details = execute_click_path(page, feature["click_path"])

    elif feature.get("sidebar_path"):
        success, details = navigate_via_sidebar(page, feature["sidebar_path"])

    else:
        # No navigation defined - might be current page
        success, details = True, "No navigation needed"

    if not success:
        print(f"    [WARN] Navigation failed: {details}")
        go_to_homepage(page)
        return False, details

    # Wait for page to fully load
    time.sleep(wait_after_nav)
    is_page_loaded(page, timeout=10000)

    # Final error check
    if is_error_page(page):
        print("    [ERROR] Error page detected after navigation")
        go_to_homepage(page)
        return False, "Error page after navigation"

    # Validate if defined
    if validation:
        return validate_feature(page, validation)

    return True, "Navigation complete"


def reset_to_homepage(page: Page) -> bool:
    """Reset to QBO homepage - call between features."""
    return go_to_homepage(page)
