# Winter Release FY26 - UAT & SALES Prints Knowledge Base
**Created**: 2026-02-17
**Source Session**: HOME session - PDF grouping + hyperlinks

---

## 1. Spreadsheet Architecture

### SALES Spreadsheet
- **File**: `00_Winter_Release_FY26_Feature_Check_Plan_v2.xlsx`
- **Drive ID**: `1zfa0f0txdOs5O3uR8MkrVx2o4scFpiUS`
- **Sheet**: `CONS.SALES`
- **Format**: XLSX (NOT native Google Sheet - Sheets API does NOT work)
- **Key Columns**:
  - A = Feature name
  - B = Click Path
  - C = USER Step-by-Step
  - D = Validation Checks
  - E = Status
  - F = Testbox Notes
  - G = Evidence
  - **H = SCREENSHOTS/EVIDENCES** (hyperlinks go here)
  - I = Notes for Intuit
  - J = Seq (sequence number)
  - K = ID (feature ID)
- **Rows**: 2-31 (30 features) + row 32 (DFY Migration) + row 33 (Customer AI)

### UAT Spreadsheet
- **File**: `00_Winter_Release_FY26_Feature_Check_Plan_UAT_v2.xlsx`
- **Drive ID**: `1dhkwUMQXQSzXAVDrKrZS26XMl4rN6bEe`
- **Sheet**: `CONS.UAT`
- **Key Columns** (DIFFERENT from SALES):
  - A = Feature name
  - B-F = same pattern
  - **G = SCREENSHOTS** (hyperlinks go here - NOT column H!)
  - H = Notes for Intuit
  - I = Seq
  - J = ID
- **Rows**: 2-33 (32 features)

### CRITICAL: Column Shift Between SALES and UAT
- SALES: Screenshots = **col H**, Seq = **col J**, ID = **col K**
- UAT: Screenshots = **col G**, Seq = **col I**, ID = **col J**
- Always verify column structure before writing data

---

## 2. Screenshot Naming Convention

### Pattern
```
{SEQ}_{IDXX}_{sequence_number}_{description}.{ext}
```
Examples:
- `01_ID16_01_reports_menu.png` → Seq=1, Feature ID=16, 1st screenshot
- `23_ID29_03_budget_export_excel.jpeg` → Seq=23, Feature ID=29, 3rd screenshot

### CRITICAL: Seq Numbers Differ Between SALES and UAT
Same feature has DIFFERENT Seq numbers in each spreadsheet:

| Feature | SALES Seq | UAT Seq |
|---------|-----------|---------|
| KPIs | 01 | 02 |
| Budgets v3 | 22 | 23 |
| Change Orders | 23 | 24 |
| etc. | ... | ... |

**Never assume SALES Seq = UAT Seq**. Always read the Seq from each spreadsheet independently.

---

## 3. Drive Folder Structure

### SALES Screenshots
- **Folder**: `10URLS9-FxuRYsCSiPPuZqq-XZiYJwuW8` (WINTER_RELEASE_EVIDENCE/SALES)
- **Contents**: 177 PNGs + 2 TXT (N/A files) + grouped PDFs
- **PDF count**: 31

### UAT Screenshots
- **Root folder**: `1qRheOtws5oFEdizef3IiDjppMd99Ssfi`
- **Subfolder**: `1xQQj4y16nXaiWDgUb_BhhvPKJSP3suMb` (PRINT_BACKUP_CLONE_UAT)
- **Contents**: 242 files (237 JPEG + 5 PNG) + grouped PDFs
- **PDF count**: 37 (more than SALES because some features have split groups)

---

## 4. PDF Grouping Process

### Steps
1. Download all screenshots from Drive folder (via API `alt=media`)
2. Group files by prefix `{SEQ}_{IDXX}` extracted via regex `^(\d+_ID\d+)`
3. Sort files within each group alphabetically (preserves sequence order)
4. Use Pillow to create multi-page PDF: `img.save(path, save_all=True, append_images=[...])`
5. Upload PDFs to Drive folder
6. List PDFs in Drive to get file IDs
7. Write hyperlinks in spreadsheet column

### Code Pattern
```python
from PIL import Image
images = [Image.open(f).convert('RGB') for f in sorted_files]
images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=100.0)
```

---

## 5. Hyperlink Best Practices

### WRONG: Formula-based hyperlinks in XLSX
```python
# This does NOT work reliably in Google Sheets opening XLSX
cell.value = '=HYPERLINK("url", "label")'
```
When Google Sheets opens an XLSX with `=HYPERLINK()` formulas, clicking the cell may not navigate to the URL correctly.

### CORRECT: Native cell hyperlink
```python
from openpyxl.styles import Font
cell.value = 'display_name.pdf'
cell.hyperlink = 'https://drive.google.com/file/d/FILE_ID/view?usp=drive_link'
cell.font = Font(color='0563C1', underline='single')
```
This creates a proper clickable hyperlink that works when the XLSX is opened in Google Sheets.

---

## 6. Spreadsheet Content Origin (CRITICAL LEARNING)

### What's Pre-Populated vs What's Test Results
The spreadsheet `Feature_Check_Plan` has TWO types of content:

**PRE-POPULATED (Test Plan / Script)**:
- **Click Path**: Navigation instructions ("Go to Reports > KPIs")
- **USER Step-by-Step**: Detailed test procedure
- **Validation Checks**: What to verify
- **Evidence (prints list)**: What screenshots to capture

These exist EVEN WHEN Feature Flag = OFF. They describe WHAT TO TEST, not test results.

**TEST RESULTS (Filled During/After Testing)**:
- **Status**: VALIDATED / NOT STARTED / BLOCKED / etc.
- **Testbox Notes**: What the tester actually observed
- **Notes for Intuit**: Issues/blockers found

### UNKNOWN: Origin of Pre-Populated Content
- The Click Path and Step-by-Step content was already in the spreadsheet
- **We do NOT know the definitive source** - could be:
  - Intuit's "Write It Straight" documentation
  - Internal TestBox test planning
  - Copied from another reference/gabarito
- **Do NOT assume "it came from Intuit"** without evidence

### Data Quality Issues Found
- **Budgets v3**: Flag ON = NO, but Click Path and Step-by-Step filled
  - Status = VALIDATED but Evidence says "BLOCKED"
  - Testbox Notes mentions "Project Reports" (wrong feature content)
- **Lesson**: Always cross-check Status vs Flag vs Evidence vs Notes for consistency

---

## 7. Google API Access

### Current Token Scope
- **Scope**: `drive.readonly` (from TSA_CORTEX .env)
- **Can**: List files, download files, read metadata
- **Cannot**: Upload files, write to Sheets, modify Drive

### Credentials Location
- `C:\Users\adm_r\Tools\TSA_CORTEX\.env`
- Client ID: `486245165530-...`
- Refresh Token: stored in .env

### To Get Write Access
- Need to regenerate token with broader scope using `scripts/get-google-token.js`
- Change SCOPES to include `drive` (not just `drive.readonly`) and `spreadsheets`

---

## 8. Local File Locations

### SALES
```
C:\Users\adm_r\Downloads\PRINTS SETAS\
├── raw_downloads/     (177 original files)
├── annotated/         (177 annotated files from audit)
├── grouped/           (31 PDFs + XLSX files)
│   ├── 01_ID16_KPIs.pdf
│   ├── ...
│   ├── SALES_WITH_HYPERLINKS.xlsx
│   └── SALES_ORIGINAL.xlsx
└── logs/              (scripts + JSON inventories)
```

### UAT
```
C:\Users\adm_r\Downloads\UAT_PRINTS\
├── raw_downloads/     (242 original files)
├── grouped/           (37 PDFs + XLSX files)
│   ├── 02_ID16_KPIs.pdf
│   ├── ...
│   ├── UAT_WITH_HYPERLINKS.xlsx
│   ├── UAT_FRESH.xlsx
│   └── UAT_TEST_ROW2.xlsx
└── uat_file_inventory.json
```

---

## 9. Feature Mapping (32 Features)

| Row | Feature | SALES Seq_ID | UAT Seq_ID |
|-----|---------|-------------|------------|
| 2 | KPIs | 01_ID16 | 02_ID16 |
| 3 | Dashboards | 02_ID17 | 03_ID17 |
| 4 | 3P Data | 03_ID18 | 04_ID18 |
| 5 | Management Reports | 04_ID20 | 05_ID20 |
| 6 | New Modern Reports | 05_ID21 | 06_ID21 |
| 7 | Finance AI | 06_ID13 | 07_ID13 |
| 8 | Calculated Fields | 07_ID19 | 08_ID08 |
| 9 | New ME Reports | 08_ID24 | 09_ID24 |
| 10 | Smart Dimension v2 | 09_ID22 | 10_ID22 |
| 11 | Dimensions Workflow | 10_ID23 | 11_ID23 |
| 12 | Parallel Approval | 11_ID25 | 12_ID25 |
| 13 | Platform Custom | 12_ID35 | 13_ID35 |
| 14 | Sales Tax AI | 13_ID11 | 14_ID11 |
| 15 | Accounting AI | 14_ID10 | 15_ID10 |
| 16 | Project Estimates | 15_ID34 | 16_ID34 |
| 17 | Proposals | 16_ID31 | 17_ID31 |
| 18 | Sales Orders | 17_ID41 | 18_ID41 |
| 19 | Cost Groups | 18_ID28 | 19_ID28 |
| 20 | Moving Avg Cost | 19_ID40 | 20_ID40 |
| 21 | Project Phases v2 | 20_ID27 | 21_ID27 |
| 22 | AIA Billing | 21_ID30 | 22_ID30 |
| 23 | Budgets v3 | 22_ID29 | 23_ID29 |
| 24 | Change Orders | 23_ID32 | 24_ID32 |
| 25 | PM AI | 24_ID12 | 25_ID24 |
| 26 | PM AI Enhancements | 25_ID33 | 31_ID35 |
| 27 | Item Receipt | 26_ID39 | 27_ID39 |
| 28 | Garnishments | 27_ID37 | 28_ID37 |
| 29 | Time 2.0 | 28_ID38 | 29_ID38 |
| 30 | ME Employee Hub | 29_ID36 | N/A |
| 31 | Solutions COA | 30_ID15 | 31_ID15 |
| 32 | DFY Migration | 31_ID26 | N/A |
| 33 | Customer AI | 32_ID14 | N/A |

---

## 10. Anti-Patterns (Don't Do This)

1. **Don't assume column positions** - SALES and UAT have different column layouts
2. **Don't assume Seq numbers match** - Same feature has different Seq in each sheet
3. **Don't use =HYPERLINK() formula** in XLSX for Google Sheets - use native hyperlinks
4. **Don't trust spreadsheet content blindly** - Cross-check Status vs Flag vs Evidence
5. **Don't assume pre-populated content = test results** - Click Path is test script, not evidence
6. **Don't claim to know the source of content without evidence** - Trace origins explicitly
7. **Don't use `drive.readonly` token for write operations** - Will get 403
