# Excel 에이전트 모드용 프롬프트 (Toys R4U 브레이크이븐)

엑셀에서 **에이전트 모드 / AI**에 그대로 붙여 넣어 사용할 수 있는 프롬프트 예시입니다.  
연결: [LinkedIn - Agent mode in Excel GA](https://www.linkedin.com/posts/brijones_agent-mode-in-excel-is-now-generally-available-activity-7421959646682357761-VLhI)

---

## 1. 브레이크이븐 분석 시트 생성용 (기본)

```
You are an Excel agent helping me build a break-even analysis model
for a toy product.

1. Create a new worksheet named "Toys R4U Break-Even".
2. In range B4:C7, build a small input table titled "Data" with:
   - B4: "Unit Revenue",   C4: 35
   - B5: "Fixed Cost",     C5: 500000
   - B6: "Marginal Cost",  C6: 15
   - B7: "Sales Forecast", C7: 30000
3. In C9, add the label "Production Quantity" and set the default
   value in C9 to 25000.
4. In column E:F, starting at E4, create a "Results" block with
   these labels in E4:E9:
   - "Total Revenue"
   - "Total Fixed Cost"
   - "Total Variable Cost"
   - "Profit (Loss)"
   - (blank row)
   - "Break-Even Point"
5. Enter the following formulas in column F:
   - F4: =C4*MIN(C7,C9)
   - F5: =IF(C9>0,C5,0)
   - F6: =C6*C9
   - F7: =F4-(F5+F6)
   - F9: =C5/(C4-C6)
6. Format:
   - Use currency format with 0 decimals for all money cells
     (C4:C6, F4:F7).
   - Use comma-separated number format with 0 decimals for quantities
     (C7, C9, F9).
   - Shade the input cells C4:C7 and C9 light yellow.
   - Shade the result cells F4:F7 light gray and F9 light orange.
7. Finally, add a short note in A12 saying:
   "Break-even quantity is shown in F9. If the expected sales
    forecast (C7) is greater than the break-even quantity,
    producing the toy is recommended."
```

---

## 2. 결과 해석까지 시키고 싶을 때 추가 문장

기본 프롬프트 뒤에 아래를 이어서 붙이면 됩니다.

```
After building the sheet, calculate the profit when production
quantity C9 is 25000 and then 30000, and summarize in plain English
below the table whether production is financially worthwhile in each
case.
```

---

## 3. 이 과목(경영과학 Week 1)에 맞게만 살짝 바꾼 버전

- 시트 이름: `Toys R4U Break-Even` 유지 (연습문제 회사명).
- 데이터: Unit Revenue 35, Fixed Cost 500000, Marginal Cost 15, Sales Forecast 30000 → **20250309.md / Week 1 연습문제**와 동일.
- 손익분기점 F9 = 25,000 → **답 셀에 색 표시**하라는 요구는 프롬프트에 “Shade F9 light orange”로 이미 포함 가능 (위 기본 프롬프트에 있음).

필요하면 프롬프트 마지막에 한 줄만 추가:

```
Also add a brief note that the break-even point is 25,000 units, so
producing 25,000 yields zero profit and producing 30,000 is recommended.
```

---

## 4. 생성된 파일과의 관계

- **`decisionMaking/Toys_R4U_BreakEven.xlsx`**  
  위 프롬프트와 동일한 레이아웃·수식으로 만든 파일.  
  **다시 만들기 (WSL):**
  ```bash
  cd decisionMaking
  python3 -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  python build_toys_r4u_break_even.py
  ```
  → `Toys_R4U_BreakEven.xlsx` 생성됨.

- **에이전트 모드**에서는 빈 통합 문서에 위 프롬프트를 붙여 넣어 시트를 만들어도 되고,  
  이미 생성된 `Toys_R4U_BreakEven.xlsx`를 열어 둔 뒤 “결과 해석” 추가 프롬프트(2번, 3번)만 던져도 됩니다.
