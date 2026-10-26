# Pipeline API

The Pipeline API manages analysis pipelines that process documents and return structured results.

It provides a complete workflow for document analysis: configure authentication credentials, set up
connections to external data sources and destinations, define documents to analyze, optionally extract
text from binary documents, select analysis flows and plugins, and execute pipelines that orchestrate
the full process.

Key concepts:
- **Authentication Configurations** store credentials (basic, bearer, or Dynizer auth) used by connections.
- **Connections** define external services for sourcing document data or storing results, each with a type (see Connection Types).
- **Documents** hold or reference the data to be analyzed — as inline text/base64, private storage references, or public URIs.
- **Text Extraction** is an optional pre-processing step that converts binary documents (PDF, DOCX, etc.) into plain text via a registered extraction service before analysis. Enable it by setting `extract: true` on the pipeline configuration.
- **Flows** are the available analysis methods (e.g. `analyze`, `analyze_v2`). Each flow exposes a JSON Schema describing its configuration.
- **Plugins** run on the flow result once analysis completes and can expose their own configuration schema.
- **Pipeline Configurations** bundle a flow, plugins, extraction setting, destination connection, webhook, and other settings into a reusable template.
- **Pipelines** represent individual execution runs. A pipeline combines a configuration with a document, tracks status through its lifecycle (QUEUED, RUNNING, SUCCESS, FAILED, etc.), and stores the output. When extraction is enabled, the pipeline first extracts text, then sends the result to the analysis flow.

Authentication is handled via JWT bearer tokens obtained through the `/login` endpoint.


| Field | Value |
|-------|-------|
| Version | 1.1.0 |
| Contact | Consono <info@consono.ai> (https://consono.ai) |

## Tags

| Name | Description |
|------|-------------|
| Login | Obtain a JWT bearer token to authenticate subsequent API requests. |
| Authentication Configurations | Authentication configurations store credentials (basic, bearer, or Dynizer auth) used by connections to access external services. |
| Connections | Connections define external services that provide document data or serve as a destination for pipeline and plugin results. Each connection has a type (see Connection Types) and optionally references an authentication configuration. |
| Connectiontypes | Connection types describe the available types that can be assigned to a connection, and whether they support document sourcing, result storage, or both. |
| Filetype Configurations | Filetype configurations list the supported document filetypes and expose a JSON Schema describing the configuration options for each. |
| Documents | Documents store or reference the data to be analyzed in a pipeline. Data can be provided inline (text/base64), from private storage via a connection, or from a public URI. |
| Flows | Flows are the available analysis methods that can be executed in a pipeline (e.g. `analyze`, `analyze_v2`). Each flow exposes a JSON Schema describing its configuration options. |
| Pipeline Configurations | Pipeline configurations are reusable templates that bundle a flow, plugins, destination connection, webhook settings, and other parameters. They are referenced when executing a pipeline. |
| Pipelines | Pipelines represent individual execution runs. A pipeline combines a configuration with a document, progresses through lifecycle statuses (QUEUED, RUNNING, SUCCESS, FAILED, etc.), and stores the analysis output. |
| Plugins | Plugins are post-analysis processors that run on the flow result once analysis completes. Each plugin can expose a JSON Schema describing its configuration options. |
| Analyzers | Analyzers are the registered analysis services that process pipeline requests. They report their capacity, supported flows, and health status. |
| Extractors | Extractors are the registered text extraction services that pre-process documents before analysis. They report their capacity and supported file types. |
| Splitters | Splitters are the registered text splitting services that segment extracted text into smaller chunks before analysis. They report their capacity and health status. |
| Health check | Kubernetes-style health check endpoint for monitoring service availability. |

## Servers

| URL | Description |
|-----|-------------|
| `https://example.dynizer.com/pipeline-api/v1` | Example server |

## Endpoints

### `POST /login`

Tags: `Login`

Operation ID: `postLogin`

Send a login authentication request.


**Responses**

- `200`: Post login response body. — [LoginToken](#logintoken)
- `400`: Bad request. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /authentication_configurations`

Tags: `Authentication Configurations`

Operation ID: `getAuthenticationConfigurations`

Get all defined authentication configurations.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| search | query | [SearchString](#searchstring) | False | Search string to search within the collection. |
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |

**Responses**

- `200`: Get authentication configurations response body. — [GetAuthenticationConfigurations](#getauthenticationconfigurations)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /authentication_configurations`

Tags: `Authentication Configurations`

Operation ID: `postAuthenticationConfigurations`

Create a new authentication configuration.


**Responses**

- `200`: Create authentication configuration response body. — [CreateAuthenticationConfigurationResult](#createauthenticationconfigurationresult)
- `400`: Bad request. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /authentication_configurations/{id}`

Tags: `Authentication Configurations`

Operation ID: `getAuthenticationConfigurationByID`

Get an authentication configuration by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `200`: Get authentication configuration by ID response body. — [GetAuthenticationConfiguration](#getauthenticationconfiguration)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `PUT /authentication_configurations/{id}`

Tags: `Authentication Configurations`

Operation ID: `putAuthenticationConfigurationByID`

Update an authentication configuration by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Put authentication configuration response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `DELETE /authentication_configurations/{id}`

Tags: `Authentication Configurations`

Operation ID: `deleteAuthenticationConfigurationByID`

Delete an authentication configuration by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Delete authentication configuration response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `409`: Conflict. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /connections`

Tags: `Connections`

Operation ID: `getConnections`

Get all defined connections.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| search | query | [SearchString](#searchstring) | False | Search string to search within the collection. |
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |

**Responses**

- `200`: Get connection response body. — [GetConnections](#getconnections)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /connections`

Tags: `Connections`

Operation ID: `postConnections`

Create a new connection.


**Responses**

- `200`: Create connection response body. — [CreateConnectionResult](#createconnectionresult)
- `400`: Bad request. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /connections/{id}`

Tags: `Connections`

Operation ID: `getConnectionByID`

Get a connection by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `200`: Get connection by ID response body. — [GetConnection](#getconnection)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `PUT /connections/{id}`

Tags: `Connections`

Operation ID: `putConnectionByID`

Update a connection by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Put connection response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `DELETE /connections/{id}`

Tags: `Connections`

Operation ID: `deleteConnectionByID`

Delete a connection by ID. This operation will not delete any data on the storage itself.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Delete connection response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `409`: Conflict. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /connections/{id}/storage`

Tags: `Connections`

Operation ID: `getConnectionByIDStorage`

Download a large object from a connection. Specify the connection ID in the path parameter, and the server path in the query parameters.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |
| path | query | [URIPath](#uripath) | True | Server path to upload/download a large object. |

**Responses**

- `200`: Download large object response body.
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /connections/{id}/storage`

Tags: `Connections`

Operation ID: `postConnectionByIDStorage`

Upload a large object to a connection. Specify the connection ID in the path parameter, and the server path in the query parameters.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |
| path | query | [URIPath](#uripath) | True | Server path to upload/download a large object. |

**Responses**

- `200`: Upload large object response body. — [UploadLOB](#uploadlob)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `DELETE /connections/{id}/storage`

Tags: `Connections`

Operation ID: `deleteConnectionByIDStorage`

Delete a large object from a connection. Specify the connection ID in the path parameter, and the server path in the query parameters.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |
| path | query | [URIPath](#uripath) | True | Server path to upload/download a large object. |

**Responses**

- `204`: Delete large object response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /documents`

Tags: `Documents`

Operation ID: `getDocuments`

Get all defined documents.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| search | query | [SearchString](#searchstring) | False | Search string to search within the collection. |
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |

**Responses**

- `200`: Get documents response body. — [GetDocuments](#getdocuments)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /documents`

Tags: `Documents`

Operation ID: `postDocuments`

Create a new document.


**Responses**

- `200`: Create document response body. — [CreateDocumentResult](#createdocumentresult)
- `400`: Bad request. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /documents/{id}`

Tags: `Documents`

Operation ID: `getDocumentByID`

Get a document by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `200`: Get document by ID response body. — [GetDocument](#getdocument)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `PUT /documents/{id}`

Tags: `Documents`

Operation ID: `putDocumentByID`

Update a document by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Put document response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `DELETE /documents/{id}`

Tags: `Documents`

Operation ID: `deleteDocumentByID`

Delete a document by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Delete document response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `409`: Conflict. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /flows`

Tags: `Flows`

Operation ID: `getFlows`

Get all flows.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| search | query | [SearchString](#searchstring) | False | Search string to search within the collection. |
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |

**Responses**

- `200`: Get flows response body. — [GetFlows](#getflows)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /flows/{name}`

Tags: `Flows`

Operation ID: `getFlowByName`

Get a flow by Name.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| name | path | [Name](#name) | True | Name of object to fetch. |

**Responses**

- `200`: Get flow by Name response body. — [GetFlow](#getflow)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /filetype_configurations`

Tags: `Filetype Configurations`

Operation ID: `getFiletypeConfigurations`

Get all filetype configurations.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| search | query | [SearchString](#searchstring) | False | Search string to search within the collection. |
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |

**Responses**

- `200`: Get filetype configurations response body. — [GetFiletypeConfigurations](#getfiletypeconfigurations)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /filetype_configurations/{name}`

Tags: `Filetype Configurations`

Operation ID: `getFiletypeConfigurationByName`

Get a filetype configuration by name.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| name | path | [Name](#name) | True | Name of object to fetch. |

**Responses**

- `200`: Get filetype configuration by name response body. — [GetFiletypeConfiguration](#getfiletypeconfiguration)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /connectiontypes`

Tags: `Connectiontypes`

Operation ID: `getConnectiontypes`

Get all connectiontypes.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| search | query | [SearchString](#searchstring) | False | Search string to search within the collection. |
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |

**Responses**

- `200`: Get connectiontypes response body. — [GetConnectiontypes](#getconnectiontypes)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /connectiontypes/{name}`

Tags: `Connectiontypes`

Operation ID: `getConnectiontypeByName`

Get a connectiontype by Name.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| name | path | [Name](#name) | True | Name of object to fetch. |

**Responses**

- `200`: Get connectiontype by Name response body. — [GetConnectiontype](#getconnectiontype)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /pipeline_configurations`

Tags: `Pipeline Configurations`

Operation ID: `getPipelineConfigurations`

Get all defined pipeline configurations.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| search | query | [SearchString](#searchstring) | False | Search string to search within the collection. |
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |

**Responses**

- `200`: Get pipeline configurations response body. — [GetPipelineConfigurations](#getpipelineconfigurations)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /pipeline_configurations`

Tags: `Pipeline Configurations`

Operation ID: `postPipelineConfigurations`

Create a new pipeline configuration.


**Responses**

- `200`: Create pipeline configuration response body. — [CreatePipelineConfigurationResult](#createpipelineconfigurationresult)
- `400`: Bad request. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /pipeline_configurations/{id}`

Tags: `Pipeline Configurations`

Operation ID: `getPipelineConfigurationByID`

Get a pipeline configuration by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `200`: Get pipeline configuration by ID response body. — [GetPipelineConfiguration](#getpipelineconfiguration)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `PUT /pipeline_configurations/{id}`

Tags: `Pipeline Configurations`

Operation ID: `putPipelineConfigurationByID`

Update a pipeline configuration by ID. This update only applies to new pipelines and does not impact existing pipelines.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Put pipeline configuration response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `DELETE /pipeline_configurations/{id}`

Tags: `Pipeline Configurations`

Operation ID: `deletePipelineConfigurationByID`

Delete a pipeline configuration by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Delete pipeline configuration response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `409`: Conflict. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /pipelines`

Tags: `Pipelines`

Operation ID: `getPipelines`

Get all executed pipelines.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| search | query | [SearchString](#searchstring) | False | Search string to search within the collection. |
| status | query | [PipelineStatus](#pipelinestatus) | False | Status string to filter on pipeline status within the collection. |
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |
| include_output | query | [IncludeOutput](#includeoutput) | False | Flag to indicate whether to include the pipeline output. |
| include_document | query | [IncludeDocument](#includedocument) | False | Flag to indicate whether to include the pipeline document. |

**Responses**

- `200`: Get pipelines response body. — [GetPipelines](#getpipelines)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /pipelines`

Tags: `Pipelines`

Operation ID: `postPipelines`

Execute a new pipeline.


**Responses**

- `200`: Create pipeline response body. — [CreatePipelineResult](#createpipelineresult)
- `400`: Bad request. — [Error](#error)
- `503`: Service unavailable. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /pipelines/{id}`

Tags: `Pipelines`

Operation ID: `getPipelineByID`

Get a pipeline by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |
| include_output | query | [IncludeOutput](#includeoutput) | False | Flag to indicate whether to include the pipeline output. |
| include_document | query | [IncludeDocument](#includedocument) | False | Flag to indicate whether to include the pipeline document. |

**Responses**

- `200`: Get pipeline by ID response body. — [GetPipeline](#getpipeline)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `PUT /pipelines/{id}`

Tags: `Pipelines`

Operation ID: `putPipelineByID`

Update a pipeline by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Put pipeline response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `410`: Gone. — [Error](#error)
- `503`: Service unavailable. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `DELETE /pipelines/{id}`

Tags: `Pipelines`

Operation ID: `deletePipelineByID`

Delete a pipeline by ID.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Delete pipeline response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /pipelines/{id}/restart`

Tags: `Pipelines`

Operation ID: `postPipelinesByIDRestart`

Restart (a part of) a pipeline.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| id | path | [ID](#id) | True | ID of object to fetch. |

**Responses**

- `204`: Pipeline plugins execute response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `409`: Conflict. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /pipelines/filter`

Tags: `Pipelines`

Operation ID: `getFilteredPipelines`

Get the pipelines that meet the specified filter criteria.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| include_output | query | [IncludeOutput](#includeoutput) | False | Flag to indicate whether to include the pipeline output. |
| include_document | query | [IncludeDocument](#includedocument) | False | Flag to indicate whether to include the pipeline document. |

**Responses**

- `200`: Get pipelines response body. — [GetPipelines](#getpipelines)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /plugins`

Tags: `Plugins`

Operation ID: `getPlugins`

Get all configured plugins.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| search | query | [SearchString](#searchstring) | False | Search string to search within the collection. |
| limit | query | [Limit](#limit) | False | Defines how many records at max are returned.
If fewer records are available, all will be returned.
Omitting or setting this to -1 will be interpreted as no limit
 |
| offset | query | [Offset](#offset) | False | Defines the offset at which to start reading.
An offset of 0 means to start from the first possible record.
 |

**Responses**

- `200`: Get plugins response body. — [GetPlugins](#getplugins)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `POST /plugins`

Tags: `Plugins`

Operation ID: `postPlugins`

Create a new plugin.


**Responses**

- `204`: Post plugin response
- `400`: Bad request. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /plugins/{name}`

Tags: `Plugins`

Operation ID: `getPluginByName`

Get a plugin by name.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| name | path | [Name](#name) | True | Name of object to fetch. |

**Responses**

- `200`: Get plugin by name response body. — [GetPlugin](#getplugin)
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `PUT /plugins/{name}`

Tags: `Plugins`

Operation ID: `putPluginByName`

Update a plugin by Name.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| name | path | [Name](#name) | True | Name of object to fetch. |

**Responses**

- `204`: Put plugin response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `DELETE /plugins/{name}`

Tags: `Plugins`

Operation ID: `deletePluginByName`

Delete a plugin by name.


**Parameters**

| Name | In | Type | Required | Description |
|------|----|------|----------|-------------|
| name | path | [Name](#name) | True | Name of object to fetch. |

**Responses**

- `204`: Delete plugin response
- `400`: Bad request. — [Error](#error)
- `404`: Not found. — [Error](#error)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /analyzers`

Tags: `Analyzers`

Operation ID: `getAnalyzers`

Get all registered analyzers.


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

- `200`: Get analyzers response body. — [GetAnalyzers](#getanalyzers)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /extractors`

Tags: `Extractors`

Operation ID: `getExtractors`

Get all registered text extraction services.


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

- `200`: Get extractors response body. — [GetExtractors](#getextractors)
- `401`: Unauthorized. — [Error](#error)
- `default`: Unexpected error. — [Error](#error)

---

### `GET /splitters`

Tags: `Splitters`

Operation ID: `getSplitters`

Get all registered text splitting services.


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

- `200`: Get splitters response body. — [GetSplitters](#getsplitters)
- `401`: Unauthorized. — [Error](#error)
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

### 410ErrorResponse

Gone.

Content (`application/json`): [Error](#error)

### 503ErrorResponse

Service unavailable.

Content (`application/json`): [Error](#error)

### PostLoginResponse

Post login response body.

Content (`application/json`): [LoginToken](#logintoken)

### GetAuthenticationConfigurationByIDResponse

Get authentication configuration by ID response body.

Content (`application/json`): [GetAuthenticationConfiguration](#getauthenticationconfiguration)

### GetAuthenticationConfigurationsResponse

Get authentication configurations response body.

Content (`application/json`): [GetAuthenticationConfigurations](#getauthenticationconfigurations)

### CreateAuthenticationConfigurationResponse

Create authentication configuration response body.

Content (`application/json`): [CreateAuthenticationConfigurationResult](#createauthenticationconfigurationresult)

### GetConnectionByIDResponse

Get connection by ID response body.

Content (`application/json`): [GetConnection](#getconnection)

### GetConnectionsResponse

Get connection response body.

Content (`application/json`): [GetConnections](#getconnections)

### CreateConnectionResponse

Create connection response body.

Content (`application/json`): [CreateConnectionResult](#createconnectionresult)

### GetDocumentByIDResponse

Get document by ID response body.

Content (`application/json`): [GetDocument](#getdocument)

### GetDocumentsResponse

Get documents response body.

Content (`application/json`): [GetDocuments](#getdocuments)

### CreateDocumentResponse

Create document response body.

Content (`application/json`): [CreateDocumentResult](#createdocumentresult)

### GetFlowByNameResponse

Get flow by Name response body.

Content (`application/json`): [GetFlow](#getflow)

### GetFlowsResponse

Get flows response body.

Content (`application/json`): [GetFlows](#getflows)

### GetFiletypeConfigurationByNameResponse

Get filetype configuration by name response body.

Content (`application/json`): [GetFiletypeConfiguration](#getfiletypeconfiguration)

### GetFiletypeConfigurationsResponse

Get filetype configurations response body.

Content (`application/json`): [GetFiletypeConfigurations](#getfiletypeconfigurations)

### GetConnectiontypeByNameResponse

Get connectiontype by Name response body.

Content (`application/json`): [GetConnectiontype](#getconnectiontype)

### GetConnectiontypesResponse

Get connectiontypes response body.

Content (`application/json`): [GetConnectiontypes](#getconnectiontypes)

### GetPipelineConfigurationByIDResponse

Get pipeline configuration by ID response body.

Content (`application/json`): [GetPipelineConfiguration](#getpipelineconfiguration)

### GetPipelineConfigurationsResponse

Get pipeline configurations response body.

Content (`application/json`): [GetPipelineConfigurations](#getpipelineconfigurations)

### CreatePipelineConfigurationResponse

Create pipeline configuration response body.

Content (`application/json`): [CreatePipelineConfigurationResult](#createpipelineconfigurationresult)

### GetPipelineByIDResponse

Get pipeline by ID response body.

Content (`application/json`): [GetPipeline](#getpipeline)

### GetPipelinesResponse

Get pipelines response body.

Content (`application/json`): [GetPipelines](#getpipelines)

### CreatePipelineResponse

Create pipeline response body.

Content (`application/json`): [CreatePipelineResult](#createpipelineresult)

### GetPluginByNameResponse

Get plugin by name response body.

Content (`application/json`): [GetPlugin](#getplugin)

### GetPluginsResponse

Get plugins response body.

Content (`application/json`): [GetPlugins](#getplugins)

### GetAnalyzersResponse

Get analyzers response body.

Content (`application/json`): [GetAnalyzers](#getanalyzers)

### GetExtractorsResponse

Get extractors response body.

Content (`application/json`): [GetExtractors](#getextractors)

### GetSplittersResponse

Get splitters response body.

Content (`application/json`): [GetSplitters](#getsplitters)

### DownloadLOBResponse

Download large object response body.

### UploadLOBResponse

Upload large object response body.

Content (`application/json`): [UploadLOB](#uploadlob)


## Schemas

### Limit

Limits the amount of records to return.

### Offset

Offsets the records to return.

### ID

ID of an object within the collection.

### Name

Name of an object within the collection (searchable).

### SearchString

Search string to search for objects within a collection (by name).

### Data

Raw text string.

### Encoding

Encoding of a document.

### ExternalID

A client side ID that can be set to reference a document.

### URIPath

Path part of a URI.

### URI

Full URI string.

### Total

Total number of records available within a collection query

### User

User name.

### Password

User password

### Token

Authentication token

### ServiceToken

Service token to be used to login to Dynizer

### Host

hostname of a service

### Port

port of a service

### ProcessAvailable

Number of processes available

### MemoryAvailable

Amount of memory available

### ProcessQueued

Number of processes queued

### IncludeOutput

Include output data

### IncludeDocument

Include document

### NameList

List of names.

### Login

Login parameters. Currently only dynizer supported.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| dynizer | [DynizerAuth](#dynizerauth) | yes |  |

### LoginToken

Login response token.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| token | [Token](#token) | yes |  |

### BasicAuth

Basic authentication parameters. User and password.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user | [User](#user) | yes |  |
| password | [Password](#password) | yes |  |

### BearerAuth

Bearer authentication parameters. Token.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| token | [Token](#token) | yes |  |

### DynizerUserAuth

Dynizer user authentication parameters. User and password.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user | [User](#user) | yes |  |
| password | [Password](#password) | yes |  |

### DynizerServiceTokenAuth

Dynizer service token authentication parameters. Service token string.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| token | [ServiceToken](#servicetoken) | yes |  |

### DynizerAuth

Dynizer authentication parameters. Either a user and password or a service token.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user | [DynizerUserAuth](#dynizeruserauth) |  |  |
| service_token | [DynizerServiceTokenAuth](#dynizerservicetokenauth) |  |  |

### AuthenticationParameters

Authentication configuration parameters
Set (only) one of the supported methods: 'basic', 'bearer', 'dynizer'


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| basic | [BasicAuth](#basicauth) |  |  |
| bearer | [BearerAuth](#bearerauth) |  |  |
| dynizer | [DynizerAuth](#dynizerauth) |  |  |

### CreateAuthenticationConfiguration

Create authentication configuration request object. Contains a name and the authentication parameters to use.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| parameters | [AuthenticationParameters](#authenticationparameters) | yes |  |

### UpdateAuthenticationConfiguration

Update authentication configuration request object. Both the name as well as the authentication parameters can be updated


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) |  |  |
| parameters | [AuthenticationParameters](#authenticationparameters) |  |  |

### CreateAuthenticationConfigurationResult

Create authentication configuration response object. Contains a unique ID to refer to the configuration.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |

### GetAuthenticationConfigurations

Get authentication configuration response object. A list of authentication configurations along with the total number that can be returned.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [GetAuthenticationConfigurationsList](#getauthenticationconfigurationslist) |  |  |

### GetAuthenticationConfigurationsList

List of authentication configurations.

### GetAuthenticationConfiguration

Get authentication configuration response object. Contains the ID along with the configured name and authentication parameters.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |
| name | [Name](#name) | yes |  |
| parameters | [AuthenticationParameters](#authenticationparameters) | yes |  |

### ConnectionParameters

Connection parameters.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| host | [Host](#host) | yes |  |
| port | [Port](#port) | yes |  |
| authentication_configuration_id | [ID](#id) |  |  |

### CreateConnection

Create connection request object. Contains a name, type and the authentication parameters to use. Use /connectiontypes to get a list of supported connection types.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| type_name | [Name](#name) | yes |  |
| parameters | [ConnectionParameters](#connectionparameters) | yes |  |

### UpdateConnection

Update connection request object. Both the name, type as well as the connection parameters can be updated. Use /connectiontypes to get a list of supported connection types.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) |  |  |
| type_name | [Name](#name) |  |  |
| parameters | [ConnectionParameters](#connectionparameters) |  |  |

### CreateConnectionResult

Create connection response object. Contains a unique ID to refer to the connection.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |

### GetConnections

Get connection response object. A list of connections along with the total number that can be returned.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [GetConnectionsList](#getconnectionslist) |  |  |

### GetConnectionsList

List of connections.

### GetConnection

Get connection response object. Contains the ID along with the configured name, type and connection parameters. Use /connectiontypes to get a list of supported connection types.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |
| name | [Name](#name) | yes |  |
| type_name | [Name](#name) | yes |  |
| parameters | [ConnectionParameters](#connectionparameters) | yes |  |

### TextDocument

Document raw text

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | [Data](#data) | yes |  |

### Base64Document

Document serialized in base64 string

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | [Data](#data) | yes |  |

### PrivateDocument

Document stored in a private storage. Needs a **Connection** defined to store the parameters on where to reach the storage, and a path to the file on that storage.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| path | [URIPath](#uripath) | yes |  |
| connection_id | [ID](#id) | yes |  |

### PublicDocument

Document which is publicly available. Full URI must be given.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| uri | [URI](#uri) | yes |  |

### FiletypeConfiguration

Dynamic configuration for a filetype. The schema depends on the selected filetype. Call /filetype_configurations to retrieve the JSON Schema for each supported filetype.

### FlowConfiguration

Dynamic configuration for a flow. The schema depends on the selected flow. Call /flows to retrieve the JSON Schema for each supported flow.

### PluginConfiguration

Dynamic configuration for a plugin. The schema depends on the selected plugin. Call /plugins to retrieve the JSON Schema for each supported plugin.

### DocumentFiletypeConfiguration

Filetype and configuration of a document

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| config | [FiletypeConfiguration](#filetypeconfiguration) |  |  |

### Document

Data to store for the document. The filetype describes the type of document. Call /filetype_configurations endpoint to get a list of supported filetypes.
Optionally the encoding of the document can be given. If this is not set, the process will try to detect the encoding of the data.
To add data, set (only) one of the following fields: text, base64, private, public.
In case the data is passed on as 'text' or 'base64', it is not stored permanently and cannot be accessed again.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| filetype_configuration | [DocumentFiletypeConfiguration](#documentfiletypeconfiguration) | yes |  |
| encoding | [Encoding](#encoding) |  |  |
| text | [TextDocument](#textdocument) |  |  |
| base64 | [Base64Document](#base64document) |  |  |
| private | [PrivateDocument](#privatedocument) |  |  |
| public | [PublicDocument](#publicdocument) |  |  |
| external_id | [ExternalID](#externalid) |  |  |

### CreateDocument

Create document request object. Contains a name and the document data.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| document | [Document](#document) | yes |  |

### CreateDocumentResult

Create document response object. Contains a unique ID to refer to the document.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |

### GetDocuments

Get documents response object. A list of documents along with the total number of documents that can be returned.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [GetDocumentsList](#getdocumentslist) |  |  |

### GetDocumentsList

List of documents.

### GetDocument

Get document response object. Contains the ID along with the configured name and document.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |
| name | [Name](#name) | yes |  |
| document | [Document](#document) | yes |  |

### UpdateDocument

Update document request object. Both name and document can be updated.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) |  |  |
| document | [Document](#document) |  |  |

### GetFlows

Get flows response object. A list of flows along with the total number of flows that can be returned.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [GetFlowsList](#getflowslist) |  |  |

### GetFlowsList

List of flows.

### GetFlow

Get flow response object. Contains the name of the flow and a JSON Schema of the flow config.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| config_model | [JSONSchema](#jsonschema) | yes |  |

### GetFiletypeConfigurations

Get filetype configurations response object. A list of filetype configurations along with the total number that can be returned.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [GetFiletypeConfigurationsList](#getfiletypeconfigurationslist) |  |  |

### GetFiletypeConfigurationsList

List of filetype configurations.

### GetFiletypeConfiguration

Get filetype configuration response object. Contains the name of the filetype and a JSON Schema of the filetype config.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| config_model | [JSONSchema](#jsonschema) | yes |  |

### GetConnectiontypes

Get connectiontypes response object. A list of connectiontypes along with the total number of connectiontypes that can be returned.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [GetConnectiontypesList](#getconnectiontypeslist) |  |  |

### GetConnectiontypesList

List of connectiontypes.

### DocumentSupport

Wether the connection can be used to refer documents.

### DestinationSupport

Wether the connection can be used to store the output of the pipeline and plugins.

### GetConnectiontype

Get connectiontype response object. Contains the name of the connectiontype and whether it is a document and/or destination connection.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| document_support | [DocumentSupport](#documentsupport) | yes |  |
| destination_support | [DestinationSupport](#destinationsupport) | yes |  |

### FlowPlugin

Plugin to execute on the flow result once it has been completed.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| config | [PluginConfiguration](#pluginconfiguration) |  |  |

### FlowPluginsList

List of flow plugins.

### PipelineFlowConfiguration

Flow configuration of a pipeline

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| config | [FlowConfiguration](#flowconfiguration) |  |  |

### CreatePipelineConfiguration

Create pipeline configuration request object. Contains a name, the flow, config and plugin(s) to execute, the Dynizer connection to store the result, webhook configuration and a client ID.
Each field except 'name' can be omitted. In case fields connection_id or flow_configuration are empty, they will have to be provided when starting the pipeline.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| connection_id | [ID](#id) |  |  |
| extract | boolean |  | When true, pipeline-api will extract text from the document via a registered extraction service before sending to analyze-api.
When false or omitted (default), the binary document is sent directly to analyze-api (legacy behavior).
 |
| split | boolean |  | When true, pipeline-api will split the extracted text into sentence-sized segments via a registered split service before sending to analyze-api.
When false or omitted (default), the full text is sent directly to analyze-api.
 |
| flow_configuration | [PipelineFlowConfiguration](#pipelineflowconfiguration) |  |  |
| plugins | [FlowPluginsList](#flowpluginslist) |  |  |
| instance | [Instance](#instance) |  |  |
| webhook | [Webhook](#webhook) |  |  |
| client_id | [ClientID](#clientid) |  |  |

### CreatePipelineConfigurationResult

Create pipeline configuration response object. Contains a unique ID to refer to the pipeline configuration.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |

### GetPipelineConfigurations

Get pipeline configurations response object. A list of pipeline configurations along with the total number of configurations that can be returned.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [GetPipelineConfigurationsList](#getpipelineconfigurationslist) |  |  |

### GetPipelineConfigurationsList

List of pipeline configurations.

### GetPipelineConfiguration

Get pipeline configuration response object. Contains the ID along with the configured name, flow, config, plugins, connection, instance, webhook and client ID.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |
| name | [Name](#name) | yes |  |
| connection_id | [ID](#id) |  |  |
| extract | boolean |  | When true, pipeline-api will extract text from the document via a registered extraction service before sending to analyze-api.
 |
| split | boolean |  | When true, pipeline-api will split the text into segments before sending to analyze-api.
 |
| flow_configuration | [PipelineFlowConfiguration](#pipelineflowconfiguration) |  |  |
| plugins | [FlowPluginsList](#flowpluginslist) |  |  |
| instance | [Instance](#instance) |  |  |
| webhook | [Webhook](#webhook) |  |  |
| client_id | [ClientID](#clientid) |  |  |

### UpdatePipelineConfiguration

Update pipeline configuration request object. The name, flow, config, plugins, connection, instance, webhook and client ID can be updated.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) |  |  |
| connection_id | [ID](#id) |  |  |
| extract | boolean |  | When true, pipeline-api will extract text from the document via a registered extraction service before sending to analyze-api.
When false or omitted (default), the binary document is sent directly to analyze-api (legacy behavior).
 |
| split | boolean |  | When true, pipeline-api will split the text into segments before sending to analyze-api.
When false or omitted (default), the full text is sent directly to analyze-api.
 |
| flow_configuration | [PipelineFlowConfiguration](#pipelineflowconfiguration) |  |  |
| plugins | [FlowPluginsList](#flowpluginslist) |  |  |
| instance | [Instance](#instance) |  |  |
| webhook | [Webhook](#webhook) |  |  |
| client_id | [ClientID](#clientid) |  |  |

### CreatePipeline

Execute pipeline request object. Set the 'configuration_id' field to the pipeline configuration ID to execute.
Additionally, 'configuration' can be set to override any parameters from the pipeline configuration. The configurations will be merged before execution.
It is allowed to omit the 'configuration_id' and pass a full config in the 'configuration' field.
Either the document ID can be set in the 'document_id' field to refer to a previously configured document, or a full document can be passed in the 'document' field.
In the case a full document is given, it will not be stored and available via the /documents endpoint.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| configuration_id | [ID](#id) |  |  |
| configuration | [CreatePipelineConfiguration](#createpipelineconfiguration) |  |  |
| document_id | [ID](#id) |  |  |
| document | [Document](#document) |  |  |

### GetFilteredPipelines

A request object used for retrieving pipelines based on specific filtering criteria.
Use the 'client_ids' property to retrieve only those pipelines associated with any of the specified client IDs.
No pipelines will be returned if client_ids is not given or empty.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client_ids | [ClientIDs](#clientids) |  |  |

### Webhook

Webhook configuration object. Optionally configure a webhook that will be called on status updates.
The endpoint will be called with method POST. The body contains the pipeline ID and status.
The provided endpoint should be reachable without authentication by the API and should return HTTP 200 when succesfully handled.
If the endpoint is unreachable or returns a status code that is not HTTP 200, the API will retry the webhook up until a maximum of 10 times with an increasing timeout.
The receiving webhook handler should always fetch the pipeline by its ID to be sure the incoming request and/or data is valid.
The status is only informative to be able to discard updates that aren't relevant to an implementation, but should only be used for this purpose.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| endpoint | [URI](#uri) | yes |  |

### PipelineRestart

Restart pipeline request object. Contains optional plugin(s) to execute, instance to write as metadata, webhook configuration and a client ID.
All options will overwite the current stored values of the pipeline. If the options are not given, the run will use the original values for these fields.
Setting flag 'reanalyze' to 'true' reanalyzes the document and clears the output. If 'false', only the plugins are executed.
The 'clear_data' flag causes plugins to erase all data, if supported, before they are restarted. Data is cleared from the current configured plugins, not the new ones passed in the body (if there are any).
The pipeline's status, start and finish times are reset.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| reanalyze | [Reanalyze](#reanalyze) |  |  |
| clear_data | [ClearData](#cleardata) |  |  |
| plugins | [FlowPluginsList](#flowpluginslist) |  |  |
| instance | [Instance](#instance) |  |  |
| webhook | [Webhook](#webhook) |  |  |
| client_id | [ClientID](#clientid) |  |  |

### Reanalyze

Wether to reanalyze the result

### ClearData

Wether to clear the data generated by the plugins (if the plugin supports it)

### ClearPlugins

Wether to clear all the plugins (empty array does no changes)

### ClientIDs

List of client IDs.

### ClientID

Optional ID for client side verification

### Timestamp

Timestamp in RFC 3339 format (e.g. 2024-01-15T09:30:00Z).

### PipelineStatus

The status the pipeline is currently in.


Enum values: ['QUEUED_LOCAL', 'QUEUED', 'RUNNING', 'FAILED', 'SUCCESS', 'CANCELED', 'PAUSED']

### PipelineStep

A pipeline step. Contains data about the start/end time and the status it is currently in


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| started_at | [Timestamp](#timestamp) | yes |  |
| finished_at | [Timestamp](#timestamp) |  |  |
| status | [PipelineStatus](#pipelinestatus) | yes |  |

### PipelineSteps

The pipeline individual steps'

### PipelineInfo

Info of a pipeline. Contains data about the start/end time, status/step it is currently in and additional error info if the pipeline failed.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| requested_at | [Timestamp](#timestamp) |  |  |
| started_at | [Timestamp](#timestamp) |  |  |
| finished_at | [Timestamp](#timestamp) |  |  |
| status | [PipelineStatus](#pipelinestatus) | yes |  |
| steps | [PipelineSteps](#pipelinesteps) |  |  |
| error | [PipelineError](#pipelineerror) |  |  |

### PipelineError

Pipeline error information

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | [PipelineErrorMessage](#pipelineerrormessage) | yes |  |
| log | [PipelineErrorLog](#pipelineerrorlog) |  |  |

### PipelineErrorMessage

Pipeline error message

### PipelineErrorLog

Pipeline error log

### CreatePipelineResult

Execute pipeline response object. Contains a unique ID to refer to the pipeline and an info object describing the current status of the pipeline.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |
| info | [PipelineInfo](#pipelineinfo) | yes |  |

### GetPipelines

Get pipelines response object. A list of pipelines along with the total number of pipelines that can be returned.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [GetPipelinesList](#getpipelineslist) |  |  |

### GetPipelinesList

List of pipelines.

### GetPipeline

Get pipeline response object. Contains the ID along with the status, configuration and document of the pipeline run.
Optionally contains the output of the the pipeline, if there is any.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | [ID](#id) | yes |  |
| configuration_id | [ID](#id) |  |  |
| configuration | [CreatePipelineConfiguration](#createpipelineconfiguration) |  |  |
| info | [PipelineInfo](#pipelineinfo) | yes |  |
| document_id | [ID](#id) |  |  |
| document | [GetDocument](#getdocument) |  |  |
| output | [PipelineOutput](#pipelineoutput) |  |  |

### PipelineOutput

The output produced by the pipeline analysis. The structure depends on the flow and plugins used.

### Operation

The operation to execute on the pipeline update.

Enum values: ['CANCEL', 'PAUSE', 'RESUME']

### UpdatePipeline

Update pipeline request object. The following operations are supported: CANCEL, PAUSE, RESUME.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| operation | [Operation](#operation) | yes |  |

### DockerRepository

The docker repository of the plugin container

### DockerImageTag

The docker image tag of the plugin container

### CreatePlugin

Create a plugin. Contains a name, the docker repository and image tag, documentation URL and an icon URL. The name of the plugin must be unique.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) | yes |  |
| docker_repository | [DockerRepository](#dockerrepository) | yes |  |
| docker_image_tag | [DockerImageTag](#dockerimagetag) | yes |  |
| documentation_url | [URI](#uri) |  |  |
| icon | [URI](#uri) |  |  |

### GetPlugins

Get plugins response object. A list of plugins along with the total number that can be returned.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total | [Total](#total) | yes |  |
| records | [GetPluginsList](#getpluginslist) |  |  |

### GetPluginsList

List of plugins.

### GetPlugin

Get plugin response object. Contains the name along with the configuration.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) |  |  |
| docker_repository | [DockerRepository](#dockerrepository) |  |  |
| docker_image_tag | [DockerImageTag](#dockerimagetag) |  |  |
| documentation_url | [URI](#uri) |  |  |
| icon | [URI](#uri) |  |  |
| config_model | [JSONSchema](#jsonschema) |  |  |

### UpdatePlugin

Update plugin request object.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | [Name](#name) |  |  |
| docker_repository | [DockerRepository](#dockerrepository) |  |  |
| docker_image_tag | [DockerImageTag](#dockerimagetag) |  |  |
| documentation_url | [URI](#uri) |  |  |
| icon | [URI](#uri) |  |  |

### GetAnalyzers

Get analyzers response object. A list of registered analyzers.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| records | [GetAnalyzerList](#getanalyzerlist) |  |  |

### GetAnalyzerList

### GetAnalyzer

A registered Analyzer. Contains the endpoint of the analyzer, how much processes are available and the flow names it supports.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| endpoint | [URI](#uri) | yes |  |
| process_available | [ProcessAvailable](#processavailable) | yes |  |
| memory_available | [MemoryAvailable](#memoryavailable) | yes |  |
| process_queued | [ProcessQueued](#processqueued) | yes |  |
| flow_names | [NameList](#namelist) | yes |  |
| updated_at | [Timestamp](#timestamp) | yes |  |

### GetExtractors

Get extractors response object. A list of registered text extraction services.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| records | [GetExtractorList](#getextractorlist) |  |  |

### GetExtractorList

### GetExtractor

A registered text extraction service. Contains the endpoint, available processes, and supported file types.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| endpoint | [URI](#uri) | yes |  |
| process_available | [ProcessAvailable](#processavailable) | yes |  |
| memory_available | [MemoryAvailable](#memoryavailable) | yes |  |
| process_queued | [ProcessQueued](#processqueued) | yes |  |
| supported_filetypes | [NameList](#namelist) | yes |  |
| updated_at | [Timestamp](#timestamp) | yes |  |

### GetSplitters

Get splitters response object. A list of registered text splitting services.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| records | [GetSplitterList](#getsplitterlist) |  |  |

### GetSplitterList

### GetSplitter

A registered text splitting service. Contains the endpoint, available processes, and health status.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| endpoint | [URI](#uri) | yes |  |
| process_available | [ProcessAvailable](#processavailable) | yes |  |
| memory_available | [MemoryAvailable](#memoryavailable) | yes |  |
| process_queued | [ProcessQueued](#processqueued) | yes |  |
| updated_at | [Timestamp](#timestamp) | yes |  |

### UploadLOB

Result information about an uploaded large object.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| path | [URIPath](#uripath) | yes |  |

### JSONSchemaID

The $id keyword defines a URI for the schema, and the base URI that other URI references within the schema are resolved against.


### JSONSchemaSchema

The $schema keyword states that this schema is written according to a specific draft of the standard and used for a variety of reasons, primarily version control.


### JSONSchemaTitle

The title and description annotation keywords are descriptive only. They do not add constraints to the data being validated. The intent of the schema is stated with these two keywords.


### JSONSchemaDescription

The title and description annotation keywords are descriptive only. They do not add constraints to the data being validated. The intent of the schema is stated with these two keywords.


### JSONSchemaType

The type validation keyword defines the first constraint on our JSON data.


### JSONSchemaRequired

### JSONSchemaProperties

JSON Schema properties object. Each key is a property name and its value is a JSON Schema describing that property.

### JSONSchema

JSON Schema definition

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| $id | [JSONSchemaID](#jsonschemaid) | yes |  |
| $schema | [JSONSchemaSchema](#jsonschemaschema) | yes |  |
| title | [JSONSchemaTitle](#jsonschematitle) |  |  |
| description | [JSONSchemaDescription](#jsonschemadescription) |  |  |
| type | [JSONSchemaType](#jsonschematype) | yes |  |
| required | [JSONSchemaRequired](#jsonschemarequired) |  |  |
| properties | [JSONSchemaProperties](#jsonschemaproperties) | yes |  |

### Instance

Setting this will add these static values to the resulting instances.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| instance_elements | [InstanceElements](#instanceelements) | yes |  |

### InstanceElements

A list of Dynizer instance elements

### InstanceElement

A Dynizer instance element. Both the deprecated misspelled fields (min_occurence, max_occurence) and the
correctly spelled fields (min_occurrence, max_occurrence) are accepted. If both variants are provided,
they must have the same value or a 400 error is returned.


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| action_label | [ActionLabel](#actionlabel) | yes |  |
| component | [Component](#component) | yes |  |
| default_data_type | [DataType](#datatype) | yes |  |
| specs | [Specs](#specs) | yes |  |
| min_occurence | [MinOccurence](#minoccurence) |  |  |
| max_occurence | [MaxOccurence](#maxoccurence) |  |  |
| min_occurrence | [MinOccurrence](#minoccurrence) |  |  |
| max_occurrence | [MaxOccurrence](#maxoccurrence) |  |  |
| values | [InstanceValues](#instancevalues) | yes |  |

### MinOccurence

Deprecated: Use min_occurrence instead. Amount of values that have to occur for a dynizer action label.

### MaxOccurence

Deprecated: Use max_occurrence instead. Amount of values that may occur for a dynizer action label.

### MinOccurrence

Amount of values that have to occur for a dynizer action label.

### MaxOccurrence

Amount of values that may occur for a dynizer action label.

### Specs

A list of value specs.

### Position

A position of a Dynizer action label.

### Spec

Spec of a value. Contains the position of the value and a datatype/format pair.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| position | [Position](#position) |  |  |
| override | [DataTypeFormat](#datatypeformat) |  |  |

### DataTypeFormat

Datatype and/or format of a value

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data_type | [DataType](#datatype) |  |  |
| format | [Format](#format) |  |  |

### DataType

A datatype of a Dynizer action label.

### Format

A format string of a Dynizer instance value.

### Component

A component of a Dynizer action label.

### InstanceValues

A list of dynizer instance values.

### ActionLabel

A label within a Dynizer instance.

### InstanceValue

A value within a Dynizer instance.

### Error

API error.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | integer | yes |  |
| message | string | yes |  |

