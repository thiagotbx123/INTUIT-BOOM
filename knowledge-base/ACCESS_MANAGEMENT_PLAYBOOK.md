# ACCESS MANAGEMENT PLAYBOOK — Intuit TestBox Environments

> **Owner**: Thiago Rodrigues + Alexandra Lacerda (TSA, Raccoons)
> **Effective**: 2026-04-16 (Kat policy update)
> **Source**: Triangulated from Slack (60+ msgs, 12 channels), Coda (Solutions Central), Drive (TBX Admin SOP), Linear (RAC-764)
> **Confidence**: 97%

---

## 1. THE NEW POLICY (Kat, Apr 16 2026)

Two distinct scenarios for access requests arriving in `#external-testbox-intuit-allusers`:

| Scenario | Signal | Action | Who |
|----------|--------|--------|-----|
| **A — Add Environment** | Person already has TestBox account, wants access to another env (e.g., "can I get QBOA MM?") | Add the environment yourself | Thiago / Alexandra |
| **B — Net-New Account** | Person does NOT have a TestBox account at all | DO NOT create account; send the canned response | Intuit's user-license team handles |

### Canned Response for Scenario B

```
Hi, please go to this doc and follow it further instructions on how to request a license for TestBox. Link here: https://docs.google.com/document/d/1RmlGoruS1bzSFgA-7ZYYr245ioVklFifVqvWfkO8tUc/edit?tab=t.0
```

> **ATENCAO (Kat, Apr 16 2026)**: O link do Google Doc acima e para os USUARIOS, nao para nos.
> Nos NAO precisamos acessar esse documento. So precisamos enviar o link como esta.
> Kat: *"We don't need to request access, we just need to send them the link"*

### Previous Process (before Apr 16)

- **ScribeHow guide**: https://scribehow.com/viewer/Submitting_a_Ticket_With_Sales_Tech_Ops__t8untHbNRsaQ_DgF3YveaA
- **Loom walkthrough**: https://www.loom.com/share/fc3158dec6c541228353ef082c681d7a
- **Intuit Slack channel**: `#sales-tech-ops-tickets` (private, Intuit-side)
- Lawton (Intuit SE) used to redirect people with: "Sales Ops owns and manages all TestBox licensing requests"
- cduarte (Intuit) also redirected: "submit an access request here" → Intuit internal channel

---

## 2. HOW TO: ADD AN ENVIRONMENT (Scenario A)

Two methods, from simplest to most thorough:

### Method 1: Impersonate an Admin (UI — Preferred for TSA)

1. Go to **app.testbox.com** → log in with your TestBox account
2. **Impersonate** an Intuit admin (e.g., Lawton Ursrey `lawton_ursrey@intuit.com`)
3. Navigate to **User Admin Settings** (gear icon → user management)
4. Find the user by email
5. Check which environments they have access to
6. **Add the requested environment** to their list
7. Confirm with the user in Slack

> **Example (Kat, Mar 2026)**: "impersonate lawton, go to user admin settings, see what Rama_Ghanta@intuit.com can access, add UAT IES Construction"

### Method 2: Django Admin (tbxadmin — for complex cases)

URL: `https://app.testbox.com/tbxadmin/`

**To add an environment to existing user:**
1. Go to `/tbxadmin/testbox/workspacemembership/` (new page, has bulk operations + filter by user/workspace)
2. Filter by the user's email
3. Click **Add another Workspace membership**
4. Select the workspace (environment)
5. Role = appropriate (usually ADMIN for Intuit admins, or whatever they need)
6. Is active = checked
7. Save

**To remove a user from an environment:**
1. Same page → filter by user
2. Delete the workspace membership
3. Note: Kat asked (Apr 16) whether removing workspace = also removing from user exports → answer: you should **delete from Django** if you don't want them showing up

### Method 3: Kat's Approach (for Mailchimp de-provisioning)

Kat's question (Apr 16): "Should I do this in Django or in the User settings panel masquerading as one of the Mailchimp admins?"

- **Django**: removes at platform level, user won't show in exports
- **User settings panel (masquerading)**: removes access but user may still appear in exports

---

## 3. HOW TO: SET UP A BRAND NEW CUSTOMER (for reference — NOT for Intuit access requests)

Full SOP from `TBX_Admin_new_customer_setup.docx` (Drive, 2026-03-27):

| Step | What | Where | Required |
|------|------|-------|----------|
| 1 | Create Company | `/tbxadmin/crm/company/add/` | Yes |
| 2 | Create Admin User | `/tbxadmin/crm/user/add/` | Yes |
| 3 | Create EmailAddress record (allauth) | `/tbxadmin/account/emailaddress/add/` | **YES — commonly missed** |
| 4 | Create Workspace | `/tbxadmin/testbox/workspace/add/` | Yes |
| 5 | Add Workspace Membership | Inline on Workspace page | Yes |
| 6 | Set current_workspace on User | Edit User page | Yes |
| 7 | Create Trial(s) | `/tbxadmin/testbox/trial/add/` | Yes |
| 8 | Set Primary Trial on Workspace | Edit Workspace | Optional |
| 9 | Trigger Trial Sync | `python manage.py trial_sync_all` or Backfill CRM data action | **YES — commonly missed** |
| 10 | Salesperson + Distributions | User + Company admin pages | If partner |

> Steps 3 and 9 are the most commonly missed.

---

## 4. KNOWN GOTCHAS

| Issue | Source | Resolution |
|-------|--------|------------|
| **410 workspace memberships on UAT IES Construction** | INC-2026-03-25 | Backfill action accidentally added all users. Use new `/tbxadmin/testbox/workspacemembership/` page with bulk delete |
| **Auto-login fails for impersonated users** | Multiple incidents | Try: refresh Chrome (Ctrl+Shift+R), clear cache, disable extensions |
| **White screen on TestBox** | Zak Kelly case Apr 2026 | Chrome extension conflict. Fix: disable extensions or use incognito |
| **User only loads most recent sandbox** | TestBox App Q&A Mar 17 | Platform limitation: buyer users added to multiple deals only load the most recent. Manual reassignment needed |
| **Mailchimp workspace not in dropdown** | RAC-764, Apr 2026 | Can't just add via Core; needs workspace membership creation + possibly separate company provisioning |
| **"Can demo" / "can sandbox" checkboxes** | TestBox App Q&A Mar 17 | Product access issues often from unselected checkboxes in company's product distribution feature set |

---

## 5. KEY CONTACTS

| Who | When to Contact | Method |
|-----|----------------|--------|
| **Kevin Small** | Quick product config, user setup, Django questions | Slack `#product` |
| **Lucas Soranzo** | Core/Django technical issues, workspace membership bulk operations | Slack `#product` |
| **Deyton** | Workspace membership admin page, incident recovery | Slack `#product` or `#engineering` |
| **Gayathri** | Project tracking, incident coordination | Slack |
| **Augusto** | Trial sync, ingestion, Retool | Slack `#engineering` |
| **Kat** | Policy decisions, Intuit relationship, escalations | Slack `#intuit-internal` |

---

## 6. REFERENCE LINKS

| Resource | URL |
|----------|-----|
| TestBox Admin | `https://app.testbox.com/tbxadmin/` |
| Workspace Memberships (new) | `https://app.testbox.com/tbxadmin/testbox/workspacemembership/` |
| Company Admin | `https://app.testbox.com/tbxadmin/crm/company/` |
| User Admin | `https://app.testbox.com/tbxadmin/crm/user/` |
| New customer setup SOP (Drive) | `https://docs.google.com/document/d/1pMUCO43F-DjzJaJy40wqmG4BgMFB-y6uhFZ85Js7G5Q/edit` |
| Intuit user license doc (Intuit-owned) | `https://docs.google.com/document/d/1RmlGoruS1bzSFgA-7ZYYr245ioVklFifVqvWfkO8tUc/edit` |
| ScribeHow (old process) | `https://scribehow.com/viewer/Submitting_a_Ticket_With_Sales_Tech_Ops__t8untHbNRsaQ_DgF3YveaA` |
| Loom walkthrough (old) | `https://www.loom.com/share/fc3158dec6c541228353ef082c681d7a` |
| RAC-764 (Mailchimp admin provisioning) | `https://linear.app/testbox/issue/RAC-764/provision-mailchimp-company-access-for-intuit-admins` |
| Coda Solutions Central | `https://coda.io/d/jfymaxsTtA` |
| Coda Integrations Central — Intuit | `https://coda.io/d/_dbd-guBL5H_/_su_H3Lto` |
| Coda — How to setup new account | `https://coda.io/d/_dbd-guBL5H_/_su0rdAbv` |
| Coda — Intuit Accounts | `https://coda.io/d/_dbd-guBL5H_/_su3MLjNf` |
| Coda — Activation failure cases | `https://coda.io/d/_dbd-guBL5H_/_suT1wr8` |
| TestBox App Q&A recording (Mar 17) | Drive: `Testbox App Q&A - 2026/03/17` |

---

## 7. ENVIRONMENT NAMES (Intuit)

| Environment Name | Type | Notes |
|-----------------|------|-------|
| IES Construction | Main demo | 8 entities, parent + 7 children |
| IES Construction SE | Seller Environment | For SEs |
| IES Construction PM | Project Manager | Keystone PM |
| IES Sales Alpha | Legacy | Sunsetting — some users still have access |
| IES Future Features | Product team | UAT/preview features |
| IES Events 2025 | Events/conferences | Juliana's team |
| UAT IES Construction | UAT testing | Limited users (should be ~15-20, not 410) |
| QBOA MM | Mid-Market (Accountant) | Single entity, mid_market@tbxofficial.com |
| QBOA Construction | Accountant version | Construction vertical |
| Non-Profit | NFP vertical | 3 entities |
| Manufacturing | Mfg vertical | 3 entities |
| Professional Services | Summit Consulting | 3 entities |
| QSP | Events + Sales | 2FA blocked |
| Mailchimp | Separate workspace | Under Intuit main company |

---

## 8. CODA DOCUMENTATION MAP

Where this knowledge lives in Coda (for manual updates — canvas pages can't be edited via API):

### Integrations Central (`bd-guBL5H_`)
Location: `Intuit` section (parent page `canvas-3ZQK_H3Lto`)

| Page | ID | What | Action Needed |
|------|----|------|---------------|
| **How to setup a new account** | `canvas-AAMV0rdAbv` | SOP for new customer provisioning (by Lucas, updated by Kat Jan 2026) | Add Kat's Apr 16 policy: Scenario A vs B, canned response link |
| **Intuit Accounts** | `canvas-KLKS3MLjNf` | Account credentials and access info (by Mason, updated by Kevin Sep 2024) | Review if access request process is documented here |
| **Quickbooks user activation failure cases** | `canvas-y_Rw4T1wr8` | Activation errors and troubleshooting | Add white screen Chrome extension fix, kledabyl case Apr 2026 |
| **Quickbooks Activities** | `canvas-GJeXYbTbE9` | Activity log / operations (by Lucas, updated Jan 2025) | Add access management activity log |
| **Quickbooks Health Checks** | `canvas-5HsvDSRwUg` | Health check procedures | No update needed |

**Best fit for Kat's new policy**: **"How to setup a new account"** page — it's the SOP for provisioning and Kat herself last edited it (Jan 27 2026). Add a new section at the top: "Access Request Triage (Apr 2026)" with Scenario A/B.

**Browser links**:
- Intuit section: https://coda.io/d/_dbd-guBL5H_/_su_H3Lto
- How to setup: https://coda.io/d/_dbd-guBL5H_/_su0rdAbv
- Intuit Accounts: https://coda.io/d/_dbd-guBL5H_/_su3MLjNf
- Activation failures: https://coda.io/d/_dbd-guBL5H_/_suT1wr8

### Solutions Central (`jfymaxsTtA`)

| Table | ID | Relevant Content |
|-------|----|-----------------|
| **QBO** | `grid-2yAT6muGXe` | Access prerequisites (Retool, Linear, Chrome, Tailscale) |
| **PHASE 1: ENVIRONMENT SETUP** | `grid-AjovHTVBiM` | Chrome CDP setup steps |
| **Customer Systems** | `grid-Z5y_vgOkce` | System dependencies |

---

## 9. CHANGELOG

| Date | Action | Detail | By |
|------|--------|--------|----|
| 2026-04-16 | CREATED | Playbook created from deep-sweep audit (60+ Slack msgs, 12 channels, 5 Coda tables, 6 Drive docs) | Thiago (via Claude) |
| 2026-04-16 | POLICY | Documented Kat's new access request policy: Scenario A (add env) vs Scenario B (redirect net-new to Google Doc link) | Kat → Thiago |
| 2026-04-16 | CORRECTION | Kat clarified: "We don't need to request access [to the doc], we just need to send them the link" | Kat |
| 2026-04-16 | TOOL | Created ACCESS_MANAGER v2 tool in `Tools/ACCESS_MANAGER/` — multi-channel scanner (13 channels + Help Tracker), 8 classifications, canned responses | Thiago (via Claude) |
| 2026-04-16 | AUDIT | Scanned 14 days across 17 channels: found 7 items (1 urgent Consolidated View, 2 pending RAC-764 + kledabyl, 2 watch items, 2 resolved) | Thiago (via Claude) |
| 2026-04-16 | CODA MAP | Mapped Intuit section in Integrations Central — identified "How to setup a new account" (`canvas-AAMV0rdAbv`) as best location for policy update | Thiago (via Claude) |

---

**Last Updated**: 2026-04-16
**Method**: Deep-sweep iterative audit (2 cycles, 65+ Slack msgs, 5 Coda tables, 6 Drive docs, Slack search across 17 channels, Coda API exploration across 4 docs)
