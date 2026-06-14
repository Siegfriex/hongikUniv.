# DM_PDF06 — concept node index

**title:** Ch.5 수송계획과 네트워크 분석
**graph_location:** LP 응용 확장: 일반 자원배분 모형이 네트워크 노드와 arc 흐름 구조로 특수화되는 구간

## Nodes

| node_id | label | term | prerequisite | follow-up | analogous |
|---|---|---|---|---|---|
| `n_DM_PDF06.transportation_problem` | 수송문제 | transportation problem | LP equality constraints | transshipment and min-cost flow | Big M 운송 예제 |
| `n_DM_PDF06.transshipment_problem` | 경유수송문제 | transshipment problem | transportation problem | minimum cost flow | flow conservation in networks |
| `n_DM_PDF06.assignment_problem` | 할당문제 | assignment problem | transportation problem | TSP and matching | Sellmore assignment |
| `n_DM_PDF06.network_flow` | 네트워크 흐름 | network flow | LP formulation | CPM/PERT and project networks | graph representation of constraints |

## Local Edges

- `e_DM_PDF06_transportation_problem_to_transshipment_problem`: `n_DM_PDF06.transportation_problem` --leads_to--> `n_DM_PDF06.transshipment_problem`
- `e_DM_PDF06_transshipment_problem_to_assignment_problem`: `n_DM_PDF06.transshipment_problem` --leads_to--> `n_DM_PDF06.assignment_problem`
- `e_DM_PDF06_assignment_problem_to_network_flow`: `n_DM_PDF06.assignment_problem` --leads_to--> `n_DM_PDF06.network_flow`
