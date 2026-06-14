"""Question-level visual learning cards for DecisionMaking notebooks.

This generator creates reproducible PNG cards and injects them into the
answer notebooks as per-question visual study material.  The cards are not
decorative: each one has a concept-node route, a task-specific chart, and a
mistake guard.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parent
IPYNB_DIR = ROOT / "ipynb"
ASSET_DIR = ROOT / "visual_assets" / "item_cards"
MANIFEST_PATH = ASSET_DIR / "manifest.json"


@dataclass(frozen=True)
class CardSpec:
    key: str
    notebook: str
    cell_heading: str
    title_ko: str
    kind: str
    nodes: tuple[str, ...]
    read_order: str
    graph_focus: str
    mistake_guard: str


def _specs() -> list[CardSpec]:
    specs: list[CardSpec] = []

    def add_series(
        notebook: str,
        prefix: str,
        titles: list[str],
        kinds: list[str],
        node_groups: list[tuple[str, ...]],
    ) -> None:
        for idx, title in enumerate(titles, start=1):
            key = f"{prefix}_Q{idx:02d}"
            heading = f"문항 {idx}"
            if prefix == "DM_G2_P0004":
                heading = f"문항 {idx} 정답"
            specs.append(
                CardSpec(
                    key=key,
                    notebook=notebook,
                    cell_heading=heading,
                    title_ko=title,
                    kind=kinds[idx - 1],
                    nodes=node_groups[idx - 1],
                    read_order=_read_order(kinds[idx - 1]),
                    graph_focus=_graph_focus(kinds[idx - 1]),
                    mistake_guard=_mistake_guard(kinds[idx - 1]),
                )
            )

    add_series(
        "DM_G1_P0001_answer.ipynb",
        "DM_G1_P0001",
        [
            "표준형 변환 기본",
            "첫 pivot 선택",
            "피벗 연산 구조 설명",
            "타블로 판정 문제",
            "복수 최적해 예제 변형",
            "비유계 판정",
            "오답 진단: ratio test",
            "Solver 매핑 문제",
            "특수 종료 신호 비교",
            "최종 요약 문제",
        ],
        ["tableau", "ratio", "pivot", "reduced", "alternate", "unbounded", "ratio_error", "solver", "decision", "concept"],
        [
            ("simplex_tableau", "standard_form", "initial_bfs"),
            ("entering_variable", "minimum_ratio_test", "leaving_variable"),
            ("pivot_operation", "basis_exchange", "adjacent_bfs"),
            ("optimality_test", "reduced_cost", "multiple_optima"),
            ("multiple_optima", "optimal_face", "alternative_entering"),
            ("unbounded_solution", "missing_bound", "ratio_failure"),
            ("minimum_ratio_test", "positive_column_only", "wrong_abs_ratio"),
            ("solver_mapping", "changing_cells", "constraint_cells"),
            ("optimality", "multiple_optima", "unbounded", "phase_i_infeasible"),
            ("reality_language", "tableau_language", "solver_language"),
        ],
    )

    add_series(
        "DM_G1_P0002_answer.ipynb",
        "DM_G1_P0002",
        [
            "surplus/artificial variable 도입 판별",
            "2단계법 문제 변형",
            "Phase I 목적함수 해석",
            "artificial variable 최종해 판정",
            "식단문제 축소형",
            "Phase II 전환 구조",
            "오답 진단: surplus 부호",
            "Solver 매핑 문제",
            "Phase I tableau 해석",
            "최종 종합 문제",
        ],
        ["standard_convert", "phase_flow", "phase_gauge", "artificial_test", "diet_matrix", "phase_flow", "surplus_sign", "solver", "phase_flow", "concept"],
        [
            ("constraint_type", "slack", "surplus", "artificial"),
            ("standard_form", "phase_i", "phase_ii"),
            ("phase_i_objective", "feasibility_test", "not_original_z"),
            ("artificial_variable", "w_star", "original_feasibility"),
            ("diet_problem", "nutrient_matrix", "minimum_requirement"),
            ("phase_i_basis", "drop_artificial", "restore_objective"),
            ("surplus_variable", "excess_amount", "artificial_basis"),
            ("diet_solver", "changing_cells", "constraint_lhs_rhs"),
            ("phase_i_tableau", "w_zero", "phase_ii_start"),
            ("slack", "surplus", "artificial", "two_phase_method"),
        ],
    )

    add_series(
        "DM_G1_P0003_answer.ipynb",
        "DM_G1_P0003",
        [
            "min 문제를 Big-M용 max 형태로 바꾸기",
            "artificial variable 동치 조건",
            "Big-M과 2단계법 비교",
            "Big-M 오답 진단",
            "식단문제와 비타민 가격 쌍대 직관",
            "primal-dual 대응표 작성",
            "약쌍대성 판정",
            "강쌍대성과 최적성",
            "상보여유 기초 판정",
            "reduced cost와 shadow price 연결",
            "sensitivity report 브릿지 판별",
            "최종 종합 문제",
        ],
        ["bigm", "artificial_test", "phase_bigm_compare", "bigm_error", "dual_network", "dual_matrix", "duality_gap", "decision", "comp_slack", "rc_sp_route", "sensitivity_route", "concept"],
        [
            ("min_to_max", "big_m_penalty", "artificial_variable"),
            ("artificial_variable", "equivalence", "r_equals_zero"),
            ("two_phase_method", "big_m_method", "artificial_removal"),
            ("big_m_sign", "penalty", "wrong_reward"),
            ("diet_primal", "vitamin_dual_price", "dual_problem"),
            ("primal_constraints", "dual_variables", "matrix_transpose"),
            ("weak_duality", "primal_bound", "dual_bound"),
            ("strong_duality", "optimality_certificate", "four_cases"),
            ("complementary_slackness", "slack", "dual_variable"),
            ("reduced_cost", "shadow_price", "question_routing"),
            ("final_tableau", "sensitivity_report", "allowable_range"),
            ("artificial_variable", "big_m", "duality", "sensitivity"),
        ],
    )

    for idx, (title, kind, nodes) in enumerate(
        [
            ("스마트 물류센터 생산계획", "tableau", ("simplex_tableau", "ratio_test", "multiple_optima", "unbounded")),
            ("응급 물류 혼합계획", "phase_flow", ("surplus", "artificial", "phase_i", "phase_ii")),
            ("친환경 부품 조달계획", "dual_network", ("big_m", "primal_dual_mapping", "complementary_slackness")),
        ],
        start=1,
    ):
        specs.append(
            CardSpec(
                key=f"DM_G1_P0004_Q{idx:02d}",
                notebook="DM_G1_P0004_integrated_deep_answer.ipynb",
                cell_heading=f"심화문제 {idx} 정답",
                title_ko=title,
                kind=kind,
                nodes=nodes,
                read_order=_read_order(kind),
                graph_focus=_graph_focus(kind),
                mistake_guard=_mistake_guard(kind),
            )
        )

    add_series(
        "DM_G2_P0004_sensitivity_answer.ipynb",
        "DM_G2_P0004",
        [
            "기본 모형 해석",
            "binding/nonbinding 판정",
            "shadow price 적용",
            "reduced cost 해석",
            "목적함수 계수 허용범위",
            "오답 진단: shadow price 무제한 적용",
            "오답 진단: reduced cost와 shadow price 혼동",
            "final tableau/duality/sensitivity 연결",
            "최종 요약",
        ],
        ["sens_overview", "sens_slack", "sens_rhs", "sens_rc", "sens_obj_range", "sens_overuse", "rc_sp_route", "sensitivity_route", "sens_summary"],
        [
            ("sensitivity_report", "variable_cells", "constraint_cells"),
            ("binding_constraint", "slack", "shadow_price"),
            ("shadow_price", "rhs_change", "allowable_range"),
            ("reduced_cost", "nonbasic_variable", "objective_coefficient"),
            ("objective_coefficient", "allowable_increase", "allowable_decrease"),
            ("shadow_price", "allowable_range", "reoptimization"),
            ("reduced_cost", "shadow_price", "variable_vs_rhs_question"),
            ("final_tableau", "dual_price", "sensitivity_report"),
            ("reduced_cost", "shadow_price", "allowable_range"),
        ],
    )

    for idx, (title, kind, nodes) in enumerate(
        [
            ("지역 물류창고 수송계획", "transport_matrix", ("transportation_problem", "balanced_transportation", "dummy_node")),
            ("장비-작업 할당문제", "assignment_matrix", ("assignment_problem", "transportation_integrality", "row_col_equal_one")),
            ("냉장식품 경유수송", "transshipment", ("transshipment_problem", "node_balance", "sumif_balance")),
            ("도시 간 최소비용흐름", "mincost_flow", ("minimum_cost_flow", "capacity", "required_net_flow")),
            ("수송문제 민감도 해석", "transport_sensitivity", ("transportation_sensitivity", "reduced_cost", "shadow_price")),
        ],
        start=1,
    ):
        specs.append(
            CardSpec(
                key=f"DM_G3_P0005_Q{idx:02d}",
                notebook="DM_G3_P0005_transportation_network_answer.ipynb",
                cell_heading=f"문제 {idx} 정답",
                title_ko=title,
                kind=kind,
                nodes=nodes,
                read_order=_read_order(kind),
                graph_focus=_graph_focus(kind),
                mistake_guard=_mistake_guard(kind),
            )
        )

    return specs


def _read_order(kind: str) -> str:
    if kind.startswith("sens"):
        return "먼저 Variable Cells/Constraints를 분리하고, 평균/범위/증감 가능구간을 본 뒤 적용 가능 여부를 판정한다."
    if kind in {"transport_matrix", "assignment_matrix"}:
        return "행은 공급/장비, 열은 수요/작업으로 읽고, 행합과 열합이 어떤 제약을 만드는지 확인한다."
    if kind in {"transshipment", "mincost_flow"}:
        return "arc를 먼저 보고, 각 node에서 총유출과 총유입의 차이가 RHS와 맞는지 확인한다."
    if "dual" in kind or kind in {"bigm", "bigm_error", "comp_slack", "rc_sp_route", "sensitivity_route"}:
        return "왼쪽 primal/artificial 노드에서 오른쪽 dual/sensitivity 노드로 이동하며 대응 관계를 읽는다."
    if kind in {"tableau", "pivot", "ratio", "ratio_error", "alternate", "unbounded"}:
        return "2차원 실행가능영역 또는 ratio 막대를 먼저 보고, 그 다음 basis 교체/종료 신호를 판정한다."
    return "노드-간선 흐름을 왼쪽에서 오른쪽으로 따라가며 현재 문항의 판정 질문을 확인한다."


def _graph_focus(kind: str) -> str:
    if kind.startswith("sens"):
        return "민감도 보고서를 기술통계처럼 읽는다: 값, slack, reduced cost, shadow price, allowable range를 분리한다."
    if kind in {"transport_matrix", "assignment_matrix"}:
        return "matrix 구조에서 행합/열합이 Solver constraint cells가 되는 과정을 본다."
    if kind in {"transshipment", "mincost_flow"}:
        return "node balance = outbound - inbound = required net-flow 구조를 본다."
    if "dual" in kind:
        return "primal constraint와 dual variable, primal variable과 dual constraint의 대응을 본다."
    if "phase" in kind or "artificial" in kind or "bigm" in kind:
        return "artificial variable이 최종 0이 되어야 원문제와 다시 같아지는 흐름을 본다."
    return "최적해 이론의 핵심 판정 신호가 그래프에서 어디에 나타나는지 본다."


def _mistake_guard(kind: str) -> str:
    if kind.startswith("sens"):
        return "허용범위 밖 변화에 기존 shadow price/reduced cost를 그대로 적용하지 않는다."
    if kind in {"transport_matrix", "assignment_matrix"}:
        return "행합과 열합을 뒤집거나, assignment에서 행/열 제약 중 하나를 누락하지 않는다."
    if kind in {"transshipment", "mincost_flow"}:
        return "경유지 제약을 생략하거나 SUMIF 시작노드/종료노드 부호를 반대로 쓰지 않는다."
    if kind in {"ratio", "ratio_error"}:
        return "ratio test에 0 또는 음수 entering-column 계수 행을 넣지 않는다."
    if kind in {"phase_flow", "phase_gauge", "artificial_test", "standard_convert", "surplus_sign"}:
        return "Phase I의 w=0을 원 목적값 z=0으로 착각하지 않고, surplus 부호를 +로 쓰지 않는다."
    if kind in {"bigm", "bigm_error"}:
        return "Big-M 부호는 artificial을 보상하지 않고 벌주는 방향이어야 한다."
    if kind in {"dual_network", "dual_matrix", "duality_gap", "comp_slack"}:
        return "dual 변수 수와 primal 변수 수를 섞지 않고, slack>0이면 대응 dual 변수는 0임을 확인한다."
    return "계산 결과만 보지 말고 어떤 노드에서 어떤 노드로 이동하는지 설명한다."


def _wrap(text: str, width: int = 18) -> str:
    words = text.split()
    lines: list[str] = []
    line: list[str] = []
    for word in words:
        if sum(len(x) for x in line) + len(line) + len(word) > width and line:
            lines.append(" ".join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(" ".join(line))
    return "\n".join(lines)


def _arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], color: str = "#475569") -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13, linewidth=1.4, color=color))


def _box(ax: plt.Axes, x: float, y: float, text: str, fc: str = "#e0f2fe") -> None:
    ax.add_patch(Rectangle((x - 0.12, y - 0.045), 0.24, 0.09, facecolor=fc, edgecolor="#334155", linewidth=1.0))
    ax.text(x, y, _wrap(text, 16), ha="center", va="center", fontsize=7.4, color="#0f172a")


def _base_figure(spec: CardSpec) -> tuple[plt.Figure, plt.Axes, plt.Axes]:
    fig = plt.figure(figsize=(13.6, 7.4))
    fig.patch.set_facecolor("#fbfbf7")
    fig.suptitle(f"{spec.key}  |  {spec.kind}", fontsize=15, weight="bold", y=0.975)
    ax_graph = fig.add_axes([0.04, 0.14, 0.36, 0.73])
    ax_chart = fig.add_axes([0.45, 0.16, 0.51, 0.68])
    ax_graph.set_title("Concept node-edge route", fontsize=11, weight="bold")
    ax_chart.set_title("Problem visual cue", fontsize=11, weight="bold")
    return fig, ax_graph, ax_chart


def _draw_concept_route(ax: plt.Axes, spec: CardSpec) -> None:
    ax.axis("off")
    y_values = np.linspace(0.78, 0.22, len(spec.nodes))
    colors = ["#dbeafe", "#dcfce7", "#fef3c7", "#fee2e2", "#ede9fe"]
    prev: tuple[float, float] | None = None
    for i, (node, y) in enumerate(zip(spec.nodes, y_values)):
        x = 0.5
        _box(ax, x, y, node, colors[i % len(colors)])
        if prev is not None:
            _arrow(ax, (prev[0], prev[1] - 0.055), (x, y + 0.055), "#2563eb")
        prev = (x, y)
    ax.text(
        0.02,
        0.04,
        "Use this route before solving:\nnode -> example -> formula -> Solver/source",
        fontsize=8.2,
        color="#475569",
        ha="left",
        va="bottom",
    )


def _draw_tableau(ax: plt.Axes, spec: CardSpec) -> None:
    x = np.linspace(0, 90, 300)
    constraints = [
        np.minimum((120 - 2 * x), 1e9),
        (100 - x) / 2,
        np.full_like(x, 45),
    ]
    ax.set_xlim(0, 75)
    ax.set_ylim(0, 80)
    y1 = np.clip(constraints[0], 0, 80)
    y2 = np.clip(constraints[1], 0, 80)
    ax.plot(x, y1, label="2x1+x2<=120")
    ax.plot(x, y2, label="x1+2x2<=100")
    ax.axvline(45, color="#f97316", label="x1<=45")
    poly = np.array([[0, 0], [45, 0], [45, 27.5], [46.7, 26.7], [0, 50]])
    ax.fill(poly[:, 0], poly[:, 1], color="#bbf7d0", alpha=0.65)
    ax.plot([0, 45, 45], [0, 0, 27.5], "-o", color="#dc2626", linewidth=2.2, label="BFS path")
    ax.annotate("initial BFS", (0, 0), xytext=(8, 10), arrowprops={"arrowstyle": "->"}, fontsize=8)
    ax.annotate("pivot move", (45, 0), xytext=(48, 12), arrowprops={"arrowstyle": "->"}, fontsize=8)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)


def _draw_ratio(ax: plt.Axes, spec: CardSpec, error: bool = False) -> None:
    labels = ["row1", "row2", "row3", "neg row"]
    vals = [60, 100, 45, 30]
    colors = ["#93c5fd", "#93c5fd", "#ef4444", "#9ca3af"]
    x = np.arange(len(labels))
    ax.bar(x, vals, color=colors, edgecolor="#334155")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("RHS / entering coefficient")
    ax.grid(axis="y", alpha=0.25)
    ax.text(2, vals[2] + 4, "leave", ha="center", fontsize=9, color="#7f1d1d", weight="bold")
    if error:
        ax.text(3, vals[3] + 4, "exclude\nnot abs()", ha="center", fontsize=9, color="#111827", weight="bold")
    ax.set_title("Positive-ratio candidates only", fontsize=11)


def _draw_flow_chart(ax: plt.Axes, labels: Iterable[str]) -> None:
    ax.axis("off")
    labels = list(labels)
    xs = np.linspace(0.08, 0.92, len(labels))
    for i, (x, label) in enumerate(zip(xs, labels)):
        _box(ax, x, 0.5, label, ["#dbeafe", "#dcfce7", "#fef3c7", "#fee2e2"][i % 4])
        if i > 0:
            _arrow(ax, (xs[i - 1] + 0.13, 0.5), (x - 0.13, 0.5), "#2563eb")


def _draw_sensitivity(ax: plt.Axes, spec: CardSpec) -> None:
    ax.axis("off")
    var_names = ["x1", "x2", "x3"]
    final = np.array([26.6667, 46.6667, 0.0])
    rc = np.array([0.0, 0.0, -8.0])
    obj = np.array([40, 30, 22])
    ai = np.array([20, 50, 8])
    ad = np.array([25, 8, 0])
    con_names = ["R1", "R2", "R3", "R4", "R5"]
    slack = np.array([0, 0, 28.3333, 23.3333, 35])
    sp = np.array([16.6667, 6.6667, 0, 0, 0])

    if spec.kind in {"sens_overview", "sens_summary"}:
        child = ax.inset_axes([0.03, 0.54, 0.44, 0.38])
        vx = np.arange(len(var_names))
        child.bar(vx, final, color="#93c5fd", edgecolor="#334155")
        child.set_xticks(vx)
        child.set_xticklabels(var_names)
        child.set_title("Variable final values", fontsize=9)
        child.grid(axis="y", alpha=0.2)
        child2 = ax.inset_axes([0.54, 0.54, 0.42, 0.38])
        cx = np.arange(len(con_names))
        child2.bar(cx, sp, color="#fbbf24", edgecolor="#334155")
        child2.set_xticks(cx)
        child2.set_xticklabels(con_names)
        child2.set_title("Shadow prices", fontsize=9)
        child2.grid(axis="y", alpha=0.2)
        table_ax = ax.inset_axes([0.04, 0.04, 0.9, 0.34])
        table_ax.axis("off")
        rows = [
            ["mean obj coeff", f"{obj.mean():.1f}"],
            ["mean reduced cost", f"{rc.mean():.1f}"],
            ["max shadow price", f"{sp.max():.1f}"],
            ["mean slack", f"{slack.mean():.1f}"],
        ]
        table = table_ax.table(cellText=rows, colLabels=["descriptive statistic", "value"], loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(8.4)
        table.scale(1, 1.25)
    elif spec.kind == "sens_slack":
        xs = np.arange(len(con_names))
        ax2 = ax.inset_axes([0.06, 0.1, 0.88, 0.78])
        ax2.bar(xs - 0.18, slack, width=0.36, label="slack", color="#bfdbfe")
        ax2.bar(xs + 0.18, sp, width=0.36, label="shadow price", color="#f97316")
        ax2.set_xticks(xs)
        ax2.set_xticklabels(con_names)
        ax2.legend(fontsize=8)
        ax2.set_title("Binding check: slack vs shadow price", fontsize=10)
        ax2.grid(axis="y", alpha=0.2)
    elif spec.kind == "sens_rhs":
        ax2 = ax.inset_axes([0.08, 0.16, 0.86, 0.68])
        labels = ["R1 +20", "R2 -50", "R1 +50"]
        changes = [20, -50, 50]
        colors = ["#22c55e", "#22c55e", "#ef4444"]
        lx = np.arange(len(labels))
        ax2.bar(lx, changes, color=colors, edgecolor="#334155")
        ax2.set_xticks(lx)
        ax2.set_xticklabels(labels)
        ax2.axhline(42.5, color="#ef4444", linestyle="--", label="R1 max inc")
        ax2.axhline(-70, color="#2563eb", linestyle="--", label="R2 max dec")
        ax2.set_title("RHS change must stay inside allowable range", fontsize=10)
        ax2.legend(fontsize=8)
        ax2.grid(axis="y", alpha=0.2)
    elif spec.kind == "sens_rc":
        ax2 = ax.inset_axes([0.08, 0.14, 0.86, 0.72])
        vx = np.arange(len(var_names))
        ax2.bar(vx, rc, color=["#94a3b8", "#94a3b8", "#ef4444"], edgecolor="#334155")
        ax2.set_xticks(vx)
        ax2.set_xticklabels(var_names)
        ax2.axhline(0, color="#111827")
        ax2.set_title("Reduced cost answers variable-entry questions", fontsize=10)
        ax2.set_ylabel("reduced cost")
        ax2.grid(axis="y", alpha=0.2)
    elif spec.kind == "sens_obj_range":
        ax2 = ax.inset_axes([0.08, 0.18, 0.84, 0.62])
        for i, name in enumerate(var_names):
            low = obj[i] - ad[i]
            high = obj[i] + ai[i]
            ax2.plot([low, high], [i, i], lw=7, color="#93c5fd")
            ax2.scatter([obj[i]], [i], color="#111827", zorder=3)
        ax2.set_yticks(range(len(var_names)))
        ax2.set_yticklabels(var_names)
        ax2.set_title("Objective coefficient allowable interval", fontsize=10)
        ax2.set_xlabel("coefficient value")
        ax2.grid(axis="x", alpha=0.2)
    elif spec.kind == "sens_overuse":
        ax2 = ax.inset_axes([0.08, 0.16, 0.86, 0.68])
        xs = ["inside +20", "outside +100"]
        xx = np.arange(len(xs))
        ax2.bar(xx, [20, 100], color=["#22c55e", "#ef4444"], edgecolor="#334155")
        ax2.set_xticks(xx)
        ax2.set_xticklabels(xs)
        ax2.axhline(42.5, color="#111827", linestyle="--", label="allowable inc")
        ax2.set_title("Do not extrapolate shadow price outside range", fontsize=10)
        ax2.legend(fontsize=8)
        ax2.grid(axis="y", alpha=0.2)
    else:
        _draw_flow_chart(ax, ["Variable question", "Reduced cost", "RHS question", "Shadow price", "Check range"])


def _draw_transport_matrix(ax: plt.Axes, spec: CardSpec) -> None:
    costs = np.array([[6, 8, 10, 9], [9, 7, 4, 5], [8, 6, 7, 6]])
    im = ax.imshow(costs, cmap="YlGnBu")
    ax.set_xticks(range(4))
    ax.set_xticklabels(["D1", "D2", "D3", "D4"])
    ax.set_yticks(range(3))
    ax.set_yticklabels(["A", "B", "C"])
    for i in range(3):
        for j in range(4):
            ax.text(j, i, str(costs[i, j]), ha="center", va="center", fontsize=9, weight="bold")
    ax.set_title("Transportation matrix: row sums=supply, column sums=demand", fontsize=10)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)


def _draw_assignment_matrix(ax: plt.Axes, spec: CardSpec) -> None:
    costs = np.array([[11, 8, 7, 10], [9, 12, 6, 7], [8, 7, 10, 6], [6, 9, 8, 11]])
    im = ax.imshow(costs, cmap="Purples")
    ax.set_xticks(range(4))
    ax.set_xticklabels(["J1", "J2", "J3", "J4"])
    ax.set_yticks(range(4))
    ax.set_yticklabels(["M1", "M2", "M3", "M4"])
    for i in range(4):
        for j in range(4):
            ax.text(j, i, str(costs[i, j]), ha="center", va="center", fontsize=9, weight="bold")
    ax.set_title("Assignment = transportation with all supplies/demands = 1", fontsize=10)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)


def _draw_network(ax: plt.Axes, spec: CardSpec, mincost: bool = False) -> None:
    ax.axis("off")
    if mincost:
        pos = {1: (0.1, 0.75), 2: (0.1, 0.25), 3: (0.45, 0.5), 4: (0.78, 0.72), 5: (0.78, 0.25)}
        edges = [(1, 3, "c5 cap30"), (1, 4, "c8 cap20"), (2, 3, "c4 cap25"), (2, 5, "c7 cap30"), (3, 4, "c3 cap25"), (3, 5, "c6 cap30"), (4, 5, "c2 cap20")]
        rhs = {1: "+35", 2: "+25", 3: "0", 4: "-20", 5: "-40"}
        title = "Minimum-cost flow: outbound - inbound = required net-flow"
    else:
        pos = {1: (0.1, 0.75), 2: (0.1, 0.25), 3: (0.45, 0.72), 4: (0.45, 0.28), 5: (0.82, 0.8), 6: (0.82, 0.5), 7: (0.82, 0.2)}
        edges = [(1, 3, "4"), (1, 4, "6"), (2, 3, "5"), (2, 4, "3"), (3, 5, "7"), (3, 6, "4"), (3, 7, "8"), (4, 5, "6"), (4, 6, "5"), (4, 7, "4")]
        rhs = {1: "+150", 2: "+170", 3: "0", 4: "0", 5: "-90", 6: "-110", 7: "-120"}
        title = "Transshipment: warehouses require inbound = outbound"
    ax.set_title(title, fontsize=10)
    for u, v, label in edges:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        _arrow(ax, (x1 + 0.035, y1), (x2 - 0.035, y2), "#64748b")
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.025, label, fontsize=7, color="#334155")
    for node, (x, y) in pos.items():
        ax.add_patch(plt.Circle((x, y), 0.045, facecolor="#dbeafe", edgecolor="#1e3a8a", linewidth=1.2))
        ax.text(x, y, str(node), ha="center", va="center", fontsize=9, weight="bold")
        ax.text(x, y - 0.075, rhs[node], ha="center", va="center", fontsize=7, color="#334155")


def _draw_transport_sensitivity(ax: plt.Axes, spec: CardSpec) -> None:
    labels = ["A-D3 RC", "C-D1 RC", "B supply SP", "D4 demand SP"]
    values = [4, 3, -2, 5]
    colors = ["#ef4444", "#ef4444", "#f59e0b", "#f59e0b"]
    x = np.arange(len(labels))
    ax.bar(x, values, color=colors, edgecolor="#334155")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.axhline(0, color="#111827")
    ax.set_title("Transportation sensitivity: route question vs node/RHS question", fontsize=10)
    ax.set_ylabel("report value")
    ax.tick_params(axis="x", rotation=10)
    ax.grid(axis="y", alpha=0.2)


def _draw_kind(ax: plt.Axes, spec: CardSpec) -> None:
    kind = spec.kind
    if kind in {"tableau", "pivot"}:
        _draw_tableau(ax, spec)
    elif kind == "ratio":
        _draw_ratio(ax, spec)
    elif kind == "ratio_error":
        _draw_ratio(ax, spec, error=True)
    elif kind == "alternate":
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.fill([0, 8, 8, 2, 0], [0, 0, 2, 8, 8], color="#bbf7d0", alpha=0.65)
        ax.plot([2, 8], [8, 2], color="#dc2626", lw=5)
        ax.scatter([4, 6, 5], [6, 4, 3], color=["#dc2626", "#dc2626", "#2563eb"])
        ax.set_title("Multiple optima only on the optimal face", fontsize=10)
        ax.grid(alpha=0.2)
    elif kind == "unbounded":
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.fill([0, 10, 10, 3, 0], [0, 0, 7, 4, 2], color="#fed7aa", alpha=0.7)
        ax.arrow(3, 2, 6, 3, width=0.05, head_width=0.3, color="#dc2626")
        ax.text(5.2, 5.5, "improving ray\nno leaving row", fontsize=9, color="#7f1d1d")
        ax.grid(alpha=0.2)
    elif kind.startswith("sens") or kind in {"rc_sp_route", "sensitivity_route"}:
        _draw_sensitivity(ax, spec)
    elif kind == "transport_matrix":
        _draw_transport_matrix(ax, spec)
    elif kind == "assignment_matrix":
        _draw_assignment_matrix(ax, spec)
    elif kind == "transshipment":
        _draw_network(ax, spec, mincost=False)
    elif kind == "mincost_flow":
        _draw_network(ax, spec, mincost=True)
    elif kind == "transport_sensitivity":
        _draw_transport_sensitivity(ax, spec)
    elif kind == "diet_matrix":
        mat = np.array([[10, 20, 10], [0, 10, 30]])
        im = ax.imshow(mat, cmap="Greens")
        ax.set_xticks(range(3))
        ax.set_xticklabels(["Food1", "Food2", "Food3"])
        ax.set_yticks(range(2))
        ax.set_yticklabels(["VitA", "VitC"])
        for i in range(2):
            for j in range(3):
                ax.text(j, i, str(mat[i, j]), ha="center", va="center", weight="bold")
        ax.set_title("Diet matrix: nutrients by food", fontsize=10)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    elif kind == "dual_matrix":
        mat = np.array([[8, 4], [4, 4], [4, 0], [0, 1]])
        im = ax.imshow(mat, cmap="Blues")
        ax.set_xticks(range(2))
        ax.set_xticklabels(["x1", "x2"])
        ax.set_yticks(range(4))
        ax.set_yticklabels(["c1", "c2", "c3", "c4"])
        for i in range(4):
            for j in range(2):
                ax.text(j, i, str(mat[i, j]), ha="center", va="center", weight="bold")
        ax.set_title("Primal-dual mapping = transpose view", fontsize=10)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    elif kind == "duality_gap":
        labels = ["Primal Z", "Dual W"]
        x = np.arange(len(labels))
        ax.bar(x, [700, 1540], color=["#93c5fd", "#fbbf24"], edgecolor="#334155")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.plot([0, 1], [700, 1540], "--", color="#334155")
        ax.text(0.5, 1120, "gap", ha="center", fontsize=9)
        ax.set_title("Weak duality: primal <= dual", fontsize=10)
        ax.grid(axis="y", alpha=0.2)
    elif kind == "comp_slack":
        labels = ["slack", "dual y", "product"]
        x = np.arange(len(labels))
        ax.bar(x, [40, 3, 120], color=["#bfdbfe", "#fbbf24", "#ef4444"], edgecolor="#334155")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_title("Complementary slackness requires slack*y = 0", fontsize=10)
        ax.grid(axis="y", alpha=0.2)
    elif kind == "bigm_error":
        r = np.arange(4)
        ax.plot(r, r, marker="o", label="wrong reward +M*r")
        ax.plot(r, -r, marker="o", label="correct penalty -M*r")
        ax.axhline(0, color="#111827", lw=0.8)
        ax.set_title("Big-M sign check", fontsize=10)
        ax.set_xlabel("artificial r")
        ax.set_ylabel("objective effect / M")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.2)
    else:
        flow_map = {
            "standard_convert": ["<=", "+ slack", ">=", "- surplus + artificial", "=", "+ artificial"],
            "phase_flow": ["standard form", "Phase I", "w*=0?", "drop artificial", "Phase II"],
            "phase_gauge": ["Phase I w", "feasibility signal", "not original z", "Phase II"],
            "artificial_test": ["artificial introduced", "must become 0", "r>0 => infeasible"],
            "surplus_sign": ["LHS >= RHS", "LHS = RHS + surplus", "LHS - surplus = RHS"],
            "solver": ["decision variables", "changing cells", "target cell", "constraint LHS/RHS"],
            "bigm": ["Min Z", "Max -Z", "add artificial", "penalize artificial"],
            "phase_bigm_compare": ["artificial", "Two-phase: separate w", "Big-M: penalty", "same goal r=0"],
            "dual_network": ["primal constraints", "dual variables", "dual objective", "shadow prices"],
            "decision": ["tableau signal", "improve?", "zero reduced cost?", "ratio candidate?", "case"],
            "concept": ["model", "basis/dual", "sensitivity", "Solver interpretation"],
        }
        _draw_flow_chart(ax, flow_map.get(kind, ["node", "edge", "formula", "Solver", "source"]))


def render_card(spec: CardSpec) -> Path:
    fig, ax_graph, ax_chart = _base_figure(spec)
    _draw_concept_route(ax_graph, spec)
    _draw_kind(ax_chart, spec)
    fig.text(0.04, 0.045, "Read order: follow node route, then inspect chart, then check formula/Solver mapping.", fontsize=8.5, color="#334155")
    fig.text(0.45, 0.045, "Mistake guard: check sign, domain, range, and node balance before calculating.", fontsize=8.5, color="#7f1d1d")
    filename = f"{spec.key}.png"
    path = ASSET_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_cards() -> dict[str, str]:
    manifest: dict[str, str] = {}
    for spec in _specs():
        path = render_card(spec)
        manifest[spec.key] = str(path.relative_to(ROOT)).replace("\\", "/")
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def _visual_block(spec: CardSpec, image_rel_to_ipynb: str) -> str:
    nodes = " -> ".join(f"`{node}`" for node in spec.nodes)
    return f"""

<!-- ITEM_VISUAL_CARD:{spec.key}:START -->
#### 문항별 시각 학습자료

![{spec.key}]({image_rel_to_ipynb})

- 노드-간선 경로: {nodes}
- 보는 순서: {spec.read_order}
- 그래프 해석: {spec.graph_focus}
- 오답 방지: {spec.mistake_guard}
<!-- ITEM_VISUAL_CARD:{spec.key}:END -->
"""


def _remove_existing_block(source: str, key: str) -> str:
    pattern = re.compile(
        rf"\n?<!-- ITEM_VISUAL_CARD:{re.escape(key)}:START -->.*?<!-- ITEM_VISUAL_CARD:{re.escape(key)}:END -->",
        flags=re.DOTALL,
    )
    return pattern.sub("", source).rstrip()


def inject_cards_into_answer_notebooks(manifest: dict[str, str]) -> None:
    specs_by_notebook: dict[str, list[CardSpec]] = {}
    for spec in _specs():
        specs_by_notebook.setdefault(spec.notebook, []).append(spec)

    for notebook_name, specs in specs_by_notebook.items():
        nb_path = IPYNB_DIR / notebook_name
        nb = nbformat.read(nb_path, as_version=4)
        for spec in specs:
            image_rel = "../" + manifest[spec.key]
            inserted = False
            for cell in nb.cells:
                if cell.cell_type != "markdown":
                    continue
                if re.search(rf"^###\s+{re.escape(spec.cell_heading)}", cell.source, flags=re.MULTILINE):
                    cell.source = _remove_existing_block(cell.source, spec.key) + _visual_block(spec, image_rel)
                    inserted = True
                    break
            if not inserted:
                raise RuntimeError(f"Could not find heading {spec.cell_heading!r} in {notebook_name}")
        nbformat.write(nb, nb_path)


def generate_item_card_pack(update_notebooks: bool = True) -> dict[str, str]:
    manifest = generate_cards()
    if update_notebooks:
        inject_cards_into_answer_notebooks(manifest)
    return manifest


if __name__ == "__main__":
    result = generate_item_card_pack(update_notebooks=True)
    print(json.dumps({"item_card_count": len(result), "manifest": str(MANIFEST_PATH)}, ensure_ascii=False, indent=2))
