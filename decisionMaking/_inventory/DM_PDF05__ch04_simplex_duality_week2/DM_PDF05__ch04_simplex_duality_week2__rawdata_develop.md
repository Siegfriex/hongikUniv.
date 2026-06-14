# DM_PDF05 — Ch.4 심플렉스, Big-M, 쌍대성 연결 로데이터 디벨롭

## Policy

- PDF 원본과 full transcript는 수정하지 않는다.
- 이 문서는 PDF transcript와 sidecar를 바탕으로 만든 derived learning view다.
- 날짜 추정은 폐기한다. `DM_PDFxx` 순서가 작업 순서다.

## 현재 그래프 위치

- 지금 보는 노드: Ch.4 심플렉스, Big-M, 쌍대성 연결
- 선행 노드: surplus/artificial variable, two-phase method, min-to-max conversion
- 후속 노드: dual problem, complementary slackness, sensitivity report
- 동형/유사 노드: 2단계법과 Big-M의 같은 목적, 다른 구현
- 연결 예제: 식단문제 min, 인위변수 r1/r2, Big-M penalty

## 원자료 핵심 전개

인위변수는 심플렉스 출발을 위한 임시 장치이고, Big-M/2단계법은 그 임시 장치를 목적함수에서 제거하도록 설계된다.

이 PDF는 기존 1~7강 마크다운 흐름에서 고립된 보충자료가 아니라, LP 모형화와 Solver, 심플렉스, 쌍대/민감도, 정수/네트워크/비선형 확장 사이의 연결을 만드는 원자료다.

## 핵심 노드 디벨롭

## n_DM_PDF05.artificial_variable — 인위변수 (artificial variable)

**한 줄 정의:** 초기 기저가능해를 만들기 위해 등식에 임시로 추가하는 변수다.

**쉬운 직관:** 실제 문제에는 없는 보조 바퀴다. 출발할 때만 필요하고 최종해에서는 0이어야 한다.

**수식 또는 모형 형태:** >= 또는 = 제약에서 slack basis가 없을 때 +r_i를 추가해 basis를 만든다.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 식단문제의 영양 최소 요구량 제약은 surplus를 빼면 초기 RHS basis가 바로 만들어지지 않아 r_i가 필요하다. |
| 수식 언어 | row: a_i x - s_i + r_i = b_i, r_i >= 0, and final r_i must be 0. |
| 스프레드시트/타블로 언어 | 타블로에서는 r_i가 초기 기저변수가 되고, Phase I/Big-M에서 제거 대상이 된다. |

**강의 속 실제 예제 연결:** DM_PDF05는 r1, r2를 도입하고 r1=0, r2=0 조건이 원문제와 동치임을 묻는다.

**자주 하는 실수:** 인위변수를 실제 의사결정 변수로 해석하면 안 된다. 최종해에 남으면 원문제가 infeasible일 수 있다.

**연결 관계**

- 선행 노드: surplus variable
- 후속 노드: Big-M and Phase I
- 동형/유사 노드: slack variable과의 대비

**근거:** `ev_DM_PDF05_001` -> `DM_PDF05:p003:L009`

> 인위변수(artificial variable) r1, r2 을 도입함

## n_DM_PDF05.big_m_method — Big-M 방법 (Big-M method)

**한 줄 정의:** 인위변수가 최종해에 남지 않도록 목적함수에 매우 큰 벌점을 주는 심플렉스 변형이다.

**쉬운 직관:** 임시 변수를 쓰되, 최적화가 그 변수를 극도로 싫어하게 만드는 방식이다.

**수식 또는 모형 형태:** max 문제에서는 artificial variable에 -M penalty, min 또는 변환식에서는 부호를 일관되게 조정한다.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 식단 min을 max -Z로 바꾸고 인위변수에 M 벌점을 붙여 원문제 feasible 해를 강제한다. |
| 수식 언어 | objective row includes +/- M r_i; tableau algebra must remove artificial basis coefficients. |
| 스프레드시트/타블로 언어 | 타블로에서는 M이 포함된 목적행을 계산하므로 부호 실수가 치명적이다. |

**강의 속 실제 예제 연결:** DM_PDF05는 Big penalty의 부호 주의를 명시한다.

**자주 하는 실수:** M을 실제 큰 숫자로만 생각하면 수치 불안정과 부호 오류를 놓친다. 핵심은 lexicographic penalty다.

**연결 관계**

- 선행 노드: artificial variable
- 후속 노드: dual problem and sensitivity
- 동형/유사 노드: two-phase method

**근거:** `ev_DM_PDF05_002` -> `DM_PDF05:p003:L016`

> 따라서 목적함수 식에 Big M을 도입하였음. Big penalty (부호주위)

## n_DM_PDF05.min_to_max_conversion — 최소화-최대화 변환 (min-to-max conversion)

**한 줄 정의:** 최소화 문제의 목적함수에 -1을 곱해 최대화 문제로 바꾸는 표현 변환이다.

**쉬운 직관:** 같은 선호를 반대 부호의 산으로 바꿔 심플렉스 규칙을 맞추는 것이다.

**수식 또는 모형 형태:** min Z = c^T x is equivalent to max -Z = -c^T x.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 식단 비용 최소화는 -비용 최대화로 바꿔 max용 타블로 규칙을 적용할 수 있다. |
| 수식 언어 | objective row changes sign; feasibility constraints do not disappear. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 원 목적은 min으로 둘 수 있지만 손계산 타블로에서는 부호 변환을 명확히 한다. |

**강의 속 실제 예제 연결:** DM_PDF05는 식단문제를 max -Z 형태로 바꾸는 과정을 보여준다.

**자주 하는 실수:** 목적함수 부호만 바꾸고 제약 부호나 surplus/artificial 처리를 잊는 오류가 많다.

**연결 관계**

- 선행 노드: LP objective sense
- 후속 노드: Big-M sign convention
- 동형/유사 노드: dual primal 방향 변환

**근거:** `ev_DM_PDF05_003` -> `DM_PDF05:p002:L002`

> 최소화 문제를 최대화 문제로 바꿔 풀 수 있음

## 표/수식 재구성 메모

- PDF에서 표가 한 줄로 붙어 추출된 경우, 최종 학습 문서에서는 변수, 목적함수, 제약식, RHS, 판정 기준을 분리해 읽는다.
- 타블로/스프레드시트 표는 `변수 셀 -> LHS 계산 셀 -> RHS -> 부호/도메인` 순서로 재구성한다.
- `[EXTRACTION_GAP]` 페이지는 OCR 또는 수동 전사 후보이며, 현재 RAG의 근거로 단정 사용하지 않는다.

## Source Trace

| RAG label | sidecar id | PDF transcript anchor | normalized PDF |
|---|---|---|---|
| `n_DM_PDF05.artificial_variable` | `ev_DM_PDF05_001` | `DM_PDF05:p003:L009` | `DM_PDF05_ch04_simplex_duality_week2.pdf` |
| `n_DM_PDF05.big_m_method` | `ev_DM_PDF05_002` | `DM_PDF05:p003:L016` | `DM_PDF05_ch04_simplex_duality_week2.pdf` |
| `n_DM_PDF05.min_to_max_conversion` | `ev_DM_PDF05_003` | `DM_PDF05:p002:L002` | `DM_PDF05_ch04_simplex_duality_week2.pdf` |
