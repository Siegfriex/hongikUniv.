# <lecture_id> conflicts / 불확실성

> 이 파일은 `_framework/skeleton/` 의 빈 템플릿이다. 강 폴더로 복사한 뒤 `<lecture_id>` 를 실 id로 치환하고, 미사용 절은 비워두거나 삭제한다.

## 1. 전사 vs md 충돌

- (`<segment_id>` ↔ `<anchor_id>`) — <한 줄 요지·근거 메모>

## 2. 노드 / 엣지 보류 (uncertain)

- `n_<…>` — <보류 사유, 근거 부족 메모>
- `e_<…>` — <방향·타입 재분류 후보>

## 3. 정책 위반 / 예외 (Rule A / B′ / D)

- **Rule A** — `L = <…>`, `G = [<min>, <max>]`, 판정: <pass|exception|violation>
- **Rule B′** — `F_has_prelecture = <true|false>`
- **Rule D** — md-primary 노드: `<…>`

## 4. 파일명 / 인코딩 패턴 (P-시리즈)

- (P2) 단일 전사 다회 강: <…>
- (P6) 이중 확장자: <…>
- 기타: <…>

## 5. 외부 자료 의존 (`grounded_by`) 항목

- `n_<…>` — `web_grounding.jsonl` 의 `<grounding_id>` 사용
