# WFS POV/SOW Framework

**Data:** 2025-12-19
**Autor:** Thiago Rodrigues (TSA, Data Architect)
**Projeto:** Intuit Workforce Solutions (WFS)
**Cliente:** Intuit

---

## 1. Executive Summary

### O que e WFS
Intuit Workforce Solutions e uma plataforma HCM (Human Capital Management) que combina:
- GoCo capabilities (HR, onboarding, benefits)
- QuickBooks Payroll (folha de pagamento)
- Integracao nativa com QBO

### Por que TestBox esta envolvido
- Criar ambientes de demo ricos em dados
- Suportar sales enablement da Intuit
- Garantir demo reliability para Alpha, Beta e GA

### Timeline
| Fase | Data | Scope |
|------|------|-------|
| Alpha | Dez 2025 | ~100 customers |
| Beta | Fev 2026 | Expanded |
| GA | Mai 2026 (01/05) | Full launch |

---

## 2. Point of View (POV)

### 2.1 Posicionamento TestBox

**TestBox deve ser o parceiro estrategico de demo para WFS porque:**

1. **Expertise em QBO** - Ja temos TCO, Construction Sales/Events funcionando
2. **Automacao** - Scripts Playwright para navegacao autonoma
3. **Data Architecture** - Golden thread data model para demos consistentes
4. **Conhecimento Mineral** - Mapeamento completo da integracao HR

### 2.2 Diferenciais Competitivos

| Area | Nossa Capacidade |
|------|------------------|
| QBO Navigation | 47 rotas mapeadas, 100% funcionando |
| Mineral Access | SSO via GoQuick Alpha confirmado |
| Automation | Playwright + CDP working |
| Documentation | Cortex, Navigation Map, Feature Surface |

### 2.3 Gaps a Enderecar

| Gap | Impacto | Mitigacao |
|-----|---------|-----------|
| PRDs WFS pendentes | Alto | Aguardar Intuit |
| API Mineral privada | Medio | Contato Mitratech |
| Sandbox WFS | Alto | Confirmar acesso dates |

---

## 3. Statement of Work (SOW) - Estrutura

### 3.1 Deliverables por Wave

#### Wave 0: Scoping (Atual)
| Deliverable | Status | Owner |
|-------------|--------|-------|
| QBO Route Mapping | DONE | Thiago |
| Mineral Access Mapping | DONE | Thiago |
| Navigation Automation | DONE | Thiago |
| PRD Collection | PENDING | Intuit |
| SOW Draft | IN PROGRESS | Katherine |

#### Wave 1: Alpha (Dez 2025)
| Deliverable | Descricao |
|-------------|-----------|
| Demo Environment Setup | Configurar ambiente WFS |
| Baseline Data | 50 employees, 6-10 depts, 3-6 locations |
| Demo Story: Unified PTO | Employee > Manager > Payroll Admin |
| Demo Story: Magic Docs | HR Admin flow |
| Enablement Guide | Documentacao para sales |

#### Wave 2: Beta (Fev 2026)
| Deliverable | Descricao |
|-------------|-----------|
| Enhanced Data | Performance data, workflows |
| Demo Story: Hire to Fire | Full lifecycle |
| Demo Story: Job Costing | Labor cost attribution |
| Automation Scripts | Refresh automatico |

#### Wave 3: GA (Mai 2026)
| Deliverable | Descricao |
|-------------|-----------|
| Production Reliability | Monitoring, alerting |
| Full Automation | Data refresh, health checks |
| Scale Testing | Multiple demo instances |

---

## 4. Technical Architecture

### 4.1 Sistemas Envolvidos

```
+------------------+     +------------------+     +------------------+
|   QuickBooks     |     |    Workforce     |     |    Mineral HR    |
|   Online (QBO)   |<--->|    Solutions     |<--->|   (Compliance)   |
+------------------+     +------------------+     +------------------+
        |                        |                        |
        v                        v                        v
+------------------+     +------------------+     +------------------+
|   Payroll API    |     |   WFS Platform   |     |   Mineral API    |
|   (REST/GraphQL) |     |   (GoCo + QBO)   |     |   (Privada)      |
+------------------+     +------------------+     +------------------+
```

### 4.2 Integracao QBO <-> WFS

| Feature QBO | Feature WFS | Integracao |
|-------------|-------------|------------|
| Employees | Worker Profile | Sync bidirectional |
| Payroll | Pay Runs | Nativa |
| Time Activities | Time/Attendance | Sync |
| Projects | Job Costing | Via time entries |

### 4.3 Integracao QBO <-> Mineral

| Feature QBO | Feature Mineral | Integracao |
|-------------|-----------------|------------|
| HR Advisor | Mineral Platform | SSO |
| Employees | Compliance tracking | Manual |
| Templates | Document templates | Export |

---

## 5. Demo Stories Detalhadas

### Story A: Unified PTO

**Objetivo:** Mostrar fluxo PTO end-to-end

**Roles:**
1. Employee - Solicita PTO
2. Manager - Aprova PTO
3. Payroll Admin - Ve reflexo no payroll

**Fluxo:**
```
Employee                Manager                 Payroll Admin
    |                       |                       |
    |-- Submit PTO -------->|                       |
    |                       |                       |
    |                       |-- Review & Approve -->|
    |                       |                       |
    |<-- Notification ------|                       |
    |                       |                       |
    |                       |                       |-- Payroll reflects
    |                       |                       |   PTO deduction
```

**Data Requirements:**
- 3 PTO policies configuradas
- 5-10 pending requests
- Employee balances visibles

**QBO Routes:**
- `/app/employees` - Ver employees
- `/app/timetracking` - Ver time off
- `/app/payroll` - Ver payroll impact

---

### Story B: Magic Docs

**Objetivo:** Mostrar AI document generation

**Role:** HR Admin

**Fluxo:**
```
1. Select template
2. Smart fields auto-populate from employee data
3. Generate document
4. E-signature flow
5. Auto-save to employee record
```

**Data Requirements:**
- Complete employee profiles
- 5-10 document templates
- E-signature enabled

---

### Story C: Job Costing

**Objetivo:** Mostrar labor cost attribution

**Fluxo:**
```
1. Employee logs time against project
2. Time entry includes pay rate
3. Project shows labor cost
4. Reports show cost breakdown
```

**QBO Routes:**
- `/app/timetracking` - Time entry
- `/app/projects` - Project view
- `/app/reports/time` - Time reports

**Ambiente Recomendado:** Keystone Construction Canada

---

## 6. Data Architecture

### 6.1 Golden Thread

Um employee record flui por multiplos modulos com IDs consistentes:

```
Employee ID --> Payroll --> Time --> Projects --> Reports
     |
     +--> WFS Profile --> PTO --> Performance
     |
     +--> Mineral --> Compliance --> Training
```

### 6.2 Baseline Dataset

| Entidade | Quantidade | Notas |
|----------|------------|-------|
| Employees | 50 core + pool | Mix hourly/salary |
| Departments | 6-10 | Org structure |
| Locations | 3-6 | Multi-state |
| Managers | 8+ | Reporting structure |
| PTO Policies | 3 | Different accruals |
| Pending PTO | 5-10 | For demo |
| Doc Templates | 5-10 | Various types |
| Workflows | 2 | Prebuilt |
| Recruiting Reqs | 5 | Open positions |
| Candidates | 30 | Pipeline |
| Pay Groups | 2 | Weekly/Biweekly |
| Historical Payroll | 2 runs | For reports |

### 6.3 Data Freshness

| Frequencia | Acao |
|------------|------|
| Weekly | 1-2 new hires, move 1 candidate |
| Pay Period | PTO accrual simulation |
| Monthly | Refresh announcements, reviews |

---

## 7. Health Checks

### Daily Checks
- [ ] Login as admin, manager, employee
- [ ] Worker profile loads
- [ ] PTO request works
- [ ] Magic Doc template exists

### Weekly Checks
- [ ] Payroll linkage works
- [ ] Job costing proof point
- [ ] No permission regressions

### Automation Script
```python
def daily_health_check():
    # 1. Login
    login_qbo('thiago@testbox.com')

    # 2. Check employees
    navigate('/app/employees')
    assert page.locator('table').count() > 0

    # 3. Check payroll
    navigate('/app/payroll')
    assert 'Overview' in page.content()

    # 4. Check time
    navigate('/app/timetracking')
    assert page.locator('form').count() > 0

    # 5. Check Mineral
    navigate('/app/hr')
    page.click('text=Go to Mineral')
    assert 'trustmineral.com' in page.url
```

---

## 8. Risk Register

| Risk | Impact | Likelihood | Mitigation | Owner |
|------|--------|------------|------------|-------|
| PRDs atrasados | Alto | Medio | Weekly follow-up | Katherine |
| Sandbox inacessivel | Alto | Baixo | Backup environment | Thiago |
| Procurement delay | Alto | Medio | Early SOW draft | Katherine |
| License count unclear | Medio | Alto | Confirm with Nir | Katherine |
| Mineral integration TBD | Medio | Alto | Document as-is | Thiago |

---

## 9. Stakeholders

### Intuit WFS Team
| Nome | Role | Responsabilidade |
|------|------|------------------|
| Ben Hale | Sales Enablement | Demo requirements |
| Nikki Behn | Marketing | Messaging |
| Kyla Ellerd | Sales Program | Coordination |
| Christina Duarte | Leadership | Approvals |
| Nir | Headcount | License forecast |

### TestBox Team
| Nome | Role | Responsabilidade |
|------|------|------------------|
| Katherine Lu | Program Lead | SOW, timeline, stakeholders |
| Thiago Rodrigues | TSA | Data, automation, technical |

---

## 10. Next Steps

### Imediato (Esta Semana)
1. [ ] Aguardar PRDs da Intuit
2. [ ] Katherine: Finalizar SOW draft
3. [ ] Thiago: Testar automation scripts
4. [ ] Schedule weekly sync

### Proximo Sprint
1. [ ] Confirmar sandbox access dates
2. [ ] Definir license count
3. [ ] Validar demo stories com Intuit
4. [ ] Setup Wave 1 environment

---

## 11. Appendix: Links Rapidos

### QBO Navigation
```
Homepage:     https://qbo.intuit.com/app/homepage
Payroll:      https://qbo.intuit.com/app/payroll
Employees:    https://qbo.intuit.com/app/employees
Time:         https://qbo.intuit.com/app/timetracking
HR Advisor:   https://qbo.intuit.com/app/hr
Projects:     https://qbo.intuit.com/app/projects
```

### Mineral
```
Dashboard:    https://apps.trustmineral.com/dashboard
Compliance:   https://apps.trustmineral.com/hr-compliance
Training:     https://apps.trustmineral.com/training
Templates:    https://apps.trustmineral.com/templates
```

### APIs
```
QBO REST:     https://quickbooks.api.intuit.com/v3/company/{realmId}/
QBO GraphQL:  https://qb.api.intuit.com/graphql
Mineral:      (privada - contato necessario)
```

---

Ultima atualizacao: 2025-12-19 13:45
