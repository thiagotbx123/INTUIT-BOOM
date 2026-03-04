# INTUIT-BOOM - Mega Memory Consolidada

> Fonte: `.claude/memory.md` (816 linhas) + sessions/ (17) + global memory + Strategic Cortex + QBO-WFS memory
> Compilado em: 2026-02-06

---

## ESTADO ATUAL (2026-02-06)

### Fase: Production - Feature Validation & Data Ingestion
- [x] Estrutura inicial criada
- [x] Sistema de camadas implementado
- [x] CAMADA 1 (Login) LOCKED
- [x] Fall Release ENTREGUE (11/20/2025)
- [x] Winter Release VALIDADO (50/50 features)
- [x] Strategic Cortex completo (5 outputs, 847 items)
- [x] WAR ROOM 2026-02-05 (30h, dataset Keystone FINAL)
- [ ] CAMADAS 2-5 owners nao definidos
- [ ] WFS environment decision (P0 BLOQUEADO)
- [ ] Ingestion CSVs prontos, aguardando execucao

---

## ULTIMAS ACOES (CRONOLOGICO REVERSO)

| Data | Acao | Resultado |
|------|------|-----------|
| 2026-02-05 | WAR ROOM Keystone 30h | 5,087 bank txns, 332 bills, 243 invoices, 3,993 time entries |
| 2026-02-05 | Alexandra finalizou employees | Iniciou vendors features |
| 2026-01-29 | 8 tickets Linear sprint | PLA-3013 resolved, PLA-2916 approved |
| 2026-01-29 | Canada: 50 bills para UNPAID | IDs 4139-4188 |
| 2026-01-27 | Employee Duplication fix | ~86 duplicados deletados |
| 2026-01-27 | Linear ticket PLA-3227 via API | Worklog como comentario |
| 2026-01-23 | SpineHUB Full Context Export | 1,500 linhas transferencia |
| 2026-01-20 | IC Balance Sheet Investigation | Bug escalado PLA-3201 |
| 2026-01-20 | Winter Release Gantt v9 Final | 29 features, 7 categorias |
| 2026-01-06 | IES February Release analise | Explicacao leigo criada |
| 2025-12-29 | Winter Release COMPLETO | 50/50 (46 PASS, 2 PARTIAL, 2 N/A) |
| 2025-12-29 | Evidence Pack completo | 30+ screenshots, Drive hyperlinks |
| 2025-12-29 | Feature Validator v2.0 | Sistema FLAGS criado |
| 2025-12-27 | Strategic Cortex build | 847 items, 7 riscos |
| 2025-12-27 | Linear full scan | 1,546 issues, 443 Intuit |
| 2025-12-19 | SpineHUB instalado | Sessions, memory, commands |
| 2025-12-06 | CAMADA 1 LOCKED | layer1_login.py validado |

---

## DATASETS ATIVOS

| Dataset | ID | Status | Companies |
|---------|----|--------|-----------|
| TCO | fab72c98-c38d-4892-a2db-5e5269571082 | ATIVO | 5 (Apex + 4 rollups) |
| Construction Sales | 321c6fa0-a4ee-4e05-b085-7b4d51473495 | ATIVO | 8 (Parent + 7 Children) |
| Construction Events | (same) | ATIVO | 8 |
| Canada | 2ed5d245-0578-43aa-842b-6e1e28367149 | ATIVO | TBD |
| Manufacturing | b6695ca6-9184-41f3-862e-82a182409617 | PARCIAL | TBD |
| Nonprofit | 3e1337cc-70ca-4041-bc95-0fe29181bb12 | PARCIAL | TBD |
| Professional Services | 58f84612-39db-4621-9703-fb9e1518001a | PARCIAL | TBD |

### TCO Companies
| Key | Nome | Company ID |
|-----|------|------------|
| apex | Apex Tire & Auto Retail, LLC | 9341455130166501 |
| consolidated | Vista consolidada | 9341455649090852 |
| global | Global Tread Distributors, LLC | 9341455130196737 |
| traction | Traction Control Outfitters, LLC | 9341455130188547 |
| roadready | RoadReady Service Solutions, LLC | 9341455130170608 |

### Construction Companies
| Key | Nome |
|-----|------|
| construction | Keystone Construction (Par.) - CID: 9341454156620895 |
| terra | Keystone Terra (Ch.) - CID: 9341454156620204 |
| (+ 6 children) | BlueCraft, Canopy, Ecocraft, Ironcraft, Stonecraft, Volt |

---

## WAR ROOM 2026-02-05 - RESULTADOS

### Entities Extraidas
| Entity | Quantidade | Status |
|--------|-----------|--------|
| Bank Transactions | 5,087 | EXTRAIDAS |
| Bills | 332 (IDs 105-436) | CSV PRONTO |
| Invoices | 243 (IDs 2460-2702) | CSV PRONTO |
| Vendors | 20 novos (IDs 34-53) | CSV PRONTO |
| Customers | 25 novos (IDs 51-75) | CSV PRONTO |
| Employees | 58 SALES (44 dataset + 14 novos) | VERIFICAR |
| Time Entries | 3,972 (FINAL) | CSV PRONTO |

### CSVs Gerados (prontos para ingestion)
```
Downloads/INTUIT BOOM DOWNLOAD/
├── PLA-3261_TIME_ENTRIES_FINAL.csv      # 3,972 entries
├── INGESTION_BILLS.csv                   # 332 (IDs 105-436)
├── INGESTION_INVOICES.csv                # 243 (IDs 2460-2702)
├── INGESTION_VENDORS_NEW.csv             # 20 (IDs 34-53)
├── INGESTION_CUSTOMERS_NEW.csv           # 25 (IDs 51-75)
```

### Regras de Ingestion
1. **Sequential IDs:** Sempre MAX(id) + 1
2. **FK Order:** Vendors/Customers ANTES de Bills/Invoices
3. **Temporal Consistency:** Dates within project periods
4. **FK type = PK type** da tabela referenciada

---

## WINTER RELEASE FY26 VALIDATION

| Ambiente | Total | PASS | PARTIAL | N/A |
|----------|-------|------|---------|-----|
| TCO | 25 | 25 | 0 | 0 |
| Construction | 25 | 21 | 2 | 2 |
| **TOTAL** | **50** | **46** | **2** | **2** |

**Features por Categoria:**
- AI Agents: 8/8 PASS
- Reporting: 7/7 PASS
- Dimensions: 4/4 PASS
- Workflow: 1/1 PASS
- Migration: 3/3 PASS
- Construction: 2/2 PASS
- Payroll: 4/4 PASS

---

## FALL RELEASE STATUS

- **Entregue:** 11/20/2025
- **TCO/Construction:** Validados
- **Manufacturing/Nonprofit:** 95%
- **Reclassificado como:** Process improvement (nao entrega pendente)

---

## WFS (WORKFORCE SOLUTIONS)

### Status: BLOQUEADO
- **Bloqueio P0:** Intuit precisa decidir environment (new vs existing)
- **Owner:** Alexandra Lacerda (Primary TSA)
- **Timeline:** Alpha Dez/25, Beta Fev/26, GA Mai/26
- **SOW:** Draft v2 (bloqueado ate decisao env)

### Demo Stories
1. Unified PTO - employee > manager > payroll admin
2. Magic Docs - AI doc generation + e-signature
3. Hire to fire lifecycle
4. Job costing

### Recomendacao TestBox: Hybrid Approach
1. Phase 1: Build new isolated env (Weeks 1-4)
2. Phase 2: Stabilize and validate (Weeks 5-6)
3. Phase 3: Evaluate integration post-Beta

---

## RISCOS ATIVOS

| # | Risco | Impacto | Status |
|---|-------|---------|--------|
| 1 | WFS Environment Decision | P0 | PENDING |
| 2 | Negative Inventory TCO | P1 | PLA-2916 (Douglas approved) |
| 3 | Login ECS Task | P1 | PLA-3013 (RESOLVED) |
| 4 | Canada Data Bills | P1 | PLA-2969 BACKLOG |
| 5 | WFS SOW Finalization | P1 | IN PROGRESS |
| 6 | Demo Load Time >20s | P2 | KLA-2337 |
| 7 | Manufacturing Visibility | P2 | 6 files only |

---

## TICKETS LINEAR RECENTES

| Ticket | Titulo | Status |
|--------|--------|--------|
| PLA-3261 | Time Entries Ingestion | CSV READY |
| PLA-3227 | Keystone Employee Duplication | RESOLVED |
| PLA-3201 | IC Balance Sheet Bug | ESCALATED |
| PLA-3013 | Login Task Failing | RESOLVED |
| PLA-2969 | Canada Bills | BACKLOG |
| PLA-2949 | TCO Bank Rules | BACKLOG |
| PLA-2916 | Negative Inventory | IN PROGRESS |
| PLA-2932 | Contractors Documents | IN PROGRESS |

---

## CORTEX SYSTEM (INTELIGENCIA)

### Metricas
| Fonte | Total | Relevantes | % |
|-------|-------|------------|---|
| Drive | 20,426 | 1,926 | 9.4% |
| Slack | 10 canais | 500+ msgs | ~80% |
| Linear | 1,546 | 443 Intuit | 28.7% |

### 5 Outputs do Strategic Cortex
| Output | Arquivo | Uso |
|--------|---------|-----|
| A | OUTPUT_A_EXECUTIVE_SNAPSHOT.md | Status rapido - LER PRIMEIRO |
| B | OUTPUT_B_STRATEGIC_MAP.md | Conexoes e arquitetura |
| C | OUTPUT_C_KNOWLEDGE_BASE.json | Dados estruturados (847 items) |
| D | OUTPUT_D_KEYWORD_MAP_LINEAR_RECIPES.md | Busca rapida |
| E | OUTPUT_E_DELTA_SUMMARY.md | Mudancas recentes |

---

## DECISOES IMPORTANTES

| Data | Decisao | Motivo |
|------|---------|--------|
| 2026-01-29 | Canada tickets para backlog | Nao prioridade agora |
| 2026-01-29 | Initial Quantity (inventory) | Evita COGS hit, usa OBE |
| 2026-01-29 | Pre-build data approach | Proven no Fall Release |
| 2025-12-22 | Fall Release = process improvement | Reclassificado |
| 2025-12-17 | GoQuick Alpha != sales demo | Evita confusao WFS |
| 2025-12-15 | Staged rollout WFS | Protege sellers |
| 2025-12-06 | Layer system LOCKED/OPEN/REVIEW | Protege codigo |

---

## OPEN QUESTIONS

- Qual ambiente final para WFS sales demo?
- Qual timeline oficial do Winter Release?
- Quais dados fluem de QBO para MineralHR?
- Status real do Manufacturing dataset?
- Demo Health Check vira servico?

---

## LEARNINGS CRITICOS (PARA NAO REPETIR)

### 5 Erros Graves da Winter Release Construction
1. **Escopo incompleto:** 4 features validadas em vez de 25
2. **Falta paridade:** Tracker Construction pobre vs TCO
3. **Screenshots invalidos:** 5 paginas 404 nao detectadas
4. **Status binario:** Nao diferenciava PARTIAL de NOT_AVAILABLE
5. **Notes genericas:** Nao descreviam conteudo real

### 6 Regras Canonicas de Validacao
1. Screenshot DEVE provar a feature especifica
2. Contexto correto OBRIGATORIO (multi-entity = Consolidated)
3. N/A = Documentacao, nao falha
4. Agrupar por contexto (trocar empresa UMA VEZ)
5. 404 = INVESTIGAR (alternativa, web, NOT_AVAILABLE)
6. Ambiente especifico = ambiente especifico (CA != Canada)

### Communication Style
- Respostas simples vencem (Kat prefere direto)
- Mostrar conhecimento tecnico da credibilidade
- "tipo espelho - tem que bater" > explicacao longa
- Mencionar AI-assisted scripting acelera entregas

---

*Compilado de 17 sessoes + 816 linhas memory.md + Strategic Cortex + QBO-WFS memory*
