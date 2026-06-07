# ML_W13_PREP_VISUAL_LECTURE Final Visualization Develop Plan

이 문서는 `ML_W13_PREP_VISUAL_LECTURE`의 최종 시각화 디벨롭 플랜이다. 기존 companion notebook의 핵심 루프는 그대로 둔다.

```text
X_batch -> net.forward -> loss_fn.forward -> loss_fn.backward -> net.backward -> optimizer.step(net)
```

시각화는 장식이 아니라 학습자가 아래 경계를 말로 설명하게 만드는 증거로만 사용한다.

```text
Optimizer는 X/y를 보지 않는다.
Optimizer는 layer가 들고 있는 param과 grad만 읽고 parameter를 update한다.
dW/db는 현재 layer의 parameter update용 gradient다.
dX는 이전 layer로 넘기는 gradient다.
Activation layer는 parameter가 없으므로 dW/db가 없다.
```

## 0. 최종 시각화 원칙

| 원칙 | 적용 |
|---|---|
| 기본 실행은 Matplotlib + NumPy/Pandas/scikit-learn | 모든 필수 그래프는 외부 다운로드 없이 실행 |
| 고차원은 한 그림으로 끝내지 않음 | 3D surface, 평면도, 정면도, 측면도, PCA projection을 함께 제공 |
| 미분은 수식만 두지 않음 | tangent, finite difference, gradient field, partial slice, heatmap을 연결 |
| EDA는 preview가 아니라 모델 설계 근거 | missing/dtype/scaling/correlation/PCA/class ratio가 output/loss/metric 선택과 연결 |
| 변수 관계는 type별로 분리 | 연속-연속 Pearson/Spearman, 범주-범주 Cramer's V, 연속-범주 eta-squared/point-biserial |
| 상관은 모델링의 시작점 | 공분산/상관 -> simple regression -> residual pattern -> model refinement로 연결 |
| Dense/ReLU는 representation block | width -> parameter count/hidden shape, ReLU -> active/dead gradient gate로 연결 |
| Bootstrap은 안정성 진단 | train subset resampling -> validation distribution -> architecture/optimizer 민감도 해석 |
| 최종 끝은 판단판 | 더 많은 그래프가 아니라 Final Visual Audit Board와 answer sentence로 종료 |
| notebook 안정성 우선 | optional seaborn/ipywidgets/NetworkX는 없어도 실패하지 않음 |
| 모든 비교 그림에는 해석 scaffold | `관찰 / 원인 / 제한 / 결론`을 바로 아래에 둠 |

## 1. 최종 섹션 매핑

| 섹션 | 기존 역할 | 최종 보강 방향 | 우선순위 |
|---|---|---|---|
| V00 | 전체 지도와 책임 분리 | 개념 graph + 실행 flow + 고차원 시각화 index table | P1 |
| V01 | 데이터/출력/손실/지표 | EDA method map, PCA 2D/3D, mixed association, regression residual dashboard | P0 |
| V02 | GD와 XOR | 1D tangent, 2D contour, 3D surface, 평면/정면/측면 view, finite difference | P0 |
| V03 | Dense backward/SoftmaxCE | dW/db/dX heatmap, Jacobian-like view, activation derivative mask, chain-rule path | P0 |
| V03.5 | Dense Width/ReLU Theory Lab | hidden width vs parameter count, ReLU function/derivative, active/dead unit ratio | P0 |
| V04 | Optimizer 4종 | optimizer trajectory를 3D surface/top/front/side view로 동시 비교 | P0 |
| V04.5 | Bootstrap stability lab | width x optimizer validation distribution, ReLU gate distribution, parameter count vs mean±std | P0 |
| V05 | Iris optimizer comparison | train/val/test metric dashboard + PCA decision-space projection | P1 |
| V05.5 | Gradient flow audit | layer별 grad norm, update/param ratio, active/dead unit ratio | P0 |
| V05.6 | Ablation lab | scaling/ReLU/width/init/lr controlled variants | P0 |
| V06 | Image tensor/CNN bridge | image grid + flatten geometry + PCA projection + local patch/CNN view | P1 |
| V07 | Proper MLP bridge | Dense+ReLU block 반복, layer-wise shape/active ratio/PCA before-after, representation quality metrics | P1 |
| V08 | Failure Gallery | symptom/evidence/cause/action/answer sentence cards | P0 |
| Final | Visual Audit Board | single-batch trace, learning dynamics, architecture bridge, answer sentence | P0 |
| Appendix EDA | 보조 데이터 | missing/categorical/datetime/scaling/PCA extension pack | P2 |

## 2. V00. 전체 지도와 역할 분리

### V00-A. Concept dependency graph

- 시각화 목적: Week8부터 Week15까지의 개념 의존성을 한 번에 고정한다.
- 사용할 데이터: 없음.
- 필요한 전처리: 없음.
- 코드 셀 설계: Mermaid text 또는 Matplotlib node diagram. 기본은 Markdown/Mermaid, 실행형은 Matplotlib fallback.
- 그래프 해석 포인트: Optimizer는 Backprop 이후에 있고, Backprop을 대체하지 않는다.
- 학생이 자주 하는 오해: optimizer가 loss와 y를 직접 보고 gradient를 계산한다고 생각한다.
- 체크포인트 질문: `optimizer.step(net)` 직전에 layer 내부에 반드시 있어야 하는 값은 무엇인가?

### V00-B. Visualization route map

- 시각화 목적: 노트북에서 어떤 개념을 어떤 view로 확인할지 선공개한다.
- 사용할 데이터: V01~V06 mapping table.
- 필요한 전처리: 없음.
- 코드 셀 설계: `concept / primary view / advanced view / section / checkpoint` table.
- 그래프 해석 포인트: 고차원은 PCA/3D/projection, 미분은 tangent/field/heatmap으로 나눠 본다.
- 학생이 자주 하는 오해: 3D 그래프가 있으면 고차원 전체를 이해했다고 생각한다.
- 체크포인트 질문: 4D Iris를 2D로 볼 때 무엇이 보존되고 무엇이 사라지는가?

## 3. V01. 데이터, 출력, 손실, 지표 설계

### V01-A. EDA dashboard

- 시각화 목적: EDA가 단순 탐색이 아니라 X/y, output, loss, metric 선택의 근거임을 보여준다.
- 사용할 데이터: `sklearn_iris`, `seaborn_titanic` profile fallback, `toy_missing_values_week14`, `toy_scaling_week14`.
- 필요한 전처리: numeric/categorical column 분리, missing count, class count, train/test split.
- 코드 셀 설계:
  - missing value bar
  - dtype count table
  - numeric correlation heatmap using Matplotlib
  - label/class distribution
  - train/test class ratio comparison
- 그래프 해석 포인트: 결측치와 dtype은 preprocessing choice를, class 분포는 metric choice를 결정한다.
- 학생이 자주 하는 오해: EDA를 모델 학습과 무관한 앞단 작업으로 본다.
- 체크포인트 질문: 이 dataset에서 accuracy만 보면 위험한 상황은 무엇인가?

### V01-A2. Mixed variable association dashboard

- 시각화 목적: 데이터 타입에 따라 관계 분석 지표가 달라져야 함을 보여준다.
- 사용할 데이터: Iris DataFrame, Titanic fallback/profile, categorical toy.
- 필요한 전처리: numeric/categorical column 분리, low-cardinality numeric target은 categorical로 처리, missing row는 pairwise drop.
- 코드 셀 설계:
  - continuous-continuous: Pearson correlation heatmap
  - continuous-continuous rank: Spearman correlation heatmap
  - ordinal/small-sample rank: Kendall tau heatmap
  - categorical-categorical: chi-square independence table, expected-count table, Cramer's V heatmap
  - categorical-categorical visual: 100% stacked bar for row-normalized composition
  - continuous-categorical: boxplot, grouped histogram, median bar, eta-squared/correlation ratio heatmap
  - continuous-categorical tests: one-way ANOVA for 3+ groups, Welch t candidate for binary category
  - binary target이 있을 경우 point-biserial correlation table
- 그래프 해석 포인트: Pearson은 선형 관계, Spearman은 단조 순위 관계, Kendall은 작은 표본/동순위 서열 안정성, chi-square p-value는 독립성 이탈, Cramer's V는 범주형 연관 강도, eta-squared는 group mean 차이 설명력을 본다.
- 학생이 자주 하는 오해: 모든 변수 조합에 Pearson correlation만 적용하려고 한다.
- 체크포인트 질문: `sex`와 `survived` 관계를 Pearson으로 보면 왜 부적절한가?

### V01-A3. Correlation to regression residual diagnostics

- 시각화 목적: 상관분석이 단순 회귀와 잔차 진단으로 어떻게 이어지는지 보여준다.
- 사용할 데이터: Iris numeric features, species label.
- 필요한 전처리: numeric columns selection, optional StandardScaler/PCA for multivariate view.
- 코드 셀 설계:
  - covariance to correlation proof-style demo
  - continuous-continuous scatter + simple regression line
  - residual vs fitted plot
  - residual histogram
  - residual by species boxplot
  - PC1/PC2 regression residual scatter for multivariate compression
- 그래프 해석 포인트: Pearson이 높아도 residual이 group별로 남으면 hidden categorical structure, interaction, nonlinear transformation, additional features를 검토해야 한다.
- 학생이 자주 하는 오해: 상관이 높으면 회귀 모델이 충분하고 인과도 성립한다고 생각한다.
- 체크포인트 질문: residual plot이 funnel shape이거나 group별 bias를 보이면 어떤 모델 수정 후보가 생기는가?

### V01-B. PCA 2D/3D projection for tabular data

- 시각화 목적: 고차원 feature matrix가 class separation과 scaling에 따라 어떻게 보이는지 확인한다.
- 사용할 데이터: Iris `X=(150,4)`, `y=(150,)`.
- 필요한 전처리: split-before-fit 원칙 유지. PCA는 `StandardScaler`를 train에 fit한 뒤 train/val/test에 transform한 결과에 적용한다.
- 코드 셀 설계:
  - raw petal scatter
  - standardized PCA 2D scatter
  - PCA 3D scatter
  - PC1-PC2 평면도, PC1-PC3 정면도, PC2-PC3 측면도
  - explained variance bar
- 그래프 해석 포인트: PCA view는 class 구조를 보기 위한 projection이며 classifier 성능 자체가 아니다.
- 학생이 자주 하는 오해: PCA 축을 원래 feature 축으로 해석한다.
- 체크포인트 질문: PCA를 split 전에 전체 데이터에 fit하면 왜 leakage인가?

### V01-C. Scaling effect on geometry and gradients

- 시각화 목적: scaling이 loss surface와 gradient scale에 영향을 준다는 점을 보여준다.
- 사용할 데이터: `toy_scaling_week14`, Iris numeric features.
- 필요한 전처리: raw, StandardScaler, MinMaxScaler 세 version 생성.
- 코드 셀 설계:
  - raw feature line/box plot
  - StandardScaler distribution
  - MinMaxScaler distribution
  - raw vs scaled PCA projection
  - feature scale ratio table
- 그래프 해석 포인트: feature scale이 크면 gradient update가 특정 축에 과도하게 민감해질 수 있다.
- 학생이 자주 하는 오해: scaling은 값만 예쁘게 바꾸는 작업이라고 생각한다.
- 체크포인트 질문: 같은 learning rate라도 scaling 전후 optimizer path가 달라질 수 있는 이유는 무엇인가?

### V01-D. Appendix EDA extension cases

- 시각화 목적: 다양한 데이터 타입에서 EDA가 어떤 preprocessing 결정을 만든다는 점을 보조로 보여준다.
- 사용할 데이터: Titanic fallback, missing toy, categorical toy, datetime toy.
- 필요한 전처리: missing count, one-hot encoded shape, datetime decomposition, train-only imputation.
- 코드 셀 설계:
  - missing bar + train mean vs full mean leakage comparison
  - categorical count + one-hot shape diagram
  - datetime feature cyclic plot
  - PCA is attempted only when numeric columns >= 2
- 그래프 해석 포인트: EDA는 dataset마다 다른 위험을 드러낸다.
- 학생이 자주 하는 오해: 모든 데이터셋에 같은 scaler와 같은 metric을 쓰면 된다고 생각한다.
- 체크포인트 질문: categorical encoding 후 input dimension은 왜 바뀌는가?

## 4. V02. Gradient Descent와 XOR Bridge

### V02-A. 1D derivative, tangent, finite difference

- 시각화 목적: derivative가 함수의 local slope이며, update는 slope 반대 방향이라는 점을 눈으로 확인한다.
- 사용할 데이터: `f(x)=(x-3)^2`, `df(x)=2(x-3)`.
- 필요한 전처리: 시작점과 learning rate 후보 고정.
- 코드 셀 설계:
  - 1D loss curve
  - 현재점 tangent line
  - finite difference slope vs analytic derivative table
  - update arrow `x_new = x - lr * grad`
- 그래프 해석 포인트: gradient는 증가 방향이고 gradient descent는 감소 방향으로 움직인다.
- 학생이 자주 하는 오해: gradient 자체가 최소점 방향을 가리킨다고 생각한다.
- 체크포인트 질문: x가 minimum 오른쪽에 있을 때 gradient sign과 update direction은 어떻게 되는가?

### V02-B. 2D loss surface multi-view

- 시각화 목적: 같은 loss surface를 3D/평면도/정면도/측면도로 분해해 curvature와 gradient를 이해한다.
- 사용할 데이터: `quad_loss(w)=0.1*w0^2 + 2.0*w1^2`.
- 필요한 전처리: meshgrid, analytic gradient, GD path.
- 코드 셀 설계:
  - 3D surface view
  - top contour 평면도
  - front view: `w0` vs loss with fixed `w1=0`
  - side view: `w1` vs loss with fixed `w0=0`
  - gradient vector field overlay
- 그래프 해석 포인트: `w1` 축의 curvature가 크므로 같은 lr에서 overshoot가 더 쉽게 발생한다.
- 학생이 자주 하는 오해: contour 간격과 gradient 크기의 관계를 보지 않는다.
- 체크포인트 질문: 왜 타원형 valley에서 zig-zag가 생기는가?

### V02-C. XOR feature-space view

- 시각화 목적: XOR가 선형 decision boundary로 분리되지 않음을 보여주고 hidden layer 필요성을 만든다.
- 사용할 데이터: embedded XOR truth table.
- 필요한 전처리: 없음. MLP decision region은 시각화 전용으로만 사용.
- 코드 셀 설계:
  - XOR truth table
  - scatter + impossible linear boundary examples
  - optional MLP decision region
  - hidden representation sketch
- 그래프 해석 포인트: hidden layer와 nonlinear activation은 feature space를 바꿔 선형 분리가 가능하게 만든다.
- 학생이 자주 하는 오해: optimizer만 바꾸면 XOR를 선형 모델로 풀 수 있다고 생각한다.
- 체크포인트 질문: XOR에서 optimizer보다 먼저 필요한 구조적 변화는 무엇인가?

## 5. V03. Dense.backward, ReLU, SoftmaxCE Shape

### V03-A. Dense forward/backward shape and axis view

- 시각화 목적: `dW`, `db`, `dX`의 shape와 책임을 분리한다.
- 사용할 데이터: synthetic mini-batch `B=4, Din=3, Dout=2`.
- 필요한 전처리: Dense convention 고정.
- 코드 셀 설계:
  - forward shape table
  - `dW = dZ.T @ X` matrix diagram
  - `db = dZ.sum(axis=0)` batch-axis diagram
  - `dX = dZ @ W` matrix diagram
  - dW/db/dX heatmaps
- 그래프 해석 포인트: `dW/db`는 parameter update용이고 `dX`는 이전 layer 전달용이다.
- 학생이 자주 하는 오해: optimizer가 `dX`를 update한다고 생각한다.
- 체크포인트 질문: `dW`와 `dX` 중 optimizer가 읽는 것은 무엇인가?

### V03-B. Activation derivative view

- 시각화 목적: ReLU가 gradient를 통과/차단하는 local derivative mask임을 보여준다.
- 사용할 데이터: synthetic `Z` matrix.
- 필요한 전처리: `mask = Z > 0`.
- 코드 셀 설계:
  - `Z` heatmap
  - ReLU output heatmap
  - ReLU derivative mask heatmap
  - upstream vs downstream gradient heatmap
- 그래프 해석 포인트: Activation layer는 parameter가 없지만 backward에서 gradient flow를 바꾼다.
- 학생이 자주 하는 오해: parameter가 없는 layer는 backward와 무관하다고 생각한다.
- 체크포인트 질문: ReLU mask에서 0인 위치의 gradient는 어떻게 되는가?

### V03-C. SoftmaxCE probability and delta view

- 시각화 목적: `p-y`가 logits로 되돌아가는 gradient임을 class별로 보여준다.
- 사용할 데이터: synthetic logits and labels.
- 필요한 전처리: softmax, one-hot, batch mean.
- 코드 셀 설계:
  - logits heatmap
  - probability heatmap
  - one-hot heatmap
  - `(p-y)/B` delta heatmap
  - row-sum assert table
- 그래프 해석 포인트: 정답 class는 probability를 올리도록, 오답 class는 probability를 낮추도록 gradient가 생긴다.
- 학생이 자주 하는 오해: softmax output과 loss gradient를 같은 것으로 본다.
- 체크포인트 질문: `delta` row sum이 0에 가까워야 하는 이유는 무엇인가?

## 5.5. V03.5. Dense Width & ReLU Action Theory Lab

### V03.5-A. Width to parameter count

- 시각화 목적: Dense width가 hidden representation shape와 parameter count를 동시에 바꾼다는 점을 보여준다.
- 사용할 데이터: Iris `Din=4`, class count `K=3`, candidate widths.
- 필요한 전처리: 없음.
- 코드 셀 설계:
  - `mlp_param_count(Din,H,K)=H(Din+1)+K(H+1)`
  - width table
  - width vs parameter count line plot
- 그래프 해석 포인트: width는 capacity와 계산/variance risk를 동시에 키운다.
- 학생이 자주 하는 오해: width 증가를 무조건 성능 증가로 본다.
- 체크포인트 질문: `H=64`일 때 어떤 parameter가 늘어나는가?

### V03.5-B. ReLU gate and derivative

- 시각화 목적: ReLU가 value gate이면서 gradient gate임을 보여준다.
- 사용할 데이터: synthetic `z=np.linspace(-5,5)`.
- 필요한 전처리: `relu=max(0,z)`, `derivative=(z>0)`.
- 코드 셀 설계:
  - ReLU function plot
  - local derivative plot
  - LeakyReLU는 note로만 언급
- 그래프 해석 포인트: z<=0이면 forward output과 local gradient가 모두 0이다.
- 학생이 자주 하는 오해: ReLU가 parameter를 가진다고 생각한다.
- 체크포인트 질문: inactive unit의 gradient는 어떻게 되는가?

### V03.5-C. Active/dead unit ratio by width

- 시각화 목적: 같은 data distribution에서도 초기 W와 width에 따라 ReLU gate 상태가 달라짐을 보여준다.
- 사용할 데이터: Iris train subset.
- 필요한 전처리: stratified split, train-only StandardScaler.
- 코드 셀 설계:
  - active_ratio
  - dead_unit_ratio
  - mean_activation
  - parameter_count
- 그래프 해석 포인트: parameter count는 단조 증가하지만 active ratio는 data/init에 의존한다.
- 학생이 자주 하는 오해: width만 키우면 모든 hidden unit이 의미 있게 작동한다고 생각한다.
- 체크포인트 질문: dead unit ratio가 높으면 backward에서 어떤 정보가 사라지는가?

## 6. V04. Optimizer 4종 비교

### V04-A. Optimizer trajectory multi-view

- 시각화 목적: 같은 gradient를 optimizer state가 어떻게 다른 trajectory로 바꾸는지 보여준다.
- 사용할 데이터: 2D anisotropic quadratic surface.
- 필요한 전처리: same start, same step count, optimizer별 stable lr.
- 코드 셀 설계:
  - 3D surface + trajectory
  - top contour 평면도 + trajectory
  - front view `w0` vs loss path
  - side view `w1` vs loss path
  - update norm time-series
- 그래프 해석 포인트: Momentum은 zig-zag를 줄이고, RMSProp/Adam은 좌표별 scale을 조절한다.
- 학생이 자주 하는 오해: optimizer가 다른 gradient를 새로 계산한다고 생각한다.
- 체크포인트 질문: trajectory가 다른 이유는 gradient가 달라서인가, update rule이 달라서인가?

### V04-B. Optimizer state decomposition

- 시각화 목적: velocity, squared-gradient EMA, first/second moment를 별도 축으로 관찰한다.
- 사용할 데이터: optimizer simulation history.
- 필요한 전처리: optimizer update 함수가 `step_norm`, `grad_norm`, state norm을 기록.
- 코드 셀 설계:
  - `grad_norm` vs `step_norm`
  - Momentum velocity norm
  - RMSProp squared accumulator norm
  - Adam first/second moment norm
  - low/base/high lr sensitivity heatmap
- 그래프 해석 포인트: raw learning rate는 optimizer별로 직접 비교하지 않고, relative setting으로 비교한다.
- 학생이 자주 하는 오해: Adam lr 0.01과 SGD lr 0.01을 같은 의미로 해석한다.
- 체크포인트 질문: `low/base/high` setting axis를 쓰는 이유는 무엇인가?

### V04-C. `optimizer.step(net)` parameter audit

- 시각화 목적: synthetic vector가 아니라 실제 Dense `W,b`가 바뀐다는 점을 확인한다.
- 사용할 데이터: dummy mini-batch and scratch network.
- 필요한 전처리: one forward/backward pass로 `dW/db` 생성.
- 코드 셀 설계:
  - before/after parameter norm table
  - dW/db norm table
  - update norm bar
  - parameter heatmap before/after/delta
- 그래프 해석 포인트: optimizer는 `X/y`가 아니라 layer의 param/grad iterator만 순회한다.
- 학생이 자주 하는 오해: optimizer가 batch data를 다시 읽는다고 생각한다.
- 체크포인트 질문: `optimizer.step(net)` 내부 loop는 어떤 object를 순회하는가?

## 6.5. V04.5. Bootstrap × Width × ReLU × Optimizer Stability

- 시각화 목적: train sample perturbation에 따른 architecture/optimizer 민감도를 단일 score가 아니라 distribution으로 보여준다.
- 사용할 데이터: Iris fixed train/validation split, bootstrap resample from train only.
- 필요한 전처리: split-before-fit, train-only scaler, fixed validation set, no test usage.
- 코드 셀 설계:
  - `bootstrap_dense_optimizer_study`
  - width in `[4,16,64]`
  - optimizer in `[SGD, Adam]`
  - val accuracy boxplot
  - val macro-F1 boxplot
  - ReLU active ratio boxplot
  - dead unit ratio boxplot
  - parameter count vs mean±std validation score
- 그래프 해석 포인트: 좋은 설계는 평균뿐 아니라 분산, active/dead gate 상태, validation-only selection으로 판단한다.
- 학생이 자주 하는 오해: bootstrap을 test replacement 또는 ensemble 성능 향상 기법으로 오해한다.
- 체크포인트 질문: validation 평균은 높지만 bootstrap 분산이 큰 조합은 어떻게 해석해야 하는가?

### V04.5-C. Selection robustness

- 시각화 목적: 평균 score가 아니라 bootstrap별 rank와 best frequency로 선택 안정성을 본다.
- 사용할 데이터: V04.5 bootstrap result table.
- 필요한 전처리: `boot_id`별 rank 계산.
- 코드 셀 설계:
  - rank by validation macro-F1
  - best frequency bar
  - p05/p50/p95 interval plot
- 그래프 해석 포인트: 가장 높은 평균과 가장 안정적인 선택은 다를 수 있다.
- 학생이 자주 하는 오해: 단일 best run을 안정적인 선택으로 착각한다.
- 체크포인트 질문: p05-p95 interval이 넓은 조합은 왜 위험한가?

## 7. V05. Iris Optimizer Comparison

### V05-A. Fair experiment dashboard

- 시각화 목적: optimizer comparison이 공정한 실험 조건 위에서만 의미가 있음을 보여준다.
- 사용할 데이터: sklearn Iris.
- 필요한 전처리: stratified train/val/test split, train-only StandardScaler, same initial weights.
- 코드 셀 설계:
  - setup audit table
  - train/val/test class ratio bar
  - initial parameter norm equality check
  - same split/same seed table
- 그래프 해석 포인트: optimizer만 바뀌어야 update rule 차이를 비교할 수 있다.
- 학생이 자주 하는 오해: split이나 초기값이 달라도 optimizer만 비교한다고 착각한다.
- 체크포인트 질문: 비교 실험에서 바뀌어도 되는 변수는 무엇인가?

### V05-B. Metric and PCA decision-space dashboard

- 시각화 목적: loss curve와 metric curve를 구분하고, Iris 4D geometry를 PCA projection으로 확인한다.
- 사용할 데이터: Iris train/val/test plus optimizer histories.
- 필요한 전처리: PCA fit on train-scaled X only.
- 코드 셀 설계:
  - train loss, val loss, val accuracy, val macro-F1
  - final test accuracy/macro-F1 table
  - final test confusion matrix
  - PCA 2D/3D class projection
  - selected optimizer prediction correctness overlay in PCA 2D
- 그래프 해석 포인트: validation으로 선택하고 test는 final report만 한다.
- 학생이 자주 하는 오해: test accuracy가 높은 optimizer를 다시 선택한다.
- 체크포인트 질문: PCA view에서 class가 겹치는 영역은 confusion matrix의 어떤 entry와 연결되는가?

## 7.5. V05.5 Gradient Flow Audit

- 시각화 목적: loss/metric curve 뒤에서 layer별 gradient와 update가 실제로 흐르는지 확인한다.
- 사용할 데이터: Iris validation probe.
- 필요한 전처리: train-only scaling.
- 코드 셀 설계:
  - train/val loss
  - validation macro-F1
  - layer별 mean grad norm
  - update/parameter ratio
  - active/dead unit ratio
- 그래프 해석 포인트: loss가 줄어도 gradient가 특정 layer에서 죽으면 학습 구조를 다시 봐야 한다.
- 학생이 자주 하는 오해: final score만 보고 학습 과정이 정상이라고 판단한다.
- 체크포인트 질문: update/parameter ratio spike는 어떤 failure 후보를 뜻하는가?

## 7.6. V05.6 Ablation Lab

- 시각화 목적: scaling/ReLU/width/init/lr 중 무엇이 성능과 안정성에 영향을 주는지 controlled comparison으로 본다.
- 사용할 데이터: Iris train/validation only.
- 필요한 전처리: variant별 조건 명시, test 미사용.
- 코드 셀 설계:
  - baseline/no scaling/no ReLU/narrow/wide/tiny init/large init/high lr
  - final validation macro-F1 bar
  - update/parameter ratio bar
  - dead unit ratio bar
  - validation macro-F1 curve
- 그래프 해석 포인트: optimizer 성능은 scale, activation, initialization, lr과 결합된 결과다.
- 학생이 자주 하는 오해: Adam/SGD 차이만으로 모든 성능 차이를 설명한다.
- 체크포인트 질문: no scaling과 high lr는 그래프에서 어떻게 다르게 실패하는가?

## 8. V06. Image Tensor / CNN Bridge

### V06-A. Image tensor and flatten geometry

- 시각화 목적: flatten은 pixel count를 보존하지만 local neighborhood 구조를 명시적으로 잃는다는 점을 보여준다.
- 사용할 데이터: Fashion-MNIST local cache or sklearn digits fallback.
- 필요한 전처리: Fashion `/255`, digits `/16`, `flat_scaled` shape/range assert.
- 코드 셀 설계:
  - sample grid
  - label distribution
  - original tensor shape table
  - flattened shape diagram
  - pixel histogram
- 그래프 해석 포인트: Dense MLP와 CNN은 optimizer를 공유할 수 있지만 parameter 구조가 다르다.
- 학생이 자주 하는 오해: flatten이 정보 손실이 없는 완전한 변환이라고 생각한다.
- 체크포인트 질문: flatten 후 어떤 위치 관계를 모델이 직접 알기 어려워지는가?

### V06-B. Image PCA and local patch bridge

- 시각화 목적: high-dimensional image vector를 PCA로 낮춰 보고, CNN local patch 관점으로 넘어간다.
- 사용할 데이터: scaled image flat matrix.
- 필요한 전처리: max sample cap, PCA fit on scaled flattened matrix.
- 코드 셀 설계:
  - PCA explained variance
  - PCA 2D/3D image class projection
  - PC1-PC2 평면도, PC1-PC3 정면도, PC2-PC3 측면도
  - sample image with local patch rectangle
  - CNN pipeline diagram
- 그래프 해석 포인트: PCA는 전체 vector variation을 보는 projection이고, CNN은 local receptive field를 학습하는 구조다.
- 학생이 자주 하는 오해: PCA와 CNN이 같은 종류의 feature extraction이라고 생각한다.
- 체크포인트 질문: PCA projection과 convolution kernel은 각각 어떤 기준으로 정보를 요약하는가?

## 9. V07. Proper MLP Representation Bridge, no Attention

- 시각화 목적: Dense+ReLU block을 반복하면 layer별 representation shape, activation sparsity, class projection이 어떻게 바뀌는지 보여준다.
- 사용할 데이터: Iris train/validation split.
- 필요한 전처리: train-only scaled Iris, no test usage.
- 코드 셀 설계:
  - `make_deeper_mlp`
  - `forward_collect_representations`
  - before/after layer output table
  - ReLU active ratio by layer
  - train/val curve
  - layer-wise PCA before/after
  - between/within ratio
  - silhouette score
- 그래프 해석 포인트: 깊은 MLP도 optimizer loop는 그대로이며, optimizer가 Dense parameter를 update해 representation을 바꾼다.
- 학생이 자주 하는 오해: 깊게 쌓으면 optimizer가 X/y를 직접 보게 된다고 생각한다.
- 체크포인트 질문: 깊은 MLP에서도 optimizer가 직접 보는 것은 `W,b,dW,db`인가?

## 9.5. V08 Failure Gallery

- 시각화 목적: 진단 그래프를 symptom/evidence/cause/action/answer sentence로 변환한다.
- 사용할 데이터: gradient flow, ablation, bootstrap, representation quality result tables.
- 필요한 전처리: 각 table에서 failure evidence row 추출.
- 코드 셀 설계:
  - failure gallery DataFrame
  - 2x2 diagnostic card board
- 그래프 해석 포인트: 시각화는 증상을 보는 데서 끝나지 않고 다음 확인 실험과 답안 문장으로 이어져야 한다.
- 학생이 자주 하는 오해: 그래프 모양을 묘사하는 것이 해석이라고 생각한다.
- 체크포인트 질문: failure card 하나를 관찰/원인/제한/결론/답안 문장으로 말할 수 있는가?

## 10. Final Visual Audit Board

- 시각화 목적: V00~V07 그래프를 한 장/두 장짜리 판단판으로 압축하고 answer sentence로 전환한다.
- 사용할 데이터: 앞선 실행 산출물.
- 필요한 전처리: 새 학습 없음. 기존 trace/run/image outputs 재사용.
- 코드 셀 설계:
  - Board 1: Single Batch Trace Board
  - Board 2: Learning Dynamics Board
  - Board 3: Architecture Bridge Board
  - Final Answer Sentence Board
- 그래프 해석 포인트: 끝은 plot 추가가 아니라 `관찰 -> 원인 -> 제한 -> 결론 -> 시험 답안 문장` 작성이다.
- 학생이 자주 하는 오해: 더 많은 3D/PCA/interactive plot이 좋은 시각화의 끝이라고 생각한다.
- 체크포인트 질문: 보드를 보고 `optimizer는 X/y가 아니라 param/grad만 본다`를 설명할 수 있는가?

## 11. 최종 코드 주석 기준

`visualization_cells.py`와 notebook에 들어갈 code comment는 다음 기준을 따른다.

| 위치 | 주석 내용 |
|---|---|
| data loading | 외부 다운로드 금지, fallback 조건, scaling range |
| split/scaling | 어떤 object에 fit하고 어떤 object에는 transform만 하는지 |
| PCA | PCA가 원래 feature가 아니라 projection axis임을 명시 |
| 3D/multiview | 3D, top, front, side view가 각각 무엇을 보존/버리는지 |
| gradient | gradient는 증가 방향, update는 반대 방향 |
| backward | dW/db와 dX의 역할 차이 |
| optimizer | optimizer가 X/y/loss를 직접 보지 않는다는 점 |
| metrics | validation 선택과 final test report 분리 |

## 10. 최종 반영 순서

1. P0: V02 1D/2D/3D derivative and loss surface multi-view.
2. P0: V04 optimizer trajectory multi-view and state decomposition.
3. P0: V03 Dense backward derivative/shape heatmap pack.
4. P0: V01 mixed variable association dashboard.
5. P0: V01 correlation-to-regression residual diagnostics.
6. P1: V01 EDA/PCA/scaling dashboard.
7. P1: V05 metric/PCA decision-space dashboard.
8. P1: V06 image PCA/local patch/CNN bridge.
9. P2: Appendix EDA extension cases.

## 11. 산출물 연결

| 산출물 | 역할 |
|---|---|
| `visualization_spec.md` | 섹션별 최종 시각화 디벨롭 플랜 |
| `visualization_cells.py` | notebook으로 옮길 수 있는 주석 강화 Python cell source |
| `visualization_checklist.md` | 구현/실행/해석 품질 게이트 |
| `ML_W13_PREP_VISUAL_LECTURE.md` | 현재 final notebook canonical source |
| `ML_W13_PREP_VISUAL_LECTURE.ipynb` | 실행 확인용 notebook |
