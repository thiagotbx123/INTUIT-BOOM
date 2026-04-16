# Bank Linking & Payroll Verification — Deep Research

> **Date**: 2026-04-14
> **Author**: Thiago Rodrigues (with Claude)
> **Environment**: IES Construction Clone (`quickbooks-testuser-construction-clone@tbxofficial.com`)
> **Related Tickets**: PLA-3431, PLA-3336, PLA-2810, PLA-1727, PLA-1141, PLA-2335

---

## Executive Summary

Bank linking in QBO demo environments operates on **two completely separate flows**:

1. **Banking Module** (Accounting > Bank transactions) — WORKING. Bank of Intuit (BOI) serves as a container for transactions injected by TestBox's automation (activity plans). Transactions appear as "pending" and a cron confirms them weekly.

2. **Payroll/Payments Verification** (Payroll > Setup > Connect your bank) — BROKEN. BOI cannot complete Intuit's internal bank verification process. It gets stuck permanently at "Thank you, we're reviewing your information."

**The Payroll blocker cannot be resolved autonomously by TestBox.** It requires Intuit's internal bank verification team to approve the account, or for Intuit to create an alternative fake bank that passes verification (precedent: Vishwa, Feb 2025).

---

## Architecture: Two Separate "Connect Your Bank" Flows

### Flow 1: Banking Module (WORKING)

```
TestBox Activity Plans (API) → Create bank transactions
         ↓
Bank of Intuit (BOI) = "container/pipe" in Banking module
         ↓
Transactions appear as "Pending" in Bank Transactions page
         ↓
Cron (confirm_bank_transactions, PLA-1727/PLA-2810) auto-confirms > 30 days
         ↓
Confirmed transactions create Expense records
```

**Status**: Fully operational. All 3 critical companies have active bank feeds.

### Flow 2: Payroll/Payments Verification (BROKEN)

```
Payroll Setup Wizard → "Connect your bank" step
         ↓
User selects Bank of Intuit
         ↓
QBO sends micro-deposits ($0.XX) to verify the account
         ↓
Screen: "Thank you, we're reviewing your information"
         ↓
STUCK FOREVER — BOI is fake, no actual deposits, verification never completes
         ↓
BLOCKS: Direct Deposit, Bill Pay, Tax E-filing
```

**Status**: Permanently stuck. No autonomous workaround exists.

---

## Bank Account Map — IES Construction Clone (verified 2026-04-14)

| Company | Role | Bank Accounts | Pending | BOI? |
|---------|------|---------------|---------|------|
| **Keystone Construction** | Parent | MMA Guardian ($10.9M), 1010 Checking ($460K) | 110 | NO |
| **Keystone Terra** | Main Child | BOI ($0), MMA Guardian ($10.9M), 1010 Checking ($460K) | 98 | YES |
| **Keystone BlueCraft** | Child | BOI ($0, Posted: -$1.07M), 1010 Checking ($460K), MMA Guardian ($10.9M) | 117 | YES |
| Other 5 children | Child | Not checked | ? | ? |

### Observations

- **MMA Guardian** and **1010 Checking** are shared across all 3 critical companies (same balances)
- **BOI only exists in Terra and BlueCraft**, not in the Parent
- **BlueCraft BOI has negative Posted** (-$1,072,864.01) — potential data issue
- All 3 companies have healthy pending transaction counts (98-117)
- Parent has 110 pending transactions despite no BOI — activity plans inject via 1010 Checking

---

## Payroll Status — Keystone Terra (verified 2026-04-14)

### What WORKS
- **Auto Payroll**: ON, 35 employees, next payday Apr 15
- **Paycheck list**: accessible
- **Employee management**: 35 employees configured
- **Contractors**: configured
- **Benefits**: Retirement Plans (Human Interest, Vestwell), Health Insurance
- **HR advisor (Mineral)**: functional

### What's BLOCKED (all depend on bank verification)

| Blocker | Status | Due Date | Impact |
|---------|--------|----------|--------|
| Bank verification (micro-deposit) | **STUCK** — "reviewing your information" | Apr 07 (OVERDUE) | Gates everything below |
| Federal EIN | **REJECTED** by IRS (invalid) | — | Blocks electronic filing |
| Automated taxes | **NEEDS ACTION** | — | Can't pay/file taxes |
| Tax filings Q1 2026 (941, CA DE 9, etc.) | **PENDING** | Apr 28 | Will fail without EIN + bank |
| Authorization forms | **OVERDUE** | Feb 17 | Compliance |
| Direct deposit | **BLOCKED** | — | Payroll runs but no real deposits |
| Bill Pay | **BLOCKED** | — | Can't send payments |
| Tax e-filing | **BLOCKED** | — | Can't submit electronically |

### The Verification Screen

URL: Payroll > Setup Tasks > Section 2 > "Watch your bank account for a small deposit"

Shows:
> "Thank you, we're reviewing your information"
> "We are currently in the process of reviewing the information you submitted. We will reach out to you in the next few days if we need anything else."

Three features gated by this verification:
1. Send money with QuickBooks (Bill Pay)
2. Pay your workforce with direct deposit
3. E-file and e-pay your taxes

**No buttons, no actions, no workaround. Dead end.**

---

## Feature-to-Company Map

| Feature | Runs On | Source |
|---------|---------|--------|
| **Payroll** | Terra (primary), setup done for all companies | Augusto (PLA-3431), Alexandra (Slack) |
| **Bill Pay** | Parent + Terra + BlueCraft | Thiago to Kat (Slack) |
| **Payments** | Terra only | Thiago to Kat (Slack) |
| **Banking (transactions)** | Parent + Terra + BlueCraft (verified) | Screenshots 2026-04-14 |

---

## Historical Context

### Bank of Intuit (BOI)
- **What**: Fake test bank available when `test_user` flag is enabled in QBO
- **Purpose**: Internal Intuit testing tool for bank features
- **Where it appears**: Banking module (as bank connection), Payroll setup wizard
- **Current issue**: Passes initial connection but fails verification (micro-deposit never completes)

### Timeline

| Date | Event | Source |
|------|-------|--------|
| 2024 | BOI was functional, payroll configured on IES Sales | PLA-2335 |
| 2024-07 | Activity plan for bank transactions created (PLA-1141) | Bryan/Linear |
| 2024-10 | Cron to confirm bank transactions created (PLA-1727) | Nora/Linear |
| 2025-01 | Vishwa (Intuit) created alternative fake bank for Keystone, passed verification | Nora (Slack) |
| 2025-04 | PLA-2335 opened for payroll setup | Lucas Soranzo |
| 2025-06 | PLA-2335 blocked, waiting on Lawton info | Lucas Soranzo |
| 2025-08 | Sam reported BOI issues | Slack |
| 2025-10 | Nora confirmed Lawton's "magic trick" for approvals | Slack |
| 2025-11 | PLA-2335 cancelled/went to limbo | Linear |
| 2026-01 | Construction Clone created (from IES Sales) | PLA-3431 |
| 2026-04-01 | Augusto starts investigating payroll (PLA-3431) | Linear |
| 2026-04-08 | Augusto: "BOI gives error at end of bank setup" | PLA-3431 comment |
| 2026-04-08 | Auto-payroll setup: complete for all companies | PLA-3431 comment |
| 2026-04-09 | Augusto: "BOI remains forever in confirmation phase" | PLA-3431 comment |
| 2026-04-13 | Thiago: shared Vishwa precedent as potential unblock | PLA-3431 comment |
| 2026-04-14 | Augusto: prefers autonomous solution, Vishwa approach not ideal | PLA-3431 comment |
| 2026-04-14 | **This deep research conducted** | This document |

### Key People (Bank/Verification)

| Person | Role | Status |
|--------|------|--------|
| **Lawton Ursrey** | Former Intuit contact, had "magic trick" for bank approvals | **No longer at TestBox/Intuit** |
| **Vishwa** | Intuit engineer, created alternative fake bank (Feb 2025) | Active at Intuit |
| **Augusto Gunsch** | TestBox engineer, owns PLA-3431 | Working on payroll reimplementation |
| **Lucas Soranzo** | TestBox engineer, owns automation/crons | Context on activity plans |
| **Nora Nguyen** | TestBox PM, documented BOI history | Has institutional knowledge |

---

## Possible Solutions (ranked by autonomy)

### 1. Ask Intuit to approve BOI verification (RECOMMENDED — fastest)
- **How**: Message Kat, ask who replaced Lawton/Vishwa for bank verifications
- **Precedent**: Vishwa did this for Keystone Construction in Feb 2025
- **Risk**: Depends on finding the right person at Intuit
- **Effort**: Low (one message)
- **Unblocks**: Direct deposit, Bill Pay, tax e-filing

### 2. Ask Intuit to create alternative fake bank (PROVEN)
- **How**: Request what Vishwa did — create a separate fake bank that passes verification
- **Precedent**: Worked for IES Sales (Keystone Construction)
- **Risk**: Augusto notes this is "higher maintenance" — bank name could vary, not scalable
- **Effort**: Medium (Intuit action required)

### 3. CSV Upload for Banking module (AUTONOMOUS — but doesn't fix payroll)
- **How**: Banking > Link account (dropdown) > Upload from file > CSV with Date/Description/Amount
- **What it does**: Injects transactions into Banking module as pending
- **What it DOESN'T do**: Does NOT fix payroll verification, Bill Pay, or tax filing
- **Use case**: Alternative data injection for environments without BOI or activity plans
- **Effort**: Low (can be automated with Playwright)

### 4. Wait for Engineering fix (PLA-3431)
- **How**: Augusto finds autonomous solution
- **Risk**: Augusto himself says "ideally from a technical standpoint" he wants autonomy, but current options are limited
- **Effort**: Unknown timeline

### 5. Skip bank verification entirely
- **How**: Payroll runs via Auto Payroll WITHOUT completed bank verification
- **Reality**: Already happening — 35 employees getting paid Apr 15
- **Limitation**: No direct deposit, no tax e-filing, no Bill Pay
- **Use case**: Demo-only (visual payroll data exists, features are "shown" but not fully functional)

---

## CSV Upload — Technical Details (for Solution 3)

### Path in QBO
Banking > "Link account" button (dropdown arrow) > "Upload from file"

### CSV Format
```
Date,Description,Amount
04/01/2026,Client Payment - Apex Tire Supply,15000.00
04/02/2026,Office Rent - Monthly,-4500.00
04/03/2026,Vendor Payment - TrailBoss Equipment,-8200.00
```

### Requirements
- 350 KB max per file
- 3 columns: Date, Description, Amount
- OR 4 columns: Date, Description, Credit, Debit
- Date format: dd/mm/yyyy or mm/dd/yyyy (consistent)
- No "amount" word in Credit/Debit headers
- Leave zero cells blank

### Automation potential
- Can be scripted with Playwright (same tool as sweeps)
- Generate CSV from dataset, upload via browser automation
- No dependency on BOI, Intuit, or anyone

---

## Augusto's Position (from PLA-3431, 2026-04-14)

> "Your suggested approach [Vishwa fake bank] could work, but I see it as higher maintenance and not ideal. If we depend on them creating the fake bank for every account we eventually ingest, that creates issues: the bank would still need to be assigned in the payroll form, and unless they consistently use the same name every time, our code would not know what to look for."

> "Ideally, from a technical standpoint, I want an autonomous solution."

**Translation**: Engineering wants to solve this without depending on Intuit, but currently has no way to bypass the bank verification flow.

---

## BREAKTHROUGH: IES Sales Original Uses 1010 Checking, NOT BOI (discovered 2026-04-14)

### The Key Finding

By logging into the IES Sales original (`quickbooks-test-account@tbxofficial.com`) and comparing with the Clone, we discovered:

| | Clone (broken) | Original IES Sales (working) |
|---|---|---|
| Payroll bank | BOI (Augusto tried to use) | **1010 Checking (....7418)** |
| Verification status | Stuck "reviewing your information" | **Verified and active** |
| Setup Tasks | "Watch your bank account for a small deposit" | "Set your tax preferences" (past the bank step!) |
| Who configured | Augusto (Apr 2026) | **Vishwa from Intuit** (Jan/Feb 2025) |

### What This Means

Augusto used the WRONG bank for payroll setup. He tried BOI, which gets stuck in verification. The working environment uses a regular bank account (1010 Checking) that was created and verified by Vishwa via Intuit's internal process.

### Working Environment Data (template to replicate)

**Principal Officer (fake data used by Vishwa):**
- Name: JOHN106 VIGIL448
- Title: President
- Phone: (490) 634-9239
- Address: 8212 134th Pl Ne, Redmond WA 94043

**Payroll Bank:** 1010 Checking (account ending ....7418)

**Payroll Accounting Mapping:** Fully mapped to Chart of Accounts:
- Bank Account: 1010 Checking
- Wages: 6325 Payroll Expenses:Salaries & Wages
- Taxes: Payroll Expenses:Taxes
- Liabilities: Payroll Liabilities (Federal, CA, NY, IL)

### Action Required

Ask Intuit (via Kat) to replicate what Vishwa did on the Clone:
1. Create/verify a bank account for payroll (like 1010 Checking ....7418)
2. This bypasses BOI completely
3. Vishwa's original fix reference: https://testbox-talk.slack.com/archives/C06PSSGEK8T/p1738427941034019

### Slack Message Sent

Message sent to Kat on 2026-04-14 requesting:
- Replication of Vishwa's bank verification for Clone
- Identification of who on Intuit side can handle this now

---

## UPDATE: Autonomous Payments Application Submitted (2026-04-14)

### What Was Done

Following Lawton's historical process ("I applied for payments and elite bill pay and notified Risk Ops to approve"), Thiago submitted the QuickBooks Payments application directly from the Clone:

1. **Path**: Settings > Account and Settings > Payments > Activate
2. **Form**: "Apply to accept online payments" — 3 sections filled:
   - About your business: pre-populated (Keystone Terra, Corporation, San Diego CA)
   - About you: owner info filled
   - Your deposit account: **manual bank entry** — US Bank NA, routing `122235821`, account `467266` (from PLA-2335)
3. **Result**: Application accepted — status changed to **"Your payments application is being reviewed"**
4. **Timeline**: "We'll email you with an update in 2 business days" (~Apr 16)

### Why This Matters

Nora (Feb 2025): *"Bill Pay is still blocked as we need the subscription first to be able to verify the bank."*
- Ref: https://testbox-talk.slack.com/archives/C06PSSGEK8T/p1738427941034019

Intuit docs: *"When you apply for Bill Pay Elite, QuickBooks reviews your information to determine eligibility for QuickBooks Payments, QuickBooks Payroll, and the B2B Business Network as part of a bundled review process."*

**If Risk Ops approves**: Cards, ACH, PayPal/Venmo activate → Bill Pay unlocks → bank verification may complete → payroll direct deposit + tax e-filing unblocked.

### Augusto's Correction

Augusto noted that "1010 Checking" is a Chart of Accounts entry ingested by TestBox, NOT an actual connected bank account. The Payroll Settings screen shows the CoA mapping, not the verified bank connection. This is a valid distinction.

### Current Status

| Item | Status |
|------|--------|
| Payments application | **Under review** (submitted 2026-04-14) |
| Expected response | ~Apr 16 (2 business days) |
| Bank used | US Bank NA (routing 122235821, acct 467266) |
| Cards/ACH/PayPal | Still Off (pending approval) |
| Kat thread | Active (Plan B if auto-approval fails) |
| Augusto thread (PLA-3431) | Pending update with this new info |
