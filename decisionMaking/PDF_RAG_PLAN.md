# DecisionMaking PDF RAG plan

## Current branch state

- Working branch: `DS_decisionMaking`
- Remote head fetched: `origin/DS_decisionMaking`
- Existing developed course notes:
  - `0330_5강.md`
  - `0406_5강.md`
  - `0413_6강.md`
  - `0420_7강.md`
- New raw inputs: eight PDFs normalized under `pdf_sources/`
- PDF numbering: follows the exact user-provided path order, not dates,
  chapter order, filename sort, or inferred lecture chronology.

## Target directories

| path | role |
|---|---|
| `pdf_sources/` | immutable normalized PDF source copies |
| `pdf_transcripts/` | full page/line PDF transcriptions |
| `_framework/` | copied ML RAG framework plus PDF-only policy |
| `_inventory/` | node/edge/segment/evidence sidecars |
| `final_brief/` | deep human study briefs derived from PDF transcripts and sidecars |
| `rag_applied_flat_pack/` | flat agent-facing pack, four files per PDF |
| `workshop/` | later practice problems, checklists, and study workflows |

## Final RAG persona

The final `3) RAG` document must target a dedicated 1:1 tutor persona, not a
generic retrieval summary. The generator must follow
`_framework/FINAL_RAG_TUTOR_PERSONA.md`.

Minimum final RAG sections:

1. current graph location
2. one-line thesis
3. concept node map
4. prerequisite / follow-up / analogous concept links
5. definition -> intuition -> formula/model -> lecture example -> common
   mistake -> connection pattern for each core node
6. worked example or modeling coach block
7. formula in three translations: real-world language, mathematical language,
   spreadsheet/tableau language
8. exam-risk and misconception checklist
9. self-check questions and mini task
10. source trace table linking RAG labels -> sidecar IDs -> PDF transcript
    page-line anchors -> normalized PDF source

## Execution plan

### Phase 0. Preservation and intake

1. Keep `decision/` original PDFs untouched.
2. Use `pdf_sources/DM_PDFxx_*.pdf` as the normalized immutable source layer.
3. Treat `pdf_sources/SOURCE_MAP.md` as the filename SSOT.

### Phase 1. Full PDF transcription

For each PDF:

1. Extract text page by page.
2. Write `pdf_transcripts/DM_PDFxx__<slug>__full_transcript.md`.
3. Add stable anchors in the form `DM_PDFxx:pNNN:LNNN`.
4. Preserve formulas, tables, examples, and slide ordering as much as possible.
5. Mark extraction uncertainty explicitly when tables/formulas are visually
   present but text extraction is incomplete.

Verification:

- page count matches PDF pages
- transcript has page anchors for every extracted page
- no empty transcript unless the PDF is image-only
- image-only pages are queued for OCR/manual transcription

### Phase 2. RAG preprocessing and graph build

For each `DM_PDFxx`:

1. Create `_inventory/DM_PDFxx__<slug>/`.
2. Generate:
   - `manifest.json`
   - `anchors_md.json` or `anchors_pdf.json`
   - `segments.jsonl`
   - `alignments.jsonl`
   - `evidence.jsonl`
   - `nodes.json`
   - `edges.json`
   - `conflicts_and_uncertainty.md`
3. Use node IDs like `n_DM_PDF01.tableau_pivot_rule` during intake.
4. Add cross-source edges for prerequisite, extends, contrasts_with,
   commonly_confused_with, applies_to, and grounded_by relations.

Verification:

- every node has at least one anchor or evidence reference
- every edge endpoint exists
- every evidence line range resolves to a transcript anchor
- cross-PDF dependencies are listed in both local sidecars and the global graph

### Phase 3. Human study brief and final RAG pack

For each `DM_PDFxx`, produce:

1. `*_rawdata_develop.md`: detailed explanation, normalization, table/formula
   reconstruction, and why the PDF matters in the course sequence.
2. `*_concept_node_index.md`: compact node/edge map for agent lookup.
3. `*_rag.md`: final RAG document with labels that jump back to sidecar IDs and
   PDF transcript anchors.
4. `final_brief/*_study_brief.md`: dense Korean study brief with step-by-step
   learning flow, prerequisite checks, worked examples, and exam-risk points.

Flat pack rule:

- Copy the four agent-facing files per PDF into `rag_applied_flat_pack/`.
- Keep filenames prefixed with `DM_PDFxx`.
- Do not include raw JSON in the flat pack unless explicitly requested.

## Global graph plan

Create `decisionMaking/_inventory/DM_global_patterns.md` after the first full
batch pass. It should include:

- source dependency spine
- recurring model-formulation nodes
- simplex/duality/sensitivity bridge nodes
- transportation/network extension nodes
- integer-programming and branch-and-bound nodes
- nonlinear-programming transition nodes
- common confusion pairs
- exam-priority map

## Immediate blockers before extraction

The current environment lacks an installed PDF text extraction tool:

- `pdftotext`: not found
- `pdfinfo`: not found
- `pypdf`: not installed
- `PyPDF2`: not installed
- `fitz`: not installed

Next execution step is to install or provide a PDF extraction dependency, then
run Phase 1 on `DM_PDF01` as the pilot before batching all eight PDFs.
