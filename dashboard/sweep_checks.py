"""All 57 sweep checks + content safety + fix rules — single source of truth."""

DEEP_STATIONS = [
    {
        "id": "D01",
        "name": "Dashboard & First Impression",
        "category": "Financial Health",
        "tier": "deep",
        "route": "/app/homepage",
        "description": "Homepage loads clean, widgets populated, correct company in header, no placeholders",
        "what_to_check": [
            "Company name correct in header",
            "P&L widget: Income, Expenses, Net Income",
            "Bank balance widget",
            "Invoices: unpaid/overdue/paid counts",
            "Cash flow widget",
            "Business Feed tiles (action items, overdue, monthly summary)",
            "No placeholder text (TBX, Lorem, Sample)",
        ],
        "drill_in": [
            "Click P&L widget to verify it drills into actual P&L report",
            "Click Invoices widget to verify invoice list has data",
            "Check Business Feed: are action items realistic? (overdue invoices, pending approvals)",
        ],
        "auto_fix": True,
        "fix_actions": ["Change date period if widgets empty", "Note placeholder origin"],
    },
    {
        "id": "D02",
        "name": "Profit & Loss (P&L)",
        "category": "Financial Health",
        "tier": "deep",
        "route": "/app/standardreports > Profit and Loss (IES: navigate sidebar, click P&L link)",
        "description": "Revenue, COGS, Expenses, Net Income must be POSITIVE. Margins within industry range",
        "what_to_check": [
            "Net Income POSITIVE (mandatory all entities)",
            "Margin within range: Construction 3-15%, Tire 25-35%, Prof Services 20-40%, NP 2-10%, Manufacturing 15-25%",
            "No placeholder category names",
            "Revenue not $0",
            "Report period correct (not blank)",
        ],
        "drill_in": [
            "Click into top revenue category to verify it has multiple income sources (not 1 mega-invoice)",
            "Click into top expense category to verify diverse vendors/payees",
            "Check if COGS exists and is proportional (not $0 if inventory products exist)",
        ],
        "auto_fix": True,
        "fix_actions": [
            "Create JE: DR AR / CR Sales/Revenue to make net income positive",
            "Change report period to All Dates if blank",
            "Rename placeholder categories in COA",
        ],
    },
    {
        "id": "D03",
        "name": "Balance Sheet",
        "category": "Financial Health",
        "tier": "deep",
        "route": "/app/standardreports > Balance Sheet (IES: navigate sidebar, click BS link, use EXTRATOR 6)",
        "description": "Assets = Liabilities + Equity. Values proportional to business, no absurd amounts",
        "what_to_check": [
            "Accounting equation balances (A = L + E)",
            "No absurd values ($20B AR, $148M checking, negative bank)",
            "AR/AP not zeroed when invoices/bills exist",
            "Cash & bank breakdown per account",
            "Fixed Assets (check for negative)",
        ],
        "auto_fix": False,
        "fix_actions": ["Report anomalies to user", "Investigate via COA"],
    },
    {
        "id": "D04",
        "name": "Banking & Reconciliation",
        "category": "Banking",
        "tier": "deep",
        "route": "/app/banking",
        "description": "Bank accounts visible, mix of categorized/uncategorized, connections active, QB vs Bank balance check",
        "what_to_check": [
            "Bank accounts visible with transactions",
            "Mix of categorized + uncategorized (realistic)",
            "Bank feed connection status (active, not Error 103)",
            "QB vs Bank balance discrepancy (flag >10x difference)",
            "Pending transaction count",
            "QBAA (QuickBooks Accounting Agent) presence",
            "Guardian Growth MMA balance (known $10.9M inflation)",
        ],
        "drill_in": [
            "Click into each bank account tab to see transaction list",
            "Review recent 10 transactions: are descriptions varied or all identical?",
            "Check if bank rules already exist (Rules tab) and if they make sense",
        ],
        "enrichment": [
            "Categorize 5-10 uncategorized txns with VARIED categories (not all same expense account)",
            "Create 2-3 bank rules for TOP recurring vendors (use vendor names from D06)",
            "Ensure categorized txns include mix: payroll, rent, supplies, utilities, vendor payments",
        ],
        "auto_fix": True,
        "fix_actions": [
            "Categorize first 5-10 uncategorized transactions",
            "Create 2-3 bank rules for recurring vendors",
        ],
    },
    {
        "id": "D05",
        "name": "Customers & Invoices (AR)",
        "category": "Data Quality",
        "tier": "deep",
        "route": "/app/customers + /app/invoices",
        "description": "Customer names realistic, top 5 enriched (company, email, address, terms, notes), invoices exist",
        "what_to_check": [
            "Top 5 customers have: company name, email, address, phone, notes, terms",
            "No placeholder names (TBX, Test, 12345, TESTER, IDT)",
            "No duplicate names with numeric suffix (Name2)",
            "Invoices exist with values",
            "Customer Hub status (Leads, Proposals, Contracts)",
            "Extreme balance customers (>$1B AR)",
            "Overdue invoice count/value",
        ],
        "drill_in": [
            "Click into top 3-5 customers to open detail page",
            "On each detail: check company, email, address, phone, notes, terms, transaction history",
            "Assess: does this customer feel real? Would a prospect believe this is a real client?",
            "Check invoices tab: are there varied amounts, dates, and products? Or all $1000 same date?",
        ],
        "enrichment": [
            "Fill notes with BUSINESS CONTEXT (not generic). Examples by sector in ENRIQUECER section below",
            "Vary terms across customers: top clients=Net 45/60, medium=Net 30, small=Net 15/Due on Receipt",
            "Add phone with LOCAL area code matching the company's state/region",
            "Ensure at least 3 customers have complete profile (all 6 fields filled)",
        ],
        "auto_fix": True,
        "fix_actions": [
            "Fill empty company name, email, address, notes, terms",
            "Rename placeholder names with realistic sector names",
            "Select Net 30 for empty terms",
            "Add context notes (Fleet account, Main supplier, etc)",
        ],
    },
    {
        "id": "D06",
        "name": "Vendors & Bills (AP)",
        "category": "Data Quality",
        "tier": "deep",
        "route": "/app/vendors + /app/bills",
        "description": "Vendor names realistic, top 5 enriched, AP aging distribution, overdue analysis",
        "what_to_check": [
            "Top 5 vendors have: name, email, address, terms, notes",
            "No TBX/Test/Placeholder names",
            "AP aging distribution (Current, 1-30, 31-60, 61-90, 91+)",
            "Not 80%+ AP in 91+ day bucket",
            "AP total not absurdly high vs Revenue",
            "No bills overdue 2+ years (stale data)",
            "No single vendor >50% of AP",
        ],
        "drill_in": [
            "Click into top 3-5 vendors to open detail page",
            "On each detail: check name, email, address, terms, notes, bill history",
            "Assess supply chain realism: do these vendors make sense for this type of business?",
            "Check AP Aging report: is aging distribution realistic or all piled in 91+ days?",
        ],
        "enrichment": [
            "Fill notes with RELATIONSHIP CONTEXT. Examples by sector in ENRIQUECER section below",
            "Vary terms: strategic suppliers=Net 60, regular=Net 30/45, utilities=Due on Receipt",
            "Ensure vendor names form a coherent supply chain for the sector (not random companies)",
            "NEVER create bills to enrich (increases COGS, risks negativizing P&L)",
        ],
        "auto_fix": True,
        "fix_actions": [
            "Edit vendor names, fill email/address/terms/notes",
            "DO NOT create bills (increases COGS, can negativize P&L)",
        ],
    },
    {
        "id": "D07",
        "name": "Employees & Payroll",
        "category": "Workforce",
        "tier": "deep",
        "route": "/app/employees + /app/payroll",
        "description": "Employees exist with realistic names, payroll history, multi-state, tax compliance",
        "what_to_check": [
            "Employee list (names, titles, pay rates)",
            "Payroll has history or documented absence",
            "Multi-state payroll status",
            "Tax penalty protection status",
            "Workers comp notices",
            "TO DO items (overdue filings, new hire reports)",
            "No placeholder employee names",
        ],
        "auto_fix": False,
        "fix_actions": [
            "TRY to edit placeholder names (may require 2FA)",
            "If 2FA blocks: STOP, annotate and advance",
            "NEVER insist on employee edits — most protected area",
        ],
    },
    {
        "id": "D08",
        "name": "Products, Services & Inventory",
        "category": "Data Quality",
        "tier": "deep",
        "route": "/app/items",
        "description": "Product names realistic, prices set, cost < price (positive margin), no spam/test products",
        "what_to_check": [
            "Top products have realistic names",
            "Prices not $0",
            "Cost not > Price (negative margin)",
            "Correct category type (Service vs Inventory vs Non-inventory)",
            "No spam products (70+ char names, nonsense)",
            "No TBX/Test/Sample placeholder names",
        ],
        "drill_in": [
            "Click into top 5 products to see detail (price, cost, description, income account)",
            "Check: does the product have a DESCRIPTION? Empty description = poor demo",
            "Check: is there a SKU or category that connects this product to the business narrative?",
        ],
        "enrichment": [
            "Add short description to top products (2-3 sentences about the product/service)",
            "Ensure price is realistic for sector (not $1 for a consulting engagement or $100K for a bolt)",
            "Products should tell the business story: what does this company SELL? Each product reinforces that",
        ],
        "auto_fix": True,
        "fix_actions": [
            "Rename placeholder names with sector-appropriate names",
            "Set realistic prices where $0",
            "Swap price/cost if inverted",
        ],
    },
    {
        "id": "D09",
        "name": "Projects & Job Costing",
        "category": "Demo Realism",
        "tier": "deep",
        "route": "/app/projects",
        "description": "Minimum 3 projects, realistic names, transactions attached, status variety, profitability",
        "what_to_check": [
            "3+ projects exist",
            "Realistic names (not 'Project 1', 'Test', 'IDT TEST')",
            "Projects have transactions attached",
            "Status variety (In Progress, Completed, Not Started)",
            "Profitability data (not 100% margin / extreme negative)",
            "Project-customer mapping",
        ],
        "drill_in": [
            "Click into each project to check: transactions list, profitability, customer assignment",
            "Assess: can you tell the STORY of this project? Budget vs actual, timeline, client?",
            "Check if project has invoices AND expenses (both sides of profitability)",
        ],
        "enrichment": [
            "Each project should have a customer assigned (not orphan)",
            "Project names should reference real-world work for the sector (see names below)",
            "Create projects if <3, with varied status: 1 In Progress, 1 Completed, 1 Not Started",
            "If project has $0 profitability data, associate existing invoices/expenses to it",
        ],
        "auto_fix": True,
        "fix_actions": [
            "Rename generic names with realistic sector names",
            "Create new projects if <3",
            "Vary status across projects",
        ],
    },
    {
        "id": "D10",
        "name": "Reports Advanced & BI",
        "category": "Feature Availability",
        "tier": "deep",
        "route": "/app/reportlist + /app/business-intelligence/kpi-scorecard",
        "description": "Reports load with data, KPI Scorecard available, Report Builder functional",
        "what_to_check": [
            "Main reports show data (P&L, BS, AR Aging, AP Aging)",
            "KPI Scorecard accessible (or feature flag OFF)",
            "Report Builder functional",
            "Reports not zeroed",
        ],
        "auto_fix": True,
        "fix_actions": [
            "Change period to All Dates if zeroed",
            "Annotate KPI 404 as BLOCKED (no fix)",
        ],
    },
    {
        "id": "D11",
        "name": "Chart of Accounts (COA)",
        "category": "Entity Config",
        "tier": "deep",
        "route": "/app/chartofaccounts?jobId=accounting",
        "description": "Complete account hierarchy, appropriate subtypes for sector, no placeholders/duplicates",
        "what_to_check": [
            "Complete hierarchy (Assets, Liabilities, Equity, Revenue, COGS, Expenses)",
            "Total account count",
            "Subtypes appropriate for sector",
            "No placeholder names ('Account 1', 'Test Account')",
            "No duplicate accounts",
            "NP: Unrestricted/Restricted Net Assets, Grant Revenue, Donations, FASB expenses",
        ],
        "auto_fix": True,
        "fix_actions": ["Rename placeholder accounts", "Annotate missing hierarchy"],
    },
    {
        "id": "D12",
        "name": "Settings — Company Info",
        "category": "Entity Config",
        "tier": "deep",
        "route": "/app/settings?panel=company",
        "description": "Legal Name, DBA, Industry, Address, Phone, EIN, Fiscal Year, Tax Form, i18n keys",
        "what_to_check": [
            "Industry correct (not 'other')",
            "Address not empty or placeholder",
            "Phone not empty or malformed",
            "Legal name vs DBA consistent",
            "EIN present",
            "No raw i18n keys displayed",
            "ZIP code matches city/state",
            "Legal name not swapped between entities",
        ],
        "auto_fix": False,
        "fix_actions": [
            "DO NOT correct settings automatically",
            "ONLY register problems found",
            "Report to user as pending",
        ],
    },
]

SURFACE_SCAN = [
    {
        "id": "S01",
        "name": "Estimates",
        "route": "/app/estimates",
        "description": "Page loads, has data, names realistic",
    },
    {"id": "S02", "name": "Sales Orders", "route": "/app/salesorders", "description": "Page exists, has data"},
    {
        "id": "S03",
        "name": "Purchase Orders",
        "route": "/app/purchaseorders",
        "description": "Page exists, has data, PO count",
    },
    {"id": "S04", "name": "Expenses", "route": "/app/expenses", "description": "Has expenses registered, entry count"},
    {
        "id": "S05",
        "name": "Recurring Transactions",
        "route": "/app/recurring",
        "description": "Recurrences configured, entry count",
    },
    {
        "id": "S06",
        "name": "Fixed Assets",
        "route": "/app/fixedassets",
        "description": "Module exists, has assets, asset count",
    },
    {
        "id": "S07",
        "name": "Revenue Recognition",
        "route": "/app/revenuerecognition",
        "description": "Module exists (Advanced only), entry count",
    },
    {
        "id": "S08",
        "name": "Time Tracking",
        "route": "/app/time",
        "description": "Module exists, has entries, entry count",
    },
    {
        "id": "S09",
        "name": "Sales Tax",
        "route": "/app/salestax",
        "description": "Configured, filing status, entry count",
    },
    {"id": "S10", "name": "Reconcile", "route": "/app/reconcile", "description": "Accounts reconciled, pending count"},
    {"id": "S11", "name": "Bank Rules", "route": "/app/banking > Rules tab", "description": "How many rules active"},
    {"id": "S12", "name": "Receipts", "route": "/app/receipts", "description": "Has receipts captured"},
    {"id": "S13", "name": "Budgets", "route": "/app/budgets", "description": "Has budgets (Construction relevant)"},
    {
        "id": "S14",
        "name": "Dimensions / Classes",
        "route": "/app/class",
        "description": "How many active, names appropriate",
    },
    {"id": "S15", "name": "Workflows", "route": "/app/workflows", "description": "Has automations configured"},
    {
        "id": "S16",
        "name": "Payment Links",
        "route": "/app/paymentlinks",
        "description": "Feature exists, loads without error",
    },
    {"id": "S17", "name": "Subscriptions", "route": "/app/subscriptions", "description": "Feature exists, has data"},
    {"id": "S18", "name": "My Accountant", "route": "/app/myaccountant", "description": "Accountant invite status"},
    {"id": "S19", "name": "Audit Log", "route": "/app/auditlog", "description": "Accessible, has activity"},
    {"id": "S20", "name": "Lending", "route": "Via menu", "description": "Feature visible in menu"},
    # v4.0 additions — Settings panels, forms, and missing modules
    {
        "id": "S21",
        "name": "Settings — Sales",
        "route": "/app/settings?panel=sales",
        "description": "Custom transaction numbers, service date, discount, deposit, tags, custom fields, automation",
    },
    {
        "id": "S22",
        "name": "Settings — Expenses",
        "route": "/app/settings?panel=expenses",
        "description": "PO, billable expenses, default markup, default bill payment terms",
    },
    {
        "id": "S23",
        "name": "Settings — Advanced",
        "route": "/app/settings?panel=advanced",
        "description": "Accounting (first month fiscal year, close books, tax form), currency, automation, projects, time tracking",
    },
    {
        "id": "S24",
        "name": "Quick Create (+New) Menu",
        "route": "+New button (global)",
        "description": "All form types render: Invoice, Estimate, Expense, Bill, PO, JE, Transfer, etc. No broken links",
    },
    {
        "id": "S25",
        "name": "Custom Form Styles",
        "route": "/app/customformstyles",
        "description": "Custom templates exist, logo uploaded, preview renders without error",
    },
    {
        "id": "S26",
        "name": "Tags",
        "route": "/app/tags",
        "description": "Tags feature enabled, has tags defined, tagged transactions exist",
    },
    {
        "id": "S27",
        "name": "Custom Fields",
        "route": "/app/customfields",
        "description": "Custom fields configured, visible on transaction forms",
    },
    {
        "id": "S28",
        "name": "Cash Flow Planner",
        "route": "/app/cashflow",
        "description": "Cash flow projection loads, chart renders, bank accounts linked",
    },
    {
        "id": "S29",
        "name": "Attachments",
        "route": "/app/attachments",
        "description": "Attachment center accessible, files attached to transactions exist",
    },
    {
        "id": "S30",
        "name": "Mileage",
        "route": "/app/mileage",
        "description": "Mileage tracking feature loads, trips logged or module accessible",
    },
]

CONDITIONAL_CHECKS = [
    # Multi-Entity
    {
        "id": "C01",
        "name": "Consolidated View",
        "condition": "multi_entity",
        "route": "Entity switcher > Consolidated",
        "description": "Functional access, data appears, dashboard metrics",
    },
    {
        "id": "C02",
        "name": "Shared COA",
        "condition": "multi_entity",
        "route": "/app/sharedcoa",
        "description": "Shared accounts between entities, 'Needs review' status",
    },
    {
        "id": "C03",
        "name": "IC Transactions",
        "condition": "multi_entity",
        "route": "/app/multi-entity-transactions?jobId=accounting",
        "description": "Intercompany transactions exist (JEs, allocations)",
    },
    {
        "id": "C04",
        "name": "Consolidated Reports",
        "condition": "multi_entity",
        "route": "/app/reportlist on Consolidated",
        "description": "Consolidated reports available with data, 17 expected types",
    },
    # Construction
    {
        "id": "C05",
        "name": "Project Phases",
        "condition": "construction",
        "route": "/app/projects > detail",
        "description": "Phases v2 configured on projects",
    },
    {
        "id": "C06",
        "name": "Cost Groups",
        "condition": "construction",
        "route": "Via Products",
        "description": "Cost groups defined for job costing",
    },
    {
        "id": "C07",
        "name": "AIA Billing",
        "condition": "construction",
        "route": "Via Projects",
        "description": "Lien waiver workflow present",
    },
    {
        "id": "C08",
        "name": "Certified Payroll",
        "condition": "construction",
        "route": "Via Payroll Reports",
        "description": "WH-347 report available",
    },
    # Non-Profit
    {
        "id": "C09",
        "name": "NP Terminology",
        "condition": "non_profit",
        "route": "All screens",
        "description": "Labels: Donors (not Customers), Pledges (not Invoices), Programs (not Products), Grants (not Projects)",
    },
    {
        "id": "C10",
        "name": "Statement of Activity",
        "condition": "non_profit",
        "route": "/app/reportlist",
        "description": "NP P&L equivalent loads with data",
    },
    {
        "id": "C11",
        "name": "NP Dimensions",
        "condition": "non_profit",
        "route": "/app/class",
        "description": "5+ active dimensions with NP-appropriate names",
    },
    # Advanced / IES
    {
        "id": "C12",
        "name": "Customer Hub",
        "condition": "advanced",
        "route": "/app/customers > Leads/Proposals",
        "description": "CRM advanced: Leads, Proposals, Contracts, Appointments, Reviews",
    },
    {
        "id": "C13",
        "name": "Intuit Intelligence",
        "condition": "advanced",
        "route": "Conversational BI in reports",
        "description": "Natural language queries function, AI chat button present",
    },
    {
        "id": "C14",
        "name": "Management Reports",
        "condition": "advanced",
        "route": "/app/managementreports",
        "description": "Customizable reports available",
    },
    # v4.0 additions
    {
        "id": "C15",
        "name": "Contractors / 1099",
        "condition": "construction",
        "route": "/app/contractors",
        "description": "Contractor list exists, 1099 tracking active, payments mapped",
    },
]

CONTENT_SAFETY = [
    {"id": "CS1", "name": "Profanity", "pattern": "Profanity words EN/PT", "severity": "CRITICAL"},
    {"id": "CS2", "name": "Placeholder Data", "pattern": r"\b(TBX|Lorem|Sample|Foo|Bar|TODO)\b", "severity": "P2"},
    {"id": "CS3", "name": "Test Names", "pattern": "Test, TESTER, explicit test markers", "severity": "P2"},
    {"id": "CS4", "name": "PII Exposure", "pattern": "SSN, credit card, @test emails", "severity": "CRITICAL"},
    {
        "id": "CS5",
        "name": "Cultural Gaffes",
        "pattern": "Sensitive names, political references",
        "severity": "CRITICAL",
    },
    {"id": "CS6", "name": "Duplicate Names", "pattern": "Names with numeric suffix (Name2)", "severity": "P2"},
    {"id": "CS7", "name": "Real Person Names", "pattern": "Real persons in financial contexts", "severity": "CRITICAL"},
    {"id": "CS8", "name": "Bilingual Gaffes", "pattern": "Mixed language, raw i18n keys", "severity": "P2"},
]

FIX_TIERS = {
    "fix_immediately": {
        "label": "Fix Immediately (no permission needed)",
        "items": [
            "Placeholder text (TBX, Test, Lorem, Sample, Foo)",
            "Duplicate names with suffix (Name2)",
            "Empty fields in top records (company, email, address, phone, notes, terms)",
            "Report wrong period -> All Dates",
            "Generic names (Project 1, Vendor A)",
            "Customer/vendor without terms -> Net 30",
            "Bank transactions uncategorized (top 5-10)",
        ],
    },
    "fix_and_report": {
        "label": "Fix but Report in Summary",
        "items": [
            "Create invoices (affects Revenue/AR)",
            "Create projects (impacts tracking)",
            "Create bank rules (impacts categorization)",
            "Rename products/services (may affect invoices)",
            "Adjust product prices (impacts margins)",
        ],
    },
    "never_fix": {
        "label": "NEVER Fix (Report to User)",
        "items": [
            "Direct PostgreSQL UPDATE/INSERT",
            "Employee edits blocked by 2FA",
            "Feature flags (depends on Intuit)",
            "Company settings (legal name, EIN, address)",
            "Payroll data (regulated)",
            "Deletes of any kind",
            "P&L negative due to inverted product cost",
        ],
    },
}

DEMO_REALISM_CRITERIA = [
    {"id": "DR01", "name": "Financial Viability", "description": "P&L makes sense? Positive net income?"},
    {"id": "DR02", "name": "Name Coherence", "description": "Customers, vendors, products match sector?"},
    {"id": "DR03", "name": "Data Volume", "description": "Looks like a real company with history?"},
    {"id": "DR04", "name": "Transaction Diversity", "description": "Not just 1 type of transaction?"},
    {"id": "DR05", "name": "Banking Health", "description": "Accounts connected, transactions categorized?"},
    {"id": "DR06", "name": "AR/AP Balance", "description": "Company has receivables AND payables?"},
    {"id": "DR07", "name": "Payroll Presence", "description": "Employees exist with salaries?"},
    {"id": "DR08", "name": "Projects Richness", "description": "Projects with transactions, not empty?"},
    {"id": "DR09", "name": "Report Quality", "description": "Reports generate useful data, not zeroed?"},
    {"id": "DR10", "name": "Storytelling Potential", "description": "Can tell a convincing business story?"},
]


def get_all_checks():
    """Return all checks in a flat list with tier info."""
    checks = []
    for c in DEEP_STATIONS:
        checks.append({**c, "tier": "deep", "enabled": True})
    for c in SURFACE_SCAN:
        checks.append(
            {
                **c,
                "tier": "surface",
                "category": "Surface Scan",
                "enabled": True,
                "what_to_check": [c["description"]],
                "auto_fix": False,
                "fix_actions": ["Navigate, wait 3s, evaluate page, annotate status"],
            }
        )
    for c in CONDITIONAL_CHECKS:
        checks.append(
            {
                **c,
                "tier": "conditional",
                "category": f"Conditional ({c['condition']})",
                "enabled": True,
                "what_to_check": [c["description"]],
                "auto_fix": False,
                "fix_actions": ["Annotate if absent/broken"],
            }
        )
    return checks


def get_default_profile():
    """Return the default full sweep profile."""
    return {
        "name": "Full Sweep v4.0",
        "description": "12 Deep + 30 Surface + 15 Conditional = 57 checks",
        "checks": {c["id"]: True for c in get_all_checks()},
        "fix_tiers": {"fix_immediately": True, "fix_and_report": True, "never_fix": False},
        "content_safety": {c["id"]: True for c in CONTENT_SAFETY},
        "realism_scoring": True,
    }
