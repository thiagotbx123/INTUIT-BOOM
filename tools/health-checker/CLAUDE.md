# QBO Health Checker - Instructions for Claude

## What This Project Is

Automated UAT/Health Check methodology for QuickBooks Online (QBO) and Intuit Enterprise Suite (IES). Uses Claude Code + Playwright MCP to validate features, capture evidence, and report results.

## How It Works

### 5-Step Workflow
```
1. DEFINE    → Load feature from playbook YAML
2. NAVIGATE  → Open QBO page (use qbo_navigation.md for correct URLs)
3. CAPTURE   → Take screenshots (naming: {row:02d}_ID{id:02d}_{seq:02d}_{desc}.jpeg)
4. UPLOAD    → Upload to Google Drive folder, extract file IDs via DOM
5. REPORT    → Update Google Sheet (status + filenames + hyperlinks)
```

### Before Starting a Session
1. Read the playbook YAML for the current release cycle
2. Check which features still need validation
3. Identify any blockers (feature flags, environment limitations)

### Screenshot Naming Convention
```
{row:02d}_ID{feature_id:02d}_{seq:02d}_{description}.jpeg
```
Example: `02_ID16_01_kpi_scorecard_overview.jpeg`

## Key References

| Need | File |
|------|------|
| QBO URL patterns | `knowledge-base/qbo_urls.md` |
| Playwright snippets | `automation/playwright_patterns.md` |
| Google Sheets tricks | `automation/google_sheets.md` |
| Google Drive upload | `automation/google_drive.md` |
| QBO navigation | `automation/qbo_navigation.md` |
| Feature definitions | `playbooks/*.yaml` |

## Critical Rules

1. **URL for Chart of Accounts**: `/app/chartofaccounts?jobId=accounting` (NOT `/app/chart-of-accounts`)
2. **Multi-line cells**: 400ms+ delay between Ctrl+Enter presses
3. **Hyperlink batches**: Max 7 per batch, use Escape (not Enter) to confirm
4. **Drive lazy loading**: Scroll 30 iterations before extracting file IDs
5. **Business Feed**: 60s timeout minimum, may freeze - use page.reload()
6. **Entity switching**: Wait 5s after switching for full context reload
7. **Never overwrite existing cell data** without confirming with user first

## Session Protocol

### Start
1. Read this CLAUDE.md
2. Load playbook for current cycle
3. Check previous session files for context

### End
1. Document what was validated in `sessions/` folder
2. Update playbook with results
3. Commit changes
