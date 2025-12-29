# PROCESSO MACRO: Validacao de Features QBO Fall Release

## Visao Geral

Este documento descreve o fluxo completo de validacao de features do QBO, desde a selecao do projeto ate a planilha final com evidencias.

## Fluxo de Ponta a Ponta

```
1. SELECAO DO PROJETO
        |
        v
2. LOGIN NO QBO
        |
        v
3. NAVEGACAO PARA FEATURES
        |
        v
4. CAPTURA DE SCREENSHOTS
        |
        v
5. SINCRONIZACAO COM GOOGLE DRIVE
        |
        v
6. APRENDIZADO DE HYPERLINKS
        |
        v
7. GERACAO DE PLANILHA
        |
        v
8. VERIFICACAO FINAL
```

---

## Etapa 1: Selecao do Projeto

**Dados necessarios:**
- Codigo do projeto (ex: TCO, TC1, TC2)
- Usuario de login (ex: quickbooks-testuser-tco-tbxdemo@tbxofficial.com)
- Company a ser usada (ex: Apex Tire)
- Lista de features a validar

**Arquivos envolvidos:**
- `qbo_checker/features.py` - definicao das features por projeto
- `qbo_checker/config.py` - configuracoes de login por projeto

---

## Etapa 2: Login no QBO

**Processo:**
1. Conectar ao Chrome existente via Playwright (CDP)
2. Verificar se ja esta logado
3. Se nao, fazer login com credenciais do projeto
4. Selecionar a company correta

**Codigo:**
```python
from qbo_checker.login import ensure_logged_in
pw, browser, page = ensure_logged_in('TCO')
```

**Arquivos envolvidos:**
- `qbo_checker/login.py` - funcoes de login e conexao

---

## Etapa 3: Navegacao para Features

**Conceitos importantes:**
- **Consolidated View**: Dashboard geral com todas as companies
- **Company View**: Dentro de uma company especifica

Algumas features so aparecem em uma view especifica. Configurar `view: 'consolidated'` ou `view: 'company'` na definicao da feature.

**Codigo:**
```python
from qbo_checker.navigator import navigate_to_feature, go_to_homepage
success, details = navigate_to_feature(page, feature)
```

**Arquivos envolvidos:**
- `qbo_checker/navigator.py` - logica de navegacao
- `qbo_checker/features.py` - rotas e cliques necessarios

---

## Etapa 4: Captura de Screenshots

**Processo:**
1. Aguardar pagina estabilizar (2-3 segundos)
2. Capturar screenshot full-page
3. Anotar com seta/highlight no elemento relevante
4. Salvar em `G:\Meu Drive\TestBox\QBO-Evidence\`

**Padrao de nome:**
```
{DATA}_{PROJETO}_{CATEGORIA}_{FEATURE}.png
Exemplo: 2025-12-03_TCO_Traction_DTM_VendorNotes.png
```

**Codigo:**
```python
from qbo_checker.screenshot import generate_filename, capture_screenshot, annotate_screenshot
filename = generate_filename('TCO', 'Traction', 'DTM_VendorNotes')
filepath = capture_screenshot(page, filename)
annotate_screenshot(filepath, bbox, 'arrow', 'DTM Vendor Notes')
```

**Arquivos envolvidos:**
- `qbo_checker/screenshot.py` - funcoes de captura e anotacao

---

## Etapa 5: Sincronizacao com Google Drive

**IMPORTANTE:** Screenshots salvos em Google Drive levam tempo para sincronizar.

**Verificar sincronizacao:**
1. Aguardar alguns minutos apos captura
2. Verificar se arquivos aparecem em `drive.google.com`
3. Cada arquivo sincronizado recebe um FILE_ID unico

**Problema comum:**
- DriveFS salva arquivos localmente primeiro
- FILE_ID so eh gerado apos upload completo
- Scripts que tentam ler FILE_ID imediatamente podem falhar

---

## Etapa 6: Aprendizado de Hyperlinks

**SOLUCAO PARA HYPERLINKS:**

Como o DriveFS nao expoe facilmente o FILE_ID, a melhor abordagem eh:

1. **Criar planilha oficial manualmente** com hyperlinks corretos
2. **Aprender os hyperlinks** dessa planilha via script
3. **Reutilizar o cache** em novas planilhas

**Codigo:**
```python
from qbo_checker.hyperlink_cache import learn_from_spreadsheet, get_hyperlink

# Aprender de planilha existente
cache = learn_from_spreadsheet('path/to/official_spreadsheet.xlsx')

# Usar hyperlink em nova planilha
url = get_hyperlink('2025-12-03_TCO_Feature.png')
```

**Arquivos envolvidos:**
- `qbo_checker/hyperlink_cache.py` - cache de hyperlinks
- `data/hyperlink_cache.json` - arquivo de cache

---

## Etapa 7: Geracao de Planilha

**Estrutura da planilha:**

| Coluna | Descricao |
|--------|-----------|
| Ref | Codigo unico (TCO-001, TCO-002...) |
| Project | Codigo do projeto |
| Company | Nome da company |
| Feature | Nome da feature |
| Status | Testing, Passed, Failed |
| Intuit_notes | Notas da Intuit |
| Internal_TBX_notes | Notas internas |
| Evidence_file | Nome do screenshot |
| Link | Hyperlink para Google Drive |

**Hyperlinks devem usar formato:**
```
https://drive.google.com/file/d/{FILE_ID}/view?usp=drive_link
```

**Codigo:**
```python
from openpyxl import Workbook
from qbo_checker.hyperlink_cache import get_hyperlink

wb = Workbook()
ws = wb.active

# Para cada feature
link_cell.hyperlink = get_hyperlink(screenshot_filename)
link_cell.value = 'View'
```

---

## Etapa 8: Verificacao Final

**Checklist:**

- [ ] Todas as features tem Evidence_file preenchido
- [ ] Todos os hyperlinks apontam para drive.google.com
- [ ] Hyperlinks abrem corretamente no navegador
- [ ] Screenshots mostram feature correta
- [ ] Anotacoes/setas estao visiveis

**Script de verificacao:**
```python
python check_new_spreadsheet.py
```

---

## Licoes Aprendidas

### 1. DriveFS e FILE_IDs
- NAO tente ler FILE_ID diretamente do DriveFS database
- Tabela `mirror_items` NAO existe
- Tabela `items` tem filename em campo BLOB (proto)
- MELHOR SOLUCAO: Aprender hyperlinks de planilha oficial

### 2. Views do QBO
- Consolidated View vs Company View sao diferentes
- Algumas features so aparecem em uma view
- Sempre configurar `view` na definicao da feature

### 3. Timing
- Aguardar pagina estabilizar antes de screenshot
- Aguardar sincronizacao do Drive antes de gerar hyperlinks

---

## Arquivos do Projeto

```
intuit-boom/
├── qbo_checker/
│   ├── __init__.py
│   ├── login.py          # Login e conexao
│   ├── navigator.py      # Navegacao QBO
│   ├── screenshot.py     # Captura e anotacao
│   ├── features.py       # Definicao de features
│   ├── config.py         # Configuracoes
│   └── hyperlink_cache.py # Cache de hyperlinks
├── data/
│   └── hyperlink_cache.json
├── docs/
│   └── MACRO_FEATURE_VALIDATION.md (este arquivo)
└── scripts/
    └── generate_spreadsheet_with_cache.py
```

---

## Exemplo Completo

```python
# 1. Login
from qbo_checker.login import ensure_logged_in
pw, browser, page = ensure_logged_in('TCO')

# 2. Para cada feature
from qbo_checker.navigator import navigate_to_feature
from qbo_checker.screenshot import capture_screenshot, annotate_screenshot

for feature in features:
    navigate_to_feature(page, feature)
    filepath = capture_screenshot(page, filename)
    annotate_screenshot(filepath, bbox, 'arrow', feature['name'])

# 3. Aguardar sync do Drive (manual)

# 4. Aprender hyperlinks (se primeira vez)
from qbo_checker.hyperlink_cache import learn_from_spreadsheet
learn_from_spreadsheet('path/to/official_spreadsheet.xlsx')

# 5. Gerar planilha
from qbo_checker.hyperlink_cache import get_hyperlink
# ... criar planilha com get_hyperlink()
```

---

Documentacao criada em: 2025-12-03
