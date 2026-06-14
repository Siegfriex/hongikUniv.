# DecisionMaking G1 Visualization Spec

이 문서는 `decisionMaking/workshop`의 G1 문제 노트북을 위한 문항별 시각 튜터 설계서다.

원칙:

- 모든 시각화는 장식용이 아니라 최적해 이론의 판정 질문을 설명해야 한다.
- 기본 실행 경로는 local Python, numpy, matplotlib, nbformat만 사용한다.
- 외부 다운로드는 사용하지 않는다.
- 문제 노트북의 정답을 누출하지 않고, 개념 구조와 판정 기준을 시각화한다.
- 이미지 내부 라벨은 폰트 호환성을 위해 주로 영어를 쓰고, 해설은 한국어 markdown으로 제공한다.

## 전체 맵

| Phase | 문항 수 | 핵심 시각화 축 |
| --- | ---: | --- |
| P0001 | 10 | feasible region, BFS, ratio test, pivot, reduced cost, termination signal |
| P0002 | 10 | standard form conversion, artificial variable, Phase I/II transition, diet/Solver mapping |
| P0003 | 12 | Big-M penalty, primal-dual mapping, duality gap, complementary slackness, sensitivity routing |

## DM_G1_P0001_Q01 - 표준형 변환 기본

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.simplex_tableau`
- source anchor: `DM_PDF01:p001:L003`
- asset: `visual_assets/DM_G1_P0001_Q01__표준형_변환_기본.png`

시각화 목적: LP 문장을 실행가능영역, slack variable, 초기 BFS로 동시에 보는 그림을 제공한다.

사용할 데이터: 문항의 2변수 LP 계수와 RHS.

필요한 전처리: 제약식을 반평면으로 바꾸고, slack은 각 제약의 남는 거리로 해석한다.

코드 셀 설계: feasible region과 objective line을 한 평면에 그린다.

그래프 해석 포인트: 원점은 slack만 basis인 초기 BFS이고, shaded region이 모든 제약을 동시에 만족하는 영역이다.

학생이 자주 하는 오해: slack을 목적함수에 넣거나, 초기 basis에 원변수 x1/x2를 포함하는 오류.

체크포인트 질문: 초기 BFS에서 x1=x2=0일 때 각 slack 값은 무엇인가?

## DM_G1_P0001_Q02 - 첫 pivot 선택

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.entering_leaving_variable`, `n_DM_PDF01.minimum_ratio_test`
- source anchor: `DM_PDF01:p001:L003`
- asset: `visual_assets/DM_G1_P0001_Q02__첫_pivot_선택.png`

시각화 목적: entering column을 고른 뒤 ratio test가 leaving row를 어떻게 결정하는지 시각화한다.

사용할 데이터: 문항 1의 RHS와 x1 column 계수.

필요한 전처리: Dantzig rule로 x1을 entering 후보로 두고 RHS / positive column coefficient를 계산한다.

코드 셀 설계: ratio bar chart에서 최소 양수 ratio를 강조한다.

그래프 해석 포인트: 가장 작은 양수 ratio가 먼저 닿는 자원 한계를 뜻하며 leaving variable을 결정한다.

학생이 자주 하는 오해: 음수나 0 계수 행을 절댓값으로 바꿔 ratio 후보에 넣는 오류.

체크포인트 질문: 왜 ratio test는 양수 계수 행만 후보로 보는가?

## DM_G1_P0001_Q03 - 피벗 연산 구조 설명

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.pivot_operation`
- source anchor: `DM_PDF01:p001:L003`
- asset: `visual_assets/DM_G1_P0001_Q03__피벗_연산_구조_설명.png`

시각화 목적: pivot을 단순 행연산이 아니라 한 BFS에서 인접 BFS로 이동하는 과정으로 보여준다.

사용할 데이터: 문항 1의 feasible region과 첫 pivot 이동.

필요한 전처리: 첫 entering x1, leaving s3를 가정하고 원점에서 x1 방향으로 이동한다.

코드 셀 설계: feasible region 위에 BFS 이동 화살표를 표시한다.

그래프 해석 포인트: pivot row 정규화와 column 제거는 새 basis에서 해당 변수 하나만 1이 되게 만드는 대수적 장치다.

학생이 자주 하는 오해: pivot을 표 계산으로만 외우고, 그래프의 꼭짓점 이동 의미를 놓치는 오류.

체크포인트 질문: 첫 pivot 뒤 basis에는 어떤 변수가 들어오고 어떤 slack이 나가는가?

## DM_G1_P0001_Q04 - 타블로 판정 문제

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.optimality_test`, `n_DM_PDF01.multiple_optima`
- source anchor: `DM_PDF01:p002:L003`
- asset: `visual_assets/DM_G1_P0001_Q04__타블로_판정_문제.png`

시각화 목적: 최적성 판정 이후 reduced cost 0이 왜 복수 최적해 신호인지 보여준다.

사용할 데이터: 문항의 z-row nonbasic coefficients: x3=0, x4=2, x5=1.

필요한 전처리: 계수를 막대로 놓고 0인 비기저변수를 별도 색으로 표시한다.

코드 셀 설계: reduced cost bar chart와 대안 최적 진입 후보를 표시한다.

그래프 해석 포인트: 개선 가능한 계수가 없으면서 0 reduced cost가 있으면 같은 목적값의 인접해가 가능하다.

학생이 자주 하는 오해: Solver가 보여주는 하나의 최적해를 유일해라고 단정하는 오류.

체크포인트 질문: x3의 reduced cost가 0이라는 말은 objective value 관점에서 무슨 뜻인가?

## DM_G1_P0001_Q05 - 복수 최적해 예제 변형

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.multiple_optima`
- source anchor: `DM_PDF01:p002:L003`
- asset: `visual_assets/DM_G1_P0001_Q05__복수_최적해_예제_변형.png`

시각화 목적: 복수 최적해가 전체 feasible region이 아니라 최적 face에만 존재함을 2D로 보여준다.

사용할 데이터: 목적함수가 한 제약 경계와 평행한 illustrative LP.

필요한 전처리: x+y<=10, x<=8, y<=8 영역에서 x+y objective의 최적 edge를 표시한다.

코드 셀 설계: 최적 edge를 굵게 그리고 edge 밖 feasible point는 최적이 아님을 표시한다.

그래프 해석 포인트: 복수 최적해는 최적 face 위의 점들이 같은 값을 갖는다는 뜻이다.

학생이 자주 하는 오해: 복수 최적해를 '아무 feasible point나 최적'이라고 해석하는 오류.

체크포인트 질문: 대안 최적해를 찾으려면 어떤 reduced cost 조건을 봐야 하는가?

## DM_G1_P0001_Q06 - 비유계 판정

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.unbounded_solution`
- source anchor: `DM_PDF01:p003:L003`
- asset: `visual_assets/DM_G1_P0001_Q06__비유계_판정.png`

시각화 목적: ratio test 후보가 없을 때 objective가 끝없이 개선되는 구조를 2D ray로 보여준다.

사용할 데이터: 개선 방향은 있으나 positive pivot coefficient가 없는 illustrative feasible cone.

필요한 전처리: feasible cone과 objective improvement ray를 표시한다.

코드 셀 설계: unbounded ray와 missing upper-bound constraint를 함께 표시한다.

그래프 해석 포인트: 개선 가능한 entering variable이 있는데 ratio 후보가 없으면 infeasible이 아니라 unbounded 신호다.

학생이 자주 하는 오해: unbounded와 infeasible을 모두 '해가 없다'로 뭉뚱그리는 오류.

체크포인트 질문: 비유계 모델에서 현실적으로 빠졌을 가능성이 큰 제약은 무엇인가?

## DM_G1_P0001_Q07 - 오답 진단: ratio test

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.minimum_ratio_test`
- source anchor: `DM_PDF01:p001:L003`
- asset: `visual_assets/DM_G1_P0001_Q07__오답_진단:_ratio_test.png`

시각화 목적: 음수 계수를 절댓값으로 바꾸는 오답이 왜 pivot을 망치는지 비교한다.

사용할 데이터: positive coefficient row와 negative coefficient row의 ratio 처리 비교.

필요한 전처리: 잘못된 절댓값 계산과 올바른 후보 제외를 나란히 배치한다.

코드 셀 설계: wrong vs correct 막대/금지 표시를 만든다.

그래프 해석 포인트: 음수 계수는 entering variable을 늘릴 때 RHS 한계에 먼저 닿는 행이 아니므로 후보가 아니다.

학생이 자주 하는 오해: RHS 나눗셈이라는 형태만 보고 부호 의미를 무시하는 오류.

체크포인트 질문: entering variable을 늘릴 때 해당 행의 LHS는 증가하는가, 감소하는가?

## DM_G1_P0001_Q08 - Solver 매핑 문제

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.simplex_tableau`
- source anchor: `DM_PDF01:p001:L003`
- asset: `visual_assets/DM_G1_P0001_Q08__Solver_매핑_문제.png`

시각화 목적: LP 모형의 변수/목적/제약을 Excel Solver 셀 구조로 번역한다.

사용할 데이터: 문항의 x1,x2, objective, three constraints.

필요한 전처리: 수식 요소를 changing cells, target cell, constraint LHS/RHS로 분리한다.

코드 셀 설계: Solver layout infographic을 그린다.

그래프 해석 포인트: Solver는 changing cells를 움직여 target cell을 개선하되 constraint cells가 RHS를 넘지 않게 한다.

학생이 자주 하는 오해: RHS와 LHS를 한 셀에 섞거나 target cell을 변수 셀로 착각하는 오류.

체크포인트 질문: constraint LHS cell과 RHS cell은 왜 분리해야 하는가?

## DM_G1_P0001_Q09 - 특수 종료 신호 비교

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.optimality_test`, `n_DM_PDF01.multiple_optima`, `n_DM_PDF01.unbounded_solution`, `n_DM_PDF01.two_phase_method`
- source anchor: `DM_PDF01:p002:L003`, `DM_PDF01:p003:L003`, `DM_PDF01:p005:L001`
- asset: `visual_assets/DM_G1_P0001_Q09__특수_종료_신호_비교.png`

시각화 목적: 최적, 복수 최적, 비유계, infeasible을 종료 신호 흐름도로 구분한다.

사용할 데이터: 타블로 목적행, ratio candidate, Phase I objective 조건.

필요한 전처리: 판정 질문을 순서대로 배치한다.

코드 셀 설계: termination decision tree를 만든다.

그래프 해석 포인트: 종료 신호는 한 줄 문장 암기가 아니라 '개선 가능성, 대안 진입, ratio 후보, Phase I 값'의 조합이다.

학생이 자주 하는 오해: 복수 최적과 비유계, infeasible 신호를 reduced cost 하나로만 판정하는 오류.

체크포인트 질문: Phase I w*>0 신호는 왜 unbounded가 아니라 infeasible인가?

## DM_G1_P0001_Q10 - 최종 요약 문제

- 출처 노트북: `ipynb/DM_G1_P0001.ipynb`
- node_id: `n_DM_PDF01.simplex_tableau`
- source anchor: `DM_PDF01:p001:L003`
- asset: `visual_assets/DM_G1_P0001_Q10__최종_요약_문제.png`

시각화 목적: 현실 언어, 타블로 언어, Solver 언어가 같은 simplex 과정을 가리킴을 연결한다.

사용할 데이터: BFS, entering, leaving, ratio, pivot, reduced cost, unbounded 핵심어.

필요한 전처리: 세 언어를 삼각형 구조로 배치하고 중심에 simplex iteration을 둔다.

코드 셀 설계: three-language concept map을 만든다.

그래프 해석 포인트: 같은 절차를 자원 배분 이동, basis 교체, Solver 반복으로 번역할 수 있어야 한다.

학생이 자주 하는 오해: 용어를 따로 외우고 서로 번역하지 못하는 오류.

체크포인트 질문: BFS 이동을 현실 언어로 한 문장으로 말하면 무엇인가?

## DM_G1_P0002_Q01 - surplus/artificial variable 도입 판별

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.surplus_artificial_variable`
- source anchor: `DM_PDF01:p004:L003`
- asset: `visual_assets/DM_G1_P0002_Q01__surplus_artificial_variable_도입_판별.png`

시각화 목적: <=, >=, = 제약마다 어떤 변수가 필요한지 한눈에 구분한다.

사용할 데이터: 세 가지 제약 유형.

필요한 전처리: 부등호 방향을 등식화 규칙으로 변환한다.

코드 셀 설계: constraint-type conversion infographic을 그린다.

그래프 해석 포인트: <=에는 slack, >=에는 surplus 제거와 artificial 추가, =에는 basis 확보용 artificial이 필요하다.

학생이 자주 하는 오해: surplus를 slack처럼 더하거나 equality에 basis가 있다고 착각하는 오류.

체크포인트 질문: 왜 >= 제약에서는 surplus를 빼야 하는가?

## DM_G1_P0002_Q02 - 2단계법 문제 변형

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.two_phase_method`
- source anchor: `DM_PDF01:p004:L002`, `DM_PDF01:p005:L001`
- asset: `visual_assets/DM_G1_P0002_Q02__2단계법_문제_변형.png`

시각화 목적: Phase I에서 feasible basis를 만들고 Phase II에서 원목적함수로 돌아가는 절차를 보여준다.

사용할 데이터: slack/surplus/artificial이 섞인 LP.

필요한 전처리: 초기 basis 후보와 Phase I objective w를 분리한다.

코드 셀 설계: two-phase pipeline을 그린다.

그래프 해석 포인트: Phase I은 원문제 최적화가 아니라 artificial 합을 0으로 만들 수 있는지 검사하는 단계다.

학생이 자주 하는 오해: Phase I objective를 원목적함수 z와 혼동하는 오류.

체크포인트 질문: Phase II로 넘어가기 위한 정확한 조건은 무엇인가?

## DM_G1_P0002_Q03 - Phase I 목적함수 해석

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.two_phase_method`
- source anchor: `DM_PDF01:p006:L001`
- asset: `visual_assets/DM_G1_P0002_Q03__Phase_I_목적함수_해석.png`

시각화 목적: w=0이 원목적값이 아니라 feasibility 신호임을 분리한다.

사용할 데이터: Phase I objective w와 original objective z.

필요한 전처리: 두 개의 계기판을 분리해 표시한다.

코드 셀 설계: w gauge와 z gauge를 나란히 그린다.

그래프 해석 포인트: w=0은 원문제 feasible basis를 얻었다는 뜻이고, z 최적값은 Phase II에서 구한다.

학생이 자주 하는 오해: w=0을 z=0 또는 최적 목적값 0으로 착각하는 오류.

체크포인트 질문: w=0 이후에도 왜 Phase II가 필요한가?

## DM_G1_P0002_Q04 - artificial variable 최종해 판정

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.two_phase_method`, `n_DM_PDF05.artificial_variable`
- source anchor: `DM_PDF01:p006:L001`, `DM_PDF05:p007:L003`
- asset: `visual_assets/DM_G1_P0002_Q04__artificial_variable_최종해_판정.png`

시각화 목적: artificial이 0이면 feasible, 양수로 남으면 infeasible이라는 판정을 비교한다.

사용할 데이터: 상황 A: w*=0 artificial nonbasic, 상황 B: w*=3 artificial positive.

필요한 전처리: 두 상황을 side-by-side로 배치한다.

코드 셀 설계: feasible gate infographic을 만든다.

그래프 해석 포인트: artificial이 양수로 남으면 원 제약만으로는 그 점을 만들 수 없다.

학생이 자주 하는 오해: artificial variable을 실제 의사결정변수처럼 해석하는 오류.

체크포인트 질문: artificial positive가 의미하는 현실적 결핍은 무엇인가?

## DM_G1_P0002_Q05 - 식단문제 축소형

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.diet_two_phase`
- source anchor: `DM_PDF01:p007:L001`, `DM_PDF01:p008:L001`
- asset: `visual_assets/DM_G1_P0002_Q05__식단문제_축소형.png`

시각화 목적: 식품량 변수, 영양소 요구량 제약, 최소비용 objective를 행렬로 시각화한다.

사용할 데이터: 식품 3개, 비타민 A/C 함량표, 요구량.

필요한 전처리: nutrient matrix와 RHS requirement를 분리한다.

코드 셀 설계: matrix heatmap과 requirement bars를 그린다.

그래프 해석 포인트: 식단문제는 비용을 줄이면서 각 영양소의 최소 요구량 이상을 만족하는 >= 제약 문제다.

학생이 자주 하는 오해: 영양소 제약 방향을 <=로 쓰거나 비용 최소화를 최대화로 착각하는 오류.

체크포인트 질문: 각 식품량 xj는 무엇을 결정하는 변수인가?

## DM_G1_P0002_Q06 - Phase II 전환 구조

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.two_phase_method`
- source anchor: `DM_PDF01:p006:L001`, `DM_PDF01:p009:L001`
- asset: `visual_assets/DM_G1_P0002_Q06__Phase_II_전환_구조.png`

시각화 목적: Phase I basis를 유지하되 artificial 열을 제거하고 원목적함수로 전환하는 구조를 보여준다.

사용할 데이터: Phase I final tableau와 Phase II start basis.

필요한 전처리: artificial columns 제거와 original objective 복귀를 단계화한다.

코드 셀 설계: Phase I to Phase II transition flow를 그린다.

그래프 해석 포인트: Phase I이 찾아준 feasible basis는 Phase II의 출발점으로 재사용된다.

학생이 자주 하는 오해: Phase I이 끝나면 basis를 버리고 처음부터 다시 시작한다고 생각하는 오류.

체크포인트 질문: Phase II 시작 전 tableau에서 제거해야 하는 열은 무엇인가?

## DM_G1_P0002_Q07 - 오답 진단: surplus 부호

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.surplus_artificial_variable`
- source anchor: `DM_PDF01:p004:L003`
- asset: `visual_assets/DM_G1_P0002_Q07__오답_진단:_surplus_부호.png`

시각화 목적: >= 제약에서 surplus는 초과량이므로 빼야 한다는 부호 직관을 그림으로 보인다.

사용할 데이터: 2x1+x2 >= 10의 LHS와 RHS.

필요한 전처리: LHS = RHS + surplus를 LHS - surplus = RHS로 재배열한다.

코드 셀 설계: number-line/excess diagram을 만든다.

그래프 해석 포인트: surplus는 기준 RHS를 넘은 초과량이므로 좌변에서 빼야 등식이 된다.

학생이 자주 하는 오해: surplus를 slack처럼 더하는 오류.

체크포인트 질문: LHS가 RHS보다 3만큼 크면 surplus 값은 얼마이고 등식은 어떻게 되는가?

## DM_G1_P0002_Q08 - Solver 매핑 문제

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.diet_two_phase`
- source anchor: `DM_PDF01:p007:L001`
- asset: `visual_assets/DM_G1_P0002_Q08__Solver_매핑_문제.png`

시각화 목적: 식단형 최소화 문제를 Solver 셀 배치로 시각화한다.

사용할 데이터: 식품량 변수, 총비용, 영양소 섭취량 LHS, 요구량 RHS.

필요한 전처리: food amount cells, cost SUMPRODUCT, nutrient LHS cells를 분리한다.

코드 셀 설계: diet Solver layout infographic을 만든다.

그래프 해석 포인트: Solver에서는 >= constraint를 영양소 섭취량 셀 >= 요구량 셀로 입력한다.

학생이 자주 하는 오해: 수동 2단계법의 artificial 변수를 Solver changing cells에 넣는 오류.

체크포인트 질문: Solver의 changing cells에는 어떤 값들이 들어가야 하는가?

## DM_G1_P0002_Q09 - Phase I tableau 해석

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.two_phase_method`
- source anchor: `DM_PDF01:p006:L001`
- asset: `visual_assets/DM_G1_P0002_Q09__Phase_I_tableau_해석.png`

시각화 목적: Phase I 마지막 타블로가 말해주는 것과 아직 말해주지 않는 것을 분리한다.

사용할 데이터: objective value w=0, artificial variables nonbasic.

필요한 전처리: meaning / not-yet / next-action 세 칸으로 나눈다.

코드 셀 설계: Phase I interpretation board를 만든다.

그래프 해석 포인트: 이 상태는 feasibility 확보이지 original optimum 확보가 아니다.

학생이 자주 하는 오해: Phase I 마지막 값을 원문제 최적값으로 보고 멈추는 오류.

체크포인트 질문: 이 상태에서 다음 simplex tableau에는 어떤 objective row가 들어가야 하는가?

## DM_G1_P0002_Q10 - 최종 종합 문제

- 출처 노트북: `ipynb/DM_G1_P0002.ipynb`
- node_id: `n_DM_PDF01.surplus_artificial_variable`, `n_DM_PDF01.two_phase_method`
- source anchor: `DM_PDF01:p004:L003`, `DM_PDF01:p005:L001`, `DM_PDF01:p006:L001`
- asset: `visual_assets/DM_G1_P0002_Q10__최종_종합_문제.png`

시각화 목적: slack, surplus, artificial, Phase I/II의 관계를 개념 그래프로 묶는다.

사용할 데이터: 2단계법 핵심 용어 목록.

필요한 전처리: 변수 유형과 Phase 흐름을 방향 그래프로 배치한다.

코드 셀 설계: concept graph를 그린다.

그래프 해석 포인트: 표준형 변환은 basis 확보 문제로 이어지고, artificial이 0이 되는지가 feasibility 판정이다.

학생이 자주 하는 오해: 각 변수를 등식화 장치와 feasibility 장치로 구분하지 못하는 오류.

체크포인트 질문: slack과 artificial의 역할 차이를 한 문장으로 말하면?

## DM_G1_P0003_Q01 - min 문제를 Big-M용 max 형태로 바꾸기

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.big_m_method`, `n_DM_PDF05.artificial_variable`
- source anchor: `DM_PDF05:p002:L002`, `DM_PDF05:p003:L009`, `DM_PDF05:p003:L016`
- asset: `visual_assets/DM_G1_P0003_Q01__min_문제를_Big-M용_max_형태로_바꾸기.png`

시각화 목적: min-to-max 변환과 artificial penalty 부호를 같은 축에서 확인한다.

사용할 데이터: 최소화 목적함수, >= 제약, artificial variables.

필요한 전처리: min Z를 max -Z로 바꾸고 artificial이 커질수록 objective가 나빠지도록 표시한다.

코드 셀 설계: objective direction and penalty sign diagram을 만든다.

그래프 해석 포인트: Big-M 부호는 목적 방향에 따라 'artificial을 벌주는가'라는 현실 문장으로 확인한다.

학생이 자주 하는 오해: max 형태에서 artificial에 보상을 주는 부호를 쓰는 오류.

체크포인트 질문: artificial이 커질수록 max objective는 좋아져야 하는가, 나빠져야 하는가?

## DM_G1_P0003_Q02 - artificial variable 동치 조건

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.artificial_variable`, `n_DM_PDF05.big_m_method`
- source anchor: `DM_PDF05:p003:L015`, `DM_PDF05:p007:L003`
- asset: `visual_assets/DM_G1_P0003_Q02__artificial_variable_동치_조건.png`

시각화 목적: r=0일 때만 artificial 확장공간에서 원문제 공간으로 돌아온다는 점을 보여준다.

사용할 데이터: r1, r2 artificial variable 상태.

필요한 전처리: r 축을 원문제 평면 바깥 방향으로 표시한다.

코드 셀 설계: original plane vs artificial dimension diagram을 만든다.

그래프 해석 포인트: r>0은 원문제에 없는 보조축을 사용한 해이므로 원문제 feasible solution이 아니다.

학생이 자주 하는 오해: r>0이 작으면 괜찮다고 해석하는 오류.

체크포인트 질문: 왜 final artificial values must be zero인가?

## DM_G1_P0003_Q03 - Big-M과 2단계법 비교

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.big_m_method`, `n_DM_PDF01.two_phase_method`
- source anchor: `DM_PDF05:p004:L002`, `DM_PDF01:p005:L001`
- asset: `visual_assets/DM_G1_P0003_Q03__Big-M과_2단계법_비교.png`

시각화 목적: 두 방법이 같은 목적을 다른 절차로 수행함을 두 레인으로 비교한다.

사용할 데이터: Two-phase와 Big-M 알고리즘 단계.

필요한 전처리: 공통 목표와 차이점을 parallel lane flow로 정리한다.

코드 셀 설계: comparison flowchart를 만든다.

그래프 해석 포인트: 두 방법 모두 artificial을 0으로 만들려 하지만, 2단계법은 별도 Phase I이고 Big-M은 penalty를 넣는다.

학생이 자주 하는 오해: Big-M과 2단계법이 완전히 다른 문제를 푼다고 생각하는 오류.

체크포인트 질문: 두 방법의 공통 목표는 무엇인가?

## DM_G1_P0003_Q04 - Big-M 오답 진단

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.big_m_method`
- source anchor: `DM_PDF05:p003:L016`
- asset: `visual_assets/DM_G1_P0003_Q04__Big-M_오답_진단.png`

시각화 목적: +M이 artificial을 보상하는 부호가 될 때 왜 위험한지 시각화한다.

사용할 데이터: wrong reward vs correct penalty for artificial r.

필요한 전처리: r 값 증가에 따른 objective effect를 두 선으로 비교한다.

코드 셀 설계: penalty sign line plot을 만든다.

그래프 해석 포인트: max에서 artificial이 커질수록 objective가 좋아지는 식은 artificial 제거 목적과 반대다.

학생이 자주 하는 오해: M이 크면 부호가 어떻게 되든 알아서 빠진다고 생각하는 오류.

체크포인트 질문: M의 크기보다 먼저 확인해야 하는 것은 무엇인가?

## DM_G1_P0003_Q05 - 식단문제와 비타민 가격 쌍대 직관

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.dual_problem`
- source anchor: `DM_PDF05:p014:L001`, `DM_PDF05:p018:L001`, `DM_PDF05:p019:L001`
- asset: `visual_assets/DM_G1_P0003_Q05__식단문제와_비타민_가격_쌍대_직관.png`

시각화 목적: 식품량 primal과 영양소 가격 dual을 bipartite graph로 연결한다.

사용할 데이터: foods, nutrients, vitamin prices.

필요한 전처리: 식품-영양소 행렬을 그래프로 바꾼다.

코드 셀 설계: bipartite network를 그린다.

그래프 해석 포인트: primal 변수는 식품량, dual 변수는 영양소 요구량의 잠재가격으로 해석될 수 있다.

학생이 자주 하는 오해: dual variable을 항상 물리적 생산량으로 해석하는 오류.

체크포인트 질문: dual 변수는 원문제의 무엇에 대응하는가?

## DM_G1_P0003_Q06 - primal-dual 대응표 작성

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.dual_problem`, `n_DM_PDF05.primal_dual_mapping`
- source anchor: `DM_PDF05:p023:L002`
- asset: `visual_assets/DM_G1_P0003_Q06__primal-dual_대응표_작성.png`

시각화 목적: primal 제약은 dual 변수, primal 변수는 dual 제약으로 넘어가는 대응을 표로 시각화한다.

사용할 데이터: 4 constraints, 2 variables primal LP.

필요한 전처리: coefficient matrix transpose 관점으로 배열한다.

코드 셀 설계: matrix transposition heatmap을 만든다.

그래프 해석 포인트: primal constraint 수가 dual variable 수가 되고, primal variable 수가 dual constraint 수가 된다.

학생이 자주 하는 오해: dual variable 수를 primal variable 수와 같게 잡는 오류.

체크포인트 질문: dual에는 변수 y가 몇 개 필요한가?

## DM_G1_P0003_Q07 - 약쌍대성 판정

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.weak_duality`, `n_DM_PDF05.strong_duality`
- source anchor: `DM_PDF05:p024:L001`
- asset: `visual_assets/DM_G1_P0003_Q07__약쌍대성_판정.png`

시각화 목적: max primal feasible value가 min dual feasible value를 넘지 못한다는 bound 구조를 숫자선으로 보여준다.

사용할 데이터: Z=700, W=1540.

필요한 전처리: number line에 primal lower bound와 dual upper bound를 배치한다.

코드 셀 설계: duality gap number line을 만든다.

그래프 해석 포인트: Z<=W이면 weak duality와 일치하며, Z=W이면 optimality certificate가 된다.

학생이 자주 하는 오해: Z<W이면 둘 중 하나가 infeasible이라고 판정하는 오류.

체크포인트 질문: Z=W가 되면 왜 양쪽 최적해라고 말할 수 있는가?

## DM_G1_P0003_Q08 - 강쌍대성과 최적성

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.weak_duality`, `n_DM_PDF05.strong_duality`, `n_DM_PDF05.four_duality_cases`
- source anchor: `DM_PDF05:p024:L001`, `DM_PDF05:p025:L001`
- asset: `visual_assets/DM_G1_P0003_Q08__강쌍대성과_최적성.png`

시각화 목적: weak duality, strong duality, 4 cases를 최적성 판정 지도에 배치한다.

사용할 데이터: A/B/C 문장 유형.

필요한 전처리: feasible/bounded 상태와 objective equality를 판정 순서로 둔다.

코드 셀 설계: duality case map을 만든다.

그래프 해석 포인트: strong duality는 feasible optimum pair의 objective equality이고, unbounded는 반대쪽 infeasible 가능성과 연결된다.

학생이 자주 하는 오해: weak duality의 부등식만 보고 최적성을 곧바로 결론내는 오류.

체크포인트 질문: 최적성 certificate로 쓰려면 무엇이 같아야 하는가?

## DM_G1_P0003_Q09 - 상보여유 기초 판정

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.complementary_slackness`, `n_DM_PDF02.shadow_price`
- source anchor: `DM_PDF05:p027:L001`, `DM_PDF05:p030:L002`
- asset: `visual_assets/DM_G1_P0003_Q09__상보여유_기초_판정.png`

시각화 목적: slack>0과 positive dual variable이 동시에 있으면 상보여유를 위반함을 보인다.

사용할 데이터: constraint 2 slack=40, y2=3.

필요한 전처리: slack*y=0 조건을 곱셈 막대로 표시한다.

코드 셀 설계: complementary slackness violation chart를 만든다.

그래프 해석 포인트: 여유가 있는 자원은 추가 가치가 0이어야 하므로 대응 dual variable은 0이어야 한다.

학생이 자주 하는 오해: binding constraint와 positive shadow price의 방향을 거꾸로 이해하는 오류.

체크포인트 질문: slack=40이면 y2는 어떤 값이어야 하는가?

## DM_G1_P0003_Q10 - reduced cost와 shadow price 연결

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF02.reduced_cost`, `n_DM_PDF02.shadow_price`
- source anchor: `DM_PDF05:p032:L002`
- asset: `visual_assets/DM_G1_P0003_Q10__reduced_cost와_shadow_price_연결.png`

시각화 목적: 변수 질문은 reduced cost, RHS/자원 질문은 shadow price로 갈라진다는 점을 지도화한다.

사용할 데이터: variable-entry question and RHS-value question.

필요한 전처리: 질문 유형을 두 갈래로 분류한다.

코드 셀 설계: question routing flow를 만든다.

그래프 해석 포인트: reduced cost는 변수/활동의 진입 조건이고 shadow price는 제약 RHS 변화의 가치다.

학생이 자주 하는 오해: 둘을 모두 '한계값'으로만 보고 같은 값처럼 해석하는 오류.

체크포인트 질문: 새 활동을 시작하려면 어떤 열을 봐야 하는가?

## DM_G1_P0003_Q11 - sensitivity report 브릿지 판별

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF02.reduced_cost`, `n_DM_PDF02.shadow_price`, `n_DM_PDF05.shadow_price_dual_solution`
- source anchor: `DM_PDF05:p032:L002`, `DM_PDF02:p026:L007`, `DM_PDF02:p026:L009`
- asset: `visual_assets/DM_G1_P0003_Q11__sensitivity_report_브릿지_판별.png`

시각화 목적: A~D 질문을 sensitivity report의 열로 라우팅한다.

사용할 데이터: reduced cost, shadow price, allowable range 질문 유형.

필요한 전처리: 질문을 변수/제약/RHS/범위로 분류한다.

코드 셀 설계: sensitivity routing board를 만든다.

그래프 해석 포인트: sensitivity report는 최종 타블로와 duality 해석을 Solver 출력 형태로 보여준다.

학생이 자주 하는 오해: allowable range를 shadow price 자체와 혼동하는 오류.

체크포인트 질문: shadow price를 적용하기 전에 반드시 확인해야 하는 범위는 무엇인가?

## DM_G1_P0003_Q12 - 최종 종합 문제

- 출처 노트북: `ipynb/DM_G1_P0003.ipynb`
- node_id: `n_DM_PDF05.artificial_variable`, `n_DM_PDF05.big_m_method`, `n_DM_PDF05.dual_problem`, `n_DM_PDF05.complementary_slackness`, `n_DM_PDF02.shadow_price`
- source anchor: `DM_PDF05:p003:L009`, `DM_PDF05:p023:L002`, `DM_PDF05:p024:L001`, `DM_PDF05:p027:L001`, `DM_PDF05:p032:L002`
- asset: `visual_assets/DM_G1_P0003_Q12__최종_종합_문제.png`

시각화 목적: artificial variable에서 sensitivity report까지 이어지는 전체 개념 사슬을 하나의 지도에 담는다.

사용할 데이터: P0003 핵심 노드 chain.

필요한 전처리: 개념 노드를 순서 그래프로 배치하고 각 edge의 의미를 표시한다.

코드 셀 설계: final concept graph를 만든다.

그래프 해석 포인트: Big-M은 artificial 제거, duality는 제약의 가격 해석, sensitivity는 최적해 이후 변화 해석으로 이어진다.

학생이 자주 하는 오해: Big-M, duality, sensitivity를 별개 암기 단원으로 분리하는 오류.

체크포인트 질문: 왜 Big-M 이후 duality를 배우면 sensitivity report 해석이 쉬워지는가?
