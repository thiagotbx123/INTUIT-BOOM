# IES February Release FY26 - Explicacao para Leigo

> Este documento explica o release de Fevereiro 2026 do Intuit Enterprise Suite
> de forma simples, para quem nao e tecnico.
> Gerado: 2026-01-06

---

## O QUE E O IES?

**IES = Intuit Enterprise Suite**

E a versao "enterprise" (para empresas maiores) do QuickBooks. Enquanto o QuickBooks normal e para pequenas empresas, o IES e para empresas com:
- Faturamento acima de $3 milhoes/ano
- Multiplas empresas (holding + filiais)
- Necessidade de relatorios consolidados
- Equipes maiores (ate 500 usuarios)

---

## O QUE SAO ESSES "RELEASES"?

A Intuit lanca atualizacoes do QuickBooks em "ondas" durante o ano:

```
Ano Fiscal 2026 da Intuit (Jul 2025 - Jun 2026)

Jul   Ago   Set   Out   Nov   Dez   Jan   Fev   Mar   Abr   Mai   Jun
 |-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
                        |           |     |
                   FALL RELEASE  WINTER  FEBRUARY
                   (Nov 2025)    RELEASE  RELEASE
                                (Fev 26) (Fev+ 26)
```

Cada release traz **novas funcionalidades**. O TSA (Technical Solutions Architect) da TestBox precisa:
1. Entender o que vem em cada release
2. Preparar demos para mostrar aos clientes
3. Validar que tudo funciona no ambiente de teste

---

## O DOCUMENTO QUE VOCE RECEBEU

O arquivo `IES February Release FY26 _ .docx` e um **documento interno da Intuit** que descreve UMA feature especifica: o **Conversational BI**.

### O que e Conversational BI?

**BI = Business Intelligence** = Ferramentas para analisar dados do negocio

**Conversational** = Voce conversa em linguagem normal

**Juntando:** Voce pode PERGUNTAR coisas sobre seu negocio ao QuickBooks, como se estivesse conversando com uma pessoa.

---

## EXEMPLOS PRATICOS

### Antes (Jeito Tradicional)

1. Abrir QuickBooks
2. Ir em Relatorios
3. Escolher "Relatorio de Vendas"
4. Configurar filtros (data, cliente, produto)
5. Gerar relatorio
6. Exportar para Excel
7. Fazer graficos manualmente
8. Juntar com dados de outros sistemas
9. Analisar...

**Tempo: 30 minutos a 2 horas**

### Depois (Com Conversational BI)

1. Abrir chat do Intuit Intelligence
2. Digitar: "Qual foi minha receita por produto nos ultimos 3 meses?"
3. Receber resposta com grafico pronto

**Tempo: 30 segundos**

---

## POR QUE ISSO E IMPORTANTE?

### Problema 1: Dados Espalhados

Uma empresa tipica tem dados em:
- QuickBooks (financeiro)
- Salesforce/HubSpot (vendas)
- Planilhas Excel (orcamentos)
- Sistemas de inventario
- Folha de pagamento

**Antes:** Voce precisa exportar de cada um, juntar no Excel, rezar pra nao ter erro.

**Depois:** O Conversational BI acessa TODOS de uma vez e responde.

### Problema 2: ChatGPT nao resolve

Muita gente usa ChatGPT para analisar dados. Mas:

| Problema | ChatGPT | Intuit Intelligence |
|----------|---------|---------------------|
| Precisa fazer upload | Sim (manual) | Nao (conectado) |
| Dados ficam atualizados? | Nao (foto do momento) | Sim (tempo real) |
| Dados vao para fora da empresa? | Sim | Nao |
| Entende contabilidade? | Mais ou menos | Sim (nativo) |
| Historico fica salvo? | Arquivos somem | Permanente |

### Problema 3: Precisao

Quando voce faz upload para o ChatGPT, ele ADIVINHA a estrutura dos dados. As vezes acerta, as vezes erra.

O Intuit Intelligence **conhece** a estrutura do QuickBooks. Quando voce pergunta "qual minha margem bruta?", ele sabe exatamente quais contas somar e dividir.

---

## O QUE VEM EM CADA VERSAO

### November 2025 (Ja lancado)

- Perguntas sobre dados do QuickBooks
- Upload de planilhas para analise junto
- Graficos bonitos nas respostas

### February 2026 (O documento)

- **NOVO:** Acesso a dados de TERCEIROS (CRM, inventario) sem upload
- **NOVO:** Benchmarks exclusivos da Intuit (comparar sua empresa com outras do setor)
- **NOVO:** Contadores podem usar pelo cliente via IAS

---

## O QUE OS COMENTARIOS DO DOCUMENTO REVELAM

O documento do Google Docs tem comentarios dos funcionarios da Intuit:

### Comentario 1 (Jed McLoughlin):
> "Is it ready to answer questions about everything on the platform, including payroll?"

**Traducao:** "Sera que o chat consegue responder sobre folha de pagamento?"

**O que isso significa:** A integracao com payroll pode nao estar 100% pronta.

### Comentario 2 (Jed McLoughlin):
> "Will it be ME [Multi-Entity] aware?"

**Traducao:** "Sera que ele entende empresas com multiplas filiais?"

**O que isso significa:** Pode haver limitacao para empresas com holding + subsidiarias.

### Comentario 3 (Casey Roeder):
> "Things have been consistently in flux... let me check in with PM"

**Traducao:** "As coisas estao mudando constantemente... deixa eu confirmar com o gerente de produto"

**O que isso significa:** O escopo final pode mudar antes do lancamento.

---

## IMPLICACOES PRATICAS PARA VOCE

### Se voce for demonstrar isso para clientes:

1. **Teste ANTES** - Features podem nao funcionar como esperado
2. **Tenha alternativas** - Se o chat nao responder, tenha relatorios tradicionais prontos
3. **Documente limitacoes** - Seja honesto sobre o que funciona e o que nao
4. **Acompanhe updates** - O PM vai atualizar o documento conforme as coisas forem confirmadas

### Perguntas para testar:

**Basicas (devem funcionar):**
- "Qual foi minha receita mes passado?"
- "Quantos clientes novos tive?"
- "Qual meu produto mais vendido?"

**Intermediarias (testar):**
- "Compare minha receita com o mes anterior"
- "Qual minha margem bruta por produto?"

**Avancadas (podem nao funcionar ainda):**
- "Analise meus dados de CRM junto com financeiro"
- "Compare minha performance com benchmarks do setor"
- "Qual o custo de payroll por departamento?"

---

## RESUMO FINAL

### O que e o February Release?

Uma atualizacao do QuickBooks Enterprise que adiciona um **chat inteligente** (Conversational BI) que permite fazer perguntas sobre o negocio em linguagem natural.

### Por que isso importa?

- Economiza tempo (minutos vs horas)
- Mais preciso que ChatGPT para dados financeiros
- Integra dados de varios sistemas
- Seguro (dados nao saem da Intuit)

### Pontos de atencao?

- Escopo ainda pode mudar
- Payroll e Multi-Entity podem ter limitacoes
- Integracao com sistemas terceiros pode nao estar pronta
- Benchmarks exclusivos podem nao estar disponiveis

### O que fazer agora?

1. Leia a analise critica completa: `IES_FEBRUARY_RELEASE_FY26_ANALISE_CRITICA.md`
2. Acompanhe updates do PM da Intuit
3. Teste no ambiente quando disponivel (Early Access: 2026-02-04)
4. Documente o que funciona e o que nao

---

## GLOSSARIO

| Termo | Significado |
|-------|-------------|
| **IES** | Intuit Enterprise Suite - versao enterprise do QuickBooks |
| **BI** | Business Intelligence - ferramentas de analise de dados |
| **Conversational** | Baseado em conversa/chat |
| **3P** | Third Party - sistemas terceiros (Salesforce, HubSpot, etc) |
| **Multi-Entity** | Multiplas empresas (holding + filiais) |
| **Payroll** | Folha de pagamento |
| **PM** | Product Manager - gerente de produto |
| **TSA** | Technical Solutions Architect - arquiteto de solucoes tecnicas |
| **Early Access** | Acesso antecipado para testers |
| **Benchmark** | Comparacao com outras empresas do setor |
| **KPI** | Key Performance Indicator - indicador chave de desempenho |

---

Documento criado para facilitar entendimento do release.
Consulte a analise critica para detalhes tecnicos.
