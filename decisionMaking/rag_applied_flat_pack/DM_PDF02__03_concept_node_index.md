# DM_PDF02 — concept node index

**title:** Ch.5 민감도 분석
**graph_location:** 7강 쌍대/민감도 이후: 최적해가 입력 변화에 얼마나 안정적인지 읽는 구간

## Nodes

| node_id | label | term | prerequisite | follow-up | analogous |
|---|---|---|---|---|---|
| `n_DM_PDF02.sensitivity_analysis` | 민감도 분석 | sensitivity analysis | 최적 타블로와 binding constraint | 수송문제의 비용/공급 변화 분석 | 쌍대변수의 경제적 의미 |
| `n_DM_PDF02.shadow_price` | 잠재가격 | shadow price | binding/nonbinding constraint | 쌍대 최적해 | 경제학의 한계가치 |
| `n_DM_PDF02.reduced_cost` | 감소비용 | reduced cost | 쌍대가격과 목적계수 | 대안 최적해 판정 | 타블로의 목적행 계수 |

## Local Edges

- `e_DM_PDF02_sensitivity_analysis_to_shadow_price`: `n_DM_PDF02.sensitivity_analysis` --leads_to--> `n_DM_PDF02.shadow_price`
- `e_DM_PDF02_shadow_price_to_reduced_cost`: `n_DM_PDF02.shadow_price` --leads_to--> `n_DM_PDF02.reduced_cost`
