# CODEBASE_TOUR — 코드베이스 한 바퀴

본 폴더 외부에서 다음 에이전트가 “읽기/수정해도 되는 곳”과 “건드리면 안 되는 곳”을 한 장에 정리한다. 절대경로는 모두 워크스페이스 루트(`c:\Users\6sieg\OneDrive\바탕 화면\hongikUniv.-26_1\`) 기준 상대.

---

## 1. 워크스페이스 트리 (관계된 부분만)

```
.
├── _framework/                   ← 본 폴더 (다음 에이전트 진입점)
├── .cursor/
│   └── rules/
│       ├── lecture_inventory_agent.mdc   ← 정책 SSOT (필독)
│       ├── 26_1_agent.mdc                ← 전역 에이전트 룰
│       ├── 26_1_git_workflow.mdc
│       ├── 26_1_dataScience_lecture_inventory.mdc
│       ├── 26_1_*_*강_context.mdc        ← 강별 보조 컨텍스트
│       └── 26_1_statistics_style.mdc
├── docs.js                       ← md → DOCX 변환기 (인벤토리 파생 지원)
├── package.json                  ← npm scripts: docx, docx:inventory, docx:rag, docx:inventory+patterns, docx:raw-develop-flat
├── dataScience/                  ← 과목 폴더 (참조 표준)
│   ├── 20260312_1강_강의록.txt   ← 내용 SSOT (불변)
│   ├── 20260312_1-2강.md         ← 구조 SSOT (불변)
│   ├── ...
│   └── _inventory/
│       ├── DS_global_patterns.md
│       ├── prompt_template_lecture_rag_md.md
│       ├── prompt_template_lecture_raw_develop.md
│       ├── rebuild_annotated_transcript.py
│       ├── 20260312_1/  (sidecar 한 강 세트)
│       ├── 20260312_2/  ...
│       ├── 20260319_3/
│       ├── 20260326_4/
│       ├── 20260402_5/
│       └── 20260409_6/
├── statistics/                   ← (sidecar 미생성 — 후보)
├── ML/                           ← (sidecar 미생성 — 후보)
├── mathematics/                  ← (sidecar 미생성 — 후보)
├── decisionMaking/               ← (sidecar 미생성 — 후보)
└── docx-export/
    └── dataScience/
        ├── *.docx                ← 강의 md 본체 docx
        ├── _inventory-derived/<id>/*.docx     ← 인벤토리 파생 docx
        └── _inventory-raw-develop-flat/*.docx ← 로데이터 디벨롭 한곳 모음
```

---

## 2. 읽기 전용(Read-only) — **절대 수정 금지**

| 경로 | 이유 |
|------|------|
| `<course>/{YYYYMMDD}_{N}강_강의록.txt` (또는 `.txt.txt`) | 내용 SSOT (불변) |
| `<course>/{YYYYMMDD}_{N}강.md` | 구조 SSOT (단, 정책 §8.2 “insert-only” 패턴 A 인용 박스만 예외) |
| `<course>/{YYYYMMDD}_{N}강.docx` | 슬라이드 SSOT (불변) |
| `<course>/_inventory/<id>/raw/` | 무표기 미러 (불변) |
| `<course>/_inventory/<id>/{*_annotated_transcript.txt}` | 마커 박힌 사본 — **마커 줄만 추가**, 원본 줄 텍스트 변경 금지 |
| `.cursor/rules/*.mdc` | 정책 SSOT (룰 변경은 사람만) |

---

## 3. 작성·갱신 가능 — sidecar / 파생 md / 검증 산출

| 경로 | 어떻게 만들어지나 |
|------|-------------------|
| `<course>/_inventory/<id>/manifest.json` | 단계 01 부트스트랩 |
| `<course>/_inventory/<id>/anchors_md.json` (`anchors_docx.json`) | 단계 01 (구조 추출) |
| `<course>/_inventory/<id>/segments.jsonl` | 단계 02 (전사 정렬) |
| `<course>/_inventory/<id>/alignments.jsonl` | 단계 02 |
| `<course>/_inventory/<id>/evidence.jsonl` | 단계 02 |
| `<course>/_inventory/<id>/nodes.json` | 단계 01 (segment_ids 는 02 끝나고 채워도 됨) |
| `<course>/_inventory/<id>/edges.json` | 단계 01 (cross-lecture 는 검증 후) |
| `<course>/_inventory/<id>/conflicts_and_uncertainty.md` | 전 단계, 보류 사항 누적 |
| `<course>/_inventory/<id>/README_inventory.md` | 단계 05 (선택) |
| `<course>/_inventory/<id>/{YYYYMMDD}_{N}강_래그.md` | 단계 03 |
| `<course>/_inventory/<id>/{YYYYMMDD}_{N}강_로데이터디벨롭.md` | 단계 04 (선택) |
| `<course>/_inventory/<id>/{YYYYMMDD}_{N}강_인용보강.md` | 단계 04 변형 (선택) |
| `docx-export/<course>/_inventory-derived/<id>/*.docx` | `node docs.js --inventory-derived-only` |

---

## 4. `docs.js` — 무엇을 하는가

루트의 단일 파일(`docs.js`, 의존성: `docx@^9.6.1`).

**변환 대상:**

1. 각 과목 강의 md (`<course>/{YYYYMMDD}_{N}강.md`) → `docx-export/<course>/{같은 이름}.docx`
2. `dataScience/_inventory/<id>/` 직계의 파생 md
   - `*_래그.md` → `_inventory-derived/<id>/*.docx`
   - `*_인용보강.md` → 동상
   - `*_로데이터디벨롭.md` → 동상
   - `conflicts_and_uncertainty.md` → 동상
   - `README_inventory.md` → 동상

**스캔 규칙(중요):**

- `_inventory` 강 폴더 직계 `.md` 만 스캔. `raw/`·`_skeleton/` 하위는 **무시**.
- 파일명 선두 `YYYYMMDD` 가 있으면 표지 날짜로 사용, 없으면 빈 문자열.
- `*_래그.md` / `*_인용보강.md` / `*_로데이터디벨롭.md` 는 **용어집 부록 자동 생략**(파생 문서이므로).

**현재 한정 사항:** `dataScience/_inventory` 만 스캔한다. 다른 과목까지 확장하려면 `INVENTORY_LECTURE_DIR_RE` 적용 위치를 늘려야 함 ([`COURSE_OVERRIDES.md`](./COURSE_OVERRIDES.md) §7).

---

## 5. `package.json` 스크립트

```json
"scripts": {
  "docx": "node docs.js",
  "docx:inventory": "node docs.js --inventory-derived-only",
  "docx:rag": "node docs.js --rag-only",
  "docx:inventory+patterns": "node docs.js --inventory-derived-only --inventory-root",
  "docx:raw-develop-flat": "node docs.js --inventory-raw-develop-flat"
}
```

스크립트 의미는 [`HOW_TO_RUN.md`](./HOW_TO_RUN.md) §1.

---

## 6. 외부 의존성

- **node**: `docs.js` 실행에 필요. `npm install` 한 번 후 `docx` 모듈만 들어가면 됨.
- **OS:** Cursor(Windows)에서 편집, 실행은 Windows PowerShell 또는 WSL 둘 다 가능. (사용자 룰: GCP/Docker/Java/Python/GPU는 WSL 전용. 그러나 본 작업은 노드뿐이라 PowerShell도 OK.)

---

## 7. 의도적으로 본 패키지가 다루지 않는 영역

- 벡터 DB·RAG 서버·세션 인프라(Redis 등) 구축 — 본 폴더는 **콘텐츠/지식 레이어** 까지.
- 강의 슬라이드 OCR·전사 자동 생성 — 입력은 이미 준비된 txt/md 가정.
- 학습자 진도·퀴즈 결과 등 운영 데이터.

이들은 별도 프로젝트(예: FastAPI + GCP + Neo4j) 단계에서 다룬다.
