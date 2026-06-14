# DM_PDF02 — Ch.5 민감도 분석 최종 RAG 튜터 운영문서

## 0. Document Contract

- **문서 성격:** PDF 요약본이 아니라, 전담 1:1 경영과학 튜터와 RAG agent가 함께 쓰는 증거 기반 운영문서다.
- **source_id:** `DM_PDF02`
- **normalized_pdf:** `decisionMaking/pdf_sources/DM_PDF02_ch05_sensitivity_analysis.pdf`
- **primary transcript:** `decisionMaking/pdf_transcripts/DM_PDF02__ch05_sensitivity_analysis__full_transcript.md`
- **sidecar:** `decisionMaking/_inventory/DM_PDF02__ch05_sensitivity_analysis`
- **flat-pack target:** `decisionMaking/rag_applied_flat_pack/DM_PDF02__04_rag.md`
- **source priority:** 1) PDF 전사본 anchor, 2) 이 문서의 enhanced sidecar, 3) 웹 그라운딩, 4) 일반 OR/MS 지식.
- **중요한 명명 주의:** `DM_PDF02`는 PDF intake index다. 강의 회차/장 번호와 혼동하지 않는다.

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
| p001 | `DM_PDF02:p001:L001, DM_PDF02:p001:L002` | Operation Research / Ch.5. Sensitivity Analysis / for Linear Programming | ok |
| p002 | `DM_PDF02:p002:L002, DM_PDF02:p002:L003` | 유모차-보행기 생산계획 문제 / – 제품배합문제(product-mix problem): 제한된 원료로 최 / 대 이익을 내는 제품별 생산 수준을 결정하는 문제 | ok |
| p003 | `DM_PDF02:p003:L002, DM_PDF02:p003:L003` | – 수요에 효율적으로 대처하기 위해 주 단위로 생산계획 / – 유모차와 보행기 생산 고려 / – 제품 단위 생산에 요구되는 각 기계 작업시간 | ok |
| p004 | `DM_PDF02:p004:L002, DM_PDF02:p004:L003` | – 제품 단위당 판매이익 (판매가격-생산원가): / 유모차 30만원, 보행기 20만원 / – 단, 보행기는 40대 이하로만 생산한다고 가정한다. | ok |
| p005 | `DM_PDF02:p005:L002, DM_PDF02:p005:L003` | 수리 모형화 / 유모차 생산량: x1 / 보행기 생산량: x2 | ok |
| p006 | `DM_PDF02:p006:L002, DM_PDF02:p006:L003` | 2.3 그래프를 이용한 선형계획 이해 / Max 30 x1 + 20 x2 / s/t 8 x1 + 3 x2 <= 240 | ok |
| p007 | `DM_PDF02:p007:L001, DM_PDF02:p007:L002` | 두 변수의 그래프 / 표현 / • X1축: 유모차 대수 | ok |
| p008 | `DM_PDF02:p008:L001, DM_PDF02:p008:L002` | 제약조건의 / 표현 / 8x1+3x2 = 240 등 | LOW_TEXT |
| p009 | `DM_PDF02:p009:L001, DM_PDF02:p009:L002` | 제약조건 / 충족영역 / • 8x1 + 3x2 <= 240 | ok |
| p010 | `DM_PDF02:p010:L001, DM_PDF02:p010:L002` | 실행가능영역 feasible region / • 모든 제한조건 / 을 충족함. | LOW_TEXT |
| p011 | `DM_PDF02:p011:L001, DM_PDF02:p011:L002` | 실행가능해와 실행 불능해 / • A, B, C는 실행가능해 / • D는 실행 불능해 | LOW_TEXT |
| p012 | `DM_PDF02:p012:L002, DM_PDF02:p012:L003` | 그래프 이해(계속) /  가능해 종류: / • 내부점(interior point): A | ok |
| p013 | `DM_PDF02:p013:L001` | 목적함수: 등위이익선 (iso-profit line) | LOW_TEXT |
| p014 | `DM_PDF02:p014:L002, DM_PDF02:p014:L003` | 등위 이익선과 최적해 결정 / • 등위 이익선을 평행이동 / (shift) 시키면서 최대 | ok |
| p015 | `DM_PDF02:p015:L002, DM_PDF02:p015:L003` | 복수 최적해 (multiple optimal solutions) / • 만일 목적함수의 x1 계수가 30  20 으로 바뀌어 / 20 x1+ 20 x2 이면 | ok |
| p016 | `DM_PDF02:p016:L001, DM_PDF02:p016:L002` | 꼭지점을 따라가는 / ‘단체법’(Simplex Method) | LOW_TEXT |
| p017 | `DM_PDF02:p017:L002, DM_PDF02:p017:L003` | 선형계획 문제의 성질 / (최적 목적함수 값이 유한값일 때) / 1. 최적해가 되는 꼭지점이 반드시 존재한다. | ok |
| p018 | `DM_PDF02:p018:L002, DM_PDF02:p018:L003` | Simplex Method / (유한 최적 값을 갖는 경우) / Simplex Method는 대수적 절차로서 | ok |
| p019 | `DM_PDF02:p019:L002, DM_PDF02:p019:L003` | Simplex method (기하적 설명) / • Simplex method: 꼭지점 이동 / 변경셀 목표셀 | ok |
| p020 | `DM_PDF02:p020:L001, DM_PDF02:p020:L002` | 실행가능영역이 없는 경우 / (Infeasible solution) | LOW_TEXT |
| p021 | `DM_PDF02:p021:L001, DM_PDF02:p021:L002` | 무한가능영역, / 무한해(unbounded solution) | LOW_TEXT |
| p022 | `DM_PDF02:p022:L001, DM_PDF02:p022:L002` | 중복제약식(redundant constraints) / • 보행기 수요가 / 60대 이하라 | LOW_TEXT |
| p023 | `DM_PDF02:p023:L001, DM_PDF02:p023:L002` | 2.4. 민감도 분석 sensitivity analysis / [예제 2.3] / 최적해: | ok |
| p024 | `DM_PDF02:p024:L002, DM_PDF02:p024:L003` | 민감도 보고서 (목표셀 계수 변화시) / 유모차 판매이익을 현재 30만원에서 변화시킴 / “총판매이익”은 유모차 판매이익에 민감하지 않음 | LOW_TEXT |
| p025 | `DM_PDF02:p025:L002, DM_PDF02:p025:L003` | 민감도 보고서 (제한조건 우변값 변화시) / ‘기계1’에 대한 사용가능시간(제한조건 우변값)을 변화 / 현재 240 시간에서 변화시킴 | ok |
| p026 | `DM_PDF02:p026:L002, DM_PDF02:p026:L003` | 민감도 보고서 / ‘해찾기 결과’ 대화상자에서 ‘민감도’를 선택하여 / 민감도 보고서를 출력하게 한다 (2010, 우편물 종류) | ok |
| p027 | `DM_PDF02:p027:L002, DM_PDF02:p027:L003` | 민감도 분석 요점 / (유용성: 새롭게 해찾기를 실행하지 않아도 결과를 예상) / 1. 한계비용: 한계에 있는 최적해(계산값)를 한 단위 증가시킬 | ok |
| p028 | `DM_PDF02:p028:L002, DM_PDF02:p028:L003` | 민감도 분석(1): 한계비용 / 유모차의 현재 계산값을 ‘0’에서 ‘1개’를 증가시키면, / (하한 조건을 >=0 에서 >=1 로 바꾸면), | ok |
| p029 | `DM_PDF02:p029:L002, DM_PDF02:p029:L003` | 민감도 분석(2): 허용 가능의 범위 (목표셀 계수) / 보행기 1대당 판매이익이 20만원에서 18만원으로 / 2만원 감소하면, | ok |
| p030 | `DM_PDF02:p030:L002, DM_PDF02:p030:L003` | 민감도 분석(3): 잠재가격 / 기계1의 제한조건을 241시간으로 1시간 더 증가시키면, / 1. 목표셀의 최적값은 잠재가격인 5.33만원 증가한다. | ok |
| p031 | `DM_PDF02:p031:L002, DM_PDF02:p031:L003` | 민감도 분석(4): 허용 가능의 범위 (우변값) / 잠재가격이 변하지 않는 우변 값의 범위를 의미함 / 기계1의 이용가능시간을 237시간으로 3시간 감소시키면, | ok |
| p032 | `DM_PDF02:p032:L002, DM_PDF02:p032:L003` | 민감도 분석 연습 / (Reduced cost=Marginal cost =수정비용=한계비용 ; Shadow price=잠재가격) / =라그랑지 승수 | ok |
| p033 | `DM_PDF02:p033:L002, DM_PDF02:p033:L003` | 목적함수 계수의 허용가능 증가/감소 /  최적해가 유지되는 목적함수 계수 범위 / 30 x1 + 20 x2 = k | ok |
| p034 | `DM_PDF02:p034:L002, DM_PDF02:p034:L003` | • 목적함수 계수의 변화 / 허용가능 증가치 = 53.33 - 30 = 23.33 / 허용가능 감소치 = 20 – 30 = -10 | ok |
| p035 | `DM_PDF02:p035:L002, DM_PDF02:p035:L003` | 한계비용(할인가,수정비용) … 참고 /  한계비용(marginal cost) / =할인가(reduced cost) | ok |
| p036 | `DM_PDF02:p036:L002, DM_PDF02:p036:L003` | 잠재가격 (라그랑지 승수) /  잠재가격(Shadow price) / • 기계1 작업시간의 잠재가격: | ok |
| p037 | `DM_PDF02:p037:L002, DM_PDF02:p037:L003` | [참고] Excel 해찾기 (번역 오류) / 해법: / 1) 선형문제  LP 심플렉스 | ok |
| p038 | `DM_PDF02:p038:L002, DM_PDF02:p038:L003` | 우편물 종류 “민감도” / Sensitivity (report) / [참고] Excel 해찾기 (번역 오류) | LOW_TEXT |
| p039 | `DM_PDF02:p039:L001` | 실습문제 | LOW_TEXT |
| p040 | `DM_PDF02:p040:L002, DM_PDF02:p040:L003` | 실습#1 (By hand) / Maximize 40 x1 + 30 x2 / subject to 0.4 x1 + 0.5 x2 <= 20 | ok |
| p041 | `DM_PDF02:p041:L001, DM_PDF02:p041:L002` | 1) 다음 문제의 최적해를 구하라. / 2) 최적해가 변하지 않는 x1의 계수의 범위를 구하라. / 3) x1과 x2의 한계비용 (marginal cost)을 각각 구하라. | ok |
| p042 | `DM_PDF02:p042:L001, DM_PDF02:p042:L002` | 실습문제 1 (PROBLEM #5.10) / David, Ladeana, and Lydia are the sole partners and workers in a company that / produces fine clocks. David and Ladeana are each available to work a maximum | ok |
| p043 | `DM_PDF02:p043:L001, DM_PDF02:p043:L002` | Each grandfather clock built and shipped yields a profit of $300, while each wall clock / yields a profit of $200. The three partners now want to determine how many clocks of / each type should be produced per week to maximize the total profit. | ok |

## 2. Chapter Thesis

민감도 분석은 최적해를 하나의 답으로 끝내지 않고, 목적계수와 RHS 변화가 기존 basis와 경제적 해석을 어디까지 유지하는지 읽는 절차다.

## 3. Current Graph Position

- **현재 그래프 위치:** LP 최적해 -> binding/nonbinding -> shadow price/reduced cost -> allowable range -> Solver sensitivity report.
- **지금 보는 노드:** `DM_PDF02` / Ch.5 민감도 분석
- **튜터 운영 원칙:** 질문이 들어오면 먼저 노드로 매핑하고, 예제 카드와 수식/Solver 구조를 거쳐 Source Trace Table의 evidence anchor로 되돌아간다.

## 4. Learning Outcomes

- reduced cost, shadow price, allowable increase/decrease를 서로 다른 질문으로 분리한다.
- 허용범위 안과 밖에서 해석 방식이 달라진다는 점을 설명한다.
- 유모차-보행기 예제를 그래프, Solver 보고서, 경제적 언어로 번역한다.

## 5. Concept Graph Map

| node_id | 개념 | 역할 | 선행 노드 | 후속 노드 |
| --- | --- | --- | --- | --- |
| `n_DM_PDF02.sensitivity_analysis` | 민감도 분석 | 최적해 주변에서 목적계수와 제약 RHS 변화가 목적값과 basis에 미치는 영향을 분석하는 절차다. | LP optimal solution, binding constraint | duality, transportation sensitivity |
| `n_DM_PDF02.product_mix_model` | 유모차-보행기 생산모형 | 두 제품 생산량을 결정해 기계시간과 수요 제약 아래 총판매이익을 최대화하는 LP 예제다. | LP formulation | sensitivity report |
| `n_DM_PDF02.binding_constraint` | 결합/비결합 제약 | 최적해에서 좌변이 RHS와 같으면 binding, 여유가 남으면 nonbinding인 제약이다. | LP feasible region | shadow price |
| `n_DM_PDF02.shadow_price` | 잠재가격 | 제약 RHS를 1단위 완화했을 때 목적값이 변하는 한계 가치다. | binding constraint | duality |
| `n_DM_PDF02.reduced_cost` | 감소비용/한계비용 | 현재 0 또는 경계에 있는 변수의 값을 한 단위 움직일 때 목적값이 얼마나 불리하게 변하는지 나타내는 값이다. | duality shadow price | objective coefficient range |
| `n_DM_PDF02.allowable_objective_range` | 목적계수 허용범위 | 현재 최적해 또는 basis가 유지되는 목적계수 변화 범위다. | reduced cost | sensitivity report |
| `n_DM_PDF02.allowable_rhs_range` | RHS 허용범위 | shadow price가 변하지 않는 제약 RHS 변화 구간이다. | shadow price | post-optimal analysis |
| `n_DM_PDF02.solver_sensitivity_report` | Solver 민감도 보고서 | Solver가 최적해 이후 변수별 reduced cost와 제약별 shadow price 및 허용범위를 표로 제공하는 보고서다. | Solver model | duality and sensitivity |

### Edge List

| from | edge_type | to |
| --- | --- | --- |
| `LP optimal solution, binding constraint` | 선행 관계 | `n_DM_PDF02.sensitivity_analysis` |
| `n_DM_PDF02.sensitivity_analysis` | 후속 관계 | `duality, transportation sensitivity` |
| `n_DM_PDF02.sensitivity_analysis` | 동형/유사 | `what-if analysis` |
| `LP formulation` | 선행 관계 | `n_DM_PDF02.product_mix_model` |
| `n_DM_PDF02.product_mix_model` | 후속 관계 | `sensitivity report` |
| `n_DM_PDF02.product_mix_model` | 동형/유사 | `Super Grain 같은 product mix` |
| `LP feasible region` | 선행 관계 | `n_DM_PDF02.binding_constraint` |
| `n_DM_PDF02.binding_constraint` | 후속 관계 | `shadow price` |
| `n_DM_PDF02.binding_constraint` | 동형/유사 | `slack variable` |
| `binding constraint` | 선행 관계 | `n_DM_PDF02.shadow_price` |
| `n_DM_PDF02.shadow_price` | 후속 관계 | `duality` |
| `n_DM_PDF02.shadow_price` | 동형/유사 | `marginal value` |
| `duality shadow price` | 선행 관계 | `n_DM_PDF02.reduced_cost` |
| `n_DM_PDF02.reduced_cost` | 후속 관계 | `objective coefficient range` |
| `n_DM_PDF02.reduced_cost` | 동형/유사 | `opportunity cost` |
| `reduced cost` | 선행 관계 | `n_DM_PDF02.allowable_objective_range` |
| `n_DM_PDF02.allowable_objective_range` | 후속 관계 | `sensitivity report` |
| `n_DM_PDF02.allowable_objective_range` | 동형/유사 | `iso-profit line` |
| `shadow price` | 선행 관계 | `n_DM_PDF02.allowable_rhs_range` |
| `n_DM_PDF02.allowable_rhs_range` | 후속 관계 | `post-optimal analysis` |
| `n_DM_PDF02.allowable_rhs_range` | 동형/유사 | `resource valuation` |
| `Solver model` | 선행 관계 | `n_DM_PDF02.solver_sensitivity_report` |
| `n_DM_PDF02.solver_sensitivity_report` | 후속 관계 | `duality and sensitivity` |
| `n_DM_PDF02.solver_sensitivity_report` | 동형/유사 | `tableau final row` |

## 6. Core Concept Node Cards

### n_DM_PDF02.sensitivity_analysis — 민감도 분석 (sensitivity analysis)

1. **한 줄 정의:** 최적해 주변에서 목적계수와 제약 RHS 변화가 목적값과 basis에 미치는 영향을 분석하는 절차다.
2. **쉬운 직관:** 해 하나를 구한 뒤 그 해가 얼마나 흔들림에 강한지 보는 사후 진단이다.
3. **언제 쓰는가:** 최적해를 얻은 뒤 자원량, 이익계수, 수요상한이 바뀌는 질문에 쓴다.
4. **변수 정의:** 기존 LP의 변수 x1, x2와 제약 RHS/목적계수.
5. **목적함수:** 기존 objective coefficient가 바뀔 때 z 변화 또는 basis 유지 여부를 본다.
6. **제약식:** RHS 변화는 shadow price와 allowable range로 해석한다.
7. **수식의 현실 의미:** 기계 시간이 1시간 더 생기면 이익이 얼마나 늘어나는가라는 질문이다.
8. **그래프/네트워크 관점:** 그래프에서는 최적 꼭짓점과 등위이익선의 접촉이 얼마나 유지되는지 본다.
9. **스프레드시트/Solver 관점:** Solver sensitivity report의 Variable Cells/Constraints 섹션을 읽는다.
10. **강의 예제 연결:** 유모차-보행기 생산계획.
11. **예제 숫자 해석:** x1*=0, x2*=40 같은 최적해에서 비생산 제품과 병목 자원을 해석한다.
12. **자주 하는 실수:** shadow price를 허용범위 밖까지 무제한 적용하는 오류.
13. **선행 노드:** LP optimal solution, binding constraint
14. **후속 노드:** duality, transportation sensitivity
15. **동형/유사 노드:** what-if analysis
16. **시험 출제 포인트:** 보고서 수치를 해석시키는 문제.
17. **RAG retrieval tags:** `sensitivity`, `민감도`, `allowable`
18. **Evidence anchors:** `ev_deep_DM_PDF02_node_sensitivity_analysis` -> `DM_PDF02:p023:L001` / source_id=`DM_PDF02`, page=`p023`, block=`p023-L001`, line=`L001`

> 근거 excerpt: 2.4. 민감도 분석 sensitivity analysis

### n_DM_PDF02.product_mix_model — 유모차-보행기 생산모형 (stroller-walker product mix)

1. **한 줄 정의:** 두 제품 생산량을 결정해 기계시간과 수요 제약 아래 총판매이익을 최대화하는 LP 예제다.
2. **쉬운 직관:** 제한된 기계시간을 어느 제품에 쓸지 배분하는 문제다.
3. **언제 쓰는가:** 민감도 해석의 기준 LP로 쓴다.
4. **변수 정의:** x1=유모차 생산량, x2=보행기 생산량.
5. **목적함수:** max 30x1+20x2.
6. **제약식:** 기계1/2/3 시간 제약과 x2<=40.
7. **수식의 현실 의미:** 기계별 시간은 자원 RHS, 제품 이익은 목적계수다.
8. **그래프/네트워크 관점:** 2변수 가능영역과 등위이익선으로 볼 수 있다.
9. **스프레드시트/Solver 관점:** Solver에서 변수셀 x1,x2, 목표셀 총이익, 제약셀 기계시간/수요.
10. **강의 예제 연결:** DM_PDF02 초반 유모차-보행기 문제.
11. **예제 숫자 해석:** 기계1 8x1+3x2<=240처럼 제품별 사용시간이 제약계수다.
12. **자주 하는 실수:** 제품 이름을 변수로 두지 않고 수익 자체를 변수로 두는 오류.
13. **선행 노드:** LP formulation
14. **후속 노드:** sensitivity report
15. **동형/유사 노드:** Super Grain 같은 product mix
16. **시험 출제 포인트:** 문장 문제를 LP 식으로 세우기.
17. **RAG retrieval tags:** `product_mix`, `유모차`, `보행기`
18. **Evidence anchors:** `ev_deep_DM_PDF02_node_product_mix_model` -> `DM_PDF02:p005:L003` / source_id=`DM_PDF02`, page=`p005`, block=`p005-L003`, line=`L003`

> 근거 excerpt: 유모차 생산량: x1

### n_DM_PDF02.binding_constraint — 결합/비결합 제약 (binding/nonbinding constraint)

1. **한 줄 정의:** 최적해에서 좌변이 RHS와 같으면 binding, 여유가 남으면 nonbinding인 제약이다.
2. **쉬운 직관:** 완전히 다 쓴 자원은 병목이고, 남는 자원은 한 단위 더 줘도 즉시 가치가 없다.
3. **언제 쓰는가:** shadow price 해석 전 제약 상태를 구분할 때 쓴다.
4. **변수 정의:** constraint LHS and RHS.
5. **목적함수:** 목적함수 변화는 binding 자원에서 더 민감하다.
6. **제약식:** binding은 slack=0, nonbinding은 slack>0.
7. **수식의 현실 의미:** 기계시간이 꽉 찼는지 남았는지 확인한다.
8. **그래프/네트워크 관점:** 최적 꼭짓점에서 접하는 경계선과 아닌 경계선이다.
9. **스프레드시트/Solver 관점:** Solver Constraints 섹션의 Final Value와 Constraint RHS를 비교한다.
10. **강의 예제 연결:** 기계1/2/3 및 보행기 수요 제약.
11. **예제 숫자 해석:** 기계1 시간이 240에 가까우면 병목 후보가 된다.
12. **자주 하는 실수:** nonbinding 제약의 shadow price를 양수로 해석하는 오류.
13. **선행 노드:** LP feasible region
14. **후속 노드:** shadow price
15. **동형/유사 노드:** slack variable
16. **시험 출제 포인트:** binding 여부와 shadow price 관계.
17. **RAG retrieval tags:** `binding`, `slack`, `constraint`
18. **Evidence anchors:** `ev_deep_DM_PDF02_node_binding_constraint` -> `DM_PDF02:p023:L012` / source_id=`DM_PDF02`, page=`p023`, block=`p023-L012`, line=`L012`

> 근거 excerpt: 목적함수 계수 및 제한조건 우변값

### n_DM_PDF02.shadow_price — 잠재가격 (shadow price)

1. **한 줄 정의:** 제약 RHS를 1단위 완화했을 때 목적값이 변하는 한계 가치다.
2. **쉬운 직관:** 부족한 자원을 한 단위 더 살 수 있다면 얼마까지 지불할 수 있는지 보는 가격이다.
3. **언제 쓰는가:** 자원량 증가/감소 질문에서 쓴다.
4. **변수 정의:** 제약 i의 RHS b_i 변화량 Delta b_i.
5. **목적함수:** Delta z = shadow price * Delta b_i, 허용범위 안에서만.
6. **제약식:** binding 제약은 양/음의 가치가 가능하고 nonbinding은 보통 0이다.
7. **수식의 현실 의미:** 기계1 시간이 1시간 늘면 이익이 5.33만원 증가한다는 식이다.
8. **그래프/네트워크 관점:** 쌍대변수 y_i와 같은 경제적 의미다.
9. **스프레드시트/Solver 관점:** Solver Constraints 섹션의 Shadow Price.
10. **강의 예제 연결:** 기계1 작업가능시간 예시.
11. **예제 숫자 해석:** 241시간으로 늘릴 때 5.33만원 증가.
12. **자주 하는 실수:** 잠재가격을 실제 시장가격으로 무조건 동일시하는 오류.
13. **선행 노드:** binding constraint
14. **후속 노드:** duality
15. **동형/유사 노드:** marginal value
16. **시험 출제 포인트:** 허용 RHS 범위와 함께 계산.
17. **RAG retrieval tags:** `shadow_price`, `잠재가격`
18. **Evidence anchors:** `ev_deep_DM_PDF02_node_shadow_price` -> `DM_PDF02:p026:L009` / source_id=`DM_PDF02`, page=`p026`, block=`p026-L009`, line=`L009`

> 근거 excerpt: Shadow price

### n_DM_PDF02.reduced_cost — 감소비용/한계비용 (reduced cost)

1. **한 줄 정의:** 현재 0 또는 경계에 있는 변수의 값을 한 단위 움직일 때 목적값이 얼마나 불리하게 변하는지 나타내는 값이다.
2. **쉬운 직관:** 선택되지 않은 제품이 왜 생산되지 않는지 알려주는 기회비용이다.
3. **언제 쓰는가:** 변수셀이 0인 제품의 진입 가능성을 해석할 때 쓴다.
4. **변수 정의:** nonbasic variable x_j와 objective coefficient c_j.
5. **목적함수:** max에서 c_j - y^T a_j가 개선 필요량/기회비용으로 읽힌다.
6. **제약식:** 기저 밖 변수는 reduced cost가 0이 되어야 들어올 수 있다.
7. **수식의 현실 의미:** 유모차 생산량을 0에서 1로 강제로 늘리면 이익이 감소하는 해석이다.
8. **그래프/네트워크 관점:** 타블로 목적행 계수와 연결된다.
9. **스프레드시트/Solver 관점:** Solver Variable Cells 섹션의 Reduced Cost.
10. **강의 예제 연결:** 유모차 x1의 한계비용 설명.
11. **예제 숫자 해석:** x1을 1개 늘리면 목적값이 12.67 줄어드는 사례.
12. **자주 하는 실수:** reduced cost를 단위 생산비로 오해하는 오류.
13. **선행 노드:** duality shadow price
14. **후속 노드:** objective coefficient range
15. **동형/유사 노드:** opportunity cost
16. **시험 출제 포인트:** 비생산 변수의 해석.
17. **RAG retrieval tags:** `reduced_cost`, `한계비용`, `수정비용`
18. **Evidence anchors:** `ev_deep_DM_PDF02_node_reduced_cost` -> `DM_PDF02:p026:L007` / source_id=`DM_PDF02`, page=`p026`, block=`p026-L007`, line=`L007`

> 근거 excerpt: Reduced cost

### n_DM_PDF02.allowable_objective_range — 목적계수 허용범위 (allowable objective coefficient range)

1. **한 줄 정의:** 현재 최적해 또는 basis가 유지되는 목적계수 변화 범위다.
2. **쉬운 직관:** 제품 이익이 어느 정도 바뀌어도 최적 생산계획이 그대로인지 보는 안정성 범위다.
3. **언제 쓰는가:** 판매이익/단위비용이 변하는 질문에 쓴다.
4. **변수 정의:** c_j current value, allowable increase/decrease.
5. **목적함수:** c_j가 범위 안이면 basis 유지, z만 새 계수로 재계산한다.
6. **제약식:** 범위를 벗어나면 새 LP를 다시 풀어야 한다.
7. **수식의 현실 의미:** 보행기 이익이 20에서 18로 낮아지는 경우.
8. **그래프/네트워크 관점:** 등위이익선의 기울기가 같은 최적 꼭짓점 범위 내에서 움직인다.
9. **스프레드시트/Solver 관점:** Solver Variable Cells의 Objective Coefficient와 Allowable Increase/Decrease.
10. **강의 예제 연결:** 목표셀 계수 변화 민감도 보고서.
11. **예제 숫자 해석:** 30 -> 20 같은 변경이 최적해를 바꾸는지 판단한다.
12. **자주 하는 실수:** 허용증가/감소를 새 계수 자체와 혼동하는 오류.
13. **선행 노드:** reduced cost
14. **후속 노드:** sensitivity report
15. **동형/유사 노드:** iso-profit line
16. **시험 출제 포인트:** 계수 변화 후 재계산 여부.
17. **RAG retrieval tags:** `allowable`, `objective`, `목적계수`
18. **Evidence anchors:** `ev_deep_DM_PDF02_node_allowable_objective_range` -> `DM_PDF02:p024:L002` / source_id=`DM_PDF02`, page=`p024`, block=`p024-L002`, line=`L002`

> 근거 excerpt: 민감도 보고서 (목표셀 계수 변화시)

### n_DM_PDF02.allowable_rhs_range — RHS 허용범위 (allowable RHS range)

1. **한 줄 정의:** shadow price가 변하지 않는 제약 RHS 변화 구간이다.
2. **쉬운 직관:** 자원을 조금 더 주거나 덜 줄 때 같은 병목 구조가 유지되는 구간이다.
3. **언제 쓰는가:** 자원량 변경 질문에서 쓴다.
4. **변수 정의:** b_i current RHS, allowable increase/decrease.
5. **목적함수:** Delta z=shadow price*Delta b_i는 이 범위 안에서만 적용한다.
6. **제약식:** 범위를 벗어나면 binding set이 바뀔 수 있다.
7. **수식의 현실 의미:** 기계1 이용가능시간을 237시간으로 줄이는 질문.
8. **그래프/네트워크 관점:** 가능영역 경계선이 평행 이동해도 같은 꼭짓점 구조가 유지되는 구간이다.
9. **스프레드시트/Solver 관점:** Solver Constraints 섹션의 Allowable Increase/Decrease.
10. **강의 예제 연결:** 우변값 변화 민감도 보고서.
11. **예제 숫자 해석:** 3시간 감소면 3*5.33만큼 이익 감소처럼 계산한다.
12. **자주 하는 실수:** allowable range 밖에서도 같은 shadow price를 쓰는 오류.
13. **선행 노드:** shadow price
14. **후속 노드:** post-optimal analysis
15. **동형/유사 노드:** resource valuation
16. **시험 출제 포인트:** RHS 변화 계산.
17. **RAG retrieval tags:** `RHS`, `allowable`, `허용범위`
18. **Evidence anchors:** `ev_deep_DM_PDF02_node_allowable_rhs_range` -> `DM_PDF02:p029:L002` / source_id=`DM_PDF02`, page=`p029`, block=`p029-L002`, line=`L002`

> 근거 excerpt: 민감도 분석(2): 허용 가능의 범위 (목표셀 계수)

### n_DM_PDF02.solver_sensitivity_report — Solver 민감도 보고서 (Solver sensitivity report)

1. **한 줄 정의:** Solver가 최적해 이후 변수별 reduced cost와 제약별 shadow price 및 허용범위를 표로 제공하는 보고서다.
2. **쉬운 직관:** 해답지 뒤의 해설표처럼, 왜 그 해가 나왔고 어디까지 유지되는지 알려준다.
3. **언제 쓰는가:** Excel Solver 해찾기 결과 후 민감도 옵션을 선택해 쓴다.
4. **변수 정의:** Variable Cells and Constraints report fields.
5. **목적함수:** 목표셀 값과 계수 변화 범위를 함께 본다.
6. **제약식:** 제약 final value, RHS, shadow price, allowable ranges를 본다.
7. **수식의 현실 의미:** 생산계획의 사후 해석 자료다.
8. **그래프/네트워크 관점:** 타블로의 reduced cost/dual price를 표로 출력한 것이다.
9. **스프레드시트/Solver 관점:** 해찾기 결과 대화상자에서 민감도 선택.
10. **강의 예제 연결:** DM_PDF02 p026 설명.
11. **예제 숫자 해석:** Variable Cells와 Constraints 섹션을 혼동하지 않는다.
12. **자주 하는 실수:** 보고서 수치를 문제 원문 단위와 연결하지 않는 오류.
13. **선행 노드:** Solver model
14. **후속 노드:** duality and sensitivity
15. **동형/유사 노드:** tableau final row
16. **시험 출제 포인트:** 보고서 읽기.
17. **RAG retrieval tags:** `solver`, `sensitivity_report`
18. **Evidence anchors:** `ev_deep_DM_PDF02_node_solver_sensitivity_report` -> `DM_PDF02:p024:L002` / source_id=`DM_PDF02`, page=`p024`, block=`p024-L002`, line=`L002`

> 근거 excerpt: 민감도 보고서 (목표셀 계수 변화시)


## 7. Example Walkthrough Cards

### ex_DM_PDF02.stroller_walker_lp — 유모차-보행기 LP 정식화

- **현실 문장 재해석:** 유모차와 보행기 생산량을 정해 총판매이익을 최대화한다.
- **의사결정변수:** x1=유모차, x2=보행기.
- **목적함수:** max 30x1+20x2.
- **제약식:** 기계1 8x1+3x2<=240, 기계2 4x1+4x2<=200, 기계3 4x1<=100, x2<=40.
- **Solver 구조:** Solver Simplex LP, 변수셀 x1:x2.
- **결과 해석:** 최적해는 각 제약의 binding 여부와 함께 해석해야 한다.
- **코칭 순서:**
1. 변수를 둔다.
2. 기계별 시간 제약을 쓴다.
3. 최적해 후 민감도 보고서를 읽는다.
- **Evidence anchors:** `ev_deep_DM_PDF02_example_stroller_walker_lp` -> `DM_PDF02:p005:L003` / page=`p005`, block=`p005-L003`, line=`L003`

> 근거 excerpt: 유모차 생산량: x1

### ex_DM_PDF02.shadow_price_machine1 — 기계1 1시간 추가 해석

- **현실 문장 재해석:** 기계1 RHS가 1시간 늘 때 이익 증가분을 잠재가격으로 계산한다.
- **의사결정변수:** Delta b_machine1=1.
- **목적함수:** Delta z=shadow price*Delta b.
- **제약식:** 허용 RHS 범위 안이어야 한다.
- **Solver 구조:** Sensitivity Report Constraints 섹션.
- **결과 해석:** 5.33만원 증가처럼 한계가치를 해석한다.
- **코칭 순서:**
1. binding 여부 확인.
2. shadow price 확인.
3. allowable range 확인.
4. Delta z 계산.
- **Evidence anchors:** `ev_deep_DM_PDF02_example_shadow_price_machine1` -> `DM_PDF02:p030:L003` / page=`p030`, block=`p030-L003`, line=`L003`

> 근거 excerpt: 기계1의 제한조건을 241시간으로 1시간 더 증가시키면,

### ex_DM_PDF02.reduced_cost_stroller — 유모차 한계비용 해석

- **현실 문장 재해석:** 현재 생산하지 않는 유모차를 1개 강제로 만들 때 목적값 변화를 본다.
- **의사결정변수:** Delta x1=1.
- **목적함수:** 변수 경계 이동에 따른 objective penalty.
- **제약식:** 나머지 제약 feasibility 재조정.
- **Solver 구조:** Variable Cells Reduced Cost.
- **결과 해석:** 생산 안 하는 이유를 자원 가치와 비교해 설명한다.
- **코칭 순서:**
1. x1 final value 확인.
2. reduced cost 확인.
3. 강제 생산 시 목적값 변화 해석.
- **Evidence anchors:** `ev_deep_DM_PDF02_example_reduced_cost_stroller` -> `DM_PDF02:p028:L003` / page=`p028`, block=`p028-L003`, line=`L003`

> 근거 excerpt: 유모차의 현재 계산값을 ‘0’에서 ‘1개’를 증가시키면,


## 8. Modeling Pattern Library

| pattern | 모형화 템플릿 | 먼저 볼 노드 | 연결 노드 |
| --- | --- | --- | --- |
| 자원가치형 | RHS 1단위 변화 질문은 shadow price와 allowable RHS range로 답한다. | shadow_price | duality |
| 제품경쟁력형 | 현재 0인 변수의 진입 질문은 reduced cost와 목적계수 허용범위로 답한다. | reduced_cost | tableau reduced cost |
| 보고서해석형 | Solver sensitivity report는 Variable Cells와 Constraints를 분리해 읽는다. | solver_sensitivity_report | Excel Solver |

## 9. Spreadsheet / Solver Mapping

| 요소 | Solver/Spreadsheet 대응 | 튜터 해설 포인트 |
| --- | --- | --- |
| 변수셀 | x1 유모차 생산량, x2 보행기 생산량 | Variable Cells에서 final value, reduced cost, objective coefficient를 읽는다. |
| 목표셀 | 총판매이익 | 목표계수 변화는 Objective Coefficient range로 해석한다. |
| 제약셀 | 기계시간/수요 제약 LHS | Constraints에서 final value, shadow price, RHS range를 읽는다. |
| 주의 | 허용범위 밖 변화 | 기존 보고서 숫자를 쓰지 말고 다시 Solver/그래프 해법을 실행한다. |

## 10. Cross-Chapter Connections

| 연결 대상 | 연결 설명 | 의존/참조 관계 |
| --- | --- | --- |
| DM_PDF05 쌍대성 | shadow price는 쌍대변수의 경제적 의미와 직접 연결된다. | dual variable -> shadow price |
| DM_PDF06 수송 민감도 | 수송비와 공급량 변화도 reduced cost/shadow price로 해석한다. | sensitivity -> transportation |
| DM_PDF01 타블로 | reduced cost는 최종 타블로 목적행 계수와 같은 정보를 담는다. | tableau -> report |

## 11. Misconception & Error Diagnosis Bank

| 오답/착각 | 왜 문제인가 | 교정 코칭 | 연결 노드 |
| --- | --- | --- | --- |
| shadow price 무제한 적용 | 허용범위 밖에서는 basis가 바뀐다. | Allowable Increase/Decrease 확인 후 적용. | shadow_price |
| reduced cost를 회계비용으로 해석 | 현재 basis 기준의 기회비용이다. | 변수 final value와 함께 해석. | reduced_cost |
| Variable/Constraint 섹션 혼동 | 제품 계수와 자원 RHS 질문의 표가 다르다. | 질문 유형부터 분류. | solver_sensitivity_report |

## 12. Retrieval Routing Table

| 사용자 질문 유형 | 먼저 볼 노드 | 다음 볼 노드 | 예제 카드 | 근거 힌트 |
| --- | --- | --- | --- | --- |
| 자원 1단위 늘리면 이익? | `shadow_price` | `allowable_rhs_range` | `shadow_price_machine1` | DM_PDF02:p030 |
| 생산 안 하는 제품은 왜 안 해? | `reduced_cost` | `product_mix_model` | `reduced_cost_stroller` | DM_PDF02:p028 |
| 목적계수 바뀌면 해 유지돼? | `allowable_objective_range` | `solver_sensitivity_report` | `stroller_walker_lp` | DM_PDF02:p029 |
| 민감도 보고서 어디 봐? | `solver_sensitivity_report` | `sensitivity_analysis` | `stroller_walker_lp` | DM_PDF02:p026 |

## 13. Tutor Session Protocol

1. **지도부터:** Concept Graph Map과 Edge List를 먼저 보여주고, 현재 노드가 전체 OR/MS 흐름에서 어디인지 설명한다.
2. **노드 중심으로:** Core Concept Node Card의 18개 필드를 순서대로 따라가되, 선행/후속/동형 노드를 최소 3개 연결한다.
3. **예제 중심으로:** Example Walkthrough Card를 사용해 현실 문장 -> 변수 -> 목적함수 -> 제약식 -> Solver -> 결과 해석 순서로 진행한다.
4. **문제 풀이 모드:** 사용자가 변수를 먼저 말하게 하고, 목적함수/제약식은 힌트로 한 단계씩 유도한다.
5. **완성 해설 모드:** 위 절차를 생략하지 않고 전체 풀이를 한 번에 제시한다.
6. **암기/정리 모드:** Modeling Pattern Library, Solver Mapping, Misconception Bank만 압축해 제시한다.

## 14. Practice / Check Questions

1. 기계1 RHS가 3 감소할 때 허용범위 안이라면 이익 변화식을 써라.
2. reduced cost와 shadow price를 각각 변수 질문/제약 질문으로 분류하라.
3. 목적계수 허용범위를 벗어나면 왜 재최적화가 필요한지 설명하라.

## 15. Source Trace Table

| RAG label | evidence_id | source_id | page | block | line | excerpt |
| --- | --- | --- | --- | --- | --- | --- |
| `n_DM_PDF02.sensitivity_analysis` | `ev_deep_DM_PDF02_node_sensitivity_analysis` | `DM_PDF02` | `p023` | `p023-L001` | `L001` | 2.4. 민감도 분석 sensitivity analysis |
| `n_DM_PDF02.product_mix_model` | `ev_deep_DM_PDF02_node_product_mix_model` | `DM_PDF02` | `p005` | `p005-L003` | `L003` | 유모차 생산량: x1 |
| `n_DM_PDF02.binding_constraint` | `ev_deep_DM_PDF02_node_binding_constraint` | `DM_PDF02` | `p023` | `p023-L012` | `L012` | 목적함수 계수 및 제한조건 우변값 |
| `n_DM_PDF02.shadow_price` | `ev_deep_DM_PDF02_node_shadow_price` | `DM_PDF02` | `p026` | `p026-L009` | `L009` | Shadow price |
| `n_DM_PDF02.reduced_cost` | `ev_deep_DM_PDF02_node_reduced_cost` | `DM_PDF02` | `p026` | `p026-L007` | `L007` | Reduced cost |
| `n_DM_PDF02.allowable_objective_range` | `ev_deep_DM_PDF02_node_allowable_objective_range` | `DM_PDF02` | `p024` | `p024-L002` | `L002` | 민감도 보고서 (목표셀 계수 변화시) |
| `n_DM_PDF02.allowable_rhs_range` | `ev_deep_DM_PDF02_node_allowable_rhs_range` | `DM_PDF02` | `p029` | `p029-L002` | `L002` | 민감도 분석(2): 허용 가능의 범위 (목표셀 계수) |
| `n_DM_PDF02.solver_sensitivity_report` | `ev_deep_DM_PDF02_node_solver_sensitivity_report` | `DM_PDF02` | `p024` | `p024-L002` | `L002` | 민감도 보고서 (목표셀 계수 변화시) |
| `ex_DM_PDF02.stroller_walker_lp` | `ev_deep_DM_PDF02_example_stroller_walker_lp` | `DM_PDF02` | `p005` | `p005-L003` | `L003` | 유모차 생산량: x1 |
| `ex_DM_PDF02.shadow_price_machine1` | `ev_deep_DM_PDF02_example_shadow_price_machine1` | `DM_PDF02` | `p030` | `p030-L003` | `L003` | 기계1의 제한조건을 241시간으로 1시간 더 증가시키면, |
| `ex_DM_PDF02.reduced_cost_stroller` | `ev_deep_DM_PDF02_example_reduced_cost_stroller` | `DM_PDF02` | `p028` | `p028-L003` | `L003` | 유모차의 현재 계산값을 ‘0’에서 ‘1개’를 증가시키면, |

## 16. QC / Extraction Risk Notes

- **page_count:** 43
- **low_text_pages:** 11
- **extraction_risk_pages:** 11
- **QC policy:** 표, 그림, 수식 이미지가 많은 페이지는 전사 텍스트만으로 숫자를 단정하지 않는다. 튜터는 수식 구조와 증거 anchor를 우선 제시하고, 숫자 최적해는 필요 시 원본 PDF를 대조한다.
