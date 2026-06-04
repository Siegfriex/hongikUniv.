# 기말 대비 심층 학습 플랜 v2

## 0. 판정

한 줄 결론:

> 계획은 승인한다. 다만 1~7강은 **기초 파이프라인 복구용**으로 30~40%만 빠르게 훑고, 8~15강은 **신경망 이론·함수·최적화·일반화·CNN·현대 딥러닝 연결** 중심으로 60~70%를 배정한다.

이 문서는 기존 1~15강 교육목표 설계의 다음 초안이다. 기존 골격인

```text
문제 정의 -> 데이터 표현 -> EDA/전처리 -> 전통 모델
-> neural network learning loop -> backprop -> Keras
-> validation/regularization -> CNN -> final report
```

는 유지한다. v2의 변화는 후반부를 더 깊게 만드는 것이다. 특히 다음 질문에 답할 수 있어야 한다.

```text
왜 Dense인가?
왜 ReLU인가?
왜 sigmoid는 gate에는 유용하지만 deep hidden activation으로는 문제가 생길 수 있는가?
왜 softmax는 분류와 attention 둘 다에 등장하는가?
왜 cross entropy는 classification/language modeling의 기본 loss인가?
왜 Adam은 기본 선택지이지만 항상 최선은 아닌가?
왜 CNN은 image에 적합하고, ViT는 image를 token sequence로 바꾸는가?
왜 LSTM은 sequence에서 vanishing gradient를 완화하려고 gate를 쓰는가?
왜 Transformer는 recurrence 대신 attention으로 token 관계를 직접 학습하는가?
```

---

## 1. Source Basis

이 플랜은 다음 1단계 SSOT와 RAG 산출물을 기준으로 한다.

| 계층 | 사용 소스 | 상태 |
|------|-----------|------|
| 전체 교육목표 | `ML/_inventory/education_plan_1_15_final.md` | 기준 문서 |
| RAG 적용본 | `ML/rag_applied_flat_pack/` | 8, 10, 11, 12, 13, 14, 15강 각 4개 파일 |
| 강별 sidecar | `ML/_inventory/<lecture_id>/nodes.json`, `edges.json`, `evidence.jsonl`, `alignments.jsonl` | 8~15강 검증 완료 |
| 구조 강의록 | `ML/20260430_8강.md` ~ `ML/20260604_15강.md` | 8~15강 후반 핵심 |
| 녹음 전사 | `ML/final_record/*.txt` 및 annotated transcript | 8~15강 transcript evidence |

중요한 제한:

- 5강과 9강은 현재 단독 구조 md가 없다.
- 1~7강은 아직 full sidecar RAG화가 되어 있지 않다.
- 따라서 v2의 깊은 RAG 기반 검증은 8~15강에 집중한다.

---

## 2. 전체 학습 비중 재조정

| 구간 | 기존 역할 | v2 비중 | 학습 방식 | 산출물 |
|------|-----------|--------:|-----------|--------|
| 1~2강 | ML 문제 정의, 확률/분류 기초 | 10% | 빠른 개념 복구 | 문제 정의 5줄 템플릿 |
| 3~4강 | NumPy/Pandas, EDA, 데이터 표현 | 10~15% | `X`, `y`, shape, DataFrame만 실전적으로 복구 | shape/EDA 체크리스트 |
| 5~7강 | 회귀/분류/전통 ML | 10~15% | 중간고사 파이프라인 재사용 수준 | split/scaling/metric 요약표 |
| 8~10강 | Perceptron, MLP, chain rule, GD | 20% | 신경망 이론의 시작점으로 심화 | XOR, learning loop, chain rule 설명 |
| 11~12강 | Backprop, Layer abstraction, vectorized backprop | 20% | 가장 중요. 손계산 <-> 코드 <-> shape 연결 | delta/gradient/shape 워크시트 |
| 13~15강 | Keras, optimizer, validation, CNN | 25~30% | 기말 핵심 + 현대 딥러닝 확장 | DNN/CNN 실험 리포트 |
| 확장 브리지 | LSTM, Attention, ViT, Transformer | 별도 10% 내외 | 시험 외 심화. 단, 신경망 구조 이해에 도움 | 현대 모델 연결 노트 |

운영 원칙:

```text
1~7강 = 빠른 기반 복구
8~15강 = 기말 본체
현대 딥러닝 = 개념 확장 브리지
```

---

## 3. v2 최상위 교육목표

기존 최종 목표:

> 새로운 데이터셋을 보면 `X`, `y`, 문제 유형, 전처리, 모델 후보, loss/metric, 검증 방식, 해석 리포트까지 설계할 수 있는가?

v2 최종 목표:

> 새로운 데이터셋을 보면, 먼저 데이터 구조를 `X/y/tensor`로 해석하고, 문제 유형에 맞는 output layer·loss·metric을 고르며, forward/loss/backward/update가 어떻게 작동하는지 설명하고, validation 결과를 바탕으로 optimizer·regularization·architecture를 조정하며, 필요하면 CNN·RNN/LSTM·Attention/Transformer 계열로 확장할 수 있는가?

이 목표는 모델명을 외우는 것이 아니라, 다음 네 가지 설계 판단을 할 수 있는지를 본다.

| 판단 축 | 질문 | 예시 답 |
|---------|------|---------|
| 데이터 구조 | `X`는 table인가 image인가 sequence인가? | table이면 DNN/전통 ML, image면 CNN/ViT, sequence면 RNN/Transformer 후보 |
| 출력 설계 | target은 연속값인가 class인가 token인가? | regression은 `Dense(1)`, multiclass는 `Dense(K, softmax)` |
| 학습 원리 | gradient는 어디서 어디로 흐르는가? | loss에서 마지막 layer를 거쳐 앞 layer로 chain rule 적용 |
| 일반화 | validation이 나빠지면 무엇을 바꿀 것인가? | regularization, learning rate, architecture, data augmentation |

---

## 4. 전체 개념 그래프 v2

```text
1~4강: 데이터와 문제 정의
X/y, DataFrame, ndarray, shape, axis, preprocessing
        ↓
5~7강: 전통 ML 파이프라인
Regression / Classification / KNN / SVM / DT / RF / metrics
        ↓
8강: Perceptron과 MLP
linear boundary -> XOR 한계 -> hidden layer -> nonlinear representation
        ↓
10강: 학습 수학
derivative -> partial derivative -> gradient -> chain rule -> gradient descent
        ↓
11강: Backprop 손계산
forward cache -> loss -> output delta -> hidden delta -> dW/db
        ↓
12강: Layer abstraction
Dense / ReLU / Sigmoid / SoftmaxCE / Network / mini-batch / vectorization
        ↓
13강: Keras와 Optimizer
Sequential / compile / fit / evaluate / SGD / Momentum / RMSProp / Adam
        ↓
14강: DNN 실전
DataFrame -> EDA -> scaling -> DNN regression/classification -> validation
        ↓
15강: 일반화와 CNN
train/val/test -> loss curve -> regularization -> convolution -> pooling -> CNN
        ↓
확장: 현대 딥러닝
RNN/LSTM -> Attention -> Transformer -> ViT -> LLM / multimodal
```

중앙 허리:

```text
10강 chain rule/GD
  -> 11강 backprop delta
  -> 12강 layer abstraction/vectorized backprop
```

이 구간이 무너지면 13강 Keras와 15강 CNN은 API 암기가 된다.

---

## 5. 1~7강 압축 복구 계획

### 5.1 1~2강: 문제 정의와 확률 출력

| 학습 노드 | 반드시 남길 것 | 가볍게 볼 것 | 후반 연결 |
|-----------|----------------|--------------|-----------|
| T/E/P | 문제를 task, experience, performance로 나누기 | ML 역사 세부 | final report 문제 정의 |
| supervised/unsupervised | `X`, `y`, label 유무 | 세부 알고리즘 암기 | dataset setup |
| regression/classification | target이 연속값인지 class인지 | 모든 예제 반복 | output/loss/metric |
| probability/Bayes | prior, likelihood, posterior | 복잡한 확률 문제 | softmax probability |
| Naive Bayes | class score 비교, argmax | 수치 예제 반복 | cross entropy 분류 사고 |

핵심 연결:

```text
Naive Bayes posterior 비교
  -> logistic/softmax class probability
  -> cross entropy로 확률분포를 학습
```

### 5.2 3~4강: 데이터 표현

| 학습 노드 | 반드시 남길 것 | 후반 연결 |
|-----------|----------------|-----------|
| ndarray | 모델 입력의 기본 단위 | tensor, mini-batch |
| shape | `(samples, features)`, image tensor, batch dimension | DNN/CNN input shape |
| axis | reduction, batch axis, feature axis | vectorized backprop |
| broadcasting | vectorized operation 이해 | gradient 계산 |
| DataFrame | 사람이 이해하는 표 | Boston Housing pipeline |
| EDA | `head`, `info`, `describe`, `isna`, `corr` | data leakage, preprocessing |
| preprocessing | missing value, scaling, encoding | 14~15강 validation 설계 |

핵심 문장:

> Pandas는 사람이 데이터를 이해하는 표이고, NumPy/tensor는 모델이 계산하는 입력이다. 기말 답안은 이 둘 사이의 변환을 말할 수 있어야 한다.

### 5.3 5~7강: 모델과 평가 감각

| 모델/개념 | 한 줄만 남길 것 | 후반 연결 |
|-----------|-----------------|-----------|
| Linear Regression | 연속값 예측, MSE/MAE | DNN regression |
| Logistic/Naive Bayes | 확률 기반 분류 | softmax/cross entropy |
| KNN | 거리 기반 다수결 | scaling 중요성 |
| SVM | margin 기반 경계 | decision boundary |
| Decision Tree | threshold 기반 분할 | overfitting, ensemble |
| Random Forest/Boosting | 여러 모델 결합 | generalization |
| Confusion Matrix | FP/FN 오류 구조 | classification report |

1~7강 복구의 최종 산출물은 긴 요약이 아니라 다음 1장이다.

```text
Problem type -> X/y -> split -> preprocessing -> model candidates -> metric -> report
```

---

## 6. 신경망 심화 트랙

## Phase A. 8강: Perceptron -> MLP -> Representation Learning

기준 RAG 노드:

- `n_ML8.forward_loss_backward_update`
- `n_ML8.xor`
- `n_ML8.mlp_xor`
- `n_ML8.hidden_layer`

한 줄 정의:

> Perceptron은 가중합과 activation으로 입력을 출력으로 바꾸는 가장 작은 신경망 단위이고, MLP는 이를 여러 층으로 쌓아 비선형 표현을 학습하는 구조다.

| 항목 | 심화 목표 |
|------|-----------|
| 이론 | `z = w^T x + b`, `a = phi(z)` 구조 이해 |
| 직관 | 하나의 perceptron은 하나의 직선/초평면만 만든다. |
| 핵심 질문 | 왜 XOR는 단일 perceptron으로 안 되는가? |
| 후속 연결 | MLP -> hidden representation -> DNN -> Transformer FFN |
| 현대 연결 | Transformer의 feed-forward network도 Dense + activation의 반복이다. |

반드시 잡을 문장:

> 층이 깊어진다는 것은 feature representation이 단계적으로 변환된다는 뜻이다.

CNN은 pixel에서 edge/texture/object로, Transformer는 token embedding에서 context-aware representation으로 변환한다. 뿌리는 MLP다.

## Phase B. 10강: Gradient, Chain Rule, Backprop의 수학 기반

기준 RAG 노드:

- `n_ML10.chain_rule`
- `n_ML10.gradient_descent`
- `n_ML10.backprop`

한 줄 정의:

> 신경망 학습은 loss를 줄이기 위해 모든 파라미터의 gradient를 계산하고, 그 반대 방향으로 움직이는 최적화 과정이다.

| 개념 | 왜 중요한가 | 후속 연결 |
|------|-------------|-----------|
| derivative | 한 변수의 변화율 | gradient 기본 |
| partial derivative | 특정 파라미터 하나의 영향 | 각 weight의 책임 계산 |
| gradient | 모든 편미분을 모은 벡터 | optimizer 입력 |
| chain rule | 합성함수의 미분 | backprop의 수학 엔진 |
| gradient descent | loss 감소 방향 update | SGD, Adam의 출발점 |

핵심 문장:

```text
Backpropagation은 새로운 마법 공식이 아니라,
chain rule을 계산 그래프의 뒤쪽에서 앞쪽으로 반복 적용하는 알고리즘이다.
```

LSTM도, CNN도, Transformer도 모두 이 원리로 학습된다.

## Phase C. 11강: Backprop 손계산과 delta 감각

기준 RAG 노드:

- `n_ML11.forward_pass`
- `n_ML11.section_05`
- `n_ML11.section_06`
- `n_ML11.gradient_check`

한 줄 정의:

> 11강은 2-2-1 network를 통해 “각 weight가 loss에 얼마나 책임이 있는가”를 chain rule로 직접 계산하는 단계다.

| 구간 | 봐야 할 것 | 질문 |
|------|------------|------|
| forward pass | cache에 무엇을 저장하는가 | backward 때 왜 cache가 필요한가? |
| output delta | 예측 오차가 마지막 층에 어떻게 들어오는가 | loss와 activation이 delta를 어떻게 만든다? |
| hidden delta | 뒤 layer의 delta가 앞 layer로 어떻게 전달되는가 | 왜 `W.T`가 등장하는가? |
| dW/db | activation과 delta가 gradient를 만든다 | 왜 `np.outer`가 자연스러운가? |
| gradient check | 수치 미분과 analytic gradient 비교 | 구현이 맞는지 어떻게 검증하는가? |

핵심 문장:

> 출력층 delta는 loss에 가까워 짧고, 은닉층 delta는 뒤 layer를 거쳐 loss에 도달하므로 더 긴 chain rule을 갖는다.

## Phase D. 12강: Layer abstraction과 vectorized backprop

기준 RAG 노드:

- `n_ML12.layer_abstraction_activation`
- `n_ML12.vectorized_backprop_batch_dimension_matrix`
- `n_ML12.network_mini_batch`
- `n_ML12.gradient`
- `n_ML12.keras`

한 줄 정의:

> 12강은 11강의 손계산 backprop을 임의 깊이 network와 mini-batch 학습이 가능한 layer 시스템으로 일반화하는 단계다.

| 개념 | 역할 | 현대 연결 |
|------|------|-----------|
| Dense | affine transform `XW + b` | FFN, Q/K/V projection |
| ReLU | 음수 gradient 차단, 비선형성 제공 | GELU, SwiGLU로 확장 |
| Sigmoid | 0~1 squash | LSTM gate |
| SoftmaxCE | logits -> probability -> CE gradient | attention softmax, LM loss |
| Network | layers를 순서대로 실행 | model/block/container |
| mini-batch | 여러 sample을 한 번에 처리 | GPU training, batch size |
| vectorization | loop 대신 matrix operation | scalable deep learning |

핵심 문장:

> 각 layer는 자기 local gradient만 계산하고, Network는 layer를 역순으로 호출한다. 이것이 Keras/PyTorch autograd의 개념적 출발점이다.

## Phase E. 13강: Keras, output/loss/metric, optimizer

기준 RAG 노드:

- `n_ML13.keras`
- `n_ML13.optimizer`
- `n_ML13.sgd_momentum_rmsprop_adam`
- `n_ML13.softmax_cross_entropy`

한 줄 정의:

> 13강은 직접 구현한 신경망 구조를 Keras API로 옮기고, optimizer를 독립된 설계 요소로 분리하는 단계다.

### 회귀와 분류 설계 차이

| 문제 | 출력층 | loss | metric | 이유 |
|------|--------|------|--------|------|
| Regression | `Dense(1)`, activation 없음 | MSE | MAE | target이 연속값 |
| Binary classification | `Dense(1, sigmoid)` | Binary CE | Accuracy/F1 | target이 0/1 |
| Multi-class classification | `Dense(K, softmax)` | Cross Entropy | Accuracy/F1 | target이 K개 class |
| Language modeling | `Dense(V, softmax)` | Cross Entropy | perplexity/accuracy | target이 vocabulary token |

### Softmax와 Cross Entropy 심화

Softmax는 가장 큰 값을 고르는 함수가 아니다. 여러 score/logit을 합이 1인 확률분포처럼 비교 가능한 weight로 바꾸는 함수다.

```text
logits z
  -> softmax(z) = probability distribution
  -> cross entropy = true class probability를 높이는 loss
```

분류에서 softmax는 class probability를 만든다. Attention에서 softmax는 token별 attention weight를 만든다. 구조는 같고 의미가 다르다.

### Optimizer 심화

| Optimizer | 핵심 요인 | 직관 | 언제 중요한가 |
|-----------|-----------|------|---------------|
| SGD | learning rate | gradient 반대 방향으로 이동 | 기본 원리 이해 |
| Momentum | velocity, `mu` | 이전 방향을 누적해 진동 완화 | 골짜기 지형 |
| RMSProp | squared gradient average | gradient 큰 축은 step 축소 | 차원별 scale 차이 |
| Adam | `m`, `v`, bias correction | Momentum + RMSProp | 기본 실험 출발점 |

현대 연결:

| 현재 강의 개념 | 현대 모델 연결 |
|----------------|----------------|
| Adam | Transformer, ViT, LLM 학습의 기본 optimizer 계열 |
| learning rate | warmup, scheduler |
| validation loss | early stopping, checkpoint 선택 |
| overfitting | regularization, dropout, data augmentation |
| batch size | gradient noise, generalization, GPU memory |

## Phase F. 14~15강: Validation, Regularization, CNN

기준 RAG 노드:

- `n_ML14.validation_test`
- `n_ML15.train_validation_test`
- `n_ML15.loss_curve`
- `n_ML15.dropout`
- `n_ML15.convolution_layer`
- `n_ML15.padding_stride_pooling`
- `n_ML15.cnn_classifier_conv_pool_flatten`
- `n_ML15.imagenet_cnn`

한 줄 정의:

> 14~15강은 모델이 학습되는가를 넘어서, 일반화되는가와 데이터 구조에 맞는 architecture인가를 판단하는 단계다.

### 일반화 심화

| 개념 | 왜 필요한가 | 판단 기준 |
|------|-------------|-----------|
| train/validation/test | 학습, 선택, 최종평가 분리 | leakage 방지 |
| loss curve | 학습/과적합 진단 | train loss 감소, val loss 증가면 overfit |
| Dropout | 일부 뉴런 무작위 비활성 | co-adaptation 완화 |
| L2 regularization | weight 크기 제한 | 과도한 복잡도 억제 |
| EarlyStopping | val 성능 악화 전 중단 | epoch 과다 방지 |
| BatchNorm | activation 분포 안정화 | 학습 안정성 향상 |
| Data augmentation | 데이터 다양성 증가 | 이미지 일반화 |

### CNN 심화

| 개념 | 정의 | 연결 |
|------|------|------|
| Filter/Kernel | 작은 학습 가능한 행렬 | local pattern detector |
| Convolution | kernel을 sliding하며 dot product | feature map 생성 |
| Feature map | 특정 패턴의 위치별 반응 | edge/texture/object part |
| Padding | 가장자리 보존, 출력 크기 조절 | spatial resolution |
| Stride | kernel 이동 간격 | downsampling 효과 |
| Pooling | 영역 요약 | translation robustness |
| Flatten | feature map을 vector로 변환 | Dense classifier 연결 |
| CNN | local receptive field 기반 feature extractor | image classification |

핵심 문장:

> Dense는 이미지를 flatten해서 위치 관계를 잃지만, CNN은 local receptive field를 통해 공간 구조를 보존하며 feature map을 만든다.

---

## 7. 현대 딥러닝 연결 트랙

이 트랙은 기말 직접 범위를 넘어가지만, 신경망 개념 내재화를 위해 붙인다. 핵심은 새 모델을 외우는 것이 아니라, 현재 배운 노드가 어떻게 재조합되는지 보는 것이다.

### 7.1 MLP -> DNN -> Transformer FFN

| 현재 배운 것 | 현대 연결 |
|--------------|-----------|
| Dense | Transformer의 Q/K/V projection, feed-forward layer |
| ReLU | GELU, SwiGLU 같은 activation |
| Layer abstraction | Transformer block, Encoder layer, Decoder layer |
| residual path | 깊은 network 학습 안정화 |
| normalization | BatchNorm -> LayerNorm |

Transformer 안에도 MLP가 있다. Attention만 있는 것이 아니다. 각 Transformer block에는 attention sublayer와 feed-forward network가 있다.

### 7.2 Sigmoid -> LSTM gate

| 현재 배운 것 | LSTM 연결 |
|--------------|-----------|
| Sigmoid output 0~1 | gate가 정보를 얼마나 통과시킬지 결정 |
| tanh | 후보 cell state 생성 |
| vanishing gradient | RNN의 장기 의존성 문제 |
| backprop | Backpropagation Through Time |
| elementwise product | forget/input/output gate 계산 |

Sigmoid는 여기서 class probability가 아니라 gate다. 0이면 막고, 1이면 통과시킨다. 같은 함수라도 위치가 바뀌면 의미가 바뀐다.

### 7.3 Softmax -> Attention

| 현재 배운 것 | Attention 연결 |
|--------------|----------------|
| logits | query-key similarity score |
| softmax | token별 attention weight |
| weighted sum | value vector 가중합 |
| matrix multiplication | `QK^T`, softmax, `A @ V` |
| scaling | gradient 안정성 |

```text
score = QK^T / sqrt(d)
attention_weight = softmax(score)
output = attention_weight @ V
```

분류에서 softmax는 class 확률을 만들고, attention에서는 어떤 token을 얼마나 볼지 만든다.

### 7.4 CNN -> ViT

| CNN | ViT |
|-----|-----|
| pixel grid를 local kernel로 처리 | image를 patch token sequence로 처리 |
| local receptive field | global attention |
| feature map | patch embedding sequence |
| pooling/stride로 downsampling | class token 또는 pooling |
| inductive bias 강함 | 데이터가 많을수록 유리한 경향 |

ViT를 이해하려면 두 가지가 필요하다.

1. 이미지는 원래 tensor다.
2. Transformer는 sequence를 처리한다.

그래서 ViT는 이미지를 patch로 잘라 token처럼 만든다.

### 7.5 Cross Entropy -> LLM next-token prediction

| 현재 배운 것 | LLM 연결 |
|--------------|----------|
| 다중분류 | 다음 token을 vocabulary 중 하나로 분류 |
| softmax | vocabulary probability distribution |
| cross entropy | 정답 token의 negative log likelihood |
| validation loss | next-token 예측 일반화 지표 |
| perplexity | CE loss의 지수 변환 |

LLM도 매 step에서는 거대한 다중분류 문제를 푼다.

---

## 8. 실행 플랜

### Step 1. 1~7강 빠른 복구

시간: 1~2회

목표:

- `X`, `y`, problem type, metric을 빠르게 복구한다.
- Pandas/NumPy/EDA/split/scaling을 14~15강에 필요한 만큼만 본다.
- 전통 ML은 DNN/CNN 비교 기준으로만 정리한다.

산출물:

```text
1페이지 파이프라인 카드:
problem -> X/y -> split -> preprocessing -> model -> metric -> report
```

### Step 2. 8강 신경망 입문 재학습

시간: 1회

목표:

- Perceptron 수식
- XOR 한계
- hidden layer 의미
- forward/loss/backward/update 루프

확인 질문:

```text
왜 XOR는 단일 perceptron으로 안 되는가?
hidden layer는 무엇을 대신하는가?
forward와 backward는 어떤 순서로 흐르는가?
```

### Step 3. 10~12강 집중 심화

시간: 3~4회

목표:

1. derivative, partial derivative, gradient, chain rule을 한 장으로 정리
2. 2-2-1 backprop 손계산
3. output delta와 hidden delta 비교
4. `Dense`, `ReLU`, `Sigmoid`, `SoftmaxCE` forward/backward shape 정리
5. mini-batch vectorization 추적

산출물:

```text
Backprop worksheet:
forward cache -> loss -> output delta -> hidden delta -> dW/db -> update
```

### Step 4. 13강 Keras와 optimizer

시간: 1~2회

목표:

- `Sequential`, `Dense`, `compile`, `fit`, `evaluate`를 12강 직접 구현과 대응
- regression/classification output/loss/metric 표 암기보다 설계 원리 이해
- SGD/Momentum/RMSProp/Adam 차이 설명

확인 질문:

```text
왜 compile에서 loss와 optimizer를 고르는가?
왜 회귀는 activation 없는 Dense(1)인가?
왜 다중분류는 softmax + cross entropy인가?
Adam은 왜 Momentum + RMSProp이라고 볼 수 있는가?
```

### Step 5. 14~15강 실전과 CNN

시간: 2~3회

목표:

1. Boston Housing류 DNN regression pipeline 작성
2. Fashion-MNIST Dense baseline 작성
3. Fashion-MNIST CNN 작성
4. train/validation/test 분리
5. loss curve 해석
6. overfitting 대응안 제시
7. CNN convolution/pooling shape 계산

산출물:

```text
DNN/CNN final report skeleton:
data -> preprocessing -> model -> training -> validation -> error analysis -> improvement
```

### Step 6. 확장 세션

시간: 2회

| 세션 | 주제 | 연결 |
|------|------|------|
| 확장 1 | RNN/LSTM | sigmoid gate, tanh, vanishing gradient, BPTT |
| 확장 2 | Attention/Transformer/ViT | softmax, matrix multiplication, Dense projection, patch token |

주의:

> 확장 세션은 기말 직접 범위를 흐리지 않게 한다. 먼저 10~15강을 완성하고, 남은 시간에 현대 모델 브리지를 붙인다.

---

## 9. RAG 구조 v2 제안

### 9.1 Existing RAG Nodes

현재 sidecar에 실제 존재하는 핵심 노드:

| 목적 | existing node |
|------|---------------|
| learning loop | `n_ML8.forward_loss_backward_update` |
| XOR/MLP | `n_ML8.xor`, `n_ML8.mlp_xor` |
| chain rule | `n_ML10.chain_rule` |
| gradient descent | `n_ML10.gradient_descent` |
| backprop bridge | `n_ML10.backprop` |
| layer abstraction | `n_ML12.layer_abstraction_activation` |
| vectorized backprop | `n_ML12.vectorized_backprop_batch_dimension_matrix` |
| output/loss/gradient | `n_ML12.gradient` |
| Keras mapping | `n_ML12.keras`, `n_ML13.keras` |
| optimizer | `n_ML13.optimizer`, `n_ML13.sgd_momentum_rmsprop_adam` |
| softmax/CE | `n_ML13.softmax_cross_entropy` |
| validation | `n_ML14.validation_test`, `n_ML15.train_validation_test`, `n_ML15.loss_curve` |
| regularization | `n_ML15.dropout`, `n_ML15.l2_regularization`, `n_ML15.early_stopping`, `n_ML15.batch_normalization` |
| CNN | `n_ML15.convolution_layer`, `n_ML15.padding_stride_pooling`, `n_ML15.cnn_classifier_conv_pool_flatten` |
| model lineage | `n_ML15.imagenet_cnn` |

### 9.2 Proposed Course-Level Nodes

아래는 아직 sidecar에 없는 course-level 제안 노드다. 실제 RAG로 승격하려면 별도 `course_nodes.md` 또는 `course_edges.json`이 필요하다.

```text
n_course.problem_to_tensor
n_course.loss_metric_output_design
n_course.forward_loss_backward_update
n_course.chain_rule_to_backprop
n_course.layer_to_framework
n_course.softmax_dual_role
n_course.optimizer_dynamics
n_course.generalization_control
n_course.cnn_receptive_field
n_course.sequence_model_bridge
n_course.attention_transformer_bridge
```

### 9.3 Proposed Cross-Lecture Edges

| from | to | edge type | 의미 | status |
|------|----|-----------|------|--------|
| `n_ML8.mlp_xor` | `n_ML10.chain_rule` | `requires_math` | MLP 학습에는 chain rule 필요 | proposed |
| `n_ML10.gradient_descent` | `n_ML13.optimizer` | `generalizes_to` | GD에서 SGD/Adam으로 확장 | proposed |
| `n_ML12.layer_abstraction_activation` | `n_ML13.keras` | `maps_to_framework` | 직접 구현에서 Keras로 | proposed |
| `n_ML13.softmax_cross_entropy` | `n_course.softmax_dual_role` | `modern_bridge` | 분류 softmax와 attention softmax 연결 | proposed |
| `n_ML12.layer_abstraction_activation` | `n_course.sequence_model_bridge` | `modern_bridge` | layer/gate/block 구조로 확장 | proposed |
| `n_ML15.convolution_layer` | `n_course.cnn_receptive_field` | `abstracts` | CNN receptive field 개념화 | proposed |
| `n_ML15.padding_stride_pooling` | `n_course.cnn_receptive_field` | `supports` | feature map 크기와 local structure | proposed |
| `n_ML15.imagenet_cnn` | `n_course.attention_transformer_bridge` | `contrast_bridge` | CNN 계보에서 ViT/Transformer로 확장 | proposed |
| `n_ML15.loss_curve` | `n_course.generalization_control` | `supports` | validation loss 해석 일반화 | proposed |

---

## 10. 최종 v2 요약

```text
1. 1~7강은 빠르게 복구한다.
   목표: X/y, DataFrame/ndarray, split/scaling, regression/classification, metric.

2. 8강부터 진짜 시작한다.
   목표: perceptron, MLP, XOR, representation learning.

3. 10~12강을 가장 깊게 한다.
   목표: chain rule, backprop, delta, Dense/ReLU/Sigmoid/SoftmaxCE, shape.

4. 13강에서 Keras와 optimizer로 연결한다.
   목표: Sequential, compile, fit, evaluate, SGD/Momentum/RMSProp/Adam.

5. 14~15강에서 실전 검증과 CNN으로 완성한다.
   목표: validation, overfitting, regularization, convolution, pooling, CNN.

6. 마지막에 현대 모델 브리지를 붙인다.
   목표: sigmoid -> LSTM gate, softmax -> attention, Dense -> Transformer FFN/QKV, CNN -> ViT patch.
```

학습 방식의 최종 원칙:

> 모든 강의를 같은 밀도로 다시 보지 않는다. 1~7강은 빠른 기반 복구, 8~15강은 신경망 중심 심화, 그 위에 LSTM/Attention/ViT/Transformer를 붙인다.

---

## 11. Validation

| 검증 항목 | 결과 | 근거 |
|-----------|------|------|
| 기존 RAG node 참조 존재성 | PASS | `nodes.json` 기준 existing node 확인 |
| 8~15강 RAG 산출물 기반성 | PASS | `ML/rag_applied_flat_pack/`의 28개 파일 |
| 1~7강 과도한 직접 범위 주장 방지 | PASS | 5강·9강 단독 SSOT 부재를 명시하고 bridge로 처리 |
| 현대 모델 연결 상태 | PASS with proposal | course-level node/edge는 proposed로 분리 |
| 15강 의미 재매핑 반영 | PASS | CNN/종강 transcript evidence 재매핑 이후 node 사용 |

최종 판정:

> v2는 기말 대비용으로 바로 사용 가능하다. 다음 작업은 `n_course.*` 제안 노드를 실제 course-level RAG 파일로 승격하고, 5강·9강 단독 SSOT를 확보해 1~15강 전체 graph를 완성하는 것이다.
