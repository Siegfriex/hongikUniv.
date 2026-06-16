#!/usr/bin/env python3
"""Create DS six-session problem notebooks without answer cells."""

from __future__ import annotations

import json
from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "dataScience" / "workshop" / "ipynb"
OUT_DIR.mkdir(parents=True, exist_ok=True)


DATASET_CELL = r"""# 공통 mock customer dataset
# 실제 고객 데이터가 아닙니다. 모든 회차에서 같은 spine을 쓰기 위해 random_state=42로 고정합니다.
import numpy as np
import pandas as pd

RANDOM_STATE = 42
rng = np.random.default_rng(RANDOM_STATE)
n = 240

customer_id = np.arange(1, n + 1)
age = np.clip(rng.normal(39, 12, n).round(), 18, 75).astype(int)
income = np.clip(rng.normal(5200, 1800, n), 1200, 12000).round(0)
usage_time = np.clip(rng.gamma(5, 8, n), 1, 120).round(1)
payment_delay = rng.poisson(1.8, n)
complaints = rng.poisson(0.6, n)
plan_type = rng.choice(["basic", "standard", "premium"], n, p=[0.38, 0.42, 0.20])
region = rng.choice(["Seoul", "Gyeonggi", "Busan", "Daejeon"], n, p=[0.42, 0.31, 0.17, 0.10])
tenure_months = np.clip(rng.gamma(3.0, 8.0, n), 1, 84).round().astype(int)
monthly_spend = (
    18
    + 0.010 * income
    + 0.55 * usage_time
    + np.where(plan_type == "premium", 36, np.where(plan_type == "standard", 18, 0))
    + rng.normal(0, 18, n)
).round(2)

logit = (
    -2.2
    + 0.10 * payment_delay
    + 0.42 * complaints
    - 0.018 * tenure_months
    - 0.010 * usage_time
    + np.where(plan_type == "basic", 0.55, 0.0)
    + rng.normal(0, 0.45, n)
)
churn_prob = 1 / (1 + np.exp(-logit))
churn = rng.binomial(1, churn_prob)
review_pool = np.array([
    "fast support stable service",
    "billing delay confusing app",
    "good speed but expensive plan",
    "frequent complaints slow response",
    "premium service reliable",
    "basic plan limited features",
])
review_text = rng.choice(review_pool, n)

df = pd.DataFrame({
    "customer_id": customer_id,
    "age": age,
    "income": income,
    "usage_time": usage_time,
    "payment_delay": payment_delay,
    "complaints": complaints,
    "plan_type": plan_type,
    "region": region,
    "tenure_months": tenure_months,
    "monthly_spend": monthly_spend,
    "review_text": review_text,
    "churn": churn,
})

missing_idx = rng.choice(df.index, 10, replace=False)
df.loc[missing_idx[:5], "income"] = np.nan
df.loc[missing_idx[5:], "usage_time"] = np.nan
df.head()"""


NOTEBOOKS = {
    "DS_SESSION01_stats_eda_foundation.ipynb": {
        "title": "DS_SESSION01_stats_eda_foundation",
        "sessions": "1회차",
        "anchors": [
            "n_DS_STATS.population_sample_parameter_statistic",
            "n_DS_STATS.frequency_histogram",
            "n_DS_CODE.dataframe_row_column",
            "n_DS_VIS.chart_selection",
            "n_DS_VIS.histogram_kde",
            "n_DS_VIS.scatter_correlation",
            "n_DS_VIS.boxplot_iqr",
            "n_DS_VIS.heatmap_multivariate",
        ],
        "tasks": [
            "unit of analysis, row meaning, column meaning을 한국어로 쓰기",
            "feature/target/data type 표 작성",
            "churn 상대도수와 간단한 분할표 손계산",
            "missing/outlier 점검 코드 작성",
            "histogram, box plot, scatter plot, heatmap 중 변수 유형에 맞는 그래프 선택",
            "오답로그: 상관=인과, boxplot 이상치 자동삭제, histogram binwidth 과해석",
            "새 문제 변형: target이 monthly_spend이면 문제 유형이 어떻게 바뀌는지 쓰기",
        ],
    },
    "DS_SESSION02_03_supervised_pipeline_regression.ipynb": {
        "title": "DS_SESSION02_03_supervised_pipeline_regression",
        "sessions": "2~3회차",
        "anchors": [
            "n_DS_ML1.feature_target_structure",
            "n_DS_ML1.train_test_generalization",
            "n_DS_ML1.preprocessing_leakage",
            "n_DS_ML1.classification_regression",
            "n_DS_ML1.loss_metric",
            "n_DS_ML1.logistic_logit_probability",
        ],
        "tasks": [
            "business question -> X/y -> train/test -> fit -> predict -> metric 흐름을 그리기",
            "TP/TN/FP/FN으로 accuracy, precision, recall, F1 손계산",
            "monthly_spend 연속형 target에 LinearRegression 문제 세팅",
            "churn 범주형 target에 LogisticRegression 문제 세팅",
            "threshold 0.3/0.5/0.7에서 precision/recall 변화 비교 코드 작성",
            "이상치 추가 전후 선형회귀 계수 변화 확인",
            "오답로그: target leakage, train/test 누락, threshold를 모델 자체로 오해",
            "새 문제 변형: FN 비용이 클 때 어떤 metric을 우선할지 쓰기",
        ],
    },
    "DS_SESSION04_05_supervised_algorithms.ipynb": {
        "title": "DS_SESSION04_05_supervised_algorithms",
        "sessions": "4~5회차",
        "anchors": [
            "n_DS_ML2.svm_margin_hyperplane",
            "n_DS_ML2.support_vectors",
            "n_DS_ML2.kernel_trick",
            "n_DS_ML2.distance_metrics",
            "n_DS_ML2.scaling_distance_models",
            "n_DS_ML2.knn_vote",
            "n_DS_ML2.k_selection_bias_variance",
            "n_DS_ML2.decision_tree_impurity",
        ],
        "tasks": [
            "SVM decision boundary, margin, support vector를 그림으로 설명",
            "w^T x + b = 0, margin width = 2 / ||w|| 손계산 미니문제",
            "make_blobs로 linear SVM margin 시각화 코드 작성",
            "make_moons로 linear SVM 실패와 RBF kernel 비교",
            "C/gamma 변화가 underfitting/overfitting에 미치는 영향 표 작성",
            "Euclidean/Manhattan/Minkowski distance 손계산",
            "KNeighborsClassifier와 DecisionTreeClassifier를 같은 데이터에서 비교",
            "오답로그: scaling 누락, k 값 고정, tree depth overfitting, margin=accuracy 착각",
            "새 문제 변형: scaling이 tree에는 작고 kNN/SVM에는 큰 이유를 쓰기",
        ],
    },
    "DS_CAPSTONE_customer_supervised_learning.ipynb": {
        "title": "DS_CAPSTONE_customer_supervised_learning",
        "sessions": "6회차",
        "anchors": [
            "n_DS_ML3.clustering_problem",
            "n_DS_ML3.kmeans_centroid_loop",
            "n_DS_ML3.kmeanspp_local_optimum",
            "n_DS_ML3.silhouette_score",
            "n_DS_ML3.pca_dimensionality_reduction",
            "n_DS_ML3.support_confidence_lift",
            "n_DS_LLM.sequence_probability",
            "n_DS_LLM.foundation_instruction_tuning",
        ],
        "tasks": [
            "customer churn capstone: EDA -> preprocessing -> model compare -> metric -> interpretation",
            "LogisticRegression, SVC, KNeighborsClassifier, DecisionTreeClassifier 비교표 작성",
            "FN 비용이 큰 상황에서 recall 중심으로 모델 선택 이유 쓰기",
            "KMeans 고객군 탐색과 silhouette score 해석",
            "PCA 2D 시각화는 예측 모델이 아니라 표현 변환임을 설명",
            "association support/confidence/lift 손계산",
            "review_text가 있을 때 Bag-of-Words 또는 embedding이 X가 되는 구조 설명",
            "오답로그: cluster label=정답, PCA=예측모델, LLM=검색엔진 착각",
            "새 문제 변형: 이탈 예측 대신 고객군 탐색이면 target이 있는지 쓰기",
        ],
    },
}


def md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(text)


def code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(text)


def make_notebook(spec: dict[str, object]) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    title = spec["title"]
    anchors = "\n".join(f"- `{anchor}`" for anchor in spec["anchors"])
    tasks = "\n".join(f"{idx}. {task}" for idx, task in enumerate(spec["tasks"], start=1))
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        "ds_policy": {
            "answer_included": False,
            "mock_data": True,
            "random_state": 42,
            "source_priority": "DS flat-pack first",
        },
    }
    nb.cells = [
        md(
            f"# {title}\n\n"
            f"- 범위: {spec['sessions']}\n"
            "- 형식: 문제지. 정답 코드와 완성 해석은 포함하지 않는다.\n"
            "- 데이터: `random_state=42`로 생성한 mock customer data. 실제 데이터가 아니다.\n\n"
            "## 관련 노드\n\n"
            f"{anchors}"
        ),
        md(
            "## 학습 루프\n\n"
            "각 회차는 `큰 개념 지도 -> 손계산 1개 -> 코드 재현 1개 -> 오답로그 1개 -> 새 문제 변형 1개` 순서로 진행한다."
        ),
        code(DATASET_CELL),
        md("## 과제 목록\n\n" + tasks),
        md("## 1. 큰 개념 지도\n\n위 관련 노드들을 `선행 -> 현재 -> 후속 -> 유사/혼동` 구조로 직접 연결해 보라."),
        code("# TODO: 필요한 컬럼 목록, feature 후보, target 후보를 코드로 분리해 보라.\n# 예: feature_cols = [...]\n# 정답 코드는 정답본에서만 제공한다.\n"),
        md("## 2. 손계산\n\n문제 설명에 맞춰 공식, 숫자 대입, 단위, 해석을 분리해서 작성하라."),
        code("# TODO: 손계산 검산용 작은 배열/표를 만들고 직접 계산한 값과 비교하라.\n"),
        md("## 3. 코드 재현\n\n힌트만 제공한다. 완성 코드는 직접 작성하라."),
        code("# TODO: pandas/numpy/sklearn 코드 작성\n# 주의: train/test split 이후 train 기준으로 preprocessing을 fit한다.\n"),
        md("## 4. 오답로그\n\n틀린 코드나 해석을 한 줄 이상 일부러 적고, 오류 위치와 최소 수정 방향을 쓰라."),
        code("# TODO: 오답 예시를 하나 만들고 왜 틀렸는지 주석으로 설명하라.\n"),
        md("## 5. 새 문제 변형\n\n같은 데이터에서 target, metric, 비용 구조, 또는 모델 조건이 바뀌면 분석 절차가 어떻게 바뀌는지 쓰라."),
        code("# TODO: 변형 문제의 X/y, metric, 모델 후보를 다시 정의하라.\n"),
    ]
    return nb


def main() -> None:
    created = []
    for filename, spec in NOTEBOOKS.items():
        path = OUT_DIR / filename
        nb = make_notebook(spec)
        nbf.validate(nb)
        nbf.write(nb, path)
        created.append(str(path.relative_to(ROOT)))
    manifest = {
        "policy": "problem notebooks only; answer notebooks are created only on request",
        "mock_data_random_state": 42,
        "created": created,
    }
    (OUT_DIR / "DS_6SESSION_NOTEBOOK_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
