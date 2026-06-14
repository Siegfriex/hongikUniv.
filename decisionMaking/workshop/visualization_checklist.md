# DecisionMaking G1 Visualization Checklist

## 생성 검증

- [ ] `python visualization_cells.py`가 32개 PNG와 manifest를 생성한다.
- [ ] `DM_G1_visual_lecture.ipynb`가 열리며 각 문항 이미지가 표시된다.
- [ ] 문제 노트북 원본은 수정하지 않는다.
- [ ] 외부 다운로드 없이 실행된다.
- [ ] 각 문항은 node_id와 source anchor를 유지한다.

## 문항별 체크

| Block | Asset | 2D/diagram | 핵심 판정 질문 |
| --- | --- | --- | --- |
| `DM_G1_P0001_Q01` | `visual_assets/DM_G1_P0001_Q01__표준형_변환_기본.png` | yes | 초기 BFS에서 x1=x2=0일 때 각 slack 값은 무엇인가? |
| `DM_G1_P0001_Q02` | `visual_assets/DM_G1_P0001_Q02__첫_pivot_선택.png` | yes | 왜 ratio test는 양수 계수 행만 후보로 보는가? |
| `DM_G1_P0001_Q03` | `visual_assets/DM_G1_P0001_Q03__피벗_연산_구조_설명.png` | yes | 첫 pivot 뒤 basis에는 어떤 변수가 들어오고 어떤 slack이 나가는가? |
| `DM_G1_P0001_Q04` | `visual_assets/DM_G1_P0001_Q04__타블로_판정_문제.png` | yes | x3의 reduced cost가 0이라는 말은 objective value 관점에서 무슨 뜻인가? |
| `DM_G1_P0001_Q05` | `visual_assets/DM_G1_P0001_Q05__복수_최적해_예제_변형.png` | yes | 대안 최적해를 찾으려면 어떤 reduced cost 조건을 봐야 하는가? |
| `DM_G1_P0001_Q06` | `visual_assets/DM_G1_P0001_Q06__비유계_판정.png` | yes | 비유계 모델에서 현실적으로 빠졌을 가능성이 큰 제약은 무엇인가? |
| `DM_G1_P0001_Q07` | `visual_assets/DM_G1_P0001_Q07__오답_진단:_ratio_test.png` | yes | entering variable을 늘릴 때 해당 행의 LHS는 증가하는가, 감소하는가? |
| `DM_G1_P0001_Q08` | `visual_assets/DM_G1_P0001_Q08__Solver_매핑_문제.png` | yes | constraint LHS cell과 RHS cell은 왜 분리해야 하는가? |
| `DM_G1_P0001_Q09` | `visual_assets/DM_G1_P0001_Q09__특수_종료_신호_비교.png` | yes | Phase I w*>0 신호는 왜 unbounded가 아니라 infeasible인가? |
| `DM_G1_P0001_Q10` | `visual_assets/DM_G1_P0001_Q10__최종_요약_문제.png` | yes | BFS 이동을 현실 언어로 한 문장으로 말하면 무엇인가? |
| `DM_G1_P0002_Q01` | `visual_assets/DM_G1_P0002_Q01__surplus_artificial_variable_도입_판별.png` | yes | 왜 >= 제약에서는 surplus를 빼야 하는가? |
| `DM_G1_P0002_Q02` | `visual_assets/DM_G1_P0002_Q02__2단계법_문제_변형.png` | yes | Phase II로 넘어가기 위한 정확한 조건은 무엇인가? |
| `DM_G1_P0002_Q03` | `visual_assets/DM_G1_P0002_Q03__Phase_I_목적함수_해석.png` | yes | w=0 이후에도 왜 Phase II가 필요한가? |
| `DM_G1_P0002_Q04` | `visual_assets/DM_G1_P0002_Q04__artificial_variable_최종해_판정.png` | yes | artificial positive가 의미하는 현실적 결핍은 무엇인가? |
| `DM_G1_P0002_Q05` | `visual_assets/DM_G1_P0002_Q05__식단문제_축소형.png` | yes | 각 식품량 xj는 무엇을 결정하는 변수인가? |
| `DM_G1_P0002_Q06` | `visual_assets/DM_G1_P0002_Q06__Phase_II_전환_구조.png` | yes | Phase II 시작 전 tableau에서 제거해야 하는 열은 무엇인가? |
| `DM_G1_P0002_Q07` | `visual_assets/DM_G1_P0002_Q07__오답_진단:_surplus_부호.png` | yes | LHS가 RHS보다 3만큼 크면 surplus 값은 얼마이고 등식은 어떻게 되는가? |
| `DM_G1_P0002_Q08` | `visual_assets/DM_G1_P0002_Q08__Solver_매핑_문제.png` | yes | Solver의 changing cells에는 어떤 값들이 들어가야 하는가? |
| `DM_G1_P0002_Q09` | `visual_assets/DM_G1_P0002_Q09__Phase_I_tableau_해석.png` | yes | 이 상태에서 다음 simplex tableau에는 어떤 objective row가 들어가야 하는가? |
| `DM_G1_P0002_Q10` | `visual_assets/DM_G1_P0002_Q10__최종_종합_문제.png` | yes | slack과 artificial의 역할 차이를 한 문장으로 말하면? |
| `DM_G1_P0003_Q01` | `visual_assets/DM_G1_P0003_Q01__min_문제를_Big-M용_max_형태로_바꾸기.png` | yes | artificial이 커질수록 max objective는 좋아져야 하는가, 나빠져야 하는가? |
| `DM_G1_P0003_Q02` | `visual_assets/DM_G1_P0003_Q02__artificial_variable_동치_조건.png` | yes | 왜 final artificial values must be zero인가? |
| `DM_G1_P0003_Q03` | `visual_assets/DM_G1_P0003_Q03__Big-M과_2단계법_비교.png` | yes | 두 방법의 공통 목표는 무엇인가? |
| `DM_G1_P0003_Q04` | `visual_assets/DM_G1_P0003_Q04__Big-M_오답_진단.png` | yes | M의 크기보다 먼저 확인해야 하는 것은 무엇인가? |
| `DM_G1_P0003_Q05` | `visual_assets/DM_G1_P0003_Q05__식단문제와_비타민_가격_쌍대_직관.png` | yes | dual 변수는 원문제의 무엇에 대응하는가? |
| `DM_G1_P0003_Q06` | `visual_assets/DM_G1_P0003_Q06__primal-dual_대응표_작성.png` | yes | dual에는 변수 y가 몇 개 필요한가? |
| `DM_G1_P0003_Q07` | `visual_assets/DM_G1_P0003_Q07__약쌍대성_판정.png` | yes | Z=W가 되면 왜 양쪽 최적해라고 말할 수 있는가? |
| `DM_G1_P0003_Q08` | `visual_assets/DM_G1_P0003_Q08__강쌍대성과_최적성.png` | yes | 최적성 certificate로 쓰려면 무엇이 같아야 하는가? |
| `DM_G1_P0003_Q09` | `visual_assets/DM_G1_P0003_Q09__상보여유_기초_판정.png` | yes | slack=40이면 y2는 어떤 값이어야 하는가? |
| `DM_G1_P0003_Q10` | `visual_assets/DM_G1_P0003_Q10__reduced_cost와_shadow_price_연결.png` | yes | 새 활동을 시작하려면 어떤 열을 봐야 하는가? |
| `DM_G1_P0003_Q11` | `visual_assets/DM_G1_P0003_Q11__sensitivity_report_브릿지_판별.png` | yes | shadow price를 적용하기 전에 반드시 확인해야 하는 범위는 무엇인가? |
| `DM_G1_P0003_Q12` | `visual_assets/DM_G1_P0003_Q12__최종_종합_문제.png` | yes | 왜 Big-M 이후 duality를 배우면 sensitivity report 해석이 쉬워지는가? |
