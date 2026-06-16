# DS_PDF08_ML3 — rawdata develop

## One-line source role

군집은 target 없이 구조를 찾고, 연관분석은 거래 안 동시출현 규칙을 support/confidence/lift로 평가한다.

## Source policy

- PDF raw: `dataScience/pdf_raw/[Lecture][DS][08][03] 머신러닝_Part_3.pdf`
- TXT raw transcript: `dataScience/txt_raw/DS_PDF06__machine_learning_part_3__full_transcript.txt`
- PDF page images are derived visual raw data, not a replacement for the PDF.
- 숫자·공식·최적값은 전사와 이미지가 충돌하면 원본 PDF 대조가 우선이다.

## Visual raw intake

- `DS_PDF08_ML3:p005:L001` kmeans_problem: 거리 기반 k-means 군집 문제 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p005__kmeans_problem.png`
- `DS_PDF08_ML3:p016:L001` spherical_kmeans: cosine 기반 spherical k-means -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p016__spherical_kmeans.png`
- `DS_PDF08_ML3:p017:L001` euclidean_cosine: Euclidean distance와 cosine similarity -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p017__euclidean_cosine.png`
- `DS_PDF08_ML3:p020:L001` kmeans_limitations: initial point와 k-means++ -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p020__kmeans_limitations.png`
- `DS_PDF08_ML3:p035:L001` association_metrics: support/confidence/lift 평가 기준 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p035__association_metrics.png`
- `DS_PDF08_ML3:p036:L001` support_formula: support 정의 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p036__support_formula.png`
- `DS_PDF08_ML3:p037:L001` confidence_formula: confidence 정의 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p037__confidence_formula.png`
- `DS_PDF08_ML3:p038:L001` lift_formula: lift 정의 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p038__lift_formula.png`
- `DS_PDF08_ML3:p042:L001` association_example: support/confidence/lift 계산 예제 -> `dataScience/visual_raw/DS_PDF08_ML3/DS_PDF08_ML3_p042__association_example.png`

## Deep rawdata development by node

### Clustering 문제정의

- 현재 노드: `n_DS_ML3.clustering_problem`
- 관련 파일: `DS_PDF08_ML3` / `DS_PDF06__machine_learning_part_3__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML3:p002:L004` / `ev_DS_PDF08_ML3_001`
- 한 줄 정의: target 없이 관측치들 사이의 유사성으로 묶음을 찾는 비지도학습 문제다.
- 쉬운 직관: 정답 이름표 없이 데이터가 자연스럽게 모이는 방을 찾는다.
- 수식/절차: input X only -> similarity/distance -> cluster labels
- 데이터프레임 구조: feature matrix만 사용하며 y는 없다.
- 코드 관점: KMeans.fit_predict(X), clustering labels
- 강의 예제 연결: ML Part 3는 k-means를 중심으로 비지도학습의 거리 기반 구조 탐색을 설명한다.
- 자주 하는 실수: cluster label을 실제 class label처럼 곧바로 해석하는 오류.
- 선행 노드: `n_DS_ML1.learning_types`, `n_DS_ML2.distance_metrics`
- 후속 노드: `n_DS_ML3.kmeans_centroid_loop`
- 유사 노드: -
- evidence snippet: Introduction to ClusteringClustering군집화(Clustering)는 데이터 안에서 서로 비슷한 특성을 가진 객체들을 하나의 그룹 혹은 군집(cluster)으로 묶는 기법군집화에서는 각 객체가 어떤 그룹에 속해야 하는지에 대한정답 레이블(y)이 존재하지 않기 때문에, 비지도 학습(unsupe...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### k-means centroid loop

- 현재 노드: `n_DS_ML3.kmeans_centroid_loop`
- 관련 파일: `DS_PDF08_ML3` / `DS_PDF06__machine_learning_part_3__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML3:p005:L004` / `ev_DS_PDF08_ML3_002`
- 한 줄 정의: 각 점을 가장 가까운 centroid에 배정하고, 각 군집 평균으로 centroid를 갱신하는 반복 알고리즘이다.
- 쉬운 직관: 중심을 놓고 점을 배정한 뒤, 다시 중심을 옮기는 과정을 멈출 때까지 반복한다.
- 수식/절차: assign x_i to nearest mu_j -> update mu_j = mean(points in cluster j) -> repeat
- 데이터프레임 구조: numeric scaled feature matrix가 입력이다.
- 코드 관점: KMeans(n_clusters=k, init='k-means++').fit(X)
- 강의 예제 연결: k-means PDF 초반은 거리와 centroid 기반 군집을 설명한다.
- 자주 하는 실수: centroid가 반드시 실제 데이터 점이라고 오해하는 오류.
- 선행 노드: `n_DS_ML3.clustering_problem`, `n_DS_ML2.scaling_distance_models`
- 후속 노드: `n_DS_ML3.kmeanspp_local_optimum`, `n_DS_ML3.silhouette_score`
- 유사 노드: -
- evidence snippet: 𝒌-means clustering𝑛개의 데이터가 주어졌을 때, 두 데이터𝑥!와𝑥"사이의 유사성을 측정하기 위해Cosine,Euclidean, 혹은 임의로 정의한 거리d(𝑥!𝑥")를 사용모든 데이터는k개의 군집으로 나누어진다고 가정하며, 각 군집은 하나의 대표값 벡터(centroid)를 가짐
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### k-means 거리 척도

- 현재 노드: `n_DS_ML3.kmeans_distance_metrics`
- 관련 파일: `DS_PDF08_ML3` / `DS_PDF06__machine_learning_part_3__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML3:p016:L004` / `ev_DS_PDF08_ML3_003`
- 한 줄 정의: k-means에서 가까움을 정의하는 Euclidean/cosine/p-norm 계열의 거리 선택 문제다.
- 쉬운 직관: 무엇을 비슷하다고 볼지 정하는 군집의 언어다.
- 수식/절차: Euclidean norm, cosine similarity, p-norm variants
- 데이터프레임 구조: feature scaling과 sparse/text representation 여부가 거리 선택을 바꾼다.
- 코드 관점: sklearn KMeans는 기본 Euclidean, cosine은 별도 spherical 접근 필요
- 강의 예제 연결: PDF는 spherical k-means와 Euclidean/Cosine 비교를 직접 다룬다.
- 자주 하는 실수: scikit-learn KMeans에서 metric만 바꾸면 cosine k-means가 된다고 착각하는 오류.
- 선행 노드: `n_DS_ML2.distance_metrics`
- 후속 노드: `n_DS_LLM.embedding_contextual_representation`
- 유사 노드: -
- evidence snippet: 𝒌-means clusteringSpherical 𝒌-means•Cosine similarity을 거리로 사용하는 𝑘–means•학습 방법은 앞서 설명한 방식과 동일, 거리 측정 기준만 변경 (거리 기준 변경으로도 결과가 확연히 달라짐)•scikit-learn 라이브러이 내 k-means 알고리즘의 거리 metric...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### k-means++와 local optimum

- 현재 노드: `n_DS_ML3.kmeanspp_local_optimum`
- 관련 파일: `DS_PDF08_ML3` / `DS_PDF06__machine_learning_part_3__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML3:p020:L004` / `ev_DS_PDF08_ML3_004`
- 한 줄 정의: k-means는 초기 centroid에 따라 지역 최적해에 수렴할 수 있어 k-means++로 좋은 초기점을 고른다.
- 쉬운 직관: 처음 중심을 어디에 놓느냐가 최종 방 배치를 바꿀 수 있다.
- 수식/절차: repeat with different seeds; k-means++ spreads initial centroids apart
- 데이터프레임 구조: random_state와 n_init으로 반복 안정성을 관리한다.
- 코드 관점: KMeans(init='k-means++', n_init='auto', random_state=...)
- 강의 예제 연결: limitations 페이지는 initial points 문제와 k-means++를 명시한다.
- 자주 하는 실수: 한 번 실행한 군집 결과를 전역 최적해로 단정하는 오류.
- 선행 노드: `n_DS_ML3.kmeans_centroid_loop`, `n_DS_CODE.reproducible_random_state`
- 후속 노드: `n_DS_ML3.silhouette_score`
- 유사 노드: -
- evidence snippet: 𝒌-means clusteringLimitations1.Initial points 에 따라 군집의 모양이 달라짐à좋은 initial points를 찾기 위해 k-means++ 사용à순차적으로 기존의 centroid에서 멀리 떨어진 점을 새로운 centroid로 선정
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Silhouette score

- 현재 노드: `n_DS_ML3.silhouette_score`
- 관련 파일: `DS_PDF08_ML3` / `DS_PDF06__machine_learning_part_3__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML3:p021:L004` / `ev_DS_PDF08_ML3_005`
- 한 줄 정의: 한 점이 자기 군집에는 얼마나 가깝고 다른 군집과는 얼마나 떨어져 있는지 비교하는 군집 품질 지표다.
- 쉬운 직관: 같은 방 안에서는 가까운지, 옆방과는 충분히 떨어졌는지 보는 점수다.
- 수식/절차: s = (b - a) / max(a, b); a=intra-cluster distance, b=nearest other-cluster distance
- 데이터프레임 구조: X와 cluster labels가 입력이며 label 수 조건을 확인한다.
- 코드 관점: silhouette_score(X, labels, metric='euclidean')
- 강의 예제 연결: PDF에 직접 없거나 약하게 나온 경우 scikit-learn 문서로 보강하는 평가 노드다.
- 자주 하는 실수: silhouette이 높으면 항상 비즈니스적으로 좋은 군집이라고 단정하는 오류.
- 선행 노드: `n_DS_ML3.kmeanspp_local_optimum`
- 후속 노드: `n_DS_ML3.pca_dimensionality_reduction`
- 유사 노드: -
- evidence snippet: 𝒌-means clusteringLimitations2.적절한 군집의 개수 정의 필요à군집의 개수 k는 사용자가 직접 설정해야하는 hyper-parameteràSihlhouette score을 기반으로 군집화 품질의 척도를 계산집
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 연관 규칙

- 현재 노드: `n_DS_ML3.association_rule`
- 관련 파일: `DS_PDF08_ML3` / `DS_PDF06__machine_learning_part_3__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML3:p033:L004` / `ev_DS_PDF08_ML3_006`
- 한 줄 정의: 거래 데이터에서 A가 발생할 때 B가 함께 발생하는 패턴을 if-then 규칙으로 표현하는 방법이다.
- 쉬운 직관: 장바구니 안에서 같이 등장하는 항목 조합을 규칙으로 찾는다.
- 수식/절차: X -> Y over transactions; evaluate by support, confidence, lift
- 데이터프레임 구조: row=transaction, columns/items=0/1 item presence
- 코드 관점: mlxtend frequent_patterns or custom crosstab over itemsets
- 강의 예제 연결: Association Analysis 페이지가 연관 규칙과 평가 기준을 설명한다.
- 자주 하는 실수: 동시출현 규칙을 인과관계로 해석하는 오류.
- 선행 노드: `n_DS_STATS.contingency_table`
- 후속 노드: `n_DS_ML3.support_confidence_lift`
- 유사 노드: -
- evidence snippet: Association Analysis연관성 분석활용-연관성 분석을 위해서는 연관 규칙 Association Rule을 찾아내야 함.Ø연관규칙: 특정 사건이 발생하였을 때 함께 발생되는 또 다른 사건의 규칙.-연관규칙을 알기 위해서는 -사건들이 여러 개 있어야 하며, -사건들 중 공통적으로 일어나는 사건들을 조합하여 ...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Support/Confidence/Lift

- 현재 노드: `n_DS_ML3.support_confidence_lift`
- 관련 파일: `DS_PDF08_ML3` / `DS_PDF06__machine_learning_part_3__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML3:p035:L004` / `ev_DS_PDF08_ML3_007`
- 한 줄 정의: support는 규칙 항목이 전체 거래에서 나타난 비율, confidence는 조건 발생 시 결과 발생 비율, lift는 독립 대비 동시출현 강도다.
- 쉬운 직관: 자주 나오나, 조건이 믿을 만한가, 우연보다 강한가를 분리해서 묻는다.
- 수식/절차: support(X->Y)=P(X∩Y), confidence=P(Y|X), lift=P(X∩Y)/(P(X)P(Y))
- 데이터프레임 구조: transaction-item matrix에서 itemset 빈도를 계산한다.
- 코드 관점: itemset counts -> support/confidence/lift table
- 강의 예제 연결: PDF 후반의 지지도/신뢰도/향상도 계산 예제가 이 노드의 수치 훈련 자료다.
- 자주 하는 실수: confidence가 높아도 Y가 원래 흔하면 의미를 과대평가하는 오류.
- 선행 노드: `n_DS_ML3.association_rule`, `n_DS_STATS.conditional_independence`
- 후속 노드: `n_DS_LLM.rag_grounding`
- 유사 노드: -
- evidence snippet: Association Analysis연관성규칙-연관 규칙 평가 기준 : 지지도(support), 신뢰도(confidence), 향상도(lift)-규칙이라는 특성 상 많이 일어나지 않는 희박한 항목에 대해서는 그 규칙을 일반화하거나 신뢰할 수 없다는 단점-연관성을 일반화하거나 신뢰할 수 있는 판단 기준이 필요-연관 규...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### PCA/차원축소

- 현재 노드: `n_DS_ML3.pca_dimensionality_reduction`
- 관련 파일: `DS_PDF08_ML3` / `DS_PDF06__machine_learning_part_3__full_transcript.txt`
- 근거 anchor: `WEB:web_sklearn_pca` / `ev_DS_PDF08_ML3_008`
- 한 줄 정의: 상관된 여러 feature를 분산이 큰 직교 축으로 변환해 저차원 표현을 만드는 기법이다.
- 쉬운 직관: 많은 변수를 정보 손실을 관리하며 몇 개의 축으로 압축하는 표현 변환이다.
- 수식/절차: center X -> covariance/SVD -> principal components -> transformed coordinates
- 데이터프레임 구조: numeric scaled feature matrix가 입력이며 explained variance를 확인한다.
- 코드 관점: PCA(n_components=...), fit_transform, explained_variance_ratio_
- 강의 예제 연결: PCA는 PDF 직접 핵심 노드가 약하므로 ML/EDA 확장 지식으로 보강한다.
- 자주 하는 실수: PCA를 target을 맞히는 예측 모델로 오해하거나 scale 없이 적용하는 오류.
- 선행 노드: `n_DS_ML2.scaling_distance_models`, `n_DS_ML3.kmeans_distance_metrics`
- 후속 노드: `n_DS_LLM.embedding_contextual_representation`
- 유사 노드: -
- evidence snippet: 강의 PDF 전사에서 직접 키워드가 약해 `web_sklearn_pca`를 확장 근거로 사용: PCA as dimensionality reduction, not a predictive model.
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?
