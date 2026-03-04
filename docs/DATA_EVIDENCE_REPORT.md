# DATA EVIDENCE REPORT - Winter Release FY26

> Gerado: 2026-01-12 09:37:23
> Banco: qbo_database (1).db

---

## RESUMO

| Status | Count |
|--------|-------|
| PASS | 6 |
| WEAK | 4 |
| ERROR | 0 |

---

## EVIDENCIAS POR FEATURE

### [OK] WR-001 - Accounting AI

**Descricao:** Bank transactions para AI suggestions

**Query:**
```sql
SELECT COUNT(*) as count, 'bank_transactions' as table_name FROM bank_transactions
```

**Resultado:** `count=434, table_name=bank_transactions`

**Status:** PASS

---

### [?] WR-003 - Project Management AI

**Descricao:** Projects com diferentes status

**Query:**
```sql
SELECT COUNT(*) as count, status FROM projects GROUP BY status
```

**Resultado:** `4 rows: [(2, 'Canceled'), (2, 'Completed'), (12, 'In Progress'), (23, 'In progress')]`

**Status:** WEAK

---

### [OK] WR-006 - Customer Agent

**Descricao:** Base de customers para leads

**Query:**
```sql
SELECT COUNT(*) as count FROM customers
```

**Resultado:** `count=10615`

**Status:** PASS

---

### [OK] WR-009 - KPIs Customizados

**Descricao:** Dados financeiros para KPIs

**Query:**
```sql
SELECT
            (SELECT COUNT(*) FROM invoices) as invoices,
            (SELECT COUNT(*) FROM expenses) as expenses,
            (SELECT COUNT(*) FROM bills) as bills
```

**Resultado:** `invoices=44823, expenses=4277, bills=4704`

**Status:** PASS

---

### [?] WR-015 - Multi-Entity Reports

**Descricao:** Invoices por company_type (multi-entity)

**Query:**
```sql
SELECT company_type, COUNT(*) as count FROM invoices GROUP BY company_type
```

**Resultado:** `5 rows: [('all', 247), ('child_3', 874), ('main_child', 29299), ('parent', 2055), ('secondary_child', 12348)]`

**Status:** WEAK

---

### [OK] WR-016 - Dimension Assignment v2

**Descricao:** Classifications/Dimensions com hierarquia

**Query:**
```sql
SELECT
            COUNT(*) as total,
            SUM(CASE WHEN parent_id IS NOT NULL THEN 1 ELSE 0 END) as with_hierarchy
            FROM classifications
```

**Resultado:** `total=265, with_hierarchy=222`

**Status:** PASS

---

### [OK] WR-017 - Hierarchical Dimension Reporting

**Descricao:** Dimensions com parent_id (hierarquia)

**Query:**
```sql
SELECT id, name, parent_id FROM classifications WHERE parent_id IS NOT NULL LIMIT 20
```

**Resultado:** `20 rows: [(257, 'Labor / Installation Charges', 255.0), (246, 'Tires', 245.0), (264, 'Road Hazard Warranty', 258.0), (235, 'Houston', 227.0), (244, 'Government / National Accounts', 240.0)]`

**Status:** PASS

---

### [?] WR-024 - Certified Payroll Report

**Descricao:** Employees por company (para payroll)

**Query:**
```sql
SELECT company_type, COUNT(*) as count FROM employees GROUP BY company_type
```

**Resultado:** `5 rows: [('all', 135), ('child_3', 30), ('main_child', 564), ('parent', 202), ('secondary_child', 764)]`

**Status:** WEAK

---

### [?] WR-026 - Multi-Entity Payroll Hub

**Descricao:** Employees distribuidos por entidade

**Query:**
```sql
SELECT company_type, COUNT(*) as count FROM employees WHERE company_type != 'all' GROUP BY company_type
```

**Resultado:** `4 rows: [('child_3', 30), ('main_child', 564), ('parent', 202), ('secondary_child', 764)]`

**Status:** WEAK

---

### [OK] WR-028 - Assignments in QBTime

**Descricao:** Time entries para assignments

**Query:**
```sql
SELECT COUNT(*) as count FROM time_entries
```

**Resultado:** `count=62997`

**Status:** PASS

---

## CONCLUSAO

Este relatorio demonstra que os dados necessarios para as features
listadas existem no banco de dados QBO. As features marcadas como PASS
tem dados suficientes para demonstracao. Features WEAK podem precisar
de dados adicionais.

Para features que requerem validacao UI, use a planilha
`WINTER_RELEASE_VALIDATION_MATRIX.xlsx` com step-by-step.
