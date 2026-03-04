"""Configuration management for Feature Checker."""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class CheckConfig:
    """Configuration for a single health check."""

    id: str
    name: str
    type: str  # auth, navigation, api, data, ui
    priority: str = "medium"  # critical, high, medium, low
    route: Optional[str] = None
    expect: Dict[str, Any] = field(default_factory=dict)
    highlight: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 30000
    retry: int = 1

    @classmethod
    def from_dict(cls, data: dict) -> "CheckConfig":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class ProductConfig:
    """Configuration for a product (e.g., QBO, People.ai)."""

    name: str
    base_url: str
    auth: Dict[str, Any] = field(default_factory=dict)
    projects: Dict[str, Any] = field(default_factory=dict)
    checks: List[CheckConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "ProductConfig":
        checks = [CheckConfig.from_dict(c) for c in data.get("checks", [])]
        return cls(
            name=data["name"],
            base_url=data["base_url"],
            auth=data.get("auth", {}),
            projects=data.get("projects", {}),
            checks=checks,
        )


@dataclass
class Config:
    """Main configuration container."""

    # Paths
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent.parent)
    config_dir: Path = field(
        default_factory=lambda: Path(__file__).parent.parent.parent.parent / "config"
    )
    evidence_dir: Path = field(
        default_factory=lambda: Path(os.getenv("EVIDENCE_DIR", "./output/evidence"))
    )
    reports_dir: Path = field(
        default_factory=lambda: Path(os.getenv("REPORTS_DIR", "./output/reports"))
    )

    # Browser
    chrome_path: str = field(
        default_factory=lambda: os.getenv(
            "CHROME_PATH", r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
    )
    chrome_debug_port: int = field(
        default_factory=lambda: int(os.getenv("CHROME_DEBUG_PORT", "9222"))
    )

    # Screenshot
    screenshot_quality: int = field(
        default_factory=lambda: int(os.getenv("SCREENSHOT_QUALITY", "95"))
    )

    # Alerting
    slack_webhook_url: Optional[str] = field(default_factory=lambda: os.getenv("SLACK_WEBHOOK_URL"))
    slack_channel: Optional[str] = field(default_factory=lambda: os.getenv("SLACK_CHANNEL"))
    alert_email: Optional[str] = field(default_factory=lambda: os.getenv("ALERT_EMAIL"))

    # Loaded products
    products: Dict[str, ProductConfig] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize paths and load configurations."""
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def load_product(self, product_name: str) -> ProductConfig:
        """Load product configuration from file."""
        if product_name in self.products:
            return self.products[product_name]

        # Try to load from config file
        product_file = self.config_dir / "products" / f"{product_name.lower()}.json"
        checks_file = self.config_dir / "checks" / f"{product_name.lower()}.json"

        if not product_file.exists():
            raise FileNotFoundError(f"Product config not found: {product_file}")

        with open(product_file) as f:
            product_data = json.load(f)

        # Load checks if separate file exists
        if checks_file.exists():
            with open(checks_file) as f:
                checks_data = json.load(f)
                product_data["checks"] = checks_data.get("checks", [])

        product = ProductConfig.from_dict(product_data)
        self.products[product_name] = product
        return product

    def get_credentials(self, product_name: str) -> Dict[str, str]:
        """Get credentials for a product from environment."""
        prefix = product_name.upper()
        return {
            "email": os.getenv(f"{prefix}_EMAIL", ""),
            "password": os.getenv(f"{prefix}_PASSWORD", ""),
            "totp_secret": os.getenv(f"{prefix}_TOTP_SECRET", ""),
        }


# Global config instance
_config: Optional[Config] = None


def load_config() -> Config:
    """Load or return cached configuration."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def get_config() -> Config:
    """Get current configuration (alias for load_config)."""
    return load_config()
