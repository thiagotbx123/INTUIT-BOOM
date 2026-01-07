# UNIVERSAL VALIDATION FRAMEWORK
## QBO Feature Validation - Aplicavel a TODOS os Ambientes
### Versao 1.0 - 2025-12-29

---

## PROPOSITO

Este documento define regras UNIVERSAIS de validacao que se aplicam a:
- TCO (Apex Tire)
- Construction (Keystone)
- Product
- TCO Demo
- Qualquer ambiente futuro

**LEITURA OBRIGATORIA ANTES DE QUALQUER VALIDACAO**

---

## PARTE 1: PRINCIPIOS FUNDAMENTAIS

### PRINCIPIO 1: Screenshot DEVE provar a feature

**NAO ACEITAR:**
- Homepage/Dashboard generico para provar feature especifica
- Pagina com loading spinner
- Pagina 404
- Tela de login
- Pagina que "menciona" a feature mas nao a mostra funcionando

**ACEITAR:**
- UI especifica da feature visivel e funcional
- Dados carregados (nao loading)
- Elementos interativos visiveis
- Contexto correto no header (empresa certa)

**PERGUNTA DE VALIDACAO:**
> "Se eu mostrar este screenshot para alguem que nao conhece QBO, essa pessoa conseguiria entender que a feature existe e funciona?"

---

### PRINCIPIO 2: Contexto correto e OBRIGATORIO

**TIPOS DE CONTEXTO:**

| Contexto | Quando usar | Como identificar no screenshot |
|----------|-------------|-------------------------------|
| EMPRESA INDIVIDUAL | Features single-entity | Nome da empresa no header (ex: "Apex Tire") |
| CONSOLIDATED VIEW | Features multi-entity | "Consolidated" ou "Vista Consolidada" no header |
| FRESH TENANT | Demos de migration | Tenant sem dados existentes |
| TENANT ESPECIFICO | Features regionais | CA=California, Canada=Sistema diferente |

**ERRO COMUM:**
Capturar feature multi-entity em empresa individual. O screenshot mostra dados, mas NAO prova que e multi-entity.

**REGRA:**
Antes de capturar, verificar: "Esta feature precisa de contexto especial?"

---

### PRINCIPIO 3: Ambiente determina disponibilidade

**REALIDADE:** Nem toda feature existe em todo ambiente.

| Situacao | Status correto | Acao |
|----------|----------------|------|
| Feature existe e funciona | PASS | Capturar screenshot |
| Feature existe com limitacoes | PARTIAL | Capturar + documentar limitacao |
| Feature nao habilitada no tenant | NOT_AVAILABLE | Documentar + justificar |
| Feature e documentacao, nao UI | N/A | Nao capturar, referenciar docs |
| Feature requer ambiente especifico | N/A (para este ambiente) | Documentar qual ambiente precisa |

**ERRO COMUM:**
Marcar N/A porque a captura falhou. N/A e para features que NAO TEM UI, nao para falhas.

---

### PRINCIPIO 4: 404 = Investigar, nao aceitar

**QUANDO URL RETORNA 404:**

1. **Verificar URL** - Esta correta? Typo?
2. **Tentar navegacao alternativa** - Menu vs URL direta
3. **Pesquisar na web** - Qual a navegacao correta?
4. **Verificar feature no ambiente** - Esta habilitada?
5. **Se nao existe:** Marcar NOT_AVAILABLE com justificativa

**NUNCA:**
- Aceitar screenshot de 404 como valido
- Marcar PASS com screenshot de erro
- Ignorar e seguir em frente

---

### PRINCIPIO 5: Organizar por contexto

**PROBLEMA:**
Trocar de empresa/contexto repetidamente = lento + erro-prone

**SOLUCAO:**
Agrupar capturas por contexto:

```
FASE 1: Empresa Individual (Apex/Keystone)
  - Capturar TODAS as features deste contexto
  - NAO trocar de empresa durante esta fase

FASE 2: Consolidated View (se aplicavel)
  - Trocar UMA VEZ para consolidated
  - Capturar TODAS as features multi-entity

FASE 3: Decisoes
  - Marcar N/A para features documentacao
  - Marcar NOT_AVAILABLE para features nao disponiveis
```

---

## PARTE 2: DIFERENCAS ENTRE AMBIENTES

### TCO (Apex Tire & Auto Retail)

**Caracteristicas:**
- Multi-entity completo (5 empresas)
- Consolidated View disponivel
- AI features habilitadas (sparkles)
- Payroll US configurado
- Workflow Automation funcional

**Features especificas:**
- WR-015 Multi-Entity Reports: DISPONIVEL
- WR-016 Dimension Assignment AI: DISPONIVEL (sparkles aparecem)
- WR-018/020 Workflow: DISPONIVEL

**Empresas disponiveis:**
- Apex Tire & Auto Retail, LLC (principal)
- Global Tread Distributors, LLC
- Traction Control Outfitters, LLC
- RoadReady Service Solutions, LLC
- Vista Consolidada

---

### CONSTRUCTION (Keystone Construction)

**Caracteristicas:**
- Foco em Construction industry
- Projects com budgets
- Certified Payroll Report (WH-347)
- Pode NAO ter todas features IES

**Features especificas:**
- WR-024 Certified Payroll: DISPONIVEL (Construction-specific)
- WR-018/020 Workflow: pode estar NOT_AVAILABLE
- WR-016 Dimension Assignment: SEM sparkles AI (menos dados)

**Diferenca critica vs TCO:**
- Workflow Automation URL pode retornar 404
- AI suggestions menos frequentes (menos dados)
- Algumas URLs funcionam em TCO mas nao em Construction

---

### AMBIENTES FUTUROS (Framework)

**Antes de validar um novo ambiente:**

1. **Identificar tipo de ambiente**
   - Multi-entity ou single-entity?
   - Industry vertical? (Construction, Nonprofit, Manufacturing)
   - Regiao? (US, Canada, UK)

2. **Verificar features habilitadas**
   - Testar URLs principais
   - Verificar menu navigation
   - Documentar o que existe vs nao existe

3. **Criar mapa de features**
   - Quais features do release existem neste ambiente?
   - Quais estao NOT_AVAILABLE?
   - Quais precisam de contexto especial?

4. **Documentar diferencas**
   - Comparar com TCO/Construction
   - Anotar URLs que funcionam/nao funcionam
   - Mapear navegacao alternativa

---

## PARTE 3: CHECKLIST PRE-CAPTURA (UNIVERSAL)

**ANTES de capturar QUALQUER feature em QUALQUER ambiente:**

### [ ] 1. Contexto correto?
- Empresa no header e a correta para esta feature?
- Se multi-entity: estou em Consolidated View?
- Se regional: estou no tenant correto?

### [ ] 2. Feature existe neste ambiente?
- URL funciona ou retorna 404?
- Menu path existe?
- Se nao existe: marcar NOT_AVAILABLE, nao tentar capturar

### [ ] 3. Sei o que capturar?
- Qual UI especifica prova esta feature?
- NAO e homepage generica?
- NAO e pagina que apenas menciona a feature?

### [ ] 4. Conteudo carregou?
- Sem loading spinner?
- Dados visiveis?
- Tempo de espera suficiente (30-60s)?

### [ ] 5. Screenshot vai provar?
- Alguem olhando este screenshot entenderia a feature?
- Elements visiveis sao os corretos?
- Header mostra contexto correto?

---

## PARTE 4: ANTI-PATTERNS COM EXEMPLOS REAIS

### ANTI-PATTERN 1: Screenshot Generico

**Exemplo real (WR-006 Customer Agent):**
```
ERRADO: Screenshot do Dashboard Homepage
  - Mostra "Good morning TestBox!"
  - Mostra widgets de cash flow, P&L
  - NAO mostra nada sobre Customer Agent

CERTO: Screenshot de Customers > Leads tab
  - Mostra opcao de import from Gmail/Outlook
  - Mostra lista de leads
  - PROVA que Customer Agent existe
```

**Porque acontece:**
- Preguica de navegar ate a feature real
- Assumir que homepage "representa" tudo

**Como evitar:**
- Sempre perguntar: "Este screenshot prova ESTA feature especifica?"

---

### ANTI-PATTERN 2: Contexto Errado

**Exemplo real (WR-015 Multi-Entity Reports):**
```
ERRADO: Screenshot de Reports em "Apex Tire & Auto Retail, LLC"
  - Mostra reports normais
  - Header mostra empresa individual
  - NAO prova que e multi-entity

CERTO: Screenshot de Reports em "Vista Consolidada"
  - Header mostra "Consolidated"
  - Reports mostram dados de multiplas empresas
  - PROVA capacidade multi-entity
```

**Porque acontece:**
- Esquecer de trocar para Consolidated View
- Nao entender a diferenca

**Como evitar:**
- Antes de features multi-entity: SEMPRE verificar header
- Se nao diz "Consolidated": trocar primeiro

---

### ANTI-PATTERN 3: Aceitar 404

**Exemplo real (WR-012 Calculated Fields, WR-026 Payroll Hub):**
```
ERRADO: Screenshot de pagina 404
  - "We're sorry, we can't find the page you requested."
  - Tamanho tipico: ~139KB
  - NAO prova nada

CERTO: Investigar e encontrar navegacao correta
  - Tentar via menu
  - Pesquisar documentacao
  - Se nao existe: marcar NOT_AVAILABLE
```

**Porque acontece:**
- URL direta nao funciona em todos ambientes
- Assumir que 404 = feature nao existe

**Como evitar:**
- 404 = investigar, NUNCA aceitar
- Tentar navegacao alternativa
- Pesquisar antes de desistir

---

### ANTI-PATTERN 4: N/A para Falhas

**Exemplo real (WR-023 Feature Compatibility):**
```
ERRADO: Capturar loading spinner e marcar N/A
  - "Nao consegui capturar, vou marcar N/A"
  - N/A usado como escape para falhas

CERTO: Entender que Feature Compatibility e DOCUMENTACAO
  - Nao existe UI para esta feature
  - E informacao sobre compatibilidade, nao tela
  - N/A e o status correto PORQUE e documentacao
```

**Quando N/A e correto:**
- Feature e documentacao (nao tem UI)
- Feature requer ambiente que nao temos acesso

**Quando N/A e ERRADO:**
- Captura falhou
- Deu 404
- Loading spinner
- Nao consegui encontrar

---

### ANTI-PATTERN 5: Ambiente Errado

**Exemplo real (WR-029 Enhanced Amendments CA):**
```
ERRADO: Capturar Payroll generico em TCO
  - TCO e ambiente US generico
  - Feature e CA-specific (California)
  - Screenshot nao prova nada

CERTO: Reconhecer que TCO nao e ambiente correto
  - Marcar N/A para TCO
  - Documentar: "Requer California-specific tenant"
  - Se tiver acesso a CA tenant: validar la
```

**Porque acontece:**
- Nao ler requisitos da feature
- Assumir que todo ambiente tem toda feature

**Como evitar:**
- Verificar requisitos de ambiente ANTES de capturar
- Se feature e regional: confirmar que estou no tenant correto

---

## PARTE 5: FLUXO DE VALIDACAO UNIVERSAL

```
INICIO
  |
  v
[1. Ler requisitos da feature]
  |
  v
[2. Feature e UI ou documentacao?]
  |
  +---> Documentacao ---> Marcar N/A, referenciar docs
  |
  v
[3. Feature requer ambiente especifico?]
  |
  +---> Sim, nao tenho acesso ---> Marcar N/A, documentar requisito
  |
  v
[4. Feature requer contexto especial?]
  |
  +---> Multi-entity ---> Trocar para Consolidated View
  |
  v
[5. Navegar para feature]
  |
  +---> 404 ---> Investigar navegacao alternativa
  |              |
  |              +---> Funciona? ---> Continuar
  |              |
  |              +---> Nao funciona ---> Marcar NOT_AVAILABLE
  |
  v
[6. Aguardar carregamento (30-60s)]
  |
  v
[7. Conteudo carregou?]
  |
  +---> Loading spinner ---> Esperar mais / Investigar
  |
  v
[8. Screenshot prova a feature?]
  |
  +---> Nao ---> Navegar para UI correta
  |
  v
[9. Capturar screenshot]
  |
  v
[10. Verificar qualidade]
  |
  +---> < 100KB ---> Investigar
  |
  v
[11. Documentar evidence notes]
  |
  v
FIM
```

---

## PARTE 6: TEMPLATE DE EVIDENCE NOTES

```
FEATURE: [WR-XXX] - [Nome]
AMBIENTE: [TCO/Construction/etc]
EMPRESA: [Nome da empresa no header]
CONTEXTO: [Individual/Consolidated/Fresh/Regional]

URL_NAVEGADA: [URL ou menu path]
TEMPO_ESPERA: [Xs]
ARQUIVO: [nome.png]
TAMANHO: [XXX KB]

O QUE FOI CAPTURADO:
- [Descrever elementos visiveis]
- [Que provam a feature]

STATUS: [PASS/PARTIAL/NOT_AVAILABLE/N/A]
JUSTIFICATIVA: [Por que este status]

PROBLEMAS ENCONTRADOS: [Se houver]
NAVEGACAO ALTERNATIVA: [Se usada]
```

---

## PARTE 7: MAPA DE FEATURES POR CONTEXTO

### Features EMPRESA INDIVIDUAL (maioria)
WR-001 a WR-014, WR-016 a WR-020, WR-021, WR-022, WR-024, WR-025, WR-027, WR-028

### Features CONSOLIDATED VIEW
- WR-015 Multi-Entity Reports
- WR-026 Multi-Entity Payroll Hub

### Features DOCUMENTATION (N/A)
- WR-023 Feature Compatibility

### Features REGIONAL/ESPECIFICAS
- WR-029 Enhanced Amendments: CA-specific tenant
- Features Canada: Canada tenant (sistema diferente)

### Features FRESH TENANT
- WR-021 Desktop Migration (demo completo)
- WR-022 DFY Migration (demo completo)

---

## PARTE 8: COMANDOS RAPIDOS

### Antes de qualquer sessao de validacao:
```python
# Ler este documento
# Ler FEATURE_VALIDATION_CANON.json
# Verificar qual ambiente vou validar
# Listar features deste ambiente
```

### Durante a captura:
```python
# Verificar header (empresa correta?)
# Verificar URL (funcionou?)
# Verificar conteudo (carregou?)
# Verificar tamanho (>100KB?)
```

### Apos a captura:
```python
# Screenshot prova a feature?
# Evidence notes documentadas?
# Status correto?
```

---

*Framework Universal de Validacao v1.0*
*Aplicavel a: TCO, Construction, Product, TCO Demo, e ambientes futuros*
*Criado: 2025-12-29*
*Claude Code + Feedback Usuario*
