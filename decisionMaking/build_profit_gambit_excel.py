#!/usr/bin/env python3
"""Profit & Gambit Co. 광고 최소비용 예제 — 엑셀 시트 생성 (수식 포함)."""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Profit_Gambit"

    # 제목
    ws["A1"] = "Profit & Gambit Co. — Advertising (Min Cost)"
    ws["A1"].font = Font(bold=True, size=12)
    ws.merge_cells("A1:G1")

    # 데이터: Unit cost ($M)
    ws["A3"] = "Unit cost ($M)"
    ws["B3"] = "TV"
    ws["C3"] = "PM"
    ws["B4"] = 1
    ws["C4"] = 2
    for c in "BC":
        ws[f"{c}4"].fill = PatternFill(start_color="DAEEF3", end_color="DAEEF3", fill_type="solid")

    # 제약 계수 및 최소 요구
    ws["A6"] = "Product"
    ws["B6"] = "TV (coeff)"
    ws["C6"] = "PM (coeff)"
    ws["D6"] = "LHS (sales inc)"
    ws["E6"] = ""
    ws["F6"] = ">="
    ws["G6"] = "Min required"

    ws["A7"] = "Stain remover"
    ws["B7"] = 0
    ws["C7"] = 1.5
    ws["D7"] = "=B7*$B$12+C7*$C$12"
    ws["F7"] = ">="
    ws["G7"] = 3

    ws["A8"] = "Liquid detergent"
    ws["B8"] = 3
    ws["C8"] = 4
    ws["D8"] = "=B8*$B$12+C8*$C$12"
    ws["F8"] = ">="
    ws["G8"] = 18

    ws["A9"] = "Powder detergent"
    ws["B9"] = -1
    ws["C9"] = 2
    ws["D9"] = "=B9*$B$12+C9*$C$12"
    ws["F9"] = ">="
    ws["G9"] = 4

    # 데이터 셀 배경 (연한 파랑)
    data_fill = PatternFill(start_color="DAEEF3", end_color="DAEEF3", fill_type="solid")
    for col in [2, 3]:
        ws.cell(row=4, column=col).fill = data_fill
    for row in [7, 8, 9]:
        for col in [2, 3, 7]:
            ws.cell(row=row, column=col).fill = data_fill

    # 결정변수 (Changing cells)
    ws["A11"] = "TV"
    ws["B11"] = "PM"
    ws["A12"] = "Units"
    ws["B12"] = 2  # 초기값 또는 최적해
    ws["C12"] = 3
    for c in ["B", "C"]:
        ws[f"{c}12"].fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        side = Side(style="medium", color="000000")
        ws[f"{c}12"].border = Border(left=side, right=side, top=side, bottom=side)

    # 목적 셀 (Cost, $M)
    ws["E11"] = "Cost ($M)"
    ws["E12"] = "=B4*B12+C4*C12"
    ws["E12"].fill = PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid")
    ws["E12"].border = Border(
        left=Side(style="medium"), right=Side(style="medium"),
        top=Side(style="medium"), bottom=Side(style="medium"),
    )

    # 열 너비
    ws.column_dimensions["A"].width = 18
    for c in "BCDEFG":
        ws.column_dimensions[c].width = 12

    # Solver 안내 시트
    ws2 = wb.create_sheet("Solver_setup")
    ws2["A1"] = "Solver 설정 안내 (Profit & Gambit)"
    ws2["A1"].font = Font(bold=True)
    ws2["A2"] = "목표: Cost($M) 최소화"
    ws2["A3"] = "목적 셀: E12 (Min)"
    ws2["A4"] = "변경 셀: B12:C12"
    ws2["A5"] = "제약: D7>=G7, D8>=G8, D9>=G9, B12>=0, C12>=0"
    ws2["A6"] = "최적해: TV*=2, PM*=3, Cost*=8 ($M)"

    out_path = "Profit_Gambit_Advertising.xlsx"
    wb.save(out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
