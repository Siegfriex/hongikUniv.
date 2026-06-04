# 1~15강 전체 교육목표 설계 최종본

## 0. 문서 판정

| 항목 | 값 |
|------|----|
| 문서 목적 | ML 1~15강을 하나의 교육목표·의존관계·RAG 링크 구조로 재정리 |
| 기준 SSOT | 현재 작업트리의 `ML/*.md`, `ML/_inventory/*`, `ML/_framework/*` |
| 1단계 산출물 위치 | `ML/_framework/`, `ML/_inventory/`, `docx-export/ML/_inventory-derived/` |
| 검증 상태 | 8~15강 RAG 구조 검증 통과, 15강 의미 재매핑 반영 |
| 주의 | 현재 트리에는 5강·9강 단독 구조 md가 없다. 본 문서는 5강을 회귀 브리지, 9강을 신경망 수학 브리지로 운영 목표에 배치하되 소스 신뢰도를 별도 표기한다. |

한 줄 요약:

> 이 과목의 최종 목표는 모델 이름을 암기하는 것이 아니라, **문제 정의 -> 데이터 표현 -> 전처리/EDA -> 모델 선택 -> 학습 원리 -> 평가/해석 -> 딥러닝 구조 확장**을 하나의 판단 체계로 만드는 것이다.

최종 역량 문장:

> 새로운 데이터셋을 보면 스스로 `X`, `y`, 문제 유형, 전처리, 모델 후보, loss/metric, 검증 방식, 해석 리포트까지 설계할 수 있는가?

---

## 1. Codex 에이전트 소스 선별

### 1.1 반드시 투입할 소스

| 우선순위 | 파일/폴더 | 역할 | 투입 이유 |
|----------|-----------|------|-----------|
| S0 | `ML/_framework/AGENT_START_HERE.md` | 에이전트 운영 진입점 | 다음 에이전트가 inventory/RAG 규칙을 재현할 수 있게 한다. |
| S0 | `ML/_framework/PIPELINE.md` | 생성 절차 | 구조 추출, 전사 정렬, RAG md, 로데이터 디벨롭, 검증 순서를 고정한다. |
| S0 | `ML/_framework/SCHEMAS.md` | sidecar 스키마 | `nodes`, `edges`, `segments`, `evidence`, `alignments`의 필드 의미를 고정한다. |
| S0 | `ML/_framework/CONVENTIONS.md` | id 규약 | `ML15.A.30.local_003`, `n_ML15.padding_stride_pooling` 같은 id 체계를 유지한다. |
| S0 | `ML/_inventory/README_inventory.md` | 완성 강 카탈로그 | 8~15강의 node/segment/evidence/DOCX 수량과 산출물 위치를 확인한다. |
| S0 | `ML/_inventory/final_verification_report_8_15.md` | 최종 검증 리포트 | 자동 검증과 15강 수동 의미 재매핑 결과를 확인한다. |
| S1 | `ML/_inventory/*/nodes.json` | 개념 노드 SSOT | 교육목표의 핵심 개념 단위를 정의한다. |
| S1 | `ML/_inventory/*/edges.json` | 강 내 링크 간선 | 강의 내부 흐름을 `leads_to` 간선으로 제공한다. |
| S1 | `ML/_inventory/*/evidence.jsonl` | 근거 SSOT | md와 transcript line 기반 evidence를 제공한다. |
| S1 | `ML/_inventory/*/alignments.jsonl` | 전사-구조 정렬 | transcript segment가 어느 md anchor에 붙는지 보여준다. |
| S1 | `ML/_inventory/*/*_래그.md` | 검색용 RAG 문서 | 사람이 빠르게 node/evidence를 조회할 때 쓴다. |
| S1 | `ML/_inventory/*/*_로데이터디벨롭.md` | 강별 디벨롭 문서 | 원문 근거와 재구성 문장을 함께 확인한다. |
| S1 | `ML/final_record/*.txt` | 강의 녹음 전사 원천 | 강의 녹음본의 텍스트화 원천이다. RAG segment/evidence의 transcript side를 검증할 때 반드시 같이 넣는다. |

### 1.2 강의 녹음본·전사 소스

현재 작업트리에는 `mp3`, `m4a`, `wav`, `aac`, `flac`, `ogg`, `webm`, `mp4` 형식의 실제 오디오 파일은 없다. 따라서 현 시점의 녹음본 소스는 `ML/final_record/*.txt` 전사 파일이며, 강의 녹음 원천을 텍스트로 보존한 SSOT로 취급한다.

| lecture_id | primary transcript | 상태 | 비고 |
|------------|--------------------|------|------|
| `20260430_8` | `ML/final_record/기계학습0430.txt` | primary | 8강 RAG segment/evidence 원천 |
| `20260507_10` | `ML/final_record/기계학습0507.txt` | primary | 10강 RAG segment/evidence 원천 |
| `20260514_11` | `ML/final_record/0514ml.txt` | primary | 11강 RAG segment/evidence 원천 |
| `20260521_12` | `ML/final_record/0521Ml.txt` | primary | 12강 RAG segment/evidence 원천 |
| `20260528_13` | `ML/final_record/0528ml.txt` | primary | 13강 RAG segment/evidence 원천 |
| `20260529_14` | `ML/final_record/0529_ml.txt` | primary | 14강 RAG segment/evidence 원천 |
| `20260529_14` | `ML/final_record/0529이용오교수님.txt` | secondary/conflict | 보조 전사다. primary와 섞지 말고 conflict source로만 사용한다. |
| `20260604_15` | `ML/final_record/0604ml.txt` | primary | 15강 RAG segment/evidence 원천. CNN/종강 구간으로 수동 의미 재매핑 완료 |
| skipped | `ML/final_record/0522ml.txt` | skipped | matching `final_brief`가 없어 1단계 batch 대상에서 제외 |

에이전트 투입 규칙:

- 강의별 md 구조 SSOT와 `final_record` 전사 SSOT를 함께 넣는다.
- RAG 검증 시 `segments.jsonl.text_raw`가 해당 전사 줄 범위와 byte-level로 일치하는지 확인한다.
- 실제 오디오 파일이 나중에 들어오면 `final_record/*.txt`보다 상위 raw source로 등록하고, 전사 파일은 derived transcript로 재분류한다.

### 1.3 강의 원문 소스

| 범위 | 파일 | 신뢰도 | 비고 |
|------|------|--------|------|
| 1강 | `ML/20250306.md` | 높음 | ML 정의, 지도학습, 선형회귀, 경사하강법, 데이터사이언스 단계 |
| 2강 | `ML/20250313.md` | 높음 | 비지도학습, 로지스틱 회귀, Naive Bayes, 다변수 회귀 |
| 3강 | `ML/20250319.md` | 높음 | NumPy, ndarray, shape, axis, vectorization |
| 4강 | `ML/20250326.md` | 높음 | Pandas, Series/DataFrame, 결측, 시계열, EDA |
| 5강 | 없음 | 보완 필요 | 현재 단독 md 부재. 1~4강과 6~7강 사이의 회귀/전처리 브리지로 운영한다. |
| 6강 | `ML/20260409.md` | 높음 | classification, Iris, KNN, SVM, Decision Tree, 평가 지표 |
| 7강 | `ML/20260416.md` | 높음 | Decision Tree, Entropy/Gini, Random Forest, Bagging/Boosting |
| 8강 | `ML/20260430_8강.md` + `ML/final_record/기계학습0430.txt` + `ML/_inventory/20260430_8/` | 매우 높음 | Neural Network, Perceptron, XOR, MLP |
| 9강 | `ML/week09_examples.ipynb` | 중간 | 단독 구조 md 부재. 8강과 10강 사이의 실습/수학 브리지로 둔다. |
| 10강 | `ML/20260507_10강.md` + `ML/final_record/기계학습0507.txt` + inventory | 매우 높음 | 미분, 편미분, gradient, chain rule, GD, backprop |
| 11강 | `ML/20260514_11강.md` + `ML/final_record/0514ml.txt` + inventory | 매우 높음 | 2-2-1 MLP backprop, delta, gradient check |
| 12강 | `ML/20260521_12강.md` + `ML/final_record/0521Ml.txt` + inventory | 매우 높음 | Layer abstraction, vectorized backprop, Network, Keras 대응 |
| 13강 | `ML/20260528_13강.md` + `ML/final_record/0528ml.txt` + inventory | 매우 높음 | Keras DNN, optimizer, 회귀/분류 output/loss/metric |
| 14강 | `ML/20260529_14강.md` + `ML/final_record/0529_ml.txt` + inventory | 매우 높음 | Boston Housing, DataFrame/EDA, scaling, DNN regression validation |
| 15강 | `ML/20260604_15강.md` + `ML/final_record/0604ml.txt` + inventory | 매우 높음 | 실험 설계, overfit 대응, CNN, Fashion-MNIST, ImageNet |

### 1.4 에이전트 투입에서 제외할 소스

| 제외 대상 | 이유 |
|-----------|------|
| `*:Zone.Identifier` | Windows 다운로드 메타데이터다. 교육/RAG 근거가 아니다. |
| `docx-export/` | 사람이 열람하는 내보내기 결과다. 에이전트에는 md/json/jsonl 원본을 우선 넣는다. |
| `ML/week13 (3).pdf` | `ML/week13.pdf`와 중복 가능성이 있어 별도 hash 확인 전 primary source로 쓰지 않는다. |
| `ML/final_record/0522ml.txt` | matching `final_brief`가 없어 현재 batch에서 skipped 상태다. |
| `ML/final_record/0529이용오교수님.txt` | 14강의 secondary/conflict transcript다. primary는 `0529_ml.txt`다. |

---

## 2. 전체 교육목표의 최상위 구조

이 과목은 6개 페이즈로 읽는다.

| 페이즈 | 범위 | 교육목표 한 줄 | 왜 필요한가 | 대표 소스 |
|--------|------|----------------|-------------|-----------|
| Phase 1 | 1~2강 | ML 문제를 수학적·확률적 문제로 번역 | 모델을 돌리기 전에 task, target, metric을 정해야 한다. | `20250306.md`, `20250313.md` |
| Phase 2 | 3~4강 | 데이터를 배열·표·시각화로 다루는 능력 확보 | 모델 입력은 결국 `X`, `y`, ndarray, DataFrame, tensor다. | `20250319.md`, `20250326.md` |
| Phase 3 | 5~7강 | 전통 ML 모델을 선택·학습·평가 | EDA, 전처리, 회귀/분류, 성능평가, 모델 비교가 중간 범위의 핵심이다. | 5강 보완 필요, `20260409.md`, `20260416.md` |
| Phase 4 | 8~10강 | 신경망을 학습 문제와 미분 문제로 연결 | Perceptron/MLP가 왜 chain rule과 gradient descent를 필요로 하는지 이해한다. | `20260430_8강.md`, `week09_examples.ipynb`, `20260507_10강.md` |
| Phase 5 | 11~12강 | Backprop을 구현 가능한 layer 시스템으로 일반화 | 2-2-1 손계산을 임의 깊이 network와 mini-batch 학습으로 확장한다. | `20260514_11강.md`, `20260521_12강.md` |
| Phase 6 | 13~15강 | DNN/CNN 실전 적용과 기말 통합 | output layer, loss, metric, optimizer, validation, CNN 구조를 설계한다. | `20260528_13강.md`, `20260529_14강.md`, `20260604_15강.md` |

핵심 구조:

```text
Problem framing
  -> data representation
  -> EDA / preprocessing
  -> traditional model selection
  -> neural network learning loop
  -> backprop implementation
  -> Keras abstraction
  -> validation / regularization
  -> CNN / image structure
  -> final report and defense
```

---

## 3. 목표달성 레벨

각 강의의 달성도는 다음 5단계로 평가한다.

| 레벨 | 이름 | 의미 | 확인 질문 |
|-----:|------|------|-----------|
| L1 | 용어 인식 | 용어의 한 줄 정의를 안다. | “이 단어를 1문장으로 정의할 수 있나?” |
| L2 | 직관 이해 | 왜 필요한지 설명한다. | “이 개념이 없으면 어떤 문제가 생기나?” |
| L3 | 수식·알고리즘 이해 | 식과 절차를 해석한다. | “기호 하나하나가 현실에서 무엇을 뜻하나?” |
| L4 | 코드·데이터 표현 | 코드에서 shape, 입력/출력, 객체 역할을 읽는다. | “이 코드 줄이 어떤 수식 또는 절차에 대응하나?” |
| L5 | 적용·판단 | 새 문제에 맞게 선택하고 해석한다. | “이 상황에서는 어떤 모델/지표/전처리를 고를 것인가?” |

기말 목표는 L5다. 특히 10~15강은 L1~L2 암기로는 부족하다. `Dense`, `ReLU`, `Softmax`, `CrossEntropy`, `Conv2D`, `Pooling`을 코드, shape, loss, metric, validation과 연결해야 한다.

---

## 4. 1~15강 강의별 심층 교육목표

| 강 | 페이즈 | 핵심 노드 | 심층 이론 목표 | 적용 목표 | 목표달성 증거 |
|---:|--------|-----------|----------------|-----------|---------------|
| 1강 | Phase 1 | ML 정의, T/E/P, supervised learning, linear regression, gradient descent, data science 5 steps | ML을 데이터로부터 패턴을 학습하고 성능을 개선하는 과정으로 이해한다. | 새 문제를 task, experience, performance, `X`, `y`, metric으로 분해한다. | 임의 문제를 5줄 ML 문제 정의로 바꾼다. |
| 2강 | Phase 1 | unsupervised learning, classification, logistic regression, Naive Bayes, conditional probability | 분류를 클래스 확률 비교 문제로 이해한다. prior, likelihood, posterior를 구분한다. | spam/weather/Iris 예제에서 posterior argmax로 클래스를 고른다. | “분모 `P(X)`는 argmax에서 왜 생략 가능한가?”를 설명한다. |
| 3강 | Phase 2 | NumPy, ndarray, shape, axis, broadcasting, vectorization | 데이터가 list가 아니라 수치 배열로 표현되는 이유를 이해한다. | reshape, axis reduction, broadcasting 결과 shape를 예측한다. | `X.shape == (n_samples, n_features)`와 image tensor shape를 설명한다. |
| 4강 | Phase 2 | Pandas, Series, DataFrame, missing values, groupby, visualization, Titanic EDA | DataFrame을 행/열 레이블이 있는 2D 데이터 구조로 이해하고 EDA를 가설 생성 단계로 본다. | `info`, `describe`, `isna`, `corr`, countplot/histplot/boxplot로 데이터 구조와 변수 관계를 해석한다. | Titanic류 데이터에서 결측, 분포, feature 후보, target 관계를 리포트로 쓴다. |
| 5강 | Phase 3 | regression bridge, feature selection, train/test split, MSE/MAE/MAPE | 회귀를 연속값 target 예측 문제로 이해한다. | 상관계수 기반 feature selection, split, linear regression, MSE/MAE/MAPE 평가를 수행한다. | 14강 DNN 회귀와 연결해 “모델만 바뀌고 회귀 설계 원리는 유지된다”고 설명한다. |
| 6강 | Phase 3 | classification, Iris, KNN, SVM, Decision Tree, confusion matrix, precision/recall/F1 | 분류를 class label 예측과 오류 비용 관리 문제로 이해한다. | scaler, KNN/SVM/DT 학습, confusion matrix, metric 해석을 수행한다. | 도메인 비용 기준으로 precision과 recall 중 무엇을 우선할지 말한다. |
| 7강 | Phase 3 | Decision Tree, entropy, information gain, Gini, CART, Random Forest, Bagging/Boosting | 트리를 feature threshold로 공간을 재귀 분할하는 모델로 이해한다. | `max_depth`, `min_samples_leaf`, `n_estimators`를 조정하며 과적합/과소적합을 비교한다. | Entropy/Gini가 불순도를 줄이는 기준임을 계산 예시로 설명한다. |
| 8강 | Phase 4 | `n_ML8.perceptron`, `n_ML8.xor`, `n_ML8.mlp_xor`, `n_ML8.forward_loss_backward_update` | Perceptron이 선형 분류기이며 XOR 한계가 hidden layer 필요성을 만든다는 점을 이해한다. | AND/OR/NAND/XOR를 선형 분리와 MLP 조합 관점으로 설명한다. | XOR 모순과 MLP 해결 구조를 그림 또는 부등식으로 방어한다. |
| 9강 | Phase 4 | notebook bridge, MLP practice, activation/loss loop | 8강 개념을 실습 코드로 연결하고 10강 미분 도구로 넘어갈 준비를 한다. | `week09_examples.ipynb`를 통해 forward/loss/update 흐름을 추적한다. | 단독 구조 md 보완 전까지는 “실습 브리지”로만 사용한다. |
| 10강 | Phase 4 | `n_ML10.chain_rule`, `n_ML10.gradient_descent`, `n_ML10.backprop` | 신경망 학습을 합성함수 미분과 최적화 문제로 이해한다. | 편미분, gradient, chain rule, GD update를 계산 그래프와 연결한다. | `fit()` 내부가 forward, loss, backward, optimizer update 반복임을 설명한다. |
| 11강 | Phase 5 | `n_ML11.forward_pass`, `n_ML11.section_05`, `n_ML11.section_06`, `n_ML11.gradient_check` | 2-2-1 MLP에서 출력층 delta와 은닉층 delta가 왜 다르게 계산되는지 이해한다. | 손계산 backprop, `np.outer`, `W.T`, gradient check를 코드와 연결한다. | 하나의 weight가 loss에 미치는 경로를 chain rule로 추적한다. |
| 12강 | Phase 5 | `n_ML12.layer_abstraction_activation`, `n_ML12.vectorized_backprop_batch_dimension_matrix`, `n_ML12.network_mini_batch`, `n_ML12.gradient` | Backprop을 layer별 local gradient와 network-level 역순 호출로 일반화한다. | Dense/ReLU/Sigmoid/SoftmaxCE, mini-batch shape, Network 조립을 구현 관점에서 설명한다. | `Dense -> Activation -> Loss`의 forward/backward shape를 말한다. |
| 13강 | Phase 6 | `n_ML13.keras`, `n_ML13.optimizer`, `n_ML13.section_07`, `n_ML13.softmax_cross_entropy` | 직접 구현한 NN이 Keras API로 어떻게 대응되는지 이해한다. 회귀와 분류의 output/loss/metric 차이를 설명한다. | DNN regression과 DNN classification을 Keras로 구현하고 optimizer를 비교한다. | 회귀는 `Dense(1)+MSE/MAE`, 분류는 `Dense(K, softmax)+cross entropy/accuracy`로 설계한다. |
| 14강 | Phase 6 | `n_ML14.dataframe`, `n_ML14.minmax_scaling`, `n_ML14.shape`, `n_ML14.modeling_training`, `n_ML14.validation_test` | DNN 성능은 모델 구조뿐 아니라 데이터 프로세싱과 검증 설계에 좌우됨을 이해한다. | Boston Housing에서 DataFrame/EDA, CHAS 제거, split, scaling, Sequential/Dense, validation, inverse transform을 수행한다. | 예측값을 원래 단위로 복원하고 MAE/산점도로 검증한다. |
| 15강 | Phase 6 | `n_ML15.train_validation_test`, `n_ML15.loss_curve`, `n_ML15.dropout`, `n_ML15.convolution_layer`, `n_ML15.padding_stride_pooling`, `n_ML15.imagenet_cnn` | 실험 설계, 과적합 대응, CNN 구조를 하나의 최종 판단 체계로 묶는다. | 3분할, leakage 방지, regularization, CNN feature extractor, Fashion-MNIST Dense vs CNN 비교를 수행한다. | “왜 이 구조, loss, metric, optimizer, validation 전략을 선택했는가?”를 코드와 리포트로 방어한다. |

---

## 5. RAG 기반 의존관계와 링크 간선

### 5.1 강의 간 핵심 간선

| from | to | 관계 | 의미 |
|------|----|------|------|
| 1강 ML 문제 정의 | 2강 확률적 분류 | `frames` | target과 metric을 정해야 확률 분류도 의미를 가진다. |
| 1강 linear regression/GD | 10강 gradient descent | `prepares_math` | 10강 GD는 1강 최적화 구조의 신경망 버전이다. |
| 2강 Naive Bayes/logistic classification | 13강 softmax/cross entropy | `prepares_probability_output` | 분류는 class probability 비교에서 softmax 확률 분포 학습으로 확장된다. |
| 3강 ndarray/shape | 12강 vectorized backprop | `prepares_tensor_reasoning` | batch dimension과 matrix shape를 모르면 vectorized backprop이 블랙박스가 된다. |
| 4강 DataFrame/EDA | 14강 Boston Housing DataFrame/EDA | `prepares_data_pipeline` | 14강 DNN 회귀도 먼저 표 데이터를 이해해야 한다. |
| 5강 회귀 | 14강 DNN regression | `upgrades_model_class` | 선형 회귀의 target/loss/metric 사고가 DNN 회귀로 이어진다. |
| 6강 classification metrics | 13강 DNN classification | `prepares_evaluation` | accuracy, precision/recall 사고가 neural classifier 평가로 이어진다. |
| 7강 overfit/ensemble | 15강 regularization | `prepares_generalization` | 전통 ML의 과적합 제어가 DNN regularization으로 확장된다. |
| 8강 perceptron/MLP | 10강 chain rule/backprop | `requires_math_tooling` | MLP가 깊어지면 손으로 책임을 추적하기 어려워 chain rule이 필요하다. |
| 10강 chain rule/GD | 11강 2-2-1 backprop | `enables_derivation` | 11강은 10강 도구를 실제 network weight에 적용한다. |
| 11강 2-2-1 backprop | 12강 Layer abstraction | `generalizes` | 손계산 delta를 layer interface와 vectorized batch로 일반화한다. |
| 12강 Network/Keras 대응 | 13강 Keras DNN | `maps_to_framework` | `Network`, `Layer`, `update`가 `Sequential`, `Dense`, `optimizer`로 대응된다. |
| 13강 Keras DNN | 14강 DNN data processing | `moves_to_real_data` | 모델 API를 실제 tabular regression pipeline에 적용한다. |
| 14강 validation/test | 15강 train/validation/test, loss curve | `refines_validation` | 2분할 실습을 3분할과 overfit 진단으로 정교화한다. |
| 15강 CNN | 최종 리포트 | `requires_defense` | 구조, loss, metric, validation, 개선안을 말로 방어해야 한다. |

### 5.2 8~15강 내부 RAG 간선 요약

| lecture_id | 대표 내부 간선 |
|------------|----------------|
| `20260430_8` | `n_ML8.perceptron -> n_ML8.xor -> n_ML8.mlp_xor -> n_ML8.forward_loss_backward_update` |
| `20260507_10` | `n_ML10.section_02 -> n_ML10.section_03 -> n_ML10.chain_rule -> n_ML10.gradient_descent -> n_ML10.backprop` |
| `20260514_11` | `n_ML11.forward_pass -> n_ML11.section_05 -> n_ML11.section_06 -> n_ML11.gradient_check -> n_ML11.xor` |
| `20260521_12` | `n_ML12.layer_abstraction_activation -> n_ML12.vectorized_backprop_batch_dimension_matrix -> n_ML12.network_mini_batch -> n_ML12.gradient -> n_ML12.keras` |
| `20260528_13` | `n_ML13.section_02 -> n_ML13.optimizer -> n_ML13.sgd_momentum_rmsprop_adam -> n_ML13.keras -> n_ML13.softmax_cross_entropy` |
| `20260529_14` | `n_ML14.dataframe -> n_ML14.eda -> n_ML14.minmax_scaling -> n_ML14.shape -> n_ML14.modeling_training -> n_ML14.validation_test` |
| `20260604_15` | `n_ML15.train_validation_test -> n_ML15.loss_curve -> n_ML15.dropout -> n_ML15.baseline_vs_regularized -> n_ML15.convolution_layer -> n_ML15.padding_stride_pooling -> n_ML15.imagenet_cnn` |

---

## 6. 페이즈별 최종 교육계획

### Phase 1. 1~2강: 문제를 ML 언어로 번역하는 능력

이 페이즈의 목표는 “ML이 무엇인가”를 외우는 것이 아니라 현실 문제를 학습 문제로 변환하는 것이다. “학생 성적을 예측하라”는 말은 아직 ML 문제가 아니다. 이를 ML 문제로 만들려면 입력 feature `X`, target `y`, task `T`, experience `E`, performance `P`를 정해야 한다.

2강은 여기에 확률적 판단을 붙인다. 분류는 단순히 맞다/틀리다가 아니라, class probability를 비교하고 가장 그럴듯한 class를 고르는 의사결정이다. 이 사고는 후반부 softmax와 cross entropy로 이어진다.

달성 기준:

- supervised/unsupervised, regression/classification을 구분한다.
- `X`, `y`, loss, metric을 문제 정의 단계에서 먼저 쓴다.
- Bayes 식의 prior, likelihood, posterior를 구분한다.

### Phase 2. 3~4강: 데이터를 모델 입력으로 바꾸는 능력

3강 NumPy와 4강 Pandas는 코딩 문법이 아니라 데이터 표현 체계다. NumPy는 모델 가까이에 있고, Pandas는 사람이 데이터를 이해하는 표 구조에 가깝다.

모델은 DataFrame 자체를 이해하지 않는다. 모델은 수치 배열을 계산한다. 반대로 사람이 ndarray만 보면 데이터 의미를 잃기 쉽다. 그래서 이 페이즈의 핵심은 “사람이 이해 가능한 표”와 “모델이 계산 가능한 배열” 사이를 왕복하는 능력이다.

달성 기준:

- `shape`, `axis`, `ndim`, broadcasting 결과를 예측한다.
- DataFrame에서 feature와 target을 분리한다.
- 결측, 이상치, 분포, 상관관계를 보고 전처리 방향을 정한다.

### Phase 3. 5~7강: 전통 ML 모델을 판단하는 능력

5~7강의 목표는 모델 이름을 많이 아는 것이 아니라, 모델마다 어떤 가정과 오류 패턴을 갖는지 이해하는 것이다.

Linear Regression은 연속값 target을 가중합으로 예측한다. KNN은 거리 기반 다수결이다. SVM은 margin을 최대화한다. Decision Tree는 threshold로 공간을 나눈다. Random Forest와 Boosting은 여러 모델을 결합해 단일 모델의 불안정성을 줄인다.

달성 기준:

- 회귀/분류 모델 후보를 데이터 구조와 metric에 맞춰 고른다.
- train/test split, scaling, hyperparameter search를 하나의 실험 절차로 묶는다.
- confusion matrix와 precision/recall/F1을 도메인 비용으로 해석한다.
- tree 계열의 entropy, information gain, Gini를 불순도 감소 관점으로 설명한다.

### Phase 4. 8~10강: 신경망을 학습 문제와 미분 문제로 연결하는 능력

8강은 기존 feature engineering의 한계를 신경망 구조로 넘기는 전환점이다. Perceptron은 선형 분류기이므로 XOR를 풀 수 없다. 이 한계가 hidden layer와 MLP의 필요성을 만든다.

10강은 이 구조가 왜 chain rule과 gradient descent를 필요로 하는지 설명한다. 신경망은 층을 합성한 함수다. 합성함수의 각 weight가 loss에 얼마나 책임이 있는지 계산하려면 chain rule이 필요하고, 그 gradient로 weight를 갱신하려면 GD가 필요하다.

달성 기준:

- Perceptron의 선형 결정경계를 설명한다.
- XOR가 왜 단일 perceptron으로 불가능한지 보인다.
- forward, loss, backward, update 루프를 쓴다.
- chain rule이 backprop의 수학적 엔진임을 설명한다.

### Phase 5. 11~12강: Backprop을 구현 가능한 layer 시스템으로 일반화하는 능력

11강은 2-2-1 network에서 backprop을 손으로 추적한다. 출력층 delta와 은닉층 delta가 다르게 생기는 이유는 loss까지 가는 경로가 다르기 때문이다. `W.T`, Hadamard product, `np.outer`는 이 경로를 코드로 표현한 것이다.

12강은 이를 임의 깊이 network로 일반화한다. 각 layer는 자기 forward/backward만 책임지고, Network는 layer를 순서대로 forward, 역순으로 backward 호출한다. 이 구조를 이해해야 Keras `Sequential`이 블랙박스가 되지 않는다.

달성 기준:

- 출력층과 은닉층 gradient 경로를 구분한다.
- gradient check의 목적을 설명한다.
- Dense/ReLU/Sigmoid/SoftmaxCE의 forward/backward shape를 추적한다.
- mini-batch dimension을 기준으로 vectorized backprop을 읽는다.

### Phase 6. 13~15강: DNN/CNN 실전 적용과 기말 통합 능력

13강은 직접 구현한 신경망을 Keras로 옮긴다. `Sequential`은 Network, `Dense`는 layer, `compile`은 loss/optimizer/metric 연결, `fit`은 forward-loss-backward-update 반복이다.

14강은 이 Keras 구조를 실제 Boston Housing 회귀에 적용한다. 핵심은 모델보다 앞단의 데이터 프로세싱이다. DataFrame, EDA, CHAS 제거, split, scaling, shape, compile/fit, validation, inverse transform까지 하나의 pipeline으로 봐야 한다.

15강은 이 pipeline을 더 엄격하게 만든다. train/validation/test 3분할, leakage 방지, loss curve, Dropout/L2/EarlyStopping/BatchNorm, baseline vs regularized 비교가 들어온다. 후반부는 CNN으로 이미지 구조를 다룬다. CNN은 flatten으로 공간 관계를 잃는 Dense의 한계를 보완하고, filter/kernel, feature map, padding, stride, pooling을 통해 local pattern을 학습한다.

달성 기준:

- 회귀와 분류에서 output layer, loss, metric을 다르게 설계한다.
- validation loss로 overfit을 진단한다.
- scaler는 train에 `fit`, validation/test에 `transform`만 적용한다고 설명한다.
- CNN에서 convolution 한 칸 계산, feature map 크기, pooling 결과를 설명한다.
- 최종 리포트에서 모델 구조 선택 이유와 개선안을 방어한다.

---

## 7. 최종 목표달성 체크리스트

| 영역 | 자기점검 질문 | 통과 기준 |
|------|---------------|-----------|
| 문제 정의 | 이 문제는 regression인가 classification인가? | target type과 metric을 함께 말한다. |
| 데이터 표현 | `X.shape`, `y.shape`, train/test shape가 무엇을 뜻하는가? | sample axis와 feature/class axis를 구분한다. |
| EDA | 결측, 분포, 이상치, 상관관계를 봤는가? | 모델링 전 리포트에 최소 3개 이상 근거를 남긴다. |
| 전처리 | scaling/encoding/split을 leakage 없이 했는가? | train 기준 `fit`, val/test 기준 `transform`을 지킨다. |
| 전통 ML | 왜 KNN/SVM/DT/RF 중 이 모델인가? | 데이터 크기, scaling 필요성, 해석성, overfit 위험으로 방어한다. |
| NN 원리 | forward-loss-backward-update를 말할 수 있는가? | 각 단계의 입력/출력과 gradient 역할을 설명한다. |
| Backprop | chain rule이 어디에 쓰이는가? | 출력층/은닉층 delta 차이를 설명한다. |
| Keras | `compile`, `fit`, `evaluate`가 무엇을 하는가? | 12강 직접 구현과 13강 Keras API를 대응시킨다. |
| 회귀 DNN | 왜 `Dense(1)`과 MSE/MAE인가? | target이 연속값이기 때문이라고 설명한다. |
| 분류 DNN | 왜 softmax와 cross entropy인가? | class probability distribution 학습으로 설명한다. |
| CNN | 왜 이미지에는 CNN이 필요한가? | flatten의 공간 구조 손실과 local receptive field를 비교한다. |
| 기말 리포트 | 왜 이 구조, loss, metric, optimizer, validation인가? | 코드, metric, learning curve, 개선안을 한 세트로 방어한다. |

---

## 8. 보완 작업 큐

| 우선순위 | 작업 | 이유 |
|----------|------|------|
| P0 | 5강 단독 SSOT md 확보 또는 작성 | 현재 1~15 계획에서 회귀 phase가 추정 브리지로 남아 있다. |
| P0 | 9강 단독 SSOT md 확보 또는 작성 | 8강 MLP와 10강 미분 사이의 실습/수학 연결을 RAG화해야 한다. |
| P1 | 1~7강도 `_inventory/<lecture_id>/` sidecar 생성 | 현재 RAG 기반 검증은 8~15강에만 완전 적용되어 있다. |
| P1 | cross-lecture edges를 별도 `course_edges.json`으로 생성 | 강의 간 간선을 현재 문서 수준이 아니라 sidecar 수준으로 추적 가능하게 한다. |
| P2 | `*:Zone.Identifier` 제외 정책을 `.gitignore` 또는 커밋 선별 규칙에 반영 | 에이전트 소스 pack에 잡파일이 섞이지 않게 한다. |

---

## 9. Validation

| 검증 항목 | 결과 | 근거 |
|-----------|------|------|
| 8~15강 node/segment/evidence/DOCX 구조 검증 | PASS | `ML/_inventory/final_verification_report_8_15.md` |
| 15강 transcript 의미 정렬 | PASS after fix | `ML/_inventory/20260604_15/_verify_report.md` |
| 15강 전처리/정규화 노드에 잘못 붙은 transcript evidence 제거 | PASS | 해당 노드는 `lecture_md_anchor` evidence만 유지 |
| source file 존재성 | PASS with gaps | 1~4, 6~15 source 존재. 5강·9강 단독 md 부재는 보완 큐에 반영 |
| 강의 녹음 전사 소스 반영 | PASS | `ML/final_record/*.txt`를 녹음 전사 SSOT로 선별표에 포함 |
| 에이전트 투입 제외 대상 식별 | PASS | `*:Zone.Identifier`, secondary transcript, duplicate PDF 후보 분리 |
| whitespace | PASS | `git diff --check` 통과 |

최종 판정:

> 본 교육계획은 현재 작업트리 기준으로 **1단계 SSOT 위에 세울 수 있는 최종 초안**이다. 다만 5강·9강 단독 SSOT가 없으므로, 완전한 1~15강 RAG 코스 그래프로 승격하려면 두 강의의 원문 확보 또는 신규 inventory 생성이 필요하다.
