# DM_PDF02 — Ch.5 민감도 분석 full PDF transcript

**source_id:** `DM_PDF02`
**normalized_pdf:** `decisionMaking/pdf_sources/DM_PDF02_ch05_sensitivity_analysis.pdf`
**original_filename:** `Ch.5 Sensitivity analysis (Ch. 5)_26 (2).pdf`
**page_count:** 43
**empty_pages:** 0
**low_text_pages:** 11
**extraction_risk_pages:** 11

## Anchor Policy

- Anchor format: `DM_PDF02:pNNN:LNNN`
- Page and line anchors are generated from extracted PDF text.
- `[EXTRACTION_GAP]` marks pages that need OCR/manual verification.

## Page 001

[DM_PDF02:p001:L001] Operation Research
[DM_PDF02:p001:L002] Ch.5. Sensitivity Analysis
[DM_PDF02:p001:L003] for Linear Programming
[DM_PDF02:p001:L004] (민감도 분석)
[DM_PDF02:p001:L005] Hyesung Seok
[DM_PDF02:p001:L006] hseok@hongik.ac.kr
[DM_PDF02:p001:L007] Department of Industrial & Data Engineering
[DM_PDF02:p001:L008] Hongik University

## Page 002

[DM_PDF02:p002:L001] 2
[DM_PDF02:p002:L002] 유모차-보행기 생산계획 문제
[DM_PDF02:p002:L003] – 제품배합문제(product-mix problem): 제한된 원료로 최
[DM_PDF02:p002:L004] 대 이익을 내는 제품별 생산 수준을 결정하는 문제
[DM_PDF02:p002:L005] (Resource Allocation Problem 중 하나)
[DM_PDF02:p002:L006] – 기계1, 기계2, 기계3의 일주간 이용가능시간 => 표 2.1

## Page 003

[DM_PDF02:p003:L001] 3
[DM_PDF02:p003:L002] – 수요에 효율적으로 대처하기 위해 주 단위로 생산계획
[DM_PDF02:p003:L003] – 유모차와 보행기 생산 고려
[DM_PDF02:p003:L004] – 제품 단위 생산에 요구되는 각 기계 작업시간
[DM_PDF02:p003:L005] => 표 2.2

## Page 004

[DM_PDF02:p004:L001] 4
[DM_PDF02:p004:L002] – 제품 단위당 판매이익 (판매가격-생산원가):
[DM_PDF02:p004:L003] 유모차 30만원, 보행기 20만원
[DM_PDF02:p004:L004] – 단, 보행기는 40대 이하로만 생산한다고 가정한다.
[DM_PDF02:p004:L005] – 총 판매이익을 최대화하는 유모차와 보행기의 생산계획을
[DM_PDF02:p004:L006] 구하시오.

## Page 005

[DM_PDF02:p005:L001] 5
[DM_PDF02:p005:L002] 수리 모형화
[DM_PDF02:p005:L003] 유모차 생산량: x1
[DM_PDF02:p005:L004] 보행기 생산량: x2
[DM_PDF02:p005:L005] Maximize 30 x1 + 20 x2 (총판매이익)
[DM_PDF02:p005:L006] Subject to
[DM_PDF02:p005:L007] 8 x1 + 3 x2 <= 240 (기계 1 작업시간 제약)
[DM_PDF02:p005:L008] 4 x1 + 4 x2 <= 200 (기계 2 작업시간 제약)
[DM_PDF02:p005:L009] 4 x1 + 0 x2 <= 100 (기계 3 작업시간 제약)
[DM_PDF02:p005:L010] x2 <= 40 (보행기 수요 제약)
[DM_PDF02:p005:L011] x1 >= 0, x2 >= 0 (비음 조건)

## Page 006

[DM_PDF02:p006:L001] 6
[DM_PDF02:p006:L002] 2.3 그래프를 이용한 선형계획 이해
[DM_PDF02:p006:L003] Max 30 x1 + 20 x2
[DM_PDF02:p006:L004] s/t 8 x1 + 3 x2 <= 240
[DM_PDF02:p006:L005] 4 x1 + 4 x2 <= 200
[DM_PDF02:p006:L006] 4 x1 + 0 x2 <= 100
[DM_PDF02:p006:L007] x2 <= 40
[DM_PDF02:p006:L008] x1 >= 0, x2 >= 0
[DM_PDF02:p006:L009]  가능영역(feasible region) 표시
[DM_PDF02:p006:L010] x2
[DM_PDF02:p006:L011] x1
[DM_PDF02:p006:L012] 4x1+0x2=100
[DM_PDF02:p006:L013] 4x1+4x2=200
[DM_PDF02:p006:L014] 8x1+3x2=240

## Page 007

[DM_PDF02:p007:L001] 두 변수의 그래프
[DM_PDF02:p007:L002] 표현
[DM_PDF02:p007:L003] • X1축: 유모차 대수
[DM_PDF02:p007:L004] • X2축: 보행기 대수
[DM_PDF02:p007:L005] • 점 (A, B) 은
[DM_PDF02:p007:L006] (A는 유모차 대수,
[DM_PDF02:p007:L007] B는 보행기 대수) 를
[DM_PDF02:p007:L008] 나타냄.
[DM_PDF02:p007:L009] 7
[DM_PDF02:p007:L010] 보행기 대수
[DM_PDF02:p007:L011] 유모차 대수
[DM_PDF02:p007:L012] (유모차 대수, 보행기대수)

## Page 008

[DM_PDF02:p008:L001] 제약조건의
[DM_PDF02:p008:L002] 표현
[DM_PDF02:p008:L003] 8x1+3x2 = 240 등
[DM_PDF02:p008:L004] 식으로 만든 후, 만
[DM_PDF02:p008:L005] 족하는 두 점
[DM_PDF02:p008:L006] 점 (0, 80)
[DM_PDF02:p008:L007] 점 (30,0)
[DM_PDF02:p008:L008] 을 찾아서, 두 점을
[DM_PDF02:p008:L009] 연결함.
[DM_PDF02:p008:L010] 8
[DM_PDF02:p008:L011] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 009

[DM_PDF02:p009:L001] 제약조건
[DM_PDF02:p009:L002] 충족영역
[DM_PDF02:p009:L003] • 8x1 + 3x2 <= 240
[DM_PDF02:p009:L004] • x1 >=0, x2>=0
[DM_PDF02:p009:L005] 조건을 충족하는지?
[DM_PDF02:p009:L006] • 점 (0, 0)은 충족함
[DM_PDF02:p009:L007] • 점 (0,0) 주변은 제
[DM_PDF02:p009:L008] 한조건을 충족함.
[DM_PDF02:p009:L009] 9

## Page 010

[DM_PDF02:p010:L001] 실행가능영역 feasible region
[DM_PDF02:p010:L002] • 모든 제한조건
[DM_PDF02:p010:L003] 을 충족함.
[DM_PDF02:p010:L004] 10
[DM_PDF02:p010:L005] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 011

[DM_PDF02:p011:L001] 실행가능해와 실행 불능해
[DM_PDF02:p011:L002] • A, B, C는 실행가능해
[DM_PDF02:p011:L003] • D는 실행 불능해
[DM_PDF02:p011:L004] 11
[DM_PDF02:p011:L005] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 012

[DM_PDF02:p012:L001] 12
[DM_PDF02:p012:L002] 그래프 이해(계속)
[DM_PDF02:p012:L003]  가능해 종류:
[DM_PDF02:p012:L004] • 내부점(interior point): A
[DM_PDF02:p012:L005] • 경계점(boundary point): B
[DM_PDF02:p012:L006] • 꼭지점(extreme point): C
[DM_PDF02:p012:L007] Simplex method : 꼭지점을 따라 최적해로 감 (Dantzig)
[DM_PDF02:p012:L008] Interior-point algorithm : 내부점으로 최적해로 감 (Kamarkar)

## Page 013

[DM_PDF02:p013:L001] 목적함수: 등위이익선 (iso-profit line)
[DM_PDF02:p013:L002] 13
[DM_PDF02:p013:L003] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 014

[DM_PDF02:p014:L001] 14
[DM_PDF02:p014:L002] 등위 이익선과 최적해 결정
[DM_PDF02:p014:L003] • 등위 이익선을 평행이동
[DM_PDF02:p014:L004] (shift) 시키면서 최대
[DM_PDF02:p014:L005] 이익을 주는 꼭지점 결정
[DM_PDF02:p014:L006] 최적해 꼭지점:
[DM_PDF02:p014:L007] 8 x1 + 3 x2 = 240
[DM_PDF02:p014:L008] 4 x1 + 4 x2 = 200
[DM_PDF02:p014:L009]  x1*=18, x2*=32

## Page 015

[DM_PDF02:p015:L001] 15
[DM_PDF02:p015:L002] 복수 최적해 (multiple optimal solutions)
[DM_PDF02:p015:L003] • 만일 목적함수의 x1 계수가 30  20 으로 바뀌어
[DM_PDF02:p015:L004] 20 x1+ 20 x2 이면
[DM_PDF02:p015:L005] • 꼭지점 (10,40)과
[DM_PDF02:p015:L006] 꼭지점 (18,32) 사이의
[DM_PDF02:p015:L007] 모든 점이 최적해가 됨
[DM_PDF02:p015:L008] • 꼭지점 (10,40):
[DM_PDF02:p015:L009] x2 = 40
[DM_PDF02:p015:L010] 4x1 + 4x2 = 200
[DM_PDF02:p015:L011] • 꼭지점 (18,32):
[DM_PDF02:p015:L012] 8 x1 + 3 x2 = 240
[DM_PDF02:p015:L013] 4 x1 + 4 x2 = 200

## Page 016

[DM_PDF02:p016:L001] 꼭지점을 따라가는
[DM_PDF02:p016:L002] ‘단체법’(Simplex Method)
[DM_PDF02:p016:L003] 16
[DM_PDF02:p016:L004] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 017

[DM_PDF02:p017:L001] 17
[DM_PDF02:p017:L002] 선형계획 문제의 성질
[DM_PDF02:p017:L003] (최적 목적함수 값이 유한값일 때)
[DM_PDF02:p017:L004] 1. 최적해가 되는 꼭지점이 반드시 존재한다.
[DM_PDF02:p017:L005] 2. 최적해가 아닌 꼭지점에 대해서는 목적함수 값을
[DM_PDF02:p017:L006] 개선할 수 있는 인접한 꼭지점이 반드시 존재한
[DM_PDF02:p017:L007] 다.
[DM_PDF02:p017:L008] 3. 목적함수 값을 더 이상 개선시킬 수 있는 인접한
[DM_PDF02:p017:L009] 꼭지점이 없으면 현재의 꼭지점이 최적해이다.

## Page 018

[DM_PDF02:p018:L001] 18
[DM_PDF02:p018:L002] Simplex Method
[DM_PDF02:p018:L003] (유한 최적 값을 갖는 경우)
[DM_PDF02:p018:L004] Simplex Method는 대수적 절차로서
[DM_PDF02:p018:L005] 1. 하나의 꼭지점에서 시작한다.
[DM_PDF02:p018:L006] 2. 인접 꼭지점을 따라 개선시켜 나간다.
[DM_PDF02:p018:L007] 3. 최적 꼭지점에 이르면(개선이 안되면) 멈춘다.

## Page 019

[DM_PDF02:p019:L001] 19
[DM_PDF02:p019:L002] Simplex method (기하적 설명)
[DM_PDF02:p019:L003] • Simplex method: 꼭지점 이동
[DM_PDF02:p019:L004] 변경셀 목표셀
[DM_PDF02:p019:L005] ① (0,0) 0
[DM_PDF02:p019:L006] ② (25,0) 750
[DM_PDF02:p019:L007] ③ (25,10) 950
[DM_PDF02:p019:L008] ④ (18,32) 1180 **
[DM_PDF02:p019:L009] ⑤ (10,40) 1100
[DM_PDF02:p019:L010] 질문: (0,0)에서 x2=0 경계를 따라 (25,0)으로 가느냐?
[DM_PDF02:p019:L011] 또는 x1=0 경계를 따라 (0,40)으로 가느냐?
[DM_PDF02:p019:L012] x2
[DM_PDF02:p019:L013] x1
[DM_PDF02:p019:L014] 4x1+0x2=100
[DM_PDF02:p019:L015] 4x1+4x2=200
[DM_PDF02:p019:L016] 8x1+3x2=240
[DM_PDF02:p019:L017] 30x1+20x2=500 30x1+20x2=750
[DM_PDF02:p019:L018] X2<=40

## Page 020

[DM_PDF02:p020:L001] 실행가능영역이 없는 경우
[DM_PDF02:p020:L002] (Infeasible solution)
[DM_PDF02:p020:L003] 20
[DM_PDF02:p020:L004] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 021

[DM_PDF02:p021:L001] 무한가능영역,
[DM_PDF02:p021:L002] 무한해(unbounded solution)
[DM_PDF02:p021:L003] 21
[DM_PDF02:p021:L004] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 022

[DM_PDF02:p022:L001] 중복제약식(redundant constraints)
[DM_PDF02:p022:L002] • 보행기 수요가
[DM_PDF02:p022:L003] 60대 이하라
[DM_PDF02:p022:L004] 면.
[DM_PDF02:p022:L005] • 이는 실행가능
[DM_PDF02:p022:L006] 영역에 영향이
[DM_PDF02:p022:L007] 없는 중복제약
[DM_PDF02:p022:L008] 식
[DM_PDF02:p022:L009] 22
[DM_PDF02:p022:L010] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 023

[DM_PDF02:p023:L001] 2.4. 민감도 분석 sensitivity analysis
[DM_PDF02:p023:L002] [예제 2.3]
[DM_PDF02:p023:L003] 최적해:
[DM_PDF02:p023:L004] 유모차 생산* = 0
[DM_PDF02:p023:L005] 보행기 생산*=40
[DM_PDF02:p023:L006] 자전거 생산*=40
[DM_PDF02:p023:L007] 목표셀값*=1440
[DM_PDF02:p023:L008] 23
[DM_PDF02:p023:L009] 주목
[DM_PDF02:p023:L010] 유모차의 판매이익이
[DM_PDF02:p023:L011] 변경된다면?
[DM_PDF02:p023:L012] 목적함수 계수 및 제한조건 우변값

## Page 024

[DM_PDF02:p024:L001] 24
[DM_PDF02:p024:L002] 민감도 보고서 (목표셀 계수 변화시)
[DM_PDF02:p024:L003] 유모차 판매이익을 현재 30만원에서 변화시킴
[DM_PDF02:p024:L004] “총판매이익”은 유모차 판매이익에 민감하지 않음
[DM_PDF02:p024:L005] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 025

[DM_PDF02:p025:L001] 25
[DM_PDF02:p025:L002] 민감도 보고서 (제한조건 우변값 변화시)
[DM_PDF02:p025:L003] ‘기계1’에 대한 사용가능시간(제한조건 우변값)을 변화
[DM_PDF02:p025:L004] 현재 240 시간에서 변화시킴
[DM_PDF02:p025:L005] 기계1시간 30시간 변화에 판매이익 160만원씩 비례하여 변화

## Page 026

[DM_PDF02:p026:L001] 26
[DM_PDF02:p026:L002] 민감도 보고서
[DM_PDF02:p026:L003] ‘해찾기 결과’ 대화상자에서 ‘민감도’를 선택하여
[DM_PDF02:p026:L004] 민감도 보고서를 출력하게 한다 (2010, 우편물 종류)
[DM_PDF02:p026:L005] 한계비용/수정비용
[DM_PDF02:p026:L006] Marginal cost
[DM_PDF02:p026:L007] Reduced cost
[DM_PDF02:p026:L008] 잠재가격
[DM_PDF02:p026:L009] Shadow price
[DM_PDF02:p026:L010] Lagrange multiplier

## Page 027

[DM_PDF02:p027:L001] 27
[DM_PDF02:p027:L002] 민감도 분석 요점
[DM_PDF02:p027:L003] (유용성: 새롭게 해찾기를 실행하지 않아도 결과를 예상)
[DM_PDF02:p027:L004] 1. 한계비용: 한계에 있는 최적해(계산값)를 한 단위 증가시킬
[DM_PDF02:p027:L005] 때 생기는 이익
[DM_PDF02:p027:L006] 2. 잠재가격: 제한조건 우변의 제약을 한 단위 완화(증가)할 때
[DM_PDF02:p027:L007] 생기는 이득
[DM_PDF02:p027:L008] 3. 허용증감 범위: 현재의 최적해(계산값)나 잠재가격이 변하
[DM_PDF02:p027:L009] 기 직전까지 목표셀 계수 및 우변값이 변할 수 있는 범위
[DM_PDF02:p027:L010] 
[DM_PDF02:p027:L011] 
[DM_PDF02:p027:L012] 
[DM_PDF02:p027:L013] 30100.1
[DM_PDF02:p027:L014] 301E
[DM_PDF02:p027:L015] 0
[DM_PDF02:p027:L016] 1025.1
[DM_PDF02:p027:L017] 1525.1
[DM_PDF02:p027:L018] 15
[DM_PDF02:p027:L019] 
[DM_PDF02:p027:L020] 
[DM_PDF02:p027:L021] 
[DM_PDF02:p027:L022] 
[DM_PDF02:p027:L023] E

## Page 028

[DM_PDF02:p028:L001] 28
[DM_PDF02:p028:L002] 민감도 분석(1): 한계비용
[DM_PDF02:p028:L003] 유모차의 현재 계산값을 ‘0’에서 ‘1개’를 증가시키면,
[DM_PDF02:p028:L004] (하한 조건을 >=0 에서 >=1 로 바꾸면),
[DM_PDF02:p028:L005] 1. 목표셀 값은 현재의 1440만원에서
[DM_PDF02:p028:L006] 1440-12.67= 1427.33 (만원)으로 감소한다.
[DM_PDF02:p028:L007] 2. 새로운 최적 생산량은 (1대, 40대, 37.33대) 로 변하나,
[DM_PDF02:p028:L008] 이는 민감도 보고서에서 알 수는 없다.

## Page 029

[DM_PDF02:p029:L001] 29
[DM_PDF02:p029:L002] 민감도 분석(2): 허용 가능의 범위 (목표셀 계수)
[DM_PDF02:p029:L003] 보행기 1대당 판매이익이 20만원에서 18만원으로
[DM_PDF02:p029:L004] 2만원 감소하면,
[DM_PDF02:p029:L005] 1. 최적해는 (0대,40대,40대) 로 변화 없음 그러나,
[DM_PDF02:p029:L006] 2. 목표셀 값은 1440만원 - 2만원*40대 = 1360만원 임

## Page 030

[DM_PDF02:p030:L001] 30
[DM_PDF02:p030:L002] 민감도 분석(3): 잠재가격
[DM_PDF02:p030:L003] 기계1의 제한조건을 241시간으로 1시간 더 증가시키면,
[DM_PDF02:p030:L004] 1. 목표셀의 최적값은 잠재가격인 5.33만원 증가한다.
[DM_PDF02:p030:L005] 2. 이때, 최적 생산량은 (0대, 40대, 40.33대) 로 변하나,
[DM_PDF02:p030:L006] 이는 민감도 보고서에서 알 수는 없다.
[DM_PDF02:p030:L007] 3. 잠재가격으로 각 제품의 가치를 계산하면
[DM_PDF02:p030:L008] 유모차: 가치… 8*5.33+4*0+4*0=42.67 > 30 …판매 (생산 안 함)
[DM_PDF02:p030:L009] 보행기: 가치…3*5.33+4*0+0*0=16 < 20 …판매 (생산 함)
[DM_PDF02:p030:L010] 자전거=3*5.33+0*0+1*0=16 = 16 (생산 함)

## Page 031

[DM_PDF02:p031:L001] 31
[DM_PDF02:p031:L002] 민감도 분석(4): 허용 가능의 범위 (우변값)
[DM_PDF02:p031:L003] 잠재가격이 변하지 않는 우변 값의 범위를 의미함
[DM_PDF02:p031:L004] 기계1의 이용가능시간을 237시간으로 3시간 감소시키면,
[DM_PDF02:p031:L005] 1. 목표셀 값은 3*5.33=15.99(만원) 감소한다.
[DM_PDF02:p031:L006] {이때, 최적 생산량은 (0대,40대,39대) 생산한다.
[DM_PDF02:p031:L007] 그러나 이는 민감도 보고서에서는 알 수 없다.}

## Page 032

[DM_PDF02:p032:L001] 32
[DM_PDF02:p032:L002] 민감도 분석 연습
[DM_PDF02:p032:L003] (Reduced cost=Marginal cost =수정비용=한계비용 ; Shadow price=잠재가격)
[DM_PDF02:p032:L004] =라그랑지 승수
[DM_PDF02:p032:L005] 최적 생산량은 모델 Q-250는 3대, 모델 Q-300는 4대 이다.
[DM_PDF02:p032:L006] (1) 공정1의 작업가능시간(RHS)이 1시간 증가되면 이익은
[DM_PDF02:p032:L007] 얼마나 증가되는가? 작업가능시간이 얼마 이상일 때 잠재가
[DM_PDF02:p032:L008] 격이 변하는가?
[DM_PDF02:p032:L009] (2) 공정2 및 공정3에 대해 동일한 질문 …

## Page 033

[DM_PDF02:p033:L001] 33
[DM_PDF02:p033:L002] 목적함수 계수의 허용가능 증가/감소
[DM_PDF02:p033:L003]  최적해가 유지되는 목적함수 계수 범위
[DM_PDF02:p033:L004] 30 x1 + 20 x2 = k
[DM_PDF02:p033:L005] x1의 계수만 변화하는 경우:
[DM_PDF02:p033:L006] c1 x1 + 20 x2 = k
[DM_PDF02:p033:L007] 이때의 기울기 = -(c1/20)
[DM_PDF02:p033:L008] -8/3 <= -c1/20 <= -1 일때
[DM_PDF02:p033:L009] (53.333 >= c1 >= 20)
[DM_PDF02:p033:L010] 꼭지점 (18,32)이 여전히 최적임
[DM_PDF02:p033:L011] x2
[DM_PDF02:p033:L012] x1
[DM_PDF02:p033:L013] 4x1+0x2=100
[DM_PDF02:p033:L014] 4x1+4x2=200
[DM_PDF02:p033:L015] 8x1+3x2=240
[DM_PDF02:p033:L016] c1 x1+ 20 x2 = k
[DM_PDF02:p033:L017] X2<=40
[DM_PDF02:p033:L018] (기울기: -1)
[DM_PDF02:p033:L019] (기울기: -8/3)
[DM_PDF02:p033:L020] (기울기: -c1/20)

## Page 034

[DM_PDF02:p034:L001] 34
[DM_PDF02:p034:L002] • 목적함수 계수의 변화
[DM_PDF02:p034:L003] 허용가능 증가치 = 53.33 - 30 = 23.33
[DM_PDF02:p034:L004] 허용가능 감소치 = 20 – 30 = -10
[DM_PDF02:p034:L005] 목적함수 계수의 허용가능 증가/감소

## Page 035

[DM_PDF02:p035:L001] 35
[DM_PDF02:p035:L002] 한계비용(할인가,수정비용) … 참고
[DM_PDF02:p035:L003]  한계비용(marginal cost)
[DM_PDF02:p035:L004] =할인가(reduced cost)
[DM_PDF02:p035:L005] • x1의 한계비용: 최적해가 하한값인 경우임.
[DM_PDF02:p035:L006] 하한(lower bound) x1 >= 0
[DM_PDF02:p035:L007] 대신 x1 >= 1 적용시의
[DM_PDF02:p035:L008] 목적함수 변화.
[DM_PDF02:p035:L009] 최적해가 안 변하면 0.
[DM_PDF02:p035:L010] • 상한이 있고, 최적해가
[DM_PDF02:p035:L011] 상한값인 경우, 한계비용은
[DM_PDF02:p035:L012] x2 <= 40 대신 x2 <= 41 일때의
[DM_PDF02:p035:L013] 목적함수 변화 (여기서는 0)

## Page 036

[DM_PDF02:p036:L001] 36
[DM_PDF02:p036:L002] 잠재가격 (라그랑지 승수)
[DM_PDF02:p036:L003]  잠재가격(Shadow price)
[DM_PDF02:p036:L004] • 기계1 작업시간의 잠재가격:
[DM_PDF02:p036:L005] 8 x1 + 3 x2 <= 240 대신
[DM_PDF02:p036:L006] 8 x1 + 3 x2 <= 241 적용
[DM_PDF02:p036:L007] 목적함수 변화
[DM_PDF02:p036:L008] • 새로운 최적해
[DM_PDF02:p036:L009] 8 x1 + 3 x2 = 241
[DM_PDF02:p036:L010] 4 x1 + 4 x2 = 200
[DM_PDF02:p036:L011]  교점: (18.2, 31.8)
[DM_PDF02:p036:L012] 목적함수 값= 30(18.2)+20(31.8)
[DM_PDF02:p036:L013] = 1182
[DM_PDF02:p036:L014] 잠재가격 = 1182-1180 = 2
[DM_PDF02:p036:L015] x2
[DM_PDF02:p036:L016] x1
[DM_PDF02:p036:L017] 4x1+0x2=100
[DM_PDF02:p036:L018] 4x1+4x2=200
[DM_PDF02:p036:L019] 8x1+3x2=240
[DM_PDF02:p036:L020] 30x1+ 20 x2 = k
[DM_PDF02:p036:L021] X2<=40
[DM_PDF02:p036:L022] (기울기: -1)
[DM_PDF02:p036:L023] (기울기: -8/3)
[DM_PDF02:p036:L024] 8 x1 + 3 x2 <= 241

## Page 037

[DM_PDF02:p037:L001] 37
[DM_PDF02:p037:L002] [참고] Excel 해찾기 (번역 오류)
[DM_PDF02:p037:L003] 해법:
[DM_PDF02:p037:L004] 1) 선형문제  LP 심플렉스
[DM_PDF02:p037:L005] 2) 미분가능 비선형
[DM_PDF02:p037:L006]  비선형 GRG
[DM_PDF02:p037:L007] 3) 미분불가능 비선형
[DM_PDF02:p037:L008]  Evolutionary
[DM_PDF02:p037:L009] Subject to (~을 조건으로)
[DM_PDF02:p037:L010] the constraints
[DM_PDF02:p037:L011] “LP 심플렉스”
[DM_PDF02:p037:L012] “제한조건”

## Page 038

[DM_PDF02:p038:L001] 38
[DM_PDF02:p038:L002] 우편물 종류 “민감도”
[DM_PDF02:p038:L003] Sensitivity (report)
[DM_PDF02:p038:L004] [참고] Excel 해찾기 (번역 오류)
[DM_PDF02:p038:L005] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 039

[DM_PDF02:p039:L001] 실습문제
[DM_PDF02:p039:L002] [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 040

[DM_PDF02:p040:L001] 40
[DM_PDF02:p040:L002] 실습#1 (By hand)
[DM_PDF02:p040:L003] Maximize 40 x1 + 30 x2
[DM_PDF02:p040:L004] subject to 0.4 x1 + 0.5 x2 <= 20
[DM_PDF02:p040:L005] 0.2 x2 <= 5
[DM_PDF02:p040:L006] 0.6 x1 + 0.3 x2 <= 21
[DM_PDF02:p040:L007] x1 >= 0, x2 >= 0
[DM_PDF02:p040:L008] (1) 가능영역을 정확하게 그려라.
[DM_PDF02:p040:L009] (2) 목적함수 값이 1200 이 되는 직선을 빨간색으로 그려라.
[DM_PDF02:p040:L010] (3) (2)의 목적함수 그래프를 평행이동하여 최적 해를 구하라.
[DM_PDF02:p040:L011] (4) 최적 해가 유지되는 목적함수 x1의 계수(c1)의 범위를 구하라.
[DM_PDF02:p040:L012] (5) 최적 해에서 첫째 제약식에 대한 잠재가격을 계산하라.
[DM_PDF02:p040:L013] ---------------------------------------------------------------------------------------------
[DM_PDF02:p040:L014] 확인 (답) (3) x1=25, x2=20, 1600; (4) 24<=c1<=60; (5) 33.33

## Page 041

[DM_PDF02:p041:L001] 1) 다음 문제의 최적해를 구하라.
[DM_PDF02:p041:L002] 2) 최적해가 변하지 않는 x1의 계수의 범위를 구하라.
[DM_PDF02:p041:L003] 3) x1과 x2의 한계비용 (marginal cost)을 각각 구하라.
[DM_PDF02:p041:L004] (주의) 각 변수의 상한과 하한의 유무를 확인하고, 존재한
[DM_PDF02:p041:L005] 다면 각각의 경우에 대한 한계비용을 구함.
[DM_PDF02:p041:L006] minimize 6x1 + 4x2
[DM_PDF02:p041:L007] s.t. 2x1 + 1x2 >= 12
[DM_PDF02:p041:L008] 1x1 + 1x2 >= 10
[DM_PDF02:p041:L009] x2 <=4
[DM_PDF02:p041:L010] x1 >= 0, x2 >= 0
[DM_PDF02:p041:L011] 실습#2 (by hand)
[DM_PDF02:p041:L012] 1) (6, 4), 52
[DM_PDF02:p041:L013] 3) X1의 한계비용: 0 (하한, 상한에서 모
[DM_PDF02:p041:L014] 두 0)
[DM_PDF02:p041:L015] X2의 한계비용: -2 (하한에서는 0, 상한에
[DM_PDF02:p041:L016] 서 -2)
[DM_PDF02:p041:L017] 2) c1>= 4, c2<=6

## Page 042

[DM_PDF02:p042:L001] 실습문제 1 (PROBLEM #5.10)
[DM_PDF02:p042:L002] David, Ladeana, and Lydia are the sole partners and workers in a company that
[DM_PDF02:p042:L003] produces fine clocks. David and Ladeana are each available to work a maximum
[DM_PDF02:p042:L004] of 40 hours per week at the company, while Lydia is available to work a
[DM_PDF02:p042:L005] maximum of 20 hours per week.
[DM_PDF02:p042:L006] The company makes two different types of clocks: a grandfather clock and a
[DM_PDF02:p042:L007] wall clock. To make a clock, David assembles the inside mechanical parts of the
[DM_PDF02:p042:L008] clock while Ladeana produces the hand-carved wood casings. Lydia is
[DM_PDF02:p042:L009] responsible for taking orders and shipping the clocks. The amount of time
[DM_PDF02:p042:L010] required for each of these tasks is shown next.
[DM_PDF02:p042:L011] Time Required
[DM_PDF02:p042:L012] Task Grandfather Clock Wall Clock
[DM_PDF02:p042:L013] Assemble clock mechanism
[DM_PDF02:p042:L014] (by David)
[DM_PDF02:p042:L015] 6 hours 4 hours
[DM_PDF02:p042:L016] Carve wood casing
[DM_PDF02:p042:L017] (by Ladeana)
[DM_PDF02:p042:L018] 8 hours 4 hours
[DM_PDF02:p042:L019] Shipping (by Lydia) 3 hours 3 hours
[DM_PDF02:p042:L020] 실습#3 (by Excel)

## Page 043

[DM_PDF02:p043:L001] Each grandfather clock built and shipped yields a profit of $300, while each wall clock
[DM_PDF02:p043:L002] yields a profit of $200. The three partners now want to determine how many clocks of
[DM_PDF02:p043:L003] each type should be produced per week to maximize the total profit.
[DM_PDF02:p043:L004] Formulate a linear programming model and solve it by Excel; and conduct sensitivity
[DM_PDF02:p043:L005] analysis.
[DM_PDF02:p043:L006] 1) 최적해는 얼마인가
[DM_PDF02:p043:L007] 2) 회사는 grandfather clock의 가격을 올리려고 한다 (현재 $300). 하지만 생산
[DM_PDF02:p043:L008] 계획은 변경하지 않으려 한다. 회사가 올릴 수 있는 가격은 최대 얼마인가?
[DM_PDF02:p043:L009] 3) Ladeana의 1시간 노동력에 대한 잠재가격은 얼마인가?
[DM_PDF02:p043:L010] 4) 만약 Ladeana가 일하는 시간을 50시간까지 늘리면, 회사의 전체 수익은 어떻게
[DM_PDF02:p043:L011] 변하는가? 민감도 분석 결과값을 가지고 이를 설명하라.
[DM_PDF02:p043:L012] 실습#3 – Cont.
[DM_PDF02:p043:L013] 답 1) 3.33, 3.33, 1667 2) $400
[DM_PDF02:p043:L014] 3) 25 4) 25*10=250,  1917
