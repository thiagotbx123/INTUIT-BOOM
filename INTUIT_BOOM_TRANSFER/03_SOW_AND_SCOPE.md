# INTUIT-BOOM - Escopo, Releases e WFS

---

## ESCOPO GERAL DO PROJETO

### Objetivo Principal
Validacao, geracao de dados e manutencao de ambientes demo QuickBooks Online (QBO) para a equipe de vendas da Intuit, cobrindo multiplos verticais e releases.

### Verticais/Ambientes
| Vertical | Dataset | Status | Prioridade |
|----------|---------|--------|------------|
| **TCO (Tire Industry)** | Multi-entity, 5 companies | PRODUCTION | PRINCIPAL |
| **Construction** | 8 companies (Keystone) | PRODUCTION | ALTA |
| **Canada** | French/English, expansion | ATIVO | MEDIA |
| **Manufacturing** | Parcial | PARCIAL | BAIXA |
| **Nonprofit** | Parcial | PARCIAL | BAIXA |
| **Professional Services** | Parcial | PARCIAL | BAIXA |
| **WFS (Workforce)** | GoCo + QB Payroll | BLOQUEADO | ALTA (futuro) |

---

## RELEASES INTUIT

### Fall Release FY26
- **Status:** ENTREGUE (11/20/2025)
- **Escopo:** Features QBO para todos verticais
- **Resultado:** TCO/Construction validados, Manufacturing/Nonprofit 95%
- **Reclassificado:** Process improvement (nao delivery)

### Winter Release FY26
- **Status:** VALIDADO
- **Features:** 50 total (25 TCO + 25 Construction)
- **Resultado:** 46 PASS, 2 PARTIAL, 2 N/A
- **Evidence:** 30+ screenshots, Drive hyperlinks, tracker Excel
- **Early Access:** 2026-02-04
- **Categorias:** AI Agents (8), Reporting (7), Dimensions (4), Workflow (1), Migration (3), Construction (2), Payroll (4)

### February/IES Release FY26
- **Status:** Em preparacao
- **Timeline:** Feb 3/4 feature flags, Feb 5 Keystone staging
- **Approach:** Pre-build foundation data ANTES do flag
- **Owner analise:** Alexandra Lacerda

---

## WFS (WORKFORCE SOLUTIONS) - PROJETO SEPARADO

### O que e
- Intuit Workforce Solutions = plataforma HCM para PMEs
- Combina GoCo + QuickBooks Payroll
- Powered by MineralHR

### Escopo TestBox
| # | Story | Descricao |
|---|-------|-----------|
| 1 | Unified PTO | Employee > Manager > Payroll Admin flow |
| 2 | Magic Docs | AI document generation + e-signature |
| 3 | Hire to Fire | Lifecycle completo |
| 4 | Job Costing | Construction integration |

### Timeline
| Milestone | Data | Status |
|-----------|------|--------|
| Alpha | Dez 2025 | DONE (~100 customers) |
| SOW Deadline | 12/19/2025 | ATRASADO |
| Environment Decision | Jan 2026 | AGUARDANDO |
| Beta | Fev 2026 | Planejado |
| GA | Mai 2026 | Planejado |

### Bloqueio Principal
**P0: Intuit precisa decidir se WFS usa environment existente (TCO/Keystone) ou novo.**
- Decision owner: Christina Duarte
- Documento: `QBO-WFS/docs/WFS_ENVIRONMENT_STRATEGY_PROS_CONS_V0.md`
- Recomendacao: Hybrid Approach (new env phase 1, integrate phase 3)

---

## INGESTION PIPELINE (ESTADO ATUAL)

### CSVs Prontos (2026-02-05)
| Arquivo | Entities | IDs | Status |
|---------|----------|-----|--------|
| INGESTION_VENDORS_NEW.csv | 20 | 34-53 | PRONTO |
| INGESTION_CUSTOMERS_NEW.csv | 25 | 51-75 | PRONTO |
| INGESTION_BILLS.csv | 332 | 105-436 | PRONTO |
| INGESTION_INVOICES.csv | 243 | 2460-2702 | PRONTO |
| PLA-3261_TIME_ENTRIES_FINAL.csv | 3,972 | - | PRONTO |

### Regras de Ingestion
1. Ordem FK: Vendors/Customers -> Bills/Invoices -> Time Entries
2. IDs sequenciais: MAX(existing) + 1
3. FK type = PK type da tabela referenciada
4. Temporal: dates dentro dos periodos dos projetos

---

## OUT OF SCOPE (2026-02-06)

- Construcao de novos verticais (Manufacturing, Nonprofit completos)
- Automacao de login end-to-end (Camada 1 funciona, 2-5 parciais)
- WFS implementation (bloqueado por environment decision)
- MCP server production deployment

---

*Compilado de memory.md, sessions/, QBO-WFS/memory.md, Strategic Cortex*
