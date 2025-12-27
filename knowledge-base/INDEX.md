# TestBox QBO/WFS Knowledge Base

## Purpose
Central knowledge repository for QuickBooks Online, WFS, and TestBox customer support context.
This is the brain of the QBO Support Bot - it searches here FIRST before going to the web.

## Structure

```
knowledge-base/
├── INDEX.md              <- This file (catalog of all sources)
├── qbo/                  <- QuickBooks Online product knowledge
│   ├── QBO_DEEP_MASTER_v1.txt   <- Main knowledge file (11k+ lines)
│   └── QBO_MASTER.md     <- Quick reference
├── wfs/                  <- Workforce Solutions context
├── slack-cortex/         <- [NEW] Inteligencia de comunicacao Slack
├── drive-cortex/         <- [NEW] Inventario de documentos Drive
├── strategic-cortex/     <- [NEW] Visao consolidada estrategica
├── cortex/               <- CORTEX collection layer docs
├── slack-threads/        <- Extracted learnings from Slack
├── meetings/             <- Meeting notes and decisions
├── access/               <- Environments, logins, credentials info
└── governance/           <- MFA, recovery, shared access rules
```

## Adding New Knowledge

### Option 1: Add to existing category
Drop `.txt` or `.md` files into the appropriate folder. The bot will automatically pick them up.

### Option 2: Create new category
Create a new folder and add files. Update this INDEX.md to document it.

### Best Practices
- Use clear filenames that describe the content
- Prefer `.txt` or `.md` format
- Include dates when relevant (e.g., `2024-12-meeting-notes.md`)
- For Slack threads, include the channel and date

## Source Catalog

| ID | Date | Type | Source | Summary | File |
|----|------|------|--------|---------|------|
| QBO-001 | 2025-12-02 | Master Doc | ChatGPT Export | Full QBO/TestBox/Intuit context | qbo/QBO_DEEP_MASTER_v1.txt |
| WFS-001 | 2025-12-19 | Cortex | Claude Session | WFS project cortex - stakeholders, timeline, demos | wfs/WFS_CORTEX_v1.md |
| WFS-002 | 2025-12-19 | UI Map | Playwright | GoQuick Alpha Retail - payroll, employees, time | wfs/WFS_ALPHA_RETAIL_MAP.md |
| WFS-003 | 2025-12-19 | UI Map | Playwright | Keystone Construction - PTO, celebrations, job costing | wfs/WFS_KEYSTONE_MAP.md |
| WFS-004 | 2025-12-19 | Summary | Playwright | Comparativo das duas empresas para demos WFS | wfs/WFS_MAPPING_SUMMARY.md |
| WFS-005 | 2025-12-19 | Navigation | Playwright | Mapa completo de rotas QBO + Mineral para navegacao autonoma | wfs/WFS_NAVIGATION_MAP.md |
| WFS-006 | 2025-12-19 | Strategy | Analysis | POV/SOW Framework - estrutura completa para atuacao WFS | wfs/WFS_POV_SOW_FRAMEWORK.md |
| SLACK-001 | 2025-12-27 | Cortex | Slack MCP | Executive snapshot - comunicacao 10 canais | slack-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md |
| SLACK-002 | 2025-12-27 | Cortex | Slack MCP | Knowledge base JSON - mensagens indexadas | slack-cortex/OUTPUT_B_KNOWLEDGE_BASE.json |
| SLACK-003 | 2025-12-27 | Cortex | Slack MCP | Keyword map - termos e queries | slack-cortex/OUTPUT_C_KEYWORD_MAP.md |
| SLACK-004 | 2025-12-27 | Cortex | Slack MCP | Delta summary - mudancas 7 dias | slack-cortex/OUTPUT_D_DELTA_SUMMARY.md |
| DRIVE-001 | 2025-12-27 | Cortex | DriveCollector | Executive snapshot - 1,442 arquivos | drive-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md |
| DRIVE-002 | 2025-12-27 | Cortex | DriveCollector | Knowledge base JSON - inventario | drive-cortex/OUTPUT_B_KNOWLEDGE_BASE.json |
| DRIVE-003 | 2025-12-27 | Cortex | DriveCollector | Keyword map - termos Drive | drive-cortex/OUTPUT_C_KEYWORD_MAP.md |
| DRIVE-004 | 2025-12-27 | Cortex | DriveCollector | Delta summary - mudancas 30 dias | drive-cortex/OUTPUT_D_DELTA_SUMMARY.md |
| STRAT-001 | 2025-12-27 | Cortex | Consolidated | Executive snapshot - status todos temas | strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md |
| STRAT-002 | 2025-12-27 | Cortex | Consolidated | Strategic map - conexoes e arquitetura | strategic-cortex/OUTPUT_B_STRATEGIC_MAP.md |
| STRAT-003 | 2025-12-27 | Cortex | Consolidated | Knowledge base JSON completo - 847 items | strategic-cortex/OUTPUT_C_KNOWLEDGE_BASE.json |
| STRAT-004 | 2025-12-27 | Cortex | Consolidated | Keyword map + Linear recipes | strategic-cortex/OUTPUT_D_KEYWORD_MAP_LINEAR_RECIPES.md |
| STRAT-005 | 2025-12-27 | Cortex | Consolidated | Delta summary - 30 dias vs anterior | strategic-cortex/OUTPUT_E_DELTA_SUMMARY.md |

## Quick Reference

### Key Projects
- **TCO (Traction Control Outfitters)**: Flagship QBO Advanced simulation
  - Parent + 3 children: Apex Tire, Global Tread, RoadReady
- **Construction Sales**: Desktop parity, IES construction features
- **Construction Events**: Stadium/project events, manual eliminations

### Key Contacts
- Thiago: Technical Solutions Architect, Data Architect
- Kat: UAT coordination
- Sam: Engineering liaison

### Environments
- TCO multi-entity
- Construction Sales
- Construction Events

### Cortex System (NEW 2025-12-27)
Three-layer intelligence system for strategic visibility:
- **Slack Cortex**: Communication intelligence from 10 channels
- **Drive Cortex**: Document inventory from 20,426 files (1,926 relevant)
- **Strategic Cortex**: Consolidated view with 5 outputs (A-E)

See `strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md` for current status.

---
Last updated: 2025-12-27
