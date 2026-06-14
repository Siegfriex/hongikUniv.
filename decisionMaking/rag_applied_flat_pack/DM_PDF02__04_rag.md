# DM_PDF02 — Ch.5 민감도 분석 최종 RAG 튜터 문서

**source_id:** `DM_PDF02`
**sidecar:** `decisionMaking/_inventory/DM_PDF02__ch05_sensitivity_analysis`
**용도:** 전담 1:1 경영과학 튜터가 바로 사용할 수 있는 심층 RAG 문서. 단순 요약이 아니라 개념 그래프, 수식 해석, 예제 연결, 오답 방지, 학습 코칭을 포함한다.

## 1. 한 줄 요약

민감도 분석은 최적해 하나를 끝으로 보지 않고, 자원량과 목적계수가 변할 때 같은 해석이 어디까지 유지되는지 읽는다.

## 2. 현재 그래프 위치

- 지금 보는 노드: Ch.5 민감도 분석
- 선행 노드: LP 최적해, shadow price, reduced cost, binding constraint
- 후속 노드: 수송/네트워크의 비용 변화, 정수계획에서 LP 완화의 한계
- 동형/유사 노드: 쌍대변수, Solver sensitivity report, 타블로 목적행 계수
- 연결 예제: 유모차-보행기 생산계획, 기계 시간 자원, 원료 제한

## 3. 개념 노드 지도

| node_id | 핵심 개념 | 역할 |
|---|---|---|
| `n_DM_PDF02.sensitivity_analysis` | 민감도 분석 | LP 최적해와 목적값이 계수, RHS, 자원량 변화에 어떻게 반응하는지 분석하는 절차다. |
| `n_DM_PDF02.shadow_price` | 잠재가격 | 제약 RHS를 1단위 완화했을 때 목적함수가 얼마나 개선되는지를 나타내는 한계 가치다. |
| `n_DM_PDF02.reduced_cost` | 감소비용 | 현재 0인 변수가 해에 들어오기 위해 목적계수가 얼마나 개선되어야 하는지 나타내는 값이다. |

## 4. 핵심 설명 블록

## n_DM_PDF02.sensitivity_analysis — 민감도 분석 (sensitivity analysis)

**한 줄 정의:** LP 최적해와 목적값이 계수, RHS, 자원량 변화에 어떻게 반응하는지 분석하는 절차다.

**쉬운 직관:** 해를 하나 구하고 끝내는 것이 아니라, 그 해가 얼마나 흔들림에 강한지 보는 사후 진단이다.

**수식 또는 모형 형태:** RHS 변화에 대한 목적값 변화는 허용범위 안에서 shadow price로 근사된다.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 기계 시간이 1시간 더 생기면 총이익이 얼마나 늘어나는지 묻는다. |
| 수식 언어 | Delta z = shadow price * Delta RHS, 단 허용가능 증감 범위 안에서만 해석한다. |
| 스프레드시트/타블로 언어 | Solver 민감도 보고서의 Shadow Price, Allowable Increase/Decrease 열을 읽는다. |

**강의 속 실제 예제 연결:** DM_PDF02는 유모차-보행기 product-mix 문제에서 기계 시간 변화와 자원 가치를 해석한다.

**자주 하는 실수:** shadow price를 무제한 적용하는 오류가 많다. 허용범위를 벗어나면 basis가 바뀌어 재해석해야 한다.

**연결 관계**

- 선행 노드: 최적 타블로와 binding constraint
- 후속 노드: 수송문제의 비용/공급 변화 분석
- 동형/유사 노드: 쌍대변수의 경제적 의미

**근거:** `ev_DM_PDF02_001` -> `DM_PDF02:p023:L001`

> 2.4. 민감도 분석 sensitivity analysis

## n_DM_PDF02.shadow_price — 잠재가격 (shadow price)

**한 줄 정의:** 제약 RHS를 1단위 완화했을 때 목적함수가 얼마나 개선되는지를 나타내는 한계 가치다.

**쉬운 직관:** 희소한 자원을 한 단위 더 얻는 것이 얼마만큼 가치 있는지 가격처럼 읽는 값이다.

**수식 또는 모형 형태:** binding constraint i에 대해 y_i = Delta z / Delta b_i, 허용범위 안에서 적용한다.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 기계2 시간이 부족한 경우 1시간 추가가 이익을 얼마나 올리는지 판단한다. |
| 수식 언어 | z_new = z_old + y_i * Delta b_i, if Delta b_i is within allowable range. |
| 스프레드시트/타블로 언어 | Solver 보고서에서는 Constraint 섹션의 Shadow Price로 표시된다. |

**강의 속 실제 예제 연결:** DM_PDF02의 기계별 이용가능시간은 resource allocation의 RHS이며 shadow price 해석 대상이다.

**자주 하는 실수:** nonbinding 제약의 shadow price가 보통 0인 이유를 놓치기 쉽다. 남는 자원은 한 단위 더 줘도 가치가 없다.

**연결 관계**

- 선행 노드: binding/nonbinding constraint
- 후속 노드: 쌍대 최적해
- 동형/유사 노드: 경제학의 한계가치

**근거:** `ev_DM_PDF02_002` -> `DM_PDF02:p032:L003`

> (Reduced cost=Marginal cost =수정비용=한계비용 ; Shadow price=잠재가격)

## n_DM_PDF02.reduced_cost — 감소비용 (reduced cost)

**한 줄 정의:** 현재 0인 변수가 해에 들어오기 위해 목적계수가 얼마나 개선되어야 하는지 나타내는 값이다.

**쉬운 직관:** 지금 선택되지 않은 활동이 경쟁력이 생기려면 단위 이익이나 비용이 얼마나 바뀌어야 하는지 보는 지표다.

**수식 또는 모형 형태:** max 문제에서 nonbasic variable j는 c_j - y^T a_j가 0 이하이면 현재 basis에서 들어오지 않는다.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 어떤 제품을 생산하지 않는 이유가 자원 소모 대비 이익이 부족해서인지 확인한다. |
| 수식 언어 | tableau z-row 또는 Solver Variable Cells 섹션의 Reduced Cost로 읽는다. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 변수셀 값이 0인 항목과 objective coefficient 변화 허용범위를 함께 본다. |

**강의 속 실제 예제 연결:** DM_PDF02의 product-mix 문제에서 생산하지 않는 제품/활동이 있다면 reduced cost가 그 이유를 설명한다.

**자주 하는 실수:** reduced cost를 실제 비용으로 오해하면 안 된다. 현재 basis 기준의 기회비용/개선 필요량이다.

**연결 관계**

- 선행 노드: 쌍대가격과 목적계수
- 후속 노드: 대안 최적해 판정
- 동형/유사 노드: 타블로의 목적행 계수

**근거:** `ev_DM_PDF02_003` -> `DM_PDF02:p026:L007`

> Reduced cost

## 5. 문제 풀이 코칭 흐름

1. 문제를 현실 문장으로 다시 읽는다.
2. 무엇을 결정해야 하는지 변수부터 둔다.
3. 목적함수가 비용 최소화인지, 이익 최대화인지 정한다.
4. 제약식의 RHS가 자원량, 수요량, 커버 조건, 정수 도메인 중 무엇인지 분류한다.
5. 해법을 고른다: 2변수 LP는 그래프, 일반 LP는 Solver/심플렉스, 정수조건은 IP/분지한계, 초기 BFS가 없으면 2단계법/Big-M, 비선형이면 GRG와 초기해 점검.
6. 해를 숫자로 끝내지 말고 현실 의미와 민감도 또는 구조적 의미를 해석한다.

## 6. 시험 위험 포인트

- 허용범위 밖 변화
- shadow price와 reduced cost 차이
- 기존 7강 쌍대 해석 연결

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
| `n_DM_PDF02.sensitivity_analysis` | `ev_DM_PDF02_001` | `DM_PDF02:p023:L001` | `DM_PDF02_ch05_sensitivity_analysis.pdf` |
| `n_DM_PDF02.shadow_price` | `ev_DM_PDF02_002` | `DM_PDF02:p032:L003` | `DM_PDF02_ch05_sensitivity_analysis.pdf` |
| `n_DM_PDF02.reduced_cost` | `ev_DM_PDF02_003` | `DM_PDF02:p026:L007` | `DM_PDF02_ch05_sensitivity_analysis.pdf` |

## 10. 검토 후 보강 메모

- 이 문서는 생성 후 자기검토 단계에서 누락 위험을 재점검했다.
- extraction risk pages: 11. 현재 문서의 단정은 추출된 텍스트 근거에 한정한다.
- 사용자가 학습 세션에서 `지도부터`, `노드 중심으로`, `예제 중심으로`, `문제 풀이 모드`, `완성 해설 모드`, `암기/정리 모드`를 말하면 이 RAG의 섹션을 출발점으로 삼는다.
