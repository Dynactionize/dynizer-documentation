# Pipeline-API Plugin Reference

Plugins are post-processing steps that run after a flow has analyzed a
document. Each plugin takes the analyzer output, transforms or filters
it, and stores the result in the Dynizer under a configurable action /
action label.

You enable plugins via the `plugins` array inside a pipeline
configuration's `flow_configuration.config` (or — depending on flow —
inside the pipeline configuration itself). Each entry has a `name`
(matching the plugin's registered identifier) and an optional `config`
object that follows the plugin's JSON Schema.

> **Tip — live discovery.** Authenticated clients can always fetch the
> live schemas (including defaults and enums) from the deployment
> itself:
>
> - `GET /plugins` — list all plugins with their JSON Schema.
> - `GET /plugins/{name}` — schema for a single plugin.
> - `GET /flows` / `GET /flows/{name}` — same for flows.
>
> Any field omitted from a `config` falls back to the `default` listed
> in that schema.

## Available plugins

| Name | Purpose |
|---|---|
| [`raw`](#raw) | Store the complete raw JSON analyzer result. |
| [`text`](#text) | Store the extracted document text (and optional summary). |
| [`sentences`](#sentences) | Store the analyzer's sentence-level output. |
| [`segments`](#segments) | Store segments grouped by component type. |
| [`segments_wide`](#segments_wide) | Wide-format segments, with extra entity-type filtering. |
| [`tokens`](#tokens) | Store the analyzer's token-level output. |
| [`pseudonymize`](#pseudonymize) | Pseudonymize selected component / entity types; store both the full and an anonymized version. |
| [`deka (Dashboard Entities, Keysegments and Actions)`](#deka) | Dashboard-oriented storage: entities, verbs, keysegments and their links. |
| [`script`](#script) | Run a user-supplied Starlark (Python-syntax) script on the analyzer output in a sandbox; the script returns instance elements that the plugin writes. |

---

## raw

**Purpose.** Raw data plugin. This configuration defines where and how to
store the raw JSON resulting from pipeline analysis.

**Registered name:** `raw`

| Field | Type | Default | Description |
|---|---|---|---|
| `action` | string | `"document_raw"` | The action to store the result raw JSON in. |
| `action_label` | string | `"document"` | The action label to store the result raw JSON in. |
| `data_type` | string (enum: `DT_Clob`, `DT_Blob`, `DT_Document`) | `"DT_Document"` | The data type to store the result raw JSON in. |
| `create_action` | boolean | `true` | Create the action if it does not exist. |
| `text_action_label` | string | `""` | The action label to store the result text in. Leave empty to omit the text. |
| `text_data_type` | string (enum: `DT_Text`, `DT_Blob`, `DT_Clob`) | `"DT_Text"` | The data type to store the result text in. |
| `summary_action_label` | string | `""` | The action label to store the result summary in. Leave empty to omit the summary. |
| `summary_data_type` | string (enum: `DT_Text`, `DT_Blob`, `DT_Clob`) | `"DT_Text"` | The data type to store the result summary in. |
| `language_action_label` | string | `""` | The action label to store the document language in. Leave empty to omit the language. |
| `add_document_meta` | boolean | `false` | Add detected metadata of the document (if applicable). |
| `unique_labels` | array<string> | `[]` | If non-empty, the plugin skips inserting a record when the combination of values for these labels already exists. |
| `add_pipeline_id` | boolean | `true` | Add the pipeline ID to the result instance. |

**Example**

```json
{
  "name": "raw",
  "config": {
    "action": "document_raw",
    "action_label": "document",
    "data_type": "DT_Document"
  }
}
```

---

## text

**Purpose.** Stores the extracted document text and, optionally, a
summary.

**Registered name:** `text`

| Field | Type | Default | Description |
|---|---|---|---|
| `action` | string | `"document_text"` | The action to store the result text in. |
| `text_actionlabel` | string | `""` | The action label to store the result text in. Leave empty to not store the text. |
| `summary_actionlabel` | string | `""` | The action label to store the result summary text in. Leave empty to not store the summary text. |
| `summmary_percentage` | integer | `25` | The percentage to keep in the summary text. |

**Example**

```json
{
  "name": "text",
  "config": {
    "action": "document_text",
    "text_actionlabel": "text"
  }
}
```

---

## sentences

**Purpose.** Stores the analyzer's sentence-level breakdown.

**Registered name:** `sentences`

| Field | Type | Default | Description |
|---|---|---|---|
| `action` | string | `"document_sentence"` | The action to store the result sentences in. |
| `actionlabel` | string | `""` | The action label for sentence text. Leave empty to not store the text. |
| `fields` | array<string> | `[]` | Fields to keep from each sentence. Leave empty for all fields. |

**Example**

```json
{
  "name": "sentences",
  "config": {
    "action": "document_sentence",
    "actionlabel": "sentence"
  }
}
```

---

## segments

**Purpose.** Stores segments grouped by component type. The
`actionlabel` is appended with the component type of each segment.

**Registered name:** `segments`

| Field | Type | Default | Description |
|---|---|---|---|
| `action` | string | `"document_segment"` | The action to store the result segments in. |
| `actionlabel` | string | `""` | Base label; the component type is appended. Leave empty to not store the text. |
| `fields` | array<string> | `[]` | Fields to keep from each segment. Leave empty for all fields. |
| `components` | array<string> | `[]` | Components to keep. Leave empty for all components. |

**Example**

```json
{
  "name": "segments",
  "config": {
    "action": "document_segment",
    "actionlabel": "segment_",
    "components": ["WHO", "WHERE"]
  }
}
```

---

## segments_wide

**Purpose.** Wide-format segments with the result document JSON, text,
summary and optional entity-type filtering all stored in a single
action.

**Registered name:** `segments_wide`

| Field | Type | Default | Description |
|---|---|---|---|
| `action` | string | `"document_segment"` | The action to store the result segments in. |
| `actionlabel` | string | `""` | Suffix of the action label for segment text; appended to the entity type of the segment. |
| `create_action` | boolean | `true` | Create the action if it does not exist. |
| `document_action_label` | string | `""` | The action label to store the result document JSON in. Leave empty to omit. |
| `document_data_type` | string (enum: `DT_Clob`, `DT_Blob`, `DT_Document`) | `"DT_Document"` | Data type for the document JSON. |
| `text_action_label` | string | `""` | The action label to store the result text in. Leave empty to omit. |
| `text_data_type` | string (enum: `DT_Text`, `DT_Blob`, `DT_Clob`) | `"DT_Text"` | Data type for the text. |
| `summary_action_label` | string | `""` | The action label to store the result summary in. Leave empty to omit. |
| `summary_data_type` | string (enum: `DT_Text`, `DT_Blob`, `DT_Clob`) | `"DT_Text"` | Data type for the summary. |
| `entity_types` | array<string> (unique, from list below) | `[]` | Entity types to keep. Leave empty for all types. |

Supported `entity_types`: `PERSON`, `NORP`, `FAC`, `ORG`, `GPE`, `LOC`,
`PRODUCT`, `EVENT`, `WORK_OF_ART`, `LAW`, `LANGUAGE`, `DATE`, `TIME`,
`PERCENT`, `MONEY`, `QUANTITY`, `ORDINAL`, `CARDINAL`.

**Example**

```json
{
  "name": "segments_wide",
  "config": {
    "action": "document_segment_wide",
    "document_action_label": "document",
    "text_action_label": "text",
    "entity_types": ["PERSON", "ORG", "DATE"]
  }
}
```

---

## tokens

**Purpose.** Stores the analyzer's token-level output. The
`actionlabel` is appended with the component of each token.

**Registered name:** `tokens`

| Field | Type | Default | Description |
|---|---|---|---|
| `action` | string | `"document_token"` | The action to store the result tokens in. |
| `actionlabel` | string | `""` | Base label; the token component is appended. Leave empty to not store the text. |
| `fields` | array<string> | `[]` | Fields to keep from each token. Leave empty for all fields. |

**Example**

```json
{
  "name": "tokens",
  "config": {
    "action": "document_token",
    "actionlabel": "token_"
  }
}
```

---

## pseudonymize

**Purpose.** Pseudonymize Raw plugin. Defines how a document is
pseudonymized — which component types and entity types are replaced.
The full and anonymized results are stored as JSON CLOBs under separate
actions. The full result contains the original *and* pseudonymized
text/values plus their positions; the anonymized result hides the
original values.

**Registered name:** `pseudonymize`

| Field | Type | Default | Description |
|---|---|---|---|
| `action` | string | `"document_pseudonymize"` | Action that stores the **complete** result (originals visible). |
| `action_anonymized` | string | `"document_pseudonymize_anonymized"` | Action that stores the **anonymized** result (originals hidden). |
| `actionlabel` | string | `"pseudonymization"` | Action label used for the JSON CLOB. |
| `create_actions` | boolean | `true` | Create the actions if they do not exist. |
| `component_types` | array<string> (unique) | `["WHO", "WHERE", "WHEN"]` | Component types to pseudonymize. Empty / omitted → none. Allowed: `WHO`, `WHAT`, `WHERE`, `WHEN`. |
| `entity_types` | array<string> (unique) | `["DATE","ORG","PERSON","LOC","FAC","GPE","NORP"]` | Entity types to pseudonymize. Empty / omitted → none. Allowed: `DATE`, `ORG`, `PERSON`, `LOC`, `FAC`, `GPE`, `NORP`, `CARDINAL`, `EVENT`, `LANGUAGE`, `LAW`, `MONEY`, `ORDINAL`, `PERCENT`, `PRODUCT`, `QUANTITY`, `TIME`, `WORK_OF_ART`. |

**Example**

```json
{
  "name": "pseudonymize",
  "config": {
    "component_types": ["WHO", "WHERE"],
    "entity_types": ["PERSON", "ORG"]
  }
}
```

---

## deka

**Purpose.** Plugin for dashboards containing entities, keysegments and
actions (DEKA = **D**ashboard **E**ntities, **K**eysegments and
**A**ctions). Stores the resulting entities, verbs, keysegments and the
links between them in dedicated actions.

**Registered name:** `deka (Dashboard Entities, Keysegments and Actions)`
*(yes — that is the full, exact identifier including the parenthetical.)*

| Field | Type | Default | Description |
|---|---|---|---|
| `create_actions` | boolean | `true` | Create the actions if they do not exist. |
| `action_entities` | string | `"deka_entity"` | Action that stores the resulting entities. |
| `action_actions` | string | `"deka_action"` | Action that stores the resulting actions (verbs). |
| `action_keysegments` | string | `"deka_keysegment"` | Action that stores the resulting keysegments. |
| `action_action_entity_link` | string | `"deka_action_entity"` | Action that stores the resulting action-entity links. |

**Example**

```json
{
  "name": "deka (Dashboard Entities, Keysegments and Actions)",
  "config": {
    "action_entities": "deka_entity",
    "action_actions": "deka_action",
    "action_keysegments": "deka_keysegment",
    "action_action_entity_link": "deka_action_entity"
  }
}
```

---

## script

**Purpose.** Run a user-supplied **Starlark** script (Python-like syntax) against the analyzer output. The script returns a list of instance elements that the plugin writes to Dynizer — the same end result as any other plugin, just driven by user code.

The script runs in a sandbox: **no network, no filesystem, no `import`, no `load()`**, bounded by an execution-step limit and a wall-clock timeout. Starlark is Python-syntax but is not full Python — there are no third-party libraries, no `re`/`datetime` modules, no I/O. If you need those, this is not the right tool.

**Registered name:** `script`

| Field | Type | Default | Description |
|---|---|---|---|
| `script` | string (**required**) | — | Starlark source code. Must define a top-level function `def execute(data, config)` that returns a list of instance elements. |
| `action` | string | `"document_script"` | Action under which the script's output instance is created. |
| `create_action` | boolean | `true` | Create the action and its labels if missing. The label schema is taken from the pipeline-level `instance` block — see "Declaring the schema" below. |
| `user_config` | object | `{}` | Arbitrary JSON object passed to the script as its `config` argument — use this for script parameters you want to tweak without editing the script. |
| `add_pipeline_id` | boolean | `true` | Add `pipeline_id` to the resulting instance. |
| `add_document_id` | boolean | `true` | Add `document_id` to the resulting instance. |
| `max_steps` | integer | `1000000` | Hard cap on Starlark execution steps (protects against runaway loops). |
| `timeout_ms` | integer | `5000` | Wall-clock timeout in milliseconds. |

**Script contract.**

```python
def execute(data, config):
    # `data` is the parsed analyzer JSON (same shape the `raw` plugin sees:
    # data["document"]["text"], ["summary"], ["language"], ["sentences"], etc.).
    # `config` is whatever you put in `user_config`.
    # Return a list of dicts:
    return [
        {"action_label": "label_name", "values": ["one", "or", "more", "strings"]},
        # optional data_type override:
        {"action_label": "lang", "values": [data["document"]["language"]], "data_type": "DT_String"},
    ]
```

Each returned element becomes one `InstanceElement` on the `CreateInstance` call. `pipeline_id` and `document_id` are appended automatically (toggle via `add_pipeline_id` / `add_document_id`).

**Declaring the schema.** The script plugin does not carry its own schema field — when `create_action` is `true` it registers labels under its `action` using the pipeline-level `instance` block. Entries in `instance.instance_elements` carry both the schema (`component`, `default_data_type`, `min_occurrence`, `max_occurrence`) and, optionally, `values`. An entry **without** `values` is treated as a schema-only declaration: the label is registered but it is not included in the resulting `CreateInstance` (the script's output is responsible for supplying its values).

**Example**

```json
{
  "name": "demo-script-config",
  "connection_id": "00000000-0000-0000-0000-000000000001",
  "flow_configuration": { "name": "analyze", "config": {} },
  "instance": {
    "instance_elements": [
      {"action_label": "summary_upper", "component": "What", "default_data_type": "DT_String", "min_occurrence": 0, "max_occurrence": 1},
      {"action_label": "lang",          "component": "What", "default_data_type": "DT_String", "min_occurrence": 0, "max_occurrence": 1}
    ]
  },
  "plugins": [
    {
      "name": "script",
      "config": {
        "action": "document_script",
        "user_config": {"min_summary_len": 10},
        "script": "def execute(data, config):\n    doc = data['document']\n    summary = doc.get('summary', '')\n    if len(summary) < config.get('min_summary_len', 0):\n        return []\n    return [\n        {'action_label': 'summary_upper', 'values': [summary.upper()]},\n        {'action_label': 'lang',          'values': [doc.get('language', '')]},\n    ]\n"
      }
    }
  ]
}
```

**Clear behavior.** `Clear` deletes all instances of the configured `action` that match the current `pipeline_id` (same pattern as `raw`).

---

## Putting it together — an example pipeline configuration

```json
{
  "name": "demo-config",
  "connection_id": "00000000-0000-0000-0000-000000000001",
  "flow_configuration": {
    "name": "analyze",
    "config": {}
  },
  "plugins": [
    {
      "name": "raw",
      "config": {
        "action": "document_raw",
        "action_label": "document"
      }
    },
    {
      "name": "text",
      "config": {
        "action": "document_text",
        "text_actionlabel": "text"
      }
    },
    {
      "name": "segments_wide",
      "config": {
        "action": "document_segment_wide",
        "document_action_label": "document",
        "text_action_label": "text",
        "entity_types": ["PERSON", "ORG", "DATE"]
      }
    }
  ]
}
```

Submit this with `POST /pipeline_configurations` (to save as a reusable
template) or inline inside the `configuration` block of `POST
/pipelines`.
