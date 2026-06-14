# DM_PDF08 — annotated PDF transcript

source: `decisionMaking/pdf_sources/DM_PDF08_ch06_integer_programming_week2.pdf`

## Page 001

[DM_PDF08:p001:L001]  1
[DM_PDF08:p001:L002]  6.8 공공 설비 입지 선정 모형
[DM_PDF08:p001:L003]  • 공공설비: 소방소, 파출소, 응급의료설비(병원), 학교 등
[DM_PDF08:p001:L004]  • 모든 지역이 혜택 받되 공공설비 설치 수는 최소화
[DM_PDF08:p001:L005]  [예제 6.7] 신도시 B의 응급 의료 서비스
[DM_PDF08:p001:L006]  • 응급차량대기 후보지 8곳을 선정
[DM_PDF08:p001:L007]  • 각 후보 지역에서 10분 이내 도달되는 행정 구역  아래 표
[DM_PDF08:p001:L008]  (전체 행정 구역은 13개)
[DM_PDF08:p001:L009]  • 13개 행정 구역이
[DM_PDF08:p001:L010]  모두 10분 이내에
[DM_PDF08:p001:L011]  응급 서비스를
[DM_PDF08:p001:L012]  받을 수 있게 하되,
[DM_PDF08:p001:L013]  설치 지역 수를 최소화하라.

## Page 002

[DM_PDF08:p002:L001]  2
[DM_PDF08:p002:L002]   모형화 가이드
[DM_PDF08:p002:L003] [[NODE:n_DM_PDF08.facility_location]] [[EVID:ev_DM_PDF08_002]] ① 후보지역에 공공설비 설치 여부  변수셀 (0-1 변수)
[DM_PDF08:p002:L004]  X=(x1,x2,…,x8)
[DM_PDF08:p002:L005]  ② 후보지역에서 10분 이내 도달 가능성: 13 X 8 행렬
[DM_PDF08:p002:L006]  앞의 표와 가로/세로 바뀜
[DM_PDF08:p002:L007]  행정구역이i 에서 후보지역j 까지 10분 이내 도달되면
[DM_PDF08:p002:L008]  Aij = 1, 아니면 Aij = 0 (여러분이 표로부터 작성해야 함)
[DM_PDF08:p002:L009]  ③ 응급차량 설치지역 수  목표셀 : 최소화
[DM_PDF08:p002:L010]  Aij = 0 or 1구역 i
[DM_PDF08:p002:L011]  후보지역 j
[DM_PDF08:p002:L012]  1
[DM_PDF08:p002:L013]  1
[DM_PDF08:p002:L014]  0
[DM_PDF08:p002:L015]  0
[DM_PDF08:p002:L016]  1
[DM_PDF08:p002:L017]  1
[DM_PDF08:p002:L018]  0
[DM_PDF08:p002:L019]  0

## Page 003

[DM_PDF08:p003:L001]  3
[DM_PDF08:p003:L002] [[NODE:n_DM_PDF08.coverage_matrix]] [[EVID:ev_DM_PDF08_003]] 후보지에서 10분 이내 도달 가능성: 0/1행렬
[DM_PDF08:p003:L003]  변수셀
[DM_PDF08:p003:L004]  행정구역 1 2 3 4 5 6 7 8
[DM_PDF08:p003:L005]  1 1 1
[DM_PDF08:p003:L006]  2 1 1 1
[DM_PDF08:p003:L007]  3 1 1 1
[DM_PDF08:p003:L008]  4 1 1
[DM_PDF08:p003:L009]  5 1 1 1
[DM_PDF08:p003:L010]  6 1 1 1
[DM_PDF08:p003:L011]  7 1 1 1
[DM_PDF08:p003:L012]  8 1 1
[DM_PDF08:p003:L013]  9 1 1 1 1
[DM_PDF08:p003:L014]  10 1 1
[DM_PDF08:p003:L015]  11 1 1
[DM_PDF08:p003:L016]  12 1
[DM_PDF08:p003:L017]  13 1 1
[DM_PDF08:p003:L018]  1 0 1 0 1 1 0 0
[DM_PDF08:p003:L019]  커버
[DM_PDF08:p003:L020]  1
[DM_PDF08:p003:L021]  1
[DM_PDF08:p003:L022]  1
[DM_PDF08:p003:L023]  1
[DM_PDF08:p003:L024]  1
[DM_PDF08:p003:L025]  1
[DM_PDF08:p003:L026]  2
[DM_PDF08:p003:L027]  1
[DM_PDF08:p003:L028]  2
[DM_PDF08:p003:L029]  1
[DM_PDF08:p003:L030]  1
[DM_PDF08:p003:L031]  0
[DM_PDF08:p003:L032]  2

## Page 004

[DM_PDF08:p004:L001]  4
[DM_PDF08:p004:L002]  수학적 모형
[DM_PDF08:p004:L003]  1. 의사결정변수
[DM_PDF08:p004:L004]  xj = 후보지역 j에 응급차량 설치여부 0-1 변수, (j=1,…,8)
[DM_PDF08:p004:L005]  2. 목적함수 = 총 설치지역 수 (x1+ x2+ … x8 )
[DM_PDF08:p004:L006]  3. 수리모형
[DM_PDF08:p004:L007]  Minimize x1+ x2+ … x8
[DM_PDF08:p004:L008]  subject to x1+ x4 >= 1 (행정구역 1)
[DM_PDF08:p004:L009]  x1+ x2+ x4 >= 1 (행정구역 2)
[DM_PDF08:p004:L010]  x1+ x2+ x7 >= 1 (행정구역 3)
[DM_PDF08:p004:L011]  … … … … …
[DM_PDF08:p004:L012]  x3+ x6 >= 1 (행정구역 13)
[DM_PDF08:p004:L013]  xj = 0 or 1, (j=1,…,8)

## Page 005

[DM_PDF08:p005:L001]  5
[DM_PDF08:p005:L002]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 006

[DM_PDF08:p006:L001]  6
[DM_PDF08:p006:L002]   모형화 가이드(참고)
[DM_PDF08:p006:L003]  ④ 모든 행정구역은 적어도 하나 이상의 응급차량 설치
[DM_PDF08:p006:L004]  지역으로부터 10분내에 도달되어야 함
[DM_PDF08:p006:L005]   set-covering problem 임.
[DM_PDF08:p006:L006] [[NODE:n_DM_PDF08.set_covering_model]] [[EVID:ev_DM_PDF08_001]] (행정구역별: covering 수 >= 1 )
[DM_PDF08:p006:L007]  (cf) set-partitioning problem (covering 수 = 1)
[DM_PDF08:p006:L008]  set-packing problem (covering 수 <= 1)
[DM_PDF08:p006:L009]  연습문제 6-20

## Page 007

[DM_PDF08:p007:L001]  7일반 모형(참고)
[DM_PDF08:p007:L002]  x=(x1,…,xn) 변수 벡터
[DM_PDF08:p007:L003]  xj = 지역 j에 입지선정 0-1 변수, (j=1,…,n)
[DM_PDF08:p007:L004]  A = covering 여부를 나타내는 행렬,
[DM_PDF08:p007:L005]  Aij = 1 , 구역 i는 입지 j가 선정되면 cover 됨,
[DM_PDF08:p007:L006]  Aij = 0 , 아니면
[DM_PDF08:p007:L007]  >=
[DM_PDF08:p007:L008]  제약식 조건
[DM_PDF08:p007:L009]  • Set Covering Problem : Ax >= 1, x : 0-1 열벡터
[DM_PDF08:p007:L010]  • Set Partitioning Problem: Ax = 1, x : 0-1 열벡터
[DM_PDF08:p007:L011]  • Set Packing Problem: Ax <= 1, x : 0-1 열벡터
[DM_PDF08:p007:L012]  (여기서 ‘1’ 은 모든 요소가 1인 열벡터)
[DM_PDF08:p007:L013]  Aij
[DM_PDF08:p007:L014]  xj
[DM_PDF08:p007:L015]  1
[DM_PDF08:p007:L016]  1
[DM_PDF08:p007:L017]  1
[DM_PDF08:p007:L018]  1
[DM_PDF08:p007:L019]  1

## Page 008

[DM_PDF08:p008:L001]  8
[DM_PDF08:p008:L002]  – 해찾기 실행
[DM_PDF08:p008:L003]  – 체크 포인트
[DM_PDF08:p008:L004]  • 공공설비 입지선정 모형에는 복수 최적해가 자주 발생함.
[DM_PDF08:p008:L005]  • ‘2진수 조건’대신 (i) 변경셀<= 1 (ii) 정수(int) 조건
[DM_PDF08:p008:L006]  대입하여도 됨

## Page 009

[DM_PDF08:p009:L001]  9
[DM_PDF08:p009:L002]  공공 설비 입지 선정 모형 – 앞의 문제 변형
[DM_PDF08:p009:L003]  (연습문제 19번)
[DM_PDF08:p009:L004]   서비스를 받을 수 있는 주민 수가
[DM_PDF08:p009:L005]  최대가 되도록.
[DM_PDF08:p009:L006]   상주 시설은 최대 3 군데
[DM_PDF08:p009:L007]  행정구역 주민수(만명)
[DM_PDF08:p009:L008]  1 5.4
[DM_PDF08:p009:L009]  2 4.2
[DM_PDF08:p009:L010]  3 7.1
[DM_PDF08:p009:L011]  4 6.2
[DM_PDF08:p009:L012]  5 8.3
[DM_PDF08:p009:L013]  6 4.7
[DM_PDF08:p009:L014]  7 6.6
[DM_PDF08:p009:L015]  8 8.7
[DM_PDF08:p009:L016]  9 7.6
[DM_PDF08:p009:L017]  10 5.1
[DM_PDF08:p009:L018]  11 10.0
[DM_PDF08:p009:L019]  12 6.9
[DM_PDF08:p009:L020]  13 9.5

## Page 010

[DM_PDF08:p010:L001]  10
[DM_PDF08:p010:L002]  19번 문제: 수학적 모형
[DM_PDF08:p010:L003]  1. 의사결정변수
[DM_PDF08:p010:L004]  xj = 후보지역 j에 응급차량 설치여부 0-1 변수, (j=1,…,8)
[DM_PDF08:p010:L005]  yi = 행정구역 i의 혜택여부 (0-1변수), (i=1,…,13)
[DM_PDF08:p010:L006]  2. 목적함수 = 혜택 받는 주민 수 (Max)
[DM_PDF08:p010:L007]  3. 수리모형
[DM_PDF08:p010:L008]  Maximize 5.4y1+ 4.2y2+ … + 9.5y13
[DM_PDF08:p010:L009]  subject to x1+ x2+ … x8 = 3
[DM_PDF08:p010:L010]  y1 <= x1+ x4 (행정구역 1)
[DM_PDF08:p010:L011]  y2 <= x1+ x2+ x4 (행정구역 2)
[DM_PDF08:p010:L012]  … … … … …
[DM_PDF08:p010:L013]  y13 <= x3+ x6 (행정구역 13)
[DM_PDF08:p010:L014]  yi , xj = 0 or 1, (i=1,…,13 ; j=1,…,8)
[DM_PDF08:p010:L015]  xj>=0 (j=1,2,3), yj = 0 or 1 (j=1,2,3)

## Page 011

[DM_PDF08:p011:L001]  11
[DM_PDF08:p011:L002]  범하기 쉬운 잘못된 모형화
[DM_PDF08:p011:L003]  xj = 후보지역 j에 응급차량 설치여부 0-1 변수, (j=1,…,8)
[DM_PDF08:p011:L004]  Maximize 5.4 (x1+ x4 ) + 4.2 (x1+ x2+ x4 )
[DM_PDF08:p011:L005]  + … + 9.5(x3+ x6 ) (혜택 받는 주민수)
[DM_PDF08:p011:L006]  subject to x1+ x2+ … x8 = 3 … 전체 설치대수
[DM_PDF08:p011:L007]  x1+ x4 >= 1 (행정구역 1)
[DM_PDF08:p011:L008]  x1+ x2+ x4 >= 1 (행정구역 2)
[DM_PDF08:p011:L009]  … … … … …
[DM_PDF08:p011:L010]  x3+ x6 >= 1 (행정구역 13)
[DM_PDF08:p011:L011]  xj = 0 or 1, (j=1,…,8)
[DM_PDF08:p011:L012]  xj>=0 (j=1,2,3), yj = 0 or 1 (j=1,2,3)

## Page 012

[DM_PDF08:p012:L001]  12
[DM_PDF08:p012:L002]  변형 모형의 스프레드시트
[DM_PDF08:p012:L003]  0/1 변수
[DM_PDF08:p012:L004]  Covering수는 2이상 나올 수 있음
[DM_PDF08:p012:L005]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 013

[DM_PDF08:p013:L001]  13
[DM_PDF08:p013:L002]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 014

[DM_PDF08:p014:L001]  14
[DM_PDF08:p014:L002]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 015

[DM_PDF08:p015:L001]  15분지한계법 적용(순수/혼합 정수계획)
[DM_PDF08:p015:L002]  예제 6.9
[DM_PDF08:p015:L003]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 016

[DM_PDF08:p016:L001]  16분지한계법 적용과정2
[DM_PDF08:p016:L002]  다음은 Z 값이 큰
[DM_PDF08:p016:L003]  부문제부터 적용
[DM_PDF08:p016:L004]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 017

[DM_PDF08:p017:L001]  17
[DM_PDF08:p017:L002]  절단
[DM_PDF08:p017:L003]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 018

[DM_PDF08:p018:L001]  18
[DM_PDF08:p018:L002]  ㅁ
[DM_PDF08:p018:L003]  비교(1)
[DM_PDF08:p018:L004]  비교(2)
[DM_PDF08:p018:L005]  최적 목적함수 값이
[DM_PDF08:p018:L006]  큰 부분제를 먼저 분기함
[DM_PDF08:p018:L007]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 019

[DM_PDF08:p019:L001]  19
[DM_PDF08:p019:L002]  절단
[DM_PDF08:p019:L003]  L=48 bound
[DM_PDF08:p019:L004]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 020

[DM_PDF08:p020:L001]  20
[DM_PDF08:p020:L002]  L=48
[DM_PDF08:p020:L003]  Z<L 절단
[DM_PDF08:p020:L004]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 021

[DM_PDF08:p021:L001]  21
[DM_PDF08:p021:L002]  최적해
[DM_PDF08:p021:L003]  L=48
[DM_PDF08:p021:L004]  Z<L 절단
[DM_PDF08:p021:L005]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 022

[DM_PDF08:p022:L001]  22
[DM_PDF08:p022:L002]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 023

[DM_PDF08:p023:L001]  23
[DM_PDF08:p023:L002]  [EXTRACTION_LOW_TEXT] 이 페이지는 추출 텍스트가 매우 적다. 표/수식/이미지 누락 가능성이 있어 OCR 또는 원본 대조가 필요하다.

## Page 024

[DM_PDF08:p024:L001]  24
[DM_PDF08:p024:L002]  실습 1번
[DM_PDF08:p024:L003]  ** 클래스넷에 올려 놓은 실습문제1번(Week2).hwp
[DM_PDF08:p024:L004]  파일보고 문제를 풀것
[DM_PDF08:p024:L005]  실습문제 2번 (a) --- sheet1
[DM_PDF08:p024:L006]  (b) --- sheet2
[DM_PDF08:p024:L007]  (참고) 한글 파일에 있는 표를 ‘복사’하여 엑셀시트에
[DM_PDF08:p024:L008]  ‘붙여 넣기’할 수 있음

## Page 025

[DM_PDF08:p025:L001]  다음을 분지한계법 (Branch and Bound)을 적용하여 구하라.
[DM_PDF08:p025:L002]  *반드시 계산과정을 p.23처럼 tree로 나타내고 최적해를 표시할 것.
[DM_PDF08:p025:L003]  (클래스넷 “분지한계법.hwp” 참고, 계산 과정 시 엑셀 사용).
[DM_PDF08:p025:L004]  Maximize 5x1+8x2
[DM_PDF08:p025:L005]  S.T. x1+x2 ≤ 7
[DM_PDF08:p025:L006]  3x1+5x2 ≤ 30
[DM_PDF08:p025:L007]  x1, x2≥0; x1, x2 are integer
[DM_PDF08:p025:L008]  정답: (x1,x2)=(0,6)
[DM_PDF08:p025:L009]  25
[DM_PDF08:p025:L010]  실습 2번
