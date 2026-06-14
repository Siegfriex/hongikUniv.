# DecisionMaking PDF source map

This map preserves the link between the original user-provided filenames under
`decision/` and the normalized RAG source filenames under
`decisionMaking/pdf_sources/`.

## Naming rule

- Prefix: `DM_PDFxx`
- Slug: lowercase English topic label
- Extension: `.pdf`
- Source IDs are stable intake IDs, not final lecture dates.
- The `xx` number follows the exact eight-PDF order provided by the user in
  the source path list. It does not follow chapter number, date, filename sort,
  or inferred curriculum order.

## Sources

| source_id | normalized filename | original filename | topic | current linkage |
|---|---|---|---|---|
| `DM_PDF01` | `DM_PDF01_ch04_simplex_tableau_twophase_supplement.pdf` | `4장 심플렉스법(보완_심플렉스 타블로이용, 2단계법)_수정본 (7).pdf` | Ch.4 simplex tableau, special cases, two-phase method | Strong link to `0413_6강.md`; also reinforces `0406_5강.md` |
| `DM_PDF02` | `DM_PDF02_ch05_sensitivity_analysis.pdf` | `Ch.5 Sensitivity analysis (Ch. 5)_26 (2).pdf` | sensitivity analysis | Extends duality/shadow price material; cross-link to `0420_7강.md` |
| `DM_PDF03` | `DM_PDF03_ch06_branch_and_bound.pdf` | `6장_분지한계법 (1).pdf` | branch and bound | Integer programming solution method; cross-link to integer-programming PDFs |
| `DM_PDF04` | `DM_PDF04_ch06_integer_programming_week1.pdf` | `6장_정수계획(1주)_hs_26 (2).pdf` | integer programming week 1 | Post-LP model extension into integrality and 0-1 structure |
| `DM_PDF05` | `DM_PDF05_ch04_simplex_duality_week2.pdf` | `4장 심플렉스법과 쌍대성(2주)_hs (7).pdf` | Ch.4 simplex, duality bridge | Strong link to `0420_7강.md`; depends on `0413_6강.md` |
| `DM_PDF06` | `DM_PDF06_ch05_transportation_network_week1.pdf` | `5장 수송 및 네트워크 (1주)_hs (6).pdf` | transportation and network models | Network-structured LP extension |
| `DM_PDF07` | `DM_PDF07_ch07_nonlinear_programming.pdf` | `7장비선형계획26_hs.pdf` | nonlinear programming | Later-course nonlinear decision model unit |
| `DM_PDF08` | `DM_PDF08_ch06_integer_programming_week2.pdf` | `6장_정수계획(2주)_hs (1).pdf` | integer programming week 2 | Continues integer-programming model and solution material |

## User-provided intake order

`DM_PDF01`
-> `DM_PDF02`
-> `DM_PDF03`
-> `DM_PDF04`
-> `DM_PDF05`
-> `DM_PDF06`
-> `DM_PDF07`
-> `DM_PDF08`

This is the operational order for renaming, extraction, batching, and pack
generation.

## Concept dependency spine

The conceptual graph may differ from intake order. Cross-links should preserve
both:

`0330_5강.md` LP formulation
-> `0406_5강.md` simplex basics
-> `0413_6강.md` tableau and two-phase method
-> `0420_7강.md` duality and sensitivity
-> `DM_PDF02` sensitivity analysis
-> `DM_PDF06` transportation/network
-> `DM_PDF04` and `DM_PDF08` integer programming
-> `DM_PDF03` branch and bound
-> `DM_PDF07` nonlinear programming
