# split-service

Sentence/clause splitting analyzer for pipeline-api (the `split` flow).

A pre-processing step modelled on text extraction: pipeline-api calls `POST /split` once with `{document, webhook, remote_id}`; the service acks `{id}`, sentencizes on a Celery worker, and POSTs `{id, remote_id, status, segments}` to the `webhook` URL. Single-call and async. Inbound auth was removed — reached only over the internal network. Designed as the split step in `Extract -> Split -> Analyze -> Plugins`; see `docs/verify_pipeline_chaining.md`.

## APIs

### Endpoint: /healthz

`GET /healthz`



  

**Responses**

+ `200`: 
        [HealthCheckResponse](#healthcheckresponse)

    
 
  
 
### Endpoint: /state

`GET /state`



  

**Responses**

+ `200`: 
        [StateInfoResponse](#stateinforesponse)

    
 
  
 
### Endpoint: /split

`POST /split`



  

**Responses**

+ `200`: 
        [SplitAcceptedResponse](#splitacceptedresponse)

    
 
+ `400`: 
        [NoUsableTextResponse](#nousabletextresponse)

    
 
+ `422`: 
        [ValidationErrorResponse](#validationerrorresponse)

    
 
  
 
---

# Components

## HealthCheckResponse


Successful Response




### application/json
schema:

  
  [HealthResponse](#healthresponse)
















## ErrorResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | string | string |

## HTTPValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | array | array |

## HealthResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| status | string | string |
| flow_name | string | string |
| backend | string | string |

## SegmentModel



| Field | Type | Schema Reference |
|-------|------|------------------|
| index | integer | integer |
| text | string | string |
| start | integer | integer |
| end | integer | integer |

## SplitRequest


A split dispatch, e.g.::

    {"document": {"text": {"data": "<text>"}},
     "webhook": "http://pipeline-api:50052/webhooks/split",
     "remote_id": "<pipeline-id>"}

Inline ``text`` and a few common document keys are also accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  |  |
| text |  |  |
| webhook |  |  |
| remote_id |  |  |
| config | object | object |

## SplitResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |

## StateResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| flow_names | array | array |
| backend | string | string |

## ValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| loc | array | array |
| msg | string | string |
| type | string | string |
| input |  |  |
| ctx | object | object |

## WebhookResult


The split result POSTed to the caller's webhook (doc-only model).


| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |
| remote_id |  |  |
| status | string | string |
| segments |  |  |
| metadata |  |  |
| error |  |  |
| log |  |  |
## StateInfoResponse


Successful Response




### application/json
schema:

  
  [StateResponse](#stateresponse)
















## ErrorResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | string | string |

## HTTPValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | array | array |

## HealthResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| status | string | string |
| flow_name | string | string |
| backend | string | string |

## SegmentModel



| Field | Type | Schema Reference |
|-------|------|------------------|
| index | integer | integer |
| text | string | string |
| start | integer | integer |
| end | integer | integer |

## SplitRequest


A split dispatch, e.g.::

    {"document": {"text": {"data": "<text>"}},
     "webhook": "http://pipeline-api:50052/webhooks/split",
     "remote_id": "<pipeline-id>"}

Inline ``text`` and a few common document keys are also accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  |  |
| text |  |  |
| webhook |  |  |
| remote_id |  |  |
| config | object | object |

## SplitResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |

## StateResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| flow_names | array | array |
| backend | string | string |

## ValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| loc | array | array |
| msg | string | string |
| type | string | string |
| input |  |  |
| ctx | object | object |

## WebhookResult


The split result POSTed to the caller's webhook (doc-only model).


| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |
| remote_id |  |  |
| status | string | string |
| segments |  |  |
| metadata |  |  |
| error |  |  |
| log |  |  |
## SplitAcceptedResponse


Successful Response




### application/json
schema:

  
  [SplitResponse](#splitresponse)
















## ErrorResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | string | string |

## HTTPValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | array | array |

## HealthResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| status | string | string |
| flow_name | string | string |
| backend | string | string |

## SegmentModel



| Field | Type | Schema Reference |
|-------|------|------------------|
| index | integer | integer |
| text | string | string |
| start | integer | integer |
| end | integer | integer |

## SplitRequest


A split dispatch, e.g.::

    {"document": {"text": {"data": "<text>"}},
     "webhook": "http://pipeline-api:50052/webhooks/split",
     "remote_id": "<pipeline-id>"}

Inline ``text`` and a few common document keys are also accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  |  |
| text |  |  |
| webhook |  |  |
| remote_id |  |  |
| config | object | object |

## SplitResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |

## StateResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| flow_names | array | array |
| backend | string | string |

## ValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| loc | array | array |
| msg | string | string |
| type | string | string |
| input |  |  |
| ctx | object | object |

## WebhookResult


The split result POSTed to the caller's webhook (doc-only model).


| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |
| remote_id |  |  |
| status | string | string |
| segments |  |  |
| metadata |  |  |
| error |  |  |
| log |  |  |
## WebhookDeliveredResponse


Successful Response




### application/json
schema:

  
  [WebhookResult](#webhookresult)
















## ErrorResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | string | string |

## HTTPValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | array | array |

## HealthResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| status | string | string |
| flow_name | string | string |
| backend | string | string |

## SegmentModel



| Field | Type | Schema Reference |
|-------|------|------------------|
| index | integer | integer |
| text | string | string |
| start | integer | integer |
| end | integer | integer |

## SplitRequest


A split dispatch, e.g.::

    {"document": {"text": {"data": "<text>"}},
     "webhook": "http://pipeline-api:50052/webhooks/split",
     "remote_id": "<pipeline-id>"}

Inline ``text`` and a few common document keys are also accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  |  |
| text |  |  |
| webhook |  |  |
| remote_id |  |  |
| config | object | object |

## SplitResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |

## StateResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| flow_names | array | array |
| backend | string | string |

## ValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| loc | array | array |
| msg | string | string |
| type | string | string |
| input |  |  |
| ctx | object | object |

## WebhookResult


The split result POSTed to the caller's webhook (doc-only model).


| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |
| remote_id |  |  |
| status | string | string |
| segments |  |  |
| metadata |  |  |
| error |  |  |
| log |  |  |
## NoUsableTextResponse


No usable document text.




### application/json
schema:

  
  [ErrorResponse](#errorresponse)
















## ErrorResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | string | string |

## HTTPValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | array | array |

## HealthResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| status | string | string |
| flow_name | string | string |
| backend | string | string |

## SegmentModel



| Field | Type | Schema Reference |
|-------|------|------------------|
| index | integer | integer |
| text | string | string |
| start | integer | integer |
| end | integer | integer |

## SplitRequest


A split dispatch, e.g.::

    {"document": {"text": {"data": "<text>"}},
     "webhook": "http://pipeline-api:50052/webhooks/split",
     "remote_id": "<pipeline-id>"}

Inline ``text`` and a few common document keys are also accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  |  |
| text |  |  |
| webhook |  |  |
| remote_id |  |  |
| config | object | object |

## SplitResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |

## StateResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| flow_names | array | array |
| backend | string | string |

## ValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| loc | array | array |
| msg | string | string |
| type | string | string |
| input |  |  |
| ctx | object | object |

## WebhookResult


The split result POSTed to the caller's webhook (doc-only model).


| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |
| remote_id |  |  |
| status | string | string |
| segments |  |  |
| metadata |  |  |
| error |  |  |
| log |  |  |
## ValidationErrorResponse


Validation Error




### application/json
schema:

  
  [HTTPValidationError](#httpvalidationerror)
















## ErrorResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | string | string |

## HTTPValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| detail | array | array |

## HealthResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| status | string | string |
| flow_name | string | string |
| backend | string | string |

## SegmentModel



| Field | Type | Schema Reference |
|-------|------|------------------|
| index | integer | integer |
| text | string | string |
| start | integer | integer |
| end | integer | integer |

## SplitRequest


A split dispatch, e.g.::

    {"document": {"text": {"data": "<text>"}},
     "webhook": "http://pipeline-api:50052/webhooks/split",
     "remote_id": "<pipeline-id>"}

Inline ``text`` and a few common document keys are also accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  |  |
| text |  |  |
| webhook |  |  |
| remote_id |  |  |
| config | object | object |

## SplitResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |

## StateResponse



| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| flow_names | array | array |
| backend | string | string |

## ValidationError



| Field | Type | Schema Reference |
|-------|------|------------------|
| loc | array | array |
| msg | string | string |
| type | string | string |
| input |  |  |
| ctx | object | object |

## WebhookResult


The split result POSTed to the caller's webhook (doc-only model).


| Field | Type | Schema Reference |
|-------|------|------------------|
| id | string | string |
| remote_id |  |  |
| status | string | string |
| segments |  |  |
| metadata |  |  |
| error |  |  |
| log |  |  |
