"""
축구공 동적 생산-재고 계획 (해답 3-13)
슬라이드 스프레드시트 재현 + 수식 해설 시트 + 제약·인과 설명
"""

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# ════════════════════════════════════════════════════════════
# 스타일 정의
# ════════════════════════════════════════════════════════════
bold = Font(bold=True)
bold_red = Font(bold=True, color="FF0000")
bold_blue = Font(bold=True, color="0000FF")
bold_green = Font(bold=True, color="006600")
bold_purple = Font(bold=True, color="660099")
header_font = Font(bold=True, size=12)
title_font = Font(bold=True, size=14, color="FF0000")
section_font = Font(bold=True, size=11, color="333399")

yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
light_yellow = PatternFill(start_color="FFFFCC", end_color="FFFFCC", fill_type="solid")
light_gray = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
light_blue = PatternFill(start_color="DAEEF3", end_color="DAEEF3", fill_type="solid")
light_green = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
light_red = PatternFill(start_color="FCE4EC", end_color="FCE4EC", fill_type="solid")
light_purple = PatternFill(start_color="E8DAEF", end_color="E8DAEF", fill_type="solid")

thin_border = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin"),
)
blue_border = Border(
    left=Side(style="medium", color="0000FF"), right=Side(style="medium", color="0000FF"),
    top=Side(style="medium", color="0000FF"), bottom=Side(style="medium", color="0000FF"),
)
red_border = Border(
    left=Side(style="medium", color="FF0000"), right=Side(style="medium", color="FF0000"),
    top=Side(style="medium", color="FF0000"), bottom=Side(style="medium", color="FF0000"),
)
center = Alignment(horizontal="center", vertical="center")
wrap = Alignment(horizontal="left", vertical="top", wrap_text=True)
num2 = "0.00"
num_comma = "#,##0.00"


def sc(ws, row, col, value, font=None, fill=None, align=None, fmt=None, border=None):
    """set_cell 헬퍼"""
    cell = ws.cell(row=row, column=col, value=value)
    if font: cell.font = font
    if fill: cell.fill = fill
    if align: cell.alignment = align
    if fmt: cell.number_format = fmt
    if border: cell.border = border
    return cell


months = ["1월", "2월", "3월", "4월", "5월", "6월"]
prod_costs = [12.50, 12.55, 12.70, 12.80, 12.85, 12.95]
demands = [10, 15, 30, 35, 25, 10]
initial_production = [5, 20, 30, 30, 25, 10]

# ════════════════════════════════════════════════════════════
# Sheet 1: 모형 (해답 3-13)
# ════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "모형"

ws.column_dimensions["A"].width = 22
for c in "BCDEFG":
    ws.column_dimensions[c].width = 12
ws.column_dimensions["H"].width = 10
ws.column_dimensions["I"].width = 45

# ── 행 1: 제목 ──
sc(ws, 1, 1, "해답 3-13  축구공 동적 생산-재고 계획", title_font)

# ── 행 2: Balance Equation 주석 (노란 박스) ──
ws.merge_cells("D2:G2")
c2 = ws.cell(row=2, column=4,
    value="월말재고(C22) = 전월말재고(B22) + 당월 생산량(C14) – 당월 수요량(C18)")
c2.font = Font(bold=True, color="FF0000", size=9)
c2.fill = light_yellow
c2.alignment = Alignment(horizontal="center", wrap_text=True)

# ── 행 3~6: 파라미터 ──
sc(ws, 3, 1, "월 최대 생산용량", bold)
sc(ws, 3, 2, 30, bold)
sc(ws, 3, 3, "천개")
sc(ws, 3, 9, "← 제약: x_t ≤ 30 (생산 상한)", bold_green)

sc(ws, 4, 1, "월 최대 재고용량", bold)
sc(ws, 4, 2, 10, bold)
sc(ws, 4, 3, "천개")
sc(ws, 4, 9, "← 제약: y_t ≤ 10 (재고 상한)", bold_green)

sc(ws, 5, 1, "1월초 재고 (y₀)", bold)
sc(ws, 5, 2, 5, bold)
sc(ws, 5, 3, "천개")
sc(ws, 5, 9, "← 초기조건: Balance Eq.의 시작점", bold_green)

sc(ws, 6, 1, "재고단가 비율", bold)
sc(ws, 6, 2, 0.05, bold)
ws["B6"].number_format = "0%"
ws["B6"].fill = yellow_fill
sc(ws, 6, 3, "(생산단가의)")
sc(ws, 6, 9, "← h_t = 0.05 × c_t (재고비 = 단가의 5%)", bold_green)

# ── 행 8~10: 월별 단가 ──
for i, m in enumerate(months):
    sc(ws, 8, 2+i, m, bold, light_gray, center)

sc(ws, 9, 1, "월 생산단가(천원)", bold)
for i, c in enumerate(prod_costs):
    sc(ws, 9, 2+i, c, fmt=num2, align=center, border=thin_border)
sc(ws, 9, 8, "c_t", bold_purple)
sc(ws, 9, 9, "← 계절적 변동(12.50→12.95). 목적계수 역할", bold_green)

sc(ws, 10, 1, "월 재고단가(천원)", bold)
for i in range(6):
    cl = get_column_letter(2+i)
    sc(ws, 10, 2+i, f"={cl}9*$B$6", fmt=num2, align=center, border=thin_border)
sc(ws, 10, 8, "h_t", bold_purple)
sc(ws, 10, 9, "← 수식: c_t × 5%. 재고비 목적계수", bold_green)

# ── 행 12~16: 생산계획 ──
sc(ws, 12, 1, "생산계획", header_font)
sc(ws, 12, 9, "【결정변수 영역】", section_font)

for i, m in enumerate(months):
    sc(ws, 13, 2+i, m, bold, light_gray, center)

sc(ws, 14, 1, "월생산량(천개)", bold)
for i, x in enumerate(initial_production):
    c = sc(ws, 14, 2+i, x, bold_blue, align=center)
    c.border = blue_border
    c.fill = light_blue
sc(ws, 14, 8, "x_t", bold_purple)
sc(ws, 14, 9, "← ★ 결정변수 (Solver 변경 셀). 관리자가 정하는 값", bold_blue)

for i in range(6):
    sc(ws, 15, 2+i, "<=", align=center)
sc(ws, 15, 9, "← 제약①: 생산량 ≤ 생산능력 (설비 한계)", bold_green)

sc(ws, 16, 1, "생산능력(천개)", bold)
for i in range(6):
    sc(ws, 16, 2+i, "=$B$3", align=center, border=thin_border)
sc(ws, 16, 9, "← RHS: $B$3=30 참조 (파라미터)", bold_green)

# ── 행 18: 수요 ──
sc(ws, 18, 1, "수요(천개)", bold)
for i, d in enumerate(demands):
    sc(ws, 18, 2+i, d, bold, light_gray, center, border=thin_border)
sc(ws, 18, 8, "d_t", bold_purple)
sc(ws, 18, 9, "← 상수(파라미터). 이미 정해진 수요 예측치", bold_green)

# ── 행 19: 수요 특징 주석 ──
sc(ws, 19, 9, "4월 수요(35) > 생산상한(30) → 미리 재고 비축 필요!", bold_red)

# ── 행 20~24: 재고 ──
for i in range(6):
    sc(ws, 20, 2+i, 0, align=center)
sc(ws, 20, 8, "하한", bold_purple)
sc(ws, 20, 9, "← 제약③: y_t ≥ 0 (백오더 불허. 재고 음수 = 수요 미충족)", bold_green)

for i in range(6):
    sc(ws, 21, 2+i, "<=", align=center)
sc(ws, 21, 9, "← 0 ≤ y_t ≤ 10 (재고는 이 범위 안에)", bold_green)

sc(ws, 22, 1, "월말재고(천개)", bold_red)
# B22: 1월 — 초기재고 사용
sc(ws, 22, 2, "=$B$5+B14-B18", align=center)
ws["B22"].border = red_border
ws["B22"].fill = light_red
# C22~G22: 체인
for i in range(1, 6):
    cl = get_column_letter(2+i)
    pcl = get_column_letter(1+i)
    c = sc(ws, 22, 2+i, f"={pcl}22+{cl}14-{cl}18", align=center)
    c.border = red_border
    c.fill = light_red
sc(ws, 22, 8, "y_t", bold_purple)
sc(ws, 22, 9, "← ★ Balance Equation: y_t = y_{t-1} + x_t - d_t", bold_red)

for i in range(6):
    sc(ws, 23, 2+i, "<=", align=center)
sc(ws, 23, 9, "← 제약②: 월말재고 ≤ 재고용량 (창고 한계)", bold_green)

for i in range(6):
    sc(ws, 24, 2+i, "=$B$4", align=center, border=thin_border)
sc(ws, 24, 8, "상한", bold_purple)
sc(ws, 24, 9, "← RHS: $B$4=10 참조 (파라미터)", bold_green)

# ── 행 25~31: 비용계산 ──
sc(ws, 25, 1, "비용계산", header_font)
sc(ws, 25, 9, "【목적함수 영역】", section_font)

for i, m in enumerate(months):
    sc(ws, 26, 2+i, m, bold, light_gray, center)

sc(ws, 27, 1, "생산비(백만원)", bold)
for i in range(6):
    cl = get_column_letter(2+i)
    sc(ws, 27, 2+i, f"={cl}9*{cl}14", fmt=num2, align=center, border=thin_border)
sc(ws, 27, 9, "← c_t × x_t (생산단가 × 생산량)", bold_green)

sc(ws, 28, 1, "재고유지비(백만원)", bold)
for i in range(6):
    cl = get_column_letter(2+i)
    sc(ws, 28, 2+i, f"={cl}10*{cl}22", fmt=num2, align=center, border=thin_border)
sc(ws, 28, 9, "← h_t × y_t (재고단가 × 월말재고)", bold_green)

sc(ws, 29, 1, "합계(백만원)", bold)
for i in range(6):
    cl = get_column_letter(2+i)
    sc(ws, 29, 2+i, f"={cl}27+{cl}28", fmt=num2, align=center, border=thin_border)
sc(ws, 29, 9, "← 월별 총비용 = 생산비 + 재고비", bold_green)

# 수식 주석 (슬라이드 빨간 글씨)
sc(ws, 30, 3, "B22=$B$5+B14-B18", bold_red)
sc(ws, 30, 9, "← 1월: 초기재고(5) + 생산 - 수요", bold_red)

sc(ws, 31, 1, "총 비용(백만원)", Font(bold=True, size=11))
tc = sc(ws, 31, 2, "=SUM(B29:G29)", Font(bold=True, size=11), fmt=num_comma)
tc.border = blue_border
sc(ws, 31, 3, "C22=B22+C14-C18", bold_red)
sc(ws, 31, 8, "Z", bold_purple)
sc(ws, 31, 9, "← ★ 목적 셀: min Z = Σ(c_t·x_t + h_t·y_t). Solver → Min", bold_blue)


# ════════════════════════════════════════════════════════════
# Sheet 2: 수식해설
# ════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("수식해설")
ws2.column_dimensions["A"].width = 6
ws2.column_dimensions["B"].width = 18
ws2.column_dimensions["C"].width = 30
ws2.column_dimensions["D"].width = 55
ws2.column_dimensions["E"].width = 50

r = 1
sc(ws2, r, 1, "수식 해설 — 각 셀이 무엇을 계산하고, 왜 필요한가", Font(bold=True, size=14, color="333399")); r += 2

# 헤더
for j, h in enumerate(["셀", "수식", "무엇을 계산하는가", "왜 필요한가 (인과)"], 1):
    sc(ws2, r, j, h, bold, light_gray, center)
r += 1

formulas = [
    ("B9:G9", "12.50, 12.55, …", "월별 생산단가 c_t (천원/천개)", "재료 가격의 계절적 변동. 뒤로 갈수록 비싸짐 → 앞 달에 미리 만들 인센티브"),
    ("B10", "=B9*$B$6", "월 재고단가 h_t = c_t × 5%", "재고 유지비의 목적계수. 생산단가에 비례하므로 수식으로 연결"),
    ("B14:G14", "(결정변수)", "월별 생산량 x_t (천개)", "★ Solver가 바꿀 셀. 관리자가 '이번 달에 몇 개 만들지' 정하는 레버"),
    ("B16", "=$B$3", "생산능력 30 (상수)", "제약①의 RHS. 설비·인력의 물리적 한계"),
    ("B18:G18", "10, 15, 30, 35, 25, 10", "월별 수요 d_t (상수)", "이미 예측된 수요. 변수가 아니라 파라미터"),
    ("B22", "=$B$5+B14-B18", "1월말 재고 y₁ = y₀ + x₁ - d₁", "Balance Eq. 시작점. 초기재고(5) 사용. 결과: 5+x₁-10"),
    ("C22", "=B22+C14-C18", "2월말 재고 y₂ = y₁ + x₂ - d₂", "전월말재고(B22) 참조 → 기간 간 체인(동적 연결)의 핵심"),
    ("D22~G22", "(같은 패턴)", "y₃~y₆ = y_{t-1} + x_t - d_t", "체인이 6월까지 이어짐. x₁ 변경 → y₁~y₆ 전부 갱신"),
    ("B27", "=B9*B14", "1월 생산비 = c₁ × x₁", "목적함수의 생산비 항. 단가(상수) × 생산량(변수)"),
    ("B28", "=B10*B22", "1월 재고비 = h₁ × y₁", "목적함수의 재고비 항. 재고단가(상수) × 월말재고(보조변수)"),
    ("B29", "=B27+B28", "1월 총비용 = 생산비 + 재고비", "월별 비용을 합산하기 위한 중간 셀"),
    ("B31", "=SUM(B29:G29)", "6개월 총비용 Z (목적 셀)", "★ Solver가 Min할 대상. Z = Σ(c_t·x_t + h_t·y_t)"),
]

for row_data in formulas:
    for j, val in enumerate(row_data, 1):
        f = bold_blue if j == 1 else None
        sc(ws2, r, j, val, f, align=wrap)
    r += 1

r += 1
sc(ws2, r, 1, "수식 연쇄 흐름도", Font(bold=True, size=12, color="333399")); r += 1
flow_lines = [
    "결정변수(x₁~x₆, 행14) ──┬── × 생산단가(행9) ──→ 생산비(행27) ──┐",
    "                         │                                       ├→ 월별비용(행29) → 총비용(B31, 목적)",
    "                         └── Balance Eq. ──→ 월말재고(행22) ──────┤",
    "                              ↑                                   └── × 재고단가(행10) → 재고비(행28)",
    "                         전월재고(체인)",
    "",
    "핵심: 모든 수식이 결정변수 6개(x₁~x₆)에서 출발해 파생된다.",
    "      Solver가 변수를 바꾸면 Balance Eq.을 통해 재고 → 재고비 → 총비용 순으로 자동 갱신.",
]
for line in flow_lines:
    sc(ws2, r, 1, line, Font(name="Consolas", size=10))
    ws2.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
    r += 1


# ════════════════════════════════════════════════════════════
# Sheet 3: 제약조건 해설
# ════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("제약조건")
ws3.column_dimensions["A"].width = 6
ws3.column_dimensions["B"].width = 20
ws3.column_dimensions["C"].width = 35
ws3.column_dimensions["D"].width = 15
ws3.column_dimensions["E"].width = 55

r = 1
sc(ws3, r, 1, "제약조건 해설 — 각 제약이 왜 도출되는가", Font(bold=True, size=14, color="333399")); r += 2

# 헤더
for j, h in enumerate(["#", "제약 이름", "수식 (대수)", "엑셀 셀", "인과 (왜 이 제약인가)"], 1):
    sc(ws3, r, j, h, bold, light_gray, center)
r += 1

constraints = [
    ("①", "생산 상한", "x_t ≤ 30  (t=1,…,6)", "B14:G14 ≤ B16:G16",
     "공장 설비·인력·작업시간의 물리적 한계. 아무리 수요가 많아도(4월 35) 한 달에 30 초과 생산 불가 → 미리 재고 비축 필요"),
    ("②", "재고 상한", "y_t ≤ 10  (t=1,…,6)", "B22:G22 ≤ B24:G24",
     "창고 공간·보관조건의 물리적 한계. 미리 많이 만들고 싶어도 10천개까지만 보관 가능"),
    ("③", "백오더 불허", "y_t ≥ 0  (t=1,…,6)", "B22:G22 ≥ B20:G20",
     "월말재고 음수 = '수요 못 채우고 다음달로 밀림(주문잔고)'. 이 문제에서는 허용 안 함"),
    ("④", "비음 조건", "x_t ≥ 0  (t=1,…,6)", "B14:G14 ≥ 0",
     "음수 생산은 물리적으로 불가능"),
    ("⑤", "Balance Eq.", "y_t = y_{t-1} + x_t - d_t", "행22 수식",
     "★ 등식이 아니라 수식 셀로 구현. Solver 제약이 아닌 엑셀 수식으로 처리됨"),
]

fills = [light_blue, light_blue, light_red, light_green, light_purple]

for i, (num, name, formula, cell_ref, reason) in enumerate(constraints):
    row_data = [num, name, formula, cell_ref, reason]
    for j, val in enumerate(row_data, 1):
        sc(ws3, r, j, val, align=wrap, fill=fills[i])
    r += 1

r += 2
sc(ws3, r, 1, "제약 부호 비교 — 이 문제 vs 이전 문제들", Font(bold=True, size=12, color="333399")); r += 1

for j, h in enumerate(["문제", "제약 부호", "인과"], 1):
    sc(ws3, r, j, h, bold, light_gray, center)
r += 1

comparisons = [
    ("Decora (절단)", "≥", "수요 이상 잘라야 (초과 = 폐기, 허용)"),
    ("Big M (운송)", "=", "공급·수요 정확히 일치 (고정 요건)"),
    ("Sellmore (할당)", "=", "1:1 배정 (겸임·공석 불가)"),
    ("W사 (혼합)", "≤ + ≥ 혼합", "자원 ≤ (남겨도 됨) + 품질 ≥ (기준 이상)"),
    ("축구공 (동적)", "≤ + ≥ + Balance", "생산·재고 상한(≤) + 비음(≥) + 기간 간 연쇄(=)"),
]

for prob, sign, reason in comparisons:
    sc(ws3, r, 1, prob, bold)
    sc(ws3, r, 2, sign, bold_blue, align=center)
    sc(ws3, r, 3, reason, align=wrap)
    r += 1

r += 2
sc(ws3, r, 1, "Solver 설정 요약", Font(bold=True, size=12, color="333399")); r += 1

for j, h in enumerate(["항목", "설정", "비고"], 1):
    sc(ws3, r, j, h, bold, light_gray, center)
r += 1

solver_settings = [
    ("목적 셀", "B31 = SUM(B29:G29)", "→ Min (6개월 총비용 최소화)"),
    ("변경 셀", "B14:G14 (6개)", "결정변수 x₁~x₆ (월별 생산량)"),
    ("제약①", "B14:G14 ≤ 30", "생산 상한"),
    ("제약②", "B22:G22 ≤ 10", "재고 상한 (=$B$4)"),
    ("제약③", "B22:G22 ≥ 0", "백오더 불허"),
    ("제약④", "B14:G14 ≥ 0", "비음 (또는 Solver 옵션 '비음 가정' 체크)"),
    ("해법", "Simplex LP", "선형 모형이므로 Simplex 사용"),
    ("", "", ""),
    ("주의", "Balance Eq.(행22)는 수식 셀", "Solver 제약에 넣지 않음! 수식이 자동 계산"),
]

for item, setting, note in solver_settings:
    f = bold_red if item == "주의" else bold
    sc(ws3, r, 1, item, f)
    sc(ws3, r, 2, setting, align=wrap)
    sc(ws3, r, 3, note, align=wrap)
    r += 1

r += 2
sc(ws3, r, 1, "핵심 트레이드오프 — 왜 '동적'인가", Font(bold=True, size=12, color="333399")); r += 1

tradeoff_lines = [
    "1. 4월 수요(35) > 생산상한(30) → 부족분 5를 이전 달 재고로 보충해야 함",
    "2. 생산단가가 뒤로 갈수록 비쌈 (12.50→12.95) → 앞 달에 미리 만들 인센티브",
    "3. 하지만 재고비(5%)가 들고, 재고상한(10)도 있음 → 무한정 미리 만들 수 없음",
    "4. 결론: '싼 달에 미리 만들어 재고로 쌓을지' vs '비싼 달에 만들지만 재고비 아낄지'",
    "   → 이 트레이드오프를 LP가 최적으로 풀어준다",
    "",
    "이것이 이전 단일기간 문제(Decora, Big M, Sellmore, W사)에는 없던 '시간적 배분' 구조이다.",
]

for line in tradeoff_lines:
    sc(ws3, r, 1, line, Font(size=10))
    ws3.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
    r += 1


# ════════════════════════════════════════════════════════════
# Sheet 4: 단위해설
# ════════════════════════════════════════════════════════════
ws4 = wb.create_sheet("단위해설")
ws4.column_dimensions["A"].width = 20
ws4.column_dimensions["B"].width = 20
ws4.column_dimensions["C"].width = 25
ws4.column_dimensions["D"].width = 45

r = 1
sc(ws4, r, 1, "단위 해설 — 왜 숫자가 이렇게 나오는가", Font(bold=True, size=14, color="333399")); r += 2

for j, h in enumerate(["항목", "원래 단위", "엑셀 단위", "변환 설명"], 1):
    sc(ws4, r, j, h, bold, light_gray, center)
r += 1

units = [
    ("생산량 x_t", "개", "천 개", "1 = 1,000개"),
    ("수요 d_t", "개", "천 개", "1 = 1,000개"),
    ("재고 y_t", "개", "천 개", "1 = 1,000개"),
    ("생산단가 c_t", "원/개", "천원/천개", "12.50 = 12,500원/1,000개"),
    ("재고단가 h_t", "원/개·월", "천원/천개·월", "0.625 = 625원/1,000개·월"),
    ("생산비 c_t·x_t", "원", "백만원", "12.50 × 5 = 62.50 (= 6,250만원)"),
    ("재고비 h_t·y_t", "원", "백만원", "0.625 × 5 = 3.125 (= 312.5만원)"),
    ("총비용 Z", "원", "백만원", "1,535.56 (= 약 15억 3,556만원)"),
]

for item, orig, excel, desc in units:
    sc(ws4, r, 1, item, bold)
    sc(ws4, r, 2, orig)
    sc(ws4, r, 3, excel)
    sc(ws4, r, 4, desc, align=wrap)
    r += 1

r += 2
sc(ws4, r, 1, "단위 확인 공식:", bold_red); r += 1
sc(ws4, r, 1, "생산비 = (천원/천개) × (천개) = 천원 × 천 = 백만원")
ws4.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4); r += 1
sc(ws4, r, 1, "재고비 = (천원/천개·월) × (천개) = 백만원/월")
ws4.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4); r += 1
sc(ws4, r, 1, "총비용 = 백만원 (6개월 합산)")
ws4.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)


# ════════════════════════════════════════════════════════════
# 저장
# ════════════════════════════════════════════════════════════
output_path = "/home/sieg/projects-wsl/hongikUniv.-26_1/decisionMaking/해답3-13_축구공_동적생산계획.xlsx"
wb.save(output_path)
print(f"✓ 저장 완료: {output_path}")
print(f"  시트: {wb.sheetnames}")

# ── 검증 ──
print("\n── 검증 (수동 계산) ──")
y0 = 5
inv_rates = [c * 0.05 for c in prod_costs]
print(f"{'월':>4} {'생산':>6} {'수요':>6} {'월말재고':>8} {'생산비':>8} {'재고비':>8} {'합계':>8}")
print("-" * 58)
total = 0
y_prev = y0
for t in range(6):
    y_t = y_prev + initial_production[t] - demands[t]
    pc = prod_costs[t] * initial_production[t]
    ic = inv_rates[t] * y_t
    mc = pc + ic
    total += mc
    print(f"{t+1:>4}월 {initial_production[t]:>6} {demands[t]:>6} {y_t:>8} {pc:>8.2f} {ic:>8.2f} {mc:>8.2f}")
    y_prev = y_t
print("-" * 58)
print(f"{'총비용':>30} {total:>8.2f}")
