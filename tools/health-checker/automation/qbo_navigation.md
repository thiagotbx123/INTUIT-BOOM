# QBO / IES Navigation Patterns

## URL Map

### Correct URL Patterns
| Area | Correct URL | Notes |
|------|------------|-------|
| Chart of Accounts | `/app/chartofaccounts?jobId=accounting` | NO hyphen, needs jobId |
| COA Templates | `/app/accounting/accounts-templates?jobId=accounting` | Separate page from COA |
| Reports | `/app/reportlist` | Standard reports list |
| KPIs | `/app/kpis` | KPI Scorecard |
| Dashboards | `/app/dashboards` | Dashboard list |
| Management Reports | `/app/management-reports` | Management report builder |
| Business Feed | `/app/homepage` | Dashboard with feed cards |
| Bank Transactions | `/app/banking` | Bank reconciliation |
| Products & Services | `/app/items` | Product/service list |
| Projects | `/app/projects` | Project list |
| Workflows | `/app/workflows` | Workflow automation |
| Estimates | `/app/estimates` | Estimate list |
| Sales Orders | `/app/salesorders` | Sales order list |
| Invoices | `/app/invoices` | Invoice list |
| Vendors | `/app/vendors` | Vendor list |
| Customers | `/app/customers` | Customer list |
| Employees | `/app/employees` | Employee list |
| Payroll | `/app/payroll` | Payroll overview |
| Time | `/app/time` | Time tracking |
| Taxes | `/app/salestax` | Sales tax center |
| Fixed Assets | `/app/fixedassets` | Fixed asset manager |
| Dimensions | `/app/dimensions` | Dimension settings |

### Known INCORRECT URLs (404)
| Wrong | Correct |
|-------|---------|
| `/app/chart-of-accounts` | `/app/chartofaccounts?jobId=accounting` |
| `/app/coa-templates` | `/app/accounting/accounts-templates?jobId=accounting` |

### URL Suffixes
- `?jobId=accounting` - Required for accounting-related pages
- `/app/` prefix - All QBO routes start with this

## Multi-Entity Navigation

### Entity Switcher
```
Click company name in top nav bar → dropdown appears with:
1. Search... (search box)
2. Consolidated View (always first)
3. Parent entity (always second, with checkmark for current)
4. Child entities (alphabetical order)
```

### Entity Order in Switcher
The entity list order is:
- **Consolidated View** → always first (fixed)
- **Parent entity** → always second (fixed)
- **Child entities** → **alphabetical by company name**

**To reorder child entities**, rename them with numeric prefixes:
- `01 - Keystone Terra` (appears first)
- `02 - Keystone BlueCraft` (appears second)
- `03 - KeyStone Canopy` (appears third)

**How to rename**: Settings (gear) > Account and settings > Company name (must do from EACH entity)

**No native reorder**: QBO does NOT have drag-and-drop or manual ordering for entities in the switcher. Renaming is the only method.

### Entity Context
When switching entities, the entire page reloads with the new company context. Wait 5 seconds after switching.

```javascript
// After entity switch
await page.waitForTimeout(5000);
// Verify correct entity loaded by checking header/title
```

### Consolidated Reports
```
Consolidated View > Reports > Standard Reports > Consolidated Reports section
```
Located in a separate section within Standard Reports, below single-entity reports.

## Page Load Patterns

### Standard Navigation
```javascript
await page.goto('https://app.qbo.intuit.com/app/reportlist', {
  timeout: 30000,
  waitUntil: 'domcontentloaded'
});
await page.waitForTimeout(2000);  // Allow dynamic content to load
```

### Timeout Recovery
QBO pages can freeze, especially Business Feed. Recovery pattern:
```javascript
try {
  await page.goto(url, { timeout: 60000 });
} catch (e) {
  // Page timed out - reload
  await page.reload({ timeout: 30000 });
  await page.waitForTimeout(3000);
}
```

### Tour/Tooltip Dismissal
QBO shows "What's New" tours on first visit to features:
```javascript
// Try to dismiss tour overlay
const dismissBtn = page.locator('button:has-text("Dismiss")');
if (await dismissBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
  await dismissBtn.click();
  await page.waitForTimeout(500);
}

// Close tooltip X button
const closeBtn = page.locator('[aria-label="Close"]');
if (await closeBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
  await closeBtn.click();
}
```

## Left Nav Structure (IES)

```
Home (Business Feed)
├── Accounting
│   ├── Bank Transactions
│   ├── Chart of Accounts
│   └── Fixed Assets
├── Sales & Get Paid
│   ├── Invoices
│   ├── Estimates
│   ├── Sales Orders
│   ├── Products & Services
│   └── Customers
├── Spend & Track
│   ├── Bills
│   ├── Purchase Orders
│   └── Vendors
├── Projects
├── Inventory
├── Reports
│   ├── Standard Reports
│   ├── Management Reports
│   ├── KPIs
│   └── Dashboards
├── Workforce
│   ├── Employees
│   ├── Payroll
│   └── Time
├── Taxes
│   └── Sales Tax
└── Settings (gear icon)
    ├── Account & Settings
    ├── Dimensions
    ├── Manage Workflows
    └── Platform Customization
```

## Business Feed Filter Categories
The Business Feed has AI-powered category filters:
- All (shows all cards)
- Accounting
- Expenses
- Sales
- Customers
- Projects
- Payroll

Card types include: Finance Agent summaries, Project Management Agent suggestions, Leads, Dimension assignment prompts.

## Tips

1. **Always use `?jobId=accounting`** for accounting pages - without it you may get 404
2. **Business Feed timeout**: This page is heavy - use 60s timeout minimum
3. **Entity switch = full reload**: Wait 5s after switching entities before interacting
4. **Left nav may collapse**: Click hamburger menu if nav items aren't visible
5. **Feature flags**: Some features are behind flags that Intuit must enable server-side
6. **Post-migration features**: Solutions Specialist and DFY Migration require actual QBDT migration, not available in TestBox
7. **TestBox limitations**: No real payroll processing, no email integration, no QBDT migration path
8. **Entity order**: Child entities appear alphabetically in switcher - rename with prefixes (01-, 02-) to control order
9. **Entity rename**: Must switch TO each entity first, then Settings > Account and settings > Company name
