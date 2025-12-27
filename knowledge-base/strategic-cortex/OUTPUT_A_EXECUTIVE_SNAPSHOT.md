# OUTPUT A - Executive Snapshot

> Strategic Intelligence - Intuit/TestBox Project
> Updated: 2025-12-27 04:00 America/Sao_Paulo
> Sources: Google Drive (20,426 files), Linear (1,546 issues), Slack (10 channels)
> Linear: 443 Intuit-related issues analyzed

---

## ONDE ESTAMOS AGORA

### WFS (Workforce Solutions)
| Aspecto | Status | Evidencia |
|---------|--------|-----------|
| **SOW** | DRAFT v1.1 | `Testbox - SOW - Intuit Workforce Solutions v1.1` |
| **Scope Plan** | DOCUMENTED | `WFS_TSA_SCOPE_PLAN.xlsx` |
| **Timeline** | Alpha Dez 2025, Beta Fev 2026, GA Mai 2026 | `WFS HCM Transformation FY26 Overview` |
| **GoCo Features** | MAPPED | `GoCo Platform Comprehensive Feature List` |
| **MineralHR** | ACCESS GRANTED | GoQuick Alpha Retail, Realm ID 9341455848423964 |
| **Environment** | PENDING DECISION | Qual ambiente sera usado para sales demo? |

**156 arquivos no Drive** | **Alta atividade** | Foco atual do projeto

### QBO / QuickBooks
| Aspecto | Status | Evidencia |
|---------|--------|-----------|
| **Contratos** | ACTIVE | 60 licencas adicionais assinadas (12/23) |
| **Fall Release** | DELIVERED | Deadline 11/20 cumprido |
| **Health Check** | IN PROGRESS | `QBO_Health_Check_Checklist_TCO_v2.xlsx` |
| **Environments** | TCO OK, Secondary 95% | Manufacturing/Nonprofit pending |

**516 arquivos no Drive** | **Estavel** | Manutencao pos-release

### TCO (Traction Control Outfitters)
| Aspecto | Status | Evidencia |
|---------|--------|-----------|
| **Multi-Entity** | ACTIVE | Parent + 3 children funcionais |
| **Negative Inventory** | BLOCKER P1 | PLA-2916 open |
| **Login Issues** | WORKAROUND | Manual login required |
| **Health Check** | DOCUMENTED | Checklist v2 criado |

**518 arquivos no Drive** | **Estavel** | Blockers ativos

### Canada
| Aspecto | Status | Evidencia |
|---------|--------|-----------|
| **Dataset** | ACTIVE | ID: 2ed5d245-0578-43aa-842b-6e1e28367149 |
| **Bank Account Fix** | DONE | Eyji corrigiu |
| **Training** | ACTIVE | Canal dedicado |

**50 arquivos no Drive** | **Baixa atividade**

### Construction
| Aspecto | Status | Evidencia |
|---------|--------|-----------|
| **Keystone** | PRIORITY | Principal customer |
| **Environment** | ACTIVE | IES Construction Sales |
| **Dataset** | MAINTAINED | Validado no Fall Release |

**45 arquivos no Drive** | **Estavel**

### Manufacturing
| Aspecto | Status | Evidencia |
|---------|--------|-----------|
| **Dataset** | UNKNOWN | Apenas 6 arquivos encontrados |
| **Status** | UNCLEAR | Projeto pausado ou de baixa prioridade |

**6 arquivos no Drive** | **Gap de visibilidade**

### Ingest / Data Pipeline
| Aspecto | Status | Evidencia |
|---------|--------|-----------|
| **Pipelines** | OPERATIONAL | 120 arquivos relacionados |
| **Validators** | ACTIVE | Data validator com assert_data_err |
| **Incidents** | SOME OPEN | Login ECS task, negative inventory |

**120 arquivos no Drive** | **Operational**

### Fall Release
| Aspecto | Status | Evidencia |
|---------|--------|-----------|
| **Status** | DELIVERED | Deadline 11/20 cumprido |
| **TCO/Construction** | COMPLETE | Validados |
| **Secondary Envs** | 95% | Manufacturing/Nonprofit pending |
| **Fusion UI** | IN PROGRESS | Migration ongoing |

**63 arquivos no Drive** | **Concluido**

---

## TOP RISCOS E BLOCKERS

### Issues BLOCKED no Linear (4)
| Issue | Titulo | Team | Assignee |
|-------|--------|------|----------|
| PLA-3013 | Login task failing for TCO | Platypus | Augusto Gunsch |
| PLA-2969 | Canada Data Ingest – Bills | Platypus | Lucas Torresan |
| PLA-2883 | Error while ingesting activities | Platypus | Augusto Gunsch |
| PLA-2724 | Dimensions in Payroll | Platypus | Eyji Koike Cuff |

### Issues URGENT no Linear (Top 5 de 15)
| Issue | Titulo | Team | Status |
|-------|--------|------|--------|
| WOM-503 | Demo environments not loading for users | Wombats | Distributed |
| KLA-2337 | Load time after clicking start demo >20s | Koala | Todo |
| PLA-3103 | Zendesk - Could not activate help center | Platypus | Production QA |
| PLA-2963 | The key requested for this client is invalid | Platypus | Production QA |
| PLA-2795 | No time entries for IES Construction | Platypus | Needs Review |

### Riscos Estrategicos
| # | Risco/Blocker | Impacto | Status | Mitigacao |
|---|---------------|---------|--------|-----------|
| 1 | **WFS Environment Decision** | P0 | PENDING | Intuit precisa confirmar ambiente para sales demo |
| 2 | **Negative Inventory TCO** | P1 | TODO | PLA-2916 - Douglas Santos assigned |
| 3 | **Login ECS Task Failing** | P1 | BLOCKED | PLA-3013 - Augusto Gunsch working |
| 4 | **Canada Data Ingest** | P1 | BLOCKED | PLA-2969 - Lucas Torresan |
| 5 | **WFS SOW Finalization** | P1 | IN PROGRESS | Thiago refinando, Katherine reviewing |
| 6 | **Manufacturing Visibility** | P2 | GAP | Apenas 6 arquivos, status unclear |
| 7 | **Demo Load Time >20s** | P2 | TODO | KLA-2337 - Pamela assigned |
| 8 | **Winter Release Planning** | P3 | NOT STARTED | Precisa comecar em Jan 2026 |

---

## DECISOES MAIS RELEVANTES

| Data | Decisao | Owner | Impacto | Por que Importa |
|------|---------|-------|---------|-----------------|
| 2025-12-22 | Fall Release work = process improvement | Katherine | P1 | Reclassifica como manutencao, nao entrega pendente |
| 2025-12-17 | GoQuick Alpha != sales demo | Katherine | P1 | Evita confusao sobre ambiente WFS |
| 2025-12-15 | Staged rollout WFS obrigatorio | Katherine | P1 | Protege sellers existentes de impacto |
| 2025-12-10 | Health Check pode virar extra service | Thiago | P2 | Potencial nova linha de receita |
| 2025-11-20 | Fall Release deadline met | Team | P0 | Projeto principal entregue |
| 2025-11-05 | PSCs continuam com ambientes curados | Intuit | P2 | TestBox para early-stage apenas |

---

## O QUE ESTA NEBULOSO

| # | Questao | Por que Importa | Onde Buscar |
|---|---------|-----------------|-------------|
| 1 | **Qual ambiente final para WFS sales demo?** | Define onde sellers vao trabalhar | Intuit decision pending |
| 2 | **Qual timeline oficial do Winter Release?** | Planning e alocacao de recursos | Katherine discussions |
| 3 | **Quais dados fluem de QBO para MineralHR?** | Escopo do SOW WFS | WFS team |
| 4 | **Status real do Manufacturing dataset?** | Apenas 6 arquivos no Drive | Verificar com Intuit |
| 5 | **Demo Health Check vira servico?** | Modelo de negocio | Katherine decision |
| 6 | **Impacto total do Fusion UI?** | UAT e timelines | Intuit roadmap |

---

## PROXIMOS PASSOS RECOMENDADOS

### P0 - Imediatos (Esta semana)
| # | Acao | Owner | Evidencia de Suporte |
|---|------|-------|---------------------|
| 1 | Finalizar SOW WFS v1.1 | Thiago/Katherine | SOW draft no Drive |
| 2 | Confirmar ambiente WFS com Intuit | Katherine | Pending decision |
| 3 | Revisar Manufacturing status | Thiago | Gap de 6 arquivos |

### P1 - Curto prazo (2 semanas)
| # | Acao | Owner | Evidencia de Suporte |
|---|------|-------|---------------------|
| 4 | Resolver negative inventory TCO | Engineering | PLA-2916 |
| 5 | Finalizar review Manufacturing/Nonprofit | Thiago | 95% -> 100% |
| 6 | Documentar staged rollout WFS | Katherine/Soranzo | DM discussions |

### P2 - Medio prazo (30 dias)
| # | Acao | Owner | Evidencia de Suporte |
|---|------|-------|---------------------|
| 7 | Iniciar planning Winter Release | Katherine | Timeline TBD |
| 8 | Avaliar Health Check como service | Katherine/Thiago | Proposta existe |
| 9 | Resolver login ECS de forma definitiva | Engineering | Workaround atual |

---

## METRICAS DE VISIBILIDADE

| Fonte | Total | Relevantes | % |
|-------|-------|------------|---|
| **Google Drive** | 20,426 | 1,926 | 9.4% |
| **Linear** | 1,546 | 443 Intuit | 28.7% |
| **Slack** | 10 canais | Coletado | Via MCP |

### Linear Stats (6 meses)
| Metrica | Valor |
|---------|-------|
| Total Issues | 1,546 |
| Intuit/QBO/WFS Related | 443 |
| Urgent Priority | 15 |
| High Priority | 99 |
| Blocked | 4 |
| Top Team: Platypus | 487 issues |

### Distribuicao por Tema (Drive)
| Tema | Arquivos | Trend |
|------|----------|-------|
| TCO | 518 | Estavel |
| QBO | 516 | Estavel |
| Contract/SOW | 213 | Alta atividade |
| Security | 184 | Estavel |
| IES | 164 | Estavel |
| WFS | 156 | **Em alta** |
| Ingest | 120 | Estavel |
| Reporting | 70 | Baixa |
| Fall Release | 63 | Concluindo |
| Dataset | 72 | Estavel |
| Canada | 50 | Baixa |
| Construction | 45 | Estavel |
| Multi-entity | 8 | Baixa |
| Manufacturing | 6 | **Gap** |

---

## HEALTH CHECK GERAL

| Area | Status | Notas |
|------|--------|-------|
| **Estrategia** | OK | WFS e foco claro, Fall Release entregue |
| **Contratos** | IN PROGRESS | WFS SOW em finalizacao |
| **Datasets** | MOSTLY OK | TCO/Construction OK, Manufacturing gap |
| **Ingest** | OPERATIONAL | 4 issues blocked, engineering working |
| **Environments** | ATTENTION | TCO login blocked (PLA-3013), WFS pending |
| **Documentacao** | GOOD | 1,926 Drive + 443 Linear issues indexados |
| **Riscos** | MANAGED | 8 riscos, 4 P1, 15 urgent Linear issues |

---

Documento gerado automaticamente
Fontes: TSA_CORTEX DriveCollector + Slack MCP + Linear API
Linear: Full scan 6 meses - 1,546 issues (443 Intuit-related)
Ultima atualizacao: 2025-12-27 04:00
