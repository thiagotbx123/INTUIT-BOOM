# QBO Feature Checker Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an automated QA routine that navigates QBO features, captures annotated screenshots, interprets evidence via AI, and updates the Fall Release control spreadsheet.

**Architecture:** Declarative JSON config defines features/routes. Python engine uses Playwright (via existing login script) to navigate and capture. Pillow annotates screenshots. Claude API interprets and generates notes. openpyxl updates Excel.

**Tech Stack:** Python 3.x, Playwright, Pillow, openpyxl, Anthropic Claude API

---

## Project Structure

```
intuit-boom/
├── intuit_login_v2_4.py          # Existing login script (DO NOT MODIFY)
├── qbo_checker/
│   ├── __init__.py
│   ├── config.py                 # Configuration constants
│   ├── features.json             # Declarative feature definitions
│   ├── navigator.py              # QBO navigation engine
│   ├── screenshot.py             # Capture + annotation module
│   ├── interpreter.py            # AI interpretation for notes
│   ├── spreadsheet.py            # Excel update module
│   └── main.py                   # CLI orchestrator
├── Fall Release - TestBox...xlsx # Source tracker (read-only reference)
└── docs/plans/                   # This plan
```

**Output Location:** `G:\Meu Drive\TestBox\QBO-Evidence\`

---

## Task 1: Project Setup and Config

**Files:**
- Create: `qbo_checker/__init__.py`
- Create: `qbo_checker/config.py`

**Step 1: Create package directory**

```bash
mkdir -p C:/Users/adm_r/intuit-boom/qbo_checker
```

**Step 2: Create __init__.py**

```python
# qbo_checker/__init__.py
"""QBO Feature Checker - Automated Fall Release QA"""
__version__ = "1.0.0"
```

**Step 3: Create config.py**

```python
# qbo_checker/config.py
"""Configuration constants for QBO Feature Checker"""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
FEATURES_JSON = PROJECT_ROOT / "qbo_checker" / "features.json"
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
        "companies": ["Apex", "Global Tread", "RoadReady"],
        "sheet_name": "TCO"
    },
    "Construction": {
        "login_option": "1",
        "companies": ["Sales", "Events"],
        "sheet_name": "CONSTRUCTION_SALES"
    }
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
    "intuit_notes": 10
}

# Screenshot settings
SCREENSHOT_QUALITY = 95
HIGHLIGHT_COLOR = (255, 0, 0)  # Red
ARROW_COLOR = (255, 165, 0)    # Orange

# Ensure evidence directory exists
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
```

**Step 4: Verify config loads**

```bash
cd C:/Users/adm_r/intuit-boom && python -c "from qbo_checker.config import *; print('EVIDENCE_DIR:', EVIDENCE_DIR); print('Projects:', list(PROJECTS.keys()))"
```

Expected: Prints paths and project names without error.

**Step 5: Commit**

```bash
cd C:/Users/adm_r/intuit-boom
git init
git add qbo_checker/__init__.py qbo_checker/config.py
git commit -m "feat: add qbo_checker package with config

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 2: Features JSON Schema and Initial Data

**Files:**
- Create: `qbo_checker/features.json`

**Step 1: Create features.json with TCO Consolidated View as pilot**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "version": "1.0.0",
  "features": [
    {
      "id": "F001",
      "ref": "R2",
      "name": "Consolidated View",
      "description": "Fusion UI for multi-entity IES customers with consolidated view",
      "projects": ["TCO"],
      "companies": ["Apex"],
      "route": "/app/homepage",
      "click_path": [
        {"action": "wait", "selector": "[data-testid='left-nav']", "timeout": 5000},
        {"action": "click", "selector": "text=Multi-Entity"},
        {"action": "wait", "selector": ".consolidated-view", "timeout": 3000}
      ],
      "validation": {
        "must_exist": [".consolidated-view", "[data-testid='entity-selector']"],
        "must_contain_text": ["Consolidated"]
      },
      "highlight": {
        "selector": ".consolidated-view-header",
        "type": "box"
      },
      "interface": "Fusion"
    },
    {
      "id": "F002",
      "ref": "R3",
      "name": "Reporting Enhancements",
      "description": "Drill down from consolidated reports, Transaction Journal with Dimensions/Projects/Customers, IC column",
      "projects": ["TCO"],
      "companies": ["Apex"],
      "route": "/app/reportlist",
      "click_path": [
        {"action": "click", "selector": "text=Multi-Entity"},
        {"action": "click", "selector": "text=Reports"},
        {"action": "wait", "selector": ".report-list", "timeout": 5000}
      ],
      "validation": {
        "must_exist": [".report-list"],
        "must_contain_text": ["Consolidated", "P&L"]
      },
      "highlight": {
        "selector": ".report-header",
        "type": "box"
      },
      "interface": "Fusion"
    },
    {
      "id": "F003",
      "ref": "R4",
      "name": "Intercompany Expense Allocations",
      "description": "IC expense allocation mapping and summary views",
      "projects": ["TCO", "Construction"],
      "companies": ["Apex", "Sales"],
      "route": "/app/intercompany",
      "click_path": [
        {"action": "click", "selector": "text=Multi-Entity"},
        {"action": "click", "selector": "text=Intercompany"},
        {"action": "wait", "selector": ".ic-allocation-view", "timeout": 5000}
      ],
      "validation": {
        "must_exist": [".ic-allocation-view"],
        "must_contain_text": ["Allocation", "Intercompany"]
      },
      "highlight": {
        "selector": ".allocation-summary",
        "type": "arrow"
      },
      "interface": "Classic"
    }
  ]
}
```

**Step 2: Validate JSON syntax**

```bash
cd C:/Users/adm_r/intuit-boom && python -c "import json; f=open('qbo_checker/features.json'); data=json.load(f); print('Features loaded:', len(data['features'])); [print(f\"  - {feat['id']}: {feat['name']}\") for feat in data['features']]"
```

Expected: Lists 3 features without JSON errors.

**Step 3: Commit**

```bash
git add qbo_checker/features.json
git commit -m "feat: add features.json with initial TCO features

Includes Consolidated View, Reporting Enhancements, IC Allocations

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 3: Screenshot Capture with Annotations

**Files:**
- Create: `qbo_checker/screenshot.py`

**Step 1: Create screenshot.py**

```python
# qbo_checker/screenshot.py
"""Screenshot capture and annotation module"""

from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io

from .config import EVIDENCE_DIR, HIGHLIGHT_COLOR, ARROW_COLOR, SCREENSHOT_QUALITY


def generate_filename(project: str, company: str, feature_name: str) -> str:
    """Generate screenshot filename following naming convention.

    Format: {YYYY-MM-DD}_{PROJECT}_{COMPANY}_{FEATURE}.png
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    # Sanitize feature name (remove spaces, special chars)
    safe_feature = feature_name.replace(" ", "").replace("/", "_").replace(":", "")
    return f"{date_str}_{project}_{company}_{safe_feature}.png"


def capture_screenshot(page, filename: str) -> Path:
    """Capture screenshot from Playwright page and save to evidence folder.

    Args:
        page: Playwright page object
        filename: Target filename

    Returns:
        Path to saved screenshot
    """
    filepath = EVIDENCE_DIR / filename
    page.screenshot(path=str(filepath), full_page=False)
    return filepath


def add_box_highlight(image: Image.Image, bbox: tuple, color: tuple = HIGHLIGHT_COLOR, width: int = 3) -> Image.Image:
    """Add rectangular highlight box around an area.

    Args:
        image: PIL Image
        bbox: (x1, y1, x2, y2) bounding box
        color: RGB tuple for box color
        width: Line width

    Returns:
        Modified image
    """
    draw = ImageDraw.Draw(image)
    draw.rectangle(bbox, outline=color, width=width)
    return image


def add_arrow(image: Image.Image, start: tuple, end: tuple, color: tuple = ARROW_COLOR, width: int = 3) -> Image.Image:
    """Add arrow pointing to element.

    Args:
        image: PIL Image
        start: (x, y) arrow start point
        end: (x, y) arrow end point (tip)
        color: RGB tuple
        width: Line width

    Returns:
        Modified image
    """
    draw = ImageDraw.Draw(image)
    # Main line
    draw.line([start, end], fill=color, width=width)

    # Arrowhead (simple triangle)
    import math
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_length = 15
    arrow_angle = math.pi / 6  # 30 degrees

    x1 = end[0] - arrow_length * math.cos(angle - arrow_angle)
    y1 = end[1] - arrow_length * math.sin(angle - arrow_angle)
    x2 = end[0] - arrow_length * math.cos(angle + arrow_angle)
    y2 = end[1] - arrow_length * math.sin(angle + arrow_angle)

    draw.polygon([end, (x1, y1), (x2, y2)], fill=color)
    return image


def add_label(image: Image.Image, position: tuple, text: str, color: tuple = HIGHLIGHT_COLOR) -> Image.Image:
    """Add text label to image.

    Args:
        image: PIL Image
        position: (x, y) position for text
        text: Label text
        color: RGB tuple

    Returns:
        Modified image
    """
    draw = ImageDraw.Draw(image)
    # Use default font (cross-platform)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()

    # Add background for readability
    bbox = draw.textbbox(position, text, font=font)
    padding = 4
    draw.rectangle(
        [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding],
        fill=(255, 255, 255, 200)
    )
    draw.text(position, text, fill=color, font=font)
    return image


def annotate_screenshot(filepath: Path, element_bbox: tuple, highlight_type: str = "box", label: str = None) -> Path:
    """Add annotations to existing screenshot.

    Args:
        filepath: Path to screenshot
        element_bbox: (x1, y1, x2, y2) of element to highlight
        highlight_type: "box" or "arrow"
        label: Optional text label

    Returns:
        Path to annotated screenshot (overwrites original)
    """
    image = Image.open(filepath)

    if highlight_type == "box":
        image = add_box_highlight(image, element_bbox)
    elif highlight_type == "arrow":
        # Arrow from top-left corner pointing to element center
        center_x = (element_bbox[0] + element_bbox[2]) // 2
        center_y = (element_bbox[1] + element_bbox[3]) // 2
        start = (50, 50)  # Top-left area
        image = add_arrow(image, start, (center_x, center_y))

    if label:
        # Position label above the element
        label_pos = (element_bbox[0], max(0, element_bbox[1] - 25))
        image = add_label(image, label_pos, label)

    image.save(filepath, quality=SCREENSHOT_QUALITY)
    return filepath


def get_element_bbox(page, selector: str) -> tuple:
    """Get bounding box of element from Playwright page.

    Args:
        page: Playwright page
        selector: CSS selector

    Returns:
        (x1, y1, x2, y2) tuple or None if not found
    """
    try:
        element = page.locator(selector).first
        if element.is_visible():
            box = element.bounding_box()
            if box:
                return (
                    int(box['x']),
                    int(box['y']),
                    int(box['x'] + box['width']),
                    int(box['y'] + box['height'])
                )
    except:
        pass
    return None
```

**Step 2: Test screenshot module (unit test)**

```bash
cd C:/Users/adm_r/intuit-boom && python -c "
from qbo_checker.screenshot import generate_filename, add_box_highlight, add_arrow
from PIL import Image

# Test filename generation
fname = generate_filename('TCO', 'Apex', 'Consolidated View')
print('Filename:', fname)
assert 'TCO_Apex_ConsolidatedView' in fname
assert fname.endswith('.png')

# Test annotation on dummy image
img = Image.new('RGB', (800, 600), color='white')
img = add_box_highlight(img, (100, 100, 300, 200))
img = add_arrow(img, (50, 50), (200, 150))
img.save('test_annotation.png')
print('Test annotation saved to test_annotation.png')
print('All tests passed!')
"
```

Expected: Filename printed, test_annotation.png created.

**Step 3: Cleanup test file**

```bash
rm -f C:/Users/adm_r/intuit-boom/test_annotation.png
```

**Step 4: Commit**

```bash
git add qbo_checker/screenshot.py
git commit -m "feat: add screenshot capture and annotation module

Supports box highlights, arrows, and text labels

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 4: AI Interpreter for Notes Generation

**Files:**
- Create: `qbo_checker/interpreter.py`

**Step 1: Create interpreter.py**

```python
# qbo_checker/interpreter.py
"""AI interpretation module for screenshot analysis and notes generation"""

import base64
import os
from pathlib import Path
from anthropic import Anthropic

# Initialize client (uses ANTHROPIC_API_KEY env var)
client = Anthropic()

SYSTEM_PROMPT = """You are a QuickBooks Fall Release QA assistant.

Your job is to analyze screenshots and generate validation notes.

For each screenshot you will:
1. Determine if the feature is working (status)
2. Write a professional note for Intuit
3. Write a technical note for internal TestBox use

STATUS RULES:
- YES: Feature works and evidence is clear
- PARTIAL: Works with limitations (e.g., Classic only, not Fusion)
- NO: Feature not found or broken
- NA: Not applicable to this environment

INTUIT NOTES STYLE:
- Audience: Intuit and customers
- Tone: Simple, neutral, professional
- Never mention: internal tools, AI, automation
- Focus: what works, limitations, next steps

INTERNAL NOTES STYLE:
- Audience: TestBox team only
- Tone: Direct and technical
- Can mention: shortcuts, risks, scripts, technical details

Keep notes concise (1-3 sentences each)."""


def encode_image(filepath: Path) -> str:
    """Encode image to base64 for API."""
    with open(filepath, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def interpret_screenshot(
    filepath: Path,
    feature_name: str,
    feature_description: str,
    project: str,
    company: str
) -> dict:
    """Analyze screenshot and generate status + notes.

    Args:
        filepath: Path to screenshot
        feature_name: Name of the feature being validated
        feature_description: Description from Fall Release tracker
        project: Project name (TCO, Construction, etc.)
        company: Company name (Apex, Sales, etc.)

    Returns:
        dict with keys: status, intuit_notes, internal_notes
    """
    image_data = encode_image(filepath)

    user_prompt = f"""Analyze this QuickBooks screenshot for the following feature:

Feature: {feature_name}
Description: {feature_description}
Project: {project}
Company: {company}

Based on what you see in the screenshot:

1. What is the STATUS? (YES / PARTIAL / NO / NA)
2. Write INTUIT_NOTES (1-3 sentences, professional tone for Intuit)
3. Write INTERNAL_NOTES (1-3 sentences, technical tone for TestBox)

Respond in this exact format:
STATUS: [status]
INTUIT_NOTES: [notes]
INTERNAL_NOTES: [notes]"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            }
        ],
        system=SYSTEM_PROMPT
    )

    # Parse response
    result_text = response.content[0].text
    result = {
        "status": "NO",
        "intuit_notes": "",
        "internal_notes": ""
    }

    for line in result_text.strip().split("\n"):
        if line.startswith("STATUS:"):
            result["status"] = line.replace("STATUS:", "").strip().upper()
        elif line.startswith("INTUIT_NOTES:"):
            result["intuit_notes"] = line.replace("INTUIT_NOTES:", "").strip()
        elif line.startswith("INTERNAL_NOTES:"):
            result["internal_notes"] = line.replace("INTERNAL_NOTES:", "").strip()

    return result


def generate_worklog_note(feature_name: str, status: str, action: str = "validated") -> str:
    """Generate a short worklog note.

    Args:
        feature_name: Feature name
        status: Status result
        action: What was done

    Returns:
        Short worklog sentence
    """
    return f"{action.capitalize()} {feature_name}, marked as {status}."
```

**Step 2: Test interpreter (requires ANTHROPIC_API_KEY)**

```bash
cd C:/Users/adm_r/intuit-boom && python -c "
from qbo_checker.interpreter import generate_worklog_note

# Test worklog generation (doesn't need API)
note = generate_worklog_note('Consolidated View', 'YES', 'validated')
print('Worklog:', note)
assert 'Consolidated View' in note
assert 'YES' in note
print('Worklog test passed!')

# API test only if key exists
import os
if os.environ.get('ANTHROPIC_API_KEY'):
    print('API key found, but skipping live test')
else:
    print('No API key - interpreter will need it at runtime')
"
```

Expected: Worklog test passes, API key status printed.

**Step 3: Commit**

```bash
git add qbo_checker/interpreter.py
git commit -m "feat: add AI interpreter for screenshot analysis

Uses Claude API for status determination and notes generation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 5: Excel Spreadsheet Module

**Files:**
- Create: `qbo_checker/spreadsheet.py`

**Step 1: Create spreadsheet.py**

```python
# qbo_checker/spreadsheet.py
"""Excel spreadsheet module for Fall Release control sheet"""

from datetime import datetime
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

from .config import CONTROL_SHEET, EVIDENCE_DIR


# Column definitions for control sheet
CONTROL_COLUMNS = [
    "Projeto",
    "Company",
    "Ref",
    "Feature",
    "Status",
    "Intuit_notes",
    "Internal_TBX_notes",
    "Evidence_file",
    "Link"
]

# Status colors
STATUS_COLORS = {
    "YES": "90EE90",      # Light green
    "PARTIAL": "FFD700",  # Gold
    "NO": "FF6B6B",       # Light red
    "NA": "D3D3D3"        # Light gray
}


def create_control_sheet() -> Path:
    """Create new control spreadsheet with headers.

    Returns:
        Path to created spreadsheet
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Feature Checks"

    # Write headers
    header_font = Font(bold=True)
    for col, header in enumerate(CONTROL_COLUMNS, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    # Set column widths
    widths = [12, 15, 8, 25, 10, 40, 40, 35, 8]
    for col, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(col)].width = width

    wb.save(CONTROL_SHEET)
    return CONTROL_SHEET


def load_or_create_control_sheet() -> openpyxl.Workbook:
    """Load existing control sheet or create new one.

    Returns:
        openpyxl Workbook
    """
    if CONTROL_SHEET.exists():
        return openpyxl.load_workbook(CONTROL_SHEET)
    else:
        create_control_sheet()
        return openpyxl.load_workbook(CONTROL_SHEET)


def add_feature_result(
    project: str,
    company: str,
    ref: str,
    feature: str,
    status: str,
    intuit_notes: str,
    internal_notes: str,
    evidence_file: str
) -> int:
    """Add a feature check result to the control sheet.

    Args:
        project: Project name (TCO, Construction)
        company: Company name (Apex, Sales, etc.)
        ref: Reference ID from tracker
        feature: Feature name
        status: YES/PARTIAL/NO/NA
        intuit_notes: Notes for Intuit
        internal_notes: Internal TestBox notes
        evidence_file: Screenshot filename

    Returns:
        Row number where result was added
    """
    wb = load_or_create_control_sheet()
    ws = wb.active

    # Find next empty row
    next_row = ws.max_row + 1

    # Build link chip
    evidence_path = EVIDENCE_DIR / evidence_file
    # For local Drive sync, use file path as link
    link_chip = f'=HYPERLINK("{evidence_path}", "📎")'

    # Write data
    data = [
        project,
        company,
        ref,
        feature,
        status,
        intuit_notes,
        internal_notes,
        evidence_file,
        None  # Link column - will add formula
    ]

    for col, value in enumerate(data, 1):
        cell = ws.cell(row=next_row, column=col, value=value)

        # Style status cell with color
        if col == 5 and status in STATUS_COLORS:
            cell.fill = PatternFill(start_color=STATUS_COLORS[status],
                                   end_color=STATUS_COLORS[status],
                                   fill_type="solid")
            cell.alignment = Alignment(horizontal='center')

    # Add hyperlink formula for link column
    link_cell = ws.cell(row=next_row, column=9)
    link_cell.value = link_chip
    link_cell.alignment = Alignment(horizontal='center')

    wb.save(CONTROL_SHEET)
    return next_row


def find_existing_result(project: str, company: str, feature: str) -> int:
    """Find existing row for a feature result.

    Args:
        project: Project name
        company: Company name
        feature: Feature name

    Returns:
        Row number if found, None otherwise
    """
    wb = load_or_create_control_sheet()
    ws = wb.active

    for row in range(2, ws.max_row + 1):
        if (ws.cell(row=row, column=1).value == project and
            ws.cell(row=row, column=2).value == company and
            ws.cell(row=row, column=4).value == feature):
            return row

    return None


def update_feature_result(
    row: int,
    status: str = None,
    intuit_notes: str = None,
    internal_notes: str = None,
    evidence_file: str = None
):
    """Update existing feature result row.

    Args:
        row: Row number to update
        status: New status (optional)
        intuit_notes: New Intuit notes (optional)
        internal_notes: New internal notes (optional)
        evidence_file: New evidence file (optional)
    """
    wb = load_or_create_control_sheet()
    ws = wb.active

    if status:
        cell = ws.cell(row=row, column=5, value=status)
        if status in STATUS_COLORS:
            cell.fill = PatternFill(start_color=STATUS_COLORS[status],
                                   end_color=STATUS_COLORS[status],
                                   fill_type="solid")

    if intuit_notes:
        ws.cell(row=row, column=6, value=intuit_notes)

    if internal_notes:
        ws.cell(row=row, column=7, value=internal_notes)

    if evidence_file:
        ws.cell(row=row, column=8, value=evidence_file)
        # Update link
        evidence_path = EVIDENCE_DIR / evidence_file
        link_chip = f'=HYPERLINK("{evidence_path}", "📎")'
        ws.cell(row=row, column=9, value=link_chip)

    wb.save(CONTROL_SHEET)


def get_summary() -> dict:
    """Get summary statistics from control sheet.

    Returns:
        dict with counts by status
    """
    wb = load_or_create_control_sheet()
    ws = wb.active

    summary = {"YES": 0, "PARTIAL": 0, "NO": 0, "NA": 0, "total": 0}

    for row in range(2, ws.max_row + 1):
        status = ws.cell(row=row, column=5).value
        if status in summary:
            summary[status] += 1
            summary["total"] += 1

    return summary
```

**Step 2: Test spreadsheet module**

```bash
cd C:/Users/adm_r/intuit-boom && python -c "
from qbo_checker.spreadsheet import create_control_sheet, add_feature_result, get_summary
from qbo_checker.config import CONTROL_SHEET

# Create fresh control sheet
path = create_control_sheet()
print('Created:', path)

# Add test result
row = add_feature_result(
    project='TCO',
    company='Apex',
    ref='R2',
    feature='Consolidated View',
    status='YES',
    intuit_notes='Feature available in Classic view.',
    internal_notes='Automated check passed.',
    evidence_file='2024-12-02_TCO_Apex_ConsolidatedView.png'
)
print('Added row:', row)

# Get summary
summary = get_summary()
print('Summary:', summary)

print('All spreadsheet tests passed!')
"
```

Expected: Creates control sheet, adds row, shows summary.

**Step 3: Commit**

```bash
git add qbo_checker/spreadsheet.py
git commit -m "feat: add Excel spreadsheet module for control sheet

Supports create, add, update, and summary functions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 6: Navigator Module

**Files:**
- Create: `qbo_checker/navigator.py`

**Step 1: Create navigator.py**

```python
# qbo_checker/navigator.py
"""QBO navigation engine using Playwright"""

import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser

from .config import CHROME_DEBUG_PORT, CHROME_DEBUG_URL, FEATURES_JSON


def load_features() -> list:
    """Load features from JSON config.

    Returns:
        List of feature definitions
    """
    with open(FEATURES_JSON) as f:
        data = json.load(f)
    return data["features"]


def get_features_for_project(project: str) -> list:
    """Get features filtered by project.

    Args:
        project: Project name (TCO, Construction)

    Returns:
        List of features for that project
    """
    features = load_features()
    return [f for f in features if project in f["projects"]]


def connect_to_chrome() -> tuple:
    """Connect to existing Chrome debug session.

    Returns:
        Tuple of (playwright, browser, page)

    Raises:
        ConnectionError if Chrome not available
    """
    pw = sync_playwright().start()

    try:
        browser = pw.chromium.connect_over_cdp(CHROME_DEBUG_URL)
    except Exception as e:
        pw.stop()
        raise ConnectionError(
            f"Could not connect to Chrome on port {CHROME_DEBUG_PORT}. "
            "Please run intuit_login_v2_4.py first to start Chrome."
        ) from e

    # Get existing context and page
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


def execute_click_path(page: Page, click_path: list) -> bool:
    """Execute a series of navigation actions.

    Args:
        page: Playwright page
        click_path: List of action dictionaries

    Returns:
        True if all actions succeeded, False otherwise
    """
    for action in click_path:
        action_type = action.get("action")
        selector = action.get("selector")
        timeout = action.get("timeout", 5000)

        try:
            if action_type == "wait":
                page.wait_for_selector(selector, timeout=timeout)
            elif action_type == "click":
                page.locator(selector).first.click()
                time.sleep(0.5)  # Brief pause after click
            elif action_type == "fill":
                value = action.get("value", "")
                page.locator(selector).first.fill(value)
        except Exception as e:
            print(f"  [WARN] Action failed: {action_type} on {selector} - {e}")
            return False

    return True


def validate_feature(page: Page, validation: dict) -> tuple:
    """Validate that feature elements exist on page.

    Args:
        page: Playwright page
        validation: Dict with must_exist and must_contain_text lists

    Returns:
        Tuple of (success: bool, details: str)
    """
    must_exist = validation.get("must_exist", [])
    must_contain = validation.get("must_contain_text", [])

    missing_elements = []
    missing_text = []

    # Check required elements
    for selector in must_exist:
        try:
            if not page.locator(selector).first.is_visible(timeout=2000):
                missing_elements.append(selector)
        except:
            missing_elements.append(selector)

    # Check required text
    page_text = page.content()
    for text in must_contain:
        if text.lower() not in page_text.lower():
            missing_text.append(text)

    if missing_elements or missing_text:
        details = []
        if missing_elements:
            details.append(f"Missing elements: {missing_elements}")
        if missing_text:
            details.append(f"Missing text: {missing_text}")
        return False, "; ".join(details)

    return True, "All validations passed"


def navigate_to_feature(page: Page, feature: dict) -> tuple:
    """Navigate to a feature and validate it.

    Args:
        page: Playwright page
        feature: Feature definition dict

    Returns:
        Tuple of (success: bool, details: str)
    """
    feature_name = feature["name"]
    route = feature.get("route", "")
    click_path = feature.get("click_path", [])
    validation = feature.get("validation", {})

    print(f"  Navigating to {feature_name}...")

    # Navigate to route if specified
    if route and not route.startswith("/app/homepage"):
        current_url = page.url
        if route not in current_url:
            # Try to navigate via URL
            base_url = current_url.split("/app/")[0] if "/app/" in current_url else current_url
            target_url = base_url + route
            try:
                page.goto(target_url, wait_until="networkidle", timeout=10000)
            except:
                pass  # Will try click path instead

    # Execute click path
    if click_path:
        if not execute_click_path(page, click_path):
            return False, "Click path failed"

    # Wait for page to settle
    time.sleep(1)

    # Validate
    if validation:
        return validate_feature(page, validation)

    return True, "Navigation complete (no validation defined)"
```

**Step 2: Test navigator (basic - no Chrome required)**

```bash
cd C:/Users/adm_r/intuit-boom && python -c "
from qbo_checker.navigator import load_features, get_features_for_project

# Test feature loading
features = load_features()
print('Total features:', len(features))

# Test filtering
tco_features = get_features_for_project('TCO')
print('TCO features:', len(tco_features))
for f in tco_features:
    print(f'  - {f[\"name\"]}')

print('Navigator tests passed!')
"
```

Expected: Lists features correctly.

**Step 3: Commit**

```bash
git add qbo_checker/navigator.py
git commit -m "feat: add QBO navigation engine

Connects to Chrome debug, executes click paths, validates features

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 7: Main Orchestrator CLI

**Files:**
- Create: `qbo_checker/main.py`

**Step 1: Create main.py**

```python
# qbo_checker/main.py
"""Main CLI orchestrator for QBO Feature Checker"""

import sys
import time
from datetime import datetime

from .config import PROJECTS, EVIDENCE_DIR
from .navigator import connect_to_chrome, get_features_for_project, navigate_to_feature
from .screenshot import generate_filename, capture_screenshot, annotate_screenshot, get_element_bbox
from .interpreter import interpret_screenshot, generate_worklog_note
from .spreadsheet import add_feature_result, find_existing_result, update_feature_result, get_summary


def show_banner():
    """Display CLI banner."""
    print()
    print("\033[96m" + "=" * 60 + "\033[0m")
    print("\033[96m       QBO FEATURE CHECKER - INTUIT BOOM\033[0m")
    print("\033[96m" + "=" * 60 + "\033[0m")
    print()


def show_menu():
    """Display project selection menu."""
    print("\033[97mSelect Project:\033[0m")
    print("-" * 30)
    for i, (project, config) in enumerate(PROJECTS.items(), 1):
        companies = ", ".join(config["companies"])
        print(f"  [{i}] {project} ({companies})")
    print("-" * 30)
    print("  [Q] Quit")
    print()


def select_project() -> str:
    """Get project selection from user.

    Returns:
        Project name or None if quit
    """
    show_menu()
    choice = input("  > ").strip().upper()

    if choice == "Q":
        return None

    try:
        idx = int(choice) - 1
        project_names = list(PROJECTS.keys())
        if 0 <= idx < len(project_names):
            return project_names[idx]
    except ValueError:
        pass

    print("\033[91m  Invalid selection\033[0m")
    return select_project()


def check_feature(page, feature: dict, project: str) -> dict:
    """Check a single feature: navigate, screenshot, interpret, save.

    Args:
        page: Playwright page
        feature: Feature definition
        project: Project name

    Returns:
        Result dict with status and details
    """
    feature_name = feature["name"]
    companies = feature.get("companies", ["Default"])
    highlight_config = feature.get("highlight", {})

    results = []

    for company in companies:
        if company not in PROJECTS[project]["companies"]:
            continue

        print(f"\n  [{project}/{company}] Checking: {feature_name}")

        # Navigate
        success, nav_details = navigate_to_feature(page, feature)

        if not success:
            print(f"    \033[91m[FAIL] {nav_details}\033[0m")
            # Still take screenshot for evidence

        # Generate filename
        filename = generate_filename(project, company, feature_name)

        # Capture screenshot
        print(f"    Capturing screenshot...")
        filepath = capture_screenshot(page, filename)

        # Annotate if highlight config exists
        if highlight_config:
            selector = highlight_config.get("selector")
            highlight_type = highlight_config.get("type", "box")

            bbox = get_element_bbox(page, selector)
            if bbox:
                print(f"    Adding {highlight_type} annotation...")
                annotate_screenshot(filepath, bbox, highlight_type, feature_name)
            else:
                print(f"    \033[93m[WARN] Could not find element for highlight\033[0m")

        # Interpret with AI
        print(f"    Interpreting screenshot...")
        try:
            interpretation = interpret_screenshot(
                filepath=filepath,
                feature_name=feature_name,
                feature_description=feature.get("description", ""),
                project=project,
                company=company
            )
        except Exception as e:
            print(f"    \033[93m[WARN] AI interpretation failed: {e}\033[0m")
            interpretation = {
                "status": "PARTIAL" if success else "NO",
                "intuit_notes": f"Feature {'accessible' if success else 'not accessible'} - manual review needed.",
                "internal_notes": f"Auto-check {'passed' if success else 'failed'}: {nav_details}"
            }

        status = interpretation["status"]
        status_color = {
            "YES": "\033[92m",
            "PARTIAL": "\033[93m",
            "NO": "\033[91m",
            "NA": "\033[90m"
        }.get(status, "")

        print(f"    Status: {status_color}{status}\033[0m")

        # Save to spreadsheet
        existing_row = find_existing_result(project, company, feature_name)

        if existing_row:
            update_feature_result(
                row=existing_row,
                status=status,
                intuit_notes=interpretation["intuit_notes"],
                internal_notes=interpretation["internal_notes"],
                evidence_file=filename
            )
            print(f"    Updated row {existing_row} in control sheet")
        else:
            row = add_feature_result(
                project=project,
                company=company,
                ref=feature.get("ref", ""),
                feature=feature_name,
                status=status,
                intuit_notes=interpretation["intuit_notes"],
                internal_notes=interpretation["internal_notes"],
                evidence_file=filename
            )
            print(f"    Added row {row} to control sheet")

        results.append({
            "company": company,
            "status": status,
            "file": filename
        })

    return results


def run_project_check(project: str):
    """Run all feature checks for a project.

    Args:
        project: Project name
    """
    print(f"\n\033[97mStarting checks for: {project}\033[0m")
    print(f"Evidence folder: {EVIDENCE_DIR}")
    print("-" * 50)

    # Get features for project
    features = get_features_for_project(project)
    print(f"Found {len(features)} features to check")

    if not features:
        print("\033[93mNo features defined for this project\033[0m")
        return

    # Connect to Chrome
    print("\nConnecting to Chrome...")
    try:
        pw, browser, page = connect_to_chrome()
    except ConnectionError as e:
        print(f"\033[91m{e}\033[0m")
        print("\nPlease run: python intuit_login_v2_4.py")
        print(f"Select option {PROJECTS[project]['login_option']} for {project}")
        return

    print("\033[92mConnected!\033[0m")

    # Process each feature
    all_results = []
    try:
        for i, feature in enumerate(features, 1):
            print(f"\n[{i}/{len(features)}] {feature['name']}")
            results = check_feature(page, feature, project)
            all_results.extend(results)

            # Brief pause between features
            time.sleep(1)
    finally:
        # Disconnect (don't close browser)
        pw.stop()

    # Summary
    print("\n" + "=" * 50)
    print("\033[97mSUMMARY\033[0m")
    print("=" * 50)

    summary = get_summary()
    print(f"  Total checked: {summary['total']}")
    print(f"  \033[92mYES: {summary['YES']}\033[0m")
    print(f"  \033[93mPARTIAL: {summary['PARTIAL']}\033[0m")
    print(f"  \033[91mNO: {summary['NO']}\033[0m")
    print(f"  \033[90mNA: {summary['NA']}\033[0m")
    print()
    print(f"Control sheet: {EVIDENCE_DIR / 'fall_release_control.xlsx'}")
    print()


def main():
    """Main entry point."""
    show_banner()

    while True:
        project = select_project()

        if project is None:
            print("\n\033[90mGoodbye!\033[0m\n")
            break

        run_project_check(project)

        print("\n" + "-" * 50)
        input("Press ENTER to continue...")
        show_banner()


if __name__ == "__main__":
    main()
```

**Step 2: Test main module imports**

```bash
cd C:/Users/adm_r/intuit-boom && python -c "
from qbo_checker.main import show_banner, show_menu
show_banner()
print('Main module imports OK!')
"
```

Expected: Banner displays, no import errors.

**Step 3: Commit**

```bash
git add qbo_checker/main.py
git commit -m "feat: add main CLI orchestrator

Company-by-company execution with progress and summary

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 8: Final Integration and Documentation

**Files:**
- Create: `qbo_checker/requirements.txt`
- Create: `qbo_checker/README.md`

**Step 1: Create requirements.txt**

```text
playwright>=1.40.0
Pillow>=10.0.0
openpyxl>=3.1.0
anthropic>=0.18.0
```

**Step 2: Create README.md**

```markdown
# QBO Feature Checker

Automated QA routine for validating QuickBooks Fall Release features.

## Setup

1. Install dependencies:
   ```bash
   pip install -r qbo_checker/requirements.txt
   playwright install chromium
   ```

2. Set Anthropic API key:
   ```bash
   set ANTHROPIC_API_KEY=your_key_here
   ```

3. Ensure Google Drive sync folder exists:
   ```
   G:\Meu Drive\TestBox\QBO-Evidence\
   ```

## Usage

1. First, login to QBO using the login script:
   ```bash
   python intuit_login_v2_4.py
   ```
   Select the account for the project you want to check.

2. Run the feature checker:
   ```bash
   python -m qbo_checker.main
   ```

3. Select a project (TCO, Construction) and wait for checks to complete.

4. Results are saved to:
   - Screenshots: `G:\Meu Drive\TestBox\QBO-Evidence\{date}_{project}_{company}_{feature}.png`
   - Control sheet: `G:\Meu Drive\TestBox\QBO-Evidence\fall_release_control.xlsx`

## Adding Features

Edit `qbo_checker/features.json` to add new features:

```json
{
  "id": "F004",
  "name": "New Feature",
  "projects": ["TCO"],
  "companies": ["Apex"],
  "route": "/app/feature-route",
  "click_path": [
    {"action": "click", "selector": "text=Menu Item"}
  ],
  "validation": {
    "must_exist": [".feature-element"]
  }
}
```
```

**Step 3: Install dependencies**

```bash
cd C:/Users/adm_r/intuit-boom && pip install playwright Pillow openpyxl anthropic --quiet && playwright install chromium
```

**Step 4: Final commit**

```bash
git add qbo_checker/requirements.txt qbo_checker/README.md
git commit -m "docs: add requirements and README

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Summary

**Total Tasks:** 8
**Files Created:** 9
- `qbo_checker/__init__.py`
- `qbo_checker/config.py`
- `qbo_checker/features.json`
- `qbo_checker/screenshot.py`
- `qbo_checker/interpreter.py`
- `qbo_checker/spreadsheet.py`
- `qbo_checker/navigator.py`
- `qbo_checker/main.py`
- `qbo_checker/requirements.txt`
- `qbo_checker/README.md`

**Execution:**
```bash
# 1. Login first
python intuit_login_v2_4.py  # Select account 2 for TCO

# 2. Run checker
python -m qbo_checker.main
```
