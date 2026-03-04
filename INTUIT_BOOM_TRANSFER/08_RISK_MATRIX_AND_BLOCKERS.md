# INTUIT-BOOM - Risk Matrix e Blockers

---

## BLOCKERS ATIVOS (Precisam Atencao Imediata)

| # | Blocker | Ticket | Severidade | Dono | Status | Acao |
|---|---------|--------|------------|------|--------|------|
| 1 | **WFS Environment Decision** | - | P0 | Christina Duarte | PENDING | Reuniao de decisao pendente |
| 2 | **Time Entries Ingestion** | PLA-3261 | P1 | Alexandra | CSV READY | 3,972 entries prontas |
| 3 | **Vendors/Customers Ingestion** | - | P1 | Alexandra | CSV READY | 20 vendors + 25 customers |
| 4 | **Bills/Invoices Ingestion** | - | P1 | Alexandra | CSV READY | 332 bills + 243 invoices |
| 5 | **28 Employees nao no Dataset** | - | P1 | Verificar | OPEN | SALES tem 58, dataset tem 44 |

---

## RISCOS ESTRATEGICOS

| # | Risco | Prob. | Impacto | Mitigacao | Owner |
|---|-------|-------|---------|-----------|-------|
| 1 | WFS environment decision atrasa | ALTA | P0 | Doc pros/cons para Christina | Katherine |
| 2 | Manufacturing visibility gap | MEDIA | P2 | Apenas 6 arquivos, verificar com Intuit | TSA |
| 3 | Demo load time >20s | MEDIA | P2 | KLA-2337 - Pamela assigned | Engineering |
| 4 | Login ECS instabilidade | BAIXA | P1 | PLA-3013 resolvido, monitorar | Augusto |
| 5 | Canada data incomplete | MEDIA | P1 | Bills line items vazio, backlog | Lucas T. |
| 6 | Fusion UI migration impact | MEDIA | P2 | Timeline unclear | Intuit |
| 7 | SOW WFS finalization | ALTA | P1 | Depende de P0 (environment) | Katherine |

---

## BLOCKERS LINEAR (HISTORICO)

| Issue | Titulo | Team | Assignee | Status |
|-------|--------|------|----------|--------|
| PLA-3261 | Time Entries Ingestion | Platypus | - | CSV READY |
| PLA-3227 | Keystone Employee Duplication | Platypus | - | **RESOLVED** |
| PLA-3201 | IC Balance Sheet Bug | Platypus | Engineering | ESCALATED |
| PLA-3013 | Login task failing TCO | Platypus | Augusto | **RESOLVED** |
| PLA-2969 | Canada Data Bills | Platypus | Lucas T. | BACKLOG |
| PLA-2949 | TCO Bank Rules | Platypus | - | BACKLOG |
| PLA-2916 | Negative Inventory | Platypus | Douglas | IN PROGRESS |
| PLA-2932 | Contractors Documents | Platypus | Douglas | IN PROGRESS |
| PLA-2883 | Error ingesting activities | Platypus | Augusto | BLOCKED |
| PLA-2724 | Dimensions in Payroll | Platypus | Eyji | BLOCKED |
| KLA-2337 | Demo load time >20s | Koala | Pamela | TODO |

---

## RISCOS RESOLVIDOS (Historico)

| Risco | Status | Data | Como Resolveu |
|-------|--------|------|---------------|
| Fall Release deadline | RESOLVIDO | 11/20/2025 | Entregue no prazo |
| Winter Release validation | RESOLVIDO | 12/29/2025 | 50/50 features validadas |
| Login CAPTCHA bypass | RESOLVIDO | 01/29/2026 | Augusto configurou test users |
| Employee duplication | RESOLVIDO | 01/27/2026 | 86 duplicados deletados manualmente |
| IC Balance Sheet | ESCALADO | 01/20/2026 | Bug de sistema, PLA-3201 |
| Construction validation | CORRIGIDO | 12/29/2025 | Re-validado com 25 features (era 4) |

---

## ERROS PASSADOS (PARA NAO REPETIR)

| Erro | Consequencia | Licao |
|------|-------------|-------|
| Validar apenas 4 features Construction (devia ser 25) | Tracker rejeitado, retrabalho | IES = TODAS features, nao subset |
| Screenshots de 404 nao detectados | 5 falsos positivos | ~140KB = provavel erro. Verificar conteudo |
| Status binario (PASS/FAIL) | Nao diferenciou PARTIAL de NOT_AVAILABLE | Usar 5 status granulares |
| Evidence notes genericas | Nao descreviam conteudo real | Template tecnico obrigatorio |
| Nao comparar ambientes | Diferencas nao documentadas | Side-by-side obrigatorio |
| Espera de 10s (devia ser 30-45s) | QBO nao carregava | QBO e LENTO, esperar 30-45s |
| Contexto errado (Individual vs Consolidated) | Screenshot nao prova feature | Verificar header ANTES de capturar |
| michael_gugel+test1@intuit.com em dados sinteticos | Real Intuit employee misturado | Auditar emails antes de publicar |

---

## MONITORAMENTO RECOMENDADO

### Semanal
- [ ] Verificar status ingestion CSVs (Alexandra)
- [ ] Verificar WFS environment decision (Katherine)
- [ ] Atualizar Linear tickets com progresso
- [ ] Verificar se novos blockers surgiram

### Quinzenal
- [ ] Sync com engineering sobre blockers
- [ ] Update Strategic Cortex (SpineHub collect)
- [ ] Verificar Manufacturing visibility
- [ ] Report para Katherine se necessario

### Pre-Release
- [ ] Identificar TODAS features do release
- [ ] Pre-build foundation data
- [ ] Aguardar feature flags
- [ ] Validar com framework v2.0

---

*Compilado de memory.md, Linear tickets, Strategic Cortex, sessions/*
