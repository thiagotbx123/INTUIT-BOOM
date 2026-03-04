# REVISAO CRITICA TCO - Winter Release FY26
## Data: 2025-12-29

---

## SUMARIO EXECUTIVO

Revisao critica identificou **10 screenshots problematicos** que NAO provam adequadamente as features.

| Severidade | Quantidade |
|------------|------------|
| CRITICO (404, contexto errado) | 5 |
| GRAVE (loading, generico) | 3 |
| MEDIO (incompleto) | 2 |
| N/A (documentacao) | 1 |
| OK | 1 |

---

## ANALISE DETALHADA POR FEATURE

### WR-006 - Customer Agent
**Status:** CRITICO - Screenshot ERRADO

**O que mostra:** Dashboard Homepage com "Business at a glance"
**O que deveria mostrar:**
- Sales > Customers > Leads tab
- Botao de import from Gmail/Outlook
- Draft estimates functionality

**Acao:** Recapturar navegando para Customers > Leads

---

### WR-007 - Omni / Intuit Intelligence
**Status:** CRITICO - Screenshot ERRADO

**O que mostra:** Dashboard Homepage com widgets em loading
**O que deveria mostrar:**
- Intuit Assist chat interface
- Conversational AI assistant
- Cross-product intelligence queries

**Acao:** Recapturar abrindo Intuit Assist (icone de chat)

---

### WR-012 - Calculated Fields
**Status:** CRITICO - PAGINA 404

**O que mostra:** "We're sorry, we can't find the page you requested."
**O que deveria mostrar:**
- Report customization interface
- Add calculated field option
- Formula builder

**Acao:** Recapturar via Reports > Custom Reports > Create > Add Calculated Field

---

### WR-014 - Benchmarking
**Status:** GRAVE - Loading spinner

**O que mostra:** Reports page com menu lateral visivel mas conteudo em loading
**O que deveria mostrar:**
- Performance Center com dados
- Industry benchmarks comparisons
- Performance metrics

**Acao:** Recapturar com 45-60s de espera no Performance Center

**Nota:** Se N/A (nao aplicavel), NAO deveria ter screenshot

---

### WR-015 - Multi-Entity Reports
**Status:** CRITICO - CONTEXTO ERRADO

**O que mostra:** Reports em "Apex Tire & Auto Retail, LLC" (empresa individual)
**O que deveria mostrar:**
- CONSOLIDATED VIEW (nao empresa individual)
- Reports mostrando dados de MULTIPLAS entidades
- Company picker mostrando "Consolidated" ou "Vista Consolidada"

**Acao:**
1. Trocar para Consolidated View via company picker
2. Capturar reports consolidados
3. Mostrar que dados vem de multiplas empresas

**REGRA:** Features Multi-Entity SEMPRE em Consolidated View

---

### WR-020 - Parallel Approval
**Status:** MEDIO - Incompleto

**O que mostra:** Workflow Automation com lista de workflows (Bill Approval, etc)
**O que deveria mostrar:**
- Configuracao de workflow com MULTIPLOS APROVADORES SIMULTANEOS
- Parallel approval path configuration
- Multiple approvers at same level

**Acao:** Recapturar entrando em Edit de um workflow e mostrando config de parallel approvers

---

### WR-021 - Seamless Desktop Migration
**Status:** OK

**O que mostra:** Import Data page com "Import from QuickBooks Desktop" visivel
**O que prova:** Feature de migracao existe e esta acessivel

**Acao:** Nenhuma - screenshot adequado

---

### WR-022 - DFY Migration Experience
**Status:** MEDIO - Generico

**O que mostra:** Import Data page generica
**O que deveria mostrar:**
- DFY (Done-For-You) migration wizard especifico
- "Save time with Advanced" ou similar
- Guided setup experience

**Nota:** Pode ser que DFY seja servico, nao UI. Investigar.

---

### WR-023 - Feature Compatibility
**Status:** N/A - DOCUMENTACAO

**O que mostra:** Settings com loading spinner
**O que deveria mostrar:** NADA - E DOCUMENTACAO

**Decisao:**
- NAO deve ter screenshot
- Marcar como N/A no tracker
- Referenciar documentacao de compatibilidade

**REGRA:** Features de documentacao = N/A, sem screenshot

---

### WR-026 - Multi-Entity Payroll Hub
**Status:** CRITICO - PAGINA 404

**O que mostra:** "We're sorry, we can't find the page you requested."
**O que deveria mostrar:**
- Employee Hub interface
- Cross-entity payroll view
- Centralized employee management

**Acao:**
1. Verificar se feature existe no tenant
2. Se existir, encontrar URL correta
3. Se nao existir, marcar NOT_AVAILABLE

---

### WR-029 - Enhanced Amendments (CA)
**Status:** INVESTIGAR - Ambiente errado?

**O que mostra:** Payroll Overview com TO DO LIST (generico)
**O que deveria mostrar:**
- CA-specific amendment handling
- Enhanced correction workflow para California

**Problema:**
- Feature e para "CA-specific tenant"
- TCO e ambiente US generico, nao California-specific
- Pode nao fazer sentido validar no TCO

**Decisao:**
1. Se TCO nao e tenant California: marcar N/A com justificativa
2. Se existir ambiente CA: migrar validacao para la
3. NAO capturar screenshots genericos que nao provam a feature

---

## MAPEAMENTO POR CONTEXTO

### APEX (Empresa Individual)
Features que devem ser capturadas na empresa Apex:
- WR-001 a WR-013 (exceto WR-012 que precisa URL correta)
- WR-016 a WR-020
- WR-024, WR-025, WR-027, WR-028

### CONSOLIDATED VIEW
Features que OBRIGATORIAMENTE precisam de Consolidated View:
- **WR-015** - Multi-Entity Reports
- **WR-026** - Multi-Entity Payroll Hub (se existir)

### FRESH TENANT
Features que precisam de tenant limpo:
- WR-021 - Seamless Desktop Migration (demo completo)
- WR-022 - DFY Migration Experience

### CA-SPECIFIC TENANT
Features que precisam de tenant California:
- WR-029 - Enhanced Amendments (CA)

### DOCUMENTACAO (N/A)
Features que NAO sao UI:
- WR-023 - Feature Compatibility

---

## PLANO DE RECAPTURA ORGANIZADO

### FASE 1: APEX (Empresa Individual)
Capturar na empresa Apex Tire, sem trocar:

| Ordem | Ref | Feature | URL/Navegacao |
|-------|-----|---------|---------------|
| 1 | WR-006 | Customer Agent | Sales > Customers > Leads tab |
| 2 | WR-007 | Intuit Intelligence | Click Intuit Assist icon |
| 3 | WR-012 | Calculated Fields | Reports > Custom Reports > Create |
| 4 | WR-014 | Benchmarking | Reports > Performance Center (45s wait) |
| 5 | WR-020 | Parallel Approval | Workflow > Edit existing > Show parallel config |

### FASE 2: CONSOLIDATED VIEW
Trocar para Vista Consolidada e capturar:

| Ordem | Ref | Feature | O que capturar |
|-------|-----|---------|----------------|
| 1 | WR-015 | Multi-Entity Reports | Reports consolidados com multiplas entidades |
| 2 | WR-026 | Payroll Hub | Employee Hub cross-entity (se existir) |

### FASE 3: DECISOES
Marcar no tracker:

| Ref | Feature | Decisao |
|-----|---------|---------|
| WR-023 | Feature Compatibility | N/A - Documentacao |
| WR-029 | Enhanced Amendments | N/A - Requer CA tenant |

---

## LEARNINGS CANONICOS

### REGRA 1: Screenshot DEVE provar a feature
- Dashboard generico NAO prova feature especifica
- O screenshot deve mostrar EXATAMENTE o que a feature faz
- Se nao conseguir capturar, investigar antes de marcar PASS

### REGRA 2: Contexto correto obrigatorio
- Multi-Entity features = Consolidated View
- CA features = CA-specific tenant
- Migration features = Fresh tenant para demo completo

### REGRA 3: N/A != Screenshot ruim
- Se feature e documentacao: N/A sem screenshot
- Se feature nao existe no ambiente: NOT_AVAILABLE
- Se screenshot nao prova: RECAPTURAR, nao marcar N/A

### REGRA 4: Organizar capturas por contexto
- Agrupar features que precisam do mesmo contexto
- Trocar empresa UMA VEZ e capturar TODAS as features daquele contexto
- Evitar ficar alternando entre Apex e Consolidated

### REGRA 5: 404 = Investigar, nao ignorar
- Se URL retorna 404, a feature pode:
  - Nao existir no ambiente
  - Ter URL diferente
  - Requerer setup especifico
- Sempre investigar antes de marcar status

### REGRA 6: Ambiente especifico significa AMBIENTE ESPECIFICO
- CA-specific = California tenant
- Canada = Canada tenant (sistema completamente diferente)
- Fresh tenant = Empresa sem dados
- NAO misturar contextos

---

## FONTES

- [Intuit Enterprise Suite Multi-Entity](https://insightfulaccountant.com/in-the-news/people-and-business/intuit-enterprise-suite-consolidated-view/)
- [Multi-Entity Accounting IES](https://outoftheboxtechnology.com/blog/multi-entity-accounting-quickbooks-alternative)
- [QuickBooks Canada vs US](https://www.mindingmybooks.ca/quickbooks-canada-vs-us-comparison)

---

*Documento gerado automaticamente - Claude Code*
*Revisao critica em: 2025-12-29*
