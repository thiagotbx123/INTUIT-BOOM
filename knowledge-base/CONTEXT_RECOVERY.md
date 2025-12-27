# Guia de Recuperacao de Contexto

> Para futuras instancias do Claude retomarem o trabalho rapidamente

## INICIO RAPIDO

```
1. Leia CLAUDE.md (instrucoes do projeto)
2. Leia strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md (status atual)
3. Leia .claude/memory.md (contexto persistente)
```

## ARQUIVOS CRITICOS POR ORDEM DE IMPORTANCIA

### 1. Status Atual (LER PRIMEIRO)
- `knowledge-base/strategic-cortex/OUTPUT_A_EXECUTIVE_SNAPSHOT.md`
  - Onde estamos
  - Riscos ativos
  - Decisoes recentes
  - Proximos passos

### 2. Contexto Persistente
- `.claude/memory.md`
  - Historico de sessoes
  - Decisoes tomadas
  - Bloqueios conhecidos
  - WFS/QBO context

### 3. Instrucoes do Projeto
- `CLAUDE.md`
  - Sistema de camadas
  - Comandos disponiveis
  - Estrutura do projeto

### 4. Busca Rapida
- `knowledge-base/strategic-cortex/OUTPUT_D_KEYWORD_MAP_LINEAR_RECIPES.md`
  - Keywords por tema
  - Queries para Drive
  - Queries para Linear

### 5. Mudancas Recentes
- `knowledge-base/strategic-cortex/OUTPUT_E_DELTA_SUMMARY.md`
  - Delta 30 dias
  - Novos riscos
  - Alteracoes de escopo

## SPINEHUB - MEMORIA GLOBAL

### Localizacao
```
C:\Users\adm_r\Projects\TSA_CORTEX\data\spinehub.json
```

### Contem
- Entidades: pessoas, canais, projetos
- Relacoes: quem trabalha com quem
- Artefatos: arquivos com URLs completas
- 264KB de conhecimento persistente

### Atualizar SpineHub
```bash
cd C:\Users\adm_r\Projects\TSA_CORTEX
node dist/cli/index.js collect -s "2025-12-20" -e "2025-12-27"
```

## FLUXO DE TRABALHO

### Inicio de Sessao
1. Ler OUTPUT_A para status atual
2. Ler memory.md para contexto
3. Verificar sessions/ para historico

### Durante Trabalho
- Usar TodoWrite para tracking
- Documentar decisoes importantes
- Atualizar riscos se necessario

### Fim de Sessao
1. Executar /consolidar
2. Criar arquivo em sessions/
3. Atualizar memory.md
4. Commit e push

## TEMAS PRINCIPAIS

### WFS (Workforce Solutions) - FOCO ATUAL
- SOW v1.1 em draft
- Timeline: Alpha Dez/25, Beta Fev/26, GA Mai/26
- Arquivos: knowledge-base/wfs/

### QBO/TCO - MANUTENCAO
- Fall Release entregue
- 3 blockers P1 ativos
- Arquivos: knowledge-base/qbo/

### Strategic Cortex - INTELIGENCIA
- 5 outputs (A-E)
- Atualizado: 2025-12-27
- 20,426 arquivos indexados

## ESPECIALIDADES ADQUIRIDAS

Como Claude, tenho conhecimento profundo de:
1. QuickBooks Online (QBO) - estrutura, features, environments
2. WFS/Workforce Solutions - roadmap, stakeholders, timeline
3. TCO Multi-entity - Apex Tire, Global Tread, RoadReady
4. TestBox platform - datasets, ingest, health checks
5. Intuit Fall Release - validacao, evidencias, UAT

## RISCOS ATIVOS (2025-12-27)

| Risco | Impacto | Status |
|-------|---------|--------|
| WFS Environment Decision | P0 | PENDING |
| Negative Inventory TCO | P1 | OPEN |
| Login ECS Task | P1 | WORKAROUND |

---

Documento criado: 2025-12-27
Proposito: Recuperacao rapida de contexto entre sessoes
