# 20260529_14 개념노드인덱스

| 항목 | 값 |
|------|----|
| lecture_id | `20260529_14` |
| node_count | 16 |
| edge_count | 15 |
| evidence_count | 31 |

## Nodes

### `n_ML14.section_01` — 왜 데이터 프로세싱을 먼저 보는가

- status: `supported_md_primary`
- anchor_ids: `ML14.A.5`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML14.boston_housing`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.boston_housing` — Boston Housing 문제 정의

- status: `supported_md_primary`
- anchor_ids: `ML14.A.6`
- segment_ids: `ML14.A.6.local_001`
- aliases: `Boston`, `Housing`
- evidence_count: 2
- outgoing: `n_ML14.section_03`
- incoming: `n_ML14.section_01`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.section_03` — `load_boston()` 객체 해부

- status: `supported_md_primary`
- anchor_ids: `ML14.A.7`
- segment_ids: `ML14.A.7.local_001`
- aliases: `load_boston`
- evidence_count: 2
- outgoing: `n_ML14.dataframe`
- incoming: `n_ML14.boston_housing`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.dataframe` — DataFrame으로 바꾸는 이유

- status: `supported_md_primary`
- anchor_ids: `ML14.A.8`
- segment_ids: `ML14.A.8.local_001`
- aliases: `DataFrame`
- evidence_count: 2
- outgoing: `n_ML14.eda`
- incoming: `n_ML14.section_03`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.eda` — `info()`와 EDA에서 확인할 것

- status: `supported_md_primary`
- anchor_ids: `ML14.A.9`
- segment_ids: `ML14.A.9.local_001`
- aliases: `info`, `EDA`
- evidence_count: 2
- outgoing: `n_ML14.section_06`
- incoming: `n_ML14.dataframe`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.section_06` — `CHAS` 제거와 입력 차원 12

- status: `supported_md_primary`
- anchor_ids: `ML14.A.11`
- segment_ids: `ML14.A.11.local_001`
- aliases: `CHAS`
- evidence_count: 2
- outgoing: `n_ML14.train_test_split`
- incoming: `n_ML14.eda`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.train_test_split` — train/test split의 의미

- status: `supported_md_primary`
- anchor_ids: `ML14.A.12`
- segment_ids: `ML14.A.12.local_001`
- aliases: `train`, `test`, `split`
- evidence_count: 2
- outgoing: `n_ML14.minmax_scaling`
- incoming: `n_ML14.section_06`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.minmax_scaling` — MinMax scaling: X와 y를 따로 정규화

- status: `supported_md_primary`
- anchor_ids: `ML14.A.13`
- segment_ids: `ML14.A.13.local_001`
- aliases: `MinMax`, `scaling`
- evidence_count: 2
- outgoing: `n_ML14.shape`
- incoming: `n_ML14.train_test_split`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.shape` — shape 체크: 모델에 들어가는 네 개의 배열

- status: `supported_md_primary`
- anchor_ids: `ML14.A.17`
- segment_ids: `ML14.A.17.local_001`
- aliases: `shape`
- evidence_count: 2
- outgoing: `n_ML14.modeling_training`
- incoming: `n_ML14.minmax_scaling`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.modeling_training` — Modeling(training): 함수 구조를 정한다

- status: `supported_md_primary`
- anchor_ids: `ML14.A.18`
- segment_ids: `ML14.A.18.local_001`
- aliases: `Modeling`, `training`
- evidence_count: 2
- outgoing: `n_ML14.section_11`
- incoming: `n_ML14.shape`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.section_11` — `compile`과 `fit`: 학습 기준과 반복 실행

- status: `supported_md_primary`
- anchor_ids: `ML14.A.27`
- segment_ids: `ML14.A.27.local_001`
- aliases: `compile`, `fit`
- evidence_count: 2
- outgoing: `n_ML14.section_12`
- incoming: `n_ML14.modeling_training`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.section_12` — 학습 곡선 해석

- status: `supported_md_primary`
- anchor_ids: `ML14.A.31`
- segment_ids: `ML14.A.31.local_001`
- evidence_count: 2
- outgoing: `n_ML14.validation_test`
- incoming: `n_ML14.section_11`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.validation_test` — Validation(test): 처음 보는 데이터에서 확인한다

- status: `supported_md_primary`
- anchor_ids: `ML14.A.36`
- segment_ids: `ML14.A.36.local_001`
- aliases: `Validation`, `test`
- evidence_count: 2
- outgoing: `n_ML14.mae`
- incoming: `n_ML14.section_12`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.mae` — 원래 단위 MAE와 예측 산점도

- status: `supported_md_primary`
- anchor_ids: `ML14.A.40`
- segment_ids: `ML14.A.40.local_001`
- aliases: `MAE`
- evidence_count: 2
- outgoing: `n_ML14.mnist`
- incoming: `n_ML14.validation_test`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.mnist` — MNIST 분류와의 검증 비교

- status: `supported_md_primary`
- anchor_ids: `ML14.A.44`
- segment_ids: `ML14.A.44.local_001`
- aliases: `MNIST`
- evidence_count: 2
- outgoing: `n_ML14.section_16`
- incoming: `n_ML14.mae`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML14.section_16` — 오늘의 핵심 정리

- status: `supported_md_primary`
- anchor_ids: `ML14.A.45`
- segment_ids: `ML14.A.45.local_001`
- evidence_count: 2
- incoming: `n_ML14.mnist`
- notes: Generated from numbered main heading and aligned transcript segment.
