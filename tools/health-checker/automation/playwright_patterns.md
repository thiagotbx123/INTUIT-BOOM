# Playwright MCP Patterns for QBO UAT Automation

> Reusable copy-pasteable snippets extracted from 10+ UAT sessions.
> All examples use the Playwright MCP tools (`browser_*` family).

---

## Table of Contents

1. [Screenshot Capture](#screenshot-capture)
2. [Google Drive Operations](#google-drive-operations)
3. [Google Sheets Operations](#google-sheets-operations)
4. [QBO Navigation](#qbo-navigation)
5. [Tips and Gotchas](#tips-and-gotchas)

---

## Screenshot Capture

### Naming Convention

```
{row:02d}_ID{feature_id:02d}_{seq:02d}_{description}.jpeg
```

Examples:
- `02_ID16_01_kpi_scorecard_overview.jpeg`
- `29_ID38_03_assignments_customer_tab.jpeg`
- `14_ID05_02_consolidated_reporting_filters.jpeg`

### Full-Page Screenshot

Use `browser_take_screenshot` with `fullPage: true` to capture the entire scrollable page.

```
Tool: browser_take_screenshot
Parameters:
  type: "jpeg"
  filename: "02_ID16_01_kpi_scorecard_overview.jpeg"
  fullPage: true
```

### Viewport-Only Screenshot

Use `browser_take_screenshot` without `fullPage` for above-the-fold captures.

```
Tool: browser_take_screenshot
Parameters:
  type: "jpeg"
  filename: "29_ID38_01_assignments_overview.jpeg"
```

### Element-Specific Screenshot

Use `ref` from a `browser_snapshot` to screenshot a single element.

```
Tool: browser_take_screenshot
Parameters:
  type: "jpeg"
  filename: "14_ID05_03_chart_widget.jpeg"
  element: "KPI chart widget"
  ref: "e42"
```

---

## Google Drive Operations

### Upload Files to a Drive Folder

```javascript
// Tool: browser_navigate
// URL: https://drive.google.com/drive/folders/{FOLDER_ID}

// Tool: browser_run_code
async (page) => {
  // 1. Click "New" button
  await page.locator('[guidedhelpid="new_menu_button"]').click();
  await page.waitForTimeout(1000);

  // 2. Click "File upload" from the menu
  const menuItems = page.locator('[role="menuitem"]');
  await menuItems.filter({ hasText: 'File upload' }).click();

  // 3. Handle file chooser
  const [fileChooser] = await Promise.all([
    page.waitForEvent('filechooser'),
  ]);
  await fileChooser.setInputFiles('/absolute/path/to/file.jpeg');
}
```

### Upload Multiple Files at Once

```javascript
// Tool: browser_run_code
async (page) => {
  await page.locator('[guidedhelpid="new_menu_button"]').click();
  await page.waitForTimeout(1000);

  const menuItems = page.locator('[role="menuitem"]');
  await menuItems.filter({ hasText: 'File upload' }).click();

  const [fileChooser] = await Promise.all([
    page.waitForEvent('filechooser'),
  ]);
  await fileChooser.setInputFiles([
    '/path/to/file1.jpeg',
    '/path/to/file2.jpeg',
    '/path/to/file3.jpeg'
  ]);
}
```

### Extract File IDs from Drive DOM

Drive uses `[data-id]` attributes on file elements. Files are lazy-loaded, so you must scroll first.

```javascript
// Tool: browser_run_code
async (page) => {
  // Step 1: Scroll all scrollable containers to load lazy content
  for (let i = 0; i < 30; i++) {
    await page.evaluate(() => {
      document.querySelectorAll('*').forEach(el => {
        if (el.scrollHeight > el.clientHeight + 100) {
          el.scrollTop = el.scrollHeight;
        }
      });
    });
    await page.waitForTimeout(500);
  }

  // Step 2: Extract file IDs and names
  const result = await page.evaluate(() => {
    const files = [];
    const seen = new Set();
    document.querySelectorAll('[data-id]').forEach(el => {
      const id = el.getAttribute('data-id');
      if (!id || seen.has(id)) return;
      seen.add(id);
      const strongEl = el.querySelector('strong');
      const name = strongEl ? strongEl.textContent.trim() : '';
      if (name && (name.endsWith('.png') || name.endsWith('.jpeg') || name.endsWith('.jpg'))) {
        files.push({ id, name });
      }
    });
    return files;
  });

  return JSON.stringify(result, null, 2);
}
```

### Drive File URL Pattern

Use this pattern to build viewable URLs from extracted file IDs:

```
https://drive.google.com/file/d/{FILE_ID}/view
```

---

## Google Sheets Operations

### Navigate to a Specific Cell (Name Box)

The Name Box (`#t-name-box`) is the fastest and most reliable way to jump to any cell. Prefer this over snapshot refs, which change on every snapshot.

```javascript
// Tool: browser_run_code
async (page) => {
  const nameBox = page.locator('#t-name-box');
  await nameBox.click();
  await nameBox.fill('E29');  // Target cell reference
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);
}
```

### Update Cell Value (Simple Text)

```javascript
// Tool: browser_run_code
async (page) => {
  // Navigate to cell
  const nameBox = page.locator('#t-name-box');
  await nameBox.click();
  await nameBox.fill('E29');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);

  // Type value (replaces current content when not in edit mode)
  await page.keyboard.type('VALIDATED');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);
}
```

### Type Multi-Line Content in a Cell

Use `Ctrl+Enter` to insert line breaks within a cell. The 400ms delay between lines is critical -- without it, lines may concatenate.

```javascript
// Tool: browser_run_code
async (page) => {
  // Navigate to cell first (see Name Box pattern above)
  const nameBox = page.locator('#t-name-box');
  await nameBox.click();
  await nameBox.fill('G29');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);

  // Enter edit mode
  await page.keyboard.press('F2');

  // Type each line with Ctrl+Enter between them
  await page.keyboard.type('02_ID16_01_overview.jpeg');
  await page.keyboard.press('Control+Enter');
  await page.waitForTimeout(400);  // CRITICAL: 400ms+ delay between lines

  await page.keyboard.type('02_ID16_02_detail.jpeg');
  await page.keyboard.press('Control+Enter');
  await page.waitForTimeout(400);

  await page.keyboard.type('02_ID16_03_settings.jpeg');

  // Confirm with Escape (preserves formatting better than Enter)
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);
}
```

### Add Hyperlink to Selected Text (Ctrl+K)

```javascript
// Tool: browser_run_code
async (page) => {
  // 1. Enter edit mode and select the text on current line
  await page.keyboard.press('F2');
  await page.keyboard.press('Home');       // Go to beginning of line
  await page.keyboard.press('Shift+End');  // Select entire line

  // 2. Open Insert Link dialog
  await page.keyboard.press('Control+k');
  await page.waitForTimeout(800);

  // 3. Fill URL in the Link combobox
  const linkInput = page.getByRole('combobox', { name: 'Link' });
  await linkInput.fill('https://drive.google.com/file/d/FILE_ID/view');
  await page.waitForTimeout(500);

  // 4. Click Apply
  await page.getByRole('button', { name: 'Apply' }).click();
  await page.waitForTimeout(500);

  // 5. Move cursor to start of next line
  await page.keyboard.press('End');
  await page.keyboard.press('ArrowRight');
}
```

### Multiple Hyperlinks in One Cell (Batch Method)

When a cell has many filenames that each need a hyperlink, split into batches of 7. Processing more than 7 in sequence can cause errors on the last link.

```javascript
// Tool: browser_run_code
async (page) => {
  // === BATCH 1: First 7 filenames ===

  // Navigate to cell and enter edit mode
  const nameBox = page.locator('#t-name-box');
  await nameBox.click();
  await nameBox.fill('G29');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);
  await page.keyboard.press('F2');

  // Type all 7 filenames with Ctrl+Enter between them
  const batch1Files = [
    '02_ID16_01_overview.jpeg',
    '02_ID16_02_detail.jpeg',
    '02_ID16_03_settings.jpeg',
    '02_ID16_04_report.jpeg',
    '02_ID16_05_chart.jpeg',
    '02_ID16_06_export.jpeg',
    '02_ID16_07_final.jpeg',
  ];

  for (let i = 0; i < batch1Files.length; i++) {
    await page.keyboard.type(batch1Files[i]);
    if (i < batch1Files.length - 1) {
      await page.keyboard.press('Control+Enter');
      await page.waitForTimeout(400);
    }
  }

  // Escape to save, then re-enter to add hyperlinks
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);

  // Now add hyperlinks one by one (re-enter edit mode)
  // Navigate back to the cell
  await nameBox.click();
  await nameBox.fill('G29');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);
  await page.keyboard.press('F2');
  await page.keyboard.press('Home');  // Go to first line

  // For each filename: select line, Ctrl+K, paste URL, Apply, move to next line
  const fileIds = ['id1', 'id2', 'id3', 'id4', 'id5', 'id6', 'id7'];

  for (let i = 0; i < fileIds.length; i++) {
    await page.keyboard.press('Home');
    await page.keyboard.press('Shift+End');
    await page.keyboard.press('Control+k');
    await page.waitForTimeout(800);

    const linkInput = page.getByRole('combobox', { name: 'Link' });
    await linkInput.fill(`https://drive.google.com/file/d/${fileIds[i]}/view`);
    await page.waitForTimeout(500);

    await page.getByRole('button', { name: 'Apply' }).click();
    await page.waitForTimeout(500);

    // Move to next line (unless last)
    if (i < fileIds.length - 1) {
      await page.keyboard.press('End');
      await page.keyboard.press('ArrowRight');
    }
  }

  // IMPORTANT: Use Escape to confirm (not Enter)
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);

  // === BATCH 2: Remaining filenames ===
  // Re-enter the cell, position cursor at end, continue with Ctrl+Enter + more filenames
  // Then repeat hyperlink loop for the new lines
}
```

### Read Cell Value via Evaluate

```javascript
// Tool: browser_evaluate
// When snapshot is too large, read cell value directly
async (page) => {
  // Navigate to cell
  const nameBox = page.locator('#t-name-box');
  await nameBox.click();
  await nameBox.fill('E29');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);

  // Read from formula bar
  const formulaBar = page.locator('#t-formula-bar-input-container');
  const value = await formulaBar.textContent();
  return value;
}
```

### Snapshot Too Large Workaround

Google Sheets snapshots regularly exceed 90K characters. Save to a file instead and search with Grep.

```
Tool: browser_snapshot
Parameters:
  filename: "sheets_snapshot.md"

Then use Grep to find specific content in the saved file.
```

---

## QBO Navigation

### Navigate to a QBO Page (Direct URL)

```
Tool: browser_navigate
Parameters:
  url: "https://app.qbo.intuit.com/app/reportlist"
```

Common QBO URLs:

| Page | URL |
|------|-----|
| Reports | `/app/reportlist` |
| Chart of Accounts | `/app/chartofaccounts?jobId=accounting` |
| COA Templates | `/app/accounting/accounts-templates` |
| Business Overview | `/app/homepage` |
| Invoices | `/app/invoices` |
| Expenses | `/app/expenses` |
| Banking | `/app/banking` |
| Sales Tax | `/app/salestax` |
| Payroll | `/app/payroll` |
| Projects | `/app/projects` |
| Budgets | `/app/budgets` |
| Recurring Transactions | `/app/recurringtransactions` |
| Custom Fields | `/app/customfields` |
| Rules | `/app/rules` |

**Note:** The Chart of Accounts URL uses `chartofaccounts` (no hyphens), NOT `chart-of-accounts`.

### Handle Page Timeout / Freeze

QBO pages (especially Business Feed) can freeze on load. Use a try-catch with reload fallback.

```javascript
// Tool: browser_run_code
async (page) => {
  try {
    await page.goto('https://app.qbo.intuit.com/app/homepage', {
      timeout: 60000,
      waitUntil: 'domcontentloaded'
    });
  } catch (e) {
    // Timeout - try reload
    await page.reload({ timeout: 30000 });
    await page.waitForTimeout(3000);
  }
}
```

### Dismiss Tour/Tooltip Overlays

QBO frequently shows "What's New" tours or tooltip overlays on first visit to a page. Dismiss them before taking screenshots or interacting.

```javascript
// Tool: browser_run_code
async (page) => {
  // Try "Dismiss" button first
  const dismissBtn = page.locator('button:has-text("Dismiss")');
  if (await dismissBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
    await dismissBtn.click();
    await page.waitForTimeout(500);
  }

  // Try close (X) button on tooltips
  const closeBtn = page.locator('[aria-label="Close"]');
  if (await closeBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
    await closeBtn.click();
    await page.waitForTimeout(500);
  }

  // Try "Got it" button (common on feature tours)
  const gotItBtn = page.locator('button:has-text("Got it")');
  if (await gotItBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
    await gotItBtn.click();
    await page.waitForTimeout(500);
  }
}
```

### Company Switcher (Multi-Entity)

```javascript
// Tool: browser_run_code
async (page) => {
  // Click entity/company name in top-right header
  // (Use snapshot to find the exact ref for the company name)
  // Select target entity from dropdown
  // Wait for full context switch - QBO reloads the entire app
  await page.waitForTimeout(5000);
}
```

### Wait for QBO Page Content to Load

```javascript
// Tool: browser_run_code
async (page) => {
  // Wait for the loading spinner to disappear
  await page.waitForSelector('.loading-spinner', { state: 'hidden', timeout: 30000 })
    .catch(() => {});  // Ignore if spinner was never shown

  // Alternative: wait for a known element to appear
  await page.waitForSelector('[data-testid="report-table"]', { timeout: 30000 })
    .catch(() => {});
}
```

---

## Complete UAT Workflow Example

A typical UAT feature validation follows this sequence:

```
1. Navigate to QBO feature page          -> browser_navigate
2. Dismiss any overlays/tours            -> browser_run_code
3. Take evidence screenshots             -> browser_take_screenshot (x N)
4. Upload screenshots to Drive folder    -> browser_navigate + browser_run_code
5. Extract file IDs from Drive           -> browser_run_code (scroll + extract)
6. Navigate to UAT Google Sheet          -> browser_navigate
7. Update status cell (e.g., E29)        -> browser_run_code (Name Box + type)
8. Update evidence cell (e.g., G29)      -> browser_run_code (multi-line + hyperlinks)
```

### Typical Cell Values

| Column | Purpose | Example Value |
|--------|---------|---------------|
| E | Status | `VALIDATED`, `BLOCKED`, `NOT TESTABLE` |
| G | Evidence filenames (hyperlinked) | `02_ID16_01_overview.jpeg` (linked to Drive) |

---

## Tips and Gotchas

### Timing

1. **QBO page load timeout**: Use 60s for initial load, 30s for subsequent navigations.
2. **Ctrl+Enter timing**: Always add **400ms+ delay** between lines in Google Sheets, or they concatenate into one line.
3. **Ctrl+K dialog**: Wait **800ms** after pressing Ctrl+K before interacting with the Link combobox.
4. **Drive upload**: Wait **1000ms** after clicking "New" before clicking "File upload".
5. **Entity switch**: Wait **5000ms** after switching companies in QBO for full reload.

### Google Sheets

6. **Name Box over snapshot refs**: Always use `#t-name-box` for cell navigation. Snapshot element refs change on every snapshot and are unreliable for repeated operations.
7. **Escape over Enter**: After adding hyperlinks in a cell, press **Escape** (not Enter) to preserve formatting. Enter may break hyperlink formatting.
8. **Hyperlink batches of 7**: When adding many hyperlinks in one cell, split into groups of **7 max**. More than 7 sequential Ctrl+K operations can cause the last link to fail.
9. **Snapshot size**: Google Sheets snapshots frequently exceed 90K characters. Save to a file with `filename` parameter and search with Grep instead of reading inline.

### Google Drive

10. **Lazy loading**: Drive only loads visible files. You must scroll **30 iterations with 500ms delays** to load all files in a large folder.
11. **New button selector**: Use `[guidedhelpid="new_menu_button"]` to find the "New" button reliably.
12. **File upload menu**: The "File upload" option is a `[role="menuitem"]` element. Filter by text content.

### QBO

13. **URL format**: Chart of Accounts is `/app/chartofaccounts?jobId=accounting` (no hyphens). COA Templates is `/app/accounting/accounts-templates`.
14. **Tour dismissal**: Always check for and dismiss overlay tours before interacting with a page or taking screenshots.
15. **Business Feed freeze**: The Business Feed / Homepage is prone to freezing. Always wrap navigation in try-catch with a reload fallback.

### File Upload (General)

16. **GEM-specific**: GEM's referral form file upload requires `page.locator('input[type="file"]').first().setInputFiles()` via `browser_run_code`, not the `browser_file_upload` MCP tool. GEM only accepts PDF/DOC/DOCX (not .txt).
17. **Drive upload**: Use the `waitForEvent('filechooser')` pattern inside `browser_run_code` for Drive uploads.

---

## Quick Reference: MCP Tool to Pattern Mapping

| MCP Tool | When to Use |
|----------|-------------|
| `browser_navigate` | Go to QBO page, Drive folder, or Sheets URL |
| `browser_snapshot` | Read page structure, find element refs. Save to file for large pages |
| `browser_take_screenshot` | Capture evidence (JPEG, named per convention) |
| `browser_click` | Click buttons/links using refs from snapshot |
| `browser_type` | Type into input fields using refs from snapshot |
| `browser_press_key` | Keyboard shortcuts (F2, Ctrl+K, Ctrl+Enter, Escape) |
| `browser_run_code` | Complex multi-step operations (Drive upload, Sheets multi-line, scrolling) |
| `browser_evaluate` | Read DOM values, extract data, run JS expressions |
| `browser_wait_for` | Wait for text to appear/disappear |
| `browser_file_upload` | Simple file uploads (not GEM, not Drive -- use `browser_run_code` for those) |
| `browser_fill_form` | Fill multiple form fields at once |
| `browser_select_option` | Select dropdown options |
