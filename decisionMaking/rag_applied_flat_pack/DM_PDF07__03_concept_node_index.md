# DM_PDF07 — concept node index

**title:** Ch.7 비선형계획
**graph_location:** LP/IP 이후 확장: 목적함수나 제약식이 선형이 아닐 때 Solver와 최적성 해석이 달라지는 구간

## Nodes

| node_id | label | term | prerequisite | follow-up | analogous |
|---|---|---|---|---|---|
| `n_DM_PDF07.nonlinear_programming` | 비선형계획 | nonlinear programming | LP formulation | local/global optimum | quadratic programming and separable programming |
| `n_DM_PDF07.local_global_optimum` | 지역 최적해와 전체 최적해 | local and global optimum | feasible region | multi-start and global search | LP의 꼭짓점 최적성과 대비 |
| `n_DM_PDF07.grg_solver` | GRG 비선형 해법 | GRG nonlinear solver | nonlinear objective | local optimum diagnostics | Solver Simplex LP와 Evolutionary 해법 |

## Local Edges

- `e_DM_PDF07_nonlinear_programming_to_local_global_optimum`: `n_DM_PDF07.nonlinear_programming` --leads_to--> `n_DM_PDF07.local_global_optimum`
- `e_DM_PDF07_local_global_optimum_to_grg_solver`: `n_DM_PDF07.local_global_optimum` --leads_to--> `n_DM_PDF07.grg_solver`
