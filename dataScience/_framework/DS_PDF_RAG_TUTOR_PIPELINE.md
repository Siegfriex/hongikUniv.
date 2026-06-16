# dataScience PDF RAG tutor pipeline

## Source policy

- 원본 PDF는 `dataScience/pdf_raw/`에 보존한다.
- 로컬 PDF 파싱 결과는 `dataScience/txt_raw/`의 TXT 전사본으로 둔다.
- `dataScience/_inventory/<DS_PDFxx__slug>/`는 TXT 전사본을 기반으로 한 구조화 작업 공간이다.
- 의사결정 작업의 `decisionMaking/_framework`, `decisionMaking/_inventory`, `decisionMaking/assets`를 참조하되, DS 산출물은 `dataScience/` 아래에 둔다.

## End-to-end stages

1. PDF raw freeze: 첨부 PDF를 immutable source로 유지한다.
2. TXT raw transcript: 페이지 마커가 있는 TXT를 만든다.
3. Deep learning design: 각 PDF별 핵심질문, 선수개념, 실습/코드 관점, 오해 포인트를 정리한다.
4. Node-link inventory: `nodes.json`, `edges.json`, `evidence.jsonl`로 선행/후속/유사/혼동 관계를 만든다.
5. RAG and rawdata develop: `*_rag.md`, `*_rawdata_develop.md`를 GPT 프로젝트 소스로 바로 넣을 수 있게 작성한다.
6. Web grounding: 최신·외부 설명이 필요한 주제는 별도 `web_grounding` evidence로 분리하고, PDF/TXT 근거와 섞어 쓰지 않는다.
7. Tutor source pack: 최종 산출물을 flat pack으로 묶어 “지도부터”, “노드 중심”, “예제 중심”, “문제 풀이 모드”를 지원하게 한다.

## Tutor mode requirements

- 정의만 쓰지 말고, 직관/수식/도구/코드/데이터 예시를 함께 제공한다.
- 각 노드는 선행 노드, 후속 노드, 유사 노드, 흔한 오해를 가진다.
- DS 특성상 통계, 시각화, R/Python, 머신러닝, LLM 사이의 연결을 계속 표시한다.
