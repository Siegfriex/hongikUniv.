# 20260507_10 개념노드인덱스

| 항목 | 값 |
|------|----|
| lecture_id | `20260507_10` |
| node_count | 8 |
| edge_count | 7 |
| evidence_count | 16 |

## Nodes

### `n_ML10.section_01` — 강의 개요

- status: `supported_md_primary`
- anchor_ids: `ML10.A.4`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML10.section_02`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML10.section_02` — 미분 복습

- status: `supported_md_primary`
- anchor_ids: `ML10.A.12`
- segment_ids: `ML10.A.12.local_001`
- evidence_count: 2
- outgoing: `n_ML10.section_03`
- incoming: `n_ML10.section_01`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML10.section_03` — 편미분과 그래디언트

- status: `supported_md_primary`
- anchor_ids: `ML10.A.28`
- segment_ids: `ML10.A.28.local_001`
- evidence_count: 2
- outgoing: `n_ML10.chain_rule`
- incoming: `n_ML10.section_02`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML10.chain_rule` — Chain Rule

- status: `supported_md_primary`
- anchor_ids: `ML10.A.52`
- segment_ids: `ML10.A.52.local_001`
- aliases: `Chain`, `Rule`
- evidence_count: 2
- outgoing: `n_ML10.sigmoid`
- incoming: `n_ML10.section_03`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML10.sigmoid` — Sigmoid 미분

- status: `supported_md_primary`
- anchor_ids: `ML10.A.66`
- segment_ids: `ML10.A.66.local_001`
- aliases: `Sigmoid`
- evidence_count: 2
- outgoing: `n_ML10.gradient_descent`
- incoming: `n_ML10.chain_rule`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML10.gradient_descent` — Gradient Descent

- status: `supported_md_primary`
- anchor_ids: `ML10.A.76`
- segment_ids: `ML10.A.76.local_001`
- aliases: `Gradient`, `Descent`
- evidence_count: 2
- outgoing: `n_ML10.backprop`
- incoming: `n_ML10.sigmoid`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML10.backprop` — 신경망/Backprop과의 연결

- status: `supported_md_primary`
- anchor_ids: `ML10.A.87`
- segment_ids: `ML10.A.87.local_001`
- aliases: `Backprop`
- evidence_count: 2
- outgoing: `n_ML10.section_08`
- incoming: `n_ML10.gradient_descent`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML10.section_08` — 정리 및 연습 아이디어

- status: `supported_md_primary`
- anchor_ids: `ML10.A.98`
- segment_ids: `ML10.A.98.local_001`, `ML10.A.98.local_002`
- evidence_count: 3
- incoming: `n_ML10.backprop`
- notes: Generated from numbered main heading and aligned transcript segment.
