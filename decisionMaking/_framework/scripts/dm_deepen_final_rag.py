#!/usr/bin/env python3
"""Deepen final DecisionMaking RAG tutor docs.

This script upgrades the initially generated PDF RAG briefs into evidence-based
tutor operating documents. It keeps the PDF transcript as the primary source and
uses web grounding only as a secondary implementation/reference layer.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "decisionMaking"
TRANSCRIPT_DIR = COURSE / "pdf_transcripts"
INVENTORY_DIR = COURSE / "_inventory"
FLAT_PACK_DIR = COURSE / "rag_applied_flat_pack"


SECTIONS = [
    "0. Document Contract",
    "1. Source Coverage Map",
    "2. Chapter Thesis",
    "3. Current Graph Position",
    "4. Learning Outcomes",
    "5. Concept Graph Map",
    "6. Core Concept Node Cards",
    "7. Example Walkthrough Cards",
    "8. Modeling Pattern Library",
    "9. Spreadsheet / Solver Mapping",
    "10. Cross-Chapter Connections",
    "11. Misconception & Error Diagnosis Bank",
    "12. Retrieval Routing Table",
    "13. Tutor Session Protocol",
    "14. Practice / Check Questions",
    "15. Source Trace Table",
    "16. QC / Extraction Risk Notes",
]


WEB_SOURCES = {
    "WEB_OR_TOOLS_LP": {
        "title": "Google OR-Tools: Solving an LP Problem",
        "url": "https://developers.google.com/optimization/lp/lp_example",
        "use": "LP/Simplex-style solver model grounding: variables, constraints, objective, optimal solution.",
    },
    "WEB_OR_TOOLS_MIP": {
        "title": "Google OR-Tools: Solving a MIP Problem",
        "url": "https://developers.google.com/optimization/mip/mip_example",
        "use": "Integer and mixed-integer model grounding: integer variables, constraints, objective, MIP solver.",
    },
    "WEB_OR_TOOLS_ASSIGNMENT": {
        "title": "Google OR-Tools: Solving an Assignment Problem",
        "url": "https://developers.google.com/optimization/assignment/assignment_example",
        "use": "Assignment constraints: each worker at most one task and each task exactly one worker.",
    },
    "WEB_OR_TOOLS_MIN_COST_FLOW": {
        "title": "Google OR-Tools: Minimum Cost Flows",
        "url": "https://developers.google.com/optimization/flow/mincostflow",
        "use": "Min-cost flow grounding: start nodes, end nodes, capacities, unit costs, supplies/demands.",
    },
    "WEB_OR_TOOLS_MAX_FLOW": {
        "title": "Google OR-Tools: Maximum Flows",
        "url": "https://developers.google.com/optimization/flow/maxflow",
        "use": "Maximum-flow grounding: nodes/arcs, capacities, source, sink, flow conservation.",
    },
    "WEB_MS_SUMPRODUCT": {
        "title": "Microsoft Support: SUMPRODUCT function",
        "url": "https://support.microsoft.com/en-US/Excel/sumproduct-function",
        "use": "Spreadsheet objective grounding: multiply corresponding arrays and sum the products.",
    },
    "WEB_MS_SUMIF": {
        "title": "Microsoft Support: SUMIF function",
        "url": "https://support.microsoft.com/en-US/Excel/sumif-function",
        "use": "Spreadsheet node-balance grounding: sum rows that satisfy a node criterion.",
    },
    "WEB_MS_SOLVERADD": {
        "title": "Microsoft Learn: SolverAdd Function",
        "url": "https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solveradd-function",
        "use": "Excel Solver constraint grounding: adding relational constraints to a solver model.",
    },
    "WEB_MS_SOLVERSOLVE": {
        "title": "Microsoft Learn: SolverSolve Function",
        "url": "https://learn.microsoft.com/en-us/office/vba/excel/concepts/functions/solversolve-function",
        "use": "Excel Solver execution grounding: solving the configured model.",
    },
}


@dataclass(frozen=True)
class Node:
    slug: str
    label: str
    english: str
    definition: str
    intuition: str
    when: str
    variables: str
    objective: str
    constraints: str
    real_meaning: str
    graph_view: str
    solver_view: str
    example: str
    numeric: str
    mistakes: str
    prereq: str
    followup: str
    similar: str
    exam: str
    tags: list[str]
    patterns: list[str]


@dataclass(frozen=True)
class Example:
    slug: str
    title: str
    problem: str
    variables: str
    objective: str
    constraints: str
    solver: str
    interpretation: str
    coach: list[str]
    patterns: list[str]


@dataclass(frozen=True)
class Route:
    question: str
    first_node: str
    next_node: str
    example: str
    evidence_hint: str


@dataclass(frozen=True)
class Profile:
    source_id: str
    slug: str
    title: str
    normalized_pdf: str
    thesis: str
    graph_position: str
    learning_outcomes: list[str]
    nodes: list[Node]
    examples: list[Example]
    patterns: list[tuple[str, str, str, str]]
    solver_rows: list[tuple[str, str, str]]
    cross_connections: list[tuple[str, str, str]]
    misconceptions: list[tuple[str, str, str, str]]
    routes: list[Route]
    practice: list[str]
    web_refs: list[str]
    qc_notes: list[str] = field(default_factory=list)


def n(
    slug: str,
    label: str,
    english: str,
    definition: str,
    intuition: str,
    when: str,
    variables: str,
    objective: str,
    constraints: str,
    real_meaning: str,
    graph_view: str,
    solver_view: str,
    example: str,
    numeric: str,
    mistakes: str,
    prereq: str,
    followup: str,
    similar: str,
    exam: str,
    tags: Iterable[str],
    patterns: Iterable[str],
) -> Node:
    return Node(
        slug,
        label,
        english,
        definition,
        intuition,
        when,
        variables,
        objective,
        constraints,
        real_meaning,
        graph_view,
        solver_view,
        example,
        numeric,
        mistakes,
        prereq,
        followup,
        similar,
        exam,
        list(tags),
        list(patterns),
    )


def ex(
    slug: str,
    title: str,
    problem: str,
    variables: str,
    objective: str,
    constraints: str,
    solver: str,
    interpretation: str,
    coach: Iterable[str],
    patterns: Iterable[str],
) -> Example:
    return Example(
        slug,
        title,
        problem,
        variables,
        objective,
        constraints,
        solver,
        interpretation,
        list(coach),
        list(patterns),
    )


PROFILES: list[Profile] = [
    Profile(
        source_id="DM_PDF01",
        slug="ch04_simplex_tableau_twophase_supplement",
        title="Ch.4 심플렉스 타블로 보완과 2단계법",
        normalized_pdf="DM_PDF01_ch04_simplex_tableau_twophase_supplement.pdf",
        thesis="그래프 해법의 꼭짓점 이동 원리를 타블로 계산으로 구현하고, 초기 BFS가 없을 때 2단계법으로 출발 가능한 기저를 만든다.",
        graph_position="LP 일반형 -> 표준형/정규형 -> BFS -> tableau -> pivot -> 특수 경우 -> two-phase method.",
        learning_outcomes=[
            "타블로에서 entering variable, leaving variable, minimum ratio test를 분리해서 설명한다.",
            "복수 최적해, 비유계, infeasible을 타블로 신호로 판별한다.",
            "인위변수와 Phase I/Phase II가 왜 필요한지 식단형 최소화 문제와 연결한다.",
        ],
        nodes=[
            n("simplex_tableau", "심플렉스 타블로", "simplex tableau", "목적행, 제약행, 기저변수, RHS, 비율검사를 한 표에 모은 심플렉스 계산 장치다.", "그래프에서 꼭짓점을 옮기는 일을 표의 행 연산과 기저 교체로 수행한다.", "2변수 그래프 해법을 일반 차원 LP로 확장할 때 쓴다.", "x1, x2 같은 원변수와 slack/surplus/artificial 변수를 함께 둔다.", "max z 또는 min w의 목적행을 기준으로 개선 가능 열을 찾는다.", "제약행은 현재 BFS의 자원 사용과 남은 여유를 RHS로 보여준다.", "현재 생산계획에서 어떤 활동을 기저에 넣으면 목적값이 개선되는지 묻는 계산표다.", "가능영역 꼭짓점은 tableau의 BFS와 대응한다.", "Solver의 Simplex LP가 내부적으로 하는 basis 이동을 사람이 읽을 수 있는 표로 드러낸다.", "예1의 max z=3x1+2x2 타블로 전개.", "최종 타블로의 x1, x2, slack 값과 z 값을 현실 생산량과 여유자원으로 해석한다.", "모든 행에 비율검사를 적용하는 오류. entering 열 계수가 양수인 행만 후보가 된다.", "표준형, 정규형, slack variable", "minimum ratio test, pivot, optimality test", "그래프 해법의 꼭짓점 최적성", "타블로 한 행을 주고 다음 피벗을 묻는다.", ["simplex", "tableau", "BFS", "pivot"], ["심플렉스 타블로를 이용", "기저"]),
            n("entering_leaving_variable", "진입/탈락변수", "entering/leaving variable", "목적값을 개선할 변수와 feasibility를 지키기 위해 기저에서 빠질 변수를 짝으로 고르는 규칙이다.", "새 활동을 늘리면 어떤 기존 여유/활동이 먼저 한계에 닿는지 찾는다.", "각 반복에서 다음 BFS를 결정할 때 쓴다.", "entering variable은 비기저변수, leaving variable은 현재 기저변수다.", "max에서는 보통 목적행의 음의 계수 중 개선 폭이 큰 열을 고른다.", "minimum ratio test가 음수가 되지 않는 RHS 한계를 만든다.", "생산활동을 늘리다가 가장 먼저 소진되는 자원을 leaving으로 본다.", "인접 꼭짓점 이동의 방향과 도착 꼭짓점이다.", "Solver에서는 직접 보이지 않지만 반복 로그의 basis change와 대응한다.", "예1의 x1 진입, slack 변수 탈락 과정.", "40/1, 100/2 등 비율은 가능한 증가량이다.", "음수 또는 0 이하 계수 행을 ratio 후보로 넣는 실수.", "simplex tableau", "pivot operation", "network flow의 arc flow 증가/용량 한계", "다음 pivot 열/행 선택.", ["entering", "leaving", "ratio"], ["비율", "기저"]),
            n("minimum_ratio_test", "최소비율검사", "minimum ratio test", "진입변수를 얼마나 늘릴 수 있는지 RHS/a_ij 중 최소 양수 비율로 판정하는 절차다.", "새 변수를 늘릴 때 가장 먼저 0이 되는 기존 기저변수를 찾는다.", "feasibility를 유지하면서 pivot row를 정할 때 쓴다.", "RHS와 entering 열의 양수 계수만 사용한다.", "목적함수와 직접 관계하지 않고 feasible movement의 한계를 찾는다.", "RHS/a_ij가 가장 작은 행이 leaving row가 된다.", "자원 소모량 대비 남은 자원이 가장 빨리 소진되는 제약을 찾는다.", "그래프에서는 이동 방향으로 닿는 첫 경계다.", "스프레드시트 수동 계산에서는 ratio 열을 따로 만든다.", "예1과 Phase I 타블로의 비율 열.", "50, 80, 40 중 최소가 leaving 후보가 되는 식으로 해석한다.", "a_ij<=0인 행을 포함하거나 최대비율을 고르는 오류.", "entering variable", "pivot operation", "capacity constraint의 bottleneck", "비율검사 후보와 제외 행 구분.", ["minimum_ratio", "ratio", "leaving"], ["비율검사", "비율"]),
            n("pivot_operation", "피벗 연산", "pivot operation", "pivot element를 1로 만들고 같은 열의 다른 값을 0으로 만들어 새 canonical form을 만드는 행 연산이다.", "좌표축을 새 기저변수 기준으로 갈아끼우는 과정이다.", "entering/leaving 변수가 정해진 뒤 tableau를 갱신할 때 쓴다.", "기저변수 목록과 tableau 행 전체가 바뀐다.", "목적행도 함께 갱신되어 z값 개선이 반영된다.", "새 기저변수의 열은 단위벡터가 되어야 한다.", "새 생산계획의 기준 활동을 바꾸는 회계 재정리다.", "BFS에서 인접 BFS로 이동한다.", "Solver 내부 basis factorization의 수동판이다.", "예1의 여러 tableau 갱신.", "pivot 후 RHS가 새 BFS의 변수값이다.", "pivot row만 바꾸고 나머지 행을 소거하지 않는 실수.", "minimum ratio test", "optimality test", "Gauss-Jordan elimination", "pivot 이후 목적행 부호 해석.", ["pivot", "basis", "tableau"], ["피벗", "기저"]),
            n("optimality_test", "최적성 판정", "optimality test", "목적행에 더 이상 개선 가능한 계수가 없으면 현재 BFS가 최적이라고 판정하는 규칙이다.", "더 좋은 인접 꼭짓점으로 갈 방향이 남아 있는지 확인한다.", "각 pivot 후 반복 종료 여부를 결정할 때 쓴다.", "비기저변수의 reduced cost/목적행 계수를 본다.", "max 문제와 min 문제의 부호 판정이 달라질 수 있다.", "개선 가능한 계수가 없으면 stop, 0 계수는 대안 최적 가능성을 뜻한다.", "어떤 생산활동을 추가해도 이익을 늘릴 수 없다는 뜻이다.", "목적 등위선이 최적 꼭짓점에 닿은 상태다.", "Solver 결과 상태 optimal과 연결된다.", "예1 최종 타블로.", "z=180 또는 z=30 같은 목적값을 변수값과 함께 읽는다.", "최적 판정과 feasible 판정을 혼동하는 오류.", "pivot operation", "multiple optima", "reduced cost", "최적/복수최적/계속진행 구분.", ["optimality", "reduced_cost"], ["최적", "목적함수 계수"]),
            n("multiple_optima", "복수 최적해", "multiple optimal solutions", "최적 타블로에서 비기저변수의 reduced cost가 0이면 다른 최적 BFS가 존재할 수 있다.", "목적함수 선이 가능영역의 모서리와 겹쳐 여러 점이 같은 목적값을 준다.", "최적성 판정 후 대안 해 여부를 확인할 때 쓴다.", "0 reduced cost인 nonbasic variable을 피벗 후보로 본다.", "목적값은 변하지 않고 해 벡터만 바뀐다.", "새 pivot을 해도 z가 동일하면 대안 최적해를 얻는다.", "서로 다른 생산계획이 같은 총이익을 만드는 상황이다.", "최적 face 위의 여러 BFS/convex combination.", "Solver가 하나만 보여줘도 동률 최적해가 있을 수 있다.", "예2의 z=280 대안 최적해.", "두 해 모두 z=280으로 동일하다는 점이 핵심이다.", "복수 최적을 아무 feasible point가 최적인 것처럼 말하는 오류.", "optimality test", "sensitivity objective range", "assignment의 복수 최적", "reduced cost 0의 의미.", ["multiple_optima", "alternate_optimum"], ["복수 최적해", "대안 최적해"]),
            n("unbounded_solution", "비유계", "unbounded solution", "feasible 해는 있지만 목적함수를 한없이 개선할 수 있어 유한 최적값이 없는 상태다.", "좋아지는 방향으로 움직이는데 제약 벽이 없는 경우다.", "entering 열에 leaving 후보가 없을 때 판정한다.", "진입변수는 늘어날 수 있지만 모든 관련 제약이 막지 않는다.", "max에서는 z가 무한 증가할 수 있다.", "entering column의 모든 제약행 계수가 <=0이면 ratio test가 불가능하다.", "제약을 빠뜨린 생산모형일 가능성이 크다.", "가능영역이 목적 개선 방향으로 열린 상태다.", "Solver에서는 unbounded 또는 model issue로 나타날 수 있다.", "예3의 x3 진입 시 목적함수 무한 개선.", "비유계는 infeasible과 달리 feasible point가 존재한다.", "비유계와 실행불가능을 혼동하는 오류.", "minimum ratio test", "model validation", "open feasible region", "unbounded 신호와 누락 제약 찾기.", ["unbounded", "비유계"], ["무한히 개선", "비유계"]),
            n("surplus_artificial_variable", "잉여/인위변수", "surplus/artificial variable", ">= 제약이나 = 제약에서 초기 기저를 만들기 위해 surplus를 빼고 artificial을 더하는 보조 변수다.", "slack은 남는 양, surplus는 초과량, artificial은 임시 발판이다.", "초기 BFS가 보이지 않는 min/greater-than 제약에서 쓴다.", "surplus s>=0, artificial r>=0를 원 제약에 넣는다.", "artificial은 원래 문제의 목적이 아니므로 제거되어야 한다.", "Phase I 또는 Big-M에서 artificial을 0으로 몰아낸다.", "최소 영양 요구량처럼 >= 제약이 있을 때 바로 slack basis가 안 생긴다.", "기저를 만들기 위한 좌표 보강이다.", "Solver는 내부적으로 처리하지만 손계산은 변수를 명시한다.", "예4와 식단 문제의 x5, x6, x9, x10 도입.", "artificial이 최종 양수이면 원문제 infeasible 가능성이 있다.", "artificial을 실제 의사결정변수로 해석하는 오류.", "standard form", "two-phase method, Big-M", "dummy supply와 달리 계산용 변수", "변수 도입 방향과 최종 제거 조건.", ["surplus", "artificial", "인위변수"], ["인위변수", "잉여변수"]),
            n("two_phase_method", "2단계법", "two-phase method", "Phase I에서 인위변수 합을 0으로 만들고, Phase II에서 원 목적함수로 최적화하는 심플렉스 절차다.", "출발점이 없을 때 임시 발판을 찾아 치운 뒤 원래 문제를 푼다.", "초기 BFS가 바로 없을 때 쓴다.", "Phase I 변수에는 artificial variables가 포함된다.", "Phase I은 min w=sum artificial, Phase II는 원 z다.", "w*=0이면 feasible basis를 얻고, w*>0이면 infeasible이다.", "식단 min 문제에서 영양 최소요구량 제약 때문에 필요하다.", "가능영역의 임의 꼭짓점부터 찾는 탐색 전처리다.", "Solver의 feasible start 탐색을 수동으로 분리한 형태다.", "예4와 식단문제 2단계 해법.", "w=0은 원 목적값이 아니라 feasible start 판별값이다.", "Phase I 목적값을 원문제 최적값으로 착각하는 오류.", "artificial variable", "Big-M, duality", "penalty method", "Phase I 종료 조건과 Phase II 전환.", ["two_phase", "Phase I", "Phase II"], ["2단계", "Phase"]),
            n("diet_two_phase", "식단문제 2단계 적용", "diet problem two-phase", "영양 최소 요구량을 만족하는 최소비용 식단을 2단계법으로 푸는 대표 min LP 예제다.", "필요 영양소를 넘겨야 하므로 >= 제약이 많아 초기 slack basis가 없다.", "최소화 문제의 two-phase 훈련용 예제로 쓴다.", "식품량 xi와 surplus/artificial variables.", "min z=식품 단가*식품량.", "비타민 A/C 최소 요구량 제약과 비음조건.", "영양 요구량을 만족하면서 비용을 줄이는 식단 구성이다.", "두 영양 제약의 교차점과 비용 등위선으로도 볼 수 있다.", "Solver에서는 변수셀 식품량, 제약셀 영양소 섭취량>=요구량.", "식단문제 P0-P4 전개.", "x5=22.5, x6=5 같은 해는 식품량 단위 해석이 필요하다.", "surplus와 artificial 부호를 뒤집는 오류.", "two-phase method", "Big-M, duality", "Stigler diet problem", ">= 제약 표준화.", ["diet", "two_phase", "min"], ["식단문제", "인위변수의 합"]),
        ],
        examples=[
            ex("example1_tableau", "예1 기본 타블로 최적화", "max z=3x1+2x2를 slack 변수와 tableau로 풀어 최적 생산량을 찾는다.", "x1, x2와 x3~x5 slack.", "max z=3x1+2x2.", "2x1+x2<=100, x1+x2<=80, x1<=40, x>=0.", "수동 tableau 또는 Solver Simplex LP.", "최종 RHS가 변수값, z행 RHS가 목적값이다.", ["표준형으로 바꾼다.", "진입열과 탈락행을 고른다.", "피벗 후 목적행 개선 가능성을 확인한다."], ["심플렉스 타블로를 이용"]),
            ex("multiple_optimum", "예2 복수 최적해 판정", "비기저변수 목적계수 0을 통해 같은 z=280의 대안 최적해를 찾는다.", "x1, x2, x3 및 slack 변수.", "max z=60x1+35x2+20x3.", "여러 자원 제약과 x2<=5.", "tableau에서 0 reduced cost pivot.", "최적해가 하나가 아니라 최적 face임을 해석한다.", ["최적 타블로를 확인한다.", "0 reduced cost 비기저변수를 찾는다.", "대안 pivot으로 새 최적 BFS를 계산한다."], ["복수 최적해"]),
            ex("unbounded_case", "예3 비유계 판정", "진입변수를 늘려도 leaving 후보가 없어 목적값을 무한히 개선하는 사례다.", "x variables and slack variables.", "max objective.", "제약이 개선 방향을 막지 못한다.", "ratio test 불가 판정.", "모형 제약 누락 또는 열린 가능영역으로 해석한다.", ["entering 열을 고른다.", "양수 계수 행이 없는지 본다.", "infeasible과 구분한다."], ["무한히 개선"]),
            ex("two_phase_example", "예4 2단계법", "인위변수 x5, x6을 도입해 Phase I feasible basis를 만들고 Phase II에서 원 목적함수를 푼다.", "x1, x2, x3, x4, artificial x5, x6.", "Phase I min w, Phase II max z.", "등식/부등식 변환 후 비음조건.", "Phase I tableau -> artificial 제거 -> Phase II tableau.", "w*=0이면 원문제 가능해가 존재한다.", ["인위변수를 넣는다.", "w를 최소화한다.", "w=0이면 원 목적행으로 전환한다."], ["2단계 해법", "1단계 문제"]),
        ],
        patterns=[
            ("표준형/타블로", "max/min LP를 등식과 비음조건으로 바꾼 뒤 tableau로 계산한다.", "simplex_tableau", "2변수 그래프 해법의 일반화"),
            ("특수 종료", "최적성 이후 0 reduced cost, ratio 불가, w>0 여부로 복수최적/비유계/infeasible을 판정한다.", "multiple_optima", "solver status 해석"),
            ("초기 BFS 생성", "slack만으로 basis가 없으면 artificial을 도입하고 Phase I을 실행한다.", "two_phase_method", "Big-M과 duality"),
        ],
        solver_rows=[
            ("변수셀", "원변수+slack/surplus/artificial", "수동 타블로의 열과 Solver 변수셀을 대응시킨다."),
            ("목표셀", "z 또는 Phase I의 w", "Phase I w와 원 목적함수 z를 혼동하지 않는다."),
            ("제약셀", "등식 변환된 제약행", "RHS는 현재 BFS의 변수값으로 읽는다."),
            ("해법", "Simplex LP", "초기 BFS가 없으면 two-phase/Big-M 설명을 붙인다."),
        ],
        cross_connections=[
            ("2강 LP 일반형", "모든 tableau는 LP 변수/제약/목적함수에서 출발한다.", "LP formulation -> tableau"),
            ("3강 그래프 해법", "꼭짓점 최적성이 tableau의 BFS 이동으로 바뀐다.", "vertex -> BFS"),
            ("DM_PDF05 Big-M/쌍대", "artificial variable 처리와 dual interpretation으로 이어진다.", "two-phase -> Big-M -> dual"),
        ],
        misconceptions=[
            ("비율검사에 음수 계수 포함", "leaving row를 잘못 잡아 infeasible tableau가 된다.", "양수 entering column 계수만 ratio 후보.", "minimum_ratio_test"),
            ("w=0을 원 목적값으로 해석", "Phase I은 실행가능성 확인용이다.", "Phase II에서 원 목적함수로 다시 최적화한다.", "two_phase_method"),
            ("비유계와 infeasible 혼동", "비유계는 feasible 해가 존재한다.", "ratio 후보 없음과 w*>0을 분리한다.", "unbounded_solution"),
        ],
        routes=[
            Route("타블로에서 다음 피벗 어떻게 골라?", "simplex_tableau", "entering_leaving_variable", "example1_tableau", "DM_PDF01:p001"),
            Route("복수 최적해인지 어떻게 알아?", "multiple_optima", "optimality_test", "multiple_optimum", "DM_PDF01:p002"),
            Route("2단계법 왜 필요해?", "two_phase_method", "surplus_artificial_variable", "two_phase_example", "DM_PDF01:p004"),
            Route("비유계와 infeasible 차이?", "unbounded_solution", "two_phase_method", "unbounded_case", "DM_PDF01:p003"),
        ],
        practice=[
            "타블로 하나를 골라 entering column과 leaving row를 말로 설명하라.",
            "Phase I w*=0의 의미와 w*>0의 의미를 각각 한 문장으로 구분하라.",
            "비유계 신호를 ratio test 관점에서 설명하라.",
        ],
        web_refs=["WEB_OR_TOOLS_LP", "WEB_MS_SOLVERADD", "WEB_MS_SOLVERSOLVE"],
        qc_notes=["수식 OCR이 깨진 페이지가 있어 숫자 타블로는 원본 PDF와 대조해야 한다."],
    ),
    Profile(
        source_id="DM_PDF02",
        slug="ch05_sensitivity_analysis",
        title="Ch.5 민감도 분석",
        normalized_pdf="DM_PDF02_ch05_sensitivity_analysis.pdf",
        thesis="민감도 분석은 최적해를 하나의 답으로 끝내지 않고, 목적계수와 RHS 변화가 기존 basis와 경제적 해석을 어디까지 유지하는지 읽는 절차다.",
        graph_position="LP 최적해 -> binding/nonbinding -> shadow price/reduced cost -> allowable range -> Solver sensitivity report.",
        learning_outcomes=[
            "reduced cost, shadow price, allowable increase/decrease를 서로 다른 질문으로 분리한다.",
            "허용범위 안과 밖에서 해석 방식이 달라진다는 점을 설명한다.",
            "유모차-보행기 예제를 그래프, Solver 보고서, 경제적 언어로 번역한다.",
        ],
        nodes=[
            n("sensitivity_analysis", "민감도 분석", "sensitivity analysis", "최적해 주변에서 목적계수와 제약 RHS 변화가 목적값과 basis에 미치는 영향을 분석하는 절차다.", "해 하나를 구한 뒤 그 해가 얼마나 흔들림에 강한지 보는 사후 진단이다.", "최적해를 얻은 뒤 자원량, 이익계수, 수요상한이 바뀌는 질문에 쓴다.", "기존 LP의 변수 x1, x2와 제약 RHS/목적계수.", "기존 objective coefficient가 바뀔 때 z 변화 또는 basis 유지 여부를 본다.", "RHS 변화는 shadow price와 allowable range로 해석한다.", "기계 시간이 1시간 더 생기면 이익이 얼마나 늘어나는가라는 질문이다.", "그래프에서는 최적 꼭짓점과 등위이익선의 접촉이 얼마나 유지되는지 본다.", "Solver sensitivity report의 Variable Cells/Constraints 섹션을 읽는다.", "유모차-보행기 생산계획.", "x1*=0, x2*=40 같은 최적해에서 비생산 제품과 병목 자원을 해석한다.", "shadow price를 허용범위 밖까지 무제한 적용하는 오류.", "LP optimal solution, binding constraint", "duality, transportation sensitivity", "what-if analysis", "보고서 수치를 해석시키는 문제.", ["sensitivity", "민감도", "allowable"], ["민감도 분석 sensitivity"]),
            n("product_mix_model", "유모차-보행기 생산모형", "stroller-walker product mix", "두 제품 생산량을 결정해 기계시간과 수요 제약 아래 총판매이익을 최대화하는 LP 예제다.", "제한된 기계시간을 어느 제품에 쓸지 배분하는 문제다.", "민감도 해석의 기준 LP로 쓴다.", "x1=유모차 생산량, x2=보행기 생산량.", "max 30x1+20x2.", "기계1/2/3 시간 제약과 x2<=40.", "기계별 시간은 자원 RHS, 제품 이익은 목적계수다.", "2변수 가능영역과 등위이익선으로 볼 수 있다.", "Solver에서 변수셀 x1,x2, 목표셀 총이익, 제약셀 기계시간/수요.", "DM_PDF02 초반 유모차-보행기 문제.", "기계1 8x1+3x2<=240처럼 제품별 사용시간이 제약계수다.", "제품 이름을 변수로 두지 않고 수익 자체를 변수로 두는 오류.", "LP formulation", "sensitivity report", "Super Grain 같은 product mix", "문장 문제를 LP 식으로 세우기.", ["product_mix", "유모차", "보행기"], ["유모차-보행기", "유모차 생산량"]),
            n("binding_constraint", "결합/비결합 제약", "binding/nonbinding constraint", "최적해에서 좌변이 RHS와 같으면 binding, 여유가 남으면 nonbinding인 제약이다.", "완전히 다 쓴 자원은 병목이고, 남는 자원은 한 단위 더 줘도 즉시 가치가 없다.", "shadow price 해석 전 제약 상태를 구분할 때 쓴다.", "constraint LHS and RHS.", "목적함수 변화는 binding 자원에서 더 민감하다.", "binding은 slack=0, nonbinding은 slack>0.", "기계시간이 꽉 찼는지 남았는지 확인한다.", "최적 꼭짓점에서 접하는 경계선과 아닌 경계선이다.", "Solver Constraints 섹션의 Final Value와 Constraint RHS를 비교한다.", "기계1/2/3 및 보행기 수요 제약.", "기계1 시간이 240에 가까우면 병목 후보가 된다.", "nonbinding 제약의 shadow price를 양수로 해석하는 오류.", "LP feasible region", "shadow price", "slack variable", "binding 여부와 shadow price 관계.", ["binding", "slack", "constraint"], ["제한조건 우변", "기계1"]),
            n("shadow_price", "잠재가격", "shadow price", "제약 RHS를 1단위 완화했을 때 목적값이 변하는 한계 가치다.", "부족한 자원을 한 단위 더 살 수 있다면 얼마까지 지불할 수 있는지 보는 가격이다.", "자원량 증가/감소 질문에서 쓴다.", "제약 i의 RHS b_i 변화량 Delta b_i.", "Delta z = shadow price * Delta b_i, 허용범위 안에서만.", "binding 제약은 양/음의 가치가 가능하고 nonbinding은 보통 0이다.", "기계1 시간이 1시간 늘면 이익이 5.33만원 증가한다는 식이다.", "쌍대변수 y_i와 같은 경제적 의미다.", "Solver Constraints 섹션의 Shadow Price.", "기계1 작업가능시간 예시.", "241시간으로 늘릴 때 5.33만원 증가.", "잠재가격을 실제 시장가격으로 무조건 동일시하는 오류.", "binding constraint", "duality", "marginal value", "허용 RHS 범위와 함께 계산.", ["shadow_price", "잠재가격"], ["잠재가격", "Shadow price"]),
            n("reduced_cost", "감소비용/한계비용", "reduced cost", "현재 0 또는 경계에 있는 변수의 값을 한 단위 움직일 때 목적값이 얼마나 불리하게 변하는지 나타내는 값이다.", "선택되지 않은 제품이 왜 생산되지 않는지 알려주는 기회비용이다.", "변수셀이 0인 제품의 진입 가능성을 해석할 때 쓴다.", "nonbasic variable x_j와 objective coefficient c_j.", "max에서 c_j - y^T a_j가 개선 필요량/기회비용으로 읽힌다.", "기저 밖 변수는 reduced cost가 0이 되어야 들어올 수 있다.", "유모차 생산량을 0에서 1로 강제로 늘리면 이익이 감소하는 해석이다.", "타블로 목적행 계수와 연결된다.", "Solver Variable Cells 섹션의 Reduced Cost.", "유모차 x1의 한계비용 설명.", "x1을 1개 늘리면 목적값이 12.67 줄어드는 사례.", "reduced cost를 단위 생산비로 오해하는 오류.", "duality shadow price", "objective coefficient range", "opportunity cost", "비생산 변수의 해석.", ["reduced_cost", "한계비용", "수정비용"], ["Reduced cost", "한계비용"]),
            n("allowable_objective_range", "목적계수 허용범위", "allowable objective coefficient range", "현재 최적해 또는 basis가 유지되는 목적계수 변화 범위다.", "제품 이익이 어느 정도 바뀌어도 최적 생산계획이 그대로인지 보는 안정성 범위다.", "판매이익/단위비용이 변하는 질문에 쓴다.", "c_j current value, allowable increase/decrease.", "c_j가 범위 안이면 basis 유지, z만 새 계수로 재계산한다.", "범위를 벗어나면 새 LP를 다시 풀어야 한다.", "보행기 이익이 20에서 18로 낮아지는 경우.", "등위이익선의 기울기가 같은 최적 꼭짓점 범위 내에서 움직인다.", "Solver Variable Cells의 Objective Coefficient와 Allowable Increase/Decrease.", "목표셀 계수 변화 민감도 보고서.", "30 -> 20 같은 변경이 최적해를 바꾸는지 판단한다.", "허용증가/감소를 새 계수 자체와 혼동하는 오류.", "reduced cost", "sensitivity report", "iso-profit line", "계수 변화 후 재계산 여부.", ["allowable", "objective", "목적계수"], ["목표셀 계수", "허용가능"]),
            n("allowable_rhs_range", "RHS 허용범위", "allowable RHS range", "shadow price가 변하지 않는 제약 RHS 변화 구간이다.", "자원을 조금 더 주거나 덜 줄 때 같은 병목 구조가 유지되는 구간이다.", "자원량 변경 질문에서 쓴다.", "b_i current RHS, allowable increase/decrease.", "Delta z=shadow price*Delta b_i는 이 범위 안에서만 적용한다.", "범위를 벗어나면 binding set이 바뀔 수 있다.", "기계1 이용가능시간을 237시간으로 줄이는 질문.", "가능영역 경계선이 평행 이동해도 같은 꼭짓점 구조가 유지되는 구간이다.", "Solver Constraints 섹션의 Allowable Increase/Decrease.", "우변값 변화 민감도 보고서.", "3시간 감소면 3*5.33만큼 이익 감소처럼 계산한다.", "allowable range 밖에서도 같은 shadow price를 쓰는 오류.", "shadow price", "post-optimal analysis", "resource valuation", "RHS 변화 계산.", ["RHS", "allowable", "허용범위"], ["우변 값", "허용 가능의 범위"]),
            n("solver_sensitivity_report", "Solver 민감도 보고서", "Solver sensitivity report", "Solver가 최적해 이후 변수별 reduced cost와 제약별 shadow price 및 허용범위를 표로 제공하는 보고서다.", "해답지 뒤의 해설표처럼, 왜 그 해가 나왔고 어디까지 유지되는지 알려준다.", "Excel Solver 해찾기 결과 후 민감도 옵션을 선택해 쓴다.", "Variable Cells and Constraints report fields.", "목표셀 값과 계수 변화 범위를 함께 본다.", "제약 final value, RHS, shadow price, allowable ranges를 본다.", "생산계획의 사후 해석 자료다.", "타블로의 reduced cost/dual price를 표로 출력한 것이다.", "해찾기 결과 대화상자에서 민감도 선택.", "DM_PDF02 p026 설명.", "Variable Cells와 Constraints 섹션을 혼동하지 않는다.", "보고서 수치를 문제 원문 단위와 연결하지 않는 오류.", "Solver model", "duality and sensitivity", "tableau final row", "보고서 읽기.", ["solver", "sensitivity_report"], ["민감도 보고서", "해찾기 결과"]),
        ],
        examples=[
            ex("stroller_walker_lp", "유모차-보행기 LP 정식화", "유모차와 보행기 생산량을 정해 총판매이익을 최대화한다.", "x1=유모차, x2=보행기.", "max 30x1+20x2.", "기계1 8x1+3x2<=240, 기계2 4x1+4x2<=200, 기계3 4x1<=100, x2<=40.", "Solver Simplex LP, 변수셀 x1:x2.", "최적해는 각 제약의 binding 여부와 함께 해석해야 한다.", ["변수를 둔다.", "기계별 시간 제약을 쓴다.", "최적해 후 민감도 보고서를 읽는다."], ["유모차-보행기", "유모차 생산량"]),
            ex("shadow_price_machine1", "기계1 1시간 추가 해석", "기계1 RHS가 1시간 늘 때 이익 증가분을 잠재가격으로 계산한다.", "Delta b_machine1=1.", "Delta z=shadow price*Delta b.", "허용 RHS 범위 안이어야 한다.", "Sensitivity Report Constraints 섹션.", "5.33만원 증가처럼 한계가치를 해석한다.", ["binding 여부 확인.", "shadow price 확인.", "allowable range 확인.", "Delta z 계산."], ["기계1의 제한조건을 241시간"]),
            ex("reduced_cost_stroller", "유모차 한계비용 해석", "현재 생산하지 않는 유모차를 1개 강제로 만들 때 목적값 변화를 본다.", "Delta x1=1.", "변수 경계 이동에 따른 objective penalty.", "나머지 제약 feasibility 재조정.", "Variable Cells Reduced Cost.", "생산 안 하는 이유를 자원 가치와 비교해 설명한다.", ["x1 final value 확인.", "reduced cost 확인.", "강제 생산 시 목적값 변화 해석."], ["한계비용", "유모차의 현재 계산값"]),
        ],
        patterns=[
            ("자원가치형", "RHS 1단위 변화 질문은 shadow price와 allowable RHS range로 답한다.", "shadow_price", "duality"),
            ("제품경쟁력형", "현재 0인 변수의 진입 질문은 reduced cost와 목적계수 허용범위로 답한다.", "reduced_cost", "tableau reduced cost"),
            ("보고서해석형", "Solver sensitivity report는 Variable Cells와 Constraints를 분리해 읽는다.", "solver_sensitivity_report", "Excel Solver"),
        ],
        solver_rows=[
            ("변수셀", "x1 유모차 생산량, x2 보행기 생산량", "Variable Cells에서 final value, reduced cost, objective coefficient를 읽는다."),
            ("목표셀", "총판매이익", "목표계수 변화는 Objective Coefficient range로 해석한다."),
            ("제약셀", "기계시간/수요 제약 LHS", "Constraints에서 final value, shadow price, RHS range를 읽는다."),
            ("주의", "허용범위 밖 변화", "기존 보고서 숫자를 쓰지 말고 다시 Solver/그래프 해법을 실행한다."),
        ],
        cross_connections=[
            ("DM_PDF05 쌍대성", "shadow price는 쌍대변수의 경제적 의미와 직접 연결된다.", "dual variable -> shadow price"),
            ("DM_PDF06 수송 민감도", "수송비와 공급량 변화도 reduced cost/shadow price로 해석한다.", "sensitivity -> transportation"),
            ("DM_PDF01 타블로", "reduced cost는 최종 타블로 목적행 계수와 같은 정보를 담는다.", "tableau -> report"),
        ],
        misconceptions=[
            ("shadow price 무제한 적용", "허용범위 밖에서는 basis가 바뀐다.", "Allowable Increase/Decrease 확인 후 적용.", "shadow_price"),
            ("reduced cost를 회계비용으로 해석", "현재 basis 기준의 기회비용이다.", "변수 final value와 함께 해석.", "reduced_cost"),
            ("Variable/Constraint 섹션 혼동", "제품 계수와 자원 RHS 질문의 표가 다르다.", "질문 유형부터 분류.", "solver_sensitivity_report"),
        ],
        routes=[
            Route("자원 1단위 늘리면 이익?", "shadow_price", "allowable_rhs_range", "shadow_price_machine1", "DM_PDF02:p030"),
            Route("생산 안 하는 제품은 왜 안 해?", "reduced_cost", "product_mix_model", "reduced_cost_stroller", "DM_PDF02:p028"),
            Route("목적계수 바뀌면 해 유지돼?", "allowable_objective_range", "solver_sensitivity_report", "stroller_walker_lp", "DM_PDF02:p029"),
            Route("민감도 보고서 어디 봐?", "solver_sensitivity_report", "sensitivity_analysis", "stroller_walker_lp", "DM_PDF02:p026"),
        ],
        practice=[
            "기계1 RHS가 3 감소할 때 허용범위 안이라면 이익 변화식을 써라.",
            "reduced cost와 shadow price를 각각 변수 질문/제약 질문으로 분류하라.",
            "목적계수 허용범위를 벗어나면 왜 재최적화가 필요한지 설명하라.",
        ],
        web_refs=["WEB_OR_TOOLS_LP", "WEB_MS_SOLVERADD", "WEB_MS_SOLVERSOLVE"],
    ),
    Profile(
        source_id="DM_PDF03",
        slug="ch06_branch_and_bound",
        title="Ch.6 분지한계법",
        normalized_pdf="DM_PDF03_ch06_branch_and_bound.pdf",
        thesis="분지한계법은 정수조건으로 생긴 불연속성을 LP 완화의 상한과 발견된 정수해의 하한으로 좁혀 가며 탐색하는 알고리즘이다.",
        graph_position="정수계획 모형 -> LP relaxation -> branching floor/ceil -> upper/lower bounds -> pruning -> incumbent optimum.",
        learning_outcomes=[
            "LP 완화값 Z와 현재 정수가능해 L의 방향을 최대화 문제 기준으로 구분한다.",
            "floor/ceil 분기 제약을 만들고 subproblem tree를 읽는다.",
            "비가해, bound 열세, 정수해 발견에 따른 세 가지 절단 사유를 설명한다.",
        ],
        nodes=[
            n("branch_and_bound", "분지한계법", "branch and bound", "LP 완화로 bound를 만들고 정수조건 위반 변수를 floor/ceil로 분기해 정수 최적해를 찾는 방법이다.", "연속해가 소수이면 그 소수가 들어갈 수 없는 두 구간으로 쪼개며 가능성을 지운다.", "순수/혼합 정수계획을 exact하게 풀 때 쓴다.", "정수조건이 붙은 x_j와 각 subproblem의 LP relaxation 변수.", "max IP에서는 LP relaxation Z가 상한 역할을 한다.", "분기 제약과 원 제약, 정수조건을 반복 적용한다.", "차량 대수처럼 2.9대가 불가능한 결정을 정수해로 고정한다.", "subproblem tree의 각 노드가 feasible region 일부다.", "Solver의 branch-and-bound/MIP search와 대응한다.", "이콤전자 승합차 구입 예제.", "초기 LP 완화해 x1=2.90, x2=1.72, Z=45.05에서 시작한다.", "LP 완화해를 반올림해 답으로 쓰는 오류.", "integer programming", "cutting planes, branch-and-cut", "binary search tree", "분기/한계/절단 순서 설명.", ["branch_bound", "분지한계"], ["분지한계법", "branchandbound"]),
            n("lp_relaxation", "LP 완화", "LP relaxation", "정수 제한조건을 잠시 제거해 연속 LP로 푸는 완화 문제다.", "정수 격자점만 보기 전에 더 넓은 다각형에서 제일 좋은 값을 먼저 본다.", "각 노드의 bound를 계산할 때 쓴다.", "integer variables without integer restriction.", "max에서는 완화 최적값이 원 IP 최적값 이상이므로 upper bound다.", "원래 제약은 유지하되 integrality만 제거한다.", "2.90대 차량처럼 현실 불가능하지만 bound로 유용한 해다.", "정수 feasible set을 포함하는 큰 polyhedron이다.", "Solver에서 int/bin 조건을 끈 Simplex LP와 유사하다.", "부문제0 LP 완화.", "x1=2.90, x2=1.72는 정수해가 아니지만 상한 Z=45.05를 준다.", "반올림 feasible/optimal 보장 착각.", "LP formulation", "branching strategy", "continuous relaxation", "LP 완화값의 bound 방향.", ["LP_relaxation", "완화"], ["LP완화", "정수제한조건만 삭제"]),
            n("upper_lower_bound", "상한/하한", "upper/lower bound", "max 문제에서 LP 완화값 Z는 상한, 현재 가장 좋은 정수가능해 L은 하한이다.", "아직 볼 가치가 있는지 판단하는 기대 최고치와 현재 확보한 점수다.", "pruning과 incumbent 갱신에 쓴다.", "Z per subproblem, L incumbent.", "Z<=L이면 더 좋은 정수해 가능성이 없으므로 절단한다.", "정수해 발견 시 L=max(L,Z_integer)로 갱신한다.", "현재 최고 정수해보다 못할 가지를 버린다.", "tree search에서 노드의 potential value.", "MIP Solver gap, incumbent/best bound와 연결된다.", "부문제6 L=38, 부문제12 L=40.", "L이 갱신되면 남은 노드의 Z와 다시 비교한다.", "최대화/최소화에서 bound 방향을 뒤집는 오류.", "LP relaxation", "pruning", "MIP optimality gap", "Z와 L 비교.", ["bound", "upper", "lower", "Z", "L"], ["", "", "상한값", "하한값"]),
            n("branching_floor_ceil", "floor/ceil 분기", "floor/ceil branching", "소수값을 가진 정수변수 x_j=v에 대해 x_j<=floor(v), x_j>=ceil(v) 두 제약으로 나누는 전략이다.", "2.90이라는 불가능한 값 주변을 2 이하와 3 이상으로 쪼갠다.", "LP 완화해가 정수가 아닐 때 쓴다.", "fractional integer-constrained variable.", "목적함수는 각 새 부문제 LP에서 다시 계산한다.", "새로 생긴 하한/상한 제약이 원 제약에 추가된다.", "차량 x1=2.90이면 x1<=2 또는 x1>=3이다.", "정수 격자 feasible set을 두 하위 영역으로 분할한다.", "Solver의 branching node creation.", "x1>=3 부문제1, x1<=2 부문제2.", "ceil/floor가 분기 제약 RHS다.", "x=2.90에서 x<=3, x>=2처럼 겹치게 분기하는 오류.", "LP relaxation fractional solution", "subproblem tree", "binary decision split", "분기 제약 쓰기.", ["branching", "floor", "ceil"], ["하한제약", "상한제약", "소수값"]),
            n("pruning_rules", "절단 규칙", "pruning rules", "비가해, Z<=L, 정수해 발견 후 L 갱신 같은 이유로 더 이상 분지하지 않는 규칙이다.", "좋아질 수 없는 길은 계산을 멈춰 탐색을 줄인다.", "각 subproblem LP를 푼 뒤 판단한다.", "subproblem status, Z value, integer feasibility.", "max에서 Z<=L이면 절단.", "infeasible이면 절단, integer feasible이면 incumbent 갱신 후 절단.", "새로 얻은 정수해보다 못할 가능성의 가지를 버린다.", "tree에서 leaf/fathomed node로 표시된다.", "Solver MIP log의 fathomed/pruned node.", "부문제3/7/9/11 비가해 절단, 부문제10 Z<L 절단.", "부문제12에서 L=40으로 갱신 후 종료.", "정수해가 나오면 무조건 전체 최적이라고 조기 종료하는 오류.", "upper/lower bound", "incumbent", "search tree pruning", "세 가지 절단 사유 구분.", ["pruning", "절단"], ["절단", "비가해"]),
            n("incumbent_solution", "현재 최선 정수해", "incumbent solution", "탐색 중 발견한 가장 좋은 정수가능해와 그 목적값 L이다.", "현재까지 확보한 방어선이다.", "새 정수해를 발견할 때마다 갱신한다.", "integer feasible solution x and objective L.", "max에서는 더 큰 정수 목적값이면 incumbent 갱신.", "incumbent는 feasible이어야 한다.", "차량구입에서 x1=3,x2=1,Z=38 후 나중에 x1=2,x2=2,Z=40으로 갱신된다.", "tree search lower bound.", "Solver의 incumbent objective.", "부문제6과 부문제12.", "L=40이 최종 정수 최적값이다.", "LP 완화 fractional 해를 incumbent로 저장하는 오류.", "integer feasible solution", "optimality proof", "best-so-far heuristic", "incumbent 갱신 조건.", ["incumbent", "L", "정수가능해"], ["정수해", "←"]),
            n("node_selection", "노드 선택", "node selection", "검토할 부문제 중 어떤 노드를 다음에 풀지 고르는 전략이다.", "가장 가능성 큰 길부터 볼지, 깊게 들어갈지 정하는 탐색 순서다.", "여러 open subproblem이 있을 때 쓴다.", "candidate subproblem list and their Z values.", "강의 예제는 목적함수값 Z가 큰 부문제를 우선 선택한다.", "선택 후 fractional variable로 분기한다.", "최고 상한을 가진 가지부터 확인한다.", "best-bound search에 가깝다.", "Solver는 best-bound, depth-first 등 다양한 node selection을 쓴다.", "부문제4,5,8 선택 순서.", "Z가 큰 부문제부터 적용한다는 지시가 반복된다.", "검토할 부문제를 임의로 골라도 된다고 생각해 증명 흐름을 놓치는 오류.", "upper bound", "branching strategy", "priority queue search", "다음 노드 선택 이유.", ["node_selection", "best_bound"], ["목적함수값이", "부문제부터"]),
            n("ecom_van_example", "이콤전자 승합차 예제", "Ecom van purchase example", "승합차 구매대수를 정수로 결정하는 정수계획을 분지한계법으로 푸는 주 예제다.", "차량은 소수대로 살 수 없으므로 LP 완화해를 분기해야 한다.", "분지한계법 전 과정을 추적하는 데 쓴다.", "x1, x2 integer vehicle counts.", "maximize 9x1+15x2.", "예산/공간 등 자원 제약과 x1>=1.", "승합차 대수 결정의 정수성 때문에 생긴 탐색 문제다.", "2D LP 가능영역 위 정수점 탐색이다.", "Solver MIP로도 풀 수 있지만 강의는 tree를 수동 전개한다.", "예제6.9.", "최종 x1=2, x2=2, Z=40.", "x1=2.90,x2=1.72를 반올림해 x1=3,x2=2로 쓰는 오류.", "integer formulation", "branch-and-bound proof", "knapsack-like resource allocation", "전체 트리와 최종해.", ["Ecom", "van", "예제6.9"], ["이콤전자", "승합차"]),
        ],
        examples=[
            ex("root_relaxation", "부문제0 LP 완화", "정수조건을 제거하고 최초 LP 완화해와 Z를 구한다.", "x1, x2 차량 대수.", "max 9x1+15x2.", "자원 제약과 x1>=1, integrality 제거.", "Simplex LP root relaxation.", "Z=45.05는 max IP의 상한이다.", ["LP 완화를 푼다.", "정수 여부를 본다.", "소수이면 첫 부문제0으로 둔다."], ["부문제 0", "45.05"]),
            ex("x1_branch", "x1 첫 분기", "x1=2.90에서 x1>=3과 x1<=2로 두 부문제를 만든다.", "x1 fractional.", "각 부문제에서 LP objective 재계산.", "원 제약 + 새 분기 제약.", "MIP branching.", "두 가지가 정수 feasible set을 빠짐없이 나눈다.", ["소수 변수를 고른다.", "floor/ceil를 계산한다.", "두 부문제의 LP를 다시 푼다."], ["x1≥3", "x1≤2"]),
            ex("final_incumbent", "부문제12 최종 incumbent", "x1=2,x2=2,Z=40인 정수해를 얻고 남은 부문제가 없어 최적을 확정한다.", "integer x1,x2.", "Z=40.", "모든 open node 절단/소진.", "branch-and-bound tree proof.", "L=40이 최종 최적 목적값이다.", ["정수해 확인.", "L 갱신.", "남은 부문제 없음 확인."], ["부문제 12", "최적해"]),
        ],
        patterns=[
            ("LP완화-분기", "소수 LP 해를 floor/ceil 제약으로 분할한다.", "branching_floor_ceil", "MIP solver"),
            ("bound-절단", "Z와 L을 비교해 볼 가치 없는 부문제를 제거한다.", "pruning_rules", "optimality proof"),
            ("incumbent-증명", "현재 최고 정수해와 모든 남은 상한의 비교로 최적성을 증명한다.", "incumbent_solution", "MIP gap"),
        ],
        solver_rows=[
            ("변수셀", "정수 또는 혼합정수 변수", "Solver에서 int/bin 조건을 둔다."),
            ("목표셀", "각 subproblem LP의 Z와 incumbent L", "Z는 bound, L은 발견된 정수해다."),
            ("제약셀", "원 제약 + 분기 제약", "x_j<=floor(v), x_j>=ceil(v)를 추가한다."),
            ("해법", "MIP branch-and-bound", "정수 최적화 비율이 있으면 gap 해석을 붙인다."),
        ],
        cross_connections=[
            ("DM_PDF04 정수계획", "분지한계법은 정수계획 모형의 대표 exact solution method다.", "IP -> B&B"),
            ("DM_PDF01 심플렉스", "각 노드의 LP 완화는 simplex/LP solver로 풀린다.", "simplex -> node bound"),
            ("DM_PDF08 0-1 응용", "set covering 같은 0-1 모형도 branch-and-bound 대상이다.", "binary model -> B&B"),
        ],
        misconceptions=[
            ("LP 완화해 반올림", "반올림해는 feasibility와 optimality가 보장되지 않는다.", "분기와 bound로 증명해야 한다.", "lp_relaxation"),
            ("Z/L 방향 반대", "max에서 Z는 상한, L은 하한이다.", "최소화 문제와 방향을 구분한다.", "upper_lower_bound"),
            ("정수해 발견 즉시 종료", "남은 open node의 upper bound가 L보다 클 수 있다.", "남은 노드 절단 여부를 확인한다.", "incumbent_solution"),
        ],
        routes=[
            Route("LP 완화해가 소수면?", "lp_relaxation", "branching_floor_ceil", "x1_branch", "DM_PDF03:p001"),
            Route("언제 가지를 자르나?", "pruning_rules", "upper_lower_bound", "final_incumbent", "DM_PDF03:p002"),
            Route("최종 최적성은 어떻게 증명?", "incumbent_solution", "pruning_rules", "final_incumbent", "DM_PDF03:p008"),
            Route("Ecom 예제 전체 흐름?", "ecom_van_example", "branch_and_bound", "root_relaxation", "DM_PDF03:p003"),
        ],
        practice=[
            "x=4.76이면 어떤 두 분기 제약을 만드는가?",
            "max 문제에서 Z=36, L=38이면 왜 절단되는지 설명하라.",
            "부문제12가 최적해가 되는 논리를 tree 기준으로 말하라.",
        ],
        web_refs=["WEB_OR_TOOLS_MIP"],
    ),
]


def add_more_profiles() -> None:
    """Append the remaining profiles while keeping the top-level literal readable."""
    PROFILES.extend(
        [
            build_dm04(),
            build_dm05(),
            build_dm06(),
            build_dm07(),
            build_dm08(),
        ]
    )


def build_dm04() -> Profile:
    return Profile(
        source_id="DM_PDF04",
        slug="ch06_integer_programming_week1",
        title="Ch.6 정수계획 1주차",
        normalized_pdf="DM_PDF04_ch06_integer_programming_week1.pdf",
        thesis="정수계획은 LP의 변수 일부 또는 전부에 정수/0-1 의미를 부여해 개수, 선택, 개방 여부 같은 불연속 의사결정을 모델링한다.",
        graph_position="LP formulation -> integer/binary domains -> Solver int/bin settings -> knapsack/capital budgeting/fixed-charge/facility-production models.",
        learning_outcomes=[
            "순수정수, 혼합정수, 0-1 정수계획을 구분한다.",
            "0-1 배낭, 자본예산, fixed-charge model의 변수와 논리제약을 세운다.",
            "Solver의 정수 최적화 비율과 bin/int 조건을 해석한다.",
        ],
        nodes=[
            n("integer_programming", "정수계획", "integer programming", "목적함수와 제약은 선형이지만 변수에 정수 또는 0-1 조건이 붙는 최적화 모형이다.", "사람 수, 공장 개방 여부, 프로젝트 선택처럼 쪼갤 수 없는 결정을 다룬다.", "LP 해가 소수로 나오면 현실 의사결정이 불가능한 경우에 쓴다.", "x_j integer 또는 binary.", "LP와 같은 선형 목적함수를 유지한다.", "선형 제약 + integrality domain.", "공장 가동 여부는 0/1, 생산량은 연속 또는 정수일 수 있다.", "LP 가능영역 중 정수 격자점만 허용한다.", "Solver에서 변수셀에 int/bin 제약을 추가한다.", "정수계획 적용 상황 전체.", "실수 최적해와 정수 최적해 목적값이 다를 수 있다.", "LP 해를 반올림해 정수 최적해로 쓰는 오류.", "LP formulation", "branch and bound", "discrete optimization", "정수조건 추가 이유.", ["integer_programming", "정수계획"], ["Integer Programming", "정수 계획"]),
            n("pure_mixed_binary_ip", "순수/혼합/0-1 IP", "pure/mixed/binary IP", "모든 변수가 정수면 순수정수, 일부만 정수면 혼합정수, 모든 변수가 0/1이면 0-1 정수계획이다.", "변수의 의미가 개수인지 선택인지 연속 생산량인지에 따라 도메인이 달라진다.", "문제 유형을 먼저 분류할 때 쓴다.", "integer x, continuous x, binary y.", "목적함수 자체보다 변수 도메인이 분류 기준이다.", "x integer, y in {0,1} 같은 domain constraints.", "생산량은 연속이고 공장 가동여부는 0/1이면 혼합정수다.", "feasible lattice 또는 binary hypercube.", "Solver에서는 int와 bin 조건을 따로 지정한다.", "p002의 세 유형 구분.", "all integer/mixed integer/0-1 integer.", "0-1 변수에 별도 비음조건을 중복해 핵심을 흐리는 오류.", "variable definition", "model classification", "domain modeling", "유형 판별.", ["pure", "mixed", "binary", "0-1"], ["순수 정수", "혼합 정수", "0/1"]),
            n("solver_integer_tolerance", "Solver 정수 최적화 비율", "integer optimality tolerance", "Solver가 LP 완화 최적값 대비 현재 정수해가 충분히 가까우면 멈출 수 있게 하는 gap 기준이다.", "정확한 증명 대신 계산시간과 정확도 사이의 타협값이다.", "Excel Solver에서 정수해가 기대와 다를 때 확인한다.", "objective incumbent and relaxation bound.", "gap percent 기준으로 종료할 수 있다.", "정수조건 무시 체크 해제와 최적화 비율 설정이 필요하다.", "1% gap이면 완전 최적 전 정수해를 반환할 수 있다.", "branch-and-bound gap interpretation.", "Solver 옵션의 모든해법/정수 제한조건 설정.", "p004-p006 Solver 옵션 설명.", "0% 설정은 더 정확하지만 시간이 늘 수 있다.", "정수조건을 체크하지 않고 연속 LP 해를 받은 뒤 최적이라고 하는 오류.", "integer programming", "branch-and-bound gap", "MIP solver settings", "Solver 옵션 해석.", ["solver", "integer_tolerance", "gap"], ["정수 최적화 비율", "정수 제한 조건"]),
            n("knapsack_problem", "0-1 배낭문제", "0-1 knapsack problem", "제한된 용량 안에서 선택가치 합을 최대화하도록 물건 선택 여부를 0/1로 결정하는 모형이다.", "가방 무게 한도 안에서 어떤 보물을 넣을지 고르는 문제다.", "한 개 또는 소수의 자원제약 아래 선택 문제에 쓴다.", "x_j=보물 j 선택 여부.", "max sum value_j x_j.", "sum weight_j x_j <= capacity, x_j in {0,1}.", "선택하면 전체 물건이 들어가고 일부만 넣을 수 없다.", "0-1 hypercube와 용량 반공간의 교집합.", "Solver 변수셀을 binary로 설정하고 무게합<=한도.", "보물 선택여부 예제.", "LP 완화에서는 fractional item이 나올 수 있다.", "LP 완화의 fractional 선택을 실제 선택으로 해석하는 오류.", "binary variable", "capital budgeting", "resource allocation", "배낭 식 세우기.", ["knapsack", "배낭"], ["배낭문제", "보물"]),
            n("lp_relaxation_ratio", "배낭 LP 완화와 효과/비용", "knapsack LP relaxation ratio", "0-1 조건을 풀면 효과/비용 순으로 fractional 할당해 완화해를 쉽게 얻을 수 있다.", "물건을 쪼갤 수 있다고 가정하면 효율 좋은 것부터 담는다.", "branch-and-bound bound 계산을 이해할 때 쓴다.", "0<=x_j<=1 continuous variables.", "max value per unit capacity.", "capacity constraint remains.", "x3=8/20처럼 일부 선택이 허용되는 완화해다.", "continuous knapsack upper bound.", "Solver에서 bin 조건 대신 0<=x<=1 연속으로 둔다.", "p010 C/B 분석.", "총가치=70+20+39*(8/20).", "완화해를 원 0-1 해로 착각.", "knapsack", "branch-and-bound", "greedy fractional knapsack", "LP relaxation 계산.", ["LP_relaxation", "C/B", "ratio"], ["LP 완화문제", "효과/비용"]),
            n("capital_budgeting", "자본예산 선택", "capital budgeting selection", "예산 제약 하에서 투자 프로젝트 선택 여부를 0-1로 결정하는 모형이다.", "한정된 예산으로 어떤 프로젝트를 채택할지 고른다.", "프로젝트 채택/미채택 의사결정에 쓴다.", "x_j=프로젝트 j 선택 여부.", "max total return or NPV.", "sum required_budget_j x_j <= budget and logical constraints.", "프로젝트는 보통 절반만 채택할 수 없으므로 binary다.", "knapsack의 다중 자원 버전이다.", "Solver binary variables and budget constraints.", "p012-p015 투자 프로젝트 선택.", "0-1 변수에는 비음조건보다 binary domain이 핵심이다.", "예산 지출액을 변수로 두고 선택여부를 잊는 오류.", "knapsack_problem", "fixed_charge/logical constraints", "portfolio selection", "자본예산 정식화.", ["capital_budgeting", "project"], ["투자 프로젝트", "0-1 변수"]),
            n("fixed_charge_model", "고정비용모형", "fixed-charge model", "생산을 시작하면 고정비가 발생하고 생산량에는 변동비가 붙는 비용구조를 0-1 변수로 모델링하는 모형이다.", "공장을 조금이라도 쓰면 문을 여는 비용이 든다.", "개방 여부와 생산량을 동시에 결정할 때 쓴다.", "x_j=생산량, y_j=가동여부 binary.", "profit=max revenue-variable cost-fixed cost or min total cost.", "x_j <= capacity_j y_j.", "y=0이면 생산량이 0이 되고 y=1이면 용량까지 생산 가능하다.", "continuous flow variable linked to binary switch.", "Solver에서 생산량 변수와 binary 가동여부 변수를 함께 둔다.", "삼부 컴퓨터 고정비용 문제.", "고정비=45y1+25y2+15y3+5y4.", "IF 함수로 고정비를 직접 쓰면 비선형/불안정 모델이 될 수 있다.", "binary variable", "facility location", "big-M implication", "논리제약 x<=My.", ["fixed_charge", "고정비용"], ["고정비용모형", "Fixed-charge"]),
            n("minimum_production_logic", "최소생산량 논리제약", "minimum production logic", "공장을 열면 최소생산량 이상, 닫으면 0이 되도록 하한/상한을 binary와 연결하는 제약이다.", "가동한다면 어느 정도 규모 이상은 생산해야 한다는 조건이다.", "생산 시작 최소량이 있는 fixed-charge 문제에 쓴다.", "x_j production, y_j open binary.", "min production cost plus fixed cost.", "min_j y_j <= x_j <= capacity_j y_j.", "y=0이면 x=0, y=1이면 최소량과 용량 사이.", "binary switch controls interval.", "Solver에 두 개의 선형 제약을 추가한다.", "콘덴서 생산공장 예제.", "최소생산량*y <= 생산량 <= 용량*y.", "하한식 방향을 반대로 쓰는 오류.", "fixed_charge_model", "facility network", "semi-continuous variable", "논리식 방향.", ["minimum_production", "logic"], ["최소생산량", "생산용량"]),
            n("production_distribution_fixed_charge", "생산-분배 결합 고정비", "production-distribution fixed charge", "공장/창고 개방 여부와 생산/수송/배송량을 동시에 결정하는 혼합정수 네트워크 모형이다.", "시설을 열지 여부와 물량을 어디로 보낼지 한 번에 정한다.", "공장-창고-고객 네트워크에 고정비가 붙을 때 쓴다.", "x_ij 수송량, w_jk 배송량, y_i 공장개방, z_j 창고운영.", "min production+transportation+delivery+fixed costs.", "공장/창고 flow balance plus x<=capacity*y, w<=demand*z.", "문을 연 시설만 물량을 처리할 수 있다.", "fixed-charge network flow.", "Solver에서 array형 변경셀과 binary facility cells를 함께 둔다.", "청정식품 공장/창고 선정 문제.", "4개 공장, 3개 창고, 5개 고객 지역 구조.", "창고가 닫혀도 배송량이 양수가 되도록 식을 빠뜨리는 오류.", "fixed_charge_model", "transportation network", "facility location", "혼합정수 네트워크 식.", ["production_distribution", "facility"], ["생산-분배", "청정식품"]),
        ],
        examples=[
            ex("treasure_knapsack", "보물 0-1 배낭문제", "무게 한도 49 안에서 보물 선택가치를 최대화한다.", "x_j=보물 j 선택 여부.", "max sum value_j x_j.", "sum weight_j x_j<=49, x_j binary.", "Solver binary changing cells.", "선택은 0/1이며 LP 완화의 fractional 해와 구분한다.", ["변수 정의.", "무게 제약.", "binary 설정.", "완화해와 정수해 비교."], ["보물 선택여부", "배낭"]),
            ex("sambu_fixed_charge", "삼부 컴퓨터 fixed-charge", "공장별 가동 여부와 생산량을 정해 이익을 최대화한다.", "x_j 생산량, y_j 가동여부.", "판매수익-변동비-고정비.", "x_j<=capacity_j y_j.", "Solver mixed-integer model.", "가동하지 않는 공장은 생산량 0이어야 한다.", ["생산량/가동여부를 분리.", "고정비를 y로 곱한다.", "용량*y 논리식 추가."], ["삼부 컴퓨터", "공장가동여부"]),
            ex("clean_food_network", "청정식품 생산-분배", "공장/창고 개방과 수송/배송량을 함께 결정한다.", "x_ij, w_jk, y_i, z_j.", "min total fixed+variable network cost.", "capacity/opening constraints and warehouse balance.", "MIP with transportation arrays.", "네트워크 LP에 fixed-charge binary가 결합된 구조다.", ["시설 binary.", "수송/배송량 array.", "balance와 linking constraints."], ["청정식품", "공장/창고 선정"]),
        ],
        patterns=[
            ("선택형", "x_j가 선택 여부이면 binary로 두고 합계/예산 제약을 둔다.", "knapsack_problem", "capital_budgeting"),
            ("개방-물량 연결형", "y_j가 0이면 x_j도 0이 되도록 x_j<=M y_j를 둔다.", "fixed_charge_model", "facility_location"),
            ("네트워크 결합형", "수송량 배열과 시설개방 binary를 함께 둔다.", "production_distribution_fixed_charge", "transportation"),
        ],
        solver_rows=[
            ("변수셀", "선택 x_j, 생산량 x_j, 가동여부 y_j", "선택/가동은 bin, 생산량은 연속 또는 정수."),
            ("목표셀", "가치 최대화 또는 비용 최소화/이익 최대화", "고정비는 binary에 곱한다."),
            ("제약셀", "예산, 용량, x<=M y, balance", "논리제약 방향을 체크한다."),
            ("옵션", "정수조건 무시 해제, 정수 최적화 비율", "정확해가 필요하면 gap을 0%로 낮춘다."),
        ],
        cross_connections=[
            ("DM_PDF03 분지한계", "정수계획 모형은 branch-and-bound로 풀린다.", "IP -> B&B"),
            ("DM_PDF06 수송", "생산-분배 fixed-charge는 수송 네트워크에 binary 개방을 붙인 모델이다.", "transportation + facility binary"),
            ("DM_PDF08 set covering", "0-1 선택변수는 공공설비 입지선정으로 이어진다.", "binary selection -> set covering"),
        ],
        misconceptions=[
            ("고정비를 IF 함수로만 처리", "비선형/불안정 모델이 되고 논리 검증이 어렵다.", "binary y와 x<=M y를 쓴다.", "fixed_charge_model"),
            ("0-1 변수에 비음조건만 둠", "0<=x<=1은 연속값도 허용한다.", "bin 또는 int+<=1을 지정한다.", "pure_mixed_binary_ip"),
            ("정수 최적화 비율 무시", "Solver가 gap 허용으로 조기 종료할 수 있다.", "정확한 최적해가 필요하면 옵션 확인.", "solver_integer_tolerance"),
        ],
        routes=[
            Route("정수계획 유형부터 구분해줘", "pure_mixed_binary_ip", "integer_programming", "treasure_knapsack", "DM_PDF04:p002"),
            Route("배낭문제 식 어떻게 세워?", "knapsack_problem", "lp_relaxation_ratio", "treasure_knapsack", "DM_PDF04:p008"),
            Route("고정비는 어떻게 선형화?", "fixed_charge_model", "minimum_production_logic", "sambu_fixed_charge", "DM_PDF04:p022"),
            Route("공장/창고 개방과 배송을 같이?", "production_distribution_fixed_charge", "fixed_charge_model", "clean_food_network", "DM_PDF04:p035"),
        ],
        practice=[
            "x_j<=capacity_j y_j가 y=0, y=1에서 각각 무슨 뜻인지 설명하라.",
            "0-1 배낭의 LP 완화해가 왜 정수해가 아닐 수 있는지 말하라.",
            "정수 최적화 비율 1%와 0%의 차이를 Solver 운영 관점에서 정리하라.",
        ],
        web_refs=["WEB_OR_TOOLS_MIP", "WEB_MS_SOLVERADD", "WEB_MS_SOLVERSOLVE"],
        qc_notes=["표가 많은 페이지는 OCR 누락 가능성이 있어 계수표 원본 대조가 필요하다."],
    )


def build_dm05() -> Profile:
    return Profile(
        source_id="DM_PDF05",
        slug="ch04_simplex_duality_week2",
        title="Ch.4 심플렉스, Big-M, 쌍대성 연결",
        normalized_pdf="DM_PDF05_ch04_simplex_duality_week2.pdf",
        thesis="Big-M은 인위변수 제거를 벌점 방식으로 처리하고, 쌍대성은 원문제의 자원 제약과 쌍대문제의 가격 변수를 한 쌍으로 연결한다.",
        graph_position="two-phase/artificial variables -> Big-M tableau -> primal-dual transformation -> weak/strong duality -> complementary slackness.",
        learning_outcomes=[
            "Big-M에서 artificial variable의 벌점 부호를 목적 방향에 맞게 둔다.",
            "원본문제와 쌍대문제의 변수-제약 대응을 만든다.",
            "약쌍대성, 강쌍대성, 상보여유정리를 민감도 보고서와 연결한다.",
        ],
        nodes=[
            n("big_m_method", "Big-M 방법", "Big-M method", "인위변수에 매우 큰 벌점 M을 부여해 최적화 과정에서 artificial variable을 0으로 밀어내는 방법이다.", "임시 발판을 쓰되 최종 답에는 남지 못하도록 큰 벌금을 매긴다.", "초기 BFS가 없고 2단계법 대신 하나의 목적함수로 처리할 때 쓴다.", "원변수, surplus, artificial r.", "max 문제는 artificial에 -M, min 문제는 +M 성격의 벌점을 둔다.", "원 제약 + artificial 도입 후 정규형 tableau.", "식단처럼 >= 제약이 있는 문제에서 시작기저를 만든다.", "feasible start를 penalty objective로 찾는다.", "Solver 내부 처리와 다르지만 손계산 tableau 훈련에 유용하다.", "p003-p008 Big-M tableau.", "r1,r2가 목적행에서 소거되어야 한다.", "M 부호를 목적 방향과 반대로 넣는 오류.", "artificial variable", "duality theory", "two-phase method", "Big-M 부호와 artificial 제거.", ["big_m", "M", "artificial"], ["Big-M", "인위변수"]),
            n("artificial_variable", "인위변수", "artificial variable", "초기 기저해를 만들기 위해 원문제에 임시로 추가하는 변수다.", "계산 시작을 위한 임시 의자지만 최종 해석에는 없어야 한다.", ">= 또는 = 제약에서 slack basis가 없을 때 쓴다.", "r_i>=0 artificial variables.", "Big-M 또는 Phase I에서 0이 되도록 유도한다.", "artificial이 최종 양수면 원 제약을 만족하는 해가 없을 수 있다.", "식단 최소요구량 제약에서 도입된다.", "basis construction device.", "수동 tableau의 시작 basis.", "r1, r2 도입.", "목적행에서 인위변수 계수를 소거한다.", "인위변수를 실제 식품량/생산량처럼 해석하는 오류.", "surplus variable", "Big-M, two-phase", "dummy variable과 구분", "도입 이유와 제거 조건.", ["artificial", "인위변수"], ["artificial variable", "인위변수"]),
            n("surplus_variable", "잉여변수", "surplus variable", ">= 제약을 등식으로 바꾸기 위해 좌변에서 빼는 비음 변수다.", "최소 요구량을 얼마나 초과했는지 나타낸다.", "최소 섭취량, 최소 생산량 같은 >= 제약에 쓴다.", "s_i>=0.", "목적에는 직접 없을 수 있다.", "a x - s = b.", "요구량보다 더 섭취한 영양분 초과량이다.", "constraint transformation.", "Solver 제약식에서는 직접 만들 필요 없지만 tableau에서는 필요하다.", "식단문제 잉여변수 1개와 인위변수 2개 힌트.", "surplus는 slack과 부호가 반대다.", "<= 제약에도 surplus를 빼는 오류.", "standard form", "artificial variable", "slack variable", "부등호별 변수 도입.", ["surplus", "잉여"], ["잉여변수"]),
            n("diet_problem", "식단문제", "diet problem", "필요 영양소 최소요구량을 만족하면서 식품 비용을 최소화하는 LP다.", "영양 기준을 넘기되 가장 싼 조합을 찾는다.", "min LP, duality, Big-M 예제로 쓴다.", "x_i=식품 i 포함량.", "min sum cost_i x_i.", "vitamin A/C intake >= requirement.", "식품량은 100g 단위 등으로 해석된다.", ">= halfspaces and cost iso-lines.", "Solver 변수셀 식품량, 목표셀 비용, 제약셀 영양섭취량>=요구량.", "박씨의 식단 문제.", "x4=1.8, x5=1.4 등 최적 식품량/잠재가격 연결.", "최소요구량을 <=로 쓰는 오류.", "min LP", "dual vitamin pill problem", "Stigler diet", "식단 모형화.", ["diet", "식단"], ["식단 문제", "비타민"]),
            n("dual_problem", "쌍대문제", "dual problem", "원본문제의 제약을 변수로, 변수를 제약으로 바꿔 만든 짝 문제다.", "자원을 직접 배분하는 문제와 그 자원의 가격을 매기는 문제를 동시에 본다.", "LP 해석, 민감도, shadow price를 이해할 때 쓴다.", "primal x, dual y.", "max primal이면 dual은 min 형태가 되는 기본 대응이 많다.", "A, b, c의 행/열 관계가 뒤집힌다.", "식단문제의 dual은 비타민 알약 가격 결정 문제로 해석된다.", "constraint-variable transpose relation.", "Solver 민감도 보고서의 shadow price와 연결된다.", "p018 쌍대문제 수학적모형.", "dual objective 50y1+60y2 등.", "부등호 방향과 변수 부호 제한을 빠뜨리는 오류.", "primal LP", "weak/strong duality", "sensitivity report", "쌍대문제 만들기.", ["dual", "쌍대"], ["쌍대문제", "dual"]),
            n("primal_dual_mapping", "원문제-쌍대 대응", "primal-dual mapping", "원문제의 각 제약은 쌍대변수 하나에, 원문제의 각 변수는 쌍대제약 하나에 대응한다.", "행과 열을 바꾸면서 자원량과 단위이익의 역할이 바뀐다.", "쌍대문제를 구성할 때 쓴다.", "A matrix rows/columns.", "primal c becomes dual RHS, primal b becomes dual objective coefficient.", "부등호 방향에 따라 dual variable sign/domain이 달라진다.", "비타민 요구량은 알약 가격 변수와 연결된다.", "matrix transpose graph.", "민감도 보고서의 Constraints/Variable Cells 섹션 대응.", "p020-p021 관계 표.", "max/min 관계 없이 기본형/역방향/무방향을 구분한다.", "행/열 개수를 반대로 세는 오류.", "dual_problem", "complementary_slackness", "matrix transpose", "변수-제약 개수 대응.", ["primal_dual", "mapping"], ["원본문제와 쌍대문제의 관계"]),
            n("weak_duality", "약쌍대성", "weak duality", "최대화 원문제의 임의 가능해 목적값은 최소화 쌍대문제의 임의 가능해 목적값보다 작거나 같다.", "생산으로 얻을 수 있는 가치는 자원 가격으로 평가한 상한을 넘을 수 없다.", "최적성 상한/하한 논리에 쓴다.", "primal feasible x, dual feasible y.", "max z(x) <= min w(y).", "feasible pair condition.", "어떤 식단 비용도 유효한 영양소 가격 상한과 비교된다.", "dual bounds.", "Solver sensitivity와 bound 해석에 연결된다.", "p024 약쌍대성.", "가능해에서 max<=min.", "최적해에서만 성립한다고 착각하는 오류.", "dual feasibility", "strong duality", "branch-and-bound bounds", "부등식 방향.", ["weak_duality", "약쌍대"], ["약쌍대성"]),
            n("strong_duality", "강쌍대성", "strong duality", "원문제와 쌍대문제가 모두 가능해를 가지면 두 문제의 최적 목적값은 같다.", "자원 배분의 최적 가치와 자원 가격 평가의 최적 가치가 최종적으로 만난다.", "LP 최적성과 dual solution 해석에 쓴다.", "optimal primal x*, dual y*.", "z*=w*.", "both feasible and bounded in corresponding case.", "식단문제 최적비용과 비타민 알약 가격문제 최적수입이 같다.", "primal-dual optimal pair.", "Solver shadow price as optimal dual variable.", "p024 강쌍대성.", "최적해에서 max=min.", "infeasible/unbounded cases에서도 무조건 같다고 하는 오류.", "weak_duality", "complementary_slackness", "KKT for LP", "최적값 같음의 조건.", ["strong_duality", "강쌍대"], ["강쌍대성"]),
            n("four_duality_cases", "쌍대성 4가지 경우", "four primal-dual cases", "원문제와 쌍대문제의 optimal/unbounded/infeasible 상태가 서로 제약되는 네 가지 관계다.", "한쪽이 무한히 좋아지면 다른 쪽은 가능하지 않을 수 있다.", "LP 상태 진단에 쓴다.", "problem status pair.", "bounded optimal, unbounded, infeasible combinations.", "duality theorem constraints.", "max unbounded이면 dual min infeasible 같은 관계.", "status duality.", "Solver status 해석.", "p025 네 가지 case.", "최적/비유계/비가해 관계.", "한쪽 infeasible이면 다른 쪽이 반드시 unbounded라고 단정하는 오류.", "weak/strong duality", "solver status", "unbounded/infeasible", "상태 관계.", ["duality_cases", "status"], ["4 Cases", "unbounded", "infeasible"]),
            n("complementary_slackness", "상보여유정리", "complementary slackness", "원문제 제약의 여유와 해당 쌍대변수, 쌍대 제약의 여유와 해당 원변수 중 하나는 반드시 0이어야 하는 최적성 조건이다.", "자원이 남으면 그 자원의 가격은 0이고, 가격이 양수면 자원은 완전히 쓰인다.", "primal-dual 최적성 검증과 민감도 해석에 쓴다.", "slack_i, y_i, dual_slack_j, x_j.", "slack_i*y_i=0, dual_slack_j*x_j=0.", "both primal and dual feasible.", "기계시간이 남으면 잠재가격 0이라는 해석과 연결된다.", "orthogonality between slack and price.", "Solver의 slack/shadow price/reduced cost 관계.", "p027-p031 상보여유 확인.", "쌍대문제 제약여유=-한계비용.", "여유가 있으면 변수도 0이라고 반대로 말하는 오류.", "strong_duality", "reduced cost/shadow price", "KKT complementarity", "여유와 가격의 곱=0.", ["complementary_slackness", "상보여유"], ["상보여유정리"]),
            n("shadow_price_dual_solution", "잠재가격과 쌍대해", "shadow price as dual solution", "민감도 보고서의 잠재가격은 제약에 대응하는 쌍대변수의 최적값으로 해석된다.", "자원의 시장가치가 dual variable로 드러난다.", "sensitivity와 duality를 연결할 때 쓴다.", "dual y_i values.", "dual objective equals primal optimum.", "binding constraints may have nonzero y_i.", "식단문제의 비타민 알약 가격이 원문제 잠재가격과 연결된다.", "dual optimal vector.", "Solver Constraints 섹션의 Shadow Price.", "p017, p030.", "비타민 알약 가격(최적해)=식단문제 잠재가격.", "잠재가격을 원변수 값과 혼동.", "dual_problem", "sensitivity_analysis", "resource valuation", "민감도-쌍대 연결.", ["shadow_price", "dual_solution"], ["잠재가격", "쌍대문제 최적해"]),
        ],
        examples=[
            ex("big_m_diet", "식단문제 Big-M", ">= 영양 제약 때문에 surplus와 artificial을 도입해 Big-M tableau로 푼다.", "식품량 x_i, surplus, artificial r.", "min cost 또는 max 변환 목적.", "영양섭취량>=요구량.", "Big-M tableau.", "artificial이 최종 0이어야 원문제 feasible 해다.", ["부등호를 등식화.", "artificial 도입.", "M 벌점 목적행 구성.", "피벗으로 artificial 제거."], ["Big-M method", "식단문제"]),
            ex("diet_dual", "식단문제 쌍대", "식단 최소비용 문제의 쌍대를 비타민 알약 가격 최대화 문제로 해석한다.", "dual y1,y2 vitamin prices.", "max 50y1+60y2.", "각 식품 가격을 넘지 않는 영양소 가격 조합.", "Solver sensitivity/dual model.", "dual optimal prices equal primal shadow prices.", ["원 제약을 dual 변수로.", "원 변수별 dual 제약 생성.", "최적값 같음 확인."], ["쌍대문제", "비타민 알약 가격"]),
            ex("complementary_slackness_check", "상보여유 확인", "원 제약 여유와 쌍대변수, 쌍대 제약 여유와 원변수의 곱이 0인지 확인한다.", "slacks, y_i, x_j.", "optimality condition not separate objective.", "primal/dual feasibility.", "Sensitivity report plus dual solution.", "남는 자원은 가격 0, 생산되는 변수는 reduced cost 0이다.", ["원 제약 slack 확인.", "dual y 확인.", "쌍대 slack과 x 확인."], ["상보여유정리", "잠재가격"]),
        ],
        patterns=[
            ("인위변수 처리", "artificial을 Big-M 벌점 또는 Phase I으로 제거한다.", "big_m_method", "two_phase"),
            ("원-쌍대 변환", "제약과 변수를 전치해 가격 문제를 만든다.", "dual_problem", "sensitivity"),
            ("최적성 검증", "강쌍대성과 상보여유로 primal/dual 최적성을 확인한다.", "complementary_slackness", "KKT"),
        ],
        solver_rows=[
            ("변수셀", "primal x 또는 dual y", "dual을 만들 때 변수/제약 개수가 뒤집힌다."),
            ("목표셀", "primal min/max와 dual max/min", "강쌍대성 조건에서 최적값이 같다."),
            ("제약셀", "영양 요구량, 알약가격 상한, slack/surplus", "부등호 방향과 변수 부호 제한을 보존한다."),
            ("보고서", "Shadow Price, Reduced Cost", "상보여유와 dual solution으로 해석한다."),
        ],
        cross_connections=[
            ("DM_PDF01 2단계법", "Big-M과 two-phase는 artificial 처리 방식이 다르다.", "artificial handling"),
            ("DM_PDF02 민감도", "shadow price/reduced cost는 duality의 계산 결과다.", "duality -> sensitivity"),
            ("DM_PDF06 네트워크", "max-flow min-cut 같은 네트워크 쌍대성이 후속 연결축이다.", "duality -> network theorem"),
        ],
        misconceptions=[
            ("M 부호 오류", "artificial을 보상하면 최종해에 남을 수 있다.", "max/min 방향별 penalty 부호 확인.", "big_m_method"),
            ("쌍대 변수 개수 오류", "원 제약 수가 쌍대 변수 수다.", "행/열 대응표를 먼저 만든다.", "primal_dual_mapping"),
            ("상보여유 역해석", "slack이 있으면 dual variable이 0이지, 모든 관련 변수가 0은 아니다.", "곱 조건을 정확히 쓴다.", "complementary_slackness"),
        ],
        routes=[
            Route("Big-M은 왜 M을 붙여?", "big_m_method", "artificial_variable", "big_m_diet", "DM_PDF05:p003"),
            Route("쌍대문제 어떻게 만들지?", "dual_problem", "primal_dual_mapping", "diet_dual", "DM_PDF05:p018"),
            Route("shadow price가 쌍대해라는 뜻?", "shadow_price_dual_solution", "dual_problem", "diet_dual", "DM_PDF05:p017"),
            Route("상보여유로 최적성 확인?", "complementary_slackness", "strong_duality", "complementary_slackness_check", "DM_PDF05:p027"),
        ],
        practice=[
            ">= 제약 하나를 surplus/artificial 포함 등식으로 바꿔라.",
            "원문제 제약 3개, 변수 5개이면 쌍대 변수/제약 개수를 말하라.",
            "slack=40인 제약의 shadow price가 왜 0이어야 하는지 설명하라.",
        ],
        web_refs=["WEB_OR_TOOLS_LP", "WEB_MS_SOLVERADD", "WEB_MS_SOLVERSOLVE"],
    )


def build_dm06() -> Profile:
    return Profile(
        source_id="DM_PDF06",
        slug="ch05_transportation_network_week1",
        title="Ch.5 수송계획과 네트워크 분석",
        normalized_pdf="DM_PDF06_ch05_transportation_network_week1.pdf",
        thesis="이 장은 LP를 네트워크 구조로 재해석한다. 수송문제, 경유수송, 할당, 최소비용흐름은 모두 flow balance와 arc cost/capacity를 공유하는 같은 계열의 모델이다.",
        graph_position="LP formulation -> transportation matrix -> transshipment node balance -> assignment special case -> min-cost/max-flow/shortest path -> CPM/PERT.",
        learning_outcomes=[
            "수송문제, 불균형 수송, 할당, 경유수송, 최소비용흐름을 하나의 네트워크 계열로 설명한다.",
            "수식, 그래프, Solver 행렬/SUMPRODUCT/SUMIF 관점을 서로 번역한다.",
            "질문 유형별로 노드와 evidence anchor를 바로 라우팅한다.",
        ],
        nodes=[
            n("transportation_problem", "수송문제", "transportation problem", "여러 공급지에서 여러 수요지로 얼마를 보낼지 결정해 총 수송비용을 최소화하는 LP 특수형이다.", "공급은 넘치지 않게, 수요는 채우면서 가장 싼 출발지-도착지 조합을 찾는다.", "다수 공급지와 다수 수요지가 있고 경유지와 arc capacity가 없을 때 쓴다.", "x_ij=공급지 i에서 수요지 j로 보내는 수송량.", "min sum_i sum_j c_ij x_ij.", "sum_j x_ij <= S_i, sum_i x_ij >= D_j, x_ij>=0. 균형이면 등식으로 읽을 수 있다.", "어느 PDC에서 어느 딜러로 몇 개를 보낼지 정하는 것이다.", "공급노드와 수요노드를 잇는 bipartite network다.", "3x3 changing cells, 행합=공급량, 열합=수요량, SUMPRODUCT(비용행렬, 수송량행렬).", "Toyota PDC 분배 문제.", "시카고/멤피스/찰스톤 공급과 루이스빌/내시빌/헌쓰빌 수요 6,650의 균형.", "행합과 열합 방향을 뒤집거나 수요 제약을 <=로 두는 오류.", "LP formulation, 공급/수요 RHS", "balanced/unbalanced transportation, min-cost flow", "assignment problem, transportation-like blending", "변수 x_ij와 행/열 제약 세우기.", ["transportation", "수송문제", "SUMPRODUCT"], ["수송문제 Transportation", "어느 공급지"]),
            n("balanced_transportation", "균형 수송문제", "balanced transportation", "총공급량과 총수요량이 같아 모든 공급과 수요를 등식으로 맞추는 수송문제다.", "들어온 총량과 나가는 총량이 정확히 맞아 가상의 노드가 필요 없다.", "supply sum=demand sum일 때 기본형으로 쓴다.", "same x_ij matrix.", "min total transportation cost.", "row sums=S_i and column sums=D_j.", "Toyota 예제에서 공급량합과 수요량합이 모두 6,650이다.", "complete bipartite network with balanced net supply.", "행합/열합이 각각 RHS와 정확히 같게 설정 가능하다.", "Toyota PDC 표.", "총수요 2,450+2,000+2,200=6,650.", "균형인데도 dummy를 추가하거나 부등호를 과도하게 쓰는 오류.", "transportation_problem", "transportation_integrality", "balanced min-cost flow", "균형 여부 판정.", ["balanced", "균형"], ["균형", "수요량합"]),
            n("unbalanced_transportation", "불균형 수송문제", "unbalanced transportation", "총공급량과 총수요량이 달라 제약 방향 조정 또는 dummy supply/demand가 필요한 수송문제다.", "재고가 남거나 수요가 부족하면 현실적으로 남김/부족을 표현해야 한다.", "supply sum != demand sum일 때 쓴다.", "x_ij plus optional dummy row/column.", "min total cost with penalty/dummy costs.", "공급초과: 공급 <=, 수요 >= 또는 =. 공급부족: 가상공급지 추가.", "공급량합 6,000, 수요량합 6,650이면 가상 공급지 650이 필요하다.", "unbalanced net supply network.", "dummy row/column and large costs, Solver constraints adjusted.", "불균형 수송문제 슬라이드.", "가상공급지 공급량=수요합-공급합.", "공급부족을 그냥 infeasible로 끝내거나 dummy 비용을 0으로 두는 오류.", "balanced_transportation", "dummy_supply_or_demand", "minimum_cost_flow imbalance", "불균형 처리 방향.", ["unbalanced", "불균형", "dummy"], ["불균형 수송문제", "가상의 공급지"]),
            n("dummy_supply_or_demand", "가상 공급지/수요지", "dummy supply or demand", "불균형 수송문제를 균형형처럼 풀기 위해 추가하는 가상의 공급 또는 수요 노드다.", "부족분이나 남는 양의 회계 처리 칸이다.", "공급부족 또는 공급초과를 균형화할 때 쓴다.", "dummy row/column variables.", "dummy arc cost는 의미에 따라 0 또는 큰 벌점이 될 수 있다.", "dummy 공급량/수요량은 차이분으로 둔다.", "공급부족 때 가상공급지 비용을 매우 큰 수로 두면 미충족 수요를 벌점 처리한다.", "artificial network node.", "Solver에서 새 행/열을 추가한다.", "p008 가상공급지 650.", "dummy supply=650.", "dummy를 실제 공급지처럼 해석하는 오류.", "unbalanced_transportation", "penalty modeling", "artificial variable but model-level", "dummy 비용 설정.", ["dummy", "가상공급지"], ["가상공급지", "큰비용"]),
            n("transportation_integrality", "수송문제 정수해 성질", "transportation integrality property", "공급량과 수요량이 정수이면 int 조건을 걸지 않아도 수송문제 최적해가 정수로 보장되는 성질이다.", "네트워크 행렬 구조 자체가 정수해를 끌어내는 특수한 경우다.", "수송/할당/최소비용흐름에서 정수조건 필요 여부를 판단할 때 쓴다.", "continuous x_ij with integer S_i, D_j.", "same min cost objective.", "transportation constraints only, no extra arbitrary side constraints.", "부품 개수처럼 정수 단위인데도 Solver에 int 조건을 안 걸어도 된다.", "network incidence/transportation matrix integrality.", "Simplex LP로 풀어도 정수해가 나온다.", "p010-p011 정수해 보장.", "할당문제 0/1 해 보장의 근거.", "추가 제약이 들어와도 항상 정수해라고 과잉 일반화하는 오류.", "balanced_transportation", "assignment_problem, min-cost integrality", "total unimodularity intuition", "int 조건 필요 여부.", ["integrality", "정수해"], ["정수이면", "int", "정수해"]),
            n("transportation_solver_model", "Solver 수송모형", "transportation Solver model", "수송량 행렬을 변경셀로 두고 SUMPRODUCT 목적셀과 행합/열합 제약으로 만든 Excel Solver 모형이다.", "수식 LP를 스프레드시트의 행렬 계산으로 바꾼 것이다.", "수송문제를 실제 Excel로 풀 때 쓴다.", "3x3 array changing cells.", "SUMPRODUCT(cost matrix, shipment matrix).", "row sums <= supply, column sums >= demand, changing cells>=0.", "각 화살표 수송량이 변경셀이다.", "bipartite arcs become matrix cells.", "Solver Simplex LP, nonnegative option, no int needed in basic transportation.", "p005-p007 모델링 가이드.", "행합은 공급한 양, 열합은 공급받는 양.", "비용행렬과 수송량행렬 차원을 다르게 잡는 오류.", "transportation_problem", "transportation_sensitivity", "spreadsheet LP pattern", "Solver 셀 구조 설명.", ["solver", "SUMPRODUCT", "changing_cells"], ["변경셀", "3 x 3", "행을 따라"]),
            n("transportation_sensitivity", "수송문제 민감도", "transportation sensitivity", "수송비용 또는 공급가능량 변화가 총비용과 최적 배정에 미치는 영향을 reduced cost/shadow price로 해석한다.", "왜 싼 경로가 항상 쓰이지 않는지, 어느 PDC 공급을 늘리면 유리한지 묻는다.", "최적 운송계획 이후 비용/공급 변화 질문에 쓴다.", "shipment variables and route costs/supply RHS.", "cost coefficient changes and RHS changes.", "allowable ranges and shadow prices if available.", "찰스톤-내시빌에 100 배정하면 비용 50씩 증가할 수 있다.", "route arcs have reduced costs; supply nodes have shadow values.", "Solver sensitivity report.", "p012-p014 민감도 보고서.", "멤피스 공급 100 증가 시 비용 10,000 감소 사례.", "거리/비용이 작다고 항상 배정된다고 생각하는 오류.", "transportation_solver_model", "DM_PDF02 sensitivity", "network reduced cost", "수송 민감도 해석.", ["transportation_sensitivity", "reduced_cost", "shadow_price"], ["민감도 보고서", "찰스톤"]),
            n("assignment_problem", "할당문제", "assignment problem", "공급량과 수요량이 모두 1인 특별한 수송문제로, 자원과 작업을 1:1로 배정한다.", "각 기계는 한 작업만, 각 작업도 한 기계에만 배정되는 matching이다.", "작업-기계, 작업자-작업, 팀 편성에 쓴다.", "x_ij=기계 i가 작업 j를 맡으면 1, 아니면 0.", "min total setup time or max total utility.", "row sums=1, column sums=1, x_ij>=0; 수송 정수해 성질로 0/1 보장.", "준비시간을 최소화하는 기계-작업 배정.", "complete bipartite matching network.", "binary처럼 해석하지만 강의는 수송문제 정수해 성질로 LP 해도 정수 보장.", "기계의 준비시간 줄이기.", "4개 기계와 4개 작업, 공급량/수요량 모두 1.", "할당을 일반 수송처럼 해도 되지만 의미상 0/1 해석을 잊는 오류.", "transportation_integrality", "set partitioning, TSP", "matching", "0/1 보장 이유.", ["assignment", "할당", "matching"], ["할당문제", "공급량=1"]),
            n("transshipment_problem", "경유수송문제", "transshipment problem", "공급지와 수요지 사이에 경유지가 있어 유입과 유출 균형을 함께 만족시키는 네트워크 수송문제다.", "물건이 물류창고를 거쳐 갈 수 있으므로 창고 장부가 맞아야 한다.", "중간 창고/허브가 있는 물류 문제에 쓴다.", "x_ij=지역 i에서 j로 보내는 양.", "min total shipping cost.", "공급지/수요지 조건 + 경유지 유입=유출.", "창고는 공급지이면서 동시에 수요지로 모형화된다.", "directed network with intermediate nodes.", "arc flow variables, node balance constraints.", "농산물 유통 경유수송문제.", "공장 3곳, 창고 2곳, 도시 2곳.", "경유지를 단순 공급지 또는 수요지 중 하나로만 두는 오류.", "transportation_problem", "minimum_cost_flow", "node balance", "경유지 처리.", ["transshipment", "경유수송"], ["경유수송문제", "경유지"]),
            n("transshipment_balance", "경유지 유입=유출", "transshipment balance", "경유지에서 공급한 양과 공급받은 양이 같아야 한다는 흐름보존 제약이다.", "창고가 물건을 만들어내거나 소비하지 않는다는 장부 원칙이다.", "transshipment node를 모델링할 때 핵심으로 쓴다.", "inflow and outflow sums at warehouse nodes.", "objective는 arc cost 합계.", "outflow_k = inflow_k for pure transshipment nodes.", "창고4, 창고5가 공급지와 수요지 목록에 동시에 들어간다.", "flow conservation at intermediate nodes.", "Solver에서 노드별 balance row를 만든다.", "p019 모델링 가이드.", "공급한 양=공급 받은 양.", "경유지에 별도 공급량을 임의로 주는 오류.", "transshipment_problem", "minimum_cost_flow node balance", "inventory conservation", "유입/유출 식 작성.", ["balance", "flow_conservation", "경유지"], ["공급한 량", "공급 받은 량"]),
            n("minimum_cost_flow", "최소비용흐름", "minimum cost flow", "아크별 비용과 용량, 노드별 공급/수요를 가진 네트워크에서 총 흐름비용을 최소화하는 일반 모형이다.", "수송과 경유수송을 더 일반적인 directed arc table로 표현한 모델이다.", "복잡한 네트워크에 비용과 용량이 모두 있을 때 쓴다.", "x_ij=arc i->j flow.", "min sum c_ij x_ij.", "x_ij<=u_ij and net outflow_i=required_i.", "레미콘 공장에서 공사장까지 비용 최소 흐름경로와 흐름량을 정한다.", "directed graph with capacities and node supplies/demands.", "arc table: start node, end node, cost, capacity, flow; node balance via SUMIF.", "레미콘 믹서 흐름배치.", "노드 3 공급 150, 노드1/6 수요 같은 required net-flow.", "수송문제보다 단순하다고 보는 오류. 오히려 수송/경유수송의 일반화다.", "transshipment_balance", "maximum_flow, shortest_path", "network simplex", "아크/노드 제약 구분.", ["min_cost_flow", "minimum_cost", "flow"], ["최소비용 흐름", "minimum cost"]),
            n("maximum_flow", "최대흐름", "maximum flow", "원천지에서 목적지까지 arc capacity를 넘지 않으면서 보낼 수 있는 총 흐름량을 최대화하는 네트워크 문제다.", "가장 좁은 병목을 고려해 네트워크가 얼마나 많이 흘릴 수 있는지 본다.", "비용보다 용량과 throughput이 중심일 때 쓴다.", "x_ij arc flow and total source outflow.", "max total flow from source to sink.", "arc capacity and intermediate flow conservation.", "한 원천지에서 한 목적지까지 최대 운송량을 찾는다.", "source-sink directed network.", "Solver에서는 arc flow cells and capacity constraints.", "p022 최대흐름 정의.", "아크 용량이 주어진 정보다.", "최대흐름에 비용 최소 목적을 섞어 변수 정의가 흔들리는 오류.", "minimum_cost_flow", "max-flow min-cut duality", "capacity bottleneck", "최대흐름과 최소비용흐름 차이.", ["max_flow", "maximum"], ["최대흐름"]),
            n("shortest_path", "최단경로", "shortest path", "출발지에서 목적지까지 거리나 비용이 가장 작은 경로를 찾는 네트워크 문제다.", "흐름량보다 어떤 길을 선택할지가 핵심이다.", "단일 출발-도착 경로 선택에 쓴다.", "x_ij path arc selection or unit flow.", "min sum distance_ij x_ij.", "unit supply at source, unit demand at sink, flow conservation.", "출발지 의무유출량=1, 목적지=-1인 min-cost flow 특수형으로 볼 수 있다.", "unit-flow network path.", "Solver에서는 0/1처럼 해석될 수 있으나 min-cost flow integrality로 경로가 나온다.", "p022, p033 최단경로 응용.", "정수 capacity/required net-flow면 정수 흐름이 보장된다.", "최단경로를 모든 수요를 보내는 수송문제로 혼동하는 오류.", "minimum_cost_flow", "CPM/PERT", "unit min-cost flow", "경로 vs 흐름 구분.", ["shortest_path", "최단경로"], ["최단경로", "출발지 의무유출량"]),
            n("network_topology_table", "네트워크 토폴로지 표", "network topology table", "아크를 시작노드, 종료노드, 단위흐름비용, 흐름용량 열로 표현하는 Solver 친화적 표 구조다.", "그림 네트워크를 행 데이터베이스로 바꾸는 방법이다.", "큰 네트워크를 스프레드시트로 풀 때 쓴다.", "one row per arc.", "total cost uses flow*unit cost over arc rows.", "capacity row constraints and node balance from arc table.", "아크별 입력자료를 표로 만들면 SUMIF 계산이 가능해진다.", "edge list representation.", "start/end/cost/capacity/flow columns.", "p029 표현법.", "1 2 5 20 같은 행이 arc 1->2의 비용/용량이다.", "그림만 보고 노드 balance를 수작업으로 흩어 쓰는 오류.", "minimum_cost_flow", "sumif_node_balance", "edge list graph", "arc table 만들기.", ["topology", "arc_table", "edge_list"], ["시작노드 종료노드 단위흐름 비용 흐름용량", "네트워크 토폴로지", "아크별 시작노드 종료노드"]),
            n("sumif_node_balance", "SUMIF 순수유출량", "SUMIF node balance", "시작노드가 해당 노드인 흐름 합에서 종료노드가 해당 노드인 흐름 합을 빼 순수유출량을 계산하는 스프레드시트 패턴이다.", "노드별 장부를 조건부 합계 두 번으로 자동 계산한다.", "큰 네트워크에서 node balance를 효율적으로 만들 때 쓴다.", "flow column and start/end node columns.", "objective는 별도 SUMPRODUCT 또는 흐름*비용 합.", "SUMIF(start,node,flow)-SUMIF(end,node,flow)=required net-flow.", "노드3의 X34-X13-X23=-5 같은 식을 자동화한다.", "incidence matrix row computation.", "Excel SUMIF(range, criteria, sum_range).", "p030-p032 SUMIF 설명.", "노드3 순수유출량 식.", "시작/종료 SUMIF 순서를 반대로 해 부호를 뒤집는 오류.", "network_topology_table", "minimum_cost_flow", "incidence matrix", "SUMIF 식 작성.", ["SUMIF", "node_balance", "순수유출량"], ["SUMIF 시작 노드 종료 노드", "SUMIF 시작노드 종료노드 흐름량", "SUMIF 영역A 셀B 영역C"]),
            n("cpm_pert", "CPM/PERT 프로젝트 네트워크", "CPM/PERT", "프로젝트 활동의 선후관계와 기간을 네트워크로 표현해 critical path와 일정 위험을 분석하는 후속 네트워크 분석 주제다.", "물류 흐름이 아니라 시간이 흐르는 네트워크다.", "프로젝트 관리 네트워크로 확장할 때 쓴다.", "activity durations and precedence arcs.", "minimize/compute project completion time, identify critical path.", "precedence constraints.", "5장 목차의 후속 네트워크 분석이다.", "directed acyclic project graph.", "Solver보다는 네트워크 일정표/forward-backward pass가 중심이다.", "p001 CPM/PERT 목차.", "critical path method와 PERT 명시.", "수송 flow와 같은 물량 보존식으로 풀려는 오류.", "shortest_path/longest path", "project scheduling", "DAG path analysis", "CPM/PERT 위치.", ["CPM", "PERT", "project"], ["CPM/PERT", "Critical path"]),
        ],
        examples=[
            ex("toyota_distribution", "Toyota PDC 분배 문제", "시카고, 멤피스, 찰스톤 PDC에서 루이스빌, 내시빌, 헌쓰빌 딜러 수요를 최소거리로 충족한다.", "x_ij=PDC i에서 딜러 j로 보내는 부품 수.", "min sum distance_ij x_ij.", "PDC별 공급량, 딜러별 수요량, x_ij>=0.", "3x3 changing cells, SUMPRODUCT, row sums, column sums, Simplex LP.", "균형 수송문제이며 총공급=총수요=6,650이다.", ["공급/수요 표를 읽는다.", "x_ij 행렬을 둔다.", "행합과 열합을 제약으로 둔다.", "총비용/거리 SUMPRODUCT를 최소화한다."], ["도요타 USA", "PDC", "6,650"]),
            ex("unbalanced_transportation", "불균형 수송 보정", "공급량합과 수요량합이 다를 때 제약 방향 또는 dummy node로 모델을 보정한다.", "x_ij plus dummy row/column.", "min cost with penalty.", "공급초과/공급부족에 따라 <=, >=, dummy supply/demand.", "새 행/열과 큰 비용 또는 잔여 비용을 추가한다.", "공급부족이면 가상공급지 650처럼 부족분을 표시한다.", ["총공급과 총수요 비교.", "초과/부족 판정.", "dummy 추가 또는 부등호 방향 조정.", "벌점 비용 의미 해석."], ["불균형 수송문제", "가상공급지"]),
            ex("machine_assignment", "기계 준비시간 할당", "4개 기계와 4개 작업을 1:1로 배정해 총 준비시간을 최소화한다.", "x_ij=기계 i가 작업 j를 수행하면 1.", "min sum setup_ij x_ij.", "각 기계 행합=1, 각 작업 열합=1.", "수송문제처럼 풀되 정수해 성질로 0/1 보장.", "수송문제의 특수형이므로 별도 int 없이 0/1 해가 나온다.", ["기계와 작업을 공급/수요로 본다.", "공급량/수요량을 모두 1로 둔다.", "준비시간 행렬을 비용행렬로 둔다."], ["기계의 준비시간", "수송문제로 모형화"]),
            ex("transshipment_min_cost", "농산물 경유수송/최소비용흐름", "공장-창고-도시 네트워크에서 창고의 유입=유출을 만족하며 비용을 최소화한다.", "x_ij=arc shipment/flow.", "min total arc cost.", "창고 balance, 공급/수요, arc availability.", "arc variables and node balance rows; larger networks use SUMIF.", "창고는 공급지이면서 수요지인 경유지다.", ["경유지를 식별한다.", "창고를 공급/수요 목록에 동시에 넣는다.", "유입=유출 제약을 둔다.", "최소비용흐름으로 일반화한다."], ["농산물 유통", "경유지"]),
            ex("ready_mix_flow", "레미콘 최소비용흐름", "레미콘 공장과 공사장을 연결하는 네트워크에서 흐름비용 합을 최소화한다.", "x_ij=아크 i->j 흐름량.", "min sum c_ij x_ij.", "x_ij<=u_ij, net outflow=required net-flow.", "topology table, SUMIF node balance, total cost cell.", "수송문제보다 일반적인 arc-capacity 네트워크다.", ["아크표 작성.", "흐름량 변경셀.", "용량 제약.", "SUMIF로 노드 balance 계산."], ["레미콘", "흐름배치"]),
        ],
        patterns=[
            ("수송행렬형", "공급지-수요지 행렬, 행합/열합, SUMPRODUCT.", "transportation_solver_model", "assignment_problem"),
            ("경유노드형", "경유지는 유입=유출 balance를 갖는다.", "transshipment_balance", "minimum_cost_flow"),
            ("아크표형", "시작노드/종료노드/비용/용량/흐름량 edge list로 네트워크를 표현한다.", "network_topology_table", "sumif_node_balance"),
            ("정수성형", "수송/할당/min-cost flow는 정수 입력에서 LP 해가 정수로 나오는 특수 구조를 갖는다.", "transportation_integrality", "assignment_problem"),
        ],
        solver_rows=[
            ("수송 결정변수", "3x3 수송량 행렬, 예: 각 PDC-딜러 arc", "변경셀은 수송량이고 반드시 비용행렬과 같은 크기여야 한다."),
            ("수송 목적셀", "SUMPRODUCT(비용행렬, 수송량행렬)", "총 거리/총비용을 최소화한다."),
            ("수송 제약셀", "행합 <= 또는 = 공급량, 열합 >= 또는 = 수요량", "균형이면 등식으로 해석하고 불균형이면 방향을 점검한다."),
            ("min-cost flow 변수", "아크별 흐름량 열", "각 row가 하나의 arc다."),
            ("min-cost flow balance", "SUMIF(시작노드,node,흐름)-SUMIF(종료노드,node,흐름)", "노드별 순수유출량=의무유출량."),
            ("해법", "Simplex LP", "정수 공급/수요/용량이면 일반적으로 int 조건 없이 정수흐름 성질을 활용한다."),
        ],
        cross_connections=[
            ("DM_PDF02 민감도", "수송비 reduced cost와 공급량 shadow price가 수송 민감도 질문을 설명한다.", "sensitivity -> transportation"),
            ("DM_PDF04 fixed-charge", "수송 네트워크에 시설개방 0-1 변수를 붙이면 생산-분배 fixed-charge가 된다.", "transportation -> MIP"),
            ("DM_PDF05 duality", "network flow에는 max-flow/min-cut 등 쌍대적 해석이 뒤따른다.", "duality -> network"),
        ],
        misconceptions=[
            ("싸면 무조건 배정", "네트워크 전체 제약 때문에 싼 arc가 안 쓰일 수 있다.", "reduced cost와 전체 balance로 해석.", "transportation_sensitivity"),
            ("경유지를 공급지로만 처리", "창고 유입=유출이 빠져 물량이 생기거나 사라진다.", "경유지를 공급지/수요지 양쪽에 둔다.", "transshipment_balance"),
            ("SUMIF 부호 반대", "순수유출량 부호가 뒤집혀 공급/수요 해석이 바뀐다.", "시작노드 합 - 종료노드 합 순서를 유지.", "sumif_node_balance"),
            ("할당문제에 정수조건 필수라고 단정", "수송문제 정수해 성질로 0/1 해가 보장된다.", "단, 추가 제약이 있으면 별도 점검.", "transportation_integrality"),
        ],
        routes=[
            Route("수송문제 식 어떻게 세워?", "transportation_problem", "transportation_solver_model", "toyota_distribution", "DM_PDF06:p004-p010"),
            Route("공급이 수요보다 적으면?", "unbalanced_transportation", "dummy_supply_or_demand", "unbalanced_transportation", "DM_PDF06:p008"),
            Route("할당문제는 왜 0/1이야?", "assignment_problem", "transportation_integrality", "machine_assignment", "DM_PDF06:p015-p016"),
            Route("경유지는 공급지야 수요지야?", "transshipment_problem", "transshipment_balance", "transshipment_min_cost", "DM_PDF06:p018-p019"),
            Route("최소비용흐름과 수송문제 차이?", "minimum_cost_flow", "transportation_problem, transshipment_problem", "ready_mix_flow", "DM_PDF06:p022-p029"),
            Route("SUMIF 왜 써?", "sumif_node_balance", "network_topology_table", "ready_mix_flow", "DM_PDF06:p030-p032"),
            Route("민감도 보고서 어떻게 읽어?", "transportation_sensitivity", "transportation_solver_model", "toyota_distribution", "DM_PDF06:p012-p014"),
        ],
        practice=[
            "Toyota 예제에서 x_Chicago,Nashville의 현실 의미와 수식 위치를 설명하라.",
            "공급부족 수송문제에 dummy supply를 추가하는 이유와 비용 설정을 말하라.",
            "노드3에 대해 SUMIF 순수유출량 식을 시작노드/종료노드 기준으로 써라.",
        ],
        web_refs=["WEB_OR_TOOLS_MIN_COST_FLOW", "WEB_OR_TOOLS_MAX_FLOW", "WEB_OR_TOOLS_ASSIGNMENT", "WEB_MS_SUMPRODUCT", "WEB_MS_SUMIF", "WEB_OR_TOOLS_LP"],
        qc_notes=["페이지 6, 7, 20, 21, 24, 34 등은 표/그림 OCR 누락 가능성이 있어 숫자 최적해는 원본 대조가 필요하다."],
    )


def build_dm07() -> Profile:
    return Profile(
        source_id="DM_PDF07",
        slug="ch07_nonlinear_programming",
        title="Ch.7 비선형계획",
        normalized_pdf="DM_PDF07_ch07_nonlinear_programming.pdf",
        thesis="비선형계획은 목적함수 또는 제약식에 비선형성이 들어가면서 지역 최적해, 초기해 민감성, 볼록성/오목성에 따른 전체 최적성 검증이 핵심이 되는 모델군이다.",
        graph_position="LP/Solver formulation -> nonlinear objective/constraint -> GRG local solution -> convexity/concavity checks -> KKT/global optimum diagnostics.",
        learning_outcomes=[
            "비선형 GRG 해가 지역 최적해일 수 있음을 설명한다.",
            "초기해와 볼록성 조건이 전체 최적성 판단에 왜 중요한지 말한다.",
            "자동차 가격 결정 예제를 목적함수, 제약식, Solver, 전체최적성 검사로 전개한다.",
        ],
        nodes=[
            n("nonlinear_programming", "비선형계획", "nonlinear programming", "목적함수 또는 제약식 중 적어도 하나가 비선형 함수인 최적화 모형이다.", "직선과 평면이 아니라 곡선/곡면 위에서 최적점을 찾는다.", "가격-수요 관계, 생산함수, 면적 최대화처럼 곱/제곱/로그 등이 있을 때 쓴다.", "continuous variables x.", "nonlinear f(x) maximize/minimize.", "linear or nonlinear constraints g_i(x)<=b_i.", "x1*x2 같은 식이 목표셀에 들어갈 수 있다.", "curved feasible regions and contour lines.", "Excel Solver에서 GRG Nonlinear 해법을 선택한다.", "p001-p002 비선형 함수식과 S=x1*x2 예제.", "2x1+x2=10 아래 S=x1*x2 최대화.", "비선형인데 Simplex LP로 풀려는 오류.", "LP formulation", "GRG, KKT", "quadratic programming", "비선형 여부 판정.", ["nonlinear", "비선형"], ["비선형 계획", "비선형 함수식"]),
            n("grg_solver", "GRG 비선형 해법", "GRG nonlinear solver", "Excel Solver에서 매끄러운 비선형 문제의 지역 최적 조건을 찾는 해법이다.", "곡면 위에서 기울기를 따라 개선하다가 더 개선하기 어려운 지점에 멈춘다.", "미분 가능한 비선형 Solver 모델에 쓴다.", "changing cells continuous x.", "nonlinear objective.", "constraints can be linear or nonlinear.", "초기해에 따라 다른 해로 갈 수 있다.", "local search on nonlinear landscape.", "Solver 해법선택: 비선형 GRG.", "p002, p031, p036.", "초기해 (0,0)과 (2.5,5) 차이.", "GRG 결과를 항상 전역 최적이라고 단정하는 오류.", "nonlinear_programming", "local_global_optimum", "KKT necessary conditions", "GRG 선택 이유.", ["GRG", "solver"], ["비선형 GRG", "GRG"]),
            n("local_global_optimum", "지역/전체 최적해", "local/global optimum", "지역 최적해는 주변에서만 최적인 해, 전체 최적해는 모든 가능해 중 최적인 해다.", "산봉우리가 여러 개면 가까운 봉우리가 최고봉이 아닐 수 있다.", "비선형 Solver 결과를 검증할 때 쓴다.", "candidate solution x*.", "compare f(x*) locally and globally.", "depends on feasible set and function shape.", "초기해 (0,0) 결과와 다른 초기해 결과가 다르다.", "nonconvex landscape.", "Solver가 찾아주는 해는 보통 지역 최적 조건을 만족한다.", "p003-p004 지역/전체 최적해.", "초기해 (0,0)->(0,0), 그 외 ->(2.5,5).", "지역 최적해를 무조건 전체 최적해로 제출하는 오류.", "GRG solver", "convexity sufficient conditions", "multi-start", "지역/전역 구분.", ["local", "global", "optimum"], ["지역 최적해", "전체 최적해"]),
            n("initial_solution_sensitivity", "초기해 민감성", "initial solution sensitivity", "비선형 Solver가 시작점에 따라 다른 지역해에 도달할 수 있는 성질이다.", "출발 위치가 다르면 다른 골짜기나 봉우리에 도착할 수 있다.", "비선형 해를 신뢰하기 전 여러 초기해를 시험할 때 쓴다.", "initial values of changing cells.", "same objective, different starting points.", "constraints unchanged.", "0,0에서 시작하면 (0,0), 다른 초기해는 (2.5,5)로 간다.", "basin of attraction.", "Solver 초기 변경셀 값과 multi-start 점검.", "p003 초기해 비교.", "초기해 하나만으로 최적성을 확정하지 않는다.", "초기값을 아무렇게 둬도 항상 같은 해라고 생각하는 오류.", "local_global_optimum", "multistart diagnostic", "nonconvex optimization", "초기해 바꿔보기.", ["initial_solution", "초기해"], ["초기해", "결과"]),
            n("convexity_concavity", "볼록성/오목성", "convexity and concavity", "최대화에서는 오목 목적함수와 볼록 가능영역, 최소화에서는 볼록 목적함수와 볼록 가능영역이 전체 최적성 보장의 핵심 조건이다.", "곡면 모양이 한 봉우리/한 골짜리이면 지역해가 전체해가 된다.", "GRG 해의 전역성 판단에 쓴다.", "objective f and feasible set.", "max concave f or min convex f under convex feasible set.", "linear constraints are convex feasible regions.", "자동차 가격결정 예제의 2차 목적함수 오목성 검사.", "convex set and contour geometry.", "Solver 결과 후 별도 수학 검증으로 붙인다.", "p006-p008, p029.", "선형 제약식들은 항상 볼록집합을 만든다.", "목적함수 볼록/오목 방향을 max/min에서 뒤집는 오류.", "local_global_optimum", "KKT sufficiency", "Hessian/principal minors", "전역 최적 충분조건.", ["convexity", "concavity", "볼록", "오목"], ["전체 최적해 조건", "오목함수", "볼록집합"]),
            n("nonlinear_constraints", "비선형 제약과 가능영역", "nonlinear constraints", "제약식이 비선형이면 각 제약이 만드는 가능영역이 볼록집합인지 따로 확인해야 한다.", "목적함수가 좋아도 feasible region이 찌그러져 있으면 지역해 문제가 생긴다.", "비선형 제약이 포함된 문제의 전역성 판단에 쓴다.", "g_i(x)<=b_i or g_i(x)>=b_i.", "objective depends on problem.", "convex feasible set conditions.", "비선형 제약의 가능해영역이 볼록이면 sufficient condition에 들어갈 수 있다.", "curved constraint boundary.", "Solver에는 식을 입력하지만, 해석은 convexity 검토가 필요하다.", "p008-p011.", "각 제약식 가능해영역이 볼록이면 전체 교집합도 볼록.", "비선형이면 무조건 nonconvex라고 단정하는 오류.", "convexity_concavity", "KKT", "feasible set geometry", "제약 볼록성 검사.", ["nonlinear_constraint", "feasible_set"], ["비선형 제약식", "가능해영역"]),
            n("quadratic_programming", "2차계획/2차 목적", "quadratic programming", "목적함수나 제약에 2차식이 포함된 비선형 최적화의 대표 형태다.", "가격-수요 또는 생산량 간 상호작용이 곡선으로 나타난다.", "2차 이익함수, 분산 최소화, 가격 결정에 쓴다.", "x variables and quadratic terms.", "quadratic objective.", "linear or quadratic constraints.", "자동차 가격 결정에서 총판매이익이 2차식으로 표현된다.", "parabolic contour/curvature.", "GRG 또는 QP solver로 풀 수 있다.", "p027-p030 자동차 가격 결정.", "목적함수가 오목이면 max의 지역해가 전체해가 된다.", "2차식이 있으면 모두 어려운 nonconvex라고 생각하는 오류.", "nonlinear_programming", "convexity_concavity", "pricing model", "2차식 해석.", ["quadratic", "2차식"], ["2차식", "자동차 가격"]),
            n("car_pricing_example", "자동차 가격 결정", "car pricing example", "중대형 승용차와 RV의 가격/판매량 관계를 반영해 총판매이익을 최대화하는 비선형 예제다.", "가격을 올리면 단위마진은 늘지만 수요가 줄어드는 trade-off를 최적화한다.", "수요-가격 관계가 있는 수익관리 문제에 쓴다.", "P1, P2 or vehicle sales/price variables.", "maximize total sales revenue - production cost.", "production capacity and price relation constraints.", "연간 생산능력 600천대 같은 제한 아래 이익을 최대화한다.", "quadratic profit surface over price variables.", "Solver changing cells에 가격 또는 관련 변수, GRG Nonlinear.", "예제 7.3 자동차 가격 결정.", "중대형/RV 생산원가와 생산능력 조건.", "가격을 독립적으로 올리면 항상 이익이 오른다고 생각하는 오류.", "quadratic_programming", "global optimality check", "revenue management", "예제 완전 정식화.", ["car_pricing", "자동차", "가격"], ["자동차 가격 결정", "총 판매이익"]),
            n("kkt_condition", "KKT 필요조건", "KKT conditions", "제약이 있는 비선형 최적화에서 지역 최적해가 만족해야 하는 일계 조건과 상보성 조건이다.", "최적점에서는 목적함수 개선방향과 제약 경계의 힘이 균형을 이룬다.", "GRG 해가 어떤 조건을 만족하는지 설명할 때 쓴다.", "gradient, multipliers, constraints.", "stationarity plus feasibility and complementarity.", "부등식 승수 비음/상보조건.", "상용 비선형 Solver 해는 보통 KKT 필요조건을 만족한다.", "tangent/normal geometry.", "Solver 결과의 수학적 진단.", "p039, p043.", "부등식 제약식*승수=0.", "KKT를 만족하면 항상 전체 최적이라고 단정하는 오류.", "local_global_optimum", "convexity sufficiency", "complementary slackness", "필요조건 vs 충분조건.", ["KKT", "multiplier"], ["KKT", "부등식제약식"]),
        ],
        examples=[
            ex("rectangle_product", "S=x1*x2 예제", "2x1+x2=10 아래 S=x1*x2를 최대화한다.", "x1,x2.", "max S=x1*x2.", "2x1+x2=10.", "GRG Nonlinear.", "초기해에 따라 Solver 결과가 달라질 수 있음을 보여준다.", ["비선형 목적 확인.", "GRG 선택.", "초기해 바꿔 실행.", "지역/전체 판단."], ["Maximize S= X1.X2", "초기해"]),
            ex("car_pricing", "자동차 가격 결정 예제", "가격-수요 관계와 생산능력 제약 아래 총판매이익을 최대화한다.", "P1,P2 또는 판매량 관련 변수.", "max revenue-cost quadratic objective.", "생산능력 선형 제약.", "GRG Nonlinear, global optimality check.", "오목 목적함수+선형 제약이면 지역 최적해가 전체 최적해다.", ["현실 관계식 읽기.", "목적함수 구성.", "제약 입력.", "오목성/볼록성 확인."], ["자동차 가격 결정", "전체 최적성 검사"]),
            ex("kkt_check", "KKT와 전체최적성 판별", "구한 KKT 해가 전체최적해인지 볼록성 조건으로 판별한다.", "candidate x and multipliers.", "stationarity condition.", "feasibility and complementarity.", "Solver 해 후 수학적 검토.", "KKT는 필요조건이고 convexity가 있어야 충분조건이 된다.", ["KKT 만족 확인.", "목적함수 curvature 확인.", "가능영역 볼록성 확인."], ["KKT해", "전체최적해인지"]),
        ],
        patterns=[
            ("GRG-local형", "비선형 Solver 결과는 지역해일 수 있으므로 초기해/전역성 검토가 필요하다.", "grg_solver", "local_global_optimum"),
            ("볼록성검토형", "max는 오목 목적+볼록 가능영역, min은 볼록 목적+볼록 가능영역을 확인한다.", "convexity_concavity", "KKT"),
            ("가격-수요형", "수익과 수요가 비선형으로 얽히면 목적함수 curvature를 해석한다.", "car_pricing_example", "quadratic_programming"),
        ],
        solver_rows=[
            ("변수셀", "연속 가격/생산/치수 변수", "초기값을 의미 있게 설정하고 여러 초기값을 시도한다."),
            ("목표셀", "곱, 제곱, 로그 등 비선형 식", "Simplex LP가 아니라 GRG Nonlinear."),
            ("제약셀", "선형/비선형 제약", "비선형 제약은 가능영역 볼록성 검토가 필요하다."),
            ("검증", "지역해 vs 전체해", "Solver 결과 후 curvature/KKT/초기해 민감성을 기록한다."),
        ],
        cross_connections=[
            ("LP 단원", "LP는 선형이라 지역/전체 문제가 단순하지만 NLP는 그렇지 않다.", "linear -> nonlinear"),
            ("DM_PDF05 상보여유", "KKT의 complementarity는 LP 상보여유의 비선형 확장이다.", "complementary slackness -> KKT"),
            ("Solver 모델링", "Solver 해법 선택이 Simplex LP에서 GRG Nonlinear로 바뀐다.", "Solver method selection"),
        ],
        misconceptions=[
            ("GRG=전체최적", "GRG는 지역 필요조건 해를 줄 수 있다.", "초기해와 convexity 검토를 붙인다.", "grg_solver"),
            ("비선형이면 무조건 못 풂", "오목/볼록 구조면 전역성 보장이 가능하다.", "목적/제약 curvature를 확인.", "convexity_concavity"),
            ("KKT 충분조건 오해", "일반 nonconvex에서 KKT는 필요조건이다.", "볼록성 조건이 있어야 충분조건.", "kkt_condition"),
        ],
        routes=[
            Route("비선형 Solver는 뭘 선택?", "grg_solver", "nonlinear_programming", "rectangle_product", "DM_PDF07:p002"),
            Route("지역해와 전체해 차이?", "local_global_optimum", "initial_solution_sensitivity", "rectangle_product", "DM_PDF07:p003"),
            Route("전체 최적성 어떻게 보장?", "convexity_concavity", "kkt_condition", "car_pricing", "DM_PDF07:p006-p008"),
            Route("자동차 가격 예제 식?", "car_pricing_example", "quadratic_programming", "car_pricing", "DM_PDF07:p027-p030"),
        ],
        practice=[
            "GRG로 얻은 해가 전체 최적해인지 확인하는 절차를 세 단계로 말하라.",
            "max 문제에서 목적함수 오목성과 가능영역 볼록성이 왜 필요한지 설명하라.",
            "초기해 두 개를 넣어 서로 다른 결과가 나왔을 때 보고서에 무엇을 적어야 하는가?",
        ],
        web_refs=["WEB_MS_SOLVERADD", "WEB_MS_SOLVERSOLVE"],
        qc_notes=["DM_PDF07은 저텍스트 페이지가 많아 그래프/수식 페이지는 원본 PDF 대조가 특히 필요하다."],
    )


def build_dm08() -> Profile:
    return Profile(
        source_id="DM_PDF08",
        slug="ch06_integer_programming_week2",
        title="Ch.6 정수계획 2주차: 0-1 응용 모형",
        normalized_pdf="DM_PDF08_ch06_integer_programming_week2.pdf",
        thesis="0-1 정수계획은 선택 여부를 변수로 두고, cover/partition/pack 같은 행렬 제약으로 공공설비 입지와 혜택 최대화 문제를 모델링한다.",
        graph_position="binary variable -> coverage matrix A -> set covering/partitioning/packing -> facility location variants -> branch-and-bound solution trace.",
        learning_outcomes=[
            "공공설비 입지 선정 문제를 set covering Ax>=1로 정식화한다.",
            "set covering, set partitioning, set packing의 부등호 차이를 구분한다.",
            "혜택 최대화 변형에서 x_j 설치변수와 y_i 혜택변수를 분리한다.",
        ],
        nodes=[
            n("facility_location_set_cover", "공공설비 입지 선정", "facility location set covering", "모든 수요지역이 일정 시간/거리 안에서 서비스되도록 최소 개수의 시설 위치를 고르는 0-1 모형이다.", "모두가 혜택을 받게 하되 설치 수를 최대한 줄인다.", "소방서, 응급차량, 학교, 병원 후보지 선택에 쓴다.", "x_j=후보지역 j에 시설 설치 여부.", "min sum x_j.", "각 행정구역 i에 대해 sum_j A_ij x_j >=1.", "13개 행정구역이 10분 내 응급서비스를 받을 수 있게 한다.", "coverage bipartite graph.", "Solver binary variables with coverage rows.", "신도시 B 응급 의료 서비스.", "후보지 8곳, 행정구역 13개.", "목적을 거리 최소화로 바꿔 버리는 오류.", "binary variable", "set covering", "facility location", "Ax>=1 정식화.", ["facility_location", "set_cover"], ["공공 설비 입지", "응급 의료"]),
            n("coverage_matrix", "커버리지 행렬", "coverage matrix", "A_ij=1이면 후보지 j가 구역 i를 커버하고, 0이면 커버하지 않는 0/1 입력 행렬이다.", "지도 위 도달 가능성을 수학 표로 바꾼 것이다.", "covering 제약을 만들 때 쓴다.", "A matrix 13x8 and x vector.", "objective independent of A except constraints.", "A x >= 1 or variants.", "10분 이내 도달 가능성을 행렬로 입력한다.", "bipartite incidence matrix.", "Spreadsheet에서 A matrix와 x vector의 row products/sums.", "p002-p003.", "행정구역 i에서 후보지역 j까지 10분 이내면 Aij=1.", "행/열을 바꿔 구역과 후보지를 혼동하는 오류.", "facility_location_set_cover", "set_partitioning_packing", "incidence matrix", "Aij 의미.", ["coverage_matrix", "Aij"], ["Aij", "도달 가능성"]),
            n("binary_open_variable", "0-1 설치변수", "binary open variable", "후보지에 시설을 설치하면 1, 아니면 0인 선택 변수다.", "스위치처럼 켜고 끄는 의사결정이다.", "시설 선택, 프로젝트 선택, 응급차량 설치 여부에 쓴다.", "x_j in {0,1}.", "sum x_j minimized or constrained.", "binary domain and coverage constraints.", "x=(x1,...,x8).", "binary vector over candidate sites.", "Solver에서 bin 조건 또는 int+<=1 조건.", "p002, p004.", "xj=후보지역 j에 응급차량 설치여부.", "0<=x<=1만 두어 fractional 설치를 허용하는 오류.", "integer programming", "branch and bound", "fixed-charge y variables", "binary 설정.", ["binary", "0-1", "xj"], ["0-1 변수", "설치여부"]),
            n("set_covering_partitioning_packing", "covering/partitioning/packing", "set covering/partitioning/packing", "Ax>=1은 최소 하나 이상 커버, Ax=1은 정확히 하나, Ax<=1은 겹치지 않게 선택하는 0-1 집합 모형이다.", "부등호 하나가 문제 의미를 완전히 바꾼다.", "coverage 구조를 변형할 때 쓴다.", "A matrix and binary x.", "min or max depending on model.", "Ax>=1, Ax=1, Ax<=1.", "행정구역별 covering 수가 1 이상이면 set covering이다.", "set system incidence.", "Spreadsheet row coverage counts compared to 1.", "p006-p007.", "set-partitioning은 covering 수=1, set-packing은 <=1.", ">=,=,<=를 암기만 하고 현실 의미를 설명하지 못하는 오류.", "coverage_matrix", "assignment/set partitioning", "combinatorial optimization", "부등호별 의미.", ["set_covering", "partitioning", "packing"], ["set-covering", "set-partitioning", "set-packing"]),
            n("benefit_max_variant", "혜택 최대화 변형", "benefit maximization variant", "설치 수가 제한된 상황에서 혜택 받는 주민 수를 최대화하도록 시설 위치와 구역 혜택 여부를 함께 결정하는 변형 모형이다.", "모두를 커버하지 못할 수 있으면, 제한된 시설로 가장 많은 주민에게 혜택을 준다.", "예산/설치 수 상한 때문에 전 지역 커버가 불가능하거나 목표가 다를 때 쓴다.", "x_j=설치 여부, y_i=구역 i 혜택 여부.", "max sum population_i y_i.", "sum x_j=3, y_i <= sum_j A_ij x_j, x,y binary.", "혜택 여부 y를 따로 둬 중복커버가 주민수를 중복 계산하지 않게 한다.", "coverage graph with covered-demand indicators.", "Solver에서 x와 y 두 binary vector를 둔다.", "연습문제 19번 변형.", "최대 3군데 설치, 주민 수 최대화.", "x 조합을 목적함수에 직접 여러 번 더해 중복 커버를 과대계산하는 오류.", "set covering", "wrong_model_diagnosis", "max coverage problem", "y_i 도입 이유.", ["max_coverage", "benefit", "yi"], ["혜택여부", "주민 수"]),
            n("wrong_model_diagnosis", "잘못된 모형화 진단", "wrong model diagnosis", "coverage 수를 그대로 주민수에 곱해 중복 혜택을 여러 번 계산하는 오류를 식별하는 진단 노드다.", "한 구역이 두 시설에서 커버돼도 주민이 두 배로 늘지는 않는다.", "혜택 최대화 변형에서 오답을 고칠 때 쓴다.", "x_j only wrong model versus y_i correct model.", "wrong objective sums coverage terms directly.", "missing y_i <= coverage_i linking.", "구역별 혜택 여부를 분리해야 중복계산을 막는다.", "overcounting in incidence graph.", "Spreadsheet에서 coverage count와 binary benefit indicator를 분리한다.", "p011 범하기 쉬운 잘못된 모형화.", "Maximize 5.4(x1+x4)+... 형태가 잘못될 수 있다.", "covering 수와 혜택 여부를 동일시하는 오류.", "benefit_max_variant", "binary logic constraints", "indicator variable", "오답식 수정.", ["wrong_model", "overcount"], ["잘못된 모형화", "혜택 받는 주민수"]),
            n("multiple_optima_facility", "입지모형 복수 최적", "multiple optima in facility location", "같은 설치 수로 전 지역을 커버하는 후보 조합이 여러 개 나올 수 있는 현상이다.", "최소 시설 수는 같지만 실제 위치 조합은 여러 해가 가능할 수 있다.", "해석과 대안 제시가 필요할 때 쓴다.", "binary x alternative solutions.", "same min sum x.", "same coverage feasibility.", "공공설비 입지선정에는 복수 최적해가 자주 발생한다.", "many equivalent covers in set system.", "Solver가 보여준 한 해 외에 대안 해 탐색 필요.", "p008 체크 포인트.", "복수 최적해 자주 발생.", "Solver 해 하나만 정책적으로 유일한 답이라고 말하는 오류.", "set_covering", "sensitivity/robustness", "alternate optimum", "대안 입지 조합.", ["multiple_optima", "facility"], ["복수 최적해"]),
            n("branch_bound_review", "분지한계법 복습", "branch-and-bound review", "0-1 입지모형 같은 정수계획을 풀기 위해 branch-and-bound 과정을 적용하는 후반 복습 노드다.", "binary 선택 문제도 결국 탐색과 bound로 최적성을 증명한다.", "정수계획 해법과 0-1 응용을 연결할 때 쓴다.", "binary/integer variables.", "LP relaxation bound and incumbent.", "branching constraints and pruning.", "예제 6.9 분지한계법 적용이 다시 등장한다.", "search tree over binary/integer decisions.", "Solver MIP search.", "p015 이후.", "Z가 큰 부문제부터 적용.", "모형화와 해법을 분리하지 못하는 오류.", "DM_PDF03 branch_and_bound", "MIP solver", "tree search", "분지한계 복습.", ["branch_bound", "review"], ["분지한계법", "부문제"]),
        ],
        examples=[
            ex("emergency_service_cover", "신도시 B 응급 의료 서비스", "후보지 8곳 중 최소 개수를 골라 13개 행정구역을 모두 10분 이내 커버한다.", "x_j=후보지 j 설치 여부.", "min x1+...+x8.", "A x >= 1, x_j binary.", "Solver binary model with coverage matrix.", "해는 설치 후보지 조합이며 복수 최적 가능성이 있다.", ["후보지와 구역 파악.", "Aij 행렬 작성.", "Ax>=1 제약.", "설치 수 최소화."], ["신도시 B", "응급 서비스를"]),
            ex("max_covered_population", "주민 수 혜택 최대화 변형", "최대 3곳 설치로 혜택 받는 주민 수를 최대화한다.", "x_j 설치, y_i 혜택.", "max sum population_i y_i.", "sum x_j=3, y_i<=coverage_i, x,y binary.", "Solver with two binary variable blocks.", "y_i가 중복커버의 과대계산을 막는다.", ["x와 y를 분리.", "설치 수 제약.", "linking constraint.", "주민수 목적함수."], ["19번 문제", "혜택여부"]),
            ex("wrong_model_fix", "잘못된 혜택모형 수정", "coverage count를 주민수에 직접 곱하는 잘못된 모형을 y_i indicator로 고친다.", "wrong: only x; correct: x and y.", "correct max population*y.", "y_i<=sum Aij xj.", "Spreadsheet coverage count plus binary benefit.", "한 구역은 커버되면 1번만 혜택으로 계산한다.", ["오답 목적함수 찾기.", "중복커버 문제 설명.", "y_i 도입.", "linking constraint 추가."], ["범하기 쉬운 잘못된 모형화"]),
        ],
        patterns=[
            ("cover 최소화", "모든 행이 하나 이상 커버되도록 Ax>=1, min sum x.", "facility_location_set_cover", "set covering"),
            ("benefit 최대화", "설치 수 제한 아래 y_i를 두고 max population*y.", "benefit_max_variant", "max coverage"),
            ("오답진단", "coverage count와 benefit indicator를 분리한다.", "wrong_model_diagnosis", "indicator variable"),
        ],
        solver_rows=[
            ("변수셀", "x_j 설치 여부, y_i 혜택 여부", "둘 다 binary."),
            ("목표셀", "설치 수 최소화 또는 혜택 주민수 최대화", "문제 변형에 따라 방향이 바뀐다."),
            ("제약셀", "Ax>=1, sum x=3, y_i<=coverage_i", "부등호 의미를 현실 문장으로 확인한다."),
            ("해법", "MIP/branch-and-bound", "복수 최적해 가능성을 보고서에 남긴다."),
        ],
        cross_connections=[
            ("DM_PDF04 0-1 IP", "입지선정은 binary 선택변수의 대표 응용이다.", "binary -> facility"),
            ("DM_PDF03 분지한계", "0-1 모형은 branch-and-bound로 최적성을 증명한다.", "set covering -> B&B"),
            ("DM_PDF06 네트워크", "coverage matrix는 네트워크 incidence/edge table 사고와 유사하다.", "incidence table"),
        ],
        misconceptions=[
            ("Ax 부등호 혼동", ">=,=,<=가 각각 covering/partitioning/packing을 뜻한다.", "구역별 현실 문장으로 먼저 번역.", "set_covering_partitioning_packing"),
            ("중복커버 과대계산", "한 구역 주민은 여러 시설로 커버되어도 한 번만 세야 한다.", "y_i 혜택변수를 둔다.", "wrong_model_diagnosis"),
            ("binary 설정 누락", "연속값 0.4개 설치 같은 해가 나올 수 있다.", "bin 또는 int+<=1을 지정.", "binary_open_variable"),
        ],
        routes=[
            Route("set covering 식 어떻게 세워?", "facility_location_set_cover", "coverage_matrix", "emergency_service_cover", "DM_PDF08:p001-p004"),
            Route("covering/partitioning/packing 차이?", "set_covering_partitioning_packing", "coverage_matrix", "emergency_service_cover", "DM_PDF08:p006-p007"),
            Route("주민수 최대화 변형은 왜 y가 필요?", "benefit_max_variant", "wrong_model_diagnosis", "max_covered_population", "DM_PDF08:p010-p011"),
            Route("복수 최적해가 나오면?", "multiple_optima_facility", "facility_location_set_cover", "emergency_service_cover", "DM_PDF08:p008"),
        ],
        practice=[
            "Aij=1의 현실 의미를 한 문장으로 쓰고 Ax>=1을 번역하라.",
            "set partitioning과 set packing의 부등호 차이를 예시와 함께 설명하라.",
            "혜택 최대화 변형에서 y_i<=coverage_i가 왜 필요한지 반례로 설명하라.",
        ],
        web_refs=["WEB_OR_TOOLS_MIP", "WEB_MS_SOLVERADD", "WEB_MS_SOLVERSOLVE"],
        qc_notes=["DM_PDF08 후반 분지한계 그림 페이지는 저텍스트가 많아 tree 숫자는 DM_PDF03 전사와 함께 대조한다."],
    )


ANCHOR_RE = re.compile(r"\[(DM_PDF\d{2}:p(\d{3}):L(\d{3}))\]\s*(.*)")


def transcript_path(profile: Profile) -> Path:
    return TRANSCRIPT_DIR / f"{profile.source_id}__{profile.slug}__full_transcript.md"


def sidecar_dir(profile: Profile) -> Path:
    return INVENTORY_DIR / f"{profile.source_id}__{profile.slug}"


def parse_transcript(path: Path) -> tuple[list[dict], dict[int, list[dict]], dict[str, int]]:
    lines: list[dict] = []
    pages: dict[int, list[dict]] = {}
    meta = {"page_count": 0, "low_text_pages": 0, "extraction_risk_pages": 0}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("**page_count:**"):
            meta["page_count"] = int(re.search(r"\d+", raw).group(0))
        elif raw.startswith("**low_text_pages:**"):
            meta["low_text_pages"] = int(re.search(r"\d+", raw).group(0))
        elif raw.startswith("**extraction_risk_pages:**"):
            meta["extraction_risk_pages"] = int(re.search(r"\d+", raw).group(0))
        match = ANCHOR_RE.match(raw)
        if not match:
            continue
        anchor, page_s, line_s, text = match.groups()
        row = {
            "anchor": anchor,
            "page": int(page_s),
            "line": int(line_s),
            "text": text.strip(),
            "raw": raw,
        }
        lines.append(row)
        pages.setdefault(row["page"], []).append(row)
    return lines, pages, meta


def norm(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def score_line(text: str, pattern: str) -> int:
    haystack = norm(text)
    tokens = [token for token in re.split(r"[\s,|/]+", pattern.lower()) if token]
    score = 0
    for token in tokens:
        if norm(token) in haystack:
            score += len(token) + 3
    return score


def find_evidence(lines: list[dict], patterns: Iterable[str]) -> dict:
    best: dict | None = None
    best_score = -1
    for line in lines:
        text = line["text"]
        if "EXTRACTION_LOW_TEXT" in text:
            continue
        for pattern in patterns:
            score = score_line(text, pattern)
            if score > best_score:
                best = line
                best_score = score
    if best is None or best_score <= 0:
        for line in lines:
            if line["text"] and not line["text"].isdigit() and "EXTRACTION" not in line["text"]:
                return line
        return {"anchor": "MISSING", "page": 0, "line": 0, "text": "MISSING", "raw": ""}
    return best


def make_evidence_id(profile: Profile, kind: str, slug: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_]+", "_", slug)
    return f"ev_deep_{profile.source_id}_{kind}_{safe}"


def source_coverage_map(pages: dict[int, list[dict]]) -> str:
    rows = ["| page | primary anchors | extracted focus | extraction note |", "|---|---|---|---|"]
    for page in sorted(pages):
        usable = [
            item
            for item in pages[page]
            if item["text"]
            and not item["text"].isdigit()
            and "EXTRACTION_LOW_TEXT" not in item["text"]
            and "EXTRACTION_GAP" not in item["text"]
        ]
        if not usable:
            focus = "텍스트 추출 부족. 원본 PDF/OCR 대조 필요."
            anchors = "-"
        else:
            focus = " / ".join(item["text"] for item in usable[:3])
            anchors = ", ".join(item["anchor"] for item in usable[:2])
        note = "LOW_TEXT" if any("EXTRACTION_LOW_TEXT" in item["text"] for item in pages[page]) else "ok"
        rows.append(f"| p{page:03d} | `{anchors}` | {focus} | {note} |")
    return "\n".join(rows)


def web_grounding_table(web_refs: list[str]) -> str:
    rows = ["| web_id | role in this RAG | URL |", "|---|---|---|"]
    for ref in web_refs:
        src = WEB_SOURCES[ref]
        rows.append(f"| `{ref}` | {src['use']} | {src['url']} |")
    return "\n".join(rows)


def render_node(profile: Profile, node: Node, evidence: dict) -> str:
    node_id = f"n_{profile.source_id}.{node.slug}"
    evidence_id = make_evidence_id(profile, "node", node.slug)
    tags = ", ".join(f"`{tag}`" for tag in node.tags)
    return f"""### {node_id} — {node.label} ({node.english})

1. **한 줄 정의:** {node.definition}
2. **쉬운 직관:** {node.intuition}
3. **언제 쓰는가:** {node.when}
4. **변수 정의:** {node.variables}
5. **목적함수:** {node.objective}
6. **제약식:** {node.constraints}
7. **수식의 현실 의미:** {node.real_meaning}
8. **그래프/네트워크 관점:** {node.graph_view}
9. **스프레드시트/Solver 관점:** {node.solver_view}
10. **강의 예제 연결:** {node.example}
11. **예제 숫자 해석:** {node.numeric}
12. **자주 하는 실수:** {node.mistakes}
13. **선행 노드:** {node.prereq}
14. **후속 노드:** {node.followup}
15. **동형/유사 노드:** {node.similar}
16. **시험 출제 포인트:** {node.exam}
17. **RAG retrieval tags:** {tags}
18. **Evidence anchors:** `{evidence_id}` -> `{evidence['anchor']}` / source_id=`{profile.source_id}`, page=`p{evidence['page']:03d}`, block=`p{evidence['page']:03d}-L{evidence['line']:03d}`, line=`L{evidence['line']:03d}`

> 근거 excerpt: {evidence['text']}
"""


def render_example(profile: Profile, example: Example, evidence: dict) -> str:
    evidence_id = make_evidence_id(profile, "example", example.slug)
    coach_steps = "\n".join(f"{idx}. {step}" for idx, step in enumerate(example.coach, start=1))
    return f"""### ex_{profile.source_id}.{example.slug} — {example.title}

- **현실 문장 재해석:** {example.problem}
- **의사결정변수:** {example.variables}
- **목적함수:** {example.objective}
- **제약식:** {example.constraints}
- **Solver 구조:** {example.solver}
- **결과 해석:** {example.interpretation}
- **코칭 순서:**
{coach_steps}
- **Evidence anchors:** `{evidence_id}` -> `{evidence['anchor']}` / page=`p{evidence['page']:03d}`, block=`p{evidence['page']:03d}-L{evidence['line']:03d}`, line=`L{evidence['line']:03d}`

> 근거 excerpt: {evidence['text']}
"""


def table(headers: list[str], rows: Iterable[Iterable[str]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_doc(profile: Profile) -> tuple[str, dict]:
    lines, pages, meta = parse_transcript(transcript_path(profile))
    node_evidence = {node.slug: find_evidence(lines, node.patterns) for node in profile.nodes}
    example_evidence = {example.slug: find_evidence(lines, example.patterns) for example in profile.examples}

    concept_rows = []
    edge_rows = []
    for node in profile.nodes:
        concept_rows.append(
            [
                f"`n_{profile.source_id}.{node.slug}`",
                node.label,
                node.definition,
                node.prereq,
                node.followup,
            ]
        )
        edge_rows.extend(
            [
                [f"`{node.prereq}`", "선행 관계", f"`n_{profile.source_id}.{node.slug}`"],
                [f"`n_{profile.source_id}.{node.slug}`", "후속 관계", f"`{node.followup}`"],
                [f"`n_{profile.source_id}.{node.slug}`", "동형/유사", f"`{node.similar}`"],
            ]
        )

    source_trace_rows: list[list[str]] = []
    enhanced_evidence_jsonl: list[dict] = []
    for node in profile.nodes:
        evidence = node_evidence[node.slug]
        evidence_id = make_evidence_id(profile, "node", node.slug)
        source_trace_rows.append(
            [
                f"`n_{profile.source_id}.{node.slug}`",
                f"`{evidence_id}`",
                f"`{profile.source_id}`",
                f"`p{evidence['page']:03d}`",
                f"`p{evidence['page']:03d}-L{evidence['line']:03d}`",
                f"`L{evidence['line']:03d}`",
                evidence["text"],
            ]
        )
        enhanced_evidence_jsonl.append(
            {
                "evidence_id": evidence_id,
                "kind": "node",
                "node_id": f"n_{profile.source_id}.{node.slug}",
                "source_id": profile.source_id,
                "page": evidence["page"],
                "block": f"p{evidence['page']:03d}-L{evidence['line']:03d}",
                "line": evidence["line"],
                "anchor": evidence["anchor"],
                "excerpt": evidence["text"],
            }
        )
    for example in profile.examples:
        evidence = example_evidence[example.slug]
        evidence_id = make_evidence_id(profile, "example", example.slug)
        source_trace_rows.append(
            [
                f"`ex_{profile.source_id}.{example.slug}`",
                f"`{evidence_id}`",
                f"`{profile.source_id}`",
                f"`p{evidence['page']:03d}`",
                f"`p{evidence['page']:03d}-L{evidence['line']:03d}`",
                f"`L{evidence['line']:03d}`",
                evidence["text"],
            ]
        )
        enhanced_evidence_jsonl.append(
            {
                "evidence_id": evidence_id,
                "kind": "example",
                "example_id": f"ex_{profile.source_id}.{example.slug}",
                "source_id": profile.source_id,
                "page": evidence["page"],
                "block": f"p{evidence['page']:03d}-L{evidence['line']:03d}",
                "line": evidence["line"],
                "anchor": evidence["anchor"],
                "excerpt": evidence["text"],
            }
        )

    doc = f"""# {profile.source_id} — {profile.title} 최종 RAG 튜터 운영문서

## 0. Document Contract

- **문서 성격:** PDF 요약본이 아니라, 전담 1:1 경영과학 튜터와 RAG agent가 함께 쓰는 증거 기반 운영문서다.
- **source_id:** `{profile.source_id}`
- **normalized_pdf:** `decisionMaking/pdf_sources/{profile.normalized_pdf}`
- **primary transcript:** `decisionMaking/pdf_transcripts/{profile.source_id}__{profile.slug}__full_transcript.md`
- **sidecar:** `decisionMaking/_inventory/{profile.source_id}__{profile.slug}`
- **flat-pack target:** `decisionMaking/rag_applied_flat_pack/{profile.source_id}__04_rag.md`
- **source priority:** 1) PDF 전사본 anchor, 2) 이 문서의 enhanced sidecar, 3) 웹 그라운딩, 4) 일반 OR/MS 지식.
- **중요한 명명 주의:** `{profile.source_id}`는 PDF intake index다. 강의 회차/장 번호와 혼동하지 않는다.

### Web Grounding Notes

웹 근거는 PDF 원문을 대체하지 않는다. Solver 구현, LP/MIP/flow 표준 용어, Excel 함수 의미를 보조 확인하기 위해서만 사용한다.

{web_grounding_table(profile.web_refs)}

## 1. Source Coverage Map

{source_coverage_map(pages)}

## 2. Chapter Thesis

{profile.thesis}

## 3. Current Graph Position

- **현재 그래프 위치:** {profile.graph_position}
- **지금 보는 노드:** `{profile.source_id}` / {profile.title}
- **튜터 운영 원칙:** 질문이 들어오면 먼저 노드로 매핑하고, 예제 카드와 수식/Solver 구조를 거쳐 Source Trace Table의 evidence anchor로 되돌아간다.

## 4. Learning Outcomes

{chr(10).join(f"- {item}" for item in profile.learning_outcomes)}

## 5. Concept Graph Map

{table(["node_id", "개념", "역할", "선행 노드", "후속 노드"], concept_rows)}

### Edge List

{table(["from", "edge_type", "to"], edge_rows)}

## 6. Core Concept Node Cards

{chr(10).join(render_node(profile, node, node_evidence[node.slug]) for node in profile.nodes)}

## 7. Example Walkthrough Cards

{chr(10).join(render_example(profile, example, example_evidence[example.slug]) for example in profile.examples)}

## 8. Modeling Pattern Library

{table(["pattern", "모형화 템플릿", "먼저 볼 노드", "연결 노드"], profile.patterns)}

## 9. Spreadsheet / Solver Mapping

{table(["요소", "Solver/Spreadsheet 대응", "튜터 해설 포인트"], profile.solver_rows)}

## 10. Cross-Chapter Connections

{table(["연결 대상", "연결 설명", "의존/참조 관계"], profile.cross_connections)}

## 11. Misconception & Error Diagnosis Bank

{table(["오답/착각", "왜 문제인가", "교정 코칭", "연결 노드"], profile.misconceptions)}

## 12. Retrieval Routing Table

{table(["사용자 질문 유형", "먼저 볼 노드", "다음 볼 노드", "예제 카드", "근거 힌트"], ([route.question, f"`{route.first_node}`", f"`{route.next_node}`", f"`{route.example}`", route.evidence_hint] for route in profile.routes))}

## 13. Tutor Session Protocol

1. **지도부터:** Concept Graph Map과 Edge List를 먼저 보여주고, 현재 노드가 전체 OR/MS 흐름에서 어디인지 설명한다.
2. **노드 중심으로:** Core Concept Node Card의 18개 필드를 순서대로 따라가되, 선행/후속/동형 노드를 최소 3개 연결한다.
3. **예제 중심으로:** Example Walkthrough Card를 사용해 현실 문장 -> 변수 -> 목적함수 -> 제약식 -> Solver -> 결과 해석 순서로 진행한다.
4. **문제 풀이 모드:** 사용자가 변수를 먼저 말하게 하고, 목적함수/제약식은 힌트로 한 단계씩 유도한다.
5. **완성 해설 모드:** 위 절차를 생략하지 않고 전체 풀이를 한 번에 제시한다.
6. **암기/정리 모드:** Modeling Pattern Library, Solver Mapping, Misconception Bank만 압축해 제시한다.

## 14. Practice / Check Questions

{chr(10).join(f"{idx}. {item}" for idx, item in enumerate(profile.practice, start=1))}

## 15. Source Trace Table

{table(["RAG label", "evidence_id", "source_id", "page", "block", "line", "excerpt"], source_trace_rows)}

## 16. QC / Extraction Risk Notes

- **page_count:** {meta["page_count"]}
- **low_text_pages:** {meta["low_text_pages"]}
- **extraction_risk_pages:** {meta["extraction_risk_pages"]}
- **QC policy:** 표, 그림, 수식 이미지가 많은 페이지는 전사 텍스트만으로 숫자를 단정하지 않는다. 튜터는 수식 구조와 증거 anchor를 우선 제시하고, 숫자 최적해는 필요 시 원본 PDF를 대조한다.
{chr(10).join(f"- {note}" for note in profile.qc_notes)}
"""

    metadata = {
        "source_id": profile.source_id,
        "node_count": len(profile.nodes),
        "example_count": len(profile.examples),
        "route_count": len(profile.routes),
        "page_count": meta["page_count"],
        "low_text_pages": meta["low_text_pages"],
        "evidence": enhanced_evidence_jsonl,
    }
    return doc.rstrip() + "\n", metadata


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def generate() -> dict:
    add_more_profiles()
    report_rows = []
    failures: list[str] = []
    for profile in PROFILES:
        doc, meta = build_doc(profile)
        sc_dir = sidecar_dir(profile)
        sc_dir.mkdir(parents=True, exist_ok=True)
        inventory_rag = sc_dir / f"{profile.source_id}__{profile.slug}__rag.md"
        flat_rag = FLAT_PACK_DIR / f"{profile.source_id}__04_rag.md"
        inventory_rag.write_text(doc, encoding="utf-8")
        flat_rag.write_text(doc, encoding="utf-8")

        nodes_json = [
            {
                "node_id": f"n_{profile.source_id}.{node.slug}",
                "label": node.label,
                "english": node.english,
                "definition": node.definition,
                "tags": node.tags,
                "source_id": profile.source_id,
            }
            for node in profile.nodes
        ]
        edges_json = []
        for node in profile.nodes:
            node_id = f"n_{profile.source_id}.{node.slug}"
            edges_json.extend(
                [
                    {"from": node.prereq, "to": node_id, "edge_type": "prerequisite"},
                    {"from": node_id, "to": node.followup, "edge_type": "followup"},
                    {"from": node_id, "to": node.similar, "edge_type": "analogous"},
                ]
            )
        routes_json = [
            {
                "question": route.question,
                "first_node": route.first_node,
                "next_node": route.next_node,
                "example": route.example,
                "evidence_hint": route.evidence_hint,
            }
            for route in profile.routes
        ]
        write_json(sc_dir / "enhanced_nodes.json", nodes_json)
        write_json(sc_dir / "enhanced_edges.json", edges_json)
        write_json(sc_dir / "enhanced_retrieval_routes.json", routes_json)
        (sc_dir / "enhanced_evidence.jsonl").write_text(
            "\n".join(json.dumps(row, ensure_ascii=False) for row in meta["evidence"]) + "\n",
            encoding="utf-8",
        )

        for section in SECTIONS:
            if f"## {section}" not in doc:
                failures.append(f"{profile.source_id}: missing section {section}")
        if "MISSING" in doc:
            failures.append(f"{profile.source_id}: missing evidence anchor")

        report_rows.append(
            {
                "source_id": profile.source_id,
                "title": profile.title,
                "nodes": meta["node_count"],
                "examples": meta["example_count"],
                "routes": meta["route_count"],
                "low_text_pages": meta["low_text_pages"],
            }
        )

    dm06_text = (FLAT_PACK_DIR / "DM_PDF06__04_rag.md").read_text(encoding="utf-8")
    required_dm06_nodes = {
        "transportation_problem",
        "balanced_transportation",
        "unbalanced_transportation",
        "transportation_integrality",
        "transportation_solver_model",
        "transportation_sensitivity",
        "assignment_problem",
        "transshipment_problem",
        "transshipment_balance",
        "minimum_cost_flow",
        "maximum_flow",
        "shortest_path",
        "network_topology_table",
        "sumif_node_balance",
        "cpm_pert",
    }
    for node in required_dm06_nodes:
        if f"n_DM_PDF06.{node}" not in dm06_text:
            failures.append(f"DM_PDF06: required node missing {node}")

    web_doc = ["# DecisionMaking Enhanced RAG Web Grounding Sources", ""]
    web_doc.append("PDF transcript anchors remain the primary evidence. These web sources are supplemental grounding for solver vocabulary, spreadsheet functions, and standard optimization formulations.")
    web_doc.append("")
    web_doc.append("| web_id | title | use | url |")
    web_doc.append("|---|---|---|---|")
    for web_id, source in WEB_SOURCES.items():
        web_doc.append(f"| `{web_id}` | {source['title']} | {source['use']} | {source['url']} |")
    (INVENTORY_DIR / "WEB_GROUNDING_SOURCES.md").write_text("\n".join(web_doc) + "\n", encoding="utf-8")

    status = "ok" if not failures else "fail"
    verification = {
        "status": status,
        "failures": failures,
        "sources": report_rows,
        "flat_pack_rag_files": len(list(FLAT_PACK_DIR.glob("DM_PDF*__04_rag.md"))),
        "section_contract": SECTIONS,
    }
    write_json(INVENTORY_DIR / "verification_report_enhanced_rag.json", verification)

    report_md = ["# Enhanced DecisionMaking RAG Development Plan and Report", ""]
    report_md.append("## Development Plan Applied")
    report_md.extend(
        [
            "1. Keep PDF transcript anchors as the primary source of truth.",
            "2. Convert each final RAG file into a 17-section tutor operating document.",
            "3. Add individualized node cards, example walkthroughs, Solver mappings, misconception banks, and retrieval routes.",
            "4. Add enhanced sidecars for nodes, edges, evidence, and routing.",
            "5. Verify section coverage, DM_PDF06 required node coverage, and evidence anchors.",
        ]
    )
    report_md.append("")
    report_md.append("## Per-PDF Development Result")
    report_md.append("| source_id | title | nodes | examples | routes | low_text_pages |")
    report_md.append("|---|---|---:|---:|---:|---:|")
    for row in report_rows:
        report_md.append(f"| `{row['source_id']}` | {row['title']} | {row['nodes']} | {row['examples']} | {row['routes']} | {row['low_text_pages']} |")
    report_md.append("")
    report_md.append("## Verification")
    report_md.append(f"- status: `{status}`")
    report_md.append(f"- failures: `{len(failures)}`")
    if failures:
        report_md.extend(f"- {failure}" for failure in failures)
    report_md.append("")
    report_md.append("## Residual QC Notes")
    report_md.append("- Low-text pages remain OCR/manual-check candidates, especially formula/table/image-heavy pages.")
    report_md.append("- Web grounding is supplemental and must not override the PDF transcript anchors.")
    (INVENTORY_DIR / "ENHANCED_RAG_DEVELOPMENT_PLAN_AND_REPORT.md").write_text("\n".join(report_md) + "\n", encoding="utf-8")
    return verification


def main() -> None:
    verification = generate()
    print(json.dumps(verification, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
