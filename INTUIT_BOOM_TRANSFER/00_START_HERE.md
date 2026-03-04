# INTUIT-BOOM - Guia de Onboarding para Novo Operador

> **LEIA ESTE DOCUMENTO PRIMEIRO**
> Este pacote contem TUDO que voce precisa para assumir o projeto INTUIT-BOOM.
> Tempo estimado de leitura completa: ~2 horas

---

## O QUE E ESTE PROJETO

INTUIT-BOOM e o maior e mais maduro projeto da TestBox. E a integracao com QuickBooks Online (QBO) da Intuit, cobrindo:

- **Validacao de features** QBO (Fall Release, Winter Release, IES releases)
- **Geracao de datasets** para 7+ ambientes demo (TCO, Construction, Canada, Manufacturing, etc.)
- **Automacao de login** e captura de evidencias via Playwright CDP
- **WFS (Workforce Solutions)** - nova linha de produto (GoCo + QB Payroll)
- **Ingestion pipeline** - CSVs com dados para importar via API/UI

**Tamanho:** ~200+ arquivos, 17 sessoes documentadas, 847 knowledge items, 5 datasets ativos

---

## GLOSSARIO ESSENCIAL

| Termo | Significado |
|-------|-------------|
| **TCO** | Traction Control Outfitters - flagship demo (multi-entity, 5 companies) |
| **Keystone** | Keystone Construction - 8 companies (Parent + 7 Children) |
| **IES** | Intuit Expert Services - time interno Intuit |
| **WFS** | Workforce Solutions - GoCo + QB Payroll (novo produto) |
| **Fall/Winter Release** | Ciclos de release Intuit (features novas validadas) |
| **CAMADA/LAYER** | Sistema de protecao de codigo (LOCKED/OPEN/REVIEW) |
| **Strategic Cortex** | Sistema de inteligencia com 5 outputs (A-E) |
| **SpineHUB** | Framework de persistencia de contexto Claude |
| **CDP** | Chrome DevTools Protocol (conexao Playwright) |
| **Evidence Pack** | Conjunto de screenshots + tracker Excel com hyperlinks |
| **TOTP** | Time-based One-Time Password (2FA) |
| **SOW** | Statement of Work |
| **Linear** | Ferramenta de project management (tickets PLA-, KLA-, RAC-, etc.) |
| **TSA** | Technical Solutions Architect |
| **CE** | Customer Engineer |
| **GTM** | Go-to-Market |

---

## ORDEM DE LEITURA (OBRIGATORIA)

| # | Documento | O que contem | Tempo |
|---|-----------|-------------|-------|
| 1 | **00_START_HERE.md** | Este documento (overview + glossario) | 5 min |
| 2 | **01_CLAUDE_MD_TRANSFER.md** | CLAUDE.md adaptado para novo operador | 10 min |
| 3 | **02_MEGA_MEMORY.md** | Memoria consolidada de TODAS as fontes | 20 min |
| 4 | **03_SOW_AND_SCOPE.md** | Escopo, releases, datasets, WFS | 10 min |
| 5 | **04_ECOSYSTEM_MAP.md** | Todos os projetos conectados ao INTUIT-BOOM | 10 min |
| 6 | **05_TECHNICAL_REFERENCE.md** | Ambientes, login, APIs, databases, scripts | 15 min |
| 7 | **06_RUNBOOKS.md** | Procedimentos operacionais passo-a-passo | 10 min |
| 8 | **07_CONTACTS_AND_STAKEHOLDERS.md** | Quem e quem (TestBox + Intuit) | 5 min |
| 9 | **08_RISK_MATRIX_AND_BLOCKERS.md** | Riscos, blockers, erros passados | 10 min |
| 10 | **09_CREDENTIALS_CHECKLIST.md** | Acessos a transferir | 5 min |
| 11 | **10_DECISIONS_LOG.md** | Todas as decisoes com contexto | 10 min |

---

## COMO USAR ESTE PACOTE

### Para o novo Claude (IA):
1. Copie `01_CLAUDE_MD_TRANSFER.md` como o novo `CLAUDE.md` do projeto
2. Copie `02_MEGA_MEMORY.md` como o novo `.claude/memory.md`
3. Leia todos os documentos na ordem acima
4. Execute `/status` para verificar estado atual

### Para o novo operador humano:
1. Leia todos os docs na ordem
2. Use `09_CREDENTIALS_CHECKLIST.md` para configurar acessos
3. Clone o repo Git: https://github.com/thiagotbx123/intuit-boom.git (verificar)
4. Configure `.env` com as credenciais
5. Teste login QBO: `python layer1_login.py`

---

## ESTADO ATUAL DO PROJETO (2026-02-06)

### Resumo Executivo
- **Fase:** Production - Feature Validation & Data Ingestion
- **Fall Release:** ENTREGUE (11/20/2025) - 100% PASS
- **Winter Release:** VALIDADO - 50/50 features (46 PASS, 2 PARTIAL, 2 N/A)
- **WAR ROOM 2026-02-05:** 30h sessao - Keystone dataset ingestion FINAL
- **WFS:** BLOQUEADO - aguardando decisao de environment (P0)
- **Datasets ativos:** 7 (TCO, Construction Sales/Events, Canada, Manufacturing, Nonprofit, ProServices)
- **Tickets Linear:** 443 Intuit-related (de 1,546 total)

### O Que ACABOU de Acontecer (2026-02-05)
- Sessao WAR ROOM de 30 horas para finalizar dataset Keystone Construction
- 5,087 bank transactions extraidas, 332 bills, 243 invoices, 3,993 time entries
- CSVs prontos para ingestion (VENDORS, CUSTOMERS, BILLS, INVOICES, TIME_ENTRIES)
- Alexandra executando ingestion de vendors/customers
- Time entries CSV FINAL pronto (3,972 entries)

---

*Pacote de transferencia criado em 2026-02-06*
*Fonte: 17 sessoes, 816 linhas de memory.md, Strategic Cortex, 5 projetos relacionados*
