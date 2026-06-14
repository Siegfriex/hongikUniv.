# DM_PDF08 — Ch.6 정수계획 2주차: 0-1 응용 모형 로데이터 디벨롭

## Policy

- PDF 원본과 full transcript는 수정하지 않는다.
- 이 문서는 PDF transcript와 sidecar를 바탕으로 만든 derived learning view다.
- 날짜 추정은 폐기한다. `DM_PDFxx` 순서가 작업 순서다.

## 현재 그래프 위치

- 지금 보는 노드: Ch.6 정수계획 2주차: 0-1 응용 모형
- 선행 노드: binary variable, integer programming, assignment structure
- 후속 노드: branch-and-bound, facility location, covering model
- 동형/유사 노드: 할당문제의 0-1 행렬, Solver bin 제약, network covering
- 연결 예제: 응급 의료 서비스 후보지, 공공 설비 입지, 행정구역 커버

## 원자료 핵심 전개

0-1 정수계획은 복잡한 선택/논리/커버 조건을 선형 제약으로 번역하는 모형화 언어다.

이 PDF는 기존 1~7강 마크다운 흐름에서 고립된 보충자료가 아니라, LP 모형화와 Solver, 심플렉스, 쌍대/민감도, 정수/네트워크/비선형 확장 사이의 연결을 만드는 원자료다.

## 핵심 노드 디벨롭

## n_DM_PDF08.set_covering_model — 집합커버링 모형 (set covering model)

**한 줄 정의:** 모든 수요 구역이 적어도 하나의 선택된 시설에 의해 커버되도록 하면서 선택 수를 최소화하는 0-1 모형이다.

**쉬운 직관:** 각 지역을 덮는 후보지를 최소 개수로 고르는 문제다.

**수식 또는 모형 형태:** min sum_j x_j subject to sum_j a_ij x_j >= 1 for every demand i, x_j in {0,1}.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 13개 행정구역 모두 10분 이내 응급 서비스를 받도록 응급차량 대기 후보지를 고른다. |
| 수식 언어 | coverage rows use 0/1 matrix A and binary decision vector x. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 A_ij 행렬과 변수셀 x_j를 SUMPRODUCT해 각 구역 커버 수를 계산하고 >=1 제약을 둔다. |

**강의 속 실제 예제 연결:** DM_PDF08은 후보지역 8곳과 행정구역 13개 커버 행렬을 통해 set covering을 제시한다.

**자주 하는 실수:** 각 구역이 정확히 1개 시설에만 커버되어야 한다고 오해하기 쉽다. 커버링은 보통 적어도 1개다.

**연결 관계**

- 선행 노드: binary variable
- 후속 노드: facility location
- 동형/유사 노드: assignment row/column sum structure

**근거:** `ev_DM_PDF08_001` -> `DM_PDF08:p006:L006`

> (행정구역별: covering 수 >= 1 )

## n_DM_PDF08.facility_location — 공공 설비 입지 선정 (facility location)

**한 줄 정의:** 시설 설치 여부를 0-1 변수로 두고 비용, 커버, 거리, 수요 조건을 만족하는 위치를 고르는 모형군이다.

**쉬운 직관:** 어디에 설치하면 가장 적은 비용/시설 수로 필요한 사람들을 서비스할 수 있는지 결정한다.

**수식 또는 모형 형태:** x_j = 1 if facility j is opened; constraints link demand coverage or capacity to opened facilities.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 응급차량 대기 후보지 중 어느 곳을 설치할지 선택한다. |
| 수식 언어 | binary open variables drive coverage and assignment constraints. |
| 스프레드시트/타블로 언어 | Solver에서는 후보지 변수셀을 bin으로 지정하고 설치 수 또는 총비용을 목표셀로 둔다. |

**강의 속 실제 예제 연결:** DM_PDF08의 공공 설비 예는 시설입지의 가장 직관적인 형태다.

**자주 하는 실수:** 시설 설치 변수와 서비스 할당 변수를 구분하지 않으면 큰 모형에서 논리가 깨진다.

**연결 관계**

- 선행 노드: 0-1 variable
- 후속 노드: fixed-charge and covering constraints
- 동형/유사 노드: transportation/network service assignment

**근거:** `ev_DM_PDF08_002` -> `DM_PDF08:p002:L003`

> ① 후보지역에 공공설비 설치 여부  변수셀 (0-1 변수)

## n_DM_PDF08.coverage_matrix — 도달 가능성 행렬 (coverage matrix)

**한 줄 정의:** 수요지 i가 후보지 j로부터 서비스 가능한지 0 또는 1로 표시한 입력 행렬이다.

**쉬운 직관:** 표의 각 칸은 후보지가 그 지역을 덮는지 표시하는 지도 압축본이다.

**수식 또는 모형 형태:** a_ij = 1 if demand i is covered by facility j, else 0.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 행정구역 i에서 후보지역 j까지 10분 이내 도달되면 Aij=1이다. |
| 수식 언어 | coverage_i = sum_j a_ij x_j. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 13x8 A 행렬과 8개 변수셀을 곱해 행별 커버 수를 만든다. |

**강의 속 실제 예제 연결:** DM_PDF08은 표를 가로/세로 바꿔 13x8 행렬을 작성해야 한다고 안내한다.

**자주 하는 실수:** 표 방향을 바꾸는 과정에서 i/j 인덱스를 뒤집는 실수가 자주 난다.

**연결 관계**

- 선행 노드: set covering model
- 후속 노드: coverage constraint
- 동형/유사 노드: assignment matrix

**근거:** `ev_DM_PDF08_003` -> `DM_PDF08:p003:L002`

> 후보지에서 10분 이내 도달 가능성: 0/1행렬

## 표/수식 재구성 메모

- PDF에서 표가 한 줄로 붙어 추출된 경우, 최종 학습 문서에서는 변수, 목적함수, 제약식, RHS, 판정 기준을 분리해 읽는다.
- 타블로/스프레드시트 표는 `변수 셀 -> LHS 계산 셀 -> RHS -> 부호/도메인` 순서로 재구성한다.
- `[EXTRACTION_GAP]` 페이지는 OCR 또는 수동 전사 후보이며, 현재 RAG의 근거로 단정 사용하지 않는다.

## Source Trace

| RAG label | sidecar id | PDF transcript anchor | normalized PDF |
|---|---|---|---|
| `n_DM_PDF08.set_covering_model` | `ev_DM_PDF08_001` | `DM_PDF08:p006:L006` | `DM_PDF08_ch06_integer_programming_week2.pdf` |
| `n_DM_PDF08.facility_location` | `ev_DM_PDF08_002` | `DM_PDF08:p002:L003` | `DM_PDF08_ch06_integer_programming_week2.pdf` |
| `n_DM_PDF08.coverage_matrix` | `ev_DM_PDF08_003` | `DM_PDF08:p003:L002` | `DM_PDF08_ch06_integer_programming_week2.pdf` |
