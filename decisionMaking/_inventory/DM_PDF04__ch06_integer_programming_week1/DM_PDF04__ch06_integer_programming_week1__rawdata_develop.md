# DM_PDF04 — Ch.6 정수계획 1주차 로데이터 디벨롭

## Policy

- PDF 원본과 full transcript는 수정하지 않는다.
- 이 문서는 PDF transcript와 sidecar를 바탕으로 만든 derived learning view다.
- 날짜 추정은 폐기한다. `DM_PDFxx` 순서가 작업 순서다.

## 현재 그래프 위치

- 지금 보는 노드: Ch.6 정수계획 1주차
- 선행 노드: LP 모형화, decision variable, Solver variable cell/domain
- 후속 노드: 분지한계법, 시설입지, 고정비, 상호배타 선택
- 동형/유사 노드: 연속 LP와 같은 목적/제약 구조에 domain 제약이 추가된 형태
- 연결 예제: 사람 수, 기계 대수, 출장 횟수, 공장 가동 여부

## 원자료 핵심 전개

정수계획은 LP의 선형 구조를 유지하되, 변수의 domain을 정수 또는 0-1로 제한해 현실적 선택을 표현한다.

이 PDF는 기존 1~7강 마크다운 흐름에서 고립된 보충자료가 아니라, LP 모형화와 Solver, 심플렉스, 쌍대/민감도, 정수/네트워크/비선형 확장 사이의 연결을 만드는 원자료다.

## 핵심 노드 디벨롭

## n_DM_PDF04.integer_programming — 정수계획 (integer programming)

**한 줄 정의:** 목적함수와 제약식은 선형이지만 일부 또는 모든 변수가 정수값만 가질 수 있는 최적화 모형이다.

**쉬운 직관:** 생산량은 연속일 수 있지만 사람 수, 트럭 수, 설치 여부는 2.7처럼 나눌 수 없기 때문에 domain을 제한한다.

**수식 또는 모형 형태:** min/max c^T x subject to Ax <= b, x_j integer for selected j.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 기계 대수나 출장 횟수처럼 셀 수 있는 결정을 변수로 둔다. |
| 수식 언어 | LP model + integer restrictions on selected variable cells. |
| 스프레드시트/타블로 언어 | Solver에서는 변수셀에 int 또는 bin 제한조건을 추가한다. |

**강의 속 실제 예제 연결:** DM_PDF04는 int/bin 선택과 정수 최적화 비율의 의미를 정수계획 도입부에서 다룬다.

**자주 하는 실수:** 식이 선형이면 단순 LP라고 착각하기 쉽다. 변수 domain이 정수이면 해법 난이도가 크게 달라진다.

**연결 관계**

- 선행 노드: LP 일반형
- 후속 노드: branch-and-bound
- 동형/유사 노드: 0-1 binary model

**근거:** `ev_DM_PDF04_001` -> `DM_PDF04:p001:L002`

> Integer Programming (정수계획법)

## n_DM_PDF04.binary_variable — 0-1 변수 (binary variable)

**한 줄 정의:** 어떤 선택을 하거나 하지 않는지를 1과 0으로 표현하는 변수다.

**쉬운 직관:** 수량을 묻는 변수가 아니라 스위치다. 켜면 1, 끄면 0이다.

**수식 또는 모형 형태:** x_j in {0,1}. 선택하면 1, 선택하지 않으면 0.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 공장을 열지 말지, 후보지에 시설을 설치할지, 과제를 배정할지를 표현한다. |
| 수식 언어 | Solver에서는 bin constraint로 지정한다. |
| 스프레드시트/타블로 언어 | 스프레드시트에서는 변수셀 값이 0/1이고 제약식은 이 선택들의 합이나 조건부 논리를 표현한다. |

**강의 속 실제 예제 연결:** DM_PDF04의 공장 가동 여부 예시는 binary variable의 대표 용도다.

**자주 하는 실수:** 0-1 변수에 연속 생산량 의미를 섞으면 안 된다. 필요하면 선택 변수 y와 생산량 x를 따로 둔다.

**연결 관계**

- 선행 노드: decision variable
- 후속 노드: fixed-charge model and facility location
- 동형/유사 노드: assignment problem의 행/열 0-1 구조

**근거:** `ev_DM_PDF04_002` -> `DM_PDF04:p011:L003`

> - 보물 선택여부 (변수셀) <- 2진수 (binary)

## n_DM_PDF04.integer_solver_option — Solver 정수 옵션 (integer Solver option)

**한 줄 정의:** Excel Solver에서 변수셀의 정수/이진 제한과 해법을 지정해 정수계획을 푸는 설정이다.

**쉬운 직관:** 수식 자체보다 변수 셀의 값 종류를 Solver에게 알려주는 단계다.

**수식 또는 모형 형태:** Variable cells with int/bin constraints; solving method may use branch-and-bound or evolutionary methods.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 변수셀을 bin으로 지정하면 0 또는 1만 허용된다. |
| 수식 언어 | Solver constraints include x_j = integer or x_j = binary. |
| 스프레드시트/타블로 언어 | 해찾기 옵션에서 정수 제한, 정수 최적화 비율, 해법 선택을 확인한다. |

**강의 속 실제 예제 연결:** DM_PDF04는 Excel 2010 Solver의 분지한계해법과 유전자해법을 함께 언급한다.

**자주 하는 실수:** Solver가 정수조건을 자동으로 이해한다고 생각하면 안 된다. 반드시 int/bin 제한을 넣어야 한다.

**연결 관계**

- 선행 노드: spreadsheet modeling
- 후속 노드: branch-and-bound performance
- 동형/유사 노드: LP Solver와 evolutionary Solver

**근거:** `ev_DM_PDF04_003` -> `DM_PDF04:p003:L004`

> 정수 제한 조건으로 해찾기

## 표/수식 재구성 메모

- PDF에서 표가 한 줄로 붙어 추출된 경우, 최종 학습 문서에서는 변수, 목적함수, 제약식, RHS, 판정 기준을 분리해 읽는다.
- 타블로/스프레드시트 표는 `변수 셀 -> LHS 계산 셀 -> RHS -> 부호/도메인` 순서로 재구성한다.
- `[EXTRACTION_GAP]` 페이지는 OCR 또는 수동 전사 후보이며, 현재 RAG의 근거로 단정 사용하지 않는다.

## Source Trace

| RAG label | sidecar id | PDF transcript anchor | normalized PDF |
|---|---|---|---|
| `n_DM_PDF04.integer_programming` | `ev_DM_PDF04_001` | `DM_PDF04:p001:L002` | `DM_PDF04_ch06_integer_programming_week1.pdf` |
| `n_DM_PDF04.binary_variable` | `ev_DM_PDF04_002` | `DM_PDF04:p011:L003` | `DM_PDF04_ch06_integer_programming_week1.pdf` |
| `n_DM_PDF04.integer_solver_option` | `ev_DM_PDF04_003` | `DM_PDF04:p003:L004` | `DM_PDF04_ch06_integer_programming_week1.pdf` |
