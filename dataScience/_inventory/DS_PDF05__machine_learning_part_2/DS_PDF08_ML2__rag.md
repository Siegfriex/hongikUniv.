# DS_PDF08_ML2 — RAG tutor source

## Retrieval Routing Table

| route | when to use | primary files |
|---|---|---|
| `DS_PDF08_ML2` | SVM은 margin을 키우고, kNN은 거리 기반 이웃 투표로 예측한다. 둘 다 feature scaling과 거리 해석이 핵심이다. | `__01_pdf_transcript`, `__02_rawdata_develop`, `__03_concept_node_index`, this `__04_rag` |

## Core Concept Node Cards

### `n_DS_ML2.svm_margin_hyperplane` — SVM margin/hyperplane

- 정의: SVM은 클래스 사이의 margin이 최대가 되는 hyperplane을 찾는 분류 알고리즘이다.
- 직관: 두 집단 사이에 가능한 한 넓은 안전지대를 만드는 경계선을 찾는다.
- 수식/절차: maximize margin subject to correct/soft-margin classification constraints
- pandas/sklearn 언어: SVC(kernel='linear'), LinearSVC, decision_function
- 오답위험: SVM이 확률을 직접 예측한다고 보거나 margin과 accuracy를 같은 값으로 보는 오류.
- 연결: 선행 n_DS_ML1.classification_regression / 후속 n_DS_ML2.support_vectors, n_DS_ML2.kernel_trick / 유사 -
- source trace: `DS_PDF08_ML2:p006:L004`, `ev_DS_PDF08_ML2_001`

### `n_DS_ML2.support_vectors` — Support vectors

- 정의: 결정경계와 가장 가까워 margin 위치를 결정하는 관측치들이다.
- 직관: 경계를 실제로 밀고 있는 핵심 점들이다.
- 수식/절차: support vectors lie on/inside margin and determine separating boundary
- pandas/sklearn 언어: model.support_vectors_, support_
- 오답위험: 모든 관측치가 경계를 똑같이 결정한다고 보는 오류.
- 연결: 선행 n_DS_ML2.svm_margin_hyperplane / 후속 n_DS_ML2.kernel_trick / 유사 -
- source trace: `DS_PDF08_ML2:p005:L004`, `ev_DS_PDF08_ML2_002`

### `n_DS_ML2.kernel_trick` — Kernel trick

- 정의: 원래 공간에서 선형 분리가 어려운 데이터를 고차원 특징공간의 내적처럼 계산해 비선형 경계를 만드는 방법이다.
- 직관: 직선으로 나누기 어려우면 공간을 접거나 펼쳐서 직선처럼 나누는 효과를 낸다.
- 수식/절차: K(x_i,x_j)=phi(x_i)^T phi(x_j), e.g. RBF/poly kernels
- pandas/sklearn 언어: SVC(kernel='rbf'), gamma, C
- 오답위험: kernel을 데이터 전처리 없이 마법처럼 쓰면 된다고 보는 오류.
- 연결: 선행 n_DS_ML2.svm_margin_hyperplane, n_DS_ML2.scaling_distance_models / 후속 n_DS_ML3.pca_dimensionality_reduction / 유사 -
- source trace: `DS_PDF08_ML2:p009:L004`, `ev_DS_PDF08_ML2_003`

### `n_DS_ML2.knn_vote` — kNN 이웃 투표

- 정의: 새 관측치와 가장 가까운 k개 학습 관측치의 label을 기준으로 분류 또는 회귀를 수행한다.
- 직관: 가까운 사례들이 무엇이었는지 보고 새 사례를 판단한다.
- 수식/절차: classification: majority vote among k nearest labels. regression: average neighbor targets.
- pandas/sklearn 언어: KNeighborsClassifier, KNeighborsRegressor, kneighbors
- 오답위험: k를 정답처럼 고정하거나, class imbalance를 고려하지 않는 오류.
- 연결: 선행 n_DS_ML1.classification_regression, n_DS_ML2.distance_metrics / 후속 n_DS_ML2.k_selection_bias_variance / 유사 -
- source trace: `DS_PDF08_ML2:p012:L004`, `ev_DS_PDF08_ML2_004`

### `n_DS_ML2.distance_metrics` — 거리 척도

- 정의: 두 관측치가 feature 공간에서 얼마나 가까운지 수치화하는 함수다.
- 직관: 비슷함을 숫자로 재는 자다.
- 수식/절차: Euclidean, Manhattan, Minkowski, cosine distance/similarity
- pandas/sklearn 언어: pairwise_distances, metric='euclidean'/'manhattan'/'cosine'
- 오답위험: 단위가 큰 변수가 거리 전체를 지배하게 두는 오류.
- 연결: 선행 n_DS_VIS.scatter_correlation / 후속 n_DS_ML2.scaling_distance_models, n_DS_ML3.kmeans_distance_metrics / 유사 -
- source trace: `DS_PDF08_ML2:p016:L004`, `ev_DS_PDF08_ML2_005`

### `n_DS_ML2.scaling_distance_models` — Scaling과 거리 기반 모델

- 정의: feature의 단위와 범위를 맞춰 거리·margin·gradient 계산이 특정 변수에 과도하게 끌리지 않게 하는 전처리다.
- 직관: 센티미터와 원화를 같은 자로 재지 않도록 단위를 맞추는 과정이다.
- 수식/절차: z=(x-mean)/std or minmax scaling before distance-sensitive estimator
- pandas/sklearn 언어: StandardScaler, MinMaxScaler, Pipeline
- 오답위험: 전체 데이터로 scaler를 fit해 test 정보를 누수시키는 오류.
- 연결: 선행 n_DS_ML2.distance_metrics, n_DS_ML1.train_test_generalization / 후속 n_DS_ML2.knn_vote, n_DS_ML3.kmeans_centroid_loop / 유사 -
- source trace: `DS_PDF08_ML2:p017:L004`, `ev_DS_PDF08_ML2_006`

### `n_DS_ML2.k_selection_bias_variance` — k 선택과 bias-variance

- 정의: kNN의 k는 이웃 수로, 작으면 노이즈에 민감하고 크면 경계가 과도하게 매끈해진다.
- 직관: 동네 몇 명의 의견을 들을지 정하는 문제다.
- 수식/절차: small k: low bias/high variance; large k: high bias/low variance
- pandas/sklearn 언어: GridSearchCV over n_neighbors
- 오답위험: k를 홀수로만 고르면 문제가 해결된다고 보는 오류.
- 연결: 선행 n_DS_ML2.knn_vote / 후속 n_DS_ML3.silhouette_score / 유사 -
- source trace: `DS_PDF08_ML2:p021:L004`, `ev_DS_PDF08_ML2_007`

### `n_DS_ML2.decision_tree_impurity` — Decision tree와 impurity

- 정의: 의사결정나무는 feature 조건 질문을 반복해 target을 분리하고, 각 split은 impurity를 낮추는 방향으로 선택된다.
- 직관: 스무고개식 질문으로 데이터를 점점 순수한 그룹으로 나누는 규칙 기반 모델이다.
- 수식/절차: choose split that maximizes impurity decrease; common criteria include gini impurity and entropy. Control overfitting with max_depth, min_samples_leaf, pruning-style constraints.
- pandas/sklearn 언어: DecisionTreeClassifier(max_depth=...), export_text, plot_tree
- 오답위험: tree는 scaling 영향이 작다고 해서 depth/leaf 제약 없이 키워도 된다고 보는 오류.
- 연결: 선행 n_DS_ML1.classification_regression, n_DS_ML1.loss_metric / 후속 n_DS_ML3.kmeanspp_local_optimum / 유사 n_DS_ML2.svm_margin_hyperplane, n_DS_ML2.knn_vote
- source trace: `DS_PDF08_ML2:p025:L004`, `ev_DS_PDF08_ML2_008`

## Visual Example Cards

- `svm_margin`: SVM margin과 결정경계 / anchor `DS_PDF08_ML2:p004:L001` / image `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p004__svm_margin.png`
- `support_vectors`: support vector와 margin 결정 관측치 / anchor `DS_PDF08_ML2:p005:L001` / image `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p005__support_vectors.png`
- `optimal_hyperplane`: 최대 margin hyperplane / anchor `DS_PDF08_ML2:p006:L001` / image `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p006__optimal_hyperplane.png`
- `kernel_svm`: 비선형 SVM과 kernel 함수 / anchor `DS_PDF08_ML2:p009:L001` / image `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p009__kernel_svm.png`
- `knn_distance_metrics`: kNN 거리 척도 / anchor `DS_PDF08_ML2:p016:L001` / image `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p016__knn_distance_metrics.png`
- `knn_scaling`: 거리 기반 모델의 scale 민감도 / anchor `DS_PDF08_ML2:p017:L001` / image `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p017__knn_scaling.png`
- `knn_classification_regression`: kNN 분류/회귀 사용 / anchor `DS_PDF08_ML2:p019:L001` / image `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p019__knn_classification_regression.png`
- `knn_majority_voting`: majority voting 문제점 / anchor `DS_PDF08_ML2:p021:L001` / image `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p021__knn_majority_voting.png`

## Code Mapping

- row = observation, column = variable, feature matrix = `X`, target vector = `y`.
- `fit` = 학습, `predict` = 추론, `transform` = 표현 변환, `metric` = 평가 함수.
- 시각화/통계 노드는 pandas 집계와 plot으로, ML 노드는 sklearn estimator/pipeline으로, LLM 노드는 tokenizer/embedding/retrieval로 매핑한다.

## Misconception Bank

- SVM margin/hyperplane: SVM이 확률을 직접 예측한다고 보거나 margin과 accuracy를 같은 값으로 보는 오류.
- Support vectors: 모든 관측치가 경계를 똑같이 결정한다고 보는 오류.
- Kernel trick: kernel을 데이터 전처리 없이 마법처럼 쓰면 된다고 보는 오류.
- kNN 이웃 투표: k를 정답처럼 고정하거나, class imbalance를 고려하지 않는 오류.
- 거리 척도: 단위가 큰 변수가 거리 전체를 지배하게 두는 오류.
- Scaling과 거리 기반 모델: 전체 데이터로 scaler를 fit해 test 정보를 누수시키는 오류.
- k 선택과 bias-variance: k를 홀수로만 고르면 문제가 해결된다고 보는 오류.
- Decision tree와 impurity: tree는 scaling 영향이 작다고 해서 depth/leaf 제약 없이 키워도 된다고 보는 오류.

## Web Grounding Notes

- `web_sklearn_svm` scikit-learn Support Vector Machines: https://scikit-learn.org/stable/modules/svm.html — SVM margin, hyperplane, kernel, classifier API mapping.
- `web_sklearn_neighbors` scikit-learn Nearest Neighbors: https://scikit-learn.org/stable/modules/neighbors.html — kNN distance/vote/radius-neighbor routing.
- `web_sklearn_preprocessing` scikit-learn preprocessing: https://scikit-learn.org/stable/modules/preprocessing.html — Scaling requirement for distance/gradient-sensitive estimators.
- `web_sklearn_tree` scikit-learn Decision Trees: https://scikit-learn.org/stable/modules/tree.html — Decision tree as supervised if-then rules, impurity reduction, max_depth/pruning-style overfitting control.

## Source Trace Table

| node_id | evidence_id | transcript_anchor | snippet |
|---|---|---|---|
| `n_DS_ML2.svm_margin_hyperplane` | `ev_DS_PDF08_ML2_001` | `DS_PDF08_ML2:p006:L004` | Machine Learning BasicsSupport Vector Machine (SVM)-SVM은 margin이 최대화가 될 수 있는 초평면(오른쪽 그림의 optimal hyperplane, 판별경계)을 찾음 |
| `n_DS_ML2.support_vectors` | `ev_DS_PDF08_ML2_002` | `DS_PDF08_ML2:p005:L004` | Machine Learning BasicsSupport Vector Machine (SVM)-Margin의 결정에 영향을 끼치는 관측치들을 서포트 벡터(Support vectors)라고 함.-서포트 벡터는 분류 경계면과 가장 가까운 점들임 |
| `n_DS_ML2.kernel_trick` | `ev_DS_PDF08_ML2_003` | `DS_PDF08_ML2:p009:L004` | Machine Learning Basics비선형 Support Vector Machine (SVM) àKernel 함수의 이용-낮은 차원(2차원)의 비선형 분류경계를 가진 데이터들이 있다면, 이입력벡터들을고차원의 특정공간으로사상(mapping)시킨 후 선형 모델로 변환함-입력 벡터들을 kernel 함수를 통해고차원공... |
| `n_DS_ML2.knn_vote` | `ev_DS_PDF08_ML2_004` | `DS_PDF08_ML2:p012:L004` | Machine Learning Basicsk-nearest neighbor (k-NN)-지도학습 알고리즘-기초적이지만 중요한 분류기법(classification) 중 하나-패턴 인식(pattern recognition), 데이터마이닝, 침입 탐지 시스템(intrusion detection system) 등에 사용-주... |
| `n_DS_ML2.distance_metrics` | `ev_DS_PDF08_ML2_005` | `DS_PDF08_ML2:p016:L004` | Machine Learning Basicsk-nearest neighbor (k-NN)-거리•Euclidean distance•Manhattan distance•Minkowski distance•Correlation distance |
| `n_DS_ML2.scaling_distance_models` | `ev_DS_PDF08_ML2_006` | `DS_PDF08_ML2:p017:L004` | Machine Learning Basicsk-nearest neighbor (k-NN)-kNN는 거리 기반으로 작동하는 알고리즘이므로 데이터에 대한 scale에 영향을 받음.-변수의 scale에 따라 상대적으로 가깝지만 거리가 훨씬 먼 것처럼 계산될 수 있기 때문에 scaling 작업 필요-Scaling 작업을 안하... |
| `n_DS_ML2.k_selection_bias_variance` | `ev_DS_PDF08_ML2_007` | `DS_PDF08_ML2:p021:L004` | Machine Learning Basicsk-nearest neighbor (k-NN) –Majority voting의 문제점-kNN은 영역안에 많은 것이 카테고리로 선택되는 시스템을 가짐-기본적으로 어떤 카테고리가 타 카테고리보다 많이 있다면 분류에 상당한 영향을 끼침-예를 들어, 남자 10명, 여자가 90명이라면... |
| `n_DS_ML2.decision_tree_impurity` | `ev_DS_PDF08_ML2_008` | `DS_PDF08_ML2:p025:L004` | Machine Learning Basics의사결정나무, Decision Tree-특정 기준(질문)에 따라 데이터를 구분하는 모델. -상위 노드로부터 하위 노드로 나무 구조를 형성하는 매 단계마다 번류변수와 분류기준값의 선택이 중요.각 노드마다 질문을 던지고 그 응답에 따라 가지를 쳐서 데이터를 분리.-데이터로부터 트... |
