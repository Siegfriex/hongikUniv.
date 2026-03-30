"""
실습문제 #1: W사 포도젤리·포도주스 혼합 생산 계획
이미지 6(초기해)·7(최적해/Solver) 레이아웃 정확히 재현
"""

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

wb = openpyxl.Workbook()

# ── 스타일 (축구공 엑셀과 동일) ──
bold = Font(bold=True)
bold_red = Font(bold=True, color="FF0000")
bold_blue = Font(bold=True, color="0000FF")
bold_green = Font(bold=True, color="006600")
title_font = Font(bold=True, size=14, color="FF0000")
section_font = Font(bold=True, size=11, color="333399")
header_font = Font(bold=True, size=12)

yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
light_yellow = PatternFill(start_color="FFFFCC", end_color="FFFFCC", fill_type="solid")
light_gray = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
light_blue = PatternFill(start_color="DAEEF3", end_color="DAEEF3", fill_type="solid")
light_green = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
light_red = PatternFill(start_color="FCE4EC", end_color="FCE4EC", fill_type="solid")

thin = Border(left=Side("thin"), right=Side("thin"), top=Side("thin"), bottom=Side("thin"))
blue_bd = Border(left=Side("medium", color="0000FF"), right=Side("medium", color="0000FF"),
                 top=Side("medium", color="0000FF"), bottom=Side("medium", color="0000FF"))
red_bd = Border(left=Side("medium", color="FF0000"), right=Side("medium", color="FF0000"),
                top=Side("medium", color="FF0000"), bottom=Side("medium", color="FF0000"))
ctr = Alignment(horizontal="center", vertical="center")
wrap = Alignment(horizontal="left", vertical="top", wrap_text=True)
num2 = "0.00"
num1 = "0.0"
num_comma = "#,##0.0"


def sc(ws, r, c, val, font=None, fill=None, align=None, fmt=None, border=None):
    cell = ws.cell(row=r, column=c, value=val)
    if font: cell.font = font
    if fill: cell.fill = fill
    if align: cell.alignment = align
    if fmt: cell.number_format = fmt
    if border: cell.border = border
    return cell


# ════════════════════════════════════════════════════════════
# Sheet 1: 모형 (이미지 6 레이아웃 정확 재현)
# ════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "모형"

ws.column_dimensions["A"].width = 22
ws.column_dimensions["B"].width = 12
ws.column_dimensions["C"].width = 12
ws.column_dimensions["D"].width = 12
ws.column_dimensions["E"].width = 12
ws.column_dimensions["F"].width = 45

# ── 행 1: 제목 ──
sc(ws, 1, 1, "W사의 혼합생산(초기해)", font=title_font)

# ── 행 3~4: 입력요소 ──
sc(ws, 3, 1, "입력요소", font=header_font)
sc(ws, 4, 1, "보유 포도등급", font=bold)
sc(ws, 4, 2, 9, font=bold, fill=light_gray, align=ctr, border=thin)
sc(ws, 4, 3, 6, font=bold, fill=light_gray, align=ctr, border=thin)
sc(ws, 4, 4, 4, font=bold, fill=light_gray, align=ctr, border=thin)
sc(ws, 4, 6, "← 등급 벡터 (SUMPRODUCT 가중치)", font=bold_green)

# ── 행 6~8: 제품별 파라미터 ──
sc(ws, 6, 2, "포도젤리", font=bold, fill=light_gray, align=ctr)
sc(ws, 6, 3, "포도주스", font=bold, fill=light_gray, align=ctr)

sc(ws, 7, 1, "판매이익(천원)", font=bold)
sc(ws, 7, 2, 2.7, font=bold, fill=yellow_fill, align=ctr, border=thin)
sc(ws, 7, 3, 3.5, font=bold, fill=yellow_fill, align=ctr, border=thin)
sc(ws, 7, 6, "← 목적계수. 주스(3.5) > 젤리(2.7)", font=bold_green)

sc(ws, 8, 1, "요구등급", font=bold)
sc(ws, 8, 2, 5, font=bold, fill=yellow_fill, align=ctr, border=thin)
sc(ws, 8, 3, 7, font=bold, fill=yellow_fill, align=ctr, border=thin)
sc(ws, 8, 6, "← 품질 기준. 주스(7)가 젤리(5)보다 까다로움", font=bold_green)

# ── 행 10~13: 모형 (결정변수) ──
sc(ws, 10, 1, "모형", font=header_font)
sc(ws, 10, 5, "(1000Kgr단위)", font=bold)
sc(ws, 10, 6, "【결정변수 영역】", font=section_font)

sc(ws, 11, 2, "9등급", font=bold, fill=light_gray, align=ctr)
sc(ws, 11, 3, "6등급", font=bold, fill=light_gray, align=ctr)
sc(ws, 11, 4, "4등급", font=bold, fill=light_gray, align=ctr)
sc(ws, 11, 5, "생산량", font=bold, fill=light_gray, align=ctr)

# 행 12: 포도젤리 혼합량 — ★ 결정변수 (초기해: 20,30,15)
sc(ws, 12, 1, "포도젤리 혼합량", font=bold)
sc(ws, 12, 2, 20, font=bold_blue, fill=light_blue, align=ctr, border=blue_bd)
sc(ws, 12, 3, 30, font=bold_blue, fill=light_blue, align=ctr, border=blue_bd)
sc(ws, 12, 4, 15, font=bold_blue, fill=light_blue, align=ctr, border=blue_bd)
sc(ws, 12, 5, "=SUM(B12:D12)", align=ctr, border=thin)
sc(ws, 12, 6, "← ★결정변수 x₁₁,x₁₂,x₁₃ / E12=SUM(B12:D12)", font=bold_blue)

# 행 13: 포도주스 혼합량 — ★ 결정변수 (초기해: 20,30,15)
sc(ws, 13, 1, "포도주스 혼합량", font=bold)
sc(ws, 13, 2, 20, font=bold_blue, fill=light_blue, align=ctr, border=blue_bd)
sc(ws, 13, 3, 30, font=bold_blue, fill=light_blue, align=ctr, border=blue_bd)
sc(ws, 13, 4, 15, font=bold_blue, fill=light_blue, align=ctr, border=blue_bd)
sc(ws, 13, 5, "=SUM(B13:D13)", align=ctr, border=thin)
sc(ws, 13, 6, "← ★결정변수 x₂₁,x₂₂,x₂₃ / E13=SUM(B13:D13)", font=bold_blue)

# ── 행 14~16: 자원 제약 ──
sc(ws, 14, 1, "등급별 포도사용량", font=bold_red)
sc(ws, 14, 2, "=SUM(B12:B13)", align=ctr, border=red_bd, fill=light_red)
sc(ws, 14, 3, "=SUM(C12:C13)", align=ctr, border=red_bd, fill=light_red)
sc(ws, 14, 4, "=SUM(D12:D13)", align=ctr, border=red_bd, fill=light_red)
sc(ws, 14, 6, "← 열합: 젤리+주스에 투입된 등급별 합 (자원 LHS)", font=bold_red)

sc(ws, 15, 1, "(1000Kgr단위)", font=bold)
sc(ws, 15, 2, "<=", align=ctr)
sc(ws, 15, 3, "<=", align=ctr)
sc(ws, 15, 4, "<=", align=ctr)
sc(ws, 15, 6, "← 제약①②③: 사용량 ≤ 보유량", font=bold_green)

sc(ws, 16, 1, "등급별 포도보유량", font=bold)
sc(ws, 16, 2, "=$B$4", align=ctr, border=thin)  # 이미지에서는 40 직접 but 참조가 좋음
sc(ws, 16, 3, 60, align=ctr, border=thin)
sc(ws, 16, 4, 60, align=ctr, border=thin)
sc(ws, 16, 6, "← 자원 RHS: 40, 60, 60 (만kg)", font=bold_green)

# ── 보유량을 상수로 직접 쓰기 (이미지 원본 따름) ──
# B16은 이미지에서 40 직접값. 참조보다 직접값이 슬라이드와 일치
ws["B16"].value = 40

# ── 행 18~20: 품질 제약 ──
sc(ws, 18, 2, "투입 등급점수", font=bold, fill=light_gray, align=ctr)
sc(ws, 18, 4, "기준등급 점수", font=bold, fill=light_gray, align=ctr)
sc(ws, 18, 6, "【품질 제약 영역】", font=section_font)

sc(ws, 19, 1, "포도젤리 등급제한", font=bold)
sc(ws, 19, 2, "=SUMPRODUCT($B$4:$D$4,B12:D12)", align=ctr, border=thin, fmt=num1)
sc(ws, 19, 3, ">=", font=bold_green, align=ctr)
sc(ws, 19, 4, "=$B$8*E12", align=ctr, border=thin, fmt=num1)
sc(ws, 19, 6, "← 제약④: 9x₁₁+6x₁₂+4x₁₃ ≥ 5·(생산량)", font=bold_green)

sc(ws, 20, 1, "포도주스 등급제한", font=bold)
sc(ws, 20, 2, "=SUMPRODUCT($B$4:$D$4,B13:D13)", align=ctr, border=thin, fmt=num1)
sc(ws, 20, 3, ">=", font=bold_green, align=ctr)
sc(ws, 20, 4, "=$C$8*E13", align=ctr, border=thin, fmt=num1)
sc(ws, 20, 6, "← 제약⑤: 9x₂₁+6x₂₂+4x₂₃ ≥ 7·(생산량)", font=bold_green)

# ── 행 21~22: 목적 셀 ──
sc(ws, 21, 2, "(백만원)", font=bold)

sc(ws, 22, 1, "총 판매이익", font=Font(bold=True, size=12))
tc = sc(ws, 22, 2, "=$B$7*E12+$C$7*E13", font=Font(bold=True, size=12, color="0000FF"),
        fmt=num_comma, align=ctr)
tc.border = red_bd
sc(ws, 22, 6, "← ★목적 셀: 2.7×젤리생산 + 3.5×주스생산 → Solver Max", font=bold_blue)

# ── 행 24~: 수식 참조 (슬라이드 빨간 주석) ──
sc(ws, 24, 1, "수식 참조", font=section_font)

refs = [
    "E12 = SUM(B12:D12)           행합: 젤리 생산량",
    "B14 = SUM(B12:B13)           열합: 9등급 사용량",
    "B19 = SUMPRODUCT($B$4:$D$4, B12:D12)   투입 등급점수 (품질LHS)",
    "D19 = $B$8*E12 = 5*SUM(B12:D12)        기준등급 점수 (품질RHS)",
    "B22 = $B$7*E12+$C$7*E13                총 판매이익 (목적 셀)",
    "",
    "단위에 주의: 백만원 = 천원 × 1000kg",
]
for i, ref in enumerate(refs):
    sc(ws, 25 + i, 1, ref, font=bold_red)

# ── 행 33~: Solver 설정 ──
sc(ws, 33, 1, "Solver 설정", font=section_font)

solver = [
    ("목적 셀", "B22", "→ Max"),
    ("변경 셀", "B12:D13 (6개)", "x₁₁~x₂₃"),
    ("제약①", "B14 ≤ B16", "9등급 사용 ≤ 보유(40)"),
    ("제약②", "C14 ≤ C16", "6등급 사용 ≤ 보유(60)"),
    ("제약③", "D14 ≤ D16", "4등급 사용 ≤ 보유(60)"),
    ("제약④", "B19 ≥ D19", "젤리 품질: 등급점수 ≥ 기준점수"),
    ("제약⑤", "B20 ≥ D20", "주스 품질: 등급점수 ≥ 기준점수"),
    ("비음", "B12:D13 ≥ 0", "Solver 옵션 체크"),
    ("해법", "Simplex LP", ""),
]
for i, (item, setting, note) in enumerate(solver):
    sc(ws, 34 + i, 1, item, font=bold)
    sc(ws, 34 + i, 2, setting, align=ctr)
    sc(ws, 34 + i, 4, note, font=bold_green)


# ════════════════════════════════════════════════════════════
# Sheet 2: 수식해설
# ════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("수식해설")
ws2.column_dimensions["A"].width = 10
ws2.column_dimensions["B"].width = 38
ws2.column_dimensions["C"].width = 38
ws2.column_dimensions["D"].width = 55

r = 1
sc(ws2, r, 1, "수식 해설 — W사 혼합 생산 계획", font=Font(bold=True, size=14, color="333399")); r += 2

for j, h in enumerate(["셀", "수식", "무엇을 계산하는가", "왜 필요한가 (인과)"], 1):
    sc(ws2, r, j, h, font=bold, fill=light_gray, align=ctr)
r += 1

formulas = [
    ("B4:D4", "9, 6, 4", "포도 등급 벡터", "SUMPRODUCT의 가중치. 품질LHS 계산에 사용"),
    ("B7,C7", "2.7, 3.5", "이익단가 (천원/kg)", "목적계수. 주스가 비싸지만 품질 기준도 높다"),
    ("B8,C8", "5, 7", "요구등급", "품질 기준. 주스(7)가 젤리(5)보다 까다로움"),
    ("B12:D12", "★ 결정변수", "젤리 등급별 투입 x₁₁,x₁₂,x₁₃", "Solver 변경 셀. '어떤 등급을 얼마나 넣을지'"),
    ("B13:D13", "★ 결정변수", "주스 등급별 투입 x₂₁,x₂₂,x₂₃", "Solver 변경 셀"),
    ("E12", "=SUM(B12:D12)", "젤리 생산량 (행합)", "투입 총량=생산량. 목적·품질RHS에 사용"),
    ("E13", "=SUM(B13:D13)", "주스 생산량 (행합)", "위와 동일"),
    ("B14", "=SUM(B12:B13)", "9등급 사용량 (열합)", "자원 제약 LHS"),
    ("C14", "=SUM(C12:C13)", "6등급 사용량 (열합)", "자원 제약 LHS"),
    ("D14", "=SUM(D12:D13)", "4등급 사용량 (열합)", "자원 제약 LHS"),
    ("B19", "=SUMPRODUCT($B$4:$D$4,B12:D12)", "젤리 투입 등급점수 (9x₁₁+6x₁₂+4x₁₃)", "품질 LHS. 분수식의 분자"),
    ("D19", "=$B$8*E12 즉 5*SUM(B12:D12)", "젤리 기준등급 점수 (5×생산량)", "품질 RHS. 분모 곱해 선형화"),
    ("B20", "=SUMPRODUCT($B$4:$D$4,B13:D13)", "주스 투입 등급점수", "품질 LHS (주스)"),
    ("D20", "=$C$8*E13 즉 7*SUM(B13:D13)", "주스 기준등급 점수 (7×생산량)", "품질 RHS (주스)"),
    ("B22", "=$B$7*E12+$C$7*E13", "총 판매이익 (백만원)", "★ 목적 셀 → Max"),
]

for rd in formulas:
    for j, val in enumerate(rd, 1):
        sc(ws2, r, j, val, font=bold_blue if j == 1 else None, align=wrap)
    r += 1

r += 2
sc(ws2, r, 1, "수식 연쇄 흐름도", font=Font(bold=True, size=12, color="333399")); r += 1

flow = [
    "결정변수(B12:D13) ─┬─ 행합(E12:E13) ─→ ×이익단가 → 총이익 B22 (목적)",
    "                    ├─ 열합(B14:D14) ─→ ≤ 보유량(B16:D16)  [자원제약]",
    "                    ├─ SUMPRODUCT(B19,B20) ─→ ≥ 기준×생산(D19,D20)  [품질제약]",
    "                    └─ ≥ 0  [비음]",
]
for line in flow:
    sc(ws2, r, 1, line, font=Font(name="Consolas", size=10))
    ws2.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    r += 1

r += 2
sc(ws2, r, 1, "품질 제약 선형화 (핵심)", font=Font(bold=True, size=12, color="333399")); r += 1

lin = [
    "【젤리: 평균등급 ≥ 5】",
    "  원래: (9x₁₁+6x₁₂+4x₁₃)/(x₁₁+x₁₂+x₁₃) ≥ 5  ← 비선형",
    "  분모 곱: 9x₁₁+6x₁₂+4x₁₃ ≥ 5(x₁₁+x₁₂+x₁₃)  ← 선형!",
    "  엑셀: B19 ≥ D19  (SUMPRODUCT ≥ 기준×SUM)",
    "  이항하면: 4x₁₁ + x₁₂ - x₁₃ ≥ 0",
    "",
    "【주스: 평균등급 ≥ 7】",
    "  이항하면: 2x₂₁ - x₂₂ - 3x₂₃ ≥ 0",
    "  9등급(+2)만 양의 계수 → 주스에는 9등급 필수",
    "",
    "초기해(20,30,15): 젤리 420≥325 OK, 주스 420≥455 NG!",
    "→ 초기해는 비실행가능. Solver가 실행가능+최적 해를 찾아줌",
]
for line in lin:
    sc(ws2, r, 1, line, font=Font(name="Consolas", size=10))
    ws2.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    r += 1


# ════════════════════════════════════════════════════════════
# Sheet 3: 제약조건
# ════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("제약조건")
ws3.column_dimensions["A"].width = 6
ws3.column_dimensions["B"].width = 18
ws3.column_dimensions["C"].width = 35
ws3.column_dimensions["D"].width = 14
ws3.column_dimensions["E"].width = 55

r = 1
sc(ws3, r, 1, "제약조건 해설", font=Font(bold=True, size=14, color="333399")); r += 2

for j, h in enumerate(["#", "제약 이름", "수식 (대수)", "엑셀 셀", "인과"], 1):
    sc(ws3, r, j, h, font=bold, fill=light_gray, align=ctr)
r += 1

constraints = [
    ("①", "9등급 상한", "x₁₁+x₂₁ ≤ 40", "B14 ≤ B16", "9등급 희소 → 바인딩 가능성 높음", light_blue),
    ("②", "6등급 상한", "x₁₂+x₂₂ ≤ 60", "C14 ≤ C16", "보유량 초과 불가", light_blue),
    ("③", "4등급 상한", "x₁₃+x₂₃ ≤ 60", "D14 ≤ D16", "품질 끌어내림 → 전량 미사용 가능", light_blue),
    ("④", "젤리 품질", "9x₁₁+6x₁₂+4x₁₃ ≥ 5·Σ", "B19 ≥ D19", "가중평균 ≥ 5. 비율→선형 변환", light_green),
    ("⑤", "주스 품질", "9x₂₁+6x₂₂+4x₂₃ ≥ 7·Σ", "B20 ≥ D20", "가중평균 ≥ 7. 9등급 필수", light_green),
    ("⑥", "비음", "x₁₁,...,x₂₃ ≥ 0", "B12:D13 ≥ 0", "음수 투입 불가", light_red),
]

for num, name, formula, cell_ref, reason, fl in constraints:
    for j, val in enumerate([num, name, formula, cell_ref, reason], 1):
        sc(ws3, r, j, val, align=wrap, fill=fl)
    r += 1

r += 2
sc(ws3, r, 1, "Solver 설정", font=Font(bold=True, size=12, color="333399")); r += 1
for j, h in enumerate(["항목", "설정", "비고"], 1):
    sc(ws3, r, j, h, font=bold, fill=light_gray, align=ctr)
r += 1

for item, setting, note in [
    ("목적 셀", "B22", "→ Max (총이익 최대화)"),
    ("변경 셀", "B12:D13 (6개)", "x₁₁~x₂₃"),
    ("제약①~③", "B14:D14 ≤ B16:D16", "자원: 사용량 ≤ 보유량"),
    ("제약④", "B19 ≥ D19", "젤리 품질"),
    ("제약⑤", "B20 ≥ D20", "주스 품질"),
    ("비음", "B12:D13 ≥ 0", "Solver 옵션 체크"),
    ("해법", "Simplex LP", "선형 모형"),
]:
    sc(ws3, r, 1, item, font=bold)
    sc(ws3, r, 2, setting, align=wrap)
    sc(ws3, r, 3, note, align=wrap)
    r += 1

r += 2
sc(ws3, r, 1, "최적해에서 확인할 것", font=Font(bold=True, size=12, color="FF0000")); r += 1
for line in [
    "1. 9등급(40만kg) 바인딩? → 희소 자원이므로 가능성 높음",
    "2. 주스 품질 제약 바인딩? → 기준7로 까다로워 LHS=RHS 가능",
    "3. 4등급 포도 남는가? → 품질 끌어내림 → 전량 미사용 가능",
    "4. 초기해(20,30,15)는 비실행가능(주스 420<455) → Solver가 수정",
]:
    sc(ws3, r, 1, line, font=Font(size=10))
    ws3.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
    r += 1


# ════════════════════════════════════════════════════════════
# 저장 + 검증
# ════════════════════════════════════════════════════════════
out = "/home/sieg/projects-wsl/hongikUniv.-26_1/decisionMaking/실습1_W사_포도젤리주스_혼합생산.xlsx"
wb.save(out)
print(f"✓ 저장 완료: {out}")
print(f"  시트: {wb.sheetnames}")

# 검증 (초기해)
print("\n── 초기해 검증 (이미지 6 대조) ──")
x = [[20, 30, 15], [20, 30, 15]]
grades = [9, 6, 4]
supply = [40, 60, 60]

for p, name in enumerate(["젤리", "주스"]):
    prod = sum(x[p])
    grade_sum = sum(g * v for g, v in zip(grades, x[p]))
    std = [5, 7][p]
    rhs = std * prod
    print(f"  {name}: 생산={prod}, 등급점수={grade_sum}, 기준점수={rhs}, {'OK' if grade_sum >= rhs else 'NG!'}")

for g in range(3):
    used = x[0][g] + x[1][g]
    print(f"  {grades[g]}등급: 사용={used}, 보유={supply[g]}, {'OK' if used <= supply[g] else 'NG!'}")

profit = 2.7 * sum(x[0]) + 3.5 * sum(x[1])
print(f"  총이익: {profit:.1f} (이미지: 403.0)")
