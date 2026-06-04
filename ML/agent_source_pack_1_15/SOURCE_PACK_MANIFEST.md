# ML 1~15 Agent Source Pack

## Purpose

This folder collects the selected source files for a Codex/agent run that needs the ML 1~15 course objective plan, lecture RAG structure, transcript evidence, and inventory framework.

Source root in this pack:

```text
ML/agent_source_pack_1_15/ML/
```

## Included

### Framework and Inventory

- `ML/_framework/`
- `ML/_inventory/`

These include the agent workflow, schemas, prompts, inventory sidecars, RAG documents, raw-develop documents, verification reports, and the final 1~15 education plan.

### Lecture Structure Sources

- `ML/20250306.md`
- `ML/20250313.md`
- `ML/20250319.md`
- `ML/20250326.md`
- `ML/20260409.md`
- `ML/20260416.md`
- `ML/20260430_8강.md`
- `ML/20260507_10강.md`
- `ML/20260514_11강.md`
- `ML/20260521_12강.md`
- `ML/20260528_13강.md`
- `ML/20260529_14강.md`
- `ML/20260604_15강.md`

### Lecture Recording Transcript Sources

- `ML/final_record/기계학습0430.txt`
- `ML/final_record/기계학습0507.txt`
- `ML/final_record/0514ml.txt`
- `ML/final_record/0521Ml.txt`
- `ML/final_record/0528ml.txt`
- `ML/final_record/0529_ml.txt`
- `ML/final_record/0604ml.txt`

No raw audio files were present in the working tree at pack creation time. These transcript files are the current recording-derived source layer.

### Supporting Lecture Assets

- `ML/week09_examples.ipynb`
- `ML/week13.pdf`
- `ML/week14_NN실험Tips.pdf`
- `ML/wk_14_cnn (1).pdf`
- `ML/week14_lecture_keras_torch_results.ipynb`
- `ML/cnn_fMNIST.ipynb`

## Excluded

- `*:Zone.Identifier`
- `ML/final_record/0522ml.txt`
  - skipped because matching `final_brief` does not exist in the current batch.
- `ML/final_record/0529이용오교수님.txt`
  - secondary/conflict transcript for 14강; primary transcript is `ML/final_record/0529_ml.txt`.
- `ML/week13 (3).pdf`
  - duplicate-candidate PDF; use `ML/week13.pdf` as the primary source unless hash-verified otherwise.
- `docx-export/`
  - exported document artifacts, not the primary agent source layer.

## Validation Expectations

Before using this pack, verify:

```text
no Zone.Identifier files
all referenced primary transcripts exist
all inventory node/edge/evidence references validate
ML/_inventory/education_plan_1_15_final.md has no missing path references
```
