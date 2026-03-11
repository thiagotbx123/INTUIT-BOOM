# OUTPUT A - Executive Snapshot

> Strategic Intelligence - Intuit/TestBox Project
> Updated: 2026-03-11 (auto-collected via Linear API + Slack API + Drive API)
> Sources: Linear (55 issues last 7d), Slack (318 msgs, 11 channels), Google Drive (17 Intuit files)

---

## INCIDENTE P0 — Demo Playbooks Outage (Mar 9)

| Aspecto | Detalhe |
|---------|---------|
| **O que aconteceu** | 45 sellers Intuit (Mailchimp) carregaram Demo Playbooks simultaneamente, sobrecarregando Saturn service |
| **Impacto** | App em loading infinito. Training cancelado. Email do Chief Sales Officer Intuit pro Sam (CEO TestBox) |
| **Root cause** | `DemoScriptStepSerializer` chama Saturn desnecessariamente a cada page load (KLA-2478) |
| **Fix** | PR #2643 (Pamela) — tornar `convert_use_cases` opt-in. WOM-544 dobrou CPU/memoria Saturn |
| **ETA** | Merge Mar 11-12, stress test com Locust + 1000 test users em staging |
| **Pivot** | Juhan criou 6/9 videos async (Loom). Training presencial adiado pra Mar 27 (office hours) |

**Pessoas-chave:** Katherine (PM), Alex Nauda (CTO), Pamela (Core), Lucas Soranzo, Gabriel Taufer, Sam, Deyton

---

## ONDE ESTAMOS AGORA

### QBO / QuickBooks — Winter Release Validation
| Ambiente | Status | Score | Data |
|----------|--------|-------|------|
| Non-Profit (NV2) | DONE | 7.5/10 | Mar 5 |
| Professional Services (Summit) | DONE | 74/100 | Mar 10 |
| Events (QSP) | DONE | 7.5/10 | Mar 6 |
| Mid Market | DONE | 6.5/10 | Mar 6 |
| Product Events | DONE | 5/10 | Mar 6 |
| QBOA Mid Market | DONE | - | Mar 10 |
| Manufacturing | IN PROGRESS | - | Mar 11 (Alexandra) |
| Close-out gaps | PENDING | - | ETA Mar 12-13 |

**6/8 ambientes validados. ETA conclusao: Mar 12-13.**

### QBO — Issues Ativos (Linear)
| Ticket | Titulo | Status | Priority | Assignee |
|--------|--------|--------|----------|----------|
| PLA-3256 | Dataset vs SALES Audit - Master Worklog | Backlog | URGENT | Thiago |
| PLA-3332 | P&L negative Professional Services | Refinement | - | Thiago |
| PLA-3336 | Bank Connection Error Linked Accounts | Refinement | Medium | Soranzo |
| PLA-3213 | Winter Release Staging - TCO Clone | Paused | Low | Augusto |

### QBO — Issues Resolvidos Recentes (Mar 4-11)
| Ticket | Titulo | Assignee |
|--------|--------|----------|
| PLA-2629 | Convert constraints to code validation | Eyji |
| PLA-2474 | Remove expiration from failed activities | Augusto |
| PLA-2450 | Migrate legacy activity plans to new format | Augusto |
| PLA-2297 | Refactor transaction confirmation logic | Augusto |
| PLA-2417 | Move matching of bank transactions into queue | Augusto |
| PLA-2412 | State machine step to delete employees | Augusto |
| PLA-2866 | Data Ingest - Products and Services | Torresan |
| PLA-2795 | No time entries for IES Construction | Soranzo |
| SEC-197 | Fix saved data | Douglas |
| PLA-2699 | Move NV3 to production | Soranzo |

**~35+ issues fechados ou cancelados no Mar 10 (sprint close/grooming).**

### QBO — Cron Schedules (via Soranzo, Mar 6)
| Atividade | Schedule |
|-----------|----------|
| Approve time entries | Fridays 01:00 |
| Ingest bills for review | Mon/Fri 18:00 |
| Send invoices | Daily 16:00 |
| Pay invoices | Daily 17:00 (legacy) |
| Retool dashboard | `retool.testbox.com/apps/026deb70.../Integrations/Quickbooks` |

### WFS (Workforce Solutions)
| Aspecto | Status |
|---------|--------|
| SOW | Alexandra revisando comments Intuit, draft v1.5 |
| Milestones chapter | Em preparacao |
| Pre-scoping questions | Em preparacao pra Intuit |

### Mailchimp Seller Launch
| Aspecto | Status |
|---------|--------|
| Sellers provisioned | 43 com Standard access (Mar 5) |
| Email blocking | 17 invites bloqueados por iphmx.com (554 poor reputation) |
| Workaround | SSO/direct links |
| Training | 6/9 videos Loom prontos (Juhan). 3 restantes ETA quinta |
| Office hours | Remarcado pra Mar 27 |

---

## NOVO REQUEST — Multi-Entity Dimensions (Mar 11, HOJE)

Request via canal externo Intuit: 5 empresas Keystone com shared dimensions (Project Type + Marketing Channel), ~1000 transactions com dimensions randomizados (min 15 por valor).

**Status:** Katherine escalou pra Intuit project team (mhrabinski, cduarte) — nenhum dos dois tinha contexto. Adicionado a agenda de hoje. **Sem acao TSA ate ter mais contexto.**

---

## DRIVE — Arquivos Intuit Modificados (Mar 4-11)

| Data | Arquivo | Autor |
|------|---------|-------|
| Mar 11 | **Intuit All Action Items** (GSheet) | Katherine Lu |
| Mar 11 | Intuit_usersworkspace_march32026.xlsx | Thiago |
| Mar 10 | QBO_PLAYBOOK_COCKPIT.xlsx | Thiago |
| Mar 10 | PLANO_TRANSICAO_ALEXANDRA_INTUIT.xlsx | Thiago |
| Mar 08 | QBO_AUTOMATION_MAP.xlsx | Thiago |
| Mar 08 | QBO_ENVIRONMENT_MASTER.xlsx | Thiago |
| Mar 06 | **QBO and WFS sync** - Notes by Gemini | Alexandra |

---

## DEV-ALERTS & POOL STATUS

| Integration | Status | Nota |
|-------------|--------|------|
| Tropic | OK (Mar 8-9) | Flag cosmetic nao limpa em retry |
| CallRail | OK | Home Services trials confirmados |
| Brevo German | ALERT (Mar 10-11) | Contact attribute issue, 2 trials falharam, pool normalizado 4/4 |
| Gong | ALERTA (Mar 11) | Pool idle, Soranzo re-habilitou ingestion. Torresan = primary |

---

## RISCOS ATIVOS

| # | Risco | Impacto | Status |
|---|-------|---------|--------|
| 1 | **Demo Playbooks P0** | Sellers Intuit sem acesso a training | PR #2643 em merge |
| 2 | **PLA-3256 Dataset vs SALES** | Dataset criado de Terra (child) nao Parent, COA desalinhado | Backlog, URGENT |
| 3 | **PLA-3332 PS P&L negativo** | Projetos modificados manualmente quebraram automacao | Refinement |
| 4 | **Multi-Entity Dimensions** | Novo request sem escopo definido | Aguardando Intuit |
| 5 | **Mailchimp email blocking** | 17/43 sellers sem invite email | Workaround SSO |

---

## EQUIPE ATIVA (Ultima Semana)

| Pessoa | Role | Foco |
|--------|------|------|
| Augusto Gunsch | Eng (Platypus) | QBO projects refactor, activity plans, data validator |
| Lucas Soranzo | Eng Lead (Platypus) | NV3 prod, bank connections, cron schedules |
| Douglas Castilhos | Eng | Fix saved data, contractors |
| Eyji Koike Cuff | Eng | Constraints validation |
| Lucas Torresan | Eng | Products/Services ingest, Gong |
| Alexandra Lacerda | TSA | Winter Release validation, WFS SOW |
| Thiago Rodrigues | TSA Lead | Sweeps, PLA-3332, PLA-3256, playbook cockpit |
| Katherine Lu | Program Lead | Action items, Intuit coordination |
| Pamela | Core | Demo Playbooks fix (PR #2643) |
| Gabriel Taufer | Integrations Lead | Saturn capacity, Gong |

---

*Gerado automaticamente em 2026-03-11 via Linear API + Slack search + Drive API v3*
