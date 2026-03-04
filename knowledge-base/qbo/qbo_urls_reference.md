# QBO / IES URL Map

> Discovered during Winter Release FY26 UAT (Feb 2026). Updated as new routes are found.

## Core Routes

| Area | URL Path | Status |
|------|----------|--------|
| Home / Business Feed | `/app/homepage` | Confirmed |
| Chart of Accounts | `/app/chartofaccounts?jobId=accounting` | Confirmed |
| COA Templates | `/app/accounting/accounts-templates?jobId=accounting` | Confirmed |
| Standard Reports | `/app/reportlist` | Confirmed |
| KPI Scorecard | `/app/kpis` | Confirmed |
| Dashboards | `/app/dashboards` | Confirmed |
| Management Reports | `/app/management-reports` | Confirmed |
| Bank Transactions | `/app/banking` | Confirmed |
| Products & Services | `/app/items` | Confirmed |
| Projects | `/app/projects` | Confirmed |
| Workflows | `/app/workflows` | Confirmed |
| Estimates | `/app/estimates` | Confirmed |
| Sales Orders | `/app/salesorders` | Confirmed |
| Invoices | `/app/invoices` | Confirmed |
| Bills | `/app/bills` | Confirmed |
| Purchase Orders | `/app/purchaseorders` | Confirmed |
| Vendors | `/app/vendors` | Confirmed |
| Customers | `/app/customers` | Confirmed |
| Employees | `/app/employees` | Confirmed |
| Payroll | `/app/payroll` | Confirmed |
| Time Tracking | `/app/time` | Confirmed |
| Time Settings | `/app/timesettings` | Confirmed |
| Sales Tax | `/app/salestax` | Confirmed |
| Fixed Assets | `/app/fixedassets` | Confirmed |
| Dimensions | `/app/dimensions` | Confirmed |
| Account & Settings | `/app/settings` | Confirmed |
| Audit Log | `/app/auditlog` | Confirmed |

## Multi-Entity Routes

| Area | URL Path | Notes |
|------|----------|-------|
| Consolidated View | Via entity switcher | No direct URL, switch context |
| Consolidated Reports | Standard Reports section | Within /app/reportlist in CV mode |
| Employee Hub (ME) | Workforce > Employee Hub | Feature flag required |
| Entity Rename | Settings > Account and settings > Company name | Must be done from each entity |

### Entity Switcher Order
- Consolidated View (fixed, always first)
- Parent entity (fixed, always second)
- Child entities (alphabetical by name)
- **No native reorder UI** - use numeric prefixes in names to control order (e.g., "01 - Entity Name")

## Known Incorrect URLs

| Wrong URL | Error | Correct URL |
|-----------|-------|-------------|
| `/app/chart-of-accounts` | 404 | `/app/chartofaccounts?jobId=accounting` |
| `/app/coa-templates` | 404 | `/app/accounting/accounts-templates?jobId=accounting` |

## URL Construction Rules

1. **Base URL**: `https://app.qbo.intuit.com`
2. **All routes start with**: `/app/`
3. **Accounting pages need**: `?jobId=accounting` suffix
4. **No hyphens in legacy routes**: `chartofaccounts` not `chart-of-accounts`
5. **Settings sub-pages**: `/app/settings` then navigate via UI

## TestBox-Specific URLs

| Area | URL Pattern |
|------|-------------|
| TestBox Login | `https://app.testbox.com/` |
| QBO via TestBox | Redirects to `app.qbo.intuit.com` |
| Start Demo | Via TestBox dashboard |

## Feature-Specific Deep Links

| Feature | Deep Link | Notes |
|---------|-----------|-------|
| KPI Manage | Reports > KPIs > Manage KPIs | No direct URL |
| Create KPI | Reports > KPIs > Manage KPIs > Create | No direct URL |
| Dimension Assignment | Settings > Dimensions > dropdown | No direct URL |
| Cost Group Management | Products & Services > More > Manage | No direct URL |
| Workflow Builder | Workflows > + Custom workflow | No direct URL |
| Project Budget | Projects > [Project] > Budget | No direct URL |
| Progress Invoicing | Account & Settings > Sales | Toggle setting |

## Last Updated
2026-02-14 (Winter Release FY26 UAT Complete)
