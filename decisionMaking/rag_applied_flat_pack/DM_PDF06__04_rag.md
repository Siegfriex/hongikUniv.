# DM_PDF06 — Ch.5 수송계획과 네트워크 분석 최종 RAG 튜터 운영문서

## 0. Document Contract

- **문서 성격:** PDF 요약본이 아니라, 전담 1:1 경영과학 튜터와 RAG agent가 함께 쓰는 증거 기반 운영문서다.
- **source_id:** `DM_PDF06`
- **normalized_pdf:** `decisionMaking/pdf_sources/DM_PDF06_ch05_transportation_network_week1.pdf`
- **primary transcript:** `decisionMaking/pdf_transcripts/DM_PDF06__ch05_transportation_network_week1__full_transcript.md`
- **sidecar:** `decisionMaking/_inventory/DM_PDF06__ch05_transportation_network_week1`
- **flat-pack target:** `decisionMaking/rag_applied_flat_pack/DM_PDF06__04_rag.md`
- **source priority:** 1) PDF 전사본 anchor, 2) 이 문서의 enhanced sidecar, 3) 웹 그라운딩, 4) 일반 OR/MS 지식.
- **중요한 명명 주의:** `DM_PDF06`는 PDF intake index다. 강의 회차/장 번호와 혼동하지 않는다.

### Web Grounding Notes

웹 근거는 PDF 원문을 대체하지 않는다. Solver 구현, LP/MIP/flow 표준 용어, Excel 함수 의미를 보조 확인하기 위해서만 사용한다.

| web_id | role in this RAG | URL |
|---|---|---|
| `WEB_OR_TOOLS_MIN_COST_FLOW` | Min-cost flow grounding: start nodes, end nodes, capacities, unit costs, supplies/demands. | https://developers.google.com/optimization/flow/mincostflow |
| `WEB_OR_TOOLS_MAX_FLOW` | Maximum-flow grounding: nodes/arcs, capacities, source, sink, flow conservation. | https://developers.google.com/optimization/flow/maxflow |
| `WEB_OR_TOOLS_ASSIGNMENT` | Assignment constraints: each worker at most one task and each task exactly one worker. | https://developers.google.com/optimization/assignment/assignment_example |
| `WEB_MS_SUMPRODUCT` | Spreadsheet objective grounding: multiply corresponding arrays and sum the products. | https://support.microsoft.com/en-US/Excel/sumproduct-function |
| `WEB_MS_SUMIF` | Spreadsheet node-balance grounding: sum rows that satisfy a node criterion. | https://support.microsoft.com/en-US/Excel/sumif-function |
| `WEB_OR_TOOLS_LP` | LP/Simplex-style solver model grounding: variables, constraints, objective, optimal solution. | https://developers.google.com/optimization/lp/lp_example |

## 1. Source Coverage Map

| page | primary anchors | extracted focus | extraction note |
|---|---|---|---|
| p001 | `DM_PDF06:p001:L002, DM_PDF06:p001:L003` | 5.1 수송문제 Transportation problem / 5.2 경유수송문제 Transshipment problem / 5.3 할당문제 Assignment problem | ok |
| p002 | `DM_PDF06:p002:L002, DM_PDF06:p002:L003` | (1) 수송문제 Transportation problem / • 공급지 및 수요지 : 다수 / • 공급량 및 수요량 : 주어짐 | ok |
| p003 | `DM_PDF06:p003:L002, DM_PDF06:p003:L003` | (2) 경유수송문제 Transshipment problem / • 공급지 및 수요지 : 다수 & 경유지 : 존재함 / • 공급량 및 수요량 : 주어짐 | ok |
| p004 | `DM_PDF06:p004:L002, DM_PDF06:p004:L003` | [예제 5.1] 분배 문제 Transportation Problem / • 도요타 USA는 북미 시카고, 멤피스, 찰스톤에 PDC(부품배 / 송센터)를 운영하고 있다. | ok |
| p005 | `DM_PDF06:p005:L002, DM_PDF06:p005:L003` | 모형화 가이드 / • 부품 수송계획 (transportation) / • 각 화살표 연결(수송경로)에 대응되는 수송량을 결정 | ok |
| p006 | `DM_PDF06:p006:L002, DM_PDF06:p006:L003` | • 스프레드시트 모형화(초기해) / 전통적인 부등호 방향 | LOW_TEXT |
| p007 | `DM_PDF06:p007:L002, DM_PDF06:p007:L003` | • 해찾기 모델 설정(최적해) / 옵션: / (1) 선형계획 | LOW_TEXT |
| p008 | `DM_PDF06:p008:L001, DM_PDF06:p008:L002` | 8불균형 수송문제 / 1. 공급량의 합 > 수요량의 합 / • 공급지 조건 : 실제공급량 <= 공급량(우변) | ok |
| p009 | `DM_PDF06:p009:L002, DM_PDF06:p009:L003` | 수송문제의 수리모형화 / • Xij : 공급지 i에서 수요지 j로 수송량 / i=1 | LOW_TEXT |
| p010 | `DM_PDF06:p010:L002, DM_PDF06:p010:L003` | 수송문제의 수리모형(계속) / Minimize / 300X11+550X12+700X13+420X21+200X22+500X23+320X31+350X32+600X33 | ok |
| p011 | `DM_PDF06:p011:L002, DM_PDF06:p011:L003` | 수송문제의 수리모형(일반형) / 공급량 Si 및 수요량 Dj 정수이면, /  정수해 보장됨 | LOW_TEXT |
| p012 | `DM_PDF06:p012:L002, DM_PDF06:p012:L003` | 수송문제의 민감도 분석 / (질문1) 찰스톤헌쓰빌 수송비용 600 에 비해 찰스톤내시빌 / 수송비용 350 이 적은데 여기에 배정하는 것이 유리하지 않은 | ok |
| p013 | `DM_PDF06:p013:L002, DM_PDF06:p013:L003` | 민감도 보고서 / (질문1 관련) 찰스톤헌쓰빌 수송비용 600, 찰스톤내시빌 수송비용 350 / 만일 찰스톤내시빌에 100 만큼 배정한다면 수송비용이 50씩 증가됨 | ok |
| p014 | `DM_PDF06:p014:L002, DM_PDF06:p014:L003` | 민감도 보고서 / (질문2 관련) 멤피스 공급량을 100 늘리면, 아래와 같이 10,000 만큼 비용이 / 줄어드나, 대신 찰스톤 공급량을 100 줄였을 때 어떻게 변할 지는 현재로는 | ok |
| p015 | `DM_PDF06:p015:L002, DM_PDF06:p015:L003` | [예제 5.3] 기계의 준비시간 줄이기 / • 4개의 기계에 4개의 작업을 할당하려 함 / • 각 기계는 한 개의 작업만 수행함 | ok |
| p016 | `DM_PDF06:p016:L002, DM_PDF06:p016:L003` |  최적해에서 변경셀에 소수 값이 나오지 않는가? / • 수송문제의 해의 성질 이용  정수해(0 or 1)가 보장됨 / 정수이기때문 | LOW_TEXT |
| p017 | `DM_PDF06:p017:L002, DM_PDF06:p017:L003` | [예제 5.2] 농산물 유통의 경유 수송문제 / • 경유수송문제 (transshipment problem) / • S농산물 가공회사 : 공장 3곳, 중간창고 2곳, 수요지 도시 2곳 | ok |
| p018 | `DM_PDF06:p018:L002, DM_PDF06:p018:L003` | • 표 5.3 : 수송 비용표 (참고: ‘-’ 수송 불가능) / • 창고는 수요지인가? 공급지인가? / 어떻게 모형화 하여야 하나? 경유지임. | ok |
| p019 | `DM_PDF06:p019:L002, DM_PDF06:p019:L003` | 모형화 가이드 /  경유지를 일단 공급지이면서 동시에 수요지로 간주 / • 공급지 : 공장1, 공장2, 공장3, 창고4, 창고5 (창고 2곳 추가) | ok |
| p020 | `DM_PDF06:p020:L002` | 경유 수송문제 모형(수리모형화) | LOW_TEXT |
| p021 | `DM_PDF06:p021:L002` | • 스프레드시트 모형화(경유수송문제로 모형화) | LOW_TEXT |
| p022 | `DM_PDF06:p022:L002, DM_PDF06:p022:L003` | 1. 최소비용 흐름문제 : / • minimum cost network flow problem / • 공급지(다수)에서 수요지(다수)까지 일정량을 흐르게 하되 | ok |
| p023 | `DM_PDF06:p023:L002, DM_PDF06:p023:L003` | A / HC / F | ok |
| p024 | `DM_PDF06:p024:L002, DM_PDF06:p024:L003` | A / HC / F | LOW_TEXT |
| p025 | `DM_PDF06:p025:L002, DM_PDF06:p025:L003` | 5.6 최소비용 흐름 문제 / Minimum cost network flow problem / • 모형요소 | ok |
| p026 | `DM_PDF06:p026:L002, DM_PDF06:p026:L003` |  최소비용 흐름 문제(계속) / • 의무유출량(required net-flow) … 입력자료 / – 노드에서 의무적으로 만족시켜야 되는 순수 공급량 | ok |
| p027 | `DM_PDF06:p027:L002, DM_PDF06:p027:L003` | [예제5.6] 레미콘 믹서의 흐름배치 문제 / • 레미콘 공장: 도시 3 (공급량 150) / • 공사장: 도시 1 (수료량 70) 및 도시 6 (수요량 60) | ok |
| p028 | `DM_PDF06:p028:L002, DM_PDF06:p028:L003` | 불균형문제 : 공급량합 > 수요량합 / 노드 1 (수요지) 조건 / 노드 6 (수요지) 조건 | ok |
| p029 | `DM_PDF06:p029:L002, DM_PDF06:p029:L003` |  스프레드시트모형 / 1. 아크별 : 흐름량(변경셀) ≤ 흐름용량(입력자료) / 2. 노드별 : 순수유출량(식) =(or <=) 의무유출량(150, 0, -70) | ok |
| p030 | `DM_PDF06:p030:L001, DM_PDF06:p030:L002` |  스프레드시트에서 노드별 순수 유출량 계산 어려움: / (네트워크가 클때) / =SUMIF(시작 노드가 3인 Xij ) - SUMIF (종료 노드가 3인 Xij ) | ok |
| p031 | `DM_PDF06:p031:L002, DM_PDF06:p031:L003` |  노드별 순수 유출량 계산 / SUMIF(영역A, 셀B or 값, 영역C) 함수 이용 : / “if 조건에 만족하는 값들을 sum 한다”. 즉, 영역A에서 셀B | ok |
| p032 | `DM_PDF06:p032:L002, DM_PDF06:p032:L003` | 시작 / 노드 / 종료 | ok |
| p033 | `DM_PDF06:p033:L002, DM_PDF06:p033:L003` | • 스프레드 시트 모형화 / 최소비용 흐름문제 해의 성질: 흐름용량과 의무유출량이 정수이면, /  최적 흐름량이 정수가 됨 | ok |
| p034 | `DM_PDF06:p034:L002` | 최적해 결과 (경로 및 흐름량) | LOW_TEXT |
| p035 | `DM_PDF06:p035:L002, DM_PDF06:p035:L003` | 실습 / 1) [예제 5-2] 경유수송문제 … slide 21 / 2) 각 노드의 공급가능량 및 수요량은 <표1>과 같고, 각 | ok |
| p036 | `DM_PDF06:p036:L002, DM_PDF06:p036:L003` | 노드 / 공급량(+) / 또는 | ok |

## 2. Chapter Thesis

이 장은 LP를 네트워크 구조로 재해석한다. 수송문제, 경유수송, 할당, 최소비용흐름은 모두 flow balance와 arc cost/capacity를 공유하는 같은 계열의 모델이다.

## 3. Current Graph Position

- **현재 그래프 위치:** LP formulation -> transportation matrix -> transshipment node balance -> assignment special case -> min-cost/max-flow/shortest path -> CPM/PERT.
- **지금 보는 노드:** `DM_PDF06` / Ch.5 수송계획과 네트워크 분석
- **튜터 운영 원칙:** 질문이 들어오면 먼저 노드로 매핑하고, 예제 카드와 수식/Solver 구조를 거쳐 Source Trace Table의 evidence anchor로 되돌아간다.

## 4. Learning Outcomes

- 수송문제, 불균형 수송, 할당, 경유수송, 최소비용흐름을 하나의 네트워크 계열로 설명한다.
- 수식, 그래프, Solver 행렬/SUMPRODUCT/SUMIF 관점을 서로 번역한다.
- 질문 유형별로 노드와 evidence anchor를 바로 라우팅한다.

## 5. Concept Graph Map

| node_id | 개념 | 역할 | 선행 노드 | 후속 노드 |
| --- | --- | --- | --- | --- |
| `n_DM_PDF06.transportation_problem` | 수송문제 | 여러 공급지에서 여러 수요지로 얼마를 보낼지 결정해 총 수송비용을 최소화하는 LP 특수형이다. | LP formulation, 공급/수요 RHS | balanced/unbalanced transportation, min-cost flow |
| `n_DM_PDF06.balanced_transportation` | 균형 수송문제 | 총공급량과 총수요량이 같아 모든 공급과 수요를 등식으로 맞추는 수송문제다. | transportation_problem | transportation_integrality |
| `n_DM_PDF06.unbalanced_transportation` | 불균형 수송문제 | 총공급량과 총수요량이 달라 제약 방향 조정 또는 dummy supply/demand가 필요한 수송문제다. | balanced_transportation | dummy_supply_or_demand |
| `n_DM_PDF06.dummy_supply_or_demand` | 가상 공급지/수요지 | 불균형 수송문제를 균형형처럼 풀기 위해 추가하는 가상의 공급 또는 수요 노드다. | unbalanced_transportation | penalty modeling |
| `n_DM_PDF06.transportation_integrality` | 수송문제 정수해 성질 | 공급량과 수요량이 정수이면 int 조건을 걸지 않아도 수송문제 최적해가 정수로 보장되는 성질이다. | balanced_transportation | assignment_problem, min-cost integrality |
| `n_DM_PDF06.transportation_solver_model` | Solver 수송모형 | 수송량 행렬을 변경셀로 두고 SUMPRODUCT 목적셀과 행합/열합 제약으로 만든 Excel Solver 모형이다. | transportation_problem | transportation_sensitivity |
| `n_DM_PDF06.transportation_sensitivity` | 수송문제 민감도 | 수송비용 또는 공급가능량 변화가 총비용과 최적 배정에 미치는 영향을 reduced cost/shadow price로 해석한다. | transportation_solver_model | DM_PDF02 sensitivity |
| `n_DM_PDF06.assignment_problem` | 할당문제 | 공급량과 수요량이 모두 1인 특별한 수송문제로, 자원과 작업을 1:1로 배정한다. | transportation_integrality | set partitioning, TSP |
| `n_DM_PDF06.transshipment_problem` | 경유수송문제 | 공급지와 수요지 사이에 경유지가 있어 유입과 유출 균형을 함께 만족시키는 네트워크 수송문제다. | transportation_problem | minimum_cost_flow |
| `n_DM_PDF06.transshipment_balance` | 경유지 유입=유출 | 경유지에서 공급한 양과 공급받은 양이 같아야 한다는 흐름보존 제약이다. | transshipment_problem | minimum_cost_flow node balance |
| `n_DM_PDF06.minimum_cost_flow` | 최소비용흐름 | 아크별 비용과 용량, 노드별 공급/수요를 가진 네트워크에서 총 흐름비용을 최소화하는 일반 모형이다. | transshipment_balance | maximum_flow, shortest_path |
| `n_DM_PDF06.maximum_flow` | 최대흐름 | 원천지에서 목적지까지 arc capacity를 넘지 않으면서 보낼 수 있는 총 흐름량을 최대화하는 네트워크 문제다. | minimum_cost_flow | max-flow min-cut duality |
| `n_DM_PDF06.shortest_path` | 최단경로 | 출발지에서 목적지까지 거리나 비용이 가장 작은 경로를 찾는 네트워크 문제다. | minimum_cost_flow | CPM/PERT |
| `n_DM_PDF06.network_topology_table` | 네트워크 토폴로지 표 | 아크를 시작노드, 종료노드, 단위흐름비용, 흐름용량 열로 표현하는 Solver 친화적 표 구조다. | minimum_cost_flow | sumif_node_balance |
| `n_DM_PDF06.sumif_node_balance` | SUMIF 순수유출량 | 시작노드가 해당 노드인 흐름 합에서 종료노드가 해당 노드인 흐름 합을 빼 순수유출량을 계산하는 스프레드시트 패턴이다. | network_topology_table | minimum_cost_flow |
| `n_DM_PDF06.cpm_pert` | CPM/PERT 프로젝트 네트워크 | 프로젝트 활동의 선후관계와 기간을 네트워크로 표현해 critical path와 일정 위험을 분석하는 후속 네트워크 분석 주제다. | shortest_path/longest path | project scheduling |

### Edge List

| from | edge_type | to |
| --- | --- | --- |
| `LP formulation, 공급/수요 RHS` | 선행 관계 | `n_DM_PDF06.transportation_problem` |
| `n_DM_PDF06.transportation_problem` | 후속 관계 | `balanced/unbalanced transportation, min-cost flow` |
| `n_DM_PDF06.transportation_problem` | 동형/유사 | `assignment problem, transportation-like blending` |
| `transportation_problem` | 선행 관계 | `n_DM_PDF06.balanced_transportation` |
| `n_DM_PDF06.balanced_transportation` | 후속 관계 | `transportation_integrality` |
| `n_DM_PDF06.balanced_transportation` | 동형/유사 | `balanced min-cost flow` |
| `balanced_transportation` | 선행 관계 | `n_DM_PDF06.unbalanced_transportation` |
| `n_DM_PDF06.unbalanced_transportation` | 후속 관계 | `dummy_supply_or_demand` |
| `n_DM_PDF06.unbalanced_transportation` | 동형/유사 | `minimum_cost_flow imbalance` |
| `unbalanced_transportation` | 선행 관계 | `n_DM_PDF06.dummy_supply_or_demand` |
| `n_DM_PDF06.dummy_supply_or_demand` | 후속 관계 | `penalty modeling` |
| `n_DM_PDF06.dummy_supply_or_demand` | 동형/유사 | `artificial variable but model-level` |
| `balanced_transportation` | 선행 관계 | `n_DM_PDF06.transportation_integrality` |
| `n_DM_PDF06.transportation_integrality` | 후속 관계 | `assignment_problem, min-cost integrality` |
| `n_DM_PDF06.transportation_integrality` | 동형/유사 | `total unimodularity intuition` |
| `transportation_problem` | 선행 관계 | `n_DM_PDF06.transportation_solver_model` |
| `n_DM_PDF06.transportation_solver_model` | 후속 관계 | `transportation_sensitivity` |
| `n_DM_PDF06.transportation_solver_model` | 동형/유사 | `spreadsheet LP pattern` |
| `transportation_solver_model` | 선행 관계 | `n_DM_PDF06.transportation_sensitivity` |
| `n_DM_PDF06.transportation_sensitivity` | 후속 관계 | `DM_PDF02 sensitivity` |
| `n_DM_PDF06.transportation_sensitivity` | 동형/유사 | `network reduced cost` |
| `transportation_integrality` | 선행 관계 | `n_DM_PDF06.assignment_problem` |
| `n_DM_PDF06.assignment_problem` | 후속 관계 | `set partitioning, TSP` |
| `n_DM_PDF06.assignment_problem` | 동형/유사 | `matching` |
| `transportation_problem` | 선행 관계 | `n_DM_PDF06.transshipment_problem` |
| `n_DM_PDF06.transshipment_problem` | 후속 관계 | `minimum_cost_flow` |
| `n_DM_PDF06.transshipment_problem` | 동형/유사 | `node balance` |
| `transshipment_problem` | 선행 관계 | `n_DM_PDF06.transshipment_balance` |
| `n_DM_PDF06.transshipment_balance` | 후속 관계 | `minimum_cost_flow node balance` |
| `n_DM_PDF06.transshipment_balance` | 동형/유사 | `inventory conservation` |
| `transshipment_balance` | 선행 관계 | `n_DM_PDF06.minimum_cost_flow` |
| `n_DM_PDF06.minimum_cost_flow` | 후속 관계 | `maximum_flow, shortest_path` |
| `n_DM_PDF06.minimum_cost_flow` | 동형/유사 | `network simplex` |
| `minimum_cost_flow` | 선행 관계 | `n_DM_PDF06.maximum_flow` |
| `n_DM_PDF06.maximum_flow` | 후속 관계 | `max-flow min-cut duality` |
| `n_DM_PDF06.maximum_flow` | 동형/유사 | `capacity bottleneck` |
| `minimum_cost_flow` | 선행 관계 | `n_DM_PDF06.shortest_path` |
| `n_DM_PDF06.shortest_path` | 후속 관계 | `CPM/PERT` |
| `n_DM_PDF06.shortest_path` | 동형/유사 | `unit min-cost flow` |
| `minimum_cost_flow` | 선행 관계 | `n_DM_PDF06.network_topology_table` |
| `n_DM_PDF06.network_topology_table` | 후속 관계 | `sumif_node_balance` |
| `n_DM_PDF06.network_topology_table` | 동형/유사 | `edge list graph` |
| `network_topology_table` | 선행 관계 | `n_DM_PDF06.sumif_node_balance` |
| `n_DM_PDF06.sumif_node_balance` | 후속 관계 | `minimum_cost_flow` |
| `n_DM_PDF06.sumif_node_balance` | 동형/유사 | `incidence matrix` |
| `shortest_path/longest path` | 선행 관계 | `n_DM_PDF06.cpm_pert` |
| `n_DM_PDF06.cpm_pert` | 후속 관계 | `project scheduling` |
| `n_DM_PDF06.cpm_pert` | 동형/유사 | `DAG path analysis` |

## 6. Core Concept Node Cards

### n_DM_PDF06.transportation_problem — 수송문제 (transportation problem)

1. **한 줄 정의:** 여러 공급지에서 여러 수요지로 얼마를 보낼지 결정해 총 수송비용을 최소화하는 LP 특수형이다.
2. **쉬운 직관:** 공급은 넘치지 않게, 수요는 채우면서 가장 싼 출발지-도착지 조합을 찾는다.
3. **언제 쓰는가:** 다수 공급지와 다수 수요지가 있고 경유지와 arc capacity가 없을 때 쓴다.
4. **변수 정의:** x_ij=공급지 i에서 수요지 j로 보내는 수송량.
5. **목적함수:** min sum_i sum_j c_ij x_ij.
6. **제약식:** sum_j x_ij <= S_i, sum_i x_ij >= D_j, x_ij>=0. 균형이면 등식으로 읽을 수 있다.
7. **수식의 현실 의미:** 어느 PDC에서 어느 딜러로 몇 개를 보낼지 정하는 것이다.
8. **그래프/네트워크 관점:** 공급노드와 수요노드를 잇는 bipartite network다.
9. **스프레드시트/Solver 관점:** 3x3 changing cells, 행합=공급량, 열합=수요량, SUMPRODUCT(비용행렬, 수송량행렬).
10. **강의 예제 연결:** Toyota PDC 분배 문제.
11. **예제 숫자 해석:** 시카고/멤피스/찰스톤 공급과 루이스빌/내시빌/헌쓰빌 수요 6,650의 균형.
12. **자주 하는 실수:** 행합과 열합 방향을 뒤집거나 수요 제약을 <=로 두는 오류.
13. **선행 노드:** LP formulation, 공급/수요 RHS
14. **후속 노드:** balanced/unbalanced transportation, min-cost flow
15. **동형/유사 노드:** assignment problem, transportation-like blending
16. **시험 출제 포인트:** 변수 x_ij와 행/열 제약 세우기.
17. **RAG retrieval tags:** `transportation`, `수송문제`, `SUMPRODUCT`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_transportation_problem` -> `DM_PDF06:p001:L002` / source_id=`DM_PDF06`, page=`p001`, block=`p001-L002`, line=`L002`

> 근거 excerpt: 5.1 수송문제 Transportation problem

### n_DM_PDF06.balanced_transportation — 균형 수송문제 (balanced transportation)

1. **한 줄 정의:** 총공급량과 총수요량이 같아 모든 공급과 수요를 등식으로 맞추는 수송문제다.
2. **쉬운 직관:** 들어온 총량과 나가는 총량이 정확히 맞아 가상의 노드가 필요 없다.
3. **언제 쓰는가:** supply sum=demand sum일 때 기본형으로 쓴다.
4. **변수 정의:** same x_ij matrix.
5. **목적함수:** min total transportation cost.
6. **제약식:** row sums=S_i and column sums=D_j.
7. **수식의 현실 의미:** Toyota 예제에서 공급량합과 수요량합이 모두 6,650이다.
8. **그래프/네트워크 관점:** complete bipartite network with balanced net supply.
9. **스프레드시트/Solver 관점:** 행합/열합이 각각 RHS와 정확히 같게 설정 가능하다.
10. **강의 예제 연결:** Toyota PDC 표.
11. **예제 숫자 해석:** 총수요 2,450+2,000+2,200=6,650.
12. **자주 하는 실수:** 균형인데도 dummy를 추가하거나 부등호를 과도하게 쓰는 오류.
13. **선행 노드:** transportation_problem
14. **후속 노드:** transportation_integrality
15. **동형/유사 노드:** balanced min-cost flow
16. **시험 출제 포인트:** 균형 여부 판정.
17. **RAG retrieval tags:** `balanced`, `균형`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_balanced_transportation` -> `DM_PDF06:p004:L019` / source_id=`DM_PDF06`, page=`p004`, block=`p004-L019`, line=`L019`

> 근거 excerpt: 수요량합

### n_DM_PDF06.unbalanced_transportation — 불균형 수송문제 (unbalanced transportation)

1. **한 줄 정의:** 총공급량과 총수요량이 달라 제약 방향 조정 또는 dummy supply/demand가 필요한 수송문제다.
2. **쉬운 직관:** 재고가 남거나 수요가 부족하면 현실적으로 남김/부족을 표현해야 한다.
3. **언제 쓰는가:** supply sum != demand sum일 때 쓴다.
4. **변수 정의:** x_ij plus optional dummy row/column.
5. **목적함수:** min total cost with penalty/dummy costs.
6. **제약식:** 공급초과: 공급 <=, 수요 >= 또는 =. 공급부족: 가상공급지 추가.
7. **수식의 현실 의미:** 공급량합 6,000, 수요량합 6,650이면 가상 공급지 650이 필요하다.
8. **그래프/네트워크 관점:** unbalanced net supply network.
9. **스프레드시트/Solver 관점:** dummy row/column and large costs, Solver constraints adjusted.
10. **강의 예제 연결:** 불균형 수송문제 슬라이드.
11. **예제 숫자 해석:** 가상공급지 공급량=수요합-공급합.
12. **자주 하는 실수:** 공급부족을 그냥 infeasible로 끝내거나 dummy 비용을 0으로 두는 오류.
13. **선행 노드:** balanced_transportation
14. **후속 노드:** dummy_supply_or_demand
15. **동형/유사 노드:** minimum_cost_flow imbalance
16. **시험 출제 포인트:** 불균형 처리 방향.
17. **RAG retrieval tags:** `unbalanced`, `불균형`, `dummy`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_unbalanced_transportation` -> `DM_PDF06:p008:L001` / source_id=`DM_PDF06`, page=`p008`, block=`p008-L001`, line=`L001`

> 근거 excerpt: 8불균형 수송문제

### n_DM_PDF06.dummy_supply_or_demand — 가상 공급지/수요지 (dummy supply or demand)

1. **한 줄 정의:** 불균형 수송문제를 균형형처럼 풀기 위해 추가하는 가상의 공급 또는 수요 노드다.
2. **쉬운 직관:** 부족분이나 남는 양의 회계 처리 칸이다.
3. **언제 쓰는가:** 공급부족 또는 공급초과를 균형화할 때 쓴다.
4. **변수 정의:** dummy row/column variables.
5. **목적함수:** dummy arc cost는 의미에 따라 0 또는 큰 벌점이 될 수 있다.
6. **제약식:** dummy 공급량/수요량은 차이분으로 둔다.
7. **수식의 현실 의미:** 공급부족 때 가상공급지 비용을 매우 큰 수로 두면 미충족 수요를 벌점 처리한다.
8. **그래프/네트워크 관점:** artificial network node.
9. **스프레드시트/Solver 관점:** Solver에서 새 행/열을 추가한다.
10. **강의 예제 연결:** p008 가상공급지 650.
11. **예제 숫자 해석:** dummy supply=650.
12. **자주 하는 실수:** dummy를 실제 공급지처럼 해석하는 오류.
13. **선행 노드:** unbalanced_transportation
14. **후속 노드:** penalty modeling
15. **동형/유사 노드:** artificial variable but model-level
16. **시험 출제 포인트:** dummy 비용 설정.
17. **RAG retrieval tags:** `dummy`, `가상공급지`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_dummy_supply_or_demand` -> `DM_PDF06:p008:L007` / source_id=`DM_PDF06`, page=`p008`, block=`p008-L007`, line=`L007`

> 근거 excerpt:  가상공급지에서 수요지까지 수송비용 = 매우 큰 수

### n_DM_PDF06.transportation_integrality — 수송문제 정수해 성질 (transportation integrality property)

1. **한 줄 정의:** 공급량과 수요량이 정수이면 int 조건을 걸지 않아도 수송문제 최적해가 정수로 보장되는 성질이다.
2. **쉬운 직관:** 네트워크 행렬 구조 자체가 정수해를 끌어내는 특수한 경우다.
3. **언제 쓰는가:** 수송/할당/최소비용흐름에서 정수조건 필요 여부를 판단할 때 쓴다.
4. **변수 정의:** continuous x_ij with integer S_i, D_j.
5. **목적함수:** same min cost objective.
6. **제약식:** transportation constraints only, no extra arbitrary side constraints.
7. **수식의 현실 의미:** 부품 개수처럼 정수 단위인데도 Solver에 int 조건을 안 걸어도 된다.
8. **그래프/네트워크 관점:** network incidence/transportation matrix integrality.
9. **스프레드시트/Solver 관점:** Simplex LP로 풀어도 정수해가 나온다.
10. **강의 예제 연결:** p010-p011 정수해 보장.
11. **예제 숫자 해석:** 할당문제 0/1 해 보장의 근거.
12. **자주 하는 실수:** 추가 제약이 들어와도 항상 정수해라고 과잉 일반화하는 오류.
13. **선행 노드:** balanced_transportation
14. **후속 노드:** assignment_problem, min-cost integrality
15. **동형/유사 노드:** total unimodularity intuition
16. **시험 출제 포인트:** int 조건 필요 여부.
17. **RAG retrieval tags:** `integrality`, `정수해`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_transportation_integrality` -> `DM_PDF06:p010:L013` / source_id=`DM_PDF06`, page=`p010`, block=`p010-L013`, line=`L013`

> 근거 excerpt: • 수송문제의 해의 성질: 공급량과 수요량이 정수이면, 최적해는

### n_DM_PDF06.transportation_solver_model — Solver 수송모형 (transportation Solver model)

1. **한 줄 정의:** 수송량 행렬을 변경셀로 두고 SUMPRODUCT 목적셀과 행합/열합 제약으로 만든 Excel Solver 모형이다.
2. **쉬운 직관:** 수식 LP를 스프레드시트의 행렬 계산으로 바꾼 것이다.
3. **언제 쓰는가:** 수송문제를 실제 Excel로 풀 때 쓴다.
4. **변수 정의:** 3x3 array changing cells.
5. **목적함수:** SUMPRODUCT(cost matrix, shipment matrix).
6. **제약식:** row sums <= supply, column sums >= demand, changing cells>=0.
7. **수식의 현실 의미:** 각 화살표 수송량이 변경셀이다.
8. **그래프/네트워크 관점:** bipartite arcs become matrix cells.
9. **스프레드시트/Solver 관점:** Solver Simplex LP, nonnegative option, no int needed in basic transportation.
10. **강의 예제 연결:** p005-p007 모델링 가이드.
11. **예제 숫자 해석:** 행합은 공급한 양, 열합은 공급받는 양.
12. **자주 하는 실수:** 비용행렬과 수송량행렬 차원을 다르게 잡는 오류.
13. **선행 노드:** transportation_problem
14. **후속 노드:** transportation_sensitivity
15. **동형/유사 노드:** spreadsheet LP pattern
16. **시험 출제 포인트:** Solver 셀 구조 설명.
17. **RAG retrieval tags:** `solver`, `SUMPRODUCT`, `changing_cells`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_transportation_solver_model` -> `DM_PDF06:p005:L005` / source_id=`DM_PDF06`, page=`p005`, block=`p005-L005`, line=`L005`

> 근거 excerpt: • 따라서 변경셀을 3 x 3 array 형태로 설정

### n_DM_PDF06.transportation_sensitivity — 수송문제 민감도 (transportation sensitivity)

1. **한 줄 정의:** 수송비용 또는 공급가능량 변화가 총비용과 최적 배정에 미치는 영향을 reduced cost/shadow price로 해석한다.
2. **쉬운 직관:** 왜 싼 경로가 항상 쓰이지 않는지, 어느 PDC 공급을 늘리면 유리한지 묻는다.
3. **언제 쓰는가:** 최적 운송계획 이후 비용/공급 변화 질문에 쓴다.
4. **변수 정의:** shipment variables and route costs/supply RHS.
5. **목적함수:** cost coefficient changes and RHS changes.
6. **제약식:** allowable ranges and shadow prices if available.
7. **수식의 현실 의미:** 찰스톤-내시빌에 100 배정하면 비용 50씩 증가할 수 있다.
8. **그래프/네트워크 관점:** route arcs have reduced costs; supply nodes have shadow values.
9. **스프레드시트/Solver 관점:** Solver sensitivity report.
10. **강의 예제 연결:** p012-p014 민감도 보고서.
11. **예제 숫자 해석:** 멤피스 공급 100 증가 시 비용 10,000 감소 사례.
12. **자주 하는 실수:** 거리/비용이 작다고 항상 배정된다고 생각하는 오류.
13. **선행 노드:** transportation_solver_model
14. **후속 노드:** DM_PDF02 sensitivity
15. **동형/유사 노드:** network reduced cost
16. **시험 출제 포인트:** 수송 민감도 해석.
17. **RAG retrieval tags:** `transportation_sensitivity`, `reduced_cost`, `shadow_price`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_transportation_sensitivity` -> `DM_PDF06:p013:L002` / source_id=`DM_PDF06`, page=`p013`, block=`p013-L002`, line=`L002`

> 근거 excerpt: 민감도 보고서

### n_DM_PDF06.assignment_problem — 할당문제 (assignment problem)

1. **한 줄 정의:** 공급량과 수요량이 모두 1인 특별한 수송문제로, 자원과 작업을 1:1로 배정한다.
2. **쉬운 직관:** 각 기계는 한 작업만, 각 작업도 한 기계에만 배정되는 matching이다.
3. **언제 쓰는가:** 작업-기계, 작업자-작업, 팀 편성에 쓴다.
4. **변수 정의:** x_ij=기계 i가 작업 j를 맡으면 1, 아니면 0.
5. **목적함수:** min total setup time or max total utility.
6. **제약식:** row sums=1, column sums=1, x_ij>=0; 수송 정수해 성질로 0/1 보장.
7. **수식의 현실 의미:** 준비시간을 최소화하는 기계-작업 배정.
8. **그래프/네트워크 관점:** complete bipartite matching network.
9. **스프레드시트/Solver 관점:** binary처럼 해석하지만 강의는 수송문제 정수해 성질로 LP 해도 정수 보장.
10. **강의 예제 연결:** 기계의 준비시간 줄이기.
11. **예제 숫자 해석:** 4개 기계와 4개 작업, 공급량/수요량 모두 1.
12. **자주 하는 실수:** 할당을 일반 수송처럼 해도 되지만 의미상 0/1 해석을 잊는 오류.
13. **선행 노드:** transportation_integrality
14. **후속 노드:** set partitioning, TSP
15. **동형/유사 노드:** matching
16. **시험 출제 포인트:** 0/1 보장 이유.
17. **RAG retrieval tags:** `assignment`, `할당`, `matching`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_assignment_problem` -> `DM_PDF06:p003:L012` / source_id=`DM_PDF06`, page=`p003`, block=`p003-L012`, line=`L012`

> 근거 excerpt: • 특별한 수송문제 간주 : 공급지 수 = 수요지 수, 공급량=1, 수요량=1

### n_DM_PDF06.transshipment_problem — 경유수송문제 (transshipment problem)

1. **한 줄 정의:** 공급지와 수요지 사이에 경유지가 있어 유입과 유출 균형을 함께 만족시키는 네트워크 수송문제다.
2. **쉬운 직관:** 물건이 물류창고를 거쳐 갈 수 있으므로 창고 장부가 맞아야 한다.
3. **언제 쓰는가:** 중간 창고/허브가 있는 물류 문제에 쓴다.
4. **변수 정의:** x_ij=지역 i에서 j로 보내는 양.
5. **목적함수:** min total shipping cost.
6. **제약식:** 공급지/수요지 조건 + 경유지 유입=유출.
7. **수식의 현실 의미:** 창고는 공급지이면서 동시에 수요지로 모형화된다.
8. **그래프/네트워크 관점:** directed network with intermediate nodes.
9. **스프레드시트/Solver 관점:** arc flow variables, node balance constraints.
10. **강의 예제 연결:** 농산물 유통 경유수송문제.
11. **예제 숫자 해석:** 공장 3곳, 창고 2곳, 도시 2곳.
12. **자주 하는 실수:** 경유지를 단순 공급지 또는 수요지 중 하나로만 두는 오류.
13. **선행 노드:** transportation_problem
14. **후속 노드:** minimum_cost_flow
15. **동형/유사 노드:** node balance
16. **시험 출제 포인트:** 경유지 처리.
17. **RAG retrieval tags:** `transshipment`, `경유수송`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_transshipment_problem` -> `DM_PDF06:p001:L003` / source_id=`DM_PDF06`, page=`p001`, block=`p001-L003`, line=`L003`

> 근거 excerpt: 5.2 경유수송문제 Transshipment problem

### n_DM_PDF06.transshipment_balance — 경유지 유입=유출 (transshipment balance)

1. **한 줄 정의:** 경유지에서 공급한 양과 공급받은 양이 같아야 한다는 흐름보존 제약이다.
2. **쉬운 직관:** 창고가 물건을 만들어내거나 소비하지 않는다는 장부 원칙이다.
3. **언제 쓰는가:** transshipment node를 모델링할 때 핵심으로 쓴다.
4. **변수 정의:** inflow and outflow sums at warehouse nodes.
5. **목적함수:** objective는 arc cost 합계.
6. **제약식:** outflow_k = inflow_k for pure transshipment nodes.
7. **수식의 현실 의미:** 창고4, 창고5가 공급지와 수요지 목록에 동시에 들어간다.
8. **그래프/네트워크 관점:** flow conservation at intermediate nodes.
9. **스프레드시트/Solver 관점:** Solver에서 노드별 balance row를 만든다.
10. **강의 예제 연결:** p019 모델링 가이드.
11. **예제 숫자 해석:** 공급한 양=공급 받은 양.
12. **자주 하는 실수:** 경유지에 별도 공급량을 임의로 주는 오류.
13. **선행 노드:** transshipment_problem
14. **후속 노드:** minimum_cost_flow node balance
15. **동형/유사 노드:** inventory conservation
16. **시험 출제 포인트:** 유입/유출 식 작성.
17. **RAG retrieval tags:** `balance`, `flow_conservation`, `경유지`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_transshipment_balance` -> `DM_PDF06:p019:L007` / source_id=`DM_PDF06`, page=`p019`, block=`p019-L007`, line=`L007`

> 근거 excerpt: (공급한 량) = (공급 받은 량) (경유지 창고에서)

### n_DM_PDF06.minimum_cost_flow — 최소비용흐름 (minimum cost flow)

1. **한 줄 정의:** 아크별 비용과 용량, 노드별 공급/수요를 가진 네트워크에서 총 흐름비용을 최소화하는 일반 모형이다.
2. **쉬운 직관:** 수송과 경유수송을 더 일반적인 directed arc table로 표현한 모델이다.
3. **언제 쓰는가:** 복잡한 네트워크에 비용과 용량이 모두 있을 때 쓴다.
4. **변수 정의:** x_ij=arc i->j flow.
5. **목적함수:** min sum c_ij x_ij.
6. **제약식:** x_ij<=u_ij and net outflow_i=required_i.
7. **수식의 현실 의미:** 레미콘 공장에서 공사장까지 비용 최소 흐름경로와 흐름량을 정한다.
8. **그래프/네트워크 관점:** directed graph with capacities and node supplies/demands.
9. **스프레드시트/Solver 관점:** arc table: start node, end node, cost, capacity, flow; node balance via SUMIF.
10. **강의 예제 연결:** 레미콘 믹서 흐름배치.
11. **예제 숫자 해석:** 노드 3 공급 150, 노드1/6 수요 같은 required net-flow.
12. **자주 하는 실수:** 수송문제보다 단순하다고 보는 오류. 오히려 수송/경유수송의 일반화다.
13. **선행 노드:** transshipment_balance
14. **후속 노드:** maximum_flow, shortest_path
15. **동형/유사 노드:** network simplex
16. **시험 출제 포인트:** 아크/노드 제약 구분.
17. **RAG retrieval tags:** `min_cost_flow`, `minimum_cost`, `flow`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_minimum_cost_flow` -> `DM_PDF06:p001:L007` / source_id=`DM_PDF06`, page=`p001`, block=`p001-L007`, line=`L007`

> 근거 excerpt: 5.6 최소비용 흐름문제 Minimum cost flow problem

### n_DM_PDF06.maximum_flow — 최대흐름 (maximum flow)

1. **한 줄 정의:** 원천지에서 목적지까지 arc capacity를 넘지 않으면서 보낼 수 있는 총 흐름량을 최대화하는 네트워크 문제다.
2. **쉬운 직관:** 가장 좁은 병목을 고려해 네트워크가 얼마나 많이 흘릴 수 있는지 본다.
3. **언제 쓰는가:** 비용보다 용량과 throughput이 중심일 때 쓴다.
4. **변수 정의:** x_ij arc flow and total source outflow.
5. **목적함수:** max total flow from source to sink.
6. **제약식:** arc capacity and intermediate flow conservation.
7. **수식의 현실 의미:** 한 원천지에서 한 목적지까지 최대 운송량을 찾는다.
8. **그래프/네트워크 관점:** source-sink directed network.
9. **스프레드시트/Solver 관점:** Solver에서는 arc flow cells and capacity constraints.
10. **강의 예제 연결:** p022 최대흐름 정의.
11. **예제 숫자 해석:** 아크 용량이 주어진 정보다.
12. **자주 하는 실수:** 최대흐름에 비용 최소 목적을 섞어 변수 정의가 흔들리는 오류.
13. **선행 노드:** minimum_cost_flow
14. **후속 노드:** max-flow min-cut duality
15. **동형/유사 노드:** capacity bottleneck
16. **시험 출제 포인트:** 최대흐름과 최소비용흐름 차이.
17. **RAG retrieval tags:** `max_flow`, `maximum`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_maximum_flow` -> `DM_PDF06:p001:L006` / source_id=`DM_PDF06`, page=`p001`, block=`p001-L006`, line=`L006`

> 근거 excerpt: 5.5 최대흐름 문제 Maximum flow problem

### n_DM_PDF06.shortest_path — 최단경로 (shortest path)

1. **한 줄 정의:** 출발지에서 목적지까지 거리나 비용이 가장 작은 경로를 찾는 네트워크 문제다.
2. **쉬운 직관:** 흐름량보다 어떤 길을 선택할지가 핵심이다.
3. **언제 쓰는가:** 단일 출발-도착 경로 선택에 쓴다.
4. **변수 정의:** x_ij path arc selection or unit flow.
5. **목적함수:** min sum distance_ij x_ij.
6. **제약식:** unit supply at source, unit demand at sink, flow conservation.
7. **수식의 현실 의미:** 출발지 의무유출량=1, 목적지=-1인 min-cost flow 특수형으로 볼 수 있다.
8. **그래프/네트워크 관점:** unit-flow network path.
9. **스프레드시트/Solver 관점:** Solver에서는 0/1처럼 해석될 수 있으나 min-cost flow integrality로 경로가 나온다.
10. **강의 예제 연결:** p022, p033 최단경로 응용.
11. **예제 숫자 해석:** 정수 capacity/required net-flow면 정수 흐름이 보장된다.
12. **자주 하는 실수:** 최단경로를 모든 수요를 보내는 수송문제로 혼동하는 오류.
13. **선행 노드:** minimum_cost_flow
14. **후속 노드:** CPM/PERT
15. **동형/유사 노드:** unit min-cost flow
16. **시험 출제 포인트:** 경로 vs 흐름 구분.
17. **RAG retrieval tags:** `shortest_path`, `최단경로`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_shortest_path` -> `DM_PDF06:p033:L005` / source_id=`DM_PDF06`, page=`p033`, block=`p033-L005`, line=`L005`

> 근거 excerpt: (최단경로 문제에 응용 : 출발지 의무유출량=1, 목적지 의무유출량=-1 )

### n_DM_PDF06.network_topology_table — 네트워크 토폴로지 표 (network topology table)

1. **한 줄 정의:** 아크를 시작노드, 종료노드, 단위흐름비용, 흐름용량 열로 표현하는 Solver 친화적 표 구조다.
2. **쉬운 직관:** 그림 네트워크를 행 데이터베이스로 바꾸는 방법이다.
3. **언제 쓰는가:** 큰 네트워크를 스프레드시트로 풀 때 쓴다.
4. **변수 정의:** one row per arc.
5. **목적함수:** total cost uses flow*unit cost over arc rows.
6. **제약식:** capacity row constraints and node balance from arc table.
7. **수식의 현실 의미:** 아크별 입력자료를 표로 만들면 SUMIF 계산이 가능해진다.
8. **그래프/네트워크 관점:** edge list representation.
9. **스프레드시트/Solver 관점:** start/end/cost/capacity/flow columns.
10. **강의 예제 연결:** p029 표현법.
11. **예제 숫자 해석:** 1 2 5 20 같은 행이 arc 1->2의 비용/용량이다.
12. **자주 하는 실수:** 그림만 보고 노드 balance를 수작업으로 흩어 쓰는 오류.
13. **선행 노드:** minimum_cost_flow
14. **후속 노드:** sumif_node_balance
15. **동형/유사 노드:** edge list graph
16. **시험 출제 포인트:** arc table 만들기.
17. **RAG retrieval tags:** `topology`, `arc_table`, `edge_list`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_network_topology_table` -> `DM_PDF06:p029:L007` / source_id=`DM_PDF06`, page=`p029`, block=`p029-L007`, line=`L007`

> 근거 excerpt: 아크별: 시작노드 – 종료노드 – 단위흐름비용 – 흐름용량

### n_DM_PDF06.sumif_node_balance — SUMIF 순수유출량 (SUMIF node balance)

1. **한 줄 정의:** 시작노드가 해당 노드인 흐름 합에서 종료노드가 해당 노드인 흐름 합을 빼 순수유출량을 계산하는 스프레드시트 패턴이다.
2. **쉬운 직관:** 노드별 장부를 조건부 합계 두 번으로 자동 계산한다.
3. **언제 쓰는가:** 큰 네트워크에서 node balance를 효율적으로 만들 때 쓴다.
4. **변수 정의:** flow column and start/end node columns.
5. **목적함수:** objective는 별도 SUMPRODUCT 또는 흐름*비용 합.
6. **제약식:** SUMIF(start,node,flow)-SUMIF(end,node,flow)=required net-flow.
7. **수식의 현실 의미:** 노드3의 X34-X13-X23=-5 같은 식을 자동화한다.
8. **그래프/네트워크 관점:** incidence matrix row computation.
9. **스프레드시트/Solver 관점:** Excel SUMIF(range, criteria, sum_range).
10. **강의 예제 연결:** p030-p032 SUMIF 설명.
11. **예제 숫자 해석:** 노드3 순수유출량 식.
12. **자주 하는 실수:** 시작/종료 SUMIF 순서를 반대로 해 부호를 뒤집는 오류.
13. **선행 노드:** network_topology_table
14. **후속 노드:** minimum_cost_flow
15. **동형/유사 노드:** incidence matrix
16. **시험 출제 포인트:** SUMIF 식 작성.
17. **RAG retrieval tags:** `SUMIF`, `node_balance`, `순수유출량`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_sumif_node_balance` -> `DM_PDF06:p030:L009` / source_id=`DM_PDF06`, page=`p030`, block=`p030-L009`, line=`L009`

> 근거 excerpt: =SUMIF(시작 노드가 3인 Xij ) - SUMIF (종료 노드가 3인 Xij )

### n_DM_PDF06.cpm_pert — CPM/PERT 프로젝트 네트워크 (CPM/PERT)

1. **한 줄 정의:** 프로젝트 활동의 선후관계와 기간을 네트워크로 표현해 critical path와 일정 위험을 분석하는 후속 네트워크 분석 주제다.
2. **쉬운 직관:** 물류 흐름이 아니라 시간이 흐르는 네트워크다.
3. **언제 쓰는가:** 프로젝트 관리 네트워크로 확장할 때 쓴다.
4. **변수 정의:** activity durations and precedence arcs.
5. **목적함수:** minimize/compute project completion time, identify critical path.
6. **제약식:** precedence constraints.
7. **수식의 현실 의미:** 5장 목차의 후속 네트워크 분석이다.
8. **그래프/네트워크 관점:** directed acyclic project graph.
9. **스프레드시트/Solver 관점:** Solver보다는 네트워크 일정표/forward-backward pass가 중심이다.
10. **강의 예제 연결:** p001 CPM/PERT 목차.
11. **예제 숫자 해석:** critical path method와 PERT 명시.
12. **자주 하는 실수:** 수송 flow와 같은 물량 보존식으로 풀려는 오류.
13. **선행 노드:** shortest_path/longest path
14. **후속 노드:** project scheduling
15. **동형/유사 노드:** DAG path analysis
16. **시험 출제 포인트:** CPM/PERT 위치.
17. **RAG retrieval tags:** `CPM`, `PERT`, `project`
18. **Evidence anchors:** `ev_deep_DM_PDF06_node_cpm_pert` -> `DM_PDF06:p001:L010` / source_id=`DM_PDF06`, page=`p001`, block=`p001-L010`, line=`L010`

> 근거 excerpt: Critical path method


## 7. Example Walkthrough Cards

### ex_DM_PDF06.toyota_distribution — Toyota PDC 분배 문제

- **현실 문장 재해석:** 시카고, 멤피스, 찰스톤 PDC에서 루이스빌, 내시빌, 헌쓰빌 딜러 수요를 최소거리로 충족한다.
- **의사결정변수:** x_ij=PDC i에서 딜러 j로 보내는 부품 수.
- **목적함수:** min sum distance_ij x_ij.
- **제약식:** PDC별 공급량, 딜러별 수요량, x_ij>=0.
- **Solver 구조:** 3x3 changing cells, SUMPRODUCT, row sums, column sums, Simplex LP.
- **결과 해석:** 균형 수송문제이며 총공급=총수요=6,650이다.
- **코칭 순서:**
1. 공급/수요 표를 읽는다.
2. x_ij 행렬을 둔다.
3. 행합과 열합을 제약으로 둔다.
4. 총비용/거리 SUMPRODUCT를 최소화한다.
- **Evidence anchors:** `ev_deep_DM_PDF06_example_toyota_distribution` -> `DM_PDF06:p004:L003` / page=`p004`, block=`p004-L003`, line=`L003`

> 근거 excerpt: • 도요타 USA는 북미 시카고, 멤피스, 찰스톤에 PDC(부품배

### ex_DM_PDF06.unbalanced_transportation — 불균형 수송 보정

- **현실 문장 재해석:** 공급량합과 수요량합이 다를 때 제약 방향 또는 dummy node로 모델을 보정한다.
- **의사결정변수:** x_ij plus dummy row/column.
- **목적함수:** min cost with penalty.
- **제약식:** 공급초과/공급부족에 따라 <=, >=, dummy supply/demand.
- **Solver 구조:** 새 행/열과 큰 비용 또는 잔여 비용을 추가한다.
- **결과 해석:** 공급부족이면 가상공급지 650처럼 부족분을 표시한다.
- **코칭 순서:**
1. 총공급과 총수요 비교.
2. 초과/부족 판정.
3. dummy 추가 또는 부등호 방향 조정.
4. 벌점 비용 의미 해석.
- **Evidence anchors:** `ev_deep_DM_PDF06_example_unbalanced_transportation` -> `DM_PDF06:p008:L001` / page=`p008`, block=`p008-L001`, line=`L001`

> 근거 excerpt: 8불균형 수송문제

### ex_DM_PDF06.machine_assignment — 기계 준비시간 할당

- **현실 문장 재해석:** 4개 기계와 4개 작업을 1:1로 배정해 총 준비시간을 최소화한다.
- **의사결정변수:** x_ij=기계 i가 작업 j를 수행하면 1.
- **목적함수:** min sum setup_ij x_ij.
- **제약식:** 각 기계 행합=1, 각 작업 열합=1.
- **Solver 구조:** 수송문제처럼 풀되 정수해 성질로 0/1 보장.
- **결과 해석:** 수송문제의 특수형이므로 별도 int 없이 0/1 해가 나온다.
- **코칭 순서:**
1. 기계와 작업을 공급/수요로 본다.
2. 공급량/수요량을 모두 1로 둔다.
3. 준비시간 행렬을 비용행렬로 둔다.
- **Evidence anchors:** `ev_deep_DM_PDF06_example_machine_assignment` -> `DM_PDF06:p015:L007` / page=`p015`, block=`p015-L007`, line=`L007`

> 근거 excerpt: 하는가? 수송문제로 모형화

### ex_DM_PDF06.transshipment_min_cost — 농산물 경유수송/최소비용흐름

- **현실 문장 재해석:** 공장-창고-도시 네트워크에서 창고의 유입=유출을 만족하며 비용을 최소화한다.
- **의사결정변수:** x_ij=arc shipment/flow.
- **목적함수:** min total arc cost.
- **제약식:** 창고 balance, 공급/수요, arc availability.
- **Solver 구조:** arc variables and node balance rows; larger networks use SUMIF.
- **결과 해석:** 창고는 공급지이면서 수요지인 경유지다.
- **코칭 순서:**
1. 경유지를 식별한다.
2. 창고를 공급/수요 목록에 동시에 넣는다.
3. 유입=유출 제약을 둔다.
4. 최소비용흐름으로 일반화한다.
- **Evidence anchors:** `ev_deep_DM_PDF06_example_transshipment_min_cost` -> `DM_PDF06:p017:L002` / page=`p017`, block=`p017-L002`, line=`L002`

> 근거 excerpt: [예제 5.2] 농산물 유통의 경유 수송문제

### ex_DM_PDF06.ready_mix_flow — 레미콘 최소비용흐름

- **현실 문장 재해석:** 레미콘 공장과 공사장을 연결하는 네트워크에서 흐름비용 합을 최소화한다.
- **의사결정변수:** x_ij=아크 i->j 흐름량.
- **목적함수:** min sum c_ij x_ij.
- **제약식:** x_ij<=u_ij, net outflow=required net-flow.
- **Solver 구조:** topology table, SUMIF node balance, total cost cell.
- **결과 해석:** 수송문제보다 일반적인 arc-capacity 네트워크다.
- **코칭 순서:**
1. 아크표 작성.
2. 흐름량 변경셀.
3. 용량 제약.
4. SUMIF로 노드 balance 계산.
- **Evidence anchors:** `ev_deep_DM_PDF06_example_ready_mix_flow` -> `DM_PDF06:p027:L002` / page=`p027`, block=`p027-L002`, line=`L002`

> 근거 excerpt: [예제5.6] 레미콘 믹서의 흐름배치 문제


## 8. Modeling Pattern Library

| pattern | 모형화 템플릿 | 먼저 볼 노드 | 연결 노드 |
| --- | --- | --- | --- |
| 수송행렬형 | 공급지-수요지 행렬, 행합/열합, SUMPRODUCT. | transportation_solver_model | assignment_problem |
| 경유노드형 | 경유지는 유입=유출 balance를 갖는다. | transshipment_balance | minimum_cost_flow |
| 아크표형 | 시작노드/종료노드/비용/용량/흐름량 edge list로 네트워크를 표현한다. | network_topology_table | sumif_node_balance |
| 정수성형 | 수송/할당/min-cost flow는 정수 입력에서 LP 해가 정수로 나오는 특수 구조를 갖는다. | transportation_integrality | assignment_problem |

## 9. Spreadsheet / Solver Mapping

| 요소 | Solver/Spreadsheet 대응 | 튜터 해설 포인트 |
| --- | --- | --- |
| 수송 결정변수 | 3x3 수송량 행렬, 예: 각 PDC-딜러 arc | 변경셀은 수송량이고 반드시 비용행렬과 같은 크기여야 한다. |
| 수송 목적셀 | SUMPRODUCT(비용행렬, 수송량행렬) | 총 거리/총비용을 최소화한다. |
| 수송 제약셀 | 행합 <= 또는 = 공급량, 열합 >= 또는 = 수요량 | 균형이면 등식으로 해석하고 불균형이면 방향을 점검한다. |
| min-cost flow 변수 | 아크별 흐름량 열 | 각 row가 하나의 arc다. |
| min-cost flow balance | SUMIF(시작노드,node,흐름)-SUMIF(종료노드,node,흐름) | 노드별 순수유출량=의무유출량. |
| 해법 | Simplex LP | 정수 공급/수요/용량이면 일반적으로 int 조건 없이 정수흐름 성질을 활용한다. |

## 10. Cross-Chapter Connections

| 연결 대상 | 연결 설명 | 의존/참조 관계 |
| --- | --- | --- |
| DM_PDF02 민감도 | 수송비 reduced cost와 공급량 shadow price가 수송 민감도 질문을 설명한다. | sensitivity -> transportation |
| DM_PDF04 fixed-charge | 수송 네트워크에 시설개방 0-1 변수를 붙이면 생산-분배 fixed-charge가 된다. | transportation -> MIP |
| DM_PDF05 duality | network flow에는 max-flow/min-cut 등 쌍대적 해석이 뒤따른다. | duality -> network |

## 11. Misconception & Error Diagnosis Bank

| 오답/착각 | 왜 문제인가 | 교정 코칭 | 연결 노드 |
| --- | --- | --- | --- |
| 싸면 무조건 배정 | 네트워크 전체 제약 때문에 싼 arc가 안 쓰일 수 있다. | reduced cost와 전체 balance로 해석. | transportation_sensitivity |
| 경유지를 공급지로만 처리 | 창고 유입=유출이 빠져 물량이 생기거나 사라진다. | 경유지를 공급지/수요지 양쪽에 둔다. | transshipment_balance |
| SUMIF 부호 반대 | 순수유출량 부호가 뒤집혀 공급/수요 해석이 바뀐다. | 시작노드 합 - 종료노드 합 순서를 유지. | sumif_node_balance |
| 할당문제에 정수조건 필수라고 단정 | 수송문제 정수해 성질로 0/1 해가 보장된다. | 단, 추가 제약이 있으면 별도 점검. | transportation_integrality |

## 12. Retrieval Routing Table

| 사용자 질문 유형 | 먼저 볼 노드 | 다음 볼 노드 | 예제 카드 | 근거 힌트 |
| --- | --- | --- | --- | --- |
| 수송문제 식 어떻게 세워? | `transportation_problem` | `transportation_solver_model` | `toyota_distribution` | DM_PDF06:p004-p010 |
| 공급이 수요보다 적으면? | `unbalanced_transportation` | `dummy_supply_or_demand` | `unbalanced_transportation` | DM_PDF06:p008 |
| 할당문제는 왜 0/1이야? | `assignment_problem` | `transportation_integrality` | `machine_assignment` | DM_PDF06:p015-p016 |
| 경유지는 공급지야 수요지야? | `transshipment_problem` | `transshipment_balance` | `transshipment_min_cost` | DM_PDF06:p018-p019 |
| 최소비용흐름과 수송문제 차이? | `minimum_cost_flow` | `transportation_problem, transshipment_problem` | `ready_mix_flow` | DM_PDF06:p022-p029 |
| SUMIF 왜 써? | `sumif_node_balance` | `network_topology_table` | `ready_mix_flow` | DM_PDF06:p030-p032 |
| 민감도 보고서 어떻게 읽어? | `transportation_sensitivity` | `transportation_solver_model` | `toyota_distribution` | DM_PDF06:p012-p014 |

## 13. Tutor Session Protocol

1. **지도부터:** Concept Graph Map과 Edge List를 먼저 보여주고, 현재 노드가 전체 OR/MS 흐름에서 어디인지 설명한다.
2. **노드 중심으로:** Core Concept Node Card의 18개 필드를 순서대로 따라가되, 선행/후속/동형 노드를 최소 3개 연결한다.
3. **예제 중심으로:** Example Walkthrough Card를 사용해 현실 문장 -> 변수 -> 목적함수 -> 제약식 -> Solver -> 결과 해석 순서로 진행한다.
4. **문제 풀이 모드:** 사용자가 변수를 먼저 말하게 하고, 목적함수/제약식은 힌트로 한 단계씩 유도한다.
5. **완성 해설 모드:** 위 절차를 생략하지 않고 전체 풀이를 한 번에 제시한다.
6. **암기/정리 모드:** Modeling Pattern Library, Solver Mapping, Misconception Bank만 압축해 제시한다.

## 14. Practice / Check Questions

1. Toyota 예제에서 x_Chicago,Nashville의 현실 의미와 수식 위치를 설명하라.
2. 공급부족 수송문제에 dummy supply를 추가하는 이유와 비용 설정을 말하라.
3. 노드3에 대해 SUMIF 순수유출량 식을 시작노드/종료노드 기준으로 써라.

## 15. Source Trace Table

| RAG label | evidence_id | source_id | page | block | line | excerpt |
| --- | --- | --- | --- | --- | --- | --- |
| `n_DM_PDF06.transportation_problem` | `ev_deep_DM_PDF06_node_transportation_problem` | `DM_PDF06` | `p001` | `p001-L002` | `L002` | 5.1 수송문제 Transportation problem |
| `n_DM_PDF06.balanced_transportation` | `ev_deep_DM_PDF06_node_balanced_transportation` | `DM_PDF06` | `p004` | `p004-L019` | `L019` | 수요량합 |
| `n_DM_PDF06.unbalanced_transportation` | `ev_deep_DM_PDF06_node_unbalanced_transportation` | `DM_PDF06` | `p008` | `p008-L001` | `L001` | 8불균형 수송문제 |
| `n_DM_PDF06.dummy_supply_or_demand` | `ev_deep_DM_PDF06_node_dummy_supply_or_demand` | `DM_PDF06` | `p008` | `p008-L007` | `L007` |  가상공급지에서 수요지까지 수송비용 = 매우 큰 수 |
| `n_DM_PDF06.transportation_integrality` | `ev_deep_DM_PDF06_node_transportation_integrality` | `DM_PDF06` | `p010` | `p010-L013` | `L013` | • 수송문제의 해의 성질: 공급량과 수요량이 정수이면, 최적해는 |
| `n_DM_PDF06.transportation_solver_model` | `ev_deep_DM_PDF06_node_transportation_solver_model` | `DM_PDF06` | `p005` | `p005-L005` | `L005` | • 따라서 변경셀을 3 x 3 array 형태로 설정 |
| `n_DM_PDF06.transportation_sensitivity` | `ev_deep_DM_PDF06_node_transportation_sensitivity` | `DM_PDF06` | `p013` | `p013-L002` | `L002` | 민감도 보고서 |
| `n_DM_PDF06.assignment_problem` | `ev_deep_DM_PDF06_node_assignment_problem` | `DM_PDF06` | `p003` | `p003-L012` | `L012` | • 특별한 수송문제 간주 : 공급지 수 = 수요지 수, 공급량=1, 수요량=1 |
| `n_DM_PDF06.transshipment_problem` | `ev_deep_DM_PDF06_node_transshipment_problem` | `DM_PDF06` | `p001` | `p001-L003` | `L003` | 5.2 경유수송문제 Transshipment problem |
| `n_DM_PDF06.transshipment_balance` | `ev_deep_DM_PDF06_node_transshipment_balance` | `DM_PDF06` | `p019` | `p019-L007` | `L007` | (공급한 량) = (공급 받은 량) (경유지 창고에서) |
| `n_DM_PDF06.minimum_cost_flow` | `ev_deep_DM_PDF06_node_minimum_cost_flow` | `DM_PDF06` | `p001` | `p001-L007` | `L007` | 5.6 최소비용 흐름문제 Minimum cost flow problem |
| `n_DM_PDF06.maximum_flow` | `ev_deep_DM_PDF06_node_maximum_flow` | `DM_PDF06` | `p001` | `p001-L006` | `L006` | 5.5 최대흐름 문제 Maximum flow problem |
| `n_DM_PDF06.shortest_path` | `ev_deep_DM_PDF06_node_shortest_path` | `DM_PDF06` | `p033` | `p033-L005` | `L005` | (최단경로 문제에 응용 : 출발지 의무유출량=1, 목적지 의무유출량=-1 ) |
| `n_DM_PDF06.network_topology_table` | `ev_deep_DM_PDF06_node_network_topology_table` | `DM_PDF06` | `p029` | `p029-L007` | `L007` | 아크별: 시작노드 – 종료노드 – 단위흐름비용 – 흐름용량 |
| `n_DM_PDF06.sumif_node_balance` | `ev_deep_DM_PDF06_node_sumif_node_balance` | `DM_PDF06` | `p030` | `p030-L009` | `L009` | =SUMIF(시작 노드가 3인 Xij ) - SUMIF (종료 노드가 3인 Xij ) |
| `n_DM_PDF06.cpm_pert` | `ev_deep_DM_PDF06_node_cpm_pert` | `DM_PDF06` | `p001` | `p001-L010` | `L010` | Critical path method |
| `ex_DM_PDF06.toyota_distribution` | `ev_deep_DM_PDF06_example_toyota_distribution` | `DM_PDF06` | `p004` | `p004-L003` | `L003` | • 도요타 USA는 북미 시카고, 멤피스, 찰스톤에 PDC(부품배 |
| `ex_DM_PDF06.unbalanced_transportation` | `ev_deep_DM_PDF06_example_unbalanced_transportation` | `DM_PDF06` | `p008` | `p008-L001` | `L001` | 8불균형 수송문제 |
| `ex_DM_PDF06.machine_assignment` | `ev_deep_DM_PDF06_example_machine_assignment` | `DM_PDF06` | `p015` | `p015-L007` | `L007` | 하는가? 수송문제로 모형화 |
| `ex_DM_PDF06.transshipment_min_cost` | `ev_deep_DM_PDF06_example_transshipment_min_cost` | `DM_PDF06` | `p017` | `p017-L002` | `L002` | [예제 5.2] 농산물 유통의 경유 수송문제 |
| `ex_DM_PDF06.ready_mix_flow` | `ev_deep_DM_PDF06_example_ready_mix_flow` | `DM_PDF06` | `p027` | `p027-L002` | `L002` | [예제5.6] 레미콘 믹서의 흐름배치 문제 |

## 16. QC / Extraction Risk Notes

- **page_count:** 36
- **low_text_pages:** 9
- **extraction_risk_pages:** 9
- **QC policy:** 표, 그림, 수식 이미지가 많은 페이지는 전사 텍스트만으로 숫자를 단정하지 않는다. 튜터는 수식 구조와 증거 anchor를 우선 제시하고, 숫자 최적해는 필요 시 원본 PDF를 대조한다.
- 페이지 6, 7, 20, 21, 24, 34 등은 표/그림 OCR 누락 가능성이 있어 숫자 최적해는 원본 대조가 필요하다.
