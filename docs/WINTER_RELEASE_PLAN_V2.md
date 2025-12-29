# PLANO WINTER RELEASE V2
**Status**: CONFIRMADO (respostas processadas)
**Gerado**: 2025-12-29
**Early Access**: 4/Fev/2026 (CONFIRMADO)

---

## SUPOSICOES ATUALIZADAS

| ID | Suposicao | Status | Notas |
|----|-----------|--------|-------|
| S1 | Early Access 4/Fev/2026 | CONFIRMADO | Katherine confirmou |
| S2 | TCO e Construction sao core | CONFIRMADO | Ambientes prioritarios |
| S3 | Login funciona | CONFIRMADO | TCO e Construction OK |
| S4 | Datasets atualizados | CONFIRMADO | QBO_DATABASE_COMPLETO.xlsb (74 sheets, ~1.1M registros) |
| S5 | Canada/Manuf/Nonprofit | ADIADO | Podem ser ignorados agora |
| S6 | Sem budget re-ingest | CONFIRMADO | Nao criar tickets engenharia |
| S7 | Prioridade por complexidade | CONFIRMADO | Usar complexidade + ordem cliente |

---

## COBERTURA DE DADOS CONFIRMADA

### QBO_DATABASE_COMPLETO.xlsb - Destaques

| Tabela | Registros | Features Suportadas |
|--------|-----------|---------------------|
| invoices | 44,823 | Accounting AI, Sales Tax AI |
| invoice_line_items | 115,725 | Dimensions, Reporting |
| invoice_classifications | 776,367 | Multi-Dimensional Reports |
| time_entries | 62,997 | Project AI, Time Tracking |
| customers | 10,615 | Customer Agent, Sales Tax |
| employees | 1,695 | Payroll AI |
| projects | 39 | Project Management AI |
| dimensions | 49 | Dimension Assignment v2 |
| workflow_automations | 8 | Workflow Automation |
| intercompany_journals | 72 | Multi-Entity |

**CONCLUSAO**: Database SUFICIENTE para 100% das features Winter Release

---

## FEATURE REUSE ANALYSIS

| Status | Count | % | Acao |
|--------|-------|---|------|
| REUSE | 21 | 58% | Reutilizar Fall Release |
| ADAPT | 6 | 17% | Adaptar automacao existente |
| NEW | 6 | 17% | Criar nova automacao |
| MANUAL | 3 | 8% | Validacao manual |

**CONCLUSAO**: 75% do trabalho ja esta pronto (Fall Release)

---

## ARTEFATO 1: RELEASE MAP V2

### P0 - Bloqueia Demo (Complexidade ALTA)
| # | Feature | Ambiente | Fall Ref | Acao | Dados OK |
|---|---------|----------|----------|------|----------|
| 1 | Accounting AI | TCO | TCO-025 | REUSE + novos sub-features | SIM |
| 2 | Project Management AI | TCO/Const | TCO-029 | ADAPT (Budget, Profitability) | SIM |
| 3 | Sales Tax AI | TCO | TCO-032 | ADAPT (Pre-file check) | SIM |
| 4 | KPIs Customizados | TCO | TCO-006, TCO-007 | REUSE | SIM |
| 5 | Dimension Assignment v2 | TCO | TCO-001 | ADAPT | SIM |

### P1 - Importante (Complexidade MEDIA)
| # | Feature | Ambiente | Fall Ref | Acao | Dados OK |
|---|---------|----------|----------|------|----------|
| 6 | Finance AI | TCO | TCO-030 | REUSE | SIM |
| 7 | Dashboards | TCO/Const | TCO-008 | REUSE | SIM |
| 8 | Management Reports | TCO | TCO-011 | REUSE | SIM |
| 9 | Multi-Entity Reports | TCO | - | NEW | SIM |
| 10 | Hierarchical Dimensions | TCO | - | NEW | SIM |

### P2 - Nice to Have (Complexidade BAIXA)
| # | Feature | Ambiente | Fall Ref | Acao |
|---|---------|----------|----------|------|
| 11 | Solutions Specialist | TCO | TCO-031 | ADAPT |
| 12 | Customer Agent | TCO | TCO-027 | REUSE |
| 13 | Calculated Fields | TCO | TCO-009 | ADAPT |
| 14 | Parallel Approval | Const | - | NEW |

### P3 - Baixa Prioridade
| # | Feature | Notas |
|---|---------|-------|
| 15 | Omni Intelligence | Beta/Handraiser |
| 16 | Conversational BI | Se disponivel |
| 17 | Migration features | MANUAL |

---

## ARTEFATO 2: MATRIZ DE AMBIENTES V2

### TCO (PRIORIDADE 1)
- **Tipo**: Multi-Entity (Parent + 3 Children)
- **Login**: CONFIRMADO OK
- **Features**: 30+ (full IES)
- **Foco**: AI Agents, KPIs, Dimensions, Multi-Entity

### Construction Sales (PRIORIDADE 1)
- **Tipo**: IES Construction
- **Login**: CONFIRMADO OK
- **Features**: 25+ (construction focus)
- **Foco**: Project AI, Certified Payroll, Cost Groups

### Canada (ADIADO)
### Manufacturing (ADIADO)
### Nonprofit (ADIADO)

---

## ARTEFATO 3: PLANO DE EXECUCAO V2

### Etapa A: Acesso e Estabilidade (HOJE)
- [x] Confirmar login TCO
- [x] Confirmar login Construction
- [ ] Verificar Chrome CDP porta 9222
- [ ] Executar health check rapido

### Etapa B: Baseline de Dados (COMPLETO)
- [x] QBO_DATABASE_COMPLETO.xlsb analisado
- [x] 74 sheets, ~1.1M registros
- [x] Cobertura 100% features Winter

### Etapa C: Validacao Fall Release REUSE (Dia 1-3)
- [ ] Executar 21 features REUSE TCO
- [ ] Confirmar funcionamento
- [ ] Documentar gaps

### Etapa D: Adaptacao Features ADAPT (Dia 3-7)
- [ ] Accounting AI - novos sub-features
- [ ] Project AI - Budget creation
- [ ] Sales Tax AI - Pre-file check
- [ ] Dimension v2 - enhancements
- [ ] Solutions Specialist - Business Feed
- [ ] Calculated Fields

### Etapa E: Criacao Features NEW (Dia 7-14)
- [ ] Multi-Entity Reports
- [ ] Hierarchical Dimensions
- [ ] Dimensions on Workflow
- [ ] Dimensions on Balance Sheet
- [ ] Parallel Approval
- [ ] Multi-Entity Payroll Hub

### Etapa F: Validacao Construction (Dia 14-18)
- [ ] Aplicar automacoes TCO adaptadas
- [ ] Features construction-specific
- [ ] Certified Payroll

### Etapa G: Tracker e Handoff (Dia 18-21)
- [ ] Tracker final
- [ ] Resumo executivo
- [ ] Handoff Intuit

---

## ARTEFATO 4: PLAYBOOKS V2

### Playbook 1: Health Check Rapido
```
1. Abrir Chrome com --remote-debugging-port=9222
2. Acessar TCO: https://qbo.intuit.com/app/homepage
3. Verificar: Dashboard carrega, Menu lateral OK
4. Navegar: Reports > Dashboards
5. Navegar: Banking
6. Status: OK/FAIL
```

### Playbook 2: Validacao Feature REUSE
```
1. Carregar features_rich.json
2. Localizar feature por ref (ex: TCO-025)
3. Navegar para route
4. Aguardar wait_for
5. Capturar screenshot
6. Comparar com evidence.filename_pattern
7. Status: PASS/FAIL/PARTIAL
```

### Playbook 3: Adaptacao Feature ADAPT
```
1. Identificar feature base no Fall Release
2. Listar novos sub-features Winter
3. Expandir automacao existente
4. Testar novos paths
5. Atualizar features_rich.json
6. Status: ADAPTED/BLOCKED
```

### Playbook 4: Criacao Feature NEW
```
1. Analisar spec Winter Release
2. Identificar dados necessarios em QBO_DATABASE
3. Criar entry em features_rich.json
4. Implementar navegacao
5. Definir evidence pattern
6. Testar end-to-end
7. Status: CREATED/BLOCKED
```

---

## ARTEFATO 5: TRIAGEM V2

### Categorias de Falha (sem re-ingest)
| Cat | Tipo | Acao | Responsavel |
|-----|------|------|-------------|
| 1 | Dado ausente | Criar manualmente | TestBox |
| 2 | UI gap | Workaround ou skip | TestBox |
| 3 | Permissao | Verificar role | Intuit |
| 4 | Flag nao habilitado | Pergunta | Intuit |
| 5 | Bug produto | Documentar | Intuit |
| 6 | Tooling erro | Fix interno | TestBox |

**NOTA**: Nao abrir tickets de re-ingest (sem budget engenharia)

---

## ARTEFATO 6: COMUNICACAO V2

### Canal Principal
- Slack: C06PSSGEK8T (Intuit channel)
- DM Katherine: D09N49AG4TV

### Update Diario
```
[DATA] Winter Release Update

AMBIENTES:
- TCO: [STATUS]
- Construction: [STATUS]

FEATURES VALIDADAS: X/30
- P0: X/5
- P1: X/5
- P2: X/4

BLOQUEADORES:
- [Lista]

PROXIMOS PASSOS:
- [Lista]
```

---

## CAMINHO PARA VALOR - 48H ATUALIZADO

### Hora 0-2: Setup Confirmado
- [x] Login TCO OK
- [x] Login Construction OK
- [ ] Chrome CDP verificar

### Hora 2-8: Fall Release Baseline
- [ ] Executar 5 features REUSE TCO
- [ ] TCO-025 Accounting AI
- [ ] TCO-006 KPIs Library
- [ ] TCO-008 Dashboards
- [ ] TCO-001 Dimension Assignment
- [ ] TCO-030 Finance AI

### Hora 8-16: Confirmar Gaps
- [ ] Listar sub-features novos Winter
- [ ] Identificar o que precisa ADAPT
- [ ] Priorizar por complexidade

### Hora 16-32: Primeiras Adaptacoes
- [ ] Accounting AI - Ready to Post batch
- [ ] Sales Tax AI - Pre-file check
- [ ] Project AI - Budget creation

### Hora 32-48: Primeiro Report
- [ ] Status por feature
- [ ] % completude
- [ ] Bloqueadores
- [ ] Timeline atualizado

---

## PROXIMA ACAO IMEDIATA

**Iniciar Etapa A**: Verificar Chrome CDP e executar health check em TCO e Construction

```bash
# Verificar Chrome com CDP
# Se Chrome nao esta aberto com CDP:
chrome.exe --remote-debugging-port=9222

# Health check via Python
cd /c/Users/adm_r/intuit-boom
python -c "
from playwright.sync_api import sync_playwright
p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://localhost:9222')
contexts = browser.contexts
print(f'Contexts: {len(contexts)}')
for ctx in contexts:
    for page in ctx.pages:
        print(f'Page: {page.url}')
"
```

---

Documento atualizado com respostas processadas
Winter Release FY26 - TestBox Validation Plan
