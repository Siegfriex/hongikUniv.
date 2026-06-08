# ML W13 Homework SSOT Inserted Report

## 1. 원본 SSOT 구조 요약

- SSOT 원본: `week13_homework (1).ipynb`
- SSOT SHA-256: `d2c06ccca1cef8f14818a775fd2e6170a368eca59c690de34a2af9a104c73c9f`
- 작업 산출본: `ML_W13_HOMEWORK_SSOT_INSERTED.ipynb`
- 산출본 SHA-256: `8eb8ae8255dcd08137808db7e4fe7666cadd002f9ffa2c0e7172a73aa39394bf`
- 원본 cell 수: 28
- 산출본 cell 수: 60
- 삽입 cell 수: 32
- 원본 구조: Cell 0 안내, Part 1 Optimizer 구현, Part 2 Iris 비교, Part 3 MNIST 비교, Part 4 학습률 민감도, Part 5 분석 질문 4개, 채점 기준 표 유지.

## 2. 변경 원칙

- 원본 notebook은 직접 덮어쓰지 않았다.
- 원본 Part 순서, heading, markdown table, scoring table, 질문 문구, code cell block 위치를 보존했다.
- 원본 TODO가 있는 code cell은 TODO 위치만 채웠다.
- 원본 TODO가 아닌 scaffold, function signature, 변수명, config, plot skeleton은 유지했다.
- 연구형 EDA, residual diagnostics, split-before-fit diagnostic, optimizer audit, LR interpretation board, V04/V05-style 하단부 심층 실험, optimizer 시각화 후보군, scoped box/barplot 보드는 모두 새 cell 삽입 방식으로 추가했다.
- 이번 추가 보강에서는 Part 1 직후 초반부에 `Virtual 3D optimizer contour analysis`를 삽입해, 3D surrogate loss geometry와 contour slice 기반 optimizer 비교분석을 앞쪽에서 먼저 읽게 했다.
- inserted code cell 15개에는 공통 교육용 주석 헤더를 추가했다. 원본 SSOT code cell에는 이 헤더를 넣지 않았다.
- 삽입 cell 변수명은 `*_ext`, `diag_*`, `audit_*`, `research_*` 계열을 사용해 원본 변수와 충돌하지 않도록 설계했다.

## 3. TODO Completion 목록

- Part 1 `MySGD._update`: in-place `param -= lr * grad`.
- Part 1 `MyMomentum._update`: `id(param)` 기반 velocity dict, in-place `param += v`.
- Part 1 `MyRMSProp._update`: `id(param)` 기반 squared-gradient EMA dict, in-place update.
- Part 1 `MyAdam.step`: `self.t += 1` 후 `super().step(net)` 호출.
- Part 1 `MyAdam._update`: `id(param)` 기반 `m`, `v` dict, bias correction, in-place update.
- Part 2 `train_iris(OptCls, **kw)`: 원본 signature 유지, `Dense(4,16) -> ReLU -> Dense(16,3)`, `SoftmaxCE`, `fit`, test accuracy, `(history["loss"], test_acc)` 반환.
- Part 3 `train_mnist(OptCls, **kw)`: 원본 signature 유지, `Dense(784,64) -> ReLU -> Dense(64,32) -> ReLU -> Dense(32,10)`, `SoftmaxCE`, 5 epoch 학습, test accuracy 반환.
- Part 4: 원본 `lrs = [1e-4, 1e-3, 1e-2, 1e-1]` 유지, `sgd_accs`, `adam_accs` 생성.
- Part 5: 원본 Q1~Q4 문구 유지, 각 질문 아래 `[근거 기반 답변 초안]` 추가.

주의: `TODO`라는 문자열은 원본 안내 주석과 과제 문맥 보존 때문에 일부 남아 있다. 실행 가능한 `pass` placeholder는 0개이며, AST syntax check도 통과했다.

## 4. 삽입 Cell 목록

| 위치 | 제목 | 보완 대상 |
|---:|---|---|
| Cell 0 직후 | `[INSERTED] SSOT and no-rewrite contract` | 전체 원본 보존 원칙 |
| Part 1 XOR 확인 뒤 | `[INSERTED] Optimizer responsibility audit` | optimizer가 X/y가 아니라 param/grad만 읽는다는 책임 분리 |
| Part 1 XOR 확인 뒤 | `[INSERTED] Optimizer visualization candidate map` | optimizer 관련 전 파트 시각화 후보군과 3D 설계 축 정리 |
| Part 1 XOR 확인 뒤 | `[INSERTED] Virtual 3D optimizer contour analysis` | 가상 3D loss geometry, contour slice, loss/update 평가표 |
| Part 2 데이터 준비 뒤 | `[INSERTED] Iris DatasetCard and EDA` | Iris shape, class balance, feature signal, Pearson correlation |
| Part 2 plot 뒤 | `[INSERTED] Iris residual-style classification diagnostics` | confusion matrix, CE residual, margin, per-class F1 |
| Part 2 뒤 | `[INSERTED] Split-before-fit diagnostic` | all-fit scaler와 train-only scaler 좌표 차이 |
| Part 2 뒤 | `[INSERTED] Iris preprocessing, data-quality, association, PCA validation audit` | 데이터 품질, Pearson/Spearman/Kendall, Cramer's V, PCA, validation/test protocol |
| Part 3 결과 뒤 | `[INSERTED] MNIST/Digits error diagnostics` | digits 기반 extension-only class별 error 진단 |
| Part 4 뒤 | `[INSERTED] LR sensitivity table and interpretation board` | 공식 `sgd_accs`, `adam_accs` 표와 민감도 해석 |
| Part 4 뒤 | `[INSERTED] V04-style optimizer trajectory and state dashboard` | 3D surface, top contour, w0-loss/w1-loss projection, update/state norm |
| Part 4 뒤 | `[INSERTED] V04 numerical interpretation notes` | 수치해석 모범 스타일의 multi-view 해석 문장 |
| Part 4 뒤 | `[INSERTED] V05-style validation gradient-flow audit` | validation-only Dense별 dW/db, update/param ratio, ReLU gate 진단 |
| Part 4 뒤 | `[INSERTED] V05-style Dense2 output ReLU placement ablation` | 마지막 Dense 뒤 ReLU 유무에 따른 loss/accuracy/score clipping 비교 |
| Part 4 뒤 | `[INSERTED] Optimizer scoped box/barplot board` | boxplot/barplot 축 스코프 최적화와 delta view |
| Part 5 직전 | `[INSERTED] Evidence board for analysis questions` | Q1~Q4 답변 근거판 |
| 마지막 | `[INSERTED] Final research conclusion board` | 공식 결과와 보조 진단 통합 요약 |

## 5. 원본 과제 요구사항 충족 여부

- 원본 Part 1~5 순서 유지: 충족.
- 원본 채점 기준 표 유지: 충족.
- library optimizer 미사용: 충족.
- `Optimizer` base class 상속 유지: 충족.
- `_update(self, param, grad)` override 구조 유지: 충족.
- `MyAdam.step`에서 `self.t += 1` 후 parent `step(net)` 호출: 충족.
- 모든 optimizer update in-place: 충족.
- `id(param)` 기반 state dict 사용: 충족.
- `test_xor()` 실행: 충족, 4 optimizer 모두 loss < 0.05.
- Part 2 `results` plot 호환: 충족.
- Part 3 `mnist_results` plot 호환: 충족.
- Part 4 `sgd_accs`, `adam_accs` plot 호환: 충족.
- Part 5 질문 4개 문구 유지: 충족.
- 삽입 cell이 공식 결과를 대체하지 않음: 충족.
- inserted code comment header 적용: 15/15개.

## 6. Fresh Kernel 실행 여부

- 실행 방식: `nbclient` fresh kernel 실행.
- 결과: 성공.
- 실행 command context: `ML/code_split/final`, project `.venv`, `MPLCONFIGDIR=/tmp/matplotlib-cache`, `JUPYTER_CONFIG_DIR=/tmp/jupyter-config`.
- code cell execution count 누락: []
- error output: []
- 경고: TensorFlow CPU/GPU 정보 로그와 nbformat missing id warning이 있었으나 실행 실패는 아니다.

## 7. 주요 결과 요약

### Early Virtual 3D Optimizer Contour Analysis

| optimizer | start_loss | final_loss | loss_drop_ratio | final_distance_to_origin | path_length_3d | max_update_norm | mean_grad_norm | overshoot_count_loss_increase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Momentum | 12.772100 | 0.005271 | 0.999587 | 0.136949 | 13.910064 | 1.001571 | 1.731060 | 22 |
| SGD | 12.772100 | 0.192473 | 0.984930 | 1.797365 | 7.006806 | 1.818174 | 0.719351 | 0 |
| Adam | 12.772100 | 0.199644 | 0.984369 | 1.529728 | 5.898985 | 0.181865 | 2.385507 | 0 |
| RMSProp | 12.772100 | 0.258842 | 0.979734 | 2.068047 | 5.006764 | 0.410792 | 1.958052 | 0 |

해석: 이 surrogate에서는 `Momentum`가 final loss를 가장 낮게 만들었다. 다만 Momentum은 `overshoot_count_loss_increase=22`로 loss 증가 step도 많아, contour slice에서 zig-zag와 inertia가 잘 드러난다. SGD는 overshoot는 없지만 완만한 `w0` 축에서 천천히 drift한다. RMSProp/Adam은 update norm이 상대적으로 부드럽고 adaptive state로 step scale을 조절한다. 이 파트는 실제 Iris loss surface가 아니라 Part 2/3 비교를 읽기 위한 3D geometry bridge다.

### Part 2 Iris 공식 결과

| optimizer | final_loss | test_acc |
| --- | --- | --- |
| MySGD | 0.085444 | 0.977778 |
| MyMomentum | 0.057353 | 0.977778 |
| MyRMSProp | 0.050463 | 0.977778 |
| MyAdam | 0.039351 | 0.977778 |

해석: Iris test accuracy는 네 optimizer 모두 97.8%로 포화되어 accuracy만으로는 차이가 작다. loss 기준으로는 MyAdam, MyRMSProp, MyMomentum, MySGD 순으로 낮다.

### Part 3 MNIST 공식 결과

| optimizer | final_loss | test_acc |
| --- | --- | --- |
| MySGD | 0.478496 | 0.833500 |
| MyMomentum | 0.242558 | 0.891000 |
| MyRMSProp | 0.156582 | 0.907000 |
| MyAdam | 0.150897 | 0.905500 |

해석: 5 epoch subset 조건에서는 `MyRMSProp`가 test accuracy 최고, `MyAdam`가 final loss 최저다. MySGD는 같은 epoch budget에서 수렴이 느리다.

### Part 4 LR Sensitivity 공식 결과

| lr | MySGD_test_acc | MyAdam_test_acc | Adam_minus_SGD |
| --- | --- | --- | --- |
| 0.000100 | 0.422222 | 0.444444 | 0.022222 |
| 0.001000 | 0.688889 | 0.955556 | 0.266667 |
| 0.010000 | 0.911111 | 0.977778 | 0.066667 |
| 0.100000 | 0.977778 | 0.977778 | 0.000000 |

### V01.2 Iris Data Quality / Association / PCA 보조 진단

Data quality 핵심:

| check | value | why_it_matters |
| --- | --- | --- |
| n_rows | 150.000 | sample 수. split 후 class별 표본이 너무 적지 않은지 본다. |
| n_numeric_features | 4.000 | Dense 입력 차원 Din=4와 직접 연결된다. |
| missing_cells | 0.000 | 0이면 imputation은 필요 없지만, 원칙은 train-only fit이다. |
| duplicate_rows | 1.000 | 중복이 있으면 split leakage와 과대평가 가능성을 점검한다. |
| class_count_min | 50.000 | stratified split의 최소 class 표본 수. |
| class_count_max | 50.000 | class imbalance 확인용 최대 class 표본 수. |
| class_balance_ratio | 1.000 | 1에 가까울수록 class balance가 좋다. |

Cramer's V 핵심:

| feature | cramers_v_with_species | contingency_shape |
| --- | --- | --- |
| petal width (cm) | 0.942242 | (3, 3) |
| petal length (cm) | 0.924701 | (3, 3) |
| sepal length (cm) | 0.641049 | (3, 3) |
| sepal width (cm) | 0.471537 | (3, 3) |

PCA fit scope 비교:

| PC | train_only_explained_variance_ratio | all_fit_explained_variance_ratio | component_alignment_abs_dot |
| --- | --- | --- | --- |
| PC1 | 0.713844 | 0.729624 | 0.997598 |
| PC2 | 0.248495 | 0.228508 | 0.997716 |
| PC3 | 0.032537 | 0.036689 | 0.999876 |

Validation/test protocol:

| optimizer | final_train_loss | val_accuracy | val_macro_f1 | test_accuracy_final_report_only | test_macro_f1_final_report_only | test_used_for_selection | selected_by_validation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MySGD | 0.130895 | 1.000000 | 1.000000 | 0.966667 | 0.966583 | False | True |
| MyMomentum | 0.088125 | 0.966667 | 0.966583 | 0.966667 | 0.966583 | False | False |
| MyRMSProp | 0.068650 | 0.966667 | 0.966583 | 0.966667 | 0.966583 | False | False |
| MyAdam | 0.061071 | 1.000000 | 1.000000 | 0.966667 | 0.966583 | False | True |

해석: missing은 없고 class balance는 1.0이다. Petal width/length는 Cramer's V가 약 0.94/0.92로 species와 강하게 연결된다. PCA는 train-only와 all-fit의 explained variance 및 test 좌표가 약간 달라지며, 이 차이가 바로 split-before-fit을 시각화하는 근거다. Validation 기준 선택에서는 `MySGD, MyAdam`가 tie로 잡혔고, test는 선택이 아니라 final reporting으로만 기록했다.

### V04-style Surface Projection 보조 진단

- `3D surface view`: synthetic quadratic loss 표면 위에서 optimizer path의 전체 공간감을 확인했다.
- `top contour view`: optimizer별 zig-zag와 overshoot를 가장 선명하게 비교하도록 추가했다.
- `front w0-loss projection`: 완만한 축 `w0`를 따라 loss가 어떻게 줄어드는지 확인하도록 추가했다.
- `side w1-loss projection`: 가파른 축 `w1`에서 초반 loss 감소와 진동을 확인하도록 추가했다.

### V05-style Dense2 Output ReLU Placement 보조 진단

| variant | relu_after_dense2 | best_val_loss | best_val_epoch | final_train_loss | final_val_loss | final_val_accuracy | final_val_macro_f1 | final_score_zero_ratio | test_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw_logits_no_relu_after_Dense2 | False | 0.037735 | 79 | 0.055851 | 0.037735 | 0.973684 | 0.973162 | 0.000000 | False |
| relu_after_Dense2 | True | 0.763149 | 79 | 0.771983 | 0.763149 | 0.684211 | 0.550265 | 0.868421 | False |

해석: 마지막 Dense 뒤 ReLU는 class score의 음수 logit을 0으로 잘라 SoftmaxCE에 들어가는 score geometry를 제한한다. Iris validation 조건에서는 output ReLU variant가 loss와 macro-F1 모두에서 크게 나빠졌다.

## 8. 누수/Leakage 관련 주의사항

- 원본 Part 2의 `X = StandardScaler().fit_transform(iris.data)`는 homework 공식 지시이므로 그대로 유지했다.
- 연구 확장 cell에서는 split-before-fit 원칙을 별도로 시각화했다.
- 이번 V01.2 보강은 `train/validation/test split -> StandardScaler.fit(train) -> transform(validation/test) -> PCA.fit(train) -> validation 선택 -> test final report` 순서를 사용했다.
- Iris처럼 쉬운 데이터에서는 metric 차이가 작거나 tie가 날 수 있지만, metric이 같아도 all-fit preprocessing은 test 분포를 fit/adapt 단계에 넣는 평가 프로토콜 오염이다.
- Cramer's V는 numeric feature를 `pd.qcut(q=3)`으로 categorical bin화한 뒤 species와의 association을 본 보조 EDA 지표다. 모델 성능 지표가 아니라 feature-label 구조 해석 도구다.

## 9. 생성 Artifact

### Manifest

- `artifacts/cell_manifest_before.csv`
- `artifacts/cell_manifest_after.csv`

### New Virtual 3D Optimizer Figures

- `artifacts/figures/virtual_3d_optimizer_contour_analysis_ext.png`

### New Virtual 3D Optimizer CSV

- `artifacts/csv/virtual_3d_optimizer_paths_ext.csv`
- `artifacts/csv/virtual_3d_optimizer_evaluation_ext.csv`
- `artifacts/csv/virtual_3d_optimizer_reading_guide_ext.csv`
- `artifacts/csv/virtual_3d_optimizer_interpretation_ext.csv`

### V01.2 Figures

- `artifacts/figures/iris_preprocessing_association_pca_audit_ext.png`
- `artifacts/figures/iris_validation_test_protocol_ext.png`

### V01.2 CSV

- `artifacts/csv/iris_data_quality_board_ext.csv`
- `artifacts/csv/iris_feature_quality_ext.csv`
- `artifacts/csv/iris_corr_pearson_ext.csv`
- `artifacts/csv/iris_corr_spearman_ext.csv`
- `artifacts/csv/iris_corr_kendall_ext.csv`
- `artifacts/csv/iris_corr_pair_rank_ext.csv`
- `artifacts/csv/iris_cramers_v_species_ext.csv`
- `artifacts/csv/iris_preprocessing_scope_audit_ext.csv`
- `artifacts/csv/iris_pca_variance_scope_ext.csv`
- `artifacts/csv/iris_pca_loadings_train_only_ext.csv`
- `artifacts/csv/iris_validation_test_protocol_ext.csv`
- `artifacts/csv/iris_preprocessing_eda_validation_interpretation_ext.csv`

### All Figures (15)

- `artifacts/figures/digits_extension_error_diagnostics.png`
- `artifacts/figures/final_official_result_summary.png`
- `artifacts/figures/iris_datasetcard_eda.png`
- `artifacts/figures/iris_preprocessing_association_pca_audit_ext.png`
- `artifacts/figures/iris_residual_confusion_diagnostics.png`
- `artifacts/figures/iris_validation_test_protocol_ext.png`
- `artifacts/figures/lr_sensitivity_interpretation_board.png`
- `artifacts/figures/optimizer_responsibility_update_norm.png`
- `artifacts/figures/optimizer_scoped_bar_box_board_ext.png`
- `artifacts/figures/split_before_fit_diagnostic.png`
- `artifacts/figures/v04_optimizer_state_dashboard_ext.png`
- `artifacts/figures/v04_optimizer_surface_projection_pack_ext.png`
- `artifacts/figures/v05_dense2_relu_placement_ablation_ext.png`
- `artifacts/figures/v05_validation_gradient_flow_audit_ext.png`
- `artifacts/figures/virtual_3d_optimizer_contour_analysis_ext.png`

### All CSV (41)

- `artifacts/csv/digits_extension_per_class_accuracy.csv`
- `artifacts/csv/final_research_conclusion_board.csv`
- `artifacts/csv/iris_classification_residuals.csv`
- `artifacts/csv/iris_corr_kendall_ext.csv`
- `artifacts/csv/iris_corr_pair_rank_ext.csv`
- `artifacts/csv/iris_corr_pearson_ext.csv`
- `artifacts/csv/iris_corr_spearman_ext.csv`
- `artifacts/csv/iris_cramers_v_species_ext.csv`
- `artifacts/csv/iris_data_quality_board_ext.csv`
- `artifacts/csv/iris_dataset_card_ext.csv`
- `artifacts/csv/iris_eda_interpretation_ext.csv`
- `artifacts/csv/iris_feature_correlation_ext.csv`
- `artifacts/csv/iris_feature_quality_ext.csv`
- `artifacts/csv/iris_pca_loadings_train_only_ext.csv`
- `artifacts/csv/iris_pca_variance_scope_ext.csv`
- `artifacts/csv/iris_preprocessing_eda_validation_interpretation_ext.csv`
- `artifacts/csv/iris_preprocessing_scope_audit_ext.csv`
- `artifacts/csv/iris_residual_diagnostic_summary.csv`
- `artifacts/csv/iris_validation_test_protocol_ext.csv`
- `artifacts/csv/lr_sensitivity_official_part4.csv`
- `artifacts/csv/lr_sensitivity_summary_ext.csv`
- `artifacts/csv/official_iris_summary.csv`
- `artifacts/csv/official_mnist_summary.csv`
- `artifacts/csv/optimizer_3d_design_candidates_ext.csv`
- `artifacts/csv/optimizer_responsibility_audit.csv`
- `artifacts/csv/optimizer_scoped_axis_policy_ext.csv`
- `artifacts/csv/optimizer_visualization_candidate_map_ext.csv`
- `artifacts/csv/part5_evidence_board.csv`
- `artifacts/csv/split_before_fit_diagnostic.csv`
- `artifacts/csv/v04_optimizer_interpretation_ext.csv`
- `artifacts/csv/v04_optimizer_trajectory_state_ext.csv`
- `artifacts/csv/v04_projection_reading_guide_ext.csv`
- `artifacts/csv/v05_dense2_relu_interpretation_ext.csv`
- `artifacts/csv/v05_dense2_relu_placement_curve_ext.csv`
- `artifacts/csv/v05_dense2_relu_placement_summary_ext.csv`
- `artifacts/csv/v05_gradient_flow_interpretation_ext.csv`
- `artifacts/csv/v05_validation_gradient_flow_audit_ext.csv`
- `artifacts/csv/virtual_3d_optimizer_evaluation_ext.csv`
- `artifacts/csv/virtual_3d_optimizer_interpretation_ext.csv`
- `artifacts/csv/virtual_3d_optimizer_paths_ext.csv`
- `artifacts/csv/virtual_3d_optimizer_reading_guide_ext.csv`

### Config (2)

- `artifacts/configs/ssot_inserted_config.json`
- `artifacts/configs/ssot_inserted_static_config.json`

## 10. 사용자가 Part 5 답변을 직접 검토해야 할 지점

- 답변은 `[근거 기반 답변 초안]`으로 넣었다. 제출 전 본인 문체와 수업 표현에 맞게 다듬는 것이 좋다.
- Q1은 새 초반 3D surrogate contour와 Part 2/3 loss curve를 함께 근거로 삼으면 좋다.
- Q2는 lr=0.1에서 Iris accuracy가 같게 나와도, loss curve나 update norm 안정성 차이를 함께 언급해야 한다.
- Q3은 네 개 lr grid만 본 실험이므로 “완전히 둔감하다”가 아니라 “이 grid에서는 상대적으로 둔감하다”로 제한을 달아야 한다.
- Q4는 Adam을 1차 baseline으로 제안하되, 데이터 구조와 scaling, epoch budget에 따라 RMSProp/Momentum을 같이 비교한다고 쓰는 편이 안전하다.
- 새 V01.2 보강은 Q4에서 “optimizer 선택은 전처리 품질, feature geometry, validation/test 분리와 함께 결정해야 한다”는 근거로 사용한다.
- 새 V04 surface projection pack은 Q1~Q3에서 “왜 loss curve와 lr sensitivity가 달라지는가”를 설명하는 보조 근거다.
- Dense2 output ReLU placement 결과는 출력층 activation을 습관적으로 추가하면 안 된다는 architecture caution 근거다.

## 11. 최종 자체 점검

- [x] 원본 Part 1~5 순서가 유지되었다.
- [x] 원본 채점 기준 표가 유지되었다.
- [x] 원본 optimizer 구현 과제에서 library optimizer를 사용하지 않았다.
- [x] MyAdam.step은 t 증가 후 parent step을 호출한다.
- [x] 모든 optimizer update는 in-place다.
- [x] test_xor가 실행된다.
- [x] Part 2 `results`가 원본 plot cell에서 작동한다.
- [x] Part 3 `mnist_results`가 원본 plot cell에서 작동한다.
- [x] Part 4 `sgd_accs`, `adam_accs`가 원본 plot cell에서 작동한다.
- [x] Part 5 질문 4개가 유지되었다.
- [x] 삽입 cell은 `[INSERTED]` prefix를 가진다.
- [x] 삽입 cell이 원본 공식 결과를 대체하지 않는다.
- [x] Virtual 3D optimizer contour analysis는 original cell 수정이 아니라 새 inserted cell로 들어갔다.
- [x] inserted code cell에는 교육용 주석 헤더가 들어갔고 original code cell은 SSOT로 보존했다.
- [x] fresh kernel로 처음부터 끝까지 실행된다.
- [x] 최종 보고서가 생성되었다.
