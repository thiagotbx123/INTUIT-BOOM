# INSTRUCOES PARA CLAUDE - INTUIT-BOOM (Transfer Version)

> **REGRAS FUNDAMENTAIS** - Claude DEVE seguir estas instrucoes em TODA sessao.

---

## 1. CAMADAS PROTEGIDAS (LAYERS.md)

**LEIA LAYERS.md ANTES DE QUALQUER ALTERACAO DE CODIGO**

| Status | Significado |
|--------|-------------|
| LOCKED | NAO ALTERAR sem autorizacao explicita |
| OPEN | Pode alterar livremente |
| REVIEW | Consultar antes de alterar |

**Camada 1 (Login):** LOCKED desde 2025-12-06 - `layer1_login.py`
**Camadas 2-5:** OPEN (Navegacao, Captura, Planilha, Orquestracao)

---

## 2. PERSISTENCIA DE CONHECIMENTO

**INICIO de sessao:**
1. Ler `.claude/memory.md` para estado atual
2. Verificar sessions/ para trabalho recente
3. Consultar knowledge-base/ se necessario
4. Ler `strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md` para status rapido

**FIM de sessao:** Executar `/consolidar`

---

## 3. HIERARQUIA DE FONTES DE CONSULTA

| Prioridade | Fonte | Localizacao |
|------------|-------|-------------|
| 1 | Strategic Cortex | `knowledge-base/strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md` |
| 2 | Memory | `.claude/memory.md` |
| 3 | Knowledge Base | `knowledge-base/` (28+ arquivos) |
| 4 | Sessions | `sessions/` (17 sessoes) |
| 5 | SpineHub | `C:\Users\adm_r\Tools\TSA_CORTEX\data\spinehub.json` |
| 6 | Web | Apenas se local nao tiver resposta |

---

## 4. REGRAS DE VALIDACAO (NUNCA IGNORAR)

### Regra 1: Escopo Completo
- ANTES de validar ambiente, listar TODAS as features aplicaveis
- IES = TCO + Construction + Product (mesmas features)

### Regra 2: Paridade de Qualidade
- Se ambiente A tem tracker com N colunas, ambiente B tem N colunas
- Evidence_notes DETALHADAS (o que esta visivel, nao apenas se carregou)

### Regra 3: Validacao Pos-Captura
- Screenshot > 100KB = provavelmente valido
- Screenshot ~140KB = provavel pagina de erro 404
- Verificar conteudo ("sorry", "error" = falha)

### Regra 4: Status Granular
- PASS = Feature funciona como esperado
- PARTIAL = Feature existe com limitacoes
- NOT_AVAILABLE = Feature nao habilitada (diferente de FAIL)
- FAIL = Bug real
- N/A = Documentacao/sem UI

### Regra 5: Comparacao Entre Ambientes
- Screenshots lado a lado, documentar diferencas

---

## 5. CONTAS DE LOGIN

| Codigo | Projeto | Email |
|--------|---------|-------|
| 1 | CONSTRUCTION | quickbooks-test-account@tbxofficial.com |
| 2 | TCO | quickbooks-testuser-tco-tbxdemo@tbxofficial.com |
| 3 | PRODUCT | quickbooks-tbx-product-team-test@tbxofficial.com |
| 4 | TCO DEMO | quickbooks-tco-tbxdemo@tbxofficial.com |

---

## 6. ESTRUTURA DO PROJETO

```
intuit-boom/
├── CLAUDE.md              <- Instrucoes Claude
├── LAYERS.md              <- Status das camadas
├── layer1_login.py        <- LOCKED - Login Intuit (CDP + TOTP)
├── .claude/
│   ├── memory.md          <- Estado persistente
│   ├── settings.local.json
│   └── commands/          <- Slash commands (/status, /consolidar)
├── sessions/              <- 17 sessoes documentadas
├── qbo_checker/           <- Modulos de validacao
│   ├── feature_validator.py  <- Validator v2.0
│   ├── navigator.py       <- Navegacao QBO
│   ├── screenshot.py      <- Captura de evidencias
│   ├── spreadsheet.py     <- Geracao Excel
│   └── features_*.json    <- Definicoes de features
├── knowledge-base/        <- Base de conhecimento
│   ├── INDEX.md           <- Catalogo de fontes
│   ├── qbo/               <- QBO product knowledge
│   ├── wfs/               <- WFS context
│   ├── slack-cortex/      <- Comunicacao Slack
│   ├── drive-cortex/      <- Inventario Drive
│   └── strategic-cortex/  <- Visao consolidada (5 outputs A-E)
├── docs/                  <- Evidencias, reports, trackers
├── EvidencePack/          <- Screenshots por release
└── data/                  <- Cache, databases
```

---

## 7. COMANDOS

| Comando | Funcao |
|---------|--------|
| `/status` | Visao geral do projeto |
| `/consolidar` | Consolidacao de sessao |

---

## 8. EQUIPE E OWNERS

| Role | Nome | Responsabilidade |
|------|------|------------------|
| TSA Lead | Thiago Rodrigues (anterior) | Arquitetura, dados, documentacao |
| TSA WFS | Alexandra Lacerda | WFS execution, data ingestion |
| CE Lead | Lucas Soranzo | Engineering, infra |
| Program | Katherine Lu | SOW, coordenacao |

---

## 9. CONTEXTO CRITICO

### Projetos Relacionados
- **QBO-WFS** (`C:\Users\adm_r\Clients\QBO-WFS\`) - Workforce Solutions
- **coda-qbo-docs** (`C:\Users\adm_r\Knowledge\coda-qbo-docs\`) - Documentacao
- **GOD_EXTRACT** (`C:\Users\adm_r\Knowledge\GOD_EXTRACT\`) - Intelligence extraction
- **quickbooks-online-mcp-server** (`C:\Users\adm_r\Integrations\quickbooks-online-mcp-server\`) - MCP
- **qb-oauth-manager** (`C:\Users\adm_r\Integrations\qb-oauth-manager\`) - OAuth tokens
- **TSA_CORTEX** (`C:\Users\adm_r\Tools\TSA_CORTEX\`) - Worklog automation

### API Access
- **Linear:** `https://api.linear.app/graphql` (key em `Tools/LINEAR_AUTO/.env`)
- **QBO:** OAuth 2.0 via `qb-oauth-manager`
- **Google Drive:** OAuth2 (token em `token_drive.pickle`)

---

*Adaptado de CLAUDE.md + LAYERS.md + memory.md em 2026-02-06*
