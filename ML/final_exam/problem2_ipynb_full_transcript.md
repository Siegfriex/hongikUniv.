# Full IPYNB Transcript: problem2 (1).ipynb

- Source notebook: `ML/final_exam/problem2 (1).ipynb`
- Cell count: 43
- 방식: notebook cell 순서대로 Markdown/code/output text를 전사. 이미지 바이너리는 Markdown에 직접 삽입하지 않고 표시만 남김.

---

## Cell 0 - markdown

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

---

## Cell 1 - markdown

## ⚠️ 학번 입력 (필수)

다음 셀의 `STUDENT_ID` 변수에 본인 학번을 입력하세요.
**입력하지 않으면 0점 처리됩니다.**

---

## Cell 2 - code

Execution count: `89`

```python
STUDENT_ID = "3085"   # ← 본인 학번 마지막 4자리로 변경
SEED = int(STUDENT_ID)

assert STUDENT_ID != "0000", "학번을 입력하세요!"
print(f'학번(끝4자리): {STUDENT_ID}, SEED: {SEED}')
```

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
학번(끝4자리): 3085, SEED: 3085
```

---

## Cell 3 - markdown

## 환경 준비

필요한 라이브러리를 import하고 seed를 고정.

**요구사항**:
- numpy, pandas, matplotlib
- tensorflow, keras
- sklearn (train_test_split, StandardScaler)
- numpy와 tensorflow 모두 SEED로 고정

---

## Cell 4 - code

Execution count: `90`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
Keras  : 3.14.1 | backend: tensorflow
pandas : 3.0.2
```

---

## Cell 5 - markdown

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

---

## Cell 6 - code

Execution count: `91`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

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

#### Output 1 - display_data

```text
   No  year  month  day  hour  pm2.5  DEWP  TEMP    PRES cbwd    Iws  Is  Ir
0   1  2010      1    1     0    NaN   -21 -11.0  1021.0   NW   1.79   0   0
1   2  2010      1    1     1    NaN   -21 -12.0  1020.0   NW   4.92   0   0
2   3  2010      1    1     2    NaN   -21 -11.0  1019.0   NW   6.71   0   0
3   4  2010      1    1     3    NaN   -21 -14.0  1019.0   NW   9.84   0   0
4   5  2010      1    1     4    NaN   -20 -12.0  1018.0   NW  12.97   0   0
```

#### Output 2 - stream

Stream: `stdout`

```text
 === 1단계 : 컬럼 역할 1차 정리 ===
```

#### Output 3 - display_data

```text
<IPython.core.display.HTML object>
```

---

## Cell 7 - markdown

**결측치 처리 **

---

## Cell 8 - code

Execution count: `92`

```python
# 결측치 처리: pm2.5의 결측치는 시간 연속성을 활용한 forward fill로 채움
# (시간 연속 데이터이므로 직전 시간 값으로 채우는 것이 합리적)
# 대안: dropna() — 2067개(약 4.7%)이므로 제거도 가능

df_clean = df.copy()
df_clean['pm2.5'] = df_clean['pm2.5'].ffill().bfill()   # 시간 연속성 활용 (pandas 3.x 호환)

print(f'결측치 처리 후: {df_clean.isnull().sum().sum()}')
print(f'Shape: {df_clean.shape}')
```

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
결측치 처리 후: 0
Shape: (43824, 13)
```

---

## Cell 9 - markdown

## A2. 범주형 변수 인코딩

`cbwd` (풍향) 컬럼을 인코딩

---

## Cell 10 - code

Execution count: `93`

```python
print('cbwd 고유값:', df_clean['cbwd'].unique())
print('cbwd 분포:')
print(df_clean['cbwd'].value_counts())

# One-Hot 인코딩
df_clean = pd.get_dummies(df_clean, columns=['cbwd'], dtype=int)
print('\nOne-Hot 인코딩 후 컬럼:')
print([c for c in df_clean.columns if 'cbwd' in c])
```

### Outputs

#### Output 0 - stream

Stream: `stdout`

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

---

## Cell 11 - markdown

## A3. 시간 변수 처리

데이터에 이미 `year/month/day/hour` 컬럼이 있음. 요일, 주말 여부, 계절 등을 Feature로 생성

---

## Cell 12 - code

Execution count: `94`

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

### Outputs

#### Output 0 - display_data

```text
'최종 컬럼:'
```

#### Output 1 - display_data

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

#### Output 2 - stream

Stream: `stdout`

```text
Shape: (43824, 17)
```

---

## Cell 13 - markdown

## A4. Train/Val/Test 3분할 + 정규화

- 60% / 20% / 20% 비율로 3분할
- **반드시 `random_state=SEED`** 사용 (본인 학번 기반)
- StandardScaler로 정규화 (train에 fit, val/test는 transform만)

**출력**:
- X_train, X_val, X_test의 shape

---

## Cell 14 - code

Execution count: `95`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
X: (43824, 16), y: (43824,)
타겟 분포: min=0.0, max=994.0, mean=97.8

Train: (26294, 16) (60%)
Val  : (8765, 16) (20%)
Test : (8765, 16) (20%)

정규화 완료
```

---

## Cell 15 - markdown

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

---

## Cell 16 - code

Execution count: `96`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
 === 2단계 : Train 데이터 기준 Target 중심 EDA 가설 설정 ===
target: pm2.5
numeric_features: ['DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir']
time_features: ['year', 'month', 'day', 'hour', 'dayofweek', 'is_weekend']
wind_dummy_features: ['cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']
```

---

## Cell 17 - code

Execution count: `97`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
target: pm2.5
numeric_weather_features: ['DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir']
time_numeric_features: ['year', 'month', 'day', 'hour', 'dayofweek']
binary_features: ['cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv', 'is_weekend']
all_numeric_for_corr: ['year', 'month', 'day', 'hour', 'DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir', 'dayofweek']

결측치 총 개수: 0
shape: (43824, 19)
```

#### Output 1 - display_data

```text
   No  year  month  day  hour  pm2.5  DEWP  TEMP    PRES    Iws  Is  Ir  \
0   1  2010      1    1     0  129.0   -21 -11.0  1021.0   1.79   0   0   
1   2  2010      1    1     1  129.0   -21 -12.0  1020.0   4.92   0   0   
2   3  2010      1    1     2  129.0   -21 -11.0  1019.0   6.71   0   0   
3   4  2010      1    1     3  129.0   -21 -14.0  1019.0   9.84   0   0   
4   5  2010      1    1     4  129.0   -20 -12.0  1018.0  12.97   0   0   

   cbwd_NE  cbwd_NW  cbwd_SE  cbwd_cv            datetime  dayofweek  \
0        0        1        0        0 2010-01-01 00:00:00          4   
1        0        1        0        0 2010-01-01 01:00:00          4   
2        0        1        0        0 2010-01-01 02:00:00          4   
3        0        1        0        0 2010-01-01 03:00:00          4   
4        0        1        0        0 2010-01-01 04:00:00          4   

   is_weekend  
0           0  
1           0  
2           0  
3           0  
4           0
```

#### Output 2 - display_data

```text
          No  year  month  day  hour  pm2.5  DEWP  TEMP    PRES     Iws  Is  \
43819  43820  2014     12   31    19    8.0   -23  -2.0  1034.0  231.97   0   
43820  43821  2014     12   31    20   10.0   -22  -3.0  1034.0  237.78   0   
43821  43822  2014     12   31    21   10.0   -22  -3.0  1034.0  242.70   0   
43822  43823  2014     12   31    22    8.0   -22  -4.0  1034.0  246.72   0   
43823  43824  2014     12   31    23   12.0   -21  -3.0  1034.0  249.85   0   

       Ir  cbwd_NE  cbwd_NW  cbwd_SE  cbwd_cv            datetime  dayofweek  \
43819   0        0        1        0        0 2014-12-31 19:00:00          2   
43820   0        0        1        0        0 2014-12-31 20:00:00          2   
43821   0        0        1        0        0 2014-12-31 21:00:00          2   
43822   0        0        1        0        0 2014-12-31 22:00:00          2   
43823   0        0        1        0        0 2014-12-31 23:00:00          2   

       is_weekend  
43819           0  
43820           0  
43821           0  
43822           0  
43823           0
```

#### Output 3 - display_data

```text
'cbwd_NE 날씨비율 : 0.1140 (11.40%)'
```

#### Output 4 - display_data

```text
'cbwd_NW 날씨비율 : 0.3229 (32.29%)'
```

#### Output 5 - display_data

```text
'cbwd_SE 날씨비율 : 0.3489 (34.89%)'
```

#### Output 6 - display_data

```text
'cbwd_cv 날씨비율 : 0.2142 (21.42%)'
```

---

## Cell 18 - code

Execution count: `98`

```python
print(' === B0-1. Train/Test 시간순 Split ===')
df_eda = df_clean.copy()
#시간 순서 정렬 : 과거데이터(2010-2013)을 바탕으로 미래데이터(test. 2014를 예측한다)
df_eda = df_eda.sort_values(['year', 'month', 'day', 'hour']).reset_index(drop=True)

train_df = df_eda[df_eda['year'] <= 2013].copy()
test_df = df_eda[df_eda['year'] == 2014].copy()

# train_size = int(len(df_eda) * 0.8) #비율은 안정, 단 확실하게 하기 위해 세부 연도별 분할

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

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

---

## Cell 19 - code

Execution count: `99`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
== 2-1 단계 : Target(pm2.5) 분포 확인 ===
= RQ0. pm2.5는 정규분포에 가까운가, 아니면 고농도 outlier가 많은 분포인가? =
```

#### Output 1 - display_data

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

#### Output 2 - stream

Stream: `stdout`

```text
skewness: 1.8345
kurtosis: 5.3810
```

#### Output 3 - display_data

```text
<Figure size 800x400 with 1 Axes>
```

#### Output 4 - display_data

```text
<Figure size 800x400 with 1 Axes>
```

#### Output 5 - stream

Stream: `stdout`

```text
해석:
pm2.5는 평균이 중앙값보다 크고, skewness가 1.83으로 양의 왜도가 크다.
또한 75% 값은 137이지만 95%는 279, 99%는 417, 최대값은 994로 오른쪽 꼬리가 길다.
따라서 pm2.5는 정규분포라기보다 고농도 outlier가 많은 -즉, 특정 시간대나 계절·기상 조건에서 고농도 episode가 발생하는 데이터이다.
모델링에서는 MSE만 보면 고농도 오차에 크게 끌릴 수 있으므로 MAE, RMSE, log1p 변환, 고농도 여부 분류 등을 함께 고려할 필요가 있다.
=== 이때, outlier는 단순 오류라기보다 실제 대기오염 고농도 사건일 수 있다. 따라서 무조건 제거하면 안 된다. 이 데이터에서는 고농도 구간 자체가 중요한 예측 대상으로 판단될 수 있다.
```

---

## Cell 20 - code

Execution count: `106`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
=== 연속형 기상 feature ↔ 연속형 target ===
```

#### Output 1 - display_data

```text
  feature          variable_type                test pearson_direction  \
3     Iws  continuous-continuous  Pearson / Spearman          negative   
0    DEWP  continuous-continuous  Pearson / Spearman          positive   
2    PRES  continuous-continuous  Pearson / Spearman          negative   
1    TEMP  continuous-continuous  Pearson / Spearman          negative   
4      Is  continuous-continuous  Pearson / Spearman          positive   
5      Ir  continuous-continuous  Pearson / Spearman          negative   

  pearson_decision_0.05  pearson_corr  pearson_p_value  spearman_corr  \
3             reject H0     -0.249642     0.000000e+00      -0.358043   
0             reject H0      0.201941    2.142763e-319       0.331976   
2             reject H0     -0.092107     6.270519e-67      -0.189042   
1             reject H0     -0.044800     4.743388e-17       0.064146   
4             reject H0      0.023158     1.444966e-05       0.046936   
5             reject H0     -0.048251     1.563929e-19       0.006044   

   spearman_p_value  abs_pearson  abs_spearman                        H0  \
3      0.000000e+00     0.249642      0.358043   Iws과 target 사이의 관계는 없다.   
0      0.000000e+00     0.201941      0.331976  DEWP과 target 사이의 관계는 없다.   
2     1.933085e-279     0.092107      0.189042  PRES과 target 사이의 관계는 없다.   
1      2.675477e-33     0.044800      0.064146  TEMP과 target 사이의 관계는 없다.   
4      1.449028e-18     0.023158      0.046936    Is과 target 사이의 관계는 없다.   
5      2.577713e-01     0.048251      0.006044    Ir과 target 사이의 관계는 없다.   

                         H1  
3   Iws과 target 사이의 관계는 있다.  
0  DEWP과 target 사이의 관계는 있다.  
2  PRES과 target 사이의 관계는 있다.  
1  TEMP과 target 사이의 관계는 있다.  
4    Is과 target 사이의 관계는 있다.  
5    Ir과 target 사이의 관계는 있다.
```

#### Output 2 - stream

Stream: `stdout`

```text
 === 시각화 1: 상관계수 bar plot. ===
```

#### Output 3 - display_data

```text
<Figure size 800x400 with 1 Axes>
```

#### Output 4 - stream

Stream: `stdout`

```text
 === 2: 연속형 feature별 scatter plot ===
```

#### Output 5 - display_data

```text
<Figure size 600x400 with 1 Axes>
```

#### Output 6 - display_data

```text
<Figure size 600x400 with 1 Axes>
```

#### Output 7 - display_data

```text
<Figure size 600x400 with 1 Axes>
```

#### Output 8 - display_data

```text
<Figure size 600x400 with 1 Axes>
```

#### Output 9 - display_data

```text
<Figure size 600x400 with 1 Axes>
```

#### Output 10 - display_data

```text
<Figure size 600x400 with 1 Axes>
```

#### Output 11 - stream

Stream: `stdout`

```text
해석:
Iws는 pm2.5와 가장 강한 음의 상관을 보인다. 누적 풍속이 커질수록 PM2.5가 낮아지는 경향이 있다.
DEWP는 pm2.5와 비교적 뚜렷한 양의 상관을 보인다. 이슬점이 높을수록 PM2.5가 높아지는 경향이 있다.
PRES는 약한 음의 상관을 보인다.
TEMP는 Pearson과 Spearman의 방향이 달라 단순 선형 관계로 해석하기 어렵다.
Is와 Ir는 통계적으로 유의하거나 일부 유의하더라도 상관 강도가 매우 약하므로 주요 feature로 보기는 어렵다.
대규모 데이터에서는 p-value보다 correlation의 절대값과 시각적 패턴을 함께 해석해야 한다.
```

---

## Cell 21 - markdown

| feature | Pearson | Spearman | 해석                                                |
| ------- | ------: | -------: | ------------------------------------------------- |
| `Iws`   |  -0.250 |   -0.358 | 가장 강한 음의 관계. 누적 풍속이 클수록 PM2.5가 낮아지는 경향            |
| `DEWP`  |   0.202 |    0.332 | 이슬점이 높을수록 PM2.5가 높아지는 경향                          |
| `PRES`  |  -0.092 |   -0.189 | 약한 음의 관계                                          |
| `TEMP`  |  -0.045 |    0.064 | 매우 약함. Pearson/Spearman 부호가 달라 단순 선형관계로 보기 어렵다    |
| `Is`    |   0.023 |    0.047 | 통계적으로는 유의하나 실질적 관계는 매우 약함                         |
| `Ir`    |  -0.048 |    0.006 | Spearman p-value가 0.2577로 유의하지 않음. 실질적으로 거의 관계 없음 |

---

## Cell 22 - code

Execution count: `123`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
 === scatter plot 개선 - 원본 target vs log1p target ===
원본 pm2.5 scatter는 고농도 outlier 때문에 낮은 구간의 구조가 잘 보이지 않을 수 있다.
```

#### Output 1 - display_data

```text
<Figure size 1200x400 with 2 Axes>
```

#### Output 2 - display_data

```text
<Figure size 1200x400 with 2 Axes>
```

#### Output 3 - display_data

```text
<Figure size 1200x400 with 2 Axes>
```

#### Output 4 - display_data

```text
<Figure size 1200x400 with 2 Axes>
```

#### Output 5 - display_data

```text
<Figure size 1200x400 with 2 Axes>
```

#### Output 6 - display_data

```text
<Figure size 1200x400 with 2 Axes>
```

---

## Cell 23 - code

Execution count: `129`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

```text
 === month별 주요 feature 상관계수 ===
```

#### Output 1 - display_data

```text
    month feature  pearson_corr  pearson_p_value  spearman_corr  \
1       1    DEWP      0.655966     0.000000e+00       0.730731   
5       2    DEWP      0.622824    3.356228e-291       0.727386   
9       3    DEWP      0.682816     0.000000e+00       0.778685   
13      4    DEWP      0.591549    1.776868e-271       0.645639   
17      5    DEWP      0.575635    2.952901e-262       0.652309   
21      6    DEWP      0.524983    9.003273e-204       0.545665   
25      7    DEWP      0.599467    6.637310e-290       0.640294   
29      8    DEWP      0.412377    1.499189e-122       0.468686   
33      9    DEWP      0.526335    5.323977e-205       0.650071   
37     10    DEWP      0.589943    1.404251e-278       0.622828   
41     11    DEWP      0.466171    2.368741e-155       0.563833   
45     12    DEWP      0.698190     0.000000e+00       0.721195   
0       1     Iws     -0.303491     1.902943e-64      -0.571587   
4       2     Iws     -0.262557     5.385522e-44      -0.437323   
8       3     Iws     -0.325823     1.491661e-74      -0.434085   
12      4     Iws     -0.266443     5.305787e-48      -0.281023   
16      5     Iws     -0.230051     4.847474e-37      -0.261836   
20      6     Iws     -0.032819     7.824396e-02      -0.041579   
24      7     Iws      0.021838     2.336685e-01      -0.030784   
28      8     Iws     -0.088496     1.330553e-06      -0.134485   
32      9     Iws     -0.119653     1.182139e-10      -0.213316   
36     10     Iws     -0.286221     3.224704e-57      -0.410410   
40     11     Iws     -0.330894     1.517585e-74      -0.576355   
44     12     Iws     -0.330468     9.147425e-77      -0.551940   
2       1    PRES     -0.359359     2.055598e-91      -0.443915   
6       2    PRES     -0.462143    1.363791e-143      -0.579718   
10      3    PRES     -0.523856    1.905183e-209      -0.501778   
14      4    PRES     -0.210928     2.530444e-30      -0.229529   
18      5    PRES      0.030444     9.681202e-02       0.052991   
22      6    PRES     -0.059190     1.483565e-03      -0.033786   
26      7    PRES      0.206925     3.845733e-30       0.253175   
30      8    PRES     -0.086881     2.068910e-06      -0.092479   
34      9    PRES     -0.321208     4.081724e-70      -0.379980   
38     10    PRES     -0.255294     1.706365e-45      -0.174410   
42     11    PRES     -0.261056     4.387960e-46      -0.246425   
46     12    PRES     -0.250782     6.533120e-44      -0.281074   
3       1    TEMP      0.035660     5.175525e-02       0.040759   
7       2    TEMP      0.128931     1.590977e-11       0.133777   
11      3    TEMP      0.061545     7.816634e-04       0.026403   
15      4    TEMP      0.055016     3.142649e-03       0.080680   
19      5    TEMP     -0.041985     2.199714e-02      -0.046329   
23      6    TEMP     -0.002587     8.896157e-01       0.012292   
27      7    TEMP     -0.029316     1.098395e-01      -0.008684   
31      8    TEMP      0.026063     1.551855e-01       0.021602   
35      9    TEMP      0.139651     5.146778e-14       0.185146   
39     10    TEMP      0.038022     3.807269e-02      -0.027065   
43     11    TEMP     -0.127534     6.451222e-12      -0.096676   
47     12    TEMP      0.044216     1.585391e-02       0.115269   

    spearman_p_value  
1       0.000000e+00  
5       0.000000e+00  
9       0.000000e+00  
13      0.000000e+00  
17      0.000000e+00  
21     3.435663e-223  
25      0.000000e+00  
29     2.061305e-162  
33      0.000000e+00  
37      0.000000e+00  
41     2.092976e-241  
45      0.000000e+00  
0      8.768334e-258  
4      4.276466e-127  
8      4.952302e-137  
12      2.037017e-53  
16      7.582088e-48  
20      2.565742e-02  
24      9.314826e-02  
28      1.745850e-13  
32      5.437184e-31  
36     2.729106e-121  
40     1.233498e-254  
44     6.180842e-237  
2      6.034986e-144  
6      2.483138e-243  
10     1.397011e-189  
14      9.666230e-36  
18      3.832595e-03  
22      6.985112e-02  
26      9.538661e-45  
30      4.333356e-07  
34      1.382537e-99  
38      9.328295e-22  
42      4.236283e-41  
46      3.689021e-55  
3       2.618140e-02  
7       2.654221e-12  
11      1.498658e-01  
15      1.458148e-05  
19      1.148185e-02  
23      5.096531e-01  
27      6.358292e-01  
31      2.387663e-01  
35      1.265727e-23  
39      1.399183e-01  
43      2.013286e-07  
47      2.851697e-10
```

#### Output 2 - stream

Stream: `stdout`

```text
 === B4-9-3단계 : month별 Spearman correlation 변화 ===
```

#### Output 3 - display_data

```text
<Figure size 800x400 with 1 Axes>
```

#### Output 4 - display_data

```text
<Figure size 800x400 with 1 Axes>
```

#### Output 5 - display_data

```text
<Figure size 800x400 with 1 Axes>
```

#### Output 6 - display_data

```text
<Figure size 800x400 with 1 Axes>
```

---

## Cell 24 - code

Execution count: `131`

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

### Outputs

#### Output 0 - stream

Stream: `stdout`

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

#### Output 1 - display_data

```text
<Figure size 1200x400 with 4 Axes>
```

#### Output 2 - stream

Stream: `stdout`

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

#### Output 3 - display_data

```text
<Figure size 1200x400 with 4 Axes>
```

#### Output 4 - stream

Stream: `stdout`

```text
 ===  Iws와 DEWP의 2D 공간에서 pm2.5 보기 ===
```

#### Output 5 - display_data

```text
<Figure size 700x500 with 2 Axes>
```

#### Output 6 - stream

Stream: `stdout`

```text
최종 결론:
연속형 기상 feature 중 Iws와 DEWP가 pm2.5와 가장 뚜렷한 관계를 보인다.
Iws는 음의 관계가 가장 강하며, 풍속이 커질수록 오염물질이 확산되어 PM2.5가 낮아지는 패턴으로 해석할 수 있다.
DEWP는 양의 관계가 비교적 강하며, 습하거나 정체된 기상 조건에서 PM2.5가 높아지는 패턴으로 해석할 수 있다.
```

---

## Cell 25 - markdown

## B2. Loss Curve 시각화 + 과적합 분석 (3점)

**요구사항**:
- Train Loss와 Val Loss를 한 그래프에 시각화
- 그래프 제목, x/y 축 라벨, 범례 모두 포함

**분석 (마크다운으로 작성)**:
- Loss curve를 보고 과적합이 발생했는지 판단하라
- 어떤 신호로 과적합을 판단했는지 설명

(직접 작성)

---

## Cell 26 - code

Execution count: `None`

```python

```

### Outputs

_No outputs._

---

## Cell 27 - markdown

**과적합 분석** (직접 작성):

(여기에 본인 그래프 기반 분석 작성)

---

## Cell 28 - markdown

---
# Part C. 정규화 4총사 각각 적용 (14점)

Part B와 같은 조건(같은 데이터, 같은 학습 설정)에서
*각 정규화 기법을 개별적으로* 적용해 효과를 비교하세요.

## C1. Dropout 적용 (3점)

**요구사항**: Baseline 구조에 Dropout(0.3)을 추가
**필수 출력**: Train Loss, Val Loss, Gap

---

## Cell 29 - code

Execution count: `None`

```python

```

### Outputs

_No outputs._

---

## Cell 30 - markdown

## C2. L2 Regularization 적용 (3점)

**요구사항**: 모든 Dense 층에 `kernel_regularizer=l2(0.01)`
**필수 출력**: Train Loss, Val Loss, Gap

---

## Cell 31 - code

Execution count: `None`

```python

```

### Outputs

_No outputs._

---

## Cell 32 - markdown

## C3. Early Stopping 적용 (3점)

**요구사항**:
- `EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)`
- epochs는 50보다 크게 잡아도 됨 (Early Stop이 멈춤)

**필수 출력**:
- Train Loss, Val Loss, Gap
(* 강의의 train_and_eval과 동일하게, history.history['val_loss'][-1](마지막 epoch의 val_loss)을 출력하시오.)
- 실제 학습된 epoch 수

---

## Cell 33 - code

Execution count: `None`

```python

```

### Outputs

_No outputs._

---

## Cell 34 - markdown

## C4. Batch Normalization 적용 (3점)

**요구사항**:
- `Dense → BatchNorm → Activation` 순서로 구성
- 활성화 함수는 Dense의 인자가 아닌 별도 `Activation('relu')`로

**필수 출력**: Train Loss, Val Loss, Gap

---

## Cell 35 - code

Execution count: `None`

```python

```

### Outputs

_No outputs._

---

## Cell 36 - markdown

## C5. 4가지 비교 시각화 (2점)

Baseline + 4총사 (5개 모델)의 loss curve를 비교 그래프로 시각화.

---

## Cell 37 - code

Execution count: `None`

```python

```

### Outputs

_No outputs._

---

## Cell 38 - markdown

---
# Part D. 종합 모델 + Test 평가 (5점)

## D1. 최종모델 선택 (5점) - 앞선 실험 결과를 통해 최종 모델을 만들 것 (과적합 및 정규화 효과 등을 고려)

## 이번에는 Test 평가까지 포함하여 최종 모델 성능을 제시할 것

---

## Cell 39 - code

Execution count: `None`

```python

```

### Outputs

_No outputs._

---

## Cell 40 - code

Execution count: `None`

```python

```

### Outputs

_No outputs._

---

## Cell 41 - code

Execution count: `None`

```python

```

### Outputs

_No outputs._

---

## Cell 42 - markdown

---

# ✅ 제출 전 체크리스트

- [ ] STUDENT_ID에 본인 학번을 정확히 입력했나?
- [ ] 모든 셀이 위에서 아래로 *실행 가능*한가?
- [ ] 모든 필수 출력값이 화면에 나타나는가?

---
