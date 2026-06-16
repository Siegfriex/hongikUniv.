# DS_PDF06_VIS — RAG tutor source

## Retrieval Routing Table

| route | when to use | primary files |
|---|---|---|
| `DS_PDF06_VIS` | 변수 유형과 분석 질문에 맞는 그래프를 고르고, 그래프가 말하는 것과 말하지 못하는 것을 분리한다. | `__01_pdf_transcript`, `__02_rawdata_develop`, `__03_concept_node_index`, this `__04_rag` |

## Core Concept Node Cards

### `n_DS_VIS.chart_selection` — 변수 유형별 그래프 선택

- 정의: 분석 질문과 변수 타입에 맞춰 단변량/이변량/다변량 그래프를 고르는 판단 규칙이다.
- 직관: 그래프는 예쁜 그림이 아니라 어떤 비교를 허용할지 정하는 측정 도구다.
- 수식/절차: 1) 변수 수 확인 2) 변수 타입 확인 3) 분포/관계/구성/비교 중 질문 선택 4) 그래프 선택 5) 해석 한계 표시
- pandas/sklearn 언어: pandas dtype 확인 -> seaborn/ggplot geom 선택 -> 축/색/크기 매핑
- 오답위험: 범주형 변수에 히스토그램을 쓰거나, 상관을 보여야 하는데 파이차트를 쓰는 오류.
- 연결: 선행 - / 후속 n_DS_VIS.histogram_kde, n_DS_VIS.scatter_correlation, n_DS_VIS.heatmap_multivariate / 유사 -
- source trace: `DS_PDF06_VIS:p002:L005`, `ev_DS_PDF06_VIS_001`

### `n_DS_VIS.histogram_kde` — 히스토그램과 KDE

- 정의: 연속형 또는 순서형 수치 변수의 분포를 구간 빈도 또는 부드러운 밀도로 보는 시각화다.
- 직관: 값들이 어디에 몰리고 어디가 비어 있는지 보는 지도다.
- 수식/절차: histogram: bin별 count/relative frequency. KDE: 각 점 주변 커널을 합쳐 연속 밀도 곡선을 만든다.
- pandas/sklearn 언어: Series.plot.hist, seaborn.histplot, ggplot2 geom_histogram/binwidth
- 오답위험: binwidth를 바꿔보지 않고 봉우리 수나 이상치를 단정하는 오류.
- 연결: 선행 n_DS_VIS.chart_selection / 후속 n_DS_STATS.frequency_histogram, n_DS_VIS.boxplot_iqr / 유사 n_DS_STATS.distribution_family
- source trace: `DS_PDF06_VIS:p005:L006`, `ev_DS_PDF06_VIS_002`

### `n_DS_VIS.scatter_correlation` — 산점도와 관계 해석

- 정의: 두 양적 변수의 좌표쌍을 점으로 찍어 관계 방향, 형태, 이상치, 군집을 보는 그래프다.
- 직관: 두 변수가 같이 움직이는지 눈으로 확인하는 첫 번째 도구다.
- 수식/절차: x축 변수와 y축 변수를 잡고 패턴이 선형/비선형/무관/군집/이상치인지 판별한다.
- pandas/sklearn 언어: plt.scatter, seaborn.scatterplot, ggplot geom_point
- 오답위험: 상관이 보인다고 인과라고 말하거나, 비선형 관계를 Pearson 상관 하나로 지워버리는 오류.
- 연결: 선행 n_DS_VIS.chart_selection / 후속 n_DS_ML1.feature_target_structure, n_DS_ML2.distance_metrics / 유사 n_DS_VIS.bubble_plot
- source trace: `DS_PDF06_VIS:p006:L005`, `ev_DS_PDF06_VIS_003`

### `n_DS_VIS.scatterplot_matrix` — 산점도 행렬

- 정의: 여러 양적 변수 쌍의 산점도를 격자로 배열해 다변량 관계를 한 번에 보는 시각화다.
- 직관: 변수 둘씩 비교한 작은 산점도들을 모아 관계 지도를 만든다.
- 수식/절차: for each pair of numeric variables -> scatter plot cell; diagonal often distribution plot
- pandas/sklearn 언어: pandas.plotting.scatter_matrix, seaborn.pairplot
- 오답위험: 행렬을 보고 모든 쌍의 관계가 독립적이라고 생각하거나 다중비교 해석 위험을 무시하는 오류.
- 연결: 선행 n_DS_VIS.scatter_correlation / 후속 n_DS_ML1.feature_target_structure / 유사 n_DS_VIS.heatmap_multivariate
- source trace: `DS_PDF06_VIS:p007:L005`, `ev_DS_PDF06_VIS_004`

### `n_DS_VIS.bubble_plot` — 버블 플롯

- 정의: 산점도 좌표에 점의 크기를 더해 세 번째 양적 변수를 표현하는 그래프다.
- 직관: 위치 두 개와 크기 하나를 동시에 읽는 산점도 확장이다.
- 수식/절차: x/y 좌표 + size mapping. 면적 인식은 비선형이므로 범위와 legend가 중요하다.
- pandas/sklearn 언어: seaborn.scatterplot(size=...), ggplot aes(size=...)
- 오답위험: 원의 반지름과 면적을 혼동해서 크기 차이를 과장/축소하는 오류.
- 연결: 선행 n_DS_VIS.scatter_correlation / 후속 n_DS_VIS.heatmap_multivariate / 유사 n_DS_VIS.scatterplot_matrix
- source trace: `DS_PDF06_VIS:p008:L006`, `ev_DS_PDF06_VIS_005`

### `n_DS_VIS.boxplot_iqr` — 박스플롯/IQR/이상치 후보

- 정의: 중앙값, 사분위수, IQR, whisker, 이상치 후보를 한 그림에 압축하는 그래프다.
- 직관: 분포의 가운데와 꼬리를 요약한 압축 프로필이다.
- 수식/절차: IQR = Q3 - Q1. 흔한 기준: Q1 - 1.5*IQR보다 작거나 Q3 + 1.5*IQR보다 큰 값을 이상치 후보로 표시.
- pandas/sklearn 언어: seaborn.boxplot, ggplot geom_boxplot, pandas boxplot
- 오답위험: 박스플롯 점을 자동 삭제해야 하는 진짜 이상치로 단정하는 오류.
- 연결: 선행 n_DS_STATS.frequency_histogram / 후속 n_DS_CODE.iris_scatter_boxplot, n_DS_ML1.preprocessing_leakage / 유사 n_DS_VIS.histogram_kde
- source trace: `DS_PDF06_VIS:p010:L005`, `ev_DS_PDF06_VIS_006`

### `n_DS_VIS.heatmap_multivariate` — 히트맵

- 정의: 행과 열의 교차값을 색으로 인코딩해 행렬형 패턴을 보는 시각화다.
- 직관: 큰 표를 색의 지형도로 바꿔 군집과 강도를 빠르게 찾는다.
- 수식/절차: matrix/crosstab/correlation table을 만들고 색상 팔레트와 스케일을 지정한다.
- pandas/sklearn 언어: pandas.pivot_table/corr -> seaborn.heatmap
- 오답위험: 색상 스케일을 확인하지 않고 값 차이를 과해석하는 오류.
- 연결: 선행 n_DS_VIS.chart_selection / 후속 n_DS_ML3.clustering_problem, n_DS_STATS.contingency_table / 유사 n_DS_VIS.scatterplot_matrix
- source trace: `DS_PDF06_VIS:p012:L007`, `ev_DS_PDF06_VIS_007`

## Visual Example Cards

- `chart_selection_map`: 단변량/이변량/다변량과 변수 유형별 그래프 선택 / anchor `DS_PDF06_VIS:p002:L001` / image `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p002__chart_selection_map.png`
- `density_kde`: 히스토그램을 부드럽게 해석하는 KDE/밀도 그래프 / anchor `DS_PDF06_VIS:p005:L001` / image `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p005__density_kde.png`
- `scatter_plot`: 두 양적변수 관계와 상관 해석의 출발점 / anchor `DS_PDF06_VIS:p006:L001` / image `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p006__scatter_plot.png`
- `scatterplot_matrix`: 다변량 관계를 여러 산점도 격자로 보는 자료 / anchor `DS_PDF06_VIS:p007:L001` / image `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p007__scatterplot_matrix.png`
- `bubble_plot`: 좌표에 세 번째 크기 변수를 추가하는 시각화 / anchor `DS_PDF06_VIS:p008:L001` / image `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p008__bubble_plot.png`
- `box_plot`: 중앙값/IQR/이상치 후보를 한 번에 보는 그래프 / anchor `DS_PDF06_VIS:p010:L001` / image `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p010__box_plot.png`
- `heatmap`: 행렬형 다변량 값과 군집 패턴을 색으로 보는 그래프 / anchor `DS_PDF06_VIS:p012:L001` / image `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p012__heatmap.png`

## Code Mapping

- row = observation, column = variable, feature matrix = `X`, target vector = `y`.
- `fit` = 학습, `predict` = 추론, `transform` = 표현 변환, `metric` = 평가 함수.
- 시각화/통계 노드는 pandas 집계와 plot으로, ML 노드는 sklearn estimator/pipeline으로, LLM 노드는 tokenizer/embedding/retrieval로 매핑한다.

## Misconception Bank

- 변수 유형별 그래프 선택: 범주형 변수에 히스토그램을 쓰거나, 상관을 보여야 하는데 파이차트를 쓰는 오류.
- 히스토그램과 KDE: binwidth를 바꿔보지 않고 봉우리 수나 이상치를 단정하는 오류.
- 산점도와 관계 해석: 상관이 보인다고 인과라고 말하거나, 비선형 관계를 Pearson 상관 하나로 지워버리는 오류.
- 산점도 행렬: 행렬을 보고 모든 쌍의 관계가 독립적이라고 생각하거나 다중비교 해석 위험을 무시하는 오류.
- 버블 플롯: 원의 반지름과 면적을 혼동해서 크기 차이를 과장/축소하는 오류.
- 박스플롯/IQR/이상치 후보: 박스플롯 점을 자동 삭제해야 하는 진짜 이상치로 단정하는 오류.
- 히트맵: 색상 스케일을 확인하지 않고 값 차이를 과해석하는 오류.

## Web Grounding Notes

- `web_ggplot2_histogram` ggplot2 geom_histogram: https://ggplot2.tidyverse.org/reference/geom_histogram.html — Histogram/binwidth and density-style visualization mapping.

## Source Trace Table

| node_id | evidence_id | transcript_anchor | snippet |
|---|---|---|---|
| `n_DS_VIS.chart_selection` | `ev_DS_PDF06_VIS_001` | `DS_PDF06_VIS:p002:L005` | •단변량 |
| `n_DS_VIS.histogram_kde` | `ev_DS_PDF06_VIS_002` | `DS_PDF06_VIS:p005:L006` | 밀도추정그래프(주로커널밀도추정, Kernel Density Estimation)는히스토그램을부드러운곡선형태로만든것 |
| `n_DS_VIS.scatter_correlation` | `ev_DS_PDF06_VIS_003` | `DS_PDF06_VIS:p006:L005` | •Scatter Plot(산점도) |
| `n_DS_VIS.scatterplot_matrix` | `ev_DS_PDF06_VIS_004` | `DS_PDF06_VIS:p007:L005` | •Scatterplot matrix |
| `n_DS_VIS.bubble_plot` | `ev_DS_PDF06_VIS_005` | `DS_PDF06_VIS:p008:L006` | - 산점도(Scatter Plot)에데이터의크기차원을하나더추가한그래프 |
| `n_DS_VIS.boxplot_iqr` | `ev_DS_PDF06_VIS_006` | `DS_PDF06_VIS:p010:L005` | •Box Plot |
| `n_DS_VIS.heatmap_multivariate` | `ev_DS_PDF06_VIS_007` | `DS_PDF06_VIS:p012:L007` | <Heatmap with Dendrogram> |
