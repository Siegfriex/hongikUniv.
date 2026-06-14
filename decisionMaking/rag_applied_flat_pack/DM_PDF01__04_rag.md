# DM_PDF01 — Ch.4 심플렉스 타블로 보완과 2단계법 최종 RAG 튜터 운영문서

## 0. Document Contract

- **문서 성격:** PDF 요약본이 아니라, 전담 1:1 경영과학 튜터와 RAG agent가 함께 쓰는 증거 기반 운영문서다.
- **source_id:** `DM_PDF01`
- **normalized_pdf:** `decisionMaking/pdf_sources/DM_PDF01_ch04_simplex_tableau_twophase_supplement.pdf`
- **primary transcript:** `decisionMaking/pdf_transcripts/DM_PDF01__ch04_simplex_tableau_twophase_supplement__full_transcript.md`
- **sidecar:** `decisionMaking/_inventory/DM_PDF01__ch04_simplex_tableau_twophase_supplement`
- **flat-pack target:** `decisionMaking/rag_applied_flat_pack/DM_PDF01__04_rag.md`
- **source priority:** 1) PDF 전사본 anchor, 2) 이 문서의 enhanced sidecar, 3) 웹 그라운딩, 4) 일반 OR/MS 지식.
- **중요한 명명 주의:** `DM_PDF01`는 PDF intake index다. 강의 회차/장 번호와 혼동하지 않는다.

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
| p001 | `DM_PDF01:p001:L001, DM_PDF01:p001:L002` | - 1 - / 4.5 심플렉스법 보완(예 1) / 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40 | ok |
| p002 | `DM_PDF01:p002:L001, DM_PDF01:p002:L002` | - 3 - / (예 2) / 복수 최적해 갖는 경우 (비기저변수의 목적함수 계수가 0)max  max  s/t ≤s/t   ≤ ==>  ≤   ≤  ≥≥≥ ≥기저우변비율1-60-35-2000000086110004848/8=60433/201002020/4=502*3/21/2001088/2=4001000015 | ok |
| p003 | `DM_PDF01:p003:L001, DM_PDF01:p003:L002` | - 5 - / (예3) / 목적함수 값을 무한히 개선시킬 수 있는 경우 (max 문제)기저우변비율1-36-3034000011-101055/1=506*50-1011010/6=5/31003-20660001/6-11/6*1-1/610/3(10/3)/(1/6)=20015/60-1/601/65/3102-90124100001-616-120011-10105* 을 진입시키면 목적함수는 개선된다. | ok |
| p004 | `DM_PDF01:p004:L001, DM_PDF01:p004:L002` | - 7 - / 2단계 해법(Two-phase method, 2국면법)(초기 기저가능해가 주어지지 않은 문제에 적용)(예4) / max  s/t ≤ ≥ ≥≥* 여유변수(slack variable)와 잉여변수(surplus variable)를 도입하여 표준형으로 변환한다. | ok |
| p005 | `DM_PDF01:p005:L001, DM_PDF01:p005:L002` | - 9 - / 1단계 문제(Phase I problem) / min  s/t     ≥≥≥≥≥≥-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------(정리) | ok |
| p006 | `DM_PDF01:p006:L001, DM_PDF01:p006:L002` | - 11 - / 기저우변비율12/3001/3-4/3010/305/12011/12-1/1207/3(7/3)/(5/12)=28/501/310-1/31/3020/3(20/3)/(1/3)=2002/3*001/3-1/3110/3(10/3)/(2/3)=510000-1-100001-1/81/8-5/81/40010-1/21/2-1/2501001/2-1/23/25최적!* 마지막 타블로에서 목적함수 값=0, 인위변수()가 모두 비기저변수임.* 이 비기저변수들을 제거시키면 원래 변수들로만 이루어지고, 초기 기저가능해를 갖는다. / * 위에서 비기저변수들을 제거시키고, 원래 변수들로만 이루어진, 초기 기저가능해를 갖는 등식에 원래 문제의 목적함수를 추가한 문제를 2단계 문제 (Phase II problem)이라고 한다. | ok |
| p007 | `DM_PDF01:p007:L001, DM_PDF01:p007:L002` | - 13 - / 기저우변비율1000-1/2250001-1/81/40010-1/2501001/2*55/(1/2)=10110003001/40103/201100100200110* 원 문제의 최적해  / - 14 - | ok |
| p008 | `DM_PDF01:p008:L001, DM_PDF01:p008:L002` | - 15 - / (P2) min  s/t    ≥* 1단계 문제: / 인위변수의 합을 최소화 한다.(P3) min  s/t    ≥ | ok |
| p009 | `DM_PDF01:p009:L001, DM_PDF01:p009:L002` | - 17 - / 기저우변100000000-1-1003/4-1/201-3/41/2-3/41/23/4-1/230/40-1/41/2105/41/21/4-1/2-1/41/270/4* 1단계 최적해 구하였음. / 최적해에서 은 비기저변수이고, 최적목적함수 값은 0 이다. 즉, 원 문제 가능해 존재한다.* 이제 을 제거하면, 초기 기저가능해를 갖는 제약식에 문제(P2)의 목적함수를 적용한 2단계 문제를 푼다. (초기 기저변수 )(P4) | ok |
| p010 | `DM_PDF01:p010:L001, DM_PDF01:p010:L002` | - 19 - / 기저우변비율1-32-22-30-3600-3-863003/4-1/43/45/401-3/41/490/40-1/21/21/2-1/2101/2-1/25* 최적해  | ok |

## 2. Chapter Thesis

그래프 해법의 꼭짓점 이동 원리를 타블로 계산으로 구현하고, 초기 BFS가 없을 때 2단계법으로 출발 가능한 기저를 만든다.

## 3. Current Graph Position

- **현재 그래프 위치:** LP 일반형 -> 표준형/정규형 -> BFS -> tableau -> pivot -> 특수 경우 -> two-phase method.
- **지금 보는 노드:** `DM_PDF01` / Ch.4 심플렉스 타블로 보완과 2단계법
- **튜터 운영 원칙:** 질문이 들어오면 먼저 노드로 매핑하고, 예제 카드와 수식/Solver 구조를 거쳐 Source Trace Table의 evidence anchor로 되돌아간다.

## 4. Learning Outcomes

- 타블로에서 entering variable, leaving variable, minimum ratio test를 분리해서 설명한다.
- 복수 최적해, 비유계, infeasible을 타블로 신호로 판별한다.
- 인위변수와 Phase I/Phase II가 왜 필요한지 식단형 최소화 문제와 연결한다.

## 5. Concept Graph Map

| node_id | 개념 | 역할 | 선행 노드 | 후속 노드 |
| --- | --- | --- | --- | --- |
| `n_DM_PDF01.simplex_tableau` | 심플렉스 타블로 | 목적행, 제약행, 기저변수, RHS, 비율검사를 한 표에 모은 심플렉스 계산 장치다. | 표준형, 정규형, slack variable | minimum ratio test, pivot, optimality test |
| `n_DM_PDF01.entering_leaving_variable` | 진입/탈락변수 | 목적값을 개선할 변수와 feasibility를 지키기 위해 기저에서 빠질 변수를 짝으로 고르는 규칙이다. | simplex tableau | pivot operation |
| `n_DM_PDF01.minimum_ratio_test` | 최소비율검사 | 진입변수를 얼마나 늘릴 수 있는지 RHS/a_ij 중 최소 양수 비율로 판정하는 절차다. | entering variable | pivot operation |
| `n_DM_PDF01.pivot_operation` | 피벗 연산 | pivot element를 1로 만들고 같은 열의 다른 값을 0으로 만들어 새 canonical form을 만드는 행 연산이다. | minimum ratio test | optimality test |
| `n_DM_PDF01.optimality_test` | 최적성 판정 | 목적행에 더 이상 개선 가능한 계수가 없으면 현재 BFS가 최적이라고 판정하는 규칙이다. | pivot operation | multiple optima |
| `n_DM_PDF01.multiple_optima` | 복수 최적해 | 최적 타블로에서 비기저변수의 reduced cost가 0이면 다른 최적 BFS가 존재할 수 있다. | optimality test | sensitivity objective range |
| `n_DM_PDF01.unbounded_solution` | 비유계 | feasible 해는 있지만 목적함수를 한없이 개선할 수 있어 유한 최적값이 없는 상태다. | minimum ratio test | model validation |
| `n_DM_PDF01.surplus_artificial_variable` | 잉여/인위변수 | >= 제약이나 = 제약에서 초기 기저를 만들기 위해 surplus를 빼고 artificial을 더하는 보조 변수다. | standard form | two-phase method, Big-M |
| `n_DM_PDF01.two_phase_method` | 2단계법 | Phase I에서 인위변수 합을 0으로 만들고, Phase II에서 원 목적함수로 최적화하는 심플렉스 절차다. | artificial variable | Big-M, duality |
| `n_DM_PDF01.diet_two_phase` | 식단문제 2단계 적용 | 영양 최소 요구량을 만족하는 최소비용 식단을 2단계법으로 푸는 대표 min LP 예제다. | two-phase method | Big-M, duality |

### Edge List

| from | edge_type | to |
| --- | --- | --- |
| `표준형, 정규형, slack variable` | 선행 관계 | `n_DM_PDF01.simplex_tableau` |
| `n_DM_PDF01.simplex_tableau` | 후속 관계 | `minimum ratio test, pivot, optimality test` |
| `n_DM_PDF01.simplex_tableau` | 동형/유사 | `그래프 해법의 꼭짓점 최적성` |
| `simplex tableau` | 선행 관계 | `n_DM_PDF01.entering_leaving_variable` |
| `n_DM_PDF01.entering_leaving_variable` | 후속 관계 | `pivot operation` |
| `n_DM_PDF01.entering_leaving_variable` | 동형/유사 | `network flow의 arc flow 증가/용량 한계` |
| `entering variable` | 선행 관계 | `n_DM_PDF01.minimum_ratio_test` |
| `n_DM_PDF01.minimum_ratio_test` | 후속 관계 | `pivot operation` |
| `n_DM_PDF01.minimum_ratio_test` | 동형/유사 | `capacity constraint의 bottleneck` |
| `minimum ratio test` | 선행 관계 | `n_DM_PDF01.pivot_operation` |
| `n_DM_PDF01.pivot_operation` | 후속 관계 | `optimality test` |
| `n_DM_PDF01.pivot_operation` | 동형/유사 | `Gauss-Jordan elimination` |
| `pivot operation` | 선행 관계 | `n_DM_PDF01.optimality_test` |
| `n_DM_PDF01.optimality_test` | 후속 관계 | `multiple optima` |
| `n_DM_PDF01.optimality_test` | 동형/유사 | `reduced cost` |
| `optimality test` | 선행 관계 | `n_DM_PDF01.multiple_optima` |
| `n_DM_PDF01.multiple_optima` | 후속 관계 | `sensitivity objective range` |
| `n_DM_PDF01.multiple_optima` | 동형/유사 | `assignment의 복수 최적` |
| `minimum ratio test` | 선행 관계 | `n_DM_PDF01.unbounded_solution` |
| `n_DM_PDF01.unbounded_solution` | 후속 관계 | `model validation` |
| `n_DM_PDF01.unbounded_solution` | 동형/유사 | `open feasible region` |
| `standard form` | 선행 관계 | `n_DM_PDF01.surplus_artificial_variable` |
| `n_DM_PDF01.surplus_artificial_variable` | 후속 관계 | `two-phase method, Big-M` |
| `n_DM_PDF01.surplus_artificial_variable` | 동형/유사 | `dummy supply와 달리 계산용 변수` |
| `artificial variable` | 선행 관계 | `n_DM_PDF01.two_phase_method` |
| `n_DM_PDF01.two_phase_method` | 후속 관계 | `Big-M, duality` |
| `n_DM_PDF01.two_phase_method` | 동형/유사 | `penalty method` |
| `two-phase method` | 선행 관계 | `n_DM_PDF01.diet_two_phase` |
| `n_DM_PDF01.diet_two_phase` | 후속 관계 | `Big-M, duality` |
| `n_DM_PDF01.diet_two_phase` | 동형/유사 | `Stigler diet problem` |

## 6. Core Concept Node Cards

### n_DM_PDF01.simplex_tableau — 심플렉스 타블로 (simplex tableau)

1. **한 줄 정의:** 목적행, 제약행, 기저변수, RHS, 비율검사를 한 표에 모은 심플렉스 계산 장치다.
2. **쉬운 직관:** 그래프에서 꼭짓점을 옮기는 일을 표의 행 연산과 기저 교체로 수행한다.
3. **언제 쓰는가:** 2변수 그래프 해법을 일반 차원 LP로 확장할 때 쓴다.
4. **변수 정의:** x1, x2 같은 원변수와 slack/surplus/artificial 변수를 함께 둔다.
5. **목적함수:** max z 또는 min w의 목적행을 기준으로 개선 가능 열을 찾는다.
6. **제약식:** 제약행은 현재 BFS의 자원 사용과 남은 여유를 RHS로 보여준다.
7. **수식의 현실 의미:** 현재 생산계획에서 어떤 활동을 기저에 넣으면 목적값이 개선되는지 묻는 계산표다.
8. **그래프/네트워크 관점:** 가능영역 꼭짓점은 tableau의 BFS와 대응한다.
9. **스프레드시트/Solver 관점:** Solver의 Simplex LP가 내부적으로 하는 basis 이동을 사람이 읽을 수 있는 표로 드러낸다.
10. **강의 예제 연결:** 예1의 max z=3x1+2x2 타블로 전개.
11. **예제 숫자 해석:** 최종 타블로의 x1, x2, slack 값과 z 값을 현실 생산량과 여유자원으로 해석한다.
12. **자주 하는 실수:** 모든 행에 비율검사를 적용하는 오류. entering 열 계수가 양수인 행만 후보가 된다.
13. **선행 노드:** 표준형, 정규형, slack variable
14. **후속 노드:** minimum ratio test, pivot, optimality test
15. **동형/유사 노드:** 그래프 해법의 꼭짓점 최적성
16. **시험 출제 포인트:** 타블로 한 행을 주고 다음 피벗을 묻는다.
17. **RAG retrieval tags:** `simplex`, `tableau`, `BFS`, `pivot`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_simplex_tableau` -> `DM_PDF01:p001:L003` / source_id=`DM_PDF01`, page=`p001`, block=`p001-L003`, line=`L003`

> 근거 excerpt: 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40

### n_DM_PDF01.entering_leaving_variable — 진입/탈락변수 (entering/leaving variable)

1. **한 줄 정의:** 목적값을 개선할 변수와 feasibility를 지키기 위해 기저에서 빠질 변수를 짝으로 고르는 규칙이다.
2. **쉬운 직관:** 새 활동을 늘리면 어떤 기존 여유/활동이 먼저 한계에 닿는지 찾는다.
3. **언제 쓰는가:** 각 반복에서 다음 BFS를 결정할 때 쓴다.
4. **변수 정의:** entering variable은 비기저변수, leaving variable은 현재 기저변수다.
5. **목적함수:** max에서는 보통 목적행의 음의 계수 중 개선 폭이 큰 열을 고른다.
6. **제약식:** minimum ratio test가 음수가 되지 않는 RHS 한계를 만든다.
7. **수식의 현실 의미:** 생산활동을 늘리다가 가장 먼저 소진되는 자원을 leaving으로 본다.
8. **그래프/네트워크 관점:** 인접 꼭짓점 이동의 방향과 도착 꼭짓점이다.
9. **스프레드시트/Solver 관점:** Solver에서는 직접 보이지 않지만 반복 로그의 basis change와 대응한다.
10. **강의 예제 연결:** 예1의 x1 진입, slack 변수 탈락 과정.
11. **예제 숫자 해석:** 40/1, 100/2 등 비율은 가능한 증가량이다.
12. **자주 하는 실수:** 음수 또는 0 이하 계수 행을 ratio 후보로 넣는 실수.
13. **선행 노드:** simplex tableau
14. **후속 노드:** pivot operation
15. **동형/유사 노드:** network flow의 arc flow 증가/용량 한계
16. **시험 출제 포인트:** 다음 pivot 열/행 선택.
17. **RAG retrieval tags:** `entering`, `leaving`, `ratio`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_entering_leaving_variable` -> `DM_PDF01:p001:L003` / source_id=`DM_PDF01`, page=`p001`, block=`p001-L003`, line=`L003`

> 근거 excerpt: 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40

### n_DM_PDF01.minimum_ratio_test — 최소비율검사 (minimum ratio test)

1. **한 줄 정의:** 진입변수를 얼마나 늘릴 수 있는지 RHS/a_ij 중 최소 양수 비율로 판정하는 절차다.
2. **쉬운 직관:** 새 변수를 늘릴 때 가장 먼저 0이 되는 기존 기저변수를 찾는다.
3. **언제 쓰는가:** feasibility를 유지하면서 pivot row를 정할 때 쓴다.
4. **변수 정의:** RHS와 entering 열의 양수 계수만 사용한다.
5. **목적함수:** 목적함수와 직접 관계하지 않고 feasible movement의 한계를 찾는다.
6. **제약식:** RHS/a_ij가 가장 작은 행이 leaving row가 된다.
7. **수식의 현실 의미:** 자원 소모량 대비 남은 자원이 가장 빨리 소진되는 제약을 찾는다.
8. **그래프/네트워크 관점:** 그래프에서는 이동 방향으로 닿는 첫 경계다.
9. **스프레드시트/Solver 관점:** 스프레드시트 수동 계산에서는 ratio 열을 따로 만든다.
10. **강의 예제 연결:** 예1과 Phase I 타블로의 비율 열.
11. **예제 숫자 해석:** 50, 80, 40 중 최소가 leaving 후보가 되는 식으로 해석한다.
12. **자주 하는 실수:** a_ij<=0인 행을 포함하거나 최대비율을 고르는 오류.
13. **선행 노드:** entering variable
14. **후속 노드:** pivot operation
15. **동형/유사 노드:** capacity constraint의 bottleneck
16. **시험 출제 포인트:** 비율검사 후보와 제외 행 구분.
17. **RAG retrieval tags:** `minimum_ratio`, `ratio`, `leaving`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_minimum_ratio_test` -> `DM_PDF01:p001:L003` / source_id=`DM_PDF01`, page=`p001`, block=`p001-L003`, line=`L003`

> 근거 excerpt: 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40

### n_DM_PDF01.pivot_operation — 피벗 연산 (pivot operation)

1. **한 줄 정의:** pivot element를 1로 만들고 같은 열의 다른 값을 0으로 만들어 새 canonical form을 만드는 행 연산이다.
2. **쉬운 직관:** 좌표축을 새 기저변수 기준으로 갈아끼우는 과정이다.
3. **언제 쓰는가:** entering/leaving 변수가 정해진 뒤 tableau를 갱신할 때 쓴다.
4. **변수 정의:** 기저변수 목록과 tableau 행 전체가 바뀐다.
5. **목적함수:** 목적행도 함께 갱신되어 z값 개선이 반영된다.
6. **제약식:** 새 기저변수의 열은 단위벡터가 되어야 한다.
7. **수식의 현실 의미:** 새 생산계획의 기준 활동을 바꾸는 회계 재정리다.
8. **그래프/네트워크 관점:** BFS에서 인접 BFS로 이동한다.
9. **스프레드시트/Solver 관점:** Solver 내부 basis factorization의 수동판이다.
10. **강의 예제 연결:** 예1의 여러 tableau 갱신.
11. **예제 숫자 해석:** pivot 후 RHS가 새 BFS의 변수값이다.
12. **자주 하는 실수:** pivot row만 바꾸고 나머지 행을 소거하지 않는 실수.
13. **선행 노드:** minimum ratio test
14. **후속 노드:** optimality test
15. **동형/유사 노드:** Gauss-Jordan elimination
16. **시험 출제 포인트:** pivot 이후 목적행 부호 해석.
17. **RAG retrieval tags:** `pivot`, `basis`, `tableau`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_pivot_operation` -> `DM_PDF01:p001:L003` / source_id=`DM_PDF01`, page=`p001`, block=`p001-L003`, line=`L003`

> 근거 excerpt: 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40

### n_DM_PDF01.optimality_test — 최적성 판정 (optimality test)

1. **한 줄 정의:** 목적행에 더 이상 개선 가능한 계수가 없으면 현재 BFS가 최적이라고 판정하는 규칙이다.
2. **쉬운 직관:** 더 좋은 인접 꼭짓점으로 갈 방향이 남아 있는지 확인한다.
3. **언제 쓰는가:** 각 pivot 후 반복 종료 여부를 결정할 때 쓴다.
4. **변수 정의:** 비기저변수의 reduced cost/목적행 계수를 본다.
5. **목적함수:** max 문제와 min 문제의 부호 판정이 달라질 수 있다.
6. **제약식:** 개선 가능한 계수가 없으면 stop, 0 계수는 대안 최적 가능성을 뜻한다.
7. **수식의 현실 의미:** 어떤 생산활동을 추가해도 이익을 늘릴 수 없다는 뜻이다.
8. **그래프/네트워크 관점:** 목적 등위선이 최적 꼭짓점에 닿은 상태다.
9. **스프레드시트/Solver 관점:** Solver 결과 상태 optimal과 연결된다.
10. **강의 예제 연결:** 예1 최종 타블로.
11. **예제 숫자 해석:** z=180 또는 z=30 같은 목적값을 변수값과 함께 읽는다.
12. **자주 하는 실수:** 최적 판정과 feasible 판정을 혼동하는 오류.
13. **선행 노드:** pivot operation
14. **후속 노드:** multiple optima
15. **동형/유사 노드:** reduced cost
16. **시험 출제 포인트:** 최적/복수최적/계속진행 구분.
17. **RAG retrieval tags:** `optimality`, `reduced_cost`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_optimality_test` -> `DM_PDF01:p002:L003` / source_id=`DM_PDF01`, page=`p002`, block=`p002-L003`, line=`L003`

> 근거 excerpt: 복수 최적해 갖는 경우 (비기저변수의 목적함수 계수가 0)max  max  s/t ≤s/t   ≤ ==>  ≤   ≤  ≥≥≥ ≥기저우변비율1-60-35-2000000086110004848/8=60433/201002020/4=502*3/21/2001088/2=4001000015

### n_DM_PDF01.multiple_optima — 복수 최적해 (multiple optimal solutions)

1. **한 줄 정의:** 최적 타블로에서 비기저변수의 reduced cost가 0이면 다른 최적 BFS가 존재할 수 있다.
2. **쉬운 직관:** 목적함수 선이 가능영역의 모서리와 겹쳐 여러 점이 같은 목적값을 준다.
3. **언제 쓰는가:** 최적성 판정 후 대안 해 여부를 확인할 때 쓴다.
4. **변수 정의:** 0 reduced cost인 nonbasic variable을 피벗 후보로 본다.
5. **목적함수:** 목적값은 변하지 않고 해 벡터만 바뀐다.
6. **제약식:** 새 pivot을 해도 z가 동일하면 대안 최적해를 얻는다.
7. **수식의 현실 의미:** 서로 다른 생산계획이 같은 총이익을 만드는 상황이다.
8. **그래프/네트워크 관점:** 최적 face 위의 여러 BFS/convex combination.
9. **스프레드시트/Solver 관점:** Solver가 하나만 보여줘도 동률 최적해가 있을 수 있다.
10. **강의 예제 연결:** 예2의 z=280 대안 최적해.
11. **예제 숫자 해석:** 두 해 모두 z=280으로 동일하다는 점이 핵심이다.
12. **자주 하는 실수:** 복수 최적을 아무 feasible point가 최적인 것처럼 말하는 오류.
13. **선행 노드:** optimality test
14. **후속 노드:** sensitivity objective range
15. **동형/유사 노드:** assignment의 복수 최적
16. **시험 출제 포인트:** reduced cost 0의 의미.
17. **RAG retrieval tags:** `multiple_optima`, `alternate_optimum`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_multiple_optima` -> `DM_PDF01:p002:L003` / source_id=`DM_PDF01`, page=`p002`, block=`p002-L003`, line=`L003`

> 근거 excerpt: 복수 최적해 갖는 경우 (비기저변수의 목적함수 계수가 0)max  max  s/t ≤s/t   ≤ ==>  ≤   ≤  ≥≥≥ ≥기저우변비율1-60-35-2000000086110004848/8=60433/201002020/4=502*3/21/2001088/2=4001000015

### n_DM_PDF01.unbounded_solution — 비유계 (unbounded solution)

1. **한 줄 정의:** feasible 해는 있지만 목적함수를 한없이 개선할 수 있어 유한 최적값이 없는 상태다.
2. **쉬운 직관:** 좋아지는 방향으로 움직이는데 제약 벽이 없는 경우다.
3. **언제 쓰는가:** entering 열에 leaving 후보가 없을 때 판정한다.
4. **변수 정의:** 진입변수는 늘어날 수 있지만 모든 관련 제약이 막지 않는다.
5. **목적함수:** max에서는 z가 무한 증가할 수 있다.
6. **제약식:** entering column의 모든 제약행 계수가 <=0이면 ratio test가 불가능하다.
7. **수식의 현실 의미:** 제약을 빠뜨린 생산모형일 가능성이 크다.
8. **그래프/네트워크 관점:** 가능영역이 목적 개선 방향으로 열린 상태다.
9. **스프레드시트/Solver 관점:** Solver에서는 unbounded 또는 model issue로 나타날 수 있다.
10. **강의 예제 연결:** 예3의 x3 진입 시 목적함수 무한 개선.
11. **예제 숫자 해석:** 비유계는 infeasible과 달리 feasible point가 존재한다.
12. **자주 하는 실수:** 비유계와 실행불가능을 혼동하는 오류.
13. **선행 노드:** minimum ratio test
14. **후속 노드:** model validation
15. **동형/유사 노드:** open feasible region
16. **시험 출제 포인트:** unbounded 신호와 누락 제약 찾기.
17. **RAG retrieval tags:** `unbounded`, `비유계`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_unbounded_solution` -> `DM_PDF01:p003:L003` / source_id=`DM_PDF01`, page=`p003`, block=`p003-L003`, line=`L003`

> 근거 excerpt: 목적함수 값을 무한히 개선시킬 수 있는 경우 (max 문제)기저우변비율1-36-3034000011-101055/1=506*50-1011010/6=5/31003-20660001/6-11/6*1-1/610/3(10/3)/(1/6)=20015/60-1/601/65/3102-90124100001-616-120011-10105* 을 진입시키면 목적함수는 개선된다.

### n_DM_PDF01.surplus_artificial_variable — 잉여/인위변수 (surplus/artificial variable)

1. **한 줄 정의:** >= 제약이나 = 제약에서 초기 기저를 만들기 위해 surplus를 빼고 artificial을 더하는 보조 변수다.
2. **쉬운 직관:** slack은 남는 양, surplus는 초과량, artificial은 임시 발판이다.
3. **언제 쓰는가:** 초기 BFS가 보이지 않는 min/greater-than 제약에서 쓴다.
4. **변수 정의:** surplus s>=0, artificial r>=0를 원 제약에 넣는다.
5. **목적함수:** artificial은 원래 문제의 목적이 아니므로 제거되어야 한다.
6. **제약식:** Phase I 또는 Big-M에서 artificial을 0으로 몰아낸다.
7. **수식의 현실 의미:** 최소 영양 요구량처럼 >= 제약이 있을 때 바로 slack basis가 안 생긴다.
8. **그래프/네트워크 관점:** 기저를 만들기 위한 좌표 보강이다.
9. **스프레드시트/Solver 관점:** Solver는 내부적으로 처리하지만 손계산은 변수를 명시한다.
10. **강의 예제 연결:** 예4와 식단 문제의 x5, x6, x9, x10 도입.
11. **예제 숫자 해석:** artificial이 최종 양수이면 원문제 infeasible 가능성이 있다.
12. **자주 하는 실수:** artificial을 실제 의사결정변수로 해석하는 오류.
13. **선행 노드:** standard form
14. **후속 노드:** two-phase method, Big-M
15. **동형/유사 노드:** dummy supply와 달리 계산용 변수
16. **시험 출제 포인트:** 변수 도입 방향과 최종 제거 조건.
17. **RAG retrieval tags:** `surplus`, `artificial`, `인위변수`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_surplus_artificial_variable` -> `DM_PDF01:p004:L003` / source_id=`DM_PDF01`, page=`p004`, block=`p004-L003`, line=`L003`

> 근거 excerpt: max  s/t ≤ ≥ ≥≥* 여유변수(slack variable)와 잉여변수(surplus variable)를 도입하여 표준형으로 변환한다.

### n_DM_PDF01.two_phase_method — 2단계법 (two-phase method)

1. **한 줄 정의:** Phase I에서 인위변수 합을 0으로 만들고, Phase II에서 원 목적함수로 최적화하는 심플렉스 절차다.
2. **쉬운 직관:** 출발점이 없을 때 임시 발판을 찾아 치운 뒤 원래 문제를 푼다.
3. **언제 쓰는가:** 초기 BFS가 바로 없을 때 쓴다.
4. **변수 정의:** Phase I 변수에는 artificial variables가 포함된다.
5. **목적함수:** Phase I은 min w=sum artificial, Phase II는 원 z다.
6. **제약식:** w*=0이면 feasible basis를 얻고, w*>0이면 infeasible이다.
7. **수식의 현실 의미:** 식단 min 문제에서 영양 최소요구량 제약 때문에 필요하다.
8. **그래프/네트워크 관점:** 가능영역의 임의 꼭짓점부터 찾는 탐색 전처리다.
9. **스프레드시트/Solver 관점:** Solver의 feasible start 탐색을 수동으로 분리한 형태다.
10. **강의 예제 연결:** 예4와 식단문제 2단계 해법.
11. **예제 숫자 해석:** w=0은 원 목적값이 아니라 feasible start 판별값이다.
12. **자주 하는 실수:** Phase I 목적값을 원문제 최적값으로 착각하는 오류.
13. **선행 노드:** artificial variable
14. **후속 노드:** Big-M, duality
15. **동형/유사 노드:** penalty method
16. **시험 출제 포인트:** Phase I 종료 조건과 Phase II 전환.
17. **RAG retrieval tags:** `two_phase`, `Phase I`, `Phase II`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_two_phase_method` -> `DM_PDF01:p004:L002` / source_id=`DM_PDF01`, page=`p004`, block=`p004-L002`, line=`L002`

> 근거 excerpt: 2단계 해법(Two-phase method, 2국면법)(초기 기저가능해가 주어지지 않은 문제에 적용)(예4)

### n_DM_PDF01.diet_two_phase — 식단문제 2단계 적용 (diet problem two-phase)

1. **한 줄 정의:** 영양 최소 요구량을 만족하는 최소비용 식단을 2단계법으로 푸는 대표 min LP 예제다.
2. **쉬운 직관:** 필요 영양소를 넘겨야 하므로 >= 제약이 많아 초기 slack basis가 없다.
3. **언제 쓰는가:** 최소화 문제의 two-phase 훈련용 예제로 쓴다.
4. **변수 정의:** 식품량 xi와 surplus/artificial variables.
5. **목적함수:** min z=식품 단가*식품량.
6. **제약식:** 비타민 A/C 최소 요구량 제약과 비음조건.
7. **수식의 현실 의미:** 영양 요구량을 만족하면서 비용을 줄이는 식단 구성이다.
8. **그래프/네트워크 관점:** 두 영양 제약의 교차점과 비용 등위선으로도 볼 수 있다.
9. **스프레드시트/Solver 관점:** Solver에서는 변수셀 식품량, 제약셀 영양소 섭취량>=요구량.
10. **강의 예제 연결:** 식단문제 P0-P4 전개.
11. **예제 숫자 해석:** x5=22.5, x6=5 같은 해는 식품량 단위 해석이 필요하다.
12. **자주 하는 실수:** surplus와 artificial 부호를 뒤집는 오류.
13. **선행 노드:** two-phase method
14. **후속 노드:** Big-M, duality
15. **동형/유사 노드:** Stigler diet problem
16. **시험 출제 포인트:** >= 제약 표준화.
17. **RAG retrieval tags:** `diet`, `two_phase`, `min`
18. **Evidence anchors:** `ev_deep_DM_PDF01_node_diet_two_phase` -> `DM_PDF01:p004:L006` / source_id=`DM_PDF01`, page=`p004`, block=`p004-L006`, line=`L006`

> 근거 excerpt: max  s/t    ≥≥≥≥인위변수  도입하여 다시 쓰면앞문제와 동등max <===>s/t     ≥≥≥≥≥≥ * 억지로 새로 도입된 변수를 인위변수(artificial variable)이라고 한다.* 인위변수가 첨가된 문제는 원래 문제와 동등한 문제가 아니다.* 인위변수를 모두 0으로 만들기 위해 인위변수의 합을 최소화한다.


## 7. Example Walkthrough Cards

### ex_DM_PDF01.example1_tableau — 예1 기본 타블로 최적화

- **현실 문장 재해석:** max z=3x1+2x2를 slack 변수와 tableau로 풀어 최적 생산량을 찾는다.
- **의사결정변수:** x1, x2와 x3~x5 slack.
- **목적함수:** max z=3x1+2x2.
- **제약식:** 2x1+x2<=100, x1+x2<=80, x1<=40, x>=0.
- **Solver 구조:** 수동 tableau 또는 Solver Simplex LP.
- **결과 해석:** 최종 RHS가 변수값, z행 RHS가 목적값이다.
- **코칭 순서:**
1. 표준형으로 바꾼다.
2. 진입열과 탈락행을 고른다.
3. 피벗 후 목적행 개선 가능성을 확인한다.
- **Evidence anchors:** `ev_deep_DM_PDF01_example_example1_tableau` -> `DM_PDF01:p001:L003` / page=`p001`, block=`p001-L003`, line=`L003`

> 근거 excerpt: 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40

### ex_DM_PDF01.multiple_optimum — 예2 복수 최적해 판정

- **현실 문장 재해석:** 비기저변수 목적계수 0을 통해 같은 z=280의 대안 최적해를 찾는다.
- **의사결정변수:** x1, x2, x3 및 slack 변수.
- **목적함수:** max z=60x1+35x2+20x3.
- **제약식:** 여러 자원 제약과 x2<=5.
- **Solver 구조:** tableau에서 0 reduced cost pivot.
- **결과 해석:** 최적해가 하나가 아니라 최적 face임을 해석한다.
- **코칭 순서:**
1. 최적 타블로를 확인한다.
2. 0 reduced cost 비기저변수를 찾는다.
3. 대안 pivot으로 새 최적 BFS를 계산한다.
- **Evidence anchors:** `ev_deep_DM_PDF01_example_multiple_optimum` -> `DM_PDF01:p002:L003` / page=`p002`, block=`p002-L003`, line=`L003`

> 근거 excerpt: 복수 최적해 갖는 경우 (비기저변수의 목적함수 계수가 0)max  max  s/t ≤s/t   ≤ ==>  ≤   ≤  ≥≥≥ ≥기저우변비율1-60-35-2000000086110004848/8=60433/201002020/4=502*3/21/2001088/2=4001000015

### ex_DM_PDF01.unbounded_case — 예3 비유계 판정

- **현실 문장 재해석:** 진입변수를 늘려도 leaving 후보가 없어 목적값을 무한히 개선하는 사례다.
- **의사결정변수:** x variables and slack variables.
- **목적함수:** max objective.
- **제약식:** 제약이 개선 방향을 막지 못한다.
- **Solver 구조:** ratio test 불가 판정.
- **결과 해석:** 모형 제약 누락 또는 열린 가능영역으로 해석한다.
- **코칭 순서:**
1. entering 열을 고른다.
2. 양수 계수 행이 없는지 본다.
3. infeasible과 구분한다.
- **Evidence anchors:** `ev_deep_DM_PDF01_example_unbounded_case` -> `DM_PDF01:p003:L003` / page=`p003`, block=`p003-L003`, line=`L003`

> 근거 excerpt: 목적함수 값을 무한히 개선시킬 수 있는 경우 (max 문제)기저우변비율1-36-3034000011-101055/1=506*50-1011010/6=5/31003-20660001/6-11/6*1-1/610/3(10/3)/(1/6)=20015/60-1/601/65/3102-90124100001-616-120011-10105* 을 진입시키면 목적함수는 개선된다.

### ex_DM_PDF01.two_phase_example — 예4 2단계법

- **현실 문장 재해석:** 인위변수 x5, x6을 도입해 Phase I feasible basis를 만들고 Phase II에서 원 목적함수를 푼다.
- **의사결정변수:** x1, x2, x3, x4, artificial x5, x6.
- **목적함수:** Phase I min w, Phase II max z.
- **제약식:** 등식/부등식 변환 후 비음조건.
- **Solver 구조:** Phase I tableau -> artificial 제거 -> Phase II tableau.
- **결과 해석:** w*=0이면 원문제 가능해가 존재한다.
- **코칭 순서:**
1. 인위변수를 넣는다.
2. w를 최소화한다.
3. w=0이면 원 목적행으로 전환한다.
- **Evidence anchors:** `ev_deep_DM_PDF01_example_two_phase_example` -> `DM_PDF01:p004:L002` / page=`p004`, block=`p004-L002`, line=`L002`

> 근거 excerpt: 2단계 해법(Two-phase method, 2국면법)(초기 기저가능해가 주어지지 않은 문제에 적용)(예4)


## 8. Modeling Pattern Library

| pattern | 모형화 템플릿 | 먼저 볼 노드 | 연결 노드 |
| --- | --- | --- | --- |
| 표준형/타블로 | max/min LP를 등식과 비음조건으로 바꾼 뒤 tableau로 계산한다. | simplex_tableau | 2변수 그래프 해법의 일반화 |
| 특수 종료 | 최적성 이후 0 reduced cost, ratio 불가, w>0 여부로 복수최적/비유계/infeasible을 판정한다. | multiple_optima | solver status 해석 |
| 초기 BFS 생성 | slack만으로 basis가 없으면 artificial을 도입하고 Phase I을 실행한다. | two_phase_method | Big-M과 duality |

## 9. Spreadsheet / Solver Mapping

| 요소 | Solver/Spreadsheet 대응 | 튜터 해설 포인트 |
| --- | --- | --- |
| 변수셀 | 원변수+slack/surplus/artificial | 수동 타블로의 열과 Solver 변수셀을 대응시킨다. |
| 목표셀 | z 또는 Phase I의 w | Phase I w와 원 목적함수 z를 혼동하지 않는다. |
| 제약셀 | 등식 변환된 제약행 | RHS는 현재 BFS의 변수값으로 읽는다. |
| 해법 | Simplex LP | 초기 BFS가 없으면 two-phase/Big-M 설명을 붙인다. |

## 10. Cross-Chapter Connections

| 연결 대상 | 연결 설명 | 의존/참조 관계 |
| --- | --- | --- |
| 2강 LP 일반형 | 모든 tableau는 LP 변수/제약/목적함수에서 출발한다. | LP formulation -> tableau |
| 3강 그래프 해법 | 꼭짓점 최적성이 tableau의 BFS 이동으로 바뀐다. | vertex -> BFS |
| DM_PDF05 Big-M/쌍대 | artificial variable 처리와 dual interpretation으로 이어진다. | two-phase -> Big-M -> dual |

## 11. Misconception & Error Diagnosis Bank

| 오답/착각 | 왜 문제인가 | 교정 코칭 | 연결 노드 |
| --- | --- | --- | --- |
| 비율검사에 음수 계수 포함 | leaving row를 잘못 잡아 infeasible tableau가 된다. | 양수 entering column 계수만 ratio 후보. | minimum_ratio_test |
| w=0을 원 목적값으로 해석 | Phase I은 실행가능성 확인용이다. | Phase II에서 원 목적함수로 다시 최적화한다. | two_phase_method |
| 비유계와 infeasible 혼동 | 비유계는 feasible 해가 존재한다. | ratio 후보 없음과 w*>0을 분리한다. | unbounded_solution |

## 12. Retrieval Routing Table

| 사용자 질문 유형 | 먼저 볼 노드 | 다음 볼 노드 | 예제 카드 | 근거 힌트 |
| --- | --- | --- | --- | --- |
| 타블로에서 다음 피벗 어떻게 골라? | `simplex_tableau` | `entering_leaving_variable` | `example1_tableau` | DM_PDF01:p001 |
| 복수 최적해인지 어떻게 알아? | `multiple_optima` | `optimality_test` | `multiple_optimum` | DM_PDF01:p002 |
| 2단계법 왜 필요해? | `two_phase_method` | `surplus_artificial_variable` | `two_phase_example` | DM_PDF01:p004 |
| 비유계와 infeasible 차이? | `unbounded_solution` | `two_phase_method` | `unbounded_case` | DM_PDF01:p003 |

## 13. Tutor Session Protocol

1. **지도부터:** Concept Graph Map과 Edge List를 먼저 보여주고, 현재 노드가 전체 OR/MS 흐름에서 어디인지 설명한다.
2. **노드 중심으로:** Core Concept Node Card의 18개 필드를 순서대로 따라가되, 선행/후속/동형 노드를 최소 3개 연결한다.
3. **예제 중심으로:** Example Walkthrough Card를 사용해 현실 문장 -> 변수 -> 목적함수 -> 제약식 -> Solver -> 결과 해석 순서로 진행한다.
4. **문제 풀이 모드:** 사용자가 변수를 먼저 말하게 하고, 목적함수/제약식은 힌트로 한 단계씩 유도한다.
5. **완성 해설 모드:** 위 절차를 생략하지 않고 전체 풀이를 한 번에 제시한다.
6. **암기/정리 모드:** Modeling Pattern Library, Solver Mapping, Misconception Bank만 압축해 제시한다.

## 14. Practice / Check Questions

1. 타블로 하나를 골라 entering column과 leaving row를 말로 설명하라.
2. Phase I w*=0의 의미와 w*>0의 의미를 각각 한 문장으로 구분하라.
3. 비유계 신호를 ratio test 관점에서 설명하라.

## 15. Source Trace Table

| RAG label | evidence_id | source_id | page | block | line | excerpt |
| --- | --- | --- | --- | --- | --- | --- |
| `n_DM_PDF01.simplex_tableau` | `ev_deep_DM_PDF01_node_simplex_tableau` | `DM_PDF01` | `p001` | `p001-L003` | `L003` | 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40 |
| `n_DM_PDF01.entering_leaving_variable` | `ev_deep_DM_PDF01_node_entering_leaving_variable` | `DM_PDF01` | `p001` | `p001-L003` | `L003` | 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40 |
| `n_DM_PDF01.minimum_ratio_test` | `ev_deep_DM_PDF01_node_minimum_ratio_test` | `DM_PDF01` | `p001` | `p001-L003` | `L003` | 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40 |
| `n_DM_PDF01.pivot_operation` | `ev_deep_DM_PDF01_node_pivot_operation` | `DM_PDF01` | `p001` | `p001-L003` | `L003` | 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40 |
| `n_DM_PDF01.optimality_test` | `ev_deep_DM_PDF01_node_optimality_test` | `DM_PDF01` | `p002` | `p002-L003` | `L003` | 복수 최적해 갖는 경우 (비기저변수의 목적함수 계수가 0)max  max  s/t ≤s/t   ≤ ==>  ≤   ≤  ≥≥≥ ≥기저우변비율1-60-35-2000000086110004848/8=60433/201002020/4=502*3/21/2001088/2=4001000015 |
| `n_DM_PDF01.multiple_optima` | `ev_deep_DM_PDF01_node_multiple_optima` | `DM_PDF01` | `p002` | `p002-L003` | `L003` | 복수 최적해 갖는 경우 (비기저변수의 목적함수 계수가 0)max  max  s/t ≤s/t   ≤ ==>  ≤   ≤  ≥≥≥ ≥기저우변비율1-60-35-2000000086110004848/8=60433/201002020/4=502*3/21/2001088/2=4001000015 |
| `n_DM_PDF01.unbounded_solution` | `ev_deep_DM_PDF01_node_unbounded_solution` | `DM_PDF01` | `p003` | `p003-L003` | `L003` | 목적함수 값을 무한히 개선시킬 수 있는 경우 (max 문제)기저우변비율1-36-3034000011-101055/1=506*50-1011010/6=5/31003-20660001/6-11/6*1-1/610/3(10/3)/(1/6)=20015/60-1/601/65/3102-90124100001-616-120011-10105* 을 진입시키면 목적함수는 개선된다. |
| `n_DM_PDF01.surplus_artificial_variable` | `ev_deep_DM_PDF01_node_surplus_artificial_variable` | `DM_PDF01` | `p004` | `p004-L003` | `L003` | max  s/t ≤ ≥ ≥≥* 여유변수(slack variable)와 잉여변수(surplus variable)를 도입하여 표준형으로 변환한다. |
| `n_DM_PDF01.two_phase_method` | `ev_deep_DM_PDF01_node_two_phase_method` | `DM_PDF01` | `p004` | `p004-L002` | `L002` | 2단계 해법(Two-phase method, 2국면법)(초기 기저가능해가 주어지지 않은 문제에 적용)(예4) |
| `n_DM_PDF01.diet_two_phase` | `ev_deep_DM_PDF01_node_diet_two_phase` | `DM_PDF01` | `p004` | `p004-L006` | `L006` | max  s/t    ≥≥≥≥인위변수  도입하여 다시 쓰면앞문제와 동등max <===>s/t     ≥≥≥≥≥≥ * 억지로 새로 도입된 변수를 인위변수(artificial variable)이라고 한다.* 인위변수가 첨가된 문제는 원래 문제와 동등한 문제가 아니다.* 인위변수를 모두 0으로 만들기 위해 인위변수의 합을 최소화한다. |
| `ex_DM_PDF01.example1_tableau` | `ev_deep_DM_PDF01_example_example1_tableau` | `DM_PDF01` | `p001` | `p001-L003` | `L003` | 심플렉스 타블로를 이용하여 최적해 구하기max  max  s/t≤ s/t  ≤ ≤==>  ≥≥ ≥≥≥≥≥기저우변비율1-3-20000021100100100/2=500110108080/1=8001*00014040/1=40 |
| `ex_DM_PDF01.multiple_optimum` | `ev_deep_DM_PDF01_example_multiple_optimum` | `DM_PDF01` | `p002` | `p002-L003` | `L003` | 복수 최적해 갖는 경우 (비기저변수의 목적함수 계수가 0)max  max  s/t ≤s/t   ≤ ==>  ≤   ≤  ≥≥≥ ≥기저우변비율1-60-35-2000000086110004848/8=60433/201002020/4=502*3/21/2001088/2=4001000015 |
| `ex_DM_PDF01.unbounded_case` | `ev_deep_DM_PDF01_example_unbounded_case` | `DM_PDF01` | `p003` | `p003-L003` | `L003` | 목적함수 값을 무한히 개선시킬 수 있는 경우 (max 문제)기저우변비율1-36-3034000011-101055/1=506*50-1011010/6=5/31003-20660001/6-11/6*1-1/610/3(10/3)/(1/6)=20015/60-1/601/65/3102-90124100001-616-120011-10105* 을 진입시키면 목적함수는 개선된다. |
| `ex_DM_PDF01.two_phase_example` | `ev_deep_DM_PDF01_example_two_phase_example` | `DM_PDF01` | `p004` | `p004-L002` | `L002` | 2단계 해법(Two-phase method, 2국면법)(초기 기저가능해가 주어지지 않은 문제에 적용)(예4) |

## 16. QC / Extraction Risk Notes

- **page_count:** 10
- **low_text_pages:** 0
- **extraction_risk_pages:** 0
- **QC policy:** 표, 그림, 수식 이미지가 많은 페이지는 전사 텍스트만으로 숫자를 단정하지 않는다. 튜터는 수식 구조와 증거 anchor를 우선 제시하고, 숫자 최적해는 필요 시 원본 PDF를 대조한다.
- 수식 OCR이 깨진 페이지가 있어 숫자 타블로는 원본 PDF와 대조해야 한다.
