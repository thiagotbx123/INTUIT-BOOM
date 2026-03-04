"""
Feature Checker - Automated health checks for demo environments.

A framework for validating that demo environments are always ready:
- Logs into applications
- Navigates to features
- Validates they work
- Captures evidence
- Alerts on failures
"""

__version__ = "1.0.0"
__author__ = "TestBox TSA Team"

from .core.browser import BrowserManager
from .core.checker import FeatureChecker
from .core.reporter import Reporter

__all__ = ["FeatureChecker", "BrowserManager", "Reporter"]
