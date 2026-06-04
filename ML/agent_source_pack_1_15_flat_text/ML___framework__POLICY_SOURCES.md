# POLICY_SOURCES — 어디의 룰을 따라야 하는가

본 폴더는 정책을 **일반화한 운영 문서**다. 정책의 1차 정의소(SSOT)는 `.cursor/rules/` 안에 있다. 본 폴더와 룰이 충돌하면 룰이 우선한다.

---

## 1. 정책 SSOT (필수 — 작업 전 1회 통독)

| 룰 파일 | 범위 | 내용 요지 |
|---------|------|-----------|
| `.cursor/rules/lecture_inventory_agent.mdc` | dataScience(글로벌) | §0 이중 SSOT, §1 파일 역할/불변, §2 evidence-first, §3 데이터 모델, §4 전사·md 처리, §5 파이프라인, §6 1~6강 적용, §7 Rule A/B′/cross/D + 강별 상태표, §8 로데이터 디벨롭(annotated 마커, insert-only) |
| `.cursor/rules/26_1_dataScience_lecture_inventory.mdc` | dataScience 26-1 한정 | 학기별 보강 (있을 때) |
| `.cursor/rules/26_1_agent.mdc` | 전역 | 전체 에이전트 규칙 |
| `.cursor/rules/26_1_git_workflow.mdc` | 전역 | git 워크플로우 |

> **에이전트 규칙:** 위 4개 중 본 작업에 관련된 것은 **`lecture_inventory_agent.mdc`** 뿐이다. 다른 두 mdc는 본 패키지의 §0~§8 일반화 안에 이미 포함된 항목 외에는 추가 행동을 요구하지 않는다.

**정책 우선순위 (충돌 시):**

```
.cursor/rules/lecture_inventory_agent.mdc  >  _framework/*.md  >  prompts/*.md
```

---

## 2. 과목별 정책 보강 (있는 만큼만)

각 과목 폴더 아래에 “과목 전역 패턴” md 가 있으면 그 안의 표가 정책 매개변수다.

| 과목 | 보강 md | 핵심 내용 |
|------|---------|-----------|
| dataScience | `dataScience/_inventory/DS_global_patterns.md` | P1–P7 패턴, 노드/엣지 반복 구조, Rule A 허용 구간 표 |
| statistics | (없음 — 신규 시 `statistics/_inventory/STAT_global_patterns.md` 생성) | — |
| ML | (없음) | — |
| mathematics | (없음) | — |
| decisionMaking | (없음) | — |

**없는 과목**을 처음 다루면 [`COURSE_OVERRIDES.md`](./COURSE_OVERRIDES.md) §3 양식대로 보강 md 를 먼저 만들고 시작한다.

---

## 3. 컨텍스트 룰 (강별)

`.cursor/rules/26_1_*_*강_context.mdc` 는 **특정 강 한정 보조 컨텍스트**다. 본 작업과 직접 충돌하면 본 패키지·정책 SSOT 가 우선한다.

| 파일 | 범위 |
|------|------|
| `.cursor/rules/26_1_ML_3강_context.mdc` | ML 3강 |
| `.cursor/rules/26_1_ML_4강_context.mdc` | ML 4강 |
| `.cursor/rules/26_1_dataScience_4강_context.mdc` | DS 4강 |
| `.cursor/rules/26_1_dataScience_5강_context.mdc` | DS 5강 |
| `.cursor/rules/26_1_statistics_3강_context.mdc` | 통계 3강 |
| `.cursor/rules/26_1_mathematics_3강_context.mdc` | 수학 3강 |
| `.cursor/rules/26_1_statistics_style.mdc` | 통계 표기 스타일 |

---

## 4. 본 폴더(`_framework/`) 내 정책 운영 문서

| 문서 | 역할 |
|------|------|
| `README.md` | 개요·디렉터리 지도 |
| `PIPELINE.md` | 한 강 → 5단계 (체크리스트) |
| `SCHEMAS.md` | sidecar 11종 스키마·예시 |
| `CONVENTIONS.md` | 과목 코드·id·파일명 규약 |
| `COURSE_OVERRIDES.md` | 새 과목 추가 시 결정해야 할 Δ |
| `prompts/01..05` | 단계별 세션 프롬프트 |
| `skeleton/` | 비어 있는 sidecar 9종 |

---

## 5. 정책 변경 발생 시 동기화 의무

룰을 바꾸면(또는 룰이 바뀌어 있으면) 본 폴더 다음 세 곳을 같이 갱신한다.

1. `_framework/SCHEMAS.md` — 필드 추가/제거가 있으면.
2. `_framework/CONVENTIONS.md` — id 패턴·어휘가 바뀌면.
3. `_framework/PIPELINE.md` 와 `prompts/*` — 단계 추가/순서 변화가 있으면.

**원칙:** 정책 SSOT 단일성. 본 폴더가 룰을 추월해 새 어휘를 도입하지 않는다 — 도입은 룰에서 먼저, 운영은 여기서 따라온다.
