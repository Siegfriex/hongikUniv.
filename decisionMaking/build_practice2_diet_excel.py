#!/usr/bin/env python3
"""Practice Assignment #2 — Ralph's Diet (Steak & Potatoes) LP. Part (a) & (b)."""

from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, PatternFill

def add_diet_sheet(ws, title, with_budget_constraint=False):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws.merge_cells("A1:G1")

    # 데이터: Cost per serving
    ws["A3"] = "Cost per serving ($)"
    ws["B3"] = "Steak"
    ws["C3"] = "Potatoes"
    ws["B4"] = 4
    ws["C4"] = 2
    data_fill = PatternFill(start_color="DAEEF3", end_color="DAEEF3", fill_type="solid")
    ws["B4"].fill = data_fill
    ws["C4"].fill = data_fill

    # 영양소 표: Grams per serving, Daily requirement
    ws["A6"] = "Ingredient"
    ws["B6"] = "Steak (g/serving)"
    ws["C6"] = "Potatoes (g/serving)"
    ws["D6"] = "LHS (used)"
    ws["E6"] = ""
    ws["F6"] = "Operator"
    ws["G6"] = "Requirement (g)"

    ws["A7"] = "Carbohydrates"
    ws["B7"] = 5
    ws["C7"] = 15
    ws["D7"] = "=B7*$B$12+C7*$C$12"
    ws["F7"] = ">="
    ws["G7"] = 50

    ws["A8"] = "Protein"
    ws["B8"] = 20
    ws["C8"] = 5
    ws["D8"] = "=B8*$B$12+C8*$C$12"
    ws["F8"] = ">="
    ws["G8"] = 40

    ws["A9"] = "Fat"
    ws["B9"] = 15
    ws["C9"] = 2
    ws["D9"] = "=B9*$B$12+C9*$C$12"
    ws["F9"] = "<="
    ws["G9"] = 60

    for r in [7, 8, 9]:
        for c in [2, 3, 7]:
            ws.cell(row=r, column=c).fill = data_fill

    # 결정변수 (Changing cells)
    ws["A11"] = "Steak"
    ws["B11"] = "Potatoes"
    ws["A12"] = "Servings"
    ws["B12"] = 1
    ws["C12"] = 1
    yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    ws["B12"].fill = yellow_fill
    ws["C12"].fill = yellow_fill
    side = Side(style="medium", color="000000")
    ws["B12"].border = Border(left=side, right=side, top=side, bottom=side)
    ws["C12"].border = Border(left=side, right=side, top=side, bottom=side)

    # 목적 셀 (Total Cost)
    ws["E11"] = "Total Cost ($)"
    ws["E12"] = "=B4*B12+C4*C12"
    orange_fill = PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid")
    ws["E12"].fill = orange_fill
    ws["E12"].border = Border(left=side, right=side, top=side, bottom=side)

    if with_budget_constraint:
        ws["A10"] = "Budget (part b)"
        ws["B10"] = 4
        ws["C10"] = 2
        ws["D10"] = "=B10*$B$12+C10*$C$12"
        ws["F10"] = "<="
        ws["G10"] = 8
        for c in [2, 3, 7]:
            ws.cell(row=10, column=c).fill = data_fill

    for c in "ABCDEFG":
        ws.column_dimensions[c].width = 14
    ws.column_dimensions["A"].width = 18

def main():
    wb = Workbook()
    ws_a = wb.active
    ws_a.title = "Part_a"
    add_diet_sheet(ws_a, "Practice #2 Part (a): Ralph's Diet — Min Cost (no budget cap)", with_budget_constraint=False)

    ws_b = wb.create_sheet("Part_b")
    add_diet_sheet(ws_b, "Practice #2 Part (b): Ralph's Diet — Min Cost with Budget <= $8", with_budget_constraint=True)

    ws_guide = wb.create_sheet("Solver_setup")
    ws_guide["A1"] = "Solver 설정 안내 (Practice #2)"
    ws_guide["A1"].font = Font(bold=True)
    ws_guide["A2"] = "Part (a): 목표 셀 E12 최소화 / 변경 셀 B12:C12"
    ws_guide["A3"] = "        제약: D7>=G7, D8>=G8, D9<=G9, B12>=0, C12>=0"
    ws_guide["A4"] = "Part (b): 위와 동일 + D10<=G10 (총 비용 <= $8)"
    ws_guide["A5"] = "결정변수: X1=Steak servings, X2=Potatoes servings"
    ws_guide["A6"] = "목적함수: Min Cost = 4*X1 + 2*X2"

    out_path = "Practice2_Ralph_Diet.xlsx"
    wb.save(out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
