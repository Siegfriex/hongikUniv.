# ML_W13_PREP_VISUAL_LECTURE Visualization Checklist

이 체크리스트는 `visualization_spec.md`와 `visualization_cells.py`를 final notebook에 반영할 때 사용하는 품질 게이트다.

## 0. Global Gates

| gate | 기준 | 상태 |
|---|---|---|
| no external download | 기본 경로에서 network/download 호출 없음 | [ ] |
| default stack | NumPy/Pandas/Matplotlib/scikit-learn만으로 P0/P1 그래프 실행 | [ ] |
| output clean | canonical notebook은 outputs/execution_count 비움 | [ ] |
| nbformat valid | `nbformat.validate()` 통과 | [ ] |
| restart run all | `nbclient` 또는 Jupyter Run All 통과 | [ ] |
| interpretation scaffold | 비교 그래프 아래 `관찰/원인/제한/결론` 포함 | [ ] |
| code comments | data split, scaling, PCA, gradient, optimizer responsibility에 주석 포함 | [ ] |
| no decorative plot | 각 plot이 X/y, shape, gradient, update rule, metric, CNN bridge 중 하나를 설명 | [ ] |

## 1. V00 Gates

| visual | required point | 상태 |
|---|---|---|
| concept dependency map | Backprop 이후 Optimizer 위치가 보임 | [ ] |
| responsibility flow | X/y -> loss/backward -> param/grad -> optimizer 순서가 보임 | [ ] |
| visualization route map | 3D/PCA/gradient/heatmap view가 어느 섹션에 들어가는지 보임 | [ ] |
| checkpoint | `optimizer.step(net)` 직전 필요한 값 질문 포함 | [ ] |

## 2. V01 Gates

| visual | required point | 상태 |
|---|---|---|
| EDA dashboard | missing, dtype, correlation, label distribution 중 최소 3개 포함 | [ ] |
| mixed association map | Pearson/Spearman/Kendall/Cramer's V/eta-squared 중 가능한 지표 표시 | [ ] |
| continuous-continuous | Pearson/Spearman/Kendall을 구분해 표시 | [ ] |
| categorical-categorical | chi-square statistic, expected count, p-value, Cramer's V 표시 | [ ] |
| categorical composition | 100% stacked bar로 row-normalized composition 표시 | [ ] |
| continuous-categorical | box/hist/median + eta-squared/correlation ratio 표시 | [ ] |
| group mean test | 3개 이상 범주는 ANOVA 후보, 2개 범주는 Welch t 후보 표시 | [ ] |
| binary target | 가능하면 point-biserial table 표시 | [ ] |
| covariance vs correlation | covariance scale-dependence and normalized correlation 설명 | [ ] |
| regression residual | scatter+line, residual vs fitted, residual distribution 포함 | [ ] |
| group residual | 범주별 residual pattern 확인 | [ ] |
| PC regression | 다변수 numeric feature를 PC score로 압축한 residual view 포함 | [ ] |
| split-before-fit demo | train에만 `fit_transform`, val/test에는 `transform` 주석 포함 | [ ] |
| PCA 2D/3D | Iris 4D를 PCA 2D/3D로 projection | [ ] |
| PCA multiview | PC1-PC2 평면도, PC1-PC3 정면도, PC2-PC3 측면도 포함 | [ ] |
| scaling geometry | raw vs StandardScaler PCA 차이 표시 | [ ] |
| leakage warning | PCA/scaler를 split 전에 fit하면 leakage라는 설명 포함 | [ ] |

## 3. V02 Gates

| visual | required point | 상태 |
|---|---|---|
| 1D tangent | derivative가 local slope임을 보여줌 | [ ] |
| finite difference | analytic derivative와 수치미분 비교표 포함 | [ ] |
| 2D contour | gradient descent path 표시 | [ ] |
| 3D surface | loss basin을 3D로 표시 | [ ] |
| top/front/side views | 평면도/정면도/측면도로 curvature 차이를 분해 | [ ] |
| gradient field | gradient는 loss 증가 방향, update는 반대 방향이라는 주석 포함 | [ ] |
| XOR view | linear boundary 불가능성과 MLP 필요성 분리 | [ ] |

## 4. V03 Gates

| visual | required point | 상태 |
|---|---|---|
| Dense convention | `W=(Dout,Din)` 명시 | [ ] |
| shape table | X, W, b, Z, dZ, dW, db, dX 모두 포함 | [ ] |
| dW heatmap | optimizer가 읽는 parameter gradient임을 설명 | [ ] |
| db view | batch axis sum 설명 | [ ] |
| dX heatmap | 이전 layer로 전달되는 gradient임을 설명 | [ ] |
| ReLU derivative mask | activation layer는 parameter가 없어도 backward를 바꾼다는 설명 | [ ] |
| SoftmaxCE delta | `(p-y)/B`와 row-sum assert 포함 | [ ] |

## 4.5. V03.5 Gates

| visual | required point | 상태 |
|---|---|---|
| Dense width table | `H(Din+1)+K(H+1)` parameter count 수식 포함 | [ ] |
| parameter count plot | hidden width 증가가 parameter count를 늘림 | [ ] |
| ReLU function | `max(0,z)` plot 포함 | [ ] |
| ReLU derivative | `z>0` local derivative mask 포함 | [ ] |
| active ratio | width별 active_ratio 표시 | [ ] |
| dead unit ratio | width별 dead_unit_ratio 표시 | [ ] |
| train-only scaling | Iris activation lab도 scaler를 train subset에만 fit | [ ] |

## 5. V04 Gates

| visual | required point | 상태 |
|---|---|---|
| optimizer trajectory 3D | 같은 loss surface에서 optimizer별 경로 비교 | [ ] |
| top contour view | trajectory의 zig-zag/overshoot 확인 | [ ] |
| front/side projection | w0-loss, w1-loss projection 포함 | [ ] |
| state dashboard | grad norm, step norm, state norm 표시 | [ ] |
| LR sensitivity | raw lr pivot 금지, low/base/high setting axis 사용 | [ ] |
| parameter audit | `optimizer.step(net)`이 param/grad iterator만 순회한다는 표/주석 포함 | [ ] |
| Adam caution | train loss만으로 optimizer 선택 금지 | [ ] |

## 5.5. V04.5 Gates

| visual | required point | 상태 |
|---|---|---|
| bootstrap scope | train subset 내부 resample만 사용 | [ ] |
| fixed validation | validation set은 bootstrap마다 고정 | [ ] |
| no test usage | `test_used=False` assert 포함 | [ ] |
| width/optimizer grid | widths 4/16/64, SGD/Adam 비교 | [ ] |
| val accuracy distribution | bootstrap boxplot 표시 | [ ] |
| val macro-F1 distribution | bootstrap boxplot 표시 | [ ] |
| ReLU active distribution | active_ratio boxplot 표시 | [ ] |
| ReLU dead distribution | dead_unit_ratio boxplot 표시 | [ ] |
| mean±std evidence | parameter count vs mean±std validation score 표시 | [ ] |
| selection frequency | bootstrap별 validation macro-F1 rank 1 빈도 표시 | [ ] |
| percentile interval | p05/p50/p95 interval 표시 | [ ] |

## 6. V05 Gates

| visual | required point | 상태 |
|---|---|---|
| setup audit | same seed/split/init/epoch/batch 조건 표시 | [ ] |
| class ratio | stratified train/val/test ratio 표시 | [ ] |
| train/val curves | train loss, val loss, val accuracy, val macro-F1 분리 | [ ] |
| final metrics | final test accuracy/macro-F1 table | [ ] |
| confusion matrix | selected optimizer가 아니라 모든 optimizer final test confusion matrix 표시 가능 | [ ] |
| PCA decision space | Iris PCA 2D/3D class projection 표시 | [ ] |
| selected report | validation으로 선택된 optimizer에 대해서만 classification report 출력 | [ ] |

## 6.5. V05 Deep Diagnostic Gates

| visual | required point | 상태 |
|---|---|---|
| gradient norm | layer별 mean_grad_norm epoch curve 표시 | [ ] |
| update ratio | update_to_param_ratio epoch curve 표시 | [ ] |
| active/dead ratio | 학습 중 active_ratio/dead_unit_ratio 표시 | [ ] |
| ablation variants | no_scaling/no_relu/narrow/wide/init/lr variants 포함 | [ ] |
| ablation test policy | ablation은 validation only, test 미사용 assert 포함 | [ ] |
| failure cause link | ablation 결과를 scale/activation/init/lr 원인 후보와 연결 | [ ] |

## 7. V06 Gates

| visual | required point | 상태 |
|---|---|---|
| image fallback | Fashion cache 없으면 sklearn digits fallback | [ ] |
| scaling assert | Fashion `/255`, digits `/16`, range assert 통과 | [ ] |
| sample grid | image class 형태 확인 | [ ] |
| shape table | `(N,H,W)` -> `(N,H*W)` 변환 표시 | [ ] |
| pixel histogram | scaling 필요성 연결 | [ ] |
| image PCA 2D/3D | flattened image vector projection 표시 | [ ] |
| image multiview | PC1-PC2 평면도, PC1-PC3 정면도, PC2-PC3 측면도 포함 | [ ] |
| CNN bridge | local patch/receptive field와 flatten 차이 설명 | [ ] |

## 7.5. V07 Gates

| visual | required point | 상태 |
|---|---|---|
| no attention | Attention/Transformer 확장 없음 | [ ] |
| deeper MLP | Dense+ReLU block 2개 이상 포함 | [ ] |
| layer representation table | before/after layer output shape 표시 | [ ] |
| active ratio by layer | ReLU layer별 positive ratio 표시 | [ ] |
| representation PCA | before/after layer-wise PCA projection 표시 | [ ] |
| representation metrics | between/within ratio와 silhouette score 표시 | [ ] |
| optimizer boundary | 깊은 MLP에서도 optimizer는 W,b,dW,db만 본다는 주석 포함 | [ ] |

## 7.55. V08 Failure Gallery Gates

| visual | required point | 상태 |
|---|---|---|
| evidence table | symptom/evidence/likely_cause/confirm_with/action/answer_sentence columns 포함 | [ ] |
| diagnostic cards | 주요 failure를 카드형 board로 압축 | [ ] |
| answer linkage | 모든 failure가 시험 답안 문장으로 연결 | [ ] |

## 7.6. Final Visual Audit Board Gates

| visual | required point | 상태 |
|---|---|---|
| Board 1 trace | X/y -> forward -> loss -> backward -> optimizer.step shape board | [ ] |
| Board 2 dynamics | train/val curves + selected final test confusion matrix | [ ] |
| Board 3 architecture | Iris tabular vs image flatten vs CNN bridge decision | [ ] |
| answer sentence board | 주요 질문별 답안 시작 문장 포함 | [ ] |
| final scaffold | 관찰/원인/제한/결론/시험 답안 문장 포함 | [ ] |

## 8. Appendix EDA Gates

| case | required point | 상태 |
|---|---|---|
| missing values | train-only imputation vs full-data mean leakage 비교 | [ ] |
| categorical encoding | one-hot 후 input dimension 변화 표시 | [ ] |
| datetime features | datetime decomposition and cyclic option note | [ ] |
| regression metric note | MSE/MAE/RMSE의 역할 차이 표 | [ ] |
| optional PCA | numeric columns >= 2일 때만 PCA 실행, 아니면 skip message | [ ] |

## 9. Code Comment Checklist

| code area | comment must state | 상태 |
|---|---|---|
| data loading | local/fallback path and no download policy | [ ] |
| scaling | train-only fit and transform-only val/test | [ ] |
| PCA | projection axis, not original feature axis | [ ] |
| association | variable type determines Pearson/Spearman/Kendall/chi-square/Cramer's V/eta-squared | [ ] |
| Dense/ReLU | width changes hidden dimension/parameter count and ReLU gates gradients | [ ] |
| bootstrap | train-only resampling and validation-only stability interpretation | [ ] |
| residual diagnostics | correlation leads to model check, not model acceptance | [ ] |
| 3D multiview | what 3D/top/front/side view shows | [ ] |
| derivative | gradient is ascent direction, update is opposite | [ ] |
| backward | dW/db for optimizer, dX for previous layer | [ ] |
| optimizer | no X/y/loss read inside `step(net)` | [ ] |
| metrics | validation selection, final test report | [ ] |
| final board | figures converge to answer sentence, not more decorative plots | [ ] |

## 10. Verification Commands

```bash
.venv/bin/python -m py_compile ML/code_split/final/visualization_cells.py
.venv/bin/python ML/code_split/final/visualization_cells.py
.venv/bin/python - <<'PY'
import nbformat
from pathlib import Path
p = Path("ML/code_split/final/ML_W13_PREP_VISUAL_LECTURE.ipynb")
nb = nbformat.read(p, as_version=4)
nbformat.validate(nb)
print("nbformat ok", len(nb.cells))
PY
```
