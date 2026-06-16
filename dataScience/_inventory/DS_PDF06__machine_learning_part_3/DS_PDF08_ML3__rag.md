# DS_PDF08_ML3 — RAG tutor source

## Retrieval Routing Table

| route | when to use | primary files |
|---|---|---|
| `DS_PDF08_ML3` | 군집은 target 없이 구조를 찾고, 연관분석은 거래 안 동시출현 규칙을 support/confidence/lift로 평가한다. | `__01_pdf_transcript`, `__02_rawdata_develop`, `__03_concept_node_index`, this `__04_rag` |

## Core Concept Node Cards

### `n_DS_ML3.clustering_problem` — Clustering 문제정의

- 정의: target 없이 관측치들 사이의 유사성으로 묶음을 찾는 비지도학습 문제다.
- 직관: 정답 이름표 없이 데이터가 자연스럽게 모이는 방을 찾는다.
- 수식/절차: input X only -> similarity/distance -> cluster labels
- pandas/sklearn 언어: KMeans.fit_predict(X), clustering labels
- 오답위험: cluster label을 실제 class label처럼 곧바로 해석하는 오류.
- 연결: 선행 n_DS_ML1.learning_types, n_DS_ML2.distance_metrics / 후속 n_DS_ML3.kmeans_centroid_loop / 유사 -
- source trace: `DS_PDF08_ML3:p002:L004`, `ev_DS_PDF08_ML3_001`

### `n_DS_ML3.kmeans_centroid_loop` — k-means centroid loop

- 정의: 각 점을 가장 가까운 centroid에 배정하고, 각 군집 평균으로 centroid를 갱신하는 반복 알고리즘이다.
- 직관: 중심을 놓고 점을 배정한 뒤, 다시 중심을 옮기는 과정을 멈출 때까지 반복한다.
- 수식/절차: assign x_i to nearest mu_j -> update mu_j = mean(points in cluster j) -> repeat
- pandas/sklearn 언어: KMeans(n_clusters=k, init='k-means++').fit(X)
- 오답위험: centroid가 반드시 실제 데이터 점이라고 오해하는 오류.
- 연결: 선행 n_DS_ML3.clustering_problem, n_DS_ML2.scaling_distance_models / 후속 n_DS_ML3.kmeanspp_local_optimum, n_DS_ML3.silhouette_score / 유사 -
- source trace: `DS_PDF08_ML3:p005:L004`, `ev_DS_PDF08_ML3_002`

### `n_DS_ML3.kmeans_distance_metrics` — k-means 거리 척도

- 정의: k-means에서 가까움을 정의하는 Euclidean/cosine/p-norm 계열의 거리 선택 문제다.
- 직관: 무엇을 비슷하다고 볼지 정하는 군집의 언어다.
- 수식/절차: Euclidean norm, cosine similarity, p-norm variants
- pandas/sklearn 언어: sklearn KMeans는 기본 Euclidean, cosine은 별도 spherical 접근 필요
- 오답위험: scikit-learn KMeans에서 metric만 바꾸면 cosine k-means가 된다고 착각하는 오류.
- 연결: 선행 n_DS_ML2.distance_metrics / 후속 n_DS_LLM.embedding_contextual_representation / 유사 -
- source trace: `DS_PDF08_ML3:p016:L004`, `ev_DS_PDF08_ML3_003`

### `n_DS_ML3.kmeanspp_local_optimum` — k-means++와 local optimum

- 정의: k-means는 초기 centroid에 따라 지역 최적해에 수렴할 수 있어 k-means++로 좋은 초기점을 고른다.
- 직관: 처음 중심을 어디에 놓느냐가 최종 방 배치를 바꿀 수 있다.
- 수식/절차: repeat with different seeds; k-means++ spreads initial centroids apart
- pandas/sklearn 언어: KMeans(init='k-means++', n_init='auto', random_state=...)
- 오답위험: 한 번 실행한 군집 결과를 전역 최적해로 단정하는 오류.
- 연결: 선행 n_DS_ML3.kmeans_centroid_loop, n_DS_CODE.reproducible_random_state / 후속 n_DS_ML3.silhouette_score / 유사 -
- source trace: `DS_PDF08_ML3:p020:L004`, `ev_DS_PDF08_ML3_004`

### `n_DS_ML3.silhouette_score` — Silhouette score

- 정의: 한 점이 자기 군집에는 얼마나 가깝고 다른 군집과는 얼마나 떨어져 있는지 비교하는 군집 품질 지표다.
- 직관: 같은 방 안에서는 가까운지, 옆방과는 충분히 떨어졌는지 보는 점수다.
- 수식/절차: s = (b - a) / max(a, b); a=intra-cluster distance, b=nearest other-cluster distance
- pandas/sklearn 언어: silhouette_score(X, labels, metric='euclidean')
- 오답위험: silhouette이 높으면 항상 비즈니스적으로 좋은 군집이라고 단정하는 오류.
- 연결: 선행 n_DS_ML3.kmeanspp_local_optimum / 후속 n_DS_ML3.pca_dimensionality_reduction / 유사 -
- source trace: `DS_PDF08_ML3:p021:L004`, `ev_DS_PDF08_ML3_005`

### `n_DS_ML3.association_rule` — 연관 규칙

- 정의: 거래 데이터에서 A가 발생할 때 B가 함께 발생하는 패턴을 if-then 규칙으로 표현하는 방법이다.
- 직관: 장바구니 안에서 같이 등장하는 항목 조합을 규칙으로 찾는다.
- 수식/절차: X -> Y over transactions; evaluate by support, confidence, lift
- pandas/sklearn 언어: mlxtend frequent_patterns or custom crosstab over itemsets
- 오답위험: 동시출현 규칙을 인과관계로 해석하는 오류.
- 연결: 선행 n_DS_STATS.contingency_table / 후속 n_DS_ML3.support_confidence_lift / 유사 -
- source trace: `DS_PDF08_ML3:p033:L004`, `ev_DS_PDF08_ML3_006`

### `n_DS_ML3.support_confidence_lift` — Support/Confidence/Lift

- 정의: support는 규칙 항목이 전체 거래에서 나타난 비율, confidence는 조건 발생 시 결과 발생 비율, lift는 독립 대비 동시출현 강도다.
- 직관: 자주 나오나, 조건이 믿을 만한가, 우연보다 강한가를 분리해서 묻는다.
- 수식/절차: support(X->Y)=P(X∩Y), confidence=P(Y|X), lift=P(X∩Y)/(P(X)P(Y))
- pandas/sklearn 언어: itemset counts -> support/confidence/lift table
- 오답위험: confidence가 높아도 Y가 원래 흔하면 의미를 과대평가하는 오류.
- 연결: 선행 n_DS_ML3.association_rule, n_DS_STATS.conditional_independence / 후속 n_DS_LLM.rag_grounding / 유사 -
- source trace: `DS_PDF08_ML3:p035:L004`, `ev_DS_PDF08_ML3_007`

### `n_DS_ML3.pca_dimensionality_reduction` — PCA/차원축소

- 정의: 상관된 여러 feature를 분산이 큰 직교 축으로 변환해 저차원 표현을 만드는 기법이다.
- 직관: 많은 변수를 정보 손실을 관리하며 몇 개의 축으로 압축하는 표현 변환이다.
- 수식/절차: center X -> covariance/SVD -> principal components -> transformed coordinates
- pandas/sklearn 언어: PCA(n_components=...), fit_transform, explained_variance_ratio_
- 오답위험: PCA를 target을 맞히는 예측 모델로 오해하거나 scale 없이 적용하는 오류.
- 연결: 선행 n_DS_ML2.scaling_distance_models, n_DS_ML3.kmeans_distance_metrics / 후속 n_DS_LLM.embedding_contextual_representation / 유사 -
- source trace: `WEB:web_sklearn_pca`, `ev_DS_PDF08_ML3_008`

## Visual Example Cards

- `kmeans_problem`: 거리 기반 k-means 군집 문제 / anchor `DS_PDF08_ML3:p005:L001` / image `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p005__kmeans_problem.png`
- `spherical_kmeans`: cosine 기반 spherical k-means / anchor `DS_PDF08_ML3:p016:L001` / image `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p016__spherical_kmeans.png`
- `euclidean_cosine`: Euclidean distance와 cosine similarity / anchor `DS_PDF08_ML3:p017:L001` / image `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p017__euclidean_cosine.png`
- `kmeans_limitations`: initial point와 k-means++ / anchor `DS_PDF08_ML3:p020:L001` / image `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p020__kmeans_limitations.png`
- `association_metrics`: support/confidence/lift 평가 기준 / anchor `DS_PDF08_ML3:p035:L001` / image `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p035__association_metrics.png`
- `support_formula`: support 정의 / anchor `DS_PDF08_ML3:p036:L001` / image `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p036__support_formula.png`
- `confidence_formula`: confidence 정의 / anchor `DS_PDF08_ML3:p037:L001` / image `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p037__confidence_formula.png`
- `lift_formula`: lift 정의 / anchor `DS_PDF08_ML3:p038:L001` / image `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p038__lift_formula.png`
- `association_example`: support/confidence/lift 계산 예제 / anchor `DS_PDF08_ML3:p042:L001` / image `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p042__association_example.png`

## Code Mapping

- row = observation, column = variable, feature matrix = `X`, target vector = `y`.
- `fit` = 학습, `predict` = 추론, `transform` = 표현 변환, `metric` = 평가 함수.
- 시각화/통계 노드는 pandas 집계와 plot으로, ML 노드는 sklearn estimator/pipeline으로, LLM 노드는 tokenizer/embedding/retrieval로 매핑한다.

## Misconception Bank

- Clustering 문제정의: cluster label을 실제 class label처럼 곧바로 해석하는 오류.
- k-means centroid loop: centroid가 반드시 실제 데이터 점이라고 오해하는 오류.
- k-means 거리 척도: scikit-learn KMeans에서 metric만 바꾸면 cosine k-means가 된다고 착각하는 오류.
- k-means++와 local optimum: 한 번 실행한 군집 결과를 전역 최적해로 단정하는 오류.
- Silhouette score: silhouette이 높으면 항상 비즈니스적으로 좋은 군집이라고 단정하는 오류.
- 연관 규칙: 동시출현 규칙을 인과관계로 해석하는 오류.
- Support/Confidence/Lift: confidence가 높아도 Y가 원래 흔하면 의미를 과대평가하는 오류.
- PCA/차원축소: PCA를 target을 맞히는 예측 모델로 오해하거나 scale 없이 적용하는 오류.

## Web Grounding Notes

- `web_sklearn_kmeans` scikit-learn K-means: https://scikit-learn.org/stable/modules/clustering.html#k-means — K-means objective, inertia, k-means++ initialization, PCA-before-kmeans caveat.
- `web_sklearn_silhouette` sklearn.metrics.silhouette_score: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html — Silhouette formula and score interpretation.
- `web_agrawal_srikant_1994` Fast Algorithms for Mining Association Rules: https://www.vldb.org/conf/1994/P487.PDF — Association-rule formalization and Apriori lineage.
- `web_sklearn_pca` scikit-learn PCA: https://scikit-learn.org/stable/modules/decomposition.html#pca — PCA as dimensionality reduction, not a predictive model.

## Source Trace Table

| node_id | evidence_id | transcript_anchor | snippet |
|---|---|---|---|
| `n_DS_ML3.clustering_problem` | `ev_DS_PDF08_ML3_001` | `DS_PDF08_ML3:p002:L004` | Introduction to ClusteringClustering군집화(Clustering)는 데이터 안에서 서로 비슷한 특성을 가진 객체들을 하나의 그룹 혹은 군집(cluster)으로 묶는 기법군집화에서는 각 객체가 어떤 그룹에 속해야 하는지에 대한정답 레이블(y)이 존재하지 않기 때문에, 비지도 학습(unsupe... |
| `n_DS_ML3.kmeans_centroid_loop` | `ev_DS_PDF08_ML3_002` | `DS_PDF08_ML3:p005:L004` | 𝒌-means clustering𝑛개의 데이터가 주어졌을 때, 두 데이터𝑥!와𝑥"사이의 유사성을 측정하기 위해Cosine,Euclidean, 혹은 임의로 정의한 거리d(𝑥!𝑥")를 사용모든 데이터는k개의 군집으로 나누어진다고 가정하며, 각 군집은 하나의 대표값 벡터(centroid)를 가짐 |
| `n_DS_ML3.kmeans_distance_metrics` | `ev_DS_PDF08_ML3_003` | `DS_PDF08_ML3:p016:L004` | 𝒌-means clusteringSpherical 𝒌-means•Cosine similarity을 거리로 사용하는 𝑘–means•학습 방법은 앞서 설명한 방식과 동일, 거리 측정 기준만 변경 (거리 기준 변경으로도 결과가 확연히 달라짐)•scikit-learn 라이브러이 내 k-means 알고리즘의 거리 metric... |
| `n_DS_ML3.kmeanspp_local_optimum` | `ev_DS_PDF08_ML3_004` | `DS_PDF08_ML3:p020:L004` | 𝒌-means clusteringLimitations1.Initial points 에 따라 군집의 모양이 달라짐à좋은 initial points를 찾기 위해 k-means++ 사용à순차적으로 기존의 centroid에서 멀리 떨어진 점을 새로운 centroid로 선정 |
| `n_DS_ML3.silhouette_score` | `ev_DS_PDF08_ML3_005` | `DS_PDF08_ML3:p021:L004` | 𝒌-means clusteringLimitations2.적절한 군집의 개수 정의 필요à군집의 개수 k는 사용자가 직접 설정해야하는 hyper-parameteràSihlhouette score을 기반으로 군집화 품질의 척도를 계산집 |
| `n_DS_ML3.association_rule` | `ev_DS_PDF08_ML3_006` | `DS_PDF08_ML3:p033:L004` | Association Analysis연관성 분석활용-연관성 분석을 위해서는 연관 규칙 Association Rule을 찾아내야 함.Ø연관규칙: 특정 사건이 발생하였을 때 함께 발생되는 또 다른 사건의 규칙.-연관규칙을 알기 위해서는 -사건들이 여러 개 있어야 하며, -사건들 중 공통적으로 일어나는 사건들을 조합하여 ... |
| `n_DS_ML3.support_confidence_lift` | `ev_DS_PDF08_ML3_007` | `DS_PDF08_ML3:p035:L004` | Association Analysis연관성규칙-연관 규칙 평가 기준 : 지지도(support), 신뢰도(confidence), 향상도(lift)-규칙이라는 특성 상 많이 일어나지 않는 희박한 항목에 대해서는 그 규칙을 일반화하거나 신뢰할 수 없다는 단점-연관성을 일반화하거나 신뢰할 수 있는 판단 기준이 필요-연관 규... |
| `n_DS_ML3.pca_dimensionality_reduction` | `ev_DS_PDF08_ML3_008` | `WEB:web_sklearn_pca` | 강의 PDF 전사에서 직접 키워드가 약해 `web_sklearn_pca`를 확장 근거로 사용: PCA as dimensionality reduction, not a predictive model. |
