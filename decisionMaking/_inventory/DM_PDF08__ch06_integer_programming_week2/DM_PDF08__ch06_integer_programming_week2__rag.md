# DM_PDF08 — Ch.6 정수계획 2주차: 0-1 응용 모형 최종 RAG 튜터 운영문서

## 0. Document Contract

- **문서 성격:** PDF 요약본이 아니라, 전담 1:1 경영과학 튜터와 RAG agent가 함께 쓰는 증거 기반 운영문서다.
- **source_id:** `DM_PDF08`
- **normalized_pdf:** `decisionMaking/pdf_sources/DM_PDF08_ch06_integer_programming_week2.pdf`
- **primary transcript:** `decisionMaking/pdf_transcripts/DM_PDF08__ch06_integer_programming_week2__full_transcript.md`
- **sidecar:** `decisionMaking/_inventory/DM_PDF08__ch06_integer_programming_week2`
- **flat-pack target:** `decisionMaking/rag_applied_flat_pack/DM_PDF08__04_rag.md`
- **source priority:** 1) PDF 전사본 anchor, 2) 이 문서의 enhanced sidecar, 3) 웹 그라운딩, 4) 일반 OR/MS 지식.
- **중요한 명명 주의:** `DM_PDF08`는 PDF intake index다. 강의 회차/장 번호와 혼동하지 않는다.

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
| p001 | `DM_PDF08:p001:L002, DM_PDF08:p001:L003` | 6.8 공공 설비 입지 선정 모형 / • 공공설비: 소방소, 파출소, 응급의료설비(병원), 학교 등 / • 모든 지역이 혜택 받되 공공설비 설치 수는 최소화 | ok |
| p002 | `DM_PDF08:p002:L002, DM_PDF08:p002:L003` |  모형화 가이드 / ① 후보지역에 공공설비 설치 여부  변수셀 (0-1 변수) / X=(x1,x2,…,x8) | ok |
| p003 | `DM_PDF08:p003:L002, DM_PDF08:p003:L003` | 후보지에서 10분 이내 도달 가능성: 0/1행렬 / 변수셀 / 행정구역 1 2 3 4 5 6 7 8 | ok |
| p004 | `DM_PDF08:p004:L002, DM_PDF08:p004:L003` | 수학적 모형 / 1. 의사결정변수 / xj = 후보지역 j에 응급차량 설치여부 0-1 변수, (j=1,…,8) | ok |
| p005 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p006 | `DM_PDF08:p006:L002, DM_PDF08:p006:L003` |  모형화 가이드(참고) / ④ 모든 행정구역은 적어도 하나 이상의 응급차량 설치 / 지역으로부터 10분내에 도달되어야 함 | ok |
| p007 | `DM_PDF08:p007:L001, DM_PDF08:p007:L002` | 7일반 모형(참고) / x=(x1,…,xn) 변수 벡터 / xj = 지역 j에 입지선정 0-1 변수, (j=1,…,n) | ok |
| p008 | `DM_PDF08:p008:L002, DM_PDF08:p008:L003` | – 해찾기 실행 / – 체크 포인트 / • 공공설비 입지선정 모형에는 복수 최적해가 자주 발생함. | ok |
| p009 | `DM_PDF08:p009:L002, DM_PDF08:p009:L003` | 공공 설비 입지 선정 모형 – 앞의 문제 변형 / (연습문제 19번) /  서비스를 받을 수 있는 주민 수가 | ok |
| p010 | `DM_PDF08:p010:L002, DM_PDF08:p010:L003` | 19번 문제: 수학적 모형 / 1. 의사결정변수 / xj = 후보지역 j에 응급차량 설치여부 0-1 변수, (j=1,…,8) | ok |
| p011 | `DM_PDF08:p011:L002, DM_PDF08:p011:L003` | 범하기 쉬운 잘못된 모형화 / xj = 후보지역 j에 응급차량 설치여부 0-1 변수, (j=1,…,8) / Maximize 5.4 (x1+ x4 ) + 4.2 (x1+ x2+ x4 ) | ok |
| p012 | `DM_PDF08:p012:L002, DM_PDF08:p012:L003` | 변형 모형의 스프레드시트 / 0/1 변수 / Covering수는 2이상 나올 수 있음 | LOW_TEXT |
| p013 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p014 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p015 | `DM_PDF08:p015:L001, DM_PDF08:p015:L002` | 15분지한계법 적용(순수/혼합 정수계획) / 예제 6.9 | LOW_TEXT |
| p016 | `DM_PDF08:p016:L001, DM_PDF08:p016:L002` | 16분지한계법 적용과정2 / 다음은 Z 값이 큰 / 부문제부터 적용 | LOW_TEXT |
| p017 | `DM_PDF08:p017:L002` | 절단 | LOW_TEXT |
| p018 | `DM_PDF08:p018:L002, DM_PDF08:p018:L003` | ㅁ / 비교(1) / 비교(2) | LOW_TEXT |
| p019 | `DM_PDF08:p019:L002, DM_PDF08:p019:L003` | 절단 / L=48 bound | LOW_TEXT |
| p020 | `DM_PDF08:p020:L002, DM_PDF08:p020:L003` | L=48 / Z<L 절단 | LOW_TEXT |
| p021 | `DM_PDF08:p021:L002, DM_PDF08:p021:L003` | 최적해 / L=48 / Z<L 절단 | LOW_TEXT |
| p022 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p023 | `-` | 텍스트 추출 부족. 원본 PDF/OCR 대조 필요. | LOW_TEXT |
| p024 | `DM_PDF08:p024:L002, DM_PDF08:p024:L003` | 실습 1번 / ** 클래스넷에 올려 놓은 실습문제1번(Week2).hwp / 파일보고 문제를 풀것 | ok |
| p025 | `DM_PDF08:p025:L001, DM_PDF08:p025:L002` | 다음을 분지한계법 (Branch and Bound)을 적용하여 구하라. / *반드시 계산과정을 p.23처럼 tree로 나타내고 최적해를 표시할 것. / (클래스넷 “분지한계법.hwp” 참고, 계산 과정 시 엑셀 사용). | ok |

## 2. Chapter Thesis

0-1 정수계획은 선택 여부를 변수로 두고, cover/partition/pack 같은 행렬 제약으로 공공설비 입지와 혜택 최대화 문제를 모델링한다.

## 3. Current Graph Position

- **현재 그래프 위치:** binary variable -> coverage matrix A -> set covering/partitioning/packing -> facility location variants -> branch-and-bound solution trace.
- **지금 보는 노드:** `DM_PDF08` / Ch.6 정수계획 2주차: 0-1 응용 모형
- **튜터 운영 원칙:** 질문이 들어오면 먼저 노드로 매핑하고, 예제 카드와 수식/Solver 구조를 거쳐 Source Trace Table의 evidence anchor로 되돌아간다.

## 4. Learning Outcomes

- 공공설비 입지 선정 문제를 set covering Ax>=1로 정식화한다.
- set covering, set partitioning, set packing의 부등호 차이를 구분한다.
- 혜택 최대화 변형에서 x_j 설치변수와 y_i 혜택변수를 분리한다.

## 5. Concept Graph Map

| node_id | 개념 | 역할 | 선행 노드 | 후속 노드 |
| --- | --- | --- | --- | --- |
| `n_DM_PDF08.facility_location_set_cover` | 공공설비 입지 선정 | 모든 수요지역이 일정 시간/거리 안에서 서비스되도록 최소 개수의 시설 위치를 고르는 0-1 모형이다. | binary variable | set covering |
| `n_DM_PDF08.coverage_matrix` | 커버리지 행렬 | A_ij=1이면 후보지 j가 구역 i를 커버하고, 0이면 커버하지 않는 0/1 입력 행렬이다. | facility_location_set_cover | set_partitioning_packing |
| `n_DM_PDF08.binary_open_variable` | 0-1 설치변수 | 후보지에 시설을 설치하면 1, 아니면 0인 선택 변수다. | integer programming | branch and bound |
| `n_DM_PDF08.set_covering_partitioning_packing` | covering/partitioning/packing | Ax>=1은 최소 하나 이상 커버, Ax=1은 정확히 하나, Ax<=1은 겹치지 않게 선택하는 0-1 집합 모형이다. | coverage_matrix | assignment/set partitioning |
| `n_DM_PDF08.benefit_max_variant` | 혜택 최대화 변형 | 설치 수가 제한된 상황에서 혜택 받는 주민 수를 최대화하도록 시설 위치와 구역 혜택 여부를 함께 결정하는 변형 모형이다. | set covering | wrong_model_diagnosis |
| `n_DM_PDF08.wrong_model_diagnosis` | 잘못된 모형화 진단 | coverage 수를 그대로 주민수에 곱해 중복 혜택을 여러 번 계산하는 오류를 식별하는 진단 노드다. | benefit_max_variant | binary logic constraints |
| `n_DM_PDF08.multiple_optima_facility` | 입지모형 복수 최적 | 같은 설치 수로 전 지역을 커버하는 후보 조합이 여러 개 나올 수 있는 현상이다. | set_covering | sensitivity/robustness |
| `n_DM_PDF08.branch_bound_review` | 분지한계법 복습 | 0-1 입지모형 같은 정수계획을 풀기 위해 branch-and-bound 과정을 적용하는 후반 복습 노드다. | DM_PDF03 branch_and_bound | MIP solver |

### Edge List

| from | edge_type | to |
| --- | --- | --- |
| `binary variable` | 선행 관계 | `n_DM_PDF08.facility_location_set_cover` |
| `n_DM_PDF08.facility_location_set_cover` | 후속 관계 | `set covering` |
| `n_DM_PDF08.facility_location_set_cover` | 동형/유사 | `facility location` |
| `facility_location_set_cover` | 선행 관계 | `n_DM_PDF08.coverage_matrix` |
| `n_DM_PDF08.coverage_matrix` | 후속 관계 | `set_partitioning_packing` |
| `n_DM_PDF08.coverage_matrix` | 동형/유사 | `incidence matrix` |
| `integer programming` | 선행 관계 | `n_DM_PDF08.binary_open_variable` |
| `n_DM_PDF08.binary_open_variable` | 후속 관계 | `branch and bound` |
| `n_DM_PDF08.binary_open_variable` | 동형/유사 | `fixed-charge y variables` |
| `coverage_matrix` | 선행 관계 | `n_DM_PDF08.set_covering_partitioning_packing` |
| `n_DM_PDF08.set_covering_partitioning_packing` | 후속 관계 | `assignment/set partitioning` |
| `n_DM_PDF08.set_covering_partitioning_packing` | 동형/유사 | `combinatorial optimization` |
| `set covering` | 선행 관계 | `n_DM_PDF08.benefit_max_variant` |
| `n_DM_PDF08.benefit_max_variant` | 후속 관계 | `wrong_model_diagnosis` |
| `n_DM_PDF08.benefit_max_variant` | 동형/유사 | `max coverage problem` |
| `benefit_max_variant` | 선행 관계 | `n_DM_PDF08.wrong_model_diagnosis` |
| `n_DM_PDF08.wrong_model_diagnosis` | 후속 관계 | `binary logic constraints` |
| `n_DM_PDF08.wrong_model_diagnosis` | 동형/유사 | `indicator variable` |
| `set_covering` | 선행 관계 | `n_DM_PDF08.multiple_optima_facility` |
| `n_DM_PDF08.multiple_optima_facility` | 후속 관계 | `sensitivity/robustness` |
| `n_DM_PDF08.multiple_optima_facility` | 동형/유사 | `alternate optimum` |
| `DM_PDF03 branch_and_bound` | 선행 관계 | `n_DM_PDF08.branch_bound_review` |
| `n_DM_PDF08.branch_bound_review` | 후속 관계 | `MIP solver` |
| `n_DM_PDF08.branch_bound_review` | 동형/유사 | `tree search` |

## 6. Core Concept Node Cards

### n_DM_PDF08.facility_location_set_cover — 공공설비 입지 선정 (facility location set covering)

1. **한 줄 정의:** 모든 수요지역이 일정 시간/거리 안에서 서비스되도록 최소 개수의 시설 위치를 고르는 0-1 모형이다.
2. **쉬운 직관:** 모두가 혜택을 받게 하되 설치 수를 최대한 줄인다.
3. **언제 쓰는가:** 소방서, 응급차량, 학교, 병원 후보지 선택에 쓴다.
4. **변수 정의:** x_j=후보지역 j에 시설 설치 여부.
5. **목적함수:** min sum x_j.
6. **제약식:** 각 행정구역 i에 대해 sum_j A_ij x_j >=1.
7. **수식의 현실 의미:** 13개 행정구역이 10분 내 응급서비스를 받을 수 있게 한다.
8. **그래프/네트워크 관점:** coverage bipartite graph.
9. **스프레드시트/Solver 관점:** Solver binary variables with coverage rows.
10. **강의 예제 연결:** 신도시 B 응급 의료 서비스.
11. **예제 숫자 해석:** 후보지 8곳, 행정구역 13개.
12. **자주 하는 실수:** 목적을 거리 최소화로 바꿔 버리는 오류.
13. **선행 노드:** binary variable
14. **후속 노드:** set covering
15. **동형/유사 노드:** facility location
16. **시험 출제 포인트:** Ax>=1 정식화.
17. **RAG retrieval tags:** `facility_location`, `set_cover`
18. **Evidence anchors:** `ev_deep_DM_PDF08_node_facility_location_set_cover` -> `DM_PDF08:p001:L002` / source_id=`DM_PDF08`, page=`p001`, block=`p001-L002`, line=`L002`

> 근거 excerpt: 6.8 공공 설비 입지 선정 모형

### n_DM_PDF08.coverage_matrix — 커버리지 행렬 (coverage matrix)

1. **한 줄 정의:** A_ij=1이면 후보지 j가 구역 i를 커버하고, 0이면 커버하지 않는 0/1 입력 행렬이다.
2. **쉬운 직관:** 지도 위 도달 가능성을 수학 표로 바꾼 것이다.
3. **언제 쓰는가:** covering 제약을 만들 때 쓴다.
4. **변수 정의:** A matrix 13x8 and x vector.
5. **목적함수:** objective independent of A except constraints.
6. **제약식:** A x >= 1 or variants.
7. **수식의 현실 의미:** 10분 이내 도달 가능성을 행렬로 입력한다.
8. **그래프/네트워크 관점:** bipartite incidence matrix.
9. **스프레드시트/Solver 관점:** Spreadsheet에서 A matrix와 x vector의 row products/sums.
10. **강의 예제 연결:** p002-p003.
11. **예제 숫자 해석:** 행정구역 i에서 후보지역 j까지 10분 이내면 Aij=1.
12. **자주 하는 실수:** 행/열을 바꿔 구역과 후보지를 혼동하는 오류.
13. **선행 노드:** facility_location_set_cover
14. **후속 노드:** set_partitioning_packing
15. **동형/유사 노드:** incidence matrix
16. **시험 출제 포인트:** Aij 의미.
17. **RAG retrieval tags:** `coverage_matrix`, `Aij`
18. **Evidence anchors:** `ev_deep_DM_PDF08_node_coverage_matrix` -> `DM_PDF08:p002:L005` / source_id=`DM_PDF08`, page=`p002`, block=`p002-L005`, line=`L005`

> 근거 excerpt: ② 후보지역에서 10분 이내 도달 가능성: 13 X 8 행렬

### n_DM_PDF08.binary_open_variable — 0-1 설치변수 (binary open variable)

1. **한 줄 정의:** 후보지에 시설을 설치하면 1, 아니면 0인 선택 변수다.
2. **쉬운 직관:** 스위치처럼 켜고 끄는 의사결정이다.
3. **언제 쓰는가:** 시설 선택, 프로젝트 선택, 응급차량 설치 여부에 쓴다.
4. **변수 정의:** x_j in {0,1}.
5. **목적함수:** sum x_j minimized or constrained.
6. **제약식:** binary domain and coverage constraints.
7. **수식의 현실 의미:** x=(x1,...,x8).
8. **그래프/네트워크 관점:** binary vector over candidate sites.
9. **스프레드시트/Solver 관점:** Solver에서 bin 조건 또는 int+<=1 조건.
10. **강의 예제 연결:** p002, p004.
11. **예제 숫자 해석:** xj=후보지역 j에 응급차량 설치여부.
12. **자주 하는 실수:** 0<=x<=1만 두어 fractional 설치를 허용하는 오류.
13. **선행 노드:** integer programming
14. **후속 노드:** branch and bound
15. **동형/유사 노드:** fixed-charge y variables
16. **시험 출제 포인트:** binary 설정.
17. **RAG retrieval tags:** `binary`, `0-1`, `xj`
18. **Evidence anchors:** `ev_deep_DM_PDF08_node_binary_open_variable` -> `DM_PDF08:p002:L003` / source_id=`DM_PDF08`, page=`p002`, block=`p002-L003`, line=`L003`

> 근거 excerpt: ① 후보지역에 공공설비 설치 여부  변수셀 (0-1 변수)

### n_DM_PDF08.set_covering_partitioning_packing — covering/partitioning/packing (set covering/partitioning/packing)

1. **한 줄 정의:** Ax>=1은 최소 하나 이상 커버, Ax=1은 정확히 하나, Ax<=1은 겹치지 않게 선택하는 0-1 집합 모형이다.
2. **쉬운 직관:** 부등호 하나가 문제 의미를 완전히 바꾼다.
3. **언제 쓰는가:** coverage 구조를 변형할 때 쓴다.
4. **변수 정의:** A matrix and binary x.
5. **목적함수:** min or max depending on model.
6. **제약식:** Ax>=1, Ax=1, Ax<=1.
7. **수식의 현실 의미:** 행정구역별 covering 수가 1 이상이면 set covering이다.
8. **그래프/네트워크 관점:** set system incidence.
9. **스프레드시트/Solver 관점:** Spreadsheet row coverage counts compared to 1.
10. **강의 예제 연결:** p006-p007.
11. **예제 숫자 해석:** set-partitioning은 covering 수=1, set-packing은 <=1.
12. **자주 하는 실수:** >=,=,<=를 암기만 하고 현실 의미를 설명하지 못하는 오류.
13. **선행 노드:** coverage_matrix
14. **후속 노드:** assignment/set partitioning
15. **동형/유사 노드:** combinatorial optimization
16. **시험 출제 포인트:** 부등호별 의미.
17. **RAG retrieval tags:** `set_covering`, `partitioning`, `packing`
18. **Evidence anchors:** `ev_deep_DM_PDF08_node_set_covering_partitioning_packing` -> `DM_PDF08:p006:L007` / source_id=`DM_PDF08`, page=`p006`, block=`p006-L007`, line=`L007`

> 근거 excerpt: (cf) set-partitioning problem (covering 수 = 1)

### n_DM_PDF08.benefit_max_variant — 혜택 최대화 변형 (benefit maximization variant)

1. **한 줄 정의:** 설치 수가 제한된 상황에서 혜택 받는 주민 수를 최대화하도록 시설 위치와 구역 혜택 여부를 함께 결정하는 변형 모형이다.
2. **쉬운 직관:** 모두를 커버하지 못할 수 있으면, 제한된 시설로 가장 많은 주민에게 혜택을 준다.
3. **언제 쓰는가:** 예산/설치 수 상한 때문에 전 지역 커버가 불가능하거나 목표가 다를 때 쓴다.
4. **변수 정의:** x_j=설치 여부, y_i=구역 i 혜택 여부.
5. **목적함수:** max sum population_i y_i.
6. **제약식:** sum x_j=3, y_i <= sum_j A_ij x_j, x,y binary.
7. **수식의 현실 의미:** 혜택 여부 y를 따로 둬 중복커버가 주민수를 중복 계산하지 않게 한다.
8. **그래프/네트워크 관점:** coverage graph with covered-demand indicators.
9. **스프레드시트/Solver 관점:** Solver에서 x와 y 두 binary vector를 둔다.
10. **강의 예제 연결:** 연습문제 19번 변형.
11. **예제 숫자 해석:** 최대 3군데 설치, 주민 수 최대화.
12. **자주 하는 실수:** x 조합을 목적함수에 직접 여러 번 더해 중복 커버를 과대계산하는 오류.
13. **선행 노드:** set covering
14. **후속 노드:** wrong_model_diagnosis
15. **동형/유사 노드:** max coverage problem
16. **시험 출제 포인트:** y_i 도입 이유.
17. **RAG retrieval tags:** `max_coverage`, `benefit`, `yi`
18. **Evidence anchors:** `ev_deep_DM_PDF08_node_benefit_max_variant` -> `DM_PDF08:p009:L004` / source_id=`DM_PDF08`, page=`p009`, block=`p009-L004`, line=`L004`

> 근거 excerpt:  서비스를 받을 수 있는 주민 수가

### n_DM_PDF08.wrong_model_diagnosis — 잘못된 모형화 진단 (wrong model diagnosis)

1. **한 줄 정의:** coverage 수를 그대로 주민수에 곱해 중복 혜택을 여러 번 계산하는 오류를 식별하는 진단 노드다.
2. **쉬운 직관:** 한 구역이 두 시설에서 커버돼도 주민이 두 배로 늘지는 않는다.
3. **언제 쓰는가:** 혜택 최대화 변형에서 오답을 고칠 때 쓴다.
4. **변수 정의:** x_j only wrong model versus y_i correct model.
5. **목적함수:** wrong objective sums coverage terms directly.
6. **제약식:** missing y_i <= coverage_i linking.
7. **수식의 현실 의미:** 구역별 혜택 여부를 분리해야 중복계산을 막는다.
8. **그래프/네트워크 관점:** overcounting in incidence graph.
9. **스프레드시트/Solver 관점:** Spreadsheet에서 coverage count와 binary benefit indicator를 분리한다.
10. **강의 예제 연결:** p011 범하기 쉬운 잘못된 모형화.
11. **예제 숫자 해석:** Maximize 5.4(x1+x4)+... 형태가 잘못될 수 있다.
12. **자주 하는 실수:** covering 수와 혜택 여부를 동일시하는 오류.
13. **선행 노드:** benefit_max_variant
14. **후속 노드:** binary logic constraints
15. **동형/유사 노드:** indicator variable
16. **시험 출제 포인트:** 오답식 수정.
17. **RAG retrieval tags:** `wrong_model`, `overcount`
18. **Evidence anchors:** `ev_deep_DM_PDF08_node_wrong_model_diagnosis` -> `DM_PDF08:p010:L006` / source_id=`DM_PDF08`, page=`p010`, block=`p010-L006`, line=`L006`

> 근거 excerpt: 2. 목적함수 = 혜택 받는 주민 수 (Max)

### n_DM_PDF08.multiple_optima_facility — 입지모형 복수 최적 (multiple optima in facility location)

1. **한 줄 정의:** 같은 설치 수로 전 지역을 커버하는 후보 조합이 여러 개 나올 수 있는 현상이다.
2. **쉬운 직관:** 최소 시설 수는 같지만 실제 위치 조합은 여러 해가 가능할 수 있다.
3. **언제 쓰는가:** 해석과 대안 제시가 필요할 때 쓴다.
4. **변수 정의:** binary x alternative solutions.
5. **목적함수:** same min sum x.
6. **제약식:** same coverage feasibility.
7. **수식의 현실 의미:** 공공설비 입지선정에는 복수 최적해가 자주 발생한다.
8. **그래프/네트워크 관점:** many equivalent covers in set system.
9. **스프레드시트/Solver 관점:** Solver가 보여준 한 해 외에 대안 해 탐색 필요.
10. **강의 예제 연결:** p008 체크 포인트.
11. **예제 숫자 해석:** 복수 최적해 자주 발생.
12. **자주 하는 실수:** Solver 해 하나만 정책적으로 유일한 답이라고 말하는 오류.
13. **선행 노드:** set_covering
14. **후속 노드:** sensitivity/robustness
15. **동형/유사 노드:** alternate optimum
16. **시험 출제 포인트:** 대안 입지 조합.
17. **RAG retrieval tags:** `multiple_optima`, `facility`
18. **Evidence anchors:** `ev_deep_DM_PDF08_node_multiple_optima_facility` -> `DM_PDF08:p008:L004` / source_id=`DM_PDF08`, page=`p008`, block=`p008-L004`, line=`L004`

> 근거 excerpt: • 공공설비 입지선정 모형에는 복수 최적해가 자주 발생함.

### n_DM_PDF08.branch_bound_review — 분지한계법 복습 (branch-and-bound review)

1. **한 줄 정의:** 0-1 입지모형 같은 정수계획을 풀기 위해 branch-and-bound 과정을 적용하는 후반 복습 노드다.
2. **쉬운 직관:** binary 선택 문제도 결국 탐색과 bound로 최적성을 증명한다.
3. **언제 쓰는가:** 정수계획 해법과 0-1 응용을 연결할 때 쓴다.
4. **변수 정의:** binary/integer variables.
5. **목적함수:** LP relaxation bound and incumbent.
6. **제약식:** branching constraints and pruning.
7. **수식의 현실 의미:** 예제 6.9 분지한계법 적용이 다시 등장한다.
8. **그래프/네트워크 관점:** search tree over binary/integer decisions.
9. **스프레드시트/Solver 관점:** Solver MIP search.
10. **강의 예제 연결:** p015 이후.
11. **예제 숫자 해석:** Z가 큰 부문제부터 적용.
12. **자주 하는 실수:** 모형화와 해법을 분리하지 못하는 오류.
13. **선행 노드:** DM_PDF03 branch_and_bound
14. **후속 노드:** MIP solver
15. **동형/유사 노드:** tree search
16. **시험 출제 포인트:** 분지한계 복습.
17. **RAG retrieval tags:** `branch_bound`, `review`
18. **Evidence anchors:** `ev_deep_DM_PDF08_node_branch_bound_review` -> `DM_PDF08:p015:L001` / source_id=`DM_PDF08`, page=`p015`, block=`p015-L001`, line=`L001`

> 근거 excerpt: 15분지한계법 적용(순수/혼합 정수계획)


## 7. Example Walkthrough Cards

### ex_DM_PDF08.emergency_service_cover — 신도시 B 응급 의료 서비스

- **현실 문장 재해석:** 후보지 8곳 중 최소 개수를 골라 13개 행정구역을 모두 10분 이내 커버한다.
- **의사결정변수:** x_j=후보지 j 설치 여부.
- **목적함수:** min x1+...+x8.
- **제약식:** A x >= 1, x_j binary.
- **Solver 구조:** Solver binary model with coverage matrix.
- **결과 해석:** 해는 설치 후보지 조합이며 복수 최적 가능성이 있다.
- **코칭 순서:**
1. 후보지와 구역 파악.
2. Aij 행렬 작성.
3. Ax>=1 제약.
4. 설치 수 최소화.
- **Evidence anchors:** `ev_deep_DM_PDF08_example_emergency_service_cover` -> `DM_PDF08:p001:L011` / page=`p001`, block=`p001-L011`, line=`L011`

> 근거 excerpt: 응급 서비스를

### ex_DM_PDF08.max_covered_population — 주민 수 혜택 최대화 변형

- **현실 문장 재해석:** 최대 3곳 설치로 혜택 받는 주민 수를 최대화한다.
- **의사결정변수:** x_j 설치, y_i 혜택.
- **목적함수:** max sum population_i y_i.
- **제약식:** sum x_j=3, y_i<=coverage_i, x,y binary.
- **Solver 구조:** Solver with two binary variable blocks.
- **결과 해석:** y_i가 중복커버의 과대계산을 막는다.
- **코칭 순서:**
1. x와 y를 분리.
2. 설치 수 제약.
3. linking constraint.
4. 주민수 목적함수.
- **Evidence anchors:** `ev_deep_DM_PDF08_example_max_covered_population` -> `DM_PDF08:p009:L003` / page=`p009`, block=`p009-L003`, line=`L003`

> 근거 excerpt: (연습문제 19번)

### ex_DM_PDF08.wrong_model_fix — 잘못된 혜택모형 수정

- **현실 문장 재해석:** coverage count를 주민수에 직접 곱하는 잘못된 모형을 y_i indicator로 고친다.
- **의사결정변수:** wrong: only x; correct: x and y.
- **목적함수:** correct max population*y.
- **제약식:** y_i<=sum Aij xj.
- **Solver 구조:** Spreadsheet coverage count plus binary benefit.
- **결과 해석:** 한 구역은 커버되면 1번만 혜택으로 계산한다.
- **코칭 순서:**
1. 오답 목적함수 찾기.
2. 중복커버 문제 설명.
3. y_i 도입.
4. linking constraint 추가.
- **Evidence anchors:** `ev_deep_DM_PDF08_example_wrong_model_fix` -> `DM_PDF08:p011:L002` / page=`p011`, block=`p011-L002`, line=`L002`

> 근거 excerpt: 범하기 쉬운 잘못된 모형화


## 8. Modeling Pattern Library

| pattern | 모형화 템플릿 | 먼저 볼 노드 | 연결 노드 |
| --- | --- | --- | --- |
| cover 최소화 | 모든 행이 하나 이상 커버되도록 Ax>=1, min sum x. | facility_location_set_cover | set covering |
| benefit 최대화 | 설치 수 제한 아래 y_i를 두고 max population*y. | benefit_max_variant | max coverage |
| 오답진단 | coverage count와 benefit indicator를 분리한다. | wrong_model_diagnosis | indicator variable |

## 9. Spreadsheet / Solver Mapping

| 요소 | Solver/Spreadsheet 대응 | 튜터 해설 포인트 |
| --- | --- | --- |
| 변수셀 | x_j 설치 여부, y_i 혜택 여부 | 둘 다 binary. |
| 목표셀 | 설치 수 최소화 또는 혜택 주민수 최대화 | 문제 변형에 따라 방향이 바뀐다. |
| 제약셀 | Ax>=1, sum x=3, y_i<=coverage_i | 부등호 의미를 현실 문장으로 확인한다. |
| 해법 | MIP/branch-and-bound | 복수 최적해 가능성을 보고서에 남긴다. |

## 10. Cross-Chapter Connections

| 연결 대상 | 연결 설명 | 의존/참조 관계 |
| --- | --- | --- |
| DM_PDF04 0-1 IP | 입지선정은 binary 선택변수의 대표 응용이다. | binary -> facility |
| DM_PDF03 분지한계 | 0-1 모형은 branch-and-bound로 최적성을 증명한다. | set covering -> B&B |
| DM_PDF06 네트워크 | coverage matrix는 네트워크 incidence/edge table 사고와 유사하다. | incidence table |

## 11. Misconception & Error Diagnosis Bank

| 오답/착각 | 왜 문제인가 | 교정 코칭 | 연결 노드 |
| --- | --- | --- | --- |
| Ax 부등호 혼동 | >=,=,<=가 각각 covering/partitioning/packing을 뜻한다. | 구역별 현실 문장으로 먼저 번역. | set_covering_partitioning_packing |
| 중복커버 과대계산 | 한 구역 주민은 여러 시설로 커버되어도 한 번만 세야 한다. | y_i 혜택변수를 둔다. | wrong_model_diagnosis |
| binary 설정 누락 | 연속값 0.4개 설치 같은 해가 나올 수 있다. | bin 또는 int+<=1을 지정. | binary_open_variable |

## 12. Retrieval Routing Table

| 사용자 질문 유형 | 먼저 볼 노드 | 다음 볼 노드 | 예제 카드 | 근거 힌트 |
| --- | --- | --- | --- | --- |
| set covering 식 어떻게 세워? | `facility_location_set_cover` | `coverage_matrix` | `emergency_service_cover` | DM_PDF08:p001-p004 |
| covering/partitioning/packing 차이? | `set_covering_partitioning_packing` | `coverage_matrix` | `emergency_service_cover` | DM_PDF08:p006-p007 |
| 주민수 최대화 변형은 왜 y가 필요? | `benefit_max_variant` | `wrong_model_diagnosis` | `max_covered_population` | DM_PDF08:p010-p011 |
| 복수 최적해가 나오면? | `multiple_optima_facility` | `facility_location_set_cover` | `emergency_service_cover` | DM_PDF08:p008 |

## 13. Tutor Session Protocol

1. **지도부터:** Concept Graph Map과 Edge List를 먼저 보여주고, 현재 노드가 전체 OR/MS 흐름에서 어디인지 설명한다.
2. **노드 중심으로:** Core Concept Node Card의 18개 필드를 순서대로 따라가되, 선행/후속/동형 노드를 최소 3개 연결한다.
3. **예제 중심으로:** Example Walkthrough Card를 사용해 현실 문장 -> 변수 -> 목적함수 -> 제약식 -> Solver -> 결과 해석 순서로 진행한다.
4. **문제 풀이 모드:** 사용자가 변수를 먼저 말하게 하고, 목적함수/제약식은 힌트로 한 단계씩 유도한다.
5. **완성 해설 모드:** 위 절차를 생략하지 않고 전체 풀이를 한 번에 제시한다.
6. **암기/정리 모드:** Modeling Pattern Library, Solver Mapping, Misconception Bank만 압축해 제시한다.

## 14. Practice / Check Questions

1. Aij=1의 현실 의미를 한 문장으로 쓰고 Ax>=1을 번역하라.
2. set partitioning과 set packing의 부등호 차이를 예시와 함께 설명하라.
3. 혜택 최대화 변형에서 y_i<=coverage_i가 왜 필요한지 반례로 설명하라.

## 15. Source Trace Table

| RAG label | evidence_id | source_id | page | block | line | excerpt |
| --- | --- | --- | --- | --- | --- | --- |
| `n_DM_PDF08.facility_location_set_cover` | `ev_deep_DM_PDF08_node_facility_location_set_cover` | `DM_PDF08` | `p001` | `p001-L002` | `L002` | 6.8 공공 설비 입지 선정 모형 |
| `n_DM_PDF08.coverage_matrix` | `ev_deep_DM_PDF08_node_coverage_matrix` | `DM_PDF08` | `p002` | `p002-L005` | `L005` | ② 후보지역에서 10분 이내 도달 가능성: 13 X 8 행렬 |
| `n_DM_PDF08.binary_open_variable` | `ev_deep_DM_PDF08_node_binary_open_variable` | `DM_PDF08` | `p002` | `p002-L003` | `L003` | ① 후보지역에 공공설비 설치 여부  변수셀 (0-1 변수) |
| `n_DM_PDF08.set_covering_partitioning_packing` | `ev_deep_DM_PDF08_node_set_covering_partitioning_packing` | `DM_PDF08` | `p006` | `p006-L007` | `L007` | (cf) set-partitioning problem (covering 수 = 1) |
| `n_DM_PDF08.benefit_max_variant` | `ev_deep_DM_PDF08_node_benefit_max_variant` | `DM_PDF08` | `p009` | `p009-L004` | `L004` |  서비스를 받을 수 있는 주민 수가 |
| `n_DM_PDF08.wrong_model_diagnosis` | `ev_deep_DM_PDF08_node_wrong_model_diagnosis` | `DM_PDF08` | `p010` | `p010-L006` | `L006` | 2. 목적함수 = 혜택 받는 주민 수 (Max) |
| `n_DM_PDF08.multiple_optima_facility` | `ev_deep_DM_PDF08_node_multiple_optima_facility` | `DM_PDF08` | `p008` | `p008-L004` | `L004` | • 공공설비 입지선정 모형에는 복수 최적해가 자주 발생함. |
| `n_DM_PDF08.branch_bound_review` | `ev_deep_DM_PDF08_node_branch_bound_review` | `DM_PDF08` | `p015` | `p015-L001` | `L001` | 15분지한계법 적용(순수/혼합 정수계획) |
| `ex_DM_PDF08.emergency_service_cover` | `ev_deep_DM_PDF08_example_emergency_service_cover` | `DM_PDF08` | `p001` | `p001-L011` | `L011` | 응급 서비스를 |
| `ex_DM_PDF08.max_covered_population` | `ev_deep_DM_PDF08_example_max_covered_population` | `DM_PDF08` | `p009` | `p009-L003` | `L003` | (연습문제 19번) |
| `ex_DM_PDF08.wrong_model_fix` | `ev_deep_DM_PDF08_example_wrong_model_fix` | `DM_PDF08` | `p011` | `p011-L002` | `L002` | 범하기 쉬운 잘못된 모형화 |

## 16. QC / Extraction Risk Notes

- **page_count:** 25
- **low_text_pages:** 13
- **extraction_risk_pages:** 13
- **QC policy:** 표, 그림, 수식 이미지가 많은 페이지는 전사 텍스트만으로 숫자를 단정하지 않는다. 튜터는 수식 구조와 증거 anchor를 우선 제시하고, 숫자 최적해는 필요 시 원본 PDF를 대조한다.
- DM_PDF08 후반 분지한계 그림 페이지는 저텍스트가 많아 tree 숫자는 DM_PDF03 전사와 함께 대조한다.
