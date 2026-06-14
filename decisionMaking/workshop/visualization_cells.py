"""DecisionMaking G1 visual lecture generator.

This module turns the G1 problem notebooks into a visual companion pack:

- 32 question-level PNG infographics
- visualization_spec.md
- visualization_checklist.md
- DM_G1_visual_lecture.ipynb

Default stack: numpy, matplotlib, nbformat. No external downloads.
"""

from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / ".mplconfig"))

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle

try:
    import nbformat
except Exception:  # pragma: no cover - notebook generation is optional at import time.
    nbformat = None


ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "visual_assets"
SPEC_PATH = ROOT / "visualization_spec.md"
CHECKLIST_PATH = ROOT / "visualization_checklist.md"
NOTEBOOK_PATH = ROOT / "DM_G1_visual_lecture.ipynb"


def _block(
    block_id: str,
    phase: str,
    question: str,
    title: str,
    source_notebook: str,
    nodes: list[str],
    anchors: list[str],
    purpose: str,
    data: str,
    preprocess: str,
    code_design: str,
    interpretation: str,
    misconception: str,
    checkpoint: str,
    plot: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": block_id,
        "phase": phase,
        "question": question,
        "title": title,
        "source_notebook": source_notebook,
        "nodes": nodes,
        "anchors": anchors,
        "purpose": purpose,
        "data": data,
        "preprocess": preprocess,
        "code_design": code_design,
        "interpretation": interpretation,
        "misconception": misconception,
        "checkpoint": checkpoint,
        "plot": plot,
    }


COMMON_FEASIBLE = {
    "constraints": [(2, 1, 120, "2x1 + x2 <= 120"), (1, 2, 100, "x1 + 2x2 <= 100"), (1, 0, 45, "x1 <= 45")],
    "objective": (5, 4, "z = 5x1 + 4x2"),
    "xlim": (0, 75),
    "ylim": (0, 80),
}


VISUAL_BLOCKS: list[dict[str, Any]] = [
    _block(
        "DM_G1_P0001_Q01",
        "P0001",
        "Q01",
        "표준형 변환 기본",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.simplex_tableau"],
        ["DM_PDF01:p001:L003"],
        "LP 문장을 실행가능영역, slack variable, 초기 BFS로 동시에 보는 그림을 제공한다.",
        "문항의 2변수 LP 계수와 RHS.",
        "제약식을 반평면으로 바꾸고, slack은 각 제약의 남는 거리로 해석한다.",
        "feasible region과 objective line을 한 평면에 그린다.",
        "원점은 slack만 basis인 초기 BFS이고, shaded region이 모든 제약을 동시에 만족하는 영역이다.",
        "slack을 목적함수에 넣거나, 초기 basis에 원변수 x1/x2를 포함하는 오류.",
        "초기 BFS에서 x1=x2=0일 때 각 slack 값은 무엇인가?",
        {"kind": "region", "scenario": "standard_lp", "title": "Standard form: feasible region and initial BFS"},
    ),
    _block(
        "DM_G1_P0001_Q02",
        "P0001",
        "Q02",
        "첫 pivot 선택",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.entering_leaving_variable", "n_DM_PDF01.minimum_ratio_test"],
        ["DM_PDF01:p001:L003"],
        "entering column을 고른 뒤 ratio test가 leaving row를 어떻게 결정하는지 시각화한다.",
        "문항 1의 RHS와 x1 column 계수.",
        "Dantzig rule로 x1을 entering 후보로 두고 RHS / positive column coefficient를 계산한다.",
        "ratio bar chart에서 최소 양수 ratio를 강조한다.",
        "가장 작은 양수 ratio가 먼저 닿는 자원 한계를 뜻하며 leaving variable을 결정한다.",
        "음수나 0 계수 행을 절댓값으로 바꿔 ratio 후보에 넣는 오류.",
        "왜 ratio test는 양수 계수 행만 후보로 보는가?",
        {"kind": "bar", "title": "Minimum ratio test", "labels": ["row1", "row2", "row3"], "values": [60, 100, 45], "highlight": 2, "ylabel": "RHS / entering-column coefficient"},
    ),
    _block(
        "DM_G1_P0001_Q03",
        "P0001",
        "Q03",
        "피벗 연산 구조 설명",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.pivot_operation"],
        ["DM_PDF01:p001:L003"],
        "pivot을 단순 행연산이 아니라 한 BFS에서 인접 BFS로 이동하는 과정으로 보여준다.",
        "문항 1의 feasible region과 첫 pivot 이동.",
        "첫 entering x1, leaving s3를 가정하고 원점에서 x1 방향으로 이동한다.",
        "feasible region 위에 BFS 이동 화살표를 표시한다.",
        "pivot row 정규화와 column 제거는 새 basis에서 해당 변수 하나만 1이 되게 만드는 대수적 장치다.",
        "pivot을 표 계산으로만 외우고, 그래프의 꼭짓점 이동 의미를 놓치는 오류.",
        "첫 pivot 뒤 basis에는 어떤 변수가 들어오고 어떤 slack이 나가는가?",
        {"kind": "region", "scenario": "pivot_path", "title": "Pivot as BFS-to-BFS movement"},
    ),
    _block(
        "DM_G1_P0001_Q04",
        "P0001",
        "Q04",
        "타블로 판정 문제",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.optimality_test", "n_DM_PDF01.multiple_optima"],
        ["DM_PDF01:p002:L003"],
        "최적성 판정 이후 reduced cost 0이 왜 복수 최적해 신호인지 보여준다.",
        "문항의 z-row nonbasic coefficients: x3=0, x4=2, x5=1.",
        "계수를 막대로 놓고 0인 비기저변수를 별도 색으로 표시한다.",
        "reduced cost bar chart와 대안 최적 진입 후보를 표시한다.",
        "개선 가능한 계수가 없으면서 0 reduced cost가 있으면 같은 목적값의 인접해가 가능하다.",
        "Solver가 보여주는 하나의 최적해를 유일해라고 단정하는 오류.",
        "x3의 reduced cost가 0이라는 말은 objective value 관점에서 무슨 뜻인가?",
        {"kind": "bar", "title": "Zero reduced cost and alternate optimum signal", "labels": ["x3", "x4", "x5"], "values": [0, 2, 1], "highlight": 0, "ylabel": "nonbasic coefficient"},
    ),
    _block(
        "DM_G1_P0001_Q05",
        "P0001",
        "Q05",
        "복수 최적해 예제 변형",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.multiple_optima"],
        ["DM_PDF01:p002:L003"],
        "복수 최적해가 전체 feasible region이 아니라 최적 face에만 존재함을 2D로 보여준다.",
        "목적함수가 한 제약 경계와 평행한 illustrative LP.",
        "x+y<=10, x<=8, y<=8 영역에서 x+y objective의 최적 edge를 표시한다.",
        "최적 edge를 굵게 그리고 edge 밖 feasible point는 최적이 아님을 표시한다.",
        "복수 최적해는 최적 face 위의 점들이 같은 값을 갖는다는 뜻이다.",
        "복수 최적해를 '아무 feasible point나 최적'이라고 해석하는 오류.",
        "대안 최적해를 찾으려면 어떤 reduced cost 조건을 봐야 하는가?",
        {"kind": "region", "scenario": "optimal_face", "title": "Multiple optima live on an optimal face"},
    ),
    _block(
        "DM_G1_P0001_Q06",
        "P0001",
        "Q06",
        "비유계 판정",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.unbounded_solution"],
        ["DM_PDF01:p003:L003"],
        "ratio test 후보가 없을 때 objective가 끝없이 개선되는 구조를 2D ray로 보여준다.",
        "개선 방향은 있으나 positive pivot coefficient가 없는 illustrative feasible cone.",
        "feasible cone과 objective improvement ray를 표시한다.",
        "unbounded ray와 missing upper-bound constraint를 함께 표시한다.",
        "개선 가능한 entering variable이 있는데 ratio 후보가 없으면 infeasible이 아니라 unbounded 신호다.",
        "unbounded와 infeasible을 모두 '해가 없다'로 뭉뚱그리는 오류.",
        "비유계 모델에서 현실적으로 빠졌을 가능성이 큰 제약은 무엇인가?",
        {"kind": "region", "scenario": "unbounded", "title": "Unbounded signal: improving ray without ratio candidate"},
    ),
    _block(
        "DM_G1_P0001_Q07",
        "P0001",
        "Q07",
        "오답 진단: ratio test",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.minimum_ratio_test"],
        ["DM_PDF01:p001:L003"],
        "음수 계수를 절댓값으로 바꾸는 오답이 왜 pivot을 망치는지 비교한다.",
        "positive coefficient row와 negative coefficient row의 ratio 처리 비교.",
        "잘못된 절댓값 계산과 올바른 후보 제외를 나란히 배치한다.",
        "wrong vs correct 막대/금지 표시를 만든다.",
        "음수 계수는 entering variable을 늘릴 때 RHS 한계에 먼저 닿는 행이 아니므로 후보가 아니다.",
        "RHS 나눗셈이라는 형태만 보고 부호 의미를 무시하는 오류.",
        "entering variable을 늘릴 때 해당 행의 LHS는 증가하는가, 감소하는가?",
        {"kind": "bar", "title": "Wrong absolute-value ratio vs valid positive-ratio rule", "labels": ["positive row", "negative row"], "values": [40, 25], "highlight": 0, "ylabel": "candidate ratio", "bad_index": 1},
    ),
    _block(
        "DM_G1_P0001_Q08",
        "P0001",
        "Q08",
        "Solver 매핑 문제",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.simplex_tableau"],
        ["DM_PDF01:p001:L003"],
        "LP 모형의 변수/목적/제약을 Excel Solver 셀 구조로 번역한다.",
        "문항의 x1,x2, objective, three constraints.",
        "수식 요소를 changing cells, target cell, constraint LHS/RHS로 분리한다.",
        "Solver layout infographic을 그린다.",
        "Solver는 changing cells를 움직여 target cell을 개선하되 constraint cells가 RHS를 넘지 않게 한다.",
        "RHS와 LHS를 한 셀에 섞거나 target cell을 변수 셀로 착각하는 오류.",
        "constraint LHS cell과 RHS cell은 왜 분리해야 하는가?",
        {"kind": "flow", "title": "LP to Excel Solver mapping", "steps": [["Decision variables"], ["Changing cells: x1, x2"], ["Target cell: 6x1+3x2"], ["Constraint LHS cells"], ["RHS bounds + nonnegativity"]]},
    ),
    _block(
        "DM_G1_P0001_Q09",
        "P0001",
        "Q09",
        "특수 종료 신호 비교",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.optimality_test", "n_DM_PDF01.multiple_optima", "n_DM_PDF01.unbounded_solution", "n_DM_PDF01.two_phase_method"],
        ["DM_PDF01:p002:L003", "DM_PDF01:p003:L003", "DM_PDF01:p005:L001"],
        "최적, 복수 최적, 비유계, infeasible을 종료 신호 흐름도로 구분한다.",
        "타블로 목적행, ratio candidate, Phase I objective 조건.",
        "판정 질문을 순서대로 배치한다.",
        "termination decision tree를 만든다.",
        "종료 신호는 한 줄 문장 암기가 아니라 '개선 가능성, 대안 진입, ratio 후보, Phase I 값'의 조합이다.",
        "복수 최적과 비유계, infeasible 신호를 reduced cost 하나로만 판정하는 오류.",
        "Phase I w*>0 신호는 왜 unbounded가 아니라 infeasible인가?",
        {"kind": "flow", "title": "Special termination signals", "steps": [["Tableau status"], ["No improving coefficient?", "Improving coefficient?"], ["Zero reduced cost?", "No ratio candidate?"], ["Multiple optima", "Unbounded", "Phase I w*>0 -> Infeasible"]]},
    ),
    _block(
        "DM_G1_P0001_Q10",
        "P0001",
        "Q10",
        "최종 요약 문제",
        "ipynb/DM_G1_P0001.ipynb",
        ["n_DM_PDF01.simplex_tableau"],
        ["DM_PDF01:p001:L003"],
        "현실 언어, 타블로 언어, Solver 언어가 같은 simplex 과정을 가리킴을 연결한다.",
        "BFS, entering, leaving, ratio, pivot, reduced cost, unbounded 핵심어.",
        "세 언어를 삼각형 구조로 배치하고 중심에 simplex iteration을 둔다.",
        "three-language concept map을 만든다.",
        "같은 절차를 자원 배분 이동, basis 교체, Solver 반복으로 번역할 수 있어야 한다.",
        "용어를 따로 외우고 서로 번역하지 못하는 오류.",
        "BFS 이동을 현실 언어로 한 문장으로 말하면 무엇인가?",
        {"kind": "flow", "title": "Three languages of simplex", "steps": [["Reality: resource limits"], ["Tableau: BFS and pivot"], ["Solver: cells and constraints"], ["Same process: improve objective safely"]]},
    ),
    _block(
        "DM_G1_P0002_Q01",
        "P0002",
        "Q01",
        "surplus/artificial variable 도입 판별",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.surplus_artificial_variable"],
        ["DM_PDF01:p004:L003"],
        "<=, >=, = 제약마다 어떤 변수가 필요한지 한눈에 구분한다.",
        "세 가지 제약 유형.",
        "부등호 방향을 등식화 규칙으로 변환한다.",
        "constraint-type conversion infographic을 그린다.",
        "<=에는 slack, >=에는 surplus 제거와 artificial 추가, =에는 basis 확보용 artificial이 필요하다.",
        "surplus를 slack처럼 더하거나 equality에 basis가 있다고 착각하는 오류.",
        "왜 >= 제약에서는 surplus를 빼야 하는가?",
        {"kind": "flow", "title": "Constraint type to standard form", "steps": [["<= row"], ["add slack +s"], [">= row"], ["subtract surplus -s and add artificial +a"], ["= row"], ["add artificial +a if no basis"]]},
    ),
    _block(
        "DM_G1_P0002_Q02",
        "P0002",
        "Q02",
        "2단계법 문제 변형",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.two_phase_method"],
        ["DM_PDF01:p004:L002", "DM_PDF01:p005:L001"],
        "Phase I에서 feasible basis를 만들고 Phase II에서 원목적함수로 돌아가는 절차를 보여준다.",
        "slack/surplus/artificial이 섞인 LP.",
        "초기 basis 후보와 Phase I objective w를 분리한다.",
        "two-phase pipeline을 그린다.",
        "Phase I은 원문제 최적화가 아니라 artificial 합을 0으로 만들 수 있는지 검사하는 단계다.",
        "Phase I objective를 원목적함수 z와 혼동하는 오류.",
        "Phase II로 넘어가기 위한 정확한 조건은 무엇인가?",
        {"kind": "flow", "title": "Two-phase method pipeline", "steps": [["Original constraints"], ["Standard form"], ["Artificial basis"], ["Phase I: minimize w=sum artificial"], ["w*=0?"], ["Phase II: restore original objective"]]},
    ),
    _block(
        "DM_G1_P0002_Q03",
        "P0002",
        "Q03",
        "Phase I 목적함수 해석",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.two_phase_method"],
        ["DM_PDF01:p006:L001"],
        "w=0이 원목적값이 아니라 feasibility 신호임을 분리한다.",
        "Phase I objective w와 original objective z.",
        "두 개의 계기판을 분리해 표시한다.",
        "w gauge와 z gauge를 나란히 그린다.",
        "w=0은 원문제 feasible basis를 얻었다는 뜻이고, z 최적값은 Phase II에서 구한다.",
        "w=0을 z=0 또는 최적 목적값 0으로 착각하는 오류.",
        "w=0 이후에도 왜 Phase II가 필요한가?",
        {"kind": "bar", "title": "Phase I w=0 is not original z=0", "labels": ["Phase I w", "Original z"], "values": [0, 1], "highlight": 0, "ylabel": "meaning scale"},
    ),
    _block(
        "DM_G1_P0002_Q04",
        "P0002",
        "Q04",
        "artificial variable 최종해 판정",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.two_phase_method", "n_DM_PDF05.artificial_variable"],
        ["DM_PDF01:p006:L001", "DM_PDF05:p007:L003"],
        "artificial이 0이면 feasible, 양수로 남으면 infeasible이라는 판정을 비교한다.",
        "상황 A: w*=0 artificial nonbasic, 상황 B: w*=3 artificial positive.",
        "두 상황을 side-by-side로 배치한다.",
        "feasible gate infographic을 만든다.",
        "artificial이 양수로 남으면 원 제약만으로는 그 점을 만들 수 없다.",
        "artificial variable을 실제 의사결정변수처럼 해석하는 오류.",
        "artificial positive가 의미하는 현실적 결핍은 무엇인가?",
        {"kind": "bar", "title": "Artificial variable final-state test", "labels": ["Case A artificial sum", "Case B artificial sum"], "values": [0, 3], "highlight": 0, "ylabel": "sum of artificial variables"},
    ),
    _block(
        "DM_G1_P0002_Q05",
        "P0002",
        "Q05",
        "식단문제 축소형",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.diet_two_phase"],
        ["DM_PDF01:p007:L001", "DM_PDF01:p008:L001"],
        "식품량 변수, 영양소 요구량 제약, 최소비용 objective를 행렬로 시각화한다.",
        "식품 3개, 비타민 A/C 함량표, 요구량.",
        "nutrient matrix와 RHS requirement를 분리한다.",
        "matrix heatmap과 requirement bars를 그린다.",
        "식단문제는 비용을 줄이면서 각 영양소의 최소 요구량 이상을 만족하는 >= 제약 문제다.",
        "영양소 제약 방향을 <=로 쓰거나 비용 최소화를 최대화로 착각하는 오류.",
        "각 식품량 xj는 무엇을 결정하는 변수인가?",
        {"kind": "matrix", "title": "Diet matrix: foods to nutrients", "matrix": [[10, 20, 10], [0, 10, 30]], "rows": ["Vitamin A", "Vitamin C"], "cols": ["Food1", "Food2", "Food3"]},
    ),
    _block(
        "DM_G1_P0002_Q06",
        "P0002",
        "Q06",
        "Phase II 전환 구조",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.two_phase_method"],
        ["DM_PDF01:p006:L001", "DM_PDF01:p009:L001"],
        "Phase I basis를 유지하되 artificial 열을 제거하고 원목적함수로 전환하는 구조를 보여준다.",
        "Phase I final tableau와 Phase II start basis.",
        "artificial columns 제거와 original objective 복귀를 단계화한다.",
        "Phase I to Phase II transition flow를 그린다.",
        "Phase I이 찾아준 feasible basis는 Phase II의 출발점으로 재사용된다.",
        "Phase I이 끝나면 basis를 버리고 처음부터 다시 시작한다고 생각하는 오류.",
        "Phase II 시작 전 tableau에서 제거해야 하는 열은 무엇인가?",
        {"kind": "flow", "title": "Phase I basis carried into Phase II", "steps": [["Phase I final basis"], ["Artificial variables = 0"], ["Drop artificial columns"], ["Restore original objective"], ["Continue simplex"]]},
    ),
    _block(
        "DM_G1_P0002_Q07",
        "P0002",
        "Q07",
        "오답 진단: surplus 부호",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.surplus_artificial_variable"],
        ["DM_PDF01:p004:L003"],
        ">= 제약에서 surplus는 초과량이므로 빼야 한다는 부호 직관을 그림으로 보인다.",
        "2x1+x2 >= 10의 LHS와 RHS.",
        "LHS = RHS + surplus를 LHS - surplus = RHS로 재배열한다.",
        "number-line/excess diagram을 만든다.",
        "surplus는 기준 RHS를 넘은 초과량이므로 좌변에서 빼야 등식이 된다.",
        "surplus를 slack처럼 더하는 오류.",
        "LHS가 RHS보다 3만큼 크면 surplus 값은 얼마이고 등식은 어떻게 되는가?",
        {"kind": "flow", "title": "Surplus sign for >= constraints", "steps": [["LHS >= RHS"], ["LHS = RHS + surplus"], ["LHS - surplus = RHS"], ["Add artificial for initial basis"]]},
    ),
    _block(
        "DM_G1_P0002_Q08",
        "P0002",
        "Q08",
        "Solver 매핑 문제",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.diet_two_phase"],
        ["DM_PDF01:p007:L001"],
        "식단형 최소화 문제를 Solver 셀 배치로 시각화한다.",
        "식품량 변수, 총비용, 영양소 섭취량 LHS, 요구량 RHS.",
        "food amount cells, cost SUMPRODUCT, nutrient LHS cells를 분리한다.",
        "diet Solver layout infographic을 만든다.",
        "Solver에서는 >= constraint를 영양소 섭취량 셀 >= 요구량 셀로 입력한다.",
        "수동 2단계법의 artificial 변수를 Solver changing cells에 넣는 오류.",
        "Solver의 changing cells에는 어떤 값들이 들어가야 하는가?",
        {"kind": "flow", "title": "Diet LP to Solver cells", "steps": [["Changing cells: food amounts"], ["Target: total cost"], ["Nutrient LHS cells"], [">= requirement RHS"], ["Simplex LP minimizes cost"]]},
    ),
    _block(
        "DM_G1_P0002_Q09",
        "P0002",
        "Q09",
        "Phase I tableau 해석",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.two_phase_method"],
        ["DM_PDF01:p006:L001"],
        "Phase I 마지막 타블로가 말해주는 것과 아직 말해주지 않는 것을 분리한다.",
        "objective value w=0, artificial variables nonbasic.",
        "meaning / not-yet / next-action 세 칸으로 나눈다.",
        "Phase I interpretation board를 만든다.",
        "이 상태는 feasibility 확보이지 original optimum 확보가 아니다.",
        "Phase I 마지막 값을 원문제 최적값으로 보고 멈추는 오류.",
        "이 상태에서 다음 simplex tableau에는 어떤 objective row가 들어가야 하는가?",
        {"kind": "flow", "title": "Phase I final tableau interpretation", "steps": [["w=0"], ["Artificial nonbasic"], ["Original feasible basis found"], ["Not original optimum yet"], ["Start Phase II"]]},
    ),
    _block(
        "DM_G1_P0002_Q10",
        "P0002",
        "Q10",
        "최종 종합 문제",
        "ipynb/DM_G1_P0002.ipynb",
        ["n_DM_PDF01.surplus_artificial_variable", "n_DM_PDF01.two_phase_method"],
        ["DM_PDF01:p004:L003", "DM_PDF01:p005:L001", "DM_PDF01:p006:L001"],
        "slack, surplus, artificial, Phase I/II의 관계를 개념 그래프로 묶는다.",
        "2단계법 핵심 용어 목록.",
        "변수 유형과 Phase 흐름을 방향 그래프로 배치한다.",
        "concept graph를 그린다.",
        "표준형 변환은 basis 확보 문제로 이어지고, artificial이 0이 되는지가 feasibility 판정이다.",
        "각 변수를 등식화 장치와 feasibility 장치로 구분하지 못하는 오류.",
        "slack과 artificial의 역할 차이를 한 문장으로 말하면?",
        {"kind": "flow", "title": "Two-phase concept graph", "steps": [["<= -> slack"], [">= -> surplus + artificial", "= -> artificial"], ["Phase I: remove artificial"], ["w*=0 -> feasible basis"], ["Phase II: optimize original z"]]},
    ),
    _block(
        "DM_G1_P0003_Q01",
        "P0003",
        "Q01",
        "min 문제를 Big-M용 max 형태로 바꾸기",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.big_m_method", "n_DM_PDF05.artificial_variable"],
        ["DM_PDF05:p002:L002", "DM_PDF05:p003:L009", "DM_PDF05:p003:L016"],
        "min-to-max 변환과 artificial penalty 부호를 같은 축에서 확인한다.",
        "최소화 목적함수, >= 제약, artificial variables.",
        "min Z를 max -Z로 바꾸고 artificial이 커질수록 objective가 나빠지도록 표시한다.",
        "objective direction and penalty sign diagram을 만든다.",
        "Big-M 부호는 목적 방향에 따라 'artificial을 벌주는가'라는 현실 문장으로 확인한다.",
        "max 형태에서 artificial에 보상을 주는 부호를 쓰는 오류.",
        "artificial이 커질수록 max objective는 좋아져야 하는가, 나빠져야 하는가?",
        {"kind": "flow", "title": "Min-to-Max and Big-M penalty sign", "steps": [["Min Z"], ["Max -Z"], [">= constraints need -s + r"], ["Artificial r must be punished"], ["Use M sign consistent with max convention"]]},
    ),
    _block(
        "DM_G1_P0003_Q02",
        "P0003",
        "Q02",
        "artificial variable 동치 조건",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.artificial_variable", "n_DM_PDF05.big_m_method"],
        ["DM_PDF05:p003:L015", "DM_PDF05:p007:L003"],
        "r=0일 때만 artificial 확장공간에서 원문제 공간으로 돌아온다는 점을 보여준다.",
        "r1, r2 artificial variable 상태.",
        "r 축을 원문제 평면 바깥 방향으로 표시한다.",
        "original plane vs artificial dimension diagram을 만든다.",
        "r>0은 원문제에 없는 보조축을 사용한 해이므로 원문제 feasible solution이 아니다.",
        "r>0이 작으면 괜찮다고 해석하는 오류.",
        "왜 final artificial values must be zero인가?",
        {"kind": "bar", "title": "Artificial variables must return to zero", "labels": ["r1 final", "r2 final", "allowed target"], "values": [0, 2, 0], "highlight": 0, "ylabel": "artificial value"},
    ),
    _block(
        "DM_G1_P0003_Q03",
        "P0003",
        "Q03",
        "Big-M과 2단계법 비교",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.big_m_method", "n_DM_PDF01.two_phase_method"],
        ["DM_PDF05:p004:L002", "DM_PDF01:p005:L001"],
        "두 방법이 같은 목적을 다른 절차로 수행함을 두 레인으로 비교한다.",
        "Two-phase와 Big-M 알고리즘 단계.",
        "공통 목표와 차이점을 parallel lane flow로 정리한다.",
        "comparison flowchart를 만든다.",
        "두 방법 모두 artificial을 0으로 만들려 하지만, 2단계법은 별도 Phase I이고 Big-M은 penalty를 넣는다.",
        "Big-M과 2단계법이 완전히 다른 문제를 푼다고 생각하는 오류.",
        "두 방법의 공통 목표는 무엇인가?",
        {"kind": "flow", "title": "Two-phase vs Big-M", "steps": [["Artificial variables introduced"], ["Two-phase: separate Phase I"], ["Big-M: penalty in objective"], ["Common goal: artificial = 0"], ["Then optimize original problem"]]},
    ),
    _block(
        "DM_G1_P0003_Q04",
        "P0003",
        "Q04",
        "Big-M 오답 진단",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.big_m_method"],
        ["DM_PDF05:p003:L016"],
        "+M이 artificial을 보상하는 부호가 될 때 왜 위험한지 시각화한다.",
        "wrong reward vs correct penalty for artificial r.",
        "r 값 증가에 따른 objective effect를 두 선으로 비교한다.",
        "penalty sign line plot을 만든다.",
        "max에서 artificial이 커질수록 objective가 좋아지는 식은 artificial 제거 목적과 반대다.",
        "M이 크면 부호가 어떻게 되든 알아서 빠진다고 생각하는 오류.",
        "M의 크기보다 먼저 확인해야 하는 것은 무엇인가?",
        {"kind": "line", "title": "Big-M sign error: reward vs penalty", "series": {"reward +Mr": [0, 1, 2, 3], "penalty -Mr": [0, -1, -2, -3]}, "xlabel": "artificial r", "ylabel": "objective effect / M"},
    ),
    _block(
        "DM_G1_P0003_Q05",
        "P0003",
        "Q05",
        "식단문제와 비타민 가격 쌍대 직관",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.dual_problem"],
        ["DM_PDF05:p014:L001", "DM_PDF05:p018:L001", "DM_PDF05:p019:L001"],
        "식품량 primal과 영양소 가격 dual을 bipartite graph로 연결한다.",
        "foods, nutrients, vitamin prices.",
        "식품-영양소 행렬을 그래프로 바꾼다.",
        "bipartite network를 그린다.",
        "primal 변수는 식품량, dual 변수는 영양소 요구량의 잠재가격으로 해석될 수 있다.",
        "dual variable을 항상 물리적 생산량으로 해석하는 오류.",
        "dual 변수는 원문제의 무엇에 대응하는가?",
        {"kind": "network", "title": "Diet primal-dual intuition", "left": ["Food1", "Food2", "Food3"], "right": ["Vitamin A price", "Vitamin C price"], "edges": [(0, 0), (1, 0), (2, 0), (1, 1), (2, 1)]},
    ),
    _block(
        "DM_G1_P0003_Q06",
        "P0003",
        "Q06",
        "primal-dual 대응표 작성",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.dual_problem", "n_DM_PDF05.primal_dual_mapping"],
        ["DM_PDF05:p023:L002"],
        "primal 제약은 dual 변수, primal 변수는 dual 제약으로 넘어가는 대응을 표로 시각화한다.",
        "4 constraints, 2 variables primal LP.",
        "coefficient matrix transpose 관점으로 배열한다.",
        "matrix transposition heatmap을 만든다.",
        "primal constraint 수가 dual variable 수가 되고, primal variable 수가 dual constraint 수가 된다.",
        "dual variable 수를 primal variable 수와 같게 잡는 오류.",
        "dual에는 변수 y가 몇 개 필요한가?",
        {"kind": "matrix", "title": "Primal-dual mapping as matrix transpose", "matrix": [[8, 4], [4, 4], [4, 0], [0, 1]], "rows": ["c1", "c2", "c3", "c4"], "cols": ["x1", "x2"]},
    ),
    _block(
        "DM_G1_P0003_Q07",
        "P0003",
        "Q07",
        "약쌍대성 판정",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.weak_duality", "n_DM_PDF05.strong_duality"],
        ["DM_PDF05:p024:L001"],
        "max primal feasible value가 min dual feasible value를 넘지 못한다는 bound 구조를 숫자선으로 보여준다.",
        "Z=700, W=1540.",
        "number line에 primal lower bound와 dual upper bound를 배치한다.",
        "duality gap number line을 만든다.",
        "Z<=W이면 weak duality와 일치하며, Z=W이면 optimality certificate가 된다.",
        "Z<W이면 둘 중 하나가 infeasible이라고 판정하는 오류.",
        "Z=W가 되면 왜 양쪽 최적해라고 말할 수 있는가?",
        {"kind": "line", "title": "Weak duality: primal value <= dual value", "series": {"primal Z": [700, 700], "dual W": [1540, 1540]}, "xlabel": "bound marker", "ylabel": "objective value"},
    ),
    _block(
        "DM_G1_P0003_Q08",
        "P0003",
        "Q08",
        "강쌍대성과 최적성",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.weak_duality", "n_DM_PDF05.strong_duality", "n_DM_PDF05.four_duality_cases"],
        ["DM_PDF05:p024:L001", "DM_PDF05:p025:L001"],
        "weak duality, strong duality, 4 cases를 최적성 판정 지도에 배치한다.",
        "A/B/C 문장 유형.",
        "feasible/bounded 상태와 objective equality를 판정 순서로 둔다.",
        "duality case map을 만든다.",
        "strong duality는 feasible optimum pair의 objective equality이고, unbounded는 반대쪽 infeasible 가능성과 연결된다.",
        "weak duality의 부등식만 보고 최적성을 곧바로 결론내는 오류.",
        "최적성 certificate로 쓰려면 무엇이 같아야 하는가?",
        {"kind": "flow", "title": "Duality case map", "steps": [["Feasible values"], ["Weak duality: Z <= W"], ["If Z = W"], ["Strong duality certificate"], ["If primal unbounded"], ["Dual infeasible case"]]},
    ),
    _block(
        "DM_G1_P0003_Q09",
        "P0003",
        "Q09",
        "상보여유 기초 판정",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.complementary_slackness", "n_DM_PDF02.shadow_price"],
        ["DM_PDF05:p027:L001", "DM_PDF05:p030:L002"],
        "slack>0과 positive dual variable이 동시에 있으면 상보여유를 위반함을 보인다.",
        "constraint 2 slack=40, y2=3.",
        "slack*y=0 조건을 곱셈 막대로 표시한다.",
        "complementary slackness violation chart를 만든다.",
        "여유가 있는 자원은 추가 가치가 0이어야 하므로 대응 dual variable은 0이어야 한다.",
        "binding constraint와 positive shadow price의 방향을 거꾸로 이해하는 오류.",
        "slack=40이면 y2는 어떤 값이어야 하는가?",
        {"kind": "bar", "title": "Complementary slackness check: slack*y must be zero", "labels": ["slack2", "y2", "product"], "values": [40, 3, 120], "highlight": 2, "ylabel": "value"},
    ),
    _block(
        "DM_G1_P0003_Q10",
        "P0003",
        "Q10",
        "reduced cost와 shadow price 연결",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF02.reduced_cost", "n_DM_PDF02.shadow_price"],
        ["DM_PDF05:p032:L002"],
        "변수 질문은 reduced cost, RHS/자원 질문은 shadow price로 갈라진다는 점을 지도화한다.",
        "variable-entry question and RHS-value question.",
        "질문 유형을 두 갈래로 분류한다.",
        "question routing flow를 만든다.",
        "reduced cost는 변수/활동의 진입 조건이고 shadow price는 제약 RHS 변화의 가치다.",
        "둘을 모두 '한계값'으로만 보고 같은 값처럼 해석하는 오류.",
        "새 활동을 시작하려면 어떤 열을 봐야 하는가?",
        {"kind": "flow", "title": "Reduced cost vs shadow price routing", "steps": [["User question"], ["Variable/activity question"], ["Reduced cost"], ["RHS/resource question"], ["Shadow price"], ["Allowable range"]]},
    ),
    _block(
        "DM_G1_P0003_Q11",
        "P0003",
        "Q11",
        "sensitivity report 브릿지 판별",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF02.reduced_cost", "n_DM_PDF02.shadow_price", "n_DM_PDF05.shadow_price_dual_solution"],
        ["DM_PDF05:p032:L002", "DM_PDF02:p026:L007", "DM_PDF02:p026:L009"],
        "A~D 질문을 sensitivity report의 열로 라우팅한다.",
        "reduced cost, shadow price, allowable range 질문 유형.",
        "질문을 변수/제약/RHS/범위로 분류한다.",
        "sensitivity routing board를 만든다.",
        "sensitivity report는 최종 타블로와 duality 해석을 Solver 출력 형태로 보여준다.",
        "allowable range를 shadow price 자체와 혼동하는 오류.",
        "shadow price를 적용하기 전에 반드시 확인해야 하는 범위는 무엇인가?",
        {"kind": "flow", "title": "Sensitivity report routing", "steps": [["A,C: variable entry"], ["Reduced Cost column"], ["B: one more resource"], ["Shadow Price column"], ["D: valid range"], ["Allowable Increase/Decrease"]]},
    ),
    _block(
        "DM_G1_P0003_Q12",
        "P0003",
        "Q12",
        "최종 종합 문제",
        "ipynb/DM_G1_P0003.ipynb",
        ["n_DM_PDF05.artificial_variable", "n_DM_PDF05.big_m_method", "n_DM_PDF05.dual_problem", "n_DM_PDF05.complementary_slackness", "n_DM_PDF02.shadow_price"],
        ["DM_PDF05:p003:L009", "DM_PDF05:p023:L002", "DM_PDF05:p024:L001", "DM_PDF05:p027:L001", "DM_PDF05:p032:L002"],
        "artificial variable에서 sensitivity report까지 이어지는 전체 개념 사슬을 하나의 지도에 담는다.",
        "P0003 핵심 노드 chain.",
        "개념 노드를 순서 그래프로 배치하고 각 edge의 의미를 표시한다.",
        "final concept graph를 만든다.",
        "Big-M은 artificial 제거, duality는 제약의 가격 해석, sensitivity는 최적해 이후 변화 해석으로 이어진다.",
        "Big-M, duality, sensitivity를 별개 암기 단원으로 분리하는 오류.",
        "왜 Big-M 이후 duality를 배우면 sensitivity report 해석이 쉬워지는가?",
        {"kind": "flow", "title": "Artificial -> Big-M -> Duality -> Sensitivity", "steps": [["Artificial variable"], ["Big-M penalty"], ["Primal-dual mapping"], ["Weak/Strong duality"], ["Complementary slackness"], ["Sensitivity report"]]},
    ),
]


def _wrap(text: str, width: int = 24) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)


def _draw_box(ax: plt.Axes, x: float, y: float, w: float, h: float, text: str, fc: str = "#f7f7f2", ec: str = "#2f3a3d") -> None:
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=1.6, joinstyle="round"))
    ax.text(x + w / 2, y + h / 2, _wrap(text, 19), ha="center", va="center", fontsize=9.4, color="#1d2528")


def _draw_arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], color: str = "#2b6cb0") -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, linewidth=1.7, color=color))


def _render_flow(block: dict[str, Any], path: Path) -> None:
    steps = block["plot"]["steps"]
    n_rows = len(steps)
    max_cols = max(len(row) for row in steps)
    fig, ax = plt.subplots(figsize=(12, max(5, n_rows * 1.08)))
    ax.set_xlim(0, max_cols * 3.2)
    ax.set_ylim(0, n_rows * 1.35 + 0.8)
    ax.axis("off")
    ax.set_title(block["plot"]["title"], fontsize=15, weight="bold", pad=18)
    colors = ["#e7f0fd", "#e9f7ef", "#fff4d6", "#fce8e6", "#ece7fb", "#e8f6f8"]
    centers_by_row: list[list[tuple[float, float]]] = []
    for r, row in enumerate(steps):
        y = n_rows * 1.35 - r * 1.35
        total_w = len(row) * 2.4 + (len(row) - 1) * 0.55
        start_x = (max_cols * 3.2 - total_w) / 2
        centers = []
        for c, label in enumerate(row):
            x = start_x + c * 2.95
            _draw_box(ax, x, y - 0.45, 2.4, 0.78, str(label), fc=colors[(r + c) % len(colors)])
            centers.append((x + 1.2, y - 0.06))
        centers_by_row.append(centers)
    for r in range(n_rows - 1):
        for a in centers_by_row[r]:
            for b in centers_by_row[r + 1]:
                if len(centers_by_row[r]) == 1 or len(centers_by_row[r + 1]) == 1 or abs(a[0] - b[0]) < 1.7:
                    _draw_arrow(ax, (a[0], a[1] - 0.44), (b[0], b[1] + 0.44))
    ax.text(0.02, 0.02, "Visual cue: follow arrows as modeling or algorithm decisions.", transform=ax.transAxes, fontsize=9, color="#5c666a")
    _save(fig, path)


def _render_bar(block: dict[str, Any], path: Path) -> None:
    plot = block["plot"]
    labels = plot["labels"]
    values = np.array(plot["values"], dtype=float)
    x = np.arange(len(labels))
    colors = ["#89b4fa"] * len(labels)
    highlight = plot.get("highlight")
    if highlight is not None:
        colors[highlight] = "#f97373"
    if plot.get("bad_index") is not None:
        colors[plot["bad_index"]] = "#9ca3af"
    fig, ax = plt.subplots(figsize=(10, 5.8))
    bars = ax.bar(x, values, color=colors, edgecolor="#243238", linewidth=1.1)
    ax.axhline(0, color="#243238", linewidth=1)
    ax.set_title(plot["title"], fontsize=15, weight="bold")
    ax.set_ylabel(plot.get("ylabel", "value"))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0)
    for i, (bar, value) in enumerate(zip(bars, values)):
        ax.text(bar.get_x() + bar.get_width() / 2, value + (0.04 * (values.max() - values.min() + 1)), f"{value:g}", ha="center", va="bottom", fontsize=10)
        if i == plot.get("bad_index"):
            ax.text(bar.get_x() + bar.get_width() / 2, max(values.max(), 1) * 0.82, "exclude", ha="center", va="center", fontsize=10, color="#7f1d1d", weight="bold")
    ax.grid(axis="y", alpha=0.25)
    ax.text(0.01, -0.18, "Interpretation: compare values by decision rule, not by arithmetic alone.", transform=ax.transAxes, fontsize=9, color="#5c666a")
    _save(fig, path)


def _feasible_mask(x: np.ndarray, y: np.ndarray, constraints: list[tuple[float, float, float, str]]) -> np.ndarray:
    mask = np.ones_like(x, dtype=bool)
    for a, b, rhs, _ in constraints:
        mask &= a * x + b * y <= rhs + 1e-9
    mask &= x >= 0
    mask &= y >= 0
    return mask


def _plot_constraints(ax: plt.Axes, constraints: list[tuple[float, float, float, str]], xlim: tuple[float, float], ylim: tuple[float, float]) -> None:
    xs = np.linspace(xlim[0], xlim[1], 400)
    for a, b, rhs, label in constraints:
        if abs(b) > 1e-12:
            ys = (rhs - a * xs) / b
            ax.plot(xs, ys, linewidth=1.5, label=label)
        elif abs(a) > 1e-12:
            ax.axvline(rhs / a, linewidth=1.5, label=label)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.grid(alpha=0.22)
    ax.legend(fontsize=8, loc="upper right")


def _render_region(block: dict[str, Any], path: Path) -> None:
    scenario = block["plot"]["scenario"]
    fig, ax = plt.subplots(figsize=(8.6, 7.2))
    ax.set_title(block["plot"]["title"], fontsize=15, weight="bold")
    if scenario in {"standard_lp", "pivot_path"}:
        constraints = COMMON_FEASIBLE["constraints"]
        xlim = COMMON_FEASIBLE["xlim"]
        ylim = COMMON_FEASIBLE["ylim"]
        xg, yg = np.meshgrid(np.linspace(*xlim, 420), np.linspace(*ylim, 420))
        mask = _feasible_mask(xg, yg, constraints)
        ax.contourf(xg, yg, mask.astype(float), levels=[0.5, 1.5], colors=["#d7f2e3"], alpha=0.9)
        _plot_constraints(ax, constraints, xlim, ylim)
        ax.scatter([0], [0], s=80, color="#111827", zorder=5)
        ax.annotate("initial BFS\n(slacks basic)", (0, 0), xytext=(8, 9), arrowprops={"arrowstyle": "->"}, fontsize=9)
        for c in [160, 260, 335]:
            xs = np.linspace(*xlim, 200)
            ys = (c - 5 * xs) / 4
            ax.plot(xs, ys, "--", color="#8b5cf6", alpha=0.55)
        if scenario == "pivot_path":
            pts = np.array([[0, 0], [45, 0], [45, 27.5]])
            ax.plot(pts[:, 0], pts[:, 1], "-o", color="#dc2626", linewidth=2.5, markersize=6)
            ax.annotate("1st pivot:\nx1 enters, s3 leaves", (45, 0), xytext=(48, 12), arrowprops={"arrowstyle": "->"}, fontsize=9)
            ax.annotate("next adjacent BFS", (45, 27.5), xytext=(30, 45), arrowprops={"arrowstyle": "->"}, fontsize=9)
    elif scenario == "optimal_face":
        xlim = (0, 11)
        ylim = (0, 11)
        poly = np.array([[0, 0], [8, 0], [8, 2], [2, 8], [0, 8]])
        ax.add_patch(Polygon(poly, closed=True, facecolor="#d7f2e3", edgecolor="#25543d", alpha=0.9, linewidth=1.8))
        ax.plot([2, 8], [8, 2], color="#dc2626", linewidth=5, label="optimal face: x1+x2=10")
        ax.scatter([4, 6, 5], [6, 4, 3], s=[70, 70, 70], color=["#dc2626", "#dc2626", "#2563eb"])
        ax.annotate("optimal", (4, 6), xytext=(1.2, 9), arrowprops={"arrowstyle": "->"}, fontsize=9)
        ax.annotate("feasible but not optimal", (5, 3), xytext=(5.7, 1.7), arrowprops={"arrowstyle": "->"}, fontsize=9)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xlabel("x1")
        ax.set_ylabel("x2")
        ax.grid(alpha=0.22)
        ax.legend(fontsize=8)
    elif scenario == "unbounded":
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        poly = np.array([[0, 0], [10, 0], [10, 7], [4, 4], [0, 2]])
        ax.add_patch(Polygon(poly, closed=True, facecolor="#fde9c8", edgecolor="#92400e", alpha=0.95, linewidth=1.8))
        ax.arrow(3, 2, 6, 2.8, width=0.05, head_width=0.35, color="#dc2626", length_includes_head=True)
        ax.text(5.1, 5.3, "improving ray\n(no leaving row)", fontsize=10, color="#7f1d1d")
        ax.text(0.4, 0.45, "Feasible region keeps extending\nin objective-improving direction.", fontsize=9)
        ax.set_xlabel("entering variable direction")
        ax.set_ylabel("other variable")
        ax.grid(alpha=0.22)
    ax.text(0.01, -0.12, "Observation: shaded area = feasible set; arrows/edges show the simplex meaning.", transform=ax.transAxes, fontsize=9, color="#5c666a")
    _save(fig, path)


def _render_matrix(block: dict[str, Any], path: Path) -> None:
    plot = block["plot"]
    mat = np.array(plot["matrix"], dtype=float)
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    im = ax.imshow(mat, cmap="Blues")
    ax.set_title(plot["title"], fontsize=15, weight="bold")
    ax.set_xticks(np.arange(len(plot["cols"])))
    ax.set_xticklabels(plot["cols"])
    ax.set_yticks(np.arange(len(plot["rows"])))
    ax.set_yticklabels(plot["rows"])
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, f"{mat[i, j]:g}", ha="center", va="center", color="#111827", fontsize=11, weight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.text(0.01, -0.16, "Interpretation: rows and columns tell which variables feed which constraints.", transform=ax.transAxes, fontsize=9, color="#5c666a")
    _save(fig, path)


def _render_network(block: dict[str, Any], path: Path) -> None:
    plot = block["plot"]
    left = plot["left"]
    right = plot["right"]
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    ax.axis("off")
    ax.set_title(plot["title"], fontsize=15, weight="bold")
    y_left = np.linspace(0.78, 0.22, len(left))
    y_right = np.linspace(0.72, 0.28, len(right))
    left_pos = [(0.22, y) for y in y_left]
    right_pos = [(0.78, y) for y in y_right]
    for i, (x, y) in enumerate(left_pos):
        _draw_box(ax, x - 0.12, y - 0.055, 0.24, 0.11, left[i], fc="#e7f0fd")
    for i, (x, y) in enumerate(right_pos):
        _draw_box(ax, x - 0.14, y - 0.055, 0.28, 0.11, right[i], fc="#fff4d6")
    for li, ri in plot["edges"]:
        _draw_arrow(ax, (left_pos[li][0] + 0.12, left_pos[li][1]), (right_pos[ri][0] - 0.14, right_pos[ri][1]), color="#64748b")
    ax.text(0.5, 0.08, "Primal quantities connect to dual prices through constraint coefficients.", ha="center", fontsize=9, color="#5c666a")
    _save(fig, path)


def _render_line(block: dict[str, Any], path: Path) -> None:
    plot = block["plot"]
    fig, ax = plt.subplots(figsize=(9, 5.7))
    ax.set_title(plot["title"], fontsize=15, weight="bold")
    for name, ys in plot["series"].items():
        ys_arr = np.array(ys, dtype=float)
        xs = np.arange(len(ys_arr)) if "r" not in plot.get("xlabel", "") else np.arange(len(ys_arr))
        ax.plot(xs, ys_arr, marker="o", linewidth=2.4, label=name)
    ax.set_xlabel(plot.get("xlabel", "x"))
    ax.set_ylabel(plot.get("ylabel", "y"))
    ax.grid(alpha=0.25)
    ax.legend()
    if "duality" in plot["title"].lower():
        ax.fill_between([0, 1], [700, 700], [1540, 1540], color="#dbeafe", alpha=0.55)
        ax.text(0.5, 1100, "duality gap", ha="center", va="center", fontsize=11, color="#1e3a8a")
    ax.text(0.01, -0.16, "Observation: compare direction and gap before applying the decision rule.", transform=ax.transAxes, fontsize=9, color="#5c666a")
    _save(fig, path)


def render_block(block: dict[str, Any], asset_dir: Path = ASSET_DIR) -> Path:
    filename = f"{block['id']}__{block['title'].replace('/', '_').replace(' ', '_')}.png"
    path = asset_dir / filename
    kind = block["plot"]["kind"]
    if kind == "flow":
        _render_flow(block, path)
    elif kind == "bar":
        _render_bar(block, path)
    elif kind == "region":
        _render_region(block, path)
    elif kind == "matrix":
        _render_matrix(block, path)
    elif kind == "network":
        _render_network(block, path)
    elif kind == "line":
        _render_line(block, path)
    else:
        raise ValueError(f"Unknown plot kind: {kind}")
    return path


def generate_all_visuals(asset_dir: Path = ASSET_DIR) -> dict[str, str]:
    asset_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, str] = {}
    for block in VISUAL_BLOCKS:
        path = render_block(block, asset_dir=asset_dir)
        manifest[block["id"]] = str(path.relative_to(ROOT))
    manifest_path = asset_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def _md_for_block(block: dict[str, Any], manifest: dict[str, str]) -> str:
    anchors = ", ".join(f"`{a}`" for a in block["anchors"])
    nodes = ", ".join(f"`{n}`" for n in block["nodes"])
    image_path = manifest[block["id"]].replace("\\", "/")
    return f"""### {block['id']} - {block['title']}

출처 노트북: `{block['source_notebook']}`

노드: {nodes}

근거: {anchors}

![{block['id']}]({image_path})

시각화 목적: {block['purpose']}

그래프 해석 포인트: {block['interpretation']}

학생이 자주 하는 오해: {block['misconception']}

체크포인트 질문: {block['checkpoint']}
"""


def write_visualization_spec(manifest: dict[str, str]) -> None:
    lines = [
        "# DecisionMaking G1 Visualization Spec",
        "",
        "이 문서는 `decisionMaking/workshop`의 G1 문제 노트북을 위한 문항별 시각 튜터 설계서다.",
        "",
        "원칙:",
        "",
        "- 모든 시각화는 장식용이 아니라 최적해 이론의 판정 질문을 설명해야 한다.",
        "- 기본 실행 경로는 local Python, numpy, matplotlib, nbformat만 사용한다.",
        "- 외부 다운로드는 사용하지 않는다.",
        "- 문제 노트북의 정답을 누출하지 않고, 개념 구조와 판정 기준을 시각화한다.",
        "- 이미지 내부 라벨은 폰트 호환성을 위해 주로 영어를 쓰고, 해설은 한국어 markdown으로 제공한다.",
        "",
        "## 전체 맵",
        "",
        "| Phase | 문항 수 | 핵심 시각화 축 |",
        "| --- | ---: | --- |",
        "| P0001 | 10 | feasible region, BFS, ratio test, pivot, reduced cost, termination signal |",
        "| P0002 | 10 | standard form conversion, artificial variable, Phase I/II transition, diet/Solver mapping |",
        "| P0003 | 12 | Big-M penalty, primal-dual mapping, duality gap, complementary slackness, sensitivity routing |",
        "",
    ]
    for block in VISUAL_BLOCKS:
        lines.append(f"## {block['id']} - {block['title']}")
        lines.extend(
            [
                "",
                f"- 출처 노트북: `{block['source_notebook']}`",
                f"- node_id: {', '.join(f'`{n}`' for n in block['nodes'])}",
                f"- source anchor: {', '.join(f'`{a}`' for a in block['anchors'])}",
                f"- asset: `{manifest[block['id']]}`",
                "",
                f"시각화 목적: {block['purpose']}",
                "",
                f"사용할 데이터: {block['data']}",
                "",
                f"필요한 전처리: {block['preprocess']}",
                "",
                f"코드 셀 설계: {block['code_design']}",
                "",
                f"그래프 해석 포인트: {block['interpretation']}",
                "",
                f"학생이 자주 하는 오해: {block['misconception']}",
                "",
                f"체크포인트 질문: {block['checkpoint']}",
                "",
            ]
        )
    SPEC_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_visualization_checklist(manifest: dict[str, str]) -> None:
    lines = [
        "# DecisionMaking G1 Visualization Checklist",
        "",
        "## 생성 검증",
        "",
        "- [ ] `python visualization_cells.py`가 32개 PNG와 manifest를 생성한다.",
        "- [ ] `DM_G1_visual_lecture.ipynb`가 열리며 각 문항 이미지가 표시된다.",
        "- [ ] 문제 노트북 원본은 수정하지 않는다.",
        "- [ ] 외부 다운로드 없이 실행된다.",
        "- [ ] 각 문항은 node_id와 source anchor를 유지한다.",
        "",
        "## 문항별 체크",
        "",
        "| Block | Asset | 2D/diagram | 핵심 판정 질문 |",
        "| --- | --- | --- | --- |",
    ]
    for block in VISUAL_BLOCKS:
        lines.append(f"| `{block['id']}` | `{manifest[block['id']]}` | yes | {block['checkpoint']} |")
    CHECKLIST_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_visual_notebook(manifest: dict[str, str]) -> None:
    if nbformat is None:
        raise RuntimeError("nbformat is required to write the visual lecture notebook.")
    nb = nbformat.v4.new_notebook()
    cells = [
        nbformat.v4.new_markdown_cell(
            "# DM_G1_VISUAL_LECTURE\n\n"
            "이 노트북은 `DM_G1_P0001~P0003` 문제 노트북의 문항별 시각 튜터 자료다.\n\n"
            "목표는 정답을 대신 주는 것이 아니라, 최적해 이론을 2D 평면, 흐름도, 행렬, duality 지도, Solver 셀 구조로 직관화하는 것이다.\n\n"
            "사용 순서: 문제를 먼저 읽고, 해당 문항의 시각자료를 본 뒤, 체크포인트 질문에 답한다."
        ),
        nbformat.v4.new_code_cell(
            "from pathlib import Path\n"
            "from visualization_cells import VISUAL_BLOCKS, generate_all_visuals\n"
            "manifest = generate_all_visuals()\n"
            "len(VISUAL_BLOCKS), list(manifest.items())[:3]"
        ),
    ]
    for phase in ["P0001", "P0002", "P0003"]:
        cells.append(nbformat.v4.new_markdown_cell(f"## {phase} 시각 튜터 블록"))
        for block in [b for b in VISUAL_BLOCKS if b["phase"] == phase]:
            cells.append(nbformat.v4.new_markdown_cell(_md_for_block(block, manifest)))
    cells.append(
        nbformat.v4.new_markdown_cell(
            "## Final. 자기 점검\n\n"
            "1. feasible region과 BFS를 같은 그림에서 설명할 수 있는가?\n"
            "2. ratio test가 왜 positive coefficient만 보는지 말할 수 있는가?\n"
            "3. artificial variable이 최종해에서 0이어야 하는 이유를 설명할 수 있는가?\n"
            "4. Big-M, duality, sensitivity report가 하나의 흐름으로 연결되는 이유를 말할 수 있는가?"
        )
    )
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    nbformat.write(nb, NOTEBOOK_PATH)


def generate_all() -> dict[str, str]:
    manifest = generate_all_visuals()
    write_visualization_spec(manifest)
    write_visualization_checklist(manifest)
    write_visual_notebook(manifest)
    try:
        from visualization_item_cards import generate_item_card_pack

        generate_item_card_pack(update_notebooks=True)
    except Exception as exc:  # pragma: no cover - keeps legacy G1 visual generation usable.
        print(f"warning: item-card pack generation skipped: {exc}")
    return manifest


if __name__ == "__main__":
    result = generate_all()
    print(json.dumps({"visual_count": len(result), "output_dir": str(ROOT), "assets": result}, ensure_ascii=False, indent=2))
