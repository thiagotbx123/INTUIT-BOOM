# INTUIT-BOOM - Mapa do Ecossistema

> Todos os projetos, ferramentas e integracoes conectados ao INTUIT-BOOM.

---

## DIAGRAMA DE CONEXOES

```
                    INTUIT-BOOM (Principal)
                    C:\Users\adm_r\Clients\intuit-boom\
                           |
          +----------------+----------------+
          |                |                |
     QBO-WFS          GOD_EXTRACT      coda-qbo-docs
     (WFS Ext)        (Intelligence)   (Docs QBO)
          |                |                |
          +--------+-------+--------+-------+
                   |                |
              TSA_CORTEX       LINEAR_AUTO
              (Worklog)        (Tickets)
                   |
          +--------+--------+
          |                 |
    REPORT_CHECK      SpineHUB
    (QA Reports)      (Framework)
                           |
                    ObsidianVault
                    (Fonte verdade)

--- INTEGRATIONS ---

    qb-oauth-manager -----> QuickBooks API (OAuth 2.0)
    quickbooks-mcp-server -> QBO MCP Protocol
    Google Drive API ------> Evidence Screenshots
    Linear API ------------> Ticket Management
    Slack API -------------> Communication Intel
    Coda API --------------> Documentation
```

---

## PROJETOS DETALHADOS

### 1. INTUIT-BOOM (Principal)
- **Local:** `C:\Users\adm_r\Clients\intuit-boom\`
- **O que faz:** Validacao features QBO, geracao de dados, evidence packs
- **Stack:** Python, Playwright CDP, openpyxl, SQLite, Linear API
- **Git:** https://github.com/thiagotbx123/intuit-boom.git (verificar)

### 2. QBO-WFS (Extensao WFS)
- **Local:** `C:\Users\adm_r\Clients\QBO-WFS\`
- **O que faz:** Workforce Solutions (GoCo + QB Payroll)
- **Status:** BLOQUEADO (environment decision)
- **Owner:** Alexandra Lacerda
- **Docs:** SOW draft v2, implementation plan, 19-section knowledge base, 1944 Slack msgs

### 3. GOD_EXTRACT (Intelligence)
- **Local:** `C:\Users\adm_r\Knowledge\GOD_EXTRACT\`
- **O que faz:** Extracao estrategica de inteligencia multi-fonte
- **Descobertas:** MCP Server Intuit, 24 TSA members, 1,853 tickets analyzed
- **Expert identificado:** Gabriel Taufer (infra, integration, security)

### 4. coda-qbo-docs (Documentacao)
- **Local:** `C:\Users\adm_r\Knowledge\coda-qbo-docs\`
- **O que faz:** Repository de docs QBO, datasets mapeados
- **Contem:** 7 datasets catalogados, credentials, running automations

### 5. quickbooks-online-mcp-server (MCP)
- **Local:** `C:\Users\adm_r\Integrations\quickbooks-online-mcp-server\`
- **O que faz:** Model Context Protocol server para QBO
- **Status:** Instalado (node_modules present)
- **Features:** Account, Bill, Customer, Employee, Invoice, Vendor CRUD

### 6. qb-oauth-manager (OAuth)
- **Local:** `C:\Users\adm_r\Integrations\qb-oauth-manager\`
- **O que faz:** Gerencia tokens OAuth 2.0 para QBO
- **Companies configuradas:**
  - Construction (Keystone) - Realm 9341454796804202
  - Terra - Realm 9341454842738078
  - BlueCraft - Realm 9341454842756096

### 7. TSA_CORTEX (Worklog)
- **Local:** `C:\Users\adm_r\Tools\TSA_CORTEX\`
- **O que faz:** Automacao de worklog, SOPs, investigacao
- **Status:** Production v2.2
- **Outputs:** 11 Linear templates, TMS v2.0, 1,606 eventos coletados
- **REGRA:** Worklog em INGLES 100%, terceira pessoa

### 8. LINEAR_AUTO (Automacao Linear)
- **Local:** `C:\Users\adm_r\Tools\LINEAR_AUTO\`
- **O que faz:** Scripts para criar/atualizar tickets Linear via API
- **Contem:** `.env` com LINEAR_API_KEY

### 9. REPORT_CHECK (QA Reports)
- **Local:** `C:\Users\adm_r\Tools\REPORT_CHECK\`
- **O que faz:** Validacao de daily reports TSA
- **Scoring:** Structure 40pts, Feeling 30pts, Content 30pts

### 10. ObsidianVault (Fonte de Verdade)
- **Local:** `C:\Users\adm_r\ObsidianVault\`
- **O que faz:** Master Memory source
- **Path critico:** `Knowledge/Claude Memory/Master Memory.md`

---

## INTEGRACOES EXTERNAS

| Servico | URL/Endpoint | Auth | Status |
|---------|-------------|------|--------|
| QuickBooks API | quickbooks.intuit.com | OAuth 2.0 | Configurado |
| Linear API | api.linear.app/graphql | API Key | Ativo |
| Google Drive API | googleapis.com | OAuth2 | Configurado |
| Coda API | coda.io/apis/v1 | API Token | Validado |
| Slack API | slack.com/api | User Token (xoxp-) | Validado |

---

## BANCOS DE DADOS LOCAIS

| Database | Local | Conteudo |
|----------|-------|----------|
| qbo_database_TCO_Construction.db | Downloads/ | SQLite com dados TCO+Construction |
| qbo_database.db | Downloads/ | SQLite QBO geral |
| hyperlink_cache.json | intuit-boom/data/ | Cache Drive URLs |
| spinehub.json | TSA_CORTEX/data/ | Entidades SpineHub |

---

*Compilado de exploracao de 10 diretorios + memory files*
