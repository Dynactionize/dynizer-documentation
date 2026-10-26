# Dynizer API

- version : 2.2
- Public API for the Dynizer knowledge engine.<br>All endpoints are under `/api/v2`, secured with JWT unless stated otherwise.<br>See the [Dynizer overview](https://www.consono.ai/technology) for architecture details.
- Consono : support@consono.ai
# Endpoints

| Tag | Description |
|-----|-------------|
| Dynizer |  |


---
# APIs

## Endpoint: /api/v2/actions
`POST /api/v2/actions`

Create an **Action** with the provided name.<br>Names must be unique, trimmed, and free of control characters. Use `CheckActionName` to validate availability.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `400`: 
    Invalid Argument
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `409`: 
    ActionName already in use
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actions/types/{action_type_label}/count
`GET /api/v2/actions/types/{action_type_label}/count`

Return the total number of **Actions** for a given **ActionType**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actions/types/{action_type_label}/names/all
`GET /api/v2/actions/types/{action_type_label}/names/all`

List **Action** names for a given **ActionType** with optional pagination window.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actions/{action_name}
`GET /api/v2/actions/{action_name}`

Fetch an **Action** definition including its **ActionLabels**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/actions/{action_name}`

Delete an **Action**.<br>Fails if **Instances** exist unless `cascade=true`, which marks the action and its instances as deleted.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`PATCH /api/v2/actions/{action_name}`

Rename an **Action**.<br>Names must be unique, trimmed, and free of control characters.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actions/{action_name}/actionlabels
`POST /api/v2/actions/{action_name}/actionlabels`

Add an **ActionLabel** to an existing **Action**.<br>Use `CheckActionLabelName` first to validate the name.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actions/{action_name}/actionlabels/{action_label}
`GET /api/v2/actions/{action_name}/actionlabels/{action_label}`

Fetch an **ActionLabel** definition for an **Action**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/actions/{action_name}/actionlabels/{action_label}`

Delete an **ActionLabel**: prevents future use and removes existing values from **Instances**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`PUT /api/v2/actions/{action_name}/actionlabels/{action_label}`

Update an **ActionLabel** definition.<br>If `cascade=true`, **Instances** violating the new definition are marked as deleted.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actions/{action_name}/purge
`DELETE /api/v2/actions/{action_name}/purge`

Permanently delete an **Action** (hard delete removes the action, its action labels, and all persisted data; this action is irreversible).<br>Fails if **Instances** exist unless `cascade=true`, which also permanently deletes all associated instances.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actionschemas
`GET /api/v2/actionschemas`

List **ActionSchemas** with optional pagination window.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`POST /api/v2/actionschemas`

Create a new **ActionSchema** including its labels and data types.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actionschemas/{action_schema_name}
`GET /api/v2/actionschemas/{action_schema_name}`

Reads an **ActionSchema** definition.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/actionschemas/{action_schema_name}`

Delete an **ActionSchema**.<br>Fails if **Actions** exist unless `cascade=true`, which marks those actions and instances as deleted.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`PATCH /api/v2/actionschemas/{action_schema_name}`

Rename an **ActionSchema**.<br>Names must be unique, trimmed, and free of control characters.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actionschemas/{action_schema_name}/purge
`DELETE /api/v2/actionschemas/{action_schema_name}/purge`

Permanently delete an **ActionSchema** (hard delete removes the action schema and all persisted data; this action is irreversible).<br>Fails if **Actions** exist unless `cascade=true`, which also permanently deletes all associated actions and their instances.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actiontypes
`GET /api/v2/actiontypes`

List **ActionTypes** with optional pagination (deprecated; use `ListActionSchemas`).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`POST /api/v2/actiontypes`

Create a new **ActionType** (deprecated in favor of **ActionSchema**).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/actiontypes/{action_type_label}
`GET /api/v2/actiontypes/{action_type_label}`

Fetch an **ActionType** definition with its **ActionLabels** (deprecated).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`PATCH /api/v2/actiontypes/{action_type_label}`

Rename an **ActionType** (deprecated).<br>Names must be unique, trimmed, and free of control characters.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/check/actions/{action_name}
`GET /api/v2/check/actions/{action_name}`

Validate whether an **Action** name is unique and uses only supported characters.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `400`: 
    Invalid ActionName format
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `409`: 
    ActionName already in use
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/check/actions/{action_name}/actionlabels/{action_label}
`GET /api/v2/check/actions/{action_name}/actionlabels/{action_label}`

Validate whether a string is an allowed, available **ActionLabel** name for the **Action**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/check/metadata/keys/{key_name}
`GET /api/v2/check/metadata/keys/{key_name}`

Validate whether a string can be used as a **MetaDataKey** name.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/check/password
`POST /api/v2/check/password`

Validate password strength and policy compliance, returning a score.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/check/user/{user}
`GET /api/v2/check/user/{user}`

Validate whether a user name is available and conforms to naming rules.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/config
`GET /api/v2/config`

Return **Dynizer** configuration as key/value pairs.<br>Security-sensitive settings are omitted.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/dataelements/query/contains
`POST /api/v2/dataelements/query/contains`

Query **DataElements** by partial match and **DataType** with optional filters.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/dataelements/top
`POST /api/v2/dataelements/top`

Fetch the top N **DataElements** used in **Instances**, with optional filters.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/find_actionlabel_links
`POST /api/v2/find_actionlabel_links`

Find **ActionLabels** that share data elements across a set of **Actions**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/instances
`POST /api/v2/instances`

Create a new **Instance** with values.<br>Each **ActionLabel** can hold multiple values (per its definition), and each value can override the label's default **DataType**. Optional metadata can be attached at all levels (experimental).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/instances/{instance_id}
`GET /api/v2/instances/{instance_id}`

Fetch an **Instance** by ID.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/instances/{instance_id}`

Delete an **Instance** (soft delete marks it as deleted without removing persisted data).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`PATCH /api/v2/instances/{instance_id}`

Update an existing **Instance**.<br>Send only changed values; to remove a value, set the **ActionLabel** datatype to *DT_Delete*. Each label supports multiple values (per its definition) and values can override the label's default **DataType**. Metadata can be updated at all levels (experimental).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/instances/{instance_id}/purge
`DELETE /api/v2/instances/{instance_id}/purge`

Permanently delete an **Instance** (hard delete removes the instance and all persisted data; this action is irreversible).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/jwt/{token}/validate
`GET /api/v2/jwt/{token}/validate`

Validates a JWT and returns the associated session identifier when valid.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/login
`POST /api/v2/login`

Authenticate with username and password.<br>On success returns a [JSON Web Token](https://jwt.io/) [(RFC 7519)](https://tools.ietf.org/html/rfc7519) to authorize subsequent calls.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/logout
`GET /api/v2/logout`

Ends the current session and clears server-side state.<br>Use when a client is finished with the issued token.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/maintenance/index/{index_name}
`GET /api/v2/maintenance/index/{index_name}`

Trigger a rebuild of the specified index.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}
`POST /api/v2/metadata/instances/{instance_id}`

Add a **MetaDataKey** and values to an **Instance**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}
`POST /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}`

Add a **MetaDataKey** and values to all **InstanceCells** under an **ActionLabel**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/keys/{key_name}
`DELETE /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/keys/{key_name}`

Remove a **MetaDataKey** and all its values from all **InstanceCells** under an **ActionLabel**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/keys/{key_name}/values
`POST /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/keys/{key_name}/values`

Add another value to a **MetaDataKey** across all **InstanceCells** under an **ActionLabel**.<br>Fails if the value already exists. Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/keys/{key_name}/values/{value}
`DELETE /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/keys/{key_name}/values/{value}`

Remove a value from a **MetaDataKey** across all **InstanceCells** under an **ActionLabel**.<br>Fails if the value is not present. Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}
`POST /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}`

Add a **MetaDataKey** and values to a specific **InstanceCell**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys
`GET /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys`

List **MetaDataKeys** and values attached to a specific **InstanceCell**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/all/count
`GET /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/all/count`

Count **MetaDataKeys** associated with a specific **InstanceCell**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/{key_name}
`GET /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/{key_name}`

Return all values for a **MetaDataKey** on a specific **InstanceCell**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/{key_name}`

Remove a **MetaDataKey** and all its values from a specific **InstanceCell**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/{key_name}/values
`POST /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/{key_name}/values`

Add another value to a **MetaDataKey** on a specific **InstanceCell**.<br>Fails if the value already exists. Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/{key_name}/values/all/count
`GET /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/{key_name}/values/all/count`

Count values set for a **MetaDataKey** on a specific **InstanceCell**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/{key_name}/values/{value}
`DELETE /api/v2/metadata/instances/{instance_id}/actionlabels/{action_label}/position/{value_position}/keys/{key_name}/values/{value}`

Remove a value from a **MetaDataKey** on a specific **InstanceCell**.<br>Fails if the value is not present (case sensitive). Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/keys
`GET /api/v2/metadata/instances/{instance_id}/keys`

List **MetaDataKeys** linked to an **Instance** with their values.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/keys/all/count
`GET /api/v2/metadata/instances/{instance_id}/keys/all/count`

Count **MetaDataKeys** attached to an **Instance**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/keys/{key_name}
`GET /api/v2/metadata/instances/{instance_id}/keys/{key_name}`

Return all values for a given **MetaDataKey** on an **Instance**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/metadata/instances/{instance_id}/keys/{key_name}`

Remove a **MetaDataKey** and all its values from an **Instance**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/keys/{key_name}/values
`POST /api/v2/metadata/instances/{instance_id}/keys/{key_name}/values`

Add another value to a **MetaDataKey** on an **Instance**.<br>Fails if the value already exists. Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/keys/{key_name}/values/all/count
`GET /api/v2/metadata/instances/{instance_id}/keys/{key_name}/values/all/count`

Count values set for a **MetaDataKey** on an **Instance**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/instances/{instance_id}/keys/{key_name}/values/{value}
`DELETE /api/v2/metadata/instances/{instance_id}/keys/{key_name}/values/{value}`

Remove a value from a **MetaDataKey** on an **Instance**.<br>Fails if the value is not present. Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/keys
`GET /api/v2/metadata/keys`

List **MetaDataKeys** with optional pagination window.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`POST /api/v2/metadata/keys`

Create a **MetaDataKey** definition.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/keys/all/count
`GET /api/v2/metadata/keys/all/count`

Count **MetaDataKeys** in the Dynizer.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/metadata/keys/{key_name}
`GET /api/v2/metadata/keys/{key_name}`

Read a **MetaDataKey** definition.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/metadata/keys/{key_name}`

Delete a **MetaDataKey**.<br>If `cascade=true`, all usages of the key are removed as well.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`PATCH /api/v2/metadata/keys/{key_name}`

Update a **MetaDataKey** (name, default DataType, max occurrence, alternative DataTypes).<br>Raises an error if existing metadata would violate the new definition.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/my/password
`PUT /api/v2/my/password`

Change the logged-in user's password using the current password for verification.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/my/profile
`GET /api/v2/my/profile`

Retrieve the current user's profile, including assigned roles.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/my/roles
`GET /api/v2/my/roles`

List roles assigned to the current authenticated user.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/objects
`GET /api/v2/objects`

List all **Object** reference UUIDs.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/objects`

Delete all large-object blocks and their data.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`POST /api/v2/objects`

Create an object reference used to store large values of type *TEXT*, *CLOB*, *BLOB*, or *DOCUMENT*.<br>*TEXT* is indexed by **FullTextIndex** if enabled; *CLOB* is an unindexed character LOB; *BLOB* is an unindexed binary LOB; *DOCUMENT* holds JSON document analysis output.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/objects/{object_ref.type}/{object_ref.ref_uuid}
`GET /api/v2/objects/{object_ref.type}/{object_ref.ref_uuid}`

Download data from a large-object block referenced by `object_ref`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/objects/{object_ref.type}/{object_ref.ref_uuid}`

Delete the referenced large-object block and its stored data.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`POST /api/v2/objects/{object_ref.type}/{object_ref.ref_uuid}`

Upload data to a large-object block referenced by `object_ref`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`PATCH /api/v2/objects/{object_ref.type}/{object_ref.ref_uuid}`

Clear the content of a referenced large-object block while keeping the reference.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/objects/{object_ref.type}/{object_ref.ref_uuid}/size
`GET /api/v2/objects/{object_ref.type}/{object_ref.ref_uuid}/size`

Get the size in bytes of data stored in a large-object block referenced by `object_ref`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/plots/filtered/{top}/{plot_name}
`POST /api/v2/plots/filtered/{top}/{plot_name}`

Execute a filtered statement to retrieve plot data JSON.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query
`POST /api/v2/query`

Execute a DQL statement and return the result.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/bind
`POST /api/v2/query/bind`

Bind parameters to a parsed DQL statement.<br>Part of the experimental query engine; enable it with session variable `query_v3_session=true`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/close
`POST /api/v2/query/close`

Close and clean up parsed/bound DQL statements.<br>Part of the experimental query engine; enable it with session variable `query_v3_session=true`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/execute
`POST /api/v2/query/execute`

Execute a parsed and bound DQL statement, returning ResultRows with optional window/offset.<br>Part of the experimental query engine; enable it with session variable `query_v3_session=true`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/filtered
`POST /api/v2/query/filtered`

Execute a filtered statement to retrieve **Instances**.<br>Experimental: interface may change in a minor update.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/parse
`POST /api/v2/query/parse`

Parse a DQL statement in the session.<br>Part of the experimental query engine; enable it with session variable `query_v3_session=true`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/portal/describe
`POST /api/v2/query/portal/describe`

Return ResultLabels for a parsed DQL statement and its bound parameters.<br>Part of the experimental query engine; enable it with session variable `query_v3_session=true`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/simple
`POST /api/v2/query/simple`

Execute a DQL statement and return results immediately.<br>Part of the experimental query engine, but also compatible with the current engine. To enable the experimental engine, set session variable `query_v3_session=true`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/statement/describe
`POST /api/v2/query/statement/describe`

Return ResultLabels for a parsed DQL statement.<br>Part of the experimental query engine; enable it with session variable `query_v3_session=true`.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/{result_handle}/close
`GET /api/v2/query/{result_handle}/close`

Close a `result_handle` and free its server-side resources.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/query/{result_handle}/next
`GET /api/v2/query/{result_handle}/next`

Fetch result rows from a `result_handle` using an optional window for pagination.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/roles
`GET /api/v2/roles`

List every role configured in the Dynizer.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/servicelogin
`POST /api/v2/servicelogin`

Authenticate using a service token tied to a service account.<br>Returns a [JSON Web Token](https://jwt.io/) [(RFC 7519)](https://tools.ietf.org/html/rfc7519) if the token is valid and the associated user is authorized.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/servicetoken/issue
`GET /api/v2/servicetoken/issue`

Issues a new service token for the current user.<br>Use this to allow headless/service processes to authenticate later without sharing a password.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/sharename
`POST /api/v2/sharename`

Create a new **ShareName**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/sharename/{share_name}/delete/value
`POST /api/v2/sharename/{share_name}/delete/value`

Delete the value stored under an existing **ShareName**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/sharename/{share_name}/value
`PATCH /api/v2/sharename/{share_name}/value`

Update the value stored under an existing **ShareName**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/system/data
`DELETE /api/v2/system/data`

Drop **all data**. **Irreversible** operation; use with extreme caution.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/system/export/useractions
`POST /api/v2/system/export/useractions`

Export all **Actions**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/system/import/useractions
`POST /api/v2/system/import/useractions`

Import **Actions**.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/system/version
`GET /api/v2/system/version`

Get the current **Dynizer** version.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/users
`GET /api/v2/users`

List users with optional pagination window.<br>Defaults to returning all users.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`POST /api/v2/users`

Create a new user with optional roles.<br>Requires admin privileges.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/users/all/count
`GET /api/v2/users/all/count`

Return total user count plus counts broken down by enabled vs disabled.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/users/{user}
`GET /api/v2/users/{user}`

Fetch a user's profile including roles and enabled/disabled status.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`DELETE /api/v2/users/{user}`

Permanently delete a user and revoke access.<br>This operation cannot be undone.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/users/{user}/disable
`PATCH /api/v2/users/{user}/disable`

Disable a user account to block logins without deleting it.<br>Requires admin privileges.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/users/{user}/enable
`PATCH /api/v2/users/{user}/enable`

Enable a user account so it can log in.<br>Requires admin privileges.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/users/{user}/password
`PUT /api/v2/users/{user}/password`

Set a new password for another user (does not require their current password).<br>Requires admin privileges.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/users/{user}/roles
`GET /api/v2/users/{user}/roles`

List all roles assigned to the specified user.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
`POST /api/v2/users/{user}/roles`

Attach a role to the specified user.<br>Requires admin privileges.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/users/{user}/roles/{role.name}
`DELETE /api/v2/users/{user}/roles/{role.name}`

Remove a role from the specified user.<br>Requires admin privileges.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/objects/download/{type}/{uuid}
`GET /api/v2/objects/download/{type}/{uuid}`

Downloads an object of provided type and UUID. Returns the raw bytes of the object.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `400`: 
    Invalid Argument
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/objects/upload/{type}/{uuid}
`POST /api/v2/objects/upload/{type}/{uuid}`

Uploads an object of provided type and UUID. Accepts the raw bytes of the object.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `400`: 
    Invalid Argument
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/docs
`GET /api/v2/docs`

Downloads the docs of Dynizer in HTML format.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `404`: 
    Not found
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/docs/{file}
`GET /api/v2/docs/{file}`

Downloads the docs of Dynizer in HTML format (index.html).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `404`: 
    Not found
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/spec
`GET /api/v2/spec`

Downloads the spec of Dynizer in format defined by the Accept header (default = application/yaml, others = application/json).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `404`: 
    Not found
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/spec/{file}
`GET /api/v2/spec/{file}`

Downloads the spec of Dynizer in the format defined by the Accept header and filename (application/yaml = dynizer.swagger.yaml, application/json = dynizer.swagger.json).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `404`: 
    Not found
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/proto
`GET /api/v2/proto`

Downloads the proto definition of Dynizer.


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `404`: 
    Not found
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
## Endpoint: /api/v2/proto/{file}
`GET /api/v2/proto/{file}`

Downloads the proto definition of Dynizer (dynizer.proto).


  

**Responses**

- `200`: 
    A successful response.
    
    
 
- `401`: 
    Unauthorized call
    
    
 
- `404`: 
    Not found
    
    
 
- `500`: 
    Unexpected internal error
    
    
 
- `default`: 
    An unexpected error response.
    
    
 
 
 
---
# Components


## Action

Message to hold a **Action**



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_name | string | string |
| action_labels | array | array |








## ActionLabel

An **ActionLabel** defines a group of columns with the same name and **ComponentType**.<br>The default **DataType** is used when no overwrite is used.<br>Min and Max occurrence is used to limit the amount of values which can be used for an **ActionLabel**.<br>The alternative **dataTypes** can be used to constrain which **DataTypes** can be used for the overwrite.<br>With it you can define all the **DataTypes** allowed to be used under this **ActionLabel**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_label_name | string | string |
| component |  | [ComponentType](#componenttype) |
| default_data_type |  | [DataType](#datatype) |
| min_occurrence | integer | integer |
| max_occurrence | integer | integer |
| alternative_data_types | array | array |
| share_name | string | string |





action_label_name, component, default_data_type, min_occurrence, max_occurrence, alternative_data_types, is_active are required properties.




## ActionLabelLink

The **ActionLabel** links of the request **Actions**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| left_action_label |  | [ActionNameActionLabelName](#actionnameactionlabelname) |
| right_action_label |  | [ActionNameActionLabelName](#actionnameactionlabelname) |
| left_total | string | string |
| right_total | string | string |
| shared_total | string | string |





left_action_label, right_action_label, left_total, right_total, shared_total are required properties.




## 



| Field | Type | Schema Reference |
|-------|------|------------------|
| name | string | string |


{'type': 'string'} is a  property.







## ActionNameActionLabelName

**Action** name and label pair



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_name | string | string |
| action_label_name | string | string |





action_name, actionlabel_name are required properties.




## ActionNameArrayResponse

Response which holds an array of **Action** records.



| Field | Type | Schema Reference |
|-------|------|------------------|
| total_actions | integer | integer |
| action_names | array | array |





action_names, total_actions are required properties.




## ActionResponse

Response which holds an **Action**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action |  | [Action](#action) |





action are required properties.




## ActionSchemaArrayRes

Response that holds **ActionSchemas**



| Field | Type | Schema Reference |
|-------|------|------------------|
| total_action_schemas | integer | integer |
| action_schema_names | array | array |





action_schema_names, total_action_schemas are required properties.




## ActionSchemaResponse

Response which holds an **ActionSchema**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_schema_name | string | string |





action_schema_name are required properties.




## 

Response that holds **ActionTypes**



| Field | Type | Schema Reference |
|-------|------|------------------|
| total_action_types | integer | integer |
| action_type_labels | array | array |





action_type_labels, total_action_types are required properties.




## 

ActionTypeLabel
Deprecated: Use `string` instead.



| Field | Type | Schema Reference |
|-------|------|------------------|
| label | string | string |








## 

Response which holds an **ActionType**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_type | string | string |
| action_type_label | string | string |





action_type_label are required properties.




## AddUserRequest

Holds all properties which are needed to create a new user in the Dynizer.



| Field | Type | Schema Reference |
|-------|------|------------------|
| user | string | string |
| password | string | string |
| roles | array | array |
| disabled | boolean | boolean |





user, password are required properties.




## ChangePasswordRequest

Request for an user to change it's own password.



| Field | Type | Schema Reference |
|-------|------|------------------|
| old_password | string | string |
| new_password | string | string |





old_password, new_password are required properties.




## CheckPasswordReq

Request checking a potential password.



| Field | Type | Schema Reference |
|-------|------|------------------|
| password | string | string |





password are required properties.




## CheckPasswordRes

an array of ResultRow messages for the list request



| Field | Type | Schema Reference |
|-------|------|------------------|
| strength | integer | integer |
| crack_time | string | string |
| valid | boolean | boolean |
| fail_reason | string | string |





strength, crack_time, valid, fail_reason are required properties.




## ComponentType

- Who: subject data category
 - What: object data category
 - Where: spatial data category
 - When: temporal data category








## 

Returns details of the number of **Instances** found divided by **ComponentType** for the **DataElement**



| Field | Type | Schema Reference |
|-------|------|------------------|
| component_type |  | [ComponentType](#componenttype) |
| num_instances | integer | integer |





component_type, num_instances are required properties.




## ConfigKV

Holds Dynizer system configuration



| Field | Type | Schema Reference |
|-------|------|------------------|
| config_key | string | string |
| numeric_value | number | number |
| string_value | string | string |





config_key, config_value are required properties.




## CountResponse

Generic count response.



| Field | Type | Schema Reference |
|-------|------|------------------|
| count | integer | integer |





count are required properties.




## CreateActionRequest

This is used to create an **Action**.<br>If supplied **ActionLabels** can be addes as well.<br>The *if_not_exists* flag allows if set not to raise an error if the **Action** already exists.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_name | string | string |
| if_not_exists | boolean | boolean |
| action_labels | array | array |





action_name are required properties.




## CreateActionSchemaRequest

This is used to create an **ActionSchema**.<br>The *if_not_exists* flag allows if set not to raise an error if the **ActionSchema** already exists.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_schema_name | string | string |
| if_not_exists | boolean | boolean |





action_schema_name are required properties.




## 

This is used to create an **ActionType**.<br>The *if_not_exists* flag allows if set not to raise an error if the **ActionType** already exists.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_type_label | string | string |
| if_not_exists | boolean | boolean |





action_type_label are required properties.




## CreateInstanceRequest

This will create an Instance, for each ActionLabel defined in the Action and element can be defined.<br>Each element can have multiple values.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_name | string | string |
| instance_elements | array | array |
| instance_metadata | array | array |





action_name, instance_elements are required properties.




## CreateMetaDataKeyRequest

Properties to create a new MetaDataKey



| Field | Type | Schema Reference |
|-------|------|------------------|
| key_name | string | string |
| default_data_type |  | [DataType](#datatype) |
| max_occurrence | integer | integer |
| alternative_data_types | array | array |





key_name, default_data_type are required properties.




## CreateObjectRequest



| Field | Type | Schema Reference |
|-------|------|------------------|
| type |  | [ObjectDataType](#objectdatatype) |





type are required properties.




## 

Creates a new **ShareName**



| Field | Type | Schema Reference |
|-------|------|------------------|
| share_name | string | string |
| if_not_exists | boolean | boolean |





share_name are required properties.




## DynizerQueryParameter

Holds Dynizer Query Parameter



| Field | Type | Schema Reference |
|-------|------|------------------|
| index | integer | integer |
| string_value | string | string |
| binary_value | string | string |
| spec |  | [DataTypeFormat](#datatypeformat) |





value are required properties.




## DynizerQueryParameterDescription

Holds Dynizer Query Parameter Description



| Field | Type | Schema Reference |
|-------|------|------------------|
| index | integer | integer |
| data_type |  | [DataType](#datatype) |





value are required properties.




## DynizerQueryLanguageRequest

DQL statment



| Field | Type | Schema Reference |
|-------|------|------------------|
| dql | string | string |
| parameters | array | array |
| statement | string | string |
| portal | string | string |





dql are required properties.




## DynizerQueryResponse

Holds the different Dynizer Query responses.



| Field | Type | Schema Reference |
|-------|------|------------------|
| select_result |  | [SelectDQLResult](#selectdqlresult) |
| rows_affected | integer | integer |





kind are required properties.




## DQLType

- DQL_None: Empty query type
 - DQL_Set: Type of a SET query
 - DQL_Show: Type of a SHOW query
 - DQL_Select: Type of a SELECT query
 - DQL_Insert: Type of a INSERT query
 - DQL_Update: Type of a UPDATE query
 - DQL_Delete: Type of a DELETE query
 - DQL_CreateSchema: Type of a CREATE SCHEMA query
 - DQL_CreateTable: Type of a CREATE_TABLE query
 - DQL_AlterSchema: Type of a ALTER SCHEMA query
 - DQL_AlterTable: Type of a ALTER TABLE query
 - DQL_DropSchema: Type of a DROP SCHEMA query
 - DQL_DropTable: Type of a DROP TABLE query
 - DQL_Begin: Type of a BEGIN query => Not implemented, no-op
 - DQL_Commit: Type of a COMMIT query => Not implemented, no-op
 - DQL_Rollback: Type of a ROLLBACK query => Not implemented, no-op
 - DQL_Discard: Type of a DISCARD query => Not implemented, no-op
 - DQL_Prepare: Type of a PREPARE query
 - DQL_Execute: Type of a EXECUTE query
 - DQL_Deallocate: Type of a DEALLOCATE query
 - DQL_Explain: Type of a EXPLAIN query








## 

Returns **DataElements** which match a contains value



| Field | Type | Schema Reference |
|-------|------|------------------|
| value | string | string |
| data_type |  | [DataType](#datatype) |
| num_instances | integer | integer |
| by_component_type | array | array |
| contains | array | array |





value, data_type, num_instances are required properties.




## DataType

- DT_Integer: Integer
 - DT_String: String
 - DT_Boolean: Boolean
 - DT_Decimal: Decimal fixed
 - DT_Timestamp: Timestamp
 - DT_Uri: URI
 - DT_Void: VOID is a designated DataType to indicate no value
 - DT_Float: Float
 - DT_UnsignedInteger: UInt
 - DT_Binary: Byte Array
 - DT_Uuid: UUID
 - DT_Text: FullTextIndex large object
 - DT_Blob: Binary large object
 - DT_Clob: Character large object
 - DT_Document: Document large object, stores/indexes document analysis output
 - DT_Any: DT_Date = 16;
DT_Time = 17;
special flag to indicate all DataTypes, to be used in AlternativeDataTypes for ActionLabels and MetaDataKeys
 - DT_Delete: special flag to indicate that the value is to be removed








## DataTypeFormat

DataType override, and an optional format string



| Field | Type | Schema Reference |
|-------|------|------------------|
| data_type |  | [DataType](#datatype) |
| format | string | string |








## DownloadObjectDataResponse

URL to fetch an **Object**



| Field | Type | Schema Reference |
|-------|------|------------------|
| data | string | string |
| content_type | string | string |





url are required properties.




## AddActionLabelRequest

Use this to add a new **ActionLabel** to an **Action**



| Field | Type | Schema Reference |
|-------|------|------------------|
| if_not_exists | boolean | boolean |
| action_label_name | string | string |
| component |  | [ComponentType](#componenttype) |
| default_data_type |  | [DataType](#datatype) |
| min_occurrence | integer | integer |
| max_occurrence | integer | integer |
| alternative_data_types | array | array |
| share_name | string | string |





action_label_name, component, default_data_type are required properties.




## AddInstanceActionLabelMetaDataRequest

Holds the properties to set MetaData for all cells under the **ActionLabel**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| key_name | string | string |
| values | array | array |
| specs | array | array |





key_name, values are required properties.




## AddInstanceActionLabelMetaDataValueRequest

Holds the properties to add a value to the MetaData to ActionLabel grouped cells.



| Field | Type | Schema Reference |
|-------|------|------------------|
| value | string | string |
| spec |  | [DataTypeFormat](#datatypeformat) |





value are required properties.




## AddInstanceCellMetaDataRequest

Holds the properties to identify MetaData assciated to an **InstanceCell**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| key_name | string | string |
| values | array | array |
| specs | array | array |





key_name, values are required properties.




## AddInstanceCellMetaDataValueRequest

Identifies a single value of a MetaData from an **InstanceCell**



| Field | Type | Schema Reference |
|-------|------|------------------|
| value | string | string |
| spec |  | [DataTypeFormat](#datatypeformat) |





value are required properties.




## AddInstanceMetaDataRequest

Used for adding a **MetaDataKey** with its values to an **Instance**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| key_name | string | string |
| values | array | array |
| specs | array | array |





key_name, values are required properties.




## AddInstanceMetaDataValueRequest

Adds a new value to an already linked **MetaDataKey**



| Field | Type | Schema Reference |
|-------|------|------------------|
| value | string | string |
| spec |  | [DataTypeFormat](#datatypeformat) |





value are required properties.




## UserRoleRequest

Request for adding or removing a role for the user specified



| Field | Type | Schema Reference |
|-------|------|------------------|
| role |  | [DynizerRole](#dynizerrole) |





role are required properties.




## 

Deletes a Value for a **ShareName**



| Field | Type | Schema Reference |
|-------|------|------------------|
| current_value | string | string |
| data_type |  | [DataType](#datatype) |





current_value, data_type are required properties.




## 

Returns plot data based on the fliter and plot name



| Field | Type | Schema Reference |
|-------|------|------------------|
| actions | array | array |
| data_types | array | array |
| component_types | array | array |
| filters | array | array |








## DynizerRole

Defines one Role of the Dynizer



| Field | Type | Schema Reference |
|-------|------|------------------|
| name | string | string |


{'type': 'string', 'description': 'Unique name of the system-wide role'} is a  property.




name are required properties.




## SetUserPasswordRequest

Set a users password as an admin



| Field | Type | Schema Reference |
|-------|------|------------------|
| new_password | string | string |





new_password are required properties.




## UpdateActionLabelReq

Use this to modify an **ActionLabel** associated to an **Action**. To ensure data integrity, please provide values for the fields alternative_data_types, min_occurrence, and max_occurrence. If these fields are omitted, they will be reset. Other fields can be safely omitted to retain their current values.



| Field | Type | Schema Reference |
|-------|------|------------------|
| new_action_label_name | string | string |
| default_data_type |  | [DataType](#datatype) |
| min_occurrence | integer | integer |
| max_occurrence | integer | integer |
| alternative_data_types | array | array |
| cascade | boolean | boolean |





default_data_type, min_occurrence, max_occurrence, alternative_data_types are required properties.




## UpdateActionSchemaRequest

Use to rename an **ActionSchema**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| new_action_schema_name | string | string |





new_action_schema_name are required properties.




## UpdateInstanceRequest

Used to update an Instance.<br>



| Field | Type | Schema Reference |
|-------|------|------------------|
| instance_cell_elements | array | array |





instance_elements are required properties.




## UpdateMetaDataKeyRequest

Used to update a **MetaDataKey**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| new_key_name | string | string |
| default_data_type |  | [DataType](#datatype) |
| max_occurrence | integer | integer |
| alternative_data_types | array | array |








## 

Updates a Value for a **ShareName**



| Field | Type | Schema Reference |
|-------|------|------------------|
| old_value | string | string |
| new_value | string | string |
| data_type |  | [DataType](#datatype) |





old_value, new_value, data_type are required properties.




## UploadObjectDataRequest

URL for an **Object**



| Field | Type | Schema Reference |
|-------|------|------------------|
| type | string | string |
| ref_uuid | string | string |
| data | string | string |
| object_ref | object | object |
| content_type | string | string |








## EmptyResponse

Response with no data.<br>Used whenever there is no payload to be returned








## ErrorArg holds an argument of an encoded gRPC error metadata



| Field | Type | Schema Reference |
|-------|------|------------------|
| int_arg | string | string |
| bool_arg | boolean | boolean |
| string_arg | string | string |
| double_arg | number | number |
| bytes_arg | string | string |








## ErrorResponse

Error message based on the [RFC 7807](https://tools.ietf.org/html/rfc7807) standard



| Field | Type | Schema Reference |
|-------|------|------------------|
| type | string | string |
| title | string | string |
| status | integer | integer |
| detail | string | string |
| reference | string | string |
| args | array | array |








## ExportUserActionsRequest

Exports all **Actions**



| Field | Type | Schema Reference |
|-------|------|------------------|
| actions | array | array |








## ExportUserActionsResponse

Returns all the exported **UserActions**



| Field | Type | Schema Reference |
|-------|------|------------------|
| actions | array | array |





actions are required properties.




## 

Returns **DataElements** with their count in the Instances slected by the filter or overall if no filter has been set



| Field | Type | Schema Reference |
|-------|------|------------------|
| actions | array | array |
| filters | array | array |





filters are required properties.




## FindActionLabelLinksRequest

Used to find links between **ActionLabels** accross **Actions**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_names | array | array |





action_names are required properties.




## FindActionLabelLinksResponse

The **ActionLabel** links of the request **Actions**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| links | array | array |





links are required properties.




## GetDynizerConfigurationResponse

Holds Dynizer system configuration



| Field | Type | Schema Reference |
|-------|------|------------------|
| config_key_values | array | array |





config_key_values are required properties.




## GetInstanceCellMetaDataKeyResponse

Holds all the MetaData values for a sepcific **MetaDataKey** information for an **Instance**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| instance_id | string | string |
| action_label | string | string |
| value_position | integer | integer |
| meta_data |  | [MetaDataOut](#metadataout) |





instance_id, action_label, value_position, meta_data are required properties.




## GetInstanceMetaDataKeyResponse

Holds all the values for a **MetaDataKey** linked to an **Instance**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| instance_id | string | string |
| meta_data |  | [MetaDataOut](#metadataout) |





instance_id, meta_data are required properties.




## GetObjectSizeResponse

Size of an **Object** in bytes



| Field | Type | Schema Reference |
|-------|------|------------------|
| size | integer | integer |





size are required properties.




## 

Returns **DataElements** with their count in the Instances slected by the filter or overall if no filter has been set



| Field | Type | Schema Reference |
|-------|------|------------------|
| top | integer | integer |
| actions | array | array |
| data_types | array | array |
| component_types | array | array |
| filters | array | array |





contains are required properties.




## 

Returns **DataElements** which match a contains value



| Field | Type | Schema Reference |
|-------|------|------------------|
| who | array | array |
| what | array | array |
| where | array | array |
| when | array | array |








## ImportUserActionsRequest

This is used to import **Actions**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| actions | array | array |
| if_not_exists | boolean | boolean |





actions are required properties.




## InstanceElement

each Element represents one ActionLabel and multiple values.<br>The specs allow for DataType override and pars format definition.<br>Additionaly can you also add MetaData for each value.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_label | string | string |
| values | array | array |
| specs | array | array |
| meta_data | array | array |





action_label, values are required properties.




## InstanceElementMetaData

MetaData information to be added per individual InstanceElement value.<br>Multiple MetaDataKeys with values can be added per InstanceElement value position



| Field | Type | Schema Reference |
|-------|------|------------------|
| position | integer | integer |
| meta_data_key_values |  | [MetaDataKeyValue](#metadatakeyvalue) |





position, meta_data_key_values are required properties.




## 

Defines an **Instance** - filter



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_label_name | string | string |
| values | array | array |
| component_type |  | [ComponentType](#componenttype) |





version, build, mode, build_date, commit are required properties.




## InstanceIDResponse

This holds the Instance ID



| Field | Type | Schema Reference |
|-------|------|------------------|
| instance_id | string | string |





instance_id are required properties.




## InstanceRes response which returns one Action Instance row

This holds an **Instance** row



| Field | Type | Schema Reference |
|-------|------|------------------|
| instance_id | string | string |
| action_labels | array | array |
| instance_cell_values | array | array |
| alternative_data_types | array | array |





instance_id, user_action_labels, instance_cell_value are required properties.




## InstanceUpdateElementCell

each Element represents one ActionLabel and multiple values.<br>The specs allow for DataType override and pars format definition.<br>Additionaly can you also add MetaData for each value.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_label | string | string |
| value | string | string |
| value_position | integer | integer |
| override |  | [DataTypeFormat](#datatypeformat) |





action_label, value, value_position are required properties.




## LabelResponse

Response that holds an **Action** and all its **ActionLabels**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| action | string | string |
| action_label |  | [ActionLabel](#actionlabel) |





user_action, action_label are required properties.




## ListInstanceCellMetaDataRes

Holds all the MetaData information for an **Instance**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| instance_id | string | string |
| action_label | string | string |
| value_position | integer | integer |
| total_meta_data_entries | integer | integer |
| meta_data | array | array |





instance_id, action_label, value_position, meta_data, total_meta_data_entries are required properties.




## ListInstanceMetaDataResponse

Holds all the MetaData information for an **Instance**.



| Field | Type | Schema Reference |
|-------|------|------------------|
| instance_id | string | string |
| total_meta_data_entries | integer | integer |
| meta_data | array | array |





instance_id, meta_data, total_meta_data_entries are required properties.




## ListRolesResponse

Roles selected by the window



| Field | Type | Schema Reference |
|-------|------|------------------|
| total_roles | integer | integer |
| roles | array | array |





roles, total_roles are required properties.




## ListUserRolesResponse

Response with all roles for a user



| Field | Type | Schema Reference |
|-------|------|------------------|
| total_roles | integer | integer |
| roles | array | array |





roles, total_roles are required properties.




## ListUsersResponse

Response which holds all users.



| Field | Type | Schema Reference |
|-------|------|------------------|
| total_users | integer | integer |
| users | array | array |





users, total_users are required properties.




## LoginRequest

Login Request with user and password.



| Field | Type | Schema Reference |
|-------|------|------------------|
| user | string | string |
| password | string | string |





user, password are required properties.




## LoginResponse

JsonWebToken response for a successful login with including the users roles



| Field | Type | Schema Reference |
|-------|------|------------------|
| jwt | string | string |
| roles | array | array |





jwt, roles are required properties.




## MetaDataKey

Message to hold a **MetaDataKey*



| Field | Type | Schema Reference |
|-------|------|------------------|
| key_name | string | string |
| default_data_type |  | [DataType](#datatype) |
| max_occurrence | integer | integer |
| alternative_data_types | array | array |





key_name, default_data_type, max_occurrence, alternative_data_types are required properties.




## MetaDataKeyArrayResponse

Response that holds **MetaDataKeys**



| Field | Type | Schema Reference |
|-------|------|------------------|
| total_meta_data_keys | integer | integer |
| meta_data_keys | array | array |





meta_data_keys are required properties.




## MetaDataKeyResponse

Response that holds a **MetaDataKey**



| Field | Type | Schema Reference |
|-------|------|------------------|
| meta_data_key |  | [MetaDataKey](#metadatakey) |





meta_data_key are required properties.




## MetaDataKeyValue

MetaData Key Value for inserts



| Field | Type | Schema Reference |
|-------|------|------------------|
| key_name | string | string |
| values | array | array |
| specs | array | array |





key_name, values are required properties.




## MetaDataOut

MetaData out Object



| Field | Type | Schema Reference |
|-------|------|------------------|
| meta_data_key_value |  | [MetaDataRecord](#metadatarecord) |








## MetaDataRecord

MetaDataRecord



| Field | Type | Schema Reference |
|-------|------|------------------|
| key_name | string | string |
| values | array | array |
| data_type |  | [DataType](#datatype) |








## ObjectDataType

- ODT_Text: object is of type TEXT, which can be indexed by the FullTextIndex
 - ODT_Blob: object is of type binary
 - ODT_Clob: object is of type character
 - ODT_Document: object is of type character, indexed by FullTextIndex








## ObjectReference

Message to hold a **ObjectReference*



| Field | Type | Schema Reference |
|-------|------|------------------|
| ref_uri | string | string |
| type |  | [ObjectDataType](#objectdatatype) |
| ref_uuid | string | string |








## ObjectResponse

This holds the Object reference URI



| Field | Type | Schema Reference |
|-------|------|------------------|
| object_ref |  | [ObjectRef](#objectref) |





object_ref are required properties.




## 

Response which holds an array of **Object** UUIDs.



| Field | Type | Schema Reference |
|-------|------|------------------|
| total_objects | integer | integer |
| object_uuids | array | array |





objects, total_objects are required properties.




## OrderField

- Created: order by created
 - Name: order by name








## 

Returns **PlotData** which match the filter



| Field | Type | Schema Reference |
|-------|------|------------------|
| plot_name | string | string |
| plot_json | string | string |








## 

Performs the Bind of Parameter values



| Field | Type | Schema Reference |
|-------|------|------------------|
| statement | string | string |
| portal | string | string |
| parameters | array | array |





parameters are required properties.




## 

Cleans up the session data for weither a portal or a statement.
If a statement close is issued all associated portals are closed too.



| Field | Type | Schema Reference |
|-------|------|------------------|
| result_handle | string | string |
| statement | string | string |
| portal | string | string |





close_for are required properties.




## 

Returns **DataElements** which match a contains value



| Field | Type | Schema Reference |
|-------|------|------------------|
| contains | string | string |
| actions | array | array |
| data_types | array | array |
| filters | array | array |
| max_length | integer | integer |
| component_types | array | array |
| with_component_type_split | boolean | boolean |





contains are required properties.




## 

Returns **DataElements** which match a contains value



| Field | Type | Schema Reference |
|-------|------|------------------|
| total_dataelements | integer | integer |
| dataelements | array | array |





total_dataelements, dataelements are required properties.




## 

Performs the Describe for either a statement or a portal.
A statement description will return the definition for both the Parameters as well as the ActionLabels.
A portal description will just return the ActionLabels.



| Field | Type | Schema Reference |
|-------|------|------------------|
| portal | string | string |





portal are required properties.




## 

Returns the description of the ActionLabels and DQL-Parameter



| Field | Type | Schema Reference |
|-------|------|------------------|
| result_labels | array | array |
| parameters | array | array |
| type |  | [DQLType](#dqltype) |





result_labels are required properties.




## 

Performs the Describe for either a statement or a portal.
A statement description will return the definition for both the Parameters as well as the ActionLabels.
A portal description will just return the ActionLabels.



| Field | Type | Schema Reference |
|-------|------|------------------|
| statement | string | string |





statement are required properties.




## 

Returns the description of the ActionLabels



| Field | Type | Schema Reference |
|-------|------|------------------|
| result_labels | array | array |
| parameter_descriptions | array | array |
| type |  | [DQLType](#dqltype) |





result_labels are required properties.




## 

Executes a prepared and bound query



| Field | Type | Schema Reference |
|-------|------|------------------|
| portal | string | string |
| window |  | [Window](#window) |





portal, row_limit are required properties.




## QueryExecuteResponse

an array of ResultRow messages for the list request



| Field | Type | Schema Reference |
|-------|------|------------------|
| rows | array | array |
| alternative_data_types | array | array |
| completed | boolean | boolean |
| type |  | [DQLType](#dqltype) |
| count | integer | integer |
| rows_affected | integer | integer |





rows are required properties.




## 

DQL statement to be parsed



| Field | Type | Schema Reference |
|-------|------|------------------|
| statement | string | string |
| dql | string | string |
| parameter_descriptions | array | array |





dql are required properties.




## QueryResultResponse

an array of ResultRow messages for the list request



| Field | Type | Schema Reference |
|-------|------|------------------|
| rows | array | array |
| alternative_data_types | array | array |





rows are required properties.




## ResultLabel

Message to hold a result label



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_name | string | string |
| result_label_name | string | string |
| result_label_index | integer | integer |
| component_type |  | [ComponentType](#componenttype) |
| default_data_type |  | [DataType](#datatype) |
| action_schema_name | string | string |








## ResultLabelWithOverride

Message to hold a result label



| Field | Type | Schema Reference |
|-------|------|------------------|
| action_name | string | string |
| result_label_name | string | string |
| result_label_index | integer | integer |
| component_type |  | [ComponentType](#componenttype) |
| default_data_type |  | [DataType](#datatype) |
| override_data_type |  | [DataType](#datatype) |
| action_schema_name | string | string |








## ResultRow

Message to hold a result row



| Field | Type | Schema Reference |
|-------|------|------------------|
| instance_cell_values | array | array |








## ResultValueAlternativeMetaDataPosition

Message to hold a the alternative DataType for a Cell in the result



| Field | Type | Schema Reference |
|-------|------|------------------|
| row | integer | integer |
| col | integer | integer |
| data_type |  | [DataType](#datatype) |








## SelectDQLResult

Message to hold a DQL SELECT result cursor handle with count and metadata



| Field | Type | Schema Reference |
|-------|------|------------------|
| result_count | integer | integer |
| result_handle | string | string |
| result_labels | array | array |








## ServiceLoginReq

Service Login carries a service token that the server validates to authenticate and impersonate the service account.



| Field | Type | Schema Reference |
|-------|------|------------------|
| token | string | string |





token are required properties.




## ServiceTokenResponse

ServieToken response for a successful issue



| Field | Type | Schema Reference |
|-------|------|------------------|
| token | string | string |





token are required properties.




## SessionID

Holds Dynizer session ID



| Field | Type | Schema Reference |
|-------|------|------------------|
| session_id | string | string |





session_id are required properties.




## 

The answers to the simple query, one for each query in the full string



| Field | Type | Schema Reference |
|-------|------|------------------|
| result | array | array |





result are required properties.




## 

The answer to a part of the simple query, either the rows affected for INSERT, UPDATE, DELETE, DROP, ... or the LabelDescription and rows for SELECT



| Field | Type | Schema Reference |
|-------|------|------------------|
| select_result |  | [SimpleSelectResult](#simpleselectresult) |
| rows_affected | integer | integer |
| type |  | [DQLType](#dqltype) |





kind are required properties.




## 

LabelDescription and rows for SELECT



| Field | Type | Schema Reference |
|-------|------|------------------|
| result_count | integer | integer |
| result_labels | array | array |
| rows | array | array |
| alternative_data_types | array | array |





result_count, result_labels, rows are required properties.




## SortOrder

- Asc: order ascending
 - Desc: order descending








## 

Returns **DataElements** which match a contains value



| Field | Type | Schema Reference |
|-------|------|------------------|
| value | string | string |
| data_type |  | [DataType](#datatype) |
| num_instances | integer | integer |





value, data_type, num_instances are required properties.




## User

Defines user in the Dynizer



| Field | Type | Schema Reference |
|-------|------|------------------|
| user_name | string | string |
| roles | array | array |
| enabled | boolean | boolean |





user_name, roles, enabled are required properties.




## User Count Response

Holds the count of all types of users and the total count.



| Field | Type | Schema Reference |
|-------|------|------------------|
| active_users | integer | integer |
| disabled_users | integer | integer |
| total_users | integer | integer |





active_users, disabled_users, total_users are required properties.




## UserResponse

Response which holds a user.



| Field | Type | Schema Reference |
|-------|------|------------------|
| user |  | [User](#user) |





user are required properties.




## ValueSpec

message which defines a ValueSpec this is for how to treat the string input in a special way, also the option to not use the default DataType



| Field | Type | Schema Reference |
|-------|------|------------------|
| position | integer | integer |
| override |  | [DataTypeFormat](#datatypeformat) |





position, override are required properties.




## VersionRes

Returns the version of the **Dynizer**



| Field | Type | Schema Reference |
|-------|------|------------------|
| version | string | string |
| build | string | string |
| build_date | string | string |





version, build, build_date are required properties.




## Window

Keeping limit and offset together



| Field | Type | Schema Reference |
|-------|------|------------------|
| limit | integer | integer |
| offset | integer | integer |
| relative | boolean | boolean |





limit, offset are required properties.




## 



| Field | Type | Schema Reference |
|-------|------|------------------|
| @type | string | string |








## 



| Field | Type | Schema Reference |
|-------|------|------------------|
| code | integer | integer |
| message | string | string |
| details | array | array |






