# QBO Support Bot - Setup Guide

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    SLACK WORKSPACE                          │
│  [@bot mencionado] ──► Evento via Socket Mode               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              SLACK BOT (rodando local)                      │
│                                                             │
│  1. Recebe menção do Slack                                  │
│  2. Busca contexto na base local (knowledge-base/)          │
│  3. Busca na web (DuckDuckGo) para complementar             │
│  4. Envia para Claude Code CLI processar                    │
│  5. Envia DM privada pro Thiago com sugestão                │
└─────────────────────────────────────────────────────────────┘
```

## Base de Conhecimento

A pasta `knowledge-base/` contém todo o contexto que o bot usa ANTES de buscar na web:

```
knowledge-base/
├── INDEX.md                    <- Catálogo de fontes
├── qbo/
│   └── QBO_DEEP_MASTER_v1.txt  <- Documento principal (11k+ linhas)
├── wfs/                        <- Workforce Solutions
├── slack-threads/              <- Extrações do Slack
├── meetings/                   <- Notas de reuniões
├── access/                     <- Ambientes, logins
└── governance/                 <- MFA, recovery, etc
```

### Adicionando Conhecimento

Simplesmente adicione arquivos `.txt` ou `.md` nas pastas apropriadas.
O bot carrega automaticamente na inicialização.

---

## Setup do Slack App

### 1. Criar Slack App

1. Acesse https://api.slack.com/apps
2. Clique "Create New App" → "From scratch"
3. Nome: `QBO Support Bot`
4. Workspace: Seu workspace

### 2. Socket Mode

1. Menu: **Socket Mode**
2. Enable: **ON**
3. Generate token → nome: `socket-token`, scope: `connections:write`
4. Copie `xapp-...` → `SLACK_APP_TOKEN`

### 3. Bot Token Scopes

Menu: **OAuth & Permissions** → Bot Token Scopes:
- `app_mentions:read`
- `channels:history`
- `channels:read`
- `chat:write`
- `im:history`
- `im:read`
- `im:write`
- `users:read`

Install to Workspace → copie `xoxb-...` → `SLACK_BOT_TOKEN`

### 4. Event Subscriptions

Menu: **Event Subscriptions**
- Enable: **ON**
- Subscribe to bot events:
  - `app_mention`
  - `message.im`

### 5. Pegar User ID

No Slack: seu perfil → "..." → Copy member ID → `MY_SLACK_USER_ID`

---

## Rodar o Bot

```bash
cd slack-bot
pip install -r requirements.txt
python main.py
```

### Testar

1. `/invite @QBO Support Bot` em um canal
2. Mencione o bot ou seja mencionado
3. Receba DM com sugestão
4. Comandos na DM:
   - `aprovar [id]` - posta
   - `editar [id] [texto]` - posta editado
   - `refinar [id] [feedback]` - melhora
   - `ignorar [id]` - descarta
   - `status` - ver pendentes
   - `help` - ajuda

---

## Troubleshooting

**Bot não responde:**
- Verifique se está no canal
- Verifique logs no terminal
- Confirme Socket Mode ON

**Erro "duckduckgo_search not installed":**
```bash
pip install duckduckgo-search
```

**Claude CLI não encontrado:**
- Instale: `npm install -g @anthropic/claude-code`
- Ou configure path manualmente

**Base de conhecimento não carrega:**
- Verifique se `knowledge-base/qbo/QBO_DEEP_MASTER_v1.txt` existe
- Verifique encoding (deve ser UTF-8)
