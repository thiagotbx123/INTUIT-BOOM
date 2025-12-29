# WINTER RELEASE - PLANO MASTER
**IES February Release FY26**
**Gerado**: 2025-12-29
**Early Access**: 4/Fev/2026

---

## O QUE É O WINTER RELEASE

Documento oficial da Intuit ("Write it Straight Doc") que define:
- Features a serem lançadas em Fevereiro 2026
- Requisitos de setup/dados para TestBox
- Informações para GTM, marketing, treinamento

**Responsabilidade TestBox**: Garantir que os ambientes de demo estejam prontos para demonstrar todas as features.

---

## INVENTÁRIO DE FEATURES WINTER RELEASE

### CATEGORIA 1: AI AGENTS

| # | Feature | SKU | Setup TestBox | Prioridade |
|---|---------|-----|---------------|------------|
| 1 | **Accounting AI** | Ledger+, Essentials+, Plus+ | Dados existentes OK | P0 |
| 2 | **Sales Tax AI** (Pre-file check) | Plus, Advanced, IES | Config sales tax | P0 |
| 3 | **Project Management AI** | Advanced (limited), IES (full) | Projetos + budgets | P0 |
| 4 | **Finance AI** | TBD | Dados financeiros | P1 |
| 5 | **Solutions Specialist** | IES | Business Feed config | P1 |
| 6 | **Customer Agent** | TBD | Gmail/Outlook connection | P2 |
| 7 | **Omni / Intuit Intelligence** | Beta/Handraiser Feb 2026 | TBD | P2 |
| 8 | **Conversational BI** | Part of Intuit Intelligence | TBD | P3 |

### CATEGORIA 2: REPORTING & KPIs

| # | Feature | Setup TestBox | Prioridade |
|---|---------|---------------|------------|
| 9 | **KPIs Customizados** | Nenhum | P0 |
| 10 | **Dashboards** | Nenhum | P0 |
| 11 | **3P Data Integrations** | Apps 3P conectados | P2 |
| 12 | **Calculated Fields** | Nenhum | P1 |
| 13 | **Management Reports** | Nenhum | P1 |
| 14 | **Benchmarking** | TBD | P2 |
| 15 | **Multi-Entity Reports** | Multi-entity structure | P1 |

### CATEGORIA 3: DIMENSIONS

| # | Feature | Setup TestBox | Prioridade |
|---|---------|---------------|------------|
| 16 | **Dimension Assignment v2** | Dimensions configurados | P0 |
| 17 | **Hierarchical Dimension Reporting** | Hierarquia de dims | P1 |
| 18 | **Dimensions on Workflow** | Workflow + dims | P1 |
| 19 | **Dimensions on Balance Sheet** | Dims em transações | P1 |

### CATEGORIA 4: WORKFLOW

| # | Feature | Setup TestBox | Prioridade |
|---|---------|---------------|------------|
| 20 | **Parallel Approval** | Approval workflow config | P1 |

### CATEGORIA 5: MIGRATION

| # | Feature | Setup TestBox | Prioridade |
|---|---------|---------------|------------|
| 21 | **Seamless Desktop Migration** | Tenant fresh | P2 |
| 22 | **DFY Migration Experience** | Tenant fresh | P2 |
| 23 | **Feature Compatibility** | Documentação | P3 |

### CATEGORIA 6: CONSTRUCTION

| # | Feature | Setup TestBox | Prioridade |
|---|---------|---------------|------------|
| 24 | **Certified Payroll Report** | Payroll data | P1 |
| 25 | **Sales Order** | TBD | P2 |

### CATEGORIA 7: PAYROLL

| # | Feature | Setup TestBox | Prioridade |
|---|---------|---------------|------------|
| 26 | **Multi-Entity Payroll Hub** | Multi-entity + employees | P1 |
| 27 | **Garnishments - Child Support** | Employee + garnishment | P2 |
| 28 | **Assignments in QBTime** | Time entries | P2 |
| 29 | **Enhanced Amendments (CA)** | CA payroll data | P3 |

---

## PLANO DE CHECK (VALIDAÇÃO)

### FASE 1: PRÉ-RELEASE (Agora até 3/Fev)

#### Semana 1 (30/Dez - 5/Jan)
- [ ] Confirmar acesso TCO e Construction
- [ ] Verificar dados existentes cobrem features
- [ ] Criar checklist por feature
- [ ] Identificar gaps de dados

#### Semana 2 (6/Jan - 12/Jan)
- [ ] Preparar dados faltantes (manual, sem re-ingest)
- [ ] Testar navegação de todas as rotas
- [ ] Documentar pre-requisitos por feature

#### Semana 3-4 (13/Jan - 26/Jan)
- [ ] Criar scripts de automação para features novas
- [ ] Testar features que já existem (Fall Release base)
- [ ] Preparar playbooks de validação

#### Semana 5 (27/Jan - 3/Fev)
- [ ] Dry-run completo
- [ ] Verificar com Intuit status de rollout
- [ ] Ajustes finais

### FASE 2: EARLY ACCESS (4/Fev em diante)

#### Dia 1-2: Smoke Test
- [ ] Verificar todas as features estão habilitadas
- [ ] Screenshot de cada feature
- [ ] Documentar o que funciona / não funciona

#### Dia 3-7: Validação Completa
- [ ] Executar checklist por feature
- [ ] Capturar evidências
- [ ] Registrar issues

#### Dia 8-14: Triagem e Fixes
- [ ] Classificar issues por categoria
- [ ] Aplicar fixes possíveis
- [ ] Escalar para Intuit o que não puder resolver

---

## PLANO DE VISIBILIDADE

### TRACKER PRINCIPAL

**Arquivo**: `WINTER_RELEASE_TRACKER.xlsx` (a criar)

| Coluna | Descrição |
|--------|-----------|
| Feature ID | WR-001, WR-002, etc |
| Feature Name | Nome da feature |
| Category | AI Agents, Reporting, etc |
| Priority | P0, P1, P2, P3 |
| Environment | TCO, Construction, Both |
| Setup Required | Yes/No + detalhes |
| Data Available | Yes/No/Partial |
| Fall Release Ref | TCO-XXX se existir |
| Status | Not Started, In Progress, Pass, Fail, Blocked |
| Evidence | Link para screenshot |
| Notes | Observações |
| Last Updated | Data |

### STATUS POR FEATURE

```
[WR-001] Accounting AI
├── Environment: TCO
├── Setup: Dados existentes OK
├── Fall Ref: TCO-025
├── Status: 🟡 Pending (aguardando Early Access)
├── Evidence: -
└── Notes: Ready to Post batch é novo
```

### DASHBOARD DE PROGRESSO

```
╔════════════════════════════════════════════╗
║     WINTER RELEASE - STATUS GERAL          ║
╠════════════════════════════════════════════╣
║ Total Features: 29                         ║
║                                            ║
║ Por Status:                                ║
║   ⬜ Not Started:  29                      ║
║   🟡 In Progress:   0                      ║
║   ✅ Pass:          0                      ║
║   ❌ Fail:          0                      ║
║   🚫 Blocked:       0                      ║
║                                            ║
║ Por Prioridade:                            ║
║   P0: 6 features                           ║
║   P1: 10 features                          ║
║   P2: 9 features                           ║
║   P3: 4 features                           ║
║                                            ║
║ Cobertura de Dados: 100%                   ║
║ Automação Pronta: 75%                      ║
╚════════════════════════════════════════════╝
```

### COMUNICAÇÃO

#### Daily Standup (Slack)
```
📊 Winter Release Update - [DATA]

PROGRESSO:
• Features validadas: X/29
• P0: X/6 | P1: X/10 | P2: X/9

HOJE:
• [Feature em andamento]

BLOCKERS:
• [Lista ou "Nenhum"]

PRÓXIMO:
• [Próxima feature]
```

#### Weekly Report
```
# Winter Release - Resumo Semanal

## Métricas
- Features completadas: X/29 (X%)
- Issues encontradas: X
- Issues resolvidas: X

## Destaques
- [Conquistas da semana]

## Riscos
- [Riscos identificados]

## Próxima Semana
- [Plano]
```

---

## CHECKLIST POR FEATURE (TEMPLATE)

### [WR-XXX] Nome da Feature

**Pre-requisitos**:
- [ ] Ambiente: TCO / Construction / Both
- [ ] Dados necessários: [lista]
- [ ] Configurações: [lista]

**Validação**:
- [ ] Navegar para feature
- [ ] Verificar UI carrega corretamente
- [ ] Testar funcionalidade principal
- [ ] Testar edge cases
- [ ] Capturar screenshot

**Resultado**:
- Status: Pass / Fail / Partial / Blocked
- Evidence: [link]
- Notes: [observações]

---

## AUTOMAÇÃO DISPONÍVEL

### Reutilizar do Fall Release (21 features)
```
TCO-001: Dimension Assignment     → WR-016
TCO-006: KPIs Library            → WR-009
TCO-007: KPIs Custom Formula     → WR-009
TCO-008: Dashboards              → WR-010
TCO-009: Advanced Reporting      → WR-012
TCO-011: Management Reports      → WR-013
TCO-025: Accounting AI           → WR-001
TCO-027: Customer Agent          → WR-006
TCO-029: Project AI              → WR-003
TCO-030: Finance AI              → WR-004
TCO-032: Sales Tax AI            → WR-002
... (mais 10)
```

### Adaptar (6 features)
- Accounting AI: Adicionar Ready to Post batch
- Project AI: Adicionar Budget creation
- Sales Tax AI: Adicionar Pre-file check
- Dimension Assignment: v2 enhancements
- Solutions Specialist: Business Feed widgets
- Calculated Fields: Expandir de Advanced Reporting

### Criar Novo (6 features)
- Multi-Entity Reports
- Hierarchical Dimensions
- Dimensions on Workflow
- Dimensions on Balance Sheet
- Parallel Approval
- Multi-Entity Payroll Hub

---

## ESTRUTURA DE ARQUIVOS

```
intuit-boom/
├── docs/
│   ├── WINTER_RELEASE_MASTER_PLAN.md    # Este documento
│   ├── WINTER_RELEASE_TRACKER.xlsx      # Tracker principal
│   ├── WINTER_RELEASE_CHECKLIST.md      # Checklists por feature
│   └── WINTER_RELEASE_PLAYBOOKS.md      # Playbooks de validação
├── qbo_checker/
│   ├── features_rich.json               # Features Fall (base)
│   └── features_winter.json             # Features Winter (criar)
├── evidence/
│   └── winter_release/
│       ├── WR-001_accounting_ai/
│       ├── WR-002_sales_tax_ai/
│       └── ...
└── data/
    ├── winter_release_content.txt       # Doc original
    └── WINTER_RELEASE_SUMMARY.md        # Resumo
```

---

## CRITÉRIOS DE SUCESSO

### Feature PASS
- UI carrega sem erros
- Funcionalidade principal funciona
- Screenshot capturado
- Comportamento conforme documentação Intuit

### Feature FAIL
- UI não carrega ou erro
- Funcionalidade não funciona
- Comportamento diferente do esperado

### Feature PARTIAL
- UI carrega mas funcionalidade limitada
- Alguns sub-features funcionam, outros não
- Precisa flag ou configuração adicional

### Feature BLOCKED
- Feature não habilitada no ambiente
- Falta dados críticos
- Dependência externa não disponível

---

## CONTATOS

| Papel | Nome | Canal |
|-------|------|-------|
| Intuit Lead | Katherine | Slack DM D09N49AG4TV |
| Intuit Channel | - | Slack C06PSSGEK8T |
| TestBox Lead | Thiago/Rafael | - |

---

## TIMELINE

```
Dez 2025    Jan 2026                          Fev 2026
|-----------|-------------------------------|-----------|
     ↑              ↑                            ↑
  Planejamento   Preparação              Early Access
  (atual)        + Dry-run                 + Validação
```

---

Documento vivo - atualizar conforme progresso
