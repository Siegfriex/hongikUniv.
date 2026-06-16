# DS_PDF06_CODE — concept node index

## Graph location

시각화와 머신러닝을 실제 코드 절차로 실행하게 만드는 도구 계층.

| node_id | label | gate | prerequisites | followups | evidence |
|---|---|---|---|---|---|
| `n_DS_CODE.computing_thinking` | 컴퓨팅 사고 | Gate 2 Python/pandas/numpy | - | `n_DS_CODE.dataframe_row_column`, `n_DS_CODE.reproducible_random_state` | `DS_PDF06_CODE:p005:L008` |
| `n_DS_CODE.dataframe_row_column` | DataFrame 행/열 구조 | Gate 2 Python/pandas/numpy | `n_DS_CODE.computing_thinking` | `n_DS_ML1.feature_target_structure`, `n_DS_VIS.chart_selection` | `DS_PDF06_CODE:p013:L007` |
| `n_DS_CODE.iris_scatter_boxplot` | Iris 산점도/박스플롯 코드 | Gate 2 Python/pandas/numpy | `n_DS_CODE.dataframe_row_column` | `n_DS_VIS.scatter_correlation`, `n_DS_VIS.boxplot_iqr` | `DS_PDF06_CODE:p025:L006` |
| `n_DS_CODE.sklearn_workflow` | scikit-learn 기본 워크플로 | Gate 2 Python/pandas/numpy | `n_DS_CODE.dataframe_row_column` | `n_DS_ML1.train_test_generalization`, `n_DS_ML2.scaling_distance_models` | `DS_PDF06_CODE:p036:L013` |
| `n_DS_CODE.reproducible_random_state` | 재현성/random_state | Gate 2 Python/pandas/numpy | `n_DS_CODE.computing_thinking` | `n_DS_ML1.train_test_generalization`, `n_DS_ML3.kmeanspp_local_optimum` | `DS_PDF06_CODE:p036:L013` |

## Visual anchors

- `DS_PDF06_CODE:p011` 프로그래밍 언어와 절차적 문제 해결 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p011__programming_language.png`
- `DS_PDF06_CODE:p016` R 언어 특성과 통계 분석 도구 관점 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p016__r_language_intro.png`
- `DS_PDF06_CODE:p023` Iris 산점도 코드 예시 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p023__iris_scatter_code.png`
- `DS_PDF06_CODE:p025` Iris boxplot과 factor level 제어 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p025__iris_boxplot_code.png`
- `DS_PDF06_CODE:p036` scikit-learn 전처리/회귀/분류/군집/평가 소개 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p036__sklearn_intro.png`
- `DS_PDF06_CODE:p037` train/test와 예측 코드 흐름 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p037__train_test_plot.png`
