# DecisionMaking PDF RAG generation review

## Coverage table

| source | pages | empty | low-text | extraction risk | nodes | evidence | review verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| `DM_PDF01` | 10 | 0 | 0 | 0 | 4 | 4 | text extraction usable |
| `DM_PDF02` | 43 | 0 | 11 | 11 | 3 | 3 | usable with OCR follow-up |
| `DM_PDF03` | 9 | 0 | 0 | 0 | 3 | 3 | text extraction usable |
| `DM_PDF04` | 44 | 0 | 10 | 10 | 3 | 3 | usable with OCR follow-up |
| `DM_PDF05` | 36 | 0 | 5 | 5 | 3 | 3 | usable with OCR follow-up |
| `DM_PDF06` | 36 | 0 | 9 | 9 | 4 | 4 | usable with OCR follow-up |
| `DM_PDF07` | 46 | 0 | 25 | 25 | 3 | 3 | usable with OCR follow-up |
| `DM_PDF08` | 25 | 0 | 13 | 13 | 3 | 3 | usable with OCR follow-up |

## 누락/보강 식별

- `DM_PDF02`: 11 page(s) need OCR/manual confirmation (empty=0, low_text=11).
- `DM_PDF04`: 10 page(s) need OCR/manual confirmation (empty=0, low_text=10).
- `DM_PDF05`: 5 page(s) need OCR/manual confirmation (empty=0, low_text=5).
- `DM_PDF06`: 9 page(s) need OCR/manual confirmation (empty=0, low_text=9).
- `DM_PDF07`: 25 page(s) need OCR/manual confirmation (empty=0, low_text=25).
- `DM_PDF08`: 13 page(s) need OCR/manual confirmation (empty=0, low_text=13).
- 모든 PDF에 최소 3개 이상 핵심 노드를 만들었고, 각 노드에는 evidence anchor를 부착했다.
- local sidecar edge는 local node 사이로만 두어 ghost id를 피했다.
- cross-PDF와 기존 1~7강 연결은 `DM_global_patterns.md`와 최종 RAG의 graph location에서 설명했다.

## 보강 조치

- 최종 RAG 문서에 `검토 후 보강 메모`를 추가했다.
- extraction gap/low-text page는 conflicts 파일과 review report에 명시했다.
- `DM_global_nodes.json`, `DM_global_edges.json`, `DM_global_patterns.md`를 추가해 통합 그래프 계층을 보강했다.
- flat pack은 PDF당 4파일로 생성했다: transcript, rawdata_develop, concept_node_index, rag.

## 남은 리스크

- 이미지로만 존재하는 표/수식은 OCR 없이 완전 전사할 수 없다.
- 일부 수식 글리프는 PDF 텍스트 레이어 품질 때문에 깨진 채 추출될 수 있다.
- 후속 수동 검토 시 빈 페이지와 표 이미지가 많은 PDF부터 OCR 보강이 필요하다.
