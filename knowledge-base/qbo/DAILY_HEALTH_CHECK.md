# Daily Health Check - QBO/Intuit BOOM

**Versao:** 1.0
**Criado em:** 2025-12-19
**Max itens:** 20

---

## Instrucoes

- Executar diariamente antes de demos
- Cada item e binario: OK ou NOT OK
- Se NOT OK, documentar e criar ticket se necessario

---

## Checklist

### 1. Acesso e Login

| # | Check | Como verificar | OK? |
|---|-------|---------------|-----|
| 1 | Login TCO funciona | Acessar com credenciais TCO, ver dashboard | [ ] |
| 2 | Login Construction funciona | Acessar com credenciais Construction | [ ] |
| 3 | Sem alertas criticos no dashboard | Verificar banner/notificacoes | [ ] |
| 4 | Company switcher funciona | Trocar entre entities | [ ] |

### 2. Dados e Transacoes

| # | Check | Como verificar | OK? |
|---|-------|---------------|-----|
| 5 | Customers tem dados | Customers > verificar lista | [ ] |
| 6 | Vendors tem dados | Vendors > verificar lista | [ ] |
| 7 | Invoices existem | Sales > Invoices | [ ] |
| 8 | Bills existem | Expenses > Bills | [ ] |
| 9 | Bank feed conectado | Banking > verificar conexao | [ ] |
| 10 | Sem inventory negativo | Reports > Inventory Stock Status | [ ] |

### 3. Features Principais

| # | Check | Como verificar | OK? |
|---|-------|---------------|-----|
| 11 | Criar Invoice funciona | + New > Invoice > Save | [ ] |
| 12 | Criar Bill funciona | + New > Bill > Save | [ ] |
| 13 | Reports carregam | Reports > P&L | [ ] |
| 14 | Classes funcionam | Transacao > Class dropdown | [ ] |
| 15 | Locations funcionam | Transacao > Location dropdown | [ ] |

### 4. Multi-Entity (TCO)

| # | Check | Como verificar | OK? |
|---|-------|---------------|-----|
| 16 | Consolidated view disponivel | Company switcher > Consolidated | [ ] |
| 17 | Reports consolidam | Reports > ver dados de todas entities | [ ] |
| 18 | IC Allocations visivel | Accounting > IC Summary | [ ] |

### 5. Evidencia e Export

| # | Check | Como verificar | OK? |
|---|-------|---------------|-----|
| 19 | Export PDF funciona | Report > Export > PDF | [ ] |
| 20 | Export Excel funciona | Report > Export > Excel | [ ] |

---

## Acoes se NOT OK

1. Documentar problema (screenshot)
2. Verificar se e issue conhecido
3. Tentar workaround se existir
4. Criar ticket Linear se novo issue

---

## Registro

| Data | Executor | Issues encontrados | Acoes |
|------|----------|-------------------|-------|
| | | | |

---

Ultima atualizacao: 2025-12-19
