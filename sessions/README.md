# Sessoes de Trabalho

Este diretorio armazena o historico de todas as sessoes de trabalho no projeto INTUIT BOOM.

## Estrutura

Cada arquivo segue o padrao: `YYYY-MM-DD_HH-MM.md`

## Como Usar

Ao final de cada sessao de trabalho, execute o comando:
```
/consolidar
```

Isso vai:
1. Verificar alteracoes nas camadas protegidas
2. Analisar toda a conversa da sessao
3. Extrair conhecimentos, decisoes, arquivos criados
4. Criar um arquivo de sessao aqui
5. Atualizar o memory file
6. Atualizar LAYERS.md se necessario
7. Fazer commit e push para GitHub

## Indice de Sessoes

| Data | Resumo | Camadas Alteradas |
|------|--------|-------------------|
| 2025-12-19 | Sistema de aprendizado implementado | Nenhuma |

## Busca de Conhecimento

Para encontrar algo especifico nas sessoes, use:
```bash
grep -r "termo" sessions/
```

Ou pelo Claude:
```
Busque nas sessoes anteriores informacoes sobre [TEMA]
```
