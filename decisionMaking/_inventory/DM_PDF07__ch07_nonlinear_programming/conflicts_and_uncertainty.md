# DM_PDF07 conflicts / 불확실성

## 1. PDF extraction gaps
- pages=46, empty_pages=0, low_text_pages=25, extracted_lines=400
- OCR 도구가 없는 환경에서 텍스트 레이어만 추출했다. `[EXTRACTION_GAP]` 또는 `[EXTRACTION_LOW_TEXT]` 페이지는 후속 OCR/수동 검토 대상이다.

## 2. Date policy
- 날짜 기반 lecture_id는 쓰지 않는다. source_id는 사용자가 지정한 PDF 순서 기준이다.

## 3. Cross-link policy
- 기존 `0330_5강.md`~`0420_7강.md`와의 연결은 RAG/brief에서 설명하되, local sidecar edge는 local node 사이만 둔다.
