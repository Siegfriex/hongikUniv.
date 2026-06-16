# DS_PDF07_STATS — RAG tutor source

## Retrieval Routing Table

| route | when to use | primary files |
|---|---|---|
| `DS_PDF07_STATS` | 표본에서 계산한 통계량으로 모집단 모수를 추론하고, 확률·분포·분할표로 불확실성을 표현한다. | `__01_pdf_transcript`, `__02_rawdata_develop`, `__03_concept_node_index`, this `__04_rag` |

## Core Concept Node Cards

### `n_DS_STATS.population_sample_parameter_statistic` — 모집단/표본/모수/통계량

- 정의: 모집단은 관심 대상 전체, 표본은 관측된 일부, 모수는 모집단 값, 통계량은 표본에서 계산한 값이다.
- 직관: 우리가 가진 작은 표본으로 보이지 않는 전체의 성질을 추정한다.
- 수식/절차: sample statistic -> estimate population parameter
- pandas/sklearn 언어: df.sample, df.mean, df.std
- 오답위험: 표본 평균을 모집단 평균 그 자체로 단정하거나 parameter/statistic을 혼동하는 오류.
- 연결: 선행 - / 후속 n_DS_STATS.statistical_inference, n_DS_ML1.train_test_generalization / 유사 -
- source trace: `DS_PDF07_STATS:p002:L007`, `ev_DS_PDF07_STATS_001`

### `n_DS_STATS.statistical_inference` — 통계적 추론

- 정의: 표본 자료를 사용해 모집단의 불확실한 성질을 추정·검정하는 과정이다.
- 직관: 일부 데이터로 전체에 대해 조심스럽게 말하는 규칙이다.
- 수식/절차: estimate + uncertainty + assumption check
- pandas/sklearn 언어: bootstrap confidence interval, train/test generalization analogy
- 오답위험: 표본이 편향되어도 큰 수면 무조건 괜찮다고 보는 오류.
- 연결: 선행 n_DS_STATS.population_sample_parameter_statistic / 후속 n_DS_STATS.bootstrap_imputation, n_DS_ML1.train_test_generalization / 유사 -
- source trace: `DS_PDF07_STATS:p055:L004`, `ev_DS_PDF07_STATS_002`

### `n_DS_STATS.frequency_histogram` — 도수분포/상대도수/히스토그램

- 정의: 자료를 구간이나 범주로 나누어 빈도와 비율을 정리하고 분포 형태를 보는 방법이다.
- 직관: 숫자 목록을 분포의 모양으로 접는 과정이다.
- 수식/절차: relative frequency = class frequency / total count
- pandas/sklearn 언어: pd.cut, value_counts(normalize=True), hist
- 오답위험: 구간폭을 바꾸지 않고 분포 모양을 단정하는 오류.
- 연결: 선행 n_DS_STATS.population_sample_parameter_statistic / 후속 n_DS_VIS.histogram_kde, n_DS_STATS.distribution_family / 유사 -
- source trace: `DS_PDF07_STATS:p010:L004`, `ev_DS_PDF07_STATS_003`

### `n_DS_STATS.probability_random_variable` — 확률/확률변수

- 정의: 불확실한 사건의 가능성을 수로 표현하고, 확률변수는 실험 결과를 숫자로 대응시킨 변수다.
- 직관: 불확실한 현실을 계산 가능한 숫자 규칙으로 바꾸는 언어다.
- 수식/절차: 0 <= P(A) <= 1, random variable X maps outcomes to values
- pandas/sklearn 언어: numpy random variables, scipy distributions
- 오답위험: 관측 비율과 이론 확률을 같은 수준의 확정값으로 혼동하는 오류.
- 연결: 선행 n_DS_STATS.population_sample_parameter_statistic / 후속 n_DS_STATS.conditional_independence, n_DS_LLM.sequence_probability / 유사 -
- source trace: `DS_PDF07_STATS:p015:L004`, `ev_DS_PDF07_STATS_004`

### `n_DS_STATS.conditional_independence` — 조건부확률과 독립

- 정의: 조건부확률은 B가 주어졌을 때 A의 확률이고, 독립은 B 정보가 A의 확률을 바꾸지 않는 상태다.
- 직관: 이미 알고 있는 정보가 판단을 바꾸는지 확인하는 규칙이다.
- 수식/절차: P(A|B)=P(A∩B)/P(B). independent if P(A|B)=P(A) or P(A∩B)=P(A)P(B).
- pandas/sklearn 언어: pd.crosstab(..., normalize='index')
- 오답위험: P(A|B)와 P(B|A)를 바꿔 쓰거나, 상관/동시발생을 독립 위반의 원인으로 과해석하는 오류.
- 연결: 선행 n_DS_STATS.probability_random_variable / 후속 n_DS_STATS.contingency_table, n_DS_LLM.sequence_probability / 유사 -
- source trace: `DS_PDF07_STATS:p012:L004`, `ev_DS_PDF07_STATS_005`

### `n_DS_STATS.distribution_family` — 이산/연속 확률분포

- 정의: 확률변수가 가질 수 있는 값과 그 가능성을 체계적으로 나타낸 모델군이다.
- 직관: 데이터가 어떤 모양으로 나올지 미리 정한 지도다.
- 수식/절차: Discrete: Bernoulli/Binomial/Poisson. Continuous: density over intervals.
- pandas/sklearn 언어: scipy.stats, histogram/KDE, empirical distribution
- 오답위험: 분포 이름을 외우고 적용 조건을 확인하지 않는 오류.
- 연결: 선행 n_DS_STATS.probability_random_variable / 후속 n_DS_ML1.loss_metric, n_DS_LLM.ngram_language_model / 유사 n_DS_VIS.histogram_kde
- source trace: `DS_PDF07_STATS:p014:L004`, `ev_DS_PDF07_STATS_006`

### `n_DS_STATS.contingency_table` — 분할표

- 정의: 두 범주형 변수의 조합 빈도를 2차원 표로 정리한 자료 구조다.
- 직관: 범주 A와 범주 B가 같이 나타나는 패턴을 표로 보는 방법이다.
- 수식/절차: cell count, row proportion, column proportion, expected count
- pandas/sklearn 언어: pd.crosstab(row_col, col_col, normalize=...)
- 오답위험: 행비율과 열비율을 혼동해 조건부확률 방향을 바꾸는 오류.
- 연결: 선행 n_DS_STATS.conditional_independence / 후속 n_DS_ML3.association_rule / 유사 -
- source trace: `DS_PDF07_STATS:p012:L004`, `ev_DS_PDF07_STATS_007`

### `n_DS_STATS.bootstrap_imputation` — Bootstrap과 Imputation

- 정의: Bootstrap은 표본을 복원추출해 통계량 변동성을 추정하고, imputation은 결측값을 분석 가능한 값으로 채운다.
- 직관: 부족하거나 빠진 데이터에서 불확실성을 다루는 두 가지 실무 도구다.
- 수식/절차: bootstrap: resample with replacement -> compute statistic repeatedly. imputation: fill missing by rule/model.
- pandas/sklearn 언어: sklearn SimpleImputer/KNNImputer, sklearn.utils.resample
- 오답위험: 결측을 무조건 평균으로 채우거나 bootstrap 결과를 원자료 증가로 오해하는 오류.
- 연결: 선행 n_DS_STATS.statistical_inference / 후속 n_DS_ML1.preprocessing_leakage, n_DS_ML3.kmeanspp_local_optimum / 유사 -
- source trace: `DS_PDF07_STATS:p056:L004`, `ev_DS_PDF07_STATS_008`

## Visual Example Cards

- `population_sample_terms`: 모집단/표본/모수/통계량 핵심 용어 / anchor `DS_PDF07_STATS:p002:L001` / image `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p002__population_sample_terms.png`
- `frequency_distribution`: 도수분포표 / anchor `DS_PDF07_STATS:p008:L001` / image `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p008__frequency_distribution.png`
- `histogram_frequency`: 히스토그램과 상대도수 / anchor `DS_PDF07_STATS:p010:L001` / image `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p010__histogram_frequency.png`
- `contingency_table`: 두 범주형 변수의 분할표 / anchor `DS_PDF07_STATS:p012:L001` / image `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p012__contingency_table.png`
- `distribution_overview`: 이산/연속 확률분포 개요 / anchor `DS_PDF07_STATS:p014:L001` / image `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p014__distribution_overview.png`
- `bernoulli_trial`: 베르누이 시행 / anchor `DS_PDF07_STATS:p015:L001` / image `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p015__bernoulli_trial.png`
- `bootstrap`: bootstrap 재표본추출 / anchor `DS_PDF07_STATS:p055:L001` / image `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p055__bootstrap.png`

## Code Mapping

- row = observation, column = variable, feature matrix = `X`, target vector = `y`.
- `fit` = 학습, `predict` = 추론, `transform` = 표현 변환, `metric` = 평가 함수.
- 시각화/통계 노드는 pandas 집계와 plot으로, ML 노드는 sklearn estimator/pipeline으로, LLM 노드는 tokenizer/embedding/retrieval로 매핑한다.

## Misconception Bank

- 모집단/표본/모수/통계량: 표본 평균을 모집단 평균 그 자체로 단정하거나 parameter/statistic을 혼동하는 오류.
- 통계적 추론: 표본이 편향되어도 큰 수면 무조건 괜찮다고 보는 오류.
- 도수분포/상대도수/히스토그램: 구간폭을 바꾸지 않고 분포 모양을 단정하는 오류.
- 확률/확률변수: 관측 비율과 이론 확률을 같은 수준의 확정값으로 혼동하는 오류.
- 조건부확률과 독립: P(A|B)와 P(B|A)를 바꿔 쓰거나, 상관/동시발생을 독립 위반의 원인으로 과해석하는 오류.
- 이산/연속 확률분포: 분포 이름을 외우고 적용 조건을 확인하지 않는 오류.
- 분할표: 행비율과 열비율을 혼동해 조건부확률 방향을 바꾸는 오류.
- Bootstrap과 Imputation: 결측을 무조건 평균으로 채우거나 bootstrap 결과를 원자료 증가로 오해하는 오류.

## Web Grounding Notes

- `web_pandas_groupby` Group by: split-apply-combine: https://pandas.pydata.org/docs/user_guide/groupby.html — groupby/crosstab style aggregation routing for EDA and contingency tables.

## Source Trace Table

| node_id | evidence_id | transcript_anchor | snippet |
|---|---|---|---|
| `n_DS_STATS.population_sample_parameter_statistic` | `ev_DS_PDF07_STATS_001` | `DS_PDF07_STATS:p002:L007` | 4. 통계량 Statistic-통계량은 표본자료를 이용해 계산한 수치-표본의 특성을 요약한 값이며, 모집단의 모수를 추정하는 데 활용 |
| `n_DS_STATS.statistical_inference` | `ev_DS_PDF07_STATS_002` | `DS_PDF07_STATS:p055:L004` | 통계 중요 개념 (3)Bootstrap-Bootstrap은하나의 표본에서 다시 표본을 반복적으로 뽑아 통계량의 변동성을 추정하는 방법-Bradley Efron이 1979년에 제안한 방법으로, 원자료의 분포를 정확히 알기 어렵거나 이론적인 표준오차 계산이 복잡할 때 유용하게 사용-Bootstrap의 핵심은복원추출으로 ... |
| `n_DS_STATS.frequency_histogram` | `ev_DS_PDF07_STATS_003` | `DS_PDF07_STATS:p010:L004` | 도수분포와 히스토그램히스토그램 Histogram-히스토그램은 도수분포 또는 상대도수분포를막대그래프 형태로 나타낸 것•가로축: 계급구간•세로축: 도수 또는 상대도수•각 막대의 높이: 해당 계급구간에 속하는 자료의 수 또는 비율누적도수분포 Cumulative Frequency Distribution-누적도수분포는 각 계... |
| `n_DS_STATS.probability_random_variable` | `ev_DS_PDF07_STATS_004` | `DS_PDF07_STATS:p015:L004` | 확률분포•이산형 확률분포 –베르누이 확률분포-베르누이 시행 Bernoulli Trial베르누이 시행은 결과가 두 가지 경우만 가능한 확률 실험 (성공(Success), 실패(Failure))한 번의 시행에서 결과가 오직 두 가지 중 하나로만 나타나는 실험을 의미-베르누이 확률변수: 베르누이 시행의 결과를 숫자로 표현... |
| `n_DS_STATS.conditional_independence` | `ev_DS_PDF07_STATS_005` | `DS_PDF07_STATS:p012:L004` | 분할표Contingency Table-두 범주형 변수에 대한 관측값을 요약하고 해석하기 위한 표 형태의 자료 정리 방법-두 변수가 모두 범주형 변수일 때 사용, 도수분포표를 2차원 형태로 확장한 형태-한 변수의 범주는 행(Row)에, 다른 변수의 범주는 열(Column)에 배치-각 셀(Cell)에는 두 범주가 동시에... |
| `n_DS_STATS.distribution_family` | `ev_DS_PDF07_STATS_006` | `DS_PDF07_STATS:p014:L004` | 확률분포•이산형 확률분포-베르누이 확률분포(Bernoulli distribution)-이항분포(Binomial distribution)-기하분포(Geometric distribution) -포아송분포(Poisson distribution) |
| `n_DS_STATS.contingency_table` | `ev_DS_PDF07_STATS_007` | `DS_PDF07_STATS:p012:L004` | 분할표Contingency Table-두 범주형 변수에 대한 관측값을 요약하고 해석하기 위한 표 형태의 자료 정리 방법-두 변수가 모두 범주형 변수일 때 사용, 도수분포표를 2차원 형태로 확장한 형태-한 변수의 범주는 행(Row)에, 다른 변수의 범주는 열(Column)에 배치-각 셀(Cell)에는 두 범주가 동시에... |
| `n_DS_STATS.bootstrap_imputation` | `ev_DS_PDF07_STATS_008` | `DS_PDF07_STATS:p056:L004` | 통계 중요 개념 (3)-2Bootstrap Aggregating (Bagging)-Bagging은 여러 개의 데이터 샘플을 복원추출(bootstrap)하여 각각의 모델을 학습시키고, 그 결과를 결합하는 앙상블 기법-각 모델이 서로 다른 데이터를 기반으로 학습하기 때문에 모델의 분산(variance)을 줄여 과적합을 ... |
