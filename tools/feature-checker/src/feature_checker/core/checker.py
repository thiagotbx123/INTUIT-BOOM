"""Main feature checker orchestrator."""

import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..auth.login import LoginHandler
from ..navigation.navigator import Navigator
from ..utils.config import CheckConfig, get_config
from ..utils.screenshot import ScreenshotManager, get_element_bbox
from .browser import BrowserManager
from .content_scanner import ContentScanner
from .reporter import Reporter


@dataclass
class CheckResult:
    """Result of a single check."""

    check_id: str
    name: str
    status: str  # PASS, FAIL, PARTIAL, SKIP
    message: str = ""
    screenshot: Optional[Path] = None
    duration_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    details: Dict[str, Any] = field(default_factory=dict)


class FeatureChecker:
    """
    Main orchestrator for running health checks.

    Usage:
        checker = FeatureChecker("qbo")
        checker.login(credentials)
        results = checker.run_all_checks()
        checker.generate_report()
    """

    def __init__(self, product_name: str, project: str = None):
        """
        Initialize feature checker.

        Args:
            product_name: Product to check (e.g., "qbo")
            project: Specific project/environment
        """
        self.config = get_config()
        self.product = self.config.load_product(product_name)
        self.project = project

        self.browser = BrowserManager()
        self.screenshots = ScreenshotManager()
        self.reporter = Reporter(product_name, project)
        self.results: List[CheckResult] = []

        self.navigator: Optional[Navigator] = None
        self.login_handler: Optional[LoginHandler] = None

    def connect(self) -> None:
        """Connect to browser."""
        pw, browser, page = self.browser.connect()
        self.navigator = Navigator(page, self.product.base_url)
        self.login_handler = LoginHandler(page, self.product.auth)

    def disconnect(self) -> None:
        """Disconnect from browser."""
        self.browser.disconnect()

    def login(self, credentials: Dict[str, str] = None) -> bool:
        """
        Perform login.

        Args:
            credentials: Optional credentials dict

        Returns:
            True if login successful
        """
        if not credentials:
            credentials = self.config.get_credentials(self.product.name)

        return self.login_handler.login(credentials)

    def run_check(self, check: CheckConfig) -> CheckResult:
        """
        Run a single health check.

        Args:
            check: Check configuration

        Returns:
            CheckResult
        """
        start_time = time.time()
        page = self.browser.get_page()

        print(f"  [{check.priority.upper()}] {check.name}...")

        try:
            # Navigate to feature
            if check.route:
                success, message = self.navigator.navigate_to_feature(
                    {
                        "route": check.route,
                        "wait_for": check.expect.get("selector"),
                    }
                )
                if not success:
                    return self._create_result(check, "FAIL", message, start_time)

            # Run validation
            status, message = self._validate_check(check)

            # Capture screenshot
            screenshot = None
            if check.type in ("navigation", "ui") or status != "PASS":
                filename = self.screenshots.generate_filename(
                    self.product.name, self.project or "default", check.name
                )
                screenshot_path = self.config.evidence_dir / filename
                page.screenshot(path=str(screenshot_path), full_page=True)

                # Add annotation if highlight config
                if check.highlight:
                    selector = check.highlight.get("selector")
                    if selector:
                        bbox = get_element_bbox(page, selector)
                        if bbox:
                            self.screenshots.annotate(
                                screenshot_path,
                                bbox,
                                check.highlight.get("type", "box"),
                                check.name,
                            )
                screenshot = screenshot_path

            return self._create_result(check, status, message, start_time, screenshot)

        except Exception as e:
            return self._create_result(check, "FAIL", str(e), start_time)

    def _validate_check(self, check: CheckConfig) -> tuple:
        """
        Validate check expectations.

        Returns:
            Tuple of (status, message)
        """
        expect = check.expect
        page = self.browser.get_page()

        # URL contains
        if url_contains := expect.get("url_contains"):
            if url_contains not in page.url:
                return "FAIL", f"URL does not contain '{url_contains}'"

        # Selector exists
        if selector := expect.get("selector"):
            if not self.navigator.element_exists(selector):
                return "FAIL", f"Element not found: {selector}"

        # Minimum count
        if (selector := expect.get("selector")) and (min_count := expect.get("min_count")):
            count = self.navigator.count_elements(selector)
            if count < min_count:
                return "FAIL", f"Found {count} elements, expected >= {min_count}"

        # Text contains
        if text := expect.get("text"):
            if selector := expect.get("selector"):
                element_text = self.navigator.get_element_text(selector)
                if not element_text or text not in element_text:
                    return "FAIL", f"Text '{text}' not found"

        # Status code (for API checks)
        if expect.get("status"):
            # API validation would go here
            pass

        # Content scan (profanity, placeholders, gaffes)
        if content_scan := expect.get("content_scan"):
            scanner = ContentScanner(
                sensitivity=content_scan.get("sensitivity", "medium"),
                extra_patterns=content_scan.get("extra_patterns", []),
            )
            # Get page text content
            page_text = page.inner_text("body")
            violations = scanner.scan_text(page_text, f"Page: {page.url}")

            if violations:
                critical = [v for v in violations if v.severity == "CRITICAL"]
                if critical:
                    details = "; ".join(f"'{v.text}' @ {v.location}" for v in critical)
                    return "FAIL", f"CRITICAL content violations: {details}"
                high = [v for v in violations if v.severity == "HIGH"]
                if high:
                    details = "; ".join(f"'{v.text}' @ {v.location}" for v in high)
                    return "PARTIAL", f"Content warnings: {details}"

        return "PASS", "All validations passed"

    def _create_result(
        self,
        check: CheckConfig,
        status: str,
        message: str,
        start_time: float,
        screenshot: Path = None,
    ) -> CheckResult:
        """Create a CheckResult."""
        duration = int((time.time() - start_time) * 1000)

        result = CheckResult(
            check_id=check.id,
            name=check.name,
            status=status,
            message=message,
            screenshot=screenshot,
            duration_ms=duration,
        )

        # Log result
        status_icon = {"PASS": "✓", "FAIL": "✗", "PARTIAL": "◐", "SKIP": "○"}.get(status, "?")
        status_color = {"PASS": "\033[92m", "FAIL": "\033[91m", "PARTIAL": "\033[93m"}.get(
            status, ""
        )
        print(f"    {status_color}{status_icon} {status}\033[0m - {message}")

        self.results.append(result)
        return result

    def run_all_checks(self, checks: List[CheckConfig] = None) -> List[CheckResult]:
        """
        Run all checks for the product.

        Args:
            checks: Optional list of checks (defaults to product checks)

        Returns:
            List of CheckResults
        """
        checks = checks or self.product.checks

        if not checks:
            print("No checks configured for this product")
            return []

        print(f"\nRunning {len(checks)} checks for {self.product.name}")
        print("=" * 50)

        for i, check in enumerate(checks, 1):
            print(f"\n[{i}/{len(checks)}] {check.name}")

            # Reset to homepage between checks
            if i > 1:
                self.navigator.go_home()
                time.sleep(1)

            self.run_check(check)

        return self.results

    def get_summary(self) -> Dict[str, int]:
        """Get summary of results."""
        summary = {"total": len(self.results), "PASS": 0, "FAIL": 0, "PARTIAL": 0, "SKIP": 0}
        for result in self.results:
            summary[result.status] = summary.get(result.status, 0) + 1
        return summary

    def generate_report(self, format: str = "excel") -> Path:
        """
        Generate report from results.

        Args:
            format: Report format (excel, json, markdown)

        Returns:
            Path to generated report
        """
        return self.reporter.generate(self.results, format)

    def print_summary(self) -> None:
        """Print summary to console."""
        summary = self.get_summary()

        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(f"  Total: {summary['total']}")
        print(f"  \033[92mPASS: {summary['PASS']}\033[0m")
        print(f"  \033[91mFAIL: {summary['FAIL']}\033[0m")
        print(f"  \033[93mPARTIAL: {summary['PARTIAL']}\033[0m")
        print(f"  \033[90mSKIP: {summary['SKIP']}\033[0m")
