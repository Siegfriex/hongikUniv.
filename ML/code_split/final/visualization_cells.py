# %% [markdown]
# # ML_W13_PREP_VISUAL_LECTURE Advanced Visualization Cells
#
# 이 파일은 final notebook에 선택 삽입할 수 있는 주석 강화 시각화 셀 팩이다.
# 기본 실행 스택은 numpy, pandas, matplotlib, scikit-learn으로 제한한다.
# 외부 다운로드는 사용하지 않는다.
#
# 핵심 반복 기준:
# X_batch -> net.forward -> loss_fn.forward -> loss_fn.backward -> net.backward -> optimizer.step(net)
#
# 핵심 책임 경계:
# Optimizer는 X/y를 보지 않는다.
# Optimizer는 layer가 들고 있는 param과 grad만 읽고 parameter를 update한다.

# %%
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris, load_digits
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

SEED = 42


# %% [markdown]
# ## Common helpers
#
# 고차원/미분/optimizer 시각화가 같은 수학 함수를 공유하도록 앞쪽에 둔다.
# notebook에 붙일 때도 이 셀은 V02/V04보다 먼저 실행되어야 한다.

# %%
def quad_loss(w: np.ndarray) -> float:
    """V02/V04 공통 2D quadratic loss.

    w[0] 방향은 완만하고 w[1] 방향은 가파르다.
    그래서 같은 learning rate에서도 w[1] 축에서는 overshoot가 쉽게 보인다.
    """
    w = np.asarray(w, dtype=float)
    return float(0.1 * w[0] ** 2 + 2.0 * w[1] ** 2)


def quad_grad(w: np.ndarray) -> np.ndarray:
    """quad_loss의 analytic gradient.

    gradient는 loss가 가장 빠르게 증가하는 방향이다.
    gradient descent update는 이 방향의 반대인 -gradient로 이동한다.
    """
    w = np.asarray(w, dtype=float)
    return np.array([0.2 * w[0], 4.0 * w[1]], dtype=float)


def make_quad_grid(xlim=(-6.0, 6.0), ylim=(-3.0, 3.0), n=160):
    """3D surface와 contour가 공유할 grid를 만든다."""
    x = np.linspace(xlim[0], xlim[1], n)
    y = np.linspace(ylim[0], ylim[1], n)
    W0, W1 = np.meshgrid(x, y)
    Z = 0.1 * W0 ** 2 + 2.0 * W1 ** 2
    return W0, W1, Z


def run_plain_gd_path(start=(5.0, 2.5), lr=0.12, steps=35):
    """V02용 plain gradient descent path.

    이 함수는 optimizer state를 쓰지 않는다.
    따라서 V04 optimizer 비교 전, learning rate와 gradient 방향만 보는 기준선이다.
    """
    w = np.array(start, dtype=float)
    path = [w.copy()]
    losses = [quad_loss(w)]
    for _ in range(steps):
        g = quad_grad(w)
        w = w - lr * g
        path.append(w.copy())
        losses.append(quad_loss(w))
    return np.vstack(path), np.array(losses)


def _plot_path_on_3d(ax, path, losses, label, color=None):
    """3D surface 위에 trajectory를 올리는 작은 helper."""
    ax.plot(path[:, 0], path[:, 1], losses, marker="o", markersize=2.5, label=label, color=color)


# %% [markdown]
# ## V02-A. 1D derivative, tangent, finite difference
#
# 이 셀은 미분을 "수식"이 아니라 "현재점의 기울기"로 보여준다.
# finite difference와 analytic derivative를 같이 놓아 gradient check의 의미도 연결한다.

# %%
def f1(x):
    """1D toy loss: minimum is at x=3."""
    return (x - 3.0) ** 2


def df1(x):
    """Analytic derivative of f1."""
    return 2.0 * (x - 3.0)


def plot_1d_derivative_tangent(x0=5.0, lr=0.25, h_values=(1e-1, 1e-2, 1e-3)):
    """1D tangent line, finite difference, and one-step update.

    주석 포인트:
    - grad는 현재점에서 loss가 증가하는 방향의 slope다.
    - update는 x_new = x - lr * grad 이므로 grad 반대 방향으로 이동한다.
    - h가 작아지면 finite difference slope가 analytic derivative에 가까워진다.
    """
    grad = df1(x0)
    x_new = x0 - lr * grad

    xs = np.linspace(0, 7, 300)
    tangent = f1(x0) + grad * (xs - x0)

    slope_rows = []
    for h in h_values:
        finite_diff = (f1(x0 + h) - f1(x0 - h)) / (2 * h)
        slope_rows.append({"h": h, "finite_difference": finite_diff, "analytic_df": grad})
    slope_table = pd.DataFrame(slope_rows)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(xs, f1(xs), label="f(x)=(x-3)^2")
    axes[0].plot(xs, tangent, "--", label="tangent at x0")
    axes[0].scatter([x0], [f1(x0)], s=80, label="current point")
    axes[0].scatter([x_new], [f1(x_new)], s=80, label="after one GD step")
    axes[0].annotate(
        "update = -lr * grad",
        xy=(x_new, f1(x_new)),
        xytext=(x0, f1(x0) + 3),
        arrowprops={"arrowstyle": "->", "lw": 2},
    )
    axes[0].set_title("1D derivative: tangent and GD update")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("loss")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].axis("off")
    axes[1].set_title("finite difference vs analytic derivative")
    table = axes[1].table(
        cellText=np.round(slope_table.to_numpy(), 6),
        colLabels=slope_table.columns,
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.4)
    plt.tight_layout()
    return fig, slope_table


# %% [markdown]
# ## V02-B. 2D loss surface multi-view
#
# 같은 2D loss를 3D surface, 평면도(top), 정면도(front), 측면도(side)로 나눠 본다.
# 3D 한 장만 보면 slope/curvature를 오해하기 쉬우므로 projection view를 함께 둔다.

# %%
def plot_quadratic_multiview(path=None, losses=None, title_prefix="V02 quadratic loss"):
    """3D surface + top/front/side view for a 2D loss.

    - 3D: 전체 loss basin의 형태를 본다.
    - top: contour 간격과 trajectory의 zig-zag를 본다.
    - front: w1=0 단면에서 w0 축 curvature를 본다.
    - side: w0=0 단면에서 w1 축 curvature를 본다.
    """
    if path is None or losses is None:
        path, losses = run_plain_gd_path()

    W0, W1, Z = make_quad_grid()
    fig = plt.figure(figsize=(13, 10))

    ax3d = fig.add_subplot(2, 2, 1, projection="3d")
    ax3d.plot_surface(W0, W1, Z, cmap="viridis", alpha=0.72, linewidth=0)
    _plot_path_on_3d(ax3d, path, losses, "GD path", color="crimson")
    ax3d.set_title(f"{title_prefix}: 3D surface")
    ax3d.set_xlabel("w0")
    ax3d.set_ylabel("w1")
    ax3d.set_zlabel("loss")
    ax3d.legend()

    ax_top = fig.add_subplot(2, 2, 2)
    ax_top.contour(W0, W1, Z, levels=28, cmap="viridis")
    ax_top.plot(path[:, 0], path[:, 1], "o-", color="crimson", markersize=3)
    ax_top.set_title("top view: contour 평면도")
    ax_top.set_xlabel("w0")
    ax_top.set_ylabel("w1")
    ax_top.set_aspect("equal")
    ax_top.grid(True, alpha=0.25)

    w0_axis = np.linspace(-6, 6, 300)
    ax_front = fig.add_subplot(2, 2, 3)
    ax_front.plot(w0_axis, [quad_loss([x, 0.0]) for x in w0_axis], label="w1 fixed at 0")
    ax_front.plot(path[:, 0], losses, "o-", color="crimson", markersize=3, label="path projected")
    ax_front.set_title("front view: w0-loss 정면도")
    ax_front.set_xlabel("w0")
    ax_front.set_ylabel("loss")
    ax_front.grid(True, alpha=0.3)
    ax_front.legend()

    w1_axis = np.linspace(-3, 3, 300)
    ax_side = fig.add_subplot(2, 2, 4)
    ax_side.plot(w1_axis, [quad_loss([0.0, y]) for y in w1_axis], label="w0 fixed at 0")
    ax_side.plot(path[:, 1], losses, "o-", color="crimson", markersize=3, label="path projected")
    ax_side.set_title("side view: w1-loss 측면도")
    ax_side.set_xlabel("w1")
    ax_side.set_ylabel("loss")
    ax_side.grid(True, alpha=0.3)
    ax_side.legend()

    plt.tight_layout()
    return fig


def plot_gradient_field_and_partial_slices(step=20):
    """Gradient vector field and partial derivative slices.

    이 시각화는 gradient가 2D vector라는 점을 보여준다.
    각 화살표는 해당 위치에서 loss가 증가하는 방향이다.
    """
    x = np.linspace(-5, 5, step)
    y = np.linspace(-2.5, 2.5, step)
    W0, W1 = np.meshgrid(x, y)
    G0 = 0.2 * W0
    G1 = 4.0 * W1
    Z = 0.1 * W0 ** 2 + 2.0 * W1 ** 2

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].contour(W0, W1, Z, levels=20, cmap="Greys")
    axes[0].quiver(W0, W1, G0, G1, color="tab:red", alpha=0.75)
    axes[0].set_title("gradient field: loss 증가 방향")
    axes[0].set_xlabel("w0")
    axes[0].set_ylabel("w1")
    axes[0].set_aspect("equal")

    axes[1].plot(x, 0.2 * x, label="partial dL/dw0")
    axes[1].axhline(0, color="black", lw=1)
    axes[1].set_title("front derivative slice: dL/dw0")
    axes[1].set_xlabel("w0")
    axes[1].set_ylabel("gradient component")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    axes[2].plot(y, 4.0 * y, label="partial dL/dw1", color="tab:orange")
    axes[2].axhline(0, color="black", lw=1)
    axes[2].set_title("side derivative slice: dL/dw1")
    axes[2].set_xlabel("w1")
    axes[2].set_ylabel("gradient component")
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    return fig


# %% [markdown]
# ## V01/V05. PCA EDA multi-view
#
# Iris는 4D feature matrix다. 2D scatter 하나로는 전체 구조를 설명할 수 없으므로
# PCA 2D, PCA 3D, PC1-PC2/PC1-PC3/PC2-PC3 projection을 함께 제공한다.

# %%
def _fit_pca_views(X, y, n_components=3):
    """Train-only scaler + PCA helper for tabular EDA.

    이 helper는 leakage 방지를 위해 호출자가 이미 split한 train data에 fit하는 방식으로도
    확장할 수 있다. 여기서는 전체 Iris 구조를 설명하는 EDA view로만 사용한다.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA(n_components=n_components, random_state=SEED)
    coords = pca.fit_transform(X_scaled)
    return coords, pca


def plot_iris_pca_multiview():
    """Iris 4D data를 PCA 2D/3D와 정면/측면 projection으로 본다."""
    iris = load_iris()
    X = iris.data.astype(float)
    y = iris.target.astype(int)
    coords, pca = _fit_pca_views(X, y, n_components=3)
    names = iris.target_names

    fig = plt.figure(figsize=(15, 11))

    ax_2d = fig.add_subplot(2, 3, 1)
    for cls in np.unique(y):
        mask = y == cls
        ax_2d.scatter(coords[mask, 0], coords[mask, 1], label=names[cls], alpha=0.8)
    ax_2d.set_title("PCA 2D: PC1-PC2 평면도")
    ax_2d.set_xlabel("PC1")
    ax_2d.set_ylabel("PC2")
    ax_2d.grid(True, alpha=0.3)
    ax_2d.legend()

    ax_3d = fig.add_subplot(2, 3, 2, projection="3d")
    for cls in np.unique(y):
        mask = y == cls
        ax_3d.scatter(coords[mask, 0], coords[mask, 1], coords[mask, 2], label=names[cls], alpha=0.75)
    ax_3d.set_title("PCA 3D: high-dimensional geometry")
    ax_3d.set_xlabel("PC1")
    ax_3d.set_ylabel("PC2")
    ax_3d.set_zlabel("PC3")

    ax_var = fig.add_subplot(2, 3, 3)
    ax_var.bar(["PC1", "PC2", "PC3"], pca.explained_variance_ratio_, color=["#4e79a7", "#f28e2b", "#59a14f"])
    ax_var.set_title("explained variance ratio")
    ax_var.set_ylim(0, 1)
    ax_var.grid(True, axis="y", alpha=0.3)

    pairs = [("PC1", "PC2", 0, 1), ("PC1", "PC3", 0, 2), ("PC2", "PC3", 1, 2)]
    for ax_i, (name_x, name_y, i, j) in enumerate(pairs, start=4):
        ax = fig.add_subplot(2, 3, ax_i)
        for cls in np.unique(y):
            mask = y == cls
            ax.scatter(coords[mask, i], coords[mask, j], label=names[cls], alpha=0.75)
        view_name = "평면도" if (i, j) == (0, 1) else ("정면도" if (i, j) == (0, 2) else "측면도")
        ax.set_title(f"{name_x}-{name_y} {view_name}")
        ax.set_xlabel(name_x)
        ax.set_ylabel(name_y)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig, pd.DataFrame(
        {
            "component": ["PC1", "PC2", "PC3"],
            "explained_variance_ratio": pca.explained_variance_ratio_,
        }
    )


def plot_scaling_effect_on_pca():
    """Raw PCA와 StandardScaler PCA를 비교한다.

    PCA는 scale에 민감하다. 이 그림은 V01의 split-before-fit/scaling 원칙이
    단순 전처리 규칙이 아니라 geometry 자체를 바꾸는 규칙임을 보여준다.
    """
    iris = load_iris()
    X = iris.data.astype(float)
    y = iris.target.astype(int)

    raw_coords = PCA(n_components=2, random_state=SEED).fit_transform(X)
    scaled_coords = PCA(n_components=2, random_state=SEED).fit_transform(StandardScaler().fit_transform(X))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, coords, title in [
        (axes[0], raw_coords, "PCA on raw features"),
        (axes[1], scaled_coords, "PCA after StandardScaler"),
    ]:
        for cls in np.unique(y):
            mask = y == cls
            ax.scatter(coords[mask, 0], coords[mask, 1], label=iris.target_names[cls], alpha=0.75)
        ax.set_title(title)
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.grid(True, alpha=0.3)
        ax.legend()
    plt.tight_layout()
    return fig


def plot_generic_eda_dashboard(df: pd.DataFrame, target_col: str | None = None):
    """Small DataFrame EDA dashboard.

    - missing bar: preprocessing risk 확인
    - dtype count: numeric/categorical split 확인
    - correlation heatmap: numeric feature relationship 확인
    - PCA 2D: numeric columns가 2개 이상일 때만 실행
    """
    numeric = df.select_dtypes(include=[np.number]).copy()
    missing = df.isna().sum().sort_values(ascending=False)
    dtype_counts = df.dtypes.astype(str).value_counts()

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    missing_nonzero = missing[missing > 0]
    if len(missing_nonzero):
        missing_nonzero.plot(kind="bar", ax=axes[0, 0], color="#e15759")
        axes[0, 0].set_ylabel("count")
    else:
        axes[0, 0].text(0.5, 0.5, "no missing values in preview", ha="center", va="center")
        axes[0, 0].set_xticks([])
        axes[0, 0].set_yticks([])
    axes[0, 0].set_title("missing values by column")

    dtype_counts.plot(kind="bar", ax=axes[0, 1], color="#4e79a7")
    axes[0, 1].set_title("dtype counts")
    axes[0, 1].set_ylabel("count")

    if numeric.shape[1] >= 2:
        corr = numeric.corr(numeric_only=True)
        im = axes[1, 0].imshow(corr.to_numpy(), cmap="coolwarm", vmin=-1, vmax=1)
        axes[1, 0].set_xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
        axes[1, 0].set_yticks(range(len(corr.index)), corr.index)
        axes[1, 0].set_title("numeric correlation")
        fig.colorbar(im, ax=axes[1, 0], fraction=0.046)
    else:
        axes[1, 0].axis("off")
        axes[1, 0].set_title("numeric correlation skipped")

    if numeric.shape[1] >= 2 and len(numeric.dropna()) >= 3:
        X = numeric.fillna(numeric.mean(numeric_only=True)).to_numpy()
        coords = PCA(n_components=2, random_state=SEED).fit_transform(StandardScaler().fit_transform(X))
        if target_col is not None and target_col in df:
            labels = pd.Categorical(df[target_col]).codes
            scatter = axes[1, 1].scatter(coords[:, 0], coords[:, 1], c=labels, cmap="tab10", alpha=0.8)
            axes[1, 1].legend(*scatter.legend_elements(), title=target_col, loc="best")
        else:
            axes[1, 1].scatter(coords[:, 0], coords[:, 1], alpha=0.8)
        axes[1, 1].set_title("numeric PCA 2D EDA view")
        axes[1, 1].set_xlabel("PC1")
        axes[1, 1].set_ylabel("PC2")
        axes[1, 1].grid(True, alpha=0.3)
    else:
        axes[1, 1].axis("off")
        axes[1, 1].set_title("PCA skipped: not enough numeric columns")

    plt.tight_layout()
    return fig


def _numeric_columns(df: pd.DataFrame, max_unique_ratio=0.9):
    """Return numeric columns suitable for continuous association views.

    ID처럼 모든 값이 거의 unique인 numeric column은 correlation 해석을 흐릴 수 있다.
    다만 notebook preview에서는 column 수가 작으므로 ratio 기준만 느슨하게 적용한다.
    """
    cols = []
    for col in df.select_dtypes(include=[np.number]).columns:
        non_null = df[col].dropna()
        if len(non_null) < 3:
            continue
        unique_ratio = non_null.nunique() / max(len(non_null), 1)
        if unique_ratio <= max_unique_ratio or len(non_null) < 30:
            cols.append(col)
    return cols


def _categorical_columns(df: pd.DataFrame, max_unique=20):
    """Return columns suitable for categorical association views."""
    cols = []
    for col in df.columns:
        series = df[col].dropna()
        if len(series) < 3:
            continue
        is_object_like = not pd.api.types.is_numeric_dtype(series)
        is_low_cardinality_numeric = pd.api.types.is_numeric_dtype(series) and series.nunique() <= max_unique
        if is_object_like or is_low_cardinality_numeric:
            cols.append(col)
    return cols


def _optional_scipy_stats():
    """Return scipy.stats when available.

    The notebook's required stack stays numpy/pandas/matplotlib/sklearn.
    If scipy is unavailable, test statistics are still shown and p-values become NaN.
    """
    try:
        from scipy import stats  # type: ignore
    except Exception:
        return None
    return stats


def _boxplot_with_labels(ax, values, labels):
    """Matplotlib-compatible boxplot label wrapper."""
    try:
        return ax.boxplot(values, tick_labels=labels)
    except TypeError:
        return ax.boxplot(values, labels=labels)


def chi_square_pair_test(df: pd.DataFrame, col_a: str, col_b: str):
    """Chi-square independence test summary for two categorical columns.

    Cramer's V is the association-strength companion to the chi-square statistic.
    A low p-value indicates dependence is plausible, but does not imply causality.
    """
    observed = pd.crosstab(df[col_a], df[col_b])
    values = observed.to_numpy(dtype=float)
    n = values.sum()
    if n == 0 or values.shape[0] < 2 or values.shape[1] < 2:
        empty = pd.DataFrame(columns=["test", "value", "meaning"])
        return observed, pd.DataFrame(index=observed.index, columns=observed.columns), empty

    row_sum = values.sum(axis=1, keepdims=True)
    col_sum = values.sum(axis=0, keepdims=True)
    expected_values = row_sum @ col_sum / n
    valid = expected_values > 0
    chi2_value = float(((values - expected_values) ** 2 / np.where(valid, expected_values, 1.0))[valid].sum())
    dof = int((values.shape[0] - 1) * (values.shape[1] - 1))
    stats = _optional_scipy_stats()
    p_value = float(stats.chi2.sf(chi2_value, dof)) if stats is not None and dof > 0 else np.nan
    v_value = cramers_v_from_table(observed)
    expected = pd.DataFrame(expected_values, index=observed.index, columns=observed.columns)
    summary = pd.DataFrame(
        [
            ["chi-square statistic", chi2_value, "observed count가 independence 기대 count에서 벗어난 정도"],
            ["degrees of freedom", dof, "(row_count-1)*(column_count-1)"],
            ["p-value", p_value, "small p suggests categorical dependence, not causality"],
            ["Cramer's V", v_value, "0~1 categorical association strength"],
            ["n", int(n), "valid paired records"],
        ],
        columns=["test", "value", "meaning"],
    )
    return observed, expected, summary


def cramers_v_from_table(table: pd.DataFrame) -> float:
    """Cramer's V for categorical-categorical association.

    기본 stack에서 scipy 없이 chi-square statistic을 직접 계산한다.
    값 범위는 0~1이며, 0은 거의 독립, 1은 강한 association을 뜻한다.
    이 값은 관계 강도이며 p-value 검정 자체는 아니다.
    """
    observed = table.to_numpy(dtype=float)
    n = observed.sum()
    if n == 0:
        return np.nan
    row_sum = observed.sum(axis=1, keepdims=True)
    col_sum = observed.sum(axis=0, keepdims=True)
    expected = row_sum @ col_sum / n
    valid = expected > 0
    if not np.any(valid):
        return np.nan
    chi2 = ((observed - expected) ** 2 / np.where(valid, expected, 1.0))[valid].sum()
    r, k = observed.shape
    denom = n * max(min(k - 1, r - 1), 1)
    return float(np.sqrt(chi2 / denom))


def categorical_association_matrix(df: pd.DataFrame, cat_cols=None, max_unique=20):
    """Cramer's V matrix for categorical-categorical relationships."""
    if cat_cols is None:
        cat_cols = _categorical_columns(df, max_unique=max_unique)
    cat_cols = list(dict.fromkeys(cat_cols))
    matrix = pd.DataFrame(np.nan, index=cat_cols, columns=cat_cols, dtype=float)
    for a in cat_cols:
        for b in cat_cols:
            if a == b:
                matrix.loc[a, b] = 1.0
                continue
            table = pd.crosstab(df[a], df[b])
            matrix.loc[a, b] = cramers_v_from_table(table)
    return matrix


def chi_square_categorical_pair_table(df: pd.DataFrame, cat_cols=None, max_unique=20):
    """Pairwise chi-square/Cramer's V table for categorical-categorical EDA."""
    if cat_cols is None:
        cat_cols = _categorical_columns(df, max_unique=max_unique)
    cat_cols = list(dict.fromkeys(cat_cols))
    rows = []
    for i, a in enumerate(cat_cols):
        for b in cat_cols[i + 1:]:
            _, _, summary = chi_square_pair_test(df, a, b)
            if summary.empty:
                continue
            lookup = dict(zip(summary["test"], summary["value"]))
            rows.append(
                {
                    "cat_a": a,
                    "cat_b": b,
                    "chi2": lookup.get("chi-square statistic", np.nan),
                    "dof": lookup.get("degrees of freedom", np.nan),
                    "p_value": lookup.get("p-value", np.nan),
                    "cramers_v": lookup.get("Cramer's V", np.nan),
                    "n": lookup.get("n", np.nan),
                }
            )
    return pd.DataFrame(rows).sort_values("cramers_v", ascending=False) if rows else pd.DataFrame()


def correlation_ratio(categories, values) -> float:
    """Eta squared style continuous-categorical association.

    categories가 values의 평균 차이를 얼마나 설명하는지 본다.
    0은 group mean 차이가 작다는 뜻이고, 1에 가까우면 group별 평균 차이가 크다.
    """
    frame = pd.DataFrame({"category": categories, "value": values}).dropna()
    if frame.empty:
        return np.nan
    overall_mean = frame["value"].mean()
    total_ss = ((frame["value"] - overall_mean) ** 2).sum()
    if total_ss == 0:
        return 0.0
    between_ss = 0.0
    for _, group in frame.groupby("category"):
        between_ss += len(group) * (group["value"].mean() - overall_mean) ** 2
    return float(between_ss / total_ss)


def numeric_categorical_association_matrix(df: pd.DataFrame, num_cols=None, cat_cols=None):
    """Eta squared matrix for continuous-categorical relationships."""
    if num_cols is None:
        num_cols = _numeric_columns(df)
    if cat_cols is None:
        cat_cols = _categorical_columns(df)
    matrix = pd.DataFrame(np.nan, index=num_cols, columns=cat_cols, dtype=float)
    for num in num_cols:
        for cat in cat_cols:
            matrix.loc[num, cat] = correlation_ratio(df[cat], df[num])
    return matrix


def continuous_by_category_test_table(df: pd.DataFrame, numeric_col: str, category_col: str):
    """Group summary plus ANOVA/Welch t-test for continuous-categorical EDA.

    This is an exploratory diagnostic, not final confirmatory inference.
    It helps decide whether a model needs category effects, interactions, or stratified review.
    """
    data = df[[numeric_col, category_col]].dropna().copy()
    data[category_col] = pd.Categorical(data[category_col])
    grouped = [grp[numeric_col].to_numpy(dtype=float) for _, grp in data.groupby(category_col, observed=True)]
    labels = [str(label) for label in data[category_col].cat.categories if label in set(data[category_col])]
    group_stats = data.groupby(category_col, observed=True)[numeric_col].agg(["count", "mean", "median", "std", "min", "max"])
    group_stats["iqr"] = data.groupby(category_col, observed=True)[numeric_col].quantile(0.75) - data.groupby(category_col, observed=True)[numeric_col].quantile(0.25)

    eta_sq = correlation_ratio(data[category_col], data[numeric_col])
    n = sum(len(g) for g in grouped)
    k = len(grouped)
    grand_mean = data[numeric_col].mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in grouped if len(g))
    ss_within = sum(((g - g.mean()) ** 2).sum() for g in grouped if len(g))
    f_value = np.nan
    anova_p = np.nan
    if k >= 2 and n > k and ss_within > 0:
        f_value = float((ss_between / (k - 1)) / (ss_within / (n - k)))
        stats = _optional_scipy_stats()
        anova_p = float(stats.f.sf(f_value, k - 1, n - k)) if stats is not None else np.nan

    welch_t = np.nan
    welch_p = np.nan
    if k == 2 and all(len(g) >= 2 for g in grouped):
        g1, g2 = grouped
        v1, v2 = g1.var(ddof=1), g2.var(ddof=1)
        se = np.sqrt(v1 / len(g1) + v2 / len(g2))
        if se > 0:
            welch_t = float((g1.mean() - g2.mean()) / se)
            df_num = (v1 / len(g1) + v2 / len(g2)) ** 2
            df_den = (v1 ** 2) / (len(g1) ** 2 * (len(g1) - 1)) + (v2 ** 2) / (len(g2) ** 2 * (len(g2) - 1))
            welch_df = df_num / df_den if df_den > 0 else np.nan
            stats = _optional_scipy_stats()
            welch_p = float(2 * stats.t.sf(abs(welch_t), welch_df)) if stats is not None and not np.isnan(welch_df) else np.nan

    test_summary = pd.DataFrame(
        [
            ["eta squared", eta_sq, "category가 numeric variance를 설명하는 비율형 강도"],
            ["one-way ANOVA F", f_value, "group mean 차이가 within-group noise 대비 큰지"],
            ["ANOVA p-value", anova_p, "small p suggests group mean difference, not causality"],
            ["Welch t statistic", welch_t, "binary category 전용 평균 차이 진단"],
            ["Welch t p-value", welch_p, "binary category 전용 p-value"],
        ],
        columns=["test", "value", "meaning"],
    )
    return group_stats, test_summary


def plot_categorical_100pct_stacked(df: pd.DataFrame, x_col: str, hue_col: str):
    """100% stacked bar for categorical-categorical composition."""
    counts = pd.crosstab(df[x_col], df[hue_col])
    pct = counts.div(counts.sum(axis=1), axis=0).fillna(0.0)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    pct.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    ax.set_title(f"100% stacked: {hue_col} within {x_col}")
    ax.set_ylabel("row proportion")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=20)
    ax.legend(title=hue_col, loc="center left", bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()
    return fig, pct


def plot_continuous_by_category_gallery(df: pd.DataFrame, numeric_col: str, category_col: str):
    """Box/hist/summary view for continuous-categorical EDA."""
    data = df[[numeric_col, category_col]].dropna().copy()
    data[category_col] = pd.Categorical(data[category_col])
    groups = [(str(label), grp[numeric_col].to_numpy(dtype=float)) for label, grp in data.groupby(category_col, observed=True)]
    labels = [label for label, _ in groups]
    values = [vals for _, vals in groups]
    group_stats, test_summary = continuous_by_category_test_table(data, numeric_col, category_col)

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    _boxplot_with_labels(axes[0], values, labels)
    axes[0].set_title(f"{numeric_col} by {category_col}")
    axes[0].set_ylabel(numeric_col)
    axes[0].tick_params(axis="x", rotation=20)
    axes[0].grid(True, axis="y", alpha=0.3)

    for label, vals in groups:
        axes[1].hist(vals, bins=min(10, max(4, len(vals) // 2)), alpha=0.45, label=label)
    axes[1].set_title("grouped histogram")
    axes[1].set_xlabel(numeric_col)
    axes[1].legend(title=category_col)

    order = group_stats.sort_values("median", ascending=False)
    axes[2].bar(order.index.astype(str), order["median"], color="#4e79a7")
    axes[2].set_title("median by category")
    axes[2].set_ylabel("median")
    axes[2].tick_params(axis="x", rotation=20)
    axes[2].grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    return fig, group_stats, test_summary


def point_biserial_target_table(df: pd.DataFrame, target_col: str, num_cols=None):
    """Pearson correlation between numeric columns and a binary target.

    target_col이 binary categorical이면 point-biserial correlation과 같은 해석을 쓴다.
    target이 binary가 아니면 빈 table을 반환한다.
    """
    if target_col not in df:
        return pd.DataFrame(columns=["numeric", "target", "point_biserial_r"])
    target = df[target_col].dropna()
    categories = pd.Categorical(target)
    if len(categories.categories) != 2:
        return pd.DataFrame(columns=["numeric", "target", "point_biserial_r"])
    if num_cols is None:
        num_cols = _numeric_columns(df)
    rows = []
    encoded = pd.Series(pd.Categorical(df[target_col]).codes, index=df.index).replace(-1, np.nan)
    for col in num_cols:
        if col == target_col:
            continue
        joined = pd.DataFrame({"x": df[col], "y": encoded}).dropna()
        if len(joined) < 3 or joined["x"].std() == 0:
            continue
        rows.append({"numeric": col, "target": target_col, "point_biserial_r": joined["x"].corr(joined["y"])})
    return pd.DataFrame(rows).sort_values("point_biserial_r", key=lambda s: s.abs(), ascending=False)


def _imshow_table(ax, table: pd.DataFrame, title: str, vmin=None, vmax=None, cmap="viridis"):
    """Heatmap helper that handles empty tables gracefully."""
    ax.set_title(title)
    if table is None or table.empty:
        ax.text(0.5, 0.5, "not enough columns", ha="center", va="center")
        ax.set_xticks([])
        ax.set_yticks([])
        return None
    im = ax.imshow(table.to_numpy(dtype=float), aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(table.columns)), table.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(table.index)), table.index)
    return im


def plot_mixed_association_dashboard(df: pd.DataFrame, target_col: str | None = None, max_unique=20):
    """Continuous/categorical association dashboard.

    포함 관계:
    - continuous-continuous: Pearson correlation, Spearman rank correlation, Kendall tau
    - categorical-categorical: chi-square independence table and Cramer's V
    - continuous-categorical: eta squared / correlation ratio
    - binary target: point-biserial correlation table
    """
    num_cols = _numeric_columns(df)
    cat_cols = _categorical_columns(df, max_unique=max_unique)

    numeric = df[num_cols].copy()
    pearson = numeric.corr(method="pearson") if len(num_cols) >= 2 else pd.DataFrame()
    spearman = numeric.corr(method="spearman") if len(num_cols) >= 2 else pd.DataFrame()
    kendall = numeric.corr(method="kendall") if len(num_cols) >= 2 else pd.DataFrame()
    cramers_v = categorical_association_matrix(df, cat_cols=cat_cols, max_unique=max_unique) if len(cat_cols) >= 2 else pd.DataFrame()
    chi_square = chi_square_categorical_pair_table(df, cat_cols=cat_cols, max_unique=max_unique) if len(cat_cols) >= 2 else pd.DataFrame()
    eta_sq = numeric_categorical_association_matrix(df, num_cols=num_cols, cat_cols=cat_cols) if num_cols and cat_cols else pd.DataFrame()
    point_biserial = point_biserial_target_table(df, target_col, num_cols=num_cols) if target_col else pd.DataFrame()

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    im = _imshow_table(axes[0, 0], pearson, "continuous-continuous: Pearson r", vmin=-1, vmax=1, cmap="coolwarm")
    if im is not None:
        fig.colorbar(im, ax=axes[0, 0], fraction=0.046)
    im = _imshow_table(axes[0, 1], spearman, "continuous-continuous: Spearman rank r", vmin=-1, vmax=1, cmap="coolwarm")
    if im is not None:
        fig.colorbar(im, ax=axes[0, 1], fraction=0.046)
    im = _imshow_table(axes[0, 2], kendall, "ordinal/small sample: Kendall tau", vmin=-1, vmax=1, cmap="coolwarm")
    if im is not None:
        fig.colorbar(im, ax=axes[0, 2], fraction=0.046)
    im = _imshow_table(axes[1, 0], cramers_v, "categorical-categorical: Cramer's V", vmin=0, vmax=1, cmap="magma")
    if im is not None:
        fig.colorbar(im, ax=axes[1, 0], fraction=0.046)
    im = _imshow_table(axes[1, 1], eta_sq, "continuous-categorical: eta squared", vmin=0, vmax=1, cmap="viridis")
    if im is not None:
        fig.colorbar(im, ax=axes[1, 1], fraction=0.046)
    axes[1, 2].set_title("binary target: point-biserial r")
    if point_biserial.empty:
        axes[1, 2].text(0.5, 0.5, "binary target unavailable", ha="center", va="center")
        axes[1, 2].set_xticks([])
        axes[1, 2].set_yticks([])
    else:
        ordered = point_biserial.sort_values("point_biserial_r")
        axes[1, 2].barh(ordered["numeric"], ordered["point_biserial_r"], color="#4e79a7")
        axes[1, 2].axvline(0, color="black", lw=1)
        axes[1, 2].set_xlabel("r")
    plt.tight_layout()

    tables = {
        "numeric_columns": pd.DataFrame({"numeric": num_cols}),
        "categorical_columns": pd.DataFrame({"categorical": cat_cols}),
        "pearson": pearson,
        "spearman": spearman,
        "kendall": kendall,
        "cramers_v": cramers_v,
        "chi_square": chi_square,
        "eta_squared": eta_sq,
        "point_biserial": point_biserial,
    }
    return fig, tables


def plot_covariance_to_correlation_demo():
    """Show why covariance needs correlation normalization.

    공분산은 방향을 알려주지만 단위/스케일에 의존한다.
    상관계수는 공분산을 표준편차로 나누어 [-1, 1] 범위로 정규화한다.
    """
    x = np.array([10, 12, 13, 15, 18, 20], dtype=float)
    y = np.array([21, 24, 22, 28, 31, 33], dtype=float)
    x_centered = x - x.mean()
    y_centered = y - y.mean()
    product = x_centered * y_centered
    cov = product.sum() / (len(x) - 1)
    corr = product.sum() / np.sqrt((x_centered ** 2).sum() * (y_centered ** 2).sum())

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].scatter(x, y, s=90, edgecolor="black")
    axes[0].set_title("raw scatter")
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")
    axes[0].grid(True, alpha=0.3)

    axes[1].bar(range(len(product)), product, color=np.where(product >= 0, "#59a14f", "#e15759"))
    axes[1].axhline(0, color="black", lw=1)
    axes[1].set_title("centered product: (x-xbar)(y-ybar)")
    axes[1].set_xlabel("sample")
    axes[1].set_ylabel("product")

    axes[2].scatter(x_centered / x.std(ddof=1), y_centered / y.std(ddof=1), s=90, edgecolor="black")
    axes[2].axhline(0, color="black", lw=1)
    axes[2].axvline(0, color="black", lw=1)
    axes[2].set_title("standardized scatter")
    axes[2].set_xlabel("z(X)")
    axes[2].set_ylabel("z(Y)")
    axes[2].grid(True, alpha=0.3)
    plt.tight_layout()

    table = pd.DataFrame(
        [
            ["sample covariance", cov, "scale-dependent direction/size"],
            ["Pearson r", corr, "normalized linear association"],
        ],
        columns=["statistic", "value", "meaning"],
    )
    return fig, table


def plot_simple_regression_residual_diagnostics(df: pd.DataFrame, x_col: str, y_col: str, group_col: str | None = None):
    """Simple linear regression diagnostic from correlation to residuals.

    중심 흐름:
    1. scatter/correlation으로 선형 관계 후보를 본다.
    2. simple regression line을 fit한다.
    3. residual vs fitted, residual histogram, group별 residual을 본다.
    4. residual pattern이 남으면 변수 추가, transformation, interaction, nonlinear model을 검토한다.
    """
    cols = [x_col, y_col] + ([group_col] if group_col else [])
    data = df[cols].dropna().copy()
    x = data[x_col].to_numpy(dtype=float)
    y = data[y_col].to_numpy(dtype=float)
    X_design = np.c_[np.ones(len(x)), x]
    intercept, slope = np.linalg.lstsq(X_design, y, rcond=None)[0]
    y_hat = intercept + slope * x
    residual = y - y_hat
    ss_res = float((residual ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    metrics = pd.DataFrame(
        [
            ["covariance", np.cov(x, y, ddof=1)[0, 1], "direction is meaningful, scale is not directly comparable"],
            ["Pearson r", pd.Series(x).corr(pd.Series(y), method="pearson"), "linear association"],
            ["Spearman r", pd.Series(x).corr(pd.Series(y), method="spearman"), "monotonic rank association"],
            ["Kendall tau", pd.Series(x).corr(pd.Series(y), method="kendall"), "rank-pair agreement"],
            ["slope", slope, "predicted y change for +1 x"],
            ["intercept", intercept, "predicted y when x=0"],
            ["R^2", r2, "variance explained by simple line"],
            ["RMSE", float(np.sqrt(np.mean(residual ** 2))), "typical residual scale"],
        ],
        columns=["statistic", "value", "meaning"],
    )

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    if group_col:
        groups = pd.Categorical(data[group_col])
        scatter = axes[0, 0].scatter(x, y, c=groups.codes, cmap="tab10", edgecolor="black", alpha=0.8)
        axes[0, 0].legend(*scatter.legend_elements(), title=group_col, loc="best")
    else:
        axes[0, 0].scatter(x, y, edgecolor="black", alpha=0.8)
    order = np.argsort(x)
    axes[0, 0].plot(x[order], y_hat[order], color="red", lw=2, label="simple regression line")
    axes[0, 0].set_title(f"{y_col} ~ {x_col}")
    axes[0, 0].set_xlabel(x_col)
    axes[0, 0].set_ylabel(y_col)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()

    axes[0, 1].scatter(y_hat, residual, edgecolor="black", alpha=0.8)
    axes[0, 1].axhline(0, color="red", lw=2)
    axes[0, 1].set_title("residual vs fitted")
    axes[0, 1].set_xlabel("fitted")
    axes[0, 1].set_ylabel("residual")
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].hist(residual, bins=min(12, max(4, len(residual) // 3)), color="#4e79a7", edgecolor="white")
    axes[1, 0].axvline(0, color="red", lw=2)
    axes[1, 0].set_title("residual distribution")
    axes[1, 0].set_xlabel("residual")

    if group_col:
        grouped_residuals = [residual[groups.codes == code] for code in range(len(groups.categories))]
        _boxplot_with_labels(axes[1, 1], grouped_residuals, list(groups.categories))
        axes[1, 1].set_title("residual by category")
        axes[1, 1].tick_params(axis="x", rotation=20)
    else:
        axes[1, 1].scatter(y, y_hat, edgecolor="black", alpha=0.8)
        lim = [min(y.min(), y_hat.min()), max(y.max(), y_hat.max())]
        axes[1, 1].plot(lim, lim, color="red", lw=2)
        axes[1, 1].set_title("observed vs predicted")
        axes[1, 1].set_xlabel("observed")
        axes[1, 1].set_ylabel("predicted")
    axes[1, 1].grid(True, alpha=0.3)
    plt.tight_layout()
    return fig, metrics


def plot_pc_regression_residual_diagnostics(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str,
    group_col: str | None = None,
    n_components=2,
):
    """Use PCs as multivariate predictors and inspect residual patterns.

    다변수 feature를 바로 2D scatter로 볼 수 없을 때, PCA score를 model input 후보로 쓴다.
    여기서는 PC1/PC2로 target을 예측하는 작은 linear model을 만들고 residual pattern을 본다.
    """
    cols = feature_cols + [target_col] + ([group_col] if group_col else [])
    data = df[cols].dropna().copy()
    X_raw = data[feature_cols].to_numpy(dtype=float)
    y = data[target_col].to_numpy(dtype=float)
    X_scaled = StandardScaler().fit_transform(X_raw)
    pca = PCA(n_components=n_components, random_state=SEED)
    pcs = pca.fit_transform(X_scaled)
    X_design = np.c_[np.ones(len(pcs)), pcs]
    coef = np.linalg.lstsq(X_design, y, rcond=None)[0]
    y_hat = X_design @ coef
    residual = y - y_hat
    ss_res = float((residual ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    if pcs.shape[1] >= 2:
        sc = axes[0, 0].scatter(pcs[:, 0], pcs[:, 1], c=residual, cmap="coolwarm", edgecolor="black")
        fig.colorbar(sc, ax=axes[0, 0], fraction=0.046, label="residual")
        axes[0, 0].set_xlabel("PC1")
        axes[0, 0].set_ylabel("PC2")
        axes[0, 0].set_title("PC score space colored by residual")
    else:
        axes[0, 0].scatter(pcs[:, 0], residual, edgecolor="black")
        axes[0, 0].set_xlabel("PC1")
        axes[0, 0].set_ylabel("residual")
        axes[0, 0].set_title("PC1 vs residual")
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].scatter(y_hat, residual, edgecolor="black", alpha=0.8)
    axes[0, 1].axhline(0, color="red", lw=2)
    axes[0, 1].set_title("PC regression: residual vs fitted")
    axes[0, 1].set_xlabel("fitted")
    axes[0, 1].set_ylabel("residual")
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].bar([f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))], pca.explained_variance_ratio_)
    axes[1, 0].set_title("PC explained variance")
    axes[1, 0].set_ylim(0, 1)
    axes[1, 0].grid(True, axis="y", alpha=0.3)

    if group_col:
        groups = pd.Categorical(data[group_col])
        grouped_residuals = [residual[groups.codes == code] for code in range(len(groups.categories))]
        _boxplot_with_labels(axes[1, 1], grouped_residuals, list(groups.categories))
        axes[1, 1].set_title("PC regression residual by category")
        axes[1, 1].tick_params(axis="x", rotation=20)
    else:
        axes[1, 1].scatter(y, y_hat, edgecolor="black", alpha=0.8)
        lim = [min(y.min(), y_hat.min()), max(y.max(), y_hat.max())]
        axes[1, 1].plot(lim, lim, color="red", lw=2)
        axes[1, 1].set_title("observed vs predicted")
        axes[1, 1].set_xlabel("observed")
        axes[1, 1].set_ylabel("predicted")
    axes[1, 1].grid(True, alpha=0.3)
    plt.tight_layout()

    metrics = pd.DataFrame(
        [
            ["features", ", ".join(feature_cols), "PCA input columns"],
            ["target", target_col, "regression target"],
            ["PC count", n_components, "compressed multivariate predictors"],
            ["R^2", r2, "variance explained by PC linear model"],
            ["RMSE", float(np.sqrt(np.mean(residual ** 2))), "typical residual scale"],
        ],
        columns=["item", "value", "meaning"],
    )
    return fig, metrics


# %% [markdown]
# ## V03. Dense backward and derivative heatmap pack
#
# 이 셀은 dW/db/dX를 한 번에 계산하고 heatmap으로 보여준다.
# optimizer가 읽는 것은 dW/db이고, dX는 이전 layer로 보내는 gradient라는 점을 반복한다.

# %%
def plot_dense_backward_gradient_views(B=4, Din=3, Dout=2):
    """Dense backward shape and gradient heatmaps."""
    rng = np.random.default_rng(SEED)
    X = rng.normal(size=(B, Din))
    W = rng.normal(size=(Dout, Din))
    b = rng.normal(size=(Dout,))
    Z = X @ W.T + b

    # dZ는 다음 연산 또는 loss에서 현재 Dense output으로 되돌아온 upstream gradient다.
    dZ = rng.normal(size=(B, Dout))

    # 이 노트북 convention: W=(Dout,Din).
    # 따라서 dW는 dZ.T @ X이고 shape은 W와 같은 (Dout,Din)이다.
    dW = dZ.T @ X
    db = dZ.sum(axis=0)
    dX = dZ @ W

    assert Z.shape == (B, Dout)
    assert dW.shape == W.shape
    assert db.shape == b.shape
    assert dX.shape == X.shape

    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    mats = [
        ("X input", X),
        ("W parameter", W),
        ("Z = X @ W.T + b", Z),
        ("dW parameter gradient", dW),
        ("db bias gradient", db.reshape(1, -1)),
        ("dX to previous layer", dX),
    ]
    for ax, (title, mat) in zip(axes.ravel(), mats):
        im = ax.imshow(mat, aspect="auto", cmap="coolwarm")
        ax.set_title(title)
        ax.set_xlabel("axis 1")
        ax.set_ylabel("axis 0")
        fig.colorbar(im, ax=ax, fraction=0.046)
    plt.tight_layout()

    shape_table = pd.DataFrame(
        [
            ["X", X.shape, "forward input/cache"],
            ["W", W.shape, "parameter, optimizer updates"],
            ["b", b.shape, "parameter, optimizer updates"],
            ["Z", Z.shape, "Dense output"],
            ["dZ", dZ.shape, "upstream gradient"],
            ["dW", dW.shape, "parameter gradient read by optimizer"],
            ["db", db.shape, "parameter gradient read by optimizer"],
            ["dX", dX.shape, "gradient sent to previous layer"],
        ],
        columns=["object", "shape", "role"],
    )
    return fig, shape_table


def plot_activation_derivative_views():
    """ReLU forward, derivative mask, and gradient pass/block view."""
    rng = np.random.default_rng(SEED)
    Z = rng.normal(size=(5, 6))
    upstream = rng.normal(size=Z.shape)
    mask = Z > 0
    relu_out = Z * mask
    downstream = upstream * mask

    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
    for ax, title, mat, cmap in [
        (axes[0], "Z before ReLU", Z, "coolwarm"),
        (axes[1], "ReLU(Z)", relu_out, "viridis"),
        (axes[2], "ReLU derivative mask", mask.astype(float), "Greys"),
        (axes[3], "downstream grad", downstream, "coolwarm"),
    ]:
        im = ax.imshow(mat, aspect="auto", cmap=cmap)
        ax.set_title(title)
        fig.colorbar(im, ax=ax, fraction=0.046)
    plt.tight_layout()
    return fig


def plot_softmax_ce_delta_views():
    """Softmax probability and (p-y)/B gradient heatmaps."""
    logits = np.array(
        [
            [2.0, 0.2, -0.5],
            [0.1, 1.7, 0.3],
            [-0.4, 0.8, 2.2],
            [1.0, 0.7, 0.6],
        ],
        dtype=float,
    )
    y = np.array([0, 1, 2, 1])
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp_z = np.exp(shifted)
    probs = exp_z / exp_z.sum(axis=1, keepdims=True)
    y_onehot = np.eye(probs.shape[1])[y]
    delta = (probs - y_onehot) / len(y)

    assert np.allclose(probs.sum(axis=1), 1.0)
    assert np.allclose(delta.sum(axis=1), 0.0)

    fig, axes = plt.subplots(1, 4, figsize=(15, 3.5))
    for ax, title, mat, cmap in [
        (axes[0], "logits", logits, "coolwarm"),
        (axes[1], "softmax probabilities", probs, "viridis"),
        (axes[2], "one-hot labels", y_onehot, "Greys"),
        (axes[3], "(p-y)/B logits gradient", delta, "coolwarm"),
    ]:
        im = ax.imshow(mat, aspect="auto", cmap=cmap)
        ax.set_title(title)
        ax.set_xlabel("class")
        ax.set_ylabel("sample")
        fig.colorbar(im, ax=ax, fraction=0.046)
    plt.tight_layout()
    return fig


# %% [markdown]
# ## V04. Optimizer trajectory multi-view
#
# 이 셀은 SGD/Momentum/RMSProp/Adam을 같은 loss surface와 같은 시작점에서 비교한다.
# 각 optimizer는 같은 gradient를 받지만 state와 update rule 때문에 경로가 달라진다.

# %%
class Optimizer2D:
    """2D vector simulation용 최소 optimizer interface."""

    def __init__(self, lr):
        self.lr = lr
        self.history = []

    def update(self, w, grad):
        raise NotImplementedError

    def _record(self, grad, step):
        self.history.append(
            {
                "grad_norm": float(np.linalg.norm(grad)),
                "step_norm": float(np.linalg.norm(step)),
            }
        )


class SGD2D(Optimizer2D):
    def update(self, w, grad):
        step = -self.lr * grad
        self._record(grad, step)
        return w + step


class Momentum2D(Optimizer2D):
    def __init__(self, lr=0.05, beta=0.9):
        super().__init__(lr)
        self.beta = beta
        self.v = np.zeros(2)

    def update(self, w, grad):
        self.v = self.beta * self.v - self.lr * grad
        self._record(grad, self.v)
        self.history[-1]["velocity_norm"] = float(np.linalg.norm(self.v))
        return w + self.v


class RMSProp2D(Optimizer2D):
    def __init__(self, lr=0.08, beta=0.9, eps=1e-8):
        super().__init__(lr)
        self.beta = beta
        self.eps = eps
        self.s = np.zeros(2)

    def update(self, w, grad):
        self.s = self.beta * self.s + (1.0 - self.beta) * (grad ** 2)
        step = -self.lr * grad / (np.sqrt(self.s) + self.eps)
        self._record(grad, step)
        self.history[-1]["second_state_norm"] = float(np.linalg.norm(self.s))
        return w + step


class Adam2D(Optimizer2D):
    def __init__(self, lr=0.12, beta1=0.9, beta2=0.999, eps=1e-8):
        super().__init__(lr)
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = np.zeros(2)
        self.v = np.zeros(2)
        self.t = 0

    def update(self, w, grad):
        self.t += 1
        self.m = self.beta1 * self.m + (1.0 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1.0 - self.beta2) * (grad ** 2)
        m_hat = self.m / (1.0 - self.beta1 ** self.t)
        v_hat = self.v / (1.0 - self.beta2 ** self.t)
        step = -self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
        self._record(grad, step)
        self.history[-1]["first_state_norm"] = float(np.linalg.norm(self.m))
        self.history[-1]["second_state_norm"] = float(np.linalg.norm(self.v))
        return w + step


def simulate_optimizer_paths(start=(5.0, 2.5), steps=45):
    """Run all optimizers from the same point on the same gradient field."""
    configs = {
        "SGD": SGD2D(lr=0.18),
        "Momentum": Momentum2D(lr=0.05, beta=0.9),
        "RMSProp": RMSProp2D(lr=0.08, beta=0.9),
        "Adam": Adam2D(lr=0.12),
    }
    results = {}
    for name, opt in configs.items():
        w = np.array(start, dtype=float)
        path = [w.copy()]
        losses = [quad_loss(w)]
        for _ in range(steps):
            grad = quad_grad(w)
            w = opt.update(w, grad)
            path.append(w.copy())
            losses.append(quad_loss(w))
        results[name] = {
            "path": np.vstack(path),
            "losses": np.array(losses),
            "history": pd.DataFrame(opt.history),
        }
    return results


def plot_optimizer_multiview(results=None):
    """Optimizer trajectory: 3D surface, top view, front view, side view."""
    if results is None:
        results = simulate_optimizer_paths()

    W0, W1, Z = make_quad_grid()
    fig = plt.figure(figsize=(14, 11))

    ax3d = fig.add_subplot(2, 2, 1, projection="3d")
    ax3d.plot_surface(W0, W1, Z, cmap="Greys", alpha=0.55, linewidth=0)
    for name, res in results.items():
        _plot_path_on_3d(ax3d, res["path"], res["losses"], name)
    ax3d.set_title("V04 3D surface: optimizer paths")
    ax3d.set_xlabel("w0")
    ax3d.set_ylabel("w1")
    ax3d.set_zlabel("loss")
    ax3d.legend()

    ax_top = fig.add_subplot(2, 2, 2)
    ax_top.contour(W0, W1, Z, levels=28, cmap="Greys")
    for name, res in results.items():
        p = res["path"]
        ax_top.plot(p[:, 0], p[:, 1], "o-", markersize=2.5, label=name)
    ax_top.set_title("top view: contour trajectory")
    ax_top.set_xlabel("w0")
    ax_top.set_ylabel("w1")
    ax_top.set_aspect("equal")
    ax_top.grid(True, alpha=0.25)
    ax_top.legend()

    ax_front = fig.add_subplot(2, 2, 3)
    for name, res in results.items():
        ax_front.plot(res["path"][:, 0], res["losses"], "o-", markersize=2.5, label=name)
    ax_front.set_title("front view: w0-loss projection")
    ax_front.set_xlabel("w0")
    ax_front.set_ylabel("loss")
    ax_front.grid(True, alpha=0.3)
    ax_front.legend()

    ax_side = fig.add_subplot(2, 2, 4)
    for name, res in results.items():
        ax_side.plot(res["path"][:, 1], res["losses"], "o-", markersize=2.5, label=name)
    ax_side.set_title("side view: w1-loss projection")
    ax_side.set_xlabel("w1")
    ax_side.set_ylabel("loss")
    ax_side.grid(True, alpha=0.3)
    ax_side.legend()

    plt.tight_layout()
    return fig


def plot_optimizer_state_dashboard(results=None):
    """Optimizer state dashboard from simulation histories."""
    if results is None:
        results = simulate_optimizer_paths()

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for name, res in results.items():
        hist = res["history"]
        axes[0].plot(hist.index, hist["grad_norm"], label=name)
        axes[1].plot(hist.index, hist["step_norm"], label=name)
        state_cols = [c for c in ["velocity_norm", "first_state_norm", "second_state_norm"] if c in hist]
        if state_cols:
            axes[2].plot(hist.index, hist[state_cols].sum(axis=1), label=name)
    axes[0].set_title("gradient norm")
    axes[1].set_title("effective update norm")
    axes[2].set_title("optimizer state norm")
    for ax in axes:
        ax.set_xlabel("step")
        ax.grid(True, alpha=0.3)
        ax.legend()
    plt.tight_layout()
    return fig


# %% [markdown]
# ## V06. Image PCA and CNN bridge
#
# Fashion-MNIST cache가 없을 때는 sklearn digits를 사용한다.
# digits는 8x8 image, pixel range 0..16이므로 /16으로 scaling한다.

# %%
def load_digits_image_bundle(max_items=400):
    """Notebook-safe image fallback bundle."""
    digits = load_digits()
    images = digits.images[:max_items]
    labels = digits.target[:max_items]
    scaled = images.astype(float) / 16.0
    flat = scaled.reshape(len(scaled), -1)
    assert flat.ndim == 2
    assert flat.shape[0] == len(labels)
    assert np.nanmin(flat) >= 0.0
    assert np.nanmax(flat) <= 1.0 + 1e-8
    return {
        "name": "sklearn_digits_fallback",
        "images": images,
        "scaled_images": scaled,
        "flat_scaled": flat,
        "labels": labels,
        "class_names": [str(i) for i in range(10)],
    }


def plot_image_pca_and_patch_bridge(bundle=None):
    """Image tensor -> flatten -> PCA projection -> local patch/CNN bridge."""
    if bundle is None:
        bundle = load_digits_image_bundle()

    images = bundle["images"]
    flat = bundle["flat_scaled"]
    labels = bundle["labels"]
    class_names = bundle["class_names"]

    pca = PCA(n_components=3, random_state=SEED)
    coords = pca.fit_transform(flat)

    fig = plt.figure(figsize=(15, 10))
    ax_grid = fig.add_subplot(2, 3, 1)
    canvas = np.block(
        [
            [images[0], images[1], images[2]],
            [images[3], images[4], images[5]],
        ]
    )
    ax_grid.imshow(canvas, cmap="gray")
    ax_grid.set_title("sample grid")
    ax_grid.axis("off")

    ax_var = fig.add_subplot(2, 3, 2)
    ax_var.bar(["PC1", "PC2", "PC3"], pca.explained_variance_ratio_, color=["#4e79a7", "#f28e2b", "#59a14f"])
    ax_var.set_title("flattened image PCA variance")
    ax_var.set_ylim(0, 1)
    ax_var.grid(True, axis="y", alpha=0.3)

    ax_3d = fig.add_subplot(2, 3, 3, projection="3d")
    scatter = ax_3d.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=labels, cmap="tab10", s=18, alpha=0.8)
    ax_3d.set_title("image PCA 3D")
    ax_3d.set_xlabel("PC1")
    ax_3d.set_ylabel("PC2")
    ax_3d.set_zlabel("PC3")

    pairs = [("PC1", "PC2", 0, 1), ("PC1", "PC3", 0, 2), ("PC2", "PC3", 1, 2)]
    for ax_i, (name_x, name_y, i, j) in enumerate(pairs, start=4):
        ax = fig.add_subplot(2, 3, ax_i)
        ax.scatter(coords[:, i], coords[:, j], c=labels, cmap="tab10", s=18, alpha=0.8)
        view_name = "평면도" if (i, j) == (0, 1) else ("정면도" if (i, j) == (0, 2) else "측면도")
        ax.set_title(f"{name_x}-{name_y} {view_name}")
        ax.set_xlabel(name_x)
        ax.set_ylabel(name_y)
        ax.grid(True, alpha=0.3)
    handles, _ = scatter.legend_elements(num=10)
    fig.legend(handles, class_names[: len(handles)], loc="lower center", ncol=10, title="class")
    plt.tight_layout(rect=(0, 0.06, 1, 1))

    shape_table = pd.DataFrame(
        [
            ["image tensor", images.shape, "N images with 2D local grid"],
            ["flattened matrix", flat.shape, "Dense MLP input; local adjacency not explicit"],
            ["PCA coords", coords.shape, "projection for visualization only"],
        ],
        columns=["object", "shape", "meaning"],
    )
    return fig, shape_table


# %% [markdown]
# ## Quick local smoke check
#
# 아래 함수는 notebook에 붙이기 전에 핵심 helper가 import와 shape assert를 통과하는지 확인한다.

# %%
def smoke_check_visualization_helpers():
    """Return lightweight checks without displaying every plot."""
    path, losses = run_plain_gd_path(steps=5)
    assert path.shape == (6, 2)
    assert losses.shape == (6,)

    iris = load_iris()
    coords, pca = _fit_pca_views(iris.data.astype(float), iris.target.astype(int))
    assert coords.shape == (150, 3)
    assert len(pca.explained_variance_ratio_) == 3

    bundle = load_digits_image_bundle(max_items=20)
    assert bundle["flat_scaled"].shape[0] == 20

    iris_df = pd.DataFrame(iris.data.astype(float), columns=iris.feature_names)
    iris_df["species"] = pd.Categorical.from_codes(iris.target.astype(int), iris.target_names)
    iris_df["is_setosa"] = (iris_df["species"] == "setosa").astype(int)
    iris_df["petal_bucket"] = pd.qcut(iris_df["petal length (cm)"], q=3, labels=["short", "mid", "long"])
    _, association_tables = plot_mixed_association_dashboard(iris_df, target_col="species")
    assert not association_tables["pearson"].empty
    assert not association_tables["kendall"].empty
    assert not association_tables["cramers_v"].empty
    assert not association_tables["chi_square"].empty
    assert not association_tables["eta_squared"].empty
    _, binary_association_tables = plot_mixed_association_dashboard(iris_df, target_col="is_setosa")
    assert not binary_association_tables["point_biserial"].empty
    _, _, chi_summary = chi_square_pair_test(iris_df, "species", "petal_bucket")
    assert "Cramer's V" in set(chi_summary["test"])
    _, stacked_pct = plot_categorical_100pct_stacked(iris_df, "species", "petal_bucket")
    assert np.allclose(stacked_pct.sum(axis=1), 1.0)
    _, group_stats, group_tests = plot_continuous_by_category_gallery(iris_df, "petal width (cm)", "species")
    assert "eta squared" in set(group_tests["test"])
    assert not group_stats.empty
    _, cov_corr_table = plot_covariance_to_correlation_demo()
    assert not cov_corr_table.empty
    _, simple_reg_metrics = plot_simple_regression_residual_diagnostics(
        iris_df,
        x_col="petal length (cm)",
        y_col="petal width (cm)",
        group_col="species",
    )
    assert "R^2" in set(simple_reg_metrics["statistic"])
    _, pc_reg_metrics = plot_pc_regression_residual_diagnostics(
        iris_df,
        feature_cols=["sepal length (cm)", "sepal width (cm)", "petal length (cm)"],
        target_col="petal width (cm)",
        group_col="species",
        n_components=2,
    )
    assert "R^2" in set(pc_reg_metrics["item"])

    return {
        "gd_path_shape": path.shape,
        "iris_pca_shape": coords.shape,
        "digits_flat_shape": bundle["flat_scaled"].shape,
        "association_tables": sorted(k for k, v in association_tables.items() if hasattr(v, "empty") and not v.empty),
    }


if __name__ == "__main__":
    # Script mode에서는 무거운 figure display 없이 shape/syntax smoke만 수행한다.
    print(smoke_check_visualization_helpers())
