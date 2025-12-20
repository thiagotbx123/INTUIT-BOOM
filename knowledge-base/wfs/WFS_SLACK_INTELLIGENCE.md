# WFS Slack Intelligence - Informacoes Coletadas

**Data:** 2025-12-19
**Fonte:** Slack TestBox (canais internos e externos)
**Coletado por:** Claude Code

---

## 1. Status do Projeto WFS

### Timeline Oficial
| Marco | Data | Status |
|-------|------|--------|
| Alpha Access | 12/12 | CONCLUIDO |
| SOW Draft | 12/19 | EM PROGRESSO |
| SOW para Cliente | Antes do Natal | TARGET |
| WFS Alpha (Intuit) | Dez 2025 | ~100 customers |
| WFS Beta | Fev 2026 | Expanded |
| WFS GA | 01/05/2026 | Full launch |

### Ambiente de Exploracao
- **GoQuick Alpha Retail** - Realm ID: `9341455848423964`
- **Proposito:** Ambiente para TestBox explorar e construir SOW
- **NAO e o ambiente final de demo para sales** (confirmado por Katherine)

---

## 2. Mineral HR - Status de Acesso

### Confirmado Funcionando
```
QBO > Payroll > HR advisor > "Go to Mineral" > apps.trustmineral.com/dashboard
```

### Detalhes do Acesso
| Campo | Valor |
|-------|-------|
| Company | Alpha Retail |
| Realm ID | 9341455848423964 |
| Billing Plan | PR_ELITE |
| Billing Status | PAID |
| Partner | Intuit |
| User Level | Client Admin |

### Usuarios com Acesso
- Thiago (Client Admin)
- Katherine (Client Admin)
- Saubhagya (Client Admin)

### Pergunta Pendente para Kev
> "What is the expected click path for reps to show WFS data flowing into Mineral in that same environment, and what data should we expect to see in Mineral to prove the flow?"

---

## 3. Conversa com Kev (Mineral Team)

### Contexto Fornecido
Katherine explicou:
> "We're working with the Intuit team to spin up demo environments with the WFS features reflected. Part of making that a rich demo story will be showing the integration with MineralHR and demonstrating how data flows from WFS into MineralHR."

### Pedido
1. Contas "premium" provisionadas para dev/testing
2. Documentacao de API (se disponivel)
3. Nivel maximo de funcionalidade para demos

### Resposta de Kev
> "Do you have accounts created for other WFS flows? Those should work for Mineral too if they are Premium and Elite."
> "How would you spin up Mineral in this demo environment that sales folks will use?"

---

## 4. Winter Release (Fevereiro 2026)

### Status
- **24 features** no total (verdes + amarelos)
- **Early Access:** 4 de Fevereiro de 2026
- **Documento:** https://docs.google.com/document/d/1lc-G-ehRWO0C9hdSglj-idNbrFy6SGP-Pq3PaSzNpjY/

### Acao Requerida
Katherine pediu para Thiago e Waki:
> "In the next 3 days before we go on holiday, do you think you can look at the green locked features and determine which of those we'll need to generate new data or automations vs what we already have?"

---

## 5. Demo Stories (Priorizacao Intuit)

### Documento de Referencia
https://docs.google.com/spreadsheets/d/1OMaSA46PdZIo9GDplRDW3xEU94ryD5iE-MbifADcc50/edit?gid=432916029#gid=432916029

### Materiais Disponiveis
- **Video:** https://digitalasset.intuit.com/render/content/dam/intuit/product-marketing/en_us/qb-online/motion-and-video/QB_US_EN_Product-Launches_October2025.mp4
- **Figma:** https://www.figma.com/design/mmyFEznma9lWGJUJso8agx/QB-Design-Exploration?node-id=3843-11165 (precisa solicitar acesso)

---

## 6. Esclarecimentos Importantes

### Sobre GoQuick Alpha Retail
**Katherine confirmou:**
> "This environment is just for us TestBox to explore inside because we need that in order to finish building the SOW."

O ambiente final de demo para sales **sera diferente** e integrado aos ambientes TCO/Keystone existentes.

### Sobre Rollout
> "If this is going to get rolled into the TCO/Keystone environments, we'll need to have a very careful rollout implementation plan bc this will impact all the sellers. So there's the possibility of doing some kind of staged testing/prod first."

---

## 7. Stakeholders Intuit WFS

### Do Slack
| Nome | Role |
|------|------|
| Kev Lubega | Mineral/WFS Team |
| Ben Hale | Sales Enablement |
| Nikki Boehm | ? |
| Kyla | Sales Program |
| Christina | Leadership |

### TestBox
| Nome | Role |
|------|------|
| Katherine Lu | Program Lead |
| Thiago Rodrigues | TSA |
| Lucas Wakigawa (Waki) | TSA Lead |

---

## 8. Documentos de Referencia

### SOW e Scope
- **Scope Plan:** https://docs.google.com/spreadsheets/d/12cuQeVA-BTEDU8l8nEMsC7DPy01xpGWo/edit?gid=1931659991#gid=1931659991
- **SOW Sketch:** https://docs.google.com/document/d/1tvP1QNJWnD4YYnkauwWGtT_qb-hyA3a-/edit

### Fall Release (em progresso)
- **Fall Release Tracker:** https://docs.google.com/spreadsheets/d/11qrIM0M5MUZLfs0aNvOVWCszdTb4XQKbvKpw3F5r_0I/edit?gid=1805450713#gid=1805450713

### Winter Release
- **Write It Straight Doc:** https://docs.google.com/document/d/1lc-G-ehRWO0C9hdSglj-idNbrFy6SGP-Pq3PaSzNpjY/

---

## 9. Proximas Acoes (do Slack)

### Para Thiago
1. [x] Explorar GoQuick Alpha Retail
2. [x] Verificar acesso Mineral HR
3. [x] Confirmar Payroll Elite ativo
4. [ ] Atualizar SOW com scope Mineral HR
5. [ ] Compartilhar SOW draft internamente
6. [ ] Enviar SOW final para cliente

### Para Katherine
- [ ] Confirmar com Kev o click path para reps
- [ ] Definir dados esperados no Mineral para provar flow
- [ ] Confirmar data do Early Access Winter Release

### Pergunta Aberta
> "What is the expected click path for reps to show WFS data flowing into Mineral in that same environment, and what data should we expect to see in Mineral to prove the flow?"

---

## 10. Licencas e Usuarios

### Situacao Atual
- 60 licencas adicionais solicitadas (PO em processamento)
- Christina esta cuidando do PO devido a pessoas OOO

### Email Generico para Admin
Intuit quer usar: `qbdemoteam@intuit.com` como primary admin (em vez de email individual)

---

## 11. Canais Slack Relevantes

| Canal | Proposito |
|-------|-----------|
| `C06PSSGEK8T` (#testbox-intuit-internal) | Comunicacao interna Intuit |
| `D09N49AG4TV` | DM Katherine <-> Thiago |
| `C09MJ6CCU9Y` | Scrum of Scrums / Daily Updates |
| `mpdm-alexandra--gabrielle--thiago--katherine--bhale1--klubega-1` | Chat com Kev sobre Mineral |

---

## 12. Insights para POV/SOW

### O que aprendemos
1. **GoQuick Alpha Retail e temporario** - apenas para exploracao
2. **Ambiente final sera integrado** aos TCO/Keystone existentes
3. **Mineral HR funciona** via SSO com Payroll Elite
4. **Kev pode ajudar** com detalhes do data flow WFS -> Mineral
5. **Winter Release vem ai** - 24 features, Early Access 4/Fev

### Riscos Identificados
1. Click path para reps ainda nao definido
2. Data flow WFS -> Mineral nao documentado
3. Ambiente final de demo TBD
4. Staged rollout pode ser necessario

---

Ultima atualizacao: 2025-12-19 15:00
