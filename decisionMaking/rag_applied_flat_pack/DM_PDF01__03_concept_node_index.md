# DM_PDF01 — concept node index

**title:** Ch.4 심플렉스 타블로 보완과 2단계법
**graph_location:** 6강 보완: 표준형과 BFS를 타블로 피벗, 특수 종료, 2단계법으로 완성하는 구간

## Nodes

| node_id | label | term | prerequisite | follow-up | analogous |
|---|---|---|---|---|---|
| `n_DM_PDF01.simplex_tableau` | 심플렉스 타블로 | simplex tableau | 표준형과 정규형 | minimum ratio test와 pivot | Solver의 반복 계산 로그 |
| `n_DM_PDF01.multiple_optima` | 복수 최적해 | multiple optimal solutions | 최적성 판정 | 민감도 분석의 대체 최적/허용범위 | 그래프 해법의 등위선 평행 접촉 |
| `n_DM_PDF01.unbounded_solution` | 비유계 | unbounded solution | minimum ratio test | 모형 검증과 제약 누락 진단 | 그래프에서 열린 가능영역 |
| `n_DM_PDF01.two_phase_method` | 2단계법 | two-phase method | surplus/artificial variable | Big-M method와 duality | Big-M의 penalty 방식 |

## Local Edges

- `e_DM_PDF01_simplex_tableau_to_multiple_optima`: `n_DM_PDF01.simplex_tableau` --leads_to--> `n_DM_PDF01.multiple_optima`
- `e_DM_PDF01_multiple_optima_to_unbounded_solution`: `n_DM_PDF01.multiple_optima` --leads_to--> `n_DM_PDF01.unbounded_solution`
- `e_DM_PDF01_unbounded_solution_to_two_phase_method`: `n_DM_PDF01.unbounded_solution` --leads_to--> `n_DM_PDF01.two_phase_method`
