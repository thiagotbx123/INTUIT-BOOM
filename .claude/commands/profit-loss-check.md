# Profit & Loss Check

## O que faz
Compara o P&L real do QBO (fonte de verdade) contra o dataset no PostgreSQL.
Identifica divergências e gera bases de correção para ingestão.

## Fonte de verdade
O **QBO** é o sistema correto. O dataset precisa refletir o QBO.

## Inputs necessários
- P&L Detail CSV exportado do QBO (Accrual, This Year) por entity
- Acesso ao PostgreSQL v20260319 (novo) ou unstable (antigo)

## Statuses (3 apenas)
- **OK** — Existe no QBO e no dataset. Nada a fazer.
- **CRIAR NO DATASET** — Existe no QBO mas não no dataset. Precisa ser adicionado.
- **PENDENTE NO QBO** — Existe no dataset mas ainda não apareceu no QBO. Activity plan vai processar.

## Etapas
1. Parsear P&L Detail CSVs do QBO
2. Consultar dataset no PostgreSQL
3. Cruzar por TBX ID (invoices, expenses, bills) e por tipo (deposits, JEs, payroll)
4. Gerar planilha de divergências com ações
5. Gerar bases de correção (invoices/LIs CSV) para ingestão
6. Ingerir no banco correto

## Entity Mapping (Coda confirmado)
- Keystone Construction (Parent) = parent
- Keystone Terra (Child) = main_child
- Keystone BlueCraft = secondary_child

## Bancos
- Novo: v20260319 (user=dataset, db=v20260319)
- Antigo: unstable (user=unstable, db=unstable)
- Dataset ID construction: 321c6fa0-a4ee-4e05-b085-7b4d51473495
