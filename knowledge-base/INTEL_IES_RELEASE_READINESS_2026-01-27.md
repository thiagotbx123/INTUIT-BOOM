# INTEL: IES Feature Release Readiness

> **Data:** 2026-01-27
> **Fonte:** Miro board (Lawton) + Slack thread
> **Classificacao:** Inteligencia Estrategica
> **Responsavel:** Alexandra Lacerda

---

## 1. CONTEXTO

O Lawton criou um Miro board documentando o processo da Intuit para suportar quarterly releases no TestBox. Foi compartilhado para Christina Duarte referenciar.

**Miro Board:** IES Feature Release Readiness
**URL:** `https://miro.com/app/live-embed/uXjVGZwISD0=/?focusWidget=3458764651611636311`

---

## 2. PROCESSO DA INTUIT (Mapeado)

```
[Write it Straight] --> [UAT Doc] --> [Siji George] --> [Feature Activation]
      |                     |               |
   Jed McLoughlin      Eunice Lee      CID file + dates
                        + PMs
```

### Etapas Detalhadas

| # | Etapa | Owner | Entregavel |
|---|-------|-------|------------|
| 1 | Write it Straight completed | Jed McLoughlin | Doc com features |
| 2 | Populate UAT doc | Eunice Lee + PMs | Clickpaths + detalhes |
| 3 | Deliver to Siji George | PMs | CID file + key dates |
| 4 | Activate features | Siji George (devs) | Features live |

---

## 3. TIMELINES IMPLICITOS

| Marco | Prazo | Nota |
|-------|-------|------|
| UAT doc finalizado | 1 semana antes go-live | SLA nao-oficial |
| UAT testing group ativado | 8-10 dias antes go-live TBX | Janela de teste |

**Importante:** Esses prazos sao "preferably" - nao sao SLAs formais. Oportunidade de formalizar.

---

## 4. CONTATOS-CHAVE

| Pessoa | Papel | Valor Estrategico |
|--------|-------|-------------------|
| **Siji George** | Ativa features (CID + dates) | Saber quando features vao live |
| **Jed McLoughlin** | Owner Write it Straight | Fonte oficial lista features |
| **Eunice Lee** | Popula UAT doc | Detalhes de clickpaths |
| **Christina Duarte** | Stakeholder informada | Escalation path |
| **Lawton** | Criou o processo | Ponto de contato processo |

---

## 5. DOCUMENTOS PARA MONITORAR

| Doc | Tipo | URL | Conteudo |
|-----|------|-----|----------|
| Write it Straight | Google Doc | `1lc-G-ehRWO0C9hdSglj-idNbrFy6SGP-Pq3PaSzNpjY` | Lista oficial features |
| UAT doc | Google Sheet | `1AppjXKZu5PG5urv-mtPTM6NjguedQ1L7WVfd941UvB4` | Clickpaths + detalhes |
| Working doc (Siji) | Google Sheet | `1PPEdIMsmtkkLA_GfDK6m7vkfKvcpasL6CVx1oxOvvb0` | CID + dates ativacao |

---

## 6. PAIN POINT IDENTIFICADO

> "Feature names from Dev versus feature names in Write It Straight is a huge time killer"

### Traducao
A Intuit tem inconsistencia de nomenclatura entre:
- Nomes usados pelo time de Dev
- Nomes no documento Write It Straight

Isso causa retrabalho e atrasos.

### Oportunidade
TestBox pode oferecer:
1. Glossario de traducao Dev <-> Write It Straight
2. Validacao de nomes antes do release
3. Processo de alinhamento pre-release

---

## 7. CONEXAO COM OUTROS ISSUES

### Thread Rachel (2026-01-26)
- Problemas de dados "bad" no IES Construction
- Bills overdue, Balance Sheet desbalanceado
- Resolvido parcialmente pela kat

### IC Balance Sheet Investigation (2026-01-20)
- Bug de consolidacao escalado (PLA-3201)
- Relacionado ao mesmo ambiente

---

## 8. ACOES RECOMENDADAS

### Alta Prioridade
- [ ] Solicitar acesso aos 3 docs (Write it Straight, UAT, Working doc)
- [ ] Mapear data do proximo quarterly release

### Media Prioridade
- [ ] Estabelecer canal direto com Siji George
- [ ] Propor formalizacao dos SLAs (1 semana, 8-10 dias)

### Baixa Prioridade
- [ ] Oferecer ajuda no pain point de nomenclatura
- [ ] Criar glossario Dev <-> Write It Straight

---

**Documento criado por:** Claude (sessao 2026-01-27)
**Para:** Alexandra Lacerda
**Revisado por:** Thiago Rodrigues
