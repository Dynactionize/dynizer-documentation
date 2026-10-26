# analyze-core — Documentation

## Table of Contents

- [Purpose](#purpose)
- [Architecture](#architecture)
- [Pipeline Stages](#pipeline-stages)
  - [Stage 1 — Decomposition](#stage-1--decomposition)
  - [Stage 2 — Action Extraction](#stage-2--action-extraction)
  - [Stage 3 — Segment Classification](#stage-3--segment-classification)
  - [Stage 4 — Entity Labeling](#stage-4--entity-labeling)
- [AnalysisService API](#analysisservice-api)
- [Training](#training)
  - [Training Data Format](#training-data-format)
  - [Config Overrides](#config-overrides)
  - [Sample Weighting](#sample-weighting)
  - [Class Weighting & Loss](#class-weighting--loss)
  - [Early Stopping](#early-stopping)
  - [Interim Checkpoints](#interim-checkpoints)
- [Evaluation](#evaluation)
- [Model Versioning](#model-versioning)
- [Base Model Registry](#base-model-registry)
- [Configuration Reference](#configuration-reference)
- [Utilities](#utilities)
- [Project Structure](#project-structure)
- [Glossary](#glossary)
- [Changelog](CHANGELOG.md)

---

## Purpose

`analyze-core` provides everything needed to **train, evaluate, and run inference** for a 4-stage NLP pipeline that transforms free-form text into structured action records:

```
"The manager approved the budget in London yesterday."
  Stage 1: Decomposition        -> ["The manager approved the budget in London yesterday"]
  Stage 2: Action Extraction    -> action_name="approve", labels=[0,0,1,0,0,0,0,0]
  Stage 3: Segment Classification -> WHO=[The manager], WHAT=[the budget], WHERE=[London], WHEN=[yesterday]
  Stage 4: Entity Labeling      -> Person, Object, Location, Date
```

Key properties:
- **Multilingual**: English, Dutch, French (extensible to 20+ languages via multilingual transformers)
- **Self-learning**: corrected examples receive higher training weight
- **Fallback-safe**: every stage has a rule-based fallback when no trained model exists
- **Versioned**: model snapshots saved after each training run with full metadata

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        AnalysisService                           │
│  Orchestrates all 4 stages, manages fallback, enriches segments  │
├──────────┬───────────────┬──────────────────┬────────────────────┤
│ Stage 1  │   Stage 2     │    Stage 3       │     Stage 4        │
│ Decomp.  │ Action Extr.  │ Segment Class.   │  Entity Label.     │
│ (mT5)    │ (Transformer  │ (BiLSTM+CRF on   │ (Transformer +     │
│          │  +linear head)│  Transformer     │  segment emb.+MLP) │ 
│          │               │  enc.)           │                    │
├──────────┴───────────────┴──────────────────┴────────────────────┤
│  Shared: callbacks, model_versioning, sample_weights, registry   │
└──────────────────────────────────────────────────────────────────┘
```

Each stage has a consistent structure: `config.py`, `model.py` (inference), `trainer.py` (training), `evaluator.py` (metrics).

---

## Pipeline Stages

### Stage 1 — Decomposition

**File**: `analyze_core/ml/decomposition/model.py`
**Architecture**: Seq2Seq (`google/flan-t5-small` or `google/mt5-small`) via `AutoModelForSeq2SeqLM`

**Example:**
```python
from analyze_core.ml.decomposition.model import DecompositionModel

model = DecompositionModel()
clauses = model.predict(
    "The girl danced in the park and the boy sang a song at home yesterday"
)
```

Output:
```python
[
    "The girl danced in the park",
    "the boy sang a song at home yesterday",
]
```

A simple sentence passes through unchanged:
```python
model.predict("The manager approved the budget")
# -> ["The manager approved the budget"]
```

**`predict()` signature:**
```python
def predict(
    text: str,
    language: str | None = None,
    allow_fallback: bool = True,
) -> list[str]
```

- **Input**: encoder receives `"decompose: {text}"`
- **Output**: list of clause strings (split on `|` separator, deduplicated, trailing punctuation stripped)
- **Generation**: `num_beams=4`, `no_repeat_ngram_size=3`, `repetition_penalty=1.2`
- **Fallback**: splits on conjunctions (`and/but/or/yet/so/while/because/although`) and semicolons
- **`allow_fallback=False`**: returns `[text]` instead of falling back

Also provides `predict_batch(texts, language) -> list[list[str]]`.

---

### Stage 2 — Action Extraction

**File**: `analyze_core/ml/action_extraction/model.py`
**Architecture**: `AutoModelForTokenClassification` (transformer + linear head, 2 labels)

**Example:**
```python
from analyze_core.ml.action_extraction.model import ActionExtractionModel

model = ActionExtractionModel()
result = model.predict("The manager approved the budget")
```

Output:
```python
{
    "tokens": ["The", "manager", "approved", "the", "budget"],
    "action_labels": [0, 0, 1, 0, 0],
    "action_name": "approve",       # lemmatized form of "approved"
    "confidence": 0.94,
}
```

The `action_labels` list is a binary mask — `1` marks the action verb token(s). The `action_name` is the lemmatized form (e.g. "approved" -> "approve", "is running" -> "run").

**`predict()` signature:**
```python
def predict(
    sentence: str,
    language: str | None = None,
    allow_fallback: bool = True,
) -> dict[str, Any]
```

- **Tokenization**: spaCy (same model as training to avoid subword mismatches)
- **Lemmatization**: spaCy lemmatizer (en/nl/fr)
- **Fallback**: spaCy POS tagging (`VERB`), confidence 0.7. Last resort: second token, confidence 0.3
- **`allow_fallback=False`**: returns empty `action_name` and confidence 0.0

---

### Stage 3 — Segment Classification

**File**: `analyze_core/ml/segment_classification/model.py`
**Architecture**: Transformer encoder + BiLSTM (2 layers, hidden=256) + CRF

**Example:**
```python
from analyze_core.ml.segment_classification.model import SegmentClassificationModel

model = SegmentClassificationModel()
result = model.predict(
    "The manager approved the budget in London yesterday",
    action_indices=[2],   # index of "approved" from Stage 2
)
```

Output:
```python
{
    "tokens": ["The", "manager", "approved", "the", "budget", "in", "London", "yesterday"],
    "bio_tags": ["B-WHO", "I-WHO", "O", "B-WHAT", "I-WHAT", "B-WHERE", "I-WHERE", "B-WHEN"],
    "segments": [
        {"ct": "who",   "tokens": [{"text": "The", "label": ""}, {"text": "manager", "label": ""}]},
        {"ct": "what",  "tokens": [{"text": "the", "label": ""}, {"text": "budget", "label": ""}]},
        {"ct": "where", "tokens": [{"text": "in", "label": ""},  {"text": "London", "label": ""}]},
        {"ct": "when",  "tokens": [{"text": "yesterday", "label": ""}]},
    ],
    "confidence": 0.85,
}
```

The `label` field in each token is empty at this stage; it gets filled by Stage 4.

**`predict()` signature:**
```python
def predict(
    sentence: str,
    action_indices: list[int] | None = None,
    language: str | None = None,
    allow_fallback: bool = True,
) -> dict[str, Any]
```

**About `action_indices`:**

This parameter is **optional** (defaults to `None`, treated as `[]`) but recommended. It tells the model which token positions are action verbs (from Stage 2's `action_labels`). It is used in two ways:

- **CRF model**: action token positions are forced to `O` tag, so the verb is excluded from WHO/WHAT/WHERE/WHEN segments.
- **Heuristic fallback**: the verb position is used to split tokens into before-verb (WHO) and after-verb (WHAT).

Without `action_indices`, the verb may incorrectly end up inside a segment (e.g. tagged as WHAT).

In practice, Stage 2 always runs first — even when the pipeline mode is `"segments"` — because the action indices are needed:

```python
# Inside AnalysisService._process_clause_partial():
action_result = self.action_extraction.predict(clause, language)
action_indices = [i for i, l in enumerate(action_result["action_labels"]) if l == 1]

# Then passed to Stage 3:
segment_result = self.segment_classification.predict(clause, action_indices, language)
```

**BIO tag set**: `O`, `B-WHO`, `I-WHO`, `B-WHAT`, `I-WHAT`, `B-WHERE`, `I-WHERE`, `B-WHEN`, `I-WHEN` (9 tags).

- **Fallback**: heuristic — before verb=WHO, after verb=WHAT, prepositional phrases=WHERE/WHEN
- **`allow_fallback=False`**: returns all-O tags with confidence 0.0

---

### Stage 4 — Entity Labeling

**File**: `analyze_core/ml/entity_labeling/model.py`
**Architecture**: `EntityClassifier` — transformer encoder + segment type embedding (dim=32) + MLP head

**Example:**
```python
from analyze_core.ml.entity_labeling.model import EntityLabelingModel

model = EntityLabelingModel()
result = model.predict(
    "The manager approved the budget in London yesterday",
    segments=[
        {"ct": "who",   "tokens": [{"text": "The"}, {"text": "manager"}]},
        {"ct": "what",  "tokens": [{"text": "the"}, {"text": "budget"}]},
        {"ct": "where", "tokens": [{"text": "in"},  {"text": "London"}]},
        {"ct": "when",  "tokens": [{"text": "yesterday"}]},
    ],
)
```

Output:
```python
{
    "segments": [
        {"ct": "who", "tokens": [
            {"text": "The", "label": "None"},
            {"text": "manager", "label": "Person"},
        ]},
        {"ct": "what", "tokens": [
            {"text": "the", "label": "None"},
            {"text": "budget", "label": "Object"},
        ]},
        {"ct": "where", "tokens": [
            {"text": "in", "label": "None"},
            {"text": "London", "label": "Location"},
        ]},
        {"ct": "when", "tokens": [
            {"text": "yesterday", "label": "Date"},
        ]},
    ],
    "confidence": 0.87,
}
```

Each token now has a fine-grained entity `label` from the taxonomy. Function words (articles, prepositions) typically get `"None"`.

**`predict()` signature:**
```python
def predict(
    sentence: str,
    segments: list[dict[str, Any]],
    language: str | None = None,
    allow_fallback: bool = True,
) -> dict[str, Any]
```

**Entity taxonomy:**

| Segment | Valid Entity Types |
|---------|-------------------|
| WHO     | Person, Organization, Group, Role, Animal, None |
| WHAT    | Object, Activity, Concept, Artwork, Product, Food, Event, None |
| WHERE   | Location, Facility, Address, GeoFeature, Region, Country, None |
| WHEN    | Date, Time, Duration, Frequency, Period, RelativeTime, None |

- **Taxonomy masking**: invalid entity types per segment are masked to `-inf` during inference
- **Low-token enrichment**: segments with < 3 tokens get clause context prepended to the encoder input
- **Fallback**: heuristic using spaCy NER and POS tags
- **`allow_fallback=False`**: returns segments with `"None"` labels, confidence 0.0

---

## AnalysisService API

**File**: `analyze_core/services/analysis_service.py`

### Constructor

```python
AnalysisService(
    decomposition_model=None,    # or a DecompositionModel instance
    action_model=None,           # or an ActionExtractionModel instance
    segment_model=None,          # or a SegmentClassificationModel instance
    entity_model=None,           # or an EntityLabelingModel instance
    base_models=None,            # dict: stage -> HuggingFace model ID
    model_dirs=None,             # dict: stage -> path to trained model directory
)
```

Set `service.allow_fallback = False` to disable rule-based fallback in all stages (for evaluation).

### Full Pipeline Example

```python
from analyze_core.services.analysis_service import AnalysisService

service = AnalysisService()
result = await service.analyze(
    "The girl danced in the park and the boy sang a song at home yesterday"
)
```

Output:
```python
{
    "job_id": "a1b2c3d4",
    "original_text": "The girl danced in the park and the boy sang a song at home yesterday",
    "language": "en",
    "mode": "full",
    "clauses": [
        "The girl danced in the park",
        "the boy sang a song at home yesterday",
    ],
    "action_records": [
        {
            "source_text": "The girl danced in the park",
            "original_text": "The girl danced in the park and the boy sang a song at home yesterday",
            "action_name": "dance",
            "segments": [
                {"ct": "who",   "tokens": [{"text": "The", "label": "None"}, {"text": "girl", "label": "Person"}]},
                {"ct": "where", "tokens": [{"text": "in", "label": "None"}, {"text": "the", "label": "None"}, {"text": "park", "label": "Location"}]},
            ],
            "confidence": 0.88,
            "confidence_per_stage": {
                "action_extraction": 0.92,
                "segment_classification": 0.85,
                "entity_labeling": 0.87,
            },
            "language": "en",
            "job_id": "a1b2c3d4",
            "reviewed": False,
        },
        {
            "source_text": "the boy sang a song at home yesterday",
            "original_text": "The girl danced in the park and the boy sang a song at home yesterday",
            "action_name": "sing",
            "segments": [
                {"ct": "who",   "tokens": [{"text": "the", "label": "None"}, {"text": "boy", "label": "Person"}]},
                {"ct": "what",  "tokens": [{"text": "a", "label": "None"}, {"text": "song", "label": "Object"}]},
                {"ct": "where", "tokens": [{"text": "at", "label": "None"}, {"text": "home", "label": "Location"}]},
                {"ct": "when",  "tokens": [{"text": "yesterday", "label": "Date"}]},
            ],
            "confidence": 0.86,
            "confidence_per_stage": {
                "action_extraction": 0.91,
                "segment_classification": 0.83,
                "entity_labeling": 0.85,
            },
            "language": "en",
            "job_id": "a1b2c3d4",
            "reviewed": False,
        },
    ],
}
```

### `analyze()`

```python
async def analyze(
    text: str,
    *,
    language: str | None = None,  # auto-detected if not provided
    job_id: str | None = None,
    mode: str = "full",           # full, decomposition, action, segments, entities
    created_by: str | None = None,
) -> dict[str, Any]
```

**Returns:**
```python
{
    "job_id": str,
    "original_text": str,
    "language": str,
    "mode": str,
    "clauses": list[str],
    "action_records": [
        {
            "source_text": str,
            "original_text": str,
            "action_name": str,
            "segments": list[dict],
            "confidence": float,
            "confidence_per_stage": {
                "action_extraction": float,
                "segment_classification": float,
                "entity_labeling": float,
            },
            "language": str,
            "job_id": str,
            "reviewed": False,
        }
    ],
}
```

### Individual Stage Methods

```python
def decompose(text, language=None) -> dict        # {"original_text", "clauses", "language"}
def extract_action(sentence, language=None) -> dict
def classify_segments(sentence, action_indices, language=None) -> dict
def label_entities(sentence, segments, language=None) -> dict
```

---

## Training

All 4 trainers share this interface:

```python
trainer.train(
    data: list[dict],
    config: dict | None = None,
    progress_callback: ProgressCallback | None = None,
    interim_checkpoint_callback: InterimCheckpointCallback | None = None,
) -> dict[str, Any]
```

**Returns:**
```python
{
    "model_path": str,
    "model": <trained model>,
    "tokenizer": <tokenizer>,
    "val_data": list[dict],
    "loss_history": [{"epoch": int, "train_loss": float, "eval_loss": float}],
    "num_examples": int,
}
```

### Training Data Format

Common fields:
```python
{
    "input_text": str,
    "output_data": ...,              # stage-specific (see below)
    "language": str,                 # "en", "nl", "fr"
    "split": "train"|"val"|"test",   # optional (otherwise random 90/10)
    "quality_score": float,          # optional, 0.0-1.0
    "provenance": str,               # optional, "corrected"|"accepted"|"generated"
}
```

**Stage-specific `output_data`:**

| Stage | Format |
|-------|--------|
| Decomposition | `list[str]` (clauses) or `dict` with `"sub_sentences"`/`"output"` key |
| Action Extraction | `{"action_name": str}` |
| Segment Classification | `{"bio_tags": list[str]}` or `{"segments": list[dict]}` |
| Entity Labeling | `{"segments": [{"ct": str, "tokens": [{"text": str, "label": str}]}]}` |

### Config Overrides

```python
trainer.train(data, config={
    "learning_rate": 5e-5,
    "batch_size": 4,
    "num_epochs": 15,
    "from_model_path": "/path/to/previous/version",
    "freeze_encoder": True,
})
```

### Sample Weighting

Reviewed examples are weighted by their **data quality** so the model leans on trustworthy data and de-emphasizes marginal examples (implemented in `ml/sample_weights.py`).

`quality_score` (0.0–1.0) is a *data-quality* rating produced upstream by `model-api`: it is computed from validation-error penalties (structural, semantic, duplicate, completeness) or set by an annotator (0 = bad, 0.5 = partial, 1 = good). **A high score means a trustworthy example; a low score means error-prone / unreliable data.** Weight therefore scales *up* with the score — better data gets more emphasis. Weight is assigned by a **smooth ramp** rather than discrete bands.

> **Note:** an earlier version of this code inverted this — it gave the *lowest*-quality examples the *highest* weight, on the mistaken assumption that `quality_score` measured the model's original difficulty. It does not; it measures the quality of the example itself. The direction was corrected on 2026-06-09 (see the [Changelog](CHANGELOG.md)).

#### Step buckets vs. smooth ramp

A **step bucket** (the original design) maps a *range* of scores to a single fixed weight. A **smooth ramp** maps the score *continuously*, so the weight changes a little for every little change in score. The difference only matters at the edges of the ranges:

| | Step buckets (old) | Smooth ramp (current) |
|---|---|---|
| `score = 0.40` | one fixed band value | ≈ 1.80x |
| `score = 0.41` | next band value (a jump) | ≈ 1.82x |
| **Change for a 0.01 score difference** | **up to 1.0x — a cliff** | **≈ 0.02x — gradual** |

With step buckets, a tiny perturbation that nudged a score across a bucket boundary swung its weight by a full `1.0`. Because quality scores often come from a noisy source (averaged human ratings, validation heuristics), examples sitting near a boundary got unstable weights from run to run. The smooth ramp removes those cliffs: neighbouring scores always map to neighbouring weights.

#### The formula

For reviewed examples (`provenance` is `"corrected"` or `"accepted"`), the weight interpolates linearly from `base_weight` at score `0.0` up to `max_weight` at score `1.0`:

```
fraction = min(max(quality_score, 0.0), 1.0)
weight   = base_weight + (max_weight - base_weight) * fraction
```

With the defaults `base_weight = 1.0`, `max_weight = 3.0`:

| `quality_score` | Weight |
|-----------------|--------|
| 0.0 | 1.0x (least trusted — floor) |
| 0.5 | 2.0x (midpoint) |
| 1.0 | 3.0x (most trusted — full weight) |

The weight is **monotonically non-decreasing** in the score — a higher-quality example never gets less weight than a lower-quality one. Non-reviewed examples (e.g. `provenance="original"`) and examples with a missing `quality_score` always get `base_weight` (the floor).

> Note `model-api` can also *exclude* low-quality examples from the training export entirely via its `quality_score_threshold` (default 0.7). When that filter is applied, the examples reaching the trainer already sit in the upper part of the ramp; when it is not, this weighting is what keeps marginal examples from dominating.

### Class Weighting & Loss

**Sample weighting and class weighting are different mechanisms, and both feed the same loss.** Sample weighting (above) scales the loss *per example* by its `quality_score`. Class weighting scales the loss *per label* to counter label-frequency imbalance. They compose: a token's loss contribution is its class/loss-function weight × its example's sample weight.

#### Class weights — Action Extraction (Stage 2)

Action extraction is a token-classification task where only ~1 token per sentence is the action verb (label `1`); every other token is `0`. Left uncorrected, the model can drive loss down by always predicting `0`. To counter this, `ActionExtractionTrainer._compute_class_weight` computes:

```
pos = #(label == 1)   neg = #(label == 0)
class_weight = [1.0, sqrt(neg / pos)]   # falls back to [1.0, 1.0] when pos == 0
```

- The positive class is up-weighted by the **negative/positive ratio**, so rare action tokens count more.
- The `sqrt` **dampens extreme ratios** (e.g. a 100× imbalance becomes 10×) to avoid over-correcting into false positives.
- Class `0` always stays at `1.0`; only the positive class is boosted.

#### Loss functions — Action Extraction (Stage 2)

Controlled by `loss_type` (default `focal`):

- **`focal`** (`ActionExtractionTrainer._focal_loss`) — down-weights easy, confident-correct predictions by `(1 - pt) ** gamma` (`focal_loss_gamma`, default 2.0) so training focuses on hard tokens. Class balance comes from `alpha` (`focal_loss_alpha`, default 0.75 on the positive class), used **instead of** the `sqrt(neg/pos)` class weights to avoid double-boosting. `labels == -100` (padding/special subwords) are excluded; an all-ignored row contributes `0.0` rather than `NaN`.
- **`cross_entropy`** — standard per-token CE using the `sqrt(neg/pos)` **class weights** above.

#### Class weights — Entity Labeling (Stage 4)

Entity labeling uses a different scheme: **inverse-frequency** class weights with a smoothing exponent. `use_class_weights` (default `True`) enables it; `class_weight_smoothing` (default 0.5) tempers how aggressively rare entity types are up-weighted. Taxonomy masking additionally constrains predictions to entity types valid for each segment during loss.

> Implementation: `analyze_core/ml/action_extraction/trainer.py` (`_compute_class_weight`, `_focal_loss`); see also the [Configuration Reference](#configuration-reference) for `loss_type`, `focal_loss_gamma`, `focal_loss_alpha`, `use_class_weights`, and `class_weight_smoothing`.

### Early Stopping

- **Stages 1 & 2** (HF Trainer): `EarlyStoppingCallback(patience=3)`, `load_best_model_at_end=True`
- **Stages 3 & 4** (custom loop): manual patience=3, minimum 4 epochs before stopping

### Interim Checkpoints

When validation loss improves, the model is saved to disk and registered as an interim version:
- If the worker crashes mid-training, the best-so-far model is still available
- Only one interim exists at a time (previous is replaced)
- On successful completion, the interim is deleted and replaced by the final version

**Stages 1 & 2**: `HFInterimCheckpointCallback` fires on `on_evaluate` in HF Trainer.
**Stages 3 & 4**: Inline logic in the training loop calls `interim_checkpoint_callback(epoch, val_loss, model_dir)`.

### Stage-Specific Training Details

**Decomposition**: `WeightedSeq2SeqTrainer` with Adafactor optimizer, `eval_strategy="steps"` (every 50 steps). Targets: `" | ".join(clauses)`.

**Action Extraction**: `WeightedTrainer` with class weight balancing (`sqrt(neg/pos)`). Supports `cross_entropy` or `focal` loss. Zero-label diagnostic logging warns when examples have no action token.

**Segment Classification**: Custom training loop. Differential LR: encoder LR vs head LR = `max(encoder_lr * 10, 5e-4)`. Cosine decay scheduler. All subwords of a word receive the word's tag.

**Entity Labeling**: Custom training loop. Data flattened to one example per segment. Differential LR: head = `max(encoder_lr * 100, 1e-3)`. Taxonomy masking during loss. Class weights via inverse-frequency smoothing.

---

## Evaluation

Each stage has an `Evaluator` with:

```python
evaluator.evaluate(model, test_data) -> dict[str, Any]
```

### Metrics by Stage

#### Decomposition (`DecompositionEvaluator`)

| Metric | Description |
|--------|-------------|
| `clause_f1` | Order-independent set F1, averaged across examples. Per example: `gold_set` and `pred_set` are lowercased, `tp = \|gold ∩ pred\|`, then standard F1 formula. |
| `exact_match` | Fraction of examples where the predicted clause set exactly equals the gold set (case-insensitive). |
| `calibration_error` | Expected Calibration Error (ECE) over 10 equal-width bins. Confidence is `sigmoid(beam_sequence_score)`, correctness is `exact_match`. |
| `error_categorization` | Qualitative breakdown of errors (up to 3 examples each). Categories: |

**Error categories** (multiple can apply to one example):
- `under_split` — fewer predicted clauses than gold (model didn't split enough)
- `over_split` — more predicted clauses than gold (model split too aggressively)
- `lost_content` — input content words missing from all predicted clauses
- `hallucination` — predicted words not found in the input or gold clauses
- `bad_coreference` — gold resolved pronouns but prediction kept them
- `wrong_boundary` — same clause count, different content, no lost/hallucinated words
- `other` — none of the above categories matched

**Return dict:**
```python
{
    "clause_f1": 0.85,
    "exact_match": 0.62,
    "eval_samples": 50,
    "calibration_error": 0.0732,
    "error_categorization": {
        "under_split": {"count": 5, "examples": [{"input": "...", "gold": [...], "predicted": [...]}]},
        "over_split": {"count": 3, "examples": [...]},
        "lost_content": {"count": 2, "examples": [...]},
        ...
    },
}
```

**Downstream impact evaluation** (`evaluate_downstream_impact()`): runs Stages 2-4 three ways — (a) with gold clauses (ceiling), (b) with predicted clauses (actual), (c) with no decomposition (floor) — to measure how decomposition quality affects downstream action extraction, segment classification, and entity labeling.

---

#### Action Extraction (`ActionExtractionEvaluator`)

| Metric | Description |
|--------|-------------|
| `token_f1` | Micro-averaged F1 across all tokens from all examples. Accumulates global TP/FP/FN. |
| `token_precision` | `TP / (TP + FP)` — of all tokens predicted as action, how many are correct. |
| `token_recall` | `TP / (TP + FN)` — of all actual action tokens, how many were found. |
| `action_name_accuracy` | Fraction of examples where the predicted lemmatized action name matches gold (case-insensitive). |
| `calibration_error` | Per-token ECE. Confidence = softmax probability of the predicted class. |
| `confusion_matrix` | All `(gold, pred)` pairs: `"0->1"`, `"1->0"`, etc. with counts. |
| `calibration` | Per-bucket detail (10 bins): `expected` confidence, `actual` accuracy, `count`. |

Word-level predictions are derived from subword logits: max subword probability per word, threshold at 0.5. The action name is the lemmatized form of the first predicted-action token.

**Return dict:**
```python
{
    "token_f1": 0.78,
    "token_precision": 0.82,
    "token_recall": 0.74,
    "action_name_accuracy": 0.85,
    "eval_samples": 50,
    "calibration_error": 0.0451,
    "confusion_matrix": {"0->1": 12, "1->0": 8},
    "calibration": {
        "0-10%": {"expected": 0.05, "actual": 0.02, "count": 120},
        "10-20%": {"expected": 0.15, "actual": 0.11, "count": 45},
        ...
    },
}
```

---

#### Segment Classification (`SegmentClassificationEvaluator`)

| Metric | Description |
|--------|-------------|
| `segment_f1` | Span-level micro F1. Spans are `(type, start, end)` tuples extracted from BIO sequences. A predicted span is a TP only if the exact same `(type, start, end)` exists in gold. |
| `segment_precision` | `TP / (TP + FP)` — of all predicted spans, how many exactly match a gold span. |
| `segment_recall` | `TP / (TP + FN)` — of all gold spans, how many were correctly predicted. |
| `tag_accuracy` | Per-token BIO tag accuracy across all tokens from all examples. |
| `calibration_error` | Per-token ECE. Confidence = max softmax probability of each word's first subword. |
| `confusion_matrix` | Off-diagonal only (misclassifications), top 50 by frequency. Format: `"B-who->O": 5`. |

Subword-to-word mapping uses the first subword per word. Span extraction: `B-X` starts a new span, `I-X` continues if the type matches (otherwise closes and reopens), `O` closes the current span.

**Return dict:**
```python
{
    "segment_f1": 0.72,
    "segment_precision": 0.75,
    "segment_recall": 0.69,
    "tag_accuracy": 0.81,
    "eval_samples": 50,
    "calibration_error": 0.0623,
    "confusion_matrix": {"B-who->O": 5, "I-what->O": 3, "O->B-where": 2, ...},
}
```

---

#### Entity Labeling (`EntityLabelingEvaluator`)

| Metric | Description |
|--------|-------------|
| `entity_accuracy` | Overall accuracy excluding tokens where gold label is `"None"` (function words). |
| `accuracy_who` | Accuracy for tokens in WHO segments only. |
| `accuracy_what` | Accuracy for tokens in WHAT segments only. |
| `accuracy_where` | Accuracy for tokens in WHERE segments only. |
| `accuracy_when` | Accuracy for tokens in WHEN segments only. |
| `macro_f1` | Unweighted mean of per-entity-class F1 scores (excluding `"None"` class). |
| `weighted_f1` | F1 weighted by each entity class's support count. |
| `per_entity_metrics` | Per-class precision, recall, F1, and support for every entity type. |
| `calibration_error` | Per-token ECE. Confidence = max softmax probability. |
| `confusion_matrix` | Off-diagonal only, top 50 by frequency. Format: `"Person->Organization": 3`. |

Tokens with gold label `"None"` are excluded from all metric computations. Per-class metrics are derived from the confusion matrix: `TP` = diagonal, `FP` = column sum off-diagonal, `FN` = row sum off-diagonal.

**Return dict:**
```python
{
    "entity_accuracy": 0.76,
    "accuracy_who": 0.82,
    "accuracy_what": 0.71,
    "accuracy_where": 0.79,
    "accuracy_when": 0.68,
    "macro_f1": 0.63,
    "weighted_f1": 0.69,
    "per_entity_metrics": {
        "Person": {"precision": 0.88, "recall": 0.85, "f1": 0.86, "support": 42},
        "Organization": {"precision": 0.72, "recall": 0.65, "f1": 0.68, "support": 18},
        "Location": {"precision": 0.81, "recall": 0.77, "f1": 0.79, "support": 25},
        "Date": {"precision": 0.90, "recall": 0.82, "f1": 0.86, "support": 15},
        ...
    },
    "eval_samples": 50,
    "calibration_error": 0.0534,
    "confusion_matrix": {"Person->Organization": 3, "Object->Activity": 2, ...},
}
```

---

#### Cross-Stage Summary

| | Decomposition | Action Extraction | Segment Classification | Entity Labeling |
|---|---|---|---|---|
| **Primary metric** | `clause_f1` | `token_f1` | `segment_f1` | `entity_accuracy` |
| **Granularity** | Per-example set | Per-token binary | Per-span (type,start,end) | Per-token multi-class |
| **Precision/Recall** | Embedded in F1 | Yes | Yes | Per-class only |
| **Exact/accuracy** | `exact_match` | `action_name_accuracy` | `tag_accuracy` | `accuracy_{type}` |
| **Macro/Weighted F1** | No | No | No | Yes |
| **Confusion matrix** | No (error categories instead) | All entries | Off-diagonal, top 50 | Off-diagonal, top 50 |
| **Calibration** | ECE (sequence-level) | ECE + per-bucket detail | ECE (token-level) | ECE (token-level) |
| **"None" excluded** | N/A | N/A | N/A | Yes |

---

## Model Versioning

**File**: `analyze_core/ml/model_versioning.py`

Versions are stored in `<model_dir>/versions/vN/` with a `version_meta.json`.

```python
from analyze_core.ml.model_versioning import save_version, list_versions, restore_version

# Save current model as a new version (auto-increments)
path = save_version(model_dir, stage="decomposition", epoch=10, train_loss=0.05)
# -> "<model_dir>/versions/v3/"

# List all versions (newest first)
versions = list_versions(model_dir)
# [{"version": "v3", "stage": ..., "timestamp": ..., "path": ...}, ...]

# Restore a specific version (copies files back to model_dir root)
restore_version(model_dir, "v2")
```

**`version_meta.json`** contains: `version`, `stage`, `timestamp`, `label`, `epochs_completed`, `final_train_loss`, plus any `extra_meta`.

---

## Base Model Registry

**File**: `analyze_core/ml/base_model_registry.py`

| Stage | Recommended | Size | Alternatives |
|-------|------------|------|--------------|
| Decomposition | `google/flan-t5-small` | 308 MB | `google/mt5-small` (1.2 GB) |
| Action Extraction | `xlm-roberta-base` | 1.1 GB | `distilbert-base-multilingual-cased` (540 MB), `bert-base-multilingual-cased` (680 MB) |
| Segment Classification | same | same | same |
| Entity Labeling | same | same | same |

```python
from analyze_core.ml.base_model_registry import get_presets_for_stage, STAGE_DEFAULTS

presets = get_presets_for_stage("decomposition")
STAGE_DEFAULTS["decomposition"]  # "google/flan-t5-small"
```

**`DownloadManager`** (`ml/download_manager.py`): singleton that handles background HuggingFace model downloads with progress tracking.

```python
from analyze_core.ml.download_manager import get_download_manager

dm = get_download_manager()
await dm.start_download("decomposition", "google/flan-t5-small")
dm.get_status("decomposition")  # {"status": "downloading", "progress": 0.45, "error": None}
```

---

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_DIR` | `./models` | Root directory for all stage model directories |
| `ALLOW_FALLBACK` | `true` | Enable/disable rule-based fallback globally |
| `TRAINING_MAX_MEMORY_GB` | `7.0` | RSS limit during training (kills training if exceeded) |
| `HF_HUB_DOWNLOAD_TIMEOUT` | `300` | HuggingFace download timeout (seconds) |

### Shared Config Fields

| Field | Default | Description |
|-------|---------|-------------|
| `model_name` | See registry | HuggingFace model ID |
| `model_dir` | `$MODEL_DIR/<stage>` | Trained model path |
| `learning_rate` | 1e-4 (S1), 3e-5 (S2-4) | LR |
| `batch_size` | 2 | Batch size |
| `num_epochs` | 20 (S1), 10 (S2-4) | Max epochs |
| `gradient_accumulation_steps` | 8 | Effective batch = batch_size * this |
| `warmup_steps` | 10 (S1), 100 (S2-4) | LR warmup |
| `weight_decay` | 0.01 | AdamW weight decay |

### Stage-Specific Config Fields

| Field | Stage | Default | Description |
|-------|-------|---------|-------------|
| `max_input_length` | 1 | 128 | Max encoder tokens |
| `max_output_length` | 1 | 256 | Max decoder tokens |
| `separator_token` | 1 | `\|` | Clause separator |
| `label_smoothing` | 1 | 0.1 | Label smoothing |
| `loss_type` | 2, 4 | `cross_entropy` | `cross_entropy` or `focal` |
| `focal_loss_gamma` | 2, 4 | 2.0 | Focal loss gamma |
| `focal_loss_alpha` | 2 | 0.75 | Focal loss alpha (positive class) |
| `num_labels` | 2 | 2 | Token classification labels |
| `lstm_hidden_size` | 3 | 256 | BiLSTM hidden dim |
| `lstm_layers` | 3 | 2 | BiLSTM layers |
| `num_tags` | 3 | 9 | BIO tag count |
| `segment_embedding_dim` | 4 | 32 | Segment type embedding |
| `use_taxonomy_masking` | 4 | True | Mask invalid entity types |
| `use_class_weights` | 4 | True | Inverse-frequency weighting |
| `class_weight_smoothing` | 4 | 0.5 | Smoothing exponent |

---

## Utilities

### Language Detection (`utils/language.py`)

```python
from analyze_core.utils.language import detect_language, SUPPORTED_LANGUAGES
# SUPPORTED_LANGUAGES = {"en", "nl", "fr"}
detect_language("The manager approved the budget")  # "en"
```

Deterministic (`langdetect` with seed=0). Returns `"en"` for unsupported/undetectable.

### BIO Utilities (`ml/segment_classification/bio_utils.py`)

```python
from analyze_core.ml.segment_classification.bio_utils import tags_to_segments, segments_to_tags

segments = tags_to_segments(tokens, bio_tags)   # BIO -> segment dicts
tags = segments_to_tags(tokens, segments)        # segment dicts -> BIO
```

### Entity Taxonomy (`ml/entity_labeling/taxonomy.py`)

```python
from analyze_core.ml.entity_labeling.taxonomy import get_valid_entities, mask_invalid_entities

get_valid_entities("who")  # ["Person", "Organization", "Group", "Role", "Animal", "None"]
```

### Callbacks (`ml/callbacks.py`)

```python
from analyze_core.ml.callbacks import TrainingProgress, ProgressCallback, InterimCheckpointCallback, ThrottledCallback

# TrainingProgress: dataclass with epoch, total_epochs, batch, total_batches, loss
# ProgressCallback = Callable[[TrainingProgress], None]
# InterimCheckpointCallback = Callable[[int, float, str], None]  # (epoch, val_loss, model_dir)

throttled = ThrottledCallback(callback, min_interval_seconds=5.0)
# Suppresses rapid calls; always forwards last batch of each epoch
```

### HF Progress Bridge (`ml/hf_progress_bridge.py`)

- `HFProgressBridge` — adapts HF Trainer events to `ProgressCallback`
- `HFInterimCheckpointCallback` — fires `InterimCheckpointCallback` when eval_loss improves
- `LossHistoryCallback` — collects `{epoch, train_loss, eval_loss}` into `.history`
- `MemoryWatchdogCallback` — raises `MemoryError` if RSS exceeds `TRAINING_MAX_MEMORY_GB`

### Sample Weights (`ml/sample_weights.py`)

```python
from analyze_core.ml.sample_weights import compute_sample_weight, compute_sample_weights

w = compute_sample_weight(quality_score=0.3, provenance="corrected")  # 3.0
ws = compute_sample_weights(data_list)  # list of weights
```

---

## Project Structure

```
analyze-core/
  pyproject.toml                          # v0.2.0, dependencies
  Makefile                                # install, test, lint
  azure-pipelines.yml                     # CI/CD
  docs/
    DOCUMENTATION.md                      # This file
  analyze_core/
    services/
      analysis_service.py                 # Pipeline orchestrator
    ml/
      callbacks.py                        # TrainingProgress, ProgressCallback, InterimCheckpointCallback
      hf_progress_bridge.py               # HF Trainer adapters (progress, interim, memory)
      model_versioning.py                 # save_version, list_versions, restore_version
      sample_weights.py                   # Quality-aware sample weighting
      base_model_registry.py              # Model presets and STAGE_DEFAULTS
      download_manager.py                 # Background HuggingFace downloads
      decomposition/                      # Stage 1
        config.py, model.py, trainer.py, evaluator.py
      action_extraction/                  # Stage 2
        config.py, model.py, trainer.py, evaluator.py, lemmatizer.py
      segment_classification/             # Stage 3
        config.py, model.py, trainer.py, evaluator.py, bio_utils.py
      entity_labeling/                    # Stage 4
        config.py, model.py, trainer.py, evaluator.py, taxonomy.py
    utils/
      language.py                         # detect_language
  tests/                                  # pytest suite
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **Adafactor** | Memory-efficient optimizer that adapts learning rates per parameter. Used in Stage 1 (mT5). |
| **AdamW** | Optimizer variant of Adam with decoupled weight decay. Used in Stages 2-4. |
| **BIO tagging** | Labeling scheme where `B-X` = beginning of segment type X, `I-X` = inside/continuation, `O` = outside any segment. |
| **BiLSTM** | Bidirectional Long Short-Term Memory — an RNN that reads the sequence both left-to-right and right-to-left. Used in Stage 3. |
| **Calibration error (ECE)** | Expected Calibration Error — measures how well a model's confidence scores match its actual accuracy. Computed over 10 equal-width bins. Lower is better. |
| **Class weights** | Per-class multipliers on the loss to counter label imbalance (e.g. rare action tokens get higher weight). |
| **Confusion matrix** | Table of `(gold_label, predicted_label)` counts showing which classes get confused with each other. |
| **Cosine decay** | Learning rate schedule that decreases following a cosine curve from initial LR down to ~0. |
| **CRF** | Conditional Random Field — a sequence labeling layer that models dependencies between adjacent tags (e.g. `I-WHO` can only follow `B-WHO`). |
| **Differential LR** | Using different learning rates for different parts of the model — typically a lower LR for the pretrained encoder and a higher LR for the randomly initialized head. |
| **Dropout** | Regularization technique that randomly zeroes a fraction of neuron activations during training to prevent overfitting. Disabled at inference via `model.eval()`. |
| **ECE** | See Calibration error. |
| **Encoder** | The pretrained transformer (e.g. DistilBERT, XLM-RoBERTa) that converts tokens into contextual embeddings. |
| **Epoch** | One complete pass through the entire training dataset. |
| **F1 score** | Harmonic mean of precision and recall: `2 * P * R / (P + R)`. Balances both metrics. |
| **Focal loss** | Loss function that down-weights easy (high-confidence) examples and focuses on hard ones. Controlled by `gamma` (focusing) and `alpha` (class balance). |
| **Freeze encoder** | Fixing the pretrained encoder weights during training so only the task-specific head is updated. Useful with small datasets. |
| **Gradient accumulation** | Simulates larger batch sizes by accumulating gradients over multiple forward passes before updating weights. Effective batch = `batch_size * gradient_accumulation_steps`. |
| **Head** | The task-specific layers added on top of the encoder (e.g. linear classifier, MLP, BiLSTM+CRF). Randomly initialized and trained from scratch. |
| **HF Trainer** | HuggingFace `Trainer` / `Seq2SeqTrainer` — a training loop abstraction that handles batching, evaluation, checkpointing, and logging. |
| **Label smoothing** | Softens one-hot training targets (e.g. 0.9 instead of 1.0) to reduce overconfidence. Used in Stage 1. |
| **Lemmatization** | Reducing a word to its base/dictionary form (e.g. "approved" -> "approve", "running" -> "run"). |
| **LR** | Learning Rate — step size for weight updates during training. Too high = unstable, too low = slow convergence. |
| **Macro F1** | Unweighted average of per-class F1 scores. Treats all classes equally regardless of frequency. |
| **MLP** | Multi-Layer Perceptron — a feedforward neural network (linear layers + activation functions). Used as the classification head in Stage 4. |
| **mT5** | Multilingual T5 — a pretrained seq2seq transformer supporting 101 languages. |
| **Patience** | Number of evaluation rounds without improvement before early stopping triggers. |
| **Precision** | Of all items predicted as positive, what fraction is actually positive: `TP / (TP + FP)`. |
| **Recall** | Of all actually positive items, what fraction was predicted as positive: `TP / (TP + FN)`. |
| **RSS** | Resident Set Size — the amount of physical memory (RAM) a process is currently using. |
| **Seq2Seq** | Sequence-to-sequence — a model architecture with an encoder (reads input) and decoder (generates output). Used in Stage 1 for decomposition. |
| **Softmax** | Function that converts raw logits into a probability distribution (values sum to 1). |
| **Subword tokenization** | Breaking words into smaller pieces (e.g. "approved" -> `["appro", "##ved"]`). Models like BERT/DistilBERT operate at the subword level. |
| **Taxonomy masking** | Preventing the model from predicting entity types that are invalid for a given segment (e.g. "Person" is invalid for a WHERE segment). |
| **TP / FP / FN** | True Positive (correct hit), False Positive (false alarm), False Negative (miss). |
| **Transformer** | Neural network architecture based on self-attention. Pretrained models (BERT, T5, XLM-R) are fine-tuned for downstream tasks. |
| **Val loss** | Validation loss — the loss computed on held-out data (not used for training). Used to detect overfitting and trigger early stopping. |
| **Warmup steps** | Initial training steps where the learning rate gradually increases from 0 to the target LR, preventing early instability. |
| **Weight decay** | Regularization that penalizes large weights by adding a fraction of the weight magnitude to the loss. Prevents overfitting. |
| **Weighted F1** | Average of per-class F1 scores weighted by each class's support (number of examples). Gives more influence to frequent classes. |
| **XLM-RoBERTa** | Cross-lingual pretrained transformer supporting 100 languages. Alternative base model for Stages 2-4. |
