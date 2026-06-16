# DS_PDF06_CODE — rawdata develop

## One-line source role

컴퓨팅 사고를 데이터프레임 조작, 시각화 코드, sklearn 학습 절차로 번역한다.

## Source policy

- PDF raw: `dataScience/pdf_raw/[Lecture][DS][06][02] RPython (1).pdf`
- TXT raw transcript: `dataScience/txt_raw/DS_PDF02__r_python__full_transcript.txt`
- PDF page images are derived visual raw data, not a replacement for the PDF.
- 숫자·공식·최적값은 전사와 이미지가 충돌하면 원본 PDF 대조가 우선이다.

## Visual raw intake

- `DS_PDF06_CODE:p011:L001` programming_language: 프로그래밍 언어와 절차적 문제 해결 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p011__programming_language.png`
- `DS_PDF06_CODE:p016:L001` r_language_intro: R 언어 특성과 통계 분석 도구 관점 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p016__r_language_intro.png`
- `DS_PDF06_CODE:p023:L001` iris_scatter_code: Iris 산점도 코드 예시 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p023__iris_scatter_code.png`
- `DS_PDF06_CODE:p025:L001` iris_boxplot_code: Iris boxplot과 factor level 제어 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p025__iris_boxplot_code.png`
- `DS_PDF06_CODE:p036:L001` sklearn_intro: scikit-learn 전처리/회귀/분류/군집/평가 소개 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p036__sklearn_intro.png`
- `DS_PDF06_CODE:p037:L001` train_test_plot: train/test와 예측 코드 흐름 -> `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p037__train_test_plot.png`

## Deep rawdata development by node

### 컴퓨팅 사고

- 현재 노드: `n_DS_CODE.computing_thinking`
- 관련 파일: `DS_PDF06_CODE` / `DS_PDF02__r_python__full_transcript.txt`
- 근거 anchor: `DS_PDF06_CODE:p005:L008` / `ev_DS_PDF06_CODE_001`
- 한 줄 정의: 문제를 입력, 처리 절차, 출력으로 나누어 컴퓨터가 수행 가능한 단계로 바꾸는 사고방식이다.
- 쉬운 직관: 현실 문제를 사람이 읽는 문장 대신 기계가 수행할 명령 순서로 바꾸는 과정이다.
- 수식/절차: problem -> input -> algorithm -> output -> validation
- 데이터프레임 구조: 입력은 DataFrame/array, 처리는 함수·조건·반복·집계, 출력은 표/그래프/모델 결과다.
- 코드 관점: 함수 분해, 반복문, vectorized operation, pipeline
- 강의 예제 연결: R/Python PDF의 프로그래밍 입문부가 데이터 분석 코드의 전제다.
- 자주 하는 실수: 코드를 암기하고 문제 구조를 입력/처리/출력으로 나누지 않는 오류.
- 선행 노드: -
- 후속 노드: `n_DS_CODE.dataframe_row_column`, `n_DS_CODE.reproducible_random_state`
- 유사 노드: -
- evidence snippet: • 소프트웨어: 하드웨어가 원활하게 작동하도록 하는 ‘명령어의 집합 (set of instructions)’으로 Excel, PowerPoint, KakaoTalk,
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### DataFrame 행/열 구조

- 현재 노드: `n_DS_CODE.dataframe_row_column`
- 관련 파일: `DS_PDF06_CODE` / `DS_PDF02__r_python__full_transcript.txt`
- 근거 anchor: `DS_PDF06_CODE:p013:L007` / `ev_DS_PDF06_CODE_002`
- 한 줄 정의: 행은 관측 단위, 열은 변수이며 데이터 분석의 기본 테이블 구조다.
- 쉬운 직관: 데이터프레임은 분석 질문을 행과 열로 고정하는 표준 작업대다.
- 수식/절차: row=observation, column=variable, X=feature matrix, y=target vector
- 데이터프레임 구조: 각 column의 dtype, missing, cardinality가 전처리와 그래프 선택을 결정한다.
- 코드 관점: pd.DataFrame, df.info, df.describe, df.groupby, df.merge
- 강의 예제 연결: Iris 데이터의 Petal.Length, Petal.Width, Species가 변수/라벨 구분 예다.
- 자주 하는 실수: 행 의미와 열 의미를 정하지 않고 바로 모델을 fit하는 오류.
- 선행 노드: `n_DS_CODE.computing_thinking`
- 후속 노드: `n_DS_ML1.feature_target_structure`, `n_DS_VIS.chart_selection`
- 유사 노드: -
- evidence snippet: 2차원 10×10 배열이 주어졌을 때, 2번째 행(row)과 5번째 열(column)을 제거하는 코드를 작성하시오.
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Iris 산점도/박스플롯 코드

- 현재 노드: `n_DS_CODE.iris_scatter_boxplot`
- 관련 파일: `DS_PDF06_CODE` / `DS_PDF02__r_python__full_transcript.txt`
- 근거 anchor: `DS_PDF06_CODE:p025:L006` / `ev_DS_PDF06_CODE_003`
- 한 줄 정의: Iris 변수와 Species 라벨을 사용해 관계와 범주별 분포를 시각화하는 코드 예제다.
- 쉬운 직관: 같은 데이터를 산점도와 박스플롯으로 보면 관계와 집단 차이가 분리되어 보인다.
- 수식/절차: scatter: x=Petal.Length, y=Petal.Width. boxplot: x=Species, y=Petal.Length.
- 데이터프레임 구조: Petal.Length/Petal.Width는 feature, Species는 grouping label이다.
- 코드 관점: ggplot geom_point/geom_boxplot 또는 seaborn.scatterplot/boxplot
- 강의 예제 연결: R 예제의 Iris scatter plot과 box plot 페이지가 Gate 3 실습의 핵심 예제다.
- 자주 하는 실수: Species 순서, 축 단위, 색상 legend를 확인하지 않는 오류.
- 선행 노드: `n_DS_CODE.dataframe_row_column`
- 후속 노드: `n_DS_VIS.scatter_correlation`, `n_DS_VIS.boxplot_iqr`
- 유사 노드: -
- evidence snippet: Create a box plot using the Petal.Length variable by Species from the Iris dataset.
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### scikit-learn 기본 워크플로

- 현재 노드: `n_DS_CODE.sklearn_workflow`
- 관련 파일: `DS_PDF06_CODE` / `DS_PDF02__r_python__full_transcript.txt`
- 근거 anchor: `DS_PDF06_CODE:p036:L013` / `ev_DS_PDF06_CODE_004`
- 한 줄 정의: 데이터 전처리, 모델 학습, 예측, 평가를 estimator API로 연결하는 Python ML 절차다.
- 쉬운 직관: 데이터프레임에서 모델 결과까지 가는 표준 컨베이어벨트다.
- 수식/절차: split -> preprocess/scale -> fit -> predict -> metric -> interpret
- 데이터프레임 구조: X는 2D feature matrix, y는 1D target vector가 기본이다.
- 코드 관점: train_test_split, StandardScaler, estimator.fit, estimator.predict, metrics
- 강의 예제 연결: R/Python PDF의 scikit-learn 소개는 ML Part 1~3의 코드 실행 기반이다.
- 자주 하는 실수: train/test를 나누지 않고 같은 데이터로 평가하거나, scaler를 전체 데이터에 fit하는 오류.
- 선행 노드: `n_DS_CODE.dataframe_row_column`
- 후속 노드: `n_DS_ML1.train_test_generalization`, `n_DS_ML2.scaling_distance_models`
- 유사 노드: -
- evidence snippet: from sklearn.model_selection import train_test_split
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 재현성/random_state

- 현재 노드: `n_DS_CODE.reproducible_random_state`
- 관련 파일: `DS_PDF06_CODE` / `DS_PDF02__r_python__full_transcript.txt`
- 근거 anchor: `DS_PDF06_CODE:p036:L013` / `ev_DS_PDF06_CODE_005`
- 한 줄 정의: 무작위 분할·초기화·샘플링 결과를 다시 만들 수 있게 난수 시드를 고정하는 규칙이다.
- 쉬운 직관: 같은 실험을 다시 실행해도 비교 가능한 결과가 나오게 하는 잠금장치다.
- 수식/절차: random_state or seed 고정 -> split/initialization/sampling 재현 -> 결과 비교 가능
- 데이터프레임 구조: mock data, train/test split, k-means 초기 중심, bootstrap sample에 적용된다.
- 코드 관점: np.random.default_rng, random_state=42
- 강의 예제 연결: Python 예제의 train/test 시각화와 k-means 초기점 문제에 모두 연결된다.
- 자주 하는 실수: 시드를 고정하지 않고 알고리즘 변경 효과와 난수 변동을 섞어 해석하는 오류.
- 선행 노드: `n_DS_CODE.computing_thinking`
- 후속 노드: `n_DS_ML1.train_test_generalization`, `n_DS_ML3.kmeanspp_local_optimum`
- 유사 노드: -
- evidence snippet: from sklearn.model_selection import train_test_split
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?
