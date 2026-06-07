# Week13 Optimizer 시각화 강의 노트북 최종 설계 문서

## 설계 결론

이 노트북은 **문제 풀이용 답안 노트북**이 아니라, **Week 13 과제를 풀기 전에 이론·수식·배열·시각화·실험 해석을 한 줄로 연결하는 companion notebook**이어야 한다. 첨부된 초안은 이미 이 방향을 명시하고 있으며, 노트북의 핵심을 `V00~V05` 모듈로 나누고 “optimizer를 Layer에서 분리한 뒤 loss curve와 accuracy를 해석하는 학습 시스템”으로 설계해야 한다고 정리한다. 또한 현재 보는 노드 메모는 Week 13의 본질이 “optimizer 4종 구현 그 자체”가 아니라 **12강의 Layer/Network/backward 구조를 13강의 optimizer 책임 분리로 확장하고, `X_batch → net.forward → loss_fn.forward → loss_fn.backward → net.backward → optimizer.step(net)`를 이해하는 것**이라고 못 박고 있다. 따라서 최종 산출물은 `ML_W13_PREP_VISUAL_LECTURE.ipynb` 1개와 그것의 설계 명세인 본 `.md` 문서 1개로 고정하는 것이 가장 타당하다. fileciteturn0file0 fileciteturn0file2

이 설계의 핵심 결론은 다섯 가지다. 첫째, **학습 서사**는 `surrogate loss → chain rule/backward → parameter update → optimizer state → learning dynamics 해석` 순서로 가야 한다. 둘째, **데이터는 Iris와 XOR를 기본 축**, Fashion-MNIST를 확장 축으로 삼고, 외부 다운로드가 필요한 MNIST/Boston/UCI는 보조 또는 연기 대상으로 다뤄야 한다. 셋째, **시각화는 Matplotlib 기본, Seaborn 보조, Plotly/Altair 선택 확장**의 3단 구조가 가장 적절하다. 넷째, **재현성 품질 게이트**는 `Restart Kernel & Run All`, hidden state 방지, split-before-fit, seed 고정, optimizer 비교 공정성, 환경 고정까지 포함해야 한다. 다섯째, 노트북의 평가는 “수식 이해”와 “그래프 서술”을 분리하지 않고, **그래프를 근거로 Part 5 같은 분석형 답안을 쓰게 만드는 방향**으로 설계해야 한다. 이 결론은 Jupyter가 코드·설명·수식·시각화·결과를 함께 담는 계산 문서라는 점, nbformat이 셀과 메타데이터 중심 구조를 갖는다는 점, 그리고 첨부 초안이 모듈형 companion notebook 구조를 전제로 설계 원칙과 품질 게이트를 이미 제안하고 있다는 점을 함께 고려한 종합 판단이다. citeturn2view0turn2view1turn17academia0turn17academia1 fileciteturn0file0

## 연구 근거와 이론선

딥러닝 훈련은 “테스트 성능 자체”를 직접 최적화하는 것이 아니라, 보통은 **경험위험(empirical risk)** 혹은 그 근사인 **surrogate loss**를 미니배치 단위로 줄이는 과정으로 수행된다. *Deep Learning* 교재는 학습 목적 함수를 훈련셋 평균 손실로 서술하고, 실제로는 0-1 loss 같은 직접 최적화하기 어려운 평가량 대신 **negative log-likelihood 같은 surrogate loss**를 최적화한다고 설명한다. 또한 실제 학습은 전체셋이 아니라 **minibatch** 기반으로 parameter update가 일어나며, validation 기반 **early stopping**은 순수 수치최적화와 달리 “gradient가 거의 0이 될 때까지”가 아니라 일반화 성능이 악화되기 전에 멈추게 만든다. 이 점은 이번 노트북에서 “loss가 낮아졌다”와 “일반화가 좋아졌다”를 구분해서 가르쳐야 하는 가장 중요한 배경이다. citeturn12view0

optimizer 파트의 이론선은 **같은 gradient를 받았을 때 parameter를 어떻게 움직일 것인가**의 차이로 정리하는 것이 가장 교육적으로 정확하다. PyTorch는 `torch.optim`을 “optimization algorithms package”로 정의하고, parameter iterable을 받아 `optimizer.step()`으로 update한다고 설명한다. Keras 역시 `Optimizer` base class에서 `build`, `update_step`, `get_config`를 오버라이드하여 variable과 gradient를 갱신하는 구조를 제시한다. 즉, 현대 프레임워크 수준에서도 **layer는 gradient를 계산하고, optimizer는 그 gradient로 parameter를 갱신하는 역할**이 분리되어 있다. 이 구조는 첨부된 Week 13 메모의 “Optimizer는 X/y를 보지 않고 param과 grad만 본다”는 요지와 정확히 맞물린다. citeturn10view1turn10view2turn3view3turn3view5 fileciteturn0file2

Adam은 원논문에서 **stochastic objective의 first-order gradient 기반 optimization**을 위해 제안된 방법으로, 1차 모멘트와 2차 모멘트의 적응적 추정을 함께 사용한다. 저자들은 Adam이 구현이 단순하고, 메모리 요구가 적고, gradient의 diagonal rescaling에 비교적 불변이며, 노이즈가 크거나 sparse gradient가 있는 문제에도 적합하다고 서술한다. 이때 Momentum은 방향의 관성, RMSProp류는 좌표별 step size 적응이라는 직관을 제공하고, Adam은 이 둘을 결합한 형태로 이해할 수 있다. 다만 이것이 곧 “항상 최고의 일반화”를 뜻하지는 않으므로, 노트북에서는 **Adam을 baseline optimizer로 시작하되, 최종 판단은 validation/test와 loss curve 해석으로 넘기는 설계**가 옳다. citeturn11academia0turn10view0turn12view0

수식과 출력 설계는 프레임워크 문서와 맞춰야 한다. Keras의 `Dense`는 `output = activation(dot(input, kernel) + bias)`를 수행한다. 따라서 출력층 설계는 **문제 유형**에 의해 결정된다. 이진분류라면 sigmoid가 `1 / (1 + exp(-x))` 형태로 `[0,1]` 값을 반환하며, Keras는 binary cross-entropy에 대해 `from_logits=True` 사용을 권장한다. 다중분류라면 softmax가 벡터를 확률분포로 바꾸고 요소 합을 1로 만든다. Keras는 one-hot 라벨에는 `CategoricalCrossentropy`, 정수 라벨에는 `SparseCategoricalCrossentropy`를 쓰라고 명시하고, PyTorch는 `CrossEntropyLoss`가 **unnormalized logits**를 입력으로 받아 `LogSoftmax + NLLLoss`와 동치라고 설명한다. 회귀라면 `Dense(1)`에 선형 출력과 `MeanSquaredError` 또는 `MeanAbsoluteError`를 두는 것이 표준적이다. 이 원리를 노트북에서 “왜 이런 output/loss를 쓰는가”까지 함께 시각화해야 사용자가 암기식이 아니라 인과적으로 이해할 수 있다. citeturn28view2turn28view1turn25view0turn26view0turn26view1turn29view2turn26view2

평가 지표는 “모델이 최적화하는 대상”이 아니라 “사람이 해석하는 대상”으로 구분해서 가르쳐야 한다. Keras는 accuracy를 “predictions equal labels”의 빈도로 정의하고, F1을 `2 * (precision * recall) / (precision + recall)`의 **harmonic mean**으로 정의한다. F1의 `average` 옵션에서 `macro`는 class 불균형을 고려하지 않는 단순 평균, `weighted`는 클래스별 크기를 반영한 평균이다. 따라서 노트북에서는 **loss는 미분 가능성과 학습 안정성**, **metric은 사람의 비용 구조와 데이터 불균형 해석**이라는 두 축을 분리해서 설명해야 한다. 이 점은 첨부 G0-B 노트북에서 이미 사용자가 집중해 온 질문과도 직접 닿아 있다. citeturn30view0turn26view3 fileciteturn0file2

## 데이터 자산과 가용성

첨부된 dataset inventory는 이번 노트북의 데이터 전략을 거의 결정해 준다. 인벤토리는 목적을 “ML_W13_PREP_VISUAL_LECTURE 설계에 이식 가능한 실제/내장/외부 데이터셋 후보 식별”로 정의하고, 추천 대상을 primary/secondary/avoid_or_defer로 구분한다. 그 결과 primary는 `sklearn_iris`, `toy_logic_gates_xor`, `keras_fashion_mnist`이며, 보조 또는 연기 대상으로는 `keras_mnist_or_openml_mnist`, `boston_housing_cmu_legacy`, `uci_appliances_energy_prediction`이 잡혀 있다. 따라서 이 노트북은 **Iris + XOR를 기본**, **Fashion-MNIST를 확장**, **외부 자산은 optional**로 설계하는 것이 맞다. fileciteturn0file1

가용성 기준으로는 아래처럼 정리하는 것이 가장 실용적이다.

| 상태 | 데이터셋 | 설계 반영 |
|---|---|---|
| 바로 이식 가능 | `sklearn_iris`, `toy_logic_gates_xor`, `toy_*_week14`, `seaborn_titanic` | 본문 기본 데모로 사용 |
| 로컬에서 바로 생성·호출 가능 | `sklearn_iris`, notebook 내 embedded toy datasets | 외부 의존성 없는 smoke test와 V01~V04용 |
| 로컬 캐시 있어 사실상 즉시 사용 가능 | `keras_fashion_mnist`, `seaborn_titanic` | V03/V05 확장 실험에 사용 |
| 외부 다운로드 필요 | `keras_mnist_or_openml_mnist`, `boston_housing_cmu_legacy`, `uci_appliances_energy_prediction` | optional appendix 또는 fallback path로만 사용 |
| 참조 파일 누락 | `daisy_image_missing_local_file` | Fashion-MNIST로 대체 |

이 분류는 인벤토리의 `availability` 필드와 추천 섹션을 바탕으로 한 직접적인 설계 반영이다. fileciteturn0file1

구체적으로 Iris는 scikit-learn 공식 문서상 **150 samples, 4 features, 3 classes**의 매우 쉬운 다중분류 데이터다. 따라서 optimizer 차이가 “최종 정확도”보다 **초기 수렴 속도와 loss curve shape**에서 더 잘 드러난다. XOR는 샘플이 매우 작아 일반화 비교에는 부적합하지만, 인벤토리가 말하듯 **chain rule/backward와 nonlinearity의 직관**에는 매우 적합하다. Fashion-MNIST는 Keras 문서상 **60,000 train / 10,000 test의 28×28 grayscale, 10-class** 이미지셋으로, 인벤토리에서도 Week13 bridge와 tensor/flatten/CNN 대비용으로 추천된다. 반면 MNIST 일반셋은 개념상 적합하지만 현재 로컬 캐시가 없을 수 있고, Boston/UCI는 외부 URL 의존성과 부수적 이슈가 있어 prep notebook의 주 데이터로는 비효율적이다. citeturn8view2turn7view1turn7view2 fileciteturn0file1

이 데이터 전략은 교육적으로도 이점이 크다. **작은 데이터로 개념을 고정한 뒤, 조금 더 어려운 이미지 분류로 확대**하는 계단식 구조가 cognitive load를 줄이기 때문이다. 첨부 초안이 제안한 `V00~V05` 모듈과도 정합적이며, 실제 Week 13 메모가 말하는 “Iris/MNIST 비교, optimizer loss curve, learning-rate sensitivity” 과제를 과도한 외부 의존성 없이 재구성할 수 있게 해 준다. 이것이 이번 설계에서 외부 다운로드 필요 자산을 보조 경로로 내린 이유다. fileciteturn0file0 fileciteturn0file2

## 노트북 아키텍처와 기능 명세

본 노트북의 정보 구조는 **전문 설계 문서의 인덱스**를 따르되, Jupyter의 셀 구조에 맞게 다시 배치해야 한다. 즉 문서는 `목적`, `범위`, `선행지식`, `의존성`, `가정`, `비목표`, `대안`, `품질 게이트`, `실행 순서`, `실험 산출물`을 가져야 하고, 이것을 Jupyter에서는 **상위 markdown heading + 짧은 요약 셀 + 인접 코드 셀**로 반복 배치해야 한다. Jupyter는 markdown heading이 문서 구조와 export 힌트를 제공하고, code cell은 rich output과 matplotlib figure, table, math rendering을 함께 실을 수 있다. nbformat은 top-level에 `metadata`, `nbformat`, `cells`를 가지는 JSON schema를 사용하므로, 이 노트북은 구조적으로도 “설명 셀과 실행 셀의 안정적 번갈아 배치”가 유리하다. 또한 최신 재현성 연구는 계산 노트북이 out-of-order execution과 hidden state 때문에 재실행 실패를 일으키기 쉽다고 지적하므로, 본 설계는 **singular cell, clean run, hidden state 금지**를 기본 규약으로 둔다. citeturn2view0turn2view1turn17academia0turn17academia1turn17academia2turn17academia3

최상위 기능 모듈은 첨부 초안을 존중해 `V00~V05`로 유지하는 것이 가장 좋다. 이는 사용자가 이미 이 구조에 익숙해져 있고, 실제 설계 초안도 같은 분해를 전제하고 있기 때문이다. 그 역할은 아래처럼 고정한다. fileciteturn0file0

| 모듈 | 핵심 질문 | 필수 산출물 | 기본 데이터 |
|---|---|---|---|
| `V00` 전체 지도 | Week13은 무엇을 묻는가 | dependency map, 역할 분리 도식 | 없음 |
| `V01` 데이터·출력·손실·지표 | 왜 이 문제에 이 output/loss/metric인가 | leakage 데모, regression/classification metric 시각화 | Titanic/toy/Iris |
| `V02` GD·chain rule | gradient와 learning rate는 무엇을 바꾸는가 | 1D/2D loss surface, path plot | XOR/toy |
| `V03` Dense backward·SoftmaxCE | `dW`, `db`, `dX`, `p-y`는 배열 수준에서 무엇인가 | shape/heatmap/table | XOR/Fashion-MNIST subset |
| `V04` optimizer 비교 | SGD, Momentum, RMSProp, Adam은 무엇이 다른가 | contour trajectory, state time-series | toy objective, XOR |
| `V05` Week13 bridge | 과제의 Iris/MNIST/Fashion-MNIST 비교를 어떻게 읽는가 | loss curve, accuracy, answer scaffold | Iris, Fashion-MNIST subset |

여기서 핵심은 **모든 모듈이 독립적이지 않고 직렬적으로 의존**한다는 점이다. `V01`이 output/loss/metric을 고정하면 `V02`에서 loss surface를 정의할 수 있고, `V02`가 chain rule과 gradient step을 설명해야 `V03`에서 backward tensor를 읽을 수 있으며, `V03`의 gradient 이해가 있어야 `V04`의 optimizer state 해석이 가능해진다. 마지막 `V05`는 앞선 모든 개념을 Week13 과제 형태로 재배열하는 bridge다. 이 직렬 구조는 첨부 초안의 학습 경로와 현재 Week13 노드 설명을 그대로 구현한 것이다. fileciteturn0file0 fileciteturn0file2

## 블록별 체크포인트와 시각화 설계

### 전체 지도 블록

`V00`은 **“이 노트북이 무엇이고 무엇이 아닌가”**를 먼저 못 박아야 한다. 여기서는 Week13이 optimizer 비교 실험이며, 선행 노드가 gradient/chain rule, 2-2-1 backprop, Layer/Network/SoftmaxCE였고, 후속 노드가 Keras `compile(optimizer=...)`, validation/loss curve, regularization, CNN 설계라는 점을 한 화면에 고정해야 한다. 이 서사는 현재 보는 노드 메모에 직접 주어져 있으며, 사용자가 길을 잃지 않게 만드는 가장 좋은 방법은 **flowchart + 역할 분리 다이어그램** 하나를 첫 화면에 두는 것이다. fileciteturn0file2

시각화는 단순 박스 다이어그램이면 충분하다. Matplotlib는 Jupyter에서 figure와 axes를 명시적으로 다루는 OO 스타일을 권장하며, Jupyter 노트북에서는 `plt.show()` 없이도 figure가 바로 표시되는 경우가 많다. 따라서 이 블록에서는 복잡한 시각화 라이브러리보다 Matplotlib + 간단한 annotation이 더 적합하다. citeturn4view2

**바로 넣을 markdown 셀 초안**

```md
# Week13 Optimizer Visual Lecture

## 이 노트북의 역할
- 이것은 제출용 숙제 답안이 아니라, Week13 과제를 풀기 전 개념·수식·shape·그래프를 연결하는 companion notebook이다.
- 목표는 optimizer 구현법 자체보다, 같은 gradient를 서로 다른 optimizer가 어떻게 다르게 해석하고 loss curve를 어떻게 바꾸는지 이해하는 것이다.

## 의존성 지도
G0-B → Gradient / Chain Rule → Dense.backward / SoftmaxCE → Optimizer State → Week13 해석형 답안
```

**바로 넣을 시각화 코드 셀 초안**

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 3))
ax.axis("off")

items = [
    ("G0-B\noutput/loss/metric", 0.08),
    ("Gate1\nGD / chain rule", 0.28),
    ("Gate2\nDense.backward\nSoftmaxCE", 0.48),
    ("Gate3\nOptimizer state", 0.68),
    ("Week13\nloss curve 해석", 0.88),
]

for text, x in items:
    ax.text(x, 0.5, text, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.5"))

for i in range(len(items) - 1):
    x1 = items[i][1] + 0.07
    x2 = items[i + 1][1] - 0.07
    ax.annotate("", xy=(x2, 0.5), xytext=(x1, 0.5),
                arrowprops=dict(arrowstyle="->", lw=2))

ax.set_title("Week13 Optimizer 실험의 의존성 지도")
plt.show()
```

### 데이터·손실·지표 블록

`V01`은 optimizer 이전에 **무엇을 최소화할지**를 고정하는 블록이다. 여기서 꼭 보여줘야 하는 것은 leakage, regression/classification/ordinal 설계, loss와 metric의 분리다. scikit-learn은 데이터 누수 방지를 위해 **반드시 split을 먼저 하고**, `fit`/`fit_transform`은 train subset에만 적용하며, test에는 `transform`만 적용하라고 명시한다. `Pipeline`은 이런 실수를 줄이는 기본 수단이다. 따라서 이 블록은 “정답 개념 설명”보다 **잘못된 전처리로 score가 부풀려지는 장면**을 직접 시각화하는 쪽이 훨씬 교육적이다. citeturn3view0turn3view2

손실과 지표는 문제 유형에 따라 아래처럼 설명한다. 회귀에서는 `MSE = mean(square(y_true - y_pred))`, `MAE = mean(abs(y_true - y_pred))`다. MSE는 오차를 제곱하므로 큰 오차를 더 크게 벌주고, MAE는 단위 해석이 상대적으로 쉽다. 분류에서는 sigmoid/softmax와 cross-entropy를 쓴다. Keras와 PyTorch 문서는 모두 **logits와 probabilities를 구분**하고, one-hot 대 정수 라벨에 따라 categorical vs sparse categorical cross-entropy를 구분한다. accuracy는 단순 빈도, F1은 precision과 recall의 조화평균이다. 이론 설명은 수식으로, 직관은 **히스토그램, 오차-제곱 곡선, confusion heatmap**으로 가르치는 것이 가장 좋다. citeturn26view2turn25view0turn26view0turn26view1turn29view2turn30view0turn26view3

이 블록의 주 시각화 도구는 Seaborn이 적합하다. Seaborn은 dataframe과 whole-dataset semantics에 맞춰 statistical graphics를 쉽게 만들고, distribution, categorical view, error bar 등을 간단히 표현한다. 따라서 Titanic이나 small tabular toy data에서 histogram, boxplot, countplot, heatmap, pairplot 계열은 Seaborn이 가장 교육 효율이 높다. 다만 세세한 figure anatomy와 축 통제는 Matplotlib가 더 직관적이므로 둘을 함께 써야 한다. citeturn6view0turn6view1turn4view2

**바로 넣을 markdown 셀 초안**

```md
## 왜 split-before-fit 인가

데이터를 train/test로 나누기 전에 scaler를 fit하면,
test 데이터의 평균과 분산이 이미 전처리에 스며든다.
이때 모델은 실제 배포 시점에 알 수 없는 정보를 미리 본 셈이므로
성능이 낙관적으로 부풀 수 있다.

이번 블록의 질문은 하나다.
"이 문제에서 무엇을 예측하고, 무엇을 최소화하고, 무엇으로 해석할 것인가?"
```

**바로 넣을 코드 셀 초안**

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame.copy()
df["target_name"] = df["target"].map(dict(enumerate(iris.target_names)))

X = df[iris.feature_names].values
y = df["target"].values

# 잘못된 전처리: 전체 데이터로 fit
X_bad = StandardScaler().fit_transform(X)
Xb_train, Xb_test, yb_train, yb_test = train_test_split(
    X_bad, y, test_size=0.3, random_state=42, stratify=y
)

# 올바른 전처리: train만 fit
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_ok = scaler.fit_transform(X_train)
X_test_ok = scaler.transform(X_test)

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(X_bad[:, 0], bins=20, alpha=0.6, label="bad: fit before split")
ax.hist(X_train_ok[:, 0], bins=20, alpha=0.6, label="good: fit on train")
ax.set_title("같아 보여도 통계 기준이 다르면 leakage 가능성이 생긴다")
ax.legend()
plt.show()
```

### gradient·backward·optimizer 블록

`V02`, `V03`, `V04`는 사실상 노트북의 본체다. `V02`에서는 learning rate가 너무 작으면 느리고, 너무 크면 overshoot/진동/발산이 난다는 점을 **1D 혹은 2D 손실 곡면**에서 보여줘야 한다. *Deep Learning* 교재는 학습이 full-batch 순수 최적화가 아니라 minibatch 기반이며, surrogate loss 위에서 작동한다고 설명한다. 여기에 XOR 같은 toy objective를 얹으면 사용자는 “gradient가 로컬 기울기이고, lr는 step size”라는 가장 중요한 감각을 눈으로 얻을 수 있다. citeturn12view0

`V03`에서는 `Dense.backward`의 배열 의미를 반드시 드러내야 한다. Keras의 Dense는 `activation(dot(input, kernel)+bias)`를 수행하므로, backward에서는 `dW`, `db`, `dX`가 각각 **가중치 변화량, bias 변화량, 이전 층으로 되돌아가는 error signal**이 된다. 마지막 출력층이 softmax CE라면, PyTorch 문서가 보여주듯 CE는 logits에 대해 `LogSoftmax + NLLLoss`와 동치이고, 정답 class 확률을 높일수록 loss가 줄어든다. 따라서 이 블록은 **shape table**, **작은 batch의 logit/probability heatmap**, **`p - y` 시각화**가 핵심이다. 여기서는 표와 heatmap이 중심이므로 Seaborn heatmap이 효과적이고, 필요하면 Altair로 interactive table-like view를 추가할 수 있다. Altair는 declarative visualization을 강조하므로, 변수 역할이 분명한 shape/gradient 표시에 잘 맞는다. citeturn28view2turn29view2turn29view1turn5view1turn6view0

`V04`에 들어오면 드디어 optimizer state를 보여줄 수 있다. Keras optimizer 예시는 `momentum` 변수를 build에서 만들고 `update_step`에서 gradient와 learning rate로 update하는 형태를 제시한다. Adam 논문은 first/second moment 추정을 핵심으로 제시한다. 따라서 이 블록에서는 **같은 loss surface 위에서 optimizer trajectory를 겹쳐 그리기**, **velocity / second-moment / bias-corrected state를 time series로 그리기**, **gradient norm과 effective step size를 같은 epoch 축에서 비교하기**가 가장 배움이 크다. 정적 그림은 Matplotlib, 분기별 토글이나 slider는 Plotly가 적합하다. Plotly는 interactive, publication-quality graph와 Jupyter widget integration을 공식적으로 지원한다. citeturn3view3turn11academia0turn6view2turn6view3turn4view2

**바로 넣을 markdown 셀 초안**

```md
## Dense.backward와 Optimizer.step은 왜 분리되는가

- backward는 "손실이 각 파라미터에 얼마나 민감한가"를 계산한다.
- optimizer는 "그 민감도를 보고 실제로 얼마나 움직일 것인가"를 결정한다.
- 따라서 backward의 출력이 같아도 optimizer가 다르면 학습 경로가 달라진다.
```

**바로 넣을 코드 셀 초안**

```python
import numpy as np
import matplotlib.pyplot as plt

def f(w):
    return 0.1 * w**4 - w**2 + 0.2 * w

def grad_f(w):
    return 0.4 * w**3 - 2 * w + 0.2

def run_sgd(w0, lr, steps=25):
    ws = [w0]
    for _ in range(steps):
        w0 = w0 - lr * grad_f(w0)
        ws.append(w0)
    return np.array(ws)

grid = np.linspace(-3, 3, 400)
vals = f(grid)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(grid, vals, label="loss surface")

for lr in [0.01, 0.1, 0.4]:
    ws = run_sgd(2.5, lr=lr, steps=15)
    ax.plot(ws, f(ws), marker="o", label=f"SGD lr={lr}")

ax.set_title("learning rate에 따라 같은 gradient도 다른 경로를 만든다")
ax.set_xlabel("w")
ax.set_ylabel("loss")
ax.legend()
plt.show()
```

**바로 넣을 shape 시각화 코드 셀 초안**

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

B, Din, Dout = 4, 3, 2
X = np.random.randn(B, Din)
W = np.random.randn(Din, Dout)
b = np.random.randn(Dout)

logits = X @ W + b
exp_logits = np.exp(logits - logits.max(axis=1, keepdims=True))
P = exp_logits / exp_logits.sum(axis=1, keepdims=True)
Y = np.array([[1, 0], [0, 1], [1, 0], [0, 1]])

dlogits = (P - Y) / B
dW = X.T @ dlogits
db = dlogits.sum(axis=0)
dX = dlogits @ W.T

shape_df = pd.DataFrame({
    "name": ["X", "W", "b", "logits", "P", "Y", "dlogits", "dW", "db", "dX"],
    "shape": [X.shape, W.shape, b.shape, logits.shape, P.shape, Y.shape,
              dlogits.shape, dW.shape, db.shape, dX.shape]
})
print(shape_df)

fig, ax = plt.subplots(figsize=(6, 3))
sns.heatmap(P, annot=True, fmt=".2f", ax=ax)
ax.set_title("softmax probability heatmap")
plt.show()
```

## Week13 브리지와 실제 셀 템플릿

`V05`는 최종적으로 **과제와 같은 형식의 질문**으로 되돌아와야 한다. 첨부 노트는 Week13 homework의 Part 1~5가 optimizer 구현, Iris/MNIST 비교, learning-rate sensitivity, 그래프 기반 분석으로 구성된다고 요약한다. 따라서 `V05`의 역할은 세 가지다. 첫째, 실험 runner를 제공한다. 둘째, 같은 초기화·같은 데이터 분할·같은 epoch·같은 batch size를 고정하여 **optimizer 비교의 공정성**을 보장한다. 셋째, 그래프 아래에 바로 **서술 템플릿**을 둬서 사용자가 Part 5형 분석을 쓰게 만든다. 이 설계는 첨부 메모의 “graph interpretation이 Gate 통과 기준”이라는 판단과 직접 이어진다. fileciteturn0file2

Iris는 scikit-learn이 제공하는 쉬운 다중분류 데이터이고, Fashion-MNIST는 로컬 캐시가 있다면 더 어려운 이미지 분류 브리지로 쓰기 좋다. 다만 leakage 방지를 위해 split 뒤에 scaler를 train에만 fit해야 하며, optimizer 비교에서는 seed와 init을 반드시 고정해야 한다. 이는 scikit-learn 누수 가이드와 첨부 초안의 품질 게이트가 모두 요구하는 조건이다. citeturn8view2turn7view1turn7view2turn3view0turn3view2 fileciteturn0file0

**바로 넣을 markdown 셀 초안**

```md
## Week13 bridge

이제부터는 설명용 그래프가 아니라 과제형 실험으로 넘어간다.

실험 원칙
- 데이터 분할은 먼저 한다.
- 전처리 통계는 train에만 맞춘다.
- 같은 seed, 같은 초기화, 같은 네트워크, 같은 epoch, 같은 batch size를 유지한다.
- optimizer만 바꿔서 loss curve와 accuracy를 비교한다.

아래 그래프를 보고 반드시 문장으로 답하라.
1. 어떤 optimizer가 더 빨리 수렴했는가?
2. 어떤 optimizer가 더 안정적이었는가?
3. learning rate를 바꾸면 누가 더 민감하게 무너졌는가?
4. 새 문제를 만나면 어떤 optimizer를 baseline으로 쓸 것인가? 왜 그렇게 해석하는가?
```

**바로 넣을 코드 셀 초안**

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 실제 구현체는 사용자의 neural_network_v2.py / optimizer 구현과 연결
# 여기서는 interface 설계만 고정한다.

def prepare_iris(seed=42):
    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=seed, stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test

def run_experiment(build_net_fn, optimizer_dict, train_fn, seed=0):
    results = {}
    X_train, X_test, y_train, y_test = prepare_iris(seed=seed)

    for name, optimizer in optimizer_dict.items():
        np.random.seed(seed)
        net = build_net_fn()
        history = train_fn(net, optimizer, X_train, y_train, X_test, y_test)
        results[name] = history
    return results

def plot_histories(results, metric_key="test_acc"):
    fig, ax = plt.subplots(figsize=(8, 4))
    for name, hist in results.items():
        ax.plot(hist[metric_key], label=name)
    ax.set_title(metric_key)
    ax.set_xlabel("epoch")
    ax.legend()
    plt.show()
```

이 블록 이후에는 바로 **답안 scaffold 셀**을 붙이는 것이 좋다. retrieval practice는 장기 기억 형성에 유리하고, worked example와 self-explanation은 초심자의 schema 형성에 효과적이라는 교육심리 연구가 널리 알려져 있다. 이번 노트북에서는 이를 “그래프 바로 아래에 빈 문장 프레임을 두는 방식”으로 구현하면 충분하다. 이 부분의 실무적 적용 방식은 첨부 초안이 제안한 answer traceability와도 맞아떨어진다. citeturn22search1turn22search0 fileciteturn0file0

## 품질 게이트와 열린 쟁점

최종 품질 게이트는 다음처럼 고정하는 것이 좋다. 이는 첨부 초안의 quality gate 제안과 Jupyter 재현성 문헌을 합친 것이다. clean run은 `Restart Kernel & Run All` 한 번으로 끝까지 실행되어야 한다. hidden state가 없어야 하고, 셀은 단독으로 거대한 부작용을 만들지 않게 쪼개야 한다. split-before-fit은 모든 전처리 단계에서 지켜져야 한다. optimizer fairness를 위해 seed, init, net structure, epoch, batch size는 고정해야 한다. Momentum/RMSProp/Adam은 내부 state를 최소 한 번은 시각화해야 한다. 최종 서술형 답안은 특정 그래프와 curve를 직접 참조해야 한다. 마지막으로 `requirements.txt` 또는 `environment.yml`과 `neural_network_v2.py` 의존성을 명시해야 한다. 이 게이트는 notebook hidden state 문제, Jupyter의 execution order 문제, 그리고 Week13 과제의 해석 중심 성격을 동시에 반영한다. citeturn17academia0turn17academia1turn17academia2turn17academia3 fileciteturn0file0

개발자용 기능 명세 형태로 적으면 아래와 같다.

| 항목 | 명세 |
|---|---|
| 제품명 | `ML_W13_PREP_VISUAL_LECTURE.ipynb` |
| 1차 사용자 | Week13 과제를 풀기 직전의 학습자 |
| 주요 목표 | optimizer 책임 분리, backward tensor 이해, loss curve 해석 |
| 비목표 | 제출용 정답 자동 생성, 범용 DL 프레임워크 구현 |
| 필수 입력 | Python 3, NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, 선택적으로 Keras/Plotly/Altair |
| 필수 출력 | 수식 설명, shape 표, loss/metric 시각화, optimizer trajectory, answer scaffold |
| 성공 기준 | clean run, hidden state 없음, leakage 없음, optimizer 공정 비교 가능 |
| 실패 기준 | split 전에 fit, 외부 다운로드 없이는 본문이 멈춤, 그래프와 서술이 분리됨 |

열린 쟁점도 짧게 남겨야 한다. 첫째, 실제 `neural_network_v2.py` 구현 파일이 현재 대화에 첨부되지 않았으므로, `params_and_grads`, `optimizer.step(net)` 같은 interface는 첨부 노트 요약에 기반한 설계 수준으로만 확정할 수 있다. 둘째, Week13 원본 숙제 노트북 전체가 현재 직접 검토 가능한 형태로 붙어 있지 않아, 셀 번호 수준의 exact patch는 본 문서에서 다루지 않았다. 셋째, pedagogical research 일부는 공개 초록/요약 접근성 한계가 있어, 이번 문서에서는 **직접 실행 가능한 notebook design과 고신뢰 공식 문서**를 중심 근거로 삼았다. 이 한계를 감안해도, 본 설계는 이미 첨부된 초안과 dataset inventory, Week13 노드 메모를 일관되게 통합한 최종 사양으로 사용하기에 충분하다. fileciteturn0file0 fileciteturn0file1 fileciteturn0file2