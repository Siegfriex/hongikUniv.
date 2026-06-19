# Full IPYNB Transcript: problem4 (1).ipynb

- Source notebook: `ML/final_exam/problem4 (1).ipynb`
- Cell count: `34`
- Method: notebook cell order preserved; markdown/code/text outputs transcribed; image outputs extracted and linked.
- Scope: current saved notebook state at transcript generation time.

---

## Cell 0 - markdown

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

---

## Cell 1 - code

Execution count: `None`

```python
STUDENT_ID = "0000"   # ← 본인 학번 마지막 4자리로 변경
SEED = int(STUDENT_ID)

assert STUDENT_ID != "0000", "학번을 입력하세요!"
print(f'학번(끝4자리): {STUDENT_ID}, SEED: {SEED}')
```

---

## Cell 2 - markdown

## 환경 준비

필요한 라이브러리를 import하고 seed를 고정하세요.
(회귀/분류 모두에 필요한 모듈 포함)

---

## Cell 3 - code

Execution count: `None`

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

---

## Cell 4 - markdown

---
# Part A. 데이터 EDA + Feature Engineering (제공 코드)

## A1. 데이터 로드 및 기본 정보

- 데이터 로드 및 shape 출력
- 결측치 확인
- 컬럼 목록 출력
- `cnt` 컬럼의 기본 통계 출력

---

## Cell 5 - code

Execution count: `None`

```python
url = 'https://raw.githubusercontent.com/PacktWorkshops/The-Data-Analysis-Workshop/master/Chapter01/data/hour.csv'
df = pd.read_csv(url)

print(f'Shape: {df.shape}')
print(f'결측치: {df.isnull().sum().sum()}')
print(f'\n컬럼: {df.columns.tolist()}')
print(f'\ncnt 분포:')
print(df['cnt'].describe())
```

---

## Cell 6 - markdown

## A2. 타겟 분포 시각화

- `cnt`의 원본 히스토그램과 log 변환 후 히스토그램을 나란히 비교
- 각 분포의 skewness 출력
- 어느 쪽이 회귀에 적합한지 판단 (마크다운으로 1줄)

---

## Cell 7 - code

Execution count: `None`

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
```

---

## Cell 8 - markdown

## A3. Feature Engineering

- 기존 데이터에서 *유용한 feature 1개 이상 추가* (예: 시간대 그룹, 주말 등)
- 추가한 feature가 범주형이면 One-Hot 인코딩
- ⚠️ **반드시 `casual`과 `registered`를 feature에서 제외** (data leakage 방지)
- ⚠️ `instant`, `dteday`, `cnt`도 feature에서 제외

**출력**:
- 최종 feature 컬럼 목록
- X.shape

---

## Cell 9 - code

Execution count: `None`

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

---

## Cell 10 - markdown

---
# Part B. 회귀 모델: cnt 예측 (10점)

## B1. 데이터 분할 + 정규화

- 타겟에 log 변환 적용 (`np.log1p`)
- 3분할 60/20/20, random_state=SEED
- StandardScaler 적용 (fit은 train에만)

---

## Cell 11 - code

Execution count: `None`

```python
# 회귀: y를 log 변환 (long-tail 처리)
y_reg_log = np.log1p(y_reg)

# 3분할
X_temp, X_test, y_temp, y_test_reg = train_test_split(
    X, y_reg_log, test_size=0.2, random_state=SEED
)
X_train_r, X_val_r, y_train_reg, y_val_reg = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=SEED
)

# 정규화
scaler_r = StandardScaler()
X_train_r = scaler_r.fit_transform(X_train_r)
X_val_r   = scaler_r.transform(X_val_r)
X_test_r  = scaler_r.transform(X_test)

print(f'Train: {X_train_r.shape}')
print(f'Val  : {X_val_r.shape}')
print(f'Test : {X_test_r.shape}')
```

---

## Cell 12 - markdown

## B2. Baseline + Regularized 회귀 모델 (7점)

**요구사항**:
- **Baseline**: Dense 2-3개 층, 정규화 없음
- **Regularized**: L2 + BatchNorm + Dropout + EarlyStopping 모두 적용
- 출력층: `Dense(1)` (회귀이므로 활성함수 없음)
- Loss: MSE, Metric: MAE
- 두 모델 모두 학습 + 결과 출력

(직접 작성)

---

## Cell 13 - code

Execution count: `None`

```python

```

---

## Cell 14 - code

Execution count: `None`

```python

```

---

## Cell 15 - markdown

## B3. Test 평가 (역변환 포함) (2점)

**요구사항**:
- 두 모델로 Test 예측
- **log 역변환** 후 *원본 스케일에서* MAE 계산
- 두 모델 MAE 비교 + 개선율 출력

**중요**: log 공간의 MAE는 의미가 약함 → 반드시 역변환 후 평가

---

## Cell 16 - code

Execution count: `None`

```python

```

---

## Cell 17 - markdown

## B4. 실제 vs 예측 산점도 (1점)

Regularized 모델의 예측값과 실제값을 산점도로 그리고, y=x 기준선 표시.
완벽한 예측이라면 점들이 y=x 선 위에 있어야 함.

---

## Cell 18 - code

Execution count: `None`

```python

```

---

## Cell 19 - markdown

---
# Part C. 분류 모델: 3구간 분류 (10점)

## C1. 타겟 binning 

- `cnt`를 3구간(low/mid/high)으로 binning
- 기준: **분위수** (33%, 66% percentile) 사용 → 균등한 클래스 분포
- 클래스 분포 출력

---

## Cell 20 - code

Execution count: `None`

```python
# 분위수 기준 binning (균등한 클래스 분포 유도)
q33 = np.percentile(y_reg, 33)
q66 = np.percentile(y_reg, 66)
print(f'33% 분위수: {q33}')
print(f'66% 분위수: {q66}')

def to_class(c):
    if c < q33: return 0   # low
    elif c < q66: return 1 # mid
    else: return 2         # high

y_cls = np.array([to_class(c) for c in y_reg])

print(f'\n클래스 분포:')
print(f'  Low (0)  : {(y_cls == 0).sum()} ({(y_cls == 0).mean():.1%})')
print(f'  Mid (1)  : {(y_cls == 1).sum()} ({(y_cls == 1).mean():.1%})')
print(f'  High (2) : {(y_cls == 2).sum()} ({(y_cls == 2).mean():.1%})')
```

---

## Cell 21 - markdown

## C2. 데이터 분할 + 분류 모델 (7점)

**요구사항**:
- 같은 feature X 사용 (Part A에서 만든 것)
- 3분할 (60/20/20) + **`stratify=y_cls`** (클래스 비율 유지)
- 별도 StandardScaler 사용 (회귀용과 분리)
- 분류 모델: Regularized (4총사 적용)
- 출력층: `Dense(3, activation='softmax')`
- Loss: `sparse_categorical_crossentropy`, Metric: `accuracy`

(직접 작성)

---

## Cell 22 - code

Execution count: `None`

```python
# 분할 (stratify=y_cls)
X_temp_c, X_test_c, y_temp_c, y_test_cls = train_test_split(
    X, y_cls, test_size=0.2, random_state=SEED, stratify=y_cls
)
X_train_c, X_val_c, y_train_cls, y_val_cls = train_test_split(
    X_temp_c, y_temp_c, test_size=0.25, random_state=SEED, stratify=y_temp_c
)

# 정규화 (별도 scaler — train 정보 누수 방지)
scaler_c = StandardScaler()
X_train_c = scaler_c.fit_transform(X_train_c)
X_val_c   = scaler_c.transform(X_val_c)
X_test_c  = scaler_c.transform(X_test_c)

print(f'Train: {X_train_c.shape}')
print(f'Val  : {X_val_c.shape}')
print(f'Test : {X_test_c.shape}')
```

---

## Cell 23 - code

Execution count: `None`

```python

```

---

## Cell 24 - markdown

## C3. Test 평가 + 혼동 행렬 (3점)

**요구사항**:
- Test Accuracy 출력
- `classification_report`로 클래스별 성능 출력
- 혼동 행렬을 seaborn heatmap으로 시각화

(직접 작성)

---

## Cell 25 - code

Execution count: `None`

```python

```

---

## Cell 26 - markdown

---
# Part D. 회귀 vs 분류 결과 비교 분석 (5점)

## D1. 두 접근법 비교 (2점)

**요구사항**:
- 회귀 모델의 예측값을 *같은 binning 기준*으로 변환해 분류 정확도 계산
- 직접 분류 모델의 정확도와 비교
- 둘 중 어느 쪽이 더 좋았는지 마크다운으로 분석

---

## Cell 27 - code

Execution count: `None`

```python

```

---

## Cell 28 - markdown

**비교 분석** (직접 작성):

(여기에 작성)

---

## Cell 29 - markdown

## D2. Feature Importance 추정 (2점)

**요구사항**:
- 회귀 모델의 첫 번째 Dense 층의 가중치 추출
- 각 feature의 *평균 절대 가중치*를 계산
- 상위 10개 feature를 막대 그래프로 시각화
- 어떤 feature가 가장 중요한지 마크다운으로 분석 (1-2줄)

(직접 작성)

---

## Cell 30 - code

Execution count: `None`

```python

```

---

## Cell 31 - markdown

**중요 Feature 분석** (직접 작성):

(여기에 작성)

---

## Cell 32 - markdown

## D3. `cnt` 분포가 long-tail인 이유와 log 변환의 효과 (1점)

**답**:

(직접 작성)

---

---

## Cell 33 - markdown

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
