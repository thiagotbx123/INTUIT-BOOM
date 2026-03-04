# qbo_checker/config.py
"""Configuration constants for QBO Feature Checker"""

from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
FEATURES_JSON = PROJECT_ROOT / "qbo_checker" / "features_v4.json"
EVIDENCE_DIR = Path("G:/Meu Drive/TestBox/QBO-Evidence")
CONTROL_SHEET = EVIDENCE_DIR / "fall_release_control.xlsx"
SOURCE_TRACKER = PROJECT_ROOT / "Fall Release - TestBox (Feature Flag & UAT Tracker) (6).xlsx"

# Chrome Debug
CHROME_DEBUG_PORT = 9222
CHROME_DEBUG_URL = f"http://127.0.0.1:{CHROME_DEBUG_PORT}"

# Projects and Companies mapping
PROJECTS = {
    "TCO": {
        "login_option": "2",
        "companies": ["Traction", "Apex", "Global Tread", "RoadReady"],
        "sheet_name": "TCO",
    },
    "Construction": {
        "login_option": "1",
        "companies": ["Sales", "Events"],
        "sheet_name": "CONSTRUCTION_SALES",
    },
}

# Spreadsheet columns (1-indexed for openpyxl)
COLUMNS = {
    "priority": 1,
    "feature": 2,
    "data_prep": 3,
    "requirements": 4,
    "click_path": 5,
    "need_data": 6,
    "already_has": 7,
    "notes": 8,
    "evidence": 9,
    "intuit_notes": 10,
}

# Screenshot settings
SCREENSHOT_QUALITY = 95
HIGHLIGHT_COLOR = (255, 0, 0)  # Red
ARROW_COLOR = (255, 0, 0)  # Red (same as highlight)

# Ensure evidence directory exists
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
