# DM_PDF05 — Ch.4 심플렉스, Big-M, 쌍대성 연결 최종 RAG 튜터 운영문서

## 0. Document Contract

- **문서 성격:** PDF 요약본이 아니라, 전담 1:1 경영과학 튜터와 RAG agent가 함께 쓰는 증거 기반 운영문서다.
- **source_id:** `DM_PDF05`
- **normalized_pdf:** `decisionMaking/pdf_sources/DM_PDF05_ch04_simplex_duality_week2.pdf`
- **primary transcript:** `decisionMaking/pdf_transcripts/DM_PDF05__ch04_simplex_duality_week2__full_transcript.md`
- **sidecar:** `decisionMaking/_inventory/DM_PDF05__ch04_simplex_duality_week2`
- **flat-pack target:** `decisionMaking/rag_applied_flat_pack/DM_PDF05__04_rag.md`
- **source priority:** 1) PDF 전사본 anchor, 2) 이 문서의 enhanced sidecar, 3) 웹 그라운딩, 4) 일반 OR/MS 지식.
- **중요한 명명 주의:** `DM_PDF05`는 PDF intake index다. 강의 회차/장 번호와 혼동하지 않는다.

### Web Grounding Notes

웹 근거는 PDF 원문을 대체하지 않는다. Solver 구현, LP/MIP/flow 표준 용어, Excel 함수 의미를 보조 확인하기 위해서만 사용한다.

| web_id | role in this RAG | URL |
|---|---|---|
| `WEB_OR_TOOLS_LP` | LP/Simplex-style solver model grounding: variables, constraints, objective, optimal solution. | https://developers.google.com/optimization/lp/lp_example |
| `WEB_MS_SOLVERADD` | Excel Solver constraint grounding: adding relational constraints to a solver model. | https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solveradd-function |
| `WEB_MS_SOLVERSOLVE` | Excel Solver execution grounding: solving the configured model. | https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solversolve-function |

## 1. Source Coverage Map

| page | primary anchors | extracted focus | extraction note |
|---|---|---|---|
| p001 | `DM_PDF05:p001:L002, DM_PDF05:p001:L003` | 심플렉스법, 2단계해법 / 지난 주 실습문제 #3 / ( 오늘 실습 문제#1로 제출할 것) | ok |
| p002 | `DM_PDF05:p002:L002, DM_PDF05:p002:L003` | 최소화 문제를 최대화 문제로 바꿔 풀 수 있음 / (1) 최소화 선형계획문제 : 식단문제 / Min Z= 35x1 +30x2 +60x3 +50x4 +27x5 +22x6 | ok |
| p003 | `DM_PDF05:p003:L002, DM_PDF05:p003:L003` | 인위변수 도입과 Big-M / (초기 기저가능해 얻을 수 없을 때) / Max -Z +35x1 +30x2 +60x3 +50x4 +27x5 +22x6 = 0 | ok |
| p004 | `DM_PDF05:p004:L002, DM_PDF05:p004:L003` | Big-M method / ※정규형으로 만들어야 심플렉스법 적용 가능함 / Max -Z +35x1 +30x2 +60x3 +50x4 +27x5 +22x6 +M r1+M r2 = 0 | ok |
| p005 | `DM_PDF05:p005:L002, DM_PDF05:p005:L003` | Big-M method(계속) / Max -Z -Mx1 - Mx2 -5Mx3 -3Mx4 -4Mx5-4Mx6+Ms1+Ms2 / +35x1 +30x2 +60x3 +50x4 +27x5 +22x6 =-110M | ok |
| p006 | `DM_PDF05:p006:L002, DM_PDF05:p006:L003` | Big-M method의 타블로 적용(1) / 반복1 / 반복0 | LOW_TEXT |
| p007 | `DM_PDF05:p007:L002, DM_PDF05:p007:L003` | Big-M method의 타블로 적용(2) / • 반복 중 r1, r2가 모두 비기저변수가 되면, 이때부터 얻어지는 해는 / 실행가능해이다. (r1=0 & r2=0 또는 M계수 행의 우변이 0 되는 때) | ok |
| p008 | `DM_PDF05:p008:L002, DM_PDF05:p008:L003` | 실습문제 #2 / Big-M method(타블로 이용)에 의해 최적해를 구하라. / Minimize Z = 3 x1 + 2 x2 + 4 x3 | ok |
| p009 | `DM_PDF05:p009:L002, DM_PDF05:p009:L003` | 복습 (slide 9~12) 2.2 최소화 문제 / • [예제2.2] 박씨의 식단 문제 / – 비타민 A와 C에 대해서 필요한 1일 최소 요구량 이상을 섭취 | ok |
| p010 | `DM_PDF05:p010:L002, DM_PDF05:p010:L003` | • 해찾기 실행 해법선택: LP 심플렉스, 음수 아닌 것으로 체크 / 최적해 / (실수해가 보통임) | LOW_TEXT |
| p011 | `DM_PDF05:p011:L002, DM_PDF05:p011:L003` | xi=비타민 식단에 포함되는 식품 i의 포함량(100g단위) / (i=1,2,3,4,5,6) / Min. 350x1 +300x2 +500x3 +340x4 +270x5 +400x6 | ok |
| p012 | `DM_PDF05:p012:L002, DM_PDF05:p012:L003` | – 민감도 보고서 / • 식품3 한계비용 = 80 / • 비타민A 잠재가격 = 15 | ok |
| p013 | `DM_PDF05:p013:L002, DM_PDF05:p013:L003` | • [예제 4.4] 제약회사의 비타민 가격 결정 / – 비타민 알약을 섭취하여 필요한 1일 최소요구량 섭취가능 / – 제약 회사에서는 표에 있는 6 종류의 식품에서만 비타민 A, | ok |
| p014 | `DM_PDF05:p014:L002, DM_PDF05:p014:L003` | – 수학적 모형 / • 비타민 알약 고객의 요구 사항: / {각 식품 100g에 포함된 비타민을 | ok |
| p015 | `DM_PDF05:p015:L002, DM_PDF05:p015:L003` |  모형화 가이드 / • 변수 셀  비타민 1단위 알략 가격 / • 소비자 입장에서 식품에 있는 비타민을 알약으로 대신하는 비용 계산 | ok |
| p016 | `DM_PDF05:p016:L001, DM_PDF05:p016:L002` | 16– 해찾기 실행 / • 목표 셀 : B21 (최대화) 변수셀 : B12:B13 / • 제한조건 : B16:G16 <= B18:G18 | ok |
| p017 | `DM_PDF05:p017:L002, DM_PDF05:p017:L003` | – 민감도보고서 / • 식품 1 ~ 식품6의 잠재가격 = 0,0,0,1.8,1.4,0 = 식단문제의 최적해 / • 비타민 알약 가격(최적해) =15, 4 = 식단문제의 잠재가격 | ok |
| p018 | `DM_PDF05:p018:L002, DM_PDF05:p018:L003` | (원문제) / Minimize 350x1 +300x2 +500x3 +340x4 +270x5 +400x6 / subject to 10x1 +20x3 +20x4 +10x5 +20x6 >= 50 | ok |
| p019 | `DM_PDF05:p019:L001, DM_PDF05:p019:L002` | – 모든 선형계획 문제에는 쌍대문제가 존재한다. / – 그러나 모든 쌍대문제의 의미를 설명하기는 어렵다. / (예) 제약회사가 없는 상황에서 식단문제의 쌍대문제의 의미를 | ok |
| p020 | `DM_PDF05:p020:L001` | 20원본문제와 쌍대문제의 관계 | LOW_TEXT |
| p021 | `DM_PDF05:p021:L002, DM_PDF05:p021:L003` | (원본 문제) / Maximize 5 x1 + 6 x2 + 7 x3 max 문제에서 / subject to 2 x1 + 3 x2 + 4 x3 <= 60 … y1 (기본형) | ok |
| p022 | `DM_PDF05:p022:L002, DM_PDF05:p022:L003` | (연습1) Max 4 x1 + 6 x2 + 18 x3 / s/t x1 + 3 x3 = 3 / 2 x2 + 2 x3 >= 5 | ok |
| p023 | `DM_PDF05:p023:L002, DM_PDF05:p023:L003` | 4.8 쌍대성 이론 / Maximize Z= 30 x1 + 20 x2 / subject to 8 x1 + 4 x2 <= 240 …… y1 | ok |
| p024 | `DM_PDF05:p024:L002, DM_PDF05:p024:L003` | 약쌍대성 & 강쌍대성 정리 / • 약쌍대성(Weak Duality) / 최대화 문제의 임의의 가능해에 대한 목적함수 값은 | ok |
| p025 | `DM_PDF05:p025:L002, DM_PDF05:p025:L003` | (원본문제,쌍대문제)의 해는 4 Cases / Case 1: 원본문제와 쌍대문제 모두 최적해를 갖고, 두 문제의 / 목적함수 값이 같은 경우. | ok |
| p026 | `DM_PDF05:p026:L002, DM_PDF05:p026:L003` | Case 4의 예 (참고) / (Primal problem) / Maximize Z= x1 + x2 | ok |
| p027 | `DM_PDF05:p027:L002, DM_PDF05:p027:L003` | 상보여유정리 / (Complementary Slackness Theorem) / 원본문제의 가능해와 쌍대문제의 가능해가 각각 최적해가 되 | ok |
| p028 | `DM_PDF05:p028:L002, DM_PDF05:p028:L003` | (원본 문제) 유모차 보행기 자전거 / Max 30x1 + 20x2 + 16x3 / s/t 8 x1 + 3 x2 + 3 x3 <= 240 … y1 (기본형) | ok |
| p029 | `DM_PDF05:p029:L002, DM_PDF05:p029:L003` |  여유없음 /  여유 있음(40) /  여유 있음(20) | LOW_TEXT |
| p030 | `DM_PDF05:p030:L002, DM_PDF05:p030:L003` | 상보여유정리 1 확인: 원본문제 제약여유와 쌍대변수 값 / 원본문제 제약식1  여유없음 / 원본문제 제약식2  여유 있음(40) | ok |
| p031 | `DM_PDF05:p031:L002, DM_PDF05:p031:L003` | 상보여유정리 2 확인: 쌍대문제 제약여유와 원본변수 값 / 쌍대문제 제약식의 여유 = - 한계비용 / 쌍대 문제 첫번째 제약식: | ok |
| p032 | `DM_PDF05:p032:L002, DM_PDF05:p032:L003` | 4.9 심플렉스법을 활용한 민감도 분석 / 1) 한계비용과 잠재가격 /  한계비용: 최적해 타블로에서 목적함수식의 | ok |
| p033 | `DM_PDF05:p033:L002` | 해찾기의 민감도 보고서(확인) | LOW_TEXT |
| p034 | `DM_PDF05:p034:L001, DM_PDF05:p034:L002` | 342) 목적함수 계수의 허용가능 증감 (최적해 타블로에서) /  최적해가 변하지 않는 범위의 해당 목적함수 계수의 범위 /  비기저변수의 허용가능 증가 = 목적함수 계수 (=-한계비용) | ok |
| p035 | `DM_PDF05:p035:L001, DM_PDF05:p035:L002` | 352) 우변값의 허용가능 증감 /  잠재가격이 변하지 않는 범위의 우변값의 범위 /  첫번째 제약식의 경우 : 240  240 + Δ, 즉 우변값은 | ok |
| p036 | `DM_PDF05:p036:L002, DM_PDF05:p036:L003` | 실습문제 #4 최대화 문제 / 1) 변수 x1, x2 의 한계비용 구하기 / 2) 제약식1, 제약식2 의 잠재가격 구하기 | ok |

## 2. Chapter Thesis

Big-M은 인위변수 제거를 벌점 방식으로 처리하고, 쌍대성은 원문제의 자원 제약과 쌍대문제의 가격 변수를 한 쌍으로 연결한다.

## 3. Current Graph Position

- **현재 그래프 위치:** two-phase/artificial variables -> Big-M tableau -> primal-dual transformation -> weak/strong duality -> complementary slackness.
- **지금 보는 노드:** `DM_PDF05` / Ch.4 심플렉스, Big-M, 쌍대성 연결
- **튜터 운영 원칙:** 질문이 들어오면 먼저 노드로 매핑하고, 예제 카드와 수식/Solver 구조를 거쳐 Source Trace Table의 evidence anchor로 되돌아간다.

## 4. Learning Outcomes

- Big-M에서 artificial variable의 벌점 부호를 목적 방향에 맞게 둔다.
- 원본문제와 쌍대문제의 변수-제약 대응을 만든다.
- 약쌍대성, 강쌍대성, 상보여유정리를 민감도 보고서와 연결한다.

## 5. Concept Graph Map

| node_id | 개념 | 역할 | 선행 노드 | 후속 노드 |
| --- | --- | --- | --- | --- |
| `n_DM_PDF05.big_m_method` | Big-M 방법 | 인위변수에 매우 큰 벌점 M을 부여해 최적화 과정에서 artificial variable을 0으로 밀어내는 방법이다. | artificial variable | duality theory |
| `n_DM_PDF05.artificial_variable` | 인위변수 | 초기 기저해를 만들기 위해 원문제에 임시로 추가하는 변수다. | surplus variable | Big-M, two-phase |
| `n_DM_PDF05.surplus_variable` | 잉여변수 | >= 제약을 등식으로 바꾸기 위해 좌변에서 빼는 비음 변수다. | standard form | artificial variable |
| `n_DM_PDF05.diet_problem` | 식단문제 | 필요 영양소 최소요구량을 만족하면서 식품 비용을 최소화하는 LP다. | min LP | dual vitamin pill problem |
| `n_DM_PDF05.dual_problem` | 쌍대문제 | 원본문제의 제약을 변수로, 변수를 제약으로 바꿔 만든 짝 문제다. | primal LP | weak/strong duality |
| `n_DM_PDF05.primal_dual_mapping` | 원문제-쌍대 대응 | 원문제의 각 제약은 쌍대변수 하나에, 원문제의 각 변수는 쌍대제약 하나에 대응한다. | dual_problem | complementary_slackness |
| `n_DM_PDF05.weak_duality` | 약쌍대성 | 최대화 원문제의 임의 가능해 목적값은 최소화 쌍대문제의 임의 가능해 목적값보다 작거나 같다. | dual feasibility | strong duality |
| `n_DM_PDF05.strong_duality` | 강쌍대성 | 원문제와 쌍대문제가 모두 가능해를 가지면 두 문제의 최적 목적값은 같다. | weak_duality | complementary_slackness |
| `n_DM_PDF05.four_duality_cases` | 쌍대성 4가지 경우 | 원문제와 쌍대문제의 optimal/unbounded/infeasible 상태가 서로 제약되는 네 가지 관계다. | weak/strong duality | solver status |
| `n_DM_PDF05.complementary_slackness` | 상보여유정리 | 원문제 제약의 여유와 해당 쌍대변수, 쌍대 제약의 여유와 해당 원변수 중 하나는 반드시 0이어야 하는 최적성 조건이다. | strong_duality | reduced cost/shadow price |
| `n_DM_PDF05.shadow_price_dual_solution` | 잠재가격과 쌍대해 | 민감도 보고서의 잠재가격은 제약에 대응하는 쌍대변수의 최적값으로 해석된다. | dual_problem | sensitivity_analysis |

### Edge List

| from | edge_type | to |
| --- | --- | --- |
| `artificial variable` | 선행 관계 | `n_DM_PDF05.big_m_method` |
| `n_DM_PDF05.big_m_method` | 후속 관계 | `duality theory` |
| `n_DM_PDF05.big_m_method` | 동형/유사 | `two-phase method` |
| `surplus variable` | 선행 관계 | `n_DM_PDF05.artificial_variable` |
| `n_DM_PDF05.artificial_variable` | 후속 관계 | `Big-M, two-phase` |
| `n_DM_PDF05.artificial_variable` | 동형/유사 | `dummy variable과 구분` |
| `standard form` | 선행 관계 | `n_DM_PDF05.surplus_variable` |
| `n_DM_PDF05.surplus_variable` | 후속 관계 | `artificial variable` |
| `n_DM_PDF05.surplus_variable` | 동형/유사 | `slack variable` |
| `min LP` | 선행 관계 | `n_DM_PDF05.diet_problem` |
| `n_DM_PDF05.diet_problem` | 후속 관계 | `dual vitamin pill problem` |
| `n_DM_PDF05.diet_problem` | 동형/유사 | `Stigler diet` |
| `primal LP` | 선행 관계 | `n_DM_PDF05.dual_problem` |
| `n_DM_PDF05.dual_problem` | 후속 관계 | `weak/strong duality` |
| `n_DM_PDF05.dual_problem` | 동형/유사 | `sensitivity report` |
| `dual_problem` | 선행 관계 | `n_DM_PDF05.primal_dual_mapping` |
| `n_DM_PDF05.primal_dual_mapping` | 후속 관계 | `complementary_slackness` |
| `n_DM_PDF05.primal_dual_mapping` | 동형/유사 | `matrix transpose` |
| `dual feasibility` | 선행 관계 | `n_DM_PDF05.weak_duality` |
| `n_DM_PDF05.weak_duality` | 후속 관계 | `strong duality` |
| `n_DM_PDF05.weak_duality` | 동형/유사 | `branch-and-bound bounds` |
| `weak_duality` | 선행 관계 | `n_DM_PDF05.strong_duality` |
| `n_DM_PDF05.strong_duality` | 후속 관계 | `complementary_slackness` |
| `n_DM_PDF05.strong_duality` | 동형/유사 | `KKT for LP` |
| `weak/strong duality` | 선행 관계 | `n_DM_PDF05.four_duality_cases` |
| `n_DM_PDF05.four_duality_cases` | 후속 관계 | `solver status` |
| `n_DM_PDF05.four_duality_cases` | 동형/유사 | `unbounded/infeasible` |
| `strong_duality` | 선행 관계 | `n_DM_PDF05.complementary_slackness` |
| `n_DM_PDF05.complementary_slackness` | 후속 관계 | `reduced cost/shadow price` |
| `n_DM_PDF05.complementary_slackness` | 동형/유사 | `KKT complementarity` |
| `dual_problem` | 선행 관계 | `n_DM_PDF05.shadow_price_dual_solution` |
| `n_DM_PDF05.shadow_price_dual_solution` | 후속 관계 | `sensitivity_analysis` |
| `n_DM_PDF05.shadow_price_dual_solution` | 동형/유사 | `resource valuation` |

## 6. Core Concept Node Cards

### n_DM_PDF05.big_m_method — Big-M 방법 (Big-M method)

1. **한 줄 정의:** 인위변수에 매우 큰 벌점 M을 부여해 최적화 과정에서 artificial variable을 0으로 밀어내는 방법이다.
2. **쉬운 직관:** 임시 발판을 쓰되 최종 답에는 남지 못하도록 큰 벌금을 매긴다.
3. **언제 쓰는가:** 초기 BFS가 없고 2단계법 대신 하나의 목적함수로 처리할 때 쓴다.
4. **변수 정의:** 원변수, surplus, artificial r.
5. **목적함수:** max 문제는 artificial에 -M, min 문제는 +M 성격의 벌점을 둔다.
6. **제약식:** 원 제약 + artificial 도입 후 정규형 tableau.
7. **수식의 현실 의미:** 식단처럼 >= 제약이 있는 문제에서 시작기저를 만든다.
8. **그래프/네트워크 관점:** feasible start를 penalty objective로 찾는다.
9. **스프레드시트/Solver 관점:** Solver 내부 처리와 다르지만 손계산 tableau 훈련에 유용하다.
10. **강의 예제 연결:** p003-p008 Big-M tableau.
11. **예제 숫자 해석:** r1,r2가 목적행에서 소거되어야 한다.
12. **자주 하는 실수:** M 부호를 목적 방향과 반대로 넣는 오류.
13. **선행 노드:** artificial variable
14. **후속 노드:** duality theory
15. **동형/유사 노드:** two-phase method
16. **시험 출제 포인트:** Big-M 부호와 artificial 제거.
17. **RAG retrieval tags:** `big_m`, `M`, `artificial`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_big_m_method` -> `DM_PDF05:p003:L002` / source_id=`DM_PDF05`, page=`p003`, block=`p003-L002`, line=`L002`

> 근거 excerpt: 인위변수 도입과 Big-M

### n_DM_PDF05.artificial_variable — 인위변수 (artificial variable)

1. **한 줄 정의:** 초기 기저해를 만들기 위해 원문제에 임시로 추가하는 변수다.
2. **쉬운 직관:** 계산 시작을 위한 임시 의자지만 최종 해석에는 없어야 한다.
3. **언제 쓰는가:** >= 또는 = 제약에서 slack basis가 없을 때 쓴다.
4. **변수 정의:** r_i>=0 artificial variables.
5. **목적함수:** Big-M 또는 Phase I에서 0이 되도록 유도한다.
6. **제약식:** artificial이 최종 양수면 원 제약을 만족하는 해가 없을 수 있다.
7. **수식의 현실 의미:** 식단 최소요구량 제약에서 도입된다.
8. **그래프/네트워크 관점:** basis construction device.
9. **스프레드시트/Solver 관점:** 수동 tableau의 시작 basis.
10. **강의 예제 연결:** r1, r2 도입.
11. **예제 숫자 해석:** 목적행에서 인위변수 계수를 소거한다.
12. **자주 하는 실수:** 인위변수를 실제 식품량/생산량처럼 해석하는 오류.
13. **선행 노드:** surplus variable
14. **후속 노드:** Big-M, two-phase
15. **동형/유사 노드:** dummy variable과 구분
16. **시험 출제 포인트:** 도입 이유와 제거 조건.
17. **RAG retrieval tags:** `artificial`, `인위변수`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_artificial_variable` -> `DM_PDF05:p003:L009` / source_id=`DM_PDF05`, page=`p003`, block=`p003-L009`, line=`L009`

> 근거 excerpt: 인위변수(artificial variable) r1, r2 을 도입함

### n_DM_PDF05.surplus_variable — 잉여변수 (surplus variable)

1. **한 줄 정의:** >= 제약을 등식으로 바꾸기 위해 좌변에서 빼는 비음 변수다.
2. **쉬운 직관:** 최소 요구량을 얼마나 초과했는지 나타낸다.
3. **언제 쓰는가:** 최소 섭취량, 최소 생산량 같은 >= 제약에 쓴다.
4. **변수 정의:** s_i>=0.
5. **목적함수:** 목적에는 직접 없을 수 있다.
6. **제약식:** a x - s = b.
7. **수식의 현실 의미:** 요구량보다 더 섭취한 영양분 초과량이다.
8. **그래프/네트워크 관점:** constraint transformation.
9. **스프레드시트/Solver 관점:** Solver 제약식에서는 직접 만들 필요 없지만 tableau에서는 필요하다.
10. **강의 예제 연결:** 식단문제 잉여변수 1개와 인위변수 2개 힌트.
11. **예제 숫자 해석:** surplus는 slack과 부호가 반대다.
12. **자주 하는 실수:** <= 제약에도 surplus를 빼는 오류.
13. **선행 노드:** standard form
14. **후속 노드:** artificial variable
15. **동형/유사 노드:** slack variable
16. **시험 출제 포인트:** 부등호별 변수 도입.
17. **RAG retrieval tags:** `surplus`, `잉여`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_surplus_variable` -> `DM_PDF05:p001:L010` / source_id=`DM_PDF05`, page=`p001`, block=`p001-L010`, line=`L010`

> 근거 excerpt: <힌트: 잉여변수 1개, 인위변수 2개가 도입되어야 함>

### n_DM_PDF05.diet_problem — 식단문제 (diet problem)

1. **한 줄 정의:** 필요 영양소 최소요구량을 만족하면서 식품 비용을 최소화하는 LP다.
2. **쉬운 직관:** 영양 기준을 넘기되 가장 싼 조합을 찾는다.
3. **언제 쓰는가:** min LP, duality, Big-M 예제로 쓴다.
4. **변수 정의:** x_i=식품 i 포함량.
5. **목적함수:** min sum cost_i x_i.
6. **제약식:** vitamin A/C intake >= requirement.
7. **수식의 현실 의미:** 식품량은 100g 단위 등으로 해석된다.
8. **그래프/네트워크 관점:** >= halfspaces and cost iso-lines.
9. **스프레드시트/Solver 관점:** Solver 변수셀 식품량, 목표셀 비용, 제약셀 영양섭취량>=요구량.
10. **강의 예제 연결:** 박씨의 식단 문제.
11. **예제 숫자 해석:** x4=1.8, x5=1.4 등 최적 식품량/잠재가격 연결.
12. **자주 하는 실수:** 최소요구량을 <=로 쓰는 오류.
13. **선행 노드:** min LP
14. **후속 노드:** dual vitamin pill problem
15. **동형/유사 노드:** Stigler diet
16. **시험 출제 포인트:** 식단 모형화.
17. **RAG retrieval tags:** `diet`, `식단`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_diet_problem` -> `DM_PDF05:p002:L003` / source_id=`DM_PDF05`, page=`p002`, block=`p002-L003`, line=`L003`

> 근거 excerpt: (1) 최소화 선형계획문제 : 식단문제

### n_DM_PDF05.dual_problem — 쌍대문제 (dual problem)

1. **한 줄 정의:** 원본문제의 제약을 변수로, 변수를 제약으로 바꿔 만든 짝 문제다.
2. **쉬운 직관:** 자원을 직접 배분하는 문제와 그 자원의 가격을 매기는 문제를 동시에 본다.
3. **언제 쓰는가:** LP 해석, 민감도, shadow price를 이해할 때 쓴다.
4. **변수 정의:** primal x, dual y.
5. **목적함수:** max primal이면 dual은 min 형태가 되는 기본 대응이 많다.
6. **제약식:** A, b, c의 행/열 관계가 뒤집힌다.
7. **수식의 현실 의미:** 식단문제의 dual은 비타민 알약 가격 결정 문제로 해석된다.
8. **그래프/네트워크 관점:** constraint-variable transpose relation.
9. **스프레드시트/Solver 관점:** Solver 민감도 보고서의 shadow price와 연결된다.
10. **강의 예제 연결:** p018 쌍대문제 수학적모형.
11. **예제 숫자 해석:** dual objective 50y1+60y2 등.
12. **자주 하는 실수:** 부등호 방향과 변수 부호 제한을 빠뜨리는 오류.
13. **선행 노드:** primal LP
14. **후속 노드:** weak/strong duality
15. **동형/유사 노드:** sensitivity report
16. **시험 출제 포인트:** 쌍대문제 만들기.
17. **RAG retrieval tags:** `dual`, `쌍대`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_dual_problem` -> `DM_PDF05:p013:L009` / source_id=`DM_PDF05`, page=`p013`, block=`p013-L009`, line=`L009`

> 근거 excerpt: 4.7 선형계획의 쌍대문제

### n_DM_PDF05.primal_dual_mapping — 원문제-쌍대 대응 (primal-dual mapping)

1. **한 줄 정의:** 원문제의 각 제약은 쌍대변수 하나에, 원문제의 각 변수는 쌍대제약 하나에 대응한다.
2. **쉬운 직관:** 행과 열을 바꾸면서 자원량과 단위이익의 역할이 바뀐다.
3. **언제 쓰는가:** 쌍대문제를 구성할 때 쓴다.
4. **변수 정의:** A matrix rows/columns.
5. **목적함수:** primal c becomes dual RHS, primal b becomes dual objective coefficient.
6. **제약식:** 부등호 방향에 따라 dual variable sign/domain이 달라진다.
7. **수식의 현실 의미:** 비타민 요구량은 알약 가격 변수와 연결된다.
8. **그래프/네트워크 관점:** matrix transpose graph.
9. **스프레드시트/Solver 관점:** 민감도 보고서의 Constraints/Variable Cells 섹션 대응.
10. **강의 예제 연결:** p020-p021 관계 표.
11. **예제 숫자 해석:** max/min 관계 없이 기본형/역방향/무방향을 구분한다.
12. **자주 하는 실수:** 행/열 개수를 반대로 세는 오류.
13. **선행 노드:** dual_problem
14. **후속 노드:** complementary_slackness
15. **동형/유사 노드:** matrix transpose
16. **시험 출제 포인트:** 변수-제약 개수 대응.
17. **RAG retrieval tags:** `primal_dual`, `mapping`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_primal_dual_mapping` -> `DM_PDF05:p020:L001` / source_id=`DM_PDF05`, page=`p020`, block=`p020-L001`, line=`L001`

> 근거 excerpt: 20원본문제와 쌍대문제의 관계

### n_DM_PDF05.weak_duality — 약쌍대성 (weak duality)

1. **한 줄 정의:** 최대화 원문제의 임의 가능해 목적값은 최소화 쌍대문제의 임의 가능해 목적값보다 작거나 같다.
2. **쉬운 직관:** 생산으로 얻을 수 있는 가치는 자원 가격으로 평가한 상한을 넘을 수 없다.
3. **언제 쓰는가:** 최적성 상한/하한 논리에 쓴다.
4. **변수 정의:** primal feasible x, dual feasible y.
5. **목적함수:** max z(x) <= min w(y).
6. **제약식:** feasible pair condition.
7. **수식의 현실 의미:** 어떤 식단 비용도 유효한 영양소 가격 상한과 비교된다.
8. **그래프/네트워크 관점:** dual bounds.
9. **스프레드시트/Solver 관점:** Solver sensitivity와 bound 해석에 연결된다.
10. **강의 예제 연결:** p024 약쌍대성.
11. **예제 숫자 해석:** 가능해에서 max<=min.
12. **자주 하는 실수:** 최적해에서만 성립한다고 착각하는 오류.
13. **선행 노드:** dual feasibility
14. **후속 노드:** strong duality
15. **동형/유사 노드:** branch-and-bound bounds
16. **시험 출제 포인트:** 부등식 방향.
17. **RAG retrieval tags:** `weak_duality`, `약쌍대`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_weak_duality` -> `DM_PDF05:p024:L002` / source_id=`DM_PDF05`, page=`p024`, block=`p024-L002`, line=`L002`

> 근거 excerpt: 약쌍대성 & 강쌍대성 정리

### n_DM_PDF05.strong_duality — 강쌍대성 (strong duality)

1. **한 줄 정의:** 원문제와 쌍대문제가 모두 가능해를 가지면 두 문제의 최적 목적값은 같다.
2. **쉬운 직관:** 자원 배분의 최적 가치와 자원 가격 평가의 최적 가치가 최종적으로 만난다.
3. **언제 쓰는가:** LP 최적성과 dual solution 해석에 쓴다.
4. **변수 정의:** optimal primal x*, dual y*.
5. **목적함수:** z*=w*.
6. **제약식:** both feasible and bounded in corresponding case.
7. **수식의 현실 의미:** 식단문제 최적비용과 비타민 알약 가격문제 최적수입이 같다.
8. **그래프/네트워크 관점:** primal-dual optimal pair.
9. **스프레드시트/Solver 관점:** Solver shadow price as optimal dual variable.
10. **강의 예제 연결:** p024 강쌍대성.
11. **예제 숫자 해석:** 최적해에서 max=min.
12. **자주 하는 실수:** infeasible/unbounded cases에서도 무조건 같다고 하는 오류.
13. **선행 노드:** weak_duality
14. **후속 노드:** complementary_slackness
15. **동형/유사 노드:** KKT for LP
16. **시험 출제 포인트:** 최적값 같음의 조건.
17. **RAG retrieval tags:** `strong_duality`, `강쌍대`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_strong_duality` -> `DM_PDF05:p024:L002` / source_id=`DM_PDF05`, page=`p024`, block=`p024-L002`, line=`L002`

> 근거 excerpt: 약쌍대성 & 강쌍대성 정리

### n_DM_PDF05.four_duality_cases — 쌍대성 4가지 경우 (four primal-dual cases)

1. **한 줄 정의:** 원문제와 쌍대문제의 optimal/unbounded/infeasible 상태가 서로 제약되는 네 가지 관계다.
2. **쉬운 직관:** 한쪽이 무한히 좋아지면 다른 쪽은 가능하지 않을 수 있다.
3. **언제 쓰는가:** LP 상태 진단에 쓴다.
4. **변수 정의:** problem status pair.
5. **목적함수:** bounded optimal, unbounded, infeasible combinations.
6. **제약식:** duality theorem constraints.
7. **수식의 현실 의미:** max unbounded이면 dual min infeasible 같은 관계.
8. **그래프/네트워크 관점:** status duality.
9. **스프레드시트/Solver 관점:** Solver status 해석.
10. **강의 예제 연결:** p025 네 가지 case.
11. **예제 숫자 해석:** 최적/비유계/비가해 관계.
12. **자주 하는 실수:** 한쪽 infeasible이면 다른 쪽이 반드시 unbounded라고 단정하는 오류.
13. **선행 노드:** weak/strong duality
14. **후속 노드:** solver status
15. **동형/유사 노드:** unbounded/infeasible
16. **시험 출제 포인트:** 상태 관계.
17. **RAG retrieval tags:** `duality_cases`, `status`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_four_duality_cases` -> `DM_PDF05:p025:L006` / source_id=`DM_PDF05`, page=`p025`, block=`p025-L006`, line=`L006`

> 근거 excerpt: 문제가 infeasible 인 경우.

### n_DM_PDF05.complementary_slackness — 상보여유정리 (complementary slackness)

1. **한 줄 정의:** 원문제 제약의 여유와 해당 쌍대변수, 쌍대 제약의 여유와 해당 원변수 중 하나는 반드시 0이어야 하는 최적성 조건이다.
2. **쉬운 직관:** 자원이 남으면 그 자원의 가격은 0이고, 가격이 양수면 자원은 완전히 쓰인다.
3. **언제 쓰는가:** primal-dual 최적성 검증과 민감도 해석에 쓴다.
4. **변수 정의:** slack_i, y_i, dual_slack_j, x_j.
5. **목적함수:** slack_i*y_i=0, dual_slack_j*x_j=0.
6. **제약식:** both primal and dual feasible.
7. **수식의 현실 의미:** 기계시간이 남으면 잠재가격 0이라는 해석과 연결된다.
8. **그래프/네트워크 관점:** orthogonality between slack and price.
9. **스프레드시트/Solver 관점:** Solver의 slack/shadow price/reduced cost 관계.
10. **강의 예제 연결:** p027-p031 상보여유 확인.
11. **예제 숫자 해석:** 쌍대문제 제약여유=-한계비용.
12. **자주 하는 실수:** 여유가 있으면 변수도 0이라고 반대로 말하는 오류.
13. **선행 노드:** strong_duality
14. **후속 노드:** reduced cost/shadow price
15. **동형/유사 노드:** KKT complementarity
16. **시험 출제 포인트:** 여유와 가격의 곱=0.
17. **RAG retrieval tags:** `complementary_slackness`, `상보여유`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_complementary_slackness` -> `DM_PDF05:p027:L002` / source_id=`DM_PDF05`, page=`p027`, block=`p027-L002`, line=`L002`

> 근거 excerpt: 상보여유정리

### n_DM_PDF05.shadow_price_dual_solution — 잠재가격과 쌍대해 (shadow price as dual solution)

1. **한 줄 정의:** 민감도 보고서의 잠재가격은 제약에 대응하는 쌍대변수의 최적값으로 해석된다.
2. **쉬운 직관:** 자원의 시장가치가 dual variable로 드러난다.
3. **언제 쓰는가:** sensitivity와 duality를 연결할 때 쓴다.
4. **변수 정의:** dual y_i values.
5. **목적함수:** dual objective equals primal optimum.
6. **제약식:** binding constraints may have nonzero y_i.
7. **수식의 현실 의미:** 식단문제의 비타민 알약 가격이 원문제 잠재가격과 연결된다.
8. **그래프/네트워크 관점:** dual optimal vector.
9. **스프레드시트/Solver 관점:** Solver Constraints 섹션의 Shadow Price.
10. **강의 예제 연결:** p017, p030.
11. **예제 숫자 해석:** 비타민 알약 가격(최적해)=식단문제 잠재가격.
12. **자주 하는 실수:** 잠재가격을 원변수 값과 혼동.
13. **선행 노드:** dual_problem
14. **후속 노드:** sensitivity_analysis
15. **동형/유사 노드:** resource valuation
16. **시험 출제 포인트:** 민감도-쌍대 연결.
17. **RAG retrieval tags:** `shadow_price`, `dual_solution`
18. **Evidence anchors:** `ev_deep_DM_PDF05_node_shadow_price_dual_solution` -> `DM_PDF05:p025:L003` / source_id=`DM_PDF05`, page=`p025`, block=`p025-L003`, line=`L003`

> 근거 excerpt: Case 1: 원본문제와 쌍대문제 모두 최적해를 갖고, 두 문제의


## 7. Example Walkthrough Cards

### ex_DM_PDF05.big_m_diet — 식단문제 Big-M

- **현실 문장 재해석:** >= 영양 제약 때문에 surplus와 artificial을 도입해 Big-M tableau로 푼다.
- **의사결정변수:** 식품량 x_i, surplus, artificial r.
- **목적함수:** min cost 또는 max 변환 목적.
- **제약식:** 영양섭취량>=요구량.
- **Solver 구조:** Big-M tableau.
- **결과 해석:** artificial이 최종 0이어야 원문제 feasible 해다.
- **코칭 순서:**
1. 부등호를 등식화.
2. artificial 도입.
3. M 벌점 목적행 구성.
4. 피벗으로 artificial 제거.
- **Evidence anchors:** `ev_deep_DM_PDF05_example_big_m_diet` -> `DM_PDF05:p004:L002` / page=`p004`, block=`p004-L002`, line=`L002`

> 근거 excerpt: Big-M method

### ex_DM_PDF05.diet_dual — 식단문제 쌍대

- **현실 문장 재해석:** 식단 최소비용 문제의 쌍대를 비타민 알약 가격 최대화 문제로 해석한다.
- **의사결정변수:** dual y1,y2 vitamin prices.
- **목적함수:** max 50y1+60y2.
- **제약식:** 각 식품 가격을 넘지 않는 영양소 가격 조합.
- **Solver 구조:** Solver sensitivity/dual model.
- **결과 해석:** dual optimal prices equal primal shadow prices.
- **코칭 순서:**
1. 원 제약을 dual 변수로.
2. 원 변수별 dual 제약 생성.
3. 최적값 같음 확인.
- **Evidence anchors:** `ev_deep_DM_PDF05_example_diet_dual` -> `DM_PDF05:p013:L006` / page=`p013`, block=`p013-L006`, line=`L006`

> 근거 excerpt: – 비타민 알약 가격이 식단 구성비보다 비싸면 사지 않을 것

### ex_DM_PDF05.complementary_slackness_check — 상보여유 확인

- **현실 문장 재해석:** 원 제약 여유와 쌍대변수, 쌍대 제약 여유와 원변수의 곱이 0인지 확인한다.
- **의사결정변수:** slacks, y_i, x_j.
- **목적함수:** optimality condition not separate objective.
- **제약식:** primal/dual feasibility.
- **Solver 구조:** Sensitivity report plus dual solution.
- **결과 해석:** 남는 자원은 가격 0, 생산되는 변수는 reduced cost 0이다.
- **코칭 순서:**
1. 원 제약 slack 확인.
2. dual y 확인.
3. 쌍대 slack과 x 확인.
- **Evidence anchors:** `ev_deep_DM_PDF05_example_complementary_slackness_check` -> `DM_PDF05:p027:L002` / page=`p027`, block=`p027-L002`, line=`L002`

> 근거 excerpt: 상보여유정리


## 8. Modeling Pattern Library

| pattern | 모형화 템플릿 | 먼저 볼 노드 | 연결 노드 |
| --- | --- | --- | --- |
| 인위변수 처리 | artificial을 Big-M 벌점 또는 Phase I으로 제거한다. | big_m_method | two_phase |
| 원-쌍대 변환 | 제약과 변수를 전치해 가격 문제를 만든다. | dual_problem | sensitivity |
| 최적성 검증 | 강쌍대성과 상보여유로 primal/dual 최적성을 확인한다. | complementary_slackness | KKT |

## 9. Spreadsheet / Solver Mapping

| 요소 | Solver/Spreadsheet 대응 | 튜터 해설 포인트 |
| --- | --- | --- |
| 변수셀 | primal x 또는 dual y | dual을 만들 때 변수/제약 개수가 뒤집힌다. |
| 목표셀 | primal min/max와 dual max/min | 강쌍대성 조건에서 최적값이 같다. |
| 제약셀 | 영양 요구량, 알약가격 상한, slack/surplus | 부등호 방향과 변수 부호 제한을 보존한다. |
| 보고서 | Shadow Price, Reduced Cost | 상보여유와 dual solution으로 해석한다. |

## 10. Cross-Chapter Connections

| 연결 대상 | 연결 설명 | 의존/참조 관계 |
| --- | --- | --- |
| DM_PDF01 2단계법 | Big-M과 two-phase는 artificial 처리 방식이 다르다. | artificial handling |
| DM_PDF02 민감도 | shadow price/reduced cost는 duality의 계산 결과다. | duality -> sensitivity |
| DM_PDF06 네트워크 | max-flow min-cut 같은 네트워크 쌍대성이 후속 연결축이다. | duality -> network theorem |

## 11. Misconception & Error Diagnosis Bank

| 오답/착각 | 왜 문제인가 | 교정 코칭 | 연결 노드 |
| --- | --- | --- | --- |
| M 부호 오류 | artificial을 보상하면 최종해에 남을 수 있다. | max/min 방향별 penalty 부호 확인. | big_m_method |
| 쌍대 변수 개수 오류 | 원 제약 수가 쌍대 변수 수다. | 행/열 대응표를 먼저 만든다. | primal_dual_mapping |
| 상보여유 역해석 | slack이 있으면 dual variable이 0이지, 모든 관련 변수가 0은 아니다. | 곱 조건을 정확히 쓴다. | complementary_slackness |

## 12. Retrieval Routing Table

| 사용자 질문 유형 | 먼저 볼 노드 | 다음 볼 노드 | 예제 카드 | 근거 힌트 |
| --- | --- | --- | --- | --- |
| Big-M은 왜 M을 붙여? | `big_m_method` | `artificial_variable` | `big_m_diet` | DM_PDF05:p003 |
| 쌍대문제 어떻게 만들지? | `dual_problem` | `primal_dual_mapping` | `diet_dual` | DM_PDF05:p018 |
| shadow price가 쌍대해라는 뜻? | `shadow_price_dual_solution` | `dual_problem` | `diet_dual` | DM_PDF05:p017 |
| 상보여유로 최적성 확인? | `complementary_slackness` | `strong_duality` | `complementary_slackness_check` | DM_PDF05:p027 |

## 13. Tutor Session Protocol

1. **지도부터:** Concept Graph Map과 Edge List를 먼저 보여주고, 현재 노드가 전체 OR/MS 흐름에서 어디인지 설명한다.
2. **노드 중심으로:** Core Concept Node Card의 18개 필드를 순서대로 따라가되, 선행/후속/동형 노드를 최소 3개 연결한다.
3. **예제 중심으로:** Example Walkthrough Card를 사용해 현실 문장 -> 변수 -> 목적함수 -> 제약식 -> Solver -> 결과 해석 순서로 진행한다.
4. **문제 풀이 모드:** 사용자가 변수를 먼저 말하게 하고, 목적함수/제약식은 힌트로 한 단계씩 유도한다.
5. **완성 해설 모드:** 위 절차를 생략하지 않고 전체 풀이를 한 번에 제시한다.
6. **암기/정리 모드:** Modeling Pattern Library, Solver Mapping, Misconception Bank만 압축해 제시한다.

## 14. Practice / Check Questions

1. >= 제약 하나를 surplus/artificial 포함 등식으로 바꿔라.
2. 원문제 제약 3개, 변수 5개이면 쌍대 변수/제약 개수를 말하라.
3. slack=40인 제약의 shadow price가 왜 0이어야 하는지 설명하라.

## 15. Source Trace Table

| RAG label | evidence_id | source_id | page | block | line | excerpt |
| --- | --- | --- | --- | --- | --- | --- |
| `n_DM_PDF05.big_m_method` | `ev_deep_DM_PDF05_node_big_m_method` | `DM_PDF05` | `p003` | `p003-L002` | `L002` | 인위변수 도입과 Big-M |
| `n_DM_PDF05.artificial_variable` | `ev_deep_DM_PDF05_node_artificial_variable` | `DM_PDF05` | `p003` | `p003-L009` | `L009` | 인위변수(artificial variable) r1, r2 을 도입함 |
| `n_DM_PDF05.surplus_variable` | `ev_deep_DM_PDF05_node_surplus_variable` | `DM_PDF05` | `p001` | `p001-L010` | `L010` | <힌트: 잉여변수 1개, 인위변수 2개가 도입되어야 함> |
| `n_DM_PDF05.diet_problem` | `ev_deep_DM_PDF05_node_diet_problem` | `DM_PDF05` | `p002` | `p002-L003` | `L003` | (1) 최소화 선형계획문제 : 식단문제 |
| `n_DM_PDF05.dual_problem` | `ev_deep_DM_PDF05_node_dual_problem` | `DM_PDF05` | `p013` | `p013-L009` | `L009` | 4.7 선형계획의 쌍대문제 |
| `n_DM_PDF05.primal_dual_mapping` | `ev_deep_DM_PDF05_node_primal_dual_mapping` | `DM_PDF05` | `p020` | `p020-L001` | `L001` | 20원본문제와 쌍대문제의 관계 |
| `n_DM_PDF05.weak_duality` | `ev_deep_DM_PDF05_node_weak_duality` | `DM_PDF05` | `p024` | `p024-L002` | `L002` | 약쌍대성 & 강쌍대성 정리 |
| `n_DM_PDF05.strong_duality` | `ev_deep_DM_PDF05_node_strong_duality` | `DM_PDF05` | `p024` | `p024-L002` | `L002` | 약쌍대성 & 강쌍대성 정리 |
| `n_DM_PDF05.four_duality_cases` | `ev_deep_DM_PDF05_node_four_duality_cases` | `DM_PDF05` | `p025` | `p025-L006` | `L006` | 문제가 infeasible 인 경우. |
| `n_DM_PDF05.complementary_slackness` | `ev_deep_DM_PDF05_node_complementary_slackness` | `DM_PDF05` | `p027` | `p027-L002` | `L002` | 상보여유정리 |
| `n_DM_PDF05.shadow_price_dual_solution` | `ev_deep_DM_PDF05_node_shadow_price_dual_solution` | `DM_PDF05` | `p025` | `p025-L003` | `L003` | Case 1: 원본문제와 쌍대문제 모두 최적해를 갖고, 두 문제의 |
| `ex_DM_PDF05.big_m_diet` | `ev_deep_DM_PDF05_example_big_m_diet` | `DM_PDF05` | `p004` | `p004-L002` | `L002` | Big-M method |
| `ex_DM_PDF05.diet_dual` | `ev_deep_DM_PDF05_example_diet_dual` | `DM_PDF05` | `p013` | `p013-L006` | `L006` | – 비타민 알약 가격이 식단 구성비보다 비싸면 사지 않을 것 |
| `ex_DM_PDF05.complementary_slackness_check` | `ev_deep_DM_PDF05_example_complementary_slackness_check` | `DM_PDF05` | `p027` | `p027-L002` | `L002` | 상보여유정리 |

## 16. QC / Extraction Risk Notes

- **page_count:** 36
- **low_text_pages:** 5
- **extraction_risk_pages:** 5
- **QC policy:** 표, 그림, 수식 이미지가 많은 페이지는 전사 텍스트만으로 숫자를 단정하지 않는다. 튜터는 수식 구조와 증거 anchor를 우선 제시하고, 숫자 최적해는 필요 시 원본 PDF를 대조한다.
