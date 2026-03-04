"""Browser management using Playwright."""

import os
import socket
import subprocess
import time
from typing import Optional, Tuple

from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from ..utils.config import get_config


class BrowserManager:
    """
    Manages Chrome browser instance for feature checking.

    Supports:
    - Starting Chrome with debug port
    - Connecting to existing Chrome instance
    - Session persistence across checks
    """

    def __init__(self):
        """Initialize browser manager."""
        self.config = get_config()
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

        # Chrome profile directory
        self.user_data_dir = os.path.join(
            os.environ.get("TEMP", "/tmp"), "feature_checker_chrome_profile"
        )

    def is_port_open(self, port: int = None) -> bool:
        """Check if debug port is open."""
        port = port or self.config.chrome_debug_port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(("127.0.0.1", port)) == 0

    def start_chrome(self) -> bool:
        """
        Start Chrome browser with remote debugging.

        Returns:
            True if Chrome started successfully
        """
        if self.is_port_open():
            print("  [INFO] Chrome already running, connecting...")
            return True

        print("  Starting Chrome...")
        os.makedirs(self.user_data_dir, exist_ok=True)

        cmd = [
            self.config.chrome_path,
            f"--remote-debugging-port={self.config.chrome_debug_port}",
            f"--user-data-dir={self.user_data_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ]

        # Platform-specific process creation
        if os.name == "nt":  # Windows
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
        else:  # Unix
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
            )

        # Wait for Chrome to start
        print("  Waiting for Chrome...")
        for _ in range(30):
            if self.is_port_open():
                time.sleep(0.5)
                return True
            time.sleep(0.5)

        return False

    def connect(self) -> Tuple[Playwright, Browser, Page]:
        """
        Connect to Chrome browser.

        Returns:
            Tuple of (playwright, browser, page)

        Raises:
            ConnectionError: If cannot connect to Chrome
        """
        if not self.start_chrome():
            raise ConnectionError("Failed to start Chrome browser")

        debug_url = f"http://127.0.0.1:{self.config.chrome_debug_port}"

        self.playwright = sync_playwright().start()

        try:
            self.browser = self.playwright.chromium.connect_over_cdp(debug_url)
        except Exception as e:
            self.playwright.stop()
            raise ConnectionError(
                f"Could not connect to Chrome on port {self.config.chrome_debug_port}"
            ) from e

        # Get or create page
        if self.browser.contexts:
            context = self.browser.contexts[0]
            self.page = context.pages[0] if context.pages else context.new_page()
        else:
            context = self.browser.new_context()
            self.page = context.new_page()

        return self.playwright, self.browser, self.page

    def disconnect(self) -> None:
        """Disconnect from browser (keeps Chrome running)."""
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
            self.browser = None
            self.page = None

    def close(self) -> None:
        """Close browser completely."""
        if self.browser:
            self.browser.close()
        self.disconnect()

    def get_page(self) -> Page:
        """
        Get current page, connecting if needed.

        Returns:
            Playwright Page instance
        """
        if not self.page:
            self.connect()
        return self.page

    def take_screenshot(self, path: str) -> str:
        """
        Take screenshot of current page.

        Args:
            path: Output file path

        Returns:
            Saved file path
        """
        self.page.screenshot(path=path, full_page=True)
        return path

    def is_error_page(self) -> bool:
        """Check if current page shows an error."""
        error_indicators = [
            "page not found",
            "404 error",
            "500 error",
            "something went wrong",
            "we're sorry",
        ]

        try:
            content = self.page.content().lower()
            return any(indicator in content for indicator in error_indicators)
        except Exception:
            return False
