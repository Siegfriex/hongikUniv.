# DM_PDF07 — Ch.7 비선형계획 최종 RAG 튜터 운영문서

## 0. Document Contract

- **문서 성격:** PDF 요약본이 아니라, 전담 1:1 경영과학 튜터와 RAG agent가 함께 쓰는 증거 기반 운영문서다.
- **source_id:** `DM_PDF07`
- **normalized_pdf:** `decisionMaking/pdf_sources/DM_PDF07_ch07_nonlinear_programming.pdf`
- **primary transcript:** `decisionMaking/pdf_transcripts/DM_PDF07__ch07_nonlinear_programming__full_transcript.md`
- **sidecar:** `decisionMaking/_inventory/DM_PDF07__ch07_nonlinear_programming`
- **flat-pack target:** `decisionMaking/rag_applied_flat_pack/DM_PDF07__04_rag.md`
- **source priority:** 1) PDF 전사본 anchor, 2) 이 문서의 enhanced sidecar, 3) 웹 그라운딩, 4) 일반 OR/MS 지식.
- **중요한 명명 주의:** `DM_PDF07`는 PDF intake index다. 강의 회차/장 번호와 혼동하지 않는다.

### Web Grounding Notes

웹 근거는 PDF 원문을 대체하지 않는다. Solver 구현, LP/MIP/flow 표준 용어, Excel 함수 의미를 보조 확인하기 위해서만 사용한다.

| web_id | role in this RAG | URL |
|---|---|---|
| `WEB_MS_SOLVERADD` | Excel Solver constraint grounding: adding relational constraints to a solver model. | https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solveradd-function |
| `WEB_MS_SOLVERSOLVE` | Excel Solver execution grounding: solving the configured model. | https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solversolve-function |

## 1. Source Coverage Map

| page | primary anchors | extracted focus | extraction note |
|---|---|---|---|
| p001 | `DM_PDF07:p001:L002, DM_PDF07:p001:L003` | 7장. 비선형 계획 / • 서론 / – 엑셀에서 비선형 함수식 (예) | ok |
| p002 | `DM_PDF07:p002:L002, DM_PDF07:p002:L003` | 비선형계획의 스프레드시트 모형 / • Maximize S= X1.X2 (2차식) / subject to 2X1 + X2 = 10 (1차식) | ok |
| p003 | `DM_PDF07:p003:L002, DM_PDF07:p003:L003` | 지역 최적해와 전체 최적해 / Maximize S= X1.X2 / subject to 2X1 + X2 <= 10 | ok |
| p004 | `DM_PDF07:p004:L002, DM_PDF07:p004:L003` | 최적해 관계 / 가능해 영역 / KKT 해 (필요조건) | LOW_TEXT |
| p005 | `DM_PDF07:p005:L001, DM_PDF07:p005:L003` | **전체 최적해가 되기 위한 충분조건** / (주의) 충분조건이므로, 표의 조건을 만족하지 않으면서 / 전체 최적해가 될 수도 있다. | LOW_TEXT |
| p006 | `DM_PDF07:p006:L002, DM_PDF07:p006:L003` | 전체 최적해 조건(1) / • 해찾기(Solver)가 찾아주는 해는 지역 최적해임 / (엄밀히는 지역 최적해가 되기 위한 필요조건 만족해) local optimum | ok |
| p007 | `DM_PDF07:p007:L002, DM_PDF07:p007:L003` | 전체 최적해 조건(2) / 2. 선형 제약식만 있는 경우 / 1) 최대화 문제의 경우 | ok |
| p008 | `DM_PDF07:p008:L002, DM_PDF07:p008:L003` | 전체 최적해 조건(3) / 3. 비선형 제약식이 있는 경우 / 1) 최대화 문제의 경우 | ok |
| p009 | `DM_PDF07:p009:L002, DM_PDF07:p009:L003` | 가능영역 조건 : 볼록 집합(1) / 1. 볼록 집합 판단: 밖에서 볼 때 볼록 / 2. (구체적인 정의) 집합 내의 임의의 두 점을 연결하는 | ok |
| p010 | `DM_PDF07:p010:L002, DM_PDF07:p010:L003` | 가능영역 조건 : 볼록 집합(2) / {x| 볼록 함수 f(x) <= b(상수)}  볼록 집합 / 볼록 함수 f(x1,x2) <= b | ok |
| p011 | `DM_PDF07:p011:L002, DM_PDF07:p011:L003` | 볼록집합의 성질 /  볼록집합들의 공통집합은 볼록집합이다. / (예) 2차원 평면에서 볼록집합들의 공통집합  볼록집합 | ok |
| p012 | `DM_PDF07:p012:L002` | 1. (미분 가능, 단일변수 경우) 볼록/오목 함수판정 | LOW_TEXT |
| p013 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p014 | `DM_PDF07:p014:L002, DM_PDF07:p014:L003` | *볼록또는오목모두 : Det(짝수X짝수주소행렬) 의부호 =양 / 부호: 양양양양… / 부호: 음양음양… | ok |
| p015 | `DM_PDF07:p015:L002, DM_PDF07:p015:L003` | 부호: 양양양양… 부호: 음양음양… / 2. (미분 가능, 다변수 경우) 볼록/오목 함수판정 | LOW_TEXT |
| p016 | `DM_PDF07:p016:L002, DM_PDF07:p016:L003` | (Hessian 행렬 및 Determinant 계산법) / 4,1 / ,1,2 | ok |
| p017 | `DM_PDF07:p017:L001, DM_PDF07:p017:L003` | 행렬식계산 (예1) / (Laplace expansion) | LOW_TEXT |
| p018 | `DM_PDF07:p018:L001` | 행렬식계산 (예2) | LOW_TEXT |
| p019 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p020 | `DM_PDF07:p020:L002` | principal monors(주-소행렬식) 의 부호로 판단 | LOW_TEXT |
| p021 | `DM_PDF07:p021:L002, DM_PDF07:p021:L003` | 0.04𝑥1 / −1 * 𝑥2 / 0.6* 𝑥3 | ok |
| p022 | `DM_PDF07:p022:L002` | 가능해영역이 볼록집합인 경우 | LOW_TEXT |
| p023 | `DM_PDF07:p023:L002, DM_PDF07:p023:L003` | (p.4 복습)전체 최적해가 되기 위한 충분조건 / (주의) 충분조건이므로, 표의 조건을 만족하지 않으면서 / 전체 최적해가 될 수도 있다. | LOW_TEXT |
| p024 | `DM_PDF07:p024:L002, DM_PDF07:p024:L003` | 실습#1 / 1. 다음 함수는 볼록함수인가? 오목함수인가? / 2. 다음 문제는 지역 최적해가 전체 최적해가 되는가? 안 | ok |
| p025 | `DM_PDF07:p025:L002` | 2번 문제 (힌트1) | LOW_TEXT |
| p026 | `DM_PDF07:p026:L002, DM_PDF07:p026:L003` | h22=f’’(ax1+bx2+c)b2 >=0 / h22=f’’(ax1+bx2+c)b2 <=0 | LOW_TEXT |
| p027 | `DM_PDF07:p027:L002, DM_PDF07:p027:L003` | 7.3 가격결정 모형(Pricing Model) / [예제 7.3] 자동차 가격 결정 / • 중대형 승용차의 가격( )과 RV차량의 가격( )에 대한 | ok |
| p028 | `DM_PDF07:p028:L002, DM_PDF07:p028:L003` | 모형화 / • 결정변수: 중대형 승용차 가격( ), RV차량 가격( ) / • 목적함수: 총 판매이익 (단위: 천대*천만원 = 백억원) | ok |
| p029 | `DM_PDF07:p029:L002, DM_PDF07:p029:L003` | 전체 최적성 검사 / • 목적함수(*최대화 문제): / 헤시안-행렬이 이므로, | ok |
| p030 | `DM_PDF07:p030:L002, DM_PDF07:p030:L003` | 스프레드시트모형화: 최적해 (전체최적해) / C15 =C6+SUMPRODUCT(D6:E6,$D$12:$E$12) / B20 =SUM(C15:C16) | ok |
| p031 | `DM_PDF07:p031:L002, DM_PDF07:p031:L003` | 해찾기 / 매개변수 / • 해법 선택: | LOW_TEXT |
| p032 | `DM_PDF07:p032:L001, DM_PDF07:p032:L002` | 실습#2 / • H호텔의 성수기와 비성수기 객실료를 𝒑𝒉, 𝒑𝒍로 책정하 / 고 있고, 성수기와 비성수기의 객실 수요량을 𝒅𝒉, 𝒅𝒍은 | ok |
| p033 | `DM_PDF07:p033:L002, DM_PDF07:p033:L003` | 최적해 관계 / 가능해 영역 / KKT 해 (필요조건) | ok |
| p034 | `DM_PDF07:p034:L001` | 비선형 문제의 최적해 | LOW_TEXT |
| p035 | `DM_PDF07:p035:L002` | (변수수 2개, 등식수 2개인경우) | LOW_TEXT |
| p036 | `DM_PDF07:p036:L002, DM_PDF07:p036:L003` | 등식만있는비선형최적화문제(문제 1, 문제 2)에대해 / 비선형 GRG엔진이제공하는해는위의필요조건을만족한다 | LOW_TEXT |
| p037 | `DM_PDF07:p037:L002` | -2 | LOW_TEXT |
| p038 | `DM_PDF07:p038:L002` | (단, 미분은 가능하다고 가정) | LOW_TEXT |
| p039 | `DM_PDF07:p039:L002, DM_PDF07:p039:L003` | ),,,,,;,,( 111 lmn vvuuxxL  / )),,(()),,((),,( / 11 i | ok |
| p040 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p041 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p042 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p043 | `DM_PDF07:p043:L002, DM_PDF07:p043:L003` | 등식은선형식이라볼록이자오목함수임 / 비선형계획일반문제에대해비선형 GRG엔진을포함한모든 / 상용비선형 solver들이 제공하는해는 KKT 필요조건을만족함 | ok |
| p044 | `DM_PDF07:p044:L002, DM_PDF07:p044:L003` | p.32 참고 / 실습#3 / V1=-4 | LOW_TEXT |
| p045 | `DM_PDF07:p045:L002, DM_PDF07:p045:L003` | 실습#4 / (b) v1=0, v2=1/9 / (c ) 만족하지않음. | LOW_TEXT |
| p046 | `DM_PDF07:p046:L001, DM_PDF07:p046:L003` | 실습#5 / 그리고 위에서 구한 KKT해가 전체최적해인지 아닌지 판별하라 / (이유 명시). | LOW_TEXT |

## 2. Chapter Thesis

비선형계획은 목적함수 또는 제약식에 비선형성이 들어가면서 지역 최적해, 초기해 민감성, 볼록성/오목성에 따른 전체 최적성 검증이 핵심이 되는 모델군이다.

## 3. Current Graph Position

- **현재 그래프 위치:** LP/Solver formulation -> nonlinear objective/constraint -> GRG local solution -> convexity/concavity checks -> KKT/global optimum diagnostics.
- **지금 보는 노드:** `DM_PDF07` / Ch.7 비선형계획
- **튜터 운영 원칙:** 질문이 들어오면 먼저 노드로 매핑하고, 예제 카드와 수식/Solver 구조를 거쳐 Source Trace Table의 evidence anchor로 되돌아간다.

## 4. Learning Outcomes

- 비선형 GRG 해가 지역 최적해일 수 있음을 설명한다.
- 초기해와 볼록성 조건이 전체 최적성 판단에 왜 중요한지 말한다.
- 자동차 가격 결정 예제를 목적함수, 제약식, Solver, 전체최적성 검사로 전개한다.

## 5. Concept Graph Map

| node_id | 개념 | 역할 | 선행 노드 | 후속 노드 |
| --- | --- | --- | --- | --- |
| `n_DM_PDF07.nonlinear_programming` | 비선형계획 | 목적함수 또는 제약식 중 적어도 하나가 비선형 함수인 최적화 모형이다. | LP formulation | GRG, KKT |
| `n_DM_PDF07.grg_solver` | GRG 비선형 해법 | Excel Solver에서 매끄러운 비선형 문제의 지역 최적 조건을 찾는 해법이다. | nonlinear_programming | local_global_optimum |
| `n_DM_PDF07.local_global_optimum` | 지역/전체 최적해 | 지역 최적해는 주변에서만 최적인 해, 전체 최적해는 모든 가능해 중 최적인 해다. | GRG solver | convexity sufficient conditions |
| `n_DM_PDF07.initial_solution_sensitivity` | 초기해 민감성 | 비선형 Solver가 시작점에 따라 다른 지역해에 도달할 수 있는 성질이다. | local_global_optimum | multistart diagnostic |
| `n_DM_PDF07.convexity_concavity` | 볼록성/오목성 | 최대화에서는 오목 목적함수와 볼록 가능영역, 최소화에서는 볼록 목적함수와 볼록 가능영역이 전체 최적성 보장의 핵심 조건이다. | local_global_optimum | KKT sufficiency |
| `n_DM_PDF07.nonlinear_constraints` | 비선형 제약과 가능영역 | 제약식이 비선형이면 각 제약이 만드는 가능영역이 볼록집합인지 따로 확인해야 한다. | convexity_concavity | KKT |
| `n_DM_PDF07.quadratic_programming` | 2차계획/2차 목적 | 목적함수나 제약에 2차식이 포함된 비선형 최적화의 대표 형태다. | nonlinear_programming | convexity_concavity |
| `n_DM_PDF07.car_pricing_example` | 자동차 가격 결정 | 중대형 승용차와 RV의 가격/판매량 관계를 반영해 총판매이익을 최대화하는 비선형 예제다. | quadratic_programming | global optimality check |
| `n_DM_PDF07.kkt_condition` | KKT 필요조건 | 제약이 있는 비선형 최적화에서 지역 최적해가 만족해야 하는 일계 조건과 상보성 조건이다. | local_global_optimum | convexity sufficiency |

### Edge List

| from | edge_type | to |
| --- | --- | --- |
| `LP formulation` | 선행 관계 | `n_DM_PDF07.nonlinear_programming` |
| `n_DM_PDF07.nonlinear_programming` | 후속 관계 | `GRG, KKT` |
| `n_DM_PDF07.nonlinear_programming` | 동형/유사 | `quadratic programming` |
| `nonlinear_programming` | 선행 관계 | `n_DM_PDF07.grg_solver` |
| `n_DM_PDF07.grg_solver` | 후속 관계 | `local_global_optimum` |
| `n_DM_PDF07.grg_solver` | 동형/유사 | `KKT necessary conditions` |
| `GRG solver` | 선행 관계 | `n_DM_PDF07.local_global_optimum` |
| `n_DM_PDF07.local_global_optimum` | 후속 관계 | `convexity sufficient conditions` |
| `n_DM_PDF07.local_global_optimum` | 동형/유사 | `multi-start` |
| `local_global_optimum` | 선행 관계 | `n_DM_PDF07.initial_solution_sensitivity` |
| `n_DM_PDF07.initial_solution_sensitivity` | 후속 관계 | `multistart diagnostic` |
| `n_DM_PDF07.initial_solution_sensitivity` | 동형/유사 | `nonconvex optimization` |
| `local_global_optimum` | 선행 관계 | `n_DM_PDF07.convexity_concavity` |
| `n_DM_PDF07.convexity_concavity` | 후속 관계 | `KKT sufficiency` |
| `n_DM_PDF07.convexity_concavity` | 동형/유사 | `Hessian/principal minors` |
| `convexity_concavity` | 선행 관계 | `n_DM_PDF07.nonlinear_constraints` |
| `n_DM_PDF07.nonlinear_constraints` | 후속 관계 | `KKT` |
| `n_DM_PDF07.nonlinear_constraints` | 동형/유사 | `feasible set geometry` |
| `nonlinear_programming` | 선행 관계 | `n_DM_PDF07.quadratic_programming` |
| `n_DM_PDF07.quadratic_programming` | 후속 관계 | `convexity_concavity` |
| `n_DM_PDF07.quadratic_programming` | 동형/유사 | `pricing model` |
| `quadratic_programming` | 선행 관계 | `n_DM_PDF07.car_pricing_example` |
| `n_DM_PDF07.car_pricing_example` | 후속 관계 | `global optimality check` |
| `n_DM_PDF07.car_pricing_example` | 동형/유사 | `revenue management` |
| `local_global_optimum` | 선행 관계 | `n_DM_PDF07.kkt_condition` |
| `n_DM_PDF07.kkt_condition` | 후속 관계 | `convexity sufficiency` |
| `n_DM_PDF07.kkt_condition` | 동형/유사 | `complementary slackness` |

## 6. Core Concept Node Cards

### n_DM_PDF07.nonlinear_programming — 비선형계획 (nonlinear programming)

1. **한 줄 정의:** 목적함수 또는 제약식 중 적어도 하나가 비선형 함수인 최적화 모형이다.
2. **쉬운 직관:** 직선과 평면이 아니라 곡선/곡면 위에서 최적점을 찾는다.
3. **언제 쓰는가:** 가격-수요 관계, 생산함수, 면적 최대화처럼 곱/제곱/로그 등이 있을 때 쓴다.
4. **변수 정의:** continuous variables x.
5. **목적함수:** nonlinear f(x) maximize/minimize.
6. **제약식:** linear or nonlinear constraints g_i(x)<=b_i.
7. **수식의 현실 의미:** x1*x2 같은 식이 목표셀에 들어갈 수 있다.
8. **그래프/네트워크 관점:** curved feasible regions and contour lines.
9. **스프레드시트/Solver 관점:** Excel Solver에서 GRG Nonlinear 해법을 선택한다.
10. **강의 예제 연결:** p001-p002 비선형 함수식과 S=x1*x2 예제.
11. **예제 숫자 해석:** 2x1+x2=10 아래 S=x1*x2 최대화.
12. **자주 하는 실수:** 비선형인데 Simplex LP로 풀려는 오류.
13. **선행 노드:** LP formulation
14. **후속 노드:** GRG, KKT
15. **동형/유사 노드:** quadratic programming
16. **시험 출제 포인트:** 비선형 여부 판정.
17. **RAG retrieval tags:** `nonlinear`, `비선형`
18. **Evidence anchors:** `ev_deep_DM_PDF07_node_nonlinear_programming` -> `DM_PDF07:p001:L004` / source_id=`DM_PDF07`, page=`p001`, block=`p001-L004`, line=`L004`

> 근거 excerpt: – 엑셀에서 비선형 함수식 (예)

### n_DM_PDF07.grg_solver — GRG 비선형 해법 (GRG nonlinear solver)

1. **한 줄 정의:** Excel Solver에서 매끄러운 비선형 문제의 지역 최적 조건을 찾는 해법이다.
2. **쉬운 직관:** 곡면 위에서 기울기를 따라 개선하다가 더 개선하기 어려운 지점에 멈춘다.
3. **언제 쓰는가:** 미분 가능한 비선형 Solver 모델에 쓴다.
4. **변수 정의:** changing cells continuous x.
5. **목적함수:** nonlinear objective.
6. **제약식:** constraints can be linear or nonlinear.
7. **수식의 현실 의미:** 초기해에 따라 다른 해로 갈 수 있다.
8. **그래프/네트워크 관점:** local search on nonlinear landscape.
9. **스프레드시트/Solver 관점:** Solver 해법선택: 비선형 GRG.
10. **강의 예제 연결:** p002, p031, p036.
11. **예제 숫자 해석:** 초기해 (0,0)과 (2.5,5) 차이.
12. **자주 하는 실수:** GRG 결과를 항상 전역 최적이라고 단정하는 오류.
13. **선행 노드:** nonlinear_programming
14. **후속 노드:** local_global_optimum
15. **동형/유사 노드:** KKT necessary conditions
16. **시험 출제 포인트:** GRG 선택 이유.
17. **RAG retrieval tags:** `GRG`, `solver`
18. **Evidence anchors:** `ev_deep_DM_PDF07_node_grg_solver` -> `DM_PDF07:p002:L006` / source_id=`DM_PDF07`, page=`p002`, block=`p002-L006`, line=`L006`

> 근거 excerpt: ** 해법선택 : 비선형 GRG

### n_DM_PDF07.local_global_optimum — 지역/전체 최적해 (local/global optimum)

1. **한 줄 정의:** 지역 최적해는 주변에서만 최적인 해, 전체 최적해는 모든 가능해 중 최적인 해다.
2. **쉬운 직관:** 산봉우리가 여러 개면 가까운 봉우리가 최고봉이 아닐 수 있다.
3. **언제 쓰는가:** 비선형 Solver 결과를 검증할 때 쓴다.
4. **변수 정의:** candidate solution x*.
5. **목적함수:** compare f(x*) locally and globally.
6. **제약식:** depends on feasible set and function shape.
7. **수식의 현실 의미:** 초기해 (0,0) 결과와 다른 초기해 결과가 다르다.
8. **그래프/네트워크 관점:** nonconvex landscape.
9. **스프레드시트/Solver 관점:** Solver가 찾아주는 해는 보통 지역 최적 조건을 만족한다.
10. **강의 예제 연결:** p003-p004 지역/전체 최적해.
11. **예제 숫자 해석:** 초기해 (0,0)->(0,0), 그 외 ->(2.5,5).
12. **자주 하는 실수:** 지역 최적해를 무조건 전체 최적해로 제출하는 오류.
13. **선행 노드:** GRG solver
14. **후속 노드:** convexity sufficient conditions
15. **동형/유사 노드:** multi-start
16. **시험 출제 포인트:** 지역/전역 구분.
17. **RAG retrieval tags:** `local`, `global`, `optimum`
18. **Evidence anchors:** `ev_deep_DM_PDF07_node_local_global_optimum` -> `DM_PDF07:p003:L002` / source_id=`DM_PDF07`, page=`p003`, block=`p003-L002`, line=`L002`

> 근거 excerpt: 지역 최적해와 전체 최적해

### n_DM_PDF07.initial_solution_sensitivity — 초기해 민감성 (initial solution sensitivity)

1. **한 줄 정의:** 비선형 Solver가 시작점에 따라 다른 지역해에 도달할 수 있는 성질이다.
2. **쉬운 직관:** 출발 위치가 다르면 다른 골짜기나 봉우리에 도착할 수 있다.
3. **언제 쓰는가:** 비선형 해를 신뢰하기 전 여러 초기해를 시험할 때 쓴다.
4. **변수 정의:** initial values of changing cells.
5. **목적함수:** same objective, different starting points.
6. **제약식:** constraints unchanged.
7. **수식의 현실 의미:** 0,0에서 시작하면 (0,0), 다른 초기해는 (2.5,5)로 간다.
8. **그래프/네트워크 관점:** basin of attraction.
9. **스프레드시트/Solver 관점:** Solver 초기 변경셀 값과 multi-start 점검.
10. **강의 예제 연결:** p003 초기해 비교.
11. **예제 숫자 해석:** 초기해 하나만으로 최적성을 확정하지 않는다.
12. **자주 하는 실수:** 초기값을 아무렇게 둬도 항상 같은 해라고 생각하는 오류.
13. **선행 노드:** local_global_optimum
14. **후속 노드:** multistart diagnostic
15. **동형/유사 노드:** nonconvex optimization
16. **시험 출제 포인트:** 초기해 바꿔보기.
17. **RAG retrieval tags:** `initial_solution`, `초기해`
18. **Evidence anchors:** `ev_deep_DM_PDF07_node_initial_solution_sensitivity` -> `DM_PDF07:p003:L006` / source_id=`DM_PDF07`, page=`p003`, block=`p003-L006`, line=`L006`

> 근거 excerpt: 초기해 (0,0)  결과: (0,0)

### n_DM_PDF07.convexity_concavity — 볼록성/오목성 (convexity and concavity)

1. **한 줄 정의:** 최대화에서는 오목 목적함수와 볼록 가능영역, 최소화에서는 볼록 목적함수와 볼록 가능영역이 전체 최적성 보장의 핵심 조건이다.
2. **쉬운 직관:** 곡면 모양이 한 봉우리/한 골짜리이면 지역해가 전체해가 된다.
3. **언제 쓰는가:** GRG 해의 전역성 판단에 쓴다.
4. **변수 정의:** objective f and feasible set.
5. **목적함수:** max concave f or min convex f under convex feasible set.
6. **제약식:** linear constraints are convex feasible regions.
7. **수식의 현실 의미:** 자동차 가격결정 예제의 2차 목적함수 오목성 검사.
8. **그래프/네트워크 관점:** convex set and contour geometry.
9. **스프레드시트/Solver 관점:** Solver 결과 후 별도 수학 검증으로 붙인다.
10. **강의 예제 연결:** p006-p008, p029.
11. **예제 숫자 해석:** 선형 제약식들은 항상 볼록집합을 만든다.
12. **자주 하는 실수:** 목적함수 볼록/오목 방향을 max/min에서 뒤집는 오류.
13. **선행 노드:** local_global_optimum
14. **후속 노드:** KKT sufficiency
15. **동형/유사 노드:** Hessian/principal minors
16. **시험 출제 포인트:** 전역 최적 충분조건.
17. **RAG retrieval tags:** `convexity`, `concavity`, `볼록`, `오목`
18. **Evidence anchors:** `ev_deep_DM_PDF07_node_convexity_concavity` -> `DM_PDF07:p005:L001` / source_id=`DM_PDF07`, page=`p005`, block=`p005-L001`, line=`L001`

> 근거 excerpt: **전체 최적해가 되기 위한 충분조건**

### n_DM_PDF07.nonlinear_constraints — 비선형 제약과 가능영역 (nonlinear constraints)

1. **한 줄 정의:** 제약식이 비선형이면 각 제약이 만드는 가능영역이 볼록집합인지 따로 확인해야 한다.
2. **쉬운 직관:** 목적함수가 좋아도 feasible region이 찌그러져 있으면 지역해 문제가 생긴다.
3. **언제 쓰는가:** 비선형 제약이 포함된 문제의 전역성 판단에 쓴다.
4. **변수 정의:** g_i(x)<=b_i or g_i(x)>=b_i.
5. **목적함수:** objective depends on problem.
6. **제약식:** convex feasible set conditions.
7. **수식의 현실 의미:** 비선형 제약의 가능해영역이 볼록이면 sufficient condition에 들어갈 수 있다.
8. **그래프/네트워크 관점:** curved constraint boundary.
9. **스프레드시트/Solver 관점:** Solver에는 식을 입력하지만, 해석은 convexity 검토가 필요하다.
10. **강의 예제 연결:** p008-p011.
11. **예제 숫자 해석:** 각 제약식 가능해영역이 볼록이면 전체 교집합도 볼록.
12. **자주 하는 실수:** 비선형이면 무조건 nonconvex라고 단정하는 오류.
13. **선행 노드:** convexity_concavity
14. **후속 노드:** KKT
15. **동형/유사 노드:** feasible set geometry
16. **시험 출제 포인트:** 제약 볼록성 검사.
17. **RAG retrieval tags:** `nonlinear_constraint`, `feasible_set`
18. **Evidence anchors:** `ev_deep_DM_PDF07_node_nonlinear_constraints` -> `DM_PDF07:p008:L003` / source_id=`DM_PDF07`, page=`p008`, block=`p008-L003`, line=`L003`

> 근거 excerpt: 3. 비선형 제약식이 있는 경우

### n_DM_PDF07.quadratic_programming — 2차계획/2차 목적 (quadratic programming)

1. **한 줄 정의:** 목적함수나 제약에 2차식이 포함된 비선형 최적화의 대표 형태다.
2. **쉬운 직관:** 가격-수요 또는 생산량 간 상호작용이 곡선으로 나타난다.
3. **언제 쓰는가:** 2차 이익함수, 분산 최소화, 가격 결정에 쓴다.
4. **변수 정의:** x variables and quadratic terms.
5. **목적함수:** quadratic objective.
6. **제약식:** linear or quadratic constraints.
7. **수식의 현실 의미:** 자동차 가격 결정에서 총판매이익이 2차식으로 표현된다.
8. **그래프/네트워크 관점:** parabolic contour/curvature.
9. **스프레드시트/Solver 관점:** GRG 또는 QP solver로 풀 수 있다.
10. **강의 예제 연결:** p027-p030 자동차 가격 결정.
11. **예제 숫자 해석:** 목적함수가 오목이면 max의 지역해가 전체해가 된다.
12. **자주 하는 실수:** 2차식이 있으면 모두 어려운 nonconvex라고 생각하는 오류.
13. **선행 노드:** nonlinear_programming
14. **후속 노드:** convexity_concavity
15. **동형/유사 노드:** pricing model
16. **시험 출제 포인트:** 2차식 해석.
17. **RAG retrieval tags:** `quadratic`, `2차식`
18. **Evidence anchors:** `ev_deep_DM_PDF07_node_quadratic_programming` -> `DM_PDF07:p027:L003` / source_id=`DM_PDF07`, page=`p027`, block=`p027-L003`, line=`L003`

> 근거 excerpt: [예제 7.3] 자동차 가격 결정

### n_DM_PDF07.car_pricing_example — 자동차 가격 결정 (car pricing example)

1. **한 줄 정의:** 중대형 승용차와 RV의 가격/판매량 관계를 반영해 총판매이익을 최대화하는 비선형 예제다.
2. **쉬운 직관:** 가격을 올리면 단위마진은 늘지만 수요가 줄어드는 trade-off를 최적화한다.
3. **언제 쓰는가:** 수요-가격 관계가 있는 수익관리 문제에 쓴다.
4. **변수 정의:** P1, P2 or vehicle sales/price variables.
5. **목적함수:** maximize total sales revenue - production cost.
6. **제약식:** production capacity and price relation constraints.
7. **수식의 현실 의미:** 연간 생산능력 600천대 같은 제한 아래 이익을 최대화한다.
8. **그래프/네트워크 관점:** quadratic profit surface over price variables.
9. **스프레드시트/Solver 관점:** Solver changing cells에 가격 또는 관련 변수, GRG Nonlinear.
10. **강의 예제 연결:** 예제 7.3 자동차 가격 결정.
11. **예제 숫자 해석:** 중대형/RV 생산원가와 생산능력 조건.
12. **자주 하는 실수:** 가격을 독립적으로 올리면 항상 이익이 오른다고 생각하는 오류.
13. **선행 노드:** quadratic_programming
14. **후속 노드:** global optimality check
15. **동형/유사 노드:** revenue management
16. **시험 출제 포인트:** 예제 완전 정식화.
17. **RAG retrieval tags:** `car_pricing`, `자동차`, `가격`
18. **Evidence anchors:** `ev_deep_DM_PDF07_node_car_pricing_example` -> `DM_PDF07:p027:L003` / source_id=`DM_PDF07`, page=`p027`, block=`p027-L003`, line=`L003`

> 근거 excerpt: [예제 7.3] 자동차 가격 결정

### n_DM_PDF07.kkt_condition — KKT 필요조건 (KKT conditions)

1. **한 줄 정의:** 제약이 있는 비선형 최적화에서 지역 최적해가 만족해야 하는 일계 조건과 상보성 조건이다.
2. **쉬운 직관:** 최적점에서는 목적함수 개선방향과 제약 경계의 힘이 균형을 이룬다.
3. **언제 쓰는가:** GRG 해가 어떤 조건을 만족하는지 설명할 때 쓴다.
4. **변수 정의:** gradient, multipliers, constraints.
5. **목적함수:** stationarity plus feasibility and complementarity.
6. **제약식:** 부등식 승수 비음/상보조건.
7. **수식의 현실 의미:** 상용 비선형 Solver 해는 보통 KKT 필요조건을 만족한다.
8. **그래프/네트워크 관점:** tangent/normal geometry.
9. **스프레드시트/Solver 관점:** Solver 결과의 수학적 진단.
10. **강의 예제 연결:** p039, p043.
11. **예제 숫자 해석:** 부등식 제약식*승수=0.
12. **자주 하는 실수:** KKT를 만족하면 항상 전체 최적이라고 단정하는 오류.
13. **선행 노드:** local_global_optimum
14. **후속 노드:** convexity sufficiency
15. **동형/유사 노드:** complementary slackness
16. **시험 출제 포인트:** 필요조건 vs 충분조건.
17. **RAG retrieval tags:** `KKT`, `multiplier`
18. **Evidence anchors:** `ev_deep_DM_PDF07_node_kkt_condition` -> `DM_PDF07:p039:L033` / source_id=`DM_PDF07`, page=`p039`, block=`p039-L033`, line=`L033`

> 근거 excerpt: 부등식제약식승수>=0


## 7. Example Walkthrough Cards

### ex_DM_PDF07.rectangle_product — S=x1*x2 예제

- **현실 문장 재해석:** 2x1+x2=10 아래 S=x1*x2를 최대화한다.
- **의사결정변수:** x1,x2.
- **목적함수:** max S=x1*x2.
- **제약식:** 2x1+x2=10.
- **Solver 구조:** GRG Nonlinear.
- **결과 해석:** 초기해에 따라 Solver 결과가 달라질 수 있음을 보여준다.
- **코칭 순서:**
1. 비선형 목적 확인.
2. GRG 선택.
3. 초기해 바꿔 실행.
4. 지역/전체 판단.
- **Evidence anchors:** `ev_deep_DM_PDF07_example_rectangle_product` -> `DM_PDF07:p001:L009` / page=`p001`, block=`p001-L009`, line=`L009`

> 근거 excerpt: Maximize S= X1.X2

### ex_DM_PDF07.car_pricing — 자동차 가격 결정 예제

- **현실 문장 재해석:** 가격-수요 관계와 생산능력 제약 아래 총판매이익을 최대화한다.
- **의사결정변수:** P1,P2 또는 판매량 관련 변수.
- **목적함수:** max revenue-cost quadratic objective.
- **제약식:** 생산능력 선형 제약.
- **Solver 구조:** GRG Nonlinear, global optimality check.
- **결과 해석:** 오목 목적함수+선형 제약이면 지역 최적해가 전체 최적해다.
- **코칭 순서:**
1. 현실 관계식 읽기.
2. 목적함수 구성.
3. 제약 입력.
4. 오목성/볼록성 확인.
- **Evidence anchors:** `ev_deep_DM_PDF07_example_car_pricing` -> `DM_PDF07:p027:L003` / page=`p027`, block=`p027-L003`, line=`L003`

> 근거 excerpt: [예제 7.3] 자동차 가격 결정

### ex_DM_PDF07.kkt_check — KKT와 전체최적성 판별

- **현실 문장 재해석:** 구한 KKT 해가 전체최적해인지 볼록성 조건으로 판별한다.
- **의사결정변수:** candidate x and multipliers.
- **목적함수:** stationarity condition.
- **제약식:** feasibility and complementarity.
- **Solver 구조:** Solver 해 후 수학적 검토.
- **결과 해석:** KKT는 필요조건이고 convexity가 있어야 충분조건이 된다.
- **코칭 순서:**
1. KKT 만족 확인.
2. 목적함수 curvature 확인.
3. 가능영역 볼록성 확인.
- **Evidence anchors:** `ev_deep_DM_PDF07_example_kkt_check` -> `DM_PDF07:p046:L003` / page=`p046`, block=`p046-L003`, line=`L003`

> 근거 excerpt: 그리고 위에서 구한 KKT해가 전체최적해인지 아닌지 판별하라


## 8. Modeling Pattern Library

| pattern | 모형화 템플릿 | 먼저 볼 노드 | 연결 노드 |
| --- | --- | --- | --- |
| GRG-local형 | 비선형 Solver 결과는 지역해일 수 있으므로 초기해/전역성 검토가 필요하다. | grg_solver | local_global_optimum |
| 볼록성검토형 | max는 오목 목적+볼록 가능영역, min은 볼록 목적+볼록 가능영역을 확인한다. | convexity_concavity | KKT |
| 가격-수요형 | 수익과 수요가 비선형으로 얽히면 목적함수 curvature를 해석한다. | car_pricing_example | quadratic_programming |

## 9. Spreadsheet / Solver Mapping

| 요소 | Solver/Spreadsheet 대응 | 튜터 해설 포인트 |
| --- | --- | --- |
| 변수셀 | 연속 가격/생산/치수 변수 | 초기값을 의미 있게 설정하고 여러 초기값을 시도한다. |
| 목표셀 | 곱, 제곱, 로그 등 비선형 식 | Simplex LP가 아니라 GRG Nonlinear. |
| 제약셀 | 선형/비선형 제약 | 비선형 제약은 가능영역 볼록성 검토가 필요하다. |
| 검증 | 지역해 vs 전체해 | Solver 결과 후 curvature/KKT/초기해 민감성을 기록한다. |

## 10. Cross-Chapter Connections

| 연결 대상 | 연결 설명 | 의존/참조 관계 |
| --- | --- | --- |
| LP 단원 | LP는 선형이라 지역/전체 문제가 단순하지만 NLP는 그렇지 않다. | linear -> nonlinear |
| DM_PDF05 상보여유 | KKT의 complementarity는 LP 상보여유의 비선형 확장이다. | complementary slackness -> KKT |
| Solver 모델링 | Solver 해법 선택이 Simplex LP에서 GRG Nonlinear로 바뀐다. | Solver method selection |

## 11. Misconception & Error Diagnosis Bank

| 오답/착각 | 왜 문제인가 | 교정 코칭 | 연결 노드 |
| --- | --- | --- | --- |
| GRG=전체최적 | GRG는 지역 필요조건 해를 줄 수 있다. | 초기해와 convexity 검토를 붙인다. | grg_solver |
| 비선형이면 무조건 못 풂 | 오목/볼록 구조면 전역성 보장이 가능하다. | 목적/제약 curvature를 확인. | convexity_concavity |
| KKT 충분조건 오해 | 일반 nonconvex에서 KKT는 필요조건이다. | 볼록성 조건이 있어야 충분조건. | kkt_condition |

## 12. Retrieval Routing Table

| 사용자 질문 유형 | 먼저 볼 노드 | 다음 볼 노드 | 예제 카드 | 근거 힌트 |
| --- | --- | --- | --- | --- |
| 비선형 Solver는 뭘 선택? | `grg_solver` | `nonlinear_programming` | `rectangle_product` | DM_PDF07:p002 |
| 지역해와 전체해 차이? | `local_global_optimum` | `initial_solution_sensitivity` | `rectangle_product` | DM_PDF07:p003 |
| 전체 최적성 어떻게 보장? | `convexity_concavity` | `kkt_condition` | `car_pricing` | DM_PDF07:p006-p008 |
| 자동차 가격 예제 식? | `car_pricing_example` | `quadratic_programming` | `car_pricing` | DM_PDF07:p027-p030 |

## 13. Tutor Session Protocol

1. **지도부터:** Concept Graph Map과 Edge List를 먼저 보여주고, 현재 노드가 전체 OR/MS 흐름에서 어디인지 설명한다.
2. **노드 중심으로:** Core Concept Node Card의 18개 필드를 순서대로 따라가되, 선행/후속/동형 노드를 최소 3개 연결한다.
3. **예제 중심으로:** Example Walkthrough Card를 사용해 현실 문장 -> 변수 -> 목적함수 -> 제약식 -> Solver -> 결과 해석 순서로 진행한다.
4. **문제 풀이 모드:** 사용자가 변수를 먼저 말하게 하고, 목적함수/제약식은 힌트로 한 단계씩 유도한다.
5. **완성 해설 모드:** 위 절차를 생략하지 않고 전체 풀이를 한 번에 제시한다.
6. **암기/정리 모드:** Modeling Pattern Library, Solver Mapping, Misconception Bank만 압축해 제시한다.

## 14. Practice / Check Questions

1. GRG로 얻은 해가 전체 최적해인지 확인하는 절차를 세 단계로 말하라.
2. max 문제에서 목적함수 오목성과 가능영역 볼록성이 왜 필요한지 설명하라.
3. 초기해 두 개를 넣어 서로 다른 결과가 나왔을 때 보고서에 무엇을 적어야 하는가?

## 15. Source Trace Table

| RAG label | evidence_id | source_id | page | block | line | excerpt |
| --- | --- | --- | --- | --- | --- | --- |
| `n_DM_PDF07.nonlinear_programming` | `ev_deep_DM_PDF07_node_nonlinear_programming` | `DM_PDF07` | `p001` | `p001-L004` | `L004` | – 엑셀에서 비선형 함수식 (예) |
| `n_DM_PDF07.grg_solver` | `ev_deep_DM_PDF07_node_grg_solver` | `DM_PDF07` | `p002` | `p002-L006` | `L006` | ** 해법선택 : 비선형 GRG |
| `n_DM_PDF07.local_global_optimum` | `ev_deep_DM_PDF07_node_local_global_optimum` | `DM_PDF07` | `p003` | `p003-L002` | `L002` | 지역 최적해와 전체 최적해 |
| `n_DM_PDF07.initial_solution_sensitivity` | `ev_deep_DM_PDF07_node_initial_solution_sensitivity` | `DM_PDF07` | `p003` | `p003-L006` | `L006` | 초기해 (0,0)  결과: (0,0) |
| `n_DM_PDF07.convexity_concavity` | `ev_deep_DM_PDF07_node_convexity_concavity` | `DM_PDF07` | `p005` | `p005-L001` | `L001` | **전체 최적해가 되기 위한 충분조건** |
| `n_DM_PDF07.nonlinear_constraints` | `ev_deep_DM_PDF07_node_nonlinear_constraints` | `DM_PDF07` | `p008` | `p008-L003` | `L003` | 3. 비선형 제약식이 있는 경우 |
| `n_DM_PDF07.quadratic_programming` | `ev_deep_DM_PDF07_node_quadratic_programming` | `DM_PDF07` | `p027` | `p027-L003` | `L003` | [예제 7.3] 자동차 가격 결정 |
| `n_DM_PDF07.car_pricing_example` | `ev_deep_DM_PDF07_node_car_pricing_example` | `DM_PDF07` | `p027` | `p027-L003` | `L003` | [예제 7.3] 자동차 가격 결정 |
| `n_DM_PDF07.kkt_condition` | `ev_deep_DM_PDF07_node_kkt_condition` | `DM_PDF07` | `p039` | `p039-L033` | `L033` | 부등식제약식승수>=0 |
| `ex_DM_PDF07.rectangle_product` | `ev_deep_DM_PDF07_example_rectangle_product` | `DM_PDF07` | `p001` | `p001-L009` | `L009` | Maximize S= X1.X2 |
| `ex_DM_PDF07.car_pricing` | `ev_deep_DM_PDF07_example_car_pricing` | `DM_PDF07` | `p027` | `p027-L003` | `L003` | [예제 7.3] 자동차 가격 결정 |
| `ex_DM_PDF07.kkt_check` | `ev_deep_DM_PDF07_example_kkt_check` | `DM_PDF07` | `p046` | `p046-L003` | `L003` | 그리고 위에서 구한 KKT해가 전체최적해인지 아닌지 판별하라 |

## 16. QC / Extraction Risk Notes

- **page_count:** 46
- **low_text_pages:** 25
- **extraction_risk_pages:** 25
- **QC policy:** 표, 그림, 수식 이미지가 많은 페이지는 전사 텍스트만으로 숫자를 단정하지 않는다. 튜터는 수식 구조와 증거 anchor를 우선 제시하고, 숫자 최적해는 필요 시 원본 PDF를 대조한다.
- DM_PDF07은 저텍스트 페이지가 많아 그래프/수식 페이지는 원본 PDF 대조가 특히 필요하다.
