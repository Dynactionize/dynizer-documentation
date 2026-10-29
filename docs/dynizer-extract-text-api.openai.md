# Extract Text API

Apache Tika wrapper API for text extraction

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Contact | Consono <info@consono.ai> (https://consono.ai) |

## Tags

| Name | Description |
|------|-------------|
| Extract | Text extraction from documents |
| State | State of the API |
| Health check | Checks regarding the health of the service |

## Endpoints

### `POST /extract`

Tags: `Extract`

Operation ID: `postExtract`

Submit a document for text extraction

**Responses**

- `202`: Extract request accepted — [ExtractAcceptedResponse](#extractacceptedresponse)
- `400`: Bad request. — [Error](#error)
- `503`: Service unavailable. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /state`

Tags: `State`

Operation ID: `getState`

Get state of the extract-text-api

**Responses**

- `200`: Get API state response — [StateResponse](#stateresponse)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /healthz`

Tags: `Health check`

Operation ID: `getHealthz`

k8s style health check. Returns 200 if running correctly


**Responses**

- `200`: Health check successful
- `503`: Service unavailable. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

## Response Components

### DefaultErrorResponse

Unexpected error.

Content (`application/json`): [Error](#error)

### 400ErrorResponse

Bad request.

Content (`application/json`): [Error](#error)

### 503ErrorResponse

Service unavailable.

Content (`application/json`): [Error](#error)

### PostExtractResponse

Extract request accepted

Content (`application/json`): [ExtractAcceptedResponse](#extractacceptedresponse)

### GetStateResponse

Get API state response

Content (`application/json`): [StateResponse](#stateresponse)


## Schemas

### ID

ID of an object.

### RemoteID

Remote ID from the API that requested the extraction.

### Status

Status of an extraction. Can be one of QUEUED|RUNNING|FAILED|SUCCESS.

### Filetype

Filetype of the document.

### FiletypeConfig

### Base64Document

Document serialized in base64 string.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | string |  | Base64-encoded document data. |

### Document

Document to extract text from.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| filetype | [Filetype](#filetype) | yes |  |
| filetype_config | [FiletypeConfig](#filetypeconfig) |  |  |
| base64 | [Base64Document](#base64document) | yes |  |

### ExtractRequest

Request to extract text from a document.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| document | [Document](#document) | yes |  |
| webhook | string | yes | Webhook URL to call with results. |
| remote_id | [RemoteID](#remoteid) | yes |  |

### ExtractAcceptedResponse

Response when an extraction request is accepted.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |
| status | [Status](#status) | yes |  |

### ExtractMetadata

Metadata extracted from the document.

### StateResponse

All data regarding the state of the API.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| endpoint | string | yes | Self-reported endpoint. |
| process_available | integer | yes | Number of available processing slots. |
| process_queued | integer |  | Number of queued requests. |
| supported_filetypes | array of string | yes | List of supported file types. |
| tika_endpoint | string |  | Tika REST API endpoint. |

### Error

API error.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | integer | yes |  |
| message | string | yes |  |

