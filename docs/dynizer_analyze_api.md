---
name: knowledge_dynizer_analyze_api
description: Dynizer Analyze API overview — NLP document analysis service (v1 and v2)
---

# Dynizer Analyze API

The Analyze API is a Natural Language Processing (NLP) service that takes in documents and produces structured JSON results. You upload a file (PDF, Word, etc.), start an analysis, and retrieve the results.

## What it does

When you submit a document, the analyzer runs a full NLP pipeline that:

1. **Extracts text** from documents (PDF, Word, and more)
2. **Tokenizes** the text into individual words
3. **Detects sentences** and their boundaries
4. **Tags parts of speech (POS)** — identifying nouns, verbs, adjectives, etc.
5. **Parses syntax and dependencies** — understanding how words relate to each other grammatically
6. **Recognizes named entities (NER)** — picking out people, places, organizations, dates, etc.
7. **Resolves co-references** — linking pronouns like "he" or "it" back to the entity they refer to
8. **Extracts key concepts** — identifying the main topics and ideas in the text
9. **Matches against ontologies** — mapping extracted entities to known domain concepts
10. **Detects tone of voice** — analyzing sentiment and communication style

The output is a structured JSON containing Who/What/Where/When elements grouped into Actions.

## API Versions

### Analyze API v1 (original)

Full-lifecycle analysis management with authentication (bearer JWT).

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `POST /documents` | Upload a document for processing |
| `POST /analyze` | Start an analysis |
| `GET /analyze` | List all analyze processes (supports `limit` and `offset`) |
| `GET /analyze/{id}` | Get status/data of a specific analyze process |
| `PUT /analyze/{id}` | Control a running analysis (pause, cancel) |
| `DELETE /analyze/{id}` | Stop and delete an analyze process |
| `GET /state` | Get API state (endpoint, available processes, flow names) |
| `GET /healthz` | Health check |

**Statuses:** `QUEUED` | `RUNNING` | `FAILED` | `SUCCESS` | `CANCELED` | `PAUSED`

**Supported file types:** txt, pdf, doc, docx, rtf, odt, eml, msg

**Document input modes** (set exactly one): `text` (raw text), `base64` (base64-encoded), `private` (previously uploaded doc ID), `public` (public URI)

### Analyze API v2 (analyze-core, 4-stage pipeline)

Lightweight internal service used by pipeline-api. No authentication — reachable only over the internal network.

**Flow:** pipeline-api calls `POST /documents` (raw extracted text) then `POST /analyze` (empty document envelope). The text is stashed in a single-slot consume-once buffer; `/analyze` consumes it and dispatches the 4-stage pipeline to a Celery worker. Results are delivered via webhook callback.

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `POST /documents` | Stash extracted text (returns `{"status": "ok"}`) |
| `POST /analyze` | Consume stashed text and start analysis (returns `{"id": "..."}`) |
| `GET /state` | API state (endpoint, available/queued processes, flow names, loaded models) |
| `GET /healthz` | Health check |

**Output formats:**
- `v1` (legacy): wrapped in `document.sections[0].action_records`
- `v2` (default): flat `document.action_records`

**Webhook result fields:** `id`, `remote_id`, `status`, `output`, `error`, `log`, `started_at`, `finished_at`

**Key schemas:** `AnalyzeRequest` (type, remote_id, webhook, flow_name, config, text, document), `ActionRecord` (instance_id, source_text, original_text, action_name, segments, confidence, language), `Segment` (ct, tokens), `Token` (text, label)