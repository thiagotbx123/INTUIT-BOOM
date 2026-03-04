# PLANO DE VALIDACAO INTELIGENTE - Winter Release FY26

> Estrategia: Dados onde possivel, UI onde necessario
> Gerado: 2026-01-12
> Banco: qbo_database (1).db - 18 tabelas, 194k+ rows

---

## RESUMO DO BANCO DE DADOS

| Tabela | Rows | Cobertura |
|--------|------|-----------|
| invoices | 44,823 | Faturamento completo |
| invoice_line_items | 43,540 | Itens detalhados |
| time_entries | 62,997 | Tracking de tempo |
| customers | 10,615 | Base de clientes |
| bills | 4,704 | Contas a pagar |
| bills_line_items | 5,199 | Itens de bills |
| expenses | 4,277 | Despesas |
| employees | 1,695 | Funcionarios |
| chart_of_accounts | 679 | Plano de contas |
| product_services | 465 | Produtos/Servicos |
| bank_transactions | 434 | Transacoes bancarias |
| estimates | 524 | Orcamentos |
| classifications | 265 | Dimensions/Classes |
| vendors | 261 | Fornecedores |
| projects | 39 | Projetos |

### Company Types no Banco
- `all`: Dados compartilhados
- `parent`: Empresa mae (Consolidated)
- `main_child`: Apex Tire
- `secondary_child`: Global Tread
- `child_3`: RoadReady/Traction

---

## MATRIZ DE VALIDACAO

### LEGENDA
- **DATA**: Validacao via query no banco (rapido, automatizavel)
- **UI**: Requer screenshot da interface (manual)
- **HYBRID**: Dados provam existencia, UI prova funcionalidade

---

## CATEGORIA: AI AGENTS (8 features)

| Ref | Feature | Tipo | Evidencia Dados | Evidencia UI | Prioridade |
|-----|---------|------|-----------------|--------------|------------|
| WR-001 | Accounting AI | HYBRID | bank_transactions (434) | Screenshot de sugestoes AI no Banking | P0 |
| WR-002 | Sales Tax AI | UI | - | Screenshot de Sales Tax com pre-check | P0 |
| WR-003 | Project Management AI | HYBRID | projects (39) | Screenshot de Projects com AI suggestions | P0 |
| WR-004 | Finance AI | UI | chart_of_accounts (679) suporta | Screenshot de Reports com insights AI | P1 |
| WR-005 | Solutions Specialist | UI | - | Screenshot de Business Feed com widgets | P1 |
| WR-006 | Customer Agent | HYBRID | customers (10,615) | Screenshot de Customers > Leads | P2 |
| WR-007 | Intuit Intelligence | UI | - | Screenshot do icone Intuit Assist | P2 |
| WR-008 | Conversational BI | UI | - | Screenshot do chat interface | P3 |

### Queries de Suporte (AI Agents)

```sql
-- WR-001: Bank Transactions existem
SELECT COUNT(*), company_type FROM bank_transactions GROUP BY company_type;

-- WR-003: Projects com dados
SELECT COUNT(*), status FROM projects GROUP BY status;

-- WR-006: Customers existem
SELECT COUNT(*), company_type FROM customers GROUP BY company_type;
```

---

## CATEGORIA: REPORTING (7 features)

| Ref | Feature | Tipo | Evidencia Dados | Evidencia UI | Prioridade |
|-----|---------|------|-----------------|--------------|------------|
| WR-009 | KPIs Customizados | HYBRID | invoices, expenses suportam KPIs | Screenshot KPI Scorecard | P0 |
| WR-010 | Dashboards | HYBRID | Dados financeiros existem | Screenshot Dashboard gallery | P0 |
| WR-011 | 3P Data Integrations | UI | - | Screenshot Apps marketplace | P2 |
| WR-012 | Calculated Fields | UI | - | Screenshot Report customization | P1 |
| WR-013 | Management Reports | UI | chart_of_accounts (679) | Screenshot Management Reports | P1 |
| WR-014 | Benchmarking | UI | - | Screenshot Benchmarking interface | P2 |
| WR-015 | Multi-Entity Reports | DATA+UI | company_type = multiple | Screenshot Consolidated view | P1 |

### Queries de Suporte (Reporting)

```sql
-- WR-009/010: Base financeira para KPIs
SELECT
  (SELECT COUNT(*) FROM invoices) as invoices,
  (SELECT COUNT(*) FROM expenses) as expenses,
  (SELECT COUNT(*) FROM bills) as bills;

-- WR-015: Multi-Entity confirmado
SELECT company_type, COUNT(*) as rows FROM invoices GROUP BY company_type;
```

---

## CATEGORIA: DIMENSIONS (4 features)

| Ref | Feature | Tipo | Evidencia Dados | Evidencia UI | Prioridade |
|-----|---------|------|-----------------|--------------|------------|
| WR-016 | Dimension Assignment v2 | HYBRID | classifications (265) | Screenshot com AI sparkles | P0 |
| WR-017 | Hierarchical Reporting | DATA | classifications com parent_id | Screenshot opcional | P1 |
| WR-018 | Dimensions on Workflow | UI | - | Screenshot Workflow automation | P1 |
| WR-019 | Dimensions on Balance Sheet | HYBRID | Dimensions existem | Screenshot Balance Sheet filter | P1 |

### Queries de Suporte (Dimensions)

```sql
-- WR-016/017: Dimensions com hierarquia
SELECT
  COUNT(*) as total,
  SUM(CASE WHEN parent_id IS NOT NULL THEN 1 ELSE 0 END) as with_parent,
  SUM(CASE WHEN is_class = 1 THEN 1 ELSE 0 END) as classes
FROM classifications;

-- Hierarquia de Dimensions
SELECT id, name, parent_id FROM classifications WHERE parent_id IS NOT NULL LIMIT 10;
```

---

## CATEGORIA: WORKFLOW (1 feature)

| Ref | Feature | Tipo | Evidencia Dados | Evidencia UI | Prioridade |
|-----|---------|------|-----------------|--------------|------------|
| WR-020 | Parallel Approval | UI | - | Screenshot Workflow automation | P1 |

**Nota**: Workflow Automation nao tem tabela no banco. Requer validacao UI.

---

## CATEGORIA: MIGRATION (3 features)

| Ref | Feature | Tipo | Evidencia Dados | Evidencia UI | Prioridade |
|-----|---------|------|-----------------|--------------|------------|
| WR-021 | Desktop Migration | UI | - | Screenshot Migration wizard | P2 |
| WR-022 | DFY Migration | UI | - | Screenshot DFY wizard | P2 |
| WR-023 | Feature Compatibility | N/A | - | Documentacao apenas | P3 |

**Nota**: Migration features nao tem representacao no banco. Sao fluxos de onboarding.

---

## CATEGORIA: CONSTRUCTION (2 features)

| Ref | Feature | Tipo | Evidencia Dados | Evidencia UI | Prioridade |
|-----|---------|------|-----------------|--------------|------------|
| WR-024 | Certified Payroll Report | HYBRID | employees (1,695) | Screenshot CPR report | P1 |
| WR-025 | Sales Order | UI | - | Screenshot Sales Order interface | P2 |

### Queries de Suporte (Construction)

```sql
-- WR-024: Employees para Certified Payroll
SELECT COUNT(*), company_type FROM employees GROUP BY company_type;
```

---

## CATEGORIA: PAYROLL (4 features)

| Ref | Feature | Tipo | Evidencia Dados | Evidencia UI | Prioridade |
|-----|---------|------|-----------------|--------------|------------|
| WR-026 | Multi-Entity Payroll Hub | HYBRID | employees multi-company | Screenshot Employee Hub | P1 |
| WR-027 | Garnishments | UI | employees existem | Screenshot Garnishments config | P2 |
| WR-028 | Assignments in QBTime | DATA | time_entries (62,997) | Screenshot opcional | P2 |
| WR-029 | Enhanced Amendments (CA) | N/A | - | CA tenant required | P3 |

### Queries de Suporte (Payroll)

```sql
-- WR-026: Employees multi-entity
SELECT company_type, COUNT(*) FROM employees GROUP BY company_type;

-- WR-028: Time entries existem
SELECT COUNT(*), entry_type FROM time_entries GROUP BY entry_type LIMIT 5;
```

---

## RESUMO POR TIPO DE VALIDACAO

| Tipo | Count | Features |
|------|-------|----------|
| DATA (banco prova) | 3 | WR-017, WR-028, +parciais |
| HYBRID (dados + UI) | 10 | WR-001, WR-003, WR-006, WR-009, WR-010, WR-015, WR-016, WR-019, WR-024, WR-026 |
| UI (screenshot obrigatorio) | 13 | WR-002, WR-004, WR-005, WR-007, WR-008, WR-011, WR-012, WR-013, WR-014, WR-018, WR-020, WR-021, WR-022 |
| N/A (documentacao ou CA) | 3 | WR-023, WR-025, WR-029 |

---

## PLANO DE EXECUCAO

### FASE 1: Validacao por Dados (30 min)
Executar queries no banco para gerar relatorio de cobertura de dados.
Output: CSV com contagens por tabela e company_type.

### FASE 2: Validacao UI Prioritaria (2h)
P0 features que requerem screenshot:
1. WR-001 Accounting AI - Banking com sugestoes
2. WR-002 Sales Tax AI - Sales Tax pre-check
3. WR-003 Project AI - Projects com AI
4. WR-009 KPIs - KPI Scorecard
5. WR-010 Dashboards - Dashboard gallery
6. WR-016 Dimensions - Assignment com sparkles

### FASE 3: Validacao UI Secundaria (2h)
P1/P2 features restantes.

### FASE 4: Consolidacao
Gerar planilha final com:
- Feature | Dados OK | UI OK | Evidencia | Status

---

## AMBIENTES

### TCO
- Login: quickbooks-testuser-tco-tbxdemo@tbxofficial.com
- Companies: Apex, Global Tread, Traction, RoadReady, Consolidated
- Banco: company_type = parent, main_child, secondary_child, child_3

### CONSTRUCTION SALES
- Login: quickbooks-test-account@tbxofficial.com
- Companies: Keystone Construction, Consolidated
- Banco: Verificar se tem dados separados ou usa mesmo banco

### CONSTRUCTION EVENTS
- Login: A confirmar
- Companies: A confirmar
- Banco: A verificar

---

Documento criado para otimizar validacao TestBox para Intuit.
