# ML 8-15강 인벤토리·RAG 산출물 검증 플랜

## 0. 목적

이 문서는 `ML/final_brief/*.md`와 `ML/final_record/*.txt`에서 생성한 8-15강 인벤토리 산출물을 원문·로데이터 기준으로 재검증하기 위한 실행 계획이다.

검증 대상은 다음 네 계층이다.

| 계층 | 검증 질문 |
|------|-----------|
| 원문 보존 | `final_brief`, `final_record`, `raw/` mirror가 변경 없이 보존됐는가? |
| 구조화 | `anchors_md.json`, `nodes.json`, `edges.json`이 강의록 heading과 실제 개념 흐름을 반영하는가? |
| 전사 정렬 | `segments.jsonl`, `alignments.jsonl`, `evidence.jsonl`, annotated transcript가 전사 줄과 의미를 정확히 잇는가? |
| 파생물 | `*_래그.md`, `*_로데이터디벨롭.md`, DOCX가 sidecar id만 쓰며 고스트 id 없이 검색 가능하게 구성됐는가? |

## 1. 현재 자동 검증 스냅샷

| lecture_id | anchors | nodes | segments | evidence | 자동 검증 |
|------------|--------:|------:|---------:|---------:|-----------|
| `20260430_8` | 118 | 24 | 23 | 45 | EXPORT OK |
| `20260507_10` | 103 | 8 | 9 | 16 | EXPORT OK |
| `20260514_11` | 36 | 17 | 18 | 34 | EXPORT OK |
| `20260521_12` | 60 | 11 | 12 | 22 | EXPORT OK |
| `20260528_13` | 29 | 11 | 12 | 20 | EXPORT OK |
| `20260529_14` | 50 | 16 | 16 | 31 | EXPORT OK |
| `20260604_15` | 42 | 23 | 21 | 43 | EXPORT OK |

자동 검증은 id 무결성, line range, ghost id, DOCX 생성 여부를 본다. 아래 플랜은 이 위에 원문 의미 정합성을 얹는 검증이다.

## 2. 공통 검증 절차

### 2.1 원문 보존 검증

각 강마다 다음을 수행한다.

```bash
cmp -s ML/final_brief/<brief>.md ML/<YYYYMMDD>_<N>강.md
cmp -s ML/final_brief/<brief>.md ML/_inventory/<lecture_id>/raw/<YYYYMMDD>_<N>강.md
cmp -s ML/final_record/<record>.txt ML/<YYYYMMDD>_<N>강_강의록.txt
cmp -s ML/final_record/<record>.txt ML/_inventory/<lecture_id>/raw/<YYYYMMDD>_<N>강_강의록.txt
```

단, 루트 `ML/<YYYYMMDD>_<N>강.md`는 RAG marker index가 insert-only로 추가되어 있을 수 있으므로 `cmp`가 실패하면 다음 대체 검증을 한다.

```bash
python3 - <<'PY'
from pathlib import Path
src = Path("ML/final_brief/<brief>.md").read_text(encoding="utf-8-sig")
ssot = Path("ML/<YYYYMMDD>_<N>강.md").read_text(encoding="utf-8")
body = ssot.split("\\n---\\n\\n<!-- INVENTORY_MARKERS:<lecture_id> -->")[0]
print("OK" if body.strip() == src.strip() else "FAIL")
PY
```

판정 기준:
- `final_brief` 원문 본문 삭제/재작성 0건
- `final_record` 원문 줄 삭제/재배치 0건
- raw mirror는 bootstrap 이후 무표기 상태 유지

### 2.2 Heading-anchor 1:1 검증

각 `ML/<YYYYMMDD>_<N>강.md`에서 marker block 이전의 heading 수와 `anchors_md.json.anchors[]` 수를 비교한다.

검증 포인트:
- `anchor_label_raw`가 원문 heading과 동일한가
- `source_line`이 실제 heading 줄인가
- marker index heading이 anchor로 다시 들어가지 않았는가

허용:
- code fence 내부의 `#`는 heading으로 세지 않는다.

### 2.3 Node 의미 검증

각 강의 `nodes.json`에서 최소 다음 샘플을 직접 대조한다.

| 샘플 | 검증 방법 |
|------|-----------|
| 첫 노드 | 강의 도입 핵심을 잡는가 |
| 중간 노드 2개 | 전사 segment와 강의록 section이 같은 개념을 말하는가 |
| 마지막 노드 | 강의 결론/다음 강의 연결을 반영하는가 |
| `supported_md_primary` 노드 | md evidence가 실제 정의·표·공식 밀집 구간인가 |

판정 기준:
- node label이 heading 제목 복붙만으로 부족하면 사람이 이해 가능한 한글 개념 라벨로 보강 필요
- 같은 node_id가 서로 다른 의미의 절에 중복 사용되면 fail
- cross-lecture edge는 상대 강 `nodes.json` 실존 id 없이는 만들지 않는다

### 2.4 Segment-line 검증

각 강마다 `segments.jsonl`에서 다음을 확인한다.

| 검증 | 기준 |
|------|------|
| 줄 범위 | `source_line_start <= source_line_end`, 전사 총 줄 수 안에 있음 |
| 원문 텍스트 | `text_raw`가 전사 해당 줄 범위와 byte-level 동일 |
| type | 행정/휴식/잡담은 `admin`, 본 강의는 `lecture_core`, 코드 설명은 필요 시 `code_demo` |
| local_seq | 같은 `section_id` 안에서 `001, 002, ...` 단조 증가 |

전사 정렬은 자동 균등 분할 기반이므로 의미 전환점 QA가 가장 중요하다. 수동 QA 시에는 각 segment의 시작/끝 2줄을 읽고, 앞뒤 segment와 개념이 끊기는지 확인한다.

### 2.5 Evidence 검증

각 node별로 다음을 확인한다.

| 검증 | 기준 |
|------|------|
| 1 evidence = 1 source | transcript와 md 문장을 한 evidence에 합치지 않음 |
| `ref.file` | manifest source path와 일치 |
| `ref.lines` | 실제 줄 범위 안에 있음 |
| quote | 해당 줄 범위에서 온 문장이고 핵심 주장을 담음 |
| Rule D | 표·정의·수식 중심 노드는 md-primary evidence가 있음 |

샘플링 기준:
- 강마다 transcript evidence 3개, md evidence 3개 이상 직접 대조
- 긴 강의인 `20260430_8`, `20260604_15`는 각 6개 이상 대조

### 2.6 Annotated transcript 검증

원본 전사와 annotated transcript를 비교한다.

판정 기준:
- 원본 줄 텍스트는 순서대로 모두 존재
- 추가된 줄은 `[[SEG]]`, `[[NODE]]`, `[[EVID]]`, `[[LINES]]` marker line뿐
- marker line의 id는 sidecar에 실재

검증 스크립트 기준:
1. annotated에서 marker line 제거
2. 남은 줄을 SSOT transcript와 비교
3. marker id를 정규식으로 추출해 sidecar id set과 비교

### 2.7 RAG / 로데이터 디벨롭 / DOCX 검증

각 강마다 다음 파일이 있어야 한다.

| 파일 | 검증 |
|------|------|
| `{YYYYMMDD}_{N}강_래그.md` | node/segment/evidence/anchor id가 모두 sidecar 실재 id |
| `{YYYYMMDD}_{N}강_로데이터디벨롭.md` | evidence 줄번호와 quote가 sidecar와 일치 |
| `docx-export/ML/_inventory-derived/<lecture_id>/*.docx` | RAG DOCX 1개, 로데이터 DOCX 1개 |

DOCX 검증은 파일 존재만으로 끝내지 않는다.
- zip 구조가 열리는지 확인
- `word/document.xml`에 해당 lecture_id 또는 강 표기가 들어 있는지 확인
- 용량 0 또는 손상 zip이면 fail

## 3. 강별 집중 검증 포인트

### 3.1 `20260430_8` — Neural Networks, Perceptron, MLP

원문:
- brief: `ML/final_brief/20260430.md`
- transcript: `ML/final_record/기계학습0430.txt`

집중 검증:
- 전사 00:00-31:56의 DNN feature extraction/learning loop가 `feature engineering`, `DNN`, `loss/backprop/GD` 노드로 맞게 나뉘었는가
- 전사 43:12 이후 Perceptron, AND/XOR, MLP, non-linear activation 흐름이 node/edge `leads_to`로 유지되는가
- `XOR` 한계와 `MLP` 해결이 같은 node로 뭉치지 않았는가
- 강의록 말미 `RAG 노드·전사 정렬 마커 인덱스`가 원문 heading anchor로 재수집되지 않았는가

필수 샘플:
- `n_ML8.perceptron`
- `n_ML8.xor`
- `n_ML8.mlp_xor`
- `n_ML8.section_15`

### 3.2 `20260507_10` — Backpropagation 수학 도구

원문:
- brief: `ML/final_brief/20260507.md`
- transcript: `ML/final_record/기계학습0507.txt`

집중 검증:
- 미분, 편미분, gradient, chain rule이 별도 노드로 분리됐는가
- sigmoid 미분과 vanishing gradient 예고가 다음 강의 연결로 잡히는가
- transcript evidence가 수식 설명 구간을 지나치게 넓게 잡지 않았는가

필수 샘플:
- gradient 관련 node
- chain rule 관련 node
- sigmoid derivative 관련 node

### 3.3 `20260514_11` — 2-2-1 MLP Backprop

원문:
- brief: `ML/final_brief/20260514.md`
- transcript: `ML/final_record/0514ml.txt`

집중 검증:
- 출력층 delta와 은닉층 delta가 구분되는가
- `np.outer`, `W2.T`, Hadamard product, shape 설명이 코드 demo segment와 연결되는가
- gradient check와 XOR 자동 학습이 별도 evidence를 갖는가

필수 샘플:
- output layer gradient node
- hidden layer gradient node
- gradient check node
- XOR training node

### 3.4 `20260521_12` — Layer abstraction, vectorized backprop

원문:
- brief: `ML/final_brief/20260521.md`
- transcript: `ML/final_record/0521Ml.txt`

집중 검증:
- `Layer` 계약과 `Dense/ReLU/Sigmoid/Softmax` override가 하나로 뭉치지 않았는가
- vectorized backprop과 batch dimension 설명이 line evidence로 추적되는가
- `Network.add`, forward loop, backward loop, update loop 간선이 순서대로 잡혔는가

필수 샘플:
- Layer abstraction node
- Dense backward node
- vectorized shape node
- Network assembly node

### 3.5 `20260528_13` — Keras DNN, Optimizers

원문:
- brief: `ML/final_brief/20260528.md`
- transcript: `ML/final_record/0528ml.txt`

집중 검증:
- 12강 직접 구현 구조와 Keras `Sequential/Dense/compile/fit/evaluate` 대응이 evidence로 잡혔는가
- optimizer 분리, SGD, Momentum, RMSProp, Adam이 적절한 granular node로 나뉘었는가
- Boston Housing 회귀와 MNIST 분류의 마지막 layer/loss/metric 차이가 명확한가

필수 샘플:
- Keras mapping node
- optimizer node
- regression design node
- classification design node

### 3.6 `20260529_14` — DNN 회귀 데이터 프로세싱

원문:
- brief: `ML/final_brief/20260529.md`
- transcript: `ML/final_record/0529_ml.txt`
- 보조 conflict: `ML/final_record/0529이용오교수님.txt`

집중 검증:
- `boston.data`, `boston.target`, `feature_names` 분리가 node/evidence로 추적되는가
- `CHAS` 제거, train/test split, MinMax scaling이 순서대로 edge에 반영되는가
- `input_shape=(12,)`, `Dense(1)`, MSE/MAE, inverse transform, scatter validation이 model/validation node로 분리되는가
- 보조 전사는 primary evidence에 섞이지 않고 conflict로 남아 있는가

필수 샘플:
- data preparing node
- preprocessing node
- modeling/training node
- validation/test node

### 3.7 `20260604_15` — 실험 설계, 과적합 대응, CNN 입문

원문:
- brief: `ML/final_brief/20260604.md`
- transcript: `ML/final_record/0604ml.txt`

집중 검증:
- 전처리 5종, train/val/test, leakage가 각각 검색 가능한 node로 잡혔는가
- overfit diagnosis와 regularization toolkit이 처방 순서로 edge 연결되는가
- Energy 실습 결과의 반전, 즉 regularized가 baseline보다 나쁠 수 있다는 해석이 evidence로 유지되는가
- CNN receptive field, filter/kernel, convolution, pooling, Fashion-MNIST 실습 비교가 별도 node/evidence로 추적되는가

필수 샘플:
- train/val/test node
- overfitting diagnosis node
- regularization node
- CNN filter/convolution node
- Fashion-MNIST comparison node

## 4. 실행 체크리스트

| 단계 | 명령/행동 | 완료 기준 |
|------|-----------|-----------|
| 1 | `git diff --check` | trailing whitespace 0 |
| 2 | 모든 `_verify_report.md`에서 `EXPORT OK` 확인 | 7/7 OK |
| 3 | 원문 보존 `cmp` 또는 marker-preclean 비교 | final_* 본문 손상 0 |
| 4 | 각 강 heading-anchor 샘플 5개 대조 | heading mismatch 0 |
| 5 | 각 강 node 4개 이상 의미 대조 | 잘못 묶인 node 0 또는 수정 backlog |
| 6 | 각 강 transcript segment 시작/끝 샘플 4개 대조 | 의미 경계 오류 기록 |
| 7 | 각 강 evidence 6개 대조 | quote/ref mismatch 0 |
| 8 | annotated transcript marker 제거 후 원문 비교 | 원문 줄 동일 |
| 9 | RAG/로데이터 markdown id ghost scan | ghost 0 |
| 10 | DOCX zip 구조 검사 | 14/14 열림 |

## 5. QA 판정 등급

| 등급 | 의미 | 후속 |
|------|------|------|
| A | 자동 검증 OK + 원문 샘플 QA OK | 배포 가능 |
| B | 자동 검증 OK, 의미 경계 일부 개선 필요 | RAG 사용 가능, segment 보정 권장 |
| C | id는 맞지만 node/evidence 의미 오류 있음 | DOCX 배포 보류 |
| F | 원문 보존, ghost id, line range 오류 | 즉시 수정 |

현재 자동 검증 기준은 7개 강 모두 `A 후보`다. 다만 전사 segment는 자동 분할 기반이므로, 최종 배포 전에는 이 문서의 강별 집중 검증 포인트를 따라 의미 경계 QA를 수행해야 한다.
