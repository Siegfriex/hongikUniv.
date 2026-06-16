# DS_PDF06_CODE — RAG tutor source

## Retrieval Routing Table

| route | when to use | primary files |
|---|---|---|
| `DS_PDF06_CODE` | 컴퓨팅 사고를 데이터프레임 조작, 시각화 코드, sklearn 학습 절차로 번역한다. | `__01_pdf_transcript`, `__02_rawdata_develop`, `__03_concept_node_index`, this `__04_rag` |

## Core Concept Node Cards

### `n_DS_CODE.computing_thinking` — 컴퓨팅 사고

- 정의: 문제를 입력, 처리 절차, 출력으로 나누어 컴퓨터가 수행 가능한 단계로 바꾸는 사고방식이다.
- 직관: 현실 문제를 사람이 읽는 문장 대신 기계가 수행할 명령 순서로 바꾸는 과정이다.
- 수식/절차: problem -> input -> algorithm -> output -> validation
- pandas/sklearn 언어: 함수 분해, 반복문, vectorized operation, pipeline
- 오답위험: 코드를 암기하고 문제 구조를 입력/처리/출력으로 나누지 않는 오류.
- 연결: 선행 - / 후속 n_DS_CODE.dataframe_row_column, n_DS_CODE.reproducible_random_state / 유사 -
- source trace: `DS_PDF06_CODE:p005:L008`, `ev_DS_PDF06_CODE_001`

### `n_DS_CODE.dataframe_row_column` — DataFrame 행/열 구조

- 정의: 행은 관측 단위, 열은 변수이며 데이터 분석의 기본 테이블 구조다.
- 직관: 데이터프레임은 분석 질문을 행과 열로 고정하는 표준 작업대다.
- 수식/절차: row=observation, column=variable, X=feature matrix, y=target vector
- pandas/sklearn 언어: pd.DataFrame, df.info, df.describe, df.groupby, df.merge
- 오답위험: 행 의미와 열 의미를 정하지 않고 바로 모델을 fit하는 오류.
- 연결: 선행 n_DS_CODE.computing_thinking / 후속 n_DS_ML1.feature_target_structure, n_DS_VIS.chart_selection / 유사 -
- source trace: `DS_PDF06_CODE:p013:L007`, `ev_DS_PDF06_CODE_002`

### `n_DS_CODE.iris_scatter_boxplot` — Iris 산점도/박스플롯 코드

- 정의: Iris 변수와 Species 라벨을 사용해 관계와 범주별 분포를 시각화하는 코드 예제다.
- 직관: 같은 데이터를 산점도와 박스플롯으로 보면 관계와 집단 차이가 분리되어 보인다.
- 수식/절차: scatter: x=Petal.Length, y=Petal.Width. boxplot: x=Species, y=Petal.Length.
- pandas/sklearn 언어: ggplot geom_point/geom_boxplot 또는 seaborn.scatterplot/boxplot
- 오답위험: Species 순서, 축 단위, 색상 legend를 확인하지 않는 오류.
- 연결: 선행 n_DS_CODE.dataframe_row_column / 후속 n_DS_VIS.scatter_correlation, n_DS_VIS.boxplot_iqr / 유사 -
- source trace: `DS_PDF06_CODE:p025:L006`, `ev_DS_PDF06_CODE_003`

### `n_DS_CODE.sklearn_workflow` — scikit-learn 기본 워크플로

- 정의: 데이터 전처리, 모델 학습, 예측, 평가를 estimator API로 연결하는 Python ML 절차다.
- 직관: 데이터프레임에서 모델 결과까지 가는 표준 컨베이어벨트다.
- 수식/절차: split -> preprocess/scale -> fit -> predict -> metric -> interpret
- pandas/sklearn 언어: train_test_split, StandardScaler, estimator.fit, estimator.predict, metrics
- 오답위험: train/test를 나누지 않고 같은 데이터로 평가하거나, scaler를 전체 데이터에 fit하는 오류.
- 연결: 선행 n_DS_CODE.dataframe_row_column / 후속 n_DS_ML1.train_test_generalization, n_DS_ML2.scaling_distance_models / 유사 -
- source trace: `DS_PDF06_CODE:p036:L013`, `ev_DS_PDF06_CODE_004`

### `n_DS_CODE.reproducible_random_state` — 재현성/random_state

- 정의: 무작위 분할·초기화·샘플링 결과를 다시 만들 수 있게 난수 시드를 고정하는 규칙이다.
- 직관: 같은 실험을 다시 실행해도 비교 가능한 결과가 나오게 하는 잠금장치다.
- 수식/절차: random_state or seed 고정 -> split/initialization/sampling 재현 -> 결과 비교 가능
- pandas/sklearn 언어: np.random.default_rng, random_state=42
- 오답위험: 시드를 고정하지 않고 알고리즘 변경 효과와 난수 변동을 섞어 해석하는 오류.
- 연결: 선행 n_DS_CODE.computing_thinking / 후속 n_DS_ML1.train_test_generalization, n_DS_ML3.kmeanspp_local_optimum / 유사 -
- source trace: `DS_PDF06_CODE:p036:L013`, `ev_DS_PDF06_CODE_005`

## Visual Example Cards

- `programming_language`: 프로그래밍 언어와 절차적 문제 해결 / anchor `DS_PDF06_CODE:p011:L001` / image `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p011__programming_language.png`
- `r_language_intro`: R 언어 특성과 통계 분석 도구 관점 / anchor `DS_PDF06_CODE:p016:L001` / image `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p016__r_language_intro.png`
- `iris_scatter_code`: Iris 산점도 코드 예시 / anchor `DS_PDF06_CODE:p023:L001` / image `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p023__iris_scatter_code.png`
- `iris_boxplot_code`: Iris boxplot과 factor level 제어 / anchor `DS_PDF06_CODE:p025:L001` / image `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p025__iris_boxplot_code.png`
- `sklearn_intro`: scikit-learn 전처리/회귀/분류/군집/평가 소개 / anchor `DS_PDF06_CODE:p036:L001` / image `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p036__sklearn_intro.png`
- `train_test_plot`: train/test와 예측 코드 흐름 / anchor `DS_PDF06_CODE:p037:L001` / image `dataScience/visual_raw/DS_PDF06_CODE/DS_PDF06_CODE_p037__train_test_plot.png`

## Code Mapping

- row = observation, column = variable, feature matrix = `X`, target vector = `y`.
- `fit` = 학습, `predict` = 추론, `transform` = 표현 변환, `metric` = 평가 함수.
- 시각화/통계 노드는 pandas 집계와 plot으로, ML 노드는 sklearn estimator/pipeline으로, LLM 노드는 tokenizer/embedding/retrieval로 매핑한다.

## Misconception Bank

- 컴퓨팅 사고: 코드를 암기하고 문제 구조를 입력/처리/출력으로 나누지 않는 오류.
- DataFrame 행/열 구조: 행 의미와 열 의미를 정하지 않고 바로 모델을 fit하는 오류.
- Iris 산점도/박스플롯 코드: Species 순서, 축 단위, 색상 legend를 확인하지 않는 오류.
- scikit-learn 기본 워크플로: train/test를 나누지 않고 같은 데이터로 평가하거나, scaler를 전체 데이터에 fit하는 오류.
- 재현성/random_state: 시드를 고정하지 않고 알고리즘 변경 효과와 난수 변동을 섞어 해석하는 오류.

## Web Grounding Notes

- `web_pandas_10min` 10 minutes to pandas: https://pandas.pydata.org/docs/user_guide/10min.html — DataFrame, row/column, indexing, missing value, quick EDA code mapping.
- `web_pandas_groupby` Group by: split-apply-combine: https://pandas.pydata.org/docs/user_guide/groupby.html — groupby/crosstab style aggregation routing for EDA and contingency tables.
- `web_sklearn_train_test_split` sklearn.model_selection.train_test_split: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html — Train/test split, random_state, generalization validation.
- `web_sklearn_preprocessing` scikit-learn preprocessing: https://scikit-learn.org/stable/modules/preprocessing.html — Scaling requirement for distance/gradient-sensitive estimators.

## Source Trace Table

| node_id | evidence_id | transcript_anchor | snippet |
|---|---|---|---|
| `n_DS_CODE.computing_thinking` | `ev_DS_PDF06_CODE_001` | `DS_PDF06_CODE:p005:L008` | • 소프트웨어: 하드웨어가 원활하게 작동하도록 하는 ‘명령어의 집합 (set of instructions)’으로 Excel, PowerPoint, KakaoTalk, |
| `n_DS_CODE.dataframe_row_column` | `ev_DS_PDF06_CODE_002` | `DS_PDF06_CODE:p013:L007` | 2차원 10×10 배열이 주어졌을 때, 2번째 행(row)과 5번째 열(column)을 제거하는 코드를 작성하시오. |
| `n_DS_CODE.iris_scatter_boxplot` | `ev_DS_PDF06_CODE_003` | `DS_PDF06_CODE:p025:L006` | Create a box plot using the Petal.Length variable by Species from the Iris dataset. |
| `n_DS_CODE.sklearn_workflow` | `ev_DS_PDF06_CODE_004` | `DS_PDF06_CODE:p036:L013` | from sklearn.model_selection import train_test_split |
| `n_DS_CODE.reproducible_random_state` | `ev_DS_PDF06_CODE_005` | `DS_PDF06_CODE:p036:L013` | from sklearn.model_selection import train_test_split |
