# INTUIT BOOM - Memory File

## REGRAS OBRIGATORIAS DE VALIDACAO (NUNCA IGNORAR)

### Regra 1: Escopo Completo
- ANTES de validar ambiente, listar TODAS as features aplicaveis
- IES = TCO + Construction + Product (mesmas features)
- NAO assumir que menos features = suficiente

### Regra 2: Paridade de Qualidade
- Evidence_notes DETALHADAS (o que esta visivel, nao apenas se carregou)
- Data validation quando aplicavel

### Regra 3: Validacao Pos-Captura
- Screenshot > 100KB = provavelmente valido
- Screenshot ~140KB = provavel pagina de erro 404
- Se erro, tentar navegacao alternativa (menu vs URL)

### Regra 4: Status Granular
- PASS / PARTIAL / NOT_AVAILABLE / FAIL

### Regra 5: Comparacao Entre Ambientes
- Comparar screenshots lado a lado
- Documentar nas notes o que difere

---

## Projeto
- **Nome**: INTUIT BOOM
- **Cliente**: Intuit (QuickBooks Online)
- **Tipo**: QBO Demo Manager — validacao, sweep e manutencao de ambientes demo
- **Dono**: Thiago

## Ambientes Configurados (9 contas)

| Shortcode | Dataset | Tipo | Entidades |
|-----------|---------|------|-----------|
| tco | tire_shop | Multi (5) | Apex Tire + 3 children + Consolidated |
| construction | construction | Multi (8) | Keystone Par + 7 children |
| mid-market | construction | Single | Keystone Construction |
| nv2 | non_profit | Multi (3) | Parent + Rise + Response |
| nv3 | manufacturing | Multi (3) | TBD |
| summit | professional_services | Multi | TBD |
| qsp | construction | Multi | Events + Sales (2FA BLOCKED) |
| construction-clone | construction | Multi | Clone dataset |
| keystone-se | construction | Single | Seller environment |

## CIDs Principais
- Keystone Par: 9341454156620895
- Keystone Terra: 9341454156620204
- Keystone BlueCraft: 9341453873733
- Mid Market: 9341452713218633
- Apex Tire (TCO): 9341455130166501
- Dataset Construction: 2ed5d245-0578-43aa-842b-6e1e28367149

## Sweep System (v5.5 Release Coverage)
- **Dashboard**: `dashboard/app.py` (FastAPI)
- **Checks**: `dashboard/sweep_checks.py` (12 Deep + 46 Surface + 19 Conditional + 9 CS + 7 Cross)
- **Profiles**: full_sweep, quick_sweep, surface_only
- **MCP**: Playwright (browser), QuickBooks API, Slack, Google Drive

## Decisoes Arquiteturais
| Decisao | Motivo |
|---------|--------|
| Sistema de camadas LOCKED/OPEN/REVIEW | Proteger codigo estavel |
| Credentials inline no SWEEP_ORDER.md | Isolamento (nao ref externa) |
| JS extractors para token mgmt | Comprimir 90KB snapshots → 2-5KB JSON |
| Sub-checks analiticos (nao thresholds) | Flexibilidade por setor |
| Net Income MUST be positive (todas entities) | Regra financeira core |

## Blockers Conhecidos
- QSP: 2FA phone blocked (SMS nao entrega)
- MFA secondary phone removed Mar 30, 2026
- Product Events: $0 revenue em ALL 3 entities

## Riscos Ativos
| Risco | Impacto | Linear |
|-------|---------|--------|
| Manufacturing visibility gap | P2 | - |
| Demo load time >20s | P2 | KLA-2337 |

---

## Historico
- Sessoes detalhadas: `.claude/memory_backup_2026-03-23.md`
- Sweep reports: `knowledge-base/sweep-learnings/`
- Strategic Cortex: `knowledge-base/strategic-cortex/OUTPUT_A_*.md`

Ultima atualizacao: 2026-03-23
