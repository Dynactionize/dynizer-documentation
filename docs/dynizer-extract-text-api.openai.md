# Extract Text API

Apache Tika wrapper API for text extraction

## Authentication



## Security Schemes

| Name              | Type              | Description              | Scheme              | Bearer Format             |
|-------------------|-------------------|--------------------------|---------------------|---------------------------|
| bearerAuth | http |  | bearer | JWT |

## APIs

### Endpoint: /extract

`POST /extract`

Submit a document for text extraction


  

**Responses**

+ `202`: 
        [PostExtractResponse](#postextractresponse)

    
 
+ `400`: 
        [400ErrorResponse](#400errorresponse)

    
 
+ `503`: 
        [503ErrorResponse](#503errorresponse)

    
 
+ `default`: 
        [DefaultErrorResponse](#defaulterrorresponse)

    
 
  
 
### Endpoint: /state

`GET /state`

Get state of the extract-text-api


  

**Responses**

+ `200`: 
        [GetStateResponse](#getstateresponse)

    
 
+ `default`: 
        [DefaultErrorResponse](#defaulterrorresponse)

    
 
  
 
### Endpoint: /healthz

`GET /healthz`

k8s style health check. Returns 200 if running correctly



  

**Responses**

+ `200`: 
        

    
 
+ `503`: 
        [503ErrorResponse](#503errorresponse)

    
 
+ `default`: 
        [DefaultErrorResponse](#defaulterrorresponse)

    
 
  
 
---

# Components

## DefaultErrorResponse


Unexpected error.




### application/json
schema:

  
  [Error](#error)
















## ID


ID of an object.



## RemoteID


Remote ID from the API that requested the extraction.



## Status


Status of an extraction. Can be one of QUEUED|RUNNING|FAILED|SUCCESS.



## Filetype


Filetype of the document.



## FiletypeConfig




## Base64Document


Document serialized in base64 string.


| Field | Type | Schema Reference |
|-------|------|------------------|
| data | string | string |

## Document


Document to extract text from.


| Field | Type | Schema Reference |
|-------|------|------------------|
| filetype |  | [Filetype](#filetype) |
| filetype_config |  | [FiletypeConfig](#filetypeconfig) |
| base64 |  | [Base64Document](#base64document) |

## ExtractRequest


Request to extract text from a document.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  | [Document](#document) |
| webhook | string | string |
| remote_id |  | [RemoteID](#remoteid) |

## ExtractAcceptedResponse


Response when an extraction request is accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| id |  | [ID](#id) |
| status |  | [Status](#status) |

## ExtractMetadata


Metadata extracted from the document.



## StateResponse


All data regarding the state of the API.


| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| supported_filetypes | array | array |
| tika_endpoint | string | string |

## Error


API error.


| Field | Type | Schema Reference |
|-------|------|------------------|
| code | integer | integer |
| message | string | string |
## 400ErrorResponse


Bad request.




### application/json
schema:

  
  [Error](#error)
















## ID


ID of an object.



## RemoteID


Remote ID from the API that requested the extraction.



## Status


Status of an extraction. Can be one of QUEUED|RUNNING|FAILED|SUCCESS.



## Filetype


Filetype of the document.



## FiletypeConfig




## Base64Document


Document serialized in base64 string.


| Field | Type | Schema Reference |
|-------|------|------------------|
| data | string | string |

## Document


Document to extract text from.


| Field | Type | Schema Reference |
|-------|------|------------------|
| filetype |  | [Filetype](#filetype) |
| filetype_config |  | [FiletypeConfig](#filetypeconfig) |
| base64 |  | [Base64Document](#base64document) |

## ExtractRequest


Request to extract text from a document.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  | [Document](#document) |
| webhook | string | string |
| remote_id |  | [RemoteID](#remoteid) |

## ExtractAcceptedResponse


Response when an extraction request is accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| id |  | [ID](#id) |
| status |  | [Status](#status) |

## ExtractMetadata


Metadata extracted from the document.



## StateResponse


All data regarding the state of the API.


| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| supported_filetypes | array | array |
| tika_endpoint | string | string |

## Error


API error.


| Field | Type | Schema Reference |
|-------|------|------------------|
| code | integer | integer |
| message | string | string |
## 503ErrorResponse


Service unavailable.




### application/json
schema:

  
  [Error](#error)
















## ID


ID of an object.



## RemoteID


Remote ID from the API that requested the extraction.



## Status


Status of an extraction. Can be one of QUEUED|RUNNING|FAILED|SUCCESS.



## Filetype


Filetype of the document.



## FiletypeConfig




## Base64Document


Document serialized in base64 string.


| Field | Type | Schema Reference |
|-------|------|------------------|
| data | string | string |

## Document


Document to extract text from.


| Field | Type | Schema Reference |
|-------|------|------------------|
| filetype |  | [Filetype](#filetype) |
| filetype_config |  | [FiletypeConfig](#filetypeconfig) |
| base64 |  | [Base64Document](#base64document) |

## ExtractRequest


Request to extract text from a document.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  | [Document](#document) |
| webhook | string | string |
| remote_id |  | [RemoteID](#remoteid) |

## ExtractAcceptedResponse


Response when an extraction request is accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| id |  | [ID](#id) |
| status |  | [Status](#status) |

## ExtractMetadata


Metadata extracted from the document.



## StateResponse


All data regarding the state of the API.


| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| supported_filetypes | array | array |
| tika_endpoint | string | string |

## Error


API error.


| Field | Type | Schema Reference |
|-------|------|------------------|
| code | integer | integer |
| message | string | string |
## PostExtractResponse


Extract request accepted




### application/json
schema:

  
  [ExtractAcceptedResponse](#extractacceptedresponse)
















## ID


ID of an object.



## RemoteID


Remote ID from the API that requested the extraction.



## Status


Status of an extraction. Can be one of QUEUED|RUNNING|FAILED|SUCCESS.



## Filetype


Filetype of the document.



## FiletypeConfig




## Base64Document


Document serialized in base64 string.


| Field | Type | Schema Reference |
|-------|------|------------------|
| data | string | string |

## Document


Document to extract text from.


| Field | Type | Schema Reference |
|-------|------|------------------|
| filetype |  | [Filetype](#filetype) |
| filetype_config |  | [FiletypeConfig](#filetypeconfig) |
| base64 |  | [Base64Document](#base64document) |

## ExtractRequest


Request to extract text from a document.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  | [Document](#document) |
| webhook | string | string |
| remote_id |  | [RemoteID](#remoteid) |

## ExtractAcceptedResponse


Response when an extraction request is accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| id |  | [ID](#id) |
| status |  | [Status](#status) |

## ExtractMetadata


Metadata extracted from the document.



## StateResponse


All data regarding the state of the API.


| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| supported_filetypes | array | array |
| tika_endpoint | string | string |

## Error


API error.


| Field | Type | Schema Reference |
|-------|------|------------------|
| code | integer | integer |
| message | string | string |
## GetStateResponse


Get API state response




### application/json
schema:

  
  [StateResponse](#stateresponse)
















## ID


ID of an object.



## RemoteID


Remote ID from the API that requested the extraction.



## Status


Status of an extraction. Can be one of QUEUED|RUNNING|FAILED|SUCCESS.



## Filetype


Filetype of the document.



## FiletypeConfig




## Base64Document


Document serialized in base64 string.


| Field | Type | Schema Reference |
|-------|------|------------------|
| data | string | string |

## Document


Document to extract text from.


| Field | Type | Schema Reference |
|-------|------|------------------|
| filetype |  | [Filetype](#filetype) |
| filetype_config |  | [FiletypeConfig](#filetypeconfig) |
| base64 |  | [Base64Document](#base64document) |

## ExtractRequest


Request to extract text from a document.


| Field | Type | Schema Reference |
|-------|------|------------------|
| document |  | [Document](#document) |
| webhook | string | string |
| remote_id |  | [RemoteID](#remoteid) |

## ExtractAcceptedResponse


Response when an extraction request is accepted.


| Field | Type | Schema Reference |
|-------|------|------------------|
| id |  | [ID](#id) |
| status |  | [Status](#status) |

## ExtractMetadata


Metadata extracted from the document.



## StateResponse


All data regarding the state of the API.


| Field | Type | Schema Reference |
|-------|------|------------------|
| endpoint | string | string |
| process_available | integer | integer |
| process_queued | integer | integer |
| supported_filetypes | array | array |
| tika_endpoint | string | string |

## Error


API error.


| Field | Type | Schema Reference |
|-------|------|------------------|
| code | integer | integer |
| message | string | string |
