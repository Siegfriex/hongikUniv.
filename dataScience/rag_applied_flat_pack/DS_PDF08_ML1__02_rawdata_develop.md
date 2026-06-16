# DS_PDF08_ML1 — rawdata develop

## One-line source role

현실 문제를 X/y 데이터 구조로 바꾸고, 분류/회귀/비지도학습과 학습·평가 절차를 판별한다.

## Source policy

- PDF raw: `dataScience/pdf_raw/[Lecture][DS][08][01] 머신러닝_Part_1 (2).pdf`
- TXT raw transcript: `dataScience/txt_raw/DS_PDF04__machine_learning_part_1__full_transcript.txt`
- PDF page images are derived visual raw data, not a replacement for the PDF.
- 숫자·공식·최적값은 전사와 이미지가 충돌하면 원본 PDF 대조가 우선이다.

## Visual raw intake

- `DS_PDF08_ML1:p002:L001` ml_intro: 머신러닝 정의와 학습 유형 도입 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p002__ml_intro.png`
- `DS_PDF08_ML1:p008:L001` supervised_unsupervised: 지도/비지도/강화학습 비교 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p008__supervised_unsupervised.png`
- `DS_PDF08_ML1:p015:L001` train_test_structure: 학습/검증 데이터 구조 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p015__train_test_structure.png`
- `DS_PDF08_ML1:p041:L001` classification_intro: 분류 문제 정의 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p041__classification_intro.png`
- `DS_PDF08_ML1:p047:L001` logistic_regression_logit: 로지스틱 회귀 logit 구조 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p047__logistic_regression_logit.png`
- `DS_PDF08_ML1:p054:L001` multiclass_classification: 다중분류 확장 -> `dataScience/visual_raw/DS_PDF08_ML1/DS_PDF08_ML1_p054__multiclass_classification.png`

## Deep rawdata development by node

### X/y feature-target 구조

- 현재 노드: `n_DS_ML1.feature_target_structure`
- 관련 파일: `DS_PDF08_ML1` / `DS_PDF04__machine_learning_part_1__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML1:p045:L004` / `ev_DS_PDF08_ML1_001`
- 한 줄 정의: feature matrix X와 target vector y로 예측 문제를 표현하는 데이터 구조다.
- 쉬운 직관: 무엇을 근거로 무엇을 맞힐지 분리하는 모델링의 시작점이다.
- 수식/절차: X = rows x features, y = label/target for each row
- 데이터프레임 구조: feature columns와 target column을 분리한다.
- 코드 관점: X = df[features]; y = df[target]
- 강의 예제 연결: ML Part 1은 classification/regression 모두 X/y 구조로 읽어야 한다.
- 자주 하는 실수: target을 feature에 섞어 target leakage를 만드는 오류.
- 선행 노드: `n_DS_CODE.dataframe_row_column`
- 후속 노드: `n_DS_ML1.classification_regression`, `n_DS_ML1.train_test_generalization`
- 유사 노드: -
- evidence snippet: Classification Algorithm –Logistic RegressionLogistic regression-어떤 현상에 대한 관측데이터 X와 이들이 어떠한 클래스(class) 또는 범주(label)에 속하는지에 대한 정보 Y가 존재-Y가 두 개의 클래스로 이루어진 경우, 하나의 데이터가 successive ...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 지도/비지도/강화학습

- 현재 노드: `n_DS_ML1.learning_types`
- 관련 파일: `DS_PDF08_ML1` / `DS_PDF04__machine_learning_part_1__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML1:p002:L005` / `ev_DS_PDF08_ML1_002`
- 한 줄 정의: 지도학습은 정답 y가 있고, 비지도학습은 구조를 찾고, 강화학습은 보상으로 행동 정책을 학습한다.
- 쉬운 직관: 정답이 있느냐, 구조를 찾느냐, 행동을 개선하느냐로 문제를 나눈다.
- 수식/절차: supervised: f(X)->y. unsupervised: structure(X). reinforcement: policy maximizing reward.
- 데이터프레임 구조: target column 유무가 지도/비지도 판별의 핵심이다.
- 코드 관점: Classifier/Regressor, clustering, RL environment
- 강의 예제 연결: ML Part 1의 학습 유형 표가 Gate 4/5 라우터다.
- 자주 하는 실수: 군집 결과를 정답 라벨처럼 평가하거나, target 없는 문제에 accuracy를 쓰는 오류.
- 선행 노드: `n_DS_ML1.feature_target_structure`
- 후속 노드: `n_DS_ML3.clustering_problem`
- 유사 노드: -
- evidence snippet: Supervised learning (지도학습)-Machine learning task of inferring a function from labeled training data- 정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습Unsupervised learning (비지도학습)-Machine learn...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Train/Test split과 일반화

- 현재 노드: `n_DS_ML1.train_test_generalization`
- 관련 파일: `DS_PDF08_ML1` / `DS_PDF04__machine_learning_part_1__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML1:p002:L005` / `ev_DS_PDF08_ML1_003`
- 한 줄 정의: 학습에 쓴 데이터와 평가 데이터를 분리해 새 데이터 성능을 추정하는 검증 절차다.
- 쉬운 직관: 외운 성적과 실전 성적을 분리해서 보는 장치다.
- 수식/절차: split data -> fit on train -> predict on test -> metric on test
- 데이터프레임 구조: 행 단위로 분할하되 시간/그룹 누수 여부를 확인한다.
- 코드 관점: train_test_split(X, y, test_size=..., random_state=...)
- 강의 예제 연결: R/Python PDF의 train/test 시각화와 ML Part 1 평가 흐름이 연결된다.
- 자주 하는 실수: 전처리나 feature selection을 split 전에 전체 데이터로 fit하는 leakage 오류.
- 선행 노드: `n_DS_CODE.sklearn_workflow`, `n_DS_STATS.statistical_inference`
- 후속 노드: `n_DS_ML1.loss_metric`, `n_DS_ML2.scaling_distance_models`
- 유사 노드: -
- evidence snippet: Supervised learning (지도학습)-Machine learning task of inferring a function from labeled training data- 정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습Unsupervised learning (비지도학습)-Machine learn...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 전처리와 leakage

- 현재 노드: `n_DS_ML1.preprocessing_leakage`
- 관련 파일: `DS_PDF08_ML1` / `DS_PDF04__machine_learning_part_1__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML1:p002:L005` / `ev_DS_PDF08_ML1_004`
- 한 줄 정의: 결측치 대체, scaling, 이상치 판단, feature selection 같은 전처리는 train/test 경계를 지키며 학습 데이터 기준으로 fit해야 한다.
- 쉬운 직관: 시험지 답을 미리 보고 공부하지 않도록 데이터 처리 순서를 잠그는 규칙이다.
- 수식/절차: split first -> fit preprocessing on train -> transform train/test -> fit model -> evaluate
- 데이터프레임 구조: missing/outlier/scaler statistics are learned from train rows only.
- 코드 관점: Pipeline([('preprocess', ...), ('model', ...)]), SimpleImputer, StandardScaler
- 강의 예제 연결: boxplot의 이상치 후보, bootstrap/imputation, scaling 민감도가 모두 이 leakage 규칙으로 연결된다.
- 자주 하는 실수: 전체 데이터로 평균/표준편차/결측 대체값을 계산한 뒤 split하는 오류.
- 선행 노드: `n_DS_ML1.train_test_generalization`, `n_DS_STATS.bootstrap_imputation`
- 후속 노드: `n_DS_ML2.scaling_distance_models`, `n_DS_ML3.kmeans_centroid_loop`
- 유사 노드: -
- evidence snippet: Supervised learning (지도학습)-Machine learning task of inferring a function from labeled training data- 정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습Unsupervised learning (비지도학습)-Machine learn...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 분류와 회귀

- 현재 노드: `n_DS_ML1.classification_regression`
- 관련 파일: `DS_PDF08_ML1` / `DS_PDF04__machine_learning_part_1__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML1:p034:L004` / `ev_DS_PDF08_ML1_005`
- 한 줄 정의: target이 범주형이면 분류, 연속형이면 회귀로 푸는 지도학습 문제 유형이다.
- 쉬운 직관: 무엇을 맞히는지가 이름표인지 숫자인지 구분하는 문제 라우터다.
- 수식/절차: classification predicts class label/probability; regression predicts continuous value.
- 데이터프레임 구조: target dtype과 의미를 확인한다.
- 코드 관점: Classifier vs Regressor estimator 선택
- 강의 예제 연결: ML Part 1의 logistic regression/classification 슬라이드가 범주형 target의 대표 예다.
- 자주 하는 실수: 숫자 코드로 저장된 범주형 target을 회귀로 착각하는 오류.
- 선행 노드: `n_DS_ML1.feature_target_structure`
- 후속 노드: `n_DS_ML2.svm_margin_hyperplane`, `n_DS_ML2.knn_vote`
- 유사 노드: -
- evidence snippet: Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervi...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Loss/Cost와 평가 지표

- 현재 노드: `n_DS_ML1.loss_metric`
- 관련 파일: `DS_PDF08_ML1` / `DS_PDF04__machine_learning_part_1__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML1:p017:L005` / `ev_DS_PDF08_ML1_006`
- 한 줄 정의: loss는 학습 중 줄이는 오류 함수이고, metric은 모델 성능을 해석하기 위한 평가 함수다.
- 쉬운 직관: 모델이 무엇을 줄이려고 학습했는지와 우리가 무엇으로 판단할지를 분리한다.
- 수식/절차: fit minimizes training objective; test metric evaluates task performance. Confusion matrix에서 Accuracy=(TP+TN)/N, Precision=TP/(TP+FP), Recall=TP/(TP+FN), F1=2PR/(P+R).
- 데이터프레임 구조: y_true/y_pred를 비교해 accuracy, precision, recall, RMSE 등을 계산한다.
- 코드 관점: sklearn.metrics, model.score, confusion_matrix, precision_recall_fscore_support
- 강의 예제 연결: ML Part 1의 prediction/loss/accuracy 흐름이 Gate 4 통과 기준이며, churn 같은 불균형 문제는 recall/F1로 확장해야 한다.
- 자주 하는 실수: loss가 낮으면 모든 비즈니스 판단이 좋다고 단정하거나, 불균형 데이터에서 accuracy만 보는 오류.
- 선행 노드: `n_DS_ML1.train_test_generalization`
- 후속 노드: `n_DS_ML2.svm_margin_hyperplane`, `n_DS_ML2.knn_vote`, `n_DS_ML2.decision_tree_impurity`
- 유사 노드: -
- evidence snippet: •성능의 반대 개념은 손실(=loss), 오류(=cost) à 높은 성능 = 낮은 손실 = 낮은 오류•모델을 학습할 땐, 성능을 최대화(=maximization)하거나 손실을 최소화(=minimization)하는 가중치 계산à대부분의 경우, 손실을 최소화하는 방법을 사용
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 로지스틱 회귀와 logit

- 현재 노드: `n_DS_ML1.logistic_logit_probability`
- 관련 파일: `DS_PDF08_ML1` / `DS_PDF04__machine_learning_part_1__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML1:p043:L004` / `ev_DS_PDF08_ML1_007`
- 한 줄 정의: 선형 점수를 확률로 바꿔 class 1에 속할 가능성을 예측하는 분류 모델이다.
- 쉬운 직관: 직선 점수를 0과 1 사이의 확률 언어로 변환한다.
- 수식/절차: odds = p/(1-p), logit(p)=log(p/(1-p)), p=sigmoid(w^T x+b)
- 데이터프레임 구조: X feature row별 class probability를 예측한다.
- 코드 관점: LogisticRegression.fit, predict_proba, threshold
- 강의 예제 연결: ML Part 1 후반 logistic regression 슬라이드가 p, odds, logit 연결을 설명한다.
- 자주 하는 실수: 로지스틱 회귀를 연속값 회귀 모델로 해석하거나 threshold를 고정 진리로 보는 오류.
- 선행 노드: `n_DS_ML1.classification_regression`, `n_DS_STATS.probability_random_variable`
- 후속 노드: `n_DS_ML2.svm_margin_hyperplane`
- 유사 노드: -
- evidence snippet: Classification Algorithm –Logistic RegressionOdds성공 확률(success probability, 𝑝)가 실패확률 (1 –𝑝)에 비해 몇 배 더 높은가?-𝑝= probability of belonging to class 1(success),  odds = p / (1-p)-0과 ...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 텍스트 벡터화

- 현재 노드: `n_DS_ML1.text_vectorization_features`
- 관련 파일: `DS_PDF08_ML1` / `DS_PDF04__machine_learning_part_1__full_transcript.txt`
- 근거 anchor: `DS_PDF08_ML1:p012:L004` / `ev_DS_PDF08_ML1_008`
- 한 줄 정의: 문자열 문서를 모델이 계산할 수 있는 수치 feature로 바꾸는 표현 변환이다.
- 쉬운 직관: 말을 숫자 좌표로 바꾸어 거리·분류·확률 모델에 넣는다.
- 수식/절차: text -> tokenization -> count/TF-IDF/embedding -> feature vector
- 데이터프레임 구조: 각 row는 문서, 각 column은 토큰/임베딩 차원이다.
- 코드 관점: CountVectorizer, TfidfVectorizer, embedding model
- 강의 예제 연결: ML Part 1의 text vectorization은 DS09 LLM의 embedding/pre-training으로 이어진다.
- 자주 하는 실수: 텍스트 원문을 모델이 그대로 이해한다고 생각하거나, 벡터화 기준을 train/test 밖에서 섞는 오류.
- 선행 노드: `n_DS_ML1.feature_target_structure`
- 후속 노드: `n_DS_LLM.embedding_contextual_representation`
- 유사 노드: -
- evidence snippet: Machine Learning BasicsSupervised Learning(지도학습) For Text Mining문서(=Document)를 수치형 벡터로 표현(e.g. Bag-of-Words, Doc2Vec 등)하고 문서마다 Label 정보(e.g. Spam/Non-Spam)를 활용하여 분류 모델을 학습 및 추론
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?
