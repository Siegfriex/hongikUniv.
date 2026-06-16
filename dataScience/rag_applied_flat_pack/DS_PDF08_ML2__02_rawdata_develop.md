# DS_PDF08_ML2 — rawdata develop

## One-line source role

SVM은 margin을 키우고, kNN은 거리 기반 이웃 투표로 예측한다. 둘 다 feature scaling과 거리 해석이 핵심이다.

## Source policy

- PDF raw: `dataScience/pdf_raw/[Lecture][DS][08][02] 머신러닝_Part_2 (1).pdf`
- TXT raw transcript: `dataScience/txt_raw/DS_PDF05__machine_learning_part_2__full_transcript.txt`
- PDF page images are derived visual raw data, not a replacement for the PDF.
- 숫자·공식·최적값은 전사와 이미지가 충돌하면 원본 PDF 대조가 우선이다.

## Visual raw intake

- `DS_PDF08_ML2:p004:L001` svm_margin: SVM margin과 결정경계 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p004__svm_margin.png`
- `DS_PDF08_ML2:p005:L001` support_vectors: support vector와 margin 결정 관측치 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p005__support_vectors.png`
- `DS_PDF08_ML2:p006:L001` optimal_hyperplane: 최대 margin hyperplane -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p006__optimal_hyperplane.png`
- `DS_PDF08_ML2:p009:L001` kernel_svm: 비선형 SVM과 kernel 함수 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p009__kernel_svm.png`
- `DS_PDF08_ML2:p016:L001` knn_distance_metrics: kNN 거리 척도 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p016__knn_distance_metrics.png`
- `DS_PDF08_ML2:p017:L001` knn_scaling: 거리 기반 모델의 scale 민감도 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p017__knn_scaling.png`
- `DS_PDF08_ML2:p019:L001` knn_classification_regression: kNN 분류/회귀 사용 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p019__knn_classification_regression.png`
- `DS_PDF08_ML2:p021:L001` knn_majority_voting: majority voting 문제점 -> `dataScience/visual_raw/DS_PDF08_ML2/DS_PDF08_ML2_p021__knn_majority_voting.png`

## Deep rawdata development by node

### SVM margin/hyperplane

- 현재 노드: `n_DS_ML2.svm_margin_hyperplane`
- 관련 파일: `DS_PDF08_ML2` / `DS_PDF05__machine_learning_part_2__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML2:p006:L004` / `ev_DS_PDF08_ML2_001`
- 한 줄 정의: SVM은 클래스 사이의 margin이 최대가 되는 hyperplane을 찾는 분류 알고리즘이다.
- 쉬운 직관: 두 집단 사이에 가능한 한 넓은 안전지대를 만드는 경계선을 찾는다.
- 수식/절차: maximize margin subject to correct/soft-margin classification constraints
- 데이터프레임 구조: 각 row는 feature 공간의 점이고 class label이 경계 학습에 쓰인다.
- 코드 관점: SVC(kernel='linear'), LinearSVC, decision_function
- 강의 예제 연결: ML Part 2 첫 SVM 페이지가 margin과 결정경계의 기하를 보여준다.
- 자주 하는 실수: SVM이 확률을 직접 예측한다고 보거나 margin과 accuracy를 같은 값으로 보는 오류.
- 선행 노드: `n_DS_ML1.classification_regression`
- 후속 노드: `n_DS_ML2.support_vectors`, `n_DS_ML2.kernel_trick`
- 유사 노드: -
- evidence snippet: Machine Learning BasicsSupport Vector Machine (SVM)-SVM은 margin이 최대화가 될 수 있는 초평면(오른쪽 그림의 optimal hyperplane, 판별경계)을 찾음
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Support vectors

- 현재 노드: `n_DS_ML2.support_vectors`
- 관련 파일: `DS_PDF08_ML2` / `DS_PDF05__machine_learning_part_2__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML2:p005:L004` / `ev_DS_PDF08_ML2_002`
- 한 줄 정의: 결정경계와 가장 가까워 margin 위치를 결정하는 관측치들이다.
- 쉬운 직관: 경계를 실제로 밀고 있는 핵심 점들이다.
- 수식/절차: support vectors lie on/inside margin and determine separating boundary
- 데이터프레임 구조: 일부 row가 boundary를 결정하는 큰 영향점을 가진다.
- 코드 관점: model.support_vectors_, support_
- 강의 예제 연결: SVM support vector 페이지는 margin 결정 관측치를 명시한다.
- 자주 하는 실수: 모든 관측치가 경계를 똑같이 결정한다고 보는 오류.
- 선행 노드: `n_DS_ML2.svm_margin_hyperplane`
- 후속 노드: `n_DS_ML2.kernel_trick`
- 유사 노드: -
- evidence snippet: Machine Learning BasicsSupport Vector Machine (SVM)-Margin의 결정에 영향을 끼치는 관측치들을 서포트 벡터(Support vectors)라고 함.-서포트 벡터는 분류 경계면과 가장 가까운 점들임
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Kernel trick

- 현재 노드: `n_DS_ML2.kernel_trick`
- 관련 파일: `DS_PDF08_ML2` / `DS_PDF05__machine_learning_part_2__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML2:p009:L004` / `ev_DS_PDF08_ML2_003`
- 한 줄 정의: 원래 공간에서 선형 분리가 어려운 데이터를 고차원 특징공간의 내적처럼 계산해 비선형 경계를 만드는 방법이다.
- 쉬운 직관: 직선으로 나누기 어려우면 공간을 접거나 펼쳐서 직선처럼 나누는 효과를 낸다.
- 수식/절차: K(x_i,x_j)=phi(x_i)^T phi(x_j), e.g. RBF/poly kernels
- 데이터프레임 구조: feature scale과 kernel parameter가 경계 복잡도를 좌우한다.
- 코드 관점: SVC(kernel='rbf'), gamma, C
- 강의 예제 연결: 비선형 SVM 페이지가 kernel을 사용한 비선형 결정경계를 보여준다.
- 자주 하는 실수: kernel을 데이터 전처리 없이 마법처럼 쓰면 된다고 보는 오류.
- 선행 노드: `n_DS_ML2.svm_margin_hyperplane`, `n_DS_ML2.scaling_distance_models`
- 후속 노드: `n_DS_ML3.pca_dimensionality_reduction`
- 유사 노드: -
- evidence snippet: Machine Learning Basics비선형 Support Vector Machine (SVM) àKernel 함수의 이용-낮은 차원(2차원)의 비선형 분류경계를 가진 데이터들이 있다면, 이입력벡터들을고차원의 특정공간으로사상(mapping)시킨 후 선형 모델로 변환함-입력 벡터들을 kernel 함수를 통해고차원공...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### kNN 이웃 투표

- 현재 노드: `n_DS_ML2.knn_vote`
- 관련 파일: `DS_PDF08_ML2` / `DS_PDF05__machine_learning_part_2__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML2:p012:L004` / `ev_DS_PDF08_ML2_004`
- 한 줄 정의: 새 관측치와 가장 가까운 k개 학습 관측치의 label을 기준으로 분류 또는 회귀를 수행한다.
- 쉬운 직관: 가까운 사례들이 무엇이었는지 보고 새 사례를 판단한다.
- 수식/절차: classification: majority vote among k nearest labels. regression: average neighbor targets.
- 데이터프레임 구조: 모든 feature가 거리 계산에 들어가므로 열의 스케일과 의미가 중요하다.
- 코드 관점: KNeighborsClassifier, KNeighborsRegressor, kneighbors
- 강의 예제 연결: kNN 페이지는 범주형 반응변수와 연속형 반응변수 모두에 쓰임을 설명한다.
- 자주 하는 실수: k를 정답처럼 고정하거나, class imbalance를 고려하지 않는 오류.
- 선행 노드: `n_DS_ML1.classification_regression`, `n_DS_ML2.distance_metrics`
- 후속 노드: `n_DS_ML2.k_selection_bias_variance`
- 유사 노드: -
- evidence snippet: Machine Learning Basicsk-nearest neighbor (k-NN)-지도학습 알고리즘-기초적이지만 중요한 분류기법(classification) 중 하나-패턴 인식(pattern recognition), 데이터마이닝, 침입 탐지 시스템(intrusion detection system) 등에 사용-주...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 거리 척도

- 현재 노드: `n_DS_ML2.distance_metrics`
- 관련 파일: `DS_PDF08_ML2` / `DS_PDF05__machine_learning_part_2__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML2:p016:L004` / `ev_DS_PDF08_ML2_005`
- 한 줄 정의: 두 관측치가 feature 공간에서 얼마나 가까운지 수치화하는 함수다.
- 쉬운 직관: 비슷함을 숫자로 재는 자다.
- 수식/절차: Euclidean, Manhattan, Minkowski, cosine distance/similarity
- 데이터프레임 구조: numeric columns가 같은 단위와 의미를 갖는지 확인해야 한다.
- 코드 관점: pairwise_distances, metric='euclidean'/'manhattan'/'cosine'
- 강의 예제 연결: kNN 거리 페이지와 k-means 거리 페이지가 같은 수학 언어를 공유한다.
- 자주 하는 실수: 단위가 큰 변수가 거리 전체를 지배하게 두는 오류.
- 선행 노드: `n_DS_VIS.scatter_correlation`
- 후속 노드: `n_DS_ML2.scaling_distance_models`, `n_DS_ML3.kmeans_distance_metrics`
- 유사 노드: -
- evidence snippet: Machine Learning Basicsk-nearest neighbor (k-NN)-거리•Euclidean distance•Manhattan distance•Minkowski distance•Correlation distance
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Scaling과 거리 기반 모델

- 현재 노드: `n_DS_ML2.scaling_distance_models`
- 관련 파일: `DS_PDF08_ML2` / `DS_PDF05__machine_learning_part_2__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML2:p017:L004` / `ev_DS_PDF08_ML2_006`
- 한 줄 정의: feature의 단위와 범위를 맞춰 거리·margin·gradient 계산이 특정 변수에 과도하게 끌리지 않게 하는 전처리다.
- 쉬운 직관: 센티미터와 원화를 같은 자로 재지 않도록 단위를 맞추는 과정이다.
- 수식/절차: z=(x-mean)/std or minmax scaling before distance-sensitive estimator
- 데이터프레임 구조: train set에 scaler를 fit하고 train/test에 transform한다.
- 코드 관점: StandardScaler, MinMaxScaler, Pipeline
- 강의 예제 연결: kNN scale 민감도 페이지는 변수 scale이 거리 결과를 바꾸는 위험을 보여준다.
- 자주 하는 실수: 전체 데이터로 scaler를 fit해 test 정보를 누수시키는 오류.
- 선행 노드: `n_DS_ML2.distance_metrics`, `n_DS_ML1.train_test_generalization`
- 후속 노드: `n_DS_ML2.knn_vote`, `n_DS_ML3.kmeans_centroid_loop`
- 유사 노드: -
- evidence snippet: Machine Learning Basicsk-nearest neighbor (k-NN)-kNN는 거리 기반으로 작동하는 알고리즘이므로 데이터에 대한 scale에 영향을 받음.-변수의 scale에 따라 상대적으로 가깝지만 거리가 훨씬 먼 것처럼 계산될 수 있기 때문에 scaling 작업 필요-Scaling 작업을 안하...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### k 선택과 bias-variance

- 현재 노드: `n_DS_ML2.k_selection_bias_variance`
- 관련 파일: `DS_PDF08_ML2` / `DS_PDF05__machine_learning_part_2__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML2:p021:L004` / `ev_DS_PDF08_ML2_007`
- 한 줄 정의: kNN의 k는 이웃 수로, 작으면 노이즈에 민감하고 크면 경계가 과도하게 매끈해진다.
- 쉬운 직관: 동네 몇 명의 의견을 들을지 정하는 문제다.
- 수식/절차: small k: low bias/high variance; large k: high bias/low variance
- 데이터프레임 구조: validation set/cross-validation으로 k 후보를 비교한다.
- 코드 관점: GridSearchCV over n_neighbors
- 강의 예제 연결: majority voting 문제점 페이지가 k와 class composition의 민감도를 암시한다.
- 자주 하는 실수: k를 홀수로만 고르면 문제가 해결된다고 보는 오류.
- 선행 노드: `n_DS_ML2.knn_vote`
- 후속 노드: `n_DS_ML3.silhouette_score`
- 유사 노드: -
- evidence snippet: Machine Learning Basicsk-nearest neighbor (k-NN) –Majority voting의 문제점-kNN은 영역안에 많은 것이 카테고리로 선택되는 시스템을 가짐-기본적으로 어떤 카테고리가 타 카테고리보다 많이 있다면 분류에 상당한 영향을 끼침-예를 들어, 남자 10명, 여자가 90명이라면...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Decision tree와 impurity

- 현재 노드: `n_DS_ML2.decision_tree_impurity`
- 관련 파일: `DS_PDF08_ML2` / `DS_PDF05__machine_learning_part_2__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML2:p025:L004` / `ev_DS_PDF08_ML2_008`
- 한 줄 정의: 의사결정나무는 feature 조건 질문을 반복해 target을 분리하고, 각 split은 impurity를 낮추는 방향으로 선택된다.
- 쉬운 직관: 스무고개식 질문으로 데이터를 점점 순수한 그룹으로 나누는 규칙 기반 모델이다.
- 수식/절차: choose split that maximizes impurity decrease; common criteria include gini impurity and entropy. Control overfitting with max_depth, min_samples_leaf, pruning-style constraints.
- 데이터프레임 구조: row는 규칙을 따라 leaf로 내려가고, leaf의 class 비율이 예측 근거가 된다.
- 코드 관점: DecisionTreeClassifier(max_depth=...), export_text, plot_tree
- 강의 예제 연결: ML2 PDF의 decision tree 페이지를 1차 근거로 두고, impurity/depth/pruning 실무 해석은 scikit-learn 문서로 보강한다.
- 자주 하는 실수: tree는 scaling 영향이 작다고 해서 depth/leaf 제약 없이 키워도 된다고 보는 오류.
- 선행 노드: `n_DS_ML1.classification_regression`, `n_DS_ML1.loss_metric`
- 후속 노드: `n_DS_ML3.kmeanspp_local_optimum`
- 유사 노드: `n_DS_ML2.svm_margin_hyperplane`, `n_DS_ML2.knn_vote`
- evidence snippet: Machine Learning Basics의사결정나무, Decision Tree-특정 기준(질문)에 따라 데이터를 구분하는 모델. -상위 노드로부터 하위 노드로 나무 구조를 형성하는 매 단계마다 번류변수와 분류기준값의 선택이 중요.각 노드마다 질문을 던지고 그 응답에 따라 가지를 쳐서 데이터를 분리.-데이터로부터 트...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?
