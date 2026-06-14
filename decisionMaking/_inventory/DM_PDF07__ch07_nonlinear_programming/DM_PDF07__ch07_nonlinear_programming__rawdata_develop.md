# DM_PDF07 — Ch.7 비선형계획 로데이터 디벨롭

## Policy

- PDF 원본과 full transcript는 수정하지 않는다.
- 이 문서는 PDF transcript와 sidecar를 바탕으로 만든 derived learning view다.
- 날짜 추정은 폐기한다. `DM_PDFxx` 순서가 작업 순서다.

## 현재 그래프 위치

- 지금 보는 노드: Ch.7 비선형계획
- 선행 노드: LP, convexity intuition, Solver modeling
- 후속 노드: GRG nonlinear, local/global optimum, KKT intuition
- 동형/유사 노드: LP의 직선/평면 제약과 NLP의 곡면 목적/제약 대비
- 연결 예제: 담장 길이로 직사각형 면적 최대화, Cobb-Douglas 형태, GRG Solver

## 원자료 핵심 전개

비선형계획은 현실의 곡선 관계를 표현할 수 있지만 지역 최적해와 초기해 민감성 때문에 LP보다 해석이 조심스럽다.

이 PDF는 기존 1~7강 마크다운 흐름에서 고립된 보충자료가 아니라, LP 모형화와 Solver, 심플렉스, 쌍대/민감도, 정수/네트워크/비선형 확장 사이의 연결을 만드는 원자료다.

## 핵심 노드 디벨롭

## n_DM_PDF07.nonlinear_programming — 비선형계획 (nonlinear programming)

**한 줄 정의:** 목적함수 또는 제약식 중 하나 이상이 비선형 함수인 최적화 모형이다.

**쉬운 직관:** 직선으로만 표현하던 관계 대신 곡선, 곱, 제곱, 로그 같은 현실 관계를 넣는 모형이다.

**수식 또는 모형 형태:** optimize f(x) subject to g_i(x) <= b_i, where f or g_i is nonlinear.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 면적 S = X1*X2를 최대화하는 문제는 목적함수가 곱이라 비선형이다. |
| 수식 언어 | B4=B7*B8처럼 변수셀끼리 곱해지는 objective cell이 생긴다. |
| 스프레드시트/타블로 언어 | Excel Solver에서는 GRG Nonlinear 해법을 선택한다. |

**강의 속 실제 예제 연결:** DM_PDF07은 X^0.5Y^0.7, log, sin, sqrt 같은 비선형 함수와 면적 최대화 예를 든다.

**자주 하는 실수:** 제약식이 선형이어도 목적함수가 비선형이면 전체 문제는 비선형계획이다.

**연결 관계**

- 선행 노드: LP formulation
- 후속 노드: local/global optimum
- 동형/유사 노드: quadratic programming and separable programming

**근거:** `ev_DM_PDF07_001` -> `DM_PDF07:p002:L006`

> ** 해법선택 : 비선형 GRG

## n_DM_PDF07.local_global_optimum — 지역 최적해와 전체 최적해 (local and global optimum)

**한 줄 정의:** 지역 최적해는 주변보다 좋은 해이고, 전체 최적해는 가능한 모든 해 중 가장 좋은 해다.

**쉬운 직관:** 산봉우리가 여러 개 있으면 가까운 봉우리는 올랐지만 세계 최고봉은 아닐 수 있다.

**수식 또는 모형 형태:** x* is local optimum if nearby feasible points are no better; global optimum if no feasible point anywhere is better.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 초기해 (0,0)에서는 멈추지만 다른 초기해에서는 (2.5,5)가 나오는 예는 초기해 민감성을 보여준다. |
| 수식 언어 | Solver result may depend on starting variable cell values. |
| 스프레드시트/타블로 언어 | GRG Nonlinear는 지역 탐색 기반이라 여러 초기해 실험이 필요할 수 있다. |

**강의 속 실제 예제 연결:** DM_PDF07은 초기해에 따라 (0,0) 또는 (2.5,5)가 나오는 비선형계획의 어려움을 제시한다.

**자주 하는 실수:** Solver가 찾은 해를 항상 전체 최적해라고 믿으면 안 된다. 특히 비볼록 문제는 위험하다.

**연결 관계**

- 선행 노드: feasible region
- 후속 노드: multi-start and global search
- 동형/유사 노드: LP의 꼭짓점 최적성과 대비

**근거:** `ev_DM_PDF07_002` -> `DM_PDF07:p006:L004`

> (엄밀히는 지역 최적해가 되기 위한 필요조건 만족해) local optimum

## n_DM_PDF07.grg_solver — GRG 비선형 해법 (GRG nonlinear solver)

**한 줄 정의:** Excel에서 부드러운 비선형 모형을 풀 때 사용하는 일반화 감소기울기 기반 해법이다.

**쉬운 직관:** 비선형 곡면 위에서 기울기를 따라 더 나은 방향을 찾는 로컬 탐색 방식이다.

**수식 또는 모형 형태:** uses gradient information and active constraints to search for a local optimum.

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | 면적 최대화 스프레드시트에서 해법선택을 비선형 GRG로 둔다. |
| 수식 언어 | objective and constraint cells may contain nonlinear formulas. |
| 스프레드시트/타블로 언어 | Solver options include GRG Nonlinear and initial variable values. |

**강의 속 실제 예제 연결:** DM_PDF07은 비선형계획 스프레드시트 모형에서 해법선택: 비선형 GRG를 명시한다.

**자주 하는 실수:** GRG를 선형 Simplex LP와 혼동하면 안 된다. 선형성 가정과 최적성 보장이 다르다.

**연결 관계**

- 선행 노드: nonlinear objective
- 후속 노드: local optimum diagnostics
- 동형/유사 노드: Solver Simplex LP와 Evolutionary 해법

**근거:** `ev_DM_PDF07_003` -> `DM_PDF07:p002:L002`

> 비선형계획의 스프레드시트 모형

## 표/수식 재구성 메모

- PDF에서 표가 한 줄로 붙어 추출된 경우, 최종 학습 문서에서는 변수, 목적함수, 제약식, RHS, 판정 기준을 분리해 읽는다.
- 타블로/스프레드시트 표는 `변수 셀 -> LHS 계산 셀 -> RHS -> 부호/도메인` 순서로 재구성한다.
- `[EXTRACTION_GAP]` 페이지는 OCR 또는 수동 전사 후보이며, 현재 RAG의 근거로 단정 사용하지 않는다.

## Source Trace

| RAG label | sidecar id | PDF transcript anchor | normalized PDF |
|---|---|---|---|
| `n_DM_PDF07.nonlinear_programming` | `ev_DM_PDF07_001` | `DM_PDF07:p002:L006` | `DM_PDF07_ch07_nonlinear_programming.pdf` |
| `n_DM_PDF07.local_global_optimum` | `ev_DM_PDF07_002` | `DM_PDF07:p006:L004` | `DM_PDF07_ch07_nonlinear_programming.pdf` |
| `n_DM_PDF07.grg_solver` | `ev_DM_PDF07_003` | `DM_PDF07:p002:L002` | `DM_PDF07_ch07_nonlinear_programming.pdf` |
