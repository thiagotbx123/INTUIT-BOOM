# Sweep Evolution Changelog

All changes follow the Protocolo Pos-Sweep: evidence-based, additive-only, one-at-a-time.

---

## 2026-04-15 — SWEEP INFRASTRUCTURE EVOLUTION v9.2 (Dual Engine)

### Context
Construction-clone sweep (Apr 15) revealed that cursor-ide-browser CANNOT set QBO React amount inputs, but user-playwright CAN via `keyboard.type({delay: 50})`. Also discovered that IES entity switcher works in Playwright but not cursor-ide-browser, and that SMS MFA is environment-wide (not just Parent). These learnings demanded infrastructure changes.

### EVO-4: SWEEP_ACTIVATION.md template — Dual Engine Browser Automation
- **Type**: instruction refined
- **File**: `sweep_engine.py` (SWEEP_ACTIVATION template, lines ~797-830)
- **Evidence**: construction-clone_2026-04-15_v2.md — GaleGuardian $140K expense created via user-playwright `keyboard.type` after cursor-ide-browser failed. TidalWave $25K invoice also created via Playwright.
- **What changed**: New "BROWSER AUTOMATION — DUAL ENGINE (v9.2)" section replaces the old single-engine block. Defines routing table: cursor-ide-browser for read/nav/text, user-playwright for amounts/entity switch/complex forms. Adds Project vs Sub-Customer warning. Documents SMS MFA as BLOCKED on ALL entities.
- **Before**: Single "BROWSER AUTOMATION" section with only cursor-ide-browser tools. Financial fixes marked as "DOCUMENTAR mas NAO corrigir".
- **Risk**: Low — additive, no behavior removed. Agents that don't have user-playwright will still use cursor-ide-browser for everything non-financial.
- **Rollback**: Revert the BROWSER AUTOMATION section to single-engine block.

### EVO-5: SWEEP_ORDER.md template — Dual Engine + Entity Switch + FIX-18/19
- **Type**: instruction refined + protocols added
- **Files**: `sweep_engine.py` (SWEEP_ORDER template, multiple sections)
- **Evidence**: Same as EVO-4. Entity switch URL method works ~70%, Playwright header dropdown works 100%.
- **Changes**:
  - REGRA #2: Updated from single "server=playwright" to "DUAL ENGINE v9.2" with routing guidance
  - REGRA #5B: Updated to cover both engines for keepalive
  - LOGIN section: Dual-engine procedure (cursor-ide-browser primary, user-playwright on-demand)
  - Entity switch block: Two methods (URL redirect + IES header dropdown via Playwright)
  - Playwright cheatsheet: Dual engine with amount input examples and beforeunload handling
  - FIX-01: Margin abort threshold changed from fixed 50% to sector-specific ceilings
  - FIX-18 (NEW): Project margin fix via user-playwright (keyboard.type + delay)
  - FIX-19 (NEW): Duplicate cleanup protocol (More actions → Delete + dialog handling)
- **Before**: Single "server=playwright" everywhere, no amount input capability, no FIX-18/19.
- **Risk**: Medium — login procedure changed from Playwright-only to dual. Agents need to know when to switch. Mitigated by clear routing table.
- **Rollback**: Revert entity switch block, login section, cheatsheet, and FIX protocols to pre-v9.2.

### EVO-6: sweep_checks.py — New sub_checks D09.11, D09.12, D12.7 + FIX tier updates
- **Type**: checks added (ADDITIVE)
- **File**: `sweep_checks.py`
- **Evidence**: construction-clone_2026-04-15_v2.md — GaleGuardian 92.9% margin (should be 3-15% for construction). TidalWave $25K invoice didn't appear in Project detail view.
- **Changes**:
  - D09.11: Project Margin Realism Auto-Fix — flags margins >sector ceiling, provides FIX-18 auto-fix protocol with user-playwright instructions
  - D09.12: Project vs Sub-Customer Income Attribution — documents that invoicing a sub-customer ≠ attributing to Project. Requires line-item project assignment.
  - D12.7: SMS MFA Detection — instructs agent to detect SMS MFA and mark as environment-wide BLOCKED (don't retry on other entities)
  - FIX_TIERS["fix_and_report"]: Added expense creation, invoice creation, duplicate cleanup
  - FIX_TIERS["never_fix"]: Updated "Company settings" to clarify SMS MFA, added "Systemic inflation"
- **Before**: D09 had 10 sub_checks, D12 had 6 sub_checks. No SMS MFA awareness. Financial fixes classified as "never_fix".
- **Risk**: Low — all additive. No existing check IDs modified.
- **Rollback**: Remove D09.11, D09.12, D12.7. Revert FIX_TIERS items.

### EVO-7: SWEEP_PLAYBOOK.md — UI Automation Limitations corrected
- **Type**: documentation corrected
- **File**: `SWEEP_PLAYBOOK.md` (lines ~40-56)
- **Evidence**: construction-clone_2026-04-15_v2.md — amounts now work via user-playwright.
- **Changes**:
  - "LIMITACOES CRITICAS DE UI AUTOMATION" table completely rewritten with 3-column format (cursor-ide-browser / user-playwright / QBO API)
  - Invoice/JE/Expense amounts marked as FUNCIONA for user-playwright (were "NAO FUNCIONA")
  - Entity switch marked as FUNCIONA for user-playwright
  - Company Info edits marked as BLOCKED SMS MFA for both engines
  - Added step-by-step procedure for Playwright amount input
  - Added entity switch procedure
  - Tools table updated to dual-engine format
- **Before**: Single-engine table showing amounts as "NAO FUNCIONA". Agents instructed to "USE API" for all financial inputs.
- **Risk**: Low — corrects documentation to match actual capability. Agents may now attempt amount fixes that previously would have been skipped.
- **Rollback**: Revert LIMITACOES CRITICAS section and tools table.

### EVO-8: configs/checks.json — Synced with sweep_checks.py
- **Type**: config synced
- **File**: `configs/checks.json`
- **Changes**: Version bumped to 9.2 "Dual Engine + Playwright Breakthroughs". D09.11, D09.12, D12.7 added. D09 fix_actions updated. D12 fix_actions updated with SMS MFA guidance.
- **Risk**: None — mirrors sweep_checks.py changes.
- **Rollback**: Revert version, remove new sub_checks.

### Validation
- `python -c "import sweep_checks"` → OK (146 checks)
- `python -c "import sweep_engine"` → OK
- `python -c "import app"` → OK
- `python -c "import data; import config; import settings"` → OK
- `configs/checks.json` → valid JSON, D09=12 sub_checks, D12=7 sub_checks

---

## 2026-04-15 — construction-clone full sweep v9.1 (Pass 4 — FINAL)

### Fixes Applied (8 total)
- **FIXED**: 3 entity names (Canopy, Ecocraft, Volt) — "KeyStone" → "Keystone" casing
- **FIXED**: Customer address ZIP 92129 → 94043-1126 (workaround: type "Cali" in State combobox)
- **FIXED**: Project "Intuit Dome 2026" renamed → "Civic Arena — Structural Phase 2"
- **FIXED**: GaleGuardian margin 92.9% → 25.2% — added $140K expense ($85K Contractors + $55K Job Supplies) via **Playwright MCP** `keyboard.type({delay:50})`
- **FIXED**: TidalWave $0 income — created $25K invoice (TBX-2026-45166I) + received payment via **Playwright MCP**
- **FIXED**: Duplicate TidalWave invoice cleaned up — deleted TBX-2026-45165I via "More actions → Delete"

### Breakthroughs (Playwright MCP)
- **BREAKTHROUGH**: QBO React amount inputs **WORK** with Playwright MCP `page.keyboard.type(value, {delay: 50})`. cursor-ide-browser's `browser_fill`/`browser_type` still fail. **Use Playwright for ALL financial inputs going forward.**
- **BREAKTHROUGH**: IES entity switcher **WORKS** in Playwright MCP. `menuitem` elements are clickable. cursor-ide-browser still blocked by CSS overlay.
- **CORRECTED**: SMS MFA blocks Company Info edits on **ALL entities** (not just Parent). Confirmed by testing BlueCraft child entity.

### Discoveries
- **QBO Project ≠ Sub-customer**: Invoicing "Customer:SubCustomer" does NOT attribute income to QBO Project. Needs line-item project assignment.
- **beforeunload dialogs**: QBO fires on invoice save. Handle with `browser_handle_dialog(accept: true)`.
- **DOCUMENTED**: 6 IES URLs that 404 (/chart-of-accounts, /products, /inventory, /inventoryoverview, /salesreceipts, /company, /mhome)

### Report
- **REPORT**: construction-clone_2026-04-15_v2.md — 12 sections, 1 manual action item remaining (Website SMS MFA)
- **Score**: 9.0/10 (was 8.5) | **Realism**: 88/100 (was 82) | **Fixes**: 8 applied, 1 blocked

---

## 2026-04-02 (Post construction_2026-04-02.md analysis)

### EVO-1: FIX PROTOCOL added to SWEEP_ACTIVATION.md template
- **Type**: instruction added
- **File**: `sweep_engine.py` (SWEEP_ACTIVATION template)
- **Evidence**: `construction_2026-04-02.md` — "Fixes Applied: 0" despite 10+ CS3 violations found (Alan Somebody, Test Testerson, Contract A/B/C, Test 1/2/3, etc.)
- **What changed**: New "FIX PROTOCOL" section in the activation file explicitly tells the agent to correct CS3/CS2 violations immediately upon detection. Distinguishes fixable (CS3/CS2 → correct now) from financial (document only).
- **Before**: Agent detected problems but only reported them.
- **Risk**: Low — only adds instructions, does not change existing logic.
- **Rollback**: Remove the "FIX PROTOCOL" and "DADOS MINIMOS" sections from the activation template in `sweep_engine.py`.

### EVO-2: Chunked reading of SWEEP_PLAYBOOK.md
- **Type**: instruction refined
- **File**: `sweep_engine.py` (SWEEP_ACTIVATION template, EXECUCAO section)
- **Evidence**: `SWEEP_SESSION_LOG_2026-04-02.md` — agent attempted to read full 119KB playbook, hit context limits. Many screens got shallow "Navegado" coverage due to context exhaustion.
- **What changed**: EXECUCAO step 1 now explicitly says "NAO ler inteiro" and provides a line-number index (TELA 1=131, TELA 2=198, etc.) with `limit:70` per section.
- **Before**: "Ler SWEEP_PLAYBOOK.md (roteiro completo tela-a-tela)" — no guidance on chunking.
- **Risk**: None — existing playbook file is unchanged.
- **Rollback**: Revert EXECUCAO step 1 to original wording.

### EVO-3: Minimum data requirements for all screens
- **Type**: check added
- **File**: `sweep_engine.py` (SWEEP_ACTIVATION template)
- **Evidence**: `SWEEP_SESSION_LOG_2026-04-02.md` — screens T22-T46 had only "Navegado" as output with zero data points. The report marked them OK but provided no evidence.
- **What changed**: New "DADOS MINIMOS POR TELA" section requires 4 data points per screen: URL final, count of items, CS3 scan, and status code (DONE/EMPTY/404/BLOCKED). Includes good/bad examples.
- **Before**: No minimum data requirements — agent could mark any screen as done with just "Navegado".
- **Risk**: Low — may slightly increase sweep time per screen (1 extra snapshot). Worth the data quality gain.
- **Rollback**: Remove the "DADOS MINIMOS POR TELA" section from the activation template.
