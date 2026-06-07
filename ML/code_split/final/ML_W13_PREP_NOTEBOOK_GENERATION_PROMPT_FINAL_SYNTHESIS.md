# IPYNB Generation Skill Prompt — ML_W13_PREP_VISUAL_LECTURE.ipynb

아래 프롬프트를 노트북 생성 스킬 또는 로컬 Codex CLI 에이전트에 그대로 넣어라.

---

너는 Machine Learning Foundations 수업용 IPYNB Generator다. `ML_W13_PREP_VISUAL_LECTURE.ipynb`를 생성하라. 이 노트북은 Week13 optimizer 과제를 풀기 직전의 companion notebook이며, 정답 제출용 노트북이 아니다.

## 1. 핵심 목표

노트북은 다음 구조를 학습자가 스스로 설명하게 만들어야 한다.

```text
X_batch
→ net.forward(X_batch)
→ loss_fn.forward(logits, y_batch)
→ loss_fn.backward()
→ net.backward(dloss)
→ optimizer.step(net)
```

반드시 다음 문장을 여러 번 반복되는 기준으로 사용하라.

```text
Optimizer는 X/y를 보지 않는다.
Optimizer는 layer가 들고 있는 param과 grad만 읽고 parameter를 update한다.
```

## 2. 입력 파일과 데이터셋 인벤토리

가능하면 아래 JSON을 읽어 dataset registry를 만든다.

```text
ML/code_split/dataset_inventory_for_ML_W13_PREP.json
dataset_inventory_for_ML_W13_PREP.json
/mnt/data/dataset_inventory_for_ML_W13_PREP.json
```

로드 실패 시 기본 registry를 하드코딩해도 된다. 단, notebook 실행은 실패하면 안 된다.

## 3. 반드시 활용할 데이터셋

### Primary

```text
sklearn_iris
- Week13 optimizer comparison 기본 데이터
- Dense(4→16→3) + SoftmaxCE
- accuracy, macro-F1, confusion matrix

toy_logic_gates_xor
- Perceptron 한계, MLP 필요성, chain rule/backward 직관

keras_fashion_mnist
- 이미지 tensor/Flatten/CNN bridge
- 로컬 IDX gzip cache 우선
- 실패 시 sklearn_digits 사용
```

### Secondary

```text
seaborn_titanic
- DataFrame EDA, 결측치, categorical/object dtype, binary target
- 외부 다운로드 금지. JSON profile head_10 또는 embedded fallback 사용

toy_missing_values_week14
- 결측치 탐지, train-only imputation, leakage 설명

toy_scaling_week14
- StandardScaler/MinMaxScaler 비교

toy_categorical_encoding_week14
- one-hot encoding 설명

toy_datetime_features_week14
- datetime feature decomposition 설명
```

### 기본 실행에서 제외

```text
boston_housing_cmu_legacy
uci_appliances_energy_prediction
keras_mnist_or_openml_mnist
daisy_image_missing_local_file
```

이 데이터들은 appendix note로만 설명하라.

## 4. Notebook 구조

아래 heading을 그대로 사용하라.

```text
# ML_W13_PREP_VISUAL_LECTURE

## V00. 전체 지도와 역할 분리
## V01. 데이터·출력·손실·지표 설계
## V02. Gradient Descent와 XOR Bridge
## V03. Dense.backward, ReLU, SoftmaxCE Shape
## V04. Optimizer 4종: SGD, Momentum, RMSProp, Adam
## V05. Week13 Bridge: Iris + Fashion-MNIST
## Final. 체크포인트와 시험 답안 프레임
```

각 섹션은 다음 패턴으로 작성하라.

```text
개념 Markdown
→ 최소 수식
→ 실행 코드
→ 시각화
→ 그래프 해석 질문
→ 답안 scaffold
→ 체크포인트
```

## 5. 공통 import 셀

첫 코드 셀은 아래를 포함한다.

```python
import json
import gzip
import struct
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris, load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

SEED = 42
np.random.seed(SEED)
plt.rcParams["figure.figsize"] = (8, 5)

try:
    import seaborn as sns
    HAS_SEABORN = True
except Exception:
    HAS_SEABORN = False
```

## 6. 필수 구현 1 — Inventory loader

아래 함수를 구현하라.

```python
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

로드에 성공하면 다음 표를 표시한다.

```text
primary / secondary / avoid_or_defer
all dataset_id / availability / shape / task_type / best_fit
```

## 7. 필수 구현 2 — Dataset factory

아래 함수를 구현하라.

```python
def dataset_from_inventory_profile(inventory, dataset_id, prefer="head_10"):
    if inventory is None:
        return None
    for ds in inventory.get("datasets", []):
        if ds.get("dataset_id") == dataset_id:
            prof = ds.get("dataset_profile") or {}
            rows = prof.get(prefer)
            if rows:
                return pd.DataFrame(rows)
    return None


def get_dataset(dataset_id, inventory=None):
    # Return notebook-safe local/embedded data.
    # Never require external download in the default path.
    ...
```

`get_dataset`은 최소한 아래를 지원해야 한다.

```text
sklearn_iris
toy_logic_gates_xor
toy_scaling_week14
toy_missing_values_week14
toy_categorical_encoding_week14
toy_datetime_features_week14
keras_fashion_mnist with fallback sklearn_digits
```

## 8. V00 요구사항

Markdown으로 설명하라.

```text
이 노트북은 제출용 답안 노트북이 아니라 companion notebook이다.
목표는 optimizer 구현법 자체보다, 같은 gradient를 서로 다른 optimizer가 어떻게 다르게 해석하는지 이해하는 것이다.
```

시각화:

```text
G0-B output/loss/metric
→ Gate1 GD/chain rule
→ Gate2 Dense.backward/SoftmaxCE
→ Gate3 Optimizer state
→ Week13 loss curve 해석
```

Matplotlib 또는 Mermaid/NetworkX로 dependency map을 만든다.

## 9. V01 요구사항

사용 데이터:

```text
Titanic fallback DataFrame
toy_missing_values_week14
toy_scaling_week14
toy_categorical_encoding_week14
toy_datetime_features_week14
Iris leakage demo
```

필수 코드:

```text
- 결측치 count table/bar
- StandardScaler vs MinMaxScaler 비교
- split-before-fit 원칙 demo
- regression/binary/multiclass output/loss/metric 표
```

Iris leakage demo는 두 경로를 비교한다.

```text
잘못된 방식: 전체 X에 scaler.fit_transform 후 split
올바른 방식: split 후 X_train에 fit_transform, X_test에 transform
```

성능 차이가 작아도 원칙상 두 번째가 맞다는 설명을 넣어라.

## 10. V02 요구사항

1D loss:

```python
def f1(x):
    return (x - 3) ** 2

def df1(x):
    return 2 * (x - 3)
```

2D loss:

```python
def quad_loss(w):
    return 0.1 * w[0]**2 + 2.0 * w[1]**2

def quad_grad(w):
    return np.array([0.2 * w[0], 4.0 * w[1]])
```

필수 시각화:

```text
- 1D loss curve 위 learning rate별 step path
- 2D contour 위 GD path
- XOR scatter plot
```

XOR 데이터:

```python
xor_df = pd.DataFrame({
    "x0": [0, 0, 1, 1],
    "x1": [0, 1, 0, 1],
    "y":  [0, 1, 1, 0],
})
```

설명:

```text
XOR는 단일 선형 경계로 분리되지 않으므로 MLP와 nonlinear activation이 필요하다.
```

## 11. V03 요구사항

Dense convention은 반드시 아래로 고정한다.

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

반드시 Keras convention과 구분하라.

```text
Keras Dense의 kernel은 보통 (Din, Dout)이다.
이 노트북의 scratch Dense는 강의 코드와 맞춰 W = (Dout, Din)으로 둔다.
```

필수 코드:

```python
B, Din, Dout = 4, 3, 2
X = np.random.randn(B, Din)
W = np.random.randn(Dout, Din)
b = np.random.randn(Dout)
Z = X @ W.T + b

dZ = np.random.randn(B, Dout)
dW = dZ.T @ X
db = dZ.sum(axis=0)
dX = dZ @ W
```

필수 시각화:

```text
- shape table
- dW heatmap
- dX heatmap
- ReLU mask heatmap
- Softmax probability heatmap
- p-y delta heatmap
```

SoftmaxCE demo:

```python
def softmax(logits):
    z = logits - logits.max(axis=1, keepdims=True)
    exp_z = np.exp(z)
    return exp_z / exp_z.sum(axis=1, keepdims=True)
```

`delta = (probs - y_onehot) / B`를 보여주고 의미를 설명하라.

## 12. V04 요구사항

아래 optimizer를 구현하라.

```text
SGD
Momentum
RMSProp
Adam
```

각 optimizer는 2D vector simulation과 `optimizer.step(net)` interface를 모두 지원하도록 설계한다.

필수 parameter iterator:

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

필수 시각화:

```text
- 2D contour 위 optimizer별 trajectory
- optimizer state time-series
- learning-rate sensitivity grid
```

그래프 아래 답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

## 13. V05 요구사항 — Iris optimizer comparison

Iris 준비:

```python
iris = load_iris()
X = iris.data.astype(float)
y = iris.target.astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=SEED, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

모델:

```text
Dense(4, 16) → ReLU → Dense(16, 3)
loss: SoftmaxCE
metrics: accuracy, macro-F1, confusion matrix
```

동일 조건:

```text
same seed
same split
same initial weights
same epoch
same batch size
optimizer only variable
```

필수 결과:

```text
- optimizer별 train loss curve
- optimizer별 test accuracy curve
- final accuracy/macro-F1 table
- confusion matrix
```

## 14. V05 요구사항 — Fashion-MNIST bridge

Fashion-MNIST IDX gzip 파일을 찾는다.

파일명 후보:

```text
train-images-idx3-ubyte.gz
train-labels-idx1-ubyte.gz
t10k-images-idx3-ubyte.gz
t10k-labels-idx1-ubyte.gz
```

탐색 경로:

```text
~/.keras/datasets
~/.keras/datasets/fashion-mnist
ML/code_split
/mnt/data
current working directory
```

실패하면 `load_digits()`를 사용한다.

필수 표시:

```text
original image shape
flattened shape
pixel scaling
sample image grid
class mapping
```

설명:

```text
Flatten MLP는 공간 이웃 관계를 잃는다.
CNN은 kernel/filter가 sliding하며 local pattern을 감지한다.
Convolution layer는 feature extractor이고 뒤의 Dense layer는 classifier다.
```

## 15. Scratch neural network fallback

course 파일 import를 먼저 시도하라.

```text
ML/code_split/0526_neural_network_v2.py
ML/code_split/0519_neural_network.py
```

실패하면 notebook 내부에 최소 구현을 둔다.

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

`Dense`는 아래 convention을 지킨다.

```text
W shape = (Dout, Din)
forward: X @ W.T + b
backward: dW = dZ.T @ X, db = dZ.sum(axis=0), dX = dZ @ W
```

## 16. Final section 요구사항

마지막에 아래 rubric table을 넣어라.

| 통과 항목 | 기준 |
|---|---|
| X/y 판단 | feature matrix와 target vector를 분리 설명 |
| output/loss/metric | 회귀/분류별 Dense, activation, loss, metric 선택 |
| backward shape | dW, db, dX shape와 목적 구분 |
| optimizer 책임 | param/grad만 보고 update한다는 점 설명 |
| curve 해석 | 빠른 수렴과 일반화 성능을 구분 |
| dataset bridge | Iris와 Fashion-MNIST의 역할 차이 설명 |
| CNN bridge | Flatten MLP와 CNN의 구조 차이 설명 |

그리고 아래 질문에 답하는 Markdown scaffold를 넣어라.

```text
1. X와 y는 무엇인가?
2. output layer는 왜 Dense(3)인가?
3. SoftmaxCE에서 p-y는 무엇인가?
4. optimizer.step(net)은 왜 X/y를 보지 않는가?
5. loss curve와 accuracy curve가 서로 다른 정보를 주는 이유는 무엇인가?
6. Adam이 항상 최선이 아닌 이유는 무엇인가?
7. 이미지에서 flatten MLP와 CNN의 차이는 무엇인가?
```

## 17. 품질 게이트

생성 후 아래를 확인하라.

```text
[ ] Restart Kernel & Run All 통과
[ ] 외부 다운로드 없이 기본 경로 실행
[ ] JSON inventory가 없어도 fallback 실행
[ ] split-before-fit 준수
[ ] Dense.backward convention 일관성 유지
[ ] Iris optimizer comparison 실행
[ ] Fashion-MNIST 또는 sklearn_digits bridge 실행
[ ] 모든 주요 그래프 아래 해석 질문/답안 scaffold 존재
[ ] Boston/UCI/uncached MNIST는 기본 실행에서 제외
```

## 18. 최종 보고 형식

노트북 생성 후 다음 형식으로만 보고하라.

```text
생성 파일:
- notebooks/ML_W13_PREP_VISUAL_LECTURE.ipynb
- notebooks/ML_W13_PREP_VISUAL_LECTURE.jupytext.md (생성한 경우)

사용한 데이터셋:
- ...

Fallback:
- ...

검증:
- Restart & Run All: PASS/FAIL
- 남은 수동 조정 지점: ...
```

---
