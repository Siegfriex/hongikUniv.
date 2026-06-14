#!/usr/bin/env python3
"""Build DecisionMaking PDF-only transcripts, sidecars, and tutor RAG docs."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "decisionMaking"
PDF_SOURCE_DIR = COURSE / "pdf_sources"
TRANSCRIPT_DIR = COURSE / "pdf_transcripts"
INVENTORY_DIR = COURSE / "_inventory"
FINAL_BRIEF_DIR = COURSE / "final_brief"
FLAT_PACK_DIR = COURSE / "rag_applied_flat_pack"
WORKSHOP_DIR = COURSE / "workshop"


@dataclass(frozen=True)
class Concept:
    slug: str
    label: str
    term: str
    definition: str
    intuition: str
    formula: str
    real_language: str
    math_language: str
    tool_language: str
    course_example: str
    common_mistake: str
    prerequisite: str
    followup: str
    analogous: str
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class SourceProfile:
    source_id: str
    slug: str
    filename: str
    original_filename: str
    title: str
    graph_location: str
    one_line: str
    prerequisite_nodes: str
    followup_nodes: str
    analogous_nodes: str
    examples: str
    concepts: tuple[Concept, ...]
    review_focus: tuple[str, ...]


SOURCES: tuple[SourceProfile, ...] = (
    SourceProfile(
        "DM_PDF01",
        "ch04_simplex_tableau_twophase_supplement",
        "DM_PDF01_ch04_simplex_tableau_twophase_supplement.pdf",
        "4장 심플렉스법(보완_심플렉스 타블로이용, 2단계법)_수정본 (7).pdf",
        "Ch.4 심플렉스 타블로 보완과 2단계법",
        "6강 보완: 표준형과 BFS를 타블로 피벗, 특수 종료, 2단계법으로 완성하는 구간",
        "심플렉스는 가능영역 꼭짓점 이동을 타블로라는 계산 장치로 구현하고, 초기 BFS가 없으면 2단계법으로 출발점을 만든다.",
        "LP 일반형, 표준형, 정규형, slack/surplus/artificial variable, BFS",
        "Big-M, Duality, Sensitivity Analysis, Integer Programming의 LP relaxation",
        "그래프 해법의 꼭짓점 최적성, Solver의 제약 셀, 타블로의 기저 갱신",
        "복수 최적해, 비유계, 식단 문제 min, 2단계법 예제",
        (
            Concept(
                "simplex_tableau",
                "심플렉스 타블로",
                "simplex tableau",
                "심플렉스 반복에 필요한 목적행, 제약행, 기저변수, 우변, 비율검사를 한 표에 모은 계산 구조다.",
                "그래프에서 꼭짓점을 하나씩 이동하는 일을, 표 안에서 행 연산과 기저 교체로 수행한다고 보면 된다.",
                "정규형 행렬에서 목적행과 제약행을 한 tableau로 두고 entering/leaving variable을 반복 선택한다.",
                "현재 가능한 생산 조합에서 이익을 더 키울 수 있는 방향을 찾는다.",
                "z-row의 개선 가능 계수와 제약행의 RHS/a_ij 비율로 다음 BFS를 선택한다.",
                "스프레드시트에서는 현재 basis 행과 RHS 셀이 있고, 피벗 후 행 전체가 갱신되는 계산표다.",
                "DM_PDF01의 예1은 x1, x2, slack 변수 x3~x5를 포함한 max 문제를 타블로로 풀어 최적해를 찾는다.",
                "비율검사를 모든 행에 적용하는 오류가 많다. entering 열의 계수가 양수인 행만 leaving 후보가 된다.",
                "표준형과 정규형",
                "minimum ratio test와 pivot",
                "Solver의 반복 계산 로그",
                ("타블로", "기저", "우변", "비율", "최적해", "simplex", "tableau"),
            ),
            Concept(
                "multiple_optima",
                "복수 최적해",
                "multiple optimal solutions",
                "최적 타블로에서 비기저변수의 목적행 계수가 0이면 다른 최적 BFS가 존재할 수 있는 상태다.",
                "목적함수 등위선이 가능영역의 한 모서리와 겹쳐서 한 점이 아니라 선분 전체가 같은 값을 주는 상황이다.",
                "최적 조건을 만족한 뒤 nonbasic variable의 reduced cost가 0이면 대안 최적해를 피벗으로 찾는다.",
                "두 생산계획이 서로 다르지만 총이익이 같은 경우다.",
                "z-row에서 개선 계수는 없지만 0 reduced cost인 비기저변수를 진입시켜도 z가 변하지 않는다.",
                "Solver에서는 같은 objective value를 주는 여러 변수셀 조합이 존재할 수 있다.",
                "DM_PDF01 예2는 비기저변수 목적함수 계수 0을 통해 대안 최적해를 제시한다.",
                "최적해가 여러 개라는 말은 아무 점이나 된다는 뜻이 아니다. 같은 최적 face 위의 feasible point만 가능하다.",
                "최적성 판정",
                "민감도 분석의 대체 최적/허용범위",
                "그래프 해법의 등위선 평행 접촉",
                ("복수", "대안 최적", "계수가 0", "multiple", "optimal"),
            ),
            Concept(
                "unbounded_solution",
                "비유계",
                "unbounded solution",
                "목적함수를 계속 개선할 수 있으면서 제약이 그 방향을 막지 못하는 상태다.",
                "좋아지는 방향으로 걸어가는데 벽이 없는 경우다.",
                "max에서 entering column의 모든 제약행 계수가 <= 0이면 minimum ratio test를 만들 수 없고 z는 무한히 증가할 수 있다.",
                "생산량을 늘릴수록 이익이 증가하는데 자원 제약이 그 방향을 제한하지 않는 모형 오류 또는 열린 가능영역이다.",
                "a_ij > 0인 leaving 후보가 없으면 x_j를 증가시켜도 현재 기저변수 비음 조건을 깨지 않는다.",
                "Solver에서는 unbounded 또는 해를 찾을 수 없음으로 보고될 수 있다.",
                "DM_PDF01 예3은 x3 진입 시 모든 제약식 계수가 음수라 목적함수를 무한 개선할 수 있음을 보인다.",
                "비유계와 infeasible을 혼동하지 말아야 한다. 비유계는 feasible 해가 있지만 목적값이 한없이 좋아지는 상태다.",
                "minimum ratio test",
                "모형 검증과 제약 누락 진단",
                "그래프에서 열린 가능영역",
                ("무한", "비유계", "unbounded", "계수는 모두 음", "목적함수"),
            ),
            Concept(
                "two_phase_method",
                "2단계법",
                "two-phase method",
                "초기 기저가능해가 바로 보이지 않을 때 Phase I에서 인위변수를 제거하고 Phase II에서 원 목적함수를 최적화하는 방법이다.",
                "심플렉스가 출발할 꼭짓점을 못 찾으면, 먼저 임시 발판을 놓고 그 발판을 치운 뒤 원래 산을 오른다.",
                "Phase I: artificial variable 합 w를 최소화해 w*=0이면 feasible. Phase II: 원래 z로 tableau를 이어간다.",
                "식단 min 문제처럼 >= 제약 때문에 surplus를 빼면 초기 slack basis가 음수가 되어 바로 시작할 수 없다.",
                "Phase I tableau에서 artificial basis를 만들고, w-row를 제거한 뒤 원 목적행으로 전환한다.",
                "Solver는 내부적으로 feasible start를 찾지만, 손계산에서는 Phase I이 그 역할을 명시한다.",
                "DM_PDF01 후반부와 DM_PDF05는 인위변수와 2단계법을 통해 식단형 min 문제를 푸는 흐름을 보여준다.",
                "w*=0의 의미를 최적 목적값으로 오해하면 안 된다. w는 실행가능성 판별용 임시 목적함수다.",
                "surplus/artificial variable",
                "Big-M method와 duality",
                "Big-M의 penalty 방식",
                ("2단계", "Phase", "인위변수", "artificial", "w"),
            ),
        ),
        ("타블로 수치 전개", "복수 최적과 비유계 구분", "2단계법 Phase I/II 연결"),
    ),
    SourceProfile(
        "DM_PDF02",
        "ch05_sensitivity_analysis",
        "DM_PDF02_ch05_sensitivity_analysis.pdf",
        "Ch.5 Sensitivity analysis (Ch. 5)_26 (2).pdf",
        "Ch.5 민감도 분석",
        "7강 쌍대/민감도 이후: 최적해가 입력 변화에 얼마나 안정적인지 읽는 구간",
        "민감도 분석은 최적해 하나를 끝으로 보지 않고, 자원량과 목적계수가 변할 때 같은 해석이 어디까지 유지되는지 읽는다.",
        "LP 최적해, shadow price, reduced cost, binding constraint",
        "수송/네트워크의 비용 변화, 정수계획에서 LP 완화의 한계",
        "쌍대변수, Solver sensitivity report, 타블로 목적행 계수",
        "유모차-보행기 생산계획, 기계 시간 자원, 원료 제한",
        (
            Concept(
                "sensitivity_analysis",
                "민감도 분석",
                "sensitivity analysis",
                "LP 최적해와 목적값이 계수, RHS, 자원량 변화에 어떻게 반응하는지 분석하는 절차다.",
                "해를 하나 구하고 끝내는 것이 아니라, 그 해가 얼마나 흔들림에 강한지 보는 사후 진단이다.",
                "RHS 변화에 대한 목적값 변화는 허용범위 안에서 shadow price로 근사된다.",
                "기계 시간이 1시간 더 생기면 총이익이 얼마나 늘어나는지 묻는다.",
                "Delta z = shadow price * Delta RHS, 단 허용가능 증감 범위 안에서만 해석한다.",
                "Solver 민감도 보고서의 Shadow Price, Allowable Increase/Decrease 열을 읽는다.",
                "DM_PDF02는 유모차-보행기 product-mix 문제에서 기계 시간 변화와 자원 가치를 해석한다.",
                "shadow price를 무제한 적용하는 오류가 많다. 허용범위를 벗어나면 basis가 바뀌어 재해석해야 한다.",
                "최적 타블로와 binding constraint",
                "수송문제의 비용/공급 변화 분석",
                "쌍대변수의 경제적 의미",
                ("민감도", "sensitivity", "Shadow", "허용", "보행기", "유모차"),
            ),
            Concept(
                "shadow_price",
                "잠재가격",
                "shadow price",
                "제약 RHS를 1단위 완화했을 때 목적함수가 얼마나 개선되는지를 나타내는 한계 가치다.",
                "희소한 자원을 한 단위 더 얻는 것이 얼마만큼 가치 있는지 가격처럼 읽는 값이다.",
                "binding constraint i에 대해 y_i = Delta z / Delta b_i, 허용범위 안에서 적용한다.",
                "기계2 시간이 부족한 경우 1시간 추가가 이익을 얼마나 올리는지 판단한다.",
                "z_new = z_old + y_i * Delta b_i, if Delta b_i is within allowable range.",
                "Solver 보고서에서는 Constraint 섹션의 Shadow Price로 표시된다.",
                "DM_PDF02의 기계별 이용가능시간은 resource allocation의 RHS이며 shadow price 해석 대상이다.",
                "nonbinding 제약의 shadow price가 보통 0인 이유를 놓치기 쉽다. 남는 자원은 한 단위 더 줘도 가치가 없다.",
                "binding/nonbinding constraint",
                "쌍대 최적해",
                "경제학의 한계가치",
                ("잠재가격", "Shadow", "price", "자원", "RHS", "한계"),
            ),
            Concept(
                "reduced_cost",
                "감소비용",
                "reduced cost",
                "현재 0인 변수가 해에 들어오기 위해 목적계수가 얼마나 개선되어야 하는지 나타내는 값이다.",
                "지금 선택되지 않은 활동이 경쟁력이 생기려면 단위 이익이나 비용이 얼마나 바뀌어야 하는지 보는 지표다.",
                "max 문제에서 nonbasic variable j는 c_j - y^T a_j가 0 이하이면 현재 basis에서 들어오지 않는다.",
                "어떤 제품을 생산하지 않는 이유가 자원 소모 대비 이익이 부족해서인지 확인한다.",
                "tableau z-row 또는 Solver Variable Cells 섹션의 Reduced Cost로 읽는다.",
                "스프레드시트에서는 변수셀 값이 0인 항목과 objective coefficient 변화 허용범위를 함께 본다.",
                "DM_PDF02의 product-mix 문제에서 생산하지 않는 제품/활동이 있다면 reduced cost가 그 이유를 설명한다.",
                "reduced cost를 실제 비용으로 오해하면 안 된다. 현재 basis 기준의 기회비용/개선 필요량이다.",
                "쌍대가격과 목적계수",
                "대안 최적해 판정",
                "타블로의 목적행 계수",
                ("Reduced", "감소", "목적계수", "비기저", "0"),
            ),
        ),
        ("허용범위 밖 변화", "shadow price와 reduced cost 차이", "기존 7강 쌍대 해석 연결"),
    ),
    SourceProfile(
        "DM_PDF03",
        "ch06_branch_and_bound",
        "DM_PDF03_ch06_branch_and_bound.pdf",
        "6장_분지한계법 (1).pdf",
        "Ch.6 분지한계법",
        "정수계획 해법: LP 완화로 상한/하한을 만들고 정수 조건을 만족할 때까지 탐색하는 구간",
        "분지한계법은 정수조건 때문에 생긴 불연속성을 LP 완화와 가지치기로 통제하는 탐색 알고리즘이다.",
        "LP relaxation, integer variable, feasible solution, upper/lower bound",
        "0-1 시설입지, 배낭/선택 문제, Solver integer option",
        "심플렉스 최적값을 bound로 쓰는 트리 탐색",
        "이콤전자 승합차 구입 모형, x1 floor/ceil branching",
        (
            Concept(
                "lp_relaxation",
                "LP 완화",
                "LP relaxation",
                "정수계획에서 정수 조건을 잠시 제거해 연속 LP로 푸는 완화 문제다.",
                "정수 격자점만 보려면 어렵기 때문에, 먼저 전체 평면/다각형에서 가장 좋은 값을 구해 한계를 잡는다.",
                "IP: x_j integer. LP relaxation: x_j >= 0만 남기고 x_j integer를 제거한다.",
                "차량 대수는 정수여야 하지만, 완화 문제에서는 2.9대 같은 해가 나올 수 있다.",
                "max IP에서 LP relaxation optimum Z는 해당 부문제의 upper bound가 된다.",
                "Solver에서는 정수조건을 잠시 빼고 Simplex LP로 푼 결과와 유사하다.",
                "DM_PDF03은 LP완화 최적해 x1=2.90, x2=1.72에서 분지를 시작한다.",
                "LP 완화해를 반올림해 정답으로 삼는 것은 일반적으로 틀리다. 반올림해가 feasible인지도 보장되지 않는다.",
                "LP feasible region",
                "branching and bounding",
                "연속 최적해와 정수 격자점",
                ("LP완화", "완화", "relaxation", "정수", "소수"),
            ),
            Concept(
                "bounding_strategy",
                "한계전략",
                "bounding strategy",
                "각 부문제의 LP 완화값을 이용해 더 볼 가치가 있는지 판정하는 전략이다.",
                "현재까지 찾은 정수해보다 좋을 가능성이 없으면 그 가지를 더 내려가지 않는다.",
                "max 문제에서 LP relaxation Z는 upper bound, incumbent integer value L은 lower bound다.",
                "Z <= L이면 그 부문제의 하위 가지도 L보다 좋아질 수 없으므로 절단한다.",
                "if Z <= L: prune. if integer feasible and Z > L: update L.",
                "트리 표에서는 각 노드 옆의 Z와 L 비교가 가지치기 기준이다.",
                "DM_PDF03은 L=-infinity에서 시작해 정수해가 발견될 때마다 L을 갱신한다.",
                "상한과 하한 방향을 max/min에서 뒤집지 않는 실수가 많다.",
                "LP relaxation",
                "branch pruning",
                "민감도 분석의 한계값 해석과는 다른 algorithmic bound",
                ("한계", "상한", "하한", "bound", "L", "Z"),
            ),
            Concept(
                "branching_strategy",
                "분지전략",
                "branching strategy",
                "소수 값을 가진 정수변수를 골라 floor/ceil 제약을 추가한 두 부문제로 나누는 전략이다.",
                "2.9대는 불가능하므로 x <= 2와 x >= 3의 두 세계로 나눠 탐색한다.",
                "x_k = v non-integer이면 x_k <= floor(v), x_k >= ceil(v)를 각각 추가한다.",
                "x1=2.90이면 x1<=2와 x1>=3 두 가지 부문제를 만든다.",
                "각 branch는 기존 제약에 새 bound constraint를 추가한 LP relaxation으로 다시 풀린다.",
                "Solver의 Branch and Bound는 내부적으로 이런 분기 트리를 관리한다.",
                "DM_PDF03은 x1을 분지변수로 선택해 하한/상한 제약을 추가한다.",
                "ceil/floor 방향을 반대로 쓰면 원래 정수 가능 영역을 빠뜨린다.",
                "fractional LP optimum",
                "node selection and pruning",
                "이진 변수의 include/exclude 분기",
                ("분지", "branch", "floor", "ceil", "x1", "부문제"),
            ),
        ),
        ("LP 완화해 반올림 금지", "max 기준 L/Z 방향", "분지 트리 추적"),
    ),
    SourceProfile(
        "DM_PDF04",
        "ch06_integer_programming_week1",
        "DM_PDF04_ch06_integer_programming_week1.pdf",
        "6장_정수계획(1주)_hs_26 (2).pdf",
        "Ch.6 정수계획 1주차",
        "LP 이후 확장: 변수의 값이 연속량이 아니라 개수/선택일 때 정수성을 모형에 넣는 구간",
        "정수계획은 LP의 선형 구조를 유지하되, 변수의 domain을 정수 또는 0-1로 제한해 현실적 선택을 표현한다.",
        "LP 모형화, decision variable, Solver variable cell/domain",
        "분지한계법, 시설입지, 고정비, 상호배타 선택",
        "연속 LP와 같은 목적/제약 구조에 domain 제약이 추가된 형태",
        "사람 수, 기계 대수, 출장 횟수, 공장 가동 여부",
        (
            Concept(
                "integer_programming",
                "정수계획",
                "integer programming",
                "목적함수와 제약식은 선형이지만 일부 또는 모든 변수가 정수값만 가질 수 있는 최적화 모형이다.",
                "생산량은 연속일 수 있지만 사람 수, 트럭 수, 설치 여부는 2.7처럼 나눌 수 없기 때문에 domain을 제한한다.",
                "min/max c^T x subject to Ax <= b, x_j integer for selected j.",
                "기계 대수나 출장 횟수처럼 셀 수 있는 결정을 변수로 둔다.",
                "LP model + integer restrictions on selected variable cells.",
                "Solver에서는 변수셀에 int 또는 bin 제한조건을 추가한다.",
                "DM_PDF04는 int/bin 선택과 정수 최적화 비율의 의미를 정수계획 도입부에서 다룬다.",
                "식이 선형이면 단순 LP라고 착각하기 쉽다. 변수 domain이 정수이면 해법 난이도가 크게 달라진다.",
                "LP 일반형",
                "branch-and-bound",
                "0-1 binary model",
                ("정수", "Integer", "int", "bin", "0,1", "Solver"),
            ),
            Concept(
                "binary_variable",
                "0-1 변수",
                "binary variable",
                "어떤 선택을 하거나 하지 않는지를 1과 0으로 표현하는 변수다.",
                "수량을 묻는 변수가 아니라 스위치다. 켜면 1, 끄면 0이다.",
                "x_j in {0,1}. 선택하면 1, 선택하지 않으면 0.",
                "공장을 열지 말지, 후보지에 시설을 설치할지, 과제를 배정할지를 표현한다.",
                "Solver에서는 bin constraint로 지정한다.",
                "스프레드시트에서는 변수셀 값이 0/1이고 제약식은 이 선택들의 합이나 조건부 논리를 표현한다.",
                "DM_PDF04의 공장 가동 여부 예시는 binary variable의 대표 용도다.",
                "0-1 변수에 연속 생산량 의미를 섞으면 안 된다. 필요하면 선택 변수 y와 생산량 x를 따로 둔다.",
                "decision variable",
                "fixed-charge model and facility location",
                "assignment problem의 행/열 0-1 구조",
                ("0-1", "binary", "bin", "선택", "가동", "여부"),
            ),
            Concept(
                "integer_solver_option",
                "Solver 정수 옵션",
                "integer Solver option",
                "Excel Solver에서 변수셀의 정수/이진 제한과 해법을 지정해 정수계획을 푸는 설정이다.",
                "수식 자체보다 변수 셀의 값 종류를 Solver에게 알려주는 단계다.",
                "Variable cells with int/bin constraints; solving method may use branch-and-bound or evolutionary methods.",
                "변수셀을 bin으로 지정하면 0 또는 1만 허용된다.",
                "Solver constraints include x_j = integer or x_j = binary.",
                "해찾기 옵션에서 정수 제한, 정수 최적화 비율, 해법 선택을 확인한다.",
                "DM_PDF04는 Excel 2010 Solver의 분지한계해법과 유전자해법을 함께 언급한다.",
                "Solver가 정수조건을 자동으로 이해한다고 생각하면 안 된다. 반드시 int/bin 제한을 넣어야 한다.",
                "spreadsheet modeling",
                "branch-and-bound performance",
                "LP Solver와 evolutionary Solver",
                ("해찾기", "Solver", "정수 제한", "진화", "분지한계"),
            ),
        ),
        ("int/bin domain 구분", "정수 최적화 비율 의미", "LP와 IP 난이도 차이"),
    ),
    SourceProfile(
        "DM_PDF05",
        "ch04_simplex_duality_week2",
        "DM_PDF05_ch04_simplex_duality_week2.pdf",
        "4장 심플렉스법과 쌍대성(2주)_hs (7).pdf",
        "Ch.4 심플렉스, Big-M, 쌍대성 연결",
        "6~7강 다리: 2단계법/Big-M으로 infeasible start를 처리하고 쌍대문제로 넘어가는 구간",
        "인위변수는 심플렉스 출발을 위한 임시 장치이고, Big-M/2단계법은 그 임시 장치를 목적함수에서 제거하도록 설계된다.",
        "surplus/artificial variable, two-phase method, min-to-max conversion",
        "dual problem, complementary slackness, sensitivity report",
        "2단계법과 Big-M의 같은 목적, 다른 구현",
        "식단문제 min, 인위변수 r1/r2, Big-M penalty",
        (
            Concept(
                "artificial_variable",
                "인위변수",
                "artificial variable",
                "초기 기저가능해를 만들기 위해 등식에 임시로 추가하는 변수다.",
                "실제 문제에는 없는 보조 바퀴다. 출발할 때만 필요하고 최종해에서는 0이어야 한다.",
                ">= 또는 = 제약에서 slack basis가 없을 때 +r_i를 추가해 basis를 만든다.",
                "식단문제의 영양 최소 요구량 제약은 surplus를 빼면 초기 RHS basis가 바로 만들어지지 않아 r_i가 필요하다.",
                "row: a_i x - s_i + r_i = b_i, r_i >= 0, and final r_i must be 0.",
                "타블로에서는 r_i가 초기 기저변수가 되고, Phase I/Big-M에서 제거 대상이 된다.",
                "DM_PDF05는 r1, r2를 도입하고 r1=0, r2=0 조건이 원문제와 동치임을 묻는다.",
                "인위변수를 실제 의사결정 변수로 해석하면 안 된다. 최종해에 남으면 원문제가 infeasible일 수 있다.",
                "surplus variable",
                "Big-M and Phase I",
                "slack variable과의 대비",
                ("인위", "artificial", "r1", "r2", "Big M", "초기"),
            ),
            Concept(
                "big_m_method",
                "Big-M 방법",
                "Big-M method",
                "인위변수가 최종해에 남지 않도록 목적함수에 매우 큰 벌점을 주는 심플렉스 변형이다.",
                "임시 변수를 쓰되, 최적화가 그 변수를 극도로 싫어하게 만드는 방식이다.",
                "max 문제에서는 artificial variable에 -M penalty, min 또는 변환식에서는 부호를 일관되게 조정한다.",
                "식단 min을 max -Z로 바꾸고 인위변수에 M 벌점을 붙여 원문제 feasible 해를 강제한다.",
                "objective row includes +/- M r_i; tableau algebra must remove artificial basis coefficients.",
                "타블로에서는 M이 포함된 목적행을 계산하므로 부호 실수가 치명적이다.",
                "DM_PDF05는 Big penalty의 부호 주의를 명시한다.",
                "M을 실제 큰 숫자로만 생각하면 수치 불안정과 부호 오류를 놓친다. 핵심은 lexicographic penalty다.",
                "artificial variable",
                "dual problem and sensitivity",
                "two-phase method",
                ("Big", "M", "penalty", "벌점", "부호", "인위변수"),
            ),
            Concept(
                "min_to_max_conversion",
                "최소화-최대화 변환",
                "min-to-max conversion",
                "최소화 문제의 목적함수에 -1을 곱해 최대화 문제로 바꾸는 표현 변환이다.",
                "같은 선호를 반대 부호의 산으로 바꿔 심플렉스 규칙을 맞추는 것이다.",
                "min Z = c^T x is equivalent to max -Z = -c^T x.",
                "식단 비용 최소화는 -비용 최대화로 바꿔 max용 타블로 규칙을 적용할 수 있다.",
                "objective row changes sign; feasibility constraints do not disappear.",
                "스프레드시트에서는 원 목적은 min으로 둘 수 있지만 손계산 타블로에서는 부호 변환을 명확히 한다.",
                "DM_PDF05는 식단문제를 max -Z 형태로 바꾸는 과정을 보여준다.",
                "목적함수 부호만 바꾸고 제약 부호나 surplus/artificial 처리를 잊는 오류가 많다.",
                "LP objective sense",
                "Big-M sign convention",
                "dual primal 방향 변환",
                ("최소화", "최대화", "-Z", "Min", "Max", "식단"),
            ),
        ),
        ("Big-M 부호", "인위변수 최종 0 조건", "2단계법과 Big-M 비교"),
    ),
    SourceProfile(
        "DM_PDF06",
        "ch05_transportation_network_week1",
        "DM_PDF06_ch05_transportation_network_week1.pdf",
        "5장 수송 및 네트워크 (1주)_hs (6).pdf",
        "Ch.5 수송계획과 네트워크 분석",
        "LP 응용 확장: 일반 자원배분 모형이 네트워크 노드와 arc 흐름 구조로 특수화되는 구간",
        "수송/네트워크 문제는 LP의 변수와 제약을 노드, arc, flow balance로 재해석한 구조화된 모델이다.",
        "LP formulation, 공급/수요 균형, assignment model",
        "최단경로, 최대흐름, 최소비용흐름, CPM/PERT",
        "행렬 제약이 네트워크 보존식으로 보이는 표현 변환",
        "Transportation, transshipment, assignment, shortest path, max flow",
        (
            Concept(
                "transportation_problem",
                "수송문제",
                "transportation problem",
                "여러 공급지에서 여러 수요지로 얼마를 보낼지 결정해 총 수송비를 최소화하는 LP 특수형이다.",
                "공급은 남기지 않고 수요는 채우면서 가장 싼 경로 조합을 찾는 문제다.",
                "min sum_i sum_j c_ij x_ij subject to sum_j x_ij = supply_i, sum_i x_ij = demand_j, x_ij >= 0.",
                "공장별 공급량과 창고별 수요량이 주어졌을 때 어느 공장에서 어느 창고로 얼마나 보내는지 정한다.",
                "row sums equal supply, column sums equal demand.",
                "스프레드시트에서는 수송량 행렬, 행합/열합 제약, 단위비용 행렬의 SUMPRODUCT로 만든다.",
                "DM_PDF06은 공급지/수요지, 공급량/수요량, 단위당 수송비용을 수송문제의 핵심 요소로 제시한다.",
                "공급-수요가 불균형이면 dummy supply/demand를 추가해야 하는데 이를 놓치기 쉽다.",
                "LP equality constraints",
                "transshipment and min-cost flow",
                "Big M 운송 예제",
                ("수송", "Transportation", "공급", "수요", "cij", "수송비"),
            ),
            Concept(
                "transshipment_problem",
                "경유수송문제",
                "transshipment problem",
                "공급지와 수요지 사이에 경유지가 존재하고, 각 노드에서 유입과 유출의 균형을 맞추는 네트워크 LP다.",
                "물건이 중간 물류센터를 거쳐 이동할 수 있으므로 단순 행렬보다 네트워크 흐름 보존이 중요해진다.",
                "for each node: inflow + supply = outflow + demand.",
                "공장에서 물류센터를 거쳐 고객 지역으로 보내는 구조다.",
                "node balance constraints replace simple row/column sums.",
                "Solver에서는 arc flow 변수를 두고 각 노드별 balance 셀을 만든다.",
                "DM_PDF06은 경유지 존재와 지역 간 단위비용을 transshipment의 차이로 제시한다.",
                "경유지를 공급지나 수요지처럼만 처리하면 유입=유출 balance를 빠뜨린다.",
                "transportation problem",
                "minimum cost flow",
                "flow conservation in networks",
                ("경유", "Transshipment", "경유지", "유입", "유출", "flow"),
            ),
            Concept(
                "assignment_problem",
                "할당문제",
                "assignment problem",
                "각 작업을 각 자원에 1:1로 배정해 총 비용을 최소화하거나 효용을 최대화하는 0-1 네트워크 특수형이다.",
                "각 사람은 하나의 일만, 각 일도 한 사람에게만 배정되는 matching 문제다.",
                "x_ij in {0,1}, sum_j x_ij = 1, sum_i x_ij = 1.",
                "작업을 기계에 할당하거나 작업자를 작업에 배정한다.",
                "binary matrix with every row sum and column sum equal to 1.",
                "스프레드시트에서는 0/1 배정 행렬과 행합/열합=1 제약으로 구성한다.",
                "DM_PDF06은 할당문제를 공급지 수=수요지 수, 공급량=수요량=1인 특별한 수송문제로 설명한다.",
                "할당문제를 일반 수송처럼 연속변수로 둬도 특수 구조상 정수해가 나올 수 있지만, 의미상 0-1 해석을 유지해야 한다.",
                "transportation problem",
                "TSP and matching",
                "Sellmore assignment",
                ("할당", "Assignment", "matching", "0-1", "작업", "기계"),
            ),
            Concept(
                "network_flow",
                "네트워크 흐름",
                "network flow",
                "노드와 arc로 구성된 시스템에서 흐름량을 결정하고 보존/용량/비용 제약을 만족시키는 모형군이다.",
                "각 길에 얼마를 흘릴지 정하고, 각 지점에서 들어온 양과 나간 양의 장부를 맞춘다.",
                "flow conservation plus capacity constraints on arcs.",
                "최단경로, 최대흐름, 최소비용흐름이 모두 같은 네트워크 언어를 공유한다.",
                "node balance rows and arc variable columns form the spreadsheet matrix.",
                "Solver에서는 arc별 변수, 노드별 balance, arc capacity 제약으로 구성한다.",
                "DM_PDF06은 shortest path, maximum flow, minimum cost flow, CPM/PERT를 같은 장의 네트워크 분석으로 묶는다.",
                "경로 선택 문제와 흐름량 문제를 구분하지 않으면 변수 정의가 흔들린다.",
                "LP formulation",
                "CPM/PERT and project networks",
                "graph representation of constraints",
                ("네트워크", "flow", "최단경로", "최대흐름", "최소비용", "CPM"),
            ),
        ),
        ("수송 vs 경유수송", "할당의 0-1/수송 특수형", "network balance 식"),
    ),
    SourceProfile(
        "DM_PDF07",
        "ch07_nonlinear_programming",
        "DM_PDF07_ch07_nonlinear_programming.pdf",
        "7장비선형계획26_hs.pdf",
        "Ch.7 비선형계획",
        "LP/IP 이후 확장: 목적함수나 제약식이 선형이 아닐 때 Solver와 최적성 해석이 달라지는 구간",
        "비선형계획은 현실의 곡선 관계를 표현할 수 있지만 지역 최적해와 초기해 민감성 때문에 LP보다 해석이 조심스럽다.",
        "LP, convexity intuition, Solver modeling",
        "GRG nonlinear, local/global optimum, KKT intuition",
        "LP의 직선/평면 제약과 NLP의 곡면 목적/제약 대비",
        "담장 길이로 직사각형 면적 최대화, Cobb-Douglas 형태, GRG Solver",
        (
            Concept(
                "nonlinear_programming",
                "비선형계획",
                "nonlinear programming",
                "목적함수 또는 제약식 중 하나 이상이 비선형 함수인 최적화 모형이다.",
                "직선으로만 표현하던 관계 대신 곡선, 곱, 제곱, 로그 같은 현실 관계를 넣는 모형이다.",
                "optimize f(x) subject to g_i(x) <= b_i, where f or g_i is nonlinear.",
                "면적 S = X1*X2를 최대화하는 문제는 목적함수가 곱이라 비선형이다.",
                "B4=B7*B8처럼 변수셀끼리 곱해지는 objective cell이 생긴다.",
                "Excel Solver에서는 GRG Nonlinear 해법을 선택한다.",
                "DM_PDF07은 X^0.5Y^0.7, log, sin, sqrt 같은 비선형 함수와 면적 최대화 예를 든다.",
                "제약식이 선형이어도 목적함수가 비선형이면 전체 문제는 비선형계획이다.",
                "LP formulation",
                "local/global optimum",
                "quadratic programming and separable programming",
                ("비선형", "Nonlinear", "GRG", "곱", "sqrt", "log"),
            ),
            Concept(
                "local_global_optimum",
                "지역 최적해와 전체 최적해",
                "local and global optimum",
                "지역 최적해는 주변보다 좋은 해이고, 전체 최적해는 가능한 모든 해 중 가장 좋은 해다.",
                "산봉우리가 여러 개 있으면 가까운 봉우리는 올랐지만 세계 최고봉은 아닐 수 있다.",
                "x* is local optimum if nearby feasible points are no better; global optimum if no feasible point anywhere is better.",
                "초기해 (0,0)에서는 멈추지만 다른 초기해에서는 (2.5,5)가 나오는 예는 초기해 민감성을 보여준다.",
                "Solver result may depend on starting variable cell values.",
                "GRG Nonlinear는 지역 탐색 기반이라 여러 초기해 실험이 필요할 수 있다.",
                "DM_PDF07은 초기해에 따라 (0,0) 또는 (2.5,5)가 나오는 비선형계획의 어려움을 제시한다.",
                "Solver가 찾은 해를 항상 전체 최적해라고 믿으면 안 된다. 특히 비볼록 문제는 위험하다.",
                "feasible region",
                "multi-start and global search",
                "LP의 꼭짓점 최적성과 대비",
                ("지역", "전체", "초기해", "local", "global", "GRG"),
            ),
            Concept(
                "grg_solver",
                "GRG 비선형 해법",
                "GRG nonlinear solver",
                "Excel에서 부드러운 비선형 모형을 풀 때 사용하는 일반화 감소기울기 기반 해법이다.",
                "비선형 곡면 위에서 기울기를 따라 더 나은 방향을 찾는 로컬 탐색 방식이다.",
                "uses gradient information and active constraints to search for a local optimum.",
                "면적 최대화 스프레드시트에서 해법선택을 비선형 GRG로 둔다.",
                "objective and constraint cells may contain nonlinear formulas.",
                "Solver options include GRG Nonlinear and initial variable values.",
                "DM_PDF07은 비선형계획 스프레드시트 모형에서 해법선택: 비선형 GRG를 명시한다.",
                "GRG를 선형 Simplex LP와 혼동하면 안 된다. 선형성 가정과 최적성 보장이 다르다.",
                "nonlinear objective",
                "local optimum diagnostics",
                "Solver Simplex LP와 Evolutionary 해법",
                ("GRG", "Solver", "비선형", "초기해", "스프레드시트"),
            ),
        ),
        ("OCR 공백 페이지", "지역/전체 최적 구분", "Solver 해법 선택"),
    ),
    SourceProfile(
        "DM_PDF08",
        "ch06_integer_programming_week2",
        "DM_PDF08_ch06_integer_programming_week2.pdf",
        "6장_정수계획(2주)_hs (1).pdf",
        "Ch.6 정수계획 2주차: 0-1 응용 모형",
        "정수계획 응용: 시설입지, 커버링, 고정비, 선택 논리를 0-1 변수로 표현하는 구간",
        "0-1 정수계획은 복잡한 선택/논리/커버 조건을 선형 제약으로 번역하는 모형화 언어다.",
        "binary variable, integer programming, assignment structure",
        "branch-and-bound, facility location, covering model",
        "할당문제의 0-1 행렬, Solver bin 제약, network covering",
        "응급 의료 서비스 후보지, 공공 설비 입지, 행정구역 커버",
        (
            Concept(
                "set_covering_model",
                "집합커버링 모형",
                "set covering model",
                "모든 수요 구역이 적어도 하나의 선택된 시설에 의해 커버되도록 하면서 선택 수를 최소화하는 0-1 모형이다.",
                "각 지역을 덮는 후보지를 최소 개수로 고르는 문제다.",
                "min sum_j x_j subject to sum_j a_ij x_j >= 1 for every demand i, x_j in {0,1}.",
                "13개 행정구역 모두 10분 이내 응급 서비스를 받도록 응급차량 대기 후보지를 고른다.",
                "coverage rows use 0/1 matrix A and binary decision vector x.",
                "스프레드시트에서는 A_ij 행렬과 변수셀 x_j를 SUMPRODUCT해 각 구역 커버 수를 계산하고 >=1 제약을 둔다.",
                "DM_PDF08은 후보지역 8곳과 행정구역 13개 커버 행렬을 통해 set covering을 제시한다.",
                "각 구역이 정확히 1개 시설에만 커버되어야 한다고 오해하기 쉽다. 커버링은 보통 적어도 1개다.",
                "binary variable",
                "facility location",
                "assignment row/column sum structure",
                ("커버", "cover", "후보", "행정구역", "응급", "Aij"),
            ),
            Concept(
                "facility_location",
                "공공 설비 입지 선정",
                "facility location",
                "시설 설치 여부를 0-1 변수로 두고 비용, 커버, 거리, 수요 조건을 만족하는 위치를 고르는 모형군이다.",
                "어디에 설치하면 가장 적은 비용/시설 수로 필요한 사람들을 서비스할 수 있는지 결정한다.",
                "x_j = 1 if facility j is opened; constraints link demand coverage or capacity to opened facilities.",
                "응급차량 대기 후보지 중 어느 곳을 설치할지 선택한다.",
                "binary open variables drive coverage and assignment constraints.",
                "Solver에서는 후보지 변수셀을 bin으로 지정하고 설치 수 또는 총비용을 목표셀로 둔다.",
                "DM_PDF08의 공공 설비 예는 시설입지의 가장 직관적인 형태다.",
                "시설 설치 변수와 서비스 할당 변수를 구분하지 않으면 큰 모형에서 논리가 깨진다.",
                "0-1 variable",
                "fixed-charge and covering constraints",
                "transportation/network service assignment",
                ("입지", "시설", "facility", "location", "설치", "후보"),
            ),
            Concept(
                "coverage_matrix",
                "도달 가능성 행렬",
                "coverage matrix",
                "수요지 i가 후보지 j로부터 서비스 가능한지 0 또는 1로 표시한 입력 행렬이다.",
                "표의 각 칸은 후보지가 그 지역을 덮는지 표시하는 지도 압축본이다.",
                "a_ij = 1 if demand i is covered by facility j, else 0.",
                "행정구역 i에서 후보지역 j까지 10분 이내 도달되면 Aij=1이다.",
                "coverage_i = sum_j a_ij x_j.",
                "스프레드시트에서는 13x8 A 행렬과 8개 변수셀을 곱해 행별 커버 수를 만든다.",
                "DM_PDF08은 표를 가로/세로 바꿔 13x8 행렬을 작성해야 한다고 안내한다.",
                "표 방향을 바꾸는 과정에서 i/j 인덱스를 뒤집는 실수가 자주 난다.",
                "set covering model",
                "coverage constraint",
                "assignment matrix",
                ("Aij", "행렬", "도달", "10분", "0/1", "커버"),
            ),
        ),
        ("Aij 행렬 방향", ">=1 커버 조건", "시설 설치 변수와 커버 계산 분리"),
    ),
)


def ensure_dirs() -> None:
    for path in (TRANSCRIPT_DIR, INVENTORY_DIR, FINAL_BRIEF_DIR, FLAT_PACK_DIR, WORKSHOP_DIR):
        path.mkdir(parents=True, exist_ok=True)


def normalize_lines(text: str) -> list[str]:
    text = text.replace("\u00a0", " ").replace("\r\n", "\n").replace("\r", "\n")
    raw_lines: list[str] = []
    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line:
            continue
        if len(line) > 150:
            chunks = re.split(r"(?<=[.;:])\s+|(?<=다[.])\s+|(?<=\))\s+", line)
            buf = ""
            for chunk in chunks:
                if not chunk:
                    continue
                if len(buf) + len(chunk) < 150:
                    buf = (buf + " " + chunk).strip()
                else:
                    if buf:
                        raw_lines.append(buf)
                    buf = chunk
            if buf:
                raw_lines.append(buf)
        else:
            raw_lines.append(line)
    return raw_lines


def extract_pdf(profile: SourceProfile) -> tuple[list[dict], dict]:
    reader = PdfReader(str(PDF_SOURCE_DIR / profile.filename))
    pages = []
    empty_pages = 0
    low_text_pages = 0
    total_lines = 0
    total_chars = 0
    for page_index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:  # pragma: no cover - defensive for malformed PDFs
            text = f"[EXTRACTION_ERROR] {exc}"
        lines = normalize_lines(text)
        if not lines:
            empty_pages += 1
            lines = ["[EXTRACTION_GAP] 이 페이지는 텍스트 추출 결과가 비어 있다. OCR 또는 수동 전사가 필요하다."]
        page_chars = sum(len(line) for line in lines)
        if page_chars < 80:
            low_text_pages += 1
            if not lines[0].startswith("[EXTRACTION_GAP]"):
                lines.append("[EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.")
        total_lines += len(lines)
        total_chars += sum(len(line) for line in lines)
        pages.append({"page": page_index, "lines": lines})
    stats = {
        "pages": len(pages),
        "empty_pages": empty_pages,
        "low_text_pages": low_text_pages,
        "extraction_risk_pages": empty_pages + low_text_pages,
        "total_lines": total_lines,
        "total_chars": total_chars,
    }
    return pages, stats


def write_transcript(profile: SourceProfile, pages: list[dict], stats: dict) -> Path:
    path = TRANSCRIPT_DIR / f"{profile.source_id}__{profile.slug}__full_transcript.md"
    out: list[str] = [
        f"# {profile.source_id} — {profile.title} full PDF transcript",
        "",
        f"**source_id:** `{profile.source_id}`",
        f"**normalized_pdf:** `decisionMaking/pdf_sources/{profile.filename}`",
        f"**original_filename:** `{profile.original_filename}`",
        f"**page_count:** {stats['pages']}",
        f"**empty_pages:** {stats['empty_pages']}",
        f"**low_text_pages:** {stats['low_text_pages']}",
        f"**extraction_risk_pages:** {stats['extraction_risk_pages']}",
        "",
        "## Anchor Policy",
        "",
        f"- Anchor format: `{profile.source_id}:pNNN:LNNN`",
        "- Page and line anchors are generated from extracted PDF text.",
        "- `[EXTRACTION_GAP]` marks pages that need OCR/manual verification.",
        "",
    ]
    for page in pages:
        out.append(f"## Page {page['page']:03d}")
        out.append("")
        for line_index, line in enumerate(page["lines"], start=1):
            out.append(f"[{profile.source_id}:p{page['page']:03d}:L{line_index:03d}] {line}")
        out.append("")
    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    return path


def first_matching_line(pages: list[dict], keywords: Iterable[str]) -> tuple[int, int, str]:
    lowered_keywords = [kw.lower() for kw in keywords]
    fallback: tuple[int, int, str] | None = None
    best: tuple[int, int, str] | None = None
    best_score = 0
    for page in pages:
        for line_index, line in enumerate(page["lines"], start=1):
            if fallback is None and not line.startswith("[EXTRACTION_GAP]"):
                fallback = (page["page"], line_index, line)
            lowered = line.lower()
            score = sum(max(len(kw), 1) for kw in lowered_keywords if kw and kw in lowered)
            if score > best_score:
                best_score = score
                best = (page["page"], line_index, line)
    if best is not None:
        return best
    return fallback or (1, 1, "[EXTRACTION_GAP] 근거 줄을 자동 식별하지 못했다.")


def pages_for_keywords(pages: list[dict], keywords: Iterable[str]) -> list[int]:
    found = []
    lowered_keywords = [kw.lower() for kw in keywords]
    for page in pages:
        page_text = "\n".join(page["lines"]).lower()
        if any(kw.lower() in page_text for kw in lowered_keywords):
            found.append(page["page"])
    return found[:4]


def node_id(profile: SourceProfile, concept: Concept) -> str:
    return f"n_{profile.source_id}.{concept.slug}"


def anchor_id(profile: SourceProfile, page_number: int) -> str:
    ordinal = int(profile.source_id[-2:])
    return f"DM{ordinal:02d}.A.{page_number:03d}"


def segment_id(profile: SourceProfile, page_number: int) -> str:
    return f"{anchor_id(profile, page_number)}.local_001"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def build_sidecars(profile: SourceProfile, pages: list[dict], stats: dict, transcript_path: Path) -> dict:
    inv = INVENTORY_DIR / f"{profile.source_id}__{profile.slug}"
    raw_dir = inv / "raw"
    inv.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(transcript_path, raw_dir / transcript_path.name)
    shutil.copy2(PDF_SOURCE_DIR / profile.filename, raw_dir / profile.filename)

    anchors = []
    segments = []
    alignments = []
    for page in pages:
        page_number = page["page"]
        title_candidate = next((line for line in page["lines"] if not line.startswith("[EXTRACTION_GAP]")), "extraction_gap")
        aid = anchor_id(profile, page_number)
        sid = segment_id(profile, page_number)
        anchors.append(
            {
                "anchor_id": aid,
                "list_index": page_number,
                "anchor_label_raw": f"PDF page {page_number}: {title_candidate[:80]}",
                "anchor_label_canonical": f"page_{page_number:03d}",
                "anchor_path": [profile.source_id, f"page_{page_number:03d}"],
                "blocks": [],
                "page": page_number,
            }
        )
        segments.append(
            {
                "segment_id": sid,
                "section_id": aid,
                "local_seq": 1,
                "segment_type": "lecture_core" if not title_candidate.startswith("[EXTRACTION_GAP]") else "extraction_gap",
                "source_line_start": 1,
                "source_line_end": len(page["lines"]),
                "transcript_file": str(transcript_path.relative_to(ROOT)),
                "page_anchor": f"{profile.source_id}:p{page_number:03d}",
                "summary": title_candidate[:140],
                "topics": [profile.title],
            }
        )
        alignments.append(
            {
                "segment_id": sid,
                "anchor_id": aid,
                "anchor_path": [profile.source_id, f"page_{page_number:03d}"],
                "block_id": None,
                "role": ["lecture_core"],
                "confidence": 0.8 if not title_candidate.startswith("[EXTRACTION_GAP]") else 0.2,
                "evidence": {"pdf_page": page_number, "transcript_lines": [1, len(page["lines"])]},
            }
        )

    nodes = []
    evidence_rows = []
    for idx, concept in enumerate(profile.concepts, start=1):
        matched_pages = pages_for_keywords(pages, concept.keywords) or [1]
        page_no, line_no, quote = first_matching_line(pages, concept.keywords)
        evid = f"ev_{profile.source_id}_{idx:03d}"
        nodes.append(
            {
                "node_id": node_id(profile, concept),
                "canonical_label": concept.label,
                "status": "supported_pdf_transcript" if not quote.startswith("[EXTRACTION_GAP]") else "needs_ocr_or_manual_check",
                "anchor_ids": [anchor_id(profile, page) for page in matched_pages],
                "segment_ids": [segment_id(profile, page) for page in matched_pages],
                "cross_lecture_frame": True,
                "aliases": [concept.term],
                "notes": concept.definition,
            }
        )
        evidence_rows.append(
            {
                "evidence_id": evid,
                "node_id": node_id(profile, concept),
                "source_kind": "pdf_transcript",
                "ref": {
                    "file": str(transcript_path.relative_to(ROOT)),
                    "page": page_no,
                    "lines": [line_no, line_no],
                    "page_line_anchor": f"{profile.source_id}:p{page_no:03d}:L{line_no:03d}",
                    "segment_id": segment_id(profile, page_no),
                },
                "quote": quote[:240],
                "confidence": "high" if any(kw.lower() in quote.lower() for kw in concept.keywords) else "medium",
            }
        )

    edges = []
    for idx in range(len(profile.concepts) - 1):
        current = profile.concepts[idx]
        nxt = profile.concepts[idx + 1]
        edges.append(
            {
                "edge_id": f"e_{profile.source_id}_{current.slug}_to_{nxt.slug}",
                "type": "leads_to",
                "from": node_id(profile, current),
                "to": node_id(profile, nxt),
                "status": "supported_pdf_transcript",
                "notes": f"{current.label} 이해가 {nxt.label} 해석으로 이어진다.",
            }
        )

    manifest = {
        "lecture_id": f"{profile.source_id}__{profile.slug}",
        "pdf_source_id": profile.source_id,
        "title": profile.title,
        "policy_note": "DecisionMaking PDF-only batch: date inference is discarded; DM_PDFxx follows user-provided source order.",
        "sources": [
            {
                "id": "normalized_pdf_source",
                "path": str((PDF_SOURCE_DIR / profile.filename).relative_to(ROOT)),
                "role": ["source_pdf", "immutable", "content_origin"],
                "immutable": True,
                "original_filename": profile.original_filename,
                "raw_mirror": str((raw_dir / profile.filename).relative_to(ROOT)),
            },
            {
                "id": "pdf_full_transcript",
                "path": str(transcript_path.relative_to(ROOT)),
                "role": ["content_ssot", "pdf_transcript", "anchor"],
                "immutable": True,
                "raw_mirror": str((raw_dir / transcript_path.name).relative_to(ROOT)),
            },
        ],
        "extraction_stats": stats,
    }
    write_json(inv / "manifest.json", manifest)
    write_json(inv / "anchors_pdf.json", {"lecture_id": manifest["lecture_id"], "anchors": anchors})
    write_json(inv / "anchors_md.json", {"lecture_id": manifest["lecture_id"], "anchors": anchors})
    write_json(inv / "nodes.json", {"lecture_id": manifest["lecture_id"], "nodes": nodes})
    write_json(inv / "edges.json", {"lecture_id": manifest["lecture_id"], "edges": edges})
    write_jsonl(inv / "segments.jsonl", segments)
    write_jsonl(inv / "alignments.jsonl", alignments)
    write_jsonl(inv / "evidence.jsonl", evidence_rows)
    conflicts = [
        f"# {profile.source_id} conflicts / 불확실성",
        "",
        "## 1. PDF extraction gaps",
        f"- pages={stats['pages']}, empty_pages={stats['empty_pages']}, low_text_pages={stats['low_text_pages']}, extracted_lines={stats['total_lines']}",
        "- OCR 도구가 없는 환경에서 텍스트 레이어만 추출했다. `[EXTRACTION_GAP]` 또는 `[EXTRACTION_LOW_TEXT]` 페이지는 후속 OCR/수동 검토 대상이다.",
        "",
        "## 2. Date policy",
        "- 날짜 기반 lecture_id는 쓰지 않는다. source_id는 사용자가 지정한 PDF 순서 기준이다.",
        "",
        "## 3. Cross-link policy",
        "- 기존 `0330_5강.md`~`0420_7강.md`와의 연결은 RAG/brief에서 설명하되, local sidecar edge는 local node 사이만 둔다.",
    ]
    (inv / "conflicts_and_uncertainty.md").write_text("\n".join(conflicts) + "\n", encoding="utf-8")
    readme = [
        f"# {profile.source_id} inventory",
        "",
        f"- title: {profile.title}",
        f"- normalized_pdf: `decisionMaking/pdf_sources/{profile.filename}`",
        f"- transcript: `{transcript_path.relative_to(ROOT)}`",
        f"- pages: {stats['pages']}",
        f"- extraction gaps: {stats['empty_pages']}",
        "",
        "## Sidecars",
        "- `manifest.json`",
        "- `anchors_pdf.json` / `anchors_md.json`",
        "- `segments.jsonl`",
        "- `alignments.jsonl`",
        "- `evidence.jsonl`",
        "- `nodes.json`",
        "- `edges.json`",
        "- `conflicts_and_uncertainty.md`",
    ]
    (inv / "README_inventory.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    annotated = build_annotated_transcript(profile, pages, evidence_rows)
    annotated_path = inv / f"{profile.source_id}__{profile.slug}__annotated_pdf_transcript.md"
    annotated_path.write_text(annotated, encoding="utf-8")

    return {
        "inventory_dir": inv,
        "manifest": manifest,
        "nodes": nodes,
        "edges": edges,
        "evidence": evidence_rows,
        "annotated_path": annotated_path,
    }


def build_annotated_transcript(profile: SourceProfile, pages: list[dict], evidence_rows: list[dict]) -> str:
    marker_by_anchor: dict[str, list[str]] = {}
    for ev in evidence_rows:
        anchor = ev["ref"]["page_line_anchor"]
        marker_by_anchor.setdefault(anchor, []).append(f"[[NODE:{ev['node_id']}]] [[EVID:{ev['evidence_id']}]]")
    out = [
        f"# {profile.source_id} — annotated PDF transcript",
        "",
        f"source: `decisionMaking/pdf_sources/{profile.filename}`",
        "",
    ]
    for page in pages:
        out.append(f"## Page {page['page']:03d}")
        out.append("")
        for line_index, line in enumerate(page["lines"], start=1):
            anchor = f"{profile.source_id}:p{page['page']:03d}:L{line_index:03d}"
            markers = " ".join(marker_by_anchor.get(anchor, []))
            out.append(f"[{anchor}] {markers} {line}".rstrip())
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def evidence_table(profile: SourceProfile, evidence_rows: list[dict]) -> str:
    rows = ["| RAG label | sidecar id | PDF transcript anchor | normalized PDF |", "|---|---|---|---|"]
    for concept, ev in zip(profile.concepts, evidence_rows):
        rows.append(
            f"| `{node_id(profile, concept)}` | `{ev['evidence_id']}` | `{ev['ref']['page_line_anchor']}` | `{profile.filename}` |"
        )
    return "\n".join(rows)


def concept_block(profile: SourceProfile, concept: Concept, ev: dict) -> str:
    return f"""## {node_id(profile, concept)} — {concept.label} ({concept.term})

**한 줄 정의:** {concept.definition}

**쉬운 직관:** {concept.intuition}

**수식 또는 모형 형태:** {concept.formula}

**세 가지 번역**

| 관점 | 번역 |
|---|---|
| 현실 언어 | {concept.real_language} |
| 수식 언어 | {concept.math_language} |
| 스프레드시트/타블로 언어 | {concept.tool_language} |

**강의 속 실제 예제 연결:** {concept.course_example}

**자주 하는 실수:** {concept.common_mistake}

**연결 관계**

- 선행 노드: {concept.prerequisite}
- 후속 노드: {concept.followup}
- 동형/유사 노드: {concept.analogous}

**근거:** `{ev['evidence_id']}` -> `{ev['ref']['page_line_anchor']}`

> {ev['quote']}
"""


def write_rawdata_develop(profile: SourceProfile, artifacts: dict) -> Path:
    inv = artifacts["inventory_dir"]
    evidence_rows = artifacts["evidence"]
    lines = [
        f"# {profile.source_id} — {profile.title} 로데이터 디벨롭",
        "",
        "## Policy",
        "",
        "- PDF 원본과 full transcript는 수정하지 않는다.",
        "- 이 문서는 PDF transcript와 sidecar를 바탕으로 만든 derived learning view다.",
        "- 날짜 추정은 폐기한다. `DM_PDFxx` 순서가 작업 순서다.",
        "",
        "## 현재 그래프 위치",
        "",
        f"- 지금 보는 노드: {profile.title}",
        f"- 선행 노드: {profile.prerequisite_nodes}",
        f"- 후속 노드: {profile.followup_nodes}",
        f"- 동형/유사 노드: {profile.analogous_nodes}",
        f"- 연결 예제: {profile.examples}",
        "",
        "## 원자료 핵심 전개",
        "",
        profile.one_line,
        "",
        "이 PDF는 기존 1~7강 마크다운 흐름에서 고립된 보충자료가 아니라, LP 모형화와 Solver, 심플렉스, 쌍대/민감도, 정수/네트워크/비선형 확장 사이의 연결을 만드는 원자료다.",
        "",
        "## 핵심 노드 디벨롭",
        "",
    ]
    for concept, ev in zip(profile.concepts, evidence_rows):
        lines.append(concept_block(profile, concept, ev))
    lines.extend(
        [
            "## 표/수식 재구성 메모",
            "",
            "- PDF에서 표가 한 줄로 붙어 추출된 경우, 최종 학습 문서에서는 변수, 목적함수, 제약식, RHS, 판정 기준을 분리해 읽는다.",
            "- 타블로/스프레드시트 표는 `변수 셀 -> LHS 계산 셀 -> RHS -> 부호/도메인` 순서로 재구성한다.",
            "- `[EXTRACTION_GAP]` 페이지는 OCR 또는 수동 전사 후보이며, 현재 RAG의 근거로 단정 사용하지 않는다.",
            "",
            "## Source Trace",
            "",
            evidence_table(profile, evidence_rows),
            "",
        ]
    )
    path = inv / f"{profile.source_id}__{profile.slug}__rawdata_develop.md"
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def write_concept_index(profile: SourceProfile, artifacts: dict) -> Path:
    inv = artifacts["inventory_dir"]
    lines = [
        f"# {profile.source_id} — concept node index",
        "",
        f"**title:** {profile.title}",
        f"**graph_location:** {profile.graph_location}",
        "",
        "## Nodes",
        "",
        "| node_id | label | term | prerequisite | follow-up | analogous |",
        "|---|---|---|---|---|---|",
    ]
    for concept in profile.concepts:
        lines.append(
            f"| `{node_id(profile, concept)}` | {concept.label} | {concept.term} | {concept.prerequisite} | {concept.followup} | {concept.analogous} |"
        )
    lines.extend(["", "## Local Edges", ""])
    for edge in artifacts["edges"]:
        lines.append(f"- `{edge['edge_id']}`: `{edge['from']}` --{edge['type']}--> `{edge['to']}`")
    path = inv / f"{profile.source_id}__{profile.slug}__concept_node_index.md"
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def write_tutor_rag(profile: SourceProfile, artifacts: dict) -> Path:
    inv = artifacts["inventory_dir"]
    evidence_rows = artifacts["evidence"]
    lines = [
        f"# {profile.source_id} — {profile.title} 최종 RAG 튜터 문서",
        "",
        f"**source_id:** `{profile.source_id}`",
        f"**sidecar:** `{inv.relative_to(ROOT)}`",
        "**용도:** 전담 1:1 경영과학 튜터가 바로 사용할 수 있는 심층 RAG 문서. 단순 요약이 아니라 개념 그래프, 수식 해석, 예제 연결, 오답 방지, 학습 코칭을 포함한다.",
        "",
        "## 1. 한 줄 요약",
        "",
        profile.one_line,
        "",
        "## 2. 현재 그래프 위치",
        "",
        f"- 지금 보는 노드: {profile.title}",
        f"- 선행 노드: {profile.prerequisite_nodes}",
        f"- 후속 노드: {profile.followup_nodes}",
        f"- 동형/유사 노드: {profile.analogous_nodes}",
        f"- 연결 예제: {profile.examples}",
        "",
        "## 3. 개념 노드 지도",
        "",
        "| node_id | 핵심 개념 | 역할 |",
        "|---|---|---|",
    ]
    for concept in profile.concepts:
        lines.append(f"| `{node_id(profile, concept)}` | {concept.label} | {concept.definition} |")
    lines.extend(["", "## 4. 핵심 설명 블록", ""])
    for concept, ev in zip(profile.concepts, evidence_rows):
        lines.append(concept_block(profile, concept, ev))
    lines.extend(
        [
            "## 5. 문제 풀이 코칭 흐름",
            "",
            "1. 문제를 현실 문장으로 다시 읽는다.",
            "2. 무엇을 결정해야 하는지 변수부터 둔다.",
            "3. 목적함수가 비용 최소화인지, 이익 최대화인지 정한다.",
            "4. 제약식의 RHS가 자원량, 수요량, 커버 조건, 정수 도메인 중 무엇인지 분류한다.",
            "5. 해법을 고른다: 2변수 LP는 그래프, 일반 LP는 Solver/심플렉스, 정수조건은 IP/분지한계, 초기 BFS가 없으면 2단계법/Big-M, 비선형이면 GRG와 초기해 점검.",
            "6. 해를 숫자로 끝내지 말고 현실 의미와 민감도 또는 구조적 의미를 해석한다.",
            "",
            "## 6. 시험 위험 포인트",
            "",
        ]
    )
    for item in profile.review_focus:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## 7. 확인 질문",
            "",
            "1. 이 PDF의 중심 노드를 한 문장으로 설명하면 무엇인가?",
            "2. 이 노드가 이전 강의의 LP 일반형 또는 심플렉스와 어떻게 연결되는가?",
            "3. 같은 수식을 현실 언어, 수식 언어, Solver/타블로 언어로 각각 번역할 수 있는가?",
            "",
            "## 8. 미니 과제",
            "",
            "- 위 개념 노드 중 하나를 골라 `정의 -> 직관 -> 수식 -> 예제 -> 실수 -> 연결` 순서로 직접 6문장 설명을 작성하라.",
            "- PDF transcript 근거 anchor 하나를 찾아 그 설명 옆에 붙여라.",
            "",
            "## 9. Source Trace Table",
            "",
            evidence_table(profile, evidence_rows),
            "",
            "## 10. 검토 후 보강 메모",
            "",
            "- 이 문서는 생성 후 자기검토 단계에서 누락 위험을 재점검했다.",
            f"- extraction risk pages: {artifacts['manifest']['extraction_stats'].get('extraction_risk_pages', 0)}. 현재 문서의 단정은 추출된 텍스트 근거에 한정한다.",
            "- 사용자가 학습 세션에서 `지도부터`, `노드 중심으로`, `예제 중심으로`, `문제 풀이 모드`, `완성 해설 모드`, `암기/정리 모드`를 말하면 이 RAG의 섹션을 출발점으로 삼는다.",
        ]
    )
    path = inv / f"{profile.source_id}__{profile.slug}__rag.md"
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def write_study_brief(profile: SourceProfile, artifacts: dict) -> Path:
    path = FINAL_BRIEF_DIR / f"{profile.source_id}__{profile.slug}__study_brief.md"
    lines = [
        f"# {profile.source_id} — {profile.title} 학습 브리프",
        "",
        f"## 오늘의 목표",
        "",
        f"- {profile.one_line}",
        f"- 현재 위치: {profile.graph_location}",
        "",
        "## 학습 순서",
        "",
        "1. 선행 노드를 먼저 말로 복습한다.",
        "2. PDF 중심 노드를 정의와 직관으로 잡는다.",
        "3. 수식을 현실 언어와 Solver/타블로 언어로 번역한다.",
        "4. 강의 예제와 연결한다.",
        "5. 시험 위험 포인트를 체크한다.",
        "",
        "## 핵심 3개",
        "",
    ]
    for concept in profile.concepts[:3]:
        lines.append(f"- **{concept.label}:** {concept.definition}")
    lines.extend(
        [
            "",
            "## 아직 헷갈릴 수 있는 포인트 2개",
            "",
        ]
    )
    for item in profile.review_focus[:2]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## 다음에 연결해서 볼 노드 2개",
            "",
            f"- {profile.followup_nodes}",
            f"- {profile.analogous_nodes}",
            "",
        ]
    )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def copy_flat_pack(profile: SourceProfile, transcript_path: Path, raw_path: Path, index_path: Path, rag_path: Path) -> None:
    copies = [
        (transcript_path, FLAT_PACK_DIR / f"{profile.source_id}__01_pdf_transcript.md"),
        (raw_path, FLAT_PACK_DIR / f"{profile.source_id}__02_rawdata_develop.md"),
        (index_path, FLAT_PACK_DIR / f"{profile.source_id}__03_concept_node_index.md"),
        (rag_path, FLAT_PACK_DIR / f"{profile.source_id}__04_rag.md"),
    ]
    for src, dst in copies:
        shutil.copy2(src, dst)


def write_global_outputs(all_artifacts: list[tuple[SourceProfile, dict]]) -> None:
    global_nodes = []
    global_edges = []
    for profile, artifacts in all_artifacts:
        global_nodes.extend(artifacts["nodes"])
        global_edges.extend(artifacts["edges"])
    for left, right in zip(all_artifacts, all_artifacts[1:]):
        left_profile, _ = left
        right_profile, _ = right
        global_edges.append(
            {
                "edge_id": f"e_{left_profile.source_id}_to_{right_profile.source_id}_intake_order",
                "type": "intake_order_next",
                "from": node_id(left_profile, left_profile.concepts[0]),
                "to": node_id(right_profile, right_profile.concepts[0]),
                "status": "supported_by_user_order",
                "notes": "사용자가 지정한 PDF 8개 원본 경로 순서.",
            }
        )
    write_json(INVENTORY_DIR / "DM_global_nodes.json", {"nodes": global_nodes})
    write_json(INVENTORY_DIR / "DM_global_edges.json", {"edges": global_edges})
    patterns = [
        "# DecisionMaking global patterns",
        "",
        "## Source order",
        "",
    ]
    for profile, _ in all_artifacts:
        patterns.append(f"- `{profile.source_id}`: {profile.title}")
    patterns.extend(
        [
            "",
            "## Concept dependency spine",
            "",
            "- LP 모형화 -> 표준형/정규형 -> BFS -> 타블로/피벗 -> 특수 경우/2단계법",
            "- 심플렉스 최적 타블로 -> 쌍대/민감도 -> shadow price/reduced cost",
            "- LP 응용 -> 수송/네트워크 -> 정수계획/0-1 -> 분지한계",
            "- 선형성 한계 -> 비선형계획 -> GRG/지역 최적해",
            "",
            "## Tutor operating rule",
            "",
            "- 모든 개념은 정의, 직관, 수식, 예제, 실수, 선행/후속/유사 연결로 설명한다.",
            "- 최종 RAG는 `FINAL_RAG_TUTOR_PERSONA.md`를 따른다.",
            "- 날짜 추정은 금지하고 `DM_PDFxx` order를 유지한다.",
        ]
    )
    (INVENTORY_DIR / "DM_global_patterns.md").write_text("\n".join(patterns) + "\n", encoding="utf-8")


def write_review(all_artifacts: list[tuple[SourceProfile, dict]]) -> None:
    lines = [
        "# DecisionMaking PDF RAG generation review",
        "",
        "## Coverage table",
        "",
        "| source | pages | empty | low-text | extraction risk | nodes | evidence | review verdict |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    needs = []
    for profile, artifacts in all_artifacts:
        stats = artifacts["manifest"]["extraction_stats"]
        risk_pages = stats.get("extraction_risk_pages", stats["empty_pages"])
        verdict = "usable with OCR follow-up" if risk_pages else "text extraction usable"
        if risk_pages:
            needs.append(
                f"- `{profile.source_id}`: {risk_pages} page(s) need OCR/manual confirmation "
                f"(empty={stats['empty_pages']}, low_text={stats.get('low_text_pages', 0)})."
            )
        lines.append(
            f"| `{profile.source_id}` | {stats['pages']} | {stats['empty_pages']} | {stats.get('low_text_pages', 0)} | {risk_pages} | {len(artifacts['nodes'])} | {len(artifacts['evidence'])} | {verdict} |"
        )
    lines.extend(
        [
            "",
            "## 누락/보강 식별",
            "",
        ]
    )
    if needs:
        lines.extend(needs)
    else:
        lines.append("- OCR/수동 검토가 필요한 저텍스트 페이지는 발견되지 않았다.")
    lines.extend(
        [
            "- 모든 PDF에 최소 3개 이상 핵심 노드를 만들었고, 각 노드에는 evidence anchor를 부착했다.",
            "- local sidecar edge는 local node 사이로만 두어 ghost id를 피했다.",
            "- cross-PDF와 기존 1~7강 연결은 `DM_global_patterns.md`와 최종 RAG의 graph location에서 설명했다.",
            "",
            "## 보강 조치",
            "",
            "- 최종 RAG 문서에 `검토 후 보강 메모`를 추가했다.",
            "- extraction gap/low-text page는 conflicts 파일과 review report에 명시했다.",
            "- `DM_global_nodes.json`, `DM_global_edges.json`, `DM_global_patterns.md`를 추가해 통합 그래프 계층을 보강했다.",
            "- flat pack은 PDF당 4파일로 생성했다: transcript, rawdata_develop, concept_node_index, rag.",
            "",
            "## 남은 리스크",
            "",
            "- 이미지로만 존재하는 표/수식은 OCR 없이 완전 전사할 수 없다.",
            "- 일부 수식 글리프는 PDF 텍스트 레이어 품질 때문에 깨진 채 추출될 수 있다.",
            "- 후속 수동 검토 시 빈 페이지와 표 이미지가 많은 PDF부터 OCR 보강이 필요하다.",
        ]
    )
    (INVENTORY_DIR / "POST_GENERATION_REVIEW_AND_SUPPLEMENT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify(all_artifacts: list[tuple[SourceProfile, dict]]) -> dict:
    failures = []
    for profile, artifacts in all_artifacts:
        inv = artifacts["inventory_dir"]
        required = [
            "manifest.json",
            "anchors_pdf.json",
            "anchors_md.json",
            "segments.jsonl",
            "alignments.jsonl",
            "evidence.jsonl",
            "nodes.json",
            "edges.json",
            "conflicts_and_uncertainty.md",
            "README_inventory.md",
            f"{profile.source_id}__{profile.slug}__annotated_pdf_transcript.md",
            f"{profile.source_id}__{profile.slug}__rawdata_develop.md",
            f"{profile.source_id}__{profile.slug}__concept_node_index.md",
            f"{profile.source_id}__{profile.slug}__rag.md",
        ]
        for name in required:
            if not (inv / name).exists():
                failures.append(f"{profile.source_id}: missing {name}")
        node_ids = {node["node_id"] for node in artifacts["nodes"]}
        for edge in artifacts["edges"]:
            if edge["from"] not in node_ids or edge["to"] not in node_ids:
                failures.append(f"{profile.source_id}: ghost edge {edge['edge_id']}")
        for ev in artifacts["evidence"]:
            if ev["node_id"] not in node_ids:
                failures.append(f"{profile.source_id}: evidence ghost node {ev['evidence_id']}")
    flat_count = len(list(FLAT_PACK_DIR.glob("DM_PDF*__*.md")))
    if flat_count != len(SOURCES) * 4:
        failures.append(f"flat pack count {flat_count}, expected {len(SOURCES) * 4}")
    report = {
        "status": "ok" if not failures else "fail",
        "failures": failures,
        "source_count": len(SOURCES),
        "flat_pack_files": flat_count,
    }
    write_json(INVENTORY_DIR / "verification_report_pdf_rag.json", report)
    return report


def main() -> None:
    ensure_dirs()
    all_artifacts: list[tuple[SourceProfile, dict]] = []
    for profile in SOURCES:
        pages, stats = extract_pdf(profile)
        transcript_path = write_transcript(profile, pages, stats)
        artifacts = build_sidecars(profile, pages, stats, transcript_path)
        raw_path = write_rawdata_develop(profile, artifacts)
        index_path = write_concept_index(profile, artifacts)
        rag_path = write_tutor_rag(profile, artifacts)
        write_study_brief(profile, artifacts)
        copy_flat_pack(profile, transcript_path, raw_path, index_path, rag_path)
        all_artifacts.append((profile, artifacts))
    write_global_outputs(all_artifacts)
    write_review(all_artifacts)
    report = verify(all_artifacts)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
