# DS_PDF06_VIS — concept node index

## Graph location

통계적 분포 이해와 ML 모델링 사이에서 데이터 구조를 눈으로 검증하는 EDA 관문.

| node_id | label | gate | prerequisites | followups | evidence |
|---|---|---|---|---|---|
| `n_DS_VIS.chart_selection` | 변수 유형별 그래프 선택 | Gate 3 EDA/시각화 | - | `n_DS_VIS.histogram_kde`, `n_DS_VIS.scatter_correlation`, `n_DS_VIS.heatmap_multivariate` | `DS_PDF06_VIS:p002:L005` |
| `n_DS_VIS.histogram_kde` | 히스토그램과 KDE | Gate 3 EDA/시각화 | `n_DS_VIS.chart_selection` | `n_DS_STATS.frequency_histogram`, `n_DS_VIS.boxplot_iqr` | `DS_PDF06_VIS:p005:L006` |
| `n_DS_VIS.scatter_correlation` | 산점도와 관계 해석 | Gate 3 EDA/시각화 | `n_DS_VIS.chart_selection` | `n_DS_ML1.feature_target_structure`, `n_DS_ML2.distance_metrics` | `DS_PDF06_VIS:p006:L005` |
| `n_DS_VIS.scatterplot_matrix` | 산점도 행렬 | Gate 3 EDA/시각화 | `n_DS_VIS.scatter_correlation` | `n_DS_ML1.feature_target_structure` | `DS_PDF06_VIS:p007:L005` |
| `n_DS_VIS.bubble_plot` | 버블 플롯 | Gate 3 EDA/시각화 | `n_DS_VIS.scatter_correlation` | `n_DS_VIS.heatmap_multivariate` | `DS_PDF06_VIS:p008:L006` |
| `n_DS_VIS.boxplot_iqr` | 박스플롯/IQR/이상치 후보 | Gate 3 EDA/시각화 | `n_DS_STATS.frequency_histogram` | `n_DS_CODE.iris_scatter_boxplot`, `n_DS_ML1.preprocessing_leakage` | `DS_PDF06_VIS:p010:L005` |
| `n_DS_VIS.heatmap_multivariate` | 히트맵 | Gate 3 EDA/시각화 | `n_DS_VIS.chart_selection` | `n_DS_ML3.clustering_problem`, `n_DS_STATS.contingency_table` | `DS_PDF06_VIS:p012:L007` |

## Visual anchors

- `DS_PDF06_VIS:p002` 단변량/이변량/다변량과 변수 유형별 그래프 선택 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p002__chart_selection_map.png`
- `DS_PDF06_VIS:p005` 히스토그램을 부드럽게 해석하는 KDE/밀도 그래프 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p005__density_kde.png`
- `DS_PDF06_VIS:p006` 두 양적변수 관계와 상관 해석의 출발점 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p006__scatter_plot.png`
- `DS_PDF06_VIS:p007` 다변량 관계를 여러 산점도 격자로 보는 자료 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p007__scatterplot_matrix.png`
- `DS_PDF06_VIS:p008` 좌표에 세 번째 크기 변수를 추가하는 시각화 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p008__bubble_plot.png`
- `DS_PDF06_VIS:p010` 중앙값/IQR/이상치 후보를 한 번에 보는 그래프 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p010__box_plot.png`
- `DS_PDF06_VIS:p012` 행렬형 다변량 값과 군집 패턴을 색으로 보는 그래프 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p012__heatmap.png`
