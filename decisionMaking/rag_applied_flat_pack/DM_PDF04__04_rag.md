# DM_PDF04 — Ch.6 정수계획 1주차 최종 RAG 튜터 문서

**source_id:** `DM_PDF04`
**sidecar:** `decisionMaking/_inventory/DM_PDF04__ch06_integer_programming_week1`
**용도:** 전담 1:1 경영과학 튜터가 바로 사용할 수 있는 심층 RAG 문서. 단순 요약이 아니라 개념 그래프, 수식 해석, 예제 연결, 오답 방지, 학습 코칭을 포함한다.

## 1. 한 줄 요약

정수계획은 LP의 선형 구조를 유지하되, 변수의 domain을 정수 또는 0-1로 제한해 현실적 선택을 표현한다.

## 2. 현재 그래프 위치

- 지금 보는 노드: Ch.6 정수계획 1주차
- 선행 노드: LP 모형화, decision variable, Solver variable cell/domain
- 후속 노드: 분지한계법, 시설입지, 고정비, 상호배타 선택
- 동형/유사 노드: 연속 LP와 같은 목적/제약 구조에 domain 제약이 추가된 형태
- 연결 예제: 사람 수, 기계 대수, 출장 횟수, 공장 가동 여부

## 3. 개념 노드 지도

| node_id | 핵심 개념 | 역할 |
|---|---|---|
| `n_DM_PDF04.integer_programming` | 정수계획 | 목적함수와 제약식은 선형이지만 일부 또는 모든 변수가 정수값만 가질 수 있는 최적화 모형이다. |
| `n_DM_PDF04.binary_variable` | 0-1 변수 | 어떤 선택을 하거나 하지 않는지를 1과 0으로 표현하는 변수다. |
| `n_DM_PDF04.integer_solver_option` | Solver 정수 옵션 | Excel Solver에서 변수셀의 정수/이진 제한과 해법을 지정해 정수계획을 푸는 설정이다. |

## 4. 핵심 설명 블록

## n_DM_PDF04.integer_programming — 정수계획 (integer programming)

**한 줄 정의:** 목적함수와 제약식은 선형이지만 일부 또는 모든 변수가 정수값만 가질 수 있는 최적화 모형이다.

**쉬운 직관:** 생산량은 연속일 수 있지만 사람 수, 트럭 수, 설치 여부는 2.7처럼 나눌 수 없기 때문에 domain을 제한한다.

**수식 또는 모형 형태:** min/max c^T x subject to Ax <= b, x_j integer for selected j.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 기계 대수나 출장 횟수처럼 셀 수 있는 결정을 변수로 둔다. |
| 수식 언어 | LP model + integer restrictions on selected variable cells. |
| 스프레드시트/타블로 언어 | Solver에서는 변수셀에 int 또는 bin 제한조건을 추가한다. |

**강의 속 실제 예제 연결:** DM_PDF04는 int/bin 선택과 정수 최적화 비율의 의미를 정수계획 도입부에서 다룬다.

**자주 하는 실수:** 식이 선형이면 단순 LP라고 착각하기 쉽다. 변수 domain이 정수이면 해법 난이도가 크게 달라진다.

**연결 관계**

- 선행 노드: LP 일반형
- 후속 노드: branch-and-bound
- 동형/유사 노드: 0-1 binary model

**근거:** `ev_DM_PDF04_001` -> `DM_PDF04:p001:L002`

> Integer Programming (정수계획법)

## n_DM_PDF04.binary_variable — 0-1 변수 (binary variable)

**한 줄 정의:** 어떤 선택을 하거나 하지 않는지를 1과 0으로 표현하는 변수다.

**쉬운 직관:** 수량을 묻는 변수가 아니라 스위치다. 켜면 1, 끄면 0이다.

**수식 또는 모형 형태:** x_j in {0,1}. 선택하면 1, 선택하지 않으면 0.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 공장을 열지 말지, 후보지에 시설을 설치할지, 과제를 배정할지를 표현한다. |
| 수식 언어 | Solver에서는 bin constraint로 지정한다. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 변수셀 값이 0/1이고 제약식은 이 선택들의 합이나 조건부 논리를 표현한다. |

**강의 속 실제 예제 연결:** DM_PDF04의 공장 가동 여부 예시는 binary variable의 대표 용도다.

**자주 하는 실수:** 0-1 변수에 연속 생산량 의미를 섞으면 안 된다. 필요하면 선택 변수 y와 생산량 x를 따로 둔다.

**연결 관계**

- 선행 노드: decision variable
- 후속 노드: fixed-charge model and facility location
- 동형/유사 노드: assignment problem의 행/열 0-1 구조

**근거:** `ev_DM_PDF04_002` -> `DM_PDF04:p011:L003`

> - 보물 선택여부 (변수셀) <- 2진수 (binary)

## n_DM_PDF04.integer_solver_option — Solver 정수 옵션 (integer Solver option)

**한 줄 정의:** Excel Solver에서 변수셀의 정수/이진 제한과 해법을 지정해 정수계획을 푸는 설정이다.

**쉬운 직관:** 수식 자체보다 변수 셀의 값 종류를 Solver에게 알려주는 단계다.

**수식 또는 모형 형태:** Variable cells with int/bin constraints; solving method may use branch-and-bound or evolutionary methods.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 변수셀을 bin으로 지정하면 0 또는 1만 허용된다. |
| 수식 언어 | Solver constraints include x_j = integer or x_j = binary. |
| 스프레드시트/타블로 언어 | 해찾기 옵션에서 정수 제한, 정수 최적화 비율, 해법 선택을 확인한다. |

**강의 속 실제 예제 연결:** DM_PDF04는 Excel 2010 Solver의 분지한계해법과 유전자해법을 함께 언급한다.

**자주 하는 실수:** Solver가 정수조건을 자동으로 이해한다고 생각하면 안 된다. 반드시 int/bin 제한을 넣어야 한다.

**연결 관계**

- 선행 노드: spreadsheet modeling
- 후속 노드: branch-and-bound performance
- 동형/유사 노드: LP Solver와 evolutionary Solver

**근거:** `ev_DM_PDF04_003` -> `DM_PDF04:p003:L004`

> 정수 제한 조건으로 해찾기

## 5. 문제 풀이 코칭 흐름

1. 문제를 현실 문장으로 다시 읽는다.
2. 무엇을 결정해야 하는지 변수부터 둔다.
3. 목적함수가 비용 최소화인지, 이익 최대화인지 정한다.
4. 제약식의 RHS가 자원량, 수요량, 커버 조건, 정수 도메인 중 무엇인지 분류한다.
5. 해법을 고른다: 2변수 LP는 그래프, 일반 LP는 Solver/심플렉스, 정수조건은 IP/분지한계, 초기 BFS가 없으면 2단계법/Big-M, 비선형이면 GRG와 초기해 점검.
6. 해를 숫자로 끝내지 말고 현실 의미와 민감도 또는 구조적 의미를 해석한다.

## 6. 시험 위험 포인트

- int/bin domain 구분
- 정수 최적화 비율 의미
- LP와 IP 난이도 차이

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
| `n_DM_PDF04.integer_programming` | `ev_DM_PDF04_001` | `DM_PDF04:p001:L002` | `DM_PDF04_ch06_integer_programming_week1.pdf` |
| `n_DM_PDF04.binary_variable` | `ev_DM_PDF04_002` | `DM_PDF04:p011:L003` | `DM_PDF04_ch06_integer_programming_week1.pdf` |
| `n_DM_PDF04.integer_solver_option` | `ev_DM_PDF04_003` | `DM_PDF04:p003:L004` | `DM_PDF04_ch06_integer_programming_week1.pdf` |

## 10. 검토 후 보강 메모

- 이 문서는 생성 후 자기검토 단계에서 누락 위험을 재점검했다.
- extraction risk pages: 10. 현재 문서의 단정은 추출된 텍스트 근거에 한정한다.
- 사용자가 학습 세션에서 `지도부터`, `노드 중심으로`, `예제 중심으로`, `문제 풀이 모드`, `완성 해설 모드`, `암기/정리 모드`를 말하면 이 RAG의 섹션을 출발점으로 삼는다.
