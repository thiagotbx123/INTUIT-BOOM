# INTUIT-BOOM - Checklist de Credenciais e Acessos

> **IMPORTANTE:** Este documento NAO contem senhas ou tokens reais.
> Ele lista O QUE precisa ser transferido e ONDE encontrar.

---

## CREDENCIAIS A TRANSFERIR

### 1. QBO Login Accounts (4 contas)
- **O que:** 4 contas de login QuickBooks Online (email + senha + TOTP)
- **Onde esta:** Hardcoded em `layer1_login.py` (PROJECTS dict)
- **Contas:**
  - TCO: quickbooks-testuser-tco-tbxdemo@tbxofficial.com
  - CONSTRUCTION: quickbooks-test-account@tbxofficial.com
  - PRODUCT: quickbooks-tbx-product-team-test@tbxofficial.com
  - TCO_DEMO: quickbooks-tco-tbxdemo@tbxofficial.com
- **TOTP Secret:** Em layer1_login.py (variavel TOTP_SECRET)
- **Acao:** Compartilhar credenciais via canal seguro

### 2. Linear API Key
- **O que:** Chave de acesso a API do Linear (GraphQL)
- **Onde esta:** `C:\Users\adm_r\Tools\LINEAR_AUTO\.env` (variavel LINEAR_API_KEY)
- **Acao:** Compartilhar ou gerar nova key

### 3. Google Drive OAuth Token
- **O que:** Token OAuth2 para Google Drive API
- **Onde esta:** `C:\Users\adm_r\token_drive.pickle`
- **OAuth Project:** 486245165530
- **Client Secret:** `client_secret_486245165530-*.json` (em Downloads)
- **Acao:** Re-autenticar no ambiente novo (token expira)

### 4. QB OAuth Manager
- **O que:** OAuth tokens para QuickBooks API
- **Onde esta:** `C:\Users\adm_r\Integrations\qb-oauth-manager\config.json`
- **Realm IDs:** Construction (9341454796804202), Terra (9341454842738078), BlueCraft (9341454842756096)
- **Acao:** Configurar no novo ambiente + re-autenticar

### 5. GitHub Access
- **Repo:** https://github.com/thiagotbx123/intuit-boom.git (verificar)
- **Acao:** Adicionar novo operador como collaborator ou transferir

### 6. Coda API Token
- **O que:** Acesso a API do Coda
- **Onde esta:** Variavel CODA_API_TOKEN (verificar .env files)
- **Acao:** Compartilhar ou gerar novo

### 7. Slack User Token
- **O que:** Token xoxp- para Slack API (search)
- **Onde esta:** TSA_CORTEX config ou .env
- **Acao:** Gerar novo token para novo operador

### 8. Linear Project Access
- **Project:** Intuit/QBO related tickets
- **Teams:** Platypus (PLA), Raccoons (RAC), Koala (KLA)
- **URL:** linear.app/testbox/
- **Acao:** Garantir acesso ao workspace

### 9. QBO MCP Server Config
- **O que:** QUICKBOOKS_CLIENT_ID e QUICKBOOKS_CLIENT_SECRET
- **Onde esta:** `C:\Users\adm_r\Integrations\quickbooks-online-mcp-server\.env`
- **Acao:** Configurar no novo ambiente

---

## CHECKLIST DE TRANSFERENCIA

```
[ ] 1. QBO login accounts (4 contas + senhas + TOTP)
[ ] 2. Linear API Key copiada/rotacionada
[ ] 3. GitHub repo: acesso concedido
[ ] 4. Google Drive: re-autenticar OAuth2
[ ] 5. QB OAuth Manager: config.json + re-auth
[ ] 6. Coda API Token compartilhado
[ ] 7. Slack Token: gerar novo
[ ] 8. Linear: acesso ao workspace confirmado
[ ] 9. QBO MCP Server: client ID/secret configurados
[ ] 10. Git clone feito e funcionando
[ ] 11. Python environment configurado (playwright, openpyxl, etc.)
[ ] 12. Chrome com --remote-debugging-port=9222 testado
[ ] 13. Claude Code configurado com .claude/commands/
[ ] 14. SQLite database copiado para ambiente local
[ ] 15. ObsidianVault sincronizado (Master Memory)
```

---

## SEGURANCA

### Rotacionar apos transferencia:
- [ ] QBO passwords (se compartilhadas diretamente)
- [ ] Linear API Key (se compartilhada diretamente)
- [ ] Google OAuth client secret
- [ ] Slack user token

### NAO compartilhar em texto/email:
- API keys e tokens
- TOTP secrets
- Senhas QBO
- OAuth client secrets

### Metodo recomendado:
1. 1Password vault compartilhado OU
2. Credential manager da empresa OU
3. Transferencia presencial/call segura

---

*Checklist criado em 2026-02-06*
