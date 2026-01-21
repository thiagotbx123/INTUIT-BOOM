# DOSSIE: Consolidated Balance Sheet "Out of Balance" Investigation

> **Data:** 2026-01-20
> **Investigadores:** Thiago Rodrigues (TSA Lead), Alexandra Lacerda (TSA)
> **Cliente:** Intuit (David Ball)
> **Ambientes:** TCO (Traction Control Outfitters), IES Construction (Keystone)
> **Status:** ESCALADO PARA ENGINEERING

---

## 1. RESUMO EXECUTIVO

### Problema Reportado
David Ball reportou erro "Your consolidated balance sheet isn't balancing" nos ambientes TCO e IES Construction ao acessar o Consolidated View Balance Sheet.

### Resultado da Investigacao
- **Causa Identificada:** Dados intercompany desbalanceados + conta deletada nos mapeamentos IC
- **Acoes Tomadas:** 7 correcoes aplicadas (mapeamentos + JEs)
- **Resultado:** Correcoes aplicadas nas entidades individuais NAO refletem no Consolidated View
- **Conclusao:** Problema de sistema/backend, nao de dados - requer Engineering

---

## 2. CRONOLOGIA DA INVESTIGACAO

### 2.1 Report Inicial (Slack)
- **Canal:** #intuit-external
- **Reportado por:** David Ball
- **Data:** 2026-01-20
- **Mensagem:** Erro no Consolidated View Balance Sheet em Keystone Construction e TCO

### 2.2 Analise Inicial
- Acessamos o Consolidated Balance Sheet
- Identificamos valores "Due From" nao eliminados:
  - Due From Apex Tire: $4,800,000
  - Due From RoadReady: $7,100,000
  - Due From Traction Control: $72,050.98
  - Due From Global Tread: $0.00 (OK - eliminado)

### 2.3 Investigacao IC Mappings
- Acessamos Multi-Entity > Overview > Resources > Intercompany Account Mapping
- Encontramos 4 entidades: Traction Control, Apex Tire, Global Tread, RoadReady
- Identificamos 6 pares de mapeamentos IC

---

## 3. PROBLEMAS IDENTIFICADOS

### 3.1 Problema #1: Conta Deletada nos Mapeamentos

**Descricao:**
A conta "Due From Traction Control Outfitters (Parent)" foi DELETADA do sistema, mas 4 mapeamentos IC ainda referenciavam ela.

**Mapeamentos Afetados:**
| # | Par | Campo Afetado |
|---|-----|---------------|
| 1 | Traction ↔ Global Tread | Due from company 1: (deleted) |
| 2 | Traction ↔ RoadReady | Due from company 1: (deleted) |
| 3 | RoadReady ↔ Traction | Due from company 2: (deleted) |
| 4 | Global Tread ↔ Traction | Due from company 2: (deleted) |

**Correcao Aplicada:**
1. Criamos a conta "Due From Traction Control Outfitters (Parent)" no Shared Chart of Accounts
2. Atualizamos os 4 mapeamentos para usar a conta nova

### 3.2 Problema #2: Saldos IC Desbalanceados

**Descricao:**
Os saldos das contas "Due From" e "Due To" entre entidades nao batiam.

**Analise dos Saldos (Balance Sheets Individuais):**

#### Traction Control Outfitters (Parent)
| Conta | Valor |
|-------|-------|
| Due From Global Tread | $704,888.01 |
| Due From Apex Tire | $1,361,421.56 |
| Due From RoadReady | $1,724,345.60 |
| Due To Global Tread | $106,617.22 |
| Due To Apex Tire | $72,050.97 |
| Due To RoadReady | $14,000.00 |

#### Apex Tire & Auto Retail
| Conta | Valor |
|-------|-------|
| Due From Global Tread | $27,387.00 |
| Due From RoadReady | $27,720.49 |
| Due From Traction | $72,050.98 |
| Due To Global Tread | $830,613.29 |
| Due To Traction | $307,769.56 |

#### RoadReady Service Solutions
| Conta | Valor |
|-------|-------|
| Due From Global Tread | -$545.00 |
| Due From Apex Tire | -$575.00 |
| Due To Global Tread | $1,243,866.18 |
| Due To Apex Tire | $18,175.49 |
| Due To RoadReady | $748,054.29 |
| Due To Traction | $985,176.31 |

#### Global Tread Distributors
| Conta | Valor |
|-------|-------|
| Due From Apex Tire | $828,789.29 |
| Due From RoadReady | $1,243,206.18 |
| Due To Global Tread | $397,329.37 |
| Due To Apex Tire | $21,786.01 |
| Due To Traction | $311,991.19 |

**Gap Identificado:**
| Par | Due From (Credor) | Due To (Devedor) | Diferenca |
|-----|-------------------|------------------|-----------|
| Traction→Apex | $1,361,422 | $307,770 | $1,053,652 |
| Traction→RoadReady | $1,724,346 | $985,176 | $739,169 |
| Traction→Global | $704,888 | $311,991 | $392,897 |

---

## 4. CORRECOES APLICADAS

### 4.1 Correcao #1: Shared Chart of Accounts
- **Acao:** Criar conta "Due From Traction Control Outfitters (Parent)"
- **Local:** Consolidated View > Shared Chart of Accounts
- **Configuracao:**
  - Account Number: 1083
  - Account Name: Due From Traction Control Outfitters (Parent)
  - Account Type: Other Current Assets
  - Detail Type: Other Current Assets
  - Share with: All companies
- **Status:** CONCLUIDO

### 4.2 Correcao #2: IC Mappings
- **Acao:** Atualizar 4 mapeamentos com conta deletada
- **Mapeamentos Atualizados:**
  1. Traction ↔ Global: Due from company 1 → conta nova
  2. Traction ↔ RoadReady: Due from company 1 → conta nova
  3. RoadReady ↔ Traction: Due from company 2 → conta nova
  4. Global ↔ Traction: Due from company 2 → conta nova
- **Status:** CONCLUIDO

### 4.3 Correcao #3: Journal Entries de Ajuste (Due To Traction)

#### JE #1 - Apex Tire
| Campo | Valor |
|-------|-------|
| Journal Date | 01/20/2026 |
| Journal No. | ADJ-IC-001 |
| Debit | Opening Balance Equity: $1,053,652.00 |
| Credit | Due To Traction Control: $1,053,652.00 |
| **Status** | CRIADO E VERIFICADO |

#### JE #2 - RoadReady
| Campo | Valor |
|-------|-------|
| Journal Date | 01/20/2026 |
| Journal No. | ADJ-IC-002 |
| Debit | Opening Balance Equity: $739,169.29 |
| Credit | Due To Traction Control: $739,169.29 |
| **Status** | CRIADO E VERIFICADO |

#### JE #3 - Global Tread
| Campo | Valor |
|-------|-------|
| Journal Date | 01/20/2026 |
| Journal No. | ADJ-IC-003 |
| Debit | Opening Balance Equity: $392,896.82 |
| Credit | Due To Traction Control: $392,896.82 |
| **Status** | CRIADO E VERIFICADO |

### 4.4 Correcao #4: Journal Entries de Ajuste (Due To Apex e RoadReady)

#### JE #4 - Traction Control (Due To Apex)
| Campo | Valor |
|-------|-------|
| Journal Date | 01/20/2026 |
| Journal No. | ADJ-IC-004 |
| Debit | Opening Balance Equity: $4,800,000.00 |
| Credit | 2081 Due To Apex Tire (Retail): $4,800,000.00 |
| **Status** | CRIADO E VERIFICADO |

#### JE #5 - Traction Control (Due To RoadReady)
| Campo | Valor |
|-------|-------|
| Journal Date | 01/20/2026 |
| Journal No. | ADJ-IC-005 |
| Debit | Opening Balance Equity: $7,100,000.00 |
| Credit | 2082 Due To RoadReady (Service): $7,100,000.00 |
| **Status** | CRIADO E VERIFICADO |

---

## 5. VERIFICACAO POS-CORRECAO

### 5.1 Balance Sheet Individual - Traction Control (APOS JEs)
| Conta | Antes | Depois | Diferenca |
|-------|-------|--------|-----------|
| Due To Apex Tire | $72,050.97 | $4,872,050.97 | +$4,800,000 ✓ |
| Due To RoadReady | $14,000.00 | $7,114,000.00 | +$7,100,000 ✓ |
| Opening Balance Equity | $0.00 | -$11,900,000.00 | Debitos dos JEs |

**Resultado:** JEs foram salvos corretamente nas entidades individuais.

### 5.2 Consolidated Balance Sheet (APOS TODAS CORRECOES)
| Conta | Antes | Depois | Mudou? |
|-------|-------|--------|--------|
| Due From Apex Tire | $4,800,000 | $4,800,000 | NAO ❌ |
| Due From RoadReady | $7,100,000 | $7,100,000 | NAO ❌ |
| Due From Traction | $72,050.98 | $72,050.98 | NAO ❌ |
| Erro "isn't balancing" | SIM | SIM | NAO ❌ |

**Resultado:** Consolidated View NAO reflete as mudancas das entidades individuais.

---

## 6. TENTATIVAS DE REFRESH

| Tentativa | Acao | Resultado |
|-----------|------|-----------|
| 1 | F5 (refresh pagina) | Sem mudanca |
| 2 | Ctrl+Shift+R (hard refresh) | Sem mudanca |
| 3 | Mudar periodo (01/19 → 01/20) | Sem mudanca |
| 4 | Fechar e reabrir aba | Sem mudanca |
| 5 | Aguardar 5+ minutos | Sem mudanca |

---

## 7. ANALISE TECNICA

### 7.1 Drill-Down da Conta 1081 (Due From Apex)
```
Due From Apex Tire (conta 1081):
- Beginning Balance: $1,959,696.27
- Transacoes YTD: +$461,229.16
- Eliminations: $4,568,385.42
- TOTAL: $5,029,614.58
- Valor mostrado no BS: $4,800,000
```

### 7.2 Comportamento Observado
1. JEs criados nas entidades individuais: FUNCIONAM
2. Balance Sheets individuais: REFLETEM os JEs
3. Consolidated View: NAO REFLETE as mudancas
4. Sistema de eliminacao: PARCIALMENTE funcional (Due To zerados, Due From nao)

### 7.3 Hipoteses
1. **Bug no motor de consolidacao:** O Consolidated View nao esta reprocessando apos mudancas nas entidades
2. **Cache do Consolidated:** Dados em cache nao estao sendo invalidados
3. **Problema de sincronizacao:** Delay entre entidades e consolidated nao explicado
4. **Logica de eliminacao quebrada:** O matching Due From/Due To nao esta funcionando corretamente

---

## 8. CONCLUSAO

### O que foi feito
1. ✅ Identificamos conta deletada nos IC mappings
2. ✅ Criamos a conta faltante no Shared COA
3. ✅ Atualizamos 4 mapeamentos IC
4. ✅ Criamos 5 Journal Entries de ajuste (~$14M total)
5. ✅ Verificamos que JEs foram salvos (BS individuais confirmam)

### O que NAO funcionou
- ❌ Consolidated View NAO reflete as mudancas
- ❌ Erro "isn't balancing" persiste
- ❌ Valores Due From permanecem identicos

### Diagnostico Final
**Este NAO e um problema de dados ou configuracao que pode ser resolvido via JEs ou mapeamentos.**

O Consolidated View do IES nao esta sincronizando/reprocessando as mudancas feitas nas entidades individuais. Isso indica um problema de sistema/backend que requer investigacao de Engineering.

---

## 9. RECOMENDACOES

### Para Intuit Engineering
1. Investigar por que o Consolidated View nao reflete mudancas das entidades
2. Verificar se ha problema no motor de eliminacao IC
3. Checar se ha cache do Consolidated que precisa ser invalidado
4. Verificar logs de sincronizacao entre entidades

### Para TestBox
1. Escalar para Intuit Engineering via ticket
2. Documentar como "known issue" para outros TSAs
3. Aguardar fix de Engineering antes de novas tentativas

### Para David Ball
1. Informar que problema foi investigado
2. Explicar que requer fix de Engineering
3. Fornecer ETA quando Engineering responder

---

## 10. ANEXOS

### 10.1 Screenshots (Localizacao)
- Consolidated Balance Sheet: Slack thread original
- IC Mappings: Investigacao nesta sessao
- Balance Sheets Individuais: Verificacao pos-JEs

### 10.2 Journal Entries Criados
| JE | Entidade | Valor | Status |
|----|----------|-------|--------|
| ADJ-IC-001 | Apex Tire | $1,053,652.00 | Criado |
| ADJ-IC-002 | RoadReady | $739,169.29 | Criado |
| ADJ-IC-003 | Global Tread | $392,896.82 | Criado |
| ADJ-IC-004 | Traction Control | $4,800,000.00 | Criado |
| ADJ-IC-005 | Traction Control | $7,100,000.00 | Criado |
| **TOTAL** | | **$14,085,718.11** | |

### 10.3 Contas Criadas
| Conta | Numero | Tipo | Entidades |
|-------|--------|------|-----------|
| Due From Traction Control Outfitters (Parent) | 1083 | Other Current Assets | Todas |

### 10.4 Mapeamentos Corrigidos
| Par | Campo | Antes | Depois |
|-----|-------|-------|--------|
| Traction↔Global | Due from co.1 | (deleted) | Due From Traction... |
| Traction↔RoadReady | Due from co.1 | (deleted) | Due From Traction... |
| RoadReady↔Traction | Due from co.2 | (deleted) | Due From Traction... |
| Global↔Traction | Due from co.2 | (deleted) | Due From Traction... |

---

## 11. REFERENCIAS

- **Slack Thread:** #intuit-external - David Ball report
- **QBO Help:** "Tips to resolve an unbalanced consolidated balance sheet in Intuit Enterprise Suite"
- **Ambiente:** TCO (quickbooks-testuser-tco-tbxdemo@tbxofficial.com)
- **Sessao Claude:** 2026-01-20 ~21:00-22:15 GMT-3

---

**Documento preparado por:** Thiago Rodrigues (TSA Lead)
**Data:** 2026-01-20
**Versao:** 1.0
