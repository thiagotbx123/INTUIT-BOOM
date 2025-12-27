# INTUIT BOOM - Memory File

## Contexto Persistente

Este arquivo armazena informacoes importantes que devem persistir entre sessoes.

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
- Keystone Construction (Par.)
- Vista consolidada



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
