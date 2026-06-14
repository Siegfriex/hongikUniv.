# DM_PDF04 — Ch.6 정수계획 1주차 최종 RAG 튜터 운영문서

## 0. Document Contract

- **문서 성격:** PDF 요약본이 아니라, 전담 1:1 경영과학 튜터와 RAG agent가 함께 쓰는 증거 기반 운영문서다.
- **source_id:** `DM_PDF04`
- **normalized_pdf:** `decisionMaking/pdf_sources/DM_PDF04_ch06_integer_programming_week1.pdf`
- **primary transcript:** `decisionMaking/pdf_transcripts/DM_PDF04__ch06_integer_programming_week1__full_transcript.md`
- **sidecar:** `decisionMaking/_inventory/DM_PDF04__ch06_integer_programming_week1`
- **flat-pack target:** `decisionMaking/rag_applied_flat_pack/DM_PDF04__04_rag.md`
- **source priority:** 1) PDF 전사본 anchor, 2) 이 문서의 enhanced sidecar, 3) 웹 그라운딩, 4) 일반 OR/MS 지식.
- **중요한 명명 주의:** `DM_PDF04`는 PDF intake index다. 강의 회차/장 번호와 혼동하지 않는다.

### Web Grounding Notes

웹 근거는 PDF 원문을 대체하지 않는다. Solver 구현, LP/MIP/flow 표준 용어, Excel 함수 의미를 보조 확인하기 위해서만 사용한다.

| web_id | role in this RAG | URL |
|---|---|---|
| `WEB_OR_TOOLS_MIP` | Integer and mixed-integer model grounding: integer variables, constraints, objective, MIP solver. | https://developers.google.com/optimization/mip/mip_example |
| `WEB_MS_SOLVERADD` | Excel Solver constraint grounding: adding relational constraints to a solver model. | https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solveradd-function |
| `WEB_MS_SOLVERSOLVE` | Excel Solver execution grounding: solving the configured model. | https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solversolve-function |

## 1. Source Coverage Map

| page | primary anchors | extracted focus | extraction note |
|---|---|---|---|
| p001 | `DM_PDF04:p001:L002, DM_PDF04:p001:L003` | Integer Programming (정수계획법) /  서 론 / 1. 선형 정수계획 모형: 목적함수 및 제한조건식: 선형식 | ok |
| p002 | `DM_PDF04:p002:L002, DM_PDF04:p002:L003` | 서론 (계속) / 4. 정수 계획(IP: integer programming) 모형 / – 순수 정수 계획 모형 (all integer ) : 모든 변수가 정수 조건 | ok |
| p003 | `DM_PDF04:p003:L002, DM_PDF04:p003:L003` | 해찾기 옵션 설정 / 모든 해법 > / 정수 제한 조건으로 해찾기 | LOW_TEXT |
| p004 | `DM_PDF04:p004:L002, DM_PDF04:p004:L003` | 해찾기 옵션 설정 / (해찾기 > 옵션 > 모든해법 > 정수 제한 조건 해찾기) / ① 정수 제한 조건 무시 (∨) 체크 없앤다 | ok |
| p005 | `DM_PDF04:p005:L002, DM_PDF04:p005:L003` |  선형계획 완화 문제 (LP relaxation) /  정수 계획 모형에서 정수 제한조건을 탈락 시키면 선형계획 / 문제가 됨  LP relaxation이라 함 | ok |
| p006 | `DM_PDF04:p006:L002, DM_PDF04:p006:L003` | ※ 정수 최적화 비율: LP relaxation의 최적해와 비교 / 엑셀 해찾기에서 정수 최적화 비율 1% 계산: /  정수계획 최적해 대신 LP relaxation의 최적 | ok |
| p007 | `DM_PDF04:p007:L002, DM_PDF04:p007:L003` | 정수계획 모델 문제 및 해법 / 1. 0-1 Knapsack Problem (배낭문제) / 2. Capital budgeting model (자금운용 모형) | ok |
| p008 | `DM_PDF04:p008:L002, DM_PDF04:p008:L003` | 6.3 0-1 배낭문제 (0-1 Knapsack Problem) / - 포함 총가치가 최대화 되도록 배낭에 넣을 물건 선택하는 문제 / - 하나의 제약식 (무게 한도 제약) | ok |
| p009 | `DM_PDF04:p009:L001, DM_PDF04:p009:L002` | 9수리모형 / - xj: 보물 j의 선택여부 (0-1 변수) / Maximize 70x1+20x2+39x3+37x4+11x5+7x6+5x7 | ok |
| p010 | `DM_PDF04:p010:L002, DM_PDF04:p010:L003` | 0-1 배낭문제 LP 완화문제 : C/B 분석 적용 / Maximize 70x1+20x2+39x3+37x4+11x5+7x6+5x7 / Subject to 31x1+10x2+20x3+19x4+6x5+4x6+3x7 <= 49 | ok |
| p011 | `DM_PDF04:p011:L002, DM_PDF04:p011:L003` | 스프레드시트 모형 (정수 최적해) / - 보물 선택여부 (변수셀) <- 2진수 (binary) / - 배낭에 넣은 보물의 총 가치 (목표셀) | ok |
| p012 | `DM_PDF04:p012:L002, DM_PDF04:p012:L003` | 6.4 자금 운용 모형 (Capital budgeting model) / 예산 제약 하에서 투자 프로젝트를 선택하는 모형 / • [예제 6.3] 정보통신원의 포로젝트 선정하기 | ok |
| p013 | `DM_PDF04:p013:L002, DM_PDF04:p013:L003` | 어떤 프로젝트들을 기술개발 계획에 포함시키나? / 프로젝트 선정 여부 : 의사결정변수 / 프로젝트명 | ok |
| p014 | `DM_PDF04:p014:L002, DM_PDF04:p014:L003` |  수학적 모형 (제약식이 다수인 Knapsack Problem) / 1. 의사결정변수 / Xj = 프로젝트 j의 선택여부 (0-1변수) | ok |
| p015 | `DM_PDF04:p015:L002, DM_PDF04:p015:L003` |  스프레드시트 모형화 / 1. 변수셀: / – 프로젝트의 선택 여부  0-1 변수 | ok |
| p016 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p017 | `DM_PDF04:p017:L002` | – 해찾기 실행 | LOW_TEXT |
| p018 | `DM_PDF04:p018:L002, DM_PDF04:p018:L003` | [모델링 이슈 1] 예산 조건 고려한 모형 /  전년도에서 남은 예산을 다음 해로 이월하여 / 추가로 지원할 수 있는 경우: | ok |
| p019 | `DM_PDF04:p019:L002, DM_PDF04:p019:L003` | [모델링 이슈 2] 정책적인 선정 조건 고려한 모형 (다음 시트에서) / 프로젝트 1, 2, 3은 CDMA 관련 분야: 최대 2개만 선정 / 프로젝트 4, 5는 차세대 완전 광통신 기술 관련 분야: | ok |
| p020 | `DM_PDF04:p020:L002, DM_PDF04:p020:L003` | (조건1) 프로젝트 1, 2, 3 중 최대 2개만 선정 / (조건2) 프로젝트 5가 선정되려면 프로젝트 4가 선정되어야 함 / (조건3) 프로젝트 6과 7 중 하나만(선정개수 =1) 선정 | ok |
| p021 | `DM_PDF04:p021:L002, DM_PDF04:p021:L003` |  [모델링 이슈 2] 모형예 / 프로젝트 1, 2, 3 중 최대 2개만 선정 /  SUM(B17:D17) <= 2 (x1+x2+x3 <= 2) | ok |
| p022 | `DM_PDF04:p022:L002, DM_PDF04:p022:L003` | 6.5 고정비용모형(Fixed-charge model) / • 총비용 = 고정비+변동비 / – 고정비 = 생산량에 관계없이 생산이 시작되면 발생(Fixed | ok |
| p023 | `DM_PDF04:p023:L002, DM_PDF04:p023:L003` | Fixed-charge model의 어려운 점 / • 쉬운 모형: 비용=고정비 + (생산량)*변동생산비 / • 어려운 | ok |
| p024 | `DM_PDF04:p024:L002, DM_PDF04:p024:L003` | [예제6.4] 삼부 컴퓨터의 고정비용 문제 / – 국민PC, 신제품 모델 개발: 판매가격(175만원) / – 년간 10,000 대 판매 예상 | ok |
| p025 | `DM_PDF04:p025:L002, DM_PDF04:p025:L003` | 모형화 가이드 / • 각 공장의 가동여부 ⇒ 변수셀 (0-1변수) 두 종류 / • 각 공장의 생산량 ⇒ 변수셀(실수변수 OK) | ok |
| p026 | `DM_PDF04:p026:L002, DM_PDF04:p026:L003` | 모형화 가이드(계속) / • 공장가동여부와 생산량과의 논리적 제한식 / 공장1의 생산량(변수셀) | ok |
| p027 | `DM_PDF04:p027:L002, DM_PDF04:p027:L003` |  수학적 모형 / 1. 의사결정변수 / xj = 공장 j의 생산량 변수, yj = 공장 j의 가동여부 (0-1변수) | ok |
| p028 | `DM_PDF04:p028:L002, DM_PDF04:p028:L003` | 스프레드시트 모형화 / 유효생산용량 B24 =B7*B20, C24 =C7*C20, … / 판매수익=수요량*판매가 | LOW_TEXT |
| p029 | `DM_PDF04:p029:L002, DM_PDF04:p029:L003` | 해찾기 실행 / 공장가동여부 결정변수 | LOW_TEXT |
| p030 | `DM_PDF04:p030:L002, DM_PDF04:p030:L003` | 모델링 이슈 / • 고정비용 처리 : IF함수로도 가능하나… / 공장1의 고장 비용(억원) “= IF(B22>0, 45, 0)” | ok |
| p031 | `DM_PDF04:p031:L002, DM_PDF04:p031:L003` | 6.9 최소 생산량 모형 / • 생산을 안 하던지 또는 최소생산량 이상을 생산해야만 하 / 는 경우 (either - or - constraint) | ok |
| p032 | `DM_PDF04:p032:L002, DM_PDF04:p032:L003` |  모형화 가이드 / – 공장 가동 여부  변수셀 ( 0-1 변수 ) / – 생산량 및 최소생산량과의 관계 | ok |
| p033 | `DM_PDF04:p033:L002, DM_PDF04:p033:L003` |  수학적 모형 / 1. 의사결정변수 / xj = 공장 j의 생산량 변수, yj = 공장 j의 가동여부 (0-1변수) | ok |
| p034 | `DM_PDF04:p034:L002` | – 스프레드시트 모형 개발 | LOW_TEXT |
| p035 | `DM_PDF04:p035:L002, DM_PDF04:p035:L003` | 6.7 생산-분배와 결합된 고정비용모형 / • 생산 및 수송계획에서의 고정비용 모형 (공장  창고) / • 배송계획에서의 고정비용 모형 (창고  고객지) | ok |
| p036 | `DM_PDF04:p036:L002, DM_PDF04:p036:L003` | • 표 6.6 : (생산+수송)단가, 고정비용, 생산용량 / • 표 6.7 : 배송단가, 고정비용, 수요량 | LOW_TEXT |
| p037 | `DM_PDF04:p037:L002, DM_PDF04:p037:L003` | • 어느 공장을 가동할 것인가? / • 어느 물류 창고를 가동할 것인가? / • (생산량)수송량이 결정되어야 한다. | ok |
| p038 | `DM_PDF04:p038:L002, DM_PDF04:p038:L003` | 모형화 가이드 /  공장 가동 여부 ⇒ 변수셀(0-1변수) /  창고 가동 여부 ⇒ 변수셀(0-1변수) | ok |
| p039 | `DM_PDF04:p039:L002, DM_PDF04:p039:L003` | 수학적 모형 / 1. 의사결정변수 / xij = 공장 i에서 창고 j로의 수송량 변수, (i=1,2,3,4 ; j=1,2,3) | ok |
| p040 | `DM_PDF04:p040:L002` | 스프레드 시트 모형화 | LOW_TEXT |
| p041 | `DM_PDF04:p041:L002, DM_PDF04:p041:L003` | 스프레드 시트 모형개발(뒷면) / 창고용량 없을 때 / xij | LOW_TEXT |
| p042 | `DM_PDF04:p042:L002, DM_PDF04:p042:L003` |  해찾기 실행 /  해찾기가 정수 최적해를 잘 구해 주지 못할 때 / 실수 최적해부터 구한 뒤, 이를 초기해로 놓고 2진조건(bin) | ok |
| p043 | `DM_PDF04:p043:L002, DM_PDF04:p043:L003` | 실습문제 #1 / P.13 문제 스프레드 시트 모형 만들기 | LOW_TEXT |
| p044 | `DM_PDF04:p044:L002, DM_PDF04:p044:L003` | 실습문제 #2 (**제출 안해도 감점 없음) / 클래스넷에 올려 놓은 한글파일을 보고 할 것 / [1] 실습문제 2번 --- sheet1 | ok |

## 2. Chapter Thesis

정수계획은 LP의 변수 일부 또는 전부에 정수/0-1 의미를 부여해 개수, 선택, 개방 여부 같은 불연속 의사결정을 모델링한다.

## 3. Current Graph Position

- **현재 그래프 위치:** LP formulation -> integer/binary domains -> Solver int/bin settings -> knapsack/capital budgeting/fixed-charge/facility-production models.
- **지금 보는 노드:** `DM_PDF04` / Ch.6 정수계획 1주차
- **튜터 운영 원칙:** 질문이 들어오면 먼저 노드로 매핑하고, 예제 카드와 수식/Solver 구조를 거쳐 Source Trace Table의 evidence anchor로 되돌아간다.

## 4. Learning Outcomes

- 순수정수, 혼합정수, 0-1 정수계획을 구분한다.
- 0-1 배낭, 자본예산, fixed-charge model의 변수와 논리제약을 세운다.
- Solver의 정수 최적화 비율과 bin/int 조건을 해석한다.

## 5. Concept Graph Map

| node_id | 개념 | 역할 | 선행 노드 | 후속 노드 |
| --- | --- | --- | --- | --- |
| `n_DM_PDF04.integer_programming` | 정수계획 | 목적함수와 제약은 선형이지만 변수에 정수 또는 0-1 조건이 붙는 최적화 모형이다. | LP formulation | branch and bound |
| `n_DM_PDF04.pure_mixed_binary_ip` | 순수/혼합/0-1 IP | 모든 변수가 정수면 순수정수, 일부만 정수면 혼합정수, 모든 변수가 0/1이면 0-1 정수계획이다. | variable definition | model classification |
| `n_DM_PDF04.solver_integer_tolerance` | Solver 정수 최적화 비율 | Solver가 LP 완화 최적값 대비 현재 정수해가 충분히 가까우면 멈출 수 있게 하는 gap 기준이다. | integer programming | branch-and-bound gap |
| `n_DM_PDF04.knapsack_problem` | 0-1 배낭문제 | 제한된 용량 안에서 선택가치 합을 최대화하도록 물건 선택 여부를 0/1로 결정하는 모형이다. | binary variable | capital budgeting |
| `n_DM_PDF04.lp_relaxation_ratio` | 배낭 LP 완화와 효과/비용 | 0-1 조건을 풀면 효과/비용 순으로 fractional 할당해 완화해를 쉽게 얻을 수 있다. | knapsack | branch-and-bound |
| `n_DM_PDF04.capital_budgeting` | 자본예산 선택 | 예산 제약 하에서 투자 프로젝트 선택 여부를 0-1로 결정하는 모형이다. | knapsack_problem | fixed_charge/logical constraints |
| `n_DM_PDF04.fixed_charge_model` | 고정비용모형 | 생산을 시작하면 고정비가 발생하고 생산량에는 변동비가 붙는 비용구조를 0-1 변수로 모델링하는 모형이다. | binary variable | facility location |
| `n_DM_PDF04.minimum_production_logic` | 최소생산량 논리제약 | 공장을 열면 최소생산량 이상, 닫으면 0이 되도록 하한/상한을 binary와 연결하는 제약이다. | fixed_charge_model | facility network |
| `n_DM_PDF04.production_distribution_fixed_charge` | 생산-분배 결합 고정비 | 공장/창고 개방 여부와 생산/수송/배송량을 동시에 결정하는 혼합정수 네트워크 모형이다. | fixed_charge_model | transportation network |

### Edge List

| from | edge_type | to |
| --- | --- | --- |
| `LP formulation` | 선행 관계 | `n_DM_PDF04.integer_programming` |
| `n_DM_PDF04.integer_programming` | 후속 관계 | `branch and bound` |
| `n_DM_PDF04.integer_programming` | 동형/유사 | `discrete optimization` |
| `variable definition` | 선행 관계 | `n_DM_PDF04.pure_mixed_binary_ip` |
| `n_DM_PDF04.pure_mixed_binary_ip` | 후속 관계 | `model classification` |
| `n_DM_PDF04.pure_mixed_binary_ip` | 동형/유사 | `domain modeling` |
| `integer programming` | 선행 관계 | `n_DM_PDF04.solver_integer_tolerance` |
| `n_DM_PDF04.solver_integer_tolerance` | 후속 관계 | `branch-and-bound gap` |
| `n_DM_PDF04.solver_integer_tolerance` | 동형/유사 | `MIP solver settings` |
| `binary variable` | 선행 관계 | `n_DM_PDF04.knapsack_problem` |
| `n_DM_PDF04.knapsack_problem` | 후속 관계 | `capital budgeting` |
| `n_DM_PDF04.knapsack_problem` | 동형/유사 | `resource allocation` |
| `knapsack` | 선행 관계 | `n_DM_PDF04.lp_relaxation_ratio` |
| `n_DM_PDF04.lp_relaxation_ratio` | 후속 관계 | `branch-and-bound` |
| `n_DM_PDF04.lp_relaxation_ratio` | 동형/유사 | `greedy fractional knapsack` |
| `knapsack_problem` | 선행 관계 | `n_DM_PDF04.capital_budgeting` |
| `n_DM_PDF04.capital_budgeting` | 후속 관계 | `fixed_charge/logical constraints` |
| `n_DM_PDF04.capital_budgeting` | 동형/유사 | `portfolio selection` |
| `binary variable` | 선행 관계 | `n_DM_PDF04.fixed_charge_model` |
| `n_DM_PDF04.fixed_charge_model` | 후속 관계 | `facility location` |
| `n_DM_PDF04.fixed_charge_model` | 동형/유사 | `big-M implication` |
| `fixed_charge_model` | 선행 관계 | `n_DM_PDF04.minimum_production_logic` |
| `n_DM_PDF04.minimum_production_logic` | 후속 관계 | `facility network` |
| `n_DM_PDF04.minimum_production_logic` | 동형/유사 | `semi-continuous variable` |
| `fixed_charge_model` | 선행 관계 | `n_DM_PDF04.production_distribution_fixed_charge` |
| `n_DM_PDF04.production_distribution_fixed_charge` | 후속 관계 | `transportation network` |
| `n_DM_PDF04.production_distribution_fixed_charge` | 동형/유사 | `facility location` |

## 6. Core Concept Node Cards

### n_DM_PDF04.integer_programming — 정수계획 (integer programming)

1. **한 줄 정의:** 목적함수와 제약은 선형이지만 변수에 정수 또는 0-1 조건이 붙는 최적화 모형이다.
2. **쉬운 직관:** 사람 수, 공장 개방 여부, 프로젝트 선택처럼 쪼갤 수 없는 결정을 다룬다.
3. **언제 쓰는가:** LP 해가 소수로 나오면 현실 의사결정이 불가능한 경우에 쓴다.
4. **변수 정의:** x_j integer 또는 binary.
5. **목적함수:** LP와 같은 선형 목적함수를 유지한다.
6. **제약식:** 선형 제약 + integrality domain.
7. **수식의 현실 의미:** 공장 가동 여부는 0/1, 생산량은 연속 또는 정수일 수 있다.
8. **그래프/네트워크 관점:** LP 가능영역 중 정수 격자점만 허용한다.
9. **스프레드시트/Solver 관점:** Solver에서 변수셀에 int/bin 제약을 추가한다.
10. **강의 예제 연결:** 정수계획 적용 상황 전체.
11. **예제 숫자 해석:** 실수 최적해와 정수 최적해 목적값이 다를 수 있다.
12. **자주 하는 실수:** LP 해를 반올림해 정수 최적해로 쓰는 오류.
13. **선행 노드:** LP formulation
14. **후속 노드:** branch and bound
15. **동형/유사 노드:** discrete optimization
16. **시험 출제 포인트:** 정수조건 추가 이유.
17. **RAG retrieval tags:** `integer_programming`, `정수계획`
18. **Evidence anchors:** `ev_deep_DM_PDF04_node_integer_programming` -> `DM_PDF04:p001:L002` / source_id=`DM_PDF04`, page=`p001`, block=`p001-L002`, line=`L002`

> 근거 excerpt: Integer Programming (정수계획법)

### n_DM_PDF04.pure_mixed_binary_ip — 순수/혼합/0-1 IP (pure/mixed/binary IP)

1. **한 줄 정의:** 모든 변수가 정수면 순수정수, 일부만 정수면 혼합정수, 모든 변수가 0/1이면 0-1 정수계획이다.
2. **쉬운 직관:** 변수의 의미가 개수인지 선택인지 연속 생산량인지에 따라 도메인이 달라진다.
3. **언제 쓰는가:** 문제 유형을 먼저 분류할 때 쓴다.
4. **변수 정의:** integer x, continuous x, binary y.
5. **목적함수:** 목적함수 자체보다 변수 도메인이 분류 기준이다.
6. **제약식:** x integer, y in {0,1} 같은 domain constraints.
7. **수식의 현실 의미:** 생산량은 연속이고 공장 가동여부는 0/1이면 혼합정수다.
8. **그래프/네트워크 관점:** feasible lattice 또는 binary hypercube.
9. **스프레드시트/Solver 관점:** Solver에서는 int와 bin 조건을 따로 지정한다.
10. **강의 예제 연결:** p002의 세 유형 구분.
11. **예제 숫자 해석:** all integer/mixed integer/0-1 integer.
12. **자주 하는 실수:** 0-1 변수에 별도 비음조건을 중복해 핵심을 흐리는 오류.
13. **선행 노드:** variable definition
14. **후속 노드:** model classification
15. **동형/유사 노드:** domain modeling
16. **시험 출제 포인트:** 유형 판별.
17. **RAG retrieval tags:** `pure`, `mixed`, `binary`, `0-1`
18. **Evidence anchors:** `ev_deep_DM_PDF04_node_pure_mixed_binary_ip` -> `DM_PDF04:p002:L004` / source_id=`DM_PDF04`, page=`p002`, block=`p002-L004`, line=`L004`

> 근거 excerpt: – 순수 정수 계획 모형 (all integer ) : 모든 변수가 정수 조건

### n_DM_PDF04.solver_integer_tolerance — Solver 정수 최적화 비율 (integer optimality tolerance)

1. **한 줄 정의:** Solver가 LP 완화 최적값 대비 현재 정수해가 충분히 가까우면 멈출 수 있게 하는 gap 기준이다.
2. **쉬운 직관:** 정확한 증명 대신 계산시간과 정확도 사이의 타협값이다.
3. **언제 쓰는가:** Excel Solver에서 정수해가 기대와 다를 때 확인한다.
4. **변수 정의:** objective incumbent and relaxation bound.
5. **목적함수:** gap percent 기준으로 종료할 수 있다.
6. **제약식:** 정수조건 무시 체크 해제와 최적화 비율 설정이 필요하다.
7. **수식의 현실 의미:** 1% gap이면 완전 최적 전 정수해를 반환할 수 있다.
8. **그래프/네트워크 관점:** branch-and-bound gap interpretation.
9. **스프레드시트/Solver 관점:** Solver 옵션의 모든해법/정수 제한조건 설정.
10. **강의 예제 연결:** p004-p006 Solver 옵션 설명.
11. **예제 숫자 해석:** 0% 설정은 더 정확하지만 시간이 늘 수 있다.
12. **자주 하는 실수:** 정수조건을 체크하지 않고 연속 LP 해를 받은 뒤 최적이라고 하는 오류.
13. **선행 노드:** integer programming
14. **후속 노드:** branch-and-bound gap
15. **동형/유사 노드:** MIP solver settings
16. **시험 출제 포인트:** Solver 옵션 해석.
17. **RAG retrieval tags:** `solver`, `integer_tolerance`, `gap`
18. **Evidence anchors:** `ev_deep_DM_PDF04_node_solver_integer_tolerance` -> `DM_PDF04:p003:L006` / source_id=`DM_PDF04`, page=`p003`, block=`p003-L006`, line=`L006`

> 근거 excerpt: 정수 최적화 비율의

### n_DM_PDF04.knapsack_problem — 0-1 배낭문제 (0-1 knapsack problem)

1. **한 줄 정의:** 제한된 용량 안에서 선택가치 합을 최대화하도록 물건 선택 여부를 0/1로 결정하는 모형이다.
2. **쉬운 직관:** 가방 무게 한도 안에서 어떤 보물을 넣을지 고르는 문제다.
3. **언제 쓰는가:** 한 개 또는 소수의 자원제약 아래 선택 문제에 쓴다.
4. **변수 정의:** x_j=보물 j 선택 여부.
5. **목적함수:** max sum value_j x_j.
6. **제약식:** sum weight_j x_j <= capacity, x_j in {0,1}.
7. **수식의 현실 의미:** 선택하면 전체 물건이 들어가고 일부만 넣을 수 없다.
8. **그래프/네트워크 관점:** 0-1 hypercube와 용량 반공간의 교집합.
9. **스프레드시트/Solver 관점:** Solver 변수셀을 binary로 설정하고 무게합<=한도.
10. **강의 예제 연결:** 보물 선택여부 예제.
11. **예제 숫자 해석:** LP 완화에서는 fractional item이 나올 수 있다.
12. **자주 하는 실수:** LP 완화의 fractional 선택을 실제 선택으로 해석하는 오류.
13. **선행 노드:** binary variable
14. **후속 노드:** capital budgeting
15. **동형/유사 노드:** resource allocation
16. **시험 출제 포인트:** 배낭 식 세우기.
17. **RAG retrieval tags:** `knapsack`, `배낭`
18. **Evidence anchors:** `ev_deep_DM_PDF04_node_knapsack_problem` -> `DM_PDF04:p007:L003` / source_id=`DM_PDF04`, page=`p007`, block=`p007-L003`, line=`L003`

> 근거 excerpt: 1. 0-1 Knapsack Problem (배낭문제)

### n_DM_PDF04.lp_relaxation_ratio — 배낭 LP 완화와 효과/비용 (knapsack LP relaxation ratio)

1. **한 줄 정의:** 0-1 조건을 풀면 효과/비용 순으로 fractional 할당해 완화해를 쉽게 얻을 수 있다.
2. **쉬운 직관:** 물건을 쪼갤 수 있다고 가정하면 효율 좋은 것부터 담는다.
3. **언제 쓰는가:** branch-and-bound bound 계산을 이해할 때 쓴다.
4. **변수 정의:** 0<=x_j<=1 continuous variables.
5. **목적함수:** max value per unit capacity.
6. **제약식:** capacity constraint remains.
7. **수식의 현실 의미:** x3=8/20처럼 일부 선택이 허용되는 완화해다.
8. **그래프/네트워크 관점:** continuous knapsack upper bound.
9. **스프레드시트/Solver 관점:** Solver에서 bin 조건 대신 0<=x<=1 연속으로 둔다.
10. **강의 예제 연결:** p010 C/B 분석.
11. **예제 숫자 해석:** 총가치=70+20+39*(8/20).
12. **자주 하는 실수:** 완화해를 원 0-1 해로 착각.
13. **선행 노드:** knapsack
14. **후속 노드:** branch-and-bound
15. **동형/유사 노드:** greedy fractional knapsack
16. **시험 출제 포인트:** LP relaxation 계산.
17. **RAG retrieval tags:** `LP_relaxation`, `C/B`, `ratio`
18. **Evidence anchors:** `ev_deep_DM_PDF04_node_lp_relaxation_ratio` -> `DM_PDF04:p005:L002` / source_id=`DM_PDF04`, page=`p005`, block=`p005-L002`, line=`L002`

> 근거 excerpt:  선형계획 완화 문제 (LP relaxation)

### n_DM_PDF04.capital_budgeting — 자본예산 선택 (capital budgeting selection)

1. **한 줄 정의:** 예산 제약 하에서 투자 프로젝트 선택 여부를 0-1로 결정하는 모형이다.
2. **쉬운 직관:** 한정된 예산으로 어떤 프로젝트를 채택할지 고른다.
3. **언제 쓰는가:** 프로젝트 채택/미채택 의사결정에 쓴다.
4. **변수 정의:** x_j=프로젝트 j 선택 여부.
5. **목적함수:** max total return or NPV.
6. **제약식:** sum required_budget_j x_j <= budget and logical constraints.
7. **수식의 현실 의미:** 프로젝트는 보통 절반만 채택할 수 없으므로 binary다.
8. **그래프/네트워크 관점:** knapsack의 다중 자원 버전이다.
9. **스프레드시트/Solver 관점:** Solver binary variables and budget constraints.
10. **강의 예제 연결:** p012-p015 투자 프로젝트 선택.
11. **예제 숫자 해석:** 0-1 변수에는 비음조건보다 binary domain이 핵심이다.
12. **자주 하는 실수:** 예산 지출액을 변수로 두고 선택여부를 잊는 오류.
13. **선행 노드:** knapsack_problem
14. **후속 노드:** fixed_charge/logical constraints
15. **동형/유사 노드:** portfolio selection
16. **시험 출제 포인트:** 자본예산 정식화.
17. **RAG retrieval tags:** `capital_budgeting`, `project`
18. **Evidence anchors:** `ev_deep_DM_PDF04_node_capital_budgeting` -> `DM_PDF04:p012:L003` / source_id=`DM_PDF04`, page=`p012`, block=`p012-L003`, line=`L003`

> 근거 excerpt: 예산 제약 하에서 투자 프로젝트를 선택하는 모형

### n_DM_PDF04.fixed_charge_model — 고정비용모형 (fixed-charge model)

1. **한 줄 정의:** 생산을 시작하면 고정비가 발생하고 생산량에는 변동비가 붙는 비용구조를 0-1 변수로 모델링하는 모형이다.
2. **쉬운 직관:** 공장을 조금이라도 쓰면 문을 여는 비용이 든다.
3. **언제 쓰는가:** 개방 여부와 생산량을 동시에 결정할 때 쓴다.
4. **변수 정의:** x_j=생산량, y_j=가동여부 binary.
5. **목적함수:** profit=max revenue-variable cost-fixed cost or min total cost.
6. **제약식:** x_j <= capacity_j y_j.
7. **수식의 현실 의미:** y=0이면 생산량이 0이 되고 y=1이면 용량까지 생산 가능하다.
8. **그래프/네트워크 관점:** continuous flow variable linked to binary switch.
9. **스프레드시트/Solver 관점:** Solver에서 생산량 변수와 binary 가동여부 변수를 함께 둔다.
10. **강의 예제 연결:** 삼부 컴퓨터 고정비용 문제.
11. **예제 숫자 해석:** 고정비=45y1+25y2+15y3+5y4.
12. **자주 하는 실수:** IF 함수로 고정비를 직접 쓰면 비선형/불안정 모델이 될 수 있다.
13. **선행 노드:** binary variable
14. **후속 노드:** facility location
15. **동형/유사 노드:** big-M implication
16. **시험 출제 포인트:** 논리제약 x<=My.
17. **RAG retrieval tags:** `fixed_charge`, `고정비용`
18. **Evidence anchors:** `ev_deep_DM_PDF04_node_fixed_charge_model` -> `DM_PDF04:p007:L005` / source_id=`DM_PDF04`, page=`p007`, block=`p007-L005`, line=`L005`

> 근거 excerpt: 3. Fixed-charge model (고정비용모형)

### n_DM_PDF04.minimum_production_logic — 최소생산량 논리제약 (minimum production logic)

1. **한 줄 정의:** 공장을 열면 최소생산량 이상, 닫으면 0이 되도록 하한/상한을 binary와 연결하는 제약이다.
2. **쉬운 직관:** 가동한다면 어느 정도 규모 이상은 생산해야 한다는 조건이다.
3. **언제 쓰는가:** 생산 시작 최소량이 있는 fixed-charge 문제에 쓴다.
4. **변수 정의:** x_j production, y_j open binary.
5. **목적함수:** min production cost plus fixed cost.
6. **제약식:** min_j y_j <= x_j <= capacity_j y_j.
7. **수식의 현실 의미:** y=0이면 x=0, y=1이면 최소량과 용량 사이.
8. **그래프/네트워크 관점:** binary switch controls interval.
9. **스프레드시트/Solver 관점:** Solver에 두 개의 선형 제약을 추가한다.
10. **강의 예제 연결:** 콘덴서 생산공장 예제.
11. **예제 숫자 해석:** 최소생산량*y <= 생산량 <= 용량*y.
12. **자주 하는 실수:** 하한식 방향을 반대로 쓰는 오류.
13. **선행 노드:** fixed_charge_model
14. **후속 노드:** facility network
15. **동형/유사 노드:** semi-continuous variable
16. **시험 출제 포인트:** 논리식 방향.
17. **RAG retrieval tags:** `minimum_production`, `logic`
18. **Evidence anchors:** `ev_deep_DM_PDF04_node_minimum_production_logic` -> `DM_PDF04:p007:L006` / source_id=`DM_PDF04`, page=`p007`, block=`p007-L006`, line=`L006`

> 근거 excerpt: 4. Either-or-constraints (최소 생산량 모형)

### n_DM_PDF04.production_distribution_fixed_charge — 생산-분배 결합 고정비 (production-distribution fixed charge)

1. **한 줄 정의:** 공장/창고 개방 여부와 생산/수송/배송량을 동시에 결정하는 혼합정수 네트워크 모형이다.
2. **쉬운 직관:** 시설을 열지 여부와 물량을 어디로 보낼지 한 번에 정한다.
3. **언제 쓰는가:** 공장-창고-고객 네트워크에 고정비가 붙을 때 쓴다.
4. **변수 정의:** x_ij 수송량, w_jk 배송량, y_i 공장개방, z_j 창고운영.
5. **목적함수:** min production+transportation+delivery+fixed costs.
6. **제약식:** 공장/창고 flow balance plus x<=capacity*y, w<=demand*z.
7. **수식의 현실 의미:** 문을 연 시설만 물량을 처리할 수 있다.
8. **그래프/네트워크 관점:** fixed-charge network flow.
9. **스프레드시트/Solver 관점:** Solver에서 array형 변경셀과 binary facility cells를 함께 둔다.
10. **강의 예제 연결:** 청정식품 공장/창고 선정 문제.
11. **예제 숫자 해석:** 4개 공장, 3개 창고, 5개 고객 지역 구조.
12. **자주 하는 실수:** 창고가 닫혀도 배송량이 양수가 되도록 식을 빠뜨리는 오류.
13. **선행 노드:** fixed_charge_model
14. **후속 노드:** transportation network
15. **동형/유사 노드:** facility location
16. **시험 출제 포인트:** 혼합정수 네트워크 식.
17. **RAG retrieval tags:** `production_distribution`, `facility`
18. **Evidence anchors:** `ev_deep_DM_PDF04_node_production_distribution_fixed_charge` -> `DM_PDF04:p007:L007` / source_id=`DM_PDF04`, page=`p007`, block=`p007-L007`, line=`L007`

> 근거 excerpt: 5. Plant/Warehouse location model (생산-분배가 결합된


## 7. Example Walkthrough Cards

### ex_DM_PDF04.treasure_knapsack — 보물 0-1 배낭문제

- **현실 문장 재해석:** 무게 한도 49 안에서 보물 선택가치를 최대화한다.
- **의사결정변수:** x_j=보물 j 선택 여부.
- **목적함수:** max sum value_j x_j.
- **제약식:** sum weight_j x_j<=49, x_j binary.
- **Solver 구조:** Solver binary changing cells.
- **결과 해석:** 선택은 0/1이며 LP 완화의 fractional 해와 구분한다.
- **코칭 순서:**
1. 변수 정의.
2. 무게 제약.
3. binary 설정.
4. 완화해와 정수해 비교.
- **Evidence anchors:** `ev_deep_DM_PDF04_example_treasure_knapsack` -> `DM_PDF04:p009:L002` / page=`p009`, block=`p009-L002`, line=`L002`

> 근거 excerpt: - xj: 보물 j의 선택여부 (0-1 변수)

### ex_DM_PDF04.sambu_fixed_charge — 삼부 컴퓨터 fixed-charge

- **현실 문장 재해석:** 공장별 가동 여부와 생산량을 정해 이익을 최대화한다.
- **의사결정변수:** x_j 생산량, y_j 가동여부.
- **목적함수:** 판매수익-변동비-고정비.
- **제약식:** x_j<=capacity_j y_j.
- **Solver 구조:** Solver mixed-integer model.
- **결과 해석:** 가동하지 않는 공장은 생산량 0이어야 한다.
- **코칭 순서:**
1. 생산량/가동여부를 분리.
2. 고정비를 y로 곱한다.
3. 용량*y 논리식 추가.
- **Evidence anchors:** `ev_deep_DM_PDF04_example_sambu_fixed_charge` -> `DM_PDF04:p024:L002` / page=`p024`, block=`p024-L002`, line=`L002`

> 근거 excerpt: [예제6.4] 삼부 컴퓨터의 고정비용 문제

### ex_DM_PDF04.clean_food_network — 청정식품 생산-분배

- **현실 문장 재해석:** 공장/창고 개방과 수송/배송량을 함께 결정한다.
- **의사결정변수:** x_ij, w_jk, y_i, z_j.
- **목적함수:** min total fixed+variable network cost.
- **제약식:** capacity/opening constraints and warehouse balance.
- **Solver 구조:** MIP with transportation arrays.
- **결과 해석:** 네트워크 LP에 fixed-charge binary가 결합된 구조다.
- **코칭 순서:**
1. 시설 binary.
2. 수송/배송량 array.
3. balance와 linking constraints.
- **Evidence anchors:** `ev_deep_DM_PDF04_example_clean_food_network` -> `DM_PDF04:p035:L008` / page=`p035`, block=`p035-L008`, line=`L008`

> 근거 excerpt: [예제 6.6] 청정식품의 공장/창고 선정 문제


## 8. Modeling Pattern Library

| pattern | 모형화 템플릿 | 먼저 볼 노드 | 연결 노드 |
| --- | --- | --- | --- |
| 선택형 | x_j가 선택 여부이면 binary로 두고 합계/예산 제약을 둔다. | knapsack_problem | capital_budgeting |
| 개방-물량 연결형 | y_j가 0이면 x_j도 0이 되도록 x_j<=M y_j를 둔다. | fixed_charge_model | facility_location |
| 네트워크 결합형 | 수송량 배열과 시설개방 binary를 함께 둔다. | production_distribution_fixed_charge | transportation |

## 9. Spreadsheet / Solver Mapping

| 요소 | Solver/Spreadsheet 대응 | 튜터 해설 포인트 |
| --- | --- | --- |
| 변수셀 | 선택 x_j, 생산량 x_j, 가동여부 y_j | 선택/가동은 bin, 생산량은 연속 또는 정수. |
| 목표셀 | 가치 최대화 또는 비용 최소화/이익 최대화 | 고정비는 binary에 곱한다. |
| 제약셀 | 예산, 용량, x<=M y, balance | 논리제약 방향을 체크한다. |
| 옵션 | 정수조건 무시 해제, 정수 최적화 비율 | 정확해가 필요하면 gap을 0%로 낮춘다. |

## 10. Cross-Chapter Connections

| 연결 대상 | 연결 설명 | 의존/참조 관계 |
| --- | --- | --- |
| DM_PDF03 분지한계 | 정수계획 모형은 branch-and-bound로 풀린다. | IP -> B&B |
| DM_PDF06 수송 | 생산-분배 fixed-charge는 수송 네트워크에 binary 개방을 붙인 모델이다. | transportation + facility binary |
| DM_PDF08 set covering | 0-1 선택변수는 공공설비 입지선정으로 이어진다. | binary selection -> set covering |

## 11. Misconception & Error Diagnosis Bank

| 오답/착각 | 왜 문제인가 | 교정 코칭 | 연결 노드 |
| --- | --- | --- | --- |
| 고정비를 IF 함수로만 처리 | 비선형/불안정 모델이 되고 논리 검증이 어렵다. | binary y와 x<=M y를 쓴다. | fixed_charge_model |
| 0-1 변수에 비음조건만 둠 | 0<=x<=1은 연속값도 허용한다. | bin 또는 int+<=1을 지정한다. | pure_mixed_binary_ip |
| 정수 최적화 비율 무시 | Solver가 gap 허용으로 조기 종료할 수 있다. | 정확한 최적해가 필요하면 옵션 확인. | solver_integer_tolerance |

## 12. Retrieval Routing Table

| 사용자 질문 유형 | 먼저 볼 노드 | 다음 볼 노드 | 예제 카드 | 근거 힌트 |
| --- | --- | --- | --- | --- |
| 정수계획 유형부터 구분해줘 | `pure_mixed_binary_ip` | `integer_programming` | `treasure_knapsack` | DM_PDF04:p002 |
| 배낭문제 식 어떻게 세워? | `knapsack_problem` | `lp_relaxation_ratio` | `treasure_knapsack` | DM_PDF04:p008 |
| 고정비는 어떻게 선형화? | `fixed_charge_model` | `minimum_production_logic` | `sambu_fixed_charge` | DM_PDF04:p022 |
| 공장/창고 개방과 배송을 같이? | `production_distribution_fixed_charge` | `fixed_charge_model` | `clean_food_network` | DM_PDF04:p035 |

## 13. Tutor Session Protocol

1. **지도부터:** Concept Graph Map과 Edge List를 먼저 보여주고, 현재 노드가 전체 OR/MS 흐름에서 어디인지 설명한다.
2. **노드 중심으로:** Core Concept Node Card의 18개 필드를 순서대로 따라가되, 선행/후속/동형 노드를 최소 3개 연결한다.
3. **예제 중심으로:** Example Walkthrough Card를 사용해 현실 문장 -> 변수 -> 목적함수 -> 제약식 -> Solver -> 결과 해석 순서로 진행한다.
4. **문제 풀이 모드:** 사용자가 변수를 먼저 말하게 하고, 목적함수/제약식은 힌트로 한 단계씩 유도한다.
5. **완성 해설 모드:** 위 절차를 생략하지 않고 전체 풀이를 한 번에 제시한다.
6. **암기/정리 모드:** Modeling Pattern Library, Solver Mapping, Misconception Bank만 압축해 제시한다.

## 14. Practice / Check Questions

1. x_j<=capacity_j y_j가 y=0, y=1에서 각각 무슨 뜻인지 설명하라.
2. 0-1 배낭의 LP 완화해가 왜 정수해가 아닐 수 있는지 말하라.
3. 정수 최적화 비율 1%와 0%의 차이를 Solver 운영 관점에서 정리하라.

## 15. Source Trace Table

| RAG label | evidence_id | source_id | page | block | line | excerpt |
| --- | --- | --- | --- | --- | --- | --- |
| `n_DM_PDF04.integer_programming` | `ev_deep_DM_PDF04_node_integer_programming` | `DM_PDF04` | `p001` | `p001-L002` | `L002` | Integer Programming (정수계획법) |
| `n_DM_PDF04.pure_mixed_binary_ip` | `ev_deep_DM_PDF04_node_pure_mixed_binary_ip` | `DM_PDF04` | `p002` | `p002-L004` | `L004` | – 순수 정수 계획 모형 (all integer ) : 모든 변수가 정수 조건 |
| `n_DM_PDF04.solver_integer_tolerance` | `ev_deep_DM_PDF04_node_solver_integer_tolerance` | `DM_PDF04` | `p003` | `p003-L006` | `L006` | 정수 최적화 비율의 |
| `n_DM_PDF04.knapsack_problem` | `ev_deep_DM_PDF04_node_knapsack_problem` | `DM_PDF04` | `p007` | `p007-L003` | `L003` | 1. 0-1 Knapsack Problem (배낭문제) |
| `n_DM_PDF04.lp_relaxation_ratio` | `ev_deep_DM_PDF04_node_lp_relaxation_ratio` | `DM_PDF04` | `p005` | `p005-L002` | `L002` |  선형계획 완화 문제 (LP relaxation) |
| `n_DM_PDF04.capital_budgeting` | `ev_deep_DM_PDF04_node_capital_budgeting` | `DM_PDF04` | `p012` | `p012-L003` | `L003` | 예산 제약 하에서 투자 프로젝트를 선택하는 모형 |
| `n_DM_PDF04.fixed_charge_model` | `ev_deep_DM_PDF04_node_fixed_charge_model` | `DM_PDF04` | `p007` | `p007-L005` | `L005` | 3. Fixed-charge model (고정비용모형) |
| `n_DM_PDF04.minimum_production_logic` | `ev_deep_DM_PDF04_node_minimum_production_logic` | `DM_PDF04` | `p007` | `p007-L006` | `L006` | 4. Either-or-constraints (최소 생산량 모형) |
| `n_DM_PDF04.production_distribution_fixed_charge` | `ev_deep_DM_PDF04_node_production_distribution_fixed_charge` | `DM_PDF04` | `p007` | `p007-L007` | `L007` | 5. Plant/Warehouse location model (생산-분배가 결합된 |
| `ex_DM_PDF04.treasure_knapsack` | `ev_deep_DM_PDF04_example_treasure_knapsack` | `DM_PDF04` | `p009` | `p009-L002` | `L002` | - xj: 보물 j의 선택여부 (0-1 변수) |
| `ex_DM_PDF04.sambu_fixed_charge` | `ev_deep_DM_PDF04_example_sambu_fixed_charge` | `DM_PDF04` | `p024` | `p024-L002` | `L002` | [예제6.4] 삼부 컴퓨터의 고정비용 문제 |
| `ex_DM_PDF04.clean_food_network` | `ev_deep_DM_PDF04_example_clean_food_network` | `DM_PDF04` | `p035` | `p035-L008` | `L008` | [예제 6.6] 청정식품의 공장/창고 선정 문제 |

## 16. QC / Extraction Risk Notes

- **page_count:** 44
- **low_text_pages:** 10
- **extraction_risk_pages:** 10
- **QC policy:** 표, 그림, 수식 이미지가 많은 페이지는 전사 텍스트만으로 숫자를 단정하지 않는다. 튜터는 수식 구조와 증거 anchor를 우선 제시하고, 숫자 최적해는 필요 시 원본 PDF를 대조한다.
- 표가 많은 페이지는 OCR 누락 가능성이 있어 계수표 원본 대조가 필요하다.
