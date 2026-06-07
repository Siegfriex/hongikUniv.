# ML_W13_PREP_VISUAL_LECTURE

이 노트북은 Week13 optimizer 과제를 풀기 직전의 companion notebook이다. 제출용 답안 노트북이 아니라, `X/y -> forward -> loss -> backward -> optimizer.step(net)` 흐름을 스스로 설명하기 위한 시각화 강의 노트북이다.

반복 기준:

```text
X_batch
→ net.forward(X_batch)
→ loss_fn.forward(logits, y_batch)
→ loss_fn.backward()
→ net.backward(dloss)
→ optimizer.step(net)
```

```text
Optimizer는 X/y를 보지 않는다.
Optimizer는 layer가 들고 있는 param과 grad만 읽고 parameter를 update한다.
```

---

### 전체 디벨롭 실행 계획

| 섹션 | 역할 | 실행 산출 |
|---|---|---|
| V00 | 전체 개념 지도와 책임 분리 흐름을 고정 | Mermaid course map, 책임 분리 flow, 단계별 입력/출력 표 |
| V01 | optimizer 비교 전에 데이터/출력/손실/지표 기준을 압축 | Iris/XOR/Image DatasetCard, scaling/leakage contrast |
| Appendix | V01 본문에서 뺀 데이터 인벤토리 보조 예시 | Titanic/missing/categorical/datetime mini EDA |
| V02 | GD와 XOR 비선형성 직관 | 1D/2D GD path, sklearn MLPClassifier visualization only |
| V03 | scratch Dense convention과 SoftmaxCE gradient shape 검증 | shape table, heatmap, assert cell, role table |
| V03.5 | Dense width와 ReLU gate 심화 | parameter count, ReLU derivative, active/dead unit ratio |
| V04 | optimizer state 직관과 `optimizer.step(net)` 책임 확인 | V04-A 2D vector simulation, V04-B dummy net update audit |
| V04.5 | bootstrap 안정성 진단 | width x optimizer metric distribution, ReLU gate distribution |
| V05 | Iris optimizer comparison 본체 | train/val curves, final test metrics, final test confusion matrix |
| V05.5 | gradient flow audit | layer별 grad/update/active/dead ratio |
| V05.6 | ablation lab | scaling/ReLU/width/init/lr failure 비교 |
| V06 | 이미지 tensor와 CNN bridge를 Week15로 연결 | sample grid, label distribution, flatten diagram, pixel histogram, CNN pipeline |
| V07 | proper MLP representation bridge | Dense+ReLU block 반복, layer-wise PCA before/after |
| V08 | failure gallery | symptom -> evidence -> cause -> action -> answer sentence |
| Final Audit | 시각화를 판단판과 답안 문장으로 압축 | trace board, learning dynamics board, architecture bridge board |
| Final | 시험 답안 프레임으로 압축 | rubric + 검증 섹션 매핑표 |

---

```python
# 공통 import 셀.
# 이 노트북은 외부 다운로드 없이 실행되는 것을 목표로 하므로,
# 기본 실행 의존성은 표준 라이브러리 + NumPy/Pandas/Matplotlib/scikit-learn으로 제한한다.
import json
import gzip
import struct
from pathlib import Path

# 배열 계산, 표 처리, 시각화를 담당하는 기본 스택이다.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Iris/digits는 로컬 내장 데이터셋이므로 네트워크가 필요 없다.
# train_test_split은 train/validation/test 분리를 엄격히 만들기 위해 사용한다.
from sklearn.datasets import load_iris, load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report, silhouette_score
from sklearn.decomposition import PCA

# V02의 XOR decision region은 비선형 경계 시각화 전용이다.
# Week13 optimizer 비교 본체는 V04~V05 scratch Network에서 수행한다.
from sklearn.neural_network import MLPClassifier

# 모든 난수 실험의 기준 seed.
# optimizer 비교에서 seed가 바뀌면 update rule 차이가 아니라 초기값 차이를 비교하게 된다.
SEED = 42
np.random.seed(SEED)

# 모든 그래프의 기본 크기를 고정해 notebook layout을 안정화한다.
plt.rcParams["figure.figsize"] = (8, 5)

# seaborn은 있으면 보조 시각화에 쓸 수 있지만, 없어도 notebook이 실패하면 안 된다.
try:
    import seaborn as sns
    HAS_SEABORN = True
except Exception:
    HAS_SEABORN = False
```

---

```python
# Core math helpers.
# 목적: V02/V04/V05가 서로의 실행 순서에 덜 의존하도록 공통 수학 함수를 앞쪽에 둔다.
def softmax(logits):
    # row-wise softmax with numerical stability.
    z = logits - logits.max(axis=1, keepdims=True)
    exp_z = np.exp(z)
    return exp_z / exp_z.sum(axis=1, keepdims=True)

def one_hot(y, num_classes):
    # SoftmaxCE 설명과 assert에 쓰는 간단한 one-hot helper.
    return np.eye(num_classes)[y]

def quad_loss(w):
    # V02와 V04가 공유하는 2D quadratic surface.
    # w[0] 방향은 완만하고, w[1] 방향은 가파르다.
    return 0.1 * w[0]**2 + 2.0 * w[1]**2

def quad_grad(w):
    # quad_loss의 analytic gradient.
    return np.array([0.2 * w[0], 4.0 * w[1]])

def make_quad_grid(xlim=(-6, 6), ylim=(-3, 3), n=160):
    # V02/V04 contour plot용 grid를 매번 독립적으로 만든다.
    # 이렇게 하면 V04만 다시 실행해도 V02의 전역 변수에 의존하지 않는다.
    x1 = np.linspace(*xlim, n)
    x2 = np.linspace(*ylim, n)
    W1, W2 = np.meshgrid(x1, x2)
    Z = 0.1 * W1**2 + 2.0 * W2**2
    return W1, W2, Z

def scale_image_pixels(images, dataset_name):
    # Fashion-MNIST는 uint8 0~255, sklearn_digits fallback은 0~16 범위다.
    # dataset별 scaling 기준을 분리하지 않으면 digits fallback이 지나치게 작아진다.
    images = images.astype(float)
    if "digits" in dataset_name:
        return images / 16.0, "pixel scaling: /16.0 for sklearn_digits fallback"
    if images.max() > 1:
        return images / 255.0, "pixel scaling: /255.0"
    return images, "pixel scaling: already normalized"
```

---

```python
# Advanced visualization extension loader.
# 목적: 고급 시각화 셀을 notebook 본문에 선택 삽입하되,
# 기존 V00~V06의 핵심 helper와 optimizer loop를 중복 정의하지 않기 위함이다.
# 이 모듈은 3D surface, 평면도/정면도/측면도, PCA, 미분 tangent,
# Dense backward heatmap, optimizer state dashboard, image PCA bridge를 제공한다.
import importlib.util

ADV_VIS_REQUIRED = [
    "plot_iris_pca_multiview",
    "plot_mixed_association_dashboard",
    "chi_square_pair_test",
    "plot_categorical_100pct_stacked",
    "plot_continuous_by_category_gallery",
    "plot_covariance_to_correlation_demo",
    "plot_simple_regression_residual_diagnostics",
    "plot_pc_regression_residual_diagnostics",
    "plot_quadratic_multiview",
    "plot_optimizer_multiview",
    "plot_image_pca_and_patch_bridge",
]


def find_advanced_visualization_pack():
    """Find visualization_cells.py from repo root or notebook folder.

    Jupyter의 현재 작업 디렉터리는 노트북을 어디서 열었는지에 따라 달라질 수 있다.
    따라서 repo root 기준 경로와 `ML/code_split/final` 폴더 기준 경로를 모두 검색한다.
    """
    cwd = Path.cwd().resolve()
    candidates = []
    for base in [cwd, *cwd.parents]:
        candidates.extend([
            base / "visualization_cells.py",
            base / "ML/code_split/final/visualization_cells.py",
        ])

    seen = set()
    unique_candidates = []
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in seen:
            unique_candidates.append(resolved)
            seen.add(resolved)

    for candidate in unique_candidates:
        if candidate.exists():
            return candidate, unique_candidates
    return None, unique_candidates


ADV_VIS_PATH, ADV_VIS_SEARCHED = find_advanced_visualization_pack()
if ADV_VIS_PATH is None:
    searched = "\n".join(f"- {path}" for path in ADV_VIS_SEARCHED[:12])
    raise FileNotFoundError(
        "Advanced visualization pack is required but was not found. "
        "Expected visualization_cells.py in the notebook folder or ML/code_split/final.\n"
        f"Searched paths:\n{searched}"
    )

spec = importlib.util.spec_from_file_location("ml_w13_advanced_visualization_cells", ADV_VIS_PATH)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot import advanced visualization pack from {ADV_VIS_PATH}")
adv_vis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adv_vis)
missing_adv_vis = [name for name in ADV_VIS_REQUIRED if not hasattr(adv_vis, name)]
if missing_adv_vis:
    raise AttributeError(f"Advanced visualization pack is missing required helpers: {missing_adv_vis}")
print("Advanced visualization pack loaded:", ADV_VIS_PATH)
```

---

```python
# 강의 코드 파일이 존재하는지 확인한다.
# 실제 실행 기본값은 아래 scratch fallback class다.
# 이유: 강의 파일은 notebook마다 class 이름이나 전역 상태가 달라질 수 있기 때문이다.
COURSE_SOURCE_CANDIDATES = [
    Path("ML/code_split/0526_neural_network_v2.py"),
    Path("ML/code_split/0519_neural_network.py"),
]

def try_load_course_source(path_candidates=COURSE_SOURCE_CANDIDATES):
    # import를 강제하지 않고, 후보 파일 경로만 확인한다.
    # 이 셀의 목적은 “강의 코드가 있으면 참고 가능하다”는 provenance를 남기는 것이다.
    for p in path_candidates:
        if p.exists():
            return p
    return None

course_source_path = try_load_course_source()
print("Course neural-network source candidate:", course_source_path)
print("Fallback classes in this notebook keep Dense W shape = (Dout, Din).")
```

---

```python
# dataset inventory는 있으면 dataset registry 표에 사용하고,
# 없으면 notebook 내부 fallback registry로 계속 실행한다.
INVENTORY_PATH_CANDIDATES = [
    Path("ML/code_split/dataset_inventory_for_ML_W13_PREP.json"),
    Path("dataset_inventory_for_ML_W13_PREP.json"),
    Path("/mnt/data/dataset_inventory_for_ML_W13_PREP.json"),
    Path("ML/code_split/final/dataset_inventory_for_ML_W13_PREP.json"),
]

def load_inventory(path_candidates=INVENTORY_PATH_CANDIDATES):
    # 후보 경로를 순서대로 확인한다.
    # 첫 번째로 발견되는 JSON만 registry source of truth로 사용한다.
    for p in path_candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f), p
    # inventory가 없어도 notebook 실행은 실패하지 않는다.
    return None, None

def classify_dataset_role(dataset_id):
    # Week13 본문에서 반드시 쓰는 데이터셋.
    primary = {"sklearn_iris", "toy_logic_gates_xor", "keras_fashion_mnist"}
    # V01 또는 Appendix에서 전처리/EDA 예시로 쓰는 데이터셋.
    secondary = {
        "seaborn_titanic",
        "toy_missing_values_week14",
        "toy_scaling_week14",
        "toy_categorical_encoding_week14",
        "toy_datetime_features_week14",
    }
    if dataset_id in primary:
        return "primary"
    if dataset_id in secondary:
        return "secondary"
    # Boston/UCI/uncached MNIST 등은 기본 실행 경로에서 제외한다.
    return "avoid_or_defer"

def inventory_table(inventory):
    # inventory가 없을 때도 핵심 DatasetCard를 만들 수 있도록 최소 registry를 제공한다.
    if inventory is None:
        return pd.DataFrame(
            [
                ["primary", "sklearn_iris", "sklearn_builtin_available", "(150, 4)", "multiclass", "Week13 optimizer comparison"],
                ["primary", "toy_logic_gates_xor", "embedded", "(4, 2)", "binary nonlinear toy", "XOR/MLP bridge"],
                ["primary", "keras_fashion_mnist", "local_or_digits_fallback", "(N, H, W)", "image multiclass", "Flatten/CNN bridge"],
            ],
            columns=["role", "dataset_id", "availability", "shape", "task_type", "best_fit"],
        )

    # 실제 inventory가 있으면 dataset_id별 metadata를 표준 컬럼으로 평탄화한다.
    rows = []
    for ds in inventory.get("datasets", []):
        dataset_id = ds.get("dataset_id", "")
        prof = ds.get("dataset_profile") or {}
        rows.append(
            {
                "role": classify_dataset_role(dataset_id),
                "dataset_id": dataset_id,
                "availability": ds.get("availability", ""),
                "shape": ds.get("shape") or prof.get("shape") or prof.get("shapes") or "",
                "task_type": ds.get("task_type", ""),
                "best_fit": ds.get("best_fit") or ds.get("recommended_use") or "",
            }
        )

    # primary -> secondary -> avoid_or_defer 순서로 정렬해 강의 우선순위를 드러낸다.
    order = {"primary": 0, "secondary": 1, "avoid_or_defer": 2}
    return pd.DataFrame(rows).sort_values(
        ["role", "dataset_id"],
        key=lambda s: s.map(order).fillna(s) if s.name == "role" else s,
    )

inventory, inventory_path = load_inventory()
print("Inventory path:", inventory_path)
dataset_registry = inventory_table(inventory)
display(dataset_registry)
```

---

```python
def dataset_from_inventory_profile(inventory, dataset_id, prefer="head_10"):
    # inventory JSON 안에 head_10 같은 작은 profile row가 있으면 DataFrame으로 변환한다.
    # 이 경로는 외부 다운로드 없이 Titanic 같은 dataset preview를 재현하기 위한 것이다.
    if inventory is None:
        return None
    for ds in inventory.get("datasets", []):
        if ds.get("dataset_id") == dataset_id:
            prof = ds.get("dataset_profile") or {}
            rows = prof.get(prefer)
            if rows:
                return pd.DataFrame(rows)
    return None

def fallback_titanic():
    # seaborn/titanic 다운로드를 하지 않기 위한 embedded mini table.
    # 결측치, categorical dtype, binary target을 보여주기에 충분한 크기만 둔다.
    return pd.DataFrame(
        {
            "survived": [0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
            "pclass": [3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
            "sex": ["male", "female", "female", "male", "female", "male", "male", "female", "male", "female"],
            "age": [22, 38, 26, np.nan, 35, 54, 2, 27, np.nan, 14],
            "fare": [7.25, 71.28, 7.93, 8.05, 53.1, 51.86, 21.08, 11.13, 13.0, 30.07],
            "embarked": ["S", "C", "S", "S", np.nan, "S", "S", "Q", "S", "C"],
        }
    )

def read_idx_images(path, max_items=200):
    # Fashion-MNIST IDX gzip image file reader.
    # header: magic, item count, row count, column count.
    # max_items로 잘라 notebook 실행 시간을 제한한다.
    with gzip.open(path, "rb") as f:
        magic, n, rows, cols = struct.unpack(">IIII", f.read(16))
        count = min(n, max_items)
        data = np.frombuffer(f.read(count * rows * cols), dtype=np.uint8)
    return data.reshape(count, rows, cols)

def read_idx_labels(path, max_items=200):
    # Fashion-MNIST IDX gzip label file reader.
    # header: magic, item count. 뒤쪽 byte가 label id다.
    with gzip.open(path, "rb") as f:
        magic, n = struct.unpack(">II", f.read(8))
        count = min(n, max_items)
        data = np.frombuffer(f.read(count), dtype=np.uint8)
    return data

def load_fashion_mnist_or_digits(max_items=200):
    # 기본 경로에서는 네트워크 다운로드를 절대 요구하지 않는다.
    # 로컬 IDX gzip cache가 있으면 Fashion-MNIST를 쓰고, 없으면 sklearn_digits로 대체한다.
    search_dirs = [
        Path.home() / ".keras" / "datasets",
        Path.home() / ".keras" / "datasets" / "fashion-mnist",
        Path("ML/code_split"),
        Path("/mnt/data"),
        Path.cwd(),
    ]
    image_name = "train-images-idx3-ubyte.gz"
    label_name = "train-labels-idx1-ubyte.gz"
    for d in search_dirs:
        img = d / image_name
        lab = d / label_name
        if img.exists() and lab.exists():
            X_img = read_idx_images(img, max_items=max_items)
            y_img = read_idx_labels(lab, max_items=max_items)
            return {
                "name": "keras_fashion_mnist",
                "images": X_img,
                "labels": y_img,
                "class_names": ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"],
                "source": str(d),
            }

    # fallback은 8x8 digit image다.
    # Fashion-MNIST와 class 의미는 다르지만 image tensor -> flatten -> classifier bridge는 유지된다.
    digits = load_digits()
    return {
        "name": "sklearn_digits_fallback",
        "images": digits.images[:max_items],
        "labels": digits.target[:max_items],
        "class_names": [str(i) for i in range(10)],
        "source": "sklearn.datasets.load_digits fallback",
    }

def get_dataset(dataset_id, inventory=None):
    # 모든 dataset은 notebook-safe local/embedded object를 반환한다.
    # default path에서 외부 다운로드가 필요한 dataset은 여기서 만들지 않는다.
    if dataset_id == "sklearn_iris":
        iris = load_iris()
        return iris.data.astype(float), iris.target.astype(int), iris
    if dataset_id == "toy_logic_gates_xor":
        return pd.DataFrame({"x0": [0, 0, 1, 1], "x1": [0, 1, 0, 1], "y": [0, 1, 1, 0]})
    if dataset_id == "seaborn_titanic":
        prof = dataset_from_inventory_profile(inventory, "seaborn_titanic")
        return prof if prof is not None else fallback_titanic()
    if dataset_id == "toy_missing_values_week14":
        prof = dataset_from_inventory_profile(inventory, dataset_id)
        return prof if prof is not None else pd.DataFrame({"feature_a": [1, 2, np.nan, 4, 5], "feature_b": [10, np.nan, 30, 40, 50], "target": [0, 1, 0, 1, 1]})
    if dataset_id == "toy_scaling_week14":
        prof = dataset_from_inventory_profile(inventory, dataset_id)
        return prof if prof is not None else pd.DataFrame({"small_scale": [1, 2, 3, 4], "large_scale": [100, 500, 900, 1300]})
    if dataset_id == "toy_categorical_encoding_week14":
        prof = dataset_from_inventory_profile(inventory, dataset_id)
        return prof if prof is not None else pd.DataFrame({"color": ["red", "blue", "green", "red"], "label": [1, 0, 1, 0]})
    if dataset_id == "toy_datetime_features_week14":
        prof = dataset_from_inventory_profile(inventory, dataset_id)
        if prof is not None:
            return prof
        dates = pd.to_datetime(["2026-05-01 09:00", "2026-05-02 13:30", "2026-05-03 21:00", "2026-05-04 08:10", "2026-05-05 18:20"])
        return pd.DataFrame({"timestamp": dates, "value": [10, 13, 9, 15, 11]})
    if dataset_id == "keras_fashion_mnist":
        return load_fashion_mnist_or_digits()
    raise ValueError(f"unknown dataset_id: {dataset_id}")

print("Dataset factory ready. 외부 다운로드는 기본 경로에서 사용하지 않는다.")
```

---

## Research → Theory → Math → Visualization Index

이 표는 노트북 전체가 어떤 연구/이론/수학/평가/프레임워크 축에서 설계되었는지 압축한다. 세부 논문 survey가 목적은 아니며, Week13 optimizer companion notebook에서 어떤 근거가 어느 구현으로 연결되는지 보여주는 인덱스다.

| 축 | 내용 | 노트북 구현 |
|---|---|---|
| 논문 | Bootstrap, Momentum/Adam/AdaGrad/AdamW 및 adaptive optimizer generalization 논의 | V04-pre, V04.5 Research Bridge |
| 이론 | stochastic gradient-based optimization, Dense representation, ReLU gate, chain rule, vectorized backprop | V02, V03, V03.5, V04 |
| 수학 | `Z=XW^T+b`, `ReLU=max(0,z)`, `θ ← θ - ηg`, velocity, squared-gradient EMA, first/second moments | V03.5, V04 optimizer classes |
| 통계/평가 | bootstrap resampling, train/validation/test, leakage, accuracy, macro-F1, confusion matrix | V01, V04.5, V05 |
| 프레임워크 | Jupyter, NumPy, Pandas, Matplotlib, scikit-learn | import/helper cells |
| 교수법 | worked example → guided visualization → checkpoint → answer scaffold | V00~Final |
| 체크포인트 | X/y, output/loss/metric, dW/db/dX, optimizer state, validation, CNN bridge | Final rubric |
| 시각화 | contour, heatmap, class distribution, confusion matrix, image grid | V02~V06 |
| 실행 코드 | local/fallback dataset factory, scratch Network, optimizer classes | code cells |

핵심 문장:
Optimizer는 gradient를 만드는 알고리즘이 아니라, 이미 계산된 gradient를 어떻게 parameter update로 바꿀지 정하는 update rule이다.

---

## Web-grounded Source Map

이 표는 각 설계 결정이 어떤 공식 문서 또는 원 논문 근거에 기대는지 보여준다. 링크는 구현을 외부 다운로드에 의존하게 만들기 위한 것이 아니라, notebook cell 설계의 provenance를 남기기 위한 source anchor다.

| 설계 결정 | 근거 문서/논문 | 노트북 반영 위치 |
|---|---|---|
| Markdown + Code cell 교차 구조 | [Jupyter nbformat](https://nbformat.readthedocs.io/en/latest/format_description.html)은 notebook을 `metadata`, `nbformat`, `nbformat_minor`, `cells`를 가진 JSON 구조로 두고 Markdown cell과 Code cell을 기본 타입으로 둔다. | 전체 셀 구조 |
| `.md` canonical source + `.ipynb` 실행본 | [Jupytext](https://jupytext.org/)는 notebook을 `.py` 또는 `.md` text file로 저장해 IDE 편집, version control, AI refactoring에 유리하게 만든다. | 산출물 정책 |
| split-before-fit | [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)는 preprocessing 전에 train/test split을 먼저 하고 test data에 `fit`/`fit_transform`을 쓰지 말라고 한다. | V01, V05 |
| StandardScaler train-only 기준 | [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)는 training samples의 mean/std를 저장해 later data에 `transform`한다고 설명한다. | V01, V05 |
| stratified split | [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)은 `stratify`가 주어지면 class label 기준 stratified split을 수행한다고 설명한다. | V01, V05 |
| Iris DatasetCard | [load_iris](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html)는 150 samples, 4 features, 3 classes의 multiclass classification dataset이다. | V01, V05 |
| Fashion-MNIST bridge | [TensorFlow Datasets Fashion-MNIST](https://www.tensorflow.org/datasets/catalog/fashion_mnist)는 60,000 train + 10,000 test examples, 28x28 grayscale image, 10 classes로 설명된다. | V06 |
| digits fallback | [load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)는 8x8 image, pixel value 0..16, 10 classes의 built-in dataset이다. | V06 fallback |
| macro-F1 | [scikit-learn metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics)는 F-score를 precision/recall 기반으로 두고 multiclass에서 `average` option으로 확장한다. | V05 metric |
| confusion matrix | [confusion_matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)는 `C[i,j]`를 true class `i`, predicted class `j` count로 정의한다. | V05 final evaluation |
| Matplotlib 중심 | [Matplotlib](https://matplotlib.org/stable/)은 static, animated, interactive visualization을 만드는 Python library다. | V02~V06 plots |
| Seaborn optional | [Seaborn](https://seaborn.pydata.org/)은 Matplotlib 기반 high-level statistical visualization library다. | Appendix/optional plots |
| ipywidgets optional | [ipywidgets interact](https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html)는 함수 인자로 UI controls를 자동 생성해 interactive exploration을 지원한다. | optional extension |
| Adam | [Adam paper](https://arxiv.org/abs/1412.6980)는 stochastic objective를 위한 first-order gradient-based optimization이며 lower-order moments의 adaptive estimates를 쓴다. | V04-pre, V04 |
| AdaGrad | [AdaGrad paper](https://jmlr.org/papers/v12/duchi11a.html)는 이전 gradient/data geometry를 반영해 더 informative gradient-based learning을 수행한다. | V04-pre |
| AdamW/generalization caution | adaptive method가 항상 더 나은 generalization을 보장한다고 단정하지 않고, decoupled weight decay 논의는 optimizer 선택 caution으로 둔다. | V04-pre, V05, Final |
| Dense operation/width | [Keras Dense](https://keras.io/api/layers/core_layers/dense/)는 `activation(dot(input, kernel)+bias)`를 계산하며 `units`가 output space의 차원이라고 설명한다. | V03.5, V07 |
| ReLU gate | [Keras ReLU activation](https://keras.io/2/api/layers/activations/)은 기본 ReLU가 `max(x,0)`이라고 설명한다. | V03.5, V07 |
| LeakyReLU caution | [TensorFlow LeakyReLU](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LeakyReLU)는 inactive unit에도 small gradient를 허용한다고 설명한다. | V03.5 note |
| Bootstrap stability | [scikit-learn resample](https://scikit-learn.org/stable/modules/generated/sklearn.utils.resample.html)은 기본 strategy가 bootstrapping procedure의 한 step이라고 설명한다. Efron 1979 bootstrap 논문은 resampling 기반 변동성 추정의 고전적 출발점이다. | V04.5 |
| Representation quality | [scikit-learn silhouette_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)는 intra-cluster distance와 nearest-cluster distance 기반 mean Silhouette Coefficient를 계산한다. | V07-C |
| Classification error report | [classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)는 precision, recall, f1-score, support를 보여주는 text report를 만든다. | V05 selected report |
| Final visual audit | 시각화의 목적은 추가 plot이 아니라 판단 근거를 한 장으로 압축해 answer sentence를 만들게 하는 것이다. | Final Visual Audit Board |

---

### Notebook-as-learning-interface 근거

이 노트북은 단순 `.py` 스크립트가 아니라 Markdown 설명과 Code 실행을 교차시키는 학습 인터페이스다. Jupyter nbformat은 notebook을 top-level dictionary로 정의하고, 그 안에 `metadata`, `nbformat`, `nbformat_minor`, `cells`가 들어간다고 설명한다. 또한 Markdown cell은 body text, Code cell은 kernel 언어의 source code와 output을 담는다. 따라서 본 노트북은 “개념 설명 → 수식 → 실행 코드 → 시각화 → 해석 질문”을 하나의 cell sequence로 설계한다.

버전 관리와 agent refactoring을 위해 canonical source는 `.md` 또는 `py:percent` 형태로 둘 수 있다. Jupytext는 notebook을 `.py` 또는 `.md` 텍스트 파일로 저장해 IDE 편집과 clean diff에 유리하게 만든다. 따라서 최종 산출은 `ML_W13_PREP_VISUAL_LECTURE.ipynb` + `ML_W13_PREP_VISUAL_LECTURE.md` pair를 권장한다.

### Notebook artifact gate

- [ ] `.ipynb`는 `nbformat.validate()`를 통과한다.
- [ ] `.md` 또는 `.py:percent` paired source를 생성한다.
- [ ] source file은 output 없이 diff 가능한 상태로 유지한다.
- [ ] `.ipynb`는 실행 결과 확인용, `.md`/`.py`는 agent refactor용 canonical source로 둔다.

---

## Visualization Method Matrix v2

시각화는 “예쁘게 보여주기”보다, 각 개념의 오해를 줄이는 증거로 사용한다. 기본 실행 경로는 Python-only이며, Matplotlib을 중심으로 둔다.

| 개념 | 시각화 | 기본/선택 | 라이브러리 | 이유 |
|---|---|---|---|---|
| GD trajectory | 1D loss path, 2D contour path | 필수 | Matplotlib | precise line/contour control |
| XOR 비선형성 | scatter + decision region | 필수 | Matplotlib + scikit-learn | decision boundary 직관 |
| Dense backward | heatmap + shape diagram | 필수 | Matplotlib | shape/axis 고정 |
| Dense width/ReLU gate | parameter count line, ReLU derivative, active/dead unit ratio | 필수 | Matplotlib | representation capacity와 gradient gate 연결 |
| SoftmaxCE `p-y` | probability/delta heatmap | 필수 | Matplotlib | class별 gradient 방향 |
| Optimizer state | contour trajectory + update norm | 필수 | Matplotlib | update dynamics |
| Bootstrap stability | width x optimizer boxplot, mean±std errorbar | 필수 | Matplotlib + scikit-learn | data perturbation 민감도 확인 |
| Iris metric | train/val curves + confusion matrix | 필수 | Matplotlib/scikit-learn | loss vs metric 분리 |
| Image tensor | sample grid + flatten/CNN diagram | 필수 | Matplotlib | spatial structure bridge |
| Final audit board | trace board, learning dynamics board, architecture board | 필수 | Matplotlib + tables | 그래프를 시험 답안 문장으로 압축 |
| EDA appendix | count/missing/categorical | 선택 | Seaborn optional | statistical plots |
| LR slider | interactive lr path | 선택 | ipywidgets | local teaching demo only |
| Concept graph | dependency map | 선택 | Mermaid/NetworkX | graph structure |

기본 실행 경로에서는 Matplotlib만으로 모든 필수 그래프가 생성되어야 한다. Seaborn/ipywidgets/NetworkX는 없어도 실패하지 않는 optional path다.

---

## V00. 전체 지도와 역할 분리

이 노트북은 제출용 답안 노트북이 아니라 companion notebook이다. 목표는 optimizer 구현법 자체보다, 같은 gradient를 서로 다른 optimizer가 어떻게 다르게 해석하는지 이해하는 것이다.

V00은 두 개의 지도만 사용한다.

1. 개념 지도: Perceptron/MLP/Backprop/Optimizer/CNN bridge가 어디에 놓이는지 보여준다.
2. 책임 분리 지도: `X_batch`, `y_batch`, `logits`, `dW/db`, `optimizer.step(net)`이 어떤 순서로 연결되는지 보여준다.

Optimizer는 X/y를 보지 않는다. Optimizer는 layer가 들고 있는 param과 grad만 읽고 parameter를 update한다.

---

### V00 디벨롭 플랜

- 시각화 목적: course-level 개념 지도와 execution-level 책임 흐름을 분리해 보여준다.
- 사용할 데이터: 없음. 구조만 다룬다.
- 필요한 전처리: 없음.
- 코드 셀 설계: 책임 분리 flow diagram과 단계별 입력/출력 표.
- 그래프 해석 포인트: `X/y`는 loss 계산까지 필요하지만, optimizer는 `W,b,dW,db`만 본다.
- 학생이 자주 하는 오해: optimizer가 loss나 y를 직접 보고 gradient를 계산한다고 생각한다.
- 체크포인트 질문: `optimizer.step(net)` 직전에 layer 안에 무엇이 준비되어 있어야 하는가?

---

```mermaid
flowchart LR
    A[Perceptron] --> B[MLP]
    B --> C[Chain Rule]
    C --> D[Backprop]
    D --> E[Layer Abstraction]
    E --> F[Optimizer]
    F --> G[Keras fit]
    G --> H[Validation / CNN]
```

이 지도에서 Optimizer는 Backprop 이후에 온다. 즉, gradient를 만드는 단계가 아니라 만들어진 gradient를 사용해 parameter를 이동시키는 단계다.

---

```python
# V00 책임 분리 지도.
# scatter map 대신 실제 실행 순서가 드러나는 flow diagram을 그린다.
flow_nodes = [
    ("X_batch", 0.0, 1.0),
    ("Network.forward", 1.4, 1.0),
    ("logits", 2.8, 1.0),
    ("y_batch", 2.8, 0.0),
    ("Loss.forward", 4.2, 0.5),
    ("scalar loss", 5.6, 0.5),
    ("Loss.backward", 7.0, 0.5),
    ("dlogits", 8.4, 0.5),
    ("Network.backward", 10.0, 0.5),
    ("dW, db, dX\nin layers", 11.7, 0.5),
    ("Optimizer.step(net)", 13.5, 0.5),
    ("updated W,b", 15.0, 0.5),
]

fig, ax = plt.subplots(figsize=(15, 3.5))
for label, x, y in flow_nodes:
    # X/y는 데이터, forward/backward/optimizer는 연산 단계, grad/param은 중간 산출물로 색을 구분한다.
    if label in {"X_batch", "y_batch"}:
        color = "#dceefb"
    elif "Optimizer" in label:
        color = "#f1ce63"
    elif "dW" in label or "dlogits" in label or "updated" in label:
        color = "#c7e9c0"
    else:
        color = "#f3f3f3"
    ax.text(x, y, label, ha="center", va="center", fontsize=9, bbox=dict(boxstyle="round,pad=0.35", facecolor=color, edgecolor="#333333"))

def arrow(a, b):
    # node index로 arrow를 연결해 흐름을 명시한다.
    x1, y1 = flow_nodes[a][1], flow_nodes[a][2]
    x2, y2 = flow_nodes[b][1], flow_nodes[b][2]
    ax.annotate("", xy=(x2 - 0.45, y2), xytext=(x1 + 0.45, y1), arrowprops=dict(arrowstyle="->", lw=1.8))

for a, b in [(0, 1), (1, 2), (2, 4), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11)]:
    arrow(a, b)

ax.set_xlim(-0.7, 15.8)
ax.set_ylim(-0.5, 1.55)
ax.set_axis_off()
ax.set_title("Responsibility flow: X/y create loss and gradients, optimizer updates only params")
plt.show()

responsibility_table = pd.DataFrame(
    [
        ["Network.forward", "X_batch", "logits", "loss"],
        ["Loss.forward", "logits, y_batch", "scalar loss", "backward start"],
        ["Loss.backward", "cached probs/y", "dlogits", "network backward"],
        ["Network.backward", "dlogits, caches", "dW, db, dX", "optimizer"],
        ["Optimizer.step", "W,b,dW,db", "updated W,b", "next forward"],
    ],
    columns=["단계", "입력", "출력", "다음 단계"],
)
display(responsibility_table)
```

---

### V00-advanced. Visualization route map

```python
# V00-advanced: final advanced visualization route map.
# 이 표는 고급 시각화가 장식이 아니라 각 오해를 줄이는 증거임을 먼저 고정한다.
visual_route_map = pd.DataFrame(
    [
        ["V01", "EDA/PCA", "missing/dtype/PCA 2D/3D", "X/y, preprocessing, metric 선택"],
        ["V01", "mixed association", "Pearson/Spearman/Kendall, chi-square/Cramer's V, eta-squared", "변수 타입별 관계 지표와 검정 선택"],
        ["V01", "regression residual", "scatter+line, residual vs fitted, PC residual", "상관에서 모델 검수로 연결"],
        ["V02", "미분과 loss geometry", "tangent, finite difference, 3D/top/front/side", "gradient 방향과 learning rate"],
        ["V03", "backward derivative", "dW/db/dX heatmap, ReLU mask, SoftmaxCE delta", "parameter gradient vs propagated gradient"],
        ["V03.5", "Dense/ReLU theory lab", "width vs parameter count, active/dead ratio", "representation capacity와 gradient gate"],
        ["V04", "optimizer dynamics", "3D trajectory, contour, state norm dashboard", "same gradient, different update rule"],
        ["V04.5", "bootstrap stability", "metric boxplot, ReLU gate boxplot, mean±std", "data perturbation 민감도"],
        ["V05", "Iris decision-space audit", "PCA train-fit, val/test transform, test correctness overlay", "validation 선택과 final report 분리"],
        ["V05.5", "gradient flow audit", "grad norm, update/param ratio, active/dead ratio", "학습 실패 원인 진단"],
        ["V05.6", "ablation lab", "no scaling/no ReLU/width/init/lr comparison", "성능 원인 분해"],
        ["V06", "image tensor bridge", "flattened image PCA, local patch/CNN bridge", "Dense MLP vs CNN structure"],
        ["V07", "proper MLP bridge", "layer-wise representation PCA before/after", "Dense+ReLU block 반복"],
        ["V08", "failure gallery", "symptom/evidence/cause/action/answer cards", "진단을 답안 문장으로 변환"],
        ["Final", "visual audit board", "single-batch trace, dynamics, architecture, answer sentence", "시각화의 답안화"],
    ],
    columns=["section", "advanced focus", "main views", "misunderstanding reduced"],
)
display(visual_route_map)
```

---

그래프 해석 질문:

- `optimizer.step(net)`이 실행되기 전에 반드시 만들어져 있어야 하는 것은 무엇인가?
- optimizer가 `X_batch`와 `y_batch`를 직접 보지 않아도 parameter를 바꿀 수 있는 이유는 무엇인가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

체크포인트: 나는 optimizer가 gradient를 계산하는 것이 아니라, 계산된 gradient로 parameter를 움직이는 주체임을 설명할 수 있다.

---

## Lecture Node Mapping

이 표는 노트북 섹션을 강의 RAG/개념 노드 수준으로 연결한다. 실제 `node_id` 명명은 강의 인벤토리와 완전히 같지 않을 수 있으므로, 여기서는 agent-facing mapping key로 사용한다.

| Notebook section | 강의 노드 | 핵심 개념 | 체크포인트 |
|---|---|---|---|
| V00 | `n_ML8.forward_loss_backward_update`, `n_ML13.section_02` | forward/loss/backward/update, optimizer 책임 분리 | optimizer는 X/y를 보는가 |
| V01 | `n_ML14.dataframe`, `n_ML15.leakage`, `n_ML15.section_03` | X/y, scaling, leakage | split-before-fit 설명 |
| V02 | `n_ML10.gradient_descent`, `n_ML8.xor`, `n_ML8.mlp_xor` | GD, XOR, MLP 필요성 | lr와 XOR 설명 |
| V03 | `n_ML12.vectorized_backprop_batch_dimension_matrix`, `n_ML12.layer_abstraction_activation` | Dense backward, dW/db/dX | shape assert 통과 |
| V04 | `n_ML13.optimizer`, `n_ML13.sgd_momentum_rmsprop_adam` | optimizer state | update rule 비교 |
| V05 | `n_ML13.keras`, `n_ML13.softmax_cross_entropy`, `n_ML15.loss_curve` | Iris 실험, SoftmaxCE, curve 해석 | val/test 구분 |
| V06 | `n_ML15.cnn`, `n_ML15.convolution_layer`, `n_ML15.padding_stride_pooling` | flatten vs CNN | local structure 설명 |

---

## V01. 데이터·출력·손실·지표 설계

V01 본문은 “optimizer 비교 전에 무엇을 고정해야 하는가”만 다룬다. 본문에 남길 항목은 네 가지다.

1. `DatasetCard — sklearn_iris`
2. `DatasetCard — toy_logic_gates_xor`
3. `DatasetCard — Fashion-MNIST / sklearn_digits fallback`
4. scaling + leakage contrast

Appendix note:
Titanic/missing/categorical/datetime 예시는 본문 흐름을 방해하지 않도록 노트북 마지막 Appendix A-D에 둔다.

---

### V01 디벨롭 플랜

- 시각화 목적: optimizer 비교의 본체 데이터와 보조 bridge 데이터를 DatasetCard로 압축한다.
- 사용할 데이터: Iris, XOR, Fashion-MNIST 또는 digits fallback.
- 필요한 전처리: Iris는 train-only StandardScaler, image는 pixel scaling, XOR는 embedded truth table.
- 코드 셀 설계: DatasetCard 표, scaling 비교, leakage contrast.
- 그래프 해석 포인트: optimizer 비교는 model/data/split/init을 고정하고 update rule만 바꿔야 한다.
- 학생이 자주 하는 오해: preprocessing 전체 fit과 train-only fit의 차이를 성능 차이 크기로만 판단한다.
- 체크포인트 질문: Iris optimizer comparison에서 `Dense(3)`, `SoftmaxCE`, macro-F1을 쓰는 이유는 무엇인가?

---

### V01-method. EDA decision map

EDA는 모델링 전 “한 번 훑는 단계”가 아니라 데이터 리스크를 조기 차단하는 의사결정 단계다. John W. Tukey식 관점으로 하나의 가설만 보지 않고 여러 시각에서 자료 구조, 이상치, 누락, 변수 관계를 살핀다.

| 구분 | CDA | EDA |
|---|---|---|
| 출발점 | 가설 검정 | 데이터 탐험 |
| 초점 | 채택/기각 | 구조/패턴 발견 |
| 산출 | 검정 결과 | 리스크 지도, 새 가설, 모델링 조건 |

EDA 4단계:

| 단계 | 확인 | 본 노트북 반영 |
|---|---|---|
| 1. 목적/변수 정의 | X/y, 단위, 타입, target, metric | DatasetCard, output/loss/metric table |
| 2. 전체 스캔 | shape, head/tail, missing, dtype, duplicate/id risk | EDA dashboard, missing/dtype table |
| 3. 단변수 점검 | histogram, boxplot, median/IQR, skew, outlier | Appendix EDA, scaling/re-expression note |
| 4. 관계 탐색 | scatter, crosstab, correlation, PCA, residual | mixed association, PCA, regression residual |

EDA 질문은 확인용 질문이 아니라 다음 행동을 정하는 질문이다.

| 질문 | 확인 | 해야 할 일 |
|---|---|---|
| 데이터셋 크기와 범위는? | row/column 수, class별 표본수, 기간 | 부족하면 수집 확대 또는 문제 재정의 |
| 전체인가 샘플인가? | sampling method, extraction ratio | 일반화 범위 제한, stratified sampling 검토 |
| 모집단 대표성은 충분한가? | class/time/group 분포 | 부족 집단 추가 수집 또는 weighting |
| 이상치/노이즈는 심한가? | IQR, z-score, residual, 도메인 위반 | 오류 correction, true anomaly tagging |
| 가공 데이터가 섞였는가? | lineage, manual edit, derived columns | 원본/가공 분리, data dictionary 작성 |
| 식별자와 중복 문제는? | primary key missing/duplicate | deduplication rule, join key test |
| 결합 기준이 같은가? | unit/timezone/code system | unit standardization, code mapping |
| 누락값은 왜 생겼는가? | missing rate, group/time pattern | delete/impute/model-based imputation 선택 |

EDA 4대 주제:

| 주제 | 의미 | 중심 시각화 |
|---|---|---|
| 저항성 | 이상치에 덜 민감한 통계량 사용 | median/IQR boxplot |
| 잔차 해석 | 추세에서 벗어난 값의 원인 탐색 | residual vs fitted, residual by group |
| 자료 재표현 | log/sqrt/standardization/PCA로 구조 재표현 | raw vs transformed scatter/PCA |
| 현시성 | 그래프 기반 전달 | scatter, heatmap, boxplot, PCA projection |

변수 조합별 이변수 분석 선택:

| 변수 조합 | 주요 시각화 | 수치/검정 방향 | 모델링 연결 |
|---|---|---|---|
| 연속형-연속형 | scatter, regression line, residual plot | covariance, Pearson, Spearman, Kendall | simple regression, transformation, nonlinear 후보 |
| 범주형-범주형 | crosstab, 100% stacked bar, heatmap | chi-square independence, Cramer's V | class imbalance, group effect, encoding |
| 범주형-연속형 | boxplot, group histogram, violin 대체 box | t-test/Z-test, ANOVA, eta-squared | group-specific model, interaction, stratification |
| 다변수 numeric | PCA 2D/3D, PC loading/score plot | explained variance, PC regression residual | dimension reduction, feature compression |

상관 해석 주의:

```text
상관은 같이 변한다는 뜻이고, 인과는 원인-결과를 뜻한다.
r=0은 선형 관계가 약하다는 뜻이지 관계가 전혀 없다는 뜻은 아니다.
공분산은 방향은 유의미하지만 scale에 의존하므로 강도 비교에는 상관계수를 쓴다.
```

---

```python
# V01 본문 DatasetCard.
# 본문은 Week13 optimizer comparison에 직접 필요한 데이터만 압축해서 보여준다.
iris_X, iris_y, iris_meta = get_dataset("sklearn_iris", inventory)
xor_df = get_dataset("toy_logic_gates_xor", inventory)
image_bundle_preview = get_dataset("keras_fashion_mnist", inventory)
image_shape = image_bundle_preview["images"].shape
flat_shape = (image_shape[0], int(np.prod(image_shape[1:])))

dataset_cards = pd.DataFrame(
    [
        [
            "sklearn_iris",
            str(iris_X.shape),
            str(iris_y.shape),
            "multiclass classification",
            "Dense(3)",
            "SoftmaxCE",
            "accuracy, macro-F1, confusion matrix",
            "optimizer comparison 본체",
        ],
        [
            "toy_logic_gates_xor",
            "(4, 2)",
            "(4,)",
            "binary nonlinear separability toy",
            "MLP + nonlinear activation",
            "BCE 또는 CE",
            "decision region, loss curve",
            "Perceptron 한계와 MLP 필요성",
        ],
        [
            f"Fashion-MNIST / {image_bundle_preview['name']} fallback",
            f"image: {image_shape}",
            f"flatten: {flat_shape}",
            "image multiclass bridge",
            "Dense after flatten 또는 CNN",
            "CE",
            "class distribution, sample grid",
            "Dense MLP vs CNN 구조 차이",
        ],
    ],
    columns=["DatasetCard", "X/image", "y/flatten", "task", "output", "loss", "metric", "role"],
)
display(dataset_cards)

# Iris class balance는 optimizer 비교에서 stratified split을 써야 하는 근거다.
iris_class_counts = pd.Series(iris_y).value_counts().sort_index()
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].bar([iris_meta.target_names[i] for i in iris_class_counts.index], iris_class_counts.values, color="#4e79a7")
axes[0].set_title("DatasetCard detail: Iris class distribution")
axes[0].set_ylabel("count")

# XOR는 선형 분리 불가능성을 보여주는 최소 toy dataset이다.
axes[1].scatter(xor_df["x0"], xor_df["x1"], c=xor_df["y"], cmap="coolwarm", s=220, edgecolor="black")
for _, r in xor_df.iterrows():
    axes[1].text(r["x0"] + 0.03, r["x1"] + 0.03, f"y={int(r['y'])}")
axes[1].set_title("DatasetCard detail: XOR")
axes[1].set_xticks([0, 1])
axes[1].set_yticks([0, 1])
axes[1].grid(True, alpha=0.25)
plt.tight_layout()
plt.show()
```

---

### Web-grounded rule: split-before-fit

scikit-learn common pitfalls 기준으로 preprocessing은 split 이후에 수행해야 한다. test data는 `fit` 또는 `fit_transform`에 절대 들어가면 안 된다. train subset에서는 `fit_transform`, validation/test subset에서는 `transform`만 사용한다. 이 규칙은 StandardScaler, imputer, feature selection, PCA 등 거의 모든 preprocessing에 적용된다.

```python
# V01 scaling + leakage contrast.
# 목적: optimizer 비교 전에 preprocessing fit 범위를 train으로 제한해야 함을 확인한다.
iris = load_iris()
X_all = iris.data.astype(float)
y_all = iris.target.astype(int)

# WRONG: scaler.fit_transform(X_all)
# 문제: test subset의 평균/표준편차가 scaler에 들어간다.
X_scaled_wrong = StandardScaler().fit_transform(X_all)
Xw_train, Xw_test, yw_train, yw_test = train_test_split(
    X_scaled_wrong, y_all, test_size=0.3, random_state=SEED, stratify=y_all
)

# RIGHT:
# X_train_scaled = scaler.fit_transform(X_train)
# X_val_scaled = scaler.transform(X_val)
# X_test_scaled = scaler.transform(X_test)
X_train_raw, X_test_raw, y_train_demo, y_test_demo = train_test_split(
    X_all, y_all, test_size=0.3, random_state=SEED, stratify=y_all
)
scaler_demo = StandardScaler()
X_train_right = scaler_demo.fit_transform(X_train_raw)
X_test_right = scaler_demo.transform(X_test_raw)

leakage_demo = pd.DataFrame(
    {
        "path": ["wrong: fit scaler on all X before split", "right: split first, fit scaler on train only"],
        "train_mean_first_feature": [Xw_train[:, 0].mean(), X_train_right[:, 0].mean()],
        "test_mean_first_feature": [Xw_test[:, 0].mean(), X_test_right[:, 0].mean()],
    }
)
display(leakage_demo)

# StandardScaler와 MinMaxScaler는 “값을 바꾸는 목적”이 다르다.
# optimizer 자체보다도 gradient scale과 loss surface 모양에 영향을 줄 수 있다.
scaling_df = get_dataset("toy_scaling_week14", inventory)
scale_numeric = scaling_df.select_dtypes(include=[np.number]).copy()
std_scaled = pd.DataFrame(StandardScaler().fit_transform(scale_numeric), columns=scale_numeric.columns)
mm_scaled = pd.DataFrame(MinMaxScaler().fit_transform(scale_numeric), columns=scale_numeric.columns)

fig, axes = plt.subplots(1, 3, figsize=(12, 3))
scale_numeric.plot(ax=axes[0], marker="o", title="raw")
std_scaled.plot(ax=axes[1], marker="o", title="StandardScaler")
mm_scaled.plot(ax=axes[2], marker="o", title="MinMaxScaler")
for ax in axes:
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("성능 차이가 작아도 원칙상 split-before-fit이 맞다. test/validation 정보는 fit 단계에 들어가면 안 된다.")
```

---

그래프 해석 질문:

- `DatasetCard`를 보면 output dimension, loss, metric을 어떻게 결정할 수 있는가?
- `fit_transform`을 전체 데이터에 먼저 적용하면 왜 leakage가 되는가?
- scaling 방식이 optimizer 비교 결과를 바꿀 수 있는 이유는 무엇인가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

체크포인트: 나는 optimizer 비교 전에 X/y, output, loss, metric, scaling 기준을 고정할 수 있다.

---

### Web-grounded rule: stratified split for Iris

Iris는 class가 3개이고 class별 sample 수가 작다. optimizer 비교에서 class ratio가 split마다 흔들리면 update rule 차이가 아니라 data split 차이를 비교하게 된다. 따라서 `train_test_split(..., stratify=y, random_state=SEED)`를 사용한다.

```python
# Iris EDA: X/y shape, class distribution, feature scatter, split ratio.
# 이 셀은 V05 optimizer comparison 전, Iris가 어떤 multiclass 데이터인지 한 번 더 고정한다.
iris = load_iris()
X_iris = iris.data.astype(float)
y_iris = iris.target.astype(int)

# output이 Dense(3)인 이유: y가 3개 class id를 가진다.
iris_shape_table = pd.DataFrame(
    [
        ["X", X_iris.shape, "4 numeric flower features"],
        ["y", y_iris.shape, "class label 0/1/2"],
        ["output", "(N, 3)", "Dense(3) logits"],
        ["loss/metric", "SoftmaxCE / accuracy, macro-F1", "multiclass classification"],
    ],
    columns=["item", "shape_or_choice", "meaning"],
)
display(iris_shape_table)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
class_counts = pd.Series(y_iris).value_counts().sort_index()
axes[0].bar([iris.target_names[i] for i in class_counts.index], class_counts.values, color="#4e79a7")
axes[0].set_title("Iris class distribution")
axes[0].set_ylabel("count")

# petal length/width는 class separation을 보기 좋은 feature pair다.
axes[1].scatter(X_iris[:, 2], X_iris[:, 3], c=y_iris, cmap="viridis", edgecolor="black")
axes[1].set_title("petal length/width scatter")
axes[1].set_xlabel("petal length")
axes[1].set_ylabel("petal width")

# stratify=y는 train/test class ratio를 유지하기 위한 옵션이다.
X_train_ratio, X_test_ratio, y_train_ratio, y_test_ratio = train_test_split(
    X_iris, y_iris, test_size=0.3, random_state=SEED, stratify=y_iris
)
split_ratio = pd.DataFrame({
    "train": pd.Series(y_train_ratio).value_counts(normalize=True).sort_index(),
    "test": pd.Series(y_test_ratio).value_counts(normalize=True).sort_index(),
})
split_ratio.index = [iris.target_names[i] for i in split_ratio.index]
split_ratio.plot(kind="bar", ax=axes[2], color=["#59a14f", "#f28e2b"])
axes[2].set_title("train/test class ratio after stratified split")
axes[2].set_ylabel("ratio")
axes[2].tick_params(axis="x", rotation=20)
plt.tight_layout()
plt.show()
```

---

### V01-advanced. EDA/PCA geometry views

이 셀은 V01의 데이터 설계를 고차원 geometry로 확장한다. Iris는 4D feature matrix이므로 PCA 2D/3D와 PC projection view를 함께 보고, DataFrame형 예시는 missing/dtype/correlation/PCA dashboard로 확인한다.

```python
# V01-advanced: EDA/PCA geometry views.
# PCA는 원래 feature 축이 아니라 projection 축이다.
# scaling과 PCA를 split 전에 전체 데이터에 fit하면 leakage가 될 수 있으므로,
# 아래 그림은 EDA 설명용이며 V05 실험에서는 train-only fit 원칙을 다시 적용한다.
if adv_vis is not None:
    fig, iris_pca_variance = adv_vis.plot_iris_pca_multiview()
    display(iris_pca_variance)

    # feature scale이 PCA geometry를 바꾸는지 확인한다.
    # 이 그림은 StandardScaler가 "값을 예쁘게 바꾸는 작업"이 아니라
    # optimizer가 보는 loss geometry에도 영향을 줄 수 있음을 보여준다.
    adv_vis.plot_scaling_effect_on_pca()

    # inventory preview 또는 embedded fallback DataFrame에 대해 EDA dashboard를 만든다.
    # target column이 있으면 PCA projection 색상으로 사용하고, 없으면 numeric PCA만 표시한다.
    titanic_preview = get_dataset("seaborn_titanic", inventory)
    target_col = "survived" if "survived" in titanic_preview.columns else None
    adv_vis.plot_generic_eda_dashboard(titanic_preview, target_col=target_col)
else:
    raise RuntimeError("Advanced visualization pack is not loaded. Run the extension loader cell before V01-advanced.")
```

그래프 해석 질문:

- PCA 3D와 PC1-PC2 평면도는 각각 무엇을 보여주고 무엇을 숨기는가?
- StandardScaler 전후 PCA geometry가 달라지는 이유는 무엇인가?
- EDA dashboard에서 missing/dtype/class distribution은 output/loss/metric 선택과 어떻게 연결되는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

### V01-advanced-B. Mixed variable association maps

이 셀은 PCA와 별도로 변수 타입별 관계 분석을 분리한다. 연속형-연속형은 Pearson/Spearman/Kendall, 범주형-범주형은 chi-square independence test와 Cramer's V, 연속형-범주형은 box/hist와 eta-squared/ANOVA/Welch t 후보로 본다. binary target이 있으면 point-biserial correlation table도 확인한다.

```python
# V01-advanced-B: mixed variable association maps.
# 모든 변수 관계를 Pearson correlation 하나로 처리하면 안 된다.
# continuous-continuous: Pearson/Spearman/Kendall
# categorical-categorical: chi-square independence + Cramer's V + 100% stacked bar
# continuous-categorical: box/hist + eta-squared + ANOVA/Welch t candidate
# binary target: point-biserial correlation
if adv_vis is not None:
    iris_assoc_df = pd.DataFrame(X_iris, columns=iris.feature_names)
    iris_assoc_df["species"] = pd.Categorical.from_codes(y_iris, iris.target_names)
    iris_assoc_df["is_setosa"] = (iris_assoc_df["species"] == "setosa").astype(int)
    iris_assoc_df["petal_bucket"] = pd.cut(
        iris_assoc_df["petal length (cm)"],
        bins=3,
        labels=["short", "mid", "long"],
    )
    fig, iris_assoc_tables = adv_vis.plot_mixed_association_dashboard(iris_assoc_df, target_col="is_setosa")
    print("Iris association columns:")
    display(iris_assoc_tables["numeric_columns"])
    display(iris_assoc_tables["categorical_columns"])
    print("Iris eta-squared: numeric feature vs species")
    display(iris_assoc_tables["eta_squared"].sort_values("species", ascending=False))
    print("Iris chi-square/Cramer's V: species vs petal_bucket")
    observed_counts, expected_counts, chi_square_summary = adv_vis.chi_square_pair_test(
        iris_assoc_df,
        "species",
        "petal_bucket",
    )
    display(observed_counts)
    display(expected_counts)
    display(chi_square_summary)
    fig, iris_petal_pct = adv_vis.plot_categorical_100pct_stacked(
        iris_assoc_df,
        x_col="species",
        hue_col="petal_bucket",
    )
    display(iris_petal_pct)
    fig, iris_group_stats, iris_group_tests = adv_vis.plot_continuous_by_category_gallery(
        iris_assoc_df,
        numeric_col="petal width (cm)",
        category_col="species",
    )
    print("Iris continuous-categorical diagnostics: petal width by species")
    display(iris_group_stats)
    display(iris_group_tests)
    print("Iris point-biserial: numeric feature vs binary is_setosa")
    display(iris_assoc_tables["point_biserial"])

    titanic_assoc_df = get_dataset("seaborn_titanic", inventory)
    titanic_target = "survived" if "survived" in titanic_assoc_df.columns else None
    fig, titanic_assoc_tables = adv_vis.plot_mixed_association_dashboard(titanic_assoc_df, target_col=titanic_target)
    print("Titanic-style mixed association: Pearson/Spearman/Kendall/Cramer's V/chi-square/eta-squared")
    for name in ["pearson", "spearman", "kendall", "cramers_v", "chi_square", "eta_squared", "point_biserial"]:
        table = titanic_assoc_tables[name]
        if not table.empty:
            print(name)
            display(table)
    if {"sex", "survived"}.issubset(titanic_assoc_df.columns):
        print("Titanic-style categorical-categorical test: sex vs survived")
        observed_counts, expected_counts, chi_square_summary = adv_vis.chi_square_pair_test(
            titanic_assoc_df,
            "sex",
            "survived",
        )
        display(observed_counts)
        display(expected_counts)
        display(chi_square_summary)
        fig, survived_by_sex_pct = adv_vis.plot_categorical_100pct_stacked(
            titanic_assoc_df,
            x_col="sex",
            hue_col="survived",
        )
        display(survived_by_sex_pct)
    if {"age", "survived"}.issubset(titanic_assoc_df.columns):
        print("Titanic-style continuous-categorical test: age by survived")
        fig, age_group_stats, age_group_tests = adv_vis.plot_continuous_by_category_gallery(
            titanic_assoc_df,
            numeric_col="age",
            category_col="survived",
        )
        display(age_group_stats)
        display(age_group_tests)
else:
    raise RuntimeError("Advanced visualization pack is not loaded. Run the extension loader cell before V01-advanced-B.")
```

그래프 해석 질문:

- Pearson과 Spearman이 다른 값을 보이면 어떤 관계를 의심할 수 있는가?
- `sex`와 `survived`처럼 범주형끼리의 관계에서 chi-square p-value와 Cramer's V는 각각 무엇을 말하는가?
- 100% 누적막대가 raw count 막대보다 더 적합한 경우는 언제인가?
- 범주별 boxplot과 ANOVA/Welch t 결과가 다를 때는 무엇을 먼저 의심해야 하는가?
- Iris에서 eta-squared가 큰 feature는 species class 구분에 어떤 의미가 있는가?
- association이 높다는 사실과 causal relationship은 왜 다른가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

### V01-advanced-C. Correlation to regression residual diagnostics

이 셀은 상관분석이 모델링으로 어떻게 이어지는지 보여준다. 연속형-연속형 scatter에서 Pearson/Spearman/Kendall을 확인한 뒤 단순 회귀선을 fit하고, residual pattern을 봐서 변환, 그룹별 차이, 다변수 feature, PCA 기반 압축 모델이 필요한지 판단한다.

```python
# V01-advanced-C: correlation -> simple regression -> residual pattern -> PC regression.
# 중심 시각화는 scatter+regression line이 아니라 residual plot이다.
# correlation이 높아도 residual이 group별로 치우치면 hidden categorical structure,
# nonlinear pattern, omitted variable 문제를 의심해야 한다.
if adv_vis is not None:
    iris_reg_df = pd.DataFrame(X_iris, columns=iris.feature_names)
    iris_reg_df["species"] = pd.Categorical.from_codes(y_iris, iris.target_names)

    fig, cov_corr_demo = adv_vis.plot_covariance_to_correlation_demo()
    display(cov_corr_demo)

    # 단순 회귀: petal length 하나로 petal width를 예측한다.
    # Pearson이 높은 pair라도 species별 residual 패턴이 남으면 단일 직선 모델의 한계를 의심한다.
    fig, simple_regression_metrics = adv_vis.plot_simple_regression_residual_diagnostics(
        iris_reg_df,
        x_col="petal length (cm)",
        y_col="petal width (cm)",
        group_col="species",
    )
    display(simple_regression_metrics)

    # 다변수일 때는 원 feature 공간을 한 번에 보기 어렵다.
    # PC1/PC2 score를 압축 predictor로 사용하고 residual이 PC space에서 어디에 남는지 본다.
    fig, pc_regression_metrics = adv_vis.plot_pc_regression_residual_diagnostics(
        iris_reg_df,
        feature_cols=["sepal length (cm)", "sepal width (cm)", "petal length (cm)"],
        target_col="petal width (cm)",
        group_col="species",
        n_components=2,
    )
    display(pc_regression_metrics)
else:
    raise RuntimeError("Advanced visualization pack is not loaded. Run the extension loader cell before V01-advanced-C.")
```

그래프 해석 질문:

- 공분산은 방향을 보여주지만 강도 비교에는 왜 부적절한가?
- 단순 회귀 residual이 fitted value나 species별로 패턴을 보이면 다음 모델 선택은 어떻게 달라지는가?
- PC regression residual이 PC score 공간에서 군집을 보이면 어떤 feature 또는 group 구조를 추가로 의심해야 하는가?
- 상관이 높다는 사실과 좋은 예측 모델이라는 사실은 왜 다를 수 있는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

## Dataset Policy / Inventory Status

V01 이후의 실행 정책은 아래와 같다. 기본 실행은 외부 다운로드 없이 끝나야 하며, inventory가 없어도 fallback으로 동작해야 한다.

| dataset_id | role | default path | fallback | notebook use |
|---|---|---|---|---|
| `sklearn_iris` | primary | sklearn builtin | 없음 | V01 DatasetCard, V05 optimizer comparison |
| `toy_logic_gates_xor` | primary | embedded DataFrame | 없음 | V01 DatasetCard, V02 XOR |
| `keras_fashion_mnist` | primary bridge | local IDX gzip cache | `sklearn_digits_fallback` | V01 DatasetCard, V06 image/CNN bridge |
| `seaborn_titanic` | appendix secondary | inventory `head_10` | embedded mini table | Appendix A |
| `toy_missing_values_week14` | appendix secondary | inventory profile | embedded mini table | Appendix B |
| `toy_categorical_encoding_week14` | appendix secondary | inventory profile | embedded mini table | Appendix C |
| `toy_datetime_features_week14` | appendix secondary | inventory profile | embedded mini table | Appendix D |
| `boston_housing_cmu_legacy` | avoid/defer | external/reference only | none | note only |
| `uci_appliances_energy_prediction` | avoid/defer | external/reference only | none | note only |
| `keras_mnist_or_openml_mnist` | avoid/defer | uncached/download path | Fashion-MNIST/digits path | note only |
| `daisy_image_missing_local_file` | avoid/defer | missing local image risk | none | note only |

---

## V02. Gradient Descent와 XOR Bridge

gradient는 loss가 증가하는 방향이고, gradient descent는 그 반대 방향으로 parameter를 이동한다. learning rate가 너무 작으면 느리고, 너무 크면 overshoot/oscillation/divergence가 생길 수 있다.

V02의 `MLPClassifier`는 **XOR 비선형 결정영역을 빠르게 보기 위한 시각화 전용**이다. Week13 optimizer 비교 본체는 V04~V05의 scratch `Network`, `Dense`, `ReLU`, `SoftmaxCE`, `optimizer.step(net)`에서 수행한다.

---

### V02 디벨롭 플랜

- 시각화 목적: gradient 방향, learning rate 크기, XOR의 비선형 필요성을 하나의 흐름으로 연결한다.
- 사용할 데이터: 1D/2D synthetic quadratic surface, `toy_logic_gates_xor`.
- 필요한 전처리: XOR label을 0/1로 고정하고 작은 MLP를 같은 seed로 학습한다.
- 코드 셀 설계: 1D path, 2D contour/arrows, XOR truth table, linear-boundary 실패 도식, MLP decision region, loss curve.
- 그래프 해석 포인트: gradient는 증가 방향이고 update는 반대 방향이다. XOR는 feature transform 없이는 직선 하나로 분리되지 않는다.
- 학생이 자주 하는 오해: learning rate가 클수록 항상 빠르다고 생각하거나, hidden layer가 단순히 parameter 수만 늘린다고 생각한다.
- 체크포인트 질문: XOR에서 hidden layer와 non-linear activation은 무엇을 바꾸는가?

---

```python
# V02-A: 1D/2D Gradient Descent path.
# 목적: optimizer state를 보기 전에 learning rate와 gradient 방향만으로도 경로가 달라짐을 확인한다.
def f1(x):
    # 최소점은 x=3이다.
    return (x - 3) ** 2

def df1(x):
    # f1의 analytic gradient.
    return 2 * (x - 3)

def gd_1d_path(x0, lr, steps=12):
    # 같은 시작점 x0에서 learning rate만 바꿔 이동 경로를 만든다.
    xs = [x0]
    x = x0
    for _ in range(steps):
        x = x - lr * df1(x)
        xs.append(x)
    return np.array(xs)

grid = np.linspace(-2, 7, 300)
fig, ax = plt.subplots()
ax.plot(grid, f1(grid), color="black", label="f(x)=(x-3)^2")
for lr in [0.05, 0.2, 0.8, 1.1]:
    path = gd_1d_path(-1.5, lr)
    ax.plot(path, f1(path), marker="o", label=f"lr={lr}")
ax.set_title("1D loss curve 위 learning rate별 step path")
ax.set_xlabel("x")
ax.set_ylabel("loss")
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()

def gd_2d_path(w0, lr=0.2, steps=35):
    # synthetic 2D parameter vector w를 직접 이동시킨다.
    # 이 w는 Dense.W가 아니라 optimizer trajectory 직관용 parameter다.
    path = [np.array(w0, dtype=float)]
    w = np.array(w0, dtype=float)
    for _ in range(steps):
        w = w - lr * quad_grad(w)
        path.append(w.copy())
    return np.vstack(path)

W1, W2, loss_surface_Z = make_quad_grid()
fig, ax = plt.subplots()
ax.contour(W1, W2, loss_surface_Z, levels=25, cmap="viridis")
path2 = gd_2d_path([5, 2.5], lr=0.18)
ax.plot(path2[:, 0], path2[:, 1], marker="o", color="#e15759")
ax.set_title("2D contour 위 GD path")
ax.set_xlabel("w0")
ax.set_ylabel("w1")
plt.show()

# V02-B: XOR 선형 분리 불가능성.
xor_df = pd.DataFrame({"x0": [0, 0, 1, 1], "x1": [0, 1, 0, 1], "y": [0, 1, 1, 0]})
fig, ax = plt.subplots()
ax.scatter(xor_df["x0"], xor_df["x1"], c=xor_df["y"], cmap="coolwarm", s=220, edgecolor="black")
for _, r in xor_df.iterrows():
    ax.text(r["x0"] + 0.03, r["x1"] + 0.03, f"y={int(r['y'])}")
ax.set_title("XOR scatter plot: 단일 선형 경계로 분리되지 않음")
ax.set_xlabel("x0")
ax.set_ylabel("x1")
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.grid(True, alpha=0.3)
plt.show()
print("XOR는 단일 선형 경계로 분리되지 않으므로 MLP와 nonlinear activation이 필요하다.")
```

---

### V02-advanced. Derivative and high-dimensional loss multi-view

이 셀은 V02의 gradient descent를 미분 자체의 시각화로 확장한다. 1D에서는 tangent와 finite difference를 보고, 2D에서는 같은 loss surface를 3D surface, 평면도, 정면도, 측면도로 나눠 본다.

```python
# V02-advanced: derivative and 3D/multi-view loss surface.
# gradient는 loss가 증가하는 방향이고, gradient descent update는 그 반대 방향이다.
# 3D surface 하나만 보면 curvature를 오해하기 쉬우므로 top/front/side view를 함께 둔다.
if adv_vis is not None:
    fig, slope_table = adv_vis.plot_1d_derivative_tangent(x0=5.0, lr=0.25)
    display(slope_table)

    gd_path_adv, gd_losses_adv = adv_vis.run_plain_gd_path(start=(5.0, 2.5), lr=0.12, steps=35)
    adv_vis.plot_quadratic_multiview(gd_path_adv, gd_losses_adv, title_prefix="V02 advanced GD")
    adv_vis.plot_gradient_field_and_partial_slices()
else:
    raise RuntimeError("Advanced visualization pack is not loaded. Run the extension loader cell before V02-advanced.")
```

그래프 해석 질문:

- tangent slope와 finite difference slope가 같은 개념을 어떻게 다르게 보여주는가?
- 3D surface, 평면도, 정면도, 측면도 중 overshoot를 가장 잘 보여주는 view는 무엇인가?
- `dL/dw0`와 `dL/dw1` scale이 다르면 같은 learning rate에서 어떤 문제가 생기는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

그래프 해석 질문:

- learning rate가 커질수록 이동 경로는 어떻게 달라지는가?
- 2D contour에서 좁은 축 방향으로 진동이 커지는 이유는 무엇인가?
- XOR가 MLP와 nonlinear activation을 요구하는 이유는 무엇인가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

체크포인트: 나는 gradient와 learning rate가 parameter 이동 경로를 어떻게 바꾸는지 설명할 수 있다.

---

```python
# XOR decision region — sklearn MLPClassifier visualization only.
# 이 셀은 XOR의 비선형 결정영역을 빠르게 보기 위한 시각화 전용이다.
# Week13 optimizer 비교 본체는 V04~V05의 scratch Network에서 수행한다.
xor_df = get_dataset("toy_logic_gates_xor", inventory)
display(xor_df.rename(columns={"x0": "input_0", "x1": "input_1", "y": "xor_y"}))

X_xor = xor_df[["x0", "x1"]].to_numpy(dtype=float)
y_xor = xor_df["y"].to_numpy(dtype=int)

# solver="lbfgs"는 작은 XOR toy에서 안정적으로 decision region을 만들기 위한 선택이다.
# 내부 optimizer는 숨겨져 있으므로 이 셀을 optimizer 비교 근거로 쓰지 않는다.
mlp = MLPClassifier(
    hidden_layer_sizes=(4,), activation="tanh", solver="lbfgs", alpha=1e-4,
    random_state=SEED, max_iter=5000
)
mlp.fit(X_xor, y_xor)

# 2D grid 전체에 대해 P(y=1)을 계산해 decision region을 그린다.
xx, yy = np.meshgrid(np.linspace(-0.35, 1.35, 160), np.linspace(-0.35, 1.35, 160))
grid_points = np.c_[xx.ravel(), yy.ravel()]
zz = mlp.predict_proba(grid_points)[:, 1].reshape(xx.shape)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].scatter(X_xor[:, 0], X_xor[:, 1], c=y_xor, cmap="coolwarm", s=260, edgecolor="black")
for _, r in xor_df.iterrows():
    axes[0].text(r["x0"] + 0.04, r["x1"] + 0.04, f"{int(r['x0'])},{int(r['x1'])} -> {int(r['y'])}")
axes[0].set_title("XOR truth scatter")
axes[0].set_xticks([0, 1])
axes[0].set_yticks([0, 1])
axes[0].grid(True, alpha=0.25)

# 두 후보 직선은 XOR를 단일 직선으로 분리하려는 시도가 실패함을 보여준다.
axes[1].scatter(X_xor[:, 0], X_xor[:, 1], c=y_xor, cmap="coolwarm", s=260, edgecolor="black")
for slope, intercept, label in [(1, -0.25, "candidate line A"), (-1, 1.25, "candidate line B")]:
    line_x = np.linspace(-0.25, 1.25, 20)
    axes[1].plot(line_x, slope * line_x + intercept, linestyle="--", label=label)
axes[1].set_title("single linear boundary cannot isolate XOR")
axes[1].set_xlim(-0.35, 1.35)
axes[1].set_ylim(-0.35, 1.35)
axes[1].legend(fontsize=8)
axes[1].grid(True, alpha=0.25)

# 비선형 hidden layer를 거치면 XOR decision region이 만들어진다.
contour = axes[2].contourf(xx, yy, zz, levels=20, cmap="coolwarm", alpha=0.7)
axes[2].contour(xx, yy, zz, levels=[0.5], colors="black", linewidths=2)
axes[2].scatter(X_xor[:, 0], X_xor[:, 1], c=y_xor, cmap="coolwarm", s=260, edgecolor="black")
axes[2].set_title("sklearn MLPClassifier visualization only")
axes[2].set_xlim(-0.35, 1.35)
axes[2].set_ylim(-0.35, 1.35)
fig.colorbar(contour, ax=axes[2], fraction=0.046, label="P(y=1)")
plt.tight_layout()
plt.show()

print("주의: 이 셀은 decision region 시각화 전용이다. scratch optimizer 비교는 V04~V05에서 수행한다.")
```

---

## V03. Dense.backward, ReLU, SoftmaxCE Shape

Dense convention은 아래로 고정한다.

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

Keras Dense의 kernel은 보통 `(Din, Dout)`이다. 이 노트북의 scratch Dense는 강의 코드와 맞춰 `W = (Dout, Din)`으로 둔다.

Optimizer는 X/y를 보지 않는다. Optimizer는 layer가 들고 있는 param과 grad만 읽고 parameter를 update한다.

---

### V03 디벨롭 플랜

- 시각화 목적: backward에서 생기는 `dW`, `db`, `dX`의 shape와 목적을 분리한다.
- 사용할 데이터: 작은 synthetic batch/logits.
- 필요한 전처리: Week13 scratch Dense convention을 `W=(Dout,Din)`으로 고정한다.
- 코드 셀 설계: shape table, matrix multiplication diagram, ReLU mask, softmax probability, `p-y` heatmap.
- 그래프 해석 포인트: `dW/db`는 현재 layer의 parameter update용이고 `dX`는 이전 layer로 전달된다.
- 학생이 자주 하는 오해: `dX`도 optimizer가 update한다고 생각하거나, activation layer에 dW/db가 있다고 생각한다.
- 체크포인트 질문: `dZ.T @ X`가 왜 `(Dout, Din)` shape를 만드는가?

---

```python
# V03 Dense.backward shape 검증.
# 이 셀은 강의 convention인 W=(Dout,Din)을 코드와 assert로 고정한다.
B, Din, Dout = 4, 3, 2
X = np.random.randn(B, Din)
W = np.random.randn(Dout, Din)
b = np.random.randn(Dout)

# forward: X @ W.T + b.
# Keras Dense kernel convention인 (Din,Dout)과 반대이므로 W.T가 필요하다.
Z = X @ W.T + b

# dZ는 다음 연산/loss에서 현재 Dense output Z로 되돌아온 gradient다.
dZ = np.random.randn(B, Dout)
dW = dZ.T @ X
db = dZ.sum(axis=0)
dX = dZ @ W

shape_table = pd.DataFrame(
    [
        ["X", X.shape, "mini-batch input"],
        ["W", W.shape, "scratch Dense: (Dout, Din)"],
        ["b", b.shape, "bias"],
        ["Z", Z.shape, "X @ W.T + b"],
        ["dZ", dZ.shape, "upstream gradient"],
        ["dW", dW.shape, "parameter gradient"],
        ["db", db.shape, "parameter gradient"],
        ["dX", dX.shape, "gradient sent to previous layer"],
    ],
    columns=["name", "shape", "meaning"],
)
display(shape_table)

fig, axes = plt.subplots(1, 3, figsize=(12, 3))
for ax, arr, title in zip(axes, [dW, dX, (Z > 0).astype(int)], ["dW heatmap", "dX heatmap", "ReLU mask heatmap"]):
    im = ax.imshow(arr, aspect="auto", cmap="coolwarm")
    ax.set_title(title)
    fig.colorbar(im, ax=ax, fraction=0.046)
plt.tight_layout()
plt.show()


# SoftmaxCE demo logits.
logits = np.array([[2.0, 0.5, -1.0], [0.2, 1.5, 0.1], [-0.5, 0.3, 1.2], [1.0, 0.8, 0.7]])
y_demo = np.array([0, 1, 2, 1])
y_onehot = one_hot(y_demo, 3)
probs = softmax(logits)
delta = (probs - y_onehot) / len(y_demo)

# 자동 shape 검증.
# 여기서 실패하면 Dense convention이나 SoftmaxCE gradient convention이 깨진 것이다.
assert Z.shape == (B, Dout)
assert dZ.shape == (B, Dout)
assert dW.shape == W.shape
assert db.shape == b.shape
assert dX.shape == X.shape
assert probs.shape == logits.shape
assert delta.shape == logits.shape
assert np.allclose(probs.sum(axis=1), 1.0)

fig, axes = plt.subplots(1, 2, figsize=(10, 3))
for ax, arr, title in zip(axes, [probs, delta], ["Softmax probability heatmap", "p-y delta heatmap"]):
    im = ax.imshow(arr, aspect="auto", cmap="viridis")
    ax.set_title(title)
    ax.set_xlabel("class")
    ax.set_ylabel("sample")
    fig.colorbar(im, ax=ax, fraction=0.046)
plt.tight_layout()
plt.show()
print("delta = (probs - y_onehot) / B 는 SoftmaxCE가 logits로 되돌려주는 batch 평균 gradient다.")
```

---

그래프 해석 질문:

- `dW/db`와 `dX`의 목적은 어떻게 다른가?
- `p-y`에서 정답 class의 값은 어떤 방향으로 움직이는가?
- Keras Dense convention과 scratch Dense convention을 섞으면 어떤 shape 오류가 생길 수 있는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

체크포인트: `dW/db`는 현재 layer의 parameter update용 gradient이고, `dX`는 이전 layer로 전달할 gradient다.

---

```python
# Dense backward matrix multiplication diagrams: dW, db, dX roles.
# 목적: dW/db와 dX를 분리해 optimizer가 무엇을 읽는지 고정한다.
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

def draw_shape(ax, labels, title):
    # labels: (표시 텍스트, 박스 폭, 색상) 목록.
    # matrix multiplication의 shape 흐름을 한 줄 diagram으로 만든다.
    ax.set_title(title)
    ax.set_axis_off()
    x = 0.05
    for text, width, color in labels:
        rect = plt.Rectangle((x, 0.35), width, 0.28, facecolor=color, edgecolor="black", alpha=0.85)
        ax.add_patch(rect)
        ax.text(x + width / 2, 0.49, text, ha="center", va="center", fontsize=10)
        x += width + 0.05

draw_shape(axes[0], [("dZ.T\n(Dout,B)", 0.25, "#f28e2b"), ("@", 0.08, "#ffffff"), ("X\n(B,Din)", 0.22, "#4e79a7"), ("=", 0.08, "#ffffff"), ("dW\n(Dout,Din)", 0.25, "#59a14f")], "dW: parameter gradient")
draw_shape(axes[1], [("sum over\nbatch axis", 0.32, "#edc948"), ("dZ\n(B,Dout)", 0.25, "#f28e2b"), ("=", 0.08, "#ffffff"), ("db\n(Dout,)", 0.22, "#59a14f")], "db: bias gradient")
draw_shape(axes[2], [("dZ\n(B,Dout)", 0.25, "#f28e2b"), ("@", 0.08, "#ffffff"), ("W\n(Dout,Din)", 0.25, "#4e79a7"), ("=", 0.08, "#ffffff"), ("dX\n(B,Din)", 0.22, "#af7aa1")], "dX: gradient to previous layer")
plt.suptitle("Dense backward matrix multiplication diagrams")
plt.tight_layout()
plt.show()

role_table = pd.DataFrame([
    ["X", "forward input/cache", "직접 보지 않음"],
    ["dX", "이전 layer로 전달", "직접 보지 않음"],
    ["W, b", "parameter", "읽고 update"],
    ["dW, db", "parameter gradient", "읽음"],
    ["p-y", "loss가 만든 logits gradient", "optimizer가 직접 보지 않음"],
], columns=["object", "role", "optimizer relationship"])
display(role_table)
```

---

### V03-advanced. Backward derivative heatmap pack

이 셀은 Dense backward와 activation/loss derivative를 더 깊게 시각화한다. 핵심은 `dW/db`는 optimizer가 읽는 parameter gradient이고, `dX`는 이전 layer로 전달되는 gradient라는 구분이다.

```python
# V03-advanced: Dense backward, ReLU derivative mask, SoftmaxCE delta.
# 이 셀의 figure들은 "shape가 맞는다"를 넘어 gradient가 어디로 가는지 보여준다.
# Activation layer는 parameter가 없어도 backward에서 gradient 흐름을 통과/차단한다.
if adv_vis is not None:
    fig, dense_advanced_shape_table = adv_vis.plot_dense_backward_gradient_views(B=4, Din=3, Dout=2)
    display(dense_advanced_shape_table)
    adv_vis.plot_activation_derivative_views()
    adv_vis.plot_softmax_ce_delta_views()
else:
    raise RuntimeError("Advanced visualization pack is not loaded. Run the extension loader cell before V03-advanced.")
```

그래프 해석 질문:

- `dW` heatmap과 `dX` heatmap은 같은 gradient 정보를 다른 목적으로 쓰는가?
- ReLU derivative mask가 0인 위치에서는 upstream gradient가 어떻게 되는가?
- SoftmaxCE의 `(p-y)/B` heatmap에서 정답 class와 오답 class의 부호는 어떻게 해석하는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

### V03-extra. Shape Failure Modes

이 표는 V03의 assert가 왜 필요한지 설명한다. shape 오류는 대부분 `W` convention 혼동, batch axis 누락, `dW`와 `dX` 역할 혼동에서 나온다.

| failure mode | 잘못된 코드/생각 | 증상 | 수정 기준 |
|---|---|---|---|
| Keras convention 혼동 | scratch `W`를 `(Din,Dout)`로 둔다 | `X @ W.T` 또는 `dZ @ W` shape 오류 | 이 노트북은 `W=(Dout,Din)` |
| batch axis 누락 | `dW = X.T @ dZ`를 그대로 사용 | `dW`가 `(Din,Dout)`로 뒤집힘 | `dW = dZ.T @ X` |
| bias sum axis 오류 | `db = dZ.sum(axis=1)` | `db`가 `(B,)`가 됨 | `db = dZ.sum(axis=0)` |
| `dW`/`dX` 혼동 | optimizer가 `dX`를 update한다고 생각 | 책임 분리 설명 실패 | optimizer는 `W,b,dW,db`만 읽음 |
| Softmax batch 평균 누락 | `delta = probs - y_onehot` | learning rate scale이 batch size에 민감 | `delta = (probs-y)/B` |
| probability normalization 오류 | row sum이 1이 아님 | CE gradient 해석 불가 | `np.allclose(probs.sum(axis=1), 1.0)` |

---

## V03.5. Dense Width & ReLU Action Theory Lab

이 섹션은 Dense와 ReLU를 “층 이름”이 아니라 실제 signal transformation으로 본다. Keras Dense 공식 문서는 Dense가 `activation(dot(input, kernel) + bias)`를 계산하고, `units`가 output space의 차원을 정한다고 설명한다. 이 노트북의 scratch Dense는 강의 convention 때문에 `W=(Dout,Din)`으로 두지만, 수학적 의미는 같다.

ReLU는 `max(0,z)`로 음수 pre-activation을 0으로 막고 양수 신호를 통과시킨다. LeakyReLU처럼 inactive 구간에 작은 gradient를 허용하는 변형도 있지만, Week13 본문은 기본 ReLU gate를 먼저 고정한다.

\[
Z = XW^T + b
\]

\[
A = ReLU(Z) = \max(0, Z)
\]

shape 기준:

```text
X: (B, Din)
Dense(Din -> H): Z = X @ W.T + b
ReLU: A = max(0, Z)
A: (B, H)
```

Iris처럼 `Din=4`, class 수 `K=3`인 1-hidden-layer MLP의 parameter 수는 아래와 같다.

\[
H(D_{in}+1) + K(H+1)
\]

여기서 `H(Din+1)`은 첫 Dense의 `W,b`, `K(H+1)`은 출력 Dense의 `W,b`다. 따라서 Dense width는 hidden feature 개수와 parameter count를 동시에 바꾼다.

ReLU derivative는 아래 gate로 해석한다.

\[
\frac{\partial ReLU(z)}{\partial z}
=
\begin{cases}
1, & z > 0 \\
0, & z \le 0
\end{cases}
\]

즉 ReLU는 forward에서 값을 바꾸는 activation이면서, backward에서 gradient를 통과시킬지 막을지 정하는 gradient gate다.

---

### V03.5 디벨롭 플랜

- 시각화 목적: Dense width가 representation 차원과 parameter 수를 바꾸고, ReLU가 activation/gradient gate로 작동한다는 것을 확인한다.
- 사용할 데이터: Iris `X=(N,4)`, `y=(N,)`.
- 필요한 전처리: activation geometry만 보기 위한 train split과 train-only `StandardScaler`.
- 코드 셀 설계: parameter count table/line plot, ReLU function/derivative, width별 active/dead unit ratio.
- 그래프 해석 포인트: width 증가는 capacity 증가지만, ReLU gate와 optimizer가 함께 작동해야 의미 있는 representation이 된다.
- 학생이 자주 하는 오해: Dense width를 단순히 “뉴런 수가 많으면 좋다”로만 이해하거나, ReLU가 backward에 영향을 주지 않는다고 생각한다.
- 체크포인트 질문: width가 커질 때 parameter count와 active ratio가 항상 같은 방향으로 좋아지는가?

---

```python
# V03.5-A: Dense width -> hidden representation shape -> parameter count.
# Dense width H는 hidden activation A의 column 수이고, 동시에 W/b parameter 수를 늘린다.
def mlp_param_count(Din, H, K):
    # Dense(Din -> H) + ReLU + Dense(H -> K)
    # first Dense: H*Din weights + H bias
    # second Dense: K*H weights + K bias
    return H * (Din + 1) + K * (H + 1)

Din, K = 4, 3
widths = [2, 4, 8, 16, 32, 64, 128]

width_table = pd.DataFrame({
    "hidden_width_H": widths,
    "hidden_activation_shape": [f"(B, {H})" for H in widths],
    "parameter_count": [mlp_param_count(Din, H, K) for H in widths],
})

display(width_table)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(width_table["hidden_width_H"], width_table["parameter_count"], marker="o")
ax.set_title("Dense hidden width changes parameter count")
ax.set_xlabel("hidden width H")
ax.set_ylabel("parameter count")
ax.grid(True, alpha=0.3)
plt.show()
```

---

```python
# V03.5-B: ReLU function and local derivative.
# ReLU는 parameter가 없지만 backward에서 z<=0 위치의 gradient를 차단한다.
z = np.linspace(-5, 5, 400)
relu = np.maximum(0, z)
relu_derivative = (z > 0).astype(float)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].plot(z, relu)
axes[0].axhline(0, color="black", linewidth=0.8)
axes[0].axvline(0, color="black", linewidth=0.8)
axes[0].set_title("ReLU(z) = max(0, z)")
axes[0].set_xlabel("z")
axes[0].set_ylabel("activation")
axes[0].grid(True, alpha=0.3)

axes[1].plot(z, relu_derivative)
axes[1].axhline(0, color="black", linewidth=0.8)
axes[1].axvline(0, color="black", linewidth=0.8)
axes[1].set_title("ReLU local derivative")
axes[1].set_xlabel("z")
axes[1].set_ylabel("dReLU/dz")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

```python
# V03.5-C: Dense width별 ReLU active/dead unit ratio.
# 이 셀은 performance 평가가 아니라 초기 Dense+ReLU block의 signal gate 상태를 보는 이론 실험이다.
# split-before-fit 원칙을 유지하기 위해 scaler는 train subset에만 fit한다.
iris_relu = load_iris()
X_relu = iris_relu.data.astype(float)
y_relu = iris_relu.target.astype(int)

X_relu_train, _, y_relu_train, _ = train_test_split(
    X_relu,
    y_relu,
    test_size=0.3,
    stratify=y_relu,
    random_state=SEED,
)
relu_scaler = StandardScaler()
X_relu_train_scaled = relu_scaler.fit_transform(X_relu_train)

activation_rows = []
for H in [2, 4, 8, 16, 32, 64]:
    # width별로 같은 seed sequence를 쓰면 H가 커질 때 앞쪽 unit은 비슷한 분포에서 출발한다.
    rng = np.random.default_rng(SEED + H)
    W = rng.normal(0, 0.5, size=(H, X_relu_train_scaled.shape[1]))
    b = np.zeros(H)
    Z = X_relu_train_scaled @ W.T + b
    A = np.maximum(0, Z)

    active_ratio = (Z > 0).mean()
    dead_unit_ratio = ((Z <= 0).all(axis=0)).mean()
    mean_activation = A.mean()

    activation_rows.append({
        "hidden_width_H": H,
        "active_ratio": active_ratio,
        "dead_unit_ratio": dead_unit_ratio,
        "mean_activation": mean_activation,
        "parameter_count": mlp_param_count(Din=4, H=H, K=3),
    })

activation_df = pd.DataFrame(activation_rows)
display(activation_df)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

axes[0].plot(activation_df["hidden_width_H"], activation_df["active_ratio"], marker="o")
axes[0].set_title("ReLU active ratio by Dense width")
axes[0].set_xlabel("hidden width")
axes[0].set_ylabel("active ratio")

axes[1].plot(activation_df["hidden_width_H"], activation_df["dead_unit_ratio"], marker="o")
axes[1].set_title("Dead unit ratio by Dense width")
axes[1].set_xlabel("hidden width")
axes[1].set_ylabel("dead unit ratio")

axes[2].plot(activation_df["hidden_width_H"], activation_df["parameter_count"], marker="o")
axes[2].set_title("Parameter count by Dense width")
axes[2].set_xlabel("hidden width")
axes[2].set_ylabel("parameter count")

for ax in axes:
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

그래프 해석 질문:

- width가 커질수록 parameter 수는 어떻게 변하는가?
- active ratio는 항상 커지는가, 아니면 초기 `W`와 data distribution에 따라 달라지는가?
- dead unit ratio가 높으면 backward에서 어떤 일이 생기는가?
- LeakyReLU가 inactive 구간에 작은 gradient를 허용한다는 사실은 ReLU gate 해석을 어떻게 보완하는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

체크포인트: Dense width는 capacity를 키우지만, ReLU gate와 optimizer가 함께 작동해야 의미 있는 representation이 된다.

---

## V04-pre. Optimizer Research/Theory Bridge

V04의 구현은 논문사를 깊게 설명하기보다, 각 optimizer가 “같은 gradient를 어떤 state로 재해석하는가”를 수학/시각화로 연결한다.

### V04-pre-A. Optimizer mechanism map

| Optimizer | state | update intuition | visualization target |
|---|---|---|---|
| SGD | none | 현재 gradient만 반영 | gradient 방향을 그대로 따르는 path |
| Momentum | velocity `v_t` | 이전 이동 방향을 누적 | zig-zag 완화 |
| RMSProp | squared gradient EMA `s_t` | 좌표별 gradient scale 조절 | 좁은 축에서 step 안정화 |
| Adam | first moment `m_t`, second moment `v_t`, bias correction | momentum + adaptive scaling | 빠른 초반 수렴과 update norm 변화 |
| AdaGrad | cumulative squared gradient | 과거 gradient geometry 반영 | 좌표별 step이 시간이 지나며 달라짐 |

Adam 논문은 Adam을 stochastic objective를 위한 first-order gradient-based optimization으로 소개하고, lower-order moments의 adaptive estimates를 쓴다고 설명한다. AdaGrad 논문은 이전 iteration에서 관측된 data geometry를 동적으로 반영해 더 informative gradient-based learning을 수행한다고 설명한다.

### V04-pre-B. Optimizer caution

| 주의 | 이유 | 노트북 반영 |
|---|---|---|
| Adam이 항상 최고라고 말하지 않는다 | adaptive estimate는 빠른 수렴을 줄 수 있지만 validation/test generalization을 자동 보장하지 않는다. | V05에서 validation curve와 final test metric을 분리 |
| train loss만 보고 optimizer를 고르지 않는다 | train loss가 낮아도 validation macro-F1이 다르게 움직일 수 있다. | V05 summary table에서 best validation 기준 선택 |
| raw learning rate끼리 직접 비교하지 않는다 | optimizer마다 stable range가 다르다. | V04 LR sensitivity는 `low/base/high` setting axis 사용 |
| AdamW는 본문 구현 밖 note로 둔다 | decoupled weight decay는 optimizer/regularization 경계 논의가 필요하다. | Final caution, appendix 확장 후보 |

핵심 문장:
Optimizer는 `loss`나 `y`를 다시 계산하지 않는다. Backward가 만든 `grad`를 update rule과 state에 넣어 parameter 이동량을 정한다.

---

## V04. Optimizer 4종: SGD, Momentum, RMSProp, Adam

같은 gradient가 만들어져도 optimizer가 다르면 parameter 이동 경로가 달라진다.

V04는 두 하위 섹션으로 나눈다.

```text
V04-A. Optimizer on synthetic 2D parameter vector
목적: state별 trajectory 직관

V04-B. Optimizer.step(net) on layer parameters
목적: 실제 Dense W,b update 책임 확인
```

---

### V04 디벨롭 플랜

- 시각화 목적: synthetic vector trajectory와 실제 layer parameter update를 분리한다.
- 사용할 데이터: 2D quadratic loss surface, dummy mini-batch, Iris는 V05에서만 사용.
- 필요한 전처리: 없음.
- 코드 셀 설계: optimizer class 정의, V04-A contour trajectory, V04-B dummy net update audit.
- 그래프 해석 포인트: 2D vector의 `w`는 직관용이고, 실제 network에서는 Dense의 `W,b`가 update된다.
- 학생이 자주 하는 오해: optimizer가 `X/y`나 `loss`를 직접 보고 update한다고 생각한다.
- 체크포인트 질문: `optimizer.step(net)`은 layer에서 어떤 object를 순회하는가?

---

```python
# V04-A/B 공통 optimizer 구현.
# 이 class들은 synthetic 2D vector simulation과 실제 Network parameter update를 모두 지원한다.
def iter_params_and_grads(layer):
    # layer가 params_and_grads를 제공하면 그 interface를 우선 사용한다.
    if hasattr(layer, "params_and_grads"):
        yield from layer.params_and_grads()
        return
    # fallback: 강의 Dense convention의 W/dW, b/db attribute를 직접 확인한다.
    if hasattr(layer, "W") and hasattr(layer, "dW"):
        yield "W", layer.W, layer.dW
    if hasattr(layer, "b") and hasattr(layer, "db"):
        yield "b", layer.b, layer.db

class Dense:
    def __init__(self, Din, Dout, rng=None, scale=0.1):
        # W shape은 강의 convention에 맞춰 (Dout,Din)으로 고정한다.
        rng = np.random.default_rng(SEED) if rng is None else rng
        self.W = rng.normal(0, scale, size=(Dout, Din))
        self.b = np.zeros(Dout)
    def forward(self, X):
        # X를 cache해야 backward에서 dW = dZ.T @ X를 계산할 수 있다.
        self.X = X
        return X @ self.W.T + self.b
    def backward(self, dZ):
        # dW/db는 optimizer가 읽는 parameter gradient다.
        # dX는 이전 layer로 전달되는 gradient이며 optimizer가 직접 update하지 않는다.
        self.dW = dZ.T @ self.X
        self.db = dZ.sum(axis=0)
        return dZ @ self.W
    def params_and_grads(self):
        # optimizer.step(net)이 읽는 표준 interface.
        yield "W", self.W, self.dW
        yield "b", self.b, self.db

class ReLU:
    def forward(self, X):
        # mask는 backward에서 gradient를 통과/차단하는 cache다.
        self.mask = X > 0
        return X * self.mask
    def backward(self, dY):
        return dY * self.mask

class SoftmaxCE:
    def forward(self, logits, y):
        # loss는 logits와 y를 보지만 optimizer는 이 둘을 직접 보지 않는다.
        self.y = y
        self.probs = softmax(logits)
        return -np.log(self.probs[np.arange(len(y)), y] + 1e-12).mean()
    def backward(self):
        # SoftmaxCE의 logits gradient.
        y_onehot = np.eye(self.probs.shape[1])[self.y]
        return (self.probs - y_onehot) / len(self.y)

class Network:
    def __init__(self, layers):
        self.layers = layers
    def forward(self, X):
        # layer를 순서대로 통과해 logits를 만든다.
        out = X
        for layer in self.layers:
            out = layer.forward(out)
        return out
    def backward(self, grad):
        # backward는 forward의 역순으로 gradient를 전달한다.
        out = grad
        for layer in reversed(self.layers):
            out = layer.backward(out)
        return out

class OptimizerBase:
    def step(self, net):
        # 실제 network update path.
        # X/y/loss를 보지 않고 layer 안의 param/grad만 순회한다.
        for layer in net.layers:
            for name, param, grad in iter_params_and_grads(layer):
                self.update(param, grad, key=(id(layer), name))
    def simulate_update(self, w, grad):
        # synthetic 2D vector update path.
        # V04-A contour trajectory를 그리기 위한 같은 update rule의 간단 버전이다.
        param = w.copy()
        self.update(param, grad, key=("sim", "w"))
        return param

class SGD(OptimizerBase):
    def __init__(self, lr=0.1):
        self.lr = lr
        self.history = []
    def update(self, param, grad, key=None):
        step = -self.lr * grad
        param += step
        self.history.append(float(np.linalg.norm(step)))

class Momentum(OptimizerBase):
    def __init__(self, lr=0.05, beta=0.9):
        self.lr, self.beta = lr, beta
        self.v = {}
        self.history = []
    def update(self, param, grad, key=None):
        key = key or id(param)
        v = self.v.get(key, np.zeros_like(param))
        v = self.beta * v - self.lr * grad
        self.v[key] = v
        param += v
        self.history.append(float(np.linalg.norm(v)))

class RMSProp(OptimizerBase):
    def __init__(self, lr=0.03, beta=0.9, eps=1e-8):
        self.lr, self.beta, self.eps = lr, beta, eps
        self.s = {}
        self.history = []
    def update(self, param, grad, key=None):
        key = key or id(param)
        s = self.s.get(key, np.zeros_like(param))
        s = self.beta * s + (1 - self.beta) * (grad ** 2)
        self.s[key] = s
        step = -self.lr * grad / (np.sqrt(s) + self.eps)
        param += step
        self.history.append(float(np.linalg.norm(step)))

class Adam(OptimizerBase):
    def __init__(self, lr=0.03, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr, self.beta1, self.beta2, self.eps = lr, beta1, beta2, eps
        self.m, self.v, self.t = {}, {}, {}
        self.history = []
    def update(self, param, grad, key=None):
        key = key or id(param)
        m = self.m.get(key, np.zeros_like(param))
        v = self.v.get(key, np.zeros_like(param))
        t = self.t.get(key, 0) + 1
        m = self.beta1 * m + (1 - self.beta1) * grad
        v = self.beta2 * v + (1 - self.beta2) * (grad ** 2)
        m_hat = m / (1 - self.beta1 ** t)
        v_hat = v / (1 - self.beta2 ** t)
        step = -self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
        param += step
        self.m[key], self.v[key], self.t[key] = m, v, t
        self.history.append(float(np.linalg.norm(step)))

def run_optimizer_path(opt, w0=np.array([5.0, 2.5]), steps=45):
    # V04-A: synthetic parameter vector w를 같은 loss surface 위에서 이동시킨다.
    w = w0.astype(float).copy()
    path = [w.copy()]
    losses = [quad_loss(w)]
    for _ in range(steps):
        grad = quad_grad(w)
        w = opt.simulate_update(w, grad)
        path.append(w.copy())
        losses.append(quad_loss(w))
    return np.vstack(path), np.array(losses), opt

optimizers = {
    "SGD": SGD(lr=0.18),
    "Momentum": Momentum(lr=0.05, beta=0.9),
    "RMSProp": RMSProp(lr=0.08, beta=0.9),
    "Adam": Adam(lr=0.12),
}

W1_v04, W2_v04, loss_surface_Z_v04 = make_quad_grid()
fig, ax = plt.subplots(figsize=(7, 5))
ax.contour(W1_v04, W2_v04, loss_surface_Z_v04, levels=25, cmap="Greys")
state_rows = []
for name, opt in optimizers.items():
    path, losses, fitted = run_optimizer_path(opt)
    ax.plot(path[:, 0], path[:, 1], marker="o", markersize=2.5, label=name)
    for i, step_norm in enumerate(fitted.history[:45]):
        state_rows.append({"optimizer": name, "step": i, "update_norm": step_norm})
ax.set_title("V04-A: optimizer trajectory on synthetic 2D parameter vector")
ax.set_xlabel("w0")
ax.set_ylabel("w1")
ax.legend()
plt.show()

state_df = pd.DataFrame(state_rows)
fig, ax = plt.subplots()
for name, g in state_df.groupby("optimizer"):
    ax.plot(g["step"], g["update_norm"], label=name)
ax.set_title("optimizer state time-series: effective update norm")
ax.set_xlabel("step")
ax.set_ylabel("update norm")
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()

lr_grid = {
    "SGD": {"low": 0.03, "base": 0.12, "high": 0.3},
    "Momentum": {"low": 0.02, "base": 0.05, "high": 0.12},
    "RMSProp": {"low": 0.02, "base": 0.06, "high": 0.12},
    "Adam": {"low": 0.03, "base": 0.08, "high": 0.18},
}
rows = []
for opt_name, settings in lr_grid.items():
    for setting, lr in settings.items():
        opt = {"SGD": SGD, "Momentum": Momentum, "RMSProp": RMSProp, "Adam": Adam}[opt_name](lr=lr)
        _, losses, _ = run_optimizer_path(opt, steps=35)
        rows.append({"optimizer": opt_name, "setting": setting, "lr": lr, "final_loss": losses[-1]})
lr_sensitivity = pd.DataFrame(rows)
display(lr_sensitivity.pivot(index="optimizer", columns="setting", values="final_loss"))
print("주의: low/base/high는 optimizer별 권장 범위를 맞춘 상대 비교 축이다. raw lr 값 자체가 같은 것은 아니다.")
```

---

그래프 해석 질문:

- 같은 loss surface에서 optimizer별 trajectory가 다르게 보이는 이유는 무엇인가?
- Momentum의 state와 RMSProp/Adam의 state는 각각 어떤 정보를 누적하는가?
- learning rate sensitivity grid에서 너무 큰 learning rate는 어떤 징후를 보이는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

체크포인트: 나는 backward가 만든 grad는 같아도 optimizer가 다르면 parameter 이동 경로가 달라진다는 것을 설명할 수 있다.

---

```python
# V04-B: optimizer.step(net) on layer parameters.
# 목적: synthetic vector가 아니라 실제 Dense.W/Dense.b가 update되는 것을 숫자로 확인한다.
optimizer_state_table = pd.DataFrame([
    ["SGD", "none", "theta <- theta - lr*g", "현재 gradient만 사용하므로 좁은 골짜기에서 zig-zag 가능"],
    ["Momentum", "velocity v", "v <- beta*v - lr*g; theta <- theta + v", "반복되는 방향은 누적하고 진동 방향은 완화"],
    ["RMSProp", "squared-gradient accumulator s", "s <- beta*s + (1-beta)*g^2", "좌표별 gradient scale을 나누어 step 크기 조절"],
    ["Adam", "first moment m + second moment v + t", "bias-corrected m_hat/sqrt(v_hat)", "방향 누적과 좌표별 scale 조절을 결합"],
], columns=["optimizer", "state", "update rule summary", "visual interpretation"])
display(optimizer_state_table)

# dummy net은 한 번 forward/backward를 수행해 dW/db를 만든다.
dummy_rng = np.random.default_rng(SEED)
dummy_net = Network([Dense(2, 3, rng=dummy_rng, scale=0.2), ReLU(), Dense(3, 2, rng=dummy_rng, scale=0.2)])
dummy_loss = SoftmaxCE()
dummy_X = np.array([[0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [0.0, 0.0]])
dummy_y = np.array([1, 1, 0, 0])

dummy_logits = dummy_net.forward(dummy_X)
loss_before = dummy_loss.forward(dummy_logits, dummy_y)
dummy_net.backward(dummy_loss.backward())

first_dense = dummy_net.layers[0]
before_W = first_dense.W.copy()
before_W_norm = np.linalg.norm(before_W)
dW_norm = np.linalg.norm(first_dense.dW)

dummy_opt = SGD(lr=0.1)
dummy_opt.step(dummy_net)

after_W_norm = np.linalg.norm(first_dense.W)
update_norm = np.linalg.norm(first_dense.W - before_W)
update_audit = pd.DataFrame(
    [[before_W_norm, dW_norm, after_W_norm, update_norm, loss_before]],
    columns=["before_W_norm", "dW_norm", "after_W_norm", "update_norm", "loss_before_step"],
)
display(update_audit)

pivot = lr_sensitivity.pivot(index="optimizer", columns="setting", values="final_loss").reindex(columns=["low", "base", "high"])
fig, ax = plt.subplots(figsize=(7, 3.5))
im = ax.imshow(pivot.to_numpy(), aspect="auto", cmap="magma_r")
ax.set_title("learning-rate sensitivity grid: final loss")
ax.set_yticks(range(len(pivot.index)), pivot.index)
ax.set_xticks(range(len(pivot.columns)), [str(c) for c in pivot.columns])
ax.set_xlabel("relative lr setting")
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        ax.text(j, i, f"{pivot.iloc[i, j]:.3g}", ha="center", va="center", fontsize=8)
fig.colorbar(im, ax=ax, fraction=0.046)
plt.tight_layout()
plt.show()
print("주의: low/base/high는 optimizer별 권장 범위를 맞춘 상대 비교 축이다. raw lr 값 자체가 같은 것은 아니다.")

print("V04-B 확인: optimizer.step(net)은 X/y가 아니라 Dense layer의 W,b,dW,db를 순회해 parameter를 바꾼다.")
```

---

### V04-advanced. Optimizer trajectory multi-view and state dashboard

이 셀은 V04 optimizer 비교를 3D surface, contour 평면도, 정면도, 측면도로 확장한다. 같은 gradient field 위에서 optimizer state가 trajectory와 update norm을 어떻게 바꾸는지 확인한다.

```python
# V04-advanced: optimizer multi-view and state dashboard.
# 모든 optimizer는 같은 quad_grad를 받는다.
# trajectory가 다른 이유는 gradient를 새로 계산해서가 아니라 update rule/state가 다르기 때문이다.
if adv_vis is not None:
    optimizer_multiview_results = adv_vis.simulate_optimizer_paths(start=(5.0, 2.5), steps=45)
    adv_vis.plot_optimizer_multiview(optimizer_multiview_results)
    adv_vis.plot_optimizer_state_dashboard(optimizer_multiview_results)
else:
    raise RuntimeError("Advanced visualization pack is not loaded. Run the extension loader cell before V04-advanced.")
```

그래프 해석 질문:

- top contour view와 3D surface view 중 optimizer별 zig-zag를 더 잘 보여주는 것은 무엇인가?
- `grad_norm`과 `step_norm`이 다르게 움직이는 optimizer는 어떤 state를 쓰는가?
- Adam이 빠르게 움직이는 구간이 있어도 validation 기준 선택이 필요한 이유는 무엇인가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

## V04.5. Bootstrap × Dense Width × ReLU × Optimizer Stability Lab

Bootstrap은 training data에서 복원추출 sample을 반복적으로 만들어 estimator나 model outcome의 변동성을 보는 방법이다. Efron의 1979 bootstrap 논문은 jackknife와 함께 resampling 기반 추정의 고전적 출발점이고, scikit-learn `resample` 문서는 기본 전략이 bootstrapping procedure의 한 step이라고 설명한다.

이 섹션에서 bootstrap은 성능을 올리는 기법이 아니다. 목적은 같은 Dense/ReLU/optimizer 설계가 training sample perturbation에 얼마나 민감한지 보는 것이다.

핵심 질문:

```text
1. Dense width가 커지면 validation 성능 평균이 좋아지는가?
2. Dense width가 커지면 validation 성능 분산도 커지는가?
3. ReLU active ratio는 width나 bootstrap sample에 따라 달라지는가?
4. 같은 width에서 SGD와 Adam은 bootstrap 분포가 다르게 나오는가?
```

실험 원칙:

```text
one fixed train/val/test split
-> bootstrap resample from train only
-> train same architecture
-> measure fixed validation accuracy / macro-F1 / ReLU active ratio
-> compare distribution by width and optimizer
```

주의:

```text
Bootstrap은 validation/test 원칙을 대체하지 않는다.
Validation set은 고정한다.
Bootstrap은 train subset 안에서만 수행한다.
Test set은 만들지만 이 섹션에서 사용하지 않는다.
```

---

### V04.5 디벨롭 플랜

- 시각화 목적: Dense width, ReLU gate, optimizer choice가 data perturbation에 따라 얼마나 흔들리는지 distribution으로 확인한다.
- 사용할 데이터: Iris train subset bootstrap, fixed validation set.
- 필요한 전처리: split-before-fit, train-only `StandardScaler`, bootstrap은 scaled train subset 내부에서만 수행.
- 코드 셀 설계: width/optimizer별 bootstrap table, validation metric boxplot, ReLU active ratio boxplot, parameter count vs mean accuracy errorbar.
- 그래프 해석 포인트: 단일 score보다 bootstrap distribution과 active/dead unit ratio가 architecture 안정성을 더 잘 보여준다.
- 학생이 자주 하는 오해: bootstrap을 test 대체물로 보거나, Adam/width 증가를 항상 일반화 성능 향상으로 해석한다.
- 체크포인트 질문: 같은 validation set에서 bootstrap 분산이 큰 조합은 어떤 리스크를 뜻하는가?

---

```python
# V04.5-A: Bootstrap stability experiment setup.
# 기본 실행 경로는 sklearn Iris만 사용하며 외부 다운로드가 없다.
# test set은 만들지만 이 섹션에서는 평가하지 않는다. test는 V05 final report용이다.
from sklearn.utils import resample

BOOT_N = 12
BOOT_EPOCHS = 35
BOOT_WIDTHS = (4, 16, 64)
BOOT_OPTIMIZERS = ("SGD", "Adam")

def make_bootstrap_iris_data(seed=SEED):
    iris = load_iris()
    X = iris.data.astype(float)
    y = iris.target.astype(int)

    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=seed
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.25, stratify=y_trainval, random_state=seed
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    return X_train, X_val, X_test, y_train, y_val, y_test

def make_width_net(width, seed=SEED):
    # Dense width H가 hidden representation 차원이다.
    rng = np.random.default_rng(seed)
    return Network([
        Dense(4, width, rng=rng, scale=0.15),
        ReLU(),
        Dense(width, 3, rng=rng, scale=0.15),
    ])

def make_boot_optimizer(name):
    # SGD와 Adam의 raw lr은 같게 맞추지 않는다.
    # optimizer별 stable range가 다르므로 여기서는 comparable starter setting을 둔다.
    if name == "SGD":
        return SGD(lr=0.08)
    if name == "Adam":
        return Adam(lr=0.03)
    raise ValueError(name)

def evaluate_net(net, X, y):
    logits = net.forward(X)
    probs = softmax(logits)
    pred = probs.argmax(axis=1)
    loss_fn = SoftmaxCE()
    loss = loss_fn.forward(logits, y)
    return {
        "loss": float(loss),
        "accuracy": accuracy_score(y, pred),
        "macro_f1": f1_score(y, pred, average="macro"),
        "pred": pred,
    }

def hidden_relu_stats(net, X):
    # 첫 Dense의 pre-activation Z를 직접 계산해 ReLU gate 상태를 본다.
    # 이 값은 optimizer가 직접 보는 값이 아니라 representation diagnostic이다.
    first_dense = net.layers[0]
    Z = X @ first_dense.W.T + first_dense.b
    active_ratio = (Z > 0).mean()
    dead_unit_ratio = ((Z <= 0).all(axis=0)).mean()
    mean_abs_preactivation = np.abs(Z).mean()
    return active_ratio, dead_unit_ratio, mean_abs_preactivation

def train_width_net_on_bootstrap(X_boot, y_boot, X_val, y_val, width, optimizer_name, seed, epochs=BOOT_EPOCHS):
    net = make_width_net(width, seed=seed)
    optimizer = make_boot_optimizer(optimizer_name)
    loss_fn = SoftmaxCE()
    rng = np.random.default_rng(seed)
    batch_size = 16

    for _ in range(epochs):
        # bootstrap sample 안에서만 mini-batch 순서를 섞는다.
        order = rng.permutation(len(X_boot))
        for start in range(0, len(X_boot), batch_size):
            idx = order[start:start + batch_size]
            logits = net.forward(X_boot[idx])
            loss_fn.forward(logits, y_boot[idx])
            net.backward(loss_fn.backward())
            optimizer.step(net)

    val_result = evaluate_net(net, X_val, y_val)
    active_ratio, dead_unit_ratio, mean_abs_preactivation = hidden_relu_stats(net, X_val)
    return {
        "val_loss": val_result["loss"],
        "val_accuracy": val_result["accuracy"],
        "val_macro_f1": val_result["macro_f1"],
        "active_ratio": active_ratio,
        "dead_unit_ratio": dead_unit_ratio,
        "mean_abs_preactivation": mean_abs_preactivation,
        "parameter_count": mlp_param_count(4, width, 3),
    }

def bootstrap_dense_optimizer_study(
    n_boot=BOOT_N,
    widths=BOOT_WIDTHS,
    optimizers=BOOT_OPTIMIZERS,
    epochs=BOOT_EPOCHS,
):
    X_train, X_val, X_test, y_train, y_val, y_test = make_bootstrap_iris_data()
    rows = []

    for boot_id in range(n_boot):
        boot_seed = SEED + 1000 + boot_id
        # scikit-learn resample의 replace=True가 bootstrap 복원추출이다.
        # stratify=y_train을 사용해 작은 Iris에서 class 하나가 bootstrap sample에서 사라지는 일을 줄인다.
        X_boot, y_boot = resample(
            X_train,
            y_train,
            replace=True,
            n_samples=len(X_train),
            random_state=boot_seed,
            stratify=y_train,
        )

        for width in widths:
            for opt_name in optimizers:
                result = train_width_net_on_bootstrap(
                    X_boot,
                    y_boot,
                    X_val,
                    y_val,
                    width=width,
                    optimizer_name=opt_name,
                    seed=boot_seed + width,
                    epochs=epochs,
                )
                rows.append({
                    "boot_id": boot_id,
                    "width": width,
                    "optimizer": opt_name,
                    "n_train_boot": len(X_boot),
                    "n_val_fixed": len(X_val),
                    "test_used": False,
                    **result,
                })

    return pd.DataFrame(rows)

bootstrap_df = bootstrap_dense_optimizer_study()
display(bootstrap_df.head())
print("V04.5 확인: bootstrap은 train subset 내부에서만 수행했고, test_used는 모두 False다.")
assert not bootstrap_df["test_used"].any()
```

---

```python
# V04.5-B: Bootstrap distribution visualization.
# 중심 그림은 단일 score가 아니라 width/optimizer 조합별 분포다.
fig, axes = plt.subplots(2, 2, figsize=(16, 9))

labels = []
acc_data = []
f1_data = []
active_data = []
dead_data = []
for opt_name in BOOT_OPTIMIZERS:
    for width in BOOT_WIDTHS:
        subset = bootstrap_df[
            (bootstrap_df["optimizer"] == opt_name) &
            (bootstrap_df["width"] == width)
        ]
        labels.append(f"{opt_name}\nH={width}")
        acc_data.append(subset["val_accuracy"].to_numpy())
        f1_data.append(subset["val_macro_f1"].to_numpy())
        active_data.append(subset["active_ratio"].to_numpy())
        dead_data.append(subset["dead_unit_ratio"].to_numpy())

try:
    axes[0, 0].boxplot(acc_data, tick_labels=labels, showmeans=True)
except TypeError:
    axes[0, 0].boxplot(acc_data, labels=labels, showmeans=True)
axes[0, 0].set_title("Bootstrap validation accuracy")
axes[0, 0].set_ylabel("val accuracy")
axes[0, 0].tick_params(axis="x", rotation=45)

try:
    axes[0, 1].boxplot(f1_data, tick_labels=labels, showmeans=True)
except TypeError:
    axes[0, 1].boxplot(f1_data, labels=labels, showmeans=True)
axes[0, 1].set_title("Bootstrap validation macro-F1")
axes[0, 1].set_ylabel("val macro-F1")
axes[0, 1].tick_params(axis="x", rotation=45)

try:
    axes[1, 0].boxplot(active_data, tick_labels=labels, showmeans=True)
except TypeError:
    axes[1, 0].boxplot(active_data, labels=labels, showmeans=True)
axes[1, 0].set_title("Bootstrap ReLU active ratio")
axes[1, 0].set_ylabel("active ratio")
axes[1, 0].tick_params(axis="x", rotation=45)

try:
    axes[1, 1].boxplot(dead_data, tick_labels=labels, showmeans=True)
except TypeError:
    axes[1, 1].boxplot(dead_data, labels=labels, showmeans=True)
axes[1, 1].set_title("Bootstrap dead unit ratio")
axes[1, 1].set_ylabel("dead unit ratio")
axes[1, 1].tick_params(axis="x", rotation=45)

for ax in axes.ravel():
    ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

summary = (
    bootstrap_df
    .groupby(["optimizer", "width", "parameter_count"])
    .agg(
        mean_acc=("val_accuracy", "mean"),
        std_acc=("val_accuracy", "std"),
        mean_f1=("val_macro_f1", "mean"),
        std_f1=("val_macro_f1", "std"),
        mean_active=("active_ratio", "mean"),
        mean_dead=("dead_unit_ratio", "mean"),
    )
    .reset_index()
)

for opt_name, group in summary.groupby("optimizer"):
    axes[0].errorbar(
        group["parameter_count"],
        group["mean_acc"],
        yerr=group["std_acc"],
        marker="o",
        capsize=4,
        label=opt_name,
    )
    axes[1].errorbar(
        group["parameter_count"],
        group["mean_f1"],
        yerr=group["std_f1"],
        marker="o",
        capsize=4,
        label=opt_name,
    )

axes[0].set_title("Parameter count vs bootstrap mean accuracy")
axes[0].set_xlabel("parameter count")
axes[0].set_ylabel("mean val accuracy ± std")
axes[1].set_title("Parameter count vs bootstrap mean macro-F1")
axes[1].set_xlabel("parameter count")
axes[1].set_ylabel("mean val macro-F1 ± std")
for ax in axes:
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

display(summary)
```

해석 질문:

- width가 커질수록 평균 validation accuracy가 올라가는가?
- width가 커질수록 bootstrap 분산이 커지는가?
- SGD와 Adam의 bootstrap 분포는 같은가?
- ReLU active ratio가 너무 낮은 조합은 있는가?
- test set을 쓰지 않았는데도 이 실험에서 말할 수 있는 것과 말할 수 없는 것은 무엇인가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

체크포인트: 좋은 architecture는 단일 점수가 아니라 bootstrap 분포, ReLU activation 상태, validation curve를 함께 보고 판단해야 한다.

---

### V04.5-C. Bootstrap Selection Robustness

분포를 보는 것에서 한 단계 더 들어가면, “어떤 조합이 가장 자주 선택되는가”를 볼 수 있다. 단일 run의 best score가 아니라 bootstrap resample별 rank를 보면 optimizer/width 선택의 안정성을 더 직접적으로 판단할 수 있다.

```python
# V04.5-C: bootstrap selection robustness.
# 단일 평균 score가 아니라 bootstrap마다 어떤 width/optimizer 조합이 1등인지 본다.
rank_df = bootstrap_df.copy()
rank_df["combo"] = rank_df["optimizer"] + " H=" + rank_df["width"].astype(str)
rank_df["rank_by_macro_f1"] = rank_df.groupby("boot_id")["val_macro_f1"].rank(ascending=False, method="min")
rank_df["rank_by_accuracy"] = rank_df.groupby("boot_id")["val_accuracy"].rank(ascending=False, method="min")

selection_frequency = (
    rank_df[rank_df["rank_by_macro_f1"] == 1]
    .groupby(["optimizer", "width", "combo"])
    .size()
    .reset_index(name="best_count_by_macro_f1")
    .sort_values("best_count_by_macro_f1", ascending=False)
)
selection_frequency["best_frequency"] = selection_frequency["best_count_by_macro_f1"] / BOOT_N

percentile_summary = (
    bootstrap_df
    .groupby(["optimizer", "width"])
    .agg(
        acc_p05=("val_accuracy", lambda s: np.percentile(s, 5)),
        acc_p50=("val_accuracy", lambda s: np.percentile(s, 50)),
        acc_p95=("val_accuracy", lambda s: np.percentile(s, 95)),
        f1_p05=("val_macro_f1", lambda s: np.percentile(s, 5)),
        f1_p50=("val_macro_f1", lambda s: np.percentile(s, 50)),
        f1_p95=("val_macro_f1", lambda s: np.percentile(s, 95)),
        active_p50=("active_ratio", lambda s: np.percentile(s, 50)),
        dead_p50=("dead_unit_ratio", lambda s: np.percentile(s, 50)),
    )
    .reset_index()
)
percentile_summary["combo"] = percentile_summary["optimizer"] + " H=" + percentile_summary["width"].astype(str)

display(selection_frequency)
display(percentile_summary)

fig, axes = plt.subplots(1, 2, figsize=(14, 4))
selection_plot = selection_frequency.sort_values("best_frequency")
axes[0].barh(selection_plot["combo"], selection_plot["best_frequency"], color="#4e79a7")
axes[0].set_title("Bootstrap best-frequency by validation macro-F1")
axes[0].set_xlabel("frequency of rank 1")
axes[0].set_xlim(0, 1)

for opt_name, group in percentile_summary.groupby("optimizer"):
    axes[1].errorbar(
        group["width"],
        group["f1_p50"],
        yerr=[group["f1_p50"] - group["f1_p05"], group["f1_p95"] - group["f1_p50"]],
        marker="o",
        capsize=4,
        label=opt_name,
    )
axes[1].set_title("Validation macro-F1 percentile interval")
axes[1].set_xlabel("hidden width")
axes[1].set_ylabel("p50 with p05-p95 interval")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

해석 질문:

- 평균이 높은 조합과 가장 자주 1등인 조합은 같은가?
- p05-p95 interval이 넓은 조합은 어떤 위험을 뜻하는가?
- bootstrap selection이 불안정하면 validation curve 선택을 어떻게 보완해야 하는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

## V05. Week13 Bridge: Iris Optimizer Comparison

Iris는 tabular multiclass optimizer comparison 본체다. 이미지 tensor와 CNN bridge는 V06에서 별도로 다룬다.

V05의 검증 원칙:

```text
train: parameter 학습
validation: epoch별 curve 관찰과 optimizer 비교
test: 학습과 비교가 끝난 뒤 final metric을 딱 한 번 확인
```

Optimizer는 X/y를 보지 않는다. Optimizer는 layer가 들고 있는 param과 grad만 읽고 parameter를 update한다.

---

### V05 metric interpretation note

scikit-learn metric 기준으로 accuracy는 전체 정답 비율을 빠르게 요약하지만, class별 실패 위치를 보여주지는 않는다. macro-F1은 class별 precision/recall 균형을 평균내므로 작은 multiclass dataset에서 class 하나가 무너지는 상황을 더 잘 드러낸다. confusion matrix는 `C[i,j] = true i, pred j` count이므로 어떤 class가 어떤 class로 섞였는지 최종 test에서 확인하는 표다.

Optimizer 선택은 test가 아니라 validation curve와 validation metric으로 끝낸다. test는 선택이 끝난 뒤 final report로 한 번만 열어야 한다.

---

### V05 디벨롭 플랜

- 시각화 목적: 실제 Iris 데이터에서 optimizer 비교를 공정 조건으로 실행하고, train/validation/test 역할을 분리한다.
- 사용할 데이터: sklearn Iris.
- 필요한 전처리: stratified train/validation/test split, train-only StandardScaler, same seed/split/init/epoch/batch size.
- 코드 셀 설계: split audit, optimizer별 train loss, val loss, val accuracy, val macro-F1, final test accuracy/macro-F1, final test confusion matrix.
- 그래프 해석 포인트: validation curve는 실험 비교 중 볼 수 있지만, test는 마지막 최종 평가에만 사용한다.
- 학생이 자주 하는 오해: epoch마다 test accuracy를 보며 optimizer를 고르는 것을 올바른 검증이라고 생각한다.
- 체크포인트 질문: optimizer 비교에서 test set은 언제 열어야 하는가?

---

```python
# Iris optimizer comparison setup audit: same data and fair comparison conditions.
# V05는 train/validation/test 3분할을 사용한다.
iris = load_iris()
X_iris = iris.data.astype(float)
y_iris = iris.target.astype(int)

X_trainval_audit, X_test_audit, y_trainval_audit, y_test_audit = train_test_split(
    X_iris, y_iris, test_size=0.2, random_state=SEED, stratify=y_iris
)
X_train_audit, X_val_audit, y_train_audit, y_val_audit = train_test_split(
    X_trainval_audit, y_trainval_audit, test_size=0.25, random_state=SEED, stratify=y_trainval_audit
)

setup_audit = pd.DataFrame([
    ["seed", SEED, "fixed for split, initialization, and batch order"],
    ["split", f"train={len(y_train_audit)}, val={len(y_val_audit)}, test={len(y_test_audit)}", "stratified by class"],
    ["split method", "stratify=y", "class ratio를 train/val/test에 유지"],
    ["input shape", X_train_audit.shape, "Iris has 4 numeric features"],
    ["output shape", "Dense(3)", "three target classes"],
    ["optimizer variable", "SGD/Momentum/RMSProp/Adam", "only update rule changes"],
    ["test policy", "final only", "not inspected during epoch loop"],
], columns=["condition", "value", "reason"])
display(setup_audit)

ratio_audit = pd.DataFrame({
    "train_count": pd.Series(y_train_audit).value_counts().sort_index(),
    "val_count": pd.Series(y_val_audit).value_counts().sort_index(),
    "test_count": pd.Series(y_test_audit).value_counts().sort_index(),
})
ratio_audit.index = iris.target_names

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
ratio_audit.plot(kind="bar", ax=axes[0], color=["#59a14f", "#f28e2b", "#4e79a7"])
axes[0].set_title("stratified train/val/test class counts")
axes[0].tick_params(axis="x", rotation=20)
axes[0].set_ylabel("count")

axes[1].scatter(X_iris[:, 2], X_iris[:, 3], c=y_iris, cmap="viridis", edgecolor="black")
axes[1].set_title("Iris feature scatter for optimizer task")
axes[1].set_xlabel("petal length")
axes[1].set_ylabel("petal width")
plt.tight_layout()
plt.show()
```

---

```python
def make_iris_data():
    # 1단계: final test를 20%로 먼저 떼어낸다.
    # 이 test set은 epoch loop에서 절대 보지 않는다.
    iris = load_iris()
    X = iris.data.astype(float)
    y = iris.target.astype(int)
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=SEED
    )
    # 2단계: 남은 80%에서 validation 25%를 떼면 전체 기준 60/20/20이 된다.
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.25, stratify=y_trainval, random_state=SEED
    )
    # 3단계: scaler는 train에만 fit한다.
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)
    return X_train, X_val, X_test, y_train, y_val, y_test

def make_base_net():
    # 모든 optimizer가 같은 초기 weight에서 출발하도록 base net을 하나 만든다.
    rng = np.random.default_rng(SEED)
    return Network([Dense(4, 16, rng=rng, scale=0.15), ReLU(), Dense(16, 3, rng=rng, scale=0.15)])

def clone_net_from(base):
    # optimizer별 실험이 같은 initial weights를 갖도록 layer별 parameter를 복사한다.
    copied_layers = []
    for layer in base.layers:
        if isinstance(layer, Dense):
            new = Dense(layer.W.shape[1], layer.W.shape[0], rng=np.random.default_rng(SEED))
            new.W = layer.W.copy()
            new.b = layer.b.copy()
            copied_layers.append(new)
        elif isinstance(layer, ReLU):
            copied_layers.append(ReLU())
    return Network(copied_layers)

def predict(net, X):
    # logits -> softmax probability -> class id.
    return np.argmax(softmax(net.forward(X)), axis=1)

def flatten_params(net):
    # Dense layer의 모든 W,b를 하나의 vector로 펴서 초기화 공정성을 확인한다.
    chunks = []
    for layer in net.layers:
        if isinstance(layer, Dense):
            chunks.append(layer.W.ravel())
            chunks.append(layer.b.ravel())
    return np.concatenate(chunks)

base_for_audit = make_base_net()
base_param_vec = flatten_params(base_for_audit)
print("base init param norm:", np.linalg.norm(base_param_vec))
print("base init param size:", base_param_vec.size)

def eval_loss_and_metrics(net, X, y):
    # validation/test 평가 helper.
    # loss 계산은 forward만 수행하며, parameter update는 하지 않는다.
    loss_fn = SoftmaxCE()
    logits = net.forward(X)
    loss = loss_fn.forward(logits, y)
    y_pred = np.argmax(loss_fn.probs, axis=1)
    return {
        "loss": float(loss),
        "accuracy": accuracy_score(y, y_pred),
        "macro_f1": f1_score(y, y_pred, average="macro"),
        "pred": y_pred,
    }

def train_iris_optimizer(opt_name, optimizer, lr, epochs=90, batch_size=16):
    # data split은 optimizer별로 동일하다.
    X_train, X_val, X_test, y_train, y_val, y_test = make_iris_data()
    base = make_base_net()
    net = clone_net_from(base)
    initial_param_norm = float(np.linalg.norm(flatten_params(net)))
    loss_fn = SoftmaxCE()
    rng = np.random.default_rng(SEED)

    train_losses, val_losses, val_accs, val_f1s = [], [], [], []
    for epoch in range(epochs):
        # batch order도 seed로 고정한다.
        order = rng.permutation(len(X_train))
        epoch_losses = []
        for start in range(0, len(X_train), batch_size):
            idx = order[start:start + batch_size]
            X_batch, y_batch = X_train[idx], y_train[idx]
            logits = net.forward(X_batch)
            loss = loss_fn.forward(logits, y_batch)
            dloss = loss_fn.backward()
            net.backward(dloss)
            optimizer.step(net)
            epoch_losses.append(loss)

        # epoch별로 train loss와 validation metrics만 기록한다.
        train_losses.append(float(np.mean(epoch_losses)))
        val_eval = eval_loss_and_metrics(net, X_val, y_val)
        val_losses.append(val_eval["loss"])
        val_accs.append(val_eval["accuracy"])
        val_f1s.append(val_eval["macro_f1"])

    # test는 학습이 끝난 뒤 final metric으로 한 번만 연다.
    test_eval = eval_loss_and_metrics(net, X_test, y_test)
    best_val_epoch = int(np.argmin(val_losses))
    best_val_loss = float(np.min(val_losses))
    final_val_accuracy = float(val_accs[-1])
    final_val_macro_f1 = float(val_f1s[-1])
    final_test_accuracy = float(test_eval["accuracy"])
    final_test_macro_f1 = float(test_eval["macro_f1"])

    return {
        "optimizer": opt_name,
        "lr": lr,
        "initial_param_norm": initial_param_norm,
        "net": net,
        "train_loss": train_losses,
        "val_loss": val_losses,
        "val_accuracy": val_accs,
        "val_macro_f1": val_f1s,
        "best_val_loss": best_val_loss,
        "best_val_epoch": best_val_epoch,
        "final_val_accuracy": final_val_accuracy,
        "final_val_macro_f1": final_val_macro_f1,
        "final_test_accuracy": final_test_accuracy,
        "final_test_macro_f1": final_test_macro_f1,
        "generalization_gap": final_val_accuracy - final_test_accuracy,
        "final_test_confusion_matrix": confusion_matrix(y_test, test_eval["pred"]),
    }

iris_runs = [
    train_iris_optimizer("SGD", SGD(lr=0.05), lr=0.05),
    train_iris_optimizer("Momentum", Momentum(lr=0.03, beta=0.9), lr=0.03),
    train_iris_optimizer("RMSProp", RMSProp(lr=0.01, beta=0.9), lr=0.01),
    train_iris_optimizer("Adam", Adam(lr=0.01), lr=0.01),
]

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for run in iris_runs:
    axes[0, 0].plot(run["train_loss"], label=run["optimizer"])
    axes[0, 1].plot(run["val_loss"], label=run["optimizer"])
    axes[1, 0].plot(run["val_accuracy"], label=run["optimizer"])
    axes[1, 1].plot(run["val_macro_f1"], label=run["optimizer"])
axes[0, 0].set_title("optimizer별 train loss curve")
axes[0, 1].set_title("optimizer별 val loss curve")
axes[1, 0].set_title("optimizer별 val accuracy curve")
axes[1, 1].set_title("optimizer별 val macro-F1 curve")
for ax in axes.ravel():
    ax.set_xlabel("epoch")
    ax.grid(True, alpha=0.3)
    ax.legend()
plt.tight_layout()
plt.show()

summary_table = pd.DataFrame(
    [
        {
            "optimizer": r["optimizer"],
            "lr": r["lr"],
            "initial_param_norm": r["initial_param_norm"],
            "best_val_loss": r["best_val_loss"],
            "best_val_epoch": r["best_val_epoch"],
            "final_val_accuracy": r["final_val_accuracy"],
            "final_val_macro_f1": r["final_val_macro_f1"],
            "final_test_accuracy": r["final_test_accuracy"],
            "final_test_macro_f1": r["final_test_macro_f1"],
            "generalization_gap": r["generalization_gap"],
        }
        for r in iris_runs
    ]
).sort_values("optimizer")
summary_table["selection_score"] = summary_table["best_val_loss"]
selected_optimizer = summary_table.sort_values("selection_score").iloc[0]["optimizer"]
print("주의: optimizer 선택 기준은 validation curve와 best_val_loss / val_macro_f1이다.")
print("주의: test metric은 선택이 끝난 뒤 보고용 final evaluation이다.")
print("주의: 아래 test column을 보고 optimizer를 다시 고르면 test leakage가 된다.")
print("Selected by validation only:", selected_optimizer)
display(summary_table)

fig, axes = plt.subplots(1, 4, figsize=(14, 3))
for ax, run in zip(axes, iris_runs):
    cm = run["final_test_confusion_matrix"]
    ax.imshow(cm, cmap="Blues")
    ax.set_title(run["optimizer"] + (" (selected by val)" if run["optimizer"] == selected_optimizer else ""))
    ax.set_xlabel("pred")
    ax.set_ylabel("true")
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, cm[i, j], ha="center", va="center")
plt.suptitle("final test confusion matrix: opened once after training")
plt.tight_layout()
plt.show()
```

---

```python
# Optional selected-model report.
# 이미 validation으로 선택된 optimizer 하나만 final test classification_report를 확인한다.
# 이 출력은 optimizer 재선택 기준이 아니라 final error pattern 설명용이다.
selected_run = next(r for r in iris_runs if r["optimizer"] == selected_optimizer)
_, _, X_test_report, _, _, y_test_report = make_iris_data()
y_pred_report = predict(selected_run["net"], X_test_report)
print("classification report for selected optimizer:", selected_optimizer)
print(classification_report(y_test_report, y_pred_report, target_names=iris.target_names, zero_division=0))
```

---

### V05.5. Gradient Flow Audit Lab

이 셀은 “loss가 줄었다”에서 멈추지 않고, 실제로 각 Dense layer에 gradient와 update가 흐르는지 확인한다. 좋은 optimizer 설명은 curve 모양뿐 아니라 `grad_norm`, `update_norm`, `param_norm`, ReLU active/dead ratio까지 연결해야 한다.

```python
# V05.5-A: gradient flow audit.
# 학습 중 layer별 dW/db norm, update norm, ReLU active/dead ratio를 epoch 단위로 추적한다.
def dense_diagnostic_rows(net, X_probe, epoch, train_loss, val_eval, mean_update_norm, mean_grad_norm):
    # X_probe forward를 실행해 각 Dense의 cache를 validation 기준으로 채운다.
    net.forward(X_probe)
    rows = []
    dense_idx = 0
    for layer in net.layers:
        if not isinstance(layer, Dense):
            continue
        Z = layer.X @ layer.W.T + layer.b
        param_norm = float(np.sqrt((layer.W ** 2).sum() + (layer.b ** 2).sum()))
        active_ratio = float((Z > 0).mean())
        dead_unit_ratio = float(((Z <= 0).all(axis=0)).mean())
        rows.append({
            "epoch": epoch,
            "dense_index": dense_idx,
            "train_loss": train_loss,
            "val_loss": val_eval["loss"],
            "val_accuracy": val_eval["accuracy"],
            "val_macro_f1": val_eval["macro_f1"],
            "param_norm": param_norm,
            "mean_grad_norm": mean_grad_norm,
            "mean_update_norm": mean_update_norm,
            "update_to_param_ratio": mean_update_norm / (param_norm + 1e-12),
            "active_ratio": active_ratio,
            "dead_unit_ratio": dead_unit_ratio,
        })
        dense_idx += 1
    return rows

def train_with_gradient_flow_audit(optimizer_name="Adam", width=16, epochs=70, lr=None, init_scale=0.15, use_relu=True, use_scaling=True):
    iris = load_iris()
    X = iris.data.astype(float)
    y = iris.target.astype(int)
    X_trainval, _, y_trainval, _ = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
    X_train, X_val, y_train, y_val = train_test_split(X_trainval, y_trainval, test_size=0.25, stratify=y_trainval, random_state=SEED)
    if use_scaling:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)

    rng = np.random.default_rng(SEED)
    layers = [Dense(4, width, rng=rng, scale=init_scale)]
    if use_relu:
        layers.append(ReLU())
    layers.append(Dense(width, 3, rng=rng, scale=init_scale))
    net = Network(layers)

    if optimizer_name == "SGD":
        optimizer = SGD(lr=0.05 if lr is None else lr)
    elif optimizer_name == "Adam":
        optimizer = Adam(lr=0.01 if lr is None else lr)
    else:
        raise ValueError(optimizer_name)

    loss_fn = SoftmaxCE()
    rng = np.random.default_rng(SEED)
    rows = []
    for epoch in range(epochs):
        order = rng.permutation(len(X_train))
        batch_losses = []
        batch_update_norms = []
        batch_grad_norms = []
        for start in range(0, len(X_train), 16):
            idx = order[start:start + 16]
            before = flatten_params(net).copy()
            logits = net.forward(X_train[idx])
            loss = loss_fn.forward(logits, y_train[idx])
            net.backward(loss_fn.backward())

            dense_grad_norms = []
            for layer in net.layers:
                if isinstance(layer, Dense):
                    dense_grad_norms.append(float(np.sqrt((layer.dW ** 2).sum() + (layer.db ** 2).sum())))
            optimizer.step(net)
            after = flatten_params(net).copy()
            batch_losses.append(float(loss))
            batch_grad_norms.append(float(np.mean(dense_grad_norms)))
            batch_update_norms.append(float(np.linalg.norm(after - before)))

        val_eval = eval_loss_and_metrics(net, X_val, y_val)
        rows.extend(dense_diagnostic_rows(
            net,
            X_val,
            epoch=epoch,
            train_loss=float(np.mean(batch_losses)),
            val_eval=val_eval,
            mean_update_norm=float(np.mean(batch_update_norms)),
            mean_grad_norm=float(np.mean(batch_grad_norms)),
        ))
    return net, pd.DataFrame(rows)

grad_audit_net, grad_flow_df = train_with_gradient_flow_audit(optimizer_name="Adam", width=16, epochs=70)
display(grad_flow_df.head())

fig, axes = plt.subplots(2, 3, figsize=(16, 8))
loss_view = grad_flow_df.groupby("epoch").agg(train_loss=("train_loss", "mean"), val_loss=("val_loss", "mean"), val_macro_f1=("val_macro_f1", "mean")).reset_index()
axes[0, 0].plot(loss_view["epoch"], loss_view["train_loss"], label="train loss")
axes[0, 0].plot(loss_view["epoch"], loss_view["val_loss"], label="val loss")
axes[0, 0].set_title("loss curve")
axes[0, 0].legend()

axes[0, 1].plot(loss_view["epoch"], loss_view["val_macro_f1"], color="#59a14f")
axes[0, 1].set_title("validation macro-F1")

for dense_idx, group in grad_flow_df.groupby("dense_index"):
    axes[0, 2].plot(group["epoch"], group["mean_grad_norm"], label=f"Dense {dense_idx}")
    axes[1, 0].plot(group["epoch"], group["update_to_param_ratio"], label=f"Dense {dense_idx}")
    axes[1, 1].plot(group["epoch"], group["active_ratio"], label=f"Dense {dense_idx}")
    axes[1, 2].plot(group["epoch"], group["dead_unit_ratio"], label=f"Dense {dense_idx}")

axes[0, 2].set_title("mean gradient norm")
axes[1, 0].set_title("update / parameter norm")
axes[1, 1].set_title("pre-activation positive ratio")
axes[1, 2].set_title("dead unit ratio")
for ax in axes.ravel():
    ax.set_xlabel("epoch")
    ax.grid(True, alpha=0.3)
    ax.legend()
plt.tight_layout()
plt.show()
```

해석 질문:

- loss가 줄어도 특정 Dense layer의 `mean_grad_norm`이 거의 0이면 무엇을 의심해야 하는가?
- `update_to_param_ratio`가 갑자기 커지는 구간은 learning rate와 어떻게 연결되는가?
- ReLU active ratio와 dead unit ratio가 validation macro-F1 해석에 어떤 보조 근거가 되는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

### V05.6. Ablation Lab

Ablation은 “무엇이 성능을 만들었는가”를 확인하는 실험이다. 여기서는 optimizer만 보지 않고 scaling, ReLU, width, initialization, learning rate를 하나씩 흔들어 failure mode를 관찰한다.

```python
# V05.6: ablation lab.
# test set은 사용하지 않고 fixed validation set에서만 비교한다.
ablation_configs = [
    {"name": "baseline_adam_H16", "optimizer": "Adam", "width": 16, "use_relu": True, "use_scaling": True, "init_scale": 0.15, "lr": 0.01},
    {"name": "no_scaling", "optimizer": "Adam", "width": 16, "use_relu": True, "use_scaling": False, "init_scale": 0.15, "lr": 0.01},
    {"name": "no_relu", "optimizer": "Adam", "width": 16, "use_relu": False, "use_scaling": True, "init_scale": 0.15, "lr": 0.01},
    {"name": "narrow_H2", "optimizer": "Adam", "width": 2, "use_relu": True, "use_scaling": True, "init_scale": 0.15, "lr": 0.01},
    {"name": "wide_H128", "optimizer": "Adam", "width": 128, "use_relu": True, "use_scaling": True, "init_scale": 0.15, "lr": 0.01},
    {"name": "tiny_init", "optimizer": "Adam", "width": 16, "use_relu": True, "use_scaling": True, "init_scale": 0.005, "lr": 0.01},
    {"name": "large_init", "optimizer": "Adam", "width": 16, "use_relu": True, "use_scaling": True, "init_scale": 1.5, "lr": 0.01},
    {"name": "sgd_high_lr", "optimizer": "SGD", "width": 16, "use_relu": True, "use_scaling": True, "init_scale": 0.15, "lr": 0.4},
]

ablation_rows = []
ablation_curves = []
for cfg in ablation_configs:
    _, cfg_flow = train_with_gradient_flow_audit(
        optimizer_name=cfg["optimizer"],
        width=cfg["width"],
        epochs=45,
        lr=cfg["lr"],
        init_scale=cfg["init_scale"],
        use_relu=cfg["use_relu"],
        use_scaling=cfg["use_scaling"],
    )
    final = cfg_flow.groupby("epoch").tail(1).groupby("epoch").mean(numeric_only=True).tail(1).iloc[0]
    ablation_rows.append({
        **cfg,
        "final_val_loss": final["val_loss"],
        "final_val_accuracy": final["val_accuracy"],
        "final_val_macro_f1": final["val_macro_f1"],
        "final_update_to_param_ratio": final["update_to_param_ratio"],
        "final_active_ratio": final["active_ratio"],
        "final_dead_unit_ratio": final["dead_unit_ratio"],
        "test_used": False,
    })
    curve = cfg_flow.groupby("epoch").agg(val_loss=("val_loss", "mean"), val_macro_f1=("val_macro_f1", "mean"), update_to_param_ratio=("update_to_param_ratio", "mean")).reset_index()
    curve["name"] = cfg["name"]
    ablation_curves.append(curve)

ablation_df = pd.DataFrame(ablation_rows).sort_values("final_val_macro_f1", ascending=False)
ablation_curve_df = pd.concat(ablation_curves, ignore_index=True)
display(ablation_df)
assert not ablation_df["test_used"].any()

fig, axes = plt.subplots(1, 3, figsize=(16, 4))
plot_df = ablation_df.sort_values("final_val_macro_f1")
axes[0].barh(plot_df["name"], plot_df["final_val_macro_f1"], color="#59a14f")
axes[0].set_title("ablation final validation macro-F1")
axes[0].set_xlabel("macro-F1")

axes[1].barh(plot_df["name"], plot_df["final_update_to_param_ratio"], color="#f28e2b")
axes[1].set_title("final update / parameter ratio")
axes[1].set_xlabel("ratio")

axes[2].barh(plot_df["name"], plot_df["final_dead_unit_ratio"], color="#e15759")
axes[2].set_title("final dead unit ratio")
axes[2].set_xlabel("dead unit ratio")
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 4))
for name, group in ablation_curve_df.groupby("name"):
    axes[0].plot(group["epoch"], group["val_macro_f1"], label=name)
    axes[1].plot(group["epoch"], group["update_to_param_ratio"], label=name)
axes[0].set_title("ablation validation macro-F1 curves")
axes[1].set_title("ablation update/parameter ratio curves")
for ax in axes:
    ax.set_xlabel("epoch")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7)
plt.tight_layout()
plt.show()
```

해석 질문:

- 성능 차이는 optimizer 하나 때문인가, scaling/width/ReLU/init/lr이 함께 만든 결과인가?
- `sgd_high_lr`의 update ratio가 크면 어떤 curve 증상이 동반되는가?
- `no_relu`가 나쁘지 않게 보이더라도 XOR 같은 비선형 문제에서는 왜 한계가 생기는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

### V05-advanced. PCA decision-space audit for selected optimizer

이 셀은 Iris 4D feature space를 PCA 2D/3D로 낮춰 보고, validation으로 선택된 optimizer의 final test prediction이 어디서 맞고 틀리는지 확인한다. PCA는 train-scaled data에만 fit하고 val/test는 transform만 한다.

```python
# V05-advanced: selected optimizer PCA decision-space audit.
# PCA는 train data에만 fit한다. val/test는 transform만 하므로
# V01의 split-before-fit 원칙을 visualization에도 그대로 적용한다.
X_train_pca, X_val_pca, X_test_pca, y_train_pca, y_val_pca, y_test_pca = make_iris_data()
pca_audit = PCA(n_components=3, random_state=SEED)
train_coords = pca_audit.fit_transform(X_train_pca)
val_coords = pca_audit.transform(X_val_pca)
test_coords = pca_audit.transform(X_test_pca)

selected_run = next(r for r in iris_runs if r["optimizer"] == selected_optimizer)
y_test_pred_pca = predict(selected_run["net"], X_test_pca)
test_correct = y_test_pred_pca == y_test_pca

fig = plt.figure(figsize=(14, 9))
ax_2d = fig.add_subplot(2, 2, 1)
for cls in np.unique(y_train_pca):
    mask = y_train_pca == cls
    ax_2d.scatter(train_coords[mask, 0], train_coords[mask, 1], alpha=0.45, label=f"train {iris.target_names[cls]}")
ax_2d.scatter(test_coords[test_correct, 0], test_coords[test_correct, 1], c="black", marker="o", s=80, label="test correct")
ax_2d.scatter(test_coords[~test_correct, 0], test_coords[~test_correct, 1], c="red", marker="x", s=120, label="test wrong")
ax_2d.set_title("PCA decision-space: PC1-PC2 평면도")
ax_2d.set_xlabel("PC1")
ax_2d.set_ylabel("PC2")
ax_2d.grid(True, alpha=0.3)
ax_2d.legend(fontsize=8)

ax_3d = fig.add_subplot(2, 2, 2, projection="3d")
ax_3d.scatter(train_coords[:, 0], train_coords[:, 1], train_coords[:, 2], c=y_train_pca, cmap="viridis", alpha=0.35, s=25)
ax_3d.scatter(test_coords[test_correct, 0], test_coords[test_correct, 1], test_coords[test_correct, 2], c="black", marker="o", s=60)
ax_3d.scatter(test_coords[~test_correct, 0], test_coords[~test_correct, 1], test_coords[~test_correct, 2], c="red", marker="x", s=90)
ax_3d.set_title("PCA decision-space: 3D projection")
ax_3d.set_xlabel("PC1")
ax_3d.set_ylabel("PC2")
ax_3d.set_zlabel("PC3")

ax_var = fig.add_subplot(2, 2, 3)
ax_var.bar(["PC1", "PC2", "PC3"], pca_audit.explained_variance_ratio_, color=["#4e79a7", "#f28e2b", "#59a14f"])
ax_var.set_title("PCA fit on train only: explained variance")
ax_var.set_ylim(0, 1)
ax_var.grid(True, axis="y", alpha=0.3)

ax_summary = fig.add_subplot(2, 2, 4)
ax_summary.axis("off")
audit_table = pd.DataFrame(
    [
        ["selected optimizer", selected_optimizer],
        ["test correct", int(test_correct.sum())],
        ["test wrong", int((~test_correct).sum())],
        ["PCA fit data", "train only"],
        ["val/test PCA rule", "transform only"],
    ],
    columns=["item", "value"],
)
display(audit_table)
table = ax_summary.table(cellText=audit_table.to_numpy(), colLabels=audit_table.columns, loc="center")
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.4)
ax_summary.set_title("validation-selected final test audit")
plt.tight_layout()
plt.show()
```

그래프 해석 질문:

- PCA 공간에서 test wrong point가 class 경계가 겹치는 영역에 놓이는가?
- PCA 3D view가 PC1-PC2 평면도보다 더 설명해주는 부분은 무엇인가?
- 이 PCA audit이 optimizer 선택 기준이 아니라 final error explanation인 이유는 무엇인가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

그래프 해석 질문:

- 어떤 optimizer가 어느 구간에서 빠르게 train loss를 낮췄는가?
- val loss와 val accuracy/macro-F1이 같은 결론을 주는가?
- test set을 epoch마다 보지 않고 final에만 여는 이유는 무엇인가?
- Iris가 쉬운 데이터라 final test accuracy 차이가 작을 수 있는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

## V06. Image Tensor / CNN Bridge

### V06 디벨롭 플랜

- 시각화 목적: 이미지 데이터가 `(N,H,W)` tensor에서 `(N,H*W)` flatten vector로 바뀔 때 잃는 정보를 보고, Week15 CNN으로 넘어갈 이유를 만든다.
- 사용할 데이터: Fashion-MNIST local cache, 실패 시 `sklearn_digits` fallback.
- 필요한 전처리: pixel scale 확인, label mapping 확인, flatten shape 계산.
- 코드 셀 설계: sample grid, label distribution, original/flatten shape diagram, pixel intensity histogram, CNN bridge diagram, Dense MLP vs CNN 비교표.
- 그래프 해석 포인트: optimizer는 Dense MLP와 CNN 모두에 쓰이지만, layer 구조가 보존/손실하는 정보는 다르다.
- 학생이 자주 하는 오해: flatten이 단순 reshape라서 정보 손실이 없다고 생각하거나, CNN이 optimizer를 대체한다고 생각한다.
- 체크포인트 질문: `28x28` 이미지를 flatten하면 어떤 구조 정보가 사라지는가?

---

### Web-grounded image dataset note

Fashion-MNIST는 28x28 grayscale image의 10-class classification dataset이다. 로컬 IDX gzip cache가 있으면 이를 사용한다. cache가 없으면 외부 다운로드를 하지 않고, scikit-learn의 `load_digits`를 fallback으로 사용한다. digits fallback은 8x8 image이고 pixel range가 0..16이므로 `/16.0`으로 scaling한다. Fashion-MNIST는 pixel range 0..255이므로 `/255.0`으로 scaling한다.

---

```python
# V06 Image Tensor / CNN Bridge.
# V05는 Iris optimizer comparison만 담당하고, 이미지 bridge는 여기서만 다룬다.
image_bundle = get_dataset("keras_fashion_mnist", inventory)
images = image_bundle["images"]
labels = image_bundle["labels"]
class_names = image_bundle["class_names"]

# Dense MLP는 이미지를 1D vector로 펼쳐 입력한다.
# dataset별 pixel range를 먼저 정규화한다.
scaled_images, scale_note = scale_image_pixels(images, image_bundle["name"])
flat_scaled = scaled_images.reshape(len(scaled_images), -1)
assert flat_scaled.ndim == 2
assert flat_scaled.shape[0] == len(labels)
assert np.nanmin(flat_scaled) >= 0.0
assert np.nanmax(flat_scaled) <= 1.0 + 1e-8

shape_bridge = pd.DataFrame([
    ["original image tensor", images.shape, "N samples with 2D spatial grid"],
    ["one image", images[0].shape, "height x width local neighborhoods remain visible"],
    ["flattened batch", flat_scaled.shape, "Dense MLP input vector; neighborhood relation no longer explicit"],
], columns=["stage", "shape", "meaning"])
print("dataset:", image_bundle["name"])
print("source:", image_bundle["source"])
print(scale_note)
print("class mapping:", dict(enumerate(class_names)))
display(shape_bridge)

# sample grid는 class별 이미지 형태가 어떻게 다른지 보여준다.
n = min(12, len(images))
fig, axes = plt.subplots(3, 4, figsize=(8, 6))
for ax, img, lab in zip(axes.ravel(), images[:n], labels[:n]):
    ax.imshow(img, cmap="gray")
    ax.set_title(class_names[int(lab)])
    ax.axis("off")
plt.suptitle("sample image grid")
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
label_counts = pd.Series(labels).value_counts().sort_index()
axes[0].bar([class_names[int(i)] for i in label_counts.index], label_counts.values, color="#4e79a7")
axes[0].set_title("label distribution")
axes[0].tick_params(axis="x", rotation=45)
axes[0].set_ylabel("count")

# pixel histogram은 scaling 필요성을 보여준다.
axes[1].hist(images.ravel(), bins=30, color="#59a14f", edgecolor="white")
axes[1].set_title("pixel intensity histogram")
axes[1].set_xlabel("pixel value")
axes[1].set_ylabel("frequency")

# Flatten MLP는 H,W 이웃 관계를 명시적으로 보존하지 않는다.
stages = ["image\n(H,W)", "flatten\n(H*W)", "Dense\nclassifier", "class\nprobabilities"]
xs = np.arange(len(stages))
axes[2].scatter(xs, np.zeros_like(xs), s=1400, color="#dceefb", edgecolor="#1f77b4")
for i, label in enumerate(stages):
    axes[2].text(i, 0, label, ha="center", va="center", fontsize=9)
    if i < len(stages) - 1:
        axes[2].annotate("", xy=(i + 0.68, 0), xytext=(i + 0.32, 0), arrowprops=dict(arrowstyle="->", lw=2))
axes[2].set_title("Flatten MLP shape diagram")
axes[2].set_axis_off()
plt.tight_layout()
plt.show()

# CNN은 local receptive field를 가진 filter/kernel이 sliding하며 feature map을 만든다.
fig, ax = plt.subplots(figsize=(10, 2.8))
stages = ["image\n(N,H,W,C)", "conv\nfeature maps", "pooling", "flatten", "dense\nclassifier"]
xs = np.arange(len(stages))
ax.scatter(xs, np.zeros_like(xs), s=1700, color="#f1ce63", edgecolor="#8f6d00")
for i, label in enumerate(stages):
    ax.text(i, 0, label, ha="center", va="center", fontsize=9)
    if i < len(stages) - 1:
        ax.annotate("", xy=(i + 0.7, 0), xytext=(i + 0.3, 0), arrowprops=dict(arrowstyle="->", lw=2))
ax.set_title("CNN bridge: local pattern -> pooled feature -> classifier")
ax.set_axis_off()
plt.show()

cnn_compare = pd.DataFrame([
    ["Dense MLP", "(N,H,W) -> (N,H*W)", "local adjacency not explicit", "Dense W,b updated by optimizer"],
    ["CNN", "(N,H,W,C) -> feature maps", "local receptive field preserved", "Conv kernels + Dense W,b updated by optimizer"],
], columns=["model family", "shape flow", "image-structure handling", "optimizer relationship"])
display(cnn_compare)
```

---

### V06-advanced. Flattened image PCA and local structure bridge

이 셀은 image tensor를 flatten한 뒤 PCA 2D/3D projection으로 보고, CNN이 왜 local patch/receptive field를 쓰는지 연결한다. Fashion-MNIST cache가 있으면 Fashion-MNIST를, 없으면 `sklearn_digits` fallback을 그대로 사용한다.

```python
# V06-advanced: flattened image PCA and CNN bridge.
# flat_scaled는 위 셀에서 shape/range assert를 이미 통과했다.
# PCA는 high-dimensional image vector를 보기 위한 projection이며,
# CNN의 convolution kernel처럼 local pattern을 직접 학습하는 구조는 아니다.
if adv_vis is not None:
    image_pca_bundle = {
        "name": image_bundle["name"],
        "images": images,
        "scaled_images": scaled_images,
        "flat_scaled": flat_scaled,
        "labels": labels,
        "class_names": class_names,
    }
    fig, image_pca_shape_table = adv_vis.plot_image_pca_and_patch_bridge(image_pca_bundle)
    display(image_pca_shape_table)
else:
    raise RuntimeError("Advanced visualization pack is not loaded. Run the extension loader cell before V06-advanced.")
```

그래프 해석 질문:

- flattened image PCA에서 class가 겹치는 이유는 무엇인가?
- PC1-PC2 평면도와 3D projection은 image variation을 어떻게 다르게 보여주는가?
- PCA projection과 CNN convolution kernel은 각각 어떤 기준으로 정보를 요약하는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

---

V06 그래프 해석 질문:

- sample grid에서 같은 class 안에서도 모양이 달라지는 이유는 무엇인가?
- label distribution이 크게 치우쳐 있으면 accuracy 해석은 어떻게 달라지는가?
- flatten 전후 전체 pixel 수는 보존된다. 그럼 무엇을 잃는가?
- CNN의 convolution/pooling은 optimizer를 대체하는가, 아니면 optimizer가 update할 parameter 구조를 다르게 만드는가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

체크포인트: Flatten MLP와 CNN의 구조 차이를 이미지 tensor의 shape 관점에서 설명할 수 있다.

기본 실행에서 제외하는 데이터:

| dataset_id | 처리 |
|---|---|
| boston_housing_cmu_legacy | appendix note only |
| uci_appliances_energy_prediction | appendix note only |
| keras_mnist_or_openml_mnist | uncached/download path 제외 |
| daisy_image_missing_local_file | local file missing 가능성이 있어 제외 |

---

## V07. Proper MLP Representation Bridge, no Attention

이 섹션은 Attention이나 Transformer로 넘어가지 않는다. Week13 범위 안에서 “진짜 신경망”으로 확장할 때 필요한 최소 bridge는 Dense+ReLU block을 여러 번 쌓는 MLP다.

핵심 block:

\[
Block(X) = ReLU(Dense(X))
\]

MLP는 이 block을 반복해 representation을 바꾼다.

```text
X
-> Dense(Din, H1) -> ReLU
-> Dense(H1, H2) -> ReLU
-> Dense(H2, K)
-> SoftmaxCE
```

각 Dense는 좌표계와 차원을 바꾸고, ReLU는 piecewise-linear gate를 추가한다. Optimizer는 모든 Dense layer의 `W,b,dW,db`를 순회하며 update한다. 따라서 깊은 MLP도 핵심 loop는 그대로다.

```text
X_batch -> net.forward -> loss_fn.forward -> loss_fn.backward -> net.backward -> optimizer.step(net)
```

---

### V07 디벨롭 플랜

- 시각화 목적: Dense+ReLU block을 여러 번 쌓으면 layer별 representation shape와 activation sparsity가 어떻게 달라지는지 본다.
- 사용할 데이터: Iris train/validation split.
- 필요한 전처리: V04.5의 train-only scaled Iris helper 재사용.
- 코드 셀 설계: 학습 전/후 layer output table, ReLU active ratio table, train/val curve, layer별 PCA projection.
- 그래프 해석 포인트: hidden representation은 층마다 바뀌며, optimizer는 그 representation이 loss에 맞게 바뀌도록 Dense parameter를 update한다.
- 학생이 자주 하는 오해: layer를 깊게 쌓는 것을 단순히 “뉴런 수 추가”로 보거나, ReLU가 parameter를 가진다고 생각한다.
- 체크포인트 질문: 깊은 MLP에서도 optimizer가 직접 보는 object는 무엇인가?

---

```python
# V07-A: deeper MLP representation collection.
# Attention/Transformer로 가지 않고 Dense+ReLU block 반복만 본다.
def forward_collect_representations(net, X):
    reps = []
    out = X
    for i, layer in enumerate(net.layers):
        out = layer.forward(out)
        reps.append({
            "layer_index": i,
            "layer_type": type(layer).__name__,
            "output": out.copy(),
            "shape": out.shape,
            "positive_ratio": float((out > 0).mean()) if out.ndim == 2 else np.nan,
            "mean_abs_output": float(np.abs(out).mean()) if out.ndim == 2 else np.nan,
        })
    return reps

def make_deeper_mlp(widths=(16, 16), seed=SEED):
    # 여러 Dense+ReLU block을 쌓아도 마지막은 class logit K=3을 만든다.
    rng = np.random.default_rng(seed)
    layers = []
    in_dim = 4
    for width in widths:
        layers.append(Dense(in_dim, width, rng=rng, scale=0.15))
        layers.append(ReLU())
        in_dim = width
    layers.append(Dense(in_dim, 3, rng=rng, scale=0.15))
    return Network(layers)

def train_deeper_mlp(net, X_train, y_train, X_val, y_val, epochs=60, batch_size=16):
    # 이 학습은 V07 representation bridge용이다.
    # optimizer 책임은 동일하다: X/y가 아니라 Dense W,b,dW,db만 update한다.
    optimizer = Adam(lr=0.01)
    loss_fn = SoftmaxCE()
    rng = np.random.default_rng(SEED)
    rows = []
    for epoch in range(epochs):
        order = rng.permutation(len(X_train))
        batch_losses = []
        for start in range(0, len(X_train), batch_size):
            idx = order[start:start + batch_size]
            logits = net.forward(X_train[idx])
            batch_losses.append(loss_fn.forward(logits, y_train[idx]))
            net.backward(loss_fn.backward())
            optimizer.step(net)
        val_eval = evaluate_net(net, X_val, y_val)
        rows.append({
            "epoch": epoch,
            "train_loss": float(np.mean(batch_losses)),
            "val_loss": val_eval["loss"],
            "val_accuracy": val_eval["accuracy"],
            "val_macro_f1": val_eval["macro_f1"],
        })
    return pd.DataFrame(rows)

X_deep_train, X_deep_val, _, y_deep_train, y_deep_val, _ = make_bootstrap_iris_data()
deep_mlp = make_deeper_mlp(widths=(16, 16), seed=SEED)

deep_reps_before = forward_collect_representations(deep_mlp, X_deep_val)
deep_history = train_deeper_mlp(deep_mlp, X_deep_train, y_deep_train, X_deep_val, y_deep_val)
deep_reps_after = forward_collect_representations(deep_mlp, X_deep_val)

def reps_to_table(reps, stage):
    return pd.DataFrame([
        {
            "stage": stage,
            "layer_index": r["layer_index"],
            "layer_type": r["layer_type"],
            "output_shape": r["shape"],
            "positive_ratio": r["positive_ratio"],
            "mean_abs_output": r["mean_abs_output"],
        }
        for r in reps
    ])

deep_rep_table = pd.concat([
    reps_to_table(deep_reps_before, "before training"),
    reps_to_table(deep_reps_after, "after training"),
], ignore_index=True)
display(deep_rep_table)
display(deep_history.tail())
```

---

```python
# V07-B: training curve and layer-wise representation PCA.
# PCA는 layer output을 보기 위한 projection이다. decision boundary 자체가 아니다.
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].plot(deep_history["epoch"], deep_history["train_loss"], label="train loss")
axes[0].plot(deep_history["epoch"], deep_history["val_loss"], label="val loss")
axes[0].set_title("Deeper MLP loss curve")
axes[0].set_xlabel("epoch")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(deep_history["epoch"], deep_history["val_accuracy"], label="val accuracy")
axes[1].plot(deep_history["epoch"], deep_history["val_macro_f1"], label="val macro-F1")
axes[1].set_title("Deeper MLP validation metrics")
axes[1].set_xlabel("epoch")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

relu_rows = deep_rep_table[deep_rep_table["layer_type"] == "ReLU"].copy()
for stage, group in relu_rows.groupby("stage"):
    axes[2].plot(group["layer_index"], group["positive_ratio"], marker="o", label=stage)
axes[2].set_title("ReLU active ratio by layer")
axes[2].set_xlabel("layer index")
axes[2].set_ylabel("positive ratio")
axes[2].legend()
axes[2].grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

plot_reps = deep_reps_before + deep_reps_after
plot_stages = ["before"] * len(deep_reps_before) + ["after"] * len(deep_reps_after)
fig, axes = plt.subplots(2, len(deep_reps_before), figsize=(4 * len(deep_reps_before), 7))

for row, (stage_name, reps) in enumerate([("before training", deep_reps_before), ("after training", deep_reps_after)]):
    for col, rep in enumerate(reps):
        ax = axes[row, col]
        out = rep["output"]
        if out.ndim == 2 and out.shape[1] >= 2:
            coords = PCA(n_components=2, random_state=SEED).fit_transform(out)
            ax.scatter(coords[:, 0], coords[:, 1], c=y_deep_val, cmap="viridis", edgecolor="black", s=45)
            ax.set_title(f"{stage_name}\nL{rep['layer_index']} {rep['layer_type']} {out.shape}")
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            ax.axis("off")
            ax.set_title(f"{stage_name}\nL{rep['layer_index']} {rep['layer_type']}\nnot PCA-compatible")
plt.tight_layout()
plt.show()
```

---

```python
# V07-C: representation quality metrics.
# scikit-learn silhouette_score는 sample의 intra-cluster distance와 nearest-cluster distance 기반 보조 지표다.
# 여기서는 label을 "진짜 군집"이라고 가정해 layer representation의 class separation을 진단한다.
def representation_quality_metrics(reps, y, stage):
    rows = []
    y = np.asarray(y)
    labels = np.unique(y)
    for rep in reps:
        out = rep["output"]
        if out.ndim != 2 or out.shape[1] < 2:
            continue
        centroids = np.vstack([out[y == label].mean(axis=0) for label in labels])
        overall = out.mean(axis=0)
        between = float(np.mean(np.sum((centroids - overall) ** 2, axis=1)))
        within_parts = []
        for centroid, label in zip(centroids, labels):
            group = out[y == label]
            within_parts.append(np.mean(np.sum((group - centroid) ** 2, axis=1)))
        within = float(np.mean(within_parts))
        try:
            sil = float(silhouette_score(out, y))
        except Exception:
            sil = np.nan
        rows.append({
            "stage": stage,
            "layer_index": rep["layer_index"],
            "layer_type": rep["layer_type"],
            "output_dim": out.shape[1],
            "between_centroid_var": between,
            "within_class_var": within,
            "between_within_ratio": between / (within + 1e-12),
            "silhouette_score": sil,
            "positive_ratio": float((out > 0).mean()),
        })
    return pd.DataFrame(rows)

representation_quality_df = pd.concat([
    representation_quality_metrics(deep_reps_before, y_deep_val, "before training"),
    representation_quality_metrics(deep_reps_after, y_deep_val, "after training"),
], ignore_index=True)
display(representation_quality_df)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for stage, group in representation_quality_df.groupby("stage"):
    axes[0].plot(group["layer_index"], group["between_within_ratio"], marker="o", label=stage)
    axes[1].plot(group["layer_index"], group["silhouette_score"], marker="o", label=stage)
    axes[2].plot(group["layer_index"], group["positive_ratio"], marker="o", label=stage)
axes[0].set_title("between/within class separation")
axes[1].set_title("silhouette score by layer")
axes[2].set_title("positive activation ratio by layer")
for ax in axes:
    ax.set_xlabel("layer index")
    ax.grid(True, alpha=0.3)
    ax.legend()
plt.tight_layout()
plt.show()
```

해석 질문:

- layer가 깊어질수록 representation shape는 어떻게 바뀌는가?
- ReLU layer 이후 active ratio는 학습 전/후 어떻게 달라지는가?
- PCA projection에서 class separation은 layer마다 달라지는가?
- between/within ratio와 silhouette score는 PCA 그림의 인상을 지지하는가, 반박하는가?
- 깊은 MLP에서도 optimizer가 직접 update하는 것은 `X/y`인가, `W,b`인가?

답안 scaffold:

```text
관찰:
원인:
제한:
결론:
```

체크포인트: 신경망은 Dense+ReLU block을 반복해 representation을 바꾸고, optimizer가 그 transformation을 loss에 맞게 조정한다.

---

## V08. Failure Gallery and Diagnostic Answer Lab

깊은 시각화의 목적은 failure symptom을 보고 원인 후보를 좁히는 것이다. 이 섹션은 앞에서 만든 gradient flow, ablation, bootstrap, representation quality 결과를 한 표로 모아 “그래프를 답안 문장으로 바꾸는” 진단 카드로 만든다.

```python
# V08: failure gallery.
# 앞선 deep diagnostics에서 evidence를 가져와 failure symptom -> cause -> action -> answer sentence로 압축한다.
baseline_row = ablation_df[ablation_df["name"] == "baseline_adam_H16"].iloc[0]
no_scaling_row = ablation_df[ablation_df["name"] == "no_scaling"].iloc[0]
no_relu_row = ablation_df[ablation_df["name"] == "no_relu"].iloc[0]
high_lr_row = ablation_df[ablation_df["name"] == "sgd_high_lr"].iloc[0]
worst_dead_row = ablation_df.sort_values("final_dead_unit_ratio", ascending=False).iloc[0]

grad_tail = grad_flow_df.groupby("dense_index").tail(1)
lowest_grad_layer = grad_tail.sort_values("mean_grad_norm").iloc[0]
most_unstable_boot = percentile_summary.assign(
    f1_interval=lambda d: d["f1_p95"] - d["f1_p05"]
).sort_values("f1_interval", ascending=False).iloc[0]
best_freq_row = selection_frequency.sort_values("best_frequency", ascending=False).iloc[0]

rep_after = representation_quality_df[representation_quality_df["stage"] == "after training"]
best_rep = rep_after.sort_values("between_within_ratio", ascending=False).iloc[0]

failure_gallery = pd.DataFrame([
    {
        "symptom": "validation macro-F1가 baseline보다 낮음",
        "evidence": f"no_scaling={no_scaling_row['final_val_macro_f1']:.3f}, baseline={baseline_row['final_val_macro_f1']:.3f}",
        "likely_cause": "feature scale이 gradient geometry와 step size를 왜곡",
        "confirm_with": "Ablation Lab: no_scaling row, update/parameter ratio",
        "action": "split 이후 train-only StandardScaler 적용",
        "answer_sentence": "Scaling은 값 모양을 예쁘게 만드는 작업이 아니라 optimizer가 보는 loss geometry를 안정화하는 전처리다.",
    },
    {
        "symptom": "비선형 representation이 약함",
        "evidence": f"no_relu macro-F1={no_relu_row['final_val_macro_f1']:.3f}",
        "likely_cause": "Dense-Dense만 쌓으면 전체가 선형 변환으로 축약될 수 있음",
        "confirm_with": "Ablation Lab: no_relu vs baseline, V02 XOR view",
        "action": "Dense 사이에 ReLU 같은 nonlinearity 사용",
        "answer_sentence": "ReLU는 단순 장식 activation이 아니라 feature space를 piecewise-linear하게 바꾸는 gate다.",
    },
    {
        "symptom": "update가 parameter 크기에 비해 과도함",
        "evidence": f"sgd_high_lr update/param={high_lr_row['final_update_to_param_ratio']:.3g}",
        "likely_cause": "learning rate가 커서 minimum 근처를 지나치거나 진동",
        "confirm_with": "Gradient Flow Audit: update_to_param_ratio curve",
        "action": "lr 낮추기, low/base/high sensitivity 재확인",
        "answer_sentence": "Gradient 방향이 맞아도 learning rate가 크면 update step이 과해 validation curve가 흔들릴 수 있다.",
    },
    {
        "symptom": "일부 ReLU unit이 거의 항상 inactive",
        "evidence": f"{worst_dead_row['name']} dead_ratio={worst_dead_row['final_dead_unit_ratio']:.3f}",
        "likely_cause": "초기화, width, data distribution이 ReLU gate를 죽임",
        "confirm_with": "V03.5 active/dead ratio, V05.5 dead unit ratio",
        "action": "init scale/lr/width 조정, LeakyReLU는 본문 밖 note",
        "answer_sentence": "ReLU는 z<=0인 위치의 신호와 gradient를 막기 때문에 dead unit은 representation capacity를 실제보다 줄인다.",
    },
    {
        "symptom": "bootstrap마다 best 조합이 흔들림",
        "evidence": f"widest f1 p05-p95 interval={most_unstable_boot['f1_interval']:.3f} at {most_unstable_boot['combo']}",
        "likely_cause": "작은 train sample perturbation에 민감한 width/optimizer 조합",
        "confirm_with": "Bootstrap Selection Robustness: best frequency and percentile interval",
        "action": "단일 score 대신 rank frequency와 interval을 함께 보고 선택",
        "answer_sentence": "Bootstrap은 성능 향상 기법이 아니라 train sample 변화에 대한 선택 안정성을 보는 진단 도구다.",
    },
    {
        "symptom": "layer representation 분리가 약함",
        "evidence": f"best after-training layer={int(best_rep['layer_index'])}, ratio={best_rep['between_within_ratio']:.3f}, silhouette={best_rep['silhouette_score']:.3f}",
        "likely_cause": "hidden representation이 class centroid를 충분히 벌리지 못함",
        "confirm_with": "V07 representation quality metrics + layer-wise PCA",
        "action": "width/depth/ReLU/optimizer curve를 함께 재검토",
        "answer_sentence": "PCA 그림의 인상은 between/within ratio와 silhouette 같은 수치로 보조 검증해야 한다.",
    },
    {
        "symptom": "gradient가 특정 Dense layer에서 약함",
        "evidence": f"Dense {int(lowest_grad_layer['dense_index'])} final grad_norm={lowest_grad_layer['mean_grad_norm']:.3g}",
        "likely_cause": "activation gate, initialization, loss saturation, lr 설정 문제",
        "confirm_with": "Gradient Flow Audit: mean_grad_norm by layer",
        "action": "layer별 grad/update/active ratio를 함께 확인",
        "answer_sentence": "loss curve만으로는 부족하며, layer별 gradient flow가 실제로 흐르는지 확인해야 한다.",
    },
], columns=["symptom", "evidence", "likely_cause", "confirm_with", "action", "answer_sentence"])

display(failure_gallery)

fig, axes = plt.subplots(2, 2, figsize=(16, 9))
card_indices = [0, 2, 4, 6]
for ax, idx in zip(axes.ravel(), card_indices):
    row = failure_gallery.iloc[idx]
    ax.axis("off")
    text = (
        f"증상: {row['symptom']}\n\n"
        f"근거: {row['evidence']}\n\n"
        f"원인 후보: {row['likely_cause']}\n\n"
        f"확인 그래프: {row['confirm_with']}\n\n"
        f"수정: {row['action']}\n\n"
        f"답안: {row['answer_sentence']}"
    )
    ax.text(0.02, 0.98, text, va="top", fontsize=10, wrap=True)
plt.suptitle("Failure Gallery: symptom -> evidence -> cause -> action -> answer sentence")
plt.tight_layout()
plt.show()
```

체크포인트:

```text
그래프를 보고 "무슨 일이 일어났는가"가 아니라
"그래서 어떤 원인을 의심하고 어떤 실험으로 확인할 것인가"까지 말할 수 있어야 한다.
```

---

## Final Visual Audit Board

시각화의 종착점은 더 많은 plot이 아니라 판단판이다. 이 보드는 앞선 V00~V07의 산출을 세 장으로 압축한다.

```text
Final Visual Audit Board
= Data Contract
+ Forward Trace
+ Backward Trace
+ Optimizer Trace
+ Validation Evidence
+ Architecture Decision
+ Answer Sentence
```

끝의 기준:

```text
그래프를 보고 관찰 -> 원인 -> 제한 -> 결론 -> 시험 답안 문장을 쓸 수 있으면 끝이다.
```

---

### Board 1. Single Batch Trace Board

```python
# Final Board 1: Single Batch Trace Board.
# 한 mini-batch가 forward/loss/backward/update로 지나가며 어떤 object와 shape를 만드는지 한 장에 압축한다.
X_trace_train, _, _, y_trace_train, _, _ = make_iris_data()
X_batch_trace = X_trace_train[:8]
y_batch_trace = y_trace_train[:8]

trace_net = clone_net_from(make_base_net())
trace_loss = SoftmaxCE()
logits_trace = trace_net.forward(X_batch_trace)
loss_trace = trace_loss.forward(logits_trace, y_batch_trace)
dlogits_trace = trace_loss.backward()
dX_trace = trace_net.backward(dlogits_trace)

trace_dense_layers = [layer for layer in trace_net.layers if isinstance(layer, Dense)]
trace_table = pd.DataFrame([
    ["X_batch", X_batch_trace.shape, "model input", "optimizer 직접 update 대상 아님"],
    ["y_batch", y_batch_trace.shape, "loss target", "optimizer가 직접 보지 않음"],
    ["hidden logits Z1", trace_dense_layers[0].X.shape, "Dense1 cached input", "dW1 계산에 사용"],
    ["logits", logits_trace.shape, "Dense2 output before SoftmaxCE", "loss input"],
    ["loss", round(float(loss_trace), 6), "SoftmaxCE scalar", "optimizer가 직접 보지 않음"],
    ["p-y / B", dlogits_trace.shape, "loss가 만든 logits gradient", "backward 시작점"],
    ["dW1", trace_dense_layers[0].dW.shape, "Dense1 parameter gradient", "optimizer update 대상"],
    ["db1", trace_dense_layers[0].db.shape, "Dense1 bias gradient", "optimizer update 대상"],
    ["dW2", trace_dense_layers[1].dW.shape, "Dense2 parameter gradient", "optimizer update 대상"],
    ["db2", trace_dense_layers[1].db.shape, "Dense2 bias gradient", "optimizer update 대상"],
    ["dX", dX_trace.shape, "previous input으로 전달될 gradient", "optimizer 직접 update 대상 아님"],
], columns=["object", "shape/value", "role", "optimizer relationship"])
display(trace_table)

fig, ax = plt.subplots(figsize=(13, 3))
nodes = [
    "X_batch\n(B,4)",
    "Dense/ReLU\nhidden (B,16)",
    "logits\n(B,3)",
    "SoftmaxCE\nloss",
    "p-y\n(B,3)",
    "backward\ndW/db/dX",
    "optimizer.step\nW,b only",
]
xs = np.arange(len(nodes))
ax.scatter(xs, np.zeros_like(xs), s=1900, color="#f1ce63", edgecolor="#8f6d00")
for i, label in enumerate(nodes):
    ax.text(i, 0, label, ha="center", va="center", fontsize=9)
    if i < len(nodes) - 1:
        ax.annotate("", xy=(i + 0.72, 0), xytext=(i + 0.28, 0), arrowprops=dict(arrowstyle="->", lw=2))
ax.set_title("Board 1. Single Batch Trace: X/y -> forward -> loss -> backward -> optimizer.step(net)")
ax.set_axis_off()
plt.show()
```

---

### Board 2. Learning Dynamics Board

```python
# Final Board 2: Learning Dynamics Board.
# optimizer 비교의 끝은 test를 계속 훔쳐보는 것이 아니라 validation evidence로 선택하고 test는 마지막 보고만 하는 것이다.
fig, axes = plt.subplots(2, 3, figsize=(16, 8))
for run in iris_runs:
    axes[0, 0].plot(run["train_loss"], label=run["optimizer"])
    axes[0, 1].plot(run["val_loss"], label=run["optimizer"])
    axes[0, 2].plot(run["val_accuracy"], label=run["optimizer"])
    axes[1, 0].plot(run["val_macro_f1"], label=run["optimizer"])

axes[0, 0].set_title("train loss")
axes[0, 1].set_title("validation loss")
axes[0, 2].set_title("validation accuracy")
axes[1, 0].set_title("validation macro-F1")

selected_run = next(r for r in iris_runs if r["optimizer"] == selected_optimizer)
selected_cm = selected_run["final_test_confusion_matrix"]
axes[1, 1].imshow(selected_cm, cmap="Blues")
axes[1, 1].set_title(f"final test confusion matrix\nselected by validation: {selected_optimizer}")
axes[1, 1].set_xlabel("pred")
axes[1, 1].set_ylabel("true")
for i in range(selected_cm.shape[0]):
    for j in range(selected_cm.shape[1]):
        axes[1, 1].text(j, i, selected_cm[i, j], ha="center", va="center")

axes[1, 2].axis("off")
selection_text = (
    "same seed / split / scaler / init / batch order\n"
    "optimizer only changes\n\n"
    f"Selected by validation: {selected_optimizer}\n"
    "Test: final report only\n\n"
    "Do not reselect optimizer from test columns."
)
axes[1, 2].text(0.02, 0.95, selection_text, va="top", fontsize=11)

for ax in [axes[0, 0], axes[0, 1], axes[0, 2], axes[1, 0]]:
    ax.set_xlabel("epoch")
    ax.grid(True, alpha=0.3)
    ax.legend()
plt.tight_layout()
plt.show()

display(summary_table)
```

---

### Board 3. Architecture Bridge Board

```python
# Final Board 3: Architecture Bridge Board.
# Week13은 optimizer companion이므로 CNN은 bridge까지만 다룬다.
image_shape = images.shape
flat_shape = flat_scaled.shape
architecture_board = pd.DataFrame([
    ["Tabular Iris", "X=(N,4)", "Dense MLP", "optimizer comparison 본체"],
    [image_bundle["name"], f"image={image_shape}", f"flatten={flat_shape}", "Flatten MLP는 local adjacency를 명시적으로 잃음"],
    ["CNN bridge", "(N,H,W,C)->feature maps", "local receptive field", "Week15 CNN 본수업으로 연결"],
], columns=["data structure", "input shape", "architecture cue", "decision"])
display(architecture_board)

fig, axes = plt.subplots(1, 2, figsize=(13, 4))
axes[0].axis("off")
tabular_text = (
    "Tabular Iris\n"
    "X = (N, 4)\n"
    "Dense(4->H) + ReLU + Dense(H->3)\n"
    "SoftmaxCE\n"
    "optimizer.step(net): W,b,dW,db"
)
axes[0].text(0.05, 0.85, tabular_text, va="top", fontsize=12)
axes[0].set_title("Tabular decision")

axes[1].axis("off")
image_text = (
    "Image tensor\n"
    "image = (N, H, W)\n"
    "Flatten = (N, H*W)\n"
    "Dense MLP loses explicit local adjacency\n"
    "CNN uses local receptive field + feature map"
)
axes[1].text(0.05, 0.85, image_text, va="top", fontsize=12)
axes[1].set_title("Image architecture bridge")
plt.tight_layout()
plt.show()
```

---

### Final Answer Sentence Board

```python
# Final Answer Sentence Board.
# 최종 셀은 새 그래프가 아니라 그래프를 시험 답안 문장으로 바꾸는 표다.
answer_sentence_board = pd.DataFrame([
    ["X/y는 무엇인가", "X는 feature matrix이고 y는 loss가 비교할 target이다."],
    ["Dense(3)는 왜 필요한가", "Iris는 3-class 문제라 class별 logit 3개가 필요하다."],
    ["Dense width는 무엇을 바꾸는가", "width H는 hidden representation 차원과 parameter count를 동시에 바꾼다."],
    ["ReLU는 무엇을 하는가", "ReLU는 음수 pre-activation을 0으로 막고 양수 신호와 gradient를 통과시킨다."],
    ["dW/db/dX는 무엇인가", "dW/db는 parameter update용이고 dX는 이전 layer 전달용이다."],
    ["optimizer는 무엇을 보는가", "optimizer는 X/y가 아니라 W,b,dW,db를 본다."],
    ["Adam이 항상 좋은가", "빠른 수렴은 가능하지만 validation/test 일반화를 보장하지 않는다."],
    ["bootstrap은 왜 쓰는가", "train sample 변화에 대한 model/optimizer 안정성을 보기 위해 쓴다."],
    ["Flatten과 CNN은 어떻게 다른가", "Flatten은 local adjacency를 명시적으로 잃고 CNN은 local receptive field로 feature map을 만든다."],
], columns=["question", "answer start"])
display(answer_sentence_board)
```

최종 scaffold:

```text
관찰:
원인:
제한:
결론:
시험 답안 문장:
```

최종 한 문장:

```text
딥러닝은 model.fit을 외우는 것이 아니라, X/y/tensor를 만들고, output/loss/metric을 설계하고, forward/loss/backward/update를 이해하며, validation에서 일반화를 확인하고, 데이터 구조에 맞는 architecture를 선택하는 과정이다.
```

---

## Final. 체크포인트와 시험 답안 프레임

rubric table:

| 통과 항목 | 기준 | 검증 섹션 |
|---|---|---|
| X/y 판단 | feature matrix와 target vector를 분리 설명 | V01, V05 |
| output/loss/metric | 회귀/분류별 Dense, activation, loss, metric 선택 | V01, V05 |
| backward shape | dW, db, dX shape와 목적 구분 | V03 |
| Dense/ReLU 작동 원리 | width, parameter count, active/dead unit ratio 설명 | V03.5 |
| optimizer 책임 | param/grad만 보고 update한다는 점 설명 | V00, V04 |
| bootstrap 안정성 | train subset perturbation에 따른 validation 분포 해석 | V04.5 |
| curve 해석 | 빠른 수렴과 일반화 성능을 구분 | V04, V05 |
| dataset bridge | Iris와 Fashion-MNIST/digits의 역할 차이 설명 | V01, V05, V06 |
| CNN bridge | Flatten MLP와 CNN의 구조 차이 설명 | V06 |
| MLP representation | Dense+ReLU block 반복이 layer representation을 바꿈 | V07 |
| 최종 판단판 | trace/dynamics/architecture 근거를 답안 문장으로 전환 | Final Visual Audit Board |

아래 질문에 답하는 Markdown scaffold. 각 답안은 시작 문장까지 포함해 바로 작성할 수 있게 둔다:

```text
1. X와 y는 무엇인가?
   - 시작 문장: X는 모델이 입력으로 받는 feature matrix이고, y는 loss가 비교할 target vector이다.
2. output layer는 왜 Dense(3)인가?
   - 시작 문장: Iris는 세 class를 예측하므로 각 sample마다 class별 logit 3개가 필요하다.
3. SoftmaxCE에서 p-y는 무엇인가?
   - 시작 문장: p-y는 예측 확률과 one-hot 정답의 차이이며 logits로 되돌아가는 gradient다.
4. optimizer.step(net)은 왜 X/y를 보지 않는가?
   - 시작 문장: X/y는 forward와 loss/backward에서 gradient를 만드는 데 쓰이고, optimizer는 이미 만들어진 param/grad만 읽는다.
5. SGD, Momentum, RMSProp, Adam의 update state는 무엇이 다른가?
   - 시작 문장: SGD는 현재 gradient만 쓰고, Momentum/RMSProp/Adam은 이전 이동 또는 gradient scale state를 누적한다.
6. loss curve가 빠르게 내려가면 항상 좋은 모델인가?
   - 시작 문장: train loss 감소는 최적화 신호이지만 일반화 판단은 validation curve와 final test 평가를 분리해서 봐야 한다.
7. train/validation/test는 각각 언제 쓰는가?
   - 시작 문장: train은 parameter update, validation은 실험 선택, test는 선택 이후 최종 보고에 사용한다.
8. Iris와 Fashion-MNIST/digits는 각각 어떤 학습 bridge 역할을 하는가?
   - 시작 문장: Iris는 optimizer comparison 본체이고, Fashion-MNIST/digits는 image tensor와 CNN 구조 차이를 연결하는 bridge다.
9. Flatten MLP와 CNN은 이미지 구조를 어떻게 다르게 다루는가?
   - 시작 문장: Flatten MLP는 이미지를 1D vector로 만들어 local adjacency를 명시적으로 잃지만, CNN은 kernel의 local receptive field로 feature map을 만든다.
```

최종 반복 기준:

```text
Optimizer는 X/y를 보지 않는다.
Optimizer는 layer가 들고 있는 param과 grad만 읽고 parameter를 update한다.
```

---

### Final 디벨롭 플랜

- 시각화 목적: V00~V06에서 본 그래프를 시험 답안 문장으로 전환한다.
- 사용할 데이터: 없음. 앞선 출력과 표를 근거로 사용한다.
- 필요한 전처리: 질문을 X/y, shape, optimizer, curve, validation, CNN bridge 순서로 정렬한다.
- 코드 셀 설계: 실행 코드는 추가하지 않고 답안 scaffold와 자기점검표를 둔다.
- 그래프 해석 포인트: 좋은 답안은 그림의 관찰을 원인과 제한까지 연결한다.
- 학생이 자주 하는 오해: 그래프 모양만 묘사하고 update rule이나 데이터 조건을 설명하지 않는다.
- 체크포인트 질문: `Optimizer는 X/y를 보지 않는다`를 Iris 실험 코드 기준으로 설명할 수 있는가?

---

## Final Visualization Develop Pack

고차원/EDA/미분 시각화 확장은 아래 3개 산출물로 분리한다. 현재 notebook 본체의 핵심 실행 루프는 유지하고, 확장 셀은 필요한 섹션에 선택 삽입한다.

| 산출물 | 역할 | notebook 반영 위치 |
|---|---|---|
| `visualization_spec.md` | V00~V06별 최종 시각화 디벨롭 플랜 | 설계/검토 기준 |
| `visualization_cells.py` | 주석 강화 Python cell pack | V01, V02, V03, V04, V05, V06 선택 삽입 |
| `visualization_checklist.md` | 실행/해석/품질 게이트 | Quality Gate 확장 |

핵심 추가 view:

| 영역 | 추가 시각화 | 목적 |
|---|---|---|
| 고차원 loss | 3D surface, 평면도, 정면도, 측면도 | curvature, overshoot, zig-zag 분리 |
| EDA/PCA | PCA 2D/3D, PC1-PC2/PC1-PC3/PC2-PC3 projection | 고차원 feature geometry 확인 |
| mixed association | Pearson, Spearman, Kendall, chi-square, Cramer's V, eta-squared, point-biserial, 100% stacked bar | 연속형/범주형 변수 조합별 관계 지표와 검정 선택 |
| regression residual | covariance/correlation, simple regression, residual vs fitted, PC residual | 상관분석을 모델 검수로 연결 |
| 미분 | tangent, finite difference, gradient field, partial derivative slice | gradient와 update 방향 구분 |
| backward | dW/db/dX heatmap, ReLU derivative mask, SoftmaxCE delta | parameter gradient와 propagated gradient 구분 |
| Dense/ReLU theory | hidden width vs parameter count, active/dead unit ratio | representation capacity와 gradient gate 설명 |
| optimizer | trajectory multi-view, state norm dashboard | 같은 gradient를 update rule이 다르게 쓰는 구조 확인 |
| bootstrap stability | width x optimizer metric distribution, ReLU gate distribution | 단일 score가 아닌 안정성/민감도 해석 |
| bootstrap selection | best-frequency, p05/p50/p95 interval | 선택 자체의 안정성 판단 |
| gradient flow audit | grad norm, update/param ratio, active/dead ratio over epochs | loss curve 뒤의 학습 신호 흐름 진단 |
| ablation | no scaling/no ReLU/width/init/lr variants | 성능 원인을 하나씩 분해 |
| MLP representation bridge | layer별 output shape, active ratio, PCA before/after | Dense+ReLU block 반복의 representation 변화 |
| representation quality | between/within ratio, silhouette score | PCA 인상을 수치로 보조 검증 |
| failure gallery | symptom/evidence/cause/action/answer cards | 그래프를 진단과 답안 문장으로 변환 |
| image bridge | flattened image PCA, local patch/CNN bridge | Dense MLP와 CNN 구조 차이 설명 |
| final audit board | single-batch trace, learning dynamics, architecture decision, answer sentence | 시각화를 최종 판단과 답안화로 압축 |

---

## Developer Functional Spec

이 표는 노트북을 유지보수하거나 다른 Week notebook으로 이식할 때 필요한 기능 명세다.

| 기능 | 함수/셀 | 입력 | 출력 | 실패 시 fallback | web source anchor |
|---|---|---|---|---|---|
| notebook schema | `nbformat.validate` gate | `.ipynb` | valid/invalid | fail report | nbformat |
| paired source | Markdown source sync | `.ipynb`/`.md` | paired text source | keep `.md` as canonical | Jupytext |
| inventory 로드 | `load_inventory` | JSON path candidates | registry dict/DataFrame | 기본 registry | notebook-local policy |
| dataset profile 변환 | `dataset_from_inventory_profile` | inventory, dataset_id | profile DataFrame | `None` | notebook-local policy |
| 데이터 생성 | `get_dataset` | dataset_id | DataFrame or arrays | embedded toy/fallback | no external download policy |
| split | `train_test_split` | X,y | train/val/test | fixed seed error | sklearn train_test_split |
| scaling | `StandardScaler` | train/val/test | scaled arrays | no fit on val/test | sklearn StandardScaler/common pitfalls |
| metric | `accuracy_score`, `f1_score`, `confusion_matrix` | y_true/y_pred | score/matrix | report selected only | sklearn metrics |
| mixed association | `plot_mixed_association_dashboard` | DataFrame, optional target | Pearson/Spearman/Kendall/Cramer's V/chi-square/eta-squared/point-biserial | skip unavailable type pairs | statistics/EDA convention |
| categorical test | `chi_square_pair_test`, `plot_categorical_100pct_stacked` | two categorical columns | observed/expected counts, chi-square, p-value, Cramer's V, row-normalized bar | skip if <2 levels | chi-square independence |
| continuous-category test | `plot_continuous_by_category_gallery`, `continuous_by_category_test_table` | numeric column, category column | box/hist/median, eta-squared, ANOVA/Welch candidates | p-value NaN if scipy unavailable | ANOVA/t-test EDA convention |
| regression residual | `plot_simple_regression_residual_diagnostics`, `plot_pc_regression_residual_diagnostics` | DataFrame, x/y/features | residual plots/metrics | skip missing columns | EDA-to-model diagnostic |
| 이미지 로드 | `load_fashion_mnist_or_digits` | local IDX gzip | image bundle | `sklearn_digits` | TensorFlow Fashion-MNIST/sklearn digits |
| pixel scaling | `scale_image_pixels` | images, dataset_name | scaled_images, scale_note | dataset별 range rule | TensorFlow Fashion-MNIST/sklearn digits |
| 수학 helper | `softmax`, `quad_loss`, `quad_grad`, `make_quad_grid` | arrays | arrays/scalars/grid | 없음 | Core helper cell |
| layer 구현 | `Dense`, `ReLU`, `SoftmaxCE`, `Network` | X/logits/grad | logits/grad/dW/db/dX | assert | Week13 Dense convention |
| Dense/ReLU theory lab | `mlp_param_count`, V03.5 cells | width, Iris train subset | parameter count, active/dead unit ratio | fixed seed | Keras Dense/ReLU |
| optimizer 구현 | `SGD`, `Momentum`, `RMSProp`, `Adam` | param/grad | updated param | state reset | Adam/AdaGrad mechanism map |
| V04 simulation | `run_optimizer_path` | optimizer, `w0` | trajectory/loss history | fixed grid | Matplotlib/optimizer papers |
| bootstrap stability | `bootstrap_dense_optimizer_study` | train bootstrap, fixed val | metric/gate distribution | reduce `BOOT_N`/epochs | sklearn resample/Efron bootstrap |
| Iris 실험 | `train_iris_optimizer` | optimizer | history/summary/cm | fixed seed/split/init | sklearn Iris/metrics |
| gradient flow audit | `train_with_gradient_flow_audit` | optimizer/width/init/lr | grad/update/activation diagnostics | fewer epochs | Dense/ReLU/optimizer theory |
| ablation lab | `ablation_configs` | controlled variants | validation-only failure comparison | reduce variant list | experimental control |
| MLP bridge | `make_deeper_mlp`, `forward_collect_representations` | Iris validation representation | layer output table/PCA | no attention path | Keras Dense/ReLU |
| representation metrics | `representation_quality_metrics` | layer outputs, labels | centroid ratio/silhouette | NaN if invalid | sklearn silhouette_score |
| failure gallery | V08 cells | diagnostic tables | symptom/evidence/action cards | table only | teaching audit |
| 이미지 bridge | V06 cells | image bundle | plots/tables | digits fallback | TensorFlow Fashion-MNIST/sklearn digits |
| final audit board | Board 1/2/3 cells | previous section outputs | trace/dynamics/architecture board | fail if upstream skipped | notebook teaching objective |

---

## Quality Gate

최종본을 잠그기 전에 아래 기준을 확인한다.

| gate | 기준 | 확인 방법 |
|---|---|---|
| JSON validity | `.ipynb`가 JSON으로 parse됨 | `python3 -m json.tool` |
| nbformat schema | `nbformat.validate()` 통과 | nbformat JSON schema |
| paired text source | `.md` 또는 `.py:percent` 생성 가능 | Jupytext text notebook |
| Restart & Run All | 전체 code cell 실행 통과 | `nbclient` execution |
| output cleanliness | 원본 notebook outputs/execution_count 비움 | code cell metadata/output scan |
| fallback safety | inventory/Fashion-MNIST cache 없어도 실행 | embedded/digits fallback |
| no external download | 기본 실행 경로에서 network 사용 없음 | dataset factory policy |
| no test fit | val/test에 `fit` 또는 `fit_transform` 금지 | scikit-learn common pitfalls |
| split-before-fit | scaler는 train에만 fit, val/test는 transform만 사용 | V01, V05 code |
| mixed association type safety | 연속-연속 Pearson/Spearman/Kendall, 범주-범주 chi-square/Cramer's V, 연속-범주 eta-squared 사용 | V01-advanced-B |
| categorical composition | 범주형-범주형 관계는 100% stacked bar와 observed/expected count를 함께 확인 | V01-advanced-B |
| group mean diagnostics | 범주형-연속형 관계는 box/hist와 ANOVA/Welch 후보를 함께 확인 | V01-advanced-B |
| residual diagnostic bridge | 상관 -> 단순 회귀 -> residual pattern -> 모델 수정 후보 연결 | V01-advanced-C |
| validation/test separation | test는 final report only | V05 summary warning |
| fallback image scaling | Fashion `/255`, digits `/16` | TensorFlow Fashion-MNIST, sklearn digits |
| image scaling assert | `flat_scaled` shape/range assert 통과 | V06 assert |
| V04 LR sensitivity | `low/base/high` setting axis 사용, raw lr는 별도 column | V04 code |
| Dense convention | `W=(Dout,Din)` 일관 | V03 assert |
| Dense width theory | `H(Din+1)+K(H+1)` parameter count와 hidden shape 일치 | V03.5 |
| ReLU gate theory | `max(0,z)`와 derivative mask/active ratio/dead unit ratio 표시 | V03.5 |
| optimizer responsibility | `optimizer.step(net)`은 param/grad만 순회 | V00, V04-B |
| bootstrap train-only | bootstrap은 train subset 내부에서만 수행, validation 고정, test 미사용 | V04.5 assert |
| bootstrap distribution | val accuracy, val macro-F1, active ratio, dead unit ratio 분포 표시 | V04.5 |
| bootstrap selection robustness | rank frequency와 p05/p50/p95 interval 표시 | V04.5-C |
| gradient flow audit | layer별 grad norm/update ratio/active ratio/dead ratio 표시 | V05.5 |
| ablation control | scaling/ReLU/width/init/lr를 validation-only로 비교하고 test 미사용 | V05.6 |
| MLP no-attention bridge | Dense+ReLU block 반복만 다루고 Attention/Transformer로 확장하지 않음 | V07 |
| representation quality | layer별 between/within ratio와 silhouette score 표시 | V07-C |
| failure gallery | symptom -> evidence -> cause -> action -> answer sentence cards 포함 | V08 |
| final visual audit | Board 1/2/3와 answer sentence board로 종료 | Final Visual Audit Board |
| appendix placement | Appendix는 본문 뒤, Final 이후 | notebook cell order |

---

### Appendix A-D. V01 보조 데이터 인벤토리

아래 예시는 Week13 optimizer 본문이 아니라, Week14 전처리/EDA bridge를 위한 보조 자료다. 본문에서는 Iris/XOR/Image DatasetCard와 scaling/leakage만 핵심으로 둔다.

---

```python
# Appendix A: Titanic missing/dtype/categorical.
# 외부 다운로드 없이 inventory profile 또는 embedded fallback을 사용한다.
titanic_df = get_dataset("seaborn_titanic", inventory)
display(titanic_df.head())

dtype_summary = pd.DataFrame({"dtype": titanic_df.dtypes.astype(str), "missing": titanic_df.isna().sum()})
display(dtype_summary)

missing_counts = titanic_df.isna().sum().sort_values(ascending=False)
fig, axes = plt.subplots(1, 3, figsize=(13, 3))
missing_counts[missing_counts > 0].plot(kind="bar", ax=axes[0], color="#e15759", title="Titanic missing count")
titanic_df["survived"].value_counts().sort_index().plot(kind="bar", ax=axes[1], color="#59a14f", title="survived distribution")
if "sex" in titanic_df.columns:
    titanic_df["sex"].value_counts().plot(kind="bar", ax=axes[2], color="#4e79a7", title="categorical count: sex")
else:
    axes[2].axis("off")
for ax in axes:
    ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.show()

# Appendix B: toy_missing_values_week14.
# train-only imputation과 full-data imputation의 차이를 값 수준에서 비교한다.
missing_df = get_dataset("toy_missing_values_week14", inventory)
missing_numeric = missing_df.select_dtypes(include=[np.number]).copy()
missing_col = missing_numeric.columns[0]
train_part, test_part = train_test_split(missing_numeric, test_size=0.4, random_state=SEED)
impute_compare = pd.DataFrame({
    "fit_scope": ["train only", "full data (leaky)"],
    "impute_value": [train_part[missing_col].mean(), missing_numeric[missing_col].mean()],
})
display(impute_compare)
missing_numeric.isna().sum().plot(kind="bar", title="toy_missing_values_week14 missingness", color="#f28e2b")
plt.ylabel("missing count")
plt.show()

# Appendix C: toy_categorical_encoding_week14.
# one-hot은 category를 독립 column으로 펼치고, 임의 순서 크기 관계를 만들지 않는다.
cat_df = get_dataset("toy_categorical_encoding_week14", inventory)
display(cat_df)
display(pd.get_dummies(cat_df, drop_first=False).head())

# Appendix D: toy_datetime_features_week14.
# datetime은 그대로 모델에 넣기보다 year/month/hour/dayofweek 같은 numeric feature로 분해한다.
dt_df = get_dataset("toy_datetime_features_week14", inventory)
dt_tmp = dt_df.copy()
if "timestamp" in dt_tmp.columns:
    dt_tmp["timestamp"] = pd.to_datetime(dt_tmp["timestamp"])
    dt_tmp["year"] = dt_tmp["timestamp"].dt.year
    dt_tmp["month"] = dt_tmp["timestamp"].dt.month
    dt_tmp["hour"] = dt_tmp["timestamp"].dt.hour
    dt_tmp["dayofweek"] = dt_tmp["timestamp"].dt.dayofweek
    dt_tmp["is_weekend"] = dt_tmp["dayofweek"].isin([5, 6]).astype(int)
display(dt_tmp.head())
```
