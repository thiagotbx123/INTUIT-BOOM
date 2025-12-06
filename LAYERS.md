# INTUIT-BOOM - Sistema de Camadas Protegidas

## Filosofia
Cada camada tem um DONO. Alteracoes so acontecem com autorizacao explicita.
"Trilhos separados que se unem - cada um cuida do seu trecho."

---

## STATUS DAS CAMADAS

### LEGENDA
- LOCKED   = Funcionando, NAO MEXER sem autorizacao
- OPEN     = Em desenvolvimento, pode alterar
- REVIEW   = Precisa revisao antes de trancar

---

## CAMADA 1: AUTENTICACAO (Owner: Rafael)
**Status: LOCKED**
**Trancado em: 2025-12-06**
**Validado com ruff: SIM (0 erros)**

**Arquivo OFICIAL (protegido):**
- `layer1_login.py` - Modulo standalone multi-projeto

**Arquivos DEPRECADOS (podem ser removidos):**
- `intuit_login_v2_4.py` - Substituido por layer1_login.py
- `qbo_checker/login.py` - Substituido por layer1_login.py
- `qbo_checker/login_v2.py` - Substituido por layer1_login.py
- `qbo_checker/config.py` - Dependencias removidas

**Responsabilidades:**
- Conexao CDP com Chrome na porta 9222
- Login no Intuit (email, senha, TOTP)
- Gerenciamento de sessao
- Suporte multi-projeto (TCO, CONSTRUCTION, PRODUCT, TCO_DEMO)
- Switch entre companies por projeto

**Contrato (o que essa camada ENTREGA):**
```python
from layer1_login import login, connect_qbo, PROJECTS

# Login completo (projeto + company)
pw, browser, page = login("TCO", "apex")
pw, browser, page = login("TCO", "consolidated")
pw, browser, page = login("CONSTRUCTION", "construction")

# Apenas conexao CDP (sem login)
pw, browser, page = connect_qbo()

# Acessar credenciais de projeto
project = PROJECTS["TCO"]
email = project["email"]
password = project["password"]
```

**Projetos disponiveis:**
| Key | Nome | Email |
|-----|------|-------|
| TCO | TCO | quickbooks-testuser-tco-tbxdemo@tbxofficial.com |
| CONSTRUCTION | CONSTRUCTION SALES | quickbooks-test-account@tbxofficial.com |
| PRODUCT | PRODUCT TEAM | quickbooks-tbx-product-team-test@tbxofficial.com |
| TCO_DEMO | TCO DEMO | quickbooks-tco-tbxdemo@tbxofficial.com |

**Companies por projeto:**

TCO:
| Key | Nome | Company ID |
|-----|------|------------|
| apex | Apex Tire & Auto Retail, LLC | 9341455130166501 |
| consolidated | Vista consolidada | 9341455649090852 |
| global | Global Tread Distributors, LLC | 9341455130196737 |
| traction | Traction Control Outfitters, LLC | 9341455130188547 |
| roadready | RoadReady Service Solutions, LLC | 9341455130170608 |

CONSTRUCTION:
| Key | Nome |
|-----|------|
| construction | Keystone Construction (Par.) |
| consolidated | Vista consolidada |

**Regras:**
- [x] LOCKED - NAO ALTERAR sem autorizacao explicita de Rafael
- [x] Para alterar: Rafael deve dizer "Autorizo alteracao na CAMADA 1"
- [x] Validado com ruff check (0 erros)
- [x] Testado: login TCO/apex funcionando

---

## CAMADA 2: NAVEGACAO (Owner: _______)
**Status: OPEN**
**Arquivos:**
- `qbo_checker/navigator.py`
- `qbo_checker/features_rich.json`
- `qbo_checker/features_v4.json`

**Responsabilidades:**
- Trocar entre Company View e Consolidated View
- Navegar para rotas especificas (/app/settings, /app/reportlist, etc.)
- Aguardar carregamento de pagina
- Validar que chegou na tela correta

**Contrato:**
```python
# Input: page + feature dict
# Output: (success: bool, details: dict)
success, details = navigate_to_feature(page, feature)
```

**Regras:**
- [ ] Nao alterar rotas sem testar navegacao
- [ ] Manter features_rich.json como fonte de verdade

---

## CAMADA 3: CAPTURA (Owner: _______)
**Status: OPEN**
**Arquivos:**
- `qbo_checker/screenshot.py`

**Responsabilidades:**
- Gerar nome de arquivo padronizado
- Capturar screenshot full-page ou viewport
- Salvar em EVIDENCE_DIR (Google Drive)
- NAO usar anotacoes (screenshots limpos)

**Contrato:**
```python
# Input: page + filename
# Output: filepath do arquivo salvo
filename = generate_filename(ref, project, company, feature_name)
filepath = capture_screenshot(page, filename)
```

**Regras:**
- [ ] Screenshots sempre limpos (sem setas/marcacoes)
- [ ] Filename sempre inclui Ref unico

---

## CAMADA 4: PLANILHA (Owner: _______)
**Status: OPEN**
**Arquivos:**
- `qbo_checker/spreadsheet.py`
- `qbo_checker/hyperlink_cache.py`
- `data/hyperlink_cache.json`

**Responsabilidades:**
- Gerar planilha Excel com estrutura padrao
- Preencher colunas: Ref, Project, Company, Feature, Status, Notes, Link
- Resolver hyperlinks do Google Drive via cache
- Nao duplicar linhas por Ref

**Contrato:**
```python
# Input: lista de features validadas
# Output: arquivo .xlsx gerado
generate_spreadsheet(features, output_path)
```

**Regras:**
- [ ] Ref e chave primaria - nunca duplicar
- [ ] Hyperlinks devem ser testados antes de entregar

---

## CAMADA 5: ORQUESTRACAO (Owner: _______)
**Status: OPEN**
**Arquivos:**
- `qbo_checker/main.py`
- `cockpit_tco.py`
- `run_validation.py`
- `run_validation_v2.py`

**Responsabilidades:**
- Coordenar fluxo completo: login -> navegacao -> captura -> planilha
- Interface de usuario (menu, selecao de features)
- Tratamento de erros entre camadas
- Logs e feedback visual

**Contrato:**
```python
# Executa validacao completa para um projeto
python run_validation_v2.py --project TCO
```

---

## COMO FUNCIONA A PROTECAO

### Para TRANCAR uma camada:
1. Testar exaustivamente
2. Documentar o contrato (input/output)
3. Rafael marca como LOCKED neste arquivo
4. Claude NAO altera arquivos dessa camada sem autorizacao

### Para ALTERAR uma camada LOCKED:
1. Rafael autoriza explicitamente no chat: "Autorizo alteracao na CAMADA X"
2. Claude faz a alteracao
3. Testar novamente
4. Re-trancar se OK

### Comando para Claude:
"Quero alterar a CAMADA 2" = autoriza alteracao
"NAO mexa na CAMADA 1" = proibido tocar

---

## HISTORICO DE ALTERACOES

| Data | Camada | Acao | Autorizado por |
|------|--------|------|----------------|
| 2025-12-06 | ALL | Criacao do sistema de camadas | Rafael |
| 2025-12-06 | 1 | Criado layer1_login.py standalone multi-projeto | Rafael |
| 2025-12-06 | 1 | Corrigido ruff (10 erros -> 0 erros) | Rafael |
| 2025-12-06 | 1 | Corrigido redirect account-manager | Rafael |
| 2025-12-06 | 1 | LOCKED - Validado com testes TCO/apex | Rafael |

---

## PROXIMOS PASSOS

1. [x] Revisar CAMADA 1 (login) e trancar se OK - FEITO
2. [ ] Definir owners para camadas 2-5
3. [ ] Testar cada camada isoladamente
4. [ ] Documentar contratos finais
5. [ ] Iniciar versionamento com Git (opcional)

---

Documento criado em: 2025-12-06
Projeto: intuit-boom
