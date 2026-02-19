# Session: QBO Super Access System
**Date:** 2026-02-13
**Duration:** ~2h
**Type:** Architecture + Implementation

---

## Summary
Built the QBO Super Access System - a unified architecture for accessing QuickBooks Online through two engines (API + Playwright), with centralized credentials and intelligent auth flow.

## What Was Done

### 1. Repository Analysis (4 repos)
- `aallsbury/qb-time-mcp-server`: NOT useful (read-only, TSheets API, not QBO)
- `consolibyte/quickbooks-php`: Full CRUD 30+ entities, PHP. No Projects.
- `ruckus/quickbooks-ruby`: Full CRUD ~30 entities, Ruby. No Projects.
- `intuit/quickbooks-online-mcp-server`: Official, 55 tools, 11 entities. No Projects/Time/Reports.
- `thiagotbx123/QBO_HEALTH_CHECKER`: Methodology/playbook repo, not executable code.

### 2. Deep Investigation of Existing Tools
Discovered critical issues:
- MCP Server: built (dist/ exists) but Claude Desktop config pointed to WRONG PATH
- qb-oauth-manager: all 3 companies had null tokens (never authorized)
- qb-construction and qb-terra: wrong realm IDs + wrong environment (sandbox vs production)
- python-quickbooks: not installed
- All QBO access was via Playwright browser automation only

### 3. QBO Credentials Store (Phase 0)
Created `knowledge-base/access/QBO_CREDENTIALS.json`:
- 5 accounts with email, password, TOTP secret, companies, realm IDs
- Auth protocol: ask email → lookup → auto-login → if fail → ask user → update
- 20+ companies/entities mapped with CIDs

### 4. MCP Server Path Fix (Phase 0)
- Fixed path in 8 MCP servers: `quickbooks-online-mcp-server` → `Integrations/quickbooks-online-mcp-server`
- Fixed construction realmId: `9341453454021291` → `9341454156620895`
- Fixed terra realmId: `9341453454021291` → `9341454156620204`
- Fixed both from sandbox → production
- Fixed path in qb-oauth-manager server.js

### 5. python-quickbooks Installation (Phase 1)
- Installed v0.9.12 via pip
- 34 entities available (vs 11 in MCP server)
- Includes: Payment, Deposit, SalesReceipt, CreditMemo, Transfer, TimeActivity, Class, Department, etc.

### 6. QBO Router (Phase 3 Foundation)
Created `knowledge-base/access/QBO_ROUTER.md`:
- Entity routing table: 11 API+MCP, 17 API-only, 12 Playwright-only
- Operation recipes for common tasks
- Auth flow documentation
- Learning log (grows with each job)
- python-quickbooks setup code

### 7. Evidence Collection Playbook
Created `knowledge-base/EVIDENCE_COLLECTION_PLAYBOOK.md` (~400 lines):
- Full pipeline: Login → Navigate → Screenshot → Upload → Group → XLSX
- Google Drive API patterns with code
- PIL/Pillow techniques
- QBO navigation patterns
- Reusable scripts inventory
- 15+ lessons learned from Winter Release, UAT, QSP, PRINTS SETAS

### 8. Git
- Commit `6f592b8`: 811 lines added across 6 files
- Push BLOCKED: GitHub Secret Scanning detected Linear API keys in older commit `300bd23`
- Need user to unblock via GitHub URLs

## Files Created/Modified

### Created
- `knowledge-base/access/QBO_CREDENTIALS.json` - Credentials store
- `knowledge-base/access/QBO_ROUTER.md` - Operation router
- `knowledge-base/EVIDENCE_COLLECTION_PLAYBOOK.md` - Evidence playbook
- `.gitignore` - Exclude .playwright-profile, __pycache__, etc.

### Modified
- `knowledge-base/INDEX.md` - Added ACC-001, ACC-002, EVD-001 entries
- `.claude/memory.md` - Added QSP entries
- Claude Desktop `claude_desktop_config.json` - Fixed 8 MCP paths + 2 realm IDs
- `qb-oauth-manager/server.js` - Fixed MCP server path
- `qb-oauth-manager/config.json` - Added mcpServerPath

### System
- Installed: python-quickbooks 0.9.12 (+ cryptography, pyjwt, intuit-oauth, cffi, pycparser, enum-compat)

## Key Architecture Decision

Two-engine hybrid approach:
```
API (python-quickbooks/MCP) → 34 entities, fast, reliable, bulk operations
Playwright (browser)        → Projects, Budgets, Settings, IES-specific, evidence
Router                      → Decides which engine per operation
Credentials                 → Single JSON, auto-lookup by email
```

## Pending
1. Push to GitHub (blocked by secrets in commit 300bd23)
2. Authorize OAuth tokens via qb-oauth-manager (start server, click authorize per company)
3. Test API connection with real query
4. Build out more recipes in router as we execute jobs

## Learnings
1. Intuit MCP server only implements 11/34+ available QBO API entities
2. python-quickbooks covers 34 entities including Payment, Deposit, TimeActivity
3. Projects require Premium API (GraphQL, Silver+ tier) - Playwright only for us
4. Budgets have ZERO API - Playwright is the only option
5. QBO refresh tokens expire in 100 days - need regular re-authorization
6. GitHub Secret Scanning blocks push if ANY commit in history has secrets
