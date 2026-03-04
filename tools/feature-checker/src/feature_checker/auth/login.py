"""Login handler for browser-based authentication."""

import time
from typing import Any, Dict

from playwright.sync_api import Page

from .totp import generate_totp, wait_for_fresh_totp


class LoginHandler:
    """
    Handles browser-based login flows.

    Supports:
    - Basic username/password
    - OAuth flows
    - TOTP/MFA
    - Session persistence
    """

    def __init__(self, page: Page, config: Dict[str, Any]):
        """
        Initialize login handler.

        Args:
            page: Playwright page instance
            config: Authentication configuration
        """
        self.page = page
        self.config = config
        self.auth_type = config.get("type", "basic")

    def login(self, credentials: Dict[str, str]) -> bool:
        """
        Perform login with given credentials.

        Args:
            credentials: Dict with email, password, and optionally totp_secret

        Returns:
            True if login successful
        """
        if self.is_logged_in():
            return True

        method = getattr(self, f"_login_{self.auth_type}", self._login_basic)
        return method(credentials)

    def is_logged_in(self) -> bool:
        """
        Check if currently logged in.

        Returns:
            True if logged in
        """
        # Check for common logged-in indicators
        indicators = self.config.get("logged_in_indicators", [])

        if not indicators:
            # Default: check URL doesn't contain login
            return "login" not in self.page.url.lower()

        for indicator in indicators:
            if indicator.get("type") == "url_contains":
                if indicator["value"] in self.page.url:
                    return True
            elif indicator.get("type") == "selector_exists":
                if self.page.query_selector(indicator["value"]):
                    return True

        return False

    def _login_basic(self, credentials: Dict[str, str]) -> bool:
        """Basic username/password login."""
        login_url = self.config.get("login_url", "/login")

        # Navigate to login
        if login_url not in self.page.url:
            self.page.goto(login_url)

        # Fill credentials
        email_selector = self.config.get("email_selector", 'input[type="email"]')
        password_selector = self.config.get("password_selector", 'input[type="password"]')
        submit_selector = self.config.get("submit_selector", 'button[type="submit"]')

        self.page.fill(email_selector, credentials["email"])
        self.page.fill(password_selector, credentials["password"])
        self.page.click(submit_selector)

        # Wait for navigation
        self.page.wait_for_load_state("networkidle", timeout=30000)

        return self.is_logged_in()

    def _login_oauth_totp(self, credentials: Dict[str, str]) -> bool:
        """OAuth login with TOTP MFA (e.g., Intuit)."""
        login_url = self.config.get("login_url")

        # Navigate to login
        self.page.goto(login_url)
        self.page.wait_for_load_state("networkidle")

        # Step 1: Email
        email_selector = self.config.get("email_selector", "#ius-identifier")
        self.page.fill(email_selector, credentials["email"])
        self.page.click(self.config.get("email_submit", "#ius-sign-in-submit-btn"))

        time.sleep(2)

        # Step 2: Password
        password_selector = self.config.get(
            "password_selector", "#ius-sign-in-mfa-password-collection-current-password"
        )
        self.page.wait_for_selector(password_selector, timeout=10000)
        self.page.fill(password_selector, credentials["password"])
        self.page.click(
            self.config.get("password_submit", "#ius-sign-in-mfa-password-collection-continue-btn")
        )

        time.sleep(2)

        # Step 3: TOTP
        if credentials.get("totp_secret"):
            totp_selector = self.config.get("totp_selector", "#ius-mfa-soft-token")

            try:
                self.page.wait_for_selector(totp_selector, timeout=10000)

                # Wait for fresh TOTP
                wait_for_fresh_totp(min_seconds=5)
                code = generate_totp(credentials["totp_secret"])

                self.page.fill(totp_selector, code)
                self.page.click(self.config.get("totp_submit", "#ius-mfa-soft-token-submit-btn"))

                time.sleep(3)
            except Exception:
                # TOTP might not be required if session is remembered
                pass

        # Handle "Skip" or "Not Now" prompts
        self._handle_post_login_prompts()

        return self.is_logged_in()

    def _handle_post_login_prompts(self) -> None:
        """Handle common post-login prompts like 'Skip', 'Not Now', etc."""
        skip_selectors = [
            "text=Skip",
            "text=Not now",
            "text=Maybe later",
            '[data-testid="skip-btn"]',
        ]

        for selector in skip_selectors:
            try:
                element = self.page.wait_for_selector(selector, timeout=3000)
                if element:
                    element.click()
                    time.sleep(1)
            except Exception:
                continue

    def logout(self) -> None:
        """Perform logout."""
        logout_url = self.config.get("logout_url")
        if logout_url:
            self.page.goto(logout_url)
        else:
            # Try common logout patterns
            logout_selectors = [
                "text=Sign out",
                "text=Log out",
                "text=Logout",
                '[data-testid="logout-btn"]',
            ]
            for selector in logout_selectors:
                try:
                    self.page.click(selector, timeout=3000)
                    return
                except Exception:
                    continue
