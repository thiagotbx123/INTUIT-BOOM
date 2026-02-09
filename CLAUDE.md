# INSTRUCOES PARA CLAUDE - INTUIT-BOOM

## REGRAS FUNDAMENTAIS

### 1. CAMADAS PROTEGIDAS
**LEIA LAYERS.md ANTES DE QUALQUER ALTERACAO**

Este projeto usa sistema de camadas protegidas:
- LOCKED = NAO ALTERAR sem autorizacao explicita
- OPEN = Pode alterar livremente
- REVIEW = Consultar antes de alterar

### 2. PERSISTENCIA DE CONHECIMENTO
**USE `.claude/memory.md` PARA CONTEXTO ENTRE SESSOES**

Ao iniciar uma sessao, leia memory.md para entender o estado atual.
Ao finalizar, execute `/consolidar` para salvar aprendizados.

---

## ANTES DE EDITAR QUALQUER ARQUIVO

1. Verificar em LAYERS.md qual camada o arquivo pertence
2. Se camada LOCKED: PARAR e perguntar "Posso alterar [arquivo]?"
3. Se camada OPEN: pode prosseguir
4. Se camada REVIEW: avisar o que vai fazer antes

---

## COMANDOS DO SISTEMA

### Operacionais (Slash Commands)
| Comando | Descricao |
|---------|-----------|
| `/status` | Ver estado do projeto, camadas e ultimas atividades |
| `/consolidar` | Salvar aprendizados da sessao + commit GitHub |

### Comandos do Usuario (Texto Livre)
| Comando | Acao |
|---------|------|
| "Autorizo alteracao na CAMADA X" | Permissao para alterar camada LOCKED |
| "Tranca a CAMADA X" | Marcar como LOCKED em LAYERS.md |
| "Abre a CAMADA X" | Marcar como OPEN em LAYERS.md |
| "Status das camadas" | Mostrar resumo de LAYERS.md |

---

## FLUXO DE TRABALHO RECOMENDADO

```
1. INICIAR SESSAO
   - /status (ver estado atual)

2. TRABALHAR
   - Verificar LAYERS.md antes de editar
   - Respeitar camadas LOCKED
   - Documentar decisoes importantes

3. FINALIZAR SESSAO
   - /consolidar (salvar tudo + git push)
```

---

## ESTRUTURA DO PROJETO

```
intuit-boom/
├── CLAUDE.md              <- ESTE ARQUIVO (ler sempre)
├── LAYERS.md              <- STATUS DAS CAMADAS (consultar antes de editar)
├── .claude/
│   ├── memory.md          <- CONTEXTO PERSISTENTE (ler no inicio)
│   ├── settings.local.json
│   └── commands/          <- Slash commands
├── sessions/              <- HISTORICO DE SESSOES
├── qbo_checker/           <- Modulos principais
├── knowledge-base/        <- Base de conhecimento QBO
├── docs/                  <- Documentacao
└── data/                  <- Cache e dados
```

---

## CONTEXTO DO PROJETO

- **Objetivo**: Validacao de features do QBO Fall Release para Intuit
- **Projeto principal**: TCO usa company "Apex Tire"
- **Screenshots**: G:\Meu Drive\TestBox\QBO-Evidence\
- **Output**: Planilha Excel com hyperlinks do Drive

---

## CONTAS DE LOGIN

| Codigo | Projeto | Email |
|--------|---------|-------|
| 1 | CONSTRUCTION | quickbooks-test-account@tbxofficial.com |
| 2 | TCO | quickbooks-testuser-tco-tbxdemo@tbxofficial.com |
| 3 | PRODUCT | quickbooks-tbx-product-team-test@tbxofficial.com |
| 4 | TCO DEMO | quickbooks-tco-tbxdemo@tbxofficial.com |

---

## FLUXO DE VALIDACAO (CAMADAS)

| Ordem | Camada | Responsabilidade |
|-------|--------|------------------|
| 1 | Login | Autenticacao Intuit + CDP |
| 2 | Navegacao | Rotas e troca de companies |
| 3 | Screenshot | Captura de evidencias |
| 4 | Planilha | Geracao Excel + hyperlinks |
| 5 | Orquestracao | Fluxo completo coordenado |

---

## FONTES DE CONHECIMENTO

### Hierarquia de Consulta
1. **Strategic Cortex** - `knowledge-base/strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md` (LER PRIMEIRO)
2. **memory.md** - `.claude/memory.md` (contexto persistente)
3. **knowledge-base/** - Documentacao local detalhada
4. **sessions/** - Historico de sessoes anteriores
5. **SpineHub** - `C:\Users\adm_r\Projects\TSA_CORTEX\data\spinehub.json` (entidades globais)
6. **Web** - Apenas se local nao tiver a resposta

### Arquivos Importantes
- `knowledge-base/strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md` - **STATUS ATUAL DO PROJETO**
- `knowledge-base/strategic-cortex/OUTPUT_D_KEYWORD_MAP_LINEAR_RECIPES.md` - Busca rapida
- `knowledge-base/qbo/QBO_DEEP_MASTER_v1.txt` - Conhecimento principal QBO
- `knowledge-base/INDEX.md` - Indice de toda a base

---

## SPINEHUB - MEMORIA PERSISTENTE

### O que e
SpineHub e o backbone de persistencia do TSA_CORTEX que armazena:
- Entidades (pessoas, canais, projetos)
- Relacoes (quem trabalha com quem)
- Artefatos (arquivos com URLs)
- Patterns (padroes identificados)

### Localizacao
```
C:\Users\adm_r\Projects\TSA_CORTEX\data\spinehub.json
```

### Como usar
1. Para atualizar o SpineHub:
```bash
cd C:\Users\adm_r\Projects\TSA_CORTEX
npx ts-node src/cli/index.ts collect --all
```

2. Para consultar entidades:
```bash
npx ts-node src/cli/index.ts query --entity "Katherine"
```

### Learnings
Novos aprendizados devem ser documentados em:
```
C:\Users\adm_r\Projects\TSA_CORTEX\knowledge-base\learnings\
```

---

## STRATEGIC CORTEX - INTELIGENCIA CONSOLIDADA

### 5 Outputs
| Output | Arquivo | Uso |
|--------|---------|-----|
| A | OUTPUT_A_EXECUTIVE_SNAPSHOT.md | Status rapido - LER PRIMEIRO |
| B | OUTPUT_B_STRATEGIC_MAP.md | Conexoes e arquitetura |
| C | OUTPUT_C_KNOWLEDGE_BASE.json | Dados estruturados |
| D | OUTPUT_D_KEYWORD_MAP_LINEAR_RECIPES.md | Busca rapida |
| E | OUTPUT_E_DELTA_SUMMARY.md | Mudancas recentes |

### Metricas Atuais (2025-12-27)
- Drive: 20,426 arquivos (1,926 relevantes)
- Slack: 10 canais monitorados
- Riscos ativos: 7 (2 P0/P1)
- Knowledge items: 847

---

## CONTEXTO ATUAL DO PROJETO (2026-02-08)

### Foco Principal: DATA INGESTION - Construction Dataset (Keystone)
- **Status:** 15 CSVs prontos, 189/189 audit PASS, aguardando Augusto ingerir
- **Dataset ID:** `321c6fa0-a4ee-4e05-b085-7b4d51473495`
- **DB:** `tbx-postgres-staging.internal:5433` user=unstable db=unstable (Tailscale VPN)
- **20 bugs encontrados e corrigidos** (ver MEMORY.md)
- **59 regras documentadas** (21 QB + 13 BIZ + 14 RL + 11 PIPE)

### Arquivos CRITICOS de Referencia
| Arquivo | Local | O que |
|---------|-------|-------|
| MEMORY.md | `.claude/projects/.../memory/` | Contexto persistente COMPLETO |
| health_check_methodology.md | `.claude/projects/.../memory/` | Checklist 59 regras detalhado |
| SLACK_INGESTION_LESSONS.md | `.claude/projects/.../memory/` | 23 incidentes de ingestao |
| SESSION_HANDOFF_2026-02-08.md | `Downloads/INGESTION_PLANS/` | Handoff completo |
| GUIA_INGESTION_AUGUSTO.md | `Downloads/INGESTION_PLANS/` | Guia passo-a-passo |
| audit_all_tables_v2.py | `Downloads/INGESTION_PLANS/` | 189 checks automatizados |
| REGRAS_MASTER_DATABASE.md | `Downloads/INGESTION_PLANS/` | 39 regras master |
| CHECKLIST xlsx | `Downloads/PARA_AUGUSTO/` | Checklist em Excel |

### P&L Final
| CT | Income | Net | Margin |
|---|---|---|---|
| parent | $3.02M | +$766K | 25.4% |
| main_child | $5.11M | +$1.46M | 28.5% |
| secondary_child | $2.80M | +$700K | 25.0% |
| **TOTAL** | **$10.93M** | **+$2.93M** | **26.8%** |

### Company Types
- **parent**: Keystone Construction (Par) - bank_account=5
- **main_child**: Keystone BlueCraft - bank_account=6, TEM PAYROLL ($1.78M)
- **secondary_child**: Terra, Volt, Stonecraft, Ironcraft, Ecocraft, Canopy - bank_account=6

### Pendencias
1. PO table name: singular vs plural (Augusto confirmar)
2. Re-upload CSVs atualizados (fix TXN-13131) ao Google Drive
3. Aguardar Augusto ingerir

### Riscos Pos-Ingestao (do Slack audit)
1. Employee duplication via API retry (90 dupes encontrados antes)
2. Third-party data contamination (Intuit SEs)
3. Gateway timeout 504 em CSVs grandes (>3K rows)

### Historico
- Fall Release: ENTREGUE (11/20/2025)
- WFS SOW v1.1: Em andamento
- Data Ingestion: 8+ sessoes desde 2026-01-23

---

Ultima atualizacao: 2026-02-08
