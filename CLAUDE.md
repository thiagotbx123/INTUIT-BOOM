# INSTRUCOES PARA CLAUDE - INTUIT-BOOM

## REGRA FUNDAMENTAL
**LEIA LAYERS.md ANTES DE QUALQUER ALTERACAO**

Este projeto usa sistema de camadas protegidas.
Cada camada tem um STATUS:
- LOCKED = NAO ALTERAR sem autorizacao explicita
- OPEN = Pode alterar livremente
- REVIEW = Consultar antes de alterar

## ANTES DE EDITAR QUALQUER ARQUIVO

1. Verificar em LAYERS.md qual camada o arquivo pertence
2. Se camada LOCKED: PARAR e perguntar "Posso alterar [arquivo]?"
3. Se camada OPEN: pode prosseguir
4. Se camada REVIEW: avisar o que vai fazer antes

## COMANDOS DO USUARIO

- "Autorizo alteracao na CAMADA X" = permissao para alterar
- "Tranca a CAMADA X" = marcar como LOCKED em LAYERS.md
- "Abre a CAMADA X" = marcar como OPEN em LAYERS.md
- "Status das camadas" = mostrar resumo de LAYERS.md

## ESTRUTURA DO PROJETO

```
intuit-boom/
├── CLAUDE.md          <- ESTE ARQUIVO (ler sempre)
├── LAYERS.md          <- STATUS DAS CAMADAS (consultar antes de editar)
├── qbo_checker/       <- Modulos principais
├── docs/              <- Documentacao
└── data/              <- Cache e dados
```

## CONTEXTO DO PROJETO

- Validacao de features do QBO Fall Release para Intuit
- Projeto TCO usa company "Apex Tire"
- Screenshots salvos em G:\Meu Drive\TestBox\QBO-Evidence\
- Planilha Excel gerada com hyperlinks do Drive

## CONTAS DE LOGIN

| Codigo | Projeto | Email |
|--------|---------|-------|
| 1 | CONSTRUCTION | quickbooks-test-account@tbxofficial.com |
| 2 | TCO | quickbooks-testuser-tco-tbxdemo@tbxofficial.com |
| 3 | PRODUCT | quickbooks-tbx-product-team-test@tbxofficial.com |
| 4 | TCO DEMO | quickbooks-tco-tbxdemo@tbxofficial.com |

## FLUXO DE VALIDACAO

1. Login (CAMADA 1)
2. Navegacao (CAMADA 2)
3. Screenshot (CAMADA 3)
4. Planilha (CAMADA 4)
5. Orquestracao (CAMADA 5)

---
Ultima atualizacao: 2025-12-06
