# DM_PDF08 — Ch.6 정수계획 2주차: 0-1 응용 모형 최종 RAG 튜터 문서

**source_id:** `DM_PDF08`
**sidecar:** `decisionMaking/_inventory/DM_PDF08__ch06_integer_programming_week2`
**용도:** 전담 1:1 경영과학 튜터가 바로 사용할 수 있는 심층 RAG 문서. 단순 요약이 아니라 개념 그래프, 수식 해석, 예제 연결, 오답 방지, 학습 코칭을 포함한다.

## 1. 한 줄 요약

0-1 정수계획은 복잡한 선택/논리/커버 조건을 선형 제약으로 번역하는 모형화 언어다.

## 2. 현재 그래프 위치

- 지금 보는 노드: Ch.6 정수계획 2주차: 0-1 응용 모형
- 선행 노드: binary variable, integer programming, assignment structure
- 후속 노드: branch-and-bound, facility location, covering model
- 동형/유사 노드: 할당문제의 0-1 행렬, Solver bin 제약, network covering
- 연결 예제: 응급 의료 서비스 후보지, 공공 설비 입지, 행정구역 커버

## 3. 개념 노드 지도

| node_id | 핵심 개념 | 역할 |
|---|---|---|
| `n_DM_PDF08.set_covering_model` | 집합커버링 모형 | 모든 수요 구역이 적어도 하나의 선택된 시설에 의해 커버되도록 하면서 선택 수를 최소화하는 0-1 모형이다. |
| `n_DM_PDF08.facility_location` | 공공 설비 입지 선정 | 시설 설치 여부를 0-1 변수로 두고 비용, 커버, 거리, 수요 조건을 만족하는 위치를 고르는 모형군이다. |
| `n_DM_PDF08.coverage_matrix` | 도달 가능성 행렬 | 수요지 i가 후보지 j로부터 서비스 가능한지 0 또는 1로 표시한 입력 행렬이다. |

## 4. 핵심 설명 블록

## n_DM_PDF08.set_covering_model — 집합커버링 모형 (set covering model)

**한 줄 정의:** 모든 수요 구역이 적어도 하나의 선택된 시설에 의해 커버되도록 하면서 선택 수를 최소화하는 0-1 모형이다.

**쉬운 직관:** 각 지역을 덮는 후보지를 최소 개수로 고르는 문제다.

**수식 또는 모형 형태:** min sum_j x_j subject to sum_j a_ij x_j >= 1 for every demand i, x_j in {0,1}.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 13개 행정구역 모두 10분 이내 응급 서비스를 받도록 응급차량 대기 후보지를 고른다. |
| 수식 언어 | coverage rows use 0/1 matrix A and binary decision vector x. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 A_ij 행렬과 변수셀 x_j를 SUMPRODUCT해 각 구역 커버 수를 계산하고 >=1 제약을 둔다. |

**강의 속 실제 예제 연결:** DM_PDF08은 후보지역 8곳과 행정구역 13개 커버 행렬을 통해 set covering을 제시한다.

**자주 하는 실수:** 각 구역이 정확히 1개 시설에만 커버되어야 한다고 오해하기 쉽다. 커버링은 보통 적어도 1개다.

**연결 관계**

- 선행 노드: binary variable
- 후속 노드: facility location
- 동형/유사 노드: assignment row/column sum structure

**근거:** `ev_DM_PDF08_001` -> `DM_PDF08:p006:L006`

> (행정구역별: covering 수 >= 1 )

## n_DM_PDF08.facility_location — 공공 설비 입지 선정 (facility location)

**한 줄 정의:** 시설 설치 여부를 0-1 변수로 두고 비용, 커버, 거리, 수요 조건을 만족하는 위치를 고르는 모형군이다.

**쉬운 직관:** 어디에 설치하면 가장 적은 비용/시설 수로 필요한 사람들을 서비스할 수 있는지 결정한다.

**수식 또는 모형 형태:** x_j = 1 if facility j is opened; constraints link demand coverage or capacity to opened facilities.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 응급차량 대기 후보지 중 어느 곳을 설치할지 선택한다. |
| 수식 언어 | binary open variables drive coverage and assignment constraints. |
| 스프레드시트/타블로 언어 | Solver에서는 후보지 변수셀을 bin으로 지정하고 설치 수 또는 총비용을 목표셀로 둔다. |

**강의 속 실제 예제 연결:** DM_PDF08의 공공 설비 예는 시설입지의 가장 직관적인 형태다.

**자주 하는 실수:** 시설 설치 변수와 서비스 할당 변수를 구분하지 않으면 큰 모형에서 논리가 깨진다.

**연결 관계**

- 선행 노드: 0-1 variable
- 후속 노드: fixed-charge and covering constraints
- 동형/유사 노드: transportation/network service assignment

**근거:** `ev_DM_PDF08_002` -> `DM_PDF08:p002:L003`

> ① 후보지역에 공공설비 설치 여부  변수셀 (0-1 변수)

## n_DM_PDF08.coverage_matrix — 도달 가능성 행렬 (coverage matrix)

**한 줄 정의:** 수요지 i가 후보지 j로부터 서비스 가능한지 0 또는 1로 표시한 입력 행렬이다.

**쉬운 직관:** 표의 각 칸은 후보지가 그 지역을 덮는지 표시하는 지도 압축본이다.

**수식 또는 모형 형태:** a_ij = 1 if demand i is covered by facility j, else 0.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 행정구역 i에서 후보지역 j까지 10분 이내 도달되면 Aij=1이다. |
| 수식 언어 | coverage_i = sum_j a_ij x_j. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 13x8 A 행렬과 8개 변수셀을 곱해 행별 커버 수를 만든다. |

**강의 속 실제 예제 연결:** DM_PDF08은 표를 가로/세로 바꿔 13x8 행렬을 작성해야 한다고 안내한다.

**자주 하는 실수:** 표 방향을 바꾸는 과정에서 i/j 인덱스를 뒤집는 실수가 자주 난다.

**연결 관계**

- 선행 노드: set covering model
- 후속 노드: coverage constraint
- 동형/유사 노드: assignment matrix

**근거:** `ev_DM_PDF08_003` -> `DM_PDF08:p003:L002`

> 후보지에서 10분 이내 도달 가능성: 0/1행렬

## 5. 문제 풀이 코칭 흐름

1. 문제를 현실 문장으로 다시 읽는다.
2. 무엇을 결정해야 하는지 변수부터 둔다.
3. 목적함수가 비용 최소화인지, 이익 최대화인지 정한다.
4. 제약식의 RHS가 자원량, 수요량, 커버 조건, 정수 도메인 중 무엇인지 분류한다.
5. 해법을 고른다: 2변수 LP는 그래프, 일반 LP는 Solver/심플렉스, 정수조건은 IP/분지한계, 초기 BFS가 없으면 2단계법/Big-M, 비선형이면 GRG와 초기해 점검.
6. 해를 숫자로 끝내지 말고 현실 의미와 민감도 또는 구조적 의미를 해석한다.

## 6. 시험 위험 포인트

- Aij 행렬 방향
- >=1 커버 조건
- 시설 설치 변수와 커버 계산 분리

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
| `n_DM_PDF08.set_covering_model` | `ev_DM_PDF08_001` | `DM_PDF08:p006:L006` | `DM_PDF08_ch06_integer_programming_week2.pdf` |
| `n_DM_PDF08.facility_location` | `ev_DM_PDF08_002` | `DM_PDF08:p002:L003` | `DM_PDF08_ch06_integer_programming_week2.pdf` |
| `n_DM_PDF08.coverage_matrix` | `ev_DM_PDF08_003` | `DM_PDF08:p003:L002` | `DM_PDF08_ch06_integer_programming_week2.pdf` |

## 10. 검토 후 보강 메모

- 이 문서는 생성 후 자기검토 단계에서 누락 위험을 재점검했다.
- extraction risk pages: 13. 현재 문서의 단정은 추출된 텍스트 근거에 한정한다.
- 사용자가 학습 세션에서 `지도부터`, `노드 중심으로`, `예제 중심으로`, `문제 풀이 모드`, `완성 해설 모드`, `암기/정리 모드`를 말하면 이 RAG의 섹션을 출발점으로 삼는다.
