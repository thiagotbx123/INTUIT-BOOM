# Session: IC Account Mapping Investigation
> Date: 2026-02-23
> Duration: ~2 hours (continued from previous context)
> Entity: Consolidated View / Keystone Construction (Par)

---

## Objective
Investigate and fix IC (Intercompany) Account Mapping configuration for Parent-BlueCraft and Parent-Terra pairs.

## Tasks Completed

### Task #17: Verify Calculated Field (COMPLETED - previous session)
- Created calculated field in Balance Sheet report
- Evidence: `calculated_field_created.png`, `calculated_field_in_report.png`

### Task #18: Fix Shared COA Account 2030 - Add Terra (COMPLETED)
- Navigated to `/app/sharedcoa` on Consolidated View
- Found account 2030 "Due to Keystone BlueCraft" only shared with Parent
- Added Terra to shared companies list
- Evidence: `shared_coa_2030_add_terra.png`, `shared_coa_2030_terra_saved.png`

### Task #19: IC Account Mapping Investigation (COMPLETED - No Change Needed)
- **URL discovered**: `/app/ic-accountdefaults` (only accessible from CV homepage SHORTCUTS)
- **Finding**: Only 2 company pairs exist (Parent-BlueCraft, Parent-Terra)
- **No direct BlueCraft-Terra pair exists** - IES routes child-to-child IC through parent

#### Parent-BlueCraft Mapping (CORRECT):
| Position | Account |
|----------|---------|
| Due to company 2 | Due to Keystone BlueCraft |
| Due from company 1 | Due from Keystone Construction |
| Due from company 2 | Due from Keystone BlueCraft |
| Due to company 1 | Due to Keystone Construction |

#### Parent-Terra Mapping (FUNCTIONAL):
| Position | Account |
|----------|---------|
| Due to company 2 | Due to Keystone Terra |
| Due from company 1 | **Terra Intercompany Receivable** |
| Due from company 2 | Due from Keystone Terra |
| Due to company 1 | Due to Keystone Construction |

- "Terra Intercompany Receivable" is functionally valid (receivable asset on Terra's books)
- Different naming convention vs BlueCraft's "Due from Keystone Construction"
- Account "Due from Keystone Construction" does NOT exist in Terra's COA
- No "Intercompany Payables" found in any current mapping field (task description was stale)
- **Decision**: No change made - mapping is functionally correct

### Task #20: Evidence Capture (COMPLETED)
- 8 screenshots captured
- Multi-page PDF: `EvidencePack/ic_configuration_evidence.pdf` (8 pages, 1.6 MB)

## Key Discoveries

### Navigation to IC Account Mapping
- **URL**: `/app/ic-accountdefaults`
- **Access**: ONLY from CV Homepage > SHORTCUTS section > "Intercompany account mapping"
- Cannot be found in: Settings gear, Account and settings, Advanced tab, Search
- Direct URL navigation may 404 without proper CV context

### CV Homepage SHORTCUTS Section
Available shortcuts on Consolidated View homepage:
1. Intercompany account mapping (`/app/ic-accountdefaults`)
2. Intercompany elimination accounts
3. Manual eliminations
4. Org chart
5. Run reports via Spreadsheet Sync

### Company Switcher
- **USE**: Header dropdown (company name with chevron)
- **DO NOT USE**: Settings > "Switch company" (causes logout/redirect to accounts.intuit.com)

### IC Account Naming Patterns
Two conventions in use across entities:
1. `"Due to/from {Entity}"` - BlueCraft, EcoCraft, Stonecraft, IronCraft, Terra (payable/receivable)
2. `"{Entity} Intercompany Receivable"` - Keystone, Terra, Volt, BlueCraft (legacy naming)

### Available IC Receivable Accounts on Parent COA
- Keystone Intercompany Receivable
- Terra Intercompany Receivable
- Volt Intercompany Receivable
- BlueCraft Intercompany Receivable
- Due from EcoCraft, Due from Stonecraft, Due from IronCraft

## Evidence Files
| File | Content |
|------|---------|
| `ic_mapping_01_overview.png` | IC Mapping dialog - 2 pairs collapsed |
| `ic_mapping_02_bluecraft.png` | Parent-BlueCraft expanded with 4 accounts |
| `ic_mapping_03_terra.png` | Parent-Terra expanded with 4 accounts |
| `ic_mapping_04_cv_homepage.png` | CV Homepage with SHORTCUTS section |
| `ic_mapping_before_fix.png` | Terra mapping before investigation |
| `shared_coa_2030_add_terra.png` | Adding Terra to Shared COA 2030 |
| `shared_coa_2030_terra_saved.png` | Terra saved in Shared COA 2030 |
| `calculated_field_created.png` | Calculated field in Customize panel |
| `calculated_field_in_report.png` | Calculated field in Balance Sheet |
| `EvidencePack/ic_configuration_evidence.pdf` | Consolidated 8-page PDF |

## QBO Router Updates
- Added `/app/ic-accountdefaults` URL and navigation recipe
- Added CV Homepage SHORTCUTS as navigation method
- Warning: Settings > "Switch company" causes logout
