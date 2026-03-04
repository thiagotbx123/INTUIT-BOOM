# TSA_CORTEX - Camada de Coleta

> Documentacao importada do projeto TSA_CORTEX para treinamento do Claude

## Visao Geral

A Camada de Coleta do CORTEX e responsavel por coletar dados de multiplas fontes para gerar worklogs automatizados. Usa padrao **Collector Pattern** com classes especializadas por fonte.

## Arquitetura

```
src/collectors/
├── base.ts        # Classe abstrata BaseCollector
├── index.ts       # Factory e barrel exports
├── slack.ts       # SlackCollector
├── linear.ts      # LinearCollector
├── drive.ts       # DriveCollector
├── local.ts       # LocalCollector
└── claude.ts      # ClaudeCollector
```

## Fontes Disponiveis

| Fonte | Classe | O que Coleta |
|-------|--------|--------------|
| **Slack** | SlackCollector | DMs, mensagens em canais, threads, mencoes |
| **Linear** | LinearCollector | Issues criadas, atribuidas, comentarios |
| **Google Drive** | DriveCollector | Arquivos criados/modificados |
| **Local** | LocalCollector | Arquivos locais por path |
| **Claude** | ClaudeCollector | Prompts do usuario em sessoes Claude |

---

## Interface Base (BaseCollector)

```typescript
export interface CollectorResult {
  source: SourceSystem;
  events: ActivityEvent[];
  rawData: unknown[];
  errors: string[];
  warnings: string[];
  recordCount: number;
}

export abstract class BaseCollector {
  protected config: Config;
  protected dateRange: DateRange;
  protected userId: string;

  abstract get source(): SourceSystem;
  abstract isConfigured(): boolean;
  abstract collect(): Promise<CollectorResult>;
}
```

### Metodos Auxiliares
- `createEmptyResult()` - Cria resultado vazio padrao
- `logInfo/logWarn/logError()` - Logging com prefixo da fonte

---

## SlackCollector

### Estrategia de Coleta

O Slack usa **Search API** com queries estruturadas:

1. **DMs**: Coleta TUDO no range (sempre relevante)
   ```
   is:dm after:YYYY-MM-DD before:YYYY-MM-DD
   ```

2. **Mensagens do Usuario**: O que EU mandei em canais
   ```
   from:me -is:dm after:YYYY-MM-DD before:YYYY-MM-DD
   ```

3. **Mencoes**: Onde fui @mencionado
   ```
   <@USER_ID> -is:dm after:YYYY-MM-DD before:YYYY-MM-DD
   ```

4. **Keywords**: Busca por palavras-chave em canais ativos

### Classificacao de Ownership

| Ownership | Significado |
|-----------|-------------|
| `my_work` | Mensagem que EU enviei |
| `mentioned` | Fui @mencionado |
| `context` | Contexto (DM recebida) |
| `keyword_match` | Match por keyword |

### Credenciais

Usa tokens XOXC/XOXD via `getSlackCredentials()`:
- `SLACK_USER_TOKEN` com scope `search:read`

---

## LinearCollector

### Estrategia de Coleta

Busca issues relacionadas ao usuario:

1. **Issues Criadas**: `creator.id === userId`
2. **Issues Atribuidas**: `assignee.id === userId`
3. **Issues Comentadas**: Comentarios do usuario

### Tipos de Eventos

| Tipo | Quando |
|------|--------|
| `issue_created` | Usuario criou a issue |
| `issue_updated` | Issue atribuida foi atualizada |
| `comment` | Usuario comentou na issue |

### API

Usa `@linear/sdk`:
```typescript
const client = new LinearClient({ apiKey: creds.apiKey });
const issues = await client.issues({ filter: {...} });
```

---

## ClaudeCollector

### Fontes de Dados

1. **history.jsonl** (principal)
   - Path: `~/.claude/history.jsonl`
   - Contem: Todos os prompts do usuario com timestamp, projeto, sessao

2. **Project Sessions** (opcional)
   - Path: `~/.claude/projects/{project}/*.jsonl`
   - Contem: Mensagens completas das sessoes

3. **memory.md** (opcional)
   - Path: `~/.claude/memory.md`
   - Contem: Memoria persistente do Claude

### Filtros Aplicados

```typescript
// Projetos ignorados (ruido)
const IGNORED_PROJECT_PATTERNS = [
  'system32',
  'C--windows',
  'windows-system32',
];

// Prompts muito curtos
const MIN_PROMPT_LENGTH = 5;

// Comandos ignorados
const ignoredCommands = ['c', 'y', 'n', 'yes', 'no', 'ok', 'b', 's'];
```

### Estrutura history.jsonl

```typescript
interface ClaudeHistoryEntry {
  display: string;      // Texto do prompt
  timestamp: number;    // ms since epoch
  project: string;      // Path do projeto
  sessionId: string;    // ID da sessao
}
```

---

## LocalCollector

### Configuracao

```typescript
interface LocalConfig {
  enabled: boolean;
  scan_paths: string[];           // Paths para escanear
  denylist_patterns: string[];    // Patterns a ignorar
  max_file_size_mb: number;       // Limite de tamanho
}
```

### Eventos Gerados

| Tipo | Condicao |
|------|----------|
| `file_created` | birthtime dentro do range |
| `file_modified` | mtime dentro do range |

### Denylist Patterns

Suporta:
- `**` - Match recursivo
- `*` - Match simples
- `*.ext` - Por extensao
- `string` - Contains

---

## Factory Pattern

```typescript
// Criar um coletor especifico
const collector = createCollector('slack', config, dateRange, userId);

// Criar todos os coletores configurados
const collectors = getAllCollectors(config, dateRange, userId);

// Executar todos e retornar resultados
const results = await runAllCollectors(config, dateRange, userId);
```

---

## Evento Normalizado (ActivityEvent)

Todos os coletores transformam dados raw para este schema:

```typescript
interface ActivityEvent {
  event_id: string;              // Hash estavel
  source_system: SourceSystem;   // slack|linear|drive|local|claude
  source_record_id: string;      // ID original da fonte
  actor_user_id: string;         // Quem fez a acao
  actor_display_name: string;    // Nome legivel
  event_timestamp_utc: string;   // ISO 8601
  event_timestamp_local: string; // Com timezone
  event_type: EventType;         // message|comment|file_created|etc
  title: string;                 // Titulo curto
  body_text_excerpt: string;     // Texto (max 500 chars)
  references: EventReference[];  // Referencias (URLs, IDs)
  source_pointers: SourcePointer[]; // Ponteiros para fonte original
  pii_redaction_applied: boolean;
  confidence: 'low' | 'medium' | 'high';
  raw_data?: Record<string, unknown>;
}
```

---

## Tipos de Evento (EventType)

```typescript
type EventType =
  | 'message'           // Mensagem Slack
  | 'comment'           // Comentario Linear
  | 'status_change'     // Mudanca de status
  | 'file_created'      // Arquivo criado
  | 'file_modified'     // Arquivo modificado
  | 'meeting_note'      // Nota de reuniao
  | 'artifact_generated'// Artefato gerado
  | 'issue_created'     // Issue criada
  | 'issue_assigned'    // Issue atribuida
  | 'issue_mentioned'   // Mencionado em issue
  | 'issue_updated'     // Issue atualizada
  | 'thread_reply'      // Resposta em thread
  | 'reaction'          // Reacao
  | 'link_shared'       // Link compartilhado
  | 'prompt'            // Prompt Claude
  | 'response';         // Resposta Claude
```

---

## Source Pointers

Ponteiros para a fonte original (rastreabilidade):

```typescript
interface SourcePointer {
  pointer_id: string;          // ID estavel
  type: SourcePointerType;     // Tipo do ponteiro
  url?: string;                // URL se aplicavel
  path?: string;               // Path local se aplicavel
  file_hash_sha256?: string;   // Hash do arquivo
  display_text: string;        // Texto legivel
}
```

### Tipos de Pointer

- `slack_message_permalink` - Link direto para mensagem Slack
- `linear_issue_url` - URL da issue Linear
- `drive_file_url` - URL do arquivo no Drive
- `local_file_path` - Path do arquivo local
- `claude_prompt` - Prompt no Claude

---

## Configuracao (config.yaml)

```yaml
collectors:
  slack:
    enabled: true
    target_channels: ['general', 'dev']
    collect_dms: true
    search_keywords: ['important', 'urgent']

  linear:
    enabled: true
    include_comments: true
    include_status_changes: true

  drive:
    enabled: true
    allowlist_folders: ['Projects', 'Work']
    denylist_extensions: ['.tmp', '.log']

  local:
    enabled: true
    scan_paths: ['~/Documents/work']
    denylist_patterns: ['node_modules', '.git']
    max_file_size_mb: 10

  claude:
    enabled: true
    include_session_context: false
    include_memory: true

privacy:
  redact_emails: true
  redact_phone_numbers: true
```

---

## Como Usar no Treinamento

### 1. Acessar Dados do Claude

O ClaudeCollector pode ler TUDO que voce fez em sessoes anteriores:
- Prompts enviados
- Projetos trabalhados
- Sessoes por data

### 2. Acessar Slack

O SlackCollector pode buscar:
- Conversas relevantes
- Decisoes documentadas
- Contexto de projetos

### 3. Acessar Linear

O LinearCollector pode buscar:
- Tasks e issues
- Historico de trabalho
- Comentarios e decisoes

---

## Proximos Passos para Treinamento

1. [ ] Configurar coletores no intuit-boom
2. [ ] Definir range de datas para coleta
3. [ ] Executar coleta de todas as fontes
4. [ ] Normalizar eventos para ActivityEvent
5. [ ] Usar dados para treinar contexto

---

Documento importado em: 2024-12-26
Fonte: TSA_CORTEX/src/collectors/
