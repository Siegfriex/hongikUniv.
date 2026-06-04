# CONVENTIONS — 과목 코드·id·파일명 규약

본 문서는 새 과목/새 강을 추가해도 sidecar·파생 md·DOCX 도구가 흔들리지 않게 하는 **이름 규약 SSOT**다. 변경 시 `lecture_inventory_agent.mdc` 와 `_framework/SCHEMAS.md` 도 같이 갱신한다.

---

## 1. 과목 코드 (`COURSE_PREFIX`)

| 과목 폴더 | `COURSE_PREFIX` | 비고 |
|-----------|-----------------|------|
| `dataScience/` | `DS` | 1·2강 통합 md는 `DS12.*` 사용 |
| `statistics/` | `STAT` |  |
| `ML/` | `ML` |  |
| `mathematics/` | `MATH` |  |
| `decisionMaking/` | `DM` |  |

**원칙:** 영문 대문자 2~4자. 새 과목 추가 시 [COURSE_OVERRIDES.md](./COURSE_OVERRIDES.md) 표를 갱신한다.

---

## 2. `lecture_id` 와 디렉터리

- `lecture_id` 패턴: `^(\d{8})_(\d+)$` — 예: `20260409_6` (2026-04-09 6강).
- 통합 강(여러 회차 한 md): 회차 중 **첫 강**의 yyyymmdd + 후미 회차 번호 (예: `20260312_2` 폴더에 1·2강 통합 md 사용).
- sidecar 폴더: `<course>/_inventory/<lecture_id>/`.

---

## 3. id 명명 규약

### 3.1 `anchor_id`

- 패턴: `{COURSE_PREFIX}{N}.A.{k}` (예: `DS6.A.3`)
- `N` = 강 회차(`lecture_id` 후미 숫자), `k` = `anchors_md.json` 의 `list_index`.
- 통합 강은 `DS12.A.{k}` 처럼 회차 묶음을 그대로 표기.

### 3.2 `block_id` (앵커 하위 표·정의 등)

- 패턴: `{anchor_id}.B.{k}` 또는 `{COURSE_PREFIX}{N}.B.{k}`
- `nodes.id`(`n_*`)와 **혼동 금지**.

### 3.3 `section_id`

- `anchor_id` 와 동일 문자열을 그대로 사용한다 (예: `DS6.A.2`).

### 3.4 `segment_id`

- 패턴: `{section_id}.local_{seq:03d}` — 예: `DS6.A.2.local_001`
- `seq` 는 **해당 `section_id` 안에서 1부터** 단조 증가.

### 3.5 `node_id`

- 패턴: `n_{COURSE_PREFIX}{N}.{snake_case_label}` — 예: `n_DS6.covariance_correlation_limits`
- `snake_case_label` 은 영문 소문자 + 숫자 + `_`. 한글·공백·하이픈 금지.

### 3.6 `edge_id`

- 패턴: `e_{COURSE_PREFIX}{N}_{from_short}_to_{to_short}` — 예: `e_DS6_cov_to_limits`
- cross-lecture 는 양쪽 접두사를 모두 표기 권장: `e_DS4_B21_to_DS6_limits`.

### 3.7 `evidence_id`

- 패턴: `ev_{LECTURE_ID}_{seq:03d}` — 예: `ev_20260409_6_001`

---

## 4. 파일명 규약

### 4.1 SSOT (수정 금지)

- 전사: `<course>/{YYYYMMDD}_{N}강_강의록.txt`
  - 이중 확장자 변형 허용: `..._강의록.txt.txt` (P6 — `manifest.policy_note`에 기록)
- 구조 md: `<course>/{YYYYMMDD}_{N}강.md`
- 슬라이드: `<course>/{YYYYMMDD}_{N}강.docx`

### 4.2 sidecar (생성·갱신 가능)

`<course>/_inventory/<lecture_id>/` 직계:

| 파일명 | 역할 |
|--------|------|
| `manifest.json` | 소스·역할·정책 |
| `anchors_md.json` (+ `anchors_docx.json`) | heading 트리 스냅샷 |
| `segments.jsonl` | 전사 세그먼트 |
| `alignments.jsonl` | segment ↔ anchor |
| `evidence.jsonl` | 인용 단위 (1:1 원문) |
| `nodes.json` | 개념 노드 |
| `edges.json` | 노드 관계 |
| `conflicts_and_uncertainty.md` | 충돌·불확실성 로그 |
| `README_inventory.md` | 강별 인벤토리 인덱스 (선택) |
| `{YYYYMMDD}_{N}강_annotated_transcript.txt` | 마커 박힌 전사 복사본 |
| `{YYYYMMDD}_{N}강_래그.md` | RAG/Spaces 인덱스 |
| `{YYYYMMDD}_{N}강_로데이터디벨롭.md` | 로데이터 디벨롭 작업본 (선택) |
| `{YYYYMMDD}_{N}강_인용보강.md` | 인용 보강만 (선택, 5강 사례) |
| `raw/` | 전사·md **무표기** 미러 (편집 금지) |

**파일명 규칙 — 강 표기:**

- `_inventory/<lecture_id>/` 안의 파생 파일은 모두 **`{YYYYMMDD}_{N}강_*`** 표기를 쓴다.
- 통합 강이라도 sidecar 내부 파일명은 **자기 강 회차** 표기로 통일한다(예: `20260312_2` 폴더에서 RAG 파일은 `20260312_2강_래그.md`).
- 단, 공식 전사 파일명이 `20260312_1_2강_강의록.txt` 처럼 통합 표기일 수 있다 — 이 경우 `manifest.policy_note` 와 `conflicts_and_uncertainty.md` 에 기록한다.

---

## 5. 정책 규칙 라벨 (Rule A / B′ / D)

`lecture_inventory_agent.mdc` §7 / `dataScience/_inventory/DS_global_patterns.md` 와 동일.

- **Rule A — 세그먼트 수 `L` vs 허용 구간 `G`:** 강별 `G = [G_min, G_max]` 표는 과목 전역 패턴 md에서 관리.
- **Rule B′ — `F_has_prelecture`:** `∃ s ∈ segments` such that `s.segment_type ∈ {"admin","admin_or_other_lecture"}`. 행정 블록 없는 강은 `false` 정상.
- **Rule D — md-primary evidence:** md에 정의가 밀집한 노드는 `lecture_md_anchor` 1차, transcript 보조. `nodes.status = "supported_md_primary"` 사용.

---

## 6. `edges.type` 권장 어휘

| type | 의미 |
|------|------|
| `prerequisite` | from을 먼저 알아야 to를 이해함 (선행 → 후속) |
| `leads_to` | 같은 강 안 흐름에서 다음 단계로 |
| `elaborates` | 같은 개념을 더 자세히 |
| `extends` | 동일 프레임을 후속 강에서 확장 |
| `applies_to` | 원리(from)를 적용 사례(to)에 |
| `contrasts_with` | 대조/대비 |
| `commonly_confused_with` | 혼동 가능 — 학습용 경고 |
| `evidenced_by` / `grounded_by` / `anchored_by` | 메타: 노드 ↔ 증거/외부근거/앵커 |
| `part_of` | 포함 관계 |

---

## 7. 강의별 README/카탈로그 갱신

새 강 1개 끝났을 때:

1. `<course>/_inventory/<lecture_id>/README_inventory.md`(있으면) 표 추가.
2. `<course>/_inventory/<COURSE>_global_patterns.md`(있으면) Rule A 표·P-패턴에 행 추가.
3. 루트 `<course>/README.md` 또는 `README_<course>_global.md` 의 강 인덱스 갱신.
4. 필요 시 `package.json` `docx:*` 스크립트 동작 확인.

---

## 8. 외래어 / 줄임말

- 산출물 본문은 한국어 우선, 영문 용어는 백틱(예: `Pearson r`).
- `nodes.canonical_label` 은 한국어 자연어 한 줄, `node_id` 의 `snake_case_label` 만 영문.
