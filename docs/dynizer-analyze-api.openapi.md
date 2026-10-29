# Analyze API

TODO

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Contact | Consono <info@consono.ai> (https://consono.ai) |

## Tags

| Name | Description |
|------|-------------|
| Analyze | Manage analyze requests and processes |
| Documents | Add documents for processing |
| State | State of the API |
| Health check | Checks regarding the health of the service |

## Endpoints

### `GET /analyze`

Tags: `Analyze`

Operation ID: `getAnalyze`

Get the status and data of all analyze processes

**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |

**Responses**

- `200`: Get all analyze processes response — [AnalyzeResponsePage](#analyzeresponsepage)
- `404`: Not found. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /analyze`

Tags: `Analyze`

Operation ID: `postAnalyze`

Request processing from the analyzer.

**Responses**

- `200`: Request analyze process response — [AnalyzeResponse](#analyzeresponse)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /analyze/{id}`

Tags: `Analyze`

Operation ID: `getAnalyzeByID`

Get the status and data of an analyze process

**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `200`: Get analyze process response — [AnalyzeResponse](#analyzeresponse)
- `404`: Not found. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `PUT /analyze/{id}`

Tags: `Analyze`

Operation ID: `putAnalyzeByID`

Send an operation to be performed on an analyze process

**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Put analyze response
- `404`: Not found. — [Error](#error)
- `409`: Conflict. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `DELETE /analyze/{id}`

Tags: `Analyze`

Operation ID: `deleteAnalyzeByID`

Stop and delete an analyze process.

**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Delete analyze response
- `404`: Not found. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /documents`

Tags: `Documents`

Operation ID: `postDocuments`

Upload a document for processing

**Responses**

- `200`: Set document data response — [DocumentResponse](#documentresponse)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /state`

Tags: `State`

Operation ID: `getState`

Get state of the analyze-api

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

### 401ErrorResponse

Unauthorized.

Content (`application/json`): [Error](#error)

### 404ErrorResponse

Not found.

Content (`application/json`): [Error](#error)

### 409ErrorResponse

Conflict.

Content (`application/json`): [Error](#error)

### 503ErrorResponse

Service unavailable.

Content (`application/json`): [Error](#error)

### GetAnalyzeResponse

Get all analyze processes response

Content (`application/json`): [AnalyzeResponsePage](#analyzeresponsepage)

### PostAnalyzeResponse

Request analyze process response

Content (`application/json`): [AnalyzeResponse](#analyzeresponse)

### GetAnalyzeByIDResponse

Get analyze process response

Content (`application/json`): [AnalyzeResponse](#analyzeresponse)

### PostDocumentResponse

Set document data response

Content (`application/json`): [DocumentResponse](#documentresponse)

### GetStateResponse

Get API state response

Content (`application/json`): [StateResponse](#stateresponse)


## Schemas

### Limit

Limits the amount of records to return.

### Offset

Offsets the records to return.

### ID

ID of an object within the collection.

### Name

Name of an object within the collection.

### RemoteID

Remote ID from the API that requested the analyze process.

### Status

Status of an analyze process. Can be one of QUEUED|RUNNING|FAILED|SUCCESS|CANCELED|PAUSED.

### Filetype

Filetype of a document. Can be one of txt|pdf|doc|docx|rtf|odt|eml|msg.

### AnalyzeRequestType

Type of request for analyze. Can be one of background|immediate.

### AnalyzeRequestWebhook

Webhook to call to push updates from the analyze process.

### URI

Full URI string.

### Operation

Operation to perform on the analyze process.

### Timestamp

Timestamp

### Data

Raw text string.

### Total

Total number of records available within a collection query

### ProcessAvailable

Amount of processes available

### NameList

List of names.

### FiletypeConfiguration

### Encoding

Encoding of a document.

### DocumentFiletypeConfiguration

Filetype and configuration of a document.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) |  |  |
| config | [FiletypeConfiguration](#filetypeconfiguration) |  |  |

### TextDocument

Document raw text.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | [Data](#data) |  |  |

### Base64Document

Document serialized in base64 string.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | [Data](#data) |  |  |

### PrivateDocument

Document uploaded to the API.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) |  |  |

### PublicDocument

Document which is publicly available. Full URI must be given.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| uri | [URI](#uri) |  |  |

### Document

Data of a document to process. The filetype describes the type of document. See /filetype_configurations endpoint of pipeline-api to get a list of supported filetypes.
Optionally the encoding of the document can be given. If this is not set, the process will try to detect the encoding of the data.
To add data, set (only) one of the following fields: text, base64, private, public.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| filetype_configuration | [DocumentFiletypeConfiguration](#documentfiletypeconfiguration) | yes |  |
| encoding | [Encoding](#encoding) |  |  |
| text | [TextDocument](#textdocument) |  |  |
| base64 | [Base64Document](#base64document) |  |  |
| private | [PrivateDocument](#privatedocument) |  |  |
| public | [PublicDocument](#publicdocument) |  |  |

### AnalyzeRequestConfig

### AnalyzeRequest

All data related to an analyze process.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | [AnalyzeRequestType](#analyzerequesttype) | yes |  |
| flow_name | [Name](#name) | yes |  |
| config | [AnalyzeRequestConfig](#analyzerequestconfig) |  |  |
| webhook | [AnalyzeRequestWebhook](#analyzerequestwebhook) |  |  |
| document | [Document](#document) | yes |  |
| remote_id | [RemoteID](#remoteid) |  |  |
| error |  |  |  |

### AnalyzeOutput

### DocumentResponse

Response to a document upload. Contains the ID to refer to the document.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |

### StateResponse

All data regarding the state of the API.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| endpoint | [URI](#uri) | yes |  |
| process_available | [ProcessAvailable](#processavailable) | yes |  |
| flow_names | [NameList](#namelist) | yes |  |

### AnalyzeResponsePage

Analyze processes list. Contains the list that was fetched and the total.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [AnalyzeResponseList](#analyzeresponselist) |  |  |

### AnalyzeResponseList

### AnalyzeResponse

Analyze process data.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |
| remote_id | [RemoteID](#remoteid) |  |  |
| status | [Status](#status) |  |  |
| output | [AnalyzeOutput](#analyzeoutput) |  |  |
| error | [AnalyzeError](#analyzeerror) |  |  |
| timestamp | [Timestamp](#timestamp) |  |  |
| started_at | [Timestamp](#timestamp) |  |  |
| finished_at | [Timestamp](#timestamp) |  |  |

### UpdateAnalyzeRequestStatus

Update request to perform an operation on an analyze process.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| operation | [Operation](#operation) | yes |  |

### AnalyzeError

Error that occurred during an analyze process. Contains additional log.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | yes |  |
| log | string | yes |  |

### Error

API error.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | integer | yes |  |
| message | string | yes |  |

