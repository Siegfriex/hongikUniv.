# DS_PDF08_ML1 — concept node index

## Graph location

통계/시각화에서 모델 선택으로 넘어가는 지도학습 입구.

| node_id | label | gate | prerequisites | followups | evidence |
|---|---|---|---|---|---|
| `n_DS_ML1.feature_target_structure` | X/y feature-target 구조 | Gate 4 지도학습 | `n_DS_CODE.dataframe_row_column` | `n_DS_ML1.classification_regression`, `n_DS_ML1.train_test_generalization` | `DS_PDF08_ML1:p045:L004` |
| `n_DS_ML1.learning_types` | 지도/비지도/강화학습 | Gate 4 지도학습 | `n_DS_ML1.feature_target_structure` | `n_DS_ML3.clustering_problem` | `DS_PDF08_ML1:p002:L005` |
| `n_DS_ML1.train_test_generalization` | Train/Test split과 일반화 | Gate 4 지도학습 | `n_DS_CODE.sklearn_workflow`, `n_DS_STATS.statistical_inference` | `n_DS_ML1.loss_metric`, `n_DS_ML2.scaling_distance_models` | `DS_PDF08_ML1:p002:L005` |
| `n_DS_ML1.preprocessing_leakage` | 전처리와 leakage | Gate 4 지도학습 | `n_DS_ML1.train_test_generalization`, `n_DS_STATS.bootstrap_imputation` | `n_DS_ML2.scaling_distance_models`, `n_DS_ML3.kmeans_centroid_loop` | `DS_PDF08_ML1:p002:L005` |
| `n_DS_ML1.classification_regression` | 분류와 회귀 | Gate 4 지도학습 | `n_DS_ML1.feature_target_structure` | `n_DS_ML2.svm_margin_hyperplane`, `n_DS_ML2.knn_vote` | `DS_PDF08_ML1:p034:L004` |
| `n_DS_ML1.loss_metric` | Loss/Cost와 평가 지표 | Gate 4 지도학습 | `n_DS_ML1.train_test_generalization` | `n_DS_ML2.svm_margin_hyperplane`, `n_DS_ML2.knn_vote`, `n_DS_ML2.decision_tree_impurity` | `DS_PDF08_ML1:p017:L005` |
| `n_DS_ML1.logistic_logit_probability` | 로지스틱 회귀와 logit | Gate 4 지도학습 | `n_DS_ML1.classification_regression`, `n_DS_STATS.probability_random_variable` | `n_DS_ML2.svm_margin_hyperplane` | `DS_PDF08_ML1:p043:L004` |
| `n_DS_ML1.text_vectorization_features` | 텍스트 벡터화 | Gate 4 지도학습 | `n_DS_ML1.feature_target_structure` | `n_DS_LLM.embedding_contextual_representation` | `DS_PDF08_ML1:p012:L004` |

## Visual anchors

- `DS_PDF08_ML1:p002` 머신러닝 정의와 학습 유형 도입 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p002__ml_intro.png`
- `DS_PDF08_ML1:p008` 지도/비지도/강화학습 비교 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p008__supervised_unsupervised.png`
- `DS_PDF08_ML1:p015` 학습/검증 데이터 구조 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p015__train_test_structure.png`
- `DS_PDF08_ML1:p041` 분류 문제 정의 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p041__classification_intro.png`
- `DS_PDF08_ML1:p047` 로지스틱 회귀 logit 구조 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p047__logistic_regression_logit.png`
- `DS_PDF08_ML1:p054` 다중분류 확장 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p054__multiclass_classification.png`
