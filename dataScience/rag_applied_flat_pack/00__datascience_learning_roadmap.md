# DataScience learning roadmap

핵심 문장: 데이터사이언스는 도구 사용법 암기가 아니라, 현실 질문을 데이터 단위, 변수, 분포, 시각화, 모델, 평가 지표, 해석, 의사결정으로 번역하고 그 수학적 의미와 실무적 의미를 동시에 검증하는 과정이다.

## Six-session priority

| 구간 | 회차 | 비중 | 역할 |
|---|---|---:|---|
| 압축 기반 | 1회차 | 15% | 통계·시각화·pandas를 지도학습 입력 구조로 연결 |
| 지도학습 핵심 | 2~5회차 | 70% | X/y, train/test, 회귀, 로지스틱, SVM, kNN, decision tree |
| 통합 정리 | 6회차 | 15% | k-means·PCA·LLM을 압축하고 전체 시험/노트북 프로젝트로 통합 |

## Session plan

| session | title | weight | role | notebook | key nodes |
|---|---|---:|---|---|---|
| 1회차 | 데이터사이언스 입력 구조 만들기 | 15% | 통계·시각화·pandas를 지도학습 입력 구조로 압축 | `DS_SESSION01_stats_eda_foundation.ipynb` | `n_DS_STATS.population_sample_parameter_statistic`<br>`n_DS_STATS.frequency_histogram`<br>`n_DS_CODE.dataframe_row_column`<br>`n_DS_VIS.chart_selection`<br>`n_DS_VIS.histogram_kde`<br>`n_DS_VIS.scatter_correlation`<br>`n_DS_VIS.boxplot_iqr`<br>`n_DS_VIS.heatmap_multivariate` |
| 2회차 | 지도학습 파이프라인과 metric | 15% | X/y, train/test, classification/regression, confusion matrix | `DS_SESSION02_03_supervised_pipeline_regression.ipynb` | `n_DS_ML1.feature_target_structure`<br>`n_DS_ML1.learning_types`<br>`n_DS_ML1.train_test_generalization`<br>`n_DS_ML1.preprocessing_leakage`<br>`n_DS_ML1.classification_regression`<br>`n_DS_ML1.loss_metric` |
| 3회차 | 선형회귀와 로지스틱 회귀 | 18% | 계수, 확률, odds/logit, threshold, precision/recall tradeoff | `DS_SESSION02_03_supervised_pipeline_regression.ipynb` | `n_DS_ML1.classification_regression`<br>`n_DS_ML1.logistic_logit_probability`<br>`n_DS_ML1.loss_metric`<br>`n_DS_ML1.preprocessing_leakage` |
| 4회차 | SVM 심화 | 18% | margin, support vector, soft margin, kernel, C/gamma, scaling | `DS_SESSION04_05_supervised_algorithms.ipynb` | `n_DS_ML2.svm_margin_hyperplane`<br>`n_DS_ML2.support_vectors`<br>`n_DS_ML2.kernel_trick`<br>`n_DS_ML2.scaling_distance_models` |
| 5회차 | kNN과 의사결정나무 | 19% | 거리 기반 vs 규칙 기반, scaling, k 선택, impurity/depth | `DS_SESSION04_05_supervised_algorithms.ipynb` | `n_DS_ML2.distance_metrics`<br>`n_DS_ML2.knn_vote`<br>`n_DS_ML2.k_selection_bias_variance`<br>`n_DS_ML2.decision_tree_impurity` |
| 6회차 | 통합 capstone | 15% | k-means/PCA/association/LLM 압축 + customer churn project | `DS_CAPSTONE_customer_supervised_learning.ipynb` | `n_DS_ML3.clustering_problem`<br>`n_DS_ML3.kmeans_centroid_loop`<br>`n_DS_ML3.kmeanspp_local_optimum`<br>`n_DS_ML3.silhouette_score`<br>`n_DS_ML3.pca_dimensionality_reduction`<br>`n_DS_ML3.support_confidence_lift`<br>`n_DS_LLM.sequence_probability`<br>`n_DS_LLM.foundation_instruction_tuning` |

## Common practice pattern

각 회차는 반드시 `큰 개념 지도 -> 손계산 1개 -> 코드 재현 1개 -> 오답로그 1개 -> 새 문제 변형 1개`를 포함한다.

## Fixed analysis spine

`business question -> unit -> row/column -> feature/target -> dtype -> preprocessing -> EDA -> model selection -> fit/predict -> metric -> interpretation -> limitation check`

## Global high-signal edges

- `n_DS_STATS.frequency_histogram` --supports--> `n_DS_VIS.histogram_kde`: 도수/상대도수 이해가 histogram/KDE 해석의 통계 기반이다.
- `n_DS_CODE.dataframe_row_column` --feeds--> `n_DS_VIS.chart_selection`: dtype과 변수 의미가 그래프 선택을 결정한다.
- `n_DS_VIS.scatter_correlation` --prepares--> `n_DS_ML1.feature_target_structure`: 관계 시각화가 feature/target 후보 탐색으로 이어진다.
- `n_DS_STATS.population_sample_parameter_statistic` --analogous_to--> `n_DS_ML1.train_test_generalization`: 표본으로 모집단을 추정하는 구조와 train으로 test 성능을 추정하는 구조가 닮아 있다.
- `n_DS_CODE.sklearn_workflow` --implements--> `n_DS_ML1.train_test_generalization`: sklearn API가 split-fit-predict-metric 절차를 실행한다.
- `n_DS_ML1.feature_target_structure` --routes_to--> `n_DS_ML1.classification_regression`: target 의미가 분류/회귀 라우팅을 결정한다.
- `n_DS_ML1.classification_regression` --extends_to_algorithm--> `n_DS_ML2.svm_margin_hyperplane`: SVM은 분류 문제의 margin 기반 알고리즘이다.
- `n_DS_ML2.distance_metrics` --operationalizes--> `n_DS_ML2.knn_vote`: kNN은 거리 척도로 이웃을 선택한다.
- `n_DS_ML1.loss_metric` --extends_to_algorithm--> `n_DS_ML2.decision_tree_impurity`: metric으로 평가하고 impurity로 split을 선택하는 tree 비교가 가능하다.
- `n_DS_ML2.decision_tree_impurity` --contrasts_with--> `n_DS_ML2.scaling_distance_models`: tree는 scaling 영향이 작지만 depth/leaf 제약이 중요하다.
- `n_DS_ML2.scaling_distance_models` --prerequisite--> `n_DS_ML3.kmeans_centroid_loop`: k-means도 거리 기반이라 scaling 영향을 받는다.
- `n_DS_ML2.distance_metrics` --shared_math--> `n_DS_ML3.kmeans_distance_metrics`: kNN과 k-means 모두 거리 정의가 결과를 바꾼다.
- `n_DS_ML3.kmeanspp_local_optimum` --validated_by--> `n_DS_ML3.silhouette_score`: 초기값과 k 선택의 결과를 silhouette로 점검한다.
- `n_DS_STATS.contingency_table` --prepares--> `n_DS_ML3.association_rule`: 분할표의 조건부 비율 사고가 association rule 평가로 확장된다.
- `n_DS_STATS.conditional_independence` --shared_formula--> `n_DS_ML3.support_confidence_lift`: lift는 독립 대비 동시출현 강도를 묻는다.
- `n_DS_STATS.conditional_independence` --shared_probability_language--> `n_DS_LLM.sequence_probability`: 언어모델의 다음 토큰 예측은 조건부확률 언어를 사용한다.
- `n_DS_ML1.text_vectorization_features` --extends--> `n_DS_LLM.embedding_contextual_representation`: 텍스트 벡터화가 embedding/문맥표현으로 깊어진다.
- `n_DS_ML3.kmeans_distance_metrics` --analogous_to--> `n_DS_LLM.embedding_contextual_representation`: embedding 공간에서도 거리/유사도 해석이 필요하다.
- `n_DS_LLM.foundation_instruction_tuning` --needs_grounding--> `n_DS_LLM.rag_grounding`: 지시 수행 능력은 근거 검색과 분리해 검증해야 한다.

## Node count

- total nodes: 52
- total edges: 64
