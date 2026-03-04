# Google Drive Automation Patterns

## Upload Files to Drive Folder

### Step 1: Navigate to Target Folder
```javascript
await page.goto('https://drive.google.com/drive/folders/FOLDER_ID');
await page.waitForTimeout(3000);  // Wait for folder to load
```

### Step 2: Click "New" Button
```javascript
// The "New" button has a specific guidedhelpid attribute
await page.locator('[guidedhelpid="new_menu_button"]').click();
await page.waitForTimeout(1000);
```

### Step 3: Click "File Upload"
```javascript
// Find the visible menu item with text "File upload"
const menuItems = page.locator('[role="menuitem"]');
await menuItems.filter({ hasText: 'File upload' }).click();
```

### Step 4: Handle File Chooser
```javascript
const [fileChooser] = await Promise.all([
  page.waitForEvent('filechooser'),
  // Dialog opens automatically after clicking "File upload"
]);
await fileChooser.setInputFiles('/path/to/screenshot.jpeg');
await page.waitForTimeout(3000);  // Wait for upload to complete
```

### Upload Multiple Files
For batch uploads, repeat the New > File upload > setInputFiles sequence for each file. Wait 3-5 seconds between uploads for Drive to process.

## Extract File IDs

### Why DOM Extraction?
Google Drive API via direct fetch returns 403 PERMISSION_DENIED in browser context. The DOM has all file metadata via `[data-id]` attributes.

### Handle Lazy Loading First
Drive only renders ~50 files at a time. Must scroll ALL scrollable containers before extraction:

```javascript
// Run via browser_run_code
for (let i = 0; i < 30; i++) {
  document.querySelectorAll('*').forEach(el => {
    if (el.scrollHeight > el.clientHeight + 100) {
      el.scrollTop = el.scrollHeight;
    }
  });
  await new Promise(r => setTimeout(r, 500));
}
```

### Extract IDs and Filenames
```javascript
const result = [];
const seen = new Set();
document.querySelectorAll('[data-id]').forEach(el => {
  const id = el.getAttribute('data-id');
  if (!id || seen.has(id)) return;
  seen.add(id);
  const strongEl = el.querySelector('strong');
  const name = strongEl ? strongEl.textContent.trim() : '';
  if (name && (
    name.endsWith('.png') ||
    name.endsWith('.jpeg') ||
    name.endsWith('.jpg') ||
    name.endsWith('.txt') ||
    name.endsWith('.xlsx')
  )) {
    result.push({ id, name });
  }
});
return JSON.stringify(result);
```

### Build File URLs
```
https://drive.google.com/file/d/{FILE_ID}/view
```

## Folder Structure Convention

For UAT evidence, use one Drive folder per release cycle:
```
WINTER_RELEASE_EVIDENCE/
├── 02_ID16_01_kpi_scorecard_overview.jpeg
├── 02_ID16_02_kpi_manage_library.jpeg
├── 03_ID17_01_dashboards_overview.jpeg
├── ...
└── 31_ID15_05_chart_of_accounts.jpeg
```

File naming: `{row:02d}_ID{feature_id:02d}_{seq:02d}_{description}.jpeg`

## Tips

1. **Lazy loading is critical**: Without scrolling 30 iterations, you'll only get ~50 files
2. **500ms delay between scroll iterations**: Drive needs time to load new content
3. **data-id is the source of truth**: Don't try to parse URLs from the page, use `[data-id]` attributes
4. **strong element has filename**: The filename is inside a `<strong>` element within the `[data-id]` container
5. **Upload wait time**: 3-5 seconds per file upload. Large files (>5MB) may need longer
6. **Folder ID from URL**: `https://drive.google.com/drive/folders/{FOLDER_ID}` - the last segment is the ID
