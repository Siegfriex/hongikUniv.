# 20260430_8 개념노드인덱스

| 항목 | 값 |
|------|----|
| lecture_id | `20260430_8` |
| node_count | 24 |
| edge_count | 23 |
| evidence_count | 45 |

## Nodes

### `n_ML8.section_01` — 전체 개념 그래프

- status: `supported_md_primary`
- anchor_ids: `ML8.A.5`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML8.feature_engineering`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.feature_engineering` — 지금까지 모델의 공통 한계: feature engineering

- status: `supported_md_primary`
- anchor_ids: `ML8.A.9`
- segment_ids: `ML8.A.9.local_001`
- aliases: `feature`, `engineering`
- evidence_count: 2
- outgoing: `n_ML8.section_03`
- incoming: `n_ML8.section_01`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.section_03` — 생물 뉴런에서 인공 뉴런으로

- status: `supported_md_primary`
- anchor_ids: `ML8.A.13`
- segment_ids: `ML8.A.13.local_001`
- evidence_count: 2
- outgoing: `n_ML8.perceptron`
- incoming: `n_ML8.feature_engineering`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.perceptron` — Perceptron: 인공 뉴런 1개

- status: `supported_md_primary`
- anchor_ids: `ML8.A.17`
- segment_ids: `ML8.A.17.local_001`
- aliases: `Perceptron`
- evidence_count: 2
- outgoing: `n_ML8.deep_neural_network`
- incoming: `n_ML8.section_03`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.deep_neural_network` — Deep Neural Network: 층을 깊게 쌓는 이유

- status: `supported_md_primary`
- anchor_ids: `ML8.A.21`
- segment_ids: `ML8.A.21.local_001`
- aliases: `Deep`, `Neural`, `Network`
- evidence_count: 2
- outgoing: `n_ML8.neural_network`
- incoming: `n_ML8.perceptron`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.neural_network` — Neural Network가 바꾼 분야

- status: `supported_md_primary`
- anchor_ids: `ML8.A.26`
- segment_ids: `ML8.A.26.local_001`
- aliases: `Neural`, `Network`
- evidence_count: 2
- outgoing: `n_ML8.neural_network_a029`
- incoming: `n_ML8.deep_neural_network`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.neural_network_a029` — Neural Network의 핵심 3요소

- status: `supported_md_primary`
- anchor_ids: `ML8.A.29`
- segment_ids: `ML8.A.29.local_001`
- aliases: `Neural`, `Network`
- evidence_count: 2
- outgoing: `n_ML8.forward_loss_backward_update`
- incoming: `n_ML8.neural_network`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.forward_loss_backward_update` — 학습 루프: Forward, Loss, Backward, Update

- status: `supported_md_primary`
- anchor_ids: `ML8.A.34`
- segment_ids: `ML8.A.34.local_001`
- aliases: `Forward`, `Loss`, `Backward`, `Update`
- evidence_count: 2
- outgoing: `n_ML8.perceptron_a038`
- incoming: `n_ML8.neural_network_a029`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.perceptron_a038` — Perceptron은 선형 분류기다

- status: `supported_md_primary`
- anchor_ids: `ML8.A.38`
- segment_ids: `ML8.A.38.local_001`
- aliases: `Perceptron`
- evidence_count: 2
- outgoing: `n_ML8.and_or_nand_xor`
- incoming: `n_ML8.forward_loss_backward_update`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.and_or_nand_xor` — AND, OR, NAND, XOR와 선형 분리

- status: `supported_md_primary`
- anchor_ids: `ML8.A.42`
- segment_ids: `ML8.A.42.local_001`
- aliases: `AND`, `OR`, `NAND`, `XOR`
- evidence_count: 2
- outgoing: `n_ML8.perceptron_a047`
- incoming: `n_ML8.perceptron_a038`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.perceptron_a047` — Perceptron 학습 규칙

- status: `supported_md_primary`
- anchor_ids: `ML8.A.47`
- segment_ids: `ML8.A.47.local_001`
- aliases: `Perceptron`
- evidence_count: 2
- outgoing: `n_ML8.xor`
- incoming: `n_ML8.and_or_nand_xor`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.xor` — XOR의 한계와 모순 증명

- status: `supported_md_primary`
- anchor_ids: `ML8.A.51`
- segment_ids: `ML8.A.51.local_001`
- aliases: `XOR`
- evidence_count: 2
- outgoing: `n_ML8.mlp_xor`
- incoming: `n_ML8.perceptron_a047`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.mlp_xor` — MLP: 뉴런 조합으로 XOR 해결

- status: `supported_md_primary`
- anchor_ids: `ML8.A.56`
- segment_ids: `ML8.A.56.local_001`
- aliases: `MLP`, `XOR`
- evidence_count: 2
- outgoing: `n_ML8.notation`
- incoming: `n_ML8.xor`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.notation` — Notation: 앞으로 사용할 표기법

- status: `supported_md_primary`
- anchor_ids: `ML8.A.62`
- segment_ids: `ML8.A.62.local_001`
- aliases: `Notation`
- evidence_count: 2
- outgoing: `n_ML8.section_15`
- incoming: `n_ML8.mlp_xor`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.section_15` — 왜 비선형 활성화가 필요한가

- status: `supported_md_primary`
- anchor_ids: `ML8.A.67`
- segment_ids: `ML8.A.67.local_001`
- evidence_count: 2
- outgoing: `n_ML8.section_16`
- incoming: `n_ML8.notation`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.section_16` — 수업 체크포인트

- status: `supported_md_primary`
- anchor_ids: `ML8.A.71`
- segment_ids: `ML8.A.71.local_001`
- evidence_count: 2
- outgoing: `n_ML8.perceptron_a075`
- incoming: `n_ML8.section_15`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.perceptron_a075` — 심화 브리지: 선형회귀에서 Perceptron으로

- status: `supported_md_primary`
- anchor_ids: `ML8.A.75`
- segment_ids: `ML8.A.75.local_001`
- aliases: `Perceptron`
- evidence_count: 2
- outgoing: `n_ML8.hidden_layer`
- incoming: `n_ML8.section_16`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.hidden_layer` — Hidden layer는 무엇을 대신하는가

- status: `supported_md_primary`
- anchor_ids: `ML8.A.79`
- segment_ids: `ML8.A.79.local_001`
- aliases: `Hidden`, `layer`
- evidence_count: 2
- outgoing: `n_ML8.section_19`
- incoming: `n_ML8.perceptron_a075`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.section_19` — 순전파, 역전파, 체인룰

- status: `supported_md_primary`
- anchor_ids: `ML8.A.84`
- segment_ids: `ML8.A.84.local_001`
- evidence_count: 2
- outgoing: `n_ML8.section_20`
- incoming: `n_ML8.hidden_layer`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.section_20` — 순전파 기반 탐색과 역전파는 어떻게 다른가

- status: `supported_md_primary`
- anchor_ids: `ML8.A.89`
- segment_ids: `ML8.A.89.local_001`
- evidence_count: 2
- outgoing: `n_ML8.section_21`
- incoming: `n_ML8.section_19`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.section_21` — 역전파와 탐색은 보완 가능한가

- status: `supported_md_primary`
- anchor_ids: `ML8.A.94`
- segment_ids: `ML8.A.94.local_001`
- evidence_count: 2
- outgoing: `n_ML8.section_22`
- incoming: `n_ML8.section_20`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.section_22` — 이미지 전문가 라벨 예시: 왜 신경망을 쓰는가

- status: `supported_md_primary`
- anchor_ids: `ML8.A.98`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML8.section_23`
- incoming: `n_ML8.section_21`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.section_23` — 최종 개념 지도

- status: `supported_md_primary`
- anchor_ids: `ML8.A.105`
- segment_ids: `ML8.A.105.local_001`
- evidence_count: 2
- outgoing: `n_ML8.section_24`
- incoming: `n_ML8.section_22`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML8.section_24` — 최종 보강: 오늘 헷갈린 지점 총정리

- status: `supported_md_primary`
- anchor_ids: `ML8.A.109`
- segment_ids:
- evidence_count: 1
- incoming: `n_ML8.section_23`
- notes: Generated from numbered main heading and aligned transcript segment.
