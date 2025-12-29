# Design Consolidado: Validacao de Features QBO Fall Release

**Data**: 2025-12-03
**Projeto**: TCO (Traction)
**Company**: Apex Tire

---

## 1. Visao Geral do Fluxo

```
INICIO
   |
   v
LOGIN no QBO (ensure_logged_in)
   |
   v
PARA CADA FEATURE:
   |
   +---> Navegar ate a feature (navigate_to_feature)
   |
   +---> Observar o que aparece na tela
   |
   +---> Capturar screenshot(s) se UI feature
   |
   +---> Gerar NOTES baseado em:
   |        - Conhecimento previo da feature
   |        - Observacao durante navegacao
   |        - Historico de validacoes anteriores
   |        - Tom geral de respostas
   |
   +---> Definir STATUS (YES/NO/PARTIAL)
   |
   v
GERAR PLANILHA com:
   - Features validadas
   - Screenshots com hyperlinks Google Drive
   - Notes geradas automaticamente
   |
   v
ATUALIZAR BASE DE CONHECIMENTO
   |
   v
FIM
```

---

## 2. Status e Seus Significados

| Status | Significado | Acao |
|--------|-------------|------|
| **YES** | Feature funciona 100% como esperado | Screenshot + Notes confirmando |
| **NO** | Feature nao funciona ou nao aparece | Notes explicando o problema |
| **PARTIAL** | TestBox entregou dados/configuracao, mas Intuit nao habilitou a feature flag | Notes explicando situacao |
| **Testing** | Ainda em processo de validacao | Placeholder |

### Importante sobre PARTIAL
- NAO e culpa da TestBox
- TestBox fez sua parte (dados, configuracao)
- Intuit/QuickBooks nao ativou a funcionalidade ainda
- Evidencia mostra que preparacao foi feita

---

## 3. Tipos de Features

### 3.1 Features de UI (Interface)
- **Requerem**: Screenshot(s) + Notes
- **Navegacao**: Menu → Submenu → Pagina
- **Evidencia**: Print mostrando a feature funcionando

### 3.2 Features de Backend/WFS
- **Requerem**: Apenas Notes demonstrando conhecimento
- **Sem screenshot**: Sao melhorias de performance/internas
- **Notes devem**: Mostrar entendimento tecnico da feature

### 3.3 Features Complexas
- **Requerem**: Multiplos screenshots
- **Quantidade**: Definida pela planilha canonica
- **Cada step**: Tem seu proprio screenshot

---

## 4. Estrutura de Notes

### 4.1 Intuit Notes (Coluna F)
**Proposito**: Comunicar para a Intuit/QuickBooks

**Conteudo**:
- O QUE a feature faz (objetivo)
- O QUE aparece na tela (evidencia visual)
- COMO o usuario interage (se aplicavel)

**Exemplo**:
```
Vendor Notes feature allows adding internal notes to vendor records.
Notes are visible in vendor profile under "Additional Info" section.
Supports rich text formatting and attachments.
```

### 4.2 Internal TBX Notes (Coluna G)
**Proposito**: Documentacao interna TestBox

**Conteudo**:
- COMO navegar ate a feature
- PROBLEMAS encontrados durante validacao
- WORKAROUNDS aplicados
- APRENDIZADOS para proximas validacoes

**Exemplo**:
```
Navigation: Expenses > Vendors > [Vendor Name] > Edit
Issue: Notes field only appears after saving vendor once
Workaround: Create vendor first, then edit to add notes
Learning: Check if vendor has transactions before testing
```

---

## 5. Processo de Geracao de Notes

```
1. CONHECIMENTO PREVIO
   - O que sei sobre esta feature?
   - Qual o objetivo do cliente?
   - Por que essa feature importa?
   |
   v
2. NAVEGACAO
   - O que encontrei no caminho?
   - Algum problema de acesso?
   - Menus mudaram?
   |
   v
3. OBSERVACAO
   - O que aparece na tela?
   - Feature esta funcionando?
   - Algo diferente do esperado?
   |
   v
4. HISTORICO ESPECIFICO
   - Como essa feature foi validada antes?
   - Teve problemas anteriores?
   - Qual foi o status anterior?
   |
   v
5. TOM GERAL
   - Como outras notes foram escritas?
   - Qual o padrao de comunicacao?
   - Nivel de detalhe esperado?
   |
   v
6. RESPOSTA FINAL
   - Combinar tudo acima
   - Gerar Intuit Notes
   - Gerar Internal Notes
   - Definir Status
```

---

## 6. Estrutura de Dados da Feature

### features.json - Estrutura Rica

```json
{
  "features": [
    {
      "ref": "TCO-001",
      "name": "Dimensions / Dimension Assignment",
      "category": "Dimensions",
      "view": "company",

      "objective": "Allow assigning custom dimensions to transactions for advanced reporting",
      "expected_behavior": "Dimension dropdown appears in transaction forms, values can be selected",

      "navigation": {
        "route": "/app/dimensions",
        "clicks": ["Settings gear", "Custom Fields", "Dimensions tab"],
        "wait_for": "Dimension list table"
      },

      "evidence": {
        "type": "ui",
        "screenshot_count": 1,
        "highlight": {
          "type": "arrow",
          "target": "text:Dimensions"
        }
      },

      "notes_template": {
        "intuit": "Dimensions feature enables {observed_behavior}. Screen shows {visual_elements}.",
        "internal": "Navigation: {navigation_path}. {issues_if_any}. {learnings}."
      },

      "validation_history": [
        {
          "date": "2025-12-03",
          "status": "YES",
          "notes": "Working as expected"
        }
      ]
    }
  ]
}
```

---

## 7. Arquivos do Projeto e Responsabilidades

```
intuit-boom/
├── qbo_checker/
│   ├── login.py           # Conexao CDP e login QBO
│   ├── navigator.py       # Navegacao entre views e features
│   ├── screenshot.py      # Captura e anotacao de prints
│   ├── features.py        # Carrega features.json
│   ├── features.json      # Definicao rica das features (FONTE)
│   ├── spreadsheet.py     # Geracao da planilha (FONTE DE VERDADE)
│   ├── hyperlink_cache.py # Cache de links do Google Drive
│   ├── notes_generator.py # [NOVO] Geracao automatica de notes
│   └── knowledge.py       # [NOVO] Base de conhecimento acumulado
│
├── data/
│   ├── hyperlink_cache.json     # Cache filename -> Drive URL
│   ├── knowledge_base.json      # [NOVO] Conhecimento acumulado
│   └── validation_history.json  # [NOVO] Historico de validacoes
│
├── docs/
│   ├── MACRO_FEATURE_VALIDATION.md  # Processo macro
│   └── plans/
│       └── 2025-12-03-feature-validation-design.md  # Este documento
│
└── scripts/
    └── generate_spreadsheet_with_cache.py  # Script de geracao
```

---

## 8. Planilha Canonica como Referencia

A planilha `fall_release_control.xlsx` serve como:

1. **Referencia de Estrutura**
   - Quais colunas existem
   - Ordem das features
   - Formato dos REFs

2. **Maximo de Screenshots por Feature**
   - Analisar Evidence_file para saber quantos prints cada feature precisa
   - Features simples: 1 print
   - Features complexas: multiplos prints (ex: Project Phases tem 5)

3. **Tom das Notes**
   - Analisar notes existentes para entender o padrao
   - Nao copiar literalmente, mas seguir o estilo

---

## 9. Codigo como Fonte de Verdade

### Principio
O CODIGO (spreadsheet.py, features.json) e a fonte de verdade, NAO a planilha Excel.

### Implicacoes
- Planilha Excel e OUTPUT, nao INPUT
- Mudancas devem ser feitas no codigo
- Planilha e gerada a partir do codigo
- Planilha canonica e apenas REFERENCIA para aprendizado

### Fluxo de Atualizacao
```
Aprendizado (conversas)
    → Codigo (features.json, spreadsheet.py)
        → Planilha gerada (fall_release_control_TCO_*.xlsx)
```

---

## 10. Proximos Passos

1. **Atualizar features.json**
   - Adicionar objective para cada feature
   - Adicionar expected_behavior
   - Adicionar notes_template
   - Definir screenshot_count baseado na planilha canonica

2. **Criar notes_generator.py**
   - Implementar logica de geracao de notes
   - Usar templates + observacao + historico

3. **Atualizar spreadsheet.py**
   - Integrar notes_generator
   - Usar hyperlink_cache para links
   - Gerar planilha completa automaticamente

4. **Testar Fluxo Completo**
   - Login → Navegacao → Screenshot → Notes → Planilha
   - Verificar todos os links funcionam
   - Validar notes geradas

---

## 11. Conhecimento Acumulado por Categoria

### Dimensions
- Permite criar campos customizados para transacoes
- Usado para reporting avancado
- Navegacao: Settings > Custom Fields > Dimensions

### DTM (Digital Transaction Management)
- Multiple Shipping Addresses: Permite multiplos enderecos por cliente
- Vendor CC/BCC: Copiar emails em comunicacoes com vendors
- Vendor Notes: Notas internas para vendors

### BI (Business Intelligence)
- KPIs Library: Biblioteca de indicadores pre-definidos
- Custom Formula: Criar KPIs customizados
- Dashboards: Paineis visuais de metricas
- Advanced Reporting: Relatorios complexos
- Management Reports: Relatorios gerenciais

### Construction
- Project Phases: Fases de projeto (5 steps)
- Cost Groups: Agrupamento de custos
- Budgets V3: Nova versao de orcamentos
- AIA Billing: Faturamento padrao AIA
- Certified Payroll: Folha certificada
- Project Estimate: Estimativas de projeto

### Bill Pay
- Approval Workflow: Fluxo de aprovacao
- Instant Payments: Pagamentos instantaneos

### AI Agents
- Accounting Agent: Assistente contabil
- Payment Agent: Assistente de pagamentos
- Customer Agent: Assistente de clientes
- Payroll Agent: Assistente de folha
- Project Agent: Assistente de projetos
- Finance Agent: Assistente financeiro
- Solutions Agent: Assistente de solucoes
- Sales Tax Agent: Assistente de impostos

---

*Documento criado em: 2025-12-03*
*Baseado em brainstorming detalhado com usuario*
