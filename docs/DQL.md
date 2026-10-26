# Dynizer Query Language (DQL)

## Table of Contents

1. [Introduction](#introduction)
2. [Set](#set)
   1. [System Parameters](#system-parameters)
   2. [Array Styles](#array-styles)
3. [Show](#show)
4. [Create](#create)
   1. [Create Schema](#create-schema)
   2. [Create Action](#create-action)
      1. [Storage Parameters](#storage-parameters)
5. [Alter](#alter)
   1. [Alter Schema](#alter-schema)
   2. [Alter Action](#alter-action)
6. [Drop](#drop)
   1. [Drop Schema](#drop-schema)
   2. [Drop Action](#drop-action)
7. [Insert Into](#insert-into)
8. [Update](#update)
9. [Delete](#delete)
10. [Select](#select)
    1. [Select Columns](#select-columns)
    2. [Join Rows](#join-rows)
    3. [Filter Rows](#filter-rows)
    4. [Group Rows](#group-rows)
    5. [Order Rows](#order-rows)
    6. [Functions](#functions)
       1. [Global](#global)
       2. [Row](#row)
       3. [Aggregate](#aggregate)
       4. [Expand](#expand)
       5. [Instance](#instance)
       6. [Query](#query)
       7. [Dynizer](#dynizer)
11. [Query Flow](#query-flow)
    1. [Simple Query](#simple-query)
    2. [Parse](#parse)
    3. [Bind](#bind)
    4. [Describe](#describe)
    5. [Execute](#execute)
    6. [Sync](#sync)
    7. [Close](#close)
12. [Parameters](#parameters)
13. [Catalog tables](#catalog-tables)
    1. [Information Schema](#information-schema)
    2. [PG Catalog](#pg-catalog)
14. [Unsupported](#unsupported)
    1. [Plannned](#planned)
    2. [Unplanned](#unplanned)
15. [Example Case](#example-case)
    1. [Setting Session Parameters](#setting-session-parameters)
    2. [Showing Session Parameters](#showing-session-parameters)
    3. [Creating a Schema](#creating-a-schema)
    4. [Setting Search Path](#setting-search-path)
    5. [Creating an Action](#creating-an-action)
    6. [Deleting an Action](#deleting-an-action)
    7. [Inserting Data](#inserting-data)
    8. [Updating Data](#updating-data)
    9. [Deleting Data](#deleting-data)

## Introduction

The Dynizer Query Language (DQL) is a [Dynizer](https://www.consono.ai/technology) specific [SQL](https://en.wikipedia.org/wiki/SQL) language based on the [PostgreSQL](https://www.postgresql.org/) dialect to allow the user to manage schemas and data.

Apart from dedicated [gRPC](https://grpc.io/) & [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) endpoints, DQL queries can be used through the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html), which allows any existing database tool supporting PostgreSQL to be used for communication with the Dynizer.

For brevity, basic explanation and examples of the syntax are omitted in this document. For a full description please refer to the documentation of [PostgreSQL syntax](https://www.postgresql.org/docs/current/sql-syntax.html). A list of unsupported functionality and/or syntax can be found [here](#unsupported).

DQL strives for maximum compatibility with the [SQL](https://en.wikipedia.org/wiki/SQL) standard as well as the [PostgreSQL](https://www.postgresql.org/) dialect. Development however is still in progress and therefore full support is not guaranteed. If you come across an unsupported feature have a look in the [Unsupported](#unsupported) section for an overview of planned and unplanned features. Still don't find the feature in there? Send an e-mail to [dql\@consono.ai](mailto:dql@consono.ai?subject=Unsupported%20DQL%20Feature) and we will have a look.

## Set

The **SET** DQL query can be used to set key/value variables within the session. The query can be used to set certain system parameters, but it is not exclusively for this purpose. The user is allowed to set any key/value(s) pair, allowing the query to be used to store non-persistent data within the session. This differs to most regular SQL implementations. Note that it is not possible to share these parameters between multiple sessions, even if they are initiated by the same user.

### System Parameters

System parameters are parameters that can be set/modified to change the behaviour of the Dynizer within the session. A full description of each available system variable can be found in the below table. Note that not all parameters will be present when initiating a session through gRPC/REST. Some system variables are merely present to support certain PostgreSQL specific applications and report to them.

| Key                         | Value type | Default | Default (pgwire) | Description                                                                                                                                                                                                                                                                                                                                        |
| --------------------------- | ---------- | ------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| search_path                 | String     | user    | user             | One or more schema names to search when executing a query. For a full description refer to the [PostgreSQL search path documentation](https://www.postgresql.org/docs/current/ddl-schemas.html#DDL-SCHEMAS-PATH)                                                                                                                                   |
| array_style                 | String     | dynizer | postgres         | Sets the return format of columns containing multiple values. Available formats are: 'dynizer', 'postgres', 'csv', 'json', 'list'. An optional second value can be added to set configuration parameters for the format. A full description of formats and parameters can be found [below](#array-styles) this table.                              |
| group_by_match_null         | Boolean    |         |                  | If set to true, a GROUP BY clause will consider a comparison between value and NULL a match.                                                                                                                                                                                                                                                       |
| query_v3_session            | Boolean    | false   | true             | Whether the Dynizer is set to run in v3 query mode. The previous DQL engine (v2) is incomplete and will not be developed further. However it is still available when this parameter is set to 'false'. Note that this document only describes features available in v3, and the v2 engine is based on the [MySQL](https://www.mysql.com/) dialect. |
| application_name            | String     |         |                  | The application name of the client. Empty string if not given on startup.                                                                                                                                                                                                                                                                          |
| client_encoding             | String     |         | UTF8             | The client string encoding. Always 'UTF8'.                                                                                                                                                                                                                                                                                                         |
| server_encoding             | String     |         | UTF8             | The server string encoding. Always 'UTF8'.                                                                                                                                                                                                                                                                                                         |
| version                     | String     |         | 14.0             | The [PostgreSQL](https://www.postgresql.org/) version corresponding to the syntax and protocol implemented.                                                                                                                                                                                                                                        |
| server_version              | String     |         | 14.0             | The [PostgreSQL](https://www.postgresql.org/) version corresponding to the syntax and protocol implemented.                                                                                                                                                                                                                                        |
| standard_conforming_strings | String     |         | off              | This informs whether ordinary string literals ('...') treat backslashes literally. Always off.                                                                                                                                                                                                                                                     |
| integer_datetimes           | String     |         | on               | Reports support for 64-bit-integer dates and times. Always on.                                                                                                                                                                                                                                                                                     |
| is_superuser                | String     |         |                  | Reports whether the user has global admin privileges.                                                                                                                                                                                                                                                                                              |
| session_authorization       | String     |         |                  | Reports the user who authorized the session.                                                                                                                                                                                                                                                                                                       |
| transaction_isolation       | String     |         | read committed   | Reports the transaction isolation level. Always 'read committed'.                                                                                                                                                                                                                                                                                  |
| IntervalStyle               | String     |         | postgres         | Sets the display format for interval values. Always 'postgres'.                                                                                                                                                                                                                                                                                    |
| DateStyle                   | String     |         | ISO, MDY         | Sets the date style for timestamp values. Always 'ISO, MDY'.                                                                                                                                                                                                                                                                                       |
| TimeZone                    | String     |         | UTC              | Sets the time zone of timestamp values. Always 'UTC'.                                                                                                                                                                                                                                                                                              |

### Array styles

The Dynizer allows the user to define labels that can contain multiple values without explicitly defining the label as an array. Various options are available to configure the return table format for these cases. The _array_style_ system variable needs to be used to configure the return format. This parameter requires at least one value containing the name of the array style, optionally a second value can be provided to configure the array style further. See [System Parameters](#system-parameters) for more information on how to configure these parameters.

Below table describes the supported array styles. When the setting is configured to an unknown array style, the default 'dynizer' is used.

| Name     | Parameter | Description                                                                                                                                                                                                                                                 |
| -------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dynizer  | no        | Creates a result column for every value of the label. This can lead to a situation where a SELECT of labels returns more columns than selected in the query.                                                                                                |
| postgres | yes       | Creates a result column containing a 'postgres' array string of the values in the label. Set the parameter value to 'string' to string quote every value in the array.                                                                                      |
| json     | yes       | Creates a result column containing a JSON array string of the values in the label. Set the parameter value to 'string' to string quote every value in the array.                                                                                            |
| csv      | yes       | Creates a result column containing a CSV string of the values in the label. Set the parameter value to the desired separator character (default ',').                                                                                                       |
| list     | yes       | Creates a result column containing a comma separated list string of the values in the label. Set the parameter value to 'string' to string quote every value in the array. This will not always output valid CSV, so 'csv' is recommended for this purpose. |

## Show

The **SHOW** query can be used to display current session key/value parameters. Additionally the **SHOW ALL** query can be used to retrieve a table containing all parameters with a description (if there is any).

## Create

**CREATE** queries are used to define schemas, actions and labels to store data. As in most SQL implementations, all schema definitions are **case-insensitive**.

### Create Schema

The **CREATE SCHEMA** query is used to create a new action schema. Schemas are generally used to group related actions or restrict access to different areas of the data model. The **IF NOT EXISTS** keyword can be used to only create the schema if it does not already exist.

### Create Action

The **CREATE TABLE** query is used to create a new action. For standard SQL compatibility the **TABLE** keyword is used to refer to an action (although this might be aliased in the future). The **IF NOT EXISTS** keyword can be used to only create the action if it does not already exist. Action labels can be defined in the same way as columns are defined in a standard SQL implementation. It is also possible to use another action as a base by using the **AS** keyword and providing a **SELECT** query. The resulting labels from the **SELECT** query will then be used as the labels for the new action.

Dynizer does not support explicit indexing as of now, and it is currently not planned for development. Therefore it is not possible to use keywords such as **PRIMARY KEY**, **FOREIGN KEY** or any other index definition.

### Storage Parameters

The **CREATE TABLE** query makes use of storage parameters to read label definitions that are Dynizer specific. Storage parameters can be added to the query using the **WITH** keyword. Labels are always created with minimum and maximum values set to 0. It is currently not possible to change this using storage parameters but it is planned to be supported in the future. Refer to [Unsupported](#unsupported) for more information.

#### Data Types

The column definition in the query only allows Dynizer data types that match the native data types of [PostgreSQL](https://www.postgresql.org/). However, Dynizer supports a few additional data types (such as unsigned integer), which can be set using storage parameter 'default_data_types'. The value for the parameter needs to be a comma separated list of data types corresponding with the order they appear in the definition. The data type in the column definition is then ignored. It is allowed to pass a list with a lower number of data types. In this case it will still use the data type defined in the column definition for the labels that do not have a matching data type in the storage parameter.

The Dynizer supports defining alternative data types for an action label. It is currently unsupported to define this using DQL. Therefore all supported data types are added as alternative in every label. Configuration for this is planned to be supported in the future. Refer to [Unsupported](#unsupported) for more information.

A list of data types can be found in the below table.

| Name            | Postgres synonym | Description                                                                                                                                                                |
| --------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Integer         | int8             | Whole number (not a fractional number) that can be positive, negative, or zero.                                                                                            |
| String          | text             | Sequence of characters.                                                                                                                                                    |
| Boolean         | bool             | True or false.                                                                                                                                                             |
| Decimal         | numeric          | Numbers, which consist of two parts namely, a whole number part and a fractional part separated by a decimal point.                                                        |
| Timestamp       | timestamptz      | A sequence of characters representing both date and time of day.                                                                                                           |
| URI             | N/A              | Unique sequence of characters that identifies a logical or physical resource used by web technologies.                                                                     |
| Void            | void             | No value, explicit NULL.                                                                                                                                                   |
| Float           | float8           | Decimal values or fractional numbers.                                                                                                                                      |
| UnsignedInteger | N/A              | Whole number (not a fractional number) that can be positive or zero.                                                                                                       |
| Binary          | bytea            | Binary string.                                                                                                                                                             |
| UUID            | N/A              | 128-bit label used for information in computer systems.                                                                                                                    |
| Text            | text             | Sequence of characters, stored as a LOB. Searchable using Full-text index.                                                                                                 |
| Blob            | bytea            | Binary string, stored as a LOB.                                                                                                                                            |
| Clob            | text             | Sequence of characters, stored as a LOB. Not searchable using Full-text index.                                                                                             |
| Document        | N/A              | JSON document in the format of 'Dynizer Pipeline' output. Special indexing data type to store analysis output of unstructured documents. Searchable using Full-text index. |
| Date            | date             | A sequence of characters representing a date                                                                                                                               |
| Time            | timetz           | A sequence of characters representing a time of day                                                                                                                        |

#### Component Types

Every label created with standard SQL will by default be assigned component type 'What'. To be able to overwrite this Dynizer specific label information, the storage parameter 'component_types' can be used. The value for the parameter needs to be a comma separated list of component types corresponding with the order they appear in the definition.

A list of component types can be found in the below table.

| Name  | Description                                                                                                           |
| ----- | --------------------------------------------------------------------------------------------------------------------- |
| Who   | People, nationalities or religious or political groups, companies, agencies, institutions, etc.                       |
| What  | Everything that can not be defined as Who, Where or When.                                                             |
| Where | Buildings, airports, highways, bridges, countries, cities, states, mountain ranges, bodies of water, etc.             |
| When  | Absolute or relative dates or periods, times smaller than a day, named hurricanes, battles, wars, sports events, etc. |

## Alter

**ALTER** queries are used to change schemas, actions and labels. This feature is currently **unimplemented** but development is planned. Refer to [Unsupported](#unsupported) for more information.

### Alter Schema

The **ALTER SCHEMA** query is used to change a schema definition. This feature is currently **unimplemented** but development is planned. Refer to [Unsupported](#unsupported) for more information.

### Alter Action

The **ALTER TABLE** query is used to change an action definition. This feature is currently **unimplemented** but development is planned. Refer to [Unsupported](#unsupported) for more information.

## Drop

The **DROP** query is used to delete schemas, actions and labels. The **CASCADE** keyword can be used to force delete, if the to be deleted actions contain data.

### Drop Schema

The **DROP SCHEMA** query is used to delete a schema definition. This feature is currently **unimplemented** but development is planned. Refer to [Unsupported](#unsupported) for more information.

### Drop Action

The **DROP TABLE** query is used to delete an action and its data. If the action contains any data, the **CASCADE** keyword must be given, otherwise the query fails and the action is not deleted. The **IF EXISTS** keyword can be used to only delete the action if it is present.

## Insert Into

The **INSERT INTO** query is used to insert new data into an action. Optionally data can be inserted into specific columns if they are provided. The **VALUES** keyword can be used to insert one or more groups of literal values into the action. The label's default data type will be assigned to the corresponding values. If the value does not parse into the default data type, the query fails and no data is inserted. It is possible to insert multiple values for a label by adding one entry in the column list for each value to be inserted, and adding the values at the corresponding position in the **VALUES** clause. The order of the values will be determined by the order they appear in the columns list.

Alternative data types for the values can be passed using casting, but this feature is currently unimplemented. It is also not yet supported to insert data from a **SELECT** query. These features are planned for development. Refer to [Unsupported](#unsupported) for more information.

## Update

The **UPDATE** query is used to update instance values of an action. The **SET** keyword kan be used to provide the new values for each label. To select instances to update, the **WHERE** clause is used. Information about **WHERE** support can be found under the [**SELECT** Filter Rows Section](#filter-rows). Note that updating instances will always be a 'soft' update, as Dynizer retains history about updated/deleted instances.

It is currently not possible to update label values that are not on the first position. When a label value is updated, only the first value will be set and all other values that were present will be removed. Providing the label twice will only take the last appearing value into account. This is a known issue and therefore it is recommended to currently not use this query when dealing with multiple values. Development to address this is planned, although the syntax has not been fully decided. Refer to [Unsupported](#unsupported) for more information.

## Delete

The **DELETE** query is used to remove instances from an action. To select instances to delete, the **WHERE** clause is used. Information about **WHERE** support can be found under the [**SELECT** Filter Rows Section](#filter-rows). Note that deleting instances will always be a 'soft' delete, as Dynizer retains history about updated/deleted instances.

## Select

The **SELECT** query is used to read instances from one or more actions. It is also a possibility to perform a **SELECT** query without providing actions, which can be used to execute certain functions which do not relate to any actions. To filter instances from the result, conditions can also be used in the **WHERE** clause. A **JOIN** clause can be used to join actions based on a condition. Furthermore, instances can be grouped and sorted using the **GROUP BY** and **ORDER BY** clause, respectively.

### Select Columns

The **SELECT** clause of the query indicates the columns to be returned.

Action label names can be provided to read the values present in each instance for the respective action label. Alternatively, '\*' can be used to select all action labels of an action. Action label names can be qualified to specify the action the columns belongs too. This is necessary when two or more actions have an action label with the same name, as the query engine cannot differentiate which action label to display in this case. Qualifying can be done either by the full action name, or the alias if one is provided with the **AS** keyword. It is also possible to qualify '\*' to select all action labels of one action only. Action labels are either provided unquoted, or quoted with double quotes (") if there are any special characters (e.g. space character), or the action label has a name that is a reserved keyword (e.g. DISTINCT).

Functions can also be provided in the **SELECT** clause if applicable. Global, row, aggregate and expand functions can be used in this part of the query. They are used to retrieve variables, manipulate data from action labels, apply aggregates or expand one row to multiple rows based on the value(s) of the action label. For more information refer to the [Functions](#functions) section.

It is also possible to provide literal values. In this case each returned row in the result will contain that value at the given position. Boolean and integer literals can be given unquoted, while string literals need to be single quoted ('). No other literal data types are available without explicitly using _casting_.

Furthermore, a **CASE** statement can be provided to return values based on a certain given condition.

Conditions provided in the **SELECT** clause are currently unsupported but development is planned. Refer to [Unsupported](#unsupported) for more information. **Note that for driver compatibility the DQL query engine does not return an error if a condition is provided, and always returns 'true' for the condition, regardless of the condition provided.**

#### Casting

Columns provided in the **SELECT** clause can be casted to enforce a certain data type on the column(s). Cast data types can be provided by suffixing the column with two colons (::) and the data type. Currently only [PostgreSQL](https://www.postgresql.org/) native data types can be used in casting. Dynizer specific data types are unsupported but development is planned. Refer to [Unsupported](#unsupported) for more information.

Note that the query parser cannot determine if the value can be casted. This implies an error can be returned during query execution should it encounter a value which cannot be casted.

### Join Rows

The **JOIN** clause can be used to combine two actions based on a condition. Multiple condition can be specified by using the **AND** and **OR** operations. Not all conditions are currently supported. Refer to [Unsupported](#unsupported) for more information. A list of supported/unsupported conditions can be found in the below table. Note that in each case, the left and right can be switched.

The **NOT** keyword is currently unimplemented but development is planned. Refer to [Unsupported](#unsupported) for more information.

| Left         | Right        | Operator | Example                           | Supported |
| ------------ | ------------ | -------- | --------------------------------- | --------- |
| Action label |              | N/A      | label_name                        | NO        |
| Literal      |              | N/A      | true                              | YES       |
| Function     |              | N/A      | function()                        | YES       |
| Case         |              | N/A      | case when ... end                 | NO        |
| Action label | Action label | =        | label_name_a = label_name_b       | YES       |
| Action label | Action label | != OR <> | label_name_a != label_name_b      | NO        |
| Action label | Action label | >        | label_name_a > label_name_b       | NO        |
| Action label | Action label | <        | label_name_a < label_name_b       | NO        |
| Action label | Action label | >=       | label_name_a >= label_name_b      | NO        |
| Action label | Action label | <=       | label_name_a <= label_name_b      | NO        |
| Action label | Literal      | =        | label_name = true                 | YES       |
| Action label | Literal      | != OR <> | label_name != true                | YES       |
| Action label | Literal      | >        | label_name > 0                    | YES       |
| Action label | Literal      | <        | label_name < 0                    | YES       |
| Action label | Literal      | >=       | label_name >= 0                   | YES       |
| Action label | Literal      | <=       | label_name <= 0                   | YES       |
| Action label | Function     | =        | label_name = function()           | YES       |
| Action label | Function     | != OR <> | label_name_a != function()        | NO        |
| Action label | Function     | >        | label_name_a > function()         | NO        |
| Action label | Function     | <        | label_name_a < function()         | NO        |
| Action label | Function     | >=       | label_name_a >= function()        | NO        |
| Action label | Function     | <=       | label_name_a <= function()        | NO        |
| Action label | Case         | =        | label_name = case when ... end    | NO        |
| Action label | Case         | != OR <> | label_name_a != case when ... end | NO        |
| Action label | Case         | >        | label_name_a > case when ... end  | NO        |
| Action label | Case         | <        | label_name_a < case when ... end  | NO        |
| Action label | Case         | >=       | label_name_a >= case when ... end | NO        |
| Action label | Case         | <=       | label_name_a <= case when ... end | NO        |
| Action label | Condition    | =        | label_name = (a = b)              | NO        |
| Action label | Condition    | != OR <> | label_name_a != (a = b)           | NO        |
| Action label | Condition    | >        | label_name_a > (a = b)            | NO        |
| Action label | Condition    | <        | label_name_a < (a = b)            | NO        |
| Action label | Condition    | >=       | label_name_a >= (a = b)           | NO        |
| Action label | Condition    | <=       | label_name_a <= (a = b)           | NO        |
| Literal      | Literal      | =        | true = true                       | YES       |
| Literal      | Literal      | != OR <> | true != false                     | YES       |
| Literal      | Literal      | >        | 1 > 0                             | YES       |
| Literal      | Literal      | <        | 0 < 1                             | YES       |
| Literal      | Literal      | >=       | 1 >= 0                            | YES       |
| Literal      | Literal      | <=       | 0 <= 1                            | YES       |
| Literal      | Function     | =        | true = function()                 | NO        |
| Literal      | Function     | != OR <> | true != function()                | NO        |
| Literal      | Function     | >        | 1 > function()                    | NO        |
| Literal      | Function     | <        | 0 < function()                    | NO        |
| Literal      | Function     | >=       | 1 >= function()                   | NO        |
| Literal      | Function     | <=       | 0 <= function()                   | NO        |
| Literal      | Case         | =        | true = function()                 | NO        |
| Literal      | Case         | != OR <> | true != function()                | NO        |
| Literal      | Case         | >        | 1 > function()                    | NO        |
| Literal      | Case         | <        | 0 < function()                    | NO        |
| Literal      | Case         | >=       | 1 >= function()                   | NO        |
| Literal      | Case         | <=       | 0 <= function()                   | NO        |
| Literal      | Condition    | =        | true = (a = b)                    | NO        |
| Literal      | Condition    | != OR <> | true != (a = b)                   | NO        |
| Literal      | Condition    | >        | 1 > (a = b)                       | NO        |
| Literal      | Condition    | <        | 0 < (a = b)                       | NO        |
| Literal      | Condition    | >=       | 1 >= (a = b)                      | NO        |
| Literal      | Condition    | <=       | 0 <= (a = b)                      | NO        |
| Function     | Case         | =        | function() = case when ... end    | NO        |
| Function     | Case         | != OR <> | function() != case when ... end   | NO        |
| Function     | Case         | >        | function() > case when ... end    | NO        |
| Function     | Case         | <        | function() < case when ... end    | NO        |
| Function     | Case         | >=       | function() >= case when ... end   | NO        |
| Function     | Case         | <=       | function() <= case when ... end   | NO        |
| Function     | Condition    | =        | function() = (a = b)              | NO        |
| Function     | Condition    | != OR <> | function() != (a = b)             | NO        |
| Function     | Condition    | >        | function() > (a = b)              | NO        |
| Function     | Condition    | <        | function() < (a = b)              | NO        |
| Function     | Condition    | >=       | function() >= (a = b)             | NO        |
| Function     | Condition    | <=       | function() <= (a = b)             | NO        |
| Case         | Condition    | =        | case when ... end = (a = b)       | NO        |
| Case         | Condition    | != OR <> | case when ... end != (a = b)      | NO        |
| Case         | Condition    | >        | case when ... end > (a = b)       | NO        |
| Case         | Condition    | <        | case when ... end < (a = b)       | NO        |
| Case         | Condition    | >=       | case when ... end >= (a = b)      | NO        |
| Case         | Condition    | <=       | case when ... end <= (a = b)      | NO        |

### Filter Rows

The **WHERE** clause can be used to filter rows of the result table based on a condition. Multiple condition can be specified by using **AND** and **OR** operations. A condition can be negated by the using the **NOT** keyword. Not all conditions are currently supported. Refer to [Unsupported](#unsupported) for more information.

Casting can be used on an element of a condition to enforce the value to match with its data type only, contrary to the default type-independent match.

A list of supported/unsupported conditions can be found in the below table. Note that in each case, the left and right can be switched.

| Left         | Right        | Operator | Example                           | Supported |
| ------------ | ------------ | -------- | --------------------------------- | --------- |
| Action label |              | N/A      | label_name                        | YES       |
| Literal      |              | N/A      | true                              | YES       |
| Function     |              | N/A      | function()                        | YES       |
| Case         |              | N/A      | case when ... end                 | YES       |
| Action label | Action label | =        | label_name_a = label_name_b       | YES       |
| Action label | Action label | != OR <> | label_name_a != label_name_b      | NO        |
| Action label | Action label | >        | label_name_a > label_name_b       | NO        |
| Action label | Action label | <        | label_name_a < label_name_b       | NO        |
| Action label | Action label | >=       | label_name_a >= label_name_b      | NO        |
| Action label | Action label | <=       | label_name_a <= label_name_b      | NO        |
| Action label | Literal      | =        | label_name = true                 | YES       |
| Action label | Literal      | != OR <> | label_name != true                | YES       |
| Action label | Literal      | >        | label_name > 0                    | YES       |
| Action label | Literal      | <        | label_name < 0                    | YES       |
| Action label | Literal      | >=       | label_name >= 0                   | YES       |
| Action label | Literal      | <=       | label_name <= 0                   | YES       |
| Action label | Function     | =        | label_name = function()           | YES       |
| Action label | Function     | != OR <> | label_name_a != function()        | NO        |
| Action label | Function     | >        | label_name_a > function()         | NO        |
| Action label | Function     | <        | label_name_a < function()         | NO        |
| Action label | Function     | >=       | label_name_a >= function()        | NO        |
| Action label | Function     | <=       | label_name_a <= function()        | NO        |
| Action label | Case         | =        | label_name = case when ... end    | YES       |
| Action label | Case         | != OR <> | label_name_a != case when ... end | NO        |
| Action label | Case         | >        | label_name_a > case when ... end  | NO        |
| Action label | Case         | <        | label_name_a < case when ... end  | NO        |
| Action label | Case         | >=       | label_name_a >= case when ... end | NO        |
| Action label | Case         | <=       | label_name_a <= case when ... end | NO        |
| Action label | Condition    | =        | label_name = (a = b)              | NO        |
| Action label | Condition    | != OR <> | label_name_a != (a = b)           | NO        |
| Action label | Condition    | >        | label_name_a > (a = b)            | NO        |
| Action label | Condition    | <        | label_name_a < (a = b)            | NO        |
| Action label | Condition    | >=       | label_name_a >= (a = b)           | NO        |
| Action label | Condition    | <=       | label_name_a <= (a = b)           | NO        |
| Literal      | Literal      | =        | true = true                       | YES       |
| Literal      | Literal      | != OR <> | true != false                     | YES       |
| Literal      | Literal      | >        | 1 > 0                             | YES       |
| Literal      | Literal      | <        | 0 < 1                             | YES       |
| Literal      | Literal      | >=       | 1 >= 0                            | YES       |
| Literal      | Literal      | <=       | 0 <= 1                            | YES       |
| Literal      | Function     | =        | true = function()                 | YES       |
| Literal      | Function     | != OR <> | true != function()                | YES       |
| Literal      | Function     | >        | 1 > function()                    | YES       |
| Literal      | Function     | <        | 0 < function()                    | YES       |
| Literal      | Function     | >=       | 1 >= function()                   | YES       |
| Literal      | Function     | <=       | 0 <= function()                   | YES       |
| Literal      | Case         | =        | true = function()                 | YES       |
| Literal      | Case         | != OR <> | true != function()                | NO        |
| Literal      | Case         | >        | 1 > function()                    | NO        |
| Literal      | Case         | <        | 0 < function()                    | NO        |
| Literal      | Case         | >=       | 1 >= function()                   | NO        |
| Literal      | Case         | <=       | 0 <= function()                   | NO        |
| Literal      | Condition    | =        | true = (a = b)                    | NO        |
| Literal      | Condition    | != OR <> | true != (a = b)                   | NO        |
| Literal      | Condition    | >        | 1 > (a = b)                       | NO        |
| Literal      | Condition    | <        | 0 < (a = b)                       | NO        |
| Literal      | Condition    | >=       | 1 >= (a = b)                      | NO        |
| Literal      | Condition    | <=       | 0 <= (a = b)                      | NO        |
| Function     | Case         | =        | function() = case when ... end    | NO        |
| Function     | Case         | != OR <> | function() != case when ... end   | NO        |
| Function     | Case         | >        | function() > case when ... end    | NO        |
| Function     | Case         | <        | function() < case when ... end    | NO        |
| Function     | Case         | >=       | function() >= case when ... end   | NO        |
| Function     | Case         | <=       | function() <= case when ... end   | NO        |
| Function     | Condition    | =        | function() = (a = b)              | NO        |
| Function     | Condition    | != OR <> | function() != (a = b)             | NO        |
| Function     | Condition    | >        | function() > (a = b)              | NO        |
| Function     | Condition    | <        | function() < (a = b)              | NO        |
| Function     | Condition    | >=       | function() >= (a = b)             | NO        |
| Function     | Condition    | <=       | function() <= (a = b)             | NO        |
| Case         | Condition    | =        | case when ... end = (a = b)       | NO        |
| Case         | Condition    | != OR <> | case when ... end != (a = b)      | NO        |
| Case         | Condition    | >        | case when ... end > (a = b)       | NO        |
| Case         | Condition    | <        | case when ... end < (a = b)       | NO        |
| Case         | Condition    | >=       | case when ... end >= (a = b)      | NO        |
| Case         | Condition    | <=       | case when ... end <= (a = b)      | NO        |

### Group Rows

Rows can be grouped by using the **GROUP BY** clause. Each element in the **GROUP BY** clause must have a corresponding element in the **SELECT** clause. To refer to an entry in the **SELECT** clause, both an integer (1-based) as a name reference can be used. Note that the grouping occurs after the **WHERE** clause filter has been resolved and it is not possible to filter the result of the grouping.

If the setting _group_by_match_null_ has been set to true in the [System Parameters](#system-parameters), the group by will consider every comparison with NULL as equal. This implies no NULL values will be returned.

### Order Rows

Rows can be ordered by using the **ORDER BY** clause. Ordering will be based on the order the entries appear in the clause. Optionally, per element, the **DESC** keyword can be set to inverse the ordering. To refer to an entry in the **SELECT** clause, both an integer (1-based) as a name reference can be used. In contrary to a grouping clause, ordering can be done on an action label if it is not in the **SELECT** clause.

### Functions

Functions can be used in various parts of the DQL query to request information about the state of the system, perform specific query lookups, build virtual result tables, perform aggregates, modify the result output and more. They can either be executed standalone or compared to an action label by using them in a condition (e.g. label = function()). DQL has 7 main categories of functions: Global, Row, Aggregate, Expand, Instance, Query, Dynizer. Each category can be used in one or more parts of the query.

A list of all function categories and their corresponding functions can be found below. A table lists the arguments for functions with at least one argument.

#### Global

Global functions can be used to retrieve information about the state of the system or session or provide simple utilities.

Global functions can be used in the **SELECT**, **FROM** or **WHERE**\* clause.

\* except set-returning e.g. _generate_series_

##### current_user

Returns the current session user.

##### current_microsoft_user

Returns the ID of the currently logged in Microsoft user. If an argument is provided, returns the Microsoft user ID of the given Microsoft Single Sign-On JWT.

| Argument | Element type | Data type | Required | Description                  |
| -------- | ------------ | --------- | -------- | ---------------------------- |
| jwt      | Literal      | String    | NO       | Microsoft Single Sign-On JWT |

##### current_microsoft_user_teams

Returns the IDs of the teams that the currently logged in Microsoft user is a member of. If an argument is provided, returns the IDs of the teams that the user in the given Microsoft Single Sign-On JWT is a member of.

| Argument | Element type | Data type | Required | Description                  |
| -------- | ------------ | --------- | -------- | ---------------------------- |
| jwt      | Literal      | String    | NO       | Microsoft Single Sign-On JWT |

##### current_schema

Returns the current schema defined in [System Parameter](#system-parameters) _search_path_.

##### current_schemas

Returns the current schema defined in [System Parameter](#system-parameters) _search_path_, with an option to include implicit schemas.

| Argument         | Element type | Data type | Required | Description              |
| ---------------- | ------------ | --------- | -------- | ------------------------ |
| include_implicit | Literal      | Boolean   | YES      | Include implicit schemas |

##### current_database

Returns the current database. Since the Dynizer does not have a concept such as database, it always returns 'dynizer'.

##### version

Returns the current [PostgreSQL](https://www.postgresql.org/) Server version used for the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html). Function for driver compatibility.

##### pg_encoding_to_char

System function for converting an encoding's internal identifier to a human-readable name. Function for driver compatibility, always returns 'UTF-8'.

| Argument    | Element type | Data type | Required | Description |
| ----------- | ------------ | --------- | -------- | ----------- |
| encoding_id | Literal      | Any       | YES      | Encoding ID |

##### pg_total_relation_size

System function determining the total on-disk size of a relation, including data and any indexes. Function for driver compatibility, always returns 0.

| Argument | Element type | Data type | Required | Description   |
| -------- | ------------ | --------- | -------- | ------------- |
| relation | Action label | N/A       | YES      | Relation name |

##### pg_relation_size

System function for determining the on-disk size of a particular fork of a relation. Function for driver compatibility, always returns 0.

| Argument | Element type | Data type | Required | Description   |
| -------- | ------------ | --------- | -------- | ------------- |
| relation | Action label | N/A       | YES      | Relation name |

##### pg_stat_get_numscans

Statistics view showing statistics about accesses to each index in the current database. Function for driver compatibility, always returns 0.

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| scans    | Literal      | Any       | YES      | Scans       |

##### pg_get_expr

System function which decompiles an expression stored as a pg_node_tree value into text suitable for inclusion into an SQL statement. Function for driver compatibility, always returns NULL.

##### pg_get_partkeydef

System function returning the definition of a partitioning key. Function for driver compatibility, always returns NULL.

##### pg_tablespace_location

System function returning the file system path of the specified tablespace. Function for driver compatibility, always returns NULL.

| Argument       | Element type | Data type | Required | Description    |
| -------------- | ------------ | --------- | -------- | -------------- |
| tablespace_oid | Literal      | Any       | YES      | Tablespace OID |

##### pg_get_constraintdef

System function for obtaining the definition of a constraint. Function for driver compatibility, always returns NULL.

| Argument       | Element type | Data type | Required | Description    |
| -------------- | ------------ | --------- | -------- | -------------- |
| constraint_oid | Literal      | Any       | YES      | Constraint OID |

##### generate_series

Generates a series of values from start to stop, with a step size of step. Step is always 1 and start and stop can only be integer. This is mainly a function for driver compatibility, but it can be used in any context.

| Argument | Element type | Data type | Required | Description  |
| -------- | ------------ | --------- | -------- | ------------ |
| start    | Literal      | Integer   | YES      | Series start |
| stop     | Literal      | Integer   | YES      | Series stop  |

##### current_time

Returns the current time, in UTC.

##### current_date

Returns the current date, in UTC.

##### current_timestamp

Returns the current timestamp, in UTC.

##### current_setting

Returns the [System Parameter] setting for the argument passed.

| Argument  | Element type | Data type | Required | Description           |
| --------- | ------------ | --------- | -------- | --------------------- |
| parameter | Literal      | String    | YES      | System parameter name |

#### Row

Row functions can be used to modify elements in a table. Most frequently these function are used in the **SELECT** clause, but it is also supported to use them in the **WHERE** clause as part of a comparison. Note that using row modifying functions in the **WHERE** requires the full result of the query to be read and temporary indexed, which can impact query performance drastically.

##### +

Adds two values.

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| left     | Literal      | Numeric   | YES      | Left value  |
| right    | Literal      | Numeric   | YES      | Right value |

##### -

Subtracts two values.

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| left     | Literal      | Numeric   | YES      | Left value  |
| right    | Literal      | Numeric   | YES      | Right value |

##### \*

Multiplies two values.

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| left     | Literal      | Numeric   | YES      | Left value  |
| right    | Literal      | Numeric   | YES      | Right value |

##### /

Divides two values.

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| left     | Literal      | Numeric   | YES      | Left value  |
| right    | Literal      | Numeric   | YES      | Right value |

##### ^

Applies power of right value to left value.

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| left     | Literal      | Numeric   | YES      | Left value  |
| right    | Literal      | Numeric   | YES      | Right value |

##### || (concat)

Concats two values. Can be called by operator or function name.

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| left     | Literal      | Any       | YES      | Left value  |
| right    | Literal      | Any       | YES      | Right value |

##### [*] (action_label_position)

Retrieves a value for an action label at given position. Can be used as array indexing or function call. Returns NULL if the action label has less values than the position given.

| Argument     | Element type | Data type       | Required | Description    |
| ------------ | ------------ | --------------- | -------- | -------------- |
| action_label | Action label | N/A             | YES      | Action label   |
| position     | Literal      | UnsignedInteger | YES      | Value position |

##### has_schema_privilege

System function determining whether the current user has the specified privilege for the specified schema.

Privilege options:

- SELECT
- INSERT
- UPDATE
- DELETE
- CREATE
- TRUNCATE
- CONNECT
- USAGE
- REFERENCES
- TRIGGER
- TEMPORARY
- EXECUTE
- SET
- ALTER SYSTEM

| Argument      | Element type  | Data type       | Required | Description   |
| ------------- | ------------- | --------------- | -------- | ------------- |
| action_schema | Action schema | N/A             | YES      | Action schema |
| privilege     | Literal       | UnsignedInteger | YES      | Privilege     |

##### has_table_privilege

System function determining whether the current user has the specified privilege for the specified action.

Privilege options:

- SELECT
- INSERT
- UPDATE
- DELETE
- CREATE
- TRUNCATE
- CONNECT
- USAGE
- REFERENCES
- TRIGGER
- TEMPORARY
- EXECUTE
- SET
- ALTER SYSTEM

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| action    | Action       | N/A             | YES      | Action      |
| privilege | Literal      | UnsignedInteger | YES      | Privilege   |

##### has_any_column_privilege

System function determining whether the current user has the specified privilege for one or more action labels of an action.

Privilege options:

- SELECT
- INSERT
- UPDATE
- DELETE
- CREATE
- TRUNCATE
- CONNECT
- USAGE
- REFERENCES
- TRIGGER
- TEMPORARY
- EXECUTE
- SET
- ALTER SYSTEM

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| action    | Action       | N/A             | YES      | Action      |
| privilege | Literal      | UnsignedInteger | YES      | Privilege   |

##### encode_base64

Converts the given value to base64.

| Argument | Element type                        | Data type | Required | Description      |
| -------- | ----------------------------------- | --------- | -------- | ---------------- |
| value    | Action label or function or literal | Any       | YES      | Value to convert |

##### decode_base64

Converts the given value from base64.

| Argument | Element type                        | Data type | Required | Description      |
| -------- | ----------------------------------- | --------- | -------- | ---------------- |
| value    | Action label or function or literal | Any       | YES      | Value to convert |

##### lob_to_base64

Converts the given LOB to base64. Leaves any value that is not a LOB untouched.

| Argument | Element type                        | Data type | Required | Description      |
| -------- | ----------------------------------- | --------- | -------- | ---------------- |
| value    | Action label or function or literal | Any       | YES      | Value to convert |

##### lob_to_string

Converts a given LOB to string and returns the full LOB content. Leaves any value that is not a LOB untouched. Note that, when used with no window, this function might cause a query to fetch a very large amount of data depending on the LOB sizes.

| Argument | Element type                        | Data type | Required | Description      |
| -------- | ----------------------------------- | --------- | -------- | ---------------- |
| value    | Action label or function or literal | Any       | YES      | Value to convert |

##### json_path

Does a [JSON path](https://www.ietf.org/archive/id/draft-goessner-dispatch-jsonpath-00.html) query on the given value. If the value is not valid JSON, or the JSON path did not evaluate to any key, the error reading/querying the JSON is returned.

| Argument | Element type                        | Data type | Required | Description     |
| -------- | ----------------------------------- | --------- | -------- | --------------- |
| value    | Action label or function or literal | Any       | YES      | Value to query  |
| query    | Literal                             | Any       | YES      | JSON path query |

##### lower

Converts the given value to lowercase.

| Argument | Element type                        | Data type | Required | Description     |
| -------- | ----------------------------------- | --------- | -------- | --------------- |
| value    | Action label or function or literal | Any       | YES      | Value to modify |

##### array_upper

Returns the upper bound of the requested array dimension.

| Argument  | Element type                        | Data type       | Required | Description               |
| --------- | ----------------------------------- | --------------- | -------- | ------------------------- |
| value     | Action label or function or literal | Any             | YES      | Array value               |
| dimension | Literal                             | UnsignedInteger | YES      | Requested array dimension |

##### format_type

System function which returns the human-readable name of a data type from its ID. The second argument is ignored and is merely there for compatibility reasons.

| Argument     | Element type | Data type       | Required | Description   |
| ------------ | ------------ | --------------- | -------- | ------------- |
| data_type_id | Literal      | UnsignedInteger | YES      | Data type ID  |
| typemod      | Literal      | Any             | YES      | Type modifier |

##### nullif

Returns a null value if argument_1 equals argument_2, otherwise it returns argument_1.

| Argument   | Element type                        | Data type | Required | Description |
| ---------- | ----------------------------------- | --------- | -------- | ----------- |
| argument_1 | Action label or function or literal | Any       | YES      | Argument 1  |
| argument_2 | Action label or function or literal | Any       | YES      | Argument 2  |

##### score

Returns the text search/similarity search score of a result label. This function should only be used in combination with the **Query** function [text_search](#text_search) or [similarity_search](#similarity_search), however using it without one of these functions will just result in NULL being returned.
The score returned is currently a floating point number that varies between 0-10 (but in rare cases could exceed 10).

When both text_search and similarity search are combined, the score is aggregated.

The scoring system might move to a normalised version soon. Refer to [Unsupported](#unsupported) for more information.

| Argument   | Element type | Data type | Required | Description  |
| ---------- | ------------ | --------- | -------- | ------------ |
| argument_1 | Action label | Any       | YES      | Action label |

##### fixed

Returns a floating point or decimal number to be of given fixed precision (rounded).

| Argument  | Element type                        | Data type       | Required | Description |
| --------- | ----------------------------------- | --------------- | -------- | ----------- |
| value     | Action label or function or literal | Numeric         | YES      | Value       |
| precision | Literal                             | UnsignedInteger | YES      | Precision   |

##### csv

Returns a CSV row of the parameters using given separator. The last function parameter is variable, at least one parameter must be given to build the rows, but multiple can be provided.

| Argument  | Element type                        | Data type         | Required | Description |
| --------- | ----------------------------------- | ----------------- | -------- | ----------- |
| separator | Literal                             | String (length 1) | YES      | Separator   |
| ...value  | Action label or function or literal | UnsignedInteger   | YES      | Value(s)    |

##### array

Returns an array of the parameters using the configured [Array Style](#array-styles). The function parameter is variable, at least one parameter must be given to build the rows, but multiple can be provided.

| Argument | Element type                        | Data type       | Required | Description |
| -------- | ----------------------------------- | --------------- | -------- | ----------- |
| ...value | Action label or function or literal | UnsignedInteger | YES      | Value(s)    |

##### array_value

Returns an array of the parameters using the configured [Array Style](#array-styles). The function parameter is variable, at least one parameter must be given to build the rows, but multiple can be provided.

This variant of the _array_ function ensures literals are returned as their data type, and not quoted as strings.

| Argument | Element type                        | Data type       | Required | Description |
| -------- | ----------------------------------- | --------------- | -------- | ----------- |
| ...value | Action label or function or literal | UnsignedInteger | YES      | Value(s)    |

##### array_string

Returns an array of the parameters using the configured [Array Style](#array-styles). The function parameter is variable, at least one parameter must be given to build the rows, but multiple can be provided.

This variant of the _array_ function ensures literals are returned as quoted strings.

| Argument | Element type                        | Data type       | Required | Description |
| -------- | ----------------------------------- | --------------- | -------- | ----------- |
| ...value | Action label or function or literal | UnsignedInteger | YES      | Value(s)    |

##### json

Returns a JSON of the parameters using the configured [Array Style](#array-styles). The function parameter is variable, at least one parameter must be given to build the rows, but multiple can be provided.

Result label names serve as keys in the resulting JSON.

| Argument | Element type                        | Data type       | Required | Description |
| -------- | ----------------------------------- | --------------- | -------- | ----------- |
| ...value | Action label or function or literal | UnsignedInteger | YES      | Value(s)    |

##### json_data_element

Returns a JSON of the parameters using the configured [Array Style](#array-styles). The function parameter is variable, at least one parameter must be given to build the rows, but multiple can be provided.

Result label names serve as keys in the resulting JSON. Returns an object for the return value containing the string literal value and the data type.

| Argument | Element type                        | Data type       | Required | Description |
| -------- | ----------------------------------- | --------------- | -------- | ----------- |
| ...value | Action label or function or literal | UnsignedInteger | YES      | Value(s)    |

##### substr (substring)

Extracts a specific number of characters from a particular position of a string. The last parameter is optional and will default to all characters after the start position. Can be called as both _substr_ and _substring_.

| Argument             | Element type                        | Data type       | Required | Description                  |
| -------------------- | ----------------------------------- | --------------- | -------- | ---------------------------- |
| value                | Action label or function or literal | Any             | YES      | Value                        |
| position_from        | Literal                             | UnsignedInteger | YES      | Position to start index      |
| number_of_characters | Literal                             | UnsignedInteger | NO       | Number of characters to keep |

##### strpos

Locates the starting position of a substring within a string.

| Argument  | Element type                        | Data type | Required | Description                       |
| --------- | ----------------------------------- | --------- | -------- | --------------------------------- |
| value     | Action label or function or literal | Any       | YES      | string to search                  |
| substring | Literal                             | String    | YES      | substring to locate within string |

##### left

Extracts n number of characters specified in the argument from the left of a given string. When the value of n is negative, the extraction will happen from left except last n characters.

| Argument | Element type                        | Data type | Required | Description         |
| -------- | ----------------------------------- | --------- | -------- | ------------------- |
| value    | Action label or function or literal | Any       | YES      | string to extract   |
| n        | Literal                             | Integer   | YES      | extraction position |

##### right

Extracts n number of characters specified in the argument from the right of a given string. When the value of n is negative, the extraction will happen from right except last n characters.

| Argument | Element type                        | Data type | Required | Description         |
| -------- | ----------------------------------- | --------- | -------- | ------------------- |
| value    | Action label or function or literal | Any       | YES      | string to extract   |
| n        | Literal                             | Integer   | YES      | extraction position |

##### coalesce

Returns the first non-null value in given arguments. The function parameter is variable, at least one parameter must be given to build the rows, but multiple can be provided.

| Argument | Element type                        | Data type | Required | Description             |
| -------- | ----------------------------------- | --------- | -------- | ----------------------- |
| ...value | Action label or function or literal | Any       | YES      | value to check for NULL |

##### chunk_score

Returns the score of the chunk for each row created with expand function [chunk_range](#chunk_range).

| Argument        | Element type                        | Data type | Required | Description                                                    |
| --------------- | ----------------------------------- | --------- | -------- | -------------------------------------------------------------- |
| Action Label    | Action label                        | N/A       | YES      | The label that was used in corresponding call to 'chunk_range' |

##### chunk_sentence_range

Returns the sentence range of the chunk for each row created with expand function [chunk_range](#chunk_range). Only returns a value if the value is of type 'Document'.

| Argument        | Element type                        | Data type | Required | Description                                                    |
| --------------- | ----------------------------------- | --------- | -------- | -------------------------------------------------------------- |
| Action Label    | Action label                        | N/A       | YES      | The label that was used in corresponding call to 'chunk_range' |

##### chunk_text

Returns the text of the chunk for each row created with expand function [chunk_range](#chunk_range).

| Argument        | Element type                        | Data type | Required | Description                                                    |
| --------------- | ----------------------------------- | --------- | -------- | -------------------------------------------------------------- |
| Action Label    | Action label                        | N/A       | YES      | The label that was used in corresponding call to 'chunk_range' |

#### Aggregate

Aggregate functions compute a single result from a result table. Aggregate functions can only be used in the **SELECT** clause.

##### count

Returns the number of rows of the given action label. NULL values are not counted. '\*' counts all rows.

| Argument | Element type                        | Data type | Required | Description |
| -------- | ----------------------------------- | --------- | -------- | ----------- |
| value    | Action label or function or literal | Any       | YES      | Value       |

##### sum

Returns the sum of all numeric values in the rows of the given action label. '\*' as a special case computes the sum of all numeric values in the table.

| Argument | Element type                        | Data type | Required | Description |
| -------- | ----------------------------------- | --------- | -------- | ----------- |
| value    | Action label or function or literal | Any       | YES      | Value       |

##### avg

Returns the average of all numeric values in the rows of the given action label. '\*' as a special case computes the average of all numeric values in the table.

| Argument | Element type                        | Data type | Required | Description |
| -------- | ----------------------------------- | --------- | -------- | ----------- |
| value    | Action label or function or literal | Any       | YES      | Value       |

##### min

Returns the minimum of all numeric values in the rows of the given action label. '\*' as a special case computes the minimum of all values in the table.

| Argument | Element type                        | Data type | Required | Description |
| -------- | ----------------------------------- | --------- | -------- | ----------- |
| value    | Action label or function or literal | Any       | YES      | Value       |

##### max

Returns the maximum of all numeric values in the rows of the given action label. '\*' as a special case computes the maximum of all values in the table.

| Argument | Element type                        | Data type | Required | Description |
| -------- | ----------------------------------- | --------- | -------- | ----------- |
| value    | Action label or function or literal | Any       | YES      | Value       |

##### string_agg

Concatenates a list of strings and places a separator between them. The function does not add the separator at the end of the string.

| Argument  | Element type                        | Data type | Required | Description |
| --------- | ----------------------------------- | --------- | -------- | ----------- |
| value     | Action label or function or literal | Any       | YES      | Value       |
| separator | Literal                             | String    | YES      | Separator   |

#### Expand

Expand functions are functions that can shrink or expand the number of result rows. Expand functions can only be used in the **SELECT** clause.

##### to_rows

Creates a row for every value of an action label that is not NULL instead of returning multiple values for the label.

| Argument     | Element type                        | Data type | Required | Description  |
| ------------ | ----------------------------------- | --------- | -------- | ------------ |
| Action label | Action label or function or literal | N/A       | YES      | Action label |

##### chunk_range

Creates a row for each chunk returned from the vector index using [similarity_search](#similarity_search) for given label.

| Argument     | Element type                        | Data type | Required | Description                                               |
| ------------ | ----------------------------------- | --------- | -------- | --------------------------------------------------------- |
| Action label | Action label                        | N/A       | YES      | The action label containing the similarity search results |

#### Instance

Instance functions are functions that retrieve information of the instance record. Instance functions can be used in the **SELECT** and **WHERE** clause.

Instance functions can and sometimes need to be scoped by preceding the function name with the action name (or alias), separated by a dot. In case of a **JOIN** clause, scoping is necessary to indicate which action to read the instance information from.

##### instance_id

Returns the instance ID.

##### instance_timestamp

Returns the instance insert timestamp.

##### instance_deleted_timestamp

Returns the instance deleted timestamp. Returns NULL if the instance is not deleted.

#### Query

Query functions can be used to perform specific filters on the data and can only be used in the **WHERE** clause.

It is possible to scope any query function to an action to limit the function to the data of that action only. This can be achieved by preceding the function name with the action name (or alias), separated by a dot.

##### text_search

Excludes all rows that did not match the given search value or query. A second optional argument can be provided to override the default text search mode _query_string_.
This function can be used in combination with the [score](#score) function to retrieve the score for elements in a row.

The following text search modes are supported:

###### query_string

This text search mode allows to describe complex queries using a simple syntax. Note that Dynizer text indexes all eligible values as trigrams, meaning that the value 'test' will index two values, both 'tes' and 'est' and keep track of their position. It is possible to configure Dynizer to use a different indexing algorithm, but this is beyond the scope of this document. It is however an important detail to understand how the text search query language can be used optimally for different scenarios.

**Trigram**: Non-quoted strings (split by spaces) performs a trigram search. Searching for value `'water'` will return matches for 'water', 'term', 'atelier', 'water supply', ...\
**Term/Phrase** Quoted strings (split by spaces outside of quotes) performs a term/phrase search. Searching for value `'"water"'` will match any string containing the complete quoted value, such as 'water', 'water supply', ... Spaces within quotes are taken into account, meaning that a search for `'"water supply"'` does not return 'watersupply', but a search for `'"water" "supply"'` does.\
**Regular Expressions** Wrapped expression in forward slashes (/). Searching for value `/"water (supply|tank)"/` will perform a regular expression on the wrapped value. Note that regular expressions which are not quoted will perform a regex search for trigrams only, which will not be useful in almost every scenario. Quote the regex field to perform a term/phrase search.\
**Required, Optional, and Exclusion** When your query string includes multiple items (split by spaces outside of quotes), by default these are placed into the SHOULD clause of a query. You can change this by prefixing your items with a '+' or '-'. Prefixing with '+' places that item in the MUST portion of the query. Prefixing with a '-' places that item in the MUST NOT portion of the query. Searching for `'+"water" -"supply" "tank"'` will match values 'water', 'water tank' and not 'water supply'.\
**Boosting** ^ operator followed by a number after the search value. Influences the relative importance of the clause. Matches for `'"water" "supply"^5 "tank"^2'` will score higher for value 'supply' than 'tank' and 'water', respectively.\
**Numeric ranges** >, >=, <, and <= operators, followed by a numeric value. Searching `'>10'` will match numbers greater than ten.\
**Date Ranges** >, >=, <, and <= operators, followed by a date value in quotes. `'>"2016-09-21"'` will match timestamps after September 21, 2016.\
**Escaping** The following quoted string enumerates the characters which may be escaped: `"+-=&|><!(){}[]^\"~\*?:\\/ "`\
**Field scoping** Query value prefixed with the name of the field separated by a colon. Searches for specific fields within **indexed documents** only. Indexed documents are results of the **Dynizer Pipeline** that have been inserted as data type _Document_ and contain the resulting full analysis of the document. Dynizer pipelines are beyond the scope of this document. Refer to the **Dynizer Pipeline** documentation for further information on how these documents are processed. The fields that can be used to search a document can be found in the below table.\

| Field       | Description                                          |
| ----------- | ---------------------------------------------------- |
| **text**    | **Full text of the document. Default field.**        |
| who         | All elements marked as WHO.                          |
| what        | All elements marked as WHAT.                         |
| where       | All elements marked as WHERE.                        |
| when        | All elements marked as WHEN.                         |
| action      | All elements marked as ACTION.                       |
| person      | People, including fictional.                         |
| norp        | Nationalities or religious or political groups.      |
| fac         | Buildings, airports, highways, bridges, etc.         |
| org         | Companies, agencies, institutions, etc.              |
| gpe         | Countries, cities, states.                           |
| loc         | Non-GPE locations, mountain ranges, bodies of water. |
| product     | Objects, vehicles, foods, etc. (Not services.)       |
| event       | Named hurricanes, battles, wars, sports events, etc. |
| work_of_art | Titles of books, songs, etc.                         |
| law         | Named documents made into laws.                      |
| language    | Any named language.                                  |
| date        | Absolute or relative dates or periods.               |
| time        | Times smaller than a day.                            |
| percent     | Percentage, including "%".                           |
| money       | Monetary values, including unit.                     |
| quantity    | Measurements, as of weight or distance.              |
| ordinal     | "first", "second", etc.                              |
| cardinal    | Numerals that do not fall under another type.        |
| numeric     | Parsed numerics found in the document.               |
| timestamp   | Parsed timestamps found in the document.             |

###### match_phrase

This text search mode performs a term/phrase search on the full given string value.

###### web_style

This text search mode provides a different, less extensive query language based on web search engines.

**Term/Phrase** Quoted strings (split by spaces outside of quotes) performs a term/phrase search. Searching for value `'"water supply"'` will match any string containing the complete quoted value, such as 'water supply', 'water supply tank', ... Spaces within quotes are taken into account, meaning that a search for `'"water supply"'` does not return 'watersupply', but a search for `'"water" "supply"'` does.\
**Required, Optional, and Exclusion** When your query string includes multiple items (split by spaces outside of quotes), by default these are placed into the MUST clause of a query. You can change this by using the 'AND', 'OR', '-' keywords. Separating with 'OR' places that item in the SHOULD portion of the query. Prefixing with a '-' places that item in the MUST NOT portion of the query. Searching for `'water -supply OR tank'` will match values 'water', 'water tank' and not 'water supply'.\
**Wildcard** '\*' operator. Wildcard matching any word or phrase.\

| Argument         | Element type | Data type | Required | Description                                              |
| ---------------- | ------------ | --------- | -------- | -------------------------------------------------------- |
| search_value     | Literal      | String    | YES      | Text search query string (interpreted depending on mode) |
| text_search_mode | Literal      | String    | NO       | Text search mode (default _query_string_)                |

##### similarity_search

Excludes all rows that did not match the given search value's nearest neighbours. The second argument must be provided to specify the amount of nearest neighbours to return.
This function can be used in combination with the [score](#score) function to retrieve the score for elements in a row as well as with the [chunk_range](#chunk_range) function to expand the result into the chunks found in the value.

| Argument         | Element type | Data type          | Required | Description                            |
| ---------------- | ------------ | ------------------ | -------- | -------------------------------------- |
| search_value     | Literal      | String             | YES      | Similarity search query string         |
| k                | Literal      | UnsignedInteger    | YES      | Amount of nearest neighbours to return |

##### metadata_key

Excludes all rows that do not contain given metadata key.

| Argument     | Element type | Data type | Required | Description  |
| ------------ | ------------ | --------- | -------- | ------------ |
| metadata_key | Literal      | String    | YES      | Metadata key |

##### metadata_key_value

Excludes all rows that do not contain given metadata key and value.

| Argument       | Element type | Data type | Required | Description    |
| -------------- | ------------ | --------- | -------- | -------------- |
| metadata_key   | Literal      | String    | YES      | Metadata key   |
| metadata_value | Literal      | String    | YES      | Metadata value |

##### instance_metadata_key

Excludes all rows that do not contain given instance metadata key.

| Argument     | Element type | Data type | Required | Description  |
| ------------ | ------------ | --------- | -------- | ------------ |
| metadata_key | Literal      | String    | YES      | Metadata key |

##### instance_metadata_key_value

Excludes all rows that do not contain given instance metadata key and value.

| Argument       | Element type | Data type | Required | Description    |
| -------------- | ------------ | --------- | -------- | -------------- |
| metadata_key   | Literal      | String    | YES      | Metadata key   |
| metadata_value | Literal      | String    | YES      | Metadata value |

##### cell_metadata_key

Excludes all rows that do not contain given cell metadata key.

| Argument     | Element type | Data type | Required | Description  |
| ------------ | ------------ | --------- | -------- | ------------ |
| metadata_key | Literal      | String    | YES      | Metadata key |

##### cell_metadata_key_value

Excludes all rows that do not contain given cell metadata key and value.

| Argument       | Element type | Data type | Required | Description    |
| -------------- | ------------ | --------- | -------- | -------------- |
| metadata_key   | Literal      | String    | YES      | Metadata key   |
| metadata_value | Literal      | String    | YES      | Metadata value |

##### component

Excludes all rows that do not contain given component (who, what, where, when).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| component | Literal      | String    | YES      | Component   |

##### data_type

Excludes all rows that do not contain a value of given data type.

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| data_type | Literal      | String    | YES      | Data type   |

##### position_index

Excludes all rows that do not contain any value for any label at given position.

| Argument | Element type | Data type       | Required | Description |
| -------- | ------------ | --------------- | -------- | ----------- |
| position | Literal      | UnsignedInteger | YES      | Position    |

##### metadata_position

Excludes all rows that do not contain any value for any label at given position in the metadata.

| Argument | Element type | Data type       | Required | Description |
| -------- | ------------ | --------------- | -------- | ----------- |
| position | Literal      | UnsignedInteger | YES      | Position    |

##### metadata_data_type

Excludes all rows that do not contain a metadata value of given data type.

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| data_type | Literal      | String    | YES      | Data type   |

##### value

Excludes all rows that do not contain given value (case-insensitive).

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| value    | Literal      | Any       | YES      | Value       |

##### exact

Excludes all rows that do not contain given value (case-sensitive).

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| value    | Literal      | Any       | YES      | Value       |

##### metadata_value

Excludes all rows that do not contain given value in the metadata (case-insensitive).

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| value    | Literal      | Any       | YES      | Value       |

##### metadata_exact

Excludes all rows that do not contain given value in the metadata (case-sensitive).

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| value    | Literal      | Any       | YES      | Value       |

##### data_type_value

Excludes all rows that do not contain given value of given data type (case-insensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| data_type | Literal      | String    | YES      | Data type   |
| value     | Literal      | Any       | YES      | Value       |

##### data_type_exact

Excludes all rows that do not contain given value of given data type (case-sensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| data_type | Literal      | String    | YES      | Data type   |
| value     | Literal      | Any       | YES      | Value       |

##### data_type_metadata_value

Excludes all rows that do not contain given value of given data type in the metadata (case-insensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| data_type | Literal      | String    | YES      | Data type   |
| value     | Literal      | Any       | YES      | Value       |

##### data_type_metadata_exact

Excludes all rows that do not contain given value of given data type in the metadata (case-sensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| data_type | Literal      | String    | YES      | Data type   |
| value     | Literal      | Any       | YES      | Value       |

##### position_value

Excludes all rows that do not contain given value at given position (case-insensitive).

| Argument | Element type | Data type       | Required | Description |
| -------- | ------------ | --------------- | -------- | ----------- |
| position | Literal      | UnsignedInteger | YES      | Position    |
| value    | Literal      | Any             | YES      | Value       |

##### position_exact

Excludes all rows that do not contain given value at given position (case-sensitive).

| Argument | Element type | Data type       | Required | Description |
| -------- | ------------ | --------------- | -------- | ----------- |
| position | Literal      | UnsignedInteger | YES      | Position    |
| value    | Literal      | Any             | YES      | Value       |

##### position_metadata_value

Excludes all rows that do not contain given value at given position in the metadata (case-insensitive).

| Argument | Element type | Data type       | Required | Description |
| -------- | ------------ | --------------- | -------- | ----------- |
| position | Literal      | UnsignedInteger | YES      | Position    |
| value    | Literal      | Any             | YES      | Value       |

##### position_metadata_exact

Excludes all rows that do not contain given value at given position in the metadata (case-sensitive).

| Argument | Element type | Data type       | Required | Description |
| -------- | ------------ | --------------- | -------- | ----------- |
| position | Literal      | UnsignedInteger | YES      | Position    |
| value    | Literal      | Any             | YES      | Value       |

##### component_value

Excludes all rows that do not contain given value with given component (case-insensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| component | Literal      | String    | YES      | Component   |
| value     | Literal      | Any       | YES      | Value       |

##### component_exact

Excludes all rows that do not contain given value with given component (case-sensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| component | Literal      | String    | YES      | Component   |
| value     | Literal      | Any       | YES      | Value       |

##### component_metadata_value

Excludes all rows that do not contain given value with given component in the metadata (case-insensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| component | Literal      | String    | YES      | Component   |
| value     | Literal      | Any       | YES      | Value       |

##### component_metadata_exact

Excludes all rows that do not contain given value with given component in the metadata (case-sensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| component | Literal      | String    | YES      | Component   |
| value     | Literal      | Any       | YES      | Value       |

##### data_type_position_value

Excludes all rows that do not contain given value of given data type at given position (case-insensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| data_type | Literal      | String          | YES      | Data type   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### data_type_position_exact

Excludes all rows that do not contain given value of given data type at given position (case-sensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| data_type | Literal      | String          | YES      | Data type   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### data_type_position_metadata_value

Excludes all rows that do not contain given value of given data type at given position in the metadata (case-insensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| data_type | Literal      | String          | YES      | Data type   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### data_type_position_metadata_exact

Excludes all rows that do not contain given value of given data type at given position in the metadata (case-sensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| data_type | Literal      | String          | YES      | Data type   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### component_data_type_value

Excludes all rows that do not contain given value of given component and data type (case-insensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| component | Literal      | String    | YES      | Component   |
| data_type | Literal      | String    | YES      | Data type   |
| value     | Literal      | Any       | YES      | Value       |

##### component_data_type_exact

Excludes all rows that do not contain given value of given component and data type (case-sensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| component | Literal      | String    | YES      | Component   |
| data_type | Literal      | String    | YES      | Data type   |
| value     | Literal      | Any       | YES      | Value       |

##### component_data_type_metadata_value

Excludes all rows that do not contain given value of given component and data type in the metadata (case-insensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| component | Literal      | String    | YES      | Component   |
| data_type | Literal      | String    | YES      | Data type   |
| value     | Literal      | Any       | YES      | Value       |

##### component_data_type_metadata_exact

Excludes all rows that do not contain given value of given component and data type in the metadata (case-sensitive).

| Argument  | Element type | Data type | Required | Description |
| --------- | ------------ | --------- | -------- | ----------- |
| component | Literal      | String    | YES      | Component   |
| data_type | Literal      | String    | YES      | Data type   |
| value     | Literal      | Any       | YES      | Value       |

##### component_position_value

Excludes all rows that do not contain given value of given component at given position (case-insensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| component | Literal      | String          | YES      | Component   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### component_position_exact

Excludes all rows that do not contain given value of given component at given position (case-sensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| component | Literal      | String          | YES      | Component   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### component_position_metadata_value

Excludes all rows that do not contain given value of given component at given position in the metadata (case-insensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| component | Literal      | String          | YES      | Component   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### component_position_metadata_exact

Excludes all rows that do not contain given value of given component at given position in the metadata (case-sensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| component | Literal      | String          | YES      | Component   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### component_data_type_position_value

Excludes all rows that do not contain given value of given data type and component at given position (case-insensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| component | Literal      | String          | YES      | Component   |
| data_type | Literal      | String          | YES      | Data type   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### component_data_type_position_exact

Excludes all rows that do not contain given value of given data type and component at given position (case-sensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| component | Literal      | String          | YES      | Component   |
| data_type | Literal      | String          | YES      | Data type   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### component_data_type_position_metadata_value

Excludes all rows that do not contain given value of given data type and component at given position in the metadata (case-insensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| component | Literal      | String          | YES      | Component   |
| data_type | Literal      | String          | YES      | Data type   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### component_data_type_position_metadata_exact

Excludes all rows that do not contain given value of given data type and component at given position in the metadata (case-sensitive).

| Argument  | Element type | Data type       | Required | Description |
| --------- | ------------ | --------------- | -------- | ----------- |
| component | Literal      | String          | YES      | Component   |
| data_type | Literal      | String          | YES      | Data type   |
| position  | Literal      | UnsignedInteger | YES      | Position    |
| value     | Literal      | Any             | YES      | Value       |

##### contains

Excludes all rows that do not have a string value that contains given value. Separating search terms by spaces performs a separate lookup for each term. Only values containing all terms are matched. Alias of [contains_all](#contains_all).

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| value    | Literal      | String    | YES      | Value       |

##### contains_all

Excludes all rows that do not have a string value that contains given value. Separating search terms by spaces performs a separate lookup for each term. Only values containing all terms are matched.

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| value    | Literal      | String    | YES      | Value       |

##### contains_any

Excludes all rows that do not have a string value that contains given value. Separating search terms by spaces performs a separate lookup for each term. Values containing at least one term are matched.

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| value    | Literal      | String    | YES      | Value       |

##### related_documents

Related documents performs a text search comparison of given document and documents in the scope of the query and/or function. An optional minimum score which the document must have can be given, as well as a variable-length list of fields to use to compare the document. When they are not given only the default fields are used to compare. Fields that can be used to filter are described in below table.

| Field       | Description                                          |
| ----------- | ---------------------------------------------------- |
| text        | Full text of the document.                           |
| **who**     | **All elements marked as WHO. Default field.**       |
| what        | All elements marked as WHAT.                         |
| **where**   | **All elements marked as WHERE. Default field.**     |
| **when**    | **All elements marked as WHEN. Default field.**      |
| **action**  | **All elements marked as ACTION. Default field.**    |
| person      | People, including fictional.                         |
| norp        | Nationalities or religious or political groups.      |
| fac         | Buildings, airports, highways, bridges, etc.         |
| org         | Companies, agencies, institutions, etc.              |
| gpe         | Countries, cities, states.                           |
| loc         | Non-GPE locations, mountain ranges, bodies of water. |
| product     | Objects, vehicles, foods, etc. (Not services.)       |
| event       | Named hurricanes, battles, wars, sports events, etc. |
| work_of_art | Titles of books, songs, etc.                         |
| law         | Named documents made into laws.                      |
| language    | Any named language.                                  |
| date        | Absolute or relative dates or periods.               |
| time        | Times smaller than a day.                            |
| percent     | Percentage, including "%".                           |
| money       | Monetary values, including unit.                     |
| quantity    | Measurements, as of weight or distance.              |
| ordinal     | "first", "second", etc.                              |
| cardinal    | Numerals that do not fall under another type.        |
| numeric     | Parsed numerics found in the document.               |
| timestamp   | Parsed timestamps found in the document.             |

| Argument      | Element type | Data type | Required | Description         |
| ------------- | ------------ | --------- | -------- | ------------------- |
| document      | Literal      | Document  | YES      | Document LOB ID     |
| minimum_score | Literal      | Float     | NO       | Minimum match score |
| ...field      | Literal      | String    | NO       | Field(s) to compare |

##### action_schema_name

Excludes all rows that do not belong to given action schema. This function is mainly useful in combination with [Dynizer Functions](#dynizer).

| Argument      | Element type | Data type | Required | Description   |
| ------------- | ------------ | --------- | -------- | ------------- |
| action_schema | Literal      | String    | YES      | Action schema |

##### action_name

Excludes all rows that do not belong to given action. This function is mainly useful in combination with [Dynizer Functions](#dynizer).

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| action   | Literal      | String    | YES      | Action      |

##### action_label_name

Excludes all rows that do not belong to given action label. This function is mainly useful in combination with [Dynizer Functions](#dynizer).

| Argument     | Element type | Data type | Required | Description  |
| ------------ | ------------ | --------- | -------- | ------------ |
| action_label | Literal      | String    | YES      | Action label |

#### Dynizer

Dynizer functions can be used to retrieve views on the all schemas/actions/labels and/or modify the base data to query. Dynizer functions can only be used in the **FROM** clause.

##### with_history

Sets the base query data of given action to include history (updated/deleted instances).

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| action   | Action       | N/A       | YES      | Action      |

##### history

Sets the base query data of given action to history only (updated/deleted instances).

| Argument | Element type | Data type | Required | Description |
| -------- | ------------ | --------- | -------- | ----------- |
| action   | Action       | N/A       | YES      | Action      |

##### instance

Returns a view of all values of all instances in all actions. Note that, when not using the function as part of a **JOIN**, filtering using [Query Functions](#query) is permitted, but does not query the view directly. These functions return only instance IDs, which means that a match for one value of an instance will return a row for each value of that instance. To query for one element only, the view's labels can be directly compared using conditions.

The returned table structure is described in below table.

| Action Label       | Data type       | Description       |
| ------------------ | --------------- | ----------------- |
| action_schema_name | String          | Action schema     |
| action_name        | String          | Action            |
| action_label_name  | String          | Action label name |
| instance_id        | String          | Instance ID       |
| value              | Any             | Value             |
| data_type          | String          | Data type         |
| component          | String          | Component         |
| position_index     | UnsignedInteger | Position          |

##### instance_metadata

Returns a view of all values and their metadata values of all instances in all actions. Values with no metadata are not returned. Note that, when not using the function as part of a **JOIN**, filtering using [Query Functions](#query) is permitted, but does not query the table directly. These functions return only instance IDs, which means that a match for one value of an instance will return a row for each value of that instance. To query for one element only, the view's labels can be directly compared using conditions.

The returned table structure is described in below table.

| Action Label       | Data type       | Description                        |
| ------------------ | --------------- | ---------------------------------- |
| action_schema_name | String          | Action schema                      |
| action_name        | String          | Action                             |
| action_label_name  | String          | Action label name                  |
| instance_id        | String          | Instance ID                        |
| value              | Any             | Value                              |
| data_type          | String          | Data type                          |
| component          | String          | Component                          |
| position_index     | UnsignedInteger | Position (0 for instance metadata) |
| metadata_key       | String          | Metadata key                       |
| metadata_value     | Any             | Metadata value                     |
| metadata_data_type | String          | Metadata data type                 |
| metadata_position  | UnsignedInteger | Metadata Position                  |

## Parameters

DQL supports the parametrisation of query values. Values must be referenced inside the DQL query using a '$' and the corresponding parameter index number. Parameter values can then be bound to the query by creating a _portal_. See [Query Flow](#query-flow).

## Query Flow

DQL execution flow mimics the flow used in the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html). However, querying Dynizer is not exclusive to this protocol. Next to the pgwire API, a gRPC and REST API are also available to interact and perform DQL queries. Each request described below has a corresponding gRPC/REST/pgwire API endpoint/handler. For more information refer to the [Dynizer API documentation](https://github.com/Dynactionize/dynizer/blob/master/docs/index.html).

### Simple Query

A simple query is a request that contains one or more DQL query strings to be executed. The request will return all returned rows grouped by the given queries in the order they appeared.

This request matches the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html) Simple Query.

### Parse

A parse request is a request that contains a query string to be parsed and the name of the prepared statement to store the parsed query. Dynizer allows the use of the unnamed statement, which will be used if the name is omitted or simply an empty string. The unnamed statement does not need to be closed explicitly. Keep in mind that, when using APIs such as gRPC/REST, which are asynchronous in nature, the user is responsible of organising correct query execution flow for the unnamed statement within a session. **Using the unnamed statement asynchronously within a single session will result in unpredictable behaviour**. When in doubt, generate a UUID for the statement name and close the statement after execution.

This request matches the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html) Parse.

### Bind

A bind request binds the parsed query to the portal for execution. The request contains a name of the portal to store the bound query and any [Parameters](#parameters) that are referenced in the query. Dynizer allows the use of the unnamed portal, which will be used if the name is omitted or simply an empty string. The unnamed portal does not need to be closed explicitly. Keep in mind that, when using APIs such as gRPC/REST that are asynchronous in nature, the user is responsible of organising correct query execution flow for the unnamed portal within a session. **Using the unnamed portal asynchronously within a single session will result in unpredictable behaviour**. When in doubt, generate a UUID for the portal name (or re-use the statement name) and close the portal after execution.

This request matches the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html) Bind.

### Describe

A describe request requests the description of the prepared statement or portal. The request contains the name of the statement/portal (or omitted/empty for unnamed). In case of a describe statement, Dynizer will respond information about the parameters that must be given to the query _Bind_ and the result table labels. For the portal variant, Dynizer will return the labels only.

In gRPC/REST, these are two separate RPCs/endpoints.

This request matches the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html) Describe.

### Execute

An execute request executes the bound portal. The request contains the name of the portal (or omitted/empty for unnamed) and the number of rows to fetch. Dynizer will return the given number of rows (or less if there are no more). A _PortalSuspended_ message is sent if there are still more rows to be executed and a _CommandComplete_ message if all rows have been read.

The execute request is slightly different in gRPC/REST. In pgwire, it is not possible to re-read rows of a query and they must all be read to complete the query (unless it is closed). In gRPC/REST, it is possible to set the 'is_relative' parameter to false and provide a limit and offset to retrieve a specific window of the query result instead of a limit only. In this case it possible to read the same rows again, or skip rows, unless the portal is closed.

This request matches the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html) Execute.

### Sync

A sync request should be sent after completion of a cycle. If the cycle is in an error state, sync provides a resynchronization point for error recovery. Dynizer will respond with a _ReadyForQuery_ message.

This request matches the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html) Sync.

### Close

A close request closes the prepared statement or portal. The request contains the name of the statement/portal (or omitted/empty for unnamed). The unnamed statement or portal does not require closing, however it can be closed explicitly just as any other named statement/portal.

In gRPC/REST, these are two separate RPCs/endpoints.

This request matches the [PostgreSQL Wire Protocol (pgwire)](https://www.postgresql.org/docs/current/protocol.html) Close.

## Catalog tables

Dynizer provides support for querying the _information_schema_ as well as the _pg_catalog_ schema the same way as they are available in [PostgreSQL](https://www.postgresql.org/). These tables can provide drivers with the necessary information to retrieve data and list the schema definitions. If a table is not relevant to Dynizer, it will never return rows if they are queried. However, all tables are available to be queried for compatibility reasons.

### Information Schema

In relational databases, the information schema (information_schema) is an ANSI-standard set of read-only views that provide information about all of the tables, views, columns, and procedures in a database. The full schema is provided by Dynizer and its tables are listed below.

| Name                                  | Returns Data | Description                                                                                                                                                                                |
| ------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| administrable_role_authorizations     | no           | The view administrable_role_authorizations identifies all roles that the current user has the admin option for.                                                                            |
| applicable_roles                      | no           | The view applicable_roles identifies all roles whose privileges the current user can use.                                                                                                  |
| attributes                            | no           | The view attributes contains information about the attributes of composite data types defined in the database.                                                                             |
| character_sets                        | yes          | The view character_sets identifies the character sets available in the current database. The only character set available is 'UTF8'                                                        |
| check_constraint_routine_usage        | no           | The view check_constraint_routine_usage identifies routines (functions and procedures) that are used by a check constraint.                                                                |
| check_constraints                     | no           | The view check_constraints contains all check constraints, either defined on a table or on a domain, that are owned by a currently enabled role.                                           |
| collation_character_set_applicability | no           | The view collation_character_set_applicability identifies which character set the available collations are applicable to.                                                                  |
| collations                            | no           | The view collations contains the collations available in the current database.                                                                                                             |
| column_column_usage                   | no           | The view column_column_usage identifies all generated columns that depend on another base column in the same table.                                                                        |
| column_domain_usage                   | no           | The view column_domain_usage identifies all columns (of a table or a view) that make use of some domain defined in the current database and owned by a currently enabled role.             |
| column_options                        | no           | The view column_options contains all the options defined for foreign table columns in the current database.                                                                                |
| column_privileges                     | yes          | The view column_privileges identifies all privileges granted on columns to a currently enabled role or by a currently enabled role.                                                        |
| column_udt_usage                      | yes          | The view column_udt_usage identifies all columns that use data types owned by a currently enabled role.                                                                                    |
| columns                               | yes          | The view columns contains information about all table columns (or view columns) in the database.                                                                                           |
| constraint_column_usage               | no           | The view constraint_column_usage identifies all columns in the current database that are used by some constraint.                                                                          |
| constraint_table_usage                | no           | The view constraint_table_usage identifies all tables in the current database that are used by some constraint and are owned by a currently enabled role.                                  |
| data_type_privileges                  | yes          | The view data_type_privileges identifies all data type descriptors that the current user has access to, by way of being the owner of the described object or having some privilege for it. |
| domain_constraints                    | no           | The view domain_constraints contains all constraints belonging to domains defined in the current database.                                                                                 |
| domain_udt_usage                      | no           | The view domain_udt_usage identifies all domains that are based on data types owned by a currently enabled role.                                                                           |
| domains                               | no           | The view domains contains all domains defined in the current database.                                                                                                                     |
| element_types                         | yes          | The view element_types contains the data type descriptors of the elements of arrays.                                                                                                       |
| enabled_roles                         | yes          | The view enabled_roles identifies the currently “enabled roles”. Returns the user who authorized the session.                                                                              |
| foreign_data_wrapper_options          | no           | The view foreign_data_wrapper_options contains all the options defined for foreign-data wrappers in the current database.                                                                  |
| foreign_data_wrappers                 | no           | The view foreign_data_wrappers contains all foreign-data wrappers defined in the current database.                                                                                         |
| foreign_server_options                | no           | The view foreign_server_options contains all the options defined for foreign servers in the current database                                                                               |
| foreign_servers                       | no           | The view foreign_servers contains all foreign servers defined in the current database.                                                                                                     |
| foreign_table_options                 | no           | The view foreign_table_options contains all the options defined for foreign tables in the current database.                                                                                |
| foreign_tables                        | no           | The view foreign_tables contains all foreign tables defined in the current database.                                                                                                       |
| information_schema_catalog_name       | yes          | information_schema_catalog_name is a table that always contains one row and one column containing the name of the current database (current catalog, in SQL terminology). Always 'dynizer' |
| key_column_usage                      | no           | The view key_column_usage identifies all columns in the current database that are restricted by some unique, primary key, or foreign key constraint.                                       |
| parameters                            | no           | The view parameters contains information about the parameters (arguments) of all functions in the current database.                                                                        |
| referential_constraints               | no           | The view referential_constraints contains all referential (foreign key) constraints in the current database.                                                                               |
| role_column_grants                    | yes          | The view role_column_grants identifies all privileges granted on columns where the grantor or grantee is a currently enabled role.                                                         |
| role_routine_grants                   | no           | The view role_routine_grants identifies all privileges granted on functions where the grantor or grantee is a currently enabled role.                                                      |
| role_table_grants                     | yes          | The view role_table_grants identifies all privileges granted on tables or views where the grantor or grantee is a currently enabled role.                                                  |
| role_udt_grants                       | no           | The view role_udt_grants is intended to identify USAGE privileges granted on user-defined types where the grantor or grantee is a currently enabled role.                                  |
| role_usage_grants                     | no           | The view role_usage_grants identifies USAGE privileges granted on various kinds of objects where the grantor or grantee is a currently enabled role.                                       |
| routine_privileges                    | no           | The view routine_column_usage is meant to identify all columns that are used by a function or procedure.                                                                                   |
| routines                              | no           | The view routine_privileges identifies all privileges granted on functions to a currently enabled role or by a currently enabled role.                                                     |
| schemata                              | yes          | The view schemata contains all schemas in the current database that the current user has access to (by way of being the owner or having some privilege).                                   |
| sequences                             | no           | The view sequences contains all sequences defined in the current database.                                                                                                                 |
| sql_features                          | no           | The table sql_features contains information about which formal features defined in the SQL standard are supported.                                                                         |
| sql_implementation_info               | yes          | The table sql_implementation_info contains information about various aspects that are left implementation-defined by the SQL standard.                                                     |
| sql_parts                             | yes          | The table sql_parts contains information about which of the several parts of the SQL standard are supported by [PostgreSQL](https://www.postgresql.org/).                                  |
| sql_sizing                            | yes          | The table sql_sizing contains information about various size limits and maximum values in [PostgreSQL](https://www.postgresql.org/).                                                       |
| table_constraints                     | no           | The view table_constraints contains all constraints belonging to tables that the current user owns or has some privilege other than SELECT on.                                             |
| table_privileges                      | yes          | The view table_privileges identifies all privileges granted on tables or views to a currently enabled role or by a currently enabled role.                                                 |
| tables                                | yes          | The view tables contains all tables and views defined in the current database.                                                                                                             |
| transforms                            | no           | The view transforms contains information about the transforms defined in the current database.                                                                                             |
| triggered_update_columns              | no           | For triggers in the current database that specify a column list (like UPDATE OF column1, column2), the view triggered_update_columns identifies these columns.                             |
| triggers                              | no           | The view triggers contains all triggers defined in the current database on tables and views that the current user owns or has some privilege other than SELECT on.                         |
| udt_privileges                        | no           | The view udt_privileges identifies USAGE privileges granted on user-defined types to a currently enabled role or by a currently enabled role.                                              |
| usage_privileges                      | no           | The view usage_privileges identifies USAGE privileges granted on various kinds of objects to a currently enabled role or by a currently enabled role.                                      |
| user_defined_types                    | no           | The view user_defined_types currently contains all composite types defined in the current database.                                                                                        |
| user_mapping_options                  | no           | The view user_mapping_options contains all the options defined for user mappings in the current database.                                                                                  |
| user_mappings                         | no           | The view user_mappings contains all user mappings defined in the current database.                                                                                                         |
| view_column_usage                     | no           | The view view_column_usage identifies all columns that are used in the query expression of a view.                                                                                         |
| view_routine_usage                    | no           | The view view_routine_usage identifies all routines (functions and procedures) that are used in the query expression of a view.                                                            |
| view_table_usage                      | no           | The view view_table_usage identifies all tables that are used in the query expression of a view.                                                                                           |
| views                                 | no           | The view views contains all views defined in the current database.                                                                                                                         |

### PG Catalog

The PG catalogs are the place where [PostgreSQL](https://www.postgresql.org/) stores schema metadata, such as information about tables and columns, and internal bookkeeping information. The full schema is provided by Dynizer and its tables are listed below.

| Name                            | Returns Data | Description                                                                                                                                                                                          |
| ------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pg_aggregate                    | no           | The catalog pg_aggregate stores information about aggregate functions.                                                                                                                               |
| pg_am                           | no           | The catalog pg_am stores information about relation access methods.                                                                                                                                  |
| pg_amop                         | no           | The catalog pg_amop stores information about operators associated with access method operator families.                                                                                              |
| pg_amproc                       | no           | The catalog pg_amproc stores information about support functions associated with access method operator families.                                                                                    |
| pg_attrdef                      | no           | The catalog pg_attrdef stores column default values.                                                                                                                                                 |
| pg_attribute                    | yes          | The catalog pg_attribute stores information about table columns. There will be exactly one pg_attribute row for every column in every table in the database.                                         |
| pg_auth_members                 | no           | The catalog pg_auth_members shows the membership relations between roles.                                                                                                                            |
| pg_authid                       | no           | The catalog pg_authid contains information about database authorization identifiers (roles).                                                                                                         |
| pg_available_extension_versions | no           | The pg_available_extension_versions view lists the specific extension versions that are available for installation                                                                                   |
| pg_available_extensions         | no           | The pg_available_extensions view lists the extensions that are available for installation.                                                                                                           |
| pg_cast                         | no           | The catalog pg_cast stores data type conversion paths, both built-in and user-defined.                                                                                                               |
| pg_class                        | yes          | The catalog pg_class catalogs tables and most everything else that has columns or is otherwise similar to a table.                                                                                   |
| pg_collation                    | no           | The catalog pg_collation describes the available collations, which are essentially mappings from an SQL name to operating system locale categories.                                                  |
| pg_config                       | no           | The view pg_config describes the compile-time configuration parameters of the currently installed version of [PostgreSQL](https://www.postgresql.org/).                                              |
| pg_constraint                   | no           | The catalog pg_constraint stores check, primary key, unique, foreign key, and exclusion constraints on tables.                                                                                       |
| pg_conversion                   | yes          | The catalog pg_conversion describes encoding conversion functions.                                                                                                                                   |
| pg_cursors                      | no           | The pg_cursors view lists the cursors that are currently available.                                                                                                                                  |
| pg_database                     | yes          | The catalog pg_database stores information about the available databases. Always database 'dynizer'                                                                                                  |
| pg_db_role_setting              | no           | The catalog pg_db_role_setting records the default values that have been set for run-time configuration variables, for each role and database combination.                                           |
| pg_default_acl                  | no           | The catalog pg_default_acl stores initial privileges to be assigned to newly created objects.                                                                                                        |
| pg_depend                       | no           | The catalog pg_depend records the dependency relationships between database objects.                                                                                                                 |
| pg_description                  | no           | The catalog pg_description stores optional descriptions (comments) for each database object.                                                                                                         |
| pg_enum                         | no           | The pg_enum catalog contains entries showing the values and labels for each enum type.                                                                                                               |
| pg_event_trigger                | no           | The catalog pg_event_trigger stores event triggers.                                                                                                                                                  |
| pg_extension                    | no           | The catalog pg_extension stores information about the installed extensions.                                                                                                                          |
| pg_file_settings                | no           | The view pg_file_settings provides a summary of the contents of the server's configuration file(s).                                                                                                  |
| pg_foreign_data_wrapper         | no           | The catalog pg_foreign_data_wrapper stores foreign-data wrapper definitions.                                                                                                                         |
| pg_foreign_server               | no           | The catalog pg_foreign_server stores foreign server definitions.                                                                                                                                     |
| pg_foreign_table                | no           | The catalog pg_foreign_table contains auxiliary information about foreign tables.                                                                                                                    |
| pg_group                        | no           | The view pg_group exists for backwards compatibility: it emulates a catalog that existed in [PostgreSQL](https://www.postgresql.org/) before version 8.1.                                            |
| pg_hba_file_rules               | no           | The view pg_hba_file_rules provides a summary of the contents of the client authentication configuration file, pg_hba.conf.                                                                          |
| pg_index                        | no           | The catalog pg_index contains part of the information about indexes.                                                                                                                                 |
| pg_indexes                      | no           | The view pg_indexes provides access to useful information about each index in the database.                                                                                                          |
| pg_inherits                     | no           | The catalog pg_inherits records information about table and index inheritance hierarchies.                                                                                                           |
| pg_init_privs                   | no           | The catalog pg_init_privs records information about the initial privileges of objects in the system.                                                                                                 |
| pg_language                     | no           | The catalog pg_language registers languages in which you can write functions or stored procedures.                                                                                                   |
| pg_largeobject                  | no           | The catalog pg_largeobject holds the data making up “large objects”.                                                                                                                                 |
| pg_largeobject_metadata         | no           | The catalog pg_largeobject_metadata holds metadata associated with large objects.                                                                                                                    |
| pg_locks                        | no           | The view pg_locks provides access to information about the locks held by active processes within the database server.                                                                                |
| pg_matviews                     | no           | The view pg_matviews provides access to useful information about each materialized view in the database.                                                                                             |
| pg_namespace                    | yes          | The catalog pg_namespace stores namespaces. A namespace is the structure underlying SQL schemas: each namespace can have a separate collection of relations, types, etc. without name conflicts.     |
| pg_opclass                      | no           | The catalog pg_opclass defines index access method operator classes.                                                                                                                                 |
| pg_operator                     | no           | The catalog pg_operator stores information about operators.                                                                                                                                          |
| pg_opfamily                     | no           | The catalog pg_opfamily defines operator families.                                                                                                                                                   |
| pg_partitioned_table            | no           | The catalog pg_partitioned_table stores information about how tables are partitioned.                                                                                                                |
| pg_policies                     | no           | The view pg_policies provides access to useful information about each row-level security policy in the database.                                                                                     |
| pg_policy                       | no           | The catalog pg_policy stores row-level security policies for tables.                                                                                                                                 |
| pg_prepared_statements          | no           | The pg_prepared_statements view displays all the prepared statements that are available in the current session.                                                                                      |
| pg_prepared_xacts               | no           | The view pg_prepared_xacts displays information about transactions that are currently prepared for two-phase commit.                                                                                 |
| pg_proc                         | yes          | The catalog pg_proc stores information about functions, procedures, aggregate functions, and window functions (collectively also known as routines).                                                 |
| pg_publication                  | no           | The catalog pg_publication contains all publications created in the database.                                                                                                                        |
| pg_publication_rel              | no           | The catalog pg_publication_rel contains the mapping between relations and publications in the database.                                                                                              |
| pg_publication_tables           | no           | The view pg_publication_tables provides information about the mapping between publications and information of tables they contain.                                                                   |
| pg_range                        | no           | The catalog pg_range stores information about range types.                                                                                                                                           |
| pg_replication_origin           | no           | The pg_replication_origin catalog contains all replication origins created.                                                                                                                          |
| pg_replication_origin_status    | no           | The pg_replication_origin_status view contains information about how far replay for a certain origin has progressed.                                                                                 |
| pg_replication_slots            | no           | The pg_replication_slots view provides a listing of all replication slots that currently exist on the database cluster, along with their current state.                                              |
| pg_rewrite                      | no           | The catalog pg_rewrite stores rewrite rules for tables and views.                                                                                                                                    |
| pg_roles                        | yes          | The view pg_roles provides access to information about database roles.                                                                                                                               |
| pg_rules                        | no           | The view pg_rules provides access to useful information about query rewrite rules.                                                                                                                   |
| pg_seclabel                     | no           | The catalog pg_seclabel stores security labels on database objects.                                                                                                                                  |
| pg_seclabels                    | no           | The view pg_seclabels provides information about security labels.                                                                                                                                    |
| pg_sequence                     | no           | The catalog pg_sequence contains information about sequences.                                                                                                                                        |
| pg_sequences                    | no           | The view pg_sequences provides access to useful information about each sequence in the database.                                                                                                     |
| pg_settings                     | yes          | The view pg_settings provides access to run-time parameters of the server. It is essentially an alternative interface to the SHOW and SET commands.                                                  |
| pg_shadow                       | no           | The view pg_shadow exists for backwards compatibility: it emulates a catalog that existed in [PostgreSQL](https://www.postgresql.org/) before version 8.1.                                           |
| pg_shdepend                     | no           | The catalog pg_shdepend records the dependency relationships between database objects and shared objects, such as roles.                                                                             |
| pg_shdescription                | no           | The catalog pg_shdescription stores optional descriptions (comments) for shared database objects.                                                                                                    |
| pg_shmem_allocations            | no           | The pg_shmem_allocations view shows allocations made from the server's main shared memory segment.                                                                                                   |
| pg_shseclabel                   | no           | The catalog pg_shseclabel stores security labels on shared database objects.                                                                                                                         |
| pg_statistic                    | no           | The catalog pg_statistic stores statistical data about the contents of the database.                                                                                                                 |
| pg_statistic_ext                | no           | The catalog pg_statistic_ext holds definitions of extended planner statistics.                                                                                                                       |
| pg_statistic_ext_data           | no           | The catalog pg_statistic_ext_data holds data for extended planner statistics defined in pg_statistic_ext.                                                                                            |
| pg_stats                        | no           | The view pg_stats provides access to the information stored in the pg_statistic catalog.                                                                                                             |
| pg_stats_ext                    | no           | The view pg_stats_ext provides access to information about each extended statistics object in the database, combining information stored in the pg_statistic_ext and pg_statistic_ext_data catalogs. |
| pg_subscription                 | no           | The catalog pg_subscription contains all existing logical replication subscriptions.                                                                                                                 |
| pg_subscription_rel             | no           | The catalog pg_subscription_rel contains the state for each replicated relation in each subscription.                                                                                                |
| pg_tables                       | yes          | The view pg_tables provides access to useful information about each table in the database.                                                                                                           |
| pg_tablespace                   | yes          | The catalog pg_tablespace stores information about the available tablespaces.                                                                                                                        |
| pg_timezone_abbrevs             | no           | The view pg_timezone_abbrevs provides a list of time zone abbreviations that are currently recognized by the datetime input routines.                                                                |
| pg_timezone_names               | no           | The view pg_timezone_names provides a list of time zone names that are recognized by SET TIMEZONE, along with their associated abbreviations, UTC offsets, and daylight-savings status.              |
| pg_transform                    | no           | The catalog pg_transform stores information about transforms, which are a mechanism to adapt data types to procedural languages.                                                                     |
| pg_trigger                      | no           | The catalog pg_trigger stores triggers on tables and views.                                                                                                                                          |
| pg_ts_config                    | no           | The pg_ts_config catalog contains entries representing text search configurations.                                                                                                                   |
| pg_ts_config_map                | no           | The pg_ts_config_map catalog contains entries showing which text search dictionaries should be consulted, and in what order, for each output token type of each text search configuration's parser.  |
| pg_ts_dict                      | no           | The pg_ts_dict catalog contains entries defining text search dictionaries.                                                                                                                           |
| pg_ts_parser                    | no           | The pg_ts_parser catalog contains entries defining text search parsers.                                                                                                                              |
| pg_ts_template                  | no           | The pg_ts_template catalog contains entries defining text search templates.                                                                                                                          |
| pg_type                         | yes          | The catalog pg_type stores information about data types.                                                                                                                                             |
| pg_user                         | no           | The view pg_user provides access to information about database users.                                                                                                                                |
| pg_user_mapping                 | no           | The catalog pg_user_mapping stores the mappings from local user to remote.                                                                                                                           |
| pg_user_mappings                | no           | The view pg_user_mappings provides access to information about user mappings.                                                                                                                        |
| pg_views                        | no           | The view pg_views provides access to useful information about each view in the database.                                                                                                             |

## Unsupported

TODO: List of unsupported SQL functionality

### Planned

TODO: Contains list of planned features and estimate

### Unplanned

TODO: Contains list of unplanned features

## Example Case

### Setting Session Parameters

The following query sets the system variable 'array_style' to 'csv':

```text
SET array_style = 'csv'
```

It is also possible to set multiple values for one key. The following query adds the csv separator ';' to the value:

```text
SET array_style = 'csv', ';'
```

### Showing Session Parameters

The following query returns the values(s) of system variable 'array_style':

```text
SHOW array_style
```

It will output the following table:

| array_style |
| ----------- |
| csv, ;      |

### Creating a Schema

The schema created in this example case will have the name 'example'. The following query creates the schema:

```text
CREATE SCHEMA example
```

It's possible to add the **IF NOT EXISTS** keyword to not return an error if the schema is already present:

```text
CREATE SCHEMA IF NOT EXISTS example
```

### Setting Search Path

The search path is a system variable that defines the schemas that will be searched when refering to an action. When the search path has been correctly setup, it is no longer necessary to qualify an action. The search path can be set to our newly created 'example' schema as follows:

```text
SET search_path = 'example'
```

### Creating an Action

Now that the schema has been defined, an action can be created in it. The first action will have the name 'person' with labels 'id', 'name'. The label 'id' will have default data type defined as 'UnsignedInteger' and 'name' will have 'String'. Storage parameters are used to make sure the 'id' label is of the correct data type, as an unsigned integer is not present in [PostgreSQL](https://www.postgresql.org/). Storage parameters are also used to define the component types. Component type 'What' is assigned to the 'id' label while 'name' will be assigned 'Who'.

The following query creates the action:

```text
CREATE TABLE person (id int8, name text) WITH (default_data_types='UnsignedInteger,String',component_types='What,Who')
```

If the search_path is not set to our 'example' schema, it is possible to still create it in this schema using a qualifier:

```text
CREATE TABLE example.person (id int8, name text) WITH (default_data_types='UnsignedInteger,String',component_types='What,Who')
```

It's possible to add the **IF NOT EXISTS** keyword to not return an error if the action is already present:

```text
CREATE TABLE IF NOT EXISTS person (id int8, name text) WITH (default_data_types='UnsignedInteger,String',component_types='What,Who')
```

### Deleting an Action

To delete the newly created action 'person', the following query can be used:

```text
DROP TABLE person
```

Should the action contain any data, the above query will fail and the **CASCADE** keyword needs to be given to be able to delete the action:

```text
DROP TABLE person CASCADE
```

The **IF EXISTS** keyword can be added to not return an error if the action does not exist.

```text
DROP TABLE IF EXISTS person CASCADE
```

### Inserting Data

To insert data into an action, an **INSERT INTO** query is used. Two instances will be created within the 'person' action in this example. The following query inserts the instances:

```text
INSERT INTO person VALUES (1, 'John Doe'), (2, 'Jane Doe')
```

Columns to insert into can be given in the query after the action name:

```text
INSERT INTO person (id, name) VALUES (1, 'John Doe'), (2, 'Jane Doe')
```

Values can also be omitted by explicitly defining the columns:

```text
INSERT INTO person (id) VALUES (3)
```

Multiple values can be inserted for a single label by providing the label _n_ times:

```text
INSERT INTO person (id, name, name) VALUES (1, 'John', 'Doe')
```

### Updating Data

The **UPDATE** query is used to update one or more instances of an action. If the data from the previous example is taken, there is still one row with 'id' as '3' that did not have a name. The following query will set the name of that instance to 'Jack Smith':

```text
UPDATE person SET name = 'Jack Smith' WHERE id = 3;
```

It is possible to omit the **WHERE** clause. The following query will set the names of all instances to 'UNKNOWN'

```text
UPDATE person SET name = 'UNKNOWN';
```

### Deleting Data

The **DELETE** query is used to delete instances from an action. In this example the instance with the 'id' as '3' is deleted:

```text
DELETE FROM person WHERE id = 3;
```

It is possible to omit the **WHERE** clause. The following query will delete all instances from the 'person' action.

```text
DELETE FROM person;
```
