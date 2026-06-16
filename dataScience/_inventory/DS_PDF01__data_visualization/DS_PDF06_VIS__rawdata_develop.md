# DS_PDF06_VIS — rawdata develop

## One-line source role

변수 유형과 분석 질문에 맞는 그래프를 고르고, 그래프가 말하는 것과 말하지 못하는 것을 분리한다.

## Source policy

- PDF raw: `dataScience/pdf_raw/[Lecture][DS][06][01] 데이터시각화 (3).pdf`
- TXT raw transcript: `dataScience/txt_raw/DS_PDF01__data_visualization__full_transcript.txt`
- PDF page images are derived visual raw data, not a replacement for the PDF.
- 숫자·공식·최적값은 전사와 이미지가 충돌하면 원본 PDF 대조가 우선이다.

## Visual raw intake

- `DS_PDF06_VIS:p002:L001` chart_selection_map: 단변량/이변량/다변량과 변수 유형별 그래프 선택 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p002__chart_selection_map.png`
- `DS_PDF06_VIS:p005:L001` density_kde: 히스토그램을 부드럽게 해석하는 KDE/밀도 그래프 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p005__density_kde.png`
- `DS_PDF06_VIS:p006:L001` scatter_plot: 두 양적변수 관계와 상관 해석의 출발점 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p006__scatter_plot.png`
- `DS_PDF06_VIS:p007:L001` scatterplot_matrix: 다변량 관계를 여러 산점도 격자로 보는 자료 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p007__scatterplot_matrix.png`
- `DS_PDF06_VIS:p008:L001` bubble_plot: 좌표에 세 번째 크기 변수를 추가하는 시각화 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p008__bubble_plot.png`
- `DS_PDF06_VIS:p010:L001` box_plot: 중앙값/IQR/이상치 후보를 한 번에 보는 그래프 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p010__box_plot.png`
- `DS_PDF06_VIS:p012:L001` heatmap: 행렬형 다변량 값과 군집 패턴을 색으로 보는 그래프 -> `dataScience/visual_raw/DS_PDF06_VIS/DS_PDF06_VIS_p012__heatmap.png`

## Deep rawdata development by node

### 변수 유형별 그래프 선택

- 현재 노드: `n_DS_VIS.chart_selection`
- 관련 파일: `DS_PDF06_VIS` / `DS_PDF01__data_visualization__full_transcript.txt`
- 근거 anchor: `DS_PDF06_VIS:p002:L005` / `ev_DS_PDF06_VIS_001`
- 한 줄 정의: 분석 질문과 변수 타입에 맞춰 단변량/이변량/다변량 그래프를 고르는 판단 규칙이다.
- 쉬운 직관: 그래프는 예쁜 그림이 아니라 어떤 비교를 허용할지 정하는 측정 도구다.
- 수식/절차: 1) 변수 수 확인 2) 변수 타입 확인 3) 분포/관계/구성/비교 중 질문 선택 4) 그래프 선택 5) 해석 한계 표시
- 데이터프레임 구조: column dtype과 cardinality가 그래프 선택의 입력이다.
- 코드 관점: pandas dtype 확인 -> seaborn/ggplot geom 선택 -> 축/색/크기 매핑
- 강의 예제 연결: 슬라이드 초반의 양적/범주형, 단변량/이변량/다변량 표가 전체 시각화 라우터다.
- 자주 하는 실수: 범주형 변수에 히스토그램을 쓰거나, 상관을 보여야 하는데 파이차트를 쓰는 오류.
- 선행 노드: -
- 후속 노드: `n_DS_VIS.histogram_kde`, `n_DS_VIS.scatter_correlation`, `n_DS_VIS.heatmap_multivariate`
- 유사 노드: -
- evidence snippet: •단변량
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 히스토그램과 KDE

- 현재 노드: `n_DS_VIS.histogram_kde`
- 관련 파일: `DS_PDF06_VIS` / `DS_PDF01__data_visualization__full_transcript.txt`
- 근거 anchor: `DS_PDF06_VIS:p005:L006` / `ev_DS_PDF06_VIS_002`
- 한 줄 정의: 연속형 또는 순서형 수치 변수의 분포를 구간 빈도 또는 부드러운 밀도로 보는 시각화다.
- 쉬운 직관: 값들이 어디에 몰리고 어디가 비어 있는지 보는 지도다.
- 수식/절차: histogram: bin별 count/relative frequency. KDE: 각 점 주변 커널을 합쳐 연속 밀도 곡선을 만든다.
- 데이터프레임 구조: 하나의 numeric column이 입력이고, binwidth가 해석을 크게 바꾼다.
- 코드 관점: Series.plot.hist, seaborn.histplot, ggplot2 geom_histogram/binwidth
- 강의 예제 연결: 데이터시각화 PDF의 density plot 페이지가 histogram을 매끈한 곡선으로 해석하는 브릿지다.
- 자주 하는 실수: binwidth를 바꿔보지 않고 봉우리 수나 이상치를 단정하는 오류.
- 선행 노드: `n_DS_VIS.chart_selection`
- 후속 노드: `n_DS_STATS.frequency_histogram`, `n_DS_VIS.boxplot_iqr`
- 유사 노드: `n_DS_STATS.distribution_family`
- evidence snippet: 밀도추정그래프(주로커널밀도추정, Kernel Density Estimation)는히스토그램을부드러운곡선형태로만든것
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 산점도와 관계 해석

- 현재 노드: `n_DS_VIS.scatter_correlation`
- 관련 파일: `DS_PDF06_VIS` / `DS_PDF01__data_visualization__full_transcript.txt`
- 근거 anchor: `DS_PDF06_VIS:p006:L005` / `ev_DS_PDF06_VIS_003`
- 한 줄 정의: 두 양적 변수의 좌표쌍을 점으로 찍어 관계 방향, 형태, 이상치, 군집을 보는 그래프다.
- 쉬운 직관: 두 변수가 같이 움직이는지 눈으로 확인하는 첫 번째 도구다.
- 수식/절차: x축 변수와 y축 변수를 잡고 패턴이 선형/비선형/무관/군집/이상치인지 판별한다.
- 데이터프레임 구조: 두 numeric columns, 필요하면 hue로 범주형 column을 추가한다.
- 코드 관점: plt.scatter, seaborn.scatterplot, ggplot geom_point
- 강의 예제 연결: Iris Petal.Length와 Petal.Width 산점도는 변수 관계와 종 분리를 동시에 보여준다.
- 자주 하는 실수: 상관이 보인다고 인과라고 말하거나, 비선형 관계를 Pearson 상관 하나로 지워버리는 오류.
- 선행 노드: `n_DS_VIS.chart_selection`
- 후속 노드: `n_DS_ML1.feature_target_structure`, `n_DS_ML2.distance_metrics`
- 유사 노드: `n_DS_VIS.bubble_plot`
- evidence snippet: •Scatter Plot(산점도)
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 산점도 행렬

- 현재 노드: `n_DS_VIS.scatterplot_matrix`
- 관련 파일: `DS_PDF06_VIS` / `DS_PDF01__data_visualization__full_transcript.txt`
- 근거 anchor: `DS_PDF06_VIS:p007:L005` / `ev_DS_PDF06_VIS_004`
- 한 줄 정의: 여러 양적 변수 쌍의 산점도를 격자로 배열해 다변량 관계를 한 번에 보는 시각화다.
- 쉬운 직관: 변수 둘씩 비교한 작은 산점도들을 모아 관계 지도를 만든다.
- 수식/절차: for each pair of numeric variables -> scatter plot cell; diagonal often distribution plot
- 데이터프레임 구조: 여러 numeric columns가 입력이고, hue로 범주 라벨을 겹칠 수 있다.
- 코드 관점: pandas.plotting.scatter_matrix, seaborn.pairplot
- 강의 예제 연결: 데이터시각화 PDF의 scatterplot matrix 페이지가 다변량 관계 탐색 예다.
- 자주 하는 실수: 행렬을 보고 모든 쌍의 관계가 독립적이라고 생각하거나 다중비교 해석 위험을 무시하는 오류.
- 선행 노드: `n_DS_VIS.scatter_correlation`
- 후속 노드: `n_DS_ML1.feature_target_structure`
- 유사 노드: `n_DS_VIS.heatmap_multivariate`
- evidence snippet: •Scatterplot matrix
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 버블 플롯

- 현재 노드: `n_DS_VIS.bubble_plot`
- 관련 파일: `DS_PDF06_VIS` / `DS_PDF01__data_visualization__full_transcript.txt`
- 근거 anchor: `DS_PDF06_VIS:p008:L006` / `ev_DS_PDF06_VIS_005`
- 한 줄 정의: 산점도 좌표에 점의 크기를 더해 세 번째 양적 변수를 표현하는 그래프다.
- 쉬운 직관: 위치 두 개와 크기 하나를 동시에 읽는 산점도 확장이다.
- 수식/절차: x/y 좌표 + size mapping. 면적 인식은 비선형이므로 범위와 legend가 중요하다.
- 데이터프레임 구조: numeric x, numeric y, numeric size column이 필요하다.
- 코드 관점: seaborn.scatterplot(size=...), ggplot aes(size=...)
- 강의 예제 연결: 시각화 PDF의 Bubble Plot 페이지는 산점도에 크기 차원을 추가하는 예다.
- 자주 하는 실수: 원의 반지름과 면적을 혼동해서 크기 차이를 과장/축소하는 오류.
- 선행 노드: `n_DS_VIS.scatter_correlation`
- 후속 노드: `n_DS_VIS.heatmap_multivariate`
- 유사 노드: `n_DS_VIS.scatterplot_matrix`
- evidence snippet: - 산점도(Scatter Plot)에데이터의크기차원을하나더추가한그래프
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 박스플롯/IQR/이상치 후보

- 현재 노드: `n_DS_VIS.boxplot_iqr`
- 관련 파일: `DS_PDF06_VIS` / `DS_PDF01__data_visualization__full_transcript.txt`
- 근거 anchor: `DS_PDF06_VIS:p010:L005` / `ev_DS_PDF06_VIS_006`
- 한 줄 정의: 중앙값, 사분위수, IQR, whisker, 이상치 후보를 한 그림에 압축하는 그래프다.
- 쉬운 직관: 분포의 가운데와 꼬리를 요약한 압축 프로필이다.
- 수식/절차: IQR = Q3 - Q1. 흔한 기준: Q1 - 1.5*IQR보다 작거나 Q3 + 1.5*IQR보다 큰 값을 이상치 후보로 표시.
- 데이터프레임 구조: numeric column을 범주별 groupby해서 분포를 비교할 수 있다.
- 코드 관점: seaborn.boxplot, ggplot geom_boxplot, pandas boxplot
- 강의 예제 연결: R/Python PDF의 Iris species별 Petal.Length boxplot과 연결된다.
- 자주 하는 실수: 박스플롯 점을 자동 삭제해야 하는 진짜 이상치로 단정하는 오류.
- 선행 노드: `n_DS_STATS.frequency_histogram`
- 후속 노드: `n_DS_CODE.iris_scatter_boxplot`, `n_DS_ML1.preprocessing_leakage`
- 유사 노드: `n_DS_VIS.histogram_kde`
- evidence snippet: •Box Plot
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### 히트맵

- 현재 노드: `n_DS_VIS.heatmap_multivariate`
- 관련 파일: `DS_PDF06_VIS` / `DS_PDF01__data_visualization__full_transcript.txt`
- 근거 anchor: `DS_PDF06_VIS:p012:L007` / `ev_DS_PDF06_VIS_007`
- 한 줄 정의: 행과 열의 교차값을 색으로 인코딩해 행렬형 패턴을 보는 시각화다.
- 쉬운 직관: 큰 표를 색의 지형도로 바꿔 군집과 강도를 빠르게 찾는다.
- 수식/절차: matrix/crosstab/correlation table을 만들고 색상 팔레트와 스케일을 지정한다.
- 데이터프레임 구조: pivot table 또는 correlation matrix가 대표 입력이다.
- 코드 관점: pandas.pivot_table/corr -> seaborn.heatmap
- 강의 예제 연결: 시각화 PDF는 heatmap with dendrogram을 다변량 패턴 탐색 예로 둔다.
- 자주 하는 실수: 색상 스케일을 확인하지 않고 값 차이를 과해석하는 오류.
- 선행 노드: `n_DS_VIS.chart_selection`
- 후속 노드: `n_DS_ML3.clustering_problem`, `n_DS_STATS.contingency_table`
- 유사 노드: `n_DS_VIS.scatterplot_matrix`
- evidence snippet: <Heatmap with Dendrogram>
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?
