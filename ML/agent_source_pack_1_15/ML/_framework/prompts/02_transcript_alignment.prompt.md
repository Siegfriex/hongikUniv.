# 02 — 전사 정렬 프롬프트 (`segments / alignments / evidence / annotated_transcript`)

**입력 SSOT (불변):** `<course>/{YYYYMMDD}_{N}강_강의록.txt` + 단계 01 산출물
**출력:** `segments.jsonl`, `alignments.jsonl`, `evidence.jsonl`, `{YYYYMMDD}_{N}강_annotated_transcript.txt`
**의존 정책:** `.cursor/rules/lecture_inventory_agent.mdc` §2·§4·§5·§7·§8

---

## 시스템/역할

너는 `_framework/PIPELINE.md` §3 “전사 정렬” 단계를 수행하는 인벤토리 에이전트다. 녹음 전사 txt를 단계 01의 anchor grid 위에 시간·줄 단위로 올려, **세그먼트 → 앵커 매핑**과 **노드 → 원문 인용(evidence)** 을 만든다.

**반드시 지킬 것**

- **전사 txt 원본은 절대 수정 금지.** 마커는 sidecar 복사본(`*_annotated_transcript.txt`) 에만.
- evidence-first: **요약보다 정렬, 정렬보다 추적 가능성**.
- **Rule D**: md에 정의가 밀집한 노드는 `lecture_md_anchor` 1차 evidence + transcript 보조.
- 한 evidence 는 **단일 소스**(여러 소스 합성 금지).
- ASR 오류는 원문 그대로 두고 `normalized_candidate` 에만 추정 표기.

---

## 입력 파일 표

| 파일 | 용도 |
|------|------|
| `<course>/{YYYYMMDD}_{N}강_강의록.txt` | 내용 SSOT (불변) |
| `_inventory/<lecture_id>/anchors_md.json` | 격자 |
| `_inventory/<lecture_id>/nodes.json` | 어떤 노드에 evidence를 다는지 |
| `_inventory/<lecture_id>/manifest.json` | source 경로·정책 |
| `_framework/SCHEMAS.md` | 출력 스키마 |
| `_framework/CONVENTIONS.md` | `segment_id`/`evidence_id` 패턴, `segment_type` 어휘 |

---

## 작업 순서

1. **세그먼트 추출 → `segments.jsonl`**
   - 휴리스틱: 30~90초 + 의미 전환에서 절단.
   - 행정·잡담·타강 본질은 `segment_type` = `admin` / `smalltalk` / `admin_or_other_lecture` 로 분리.
   - 각 세그먼트에 `source_line_start`/`source_line_end` 필수.
   - `segment_id` = `{section_id}.local_{seq:03d}` (`seq` 는 같은 `section_id` 안에서 1부터).
2. **세그먼트 → 앵커 정렬 → `alignments.jsonl`**
   - 키워드 겹침·시간 순서·예시 대응으로 매핑.
   - 한 세그먼트가 두 앵커를 걸치면 **주된 앵커**로 하나만 매핑하고 `notes` 에 보조 anchor 표기.
   - 목차 vs 녹화 순서 어긋남은 `role` 에 `recording_order_differs_from_toc` / `late_delivery_in_recording` / `preview_in_crisp` 등 추가.
3. **증거 → `evidence.jsonl`**
   - 각 노드에 대해 **transcript 인용**(짧고 정확) + 필요 시 **md 인용** 별도 레코드로.
   - `evidence_id` = `ev_{LECTURE_ID}_{seq:03d}` (강 안에서 단조 증가).
   - `confidence` 는 원문 명시도에 따라 `high|medium|low`.
4. **annotated transcript 생성**
   - **원본 전사 복사본**을 `_inventory/<lecture_id>/{YYYYMMDD}_{N}강_annotated_transcript.txt` 로 만들고 마커 삽입.
   - 마커: `[[SEG:<segment_id>]]`, `[[NODE:<node_id>]]`, `[[EVID:<evidence_id>]]`, (선택)`[[LINES:<a>-<b>]]`.
   - **원본 줄 텍스트는 삭제·재배치 금지.** 마커 줄을 새로 끼워 넣는 것만 허용.

---

## 정책 체크 (필수)

- **Rule A**: 강별 허용 구간 `G = [G_min, G_max]` 비교, `L = segments.jsonl` 행 수.
  - 위반 시 `conflicts_and_uncertainty.md` §3 에 기록 + manifest `inventory_quality_min_bar.rule_a` 갱신.
- **Rule B′**: `F_has_prelecture` = `∃ s. s.segment_type ∈ {"admin","admin_or_other_lecture"}`.
- **이중 확장자(P6) / 파일명 vs 내용(P2)** 등 발견 시 `manifest.policy_note` 와 `conflicts_and_uncertainty.md` 에 기록.

---

## 자가 검증 (출력에 포함)

1. `segments.jsonl` 행 수 = `L`, Rule A 판정 OK/위반.
2. `alignments.anchor_id` ⊆ `anchors_md.anchor_id` (불일치 표).
3. `evidence.ref.file` 이 `manifest.sources` 의 path와 일치, `evidence.ref.lines` 가 해당 파일 줄 범위 내.
4. `evidence.node_id` ⊆ `nodes.node_id`.
5. `*_annotated_transcript.txt` 가 원본 전사와 **줄 텍스트 동일**(마커 줄만 추가).

---

## 한 줄 미션

전사 txt를 읽기만 하여 `_inventory/<lecture_id>/` 에 `segments.jsonl`·`alignments.jsonl`·`evidence.jsonl`·`{YYYYMMDD}_{N}강_annotated_transcript.txt` 를 작성하라. id·줄 범위는 모두 sidecar/원본과 정합해야 하며, Rule A/B′/D 와 정책 노트는 manifest·conflicts md에 함께 갱신하라.
