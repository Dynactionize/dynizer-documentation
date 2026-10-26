# Proto Documentation

> Syntax: `proto3`



## Services


### Dynizer


| Method | Request | Response | Type |
|--------|---------|----------|------|
| Login | [LoginReq](#loginreq) | [LoginRes](#loginres) | Unary |
| ServiceLogin | [ServiceLoginReq](#serviceloginreq) | [LoginRes](#loginres) | Unary |
| Logout | [EmptyReq](#emptyreq) | [EmptyRes](#emptyres) | Unary |
| ValidateToken | [TokenReq](#tokenreq) | [SessionID](#sessionid) | Unary |
| IssueServiceToken | [EmptyReq](#emptyreq) | [ServiceTokenRes](#servicetokenres) | Unary |
| ListRoles | [EmptyReq](#emptyreq) | [ListRolesRes](#listrolesres) | Unary |
| AddUser | [AddUserReq](#adduserreq) | [EmptyRes](#emptyres) | Unary |
| AssignUserRole | [UserRoleReq](#userrolereq) | [EmptyRes](#emptyres) | Unary |
| RevokeUserRole | [UserRoleReq](#userrolereq) | [EmptyRes](#emptyres) | Unary |
| EnableUser | [UserReq](#userreq) | [EmptyRes](#emptyres) | Unary |
| DisableUser | [UserReq](#userreq) | [EmptyRes](#emptyres) | Unary |
| SetUserPassword | [SetUserPasswordReq](#setuserpasswordreq) | [EmptyRes](#emptyres) | Unary |
| ChangeMyPassword | [ChangePasswordReq](#changepasswordreq) | [EmptyRes](#emptyres) | Unary |
| GetUser | [UserReq](#userreq) | [UserRes](#userres) | Unary |
| GetMyProfile | [EmptyReq](#emptyreq) | [UserRes](#userres) | Unary |
| DeleteUser | [UserReq](#userreq) | [EmptyRes](#emptyres) | Unary |
| GetUserCount | [EmptyReq](#emptyreq) | [UserCountRes](#usercountres) | Unary |
| ListUsers | [WindowReq](#windowreq) | [ListUsersRes](#listusersres) | Unary |
| ListUserRoles | [UserReq](#userreq) | [ListUserRolesRes](#listuserrolesres) | Unary |
| GetMyRoles | [EmptyReq](#emptyreq) | [ListUserRolesRes](#listuserrolesres) | Unary |
| CheckUserName | [UserReq](#userreq) | [EmptyRes](#emptyres) | Unary |
| CheckPassword | [CheckPasswordReq](#checkpasswordreq) | [CheckPasswordRes](#checkpasswordres) | Unary |
| CreateActionType | [CreateActionTypeReq](#createactiontypereq) | [EmptyRes](#emptyres) | Unary |
| UpdateActionType | [UpdateActionTypeReq](#updateactiontypereq) | [EmptyRes](#emptyres) | Unary |
| ReadActionType | [ActionTypeReq](#actiontypereq) | [ActionTypeRes](#actiontyperes) | Unary |
| ListActionTypes | [WindowReq](#windowreq) | [ActionTypeArrayRes](#actiontypearrayres) | Unary |
| CreateActionSchema | [CreateActionSchemaReq](#createactionschemareq) | [EmptyRes](#emptyres) | Unary |
| UpdateActionSchema | [UpdateActionSchemaReq](#updateactionschemareq) | [EmptyRes](#emptyres) | Unary |
| DeleteActionSchema | [DeleteActionSchemaReq](#deleteactionschemareq) | [EmptyRes](#emptyres) | Unary |
| ReadActionSchema | [ActionSchemaReq](#actionschemareq) | [ActionSchemaRes](#actionschemares) | Unary |
| ListActionSchemas | [WindowReq](#windowreq) | [ActionSchemaArrayRes](#actionschemaarrayres) | Unary |
| CheckActionName | [CheckActionNameReq](#checkactionnamereq) | [EmptyRes](#emptyres) | Unary |
| CreateAction | [CreateActionReq](#createactionreq) | [EmptyRes](#emptyres) | Unary |
| UpdateAction | [UpdateActionReq](#updateactionreq) | [EmptyRes](#emptyres) | Unary |
| DeleteAction | [DeleteActionReq](#deleteactionreq) | [EmptyRes](#emptyres) | Unary |
| ReadAction | [ActionReq](#actionreq) | [ActionRes](#actionres) | Unary |
| CountActions | [CountActionReq](#countactionreq) | [CountRes](#countres) | Unary |
| ListActionNames | [ListActionNamesWindowReq](#listactionnameswindowreq) | [ActionNameArrayRes](#actionnamearrayres) | Unary |
| CheckActionLabelName | [CheckActionLabelNameReq](#checkactionlabelnamereq) | [EmptyRes](#emptyres) | Unary |
| AddActionLabel | [AddActionLabelReq](#addactionlabelreq) | [EmptyRes](#emptyres) | Unary |
| UpdateActionLabel | [UpdateActionLabelReq](#updateactionlabelreq) | [EmptyRes](#emptyres) | Unary |
| DeleteActionLabel | [ActionLabelReq](#actionlabelreq) | [EmptyRes](#emptyres) | Unary |
| ReadActionLabel | [ActionLabelReq](#actionlabelreq) | [LabelRes](#labelres) | Unary |
| CreateObject | [CreateObjectReq](#createobjectreq) | [ObjectRes](#objectres) | Unary |
| ClearObjectData | [ClearObjectDataReq](#clearobjectdatareq) | [EmptyRes](#emptyres) | Unary |
| DeleteObject | [DeleteObjectReq](#deleteobjectreq) | [EmptyRes](#emptyres) | Unary |
| StreamObjectDataIn | [StreamObjectDataInReq](#streamobjectdatainreq) | [EmptyRes](#emptyres) | Client Streaming |
| StreamObjectDataOut | [StreamObjectDataOutReq](#streamobjectdataoutreq) | [StreamObjectDataOutRes](#streamobjectdataoutres) | Server Streaming |
| UploadObjectData | [UploadObjectDataReq](#uploadobjectdatareq) | [EmptyRes](#emptyres) | Unary |
| DownloadObjectData | [DownloadObjectDataReq](#downloadobjectdatareq) | [DownloadObjectDataRes](#downloadobjectdatares) | Unary |
| ListObjectUUIDS | [EmptyReq](#emptyreq) | [ObjectUUIDArrayRes](#objectuuidarrayres) | Unary |
| DeleteAllObjects | [EmptyReq](#emptyreq) | [EmptyRes](#emptyres) | Unary |
| CreateInstance | [CreateInstanceReq](#createinstancereq) | [InstanceIDRes](#instanceidres) | Unary |
| StreamInstances | [StreamInstanceReq](#streaminstancereq) | [StreamInstanceIDRes](#streaminstanceidres) | Bidirectional Streaming |
| UpdateInstance | [UpdateInstanceReq](#updateinstancereq) | [EmptyRes](#emptyres) | Unary |
| DeleteInstance | [InstanceReq](#instancereq) | [EmptyRes](#emptyres) | Unary |
| ReadInstance | [InstanceReq](#instancereq) | [InstanceRes](#instanceres) | Unary |
| DynizerQuery | [DQLReq](#dqlreq) | [DQLRes](#dqlres) | Unary |
| QueryResultNext | [QueryResultReq](#queryresultreq) | [QueryResultRes](#queryresultres) | Unary |
| QueryResultClose | [QueryCloseReq](#queryclosereq) | [EmptyRes](#emptyres) | Unary |
| CheckMetaDataKeyName | [CheckMetaDataKeyNameReq](#checkmetadatakeynamereq) | [EmptyRes](#emptyres) | Unary |
| CreateMetaDataKey | [CreateMetaDataKeyReq](#createmetadatakeyreq) | [EmptyRes](#emptyres) | Unary |
| ReadMetaDataKey | [MetaDataKeyReq](#metadatakeyreq) | [MetaDataKeyRes](#metadatakeyres) | Unary |
| UpdateMetaDataKey | [UpdateMetaDataKeyReq](#updatemetadatakeyreq) | [EmptyRes](#emptyres) | Unary |
| DeleteMetaDataKey | [DeleteMetaDataKeyReq](#deletemetadatakeyreq) | [EmptyRes](#emptyres) | Unary |
| CountMetaDataKeys | [EmptyReq](#emptyreq) | [CountRes](#countres) | Unary |
| ListMetaDataKeys | [ListMetaDataKeysReq](#listmetadatakeysreq) | [MetaDataKeyArrayRes](#metadatakeyarrayres) | Unary |
| AddInstanceMetaData | [AddInstanceMetaDataReq](#addinstancemetadatareq) | [EmptyRes](#emptyres) | Unary |
| RemoveInstanceMetaData | [InstanceMetaDataKeyReq](#instancemetadatakeyreq) | [EmptyRes](#emptyres) | Unary |
| AddInstanceMetaDataValue | [AddInstanceMetaDataValueReq](#addinstancemetadatavaluereq) | [EmptyRes](#emptyres) | Unary |
| RemoveInstanceMetaDataValue | [InstanceMetaDataKeyValueReq](#instancemetadatakeyvaluereq) | [EmptyRes](#emptyres) | Unary |
| GetInstanceMetaDataValues | [InstanceMetaDataKeyReq](#instancemetadatakeyreq) | [GetInstanceMetaDataKeyRes](#getinstancemetadatakeyres) | Unary |
| CountInstanceMetaDataKeys | [InstanceReq](#instancereq) | [CountRes](#countres) | Unary |
| CountInstanceMetaDataKeyValues | [InstanceMetaDataKeyReq](#instancemetadatakeyreq) | [CountRes](#countres) | Unary |
| ListInstanceMetaData | [InstanceReq](#instancereq) | [ListInstanceMetaDataRes](#listinstancemetadatares) | Unary |
| AddInstanceActionLabelMetaData | [AddInstanceActionLabelMetaDataReq](#addinstanceactionlabelmetadatareq) | [EmptyRes](#emptyres) | Unary |
| RemoveInstanceActionLabelMetaData | [InstanceActionLabelMetaDataKeyReq](#instanceactionlabelmetadatakeyreq) | [EmptyRes](#emptyres) | Unary |
| AddInstanceActionLabelMetaDataValue | [AddInstanceActionLabelMetaDataValueReq](#addinstanceactionlabelmetadatavaluereq) | [EmptyRes](#emptyres) | Unary |
| RemoveInstanceActionLabelMetaDataValue | [InstanceActionLabelMetaDataValueReq](#instanceactionlabelmetadatavaluereq) | [EmptyRes](#emptyres) | Unary |
| AddInstanceCellMetaData | [AddInstanceCellMetaDataReq](#addinstancecellmetadatareq) | [EmptyRes](#emptyres) | Unary |
| RemoveInstanceCellMetaData | [InstanceCellMetaDataKeyReq](#instancecellmetadatakeyreq) | [EmptyRes](#emptyres) | Unary |
| AddInstanceCellMetaDataValue | [AddInstanceCellMetaDataValueReq](#addinstancecellmetadatavaluereq) | [EmptyRes](#emptyres) | Unary |
| RemoveInstanceCellMetaDataValue | [InstanceCellMetaDataKeyValueReq](#instancecellmetadatakeyvaluereq) | [EmptyRes](#emptyres) | Unary |
| GetInstanceCellMetaDataValues | [InstanceCellMetaDataKeyReq](#instancecellmetadatakeyreq) | [GetInstanceCellMetaDataKeyRes](#getinstancecellmetadatakeyres) | Unary |
| CountInstanceCellMetaDataKeys | [InstanceCellMetaDataReq](#instancecellmetadatareq) | [CountRes](#countres) | Unary |
| CountInstanceCellMetaDataKeyValues | [InstanceCellMetaDataKeyReq](#instancecellmetadatakeyreq) | [CountRes](#countres) | Unary |
| ListInstanceCellMetaData | [InstanceCellMetaDataReq](#instancecellmetadatareq) | [ListInstanceCellMetaDataRes](#listinstancecellmetadatares) | Unary |
| GetDynizerConfiguration | [EmptyReq](#emptyreq) | [GetDynizerConfigurationRes](#getdynizerconfigurationres) | Unary |
| ExportUserActions | [ExportUserActionsReq](#exportuseractionsreq) | [ExportUserActionsRes](#exportuseractionsres) | Unary |
| ImportUserActions | [ImportUserActionsReq](#importuseractionsreq) | [EmptyRes](#emptyres) | Unary |
| DropData | [EmptyReq](#emptyreq) | [EmptyRes](#emptyres) | Unary |
| GetDynizerVersion | [EmptyReq](#emptyreq) | [VersionRes](#versionres) | Unary |
| QueryDataElements | [QueryDataElementsReq](#querydataelementsreq) | [QueryDataElementsRes](#querydataelementsres) | Unary |
| GetTopNDataElements | [GetTopNDataElementsReq](#gettopndataelementsreq) | [GetTopNDataElementsRes](#gettopndataelementsres) | Unary |
| DynizerFilteredQuery | [FilterQueryReq](#filterqueryreq) | [DQLRes](#dqlres) | Unary |
| ReIndex | [ReIndexReq](#reindexreq) | [EmptyRes](#emptyres) | Unary |
| DynizerFilteredPlot | [FilteredPlotReq](#filteredplotreq) | [PlotRes](#plotres) | Unary |
| CreateShareName | [CreateShareNameReq](#createsharenamereq) | [EmptyRes](#emptyres) | Unary |
| UpdateShareNameValue | [UpdateShareNameValueReq](#updatesharenamevaluereq) | [EmptyRes](#emptyres) | Unary |
| DeleteShareNameValue | [DeleteShareNameValueReq](#deletesharenamevaluereq) | [EmptyRes](#emptyres) | Unary |
| SimpleQuery | [DQLReq](#dqlreq) | [SimpleQueryRes](#simplequeryres) | Unary |
| QueryParse | [QueryParseReq](#queryparsereq) | [EmptyRes](#emptyres) | Unary |
| QueryBind | [QueryBindReq](#querybindreq) | [EmptyRes](#emptyres) | Unary |
| QueryDescribeStatement | [QueryDescribeStatementReq](#querydescribestatementreq) | [QueryDescribeStatementRes](#querydescribestatementres) | Unary |
| QueryDescribePortal | [QueryDescribePortalReq](#querydescribeportalreq) | [QueryDescribePortalRes](#querydescribeportalres) | Unary |
| QueryExecute | [QueryExecuteReq](#queryexecutereq) | [QueryExecuteRes](#queryexecuteres) | Unary |
| QueryClose | [QueryCloseReq](#queryclosereq) | [EmptyRes](#emptyres) | Unary |
| FindActionLabelLinks | [FindActionLabelLinksReq](#findactionlabellinksreq) | [FindActionLabelLinksRes](#findactionlabellinksres) | Unary |




## Messages


### ErrorMeta



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| dynizer_code | int64 | 1 |  |  |
| uuid | string | 2 |  |  |
| original_error | string | 3 |  |  |
| args | [ErrorArg](#errorarg) | 4 | repeated |  |



### ErrorArg




**oneof `arg`** 

| Field | Type | Number | Description |
|-------|------|--------|-------------|
| int_arg | int64 | 1 |  |
| bool_arg | bool | 2 |  |
| string_arg | string | 3 |  |
| double_arg | double | 4 |  |
| bytes_arg | bytes | 5 |  |




### ErrorResponse



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| type | string | 1 |  |  |
| title | string | 2 |  |  |
| status | int32 | 3 |  |  |
| detail | string | 4 |  |  |
| reference | string | 5 |  |  |
| args | [ErrorArg](#errorarg) | 6 | repeated |  |



### LoginReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| user | string | 1 |  |  |
| password | string | 2 |  |  |



### ServiceLoginReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| token | string | 1 |  |  |



### TokenReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| token | string | 1 |  |  |



### AddUserReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| user | string | 1 |  |  |
| password | string | 2 |  |  |
| roles | [DynizerRole](#dynizerrole) | 3 | repeated |  |
| disabled | bool | 4 |  |  |



### UserRoleReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| user | string | 1 |  |  |
| role | [DynizerRole](#dynizerrole) | 2 |  |  |



### UserReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| user | string | 1 |  |  |



### CheckPasswordReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| password | string | 1 |  |  |



### WindowReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| window | [Window](#window) | 1 |  |  |



### ListActionNamesWindowReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_type_label | string | 1 |  |  |
| window | [Window](#window) | 2 |  |  |
| order_field | [OrderField](#orderfield) | 3 |  |  |
| order_direction | [SortOrder](#sortorder) | 4 |  |  |



### SetUserPasswordReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| user | string | 1 |  |  |
| new_password | string | 2 |  |  |



### ChangePasswordReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| old_password | string | 1 |  |  |
| new_password | string | 2 |  |  |



### CheckActionNameReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |



### CreateActionReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| if_not_exists | bool | 2 |  |  |
| action_labels | [ActionLabel](#actionlabel) | 3 | repeated |  |



### ActionName



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| name | string | 1 |  |  |



### UpdateActionReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| new_action_name | [ActionName](#actionname) | 2 |  |  |



### DeleteActionReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| cascade | bool | 2 |  |  |



### ActionReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |



### ActionRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action | [Action](#action) | 1 |  |  |



### CreateActionTypeReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_type_label | string | 1 |  |  |
| if_not_exists | bool | 2 |  |  |



### ActionTypeLabel



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| label | string | 1 |  |  |



### CreateActionSchemaReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_schema_name | string | 1 |  |  |
| if_not_exists | bool | 2 |  |  |



### UpdateActionTypeReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_type_label | string | 1 |  |  |
| new_action_type_label | [ActionTypeLabel](#actiontypelabel) | 2 |  |  |



### UpdateActionSchemaReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_schema_name | string | 1 |  |  |
| new_action_schema_name | string | 2 |  |  |



### DeleteActionSchemaReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_schema_name | string | 1 |  |  |
| cascade | bool | 2 |  |  |



### ActionTypeReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_type_label | string | 1 |  |  |



### ActionSchemaReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_schema_name | string | 1 |  |  |



### ActionTypeRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_type | int64 | 1 |  |  |
| action_type_label | string | 2 |  |  |



### ActionSchemaRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_schema_name | string | 2 |  |  |



### ActionTypeArrayRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| total_action_types | int64 | 1 |  |  |
| action_type_labels | string | 2 | repeated |  |



### ActionSchemaArrayRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| total_action_schemas | int64 | 1 |  |  |
| action_schema_names | string | 2 | repeated |  |



### EmptyReq





### CheckActionLabelNameReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| action_label | string | 2 |  |  |



### AddActionLabelReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| if_not_exists | bool | 2 |  |  |
| action_label_name | string | 3 |  |  |
| component | [ComponentType](#componenttype) | 4 |  |  |
| default_data_type | [DataType](#datatype) | 5 |  |  |
| min_occurrence | uint32 | 6 |  |  |
| max_occurrence | uint32 | 7 |  |  |
| alternative_data_types | [DataType](#datatype) | 8 | repeated |  |
| share_name | string | 9 |  |  |



### UpdateActionLabelReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| action_label | string | 2 |  |  |
| new_action_label_name | string | 3 |  |  |
| default_data_type | [DataType](#datatype) | 4 |  |  |
| min_occurrence | uint32 | 5 |  |  |
| max_occurrence | uint32 | 6 |  |  |
| alternative_data_types | [DataType](#datatype) | 7 | repeated |  |
| cascade | bool | 8 |  |  |



### ActionLabelReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| action_label | string | 2 |  |  |



### CreateObjectReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| type | [ObjectDataType](#objectdatatype) | 1 |  |  |



### ObjectRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| object_ref | [ObjectRef](#objectref) | 2 |  |  |



### ClearObjectDataReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| type | [ObjectDataType](#objectdatatype) | 1 |  |  |
| ref_uuid | string | 2 |  |  |
| object_ref | [ObjectRef](#objectref) | 3 |  |  |



### DeleteObjectReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| type | string | 1 |  |  |
| ref_uuid | string | 2 |  |  |
| object_ref | [ObjectRef](#objectref) | 3 |  |  |



### StreamObjectDataInReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| object_ref | [ObjectRef](#objectref) | 1 |  |  |
| data | bytes | 2 |  |  |
| content_type | string | 3 |  |  |



### StreamObjectDataOutReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| type | [ObjectDataType](#objectdatatype) | 1 |  |  |
| ref_uuid | string | 2 |  |  |
| object_ref | [ObjectRef](#objectref) | 3 |  |  |



### StreamObjectDataOutRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| data | bytes | 1 |  |  |
| content_type | string | 2 |  |  |



### DownloadObjectDataReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| type | string | 1 |  |  |
| ref_uuid | string | 2 |  |  |
| object_ref | [ObjectRef](#objectref) | 3 |  |  |



### DownloadObjectDataRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| data | bytes | 1 |  |  |
| content_type | string | 2 |  |  |



### UploadObjectDataReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| type | string | 1 |  |  |
| ref_uuid | string | 2 |  |  |
| data | bytes | 3 |  |  |
| object_ref | [ObjectRef](#objectref) | 4 |  |  |
| content_type | string | 5 |  |  |



### ObjectUUIDArrayRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| total_objects | int64 | 1 |  |  |
| object_uuids | string | 2 | repeated |  |



### CreateInstanceReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| instance_elements | [InstanceElement](#instanceelement) | 2 | repeated |  |
| instance_metadata | [MetaDataKeyValue](#metadatakeyvalue) | 3 | repeated |  |



### StreamInstanceReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| user_reference | string | 1 |  |  |
| instance | [CreateInstanceReq](#createinstancereq) | 2 |  |  |



### UpdateInstanceReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| instance_cell_elements | [InstanceUpdateElementCell](#instanceupdateelementcell) | 2 | repeated |  |



### InstanceReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |



### ReadActionInstancesReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| window | [Window](#window) | 2 |  |  |



### CountActionReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_type_label | string | 1 |  |  |



### DQLReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| dql | string | 1 |  |  |
| parameters | [DQLParam](#dqlparam) | 2 | repeated |  |
| statement | string | 3 |  |  |
| portal | string | 4 |  |  |



### QueryResultReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| result_handle | string | 1 |  |  |
| window | [Window](#window) | 2 |  |  |



### CheckMetaDataKeyNameReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |



### CreateMetaDataKeyReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |
| default_data_type | [DataType](#datatype) | 2 |  |  |
| max_occurrence | uint32 | 3 |  |  |
| alternative_data_types | [DataType](#datatype) | 4 | repeated |  |



### DeactivateMetaDataKeyReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |



### UpdateMetaDataKeyReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |
| new_key_name | string | 2 |  |  |
| default_data_type | [DataType](#datatype) | 3 |  |  |
| max_occurrence | uint32 | 4 |  |  |
| alternative_data_types | [DataType](#datatype) | 5 | repeated |  |



### MetaDataKeyReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |



### DeleteMetaDataKeyReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |
| cascade | bool | 2 |  |  |



### ListMetaDataKeysReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| window | [Window](#window) | 1 |  |  |



### AddInstanceMetaDataReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| key_name | string | 2 |  |  |
| values | string | 3 | repeated |  |
| specs | [ValueSpec](#valuespec) | 4 | repeated |  |



### AddInstanceMetaDataValueReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| key_name | string | 2 |  |  |
| value | string | 3 |  |  |
| spec | [DataTypeFormat](#datatypeformat) | 4 |  |  |



### InstanceMetaDataKeyReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| key_name | string | 2 |  |  |



### InstanceMetaDataKeyValueReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| key_name | string | 2 |  |  |
| value | string | 3 |  |  |
| spec | [DataTypeFormat](#datatypeformat) | 4 |  |  |



### AddInstanceActionLabelMetaDataReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| key_name | string | 3 |  |  |
| values | string | 4 | repeated |  |
| specs | [ValueSpec](#valuespec) | 5 | repeated |  |



### InstanceActionLabelMetaDataKeyReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| key_name | string | 3 |  |  |



### InstanceActionLabelMetaDataReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |



### AddInstanceCellMetaDataReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| value_position | uint32 | 3 |  |  |
| key_name | string | 4 |  |  |
| values | string | 5 | repeated |  |
| specs | [ValueSpec](#valuespec) | 6 | repeated |  |



### InstanceCellMetaDataKeyReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| value_position | uint32 | 3 |  |  |
| key_name | string | 4 |  |  |



### InstanceCellMetaDataReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| value_position | uint32 | 3 |  |  |



### StatsMetaDataKeyUsageReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |



### StatsMetaDataKeyValueUsageReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |
| value | string | 2 |  |  |
| spec | [DataTypeFormat](#datatypeformat) | 3 |  |  |



### ListMetaDataKeyLinksReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |
| window | [Window](#window) | 2 |  |  |



### AddInstanceActionLabelMetaDataValueReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| key_name | string | 3 |  |  |
| value | string | 4 |  |  |
| spec | [DataTypeFormat](#datatypeformat) | 5 |  |  |



### InstanceActionLabelMetaDataValueReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| key_name | string | 3 |  |  |
| value | string | 4 |  |  |
| spec | [DataTypeFormat](#datatypeformat) | 5 |  |  |



### InstanceCellMetaDataKeyValueReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| value_position | uint32 | 3 |  |  |
| key_name | string | 4 |  |  |
| value | string | 5 |  |  |
| spec | [DataTypeFormat](#datatypeformat) | 6 |  |  |



### AddInstanceCellMetaDataValueReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| value_position | uint32 | 3 |  |  |
| key_name | string | 4 |  |  |
| value | string | 5 |  |  |
| spec | [DataTypeFormat](#datatypeformat) | 6 |  |  |



### MetaDataValue



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| value | [MetaDataValue](#metadatavalue) | 3 |  |  |
| data_type | [DataType](#datatype) | 4 | repeated |  |
| format | string | 5 |  |  |



### InstanceElement



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_label | string | 1 |  |  |
| values | string | 2 | repeated |  |
| specs | [ValueSpec](#valuespec) | 3 | repeated |  |
| meta_data | [InstanceElementMetaData](#instanceelementmetadata) | 4 | repeated |  |



### ValueSpec



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| position | uint32 | 1 |  |  |
| override | [DataTypeFormat](#datatypeformat) | 2 |  |  |



### InstanceElementMetaData



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| position | uint32 | 1 |  |  |
| meta_data_key_values | [MetaDataKeyValue](#metadatakeyvalue) | 2 |  |  |



### MetaDataKeyValue



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |
| values | string | 2 | repeated |  |
| specs | [ValueSpec](#valuespec) | 4 | repeated |  |



### DataTypeFormat



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| data_type | [DataType](#datatype) | 3 |  |  |
| format | string | 4 |  |  |



### InstanceUpdateElementCell



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_label | string | 1 |  |  |
| value | string | 2 |  |  |
| value_position | uint32 | 3 |  |  |
| override | [DataTypeFormat](#datatypeformat) | 4 |  |  |



### EmptyRes





### LoginRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| jwt | string | 1 |  |  |
| roles | [DynizerRole](#dynizerrole) | 2 | repeated |  |



### ServiceTokenRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| token | string | 1 |  |  |



### UserRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| user | [User](#user) | 1 |  |  |



### ListUsersRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| total_users | int64 | 1 |  |  |
| users | [User](#user) | 2 | repeated |  |



### ActionNameArrayRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| total_actions | int64 | 1 |  |  |
| action_names | string | 2 | repeated |  |



### LabelRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action | string | 1 |  |  |
| action_label | [ActionLabel](#actionlabel) | 2 |  |  |



### InstanceIDRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 2 |  |  |



### StreamInstanceIDRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| user_reference | string | 1 |  |  |
| instance_id | string | 2 |  |  |
| error | [ErrorResponse](#errorresponse) | 3 |  |  |



### InstanceRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_labels | [ResultLabel](#resultlabel) | 2 | repeated |  |
| instance_cell_values | string | 3 | repeated |  |
| alternative_data_types | [ResultValueAlternativeMetaDataPosition](#resultvaluealternativemetadataposition) | 4 | repeated |  |



### CountRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| count | int64 | 1 |  |  |



### UserCountRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| active_users | int64 | 1 |  |  |
| disabled_users | int64 | 2 |  |  |
| total_users | int64 | 3 |  |  |



### DQLRes




**oneof `kind`** 

| Field | Type | Number | Description |
|-------|------|--------|-------------|
| select_result | [SelectDQLResult](#selectdqlresult) | 1 |  |
| rows_affected | int64 | 2 |  |




### ListRolesRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| total_roles | int64 | 1 |  |  |
| roles | [DynizerRole](#dynizerrole) | 2 | repeated |  |



### ListUserRolesRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| total_roles | int64 | 1 |  |  |
| roles | [DynizerRole](#dynizerrole) | 2 | repeated |  |



### MetaDataKeyRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| meta_data_key | [MetaDataKey](#metadatakey) | 1 |  |  |



### MetaDataKeyArrayRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| total_meta_data_keys | int64 | 1 |  |  |
| meta_data_keys | [MetaDataKey](#metadatakey) | 2 | repeated |  |



### ListInstanceMetaDataRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| total_meta_data_entries | int64 | 2 |  |  |
| meta_data | [MetaDataOut](#metadataout) | 3 | repeated |  |



### GetInstanceMetaDataKeyRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| meta_data | [MetaDataOut](#metadataout) | 2 |  |  |



### ListInstanceCellMetaDataRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| value_position | uint32 | 3 |  |  |
| total_meta_data_entries | int64 | 4 |  |  |
| meta_data | [MetaDataOut](#metadataout) | 5 | repeated |  |



### GetInstanceCellMetaDataKeyRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_id | string | 1 |  |  |
| action_label | string | 2 |  |  |
| value_position | uint32 | 3 |  |  |
| meta_data | [MetaDataOut](#metadataout) | 4 |  |  |



### StatsMetaUsageRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_count | int64 | 1 |  |  |
| cell_count | int64 | 2 |  |  |



### CheckPasswordRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| strength | uint32 | 1 |  |  |
| crack_time | string | 2 |  |  |
| valid | bool | 3 |  |  |
| fail_reason | string | 4 |  |  |



### DynizerRole



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| name | string | 1 |  |  |



### User



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| user_name | string | 1 |  |  |
| roles | [DynizerRole](#dynizerrole) | 2 | repeated |  |
| enabled | bool | 3 |  |  |



### DDLResult





### SelectDQLResult



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| result_count | int64 | 1 |  |  |
| result_handle | string | 2 |  |  |
| result_labels | [ResultLabel](#resultlabel) | 3 | repeated |  |



### ResultLabel



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| result_label_name | string | 2 |  |  |
| result_label_index | uint32 | 3 |  |  |
| component_type | [ComponentType](#componenttype) | 4 |  |  |
| default_data_type | [DataType](#datatype) | 5 |  |  |
| action_schema_name | string | 6 |  |  |



### ResultLabelWithOverride



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| result_label_name | string | 2 |  |  |
| result_label_index | uint32 | 3 |  |  |
| component_type | [ComponentType](#componenttype) | 4 |  |  |
| default_data_type | [DataType](#datatype) | 5 |  |  |
| override_data_type | [DataType](#datatype) | 6 |  |  |
| action_schema_name | string | 7 |  |  |



### ResultValueAlternativeMetaDataPosition



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| row | uint32 | 1 |  |  |
| col | uint32 | 2 |  |  |
| data_type | [DataType](#datatype) | 3 |  |  |



### ResultRow



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| instance_cell_values | string | 1 | repeated |  |



### Action



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| action_labels | [ActionLabel](#actionlabel) | 3 | repeated |  |



### ObjectRef



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| ref_uri | string | 1 |  |  |
| type | [ObjectDataType](#objectdatatype) | 2 |  |  |
| ref_uuid | string | 3 |  |  |



### ActionLabel



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_label_name | string | 1 |  |  |
| component | [ComponentType](#componenttype) | 2 |  |  |
| default_data_type | [DataType](#datatype) | 3 |  |  |
| min_occurrence | uint32 | 4 |  |  |
| max_occurrence | uint32 | 5 |  |  |
| alternative_data_types | [DataType](#datatype) | 6 | repeated |  |
| share_name | string | 7 |  |  |



### MetaDataKey



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |
| default_data_type | [DataType](#datatype) | 3 |  |  |
| max_occurrence | uint32 | 4 |  |  |
| alternative_data_types | [DataType](#datatype) | 5 | repeated |  |



### MetaDataOut



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| meta_data_key_value | [MetaDataRecord](#metadatarecord) | 1 |  |  |



### MetaDataRecord



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| key_name | string | 1 |  |  |
| values | string | 2 | repeated |  |
| data_type | [DataType](#datatype) | 3 |  |  |



### Window



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| limit | int64 | 1 |  |  |
| offset | int64 | 2 |  |  |
| relative | bool | 3 |  |  |



### DQLParam



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| index | uint32 | 1 |  |  |
| spec | [DataTypeFormat](#datatypeformat) | 4 |  |  |


**oneof `value`** 

| Field | Type | Number | Description |
|-------|------|--------|-------------|
| string_value | string | 2 |  |
| binary_value | bytes | 3 |  |




### SessionID



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| session_id | string | 1 |  |  |



### ConfigKV



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| config_key | string | 1 |  |  |


**oneof `config_value`** 

| Field | Type | Number | Description |
|-------|------|--------|-------------|
| numeric_value | float | 2 |  |
| string_value | string | 3 |  |




### GetDynizerConfigurationRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| config_key_values | [ConfigKV](#configkv) | 1 | repeated |  |



### ExportUserActionsReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| actions | string | 1 | repeated |  |



### ExportUserActionsRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| actions | [Action](#action) | 1 | repeated |  |



### ImportUserActionsReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| actions | [Action](#action) | 1 | repeated |  |
| if_not_exists | bool | 2 |  |  |



### ActionLabelSelector



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| action_label | string | 2 |  |  |



### VersionRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| version | string | 1 |  |  |
| build | string | 2 |  |  |
| build_date | string | 4 |  |  |



### InstanceFilter



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_label_name | string | 1 |  |  |
| values | string | 2 | repeated |  |
| component_type | [ComponentType](#componenttype) | 3 |  |  |



### QueryDataElementsReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| contains | string | 1 |  |  |
| actions | string | 2 | repeated |  |
| data_types | [DataType](#datatype) | 3 | repeated |  |
| filters | [InstanceFilter](#instancefilter) | 4 | repeated |  |
| max_length | int64 | 5 |  |  |
| component_types | [ComponentType](#componenttype) | 7 | repeated |  |
| with_component_type_split | bool | 8 |  |  |



### GetTopNDataElementsReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| top | int64 | 1 |  |  |
| actions | string | 2 | repeated |  |
| data_types | [DataType](#datatype) | 3 | repeated |  |
| component_types | [ComponentType](#componenttype) | 4 | repeated |  |
| filters | [InstanceFilter](#instancefilter) | 5 | repeated |  |



### GetTopNDataElementsRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| who | [TopNDataElement](#topndataelement) | 1 | repeated |  |
| what | [TopNDataElement](#topndataelement) | 2 | repeated |  |
| where | [TopNDataElement](#topndataelement) | 3 | repeated |  |
| when | [TopNDataElement](#topndataelement) | 4 | repeated |  |



### PlotRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| plot_name | string | 1 |  |  |
| plot_json | string | 2 |  |  |



### FilterQueryReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| actions | string | 1 | repeated |  |
| filters | [InstanceFilter](#instancefilter) | 2 | repeated |  |



### FilteredPlotReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| top | int64 | 1 |  |  |
| plot_name | string | 2 |  |  |
| actions | string | 3 | repeated |  |
| data_types | [DataType](#datatype) | 4 | repeated |  |
| component_types | [ComponentType](#componenttype) | 5 | repeated |  |
| filters | [InstanceFilter](#instancefilter) | 6 | repeated |  |



### ComponentTypeUsage



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| component_type | [ComponentType](#componenttype) | 1 |  |  |
| num_instances | int64 | 2 |  |  |



### TopNDataElement



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| value | string | 1 |  |  |
| data_type | [DataType](#datatype) | 2 |  |  |
| num_instances | int64 | 3 |  |  |



### DataElement



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| value | string | 1 |  |  |
| data_type | [DataType](#datatype) | 2 |  |  |
| num_instances | int64 | 3 |  |  |
| by_component_type | [ComponentTypeUsage](#componenttypeusage) | 4 | repeated |  |
| contains | string | 5 | repeated |  |



### QueryDataElementsRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| total_dataelements | int64 | 1 |  |  |
| dataelements | [DataElement](#dataelement) | 2 | repeated |  |



### ReIndexReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| index_name | string | 1 |  |  |
| args | string | 2 | repeated |  |



### CreateShareNameReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| share_name | string | 1 |  |  |
| if_not_exists | bool | 2 |  |  |



### UpdateShareNameValueReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| share_name | string | 1 |  |  |
| old_value | string | 2 |  |  |
| new_value | string | 3 |  |  |
| data_type | [DataType](#datatype) | 4 |  |  |



### DeleteShareNameValueReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| share_name | string | 1 |  |  |
| current_value | string | 2 |  |  |
| data_type | [DataType](#datatype) | 3 |  |  |



### BulkInstanceInsertStartReq





### BuilInstanceInsertRes





### BulkInstanceInsertDataReq





### BulkInstanceInsertCloseReq





### QueryResultRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| rows | [ResultRow](#resultrow) | 1 | repeated |  |
| alternative_data_types | [ResultValueAlternativeMetaDataPosition](#resultvaluealternativemetadataposition) | 2 | repeated |  |



### QueryExecuteRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| rows | [ResultRow](#resultrow) | 1 | repeated |  |
| alternative_data_types | [ResultValueAlternativeMetaDataPosition](#resultvaluealternativemetadataposition) | 2 | repeated |  |
| completed | bool | 3 |  |  |
| type | [DQLType](#dqltype) | 4 |  |  |
| count | int64 | 5 |  |  |
| rows_affected | int64 | 6 |  |  |



### SimpleSelectResult



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| result_count | int64 | 1 |  |  |
| result_labels | [ResultLabelWithOverride](#resultlabelwithoverride) | 3 | repeated |  |
| rows | [ResultRow](#resultrow) | 4 | repeated |  |
| alternative_data_types | [ResultValueAlternativeMetaDataPosition](#resultvaluealternativemetadataposition) | 5 | repeated |  |



### SimpleQueryResItem



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| type | [DQLType](#dqltype) | 3 |  |  |


**oneof `kind`** 

| Field | Type | Number | Description |
|-------|------|--------|-------------|
| select_result | [SimpleSelectResult](#simpleselectresult) | 1 |  |
| rows_affected | int64 | 2 |  |




### SimpleQueryRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| result | [SimpleQueryResItem](#simplequeryresitem) | 1 | repeated |  |



### QueryParseReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| statement | string | 1 |  |  |
| dql | string | 2 |  |  |
| parameter_descriptions | [DQLParamDescription](#dqlparamdescription) | 3 | repeated |  |



### QueryBindReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| statement | string | 1 |  |  |
| portal | string | 2 |  |  |
| parameters | [DQLParam](#dqlparam) | 3 | repeated |  |



### QueryDescribeStatementReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| statement | string | 1 |  |  |



### QueryDescribePortalReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| portal | string | 1 |  |  |



### QueryDescribeStatementRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| result_labels | [ResultLabelWithOverride](#resultlabelwithoverride) | 1 | repeated |  |
| parameter_descriptions | [DQLParamDescription](#dqlparamdescription) | 2 | repeated |  |
| type | [DQLType](#dqltype) | 3 |  |  |



### QueryDescribePortalRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| result_labels | [ResultLabelWithOverride](#resultlabelwithoverride) | 1 | repeated |  |
| parameters | [DQLParam](#dqlparam) | 2 | repeated |  |
| type | [DQLType](#dqltype) | 3 |  |  |



### QueryExecuteReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| portal | string | 1 |  |  |
| window | [Window](#window) | 2 |  |  |



### QueryCloseReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| result_handle | string | 1 |  |  |


**oneof `close_for`** 

| Field | Type | Number | Description |
|-------|------|--------|-------------|
| statement | string | 2 |  |
| portal | string | 3 |  |




### QueryCancelReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| portal | string | 1 |  |  |



### DQLParamDescription



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| index | uint32 | 1 |  |  |
| data_type | [DataType](#datatype) | 2 |  |  |



### FindActionLabelLinksReq



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_names | string | 1 | repeated |  |



### FindActionLabelLinksRes



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| links | [ActionLabelLink](#actionlabellink) | 1 | repeated |  |



### ActionNameActionLabelName



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| action_name | string | 1 |  |  |
| action_label_name | string | 2 |  |  |



### ActionLabelLink



| Field | Type | Number | Label | Description |
|-------|------|--------|-------|-------------|
| left_action_label | [ActionNameActionLabelName](#actionnameactionlabelname) | 1 |  |  |
| right_action_label | [ActionNameActionLabelName](#actionnameactionlabelname) | 2 |  |  |
| left_total | int64 | 3 |  |  |
| right_total | int64 | 4 |  |  |
| shared_total | int64 | 5 |  |  |




## Enums


### ComponentType


| Name | Number | Description |
|------|--------|-------------|
| InvalidComponentType | 0 |  |
| Who | 1 |  |
| What | 2 |  |
| Where | 3 |  |
| When | 4 |  |



### DataType


| Name | Number | Description |
|------|--------|-------------|
| InvalidDataType | 0 |  |
| DT_Integer | 1 |  |
| DT_String | 2 |  |
| DT_Boolean | 3 |  |
| DT_Decimal | 4 |  |
| DT_Timestamp | 5 |  |
| DT_Uri | 6 |  |
| DT_Void | 7 |  |
| DT_Float | 8 |  |
| DT_UnsignedInteger | 9 |  |
| DT_Binary | 10 |  |
| DT_Uuid | 11 |  |
| DT_Text | 12 |  |
| DT_Blob | 13 |  |
| DT_Clob | 14 |  |
| DT_Document | 15 |  |
| DT_Any | 100000 |  |
| DT_Delete | 100001 |  |



### ObjectDataType


| Name | Number | Description |
|------|--------|-------------|
| InvalidObjectDataType | 0 |  |
| ODT_Text | 12 |  |
| text | 12 |  |
| ODT_Blob | 13 |  |
| blob | 13 |  |
| ODT_Clob | 14 |  |
| clob | 14 |  |
| ODT_Document | 15 |  |
| document | 15 |  |



### SortOrder


| Name | Number | Description |
|------|--------|-------------|
| Asc | 0 |  |
| Desc | 1 |  |



### OrderField


| Name | Number | Description |
|------|--------|-------------|
| Created | 0 |  |
| Name | 1 |  |



### DQLType


| Name | Number | Description |
|------|--------|-------------|
| DQL_None | 0 |  |
| DQL_Set | 1 |  |
| DQL_Show | 2 |  |
| DQL_Select | 3 |  |
| DQL_Insert | 4 |  |
| DQL_Update | 5 |  |
| DQL_Delete | 6 |  |
| DQL_CreateSchema | 7 |  |
| DQL_CreateTable | 8 |  |
| DQL_AlterSchema | 9 |  |
| DQL_AlterTable | 10 |  |
| DQL_DropSchema | 11 |  |
| DQL_DropTable | 12 |  |
| DQL_Begin | 13 |  |
| DQL_Commit | 14 |  |
| DQL_Rollback | 15 |  |
| DQL_Discard | 16 |  |
| DQL_Prepare | 17 |  |
| DQL_Execute | 18 |  |
| DQL_Deallocate | 19 |  |
| DQL_Explain | 20 |  |



