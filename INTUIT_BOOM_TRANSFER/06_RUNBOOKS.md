# INTUIT-BOOM - Runbooks Operacionais

> Procedimentos passo-a-passo para cada tarefa recorrente no projeto.

---

## RUNBOOK 1: Inicio de Sessao Claude

**Quando:** Toda vez que abrir o projeto no Claude Code

```
1. cd C:\Users\adm_r\Clients\intuit-boom
2. Claude le .claude/memory.md automaticamente
3. Ler strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md
4. Verificar sessions/ para contexto recente
5. Executar /status para visao rapida
```

---

## RUNBOOK 2: Fim de Sessao Claude

**Quando:** Antes de fechar o Claude Code

```
1. Executar /consolidar
   - Cria arquivo em sessions/ com resumo
   - Atualiza .claude/memory.md
   - Git commit + push
2. Verificar que commit foi feito
3. Se houve decisao importante, documentar em knowledge-base/
```

---

## RUNBOOK 3: Login QBO via Playwright CDP

**Quando:** Precisar acessar QBO automaticamente

```bash
# 1. Abrir Chrome com debug port
chrome.exe --remote-debugging-port=9222

# 2. Executar login
python layer1_login.py

# OU usar no codigo:
from layer1_login import login
pw, browser, page = login("TCO", "apex")

# Projetos disponiveis:
# TCO: apex, consolidated, global, traction, roadready
# CONSTRUCTION: construction, consolidated
# PRODUCT: (default)
# TCO_DEMO: (same as TCO, different email)
```

**NOTA:** Chrome DEVE estar aberto com `--remote-debugging-port=9222` ANTES do script.

---

## RUNBOOK 4: Validacao de Features

**Quando:** Novo release precisa ser validado

```
1. Identificar TODAS features aplicaveis (IES = TCO + Construction + Product)
2. Criar tracker Excel com colunas padrao
3. Para cada feature:
   a. LOGIN no ambiente correto
   b. NAVEGAR para URL da feature
   c. ESPERAR 30-45s (QBO e lento!)
   d. CAPTURAR screenshot
   e. ANALISAR (flags + tamanho)
   f. Se erro: tentar URL alternativa
   g. DOCUMENTAR evidence notes
   h. DECIDIR status (PASS/PARTIAL/NOT_AVAILABLE/N/A)
4. Upload screenshots para Google Drive
5. Gerar hyperlinks no tracker
6. Validar data quality (Strong/Weak/Inconclusive)
7. Comparar ambientes lado a lado

CHECKLIST POS-CAPTURA:
[ ] Screenshot > 100KB?
[ ] ~140KB pode ser 404?
[ ] Conteudo mostra feature especifica?
[ ] Contexto correto (Consolidated vs Individual)?
[ ] Evidence notes descrevem o que esta visivel?
```

---

## RUNBOOK 5: Ingestion de Dados (CSV)

**Quando:** Novos dados precisam ser importados para dataset

```
1. VERIFICAR IDs existentes:
   SELECT MAX(id) FROM [tabela] WHERE dataset_id = '[id]'

2. GERAR CSV com IDs sequenciais (MAX+1)

3. VALIDAR FK dependencies:
   - Vendors/Customers EXISTEM antes de Bills/Invoices
   - product_service_id validos
   - project_id dentro do range correto
   - Dates dentro dos periodos dos projetos

4. ORDEM DE INGESTION:
   a. Vendors (sem FK externas)
   b. Customers (sem FK externas)
   c. Bills (FK -> vendors)
   d. Invoices (FK -> customers)
   e. Time Entries (FK -> employees, projects, products)

5. VERIFICAR pos-ingestion:
   - Count bate com CSV
   - FKs resolvem corretamente
   - Nenhum orphan record
```

---

## RUNBOOK 6: Criar/Atualizar Tickets Linear

**Quando:** Novas tasks ou updates de status

```bash
# Criar ticket
python create_linear_ticket.py

# Adicionar comentario/worklog
python add_linear_comment.py

# Atualizar status batch
python linear_update_all.py

# Ver tabela de tickets
python get_full_ticket_table.py
```

**API:** `https://api.linear.app/graphql`
**Key:** Em `C:\Users\adm_r\Tools\LINEAR_AUTO\.env`

---

## RUNBOOK 7: Upload Evidence para Google Drive

**Quando:** Screenshots capturados precisam ir para Drive

```python
# Usa token OAuth2 persistente
# Token: C:\Users\adm_r\token_drive.pickle

# Pasta destino: 08. Intuit/06. Winter Release/
# Subpastas: TCO/, Construction/

# Se token expirou:
# 1. Deletar token_drive.pickle
# 2. Re-executar script (abre browser para auth)
# 3. Novo token e salvo automaticamente
```

---

## RUNBOOK 8: Acessar SQLite Database

**Quando:** Precisar consultar dados locais

```python
import sqlite3
conn = sqlite3.connect('C:/Users/adm_r/Downloads/qbo_database_TCO_Construction.db')
cursor = conn.cursor()

# Exemplo: listar classifications TCO
cursor.execute("""
    SELECT * FROM classifications
    WHERE dataset_id = 'fab72c98-c38d-4892-a2db-5e5269571082'
""")
results = cursor.fetchall()
print(f"Found {len(results)} classifications")  # 51

conn.close()
```

---

## RUNBOOK 9: Verificacao de Fatos

**Quando:** Antes de afirmar qualquer coisa sobre QBO/Intuit

```
CHECKLIST:
[ ] 1. Esta na documentacao QBO oficial?
[ ] 2. Foi testado no ambiente real?
[ ] 3. Bate com o que esta no dataset?
[ ] 4. O Linear ticket confirma?
[ ] 5. Se aplica ao vertical correto?

FONTES CONFIAVEIS (em ordem):
1. Ambiente QBO real (login e verificar)
2. SQLite database local
3. Knowledge-base/strategic-cortex/
4. Linear tickets
5. Slack (contexto, nao verdade absoluta)

FONTES NAO CONFIAVEIS:
- Assuncoes sem verificar
- Memoria de sessoes antigas sem reler
- Informacao de um vertical aplicada a outro
```

---

## RUNBOOK 10: Strategic Cortex Update

**Quando:** Precisar atualizar inteligencia consolidada

```bash
# 1. Atualizar SpineHub
cd C:\Users\adm_r\Tools\TSA_CORTEX
npx ts-node src/cli/index.ts collect --all

# 2. Consultar entidade especifica
npx ts-node src/cli/index.ts query --entity "Katherine"

# 3. Outputs gerados:
# OUTPUT_A_EXECUTIVE_SNAPSHOT.md - Status rapido
# OUTPUT_B_STRATEGIC_MAP.md - Conexoes
# OUTPUT_C_KNOWLEDGE_BASE.json - Dados (847 items)
# OUTPUT_D_KEYWORD_MAP_LINEAR_RECIPES.md - Busca
# OUTPUT_E_DELTA_SUMMARY.md - Mudancas
```

---

## RUNBOOK 11: Monitorar Blockers

**Quando:** Semanalmente (minimo)

```
1. Abrir Linear e filtrar por Blocked no Intuit/QBO
2. Verificar status de cada blocker:
   - PLA-3013 (Login TCO) - RESOLVED
   - PLA-2969 (Canada Bills) - BACKLOG
   - PLA-2883 (Ingesting activities) - CHECK
   - PLA-2724 (Dimensions Payroll) - CHECK
   - PLA-2916 (Negative Inventory) - IN PROGRESS
3. Atualizar memory.md se algo mudou
4. Escalar se blocker tem mais de 1 semana sem progresso
5. Verificar WFS environment decision com Katherine
```

---

*Runbooks criados em 2026-02-06 baseados nas 17 sessoes documentadas*
