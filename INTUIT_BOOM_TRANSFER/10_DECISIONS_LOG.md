# INTUIT-BOOM - Log de Decisoes

> Todas as decisoes tomadas no projeto, com contexto e raciocinio.
> IMPORTANTE: Entender o POR QUE e tao critico quanto saber O QUE.

---

## DECISOES ESTRATEGICAS

### D-001: Fall Release = Process Improvement
- **Data:** 2025-12-22
- **Decisao:** Reclassificar trabalho Fall Release como manutencao/process improvement
- **Quem decidiu:** Katherine (Kat)
- **Por que:** Nao e entrega pendente, e melhoria continua
- **Impacto:** Muda como reportamos progresso

### D-002: GoQuick Alpha != Sales Demo
- **Data:** 2025-12-17
- **Decisao:** GoQuick Alpha Retail NAO e o ambiente para sales demo WFS
- **Quem decidiu:** Katherine
- **Por que:** Evita confusao entre ambientes de teste e producao
- **Impacto:** WFS precisa de novo ambiente (decisao P0 pendente)

### D-003: Staged Rollout WFS Obrigatorio
- **Data:** 2025-12-15
- **Decisao:** WFS tem que ser staged rollout, nao big bang
- **Quem decidiu:** Katherine
- **Por que:** Proteger sellers existentes de impacto
- **Impacto:** Timeline mais longa, mas mais segura

### D-004: Strategic Cortex com 5 Outputs
- **Data:** 2025-12-27
- **Decisao:** Implementar sistema de inteligencia com 5 outputs (A-E)
- **Quem decidiu:** Thiago (TSA)
- **Por que:** Cobertura completa do projeto com diferentes granularidades
- **Impacto:** 847 knowledge items, visibilidade total

### D-005: Hybrid Approach para WFS Environment
- **Data:** 2026-01-05
- **Decisao:** Recomendar approach hibrido (new env fase 1, integrate fase 3)
- **Quem decidiu:** Thiago (recomendacao para Christina)
- **Por que:** Equilibra isolamento com integracao futura
- **Status:** AGUARDANDO decisao de Christina Duarte

---

## DECISOES TECNICAS

### D-006: Sistema de Camadas LOCKED/OPEN/REVIEW
- **Data:** 2025-12-06
- **Decisao:** Implementar protecao de codigo por camadas
- **Quem decidiu:** Rafael/Thiago
- **Por que:** Prevenir quebra de codigo estavel (login especialmente)
- **Impacto:** Camada 1 (Login) LOCKED desde dia 1

### D-007: layer1_login.py como Modulo Standalone
- **Data:** 2025-12-06
- **Decisao:** Login como modulo independente, importavel por qualquer projeto
- **Por que:** Reutilizacao multi-projeto (TCO, Construction, Product)
- **Impacto:** Codigo limpo, testavel isoladamente

### D-008: Feature Validator v2.0 com FLAGS
- **Data:** 2025-12-29
- **Decisao:** Nunca rejeitar screenshot, sempre capturar com FLAGS
- **Por que:** 5 erros graves na validacao Construction (rejeitados indevidamente)
- **Impacto:** Zero falsos negativos, decisao posteriordata

### D-009: Pre-Build Data Approach
- **Data:** 2026-01-29
- **Decisao:** Construir dados ANTES dos feature flags ativarem
- **Quem decidiu:** Thiago + validado por Kat
- **Por que:** Proven no Fall Release - dados base prontos aceleram validacao
- **Impacto:** Semanas de vantagem em cada release

### D-010: Initial Quantity para Negative Inventory
- **Data:** 2026-01-29
- **Decisao:** Usar Initial Quantity em vez de Inventory Adjustment
- **Quem decidiu:** Douglas Santos (proposal) + Thiago (aprovacao)
- **Por que:** Hit vai para Opening Balance Equity (nao COGS)
- **Impacto:** COGS so reflete vendas reais

### D-011: Canada Tickets para Backlog
- **Data:** 2026-01-29
- **Decisao:** Mover PLA-2969 e PLA-2949 para backlog
- **Quem decidiu:** Thiago
- **Por que:** Nao e prioridade agora, bills line items vazio
- **Impacto:** Foco em Keystone/Winter Release

### D-012: DriveCollector via TSA_CORTEX
- **Data:** 2025-12-27
- **Decisao:** Usar TSA_CORTEX para coletar dados do Drive (nao MCP)
- **Por que:** MCP Drive nao disponivel na epoca
- **Impacto:** 20,426 arquivos indexados

### D-013: Linear via API Direta
- **Data:** 2026-01-27
- **Decisao:** Usar Linear GraphQL API direto (nao MCP Linear)
- **Por que:** API key disponivel, mais flexivel
- **Impacto:** Scripts Python para criar tickets e comentarios

---

## DECISOES DE PROCESSO

### D-014: SpineHUB como Framework
- **Data:** 2025-12-19
- **Decisao:** Usar SpineHUB v3.1 para persistencia de contexto
- **Por que:** Garante continuidade entre sessoes Claude
- **Impacto:** Sessions/, memory.md, commands/, knowledge-base/

### D-015: 5 Status Granulares de Validacao
- **Data:** 2025-12-29
- **Decisao:** PASS / PARTIAL / NOT_AVAILABLE / FAIL / N/A
- **Por que:** Status binario (PASS/FAIL) nao diferencia limitacao de ausencia
- **Impacto:** Validacao mais precisa, menos retrabalho

### D-016: Worklog em Ingles 100%
- **Data:** TSA_CORTEX v2.2
- **Decisao:** Todo worklog DEVE ser em ingles, terceira pessoa
- **Por que:** Time global, padronizacao
- **Impacto:** Nunca usar "I worked on...", sempre "Thiago processed..."

---

## DECISOES PENDENTES

| # | Decisao | Quem Decide | Quando | Impacto |
|---|---------|-------------|--------|------------|
| P-001 | WFS: Environment new vs existing | Christina Duarte | **URGENTE** | Desbloqueia SOW e todo WFS |
| P-002 | Manufacturing: status real? | Intuit | Proximas semanas | Clarifica gap de 6 arquivos |
| P-003 | Demo Health Check vira servico? | Katherine | TBD | Nova linha de receita |
| P-004 | Timeline oficial Winter Release | Intuit | Feb 2026 | Alocacao de recursos |
| P-005 | MineralHR data flow | WFS Team | Pre-Beta | Escopo SOW WFS |

---

*Log compilado de memory.md (816 linhas), 17 sessions/, Strategic Cortex em 2026-02-06*
