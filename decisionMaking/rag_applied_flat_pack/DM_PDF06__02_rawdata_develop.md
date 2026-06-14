# DM_PDF06 — Ch.5 수송계획과 네트워크 분석 로데이터 디벨롭

## Policy

- PDF 원본과 full transcript는 수정하지 않는다.
- 이 문서는 PDF transcript와 sidecar를 바탕으로 만든 derived learning view다.
- 날짜 추정은 폐기한다. `DM_PDFxx` 순서가 작업 순서다.

## 현재 그래프 위치

- 지금 보는 노드: Ch.5 수송계획과 네트워크 분석
- 선행 노드: LP formulation, 공급/수요 균형, assignment model
- 후속 노드: 최단경로, 최대흐름, 최소비용흐름, CPM/PERT
- 동형/유사 노드: 행렬 제약이 네트워크 보존식으로 보이는 표현 변환
- 연결 예제: Transportation, transshipment, assignment, shortest path, max flow

## 원자료 핵심 전개

수송/네트워크 문제는 LP의 변수와 제약을 노드, arc, flow balance로 재해석한 구조화된 모델이다.

이 PDF는 기존 1~7강 마크다운 흐름에서 고립된 보충자료가 아니라, LP 모형화와 Solver, 심플렉스, 쌍대/민감도, 정수/네트워크/비선형 확장 사이의 연결을 만드는 원자료다.

## 핵심 노드 디벨롭

## n_DM_PDF06.transportation_problem — 수송문제 (transportation problem)

**한 줄 정의:** 여러 공급지에서 여러 수요지로 얼마를 보낼지 결정해 총 수송비를 최소화하는 LP 특수형이다.

**쉬운 직관:** 공급은 남기지 않고 수요는 채우면서 가장 싼 경로 조합을 찾는 문제다.

**수식 또는 모형 형태:** min sum_i sum_j c_ij x_ij subject to sum_j x_ij = supply_i, sum_i x_ij = demand_j, x_ij >= 0.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 공장별 공급량과 창고별 수요량이 주어졌을 때 어느 공장에서 어느 창고로 얼마나 보내는지 정한다. |
| 수식 언어 | row sums equal supply, column sums equal demand. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 수송량 행렬, 행합/열합 제약, 단위비용 행렬의 SUMPRODUCT로 만든다. |

**강의 속 실제 예제 연결:** DM_PDF06은 공급지/수요지, 공급량/수요량, 단위당 수송비용을 수송문제의 핵심 요소로 제시한다.

**자주 하는 실수:** 공급-수요가 불균형이면 dummy supply/demand를 추가해야 하는데 이를 놓치기 쉽다.

**연결 관계**

- 선행 노드: LP equality constraints
- 후속 노드: transshipment and min-cost flow
- 동형/유사 노드: Big M 운송 예제

**근거:** `ev_DM_PDF06_001` -> `DM_PDF06:p001:L002`

> 5.1 수송문제 Transportation problem

## n_DM_PDF06.transshipment_problem — 경유수송문제 (transshipment problem)

**한 줄 정의:** 공급지와 수요지 사이에 경유지가 존재하고, 각 노드에서 유입과 유출의 균형을 맞추는 네트워크 LP다.

**쉬운 직관:** 물건이 중간 물류센터를 거쳐 이동할 수 있으므로 단순 행렬보다 네트워크 흐름 보존이 중요해진다.

**수식 또는 모형 형태:** for each node: inflow + supply = outflow + demand.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 공장에서 물류센터를 거쳐 고객 지역으로 보내는 구조다. |
| 수식 언어 | node balance constraints replace simple row/column sums. |
| 스프레드시트/타블로 언어 | Solver에서는 arc flow 변수를 두고 각 노드별 balance 셀을 만든다. |

**강의 속 실제 예제 연결:** DM_PDF06은 경유지 존재와 지역 간 단위비용을 transshipment의 차이로 제시한다.

**자주 하는 실수:** 경유지를 공급지나 수요지처럼만 처리하면 유입=유출 balance를 빠뜨린다.

**연결 관계**

- 선행 노드: transportation problem
- 후속 노드: minimum cost flow
- 동형/유사 노드: flow conservation in networks

**근거:** `ev_DM_PDF06_002` -> `DM_PDF06:p001:L003`

> 5.2 경유수송문제 Transshipment problem

## n_DM_PDF06.assignment_problem — 할당문제 (assignment problem)

**한 줄 정의:** 각 작업을 각 자원에 1:1로 배정해 총 비용을 최소화하거나 효용을 최대화하는 0-1 네트워크 특수형이다.

**쉬운 직관:** 각 사람은 하나의 일만, 각 일도 한 사람에게만 배정되는 matching 문제다.

**수식 또는 모형 형태:** x_ij in {0,1}, sum_j x_ij = 1, sum_i x_ij = 1.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 작업을 기계에 할당하거나 작업자를 작업에 배정한다. |
| 수식 언어 | binary matrix with every row sum and column sum equal to 1. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 0/1 배정 행렬과 행합/열합=1 제약으로 구성한다. |

**강의 속 실제 예제 연결:** DM_PDF06은 할당문제를 공급지 수=수요지 수, 공급량=수요량=1인 특별한 수송문제로 설명한다.

**자주 하는 실수:** 할당문제를 일반 수송처럼 연속변수로 둬도 특수 구조상 정수해가 나올 수 있지만, 의미상 0-1 해석을 유지해야 한다.

**연결 관계**

- 선행 노드: transportation problem
- 후속 노드: TSP and matching
- 동형/유사 노드: Sellmore assignment

**근거:** `ev_DM_PDF06_003` -> `DM_PDF06:p001:L004`

> 5.3 할당문제 Assignment problem

## n_DM_PDF06.network_flow — 네트워크 흐름 (network flow)

**한 줄 정의:** 노드와 arc로 구성된 시스템에서 흐름량을 결정하고 보존/용량/비용 제약을 만족시키는 모형군이다.

**쉬운 직관:** 각 길에 얼마를 흘릴지 정하고, 각 지점에서 들어온 양과 나간 양의 장부를 맞춘다.

**수식 또는 모형 형태:** flow conservation plus capacity constraints on arcs.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 최단경로, 최대흐름, 최소비용흐름이 모두 같은 네트워크 언어를 공유한다. |
| 수식 언어 | node balance rows and arc variable columns form the spreadsheet matrix. |
| 스프레드시트/타블로 언어 | Solver에서는 arc별 변수, 노드별 balance, arc capacity 제약으로 구성한다. |

**강의 속 실제 예제 연결:** DM_PDF06은 shortest path, maximum flow, minimum cost flow, CPM/PERT를 같은 장의 네트워크 분석으로 묶는다.

**자주 하는 실수:** 경로 선택 문제와 흐름량 문제를 구분하지 않으면 변수 정의가 흔들린다.

**연결 관계**

- 선행 노드: LP formulation
- 후속 노드: CPM/PERT and project networks
- 동형/유사 노드: graph representation of constraints

**근거:** `ev_DM_PDF06_004` -> `DM_PDF06:p001:L006`

> 5.5 최대흐름 문제 Maximum flow problem

## 표/수식 재구성 메모

- PDF에서 표가 한 줄로 붙어 추출된 경우, 최종 학습 문서에서는 변수, 목적함수, 제약식, RHS, 판정 기준을 분리해 읽는다.
- 타블로/스프레드시트 표는 `변수 셀 -> LHS 계산 셀 -> RHS -> 부호/도메인` 순서로 재구성한다.
- `[EXTRACTION_GAP]` 페이지는 OCR 또는 수동 전사 후보이며, 현재 RAG의 근거로 단정 사용하지 않는다.

## Source Trace

| RAG label | sidecar id | PDF transcript anchor | normalized PDF |
|---|---|---|---|
| `n_DM_PDF06.transportation_problem` | `ev_DM_PDF06_001` | `DM_PDF06:p001:L002` | `DM_PDF06_ch05_transportation_network_week1.pdf` |
| `n_DM_PDF06.transshipment_problem` | `ev_DM_PDF06_002` | `DM_PDF06:p001:L003` | `DM_PDF06_ch05_transportation_network_week1.pdf` |
| `n_DM_PDF06.assignment_problem` | `ev_DM_PDF06_003` | `DM_PDF06:p001:L004` | `DM_PDF06_ch05_transportation_network_week1.pdf` |
| `n_DM_PDF06.network_flow` | `ev_DM_PDF06_004` | `DM_PDF06:p001:L006` | `DM_PDF06_ch05_transportation_network_week1.pdf` |
