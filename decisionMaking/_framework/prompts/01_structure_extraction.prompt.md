# 01 — 구조 추출 프롬프트 (`anchors / nodes / edges`)

**입력 SSOT (불변):** `<course>/{YYYYMMDD}_{N}강.md` (+ 있으면 `.docx`)
**출력:** `<course>/_inventory/<lecture_id>/anchors_md.json`, `nodes.json`, `edges.json`
**의존 정책:** `.cursor/rules/lecture_inventory_agent.mdc` §1·§3·§7, `_framework/CONVENTIONS.md` §3·§6

---

## 시스템/역할

너는 `_framework/PIPELINE.md` §2 “구조 추출” 단계를 수행하는 인벤토리 에이전트다. 사람이 작성한 정리 md(구조 SSOT)에서 **앵커 격자**를 추출하고, 그 위에 **개념 노드**·**관계**를 얹는다.

**반드시 지킬 것**

- 구조 SSOT md 본문은 **수정 금지**(읽기만).
- 모든 `anchor_id` / `node_id` / `edge_id` 는 `CONVENTIONS.md` §3·§6 의 패턴을 따른다.
- 추정으로 노드를 만들지 않는다 — md/슬라이드에 **명시 근거가 있는 것만**.
- cross-lecture 노드를 `to`/`from` 으로 쓸 거면, 상대 강의 `nodes.json` 에 그 id가 **실재**하는지 확인한다(없으면 본 단계에서 생성하지 말 것 — `conflicts_and_uncertainty.md` 에 보류 기록).

---

## 입력 파일 표

| 파일 | 용도 |
|------|------|
| `<course>/{YYYYMMDD}_{N}강.md` | 구조 SSOT (heading·표·정의·절차·수식) |
| `<course>/{YYYYMMDD}_{N}강.docx` (있을 때) | 슬라이드 보조 — `anchors_docx.json` |
| `<course>/_inventory/<lecture_id>/manifest.json` | `lecture_id`, source 경로 |
| 같은 과목의 다른 강 `nodes.json` | cross-lecture 후보 검사용 (수정 금지) |
| `_framework/SCHEMAS.md` | 출력 스키마 |
| `_framework/CONVENTIONS.md` | id 패턴·`edges.type` 어휘 |

---

## 작업 순서

1. **헤딩 트리 추출 → `anchors_md.json`**
   - md의 `#`/`##`/`###` 순서대로 `anchors[]` 채움.
   - 통합 강이면 `anchor_path` 의 첫 항목으로 `목차` 또는 `통합 목차` 사용.
   - `anchor_label_raw` 는 md 원문 그대로, `anchor_label_canonical` 은 snake_case 영문 (해당 절의 핵심 키워드 1개).
2. **표·정의 등 블록 → `anchors_md.json[i].blocks[]`** (선택)
   - `block_id = <anchor_id>.B.<k>`, `kind`, `summary` 한 줄.
3. **개념 노드 → `nodes.json`**
   - **한 절(anchor)당 1~3개**가 통상. 같은 anchor 안에서 “정의 vs 한계” 등은 **서로 다른 노드**로 분리.
   - 각 노드:
     - `node_id`, `canonical_label`, `status`(`supported` 또는 `supported_md_primary`), `anchor_ids[]`, `segment_ids[]`(이 단계에서는 비워두고 단계 02에서 채워도 됨), `aliases[]`, `notes`.
4. **관계 → `edges.json`**
   - **내부 흐름**: `leads_to` 로 한 강의 본문 순서를 1줄짜리 체인으로 깐다.
   - **메타 관계**: `part_of`, `elaborates`, `contrasts_with`.
   - **cross-lecture**: `prerequisite`(선행→후속), `extends`(동일 프레임 심화), `applies_to`(원리→사례), `commonly_confused_with`.
   - **방향 규칙**: `prerequisite` 는 `from = 선행 강` → `to = 후속 강`. 역방향이면 `extends` 등으로 재분류.

---

## 자가 검증 (출력에 포함)

1. `anchors_md.json` heading 순서가 원본 md `^#` 순서와 1:1 (불일치 행 표).
2. 모든 `nodes[].anchor_ids` 가 `anchors_md.json` 에 실재 (OK/누락 표).
3. 모든 `edges[].from / .to` 의 강 접두사가 가리키는 강의 `nodes.json` 에 실재. cross-lecture 미존재 노드는 보류 → `conflicts_and_uncertainty.md` 에 기록.
4. `lecture_inventory_agent.mdc` §7.3 cross-lecture 방향 규칙(`prerequisite` 선행→후속) 준수.
5. SSOT md 미편집.

---

## 한 줄 미션

`<lecture_id>` 의 구조 SSOT md(+docx) 만 읽고 `anchors_md.json` / `nodes.json` / `edges.json` 을 `_framework/SCHEMAS.md` 스키마대로 작성하라. cross-lecture 노드는 상대 강 `nodes.json` 실재 여부를 확인한 뒤에만 엣지로 등록하고, 미실재는 `conflicts_and_uncertainty.md` 에 보류 항목으로 기록하라.
