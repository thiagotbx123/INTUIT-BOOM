# OUTPUT E - Delta Summary (Ultimos 30 dias)

> Mudancas recentes baseadas em last_modified (Drive)
> Periodo: 2025-11-27 a 2025-12-27
> Periodo anterior: 2025-10-28 a 2025-11-27
> Linear: Sem acesso direto (inferido de referencias)

---

## RESUMO EXECUTIVO

| Metrica | Ultimos 30 dias | 30-60 dias atras | Delta |
|---------|-----------------|------------------|-------|
| **Arquivos modificados** | 891 | 2,100+ | -57% |
| **Arquivos relevantes** | 203 | 544 | -63% |
| **Arquivos high priority** | 45 | 80+ | -44% |

**Interpretacao**: Atividade significativamente menor nos ultimos 30 dias. Esperado pois o periodo anterior incluiu pico do Fall Release (deadline 11/20).

---

## MUDANCAS DE DIRECAO

### 1. Foco Estrategico Migrou para WFS
| Antes (Out-Nov) | Agora (Nov-Dez) | Evidencia |
|-----------------|-----------------|-----------|
| Fall Release delivery | WFS SOW development | 60 arquivos WFS em 30 dias |
| TCO validation | TCO maintenance | Atividade TCO -60% |
| Feature validation | Process improvement | Katherine decision 12/22 |

**Impacto**: Realocacao de recursos de delivery para planning do proximo projeto.

### 2. WFS Tomou Centro do Palco
```
Arquivos WFS criados em 30 dias:
├─ SOW v1.1 (draft)
├─ WFS_TSA_SCOPE_PLAN.xlsx
├─ WFS HCM Transformation FY26 Overview
├─ TestBox_WFS Demo Scenarios.xlsx
├─ sketch_SOW_WFS.docx (multiplas versoes)
├─ Workforce Solutions meeting notes
└─ GoCo feature analysis
```

### 3. Fall Release Transicionou para Manutencao
| Status Antes | Status Agora |
|--------------|--------------|
| Active delivery | Process improvement |
| UAT in progress | UAT complete |
| Deadline pressure | Lessons learned |

---

## NOVOS RISCOS IDENTIFICADOS

### Surgidos nos Ultimos 30 Dias
| Risco | Quando Apareceu | Impacto | Status |
|-------|-----------------|---------|--------|
| **WFS Environment Decision** | Dez 2025 | P0 | PENDING |
| **WFS SOW Dependencies** | Dez 2025 | P1 | IN PROGRESS |
| **Staged Rollout Complexity** | Dez 2025 | P2 | PLANNING |

### Riscos que Persistem
| Risco | Desde Quando | Impacto | Mudanca |
|-------|--------------|---------|---------|
| Negative Inventory TCO | Set 2025 | P1 | Sem progresso |
| Login ECS Task | Out 2025 | P1 | Workaround ativo |
| Manufacturing Visibility | Nov 2025 | P2 | Sem mudanca |

### Riscos Mitigados
| Risco | Mitigacao | Quando |
|-------|-----------|--------|
| Fall Release Deadline | Entregue em 11/20 | Nov 2025 |
| MineralHR Access | Access granted | Dez 2025 |
| WFS Exploration | GoQuick Alpha disponivel | Dez 2025 |

---

## ALTERACOES DE ESCOPO

### WFS (Novo Projeto)
```
Escopo Adicionado:
+ Worker Profile V1
+ Time Off V1 (PTO: Sick, Vacation, Personal)
+ Onboarding V1 (Digital I-9, Offer Letter)
+ Manager Role V1
+ MineralHR Integration
+ GoCo Platform Features (subset)

Escopo em Discussao:
? Demo environment final
? Staged rollout approach
? Integration depth with existing environments
```

### Fall Release
```
Escopo Concluido:
✓ TCO Environment validation
✓ Construction Sales validation
✓ Core features (Payments Agent, Finance Agent, etc.)

Escopo Pendente:
~ Manufacturing environment (95%)
~ Nonprofit environment (95%)
```

### Contratos
```
Novos Contratos (30 dias):
+ Intuit 60 Additional Licenses (assinado 12/23)
+ WFS SOW v1.1 (draft)
+ Gem SOW (draft)

Contratos em Negociacao:
~ Mailchimp SOW
~ Zuper extension
```

---

## EVOLUCAO DO INGEST E DATASETS

### Ingest Pipeline
| Componente | Status Antes | Status Agora | Mudanca |
|------------|--------------|--------------|---------|
| ECS Login Task | Failing | Failing | Workaround manual |
| Data Validator | Active | Active | assert_data_err added |
| Type Hints | Optional | Enforced | Pipeline requirement |

### Datasets
| Dataset | Status Antes | Status Agora | Mudanca |
|---------|--------------|--------------|---------|
| TCO | Validating | Validated | Complete |
| Construction | Validating | Validated | Complete |
| Canada | Active | Active | Bank account fix |
| Manufacturing | Unknown | Unknown | Gap persiste |
| WFS/GoQuick | N/A | Exploring | New |

### Health Checks
| Check | Status Antes | Status Agora | Mudanca |
|-------|--------------|--------------|---------|
| TCO Checklist | v1 | v2 | Atualizado |
| Automated Tests | Partial | Partial | Sem mudanca |
| Manual Spot Checks | Active | Active | Sem mudanca |

---

## DOCUMENTOS CRITICOS CRIADOS/MODIFICADOS

### Novos Documentos (Ultimos 30 dias)
| Documento | Data | Tipo | Importancia |
|-----------|------|------|-------------|
| Testbox - SOW - Intuit WFS v1.1 | 2025-12-18 | contract | **ALTA** |
| WFS_TSA_SCOPE_PLAN.xlsx | 2025-12-23 | strategy | **ALTA** |
| SYNC WFS TSA Notes | 2025-12-23 | meeting | Media |
| Intuit 60 Licenses (signed) | 2025-12-23 | contract | **ALTA** |
| QBO_Health_Check_Checklist_TCO_v2 | 2025-12-10 | ops | **ALTA** |

### Documentos Modificados (Ultimos 30 dias)
| Documento | Data | Mudanca |
|-----------|------|---------|
| WFS HCM Transformation FY26 | 2025-12-23 | Updated slides |
| TestBox 3.0 | 2025-12-23 | Product updates |
| GoCo Feature List | Stable | Reference only |

---

## ATIVIDADE POR TEMA

### Comparativo 30 dias vs 30-60 dias
| Tema | Antes | Agora | Trend |
|------|-------|-------|-------|
| WFS | 20 | 60 | **+200%** |
| QuickBooks | 150 | 65 | -57% |
| TCO | 200 | 40 | -80% |
| Contract/SOW | 50 | 45 | -10% |
| Fall Release | 100 | 15 | -85% |
| Construction | 30 | 12 | -60% |
| Canada | 20 | 8 | -60% |
| Ingest | 40 | 25 | -38% |
| Manufacturing | 5 | 2 | -60% |

**Insight Principal**: Transicao clara de execucao (Fall Release) para planning (WFS).

---

## DECISOES TOMADAS NOS ULTIMOS 30 DIAS

| Data | Decisao | Owner | Impacto |
|------|---------|-------|---------|
| 2025-12-22 | Fall Release = process improvement | Katherine | P1 |
| 2025-12-17 | GoQuick Alpha != sales demo | Katherine | P1 |
| 2025-12-15 | Staged rollout for WFS | Katherine | P1 |
| 2025-12-10 | Health Check could be extra service | Thiago | P2 |
| 2025-12-05 | PSC licensing review after Fusion | Saniya | P2 |

---

## OPEN QUESTIONS QUE SURGIRAM

### Novas nos Ultimos 30 Dias
| Questao | Quando Surgiu | Status |
|---------|---------------|--------|
| WFS final sales demo environment? | Dez 2025 | PENDING |
| Quais dados QBO -> MineralHR? | Dez 2025 | PENDING |
| Staged rollout approach? | Dez 2025 | IN DISCUSSION |
| Health Check as service? | Dez 2025 | IN DISCUSSION |

### Questoes que Persistem
| Questao | Desde Quando | Status |
|---------|--------------|--------|
| Manufacturing dataset status? | Nov 2025 | UNKNOWN |
| Winter Release timeline? | Nov 2025 | PENDING |
| Fusion UI impact? | Out 2025 | IN PROGRESS |

---

## STAKEHOLDER ACTIVITY

### Mais Ativos nos Ultimos 30 Dias
| Pessoa | Atividade | Foco |
|--------|-----------|------|
| **Thiago** | Alta | WFS SOW, Health Checks |
| **Katherine** | Alta | WFS alignment, decisions |
| **Soranzo** | Baixa | Staging coordination |

### Atividade Intuit
| Stakeholder | Atividade | Contexto |
|-------------|-----------|----------|
| Nikki (WFS) | Media | Access grants |
| Ben Hale | Baixa | Sales enablement |
| PSC Team | Baixa | Licensing review pending |

---

## PROJECAO PROXIMOS 30 DIAS

### Esperado
| Tema | Expectativa |
|------|-------------|
| WFS | SOW finalization, Alpha preparation |
| TCO | Maintenance, blocker fixes |
| Fall Release | Final 5% cleanup |
| Winter Release | Planning kickoff |

### Riscos a Monitorar
| Risco | Trigger |
|-------|---------|
| WFS delay | Environment decision not made |
| TCO degradation | Negative inventory not fixed |
| Resource contention | WFS + Winter Release overlap |

---

## METRICAS DE SAUDE

| Indicador | Status | Trend |
|-----------|--------|-------|
| Documentacao | GOOD | Estavel |
| Riscos Ativos | 6 | +2 (WFS related) |
| Decisoes Pendentes | 3 | Estavel |
| Open Questions | 6 | +2 |
| Blockers P0/P1 | 3 | Estavel |

---

Documento gerado automaticamente
Periodo: 2025-11-27 a 2025-12-27
Fonte: Google Drive (891 arquivos modificados)
Linear: Sem acesso direto
