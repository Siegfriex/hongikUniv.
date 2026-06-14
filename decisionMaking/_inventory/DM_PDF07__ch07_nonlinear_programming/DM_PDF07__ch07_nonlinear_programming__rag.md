# DM_PDF07 — Ch.7 비선형계획 최종 RAG 튜터 문서

**source_id:** `DM_PDF07`
**sidecar:** `decisionMaking/_inventory/DM_PDF07__ch07_nonlinear_programming`
**용도:** 전담 1:1 경영과학 튜터가 바로 사용할 수 있는 심층 RAG 문서. 단순 요약이 아니라 개념 그래프, 수식 해석, 예제 연결, 오답 방지, 학습 코칭을 포함한다.

## 1. 한 줄 요약

비선형계획은 현실의 곡선 관계를 표현할 수 있지만 지역 최적해와 초기해 민감성 때문에 LP보다 해석이 조심스럽다.

## 2. 현재 그래프 위치

- 지금 보는 노드: Ch.7 비선형계획
- 선행 노드: LP, convexity intuition, Solver modeling
- 후속 노드: GRG nonlinear, local/global optimum, KKT intuition
- 동형/유사 노드: LP의 직선/평면 제약과 NLP의 곡면 목적/제약 대비
- 연결 예제: 담장 길이로 직사각형 면적 최대화, Cobb-Douglas 형태, GRG Solver

## 3. 개념 노드 지도

| node_id | 핵심 개념 | 역할 |
|---|---|---|
| `n_DM_PDF07.nonlinear_programming` | 비선형계획 | 목적함수 또는 제약식 중 하나 이상이 비선형 함수인 최적화 모형이다. |
| `n_DM_PDF07.local_global_optimum` | 지역 최적해와 전체 최적해 | 지역 최적해는 주변보다 좋은 해이고, 전체 최적해는 가능한 모든 해 중 가장 좋은 해다. |
| `n_DM_PDF07.grg_solver` | GRG 비선형 해법 | Excel에서 부드러운 비선형 모형을 풀 때 사용하는 일반화 감소기울기 기반 해법이다. |

## 4. 핵심 설명 블록

## n_DM_PDF07.nonlinear_programming — 비선형계획 (nonlinear programming)

**한 줄 정의:** 목적함수 또는 제약식 중 하나 이상이 비선형 함수인 최적화 모형이다.

**쉬운 직관:** 직선으로만 표현하던 관계 대신 곡선, 곱, 제곱, 로그 같은 현실 관계를 넣는 모형이다.

**수식 또는 모형 형태:** optimize f(x) subject to g_i(x) <= b_i, where f or g_i is nonlinear.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 면적 S = X1*X2를 최대화하는 문제는 목적함수가 곱이라 비선형이다. |
| 수식 언어 | B4=B7*B8처럼 변수셀끼리 곱해지는 objective cell이 생긴다. |
| 스프레드시트/타블로 언어 | Excel Solver에서는 GRG Nonlinear 해법을 선택한다. |

**강의 속 실제 예제 연결:** DM_PDF07은 X^0.5Y^0.7, log, sin, sqrt 같은 비선형 함수와 면적 최대화 예를 든다.

**자주 하는 실수:** 제약식이 선형이어도 목적함수가 비선형이면 전체 문제는 비선형계획이다.

**연결 관계**

- 선행 노드: LP formulation
- 후속 노드: local/global optimum
- 동형/유사 노드: quadratic programming and separable programming

**근거:** `ev_DM_PDF07_001` -> `DM_PDF07:p002:L006`

> ** 해법선택 : 비선형 GRG

## n_DM_PDF07.local_global_optimum — 지역 최적해와 전체 최적해 (local and global optimum)

**한 줄 정의:** 지역 최적해는 주변보다 좋은 해이고, 전체 최적해는 가능한 모든 해 중 가장 좋은 해다.

**쉬운 직관:** 산봉우리가 여러 개 있으면 가까운 봉우리는 올랐지만 세계 최고봉은 아닐 수 있다.

**수식 또는 모형 형태:** x* is local optimum if nearby feasible points are no better; global optimum if no feasible point anywhere is better.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 초기해 (0,0)에서는 멈추지만 다른 초기해에서는 (2.5,5)가 나오는 예는 초기해 민감성을 보여준다. |
| 수식 언어 | Solver result may depend on starting variable cell values. |
| 스프레드시트/타블로 언어 | GRG Nonlinear는 지역 탐색 기반이라 여러 초기해 실험이 필요할 수 있다. |

**강의 속 실제 예제 연결:** DM_PDF07은 초기해에 따라 (0,0) 또는 (2.5,5)가 나오는 비선형계획의 어려움을 제시한다.

**자주 하는 실수:** Solver가 찾은 해를 항상 전체 최적해라고 믿으면 안 된다. 특히 비볼록 문제는 위험하다.

**연결 관계**

- 선행 노드: feasible region
- 후속 노드: multi-start and global search
- 동형/유사 노드: LP의 꼭짓점 최적성과 대비

**근거:** `ev_DM_PDF07_002` -> `DM_PDF07:p006:L004`

> (엄밀히는 지역 최적해가 되기 위한 필요조건 만족해) local optimum

## n_DM_PDF07.grg_solver — GRG 비선형 해법 (GRG nonlinear solver)

**한 줄 정의:** Excel에서 부드러운 비선형 모형을 풀 때 사용하는 일반화 감소기울기 기반 해법이다.

**쉬운 직관:** 비선형 곡면 위에서 기울기를 따라 더 나은 방향을 찾는 로컬 탐색 방식이다.

**수식 또는 모형 형태:** uses gradient information and active constraints to search for a local optimum.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 면적 최대화 스프레드시트에서 해법선택을 비선형 GRG로 둔다. |
| 수식 언어 | objective and constraint cells may contain nonlinear formulas. |
| 스프레드시트/타블로 언어 | Solver options include GRG Nonlinear and initial variable values. |

**강의 속 실제 예제 연결:** DM_PDF07은 비선형계획 스프레드시트 모형에서 해법선택: 비선형 GRG를 명시한다.

**자주 하는 실수:** GRG를 선형 Simplex LP와 혼동하면 안 된다. 선형성 가정과 최적성 보장이 다르다.

**연결 관계**

- 선행 노드: nonlinear objective
- 후속 노드: local optimum diagnostics
- 동형/유사 노드: Solver Simplex LP와 Evolutionary 해법

**근거:** `ev_DM_PDF07_003` -> `DM_PDF07:p002:L002`

> 비선형계획의 스프레드시트 모형

## 5. 문제 풀이 코칭 흐름

1. 문제를 현실 문장으로 다시 읽는다.
2. 무엇을 결정해야 하는지 변수부터 둔다.
3. 목적함수가 비용 최소화인지, 이익 최대화인지 정한다.
4. 제약식의 RHS가 자원량, 수요량, 커버 조건, 정수 도메인 중 무엇인지 분류한다.
5. 해법을 고른다: 2변수 LP는 그래프, 일반 LP는 Solver/심플렉스, 정수조건은 IP/분지한계, 초기 BFS가 없으면 2단계법/Big-M, 비선형이면 GRG와 초기해 점검.
6. 해를 숫자로 끝내지 말고 현실 의미와 민감도 또는 구조적 의미를 해석한다.

## 6. 시험 위험 포인트

- OCR 공백 페이지
- 지역/전체 최적 구분
- Solver 해법 선택

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
| `n_DM_PDF07.nonlinear_programming` | `ev_DM_PDF07_001` | `DM_PDF07:p002:L006` | `DM_PDF07_ch07_nonlinear_programming.pdf` |
| `n_DM_PDF07.local_global_optimum` | `ev_DM_PDF07_002` | `DM_PDF07:p006:L004` | `DM_PDF07_ch07_nonlinear_programming.pdf` |
| `n_DM_PDF07.grg_solver` | `ev_DM_PDF07_003` | `DM_PDF07:p002:L002` | `DM_PDF07_ch07_nonlinear_programming.pdf` |

## 10. 검토 후 보강 메모

- 이 문서는 생성 후 자기검토 단계에서 누락 위험을 재점검했다.
- extraction risk pages: 25. 현재 문서의 단정은 추출된 텍스트 근거에 한정한다.
- 사용자가 학습 세션에서 `지도부터`, `노드 중심으로`, `예제 중심으로`, `문제 풀이 모드`, `완성 해설 모드`, `암기/정리 모드`를 말하면 이 RAG의 섹션을 출발점으로 삼는다.
