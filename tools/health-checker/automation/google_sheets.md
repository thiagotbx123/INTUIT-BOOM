# Google Sheets Automation Patterns

## Cell Navigation

### Name Box (Preferred Method)
```javascript
// Always use #t-name-box instead of snapshot refs (refs change between sessions)
const nameBox = page.locator('#t-name-box');
await nameBox.click();
await nameBox.fill('E29');  // Cell reference
await page.keyboard.press('Enter');
await page.waitForTimeout(500);
```

### Find Feature Row (Ctrl+F)
```javascript
// When row number is uncertain, search by feature name
await page.keyboard.press('Control+f');
await page.waitForTimeout(500);
await page.keyboard.type('Cost Groups');
await page.keyboard.press('Enter');
await page.waitForTimeout(500);
await page.keyboard.press('Escape');  // Close find bar
```

## Cell Editing

### Simple Value Update
```javascript
// Navigate to cell first, then type
await page.keyboard.type('VALIDATED');
await page.keyboard.press('Enter');
await page.waitForTimeout(500);
```

### Multi-Line Cell Input
```javascript
// Enter edit mode
await page.keyboard.press('F2');

// Type lines with Ctrl+Enter between them
await page.keyboard.type('file1.png');
await page.keyboard.press('Control+Enter');
await page.waitForTimeout(400);  // CRITICAL: 400ms minimum delay
await page.keyboard.type('file2.png');
await page.keyboard.press('Control+Enter');
await page.waitForTimeout(400);
await page.keyboard.type('file3.png');

// Confirm cell
await page.keyboard.press('Escape');  // Preserves formatting
await page.waitForTimeout(500);
```

**Why 400ms delay?** Without it, lines concatenate on the same line. Google Sheets needs time to process Ctrl+Enter before the next character input.

### Batch Approach for Many Lines
For cells with 10+ lines, split into batches of 7:
1. Type first 7 filenames with Ctrl+Enter between them
2. Confirm cell (Escape)
3. Re-enter cell (F2), go to end (Ctrl+End)
4. Continue with Ctrl+Enter + remaining filenames
5. Confirm cell (Escape)

## Hyperlinks

### Single Hyperlink (Ctrl+K)
```javascript
// 1. Select text in cell
await page.keyboard.press('F2');        // Edit mode
await page.keyboard.press('Home');      // Start of line
await page.keyboard.press('Shift+End'); // Select line

// 2. Insert link
await page.keyboard.press('Control+k');
await page.waitForTimeout(800);

// 3. Fill URL
const linkInput = page.getByRole('combobox', { name: 'Link' });
await linkInput.fill('https://drive.google.com/file/d/FILE_ID/view');
await page.waitForTimeout(500);

// 4. Apply
await page.getByRole('button', { name: 'Apply' }).click();
await page.waitForTimeout(500);
```

### Multiple Hyperlinks in One Cell
Each filename on its own line, each linked individually:

```javascript
// After typing all filenames (multi-line), re-enter edit mode
await page.keyboard.press('F2');
await page.keyboard.press('Control+Home');  // Go to very beginning

// For each line:
await page.keyboard.press('Home');
await page.keyboard.press('Shift+End');     // Select line
await page.keyboard.press('Control+k');      // Open link dialog
await page.waitForTimeout(800);
const linkInput = page.getByRole('combobox', { name: 'Link' });
await linkInput.fill(url);
await page.waitForTimeout(500);
await page.getByRole('button', { name: 'Apply' }).click();
await page.waitForTimeout(500);
// Move to next line
await page.keyboard.press('End');
await page.keyboard.press('ArrowRight');
// Repeat for next line...

// IMPORTANT: Use Escape to confirm cell (not Enter)
await page.keyboard.press('Escape');
```

**Batch limit**: Process max 7 hyperlinks per batch to avoid errors on the last link.

## xlsx vs Native Google Sheets

### Key Differences
| Aspect | Native (.gsheet) | xlsx (opened in Sheets) |
|--------|------------------|------------------------|
| Apps Script | Available (Extensions menu) | NOT available |
| RichTextValue API | Works | Not accessible |
| Copy-paste hyperlinks | Works (within same doc) | Ctrl+V pastes as IMAGE |
| Formulas | Full support | Full support |

### Workaround for xlsx Hyperlinks
Since Apps Script doesn't work on xlsx files, use the Ctrl+K method described above.

### If You Need Apps Script (Native Sheets Only)
```javascript
// RichTextValue for multiple hyperlinks in one cell
var rtv = SpreadsheetApp.newRichTextValue()
  .setText("file1.png\nfile2.png")
  .setLinkUrl(0, 9, "https://drive.google.com/file/d/FILE_ID_1/view")
  .setLinkUrl(10, 19, "https://drive.google.com/file/d/FILE_ID_2/view")
  .build();
sheet.getRange("H2").setRichTextValue(rtv);
```

- `setLinkUrl(startOffset, endOffset, url)` uses character positions
- Each filename on its own line (`\n` separator)

### Apps Script Authorization Flow
1. Click "Run" in Apps Script editor
2. "Authorization required" dialog > click "Review permissions"
3. Google account chooser > select account
4. "This app isn't verified" > click "Continue" (if shown)
5. Permission grant page > click "Allow"
6. Script executes automatically after authorization

## Tips

1. **Snapshot too large**: Google Sheets snapshots can exceed 90K chars. Save to file and use Grep to search
2. **Cross-document paste fails**: Ctrl+V between different Google Sheets docs pastes cells as IMAGE (not rich text). Use Apps Script or manual Ctrl+K instead
3. **Monaco editor (Apps Script)**: Use Monaco API to set code: `window.monaco.editor.getEditors()[0].executeEdits(...)` - avoids auto-indent issues
4. **HTML clipboard paste fails**: Google Sheets strips `<a>` tags from HTML clipboard
5. **Blob context**: Clipboard API with `Blob` must run inside `page.evaluate()` (browser context)
6. **Auth consent**: Clicking "Continue" on OAuth consent may close the tab but authorization still succeeds
7. **Never overwrite existing data**: Always check cell contents before writing. Use Ctrl+Z (up to 50x) if needed
