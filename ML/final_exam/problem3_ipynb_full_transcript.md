# Full IPYNB Transcript: problem3 (1).ipynb

- Source notebook: `ML/final_exam/problem3 (1).ipynb`
- Cell count: `33`
- Method: notebook cell order preserved; markdown/code/text outputs transcribed; image outputs extracted and linked.
- Scope: current saved notebook state at transcript generation time.

---

## Cell 0 - markdown

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

---

## Cell 1 - code

Execution count: `None`

````python
STUDENT_ID = "0000"   # ← 본인 학번 마지막 4자리로 변경
SEED = int(STUDENT_ID)

assert STUDENT_ID != "0000", "학번을 입력하세요!"
print(f'학번(끝4자리): {STUDENT_ID}, SEED: {SEED}')
````

---

## Cell 2 - markdown

## 환경 준비

필요한 라이브러리를 import하고 seed를 고정하세요.
(seaborn, sklearn.metrics 등 분류에 필요한 모듈도 포함)

---

## Cell 3 - code

Execution count: `None`

````python
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
````

---

## Cell 4 - markdown

---
# Part A. EDA + 클래스 분포 (제공 코드)

## A1. 데이터 로드 및 기본 정보 출력

- `seaborn.load_dataset('diamonds')`로 로드
- 데이터 shape, 수치형/범주형 컬럼 목록, 결측치 개수, 기본 통계 출력

---

## Cell 5 - code

Execution count: `None`

````python
df = sns.load_dataset('diamonds')
print(f'Shape: {df.shape}')
print(f'\n수치형 컬럼: {df.select_dtypes(include="number").columns.tolist()}')
print(f'범주형 컬럼: {df.select_dtypes(include="category").columns.tolist()}')
print(f'\n결측치: {df.isnull().sum().sum()}')
print(f'\n기본 통계:')
print(df.describe())
````

---

## Cell 6 - markdown

## A2. 타겟 변수(cut) 클래스 분포

- 각 클래스 개수와 비율을 출력
- 막대 그래프로 시각화 (제목/축 라벨 포함)
- 클래스 불균형 비율 계산 (최대 클래스 / 최소 클래스)

---

## Cell 7 - code

Execution count: `None`

````python
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
````

---

## Cell 8 - markdown

## A3. 이상치 탐지 및 처리

데이터의 `x`, `y`, `z` (다이아몬드 크기) 컬럼에 *0값*이 존재할 수 있습니다.
이는 측정 오류로 추정됩니다.

- 각 컬럼별 0값 개수 출력
- 이상치를 처리한 후 데이터 shape 출력

---

## Cell 9 - code

Execution count: `None`

````python
# x, y, z (다이아몬드 크기)에 0값(이상치) 존재 여부 확인
for col in ['x', 'y', 'z']:
    zeros = (df[col] == 0).sum()
    print(f'{col}: 0 values = {zeros}')

# 이상치 처리: x, y, z 중 0인 행 제거
df_clean = df[(df['x'] > 0) & (df['y'] > 0) & (df['z'] > 0)].copy()
print(f'\n이상치 제거 후 shape: {df_clean.shape}')
````

---

## Cell 10 - markdown

---
# Part B. 범주형 인코딩 전처리 (제공 코드)

## B1. Ordinal Encoding (color, clarity)

`color`와 `clarity`는 **순서가 있는** 범주형 변수입니다:
- color: D(최고) → J(최하)
- clarity: IF(최고) → I1(최하)

**필요사항**:
- 순서를 보존하는 Ordinal Encoding 적용
- 인코딩 후 결과 검증 (예: 등급별 매핑 출력)

---

## Cell 11 - code

Execution count: `None`

````python
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
````

---

## Cell 12 - markdown

## B2. 타겟 인코딩

- `cut` 타겟을 정수로 인코딩 (Fair=0, Good=1, Very Good=2, Premium=3, Ideal=4)

**출력**:
- 인코딩 후 결과 검증 (예: 클래스별 매핑 출력)

---

## Cell 13 - code

Execution count: `None`

````python
# 타겟 인코딩
cut_order = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
cut_map = {c: i for i, c in enumerate(cut_order)}

df_clean['cut_label'] = df_clean['cut'].map(cut_map)

print('cut 인코딩:')
print(df_clean[['cut', 'cut_label']].drop_duplicates().sort_values('cut_label'))
````

---

## Cell 14 - markdown

## B3. Feature 선택 + 3분할 + 정규화

- Feature 선택 (수치형 + 인코딩한 범주형)
- 3분할 (60/20/20)
- **반드시 `stratify=y` 사용** (클래스 비율 유지)
- StandardScaler로 정규화

> 💡 **stratify=y**: 클래스 분포가 불균형하므로 분할 시 비율 유지 필수

**출력**:
- X_train, X_val, X_test shape
- 분할 후 각 클래스 비율이 유지되는지 확인 (예: train의 y_train 분포)

---

## Cell 15 - code

Execution count: `None`

````python
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
````

---

## Cell 16 - markdown

---
# Part C. 분류 모델 구축 (15점)

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

(직접 작성)

---

## Cell 17 - code

Execution count: `None`

````python
# C1. Baseline 분류 모델 — 여기에 작성하세요
````

---

## Cell 18 - markdown

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

(직접 작성)

---

## Cell 19 - code

Execution count: `None`

````python
# C2. Regularized 분류 모델 — 여기에 작성하세요
````

---

## Cell 20 - markdown

## C3. 학습 곡선 비교 (3점)

두 모델(Baseline, Regularized)의 **Validation Loss**와 **Validation Accuracy**를 각각 비교 시각화하시오.
(하나의 Figure에 서브플롯 2개 — 왼쪽: Validation Loss, 오른쪽: Validation Accuracy)

---

## Cell 21 - code

Execution count: `None`

````python
# C3. 학습 곡선 비교 (Val Loss / Val Accuracy) — 여기에 작성하세요
````

---

## Cell 22 - markdown

---
# Part D. 혼동 행렬 + 클래스별 성능 분석 (10점)

## D1. Test 예측 및 정확도 (3점)

**요구사항**:
- 두 모델 모두 X_test로 예측
- `predict()` 결과를 `argmax`로 클래스 변환
- 두 모델의 Test Accuracy 출력 및 비교

(직접 작성)

---

## Cell 23 - code

Execution count: `None`

````python
# D1. Test 예측 및 정확도 — 여기에 작성하세요
````

---

## Cell 24 - markdown

## D2. 혼동 행렬 시각화 (2점)

**요구사항**:
- 두 모델의 혼동 행렬을 *seaborn heatmap*으로 시각화
- 행/열 라벨에 클래스 이름 표시 (Fair, Good, Very Good, Premium, Ideal)
- 제목에 각 모델의 Test Accuracy 표시

(직접 작성)

---

## Cell 25 - code

Execution count: `None`

````python
# D2. 혼동 행렬 시각화 — 여기에 작성하세요
````

---

## Cell 26 - markdown

## D3. 클래스별 정밀도/재현율/F1 출력 (2점)

`sklearn.metrics.classification_report` 사용하여 클래스별 성능 출력 (두 모델 모두).

---

## Cell 27 - code

Execution count: `None`

````python
# D3. classification_report — 여기에 작성하세요
````

---

## Cell 28 - markdown

## D4. 클래스별 성능 분석 (마크다운, 3점)

본인의 혼동 행렬과 분류 리포트를 보고 답하라:

1. **어떤 클래스가 가장 잘 분류되었는가?** 원인은?
2. **어떤 클래스가 가장 못 분류되었는가?** 원인은?
3. **어떤 클래스 쌍이 가장 자주 혼동되는가?**

(직접 작성)

---

## Cell 29 - markdown

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

(직접 작성)

---

## Cell 30 - code

Execution count: `None`

````python
# E1. class_weight 적용 모델 — 여기에 작성하세요 (보너스)
````

---

## Cell 31 - code

Execution count: `None`

````python
# E2. 결과 비교 — 여기에 작성하세요 (보너스)
````

---

## Cell 32 - markdown

---

# ✅ 제출 전 체크리스트

- [ ] STUDENT_ID에 본인 학번을 정확히 입력했나?
- [ ] 모든 셀이 실행 가능한가?
- [ ] stratify=y로 분할했는가?

---
