# Sessao: 2026-02-09 19:30

## Resumo
Execucao completa do ciclo de Demo Realism Health Check para Keystone Construction QBO. Navegacao UI via Playwright, documentacao de 6 gaps criticos, correcao do time entries supplement (1,701→1,575), e verificacao pos-fix confirmando que gaps sao dependentes de activity plans (nao fixaveis via DB).

## Participantes
- Usuario: Thiago
- Assistente: Claude Opus 4.6

## Camadas Alteradas

| Camada | Acao | Autorizado |
|--------|------|------------|
| DB (time_entries) | DELETE 1,701 + INSERT 1,575 supplement rows | Sim (plano aprovado) |
| DB (readonly) | Queries de analise em todas as tabelas | N/A (somente leitura) |

## Decisoes Tomadas

| Decisao | Contexto | Impacto |
|---------|----------|---------|
| NAO modificar bill_paid | Bills com paid_date futuro poderiam gerar AP, mas alteraria behavior do activity plan | AP continua $0 - aceitar como limitacao |
| NAO modificar invoice paid_invoice | Todas false, correto para AR tracking | AR inflado inclui old cycle data ($33.35M) |
| Corrigir time entries supplement | 1,701 rows (erradas) → 1,575 rows (corrigidas) | DB consistente para proximo activity plan run |
| Score 5/10 para health check | Dados corretos no DB mas UI depende de activity plan + timing | Report documenta gaps + resolucao timeline |

## Conhecimentos Adquiridos

### QBO/Intuit
- Activity plans processam DB tables em QBO transactions - raw DB data NAO aparece direto na UI
- bill_paid=true com relative_paid_date futuro: activity plan marca como pago no momento do processamento, nao na data futura
- AR aging no consolidated view inclui dados do ciclo anterior (2025) como 90+ overdue
- Time entries na UI so aparecem apos activity plan execution, nao via DB insert
- base_date=first_of_year means Jan 1; em Feb 9, apenas 11% dos dados sao "passado"

### TestBox
- Passkey login automatico funciona via Playwright (sem necessidade de digitar senha)
- Company switcher acessivel via header dropdown no IES

### Tecnico
- relative_paid_date e NULLABLE na tabela quickbooks_bills (contrario ao que se acreditava)
- PGPASSWORD env var com psql.exe funciona em bash syntax (nao PowerShell $env:)
- Playwright browser_wait_for pode gerar output > 70K chars que excede token limit
- ingest_to_db.py step 11-TE: deleta id>=73993 e insere supplement CSV

## Arquivos Criados
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\HEALTH_CHECK_REPORT_2026-02-09.md` - Report completo (14 secoes)
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\01_dashboard_consolidated.png`
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\01_dashboard_consolidated_full.png`
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\02_dashboard_bluecraft.png`
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\02_dashboard_bluecraft_full.png`
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\03_invoices_bluecraft.png`
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\04_expenses_bluecraft.png`
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\05_post_fix_consolidated.png`
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\06_post_fix_bluecraft_dashboard.png`
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\06f_post_fix_bluecraft_full.png`
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\07_time_entries_bluecraft.png`

## Arquivos Modificados
- `.claude/projects/C--Users-adm-r-Clients-intuit-boom/memory/MEMORY.md` - DB state + health check results
- `C:\Users\adm_r\Downloads\HEALTH_CHECK\HEALTH_CHECK_REPORT_2026-02-09.md` - Added sections 10-14

## Problemas Encontrados e Resolucoes

| Problema | Causa | Solucao |
|----------|-------|---------|
| Chrome blocking Playwright | Chrome already running | taskkill //IM chrome.exe //F |
| psql PGPASSWORD not working | PowerShell vs bash syntax | PGPASSWORD=xxx inline syntax |
| Time entries 1,701 vs 1,575 | Old supplement CSV had 126 extra rows | ingest_to_db.py step 11-TE with corrected CSV |
| AR $34M inflated | Old cycle (2025) invoices still unpaid | NOT fixable via DB - needs engineering |
| AP = $0 | All bills bill_paid=true | NOT fixable safely - activity plan manages |
| Dashboard P&L -$61K | QBO includes old cycle costs + only 40 days data | Timing-dependent - will improve over time |
| Project widgets empty | Activity plan hasn't linked time entries to projects | Needs activity plan execution |
| browser_wait_for token overflow | Output > 70K chars | Use browser_snapshot instead |

## Metricas da Sessao
- Arquivos criados: 12 (1 report + 11 screenshots)
- Arquivos modificados: 2 (MEMORY.md + report)
- DB operations: 1 (DELETE+INSERT time entries)
- Commits: 0 (pending)
- Screenshots: 11 total (4 pre-fix, 4 post-fix, 3 individual pages)

## Proximos Passos Sugeridos
1. **Feb 14+**: Re-check dashboard after payroll auto-starts (~$194K/month)
2. **Feb 15+**: Run health check again - compare P&L, project widgets
3. **Engineering escalation**: AR inflation ($33.35M from old cycle) needs activity plan cleanup
4. **Engineering escalation**: Project widget linkage (time entries → projects → invoices)
5. **Feb 28**: Full 2-month health check - dashboard should be significantly more realistic

## Notas Adicionais
- A causa raiz de todos os gaps visuais e o timing: base_date=first_of_year + estamos no dia 40 do ano
- O DB tem dados corretos e validados (189/189 audit pass) - o problema e exclusivamente na camada de activity plans e processamento QBO
- O score 5/10 vai melhorar naturalmente conforme mais dias passam e mais dados entram no range "passado"
- Payroll ($1.78M/ano) e o maior fator pendente - deve aparecer a partir de Feb 14

---
*Consolidado automaticamente via /consolidar*
