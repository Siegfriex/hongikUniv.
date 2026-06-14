# DM_PDF03 — Ch.6 분지한계법 최종 RAG 튜터 문서

**source_id:** `DM_PDF03`
**sidecar:** `decisionMaking/_inventory/DM_PDF03__ch06_branch_and_bound`
**용도:** 전담 1:1 경영과학 튜터가 바로 사용할 수 있는 심층 RAG 문서. 단순 요약이 아니라 개념 그래프, 수식 해석, 예제 연결, 오답 방지, 학습 코칭을 포함한다.

## 1. 한 줄 요약

분지한계법은 정수조건 때문에 생긴 불연속성을 LP 완화와 가지치기로 통제하는 탐색 알고리즘이다.

## 2. 현재 그래프 위치

- 지금 보는 노드: Ch.6 분지한계법
- 선행 노드: LP relaxation, integer variable, feasible solution, upper/lower bound
- 후속 노드: 0-1 시설입지, 배낭/선택 문제, Solver integer option
- 동형/유사 노드: 심플렉스 최적값을 bound로 쓰는 트리 탐색
- 연결 예제: 이콤전자 승합차 구입 모형, x1 floor/ceil branching

## 3. 개념 노드 지도

| node_id | 핵심 개념 | 역할 |
|---|---|---|
| `n_DM_PDF03.lp_relaxation` | LP 완화 | 정수계획에서 정수 조건을 잠시 제거해 연속 LP로 푸는 완화 문제다. |
| `n_DM_PDF03.bounding_strategy` | 한계전략 | 각 부문제의 LP 완화값을 이용해 더 볼 가치가 있는지 판정하는 전략이다. |
| `n_DM_PDF03.branching_strategy` | 분지전략 | 소수 값을 가진 정수변수를 골라 floor/ceil 제약을 추가한 두 부문제로 나누는 전략이다. |

## 4. 핵심 설명 블록

## n_DM_PDF03.lp_relaxation — LP 완화 (LP relaxation)

**한 줄 정의:** 정수계획에서 정수 조건을 잠시 제거해 연속 LP로 푸는 완화 문제다.

**쉬운 직관:** 정수 격자점만 보려면 어렵기 때문에, 먼저 전체 평면/다각형에서 가장 좋은 값을 구해 한계를 잡는다.

**수식 또는 모형 형태:** IP: x_j integer. LP relaxation: x_j >= 0만 남기고 x_j integer를 제거한다.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 차량 대수는 정수여야 하지만, 완화 문제에서는 2.9대 같은 해가 나올 수 있다. |
| 수식 언어 | max IP에서 LP relaxation optimum Z는 해당 부문제의 upper bound가 된다. |
| 스프레드시트/타블로 언어 | Solver에서는 정수조건을 잠시 빼고 Simplex LP로 푼 결과와 유사하다. |

**강의 속 실제 예제 연결:** DM_PDF03은 LP완화 최적해 x1=2.90, x2=1.72에서 분지를 시작한다.

**자주 하는 실수:** LP 완화해를 반올림해 정답으로 삼는 것은 일반적으로 틀리다. 반올림해가 feasible인지도 보장되지 않는다.

**연결 관계**

- 선행 노드: LP feasible region
- 후속 노드: branching and bounding
- 동형/유사 노드: 연속 최적해와 정수 격자점

**근거:** `ev_DM_PDF03_001` -> `DM_PDF03:p001:L001`

> 분지한계법(경영과학,박구현저)여기서제시하는분지한계법(branchandboundmethod)은순수정수계획문제나혼합정수계획문제모두에적용할수있으며,정수계획문제는최대화문제라고가정한다.분지한계법은다음과같은한계전략(boundingstrategy)과분지전략(branchingstrategy)을반복적으로적용하여정수최적해를구해나간다.1.<한계전략>분지한계법은한계전략으로서변수들의정수제한조건만삭제된LP완화문제를고려한다.최대화문제의경우LP완화된문제의

## n_DM_PDF03.bounding_strategy — 한계전략 (bounding strategy)

**한 줄 정의:** 각 부문제의 LP 완화값을 이용해 더 볼 가치가 있는지 판정하는 전략이다.

**쉬운 직관:** 현재까지 찾은 정수해보다 좋을 가능성이 없으면 그 가지를 더 내려가지 않는다.

**수식 또는 모형 형태:** max 문제에서 LP relaxation Z는 upper bound, incumbent integer value L은 lower bound다.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | Z <= L이면 그 부문제의 하위 가지도 L보다 좋아질 수 없으므로 절단한다. |
| 수식 언어 | if Z <= L: prune. if integer feasible and Z > L: update L. |
| 스프레드시트/타블로 언어 | 트리 표에서는 각 노드 옆의 Z와 L 비교가 가지치기 기준이다. |

**강의 속 실제 예제 연결:** DM_PDF03은 L=-infinity에서 시작해 정수해가 발견될 때마다 L을 갱신한다.

**자주 하는 실수:** 상한과 하한 방향을 max/min에서 뒤집지 않는 실수가 많다.

**연결 관계**

- 선행 노드: LP relaxation
- 후속 노드: branch pruning
- 동형/유사 노드: 민감도 분석의 한계값 해석과는 다른 algorithmic bound

**근거:** `ev_DM_PDF03_002` -> `DM_PDF03:p001:L001`

> 분지한계법(경영과학,박구현저)여기서제시하는분지한계법(branchandboundmethod)은순수정수계획문제나혼합정수계획문제모두에적용할수있으며,정수계획문제는최대화문제라고가정한다.분지한계법은다음과같은한계전략(boundingstrategy)과분지전략(branchingstrategy)을반복적으로적용하여정수최적해를구해나간다.1.<한계전략>분지한계법은한계전략으로서변수들의정수제한조건만삭제된LP완화문제를고려한다.최대화문제의경우LP완화된문제의

## n_DM_PDF03.branching_strategy — 분지전략 (branching strategy)

**한 줄 정의:** 소수 값을 가진 정수변수를 골라 floor/ceil 제약을 추가한 두 부문제로 나누는 전략이다.

**쉬운 직관:** 2.9대는 불가능하므로 x <= 2와 x >= 3의 두 세계로 나눠 탐색한다.

**수식 또는 모형 형태:** x_k = v non-integer이면 x_k <= floor(v), x_k >= ceil(v)를 각각 추가한다.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | x1=2.90이면 x1<=2와 x1>=3 두 가지 부문제를 만든다. |
| 수식 언어 | 각 branch는 기존 제약에 새 bound constraint를 추가한 LP relaxation으로 다시 풀린다. |
| 스프레드시트/타블로 언어 | Solver의 Branch and Bound는 내부적으로 이런 분기 트리를 관리한다. |

**강의 속 실제 예제 연결:** DM_PDF03은 x1을 분지변수로 선택해 하한/상한 제약을 추가한다.

**자주 하는 실수:** ceil/floor 방향을 반대로 쓰면 원래 정수 가능 영역을 빠뜨린다.

**연결 관계**

- 선행 노드: fractional LP optimum
- 후속 노드: node selection and pruning
- 동형/유사 노드: 이진 변수의 include/exclude 분기

**근거:** `ev_DM_PDF03_003` -> `DM_PDF03:p001:L001`

> 분지한계법(경영과학,박구현저)여기서제시하는분지한계법(branchandboundmethod)은순수정수계획문제나혼합정수계획문제모두에적용할수있으며,정수계획문제는최대화문제라고가정한다.분지한계법은다음과같은한계전략(boundingstrategy)과분지전략(branchingstrategy)을반복적으로적용하여정수최적해를구해나간다.1.<한계전략>분지한계법은한계전략으로서변수들의정수제한조건만삭제된LP완화문제를고려한다.최대화문제의경우LP완화된문제의

## 5. 문제 풀이 코칭 흐름

1. 문제를 현실 문장으로 다시 읽는다.
2. 무엇을 결정해야 하는지 변수부터 둔다.
3. 목적함수가 비용 최소화인지, 이익 최대화인지 정한다.
4. 제약식의 RHS가 자원량, 수요량, 커버 조건, 정수 도메인 중 무엇인지 분류한다.
5. 해법을 고른다: 2변수 LP는 그래프, 일반 LP는 Solver/심플렉스, 정수조건은 IP/분지한계, 초기 BFS가 없으면 2단계법/Big-M, 비선형이면 GRG와 초기해 점검.
6. 해를 숫자로 끝내지 말고 현실 의미와 민감도 또는 구조적 의미를 해석한다.

## 6. 시험 위험 포인트

- LP 완화해 반올림 금지
- max 기준 L/Z 방향
- 분지 트리 추적

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
| `n_DM_PDF03.lp_relaxation` | `ev_DM_PDF03_001` | `DM_PDF03:p001:L001` | `DM_PDF03_ch06_branch_and_bound.pdf` |
| `n_DM_PDF03.bounding_strategy` | `ev_DM_PDF03_002` | `DM_PDF03:p001:L001` | `DM_PDF03_ch06_branch_and_bound.pdf` |
| `n_DM_PDF03.branching_strategy` | `ev_DM_PDF03_003` | `DM_PDF03:p001:L001` | `DM_PDF03_ch06_branch_and_bound.pdf` |

## 10. 검토 후 보강 메모

- 이 문서는 생성 후 자기검토 단계에서 누락 위험을 재점검했다.
- extraction risk pages: 0. 현재 문서의 단정은 추출된 텍스트 근거에 한정한다.
- 사용자가 학습 세션에서 `지도부터`, `노드 중심으로`, `예제 중심으로`, `문제 풀이 모드`, `완성 해설 모드`, `암기/정리 모드`를 말하면 이 RAG의 섹션을 출발점으로 삼는다.
