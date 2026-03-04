# 3-Gate Ingestion Validation Pipeline

> Regras canônicas para ingestão de dados no QBO. Todo dataset DEVE passar pelos 3 gates antes de ser considerado válido.

## Overview

```
CSVs prontos
    │
    ▼
┌─────────────────────────┐
│  GATE 1: validate_csvs  │  Local, pré-INSERT
│  Script Python           │  91 PASS / 6 FAIL / 9 WARN (último run)
└────────────┬────────────┘
             │ TODOS PASS? → Sim → INSERT no banco
             ▼
┌─────────────────────────┐
│  GATE 2: Retool Validator│  Pós-INSERT, validação backend
│  TMS JWT + Dataset       │  Tabela: ID, Rule slug, Table, Source, Message
└────────────┬────────────┘
             │ 0 ERROS? → Sim → Gate 3
             ▼
┌─────────────────────────┐
│  GATE 3: Auditoria Claude│  Pós-INSERT, coerência geral
│  Múltiplos auditores     │  Simultâneos, especializados, exaustivos
└────────────┬────────────┘
             │ APROVADO? → Dataset VÁLIDO
             ▼
         DONE ✓
```

---

## GATE 1: validate_csvs.py (Pré-INSERT)

### Localização
- Script: `scripts/ingestion/validation/validate_csvs.py`
- Spec: `scripts/ingestion/validation/VALIDATION_SPEC_CONSTRUCTION.xlsx`
- Builder: `scripts/ingestion/validation/build_validation_workbook.py`

### O que valida
- 59 regras em 4 categorias: QB (sistema), BIZ (negócio), RL (realismo), PIPE (pipeline)
- 189 checks automatizados
- FK isolation, sequential IDs, date formats, P&L, margins

### Como rodar
```bash
cd C:\Users\adm_r\Downloads\INGESTION_PLANS
python validate_csvs.py
```

### Critério de passagem
- TODOS os checks PASS (FAIL = 0)
- WARN aceitáveis com justificativa documentada

---

## GATE 2: Retool Validator (Pós-INSERT)

### URL
https://retool.testbox.com/apps/d9d08afa-51c8-11f0-84ee-e712dd42e27c/Integrations/Quickbooks/Quickbooks%20dataset%20validation/defaultPage

### Passo a passo

0. **VERIFICAR AMBIENTE = staging** (rodapé inferior da página)
   - Por default vem como `production` → SEMPRE trocar pra `staging`
   - Bolinha amarela = staging (correto)
   - Localização: canto inferior esquerdo, ao lado de "Retool" e avatar
   - **NUNCA rodar validação em production**

1. **Obter TMS JWT** válido (expira periodicamente)
   - Se expirado → pedir novo ao usuário IMEDIATAMENTE
   - Payload deve ter `aud` compatível com QBO

2. **Colar JWT** no campo "TMS Jwt"

3. **Selecionar Dataset segment** na lista suspensa
   - Datasets disponíveis: construction, professional_services, non_profit, manufacturing, canada_construction, tire_shop
   - Usuário define qual selecionar

4. **Clicar Refresh AZUL** (botão grande ao lado do Dataset segment)
   - Esperar notificação "lambda_call" com ícone SUCCESS (verde)
   - Se ERROR → JWT inválido/expirado → pedir novo

5. **Scrollar para baixo** até a toolbar da tabela principal (superior)

6. **Clicar Refresh da TABELA SUPERIOR** (ícone circular ↻ na toolbar do grid)
   - Tabela carrega com colunas: ID, Rule slug, Segment, Table, Source, Message
   - Mostra cada erro individual com detalhes completos

7. **Clicar Refresh da TABELA INFERIOR** (ícone circular ↻ na toolbar do grid de resumo)
   - Tabela de resumo: Rule, Total
   - Agrega erros por regra com contagem total
   - Útil quando tabela superior tem muitas ocorrências
   - Usar como ponto de partida para priorizar correções (regra com mais erros primeiro)

### Critério de passagem
- 0 erros na tabela superior (detalhes)
- 0 erros na tabela inferior (resumo)

### Ciclo de correção (CÍCLICO até convergir)

```
┌──────────────────────────────────────────────────┐
│  1. LOCALIZAR o erro                             │
│     - Tabela inferior (resumo): priorizar regra  │
│       com mais ocorrências                       │
│     - Tabela superior (detalhe): Rule slug,      │
│       Table, Source, Message                      │
│                                                  │
│  2. INVESTIGAR no PostgreSQL                     │
│     - Conectar ao banco (psycopg2)               │
│     - Consultar a tabela afetada                 │
│     - Encontrar os registros problemáticos       │
│                                                  │
│  3. CONTEXTUALIZAR                               │
│     ├─ Erro NOVO?                                │
│     │  → Documentar em knowledge-base            │
│     │  → Adicionar regra em validate_csvs.py     │
│     │  → Salvar padrão para próximos datasets    │
│     │                                            │
│     └─ Erro CONHECIDO?                           │
│        → Aplicar fix já documentado              │
│                                                  │
│  4. CORRIGIR                                     │
│     - Atualizar CSV fonte                        │
│     - Ou corrigir direto no banco (UPDATE/DELETE) │
│                                                  │
│  5. RE-INGERIR via PostgreSQL                    │
│     - DELETE afetados → INSERT corrigidos         │
│     - Respeitar ordem FK (filhos antes de pais)  │
│                                                  │
│  6. RE-VALIDAR no Retool                         │
│     - Refresh azul → Refresh tabela superior     │
│     - Refresh tabela inferior (resumo)           │
│                                                  │
│  7. AVALIAR                                      │
│     ├─ Ainda tem erros → VOLTA pro passo 1       │
│     ├─ 0 erros → Segue pro Gate 3                │
│     └─ Não sei resolver → PARAR e perguntar      │
│        ao usuário                                │
└──────────────────────────────────────────────────┘
```

### Regra de ouro
- **Cada erro novo é um aprendizado permanente**: documentar SEMPRE
- **Refinar Gate 1 a cada ciclo**: validate_csvs.py deve evoluir pra pegar erros antes de chegar no Retool
- **Não forçar**: se não souber resolver, parar e perguntar

---

## GATE 3: Auditoria Claude (Pós-INSERT)

### O que é
Auditoria geral de coerência executada por mim (Claude) com múltiplos auditores simultâneos, extremamente criteriosos e especializados.

### Auditores planejados
1. **Auditor Financeiro** - P&L por company_type, margens, COGS, income vs expenses
2. **Auditor de Integridade** - FKs, orphans, duplicatas, IDs sequenciais
3. **Auditor de Realismo** - Distribuição, variação, padrões sazonais, nomes
4. **Auditor Cross-Table** - Consistência entre tabelas relacionadas
5. **Auditor de Schema** - Tipos, nulls, constraints, formatos

### Como executar
- Conectar ao banco via psycopg2
- Rodar queries de validação em paralelo
- Comparar resultados com regras documentadas
- Gerar relatório PASS/FAIL/WARN

### Conexão
```python
CONN = {
    "host": "tbx-postgres-staging.internal",
    "port": 5433,
    "user": "unstable",
    "dbname": "unstable",
    "password": "FaMVkKIM0IcsXHCW_323pJync_ofrBsi",
}
```

### Permissões confirmadas
- FULL (INSERT/SELECT/UPDATE/DELETE) em 17 tabelas QBO
- SEM ACESSO em: quickbooks_products_services, quickbooks_purchase_orders

### Critério de passagem
- Todos os auditores PASS
- Nenhum FAIL crítico
- WARNs documentados e justificados

---

## Acesso direto ao banco

### Confirmado em 2026-02-09
- User `unstable` tem INSERT/UPDATE/DELETE em quase todas as tabelas QBO
- Podemos fazer ingestão direta sem depender do csv_ingestor externo
- VPN Tailscale necessária para acesso

### Ordem de operações (do GUIA_INGESTION_AUGUSTO.md)
1. DELETE: filhos/junctions primeiro, depois pais
2. INSERT: pais primeiro, depois filhos
3. VERIFY: row counts, P&L, FKs

---

## Status

| Gate | Status | Última execução |
|------|--------|-----------------|
| Gate 1 | COMMITADO no repo | 91 PASS, 6 FAIL, 9 WARN |
| Gate 2 | PENDENTE (JWT correto necessário) | - |
| Gate 3 | PLANEJADO (não executado ainda) | - |

---

Última atualização: 2026-02-09
