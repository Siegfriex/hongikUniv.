# DecisionMaking PDF-only RAG policy

This course run has PDF slides only as new raw data. Unlike the ML RAG run,
there is no separate lecture recording transcript txt and no pre-existing
final_brief md for the eight new files.

## Source roles

- `decisionMaking/pdf_sources/*.pdf` is the immutable normalized PDF source
  layer.
- `decisionMaking/pdf_transcripts/*.md` is the full PDF transcription layer.
  It replaces the ML workflow's `final_record/*.txt` and must preserve page and
  line anchors.
- `decisionMaking/_inventory/<id>/` is the sidecar layer for graph/RAG
  preprocessing.
- `decisionMaking/final_brief/*.md` is the human study brief layer.
- `decisionMaking/rag_applied_flat_pack/` is the flat agent-facing RAG pack.

## ID policy

The original PDFs do not contain reliable lecture dates in their filenames.
Date inference is intentionally discarded for this batch. Use stable source
IDs based only on the exact order of the eight PDF paths provided by the user:

- `DM_PDF01` through `DM_PDF08` for immutable PDF source files.
- Page-line references use `DM_PDFxx:pNNN:LNNN`.
- If a PDF is later connected to a dated class note, the `manifest.json` must
  still keep the original `pdf_source_id` and normalized PDF path so evidence
  references remain stable.

Do not invent dates just to satisfy `YYYYMMDD_N`. For this PDF-only batch,
source folders may use `DM_PDFxx__<slug>` instead of dated `lecture_id`.

## Evidence policy

Every claim in nodes, edges, briefs, and RAG md must point back in this order:

1. final RAG block
2. sidecar id (`node_id`, `edge_id`, `segment_id`, `evidence_id`)
3. PDF transcript page-line anchor
4. normalized PDF filename
5. original PDF filename recorded in `pdf_sources/SOURCE_MAP.md`

## Required outputs per PDF

For each `DM_PDFxx`:

1. Full transcript: `pdf_transcripts/DM_PDFxx__<slug>__full_transcript.md`
2. Inventory sidecars: `_inventory/DM_PDFxx__<slug>/`
3. Raw-data develop md: `_inventory/DM_PDFxx__<slug>/DM_PDFxx__<slug>__rawdata_develop.md`
4. RAG md: `_inventory/DM_PDFxx__<slug>/DM_PDFxx__<slug>__rag.md`
5. Human brief: `final_brief/DM_PDFxx__<slug>__study_brief.md`
6. Flat pack copy: four files per PDF in `rag_applied_flat_pack/`

## Final RAG persona requirement

The final `*_rag.md` output is not a short summary. It must be written as a
teaching-grade RAG document for a dedicated 1:1 Operations Research tutor.
Follow `FINAL_RAG_TUTOR_PERSONA.md` when generating every final RAG document.

## PDF extraction note

At preparation time, this environment did not have `pdftotext`, `pdfinfo`,
`pypdf`, `PyPDF2`, or `fitz` installed. The extraction stage must first install
or provide a PDF text extraction tool, then run a page/line completeness check.
