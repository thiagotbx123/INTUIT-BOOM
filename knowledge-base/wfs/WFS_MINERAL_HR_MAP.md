# WFS Mineral HR - Mapeamento Completo

**Data:** 2025-12-19
**Status:** MAPEADO COM SUCESSO
**Ambiente:** GoQuick Alpha Retail
**Conta:** thiago@testbox.com

---

## 1. Acesso ao Mineral

### Fluxo de Acesso (Confirmado)
1. Login no QBO com conta autorizada
2. Selecionar empresa **GoQuick Alpha Retail**
3. Menu: **Payroll > HR advisor**
4. Clicar em **"Go to Mineral"**
5. Abre nova aba: `apps.trustmineral.com/dashboard`

### URLs
- QBO HR Advisor: `https://qbo.intuit.com/app/hr`
- Mineral Dashboard: `https://apps.trustmineral.com/dashboard`

### Empresas com Acesso
| Empresa | Mineral Access |
|---------|----------------|
| GoQuick Alpha Retail | **SIM** |
| Keystone Construction Canada | NAO (404) |

---

## 2. Interface do Mineral

### Header
- **Logo:** Intuit QuickBooks
- **Branding:** "Powered By Mineral" (MITRATECH)
- **Search:** "Search Content and Documents in the Platform"
- **Icons:** Calendar, Notifications, User Profile

### Menu Principal
| Item | Descricao |
|------|-----------|
| HR Compliance | Updates de compliance, leis trabalhistas |
| Company Policies | Politicas da empresa |
| Safety | Seguranca no trabalho |
| Training | Treinamentos para funcionarios |
| HR Tools | Ferramentas de HR |
| Templates | Modelos de documentos |
| Resources | Recursos e guias |
| Community | Comunidade de usuarios |
| Help | Suporte e ajuda |

---

## 3. Dashboard Principal

### Secoes Identificadas

**Banner de Upsell:**
- "Upgrade to Hands-on Guidance From a Dedicated HR Expert"
- Botao "Learn More"

**My Dashboard:**
- Featured Content
- Compliance Updates
- Featured Topics (ex: "Wage and Hour")

**Get Help Button:** Canto inferior direito

---

## 4. HR Advisor no QBO

### Acesso via QBO
**Rota:** Payroll > HR advisor

### Categorias Disponiveis
1. **Hiring and onboarding**
   - Job description
   - New hire checklist
   - Offer letter template

2. **Setting policies**

3. **Following HR laws**

4. **Managing conflict**

5. **Terminating**

### Acoes Disponiveis
- "Send a question" - Enviar pergunta para experts
- "Talk to an expert" - Falar com especialista
- "Go to Mineral" - Acessar plataforma completa

---

## 5. Comparativo Mineral vs WFS

| Feature | Mineral | WFS | Overlap |
|---------|---------|-----|---------|
| HR Compliance | **Forte** (3000+ regs) | TBD | Complementar |
| Employee Handbook | Smart Handbook | Magic Docs | Potencial |
| Training | Cursos inclusos | TBD | Complementar |
| Templates | Forms, letters, policies | Magic Docs | Potencial |
| Payroll | Via QBO | Nativo | Diferente |
| PTO/Time Off | Limitado | **Forte** | WFS melhor |
| Recruiting | NAO | **Sim** | WFS unico |
| Onboarding | Templates | **Workflow** | WFS melhor |
| Performance | NAO | **Sim** | WFS unico |
| Job Costing | NAO | **Sim** | WFS unico |

---

## 6. API do Mineral

### Status
- Developer Hub existe mas e privado (403)
- URL staging: `developers.dev.trustmineral-staging.com`

### Integracao Atual
- SSO via Intuit authentication
- Nao ha API publica documentada
- Acesso embedded no QBO Payroll

### Para Investigar API
1. Contatar Mitratech/Mineral diretamente
2. Verificar se ha partnership agreement
3. Solicitar acesso ao Developer Hub

---

## 7. Screenshots Capturados

### Mineral Dashboard
```
wfs_mapping/screenshots/mineral/
├── mineral_dashboard_real.png    # Dashboard principal
├── mineral_new_tab.png           # Dashboard via SSO
├── goquick_hr.png                # HR Advisor no QBO
└── sections/
    ├── hr_compliance.png
    ├── company_policies.png
    ├── training.png
    ├── hr_tools.png
    ├── templates.png
    └── resources.png
```

---

## 8. Conclusoes

### Mineral e ideal para:
- Compliance tracking automatizado
- Templates de documentos HR
- Treinamentos de funcionarios
- Suporte de especialistas HR

### WFS e ideal para:
- Employee lifecycle completo
- PTO/Time off management
- Recruiting e onboarding workflow
- Performance management
- Job costing

### Recomendacao
**WFS + Mineral = Complementares**
- Mineral: Compliance e templates
- WFS: Lifecycle e workflow

---

## 9. Proximos Passos

1. [x] Acessar Mineral via GoQuick Alpha Retail
2. [x] Mapear dashboard e menu
3. [x] Identificar features principais
4. [ ] Explorar cada secao em detalhe quando carregar
5. [ ] Investigar API para integracao
6. [ ] Confirmar decisao de integracao com Intuit

---

Ultima atualizacao: 2025-12-19 13:00
