# ML W13 Homework SSOT Inserted Report

## 1. 현재 산출본

- SSOT 원본: `week13_homework (1).ipynb`
- SSOT SHA-256: `d2c06ccca1cef8f14818a775fd2e6170a368eca59c690de34a2af9a104c73c9f`
- 연구형 삽입본: `ML_W13_HOMEWORK_SSOT_INSERTED.ipynb`
- 제출 안정성 정리본: `ML_W13_HOMEWORK_SUBMISSION_READY.ipynb`
- 연구형 삽입본 SHA-256: `f270c544f1c88b8a7dc9c53506383455541fbad2e5374664827d8a2ce6986efe`
- 제출 정리본 SHA-256: `5d6ac429d168dada627e92ddbe555dced38f795d563f28da53037b5af9e6defa`
- 연구형 삽입본 cell 수: 60 = 원본 28 + inserted 32
- 제출 정리본 cell 수: 61. 앞 28개는 원본 공식 homework cell, 이후는 Appendix extension.

## 2. 이번 정리에서 반영한 지적사항

- Part 5의 `[근거 기반 답변 초안]`을 Q1 아래에 몰아둔 구조를 제거하고, Q1~Q4 각각에 최종 답변을 배치했다.
- Final research conclusion board에서 Iris를 `MySGD best`처럼 보이게 하던 tie 처리 오류를 수정했다. 이제 Iris는 `test accuracy tie at 0.978: MySGD, MyMomentum, MyRMSProp, MyAdam; lowest loss=MyAdam`으로 기록된다.
- MNIST 결론은 `test accuracy best=MyRMSProp; lowest final loss=MyAdam`으로 accuracy와 loss를 분리해 기록한다.
- V04 trajectory summary에서 마지막 step의 `update_norm/state_norm`이 `NaN`으로 보이던 문제를 optimizer별 직전 update/state carry-forward로 정리했다.
- 제출 안정성 리스크를 줄이기 위해 `ML_W13_HOMEWORK_SUBMISSION_READY.ipynb`를 추가했다. 이 파일은 공식 과제 28개 cell을 먼저 두고, 연구형 확장은 Appendix로 이동한다.

## 3. Fresh Kernel 실행 결과

| notebook | cells | missing execution count | error outputs |
|---|---:|---|---|
| `ML_W13_HOMEWORK_SSOT_INSERTED.ipynb` | 60 | [] | [] |
| `ML_W13_HOMEWORK_SUBMISSION_READY.ipynb` | 61 | [] | [] |

TensorFlow CPU/GPU 정보 로그와 nbformat missing id warning은 있었지만 실행 실패는 아니다.

## 4. 공식 결과 요약

### Iris Official

| optimizer | final_loss | test_acc |
| --- | --- | --- |
| MySGD | 0.085444 | 0.977778 |
| MyMomentum | 0.057353 | 0.977778 |
| MyRMSProp | 0.050463 | 0.977778 |
| MyAdam | 0.039351 | 0.977778 |

해석: Iris는 네 optimizer가 모두 test accuracy 97.8%로 동률이다. 정확도만으로 winner를 고르면 안 되고, final loss에서는 MyAdam이 가장 낮다.

### MNIST Official

| optimizer | final_loss | test_acc |
| --- | --- | --- |
| MySGD | 0.478496 | 0.833500 |
| MyMomentum | 0.242558 | 0.891000 |
| MyRMSProp | 0.156582 | 0.907000 |
| MyAdam | 0.150897 | 0.905500 |

해석: MNIST는 test accuracy 기준 MyRMSProp이 90.7%로 최고이고, final loss 기준 MyAdam이 가장 낮다. 따라서 `RMSProp ≈ Adam > Momentum > SGD`로 쓰는 것이 결과와 맞다.

### LR Sensitivity

| lr | MySGD_test_acc | MyAdam_test_acc | Adam_minus_SGD |
| --- | --- | --- | --- |
| 0.000100 | 0.422222 | 0.444444 | 0.022222 |
| 0.001000 | 0.688889 | 0.955556 | 0.266667 |
| 0.010000 | 0.911111 | 0.977778 | 0.066667 |
| 0.100000 | 0.977778 | 0.977778 | 0.000000 |

## 5. 수정된 Final Board

| evidence area | summary | interpretation |
| --- | --- | --- |
| official Iris | test accuracy tie at 0.978: MySGD, MyMomentum, MyRMSProp, MyAdam; lowest loss=MyAdam | accuracy is saturated, so do not call the first sorted row the real best |
| official MNIST | test accuracy best=MyRMSProp; lowest final loss=MyAdam | RMSProp and Adam are close; report both accuracy and loss |
| LR sensitivity | MyAdam | smaller range means less sensitive in this grid |
| split-before-fit | train-only fit for research | official Part 2 kept all-fit scaler because homework specified it |
| V01.2 preprocessing audit | quality/correlation/Cramer/PCA + validation-test protocol | extension-only evidence that fit scope changes coordinates and model-selection ethics |
| diagnostics | confusion/residual/gradient audit | extension-only evidence, not replacement for scoring |
| V04 optimizer dynamics | trajectory/update/state dashboard | same gradient can produce different paths because optimizer state changes updates |
| Early virtual 3D contour | 3D parameter path + contour slices + evaluation table | front-loads optimizer geometry before Iris/MNIST official comparisons |
| V05 gradient flow | validation-only dW/db and update audit | test_used=False; explains loss/metric curve causes without replacing official results |
| Dense2 ReLU placement | raw logits vs output ReLU ablation | output activation can change CE score geometry even when accuracy is similar |
| Scoped plot policy | zoomed bars and quantile boxplots | differences are clearer, but titles/cautions must say scoped or zoomed |

## 6. V04 NaN 정리 확인

| optimizer | step | update_norm | state_norm |
| --- | --- | --- | --- |
| MySGD | 45 | 0.035864 | 0.000000 |
| MyMomentum | 45 | 0.113996 | 0.113996 |
| MyRMSProp | 45 | 0.055935 | 2.035072 |
| MyAdam | 45 | 0.057912 | 1.594512 |

마지막 summary row에 `NaN`이 남아 있지 않다.

## 7. Manifest / Artifacts

- `artifacts/cell_manifest_before.csv`
- `artifacts/cell_manifest_after.csv`
- `artifacts/cell_manifest_submission_ready.csv`
- figures: 15 files
- csv: 41 files
- configs: 2 files

## 8. 제출용 권장 파일

제출 안정성을 우선하면 `ML_W13_HOMEWORK_SUBMISSION_READY.ipynb`를 사용한다. 이 파일은 공식 Part 1~5를 먼저 보여주고, 연구 확장은 Appendix로 분리한다.

연구/학습 설명까지 함께 보여주려면 `ML_W13_HOMEWORK_SSOT_INSERTED.ipynb`를 사용한다.

## 9. 최종 자체 점검

- [x] 원본 homework SSOT는 직접 수정하지 않았다.
- [x] 공식 Part 1~5의 질문과 채점 기준 문구를 유지했다.
- [x] Part 5 Q1~Q4에 각각 답변이 들어갔다.
- [x] Iris accuracy tie를 winner처럼 표현하지 않도록 수정했다.
- [x] MNIST accuracy와 loss 기준 결론을 분리했다.
- [x] V04 final summary NaN을 제거했다.
- [x] submission-ready notebook은 원본 공식 cell 28개를 먼저 배치한다.
- [x] 두 notebook 모두 fresh kernel 실행에 성공했다.
