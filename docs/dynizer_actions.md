---
name: dynizer_actions
description: Explains Dynizer Actions, ActionLabels, ActionSchemas, Instances, semantic categories (Who/What/Where/When), and how conventional data maps to Actions.
---

# Dynizer Actions and ActionSchemas

## Introduction
Dynizer is a semantic data platform that organizes information into four core categories: **Who**, **What**, **Where**, and **When**. These elements are connected through **Actions**, which represent context-specific relationships between data points.

Building Actions enables:
- Easy integration of structured and unstructured data.
- Semantic indexing for detecting complex relationships.
- Advanced analytics beyond relational models.
- Improved AI and LLM interactions via structured semantic context.

## Understanding Actions

### Actions
In Dynizer, **Actions** represent meaningful events or situations derived from data.
They are *context-aware semantic links* that connect fundamental dimensions of information: *Who*, *What*, *Where*, and *When*.

Rather than treating data as isolated values, Dynizer models data as *relationships occurring within a context*. Each Action captures *how semantic elements interact in a specific situation*.

Key characteristics of Actions:
- Actions are stored in the **Core Semantic Index**, implemented as a compressed **bit-matrix engine** for efficiency and scalability.
- Each Action explicitly links multiple semantic elements while preserving their contextual meaning.
- *Generic semantic* categories (e.g., Who, What) are enriched with *domain-specific* labels, allowing the same structure to adapt across domains such as healthcare, finance, or legal documents.

In essence, an Action is Dynizer's fundamental unit of meaning.

### Action Components
An Action is composed of:
- **Semantic categories**: abstract dimensions such as *Who*, *What*, *Where*, *When* describing its role in meaning.
- **Labels**: domain-specific roles that refine each semantic category (e.g., *doctor*, *patient*, *city*).

A set of values of the semantic categories of an action is called an **Instance**.

**Example: Medical Consultation Action**

This Action is constructed using the following semantic categories and labels:

| Semantic category | Label   |
|-------------------|---------|
| Who               | Doctor  |
| Who               | Patient |
| What              | Sickness|
| Where             | City    |
| When              | When    |

Similar to a relational database, an action can be represented as a *table* in the semantic index:

**Action Name**: Medical Consultation

| Who (Doctor) | Who (Patient) | What (Sickness) | When (When)          | Where (City) |
|--------------|---------------|------------------|----------------------|--------------|
| Dr. Stranger | John Doe      | Flu Check        | 24th of December     | Gent         |

### Conventional Data to Actions
Dynizer Actions provide a unifying abstraction that can model traditional data systems:

- **Relational DB**:
  - Table -> Action
  - Columns -> Semantic category
  - Column names -> Labels
- **Document DB**:
  - Document -> Action
  - Fields -> Semantic elements
- **Graph DB**:
  - Nodes -> Semantic categories
  - Relations -> Combine nodes into Actions

Through this transformation, Dynizer preserves existing data while enriching it with *explicit semantics*, *context*, and *interpretability*, enabling deeper analysis beyond conventional data models.

### Different Schemas of Actions
Actions can be organized into different schemas, each defining a distinct scope of use and visibility.
This separation makes it possible to distinguish between schemas that are shared and commonly used by regular users and schemas that are restricted, hidden from standard access, and reserved for administrators.
Such administrative schemas support security, governance, and internal control without exposing sensitive structures to end users.

### ReferenceJSONfiles
`ReferenceJSONfiles` is the Dynizer action that stores document-analysis JSON outputs for matching. Each instance represents one file's JSON plus metadata, with labels: `JSON_ID`, `FileName`, `Content` (raw JSON blob), and optional `MatchingStructure` (prepared structure).
Status is derived from MatchingStructure: RAW if empty, ReadyToMatch if present.

## API Overview

Dynizer provides a REST API for managing Actions, Action Labels, Action Instances and Action Schemas. Key endpoint groups:

- **Actions**: Create, list, fetch, rename, delete actions
- **ActionLabels**: Add, fetch, update, delete labels within an action
- **ActionSchemas**: Create, list, fetch, rename, delete schemas
- **Instances**: Create, fetch, update, delete instances with values
- **Metadata**: Attach key-value metadata to instances and instance cells
- **Check**: Validate action and label names before creation
