#!/usr/bin/env python3
"""
Toys R4U 브레이크이븐 분석 — 변수·파라미터·수식·안내 문구 설명

[1] 문제
    크리스마스용 신규 장난감을 도입할지 결정. 생산·판매비 500,000 + 15×Q,
    판매 시 단위당 35 수입. "몇 개까지는 손해, 그 이상은 이익"인 손익분기점을 구함.

[2] 파라미터 (문제에서 주어진 고정값, 시트의 Data 블록)
    C4 Unit Revenue    = 35   → 장난감 1개 팔 때 벌어들이는 돈 (매출 단가)
    C5 Fixed Cost      = 500000 → 도입 시 한 번만 드는 비용 (설비·광고 등)
    C6 Marginal Cost  = 15   → 1개 더 만들 때 추가로 드는 비용 (변동비)
    C7 Sales Forecast = 30000 → 예상 판매량 (몇 개나 팔릴지 예측)

[3] 결정변수 (우리가 정하는 값)
    C9 Production Quantity = 25000 (기본값) → 실제로 몇 개 생산할지

[4] 결과 수식이 나오는 이유
    • 총매출 F4 = 단가×판매량. 판매량 = min(예상판매, 생산량) 이므로
      F4 = C4 * MIN(C7, C9)
    • 총고정비 F5 = 생산하기로 하면(C9>0) 고정비 전부, 아니면 0
      F5 = IF(C9>0, C5, 0)
    • 총변동비 F6 = 개당 변동비 × 생산량
      F6 = C6 * C9
    • 이익 F7 = 총매출 - (고정비+변동비)
      F7 = F4 - (F5 + F6)
    • 손익분기점 F9 = 이익이 0이 되는 생산량 Q.
      이익 = (단가-변동비)×Q - 고정비 = (C4-C6)*Q - C5 = 0
      → Q = C5 / (C4 - C6)  즉  F9 = C5/(C4-C6)
      여기서는 500000/(35-15) = 25,000개.

[5] A12 안내 문구가 말하는 것
    "손익분기량은 F9에 있다. 예상 판매량(C7)이 손익분기량보다 크면,
     장난감을 생산하는 것을 권한다."
    이유: 예상 판매가 손익분기보다 많으면, 그만큼 생산해도 이익이 나므로
    (F7 > 0) 도입이 유리함. 반대로 예상 판매가 손익분기보다 적으면
    생산해도 손해가 나므로 도입 비권장.
"""
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("openpyxl 필요: pip install openpyxl")
    raise

OUTPUT = Path(__file__).resolve().parent / "C293085_RYUJIWAN_WEEK1_markDownComapny.xlsx"

def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "decisionMakingWeek1"

    # Data block B4:C7
    ws["B3"] = "Data"
    ws["B3"].font = Font(bold=True)
    data = [
        ("Unit Revenue", 35),
        ("Fixed Cost", 500000),
        ("Marginal Cost", 15),
        ("Sales Forecast", 30000),
    ]
    for i, (label, value) in enumerate(data, start=4):
        ws.cell(row=i, column=2, value=label)
        ws.cell(row=i, column=3, value=value)

    # Production Quantity C9
    ws["B9"] = "Production Quantity"
    ws["C9"] = 25000

    # Results block E4:F9
    ws["E3"] = "Results"
    ws["E3"].font = Font(bold=True)
    result_labels = [
        "Total Revenue",
        "Total Fixed Cost",
        "Total Variable Cost",
        "Profit (Loss)",
        "",
        "Break-Even Point",
    ]
    for i, label in enumerate(result_labels, start=4):
        ws.cell(row=i, column=5, value=label if label else None)

    # Formulas in F4:F9 (이유는 파일 상단 docstring 참고)
    ws["F4"] = "=C4*MIN(C7,C9)"   # 총매출 = 단가 × min(예상판매, 생산량)
    ws["F5"] = "=IF(C9>0,C5,0)"   # 생산하면 고정비 전부, 아니면 0
    ws["F6"] = "=C6*C9"           # 총변동비 = 개당변동비 × 생산량
    ws["F7"] = "=F4-(F5+F6)"      # 이익 = 총매출 - 총비용
    ws["F9"] = "=C5/(C4-C6)"      # 손익분기점 = 고정비/(단가-변동비)

    # Format: currency for money cells
    for row in [4, 5, 6]:
        ws.cell(row=row, column=3).number_format = '"$"#,##0'
        ws.cell(row=row, column=6).number_format = '"$"#,##0'
    ws["F7"].number_format = '"$"#,##0'

    # Comma format for quantities
    for cell in [ws["C7"], ws["C9"], ws["F9"]]:
        cell.number_format = "#,##0"

    # Shade input cells C4:C7, C9 light yellow
    yellow_fill = PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")
    for row in range(4, 8):
        ws.cell(row=row, column=3).fill = yellow_fill
    ws["C9"].fill = yellow_fill

    # Shade result cells F4:F7 light gray, F9 light orange
    gray_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    orange_fill = PatternFill(start_color="FFCC99", end_color="FFCC99", fill_type="solid")
    for row in range(4, 8):
        ws.cell(row=row, column=6).fill = gray_fill
    ws["F9"].fill = orange_fill

    # Note in A12: 손익분기량(F9)보다 예상판매(C7)가 크면 생산 권장 (이유는 docstring [5])
    ws["A12"] = (
        "Break-even quantity is shown in F9. If the expected sales "
        "forecast (C7) is greater than the break-even quantity, producing the toy is recommended. "
        "손익분기량 25,000개 = 25,000개까지는 이익 0, 그 위로는 개당 (35−15)=20달러씩 이익. "
        "예상 판매가 30,000개면 25,000개 넘는 5,000개에서 이익이 나므로 생산이 유리. "
        "최종 근거: 예상 판매가 손익분기보다 많으면 (F7>0) 도입 유리, 적으면 손해이므로 도입 비권장."
    )
    ws["A12"].alignment = Alignment(wrap_text=True)
    ws.column_dimensions["A"].width = 70

    wb.save(OUTPUT)
    print(f"Created: {OUTPUT}")

if __name__ == "__main__":
    main()
