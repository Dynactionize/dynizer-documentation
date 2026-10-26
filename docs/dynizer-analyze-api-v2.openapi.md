# analyze-api-v2

Text-analysis service (analyze-core 4-stage pipeline) for pipeline-api.

pipeline-api dispatches `analyze_v2` work with a single `POST /analyze` carrying the document inline — either pre-split `segments` (from the split step) or raw `text`/`document`. `/analyze` dispatches the 4-stage pipeline to a Celery worker, and the worker POSTs the result to the `webhook` URL. Inbound requests require a valid Dynizer JWT or the pipeline-api shared secret.

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Contact | Consono <info@consono.ai> (https://consono.ai/) |

## Tags

| Name | Description |
|------|-------------|
| analyze | Submit text-analysis work. |
| health | Liveness. |
| state | Capacity and per-stage model availability. |

## Servers

| URL | Description |
|-----|-------------|
| `/` | Current host |

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

### `POST /analyze`

*Post Analyze*

Tags: `analyze`

Operation ID: `postAnalyze`

**Request Body** (`application/json`): [AnalyzeRequest](#analyzerequest)

**Responses**

- `200`: Successful Response — [AnalyzeResponse](#analyzeresponse)
- `400`: No usable document text. — [ErrorResponse](#errorresponse)
- `422`: Validation Error — [HTTPValidationError](#httpvalidationerror)

**Callbacks**

- `analysis_webhook`
  - Expression: `{$request.body#/webhook}`
  - `POST` Analysis result delivered to the caller's webhook

---

### `GET /analyze/{job_id}`

*Get Analyze Status*

Tags: `analyze`

Operation ID: `getAnalyzeStatus`

Poll the status and result of a submitted analysis job.

**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| job_id | path | string | True |  |

**Responses**

- `200`: Successful Response — [JobStatusResponse](#jobstatusresponse)
- `404`: Unknown job ID. — [ErrorResponse](#errorresponse)
- `422`: Validation Error — [HTTPValidationError](#httpvalidationerror)

---

## Response Components

### HealthCheckResponse

Successful Response

Content (`application/json`): [HealthResponse](#healthresponse)

### StateInfoResponse

Successful Response

Content (`application/json`): [StateResponse](#stateresponse)

### AnalyzeAcceptedResponse

Successful Response

Content (`application/json`): [AnalyzeResponse](#analyzeresponse)

### JobStatusOKResponse

Successful Response

Content (`application/json`): [JobStatusResponse](#jobstatusresponse)

### NoUsableTextResponse

No usable document text.

Content (`application/json`): [ErrorResponse](#errorresponse)

### UnknownJobResponse

Unknown job ID.

Content (`application/json`): [ErrorResponse](#errorresponse)

### ValidationErrorResponse

Validation Error

Content (`application/json`): [HTTPValidationError](#httpvalidationerror)


## Schemas

### ActionRecord

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| instance_id | string | null |  |  |
| source_text | string | yes |  |
| original_text | string | yes |  |
| action_name | string | yes |  |
| segments | array of [Segment](#segment) | yes |  |
| confidence | number | yes |  |
| confidence_per_stage | map of number | null |  |  |
| language | string | null |  |  |
| job_id | string | null |  |  |
| reviewed | boolean |  |  (default: `False`) |

### AnalyzeConfig

Recognised ``config`` keys for an analyze request.

Only the fields below change pipeline behaviour.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| mode | string enum: ['full', 'decomposition', 'action', 'segments', 'entities'] |  | Stage selector for the analyze-core pipeline. 'full' = decomposition + per-clause action/segments/entities (stages 1-4). 'decomposition' = stage 1 only (clauses, no action records). 'action' = stage 2 only, input treated as one clause. 'segments' = stages 2-3. 'entities' = stages 2-4. (default: `full`) |
| output_format | string enum: ['v1', 'v2'] |  | Result shape on the webhook. 'v1' wraps action_records under sections[0] (default, parsed by pipeline-api's v1 plugins); 'v2' is the flat action_records document. (default: `v1`) |
| language | [LanguageConfig](#languageconfig) | null |  | Language routing; omit to auto-detect from the text. |
| segments | array of [InputSegment](#inputsegment) | null |  | Pre-split units forwarded by pipeline-api's split flow. Typically arrives under config.segments rather than top-level segments. |

### AnalyzeOutputV1

Legacy output (`config.output_format = "v1"`): wrapped in sections[0].

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| document | [DocumentV1](#documentv1) | yes |  |

### AnalyzeOutputV2

Default output (`config.output_format = "v2"`): flat action_records.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| document | [DocumentV2](#documentv2) | yes |  |

### AnalyzeRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string |  |  (default: `background`) |
| remote_id | string | null |  |  |
| webhook | string | null |  |  |
| flow_name | string | null |  |  |
| config | [AnalyzeConfig](#analyzeconfig) |  |  |
| text | string | null |  |  |
| document | [DocumentInput](#documentinput) | null |  |  |
| segments | array of [InputSegment](#inputsegment) | null |  |  |

### AnalyzeResponse

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | yes |  |

### DocumentInput

Incoming document envelope (Dynizer TextDocument or legacy formats).

pipeline-api sends a Dynizer TextDocument with ``text.data``; older
contracts may nest content under ``private``.  The router's
``resolve_text()`` probes all known locations.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | [TextData](#textdata) | null |  | Inline text or a Dynizer TextDocument ``{data: ...}`` object. |
| private | map of string | null |  | Legacy private block; may carry text/content/body/data keys. |
| filetype_configuration | map of string | null |  | Filetype configuration forwarded from pipeline-api. |
| content | string | null |  | Legacy content field. |
| body | string | null |  | Legacy body field. |
| data | string | null |  | Legacy data field. |

### DocumentV1

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | yes |  |
| language | string | null |  |  |
| sections | array of [SectionV1](#sectionv1) |  |  |

### DocumentV2

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | yes |  |
| language | string | null |  |  |
| clauses | array of string |  |  |
| action_records | array of [ActionRecord](#actionrecord) |  |  |

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
| flow_name | string | yes | Configured flow name, e.g. analyze_v2. |
| model_dir_present | boolean | yes | Whether the model dir exists on disk. |

### InputSegment

One pre-split unit from the split step.

``text`` is the sentence/clause-sized unit fed to the pipeline; ``index`` /
``start`` / ``end`` (char offsets into the source) are used only to order the
segments on merge. A bare string is accepted and coerced to ``{text: ...}``.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | yes |  |
| index | integer | null |  | 0-based position in the document. |
| start | integer | null |  | Start char offset into the source text. |
| end | integer | null |  | End char offset into the source text. |

### JobStatusResponse

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | yes | Job ID. |
| status | string | yes | "PENDING" | "STARTED" | "SUCCESS" | "FAILED" |
| output | [AnalyzeOutputV2](#analyzeoutputv2) | [AnalyzeOutputV1](#analyzeoutputv1) | null |  | Analysis output on SUCCESS; null otherwise. |
| error | string | null |  | Error message on FAILED. |

### LanguageConfig

Language routing for the pipeline.

``target_languages[0]`` selects the per-language promoted model set
(see model_resolver.model_dirs_for_language); when absent the worker
auto-detects the language from the text.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| target_languages | array of string |  | Declared target languages, e.g. ['en']. First entry routes model selection; if empty the language is auto-detected. |

### SectionV1

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| clauses | array of string |  |  |
| action_records | array of [ActionRecord](#actionrecord) |  |  |

### Segment

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ct | string | yes | Segment type: who, what, where, when |
| tokens | array of [Token](#token) | yes |  |

### StateResponse

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| endpoint | string | yes | This service's own registration endpoint. |
| process_available | integer | yes | Free Celery concurrency: max(0, total_concurrency - active). |
| process_queued | integer | yes | Reserved (queued) Celery tasks. |
| flow_names | array of string | yes | Flow names this analyzer serves. |
| models_loaded | map of boolean | yes | Per-stage presence of a fine-tuned model dir on disk. |

### TextData

Dynizer TextDocument nested text object: ``{data: "<extracted text>"}``.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | string | yes | Extracted plain-text content. |

### Token

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | yes |  |
| label | string |  |  (default: ``) |

### ValidationError

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| loc | array of string | integer | yes |  |
| msg | string | yes |  |
| type | string | yes |  |
| input | string |  | The input value that caused the error. |
| ctx | map of string |  | Additional error context. |

### WebhookResult

Doc-only model describing the webhook callback body with a typed output.

Distinct from ``WebhookPayload`` so enriching the OpenAPI callback never
risks re-validating the live payload the worker delivers.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | yes |  |
| remote_id | string | null |  |  |
| status | string | yes | "SUCCESS" | "FAILED" |
| output | [AnalyzeOutputV2](#analyzeoutputv2) | [AnalyzeOutputV1](#analyzeoutputv1) | null |  | Mapped analysis output on SUCCESS; null on FAILED. |
| error | string | null |  | Error message on FAILED. |
| log | string | null |  | Traceback on FAILED. |
| started_at | string | null |  |  |
| finished_at | string | null |  |  |

