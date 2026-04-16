# Session 2026-04-16 — INGEST_CHECK + Payroll Tax Debug + May Release Analysis

**Duration**: Full day (multi-hour, high-density)
**Owner**: Thiago Rodrigues
**Significance**: HIGH — one of the most impactful sessions (14 DB fixes, payroll unblocked, May release risk identified)

---

## Part 1: INGEST_CHECK — TCO + Construction (morning/afternoon)

### TCO Dataset (fab72c98-c38d-4892-a2db-5e5269571082)

8 fixes applied directly to V2 Postgres. All verified PASS (0 erros):

| Fix | Rule | Rows |
|-----|------|------|
| LIC field_id NULL | QB_INVOICE_UNIQUE_CLASSIFICATION_DIMENSIONS | 26,288 |
| PSC overlap delete | QB_INVOICE_UNIQUE_CLASSIFICATION_DIMENSIONS | 466 deleted |
| Fixed assets dims | QB_FIXED_ASSETS_HAVE_DIMENSION | 113 inserted |
| Company type match | QB_COMPANY_TYPES_MATCH | 2 products |
| Invoice dates >365d | QB_INVOICES_WITHIN_YEAR | 127 capped |
| PO LIC field_id NULL | QB_PURCHASE_ORDER_UNIQUE_CLASSIFICATION_DIMENSIONS | 2,565 |
| Expense LIC field_id NULL | QB_EXPENSE_UNIQUE_CLASSIFICATION_DIMENSIONS | 2,690 |
| Duplicate product names | QB_CONSTRAINT_UNIQUE_NAME | 3 deleted, 562 LIs redirected |

**Ticket**: PLA-3473 (created with 7 verification CSVs attached)
**Pendente**: QB_INVOICE_TERMS_MATCH — 20,002 erros (Augusto)

### Construction Dataset (321c6fa0-a4ee-4e05-b085-7b4d51473495)

6 fixes applied. All verified PASS:

| Fix | Rule | Rows |
|-----|------|------|
| LIC field_id NULL | QB_INVOICE_UNIQUE_CLASSIFICATION_DIMENSIONS | 8,432 |
| PSC overlap delete | QB_INVOICE_UNIQUE_CLASSIFICATION_DIMENSIONS | 83 deleted |
| PO LIC field_id NULL | (preventivo) | 416 |
| Expense LIC field_id NULL | (preventivo) | 4,024 |
| Invoice terms mismatch | QB_INVOICE_TERMS_MATCH | 256 → Net 30 |
| Time entries outside project | QB_TIME_ENTRIES_START/END_IN_PROJECT | 59 clamped to day 90 |

**Ticket**: PLA-3474 (created with 5 verification CSVs attached)

### Checklist Updated
- 6 new rules added (rows 72-77)
- 2 status updates (FAIL→PASS)
- **Totals**: 76 rules | 62 PASS | 11 N/A | 3 FAIL (pre-existing)
- File: `~/Downloads/CHECKLIST_INGESTION_CONSTRUCTION (7).xlsx`

---

## Part 2: Payroll Tax Debug — Construction Clone (late afternoon/evening)

### Problem
Account `quickbooks-testuser-construction-clone@tbxofficial.com` had a critical warning:
> "Finish federal tax setup by May 16, 2026 to keep running your payroll"

### Root Cause Investigation

1. **Slack search** (500 days range): Found PLA-3431 history — Soranzo, Augusto, Eyji, Kat all involved. Lawton previously handled similar tax enrollment issues.

2. **QBO product change discovered**: Accounts created **after November 15, 2025** are locked into "Automated Taxes & Forms" mode. No toggle to switch to manual filing.
   - Source: https://quickbooks.intuit.com/learn-support/en-us/process-payroll/set-up-payroll-taxes-and-forms/00/370042
   - Source: https://quickbooks.intuit.com/learn-support/en-us/help-article/payroll-forms/manage-automatic-tax-payments-form-filings/L8IgYMkDo_US_en_US

3. **Tax enrollment state**:
   - Federal/IRS: **Declined** — "IRS didn't accept enrollment because of invalid Federal EIN"
   - New York: **E-signature needed**
   - Both are expected failures on test accounts with fake EINs

4. **Employee profile gaps**: `Admin Keystone` and `Simon Walker` had incomplete profiles (missing SSN, address, DOB, pay types, tax withholdings, payment method). Fixed manually with test data.

### Test Execution

1. Completed both employee profiles (SSN `078-05-1120`, address `123 Main St, San Jose, CA 95112`, hourly $25, Paper check)
2. Disabled Auto Payroll for current period (missed cutoff)
3. Submitted manual payroll for **Keystone Terra (Child)**, period 04/16-04/30
4. **RESULT: SUCCESS** — 35 employees, $177,213.21 total, all Paper check

### Key Finding
The May 16 deadline is **future-dated** — QBO gives a 30-day grace period. Only automated tax e-filing is disabled; actual paycheck generation works normally until May 16.

### Linear Updates
- **Comment 1** on PLA-3431: Root cause analysis (autotax enforcement, Nov 2025 cutoff)
- **Comment 2** on PLA-3431: Test result + May Release risk analysis + 3-tier recommendation

---

## Part 3: May Release (Spring Release) Payroll Risk Analysis

### WIS Features Related to Payroll

| WIS # | Category | Feature | OOTB Status | Risk Level |
|-------|----------|---------|-------------|------------|
| 23 | HCM – WFS Launch | **PAYROLL NAME CHANGE and REBRAND** | Blank | **HIGH** (could change UI/enforcement) |
| 24 | HCM – WFS Launch | New Company Onboarding | Yes | Medium (onboarding flow changes) |
| 35 | WFS | **ME Payroll Hub** | Not sure | Medium (Multi-Entity payroll dashboard) |
| 36 | WFS | **Certified Payroll Reports** | Not sure | Low (new report type) |

### Risk Assessment
- **#23 Payroll Rebrand** is a wild card — if QBO tightens tax enforcement as part of the rebrand rollout, the workaround (running with Declined status) could break after May 16
- The May 16 tax deadline falls exactly in the May release window
- No WIS feature explicitly mentions "auto tax enforcement change," but the rebrand could bundle behavioral changes
- WIS lock expected April 17 — need to verify if any payroll behavior changes are included

### Slack Context (Alexandra's Spring Release post, Apr 14)
- 51 active features across 9 categories
- Feature Tracking v4.0 + Spring Release Radar docs shared
- For HCM features, ticket model covers API discovery → data provisioning → UI validation
- Already applied to Time Off (RAC-765)

### Recommendation (posted to PLA-3431)
1. **Short term (now–May 16)**: Payroll works. Demo-ready. No action needed.
2. **Medium term (before May 16)**: Request Intuit Payroll Ops to either flip autotax flag to manual, or approve test EIN
3. **Long term**: PLA-3451 (migrate to auto payroll) must account for Nov 2025 autotax enforcement on newer accounts

---

## Learnings for Future Sessions

### Payroll-Specific
1. **Nov 15, 2025 cutoff**: QBO accounts created after this date are LOCKED into Automated Taxes. Cannot be disabled. This affects ALL demo/test accounts provisioned from Dec 2025 onwards.
2. **Fake EINs always fail enrollment**: Federal tax enrollment uses IRS validation — test EINs will always be "Declined." This is expected and NOT a bug.
3. **Grace period pattern**: QBO gives ~30 days after account creation before enforcing tax setup. Payroll runs normally during grace period; only e-filing is disabled.
4. **Paper check workaround**: Even without bank connection or tax enrollment, payroll runs via Paper check. This is the safest demo path.
5. **Auto Payroll vs Manual**: Auto Payroll processes on schedule. If cutoff is missed (e.g., within 2 days of pay date), system falls back to manual submission. This is actually useful for demos — you control when it runs.
6. **Employee profile completeness**: QBO requires ALL of: Personal Info (SSN, DOB, address), Pay types (hourly/salary + rate), Employee taxes (Federal W-4 + State), Payment method (check/DD). Missing ANY of these blocks the employee from being included in payroll.
7. **Test data for employees**: Safe test SSN: `078-05-1120`. Safe test address: `123 Main St, San Jose, CA 95112`. W-4: Single, 0 allowances, no additional withholding.

### May Release Intelligence
8. **WIS lock date**: Expected April 17 — after this, feature scope is frozen
9. **3 payroll features in May release**: Rebrand (#23), ME Hub (#35), Certified Reports (#36)
10. **Spring Release validation model**: Alexandra's ticket model (API discovery → data provisioning → UI validation) — already applied to Time Off (RAC-765)
11. **Risk: Payroll Rebrand (#23)** may change enforcement behavior — monitor after WIS lock

### Cross-Cutting
12. **Triangulation works**: Slack (historical context) + Linear (ticket state) + QBO Help (product docs) + hands-on testing = comprehensive picture. Never rely on just one source.
13. **Product changes vs config issues**: The tax setup problem was NOT a configuration error — it was a QBO platform change. Always check if behavior changed at the product level before debugging config.
14. **Future account provisioning**: Any new QBO account must account for the Nov 2025 autotax enforcement. Either (a) provision before Nov 2025 cutoff (impossible now), (b) get Intuit Ops to flip the flag, or (c) complete real tax enrollment (impossible with test EINs).

---

## Scripts Created

| Script | Purpose |
|--------|---------|
| `~/Downloads/post_comment_3431.py` | Post root cause analysis to PLA-3431 |
| `~/Downloads/post_comment_3431_v2.py` | Post test result + May release risk to PLA-3431 |
| (INGEST_CHECK scripts from Part 1 — see memory.md for full list) | |

## Tickets Updated
- **PLA-3431**: 2 comments added (root cause + test result + May release risk)
- **PLA-3473**: Created (TCO 8 fixes)
- **PLA-3474**: Created (Construction 6 fixes)

---

**Next session priorities:**
1. Monitor WIS lock (Apr 17) — check if payroll rebrand includes enforcement changes
2. Follow up on activity plans (Augusto) for TCO + Construction DB fixes
3. Before May 16: escalate to Intuit Ops for autotax flag flip or test EIN approval
4. TCO invoice terms investigation (20K errors)
