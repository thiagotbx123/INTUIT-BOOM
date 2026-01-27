# URGENTE: Acoes Alexandra - February Release

> **Data:** 2026-01-27
> **De:** Thiago Rodrigues
> **Para:** Alexandra Lacerda
> **Prazo:** HOJE (EOD)
> **Prioridade:** CRITICA

---

## SITUACAO

A kat mandou mensagem pedindo confirmacao sobre o February Release.
Feature flags sobem em **3 de fevereiro (7 dias uteis)**.
Ela precisa de resposta **HOJE**.

---

## SUAS ACOES (em ordem)

### ACAO 1: Pedir Acesso aos 3 Docs (FAZER AGORA)

Acesse o link que a kat mandou no Slack:
```
https://testbox-talk.slack.com/archives/C0A790REMGD/p1769211731972179
```

Clique nos 3 links e peca acesso:
1. **UAT doc** - Features Feb, PMs, click-paths, demo videos
2. **CID doc** - CIDs das test accounts
3. **Feature flags tracking** - Status das flags

**Se nao conseguir acesso**, avise a kat imediatamente:
```
Oi kat, pedi acesso aos 3 docs mas ainda nao recebi.
Pode pingar o time pra liberar?
```

---

### ACAO 2: Ler o Plano do Marcus (FAZER AGORA)

O plano completo esta na thread. Resumo:

| Data | O que acontece | Quem faz |
|------|----------------|----------|
| Antes de 2/3 | Preencher colunas B, C, E no UAT doc | Gregory team |
| **2/3 - 21:30 PT** | Feature flags habilitadas no staging | Siji George |
| 2/4 | Validar features no TCO staging | Gregory team |
| 2/4+ | Construir dados no staging | TBX (nos) |
| Apos validacao | Portar para PROD (TCO, Keystone) | - |

---

### ACAO 3: Verificar Status do Staging (FAZER AGORA)

A kat precisa saber:
> "Staging clone environments de Keystone e TCO estarao prontos ate 2/3?"

**Voce precisa descobrir isso HOJE.**

Perguntas para responder:
- [ ] Temos staging de TCO pronto?
- [ ] Temos staging de Keystone pronto?
- [ ] Se nao, quando estara pronto?
- [ ] Se nao der tempo, precisamos do Plano B (usar PROD)

**Se voce NAO souber a resposta**, pergunte para:
1. Thiago (eu)
2. Ou kat diretamente

---

### ACAO 4: Responder a kat (FAZER HOJE)

Depois de verificar o status, responda a kat.

**Use um destes templates:**

---

**Se staging VAI estar pronto:**
```
Oi kat! Confirmado:

1. Pedi acesso aos 3 docs ✓
2. Li o plano e entendi os riscos ✓
3. Staging de TCO e Keystone estarao prontos ate 2/3 ✓

Seguimos com o plano original. Qualquer duvida, me avisa!
```

---

**Se staging NAO vai estar pronto:**
```
Oi kat! Confirmado:

1. Pedi acesso aos 3 docs ✓
2. Li o plano e entendi os riscos ✓
3. ⚠️ Staging NAO estara pronto ate 2/3

Precisamos do Plano B (PROD accounts como no Fall Release).
Podemos alinhar ainda hoje sobre os proximos passos?
```

---

**Se ainda nao sabe:**
```
Oi kat! Update parcial:

1. Pedi acesso aos 3 docs ✓
2. Li o plano e entendi os riscos ✓
3. Estou verificando status do staging com o time

Te confirmo ate [HORARIO] se vai dar tempo ou se precisamos do Plano B.
```

---

## CHECKLIST FINAL

Antes de sair hoje, confirme:

- [ ] Pedi acesso aos 3 docs
- [ ] Li o plano do Marcus na thread
- [ ] Verifiquei status do staging (ou perguntei pra quem sabe)
- [ ] Respondi a kat com uma das opcoes acima

---

## RISCOS SE NAO FIZER HOJE

1. Kat pode escalar que TBX nao respondeu
2. Podem decidir plano sem nossa opiniao
3. Ficaremos correndo atras depois

---

## SE TIVER DUVIDAS

Falar com Thiago ANTES de responder a kat sobre:
- Status real do staging
- Se precisamos do Plano B
- Qualquer coisa que voce nao tenha certeza

**NAO invente resposta. Se nao souber, diz que esta verificando.**

---

## TIMELINE RESUMIDO

```
HOJE (27/01)
  └── Pedir acesso docs
  └── Ler plano
  └── Verificar staging
  └── Responder kat

2/3 (Segunda)
  └── Feature flags sobem 21:30 PT
  └── Staging precisa estar pronto

2/4 (Terca)
  └── Validacao comeca
  └── TBX constroi dados
```

---

**Qualquer duvida, me chama!**

Thiago
