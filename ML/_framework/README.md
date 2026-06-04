# `_framework/` — 강의 인벤토리·RAG 구조화 공통 프레임워크

> **다음 에이전트는 [`AGENT_START_HERE.md`](./AGENT_START_HERE.md) 부터 읽어라.** 본 README 는 디렉터리 지도와 개요다.

데이터사이언스 1~6강에서 검증된 “원본 md/docx + 강의 녹음 전사 → 인벤토리 sidecar → RAG/검색 인덱스” 파이프라인을 **다른 과목·다른 학기에도 그대로 복제**하기 위한 표준 문서·템플릿 모음이다.

이 폴더는 **인스턴스가 아니라 클래스**다. 실제 산출물은 각 과목 폴더의 `_inventory/` 아래에 만든다(예: `dataScience/_inventory/20260409_6/`).

본 폴더는 **자기 완결적**이다. 다음 에이전트는 이 폴더 + `.cursor/rules/lecture_inventory_agent.mdc` + 각 과목 폴더의 SSOT 입력 외 다른 곳을 추가로 탐색할 필요가 없도록 설계됐다.

---

## 1. 어디서 왔는가 (검증된 인스턴스)

본 프레임워크는 아래 산출물에서 **귀납**한 일반화 규약이다. 새 과목 작업 중 모호한 점이 있으면 이 인스턴스를 정답지로 본다.

- 정책 SSOT: `.cursor/rules/lecture_inventory_agent.mdc` (§0~§8)
- 과목 전역 패턴: `dataScience/_inventory/DS_global_patterns.md`
- 강별 sidecar 한 세트 (참조 표준): `dataScience/_inventory/20260409_6/`
  - `manifest.json`, `anchors_md.json`, `segments.jsonl`, `alignments.jsonl`, `evidence.jsonl`, `nodes.json`, `edges.json`, `conflicts_and_uncertainty.md`, `*_annotated_transcript.txt`, `*_래그.md`, `*_로데이터디벨롭.md`
- 강별 RAG md 작성법: `dataScience/_inventory/prompt_template_lecture_rag_md.md`
- 강별 로데이터 디벨롭 작성법: `dataScience/_inventory/prompt_template_lecture_raw_develop.md`
- DOCX 변환기: 루트 `docs.js` (인벤토리 파생 md → docx)

---

## 2. 디렉터리 지도

```
_framework/
  AGENT_START_HERE.md        ← ★ 다음 에이전트 진입점 (가장 먼저)
  POLICY_SOURCES.md          ← 어디의 .cursor/rules 를 따라야 하는지
  INVENTORY_INDEX.md         ← 현존 강의·sidecar 카탈로그 + 다음 작업 후보
  CODEBASE_TOUR.md           ← docs.js / package.json / 입출력 경로
  HOW_TO_RUN.md              ← 실제 명령 (PowerShell·WSL)
  README.md                  ← 본 파일 (개요·디렉터리 지도)
  PIPELINE.md                ← 한 강을 만드는 5단계 (체크리스트)
  CONVENTIONS.md             ← 과목 코드·id·파일명 규약
  SCHEMAS.md                 ← sidecar 파일 스키마 (필드 정의)
  COURSE_OVERRIDES.md        ← 새 과목을 추가할 때 정해야 할 Δ
  prompts/
    01_structure_extraction.prompt.md    ← md/docx → anchors / nodes / edges
    02_transcript_alignment.prompt.md    ← txt → segments / alignments / evidence
    03_rag_index.prompt.md               ← *_래그.md (RAG / Spaces 인덱스)
    04_raw_develop.prompt.md             ← *_로데이터디벨롭.md (insert-only)
    05_verify_and_export.prompt.md       ← id 정합 검증 + docx 내보내기
  skeleton/
    manifest.json
    anchors_md.json
    segments.jsonl
    alignments.jsonl
    evidence.jsonl
    nodes.json
    edges.json
    conflicts_and_uncertainty.md
    README_inventory.md
```

**주의:** `_framework/skeleton/`은 빈 자리 표시(placeholder)다. 새 강을 시작할 때 `<course>/_inventory/<lecture_id>/` 로 복사해서 채운다. 빈 파일을 그대로 커밋하지 않는다.

---

## 3. 한 강을 만드는 흐름 — 한 줄

> **bootstrap → 구조 추출 → 전사 정렬 → 파생 md(RAG/raw-develop) → 검증·DOCX**

자세한 항목은 [`PIPELINE.md`](./PIPELINE.md) 참조. 단계별 프롬프트는 `prompts/01..05.*.md`를 사용한다.

---

## 4. 이 프레임워크가 보장하는 것 (와 보장하지 않는 것)

**보장하는 것**

- 원본 전사 txt·구조 SSOT md/docx는 **항상 불변**(insert-only 예외는 정책 §8.2 안에서만).
- 모든 인용·노드·세그먼트에 **id**가 붙고, 그 id는 sidecar 파일에서 1차 정의된다(고스트 id 금지).
- “정렬 → 노드 → 증거 → 파생 md → docx” 어디로 들어와도 **같은 id로 역추적 가능**.
- 강·과목이 늘어도 같은 디렉터리·파일 명명으로 도구(`docs.js` 등) 재사용.

**보장하지 않는 것**

- 자동 정확도. evidence-first 원칙상 “모르면 비워두는” 쪽이 옳고, LLM이 채워 넣는 추정은 `uncertain` 표식이 필요하다.
- 코퍼스 운영(벡터 DB, RAG 서버, 인증). 본 프레임워크는 **콘텐츠/지식 레이어**까지다. API/세션/검색 인프라는 별도 설계.

---

## 5. 새 과목·새 강을 시작하기 전 필수 입력

| 입력 | 위치 | 필수 |
|------|------|------|
| 강의 녹음 전사 txt | `<course>/{YYYYMMDD}_{N}강_강의록.txt` | ✓ |
| 구조 SSOT md (사람이 작성한 정리본) | `<course>/{YYYYMMDD}_{N}강.md` | ✓ |
| 강의 슬라이드 docx/pdf | `<course>/{YYYYMMDD}_{N}강.docx` 등 | 권장 |
| 과목 코드 (DS / STAT / ML / MATH / DM …) | [`CONVENTIONS.md`](./CONVENTIONS.md) §1 | ✓ |

---

## 6. 관련 문서 빠른 링크

**진입(다음 에이전트):**

- [AGENT_START_HERE.md](./AGENT_START_HERE.md) — 정체성·불변 원칙·5분 진입 절차
- [POLICY_SOURCES.md](./POLICY_SOURCES.md) — 어떤 `.cursor/rules` 를 따라야 하는지
- [INVENTORY_INDEX.md](./INVENTORY_INDEX.md) — 현존 강의·다음 작업 후보
- [CODEBASE_TOUR.md](./CODEBASE_TOUR.md) — 코드베이스 한 바퀴
- [HOW_TO_RUN.md](./HOW_TO_RUN.md) — 실제 명령

**작업 표준:**

- [PIPELINE.md](./PIPELINE.md) — 5단계 체크리스트
- [CONVENTIONS.md](./CONVENTIONS.md) — 과목 코드·`node_id`·`segment_id` 명명 규약
- [SCHEMAS.md](./SCHEMAS.md) — sidecar 필드 정의
- [COURSE_OVERRIDES.md](./COURSE_OVERRIDES.md) — 새 과목 추가 시 결정해야 할 Δ

**외부 SSOT:**

- 정책 룰: [`.cursor/rules/lecture_inventory_agent.mdc`](../.cursor/rules/lecture_inventory_agent.mdc)
