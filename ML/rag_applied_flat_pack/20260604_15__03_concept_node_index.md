# 20260604_15 개념노드인덱스

| 항목 | 값 |
|------|----|
| lecture_id | `20260604_15` |
| node_count | 23 |
| edge_count | 22 |
| evidence_count | 40 |

## Nodes

### `n_ML15.section_01` — 직전 강의에서 오늘 강의로 넘어가는 이유

- status: `supported_md_primary`
- anchor_ids: `ML15.A.5`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML15.leakage`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.leakage` — 전처리 표준 1: 결측치 처리와 leakage

- status: `supported_md_primary`
- anchor_ids: `ML15.A.6`
- segment_ids:
- aliases: `leakage`
- evidence_count: 1
- outgoing: `n_ML15.section_03`
- incoming: `n_ML15.section_01`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.section_03` — 전처리 표준 2: 수치형 정규화

- status: `supported_md_primary`
- anchor_ids: `ML15.A.7`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML15.section_04`
- incoming: `n_ML15.leakage`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.section_04` — 전처리 표준 3: 범주형 인코딩

- status: `supported_md_primary`
- anchor_ids: `ML15.A.8`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML15.section_05`
- incoming: `n_ML15.section_03`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.section_05` — 전처리 표준 4: 시간 변수 처리

- status: `supported_md_primary`
- anchor_ids: `ML15.A.11`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML15.train_validation_test`
- incoming: `n_ML15.section_04`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.train_validation_test` — Train / Validation / Test 3분할

- status: `supported_md_primary`
- anchor_ids: `ML15.A.12`
- segment_ids:
- aliases: `Train`, `Validation`, `Test`
- evidence_count: 1
- outgoing: `n_ML15.section_07`
- incoming: `n_ML15.section_05`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.section_07` — 과적합, 과소적합, 좋은 적합

- status: `supported_md_primary`
- anchor_ids: `ML15.A.13`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML15.loss_curve`
- incoming: `n_ML15.train_validation_test`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.loss_curve` — Loss curve로 진단하기

- status: `supported_md_primary`
- anchor_ids: `ML15.A.14`
- segment_ids:
- aliases: `Loss`, `curve`
- evidence_count: 1
- outgoing: `n_ML15.section_09`
- incoming: `n_ML15.section_07`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.section_09` — 일부러 과적합을 만들어보는 실험 습관

- status: `supported_md_primary`
- anchor_ids: `ML15.A.15`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML15.dropout`
- incoming: `n_ML15.loss_curve`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.dropout` — 정규화 도구 1: Dropout

- status: `supported_md_primary`
- anchor_ids: `ML15.A.16`
- segment_ids:
- aliases: `Dropout`
- evidence_count: 1
- outgoing: `n_ML15.l2_regularization`
- incoming: `n_ML15.section_09`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.l2_regularization` — 정규화 도구 2: L2 Regularization

- status: `supported_md_primary`
- anchor_ids: `ML15.A.17`
- segment_ids:
- aliases: `L2`, `Regularization`
- evidence_count: 1
- outgoing: `n_ML15.early_stopping`
- incoming: `n_ML15.dropout`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.early_stopping` — 정규화 도구 3: Early Stopping

- status: `supported_md_primary`
- anchor_ids: `ML15.A.18`
- segment_ids:
- aliases: `Early`, `Stopping`
- evidence_count: 1
- outgoing: `n_ML15.batch_normalization`
- incoming: `n_ML15.l2_regularization`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.batch_normalization` — 정규화 도구 4: Batch Normalization

- status: `supported_md_primary`
- anchor_ids: `ML15.A.19`
- segment_ids:
- aliases: `Batch`, `Normalization`
- evidence_count: 1
- outgoing: `n_ML15.baseline_vs_regularized`
- incoming: `n_ML15.early_stopping`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.baseline_vs_regularized` — 종합 실습: baseline vs regularized

- status: `supported_md_primary`
- anchor_ids: `ML15.A.20`
- segment_ids:
- aliases: `baseline`, `vs`, `regularized`
- evidence_count: 1
- outgoing: `n_ML15.cnn`
- incoming: `n_ML15.batch_normalization`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.cnn` — 왜 이미지에는 CNN이 필요한가

- status: `supported_md_primary`
- anchor_ids: `ML15.A.26`
- segment_ids:
- aliases: `CNN`
- evidence_count: 1
- outgoing: `n_ML15.receptive_field_filter`
- incoming: `n_ML15.baseline_vs_regularized`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.receptive_field_filter` — Receptive field와 filter

- status: `supported_md_primary`
- anchor_ids: `ML15.A.27`
- segment_ids:
- aliases: `Receptive`, `field`, `filter`
- evidence_count: 1
- outgoing: `n_ML15.convolution_layer`
- incoming: `n_ML15.cnn`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.convolution_layer` — Convolution layer의 구성 요소

- status: `supported_md_primary`
- anchor_ids: `ML15.A.28`
- segment_ids: `ML15.A.28.local_001`
- aliases: `Convolution`, `layer`
- evidence_count: 2
- outgoing: `n_ML15.channel_kernel`
- incoming: `n_ML15.receptive_field_filter`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.channel_kernel` — 다중 channel과 다중 kernel

- status: `supported_md_primary`
- anchor_ids: `ML15.A.29`
- segment_ids: `ML15.A.29.local_001`, `ML15.A.29.local_002`
- aliases: `channel`, `kernel`
- evidence_count: 3
- outgoing: `n_ML15.padding_stride_pooling`
- incoming: `n_ML15.convolution_layer`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.padding_stride_pooling` — Padding, stride, pooling

- status: `supported_md_primary`
- anchor_ids: `ML15.A.30`
- segment_ids: `ML15.A.30.local_001`, `ML15.A.30.local_002`, `ML15.A.30.local_003`, `ML15.A.30.local_004`
- aliases: `Padding`, `stride`, `pooling`
- evidence_count: 5
- outgoing: `n_ML15.cnn_classifier_conv_pool_flatten`
- incoming: `n_ML15.channel_kernel`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.cnn_classifier_conv_pool_flatten` — CNN에서 classifier까지: Conv -> Pool -> Flatten -> Dense

- status: `supported_md_primary`
- anchor_ids: `ML15.A.34`
- segment_ids: `ML15.A.34.local_001`
- aliases: `CNN`, `classifier`, `Conv`, `Pool`, `Flatten`, `Dense`
- evidence_count: 2
- outgoing: `n_ML15.fashion_mnist_dense_baseline_vs`
- incoming: `n_ML15.padding_stride_pooling`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.fashion_mnist_dense_baseline_vs` — Fashion-MNIST 보충 실습: Dense baseline vs CNN

- status: `supported_md_primary`
- anchor_ids: `ML15.A.35`
- segment_ids: `ML15.A.35.local_001`
- aliases: `Fashion-MNIST`, `Dense`, `baseline`, `vs`, `CNN`
- evidence_count: 2
- outgoing: `n_ML15.imagenet_cnn`
- incoming: `n_ML15.cnn_classifier_conv_pool_flatten`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.imagenet_cnn` — ImageNet과 CNN 모델 계보

- status: `supported_md_primary`
- anchor_ids: `ML15.A.41`
- segment_ids: `ML15.A.41.local_001`, `ML15.A.41.local_002`, `ML15.A.41.local_003`, `ML15.A.41.local_004`
- aliases: `ImageNet`, `CNN`
- evidence_count: 5
- outgoing: `n_ML15.section_23`
- incoming: `n_ML15.fashion_mnist_dense_baseline_vs`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML15.section_23` — 오늘의 핵심 정리

- status: `supported_md_primary`
- anchor_ids: `ML15.A.42`
- segment_ids: `ML15.A.42.local_001`, `ML15.A.42.local_002`, `ML15.A.42.local_003`, `ML15.A.42.local_005`
- evidence_count: 5
- incoming: `n_ML15.imagenet_cnn`
- notes: Generated from numbered main heading and aligned transcript segment.
