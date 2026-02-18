# QBO/IES Evidence Collection Playbook

> Consolidated from: Winter Release FY26 (32 features), UAT FY26 (33 features), QSP (3 features)
> Last updated: 2026-02-13 (QSP session)

---

## 1. END-TO-END PIPELINE

```
LOGIN → NAVIGATE → SCREENSHOT → UPLOAD → GROUP → XLSX → SPREADSHEET UPDATE
```

### Phase 1: Login (Playwright MCP)
```
1. browser_navigate → QBO login page
2. Fill email + password via browser_fill_form
3. Handle MFA:
   - TOTP: use pyotp.TOTP(secret).now() for 6-digit code
   - SMS: use 000000 for test users with +55 phone
4. Wait for dashboard load (check for "Dashboard" or company name)
5. Verify correct entity via header text
```

### Phase 2: Navigate & Capture
```
1. Navigate to feature URL (e.g., /app/projects, /app/reportlist)
2. Wait 30-45s for QBO SPA to fully render (NOT 10s!)
3. Take screenshot via browser_take_screenshot (type: png)
4. Verify: file > 100KB = valid, ~140KB = likely 404 error page
5. If 404: try alternative navigation (menu click vs direct URL)
```

### Phase 3: Upload to Drive
```python
# Pattern: upload_to_drive.py
from googleapiclient.http import MediaFileUpload
media = MediaFileUpload(fpath, mimetype='image/png', resumable=True)
result = drive.files().create(
    body={'name': fname, 'parents': [FOLDER_ID]},
    media_body=media, fields='id,name'
).execute()
```

### Phase 4: Group Screenshots into Multi-Page PDFs
```python
# Pattern: merge PNGs into 1 PDF per feature
from PIL import Image
images = [Image.open(f).convert("RGB") for f in png_files]
images[0].save(pdf_path, "PDF", resolution=100.0,
               save_all=True, append_images=images[1:])
```

### Phase 5: Create Evidence XLSX with Hyperlinks
```python
# Pattern: openpyxl with clickable Drive links
from openpyxl.styles import Font
link_font = Font(color="0563C1", underline="single", size=11)
ws.cell(row, col).value = filename
ws.cell(row, col).hyperlink = drive_web_view_link
ws.cell(row, col).font = link_font
```

### Phase 6: Update Master Spreadsheet on Drive
```python
# Pattern: download xlsx → modify → re-upload
# Download
request = drive.files().get_media(fileId=FILE_ID)
downloader = MediaIoBaseDownload(f, request)
# Modify with openpyxl
wb = openpyxl.load_workbook(path)
ws = wb['SHEET_NAME']
ws.cell(row, col).value = new_value
wb.save(path)
# Re-upload
media = MediaFileUpload(path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
drive.files().update(fileId=FILE_ID, media_body=media).execute()
```

---

## 2. SCREENSHOT NAMING CONVENTION

```
{FEATURE_PREFIX}_{SEQUENCE}_{description}.png
```

### Examples:
- `F1_ME_REPORTS_01_CV_homepage.png`
- `F2_PROJ_EST_03_PE_form_auto_opened.png`
- `F3_BUDGETS_05_populated_from_estimate.png`

### Extras (variants of same step):
- `F2_PROJ_EST_05b_deposit_autoconvert_toggle.png`
- `F2_PROJ_EST_05c_scrolled_settings.png`

### PDF Grouping (1 per feature):
- `F1_ME_REPORTS.pdf` (12 pages)
- `F2_PROJ_EST.pdf` (8 pages)
- `F3_BUDGETS.pdf` (6 pages)

---

## 3. GOOGLE DRIVE API PATTERNS

### Authentication (reusable pickle token)
```python
TOKEN_FILE = r"C:\Users\adm_r\token_drive_write.pickle"
with open(TOKEN_FILE, 'rb') as f:
    creds = pickle.load(f)
if not creds.valid:
    creds.refresh(Request())
    with open(TOKEN_FILE, 'wb') as f:
        pickle.dump(creds, f)
drive = build('drive', 'v3', credentials=creds)
```

### Token Exchange (when token expires)
```python
# 1. Generate auth URL with scopes
# 2. User visits URL, grants access, gets auth code
# 3. Exchange code for token:
resp = requests.post("https://oauth2.googleapis.com/token", data={
    "code": AUTH_CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": "http://localhost:8099/",
    "grant_type": "authorization_code",
})
# 4. Save as Credentials pickle
```

### Required Scopes
- `https://www.googleapis.com/auth/drive` (upload/download/list)
- `https://www.googleapis.com/auth/spreadsheets` (Sheets API)

### Client ID
- Project: `486245165530`
- Client: `REDACTED_GOOGLE_CLIENT_ID`
- Client secret file: `C:\Users\adm_r\Downloads\BACKUP\client_secret_486245165530-*.json`

### List Files in Folder
```python
results = drive.files().list(
    q=f"'{FOLDER_ID}' in parents and trashed = false",
    fields="files(id, name, mimeType, webViewLink)",
    orderBy="name", pageSize=100
).execute()
```

### Check for Existing File (avoid duplicates)
```python
existing = drive.files().list(
    q=f"'{FOLDER_ID}' in parents and trashed = false and name = '{filename}'",
    fields="files(id, name)"
).execute().get('files', [])
if existing:
    drive.files().update(fileId=existing[0]['id'], media_body=media).execute()
else:
    drive.files().create(body=metadata, media_body=media).execute()
```

---

## 4. XLSX STYLING PATTERNS (openpyxl)

### Color Palette (consistent across all evidence sheets)
```python
header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")  # Dark blue
header_font = Font(bold=True, size=11, color="FFFFFF")
green = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")  # VALIDATED
yellow = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")  # PARTIAL
gray = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")  # NOT TESTABLE
link_font = Font(color="0563C1", underline="single", size=11)  # Hyperlinks
```

### Merged Cells for Feature Groups
```python
ws.merge_cells(start_row=first_row, start_column=1, end_row=last_row, end_column=1)
```

### Freeze Header
```python
ws.freeze_panes = "A2"
```

---

## 5. QBO NAVIGATION PATTERNS

### Entity Switcher (Consolidated View)
- Click gear icon → Switch company → Select "(Event)" suffix entity for CV
- CV URL pattern: different CID in URL, shows "Consolidated" label

### Key URLs
| Feature | URL |
|---------|-----|
| Standard Reports | `/app/standardreports` (NOT `/app/reportlist` - 404!) |
| Projects | `/app/projects` |
| Estimates | `/app/estimates` (in Customer Hub) |
| Settings > Sales | `/app/salesSettings` |
| Dimensions | `/app/dimensions` |
| Workflows | `/app/workflows` |
| Sales Orders | inventory menu → Sales orders |
| Budget | Inside project → Budget tab |

### Common Pitfalls
- QBO Reports URL changed: `/app/standardreports` (NOT `/app/reportlist` which gives 404)
- Entity switcher: "(Event)" suffix = consolidated view parent
- PM Agent panel: scroll may not work via JS (accept screenshot as-is)
- `browser_wait_for` can return 241K chars output → use `browser_snapshot` instead
- Budget creation: may work even when expected to be blocked by feature flag

### TOTP Authentication
```python
import pyotp
totp = pyotp.TOTP(TOTP_SECRET)
code = totp.now()  # 6-digit string
```

---

## 6. PIL/PILLOW TECHNIQUES

### Add Border to Screenshots
```python
from PIL import Image, ImageOps
img = Image.open(path)
bordered = ImageOps.expand(img, border=3, fill=(24, 32, 63))  # dark navy
bordered.save(output_path)
```

### Vertical Stitch (grouped image)
```python
max_width = max(img.width for img in images)
total_height = sum(img.height for img in images) + GAP * (len(images) - 1)
canvas = Image.new("RGB", (max_width, total_height), (245, 245, 245))
y_offset = 0
for img in images:
    x_offset = (max_width - img.width) // 2
    canvas.paste(img, (x_offset, y_offset))
    y_offset += img.height + GAP
canvas.save(out_path, "PNG", optimize=True)
```

### PNG to Multi-Page PDF
```python
images = [Image.open(f).convert("RGB") for f in sorted_files]
images[0].save(pdf_path, "PDF", resolution=100.0,
               save_all=True, append_images=images[1:])
# Result: 1 PDF with N pages, each page = 1 screenshot
```

---

## 7. EVIDENCE NOTES TEMPLATE

### For VALIDATED features:
```
{What is visible on the page/form}. {Specific data points with numbers}.
{Second observation with drill-down details}.

{Settings or configuration that confirms the feature}.
{Cross-entity data if applicable: Entity A ($X) + Entity B ($Y) = Total ($Z)}.

{Functional elements: buttons, toggles, dropdowns confirmed working}.
```

### For NOT TESTABLE features:
```
{Where we looked}. {What we expected to find}.
{Why it cannot be tested} (e.g., requires new tenant, feature flag OFF, QBDT required).
```

### For PARTIAL features:
```
{What works}. {What doesn't work and why}.
{Prereqs not met} (e.g., insufficient data volume, integration not connected).
```

---

## 8. VALIDATION STATUS DEFINITIONS

| Status | Meaning | When to Use |
|--------|---------|-------------|
| VALIDATED | Feature works as described | All checks pass, evidence captured |
| PARTIAL | Feature exists but limited | Some checks pass, prereqs missing |
| NOT TESTABLE | Cannot validate in this env | Requires new tenant, QBDT, specific flag |
| NOT AVAILABLE | Feature not enabled | Flag OFF, no UI entry point |
| INTUIT PENDING | Waiting on Intuit action | Flag needs enablement, permission needed |
| BLOCKED | Known blocker | Engineering issue, environment problem |

---

## 9. DRIVE FOLDER STRUCTURE

### Pattern per Evidence Session
```
Google Drive/
└── {PROJECT_FOLDER}/
    ├── screenshots/          # Individual PNGs (all features)
    ├── F1_{FEATURE}.pdf      # Grouped PDF per feature
    ├── F2_{FEATURE}.pdf
    ├── F3_{FEATURE}.pdf
    └── Evidence_Links.xlsx   # XLSX with hyperlinks to PDFs
```

### Key Drive Folders
| Session | Folder ID | Content |
|---------|-----------|---------|
| Winter Release FY26 | `10URLS9-FxuRYsCSiPPuZqq-XZiYJwuW8` | 107 files (104 PNG + 2 TXT + 1 xlsx) |
| UAT FY26 | `1qRheOtws5oFEdizef3IiDjppMd99Ssfi` | ~190+ screenshots |
| QSP | `1M8_5zyCv0VTGStrcwnzxk77dGWLvA2PX` | 26 PNG + 3 PDF |

### Key Spreadsheets
| Session | File ID | Format | Tab |
|---------|---------|--------|-----|
| Winter Release | `1zfa0f0txdOs5O3uR8MkrVx2o4scFpiUS` | xlsx | CONS.SALES |
| UAT | `1dhkwUMQXQSzXAVDrKrZS26XMl4rN6bEe` | gsheet | CONS.UAT |
| QSP | `1bTLnIbYfAcWmDH_qq4YSOeAYTMeuL7b0` | xlsx | CONS.SALES |

---

## 10. REUSABLE SCRIPTS INVENTORY

### Evidence Collection
| Script | Location | Purpose |
|--------|----------|---------|
| `upload_to_drive.py` | `QSP_EVIDENCE/` | Batch upload PNGs to Drive folder |
| `merge_and_link.py` | `QSP_EVIDENCE/` | PNGs→PDFs + upload + XLSX with links |
| `update_gsheet.py` | `QSP_EVIDENCE/` | Download xlsx → modify → re-upload |
| `create_evidence_xlsx.py` | `QSP_EVIDENCE/` | Standalone XLSX with Drive hyperlinks |
| `group_screenshots.py` | `QSP_EVIDENCE/` | Vertical stitch PNGs by feature |

### Token Management
| Script | Location | Purpose |
|--------|----------|---------|
| `exchange_token.py` | `WINTER_RELEASE_EVIDENCE_2026/` | Auth code → pickle token |
| Token file | `C:\Users\adm_r\token_drive_write.pickle` | Reusable across all sessions |

### Winter Release Specific
| Script | Location | Purpose |
|--------|----------|---------|
| `gen_notes_xlsx.py` | `WINTER_RELEASE_EVIDENCE_2026/` | 26 features XLSX with notes |
| `gen_16_notes.py` | `WINTER_RELEASE_EVIDENCE_2026/` | 16 features batch update |
| `apps_script.js` | `WINTER_RELEASE_EVIDENCE/` | Google Sheets hyperlinks via Apps Script |

### Image Processing
| Script | Location | Purpose |
|--------|----------|---------|
| `process_new_screenshots.py` | `GEM-BOOM/` | Add borders to PNGs |
| `annotate_screenshots.py` | `PRINTS SETAS/logs/` | Add arrows/labels to PNGs |

---

## 11. QBO LOGIN CREDENTIALS (Evidence Environments)

| Environment | Email | Password | MFA |
|-------------|-------|----------|-----|
| Construction (Par) | quickbooks-test-account@tbxofficial.com | TestBox123! | TOTP |
| QSP | quickbooks-test-account-qsp@tbxofficial.com | TestBox123! | TOTP: `J4NUWKE7OZTIBOXI3MP42Z4QVBDDNITH` |
| TCO | quickbooks-testuser-tco-tbxdemo@tbxofficial.com | TestBox123! | varies |
| Product | quickbooks-tbx-product-team-test@tbxofficial.com | TestBox123! | varies |

---

## 12. LESSONS LEARNED

### From Winter Release (Dec 2025)
1. IES = ALL features (not subset) - validate full scope
2. Screenshot > 100KB = valid, ~140KB = likely 404
3. 30-45s wait time for QBO SPA (not 10s)
4. 404 = investigate alternative nav, don't just mark N/A
5. Group by context: capture all features in same entity before switching

### From UAT (Feb 2026)
1. Google Sheets Name Box: use `#t-name-box` (NOT `[aria-label="Name Box"]`)
2. Smart chips `@` search doesn't find files in shared Drive
3. Drive upload lazy loading: files may not appear immediately
4. QBO Standard Reports URL: `/app/standardreports` (NOT `/app/reportlist`)

### From QSP (Feb 2026)
1. Budgets v3 worked even when expected to be blocked by feature flag
2. PM Agent panel scroll doesn't work via JS - accept screenshot as-is
3. `browser_wait_for` output can exceed 241K chars - use snapshot instead
4. PNG→multi-page PDF via PIL is the standard grouping format (not stitched images)
5. Always check for existing files in Drive before uploading (avoid duplicates)
6. Windows paths with backslash need `cd` alternative: use full path in python command

### From PRINTS SETAS (Feb 2026)
1. gdown FAILS on private Drive → use browser cookies + Python requests
2. Drive Ctrl+A selects only ~50 visible rows (virtual scrolling)
3. Extract cookies: `page.context().cookies('https://drive.google.com')` via Playwright
4. Drive file IDs: `[role="row"][data-id]` + `strong` in DOM (2 passes for full coverage)
