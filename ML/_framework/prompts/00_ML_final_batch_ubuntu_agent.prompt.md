# ML `final_brief` / `final_record` 배치 — Ubuntu(WSL) 로컬 에이전트 마스터 프롬프트

**한 세션에 이 문서 전체 + (단계별) `01`~`05` 프롬프트 파일**을 컨텍스트에 넣고 실행한다. 정책 SSOT: `REPO_ROOT/.cursor/rules/lecture_inventory_agent.mdc` (있으면). 충돌 시 정책 룰 우선.

---

## 0. 환경·경로 (WSL만 사용)

```text
REPO_ROOT=/home/sieg/projects-wsl/hongikUniv.-26_1
FRAMEWORK=$REPO_ROOT/_framework
COURSE=ML
COURSE_PREFIX=ML
```

| 역할 | WSL 절대경로 |
|------|----------------|
| 프레임워크 | `$REPO_ROOT/_framework/` |
| **강의록 원본 (md)** | `$REPO_ROOT/ML/final_brief/*.md` |
| **전사 원본 (txt)** | `$REPO_ROOT/ML/final_record/*.txt` (폴더 안 **모든** `.txt`가 대상) |
| 인벤토리 산출 | `$REPO_ROOT/ML/_inventory/<lecture_id>/` |
| SSOT (부트스트랩 후) | `$REPO_ROOT/ML/{YYYYMMDD}_{N}강.md` · `…_강의록.txt` |
| DOCX 출력 | `$REPO_ROOT/docx-export/ML/_inventory-derived/<lecture_id>/` |

**실행:** `cd $REPO_ROOT` 후 `npm install`(1회), Python/GPU 불필요. DOCX는 `node docs.js`.

**금지:** `final_brief`·`final_record` 원본을 **직접 수정**하지 않는다(읽기·복사만). `raw/` 미러도 편집 타깃이 아니다.

---

## 1. 네가 할 일 (한 줄)

`final_brief`의 각 md와 `final_record`의 대응 전사 txt를 **`_framework/PIPELINE.md` 5단계**에 맞춰 `ML/_inventory/<lecture_id>/` sidecar + **`{YYYYMMDD}_{N}강_래그.md`**(RAG) + **`{YYYYMMDD}_{N}강_로데이터디벨롭.md`**(선택)를 만들고, 검증 후 **DOCX**까지보낸다.

---

## 2. 불변 원칙

1. 전사 txt **줄 텍스트 변경 금지** — 마커는 `*_annotated_transcript.txt` sidecar만.
2. 구조 SSOT md **본문·heading 삭제·재작성 금지** — §8.2 **insert-only**(인용 blockquote + `[[NODE]]`/`[[SEG]]`/`[[EVID]]` 추가만).
3. `node_id` / `evidence_id` / `segment_id` / `anchor_id` 는 **sidecar에서만 1차 정의** — 파생 md에 고스트 id 금지.
4. evidence **1레코드 = 1소스** (전사·md 합성 인용 금지).
5. cross-lecture `edges`는 상대 강 `nodes.json`에 **실존하는 id만**.

---

## 3. `final_*` → 프레임워크 SSOT (강마다 0단계)

각 `final_brief/YYYYMMDD.md`에 대해:

1. md **첫 줄 `# …`** 에서 **날짜**와 **`N강` 회차 숫자 `N`** 을 파싱한다. (예: `# 2026-05-14 ML 11강: …` → `N=11`)
2. `lecture_id` = `{YYYYMMDD}_{N}` (예: `20260514_11`).
3. 아래 **복사만** 수행(내용 변경 없음):

```bash
BRIEF="$REPO_ROOT/ML/final_brief/20260514.md"   # 예시
REC="$REPO_ROOT/ML/final_record/0514ml.txt"     # 페어링 표 참고
LID="20260514_11"
N=11
YMD=20260514

cp "$BRIEF" "$REPO_ROOT/ML/${YMD}_${N}강.md"
cp "$REC"   "$REPO_ROOT/ML/${YMD}_${N}강_강의록.txt"

mkdir -p "$REPO_ROOT/ML/_inventory/$LID/raw"
cp "$BRIEF" "$REPO_ROOT/ML/_inventory/$LID/raw/${YMD}_${N}강.md"
cp "$REC"   "$REPO_ROOT/ML/_inventory/$LID/raw/${YMD}_${N}강_강의록.txt"
```

4. `_framework/skeleton/` 9개 → `ML/_inventory/$LID/` 복사, 각 파일 첫 줄 `_skeleton_note` 삭제.
5. `manifest.json` 작성:
   - `lecture_id`: `$LID`
   - `transcript_ssot.path`: `ML/${YMD}_${N}강_강의록.txt`
   - `lecture_md_anchor.path`: `ML/${YMD}_${N}강.md`
   - `raw_mirror`: 위 `raw/` 경로
   - `policy_note`: 소스가 `final_brief`/`final_record`임을 1줄 기록

### 3.1 1차 페어링 표 (`_framework/plans/ML/_overview.md` 와 동일)

| brief | 전사 txt (1차) |
|-------|----------------|
| `20260430.md` | `기계학습0430.txt` |
| `20260507.md` | `기계학습0507.txt` |
| `20260514.md` | `0514ml.txt` |
| `20260521.md` | `0521Ml.txt` |
| `20260528.md` | `0528ml.txt` |
| `20260529.md` | `0529_ml.txt` (+ 보조 `0529이용오교수님.txt` → conflicts) |
| `20260604.md` | `0604ml.txt` |
| *(brief 없음)* | `0522ml.txt` → 고아; brief 확보 전까지 스킵 또는 conflicts |

**0529 2파일:** 주 전사는 `0529_ml.txt`, `0529이용오교수님.txt`는 `conflicts_and_uncertainty.md`에 보조·중복·역할 메모.

---

## 4. 파이프라인 (강 1개당 순서 고정)

| 단계 | 프롬프트 파일 | 산출 |
|------|---------------|------|
| 01 구조 추출 | `$FRAMEWORK/prompts/01_structure_extraction.prompt.md` | `anchors_md.json`, `nodes.json`, `edges.json` |
| 02 전사 정렬 | `$FRAMEWORK/prompts/02_transcript_alignment.prompt.md` | `segments.jsonl`, `alignments.jsonl`, `evidence.jsonl`, `{YMD}_{N}강_annotated_transcript.txt` |
| 03 RAG | `$FRAMEWORK/prompts/03_rag_index.prompt.md` | `{YMD}_{N}강_래그.md` |
| 04 로데이터 디벨롭 | `$FRAMEWORK/prompts/04_raw_develop.prompt.md` | `{YMD}_{N}강_로데이터디벨롭.md` |
| 05 검증·DOCX | `$FRAMEWORK/prompts/05_verify_and_export.prompt.md` | 검증 표 + DOCX |

**단계마다:** 해당 `0X` 프롬프트 **전문** + 아래 **한 줄 미션**을 세션에 넣고, 프롬프트 끝 **자가 검증 표**를 답변에 반드시 포함.

### 한 줄 미션 (치환: `<lecture_id>`, `{YMD}`, `{N}`)

- **01:** `<lecture_id>` 의 구조 SSOT md만 읽고 `anchors_md.json` / `nodes.json` / `edges.json` 을 `SCHEMAS.md`대로 작성. `COURSE_PREFIX=ML`. cross-lecture 미실재 노드는 `conflicts` 보류.
- **02:** 전사 txt 읽기만. `segments.jsonl`·`alignments.jsonl`·`evidence.jsonl`·`{YMD}_{N}강_annotated_transcript.txt` 작성. Rule A/B′/D·manifest·conflicts 갱신.
- **03:** `<lecture_id>` 인벤토리만으로 `ML/_inventory/<lecture_id>/{YMD}_{N}강_래그.md` 작성. SSOT 원본 미편집.
- **04:** 루트 md insert-only + `…/{YMD}_{N}강_로데이터디벨롭.md` 작성. evidence/segments/nodes 정합.
- **05:** 검증 1–8 표. 전부 OK면:
  ```bash
  cd $REPO_ROOT && node docs.js --inventory-derived-only --inventory-course ML
  ```
  `docx-export/ML/_inventory-derived/<lecture_id>/` 경로 보고. fail이면 `EXPORT BLOCKED`.

---

## 5. RAG 산출물 형태 (`*_래그.md`)

`_framework/prompts/03_rag_index.prompt.md` **출력 스키마**를 그대로 따른다.

- 상단: `lecture_id`, `sidecar 파일명`, 용도, 검색 팁.
- 각 `nodes.json` 노드마다 `## {node_id} — {한글 라벨}` + 고정 불릿(`anchor_ids`, `segment_ids`, `aliases`, `status`, `간선`, `### 증거`).
- `evidence.jsonl` 레코드와 **1:1** `인용:` 줄.
- 부록: `leads_to` 체인, annotated 경로.

Perplexity Spaces·로컬 RAG에 **이 파일만** 올려도 id로 역추적 가능해야 한다.

---

## 6. 배치 운영 (여러 강)

1. **한 세션 = 한 `lecture_id`** (섞지 않음).
2. 권장 순서: 날짜 오름차순 (`20260430` → … → `20260604`).
3. 강마다 `README_inventory.md` 한 줄 + `_framework/plans/ML/_overview.md` 완료 표시(선택).
4. 첫 강 시 `ML/_inventory/ML_global_patterns.md` 생성 — Rule A 표·`code_demo` segment_type (`COURSE_OVERRIDES.md` §3).

---

## 7. 첫 응답 형식 (에이전트)

1. `final_brief`·`final_record` **파일 목록** (WSL `ls`)
2. 강별 **`lecture_id`·페어링·N** 표 (H1 파싱 결과)
3. **다음 1강** 0단계 bootstrap 명령(복사 경로)
4. 0단계 완료 확인 후 **01** 진행

**지금:** 위 1–3을 출력한 뒤, 사용자가 지정한 1강(또는 표의 첫 미처리 강)부터 0단계를 실행하라.

---

## 8. 참고 읽기 순서 (`_framework`)

`AGENT_START_HERE.md` → `PIPELINE.md` → `CONVENTIONS.md` → `SCHEMAS.md` → `plans/ML/_overview.md`

완성 참조(형식만): `dataScience/_inventory/20260409_6/` (데사 6강). ML 내용을 베끼지 말 것.
