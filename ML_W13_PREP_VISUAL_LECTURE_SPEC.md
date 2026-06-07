# ML_W13_PREP_VISUAL_LECTURE_SPEC

## 0. Context

이 문서는 `week13_homework (1).ipynb`를 대체하지 않는 companion notebook인
`ML_W13_PREP_VISUAL_LECTURE.ipynb`의 구현 명세다.

목표는 Week13 Optimizer 과제에 들어가기 전, 사용자가 아래 흐름을 하나의 실행 가능한
시각화 강의 노트북에서 연결해 보게 하는 것이다.

```text
G0-B split/scaling/output/loss/metric
-> Gate1 gradient descent / chain rule
-> Gate2 Dense.backward / ReLU / SoftmaxCE / Network
-> Gate3 SGD / Momentum / RMSProp / Adam
-> Week13 optimizer 비교 과제
```

이 노트북은 정답 노트북이 아니다. 사용자가 각 셀을 실행하면서 데이터, loss, gradient,
layer backward, optimizer update, loss curve, accuracy 변화를 눈으로 확인하는 직관 생성
노트북이다.

## 1. Artifacts

| 산출물 | 역할 | 상태 |
|---|---|---|
| `ML_W13_PREP_VISUAL_LECTURE.ipynb` | 시각화 중심 companion notebook | 생성 대상 |
| `ML_W13_PREP_VISUAL_LECTURE_SPEC.md` | 본 설계 명세 | 현재 문서 |
| `ML/code_split/dataset_inventory_for_ML_W13_PREP.json` | 강의 파일 내 데이터셋 후보 인벤토리 | 생성됨 |
| `data/ML_W13_PREP/` | 선택적 보조 데이터 경로 | 필요 시 생성 |
| `week13_homework (1).ipynb` | 제출용 숙제 | 수정 대상 아님 |

## 2. Goals

- G0-B의 split-before-fit, leakage, output/loss/metric 선택을 시각화한다.
- loss가 gradient의 출발점이라는 점을 보여준다.
- backprop이 layer별 `param`에 대한 `grad`를 만든다는 점을 보여준다.
- optimizer는 `X/y`가 아니라 이미 계산된 `param/grad/state`만 본다는 점을 보여준다.
- SGD, Momentum, RMSProp, Adam의 update rule 차이를 같은 objective와 같은 초기값에서 비교한다.
- Week13 과제의 loss curve와 accuracy를 해석하는 문장 프레임을 제공한다.

## 3. Non-Goals

- `week13_homework (1).ipynb`의 제출 답안을 직접 작성하지 않는다.
- 범용 딥러닝 프레임워크를 새로 만들지 않는다.
- CNN 전체 강의를 확장하지 않는다.
- 외부 다운로드가 필수인 대형 데이터셋에 노트북 실행을 의존시키지 않는다.

## 4. Design Principles

| 원칙 | 구현 기준 |
|---|---|
| loss와 metric 병렬 제시 | loss curve와 accuracy 또는 대응 metric을 함께 표시 |
| backward와 optimizer 책임 분리 | `loss.backward()` / `net.backward()` 이후 `optimizer.step()` 구조 노출 |
| split-before-fit | scaler/encoder/imputer는 train에만 `fit` |
| clean-kernel 재현성 | `Restart Kernel & Run All` 기준으로 끝까지 실행 |
| 셀 단일성 | 한 셀은 한 개념, 한 계산, 한 시각화에 가깝게 유지 |
| state 가시화 | Momentum/RMSProp/Adam 내부 state를 최소 1회 이상 표 또는 그래프로 노출 |
| 외부 의존 최소화 | 기본은 synthetic data와 로컬 builtin/cache dataset 사용 |

## 5. Dataset Strategy

데이터셋 후보는 `ML/code_split/dataset_inventory_for_ML_W13_PREP.json`을 기준으로 한다.

### 5.1 Primary Datasets

| dataset_id | 용도 | 이유 |
|---|---|---|
| `sklearn_iris` | Week13 optimizer 비교 bridge | 이미 Week13 예제와 연결됨, 작고 빠름, SoftmaxCE/Dense(3)에 적합 |
| `toy_logic_gates_xor` | Gate1/Gate2 backprop 직관 | Perceptron 한계, XOR, MLP, loss curve를 가장 작게 보여줌 |
| `keras_fashion_mnist` | image tensor / Flatten / CNN 대비 | 로컬 IDX gzip cache 직접 읽기 가능, MNIST 대체 가능 |

### 5.2 Secondary Datasets

| dataset_id | 용도 |
|---|---|
| `seaborn_titanic` | missing value, categorical dtype, leakage 전 단계 EDA |
| `toy_missing_values_week14` | train-only imputation 설명 |
| `toy_scaling_week14` | StandardScaler/MinMaxScaler 차이 |
| `toy_categorical_encoding_week14` | one-hot / ordinal encoding 차이 |

### 5.3 Deferred Datasets

| dataset_id | 보류 이유 |
|---|---|
| `keras_mnist_or_openml_mnist` | 현재 로컬 cache 없음, 다운로드 의존 |
| `boston_housing_cmu_legacy` | 외부 URL 의존 및 윤리 경고 필요 |
| `uci_appliances_energy_prediction` | 실전성은 높지만 크고 외부 URL 의존 |
| `daisy_image_missing_local_file` | `daisy.jpg` 원본 누락 |

## 6. Notebook Module Architecture

```text
V00 = 전체 개념 지도
V01 = G0-B: split/scaling/leakage + output/loss/metric
V02 = Gate1: gradient descent / chain rule
V03 = Gate2: Dense.backward / ReLU / SoftmaxCE / Network
V04 = Gate3: SGD / Momentum / RMSProp / Adam
V05 = Week13 과제 브리지: Iris/Fashion-MNIST optimizer 비교와 그래프 해석
V06 = 최종 체크포인트와 AI 질문 템플릿
```

각 checkpoint는 아래 셀 문법을 따른다.

```text
1. Markdown: 현재 노드 / 선행 노드 / 후속 노드
2. Markdown: 이론·수식 설명
3. Code: toy data 또는 로컬 small data 생성/로드
4. Code: 계산 과정 확인
5. Code: 시각화
6. Markdown: 관찰 결과 해석
7. Code: 사용자가 바꿔볼 파라미터
8. Markdown: 체크포인트 질문
```

## 7. Required Visualizations

| 노드 | 핵심 개념 | 시각화 |
|---|---|---|
| V01 split/scaling | `fit`은 train에만 | train vs full scaler histplot |
| V01 loss/metric | MSE/MAE/RMSE 차이 | error penalty curve |
| V01 classification | sigmoid/softmax/CE | sigmoid curve, softmax heatmap, CE curve |
| V01 metric | F1 조화평균 | arithmetic vs harmonic line plot |
| V01 ordinal | ordinal cost matrix | heatmap |
| V02 GD | `theta <- theta - lr * grad` | 1D/2D trajectory |
| V02 chain rule | local derivative 곱 | 계산 그래프 table |
| V03 Dense | `dW/db/dX` | matrix heatmap |
| V03 ReLU | mask | function/derivative plot |
| V03 SoftmaxCE | `probs - y_onehot` | gradient heatmap |
| V04 optimizer | update rule 차이 | contour trajectory |
| V05 bridge | optimizer 비교 | loss curve / accuracy barplot |

## 8. Common Imports

```python
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

np.random.seed(42)
rng = np.random.default_rng(42)

plt.rcParams["figure.figsize"] = (8, 5)
plt.rcParams["axes.grid"] = True
sns.set_theme(style="whitegrid")
```

## 9. Core Execution Interface

Week13 optimizer 비교는 동일 스키마로 결과를 기록한다.

```python
def run_experiment(
    name,
    build_net_fn,
    fit_fn,
    optimizer,
    X_train,
    y_train,
    X_test,
    y_test,
    *,
    seed=0,
    epochs=20,
    batch_size=32,
):
    np.random.seed(seed)
    net = build_net_fn()
    history = fit_fn(
        net,
        X_train,
        y_train,
        optimizer=optimizer,
        epochs=epochs,
        batch_size=batch_size,
        seed=seed,
    )
    logits = net.forward(X_test)
    y_pred = logits.argmax(axis=1)
    test_acc = (y_pred == y_test).mean()

    return {
        "name": name,
        "seed": seed,
        "lr": getattr(optimizer, "lr", None),
        "losses": history["loss"],
        "test_acc": test_acc,
    }
```

핵심은 모든 비교 실험이 같은 필드를 갖는 결과 객체를 반환하게 하는 것이다.

## 10. Module Details

### V00. 전체 개념 지도

목표:
- G0-B에서 Week13 optimizer까지의 의존성을 한 화면에 고정한다.

필수 메시지:

```text
X_batch
-> net.forward
-> loss_fn.forward
-> loss_fn.backward
-> net.backward
-> optimizer.step(net)
```

체크포인트:
- loss는 어디서 계산되는가?
- gradient는 누가 계산하는가?
- param은 어디에 있는가?
- optimizer는 무엇을 보고 움직이는가?
- loss curve는 무엇의 결과인가?

### V01. G0-B 시각화

필수 submodule:
- split / scaling / leakage
- MSE / MAE / RMSE와 gradient
- sigmoid / softmax / Cross Entropy
- precision / recall / F1
- ordinal target cost matrix

데이터:
- 기본 synthetic data
- Titanic 또는 Week14 toy data 선택 사용 가능

### V02. Gate1: Gradient Descent / Chain Rule

필수 실험:

```text
L(w) = (w - 3)^2
dL/dw = 2(w - 3)
w <- w - lr * dL/dw
```

필수 시각화:
- lr별 1D trajectory
- 2D contour trajectory
- chain-rule table

### V03. Gate2: Dense.backward / ReLU / SoftmaxCE / Network

필수 실험:
- Dense forward/backward shape heatmap
- ReLU mask
- SoftmaxCE gradient `probs - y_onehot`
- XOR 또는 Iris small network loss curve

핵심 질문:
- `dW`는 왜 `W`와 같은 shape인가?
- `db`는 왜 output neuron 수만큼 생기는가?
- `dX`는 왜 앞 layer로 넘기는 gradient인가?

### V04. Gate3: Optimizer 비교

비교 대상:
- SGD
- Momentum
- RMSProp
- Adam

필수 원칙:
- 같은 objective
- 같은 start point
- 같은 seed
- 같은 step 수
- optimizer state를 최소 1회 이상 출력

필수 시각화:
- 2D contour path
- loss per step
- state table

### V05. Week13 과제 브리지

기본 데이터:
- `sklearn_iris`

선택 확장:
- `keras_fashion_mnist` subset

필수 산출:
- optimizer별 loss curve
- optimizer별 test accuracy barplot
- confusion matrix 또는 class별 metric
- Part 5 서술형 답안 템플릿

### V06. 최종 체크포인트와 AI 질문 템플릿

최종 사용자는 아래 문장을 설명할 수 있어야 한다.

```text
데이터는 DataFrame에서 의미와 전처리를 확정하고,
ndarray/tensor로 계산 가능하게 만든다.
loss는 예측 오류를 수치화하고 gradient의 출발점이 되며,
backprop은 각 layer의 param에 대한 grad를 계산한다.
optimizer는 그 grad를 이용해 param을 움직이고,
optimizer별 update rule 차이는 loss curve와 accuracy 차이로 나타난다.
```

## 11. Quality Gates

| 게이트 | 통과 조건 |
|---|---|
| clean run | `Restart Kernel & Run All` 1회로 끝까지 실행 |
| hidden state 없음 | 특정 셀 단독 선실행 없이도 본문 재현 가능 |
| split-before-fit | 모든 scaler/encoder/selector가 train only statistics 사용 |
| shape transparency | `V03`에서 모든 핵심 tensor shape를 출력 또는 시각화 |
| optimizer fairness | seed, init, net 구조, epoch, batch size를 비교군 간 고정 |
| state visibility | Momentum/RMSProp/Adam 내부 state가 최소 1회 이상 시각화 |
| answer traceability | Part 5 서술이 특정 그래프 이름과 곡선을 직접 참조 |
| dependency capture | 환경 파일 포함, `neural_network_v2.py` 의존 명시 |
| smoke test | XOR 또는 toy objective에서 optimizer 4종의 최소 동작 확인 |

## 12. Notebook Metadata Tags

권장 태그:

```text
lecture
theory
formula
data
visualization
checkpoint
smoke-test
assert
optional
```

검증 보조 셀은 `smoke-test` 또는 `assert` tag를 붙인다.

예:

```python
assert probs.ndim == 2
assert np.allclose(probs.sum(axis=1), 1.0, atol=1e-6)
assert dW.shape == W.shape
assert db.shape == b.shape
assert dX.shape == X.shape
```

## 13. Implementation Notes

- 기본 시각화는 Matplotlib로 고정한다.
- 분포, heatmap, summary plot은 Seaborn을 사용한다.
- Plotly/Altair는 기본 의존성에 넣지 않는다.
- MNIST가 필요하면 우선 Fashion-MNIST local IDX gzip cache를 사용한다.
- 외부 URL 데이터는 기본 Run All 경로에 넣지 않는다.
- `Boston Housing`은 윤리 경고를 동반한 선택 확장으로만 둔다.
- `UCI Appliances Energy`는 후속 Week14 확장으로 둔다.

## 14. Success Criteria

- 사용자가 optimizer를 단순 이름 암기가 아니라 update rule 차이로 설명할 수 있다.
- 사용자가 layer backward와 optimizer step의 책임을 분리해 말할 수 있다.
- 사용자가 loss curve와 accuracy를 함께 읽을 수 있다.
- 사용자가 split-before-fit과 leakage 위험을 시각적으로 설명할 수 있다.
- 노트북이 clean kernel에서 끝까지 실행된다.
- `ML/code_split/dataset_inventory_for_ML_W13_PREP.json`에 근거해 실제 데이터 선택 이유를 설명할 수 있다.
