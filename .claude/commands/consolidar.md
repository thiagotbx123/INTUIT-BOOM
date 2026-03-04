Voce DEVE executar uma consolidacao completa do aprendizado desta sessao. Siga TODOS os passos abaixo:

## PASSO 1: Verificar Camadas

ANTES de qualquer coisa, verifique LAYERS.md:
- Alguma camada foi alterada nesta sessao?
- Se sim, foi com autorizacao?
- Atualizar status da camada se necessario

## PASSO 2: Analise da Sessao

Revise TODA a conversa desta sessao e extraia:

1. **Decisoes tomadas** - Qualquer escolha de arquitetura, tecnologia, abordagem
2. **Novos conhecimentos** - Informacoes sobre QBO, Intuit, TestBox que aprendemos
3. **Arquivos criados/modificados** - Lista completa com caminhos
4. **Arquivos anexos recebidos** - Se o usuario anexou prints, docs - extraia o conteudo relevante
5. **Problemas resolvidos** - Bugs, erros, troubleshooting
6. **Insights importantes** - Qualquer aprendizado que deve persistir

## PASSO 3: Criar Arquivo de Sessao

Crie um arquivo em `sessions/YYYY-MM-DD_HH-MM.md` com:

```markdown
# Sessao: [Data e Hora]

## Resumo
[2-3 frases do que foi feito]

## Camadas Alteradas
- [CAMADA X]: [O que foi feito] (Autorizado: Sim/Nao)

## Decisoes
- [lista de decisoes]

## Conhecimentos Adquiridos
### QBO/Intuit
- [novos conhecimentos sobre QBO]

### TestBox
- [novos conhecimentos sobre TestBox]

### Tecnico
- [aprendizados tecnicos]

## Arquivos Criados/Modificados
- [lista com caminhos]

## Conteudo de Anexos Processados
[Se houver anexos, extraia e documente o conteudo relevante aqui]

## Problemas Resolvidos
- [lista]

## Proximos Passos Sugeridos
- [acoes para proxima sessao]
```

## PASSO 4: Atualizar Memory File

Atualize `.claude/memory.md` com:
- Estado atual do projeto
- Ultimas acoes realizadas
- Bloqueios conhecidos
- Notas importantes da sessao

## PASSO 5: Atualizar LAYERS.md (se necessario)

Se alguma camada mudou de status:
- Atualizar status (LOCKED/OPEN/REVIEW)
- Adicionar entrada no historico de alteracoes

## PASSO 6: Commit e Push

Execute:
```bash
cd /c/Users/adm_r/intuit-boom
git add -A
git commit -m "Sessao [DATA]: [RESUMO CURTO]

[Lista dos principais itens trabalhados]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

git push origin master
```

## PASSO 7: Relatorio Final

Apresente ao usuario:
1. Resumo do que foi consolidado
2. Camadas alteradas (se houver)
3. Arquivos atualizados
4. Link do commit (se push foi sucesso)
5. Sugestao para proxima sessao

---
IMPORTANTE:
- NAO pule nenhum passo
- SEMPRE verificar LAYERS.md primeiro
- Se nao houver conteudo para alguma secao, escreva "Nenhum nesta sessao"
- Seja thorough na extracao de conhecimento
