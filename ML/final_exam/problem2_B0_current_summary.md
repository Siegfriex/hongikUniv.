# Problem 2 현시점 정리 - Beijing PM2.5 회귀 분석

기준 파일: `ML/final_exam/problem2 (1).ipynb`  
정리 범위: A파트 제공 전처리 완료 후, 추가 B0 EDA 심화까지 진행한 상태  
현재 상태: B1 이후 모델 학습/정규화/최종 평가 셀은 아직 작성 전

---

## 1. 현재 진행 상태

- 학번 seed: `3085`
- 데이터: Beijing PM2.5 hourly data
- 원본 shape: `(43824, 13)`
- 원본 결측치: `pm2.5` 컬럼에 2067개
- 결측 처리: `ffill().bfill()` 적용
- 결측 처리 후 결측치: 0개
- 범주형 변수 `cbwd` one-hot encoding 완료
  - `cbwd_NE`
  - `cbwd_NW`
  - `cbwd_SE`
  - `cbwd_cv`
- 시간 변수 처리 완료
  - `datetime`
  - `dayofweek`
  - `is_weekend`
- 최종 모델 입력용 데이터:
  - `X: (43824, 16)`
  - `y: (43824,)`
- 제공 코드 기준 random 60/20/20 split 완료
  - Train: `(26294, 16)` / 60%
  - Val: `(8765, 16)` / 20%
  - Test: `(8765, 16)` / 20%
- `StandardScaler` 정규화 완료
  - train에 `fit_transform`
  - val/test에는 `transform`

---

## 2. B0 EDA 심화의 목적

B0는 모델을 만들기 전에 `pm2.5` target과 주요 feature의 관계를 확인하는 단계다.

핵심 목적은 다음이다.

1. `pm2.5`가 어떤 분포를 갖는지 확인한다.
2. 고농도 outlier가 단순 오류인지, 예측해야 할 중요한 사건인지 판단한다.
3. 주요 기상 feature와 target 사이의 관계를 확인한다.
4. test 정보를 보고 가설을 세우는 간접 leakage를 피하기 위해 train 기준으로 EDA한다.
5. 이후 B1 baseline DNN과 Part C regularization 실험의 해석 근거를 만든다.

---

## 3. B0-1. 시간순 Train/Test Split

B0에서는 별도로 시간순 split을 구성했다.

```text
df_eda shape: (43824, 19)
train_df shape: (35064, 19)
test_df shape: (8760, 19)
```

Train 기간:

```text
2010-01-01 00시 ~ 2013-12-31 23시
```

Test 기간:

```text
2014-01-01 00시 ~ 2014-12-31 23시
```

해석:

이 split은 “과거 4년으로 학습해서 다음 1년을 예측한다”는 현실적 예측 구조에 가깝다.  
시간 데이터에서는 미래 정보를 보고 가설을 세우면 간접적인 leakage가 생길 수 있으므로, B0 EDA에서는 train 기간 중심으로 target과 feature 관계를 확인했다.

주의:

시험 제공 코드의 실제 학습 split은 A4의 random 60/20/20 split이다. 따라서 제출용 B1 이후 모델 학습은 제공된 `X_train`, `X_val`, `X_test`, `y_train`, `y_val`, `y_test`를 기준으로 이어가는 것이 안전하다. B0 시간순 split은 심화 EDA 근거로 두는 편이 좋다.

---

## 4. B0-2. Target 분포 확인

Target은 `pm2.5`이며 연속형 회귀 target이다.

Train 기준 `pm2.5` 요약:

| 통계량 | 값 |
|---:|---:|
| count | 35064 |
| mean | 97.78 |
| std | 90.75 |
| min | 0 |
| 1% | 6 |
| 5% | 10 |
| 25% | 29 |
| 50% | 72 |
| 75% | 137 |
| 95% | 279 |
| 99% | 417 |
| max | 994 |

추가 지표:

```text
skewness: 1.8345
kurtosis: 5.3810
```

해석:

`pm2.5`는 정규분포에 가깝지 않다. 평균이 중앙값보다 크고, 75% 값은 137인데 95%는 279, 99%는 417, 최대값은 994까지 올라간다. 즉 오른쪽 꼬리가 긴 long-tail 분포이며, 고농도 outlier 또는 고농도 episode가 존재한다.

이 outlier는 단순 오류라기보다 실제 대기오염 고농도 사건일 수 있으므로 무조건 제거하면 안 된다. 모델링에서는 MSE가 큰 오차에 민감하게 반응할 수 있으므로 MAE, RMSE, `log1p` 변환, 고농도 구간 해석을 함께 고려해야 한다.

---

## 5. B0-3. 연속형 기상 feature와 target 관계

분석 대상 feature:

```text
DEWP, TEMP, PRES, Iws, Is, Ir
```

상관 분석 결과 요약:

| feature | Pearson | Spearman | 해석 |
|---|---:|---:|---|
| `Iws` | -0.250 | -0.358 | 가장 강한 음의 관계. 누적 풍속이 클수록 PM2.5가 낮아지는 경향 |
| `DEWP` | 0.202 | 0.332 | 이슬점이 높을수록 PM2.5가 높아지는 경향 |
| `PRES` | -0.092 | -0.189 | 약한 음의 관계 |
| `TEMP` | -0.045 | 0.064 | 관계가 매우 약하고 Pearson/Spearman 부호가 달라 단순 선형 관계로 보기 어려움 |
| `Is` | 0.023 | 0.047 | 통계적으로는 유의하지만 실질적 관계는 약함 |
| `Ir` | -0.048 | 0.006 | Spearman 기준 거의 관계 없음 |

핵심 해석:

- `Iws`는 PM2.5와 가장 뚜렷한 음의 관계를 보인다.
- `DEWP`는 PM2.5와 비교적 뚜렷한 양의 관계를 보인다.
- `PRES`는 약한 음의 관계를 보인다.
- `TEMP`, `Is`, `Ir`는 단독 feature로 강하게 해석하기 어렵다.
- 데이터 수가 매우 크기 때문에 p-value만 보면 대부분 유의하게 나올 수 있다. 따라서 p-value보다 correlation 크기와 시각적 패턴을 함께 봐야 한다.

---

## 6. B0-4. 원본 target과 log1p target 비교

원본 `pm2.5` scatter plot은 고농도 outlier 때문에 낮은 농도 구간의 구조가 잘 보이지 않을 수 있다.

따라서 B0에서는 다음 변수를 추가해 원본 target과 log 변환 target을 함께 비교했다.

```python
train_df["pm2.5_log1p"] = np.log1p(train_df["pm2.5"])
```

해석:

- `log1p` 변환은 오른쪽 긴 꼬리를 압축한다.
- 고농도 extreme value가 시각화를 지배하는 문제를 줄인다.
- 낮은 농도 구간의 구조를 더 잘 볼 수 있다.
- 회귀 모델이 큰 농도값 몇 개에 과도하게 끌리는 현상을 완화할 수 있다.
- 다만 시험 문제 Part B의 기본 target은 제공 코드 기준 `pm2.5` 원본이다. `log1p`를 실제 모델에 적용한다면 평가와 해석 단위를 명확히 써야 한다.

---

## 7. B0-5. 월별 상관 구조 변화

월별로 다음 feature와 `pm2.5`의 상관관계를 다시 확인했다.

```text
Iws, DEWP, PRES, TEMP
```

핵심 패턴:

- `DEWP`는 대부분의 월에서 PM2.5와 강한 양의 Spearman correlation을 보인다.
- `Iws`는 특히 겨울/가을 일부 구간에서 강한 음의 correlation을 보인다.
- `PRES`는 계절에 따라 방향과 강도가 달라진다.
- `TEMP`는 월별로 방향이 바뀌거나 약한 관계를 보여 전체 단순 상관만으로 해석하기 어렵다.

해석:

PM2.5 예측은 단순히 한 feature와 target의 전역 상관만으로 설명하기 어렵다. 계절, 월, 시간대에 따라 기상 feature의 의미가 달라질 수 있다. 따라서 DNN 모델은 이런 비선형·상호작용 구조를 일부 학습할 수 있다는 점에서 선형 모델보다 유리할 수 있다.

---

## 8. B0-6. 핵심 feature 후보

### 8.1 `Iws`

- 누적 풍속
- PM2.5와 가장 강한 음의 관계
- 풍속이 커질수록 오염물질이 확산되어 PM2.5가 낮아지는 패턴으로 해석 가능

### 8.2 `DEWP`

- 이슬점
- PM2.5와 비교적 강한 양의 관계
- 습하거나 정체된 기상 조건에서 PM2.5가 높아지는 패턴으로 해석 가능

### 8.3 `PRES`

- 기압
- 약한 음의 관계
- 계절별로 관계가 달라질 수 있음

### 8.4 시간 관련 변수

해당 변수:

```text
year, month, day, hour, dayofweek, is_weekend
```

주의:

`month`, `hour`, `dayofweek`는 숫자로 저장되어 있지만 순수한 continuous variable이라기보다 주기성/범주성 성격이 있다. 단순 선형 숫자처럼만 해석하면 위험하다.

---

## 9. B0까지의 최종 결론

`pm2.5`는 오른쪽 꼬리가 긴 연속형 회귀 target이며, 고농도 outlier가 실제 예측 대상이므로 무조건 제거하면 안 된다.

Train 기준 EDA에서 `Iws`는 PM2.5와 가장 강한 음의 관계를 보였고, `DEWP`는 비교적 강한 양의 관계를 보였다. `PRES`는 약한 음의 관계가 있으며, `TEMP`, `Is`, `Ir`는 단독 feature로 강하게 해석하기 어렵다.

계절과 월에 따라 상관 구조가 달라지므로, 이후 DNN 회귀 모델은 단순 선형 관계보다 비선형·상호작용 구조를 학습할 수 있는지 확인하는 방향으로 설계한다.

---

## 10. B1 이후 남은 작업

### 10.1 B1. Baseline 회귀 모델 구축

요구사항:

- DNN 회귀 모델 생성
- Dense layer 4개 이상
- 과적합 유도를 위해 train 일부, 최대 2000개만 사용
- `keras.utils.set_random_seed(SEED)` 호출 후 모델 생성
- optimizer: Adam
- loss: MSE
- metric: MAE
- `validation_data=(X_val, y_val)` 사용
- epochs=50
- batch_size=32
- 최종 Train Loss, Val Loss, Gap 출력

### 10.2 B2. Loss Curve 시각화와 과적합 분석

요구사항:

- train loss와 val loss를 한 그래프에 표시
- 제목, x축, y축, legend 포함
- train loss는 낮아지는데 val loss가 높거나 gap이 커지면 과적합으로 해석

### 10.3 Part C. 정규화 4총사

Baseline과 같은 조건에서 각각 따로 적용한다.

1. Dropout
   - `Dropout(0.3)`

2. L2 Regularization
   - 모든 Dense 층에 `kernel_regularizer=l2(0.01)`

3. EarlyStopping
   - `EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)`
   - 실제 학습 epoch 수 출력

4. BatchNormalization
   - `Dense -> BatchNormalization -> Activation("relu")` 순서

### 10.4 Part D. 최종 모델 + Test 평가

요구사항:

- 앞선 실험 결과를 바탕으로 최종 모델 선택
- 과적합과 정규화 효과를 근거로 선택 이유 작성
- test set으로 최종 성능 평가
- train/val/test 역할을 구분해서 해석

---

## 11. 제출용 주의사항

현재 노트북에는 A4의 random split과 B0의 시간순 split이 함께 존재한다.

정리:

- A4 random split:
  - 시험 제공 코드 기준
  - B1 이후 모델 학습에서 사용 권장
  - 변수: `X_train`, `X_val`, `X_test`, `y_train`, `y_val`, `y_test`

- B0 시간순 split:
  - 심화 EDA와 현실 예측 구조 설명용
  - 변수: `train_df`, `test_df`
  - 제출 답안에서는 모델 학습 기준 split과 혼동하지 않게 설명 필요

따라서 B1 이후에는 시험 요구사항에 맞춰 제공된 A4 split을 사용하고, B0는 “train 기준 EDA를 통해 target 구조와 주요 feature 관계를 확인했다”는 해석 근거로 두는 것이 가장 안전하다.
