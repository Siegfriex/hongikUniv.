# 00. DecisionMaking 전체 학습 로드맵

이 문서는 `decisionMaking/rag_applied_flat_pack`의 전체 학습 순서를 잡는 최상위 로드맵이다.

사용 순서:

1. 먼저 이 로드맵으로 Phase와 목표를 정한다.
2. 해당 Phase의 관련 PDF `DM_PDFxx__04_rag.md`를 우선 조회한다.
3. 필요하면 `__03_concept_node_index.md`, `__02_rawdata_develop.md`, `__01_pdf_transcript.md`로 내려가 근거를 확인한다.
4. 문제 노트북 생성 시 이 표의 Phase 번호를 `Gate/Phase` 기준으로 사용한다.

| Phase | 관련 PDF | 목표 | 세부 태스크 | 통과 기준 |
| --- | --- | --- | --- | --- |
| 0. 모델링 문법 장착 | 전체 공통 | 모든 문제를 변수, 목적함수, 제약식, domain, Solver 셀로 번역 | decision variable / target cell / changing cells / constraint LHS-RHS / continuous-int-bin 구분 템플릿 만들기 | 새 문제를 보면 “무엇을 결정하고, 무엇을 최적화하고, 무엇이 제한인가”를 말할 수 있음 |
| 1. Ch.4 심플렉스 타블로 | DM_PDF01 | LP의 꼭짓점 이동을 tableau로 이해 | 표준형 변환, slack 변수, 초기 BFS, entering/leaving variable, minimum ratio test, pivot, optimality test | 타블로에서 다음 pivot을 직접 고르고, 최적/복수최적/비유계를 판별 |
| 2. 2단계법과 artificial variable | DM_PDF01 | 초기 기저가능해가 없을 때 출발점 만드는 법 이해 | surplus/artificial variable 도입, Phase I에서 artificial 합 최소화, Phase II로 원 목적함수 복귀 | artificial variable이 최종해에서 0이어야 하는 이유 설명 |
| 3. Big-M + 쌍대성 연결 | DM_PDF05 | 2단계법과 Big-M, primal-dual 사고 연결 | min->max 변환, Big-M penalty 부호, artificial variable 제거, primal-dual mapping, weak/strong duality, complementary slackness | Big-M 부호 오류 없이 식 세우고, primal 제약 <-> dual 변수 대응 가능 |
| 4. Ch.5 민감도 분석 | DM_PDF02 | 최적해 이후 “값이 바뀌면 어떻게 되는가” 해석 | binding/nonbinding, reduced cost, shadow price, allowable increase/decrease, Solver sensitivity report | shadow price를 허용범위 안에서만 적용하고, reduced cost와 shadow price를 구분 |
| 5. Ch.5 수송·네트워크 | DM_PDF06 | LP를 행렬/노드/arc/flow balance 구조로 재해석 | transportation, unbalanced/dummy, assignment, transshipment, minimum cost flow, SUMPRODUCT, SUMIF node balance | 행합/열합 제약과 node balance 제약을 구분하고 Solver 셀 구조 작성 |
| 6. Ch.6 정수계획 1주차 | DM_PDF04 | domain이 continuous가 아니라 int/bin일 때 모델이 어떻게 바뀌는지 이해 | pure/mixed/binary IP, knapsack, capital budgeting, policy logic, fixed-charge, either-or, `x <= M y` | 0-1 선택변수와 연속 생산량 변수를 분리하고, LP relaxation 반올림 금지 설명 |
| 7. 분지한계법 | DM_PDF03 | 정수계획을 exact하게 푸는 탐색 알고리즘 이해 | LP relaxation, upper/lower bound, incumbent, floor/ceil branching, pruning, tree 작성 | 왜 특정 노드를 절단해도 최적성을 잃지 않는지 증명 |
| 8. Ch.6 정수계획 2주차 | DM_PDF08 | 0-1 응용모형: facility location, set covering | coverage matrix, set covering/partitioning/packing, max coverage 변형, 중복계산 오답 진단 | `Ax >= 1`, `Ax = 1`, `Ax <= 1`의 의미 차이와 x/y 변수 분리 |
| 9. Ch.7 비선형계획 | DM_PDF07 | 선형이 아닌 목적/제약에서 Solver 해석이 왜 조심스러운지 이해 | nonlinear objective/constraint, GRG, local/global optimum, initial solution, convexity/concavity, KKT | GRG 해를 전체최적해로 단정하지 않고, KKT 필요조건과 전체최적 충분조건 구분 |
| 10. 통합 실전 | 전체 | 새 문제를 유형 판별부터 해석까지 독립 수행 | LP/IP/network/NLP 섞은 문제 분류, Solver 설정, 결과 해석, 오답노트 작성 | 문제 유형 판별 -> 모형화 -> Solver -> 해석 -> 민감도/오답검증까지 완주 |

## IPYNB 생성용 Phase 매핑

문제 노트북 생성 시 권장 파일명:

| Roadmap Phase | 권장 notebook id | 예시 파일명 |
| --- | --- | --- |
| Phase 0 | `DM_G0_P0001` | `DM_G0_P0001.ipynb`, `DM_G0_P0001_answer.ipynb` |
| Phase 1 | `DM_G1_P0001` | `DM_G1_P0001.ipynb`, `DM_G1_P0001_answer.ipynb` |
| Phase 2 | `DM_G1_P0002` | `DM_G1_P0002.ipynb`, `DM_G1_P0002_answer.ipynb` |
| Phase 3 | `DM_G1_P0003` | `DM_G1_P0003.ipynb`, `DM_G1_P0003_answer.ipynb` |
| Phase 4 | `DM_G2_P0001` | `DM_G2_P0001.ipynb`, `DM_G2_P0001_answer.ipynb` |
| Phase 5 | `DM_G3_P0001` | `DM_G3_P0001.ipynb`, `DM_G3_P0001_answer.ipynb` |
| Phase 6 | `DM_G4_P0001` | `DM_G4_P0001.ipynb`, `DM_G4_P0001_answer.ipynb` |
| Phase 7 | `DM_G4_P0002` | `DM_G4_P0002.ipynb`, `DM_G4_P0002_answer.ipynb` |
| Phase 8 | `DM_G4_P0003` | `DM_G4_P0003.ipynb`, `DM_G4_P0003_answer.ipynb` |
| Phase 9 | `DM_G5_P0001` | `DM_G5_P0001.ipynb`, `DM_G5_P0001_answer.ipynb` |
| Phase 10 | `DM_GX_P0001` | `DM_GX_P0001.ipynb`, `DM_GX_P0001_answer.ipynb` |

운영 기준: Phase 1~3은 모두 G1로 묶고, `DM_G1_P0003`은 Big-M에서 duality/sensitivity로 넘어가는 G1->G2 브릿지로 취급한다.
