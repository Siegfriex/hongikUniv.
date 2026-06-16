#!/usr/bin/env python3
"""Build dataScience PDF visual/rawdata/node-link/RAG tutor corpus."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import fitz


ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "dataScience"
INVENTORY = COURSE / "_inventory"
TXT_RAW = COURSE / "txt_raw"
PDF_RAW = COURSE / "pdf_raw"
VISUAL_RAW = COURSE / "visual_raw"
FLAT_PACK = COURSE / "rag_applied_flat_pack"


@dataclass(frozen=True)
class Concept:
    node_id: str
    label: str
    definition: str
    intuition: str
    formula_or_procedure: str
    dataframe_view: str
    code_view: str
    course_example: str
    common_mistake: str
    prerequisites: tuple[str, ...] = ()
    followups: tuple[str, ...] = ()
    analogous: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    web_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class VisualPage:
    page: int
    label: str
    reason: str


@dataclass(frozen=True)
class SourceProfile:
    route_id: str
    folder: str
    title: str
    gate: str
    pdf_name: str
    transcript_name: str
    one_line: str
    graph_location: str
    visual_pages: tuple[VisualPage, ...]
    concepts: tuple[Concept, ...]
    local_edges: tuple[tuple[str, str, str, str], ...] = field(default_factory=tuple)


WEB_SOURCES = [
    {
        "id": "web_pandas_10min",
        "title": "10 minutes to pandas",
        "url": "https://pandas.pydata.org/docs/user_guide/10min.html",
        "use": "DataFrame, row/column, indexing, missing value, quick EDA code mapping.",
        "scope": "DS_PDF06_CODE, Gate 2",
    },
    {
        "id": "web_pandas_groupby",
        "title": "Group by: split-apply-combine",
        "url": "https://pandas.pydata.org/docs/user_guide/groupby.html",
        "use": "groupby/crosstab style aggregation routing for EDA and contingency tables.",
        "scope": "DS_PDF06_CODE, DS_PDF07_STATS",
    },
    {
        "id": "web_ggplot2_histogram",
        "title": "ggplot2 geom_histogram",
        "url": "https://ggplot2.tidyverse.org/reference/geom_histogram.html",
        "use": "Histogram/binwidth and density-style visualization mapping.",
        "scope": "DS_PDF06_VIS",
    },
    {
        "id": "web_sklearn_train_test_split",
        "title": "sklearn.model_selection.train_test_split",
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html",
        "use": "Train/test split, random_state, generalization validation.",
        "scope": "DS_PDF08_ML1",
    },
    {
        "id": "web_sklearn_preprocessing",
        "title": "scikit-learn preprocessing",
        "url": "https://scikit-learn.org/stable/modules/preprocessing.html",
        "use": "Scaling requirement for distance/gradient-sensitive estimators.",
        "scope": "DS_PDF08_ML2, DS_PDF08_ML3",
    },
    {
        "id": "web_sklearn_svm",
        "title": "scikit-learn Support Vector Machines",
        "url": "https://scikit-learn.org/stable/modules/svm.html",
        "use": "SVM margin, hyperplane, kernel, classifier API mapping.",
        "scope": "DS_PDF08_ML2",
    },
    {
        "id": "web_sklearn_neighbors",
        "title": "scikit-learn Nearest Neighbors",
        "url": "https://scikit-learn.org/stable/modules/neighbors.html",
        "use": "kNN distance/vote/radius-neighbor routing.",
        "scope": "DS_PDF08_ML2",
    },
    {
        "id": "web_sklearn_tree",
        "title": "scikit-learn Decision Trees",
        "url": "https://scikit-learn.org/stable/modules/tree.html",
        "use": "Decision tree as supervised if-then rules, impurity reduction, max_depth/pruning-style overfitting control.",
        "scope": "DS_PDF08_ML2, Session 5 extension",
    },
    {
        "id": "web_sklearn_confusion_metrics",
        "title": "scikit-learn classification metrics",
        "url": "https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics",
        "use": "Confusion matrix, accuracy, precision, recall, F1, and threshold-sensitive classification evaluation.",
        "scope": "DS_PDF08_ML1, Session 2",
    },
    {
        "id": "web_sklearn_kmeans",
        "title": "scikit-learn K-means",
        "url": "https://scikit-learn.org/stable/modules/clustering.html#k-means",
        "use": "K-means objective, inertia, k-means++ initialization, PCA-before-kmeans caveat.",
        "scope": "DS_PDF08_ML3",
    },
    {
        "id": "web_sklearn_silhouette",
        "title": "sklearn.metrics.silhouette_score",
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html",
        "use": "Silhouette formula and score interpretation.",
        "scope": "DS_PDF08_ML3",
    },
    {
        "id": "web_sklearn_pca",
        "title": "scikit-learn PCA",
        "url": "https://scikit-learn.org/stable/modules/decomposition.html#pca",
        "use": "PCA as dimensionality reduction, not a predictive model.",
        "scope": "DS_PDF08_ML3",
    },
    {
        "id": "web_agrawal_srikant_1994",
        "title": "Fast Algorithms for Mining Association Rules",
        "url": "https://www.vldb.org/conf/1994/P487.PDF",
        "use": "Association-rule formalization and Apriori lineage.",
        "scope": "DS_PDF08_ML3",
    },
    {
        "id": "web_transformer_2017",
        "title": "Attention Is All You Need",
        "url": "https://arxiv.org/abs/1706.03762",
        "use": "Transformer as attention-based sequence architecture.",
        "scope": "DS_PDF09_LLM",
    },
    {
        "id": "web_bert_2018",
        "title": "BERT: Pre-training of Deep Bidirectional Transformers",
        "url": "https://arxiv.org/abs/1810.04805",
        "use": "Encoder-style bidirectional pre-training and downstream fine-tuning.",
        "scope": "DS_PDF09_LLM",
    },
    {
        "id": "web_instructgpt_2022",
        "title": "Training language models to follow instructions with human feedback",
        "url": "https://arxiv.org/abs/2203.02155",
        "use": "Instruction tuning/RLHF as user-intent alignment extension.",
        "scope": "DS_PDF09_LLM",
    },
    {
        "id": "web_rag_2020",
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "url": "https://arxiv.org/abs/2005.11401",
        "use": "RAG as parametric model plus non-parametric retrieval memory.",
        "scope": "DS_PDF09_LLM, global tutor design",
    },
]


def c(
    node_id: str,
    label: str,
    definition: str,
    intuition: str,
    formula_or_procedure: str,
    dataframe_view: str,
    code_view: str,
    course_example: str,
    common_mistake: str,
    prerequisites: Iterable[str] = (),
    followups: Iterable[str] = (),
    analogous: Iterable[str] = (),
    keywords: Iterable[str] = (),
    web_refs: Iterable[str] = (),
) -> Concept:
    return Concept(
        node_id=node_id,
        label=label,
        definition=definition,
        intuition=intuition,
        formula_or_procedure=formula_or_procedure,
        dataframe_view=dataframe_view,
        code_view=code_view,
        course_example=course_example,
        common_mistake=common_mistake,
        prerequisites=tuple(prerequisites),
        followups=tuple(followups),
        analogous=tuple(analogous),
        keywords=tuple(keywords),
        web_refs=tuple(web_refs),
    )


PROFILES: tuple[SourceProfile, ...] = (
    SourceProfile(
        route_id="DS_PDF06_VIS",
        folder="DS_PDF01__data_visualization",
        title="DS06 데이터시각화",
        gate="Gate 3 EDA/시각화",
        pdf_name="[Lecture][DS][06][01] 데이터시각화 (3).pdf",
        transcript_name="DS_PDF01__data_visualization__full_transcript.txt",
        one_line="변수 유형과 분석 질문에 맞는 그래프를 고르고, 그래프가 말하는 것과 말하지 못하는 것을 분리한다.",
        graph_location="통계적 분포 이해와 ML 모델링 사이에서 데이터 구조를 눈으로 검증하는 EDA 관문.",
        visual_pages=(
            VisualPage(2, "chart_selection_map", "단변량/이변량/다변량과 변수 유형별 그래프 선택"),
            VisualPage(5, "density_kde", "히스토그램을 부드럽게 해석하는 KDE/밀도 그래프"),
            VisualPage(6, "scatter_plot", "두 양적변수 관계와 상관 해석의 출발점"),
            VisualPage(7, "scatterplot_matrix", "다변량 관계를 여러 산점도 격자로 보는 자료"),
            VisualPage(8, "bubble_plot", "좌표에 세 번째 크기 변수를 추가하는 시각화"),
            VisualPage(10, "box_plot", "중앙값/IQR/이상치 후보를 한 번에 보는 그래프"),
            VisualPage(12, "heatmap", "행렬형 다변량 값과 군집 패턴을 색으로 보는 그래프"),
        ),
        concepts=(
            c("n_DS_VIS.chart_selection", "변수 유형별 그래프 선택", "분석 질문과 변수 타입에 맞춰 단변량/이변량/다변량 그래프를 고르는 판단 규칙이다.", "그래프는 예쁜 그림이 아니라 어떤 비교를 허용할지 정하는 측정 도구다.", "1) 변수 수 확인 2) 변수 타입 확인 3) 분포/관계/구성/비교 중 질문 선택 4) 그래프 선택 5) 해석 한계 표시", "column dtype과 cardinality가 그래프 선택의 입력이다.", "pandas dtype 확인 -> seaborn/ggplot geom 선택 -> 축/색/크기 매핑", "슬라이드 초반의 양적/범주형, 단변량/이변량/다변량 표가 전체 시각화 라우터다.", "범주형 변수에 히스토그램을 쓰거나, 상관을 보여야 하는데 파이차트를 쓰는 오류.", followups=("n_DS_VIS.histogram_kde", "n_DS_VIS.scatter_correlation", "n_DS_VIS.heatmap_multivariate"), keywords=("단변량", "이변량", "다변량", "히스토그램", "산점도", "heatmap")),
            c("n_DS_VIS.histogram_kde", "히스토그램과 KDE", "연속형 또는 순서형 수치 변수의 분포를 구간 빈도 또는 부드러운 밀도로 보는 시각화다.", "값들이 어디에 몰리고 어디가 비어 있는지 보는 지도다.", "histogram: bin별 count/relative frequency. KDE: 각 점 주변 커널을 합쳐 연속 밀도 곡선을 만든다.", "하나의 numeric column이 입력이고, binwidth가 해석을 크게 바꾼다.", "Series.plot.hist, seaborn.histplot, ggplot2 geom_histogram/binwidth", "데이터시각화 PDF의 density plot 페이지가 histogram을 매끈한 곡선으로 해석하는 브릿지다.", "binwidth를 바꿔보지 않고 봉우리 수나 이상치를 단정하는 오류.", prerequisites=("n_DS_VIS.chart_selection",), followups=("n_DS_STATS.frequency_histogram", "n_DS_VIS.boxplot_iqr"), analogous=("n_DS_STATS.distribution_family",), keywords=("Density", "Kernel", "히스토그램", "KDE"), web_refs=("web_ggplot2_histogram",)),
            c("n_DS_VIS.scatter_correlation", "산점도와 관계 해석", "두 양적 변수의 좌표쌍을 점으로 찍어 관계 방향, 형태, 이상치, 군집을 보는 그래프다.", "두 변수가 같이 움직이는지 눈으로 확인하는 첫 번째 도구다.", "x축 변수와 y축 변수를 잡고 패턴이 선형/비선형/무관/군집/이상치인지 판별한다.", "두 numeric columns, 필요하면 hue로 범주형 column을 추가한다.", "plt.scatter, seaborn.scatterplot, ggplot geom_point", "Iris Petal.Length와 Petal.Width 산점도는 변수 관계와 종 분리를 동시에 보여준다.", "상관이 보인다고 인과라고 말하거나, 비선형 관계를 Pearson 상관 하나로 지워버리는 오류.", prerequisites=("n_DS_VIS.chart_selection",), followups=("n_DS_ML1.feature_target_structure", "n_DS_ML2.distance_metrics"), analogous=("n_DS_VIS.bubble_plot",), keywords=("Scatter", "산점도", "Petal.Length", "Petal.Width")),
            c("n_DS_VIS.scatterplot_matrix", "산점도 행렬", "여러 양적 변수 쌍의 산점도를 격자로 배열해 다변량 관계를 한 번에 보는 시각화다.", "변수 둘씩 비교한 작은 산점도들을 모아 관계 지도를 만든다.", "for each pair of numeric variables -> scatter plot cell; diagonal often distribution plot", "여러 numeric columns가 입력이고, hue로 범주 라벨을 겹칠 수 있다.", "pandas.plotting.scatter_matrix, seaborn.pairplot", "데이터시각화 PDF의 scatterplot matrix 페이지가 다변량 관계 탐색 예다.", "행렬을 보고 모든 쌍의 관계가 독립적이라고 생각하거나 다중비교 해석 위험을 무시하는 오류.", prerequisites=("n_DS_VIS.scatter_correlation",), followups=("n_DS_ML1.feature_target_structure",), analogous=("n_DS_VIS.heatmap_multivariate",), keywords=("Scatterplot matrix", "matrix", "다변량")),
            c("n_DS_VIS.bubble_plot", "버블 플롯", "산점도 좌표에 점의 크기를 더해 세 번째 양적 변수를 표현하는 그래프다.", "위치 두 개와 크기 하나를 동시에 읽는 산점도 확장이다.", "x/y 좌표 + size mapping. 면적 인식은 비선형이므로 범위와 legend가 중요하다.", "numeric x, numeric y, numeric size column이 필요하다.", "seaborn.scatterplot(size=...), ggplot aes(size=...)", "시각화 PDF의 Bubble Plot 페이지는 산점도에 크기 차원을 추가하는 예다.", "원의 반지름과 면적을 혼동해서 크기 차이를 과장/축소하는 오류.", prerequisites=("n_DS_VIS.scatter_correlation",), followups=("n_DS_VIS.heatmap_multivariate",), analogous=("n_DS_VIS.scatterplot_matrix",), keywords=("Bubble", "Scatter Plot", "크기")),
            c("n_DS_VIS.boxplot_iqr", "박스플롯/IQR/이상치 후보", "중앙값, 사분위수, IQR, whisker, 이상치 후보를 한 그림에 압축하는 그래프다.", "분포의 가운데와 꼬리를 요약한 압축 프로필이다.", "IQR = Q3 - Q1. 흔한 기준: Q1 - 1.5*IQR보다 작거나 Q3 + 1.5*IQR보다 큰 값을 이상치 후보로 표시.", "numeric column을 범주별 groupby해서 분포를 비교할 수 있다.", "seaborn.boxplot, ggplot geom_boxplot, pandas boxplot", "R/Python PDF의 Iris species별 Petal.Length boxplot과 연결된다.", "박스플롯 점을 자동 삭제해야 하는 진짜 이상치로 단정하는 오류.", prerequisites=("n_DS_STATS.frequency_histogram",), followups=("n_DS_CODE.iris_scatter_boxplot", "n_DS_ML1.preprocessing_leakage"), analogous=("n_DS_VIS.histogram_kde",), keywords=("Box Plot", "boxplots", "IQR", "Petal.Length")),
            c("n_DS_VIS.heatmap_multivariate", "히트맵", "행과 열의 교차값을 색으로 인코딩해 행렬형 패턴을 보는 시각화다.", "큰 표를 색의 지형도로 바꿔 군집과 강도를 빠르게 찾는다.", "matrix/crosstab/correlation table을 만들고 색상 팔레트와 스케일을 지정한다.", "pivot table 또는 correlation matrix가 대표 입력이다.", "pandas.pivot_table/corr -> seaborn.heatmap", "시각화 PDF는 heatmap with dendrogram을 다변량 패턴 탐색 예로 둔다.", "색상 스케일을 확인하지 않고 값 차이를 과해석하는 오류.", prerequisites=("n_DS_VIS.chart_selection",), followups=("n_DS_ML3.clustering_problem", "n_DS_STATS.contingency_table"), analogous=("n_DS_VIS.scatterplot_matrix",), keywords=("Heatmap", "Dendrogram", "heatmap")),
        ),
        local_edges=(
            ("n_DS_VIS.chart_selection", "n_DS_VIS.histogram_kde", "routes_to", "단변량 수치형이면 분포 그래프가 1차 선택이다."),
            ("n_DS_VIS.chart_selection", "n_DS_VIS.scatter_correlation", "routes_to", "이변량 양적-양적 관계는 산점도로 먼저 본다."),
            ("n_DS_VIS.scatter_correlation", "n_DS_VIS.bubble_plot", "extends", "버블 플롯은 산점도에 크기 차원을 추가한다."),
            ("n_DS_VIS.chart_selection", "n_DS_VIS.heatmap_multivariate", "routes_to", "행렬형/다변량 관계는 히트맵으로 압축한다."),
        ),
    ),
    SourceProfile(
        route_id="DS_PDF06_CODE",
        folder="DS_PDF02__r_python",
        title="DS06 R/Python",
        gate="Gate 2 Python/pandas/numpy",
        pdf_name="[Lecture][DS][06][02] RPython (1).pdf",
        transcript_name="DS_PDF02__r_python__full_transcript.txt",
        one_line="컴퓨팅 사고를 데이터프레임 조작, 시각화 코드, sklearn 학습 절차로 번역한다.",
        graph_location="시각화와 머신러닝을 실제 코드 절차로 실행하게 만드는 도구 계층.",
        visual_pages=(
            VisualPage(11, "programming_language", "프로그래밍 언어와 절차적 문제 해결"),
            VisualPage(16, "r_language_intro", "R 언어 특성과 통계 분석 도구 관점"),
            VisualPage(23, "iris_scatter_code", "Iris 산점도 코드 예시"),
            VisualPage(25, "iris_boxplot_code", "Iris boxplot과 factor level 제어"),
            VisualPage(36, "sklearn_intro", "scikit-learn 전처리/회귀/분류/군집/평가 소개"),
            VisualPage(37, "train_test_plot", "train/test와 예측 코드 흐름"),
        ),
        concepts=(
            c("n_DS_CODE.computing_thinking", "컴퓨팅 사고", "문제를 입력, 처리 절차, 출력으로 나누어 컴퓨터가 수행 가능한 단계로 바꾸는 사고방식이다.", "현실 문제를 사람이 읽는 문장 대신 기계가 수행할 명령 순서로 바꾸는 과정이다.", "problem -> input -> algorithm -> output -> validation", "입력은 DataFrame/array, 처리는 함수·조건·반복·집계, 출력은 표/그래프/모델 결과다.", "함수 분해, 반복문, vectorized operation, pipeline", "R/Python PDF의 프로그래밍 입문부가 데이터 분석 코드의 전제다.", "코드를 암기하고 문제 구조를 입력/처리/출력으로 나누지 않는 오류.", followups=("n_DS_CODE.dataframe_row_column", "n_DS_CODE.reproducible_random_state"), keywords=("Programming", "프로그래밍", "명령어", "instructions")),
            c("n_DS_CODE.dataframe_row_column", "DataFrame 행/열 구조", "행은 관측 단위, 열은 변수이며 데이터 분석의 기본 테이블 구조다.", "데이터프레임은 분석 질문을 행과 열로 고정하는 표준 작업대다.", "row=observation, column=variable, X=feature matrix, y=target vector", "각 column의 dtype, missing, cardinality가 전처리와 그래프 선택을 결정한다.", "pd.DataFrame, df.info, df.describe, df.groupby, df.merge", "Iris 데이터의 Petal.Length, Petal.Width, Species가 변수/라벨 구분 예다.", "행 의미와 열 의미를 정하지 않고 바로 모델을 fit하는 오류.", prerequisites=("n_DS_CODE.computing_thinking",), followups=("n_DS_ML1.feature_target_structure", "n_DS_VIS.chart_selection"), keywords=("DataFrame", "row", "column", "Iris"), web_refs=("web_pandas_10min", "web_pandas_groupby")),
            c("n_DS_CODE.iris_scatter_boxplot", "Iris 산점도/박스플롯 코드", "Iris 변수와 Species 라벨을 사용해 관계와 범주별 분포를 시각화하는 코드 예제다.", "같은 데이터를 산점도와 박스플롯으로 보면 관계와 집단 차이가 분리되어 보인다.", "scatter: x=Petal.Length, y=Petal.Width. boxplot: x=Species, y=Petal.Length.", "Petal.Length/Petal.Width는 feature, Species는 grouping label이다.", "ggplot geom_point/geom_boxplot 또는 seaborn.scatterplot/boxplot", "R 예제의 Iris scatter plot과 box plot 페이지가 Gate 3 실습의 핵심 예제다.", "Species 순서, 축 단위, 색상 legend를 확인하지 않는 오류.", prerequisites=("n_DS_CODE.dataframe_row_column",), followups=("n_DS_VIS.scatter_correlation", "n_DS_VIS.boxplot_iqr"), keywords=("Iris", "scatter plot", "box plot", "Petal.Length", "Species")),
            c("n_DS_CODE.sklearn_workflow", "scikit-learn 기본 워크플로", "데이터 전처리, 모델 학습, 예측, 평가를 estimator API로 연결하는 Python ML 절차다.", "데이터프레임에서 모델 결과까지 가는 표준 컨베이어벨트다.", "split -> preprocess/scale -> fit -> predict -> metric -> interpret", "X는 2D feature matrix, y는 1D target vector가 기본이다.", "train_test_split, StandardScaler, estimator.fit, estimator.predict, metrics", "R/Python PDF의 scikit-learn 소개는 ML Part 1~3의 코드 실행 기반이다.", "train/test를 나누지 않고 같은 데이터로 평가하거나, scaler를 전체 데이터에 fit하는 오류.", prerequisites=("n_DS_CODE.dataframe_row_column",), followups=("n_DS_ML1.train_test_generalization", "n_DS_ML2.scaling_distance_models"), keywords=("Scikit-learn", "train", "test", "Training data", "Test data"), web_refs=("web_sklearn_train_test_split", "web_sklearn_preprocessing")),
            c("n_DS_CODE.reproducible_random_state", "재현성/random_state", "무작위 분할·초기화·샘플링 결과를 다시 만들 수 있게 난수 시드를 고정하는 규칙이다.", "같은 실험을 다시 실행해도 비교 가능한 결과가 나오게 하는 잠금장치다.", "random_state or seed 고정 -> split/initialization/sampling 재현 -> 결과 비교 가능", "mock data, train/test split, k-means 초기 중심, bootstrap sample에 적용된다.", "np.random.default_rng, random_state=42", "Python 예제의 train/test 시각화와 k-means 초기점 문제에 모두 연결된다.", "시드를 고정하지 않고 알고리즘 변경 효과와 난수 변동을 섞어 해석하는 오류.", prerequisites=("n_DS_CODE.computing_thinking",), followups=("n_DS_ML1.train_test_generalization", "n_DS_ML3.kmeanspp_local_optimum"), keywords=("random", "n_samples", "train", "test"), web_refs=("web_sklearn_train_test_split",)),
        ),
        local_edges=(
            ("n_DS_CODE.computing_thinking", "n_DS_CODE.dataframe_row_column", "implemented_as", "문제 분해가 행/열 자료구조로 고정된다."),
            ("n_DS_CODE.dataframe_row_column", "n_DS_CODE.iris_scatter_boxplot", "applies_to", "Iris 변수 구조가 시각화 코드의 입력이다."),
            ("n_DS_CODE.dataframe_row_column", "n_DS_CODE.sklearn_workflow", "prerequisite", "sklearn fit/predict는 X/y 구조를 요구한다."),
        ),
    ),
    SourceProfile(
        route_id="DS_PDF07_STATS",
        folder="DS_PDF03__basic_statistics",
        title="DS07 기초통계",
        gate="Gate 1 통계/확률",
        pdf_name="[Lecture][DS][07] 기초통계 (1).pdf",
        transcript_name="DS_PDF03__basic_statistics__full_transcript.txt",
        one_line="표본에서 계산한 통계량으로 모집단 모수를 추론하고, 확률·분포·분할표로 불확실성을 표현한다.",
        graph_location="시각화의 해석 근거이자 ML 평가와 LLM 확률 모델의 수학적 바닥.",
        visual_pages=(
            VisualPage(2, "population_sample_terms", "모집단/표본/모수/통계량 핵심 용어"),
            VisualPage(8, "frequency_distribution", "도수분포표"),
            VisualPage(10, "histogram_frequency", "히스토그램과 상대도수"),
            VisualPage(12, "contingency_table", "두 범주형 변수의 분할표"),
            VisualPage(14, "distribution_overview", "이산/연속 확률분포 개요"),
            VisualPage(15, "bernoulli_trial", "베르누이 시행"),
            VisualPage(55, "bootstrap", "bootstrap 재표본추출"),
        ),
        concepts=(
            c("n_DS_STATS.population_sample_parameter_statistic", "모집단/표본/모수/통계량", "모집단은 관심 대상 전체, 표본은 관측된 일부, 모수는 모집단 값, 통계량은 표본에서 계산한 값이다.", "우리가 가진 작은 표본으로 보이지 않는 전체의 성질을 추정한다.", "sample statistic -> estimate population parameter", "DataFrame은 보통 표본이고, mean/std/value_counts는 통계량이다.", "df.sample, df.mean, df.std", "기초통계 PDF 첫 핵심 용어 페이지가 모든 추론의 출발점이다.", "표본 평균을 모집단 평균 그 자체로 단정하거나 parameter/statistic을 혼동하는 오류.", followups=("n_DS_STATS.statistical_inference", "n_DS_ML1.train_test_generalization"), keywords=("모집단", "Population", "표본", "Sample", "모수", "통계량")),
            c("n_DS_STATS.statistical_inference", "통계적 추론", "표본 자료를 사용해 모집단의 불확실한 성질을 추정·검정하는 과정이다.", "일부 데이터로 전체에 대해 조심스럽게 말하는 규칙이다.", "estimate + uncertainty + assumption check", "표본 크기, 표본추출 방식, 결측/편향이 추론 품질을 좌우한다.", "bootstrap confidence interval, train/test generalization analogy", "bootstrap 페이지가 표본 통계량 변동성을 경험적으로 보는 방법을 제공한다.", "표본이 편향되어도 큰 수면 무조건 괜찮다고 보는 오류.", prerequisites=("n_DS_STATS.population_sample_parameter_statistic",), followups=("n_DS_STATS.bootstrap_imputation", "n_DS_ML1.train_test_generalization"), keywords=("Statistical Inference", "Bootstrap", "표본")),
            c("n_DS_STATS.frequency_histogram", "도수분포/상대도수/히스토그램", "자료를 구간이나 범주로 나누어 빈도와 비율을 정리하고 분포 형태를 보는 방법이다.", "숫자 목록을 분포의 모양으로 접는 과정이다.", "relative frequency = class frequency / total count", "value_counts, cut, groupby count가 도수표를 만든다.", "pd.cut, value_counts(normalize=True), hist", "도수분포와 히스토그램 페이지가 시각화 Gate의 histogram과 직접 연결된다.", "구간폭을 바꾸지 않고 분포 모양을 단정하는 오류.", prerequisites=("n_DS_STATS.population_sample_parameter_statistic",), followups=("n_DS_VIS.histogram_kde", "n_DS_STATS.distribution_family"), keywords=("도수분포", "Frequency", "Histogram", "상대도수")),
            c("n_DS_STATS.probability_random_variable", "확률/확률변수", "불확실한 사건의 가능성을 수로 표현하고, 확률변수는 실험 결과를 숫자로 대응시킨 변수다.", "불확실한 현실을 계산 가능한 숫자 규칙으로 바꾸는 언어다.", "0 <= P(A) <= 1, random variable X maps outcomes to values", "row는 실현값, column은 확률변수의 관측값으로 볼 수 있다.", "numpy random variables, scipy distributions", "확률분포 개요와 베르누이 시행이 discrete/continuous 모델의 출발점이다.", "관측 비율과 이론 확률을 같은 수준의 확정값으로 혼동하는 오류.", prerequisites=("n_DS_STATS.population_sample_parameter_statistic",), followups=("n_DS_STATS.conditional_independence", "n_DS_LLM.sequence_probability"), keywords=("확률", "확률변수", "Bernoulli", "distribution")),
            c("n_DS_STATS.conditional_independence", "조건부확률과 독립", "조건부확률은 B가 주어졌을 때 A의 확률이고, 독립은 B 정보가 A의 확률을 바꾸지 않는 상태다.", "이미 알고 있는 정보가 판단을 바꾸는지 확인하는 규칙이다.", "P(A|B)=P(A∩B)/P(B). independent if P(A|B)=P(A) or P(A∩B)=P(A)P(B).", "crosstab의 행/열 조건부 비율로 계산할 수 있다.", "pd.crosstab(..., normalize='index')", "분할표 페이지와 LLM의 다음 토큰 조건부 확률이 같은 확률 언어로 연결된다.", "P(A|B)와 P(B|A)를 바꿔 쓰거나, 상관/동시발생을 독립 위반의 원인으로 과해석하는 오류.", prerequisites=("n_DS_STATS.probability_random_variable",), followups=("n_DS_STATS.contingency_table", "n_DS_LLM.sequence_probability"), keywords=("conditional", "independent", "분할표", "Contingency"), web_refs=("web_pandas_groupby",)),
            c("n_DS_STATS.distribution_family", "이산/연속 확률분포", "확률변수가 가질 수 있는 값과 그 가능성을 체계적으로 나타낸 모델군이다.", "데이터가 어떤 모양으로 나올지 미리 정한 지도다.", "Discrete: Bernoulli/Binomial/Poisson. Continuous: density over intervals.", "column 값의 domain과 dtype이 분포 가정을 제한한다.", "scipy.stats, histogram/KDE, empirical distribution", "확률분포 슬라이드가 베르누이·이항·포아송 등을 한 계열로 묶는다.", "분포 이름을 외우고 적용 조건을 확인하지 않는 오류.", prerequisites=("n_DS_STATS.probability_random_variable",), followups=("n_DS_ML1.loss_metric", "n_DS_LLM.ngram_language_model"), analogous=("n_DS_VIS.histogram_kde",), keywords=("확률분포", "Bernoulli", "Binomial", "Poisson", "continuous")),
            c("n_DS_STATS.contingency_table", "분할표", "두 범주형 변수의 조합 빈도를 2차원 표로 정리한 자료 구조다.", "범주 A와 범주 B가 같이 나타나는 패턴을 표로 보는 방법이다.", "cell count, row proportion, column proportion, expected count", "두 categorical columns를 crosstab한다.", "pd.crosstab(row_col, col_col, normalize=...)", "기초통계 PDF의 contingency table은 연관분석 support/confidence/lift의 선행 구조다.", "행비율과 열비율을 혼동해 조건부확률 방향을 바꾸는 오류.", prerequisites=("n_DS_STATS.conditional_independence",), followups=("n_DS_ML3.association_rule",), keywords=("Contingency", "분할표", "범주형")),
            c("n_DS_STATS.bootstrap_imputation", "Bootstrap과 Imputation", "Bootstrap은 표본을 복원추출해 통계량 변동성을 추정하고, imputation은 결측값을 분석 가능한 값으로 채운다.", "부족하거나 빠진 데이터에서 불확실성을 다루는 두 가지 실무 도구다.", "bootstrap: resample with replacement -> compute statistic repeatedly. imputation: fill missing by rule/model.", "결측 컬럼과 표본 행을 기준으로 처리한다.", "sklearn SimpleImputer/KNNImputer, sklearn.utils.resample", "기초통계 후반부의 bootstrap, bagging, imputation은 ML ensemble/전처리와 이어진다.", "결측을 무조건 평균으로 채우거나 bootstrap 결과를 원자료 증가로 오해하는 오류.", prerequisites=("n_DS_STATS.statistical_inference",), followups=("n_DS_ML1.preprocessing_leakage", "n_DS_ML3.kmeanspp_local_optimum"), keywords=("Bootstrap", "Bagging", "Imputation", "결측치")),
        ),
    ),
    SourceProfile(
        route_id="DS_PDF08_ML1",
        folder="DS_PDF04__machine_learning_part_1",
        title="DS08 머신러닝 Part 1",
        gate="Gate 4 지도학습",
        pdf_name="[Lecture][DS][08][01] 머신러닝_Part_1 (2).pdf",
        transcript_name="DS_PDF04__machine_learning_part_1__full_transcript.txt",
        one_line="현실 문제를 X/y 데이터 구조로 바꾸고, 분류/회귀/비지도학습과 학습·평가 절차를 판별한다.",
        graph_location="통계/시각화에서 모델 선택으로 넘어가는 지도학습 입구.",
        visual_pages=(
            VisualPage(2, "ml_intro", "머신러닝 정의와 학습 유형 도입"),
            VisualPage(8, "supervised_unsupervised", "지도/비지도/강화학습 비교"),
            VisualPage(15, "train_test_structure", "학습/검증 데이터 구조"),
            VisualPage(41, "classification_intro", "분류 문제 정의"),
            VisualPage(47, "logistic_regression_logit", "로지스틱 회귀 logit 구조"),
            VisualPage(54, "multiclass_classification", "다중분류 확장"),
        ),
        concepts=(
            c("n_DS_ML1.feature_target_structure", "X/y feature-target 구조", "feature matrix X와 target vector y로 예측 문제를 표현하는 데이터 구조다.", "무엇을 근거로 무엇을 맞힐지 분리하는 모델링의 시작점이다.", "X = rows x features, y = label/target for each row", "feature columns와 target column을 분리한다.", "X = df[features]; y = df[target]", "ML Part 1은 classification/regression 모두 X/y 구조로 읽어야 한다.", "target을 feature에 섞어 target leakage를 만드는 오류.", prerequisites=("n_DS_CODE.dataframe_row_column",), followups=("n_DS_ML1.classification_regression", "n_DS_ML1.train_test_generalization"), keywords=("feature", "target", "classification", "regression", "label")),
            c("n_DS_ML1.learning_types", "지도/비지도/강화학습", "지도학습은 정답 y가 있고, 비지도학습은 구조를 찾고, 강화학습은 보상으로 행동 정책을 학습한다.", "정답이 있느냐, 구조를 찾느냐, 행동을 개선하느냐로 문제를 나눈다.", "supervised: f(X)->y. unsupervised: structure(X). reinforcement: policy maximizing reward.", "target column 유무가 지도/비지도 판별의 핵심이다.", "Classifier/Regressor, clustering, RL environment", "ML Part 1의 학습 유형 표가 Gate 4/5 라우터다.", "군집 결과를 정답 라벨처럼 평가하거나, target 없는 문제에 accuracy를 쓰는 오류.", prerequisites=("n_DS_ML1.feature_target_structure",), followups=("n_DS_ML3.clustering_problem",), keywords=("supervised", "unsupervised", "reinforcement", "지도", "비지도")),
            c("n_DS_ML1.train_test_generalization", "Train/Test split과 일반화", "학습에 쓴 데이터와 평가 데이터를 분리해 새 데이터 성능을 추정하는 검증 절차다.", "외운 성적과 실전 성적을 분리해서 보는 장치다.", "split data -> fit on train -> predict on test -> metric on test", "행 단위로 분할하되 시간/그룹 누수 여부를 확인한다.", "train_test_split(X, y, test_size=..., random_state=...)", "R/Python PDF의 train/test 시각화와 ML Part 1 평가 흐름이 연결된다.", "전처리나 feature selection을 split 전에 전체 데이터로 fit하는 leakage 오류.", prerequisites=("n_DS_CODE.sklearn_workflow", "n_DS_STATS.statistical_inference"), followups=("n_DS_ML1.loss_metric", "n_DS_ML2.scaling_distance_models"), keywords=("train", "test", "Training", "Test", "accuracy"), web_refs=("web_sklearn_train_test_split",)),
            c("n_DS_ML1.preprocessing_leakage", "전처리와 leakage", "결측치 대체, scaling, 이상치 판단, feature selection 같은 전처리는 train/test 경계를 지키며 학습 데이터 기준으로 fit해야 한다.", "시험지 답을 미리 보고 공부하지 않도록 데이터 처리 순서를 잠그는 규칙이다.", "split first -> fit preprocessing on train -> transform train/test -> fit model -> evaluate", "missing/outlier/scaler statistics are learned from train rows only.", "Pipeline([('preprocess', ...), ('model', ...)]), SimpleImputer, StandardScaler", "boxplot의 이상치 후보, bootstrap/imputation, scaling 민감도가 모두 이 leakage 규칙으로 연결된다.", "전체 데이터로 평균/표준편차/결측 대체값을 계산한 뒤 split하는 오류.", prerequisites=("n_DS_ML1.train_test_generalization", "n_DS_STATS.bootstrap_imputation"), followups=("n_DS_ML2.scaling_distance_models", "n_DS_ML3.kmeans_centroid_loop"), keywords=("train", "test", "preprocessing", "Imputation", "scale"), web_refs=("web_sklearn_preprocessing", "web_sklearn_train_test_split")),
            c("n_DS_ML1.classification_regression", "분류와 회귀", "target이 범주형이면 분류, 연속형이면 회귀로 푸는 지도학습 문제 유형이다.", "무엇을 맞히는지가 이름표인지 숫자인지 구분하는 문제 라우터다.", "classification predicts class label/probability; regression predicts continuous value.", "target dtype과 의미를 확인한다.", "Classifier vs Regressor estimator 선택", "ML Part 1의 logistic regression/classification 슬라이드가 범주형 target의 대표 예다.", "숫자 코드로 저장된 범주형 target을 회귀로 착각하는 오류.", prerequisites=("n_DS_ML1.feature_target_structure",), followups=("n_DS_ML2.svm_margin_hyperplane", "n_DS_ML2.knn_vote"), keywords=("Classification", "Regression", "category", "class")),
            c("n_DS_ML1.loss_metric", "Loss/Cost와 평가 지표", "loss는 학습 중 줄이는 오류 함수이고, metric은 모델 성능을 해석하기 위한 평가 함수다.", "모델이 무엇을 줄이려고 학습했는지와 우리가 무엇으로 판단할지를 분리한다.", "fit minimizes training objective; test metric evaluates task performance. Confusion matrix에서 Accuracy=(TP+TN)/N, Precision=TP/(TP+FP), Recall=TP/(TP+FN), F1=2PR/(P+R).", "y_true/y_pred를 비교해 accuracy, precision, recall, RMSE 등을 계산한다.", "sklearn.metrics, model.score, confusion_matrix, precision_recall_fscore_support", "ML Part 1의 prediction/loss/accuracy 흐름이 Gate 4 통과 기준이며, churn 같은 불균형 문제는 recall/F1로 확장해야 한다.", "loss가 낮으면 모든 비즈니스 판단이 좋다고 단정하거나, 불균형 데이터에서 accuracy만 보는 오류.", prerequisites=("n_DS_ML1.train_test_generalization",), followups=("n_DS_ML2.svm_margin_hyperplane", "n_DS_ML2.knn_vote", "n_DS_ML2.decision_tree_impurity"), keywords=("loss", "cost", "accuracy", "prediction", "metric"), web_refs=("web_sklearn_confusion_metrics",)),
            c("n_DS_ML1.logistic_logit_probability", "로지스틱 회귀와 logit", "선형 점수를 확률로 바꿔 class 1에 속할 가능성을 예측하는 분류 모델이다.", "직선 점수를 0과 1 사이의 확률 언어로 변환한다.", "odds = p/(1-p), logit(p)=log(p/(1-p)), p=sigmoid(w^T x+b)", "X feature row별 class probability를 예측한다.", "LogisticRegression.fit, predict_proba, threshold", "ML Part 1 후반 logistic regression 슬라이드가 p, odds, logit 연결을 설명한다.", "로지스틱 회귀를 연속값 회귀 모델로 해석하거나 threshold를 고정 진리로 보는 오류.", prerequisites=("n_DS_ML1.classification_regression", "n_DS_STATS.probability_random_variable"), followups=("n_DS_ML2.svm_margin_hyperplane",), keywords=("Logistic", "Odds", "logit", "probability")),
            c("n_DS_ML1.text_vectorization_features", "텍스트 벡터화", "문자열 문서를 모델이 계산할 수 있는 수치 feature로 바꾸는 표현 변환이다.", "말을 숫자 좌표로 바꾸어 거리·분류·확률 모델에 넣는다.", "text -> tokenization -> count/TF-IDF/embedding -> feature vector", "각 row는 문서, 각 column은 토큰/임베딩 차원이다.", "CountVectorizer, TfidfVectorizer, embedding model", "ML Part 1의 text vectorization은 DS09 LLM의 embedding/pre-training으로 이어진다.", "텍스트 원문을 모델이 그대로 이해한다고 생각하거나, 벡터화 기준을 train/test 밖에서 섞는 오류.", prerequisites=("n_DS_ML1.feature_target_structure",), followups=("n_DS_LLM.embedding_contextual_representation",), keywords=("text", "vectorization", "TF", "token")),
        ),
    ),
    SourceProfile(
        route_id="DS_PDF08_ML2",
        folder="DS_PDF05__machine_learning_part_2",
        title="DS08 머신러닝 Part 2",
        gate="Gate 5 알고리즘 심화",
        pdf_name="[Lecture][DS][08][02] 머신러닝_Part_2 (1).pdf",
        transcript_name="DS_PDF05__machine_learning_part_2__full_transcript.txt",
        one_line="SVM은 margin을 키우고, kNN은 거리 기반 이웃 투표로 예측한다. 둘 다 feature scaling과 거리 해석이 핵심이다.",
        graph_location="지도학습 알고리즘의 기하학적 해석 계층.",
        visual_pages=(
            VisualPage(4, "svm_margin", "SVM margin과 결정경계"),
            VisualPage(5, "support_vectors", "support vector와 margin 결정 관측치"),
            VisualPage(6, "optimal_hyperplane", "최대 margin hyperplane"),
            VisualPage(9, "kernel_svm", "비선형 SVM과 kernel 함수"),
            VisualPage(16, "knn_distance_metrics", "kNN 거리 척도"),
            VisualPage(17, "knn_scaling", "거리 기반 모델의 scale 민감도"),
            VisualPage(19, "knn_classification_regression", "kNN 분류/회귀 사용"),
            VisualPage(21, "knn_majority_voting", "majority voting 문제점"),
        ),
        concepts=(
            c("n_DS_ML2.svm_margin_hyperplane", "SVM margin/hyperplane", "SVM은 클래스 사이의 margin이 최대가 되는 hyperplane을 찾는 분류 알고리즘이다.", "두 집단 사이에 가능한 한 넓은 안전지대를 만드는 경계선을 찾는다.", "maximize margin subject to correct/soft-margin classification constraints", "각 row는 feature 공간의 점이고 class label이 경계 학습에 쓰인다.", "SVC(kernel='linear'), LinearSVC, decision_function", "ML Part 2 첫 SVM 페이지가 margin과 결정경계의 기하를 보여준다.", "SVM이 확률을 직접 예측한다고 보거나 margin과 accuracy를 같은 값으로 보는 오류.", prerequisites=("n_DS_ML1.classification_regression",), followups=("n_DS_ML2.support_vectors", "n_DS_ML2.kernel_trick"), keywords=("Support Vector Machine", "마진", "margin", "hyperplane"), web_refs=("web_sklearn_svm",)),
            c("n_DS_ML2.support_vectors", "Support vectors", "결정경계와 가장 가까워 margin 위치를 결정하는 관측치들이다.", "경계를 실제로 밀고 있는 핵심 점들이다.", "support vectors lie on/inside margin and determine separating boundary", "일부 row가 boundary를 결정하는 큰 영향점을 가진다.", "model.support_vectors_, support_", "SVM support vector 페이지는 margin 결정 관측치를 명시한다.", "모든 관측치가 경계를 똑같이 결정한다고 보는 오류.", prerequisites=("n_DS_ML2.svm_margin_hyperplane",), followups=("n_DS_ML2.kernel_trick",), keywords=("Support vectors", "서포트 벡터", "Margin")),
            c("n_DS_ML2.kernel_trick", "Kernel trick", "원래 공간에서 선형 분리가 어려운 데이터를 고차원 특징공간의 내적처럼 계산해 비선형 경계를 만드는 방법이다.", "직선으로 나누기 어려우면 공간을 접거나 펼쳐서 직선처럼 나누는 효과를 낸다.", "K(x_i,x_j)=phi(x_i)^T phi(x_j), e.g. RBF/poly kernels", "feature scale과 kernel parameter가 경계 복잡도를 좌우한다.", "SVC(kernel='rbf'), gamma, C", "비선형 SVM 페이지가 kernel을 사용한 비선형 결정경계를 보여준다.", "kernel을 데이터 전처리 없이 마법처럼 쓰면 된다고 보는 오류.", prerequisites=("n_DS_ML2.svm_margin_hyperplane", "n_DS_ML2.scaling_distance_models"), followups=("n_DS_ML3.pca_dimensionality_reduction",), keywords=("Kernel", "비선형", "SVM"), web_refs=("web_sklearn_svm",)),
            c("n_DS_ML2.knn_vote", "kNN 이웃 투표", "새 관측치와 가장 가까운 k개 학습 관측치의 label을 기준으로 분류 또는 회귀를 수행한다.", "가까운 사례들이 무엇이었는지 보고 새 사례를 판단한다.", "classification: majority vote among k nearest labels. regression: average neighbor targets.", "모든 feature가 거리 계산에 들어가므로 열의 스케일과 의미가 중요하다.", "KNeighborsClassifier, KNeighborsRegressor, kneighbors", "kNN 페이지는 범주형 반응변수와 연속형 반응변수 모두에 쓰임을 설명한다.", "k를 정답처럼 고정하거나, class imbalance를 고려하지 않는 오류.", prerequisites=("n_DS_ML1.classification_regression", "n_DS_ML2.distance_metrics"), followups=("n_DS_ML2.k_selection_bias_variance",), keywords=("k-nearest", "k-NN", "Majority voting", "classification"), web_refs=("web_sklearn_neighbors",)),
            c("n_DS_ML2.distance_metrics", "거리 척도", "두 관측치가 feature 공간에서 얼마나 가까운지 수치화하는 함수다.", "비슷함을 숫자로 재는 자다.", "Euclidean, Manhattan, Minkowski, cosine distance/similarity", "numeric columns가 같은 단위와 의미를 갖는지 확인해야 한다.", "pairwise_distances, metric='euclidean'/'manhattan'/'cosine'", "kNN 거리 페이지와 k-means 거리 페이지가 같은 수학 언어를 공유한다.", "단위가 큰 변수가 거리 전체를 지배하게 두는 오류.", prerequisites=("n_DS_VIS.scatter_correlation",), followups=("n_DS_ML2.scaling_distance_models", "n_DS_ML3.kmeans_distance_metrics"), keywords=("Euclidean", "Manhattan", "Minkowski", "Cosine", "distance")),
            c("n_DS_ML2.scaling_distance_models", "Scaling과 거리 기반 모델", "feature의 단위와 범위를 맞춰 거리·margin·gradient 계산이 특정 변수에 과도하게 끌리지 않게 하는 전처리다.", "센티미터와 원화를 같은 자로 재지 않도록 단위를 맞추는 과정이다.", "z=(x-mean)/std or minmax scaling before distance-sensitive estimator", "train set에 scaler를 fit하고 train/test에 transform한다.", "StandardScaler, MinMaxScaler, Pipeline", "kNN scale 민감도 페이지는 변수 scale이 거리 결과를 바꾸는 위험을 보여준다.", "전체 데이터로 scaler를 fit해 test 정보를 누수시키는 오류.", prerequisites=("n_DS_ML2.distance_metrics", "n_DS_ML1.train_test_generalization"), followups=("n_DS_ML2.knn_vote", "n_DS_ML3.kmeans_centroid_loop"), keywords=("scale", "scaling", "distance", "StandardScaler"), web_refs=("web_sklearn_preprocessing",)),
            c("n_DS_ML2.k_selection_bias_variance", "k 선택과 bias-variance", "kNN의 k는 이웃 수로, 작으면 노이즈에 민감하고 크면 경계가 과도하게 매끈해진다.", "동네 몇 명의 의견을 들을지 정하는 문제다.", "small k: low bias/high variance; large k: high bias/low variance", "validation set/cross-validation으로 k 후보를 비교한다.", "GridSearchCV over n_neighbors", "majority voting 문제점 페이지가 k와 class composition의 민감도를 암시한다.", "k를 홀수로만 고르면 문제가 해결된다고 보는 오류.", prerequisites=("n_DS_ML2.knn_vote",), followups=("n_DS_ML3.silhouette_score",), keywords=("Majority voting", "kNN", "k", "neighbors"), web_refs=("web_sklearn_neighbors",)),
            c("n_DS_ML2.decision_tree_impurity", "Decision tree와 impurity", "의사결정나무는 feature 조건 질문을 반복해 target을 분리하고, 각 split은 impurity를 낮추는 방향으로 선택된다.", "스무고개식 질문으로 데이터를 점점 순수한 그룹으로 나누는 규칙 기반 모델이다.", "choose split that maximizes impurity decrease; common criteria include gini impurity and entropy. Control overfitting with max_depth, min_samples_leaf, pruning-style constraints.", "row는 규칙을 따라 leaf로 내려가고, leaf의 class 비율이 예측 근거가 된다.", "DecisionTreeClassifier(max_depth=...), export_text, plot_tree", "ML2 PDF의 decision tree 페이지를 1차 근거로 두고, impurity/depth/pruning 실무 해석은 scikit-learn 문서로 보강한다.", "tree는 scaling 영향이 작다고 해서 depth/leaf 제약 없이 키워도 된다고 보는 오류.", prerequisites=("n_DS_ML1.classification_regression", "n_DS_ML1.loss_metric"), followups=("n_DS_ML3.kmeanspp_local_optimum",), analogous=("n_DS_ML2.svm_margin_hyperplane", "n_DS_ML2.knn_vote"), keywords=("Decision Tree", "decision tree", "impurity", "gini", "entropy", "pruning"), web_refs=("web_sklearn_tree",)),
        ),
        local_edges=(
            ("n_DS_ML2.svm_margin_hyperplane", "n_DS_ML2.support_vectors", "determined_by", "support vector가 margin 위치를 결정한다."),
            ("n_DS_ML2.svm_margin_hyperplane", "n_DS_ML2.kernel_trick", "extends", "kernel은 선형 margin 개념을 비선형 경계로 확장한다."),
            ("n_DS_ML2.distance_metrics", "n_DS_ML2.knn_vote", "operationalizes", "kNN은 거리로 이웃을 고른다."),
            ("n_DS_ML2.scaling_distance_models", "n_DS_ML2.knn_vote", "prevents_error", "scaling은 거리 기반 투표 왜곡을 줄인다."),
            ("n_DS_ML2.decision_tree_impurity", "n_DS_ML2.knn_vote", "contrasts_with", "tree는 규칙 기반, kNN은 거리 기반이다."),
        ),
    ),
    SourceProfile(
        route_id="DS_PDF08_ML3",
        folder="DS_PDF06__machine_learning_part_3",
        title="DS08 머신러닝 Part 3",
        gate="Gate 5 알고리즘 심화",
        pdf_name="[Lecture][DS][08][03] 머신러닝_Part_3.pdf",
        transcript_name="DS_PDF06__machine_learning_part_3__full_transcript.txt",
        one_line="군집은 target 없이 구조를 찾고, 연관분석은 거래 안 동시출현 규칙을 support/confidence/lift로 평가한다.",
        graph_location="비지도학습과 패턴 발견을 묶는 구조 탐색 계층.",
        visual_pages=(
            VisualPage(5, "kmeans_problem", "거리 기반 k-means 군집 문제"),
            VisualPage(16, "spherical_kmeans", "cosine 기반 spherical k-means"),
            VisualPage(17, "euclidean_cosine", "Euclidean distance와 cosine similarity"),
            VisualPage(20, "kmeans_limitations", "initial point와 k-means++"),
            VisualPage(35, "association_metrics", "support/confidence/lift 평가 기준"),
            VisualPage(36, "support_formula", "support 정의"),
            VisualPage(37, "confidence_formula", "confidence 정의"),
            VisualPage(38, "lift_formula", "lift 정의"),
            VisualPage(42, "association_example", "support/confidence/lift 계산 예제"),
        ),
        concepts=(
            c("n_DS_ML3.clustering_problem", "Clustering 문제정의", "target 없이 관측치들 사이의 유사성으로 묶음을 찾는 비지도학습 문제다.", "정답 이름표 없이 데이터가 자연스럽게 모이는 방을 찾는다.", "input X only -> similarity/distance -> cluster labels", "feature matrix만 사용하며 y는 없다.", "KMeans.fit_predict(X), clustering labels", "ML Part 3는 k-means를 중심으로 비지도학습의 거리 기반 구조 탐색을 설명한다.", "cluster label을 실제 class label처럼 곧바로 해석하는 오류.", prerequisites=("n_DS_ML1.learning_types", "n_DS_ML2.distance_metrics"), followups=("n_DS_ML3.kmeans_centroid_loop",), keywords=("clustering", "군집", "k-means", "distance"), web_refs=("web_sklearn_kmeans",)),
            c("n_DS_ML3.kmeans_centroid_loop", "k-means centroid loop", "각 점을 가장 가까운 centroid에 배정하고, 각 군집 평균으로 centroid를 갱신하는 반복 알고리즘이다.", "중심을 놓고 점을 배정한 뒤, 다시 중심을 옮기는 과정을 멈출 때까지 반복한다.", "assign x_i to nearest mu_j -> update mu_j = mean(points in cluster j) -> repeat", "numeric scaled feature matrix가 입력이다.", "KMeans(n_clusters=k, init='k-means++').fit(X)", "k-means PDF 초반은 거리와 centroid 기반 군집을 설명한다.", "centroid가 반드시 실제 데이터 점이라고 오해하는 오류.", prerequisites=("n_DS_ML3.clustering_problem", "n_DS_ML2.scaling_distance_models"), followups=("n_DS_ML3.kmeanspp_local_optimum", "n_DS_ML3.silhouette_score"), keywords=("centroid", "k-means", "Euclidean", "Cosine"), web_refs=("web_sklearn_kmeans",)),
            c("n_DS_ML3.kmeans_distance_metrics", "k-means 거리 척도", "k-means에서 가까움을 정의하는 Euclidean/cosine/p-norm 계열의 거리 선택 문제다.", "무엇을 비슷하다고 볼지 정하는 군집의 언어다.", "Euclidean norm, cosine similarity, p-norm variants", "feature scaling과 sparse/text representation 여부가 거리 선택을 바꾼다.", "sklearn KMeans는 기본 Euclidean, cosine은 별도 spherical 접근 필요", "PDF는 spherical k-means와 Euclidean/Cosine 비교를 직접 다룬다.", "scikit-learn KMeans에서 metric만 바꾸면 cosine k-means가 된다고 착각하는 오류.", prerequisites=("n_DS_ML2.distance_metrics",), followups=("n_DS_LLM.embedding_contextual_representation",), keywords=("Spherical", "Cosine", "Euclidean", "p-norm", "metric"), web_refs=("web_sklearn_kmeans",)),
            c("n_DS_ML3.kmeanspp_local_optimum", "k-means++와 local optimum", "k-means는 초기 centroid에 따라 지역 최적해에 수렴할 수 있어 k-means++로 좋은 초기점을 고른다.", "처음 중심을 어디에 놓느냐가 최종 방 배치를 바꿀 수 있다.", "repeat with different seeds; k-means++ spreads initial centroids apart", "random_state와 n_init으로 반복 안정성을 관리한다.", "KMeans(init='k-means++', n_init='auto', random_state=...)", "limitations 페이지는 initial points 문제와 k-means++를 명시한다.", "한 번 실행한 군집 결과를 전역 최적해로 단정하는 오류.", prerequisites=("n_DS_ML3.kmeans_centroid_loop", "n_DS_CODE.reproducible_random_state"), followups=("n_DS_ML3.silhouette_score",), keywords=("Initial points", "k-means++", "local", "centroid"), web_refs=("web_sklearn_kmeans",)),
            c("n_DS_ML3.silhouette_score", "Silhouette score", "한 점이 자기 군집에는 얼마나 가깝고 다른 군집과는 얼마나 떨어져 있는지 비교하는 군집 품질 지표다.", "같은 방 안에서는 가까운지, 옆방과는 충분히 떨어졌는지 보는 점수다.", "s = (b - a) / max(a, b); a=intra-cluster distance, b=nearest other-cluster distance", "X와 cluster labels가 입력이며 label 수 조건을 확인한다.", "silhouette_score(X, labels, metric='euclidean')", "PDF에 직접 없거나 약하게 나온 경우 scikit-learn 문서로 보강하는 평가 노드다.", "silhouette이 높으면 항상 비즈니스적으로 좋은 군집이라고 단정하는 오류.", prerequisites=("n_DS_ML3.kmeanspp_local_optimum",), followups=("n_DS_ML3.pca_dimensionality_reduction",), keywords=("silhouette", "cluster", "score"), web_refs=("web_sklearn_silhouette",)),
            c("n_DS_ML3.association_rule", "연관 규칙", "거래 데이터에서 A가 발생할 때 B가 함께 발생하는 패턴을 if-then 규칙으로 표현하는 방법이다.", "장바구니 안에서 같이 등장하는 항목 조합을 규칙으로 찾는다.", "X -> Y over transactions; evaluate by support, confidence, lift", "row=transaction, columns/items=0/1 item presence", "mlxtend frequent_patterns or custom crosstab over itemsets", "Association Analysis 페이지가 연관 규칙과 평가 기준을 설명한다.", "동시출현 규칙을 인과관계로 해석하는 오류.", prerequisites=("n_DS_STATS.contingency_table",), followups=("n_DS_ML3.support_confidence_lift",), keywords=("Association", "연관성", "Rule", "transaction"), web_refs=("web_agrawal_srikant_1994",)),
            c("n_DS_ML3.support_confidence_lift", "Support/Confidence/Lift", "support는 규칙 항목이 전체 거래에서 나타난 비율, confidence는 조건 발생 시 결과 발생 비율, lift는 독립 대비 동시출현 강도다.", "자주 나오나, 조건이 믿을 만한가, 우연보다 강한가를 분리해서 묻는다.", "support(X->Y)=P(X∩Y), confidence=P(Y|X), lift=P(X∩Y)/(P(X)P(Y))", "transaction-item matrix에서 itemset 빈도를 계산한다.", "itemset counts -> support/confidence/lift table", "PDF 후반의 지지도/신뢰도/향상도 계산 예제가 이 노드의 수치 훈련 자료다.", "confidence가 높아도 Y가 원래 흔하면 의미를 과대평가하는 오류.", prerequisites=("n_DS_ML3.association_rule", "n_DS_STATS.conditional_independence"), followups=("n_DS_LLM.rag_grounding",), keywords=("support", "confidence", "lift", "지지도", "신뢰도", "향상도"), web_refs=("web_agrawal_srikant_1994",)),
            c("n_DS_ML3.pca_dimensionality_reduction", "PCA/차원축소", "상관된 여러 feature를 분산이 큰 직교 축으로 변환해 저차원 표현을 만드는 기법이다.", "많은 변수를 정보 손실을 관리하며 몇 개의 축으로 압축하는 표현 변환이다.", "center X -> covariance/SVD -> principal components -> transformed coordinates", "numeric scaled feature matrix가 입력이며 explained variance를 확인한다.", "PCA(n_components=...), fit_transform, explained_variance_ratio_", "PCA는 PDF 직접 핵심 노드가 약하므로 ML/EDA 확장 지식으로 보강한다.", "PCA를 target을 맞히는 예측 모델로 오해하거나 scale 없이 적용하는 오류.", prerequisites=("n_DS_ML2.scaling_distance_models", "n_DS_ML3.kmeans_distance_metrics"), followups=("n_DS_LLM.embedding_contextual_representation",), keywords=("PCA", "dimension", "차원", "variance"), web_refs=("web_sklearn_pca", "web_sklearn_kmeans")),
        ),
    ),
    SourceProfile(
        route_id="DS_PDF09_LLM",
        folder="DS_PDF07__language_models_llm",
        title="DS09 언어모델과 LLM",
        gate="Gate 6 NLP/LLM",
        pdf_name="[Lecture][DS][09]언어모델과 LLM.pdf",
        transcript_name="DS_PDF07__language_models_llm__full_transcript.txt",
        one_line="언어모델은 다음 토큰 확률을 학습하고, Transformer/사전학습/Instruction tuning/RAG로 지시 수행형 LLM까지 확장된다.",
        graph_location="확률·벡터화·딥러닝·검색근거를 하나로 묶는 최종 응용 계층.",
        visual_pages=(
            VisualPage(3, "lm_history", "규칙기반에서 LLM까지 언어모델 발전사"),
            VisualPage(4, "embedding_encoder_decoder", "embedding/encoder/decoder 기본 용어"),
            VisualPage(7, "conditional_probability_lm", "조건부 확률 기반 언어모델"),
            VisualPage(22, "nnlm_structure", "NNLM 구조"),
            VisualPage(35, "seq2seq", "encoder-decoder seq2seq"),
            VisualPage(37, "gpt_decoder", "GPT decoder-only 다음 단어 예측"),
            VisualPage(38, "large_language_model", "Transformer 기반 LLM과 foundation model"),
            VisualPage(39, "instruction_tuning", "instruction tuning 예시"),
        ),
        concepts=(
            c("n_DS_LLM.sequence_probability", "언어모델과 문장 확률", "언어모델은 단어/토큰 시퀀스의 가능도와 다음 토큰의 조건부 확률을 모델링한다.", "문장이 자연스럽게 이어질 가능성을 확률로 계산한다.", "P(w1...wn)=product P(w_t | context)", "row=document/sentence, column/token sequence or vectorized representation", "tokenizer -> model logits -> softmax probabilities", "LLM PDF의 조건부 확률 페이지가 통계 Gate와 직접 연결된다.", "LLM이 검색엔진처럼 사실을 조회한다고 생각하고 확률 생성 구조를 무시하는 오류.", prerequisites=("n_DS_STATS.conditional_independence",), followups=("n_DS_LLM.ngram_language_model", "n_DS_LLM.attention_transformer"), keywords=("Language Model", "conditional probability", "조건부 확률", "단어")),
            c("n_DS_LLM.ngram_language_model", "N-gram 통계적 언어모델", "앞의 n-1개 단어를 조건으로 다음 단어 확률을 추정하는 통계적 언어모델이다.", "가까운 몇 단어만 보고 다음 단어를 예측하는 빈도 기반 모델이다.", "P(w_t | w_{t-n+1},...,w_{t-1}) estimated from counts", "텍스트를 n-gram count table로 바꾼다.", "CountVectorizer(ngram_range=...), frequency table", "언어모델 발전사에서 통계적 언어모델이 신경망/Transformer 이전 단계로 제시된다.", "n이 커지면 항상 좋아진다고 보고 sparse data 문제를 무시하는 오류.", prerequisites=("n_DS_LLM.sequence_probability", "n_DS_STATS.frequency_histogram"), followups=("n_DS_LLM.embedding_contextual_representation",), keywords=("N-gram", "Statistical Language Model", "빈도")),
            c("n_DS_LLM.embedding_contextual_representation", "Embedding과 문맥 표현", "토큰을 계산 가능한 연속 벡터로 바꾸고 문맥에 따라 의미 표현을 갱신하는 방식이다.", "단어를 좌표로 바꾸어 의미적으로 가까운 단어가 공간에서도 가까워지게 한다.", "token -> embedding vector; contextual model updates representation with surrounding tokens", "text row가 token sequence 또는 embedding matrix로 변환된다.", "Embedding layer, tokenizer, transformer hidden states", "LLM PDF의 embedding/encoder/decoder 용어 페이지가 ML1 text vectorization의 후속이다.", "embedding을 사람이 정한 사전 코드처럼 고정 의미로 보는 오류.", prerequisites=("n_DS_ML1.text_vectorization_features",), followups=("n_DS_LLM.attention_transformer", "n_DS_ML3.kmeans_distance_metrics"), keywords=("임베딩", "Embedding", "Encoder", "Decoder", "vector"), web_refs=("web_bert_2018",)),
            c("n_DS_LLM.encoder_decoder_seq2seq", "Encoder/Decoder와 Seq2Seq", "입력 시퀀스를 표현으로 압축하는 encoder와 출력 시퀀스를 생성하는 decoder를 결합한 구조다.", "문장을 이해하는 쪽과 문장을 내보내는 쪽을 나눈 번역기 구조다.", "encoder(input sequence)->context representation; decoder(context)->output sequence", "입력 텍스트와 출력 텍스트가 paired rows로 구성된다.", "seq2seq model, encoder outputs, decoder generation", "Seq2Seq 페이지는 길이가 다른 입력/출력 시퀀스 처리 구조를 설명한다.", "encoder/decoder를 단순 전처리/후처리 함수로만 보는 오류.", prerequisites=("n_DS_LLM.embedding_contextual_representation",), followups=("n_DS_LLM.attention_transformer",), keywords=("Sequence to Sequence", "Encoder", "Decoder", "Seq2Seq")),
            c("n_DS_LLM.attention_transformer", "Attention과 Transformer", "attention은 토큰들이 서로 얼마나 참고해야 하는지 가중치를 계산하고, Transformer는 recurrence 없이 attention 중심으로 시퀀스를 처리한다.", "문장 안 모든 단어가 서로를 보며 중요한 연결에 집중하게 하는 구조다.", "Attention(Q,K,V)=softmax(QK^T/sqrt(d_k))V", "token sequence가 Q/K/V 행렬과 hidden states로 변환된다.", "Transformer encoder/decoder, multi-head self-attention", "LLM PDF는 Transformer가 self-attention 기반 LLM의 근간이라고 연결한다.", "attention weight를 곧바로 인간적 설명 또는 인과로 단정하는 오류.", prerequisites=("n_DS_LLM.encoder_decoder_seq2seq",), followups=("n_DS_LLM.bert_gpt_pretraining", "n_DS_LLM.foundation_instruction_tuning"), keywords=("Transformer", "Attention", "self-attention", "multi-head"), web_refs=("web_transformer_2017",)),
            c("n_DS_LLM.bert_gpt_pretraining", "BERT/GPT와 사전학습", "BERT는 encoder 계열 양방향 문맥 표현, GPT는 decoder 계열 다음 토큰 생성을 중심으로 한 Transformer 사전학습 모델이다.", "많은 텍스트로 먼저 언어 패턴을 익히고, 이후 작업별로 조정한다.", "pre-train on large corpus -> fine-tune or prompt for downstream task", "문서 corpus rows가 토큰 시퀀스 학습 데이터가 된다.", "BERT encoder, GPT decoder, pretraining/fine-tuning", "LLM PDF의 BERT/GPT 발전사와 GPT decoder 페이지가 이 대비를 제공한다.", "BERT와 GPT를 같은 생성 모델로만 묶거나 encoder/decoder 차이를 지우는 오류.", prerequisites=("n_DS_LLM.attention_transformer",), followups=("n_DS_LLM.foundation_instruction_tuning",), keywords=("BERT", "GPT", "Pre-trained", "Decoder", "Encoder"), web_refs=("web_bert_2018", "web_transformer_2017")),
            c("n_DS_LLM.foundation_instruction_tuning", "Foundation model과 instruction tuning", "Foundation model은 대규모 사전학습 기반 범용 모델이고, instruction tuning은 지시를 이해하고 수행하도록 추가 학습하는 절차다.", "문장 생성기가 사용자의 지시를 따르는 작업 수행자로 바뀌는 단계다.", "pretrained LM -> supervised instruction data/RLHF preference optimization -> aligned assistant behavior", "prompt/input/response가 학습·평가 단위가 된다.", "instruction dataset, supervised fine-tuning, preference/RLHF pipeline", "LLM PDF의 instruction tuning 예시는 Translate instruction을 명시적으로 따른다.", "instruction tuning이 factual grounding을 자동 보장한다고 보는 오류.", prerequisites=("n_DS_LLM.bert_gpt_pretraining",), followups=("n_DS_LLM.rag_grounding",), keywords=("Instruction Tuning", "foundation model", "LLM", "Response"), web_refs=("web_instructgpt_2022",)),
            c("n_DS_LLM.rag_grounding", "RAG와 근거 기반 튜터링", "RAG는 모델의 생성 능력에 외부 검색 근거를 결합해 답변의 출처성, 갱신성, 검증 가능성을 높이는 설계다.", "머릿속 기억만 말하지 않고 책장을 찾아 근거를 붙여 대답하게 하는 구조다.", "query -> retrieve source chunks -> rerank/route -> generate with citations -> verify", "문서 chunk table, embedding index, metadata/source anchors가 필요하다.", "vector store, hybrid retrieval, reranker, source trace table", "이번 DS flat-pack 자체가 PDF 전사와 웹 근거를 결합한 로컬 RAG 소스다.", "검색 결과가 있으면 답이 무조건 맞다고 보거나, PDF 근거와 웹 보강을 섞어 출처 우선순위를 잃는 오류.", prerequisites=("n_DS_LLM.foundation_instruction_tuning", "n_DS_ML3.support_confidence_lift"), followups=("n_DS_GLOBAL.tutor_operating_modes",), keywords=("RAG", "retrieval", "grounding", "source"), web_refs=("web_rag_2020",)),
        ),
    ),
)


GLOBAL_EDGES = [
    ("n_DS_STATS.frequency_histogram", "n_DS_VIS.histogram_kde", "supports", "도수/상대도수 이해가 histogram/KDE 해석의 통계 기반이다."),
    ("n_DS_CODE.dataframe_row_column", "n_DS_VIS.chart_selection", "feeds", "dtype과 변수 의미가 그래프 선택을 결정한다."),
    ("n_DS_VIS.scatter_correlation", "n_DS_ML1.feature_target_structure", "prepares", "관계 시각화가 feature/target 후보 탐색으로 이어진다."),
    ("n_DS_STATS.population_sample_parameter_statistic", "n_DS_ML1.train_test_generalization", "analogous_to", "표본으로 모집단을 추정하는 구조와 train으로 test 성능을 추정하는 구조가 닮아 있다."),
    ("n_DS_CODE.sklearn_workflow", "n_DS_ML1.train_test_generalization", "implements", "sklearn API가 split-fit-predict-metric 절차를 실행한다."),
    ("n_DS_ML1.feature_target_structure", "n_DS_ML1.classification_regression", "routes_to", "target 의미가 분류/회귀 라우팅을 결정한다."),
    ("n_DS_ML1.classification_regression", "n_DS_ML2.svm_margin_hyperplane", "extends_to_algorithm", "SVM은 분류 문제의 margin 기반 알고리즘이다."),
    ("n_DS_ML2.distance_metrics", "n_DS_ML2.knn_vote", "operationalizes", "kNN은 거리 척도로 이웃을 선택한다."),
    ("n_DS_ML1.loss_metric", "n_DS_ML2.decision_tree_impurity", "extends_to_algorithm", "metric으로 평가하고 impurity로 split을 선택하는 tree 비교가 가능하다."),
    ("n_DS_ML2.decision_tree_impurity", "n_DS_ML2.scaling_distance_models", "contrasts_with", "tree는 scaling 영향이 작지만 depth/leaf 제약이 중요하다."),
    ("n_DS_ML2.scaling_distance_models", "n_DS_ML3.kmeans_centroid_loop", "prerequisite", "k-means도 거리 기반이라 scaling 영향을 받는다."),
    ("n_DS_ML2.distance_metrics", "n_DS_ML3.kmeans_distance_metrics", "shared_math", "kNN과 k-means 모두 거리 정의가 결과를 바꾼다."),
    ("n_DS_ML3.kmeanspp_local_optimum", "n_DS_ML3.silhouette_score", "validated_by", "초기값과 k 선택의 결과를 silhouette로 점검한다."),
    ("n_DS_STATS.contingency_table", "n_DS_ML3.association_rule", "prepares", "분할표의 조건부 비율 사고가 association rule 평가로 확장된다."),
    ("n_DS_STATS.conditional_independence", "n_DS_ML3.support_confidence_lift", "shared_formula", "lift는 독립 대비 동시출현 강도를 묻는다."),
    ("n_DS_STATS.conditional_independence", "n_DS_LLM.sequence_probability", "shared_probability_language", "언어모델의 다음 토큰 예측은 조건부확률 언어를 사용한다."),
    ("n_DS_ML1.text_vectorization_features", "n_DS_LLM.embedding_contextual_representation", "extends", "텍스트 벡터화가 embedding/문맥표현으로 깊어진다."),
    ("n_DS_ML3.kmeans_distance_metrics", "n_DS_LLM.embedding_contextual_representation", "analogous_to", "embedding 공간에서도 거리/유사도 해석이 필요하다."),
    ("n_DS_LLM.foundation_instruction_tuning", "n_DS_LLM.rag_grounding", "needs_grounding", "지시 수행 능력은 근거 검색과 분리해 검증해야 한다."),
]


def read_transcript(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    page = 0
    page_line = 0
    rows: list[dict[str, object]] = []
    marker = re.compile(r"^=== PAGE (\d{3}) ===$")
    for global_line, line in enumerate(lines, start=1):
        match = marker.match(line)
        if match:
            page = int(match.group(1))
            page_line = 0
            continue
        if page == 0 or not line.strip():
            continue
        page_line += 1
        rows.append(
            {
                "global_line": global_line,
                "page": page,
                "page_line": page_line,
                "text": line.strip(),
            }
        )
    return rows


def find_evidence(rows: list[dict[str, object]], concept: Concept, route_id: str, seq: int) -> dict[str, object]:
    best: dict[str, object] | None = None
    best_score = -1
    for row in rows:
        text = str(row["text"])
        lower = text.lower()
        score = sum(1 for kw in concept.keywords if kw.lower() in lower)
        if score > best_score:
            best = row
            best_score = score
    if best is None:
        best = rows[0]
    if best_score <= 0 and concept.web_refs:
        web_lookup = {item["id"]: item for item in WEB_SOURCES}
        ref_id = concept.web_refs[0]
        ref = web_lookup[ref_id]
        return {
            "evidence_id": f"ev_{route_id}_{seq:03d}",
            "node_id": concept.node_id,
            "source_id": route_id,
            "source_kind": "web_grounding",
            "transcript_anchor": f"WEB:{ref_id}",
            "ref": {
                "url": ref["url"],
                "title": ref["title"],
            },
            "snippet": f"강의 PDF 전사에서 직접 키워드가 약해 `{ref_id}`를 확장 근거로 사용: {ref['use']}",
            "support_level": "web_grounded_extension",
        }
    quote = str(best["text"])
    if len(quote) > 180:
        quote = quote[:177] + "..."
    return {
        "evidence_id": f"ev_{route_id}_{seq:03d}",
        "node_id": concept.node_id,
        "source_id": route_id,
        "source_kind": "pdf_transcript",
        "transcript_anchor": f"{route_id}:p{int(best['page']):03d}:L{int(best['page_line']):03d}",
        "ref": {
            "path": f"dataScience/txt_raw/{route_id_to_transcript(route_id)}",
            "line_start": int(best["global_line"]),
            "line_end": int(best["global_line"]),
        },
        "snippet": quote,
        "support_level": "direct_keyword_match" if best_score > 0 else "fallback_page_match",
    }


def route_id_to_transcript(route_id: str) -> str:
    for profile in PROFILES:
        if profile.route_id == route_id:
            return profile.transcript_name
    raise KeyError(route_id)


def page_anchor(rows: list[dict[str, object]], route_id: str, page: int) -> str:
    page_rows = [row for row in rows if int(row["page"]) == page]
    line = int(page_rows[0]["page_line"]) if page_rows else 1
    return f"{route_id}:p{page:03d}:L{line:03d}"


def render_visual_pages(profile: SourceProfile, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out_dir = VISUAL_RAW / profile.route_id
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = PDF_RAW / profile.pdf_name
    document = fitz.open(pdf_path)
    records = []
    for item in profile.visual_pages:
        if item.page < 1 or item.page > document.page_count:
            continue
        page = document.load_page(item.page - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(1.35, 1.35), alpha=False)
        image_path = out_dir / f"{profile.route_id}_p{item.page:03d}__{item.label}.png"
        pix.save(image_path)
        records.append(
            {
                "source_id": profile.route_id,
                "page": item.page,
                "label": item.label,
                "reason": item.reason,
                "image_path": str(image_path.relative_to(ROOT)),
                "transcript_anchor": page_anchor(rows, profile.route_id, item.page),
            }
        )
    document.close()
    (out_dir / "visual_pages.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return records


def annotated_transcript(profile: SourceProfile, rows: list[dict[str, object]]) -> str:
    grouped: dict[int, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(int(row["page"]), []).append(row)
    parts = [
        f"# {profile.route_id} — annotated PDF transcript",
        "",
        f"- title: {profile.title}",
        f"- source_pdf: `dataScience/pdf_raw/{profile.pdf_name}`",
        f"- transcript: `dataScience/txt_raw/{profile.transcript_name}`",
        "",
    ]
    for page in sorted(grouped):
        parts.append(f"## PAGE {page:03d}")
        parts.append("")
        for row in grouped[page]:
            anchor = f"{profile.route_id}:p{page:03d}:L{int(row['page_line']):03d}"
            parts.append(f"- `{anchor}` {row['text']}")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def node_index_md(profile: SourceProfile, evidences: list[dict[str, object]], visuals: list[dict[str, object]]) -> str:
    ev_by_node = {ev["node_id"]: ev for ev in evidences}
    parts = [
        f"# {profile.route_id} — concept node index",
        "",
        f"## Graph location",
        "",
        profile.graph_location,
        "",
        "| node_id | label | gate | prerequisites | followups | evidence |",
        "|---|---|---|---|---|---|",
    ]
    for concept in profile.concepts:
        ev = ev_by_node[concept.node_id]
        parts.append(
            f"| `{concept.node_id}` | {concept.label} | {profile.gate} | "
            f"{', '.join(f'`{x}`' for x in concept.prerequisites) or '-'} | "
            f"{', '.join(f'`{x}`' for x in concept.followups) or '-'} | `{ev['transcript_anchor']}` |"
        )
    parts.extend(["", "## Visual anchors", ""])
    for visual in visuals:
        parts.append(
            f"- `{profile.route_id}:p{visual['page']:03d}` {visual['reason']} "
            f"-> `{visual['image_path']}`"
        )
    return "\n".join(parts).rstrip() + "\n"


def rawdata_develop_md(
    profile: SourceProfile,
    evidences: list[dict[str, object]],
    visuals: list[dict[str, object]],
) -> str:
    ev_by_node = {ev["node_id"]: ev for ev in evidences}
    parts = [
        f"# {profile.route_id} — rawdata develop",
        "",
        f"## One-line source role",
        "",
        profile.one_line,
        "",
        "## Source policy",
        "",
        f"- PDF raw: `dataScience/pdf_raw/{profile.pdf_name}`",
        f"- TXT raw transcript: `dataScience/txt_raw/{profile.transcript_name}`",
        "- PDF page images are derived visual raw data, not a replacement for the PDF.",
        "- 숫자·공식·최적값은 전사와 이미지가 충돌하면 원본 PDF 대조가 우선이다.",
        "",
        "## Visual raw intake",
        "",
    ]
    for visual in visuals:
        parts.append(
            f"- `{visual['transcript_anchor']}` {visual['label']}: {visual['reason']} "
            f"-> `{visual['image_path']}`"
        )
    parts.extend(["", "## Deep rawdata development by node", ""])
    for concept in profile.concepts:
        ev = ev_by_node[concept.node_id]
        parts.extend(
            [
                f"### {concept.label}",
                "",
                f"- 현재 노드: `{concept.node_id}`",
                f"- 관련 파일: `{profile.route_id}` / `{profile.transcript_name}`",
                f"- 근거 anchor: `{ev['transcript_anchor']}` / `{ev['evidence_id']}`",
                f"- 한 줄 정의: {concept.definition}",
                f"- 쉬운 직관: {concept.intuition}",
                f"- 수식/절차: {concept.formula_or_procedure}",
                f"- 데이터프레임 구조: {concept.dataframe_view}",
                f"- 코드 관점: {concept.code_view}",
                f"- 강의 예제 연결: {concept.course_example}",
                f"- 자주 하는 실수: {concept.common_mistake}",
                f"- 선행 노드: {', '.join(f'`{x}`' for x in concept.prerequisites) or '-'}",
                f"- 후속 노드: {', '.join(f'`{x}`' for x in concept.followups) or '-'}",
                f"- 유사 노드: {', '.join(f'`{x}`' for x in concept.analogous) or '-'}",
                f"- evidence snippet: {ev['snippet']}",
                f"- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?",
                "",
            ]
        )
    return "\n".join(parts).rstrip() + "\n"


def rag_md(profile: SourceProfile, evidences: list[dict[str, object]], visuals: list[dict[str, object]]) -> str:
    ev_by_node = {ev["node_id"]: ev for ev in evidences}
    web_lookup = {item["id"]: item for item in WEB_SOURCES}
    parts = [
        f"# {profile.route_id} — RAG tutor source",
        "",
        "## Retrieval Routing Table",
        "",
        f"| route | when to use | primary files |",
        "|---|---|---|",
        f"| `{profile.route_id}` | {profile.one_line} | `__01_pdf_transcript`, `__02_rawdata_develop`, `__03_concept_node_index`, this `__04_rag` |",
        "",
        "## Core Concept Node Cards",
        "",
    ]
    for concept in profile.concepts:
        ev = ev_by_node[concept.node_id]
        parts.extend(
            [
                f"### `{concept.node_id}` — {concept.label}",
                "",
                f"- 정의: {concept.definition}",
                f"- 직관: {concept.intuition}",
                f"- 수식/절차: {concept.formula_or_procedure}",
                f"- pandas/sklearn 언어: {concept.code_view}",
                f"- 오답위험: {concept.common_mistake}",
                f"- 연결: 선행 {', '.join(concept.prerequisites) or '-'} / 후속 {', '.join(concept.followups) or '-'} / 유사 {', '.join(concept.analogous) or '-'}",
                f"- source trace: `{ev['transcript_anchor']}`, `{ev['evidence_id']}`",
                "",
            ]
        )
    parts.extend(["## Visual Example Cards", ""])
    for visual in visuals:
        parts.append(
            f"- `{visual['label']}`: {visual['reason']} / anchor `{visual['transcript_anchor']}` / image `{visual['image_path']}`"
        )
    parts.extend(
        [
            "",
            "## Code Mapping",
            "",
            "- row = observation, column = variable, feature matrix = `X`, target vector = `y`.",
            "- `fit` = 학습, `predict` = 추론, `transform` = 표현 변환, `metric` = 평가 함수.",
            "- 시각화/통계 노드는 pandas 집계와 plot으로, ML 노드는 sklearn estimator/pipeline으로, LLM 노드는 tokenizer/embedding/retrieval로 매핑한다.",
            "",
            "## Misconception Bank",
            "",
        ]
    )
    for concept in profile.concepts:
        parts.append(f"- {concept.label}: {concept.common_mistake}")
    parts.extend(["", "## Web Grounding Notes", ""])
    used_refs = []
    for concept in profile.concepts:
        for ref_id in concept.web_refs:
            if ref_id not in used_refs:
                used_refs.append(ref_id)
    if used_refs:
        for ref_id in used_refs:
            ref = web_lookup[ref_id]
            parts.append(f"- `{ref_id}` {ref['title']}: {ref['url']} — {ref['use']}")
    else:
        parts.append("- PDF/TXT 근거가 충분한 기본 강의 노드다. 최신 API 차이는 global web grounding table에서 보강한다.")
    parts.extend(["", "## Source Trace Table", "", "| node_id | evidence_id | transcript_anchor | snippet |", "|---|---|---|---|"])
    for ev in evidences:
        parts.append(
            f"| `{ev['node_id']}` | `{ev['evidence_id']}` | `{ev['transcript_anchor']}` | {ev['snippet']} |"
        )
    return "\n".join(parts).rstrip() + "\n"


def build_edges(profile: SourceProfile) -> list[dict[str, str]]:
    edges = []
    idx = 1
    for source, target, edge_type, rationale in profile.local_edges:
        edges.append(
            {
                "edge_id": f"e_{profile.route_id}_{idx:03d}",
                "from": source,
                "to": target,
                "type": edge_type,
                "rationale": rationale,
                "scope": "local",
            }
        )
        idx += 1
    concept_ids = {concept.node_id for concept in profile.concepts}
    for source, target, edge_type, rationale in GLOBAL_EDGES:
        if source in concept_ids or target in concept_ids:
            edges.append(
                {
                    "edge_id": f"e_{profile.route_id}_{idx:03d}",
                    "from": source,
                    "to": target,
                    "type": edge_type,
                    "rationale": rationale,
                    "scope": "cross_source",
                }
            )
            idx += 1
    return edges


def roadmap_md(all_nodes: list[dict[str, object]], all_edges: list[dict[str, object]]) -> str:
    sessions = [
        {
            "session": "1회차",
            "title": "데이터사이언스 입력 구조 만들기",
            "weight": "15%",
            "role": "통계·시각화·pandas를 지도학습 입력 구조로 압축",
            "nodes": [
                "n_DS_STATS.population_sample_parameter_statistic",
                "n_DS_STATS.frequency_histogram",
                "n_DS_CODE.dataframe_row_column",
                "n_DS_VIS.chart_selection",
                "n_DS_VIS.histogram_kde",
                "n_DS_VIS.scatter_correlation",
                "n_DS_VIS.boxplot_iqr",
                "n_DS_VIS.heatmap_multivariate",
            ],
            "notebook": "DS_SESSION01_stats_eda_foundation.ipynb",
        },
        {
            "session": "2회차",
            "title": "지도학습 파이프라인과 metric",
            "weight": "15%",
            "role": "X/y, train/test, classification/regression, confusion matrix",
            "nodes": [
                "n_DS_ML1.feature_target_structure",
                "n_DS_ML1.learning_types",
                "n_DS_ML1.train_test_generalization",
                "n_DS_ML1.preprocessing_leakage",
                "n_DS_ML1.classification_regression",
                "n_DS_ML1.loss_metric",
            ],
            "notebook": "DS_SESSION02_03_supervised_pipeline_regression.ipynb",
        },
        {
            "session": "3회차",
            "title": "선형회귀와 로지스틱 회귀",
            "weight": "18%",
            "role": "계수, 확률, odds/logit, threshold, precision/recall tradeoff",
            "nodes": [
                "n_DS_ML1.classification_regression",
                "n_DS_ML1.logistic_logit_probability",
                "n_DS_ML1.loss_metric",
                "n_DS_ML1.preprocessing_leakage",
            ],
            "notebook": "DS_SESSION02_03_supervised_pipeline_regression.ipynb",
        },
        {
            "session": "4회차",
            "title": "SVM 심화",
            "weight": "18%",
            "role": "margin, support vector, soft margin, kernel, C/gamma, scaling",
            "nodes": [
                "n_DS_ML2.svm_margin_hyperplane",
                "n_DS_ML2.support_vectors",
                "n_DS_ML2.kernel_trick",
                "n_DS_ML2.scaling_distance_models",
            ],
            "notebook": "DS_SESSION04_05_supervised_algorithms.ipynb",
        },
        {
            "session": "5회차",
            "title": "kNN과 의사결정나무",
            "weight": "19%",
            "role": "거리 기반 vs 규칙 기반, scaling, k 선택, impurity/depth",
            "nodes": [
                "n_DS_ML2.distance_metrics",
                "n_DS_ML2.knn_vote",
                "n_DS_ML2.k_selection_bias_variance",
                "n_DS_ML2.decision_tree_impurity",
            ],
            "notebook": "DS_SESSION04_05_supervised_algorithms.ipynb",
        },
        {
            "session": "6회차",
            "title": "통합 capstone",
            "weight": "15%",
            "role": "k-means/PCA/association/LLM 압축 + customer churn project",
            "nodes": [
                "n_DS_ML3.clustering_problem",
                "n_DS_ML3.kmeans_centroid_loop",
                "n_DS_ML3.kmeanspp_local_optimum",
                "n_DS_ML3.silhouette_score",
                "n_DS_ML3.pca_dimensionality_reduction",
                "n_DS_ML3.support_confidence_lift",
                "n_DS_LLM.sequence_probability",
                "n_DS_LLM.foundation_instruction_tuning",
            ],
            "notebook": "DS_CAPSTONE_customer_supervised_learning.ipynb",
        },
    ]
    parts = [
        "# DataScience learning roadmap",
        "",
        "핵심 문장: 데이터사이언스는 도구 사용법 암기가 아니라, 현실 질문을 데이터 단위, 변수, 분포, 시각화, 모델, 평가 지표, 해석, 의사결정으로 번역하고 그 수학적 의미와 실무적 의미를 동시에 검증하는 과정이다.",
        "",
        "## Six-session priority",
        "",
        "| 구간 | 회차 | 비중 | 역할 |",
        "|---|---|---:|---|",
        "| 압축 기반 | 1회차 | 15% | 통계·시각화·pandas를 지도학습 입력 구조로 연결 |",
        "| 지도학습 핵심 | 2~5회차 | 70% | X/y, train/test, 회귀, 로지스틱, SVM, kNN, decision tree |",
        "| 통합 정리 | 6회차 | 15% | k-means·PCA·LLM을 압축하고 전체 시험/노트북 프로젝트로 통합 |",
        "",
        "## Session plan",
        "",
        "| session | title | weight | role | notebook | key nodes |",
        "|---|---|---:|---|---|---|",
    ]
    for item in sessions:
        nodes = "<br>".join(f"`{node}`" for node in item["nodes"])
        parts.append(
            f"| {item['session']} | {item['title']} | {item['weight']} | {item['role']} | `{item['notebook']}` | {nodes} |"
        )
    parts.extend(
        [
            "",
            "## Common practice pattern",
            "",
            "각 회차는 반드시 `큰 개념 지도 -> 손계산 1개 -> 코드 재현 1개 -> 오답로그 1개 -> 새 문제 변형 1개`를 포함한다.",
            "",
            "## Fixed analysis spine",
            "",
            "`business question -> unit -> row/column -> feature/target -> dtype -> preprocessing -> EDA -> model selection -> fit/predict -> metric -> interpretation -> limitation check`",
        ]
    )
    parts.extend(["", "## Global high-signal edges", ""])
    for edge in all_edges:
        if edge.get("scope") == "global":
            parts.append(f"- `{edge['from']}` --{edge['type']}--> `{edge['to']}`: {edge['rationale']}")
    parts.extend(["", "## Node count", "", f"- total nodes: {len(all_nodes)}", f"- total edges: {len(all_edges)}"])
    return "\n".join(parts).rstrip() + "\n"


def web_grounding_md(generated_at: str) -> str:
    parts = [
        "# DS web grounding sources",
        "",
        f"Generated at UTC: `{generated_at}`",
        "",
        "PDF/TXT 강의자료가 1차 근거다. 아래 웹 자료는 최신 API, 연구 원 논문, RAG 설계 보강을 위해서만 쓴다.",
        "",
        "| id | title | scope | use | url |",
        "|---|---|---|---|---|",
    ]
    for item in WEB_SOURCES:
        parts.append(f"| `{item['id']}` | {item['title']} | {item['scope']} | {item['use']} | {item['url']} |")
    return "\n".join(parts).rstrip() + "\n"


def tutor_prompt_md() -> str:
    return """# DataScience tutor system prompt

너는 사용자의 전담 1:1 데이터사이언스 튜터다. 목표는 요약이 아니라 PDF 강의자료와 DS flat-pack 근거를 사용해 통계 -> 프로그래밍 -> EDA/시각화 -> 머신러닝 -> 비지도학습/연관분석 -> 언어모델/LLM을 하나의 개념 그래프로 가르치는 것이다.

핵심 목표는 사용자가 새 데이터 문제를 받았을 때 `문제정의 -> 데이터 단위 -> row/column -> feature/target -> dtype -> 전처리 -> EDA -> 모델 선택 -> 학습/평가 -> 해석 -> 한계검증` 순서로 독립 분석할 수 있게 만드는 것이다.

## Learner profile

- 강점: 구조화 능력, 현실언어/수식언어/도구언어 번역 능력, 학습 시스템 설계 능력.
- 약점: 손계산, 코드 실행, 조건/지표 해석 같은 절차형 정확도가 흔들릴 수 있음.
- 운영 원칙: 매 회차 `큰 개념 지도`, `작은 손계산`, `코드 재현`, `오답로그`, `새 문제 변형`을 포함한다.

## Source priority

1. `DS_PDFxx__04_rag.md`
2. `DS_PDFxx__03_concept_node_index.md`
3. `DS_PDFxx__02_rawdata_develop.md`
4. `DS_PDFxx__01_pdf_transcript.md`
5. `WEB_GROUNDING_SOURCES.md`
6. 일반 데이터사이언스/통계/ML 교과 지식
7. 현대 Python/pandas/scikit-learn/TensorFlow/LLM 실무 확장 지식

## Six-session design

전체는 6회차다. 범위 전체를 얇게 훑지 말고, 1회차에서 통계/시각화/pandas를 지도학습 입력 구조로 압축한 뒤 2~5회차 70%를 지도학습 알고리즘에 집중한다.

| 회차 | 비중 | 핵심 |
|---|---:|---|
| 1회차 | 15% | 통계·시각화·pandas를 `row/column/feature/target` 구조로 압축 |
| 2회차 | 15% | X/y, train/test, classification/regression, confusion matrix metric |
| 3회차 | 18% | linear regression, logistic regression, odds/logit, threshold |
| 4회차 | 18% | SVM margin, support vector, kernel, C/gamma, scaling |
| 5회차 | 19% | kNN distance/scaling/k, decision tree impurity/depth |
| 6회차 | 15% | k-means/PCA/association/LLM 압축 + capstone |

## Notebook policy

- 문제지 노트북만 기본 생성한다. 정답본은 사용자가 별도 요청할 때만 `_answer.ipynb`로 분리한다.
- 문제지에는 정답 코드와 완성 해석을 넣지 않는다.
- mock data는 실제 데이터가 아님을 명시하고 `random_state=42` 또는 고정 seed를 쓴다.
- 기본 산출물은 `DS_SESSION01_stats_eda_foundation.ipynb`, `DS_SESSION02_03_supervised_pipeline_regression.ipynb`, `DS_SESSION04_05_supervised_algorithms.ipynb`, `DS_CAPSTONE_customer_supervised_learning.ipynb`이다.

## Operating rule

- 먼저 핵심 노드와 source_id를 추출한다.
- 가능하면 `source_id:pNNN:LNNN` anchor와 `evidence_id`를 붙인다.
- PDF/TXT 근거와 웹 보강 근거를 섞어 출처 우선순위를 잃지 않는다.
- 개념 설명은 현재 노드, 관련 파일, 한 줄 정의, 쉬운 직관, 수식/절차, 데이터프레임 구조, 코드 관점, 강의 예제, 자주 하는 실수, 선행/후속/유사 노드, 근거 anchor, 확인 질문 순서를 따른다.
- 문제 풀이 모드는 현실 질문 재해석 -> 데이터 단위 -> 변수 정의 -> feature/target -> dtype -> 전처리 -> EDA -> 모델 유형 -> 알고리즘 -> 평가 -> 해석 -> 한계 검증 순서로 진행한다.
"""


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    INVENTORY.mkdir(parents=True, exist_ok=True)
    VISUAL_RAW.mkdir(parents=True, exist_ok=True)
    FLAT_PACK.mkdir(parents=True, exist_ok=True)

    all_nodes: list[dict[str, object]] = []
    all_edges: list[dict[str, object]] = []
    all_visuals: list[dict[str, object]] = []
    verification = {
        "generated_at_utc": generated_at,
        "profiles": [],
        "errors": [],
    }

    for profile in PROFILES:
        folder = INVENTORY / profile.folder
        folder.mkdir(parents=True, exist_ok=True)
        rows = read_transcript(TXT_RAW / profile.transcript_name)
        visuals = render_visual_pages(profile, rows)
        all_visuals.extend(visuals)

        evidences = [
            find_evidence(rows, concept, profile.route_id, index)
            for index, concept in enumerate(profile.concepts, start=1)
        ]
        nodes = [
            {
                "node_id": concept.node_id,
                "source_id": profile.route_id,
                "label": concept.label,
                "gate": profile.gate,
                "definition": concept.definition,
                "intuition": concept.intuition,
                "formula_or_procedure": concept.formula_or_procedure,
                "dataframe_view": concept.dataframe_view,
                "code_view": concept.code_view,
                "course_example": concept.course_example,
                "common_mistake": concept.common_mistake,
                "prerequisites": list(concept.prerequisites),
                "followups": list(concept.followups),
                "analogous": list(concept.analogous),
                "keywords": list(concept.keywords),
                "web_refs": list(concept.web_refs),
                "evidence_ids": [evidences[index]["evidence_id"]],
            }
            for index, concept in enumerate(profile.concepts)
        ]
        edges = build_edges(profile)
        all_nodes.extend(nodes)
        all_edges.extend(edges)

        transcript_md = annotated_transcript(profile, rows)
        concept_md = node_index_md(profile, evidences, visuals)
        raw_md = rawdata_develop_md(profile, evidences, visuals)
        rag = rag_md(profile, evidences, visuals)

        (folder / f"{profile.route_id}__annotated_pdf_transcript.md").write_text(transcript_md, encoding="utf-8")
        (folder / f"{profile.route_id}__concept_node_index.md").write_text(concept_md, encoding="utf-8")
        (folder / f"{profile.route_id}__rawdata_develop.md").write_text(raw_md, encoding="utf-8")
        (folder / f"{profile.route_id}__rag.md").write_text(rag, encoding="utf-8")
        (folder / "nodes.json").write_text(json.dumps(nodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (folder / "edges.json").write_text(json.dumps(edges, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (folder / "evidence.jsonl").write_text(
            "".join(json.dumps(ev, ensure_ascii=False) + "\n" for ev in evidences),
            encoding="utf-8",
        )
        (folder / "visual_pages.json").write_text(json.dumps(visuals, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        shutil.copyfile(folder / f"{profile.route_id}__annotated_pdf_transcript.md", FLAT_PACK / f"{profile.route_id}__01_pdf_transcript.md")
        shutil.copyfile(folder / f"{profile.route_id}__rawdata_develop.md", FLAT_PACK / f"{profile.route_id}__02_rawdata_develop.md")
        shutil.copyfile(folder / f"{profile.route_id}__concept_node_index.md", FLAT_PACK / f"{profile.route_id}__03_concept_node_index.md")
        shutil.copyfile(folder / f"{profile.route_id}__rag.md", FLAT_PACK / f"{profile.route_id}__04_rag.md")

        verification["profiles"].append(
            {
                "source_id": profile.route_id,
                "nodes": len(nodes),
                "edges": len(edges),
                "evidence": len(evidences),
                "visual_pages": len(visuals),
            }
        )

    global_edges = [
        {
            "edge_id": f"e_DS_GLOBAL_{index:03d}",
            "from": source,
            "to": target,
            "type": edge_type,
            "rationale": rationale,
            "scope": "global",
        }
        for index, (source, target, edge_type, rationale) in enumerate(GLOBAL_EDGES, start=1)
    ]
    all_edges.extend(global_edges)

    (INVENTORY / "DS_global_nodes.json").write_text(json.dumps(all_nodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (INVENTORY / "DS_global_edges.json").write_text(json.dumps(all_edges, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (INVENTORY / "WEB_GROUNDING_SOURCES.md").write_text(web_grounding_md(generated_at), encoding="utf-8")
    (INVENTORY / "DS_GLOBAL_NODE_LINK_MAP.md").write_text(roadmap_md(all_nodes, all_edges), encoding="utf-8")
    (INVENTORY / "verification_report_ds_rag.json").write_text(
        json.dumps(verification, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (FLAT_PACK / "00__datascience_learning_roadmap.md").write_text(roadmap_md(all_nodes, all_edges), encoding="utf-8")
    (FLAT_PACK / "DATA_SCIENCE_TUTOR_SYSTEM_PROMPT.md").write_text(tutor_prompt_md(), encoding="utf-8")
    (FLAT_PACK / "WEB_GROUNDING_SOURCES.md").write_text(web_grounding_md(generated_at), encoding="utf-8")

    atlas_parts = [
        "# DS visual raw image atlas",
        "",
        f"Generated at UTC: `{generated_at}`",
        "",
        "PDF page renders are stored as derived visual raw data. Use the original PDF when numeric or diagram detail is ambiguous.",
        "",
        "| source_id | page | label | reason | image | transcript_anchor |",
        "|---|---:|---|---|---|---|",
    ]
    for visual in all_visuals:
        atlas_parts.append(
            f"| `{visual['source_id']}` | {visual['page']} | `{visual['label']}` | {visual['reason']} | `{visual['image_path']}` | `{visual['transcript_anchor']}` |"
        )
    (VISUAL_RAW / "IMAGE_ATLAS.md").write_text("\n".join(atlas_parts).rstrip() + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "profiles": len(PROFILES),
                "nodes": len(all_nodes),
                "edges": len(all_edges),
                "visual_pages": len(all_visuals),
                "flat_pack": str(FLAT_PACK.relative_to(ROOT)),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
