# OUTPUT A - Executive Snapshot

> Slack Cortex - Intuit/TestBox Intelligence
> Periodo: Ultimos 180 dias (ate 2025-12-26)
> Timezone: America/Sao_Paulo
> Canais analisados: 10

---

## STATUS POR TEMA

### 1. FALL RELEASE
| Indicador | Status | Detalhes |
|-----------|--------|----------|
| **Delivery** | DELIVERED | Deadline 11/20 cumprido |
| **TCO Environment** | OK | Apex Tire, Global Tread, RoadReady funcionais |
| **Construction Sales** | OK | Keystone Construction prioritario |
| **Secondary Envs** | 95% | Manufacturing/Nonprofit pending final review |
| **Fusion UI Migration** | IN PROGRESS | Impacta interface, delays reportados |

### 2. WFS (Workforce Solutions)
| Indicador | Status | Detalhes |
|-----------|--------|----------|
| **Alpha** | PLANNED | Dez 2025, ~100 customers |
| **Beta** | PLANNED | Fev 2026 |
| **GA** | PLANNED | Mai 2026 (2026-05-01) |
| **SOW** | IN PROGRESS | Thiago refinando com Katherine |
| **MineralHR Access** | GRANTED | GoQuick Alpha Retail, Realm ID 9341455848423964 |
| **Intuit Environment** | PENDING | Aguardando confirmacao de qual ambiente sales usara |

### 3. TCO MULTI-ENTITY
| Indicador | Status | Detalhes |
|-----------|--------|----------|
| **Parent Company** | OK | TCO (Traction Control Outfitters) |
| **Child: Apex Tire** | OK | Southwest region |
| **Child: Global Tread** | OK | Distribution |
| **Child: RoadReady** | OK | Fleet services |
| **Negative Inventory** | BLOCKER | PLA-2916 em progresso |
| **Login Issues** | WORKAROUND | ECS task failing, manual login |

### 4. CANADA CONSTRUCTION
| Indicador | Status | Detalhes |
|-----------|--------|----------|
| **Dataset** | ACTIVE | ID: 2ed5d245-0578-43aa-842b-6e1e28367149 |
| **Bank Account Fix** | DONE | Eyji corrigiu para Canada |
| **Training** | ACTIVE | Canal dedicado |

### 5. ENGINEERING/PLATFORM
| Indicador | Status | Detalhes |
|-----------|--------|----------|
| **Staging Environment** | SHARED | Coordenacao via Slack obrigatoria |
| **Data Validator** | ACTIVE | assert_data_err para report dinamico |
| **Type Hints** | ENFORCED | Pipeline GitHub valida |
| **Captcha Issues** | RECURRING | Afeta login automation |

---

## TOP BLOCKERS

| # | Blocker | Owner | Impacto | Status |
|---|---------|-------|---------|--------|
| 1 | **Negative Inventory TCO** | Engineering | Products com stock negativo | PLA-2916 open |
| 2 | **WFS Environment Decision** | Intuit | Qual ambiente para sales demo | Aguardando Intuit |
| 3 | **Fusion UI Delays** | Intuit | Interface migration impactando UAT | Em progresso |
| 4 | **Login ECS Task** | Engineering | TCO login failing | Workaround manual |
| 5 | **Staging Conflicts** | Team | Ambiente compartilhado | Protocolo de lock |

---

## DECISOES DOCUMENTADAS (Ultimos 90 dias)

| Data | Decisao | Fonte |
|------|---------|-------|
| 2025-12-22 | Fall Release work = process improvement, nao outstanding delivery | Katherine-Thiago DM |
| 2025-12-17 | GoQuick Alpha Retail NAO e demo final para sales WFS | Katherine |
| 2025-12-15 | WFS rollout precisa staged testing por impacto em sellers | Katherine |
| 2025-12-15 | Evitar tagging Waki para reduzir ruido | Thiago |
| 2025-12-10 | Demo Health Checker como potencial extra service | Thiago |
| 2025-11-05 | PSCs continuam com ambientes curados, TestBox para early-stage | Intuit PSC Team |
| 2025-11-04 | Reavaliar licensing apos Fusion launch | Saniya |

---

## OPEN QUESTIONS

1. **WFS Environment**: Qual sera o ambiente final que sales usara para WFS demo? (Intuit nao confirmou)
2. **Winter Release Timeline**: Quando comeca oficialmente? (Katherine menciona Fev 2026)
3. **MineralHR Data Flow**: Quais dados fluem de QBO para Mineral? (Aguardando resposta WFS team)
4. **Staged Rollout**: Como fazer rollout WFS sem impactar sellers existentes de TCO?
5. **Demo Health Routine**: Vai virar servico separado ou incluso no SOW?

---

## NEXT ACTIONS (Identificadas)

| # | Acao | Owner | ETA | Fonte |
|---|------|-------|-----|-------|
| 1 | Finalizar SOW WFS com MineralHR params | Thiago | Jan 2026 | Katherine-Thiago DM |
| 2 | Review Manufacturing/Nonprofit envs | Thiago | Antes de Jan | Fall Release |
| 3 | Confirmar ambiente demo WFS com Intuit | Katherine | TBD | WFS discussions |
| 4 | Documentar staged rollout plan WFS | Katherine/Soranzo | TBD | DM discussion |
| 5 | Resolver negative inventory TCO | Engineering | TBD | PLA-2916 |
| 6 | Reavaliar PSC licensing | Katherine/Saniya | Pos-Fusion | Channel discussion |

---

## KEY METRICS

| Metrica | Valor | Periodo |
|---------|-------|---------|
| Canais monitorados | 10 | - |
| Mensagens relevantes | ~150+ | 180 dias |
| Threads ativos | 20+ | 90 dias |
| Decisoes documentadas | 7 | 90 dias |
| Blockers ativos | 5 | Atual |
| Open questions | 5 | Atual |

---

## STAKEHOLDER ACTIVITY

| Pessoa | Role | Atividade Recente |
|--------|------|-------------------|
| **Katherine Lu** | Account Lead | WFS SOW, Fall Release review, stakeholder alignment |
| **Thiago Rodrigues** | TSA | Daily reports, demo health, data architecture |
| **Lucas Soranzo** | Eng Lead | Staging coordination, retool access |
| **Eyji Koike Cuff** | Engineer | Canada fixes, staging usage |
| **Marcelo** | Engineer | Staging usage, login issues |
| **Augusto** | Engineer | Data validator, type hints enforcement |
| **Saniya** | Intuit | PSC licensing discussions |

---

Gerado: 2025-12-26
Fonte: Slack MCP Collection
Canais: C06PSSGEK8T, C09SGBFBC02, C09QC6096G7, C09DKMB4NAE, C072MQDJRJS, D09GQC60JBC, D09N49AG4TV, C091ZCL7371, C0762U2S3JN, C0901G1BVME
