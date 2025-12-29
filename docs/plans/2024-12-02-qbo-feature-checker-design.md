# QBO Feature Checker - Design Document

## Overview

Automated QA routine for validating Fall Release features in QuickBooks Online environments. Navigates to features, captures annotated screenshots, interprets evidence via AI, and updates control spreadsheet.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              QBO FEATURE CHECKER - INTUIT BOOM                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CONFIG LAYER (Declarative)                                     │
│  ├─ features.json    → routes, selectors, validations           │
│  └─ fall_release.xlsx → source of truth for features            │
│                                                                 │
│  ENGINE LAYER (Python + Playwright)                             │
│  ├─ Uses intuit_login_v2_4.py (no reimplementation)             │
│  ├─ Reuses existing Chrome session when possible                │
│  ├─ Navigates using paths from features.json                    │
│  ├─ Validates expected elements (selectors)                     │
│  ├─ Captures screenshot with highlights/arrows                  │
│  └─ Interprets screenshot via AI for notes generation           │
│                                                                 │
│  OUTPUT LAYER                                                   │
│  ├─ Screenshots → G:\Meu Drive\TestBox\QBO-Evidence\            │
│  └─ Spreadsheet → fall_release_control.xlsx                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Execution Flow

### Phase 0 - Setup
- Read Fall Release tracker (Excel model)
- Load features.json (declarative mapper)
- Check existing evidence in Drive folder

### Phase 1 - Login
- Use intuit_login_v2_4.py (accounts: 1=Construction, 2=TCO, 3=Product, 4=TCO Demo)
- Reuse existing Chrome session if available
- Only request new login when session is lost

### Phase 2 - Navigate + Capture (per feature)
- Navigate using path from features.json
- Validate expected elements exist
- Screenshot with highlight/arrows on key element
- Save to: `G:\Meu Drive\TestBox\QBO-Evidence\`

### Phase 3 - Interpret + Notes (AI)
- Analyze captured screenshot
- Determine status: YES | PARTIAL | NO | NA
- Generate Internal_TBX_notes (direct, technical tone)
- Generate Intuit_notes (neutral, professional tone)

### Phase 4 - Update Spreadsheet
- Update control spreadsheet with all columns

## File Naming Convention

```
{YYYY-MM-DD}_{PROJECT}_{COMPANY}_{FEATURE}.png
```

Examples:
- `2024-12-02_TCO_Apex_ConsolidatedView.png`
- `2024-12-02_TCO_GlobalTread_ConsolidatedView.png`
- `2024-12-02_Construction_Sales_VendorCCBCC.png`

## Spreadsheet Structure

| Column | Description | Example |
|--------|-------------|---------|
| Projeto | Environment/Project | TCO, Construction, Keystone |
| Company | Specific company | Apex, Global Tread, RoadReady, Sales, Events |
| Ref | Row ID from tracker | R12, R23 |
| Feature | Feature name | Consolidated View, Vendor CC BCC |
| Status | Validation result | YES, PARTIAL, NO, NA |
| Intuit_notes | Customer-facing note | Feature available in Classic... |
| Internal_TBX_notes | TestBox internal note | Automated check passed... |
| Evidence_file | Screenshot filename | `2024-12-02_TCO_Apex_ConsolidatedView.png` |
| 📎 | Clickable chip link | [📎](drive_link) |

## Status Rules (from INTUIT BOOM v6)

| Status | When to Use |
|--------|-------------|
| **YES** | Feature works, clear evidence exists |
| **PARTIAL** | Works in Classic but not Fusion, or works with limitations |
| **NO** | Feature not found after checking settings, help docs, similar tenants |
| **NA** | Out of scope for this environment |

## Notes Generation Guidelines

### Intuit_notes (Customer-facing)
- Audience: Intuit and customer readers
- Tone: Simple, neutral, professional
- Never mention: internal tools, AI, automation
- Focus: what works, limitations, next steps

### Internal_TBX_notes (TestBox only)
- Audience: TestBox team
- Tone: Direct and simple
- Can mention: shortcuts, fragile parts, technical risks, scripts used

## Features.json Schema

```json
{
  "features": [
    {
      "id": "R12",
      "name": "Consolidated View",
      "projects": ["TCO"],
      "companies": ["Apex", "Global Tread", "RoadReady"],
      "route": "/app/consolidatedview",
      "selectors": {
        "validate": "[data-testid='consolidated-view-table']",
        "highlight": ".consolidated-header"
      },
      "interface": "Classic"
    }
  ]
}
```

## Storage Paths

| Item | Path |
|------|------|
| Screenshots | `G:\Meu Drive\TestBox\QBO-Evidence\` |
| Control Sheet | `G:\Meu Drive\TestBox\QBO-Evidence\fall_release_control.xlsx` |
| Features Config | `C:\Users\adm_r\intuit-boom\features.json` |
| Login Script | `C:\Users\adm_r\intuit-boom\intuit_login_v2_4.py` |

## Execution Mode

- **Company by company**: Select project (TCO, Construction, etc.)
- Engine runs all features for that project
- Review results before moving to next project

## Dependencies

- Python 3.x
- Playwright (already used in intuit_login_v2_4.py)
- Pillow (for screenshot annotations)
- openpyxl (for Excel manipulation)
- Claude API (for screenshot interpretation and notes generation)

## Integration with INTUIT BOOM v6 Prompt

The engine follows all rules from INTUIT BOOM v6:
- Efficiency rules (minimize logins, reuse sessions)
- Screenshot style (show exact control, avoid noise)
- Status rules (YES/PARTIAL/NO/NA criteria)
- Notes format (separate Internal and Intuit notes)
- File naming convention
