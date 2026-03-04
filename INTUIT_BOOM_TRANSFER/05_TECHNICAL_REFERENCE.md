# INTUIT-BOOM - Referencia Tecnica

---

## SISTEMA DE CAMADAS (LAYERS)

| Camada | Nome | Status | Arquivo Principal | Owner |
|--------|------|--------|-------------------|-------|
| 1 | Autenticacao | **LOCKED** | `layer1_login.py` | Rafael |
| 2 | Navegacao | OPEN | `qbo_checker/navigator.py` | - |
| 3 | Captura | OPEN | `qbo_checker/screenshot.py` | - |
| 4 | Planilha | OPEN | `qbo_checker/spreadsheet.py` | - |
| 5 | Orquestracao | OPEN | `run_validation_v2.py` | - |

### Camada 1 - Login (LOCKED)
```python
from layer1_login import login, connect_qbo, PROJECTS

# Login completo (projeto + company)
pw, browser, page = login("TCO", "apex")
pw, browser, page = login("TCO", "consolidated")
pw, browser, page = login("CONSTRUCTION", "construction")

# Apenas conexao CDP (sem login)
pw, browser, page = connect_qbo()

# Acessar credenciais
project = PROJECTS["TCO"]
email = project["email"]
```

### Projetos Disponiveis
| Key | Email |
|-----|-------|
| TCO | quickbooks-testuser-tco-tbxdemo@tbxofficial.com |
| CONSTRUCTION | quickbooks-test-account@tbxofficial.com |
| PRODUCT | quickbooks-tbx-product-team-test@tbxofficial.com |
| TCO_DEMO | quickbooks-tco-tbxdemo@tbxofficial.com |

### Tecnologia
- Playwright CDP na porta 9222
- Login Intuit (email, senha, TOTP)
- Chrome ja aberto com `--remote-debugging-port=9222`

---

## FEATURE VALIDATOR v2.0

### Metodo Padronizado
```
1. LOGIN (layer1_login.py + TOTP)
2. NAVEGACAO (URL + timeout 60s)
3. ESPERA (30-45s - QBO e lento!)
4. CAPTURA (screenshot + timeout 60s)
5. ANALISE (flags + tamanho + headers)
6. FALLBACK (se erro, URL alternativa)
7. EVIDENCE NOTES (template tecnico)
8. DECISAO (PASS/REVIEW/NOT_AVAILABLE/N/A)
```

### Sistema de FLAGS
```python
LOGIN_PAGE        # Capturou pagina de login
LOADING_DETECTED  # Spinner visivel
ERROR_CONTENT     # Conteudo de erro
VERY_SMALL_FILE   # < 50KB
SMALL_FILE        # 50-100KB
ERROR_PAGE_404    # Pagina 404 confirmada
NOT_AVAILABLE     # Feature nao disponivel
```

### Thresholds de Qualidade (KB)
| Quality | Size |
|---------|------|
| EXCELLENT | >= 250 |
| GOOD | >= 150 |
| ACCEPTABLE | >= 100 |
| WEAK | >= 50 |
| INVALID | < 50 |
| ERROR_PAGE | ~139 |

---

## AMBIENTES QBO

### TCO Multi-Entity
| Company | Company ID | Tipo |
|---------|------------|------|
| Apex Tire & Auto Retail | 9341455130166501 | Parent |
| Vista Consolidada | 9341455649090852 | Consolidated |
| Global Tread Distributors | 9341455130196737 | Child |
| Traction Control Outfitters | 9341455130188547 | Child |
| RoadReady Service Solutions | 9341455130170608 | Child |

### Keystone Construction
| Company | Company ID | Tipo |
|---------|------------|------|
| Keystone Construction (Par.) | 9341454156620895 | Parent |
| Keystone Terra (Ch.) | 9341454156620204 | Child |
| BlueCraft | (Realm 9341454842756096) | Child |
| + Canopy, Ecocraft, Ironcraft, Stonecraft, Volt | - | Children |

### Usuarios Intuit com Acesso (Keystone)
| Nome | Email | Role |
|------|-------|------|
| QB Demoteam | qbdemoteam@intuit.com | Primary Admin |
| Akshit Agarwal | akshit_agarwal@intuit.com | Company admin |
| Garrett Lusk | garrett_lusk@intuit.com | Company admin |
| Austin Alexander | austin_alexander@intuit.com | Bill approver |

---

## LINEAR API

### Configuracao
- **Endpoint:** `https://api.linear.app/graphql`
- **Key:** Ver `C:\Users\adm_r\Tools\LINEAR_AUTO\.env`

### Teams
| Team | Key | ID |
|------|-----|-----|
| Platypus | PLA | fd21180c-8619-4014-98c6-ac9eb8d47975 |
| Raccoons | RAC | 5a021b9f-bb1a-49fa-ad3b-83422c46c357 |
| Koala | KLA | fea84e7b-54e5-4b89-bf90-9967bdd2b90b |

### Scripts
- `create_linear_ticket.py` - Criar tickets
- `add_linear_comment.py` - Adicionar comentarios

---

## GOOGLE DRIVE API

### Configuracao
- **OAuth Project:** 486245165530
- **Token:** `C:\Users\adm_r\token_drive.pickle`
- **Pasta Evidence:** `08. Intuit/06. Winter Release/`

### Estrutura no Drive
```
08. Intuit/06. Winter Release/
├── WINTER_RELEASE_VALIDATION_WITH_LINKS.xlsx
├── TCO/ (29 screenshots)
├── Construction/ (4+ screenshots)
└── CONSTRUCTION_WINTER_RELEASE_VALIDATION.xlsx
```

---

## SQLITE DATABASE

### Database Principal
- **Local:** `Downloads/qbo_database_TCO_Construction.db`
- **Query exemplo:**
```sql
SELECT * FROM classifications
WHERE dataset_id = 'fab72c98-c38d-4892-a2db-5e5269571082'
-- Retorna 51 classifications (8 de 9 facets)
```

---

## QB OAUTH MANAGER

### Companies Configuradas
```json
{
  "Construction": {"realmId": "9341454796804202", "type": "parent"},
  "Terra": {"realmId": "9341454842738078", "type": "child"},
  "BlueCraft": {"realmId": "9341454842756096", "type": "child"}
}
```
- **Local:** `C:\Users\adm_r\Integrations\qb-oauth-manager\`

---

## SCRIPTS CRITICOS

### Data Extraction (WAR ROOM)
| Script | Funcao |
|--------|--------|
| `extract_bank_transactions.py` | 5,087 bank txns |
| `extract_bills.py` | A/P consolidation |
| `extract_invoices.py` | A/R consolidation |
| `validate_fk_dependencies.py` | FK validation |
| `generate_ingestion_csvs.py` | CSV generation |

### Time Entries Pipeline
| Script | Funcao |
|--------|--------|
| `fix_time_entries_services.py` | Service ID correction |
| `fix_time_entries_projects.py` | Project ID/date fixes |
| `fix_time_entries_v3_smart.py` | Final corrections |

### Linear Integration
| Script | Funcao |
|--------|--------|
| `linear_update.py` | Status updates |
| `linear_update_all.py` | Batch updates |
| `get_full_ticket_table.py` | Status tracking |
| `compare_employees.py` | Dataset validation |

### Feature Validation
| Script | Funcao |
|--------|--------|
| `layer1_login.py` | Login QBO (LOCKED) |
| `qbo_checker/feature_validator.py` | Validator v2.0 |
| `run_validation_v2.py` | Orquestracao |

---

## PYTHON ENVIRONMENT

### Dependencias Principais
- playwright (CDP browser automation)
- openpyxl (Excel generation)
- requests (API calls)
- google-api-python-client (Drive API)
- google-auth-oauthlib (OAuth2)
- pyotp (TOTP 2FA)
- sqlite3 (built-in)

---

*Compilado de LAYERS.md, memory.md, sessions/, scripts/*
