# QBO Health Checker

Automated UAT and Health Check methodology for **QuickBooks Online (QBO)** and **Intuit Enterprise Suite (IES)** using **Claude Code + Playwright MCP**.

Proven on the Winter Release FY26 UAT: 33 features processed, 22 validated, across ~10 sessions in 4 days.

---

## What It Does

Provides a structured, repeatable method to:
- Validate QBO/IES features against release notes
- Capture screenshot evidence for each feature
- Upload evidence to Google Drive with organized naming
- Track validation status in Google Sheets with hyperlinked evidence
- Generate summary reports of UAT/health check results

## Prerequisites

- **Claude Code** with Playwright MCP server configured
- **Google Account** with access to Drive and Sheets
- **QBO/IES access** via TestBox or direct login
- **Browser session** authenticated to QBO, Google Drive, and Google Sheets

## Workflow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  DEFINE  │───>│ NAVIGATE │───>│ CAPTURE  │───>│  UPLOAD  │───>│  REPORT  │
│          │    │          │    │          │    │          │    │          │
│ Load     │    │ Open QBO │    │ Take     │    │ Upload   │    │ Update   │
│ feature  │    │ page via │    │ screen-  │    │ to Drive │    │ Google   │
│ from     │    │ URL or   │    │ shots    │    │ folder   │    │ Sheet    │
│ playbook │    │ click    │    │ with     │    │ extract  │    │ status + │
│ YAML     │    │ path     │    │ naming   │    │ file IDs │    │ evidence │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### Step 1: Define
Load the feature definition from a playbook YAML file. Each feature includes:
- Click path (navigation instructions)
- Step-by-step validation procedure
- Expected validation checks
- Screenshot naming prefix

### Step 2: Navigate
Open the QBO/IES page using the correct URL. See `automation/qbo_navigation.md` for the URL map and known gotchas (e.g., `/app/chartofaccounts?jobId=accounting`, NOT `/app/chart-of-accounts`).

### Step 3: Capture
Take screenshots following the naming convention:
```
{row:02d}_ID{feature_id:02d}_{seq:02d}_{description}.jpeg
```
Example: `02_ID16_01_kpi_scorecard_overview.jpeg`

### Step 4: Upload
Upload screenshots to a Google Drive folder. Extract file IDs via DOM `[data-id]` attributes (requires scrolling to handle lazy loading). See `automation/google_drive.md`.

### Step 5: Report
Update the tracking Google Sheet:
- Set feature status (VALIDATED / BLOCKED / NOT TESTABLE / EXCLUDED)
- Add evidence filenames
- Create hyperlinks to Drive files using Ctrl+K method

See `automation/google_sheets.md` for all patterns.

## Quick Start

### 1. Create a New Playbook
```bash
cp playbooks/_template.yaml playbooks/my_release.yaml
```

Edit the YAML to define your features. Use `config/features_template.yaml` as reference for the feature schema.

### 2. Set Up Tracking
- Create a Google Sheet for tracking (or use existing)
- Create a Google Drive folder for evidence
- Add the IDs to your playbook YAML

### 3. Run Validation
Open Claude Code with Playwright MCP and work through features one by one following the 5-step workflow.

### 4. Generate Summary
After all features are processed, review `output/examples/winter_fy26_summary.md` as a template for your summary report.

## Project Structure

```
QBO_HEALTH_CHECKER/
├── README.md                    # This file
├── CLAUDE.md                    # Instructions for Claude Code
├── package.json                 # Project metadata
├── .gitignore                   # Ignores screenshots, .env, etc.
│
├── config/
│   └── features_template.yaml   # Schema reference for feature definitions
│
├── playbooks/
│   ├── _template.yaml           # Empty template for new playbooks
│   └── winter_release_fy26.yaml # Real example: 33 features from Winter Release
│
├── automation/
│   ├── playwright_patterns.md   # All reusable Playwright MCP snippets
│   ├── google_sheets.md         # Google Sheets automation patterns
│   ├── google_drive.md          # Google Drive upload/extraction patterns
│   └── qbo_navigation.md       # QBO/IES URL map and navigation patterns
│
├── output/                      # Results (gitignored except examples)
│   └── examples/
│       └── winter_fy26_summary.md  # Example summary report
│
├── sessions/                    # Session history (gitignored except template)
│   └── _template.md
│
└── knowledge-base/
    └── qbo_urls.md              # Complete QBO/IES URL reference
```

## Key Patterns Reference

| Pattern | File | Description |
|---------|------|-------------|
| Screenshot naming | `automation/playwright_patterns.md` | `{row}_ID{id}_{seq}_{desc}.jpeg` |
| Drive file upload | `automation/google_drive.md` | New button + file chooser |
| Drive ID extraction | `automation/google_drive.md` | `[data-id]` DOM query |
| Sheet cell navigation | `automation/google_sheets.md` | Name Box `#t-name-box` |
| Multi-line cell input | `automation/google_sheets.md` | Ctrl+Enter with 400ms delays |
| Hyperlink creation | `automation/google_sheets.md` | Ctrl+K method |
| QBO URL map | `automation/qbo_navigation.md` | Correct URLs with `?jobId` |
| Page timeout recovery | `automation/qbo_navigation.md` | Reload on freeze |

## Status Values

| Status | Meaning |
|--------|---------|
| VALIDATED | Feature works as documented |
| BLOCKED | Cannot test (feature flag OFF, environment limitation) |
| NOT TESTABLE | Requires conditions unavailable (new account, QBDT, etc.) |
| EXCLUDED | Feature not shipping in this release |

## Winter Release FY26 Results

The first complete run of this methodology:
- **33 features** defined and processed
- **22 validated** (66.7%)
- **7 blocked** (feature flags or environment)
- **3 not testable** (QBDT or new account required)
- **1 excluded** (not shipping)
- **~10 sessions** over 4 days
- **~150+ screenshots** captured and uploaded

See `output/examples/winter_fy26_summary.md` for the full results.
