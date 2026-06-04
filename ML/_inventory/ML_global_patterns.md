# ML Inventory Global Patterns

| rule | pattern | application |
|------|---------|-------------|
| Rule A | batch default G=[8,32] for final_brief/final_record lectures | Used for 20260430-20260604 auto segmentation QA. |
| Rule B′ | admin/prelecture exists when transcript contains metadata, breaks, closing, or administrative notes | Marker-only annotated transcript preserves original lines. |
| Rule D | numbered md sections become md-primary evidence; transcript chunks are supporting evidence | Applies to all generated nodes. |
| segment_type | admin, lecture_core, code_demo, admin_or_other_lecture | code_demo may be refined manually after notebook/code-heavy QA. |
