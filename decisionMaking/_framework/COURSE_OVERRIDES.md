# COURSE_OVERRIDES — 새 과목을 추가할 때 정해야 할 Δ

`_framework/` 본체는 과목 비종속이다. 새 과목(예: `statistics`, `ML`, `mathematics`, `decisionMaking`)을 인벤토리·RAG 라인에 태우려면 아래 **델타(Δ) 4가지**만 결정하면 된다.

---

## 1. 과목 코드 (`COURSE_PREFIX`)

`CONVENTIONS.md` §1 의 표에 한 줄 추가한다.

| 과목 폴더 | `COURSE_PREFIX` | 비고 |
|-----------|-----------------|------|
| `<your_course>/` | `<2~4자 영문 대문자>` | 통합 강 표기 규약(있으면 명시) |

**원칙:** 과목 줄임은 **회차 표기와 충돌하지 않게**. 예: `STAT3` 는 OK(통계 3강), `S3` 는 비권장(다른 과목과 충돌).

---

## 2. 강의 폴더 / 파일 명명 규약

거의 모든 과목은 동일하다. 예외만 정의한다.

| 항목 | 기본값 | 과목별 예외 |
|------|--------|--------------|
| 강의 md | `<course>/{YYYYMMDD}_{N}강.md` | (없으면 비움) |
| 전사 txt | `<course>/{YYYYMMDD}_{N}강_강의록.txt` | 이중 확장자 등은 `manifest.policy_note` 에 |
| sidecar 폴더 | `<course>/_inventory/<lecture_id>/` | — |
| 통합 강(여러 회차 한 md) | 첫 강 yyyymmdd + 후미 회차 (예: `20260312_2`) | 데사 1·2강이 사례 |

**decisionMaking PDF-only 예외:** `decisionMaking/pdf_sources/DM_PDF01`~`DM_PDF08`은 날짜를 추정하지 않는다. sidecar 폴더는 `decisionMaking/_inventory/DM_PDFxx__<slug>/`를 사용하고, transcript anchor는 `DM_PDFxx:pNNN:LNNN`을 사용한다.

---

## 3. 정책 매개변수 (Rule A / B′ / D)

`<course>/_inventory/<COURSE>_global_patterns.md` 를 만들어 다음 표를 둔다 (없으면 데사 양식 따라 생성).

```markdown
## Rule A 허용 구간

| lecture_id | G = [min, max] | 비고 |
|------------|----------------|------|
| <id> | [<min>, <max>] | <짧은 사유> |

## Rule B′ 예외

- <전사가 행정 블록 없이 본론 시작> 강의 list

## Rule D — md-primary 노드 후보

- <노드 종류·앵커 절>
```

**기본값:**

- Rule A: 회차당 90분 강의 기준 `G ≈ [14, 18]` (짧은 오리엔테이션 강은 별도 예외).
- Rule B′: 행정 블록 없는 강은 `false` 정상.
- Rule D: 표·정의가 밀집한 절(예: 분류 표, 공식 박스)은 md-primary.

---

## 4. 과목별 추가 어휘 (선택)

다음 어휘를 늘릴 필요가 있으면 `<course>/_inventory/<COURSE>_global_patterns.md` 에 절을 추가한다.

- **`segment_type`** 추가: 통계라면 `proof_walkthrough`, ML이라면 `code_demo` 등.
- **`alignments.role`** 추가: `formula_derivation`, `numerical_example`, `interactive_quiz` 등.
- **`edges.type`** 추가: 수학 계열은 `proves`, `assumes`, ML 계열은 `trains_on`, `evaluated_by`.

> 추가는 가능하지만, 기본 어휘(`leads_to`, `extends`, `prerequisite` 등)는 그대로 유지한다 — 도구·검증 스크립트는 기본 어휘에 의존한다.

---

## 5. (선택) 과목 룰 mdc

`/.cursor/rules/` 에 `26_<sem>_<course>_inventory.mdc` 를 만들고 본 폴더의 `_framework` 를 우선 정책으로, 본 mdc 는 “Δ만” 적는다. 예:

```markdown
---
description: "<sem> <course> 인벤토리 — _framework 위에 과목 Δ"
globs: <course>/**/*
alwaysApply: false
---

본 룰은 `_framework/README.md` 의 일반 규약을 그대로 따르고, 과목별 차이만 아래에 정의한다.

## Δ-1. COURSE_PREFIX
- `<COURSE>`

## Δ-2. Rule A 허용 구간
| lecture_id | G | 비고 |

## Δ-3. 추가 어휘
- segment_type: …
- alignments.role: …
- edges.type: …
```

---

## 6. 새 과목 부트스트랩 체크리스트

- [ ] `<course>/` 디렉터리 존재 (강의 md·전사 txt 일부 이미 들어 있음)
- [ ] 본 문서 §1 표에 과목 코드 추가
- [ ] `<course>/_inventory/` 생성, `_framework/skeleton/` 1셋 복사
- [ ] `<course>/_inventory/<COURSE>_global_patterns.md` 생성 (Rule A 표 등)
- [ ] (선택) `/.cursor/rules/26_<sem>_<course>_inventory.mdc` 생성
- [ ] `_framework/PIPELINE.md` 의 5단계로 한 강 시범 가동
- [ ] `node docs.js --inventory-derived-only` 가 정상 동작하는지 확인 (데사 출력 경로와 동일 패턴)

---

## 7. `docs.js` 와의 호환

현재 `docs.js` 의 인벤토리 파생 스캔은 **`dataScience/_inventory`** 만 본다. 과목 확장 시 다음 둘 중 한 가지로 처리한다.

1. **단일 과목으로 유지**: 다른 과목은 자체 mdc/스크립트로 관리하고 docs.js 는 dataScience 만 다룸.
2. **다과목으로 확장**: `docs.js` 의 `INVENTORY_LECTURE_DIR_RE` 가 적용되는 코스 목록에 `<course>/_inventory` 를 추가. 이 변경은 `_framework/PIPELINE.md` §5 EXPORT 단계와 함께 수행.

> 어느 쪽이든 sidecar 스키마·파생 md 규약(SCHEMAS §10) 은 동일하므로, 도구를 늦게 확장해도 콘텐츠 작업은 막히지 않는다.
