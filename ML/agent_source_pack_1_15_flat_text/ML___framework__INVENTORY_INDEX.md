# INVENTORY_INDEX — 현존 인스턴스·다음 작업 후보

본 문서는 코드베이스에서 실제로 발견된 강의 SSOT·sidecar 카탈로그다. 다음 에이전트가 “어디에 무엇이 있고, 무엇이 다음 작업 후보인지”를 한 페이지에서 보고 시작하도록 한다.

> 마지막 갱신: 2026-04. 새 강·새 과목을 추가하거나 sidecar를 완성할 때 본 표를 같이 갱신한다.

---

## 1. 과목 인덱스

| 과목 폴더 | `COURSE_PREFIX` | sidecar 트리 | 비고 |
|-----------|-----------------|--------------|------|
| `dataScience/` | `DS` | `dataScience/_inventory/` | 1~6강 sidecar 완성. 참조 표준. |
| `statistics/` | `STAT` | `statistics/_inventory/20250303_1/`, `statistics/_inventory/20250310_2/` (1·2강 sidecar 생성 — no-transcript 분기) | 1~6강 md 존재. 3강부터 Perplexity v2 배치 기반 심화(deep_dive) 예정. |
| `ML/` | `ML` | (없음) | 강의 md 6강만 존재(현재). |
| `mathematics/` | `MATH` | (없음) | 컨텍스트 룰만 존재(3강). |
| `decisionMaking/` | `DM` | (없음) | 강의 md 5·6·6강 존재(2개 6강은 4-13/4-06 별 강). |

---

## 2. dataScience — 강별 sidecar 상태 (완성)

**참조 표준 강:** `dataScience/_inventory/20260409_6/` (전 sidecar 파일 다 있음).

| `lecture_id` | 입력 SSOT | sidecar (`_inventory/<id>/`) | 파생 md |
|--------------|-----------|-------------------------------|---------|
| `20260312_1` | `dataScience/20260312_1강_강의록.txt`, `dataScience/20260312_1-2강.md` | manifest, anchors_md, segments, alignments, evidence, nodes, edges, conflicts, README_inventory | `20260312_1강_래그.md`, `20260312_1강_로데이터디벨롭.md` |
| `20260312_2` | `dataScience/20260312_1_2강_강의록.txt`, `dataScience/20260312_1-2강.md` | 동상 + `_merge_markers.py` | `20260312_2강_래그.md`, `20260312_1_2강_래그.md`, `20260312_2강_로데이터디벨롭.md` |
| `20260319_3` | `dataScience/20260319_3강_강의록.txt`, `dataScience/20260319_3강.md` | 동상 + `_build_annotated.py`, `_apply_transcript_markers.py`, `_merge_markers.py` | `20260319_3강_래그.md`, `20260319_3강_로데이터디벨롭.md` |
| `20260326_4` | `dataScience/20260326_4강_강의록.txt`, `dataScience/20260326_4강.md`, (`.docx`) | 동상 + `_skeleton/`, `_gen_raw_develop_md.py`, `_build_annotated.py` | `20260326_4강_래그.md`, `20260326_4강_로데이터디벨롭.md` |
| `20260402_5` | `dataScience/20260402_5강_강의록.txt`, `dataScience/20260402_5강.md` | 동상 | `20260402_5강_래그.md`, `20260402_5강_인용보강.md` |
| `20260409_6` | `dataScience/20260409_6강_강의록.txt.txt` (이중 확장자), `dataScience/20260409_6강.md` | 동상 | `20260409_6강_래그.md`, `20260409_6강_로데이터디벨롭.md` |

**보조 자산:**

- 과목 패턴 md: `dataScience/_inventory/DS_global_patterns.md` (P1–P7, Rule A 허용 구간 표 등)
- 프롬프트 원본: `dataScience/_inventory/prompt_template_lecture_rag_md.md`, `prompt_template_lecture_raw_develop.md` (본 폴더 `prompts/03·04` 의 데사 한정 풀버전)
- 스크립트: `dataScience/_inventory/rebuild_annotated_transcript.py`

**상태 한 줄:** 6개 강 sidecar·파생 md 완성, DOCX 내보내기까지 검증 완료(`docs.js --inventory-derived-only` → 16 파일 success).

---

## 3. 다음 작업 후보 (우선순위 제안)

| 우선 | `<course>` | `<lecture_id>` 후보 | 입력 SSOT 존재 | 비고 |
|------|------------|---------------------|----------------|------|
| 🟢 진행 | `statistics` | `20250303_1`, `20250310_2`, **`20260317_3`** | md ✓ / 전사 txt 없음 | sidecar + **심화.md 완료** (`20260317_3강_심화.md`, 15 nodes, 24 edges, 16 evidence, 19 web_grounding seed) |
| ⚪ A | `statistics` | `20260324_4`, `20260407_5`, `20260414_6` | md ✓ / 전사 txt 없음 | Perplexity v2 배치 기반 심화(deep_dive) 진행 예정 |
| ⚪ B | `ML` | `20260409_6` | md ✓ / 전사 txt — 확인 필요 | 1강 sidecar 부터 만들 수 있도록 입력 점검 |
| ⚪ C | `decisionMaking` | `20260330_5`, `20260406_6`, `20260413_6` | md ✓ / 전사 txt — 확인 필요 | 6강이 두 회차로 구성됨, 회차 표기 주의 |
| ⚪ D | `mathematics` | `20260*_3` (컨텍스트 룰 기준) | 입력 점검 필요 | 컨텍스트 룰 `26_1_mathematics_3강_context.mdc` 참조 |

**작업 전 점검(필수):**

```
<course>/{YYYYMMDD}_{N}강.md          ← 구조 SSOT
<course>/{YYYYMMDD}_{N}강_강의록.txt   ← 내용 SSOT
```

두 파일이 모두 있으면 부트스트랩 가능. **md만 있고 전사 txt가 없으면** 단계 02 (`02_transcript_alignment.prompt.md`) 가 막히므로 일단 단계 01·03 (구조 추출, RAG md 초안) 까지만 진행하고 나머지는 보류한다.

---

## 4. 새 강을 시작할 때의 표준 부트스트랩 결과 (예측)

`<course>/_inventory/<lecture_id>/` 안에 다음이 생긴다.

```
manifest.json
anchors_md.json
segments.jsonl
alignments.jsonl
evidence.jsonl
nodes.json
edges.json
conflicts_and_uncertainty.md
README_inventory.md
{YYYYMMDD}_{N}강_annotated_transcript.txt  (단계 02 통과 후)
{YYYYMMDD}_{N}강_래그.md                   (단계 03)
{YYYYMMDD}_{N}강_로데이터디벨롭.md         (단계 04, 선택)
{YYYYMMDD}_{N}강_인용보강.md               (단계 04 변형, 선택)
raw/                                       (전사·md 무표기 미러)
```

추가로 docx-export:

```
docx-export/<course>/_inventory-derived/<lecture_id>/*.docx
```

---

## 5. 본 인덱스 갱신 의무

새 강을 끝낸 에이전트는 다음 두 곳을 갱신하고 응답을 마친다.

1. 본 문서 §2 (또는 새 과목이면 §1·§2 둘 다) 표에 줄을 추가/갱신.
2. 해당 과목의 `<COURSE>_global_patterns.md` 의 Rule A 표·P-패턴 행 추가.

이 두 곳을 갱신하지 않으면 다음 에이전트가 같은 강을 중복 작업할 위험이 있다.
