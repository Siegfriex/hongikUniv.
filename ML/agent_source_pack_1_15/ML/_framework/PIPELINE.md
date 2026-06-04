# PIPELINE — 한 강을 만드는 5단계

`<course>/_inventory/<lecture_id>/` 한 폴더를 **0에서 RAG/DOCX까지** 가져가는 표준 파이프라인이다. 각 단계는 “입력 / 출력 / 사용 프롬프트 / 자가 검증” 네 칸으로 정의된다.

> 본 문서는 `lecture_inventory_agent.mdc` §3·§5·§7·§8 의 일반화 버전이다. 충돌 시 정책 룰이 우선한다.

---

## 0. 사전 점검

- [ ] 과목 코드 결정 (`CONVENTIONS.md` §1)
- [ ] `lecture_id` = `YYYYMMDD_N`(예: `20260409_6`)
- [ ] `<course>/{YYYYMMDD}_{N}강.md` (구조 SSOT) 존재
- [ ] `<course>/{YYYYMMDD}_{N}강_강의록.txt` (내용 SSOT) 존재
- [ ] (있으면) `<course>/{YYYYMMDD}_{N}강.docx` 등 슬라이드

---

## 1. Bootstrap — 폴더·매니페스트 골격

**목적:** sidecar 자리를 잡고, SSOT 경로를 `manifest.json`에 박는다.

| 항목 | 내용 |
|------|------|
| 입력 | 구조 SSOT md, 전사 txt 경로 |
| 출력 | `_inventory/<lecture_id>/` 디렉터리, `manifest.json`, `raw/` 미러 |
| 프롬프트 | (없음 — 수작업 또는 `bootstrap` 스크립트) |
| 자가 검증 | `manifest.sources` 의 모든 경로가 실제로 존재하는가? |

**권장 행위:**

1. `_framework/skeleton/` 의 모든 파일을 `<course>/_inventory/<lecture_id>/` 로 복사.
2. `manifest.json` 채움:
   - `lecture_id`
   - `sources[]`: `transcript_ssot`(`role: ["content_ssot"], immutable: true`), `lecture_md_anchor`(`role: ["structure_ssot","anchor","canonical_view"], immutable: true`)
   - 필요 시 `lecture_docx_anchor`
3. `raw/` 디렉터리에 전사·md를 **무표기 미러**로 복사 (편집 금지·정본은 루트 파일).

**금지:** 원본 전사·md 파일을 이 단계에서 손대는 것.

---

## 2. 구조 추출 — md/docx → anchors / nodes / edges

**목적:** 사람이 만든 정리 md의 heading·섹션·표를 **고정 격자(anchor grid)** 로 추출하고, 그 위에 개념 노드와 관계를 얹는다.

| 항목 | 내용 |
|------|------|
| 입력 | `manifest.sources` 의 `lecture_md_anchor`(+ docx) |
| 출력 | `anchors_md.json` (+ `anchors_docx.json`), `nodes.json`, `edges.json` |
| 프롬프트 | [`prompts/01_structure_extraction.prompt.md`](./prompts/01_structure_extraction.prompt.md) |
| 자가 검증 | `anchors_md.json` heading 트리가 원본 md의 `#` 순서와 1:1; `nodes.anchor_ids` 의 모든 id가 `anchors_md.json` 에 실재 |

**핵심 규약:**

- `anchor_id` 패턴: `{COURSE_PREFIX}{N}.A.{k}` (예: `DS6.A.3`).
- `anchor_label_raw` 는 원본 그대로, `anchor_label_canonical` 은 코드/그래프용 영문 통일 라벨.
- `node_id` 패턴: `n_{COURSE_PREFIX}{N}.{snake_case_label}`.
- `edges.type` 권장 어휘: `prerequisite` | `leads_to` | `elaborates` | `extends` | `applies_to` | `contrasts_with` | `commonly_confused_with` | `evidenced_by` | `grounded_by` | `anchored_by` | `part_of`.
- 모든 cross-lecture 엣지는 `from`/`to` 양쪽 강의 `nodes.json` 에 노드가 **실재**해야 함(고스트 id 금지).

---

## 3. 전사 정렬 — txt → segments / alignments / evidence

**목적:** 녹음 전사 txt를 anchor grid 위에 시간·줄 단위로 정렬하고, 각 노드의 주장에 원문 인용을 1:1로 묶는다.

| 항목 | 내용 |
|------|------|
| 입력 | 전사 txt(불변), 단계 2 산출물 |
| 출력 | `segments.jsonl`, `alignments.jsonl`, `evidence.jsonl`, `*_annotated_transcript.txt` |
| 프롬프트 | [`prompts/02_transcript_alignment.prompt.md`](./prompts/02_transcript_alignment.prompt.md) |
| 자가 검증 | (a) 모든 `evidence.ref.lines` 가 전사 줄 범위 내; (b) `alignments.anchor_id` 가 `anchors_md.json` 에 실재; (c) `segments.local_seq` 가 `section_id` 안에서 1부터 단조 증가 |

**핵심 규약:**

- `segment_id` 패턴: `{section_id}.local_{seq}`(예: `DS6.A.2.local_001`).
- `segment_type` ∈ `admin` | `smalltalk` | `lecture_core` | `admin_or_other_lecture`(타 강 본질 구간).
- `evidence.source_kind` ∈ `transcript` | `lecture_md_anchor`(필요 시 `lecture_docx_anchor`, `web_grounding`).
- **Rule D:** md에 정의가 밀집한 노드(예: 표·정의 박스)는 `lecture_md_anchor` 가 1차 evidence, transcript는 보조.
- **Rule A / B′ (회차 길이 / prelecture):** `CONVENTIONS.md` §3 참조. 위반 시 `conflicts_and_uncertainty.md` 에 기록.
- `*_annotated_transcript.txt`: **원본 전사 복사본 + 마커**(`[[SEG:…]]` `[[NODE:…]]` `[[EVID:…]]` `[[LINES:…]]`). 원본은 절대 수정 금지.

---

## 4. 파생 md — RAG 인덱스 / 로데이터 디벨롭

**목적:** 위 sidecar를 **사람·LLM이 바로 검색 가능한 한 장의 md** 로 평탄화한다. SSOT 가공이 아니라 **derived view**.

### 4-A. `*_래그.md` (RAG / Perplexity Spaces 인덱스)

| 항목 | 내용 |
|------|------|
| 입력 | 단계 3까지의 모든 sidecar |
| 출력 | `_inventory/<lecture_id>/{YYYYMMDD}_{N}강_래그.md` |
| 프롬프트 | [`prompts/03_rag_index.prompt.md`](./prompts/03_rag_index.prompt.md) |
| 자가 검증 | 본 md에 등장한 모든 `node_id`/`segment_id`/`evidence_id`/`anchor_id` 가 sidecar에 실재 |

### 4-B. `*_로데이터디벨롭.md` (선택)

| 항목 | 내용 |
|------|------|
| 입력 | 단계 3까지 + 구조 SSOT md |
| 출력 | `_inventory/<lecture_id>/{YYYYMMDD}_{N}강_로데이터디벨롭.md` |
| 프롬프트 | [`prompts/04_raw_develop.prompt.md`](./prompts/04_raw_develop.prompt.md) |
| 자가 검증 | 루트 md 본문이 손상되지 않음(insert-only); 인용은 `evidence.jsonl` 의 줄 범위와 일치 |

> 5강처럼 “인용 보강 위주”라면 파일명을 `*_인용보강.md` 로도 가능(데사 5강 사례). 같은 카테고리(`raw_develop`/`quote_enrich`)로 다룬다.

---

## 5. 검증 + DOCX 내보내기

**목적:** id 정합·고스트 id를 잡고, 결과 md를 DOCX로 묶어 배포 가능한 산출물을 만든다.

| 항목 | 내용 |
|------|------|
| 입력 | 단계 1–4 모든 산출물 |
| 출력 | (a) 검증 리포트 (콘솔/파일), (b) `docx-export/<course>/_inventory-derived/<lecture_id>/*.docx`, (c) `README_inventory.md` 갱신 |
| 프롬프트 | [`prompts/05_verify_and_export.prompt.md`](./prompts/05_verify_and_export.prompt.md) |
| 자가 검증 | 콘솔에 `fail:` 없음, `success == total` |

**검증 항목 (반드시 통과):**

1. `nodes.anchor_ids` ⊆ `anchors_md.anchor_id`
2. `nodes.segment_ids` ⊆ `segments.segment_id`
3. `edges.from`, `edges.to` 의 강 접두사가 가리키는 강의 `nodes.json` 에 실재
4. `evidence.ref.lines` 가 해당 파일 줄 범위 내
5. `*_래그.md` / `*_로데이터디벨롭.md` 에 등장한 모든 id가 sidecar에 실재 (고스트 id 0건)
6. `manifest.sources[].path` 가 실제 파일 존재

**DOCX 내보내기 (`docs.js`):**

- 강별 파생 md 전부 → `docx-export/<course>/_inventory-derived/<lecture_id>/`
  ```
  node docs.js --inventory-derived-only
  ```
- 로데이터/인용보강만 한 폴더로:
  ```
  node docs.js --inventory-raw-develop-flat
  ```

---

## 6. 한 강 종료 체크리스트

- [ ] §1 manifest 경로 모두 실재
- [ ] §2 anchors / nodes / edges 작성·교차 검증
- [ ] §3 segments / alignments / evidence 작성·교차 검증
- [ ] §3 `*_annotated_transcript.txt` 마커 적용 (원본 미수정)
- [ ] §4-A `*_래그.md` 작성
- [ ] §4-B 필요 시 `*_로데이터디벨롭.md` 또는 `*_인용보강.md`
- [ ] §5 검증 0 fail, DOCX 산출
- [ ] `conflicts_and_uncertainty.md` 에 미해소 항목 모두 기록
- [ ] `README_inventory.md` (또는 과목 README) 표 갱신
