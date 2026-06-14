# DM_PDF05 — Ch.4 심플렉스, Big-M, 쌍대성 연결 최종 RAG 튜터 문서

**source_id:** `DM_PDF05`
**sidecar:** `decisionMaking/_inventory/DM_PDF05__ch04_simplex_duality_week2`
**용도:** 전담 1:1 경영과학 튜터가 바로 사용할 수 있는 심층 RAG 문서. 단순 요약이 아니라 개념 그래프, 수식 해석, 예제 연결, 오답 방지, 학습 코칭을 포함한다.

## 1. 한 줄 요약

인위변수는 심플렉스 출발을 위한 임시 장치이고, Big-M/2단계법은 그 임시 장치를 목적함수에서 제거하도록 설계된다.

## 2. 현재 그래프 위치

- 지금 보는 노드: Ch.4 심플렉스, Big-M, 쌍대성 연결
- 선행 노드: surplus/artificial variable, two-phase method, min-to-max conversion
- 후속 노드: dual problem, complementary slackness, sensitivity report
- 동형/유사 노드: 2단계법과 Big-M의 같은 목적, 다른 구현
- 연결 예제: 식단문제 min, 인위변수 r1/r2, Big-M penalty

## 3. 개념 노드 지도

| node_id | 핵심 개념 | 역할 |
|---|---|---|
| `n_DM_PDF05.artificial_variable` | 인위변수 | 초기 기저가능해를 만들기 위해 등식에 임시로 추가하는 변수다. |
| `n_DM_PDF05.big_m_method` | Big-M 방법 | 인위변수가 최종해에 남지 않도록 목적함수에 매우 큰 벌점을 주는 심플렉스 변형이다. |
| `n_DM_PDF05.min_to_max_conversion` | 최소화-최대화 변환 | 최소화 문제의 목적함수에 -1을 곱해 최대화 문제로 바꾸는 표현 변환이다. |

## 4. 핵심 설명 블록

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

## 5. 문제 풀이 코칭 흐름

1. 문제를 현실 문장으로 다시 읽는다.
2. 무엇을 결정해야 하는지 변수부터 둔다.
3. 목적함수가 비용 최소화인지, 이익 최대화인지 정한다.
4. 제약식의 RHS가 자원량, 수요량, 커버 조건, 정수 도메인 중 무엇인지 분류한다.
5. 해법을 고른다: 2변수 LP는 그래프, 일반 LP는 Solver/심플렉스, 정수조건은 IP/분지한계, 초기 BFS가 없으면 2단계법/Big-M, 비선형이면 GRG와 초기해 점검.
6. 해를 숫자로 끝내지 말고 현실 의미와 민감도 또는 구조적 의미를 해석한다.

## 6. 시험 위험 포인트

- Big-M 부호
- 인위변수 최종 0 조건
- 2단계법과 Big-M 비교

## 7. 확인 질문

1. 이 PDF의 중심 노드를 한 문장으로 설명하면 무엇인가?
2. 이 노드가 이전 강의의 LP 일반형 또는 심플렉스와 어떻게 연결되는가?
3. 같은 수식을 현실 언어, 수식 언어, Solver/타블로 언어로 각각 번역할 수 있는가?

## 8. 미니 과제

- 위 개념 노드 중 하나를 골라 `정의 -> 직관 -> 수식 -> 예제 -> 실수 -> 연결` 순서로 직접 6문장 설명을 작성하라.
- PDF transcript 근거 anchor 하나를 찾아 그 설명 옆에 붙여라.

## 9. Source Trace Table

| RAG label | sidecar id | PDF transcript anchor | normalized PDF |
|---|---|---|---|
| `n_DM_PDF05.artificial_variable` | `ev_DM_PDF05_001` | `DM_PDF05:p003:L009` | `DM_PDF05_ch04_simplex_duality_week2.pdf` |
| `n_DM_PDF05.big_m_method` | `ev_DM_PDF05_002` | `DM_PDF05:p003:L016` | `DM_PDF05_ch04_simplex_duality_week2.pdf` |
| `n_DM_PDF05.min_to_max_conversion` | `ev_DM_PDF05_003` | `DM_PDF05:p002:L002` | `DM_PDF05_ch04_simplex_duality_week2.pdf` |

## 10. 검토 후 보강 메모

- 이 문서는 생성 후 자기검토 단계에서 누락 위험을 재점검했다.
- extraction risk pages: 5. 현재 문서의 단정은 추출된 텍스트 근거에 한정한다.
- 사용자가 학습 세션에서 `지도부터`, `노드 중심으로`, `예제 중심으로`, `문제 풀이 모드`, `완성 해설 모드`, `암기/정리 모드`를 말하면 이 RAG의 섹션을 출발점으로 삼는다.
