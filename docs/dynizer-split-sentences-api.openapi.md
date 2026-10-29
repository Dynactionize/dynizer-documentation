# split-sentences-api

Sentence/clause splitting analyzer for pipeline-api (the `split` flow).

A pre-processing step modelled on text extraction: pipeline-api calls `POST /split` once with `{document, webhook, remote_id}`; the service acks `{id}`, sentencizes on a Celery worker, and POSTs `{id, remote_id, status, segments}` to the `webhook` URL. Single-call and async. Inbound auth was removed — reached only over the internal network. Designed as the split step in `Extract -> Split -> Analyze -> Plugins`; see `docs/verify_pipeline_chaining.md`.

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Contact | Consono <info@consono.ai> (https://consono.ai/) |

## Tags

| Name | Description |
|------|-------------|
| split | Split a document into ordered segments. |
| health | Liveness. |
| state | Capacity and configured sentencizer backend. |

## Servers

| URL | Description |
|-----|-------------|
| `/` | Default |

## Endpoints

### `GET /healthz`

*Healthz*

Tags: `health`

Operation ID: `healthz`

**Responses**

- `200`: Successful Response — [HealthResponse](#healthresponse)

---

### `GET /state`

*State*

Tags: `state`

Operation ID: `getState`

**Responses**

- `200`: Successful Response — [StateResponse](#stateresponse)

---

### `POST /split`

*Post Split*

Tags: `split`

Operation ID: `submitSplit`

**Request Body** (`application/json`): [SplitRequest](#splitrequest)

**Responses**

- `200`: Successful Response — [SplitResponse](#splitresponse)
- `400`: No usable document text. — [ErrorResponse](#errorresponse)
- `422`: Validation Error — [HTTPValidationError](#httpvalidationerror)

**Callbacks**

- `split_webhook`
  - Expression: `{$request.body#/webhook}`
  - `POST` Segments delivered to the caller's webhook

---

## Response Components

### HealthCheckResponse

Successful Response

Content (`application/json`): [HealthResponse](#healthresponse)

### StateInfoResponse

Successful Response

Content (`application/json`): [StateResponse](#stateresponse)

### SplitAcceptedResponse

Successful Response

Content (`application/json`): [SplitResponse](#splitresponse)

### WebhookDeliveredResponse

Successful Response

Content (`application/json`): [WebhookResult](#webhookresult)

### NoUsableTextResponse

No usable document text.

Content (`application/json`): [ErrorResponse](#errorresponse)

### ValidationErrorResponse

Validation Error

Content (`application/json`): [HTTPValidationError](#httpvalidationerror)


## Schemas

### DocumentEnvelope

Minimal typed shape for the ``document`` field.

pipeline-api sends ``{"text": {"data": "<text>"}}``. Other keys
(``content``, ``body``, ``data``) are also probed by ``resolve_text``.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | [DocumentText](#documenttext) | string | null |  |  |
| content | string | null |  |  |
| body | string | null |  |  |
| data | string | null |  |  |

### DocumentText

The ``text`` sub-object inside a document envelope.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | string | null |  |  |

### ErrorResponse

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| detail | string | yes | Human-readable error detail. |

### HTTPValidationError

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| detail | array of [ValidationError](#validationerror) |  |  |

### HealthResponse

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| status | string |  | Liveness marker. (default: `ok`) |
| flow_name | string | yes | Configured flow name, e.g. split. |
| backend | string | yes | Configured sentencizer backend. |

### LanguageConfig

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| target_languages | array of string |  |  |

### SegmentModel

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| index | integer | yes | 0-based position of the segment in the document. |
| text | string | yes | The segment (sentence/clause) text, stripped. |
| start | integer | yes | Start char offset into the source text (inclusive). |
| end | integer | yes | End char offset into the source text (exclusive). |

### SentencizerConfig

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| backend | string | null |  |  |

### SplitConfig

Optional per-request config overlay.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| language | [LanguageConfig](#languageconfig) | null |  |  |
| sentencizer | [SentencizerConfig](#sentencizerconfig) | null |  |  |

### SplitMetadata

Extraction-style metadata returned with the webhook result.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| language | string | null |  | Detected or requested language code. |
| count | integer | null |  | Number of segments produced. |

### SplitRequest

A split dispatch, e.g.::

    {"document": {"text": {"data": "<text>"}},
     "webhook": "http://pipeline-api:50052/webhooks/split",
     "remote_id": "<pipeline-id>"}

Inline ``text`` and a few common document keys are also accepted.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| document | [DocumentEnvelope](#documentenvelope) | null |  |  |
| text | string | null |  |  |
| webhook | string | null |  |  |
| remote_id | string | null |  |  |
| config | [SplitConfig](#splitconfig) | null |  |  |

### SplitResponse

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | yes |  |

### StateResponse

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| endpoint | string | yes | This service's own registration endpoint. |
| process_available | integer | yes | Free Celery concurrency: max(0, total_concurrency - active). |
| process_queued | integer | yes | Reserved (queued) Celery tasks. |
| flow_names | array of string | yes | Flow names this analyzer serves. |
| backend | string | yes | Configured sentencizer backend. |

### ValidationError

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| loc | array of string | integer | yes |  |
| msg | string | yes |  |
| type | string | yes |  |
| input |  |  |  |
| ctx | object |  |  |

### WebhookResult

The split result POSTed to the caller's webhook (doc-only model).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | yes |  |
| remote_id | string | null |  |  |
| status | string | yes | "SUCCESS" | "FAILED" |
| segments | array of [SegmentModel](#segmentmodel) | null |  | Ordered segments on SUCCESS; null on FAILED. |
| metadata | [SplitMetadata](#splitmetadata) | null |  | Extraction-style metadata, e.g. {language, count}. |
| error | string | null |  | Error message on FAILED. |
| log | string | null |  | Traceback on FAILED. |

