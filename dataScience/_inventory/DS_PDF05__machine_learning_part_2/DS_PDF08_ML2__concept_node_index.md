# DS_PDF08_ML2 — concept node index

## Graph location

지도학습 알고리즘의 기하학적 해석 계층.

| node_id | label | gate | prerequisites | followups | evidence |
|---|---|---|---|---|---|
| `n_DS_ML2.svm_margin_hyperplane` | SVM margin/hyperplane | Gate 5 알고리즘 심화 | `n_DS_ML1.classification_regression` | `n_DS_ML2.support_vectors`, `n_DS_ML2.kernel_trick` | `DS_PDF08_ML2:p006:L004` |
| `n_DS_ML2.support_vectors` | Support vectors | Gate 5 알고리즘 심화 | `n_DS_ML2.svm_margin_hyperplane` | `n_DS_ML2.kernel_trick` | `DS_PDF08_ML2:p005:L004` |
| `n_DS_ML2.kernel_trick` | Kernel trick | Gate 5 알고리즘 심화 | `n_DS_ML2.svm_margin_hyperplane`, `n_DS_ML2.scaling_distance_models` | `n_DS_ML3.pca_dimensionality_reduction` | `DS_PDF08_ML2:p009:L004` |
| `n_DS_ML2.knn_vote` | kNN 이웃 투표 | Gate 5 알고리즘 심화 | `n_DS_ML1.classification_regression`, `n_DS_ML2.distance_metrics` | `n_DS_ML2.k_selection_bias_variance` | `DS_PDF08_ML2:p012:L004` |
| `n_DS_ML2.distance_metrics` | 거리 척도 | Gate 5 알고리즘 심화 | `n_DS_VIS.scatter_correlation` | `n_DS_ML2.scaling_distance_models`, `n_DS_ML3.kmeans_distance_metrics` | `DS_PDF08_ML2:p016:L004` |
| `n_DS_ML2.scaling_distance_models` | Scaling과 거리 기반 모델 | Gate 5 알고리즘 심화 | `n_DS_ML2.distance_metrics`, `n_DS_ML1.train_test_generalization` | `n_DS_ML2.knn_vote`, `n_DS_ML3.kmeans_centroid_loop` | `DS_PDF08_ML2:p017:L004` |
| `n_DS_ML2.k_selection_bias_variance` | k 선택과 bias-variance | Gate 5 알고리즘 심화 | `n_DS_ML2.knn_vote` | `n_DS_ML3.silhouette_score` | `DS_PDF08_ML2:p021:L004` |
| `n_DS_ML2.decision_tree_impurity` | Decision tree와 impurity | Gate 5 알고리즘 심화 | `n_DS_ML1.classification_regression`, `n_DS_ML1.loss_metric` | `n_DS_ML3.kmeanspp_local_optimum` | `DS_PDF08_ML2:p025:L004` |

## Visual anchors

- `DS_PDF08_ML2:p004` SVM margin과 결정경계 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p004__svm_margin.png`
- `DS_PDF08_ML2:p005` support vector와 margin 결정 관측치 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p005__support_vectors.png`
- `DS_PDF08_ML2:p006` 최대 margin hyperplane -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p006__optimal_hyperplane.png`
- `DS_PDF08_ML2:p009` 비선형 SVM과 kernel 함수 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p009__kernel_svm.png`
- `DS_PDF08_ML2:p016` kNN 거리 척도 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p016__knn_distance_metrics.png`
- `DS_PDF08_ML2:p017` 거리 기반 모델의 scale 민감도 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p017__knn_scaling.png`
- `DS_PDF08_ML2:p019` kNN 분류/회귀 사용 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p019__knn_classification_regression.png`
- `DS_PDF08_ML2:p021` majority voting 문제점 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p021__knn_majority_voting.png`
