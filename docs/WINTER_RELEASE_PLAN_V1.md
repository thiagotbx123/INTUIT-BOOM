# PLANO WINTER RELEASE V1
**Status**: DRAFT com suposicoes
**Gerado**: 2025-12-29

---

## SUPOSICOES ATIVAS

| ID | Suposicao | Risco | Validar |
|----|-----------|-------|---------|
| S1 | Early Access 4/Fev/2026 | Timeline errado | Katherine |
| S2 | TCO e Construction sao core | Escopo incompleto | Intuit |
| S3 | Login precisa workaround | Delay automacao | PLA-3013 |
| S4 | Datasets de Nov/2025 | Dados obsoletos | Verificar |
| S5 | Jan 6-31 janela trabalho | Recursos errados | Holidays |
| S6 | Agents AI sao P0 | Prioridade errada | Tracker |

---

## ARTEFATO 1: RELEASE MAP E PRIORIDADES

### P0 - Bloqueia Demo/Narrative
| Feature | Ambiente | Risco | Dados Necessarios |
|---------|----------|-------|-------------------|
| Accounting AI | TCO | Alto | Bank feeds, transacoes |
| Project Management AI | Construction | Alto | Projetos, budgets |
| Sales Tax AI | TCO | Alto | Sales tax config |
| KPIs and Dashboards | TCO/Const | Medio | Metricas |
| Dimension Assignment v2 | TCO | Medio | Dimensions |

### P1 - Importante
| Feature | Ambiente | Risco |
|---------|----------|-------|
| Finance AI | TCO | Medio |
| Solutions Specialist | IES | Medio |
| Management Reports | TCO/Const | Baixo |
| Calculated Fields | TCO | Baixo |
| Multi-Entity Reports | TCO | Medio |

### P2 - Nice to have
| Feature | Ambiente | Notas |
|---------|----------|-------|
| Conversational BI | TCO | Beta |
| Omni Intelligence | TCO | Handraiser |
| Parallel Approval | Construction | Workflow |

---

## ARTEFATO 2: MATRIZ DE AMBIENTES

### TCO
- Tipo: Multi-Entity (1 parent + 3 children)
- Objetivo: Flagship QBO Advanced, AI features
- Features: Accounting AI, Sales Tax AI, Finance AI, KPIs, Dimensions v2

### Construction Sales
- Tipo: IES Construction
- Objetivo: Desktop parity, seller flows
- Features: Project Management AI, CPR, Sales Order

### Construction Events
- Tipo: IES Events
- Objetivo: Stadium projects
- Features: Project Management AI

---

## ARTEFATO 3: PLANO DE EXECUCAO

### Etapa A: Acesso e Estabilidade (Dia 1-2)
- Testar login manual em cada ambiente
- Verificar Chrome CDP porta 9222
- Documentar bloqueios

### Etapa B: Baseline de Dados (Dia 2-4)
- Verificar datas dos datasets
- Contar registros principais
- Identificar gaps

### Etapa C: Baseline de UI (Dia 3-5)
- Navegar rotas principais
- Confirmar permissoes
- Screenshots baseline

### Etapa D: Validacao Features (Dia 5-15)
- Validar P0 com evidencias
- Validar P1
- Registrar pass/fail

### Etapa E: Evidencias e Tracker (Dia 15-18)
- Organizar screenshots
- Atualizar tracker
- Resumo executivo

### Etapa F: Triagem (Dia 18-25)
- Classificar falhas
- Aplicar fixes
- Abrir tickets

### Etapa G: Re-teste (Dia 25-30)
- Re-testar correcoes
- Tracker final
- Handoff


---

## ARTEFATO 4: PLAYBOOKS

### Playbook 1: Login e Sanity Check
1. Abrir Chrome com --remote-debugging-port=9222
2. Executar layer1_login.py
3. Verificar dashboard carrega
4. Registrar OK ou FAIL

### Playbook 2: Health Check de Dados
1. Carregar JSON/SQLite
2. Contar: Customers(50+), Vendors(30+), Employees(10+)
3. Verificar FKs e campos obrigatorios
4. Registrar inventario

### Playbook 3: Feature Check
1. Confirmar pre-requisitos de dados
2. Navegar para feature
3. Validar comportamento
4. Capturar screenshot
5. Registrar PASS/FAIL/PARTIAL

### Playbook 4: Triagem de Falha
1. Identificar sintoma
2. Classificar: Dado ausente, Desconectado, UI gap, Permissao, Flag, Bug, Tooling
3. Decidir acao: Fix manual, Re-ingest, Ticket, Pergunta Intuit
4. Documentar

### Playbook 5: Re-teste
1. Identificar fix aplicado
2. Repetir Playbook 3
3. Comparar resultados
4. Atualizar tracker

---

## ARTEFATO 5: TRIAGEM

### Categorias de Falha
- Cat 1: Dado ausente -> Re-ingest
- Cat 2: Dado desconectado -> Re-ingest ou fix
- Cat 3: UI nao expoe -> Pergunta Intuit
- Cat 4: Permissao/role -> Pergunta Intuit
- Cat 5: Flag/rollout -> Pergunta Intuit
- Cat 6: Bug produto -> Ticket
- Cat 7: Tooling -> Fix manual

---

## ARTEFATO 6: COMUNICACAO

### Update Diario (Slack)
- Status por ambiente
- Features validadas
- Bloqueadores
- Proximos passos

### Resumo Semanal
- Progresso P0/P1
- Riscos
- Decisoes necessarias
- Timeline status

---

## CAMINHO PARA VALOR EM 48H

### Hora 0-4: Setup
- Confirmar Chrome CDP ativo
- Testar login TCO manual
- Testar login Construction Sales manual

### Hora 4-12: Health Check Rapido
- Verificar 3 rotas principais TCO
- Verificar 3 rotas principais Construction
- Documentar bloqueios

### Hora 12-24: Baseline de Dados
- Contar registros principais TCO
- Contar registros principais Construction
- Identificar gaps obvios

### Hora 24-36: Validacao P0 Inicial
- Testar Accounting AI (se disponivel)
- Testar KPIs and Dashboards
- Testar Dimension Assignment v2

### Hora 36-48: Primeiro Report
- Gerar Health Check por ambiente
- Listar bloqueadores
- Propor proximos passos

---

Documento gerado automaticamente
Sujeito a revisao apos respostas das 15 perguntas
