# DS_PDF08_ML3 — concept node index

## Graph location

비지도학습과 패턴 발견을 묶는 구조 탐색 계층.

| node_id | label | gate | prerequisites | followups | evidence |
|---|---|---|---|---|---|
| `n_DS_ML3.clustering_problem` | Clustering 문제정의 | Gate 5 알고리즘 심화 | `n_DS_ML1.learning_types`, `n_DS_ML2.distance_metrics` | `n_DS_ML3.kmeans_centroid_loop` | `DS_PDF08_ML3:p002:L004` |
| `n_DS_ML3.kmeans_centroid_loop` | k-means centroid loop | Gate 5 알고리즘 심화 | `n_DS_ML3.clustering_problem`, `n_DS_ML2.scaling_distance_models` | `n_DS_ML3.kmeanspp_local_optimum`, `n_DS_ML3.silhouette_score` | `DS_PDF08_ML3:p005:L004` |
| `n_DS_ML3.kmeans_distance_metrics` | k-means 거리 척도 | Gate 5 알고리즘 심화 | `n_DS_ML2.distance_metrics` | `n_DS_LLM.embedding_contextual_representation` | `DS_PDF08_ML3:p016:L004` |
| `n_DS_ML3.kmeanspp_local_optimum` | k-means++와 local optimum | Gate 5 알고리즘 심화 | `n_DS_ML3.kmeans_centroid_loop`, `n_DS_CODE.reproducible_random_state` | `n_DS_ML3.silhouette_score` | `DS_PDF08_ML3:p020:L004` |
| `n_DS_ML3.silhouette_score` | Silhouette score | Gate 5 알고리즘 심화 | `n_DS_ML3.kmeanspp_local_optimum` | `n_DS_ML3.pca_dimensionality_reduction` | `DS_PDF08_ML3:p021:L004` |
| `n_DS_ML3.association_rule` | 연관 규칙 | Gate 5 알고리즘 심화 | `n_DS_STATS.contingency_table` | `n_DS_ML3.support_confidence_lift` | `DS_PDF08_ML3:p033:L004` |
| `n_DS_ML3.support_confidence_lift` | Support/Confidence/Lift | Gate 5 알고리즘 심화 | `n_DS_ML3.association_rule`, `n_DS_STATS.conditional_independence` | `n_DS_LLM.rag_grounding` | `DS_PDF08_ML3:p035:L004` |
| `n_DS_ML3.pca_dimensionality_reduction` | PCA/차원축소 | Gate 5 알고리즘 심화 | `n_DS_ML2.scaling_distance_models`, `n_DS_ML3.kmeans_distance_metrics` | `n_DS_LLM.embedding_contextual_representation` | `WEB:web_sklearn_pca` |

## Visual anchors

- `DS_PDF08_ML3:p005` 거리 기반 k-means 군집 문제 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p005__kmeans_problem.png`
- `DS_PDF08_ML3:p016` cosine 기반 spherical k-means -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p016__spherical_kmeans.png`
- `DS_PDF08_ML3:p017` Euclidean distance와 cosine similarity -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p017__euclidean_cosine.png`
- `DS_PDF08_ML3:p020` initial point와 k-means++ -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p020__kmeans_limitations.png`
- `DS_PDF08_ML3:p035` support/confidence/lift 평가 기준 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p035__association_metrics.png`
- `DS_PDF08_ML3:p036` support 정의 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p036__support_formula.png`
- `DS_PDF08_ML3:p037` confidence 정의 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p037__confidence_formula.png`
- `DS_PDF08_ML3:p038` lift 정의 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p038__lift_formula.png`
- `DS_PDF08_ML3:p042` support/confidence/lift 계산 예제 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p042__association_example.png`
