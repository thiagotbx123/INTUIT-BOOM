# WFS Mapping Summary

**Data:** 2025-12-19
**Autor:** Thiago (TSA)
**Conta:** thiago@testbox.com

---

## Empresas Mapeadas

| Empresa | Tipo | Employees | Payroll | WFS Score |
|---------|------|-----------|---------|-----------|
| GoQuick Alpha Retail | Retail | 3 | Basico | 6/10 |
| Keystone Construction Canada | Construction | 7+ | Robusto | 9/10 |

---

## Descobertas Chave para WFS

### 1. PTO/Vacation Tracking
- **Keystone** tem coluna "AVAILABLE VACATION" visivel
- Ideal para demo story "Unified PTO"
- GoQuick nao mostra vacation data

### 2. Celebrations (Engagement)
- **Keystone** tem panel CELEBRATE
- Mostra birthdays e work anniversaries
- Feature de engajamento para WFS

### 3. Employee Types
- **GoQuick**: 3 salary employees ($25k-$90k)
- **Keystone**: Mix hourly ($56-65/h) + salary ($43k-$85k)
- Keystone mais realista para demos

### 4. Job Costing
- **Keystone** = Construction company
- Ideal para demo story "Job costing"
- Projects module disponivel
- Time tracking por Customer/Service

### 5. Invite to Workforce
- **GoQuick** tem botao "Invite to Workforce"
- Ponto de integracao QBO -> WFS
- Nao visivel em Keystone (pode estar em outro lugar)

### 6. Intuit Intelligence
- **GoQuick** mostra AI assistant BETA
- "What can I do for you today?"
- Pode ser relevante para Magic Docs

---

## Matriz de Demo Stories

| Story | GoQuick | Keystone | Recomendacao |
|-------|---------|----------|--------------|
| Unified PTO | - | **AVAILABLE VACATION** | Keystone |
| Magic Docs | Intuit Intelligence | - | GoQuick |
| Hire to fire | 3 employees | 7+ employees | Keystone |
| Job costing | Retail | **Construction** | Keystone |

---

## Arquivos Gerados

### Screenshots
```
wfs_mapping/screenshots/
├── homepage.png         # GoQuick dashboard
├── payroll.png          # GoQuick payroll
├── employees.png        # GoQuick employees
├── time.png             # GoQuick timesheet
├── projects.png         # GoQuick projects
├── reports.png          # GoQuick reports
├── settings.png         # GoQuick settings
├── hr_advisor.png       # 404 - not enabled
├── company_select.png   # Company selection
├── keystone/
│   ├── payroll.png      # Keystone payroll + celebrations
│   └── employees.png    # Keystone employees + vacation
└── mapping_report.json  # JSON report
```

### Documentacao
```
knowledge-base/wfs/
├── WFS_CORTEX_v1.md           # Cortex do projeto
├── WFS_ALPHA_RETAIL_MAP.md    # Mapeamento GoQuick
├── WFS_KEYSTONE_MAP.md        # Mapeamento Keystone
└── WFS_MAPPING_SUMMARY.md     # Este arquivo
```

---

## Proximos Passos

1. [ ] Testar fluxo "Invite to Workforce" em GoQuick
2. [ ] Explorar Projects em Keystone para job costing
3. [ ] Verificar se Keystone tem acesso a WFS
4. [ ] Mapear Reports relevantes para payroll/HR
5. [ ] Aguardar PRDs da Intuit para escopo detalhado
6. [ ] Confirmar acesso a Mineral HR (parceiro externo)

---

## Conclusao

**Keystone Construction Canada** e o ambiente recomendado para demos WFS porque:
- Mais employees (realismo)
- Vacation/PTO tracking visivel
- Celebrations panel (HR engagement)
- Mix de hourly/salary
- Construction = job costing nativo
- Dados financeiros robustos

**GoQuick Alpha Retail** serve para:
- Demos simples
- "Invite to Workforce" visivel
- Intuit Intelligence BETA

---

Mapeamento concluido em 2025-12-19 11:45
