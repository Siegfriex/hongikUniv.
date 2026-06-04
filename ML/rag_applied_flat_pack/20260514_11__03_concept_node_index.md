# 20260514_11 개념노드인덱스

| 항목 | 값 |
|------|----|
| lecture_id | `20260514_11` |
| node_count | 17 |
| edge_count | 16 |
| evidence_count | 34 |

## Nodes

### `n_ML11.section_01` — 주차 맥락과 코스 연결

- status: `supported_md_primary`
- anchor_ids: `ML11.A.6`
- segment_ids:
- evidence_count: 1
- outgoing: `n_ML11.section_02`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_02` — 2-2-1 네트워크 구조와 표기

- status: `supported_md_primary`
- anchor_ids: `ML11.A.7`
- segment_ids: `ML11.A.7.local_001`
- evidence_count: 2
- outgoing: `n_ML11.forward_pass`
- incoming: `n_ML11.section_01`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.forward_pass` — Forward pass

- status: `supported_md_primary`
- anchor_ids: `ML11.A.8`
- segment_ids: `ML11.A.8.local_001`
- aliases: `Forward`, `pass`
- evidence_count: 2
- outgoing: `n_ML11.section_04`
- incoming: `n_ML11.section_02`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_04` — 공통 숫자·출력 오차·δ의 자리

- status: `supported_md_primary`
- anchor_ids: `ML11.A.9`
- segment_ids: `ML11.A.9.local_001`
- evidence_count: 2
- outgoing: `n_ML11.section_05`
- incoming: `n_ML11.forward_pass`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_05` — 출력층: 짧은 체인

- status: `supported_md_primary`
- anchor_ids: `ML11.A.12`
- segment_ids: `ML11.A.12.local_001`
- evidence_count: 2
- outgoing: `n_ML11.section_06`
- incoming: `n_ML11.section_04`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_06` — 은닉층: 긴 체인과 δ⁽¹⁾

- status: `supported_md_primary`
- anchor_ids: `ML11.A.14`
- segment_ids: `ML11.A.14.local_001`
- evidence_count: 2
- outgoing: `n_ML11.section_07`
- incoming: `n_ML11.section_05`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_07` — 은닉층 6개 편미분 표

- status: `supported_md_primary`
- anchor_ids: `ML11.A.18`
- segment_ids: `ML11.A.18.local_001`
- evidence_count: 2
- outgoing: `n_ML11.forward_vs_backward`
- incoming: `n_ML11.section_06`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.forward_vs_backward` — Forward vs Backward·9개 총정리

- status: `supported_md_primary`
- anchor_ids: `ML11.A.19`
- segment_ids: `ML11.A.19.local_001`
- aliases: `Forward`, `vs`, `Backward`
- evidence_count: 2
- outgoing: `n_ML11.week`
- incoming: `n_ML11.section_07`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.week` — 일반 패턴과 Week 12로의 다리

- status: `supported_md_primary`
- anchor_ids: `ML11.A.20`
- segment_ids: `ML11.A.20.local_001`
- aliases: `Week`
- evidence_count: 2
- outgoing: `n_ML11.section_10`
- incoming: `n_ML11.forward_vs_backward`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_10` — `mlp_scratch.py` 구현 해설

- status: `supported_md_primary`
- anchor_ids: `ML11.A.21`
- segment_ids: `ML11.A.21.local_001`
- aliases: `mlp_scratch`, `py`
- evidence_count: 2
- outgoing: `n_ML11.gradient_check`
- incoming: `n_ML11.week`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.gradient_check` — `train`·gradient check

- status: `supported_md_primary`
- anchor_ids: `ML11.A.26`
- segment_ids: `ML11.A.26.local_001`
- aliases: `train`, `gradient`, `check`
- evidence_count: 2
- outgoing: `n_ML11.xor`
- incoming: `n_ML11.section_10`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.xor` — XOR 자동 학습

- status: `supported_md_primary`
- anchor_ids: `ML11.A.28`
- segment_ids: `ML11.A.28.local_001`
- aliases: `XOR`
- evidence_count: 2
- outgoing: `n_ML11.section_13`
- incoming: `n_ML11.gradient_check`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_13` — 강의 실행: `week11_examples.ipynb`

- status: `supported_md_primary`
- anchor_ids: `ML11.A.29`
- segment_ids: `ML11.A.29.local_001`
- aliases: `week11_examples`, `ipynb`
- evidence_count: 2
- outgoing: `n_ML11.section_14`
- incoming: `n_ML11.xor`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_14` — 부록: 스니펫·손계산 표

- status: `supported_md_primary`
- anchor_ids: `ML11.A.30`
- segment_ids: `ML11.A.30.local_001`
- evidence_count: 2
- outgoing: `n_ML11.html`
- incoming: `n_ML11.section_13`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.html` — 인터랙티브 HTML 보조 자료

- status: `supported_md_primary`
- anchor_ids: `ML11.A.31`
- segment_ids: `ML11.A.31.local_001`
- aliases: `HTML`
- evidence_count: 2
- outgoing: `n_ML11.section_16`
- incoming: `n_ML11.section_14`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_16` — 오늘의 핵심·헷갈림·다음 강의

- status: `supported_md_primary`
- anchor_ids: `ML11.A.32`
- segment_ids: `ML11.A.32.local_001`
- evidence_count: 2
- outgoing: `n_ML11.section_17`
- incoming: `n_ML11.html`
- notes: Generated from numbered main heading and aligned transcript segment.

### `n_ML11.section_17` — 편집 변경 요약

- status: `supported_md_primary`
- anchor_ids: `ML11.A.36`
- segment_ids: `ML11.A.36.local_001`, `ML11.A.36.local_002`
- evidence_count: 3
- incoming: `n_ML11.section_16`
- notes: Generated from numbered main heading and aligned transcript segment.
