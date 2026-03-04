"""Navigation engine for web applications."""

import time
from typing import Any, Dict, List, Optional, Tuple

from playwright.sync_api import Page


class Navigator:
    """
    Handles navigation within web applications.

    Supports:
    - URL-based navigation
    - Click-path navigation
    - Element waiting
    - Error detection
    """

    def __init__(self, page: Page, base_url: str):
        """
        Initialize navigator.

        Args:
            page: Playwright page instance
            base_url: Base URL of the application
        """
        self.page = page
        self.base_url = base_url.rstrip("/")

    def goto(self, path: str, wait_for: str = None, timeout: int = 30000) -> bool:
        """
        Navigate to a path.

        Args:
            path: URL path or full URL
            wait_for: Selector to wait for after navigation
            timeout: Navigation timeout in ms

        Returns:
            True if navigation successful
        """
        url = path if path.startswith("http") else f"{self.base_url}{path}"

        try:
            self.page.goto(url, timeout=timeout)
            self.page.wait_for_load_state("networkidle", timeout=timeout)

            if wait_for:
                self.page.wait_for_selector(wait_for, timeout=timeout)

            return True
        except Exception as e:
            print(f"  [ERROR] Navigation failed: {e}")
            return False

    def navigate_by_clicks(self, clicks: List[str], timeout: int = 5000) -> bool:
        """
        Navigate by clicking elements in sequence.

        Args:
            clicks: List of selectors or text to click
            timeout: Timeout per click in ms

        Returns:
            True if all clicks successful
        """
        for click_target in clicks:
            try:
                # Try as selector first
                try:
                    self.page.click(click_target, timeout=timeout)
                except Exception:
                    # Try as text
                    self.page.click(f"text={click_target}", timeout=timeout)

                time.sleep(0.5)  # Brief pause between clicks
            except Exception as e:
                print(f"  [ERROR] Click failed: {click_target} - {e}")
                return False

        return True

    def navigate_to_feature(self, feature: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Navigate to a feature based on its configuration.

        Args:
            feature: Feature configuration dict

        Returns:
            Tuple of (success, details)
        """
        feature_name = feature.get("name", "Unknown")

        # Method 1: Direct route
        if route := feature.get("route"):
            wait_for = feature.get("wait_for")
            if self.goto(route, wait_for=wait_for):
                return True, f"Navigated to {route}"
            # Continue to try fallback methods

        # Method 2: Click path
        if clicks := feature.get("clicks"):
            if self.navigate_by_clicks(clicks):
                return True, "Navigated via clicks"

        # Method 3: Navigation config
        if nav := feature.get("navigation"):
            if route := nav.get("route"):
                if self.goto(route, wait_for=nav.get("wait_for")):
                    # Additional clicks if needed
                    if clicks := nav.get("clicks"):
                        self.navigate_by_clicks(clicks)
                    return True, f"Navigated to {route}"

        return False, f"Could not navigate to {feature_name}"

    def go_home(self, home_path: str = "/app/homepage") -> bool:
        """
        Navigate to application homepage.

        Args:
            home_path: Path to homepage

        Returns:
            True if successful
        """
        return self.goto(home_path)

    def wait_for_element(self, selector: str, timeout: int = 10000, state: str = "visible") -> bool:
        """
        Wait for element to be in specified state.

        Args:
            selector: CSS selector
            timeout: Wait timeout in ms
            state: Expected state (visible, hidden, attached, detached)

        Returns:
            True if element found in state
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state=state)
            return True
        except Exception:
            return False

    def element_exists(self, selector: str) -> bool:
        """
        Check if element exists on page.

        Args:
            selector: CSS selector

        Returns:
            True if element exists
        """
        return self.page.query_selector(selector) is not None

    def get_element_text(self, selector: str) -> Optional[str]:
        """
        Get text content of element.

        Args:
            selector: CSS selector

        Returns:
            Element text or None
        """
        element = self.page.query_selector(selector)
        return element.text_content() if element else None

    def count_elements(self, selector: str) -> int:
        """
        Count elements matching selector.

        Args:
            selector: CSS selector

        Returns:
            Number of matching elements
        """
        return len(self.page.query_selector_all(selector))

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url
