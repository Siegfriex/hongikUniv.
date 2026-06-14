# DM_PDF08 — concept node index

**title:** Ch.6 정수계획 2주차: 0-1 응용 모형
**graph_location:** 정수계획 응용: 시설입지, 커버링, 고정비, 선택 논리를 0-1 변수로 표현하는 구간

## Nodes

| node_id | label | term | prerequisite | follow-up | analogous |
|---|---|---|---|---|---|
| `n_DM_PDF08.set_covering_model` | 집합커버링 모형 | set covering model | binary variable | facility location | assignment row/column sum structure |
| `n_DM_PDF08.facility_location` | 공공 설비 입지 선정 | facility location | 0-1 variable | fixed-charge and covering constraints | transportation/network service assignment |
| `n_DM_PDF08.coverage_matrix` | 도달 가능성 행렬 | coverage matrix | set covering model | coverage constraint | assignment matrix |

## Local Edges

- `e_DM_PDF08_set_covering_model_to_facility_location`: `n_DM_PDF08.set_covering_model` --leads_to--> `n_DM_PDF08.facility_location`
- `e_DM_PDF08_facility_location_to_coverage_matrix`: `n_DM_PDF08.facility_location` --leads_to--> `n_DM_PDF08.coverage_matrix`
