# 3085_problem1.ipynb

# 기말고사 문제 1 — 홍익의 backward 고치기 (2-2-2, ReLU, Softmax+CE)

> **기계학습 라이브러리 활용** · 기말 Take-home · 배점 **25점**


11주의 2-2-1(출력 1개, sigmoid, MSE) 네트워크를 **2-2-2 + 은닉 ReLU + 출력 Softmax+CrossEntropy** 로 바꿨다.

$$x \xrightarrow{W^{(1)},b^{(1)}} z^{(1)} \xrightarrow{\mathrm{ReLU}} a^{(1)} \xrightarrow{W^{(2)},b^{(2)}} z^{(2)} \xrightarrow{\mathrm{softmax}} p,\quad L=-\sum_i y_i\log p_i$$

**상황**: **홍익**이 이 네트워크의 backward 를 나름대로 계산해서 코드로 적었다.
그런데 **원하는 gradient 값(정답 y)** 이 나와야 하는데 **엉뚱한 값(z)** 이 나온다.
홍익이 틀린 줄은 `# ← BUG` 로 표시해 두었다. **그 줄들을 고쳐 정답이 나오게 하라.**

| Part | 할 일 | 배점 |
|------|-------|------|
| 1 | `MLP2` forward 빈칸(ReLU·softmax·loss) 채우기 | 5 |
| 2 | 홍익의 backward 버그 3곳 수정 | 15 |
| 3 | 개념 관련 객관식 문제 | 5 |

**제약**: numpy 만. 코드를 처음부터 짜는 문제가 아니라 — 표시된 곳만 고칠 것!

## ⚠️ 학번 입력 (필수)

```python
STUDENT_ID = "3085"   # ← 본인 학번 마지막 4자리
assert STUDENT_ID != "0000", "학번을 마지막 4자리를 입력하세요!"
print("학번:", STUDENT_ID)
```

```text
학번: 3085
```

## 환경 준비

```python
import numpy as np
import matplotlib.pyplot as plt
```

---
# Part 1. forward 빈칸 채우기 (5점)

은닉 활성화가 **ReLU** 로 바뀐 것에 주의. `_relu`, `_softmax`, `loss` 세 줄만 채워라.
- `_relu(z)`: `max(0, z)` (numpy: `np.maximum`)
- `_softmax(z)`: `z - max(z)` 후 `exp / 합`
- `loss(cache, y)`: CrossEntropy `-Σ yᵢ log pᵢ` (`+1e-12`)

```python
class MLP2:
    def __init__(self, random_seed=None):
        if random_seed is not None: np.random.seed(random_seed)
        self.W1=np.random.randn(2,2)*0.5; self.b1=np.zeros(2)
        self.W2=np.random.randn(2,2)*0.5; self.b2=np.zeros(2)

    def _relu(self, z):
        return np.maximum(0.0, z)

    def _softmax(self, z):
        z=z-np.max(z); e=np.exp(z); return e/np.sum(e)

    def forward(self, x):
        a1 = self._relu(self.W1 @ x + self.b1)
        return self._softmax(self.W2 @ a1 + self.b2)

    def forward_with_cache(self, x):
        z1=self.W1@x+self.b1; a1=self._relu(z1); z2=self.W2@a1+self.b2; p=self._softmax(z2)
        return {"x":x,"z1":z1,"a1":a1,"z2":z2,"p":p}

    def loss(self, cache, y):
        return -np.sum(y*np.log(cache["p"]+1e-12))


_m=MLP2(random_seed=0); _p=_m.forward(np.array([0.5,-0.3]))
print("forward 합 =", round(float(np.sum(_p)),6)) # output의 합이 1인지 확인
```

```text
forward 합 = 1.0
```

---
# Part 2. 홍익의 backward 고치기 (15점)

아래 도구를 먼저 실행하라.

```python
# ============================================================
# [수정 금지] 정답 forward + 도구. 그대로 실행하세요.
# ============================================================
def relu(z): return np.maximum(0.0, z)
def relu_prime(z): return (z > 0).astype(float)   # ReLU 미분: z>0 → 1, 아니면 0

class MLP2Ref:
    """2-2-2, 은닉 ReLU, 출력 Softmax+CE. (정답 forward)"""
    def __init__(self, random_seed=None):
        if random_seed is not None: np.random.seed(random_seed)
        self.W1=np.random.randn(2,2)*0.5; self.b1=np.zeros(2)
        self.W2=np.random.randn(2,2)*0.5; self.b2=np.zeros(2)
    def _softmax(self,z): z=z-np.max(z); e=np.exp(z); return e/np.sum(e)
    def forward_with_cache(self,x):
        z1=self.W1@x+self.b1; a1=relu(z1); z2=self.W2@a1+self.b2; p=self._softmax(z2)
        return {"x":x,"z1":z1,"a1":a1,"z2":z2,"p":p}
    def forward(self,x): return self.forward_with_cache(x)["p"]
    def loss(self,cache,y): return -np.sum(y*np.log(cache["p"]+1e-12))

def gradient_check(mlp, backward_fn, x, y, eps=1e-5):
    ana=backward_fn(mlp, mlp.forward_with_cache(x), y)
    def L(): return mlp.loss(mlp.forward_with_cache(x), y)
    per={}
    for nm,par,g in [("W1",mlp.W1,ana["dW1"]),("b1",mlp.b1,ana["db1"]),
                     ("W2",mlp.W2,ana["dW2"]),("b2",mlp.b2,ana["db2"])]:
        it=np.nditer(par,flags=["multi_index"],op_flags=["readwrite"]); mx=0.0
        while not it.finished:
            i=it.multi_index;o=par[i];par[i]=o+eps;lp=L();par[i]=o-eps;lm=L();par[i]=o
            num=(lp-lm)/(2*eps); mx=max(mx,abs(num-g[i])/max(abs(num),abs(g[i]),1e-12)); it.iternext()
        per[nm]=mx
    return per

# ----- 고정 테스트 케이스: "원하는 결과(정답)" -----
def make_case():
    m=MLP2Ref()
    m.W1=np.array([[0.1,0.2],[0.3,0.4]]); m.b1=np.zeros(2)
    m.W2=np.array([[0.5,0.6],[0.7,0.8]]); m.b2=np.zeros(2)
    x=np.array([1.0,1.0]); y=np.array([1.0,0.0])
    return m, x, y
EXPECTED = {  # 정답 gradient (원하는 결과 y)
    "dW2": [[-0.165,-0.3849],[0.165,0.3849]],
    "db2": [-0.5498,0.5498],
    "dW1": [[0.11,0.11],[0.11,0.11]],
    "db1": [0.11,0.11],
}
def compare_to_expected(backward_fn):
    m,x,y=make_case(); g=backward_fn(m, m.forward_with_cache(x), y)
    print(f"{'param':5s} | {'홍익 결과(z)':28s} | 정답(y)")
    print("-"*70); allok=True
    for k in ["dW2","db2","dW1","db1"]:
        got=np.round(g[k],4); exp=np.array(EXPECTED[k]); ok=np.allclose(got,exp,atol=1e-3)
        allok&=ok
        print(f"{k:5s} | {str(got.tolist()):28s} | {exp.tolist()}  {'✅' if ok else '❌'}")
    print("\n→ 모두 정답과 일치!" if allok else "\n→ 아직 다릅니다. 표시된 줄을 고치세요.")
    return allok
print("도구 준비 완료.")
```

```text
도구 준비 완료.
```

## 홍익의 backward — 버그 3곳 (`# ← BUG`)

표시된 줄을 고쳐, `compare_to_expected(backward_honggik)` 가 **모두 ✅** 가 되도록 하라.
- **BUG1 (출력층)**: Softmax+CE 의 출력 오차 ∂L/∂z² 는 *깔끔*하다.
- **BUG2 (은닉층)**: 출력이 2개다. 은닉 뉴런으로 들어오는 에러는 **두 출력 경로의 합**인데, 홍익은 한 경로만 더했다.
- **BUG3 (ReLU)**: 은닉 활성화가 ReLU 인데 홍익은 *sigmoid* 미분을 썼다.

```python
def backward_honggik(mlp, cache, y):
    x, z1, a1, p = cache["x"], cache["z1"], cache["a1"], cache["p"]

    # 1. 출력층 오차
    dz2 = p - y                                           # ← BUG1 수정: Softmax+CE
    dW2 = np.outer(dz2, a1)
    db2 = dz2

    # 2. 은닉층으로 에러 역전파 (출력 0 경로 + 출력 1 경로 = 합!)
    dL_da1_0 = mlp.W2[0,0]*dz2[0] + mlp.W2[1,0]*dz2[1]  # ← BUG2 수정
    dL_da1_1 = mlp.W2[0,1]*dz2[0] + mlp.W2[1,1]*dz2[1]  # ← BUG2 수정
    dL_da1 = np.array([dL_da1_0, dL_da1_1])

    # 3. 활성화 미분 통과 (ReLU!)
    delta1 = dL_da1 * relu_prime(z1)                       # ← BUG3 수정

    # 4. 은닉층 파라미터
    dW1 = np.outer(delta1, x)
    db1 = delta1
    return {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2}

compare_to_expected(backward_honggik)
```

```text
param | 홍익 결과(z)                     | 정답(y)
----------------------------------------------------------------------
dW2   | [[-0.165, -0.3849], [0.165, 0.3849]] | [[-0.165, -0.3849], [0.165, 0.3849]]  ✅
db2   | [-0.5498, 0.5498]            | [-0.5498, 0.5498]  ✅
dW1   | [[0.11, 0.11], [0.11, 0.11]] | [[0.11, 0.11], [0.11, 0.11]]  ✅
db1   | [0.11, 0.11]                 | [0.11, 0.11]  ✅

→ 모두 정답과 일치!
```

```text
True
```

### (선택, 채점 외) 랜덤 입력으로도 검증
`compare_to_expected` 는 고정 케이스만 본다. 아래는 임의 입력에서 수치미분과 비교한다(모두 < 1e-7 이면 완벽).

```python
np.random.seed(7); _mr=MLP2Ref(random_seed=7); _xr=np.random.randn(2)
_per=gradient_check(_mr, backward_honggik, _xr, np.array([1.0,0.0]))
print({k: f"{v:.1e}" for k,v in _per.items()})
```

```text
{'W1': '5.7e-11', 'b1': '1.6e-11', 'W2': '6.8e-11', 'b2': '1.4e-11'}
```

---
# Part 3. 개념 객관식 (5점)

Q1~5번 객관식 문제의 답을 다음 셀 `concept_answers` 딕셔너리의 각 문제 키 값으로 작성하시오. (`None` 부분을 `'a'`~`'d'` 로 수정)

**Q1.** Softmax+CE 의 출력층 오차 ∂L/∂z² 는? <br>
&nbsp;(a) p−y &nbsp;(b) (p−y)p(1−p) &nbsp;(c) y−p &nbsp;(d) (p−y)a¹

**Q2.** 출력이 **2개**일 때, 은닉 뉴런 a¹ⱼ 로 들어오는 에러 ∂L/∂a¹ⱼ 는? <br>
&nbsp;(a) 출력 0 경로만 &nbsp;(b) 출력 1 경로만 &nbsp;(c) **두 출력 경로의 합** &nbsp;(d) 두 경로의 곱

**Q3.** 은닉 활성화가 ReLU 일 때 δ¹ = ∂L/∂a¹ · ? (단, z¹ 은 ReLU 입력) <br>
&nbsp;(a) a¹(1−a¹) &nbsp;(b) (z¹>0) &nbsp;(c) 1 &nbsp;(d) z¹

**Q4.** 홍익이 BUG2(출력 1 경로 누락)만 가지고 있을 때, 값이 틀려지는 gradient 는? <br>
&nbsp;(a) dW2, db2 &nbsp;(b) dW1, db1 &nbsp;(c) 전부 &nbsp;(d) 없음

**Q5.** 출력층 오차 dz²(=BUG1) 가 틀리면 영향 범위는? <br>
&nbsp;(a) dW2, db2 만 &nbsp;(b) dW1, db1 만 &nbsp;(c) 네 파라미터 전부 &nbsp;(d) 없음

```python
concept_answers = {"q1":"a","q2":"c","q3":"b","q4":"b","q5":"c"}   # 'a'~'d'
```

---
# ✅ 제출 전 체크리스트
- [ ] 학번 입력 / Part 1 forward 합 = 1
- [ ] `compare_to_expected(backward_honggik)` 가 **모두 ✅**
- [ ] `concept_answers` q1~q5 채움
- [ ] 파일명 `[학번]_problem1.ipynb`

---

# 3085_problem2.ipynb

# 기말고사 문제 2 — Beijing PM2.5 회귀 분석

> **기계학습 라이브러리 활용** · 기말 Take-home Exam
> 배점: **25점** (Part B 6 + Part C 14 + Part D 5)  ·  데이터 전처리(Part A)는 제공 코드

---

## 📌 시험 안내 (필독)

### 데이터
- **출처**: UCI ML Repository — Beijing PM2.5 Data Set
- **URL**: `https://raw.githubusercontent.com/jbrownlee/Datasets/master/pollution.csv`
- **샘플**: 43,824개 (시간별, 5년치)
- **타겟**: `pm2.5` 컬럼 (회귀)
- **특성**: 결측치 있음, 범주형(`cbwd` 풍향) 포함

---

## ⚠️ 학번 입력 (필수)

다음 셀의 `STUDENT_ID` 변수에 본인 학번을 입력하세요.
**입력하지 않으면 0점 처리됩니다.**

```python
STUDENT_ID = "3085"   # ← 본인 학번 마지막 4자리로 변경
SEED = int(STUDENT_ID)

assert STUDENT_ID != "0000", "학번을 입력하세요!"
print(f'학번(끝4자리): {STUDENT_ID}, SEED: {SEED}')
```

```text
학번(끝4자리): 3085, SEED: 3085
```

## 환경 준비

필요한 라이브러리를 import하고 seed를 고정.

**요구사항**:
- numpy, pandas, matplotlib
- tensorflow, keras
- sklearn (train_test_split, StandardScaler)
- numpy와 tensorflow 모두 SEED로 고정

```python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '0')
os.environ.setdefault('MPLCONFIGDIR', '/tmp/mplconfig')
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

import warnings
warnings.filterwarnings('ignore', message=r'Glyph .* missing from font.*', category=UserWarning)
warnings.filterwarnings('ignore', message=r'.*Glyph .* missing from current font.*', category=UserWarning)
warnings.filterwarnings('ignore', message=r'Do not pass an `input_shape`/`input_dim` argument to a layer.*', category=UserWarning)

import contextlib
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@contextlib.contextmanager
def suppress_native_stderr():
    stderr_fd = sys.stderr.fileno()
    saved_stderr_fd = os.dup(stderr_fd)
    try:
        with open(os.devnull, 'w') as devnull:
            os.dup2(devnull.fileno(), stderr_fd)
            yield
    finally:
        os.dup2(saved_stderr_fd, stderr_fd)
        os.close(saved_stderr_fd)

# TensorFlow/Keras 초기화 때 출력되는 CUDA/absl stderr 로그는 과제 출력과 무관하므로 숨긴다.
with suppress_native_stderr():
    import keras
    from keras import Sequential
    from keras.layers import Dense, Dropout, BatchNormalization, Activation
    from keras.regularizers import l2
    from keras.callbacks import EarlyStopping

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report

# 재현성: 학번 기반 SEED로 고정 (numpy + 현재 keras 백엔드 동시 고정)
np.random.seed(SEED)
with suppress_native_stderr():
    keras.utils.set_random_seed(SEED)
    keras_backend_name = keras.backend.backend()

print('Keras  :', keras.__version__, '| backend:', keras_backend_name)
print('pandas :', pd.__version__)
```

```text
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1781877872.429519  424734 cudart_stub.cc:31] Could not find cuda drivers on your machine, GPU will not be used.
```

```text
Keras  : 3.14.1 | backend: tensorflow
pandas : 3.0.2
```

```text
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1781877873.688823  424734 cudart_stub.cc:31] Could not find cuda drivers on your machine, GPU will not be used.
```

---
데이터 전처리 (제공 코드 · 채점 제외)

## A1. 데이터 로드 및 결측치 처리 

1. URL에서 데이터를 로드
2. 전체 결측치 개수를 출력
3. 어느 컬럼에 결측치가 있는지 출력

**출력**:
- 원본 데이터 shape
- 처리 전 결측치 개수
- 처리 후 결측치 개수

```python
# 데이터 로드
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/pollution.csv'
df = pd.read_csv(url)

print('=== 원본 데이터 ===')
print(f'Shape: {df.shape}')
print(f'결측치 총 개수: {df.isnull().sum().sum()}')
print(f'결측치 컬럼별:\n{df.isnull().sum()[df.isnull().sum() > 0]}')

print(df.head(10))

print(df.tail(10))
print(df.info())
print(df.describe())

# 컬럼 목록
print(f'Columns: {df.columns}') 
#Index(['No', 'year', 'month', 'day', 'hour', 'pm2.5', 'DEWP', 'TEMP', 'PRES','cbwd', 'Iws', 'Is', 'Ir'],
print(df.columns.tolist())
#['No', 'year', 'month', 'day', 'hour', 'pm2.5', 'DEWP', 'TEMP', 'PRES', 'cbwd', 'Iws', 'Is', 'Ir']
print(df.dtypes)
display(df.head())

print(' === 1단계 : 컬럼 역할 1차 정리 ===')
# 데이터프레임을 바탕으로, 데이터샘플의 컬럼과 의미를 이해함이 목적.
# 트랜스포즈(전치)하지 않고, 모든 텍스트 전부 들어가게 출력
from IPython.display import display, HTML

col_info = pd.DataFrame({
    'column': ['No', 'year', 'month', 'day', 'hour', 'pm2.5', 'DEWP', 'TEMP', 'PRES', 'cbwd', 'Iws', 'Is', 'Ir'],
    '1_초기분류': [
        'id',
        'time',
        'time',
        'time',
        'time',
        'target',
        'numeric_feature',
        'numeric_feature',
        'numeric_feature',
        'categorical_feature',
        'numeric_feature',
        'numeric_feature',
        'numeric_feature'
    ],
    '2_라벨': [
        '행 번호. 관측 순서 또는 ID, = ~feature',
        '관측 연도',
        '관측 월',
        '관측 일',
        '관측 시각',
        'PM2.5 초미세먼지 농도. µg/m³단위',
        'Dew Point, ℃, 이슬점 //습도 상태를 나타내는 기상 feature',
        'Temperature, ℃, 기온 //계절, 난방, 대기 안정성과 연결되는 feature',
        'Pressure, hPa, 기압고기압/저기 // 대기 정체와 관련된 feature',
        'Combined Wind Direction, 풍향, NW, NE, SE, 등 범주형, // 풍향+본데이터에선 오염물질질 유입/확산 방향 feature',
        'Cumulated Wind Speed, 누적 풍속. m/s // 풍향에 따른 확산 정도 feature, 누적 풍속',
        'Cumulated hours of Snow, IS, 시간, 누적 눈 시간 // 강수·계절(겨울) feature',
        'Cumulated hours of rain, IR, 누적 비 시간. // 누적강수량, 본 데이터에선 대기오염 개선 효과 feature'
    ],
    '3_도메인심화' : [
        'N/A',
        'N/A',
        'N/A',
        'N/A',
        'N/A',
        'Particulate Matter 2.5 / (m2.5 = 100)=공기 1m³ 안에 PM2.5 질량 100µg. 대기오염의 결과값.',
        'DEWP가 그 기온(TEMP = 기온)에 비해 가까우면 공기가 습한 편으로 해석. ',
        '계절성과 생활·산업 활동의 proxy 역할 / 겨울에는 난방, 대기 정체 OR 여름에는 대기혼합 등',
        '“공기가 잘 섞이는 상태인가, 정체되는 상태인가”, 고기압성? 저기압? =강한 바람·강수 상황? ',
        'NW는 북서풍, NE는 북동풍, SE는 남동풍. cv는 보통 calm/variable',
        '“공기가 얼마나 많이 이동했는가”=환기·확산 능력',
        'wet deposition, 즉 세정 효과 + 계절요인',
        '상동'
    ]
})

# 각 셀의 줄 바꿈이 발생하도록 style 확장 (css =pre-line 적용)
styles = [
    dict(selector="td", props=[("white-space", "pre-line"), ("max-width", "320px")]),
    dict(selector="th", props=[("white-space", "pre-line")])
]
display(HTML(col_info.style.set_table_styles(styles).set_properties(**{'height': 'auto'}).to_html()))
```

```text
=== 원본 데이터 ===
Shape: (43824, 13)
결측치 총 개수: 2067
결측치 컬럼별:
pm2.5    2067
dtype: int64
   No  year  month  day  hour  pm2.5  DEWP  TEMP    PRES cbwd    Iws  Is  Ir
0   1  2010      1    1     0    NaN   -21 -11.0  1021.0   NW   1.79   0   0
1   2  2010      1    1     1    NaN   -21 -12.0  1020.0   NW   4.92   0   0
2   3  2010      1    1     2    NaN   -21 -11.0  1019.0   NW   6.71   0   0
3   4  2010      1    1     3    NaN   -21 -14.0  1019.0   NW   9.84   0   0
4   5  2010      1    1     4    NaN   -20 -12.0  1018.0   NW  12.97   0   0
5   6  2010      1    1     5    NaN   -19 -10.0  1017.0   NW  16.10   0   0
6   7  2010      1    1     6    NaN   -19  -9.0  1017.0   NW  19.23   0   0
7   8  2010      1    1     7    NaN   -19  -9.0  1017.0   NW  21.02   0   0
8   9  2010      1    1     8    NaN   -19  -9.0  1017.0   NW  24.15   0   0
9  10  2010      1    1     9    NaN   -20  -8.0  1017.0   NW  27.28   0   0
          No  year  month  day  hour  pm2.5  DEWP  TEMP    PRES cbwd     Iws  \
43814  43815  2014     12   31    14    9.0   -27   1.0  1032.0   NW  196.21   
43815  43816  2014     12   31    15   11.0   -26   1.0  1032.0   NW  205.15   
43816  43817  2014     12   31    16    8.0   -23   0.0  1032.0   NW  214.09   
43817  43818  2014     12   31    17    9.0   -22  -1.0  1033.0   NW  221.24   
43818  43819  2014     12   31    18   10.0   -22  -2.0  1033.0   NW  226.16   
43819  43820  2014     12   31    19    8.0   -23  -2.0  1034.0   NW  231.97   
43820  43821  2014     12   31    20   10.0   -22  -3.0  1034.0   NW  237.78   
43821  43822  2014     12   31    21   10.0   -22  -3.0  1034.0   NW  242.70   
43822  43823  2014     12   31    22    8.0   -22  -4.0  1034.0   NW  246.72   
43823  43824  2014     12   31    23   12.0   -21  -3.0  1034.0   NW  249.85   

       Is  Ir  
43814   0   0  
43815   0   0  
43816   0   0  
43817   0   0  
43818   0   0  
43819   0   0  
43820   0   0  
43821   0   0  
43822   0   0  
43823   0   0  
<class 'pandas.DataFrame'>
RangeIndex: 43824 entries, 0 to 43823
Data columns (total 13 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   No      43824 non-null  int64  
 1   year    43824 non-null  int64  
 2   month   43824 non-null  int64  
 3   day     43824 non-null  int64  
 4   hour    43824 non-null  int64  
 5   pm2.5   41757 non-null  float64
 6   DEWP    43824 non-null  int64  
 7   TEMP    43824 non-null  float64
 8   PRES    43824 non-null  float64
 9   cbwd    43824 non-null  str    
 10  Iws     43824 non-null  float64
 11  Is      43824 non-null  int64  
 12  Ir      43824 non-null  int64  
dtypes: float64(4), int64(8), str(1)
memory usage: 4.3 MB
None
                 No          year         month           day          hour  \
count  43824.000000  43824.000000  43824.000000  43824.000000  43824.000000   
mean   21912.500000   2012.000000      6.523549     15.727820     11.500000   
std    12651.043435      1.413842      3.448572      8.799425      6.922266   
min        1.000000   2010.000000      1.000000      1.000000      0.000000   
25%    10956.750000   2011.000000      4.000000      8.000000      5.750000   
50%    21912.500000   2012.000000      7.000000     16.000000     11.500000   
75%    32868.250000   2013.000000     10.000000     23.000000     17.250000   
max    43824.000000   2014.000000     12.000000     31.000000     23.000000   

              pm2.5          DEWP          TEMP          PRES           Iws  \
count  41757.000000  43824.000000  43824.000000  43824.000000  43824.000000   
mean      98.613215      1.817246     12.448521   1016.447654     23.889140   
std       92.050387     14.433440     12.198613     10.268698     50.010635   
min        0.000000    -40.000000    -19.000000    991.000000      0.450000   
25%       29.000000    -10.000000      2.000000   1008.000000      1.790000   
50%       72.000000      2.000000     14.000000   1016.000000      5.370000   
75%      137.000000     15.000000     23.000000   1025.000000     21.910000   
max      994.000000     28.000000     42.000000   1046.000000    585.600000   

                 Is            Ir  
count  43824.000000  43824.000000  
mean       0.052734      0.194916  
std        0.760375      1.415867  
min        0.000000      0.000000  
25%        0.000000      0.000000  
50%        0.000000      0.000000  
75%        0.000000      0.000000  
max       27.000000     36.000000  
Columns: Index(['No', 'year', 'month', 'day', 'hour', 'pm2.5', 'DEWP', 'TEMP', 'PRES',
       'cbwd', 'Iws', 'Is', 'Ir'],
      dtype='str')
['No', 'year', 'month', 'day', 'hour', 'pm2.5', 'DEWP', 'TEMP', 'PRES', 'cbwd', 'Iws', 'Is', 'Ir']
No         int64
year       int64
month      int64
day        int64
hour       int64
pm2.5    float64
DEWP       int64
TEMP     float64
PRES     float64
cbwd         str
Iws      float64
Is         int64
Ir         int64
dtype: object
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>No</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>hour</th>
      <th>pm2.5</th>
      <th>DEWP</th>
      <th>TEMP</th>
      <th>PRES</th>
      <th>cbwd</th>
      <th>Iws</th>
      <th>Is</th>
      <th>Ir</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>NaN</td>
      <td>-21</td>
      <td>-11.0</td>
      <td>1021.0</td>
      <td>NW</td>
      <td>1.79</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>NaN</td>
      <td>-21</td>
      <td>-12.0</td>
      <td>1020.0</td>
      <td>NW</td>
      <td>4.92</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>NaN</td>
      <td>-21</td>
      <td>-11.0</td>
      <td>1019.0</td>
      <td>NW</td>
      <td>6.71</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>NaN</td>
      <td>-21</td>
      <td>-14.0</td>
      <td>1019.0</td>
      <td>NW</td>
      <td>9.84</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>4</td>
      <td>NaN</td>
      <td>-20</td>
      <td>-12.0</td>
      <td>1018.0</td>
      <td>NW</td>
      <td>12.97</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>

```text
 === 1단계 : 컬럼 역할 1차 정리 ===
```

<style type="text/css">
#T_51bc3 td {
  white-space: pre-line;
  max-width: 320px;
}
#T_51bc3 th {
  white-space: pre-line;
}
#T_51bc3_row0_col0, #T_51bc3_row0_col1, #T_51bc3_row0_col2, #T_51bc3_row0_col3, #T_51bc3_row1_col0, #T_51bc3_row1_col1, #T_51bc3_row1_col2, #T_51bc3_row1_col3, #T_51bc3_row2_col0, #T_51bc3_row2_col1, #T_51bc3_row2_col2, #T_51bc3_row2_col3, #T_51bc3_row3_col0, #T_51bc3_row3_col1, #T_51bc3_row3_col2, #T_51bc3_row3_col3, #T_51bc3_row4_col0, #T_51bc3_row4_col1, #T_51bc3_row4_col2, #T_51bc3_row4_col3, #T_51bc3_row5_col0, #T_51bc3_row5_col1, #T_51bc3_row5_col2, #T_51bc3_row5_col3, #T_51bc3_row6_col0, #T_51bc3_row6_col1, #T_51bc3_row6_col2, #T_51bc3_row6_col3, #T_51bc3_row7_col0, #T_51bc3_row7_col1, #T_51bc3_row7_col2, #T_51bc3_row7_col3, #T_51bc3_row8_col0, #T_51bc3_row8_col1, #T_51bc3_row8_col2, #T_51bc3_row8_col3, #T_51bc3_row9_col0, #T_51bc3_row9_col1, #T_51bc3_row9_col2, #T_51bc3_row9_col3, #T_51bc3_row10_col0, #T_51bc3_row10_col1, #T_51bc3_row10_col2, #T_51bc3_row10_col3, #T_51bc3_row11_col0, #T_51bc3_row11_col1, #T_51bc3_row11_col2, #T_51bc3_row11_col3, #T_51bc3_row12_col0, #T_51bc3_row12_col1, #T_51bc3_row12_col2, #T_51bc3_row12_col3 {
  height: auto;
}
</style>
<table id="T_51bc3">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_51bc3_level0_col0" class="col_heading level0 col0" >column</th>
      <th id="T_51bc3_level0_col1" class="col_heading level0 col1" >1_초기분류</th>
      <th id="T_51bc3_level0_col2" class="col_heading level0 col2" >2_라벨</th>
      <th id="T_51bc3_level0_col3" class="col_heading level0 col3" >3_도메인심화</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_51bc3_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_51bc3_row0_col0" class="data row0 col0" >No</td>
      <td id="T_51bc3_row0_col1" class="data row0 col1" >id</td>
      <td id="T_51bc3_row0_col2" class="data row0 col2" >행 번호. 관측 순서 또는 ID, = ~feature</td>
      <td id="T_51bc3_row0_col3" class="data row0 col3" >N/A</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_51bc3_row1_col0" class="data row1 col0" >year</td>
      <td id="T_51bc3_row1_col1" class="data row1 col1" >time</td>
      <td id="T_51bc3_row1_col2" class="data row1 col2" >관측 연도</td>
      <td id="T_51bc3_row1_col3" class="data row1 col3" >N/A</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_51bc3_row2_col0" class="data row2 col0" >month</td>
      <td id="T_51bc3_row2_col1" class="data row2 col1" >time</td>
      <td id="T_51bc3_row2_col2" class="data row2 col2" >관측 월</td>
      <td id="T_51bc3_row2_col3" class="data row2 col3" >N/A</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_51bc3_row3_col0" class="data row3 col0" >day</td>
      <td id="T_51bc3_row3_col1" class="data row3 col1" >time</td>
      <td id="T_51bc3_row3_col2" class="data row3 col2" >관측 일</td>
      <td id="T_51bc3_row3_col3" class="data row3 col3" >N/A</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_51bc3_row4_col0" class="data row4 col0" >hour</td>
      <td id="T_51bc3_row4_col1" class="data row4 col1" >time</td>
      <td id="T_51bc3_row4_col2" class="data row4 col2" >관측 시각</td>
      <td id="T_51bc3_row4_col3" class="data row4 col3" >N/A</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_51bc3_row5_col0" class="data row5 col0" >pm2.5</td>
      <td id="T_51bc3_row5_col1" class="data row5 col1" >target</td>
      <td id="T_51bc3_row5_col2" class="data row5 col2" >PM2.5 초미세먼지 농도. µg/m³단위</td>
      <td id="T_51bc3_row5_col3" class="data row5 col3" >Particulate Matter 2.5 / (m2.5 = 100)=공기 1m³ 안에 PM2.5 질량 100µg. 대기오염의 결과값.</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_51bc3_row6_col0" class="data row6 col0" >DEWP</td>
      <td id="T_51bc3_row6_col1" class="data row6 col1" >numeric_feature</td>
      <td id="T_51bc3_row6_col2" class="data row6 col2" >Dew Point, ℃, 이슬점 //습도 상태를 나타내는 기상 feature</td>
      <td id="T_51bc3_row6_col3" class="data row6 col3" >DEWP가 그 기온(TEMP = 기온)에 비해 가까우면 공기가 습한 편으로 해석. </td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_51bc3_row7_col0" class="data row7 col0" >TEMP</td>
      <td id="T_51bc3_row7_col1" class="data row7 col1" >numeric_feature</td>
      <td id="T_51bc3_row7_col2" class="data row7 col2" >Temperature, ℃, 기온 //계절, 난방, 대기 안정성과 연결되는 feature</td>
      <td id="T_51bc3_row7_col3" class="data row7 col3" >계절성과 생활·산업 활동의 proxy 역할 / 겨울에는 난방, 대기 정체 OR 여름에는 대기혼합 등</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_51bc3_row8_col0" class="data row8 col0" >PRES</td>
      <td id="T_51bc3_row8_col1" class="data row8 col1" >numeric_feature</td>
      <td id="T_51bc3_row8_col2" class="data row8 col2" >Pressure, hPa, 기압고기압/저기 // 대기 정체와 관련된 feature</td>
      <td id="T_51bc3_row8_col3" class="data row8 col3" >“공기가 잘 섞이는 상태인가, 정체되는 상태인가”, 고기압성? 저기압? =강한 바람·강수 상황? </td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_51bc3_row9_col0" class="data row9 col0" >cbwd</td>
      <td id="T_51bc3_row9_col1" class="data row9 col1" >categorical_feature</td>
      <td id="T_51bc3_row9_col2" class="data row9 col2" >Combined Wind Direction, 풍향, NW, NE, SE, 등 범주형, // 풍향+본데이터에선 오염물질질 유입/확산 방향 feature</td>
      <td id="T_51bc3_row9_col3" class="data row9 col3" >NW는 북서풍, NE는 북동풍, SE는 남동풍. cv는 보통 calm/variable</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_51bc3_row10_col0" class="data row10 col0" >Iws</td>
      <td id="T_51bc3_row10_col1" class="data row10 col1" >numeric_feature</td>
      <td id="T_51bc3_row10_col2" class="data row10 col2" >Cumulated Wind Speed, 누적 풍속. m/s // 풍향에 따른 확산 정도 feature, 누적 풍속</td>
      <td id="T_51bc3_row10_col3" class="data row10 col3" >“공기가 얼마나 많이 이동했는가”=환기·확산 능력</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_51bc3_row11_col0" class="data row11 col0" >Is</td>
      <td id="T_51bc3_row11_col1" class="data row11 col1" >numeric_feature</td>
      <td id="T_51bc3_row11_col2" class="data row11 col2" >Cumulated hours of Snow, IS, 시간, 누적 눈 시간 // 강수·계절(겨울) feature</td>
      <td id="T_51bc3_row11_col3" class="data row11 col3" >wet deposition, 즉 세정 효과 + 계절요인</td>
    </tr>
    <tr>
      <th id="T_51bc3_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_51bc3_row12_col0" class="data row12 col0" >Ir</td>
      <td id="T_51bc3_row12_col1" class="data row12 col1" >numeric_feature</td>
      <td id="T_51bc3_row12_col2" class="data row12 col2" >Cumulated hours of rain, IR, 누적 비 시간. // 누적강수량, 본 데이터에선 대기오염 개선 효과 feature</td>
      <td id="T_51bc3_row12_col3" class="data row12 col3" >상동</td>
    </tr>
  </tbody>
</table>

**결측치 처리 ** 

```python
# 결측치 처리: pm2.5의 결측치는 시간 연속성을 활용한 forward fill로 채움
# (시간 연속 데이터이므로 직전 시간 값으로 채우는 것이 합리적)
# 대안: dropna() — 2067개(약 4.7%)이므로 제거도 가능

df_clean = df.copy()
df_clean['pm2.5'] = df_clean['pm2.5'].ffill().bfill()   # 시간 연속성 활용 (pandas 3.x 호환)

print(f'결측치 처리 후: {df_clean.isnull().sum().sum()}')
print(f'Shape: {df_clean.shape}')
```

```text
결측치 처리 후: 0
Shape: (43824, 13)
```

## A2. 범주형 변수 인코딩

`cbwd` (풍향) 컬럼을 인코딩

```python
print('cbwd 고유값:', df_clean['cbwd'].unique())
print('cbwd 분포:')
print(df_clean['cbwd'].value_counts())

# One-Hot 인코딩
df_clean = pd.get_dummies(df_clean, columns=['cbwd'], dtype=int)
print('\nOne-Hot 인코딩 후 컬럼:')
print([c for c in df_clean.columns if 'cbwd' in c])
```

```text
cbwd 고유값: <StringArray>
['NW', 'cv', 'NE', 'SE']
Length: 4, dtype: str
cbwd 분포:
cbwd
SE    15290
NW    14150
cv     9387
NE     4997
Name: count, dtype: int64

One-Hot 인코딩 후 컬럼:
['cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']
```

## A3. 시간 변수 처리

데이터에 이미 `year/month/day/hour` 컬럼이 있음. 요일, 주말 여부, 계절 등을 Feature로 생성

```python
# datetime 컬럼 생성
df_clean['datetime'] = pd.to_datetime(df_clean[['year', 'month', 'day', 'hour']])
df_clean['dayofweek']  = df_clean['datetime'].dt.dayofweek
df_clean['is_weekend'] = (df_clean['dayofweek'] >= 5).astype(int)

# 불필요한 컬럼 제거
df_final = df_clean.drop(columns=['No', 'datetime'])

display('최종 컬럼:', df_final.columns.tolist())
print('Shape:', df_final.shape)
```

```text
'최종 컬럼:'
```

```text
['year',
 'month',
 'day',
 'hour',
 'pm2.5',
 'DEWP',
 'TEMP',
 'PRES',
 'Iws',
 'Is',
 'Ir',
 'cbwd_NE',
 'cbwd_NW',
 'cbwd_SE',
 'cbwd_cv',
 'dayofweek',
 'is_weekend']
```

```text
Shape: (43824, 17)
```

## A4. Train/Val/Test 3분할 + 정규화

- 60% / 20% / 20% 비율로 3분할
- **반드시 `random_state=SEED`** 사용 (본인 학번 기반)
- StandardScaler로 정규화 (train에 fit, val/test는 transform만)

**출력**:
- X_train, X_val, X_test의 shape

```python
# X, y 분리
y = df_final['pm2.5'].values.astype(np.float32)
X = df_final.drop(columns=['pm2.5']).values.astype(np.float32)

print(f'X: {X.shape}, y: {y.shape}')
print(f'타겟 분포: min={y.min():.1f}, max={y.max():.1f}, mean={y.mean():.1f}')

# 3분할 (60/20/20)
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=SEED)
# 0.25 of 0.8 = 0.2 → 최종 60/20/20

print(f'\nTrain: {X_train.shape} ({len(X_train)/len(X):.0%})')
print(f'Val  : {X_val.shape} ({len(X_val)/len(X):.0%})')
print(f'Test : {X_test.shape} ({len(X_test)/len(X):.0%})')

# 정규화 (train에 fit, val/test는 transform만)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)
X_test  = scaler.transform(X_test)

print('\n정규화 완료')
```

```text
X: (43824, 16), y: (43824,)
타겟 분포: min=0.0, max=994.0, mean=97.8

Train: (26294, 16) (60%)
Val  : (8765, 16) (20%)
Test : (8765, 16) (20%)

정규화 완료
```

---
'''
# (추가입니다_ B0 EDA 심화)

    ## 0-1. 현재까지 상황정리 : 
        target: pm2.5 = 연속형 target

        numeric feature: year, month, day, hour, DEWP, TEMP, PRES, Iws, Is, Ir, dayofweek

        binary / dummy feature: cbwd_NE, cbwd_NW, cbwd_SE, cbwd_cv, is_weekend

    /단, month, hour, dayofweek는 숫자로 되어 있지만 coninuos 가 아닌보다는 categorical에 가까운 변수임에 유의.

**1. fix_train**:
- train 데이터 기준 fix. test 데이터까지 보고 가설을 세우면 간접적인 leakage. #시간 순서 split

**2. Target 중심 가설 설계**: 기본 target은 pm2.5 
- Q1. 수치형 기상 변수는 PM2.5와 선형 상관이 있는가?
    - numeric_features = ['DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir']
    - H0: feature와 pm2.5 사이의 Pearson 상관계수는 0이다. 즉, 선형 상관관계가 없다.
    - H1: feature와 pm2.5 사이의 Pearson 상관계수는 0이 아니다.
    즉, 선형 상관관계가 있다.
    - p-value < 0.05: 귀무가설 기각. 해당 feature와 pm2.5 사이에 통계적으로 유의한 상관관계가 있다고 판단.
    - p-value >= 0.05: 귀무가설 기각 실패. 상관관계가 있다고 보기 어렵다.
    - corr > 0:
    feature가 커질수록 pm2.5도 증가하는 경향.
    - corr < 0:
    feature가 커질수록 pm2.5는 감소하는 경향.
    - abs(corr)가 클수록 관계 강도가 큼.

- Q2. 월별 PM2.5 평균은 같은가? -> month는 범주형에 가까우므로, 따라서 Pearson + groupby/boxplot/ANOVA
    - time_features = ['year', 'month', 'day', 'hour', 'dayofweek', 'is_weekend']
    - H0: 모든 월의 평균 pm2.5는 같다.
    - H1: 적어도 하나의 월은 평균 pm2.5가 다르다.
    - p-value < 0.05이면 월별 PM2.5 평균이 모두 같다는 귀무가설을 기각한다.
    - 즉, PM2.5에는 계절성 또는 월별 패턴이 있다고 볼 수 있다.

- Q3. 풍향 dummy(one-hot)와 PM2.5의 상관성.
    - dummy_features = ['cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']
    - 각각은 0/1 binary feature임으로 따라서 각 dummy에 대해 다음 H0와 H1을 검정할 수 있다.
    - H0: 해당 풍향 여부에 따라 pm2.5 평균은 다르지 않다.
    - H1: 해당 풍향 여부에 따라 pm2.5 평균은 다르다.
  

**3. feature끼리의 상관성 파악**: feature 간 중복성 확인목적

- numeric_features_for_corr = ['year', 'month', 'day', 'hour', 'DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir', 'dayofweek']
    - H0: 두 numeric feature 사이의 Pearson 상관계수는 0이다.
    - H1: 두 numeric feature 사이의 Pearson 상관계수는 0이 아니다.
    - EX) H0: DEWP와 TEMP 사이의 선형 상관은 없다. H1: DEWP와 TEMP 사이의 선형 상관이 있다.

```python
print(' === 2단계 : Train 데이터 기준 Target 중심 EDA 가설 설정 ===')

target = 'pm2.5'

numeric_features = ['DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir']
time_features = ['year', 'month', 'day', 'hour', 'dayofweek', 'is_weekend']
wind_dummy_features = ['cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']

print('target:', target)
print('numeric_features:', numeric_features)
print('time_features:', time_features)
print('wind_dummy_features:', wind_dummy_features)
```

```text
 === 2단계 : Train 데이터 기준 Target 중심 EDA 가설 설정 ===
target: pm2.5
numeric_features: ['DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir']
time_features: ['year', 'month', 'day', 'hour', 'dayofweek', 'is_weekend']
wind_dummy_features: ['cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']
```

```python
from scipy.stats import pearsonr, spearmanr
from scipy.stats import ttest_ind, f_oneway, chi2_contingency
from scipy.stats import kruskal, mannwhitneyu


target = 'pm2.5'
numeric_weather_features = ['DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir']
time_numeric_features = ['year', 'month', 'day', 'hour', 'dayofweek']
binary_features = ['cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv', 'is_weekend']
all_numeric_for_corr = [
    'year', 'month', 'day', 'hour',
    'DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir',
    'dayofweek'
]

wind_dummy_features = ['cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']

print('target:', target)
print('numeric_weather_features:', numeric_weather_features)
print('time_numeric_features:', time_numeric_features)
print('binary_features:', binary_features)
print('all_numeric_for_corr:', all_numeric_for_corr)

print('\n결측치 총 개수:', df_clean.isnull().sum().sum())
print('shape:', df_clean.shape)
display(df_clean.head())
display(df_clean.tail())
# 'cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv'의 값 비율 확인
for col in wind_dummy_features:
    ratio = df_clean[col].mean()
    display(f"{col} 날씨비율 : {ratio:.4f} ({ratio*100:.2f}%)")
```

```text
target: pm2.5
numeric_weather_features: ['DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir']
time_numeric_features: ['year', 'month', 'day', 'hour', 'dayofweek']
binary_features: ['cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv', 'is_weekend']
all_numeric_for_corr: ['year', 'month', 'day', 'hour', 'DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir', 'dayofweek']
```

```text

결측치 총 개수: 0
shape: (43824, 19)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>No</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>hour</th>
      <th>pm2.5</th>
      <th>DEWP</th>
      <th>TEMP</th>
      <th>PRES</th>
      <th>Iws</th>
      <th>Is</th>
      <th>Ir</th>
      <th>cbwd_NE</th>
      <th>cbwd_NW</th>
      <th>cbwd_SE</th>
      <th>cbwd_cv</th>
      <th>datetime</th>
      <th>dayofweek</th>
      <th>is_weekend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>129.0</td>
      <td>-21</td>
      <td>-11.0</td>
      <td>1021.0</td>
      <td>1.79</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2010-01-01 00:00:00</td>
      <td>4</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>129.0</td>
      <td>-21</td>
      <td>-12.0</td>
      <td>1020.0</td>
      <td>4.92</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2010-01-01 01:00:00</td>
      <td>4</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>129.0</td>
      <td>-21</td>
      <td>-11.0</td>
      <td>1019.0</td>
      <td>6.71</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2010-01-01 02:00:00</td>
      <td>4</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>129.0</td>
      <td>-21</td>
      <td>-14.0</td>
      <td>1019.0</td>
      <td>9.84</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2010-01-01 03:00:00</td>
      <td>4</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>2010</td>
      <td>1</td>
      <td>1</td>
      <td>4</td>
      <td>129.0</td>
      <td>-20</td>
      <td>-12.0</td>
      <td>1018.0</td>
      <td>12.97</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2010-01-01 04:00:00</td>
      <td>4</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>No</th>
      <th>year</th>
      <th>month</th>
      <th>day</th>
      <th>hour</th>
      <th>pm2.5</th>
      <th>DEWP</th>
      <th>TEMP</th>
      <th>PRES</th>
      <th>Iws</th>
      <th>Is</th>
      <th>Ir</th>
      <th>cbwd_NE</th>
      <th>cbwd_NW</th>
      <th>cbwd_SE</th>
      <th>cbwd_cv</th>
      <th>datetime</th>
      <th>dayofweek</th>
      <th>is_weekend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>43819</th>
      <td>43820</td>
      <td>2014</td>
      <td>12</td>
      <td>31</td>
      <td>19</td>
      <td>8.0</td>
      <td>-23</td>
      <td>-2.0</td>
      <td>1034.0</td>
      <td>231.97</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2014-12-31 19:00:00</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>43820</th>
      <td>43821</td>
      <td>2014</td>
      <td>12</td>
      <td>31</td>
      <td>20</td>
      <td>10.0</td>
      <td>-22</td>
      <td>-3.0</td>
      <td>1034.0</td>
      <td>237.78</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2014-12-31 20:00:00</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>43821</th>
      <td>43822</td>
      <td>2014</td>
      <td>12</td>
      <td>31</td>
      <td>21</td>
      <td>10.0</td>
      <td>-22</td>
      <td>-3.0</td>
      <td>1034.0</td>
      <td>242.70</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2014-12-31 21:00:00</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>43822</th>
      <td>43823</td>
      <td>2014</td>
      <td>12</td>
      <td>31</td>
      <td>22</td>
      <td>8.0</td>
      <td>-22</td>
      <td>-4.0</td>
      <td>1034.0</td>
      <td>246.72</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2014-12-31 22:00:00</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>43823</th>
      <td>43824</td>
      <td>2014</td>
      <td>12</td>
      <td>31</td>
      <td>23</td>
      <td>12.0</td>
      <td>-21</td>
      <td>-3.0</td>
      <td>1034.0</td>
      <td>249.85</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>2014-12-31 23:00:00</td>
      <td>2</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>

```text
'cbwd_NE 날씨비율 : 0.1140 (11.40%)'
```

```text
'cbwd_NW 날씨비율 : 0.3229 (32.29%)'
```

```text
'cbwd_SE 날씨비율 : 0.3489 (34.89%)'
```

```text
'cbwd_cv 날씨비율 : 0.2142 (21.42%)'
```

```python
print(' === B0-1. Train/Test 시간순 Split ===')
df_eda = df_clean.copy()
#시간 순서 정렬 : 과거데이터(2010-2013)을 바탕으로 미래데이터(test. 2014를 예측한다)
df_eda = df_eda.sort_values(['year', 'month', 'day', 'hour']).reset_index(drop=True)

train_df = df_eda[df_eda['year'] <= 2013].copy()
test_df = df_eda[df_eda['year'] == 2014].copy()

# train_size = int(len(df_eda) * 0.8) ,split 8:2시 35063  2013     12   31    23 에서 분기되는 것을 확인- 즉 기존 train+val : test 를 비율로 나눈것과 연도별 2010~2013:2014 마진은 동일함. // 단 확실하게 하기 위해 세부 연도별 분할

print(f'df_eda shape: {df_eda.shape}')
print(f'train_df shape: {train_df.shape}')
print(f'test_df shape: {test_df.shape}')

print('\nTrain 기간:')
print(train_df[['year', 'month', 'day', 'hour']].head(1))
print(train_df[['year', 'month', 'day', 'hour']].tail(1))

print('\nTest 기간:')
print(test_df[['year', 'month', 'day', 'hour']].head(1))
print(test_df[['year', 'month', 'day', 'hour']].tail(1))

print(' === “과거 4년으로 학습해서 다음 1년을 예측한다” ===')
```

```text
 === B0-1. Train/Test 시간순 Split ===
df_eda shape: (43824, 19)
train_df shape: (35064, 19)
test_df shape: (8760, 19)

Train 기간:
   year  month  day  hour
0  2010      1    1     0
       year  month  day  hour
35063  2013     12   31    23

Test 기간:
       year  month  day  hour
35064  2014      1    1     0
       year  month  day  hour
43823  2014     12   31    23
 === “과거 4년으로 학습해서 다음 1년을 예측한다” ===
```

```python
print('== 2-1 단계 : Target(pm2.5) 분포 확인 ===')
print('= RQ0. pm2.5는 정규분포에 가까운가, 아니면 고농도 outlier가 많은 분포인가? =')

target_desc = train_df[target].describe(
    percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
)

display(target_desc)

print(f"skewness: {train_df[target].skew():.4f}")
print(f"kurtosis: {train_df[target].kurtosis():.4f}")

plt.figure(figsize=(8, 4))
plt.hist(train_df[target], bins=60)
plt.title('Distribution of PM2.5 - Train')
plt.xlabel('pm2.5')
plt.ylabel('count')
plt.show()

plt.figure(figsize=(8, 4))
plt.boxplot(train_df[target], vert=False)
plt.title('Boxplot of PM2.5 - Train')
plt.xlabel('pm2.5')
plt.show()

print('해석:')
print('pm2.5는 평균이 중앙값보다 크고, skewness가 1.83으로 양의 왜도가 크다.')
print('또한 75% 값은 137이지만 95%는 279, 99%는 417, 최대값은 994로 오른쪽 꼬리가 길다.')
print('따라서 pm2.5는 정규분포라기보다 고농도 outlier가 많은 -즉, 특정 시간대나 계절·기상 조건에서 고농도 episode가 발생하는 데이터이다.')
print('모델링에서는 MSE만 보면 고농도 오차에 크게 끌릴 수 있으므로 MAE, RMSE, log1p 변환, 고농도 여부 분류 등을 함께 고려할 필요가 있다.')
print('=== 이때, outlier는 단순 오류라기보다 실제 대기오염 고농도 사건일 수 있다. 따라서 무조건 제거하면 안 된다. 이 데이터에서는 고농도 구간 자체가 중요한 예측 대상으로 판단될 수 있다.')
```

```text
== 2-1 단계 : Target(pm2.5) 분포 확인 ===
= RQ0. pm2.5는 정규분포에 가까운가, 아니면 고농도 outlier가 많은 분포인가? =
```

```text
count    35064.000000
mean        97.782883
std         90.748846
min          0.000000
1%           6.000000
5%          10.000000
25%         29.000000
50%         72.000000
75%        137.000000
95%        279.000000
99%        417.000000
max        994.000000
Name: pm2.5, dtype: float64
```

```text
skewness: 1.8345
kurtosis: 5.3810
```

![output](assets/3085_problem2_cell019_out03_img01.png)

![output](assets/3085_problem2_cell019_out04_img02.png)

```text
해석:
pm2.5는 평균이 중앙값보다 크고, skewness가 1.83으로 양의 왜도가 크다.
또한 75% 값은 137이지만 95%는 279, 99%는 417, 최대값은 994로 오른쪽 꼬리가 길다.
따라서 pm2.5는 정규분포라기보다 고농도 outlier가 많은 -즉, 특정 시간대나 계절·기상 조건에서 고농도 episode가 발생하는 데이터이다.
모델링에서는 MSE만 보면 고농도 오차에 크게 끌릴 수 있으므로 MAE, RMSE, log1p 변환, 고농도 여부 분류 등을 함께 고려할 필요가 있다.
=== 이때, outlier는 단순 오류라기보다 실제 대기오염 고농도 사건일 수 있다. 따라서 무조건 제거하면 안 된다. 이 데이터에서는 고농도 구간 자체가 중요한 예측 대상으로 판단될 수 있다.
```

```python
print('=== 연속형 기상 feature ↔ 연속형 target ===')
corr_rows = []

for col in numeric_weather_features:
    pearson_corr, pearson_p = pearsonr(train_df[col], train_df[target])
    spearman_corr, spearman_p = spearmanr(train_df[col], train_df[target])

    corr_rows.append({
        'feature': col,
        'variable_type': 'continuous-continuous',
        'test': 'Pearson / Spearman',
        'pearson_direction': 'positive' if pearson_corr > 0 else 'negative',
        'pearson_decision_0.05': 'reject H0' if pearson_p < 0.05 else 'fail to reject H0',
        'pearson_corr': pearson_corr,
        'pearson_p_value': pearson_p,
        'spearman_corr': spearman_corr,
        'spearman_p_value': spearman_p,
        'abs_pearson': abs(pearson_corr),
        'abs_spearman': abs(spearman_corr),
        'pearson_direction': 'positive' if pearson_corr > 0 else 'negative',
        'pearson_decision_0.05': 'reject H0' if pearson_p < 0.05 else 'fail to reject H0',
        'H0': f'{col}과 target 사이의 관계는 없다.',
        'H1': f'{col}과 target 사이의 관계는 있다.'
    })

corr_result = pd.DataFrame(corr_rows)
corr_result = corr_result.sort_values('abs_spearman', ascending=False)

display(corr_result)

print(' === 시각화 1: 상관계수 bar plot. ===')
plot_df = corr_result.sort_values('spearman_corr')

plt.figure(figsize=(8, 4))
plt.barh(plot_df['feature'], plot_df['spearman_corr'])
plt.axvline(0)
plt.title('Spearman Correlation with PM2.5')
plt.xlabel('Spearman correlation')
plt.ylabel('feature')
plt.show()

print(' === 2: 연속형 feature별 scatter plot ===')
for col in numeric_weather_features:
    plt.figure(figsize=(6, 4))
    plt.scatter(train_df[col], train_df[target], alpha=0.15, s=8)
    plt.title(f'{col} vs PM2.5')
    plt.xlabel(col)
    plt.ylabel('pm2.5')
    plt.show()


print('해석:')
print('Iws는 pm2.5와 가장 강한 음의 상관을 보인다. 누적 풍속이 커질수록 PM2.5가 낮아지는 경향이 있다.')
print('DEWP는 pm2.5와 비교적 뚜렷한 양의 상관을 보인다. 이슬점이 높을수록 PM2.5가 높아지는 경향이 있다.')
print('PRES는 약한 음의 상관을 보인다.')
print('TEMP는 Pearson과 Spearman의 방향이 달라 단순 선형 관계로 해석하기 어렵다.')
print('Is와 Ir는 통계적으로 유의하거나 일부 유의하더라도 상관 강도가 매우 약하므로 주요 feature로 보기는 어렵다.')
print('대규모 데이터에서는 p-value보다 correlation의 절대값과 시각적 패턴을 함께 해석해야 한다.')
```

```text
=== 연속형 기상 feature ↔ 연속형 target ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature</th>
      <th>variable_type</th>
      <th>test</th>
      <th>pearson_direction</th>
      <th>pearson_decision_0.05</th>
      <th>pearson_corr</th>
      <th>pearson_p_value</th>
      <th>spearman_corr</th>
      <th>spearman_p_value</th>
      <th>abs_pearson</th>
      <th>abs_spearman</th>
      <th>H0</th>
      <th>H1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3</th>
      <td>Iws</td>
      <td>continuous-continuous</td>
      <td>Pearson / Spearman</td>
      <td>negative</td>
      <td>reject H0</td>
      <td>-0.249642</td>
      <td>0.000000e+00</td>
      <td>-0.358043</td>
      <td>0.000000e+00</td>
      <td>0.249642</td>
      <td>0.358043</td>
      <td>Iws과 target 사이의 관계는 없다.</td>
      <td>Iws과 target 사이의 관계는 있다.</td>
    </tr>
    <tr>
      <th>0</th>
      <td>DEWP</td>
      <td>continuous-continuous</td>
      <td>Pearson / Spearman</td>
      <td>positive</td>
      <td>reject H0</td>
      <td>0.201941</td>
      <td>2.142763e-319</td>
      <td>0.331976</td>
      <td>0.000000e+00</td>
      <td>0.201941</td>
      <td>0.331976</td>
      <td>DEWP과 target 사이의 관계는 없다.</td>
      <td>DEWP과 target 사이의 관계는 있다.</td>
    </tr>
    <tr>
      <th>2</th>
      <td>PRES</td>
      <td>continuous-continuous</td>
      <td>Pearson / Spearman</td>
      <td>negative</td>
      <td>reject H0</td>
      <td>-0.092107</td>
      <td>6.270519e-67</td>
      <td>-0.189042</td>
      <td>1.933085e-279</td>
      <td>0.092107</td>
      <td>0.189042</td>
      <td>PRES과 target 사이의 관계는 없다.</td>
      <td>PRES과 target 사이의 관계는 있다.</td>
    </tr>
    <tr>
      <th>1</th>
      <td>TEMP</td>
      <td>continuous-continuous</td>
      <td>Pearson / Spearman</td>
      <td>negative</td>
      <td>reject H0</td>
      <td>-0.044800</td>
      <td>4.743388e-17</td>
      <td>0.064146</td>
      <td>2.675477e-33</td>
      <td>0.044800</td>
      <td>0.064146</td>
      <td>TEMP과 target 사이의 관계는 없다.</td>
      <td>TEMP과 target 사이의 관계는 있다.</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Is</td>
      <td>continuous-continuous</td>
      <td>Pearson / Spearman</td>
      <td>positive</td>
      <td>reject H0</td>
      <td>0.023158</td>
      <td>1.444966e-05</td>
      <td>0.046936</td>
      <td>1.449028e-18</td>
      <td>0.023158</td>
      <td>0.046936</td>
      <td>Is과 target 사이의 관계는 없다.</td>
      <td>Is과 target 사이의 관계는 있다.</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Ir</td>
      <td>continuous-continuous</td>
      <td>Pearson / Spearman</td>
      <td>negative</td>
      <td>reject H0</td>
      <td>-0.048251</td>
      <td>1.563929e-19</td>
      <td>0.006044</td>
      <td>2.577713e-01</td>
      <td>0.048251</td>
      <td>0.006044</td>
      <td>Ir과 target 사이의 관계는 없다.</td>
      <td>Ir과 target 사이의 관계는 있다.</td>
    </tr>
  </tbody>
</table>
</div>

```text
 === 시각화 1: 상관계수 bar plot. ===
```

![output](assets/3085_problem2_cell020_out03_img03.png)

```text
 === 2: 연속형 feature별 scatter plot ===
```

![output](assets/3085_problem2_cell020_out05_img04.png)

![output](assets/3085_problem2_cell020_out06_img05.png)

![output](assets/3085_problem2_cell020_out07_img06.png)

![output](assets/3085_problem2_cell020_out08_img07.png)

![output](assets/3085_problem2_cell020_out09_img08.png)

![output](assets/3085_problem2_cell020_out10_img09.png)

```text
해석:
Iws는 pm2.5와 가장 강한 음의 상관을 보인다. 누적 풍속이 커질수록 PM2.5가 낮아지는 경향이 있다.
DEWP는 pm2.5와 비교적 뚜렷한 양의 상관을 보인다. 이슬점이 높을수록 PM2.5가 높아지는 경향이 있다.
PRES는 약한 음의 상관을 보인다.
TEMP는 Pearson과 Spearman의 방향이 달라 단순 선형 관계로 해석하기 어렵다.
Is와 Ir는 통계적으로 유의하거나 일부 유의하더라도 상관 강도가 매우 약하므로 주요 feature로 보기는 어렵다.
대규모 데이터에서는 p-value보다 correlation의 절대값과 시각적 패턴을 함께 해석해야 한다.
```

| feature | Pearson | Spearman | 해석                                                |
| ------- | ------: | -------: | ------------------------------------------------- |
| `Iws`   |  -0.250 |   -0.358 | 가장 강한 음의 관계. 누적 풍속이 클수록 PM2.5가 낮아지는 경향            |
| `DEWP`  |   0.202 |    0.332 | 이슬점이 높을수록 PM2.5가 높아지는 경향                          |
| `PRES`  |  -0.092 |   -0.189 | 약한 음의 관계                                          |
| `TEMP`  |  -0.045 |    0.064 | 매우 약함. Pearson/Spearman 부호가 달라 단순 선형관계로 보기 어렵다    |
| `Is`    |   0.023 |    0.047 | 통계적으로는 유의하나 실질적 관계는 매우 약함                         |
| `Ir`    |  -0.048 |    0.006 | Spearman p-value가 0.2577로 유의하지 않음. 실질적으로 거의 관계 없음 |

```python
print(' === scatter plot 개선 - 원본 target vs log1p target ===')
print('원본 pm2.5 scatter는 고농도 outlier 때문에 낮은 구간의 구조가 잘 보이지 않을 수 있다.')

# log1p target 생성
# log1p(x) = log(1+x)
# pm2.5에 0이 있으므로 log(x)보다 log1p(x)가 안전하다.
train_df['pm2.5_log1p'] = np.log1p(train_df[target])

# 시각화용 샘플
train_sample = train_df.sample(
    n=min(5000, len(train_df)),
    random_state=3085
)

for col in numeric_weather_features:
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.scatter(train_sample[col], train_sample[target], alpha=0.15, s=8)
    plt.title(f'{col} vs PM2.5')
    plt.xlabel(col)
    plt.ylabel('pm2.5')
    
    plt.subplot(1, 2, 2)
    plt.scatter(train_sample[col], train_sample['pm2.5_log1p'], alpha=0.15, s=8)
    plt.title(f'{col} vs log1p(PM2.5)')
    plt.xlabel(col)
    plt.ylabel('log1p(pm2.5)')
    
    plt.tight_layout()
    plt.show()
```

```text
 === scatter plot 개선 - 원본 target vs log1p target ===
원본 pm2.5 scatter는 고농도 outlier 때문에 낮은 구간의 구조가 잘 보이지 않을 수 있다.
```

![output](assets/3085_problem2_cell022_out01_img10.png)

![output](assets/3085_problem2_cell022_out02_img11.png)

![output](assets/3085_problem2_cell022_out03_img12.png)

![output](assets/3085_problem2_cell022_out04_img13.png)

![output](assets/3085_problem2_cell022_out05_img14.png)

![output](assets/3085_problem2_cell022_out06_img15.png)

```python
print(' === month별 주요 feature 상관계수 ===')

month_corr_rows = []

for month_value, group in train_df.groupby('month'):
    for col in ['Iws', 'DEWP', 'PRES', 'TEMP']:
        if group[col].nunique() > 1 and group[target].nunique() > 1:
            pearson_corr, pearson_p = pearsonr(group[col], group[target])
            spearman_corr, spearman_p = spearmanr(group[col], group[target])
            
            month_corr_rows.append({
                'month': month_value,
                'feature': col,
                'pearson_corr': pearson_corr,
                'pearson_p_value': pearson_p,
                'spearman_corr': spearman_corr,
                'spearman_p_value': spearman_p
            })

month_corr_result = pd.DataFrame(month_corr_rows)

display(month_corr_result.sort_values(['feature', 'month']))

print(' === B4-9-3단계 : month별 Spearman correlation 변화 ===')

for col in ['Iws', 'DEWP', 'PRES', 'TEMP']:
    temp_plot = month_corr_result[month_corr_result['feature'] == col]
    
    plt.figure(figsize=(8, 4))
    plt.plot(temp_plot['month'], temp_plot['spearman_corr'], marker='o')
    plt.axhline(0)
    plt.title(f'Monthly Spearman correlation: {col} vs pm2.5')
    plt.xlabel('month')
    plt.ylabel('Spearman correlation')
    plt.xticks(range(1, 13))
    plt.show()
```

```text
 === month별 주요 feature 상관계수 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month</th>
      <th>feature</th>
      <th>pearson_corr</th>
      <th>pearson_p_value</th>
      <th>spearman_corr</th>
      <th>spearman_p_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>DEWP</td>
      <td>0.655966</td>
      <td>0.000000e+00</td>
      <td>0.730731</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2</td>
      <td>DEWP</td>
      <td>0.622824</td>
      <td>3.356228e-291</td>
      <td>0.727386</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>9</th>
      <td>3</td>
      <td>DEWP</td>
      <td>0.682816</td>
      <td>0.000000e+00</td>
      <td>0.778685</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>13</th>
      <td>4</td>
      <td>DEWP</td>
      <td>0.591549</td>
      <td>1.776868e-271</td>
      <td>0.645639</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>17</th>
      <td>5</td>
      <td>DEWP</td>
      <td>0.575635</td>
      <td>2.952901e-262</td>
      <td>0.652309</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>21</th>
      <td>6</td>
      <td>DEWP</td>
      <td>0.524983</td>
      <td>9.003273e-204</td>
      <td>0.545665</td>
      <td>3.435663e-223</td>
    </tr>
    <tr>
      <th>25</th>
      <td>7</td>
      <td>DEWP</td>
      <td>0.599467</td>
      <td>6.637310e-290</td>
      <td>0.640294</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>29</th>
      <td>8</td>
      <td>DEWP</td>
      <td>0.412377</td>
      <td>1.499189e-122</td>
      <td>0.468686</td>
      <td>2.061305e-162</td>
    </tr>
    <tr>
      <th>33</th>
      <td>9</td>
      <td>DEWP</td>
      <td>0.526335</td>
      <td>5.323977e-205</td>
      <td>0.650071</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>37</th>
      <td>10</td>
      <td>DEWP</td>
      <td>0.589943</td>
      <td>1.404251e-278</td>
      <td>0.622828</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>41</th>
      <td>11</td>
      <td>DEWP</td>
      <td>0.466171</td>
      <td>2.368741e-155</td>
      <td>0.563833</td>
      <td>2.092976e-241</td>
    </tr>
    <tr>
      <th>45</th>
      <td>12</td>
      <td>DEWP</td>
      <td>0.698190</td>
      <td>0.000000e+00</td>
      <td>0.721195</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Iws</td>
      <td>-0.303491</td>
      <td>1.902943e-64</td>
      <td>-0.571587</td>
      <td>8.768334e-258</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2</td>
      <td>Iws</td>
      <td>-0.262557</td>
      <td>5.385522e-44</td>
      <td>-0.437323</td>
      <td>4.276466e-127</td>
    </tr>
    <tr>
      <th>8</th>
      <td>3</td>
      <td>Iws</td>
      <td>-0.325823</td>
      <td>1.491661e-74</td>
      <td>-0.434085</td>
      <td>4.952302e-137</td>
    </tr>
    <tr>
      <th>12</th>
      <td>4</td>
      <td>Iws</td>
      <td>-0.266443</td>
      <td>5.305787e-48</td>
      <td>-0.281023</td>
      <td>2.037017e-53</td>
    </tr>
    <tr>
      <th>16</th>
      <td>5</td>
      <td>Iws</td>
      <td>-0.230051</td>
      <td>4.847474e-37</td>
      <td>-0.261836</td>
      <td>7.582088e-48</td>
    </tr>
    <tr>
      <th>20</th>
      <td>6</td>
      <td>Iws</td>
      <td>-0.032819</td>
      <td>7.824396e-02</td>
      <td>-0.041579</td>
      <td>2.565742e-02</td>
    </tr>
    <tr>
      <th>24</th>
      <td>7</td>
      <td>Iws</td>
      <td>0.021838</td>
      <td>2.336685e-01</td>
      <td>-0.030784</td>
      <td>9.314826e-02</td>
    </tr>
    <tr>
      <th>28</th>
      <td>8</td>
      <td>Iws</td>
      <td>-0.088496</td>
      <td>1.330553e-06</td>
      <td>-0.134485</td>
      <td>1.745850e-13</td>
    </tr>
    <tr>
      <th>32</th>
      <td>9</td>
      <td>Iws</td>
      <td>-0.119653</td>
      <td>1.182139e-10</td>
      <td>-0.213316</td>
      <td>5.437184e-31</td>
    </tr>
    <tr>
      <th>36</th>
      <td>10</td>
      <td>Iws</td>
      <td>-0.286221</td>
      <td>3.224704e-57</td>
      <td>-0.410410</td>
      <td>2.729106e-121</td>
    </tr>
    <tr>
      <th>40</th>
      <td>11</td>
      <td>Iws</td>
      <td>-0.330894</td>
      <td>1.517585e-74</td>
      <td>-0.576355</td>
      <td>1.233498e-254</td>
    </tr>
    <tr>
      <th>44</th>
      <td>12</td>
      <td>Iws</td>
      <td>-0.330468</td>
      <td>9.147425e-77</td>
      <td>-0.551940</td>
      <td>6.180842e-237</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>PRES</td>
      <td>-0.359359</td>
      <td>2.055598e-91</td>
      <td>-0.443915</td>
      <td>6.034986e-144</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2</td>
      <td>PRES</td>
      <td>-0.462143</td>
      <td>1.363791e-143</td>
      <td>-0.579718</td>
      <td>2.483138e-243</td>
    </tr>
    <tr>
      <th>10</th>
      <td>3</td>
      <td>PRES</td>
      <td>-0.523856</td>
      <td>1.905183e-209</td>
      <td>-0.501778</td>
      <td>1.397011e-189</td>
    </tr>
    <tr>
      <th>14</th>
      <td>4</td>
      <td>PRES</td>
      <td>-0.210928</td>
      <td>2.530444e-30</td>
      <td>-0.229529</td>
      <td>9.666230e-36</td>
    </tr>
    <tr>
      <th>18</th>
      <td>5</td>
      <td>PRES</td>
      <td>0.030444</td>
      <td>9.681202e-02</td>
      <td>0.052991</td>
      <td>3.832595e-03</td>
    </tr>
    <tr>
      <th>22</th>
      <td>6</td>
      <td>PRES</td>
      <td>-0.059190</td>
      <td>1.483565e-03</td>
      <td>-0.033786</td>
      <td>6.985112e-02</td>
    </tr>
    <tr>
      <th>26</th>
      <td>7</td>
      <td>PRES</td>
      <td>0.206925</td>
      <td>3.845733e-30</td>
      <td>0.253175</td>
      <td>9.538661e-45</td>
    </tr>
    <tr>
      <th>30</th>
      <td>8</td>
      <td>PRES</td>
      <td>-0.086881</td>
      <td>2.068910e-06</td>
      <td>-0.092479</td>
      <td>4.333356e-07</td>
    </tr>
    <tr>
      <th>34</th>
      <td>9</td>
      <td>PRES</td>
      <td>-0.321208</td>
      <td>4.081724e-70</td>
      <td>-0.379980</td>
      <td>1.382537e-99</td>
    </tr>
    <tr>
      <th>38</th>
      <td>10</td>
      <td>PRES</td>
      <td>-0.255294</td>
      <td>1.706365e-45</td>
      <td>-0.174410</td>
      <td>9.328295e-22</td>
    </tr>
    <tr>
      <th>42</th>
      <td>11</td>
      <td>PRES</td>
      <td>-0.261056</td>
      <td>4.387960e-46</td>
      <td>-0.246425</td>
      <td>4.236283e-41</td>
    </tr>
    <tr>
      <th>46</th>
      <td>12</td>
      <td>PRES</td>
      <td>-0.250782</td>
      <td>6.533120e-44</td>
      <td>-0.281074</td>
      <td>3.689021e-55</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>TEMP</td>
      <td>0.035660</td>
      <td>5.175525e-02</td>
      <td>0.040759</td>
      <td>2.618140e-02</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2</td>
      <td>TEMP</td>
      <td>0.128931</td>
      <td>1.590977e-11</td>
      <td>0.133777</td>
      <td>2.654221e-12</td>
    </tr>
    <tr>
      <th>11</th>
      <td>3</td>
      <td>TEMP</td>
      <td>0.061545</td>
      <td>7.816634e-04</td>
      <td>0.026403</td>
      <td>1.498658e-01</td>
    </tr>
    <tr>
      <th>15</th>
      <td>4</td>
      <td>TEMP</td>
      <td>0.055016</td>
      <td>3.142649e-03</td>
      <td>0.080680</td>
      <td>1.458148e-05</td>
    </tr>
    <tr>
      <th>19</th>
      <td>5</td>
      <td>TEMP</td>
      <td>-0.041985</td>
      <td>2.199714e-02</td>
      <td>-0.046329</td>
      <td>1.148185e-02</td>
    </tr>
    <tr>
      <th>23</th>
      <td>6</td>
      <td>TEMP</td>
      <td>-0.002587</td>
      <td>8.896157e-01</td>
      <td>0.012292</td>
      <td>5.096531e-01</td>
    </tr>
    <tr>
      <th>27</th>
      <td>7</td>
      <td>TEMP</td>
      <td>-0.029316</td>
      <td>1.098395e-01</td>
      <td>-0.008684</td>
      <td>6.358292e-01</td>
    </tr>
    <tr>
      <th>31</th>
      <td>8</td>
      <td>TEMP</td>
      <td>0.026063</td>
      <td>1.551855e-01</td>
      <td>0.021602</td>
      <td>2.387663e-01</td>
    </tr>
    <tr>
      <th>35</th>
      <td>9</td>
      <td>TEMP</td>
      <td>0.139651</td>
      <td>5.146778e-14</td>
      <td>0.185146</td>
      <td>1.265727e-23</td>
    </tr>
    <tr>
      <th>39</th>
      <td>10</td>
      <td>TEMP</td>
      <td>0.038022</td>
      <td>3.807269e-02</td>
      <td>-0.027065</td>
      <td>1.399183e-01</td>
    </tr>
    <tr>
      <th>43</th>
      <td>11</td>
      <td>TEMP</td>
      <td>-0.127534</td>
      <td>6.451222e-12</td>
      <td>-0.096676</td>
      <td>2.013286e-07</td>
    </tr>
    <tr>
      <th>47</th>
      <td>12</td>
      <td>TEMP</td>
      <td>0.044216</td>
      <td>1.585391e-02</td>
      <td>0.115269</td>
      <td>2.851697e-10</td>
    </tr>
  </tbody>
</table>
</div>

```text
 === B4-9-3단계 : month별 Spearman correlation 변화 ===
```

![output](assets/3085_problem2_cell023_out03_img16.png)

![output](assets/3085_problem2_cell023_out04_img17.png)

![output](assets/3085_problem2_cell023_out05_img18.png)

![output](assets/3085_problem2_cell023_out06_img19.png)

```python
print(' === 핵심 feature Iws, DEWP 집중 분석 ===')

main_numeric_candidates = ['Iws', 'DEWP']

for col in main_numeric_candidates:
    print(f'\n=== {col} 집중 분석 ===')
    
    print(train_df[[col, target, 'pm2.5_log1p']].describe())
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.hexbin(train_df[col], train_df[target], gridsize=40, mincnt=1)
    plt.colorbar(label='count')
    plt.title(f'{col} vs PM2.5')
    plt.xlabel(col)
    plt.ylabel('pm2.5')
    
    plt.subplot(1, 2, 2)
    plt.hexbin(train_df[col], train_df['pm2.5_log1p'], gridsize=40, mincnt=1)
    plt.colorbar(label='count')
    plt.title(f'{col} vs log1p(PM2.5)')
    plt.xlabel(col)
    plt.ylabel('log1p(pm2.5)')
    
    plt.tight_layout()
    plt.show()

print(' ===  Iws와 DEWP의 2D 공간에서 pm2.5 보기 ===')

plt.figure(figsize=(7, 5))

scatter = plt.scatter(
    train_sample['Iws'],
    train_sample['DEWP'],
    c=train_sample[target],
    alpha=0.5,
    s=10
)

plt.colorbar(scatter, label='pm2.5')
plt.title('Iws vs DEWP colored by PM2.5')
plt.xlabel('Iws')
plt.ylabel('DEWP')
plt.show()


print('최종 결론:')
print('연속형 기상 feature 중 Iws와 DEWP가 pm2.5와 가장 뚜렷한 관계를 보인다.')
print('Iws는 음의 관계가 가장 강하며, 풍속이 커질수록 오염물질이 확산되어 PM2.5가 낮아지는 패턴으로 해석할 수 있다.')
print('DEWP는 양의 관계가 비교적 강하며, 습하거나 정체된 기상 조건에서 PM2.5가 높아지는 패턴으로 해석할 수 있다.')
```

```text
 === 핵심 feature Iws, DEWP 집중 분석 ===

=== Iws 집중 분석 ===
                Iws         pm2.5   pm2.5_log1p
count  35064.000000  35064.000000  35064.000000
mean      24.956033     97.782883      4.156130
std       51.300274     90.748846      1.005972
min        0.450000      0.000000      0.000000
25%        1.790000     29.000000      3.401197
50%        5.810000     72.000000      4.290459
75%       23.250000    137.000000      4.927254
max      585.600000    994.000000      6.902743
```

![output](assets/3085_problem2_cell024_out01_img20.png)

```text

=== DEWP 집중 분석 ===
               DEWP         pm2.5   pm2.5_log1p
count  35064.000000  35064.000000  35064.000000
mean       1.758556     97.782883      4.156130
std       14.499931     90.748846      1.005972
min      -33.000000      0.000000      0.000000
25%      -11.000000     29.000000      3.401197
50%        2.000000     72.000000      4.290459
75%       15.000000    137.000000      4.927254
max       28.000000    994.000000      6.902743
```

![output](assets/3085_problem2_cell024_out03_img21.png)

```text
 ===  Iws와 DEWP의 2D 공간에서 pm2.5 보기 ===
```

![output](assets/3085_problem2_cell024_out05_img22.png)

```text
최종 결론:
연속형 기상 feature 중 Iws와 DEWP가 pm2.5와 가장 뚜렷한 관계를 보인다.
Iws는 음의 관계가 가장 강하며, 풍속이 커질수록 오염물질이 확산되어 PM2.5가 낮아지는 패턴으로 해석할 수 있다.
DEWP는 양의 관계가 비교적 강하며, 습하거나 정체된 기상 조건에서 PM2.5가 높아지는 패턴으로 해석할 수 있다.
```

## **PM2.5 데이터 분포 및 주요 변수 요약**

- **PM2.5 분포 특성**
  - 이 데이터의 **PM2.5 값은 정규분포가 아니며**, episode(사건)가 포함된 **오른쪽으로 치우친 분포**를 가진다.

- **분석**
  - 따라서, **고농도 값을 단순 outlier로 간주해 제거하기보다는**  
    **모델이 중요한 이상치를 염두에 두고** 평가하는 것이 중요하다.

- **주요 기상 feature**
  - **연속형 기상 변수(feature) 중**
    - `Iws`와 `DEWP`가 **PM2.5와 가장 밀접한 관계**를 보이는 1차 후보로 선정됨
    - `Iws`는 **음의 관계** (풍속↑ → PM2.5↓, 즉 풍속이 클수록 오염물질이 잘 흩어짐)
    - `DEWP`는 **양의 관계** (이슬점/습도↑ → PM2.5↑, 즉 습하거나 정체된 조건에서 고농도 발생)

- **월별, 계절 특이성**
  - **DEWP는 월별로 나눠도 PM2.5와 안정적으로 양의 상관**을 유지. 특히 DEWP는 단순히 “여름이라 높다/겨울이라 낮다” 수준이 아니라, 같은 월 안에서도 이슬점이 높을수록 PM2.5가 높아지는 경향이 나타남. 이는 이슬점이 높은 습한 대기 조건에서 PM2.5 농도가 높아지는 경향이 있음을 시사함. 핵심 feature 후보로 설정 가능.
  - **Iws는 계절에 따라 효과 강도가 달라지는 특성**을 보임. 이때 Iws는 전체적으로 PM2.5와 음의 관계를 보이며, 특히 겨울·가을에 그 관계가 강함. ->
즉 Iws의 효과는 누적 풍속이 PM2.5 확산 또는 저감과 관련될 가능성이 큼. 계절에 따라 달라지는 피처일 가능성이 있음.

- **후속 모델 설계 방향**
  - 이후 모델링에서는
    - **기상 feature뿐만 아니라**
    - **month / hour / cbwd(풍향 등) 구조까지** 포함하여
    - **시간적 패턴과 기상 조건이 함께 작동하는 PM2.5 예측 문제**로 설계하는 것이 바람직할 것으로 생각된다.

---
# Part B. Baseline 회귀 모델 + 과적합 유발 + 정규화를 통한 과적합 해결 시도 (6점)

## B1. Baseline 모델 구축 및 학습 (3점)

**요구사항**:
- DNN (Dense layer 4개 이상) Baseline 모델 구축
- 과적합을 유도하기 위해 train 데이터의 일부(최대 2000개)만 사용
- `keras.utils.set_random_seed(SEED)` 호출 후 모델 생성
- Adam optimizer, MSE loss, MAE metric
- validation_data로 X_val/y_val 사용
- epochs=50, batch_size=32

**필수 출력**:
- 최종 Train Loss, Val Loss
- Gap (Val - Train) 값

기본 feature:
DEWP, TEMP, PRES, Iws, Is, Ir

시간 feature:
month, hour, dayofweek, is_weekend

풍향 feature:
cbwd_NE, cbwd_NW, cbwd_SE
또는 tree 모델이면 cbwd dummy 전체 사용 가능

핵심 interaction 후보:
Iws × DEWP
Iws × month
DEWP × month
Iws × cbwd

## B1. EDA 기반 모델링 설계

B0 EDA 결과, target `pm2.5`는 평균이 중앙값보다 크고 오른쪽 꼬리가 긴 heavy-tail 분포로 확인되었다. 따라서 고농도 값을 단순 outlier로 제거하기보다, 모델이 고농도 episode를 얼마나 잘 예측하는지 평가해야 한다.

연속형 기상 feature 중에서는 `Iws`와 `DEWP`가 가장 중요한 1차 후보로 나타났다. `DEWP`는 전체 분석과 월별 분석 모두에서 PM2.5와 안정적인 양의 관계를 보였으므로, 비교적 선형적인 설명력을 가진 feature로 해석할 수 있다. 반면 `Iws`는 전체적으로 PM2.5와 음의 관계를 보였지만, 월별로 관계 강도가 달라졌으므로 비선형성 또는 시간 조건과의 상호작용 가능성이 있다.

따라서 본 모델링에서는 단순 선형 모델보다 hidden layer와 ReLU activation을 가진 DNN을 baseline으로 사용한다. DNN은 `DEWP`의 선형적 효과뿐 아니라 `Iws × month`, `Iws × cbwd`, `DEWP × TEMP`, `hour × weather` 같은 feature interaction을 내부 표현으로 학습할 수 있다.

모델링 기준은 다음과 같다.

| 항목 | 설계 |
|---|---|
| 문제 유형 | 회귀(regression) |
| 입력 X | 시간 변수, 기상 변수, 풍향 dummy, 주말 여부 |
| 출력 y | `pm2.5` |
| 출력층 | `Dense(1)` |
| 출력 activation | 없음(linear output) |
| loss | MSE |
| 보조 metric | MAE |
| optimizer | Adam |
| baseline 목적 | 정규화 전 기본 DNN의 train/val loss curve 확인 |
| 이후 비교 | Dropout, L2, EarlyStopping, BatchNorm 개별 적용 |

```python
print(' === B1-1. 공통 유틸 함수 정의 ===')

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 재고정
np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

input_dim = X_train.shape[1]

# B1 요구조건: train 데이터 일부, 최대 2000개만 사용하고 batch_size=32로 학습한다.
# Part C의 공정 비교를 위해 정규화 4개 모델도 같은 subset과 batch size를 사용한다.
TRAIN_SUBSET_SIZE = min(2000, len(X_train))
BATCH_SIZE = 32

rng = np.random.default_rng(SEED)
train_subset_idx = rng.choice(len(X_train), size=TRAIN_SUBSET_SIZE, replace=False)
train_subset_idx = np.sort(train_subset_idx)

X_train_fit = X_train[train_subset_idx]
y_train_fit = y_train[train_subset_idx]

print(f'input_dim: {input_dim}')
print(f'X_train shape: {X_train.shape}')
print(f'X_train_fit shape: {X_train_fit.shape}  # B1 max 2000 subset')
print(f'X_val shape: {X_val.shape}')
print(f'X_test shape: {X_test.shape}')
print(f'y_train shape: {y_train.shape}')
print(f'y_train_fit shape: {y_train_fit.shape}')
print(f'y_val shape: {y_val.shape}')
print(f'y_test shape: {y_test.shape}')
print(f'BATCH_SIZE: {BATCH_SIZE}')

def show_last_result(model_name, history):
    """
    history 객체에서 마지막 epoch의 train loss, val loss, gap을 출력한다.
    Part C 요구사항의 Train Loss, Val Loss, Gap 출력에 맞춘 함수.
    """
    train_loss = history.history['loss'][-1]
    val_loss = history.history['val_loss'][-1]
    gap = val_loss - train_loss
    
    print(f'[{model_name}]')
    print(f'Train Loss: {train_loss:.4f}')
    print(f'Val Loss  : {val_loss:.4f}')
    print(f'Gap       : {gap:.4f}')
    
    return {
        'model': model_name,
        'train_loss': train_loss,
        'val_loss': val_loss,
        'gap': gap,
        'epochs': len(history.history['loss'])
    }


def plot_loss_curve(history, title):
    """
    Train Loss와 Val Loss를 한 그래프에 시각화한다.
    Part B 요구사항: 제목, x축, y축, 범례 포함.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel('Loss (MSE)')
    plt.legend()
    plt.show()


def regression_eval(model, X_data, y_data, dataset_name='data'):
    """
    회귀 모델 평가용 함수.
    Keras evaluate의 loss/MAE 외에 RMSE, R²를 함께 계산한다.
    """
    y_pred = model.predict(X_data, verbose=0).reshape(-1)
    
    mae = mean_absolute_error(y_data, y_pred)
    mse = mean_squared_error(y_data, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_data, y_pred)
    
    print(f'=== {dataset_name} regression metrics ===')
    print(f'MAE : {mae:.4f}')
    print(f'MSE : {mse:.4f}')
    print(f'RMSE: {rmse:.4f}')
    print(f'R²  : {r2:.4f}')
    
    return {
        'dataset': dataset_name,
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2
    }
```

```text
 === B1-1. 공통 유틸 함수 정의 ===
input_dim: 16
X_train shape: (26294, 16)
X_train_fit shape: (2000, 16)  # B1 max 2000 subset
X_val shape: (8765, 16)
X_test shape: (8765, 16)
y_train shape: (26294,)
y_train_fit shape: (2000,)
y_val shape: (8765,)
y_test shape: (8765,)
BATCH_SIZE: 32
```

```python
print(' === B2. Baseline DNN 모델 학습 ===')
def build_baseline_model():
    model = Sequential()
    
    # Dense + ReLU
    # DEWP의 선형/준선형 효과와 Iws의 비선형 패턴을 hidden layer에서 함께 학습하게 한다.
    model.add(Dense(64, activation='relu', input_shape=(input_dim,)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    
    # 회귀 출력층: pm2.5는 연속값이므로 activation을 두지 않는다.
    model.add(Dense(1))
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    return model


baseline_model = build_baseline_model()

baseline_model.summary()

baseline_history = baseline_model.fit(
    X_train_fit, y_train_fit,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=BATCH_SIZE,
    verbose=0
)

baseline_result = show_last_result('Baseline', baseline_history) 

plot_loss_curve(baseline_history, 'Baseline DNN Loss Curve')
```

```text
 === B2. Baseline DNN 모델 학습 ===
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Model: "sequential"</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Layer (type)                    </span>┃<span style="font-weight: bold"> Output Shape           </span>┃<span style="font-weight: bold">       Param # </span>┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ dense (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)                   │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">64</span>)             │         <span style="color: #00af00; text-decoration-color: #00af00">1,088</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_1 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)                 │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">32</span>)             │         <span style="color: #00af00; text-decoration-color: #00af00">2,080</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_2 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)                 │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">16</span>)             │           <span style="color: #00af00; text-decoration-color: #00af00">528</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_3 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)                 │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">1</span>)              │            <span style="color: #00af00; text-decoration-color: #00af00">17</span> │
└─────────────────────────────────┴────────────────────────┴───────────────┘
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold"> Total params: </span><span style="color: #00af00; text-decoration-color: #00af00">3,713</span> (14.50 KB)
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold"> Trainable params: </span><span style="color: #00af00; text-decoration-color: #00af00">3,713</span> (14.50 KB)
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold"> Non-trainable params: </span><span style="color: #00af00; text-decoration-color: #00af00">0</span> (0.00 B)
</pre>

```text
[Baseline]
Train Loss: 3994.2639
Val Loss  : 5263.4839
Gap       : 1269.2200
```

![output](assets/3085_problem2_cell029_out07_img23.png)

## B2. Loss Curve 시각화 + 과적합 분석 (3점)

**요구사항**:
- Train Loss와 Val Loss를 한 그래프에 시각화
- 그래프 제목, x/y 축 라벨, 범례 모두 포함

**분석 (마크다운으로 작성)**:
- Loss curve를 보고 과적합이 발생했는지 판단하라
- 어떤 신호로 과적합을 판단했는지 설명

**모델링**:
- Baseline DNN은 Dense(64) → Dense(32) → Dense(16) → Dense(1) 구조로 구성했다.
- B1 요구조건에 맞춰 train 데이터 전체가 아니라 `X_train_fit/y_train_fit` 2000개 subset만 사용했고, `batch_size=32`로 학습했다.
- 입력 feature는 16개이고, target은 연속형 pm2.5이므로 출력층은 activation이 없는 Dense(1)로 두었다.
- Hidden layer에는 ReLU를 사용해 DEWP의 비교적 안정적인 관계와 Iws의 비선형 패턴을 함께 학습하도록 설계했다.

**분석**:
- Loss curve
    - train loss와 validation loss의 진행 방향을 함께 보고, 마지막 epoch 기준 Train Loss, Val Loss, Gap을 바로 위 B2 출력값으로 판단한다.
    - B1은 일부 train subset으로 과적합 가능성을 유도하는 실험이므로, 전체 train set 학습보다 train-validation gap이 커질 수 있다.
    - validation loss가 계속 내려가면 추가 학습 여지가 있고, validation loss가 상승하면 과적합 신호로 해석한다.

- Validation
    - MAE, RMSE, R²는 바로 위 validation prediction check의 최신 출력값을 기준으로 해석한다.
    - Actual vs Predicted와 residual plot에서는 모델이 전체 경향을 학습했는지, 예측값이 중앙 범위로 압축되는지, 고농도 구간을 과소예측하는지 확인한다.
    - 농도 구간별 오차 분석에서는 low/mid/high/extreme bin에서 MAE와 mean residual이 어떻게 달라지는지가 핵심이다.

**결론 및 향후 모델링 방향성**:
- Baseline DNN은 B1 요구조건을 만족하는 기준 모델이다.
- Part C에서는 Dropout, L2 Regularization, EarlyStopping, Batch Normalization을 같은 subset과 같은 batch size 조건에서 각각 개별 적용해 validation loss, train-validation gap, 고농도 구간 오차가 개선되는지 비교한다.

```python
print(' === B2-1. Baseline Loss Curve + Best Epoch ===')

baseline_epoch_df = pd.DataFrame({
    'epoch': np.arange(1, len(baseline_history.history['loss']) + 1),
    'train_loss': baseline_history.history['loss'],
    'val_loss': baseline_history.history['val_loss'],
    'train_mae': baseline_history.history['mae'],
    'val_mae': baseline_history.history['val_mae']
})

baseline_epoch_df['loss_gap'] = baseline_epoch_df['val_loss'] - baseline_epoch_df['train_loss']

best_idx = baseline_epoch_df['val_loss'].idxmin()
best_row = baseline_epoch_df.loc[best_idx]
best_epoch = int(best_row['epoch'])

print(f"Best epoch    : {best_epoch}")
print(f"Train Loss    : {best_row['train_loss']:.4f}")
print(f"Val Loss      : {best_row['val_loss']:.4f}")
print(f"Gap           : {best_row['loss_gap']:.4f}")
print(f"Train MAE     : {best_row['train_mae']:.4f}")
print(f"Val MAE       : {best_row['val_mae']:.4f}")
print(f"Val RMSE      : {np.sqrt(best_row['val_loss']):.4f}")

plt.figure(figsize=(8, 5))
plt.plot(baseline_epoch_df['epoch'], baseline_epoch_df['train_loss'], label='Train Loss')
plt.plot(baseline_epoch_df['epoch'], baseline_epoch_df['val_loss'], label='Val Loss')
plt.axvline(best_epoch, linestyle='--', label=f'Best epoch = {best_epoch}')
plt.title('Baseline DNN Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.legend()
plt.show()
print('Loss curve를 보면 train loss와 validation loss가 모두 epoch가 증가함에 따라 감소한다. Best epoch는 50일때, Validation loss가 상승하지 않았으므로 강한 과적합은 관찰되지 않는다.')
print('따라서 모델이 train set에 더 잘 맞는 약한 generalization gap은 존재한다')

plt.figure(figsize=(8, 4))
plt.plot(baseline_epoch_df['epoch'], baseline_epoch_df['loss_gap'], label='Val Loss - Train Loss')
plt.axhline(0, linestyle='--')
plt.axvline(best_epoch, linestyle='--', label=f'Best epoch = {best_epoch}')
plt.title('Baseline Generalization Gap')
plt.xlabel('Epoch')
plt.ylabel('Loss Gap')
plt.legend()
plt.show()

print(f'다만 train loss가 validation loss보다 지속적으로 낮고, 마지막 기준 train loss는 약 {best_row["train_loss"]:.1f}, validation loss는 약 {best_row["val_loss"]:.1f}, gap은 약 {best_row["loss_gap"]:.1f}이다.')
print('따라서 2000개 subset 학습 조건에서는 train set에 더 잘 맞는 generalization gap이 존재한다.')
print('== 단, validation loss가 상승하는 패턴보다는 train/validation loss가 함께 감소하는 패턴이므로, 강한 과적합이라기보다 subset 학습에서 발생한 일반화 gap으로 판단한다. ==')
```

```text
 === B2-1. Baseline Loss Curve + Best Epoch ===
Best epoch    : 50
Train Loss    : 3994.2639
Val Loss      : 5263.4839
Gap           : 1269.2200
Train MAE     : 44.8329
Val MAE       : 51.0481
Val RMSE      : 72.5499
```

![output](assets/3085_problem2_cell032_out01_img24.png)

```text
Loss curve를 보면 train loss와 validation loss가 모두 epoch가 증가함에 따라 감소한다. Best epoch는 50일때, Validation loss가 상승하지 않았으므로 강한 과적합은 관찰되지 않는다.
따라서 모델이 train set에 더 잘 맞는 약한 generalization gap은 존재한다
```

![output](assets/3085_problem2_cell032_out03_img25.png)

```text
다만 train loss가 validation loss보다 지속적으로 낮고, 마지막 기준 train loss는 약 3994.3, validation loss는 약 5263.5, gap은 약 1269.2이다.
따라서 2000개 subset 학습 조건에서는 train set에 더 잘 맞는 generalization gap이 존재한다.
== 단, validation loss가 상승하는 패턴보다는 train/validation loss가 함께 감소하는 패턴이므로, 강한 과적합이라기보다 subset 학습에서 발생한 일반화 gap으로 판단한다. ==
```

```python
print(' === B2-2. Baseline Validation Prediction Check ===')

y_val_pred = baseline_model.predict(X_val, verbose=0).reshape(-1)

val_residual = y_val - y_val_pred
val_abs_error = np.abs(val_residual)

baseline_val_eval = pd.DataFrame({
    'y_true': y_val,
    'y_pred': y_val_pred,
    'residual': val_residual,
    'abs_error': val_abs_error
})

val_mae = mean_absolute_error(y_val, y_val_pred)
val_mse = mean_squared_error(y_val, y_val_pred)
val_rmse = np.sqrt(val_mse)
val_r2 = r2_score(y_val, y_val_pred)

print(f"MAE : {val_mae:.4f}")
print(f"MSE : {val_mse:.4f}")
print(f"RMSE: {val_rmse:.4f}")
print(f"R²  : {val_r2:.4f}")

display(baseline_val_eval.describe())

print(f'Validation 성능은 MAE 약 {val_mae:.2f}, RMSE 약 {val_rmse:.2f}, R² 약 {val_r2:.3f}로 나타났다.')

min_value = min(y_val.min(), y_val_pred.min())
max_value = max(y_val.max(), y_val_pred.max())

plt.figure(figsize=(6, 6))
plt.hexbin(y_val, y_val_pred, gridsize=50, mincnt=1)
plt.colorbar(label='count')
plt.plot([min_value, max_value], [min_value, max_value], linestyle='--')
plt.title('Actual vs Predicted PM2.5')
plt.xlabel('Actual PM2.5')
plt.ylabel('Predicted PM2.5')
plt.show()

print('Actual vs Predicted와 residual plot을 보면 모델은 전체 경향은 학습했지만, 예측값이 중앙 범위로 압축되는 경향이 있다')
plt.figure(figsize=(8, 4))
plt.scatter(y_val_pred, val_residual, alpha=0.25, s=8)
plt.axhline(0, linestyle='--')
plt.title('Residual Plot')
plt.xlabel('Predicted PM2.5')
plt.ylabel('Residual = Actual - Predicted')
plt.show()

print('== 이는 baseline DNN이 PM2.5 변동의 일부를 설명하고 있으나, 고농도 episode까지 충분히 정밀하게 맞히지는 못한다는 의미다. ==')
```

```text
 === B2-2. Baseline Validation Prediction Check ===
```

```text
MAE : 51.0481
MSE : 5263.4834
RMSE: 72.5499
R²  : 0.3859
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>y_true</th>
      <th>y_pred</th>
      <th>residual</th>
      <th>abs_error</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>8765.000000</td>
      <td>8765.000000</td>
      <td>8765.000000</td>
      <td>8765.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>98.154823</td>
      <td>100.019035</td>
      <td>-1.864221</td>
      <td>51.048088</td>
    </tr>
    <tr>
      <th>std</th>
      <td>92.585632</td>
      <td>62.285843</td>
      <td>72.530052</td>
      <td>51.554626</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>-3.687966</td>
      <td>-214.950775</td>
      <td>0.018097</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>28.000000</td>
      <td>51.823105</td>
      <td>-44.349060</td>
      <td>15.135445</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>71.000000</td>
      <td>100.486534</td>
      <td>-6.348734</td>
      <td>36.195206</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>136.000000</td>
      <td>141.693863</td>
      <td>25.427608</td>
      <td>70.425262</td>
    </tr>
    <tr>
      <th>max</th>
      <td>980.000000</td>
      <td>343.845123</td>
      <td>912.366272</td>
      <td>912.366272</td>
    </tr>
  </tbody>
</table>
</div>

```text
Validation 성능은 MAE 약 51.05, RMSE 약 72.55, R² 약 0.386로 나타났다.
```

![output](assets/3085_problem2_cell033_out04_img26.png)

```text
Actual vs Predicted와 residual plot을 보면 모델은 전체 경향은 학습했지만, 예측값이 중앙 범위로 압축되는 경향이 있다
```

![output](assets/3085_problem2_cell033_out06_img27.png)

```text
== 이는 baseline DNN이 PM2.5 변동의 일부를 설명하고 있으나, 고농도 episode까지 충분히 정밀하게 맞히지는 못한다는 의미다. ==
```

```python
print(' === B2-3. PM2.5 농도구간별오차. (categorical로 치환)===')

q50 = np.quantile(y_val, 0.50)
q75 = np.quantile(y_val, 0.75)
q95 = np.quantile(y_val, 0.95)

def pm25_bin(x):
    if x < q50:
        return 'low_<50%'
    elif x < q75:
        return 'mid_50-75%'
    elif x < q95:
        return 'high_75-95%'
    else:
        return 'extreme_>=95%'

bin_order = ['low_<50%', 'mid_50-75%', 'high_75-95%', 'extreme_>=95%']

baseline_val_eval['pm25_bin'] = baseline_val_eval['y_true'].apply(pm25_bin)
baseline_val_eval['pm25_bin'] = pd.Categorical(
    baseline_val_eval['pm25_bin'],
    categories=bin_order,
    ordered=True
)

bin_error = baseline_val_eval.groupby('pm25_bin', observed=False).agg(
    count=('y_true', 'count'),
    y_true_mean=('y_true', 'mean'),
    y_pred_mean=('y_pred', 'mean'),
    mae=('abs_error', 'mean'),
    residual_mean=('residual', 'mean')
)

bin_error['bias'] = np.where(
    bin_error['residual_mean'] > 0,
    'underprediction',
    'overprediction'
)

display(bin_error)
print('== 농도 구간별 오차 분석에서 저농도 구간은 과대예측하고, 고농도 extreme 구간은 과소예측하는 패턴이 나타났다. ==')


plt.figure(figsize=(8, 4))
plt.bar(bin_error.index, bin_error['mae'])
plt.title('Validation MAE by PM2.5 Bin')
plt.xlabel('PM2.5 bin')
plt.ylabel('MAE')
plt.xticks(rotation=25)
plt.show()

print('===  따라서 Baseline DNN은 강한 과적합 모델은 아니지만, 저농도, 특히 고농도 PM2.5 episode를 충분히 잡지 못하는 한계가 있다. ===')

plt.figure(figsize=(8, 4))
plt.bar(bin_error.index, bin_error['residual_mean'])
plt.axhline(0, linestyle='--')
plt.title('Mean Residual by PM2.5 Bin')
plt.xlabel('PM2.5 bin')
plt.ylabel('Mean residual')
plt.xticks(rotation=25)
plt.show()

print(' ==> 이에 대하여 Part C에서는 Dropout, L2 Regularization, EarlyStopping, Batch Normalization을 각각 개별 적용하여,')
print('validation loss, train-validation gap, 그리고 고농도 구간 오차가 개선되는지를 중점적으로 비교함이 적절할 것으로 판단된다. ==')
```

```text
 === B2-3. PM2.5 농도구간별오차. (categorical로 치환)===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
      <th>y_true_mean</th>
      <th>y_pred_mean</th>
      <th>mae</th>
      <th>residual_mean</th>
      <th>bias</th>
    </tr>
    <tr>
      <th>pm25_bin</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>low_&lt;50%</th>
      <td>4345</td>
      <td>32.170311</td>
      <td>64.850098</td>
      <td>41.171467</td>
      <td>-32.679790</td>
      <td>overprediction</td>
    </tr>
    <tr>
      <th>mid_50-75%</th>
      <td>2215</td>
      <td>99.531830</td>
      <td>115.733360</td>
      <td>38.311584</td>
      <td>-16.201534</td>
      <td>overprediction</td>
    </tr>
    <tr>
      <th>high_75-95%</th>
      <td>1765</td>
      <td>190.954681</td>
      <td>144.801163</td>
      <td>58.694447</td>
      <td>46.153500</td>
      <td>underprediction</td>
    </tr>
    <tr>
      <th>extreme_&gt;=95%</th>
      <td>440</td>
      <td>370.565918</td>
      <td>188.567612</td>
      <td>182.024124</td>
      <td>181.998291</td>
      <td>underprediction</td>
    </tr>
  </tbody>
</table>
</div>

```text
== 농도 구간별 오차 분석에서 저농도 구간은 과대예측하고, 고농도 extreme 구간은 과소예측하는 패턴이 나타났다. ==
```

![output](assets/3085_problem2_cell034_out03_img28.png)

```text
===  따라서 Baseline DNN은 강한 과적합 모델은 아니지만, 저농도, 특히 고농도 PM2.5 episode를 충분히 잡지 못하는 한계가 있다. ===
```

![output](assets/3085_problem2_cell034_out05_img29.png)

```text
 ==> 이에 대하여 Part C에서는 Dropout, L2 Regularization, EarlyStopping, Batch Normalization을 각각 개별 적용하여,
validation loss, train-validation gap, 그리고 고농도 구간 오차가 개선되는지를 중점적으로 비교함이 적절할 것으로 판단된다. ==
```

---
# Part C. 정규화 4총사 각각 적용 (14점)

Part B와 같은 조건(같은 데이터, 같은 학습 설정)에서
*각 정규화 기법을 개별적으로* 적용해 효과를 비교하세요.

**B 요약 및 C 모델링 방향성**:
- Baseline 모델은 과적합이 심한 모델이 아니며, 정상적으로 학습 중이지만 저/고농도 값에 대해 성능이 다소 부족한 문제가 발생하였다.

- 따라서 C파트의 목적은 단순히 train loss를 낮추는 것이 아니라 validation 일반화와 고농도 구간 예측 취약점이 개선되는지 확인하는 것이다.

```python
print(' === C0. 정규화 GLOBAL 설정 ===')

regularization_results = []
regularization_histories = {}

def get_last_result(model_name, history):
    train_loss = history.history['loss'][-1]
    val_loss = history.history['val_loss'][-1]
    gap = val_loss - train_loss
    
    train_mae = history.history['mae'][-1]
    val_mae = history.history['val_mae'][-1]
    
    print(f'[{model_name}]')
    print(f'Train Loss: {train_loss:.4f}')
    print(f'Val Loss  : {val_loss:.4f}')
    print(f'Gap       : {gap:.4f}')
    print(f'Train MAE : {train_mae:.4f}')
    print(f'Val MAE   : {val_mae:.4f}')
    
    return {
        'model': model_name,
        'train_loss': train_loss,
        'val_loss': val_loss,
        'gap': gap,
        'train_mae': train_mae,
        'val_mae': val_mae,
        'epochs': len(history.history['loss'])
    }

# Baseline도 같은 기준으로 저장
baseline_c_result = get_last_result('Baseline', baseline_history)
regularization_results.append(baseline_c_result)
regularization_histories['Baseline'] = baseline_history
```

```text
 === C0. 정규화 GLOBAL 설정 ===
[Baseline]
Train Loss: 3994.2639
Val Loss  : 5263.4839
Gap       : 1269.2200
Train MAE : 44.8329
Val MAE   : 51.0481
```

## C1. Dropout 적용 (3점)

**요구사항**: Baseline 구조에 Dropout(0.3)을 추가
**필수 출력**: Train Loss, Val Loss, Gap

```python
print(' === C1. Dropout(0.3) 적용 ===')

np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

def build_dropout_model():
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(input_dim,)))
    model.add(Dropout(0.3))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    return model

dropout_model = build_dropout_model()

dropout_history = dropout_model.fit(
    X_train_fit, y_train_fit,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=BATCH_SIZE,
    verbose=0
)

dropout_result = get_last_result('Dropout', dropout_history)

regularization_results.append(dropout_result)
regularization_histories['Dropout'] = dropout_history
```

```text
 === C1. Dropout(0.3) 적용 ===
```

```text
[Dropout]
Train Loss: 6002.7637
Val Loss  : 5742.8447
Gap       : -259.9189
Train MAE : 53.6394
Val MAE   : 52.5151
```

## C2. L2 Regularization 적용 (3점)

**요구사항**: 모든 Dense 층에 `kernel_regularizer=l2(0.01)`
**필수 출력**: Train Loss, Val Loss, Gap

```python
print(' === C2. L2 Regularization 적용 ===')

np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

def build_l2_model():
    model = Sequential()
    
    model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01), input_shape=(input_dim,)))
    model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(Dense(16, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(Dense(1, kernel_regularizer=l2(0.01)))
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    return model

l2_model = build_l2_model()

l2_history = l2_model.fit(
    X_train_fit, y_train_fit,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=BATCH_SIZE,
    verbose=0
)

l2_result = get_last_result('L2', l2_history)

regularization_results.append(l2_result)
regularization_histories['L2'] = l2_history
```

```text
 === C2. L2 Regularization 적용 ===
```

```text
[L2]
Train Loss: 4042.7578
Val Loss  : 5251.4712
Gap       : 1208.7134
Train MAE : 45.0991
Val MAE   : 51.0716
```

## C3. Early Stopping 적용 (3점)

**요구사항**:
- `EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)`
- epochs는 50보다 크게 잡아도 됨 (Early Stop이 멈춤)

**필수 출력**:
- Train Loss, Val Loss, Gap
(* 강의의 train_and_eval과 동일하게, history.history['val_loss'][-1](마지막 epoch의 val_loss)을 출력하시오.)
- 실제 학습된 epoch 수

```python
print(' === C3. Early Stopping 적용 ===')

np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

def build_earlystop_model():
    model = Sequential()
    
    model.add(Dense(64, activation='relu', input_shape=(input_dim,)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1))
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    return model

earlystop_model = build_earlystop_model()

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

earlystop_history = earlystop_model.fit(
    X_train_fit, y_train_fit,
    validation_data=(X_val, y_val),
    epochs=150,
    batch_size=BATCH_SIZE,
    callbacks=[early_stop],
    verbose=0
)

earlystop_result = get_last_result('EarlyStopping', earlystop_history)

print(f"실제 학습된 epoch 수: {len(earlystop_history.history['loss'])}")

regularization_results.append(earlystop_result)
regularization_histories['EarlyStopping'] = earlystop_history
```

```text
 === C3. Early Stopping 적용 ===
```

```text
[EarlyStopping]
Train Loss: 2647.9390
Val Loss  : 5022.9136
Gap       : 2374.9746
Train MAE : 36.6457
Val MAE   : 49.0036
실제 학습된 epoch 수: 115
```

## C4. Batch Normalization 적용 (3점)

**요구사항**:
- `Dense → BatchNorm → Activation` 순서로 구성
- 활성화 함수는 Dense의 인자가 아닌 별도 `Activation('relu')`로

**필수 출력**: Train Loss, Val Loss, Gap

```python
print(' === C4. Batch Normalization 적용 ===')

np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

def build_batchnorm_model():
    model = Sequential()
    
    model.add(Dense(64, input_shape=(input_dim,)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    
    model.add(Dense(32))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    
    model.add(Dense(16))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    
    model.add(Dense(1))
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    return model

batchnorm_model = build_batchnorm_model()

batchnorm_history = batchnorm_model.fit(
    X_train_fit, y_train_fit,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=BATCH_SIZE,
    verbose=0
)

batchnorm_result = get_last_result('BatchNorm', batchnorm_history)

regularization_results.append(batchnorm_result)
regularization_histories['BatchNorm'] = batchnorm_history
```

```text
 === C4. Batch Normalization 적용 ===
```

```text
[BatchNorm]
Train Loss: 1473.8469
Val Loss  : 9147.0645
Gap       : 7673.2175
Train MAE : 27.8435
Val MAE   : 58.9086
```

## C5. 4가지 비교 시각화 (2점)

Baseline + 4총사 (5개 모델)의 loss curve를 비교 그래프로 시각화.

**요약**
- Baseline, Dropout, L2 Regularization, EarlyStopping, Batch Normalization을 같은 train subset, 같은 train/validation split, 같은 `batch_size=32` 조건에서 비교했다.
- 비교 기준은 validation loss, validation MAE, gap = validation loss - train loss, 그리고 loss curve의 안정성이다.

- 주안: B2에서 Baseline은 `train subset 2000개`만 사용한 기준 모델이므로 train-validation gap과 고농도 PM2.5 과소예측 여부를 반드시 확인해야 한다.
- 따라서 Part C의 목적은 단순히 train loss를 낮추는 것이 아니라, validation 기준 일반화 성능과 예측 안정성이 Baseline 대비 개선되는지 확인하는 것이다.

**Validation loss curve**
- 최신 수치는 바로 아래 C5 결과표를 기준으로 한다.
- C5에서는 `val_loss`를 1순위, `val_mae`를 2순위, `gap_abs`를 보조 기준으로 정렬한다.
- Baseline보다 validation loss가 낮고, validation MAE도 낮으며, gap 해석이 가능한 모델을 최종 후보로 선택한다.

**결론**
- 최종 후보는 C5의 `selection_df` 1행에 있는 모델이다.
- 단, validation 기준 후보가 test set에서도 실제 일반화되는지는 Part D에서 Baseline 대비 test metric, residual, 농도 구간별 MAE로 다시 검증한다.

```python
print(' === C5-1. 정규화 5개 모델 결과표 정리 ===')

# 여러 번 실행했을 경우 같은 model이 중복 저장될 수 있으므로 마지막 결과만 사용
regularization_result_df = pd.DataFrame(regularization_results).drop_duplicates(
    subset='model',
    keep='last'
).copy()

model_order = ['Baseline', 'Dropout', 'L2', 'EarlyStopping', 'BatchNorm']
model_order = [m for m in model_order if m in regularization_result_df['model'].values]

regularization_result_df['model'] = pd.Categorical(
    regularization_result_df['model'],
    categories=model_order,
    ordered=True
)

regularization_result_df = regularization_result_df.sort_values('model').reset_index(drop=True)

# 추가 해석 metric
regularization_result_df['val_rmse'] = np.sqrt(regularization_result_df['val_loss'])
regularization_result_df['gap_abs'] = regularization_result_df['gap'].abs()

baseline_val_loss = regularization_result_df.loc[
    regularization_result_df['model'] == 'Baseline',
    'val_loss'
].iloc[0]

baseline_val_mae = regularization_result_df.loc[
    regularization_result_df['model'] == 'Baseline',
    'val_mae'
].iloc[0]

regularization_result_df['val_loss_delta_vs_baseline'] = (
    regularization_result_df['val_loss'] - baseline_val_loss
)

regularization_result_df['val_loss_improve_pct'] = (
    (baseline_val_loss - regularization_result_df['val_loss']) / baseline_val_loss * 100
)

regularization_result_df['val_mae_delta_vs_baseline'] = (
    regularization_result_df['val_mae'] - baseline_val_mae
)

# 모델별 해석 라벨
diagnosis_map = {
    'Baseline': 'reference',
    'Dropout': 'strong regularization / possible underfit',
    'L2': 'mild regularization',
    'EarlyStopping': 'long training + best epoch search',
    'BatchNorm': 'hidden activation stabilization'
}

regularization_result_df['diagnosis_label'] = regularization_result_df['model'].astype(str).map(diagnosis_map)

display(
    regularization_result_df[
        [
            'model',
            'epochs',
            'train_loss',
            'val_loss',
            'gap',
            'val_mae',
            'val_rmse',
            'val_loss_delta_vs_baseline',
            'val_loss_improve_pct',
            'diagnosis_label'
        ]
    ].sort_values('val_loss')
)

print('해석 기준:')
print('1. val_loss가 낮을수록 validation 기준 회귀 오차가 작음')
print('2. gap = val_loss - train_loss이며, 양수면 validation 손실이 train 손실보다 큰 것으로 판단.')
print('3. Dropout의 gap이 음수 => Train 단계에서 dropout noise가 적용되어 train loss가 더 크게 나올 수 있기 때문임을 유의.')
print('4. 최종 선택은 val_loss를 1순위로 두되, val_mae와 gap을 보조 기준으로 둔다.')
```

```text
 === C5-1. 정규화 5개 모델 결과표 정리 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>epochs</th>
      <th>train_loss</th>
      <th>val_loss</th>
      <th>gap</th>
      <th>val_mae</th>
      <th>val_rmse</th>
      <th>val_loss_delta_vs_baseline</th>
      <th>val_loss_improve_pct</th>
      <th>diagnosis_label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3</th>
      <td>EarlyStopping</td>
      <td>115</td>
      <td>2647.938965</td>
      <td>5022.913574</td>
      <td>2374.974609</td>
      <td>49.003605</td>
      <td>70.872516</td>
      <td>-240.570312</td>
      <td>4.570553</td>
      <td>long training + best epoch search</td>
    </tr>
    <tr>
      <th>2</th>
      <td>L2</td>
      <td>50</td>
      <td>4042.757812</td>
      <td>5251.471191</td>
      <td>1208.713379</td>
      <td>51.071568</td>
      <td>72.467035</td>
      <td>-12.012695</td>
      <td>0.228227</td>
      <td>mild regularization</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>50</td>
      <td>3994.263916</td>
      <td>5263.483887</td>
      <td>1269.219971</td>
      <td>51.048092</td>
      <td>72.549872</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>reference</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Dropout</td>
      <td>50</td>
      <td>6002.763672</td>
      <td>5742.844727</td>
      <td>-259.918945</td>
      <td>52.515144</td>
      <td>75.781559</td>
      <td>479.360840</td>
      <td>-9.107292</td>
      <td>strong regularization / possible underfit</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BatchNorm</td>
      <td>50</td>
      <td>1473.846924</td>
      <td>9147.064453</td>
      <td>7673.217529</td>
      <td>58.908566</td>
      <td>95.640287</td>
      <td>3883.580566</td>
      <td>-73.783461</td>
      <td>hidden activation stabilization</td>
    </tr>
  </tbody>
</table>
</div>

```text
해석 기준:
1. val_loss가 낮을수록 validation 기준 회귀 오차가 작음
2. gap = val_loss - train_loss이며, 양수면 validation 손실이 train 손실보다 큰 것으로 판단.
3. Dropout의 gap이 음수 => Train 단계에서 dropout noise가 적용되어 train loss가 더 크게 나올 수 있기 때문임을 유의.
4. 최종 선택은 val_loss를 1순위로 두되, val_mae와 gap을 보조 기준으로 둔다.
```

```python
print(' === C5-2. 정규화 모델 비교용 결과표 재정리 ===')

# 여러 번 실행했을 경우 같은 model이 중복 저장될 수 있으므로 마지막 결과만 사용
regularization_result_df = pd.DataFrame(regularization_results).drop_duplicates(
    subset='model',
    keep='last'
).copy()

model_order = ['Baseline', 'Dropout', 'L2', 'EarlyStopping', 'BatchNorm']
model_order = [m for m in model_order if m in regularization_result_df['model'].values]

regularization_result_df['model'] = regularization_result_df['model'].astype(str)
regularization_result_df = regularization_result_df.set_index('model').loc[model_order].reset_index()

# 추가 지표
regularization_result_df['val_rmse'] = np.sqrt(regularization_result_df['val_loss'])
regularization_result_df['gap_abs'] = regularization_result_df['gap'].abs()

baseline_val_loss = regularization_result_df.loc[
    regularization_result_df['model'] == 'Baseline',
    'val_loss'
].iloc[0]

baseline_val_mae = regularization_result_df.loc[
    regularization_result_df['model'] == 'Baseline',
    'val_mae'
].iloc[0]

baseline_gap = regularization_result_df.loc[
    regularization_result_df['model'] == 'Baseline',
    'gap'
].iloc[0]

regularization_result_df['val_loss_delta_vs_baseline'] = (
    regularization_result_df['val_loss'] - baseline_val_loss
)

regularization_result_df['val_loss_improve_pct'] = (
    (baseline_val_loss - regularization_result_df['val_loss']) / baseline_val_loss * 100
)

regularization_result_df['val_mae_delta_vs_baseline'] = (
    regularization_result_df['val_mae'] - baseline_val_mae
)

# 모델 약칭
model_abbr = {
    'Baseline': 'BL',
    'Dropout': 'DO',
    'L2': 'L2',
    'EarlyStopping': 'ES',
    'BatchNorm': 'BN'
}

regularization_result_df['abbr'] = regularization_result_df['model'].map(model_abbr)

# 모델 성격 라벨
diagnosis_map = {
    'Baseline': 'reference',
    'Dropout': 'strong regularization / possible underfit',
    'L2': 'mild regularization',
    'EarlyStopping': 'long training + best epoch search',
    'BatchNorm': 'hidden activation stabilization'
}

regularization_result_df['diagnosis_label'] = regularization_result_df['model'].map(diagnosis_map)

# 선택 기준: val_loss 1순위, val_mae 2순위, gap_abs 3순위
selection_df = regularization_result_df.sort_values(
    ['val_loss', 'val_mae', 'gap_abs'],
    ascending=[True, True, True]
).reset_index(drop=True)

best_model_name = selection_df.loc[0, 'model']
best_model_val_loss = selection_df.loc[0, 'val_loss']
best_model_val_mae = selection_df.loc[0, 'val_mae']
best_model_gap = selection_df.loc[0, 'gap']
best_model_improve_pct = selection_df.loc[0, 'val_loss_improve_pct']

display(
    selection_df[
        [
            'abbr',
            'model',
            'epochs',
            'train_loss',
            'val_loss',
            'gap',
            'val_mae',
            'val_rmse',
            'val_loss_improve_pct',
            'diagnosis_label'
        ]
    ]
)

print('해석:')
print('C5에서는 val_loss를 1순위 기준으로 모델을 정렬한다.')
print('val_mae는 실제 PM2.5 단위에서 평균적으로 얼마나 틀리는지를 보여주는 보조 기준이다.')
print('gap은 train loss와 validation loss의 차이이므로, 과적합 또는 학습 noise 여부를 판단하는 보조 신호다.')
print(f'현재 validation 기준 1위 모델은 {best_model_name}이다.')

#print(' === C5-3. Validation Loss Curve 비교 ===')

plt.figure(figsize=(10, 6))

for model_name in model_order:
    history = regularization_histories[model_name]
    val_loss = history.history['val_loss']
    epochs = np.arange(1, len(val_loss) + 1)
    abbr = model_abbr[model_name]
    
    plt.plot(
        epochs,
        val_loss,
        label=f'{abbr}: {model_name} ({len(epochs)} ep)'
    )

plt.axhline(
    baseline_val_loss,
    linestyle='--',
    label=f'BL final reference = {baseline_val_loss:.0f}'
)

plt.title('C5-1. Validation Loss Curves')
plt.xlabel('Epoch')
plt.ylabel('Validation Loss (MSE)')
plt.legend()
plt.show()

print('===시각화 1. 해석:===')
print('==Validation loss curve는 각 정규화 전략이 epoch가 진행되면서 일반화 오차를 어떻게 낮추는지 보여준다.==')
print('------------------')
print(f'=Baseline은 50 epoch 기준 모델이고, {best_model_name}은 {int(selection_df.loc[0, "epochs"])} epoch까지 학습된 뒤 validation 기준 최저 손실을 기록했다.=')
print('따라서 C5의 핵심은 같은 subset 조건에서 어느 정규화 전략이 validation loss를 가장 낮췄는지 비교하는 것이다.')
print('각 정규화 기법의 해석은 아래 결과표의 val_loss, val_mae, gap을 함께 보고 판단한다.')
print('------------------')
print(f'==결론: validation curve 기준으로는 {best_model_name}이 가장 낮은 일반화 오차를 보인 최종 후보이다.==')

#print(' === C5-4. Final Metric Dashboard ===')

plot_df = regularization_result_df.copy()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1. Val Loss
ordered_loss = plot_df.sort_values('val_loss')
axes[0].bar(ordered_loss['abbr'], ordered_loss['val_loss'])
axes[0].axhline(baseline_val_loss, linestyle='--')
axes[0].set_title('Final Val Loss')
axes[0].set_xlabel('Model')
axes[0].set_ylabel('MSE')

for i, v in enumerate(ordered_loss['val_loss']):
    axes[0].text(i, v, f'{v:.0f}', ha='center', va='bottom', fontsize=8)

# 2. Val MAE
ordered_mae = plot_df.sort_values('val_mae')
axes[1].bar(ordered_mae['abbr'], ordered_mae['val_mae'])
axes[1].axhline(baseline_val_mae, linestyle='--')
axes[1].set_title('Final Val MAE')
axes[1].set_xlabel('Model')
axes[1].set_ylabel('MAE')

for i, v in enumerate(ordered_mae['val_mae']):
    axes[1].text(i, v, f'{v:.1f}', ha='center', va='bottom', fontsize=8)

# 3. Gap
ordered_gap = plot_df.sort_values('gap_abs')
axes[2].bar(ordered_gap['abbr'], ordered_gap['gap'])
axes[2].axhline(0, linestyle='--')
axes[2].axhline(baseline_gap, linestyle=':')
axes[2].set_title('Train-Val Gap')
axes[2].set_xlabel('Model')
axes[2].set_ylabel('Val Loss - Train Loss')

for i, v in enumerate(ordered_gap['gap']):
    va = 'bottom' if v >= 0 else 'top'
    axes[2].text(i, v, f'{v:.0f}', ha='center', va=va, fontsize=8)

plt.tight_layout()
plt.show()

print('===시각화 2. 해석:===')
print('Final metric dashboard는 validation loss, validation MAE, train-validation gap을 분리해서 보여준다.')
print('Val Loss는 MSE 기준이므로 큰 오차, 특히 고농도 PM2.5 예측 실패에 더 민감하다.')
print('Val MAE는 실제 PM2.5 단위에서 평균적으로 얼마나 틀리는지를 보여주므로 해석이 직관적이다.')
print('Gap은 train과 validation 사이의 차이를 보여주며, 너무 크면 train에 더 잘 맞는 모델일 수 있다.')
print('------------------')
print(f'===> {best_model_name}은 Val Loss {best_model_val_loss:.2f}, Val MAE {best_model_val_mae:.2f}로 validation 기준 1위다.')
print(f'Baseline 대비 validation loss는 {best_model_improve_pct:.2f}% 개선되었다.===')
print('------------------')
print('Baseline 대비 개선 여부는 각 모델의 val_loss_improve_pct와 val_mae_delta_vs_baseline으로 판단한다.')
print('Dropout은 train 단계 noise 때문에 gap이 음수로 나올 수 있어, val_loss와 val_mae를 함께 보고 underfitting 여부를 판단한다.')
print(f" L2는 gap은 안정적인 편이지만 Val Loss 개선율이 {regularization_result_df.loc[regularization_result_df['model'] == 'L2', 'val_loss_improve_pct'].iloc[0]:.2f}%이므로 최종 후보로 보기는 어렵다.")
print(f'= 다만 {best_model_name}의 gap은 {best_model_gap:.2f}이고 Baseline gap은 {baseline_gap:.2f}이므로, D파트에서 test set과 residual 분석으로 실제 일반화 성능을 반드시 확인해야 한다. =')

#print(' === C5-5. Model Selection Map ===')

plt.figure(figsize=(8, 6))

for _, row in regularization_result_df.iterrows():
    plt.scatter(row['val_loss'], row['gap'], s=160)
    plt.text(
        row['val_loss'],
        row['gap'],
        row['abbr'],
        ha='center',
        va='center',
        fontsize=9,
        color='white',
        fontweight='bold'
    )

plt.axvline(baseline_val_loss, linestyle='--', label='Baseline Val Loss')
plt.axhline(baseline_gap, linestyle=':', label='Baseline Gap')
plt.axhline(0, linestyle='--', label='Zero Gap')

best_row = selection_df.iloc[0]

plt.scatter(
    best_row['val_loss'],
    best_row['gap'],
    s=360,
    facecolors='none',
    edgecolors='black',
    linewidth=2.2,
    label='Selected'
)

plt.title('C5-3. Model Selection Map')
plt.xlabel('Validation Loss (lower is better)')
plt.ylabel('Gap = Val Loss - Train Loss')
plt.legend()
plt.show()

print('===시각화 결론 해석:===')
print('[validation loss와 train-validation gap을 동시에 보는 시각화 맵]')
print('왼쪽에 있을수록 validation loss가 낮아 성능이 좋고, y=0에 가까울수록 train과 validation 손실 차이가 작다.')
print('Baseline 기준선보다 왼쪽에 있는 모델은 validation loss 기준으로 Baseline보다 개선된 모델이다.')
print(f'{best_model_name}은 validation loss 기준 가장 낮은 위치에 있으므로 최종 후보로 선택된다')
print(f'=그러나 {best_model_name}의 gap({best_model_gap:.2f})이 Baseline gap({baseline_gap:.2f})보다 크므로, 성능은 가장 좋지만 gap 보완이 필요한 모델로 해석해야 한다.=')
print('------------------')
second_row = selection_df.iloc[1]
print(f'2순위 후보는 {second_row["model"]}이며, val_loss={second_row["val_loss"]:.2f}, 개선율={second_row["val_loss_improve_pct"]:.2f}%이다.')
print('L2는 gap 안정성과 validation 성능 개선폭을 함께 보고 보수적 후보인지 판단한다.')
print('Dropout은 val_loss 위치와 gap 방향을 함께 보고 최종 후보 포함 여부를 판단한다.')

print('\n최종 판정:')
print(f'- Validation 기준 1순위 후보: {best_model_name}')
print(f'- Val Loss: {best_model_val_loss:.4f}')
print(f'- Val MAE : {best_model_val_mae:.4f}')
print(f'- Gap     : {best_model_gap:.4f}')
print(f'- Baseline 대비 Val Loss 개선율: {best_model_improve_pct:.2f}%')
print(f'----따라서 Part D에서는 *{best_model_name}* 모델을 최종 모델로 선택하고, test set에서 최종 일반화 성능을 평가한다.----')
```

```text
 === C5-2. 정규화 모델 비교용 결과표 재정리 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>abbr</th>
      <th>model</th>
      <th>epochs</th>
      <th>train_loss</th>
      <th>val_loss</th>
      <th>gap</th>
      <th>val_mae</th>
      <th>val_rmse</th>
      <th>val_loss_improve_pct</th>
      <th>diagnosis_label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ES</td>
      <td>EarlyStopping</td>
      <td>115</td>
      <td>2647.938965</td>
      <td>5022.913574</td>
      <td>2374.974609</td>
      <td>49.003605</td>
      <td>70.872516</td>
      <td>4.570553</td>
      <td>long training + best epoch search</td>
    </tr>
    <tr>
      <th>1</th>
      <td>L2</td>
      <td>L2</td>
      <td>50</td>
      <td>4042.757812</td>
      <td>5251.471191</td>
      <td>1208.713379</td>
      <td>51.071568</td>
      <td>72.467035</td>
      <td>0.228227</td>
      <td>mild regularization</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BL</td>
      <td>Baseline</td>
      <td>50</td>
      <td>3994.263916</td>
      <td>5263.483887</td>
      <td>1269.219971</td>
      <td>51.048092</td>
      <td>72.549872</td>
      <td>0.000000</td>
      <td>reference</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DO</td>
      <td>Dropout</td>
      <td>50</td>
      <td>6002.763672</td>
      <td>5742.844727</td>
      <td>-259.918945</td>
      <td>52.515144</td>
      <td>75.781559</td>
      <td>-9.107292</td>
      <td>strong regularization / possible underfit</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BN</td>
      <td>BatchNorm</td>
      <td>50</td>
      <td>1473.846924</td>
      <td>9147.064453</td>
      <td>7673.217529</td>
      <td>58.908566</td>
      <td>95.640287</td>
      <td>-73.783461</td>
      <td>hidden activation stabilization</td>
    </tr>
  </tbody>
</table>
</div>

```text
해석:
C5에서는 val_loss를 1순위 기준으로 모델을 정렬한다.
val_mae는 실제 PM2.5 단위에서 평균적으로 얼마나 틀리는지를 보여주는 보조 기준이다.
gap은 train loss와 validation loss의 차이이므로, 과적합 또는 학습 noise 여부를 판단하는 보조 신호다.
현재 validation 기준 1위 모델은 EarlyStopping이다.
```

![output](assets/3085_problem2_cell049_out03_img30.png)

```text
===시각화 1. 해석:===
==Validation loss curve는 각 정규화 전략이 epoch가 진행되면서 일반화 오차를 어떻게 낮추는지 보여준다.==
------------------
=Baseline은 50 epoch 기준 모델이고, EarlyStopping은 115 epoch까지 학습된 뒤 validation 기준 최저 손실을 기록했다.=
따라서 C5의 핵심은 같은 subset 조건에서 어느 정규화 전략이 validation loss를 가장 낮췄는지 비교하는 것이다.
각 정규화 기법의 해석은 아래 결과표의 val_loss, val_mae, gap을 함께 보고 판단한다.
------------------
==결론: validation curve 기준으로는 EarlyStopping이 가장 낮은 일반화 오차를 보인 최종 후보이다.==
```

![output](assets/3085_problem2_cell049_out05_img31.png)

```text
===시각화 2. 해석:===
Final metric dashboard는 validation loss, validation MAE, train-validation gap을 분리해서 보여준다.
Val Loss는 MSE 기준이므로 큰 오차, 특히 고농도 PM2.5 예측 실패에 더 민감하다.
Val MAE는 실제 PM2.5 단위에서 평균적으로 얼마나 틀리는지를 보여주므로 해석이 직관적이다.
Gap은 train과 validation 사이의 차이를 보여주며, 너무 크면 train에 더 잘 맞는 모델일 수 있다.
------------------
===> EarlyStopping은 Val Loss 5022.91, Val MAE 49.00로 validation 기준 1위다.
Baseline 대비 validation loss는 4.57% 개선되었다.===
------------------
Baseline 대비 개선 여부는 각 모델의 val_loss_improve_pct와 val_mae_delta_vs_baseline으로 판단한다.
Dropout은 train 단계 noise 때문에 gap이 음수로 나올 수 있어, val_loss와 val_mae를 함께 보고 underfitting 여부를 판단한다.
 L2는 gap은 안정적인 편이지만 Val Loss 개선율이 0.23%이므로 최종 후보로 보기는 어렵다.
= 다만 EarlyStopping의 gap은 2374.97이고 Baseline gap은 1269.22이므로, D파트에서 test set과 residual 분석으로 실제 일반화 성능을 반드시 확인해야 한다. =
```

![output](assets/3085_problem2_cell049_out07_img32.png)

```text
===시각화 결론 해석:===
[validation loss와 train-validation gap을 동시에 보는 시각화 맵]
왼쪽에 있을수록 validation loss가 낮아 성능이 좋고, y=0에 가까울수록 train과 validation 손실 차이가 작다.
Baseline 기준선보다 왼쪽에 있는 모델은 validation loss 기준으로 Baseline보다 개선된 모델이다.
EarlyStopping은 validation loss 기준 가장 낮은 위치에 있으므로 최종 후보로 선택된다
=그러나 EarlyStopping의 gap(2374.97)이 Baseline gap(1269.22)보다 크므로, 성능은 가장 좋지만 gap 보완이 필요한 모델로 해석해야 한다.=
------------------
2순위 후보는 L2이며, val_loss=5251.47, 개선율=0.23%이다.
L2는 gap 안정성과 validation 성능 개선폭을 함께 보고 보수적 후보인지 판단한다.
Dropout은 val_loss 위치와 gap 방향을 함께 보고 최종 후보 포함 여부를 판단한다.

최종 판정:
- Validation 기준 1순위 후보: EarlyStopping
- Val Loss: 5022.9136
- Val MAE : 49.0036
- Gap     : 2374.9746
- Baseline 대비 Val Loss 개선율: 4.57%
----따라서 Part D에서는 *EarlyStopping* 모델을 최종 모델로 선택하고, test set에서 최종 일반화 성능을 평가한다.----
```

---
# Part D. 종합 모델 + Test 평가 (5점)

## D1. 최종모델 선택 (5점) - 앞선 실험 결과를 통해 최종 모델을 만들 것 (과적합 및 정규화 효과 등을 고려)

## 이번에는 Test 평가까지 포함하여 최종 모델 성능을 제시할 것

```python
print(' === D1. 최종 모델 선택 ===')

# C5에서 선택한 best_model_name을 기준으로 최종 모델 선택
# C5 결과에서 계산된 best_model_name을 사용한다.

model_dict = {
    'Baseline': baseline_model,
    'Dropout': dropout_model,
    'L2': l2_model,
    'EarlyStopping': earlystop_model,
    'BatchNorm': batchnorm_model
}

if 'best_model_name' not in globals():
    best_model_name = selection_df.loc[0, 'model']

final_model_name = str(best_model_name)
final_model = model_dict[final_model_name]

print(f'Final selected model: {final_model_name}')

display(
    selection_df[
        [
            'abbr',
            'model',
            'val_loss',
            'val_mae',
            'val_rmse',
            'gap',
            'epochs',
            'val_loss_improve_pct',
            'diagnosis_label'
        ]
    ]
)

print('[선택 근거]')
print('C5에서 validation loss를 1순위, validation MAE와 gap을 보조 기준으로 비교했다.')
print(f'{final_model_name}은 validation loss와 validation MAE 기준으로 최종 후보가 되었다.')
print(f'Baseline 대비 validation loss가 {best_model_improve_pct:.2f}% 개선되어 최종 후보로 선택한다.')
print(f'다만 {final_model_name}의 gap({best_model_gap:.2f})과 Baseline gap({baseline_gap:.2f})을 비교하면 gap 보완 여부를 test set에서 반드시 확인해야 한다.')
```

```text
 === D1. 최종 모델 선택 ===
Final selected model: EarlyStopping
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>abbr</th>
      <th>model</th>
      <th>val_loss</th>
      <th>val_mae</th>
      <th>val_rmse</th>
      <th>gap</th>
      <th>epochs</th>
      <th>val_loss_improve_pct</th>
      <th>diagnosis_label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ES</td>
      <td>EarlyStopping</td>
      <td>5022.913574</td>
      <td>49.003605</td>
      <td>70.872516</td>
      <td>2374.974609</td>
      <td>115</td>
      <td>4.570553</td>
      <td>long training + best epoch search</td>
    </tr>
    <tr>
      <th>1</th>
      <td>L2</td>
      <td>L2</td>
      <td>5251.471191</td>
      <td>51.071568</td>
      <td>72.467035</td>
      <td>1208.713379</td>
      <td>50</td>
      <td>0.228227</td>
      <td>mild regularization</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BL</td>
      <td>Baseline</td>
      <td>5263.483887</td>
      <td>51.048092</td>
      <td>72.549872</td>
      <td>1269.219971</td>
      <td>50</td>
      <td>0.000000</td>
      <td>reference</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DO</td>
      <td>Dropout</td>
      <td>5742.844727</td>
      <td>52.515144</td>
      <td>75.781559</td>
      <td>-259.918945</td>
      <td>50</td>
      <td>-9.107292</td>
      <td>strong regularization / possible underfit</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BN</td>
      <td>BatchNorm</td>
      <td>9147.064453</td>
      <td>58.908566</td>
      <td>95.640287</td>
      <td>7673.217529</td>
      <td>50</td>
      <td>-73.783461</td>
      <td>hidden activation stabilization</td>
    </tr>
  </tbody>
</table>
</div>

```text
[선택 근거]
C5에서 validation loss를 1순위, validation MAE와 gap을 보조 기준으로 비교했다.
EarlyStopping은 validation loss와 validation MAE 기준으로 최종 후보가 되었다.
Baseline 대비 validation loss가 4.57% 개선되어 최종 후보로 선택한다.
다만 EarlyStopping의 gap(2374.97)과 Baseline gap(1269.22)을 비교하면 gap 보완 여부를 test set에서 반드시 확인해야 한다.
```

```python
print(' === D2. 최종 모델 Test 평가 ===')

# Test set은 모델 선택에 사용하지 않고, 최종 모델 선택 후 단 한 번 평가한다.
test_loss, test_mae = final_model.evaluate(X_test, y_test, verbose=0)

y_test_pred = final_model.predict(X_test, verbose=0).reshape(-1)

test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)
test_mae_direct = mean_absolute_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)

print(f'Final model      : {final_model_name}')
print(f'Test Loss (MSE)  : {test_loss:.4f}')
print(f'Test MAE         : {test_mae:.4f}')
print(f'Test RMSE        : {test_rmse:.4f}')
print(f'Test R²          : {test_r2:.4f}')

test_result_summary = pd.DataFrame([{
    'final_model': final_model_name,
    'test_loss_mse': test_loss,
    'test_mae': test_mae,
    'test_rmse': test_rmse,
    'test_r2': test_r2
}])

display(test_result_summary)

print('해석:')
print('MSE는 큰 오차에 민감하므로 고농도 PM2.5 예측 실패를 강하게 반영한다.')
print('MAE는 실제 PM2.5 단위에서 평균적으로 얼마나 틀리는지 보여준다.')
print('RMSE는 MSE를 원래 단위로 되돌린 값이며, 큰 오차에 더 민감하다.')
print('R²는 target 변동성 중 모델이 설명한 비율을 의미한다.')
```

```text
 === D2. 최종 모델 Test 평가 ===
```

```text
Final model      : EarlyStopping
Test Loss (MSE)  : 4942.5566
Test MAE         : 48.8242
Test RMSE        : 70.3033
Test R²          : 0.4125
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>final_model</th>
      <th>test_loss_mse</th>
      <th>test_mae</th>
      <th>test_rmse</th>
      <th>test_r2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>EarlyStopping</td>
      <td>4942.556641</td>
      <td>48.824226</td>
      <td>70.303319</td>
      <td>0.412481</td>
    </tr>
  </tbody>
</table>
</div>

```text
해석:
MSE는 큰 오차에 민감하므로 고농도 PM2.5 예측 실패를 강하게 반영한다.
MAE는 실제 PM2.5 단위에서 평균적으로 얼마나 틀리는지 보여준다.
RMSE는 MSE를 원래 단위로 되돌린 값이며, 큰 오차에 더 민감하다.
R²는 target 변동성 중 모델이 설명한 비율을 의미한다.
```

```python
print(' === D3-D4. Baseline vs Selected Model: Test Residual / Bin Error Comparison ===')
print('핵심 질문: 최종 선택 모델이 Baseline 대비 test set에서 실제로 무엇을 얼마나 개선했는가?')
print('D의 결론은 최종 모델 단독 성능이 아니라, Baseline에서 보였던 고농도 과소예측과 구간별 오차가 줄었는지로 판단한다.')

import warnings
warnings.filterwarnings('ignore', message=r'Glyph .* missing from font.*', category=UserWarning)
warnings.filterwarnings('ignore', message=r'.*Glyph .* missing from current font.*', category=UserWarning)

# Plot text is ASCII-only to prevent matplotlib Korean glyph warnings.
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 120

required_names = ['baseline_model', 'final_model', 'final_model_name', 'X_test', 'y_test']
missing_names = [name for name in required_names if name not in globals()]
if missing_names:
    raise NameError(f'D3-D4 비교 분석 전에 필요한 객체가 없습니다: {missing_names}')

y_test_array = np.asarray(y_test).reshape(-1)
baseline_test_pred = baseline_model.predict(X_test, verbose=0).reshape(-1)
selected_test_pred = final_model.predict(X_test, verbose=0).reshape(-1)

# Keep D2 variable name compatible with the previous notebook flow.
y_test_pred = selected_test_pred

baseline_label = 'Baseline'
selected_label = f'Selected ({final_model_name})'
comparison_order = [baseline_label, selected_label]
model_color = {
    baseline_label: '#4E79A7',
    selected_label: '#E15759'
}

def build_eval_frame(model_label, y_pred):
    residual = y_test_array - y_pred
    return pd.DataFrame({
        'model': model_label,
        'y_true': y_test_array,
        'y_pred': y_pred,
        'residual': residual,
        'abs_error': np.abs(residual),
        'squared_error': residual ** 2,
        'underprediction': residual > 0,
        'overprediction': residual < 0
    })

test_eval_baseline_df = build_eval_frame(baseline_label, baseline_test_pred)
test_eval_selected_df = build_eval_frame(selected_label, selected_test_pred)
test_eval_compare_df = pd.concat(
    [test_eval_baseline_df, test_eval_selected_df],
    ignore_index=True
)
test_eval_compare_df['model'] = pd.Categorical(
    test_eval_compare_df['model'],
    categories=comparison_order,
    ordered=True
)

def regression_metric_row(model_label, y_pred):
    residual = y_test_array - y_pred
    mse = mean_squared_error(y_test_array, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test_array, y_pred)
    r2 = r2_score(y_test_array, y_pred)
    return {
        'model': model_label,
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'mean_residual': residual.mean(),
        'median_abs_error': np.median(np.abs(residual)),
        'p95_abs_error': np.quantile(np.abs(residual), 0.95),
        'underprediction_rate': np.mean(residual > 0),
        'overprediction_rate': np.mean(residual < 0)
    }

test_metric_compare = pd.DataFrame([
    regression_metric_row(baseline_label, baseline_test_pred),
    regression_metric_row(selected_label, selected_test_pred)
])

test_metric_compare['model'] = pd.Categorical(
    test_metric_compare['model'],
    categories=comparison_order,
    ordered=True
)
test_metric_compare = test_metric_compare.sort_values('model').reset_index(drop=True)

baseline_metrics = test_metric_compare.set_index('model').loc[baseline_label]
selected_metrics = test_metric_compare.set_index('model').loc[selected_label]

test_metric_delta = pd.DataFrame([
    {
        'metric': 'MSE',
        'baseline': baseline_metrics['mse'],
        'selected': selected_metrics['mse'],
        'delta_selected_minus_baseline': selected_metrics['mse'] - baseline_metrics['mse'],
        'improvement_pct_lower_is_better': (baseline_metrics['mse'] - selected_metrics['mse']) / baseline_metrics['mse'] * 100
    },
    {
        'metric': 'RMSE',
        'baseline': baseline_metrics['rmse'],
        'selected': selected_metrics['rmse'],
        'delta_selected_minus_baseline': selected_metrics['rmse'] - baseline_metrics['rmse'],
        'improvement_pct_lower_is_better': (baseline_metrics['rmse'] - selected_metrics['rmse']) / baseline_metrics['rmse'] * 100
    },
    {
        'metric': 'MAE',
        'baseline': baseline_metrics['mae'],
        'selected': selected_metrics['mae'],
        'delta_selected_minus_baseline': selected_metrics['mae'] - baseline_metrics['mae'],
        'improvement_pct_lower_is_better': (baseline_metrics['mae'] - selected_metrics['mae']) / baseline_metrics['mae'] * 100
    },
    {
        'metric': 'P95 Abs Error',
        'baseline': baseline_metrics['p95_abs_error'],
        'selected': selected_metrics['p95_abs_error'],
        'delta_selected_minus_baseline': selected_metrics['p95_abs_error'] - baseline_metrics['p95_abs_error'],
        'improvement_pct_lower_is_better': (baseline_metrics['p95_abs_error'] - selected_metrics['p95_abs_error']) / baseline_metrics['p95_abs_error'] * 100
    },
    {
        'metric': 'R2',
        'baseline': baseline_metrics['r2'],
        'selected': selected_metrics['r2'],
        'delta_selected_minus_baseline': selected_metrics['r2'] - baseline_metrics['r2'],
        'improvement_pct_lower_is_better': np.nan
    }
])

print('\n[D3-0. Test metric comparison table]')
display(test_metric_compare)
display(test_metric_delta)

print('해석:')
print('- MSE/RMSE/MAE/P95 Abs Error는 낮을수록 좋다. improvement_pct가 양수이면 Baseline 대비 개선이다.')
print('- R2는 높을수록 좋으므로 delta_selected_minus_baseline이 양수이면 설명력이 증가한 것이다.')
print('- mean_residual > 0이면 실제값이 예측값보다 큰 경우가 평균적으로 많아 과소예측 편향이 남아 있다는 뜻이다.')

# ---------------------------------------------------------------------
# Figure 1. Metric delta dashboard
# ---------------------------------------------------------------------
metric_plot = test_metric_delta[test_metric_delta['metric'].isin(['MSE', 'RMSE', 'MAE', 'P95 Abs Error'])].copy()
metric_plot['improvement_pct_lower_is_better'] = metric_plot['improvement_pct_lower_is_better'].astype(float)

fig, axes = plt.subplots(1, 2, figsize=(15, 5.2), constrained_layout=True)

x = np.arange(len(metric_plot))
width = 0.36
axes[0].bar(x - width / 2, metric_plot['baseline'], width=width, label='Baseline', color=model_color[baseline_label], alpha=0.88)
axes[0].bar(x + width / 2, metric_plot['selected'], width=width, label='Selected', color=model_color[selected_label], alpha=0.88)
axes[0].set_xticks(x)
axes[0].set_xticklabels(metric_plot['metric'], rotation=20, ha='right')
axes[0].set_title('D3-1. Test Error Metrics')
axes[0].set_ylabel('Metric value')
axes[0].grid(axis='y', linestyle='--', alpha=0.28)
axes[0].legend()

for i, row in metric_plot.reset_index(drop=True).iterrows():
    ymax = max(row['baseline'], row['selected'])
    axes[0].text(i, ymax, f"{row['improvement_pct_lower_is_better']:+.1f}%", ha='center', va='bottom', fontsize=8.5)

improve_colors = ['#59A14F' if v >= 0 else '#E15759' for v in metric_plot['improvement_pct_lower_is_better']]
axes[1].bar(metric_plot['metric'], metric_plot['improvement_pct_lower_is_better'], color=improve_colors, alpha=0.9)
axes[1].axhline(0, color='#111111', linestyle='--', linewidth=1)
axes[1].set_title('D3-1b. Improvement vs Baseline')
axes[1].set_ylabel('Improvement %, lower-error metrics')
axes[1].tick_params(axis='x', rotation=20)
axes[1].grid(axis='y', linestyle='--', alpha=0.28)
for i, v in enumerate(metric_plot['improvement_pct_lower_is_better']):
    va = 'bottom' if v >= 0 else 'top'
    axes[1].text(i, v, f'{v:+.1f}%', ha='center', va=va, fontsize=8.5)

plt.show()

print('시각화 1 해석:')
print('- 왼쪽 막대그래프는 Baseline과 선택 모델의 test error를 같은 축에서 비교한다.')
print('- 오른쪽 improvement 그래프는 Baseline 대비 오차가 몇 % 줄었는지 직접 보여준다.')
print('- 여기서 양수 개선률이 크면, validation에서 고른 모델이 test에서도 Baseline보다 실질적으로 개선된 것이다.')

# ---------------------------------------------------------------------
# Figure 2. Actual vs predicted, same axis scale
# ---------------------------------------------------------------------
axis_min = float(np.nanmin([y_test_array.min(), baseline_test_pred.min(), selected_test_pred.min()]))
axis_max = float(np.nanmax([y_test_array.max(), baseline_test_pred.max(), selected_test_pred.max()]))
axis_min = min(0.0, axis_min)
axis_pad = max((axis_max - axis_min) * 0.04, 1.0)
axis_min -= axis_pad
axis_max += axis_pad

fig, axes = plt.subplots(1, 2, figsize=(13, 5.8), sharex=True, sharey=True, constrained_layout=True)
for ax, model_label, eval_df in [
    (axes[0], baseline_label, test_eval_baseline_df),
    (axes[1], selected_label, test_eval_selected_df)
]:
    hb = ax.hexbin(
        eval_df['y_true'],
        eval_df['y_pred'],
        gridsize=55,
        mincnt=1,
        cmap='viridis'
    )
    ax.plot([axis_min, axis_max], [axis_min, axis_max], linestyle='--', color='white', linewidth=1.6)
    ax.plot([axis_min, axis_max], [axis_min, axis_max], linestyle='--', color='black', linewidth=0.8)
    ax.set_title(f'Actual vs Predicted: {model_label}')
    ax.set_xlabel('Actual PM2.5')
    ax.set_xlim(axis_min, axis_max)
    ax.set_ylim(axis_min, axis_max)
    ax.grid(True, linestyle='--', alpha=0.2)
    cbar = fig.colorbar(hb, ax=ax)
    cbar.set_label('count')
axes[0].set_ylabel('Predicted PM2.5')
plt.show()

print('시각화 2 해석:')
print('- 두 그래프는 같은 test set, 같은 x/y 축 범위, 같은 대각선 기준으로 비교한다.')
print('- 점이 대각선 아래에 몰리면 실제 PM2.5보다 낮게 예측한 과소예측이다.')
print('- 선택 모델 그래프에서 고농도 영역의 구름이 Baseline보다 대각선에 가까워졌다면 고농도 episode 대응이 개선된 것이다.')
print('- 반대로 고농도 영역이 여전히 대각선 아래에 있으면, 평균 metric이 좋아져도 위험 구간 예측 한계가 남아 있다.')

# ---------------------------------------------------------------------
# Figure 3. Residual overlay and PM2.5-bin comparison
# ---------------------------------------------------------------------
rng_seed = int(SEED) if 'SEED' in globals() else 42
rng = np.random.default_rng(rng_seed)
sample_size = min(3500, len(y_test_array))
sample_idx = rng.choice(len(y_test_array), size=sample_size, replace=False)

q50 = np.quantile(y_test_array, 0.50)
q75 = np.quantile(y_test_array, 0.75)
q95 = np.quantile(y_test_array, 0.95)

def pm25_bin_test(x):
    if x < q50:
        return 'low_<50%'
    elif x < q75:
        return 'mid_50-75%'
    elif x < q95:
        return 'high_75-95%'
    else:
        return 'extreme_>=95%'

bin_order = ['low_<50%', 'mid_50-75%', 'high_75-95%', 'extreme_>=95%']
test_eval_compare_df['pm25_bin'] = test_eval_compare_df['y_true'].apply(pm25_bin_test)
test_eval_compare_df['pm25_bin'] = pd.Categorical(
    test_eval_compare_df['pm25_bin'],
    categories=bin_order,
    ordered=True
)

test_bin_error = test_eval_compare_df.groupby(['model', 'pm25_bin'], observed=False).agg(
    count=('y_true', 'count'),
    y_true_mean=('y_true', 'mean'),
    y_pred_mean=('y_pred', 'mean'),
    mae=('abs_error', 'mean'),
    rmse=('squared_error', lambda s: np.sqrt(np.mean(s))),
    residual_mean=('residual', 'mean'),
    underprediction_rate=('underprediction', 'mean')
).reset_index()

test_bin_error['bias'] = np.where(
    test_bin_error['residual_mean'] > 0,
    'underprediction',
    'overprediction'
)

test_bin_mae_wide = test_bin_error.pivot(index='pm25_bin', columns='model', values='mae').loc[bin_order]
test_bin_residual_wide = test_bin_error.pivot(index='pm25_bin', columns='model', values='residual_mean').loc[bin_order]
test_bin_under_rate_wide = test_bin_error.pivot(index='pm25_bin', columns='model', values='underprediction_rate').loc[bin_order]

test_bin_compare = pd.DataFrame({
    'baseline_mae': test_bin_mae_wide[baseline_label],
    'selected_mae': test_bin_mae_wide[selected_label],
    'mae_delta_selected_minus_baseline': test_bin_mae_wide[selected_label] - test_bin_mae_wide[baseline_label],
    'mae_improvement_pct': (test_bin_mae_wide[baseline_label] - test_bin_mae_wide[selected_label]) / test_bin_mae_wide[baseline_label] * 100,
    'baseline_mean_residual': test_bin_residual_wide[baseline_label],
    'selected_mean_residual': test_bin_residual_wide[selected_label],
    'baseline_underprediction_rate': test_bin_under_rate_wide[baseline_label],
    'selected_underprediction_rate': test_bin_under_rate_wide[selected_label]
})

print('\n[D4-0. PM2.5 bin-wise comparison table]')
display(test_bin_error)
display(test_bin_compare)

fig, axes = plt.subplots(2, 2, figsize=(15, 10), constrained_layout=True)

# 3A. Residual vs actual overlay sampled
for model_label, eval_df in [(baseline_label, test_eval_baseline_df), (selected_label, test_eval_selected_df)]:
    axes[0, 0].scatter(
        eval_df['y_true'].to_numpy()[sample_idx],
        eval_df['residual'].to_numpy()[sample_idx],
        s=8,
        alpha=0.22,
        color=model_color[model_label],
        label=model_label
    )
axes[0, 0].axhline(0, color='#111111', linestyle='--', linewidth=1)
axes[0, 0].set_title('Residual vs Actual PM2.5')
axes[0, 0].set_xlabel('Actual PM2.5')
axes[0, 0].set_ylabel('Residual = Actual - Predicted')
axes[0, 0].grid(True, linestyle='--', alpha=0.25)
axes[0, 0].legend()

# 3B. Residual distribution overlay
bins = np.linspace(
    np.quantile(test_eval_compare_df['residual'], 0.01),
    np.quantile(test_eval_compare_df['residual'], 0.99),
    70
)
for model_label, eval_df in [(baseline_label, test_eval_baseline_df), (selected_label, test_eval_selected_df)]:
    axes[0, 1].hist(
        eval_df['residual'],
        bins=bins,
        density=True,
        alpha=0.42,
        color=model_color[model_label],
        label=model_label
    )
axes[0, 1].axvline(0, color='#111111', linestyle='--', linewidth=1)
axes[0, 1].set_title('Residual Distribution Overlay')
axes[0, 1].set_xlabel('Residual')
axes[0, 1].set_ylabel('Density')
axes[0, 1].grid(True, linestyle='--', alpha=0.25)
axes[0, 1].legend()

# 3C. Bin MAE grouped bar
x = np.arange(len(bin_order))
width = 0.36
axes[1, 0].bar(x - width / 2, test_bin_mae_wide[baseline_label], width=width, color=model_color[baseline_label], alpha=0.88, label=baseline_label)
axes[1, 0].bar(x + width / 2, test_bin_mae_wide[selected_label], width=width, color=model_color[selected_label], alpha=0.88, label=selected_label)
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(bin_order, rotation=20, ha='right')
axes[1, 0].set_title('MAE by PM2.5 Bin')
axes[1, 0].set_ylabel('MAE')
axes[1, 0].grid(axis='y', linestyle='--', alpha=0.25)
axes[1, 0].legend()
for i, b in enumerate(bin_order):
    v = test_bin_compare.loc[b, 'mae_improvement_pct']
    y_top = max(test_bin_mae_wide.loc[b, baseline_label], test_bin_mae_wide.loc[b, selected_label])
    axes[1, 0].text(i, y_top, f'{v:+.1f}%', ha='center', va='bottom', fontsize=8.5)

# 3D. Mean residual by bin line overlay
for model_label in comparison_order:
    axes[1, 1].plot(
        x,
        test_bin_residual_wide[model_label].to_numpy(),
        marker='o',
        linewidth=2,
        color=model_color[model_label],
        label=model_label
    )
axes[1, 1].axhline(0, color='#111111', linestyle='--', linewidth=1)
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(bin_order, rotation=20, ha='right')
axes[1, 1].set_title('Mean Residual by PM2.5 Bin')
axes[1, 1].set_ylabel('Mean residual')
axes[1, 1].grid(True, linestyle='--', alpha=0.25)
axes[1, 1].legend()

plt.show()

extreme_row = test_bin_compare.loc['extreme_>=95%']
overall_mae_improve = float(test_metric_delta.loc[test_metric_delta['metric'] == 'MAE', 'improvement_pct_lower_is_better'].iloc[0])
overall_rmse_improve = float(test_metric_delta.loc[test_metric_delta['metric'] == 'RMSE', 'improvement_pct_lower_is_better'].iloc[0])
extreme_mae_improve = float(extreme_row['mae_improvement_pct'])
extreme_residual_selected = float(extreme_row['selected_mean_residual'])

print('시각화 3 해석:')
print('- Residual overlay는 Baseline과 선택 모델의 오차 구름을 같은 좌표계에 겹쳐서 보여준다.')
print('- Residual distribution overlay에서 선택 모델 분포가 0 주변으로 좁아지면 전체 오차 변동이 줄었다는 뜻이다.')
print('- 농도 구간별 MAE 막대는 평균 성능이 아니라 low/mid/high/extreme 어느 구간에서 개선됐는지 보여준다.')
print('- Mean residual line에서 high/extreme 구간이 양수이면 실제 고농도보다 낮게 예측하는 과소예측이 남아 있는 것이다.')

print('\n[D 최종 비교 결론]')
print(f'- 선택 모델: {final_model_name}')
print(f'- Test MAE 개선율: {overall_mae_improve:+.2f}%')
print(f'- Test RMSE 개선율: {overall_rmse_improve:+.2f}%')
print(f'- Extreme bin MAE 개선율: {extreme_mae_improve:+.2f}%')
print(f'- Extreme bin selected mean residual: {extreme_residual_selected:+.2f}')

if overall_mae_improve > 0 and overall_rmse_improve > 0:
    print('- 결론 1: 선택 모델은 Baseline 대비 test 평균 오차를 줄였다.')
else:
    print('- 결론 1: 선택 모델은 validation 기준으로 선택됐지만 test 평균 오차 개선은 충분하지 않다.')

if extreme_mae_improve > 0:
    print('- 결론 2: extreme PM2.5 구간에서도 Baseline 대비 MAE가 감소했다.')
else:
    print('- 결론 2: extreme PM2.5 구간에서는 Baseline 대비 MAE가 줄지 않아 고농도 episode 예측 한계가 남아 있다.')

if extreme_residual_selected > 0:
    print('- 결론 3: extreme 구간 residual_mean이 양수이므로, 최종 모델도 고농도 PM2.5를 낮게 예측하는 편향이 남아 있다.')
else:
    print('- 결론 3: extreme 구간 평균 residual이 0 이하이므로, 고농도 과소예측 편향은 Baseline보다 완화됐다고 볼 수 있다.')
```

```text
 === D3-D4. Baseline vs Selected Model: Test Residual / Bin Error Comparison ===
핵심 질문: 최종 선택 모델이 Baseline 대비 test set에서 실제로 무엇을 얼마나 개선했는가?
D의 결론은 최종 모델 단독 성능이 아니라, Baseline에서 보였던 고농도 과소예측과 구간별 오차가 줄었는지로 판단한다.
```

```text

[D3-0. Test metric comparison table]
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>mse</th>
      <th>rmse</th>
      <th>mae</th>
      <th>r2</th>
      <th>mean_residual</th>
      <th>median_abs_error</th>
      <th>p95_abs_error</th>
      <th>underprediction_rate</th>
      <th>overprediction_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>5148.777344</td>
      <td>71.754981</td>
      <td>50.660839</td>
      <td>0.387968</td>
      <td>-1.214127</td>
      <td>36.353111</td>
      <td>147.950211</td>
      <td>0.452025</td>
      <td>0.547975</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Selected (EarlyStopping)</td>
      <td>4942.556641</td>
      <td>70.303319</td>
      <td>48.824215</td>
      <td>0.412481</td>
      <td>-1.128010</td>
      <td>33.620968</td>
      <td>146.156387</td>
      <td>0.442898</td>
      <td>0.557102</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>metric</th>
      <th>baseline</th>
      <th>selected</th>
      <th>delta_selected_minus_baseline</th>
      <th>improvement_pct_lower_is_better</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MSE</td>
      <td>5148.777344</td>
      <td>4942.556641</td>
      <td>-206.220703</td>
      <td>4.005236</td>
    </tr>
    <tr>
      <th>1</th>
      <td>RMSE</td>
      <td>71.754981</td>
      <td>70.303319</td>
      <td>-1.451662</td>
      <td>2.023083</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MAE</td>
      <td>50.660839</td>
      <td>48.824215</td>
      <td>-1.836624</td>
      <td>3.625333</td>
    </tr>
    <tr>
      <th>3</th>
      <td>P95 Abs Error</td>
      <td>147.950211</td>
      <td>146.156387</td>
      <td>-1.793823</td>
      <td>1.212451</td>
    </tr>
    <tr>
      <th>4</th>
      <td>R2</td>
      <td>0.387968</td>
      <td>0.412481</td>
      <td>0.024513</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>

```text
해석:
- MSE/RMSE/MAE/P95 Abs Error는 낮을수록 좋다. improvement_pct가 양수이면 Baseline 대비 개선이다.
- R2는 높을수록 좋으므로 delta_selected_minus_baseline이 양수이면 설명력이 증가한 것이다.
- mean_residual > 0이면 실제값이 예측값보다 큰 경우가 평균적으로 많아 과소예측 편향이 남아 있다는 뜻이다.
```

![output](assets/3085_problem2_cell053_out05_img33.png)

```text
시각화 1 해석:
- 왼쪽 막대그래프는 Baseline과 선택 모델의 test error를 같은 축에서 비교한다.
- 오른쪽 improvement 그래프는 Baseline 대비 오차가 몇 % 줄었는지 직접 보여준다.
- 여기서 양수 개선률이 크면, validation에서 고른 모델이 test에서도 Baseline보다 실질적으로 개선된 것이다.
```

![output](assets/3085_problem2_cell053_out07_img34.png)

```text
시각화 2 해석:
- 두 그래프는 같은 test set, 같은 x/y 축 범위, 같은 대각선 기준으로 비교한다.
- 점이 대각선 아래에 몰리면 실제 PM2.5보다 낮게 예측한 과소예측이다.
- 선택 모델 그래프에서 고농도 영역의 구름이 Baseline보다 대각선에 가까워졌다면 고농도 episode 대응이 개선된 것이다.
- 반대로 고농도 영역이 여전히 대각선 아래에 있으면, 평균 metric이 좋아져도 위험 구간 예측 한계가 남아 있다.

[D4-0. PM2.5 bin-wise comparison table]
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>pm25_bin</th>
      <th>count</th>
      <th>y_true_mean</th>
      <th>y_pred_mean</th>
      <th>mae</th>
      <th>rmse</th>
      <th>residual_mean</th>
      <th>underprediction_rate</th>
      <th>bias</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>low_&lt;50%</td>
      <td>4352</td>
      <td>33.184971</td>
      <td>64.871864</td>
      <td>40.322502</td>
      <td>55.040131</td>
      <td>-31.686890</td>
      <td>0.299173</td>
      <td>overprediction</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Baseline</td>
      <td>mid_50-75%</td>
      <td>2205</td>
      <td>101.779137</td>
      <td>118.329559</td>
      <td>37.587124</td>
      <td>47.795727</td>
      <td>-16.550421</td>
      <td>0.360998</td>
      <td>overprediction</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Baseline</td>
      <td>high_75-95%</td>
      <td>1765</td>
      <td>192.043060</td>
      <td>144.310379</td>
      <td>60.136227</td>
      <td>73.685822</td>
      <td>47.732685</td>
      <td>0.805666</td>
      <td>underprediction</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Baseline</td>
      <td>extreme_&gt;=95%</td>
      <td>443</td>
      <td>365.747192</td>
      <td>186.277618</td>
      <td>179.545547</td>
      <td>197.756027</td>
      <td>179.469559</td>
      <td>0.997743</td>
      <td>underprediction</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Selected (EarlyStopping)</td>
      <td>low_&lt;50%</td>
      <td>4352</td>
      <td>33.184971</td>
      <td>61.958050</td>
      <td>36.579159</td>
      <td>52.009247</td>
      <td>-28.773079</td>
      <td>0.271140</td>
      <td>overprediction</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Selected (EarlyStopping)</td>
      <td>mid_50-75%</td>
      <td>2205</td>
      <td>101.779137</td>
      <td>116.262627</td>
      <td>39.725945</td>
      <td>51.995041</td>
      <td>-14.483487</td>
      <td>0.397279</td>
      <td>overprediction</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Selected (EarlyStopping)</td>
      <td>high_75-95%</td>
      <td>1765</td>
      <td>192.043060</td>
      <td>149.152298</td>
      <td>61.955353</td>
      <td>76.347214</td>
      <td>42.890755</td>
      <td>0.786969</td>
      <td>underprediction</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Selected (EarlyStopping)</td>
      <td>extreme_&gt;=95%</td>
      <td>443</td>
      <td>365.747192</td>
      <td>204.195618</td>
      <td>162.087677</td>
      <td>185.843994</td>
      <td>161.551559</td>
      <td>0.986456</td>
      <td>underprediction</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>baseline_mae</th>
      <th>selected_mae</th>
      <th>mae_delta_selected_minus_baseline</th>
      <th>mae_improvement_pct</th>
      <th>baseline_mean_residual</th>
      <th>selected_mean_residual</th>
      <th>baseline_underprediction_rate</th>
      <th>selected_underprediction_rate</th>
    </tr>
    <tr>
      <th>pm25_bin</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>low_&lt;50%</th>
      <td>40.322502</td>
      <td>36.579159</td>
      <td>-3.743343</td>
      <td>9.283510</td>
      <td>-31.686890</td>
      <td>-28.773079</td>
      <td>0.299173</td>
      <td>0.271140</td>
    </tr>
    <tr>
      <th>mid_50-75%</th>
      <td>37.587124</td>
      <td>39.725945</td>
      <td>2.138821</td>
      <td>-5.690301</td>
      <td>-16.550421</td>
      <td>-14.483487</td>
      <td>0.360998</td>
      <td>0.397279</td>
    </tr>
    <tr>
      <th>high_75-95%</th>
      <td>60.136227</td>
      <td>61.955353</td>
      <td>1.819126</td>
      <td>-3.025009</td>
      <td>47.732685</td>
      <td>42.890755</td>
      <td>0.805666</td>
      <td>0.786969</td>
    </tr>
    <tr>
      <th>extreme_&gt;=95%</th>
      <td>179.545547</td>
      <td>162.087677</td>
      <td>-17.457870</td>
      <td>9.723366</td>
      <td>179.469559</td>
      <td>161.551559</td>
      <td>0.997743</td>
      <td>0.986456</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem2_cell053_out11_img35.png)

```text
시각화 3 해석:
- Residual overlay는 Baseline과 선택 모델의 오차 구름을 같은 좌표계에 겹쳐서 보여준다.
- Residual distribution overlay에서 선택 모델 분포가 0 주변으로 좁아지면 전체 오차 변동이 줄었다는 뜻이다.
- 농도 구간별 MAE 막대는 평균 성능이 아니라 low/mid/high/extreme 어느 구간에서 개선됐는지 보여준다.
- Mean residual line에서 high/extreme 구간이 양수이면 실제 고농도보다 낮게 예측하는 과소예측이 남아 있는 것이다.

[D 최종 비교 결론]
- 선택 모델: EarlyStopping
- Test MAE 개선율: +3.63%
- Test RMSE 개선율: +2.02%
- Extreme bin MAE 개선율: +9.72%
- Extreme bin selected mean residual: +161.55
- 결론 1: 선택 모델은 Baseline 대비 test 평균 오차를 줄였다.
- 결론 2: extreme PM2.5 구간에서도 Baseline 대비 MAE가 감소했다.
- 결론 3: extreme 구간 residual_mean이 양수이므로, 최종 모델도 고농도 PM2.5를 낮게 예측하는 편향이 남아 있다.
```

---

# ✅ 제출 전 체크리스트

- [x] STUDENT_ID에 본인 학번을 정확히 입력했나?
- [x] 모든 셀이 위에서 아래로 *실행 가능*한가?
- [x] 모든 필수 출력값이 화면에 나타나는가?

---

# 3085_problem3.ipynb

# 기말고사 문제 3 — Diamonds 분류 분석  〔배포용〕

> 배점: **25점** (Part C 15 + Part D 10) + Part E 보너스  ·  Part A·B(EDA/전처리)는 제공 코드


---

## 📌 시험 안내

### 데이터
- **출처**: seaborn 내장 데이터셋 (`seaborn.load_dataset('diamonds')`)
- **샘플**: 53,940개
- **타겟**: `cut` (5클래스 분류: Fair / Good / Very Good / Premium / Ideal)
- **특성**:
  - 수치형: carat, depth, table, price, x, y, z
  - 범주형: color (7등급), clarity (8등급)

```python
STUDENT_ID = "3085"   # ← 본인 학번 마지막 4자리로 변경
SEED = int(STUDENT_ID)

assert STUDENT_ID != "0000", "학번을 입력하세요!"
print(f'학번(끝4자리): {STUDENT_ID}, SEED: {SEED}')
```

```text
학번(끝4자리): 3085, SEED: 3085
```

## 환경 준비

필요한 라이브러리를 import하고 seed를 고정하세요.
(seaborn, sklearn.metrics 등 분류에 필요한 모듈도 포함)

```python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import keras
from keras import Sequential
from keras.layers import Dense, Dropout, BatchNormalization, Activation
from keras.regularizers import l2
from keras.callbacks import EarlyStopping

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report

# 재현성: 학번 기반 SEED로 고정 (numpy + 현재 keras 백엔드 동시 고정)
np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

print('Keras  :', keras.__version__, '| backend:', keras.backend.backend())
print('pandas :', pd.__version__)
```

```text
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1781880128.169287  488215 port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
I0000 00:00:1781880128.169893  488215 cudart_stub.cc:31] Could not find cuda drivers on your machine, GPU will not be used.
```

```text
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1781880130.493916  488215 port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
I0000 00:00:1781880130.494394  488215 cudart_stub.cc:31] Could not find cuda drivers on your machine, GPU will not be used.
```

```text
Keras  : 3.14.1 | backend: tensorflow
pandas : 3.0.2
```

---
# Part A. EDA + 클래스 분포 (제공 코드)

## A1. 데이터 로드 및 기본 정보 출력

- `seaborn.load_dataset('diamonds')`로 로드
- 데이터 shape, 수치형/범주형 컬럼 목록, 결측치 개수, 기본 통계 출력

```python
df = sns.load_dataset('diamonds')
print(f'Shape: {df.shape}')
print(f'\n수치형 컬럼: {df.select_dtypes(include="number").columns.tolist()}')
print(f'범주형 컬럼: {df.select_dtypes(include="category").columns.tolist()}')
print(f'\n결측치: {df.isnull().sum().sum()}')
print(f'\n기본 통계:')
print(df.describe())
```

```text
Shape: (53940, 10)

수치형 컬럼: ['carat', 'depth', 'table', 'price', 'x', 'y', 'z']
범주형 컬럼: ['cut', 'color', 'clarity']

결측치: 0

기본 통계:
              carat         depth         table         price             x  \
count  53940.000000  53940.000000  53940.000000  53940.000000  53940.000000   
mean       0.797940     61.749405     57.457184   3932.799722      5.731157   
std        0.474011      1.432621      2.234491   3989.439738      1.121761   
min        0.200000     43.000000     43.000000    326.000000      0.000000   
25%        0.400000     61.000000     56.000000    950.000000      4.710000   
50%        0.700000     61.800000     57.000000   2401.000000      5.700000   
75%        1.040000     62.500000     59.000000   5324.250000      6.540000   
max        5.010000     79.000000     95.000000  18823.000000     10.740000   

                  y             z  
count  53940.000000  53940.000000  
mean       5.734526      3.538734  
std        1.142135      0.705699  
min        0.000000      0.000000  
25%        4.720000      2.910000  
50%        5.710000      3.530000  
75%        6.540000      4.040000  
max       58.900000     31.800000  
```

## A2. 타겟 변수(cut) 클래스 분포

- 각 클래스 개수와 비율을 출력
- 막대 그래프로 시각화 (제목/축 라벨 포함)
- 클래스 불균형 비율 계산 (최대 클래스 / 최소 클래스)

```python
print('cut (타겟) 분포:')
print(df['cut'].value_counts())
print()
print('비율:')
print(df['cut'].value_counts(normalize=True).round(3))

# 시각화
plt.figure(figsize=(8, 4))
df['cut'].value_counts().plot(kind='bar', color='steelblue')
plt.title('Class Distribution (Cut)')
plt.xlabel('Cut')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.grid(alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# 클래스 불균형 비율 계산
imbalance_ratio = df['cut'].value_counts().max() / df['cut'].value_counts().min()
print(f'\n클래스 불균형 비율 (최대/최소): {imbalance_ratio:.1f}배')
```

```text
cut (타겟) 분포:
cut
Ideal        21551
Premium      13791
Very Good    12082
Good          4906
Fair          1610
Name: count, dtype: int64

비율:
cut
Ideal        0.400
Premium      0.256
Very Good    0.224
Good         0.091
Fair         0.030
Name: proportion, dtype: float64
```

![output](assets/3085_problem3_cell007_out01_img01.png)

```text

클래스 불균형 비율 (최대/최소): 13.4배
```

## A3. 이상치 탐지 및 처리

데이터의 `x`, `y`, `z` (다이아몬드 크기) 컬럼에 *0값*이 존재할 수 있습니다.
이는 측정 오류로 추정됩니다.

- 각 컬럼별 0값 개수 출력
- 이상치를 처리한 후 데이터 shape 출력

```python
# x, y, z (다이아몬드 크기)에 0값(이상치) 존재 여부 확인
for col in ['x', 'y', 'z']:
    zeros = (df[col] == 0).sum()
    print(f'{col}: 0 values = {zeros}')

# 이상치 처리: x, y, z 중 0인 행 제거
df_clean = df[(df['x'] > 0) & (df['y'] > 0) & (df['z'] > 0)].copy()
print(f'\n이상치 제거 후 shape: {df_clean.shape}')
```

```text
x: 0 values = 8
y: 0 values = 7
z: 0 values = 20
```

```text

이상치 제거 후 shape: (53920, 10)
```

---
# Part B. 범주형 인코딩 전처리 (제공 코드)

## B1. Ordinal Encoding (color, clarity)

`color`와 `clarity`는 **순서가 있는** 범주형 변수입니다:
- color: D(최고) → J(최하)
- clarity: IF(최고) → I1(최하)

**필요사항**:
- 순서를 보존하는 Ordinal Encoding 적용
- 인코딩 후 결과 검증 (예: 등급별 매핑 출력)

```python
# 순서 정의 (등급 좋은 순으로 높은 숫자)
color_order = ['J', 'I', 'H', 'G', 'F', 'E', 'D']           # D가 최고
clarity_order = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']  # IF가 최고

color_map = {c: i for i, c in enumerate(color_order)}
clarity_map = {c: i for i, c in enumerate(clarity_order)}

df_clean['color_ord']   = df_clean['color'].map(color_map)
df_clean['clarity_ord'] = df_clean['clarity'].map(clarity_map)

print('color 인코딩 확인:')
print(df_clean[['color', 'color_ord']].drop_duplicates().sort_values('color_ord'))
print()
print('clarity 인코딩 확인:')
print(df_clean[['clarity', 'clarity_ord']].drop_duplicates().sort_values('clarity_ord'))
```

```text
color 인코딩 확인:
   color color_ord
28     D         6
0      E         5
12     F         4
25     G         3
7      H         2
3      I         1
4      J         0

clarity 인코딩 확인:
    clarity clarity_ord
229      IF           7
6      VVS1           6
5      VVS2           5
2       VS1           4
3       VS2           3
1       SI1           2
0       SI2           1
15       I1           0
```

## B2. 타겟 인코딩

- `cut` 타겟을 정수로 인코딩 (Fair=0, Good=1, Very Good=2, Premium=3, Ideal=4)

**출력**:
- 인코딩 후 결과 검증 (예: 클래스별 매핑 출력)

```python
# 타겟 인코딩
cut_order = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
cut_map = {c: i for i, c in enumerate(cut_order)}

df_clean['cut_label'] = df_clean['cut'].map(cut_map)

print('cut 인코딩:')
print(df_clean[['cut', 'cut_label']].drop_duplicates().sort_values('cut_label'))
```

```text
cut 인코딩:
         cut cut_label
0      Ideal         4
1    Premium         3
5  Very Good         2
2       Good         1
8       Fair         0
```

## B3. Feature 선택 + 3분할 + 정규화

- Feature 선택 (수치형 + 인코딩한 범주형)
- 3분할 (60/20/20)
- **반드시 `stratify=y` 사용** (클래스 비율 유지)
- StandardScaler로 정규화

> 💡 **stratify=y**: 클래스 분포가 불균형하므로 분할 시 비율 유지 필수

**출력**:
- X_train, X_val, X_test shape
- 분할 후 각 클래스 비율이 유지되는지 확인 (예: train의 y_train 분포)

```python
# Feature 선택
feature_cols = ['carat', 'depth', 'table', 'price', 'x', 'y', 'z',
                'color_ord', 'clarity_ord']
X = df_clean[feature_cols].values.astype(np.float32)
y = df_clean['cut_label'].values.astype(np.int32)

print(f'X: {X.shape}, y: {y.shape}')
print(f'클래스 수: {len(np.unique(y))}')

# 3분할 (60/20/20)
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y  # 클래스 비율 유지
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=SEED, stratify=y_temp
)

# 정규화
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)
X_test  = scaler.transform(X_test)

print(f'\nTrain: {X_train.shape}')
print(f'Val  : {X_val.shape}')
print(f'Test : {X_test.shape}')

# 분할 후 클래스 비율 유지 확인
print('\n[클래스 비율 유지 확인]')
for name, yy in [('train', y_train), ('val', y_val), ('test', y_test)]:
    ratio = pd.Series(yy).value_counts(normalize=True).sort_index().round(3).tolist()
    print(f'  {name:5s}: {ratio}')
```

```text
X: (53920, 9), y: (53920,)
클래스 수: 5

Train: (32352, 9)
Val  : (10784, 9)
Test : (10784, 9)

[클래스 비율 유지 확인]
  train: [0.03, 0.091, 0.224, 0.256, 0.4]
  val  : [0.03, 0.091, 0.224, 0.256, 0.4]
  test : [0.03, 0.091, 0.224, 0.256, 0.4]
```

---
# Part C. 분류 모델 구축 (15점)

## C0. (추가입니다._EDA)

## C0. 제공 split 보존 EDA와 모델링 결정

이 섹션은 A/B 제공 전처리 코드를 수정하지 않고, 제공된 `X_train`, `X_val` 뒤의 원본 행만 복원해 모델 설계 근거를 설명한다. `X_test`는 Part D 전까지 열지 않는다.

핵심 모델링 결정은 다음과 같다.

- Target은 `Fair=0`부터 `Ideal=4`까지의 5-class ordinal multiclass 문제다. 모델은 시험 요구에 맞게 softmax와 sparse categorical cross-entropy를 사용하고, 순서형 오차는 `ordinal_mae`로 보조 확인한다.
- 직접 geometry 신호는 `table`, `depth`, `xy_ratio`, `z_to_xy_mean`이다. 이 변수들은 cut과 연결되는 비율/형태 정보를 담는다.
- `carat`, `x`, `y`, `z`, `volume`, `price`는 강한 size-price 중복 축을 형성한다.
- `Fair`, `Good`은 소수 클래스이므로 accuracy만 보지 않고 macro-F1, balanced accuracy, class별 recall, ordinal MAE를 함께 본다.
- 최종 mandatory 모델은 test를 보기 전에 validation metric 기준으로 선택한다.

```python
print('=== C0-1. Rebuild split metadata without opening test EDA ===')

from IPython.display import display, Markdown
from scipy.stats import spearmanr, kruskal, chi2_contingency
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    balanced_accuracy_score,
    confusion_matrix,
    classification_report,
)
from sklearn.utils.class_weight import compute_class_weight

# Recreate only positional indices using the exact B3 split logic.
# The provided X_train, X_val, X_test, y_train, y_val, y_test arrays are not changed.
idx_all = np.arange(len(df_clean), dtype=np.int64)

idx_temp, idx_test_locked, y_temp_idx, y_test_idx_locked = train_test_split(
    idx_all,
    y,
    test_size=0.2,
    random_state=SEED,
    stratify=y,
)

idx_train, idx_val, y_train_idx, y_val_idx = train_test_split(
    idx_temp,
    y_temp_idx,
    test_size=0.25,
    random_state=SEED,
    stratify=y_temp_idx,
)

train_meta = df_clean.iloc[idx_train].copy()
val_meta = df_clean.iloc[idx_val].copy()

train_X_raw_recovered = scaler.inverse_transform(X_train)
val_X_raw_recovered = scaler.inverse_transform(X_val)

train_alignment = (
    np.array_equal(y_train_idx.astype(np.int32), y_train)
    and np.array_equal(train_meta['cut_label'].to_numpy(np.int32), y_train)
    and np.allclose(
        train_X_raw_recovered,
        train_meta[feature_cols].to_numpy(np.float32),
        rtol=1e-5,
        atol=1e-3,
    )
)

val_alignment = (
    np.array_equal(y_val_idx.astype(np.int32), y_val)
    and np.array_equal(val_meta['cut_label'].to_numpy(np.int32), y_val)
    and np.allclose(
        val_X_raw_recovered,
        val_meta[feature_cols].to_numpy(np.float32),
        rtol=1e-5,
        atol=1e-3,
    )
)

assert train_alignment, 'train_meta is not aligned with provided X_train/y_train.'
assert val_alignment, 'val_meta is not aligned with provided X_val/y_val.'

print('train alignment:', train_alignment, '| shape:', train_meta.shape)
print('val alignment  :', val_alignment, '| shape:', val_meta.shape)
print('test           : locked until Part D')


def add_diagnostic_features(frame):
    """Create diagnostic-only geometry/price features without changing mandatory X."""
    out = frame.copy()
    xy_mean = (out['x'] + out['y']) / 2.0
    out['volume'] = out['x'] * out['y'] * out['z']
    out['xy_ratio'] = out['x'] / out['y']
    out['z_to_xy_mean'] = out['z'] / xy_mean
    out['price_per_carat'] = out['price'] / out['carat']
    return out


train_eda = add_diagnostic_features(train_meta)
val_eda = add_diagnostic_features(val_meta)

print('train_eda shape:', train_eda.shape)
print('val_eda shape  :', val_eda.shape)
```

```text
=== C0-1. Rebuild split metadata without opening test EDA ===
train alignment: True | shape: (32352, 13)
val alignment  : True | shape: (10784, 13)
test           : locked until Part D
train_eda shape: (32352, 17)
val_eda shape  : (10784, 17)
```

```python
print('=== C0-2. Train/validation class balance ===')

class_ids = np.arange(len(cut_order))

train_counts = pd.Series(y_train).value_counts().reindex(class_ids, fill_value=0)
val_counts = pd.Series(y_val).value_counts().reindex(class_ids, fill_value=0)

split_distribution = pd.DataFrame({
    'class_id': class_ids,
    'class_name': cut_order,
    'train_count': train_counts.to_numpy(),
    'train_ratio': (train_counts / len(y_train)).to_numpy(),
    'val_count': val_counts.to_numpy(),
    'val_ratio': (val_counts / len(y_val)).to_numpy(),
})

display(split_distribution)

fig, ax = plt.subplots(figsize=(9, 4))
x_pos = np.arange(len(cut_order))
width = 0.38
ax.bar(x_pos - width / 2, split_distribution['train_ratio'], width=width, label='Train')
ax.bar(x_pos + width / 2, split_distribution['val_ratio'], width=width, label='Validation')
ax.set_title('Cut class ratio: train vs validation')
ax.set_xlabel('Cut class')
ax.set_ylabel('Ratio')
ax.set_xticks(x_pos)
ax.set_xticklabels(cut_order, rotation=20)
ax.legend()
ax.grid(alpha=0.25, axis='y')
plt.tight_layout()
plt.show()

balanced_weights = compute_class_weight(
    class_weight='balanced',
    classes=class_ids,
    y=y_train,
)

class_weight_dict = {
    int(c): float(w)
    for c, w in zip(class_ids, balanced_weights)
}

print('Candidate class weights from train split:')
for class_id, class_name in enumerate(cut_order):
    print(f'  {class_name:10s} ({class_id}): {class_weight_dict[class_id]:.4f}')

print('\nModeling implication:')
print('- Fair/Good are minority classes, so accuracy alone is not enough.')
print('- C1/C2 remain unweighted for the mandatory controlled comparison.')
print('- Validation macro-F1 is the primary selection metric; ordinal MAE is a supplementary error-distance check.')
print('- class_weight is isolated as the optional Part E experiment.')
```

```text
=== C0-2. Train/validation class balance ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>class_id</th>
      <th>class_name</th>
      <th>train_count</th>
      <th>train_ratio</th>
      <th>val_count</th>
      <th>val_ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>Fair</td>
      <td>965</td>
      <td>0.029828</td>
      <td>322</td>
      <td>0.029859</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Good</td>
      <td>2942</td>
      <td>0.090937</td>
      <td>980</td>
      <td>0.090875</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Very Good</td>
      <td>7249</td>
      <td>0.224067</td>
      <td>2416</td>
      <td>0.224036</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>Premium</td>
      <td>8268</td>
      <td>0.255564</td>
      <td>2756</td>
      <td>0.255564</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Ideal</td>
      <td>12928</td>
      <td>0.399604</td>
      <td>4310</td>
      <td>0.399666</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem3_cell019_out02_img02.png)

```text
Candidate class weights from train split:
  Fair       (0): 6.7051
  Good       (1): 2.1993
  Very Good  (2): 0.8926
  Premium    (3): 0.7826
  Ideal      (4): 0.5005

Modeling implication:
- Fair/Good are minority classes, so accuracy alone is not enough.
- C1/C2 remain unweighted for the mandatory controlled comparison.
- Validation macro-F1 is the primary selection metric; ordinal MAE is a supplementary error-distance check.
- class_weight is isolated as the optional Part E experiment.
```

```python
print('=== C0-3. Train-only numeric evidence for cut separation ===')

numeric_eda_cols = [
    'carat', 'depth', 'table', 'price', 'x', 'y', 'z',
    'volume', 'xy_ratio', 'z_to_xy_mean', 'price_per_carat',
]

numeric_rows = []

for col in numeric_eda_cols:
    rho, spearman_p = spearmanr(train_eda[col], train_eda['cut_label'])

    groups = [
        train_eda.loc[train_eda['cut_label'] == class_id, col].to_numpy()
        for class_id in class_ids
    ]

    h_stat, kw_p = kruskal(*groups)

    n = len(train_eda)
    k = len(class_ids)
    epsilon_sq = max(0.0, (h_stat - k + 1) / (n - k))

    numeric_rows.append({
        'feature': col,
        'spearman_corr': rho,
        'spearman_p_value': spearman_p,
        'kruskal_stat': h_stat,
        'kruskal_p_value': kw_p,
        'epsilon_sq_effect': epsilon_sq,
    })

numeric_train_result = (
    pd.DataFrame(numeric_rows)
    .sort_values(['epsilon_sq_effect', 'feature'], ascending=[False, True])
    .reset_index(drop=True)
)

top_numeric_features = numeric_train_result.head(6)['feature'].tolist()
display(numeric_train_result)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

plot_effect = numeric_train_result.sort_values('epsilon_sq_effect')
axes[0].barh(plot_effect['feature'], plot_effect['epsilon_sq_effect'])
axes[0].set_title('Train Kruskal-Wallis effect size')
axes[0].set_xlabel('Epsilon squared')

plot_rho = numeric_train_result.sort_values('spearman_corr')
axes[1].barh(plot_rho['feature'], plot_rho['spearman_corr'])
axes[1].axvline(0, linestyle='--', linewidth=1)
axes[1].set_title('Train Spearman correlation with cut_label')
axes[1].set_xlabel('Spearman correlation')

plt.tight_layout()
plt.show()

display(Markdown(f"""
**EDA 해석.** `table`은 train 기준에서 가장 강한 geometry 신호다. `xy_ratio`, `depth`, `z_to_xy_mean`도 단조 상관이 아주 크지 않더라도 class별 분포를 분리한다. 반면 `carat/x/y/z/volume/price`는 독립적인 cut 원인이라기보다 중복된 size-price 축으로 해석한다.

**상위 numeric 근거:** `{', '.join(top_numeric_features)}`.
"""))
```

```text
=== C0-3. Train-only numeric evidence for cut separation ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature</th>
      <th>spearman_corr</th>
      <th>spearman_p_value</th>
      <th>kruskal_stat</th>
      <th>kruskal_p_value</th>
      <th>epsilon_sq_effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>table</td>
      <td>-0.474184</td>
      <td>0.000000e+00</td>
      <td>12377.980218</td>
      <td>0.000000e+00</td>
      <td>0.382539</td>
    </tr>
    <tr>
      <th>1</th>
      <td>xy_ratio</td>
      <td>0.019192</td>
      <td>5.561949e-04</td>
      <td>6605.139958</td>
      <td>0.000000e+00</td>
      <td>0.204073</td>
    </tr>
    <tr>
      <th>2</th>
      <td>depth</td>
      <td>-0.206900</td>
      <td>9.862443e-310</td>
      <td>3551.828548</td>
      <td>0.000000e+00</td>
      <td>0.109680</td>
    </tr>
    <tr>
      <th>3</th>
      <td>z_to_xy_mean</td>
      <td>-0.207077</td>
      <td>2.860125e-310</td>
      <td>3526.733699</td>
      <td>0.000000e+00</td>
      <td>0.108904</td>
    </tr>
    <tr>
      <th>4</th>
      <td>z</td>
      <td>-0.149802</td>
      <td>1.087375e-161</td>
      <td>1148.984762</td>
      <td>1.824604e-247</td>
      <td>0.035397</td>
    </tr>
    <tr>
      <th>5</th>
      <td>carat</td>
      <td>-0.139452</td>
      <td>3.535842e-140</td>
      <td>1127.456812</td>
      <td>8.466494e-243</td>
      <td>0.034731</td>
    </tr>
    <tr>
      <th>6</th>
      <td>x</td>
      <td>-0.125211</td>
      <td>3.497005e-113</td>
      <td>1113.486900</td>
      <td>9.032882e-240</td>
      <td>0.034300</td>
    </tr>
    <tr>
      <th>7</th>
      <td>volume</td>
      <td>-0.127411</td>
      <td>3.706139e-117</td>
      <td>988.062660</td>
      <td>1.378962e-212</td>
      <td>0.030422</td>
    </tr>
    <tr>
      <th>8</th>
      <td>y</td>
      <td>-0.126108</td>
      <td>8.556363e-115</td>
      <td>932.112425</td>
      <td>1.835388e-200</td>
      <td>0.028692</td>
    </tr>
    <tr>
      <th>9</th>
      <td>price</td>
      <td>-0.094100</td>
      <td>1.559135e-64</td>
      <td>614.333321</td>
      <td>1.224616e-131</td>
      <td>0.018868</td>
    </tr>
    <tr>
      <th>10</th>
      <td>price_per_carat</td>
      <td>-0.025139</td>
      <td>6.119573e-06</td>
      <td>186.949308</td>
      <td>2.397667e-39</td>
      <td>0.005656</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem3_cell020_out02_img03.png)


**EDA 해석.** `table`은 train 기준에서 가장 강한 geometry 신호다. `xy_ratio`, `depth`, `z_to_xy_mean`도 단조 상관이 아주 크지 않더라도 class별 분포를 분리한다. 반면 `carat/x/y/z/volume/price`는 독립적인 cut 원인이라기보다 중복된 size-price 축으로 해석한다.

**상위 numeric 근거:** `table, xy_ratio, depth, z_to_xy_mean, z, carat`.

```python
print('=== C0-4. Train-only categorical association with cut ===')


def corrected_cramers_v(contingency):
    """Bias-corrected Cramer's V for a contingency table."""
    chi2, p_value, dof, _ = chi2_contingency(contingency)
    n = contingency.to_numpy().sum()
    r, k = contingency.shape

    phi2 = chi2 / n
    phi2_corr = max(0.0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    r_corr = r - ((r - 1) ** 2) / (n - 1)
    k_corr = k - ((k - 1) ** 2) / (n - 1)
    denom = min(k_corr - 1, r_corr - 1)

    v = np.sqrt(phi2_corr / denom) if denom > 0 else 0.0
    return chi2, p_value, dof, v


category_orders = {
    'color': color_order,
    'clarity': clarity_order,
}

categorical_rows = []

for col, category_order in category_orders.items():
    count_table = pd.crosstab(train_eda[col], train_eda['cut']).reindex(
        index=category_order,
        columns=cut_order,
        fill_value=0,
    )

    ratio_table = count_table.div(count_table.sum(axis=1), axis=0)

    chi2, p_value, dof, cramers_v = corrected_cramers_v(count_table)

    print(f'\n--- Train {col} x cut count ---')
    display(count_table)

    print(f'--- Train {col} x cut row ratio ---')
    display(ratio_table)

    ratio_table.plot(kind='bar', stacked=True, figsize=(10, 4))
    plt.title(f'Train cut ratio by {col}')
    plt.xlabel(col)
    plt.ylabel('Row ratio')
    plt.legend(title='cut', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    categorical_rows.append({
        'feature': col,
        'chi2': chi2,
        'p_value': p_value,
        'dof': dof,
        'cramers_v': cramers_v,
    })

categorical_train_result = (
    pd.DataFrame(categorical_rows)
    .sort_values('cramers_v', ascending=False)
    .reset_index(drop=True)
)

display(categorical_train_result)

display(Markdown("""
**범주형 해석.** 이 train split에서는 `clarity`가 `color`보다 cut과 더 강하게 관련되지만, 둘 다 핵심 geometry 신호보다는 약하다. 제공된 ordinal encoding은 등급 순서를 보존하므로 그대로 유지하고, hidden layer가 비선형 상호작용을 학습하도록 둔다.
"""))
```

```text
=== C0-4. Train-only categorical association with cut ===

--- Train color x cut count ---
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>cut</th>
      <th>Fair</th>
      <th>Good</th>
      <th>Very Good</th>
      <th>Premium</th>
      <th>Ideal</th>
    </tr>
    <tr>
      <th>color</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>J</th>
      <td>74</td>
      <td>178</td>
      <td>391</td>
      <td>482</td>
      <td>548</td>
    </tr>
    <tr>
      <th>I</th>
      <td>102</td>
      <td>328</td>
      <td>719</td>
      <td>843</td>
      <td>1210</td>
    </tr>
    <tr>
      <th>H</th>
      <td>175</td>
      <td>421</td>
      <td>1084</td>
      <td>1403</td>
      <td>1846</td>
    </tr>
    <tr>
      <th>G</th>
      <td>193</td>
      <td>535</td>
      <td>1426</td>
      <td>1772</td>
      <td>2975</td>
    </tr>
    <tr>
      <th>F</th>
      <td>196</td>
      <td>537</td>
      <td>1252</td>
      <td>1437</td>
      <td>2300</td>
    </tr>
    <tr>
      <th>E</th>
      <td>133</td>
      <td>548</td>
      <td>1464</td>
      <td>1405</td>
      <td>2358</td>
    </tr>
    <tr>
      <th>D</th>
      <td>92</td>
      <td>395</td>
      <td>913</td>
      <td>926</td>
      <td>1691</td>
    </tr>
  </tbody>
</table>
</div>

```text
--- Train color x cut row ratio ---
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>cut</th>
      <th>Fair</th>
      <th>Good</th>
      <th>Very Good</th>
      <th>Premium</th>
      <th>Ideal</th>
    </tr>
    <tr>
      <th>color</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>J</th>
      <td>0.044232</td>
      <td>0.106396</td>
      <td>0.233712</td>
      <td>0.288105</td>
      <td>0.327555</td>
    </tr>
    <tr>
      <th>I</th>
      <td>0.031855</td>
      <td>0.102436</td>
      <td>0.224547</td>
      <td>0.263273</td>
      <td>0.377889</td>
    </tr>
    <tr>
      <th>H</th>
      <td>0.035504</td>
      <td>0.085413</td>
      <td>0.219923</td>
      <td>0.284642</td>
      <td>0.374518</td>
    </tr>
    <tr>
      <th>G</th>
      <td>0.027967</td>
      <td>0.077525</td>
      <td>0.206637</td>
      <td>0.256774</td>
      <td>0.431097</td>
    </tr>
    <tr>
      <th>F</th>
      <td>0.034254</td>
      <td>0.093848</td>
      <td>0.218805</td>
      <td>0.251136</td>
      <td>0.401957</td>
    </tr>
    <tr>
      <th>E</th>
      <td>0.022512</td>
      <td>0.092756</td>
      <td>0.247800</td>
      <td>0.237813</td>
      <td>0.399120</td>
    </tr>
    <tr>
      <th>D</th>
      <td>0.022903</td>
      <td>0.098332</td>
      <td>0.227284</td>
      <td>0.230520</td>
      <td>0.420961</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem3_cell021_out04_img04.png)

```text

--- Train clarity x cut count ---
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>cut</th>
      <th>Fair</th>
      <th>Good</th>
      <th>Very Good</th>
      <th>Premium</th>
      <th>Ideal</th>
    </tr>
    <tr>
      <th>clarity</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>I1</th>
      <td>126</td>
      <td>52</td>
      <td>51</td>
      <td>120</td>
      <td>87</td>
    </tr>
    <tr>
      <th>SI2</th>
      <td>284</td>
      <td>645</td>
      <td>1258</td>
      <td>1800</td>
      <td>1548</td>
    </tr>
    <tr>
      <th>SI1</th>
      <td>230</td>
      <td>947</td>
      <td>1897</td>
      <td>2125</td>
      <td>2546</td>
    </tr>
    <tr>
      <th>VS2</th>
      <td>164</td>
      <td>578</td>
      <td>1559</td>
      <td>2015</td>
      <td>3054</td>
    </tr>
    <tr>
      <th>VS1</th>
      <td>104</td>
      <td>383</td>
      <td>1063</td>
      <td>1217</td>
      <td>2141</td>
    </tr>
    <tr>
      <th>VVS2</th>
      <td>42</td>
      <td>180</td>
      <td>787</td>
      <td>510</td>
      <td>1585</td>
    </tr>
    <tr>
      <th>VVS1</th>
      <td>12</td>
      <td>113</td>
      <td>477</td>
      <td>348</td>
      <td>1249</td>
    </tr>
    <tr>
      <th>IF</th>
      <td>3</td>
      <td>44</td>
      <td>157</td>
      <td>133</td>
      <td>718</td>
    </tr>
  </tbody>
</table>
</div>

```text
--- Train clarity x cut row ratio ---
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>cut</th>
      <th>Fair</th>
      <th>Good</th>
      <th>Very Good</th>
      <th>Premium</th>
      <th>Ideal</th>
    </tr>
    <tr>
      <th>clarity</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>I1</th>
      <td>0.288991</td>
      <td>0.119266</td>
      <td>0.116972</td>
      <td>0.275229</td>
      <td>0.199541</td>
    </tr>
    <tr>
      <th>SI2</th>
      <td>0.051310</td>
      <td>0.116531</td>
      <td>0.227281</td>
      <td>0.325203</td>
      <td>0.279675</td>
    </tr>
    <tr>
      <th>SI1</th>
      <td>0.029697</td>
      <td>0.122272</td>
      <td>0.244932</td>
      <td>0.274371</td>
      <td>0.328728</td>
    </tr>
    <tr>
      <th>VS2</th>
      <td>0.022252</td>
      <td>0.078426</td>
      <td>0.211533</td>
      <td>0.273406</td>
      <td>0.414383</td>
    </tr>
    <tr>
      <th>VS1</th>
      <td>0.021190</td>
      <td>0.078036</td>
      <td>0.216585</td>
      <td>0.247963</td>
      <td>0.436227</td>
    </tr>
    <tr>
      <th>VVS2</th>
      <td>0.013531</td>
      <td>0.057990</td>
      <td>0.253544</td>
      <td>0.164304</td>
      <td>0.510631</td>
    </tr>
    <tr>
      <th>VVS1</th>
      <td>0.005457</td>
      <td>0.051387</td>
      <td>0.216917</td>
      <td>0.158254</td>
      <td>0.567985</td>
    </tr>
    <tr>
      <th>IF</th>
      <td>0.002844</td>
      <td>0.041706</td>
      <td>0.148815</td>
      <td>0.126066</td>
      <td>0.680569</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem3_cell021_out09_img05.png)

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature</th>
      <th>chi2</th>
      <th>p_value</th>
      <th>dof</th>
      <th>cramers_v</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>clarity</td>
      <td>2725.764739</td>
      <td>0.000000e+00</td>
      <td>28</td>
      <td>0.144394</td>
    </tr>
    <tr>
      <th>1</th>
      <td>color</td>
      <td>189.393494</td>
      <td>1.162032e-27</td>
      <td>24</td>
      <td>0.035752</td>
    </tr>
  </tbody>
</table>
</div>


**범주형 해석.** 이 train split에서는 `clarity`가 `color`보다 cut과 더 강하게 관련되지만, 둘 다 핵심 geometry 신호보다는 약하다. 제공된 ordinal encoding은 등급 순서를 보존하므로 그대로 유지하고, hidden layer가 비선형 상호작용을 학습하도록 둔다.

```python
print('=== C0-5. Redundancy and geometry anomaly checks ===')

corr_cols = [
    'carat', 'depth', 'table', 'price', 'x', 'y', 'z',
    'volume', 'xy_ratio', 'z_to_xy_mean', 'price_per_carat',
    'color_ord', 'clarity_ord',
]

train_corr = train_eda[corr_cols].corr(method='spearman')

plt.figure(figsize=(12, 9))
sns.heatmap(train_corr, cmap='coolwarm', center=0, vmin=-1, vmax=1)
plt.title('Train Spearman correlation among candidate features')
plt.tight_layout()
plt.show()

pair_rows = []

for i, col_1 in enumerate(corr_cols):
    for col_2 in corr_cols[i + 1:]:
        corr_value = train_corr.loc[col_1, col_2]
        pair_rows.append({
            'feature_1': col_1,
            'feature_2': col_2,
            'spearman_corr': corr_value,
            'abs_corr': abs(corr_value),
        })

high_corr_pairs = (
    pd.DataFrame(pair_rows)
    .sort_values('abs_corr', ascending=False)
    .reset_index(drop=True)
)

print('Top redundancy pairs:')
display(high_corr_pairs.head(20))

geometry_check_cols = ['x', 'y', 'z', 'volume', 'xy_ratio', 'z_to_xy_mean']

outlier_rows = []

for col in geometry_check_cols:
    q1 = train_eda[col].quantile(0.25)
    q3 = train_eda[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (train_eda[col] < lower) | (train_eda[col] > upper)

    outlier_rows.append({
        'feature': col,
        'min': train_eda[col].min(),
        'q01': train_eda[col].quantile(0.01),
        'median': train_eda[col].median(),
        'q99': train_eda[col].quantile(0.99),
        'max': train_eda[col].max(),
        'iqr_outlier_count': int(mask.sum()),
        'iqr_outlier_ratio': float(mask.mean()),
    })

geometry_outlier_summary = pd.DataFrame(outlier_rows)
display(geometry_outlier_summary)

display(Markdown("""
**모델링 해석.** size-price 축(`carat/x/y/z/volume/price`)은 매우 강하게 중복되어 있다. `depth`와 `z_to_xy_mean`도 거의 같은 proportion 신호로 볼 수 있다. B3 이후 mandatory feature를 추가하거나 제거하지 않고, Regularized 모델에서 L2, BatchNorm, Dropout, EarlyStopping이 이 중복성을 제어하는지 비교한다.
"""))
```

```text
=== C0-5. Redundancy and geometry anomaly checks ===
```

![output](assets/3085_problem3_cell022_out01_img06.png)

```text
Top redundancy pairs:
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature_1</th>
      <th>feature_2</th>
      <th>spearman_corr</th>
      <th>abs_corr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>carat</td>
      <td>volume</td>
      <td>0.998334</td>
      <td>0.998334</td>
    </tr>
    <tr>
      <th>1</th>
      <td>y</td>
      <td>volume</td>
      <td>0.998108</td>
      <td>0.998108</td>
    </tr>
    <tr>
      <th>2</th>
      <td>x</td>
      <td>volume</td>
      <td>0.998080</td>
      <td>0.998080</td>
    </tr>
    <tr>
      <th>3</th>
      <td>x</td>
      <td>y</td>
      <td>0.997960</td>
      <td>0.997960</td>
    </tr>
    <tr>
      <th>4</th>
      <td>depth</td>
      <td>z_to_xy_mean</td>
      <td>0.996767</td>
      <td>0.996767</td>
    </tr>
    <tr>
      <th>5</th>
      <td>carat</td>
      <td>x</td>
      <td>0.996587</td>
      <td>0.996587</td>
    </tr>
    <tr>
      <th>6</th>
      <td>carat</td>
      <td>y</td>
      <td>0.995922</td>
      <td>0.995922</td>
    </tr>
    <tr>
      <th>7</th>
      <td>carat</td>
      <td>z</td>
      <td>0.994647</td>
      <td>0.994647</td>
    </tr>
    <tr>
      <th>8</th>
      <td>z</td>
      <td>volume</td>
      <td>0.994260</td>
      <td>0.994260</td>
    </tr>
    <tr>
      <th>9</th>
      <td>x</td>
      <td>z</td>
      <td>0.988335</td>
      <td>0.988335</td>
    </tr>
    <tr>
      <th>10</th>
      <td>y</td>
      <td>z</td>
      <td>0.988139</td>
      <td>0.988139</td>
    </tr>
    <tr>
      <th>11</th>
      <td>price</td>
      <td>volume</td>
      <td>0.963920</td>
      <td>0.963920</td>
    </tr>
    <tr>
      <th>12</th>
      <td>price</td>
      <td>x</td>
      <td>0.963876</td>
      <td>0.963876</td>
    </tr>
    <tr>
      <th>13</th>
      <td>price</td>
      <td>y</td>
      <td>0.963360</td>
      <td>0.963360</td>
    </tr>
    <tr>
      <th>14</th>
      <td>carat</td>
      <td>price</td>
      <td>0.962920</td>
      <td>0.962920</td>
    </tr>
    <tr>
      <th>15</th>
      <td>price</td>
      <td>z</td>
      <td>0.958590</td>
      <td>0.958590</td>
    </tr>
    <tr>
      <th>16</th>
      <td>price</td>
      <td>price_per_carat</td>
      <td>0.956238</td>
      <td>0.956238</td>
    </tr>
    <tr>
      <th>17</th>
      <td>y</td>
      <td>price_per_carat</td>
      <td>0.855711</td>
      <td>0.855711</td>
    </tr>
    <tr>
      <th>18</th>
      <td>x</td>
      <td>price_per_carat</td>
      <td>0.855260</td>
      <td>0.855260</td>
    </tr>
    <tr>
      <th>19</th>
      <td>volume</td>
      <td>price_per_carat</td>
      <td>0.854655</td>
      <td>0.854655</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature</th>
      <th>min</th>
      <th>q01</th>
      <th>median</th>
      <th>q99</th>
      <th>max</th>
      <th>iqr_outlier_count</th>
      <th>iqr_outlier_ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>x</td>
      <td>3.730000</td>
      <td>4.010000</td>
      <td>5.700000</td>
      <td>8.340000</td>
      <td>10.740000</td>
      <td>12</td>
      <td>0.000371</td>
    </tr>
    <tr>
      <th>1</th>
      <td>y</td>
      <td>3.680000</td>
      <td>4.040000</td>
      <td>5.710000</td>
      <td>8.320000</td>
      <td>58.900000</td>
      <td>12</td>
      <td>0.000371</td>
    </tr>
    <tr>
      <th>2</th>
      <td>z</td>
      <td>1.070000</td>
      <td>2.480000</td>
      <td>3.530000</td>
      <td>5.150000</td>
      <td>8.060000</td>
      <td>14</td>
      <td>0.000433</td>
    </tr>
    <tr>
      <th>3</th>
      <td>volume</td>
      <td>31.707984</td>
      <td>40.081566</td>
      <td>114.907949</td>
      <td>353.766008</td>
      <td>3840.598060</td>
      <td>781</td>
      <td>0.024141</td>
    </tr>
    <tr>
      <th>4</th>
      <td>xy_ratio</td>
      <td>0.137351</td>
      <td>0.982729</td>
      <td>0.995726</td>
      <td>1.020185</td>
      <td>1.615572</td>
      <td>93</td>
      <td>0.002875</td>
    </tr>
    <tr>
      <th>5</th>
      <td>z_to_xy_mean</td>
      <td>0.161023</td>
      <td>0.578758</td>
      <td>0.618431</td>
      <td>0.655905</td>
      <td>1.006965</td>
      <td>1639</td>
      <td>0.050661</td>
    </tr>
  </tbody>
</table>
</div>


**모델링 해석.** size-price 축(`carat/x/y/z/volume/price`)은 매우 강하게 중복되어 있다. `depth`와 `z_to_xy_mean`도 거의 같은 proportion 신호로 볼 수 있다. B3 이후 mandatory feature를 추가하거나 제거하지 않고, Regularized 모델에서 L2, BatchNorm, Dropout, EarlyStopping이 이 중복성을 제어하는지 비교한다.

```python
print('=== C0-6. Validation sanity check without using test ===')

sanity_cols = ['table', 'depth', 'xy_ratio', 'z_to_xy_mean', 'carat', 'volume', 'price']

train_profile = train_eda.groupby('cut_label', observed=False)[sanity_cols].median().reindex(class_ids)
val_profile = val_eda.groupby('cut_label', observed=False)[sanity_cols].median().reindex(class_ids)
profile_scale = train_eda[sanity_cols].std().replace(0, 1)

profile_shift = ((val_profile - train_profile) / profile_scale).abs()
profile_shift.index = cut_order

display(profile_shift)

plt.figure(figsize=(11, 4.8))
sns.heatmap(profile_shift, cmap='YlOrRd', annot=True, fmt='.2f')
plt.title('Validation median shift from train profile (scaled by train std)')
plt.xlabel('Diagnostic feature')
plt.ylabel('Cut class')
plt.tight_layout()
plt.show()

max_shift = profile_shift.stack().idxmax()
max_shift_value = profile_shift.stack().max()

display(Markdown(f"""
**관찰:** 주요 EDA feature에서 validation profile은 train profile과 크게 벗어나지 않는다. 가장 큰 scaled median shift는 `{max_shift[0]}` / `{max_shift[1]}` = `{max_shift_value:.3f}`이다.

**결론:** C0에서 validation은 split sanity check 용도로만 사용한다. 모델 선택은 C4에서 validation prediction으로 수행하고, test는 Part D 전까지 사용하지 않는다.
"""))
```

```text
=== C0-6. Validation sanity check without using test ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>table</th>
      <th>depth</th>
      <th>xy_ratio</th>
      <th>z_to_xy_mean</th>
      <th>carat</th>
      <th>volume</th>
      <th>price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fair</th>
      <td>0.0</td>
      <td>0.070044</td>
      <td>0.074292</td>
      <td>0.069540</td>
      <td>0.000000</td>
      <td>0.016979</td>
      <td>0.072292</td>
    </tr>
    <tr>
      <th>Good</th>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.014587</td>
      <td>0.004040</td>
      <td>0.021194</td>
      <td>0.041035</td>
      <td>0.059571</td>
    </tr>
    <tr>
      <th>Very Good</th>
      <td>0.0</td>
      <td>0.070044</td>
      <td>0.003769</td>
      <td>0.057809</td>
      <td>0.000000</td>
      <td>0.009734</td>
      <td>0.006171</td>
    </tr>
    <tr>
      <th>Premium</th>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.000878</td>
      <td>0.025174</td>
      <td>0.254332</td>
      <td>0.177121</td>
      <td>0.096977</td>
    </tr>
    <tr>
      <th>Ideal</th>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.003921</td>
      <td>0.014589</td>
      <td>0.021194</td>
      <td>0.014403</td>
      <td>0.005919</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem3_cell023_out02_img07.png)


**관찰:** 주요 EDA feature에서 validation profile은 train profile과 크게 벗어나지 않는다. 가장 큰 scaled median shift는 `Premium` / `carat` = `0.254`이다.

**결론:** C0에서 validation은 split sanity check 용도로만 사용한다. 모델 선택은 C4에서 validation prediction으로 수행하고, test는 Part D 전까지 사용하지 않는다.

```python
print('=== C0-7. Deep visual board from train-only EDA signals ===')

from sklearn.decomposition import PCA


def stratified_eda_sample(frame, max_per_class=700):
    parts = []
    for class_id in class_ids:
        part = frame.loc[frame['cut_label'] == class_id]
        n = min(max_per_class, len(part))
        parts.append(part.sample(n=n, random_state=SEED))
    return pd.concat(parts, axis=0).sample(frac=1.0, random_state=SEED)


plot_train = stratified_eda_sample(train_eda, max_per_class=700)

deep_profile_cols = ['table', 'depth', 'xy_ratio', 'z_to_xy_mean', 'carat', 'volume', 'price']
class_medians = train_eda.groupby('cut_label', observed=False)[deep_profile_cols].median().reindex(class_ids)
class_medians.index = cut_order

class_z = (class_medians - train_eda[deep_profile_cols].median()) / train_eda[deep_profile_cols].std().replace(0, 1)

plt.figure(figsize=(11, 4.8))
sns.heatmap(class_z, cmap='coolwarm', center=0, annot=True, fmt='.2f')
plt.title('Train class median profile: standardized geometry and size-price signals')
plt.xlabel('Diagnostic feature')
plt.ylabel('Cut class')
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

sns.scatterplot(
    data=plot_train,
    x='table',
    y='depth',
    hue='cut',
    hue_order=cut_order,
    alpha=0.38,
    s=18,
    linewidth=0,
    ax=axes[0],
)
axes[0].set_title('Train geometry plane: table vs depth')
axes[0].grid(alpha=0.25)

sns.scatterplot(
    data=plot_train,
    x='xy_ratio',
    y='z_to_xy_mean',
    hue='cut',
    hue_order=cut_order,
    alpha=0.38,
    s=18,
    linewidth=0,
    ax=axes[1],
)
axes[1].set_title('Train proportion plane: xy_ratio vs z_to_xy_mean')
axes[1].grid(alpha=0.25)
axes[1].legend_.remove()

plt.tight_layout()
plt.show()

pca_cols = ['carat', 'x', 'y', 'z', 'volume', 'price', 'table', 'depth', 'xy_ratio', 'z_to_xy_mean']
pca_scaler = StandardScaler()
pca_values = pca_scaler.fit_transform(train_eda[pca_cols])
pca = PCA(n_components=2)
pca_scores = pca.fit_transform(pca_values)

pca_frame = train_eda[['cut', 'cut_label']].copy()
pca_frame['PC1'] = pca_scores[:, 0]
pca_frame['PC2'] = pca_scores[:, 1]
pca_plot = stratified_eda_sample(pca_frame, max_per_class=700)

pca_loadings = pd.DataFrame(
    pca.components_.T,
    index=pca_cols,
    columns=['PC1_loading', 'PC2_loading'],
)
pca_loadings['abs_PC1'] = pca_loadings['PC1_loading'].abs()
pca_loadings['abs_PC2'] = pca_loadings['PC2_loading'].abs()

print('PCA explained variance ratio:', np.round(pca.explained_variance_ratio_, 4).tolist())
display(pca_loadings.sort_values('abs_PC1', ascending=False).drop(columns=['abs_PC1', 'abs_PC2']))

plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=pca_plot,
    x='PC1',
    y='PC2',
    hue='cut',
    hue_order=cut_order,
    alpha=0.35,
    s=18,
    linewidth=0,
)
plt.title('Train PCA map: size-price axis vs geometry overlap')
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()

display(Markdown("""
**관찰:** `Fair`는 support가 작지만 geometry profile이 상대적으로 극단적이어서 분리 가능성이 있다. 반면 `Very Good`, `Premium`, `Ideal`은 상위 품질 영역에서 geometry가 많이 겹친다.

**원인:** MLP는 geometry 신호와 강한 size-price 축을 동시에 본다. geometry가 국소적으로 애매하면 class prior와 중복된 size-price 정보가 중간 class를 더 큰 인접/상위 class 쪽으로 끌어갈 수 있다.

**한계:** 이 그림들은 train-only 진단이다. 모델 설계와 D4 해석 근거로만 사용하며, test를 보고 모델을 선택하지 않는다.

**결론:** 핵심 시각화 리스크는 단순한 인접 class 혼동이 아니라 상위 품질 영역의 geometry overlap이다. 특히 중간 class가 더 큰 `Ideal` 영역으로 흡수될 수 있다.
"""))
```

```text
=== C0-7. Deep visual board from train-only EDA signals ===
```

![output](assets/3085_problem3_cell024_out01_img08.png)

![output](assets/3085_problem3_cell024_out02_img09.png)

```text
PCA explained variance ratio: [0.5743, 0.2091]
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PC1_loading</th>
      <th>PC2_loading</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>carat</th>
      <td>0.412924</td>
      <td>0.026837</td>
    </tr>
    <tr>
      <th>x</th>
      <td>0.411976</td>
      <td>-0.009238</td>
    </tr>
    <tr>
      <th>z</th>
      <td>0.410992</td>
      <td>0.072610</td>
    </tr>
    <tr>
      <th>volume</th>
      <td>0.408514</td>
      <td>-0.002156</td>
    </tr>
    <tr>
      <th>y</th>
      <td>0.405530</td>
      <td>-0.035117</td>
    </tr>
    <tr>
      <th>price</th>
      <td>0.387069</td>
      <td>0.006839</td>
    </tr>
    <tr>
      <th>table</th>
      <td>0.091375</td>
      <td>-0.319760</td>
    </tr>
    <tr>
      <th>xy_ratio</th>
      <td>0.036474</td>
      <td>0.091272</td>
    </tr>
    <tr>
      <th>depth</th>
      <td>0.003502</td>
      <td>0.663310</td>
    </tr>
    <tr>
      <th>z_to_xy_mean</th>
      <td>-0.001620</td>
      <td>0.664891</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem3_cell024_out05_img10.png)


**관찰:** `Fair`는 support가 작지만 geometry profile이 상대적으로 극단적이어서 분리 가능성이 있다. 반면 `Very Good`, `Premium`, `Ideal`은 상위 품질 영역에서 geometry가 많이 겹친다.

**원인:** MLP는 geometry 신호와 강한 size-price 축을 동시에 본다. geometry가 국소적으로 애매하면 class prior와 중복된 size-price 정보가 중간 class를 더 큰 인접/상위 class 쪽으로 끌어갈 수 있다.

**한계:** 이 그림들은 train-only 진단이다. 모델 설계와 D4 해석 근거로만 사용하며, test를 보고 모델을 선택하지 않는다.

**결론:** 핵심 시각화 리스크는 단순한 인접 class 혼동이 아니라 상위 품질 영역의 geometry overlap이다. 특히 중간 class가 더 큰 `Ideal` 영역으로 흡수될 수 있다.

```python
print('=== C0-8. Shared model/evaluation utilities ===')


def reset_seed():
    np.random.seed(SEED)
    keras.utils.set_random_seed(SEED)


def classification_metrics(y_true, y_pred):
    """Common metrics for imbalanced ordinal multiclass classification."""
    y_true = np.asarray(y_true).reshape(-1)
    y_pred = np.asarray(y_pred).reshape(-1)

    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'macro_f1': f1_score(y_true, y_pred, average='macro', zero_division=0),
        'weighted_f1': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'balanced_accuracy': balanced_accuracy_score(y_true, y_pred),
        'ordinal_mae': np.mean(np.abs(y_true - y_pred)),
    }


def predict_class(model, X_data):
    probability = model.predict(X_data, verbose=0)
    prediction = np.argmax(probability, axis=1)
    return probability, prediction


def display_history_end(model_name, history):
    last_idx = len(history.history['loss']) - 1

    row = {
        'model': model_name,
        'trained_epochs': len(history.history['loss']),
        'last_train_loss': history.history['loss'][last_idx],
        'last_val_loss': history.history['val_loss'][last_idx],
        'last_train_accuracy': history.history['accuracy'][last_idx],
        'last_val_accuracy': history.history['val_accuracy'][last_idx],
    }

    display(pd.DataFrame([row]))
    return row


print('input_dim :', X_train.shape[1])
print('num_classes:', len(cut_order))
print('X_train / X_val / X_test:', X_train.shape, X_val.shape, X_test.shape)
```

```text
=== C0-8. Shared model/evaluation utilities ===
input_dim : 9
num_classes: 5
X_train / X_val / X_test: (32352, 9) (10784, 9) (10784, 9)
```

---

## C1. Baseline 분류 모델 (6점)

**요구사항**:
- 다중분류 모델 (Dense 3개층 이상)
- 출력층: `Dense(5, activation='softmax')`
- Loss: `sparse_categorical_crossentropy` (타겟이 int이므로)
- Metric: `accuracy`
- epochs=30, batch_size=64

**필수 출력**:
- 모델 구조 (`.summary()`)
- 최종 Train Accuracy, Val Accuracy

```python
# C1. Baseline 분류 모델
print(' === C1. Baseline 분류 모델 ===')

input_dim = X_train.shape[1]
num_classes = len(cut_order)


def build_baseline_model(input_dim, num_classes=5):
    model = Sequential(name='baseline_classifier')
    model.add(keras.Input(shape=(input_dim,)))
    model.add(Dense(128, activation='relu', name='dense_128'))
    model.add(Dense(64, activation='relu', name='dense_64'))
    model.add(Dense(32, activation='relu', name='dense_32'))
    model.add(Dense(num_classes, activation='softmax', name='cut_probability'))
    return model


keras.backend.clear_session()
reset_seed()

baseline_model = build_baseline_model(input_dim, num_classes)

baseline_model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

baseline_model.summary()

history_baseline = baseline_model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=30,
    batch_size=64,
    verbose=0,
)

baseline_train_eval = baseline_model.evaluate(
    X_train,
    y_train,
    verbose=0,
    return_dict=True,
)

baseline_val_eval = baseline_model.evaluate(
    X_val,
    y_val,
    verbose=0,
    return_dict=True,
)

print('\n=== C1 최종 성능 ===')
print(f"Final Train Accuracy: {baseline_train_eval['accuracy']:.4f}")
print(f"Final Val Accuracy  : {baseline_val_eval['accuracy']:.4f}")

baseline_history_end = display_history_end('Baseline', history_baseline)
```

```text
 === C1. Baseline 분류 모델 ===
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Model: "baseline_classifier"</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Layer (type)                    </span>┃<span style="font-weight: bold"> Output Shape           </span>┃<span style="font-weight: bold">       Param # </span>┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ dense_128 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)               │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">128</span>)            │         <span style="color: #00af00; text-decoration-color: #00af00">1,280</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_64 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)                │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">64</span>)             │         <span style="color: #00af00; text-decoration-color: #00af00">8,256</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_32 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)                │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">32</span>)             │         <span style="color: #00af00; text-decoration-color: #00af00">2,080</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ cut_probability (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)         │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">5</span>)              │           <span style="color: #00af00; text-decoration-color: #00af00">165</span> │
└─────────────────────────────────┴────────────────────────┴───────────────┘
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold"> Total params: </span><span style="color: #00af00; text-decoration-color: #00af00">11,781</span> (46.02 KB)
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold"> Trainable params: </span><span style="color: #00af00; text-decoration-color: #00af00">11,781</span> (46.02 KB)
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold"> Non-trainable params: </span><span style="color: #00af00; text-decoration-color: #00af00">0</span> (0.00 B)
</pre>

```text

=== C1 최종 성능 ===
Final Train Accuracy: 0.8008
Final Val Accuracy  : 0.7884
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>trained_epochs</th>
      <th>last_train_loss</th>
      <th>last_val_loss</th>
      <th>last_train_accuracy</th>
      <th>last_val_accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>30</td>
      <td>0.512972</td>
      <td>0.54091</td>
      <td>0.794912</td>
      <td>0.78839</td>
    </tr>
  </tbody>
</table>
</div>

## C2. Regularized 분류 모델 (6점)

**요구사항**: 다음을 *모두* 적용
- L2 regularization (모든 Dense 층, λ=0.001)
- BatchNormalization (`Dense → BN → Activation` 순서)
- Dropout(0.3)
- EarlyStopping (patience=10, restore_best_weights=True)
- epochs=100 (EarlyStopping이 조기 종료하므로 충분히 크게 설정)

**필수 출력**:
- 최종 Train Accuracy, Val Accuracy
- 실제 학습된 epoch 수

```python
# C2. Regularized 분류 모델
print(' === C2. Regularized 분류 모델 ===')


def build_regularized_model(input_dim, num_classes=5):
    model = Sequential(name='regularized_classifier')
    model.add(keras.Input(shape=(input_dim,)))

    # Dense → BatchNormalization → Activation → Dropout
    model.add(Dense(
        128,
        use_bias=False,
        kernel_regularizer=l2(0.001),
        name='dense_128_l2',
    ))
    model.add(BatchNormalization(name='bn_128'))
    model.add(Activation('relu', name='relu_128'))
    model.add(Dropout(0.3, name='dropout_128'))

    model.add(Dense(
        64,
        use_bias=False,
        kernel_regularizer=l2(0.001),
        name='dense_64_l2',
    ))
    model.add(BatchNormalization(name='bn_64'))
    model.add(Activation('relu', name='relu_64'))
    model.add(Dropout(0.3, name='dropout_64'))

    model.add(Dense(
        32,
        use_bias=False,
        kernel_regularizer=l2(0.001),
        name='dense_32_l2',
    ))
    model.add(BatchNormalization(name='bn_32'))
    model.add(Activation('relu', name='relu_32'))
    model.add(Dropout(0.3, name='dropout_32'))

    # 모든 Dense 층 L2 요구에 따라 output Dense에도 L2 적용
    model.add(Dense(
        num_classes,
        activation='softmax',
        kernel_regularizer=l2(0.001),
        name='cut_probability_l2',
    ))

    return model


keras.backend.clear_session()
reset_seed()

regularized_model = build_regularized_model(input_dim, num_classes)

regularized_model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

regularized_model.summary()

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=0,
)

history_regularized = regularized_model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=100,
    batch_size=64,
    callbacks=[early_stopping],
    verbose=0,
)

regularized_train_eval = regularized_model.evaluate(
    X_train,
    y_train,
    verbose=0,
    return_dict=True,
)

regularized_val_eval = regularized_model.evaluate(
    X_val,
    y_val,
    verbose=0,
    return_dict=True,
)

regularized_best_epoch = int(np.argmin(history_regularized.history['val_loss']) + 1)

print('\n=== C2 최종 성능 — restore_best_weights 적용 후 ===')
print(f"Final Train Accuracy: {regularized_train_eval['accuracy']:.4f}")
print(f"Final Val Accuracy  : {regularized_val_eval['accuracy']:.4f}")
print(f"Actual trained epochs: {len(history_regularized.history['loss'])}")
print(f"Best val_loss epoch   : {regularized_best_epoch}")

regularized_history_end = display_history_end('Regularized', history_regularized)
```

```text
 === C2. Regularized 분류 모델 ===
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">Model: "regularized_classifier"</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃<span style="font-weight: bold"> Layer (type)                    </span>┃<span style="font-weight: bold"> Output Shape           </span>┃<span style="font-weight: bold">       Param # </span>┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ dense_128_l2 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)            │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">128</span>)            │         <span style="color: #00af00; text-decoration-color: #00af00">1,152</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ bn_128 (<span style="color: #0087ff; text-decoration-color: #0087ff">BatchNormalization</span>)     │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">128</span>)            │           <span style="color: #00af00; text-decoration-color: #00af00">512</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ relu_128 (<span style="color: #0087ff; text-decoration-color: #0087ff">Activation</span>)           │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">128</span>)            │             <span style="color: #00af00; text-decoration-color: #00af00">0</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_128 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dropout</span>)           │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">128</span>)            │             <span style="color: #00af00; text-decoration-color: #00af00">0</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_64_l2 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)             │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">64</span>)             │         <span style="color: #00af00; text-decoration-color: #00af00">8,192</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ bn_64 (<span style="color: #0087ff; text-decoration-color: #0087ff">BatchNormalization</span>)      │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">64</span>)             │           <span style="color: #00af00; text-decoration-color: #00af00">256</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ relu_64 (<span style="color: #0087ff; text-decoration-color: #0087ff">Activation</span>)            │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">64</span>)             │             <span style="color: #00af00; text-decoration-color: #00af00">0</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_64 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dropout</span>)            │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">64</span>)             │             <span style="color: #00af00; text-decoration-color: #00af00">0</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_32_l2 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)             │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">32</span>)             │         <span style="color: #00af00; text-decoration-color: #00af00">2,048</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ bn_32 (<span style="color: #0087ff; text-decoration-color: #0087ff">BatchNormalization</span>)      │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">32</span>)             │           <span style="color: #00af00; text-decoration-color: #00af00">128</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ relu_32 (<span style="color: #0087ff; text-decoration-color: #0087ff">Activation</span>)            │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">32</span>)             │             <span style="color: #00af00; text-decoration-color: #00af00">0</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_32 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dropout</span>)            │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">32</span>)             │             <span style="color: #00af00; text-decoration-color: #00af00">0</span> │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ cut_probability_l2 (<span style="color: #0087ff; text-decoration-color: #0087ff">Dense</span>)      │ (<span style="color: #00d7ff; text-decoration-color: #00d7ff">None</span>, <span style="color: #00af00; text-decoration-color: #00af00">5</span>)              │           <span style="color: #00af00; text-decoration-color: #00af00">165</span> │
└─────────────────────────────────┴────────────────────────┴───────────────┘
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold"> Total params: </span><span style="color: #00af00; text-decoration-color: #00af00">12,453</span> (48.64 KB)
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold"> Trainable params: </span><span style="color: #00af00; text-decoration-color: #00af00">12,005</span> (46.89 KB)
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold"> Non-trainable params: </span><span style="color: #00af00; text-decoration-color: #00af00">448</span> (1.75 KB)
</pre>

```text

=== C2 최종 성능 — restore_best_weights 적용 후 ===
Final Train Accuracy: 0.7714
Final Val Accuracy  : 0.7728
Actual trained epochs: 48
Best val_loss epoch   : 38
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>trained_epochs</th>
      <th>last_train_loss</th>
      <th>last_val_loss</th>
      <th>last_train_accuracy</th>
      <th>last_val_accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Regularized</td>
      <td>48</td>
      <td>0.742204</td>
      <td>0.646654</td>
      <td>0.715999</td>
      <td>0.767526</td>
    </tr>
  </tbody>
</table>
</div>

### C2 결과 해석 보완

Regularized 모델은 `Dropout(0.3)`, `L2(0.001)`, `BatchNormalization`, `EarlyStopping`을 모두 적용한 모델이다. 학습 history 마지막 줄의 train accuracy는 dropout이 켜진 training mode에서 측정되므로 낮게 보일 수 있다. 반면 `model.evaluate()`는 dropout이 꺼진 inference mode에서 수행되고, `restore_best_weights=True` 때문에 best validation loss 시점의 weight가 복원된 뒤 평가된다.

따라서 C2의 최종 해석은 history 마지막 줄만 보지 말고 `evaluate()` 결과를 기준으로 한다. 현재 실행에서는 Regularized가 validation accuracy와 macro-F1에서 Baseline보다 낮다. 이는 과적합 완화 효과보다 약한 underfitting 또는 과도한 regularization 효과가 더 크게 작동한 것으로 해석한다.

## C3. 학습 곡선 비교 (3점)

두 모델(Baseline, Regularized)의 **Validation Loss**와 **Validation Accuracy**를 각각 비교 시각화하시오.
(하나의 Figure에 서브플롯 2개 — 왼쪽: Validation Loss, 오른쪽: Validation Accuracy)

```python
print('=== C3. Baseline vs Regularized learning curves ===')

baseline_epochs = np.arange(1, len(history_baseline.history['loss']) + 1)
regularized_epochs = np.arange(1, len(history_regularized.history['loss']) + 1)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(
    baseline_epochs,
    history_baseline.history['val_loss'],
    label='Baseline Val Loss',
)
axes[0].plot(
    regularized_epochs,
    history_regularized.history['val_loss'],
    label='Regularized Val Loss',
)
axes[0].axvline(
    regularized_best_epoch,
    linestyle='--',
    linewidth=1,
    label=f'Regularized Best Epoch={regularized_best_epoch}',
)
axes[0].set_title('Validation Loss Comparison')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Validation Loss')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(
    baseline_epochs,
    history_baseline.history['val_accuracy'],
    label='Baseline Val Accuracy',
)
axes[1].plot(
    regularized_epochs,
    history_regularized.history['val_accuracy'],
    label='Regularized Val Accuracy',
)
axes[1].set_title('Validation Accuracy Comparison')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Validation Accuracy')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print('Note: Regularized val_loss includes the L2 penalty, so loss is not the only cross-model criterion.')

print('=== C4. Validation prediction metrics before test access ===')

baseline_val_probability, baseline_val_pred = predict_class(baseline_model, X_val)
regularized_val_probability, regularized_val_pred = predict_class(regularized_model, X_val)

baseline_val_metrics = classification_metrics(y_val, baseline_val_pred)
regularized_val_metrics = classification_metrics(y_val, regularized_val_pred)

val_comparison_df = pd.DataFrame([
    {'model': 'Baseline', **baseline_val_metrics},
    {'model': 'Regularized', **regularized_val_metrics},
])

val_comparison_df = val_comparison_df.sort_values(
    ['macro_f1', 'accuracy', 'ordinal_mae'],
    ascending=[False, False, True],
).reset_index(drop=True)

display(val_comparison_df)

selected_model_name = val_comparison_df.loc[0, 'model']

selected_model = (
    baseline_model
    if selected_model_name == 'Baseline'
    else regularized_model
)

selected_val_pred = (
    baseline_val_pred
    if selected_model_name == 'Baseline'
    else regularized_val_pred
)

print(f'Validation-selected model: {selected_model_name}')
```

```text
=== C3. Baseline vs Regularized learning curves ===
```

![output](assets/3085_problem3_cell032_out01_img11.png)

```text
Note: Regularized val_loss includes the L2 penalty, so loss is not the only cross-model criterion.
=== C4. Validation prediction metrics before test access ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>accuracy</th>
      <th>macro_f1</th>
      <th>weighted_f1</th>
      <th>balanced_accuracy</th>
      <th>ordinal_mae</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>0.788390</td>
      <td>0.772067</td>
      <td>0.785114</td>
      <td>0.762396</td>
      <td>0.290616</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Regularized</td>
      <td>0.772812</td>
      <td>0.743734</td>
      <td>0.767299</td>
      <td>0.721262</td>
      <td>0.305545</td>
    </tr>
  </tbody>
</table>
</div>

```text
Validation-selected model: Baseline
```

---
# Part D. 혼동 행렬 + 클래스별 성능 분석 (10점)

## D1. Test 예측 및 정확도 (3점)

**요구사항**:
- 두 모델 모두 X_test로 예측
- `predict()` 결과를 `argmax`로 클래스 변환
- 두 모델의 Test Accuracy 출력 및 비교

```python
print('=== D1. Test prediction and accuracy comparison - first test access ===')

baseline_test_probability, baseline_test_pred = predict_class(baseline_model, X_test)
regularized_test_probability, regularized_test_pred = predict_class(regularized_model, X_test)

assert np.allclose(baseline_test_probability.sum(axis=1), 1.0, atol=1e-5)
assert np.allclose(regularized_test_probability.sum(axis=1), 1.0, atol=1e-5)

baseline_test_metrics = classification_metrics(y_test, baseline_test_pred)
regularized_test_metrics = classification_metrics(y_test, regularized_test_pred)

test_comparison_df = pd.DataFrame([
    {'model': 'Baseline', **baseline_test_metrics},
    {'model': 'Regularized', **regularized_test_metrics},
])

display(test_comparison_df)

print(f"Baseline Test Accuracy   : {baseline_test_metrics['accuracy']:.4f}")
print(f"Regularized Test Accuracy: {regularized_test_metrics['accuracy']:.4f}")
print(f"C4 pre-selected model     : {selected_model_name}")
print('Test is used only for final generalization reporting, not for retroactive model selection.')
```

```text
=== D1. Test prediction and accuracy comparison - first test access ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>accuracy</th>
      <th>macro_f1</th>
      <th>weighted_f1</th>
      <th>balanced_accuracy</th>
      <th>ordinal_mae</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>0.783568</td>
      <td>0.769408</td>
      <td>0.779274</td>
      <td>0.756928</td>
      <td>0.296643</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Regularized</td>
      <td>0.763631</td>
      <td>0.733882</td>
      <td>0.756994</td>
      <td>0.710900</td>
      <td>0.318157</td>
    </tr>
  </tbody>
</table>
</div>

```text
Baseline Test Accuracy   : 0.7836
Regularized Test Accuracy: 0.7636
C4 pre-selected model     : Baseline
Test is used only for final generalization reporting, not for retroactive model selection.
```

## D2. 혼동 행렬 시각화 (2점)

**요구사항**:
- 두 모델의 혼동 행렬을 *seaborn heatmap*으로 시각화
- 행/열 라벨에 클래스 이름 표시 (Fair, Good, Very Good, Premium, Ideal)
- 제목에 각 모델의 Test Accuracy 표시

```python
# D2. 혼동 행렬 시각화
print('=== D2. Confusion matrices for both models ===')

cm_baseline = confusion_matrix(y_test, baseline_test_pred, labels=class_ids)
cm_regularized = confusion_matrix(y_test, regularized_test_pred, labels=class_ids)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.heatmap(
    cm_baseline,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=cut_order,
    yticklabels=cut_order,
    ax=axes[0],
)
axes[0].set_title(
    f"Baseline Confusion Matrix\nTest Accuracy={baseline_test_metrics['accuracy']:.4f}"
)
axes[0].set_xlabel('Predicted class')
axes[0].set_ylabel('True class')

sns.heatmap(
    cm_regularized,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=cut_order,
    yticklabels=cut_order,
    ax=axes[1],
)
axes[1].set_title(
    f"Regularized Confusion Matrix\nTest Accuracy={regularized_test_metrics['accuracy']:.4f}"
)
axes[1].set_xlabel('Predicted class')
axes[1].set_ylabel('True class')

plt.tight_layout()
plt.show()
```

```text
=== D2. Confusion matrices for both models ===
```

![output](assets/3085_problem3_cell036_out01_img12.png)

## D3. 클래스별 정밀도/재현율/F1 출력 (2점)

`sklearn.metrics.classification_report` 사용하여 클래스별 성능 출력 (두 모델 모두).

```python
print('=== D3. Per-class precision / recall / F1 ===')

print('\n[Baseline classification report]')
print(classification_report(
    y_test,
    baseline_test_pred,
    labels=class_ids,
    target_names=cut_order,
    digits=4,
    zero_division=0,
))

print('[Regularized classification report]')
print(classification_report(
    y_test,
    regularized_test_pred,
    labels=class_ids,
    target_names=cut_order,
    digits=4,
    zero_division=0,
))

baseline_report_dict = classification_report(
    y_test,
    baseline_test_pred,
    labels=class_ids,
    target_names=cut_order,
    output_dict=True,
    zero_division=0,
)

regularized_report_dict = classification_report(
    y_test,
    regularized_test_pred,
    labels=class_ids,
    target_names=cut_order,
    output_dict=True,
    zero_division=0,
)

baseline_report_df = pd.DataFrame(baseline_report_dict).T
regularized_report_df = pd.DataFrame(regularized_report_dict).T

print('Baseline report DataFrame:')
display(baseline_report_df)

print('Regularized report DataFrame:')
display(regularized_report_df)
```

```text
=== D3. Per-class precision / recall / F1 ===

[Baseline classification report]
              precision    recall  f1-score   support

        Fair     0.8628    0.8789    0.8708       322
        Good     0.7828    0.6031    0.6813       980
   Very Good     0.6485    0.6047    0.6258      2416
     Premium     0.8375    0.7743    0.8047      2756
       Ideal     0.8124    0.9237    0.8645      4310

    accuracy                         0.7836     10784
   macro avg     0.7888    0.7569    0.7694     10784
weighted avg     0.7809    0.7836    0.7793     10784

[Regularized classification report]
              precision    recall  f1-score   support

        Fair     0.8716    0.8012    0.8350       322
        Good     0.7729    0.4827    0.5942       980
   Very Good     0.6089    0.5786    0.5934      2416
     Premium     0.8071    0.7634    0.7846      2756
       Ideal     0.8047    0.9285    0.8622      4310

    accuracy                         0.7636     10784
   macro avg     0.7730    0.7109    0.7339     10784
weighted avg     0.7606    0.7636    0.7570     10784

Baseline report DataFrame:
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>precision</th>
      <th>recall</th>
      <th>f1-score</th>
      <th>support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fair</th>
      <td>0.862805</td>
      <td>0.878882</td>
      <td>0.870769</td>
      <td>322.000000</td>
    </tr>
    <tr>
      <th>Good</th>
      <td>0.782781</td>
      <td>0.603061</td>
      <td>0.681268</td>
      <td>980.000000</td>
    </tr>
    <tr>
      <th>Very Good</th>
      <td>0.648469</td>
      <td>0.604719</td>
      <td>0.625830</td>
      <td>2416.000000</td>
    </tr>
    <tr>
      <th>Premium</th>
      <td>0.837520</td>
      <td>0.774311</td>
      <td>0.804676</td>
      <td>2756.000000</td>
    </tr>
    <tr>
      <th>Ideal</th>
      <td>0.812449</td>
      <td>0.923666</td>
      <td>0.864495</td>
      <td>4310.000000</td>
    </tr>
    <tr>
      <th>accuracy</th>
      <td>0.783568</td>
      <td>0.783568</td>
      <td>0.783568</td>
      <td>0.783568</td>
    </tr>
    <tr>
      <th>macro avg</th>
      <td>0.788805</td>
      <td>0.756928</td>
      <td>0.769408</td>
      <td>10784.000000</td>
    </tr>
    <tr>
      <th>weighted avg</th>
      <td>0.780926</td>
      <td>0.783568</td>
      <td>0.779274</td>
      <td>10784.000000</td>
    </tr>
  </tbody>
</table>
</div>

```text
Regularized report DataFrame:
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>precision</th>
      <th>recall</th>
      <th>f1-score</th>
      <th>support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fair</th>
      <td>0.871622</td>
      <td>0.801242</td>
      <td>0.834951</td>
      <td>322.000000</td>
    </tr>
    <tr>
      <th>Good</th>
      <td>0.772876</td>
      <td>0.482653</td>
      <td>0.594221</td>
      <td>980.000000</td>
    </tr>
    <tr>
      <th>Very Good</th>
      <td>0.608885</td>
      <td>0.578642</td>
      <td>0.593379</td>
      <td>2416.000000</td>
    </tr>
    <tr>
      <th>Premium</th>
      <td>0.807058</td>
      <td>0.763425</td>
      <td>0.784635</td>
      <td>2756.000000</td>
    </tr>
    <tr>
      <th>Ideal</th>
      <td>0.804746</td>
      <td>0.928538</td>
      <td>0.862221</td>
      <td>4310.000000</td>
    </tr>
    <tr>
      <th>accuracy</th>
      <td>0.763631</td>
      <td>0.763631</td>
      <td>0.763631</td>
      <td>0.763631</td>
    </tr>
    <tr>
      <th>macro avg</th>
      <td>0.773037</td>
      <td>0.710900</td>
      <td>0.733882</td>
      <td>10784.000000</td>
    </tr>
    <tr>
      <th>weighted avg</th>
      <td>0.760557</td>
      <td>0.763631</td>
      <td>0.756994</td>
      <td>10784.000000</td>
    </tr>
  </tbody>
</table>
</div>

## D4. 클래스별 성능 분석 (3점)

선택 모델의 confusion matrix와 classification report를 보고 다음 질문에 답한다.

1. 어떤 class가 가장 잘 분류되었는가? 그 원인은 무엇인가?
2. 어떤 class가 가장 분류하기 어려운가? 그 원인은 무엇인가?
3. 어떤 class 쌍이 가장 자주 혼동되는가?

아래 분석은 C4에서 validation macro-F1 기준으로 모델을 선택한 뒤, Part D에서 실제 test metric을 사용해 생성한 제출용 분석이다.

```python
print('=== D4. Per-class analysis for the selected model ===')

if selected_model_name == 'Baseline':
    analysis_test_pred = baseline_test_pred
    analysis_report_df = baseline_report_df
    analysis_cm = cm_baseline
    other_model_name = 'Regularized'
else:
    analysis_test_pred = regularized_test_pred
    analysis_report_df = regularized_report_df
    analysis_cm = cm_regularized
    other_model_name = 'Baseline'

class_report = analysis_report_df.loc[
    cut_order,
    ['precision', 'recall', 'f1-score', 'support']
].copy()

best_class = class_report['f1-score'].idxmax()
worst_class = class_report['f1-score'].idxmin()

pair_matrix = analysis_cm + analysis_cm.T
np.fill_diagonal(pair_matrix, 0)

pair_i, pair_j = np.unravel_index(np.argmax(pair_matrix), pair_matrix.shape)

if pair_i > pair_j:
    pair_i, pair_j = pair_j, pair_i

pair_class_1 = cut_order[pair_i]
pair_class_2 = cut_order[pair_j]
pair_distance = abs(pair_i - pair_j)

pair_total = int(analysis_cm[pair_i, pair_j] + analysis_cm[pair_j, pair_i])
pair_1_to_2 = int(analysis_cm[pair_i, pair_j])
pair_2_to_1 = int(analysis_cm[pair_j, pair_i])

if pair_distance == 1:
    pair_relation_text = '인접 등급 간 혼동'
else:
    pair_relation_text = f'{pair_distance}단계 떨어진 비인접 등급 간 혼동'

profile_cols = ['table', 'depth']
class_profile = train_meta.groupby('cut_label', observed=False)[profile_cols].median().reindex(class_ids)
profile_scale = train_meta[profile_cols].std().replace(0, 1)

worst_idx = cut_order.index(worst_class)

profile_distance = np.sqrt(
    (((class_profile - class_profile.loc[worst_idx]) / profile_scale) ** 2).sum(axis=1)
)

profile_distance.loc[worst_idx] = np.inf

nearest_profile_idx = int(profile_distance.idxmin())
nearest_profile_class = cut_order[nearest_profile_idx]

train_ratio_map = split_distribution.set_index('class_name')['train_ratio'].to_dict()

selected_macro_f1 = classification_metrics(y_test, analysis_test_pred)['macro_f1']

other_macro_f1 = (
    regularized_test_metrics['macro_f1']
    if selected_model_name == 'Baseline'
    else baseline_test_metrics['macro_f1']
)

analysis_markdown = f"""
### D4 제출용 분석

1. **가장 잘 분류된 class는 `{best_class}`이다.** 선택 모델 `{selected_model_name}`에서 precision은 `{class_report.loc[best_class, 'precision']:.4f}`, recall은 `{class_report.loc[best_class, 'recall']:.4f}`, F1은 `{class_report.loc[best_class, 'f1-score']:.4f}`이다. Train 비율은 `{train_ratio_map[best_class]:.2%}`이다. 이 결과를 단순히 support가 충분해서라고 설명하면 부정확하다. C0의 train-only 시각화에서 확인한 것처럼 `table`과 `depth` geometry가 일부 class를 상대적으로 분리해 주기 때문에, support가 작아도 성능이 높게 나올 수 있다.

2. **가장 분류가 어려운 class는 `{worst_class}`이다.** precision은 `{class_report.loc[worst_class, 'precision']:.4f}`, recall은 `{class_report.loc[worst_class, 'recall']:.4f}`, F1은 `{class_report.loc[worst_class, 'f1-score']:.4f}`이다. Train 비율은 `{train_ratio_map[worst_class]:.2%}`이다. Train-only `table`/`depth` 중앙값 profile에서는 `{nearest_profile_class}`와 가장 가깝다. 따라서 단순한 표본 부족보다는 geometry overlap 때문에 softmax 경계가 불안정해진 것으로 해석한다.

3. **가장 자주 혼동된 class 쌍은 `{pair_class_1}`-`{pair_class_2}`이다.** 양방향 off-diagonal 합은 `{pair_total}`건이며, `{pair_class_1} -> {pair_class_2}`는 `{pair_1_to_2}`건, `{pair_class_2} -> {pair_class_1}`는 `{pair_2_to_1}`건이다. 이 쌍은 label 기준으로 `{pair_relation_text}`이다. 중간 품질 class가 더 큰 상위 품질 영역으로 흡수되는 경우, 모델이 국소적인 `table`/`depth` 차이보다 class prior와 겹치는 geometry 영역을 더 강하게 반영했을 가능성이 있다.

4. **최종 mandatory 모델은 `{selected_model_name}`이다.** 선택 모델의 Test macro-F1은 `{selected_macro_f1:.4f}`이고, 비교 모델 `{other_model_name}`의 Test macro-F1은 `{other_macro_f1:.4f}`이다. 이 선택은 test 접근 전에 C4의 validation macro-F1 기준으로 이미 완료했으며, Part D의 test 결과는 최종 일반화 성능 보고용으로만 사용한다.
"""

display(Markdown(analysis_markdown))
```

```text
=== D4. Per-class analysis for the selected model ===
```


### D4 제출용 분석

1. **가장 잘 분류된 class는 `Fair`이다.** 선택 모델 `Baseline`에서 precision은 `0.8628`, recall은 `0.8789`, F1은 `0.8708`이다. Train 비율은 `2.98%`이다. 이 결과를 단순히 support가 충분해서라고 설명하면 부정확하다. C0의 train-only 시각화에서 확인한 것처럼 `table`과 `depth` geometry가 일부 class를 상대적으로 분리해 주기 때문에, support가 작아도 성능이 높게 나올 수 있다.

2. **가장 분류가 어려운 class는 `Very Good`이다.** precision은 `0.6485`, recall은 `0.6047`, F1은 `0.6258`이다. Train 비율은 `22.41%`이다. Train-only `table`/`depth` 중앙값 profile에서는 `Premium`와 가장 가깝다. 따라서 단순한 표본 부족보다는 geometry overlap 때문에 softmax 경계가 불안정해진 것으로 해석한다.

3. **가장 자주 혼동된 class 쌍은 `Very Good`-`Ideal`이다.** 양방향 off-diagonal 합은 `752`건이며, `Very Good -> Ideal`는 `556`건, `Ideal -> Very Good`는 `196`건이다. 이 쌍은 label 기준으로 `2단계 떨어진 비인접 등급 간 혼동`이다. 중간 품질 class가 더 큰 상위 품질 영역으로 흡수되는 경우, 모델이 국소적인 `table`/`depth` 차이보다 class prior와 겹치는 geometry 영역을 더 강하게 반영했을 가능성이 있다.

4. **최종 mandatory 모델은 `Baseline`이다.** 선택 모델의 Test macro-F1은 `0.7694`이고, 비교 모델 `Regularized`의 Test macro-F1은 `0.7339`이다. 이 선택은 test 접근 전에 C4의 validation macro-F1 기준으로 이미 완료했으며, Part D의 test 결과는 최종 일반화 성능 보고용으로만 사용한다.

---
# Part E. 클래스 불균형 해결 (보너스)

> 이 Part는 **선택사항**입니다. 시도하지 않아도 100점 만점 가능.
> 시도해서 정확히 구현하면 최대 15점 추가 (총점 115점 가능).

## E1. class_weight 적용 모델

**요구사항**:
- `sklearn.utils.class_weight.compute_class_weight`로 균형 가중치 계산
- 위 가중치를 `model.fit(..., class_weight=...)`에 전달
- 동일 구조의 Regularized 모델로 학습

## E2. 결과 비교

**필수 출력**:
- class_weighted 모델의 Test Accuracy
- 분류 리포트 (D3와 비교)
- 마크다운으로 분석: macro F1이나 소수 클래스 recall이 어떻게 변했는가?

```python
# E1. class_weight 적용 모델 (보너스)
print('=== E1. Class-weighted Regularized model ===')

weight_values = compute_class_weight(
    class_weight='balanced',
    classes=class_ids,
    y=y_train,
)

class_weight_bonus = {
    int(class_id): float(weight)
    for class_id, weight in zip(class_ids, weight_values)
}

print('class_weight:', class_weight_bonus)

keras.backend.clear_session()
reset_seed()

class_weighted_model = build_regularized_model(input_dim, num_classes)

class_weighted_model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

weighted_early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=0,
)

history_class_weighted = class_weighted_model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=100,
    batch_size=64,
    class_weight=class_weight_bonus,
    callbacks=[weighted_early_stopping],
    verbose=0,
)

weighted_val_probability, weighted_val_pred = predict_class(class_weighted_model, X_val)
weighted_val_metrics = classification_metrics(y_val, weighted_val_pred)

print('Actual trained epochs:', len(history_class_weighted.history['loss']))

print('Validation metrics:')
display(pd.DataFrame([{'model': 'Class-weighted', **weighted_val_metrics}]))

print('The bonus model direction is checked on validation before test reporting.')
```

```text
=== E1. Class-weighted Regularized model ===
class_weight: {0: 6.705077720207254, 1: 2.199320190346703, 2: 0.8925920816664368, 3: 0.7825834542815675, 4: 0.5004950495049505}
```

```text
Actual trained epochs: 55
Validation metrics:
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>accuracy</th>
      <th>macro_f1</th>
      <th>weighted_f1</th>
      <th>balanced_accuracy</th>
      <th>ordinal_mae</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Class-weighted</td>
      <td>0.75714</td>
      <td>0.725022</td>
      <td>0.747167</td>
      <td>0.757162</td>
      <td>0.324091</td>
    </tr>
  </tbody>
</table>
</div>

```text
The bonus model direction is checked on validation before test reporting.
```

```python
# E2. Compare class_weighted results with Baseline and Regularized.
print('=== E2. Class-weighted test result comparison ===')

weighted_test_probability, weighted_test_pred = predict_class(class_weighted_model, X_test)
weighted_test_metrics = classification_metrics(y_test, weighted_test_pred)

print(f"Class-weighted Test Accuracy: {weighted_test_metrics['accuracy']:.4f}")

print('\n[Class-weighted classification report]')
print(classification_report(
    y_test,
    weighted_test_pred,
    labels=class_ids,
    target_names=cut_order,
    digits=4,
    zero_division=0,
))

weighted_report_dict = classification_report(
    y_test,
    weighted_test_pred,
    labels=class_ids,
    target_names=cut_order,
    output_dict=True,
    zero_division=0,
)

weighted_report_df = pd.DataFrame(weighted_report_dict).T

bonus_comparison_df = pd.DataFrame([
    {'model': 'Baseline', **baseline_test_metrics},
    {'model': 'Regularized', **regularized_test_metrics},
    {'model': 'Class-weighted', **weighted_test_metrics},
])

display(bonus_comparison_df)

metric_plot_df = bonus_comparison_df.set_index('model')[['accuracy', 'macro_f1', 'balanced_accuracy']]
metric_plot_df.plot(kind='bar', figsize=(9, 4), rot=0)
plt.title('Test metric comparison: Baseline vs Regularized vs Class-weighted')
plt.ylabel('Score')
plt.ylim(0, 1)
plt.grid(alpha=0.25, axis='y')
plt.tight_layout()
plt.show()

cm_weighted = confusion_matrix(y_test, weighted_test_pred, labels=class_ids)

plt.figure(figsize=(8, 6))
sns.heatmap(
    cm_weighted,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=cut_order,
    yticklabels=cut_order,
)
plt.title(
    f"Class-weighted confusion matrix\nTest accuracy={weighted_test_metrics['accuracy']:.4f}"
)
plt.xlabel('Predicted class')
plt.ylabel('True class')
plt.tight_layout()
plt.show()

minority_classes = ['Fair', 'Good']

minority_compare = pd.DataFrame({
    'baseline_recall': baseline_report_df.loc[minority_classes, 'recall'],
    'regularized_recall': regularized_report_df.loc[minority_classes, 'recall'],
    'class_weighted_recall': weighted_report_df.loc[minority_classes, 'recall'],
})

minority_compare['weighted_vs_regularized'] = (
    minority_compare['class_weighted_recall']
    - minority_compare['regularized_recall']
)

minority_compare['weighted_vs_baseline'] = (
    minority_compare['class_weighted_recall']
    - minority_compare['baseline_recall']
)

display(minority_compare)

per_class_compare = pd.DataFrame({
    'Baseline recall': baseline_report_df.loc[cut_order, 'recall'],
    'Regularized recall': regularized_report_df.loc[cut_order, 'recall'],
    'Class-weighted recall': weighted_report_df.loc[cut_order, 'recall'],
    'Baseline F1': baseline_report_df.loc[cut_order, 'f1-score'],
    'Regularized F1': regularized_report_df.loc[cut_order, 'f1-score'],
    'Class-weighted F1': weighted_report_df.loc[cut_order, 'f1-score'],
})

display(per_class_compare)

fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
per_class_compare[['Baseline recall', 'Regularized recall', 'Class-weighted recall']].plot(
    kind='bar',
    ax=axes[0],
    rot=20,
)
axes[0].set_title('Per-class recall trade-off')
axes[0].set_ylim(0, 1)
axes[0].grid(alpha=0.25, axis='y')

per_class_compare[['Baseline F1', 'Regularized F1', 'Class-weighted F1']].plot(
    kind='bar',
    ax=axes[1],
    rot=20,
)
axes[1].set_title('Per-class F1 trade-off')
axes[1].set_ylim(0, 1)
axes[1].grid(alpha=0.25, axis='y')

plt.tight_layout()
plt.show()

macro_change_vs_regularized = (
    weighted_test_metrics['macro_f1']
    - regularized_test_metrics['macro_f1']
)

accuracy_change_vs_regularized = (
    weighted_test_metrics['accuracy']
    - regularized_test_metrics['accuracy']
)

macro_change_vs_baseline = (
    weighted_test_metrics['macro_f1']
    - baseline_test_metrics['macro_f1']
)

accuracy_change_vs_baseline = (
    weighted_test_metrics['accuracy']
    - baseline_test_metrics['accuracy']
)

bonus_markdown = f"""
### Part E 결과 분석

Regularized와 비교하면 class_weight 적용 모델의 Test macro-F1 변화는 `{macro_change_vs_regularized:+.4f}`, accuracy 변화는 `{accuracy_change_vs_regularized:+.4f}`이다. Fair recall 변화는 `{minority_compare.loc['Fair', 'weighted_vs_regularized']:+.4f}`, Good recall 변화는 `{minority_compare.loc['Good', 'weighted_vs_regularized']:+.4f}`이다.

Baseline과 비교하면 class_weight 적용 모델의 Test macro-F1 변화는 `{macro_change_vs_baseline:+.4f}`, accuracy 변화는 `{accuracy_change_vs_baseline:+.4f}`이다.

이 결과는 최종 모델 개선이 아니라 trade-off로 해석해야 한다. `class_weight`는 decision boundary를 소수 class 쪽으로 이동시켜 Regularized 대비 Fair/Good recall을 개선했지만, 현재 실행에서는 전체 accuracy와 macro-F1을 낮췄다. 따라서 Part E는 소수 class recall 개선을 보여주는 보조 실험으로 보고, 최종 mandatory 모델은 validation 기준으로 선택된 Baseline으로 유지한다.
"""

display(Markdown(bonus_markdown))
```

```text
=== E2. Class-weighted test result comparison ===
```

```text
Class-weighted Test Accuracy: 0.7507

[Class-weighted classification report]
              precision    recall  f1-score   support

        Fair     0.7345    0.8851    0.8028       322
        Good     0.5536    0.7531    0.6381       980
   Very Good     0.6530    0.4098    0.5036      2416
     Premium     0.7922    0.7747    0.7833      2756
       Ideal     0.8137    0.9160    0.8618      4310

    accuracy                         0.7507     10784
   macro avg     0.7094    0.7477    0.7179     10784
weighted avg     0.7462    0.7507    0.7394     10784
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>accuracy</th>
      <th>macro_f1</th>
      <th>weighted_f1</th>
      <th>balanced_accuracy</th>
      <th>ordinal_mae</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>0.783568</td>
      <td>0.769408</td>
      <td>0.779274</td>
      <td>0.756928</td>
      <td>0.296643</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Regularized</td>
      <td>0.763631</td>
      <td>0.733882</td>
      <td>0.756994</td>
      <td>0.710900</td>
      <td>0.318157</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Class-weighted</td>
      <td>0.750742</td>
      <td>0.717935</td>
      <td>0.739412</td>
      <td>0.747721</td>
      <td>0.331973</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem3_cell043_out03_img13.png)

![output](assets/3085_problem3_cell043_out04_img14.png)

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>baseline_recall</th>
      <th>regularized_recall</th>
      <th>class_weighted_recall</th>
      <th>weighted_vs_regularized</th>
      <th>weighted_vs_baseline</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fair</th>
      <td>0.878882</td>
      <td>0.801242</td>
      <td>0.885093</td>
      <td>0.083851</td>
      <td>0.006211</td>
    </tr>
    <tr>
      <th>Good</th>
      <td>0.603061</td>
      <td>0.482653</td>
      <td>0.753061</td>
      <td>0.270408</td>
      <td>0.150000</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Baseline recall</th>
      <th>Regularized recall</th>
      <th>Class-weighted recall</th>
      <th>Baseline F1</th>
      <th>Regularized F1</th>
      <th>Class-weighted F1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Fair</th>
      <td>0.878882</td>
      <td>0.801242</td>
      <td>0.885093</td>
      <td>0.870769</td>
      <td>0.834951</td>
      <td>0.802817</td>
    </tr>
    <tr>
      <th>Good</th>
      <td>0.603061</td>
      <td>0.482653</td>
      <td>0.753061</td>
      <td>0.681268</td>
      <td>0.594221</td>
      <td>0.638132</td>
    </tr>
    <tr>
      <th>Very Good</th>
      <td>0.604719</td>
      <td>0.578642</td>
      <td>0.409768</td>
      <td>0.625830</td>
      <td>0.593379</td>
      <td>0.503561</td>
    </tr>
    <tr>
      <th>Premium</th>
      <td>0.774311</td>
      <td>0.763425</td>
      <td>0.774673</td>
      <td>0.804676</td>
      <td>0.784635</td>
      <td>0.783343</td>
    </tr>
    <tr>
      <th>Ideal</th>
      <td>0.923666</td>
      <td>0.928538</td>
      <td>0.916009</td>
      <td>0.864495</td>
      <td>0.862221</td>
      <td>0.861821</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem3_cell043_out07_img15.png)


### Part E 결과 분석

Regularized와 비교하면 class_weight 적용 모델의 Test macro-F1 변화는 `-0.0159`, accuracy 변화는 `-0.0129`이다. Fair recall 변화는 `+0.0839`, Good recall 변화는 `+0.2704`이다.

Baseline과 비교하면 class_weight 적용 모델의 Test macro-F1 변화는 `-0.0515`, accuracy 변화는 `-0.0328`이다.

이 결과는 최종 모델 개선이 아니라 trade-off로 해석해야 한다. `class_weight`는 decision boundary를 소수 class 쪽으로 이동시켜 Regularized 대비 Fair/Good recall을 개선했지만, 현재 실행에서는 전체 accuracy와 macro-F1을 낮췄다. 따라서 Part E는 소수 class recall 개선을 보여주는 보조 실험으로 보고, 최종 mandatory 모델은 validation 기준으로 선택된 Baseline으로 유지한다.

# 최종 제출 결론

이 문제는 diamond `cut`을 예측하는 5-class ordinal multiclass classification 문제다. C0는 제공 split을 보존한 상태에서 수행했다. EDA는 train 기준으로 진행했고, validation은 sanity check와 모델 선택에만 사용했으며, test는 Part D에서 처음 열었다.

Train-only EDA에서는 `table`, `depth`, `xy_ratio`, `z_to_xy_mean`이 cut과 관련된 geometry/proportion 신호로 확인되었다. 또한 `carat`, `x`, `y`, `z`, `volume`, `price`는 강한 size-price 중복 축을 형성했다. `Fair`와 `Good`은 소수 class이므로 모델 선택에는 validation macro-F1을 우선 사용하고, accuracy, balanced accuracy, ordinal MAE를 보조 지표로 함께 확인했다.

최종 mandatory 모델은 **Baseline**이다. Baseline은 test 접근 전 validation accuracy, validation macro-F1, ordinal MAE 기준에서 Regularized보다 좋았다. Part D의 test 평가에서도 Baseline이 accuracy, macro-F1, ordinal MAE 기준으로 더 안정적이었다. Regularized 모델은 L2, BatchNorm, Dropout, EarlyStopping 요구사항을 모두 충족하지만, 현재 데이터에서는 과적합 완화보다 약한 underfitting 또는 과도한 regularization 효과가 더 크게 작동했다.

Confusion analysis에서는 `Fair`가 소수 class임에도 geometry가 상대적으로 분리되어 좋은 성능을 보였다. 반면 `Very Good`, `Premium`, `Ideal`이 겹치는 상위 품질 영역은 분류가 어렵다. 가장 큰 혼동이 `Very Good`-`Ideal`처럼 비인접 쌍으로 나타날 수 있으므로, 이를 단순한 인접 등급 혼동이라고 설명하면 안 된다.

Bonus class_weight 모델은 Regularized 대비 `Fair`와 `Good` recall을 개선했지만, overall accuracy와 macro-F1은 낮아졌다. 따라서 class_weight는 소수 class recall 개선의 trade-off를 보여주는 보조 실험으로 해석하고, 최종 모델로는 Baseline을 유지한다.

---

# 제출 전 체크리스트

- [ ] `STUDENT_ID`가 본인 학번에 맞게 설정되어 있는가?
- [ ] Restart Kernel -> Run All 실행 시 traceback 없이 끝나는가?
- [ ] A/B 제공 코드를 수정하지 않았는가?
- [ ] C0가 train-only EDA와 validation-only sanity check 원칙을 지키는가?
- [ ] C4에서 test 접근 전에 모델 선택이 끝나는가?
- [ ] D4에서 `Very Good`-`Ideal`을 인접 등급이라고 잘못 설명하지 않는가?
- [ ] E2 비교표에 Baseline, Regularized, Class-weighted가 모두 포함되어 있는가?

---

# 3085_problem4.ipynb

# 기말고사 문제 4 — Bike Sharing 회귀 + 분류 종합 분석

> **기계학습 라이브러리 활용** · 기말 Take-home Exam
> 배점: **25점** (Part B 10 + Part C 10 + Part D 5)  ·  Part A·B1(EDA/전처리)는 제공 코드

이 문제는 **회귀와 분류를 같은 데이터에서 모두 수행**하는 종합 응용 문제입니다.

---

## 📌 시험 안내

### 데이터
- **출처**: UCI ML Repository — Bike Sharing Dataset (hour-level)
- **URL**: `https://raw.githubusercontent.com/PacktWorkshops/The-Data-Analysis-Workshop/master/Chapter01/data/hour.csv`
- **샘플**: 17,379개 (시간별 2년치)
- **타겟**: `cnt` (시간당 자전거 대여 수, 1~977)

### 두 가지 문제
1. **회귀**: `cnt` 값을 직접 예측 (MAE 평가)
2. **분류**: `cnt`를 3구간(low/mid/high)으로 binning 후 분류 (Accuracy 평가)

### 주의사항
- `casual`과 `registered` 컬럼은 **feature로 사용 금지** (`cnt = casual + registered`이므로 data leakage)
- 학번 마지막 4자리를 seed로 사용

---

## ⚠️ 학번 입력 (필수)

```python
STUDENT_ID = "3085"   # ← 본인 학번 마지막 4자리로 변경
SEED = int(STUDENT_ID)

assert STUDENT_ID != "0000", "학번을 입력하세요!"
print(f'학번(끝4자리): {STUDENT_ID}, SEED: {SEED}')
```

```text
학번(끝4자리): 3085, SEED: 3085
```

## 환경 준비

필요한 라이브러리를 import하고 seed를 고정하세요.
(회귀/분류 모두에 필요한 모듈 포함)

```python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import keras
from keras import Sequential
from keras.layers import Dense, Dropout, BatchNormalization, Activation
from keras.regularizers import l2
from keras.callbacks import EarlyStopping

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report

# 재현성: 학번 기반 SEED로 고정 (numpy + 현재 keras 백엔드 동시 고정)
np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

print('Keras  :', keras.__version__, '| backend:', keras.backend.backend())
print('pandas :', pd.__version__)
```

```text
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1781882366.794341  572260 port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
I0000 00:00:1781882366.795595  572260 cudart_stub.cc:31] Could not find cuda drivers on your machine, GPU will not be used.
```

```text
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1781882369.084107  572260 port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
I0000 00:00:1781882369.084557  572260 cudart_stub.cc:31] Could not find cuda drivers on your machine, GPU will not be used.
```

```text
Keras  : 3.14.1 | backend: tensorflow
pandas : 3.0.2
```

---
# Part A. 데이터 EDA + Feature Engineering (제공 코드)

## A1. 데이터 로드 및 기본 정보

- 데이터 로드 및 shape 출력
- 결측치 확인
- 컬럼 목록 출력
- `cnt` 컬럼의 기본 통계 출력

```python
url = 'https://raw.githubusercontent.com/PacktWorkshops/The-Data-Analysis-Workshop/master/Chapter01/data/hour.csv'
df = pd.read_csv(url)

print(f'Shape: {df.shape}')
print(f'결측치: {df.isnull().sum().sum()}')
print(f'\n컬럼: {df.columns.tolist()}')
print(f'\ncnt 분포:')
print(df['cnt'].describe())
```

```text
Shape: (17379, 17)
결측치: 0

컬럼: ['instant', 'dteday', 'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']

cnt 분포:
count    17379.000000
mean       189.463088
std        181.387599
min          1.000000
25%         40.000000
50%        142.000000
75%        281.000000
max        977.000000
Name: cnt, dtype: float64
```

## A2. 타겟 분포 시각화

- `cnt`의 원본 히스토그램과 log 변환 후 히스토그램을 나란히 비교
- 각 분포의 skewness 출력
- 어느 쪽이 회귀에 적합한지 판단 (마크다운으로 1줄)

```python
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# 히스토그램
axes[0].hist(df['cnt'], bins=50, color='steelblue', alpha=0.7)
axes[0].set_xlabel('cnt'); axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of cnt (Bike Rental Count)')
axes[0].grid(alpha=0.3)

# log 변환 후
axes[1].hist(np.log1p(df['cnt']), bins=50, color='teal', alpha=0.7)
axes[1].set_xlabel('log1p(cnt)'); axes[1].set_ylabel('Frequency')
axes[1].set_title('Distribution after log1p')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print(f'원본 skewness: {df["cnt"].skew():.2f}')
print(f'log 변환 후  : {np.log1p(df["cnt"]).skew():.2f}')

print(' === A1. Bike Sharing 데이터 컬럼 역할 정의 ===')

column_role_table = pd.DataFrame([
    ['instant', 'id', 'record index', '행 번호. 관측 순서 ID', 'feature에서 제외'],
    ['dteday', 'date', 'date', '날짜. 시간 정보 원천', '직접 feature 제외. 필요하면 파생변수만 사용'],
    ['season', 'categorical_feature', '1:winter, 2:spring, 3:summer, 4:fall', '계절. 수요의 장기 패턴', '사용 가능'],
    ['yr', 'categorical/time_feature', '0:2011, 1:2012', '연도. 서비스 성장 또는 연도 효과', '사용 가능'],
    ['mnth', 'categorical/time_feature', '1~12', '월. 계절성과 월별 수요 패턴', '사용 가능'],
    ['hr', 'categorical/time_feature', '0~23', '시간대. 출퇴근/야간/낮 패턴 핵심', '사용 가능'],
    ['holiday', 'binary_feature', '0/1', '공휴일 여부', '사용 가능'],
    ['weekday', 'categorical_feature', 'day of week', '요일. 주말/평일 패턴', '사용 가능'],
    ['workingday', 'binary_feature', '0/1', '주말/공휴일이 아니면 1', '사용 가능'],
    ['weathersit', 'categorical_feature', '1~4', '날씨 상태. 맑음/흐림/비/눈 등', '사용 가능'],
    ['temp', 'numeric_feature', 'normalized temperature', '정규화된 기온', '사용 가능'],
    ['atemp', 'numeric_feature', 'normalized feeling temperature', '정규화된 체감온도', '사용 가능'],
    ['hum', 'numeric_feature', 'normalized humidity', '정규화된 습도', '사용 가능'],
    ['windspeed', 'numeric_feature', 'normalized wind speed', '정규화된 풍속', '사용 가능'],
    ['casual', 'leakage', 'casual user count', '비회원/일회성 사용자 대여량', 'cnt 구성요소이므로 제외'],
    ['registered', 'leakage', 'registered user count', '등록 사용자 대여량', 'cnt 구성요소이므로 제외'],
    ['cnt', 'target', 'casual + registered', '총 대여량. 회귀 target 또는 분류 binning 기준', 'y']
], columns=['column', 'role', 'raw meaning', 'domain meaning', 'modeling decision'])

display(column_role_table)

print(' === A1-1. 기본 데이터 점검 ===')
print(f'Shape: {df.shape}')
print(f'결측치 총 개수: {df.isnull().sum().sum()}')
print(f'중복 instant 개수: {df["instant"].duplicated().sum()}')

df_audit = df.copy()
df_audit['dteday'] = pd.to_datetime(df_audit['dteday'])

print(f'날짜 범위: {df_audit["dteday"].min()} ~ {df_audit["dteday"].max()}')
print(f'시간 hr 범위: {df["hr"].min()} ~ {df["hr"].max()}')
print(f'cnt 범위: {df["cnt"].min()} ~ {df["cnt"].max()}')

print('\n === A1-2. Leakage 확인: casual + registered == cnt ===')
leakage_match_rate = ((df['casual'] + df['registered']) == df['cnt']).mean()
print(f'(casual + registered == cnt) 비율: {leakage_match_rate:.4f}')

print('\n해석:')
print('casual과 registered는 cnt의 직접 구성요소이므로 feature에 포함하면 data leakage가 발생한다.')
print('따라서 회귀/분류 모두 X에서는 casual, registered, cnt, instant, dteday를 제외한다.')

print(' === A2. Target(cnt) 분포 심화 확인 ===')
print('RQ0. cnt는 정규분포에 가까운가, 아니면 특정 시간대에 수요가 몰리는 long-tail count target인가?')

target = 'cnt'

cnt_desc = df[target].describe(
    percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
)

display(cnt_desc)

cnt_skew = df[target].skew()
cnt_kurt = df[target].kurtosis()
log_cnt = np.log1p(df[target])
log_cnt_skew = log_cnt.skew()
log_cnt_kurt = log_cnt.kurtosis()

print(f'원본 skewness: {cnt_skew:.4f}')
print(f'원본 kurtosis: {cnt_kurt:.4f}')
print(f'log1p skewness: {log_cnt_skew:.4f}')
print(f'log1p kurtosis: {log_cnt_kurt:.4f}')

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

axes[0].hist(df['cnt'], bins=50, alpha=0.7)
axes[0].set_xlabel('cnt')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of cnt')
axes[0].grid(alpha=0.3)

axes[1].hist(np.log1p(df['cnt']), bins=50, alpha=0.7)
axes[1].set_xlabel('log1p(cnt)')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Distribution after log1p')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 4))
plt.boxplot(df['cnt'], vert=False)
plt.title('Boxplot of cnt')
plt.xlabel('cnt')
plt.show()

print('해석:')
print('cnt는 평균이 중앙값보다 크고, max가 977로 높아 오른쪽 꼬리가 존재한다.')
print('이는 특정 시간대, 계절, 날씨 조건에서 대여량이 급증하는 demand peak가 있다는 뜻이다.')
print('원본 cnt를 그대로 MSE로 학습하면 고수요 시간대의 큰 오차가 loss를 강하게 지배할 수 있다.')
print('log1p(cnt)는 큰 값을 압축해 회귀 학습을 안정화할 수 있다.')
print('따라서 Part B 회귀에서는 y에 log1p 변환을 적용하고, 최종 평가는 expm1으로 원본 스케일 복원 후 MAE를 계산하는 것이 적절하다.')
```

![output](assets/3085_problem4_cell007_out00_img01.png)

```text
원본 skewness: 1.28
log 변환 후  : -0.82
 === A1. Bike Sharing 데이터 컬럼 역할 정의 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>column</th>
      <th>role</th>
      <th>raw meaning</th>
      <th>domain meaning</th>
      <th>modeling decision</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>instant</td>
      <td>id</td>
      <td>record index</td>
      <td>행 번호. 관측 순서 ID</td>
      <td>feature에서 제외</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dteday</td>
      <td>date</td>
      <td>date</td>
      <td>날짜. 시간 정보 원천</td>
      <td>직접 feature 제외. 필요하면 파생변수만 사용</td>
    </tr>
    <tr>
      <th>2</th>
      <td>season</td>
      <td>categorical_feature</td>
      <td>1:winter, 2:spring, 3:summer, 4:fall</td>
      <td>계절. 수요의 장기 패턴</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>3</th>
      <td>yr</td>
      <td>categorical/time_feature</td>
      <td>0:2011, 1:2012</td>
      <td>연도. 서비스 성장 또는 연도 효과</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>4</th>
      <td>mnth</td>
      <td>categorical/time_feature</td>
      <td>1~12</td>
      <td>월. 계절성과 월별 수요 패턴</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>5</th>
      <td>hr</td>
      <td>categorical/time_feature</td>
      <td>0~23</td>
      <td>시간대. 출퇴근/야간/낮 패턴 핵심</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>6</th>
      <td>holiday</td>
      <td>binary_feature</td>
      <td>0/1</td>
      <td>공휴일 여부</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>7</th>
      <td>weekday</td>
      <td>categorical_feature</td>
      <td>day of week</td>
      <td>요일. 주말/평일 패턴</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>8</th>
      <td>workingday</td>
      <td>binary_feature</td>
      <td>0/1</td>
      <td>주말/공휴일이 아니면 1</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>9</th>
      <td>weathersit</td>
      <td>categorical_feature</td>
      <td>1~4</td>
      <td>날씨 상태. 맑음/흐림/비/눈 등</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>10</th>
      <td>temp</td>
      <td>numeric_feature</td>
      <td>normalized temperature</td>
      <td>정규화된 기온</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>11</th>
      <td>atemp</td>
      <td>numeric_feature</td>
      <td>normalized feeling temperature</td>
      <td>정규화된 체감온도</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>12</th>
      <td>hum</td>
      <td>numeric_feature</td>
      <td>normalized humidity</td>
      <td>정규화된 습도</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>13</th>
      <td>windspeed</td>
      <td>numeric_feature</td>
      <td>normalized wind speed</td>
      <td>정규화된 풍속</td>
      <td>사용 가능</td>
    </tr>
    <tr>
      <th>14</th>
      <td>casual</td>
      <td>leakage</td>
      <td>casual user count</td>
      <td>비회원/일회성 사용자 대여량</td>
      <td>cnt 구성요소이므로 제외</td>
    </tr>
    <tr>
      <th>15</th>
      <td>registered</td>
      <td>leakage</td>
      <td>registered user count</td>
      <td>등록 사용자 대여량</td>
      <td>cnt 구성요소이므로 제외</td>
    </tr>
    <tr>
      <th>16</th>
      <td>cnt</td>
      <td>target</td>
      <td>casual + registered</td>
      <td>총 대여량. 회귀 target 또는 분류 binning 기준</td>
      <td>y</td>
    </tr>
  </tbody>
</table>
</div>

```text
 === A1-1. 기본 데이터 점검 ===
Shape: (17379, 17)
결측치 총 개수: 0
중복 instant 개수: 0
날짜 범위: 2011-01-01 00:00:00 ~ 2012-12-31 00:00:00
시간 hr 범위: 0 ~ 23
cnt 범위: 1 ~ 977

 === A1-2. Leakage 확인: casual + registered == cnt ===
(casual + registered == cnt) 비율: 1.0000

해석:
casual과 registered는 cnt의 직접 구성요소이므로 feature에 포함하면 data leakage가 발생한다.
따라서 회귀/분류 모두 X에서는 casual, registered, cnt, instant, dteday를 제외한다.
 === A2. Target(cnt) 분포 심화 확인 ===
RQ0. cnt는 정규분포에 가까운가, 아니면 특정 시간대에 수요가 몰리는 long-tail count target인가?
```

```text
count    17379.000000
mean       189.463088
std        181.387599
min          1.000000
1%           2.000000
5%           5.000000
25%         40.000000
50%        142.000000
75%        281.000000
90%        451.200000
95%        563.100000
99%        782.220000
max        977.000000
Name: cnt, dtype: float64
```

```text
원본 skewness: 1.2774
원본 kurtosis: 1.4172
log1p skewness: -0.8182
log1p kurtosis: -0.1795
```

![output](assets/3085_problem4_cell007_out06_img02.png)

![output](assets/3085_problem4_cell007_out07_img03.png)

```text
해석:
cnt는 평균이 중앙값보다 크고, max가 977로 높아 오른쪽 꼬리가 존재한다.
이는 특정 시간대, 계절, 날씨 조건에서 대여량이 급증하는 demand peak가 있다는 뜻이다.
원본 cnt를 그대로 MSE로 학습하면 고수요 시간대의 큰 오차가 loss를 강하게 지배할 수 있다.
log1p(cnt)는 큰 값을 압축해 회귀 학습을 안정화할 수 있다.
따라서 Part B 회귀에서는 y에 log1p 변환을 적용하고, 최종 평가는 expm1으로 원본 스케일 복원 후 MAE를 계산하는 것이 적절하다.
```

## A3. Feature Engineering

- 기존 데이터에서 *유용한 feature 1개 이상 추가* (예: 시간대 그룹, 주말 등)
- 추가한 feature가 범주형이면 One-Hot 인코딩
- ⚠️ **반드시 `casual`과 `registered`를 feature에서 제외** (data leakage 방지)
- ⚠️ `instant`, `dteday`, `cnt`도 feature에서 제외

**출력**:
- 최종 feature 컬럼 목록
- X.shape

```python
df_clean = df.copy()

# 시간대 그룹 (rush hour 등의 패턴 반영)
def time_of_day(h):
    if 6 <= h <= 9:  return 'morning_rush'
    elif 10 <= h <= 16: return 'daytime'
    elif 17 <= h <= 20: return 'evening_rush'
    else: return 'night'
df_clean['time_group'] = df_clean['hr'].apply(time_of_day)

# 주말 여부 (workingday를 그대로 써도 됨)
df_clean['is_weekend'] = (df_clean['weekday'].isin([0, 6])).astype(int)

# Feature 선택 (casual, registered는 cnt의 직접 분해이므로 제외)
# date, instant도 제외
feature_cols = [
    'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit',
    'temp', 'atemp', 'hum', 'windspeed',
    'is_weekend'
]

# time_group은 범주형 → One-Hot
df_encoded = pd.get_dummies(df_clean[feature_cols + ['time_group']],
                            columns=['time_group'], dtype=int)

X = df_encoded.values.astype(np.float32)
y_reg = df_clean['cnt'].values.astype(np.float32)

print(f'X shape: {X.shape}')
print(f'Feature 컬럼 수: {X.shape[1]}')
print(f'Feature 목록: {df_encoded.columns.tolist()}')
```

```text
X shape: (17379, 17)
Feature 컬럼 수: 17
Feature 목록: ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'is_weekend', 'time_group_daytime', 'time_group_evening_rush', 'time_group_morning_rush', 'time_group_night']
```

```python
print(' === A3-1. Feature Engineering 결과 검증 ===')

print(f'df_clean shape : {df_clean.shape}')
print(f'df_encoded shape: {df_encoded.shape}')
print(f'X shape        : {X.shape}')
print(f'y_reg shape    : {y_reg.shape}')

print('\n[Feature columns]')
display(pd.DataFrame({
    'feature_index': np.arange(len(df_encoded.columns)),
    'feature_name': df_encoded.columns.tolist(),
    'dtype': [df_encoded[c].dtype for c in df_encoded.columns]
}))

print('\n[Leakage column check]')
leakage_cols = ['casual', 'registered', 'cnt', 'instant', 'dteday']
leakage_in_features = [c for c in leakage_cols if c in df_encoded.columns]

print(f'feature에 포함된 leakage 후보: {leakage_in_features}')

if len(leakage_in_features) == 0:
    print('결론: casual, registered, cnt, instant, dteday가 X에서 제외되었으므로 leakage 통제가 적절하다.')
else:
    print('주의: leakage 가능 컬럼이 feature에 포함되어 있다. 반드시 제거해야 한다.')

print('\n[time_group one-hot check]')
time_group_cols = [c for c in df_encoded.columns if c.startswith('time_group_')]
print(f'time_group dummy columns: {time_group_cols}')
print(df_encoded[time_group_cols].sum())

print('\n해석:')
print('A3에서는 시간대 구조를 반영하기 위해 hr를 morning_rush/daytime/evening_rush/night로 파생했다.')
print('또한 weekday에서 is_weekend를 만들었다.')
print('이 두 feature는 A8의 시간대 수요 구조 가설과 직접 연결된다.')
print('casual과 registered는 cnt의 직접 구성요소이므로 feature에서 제외했다.')
```

```text
 === A3-1. Feature Engineering 결과 검증 ===
df_clean shape : (17379, 19)
df_encoded shape: (17379, 17)
X shape        : (17379, 17)
y_reg shape    : (17379,)

[Feature columns]
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature_index</th>
      <th>feature_name</th>
      <th>dtype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>season</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>yr</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>mnth</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>hr</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>holiday</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>weekday</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>workingday</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
      <td>weathersit</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>temp</td>
      <td>float64</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
      <td>atemp</td>
      <td>float64</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10</td>
      <td>hum</td>
      <td>float64</td>
    </tr>
    <tr>
      <th>11</th>
      <td>11</td>
      <td>windspeed</td>
      <td>float64</td>
    </tr>
    <tr>
      <th>12</th>
      <td>12</td>
      <td>is_weekend</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>13</th>
      <td>13</td>
      <td>time_group_daytime</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>14</th>
      <td>14</td>
      <td>time_group_evening_rush</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>15</th>
      <td>15</td>
      <td>time_group_morning_rush</td>
      <td>int64</td>
    </tr>
    <tr>
      <th>16</th>
      <td>16</td>
      <td>time_group_night</td>
      <td>int64</td>
    </tr>
  </tbody>
</table>
</div>

```text

[Leakage column check]
feature에 포함된 leakage 후보: []
결론: casual, registered, cnt, instant, dteday가 X에서 제외되었으므로 leakage 통제가 적절하다.

[time_group one-hot check]
time_group dummy columns: ['time_group_daytime', 'time_group_evening_rush', 'time_group_morning_rush', 'time_group_night']
time_group_daytime         5099
time_group_evening_rush    2914
time_group_morning_rush    2906
time_group_night           6460
dtype: int64

해석:
A3에서는 시간대 구조를 반영하기 위해 hr를 morning_rush/daytime/evening_rush/night로 파생했다.
또한 weekday에서 is_weekend를 만들었다.
이 두 feature는 A8의 시간대 수요 구조 가설과 직접 연결된다.
casual과 registered는 cnt의 직접 구성요소이므로 feature에서 제외했다.
```

```python
print(' === A4. EDA 기반 귀무가설 후보 3개 설정 ===')

hypothesis_table = pd.DataFrame([
    {
        'id': 'H0-1',
        'axis': '시간대 수요 구조',
        'H0': 'hr, time_group, workingday에 따라 cnt 분포 차이가 없다.',
        'H1': '시간대와 근무일 구조에 따라 cnt 분포가 달라진다.',
        'evidence_to_check': 'hour별 평균, workingday별 hour profile, time_group별 평균',
        'model_connection': 'hr, workingday, weekday, holiday, time_group을 feature로 유지'
    },
    {
        'id': 'H0-2',
        'axis': '날씨·쾌적성 구조',
        'H0': 'temp, atemp, hum, windspeed, weathersit은 cnt와 관계가 없다.',
        'H1': '날씨·쾌적성 변수는 자전거 대여량과 관련된다.',
        'evidence_to_check': 'Spearman correlation, weathersit별 평균 cnt',
        'model_connection': 'temp, atemp, hum, windspeed, weathersit을 feature로 유지'
    },
    {
        'id': 'H0-3',
        'axis': '계절·연도 효과',
        'H0': 'season, mnth, yr에 따라 cnt 분포 차이가 없다.',
        'H1': '계절성, 월별 패턴, 연도 성장 효과가 존재한다.',
        'evidence_to_check': 'season별 평균, month trend, yr별 평균',
        'model_connection': 'season, mnth, yr를 feature로 유지'
    }
])

display(hypothesis_table)

print('해석:')
print('이 노트북의 EDA는 단순 시각화가 아니라 feature 설계의 근거를 만드는 과정이다.')
print('A3에서 만든 feature set은 시간 구조, 날씨 구조, 계절/연도 구조라는 세 축으로 정리된다.')
print('이 세 가설이 Part B 회귀와 Part C 분류 모델의 입력 X 설계를 정당화한다.')

print(' === A5. H0-1 시간대 / 근무일 / 시간그룹 수요 구조 검정 ===')
print('RQ1. 자전거 대여량은 시간대와 근무일 여부에 따라 다른 패턴을 보이는가?')
print('H0-1: hr, time_group, workingday에 따라 cnt 분포 차이가 없다.')
print('H1-1: 시간대와 근무일 구조에 따라 cnt 분포가 달라진다.')

from scipy.stats import kruskal, mannwhitneyu, spearmanr

def p_decision(p, alpha=0.05):
    return 'reject H0' if p < alpha else 'fail to reject H0'

def eta_squared_by_group(data, group_col, target_col='cnt'):
    temp = data[[group_col, target_col]].dropna().copy()
    overall_mean = temp[target_col].mean()
    ss_between = 0
    
    for _, group in temp.groupby(group_col):
        ss_between += len(group) * (group[target_col].mean() - overall_mean) ** 2
    
    ss_total = ((temp[target_col] - overall_mean) ** 2).sum()
    return ss_between / ss_total if ss_total != 0 else np.nan

def kruskal_group_test(data, group_col, target_col='cnt'):
    groups = [
        g[target_col].dropna().values
        for _, g in data.groupby(group_col)
        if len(g[target_col].dropna()) > 0
    ]
    stat, p = kruskal(*groups)
    eta2 = eta_squared_by_group(data, group_col, target_col)
    return stat, p, eta2

def mannwhitney_binary_test(data, group_col, target_col='cnt'):
    g0 = data[data[group_col] == 0][target_col].dropna().values
    g1 = data[data[group_col] == 1][target_col].dropna().values
    stat, p = mannwhitneyu(g0, g1, alternative='two-sided')
    eta2 = eta_squared_by_group(data, group_col, target_col)
    return stat, p, eta2

hr_stat, hr_p, hr_eta2 = kruskal_group_test(df_clean, 'hr')
tg_stat, tg_p, tg_eta2 = kruskal_group_test(df_clean, 'time_group')
wd_stat, wd_p, wd_eta2 = mannwhitney_binary_test(df_clean, 'workingday')

time_test_result = pd.DataFrame([
    ['hr', 'Kruskal-Wallis', hr_stat, hr_p, p_decision(hr_p), hr_eta2],
    ['time_group', 'Kruskal-Wallis', tg_stat, tg_p, p_decision(tg_p), tg_eta2],
    ['workingday', 'Mann-Whitney U', wd_stat, wd_p, p_decision(wd_p), wd_eta2]
], columns=['feature_axis', 'test', 'statistic', 'p_value', 'decision_0.05', 'eta_squared_descriptive'])

display(time_test_result)

hour_pattern = df_clean.groupby('hr')['cnt'].agg(['count', 'mean', 'median', 'std']).reset_index()
display(hour_pattern)

plt.figure(figsize=(9, 4))
plt.plot(hour_pattern['hr'], hour_pattern['mean'], marker='o')
plt.title('Average Bike Rentals by Hour')
plt.xlabel('Hour')
plt.ylabel('Mean cnt')
plt.xticks(range(0, 24))
plt.grid(alpha=0.3)
plt.show()

print('시각화 1 해석:')
print('hour별 평균 cnt를 보면 새벽 시간대에는 수요가 낮고, 아침과 저녁 시간대에 수요가 급격히 커진다.')
print('특히 8시와 17~18시 부근에서 평균 대여량이 크게 올라가므로, hr는 단순 숫자 feature가 아니라 수요 패턴의 핵심 축이다.')
print('따라서 “시간대별 cnt 분포 차이가 없다”는 H0-1은 기각하는 방향으로 해석한다.')

working_hour_pattern = df_clean.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()

plt.figure(figsize=(10, 5))
for wd_value, label in [(0, 'non-workingday'), (1, 'workingday')]:
    temp = working_hour_pattern[working_hour_pattern['workingday'] == wd_value]
    plt.plot(temp['hr'], temp['cnt'], marker='o', label=label)

plt.title('Average cnt by Hour and Workingday')
plt.xlabel('Hour')
plt.ylabel('Mean cnt')
plt.xticks(range(0, 24))
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print('시각화 2 해석:')
print('workingday별 hour profile은 자전거 수요의 도메인 구조를 보여준다.')
print('workingday=1에서는 출근/퇴근 시간대의 commuting demand가 강하게 나타날 가능성이 크다.')
print('workingday=0에서는 출퇴근형 peak보다 낮 시간대 leisure demand가 상대적으로 중요할 수 있다.')
print('따라서 hr와 workingday는 독립적으로만 보는 것이 아니라 hr × workingday interaction 관점에서 해석해야 한다.')

time_group_summary = df_clean.groupby('time_group')['cnt'].agg(
    count='count',
    mean='mean',
    median='median',
    std='std'
).sort_values('mean', ascending=False)

display(time_group_summary)

plt.figure(figsize=(8, 4))
plt.bar(time_group_summary.index, time_group_summary['mean'])
plt.title('Average cnt by Time Group')
plt.xlabel('time_group')
plt.ylabel('Mean cnt')
plt.xticks(rotation=20)
plt.grid(axis='y', alpha=0.3)
plt.show()

print('시각화 3 해석:')
print('time_group별 평균을 보면 evening_rush가 가장 높고, night가 가장 낮다.')
print('이는 A3에서 만든 time_group 파생변수가 시간대 수요 구조를 압축하는 유용한 feature임을 보여준다.')

print('최종 결론:')
print(f'- hr p-value: {hr_p:.3e}, decision: {p_decision(hr_p)}')
print(f'- time_group p-value: {tg_p:.3e}, decision: {p_decision(tg_p)}')
print(f'- workingday p-value: {wd_p:.3e}, decision: {p_decision(wd_p)}')
print('==> H0-1은 기각한다. 시간대와 근무일 구조는 cnt 예측의 핵심 feature 축이다.')
```

```text
 === A4. EDA 기반 귀무가설 후보 3개 설정 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>axis</th>
      <th>H0</th>
      <th>H1</th>
      <th>evidence_to_check</th>
      <th>model_connection</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>H0-1</td>
      <td>시간대 수요 구조</td>
      <td>hr, time_group, workingday에 따라 cnt 분포 차이가 없다.</td>
      <td>시간대와 근무일 구조에 따라 cnt 분포가 달라진다.</td>
      <td>hour별 평균, workingday별 hour profile, time_group...</td>
      <td>hr, workingday, weekday, holiday, time_group을 ...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>H0-2</td>
      <td>날씨·쾌적성 구조</td>
      <td>temp, atemp, hum, windspeed, weathersit은 cnt와 ...</td>
      <td>날씨·쾌적성 변수는 자전거 대여량과 관련된다.</td>
      <td>Spearman correlation, weathersit별 평균 cnt</td>
      <td>temp, atemp, hum, windspeed, weathersit을 featu...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>H0-3</td>
      <td>계절·연도 효과</td>
      <td>season, mnth, yr에 따라 cnt 분포 차이가 없다.</td>
      <td>계절성, 월별 패턴, 연도 성장 효과가 존재한다.</td>
      <td>season별 평균, month trend, yr별 평균</td>
      <td>season, mnth, yr를 feature로 유지</td>
    </tr>
  </tbody>
</table>
</div>

```text
해석:
이 노트북의 EDA는 단순 시각화가 아니라 feature 설계의 근거를 만드는 과정이다.
A3에서 만든 feature set은 시간 구조, 날씨 구조, 계절/연도 구조라는 세 축으로 정리된다.
이 세 가설이 Part B 회귀와 Part C 분류 모델의 입력 X 설계를 정당화한다.
 === A5. H0-1 시간대 / 근무일 / 시간그룹 수요 구조 검정 ===
RQ1. 자전거 대여량은 시간대와 근무일 여부에 따라 다른 패턴을 보이는가?
H0-1: hr, time_group, workingday에 따라 cnt 분포 차이가 없다.
H1-1: 시간대와 근무일 구조에 따라 cnt 분포가 달라진다.
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature_axis</th>
      <th>test</th>
      <th>statistic</th>
      <th>p_value</th>
      <th>decision_0.05</th>
      <th>eta_squared_descriptive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>hr</td>
      <td>Kruskal-Wallis</td>
      <td>1.097304e+04</td>
      <td>0.000000</td>
      <td>reject H0</td>
      <td>0.501493</td>
    </tr>
    <tr>
      <th>1</th>
      <td>time_group</td>
      <td>Kruskal-Wallis</td>
      <td>7.874234e+03</td>
      <td>0.000000</td>
      <td>reject H0</td>
      <td>0.357591</td>
    </tr>
    <tr>
      <th>2</th>
      <td>workingday</td>
      <td>Mann-Whitney U</td>
      <td>3.185830e+07</td>
      <td>0.005558</td>
      <td>reject H0</td>
      <td>0.000917</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>hr</th>
      <th>count</th>
      <th>mean</th>
      <th>median</th>
      <th>std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>726</td>
      <td>53.898072</td>
      <td>40.0</td>
      <td>42.307910</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>724</td>
      <td>33.375691</td>
      <td>20.0</td>
      <td>33.538727</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>715</td>
      <td>22.869930</td>
      <td>11.0</td>
      <td>26.578642</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>697</td>
      <td>11.727403</td>
      <td>6.0</td>
      <td>13.239190</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>697</td>
      <td>6.352941</td>
      <td>6.0</td>
      <td>4.143818</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>717</td>
      <td>19.889819</td>
      <td>19.0</td>
      <td>13.200765</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>725</td>
      <td>76.044138</td>
      <td>76.0</td>
      <td>55.084348</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
      <td>727</td>
      <td>212.064649</td>
      <td>208.0</td>
      <td>161.441936</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>727</td>
      <td>359.011004</td>
      <td>385.0</td>
      <td>235.189285</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
      <td>727</td>
      <td>219.309491</td>
      <td>216.0</td>
      <td>93.703458</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10</td>
      <td>727</td>
      <td>173.668501</td>
      <td>147.0</td>
      <td>102.205413</td>
    </tr>
    <tr>
      <th>11</th>
      <td>11</td>
      <td>727</td>
      <td>208.143054</td>
      <td>180.0</td>
      <td>127.495536</td>
    </tr>
    <tr>
      <th>12</th>
      <td>12</td>
      <td>728</td>
      <td>253.315934</td>
      <td>229.0</td>
      <td>145.081134</td>
    </tr>
    <tr>
      <th>13</th>
      <td>13</td>
      <td>729</td>
      <td>253.661180</td>
      <td>224.0</td>
      <td>148.107657</td>
    </tr>
    <tr>
      <th>14</th>
      <td>14</td>
      <td>729</td>
      <td>240.949246</td>
      <td>212.0</td>
      <td>147.271574</td>
    </tr>
    <tr>
      <th>15</th>
      <td>15</td>
      <td>729</td>
      <td>251.233196</td>
      <td>227.0</td>
      <td>144.632541</td>
    </tr>
    <tr>
      <th>16</th>
      <td>16</td>
      <td>730</td>
      <td>311.983562</td>
      <td>304.5</td>
      <td>148.682618</td>
    </tr>
    <tr>
      <th>17</th>
      <td>17</td>
      <td>730</td>
      <td>461.452055</td>
      <td>475.0</td>
      <td>232.656611</td>
    </tr>
    <tr>
      <th>18</th>
      <td>18</td>
      <td>728</td>
      <td>425.510989</td>
      <td>418.5</td>
      <td>224.639304</td>
    </tr>
    <tr>
      <th>19</th>
      <td>19</td>
      <td>728</td>
      <td>311.523352</td>
      <td>309.5</td>
      <td>161.050359</td>
    </tr>
    <tr>
      <th>20</th>
      <td>20</td>
      <td>728</td>
      <td>226.030220</td>
      <td>223.5</td>
      <td>119.670164</td>
    </tr>
    <tr>
      <th>21</th>
      <td>21</td>
      <td>728</td>
      <td>172.314560</td>
      <td>173.5</td>
      <td>89.788893</td>
    </tr>
    <tr>
      <th>22</th>
      <td>22</td>
      <td>728</td>
      <td>131.335165</td>
      <td>129.0</td>
      <td>69.937782</td>
    </tr>
    <tr>
      <th>23</th>
      <td>23</td>
      <td>728</td>
      <td>87.831044</td>
      <td>80.0</td>
      <td>50.846889</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell011_out05_img04.png)

```text
시각화 1 해석:
hour별 평균 cnt를 보면 새벽 시간대에는 수요가 낮고, 아침과 저녁 시간대에 수요가 급격히 커진다.
특히 8시와 17~18시 부근에서 평균 대여량이 크게 올라가므로, hr는 단순 숫자 feature가 아니라 수요 패턴의 핵심 축이다.
따라서 “시간대별 cnt 분포 차이가 없다”는 H0-1은 기각하는 방향으로 해석한다.
```

![output](assets/3085_problem4_cell011_out07_img05.png)

```text
시각화 2 해석:
workingday별 hour profile은 자전거 수요의 도메인 구조를 보여준다.
workingday=1에서는 출근/퇴근 시간대의 commuting demand가 강하게 나타날 가능성이 크다.
workingday=0에서는 출퇴근형 peak보다 낮 시간대 leisure demand가 상대적으로 중요할 수 있다.
따라서 hr와 workingday는 독립적으로만 보는 것이 아니라 hr × workingday interaction 관점에서 해석해야 한다.
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
      <th>mean</th>
      <th>median</th>
      <th>std</th>
    </tr>
    <tr>
      <th>time_group</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>evening_rush</th>
      <td>2914</td>
      <td>356.201441</td>
      <td>325.0</td>
      <td>211.890752</td>
    </tr>
    <tr>
      <th>daytime</th>
      <td>5099</td>
      <td>241.902138</td>
      <td>214.0</td>
      <td>144.093134</td>
    </tr>
    <tr>
      <th>morning_rush</th>
      <td>2906</td>
      <td>216.704061</td>
      <td>169.0</td>
      <td>182.485182</td>
    </tr>
    <tr>
      <th>night</th>
      <td>6460</td>
      <td>60.604799</td>
      <td>29.0</td>
      <td>72.478411</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell011_out10_img06.png)

```text
시각화 3 해석:
time_group별 평균을 보면 evening_rush가 가장 높고, night가 가장 낮다.
이는 A3에서 만든 time_group 파생변수가 시간대 수요 구조를 압축하는 유용한 feature임을 보여준다.
최종 결론:
- hr p-value: 0.000e+00, decision: reject H0
- time_group p-value: 0.000e+00, decision: reject H0
- workingday p-value: 5.558e-03, decision: reject H0
==> H0-1은 기각한다. 시간대와 근무일 구조는 cnt 예측의 핵심 feature 축이다.
```

```python
print(' === A6. H0-2 날씨·쾌적성 변수와 cnt 관계 검정 ===')
print('RQ2. 기온, 체감온도, 습도, 풍속, 날씨 상태는 자전거 대여량과 관계가 있는가?')
print('H0-2: temp, atemp, hum, windspeed, weathersit은 cnt와 관계가 없다.')
print('H1-2: 날씨·쾌적성 변수는 cnt와 관련된다.')

weather_features = ['temp', 'atemp', 'hum', 'windspeed']

weather_corr_rows = []

for col in weather_features:
    spear_corr, spear_p = spearmanr(df_clean[col], df_clean['cnt'])
    pearson_corr = df_clean[[col, 'cnt']].corr(method='pearson').iloc[0, 1]
    
    weather_corr_rows.append({
        'feature': col,
        'pearson_corr': pearson_corr,
        'spearman_corr': spear_corr,
        'spearman_p_value': spear_p,
        'decision_0.05': p_decision(spear_p),
        'abs_spearman': abs(spear_corr)
    })

weather_corr_result = pd.DataFrame(weather_corr_rows).sort_values('abs_spearman', ascending=False)
display(weather_corr_result)

weather_stat, weather_p, weather_eta2 = kruskal_group_test(df_clean, 'weathersit')

weather_test_result = pd.DataFrame([[
    'weathersit',
    'Kruskal-Wallis',
    weather_stat,
    weather_p,
    p_decision(weather_p),
    weather_eta2
]], columns=['feature_axis', 'test', 'statistic', 'p_value', 'decision_0.05', 'eta_squared_descriptive'])

display(weather_test_result)

plot_df = weather_corr_result.sort_values('spearman_corr')

plt.figure(figsize=(8, 4))
plt.barh(plot_df['feature'], plot_df['spearman_corr'])
plt.axvline(0)
plt.title('Spearman Correlation with cnt')
plt.xlabel('Spearman correlation')
plt.ylabel('weather feature')
plt.grid(axis='x', alpha=0.3)
plt.show()

print('시각화 1 해석:')
print('temp와 atemp는 cnt와 양의 관계를 보인다. 즉 기온 또는 체감온도가 올라가면 자전거 이용이 증가하는 경향이 있다.')
print('hum은 cnt와 음의 관계를 보인다. 습도가 높을수록 야외 이동 선호가 낮아질 수 있다.')
print('windspeed는 상대적으로 약한 관계이므로 단독 핵심 feature라기보다 시간대/계절과 함께 해석해야 한다.')

for col in ['temp', 'hum']:
    plt.figure(figsize=(6, 4))
    plt.hexbin(df_clean[col], df_clean['cnt'], gridsize=35, mincnt=1)
    plt.colorbar(label='count')
    plt.title(f'{col} vs cnt')
    plt.xlabel(col)
    plt.ylabel('cnt')
    plt.show()
    
    print(f'시각화 해석: {col} vs cnt')
    if col == 'temp':
        print('temp는 자전거 이용 쾌적성과 연결된다. 낮은 기온보다 적절히 높은 기온에서 수요가 커지는 패턴을 확인한다.')
    else:
        print('hum은 습도 변수다. 높은 습도에서 대여량이 낮아지는 경향이 있으면 야외활동 불쾌감이 수요를 낮추는 요인으로 해석할 수 있다.')

weather_map = {
    1: 'clear_or_partly_cloudy',
    2: 'mist_or_cloudy',
    3: 'light_rain_or_snow',
    4: 'heavy_rain_or_bad_weather'
}

df_clean['weathersit_label'] = df_clean['weathersit'].map(weather_map)

weather_summary = df_clean.groupby(['weathersit', 'weathersit_label'])['cnt'].agg(
    count='count',
    mean='mean',
    median='median',
    std='std'
).reset_index()

display(weather_summary)

plt.figure(figsize=(9, 4))
plt.bar(weather_summary['weathersit_label'], weather_summary['mean'])
plt.title('Average cnt by Weather Situation')
plt.xlabel('Weather situation')
plt.ylabel('Mean cnt')
plt.xticks(rotation=20)
plt.grid(axis='y', alpha=0.3)
plt.show()

print('시각화 3 해석:')
print('weathersit이 나빠질수록 평균 cnt가 낮아지는 경향이 나타난다.')
print('clear_or_partly_cloudy의 평균 수요가 가장 높고, light_rain_or_snow에서는 수요가 크게 낮아진다.')
print('단, heavy_rain_or_bad_weather는 관측치가 3개뿐이므로 평균 해석은 조심해야 한다.')

print('최종 결론:')
print(f'- weathersit p-value: {weather_p:.3e}, decision: {p_decision(weather_p)}')
print('==> H0-2는 기각한다. 날씨·쾌적성 변수는 cnt와 관련되며, temp, atemp, hum, weathersit은 모델 입력으로 타당하다.')
```

```text
 === A6. H0-2 날씨·쾌적성 변수와 cnt 관계 검정 ===
RQ2. 기온, 체감온도, 습도, 풍속, 날씨 상태는 자전거 대여량과 관계가 있는가?
H0-2: temp, atemp, hum, windspeed, weathersit은 cnt와 관계가 없다.
H1-2: 날씨·쾌적성 변수는 cnt와 관련된다.
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature</th>
      <th>pearson_corr</th>
      <th>spearman_corr</th>
      <th>spearman_p_value</th>
      <th>decision_0.05</th>
      <th>abs_spearman</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>temp</td>
      <td>0.404772</td>
      <td>0.423330</td>
      <td>0.000000e+00</td>
      <td>reject H0</td>
      <td>0.423330</td>
    </tr>
    <tr>
      <th>1</th>
      <td>atemp</td>
      <td>0.400929</td>
      <td>0.423258</td>
      <td>0.000000e+00</td>
      <td>reject H0</td>
      <td>0.423258</td>
    </tr>
    <tr>
      <th>2</th>
      <td>hum</td>
      <td>-0.322911</td>
      <td>-0.359614</td>
      <td>0.000000e+00</td>
      <td>reject H0</td>
      <td>0.359614</td>
    </tr>
    <tr>
      <th>3</th>
      <td>windspeed</td>
      <td>0.093234</td>
      <td>0.126629</td>
      <td>4.809744e-63</td>
      <td>reject H0</td>
      <td>0.126629</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature_axis</th>
      <th>test</th>
      <th>statistic</th>
      <th>p_value</th>
      <th>decision_0.05</th>
      <th>eta_squared_descriptive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>weathersit</td>
      <td>Kruskal-Wallis</td>
      <td>397.030875</td>
      <td>9.733811e-86</td>
      <td>reject H0</td>
      <td>0.021486</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell012_out03_img07.png)

```text
시각화 1 해석:
temp와 atemp는 cnt와 양의 관계를 보인다. 즉 기온 또는 체감온도가 올라가면 자전거 이용이 증가하는 경향이 있다.
hum은 cnt와 음의 관계를 보인다. 습도가 높을수록 야외 이동 선호가 낮아질 수 있다.
windspeed는 상대적으로 약한 관계이므로 단독 핵심 feature라기보다 시간대/계절과 함께 해석해야 한다.
```

![output](assets/3085_problem4_cell012_out05_img08.png)

```text
시각화 해석: temp vs cnt
temp는 자전거 이용 쾌적성과 연결된다. 낮은 기온보다 적절히 높은 기온에서 수요가 커지는 패턴을 확인한다.
```

![output](assets/3085_problem4_cell012_out07_img09.png)

```text
시각화 해석: hum vs cnt
hum은 습도 변수다. 높은 습도에서 대여량이 낮아지는 경향이 있으면 야외활동 불쾌감이 수요를 낮추는 요인으로 해석할 수 있다.
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>weathersit</th>
      <th>weathersit_label</th>
      <th>count</th>
      <th>mean</th>
      <th>median</th>
      <th>std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>clear_or_partly_cloudy</td>
      <td>11413</td>
      <td>204.869272</td>
      <td>159.0</td>
      <td>189.487773</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>mist_or_cloudy</td>
      <td>4544</td>
      <td>175.165493</td>
      <td>133.0</td>
      <td>165.431589</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>light_rain_or_snow</td>
      <td>1419</td>
      <td>111.579281</td>
      <td>63.0</td>
      <td>133.781045</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>heavy_rain_or_bad_weather</td>
      <td>3</td>
      <td>74.333333</td>
      <td>36.0</td>
      <td>77.925178</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell012_out10_img10.png)

```text
시각화 3 해석:
weathersit이 나빠질수록 평균 cnt가 낮아지는 경향이 나타난다.
clear_or_partly_cloudy의 평균 수요가 가장 높고, light_rain_or_snow에서는 수요가 크게 낮아진다.
단, heavy_rain_or_bad_weather는 관측치가 3개뿐이므로 평균 해석은 조심해야 한다.
최종 결론:
- weathersit p-value: 9.734e-86, decision: reject H0
==> H0-2는 기각한다. 날씨·쾌적성 변수는 cnt와 관련되며, temp, atemp, hum, weathersit은 모델 입력으로 타당하다.
```

```python
print(' === A7-1. H0-3 계절 / 월 / 연도 효과 검정 ===')
print('RQ3. 자전거 대여량은 season, month, year에 따라 달라지는가?')
print('H0-3: season, mnth, yr에 따라 cnt 분포 차이가 없다.')
print('H1-3: 계절성, 월별 패턴, 연도 성장 효과가 존재한다.')

season_stat, season_p, season_eta2 = kruskal_group_test(df_clean, 'season')
month_stat, month_p, month_eta2 = kruskal_group_test(df_clean, 'mnth')
yr_stat, yr_p, yr_eta2 = mannwhitney_binary_test(df_clean, 'yr')

season_test_result = pd.DataFrame([
    ['season', 'Kruskal-Wallis', season_stat, season_p, p_decision(season_p), season_eta2],
    ['mnth', 'Kruskal-Wallis', month_stat, month_p, p_decision(month_p), month_eta2],
    ['yr', 'Mann-Whitney U', yr_stat, yr_p, p_decision(yr_p), yr_eta2]
], columns=['feature_axis', 'test', 'statistic', 'p_value', 'decision_0.05', 'eta_squared_descriptive'])

display(season_test_result)

season_map = {
    1: 'winter',
    2: 'spring',
    3: 'summer',
    4: 'fall'
}

df_clean['season_label'] = df_clean['season'].map(season_map)

season_summary = df_clean.groupby(['season', 'season_label'])['cnt'].agg(
    count='count',
    mean='mean',
    median='median',
    std='std'
).reset_index()

display(season_summary)

plt.figure(figsize=(8, 4))
plt.bar(season_summary['season_label'], season_summary['mean'])
plt.title('Average cnt by Season')
plt.xlabel('Season')
plt.ylabel('Mean cnt')
plt.grid(axis='y', alpha=0.3)
plt.show()

print('시각화 1 해석:')
print('season별 평균 cnt를 보면 winter가 가장 낮고, spring/summer/fall에서 수요가 증가한다.')
print('이는 자전거 이용이 야외활동 가능성과 계절 조건에 강하게 반응한다는 뜻이다.')
print('따라서 season은 단순 숫자가 아니라 계절성 수요를 담는 중요한 categorical feature다.')

month_summary = df_clean.groupby('mnth')['cnt'].agg(['count', 'mean', 'median', 'std']).reset_index()
display(month_summary)

plt.figure(figsize=(9, 4))
plt.plot(month_summary['mnth'], month_summary['mean'], marker='o')
plt.title('Average cnt by Month')
plt.xlabel('Month')
plt.ylabel('Mean cnt')
plt.xticks(range(1, 13))
plt.grid(alpha=0.3)
plt.show()

print('시각화 2 해석:')
print('mnth별 평균은 장기 계절성을 더 세밀하게 보여준다.')
print('월별 패턴은 season보다 더 촘촘한 시간 정보를 제공하므로 회귀와 분류 모델 모두에서 유용할 수 있다.')
print('단, season과 mnth는 서로 관련이 크므로 둘의 중복성은 해석 시 유의해야 한다.')

year_summary = df_clean.groupby('yr')['cnt'].agg(['count', 'mean', 'median', 'std']).reset_index()
display(year_summary)

plt.figure(figsize=(6, 4))
plt.bar(year_summary['yr'].astype(str), year_summary['mean'])
plt.title('Average cnt by Year Code')
plt.xlabel('yr: 0=2011, 1=2012')
plt.ylabel('Mean cnt')
plt.grid(axis='y', alpha=0.3)
plt.show()

print('시각화 3 해석:')
print('yr=1의 평균 cnt가 yr=0보다 높다.')
print('이는 단순한 날씨 차이라기보다 서비스 확산, 이용자 증가, 등록 사용자 기반 확대 같은 연도 성장 효과를 반영할 수 있다.')
print('따라서 yr는 모델에 포함할 가치가 있는 시간 feature다.')

print('최종 결론:')
print(f'- season p-value: {season_p:.3e}, decision: {p_decision(season_p)}')
print(f'- mnth p-value: {month_p:.3e}, decision: {p_decision(month_p)}')
print(f'- yr p-value: {yr_p:.3e}, decision: {p_decision(yr_p)}')
print('==> H0-3은 기각한다. 계절성, 월별 패턴, 연도 성장 효과가 존재하므로 season, mnth, yr를 모델 feature로 유지한다.')
```

```text
 === A7-1. H0-3 계절 / 월 / 연도 효과 검정 ===
RQ3. 자전거 대여량은 season, month, year에 따라 달라지는가?
H0-3: season, mnth, yr에 따라 cnt 분포 차이가 없다.
H1-3: 계절성, 월별 패턴, 연도 성장 효과가 존재한다.
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature_axis</th>
      <th>test</th>
      <th>statistic</th>
      <th>p_value</th>
      <th>decision_0.05</th>
      <th>eta_squared_descriptive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>season</td>
      <td>Kruskal-Wallis</td>
      <td>1.190269e+03</td>
      <td>9.474683e-258</td>
      <td>reject H0</td>
      <td>0.065988</td>
    </tr>
    <tr>
      <th>1</th>
      <td>mnth</td>
      <td>Kruskal-Wallis</td>
      <td>1.290516e+03</td>
      <td>4.964875e-270</td>
      <td>reject H0</td>
      <td>0.075049</td>
    </tr>
    <tr>
      <th>2</th>
      <td>yr</td>
      <td>Mann-Whitney U</td>
      <td>2.870715e+07</td>
      <td>9.740686e-165</td>
      <td>reject H0</td>
      <td>0.062748</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>season</th>
      <th>season_label</th>
      <th>count</th>
      <th>mean</th>
      <th>median</th>
      <th>std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>winter</td>
      <td>4242</td>
      <td>111.114569</td>
      <td>76.0</td>
      <td>119.224010</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>spring</td>
      <td>4409</td>
      <td>208.344069</td>
      <td>165.0</td>
      <td>188.362473</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>summer</td>
      <td>4496</td>
      <td>236.016237</td>
      <td>199.0</td>
      <td>197.711630</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>fall</td>
      <td>4232</td>
      <td>198.868856</td>
      <td>155.5</td>
      <td>182.967972</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell013_out03_img11.png)

```text
시각화 1 해석:
season별 평균 cnt를 보면 winter가 가장 낮고, spring/summer/fall에서 수요가 증가한다.
이는 자전거 이용이 야외활동 가능성과 계절 조건에 강하게 반응한다는 뜻이다.
따라서 season은 단순 숫자가 아니라 계절성 수요를 담는 중요한 categorical feature다.
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>mnth</th>
      <th>count</th>
      <th>mean</th>
      <th>median</th>
      <th>std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1429</td>
      <td>94.424773</td>
      <td>66.0</td>
      <td>99.907146</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1341</td>
      <td>112.865026</td>
      <td>82.0</td>
      <td>112.486565</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1473</td>
      <td>155.410726</td>
      <td>104.0</td>
      <td>163.543050</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1437</td>
      <td>187.260960</td>
      <td>136.0</td>
      <td>181.137902</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>1488</td>
      <td>222.907258</td>
      <td>188.5</td>
      <td>187.721497</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>1440</td>
      <td>240.515278</td>
      <td>203.0</td>
      <td>196.038950</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>1488</td>
      <td>231.819892</td>
      <td>202.0</td>
      <td>187.483806</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>1475</td>
      <td>238.097627</td>
      <td>204.0</td>
      <td>200.444648</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>1437</td>
      <td>240.773138</td>
      <td>190.0</td>
      <td>214.609531</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>1451</td>
      <td>222.158511</td>
      <td>174.0</td>
      <td>203.477057</td>
    </tr>
    <tr>
      <th>10</th>
      <td>11</td>
      <td>1437</td>
      <td>177.335421</td>
      <td>145.0</td>
      <td>158.973887</td>
    </tr>
    <tr>
      <th>11</th>
      <td>12</td>
      <td>1483</td>
      <td>142.303439</td>
      <td>106.0</td>
      <td>141.080674</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell013_out06_img12.png)

```text
시각화 2 해석:
mnth별 평균은 장기 계절성을 더 세밀하게 보여준다.
월별 패턴은 season보다 더 촘촘한 시간 정보를 제공하므로 회귀와 분류 모델 모두에서 유용할 수 있다.
단, season과 mnth는 서로 관련이 크므로 둘의 중복성은 해석 시 유의해야 한다.
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>yr</th>
      <th>count</th>
      <th>mean</th>
      <th>median</th>
      <th>std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>8645</td>
      <td>143.794448</td>
      <td>109.0</td>
      <td>133.797854</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>8734</td>
      <td>234.666361</td>
      <td>191.0</td>
      <td>208.910941</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell013_out09_img13.png)

```text
시각화 3 해석:
yr=1의 평균 cnt가 yr=0보다 높다.
이는 단순한 날씨 차이라기보다 서비스 확산, 이용자 증가, 등록 사용자 기반 확대 같은 연도 성장 효과를 반영할 수 있다.
따라서 yr는 모델에 포함할 가치가 있는 시간 feature다.
최종 결론:
- season p-value: 9.475e-258, decision: reject H0
- mnth p-value: 4.965e-270, decision: reject H0
- yr p-value: 9.741e-165, decision: reject H0
==> H0-3은 기각한다. 계절성, 월별 패턴, 연도 성장 효과가 존재하므로 season, mnth, yr를 모델 feature로 유지한다.
```

```python
print(' === A8. EDA 최종 결론 및 모델링 연결 ===')

eda_conclusion_table = pd.DataFrame([
    [
        'Target distribution',
        'cnt는 평균 189.46, 중앙값 142, max 977로 오른쪽 꼬리가 존재한다.',
        '회귀에서는 log1p(cnt)를 target으로 사용하고, test 평가는 expm1 후 원본 스케일 MAE로 계산한다.'
    ],
    [
        'Time demand structure',
        'hr, workingday, time_group에 따라 수요 패턴이 크게 달라진다.',
        'hr, workingday, weekday, holiday, time_group을 feature로 사용한다.'
    ],
    [
        'Weather comfort',
        'temp/atemp는 양의 관계, hum은 음의 관계, weathersit 악화 시 cnt 감소 경향이 있다.',
        'temp, atemp, hum, windspeed, weathersit을 feature로 사용한다.'
    ],
    [
        'Season/year effect',
        'season, mnth, yr에 따라 평균 수요가 달라진다.',
        'season, mnth, yr를 장기 수요 패턴 feature로 사용한다.'
    ],
    [
        'Leakage control',
        'casual + registered == cnt 비율이 1.0이다.',
        'casual, registered, cnt, instant, dteday는 X에서 제외한다.'
    ],
    [
        'Classification target',
        'cnt의 33%, 66% 분위수 기준 binning 결과 low/mid/high 클래스가 거의 균등하다.',
        'Part C에서는 stratify=y_cls로 60/20/20 split한다.'
    ]
], columns=['EDA finding', 'evidence', 'modeling decision'])

display(eda_conclusion_table)

print('최종 EDA 결론:')
print('1. 이 데이터는 시간별 자전거 대여량 cnt를 예측하는 도시 수요 예측 문제다.')
print('2. cnt는 오른쪽 꼬리가 있는 count target이므로, 회귀에서는 log1p 변환을 적용하는 것이 타당하다.')
print('3. 가장 강한 도메인 축은 시간대 수요 구조다. hr, workingday, time_group은 반드시 유지한다.')
print('4. 날씨 변수는 수요의 쾌적성 조건을 설명한다. temp/atemp는 양의 관계, hum은 음의 관계를 보인다.')
print('5. season, mnth, yr는 계절성과 연도 성장 효과를 담으므로 모델 feature로 유지한다.')
print('6. casual과 registered는 cnt의 직접 구성요소이므로 절대 feature에 넣지 않는다.')
print('7. Part B는 log1p(cnt) 회귀 문제, Part C는 분위수 기반 3-class classification 문제로 설계한다.')
print('==> 따라서 최종 feature set은 시간 + 계절 + 날씨 + 파생 time_group/is_weekend를 포함하되, leakage 컬럼은 제외하는 구조가 타당하다.')
```

```text
 === A8. EDA 최종 결론 및 모델링 연결 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>EDA finding</th>
      <th>evidence</th>
      <th>modeling decision</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Target distribution</td>
      <td>cnt는 평균 189.46, 중앙값 142, max 977로 오른쪽 꼬리가 존재한다.</td>
      <td>회귀에서는 log1p(cnt)를 target으로 사용하고, test 평가는 expm...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Time demand structure</td>
      <td>hr, workingday, time_group에 따라 수요 패턴이 크게 달라진다.</td>
      <td>hr, workingday, weekday, holiday, time_group을 ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Weather comfort</td>
      <td>temp/atemp는 양의 관계, hum은 음의 관계, weathersit 악화 시...</td>
      <td>temp, atemp, hum, windspeed, weathersit을 featu...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Season/year effect</td>
      <td>season, mnth, yr에 따라 평균 수요가 달라진다.</td>
      <td>season, mnth, yr를 장기 수요 패턴 feature로 사용한다.</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Leakage control</td>
      <td>casual + registered == cnt 비율이 1.0이다.</td>
      <td>casual, registered, cnt, instant, dteday는 X에서 ...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Classification target</td>
      <td>cnt의 33%, 66% 분위수 기준 binning 결과 low/mid/high 클...</td>
      <td>Part C에서는 stratify=y_cls로 60/20/20 split한다.</td>
    </tr>
  </tbody>
</table>
</div>

```text
최종 EDA 결론:
1. 이 데이터는 시간별 자전거 대여량 cnt를 예측하는 도시 수요 예측 문제다.
2. cnt는 오른쪽 꼬리가 있는 count target이므로, 회귀에서는 log1p 변환을 적용하는 것이 타당하다.
3. 가장 강한 도메인 축은 시간대 수요 구조다. hr, workingday, time_group은 반드시 유지한다.
4. 날씨 변수는 수요의 쾌적성 조건을 설명한다. temp/atemp는 양의 관계, hum은 음의 관계를 보인다.
5. season, mnth, yr는 계절성과 연도 성장 효과를 담으므로 모델 feature로 유지한다.
6. casual과 registered는 cnt의 직접 구성요소이므로 절대 feature에 넣지 않는다.
7. Part B는 log1p(cnt) 회귀 문제, Part C는 분위수 기반 3-class classification 문제로 설계한다.
==> 따라서 최종 feature set은 시간 + 계절 + 날씨 + 파생 time_group/is_weekend를 포함하되, leakage 컬럼은 제외하는 구조가 타당하다.
```

---
# Part B. 회귀 모델: cnt 예측 (10점)

B0. 회귀/분류 공통 준비

```python
print(' === B0. 회귀/분류 공통 준비 ===')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    f1_score,
    confusion_matrix,
    classification_report
)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras import Sequential
from keras.layers import Dense, Dropout, BatchNormalization, Activation
from keras.regularizers import l2
from keras.callbacks import EarlyStopping

np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

required_names = ['X', 'y_reg', 'df_clean', 'df_encoded']
missing_names = [name for name in required_names if name not in globals()]
if missing_names:
    raise NameError(f'A3 Feature Engineering 셀을 먼저 실행해야 합니다. 누락 객체: {missing_names}')

print(f'X shape: {X.shape}')
print(f'y_reg shape: {y_reg.shape}')
print(f'Feature count: {X.shape[1]}')

print('\n해석:')
print('B파트 회귀와 C파트 분류는 A3에서 만든 동일한 feature X를 사용한다.')
print('단, 회귀는 log1p(cnt)를 target으로 사용하고, 분류는 cnt를 분위수 기준 low/mid/high로 변환한다.')
print('casual, registered, cnt, instant, dteday는 feature에서 제외된 상태여야 한다.')
```

```text
 === B0. 회귀/분류 공통 준비 ===
X shape: (17379, 17)
y_reg shape: (17379,)
Feature count: 17

해석:
B파트 회귀와 C파트 분류는 A3에서 만든 동일한 feature X를 사용한다.
단, 회귀는 log1p(cnt)를 target으로 사용하고, 분류는 cnt를 분위수 기준 low/mid/high로 변환한다.
casual, registered, cnt, instant, dteday는 feature에서 제외된 상태여야 한다.
```


## B1. 데이터 분할 + 정규화

- 타겟에 log 변환 적용 (`np.log1p`)
- 3분할 60/20/20, random_state=SEED
- StandardScaler 적용 (fit은 train에만)

```python
print(' === B1. 회귀 데이터 분할 + 정규화 ===')

# 회귀 target: long-tail 완화를 위해 log1p 적용
y_reg_log = np.log1p(y_reg)

X_temp, X_test, y_temp, y_test_reg = train_test_split(
    X,
    y_reg_log,
    test_size=0.2,
    random_state=SEED
)

X_train_r, X_val_r, y_train_reg, y_val_reg = train_test_split(
    X_temp,
    y_temp,
    test_size=0.25,
    random_state=SEED
)

scaler_r = StandardScaler()
X_train_r = scaler_r.fit_transform(X_train_r)
X_val_r = scaler_r.transform(X_val_r)
X_test_r = scaler_r.transform(X_test)

print(f'Train: {X_train_r.shape}')
print(f'Val  : {X_val_r.shape}')
print(f'Test : {X_test_r.shape}')
print(f'y_train_reg: {y_train_reg.shape}')
print(f'y_val_reg  : {y_val_reg.shape}')
print(f'y_test_reg : {y_test_reg.shape}')

print('\nTarget check:')
print(f'Original cnt mean       : {y_reg.mean():.4f}')
print(f'Original cnt median     : {np.median(y_reg):.4f}')
print(f'log1p(cnt) mean         : {y_reg_log.mean():.4f}')
print(f'log1p(cnt) std          : {y_reg_log.std():.4f}')

print('\n해석:')
print('cnt는 오른쪽 꼬리가 있는 count target이므로 log1p(cnt)를 회귀 target으로 사용한다.')
print('X는 train/validation/test = 60/20/20으로 분할했다.')
print('StandardScaler는 train set에만 fit하고, validation/test에는 transform만 적용해 데이터 누수를 방지한다.')
print('최종 평가는 log 공간이 아니라 expm1으로 원본 cnt 단위로 복원한 뒤 MAE를 계산한다.')
```

```text
 === B1. 회귀 데이터 분할 + 정규화 ===
Train: (10427, 17)
Val  : (3476, 17)
Test : (3476, 17)
y_train_reg: (10427,)
y_val_reg  : (3476,)
y_test_reg : (3476,)

Target check:
Original cnt mean       : 189.4631
Original cnt median     : 142.0000
log1p(cnt) mean         : 4.5747
log1p(cnt) std          : 1.4178

해석:
cnt는 오른쪽 꼬리가 있는 count target이므로 log1p(cnt)를 회귀 target으로 사용한다.
X는 train/validation/test = 60/20/20으로 분할했다.
StandardScaler는 train set에만 fit하고, validation/test에는 transform만 적용해 데이터 누수를 방지한다.
최종 평가는 log 공간이 아니라 expm1으로 원본 cnt 단위로 복원한 뒤 MAE를 계산한다.
```

## B2. Baseline + Regularized 회귀 모델 (7점)

**요구사항**:
- **Baseline**: Dense 2-3개 층, 정규화 없음
- **Regularized**: L2 + BatchNorm + Dropout + EarlyStopping 모두 적용
- 출력층: `Dense(1)` (회귀이므로 활성함수 없음)
- Loss: MSE, Metric: MAE
- 두 모델 모두 학습 + 결과 출력

```python
print(' === B2. Baseline + Regularized 회귀 모델 학습 ===')

input_dim_r = X_train_r.shape[1]

def build_regression_baseline():
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(input_dim_r,)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))  # 회귀 출력층: activation 없음
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    return model

def build_regression_regularized():
    model = Sequential()
    
    model.add(Dense(128, kernel_regularizer=l2(0.001), input_shape=(input_dim_r,)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.25))
    
    model.add(Dense(64, kernel_regularizer=l2(0.001)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.25))
    
    model.add(Dense(32, kernel_regularizer=l2(0.001)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.15))
    
    model.add(Dense(1))  # 회귀 출력층: activation 없음
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    return model

np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

reg_baseline_model = build_regression_baseline()

reg_baseline_history = reg_baseline_model.fit(
    X_train_r,
    y_train_reg,
    validation_data=(X_val_r, y_val_reg),
    epochs=80,
    batch_size=64,
    verbose=0
)

np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

reg_regularized_model = build_regression_regularized()

reg_early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

reg_regularized_history = reg_regularized_model.fit(
    X_train_r,
    y_train_reg,
    validation_data=(X_val_r, y_val_reg),
    epochs=150,
    batch_size=64,
    callbacks=[reg_early_stop],
    verbose=0
)

def get_reg_history_result(model_name, history):
    train_loss = history.history['loss'][-1]
    val_loss = history.history['val_loss'][-1]
    gap = val_loss - train_loss
    train_mae = history.history['mae'][-1]
    val_mae = history.history['val_mae'][-1]
    
    print(f'[{model_name}]')
    print(f'Epochs        : {len(history.history["loss"])}')
    print(f'Train Loss    : {train_loss:.4f}')
    print(f'Val Loss      : {val_loss:.4f}')
    print(f'Gap           : {gap:.4f}')
    print(f'Train MAE log : {train_mae:.4f}')
    print(f'Val MAE log   : {val_mae:.4f}')
    
    return {
        'model': model_name,
        'epochs': len(history.history['loss']),
        'train_loss_log_mse': train_loss,
        'val_loss_log_mse': val_loss,
        'gap': gap,
        'train_mae_log': train_mae,
        'val_mae_log': val_mae
    }

reg_history_result_df = pd.DataFrame([
    get_reg_history_result('Baseline', reg_baseline_history),
    get_reg_history_result('Regularized', reg_regularized_history)
])

display(reg_history_result_df)

plt.figure(figsize=(9, 5))
plt.plot(reg_baseline_history.history['val_loss'], label='Baseline Val Loss')
plt.plot(reg_regularized_history.history['val_loss'], label='Regularized Val Loss')
plt.title('Regression Validation Loss: Baseline vs Regularized')
plt.xlabel('Epoch')
plt.ylabel('Validation Loss (log-space MSE)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print('시각화 1 해석:')
print('이 그래프는 log1p(cnt) 회귀에서 Baseline과 Regularized 모델의 validation loss 흐름을 비교한다.')
print('Baseline은 정규화가 없는 기본 DNN이고, Regularized는 L2, BatchNorm, Dropout, EarlyStopping을 모두 적용한 모델이다.')
print('validation loss가 더 낮고 안정적인 모델이 log target 기준 일반화 성능이 더 좋다.')
print('단, 최종 평가는 log 공간이 아니라 원본 cnt 스케일로 복원한 뒤 MAE를 비교해야 한다.')

plt.figure(figsize=(9, 4))
plt.plot(reg_baseline_history.history['loss'], label='Baseline Train Loss')
plt.plot(reg_baseline_history.history['val_loss'], label='Baseline Val Loss')
plt.title('Baseline Regression Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss (log-space MSE)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print('시각화 2 해석:')
print('Baseline loss curve는 정규화 없는 기본 DNN이 train/validation에서 어떻게 학습되는지 보여준다.')
print('train loss와 validation loss의 차이가 커지면 train set에 더 잘 맞는 generalization gap으로 해석한다.')
print('이후 Regularized 모델이 이 gap과 validation loss를 얼마나 개선하는지 비교한다.')

plt.figure(figsize=(9, 4))
plt.plot(reg_regularized_history.history['loss'], label='Regularized Train Loss')
plt.plot(reg_regularized_history.history['val_loss'], label='Regularized Val Loss')
plt.title('Regularized Regression Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss (log-space MSE)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print('시각화 3 해석:')
print('Regularized 모델은 L2, BatchNorm, Dropout, EarlyStopping을 함께 적용한 모델이다.')
print('Dropout과 L2는 과도한 parameter 의존을 줄이고, BatchNorm은 hidden activation scale을 안정화한다.')
print('EarlyStopping은 validation loss가 더 이상 개선되지 않으면 학습을 중단하고 best weight를 복원한다.')
```

```text
 === B2. Baseline + Regularized 회귀 모델 학습 ===
```

```text
/home/sieg/projects-wsl/hongikUniv.-26_1/.venv/lib/python3.12/site-packages/keras/src/layers/core/dense.py:107: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
  super().__init__(activity_regularizer=activity_regularizer, **kwargs)
```

```text
[Baseline]
Epochs        : 80
Train Loss    : 0.0859
Val Loss      : 0.1081
Gap           : 0.0221
Train MAE log : 0.2112
Val MAE log   : 0.2348
[Regularized]
Epochs        : 72
Train Loss    : 0.3332
Val Loss      : 0.1766
Gap           : -0.1565
Train MAE log : 0.4265
Val MAE log   : 0.2786
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>epochs</th>
      <th>train_loss_log_mse</th>
      <th>val_loss_log_mse</th>
      <th>gap</th>
      <th>train_mae_log</th>
      <th>val_mae_log</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>80</td>
      <td>0.085917</td>
      <td>0.108055</td>
      <td>0.022137</td>
      <td>0.211153</td>
      <td>0.234764</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Regularized</td>
      <td>72</td>
      <td>0.333188</td>
      <td>0.176645</td>
      <td>-0.156543</td>
      <td>0.426539</td>
      <td>0.278585</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell020_out04_img14.png)

```text
시각화 1 해석:
이 그래프는 log1p(cnt) 회귀에서 Baseline과 Regularized 모델의 validation loss 흐름을 비교한다.
Baseline은 정규화가 없는 기본 DNN이고, Regularized는 L2, BatchNorm, Dropout, EarlyStopping을 모두 적용한 모델이다.
validation loss가 더 낮고 안정적인 모델이 log target 기준 일반화 성능이 더 좋다.
단, 최종 평가는 log 공간이 아니라 원본 cnt 스케일로 복원한 뒤 MAE를 비교해야 한다.
```

![output](assets/3085_problem4_cell020_out06_img15.png)

```text
시각화 2 해석:
Baseline loss curve는 정규화 없는 기본 DNN이 train/validation에서 어떻게 학습되는지 보여준다.
train loss와 validation loss의 차이가 커지면 train set에 더 잘 맞는 generalization gap으로 해석한다.
이후 Regularized 모델이 이 gap과 validation loss를 얼마나 개선하는지 비교한다.
```

![output](assets/3085_problem4_cell020_out08_img16.png)

```text
시각화 3 해석:
Regularized 모델은 L2, BatchNorm, Dropout, EarlyStopping을 함께 적용한 모델이다.
Dropout과 L2는 과도한 parameter 의존을 줄이고, BatchNorm은 hidden activation scale을 안정화한다.
EarlyStopping은 validation loss가 더 이상 개선되지 않으면 학습을 중단하고 best weight를 복원한다.
```

## B3. Test 평가 (역변환 포함) (2점)

**요구사항**:
- 두 모델로 Test 예측
- **log 역변환** 후 *원본 스케일에서* MAE 계산
- 두 모델 MAE 비교 + 개선율 출력

**중요**: log 공간의 MAE는 의미가 약함 → 반드시 역변환 후 평가

```python
print(' === B3. Regression Test 평가: log 역변환 후 원본 스케일 비교 ===')

def inverse_log_count(y_log):
    return np.maximum(0, np.expm1(y_log))

# 실제 y도 원본 cnt 스케일로 복원
y_test_cnt = inverse_log_count(y_test_reg)

baseline_pred_log = reg_baseline_model.predict(X_test_r, verbose=0).reshape(-1)
regularized_pred_log = reg_regularized_model.predict(X_test_r, verbose=0).reshape(-1)

baseline_pred_cnt = inverse_log_count(baseline_pred_log)
regularized_pred_cnt = inverse_log_count(regularized_pred_log)

def regression_original_scale_metrics(model_name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    median_ae = np.median(np.abs(y_true - y_pred))
    p95_ae = np.quantile(np.abs(y_true - y_pred), 0.95)
    
    return {
        'model': model_name,
        'test_mae_original': mae,
        'test_mse_original': mse,
        'test_rmse_original': rmse,
        'test_r2_original': r2,
        'median_abs_error': median_ae,
        'p95_abs_error': p95_ae
    }

reg_test_result_df = pd.DataFrame([
    regression_original_scale_metrics('Baseline', y_test_cnt, baseline_pred_cnt),
    regression_original_scale_metrics('Regularized', y_test_cnt, regularized_pred_cnt)
])

baseline_mae = reg_test_result_df.loc[
    reg_test_result_df['model'] == 'Baseline',
    'test_mae_original'
].iloc[0]

regularized_mae = reg_test_result_df.loc[
    reg_test_result_df['model'] == 'Regularized',
    'test_mae_original'
].iloc[0]

baseline_rmse = reg_test_result_df.loc[
    reg_test_result_df['model'] == 'Baseline',
    'test_rmse_original'
].iloc[0]

regularized_rmse = reg_test_result_df.loc[
    reg_test_result_df['model'] == 'Regularized',
    'test_rmse_original'
].iloc[0]

mae_improve_pct = (baseline_mae - regularized_mae) / baseline_mae * 100
rmse_improve_pct = (baseline_rmse - regularized_rmse) / baseline_rmse * 100

display(reg_test_result_df)

print(f'Baseline Test MAE    : {baseline_mae:.4f}')
print(f'Regularized Test MAE : {regularized_mae:.4f}')
print(f'MAE 개선율           : {mae_improve_pct:.2f}%')
print(f'RMSE 개선율          : {rmse_improve_pct:.2f}%')

print('해석:')
print('회귀 모델은 log1p(cnt)를 학습했지만, 실제 대여량 해석은 원본 cnt 단위에서 해야 한다.')
print('따라서 예측값과 실제값을 expm1으로 복원한 뒤 원본 스케일 MAE/RMSE/R²를 계산했다.')
if mae_improve_pct > 0:
    print('결론: Regularized 모델은 Baseline보다 원본 스케일 MAE를 줄였다.')
else:
    print('결론: Regularized 모델은 Baseline보다 원본 스케일 MAE를 줄이지 못했다.')
```

```text
 === B3. Regression Test 평가: log 역변환 후 원본 스케일 비교 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>test_mae_original</th>
      <th>test_mse_original</th>
      <th>test_rmse_original</th>
      <th>test_r2_original</th>
      <th>median_abs_error</th>
      <th>p95_abs_error</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>32.266636</td>
      <td>2709.543701</td>
      <td>52.053278</td>
      <td>0.919097</td>
      <td>17.541306</td>
      <td>118.431366</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Regularized</td>
      <td>38.041706</td>
      <td>3783.676025</td>
      <td>61.511593</td>
      <td>0.887025</td>
      <td>19.743454</td>
      <td>137.285294</td>
    </tr>
  </tbody>
</table>
</div>

```text
Baseline Test MAE    : 32.2666
Regularized Test MAE : 38.0417
MAE 개선율           : -17.90%
RMSE 개선율          : -18.17%
해석:
회귀 모델은 log1p(cnt)를 학습했지만, 실제 대여량 해석은 원본 cnt 단위에서 해야 한다.
따라서 예측값과 실제값을 expm1으로 복원한 뒤 원본 스케일 MAE/RMSE/R²를 계산했다.
결론: Regularized 모델은 Baseline보다 원본 스케일 MAE를 줄이지 못했다.
```

## B4. 실제 vs 예측 산점도 (1점)

Regularized 모델의 예측값과 실제값을 산점도로 그리고, y=x 기준선 표시.
완벽한 예측이라면 점들이 y=x 선 위에 있어야 함.

```python
print(' === B4. Regularized Regression: Actual vs Predicted / Residual ===')

min_value = min(y_test_cnt.min(), regularized_pred_cnt.min())
max_value = max(y_test_cnt.max(), regularized_pred_cnt.max())

plt.figure(figsize=(6, 6))
plt.scatter(y_test_cnt, regularized_pred_cnt, alpha=0.25, s=10)
plt.plot([min_value, max_value], [min_value, max_value], linestyle='--')
plt.title('Regularized Regression: Actual vs Predicted cnt')
plt.xlabel('Actual cnt')
plt.ylabel('Predicted cnt')
plt.grid(alpha=0.3)
plt.show()

print('시각화 1 해석:')
print('Actual vs Predicted 그래프에서 점들이 y=x 기준선에 가까울수록 예측이 정확하다.')
print('고수요 구간에서 점들이 기준선 아래에 있으면 실제 대여량보다 낮게 예측한 과소예측이다.')
print('Bike Sharing 데이터는 demand peak가 존재하므로 평균 MAE뿐 아니라 고수요 구간 예측도 함께 확인해야 한다.')

regularized_residual = y_test_cnt - regularized_pred_cnt

plt.figure(figsize=(8, 4))
plt.scatter(regularized_pred_cnt, regularized_residual, alpha=0.25, s=10)
plt.axhline(0, linestyle='--')
plt.title('Regularized Regression Residual Plot')
plt.xlabel('Predicted cnt')
plt.ylabel('Residual = Actual - Predicted')
plt.grid(alpha=0.3)
plt.show()

print('시각화 2 해석:')
print('residual이 0 주변에 무작위로 퍼질수록 예측 편향이 작다.')
print('residual이 양수이면 과소예측, 음수이면 과대예측이다.')
print('예측값이 커질수록 residual이 양수로 커지면 고수요 구간을 낮게 예측하는 한계가 남아 있는 것이다.')
```

```text
 === B4. Regularized Regression: Actual vs Predicted / Residual ===
```

![output](assets/3085_problem4_cell024_out01_img17.png)

```text
시각화 1 해석:
Actual vs Predicted 그래프에서 점들이 y=x 기준선에 가까울수록 예측이 정확하다.
고수요 구간에서 점들이 기준선 아래에 있으면 실제 대여량보다 낮게 예측한 과소예측이다.
Bike Sharing 데이터는 demand peak가 존재하므로 평균 MAE뿐 아니라 고수요 구간 예측도 함께 확인해야 한다.
```

![output](assets/3085_problem4_cell024_out03_img18.png)

```text
시각화 2 해석:
residual이 0 주변에 무작위로 퍼질수록 예측 편향이 작다.
residual이 양수이면 과소예측, 음수이면 과대예측이다.
예측값이 커질수록 residual이 양수로 커지면 고수요 구간을 낮게 예측하는 한계가 남아 있는 것이다.
```

---
# Part C. 분류 모델: 3구간 분류 (10점)

## C1. 타겟 binning 

- `cnt`를 3구간(low/mid/high)으로 binning
- 기준: **분위수** (33%, 66% percentile) 사용 → 균등한 클래스 분포
- 클래스 분포 출력

```python
print(' === C1. cnt 분위수 기반 3구간 분류 target 생성 ===')

q33 = np.percentile(y_reg, 33)
q66 = np.percentile(y_reg, 66)

print(f'33% 분위수: {q33}')
print(f'66% 분위수: {q66}')

def to_class(c):
    if c < q33:
        return 0
    elif c < q66:
        return 1
    else:
        return 2

y_cls = np.array([to_class(c) for c in y_reg])

class_distribution = pd.DataFrame({
    'class': [0, 1, 2],
    'label': ['low', 'mid', 'high'],
    'count': [(y_cls == 0).sum(), (y_cls == 1).sum(), (y_cls == 2).sum()],
    'ratio': [(y_cls == 0).mean(), (y_cls == 1).mean(), (y_cls == 2).mean()]
})

display(class_distribution)

plt.figure(figsize=(6, 4))
plt.bar(class_distribution['label'], class_distribution['count'])
plt.title('Class Distribution: low / mid / high')
plt.xlabel('cnt class')
plt.ylabel('count')
plt.grid(axis='y', alpha=0.3)
plt.show()

print('시각화 해석:')
print('cnt를 33%, 66% 분위수 기준으로 low/mid/high 3개 class로 나누었다.')
print('클래스 비율이 거의 1/3씩 유지되므로 다중분류 모델 학습에 적합하다.')
print('이후 train/validation/test split에서는 stratify=y_cls를 사용해 클래스 비율을 유지한다.')
```

```text
 === C1. cnt 분위수 기반 3구간 분류 target 생성 ===
33% 분위수: 69.0
66% 분위수: 221.0
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>class</th>
      <th>label</th>
      <th>count</th>
      <th>ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>low</td>
      <td>5694</td>
      <td>0.327637</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>mid</td>
      <td>5750</td>
      <td>0.330859</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>high</td>
      <td>5935</td>
      <td>0.341504</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell026_out02_img19.png)

```text
시각화 해석:
cnt를 33%, 66% 분위수 기준으로 low/mid/high 3개 class로 나누었다.
클래스 비율이 거의 1/3씩 유지되므로 다중분류 모델 학습에 적합하다.
이후 train/validation/test split에서는 stratify=y_cls를 사용해 클래스 비율을 유지한다.
```

## C2. 데이터 분할 + 분류 모델 (7점)

**요구사항**:
- 같은 feature X 사용 (Part A에서 만든 것)
- 3분할 (60/20/20) + **`stratify=y_cls`** (클래스 비율 유지)
- 별도 StandardScaler 사용 (회귀용과 분리)
- 분류 모델: Regularized (4총사 적용)
- 출력층: `Dense(3, activation='softmax')`
- Loss: `sparse_categorical_crossentropy`, Metric: `accuracy`

```python
print(' === C2. 분류 데이터 분할 + Regularized Classification 모델 학습 ===')

X_temp_c, X_test_c, y_temp_c, y_test_cls = train_test_split(
    X,
    y_cls,
    test_size=0.2,
    random_state=SEED,
    stratify=y_cls
)

X_train_c, X_val_c, y_train_cls, y_val_cls = train_test_split(
    X_temp_c,
    y_temp_c,
    test_size=0.25,
    random_state=SEED,
    stratify=y_temp_c
)

scaler_c = StandardScaler()
X_train_c = scaler_c.fit_transform(X_train_c)
X_val_c = scaler_c.transform(X_val_c)
X_test_c = scaler_c.transform(X_test_c)

print(f'Train: {X_train_c.shape}')
print(f'Val  : {X_val_c.shape}')
print(f'Test : {X_test_c.shape}')

print('\nTrain class distribution:')
print(pd.Series(y_train_cls).value_counts(normalize=True).sort_index())

print('\nVal class distribution:')
print(pd.Series(y_val_cls).value_counts(normalize=True).sort_index())

print('\nTest class distribution:')
print(pd.Series(y_test_cls).value_counts(normalize=True).sort_index())

input_dim_c = X_train_c.shape[1]

def build_classification_regularized():
    model = Sequential()
    
    model.add(Dense(128, kernel_regularizer=l2(0.001), input_shape=(input_dim_c,)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.25))
    
    model.add(Dense(64, kernel_regularizer=l2(0.001)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.25))
    
    model.add(Dense(32, kernel_regularizer=l2(0.001)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.15))
    
    model.add(Dense(3, activation='softmax'))
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

cls_model = build_classification_regularized()

cls_early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

cls_history = cls_model.fit(
    X_train_c,
    y_train_cls,
    validation_data=(X_val_c, y_val_cls),
    epochs=150,
    batch_size=64,
    callbacks=[cls_early_stop],
    verbose=0
)

print(f'실제 학습 epoch 수: {len(cls_history.history["loss"])}')
print(f'Final Train Loss: {cls_history.history["loss"][-1]:.4f}')
print(f'Final Val Loss  : {cls_history.history["val_loss"][-1]:.4f}')
print(f'Final Train Acc : {cls_history.history["accuracy"][-1]:.4f}')
print(f'Final Val Acc   : {cls_history.history["val_accuracy"][-1]:.4f}')

plt.figure(figsize=(9, 4))
plt.plot(cls_history.history['accuracy'], label='Train Accuracy')
plt.plot(cls_history.history['val_accuracy'], label='Val Accuracy')
plt.title('Classification Accuracy Curve')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print('시각화 1 해석:')
print('분류 모델은 cnt를 low/mid/high 3개 구간으로 예측한다.')
print('Train accuracy와 validation accuracy가 함께 상승하면 모델이 수요 구간 분류 구조를 학습하고 있다는 뜻이다.')
print('validation accuracy가 정체되거나 하락하면 과적합 가능성이 있으므로 EarlyStopping으로 best weight를 복원한다.')

plt.figure(figsize=(9, 4))
plt.plot(cls_history.history['loss'], label='Train Loss')
plt.plot(cls_history.history['val_loss'], label='Val Loss')
plt.title('Classification Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('Sparse Categorical Crossentropy')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print('시각화 2 해석:')
print('분류 loss curve는 모델이 class probability distribution을 얼마나 잘 학습하는지 보여준다.')
print('Train loss만 계속 내려가고 validation loss가 올라가면 과적합 신호다.')
print('EarlyStopping은 validation loss 기준으로 best weight를 복원해 일반화 성능을 방어한다.')
```

```text
 === C2. 분류 데이터 분할 + Regularized Classification 모델 학습 ===
```

```text
Train: (10427, 17)
Val  : (3476, 17)
Test : (3476, 17)

Train class distribution:
0    0.327611
1    0.330872
2    0.341517
Name: proportion, dtype: float64

Val class distribution:
0    0.327675
1    0.330840
2    0.341484
Name: proportion, dtype: float64

Test class distribution:
0    0.327675
1    0.330840
2    0.341484
Name: proportion, dtype: float64
```

```text
/home/sieg/projects-wsl/hongikUniv.-26_1/.venv/lib/python3.12/site-packages/keras/src/layers/core/dense.py:107: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
  super().__init__(activity_regularizer=activity_regularizer, **kwargs)
```

```text
실제 학습 epoch 수: 65
Final Train Loss: 0.3723
Final Val Loss  : 0.3485
Final Train Acc : 0.8587
Final Val Acc   : 0.8691
```

![output](assets/3085_problem4_cell028_out04_img20.png)

```text
시각화 1 해석:
분류 모델은 cnt를 low/mid/high 3개 구간으로 예측한다.
Train accuracy와 validation accuracy가 함께 상승하면 모델이 수요 구간 분류 구조를 학습하고 있다는 뜻이다.
validation accuracy가 정체되거나 하락하면 과적합 가능성이 있으므로 EarlyStopping으로 best weight를 복원한다.
```

![output](assets/3085_problem4_cell028_out06_img21.png)

```text
시각화 2 해석:
분류 loss curve는 모델이 class probability distribution을 얼마나 잘 학습하는지 보여준다.
Train loss만 계속 내려가고 validation loss가 올라가면 과적합 신호다.
EarlyStopping은 validation loss 기준으로 best weight를 복원해 일반화 성능을 방어한다.
```

## C3. Test 평가 + 혼동 행렬 (3점)

**요구사항**:
- Test Accuracy 출력
- `classification_report`로 클래스별 성능 출력
- 혼동 행렬을 seaborn heatmap으로 시각화

```python
print(' === C3. Classification Test 평가 ===')

test_cls_loss, test_cls_acc = cls_model.evaluate(X_test_c, y_test_cls, verbose=0)

y_test_cls_prob = cls_model.predict(X_test_c, verbose=0)
y_test_cls_pred = np.argmax(y_test_cls_prob, axis=1)

test_macro_f1 = f1_score(y_test_cls, y_test_cls_pred, average='macro')
test_weighted_f1 = f1_score(y_test_cls, y_test_cls_pred, average='weighted')

print(f'Test Loss       : {test_cls_loss:.4f}')
print(f'Test Accuracy   : {test_cls_acc:.4f}')
print(f'Test Macro-F1   : {test_macro_f1:.4f}')
print(f'Test Weighted-F1: {test_weighted_f1:.4f}')

class_names = ['low', 'mid', 'high']

print('\nClassification Report:')
print(classification_report(y_test_cls, y_test_cls_pred, target_names=class_names))

cm = confusion_matrix(y_test_cls, y_test_cls_pred)

plt.figure(figsize=(6, 5))
plt.imshow(cm)
plt.title('Confusion Matrix: cnt class prediction')
plt.xlabel('Predicted class')
plt.ylabel('True class')
plt.xticks([0, 1, 2], class_names)
plt.yticks([0, 1, 2], class_names)

for i in range(3):
    for j in range(3):
        plt.text(j, i, cm[i, j], ha='center', va='center')

plt.colorbar()
plt.show()

print('시각화 해석:')
print('Confusion matrix는 low/mid/high 수요 구간을 모델이 어떻게 혼동하는지 보여준다.')
print('대각선 값이 클수록 정확히 분류한 것이다.')
print('인접 class로의 오분류는 수요 구간 경계 근처에서 발생할 수 있다.')
print('low를 high로, high를 low로 예측하는 경우는 수요 수준을 크게 잘못 판단한 것이므로 특히 주의해야 한다.')
print('Macro-F1은 각 class를 동일하게 보므로 low/mid/high 성능 균형을 확인하는 데 적합하다.')
```

```text
 === C3. Classification Test 평가 ===
```

```text
Test Loss       : 0.3307
Test Accuracy   : 0.8803
Test Macro-F1   : 0.8811
Test Weighted-F1: 0.8811

Classification Report:
              precision    recall  f1-score   support

         low       0.93      0.91      0.92      1139
         mid       0.80      0.85      0.83      1150
        high       0.91      0.88      0.90      1187

    accuracy                           0.88      3476
   macro avg       0.88      0.88      0.88      3476
weighted avg       0.88      0.88      0.88      3476
```

![output](assets/3085_problem4_cell030_out02_img22.png)

```text
시각화 해석:
Confusion matrix는 low/mid/high 수요 구간을 모델이 어떻게 혼동하는지 보여준다.
대각선 값이 클수록 정확히 분류한 것이다.
인접 class로의 오분류는 수요 구간 경계 근처에서 발생할 수 있다.
low를 high로, high를 low로 예측하는 경우는 수요 수준을 크게 잘못 판단한 것이므로 특히 주의해야 한다.
Macro-F1은 각 class를 동일하게 보므로 low/mid/high 성능 균형을 확인하는 데 적합하다.
```

---
# Part D. 회귀 vs 분류 결과 비교 분석 (5점)

## D1. 두 접근법 비교 (2점)

**요구사항**:
- 회귀 모델의 예측값을 *같은 binning 기준*으로 변환해 분류 정확도 계산
- 직접 분류 모델의 정확도와 비교
- 둘 중 어느 쪽이 더 좋았는지 마크다운으로 분석

```python
print(' === D1. 회귀 + 분류 최종 성능 요약 ===')

reg_summary = reg_test_result_df.copy()
reg_summary['mae_improvement_pct_vs_baseline'] = np.nan
reg_summary.loc[
    reg_summary['model'] == 'Regularized',
    'mae_improvement_pct_vs_baseline'
] = mae_improve_pct

display(reg_summary)

cls_summary = pd.DataFrame([{
    'model': 'Regularized Classification',
    'test_loss': test_cls_loss,
    'test_accuracy': test_cls_acc,
    'test_macro_f1': test_macro_f1,
    'test_weighted_f1': test_weighted_f1,
    'target_design': 'cnt quantile bins: low/mid/high'
}])

display(cls_summary)

print('해석:')
print('Part B 회귀는 cnt를 연속값으로 예측하므로 원본 스케일 MAE/RMSE/R²를 중심으로 평가한다.')
print('Part C 분류는 cnt를 low/mid/high 구간으로 예측하므로 accuracy와 macro-F1을 함께 본다.')
print('회귀는 정확한 수량 예측에 유리하고, 분류는 수요 수준을 낮음/중간/높음으로 판단하는 데 유리하다.')
```

```text
 === D1. 회귀 + 분류 최종 성능 요약 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>test_mae_original</th>
      <th>test_mse_original</th>
      <th>test_rmse_original</th>
      <th>test_r2_original</th>
      <th>median_abs_error</th>
      <th>p95_abs_error</th>
      <th>mae_improvement_pct_vs_baseline</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>32.266636</td>
      <td>2709.543701</td>
      <td>52.053278</td>
      <td>0.919097</td>
      <td>17.541306</td>
      <td>118.431366</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Regularized</td>
      <td>38.041706</td>
      <td>3783.676025</td>
      <td>61.511593</td>
      <td>0.887025</td>
      <td>19.743454</td>
      <td>137.285294</td>
      <td>-17.897962</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>model</th>
      <th>test_loss</th>
      <th>test_accuracy</th>
      <th>test_macro_f1</th>
      <th>test_weighted_f1</th>
      <th>target_design</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Regularized Classification</td>
      <td>0.330658</td>
      <td>0.880322</td>
      <td>0.881089</td>
      <td>0.881116</td>
      <td>cnt quantile bins: low/mid/high</td>
    </tr>
  </tbody>
</table>
</div>

```text
해석:
Part B 회귀는 cnt를 연속값으로 예측하므로 원본 스케일 MAE/RMSE/R²를 중심으로 평가한다.
Part C 분류는 cnt를 low/mid/high 구간으로 예측하므로 accuracy와 macro-F1을 함께 본다.
회귀는 정확한 수량 예측에 유리하고, 분류는 수요 수준을 낮음/중간/높음으로 판단하는 데 유리하다.
```

**비교 분석** :

Part B 회귀는 cnt를 연속값으로 예측하므로 원본 스케일 MAE/RMSE/R²를 중심으로 평가한다.
Part C 분류는 cnt를 low/mid/high 구간으로 예측하므로 accuracy와 macro-F1을 함께 본다.
회귀는 정확한 수량 예측에 유리하고, 분류는 수요 수준을 낮음/중간/높음으로 판단하는 데 유리하다.

## D2. Feature Importance 추정 (2점)

**요구사항**:
- 회귀 모델의 첫 번째 Dense 층의 가중치 추출
- 각 feature의 *평균 절대 가중치*를 계산
- 상위 10개 feature를 막대 그래프로 시각화
- 어떤 feature가 가장 중요한지 마크다운으로 분석 (1-2줄)

```python
print(' === D2. Feature Importance 추정: 첫 Dense layer 평균 절대 가중치 ===')

first_dense_layer = None
for layer in reg_regularized_model.layers:
    if isinstance(layer, Dense):
        first_dense_layer = layer
        break

if first_dense_layer is None:
    raise ValueError('회귀 모델에서 Dense layer를 찾지 못했습니다.')

first_kernel = first_dense_layer.get_weights()[0]

feature_importance_df = pd.DataFrame({
    'feature': df_encoded.columns.tolist(),
    'mean_abs_weight': np.mean(np.abs(first_kernel), axis=1),
}).sort_values('mean_abs_weight', ascending=False).reset_index(drop=True)

feature_importance_top10 = feature_importance_df.head(10).copy()

display(feature_importance_top10)

plt.figure(figsize=(9, 5))
plot_df = feature_importance_top10.sort_values('mean_abs_weight')
plt.barh(plot_df['feature'], plot_df['mean_abs_weight'])
plt.title('Top 10 Feature Importance from First Dense Layer')
plt.xlabel('Mean absolute input weight')
plt.ylabel('Feature')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

top_feature = feature_importance_top10.iloc[0]['feature']
top_weight = feature_importance_top10.iloc[0]['mean_abs_weight']
top3_features = feature_importance_top10['feature'].head(3).tolist()

print('해석:')
print(f'첫 Dense layer의 평균 절대 가중치 기준 가장 큰 feature는 {top_feature}이며, 값은 {top_weight:.4f}이다.')
print(f'상위 3개 feature는 {top3_features}이다.')
print('이 방식은 신경망 내부 weight 기반의 단순 중요도 추정이므로 인과 효과나 permutation importance와 동일하게 해석하면 안 된다.')
print('그래도 입력층에서 모델이 어떤 feature 축에 상대적으로 큰 weight를 부여했는지 확인하는 제출 요구사항에는 부합한다.')

print('\n === D2-보강. 수요 구간별 회귀 오류 분석 ===')


reg_eval_compare = pd.DataFrame({
    'y_true_cnt': y_test_cnt,
    'baseline_pred_cnt': baseline_pred_cnt,
    'regularized_pred_cnt': regularized_pred_cnt
})

reg_eval_compare['baseline_residual'] = reg_eval_compare['y_true_cnt'] - reg_eval_compare['baseline_pred_cnt']
reg_eval_compare['regularized_residual'] = reg_eval_compare['y_true_cnt'] - reg_eval_compare['regularized_pred_cnt']
reg_eval_compare['baseline_abs_error'] = np.abs(reg_eval_compare['baseline_residual'])
reg_eval_compare['regularized_abs_error'] = np.abs(reg_eval_compare['regularized_residual'])

def cnt_bin_from_quantile(c):
    if c < q33:
        return 'low'
    elif c < q66:
        return 'mid'
    else:
        return 'high'

reg_eval_compare['cnt_bin'] = reg_eval_compare['y_true_cnt'].apply(cnt_bin_from_quantile)

bin_order = ['low', 'mid', 'high']
reg_eval_compare['cnt_bin'] = pd.Categorical(
    reg_eval_compare['cnt_bin'],
    categories=bin_order,
    ordered=True
)

bin_error_rows = []

for bin_name, group in reg_eval_compare.groupby('cnt_bin', observed=False):
    baseline_mae_bin = group['baseline_abs_error'].mean()
    regularized_mae_bin = group['regularized_abs_error'].mean()
    improve_pct_bin = (baseline_mae_bin - regularized_mae_bin) / baseline_mae_bin * 100
    
    bin_error_rows.append({
        'cnt_bin': bin_name,
        'count': len(group),
        'y_true_mean': group['y_true_cnt'].mean(),
        'baseline_mae': baseline_mae_bin,
        'regularized_mae': regularized_mae_bin,
        'mae_improvement_pct': improve_pct_bin,
        'baseline_mean_residual': group['baseline_residual'].mean(),
        'regularized_mean_residual': group['regularized_residual'].mean()
    })

reg_bin_error_df = pd.DataFrame(bin_error_rows)
display(reg_bin_error_df)

x = np.arange(len(bin_order))
width = 0.36

plt.figure(figsize=(8, 4))
plt.bar(x - width / 2, reg_bin_error_df['baseline_mae'], width=width, label='Baseline')
plt.bar(x + width / 2, reg_bin_error_df['regularized_mae'], width=width, label='Regularized')
plt.xticks(x, bin_order)
plt.title('Regression MAE by cnt Demand Bin')
plt.xlabel('cnt bin')
plt.ylabel('MAE original scale')
plt.legend()
plt.grid(axis='y', alpha=0.3)

for i, v in enumerate(reg_bin_error_df['mae_improvement_pct']):
    y_top = max(reg_bin_error_df.loc[i, 'baseline_mae'], reg_bin_error_df.loc[i, 'regularized_mae'])
    plt.text(i, y_top, f'{v:+.1f}%', ha='center', va='bottom', fontsize=9)

plt.show()

print('시각화 1 해석:')
print('수요 구간별 MAE는 모델이 low/mid/high 중 어느 수요 구간에서 더 잘 맞는지 보여준다.')
print('전체 MAE가 개선되어도 high demand 구간에서 오차가 크면 운영 관점에서는 중요한 한계가 남는다.')
print('막대 위 개선율이 양수이면 해당 구간에서 Regularized 모델이 Baseline보다 개선된 것이다.')

plt.figure(figsize=(8, 4))
plt.plot(reg_bin_error_df['cnt_bin'], reg_bin_error_df['baseline_mean_residual'], marker='o', label='Baseline')
plt.plot(reg_bin_error_df['cnt_bin'], reg_bin_error_df['regularized_mean_residual'], marker='o', label='Regularized')
plt.axhline(0, linestyle='--')
plt.title('Mean Residual by cnt Demand Bin')
plt.xlabel('cnt bin')
plt.ylabel('Mean residual = Actual - Predicted')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print('시각화 2 해석:')
print('mean residual이 양수이면 실제 수요보다 낮게 예측한 과소예측이다.')
print('mean residual이 음수이면 실제 수요보다 높게 예측한 과대예측이다.')
print('high bin에서 residual이 양수로 크면 모델이 peak demand를 충분히 따라가지 못한다는 뜻이다.')
print('이 분석은 회귀 모델이 평균적으로 좋은지뿐 아니라, 고수요 운영 상황에서 쓸 만한지 판단하는 데 필요하다.')
```

```text
 === D2. Feature Importance 추정: 첫 Dense layer 평균 절대 가중치 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>feature</th>
      <th>mean_abs_weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>hr</td>
      <td>0.153635</td>
    </tr>
    <tr>
      <th>1</th>
      <td>time_group_night</td>
      <td>0.075680</td>
    </tr>
    <tr>
      <th>2</th>
      <td>time_group_daytime</td>
      <td>0.073424</td>
    </tr>
    <tr>
      <th>3</th>
      <td>time_group_evening_rush</td>
      <td>0.072185</td>
    </tr>
    <tr>
      <th>4</th>
      <td>workingday</td>
      <td>0.062049</td>
    </tr>
    <tr>
      <th>5</th>
      <td>time_group_morning_rush</td>
      <td>0.058511</td>
    </tr>
    <tr>
      <th>6</th>
      <td>is_weekend</td>
      <td>0.056130</td>
    </tr>
    <tr>
      <th>7</th>
      <td>mnth</td>
      <td>0.047974</td>
    </tr>
    <tr>
      <th>8</th>
      <td>season</td>
      <td>0.047957</td>
    </tr>
    <tr>
      <th>9</th>
      <td>temp</td>
      <td>0.047407</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell035_out02_img23.png)

```text
해석:
첫 Dense layer의 평균 절대 가중치 기준 가장 큰 feature는 hr이며, 값은 0.1536이다.
상위 3개 feature는 ['hr', 'time_group_night', 'time_group_daytime']이다.
이 방식은 신경망 내부 weight 기반의 단순 중요도 추정이므로 인과 효과나 permutation importance와 동일하게 해석하면 안 된다.
그래도 입력층에서 모델이 어떤 feature 축에 상대적으로 큰 weight를 부여했는지 확인하는 제출 요구사항에는 부합한다.

 === D2-보강. 수요 구간별 회귀 오류 분석 ===
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cnt_bin</th>
      <th>count</th>
      <th>y_true_mean</th>
      <th>baseline_mae</th>
      <th>regularized_mae</th>
      <th>mae_improvement_pct</th>
      <th>baseline_mean_residual</th>
      <th>regularized_mean_residual</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>low</td>
      <td>1133</td>
      <td>24.455427</td>
      <td>9.247062</td>
      <td>10.216297</td>
      <td>-10.481550</td>
      <td>-5.280204</td>
      <td>-3.826363</td>
    </tr>
    <tr>
      <th>1</th>
      <td>mid</td>
      <td>1158</td>
      <td>141.152847</td>
      <td>27.949003</td>
      <td>32.065536</td>
      <td>-14.728731</td>
      <td>-7.372068</td>
      <td>-8.455404</td>
    </tr>
    <tr>
      <th>2</th>
      <td>high</td>
      <td>1185</td>
      <td>396.952728</td>
      <td>58.495319</td>
      <td>70.486076</td>
      <td>-20.498661</td>
      <td>20.346928</td>
      <td>40.764473</td>
    </tr>
  </tbody>
</table>
</div>

![output](assets/3085_problem4_cell035_out05_img24.png)

```text
시각화 1 해석:
수요 구간별 MAE는 모델이 low/mid/high 중 어느 수요 구간에서 더 잘 맞는지 보여준다.
전체 MAE가 개선되어도 high demand 구간에서 오차가 크면 운영 관점에서는 중요한 한계가 남는다.
막대 위 개선율이 양수이면 해당 구간에서 Regularized 모델이 Baseline보다 개선된 것이다.
```

![output](assets/3085_problem4_cell035_out07_img25.png)

```text
시각화 2 해석:
mean residual이 양수이면 실제 수요보다 낮게 예측한 과소예측이다.
mean residual이 음수이면 실제 수요보다 높게 예측한 과대예측이다.
high bin에서 residual이 양수로 크면 모델이 peak demand를 충분히 따라가지 못한다는 뜻이다.
이 분석은 회귀 모델이 평균적으로 좋은지뿐 아니라, 고수요 운영 상황에서 쓸 만한지 판단하는 데 필요하다.
```

```python
print(' === D3. 최종 모델링 결론 ===')

print('[EDA 결론]')
print('Bike Sharing 데이터는 시간별 도시 자전거 대여 수요 예측 문제다.')
print('cnt는 오른쪽 꼬리가 있는 count target이며, 특정 시간대와 조건에서 demand peak가 발생한다.')
print('귀무가설 검정과 시각화 결과, 시간대/근무일 구조, 날씨·쾌적성, 계절·연도 효과는 모두 cnt와 관련된다.')
print('따라서 최종 feature set은 시간 변수, 계절 변수, 날씨 변수, time_group, is_weekend를 포함하고, leakage 컬럼은 제외했다.')

print('\n[회귀 결론]')
print('Part B에서는 log1p(cnt)를 target으로 사용해 long-tail 영향을 완화했다.')
print('최종 평가는 expm1으로 원본 스케일을 복원한 뒤 MAE/RMSE/R²를 계산했다.')
print(f'Baseline Test MAE는 {baseline_mae:.4f}, Regularized Test MAE는 {regularized_mae:.4f}이다.')
print(f'Regularized 모델의 원본 스케일 MAE 개선율은 {mae_improve_pct:.2f}%이다.')
print(f'Regularized 모델의 원본 스케일 RMSE 개선율은 {rmse_improve_pct:.2f}%이다.')

if mae_improve_pct > 0:
    print('따라서 Regularized 회귀 모델은 Baseline 대비 평균 절대오차를 줄였다.')
else:
    print('따라서 Regularized 회귀 모델은 Baseline 대비 평균 절대오차를 줄이지 못했다.')

high_bin_row = reg_bin_error_df[reg_bin_error_df['cnt_bin'] == 'high'].iloc[0]
print(f'high demand 구간 MAE 개선율은 {high_bin_row["mae_improvement_pct"]:.2f}%이다.')

if high_bin_row['regularized_mean_residual'] > 0:
    print('high demand 구간에서는 residual mean이 양수이므로, 고수요 시간대를 낮게 예측하는 경향이 남아 있다.')
else:
    print('high demand 구간에서는 residual mean이 0 이하이므로, 고수요 과소예측 편향은 크지 않다.')

print('\n[분류 결론]')
print('Part C에서는 cnt를 33%, 66% 분위수 기준으로 low/mid/high 3개 class로 나누었다.')
print('stratify split으로 클래스 비율을 유지했고, softmax 출력층과 sparse categorical crossentropy를 사용했다.')
print(f'Classification Test Accuracy는 {test_cls_acc:.4f}, Macro-F1은 {test_macro_f1:.4f}이다.')
print('Accuracy는 전체 정답률을 보여주고, Macro-F1은 low/mid/high 각 class의 균형 성능을 보여준다.')

print('\n[최종 판단]')
print('이 문제에서 가장 중요한 feature 축은 hr, workingday, time_group으로 대표되는 시간 수요 구조다.')
top_feature_text = ', '.join(feature_importance_top10['feature'].head(3).tolist())
print(f'D2 첫 Dense layer 평균 절대 가중치 기준 상위 feature는 {top_feature_text}이다.')
print('날씨 변수는 수요의 쾌적성 조건을 설명하고, season/mnth/yr는 장기 계절성과 성장 효과를 설명한다.')
print('casual과 registered는 cnt의 직접 구성요소이므로 feature에서 제외하여 data leakage를 방지했다.')
print('최종적으로 회귀 모델은 수량 예측, 분류 모델은 수요 수준 판단에 사용될 수 있다.')
print('추가 개선 방향은 hr×workingday interaction, cyclical hour encoding, 고수요 구간 sample weighting, 시간순 split 검증이다.')
```

```text
 === D3. 최종 모델링 결론 ===
[EDA 결론]
Bike Sharing 데이터는 시간별 도시 자전거 대여 수요 예측 문제다.
cnt는 오른쪽 꼬리가 있는 count target이며, 특정 시간대와 조건에서 demand peak가 발생한다.
귀무가설 검정과 시각화 결과, 시간대/근무일 구조, 날씨·쾌적성, 계절·연도 효과는 모두 cnt와 관련된다.
따라서 최종 feature set은 시간 변수, 계절 변수, 날씨 변수, time_group, is_weekend를 포함하고, leakage 컬럼은 제외했다.

[회귀 결론]
Part B에서는 log1p(cnt)를 target으로 사용해 long-tail 영향을 완화했다.
최종 평가는 expm1으로 원본 스케일을 복원한 뒤 MAE/RMSE/R²를 계산했다.
Baseline Test MAE는 32.2666, Regularized Test MAE는 38.0417이다.
Regularized 모델의 원본 스케일 MAE 개선율은 -17.90%이다.
Regularized 모델의 원본 스케일 RMSE 개선율은 -18.17%이다.
따라서 Regularized 회귀 모델은 Baseline 대비 평균 절대오차를 줄이지 못했다.
high demand 구간 MAE 개선율은 -20.50%이다.
high demand 구간에서는 residual mean이 양수이므로, 고수요 시간대를 낮게 예측하는 경향이 남아 있다.

[분류 결론]
Part C에서는 cnt를 33%, 66% 분위수 기준으로 low/mid/high 3개 class로 나누었다.
stratify split으로 클래스 비율을 유지했고, softmax 출력층과 sparse categorical crossentropy를 사용했다.
Classification Test Accuracy는 0.8803, Macro-F1은 0.8811이다.
Accuracy는 전체 정답률을 보여주고, Macro-F1은 low/mid/high 각 class의 균형 성능을 보여준다.

[최종 판단]
이 문제에서 가장 중요한 feature 축은 hr, workingday, time_group으로 대표되는 시간 수요 구조다.
D2 첫 Dense layer 평균 절대 가중치 기준 상위 feature는 hr, time_group_night, time_group_daytime이다.
날씨 변수는 수요의 쾌적성 조건을 설명하고, season/mnth/yr는 장기 계절성과 성장 효과를 설명한다.
casual과 registered는 cnt의 직접 구성요소이므로 feature에서 제외하여 data leakage를 방지했다.
최종적으로 회귀 모델은 수량 예측, 분류 모델은 수요 수준 판단에 사용될 수 있다.
추가 개선 방향은 hr×workingday interaction, cyclical hour encoding, 고수요 구간 sample weighting, 시간순 split 검증이다.
```

## D3. `cnt` 분포가 long-tail인 이유와 log 변환의 효과 (1점)

**답**:

cnt 분포가 long-tail인 이유는 자전거 대여 수요가 모든 시간대에 균등하게 발생하지 않기 때문이다. 

대부분의 시간대에는 대여량이 낮거나 중간 수준이지만, 출근 시간대, 퇴근 시간대, 좋은 날씨, 특정 계절처럼 수요가 몰리는 조건에서는 cnt가 크게 증가한다. 

실제로 cnt의 평균은 189.46이고 중앙값은 142로 평균이 중앙값보다 크며, 최대값은 977까지 나타난다. 또한 원본 skewness가 1.28로 양의 왜도를 가지므로, 오른쪽 꼬리가 긴 분포라고 해석할 수 있다.

---

# ✅ 제출 전 체크리스트

- [ ] STUDENT_ID에 본인 학번을 정확히 입력했나?
- [ ] casual/registered를 feature에서 제외했나?
- [ ] 회귀에서 log 변환 → 역변환을 정확히 적용했나?
- [ ] 분류에서 stratify=y_cls를 사용했나?
- [ ] 모든 셀이 실행 가능한가?
- [ ] 분석 질문(A2, D1, D2, D3)에 답을 작성했나?
- [ ] 파일명을 `[본인학번]_problem4.ipynb`로 저장했나?

**제출**: LMS에 업로드

---
