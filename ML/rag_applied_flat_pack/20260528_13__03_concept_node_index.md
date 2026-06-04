# 20260528_13 개념노드인덱스

| 항목 | 값 |
|------|----|
| lecture_id | `20260528_13` |
| node_count | 11 |
| edge_count | 10 |
| evidence_count | 20 |

## Nodes

### `n_ML13.deep_neural_network` — Deep Neural Network의 의미

- status: `supported_md_primary`
- anchor_ids: `ML13.A.10`
- segment_ids:
- aliases: `Deep`, `Neural`, `Network`
- evidence_count: 1
- outgoing: `n_ML13.section_02`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.section_02` — 12강 코드에서 13강 코드로: 책임 분리

- status: `supported_md_primary`
- anchor_ids: `ML13.A.11`
- segment_ids: `ML13.A.11.local_001`
- evidence_count: 2
- outgoing: `n_ML13.optimizer`
- incoming: `n_ML13.deep_neural_network`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.optimizer` — Optimizer가 필요한 이유

- status: `supported_md_primary`
- anchor_ids: `ML13.A.12`
- segment_ids: `ML13.A.12.local_001`
- aliases: `Optimizer`
- evidence_count: 2
- outgoing: `n_ML13.sgd_momentum_rmsprop_adam`
- incoming: `n_ML13.section_02`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.sgd_momentum_rmsprop_adam` — SGD, Momentum, RMSProp, Adam

- status: `supported_md_primary`
- anchor_ids: `ML13.A.13`
- segment_ids: `ML13.A.13.local_001`
- aliases: `SGD`, `Momentum`, `RMSProp`, `Adam`
- evidence_count: 2
- outgoing: `n_ML13.keras`
- incoming: `n_ML13.optimizer`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.keras` — Keras 모델링의 공통 절차

- status: `supported_md_primary`
- anchor_ids: `ML13.A.19`
- segment_ids: `ML13.A.19.local_001`
- aliases: `Keras`
- evidence_count: 2
- outgoing: `n_ML13.dnn`
- incoming: `n_ML13.sgd_momentum_rmsprop_adam`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.dnn` — DNN 회귀: 주택 가격 예측

- status: `supported_md_primary`
- anchor_ids: `ML13.A.20`
- segment_ids: `ML13.A.20.local_001`
- aliases: `DNN`
- evidence_count: 2
- outgoing: `n_ML13.section_07`
- incoming: `n_ML13.keras`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.section_07` — 회귀 모델 구조와 손실 함수

- status: `supported_md_primary`
- anchor_ids: `ML13.A.21`
- segment_ids: `ML13.A.21.local_001`
- evidence_count: 2
- outgoing: `n_ML13.dnn_a022`
- incoming: `n_ML13.dnn`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.dnn_a022` — DNN 분류: 손글씨 숫자 인식

- status: `supported_md_primary`
- anchor_ids: `ML13.A.22`
- segment_ids: `ML13.A.22.local_001`
- aliases: `DNN`
- evidence_count: 2
- outgoing: `n_ML13.softmax_cross_entropy`
- incoming: `n_ML13.section_07`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.softmax_cross_entropy` — Softmax와 Cross Entropy

- status: `supported_md_primary`
- anchor_ids: `ML13.A.23`
- segment_ids: `ML13.A.23.local_001`
- aliases: `Softmax`, `Cross`, `Entropy`
- evidence_count: 2
- outgoing: `n_ML13.section_10`
- incoming: `n_ML13.dnn_a022`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.section_10` — 학습 곡선, 검증, 과적합

- status: `supported_md_primary`
- anchor_ids: `ML13.A.24`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML13.section_11`
- incoming: `n_ML13.softmax_cross_entropy`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML13.section_11` — 오늘의 핵심 정리

- status: `supported_md_primary`
- anchor_ids: `ML13.A.25`
- segment_ids: `ML13.A.25.local_001`
- evidence_count: 2
- incoming: `n_ML13.section_10`
- notes: Generated from numbered main heading and aligned transcript segment.
