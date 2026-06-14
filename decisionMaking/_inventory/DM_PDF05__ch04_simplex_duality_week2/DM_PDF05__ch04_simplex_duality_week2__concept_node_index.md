# DM_PDF05 — concept node index

**title:** Ch.4 심플렉스, Big-M, 쌍대성 연결
**graph_location:** 6~7강 다리: 2단계법/Big-M으로 infeasible start를 처리하고 쌍대문제로 넘어가는 구간

## Nodes

| node_id | label | term | prerequisite | follow-up | analogous |
|---|---|---|---|---|---|
| `n_DM_PDF05.artificial_variable` | 인위변수 | artificial variable | surplus variable | Big-M and Phase I | slack variable과의 대비 |
| `n_DM_PDF05.big_m_method` | Big-M 방법 | Big-M method | artificial variable | dual problem and sensitivity | two-phase method |
| `n_DM_PDF05.min_to_max_conversion` | 최소화-최대화 변환 | min-to-max conversion | LP objective sense | Big-M sign convention | dual primal 방향 변환 |

## Local Edges

- `e_DM_PDF05_artificial_variable_to_big_m_method`: `n_DM_PDF05.artificial_variable` --leads_to--> `n_DM_PDF05.big_m_method`
- `e_DM_PDF05_big_m_method_to_min_to_max_conversion`: `n_DM_PDF05.big_m_method` --leads_to--> `n_DM_PDF05.min_to_max_conversion`
