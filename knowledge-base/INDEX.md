# TestBox QBO/WFS Knowledge Base

## Purpose
Central knowledge repository for QuickBooks Online, WFS, and TestBox customer support context.

## Structure (Verified 2026-04-13)

```
knowledge-base/
├── INDEX.md                    <- This file (catalog of all sources)
├── qbo/                        <- QuickBooks Online product knowledge
│   ├── QBO_MASTER.md           <- Quick reference
│   ├── DAILY_HEALTH_CHECK.md   <- Daily check procedures
│   ├── FEATURE_SURFACE_MAP.md  <- Feature surface mapping
│   ├── QBO_CORTEX_v1.md        <- QBO cortex v1
│   ├── QBO_CORTEX_v2.md        <- QBO cortex v2
│   └── qbo_urls_reference.md   <- URL reference (updated Mar 2026)
├── wfs/                        <- Workforce Solutions context (Dec 2025 — NEEDS REFRESH)
│   ├── WFS_CORTEX_v1.md        <- WFS project cortex
│   ├── WFS_ALPHA_RETAIL_MAP.md <- GoQuick Alpha Retail map
│   ├── WFS_KEYSTONE_MAP.md     <- Keystone Construction WFS map
│   ├── WFS_MAPPING_SUMMARY.md  <- Summary of both companies
│   ├── WFS_NAVIGATION_MAP.md   <- Route navigation map
│   ├── WFS_MINERAL_HR_MAP.md   <- Mineral HR mapping
│   ├── WFS_EXPLORATION_COMPLETE.md
│   ├── WFS_POV_SOW_FRAMEWORK.md
│   ├── WFS_SESSION_CONSOLIDATION_20251219.md
│   ├── WFS_SLACK_INTELLIGENCE.md
│   └── WFS_STRATEGIC_INSIGHTS.md
├── slack-cortex/               <- Slack intelligence
│   ├── OUTPUT_A-D (Dec 2025)   <- STALE — baseline snapshots
│   ├── INTUIT_DEEP_LEARN_INTELLIGENCE.md  <- Mar 2026
│   └── INTUIT_INTELLIGENCE_2026-04-13.md  <- CURRENT — deep refresh
├── drive-cortex/               <- Drive inventory (Dec 2025 — STALE)
│   ├── full_inventory.json     <- 1.1MB inventory
│   └── OUTPUT_A-D (Dec 2025)
├── strategic-cortex/           <- Consolidated strategic view
│   ├── OUTPUT_A-E (Dec 2025)   <- STALE — baseline
│   └── OUTPUT_A_EXECUTIVE_SNAPSHOT_2026-03-11.md <- Refresh Mar 11
├── sweep-learnings/            <- Post-sweep analysis (33 reports, CURRENT)
│   ├── CHANGELOG.md            <- Sweep evolution log
│   └── {dataset}_{date}.md     <- Per-dataset reports
├── access/                     <- Credentials & access (SENSITIVE)
│   ├── QBO_CREDENTIALS.json    <- Single source of truth
│   ├── QBO_ROUTER.md           <- Operation→Engine mapping
│   ├── TESTBOX_ACCOUNTS.md     <- All account details
│   ├── retool_production_export.csv
│   └── retool_staging_export.csv
├── cortex/                     <- CORTEX collection layer docs
│   └── CAMADA_COLETA.md
├── CONTEXT_RECOVERY.md
├── EVIDENCE_COLLECTION_PLAYBOOK.md  <- Evidence pipeline guide (Feb 2026)
├── IES_FEBRUARY_RELEASE_*.md   <- February release analysis (2 files)
├── INGESTION_3_GATES.md        <- Gate process for ingestion
├── INTEL_IES_RELEASE_READINESS_2026-01-27.md
├── TREINAMENTO_COLETADO.md
├── UAT_KEYSTONE_CONFIDENCE_ANALYSIS.md
├── UAT_SALES_PRINTS_KNOWLEDGE.md
└── UNIVERSAL_VALIDATION_FRAMEWORK.md  <- Framework (Mar 2026)
```

**NOTE:** INDEX previously referenced `slack-threads/`, `meetings/`, `governance/` folders — these never existed on disk and have been removed from this index.

**NOTE:** `qbo/QBO_DEEP_MASTER_v1.txt` referenced as main knowledge file but not found in `qbo/` folder. A copy exists at the intuit-boom project root as `QBO_DEEP_MASTER_v1 (1).txt`.

## Source Catalog

| ID | Date | Type | Source | Summary | File |
|----|------|------|--------|---------|------|
| QBO-001 | 2025-12-02 | Master Doc | ChatGPT Export | Full QBO/TestBox/Intuit context | (root)/QBO_DEEP_MASTER_v1 (1).txt |
| WFS-001 | 2025-12-19 | Cortex | Claude Session | WFS project cortex | wfs/WFS_CORTEX_v1.md |
| WFS-002–006 | 2025-12-19 | Maps | Playwright | WFS UI maps and navigation | wfs/ |
| SLACK-001–004 | 2025-12-27 | Cortex | Slack MCP | Slack intelligence (STALE) | slack-cortex/OUTPUT_A–D |
| DRIVE-001–004 | 2025-12-27 | Cortex | DriveCollector | Drive inventory (STALE) | drive-cortex/ |
| STRAT-001–005 | 2025-12-27 | Cortex | Consolidated | Strategic view (STALE except A) | strategic-cortex/ |
| DL-001 | 2026-03-04 | Deep-Learn | Slack API | 5 canais Intuit (11,202 msgs) | slack-cortex/INTUIT_DEEP_LEARN_INTELLIGENCE.md |
| **DL-002** | **2026-04-13** | **Deep-Learn** | **Slack API** | **8-query deep refresh: org, releases, WFS, datasets** | **slack-cortex/INTUIT_INTELLIGENCE_2026-04-13.md** |
| ACC-001 | 2026-02-13 | Credentials | Claude Session | All QBO credentials | access/QBO_CREDENTIALS.json |
| ACC-002 | 2026-02-13 | Router | Claude Session | Operation→Engine mapping | access/QBO_ROUTER.md |
| EVD-001 | 2026-02-13 | Playbook | Claude Session | Evidence collection pipeline | EVIDENCE_COLLECTION_PLAYBOOK.md |

## Freshness Summary

| Area | Status | Last Updated |
|------|--------|--------------|
| sweep-learnings/ | CURRENT | Apr 2, 2026 |
| slack-cortex (DL-002) | CURRENT | Apr 13, 2026 |
| memory.md | CURRENT | Apr 13, 2026 |
| scripts/ingestion/ | CURRENT | Apr 13, 2026 |
| access/ credentials | OK | Mar 10, 2026 |
| strategic-cortex/ | STALE | Dec 2025 (one OUTPUT_A Mar 11) |
| drive-cortex/ | STALE | Dec 2025 |
| slack-cortex/ OUTPUTs | STALE | Dec 2025 |
| wfs/ | STALE | Dec 2025 |
| INDEX.md | REFRESHED | Apr 13, 2026 |

---
Last updated: 2026-04-13
