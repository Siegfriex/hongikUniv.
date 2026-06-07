# ML_W13_PREP_VISUAL_LECTURE — 최종 소스 설계 문서

## 0. 산출물 성격

이 문서는 단순 중복 제거본이 아니다. 입력 기준은 다음 두 축이다.

1. `Week13 Optimizer 시각화 강의 노트북 최종 설계 문서.docx`의 장점: V00~V05 모듈 구조, surrogate loss → chain rule/backward → parameter update → optimizer state → learning dynamics 해석 순서, 시각화 중심 수업 설계, 품질 게이트, 그래프 기반 답안 scaffold.
2. `dataset_inventory_for_ML_W13_PREP.json`의 장점: 실제 로컬/내장/외부 데이터셋 후보, availability, Week별 데이터 매핑, primary/secondary/defer 정책, dataset profile/head metadata.

최종 목표는 로컬 Codex CLI 에이전트가 이 문서를 읽고 `ML_W13_PREP_VISUAL_LECTURE.ipynb`를 생성하거나, 별도의 IPYNB Generator에 넘길 수 있는 확정 사양을 제공하는 것이다.

## 1. 최종 설계 결론

최종 노트북은 Week13 optimizer 구현 과제를 그대로 풀어주는 답안지가 아니라, 과제를 풀기 전에 필요한 개념·수식·shape·시각화·실험 해석을 한 줄로 연결하는 companion notebook이다.

핵심 학습 루프는 아래로 고정한다.

```text
X_batch
→ net.forward(X_batch)
→ loss_fn.forward(logits, y_batch)
→ loss_fn.backward()
→ net.backward(dloss)
→ optimizer.step(net)
```

핵심 문장은 다음이다.

```text
Layer/Network는 forward와 backward를 통해 prediction, loss, gradient를 만든다.
Optimizer는 X/y를 보지 않는다.
Optimizer는 layer가 들고 있는 param과 grad만 읽고, update rule에 따라 param을 이동시킨다.
```

이 문장 때문에 노트북은 `optimizer 4종 구현`보다 `gradient가 만들어진 뒤 parameter가 어떻게 움직이는가`를 시각적으로 보여주는 데 초점을 둔다.

## 2. 로컬 Codex CLI 에이전트에게 부여할 작업

Codex CLI 에이전트는 아래 파일을 생성한다.

```text
notebooks/ML_W13_PREP_VISUAL_LECTURE.ipynb
notebooks/ML_W13_PREP_VISUAL_LECTURE.jupytext.md   # 가능하면 생성
notes/ML_W13_PREP_VISUAL_LECTURE_SOURCE.md         # 본 문서 복사본
```

생성 원칙은 다음이다.

```text
- 원본 강의 파일, 원본 JSON inventory, 기존 code_split 파일을 수정하지 않는다.
- notebook은 외부 다운로드 없이 기본 실행 가능해야 한다.
- JSON inventory가 없거나 경로가 다르면 fallback dataset을 사용한다.
- Restart Kernel & Run All 기준으로 끝까지 실행되어야 한다.
- 각 시각화 아래에는 해석 질문과 답안 scaffold를 둔다.
```

## 3. 두 입력 문서의 장점 통합 방식

### 3.1 DOCX에서 채택할 포인트

| 채택 요소 | 최종 반영 방식 |
|---|---|
| V00~V05 모듈 구조 | 최종 notebook의 top-level heading으로 유지 |
| surrogate loss → chain rule/backward → parameter update → optimizer state → learning dynamics | notebook 서사의 기본 순서로 사용 |
| optimizer는 X/y가 아니라 param/grad를 본다 | V00, V03, V04, V05에서 반복되는 핵심 문장으로 배치 |
| Matplotlib 기본, Seaborn 보조, Plotly/Altair 선택 | 시각화 스택 정책으로 명시 |
| Restart & Run All, hidden state 방지, split-before-fit, seed 고정 | 품질 게이트로 고정 |
| 그래프 바로 아래 답안 scaffold | V04/V05에서 Part 5형 해석 훈련으로 배치 |

### 3.2 JSON inventory에서 채택할 포인트

| 채택 요소 | 최종 반영 방식 |
|---|---|
| primary: `sklearn_iris`, `toy_logic_gates_xor`, `keras_fashion_mnist` | V02~V05의 기본 데이터 축 |
| secondary: `seaborn_titanic`, `toy_missing_values_week14`, `toy_scaling_week14` | V01 전처리·leakage·metric 블록 |
| avoid/defer: Boston, UCI Energy, uncached MNIST | appendix note로만 사용 |
| dataset shape/profile/head metadata | inventory summary table과 fallback DataFrame 생성에 사용 |
| lecture_date_band_map | 필요 시 notebook의 “왜 이 데이터가 여기서 등장하는가” 설명에 사용 |

## 4. 데이터셋 사용 정책

### 4.1 기본 데이터 흐름

```text
V00: 데이터 없음. 전체 의존성 지도.
V01: Titanic/toy_missing/toy_scaling/toy_categorical/toy_datetime + Iris leakage demo.
V02: toy_loss_surface + XOR.
V03: XOR 또는 synthetic batch + Fashion-MNIST/digits shape bridge.
V04: synthetic 1D/2D loss surface + optimizer trajectory.
V05: Iris optimizer comparison + Fashion-MNIST subset bridge.
```

### 4.2 JSON inventory 기반 전체 데이터셋 명세

| dataset_id | availability | shape/profile | task_type | 최종 노트북 사용처 |
|---|---|---:|---|---|
| `seaborn_titanic` | local_cache_available | [891, 15] | binary classification target candidate: survived | V01 split/scaling/leakage의 DataFrame EDA 전 단계; 결측치 처리와 leakage 설명; categorical/object dtype 처리 예시 |
| `sklearn_iris` | sklearn_builtin_available | [150, 6] | single-label multiclass classification | V05 optimizer 비교의 실제 small classification data; SoftmaxCE / Dense(3) / macro-F1 / confusion matrix; 같은 초기화와 optimizer별 loss curve 비교 |
| `toy_dog_size_knn_svm` | embedded_in_notebook_code | [16, 5] | binary classification toy | V01 classification metric toy; V02 gradient 이전 decision boundary 직관; small scatterplot demo |
| `toy_logic_gates_xor` | embedded_in_python_and_notebooks | [4, 8] | binary classification toy / non-linear separability | V02 gradient descent/chain rule intro; V03 Dense.backward shape demo; XOR loss curve and decision boundary visual |
| `toy_missing_values_week14` | embedded_in_notebook_code | [5, 3] | 결측치 탐지/삭제/대체와 train-only imputation leakage 설명 | V01 split/scaling/leakage preprocessing mini-demo |
| `toy_categorical_encoding_week14` | embedded_in_notebook_code | [4, 2] | OneHotEncoding vs ordinal encoding 설명 | V01 split/scaling/leakage preprocessing mini-demo |
| `toy_datetime_features_week14` | embedded_in_notebook_code | [5, 7] | datetime -> year/month/hour/dayofweek/is_weekend 분해 | V01 split/scaling/leakage preprocessing mini-demo |
| `toy_scaling_week14` | embedded_in_notebook_code | [4, 2] | StandardScaler/MinMaxScaler scale 차이 시각화 | V01 split/scaling/leakage preprocessing mini-demo |
| `keras_fashion_mnist` | local_idx_gzip_cache_available_direct_read | {'train_images': [60000, 28, 28], 'train_labels': [60000], 'test_images': [10000, 28, 28], 'test_labels': [10000]} | single-label multiclass image classification | V05 Week13 bridge harder optimizer comparison candidate; V03 tensor/flatten/CNN contrast; loss curve/accuracy barplot |
| `keras_mnist_or_openml_mnist` | referenced_but_not_cached_locally_or_requires_download | — | single-label multiclass image classification | V05 optimizer comparison harder target than Iris; loss curve / accuracy comparison; flatten vs tensor visualization |
| `boston_housing_cmu_legacy` | referenced_by_url_not_local_file | — | tabular regression | V01 MSE/MAE/RMSE/inverse_transform; regression output Dense(1) visual; ethical dataset caution example |
| `uci_appliances_energy_prediction` | referenced_by_url_not_local_file | — | time-aware tabular regression | V01 split/scaling/leakage real regression extension; train/val/test and overfitting loss curves; regularization bridge after optimizer |
| `daisy_image_missing_local_file` | referenced_but_source_image_missing_in_code_split | — | image array manipulation | not recommended unless image file is restored |

### 4.3 사용 우선순위

#### Tier A — 반드시 사용

| dataset_id | 이유 | 모듈 |
|---|---|---|
| `sklearn_iris` | 작고 빠르며 Week13 optimizer 비교에 가장 적합. `Dense(4→16→3) + SoftmaxCE` 구조를 바로 만들 수 있음 | V01, V05 |
| `toy_logic_gates_xor` | Perceptron 한계, 비선형성, MLP, chain rule/backward 직관에 최적 | V02, V03 |
| `keras_fashion_mnist` | 이미지 tensor, flatten, CNN bridge, Week14 연결에 적합. 로컬 IDX gzip cache 우선 사용 | V03, V05 |

#### Tier B — 적극 사용

| dataset_id | 이유 | 모듈 |
|---|---|---|
| `seaborn_titanic` | 결측치, categorical/object dtype, binary target, EDA 흐름 설명에 적합 | V01 |
| `toy_missing_values_week14` | train-only imputation과 leakage 시각화에 즉시 사용 가능 | V01 |
| `toy_scaling_week14` | StandardScaler/MinMaxScaler 차이 시각화에 즉시 사용 가능 | V01 |
| `toy_categorical_encoding_week14` | one-hot encoding과 ordinal encoding 차이 설명 | V01 appendix |
| `toy_datetime_features_week14` | datetime feature decomposition 설명 | V01 appendix |

#### Tier C — optional / appendix

| dataset_id | 처리 |
|---|---|
| `toy_dog_size_knn_svm` | decision boundary 직관 보조. optimizer 본체에서는 사용하지 않음 |
| `keras_mnist_or_openml_mnist` | 캐시 없을 수 있으므로 기본 경로 제외. Fashion-MNIST 또는 sklearn_digits로 대체 |
| `boston_housing_cmu_legacy` | legacy/윤리/외부 URL 이슈. 회귀 output/loss note로만 언급 |
| `uci_appliances_energy_prediction` | 크고 외부 의존. Week14 regularization extension note로만 언급 |
| `daisy_image_missing_local_file` | 원본 이미지 누락. 사용 금지, Fashion-MNIST로 대체 |

## 5. 최종 Notebook 모듈 구조

DOCX의 V00~V05 구조를 유지하되, JSON 데이터셋을 더 촘촘히 배치한다.

### V00. 전체 지도와 역할 분리

목표: Week13 optimizer 과제가 어떤 노드 조합인지 첫 화면에서 고정한다.

필수 내용:

```text
G0-B output/loss/metric
→ Gate1 gradient / chain rule
→ Gate2 Dense.backward / SoftmaxCE
→ Gate3 optimizer state
→ Week13 loss curve interpretation
```

필수 산출물:

```text
- dependency map
- forward/loss/backward/update flow diagram
- Layer vs Optimizer responsibility table
```

체크포인트:

```text
나는 optimizer가 gradient를 계산하는 것이 아니라, 계산된 gradient로 parameter를 움직이는 주체임을 설명할 수 있다.
```

### V01. 데이터·출력·손실·지표 설계

목표: optimizer 비교 전에 “무엇을 예측하고, 무엇을 최소화하며, 무엇으로 평가할지”를 확정한다.

사용 데이터:

```text
seaborn_titanic 또는 JSON head_10 fallback
toy_missing_values_week14
toy_scaling_week14
toy_categorical_encoding_week14
toy_datetime_features_week14
sklearn_iris leakage demo
```

필수 내용:

```text
- X/y, feature/target
- DataFrame vs ndarray/tensor
- train/test 또는 train/validation/test split
- fit은 train에만, transform은 val/test에만
- regression vs binary classification vs multiclass classification
- output layer / activation / loss / metric 결정표
```

필수 시각화:

```text
- 결측치 count table/bar
- scaling 전후 비교 plot
- classification label countplot
- regression error curve: abs error vs squared error
- confusion matrix toy example
```

체크포인트:

```text
나는 문제를 보면 output dimension, activation, loss, metric을 결정할 수 있다.
```

### V02. Gradient Descent와 Chain Rule 직관

목표: optimizer가 작동할 수 있는 전제인 gradient와 learning rate를 눈으로 이해한다.

사용 데이터:

```text
toy quadratic surface
toy_logic_gates_xor
```

필수 내용:

```text
- gradient = loss 증가 방향
- gradient descent = gradient 반대 방향 이동
- learning rate가 작으면 느리고, 크면 overshoot/oscillation/divergence
- XOR는 단일 선형 경계로 풀 수 없음
- MLP + nonlinear activation이 필요한 이유
```

필수 시각화:

```text
- 1D loss curve 위 lr별 step path
- 2D contour 위 GD path
- XOR scatter + decision boundary impossibility
```

체크포인트:

```text
나는 gradient와 learning rate가 parameter 이동 경로를 어떻게 바꾸는지 설명할 수 있다.
```

### V03. Dense.backward, ReLU, SoftmaxCE shape 블록

목표: Week12에서 만든 gradient가 Week13 optimizer의 입력이 되는 구조를 배열 수준으로 고정한다.

사용 데이터:

```text
synthetic mini-batch
XOR mini-batch
Fashion-MNIST 또는 sklearn_digits shape bridge
```

강의 convention은 아래로 고정한다.

```text
X:  (B, Din)
W:  (Dout, Din)
b:  (Dout,)
Z = X @ W.T + b
Z:  (B, Dout)
dZ: (B, Dout)
dW = dZ.T @ X       -> (Dout, Din)
db = dZ.sum(axis=0) -> (Dout,)
dX = dZ @ W         -> (B, Din)
```

주의:

```text
Keras Dense의 kernel convention은 보통 (Din, Dout)이다.
이 노트북의 scratch convention은 강의 코드와 맞춰 W = (Dout, Din)으로 둔다.
두 convention을 섞지 말고 별도 표로 구분한다.
```

필수 시각화:

```text
- shape table
- dW/db/dX heatmap
- ReLU mask heatmap
- Softmax probability heatmap
- p-y delta heatmap
```

체크포인트:

```text
dW/db는 현재 layer의 parameter update용 gradient이고, dX는 이전 layer로 전달할 gradient다.
```

### V04. Optimizer 4종 비교

목표: 같은 gradient를 서로 다른 optimizer가 어떻게 다르게 재사용하는지 보여준다.

필수 optimizer:

```text
SGD
Momentum
RMSProp
Adam
```

필수 내용:

```text
SGD: 현재 gradient만 사용
Momentum: velocity, 이전 이동 방향 누적
RMSProp: squared gradient moving average로 좌표별 step 조정
Adam: first moment + second moment + bias correction
```

필수 시각화:

```text
- 2D contour 위 optimizer별 trajectory
- optimizer별 state time-series: velocity, squared average, effective step
- learning-rate sensitivity grid
```

필수 interface:

```python
optimizer.step(net)
```

이 interface는 다음 순회 방식을 지원해야 한다.

```python
for layer in net.layers:
    for name, param, grad in iter_params_and_grads(layer):
        update(param, grad)
```

체크포인트:

```text
나는 backward가 만든 grad는 같아도 optimizer가 다르면 parameter 이동 경로가 달라진다는 것을 설명할 수 있다.
```

### V05. Week13 과제 브리지: Iris + Fashion-MNIST

목표: V00~V04를 실제 Week13 과제형 분석으로 연결한다.

사용 데이터:

```text
sklearn_iris: 기본 optimizer comparison
keras_fashion_mnist: image tensor / flatten / harder data bridge
fallback: sklearn_digits
```

Iris 기본 모델:

```text
X: (150, 4)
y: 3 classes
split: stratify=y
scaler: StandardScaler fit on X_train only
model: Dense(4, 16) → ReLU → Dense(16, 3)
loss: SoftmaxCE
metrics: accuracy, macro-F1, confusion matrix
```

실험 공정성:

```text
- 같은 seed
- 같은 train/test split
- 같은 initial weights
- 같은 epoch
- 같은 batch size
- optimizer만 변경
```

필수 결과:

```text
- optimizer별 train loss curve
- optimizer별 test accuracy curve
- final accuracy/macro-F1 table
- confusion matrix
- answer scaffold
```

그래프 아래 답안 scaffold:

```text
관찰: 어떤 optimizer가 어느 구간에서 빠르게 loss를 낮췄는가?
원인: 해당 optimizer의 update state가 어떤 역할을 했는가?
제한: Iris가 쉬운 데이터라 최종 accuracy 차이가 작을 수 있는가?
결론: 새 문제의 baseline optimizer로 무엇을 둘 것인가?
```

Fashion-MNIST bridge:

```text
- image shape: (N, 28, 28)
- flattened shape: (N, 784)
- pixel scaling: /255.0
- sample grid
- MLP subset experiment optional
- CNN은 다음 강 bridge note로만 설명
```

체크포인트:

```text
Flatten MLP는 이미지의 공간 이웃 관계를 잃고, CNN은 kernel/filter로 local pattern을 감지한다.
```

## 6. 구현 필수 함수 명세

### 6.1 Inventory loader

```python
from pathlib import Path
import json

INVENTORY_PATH_CANDIDATES = [
    Path("ML/code_split/dataset_inventory_for_ML_W13_PREP.json"),
    Path("dataset_inventory_for_ML_W13_PREP.json"),
    Path("/mnt/data/dataset_inventory_for_ML_W13_PREP.json"),
]

def load_inventory(path_candidates=INVENTORY_PATH_CANDIDATES):
    for p in path_candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f), p
    return None, None
```

### 6.2 Dataset factory

```python
def get_dataset(dataset_id, inventory=None):
    "Return a small, notebook-safe dataset object. Never require external download in default path."
    if dataset_id == "sklearn_iris":
        ...
    if dataset_id == "toy_logic_gates_xor":
        ...
    if dataset_id == "toy_scaling_week14":
        ...
    if dataset_id == "toy_missing_values_week14":
        ...
    if dataset_id == "keras_fashion_mnist":
        ...
    if dataset_id == "sklearn_digits_fallback":
        ...
```

### 6.3 Parameter/gradient iterator

```python
def iter_params_and_grads(layer):
    if hasattr(layer, "params_and_grads"):
        yield from layer.params_and_grads()
        return
    if hasattr(layer, "W") and hasattr(layer, "dW"):
        yield "W", layer.W, layer.dW
    if hasattr(layer, "b") and hasattr(layer, "db"):
        yield "b", layer.b, layer.db
```

### 6.4 Minimal scratch neural network fallback

Codex CLI는 기존 `0526_neural_network_v2.py` 또는 `0519_neural_network.py`를 우선 import한다. 실패하면 notebook 내부에 최소 구현을 둔다.

필수 클래스:

```text
Dense
ReLU
SoftmaxCE
Network
SGD
Momentum
RMSProp
Adam
```

필수 convention:

```text
Dense.W shape = (Dout, Din)
Dense.forward(X): X @ W.T + b
Dense.backward(dZ): dW, db, dX 계산
Optimizer.step(net): param/grad 순회 후 in-place update
```

## 7. 시각화 스택 정책

| 도구 | 사용처 |
|---|---|
| Matplotlib | 기본. loss curve, contour, trajectory, image grid |
| Seaborn | 있으면 사용. countplot, heatmap, pairplot, distribution |
| Plotly | 선택. lr slider 또는 interactive trajectory |
| Altair | 선택. 표 기반 인터랙티브 encoding 설명 |
| NetworkX/Mermaid | 선택. dependency map |

기본 실행은 Matplotlib + Pandas + NumPy + scikit-learn만으로 가능해야 한다.

## 8. Notebook 품질 게이트

Codex CLI는 생성 후 아래를 확인한다.

```text
[ ] Restart Kernel & Run All 통과
[ ] inventory JSON이 없어도 fallback으로 실행 가능
[ ] 외부 다운로드 없이 기본 경로 실행
[ ] split-before-fit 원칙 준수
[ ] optimizer 비교에서 seed/init/split/epoch/batch 고정
[ ] Dense.backward shape convention이 문서와 코드에서 일치
[ ] Iris optimizer comparison 실행
[ ] Fashion-MNIST 또는 sklearn_digits bridge 실행
[ ] 각 주요 그래프 아래 answer scaffold 존재
[ ] Boston/UCI/uncached MNIST는 기본 실행 경로 제외
```

## 9. 비목표

```text
- 제출용 Week13 정답 자동 생성
- 대형 데이터셋 full training
- CNN 완전 구현
- Boston/UCI 외부 다운로드 기본 실행
- 최신 논문 survey 중심 문서
- 로컬 강의 원본 파일 수정
```

## 10. 최종 Codex CLI 실행 지시 요약

Codex CLI에게 아래 순서로 지시한다.

```text
1. workspace에서 ML/code_split 파일 존재 여부를 확인한다.
2. dataset_inventory_for_ML_W13_PREP.json을 읽는다.
3. 가능한 course neural_network 파일을 import 시도한다.
4. import 실패 시 notebook 내부 fallback 구현을 사용한다.
5. V00~V05 구조로 notebook을 생성한다.
6. Iris optimizer comparison을 반드시 포함한다.
7. Fashion-MNIST cache를 찾고, 실패 시 sklearn_digits로 fallback한다.
8. 모든 시각화 아래에 해석 질문과 답안 scaffold를 넣는다.
9. notebook을 Restart & Run All로 검증한다.
10. 최종 생성 파일과 fallback 여부를 보고한다.
```
