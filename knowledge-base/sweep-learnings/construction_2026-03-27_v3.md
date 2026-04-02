# QBO Sweep Report — Construction Dataset (Keystone 8-Entity)
## God Complete v8.1 | 2026-03-27

### Executive Summary
- **Dataset:** Construction (Keystone 8-entity IES hierarchy)
- **Profile:** God Complete v8.1
- **Score:** 7/10 | Realism: 74/100
- **Screens Executed:** 46 (parent) + 30 (P0 children) + 20 (P1 children) + 7 (cross-entity) = 103 total
- **CS Violations:** 5 found, **3 FIXED**, 2 documented (NEVER FIX tier)
- **P1 Findings:** 4 must-fix | **P2 Findings:** 5 should-fix

---

### Entity Hierarchy
| Entity | Type | Priority | Screens | Status |
|--------|------|----------|---------|--------|
| Keystone Construction (Par) | parent | P0 | T01-T46 (46) | COMPLETE |
| Keystone Terra (Ch.) | child | P0 | T01-T15 (15) | COMPLETE |
| Keystone BlueCraft (Ch.) | child | P0 | T01-T15 (15) | COMPLETE |
| KeyStone Ironcraft | child | P1 | T01+T02+T05+T06 (4) | COMPLETE |
| KeyStone Stonecraft | child | P1 | T01+T02+T05+T06 (4) | COMPLETE |
| KeyStone Canopy | child | P1 | T01+T02+T05+T06 (4) | COMPLETE |
| KeyStone Ecocraft | child | P1 | T01+T02+T05+T06 (4) | COMPLETE |
| KeyStone Volt | child | P1 | T01+T02+T05+T06 (4) | COMPLETE |
| Cross-Entity | validation | - | X01-X07 (7) | COMPLETE |

---

### Parent Entity Financial Summary (YTD Jan 1 - Mar 27, 2026)
| Metric | Value |
|--------|-------|
| Total Income | $592,662.64 |
| COGS | $7,129.56 |
| Gross Profit | $585,533.08 |
| Total Expenses | $495,138.38 |
| Net Operating Income | $90,394.70 |
| Net Income | $81,871.08 |
| **Margin** | **13.8%** |
| Total Assets | $14,170,138.86 |
| Total Liabilities | $2,348,094.11 |
| Total Equity | $11,822,044.75 |
| A = L + E | BALANCED |
| Bank (QB) | $8,336,740.37 |
| Bank (External) | $460,000.00 |
| AR Total | $4,382,515.63 |
| AP Total | $1,046,481.64 |
| Quick Ratio | 5.89 |

---

### CS Violations — Content Safety
| # | Type | Location | Description | Action | Status |
|---|------|----------|-------------|--------|--------|
| 1 | CS3 | T05 Customers | "Client 1" generic customer name | Renamed to "Hawthorne Development Group" | **FIXED** |
| 2 | CS3 | T09 Projects | "Demo 3.5" test project name | Renamed to "Coral Gables Mixed-Use Development" | **FIXED** |
| 3 | CS3 | T09 Projects | "Test 123" test project name | Renamed to "Summit Ridge Foundation Work" | **FIXED** |
| 4 | CS3 | T10 Invoices | TBX prefix on 33 invoice numbers (TBX-2025-xxxxx) | System-generated, not editable | DOCUMENTED |
| 5 | CS5 | T15 Settings | Legal name "Testing_OBS_AUTOMATION_DBA" | NEVER FIX tier — company settings protected | DOCUMENTED |

---

### Findings — Prioritized

#### P1 — Must Fix (4)
1. **Overdue Tax Filings (T16):** 5 overdue tax filings — CA DE 9, CA DE 9C, 941, 940, W-2 (all due Jan 29). IRS/state penalties visible to expert viewers.
2. **Zero Contractors (T17):** No contractors in parent entity. Subcontractors are 40-60% of construction costs. Critical demo gap.
3. **Zero Fixed Assets (T21):** No equipment/vehicles registered. Construction is equipment-heavy industry.
4. **Online Payments Disabled (T27):** Feature #1 prospects ask about. Requires merchant account to enable.

#### P2 — Should Fix (5)
5. **Bank QB vs External Discrepancy (T04):** QB $8.37M vs Bank $460K. Prior cycle inflation artifact.
6. **AR 91+ Days = $3.8M (T40):** 87% of AR aged beyond 91 days. Prior cycle data.
7. **AP 91+ Days = $660K (T41):** 63% of AP aged beyond 91 days. Prior cycle data.
8. **Zero Recurring Templates (T20):** Feature not demonstrated — opportunity for automation showcase.
9. **Zero Workflows (T25):** Automation feature gap — IES differentiator not visible.

#### P3 — Nice to Have (4)
10. Negative expense accounts on P&L (Consultancy -$163K, Payroll -$3K)
11. 2 employees with missing pay rate (Jones Jim, Kennedy Bob)
12. Revenue Recognition not configured
13. CRM features (Leads/Proposals/Contracts) all empty

---

### Parent Screen Results (46 Screens)
| Screen | Status | Key Metric | CS |
|--------|--------|------------|-----|
| T01 Dashboard | WARN | Net $342K (Feb), Bank $460K | - |
| T02 P&L | WARN | Income $593K, Net $82K, 13.8% margin | - |
| T03 Balance Sheet | WARN | Assets $14.2M, A=L+E balanced | - |
| T04 Banking | WARN | QB $8.37M vs Bank $460K | - |
| T05 Customers | PASS | 51 customers | 1 FIXED |
| T06 Vendors | WARN | 48 vendors, 254 overdue bills | - |
| T07 Employees | WARN | 7 employees, 2 missing pay rate | - |
| T08 Products | PASS | 51 items (30 service, 24 inventory, 4 bundle) | - |
| T09 Projects | PASS | Multiple projects | 2 FIXED |
| T10 Invoices | WARN | 37 invoices, 51% overdue | TBX documented |
| T11 Bills | WARN | 52 bills, 96% overdue | - |
| T12 Expenses | PASS | 52 expenses | TBX documented |
| T13 Estimates | WARN | 71 estimates, $82M backlog inflated | - |
| T14 COA | PASS | 76 accounts, diverse types | - |
| T15 Settings | WARN | S-Corp, Accrual, CA legal addr | Legal name documented |
| T16 Payroll Hub | FAIL | 5 overdue filings | - |
| T17 Contractors | FAIL | Zero contractors | - |
| T18 Time Tracking | PASS | 4 entries visible | - |
| T19 Sales Tax | PASS | Setup complete | - |
| T20 Recurring | WARN | Zero templates | - |
| T21 Fixed Assets | FAIL | Zero assets | - |
| T22 Rev Recognition | WARN | Not configured | - |
| T23 Budgets | PASS | 1 active budget (FY2026) | - |
| T24 Classes/Locations | PASS | 4 classes, 2 locations | - |
| T25 Workflows | WARN | Zero workflows | - |
| T26 Custom Fields | PASS | 3 fields (Insurance, Exp Date, PM) | - |
| T27 Sales Settings | WARN | Online payments disabled | - |
| T28 Expense Settings | PASS | POs enabled, billable expenses ON | - |
| T29 Advanced Settings | PASS | Accrual, Classes ON, Projects ON | - |
| T30 Reconciliation | WARN | 1/6 accounts reconciled | - |
| T31-T46 | MIXED | Detail drills, reports, AI features | - |

---

### Recommendations

**Immediate (before next demo):**
1. Acknowledge overdue tax filings or file them in sandbox
2. Add 5-10 subcontractors with realistic names
3. Add 3-5 fixed assets (trucks, excavator, office equipment)

**Short-term:**
4. Create 3-5 recurring templates (rent, insurance, supplies)
5. Create 2-3 workflows (invoice reminders, payment notifications)
6. Configure Revenue Recognition rules for construction contracts

**Nice to have:**
7. Clean up AR/AP aging (prior cycle data)
8. Fix negative expense accounts via JE
9. Populate CRM features (leads, proposals)

---

*Generated by Claude Code Sweep Engine v8.1 — 2026-03-27T22:42:00-03:00*
