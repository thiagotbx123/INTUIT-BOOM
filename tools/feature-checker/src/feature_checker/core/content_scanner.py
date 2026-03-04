"""Content scanner for detecting profanity, gaffes, and inappropriate data in demo environments."""

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ContentViolation:
    """A single content violation found during scanning."""

    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # profanity, placeholder, test_data, pii, nonsense, offensive
    text: str  # The offending text
    location: str  # Where it was found (page, field, etc.)
    context: str = ""  # Surrounding text for context
    suggestion: str = ""  # Suggested fix


# Profanity / offensive word list (English + Portuguese common terms)
# This is intentionally conservative — better to flag false positives than miss real issues
PROFANITY_PATTERNS = [
    # English
    r"\bdick(?:s|head|weed)?\b",
    r"\bfuck(?:ing|ed|er|s)?\b",
    r"\bshit(?:ty|s|head)?\b",
    r"\bass(?:hole|es|wipe)?\b",
    r"\bbitch(?:es|ing)?\b",
    r"\bbastard(?:s)?\b",
    r"\bdamn(?:ed|it)?\b",
    r"\bcrap(?:py|s)?\b",
    r"\bhell\b",  # Only as standalone (not "hello", "shell")
    r"\bpiss(?:ed|ing|s)?\b",
    r"\bcunt(?:s)?\b",
    r"\bwhore(?:s)?\b",
    r"\bslut(?:s)?\b",
    r"\bnigger(?:s)?\b",
    r"\bfaggot(?:s)?\b",
    r"\bretard(?:ed|s)?\b",
    # Portuguese
    r"\bmerda(?:s)?\b",
    r"\bporra(?:s)?\b",
    r"\bcaralho\b",
    r"\bputa(?:s)?\b",
    r"\bviado(?:s)?\b",
    r"\bfodido(?:s|a|as)?\b",
    r"\bfoder\b",
    r"\bcaçete\b",
    r"\bdesgraça(?:do|da|dos|das)?\b",
]

# Placeholder / test data patterns that look unprofessional
PLACEHOLDER_PATTERNS = [
    r"\btest\s*(?:123|456|789|data|user|account|company)\b",
    r"\bfoo(?:bar|baz)?\b",
    r"\bloremipsum\b",
    r"\basdf(?:ghjkl?)?\b",
    r"\bxxx+\b",
    r"\bzzz+\b",
    r"\btodo\b",
    r"\bfixme\b",
    r"\bhack\b",
    r"\bplaceholder\b",
    r"\bsample\s*data\b",
    r"\bdummy\b",
    r"\bblah\b",
    r"\bn/a\b",
]

# PII patterns that shouldn't be in demo data
PII_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
    r"\b\d{3}\.\d{2}\.\d{4}\b",  # SSN with dots
    r"\b(?:4[0-9]{12}(?:[0-9]{3})?)\b",  # Visa
    r"\b(?:5[1-5][0-9]{14})\b",  # Mastercard
    r"\b[A-Za-z0-9._%+-]+@(?!tbxofficial|testbox|example|test)\S+\.\S+\b",  # Real emails
]

# Nonsense / gibberish detection (consecutive consonants or too-random strings)
NONSENSE_PATTERNS = [
    r"\b[bcdfghjklmnpqrstvwxyz]{5,}\b",  # 5+ consecutive consonants
    r"\b[A-Z]{8,}\b",  # 8+ uppercase letters (likely test data)
]


class ContentScanner:
    """
    Scans page content for inappropriate, unprofessional, or problematic text.

    Designed for QBO/TestBox demo environments where data quality matters
    because prospects see it during demos.

    Usage:
        scanner = ContentScanner()
        violations = scanner.scan_text("This is some dicks text", "Dimensions > Values")
        scanner.scan_page_snapshot(snapshot_text, "Customers Page")
    """

    def __init__(self, extra_patterns: List[str] = None, sensitivity: str = "medium"):
        """
        Initialize scanner.

        Args:
            extra_patterns: Additional regex patterns to flag
            sensitivity: "low" (profanity only), "medium" (+placeholders), "high" (+PII, nonsense)
        """
        self.sensitivity = sensitivity
        self.violations: List[ContentViolation] = []
        self.extra_patterns = extra_patterns or []

        # Build pattern sets based on sensitivity
        self._patterns = self._build_patterns()

    def _build_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Build compiled regex patterns based on sensitivity level."""
        patterns = {
            "profanity": [re.compile(p, re.IGNORECASE) for p in PROFANITY_PATTERNS],
        }

        if self.sensitivity in ("medium", "high"):
            patterns["placeholder"] = [re.compile(p, re.IGNORECASE) for p in PLACEHOLDER_PATTERNS]

        if self.sensitivity == "high":
            patterns["pii"] = [re.compile(p) for p in PII_PATTERNS]
            patterns["nonsense"] = [re.compile(p, re.IGNORECASE) for p in NONSENSE_PATTERNS]

        if self.extra_patterns:
            patterns["custom"] = [re.compile(p, re.IGNORECASE) for p in self.extra_patterns]

        return patterns

    def scan_text(self, text: str, location: str = "unknown") -> List[ContentViolation]:
        """
        Scan a text string for violations.

        Args:
            text: Text to scan
            location: Description of where this text came from

        Returns:
            List of violations found
        """
        found = []

        for category, patterns in self._patterns.items():
            severity = self._category_severity(category)

            for pattern in patterns:
                for match in pattern.finditer(text):
                    # Get context (surrounding text)
                    start = max(0, match.start() - 30)
                    end = min(len(text), match.end() + 30)
                    context = text[start:end].strip()

                    violation = ContentViolation(
                        severity=severity,
                        category=category,
                        text=match.group(),
                        location=location,
                        context=f"...{context}...",
                        suggestion=self._get_suggestion(category, match.group()),
                    )
                    found.append(violation)
                    self.violations.append(violation)

        return found

    def scan_items(self, items: List[str], location: str = "unknown") -> List[ContentViolation]:
        """
        Scan a list of text items (e.g., dimension values, customer names).

        Args:
            items: List of text strings to scan
            location: Description of the data source

        Returns:
            List of violations found
        """
        found = []
        for i, item in enumerate(items):
            item_location = f"{location} > item {i + 1}: '{item}'"
            found.extend(self.scan_text(item, item_location))
        return found

    def scan_page_snapshot(self, snapshot: str, page_name: str) -> List[ContentViolation]:
        """
        Scan a Playwright accessibility snapshot for violations.

        Args:
            snapshot: Raw snapshot text from browser_snapshot
            page_name: Name of the page being scanned

        Returns:
            List of violations found
        """
        # Extract text content from snapshot (strip refs and metadata)
        lines = snapshot.split("\n")
        text_content = []

        for line in lines:
            # Extract text from snapshot entries like: - text: "Some text"
            # or cell "Some text" or heading "Some text" etc.
            text_matches = re.findall(r'"([^"]+)"', line)
            text_content.extend(text_matches)

            # Also extract bare text content
            text_matches = re.findall(r":\s+(.+?)(?:\s+\[ref=|$)", line)
            text_content.extend(text_matches)

        all_text = " ".join(text_content)
        return self.scan_text(all_text, f"Page: {page_name}")

    def _category_severity(self, category: str) -> str:
        """Map category to severity level."""
        return {
            "profanity": "CRITICAL",
            "pii": "CRITICAL",
            "custom": "HIGH",
            "placeholder": "MEDIUM",
            "nonsense": "LOW",
        }.get(category, "MEDIUM")

    def _get_suggestion(self, category: str, text: str) -> str:
        """Get a fix suggestion for a violation."""
        suggestions = {
            "profanity": f"Remove or rename '{text}' — this is visible to demo prospects",
            "placeholder": f"Replace '{text}' with realistic business data",
            "pii": f"Remove PII '{text[:8]}...' — use synthetic data instead",
            "nonsense": f"Replace '{text}' with meaningful content",
            "custom": f"Review '{text}' per custom rules",
        }
        return suggestions.get(category, f"Review '{text}'")

    def get_summary(self) -> Dict[str, int]:
        """Get summary counts by severity."""
        summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "total": 0}
        for v in self.violations:
            summary[v.severity] = summary.get(v.severity, 0) + 1
            summary["total"] += 1
        return summary

    def get_report(self) -> str:
        """Generate a text report of all violations."""
        if not self.violations:
            return "Content Scan: CLEAN — No violations found."

        lines = [
            f"Content Scan: {len(self.violations)} violation(s) found",
            "=" * 60,
        ]

        # Group by severity
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            sevs = [v for v in self.violations if v.severity == severity]
            if sevs:
                lines.append(f"\n{severity} ({len(sevs)}):")
                for v in sevs:
                    lines.append(f"  [{v.category}] '{v.text}' @ {v.location}")
                    if v.context:
                        lines.append(f"    Context: {v.context}")
                    if v.suggestion:
                        lines.append(f"    Fix: {v.suggestion}")

        return "\n".join(lines)

    def clear(self) -> None:
        """Clear all recorded violations."""
        self.violations.clear()
