# INTUIT BOOM - Memory File

## Contexto Persistente

Este arquivo armazena informacoes importantes que devem persistir entre sessoes.

---
## REGRAS OBRIGATORIAS DE VALIDACAO (NUNCA IGNORAR)

### Regra 1: Escopo Completo
- ANTES de validar ambiente, listar TODAS as features aplicaveis
- IES = TCO + Construction + Product (mesmas features)
- NAO assumir que menos features = suficiente

### Regra 2: Paridade de Qualidade
- Se ambiente A tem tracker com N colunas, ambiente B tem N colunas
- Evidence_notes DETALHADAS (o que esta visivel, nao apenas se carregou)
- Data validation quando aplicavel

### Regra 3: Validacao Pos-Captura
- Screenshot > 100KB = provavelmente valido
- Screenshot ~140KB = provavel pagina de erro 404
- Verificar conteudo da pagina ("sorry", "error" = falha)
- Se erro, tentar navegacao alternativa (menu vs URL)

### Regra 4: Status Granular
- PASS = Feature funciona como esperado
- PARTIAL = Feature existe mas com limitacoes
- NOT_AVAILABLE = Feature nao habilitada no ambiente (diferente de FAIL)
- FAIL = Bug real

### Regra 5: Comparacao Entre Ambientes
- Comparar screenshots lado a lado
- Identificar diferencas de conteudo (AI icons, dados populados)
- Documentar nas notes o que difere

---

## Projeto
- **Nome**: INTUIT BOOM
- **Cliente**: Intuit (QuickBooks Online)
- **Tipo**: Validacao de features QBO Fall Release
- **Dono do projeto**: Thiago

## Estado Atual do Projeto

### Fase
- [x] Estrutura inicial criada
- [x] Sistema de camadas implementado
- [x] CAMADA 1 (Login) LOCKED
- [ ] CAMADA 2 (Navegacao) finalizada
- [ ] CAMADA 3 (Captura) finalizada
- [ ] CAMADA 4 (Planilha) finalizada
- [ ] CAMADA 5 (Orquestracao) finalizada

### Ultimas Acoes
- 2026-01-27: Deep Investigation - 6 usuarios Intuit com admin access identificados no ambiente
- 2026-01-27: Descoberta: custom role "Project Custom" criado 1/20/2026 (7 dias antes do problema)
- 2026-01-27: Resposta tecnica formulada para Jason/Matt com sugestao de Activity Log
- 2026-01-27: Keystone Payroll Employee Duplication - 90 employees com erro, ~86 duplicados deletados manualmente
- 2026-01-27: Root cause: processo QBO-side criando records (nao TBX bug)
- 2026-01-27: Linear ticket PLA-3227 criado via API + worklog adicionado como comentario
- 2026-01-27: Linear API integrada - scripts create_linear_ticket.py e add_linear_comment.py
- 2026-01-27: February Release prep - 3 docs de orientacao para Alexandra criados
- 2026-01-27: Descoberta: michael_gugel+test1@intuit.com (real Intuit employee) em dados sinteticos
- 2026-01-23: SpineHUB Full Context Export - Documento completo gerado (INTUIT_BOOM_FULL_CONTEXT_2026-01-23.md)
- 2026-01-23: Contexto consolidado para transferencia de conhecimento entre IAs (~1,500 linhas)
- 2026-01-20: IC Balance Sheet Investigation - Bug identificado, escalado para Engineering (PLA-3201)
- 2026-01-20: Dossier completo criado (PT + EN) - 339 linhas documentando investigacao
- 2026-01-20: 5 JEs criados (~$14M) + 4 IC mappings corrigidos + conta 1083 criada
- 2026-01-20: Troubleshooting Guide criado em SpineHUB/knowledge-base
- 2026-01-20: Winter Release 2026 Gantt v9 Final - 29 features consolidadas em 7 categorias
- 2026-01-20: Google Sheets integration via gspread - paleta de cores extraida
- 2026-01-20: Auditoria completa do GSheet (10 issues, 44 warnings identificados)
- 2026-01-06: IES February Release FY26 - Analise Critica Integrada criada
- 2026-01-06: Documento Conversational BI analisado com comentarios internos Intuit
- 2026-01-06: Explicacao para leigo criada (IES_FEBRUARY_RELEASE_EXPLICACAO_LEIGO.md)
- 2026-01-05: PPTs RACCOONS criados (Recursos + Alinhamentos) com hyperlinks
- 2026-01-05: SpineHUB collect completo - 1293 eventos (958 Slack, 209 Drive, 87 Claude)
- 2026-01-05: Alinhamentos Thais documentados (SYNC 02 Jan 2025)
- 2025-12-29: WINTER RELEASE CONSTRUCTION CORRIGIDO - 25 features (21 PASS, 2 PARTIAL, 2 N/A)
- 2025-12-29: Learnings criticos documentados (5 erros graves corrigidos)
- 2025-12-29: Tracker unificado TCO+Construction com 50 features
- 2025-12-29: WINTER RELEASE TCO COMPLETO - End-to-end validation
- 2025-12-29: Google Drive API configurada (OAuth2 + token salvo)
- 2025-12-29: 29 screenshots com hyperlinks no Drive organizados
- 2025-12-29: Tracker final: WINTER_RELEASE_VALIDATION_WITH_LINKS.xlsx
- 2025-12-29: Evidence Pack completo - 30 screenshots capturados via Playwright CDP
- 2025-12-29: Master Validation Sheet atualizada com Evidence_links
- 2025-12-29: Data Validation executada - 17 Strong, 5 Weak, 1 Inconclusive
- 2025-12-29: Executive Report criado com recomendacoes de acao
- 2025-12-29: Winter Release FY26 Validation COMPLETA - 29/29 PASS (100%)
- 2025-12-29: Tracker JSON e CSV atualizados
- 2025-12-29: Learning file criado no SpineHub
- 2025-12-27: Linear full scan - 1,546 issues (443 Intuit-related)
- 2025-12-27: 4 blockers e 15 urgents identificados no Linear
- 2025-12-27: Strategic Cortex atualizado com dados Linear
- 2025-12-27: Strategic Cortex completo (5 outputs) - 20,426 arquivos processados
- 2025-12-27: Drive Cortex criado - 1,926 arquivos relevantes indexados
- 2025-12-27: Slack Cortex criado - 10 canais processados
- 2025-12-19: Sistema de aprendizado e consolidacao implementado
- 2025-12-06: CAMADA 1 trancada (layer1_login.py validado)
- 2025-12-06: Sistema de camadas criado

## Decisoes Importantes

| Data | Decisao | Motivo |
|------|---------|--------|
| 2025-12-27 | Strategic Cortex com 5 outputs (A-E) | Cobertura completa do projeto |
| 2025-12-27 | DriveCollector via TSA_CORTEX | MCP Drive nao disponivel |
| 2026-01-27 | Linear via API direta | API key em Tools/LINEAR_AUTO/.env |
| 2025-12-27 | Linear como receitas manuais | MCP Linear nao configurado |
| 2025-12-22 | Fall Release = process improvement | Reclassificado como manutencao |
| 2025-12-17 | GoQuick Alpha != sales demo | Evitar confusao ambiente WFS |
| 2025-12-15 | Staged rollout WFS obrigatorio | Proteger sellers existentes |
| 2025-12-06 | Sistema de camadas LOCKED/OPEN/REVIEW | Proteger codigo estavel |
| 2025-12-06 | layer1_login.py como modulo standalone | Reutilizacao multi-projeto |

## Bloqueios Conhecidos

- [ ] Camadas 2-5 ainda nao tem owners definidos
- [ ] Hyperlinks do Google Drive precisam de cache

### Riscos Ativos (via Strategic Cortex + Linear)
| # | Risco | Impacto | Status | Linear |
|---|-------|---------|--------|--------|
| 1 | WFS Environment Decision | P0 | PENDING | - |
| 2 | Negative Inventory TCO | P1 | TODO | PLA-2916 |
| 3 | Login ECS Task Failing | P1 | BLOCKED | PLA-3013 |
| 4 | Canada Data Ingest Bills | P1 | BLOCKED | PLA-2969 |
| 5 | WFS SOW Finalization | P1 | IN PROGRESS | - |
| 6 | Demo Load Time >20s | P2 | TODO | KLA-2337 |
| 7 | Manufacturing Visibility | P2 | GAP | - |

### Blockers Linear (4)
- PLA-3013: Login task failing for TCO (Augusto Gunsch)
- PLA-2969: Canada Data Ingest Bills (Lucas Torresan)
- PLA-2883: Error ingesting activities (Augusto Gunsch)
- PLA-2724: Dimensions in Payroll (Eyji Koike Cuff)

### Tickets Recentes
- PLA-3227: Keystone Employee Duplication (RESOLVED) - 2026-01-27
- PLA-3201: IC Balance Sheet (ESCALATED) - 2026-01-20

### Open Questions
- Qual ambiente final para WFS sales demo?
- Qual timeline oficial do Winter Release?
- Quais dados fluem de QBO para MineralHR?
- Status real do Manufacturing dataset?
- Demo Health Check vira servico?

## Projetos/Companies Ativos

### TCO
- Apex Tire & Auto Retail, LLC (9341455130166501)
- Vista consolidada (9341455649090852)
- Global Tread Distributors, LLC (9341455130196737)
- Traction Control Outfitters, LLC (9341455130188547)
- RoadReady Service Solutions, LLC (9341455130170608)

### CONSTRUCTION
- Keystone Construction (Par.) - CID: 9341454156620895
- Keystone Terra (Ch.) - CID: 9341454156620204
- Vista consolidada
- Dataset: construction_demo (ID: 2ed5d245-0578-43aa-842b-6e1e28367149)
- Employees no dataset: 45
- Projects no dataset: 6 (GaleGuardian, Sobey Stadium, Leap Labs, BMH, TidalWave, Azure Pines)

### USUARIOS INTUIT COM ACESSO (Keystone Terra)
| Nome | Email | Role |
|------|-------|------|
| QB Demoteam | qbdemoteam@intuit.com | Primary Admin |
| Akshit Agarwal | akshit_agarwal@intuit.com | Company admin |
| Garrett Lusk | garrett_lusk@intuit.com | Company admin |
| Lawton Ursrey | - | Company admin |
| Austin Alexander | austin_alexander@intuit.com | Bill approver |
| Sumit Kumar | sumit_kumar1@intuit.com | Bill approver |



## WFS (Workforce Solutions) Project

### O que e WFS
- Intuit Workforce Solutions - plataforma HCM para pequenas e medias empresas
- Combina payroll, HR, benefits, time com integracao QuickBooks
- Powered by GoCo + QuickBooks Payroll

### Timeline
- Alpha: Dezembro 2025 (~100 customers)
- Beta: Fevereiro 2026 (confirmar - algumas fontes dizem Marco)
- GA: Maio 2026 (key date: 2026-05-01)

### Stakeholders Intuit
- Ben Hale: sales enablement
- Nikki Behn: marketing (GoCo background)
- Kyla Ellerd: sales program management
- Christina Duarte: leadership, scoping
- Nir: headcount forecast

### Stakeholders TestBox
- Katherine Lu: program lead, SOW
- Thiago Rodrigues: TSA, data architect

### Demo Stories Prioritizadas
1. Unified PTO - employee > manager > payroll admin
2. Magic Docs - AI document generation + e-signature
3. Hire to fire lifecycle
4. Job costing

### Blockers Conhecidos
- PRDs tecnicos faltando
- Sandbox access dates incertos
- Procurement delay risk
- User license count para Fevereiro
- Mineral HR partner integration decision

### Documentacao
- wfs/WFS_CORTEX_v1.md - Cortex completo do projeto

## Notas de Sessao

Adicione aqui notas importantes de cada sessao de trabalho:

---
### Sessao: 2025-12-19 - Sistema de Aprendizado + WFS Cortex
**Conquistas:**
- Sistema de consolidacao (/consolidar) criado
- Sistema de status (/status) criado
- Memory file criado para persistencia entre sessoes
- Pasta sessions/ criada para historico
- WFS_CORTEX_v1.md importado para knowledge-base

**Conhecimentos adquiridos:**
- WFS project scope, timeline, stakeholders
- Demo stories prioritizadas (PTO, Magic Docs)
- Golden thread data architecture
- Delivery waves (0-3)

**Proximo passo:** Definir owners para camadas 2-5, aguardar PRDs WFS
---

---
### Sessao: 2025-12-26 - Treinamento via Camada de Coleta
**Conquistas:**
- Aprendido sistema de Collectors do TSA_CORTEX
- Mapeados 416 arquivos relevantes em Downloads
- Coletadas informacoes de WFS, Fall Release, TCO, Canada, Construction
- Consolidado conhecimento em knowledge-base/TREINAMENTO_COLETADO.md
- Importada documentacao da Camada de Coleta do CORTEX

**Fontes Processadas:**
- TBX_QuickBooks_Context_for_ChatGPT.txt (contexto completo)
- GoCo + WFS Teams and Deliverables CSV (roadmap WFS)
- GoCo Platform Feature List CSV (features por fase)
- fall_release_catalog.md (catalogo de features)
- step qbo.txt (guia intercompany)
- datasets.csv (segmentos disponiveis)
- construction_demo_customers CSV (dados Canada)
- TCO_Milestone CSV (milestones projetos)

**Conhecimento Chave Adquirido:**
- WFS Timeline: Alpha Dez/25 > Beta Fev/26 > GA Mai/26
- Feature flags: ENABLE-HCM-ROUTES, ENABLE-BETA-HCM-ROUTES
- Stakeholders Intuit e TestBox
- Estrutura datasets: TCO, Construction, Canada, Manufacturing
- Tickets Linear ativos e blockers

**Proximo passo:** Processar arquivos Excel/PDF restantes quando Python disponivel
---

---
### Sessao: 2025-12-27 - Strategic Cortex Build
**Conquistas:**
- Slack Cortex completo (10 canais, 4 outputs)
- Drive Cortex completo (20,426 arquivos, 1,926 relevantes)
- Strategic Cortex completo (5 outputs A-E)
- Learning file criado no SpineHub/TSA_CORTEX
- 847 knowledge items extraidos
- 7 riscos identificados e priorizados

**Fontes Processadas:**
- Google Drive via DriveCollector (OAuth2)
- Slack via MCP (10 canais)
- Linear (receitas manuais - sem acesso direto)

**Conhecimento Chave Adquirido:**
- WFS e foco atual (+200% atividade vs anterior)
- Fall Release entregue 11/20 (deadline cumprido)
- 60 licencas adicionais assinadas 12/23
- SOW WFS v1.1 em draft
- TCO com 3 blockers P1 ativos
- Manufacturing com gap de visibilidade (6 arquivos)

**Pattern Aprendido:** Strategic Cortex (5 outputs)
- A: Executive Snapshot - status rapido
- B: Strategic Map - conexoes
- C: Knowledge Base JSON - automacao
- D: Keyword Map - busca
- E: Delta Summary - mudancas

**Proximo passo:** Configurar Linear MCP, resolver WFS environment decision
---

---
### Sessao: 2025-12-27 04:00 - Linear Full Scan
**Conquistas:**
- Linear full scan executado (6 meses, 1,546 issues)
- 443 issues Intuit-related identificadas (28.7%)
- 4 blockers criticos encontrados
- 15 issues urgentes mapeadas
- Strategic Cortex atualizado com dados Linear

**Blockers Encontrados:**
- PLA-3013: Login task failing for TCO
- PLA-2969: Canada Data Ingest Bills
- PLA-2883: Error ingesting activities
- PLA-2724: Dimensions in Payroll

**Conhecimento Chave:**
- Platypus e o time com mais issues (487)
- 99 issues High priority abertas
- WOM-507: Phil Skinner autologin issue (ativo)
- KLA-2337: Demo load time >20s (urgente)

**Proximo passo:** Resolver PLA-3013 (login TCO), monitorar WOM-507
---

---
### Sessao: 2025-12-29 - Winter Release FY26 Validation COMPLETA
**Conquistas:**
- Validacao completa de 29 features Winter Release
- 29/29 PASS (100%)
- Tracker JSON atualizado (features_winter.json)
- Tracker CSV criado (WINTER_RELEASE_TRACKER.csv)
- Learning file criado no SpineHub

**Features Validadas por Categoria:**
| Categoria | Features | Status |
|-----------|----------|--------|
| AI Agents | 8 | 100% PASS |
| Reporting | 7 | 100% PASS |
| Dimensions | 4 | 100% PASS |
| Workflow | 1 | 100% PASS |
| Migration | 3 | 100% PASS |
| Construction | 2 | 100% PASS |
| Payroll | 4 | 100% PASS |

**Tecnicas Aprendidas:**
- Validacao content-based (mais robusta que CSS selectors)
- CDP connection via Playwright (port 9222)
- Batch processing por prioridade (P0 > P1 > P2 > P3)

**Arquivos Criados:**
- `qbo_checker/features_winter.json` - Tracker JSON
- `docs/WINTER_RELEASE_TRACKER.csv` - Tracker CSV
- `TSA_CORTEX/knowledge-base/learnings/2025-12-29_winter_release.md` - Learning

**Proximo passo:** Monitorar early access (2026-02-04), re-validar antes do release
---

---
### Sessao: 2025-12-29 11:12 - Winter Release Evidence Pack
**Conquistas:**
- 30 screenshots capturados via Playwright CDP (porta 9222)
- Master Validation Sheet com 18 colunas e Evidence_links
- Data Validation: 17 Strong, 5 Weak, 1 Inconclusive, 6 N/A
- Executive Report com recomendacoes de acao
- 2 commits pushados para GitHub

**Arquivos Entregues:**
- `EvidencePack/WinterRelease/TCO/*.png` - 30 screenshots
- `docs/WINTER_RELEASE_MASTER_VALIDATION.xlsx` - Planilha mestre
- `docs/DATA_VALIDATION_RESULTS.csv` - Resultados validacao
- `docs/WINTER_RELEASE_EXECUTIVE_REPORT.md` - Relatorio executivo

**Features com Dados Fracos (acao necessaria):**
- WR-008, WR-010, WR-013: custom_reports (3 rows) - PopulateData
- WR-018, WR-020: workflow_automations (8 rows) - PopulateData
- WR-016: product_services_classifications NOT FOUND - AdjustConfig

**Proximo passo:** Povoar dados fracos, re-validar antes de Early Access (2026-02-04)
---

---
### Sessao: 2025-12-29 12:30 - Winter Release TCO COMPLETO
**Conquistas:**
- Processo end-to-end de validacao concluido
- 29 screenshots com qualidade validada (17 EXCELLENT, 8 GOOD)
- Google Drive API configurada (OAuth2 + token persistente)
- Hyperlinks funcionais no tracker Excel
- Organizacao completa no Drive (pasta TCO + tracker)

**Tecnicas Aprendidas:**
- Screenshot quality assessment por tamanho (>200KB = EXCELLENT)
- Google API OAuth2 flow com token pickle
- Excel hyperlinks via openpyxl
- Drive file listing via API v3

**Arquivos Criados:**
- `drive_links.json` - Mapeamento filename -> Drive URL
- `token_drive.pickle` - Token OAuth2 persistente
- `WINTER_RELEASE_VALIDATION_WITH_LINKS.xlsx` - Tracker final

**Google Drive Final:**
```
08. Intuit/06. Winter Release/
├── WINTER_RELEASE_VALIDATION_WITH_LINKS.xlsx
└── TCO/ (29 screenshots)
```

**Credenciais Configuradas:**
- Google: thiago@testbox.com / Olivia@190985
- OAuth Project: 486245165530
- Token: C:/Users/adm_r/token_drive.pickle

**Proximo passo:** Replicar processo para CONSTRUCTION
---

---
### Sessao: 2025-12-29 13:00 - Winter Release CONSTRUCTION COMPLETO
**Conquistas:**
- Login no QBO Construction (Keystone Construction) via Playwright CDP
- 4 features validadas com 100% PASS
- Screenshots de alta qualidade (2 EXCELLENT, 2 GOOD)
- Pasta Construction criada no Drive
- Tracker com hyperlinks criado

**Features Validadas:**
| Ref | Feature | Quality |
|-----|---------|---------|
| WR-003 | Project Management AI | GOOD (191KB) |
| WR-020 | Parallel Approval | GOOD (139KB) |
| WR-024 | Certified Payroll Report | EXCELLENT (265KB) |
| WR-025 | Sales Order | EXCELLENT (306KB) |

**Google Drive Final:**
```
08. Intuit/06. Winter Release/
├── WINTER_RELEASE_VALIDATION_WITH_LINKS.xlsx (TCO)
├── CONSTRUCTION_WINTER_RELEASE_VALIDATION.xlsx (Construction)
├── TCO/ (29 screenshots)
└── Construction/ (4 screenshots)
```

**Arquivos Criados:**
- `drive_links_construction.json` - Mapeamento filename -> Drive URL
- `CONSTRUCTION_WINTER_RELEASE_VALIDATION.xlsx` - Tracker Construction
- `EvidencePack/WinterRelease/Construction/*.png` - 4 screenshots

**Totais Winter Release:**
- TCO: 29/29 PASS (100%)
- Construction: 4/4 PASS (100%)
- Total: 33/33 PASS (100%)

**Proximo passo:** Winter Release FY26 pronto para Early Access (2026-02-04)
---

---
### Sessao: 2025-12-29 14:30 - Construction CORRIGIDO + Learnings Criticos
**Problema Inicial:**
- Usuario rejeitou validacao Construction por ser muito superficial
- Apenas 4 features validadas (deveria ser 25)
- Tracker sem evidence_notes detalhadas
- Screenshots de erro 404 nao identificados

**Erros Cometidos (e corrigidos):**
1. **Escopo incompleto**: 4 features em vez de 25 (IES = todas features)
2. **Falta de paridade**: Tracker Construction muito mais pobre que TCO
3. **Screenshots invalidos**: 5 paginas de erro 404 nao detectadas
4. **Status binario**: Nao diferenciava PARTIAL de NOT_AVAILABLE
5. **Evidence_notes genericas**: Nao descreviam conteudo real

**Correcoes Aplicadas:**
- Recaptura de 25 features (todas IES aplicaveis)
- Tracker com mesmo formato do TCO (15 colunas)
- Validacao pos-captura (tamanho arquivo + conteudo)
- Status granular: PASS/PARTIAL/NOT_AVAILABLE
- Evidence_notes detalhadas por screenshot

**Resultado Final:**
| Ambiente | Total | PASS | PARTIAL | N/A |
|----------|-------|------|---------|-----|
| TCO | 25 | 25 | 0 | 0 |
| Construction | 25 | 21 | 2 | 2 |
| TOTAL | 50 | 46 | 2 | 2 |

**Features Parciais (Construction):**
- WR-011: URL /app/apps nao existe
- WR-027: Employees page vazia

**Features Nao Disponiveis (Construction):**
- WR-018: Workflow URL 404
- WR-020: Workflow URL 404

**Arquivos Criados:**
- `docs/WINTER_RELEASE_UNIFIED_TRACKER_FINAL.xlsx` - Tracker unificado
- `TSA_CORTEX/knowledge-base/learnings/2025-12-29_construction_validation_deep_learnings.md`

**Learnings Documentados:**
- Arquivo de learnings com 5 erros graves e suas correcoes
- Checklist obrigatorio para validacao de ambiente
- Regras permanentes adicionadas ao memory.md

**Proximo passo:** Aplicar learnings em validacoes futuras, nunca repetir erros
---

---
### Sessao: 2025-12-29 19:30 - Feature Validator v2.0 + Recaptura Refinada
**Conquistas:**
- Feature Validator v2.0 criado (qbo_checker/feature_validator.py)
- Metodo padronizado de captura com FLAGS (nunca rejeita)
- Recaptura TCO: WR-014, WR-021, WR-022, WR-023 concluida
- Recaptura Construction: WR-018, WR-020 documentadas como NOT_AVAILABLE
- SpineHub atualizado com learnings

**Learnings Criticos Aplicados:**
1. **Tempo de espera**: 30-45s (nao 10s) - QBO e lento
2. **Nunca rejeitar**: Sempre capturar, marcar com FLAGS
3. **Evidence notes tecnicas**: Template estruturado com confianca
4. **404 = NOT_AVAILABLE**: Documentar, buscar na web, nao retentar
5. **Features de documentacao**: Marcar N/A (nao UI)

**Sistema de FLAGS:**
```python
LOGIN_PAGE        # Capturou pagina de login
LOADING_DETECTED  # Spinner visivel
ERROR_CONTENT     # Conteudo de erro
VERY_SMALL_FILE   # < 50KB
SMALL_FILE        # 50-100KB
ERROR_PAGE_404    # Pagina 404 confirmada
NOT_AVAILABLE     # Feature nao disponivel
```

**Thresholds de Qualidade (KB):**
| Quality | Size |
|---------|------|
| EXCELLENT | >= 250 |
| GOOD | >= 150 |
| ACCEPTABLE | >= 100 |
| WEAK | >= 50 |
| INVALID | < 50 |
| ERROR_PAGE | ~139 |

**Resultados Recaptura:**
| Feature | Ambiente | Status | Size | Observacao |
|---------|----------|--------|------|------------|
| WR-014 | TCO | PASS | 113KB | Reports + Performance center |
| WR-021 | TCO | PASS | 161KB | Import Data page |
| WR-022 | TCO | PASS | 165KB | Import Data page |
| WR-023 | TCO | N/A | - | Documentation feature |
| WR-018 | CONSTR | NOT_AVAILABLE | 139KB | URL 404 |
| WR-020 | CONSTR | NOT_AVAILABLE | 22KB | Depende de WR-018 |

**Arquivos Criados:**
- `qbo_checker/feature_validator.py` - Metodo padronizado v2.0
- `docs/RECAPTURE_TCO_FINAL_20251229.md` - Resultados TCO
- `docs/RECAPTURE_CONSTRUCTION_FINAL_20251229.md` - Resultados Construction
- `WINTER_RELEASE_TRACKER_UPDATED_20251229.xlsx` - Tracker atualizado
- `TSA_CORTEX/knowledge-base/learnings/FEATURE_VALIDATOR_LEARNINGS_20251229.md`

**Metodo Padronizado v2.0:**
```
1. LOGIN (layer1_login.py + TOTP)
2. NAVEGACAO (URL + timeout 60s)
3. ESPERA (30-45s)
4. CAPTURA (screenshot + timeout 60s)
5. ANALISE (flags + tamanho + headers)
6. FALLBACK (se erro, tentar URL alternativa)
7. EVIDENCE NOTES (template tecnico)
8. DECISAO (PASS/REVIEW/NOT_AVAILABLE/N/A)
```

**Proximo passo:** Usar feature_validator.py em todas validacoes futuras
---

---
### Sessao: 2025-12-29 20:30 - REVISAO CRITICA + Framework Universal
**Conquistas:**
- Revisao critica de 10 screenshots TCO problematicos
- Framework Universal de Validacao criado (aplicavel a TODOS ambientes)
- Checklist pre-captura em JSON
- 6 regras canonicas documentadas
- 5 anti-patterns com exemplos reais

**Problemas Identificados nos Screenshots:**
| Ref | Feature | Problema | Severidade |
|-----|---------|----------|------------|
| WR-006 | Customer Agent | Dashboard generico | CRITICO |
| WR-007 | Intuit Intelligence | Homepage sem chat | CRITICO |
| WR-012 | Calculated Fields | 404 | CRITICO |
| WR-014 | Benchmarking | Loading spinner | GRAVE |
| WR-015 | Multi-Entity Reports | Contexto errado (Apex vs Consolidated) | CRITICO |
| WR-020 | Parallel Approval | Lista generica | MEDIO |
| WR-023 | Feature Compatibility | N/A - Documentacao | N/A |
| WR-026 | Payroll Hub | 404 | CRITICO |
| WR-029 | Enhanced Amendments | CA-specific, TCO errado | N/A |

**6 REGRAS CANONICAS (UNIVERSAIS):**
```
REGRA 1: Screenshot DEVE provar a feature especifica
         - NAO aceitar homepage/dashboard generico
         - Pergunta: "Este screenshot prova ESTA feature?"

REGRA 2: Contexto correto OBRIGATORIO
         - Multi-entity = Consolidated View
         - CA features = California tenant
         - Verificar header ANTES de capturar

REGRA 3: N/A = DOCUMENTACAO, nao falha
         - N/A so para features sem UI
         - Se falhou: investigar, nao marcar N/A

REGRA 4: Agrupar por contexto
         - Capturar TODAS features do contexto atual
         - Trocar empresa UMA VEZ
         - Evitar switching repetido

REGRA 5: 404 = INVESTIGAR
         - Tentar navegacao alternativa
         - Pesquisar na web
         - Se nao existe: NOT_AVAILABLE com justificativa

REGRA 6: Ambiente especifico = Ambiente especifico
         - CA = California (nao Canada)
         - Canada = Sistema payroll diferente
         - Fresh tenant = Sem dados
```

**Mapa de Contextos:**
| Contexto | Features |
|----------|----------|
| APEX (Individual) | WR-001 a WR-014, WR-016 a WR-020, etc |
| CONSOLIDATED VIEW | WR-015, WR-026 |
| DOCUMENTATION | WR-023 |
| CA TENANT | WR-029 |

**Arquivos Criados:**
- `knowledge-base/UNIVERSAL_VALIDATION_FRAMEWORK.md` - Framework completo
- `qbo_checker/CAPTURE_CHECKLIST.json` - Checklist executavel
- `docs/REVISAO_CRITICA_TCO_20251229.md` - Analise detalhada
- `qbo_checker/FEATURE_VALIDATION_CANON.json` v3.0 - Regras atualizadas

**Diferencas TCO vs Construction:**
| Aspecto | TCO | Construction |
|---------|-----|--------------|
| Multi-entity | Sim (5 empresas) | Verificar |
| Consolidated View | Disponivel | Verificar |
| Workflow Automation | Funcional | 404 |
| AI Sparkles | Visivel | Limitado |
| Special | - | Certified Payroll, Projects |

**Proximo passo:** Executar recaptura TCO com novo framework
---

---
### Sessao: 2026-01-20 22:30 - IC Balance Sheet Investigation
**Conquistas:**
- Investigacao completa do erro "Consolidated Balance Sheet isn't balancing"
- Identificacao de conta deletada em 4 IC mappings
- Criacao da conta 1083 no Shared COA
- Atualizacao de 4 mapeamentos IC
- Criacao de 5 Journal Entries (~$14M total)
- Descoberta de bug no Consolidated View (nao sincroniza mudancas)

**Problema:**
- JEs salvos corretamente nas entidades individuais
- Consolidated View NAO reflete as mudancas
- Refreshes multiplos nao resolvem

**Acoes:**
- Dossier criado (PT): DOSSIE Consolidated Balance Sheet Out of Balance Investigation.txt
- Dossier criado (EN): DOSSIER_Consolidated_Balance_Sheet_Investigation_EN.md
- Linear ticket criado: PLA-3201
- Troubleshooting Guide: SpineHUB/knowledge-base/QBO_IC_BALANCE_SHEET_TROUBLESHOOTING.md

**Conclusao:**
- Problema de sistema/backend, nao de dados
- Escalado para Intuit Engineering

**Proximo passo:** Aguardar resposta de Engineering, atualizar David Ball
---

## Cortex System

### Estrutura
```
knowledge-base/
├── slack-cortex/     <- Comunicacao (10 canais)
├── drive-cortex/     <- Documentos (20,426 -> 1,926)
├── strategic-cortex/ <- Consolidado (5 outputs)
```

### Metricas
| Fonte | Total | Relevantes | % |
|-------|-------|------------|---|
| Drive | 20,426 | 1,926 | 9.4% |
| Slack | 10 canais | 500+ msgs | ~80% |
| Linear | 1,546 | 443 Intuit | 28.7% |

### Linear Stats (6 meses)
- Issues Urgentes: 15
- Issues High: 99
- Blocked: 4
- Top Team: Platypus (487)

### Como Usar
1. **Inicio de sessao:** Ler `strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md`
2. **Buscar info:** Usar queries de `OUTPUT_D_KEYWORD_MAP_LINEAR_RECIPES.md`
3. **Verificar mudancas:** Consultar `OUTPUT_E_DELTA_SUMMARY.md`
4. **Dados estruturados:** Usar `OUTPUT_C_KNOWLEDGE_BASE.json`

---

## Linear API Access

### Configuracao
- **API Key:** Ver `C:\Users\adm_r\Tools\LINEAR_AUTO\.env`
- **Location:** `C:\Users\adm_r\Tools\LINEAR_AUTO\.env`
- **Endpoint:** `https://api.linear.app/graphql`

### Teams
| Team | Key | ID |
|------|-----|-----|
| Platypus | PLA | fd21180c-8619-4014-98c6-ac9eb8d47975 |
| Raccoons | RAC | 5a021b9f-bb1a-49fa-ad3b-83422c46c357 |
| Koala | KLA | fea84e7b-54e5-4b89-bf90-9967bdd2b90b |

### Scripts Disponiveis
- `create_linear_ticket.py` - Criar tickets via API
- `add_linear_comment.py` - Adicionar comentarios via API

---

---
### Sessao: 2026-01-27 14:00 - Keystone Payroll Duplication + February Release Prep
**Conquistas:**
- Keystone Payroll: 90 employees com erro, ~86 duplicados deletados manualmente
- Root cause identificado: processo QBO-side (nao TBX bug)
- Descoberta: michael_gugel+test1@intuit.com (real Intuit employee) em dados sinteticos
- Linear ticket PLA-3227 criado via API + worklog como comentario
- Linear API integrada com scripts Python
- February Release: 3 docs de orientacao para Alexandra

**Conhecimentos Adquiridos:**
- Linear GraphQL API: mutations para criar issues e comentarios
- QBO pode estar criando records via recovery/retry automatico
- IES Release process: Write it Straight -> UAT doc -> Siji George -> Feature Activation
- Pain point Intuit: nomes Dev vs Write It Straight

**Arquivos Criados:**
- `docs/WORKLOG_KEYSTONE_PAYROLL_DUPLICATION_2026-01-27.md`
- `docs/URGENTE_ALEXANDRA_FEB_RELEASE_2026-01-27.md`
- `docs/ORIENTACAO_ALEXANDRA_IES_RELEASE_2026-01-27.md`
- `knowledge-base/INTEL_IES_RELEASE_READINESS_2026-01-27.md`
- `create_linear_ticket.py`, `add_linear_comment.py`

**Proximo passo:** Postar report em #testbox-intuit-mm-external, Alexandra responder kat sobre February Release
---

---
### Sessao: 2026-01-27 22:00 - Deep Investigation Employee Duplication
**Conquistas:**
- Investigacao profunda no ambiente QBO (Manage Users)
- 6 usuarios Intuit com admin access identificados
- Custom role "Project Custom" criado 1/20/2026 descoberto (sem description, 0 users)
- Datasets analisados: 45 employees, 6 projects (vs 30+ no ambiente)
- Resposta tecnica formulada para Jason/Matt

**Conhecimentos Adquiridos:**
- QBO IAM: Custom roles requerem acao admin explicita
- QBO Audit: actor_id, timestamp, request_origin em cada mutation
- Raciocinio investigativo: Manage Users = primeiro passo para identificar atores

**Tecnica Aprendida:**
- Investigacao de anomalias: verificar quem tem write permissions antes de tudo
- Se dados aparecem sem explicacao, procurar authenticated actors

**Proximo passo:** Matt puxar Activity Log, Thiago postar response tecnica
---
