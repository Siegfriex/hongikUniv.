# 20260521_12 개념노드인덱스

| 항목 | 값 |
|------|----|
| lecture_id | `20260521_12` |
| node_count | 11 |
| edge_count | 10 |
| evidence_count | 22 |

## Nodes

### `n_ML12.backprop` — 직전 복습: 2-2-1 Backprop의 일반 패턴

- status: `supported_md_primary`
- anchor_ids: `ML12.A.6`
- segment_ids:
- aliases: `Backprop`
- evidence_count: 1
- outgoing: `n_ML12.layer_abstraction_activation`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.layer_abstraction_activation` — Layer Abstraction: `Layer`·`Dense`·activation

- status: `supported_md_primary`
- anchor_ids: `ML12.A.7`
- segment_ids: `ML12.A.7.local_001`
- aliases: `Layer`, `Abstraction`, `Layer`, `Dense`, `activation`
- evidence_count: 2
- outgoing: `n_ML12.vectorized_backprop_batch_dimension_matrix`
- incoming: `n_ML12.backprop`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.vectorized_backprop_batch_dimension_matrix` — Vectorized Backprop: batch dimension과 matrix shape

- status: `supported_md_primary`
- anchor_ids: `ML12.A.13`
- segment_ids: `ML12.A.13.local_001`
- aliases: `Vectorized`, `Backprop`, `batch`, `dimension`, `matrix`, `shape`
- evidence_count: 2
- outgoing: `n_ML12.network_mini_batch`
- incoming: `n_ML12.layer_abstraction_activation`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.network_mini_batch` — Network 조립과 mini-batch 학습

- status: `supported_md_primary`
- anchor_ids: `ML12.A.14`
- segment_ids: `ML12.A.14.local_001`
- aliases: `Network`, `mini-batch`
- evidence_count: 2
- outgoing: `n_ML12.xor_vanishing_gradient_iris_mnist`
- incoming: `n_ML12.vectorized_backprop_batch_dimension_matrix`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.xor_vanishing_gradient_iris_mnist` — 실험 흐름: XOR·Vanishing Gradient·Iris·MNIST

- status: `supported_md_primary`
- anchor_ids: `ML12.A.18`
- segment_ids: `ML12.A.18.local_001`
- aliases: `XOR`, `Vanishing`, `Gradient`, `Iris`, `MNIST`
- evidence_count: 2
- outgoing: `n_ML12.gradient`
- incoming: `n_ML12.network_mini_batch`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.gradient` — 분류와 회귀: 출력층·손실·gradient 선택

- status: `supported_md_primary`
- anchor_ids: `ML12.A.22`
- segment_ids: `ML12.A.22.local_001`
- aliases: `gradient`
- evidence_count: 2
- outgoing: `n_ML12.keras`
- incoming: `n_ML12.xor_vanishing_gradient_iris_mnist`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.keras` — Keras와의 일대일 대응

- status: `supported_md_primary`
- anchor_ids: `ML12.A.27`
- segment_ids: `ML12.A.27.local_001`
- aliases: `Keras`
- evidence_count: 2
- outgoing: `n_ML12.layer`
- incoming: `n_ML12.gradient`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.layer` — 구현 포인터: 기존 `mlp_scratch.py`에서 일반 Layer로

- status: `supported_md_primary`
- anchor_ids: `ML12.A.28`
- segment_ids: `ML12.A.28.local_001`
- aliases: `mlp_scratch`, `py`, `Layer`
- evidence_count: 2
- outgoing: `n_ML12.section_09`
- incoming: `n_ML12.keras`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.section_09` — 오늘의 핵심·헷갈림·다음 연결

- status: `supported_md_primary`
- anchor_ids: `ML12.A.29`
- segment_ids: `ML12.A.29.local_001`
- evidence_count: 2
- outgoing: `n_ML12.section_10`
- incoming: `n_ML12.layer`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.section_10` — 노트북 인텔리전스 브리핑

- status: `supported_md_primary`
- anchor_ids: `ML12.A.33`
- segment_ids: `ML12.A.33.local_001`
- evidence_count: 2
- outgoing: `n_ML12.section_11`
- incoming: `n_ML12.section_09`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML12.section_11` — 노트북 전체 인용 워크스루

- status: `supported_md_primary`
- anchor_ids: `ML12.A.34`
- segment_ids: `ML12.A.34.local_001`, `ML12.A.34.local_002`
- evidence_count: 3
- incoming: `n_ML12.section_10`
- notes: Generated from numbered main heading and aligned transcript segment.
