# DM_PDF04 — concept node index

**title:** Ch.6 정수계획 1주차
**graph_location:** LP 이후 확장: 변수의 값이 연속량이 아니라 개수/선택일 때 정수성을 모형에 넣는 구간

## Nodes

| node_id | label | term | prerequisite | follow-up | analogous |
|---|---|---|---|---|---|
| `n_DM_PDF04.integer_programming` | 정수계획 | integer programming | LP 일반형 | branch-and-bound | 0-1 binary model |
| `n_DM_PDF04.binary_variable` | 0-1 변수 | binary variable | decision variable | fixed-charge model and facility location | assignment problem의 행/열 0-1 구조 |
| `n_DM_PDF04.integer_solver_option` | Solver 정수 옵션 | integer Solver option | spreadsheet modeling | branch-and-bound performance | LP Solver와 evolutionary Solver |

## Local Edges

- `e_DM_PDF04_integer_programming_to_binary_variable`: `n_DM_PDF04.integer_programming` --leads_to--> `n_DM_PDF04.binary_variable`
- `e_DM_PDF04_binary_variable_to_integer_solver_option`: `n_DM_PDF04.binary_variable` --leads_to--> `n_DM_PDF04.integer_solver_option`
