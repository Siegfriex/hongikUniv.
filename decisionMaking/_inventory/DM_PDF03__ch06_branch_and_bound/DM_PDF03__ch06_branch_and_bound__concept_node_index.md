# DM_PDF03 — concept node index

**title:** Ch.6 분지한계법
**graph_location:** 정수계획 해법: LP 완화로 상한/하한을 만들고 정수 조건을 만족할 때까지 탐색하는 구간

## Nodes

| node_id | label | term | prerequisite | follow-up | analogous |
|---|---|---|---|---|---|
| `n_DM_PDF03.lp_relaxation` | LP 완화 | LP relaxation | LP feasible region | branching and bounding | 연속 최적해와 정수 격자점 |
| `n_DM_PDF03.bounding_strategy` | 한계전략 | bounding strategy | LP relaxation | branch pruning | 민감도 분석의 한계값 해석과는 다른 algorithmic bound |
| `n_DM_PDF03.branching_strategy` | 분지전략 | branching strategy | fractional LP optimum | node selection and pruning | 이진 변수의 include/exclude 분기 |

## Local Edges

- `e_DM_PDF03_lp_relaxation_to_bounding_strategy`: `n_DM_PDF03.lp_relaxation` --leads_to--> `n_DM_PDF03.bounding_strategy`
- `e_DM_PDF03_bounding_strategy_to_branching_strategy`: `n_DM_PDF03.bounding_strategy` --leads_to--> `n_DM_PDF03.branching_strategy`
