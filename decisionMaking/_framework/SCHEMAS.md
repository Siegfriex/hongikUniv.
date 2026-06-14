# SCHEMAS — sidecar 파일 스키마

각 sidecar 파일의 **필수 필드·옵션 필드·예시**를 한곳에 모은 참조 문서. 신규 도구·검증 스크립트는 본 문서의 키만 의존하도록 작성한다.

> 형식 규약: `JSON` = 객체 단일, `JSONL` = 한 줄 한 레코드(`{...}\n` 반복), 들여쓰기/순서는 자유.

---

## 1. `manifest.json` (JSON)

**필수**

```json
{
  "lecture_id": "<YYYYMMDD>_<N>",
  "sources": [
    {
      "id": "transcript_ssot",
      "path": "<course>/<file>.txt",
      "role": ["content_ssot"],
      "immutable": true
    },
    {
      "id": "lecture_md_anchor",
      "path": "<course>/<file>.md",
      "role": ["structure_ssot", "anchor", "canonical_view"],
      "immutable": true
    }
  ]
}
```

**선택 필드**

- `policy_note` — 파일명 변형, P6 이중확장자 등 정책 메모 (string)
- `inventory_quality_min_bar` — Rule A/B′/D 체크리스트 객체
- `sources[].raw_mirror` — `_inventory/<id>/raw/...` 의 무표기 사본 경로
- `sources[].notes`
- 추가 source `id`: `lecture_docx_anchor`, `annotated_transcript`, `lecture_md_raw_develop_copy`, …

---

## 2. `anchors_md.json` / `anchors_docx.json` (JSON)

```json
{
  "lecture_id": "<id>",
  "structure_ssot_source": "<file>.md",
  "anchors": [
    {
      "anchor_id": "<COURSE><N>.A.<k>",
      "list_index": 1,
      "anchor_label_raw": "<원본 heading>",
      "anchor_label_canonical": "<snake_case 영문>",
      "anchor_path": ["목차", "<원본 부모 heading>"],
      "blocks": []
    }
  ]
}
```

- `blocks[]` 는 표·정의·절차 등을 별도 id로 잡을 때 사용. 각 항목 예시:
  ```json
  {"block_id": "<anchor>.B.1", "kind": "table|definition|procedure", "summary": "한 줄"}
  ```

---

## 3. `segments.jsonl` (JSONL)

한 줄 예시:

```json
{"segment_id":"DS6.A.2.local_001","section_id":"DS6.A.2","local_seq":1,"time_start":"02:26","time_end":"06:22","timecode_raw":"02:26","speaker":"참석자 1","segment_type":"lecture_core","source_line_start":27,"source_line_end":74,"text_raw":"...","normalized_candidate":null,"transcript_file":"20260409_6강_강의록.txt.txt","summary":"한 줄","topics":["전처리시간","정성","정량"]}
```

**필수:** `segment_id`, `section_id`, `local_seq`, `segment_type`, `source_line_start`, `source_line_end`, `transcript_file`

**선택:** `time_start`, `time_end`, `timecode_raw`, `speaker`, `text_raw`, `normalized_candidate`, `summary`, `topics`

**`segment_type`:** `admin` | `smalltalk` | `lecture_core` | `admin_or_other_lecture` | `case_story` | `example_only`

---

## 4. `alignments.jsonl` (JSONL)

```json
{"segment_id":"DS6.A.2.local_001","anchor_id":"DS6.A.2","anchor_path":["목차","2. 데이터 준비와 Raw Data"],"block_id":null,"role":["lecture_core"],"confidence":0.92,"evidence":{"keywords_overlap":["전처리","정성","정량"],"transcript_lines":[27,74]}}
```

**필수:** `segment_id`, `anchor_id`, `role[]`, `confidence`(0~1), `evidence`

**`role` 권장 어휘:** `lecture_core` | `admin` | `expands_example` | `filename_vs_content_mismatch` | `recording_order_differs_from_toc` | `late_delivery_in_recording` | `preview_in_crisp` | `bridge_from_7v` | `admin_or_other_lecture`

---

## 5. `nodes.json` (JSON)

```json
{
  "lecture_id": "<id>",
  "notes": "선택 — 폐기·흡수된 노드 메모",
  "nodes": [
    {
      "node_id": "n_<COURSE><N>.<snake_label>",
      "canonical_label": "<한국어 자연어 한 줄>",
      "status": "supported|supported_md_primary|supported_cross_lecture|uncertain",
      "anchor_ids": ["<anchor>"],
      "segment_ids": ["<segment_id>"],
      "cross_lecture_frame": true,
      "aliases": [],
      "notes": "선택"
    }
  ]
}
```

---

## 6. `edges.json` (JSON)

```json
{
  "lecture_id": "<id>",
  "edges": [
    {
      "edge_id": "e_<…>",
      "type": "prerequisite|leads_to|elaborates|extends|applies_to|contrasts_with|commonly_confused_with|evidenced_by|grounded_by|anchored_by|part_of",
      "from": "n_<…>",
      "to": "n_<…>",
      "status": "supported|supported_cross_lecture|uncertain",
      "notes": "한 줄"
    }
  ]
}
```

**금지:** `from`/`to` 의 강 접두사가 가리키는 강의 `nodes.json` 에 없는 노드(고스트 id).

---

## 7. `evidence.jsonl` (JSONL)

```json
{"evidence_id":"ev_20260409_6_001","node_id":"n_DS6.raw_data_preparation_time","source_kind":"transcript","ref":{"file":"20260409_6강_강의록.txt.txt","lines":[28,28],"segment_id":"DS6.A.2.local_001"},"quote":"<원문 그대로 짧게>","confidence":"high"}
```

**필수:** `evidence_id`, `node_id`, `source_kind`, `ref{file,lines}`, `quote`, `confidence`

**`source_kind`:** `transcript` | `lecture_md_anchor` | `lecture_docx_anchor` | `web_grounding`

**`confidence`:** `high` | `medium` | `low`

**규칙(Rule D):** 한 evidence 는 **단일 소스**. 다른 소스 문장을 합쳐 한 인용처럼 쓰지 않는다.

---

## 8. `conflicts_and_uncertainty.md` (Markdown)

자유 형식이지만 다음 절을 권장:

```markdown
# <lecture_id> conflicts / 불확실성

## 1. 전사 vs md 충돌
- (`segment_id` ↔ `anchor_id`) 한 줄 요지

## 2. 노드/엣지 보류
- `n_<…>`: <보류 사유, 근거 없음 메모>

## 3. 정책(Rule A/B′/D) 위반·예외
- `Rule A`: L=<…>, G=<…>, 판정: <…>

## 4. 외부 자료 의존(grounded_by) 항목
```

---

## 9. `*_annotated_transcript.txt` (Plain Text)

- 원본 전사 줄 텍스트 그대로 + 마커.
- 마커 형식 (정규식 친화):
  - `[[SEG:<segment_id>]]`
  - `[[NODE:<node_id>]]`
  - `[[EVID:<evidence_id>]]`
  - `[[LINES:<start>-<end>]]` (선택)
- 줄 번호는 원본 전사 기준. 마커 줄을 새로 추가해도 원본 줄을 **삭제·재배치하지 않는다**.

---

## 10. 파생 md (`*_래그.md` / `*_로데이터디벨롭.md` / `*_인용보강.md`)

### 10.1 `*_래그.md` (RAG 인덱스)

- 파일 상단 메타 키 (순서 고정):
  1. `# <강 식별 제목> 개념 노드 인덱스 (RAG / Perplexity Spaces용)`
  2. `**lecture_id:** \`…\``
  3. `**sidecar 파일명:** \`…\``
  4. `**용도:**` 한 단락
  5. `**검색 팁:**` 한 단락
- 본문 블록:
  - (선택) Prelecture/admin 블록 — `## <segment_id> — prelecture`
  - 노드 블록 — `## <node_id> — <짧은 한글 라벨>` + 불릿(`anchor_ids`/`segment_ids`/`aliases`/`status`/`간선`) + `### 증거`
- 부록(고정 2개):
  - `## 부록: <강> 내부 노드 순서 (leads_to)`
  - `## 부록: 마커가 박힌 전사 사본`
- **id 무결성:** 본 md에 등장한 모든 id는 sidecar에 실재해야 함.

### 10.2 `*_로데이터디벨롭.md`

- 헤더: `# <강> — 로데이터 디벨롭`
- 정책 박스(`policy_note` 요지 한 단락) + “SSOT 원본 미수정” 명시
- 본문은 §8.2 패턴 A 인용 + 메타 마커 **insert-only**.
- 줄 번호 정본은 “루트 md 기준” / “raw 미러 기준” 중 하나로 고정해 박스에 표기.

### 10.3 `*_인용보강.md`

- 5강 사례. `*_로데이터디벨롭.md` 의 축소판 — 새 본문 없이 인용 박스만 추가.

---

## 11. (선택) `web_grounding.jsonl`

용어가 SSOT에서 모호할 때만 사용.

```json
{"grounding_id":"wg_<…>","node_id":"n_<…>","source":"<URL or 책 ISBN>","quote":"<원문>","retrieved_at":"YYYY-MM-DD","confidence":"medium"}
```

`edges.type = grounded_by` 와 함께 사용한다.
