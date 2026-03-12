"""All sweep checks + content safety + fix rules — single source of truth.

v5.1 Enhanced — 2026-03-12
Changes from v5.0:
- Every Deep Station now has `sub_checks` (analytical questions, not static thresholds)
- Every Deep Station now has `cross_refs` (connecting data across stations)
- New CROSS_ENTITY_CHECKS section (X01-X06) for multi-entity validation
- New REVALIDATION_RULES for mandatory post-fix verification
- Enhanced CONTENT_SAFETY with semantic guidance + CS9 (spam/nonsense)
- Surface Scan upgraded with `quality_checks` per page
- All changes are ADDITIVE — existing fields untouched, new fields optional
"""

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
        "sub_checks": [
            "D01.1 — Data Recency: Do the dashboard widgets show data from the current period? If all widgets show stale data (90+ days old) or 'No data for this period', change the date filter first.",
            "D01.2 — Getting Started: Is there a setup wizard or onboarding prompt visible? A mature demo should NOT show 'Getting Started' tasks.",
            "D01.3 — Widget vs Report: Note the P&L widget numbers. When you reach D02, verify they match the full P&L report. If they disagree, the display period is misaligned.",
            "D01.4 — Invoice Pipeline: Are all invoices overdue? If 80%+ of unpaid invoices are overdue, the demo looks like an abandoned business. Note for D05.",
            "D01.5 — Business Feed: Check the most recent item in Business Feed. If the newest action is 60+ days old, the environment looks inactive.",
        ],
        "cross_refs": ["D02", "D04", "D05"],
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
        "sub_checks": [
            "D02.1 — Revenue Diversity: Click the top revenue category. Does it have 3+ distinct customer sources? A single mega-invoice generating 80%+ of revenue is a fragile demo.",
            "D02.2 — COGS Consistency: If inventory products exist (check D08 later), COGS should be > $0. If COGS is $0 but products exist, the cost flow is broken.",
            "D02.3 — Gross Margin Context: Calculate Gross Profit / Revenue. Is this margin realistic for the sector? A 95% gross margin on a construction company or 5% on a consulting firm is a red flag. Use your knowledge of the industry.",
            "D02.4 — Expense Coherence: Scan the top 5 expense categories. Do they make sense for this type of business? Payroll should be the largest for services; materials/subcontractors for construction.",
            "D02.5 — Revenue vs Expense Ratio: Is total revenue at least slightly above total expenses? A ratio below 1.0 means the business is losing money. Above 3.0 is unrealistically profitable for an SMB.",
            "D02.6 — JE Date Validation (CRITICAL): If you create a JE to fix P&L, the JE date MUST fall within the period displayed on the P&L report. Use the 1st of the current month. After saving, NAVIGATE BACK to the P&L and confirm Net Income changed. This is the #1 cause of fix regression (QSP BlueCraft reverted because JE was outside display period).",
            "D02.7 — Income Diversity: Are there 2+ income line items? A single 'Sales' line is weak. Look for service income, product sales, consulting fees — varied revenue tells a richer story.",
            "D02.8 — Negative Line Items: Scan for negative values in Income or positive values in Expenses. These indicate misclassified transactions (revenue recorded as expense or vice versa).",
        ],
        "cross_refs": ["D01", "D03", "D08", "D11"],
        "auto_fix": True,
        "fix_actions": [
            "Create JE: DR AR / CR Sales/Revenue to make net income positive",
            "CRITICAL: JE date MUST be 1st of current month (within report display period)",
            "After saving JE: MUST navigate back to P&L and confirm Net Income is now positive",
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
        "sub_checks": [
            "D03.1 — Opening Balance Equity: Is there an 'Opening Balance Equity' account with a balance? In a mature demo this should be $0. A large balance suggests incomplete setup.",
            "D03.2 — Retained Earnings Alignment: Does Retained Earnings movement align with the Net Income you saw in D02? If the P&L says +$285K but Retained Earnings didn't change, something is disconnected.",
            "D03.3 — Asset Concentration: Is any single account holding the majority of Total Assets? If one AR customer or one bank account represents 60%+ of all assets, the balance sheet looks artificially inflated.",
            "D03.4 — Bank Cross-Check: Do the bank accounts listed here match what you see in D04 Banking? If the BS shows 5 accounts but Banking only shows 3, investigate the ghost accounts.",
            "D03.5 — AR vs Invoices: Does total AR approximately match the open invoice total from D05? A massive gap (AR $5M but open invoices $50K) means phantom receivables exist.",
            "D03.6 — Negative Balances: Flag any asset account with a negative balance. A checking account at -$1.83M or negative fixed assets is a demo blocker.",
            "D03.7 — IES Truncation Workaround: If the BS report truncates on IES (only Assets section renders, Equity/Liability missing), use the COA page as fallback — navigate to /app/chartofaccounts?jobId=accounting and review account balances there.",
        ],
        "cross_refs": ["D02", "D04", "D05", "D06", "D11"],
        "auto_fix": False,
        "fix_actions": [
            "Report anomalies with root cause hypothesis",
            "If IES truncates BS: document what WAS readable and verify key balances via COA",
            "Investigate extreme values via COA (navigate to account, check transaction history)",
        ],
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
        "sub_checks": [
            "D04.1 — Transaction Recency: What is the date of the most recent bank transaction? If everything is 60+ days old, the bank feed is stale or disconnected.",
            "D04.2 — Categorization Quality: After categorizing transactions, verify you used 5+ different expense/income accounts. All transactions going to the same account is lazy and unrealistic.",
            "D04.3 — Duplicate Detection: Scan the visible transaction list for exact duplicates (same amount + same date + same payee). 3+ identical entries on the same day suggests a double import.",
            "D04.4 — Connection Health: Are bank connections active or showing errors (Error 103 = auth expired, Error 324 = institution issue)? Note connection age if visible.",
            "D04.5 — QB vs Bank Ratio: Compare QB Balance to Bank Balance for each account. A ratio >10x in either direction or QB negative while Bank positive is an anomaly worth noting — is it reconciliation lag, pending transactions, or data corruption?",
            "D04.6 — Scale Appropriateness: Are bank balances proportional to the business revenue you saw in D02? A $20M money market account in a $900K/year consulting firm is disproportionate. Note it and assess whether it's a platform artifact or genuine data issue.",
        ],
        "cross_refs": ["D03", "D05", "D06"],
        "auto_fix": True,
        "fix_actions": [
            "Categorize first 5-10 uncategorized transactions with VARIED accounts",
            "VERIFY after categorizing: did you use 5+ different accounts? (D04.2)",
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
        "sub_checks": [
            "D05.1 — Balance Reasonableness: Is any customer balance wildly disproportionate to the others? One customer at $20B while the rest are $5K-$50K makes the entire AR report unusable. Evaluate relative to the business scale from D02.",
            "D05.2 — Email Format: Are customer emails using fake domains (@test.com, @example.com)? Note: @tbxofficial.com is the standard platform domain and is acceptable.",
            "D05.3 — Geographic Consistency: Do customer addresses make internal sense? A Mountain View, CA address with a 92129 ZIP (San Diego) is a data quality issue.",
            "D05.4 — Customer-Invoice Linkage: Click into top 3 customers. Does their balance match their open invoices? A customer with $50K balance but no invoices has phantom AR.",
            "D05.5 — Invoice Value Diversity: Are invoice amounts varied? If 80%+ of invoices have the exact same amount, the demo looks obviously auto-generated.",
            "D05.6 — Sector Name Coherence: Do customer names fit the industry? A tire shop shouldn't have 'Dr. Smith Pediatrics', and a non-profit shouldn't have 'ACME Heavy Equipment'.",
        ],
        "cross_refs": ["D03", "D06", "D09"],
        "auto_fix": True,
        "fix_actions": [
            "Fill empty company name, email, address, notes, terms",
            "Rename placeholder names with realistic sector names",
            "Select Net 30 for empty terms",
            "Add context notes that tell the business story (e.g., 'Fleet account — 200+ vehicles, quarterly tire rotation contract')",
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
        "sub_checks": [
            "D06.1 — AP Concentration: Does a single vendor hold >40% of total AP? That level of concentration is unrealistic for most SMBs and makes AP demos feel skewed.",
            "D06.2 — Supply Chain Coherence: Do vendor names form a logical supply chain for this industry? Construction needs material suppliers and subcontractors; consulting needs software, travel, and office vendors.",
            "D06.3 — AP Aging Distribution: What does the aging look like? Healthy: 40-60% Current, declining through buckets. Unhealthy: 80%+ in 91+ days (looks like the company never pays anyone).",
            "D06.4 — AP vs Revenue: Is total AP proportional to annual revenue? AP exceeding annual revenue means the company owes more than it earns per year — a red flag for any demo.",
            "D06.5 — Negative Vendor Balance: Any vendor with a large negative balance (credit > $100K)? This usually means an overpayment or credit memo — note it.",
            "D06.6 — Vendor-Customer Overlap: Does any non-IC entity appear as both vendor AND customer? This is confusing in demos (unless it's an intercompany entity, which is normal).",
        ],
        "cross_refs": ["D02", "D03", "D05"],
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
        "sub_checks": [
            "D07.1 — Payroll-to-Employee Ratio: Divide the Payroll expense from D02 by the employee count. Does the average salary make sense for this industry and region? $30K-$200K is the typical range.",
            "D07.2 — Overdue Tax Filings: Count the TO DO items. More than 5 overdue filings makes the demo look non-compliant — bad for Intuit's brand. Note the count and types.",
            "D07.3 — Job Title Coherence: Do employee titles make sense for the sector? A construction company with 'VP of Digital Marketing' or a non-profit with 'Drilling Supervisor' is inconsistent.",
            "D07.4 — Active vs Terminated: Is the majority of the workforce active? If 60%+ employees are terminated, the demo looks like a company that laid everyone off.",
        ],
        "cross_refs": ["D02"],
        "auto_fix": False,
        "fix_actions": [
            "TRY to edit placeholder names (may require 2FA)",
            "If 2FA blocks: STOP, annotate and advance — DO NOT enter retry loops",
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
        "sub_checks": [
            "D08.1 — Duplicate Detection: Scan the product list for near-duplicates (e.g., 'Consulting Services' and 'Consulting Service'). These confuse demos.",
            "D08.2 — Description Completeness: Click into the top 5 most-used products. Do they have descriptions? Empty descriptions weaken the demo — add 1-2 sentences about each product/service.",
            "D08.3 — Price Realism: Are prices realistic for the sector? $1 for strategy consulting, $100K for a bolt, or $0 for a service that should be billable are all issues.",
            "D08.4 — Income Account Mapping: Are products mapped to the correct income accounts? An inventory product on 'Other Income' or a service on 'COGS' is a misclassification that will show up in D02.",
            "D08.5 — Business Narrative: Do the products collectively tell the story of what this company does? Each product should reinforce the sector narrative.",
        ],
        "cross_refs": ["D02", "D09", "D11"],
        "auto_fix": True,
        "fix_actions": [
            "Rename placeholder names with sector-appropriate names",
            "Set realistic prices where $0",
            "Swap price/cost if inverted",
            "Add descriptions to top 5 products (1-2 sentences each)",
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
        "sub_checks": [
            "D09.1 — Negative Margin Investigation: Any project with margin below -5% requires you to DRILL IN and identify the root cause. Click into the project, check expenses — is it a cost misallocation, missing revenue, or data corruption?",
            "D09.2 — 100% Margin Flag: A project at 100% margin means zero expenses were recorded. You cannot demo job costing profitability with a project that has no costs. Note it as a demo limitation.",
            "D09.3 — Both Sides of Profitability: Each project should ideally have BOTH income (invoices) AND expenses. A project with only income or only expenses cannot demonstrate the profitability tracking feature.",
            "D09.4 — Date Spread: Are all projects started on the same date? Mass-created projects on one date look synthetic. Projects should span 6-18 months.",
            "D09.5 — Customer Linkage: Every project should have a customer assigned. An orphan project (no customer) breaks the narrative of 'who is paying for this work.'",
        ],
        "cross_refs": ["D02", "D05", "D08"],
        "auto_fix": True,
        "fix_actions": [
            "Rename generic names with realistic sector names",
            "Create new projects if <3",
            "Vary status across projects",
            "For extreme negative margins: document root cause in report (not just the number)",
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
        "sub_checks": [
            "D10.1 — Core 4 Reports: Run P&L, Balance Sheet, AR Aging, AP Aging. ALL four must show non-zero data with 'All Dates' selected. If any is zeroed, the report is useless for demos.",
            "D10.2 — AR Aging Cross-Check: Compare the AR Aging total with the AR figure from D03 Balance Sheet and the customer balances from D05. Large discrepancies indicate reconciliation gaps.",
            "D10.3 — Report Period Consistency: Are all reports defaulting to sensible periods? Mismatched periods between P&L and AR Aging create confusing demos.",
        ],
        "cross_refs": ["D02", "D03", "D05", "D06"],
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
        "sub_checks": [
            "D11.1 — Hierarchy Completeness: Navigate the COA and confirm ALL 6 top-level categories exist: Assets, Liabilities, Equity, Revenue (Income), COGS, Expenses. A missing category (e.g., no COGS on a product-based company) creates a structural gap in reports.",
            "D11.2 — Account Count Sanity: Count total accounts. A healthy SMB demo has 40-120 accounts. Under 20 looks barren; over 200 suggests bloat or mass-import artifacts. Note the count for the report.",
            "D11.3 — Sector-Specific Accounts: Does the COA include accounts that tell this company's story? Construction needs 'Subcontractor Expenses', 'Equipment Rental'; Non-Profit needs 'Grant Revenue', 'Restricted Net Assets', 'Program Expenses'; Services need 'Professional Development', 'Software Subscriptions'.",
            "D11.4 — Orphan Accounts: Scan for accounts with $0 balance AND no transactions. A few are normal (placeholder for future use), but 20+ empty accounts clutter the COA and make demos harder to navigate.",
            "D11.5 — Duplicate Account Detection: Look for near-duplicate accounts: 'Office Supplies' vs 'Office Supply', 'Travel' vs 'Travel Expenses'. These cause transaction miscategorization and confusing reports.",
            "D11.6 — Income Account Mapping: Cross-check with D02 — do the income accounts here match the revenue line items on the P&L? If the P&L shows 'Services' but the COA has no 'Service Income' account, there's a mapping inconsistency.",
            "D11.7 — BS Fallback Verification: If D03 Balance Sheet was truncated on IES, this is your fallback. Review account balances here and verify the key figures: Total Assets, Total Liabilities, Total Equity. Do they balance?",
        ],
        "cross_refs": ["D02", "D03", "D08"],
        "auto_fix": True,
        "fix_actions": [
            "Rename placeholder accounts with sector-appropriate names",
            "Annotate missing hierarchy categories in report",
            "Flag orphan accounts (>20 with $0 balance) as cleanup opportunity",
        ],
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
        "sub_checks": [
            "D12.1 — Industry Accuracy: Is the industry field set to the correct value for this company? 'other' is NEVER acceptable — it disables sector-specific features. Non-Profit must show 'Non profit' (exact). Construction must show a construction-related industry.",
            "D12.2 — Address Integrity: Check city + state + ZIP consistency. A San Francisco address with ZIP 92129 (San Diego) or New York city with state CA is a data quality issue. Use your geographic knowledge.",
            "D12.3 — Legal Name vs DBA: Legal Name and DBA (Company Name) should be consistent. 'Keystone BlueCraft LLC' as legal with 'Terra Construction' as DBA means the names are SWAPPED between entities — this is a known issue across QSP and Product Events environments.",
            "D12.4 — i18n Key Detection: Scan ALL visible text on the settings page for raw i18n keys — strings like 'qbo.settings.company.industry' or 'common.label.phone'. These are unresolved translation tokens and are a CRITICAL visual bug.",
            "D12.5 — Cross-Entity Legal Name Audit (MULTI-ENTITY ONLY): If this is a multi-entity environment, you MUST compare legal names across ALL entities. Navigate to each entity's settings and verify no legal name belongs to a different entity. This is the #1 metadata corruption issue found in QSP sweeps.",
            "D12.6 — Contact Info Completeness: Phone, email, and website should all be populated. An empty phone field or missing website for a company that supposedly has $5M+ revenue looks incomplete.",
        ],
        "cross_refs": ["D05", "D06", "D11"],
        "auto_fix": False,
        "fix_actions": [
            "DO NOT correct settings automatically — most require admin/2FA access",
            "ONLY register problems found with severity rating",
            "Report legal name swaps as P1 (blocks trust in multi-entity demos)",
            "Report industry='other' as P2 (disables features but not visually broken)",
            "Report i18n keys as P1 (visually broken, client-facing)",
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

CROSS_ENTITY_CHECKS = [
    # These checks run AFTER all individual entity sweeps are complete.
    # They validate consistency and integrity ACROSS entities in multi-entity environments.
    # Skip entirely for single-entity environments.
    {
        "id": "X01",
        "name": "P&L Consolidation Reconciliation",
        "category": "Cross-Entity Financial",
        "description": "Sum of individual entity Net Incomes should approximately match Consolidated P&L Net Income. Variance >5% requires investigation.",
        "what_to_check": [
            "Record Net Income for EACH entity during individual sweeps",
            "Navigate to Consolidated View, open P&L report",
            "Compare: Sum(Entity NIs) vs Consolidated NI",
            "IC eliminations may explain small differences — large gaps indicate data issues",
        ],
        "cross_refs": ["D02", "C01", "C04"],
    },
    {
        "id": "X02",
        "name": "Legal Name Integrity",
        "category": "Cross-Entity Metadata",
        "description": "Each entity's legal name must match its actual business. Names swapped between entities is the #1 metadata corruption issue.",
        "what_to_check": [
            "Collect legal name + DBA from D12 for EVERY entity",
            "Cross-compare: does Entity A's legal name appear as Entity B's DBA or vice versa?",
            "Verify the entity switcher dropdown labels match the legal names in settings",
            "Known issue: QSP BlueCraft and Terra have swapped legal names",
        ],
        "cross_refs": ["D12"],
    },
    {
        "id": "X03",
        "name": "Industry Consistency",
        "category": "Cross-Entity Metadata",
        "description": "All entities in a multi-entity group should have consistent industry settings. A construction parent with a 'retail' child is suspicious.",
        "what_to_check": [
            "Compare industry field from D12 across all entities",
            "Parent industry should match or be broader than child industries",
            "Flag any entity with industry='other' — this disables features",
            "Known issue: NV2 Rise had industry='other' while Parent and Response had 'Non profit'",
        ],
        "cross_refs": ["D12"],
    },
    {
        "id": "X04",
        "name": "IC Entity Existence",
        "category": "Cross-Entity Financial",
        "description": "For multi-entity environments with IC transactions, verify that IC trading partners exist as vendors/customers in the counterparty entity.",
        "what_to_check": [
            "In C03 (IC Transactions), note the entity names involved",
            "Navigate to each entity and verify the counterparty appears as vendor AND/OR customer",
            "IC entities should have recognizable names (not 'Vendor 1')",
            "IC balances should net to approximately $0 across the group",
        ],
        "cross_refs": ["C03", "D05", "D06"],
    },
    {
        "id": "X05",
        "name": "COA Alignment",
        "category": "Cross-Entity Structure",
        "description": "Entities in the same group should share a similar COA structure. Wildly different account hierarchies make consolidated reporting unreliable.",
        "what_to_check": [
            "Compare top-level account categories across entities (from D11)",
            "All entities should have the same income account types (or subset)",
            "Shared COA (C02) should show accounts in 'Needs review' — note count",
            "Flag if one entity has 100+ accounts while another has 15",
        ],
        "cross_refs": ["D11", "C02"],
    },
    {
        "id": "X06",
        "name": "Data Freshness Parity",
        "category": "Cross-Entity Data Quality",
        "description": "All entities should have similarly recent data. One entity with transactions from 2025 while others have 2026 data creates an inconsistent demo.",
        "what_to_check": [
            "Compare most recent transaction dates across entities (from D01 and D04)",
            "All entities should have data within the same 30-day window",
            "Flag any entity where the newest transaction is 60+ days older than others",
            "Check bank feed connection dates — stale feeds on one entity but active on others is a gap",
        ],
        "cross_refs": ["D01", "D04"],
    },
]

CONTENT_SAFETY = [
    {"id": "CS1", "name": "Profanity", "pattern": "Profanity words EN/PT", "severity": "CRITICAL"},
    {
        "id": "CS2",
        "name": "Placeholder Data",
        "pattern": r"\b(TBX|Lorem|Sample|Foo|Bar|TODO|ACME|Placeholder|Default|Untitled)\b",
        "severity": "P2",
        "guidance": "Scan ALL visible text on every page visited. Placeholders hide in descriptions, notes, memo fields, and product names — not just primary labels.",
    },
    {
        "id": "CS3",
        "name": "Test Names",
        "pattern": "Test, TESTER, IDT, explicit test markers, 'test project', 'test customer'",
        "severity": "P2",
        "guidance": "Check customer names, vendor names, project names, product names, and employee names. Also check notes/description fields where 'test' entries are commonly left behind.",
    },
    {"id": "CS4", "name": "PII Exposure", "pattern": "SSN, credit card, @test emails", "severity": "CRITICAL"},
    {
        "id": "CS5",
        "name": "Cultural Gaffes",
        "pattern": "Sensitive names, political references, controversial figures",
        "severity": "CRITICAL",
        "guidance": "Names referencing real controversial figures (political, religious, criminal) in financial contexts are a demo blocker. The George Floyd Fund incident (NV2 Mar 2025) is the precedent — renamed to 'Social Justice Fund'.",
    },
    {"id": "CS6", "name": "Duplicate Names", "pattern": "Names with numeric suffix (Name2)", "severity": "P2"},
    {"id": "CS7", "name": "Real Person Names", "pattern": "Real persons in financial contexts", "severity": "CRITICAL"},
    {
        "id": "CS8",
        "name": "Bilingual Gaffes",
        "pattern": "Mixed language, raw i18n keys, unresolved tokens",
        "severity": "P2",
        "guidance": "i18n keys look like 'qbo.module.label.xxx' or 'common.xxx.yyy'. Also check for Portuguese/Spanish text in an English environment (e.g., 'Configurações' instead of 'Settings'). These appear most often on Settings pages and in report headers.",
    },
    {
        "id": "CS9",
        "name": "Spam / Nonsense Data",
        "pattern": "Keyboard mash (asdfgh, qwerty), repeated characters (aaaa, 1111), extremely long strings (70+ chars), emoji spam, random URLs in name fields",
        "severity": "P2",
        "guidance": "Scan product names, customer names, vendor names, project names, and memo fields. Data imported from automation or testing often contains keyboard mash entries, UUID strings, or absurdly long auto-generated names. These destroy demo credibility.",
    },
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


REVALIDATION_RULES = [
    # Every fix applied during a sweep MUST be revalidated before moving to the next station.
    # These rules define what "revalidation" means for each fix type.
    {
        "id": "RV01",
        "trigger": "Journal Entry created to fix P&L",
        "revalidation": "Navigate BACK to P&L report. Confirm Net Income changed to positive. If Net Income did not change, the JE date is likely outside the report display period — adjust the JE date to 1st of current month and re-check.",
        "failure_action": "Do NOT proceed to next station. Fix the JE date first. This is the #1 regression cause.",
    },
    {
        "id": "RV02",
        "trigger": "Customer/Vendor/Product renamed",
        "revalidation": "Navigate BACK to the list view (customers, vendors, items). Confirm the new name appears. Then spot-check one transaction linked to this record — does it show the updated name?",
        "failure_action": "If name didn't update on linked transactions, it may be cached. Note in report as 'rename applied, propagation pending'.",
    },
    {
        "id": "RV03",
        "trigger": "Bank transactions categorized",
        "revalidation": "After categorizing 5-10 transactions, navigate to the Banking overview. Confirm the 'For Review' count decreased by approximately the same number. Then check one categorized transaction in the register to verify the account assignment.",
        "failure_action": "If count didn't decrease, the categorization may have failed silently. Re-attempt or note as blocked.",
    },
    {
        "id": "RV04",
        "trigger": "Project created or renamed",
        "revalidation": "Navigate to /app/projects. Confirm the project appears with correct name, customer assignment, and status. Click into it to verify the detail page loads.",
        "failure_action": "If project doesn't appear in list, check for save errors. AI Project Management Agent dialog may have intercepted.",
    },
    {
        "id": "RV05",
        "trigger": "Customer/Vendor enrichment (notes, terms, address, email)",
        "revalidation": "Navigate BACK to the record detail page after saving. Confirm ALL enriched fields persisted. QBO sometimes silently drops fields that fail validation (e.g., malformed email, invalid phone format).",
        "failure_action": "If fields reverted, check format requirements. Phone must include area code, email must be valid format, ZIP must be 5 or 9 digits.",
    },
    {
        "id": "RV06",
        "trigger": "Report period changed",
        "revalidation": "After changing report period (e.g., to 'All Dates'), verify the report now shows non-zero data. If still zeroed, the environment genuinely has no data for that report — note as structural gap, not a period issue.",
        "failure_action": "If changing to All Dates still shows $0, this is a data gap not a display issue. Document accordingly.",
    },
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
    for c in CROSS_ENTITY_CHECKS:
        checks.append(
            {
                **c,
                "tier": "cross_entity",
                "enabled": True,
                "auto_fix": False,
                "fix_actions": ["Document discrepancy with severity and root cause hypothesis"],
            }
        )
    return checks


def get_default_profile():
    """Return the default full sweep profile."""
    return {
        "name": "Full Sweep v5.1 Enhanced",
        "description": "12 Deep + 30 Surface + 15 Conditional + 6 Cross-Entity + 9 Content Safety + 6 Revalidation = 78 checks",
        "checks": {c["id"]: True for c in get_all_checks()},
        "fix_tiers": {"fix_immediately": True, "fix_and_report": True, "never_fix": False},
        "content_safety": {c["id"]: True for c in CONTENT_SAFETY},
        "revalidation": {r["id"]: True for r in REVALIDATION_RULES},
        "realism_scoring": True,
    }
