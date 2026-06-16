# DS_PDF08_ML1 — annotated PDF transcript

- title: DS08 머신러닝 Part 1
- source_pdf: `dataScience/pdf_raw/[Lecture][DS][08][01] 머신러닝_Part_1 (2).pdf`
- transcript: `dataScience/txt_raw/DS_PDF04__machine_learning_part_1__full_transcript.txt`

## PAGE 001

- `DS_PDF08_ML1:p001:L001` Machine Learning (1)[140316]DATA SCIENCE
- `DS_PDF08_ML1:p001:L002` HunsikShinDepartment of Industrial and Data Engineering{hunsik.shin}@hongik.ac.kr

## PAGE 002

- `DS_PDF08_ML1:p002:L001` 제목
- `DS_PDF08_ML1:p002:L002` 2
- `DS_PDF08_ML1:p002:L003` 제목
- `DS_PDF08_ML1:p002:L004` Machine Learning BasicsMachine learning (기계학습)A set of methods that can automatically detect patterns in data, and then use the uncovered patterns to predict future data, or to perform other kinds of decision making under uncertainty“Machine Learning: A Probabilistic Perspective” by Kevin P . Murphy
- `DS_PDF08_ML1:p002:L005` Supervised learning (지도학습)-Machine learning task of inferring a function from labeled training data- 정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습Unsupervised learning (비지도학습)-Machine learning algorithm used to draw inferences from unlabeled training data- 관측치의 특성 정보를 담고 있는 데이터에 적용, 데이터에 존재하는 패턴 혹은 인사이트를 찾음Reinforcement learning (강화학습)-concerned with how software agents

## PAGE 003

- `DS_PDF08_ML1:p003:L001` 제목
- `DS_PDF08_ML1:p003:L002` 3
- `DS_PDF08_ML1:p003:L003` 제목
- `DS_PDF08_ML1:p003:L004` Machine Learning BasicsSupervised Learning(지도학습)Machine learning task of inferring a function from labeled training data정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습

## PAGE 004

- `DS_PDF08_ML1:p004:L001` 제목
- `DS_PDF08_ML1:p004:L002` 4
- `DS_PDF08_ML1:p004:L003` 제목
- `DS_PDF08_ML1:p004:L004` Machine Learning BasicsSupervised Learning(지도학습)Machine learning task of inferring a function from labeled training data정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습

## PAGE 005

- `DS_PDF08_ML1:p005:L001` 제목
- `DS_PDF08_ML1:p005:L002` 5
- `DS_PDF08_ML1:p005:L003` 제목
- `DS_PDF08_ML1:p005:L004` Machine Learning BasicsSupervised Learning(지도학습)Machine learning task of inferring a function from labeled training data정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습

## PAGE 006

- `DS_PDF08_ML1:p006:L001` 제목
- `DS_PDF08_ML1:p006:L002` 6
- `DS_PDF08_ML1:p006:L003` 제목
- `DS_PDF08_ML1:p006:L004` Machine Learning BasicsSupervised Learning(지도학습)Machine learning task of inferring a function from labeled training data정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습

## PAGE 007

- `DS_PDF08_ML1:p007:L001` 제목
- `DS_PDF08_ML1:p007:L002` 7
- `DS_PDF08_ML1:p007:L003` 제목
- `DS_PDF08_ML1:p007:L004` Machine Learning BasicsSupervised Learning(지도학습)Machine learning task of inferring a function from labeled training data정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습

## PAGE 008

- `DS_PDF08_ML1:p008:L001` 제목
- `DS_PDF08_ML1:p008:L002` 8
- `DS_PDF08_ML1:p008:L003` 제목
- `DS_PDF08_ML1:p008:L004` Machine Learning BasicsSupervised Learning(지도학습)Machine learning task of inferring a function from labeled training data정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습

## PAGE 009

- `DS_PDF08_ML1:p009:L001` 제목
- `DS_PDF08_ML1:p009:L002` 9
- `DS_PDF08_ML1:p009:L003` 제목
- `DS_PDF08_ML1:p009:L004` Machine Learning BasicsSupervised Learning(지도학습)Machine learning task of inferring a function from labeled training data정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습

## PAGE 010

- `DS_PDF08_ML1:p010:L001` 제목
- `DS_PDF08_ML1:p010:L002` 10
- `DS_PDF08_ML1:p010:L003` 제목
- `DS_PDF08_ML1:p010:L004` Machine Learning BasicsSupervised Learning(지도학습)Machine learning task of inferring a function from labeled training data정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습

## PAGE 011

- `DS_PDF08_ML1:p011:L001` 제목
- `DS_PDF08_ML1:p011:L002` 11
- `DS_PDF08_ML1:p011:L003` 제목
- `DS_PDF08_ML1:p011:L004` Machine Learning BasicsSupervised Learning(지도학습)Machine learning task of inferring a function from labeled training data정답을 맞히는데 필요한 정보와 정답 모두 있는 데이터를 학습

## PAGE 012

- `DS_PDF08_ML1:p012:L001` 제목
- `DS_PDF08_ML1:p012:L002` 12
- `DS_PDF08_ML1:p012:L003` 제목
- `DS_PDF08_ML1:p012:L004` Machine Learning BasicsSupervised Learning(지도학습) For Text Mining문서(=Document)를 수치형 벡터로 표현(e.g. Bag-of-Words, Doc2Vec 등)하고 문서마다 Label 정보(e.g. Spam/Non-Spam)를 활용하여 분류 모델을 학습 및 추론
- `DS_PDF08_ML1:p012:L005` X1“Y ou”X2“are”X3“a”X4“good”X5“boy”X6“girl”X7“the”X8“world”11111000YSpam

## PAGE 013

- `DS_PDF08_ML1:p013:L001` 제목
- `DS_PDF08_ML1:p013:L002` 13
- `DS_PDF08_ML1:p013:L003` 제목
- `DS_PDF08_ML1:p013:L004` Machine Learning BasicsSupervised Learning(지도학습)Classification(분류):Output Y가 이산형(discrete)이거나 범주형(categorical)일 때 지도 학습 task•제품의 품질 분류 : Y = { 불량, 정상 }•스팸 메일 분류 : Y = { 정상 메일, 스팸 메일 }
- `DS_PDF08_ML1:p013:L005` Regression(회귀)/Prediction(예측): Output Y가 연속형(continuous)이거나 실수(real number)일 때지도 학습 task•내일 KOSPI 200 종가(=Y) 예측•강수량(=Y) 예측•5일 뒤의 전력 사용량 예측

## PAGE 014

- `DS_PDF08_ML1:p014:L001` 제목
- `DS_PDF08_ML1:p014:L002` 14
- `DS_PDF08_ML1:p014:L003` 제목
- `DS_PDF08_ML1:p014:L004` Machine Learning BasicsSupervised Learning(지도학습)Classification(분류):Output Y가 이산형(discrete)이거나 범주형(categorical)일 때 지도 학습 taskRegression(회귀)/Prediction(예측): Output Y가 연속형(continuous)이거나 실수(real number)일 때지도 학습 task

## PAGE 015

- `DS_PDF08_ML1:p015:L001` 제목
- `DS_PDF08_ML1:p015:L002` 15
- `DS_PDF08_ML1:p015:L003` 제목
- `DS_PDF08_ML1:p015:L004` Machine Learning BasicsSupervised Learning(지도학습)Classification(분류):Output Y가 이산형(discrete)이거나 범주형(categorical)일 때 지도 학습 task

## PAGE 016

- `DS_PDF08_ML1:p016:L001` 제목
- `DS_PDF08_ML1:p016:L002` 16
- `DS_PDF08_ML1:p016:L003` 제목
- `DS_PDF08_ML1:p016:L004` Machine Learning BasicsSupervised Learning(지도학습)Regression(회귀)/Prediction(예측): Output Y가 연속형(continuous)이거나 실수(real number)일 때지도 학습 task

## PAGE 017

- `DS_PDF08_ML1:p017:L001` 제목
- `DS_PDF08_ML1:p017:L002` 17
- `DS_PDF08_ML1:p017:L003` 제목
- `DS_PDF08_ML1:p017:L004` Machine Learning Basics기계학습 모델 학습의 의미분류 모델의 성능은 정확도(=accuracy)를 기준으로 측정 à 높은 정확도를 갖는 모델이 좋은 성능을 가짐•모델 학습 목표 = 높은 성능•모델의 학습 과정 = 모델의 성능이 높도록 모델를 구성하는 가중치(=weight)를 정하는 과정e,g. 𝑦=𝑎∗𝑋!+𝑏∗𝑋"+𝑐∗𝑋#모델일 때, 주어진 데이터를 기반으로 성능이 높을 수 있는 𝑎,𝑏,𝑐 값을 찾는 것
- `DS_PDF08_ML1:p017:L005` •성능의 반대 개념은 손실(=loss), 오류(=cost) à 높은 성능 = 낮은 손실 = 낮은 오류•모델을 학습할 땐, 성능을 최대화(=maximization)하거나 손실을 최소화(=minimization)하는 가중치 계산à대부분의 경우, 손실을 최소화하는 방법을 사용

## PAGE 018

- `DS_PDF08_ML1:p018:L001` 제목
- `DS_PDF08_ML1:p018:L002` 18
- `DS_PDF08_ML1:p018:L003` 제목
- `DS_PDF08_ML1:p018:L004` 회귀분석(Regression Analysis)•1885년 영국 F. Galton의 1078쌍 부자간의 키 관계 분석이 시초: 회귀[regression, 回歸] 부모와 자식 간의 신장을 조사하여, 일반적으로 장신인 부모의 아이는 장신이지만, 그 평균신장은 부모만큼 크지 않다는 것을 밝혀냈다. 다시 말하면 아이의 신장은 항상 일반적인 평균으로 되돌아가는 경향이 있다고 하여, 이것을 평균의 회귀현상이라고 함
- `DS_PDF08_ML1:p018:L005` •회귀분석은 변수들 사이의 관계를 추정하는 분석방법이다. 기본적으로 변수들 사이에서 나타나는 경향성을 설명하는 것이 주 목적

## PAGE 019

- `DS_PDF08_ML1:p019:L001` 제목
- `DS_PDF08_ML1:p019:L002` 19
- `DS_PDF08_ML1:p019:L003` 제목
- `DS_PDF08_ML1:p019:L004` 회귀분석(Regression Analysis)•상관분석은 두 변수 사이에 선형적인 관련성이 있는지를 확인하는 단계이고, 회귀분석은 그 관련성을 직선이나 함수로 표현해서 한 변수를 다른 변수로 설명하거나 예측하는 단계

## PAGE 020

- `DS_PDF08_ML1:p020:L001` 제목
- `DS_PDF08_ML1:p020:L002` 20
- `DS_PDF08_ML1:p020:L003` 제목
- `DS_PDF08_ML1:p020:L004` 회귀분석(Regression Analysis)

## PAGE 021

- `DS_PDF08_ML1:p021:L001` 제목
- `DS_PDF08_ML1:p021:L002` 21
- `DS_PDF08_ML1:p021:L003` 제목
- `DS_PDF08_ML1:p021:L004` 회귀분석(Regression Analysis)

## PAGE 022

- `DS_PDF08_ML1:p022:L001` 제목
- `DS_PDF08_ML1:p022:L002` 22
- `DS_PDF08_ML1:p022:L003` 제목
- `DS_PDF08_ML1:p022:L004` 회귀분석(Regression Analysis)선형회귀분석-두 변수들 사이의 관계를 분석하는 방법-X변수 (독립변수, 등간 or 비율척도), Y변수 (종속변수, 등간 or 비율척도)-선형회귀모델: 독립변수와 종속변수 사이의 관계를 직선으로 표현단순선형회귀: 독립변수 1개다중선형회귀: 독립변수 2개 이상-목적두 변수 사이의 관계를 수치로 설명미래의 종속변수 값을 예측

## PAGE 023

- `DS_PDF08_ML1:p023:L001` 제목
- `DS_PDF08_ML1:p023:L002` 23
- `DS_PDF08_ML1:p023:L003` 제목
- `DS_PDF08_ML1:p023:L004` 회귀분석(Regression Analysis)선형회귀의 기본 가정-종속 변수와 독립변수들 간에는 선형성이 성립한다.-독립 변수는 정확히 측정된 값으로 확률적으로 변하는 값이 아닌 고정된 값이다.-오차는 평균이 0, 분산이 s2인 정규 분포를 따르며, 평균과 분산이 일정하다.-오차들 간은 서로 독립이다.-독립 변수들 간에는 다중 공선성(Multicollinearity)이 적어야 한다.

## PAGE 024

- `DS_PDF08_ML1:p024:L001` 제목
- `DS_PDF08_ML1:p024:L002` 24
- `DS_PDF08_ML1:p024:L003` 제목
- `DS_PDF08_ML1:p024:L004` 회귀분석(Regression Analysis)다중공선성(multicollinearity)-회귀분석에서독립변수들끼리 강한 선형관계가 있는 현상예)  𝑥!이 아빠 키,𝑥"가 엄마 키,𝑥#가 부모 평균 키라면𝑥#는𝑥!,𝑥"와 강하게 관련-데이터가 조금만 바뀌어도회귀계수가 크게 달라질 수있음 불안정해짐-각 변수의 효과를 분리하기 어려움
- `DS_PDF08_ML1:p024:L005` 독립변수 간 상관계수 확인-독립변수끼리 상관계수가 너무 높으면 다중공선성을 의심(상관계수∣𝑟∣>0.7또는∣𝑟∣>0.8)-Variance Inflation Factor (분산팽창계수, VIF)
- `DS_PDF08_ML1:p024:L006` 𝑉𝐼𝐹!=11−𝑅!"•𝑅!"는 특정 독립변수𝑥!를 나머지 독립변수들로 회귀했을 때의 결정계수•일반적으로VIF가 5 이상이면 주의, 10 이상이면 심각한 다중공선성

## PAGE 025

- `DS_PDF08_ML1:p025:L001` 제목
- `DS_PDF08_ML1:p025:L002` 25
- `DS_PDF08_ML1:p025:L003` 제목
- `DS_PDF08_ML1:p025:L004` 회귀분석(Regression Analysis)종속변수와 독립변수의 관계-회귀모델에서는 독립변수의 값에 대한 종속변수의 값이 오직 하나만 결정되는 함수적 관계가 아니고, 독립변수의 값이 종속변수 값의 확률분포에 따라 결정되는 확률적 관계-실제 데이터는 완전히 설명하지 못하는 요인혹은 랜덤한 오차가 포함되어 있음à키의 경우 유전, 영양, 운동, 수면, 환경, 측정오차들이 완전히 설명하지 못하는 요인

## PAGE 026

- `DS_PDF08_ML1:p026:L001` 제목
- `DS_PDF08_ML1:p026:L002` 26
- `DS_PDF08_ML1:p026:L003` 제목
- `DS_PDF08_ML1:p026:L004` 회귀분석(Regression Analysis)선형 회귀분석 모델-선형 회귀모델은 독립변수(X)와 종속변수(Y) 사이의 관계를 수식으로 표현하는 방법이다.-데이터를 이용하여 절편	𝛽#과 기울기 𝛽$(같은 회귀계수를 추정한다.-단순 선형회귀는 독립변수 1개를 사용하고, 다중 선형회귀는 2개 이상의 변수를 사용하여 값을 예측

## PAGE 027

- `DS_PDF08_ML1:p027:L001` 제목
- `DS_PDF08_ML1:p027:L002` 27
- `DS_PDF08_ML1:p027:L003` 제목
- `DS_PDF08_ML1:p027:L004` 회귀분석(Regression Analysis)•어떤 선이 최선인가?

## PAGE 028

- `DS_PDF08_ML1:p028:L001` 제목
- `DS_PDF08_ML1:p028:L002` 28
- `DS_PDF08_ML1:p028:L003` 제목
- `DS_PDF08_ML1:p028:L004` 회귀분석(Regression Analysis)잔차와 최소제곱법(Least Square Estimation)•잔차: 실제 관측값과 회귀모델 추정값의 차이
- `DS_PDF08_ML1:p028:L005` •최소 제곱법(Least Square Method): 다음 식을 최소로 하는 회귀모델 계수를 추정하는 방법

## PAGE 029

- `DS_PDF08_ML1:p029:L001` 제목
- `DS_PDF08_ML1:p029:L002` 29
- `DS_PDF08_ML1:p029:L003` 제목
- `DS_PDF08_ML1:p029:L004` 회귀분석(Regression Analysis)최소제곱법: 오차가 가장 작은 직선 찾기-최소제곱법은 실제 관측값과 회귀직선 사이의 오차를 제곱한 뒤 모두 더한 값이 가장 작아지는 직선을 찾는 방법-각 점에서 직선까지의 세로 거리인 잔차𝑒&를 이용하며, 목표는∑𝑒&"를 최소화하는 것-같은 데이터라도 직선의 기울기와 절편이 달라지면 오차제곱합이 달라지며, 가장 작은 값을 만드는 직선이 최적의 회귀직선

## PAGE 030

- `DS_PDF08_ML1:p030:L001` 제목
- `DS_PDF08_ML1:p030:L002` 30
- `DS_PDF08_ML1:p030:L003` 제목
- `DS_PDF08_ML1:p030:L004` 회귀분석(Regression Analysis)SST = SSR + SSE•SST: Sum of Squares T otal, 전체 변동량을 의미-실제 관측값𝑌&가 평균값.𝑌으로부터 얼마나 떨어져 있는지를 나타냄-데이터 자체가 원래 가지고 있는 총 변동성을 측정하는 값이다.•SSR: Sum of Squares Regression,회귀로 설명된 변동량을 의미-회귀모델이 예측한 값/𝑌&가 평균값.𝑌에서 얼마나 벗어나는지를 계산-회귀직선이 데이터의 변동을 얼마나 잘 설명하는지를보임•SSE: Sum of Squares Error, 회귀로 설명하지 못한 오차 변동량을 의미한다. -실제값𝑌&와 예측값/𝑌&사이의 차이를 나타내며, 값이 작을수록 회귀모델이 데이터를 더 잘 설명
- `DS_PDF08_ML1:p030:L005` 𝑆𝑆𝑇=𝑆𝑆𝑅+𝑆𝑆𝐸à전체 변동량 = 회귀모델이 설명한 변동량 + 설명하지 못한 오차 변동량

## PAGE 031

- `DS_PDF08_ML1:p031:L001` 제목
- `DS_PDF08_ML1:p031:L002` 31
- `DS_PDF08_ML1:p031:L003` 제목
- `DS_PDF08_ML1:p031:L004` 회귀분석(Regression Analysis)SST = SSR + SSE

## PAGE 032

- `DS_PDF08_ML1:p032:L001` 제목
- `DS_PDF08_ML1:p032:L002` 32
- `DS_PDF08_ML1:p032:L003` 제목
- `DS_PDF08_ML1:p032:L004` 회귀분석(Regression Analysis)결정계수-결정계수𝑅"는 회귀모델이 종속변수𝑌의 변동을 얼마나 잘 설명하는지를 나타내는 지표-전체 변동(SST) 중에서 회귀모델이 설명한 변동(SSR)의 비율로 정의𝑅"=𝑆𝑆𝑅𝑆𝑆𝑇-결정계수의 값은 0과 1 사이에 존재Ø𝑅"=1이면 회귀직선이 데이터의 변동을 완벽하게 설명한다는 의미Ø𝑅"=0이면 회귀모델이 변수 간의 관계를 전혀 설명하지 못한다는 의미-따라서 결정계수는 회귀모델의 적합도를 평가하는 대표적인 척도로 사용되며, 일반적으로 값이 1에 가까울수록 데이터에 잘 맞는 회귀모델이라고 해석

## PAGE 033

- `DS_PDF08_ML1:p033:L001` 제목
- `DS_PDF08_ML1:p033:L002` 33
- `DS_PDF08_ML1:p033:L003` 제목
- `DS_PDF08_ML1:p033:L004` 회귀분석(Regression Analysis)이상치의 영향-회귀분석은 데이터 전체의 오차를 최소화하기 때문에멀리 떨어진 이상치(outlier)에 큰 영향을 받음-하나의 이상치만 추가되어도 회귀선의 기울기와 절편이 크게 변할 수 있음-따라서 이상치는 모델의 예측 성능과 해석 결과를 왜곡시킬 수 있어 주의가 필요

## PAGE 034

- `DS_PDF08_ML1:p034:L001` 제목
- `DS_PDF08_ML1:p034:L002` 34
- `DS_PDF08_ML1:p034:L003` 제목
- `DS_PDF08_ML1:p034:L004` Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervised learning)의 한 유형

## PAGE 035

- `DS_PDF08_ML1:p035:L001` 제목
- `DS_PDF08_ML1:p035:L002` 35
- `DS_PDF08_ML1:p035:L003` 제목
- `DS_PDF08_ML1:p035:L004` Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervised learning)의 한 유형

## PAGE 036

- `DS_PDF08_ML1:p036:L001` 제목
- `DS_PDF08_ML1:p036:L002` 36
- `DS_PDF08_ML1:p036:L003` 제목
- `DS_PDF08_ML1:p036:L004` Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervised learning)의 한 유형

## PAGE 037

- `DS_PDF08_ML1:p037:L001` 제목
- `DS_PDF08_ML1:p037:L002` 37
- `DS_PDF08_ML1:p037:L003` 제목
- `DS_PDF08_ML1:p037:L004` Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervised learning)의 한 유형
- `DS_PDF08_ML1:p037:L005` 이상치 데이터가 추가된다면?

## PAGE 038

- `DS_PDF08_ML1:p038:L001` 제목
- `DS_PDF08_ML1:p038:L002` 38
- `DS_PDF08_ML1:p038:L003` 제목
- `DS_PDF08_ML1:p038:L004` Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervised learning)의 한 유형
- `DS_PDF08_ML1:p038:L005` 모델 가중치 변화 큼

## PAGE 039

- `DS_PDF08_ML1:p039:L001` 제목
- `DS_PDF08_ML1:p039:L002` 39
- `DS_PDF08_ML1:p039:L003` 제목
- `DS_PDF08_ML1:p039:L004` Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervised learning)의 한 유형
- `DS_PDF08_ML1:p039:L005` 모델 가중치 변화 큼

## PAGE 040

- `DS_PDF08_ML1:p040:L001` 제목
- `DS_PDF08_ML1:p040:L002` 40
- `DS_PDF08_ML1:p040:L003` 제목
- `DS_PDF08_ML1:p040:L004` Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervised learning)의 한 유형

## PAGE 041

- `DS_PDF08_ML1:p041:L001` 제목
- `DS_PDF08_ML1:p041:L002` 41
- `DS_PDF08_ML1:p041:L003` 제목
- `DS_PDF08_ML1:p041:L004` Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervised learning)의 한 유형
- `DS_PDF08_ML1:p041:L005` Linear regression을 통한 분류 à 한계 존재-선형회귀모델은 출력변수 Y의 값이 (−∞,∞)에서 정의 됨-반면 분류(classification)의 출력 변수는 이산 값(e.g. 0과 1)을 가짐-분류하고자 하는 클래스(class)가 여러 개인 경우(multi-class classification) 선형 회귀 모델로 학습하기어려움

## PAGE 042

- `DS_PDF08_ML1:p042:L001` 제목
- `DS_PDF08_ML1:p042:L002` 42
- `DS_PDF08_ML1:p042:L003` 제목
- `DS_PDF08_ML1:p042:L004` Classification Algorithm –Logistic RegressionClassification (분류)- 분류는 새로운 관측값(데이터)이여러 범주(category, class)중어느 하나에 속하는지를 식별하는 문제- 출력값이 이산적(discrete) 혹은 범주형 변수(class)인 지도학습(supervised learning)의 한 유형
- `DS_PDF08_ML1:p042:L005` Solution-분류 모델의 결과는 해당 class에 속할 확률 p(0~1)로 정의 (e.g. class 1에 속할 확률)à X = (3, 4.1, 2.1) 일 때, class 1에 속할 확률은 0.9 (=class 1로 분류)- 기존 선형회귀모델 출력변수 Y(−∞,∞)를 squeeze 하여 확률 과 연결- 이진 분류(Binary classification)에서 여러 개의 클래스를 분류하는 다중 클래스 분류로 확장

## PAGE 043

- `DS_PDF08_ML1:p043:L001` 제목
- `DS_PDF08_ML1:p043:L002` 43
- `DS_PDF08_ML1:p043:L003` 제목
- `DS_PDF08_ML1:p043:L004` Classification Algorithm –Logistic RegressionOdds성공 확률(success probability, 𝑝)가 실패확률 (1 –𝑝)에 비해 몇 배 더 높은가?-𝑝= probability of belonging to class 1(success),  odds = p / (1-p)-0과 1사이를 갖는 𝑝 를 가지고 0과 양의 무한대를 갖는 Odds로 변환, log를 씌워 logit으로 변환 가능- 1에 가까운 𝑝로예측 = 큰 수의 logit으로 예측 à logit에 대해 선형회귀함수를 학습 = 0과 1 사이를 예측하는 분류 함수 학습
- `DS_PDF08_ML1:p043:L005` Probability, 𝑝

## PAGE 044

- `DS_PDF08_ML1:p044:L001` 제목
- `DS_PDF08_ML1:p044:L002` 44
- `DS_PDF08_ML1:p044:L003` 제목
- `DS_PDF08_ML1:p044:L004` Classification Algorithm –Logistic RegressionOdds와 선형회귀모델에서 확률 p의 관계-0과 1사이를 갖는 𝑝 를 가지고 0과 양의 무한대를 갖는 Odds로 변환, log를 씌워 logit으로 변환 가능- 1에 가까운 𝑝로예측 = 큰 수의 logit으로 예측 à logit에 대해 선형회귀함수를 학습 = 0과 1 사이를 예측하는 분류 함수 학습
- `DS_PDF08_ML1:p044:L005` 𝐿𝑜𝑔𝑖𝑡=

## PAGE 045

- `DS_PDF08_ML1:p045:L001` 제목
- `DS_PDF08_ML1:p045:L002` 45
- `DS_PDF08_ML1:p045:L003` 제목
- `DS_PDF08_ML1:p045:L004` Classification Algorithm –Logistic RegressionLogistic regression-어떤 현상에 대한 관측데이터 X와 이들이 어떠한 클래스(class) 또는 범주(label)에 속하는지에 대한 정보 Y가 존재-Y가 두 개의 클래스로 이루어진 경우, 하나의 데이터가 successive class (Y=1) 일 확률을 아래 식으로 추정 가능

## PAGE 046

- `DS_PDF08_ML1:p046:L001` 제목
- `DS_PDF08_ML1:p046:L002` 46
- `DS_PDF08_ML1:p046:L003` 제목
- `DS_PDF08_ML1:p046:L004` Classification Algorithm –Logistic RegressionLogistic regression-어떤 현상에 대한 관측데이터 X와 이들이 어떠한 클래스(class) 또는 범주(label)에 속하는지에 대한 정보 Y가 존재-Y가 두 개의 클래스로 이루어진 경우, 하나의 데이터가 successive class (Y=1) 일 확률을 아래 식으로 추정 가능

## PAGE 047

- `DS_PDF08_ML1:p047:L001` 제목
- `DS_PDF08_ML1:p047:L002` 47
- `DS_PDF08_ML1:p047:L003` 제목
- `DS_PDF08_ML1:p047:L004` Classification Algorithm –Logistic RegressionLogistic regressionLogistic regression = p는 class 1일 확률이고 이를 logit의 형태로 변환하여 선형회귀함수와 연결한 모델그럼 가중치(=weight) 𝛽', 𝛽!, … 𝛽(는 어떻게 구할까?기계학습 모델 학습의 의미•모델의 학습 과정 = 모델의 성능이 높도록 모델를 구성하는 가중치(=weight)를 정하는 과정•모델을 학습할 땐, 성능을 최대화(=maximization)하거나 손실을 최소화(=minimization)하는 가중치 계산
- `DS_PDF08_ML1:p047:L005` 예측 𝒑예측 𝟏−𝒑실제 class0.80.210.90.110.10.900.20.80
- `DS_PDF08_ML1:p047:L006` 예측 𝒑예측 𝟏−𝒑실제 class0.10.910.40.610.70.300.60.40<성능이 좋은 분류 모델 A> <성능이 나쁜 분류 모델B>

## PAGE 048

- `DS_PDF08_ML1:p048:L001` 제목
- `DS_PDF08_ML1:p048:L002` 48
- `DS_PDF08_ML1:p048:L003` 제목
- `DS_PDF08_ML1:p048:L004` Classification Algorithm –Logistic RegressionLogistic regressionLogistic regression = p는 class 1일 확률이고 이를 logit의 형태로 변환하여 선형회귀함수와 연결한 모델그럼 가중치(=weight) 𝛽', 𝛽!, … 𝛽(는 어떻게 구할까?à두 모델 성능 비교는 성공 예측일 땐𝑝, 실패 예측일 땐 1−𝑝를 곱한 값으로 비교•A: 0.8*0.9*0.9*0.8 = 0.5184•B: 0.1*0.4*0.3*0.4 = 0.00480.5184 > 0.0048, 모델 A wins!à확률 곱이 최대가 되는 모델이 좋은 모델
- `DS_PDF08_ML1:p048:L005` 예측 𝒑예측 𝟏−𝒑실제 class0.80.210.90.110.10.900.20.80
- `DS_PDF08_ML1:p048:L006` 예측 𝒑예측 𝟏−𝒑실제 class0.10.910.40.610.70.300.60.40<성능이 좋은 분류 모델A> <성능이 나쁜 분류 모델B>

## PAGE 049

- `DS_PDF08_ML1:p049:L001` 제목
- `DS_PDF08_ML1:p049:L002` 49
- `DS_PDF08_ML1:p049:L003` 제목
- `DS_PDF08_ML1:p049:L004` Classification Algorithm –Logistic RegressionLogistic regression

## PAGE 050

- `DS_PDF08_ML1:p050:L001` 제목
- `DS_PDF08_ML1:p050:L002` 50
- `DS_PDF08_ML1:p050:L003` 제목
- `DS_PDF08_ML1:p050:L004` Classification Algorithm –Logistic RegressionLogistic regression

## PAGE 051

- `DS_PDF08_ML1:p051:L001` 제목
- `DS_PDF08_ML1:p051:L002` 51
- `DS_PDF08_ML1:p051:L003` 제목
- `DS_PDF08_ML1:p051:L004` Classification Algorithm –Logistic RegressionLogistic regression

## PAGE 052

- `DS_PDF08_ML1:p052:L001` 제목
- `DS_PDF08_ML1:p052:L002` 52
- `DS_PDF08_ML1:p052:L003` 제목
- `DS_PDF08_ML1:p052:L004` Classification Algorithm –Logistic RegressionLogistic regression

## PAGE 053

- `DS_PDF08_ML1:p053:L001` 제목
- `DS_PDF08_ML1:p053:L002` 53
- `DS_PDF08_ML1:p053:L003` 제목
- `DS_PDF08_ML1:p053:L004` Classification Algorithm –Logistic RegressionLogistic regression

## PAGE 054

- `DS_PDF08_ML1:p054:L001` 제목
- `DS_PDF08_ML1:p054:L002` 54
- `DS_PDF08_ML1:p054:L003` 제목
- `DS_PDF08_ML1:p054:L004` Classification Algorithm –Logistic RegressionLogistic regression –Multi-class classification

## PAGE 055

- `DS_PDF08_ML1:p055:L001` 제목
- `DS_PDF08_ML1:p055:L002` 55
- `DS_PDF08_ML1:p055:L003` 제목
- `DS_PDF08_ML1:p055:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)-데이터의 실제 클래스(𝑌)와 모델에 의해 예측된 클래스(/𝑌)를 비교하는 행렬-클래스 별로 잘 분류된 포인트와 잘못 분류된 포인트의 수를 정리한 행렬

## PAGE 056

- `DS_PDF08_ML1:p056:L001` 제목
- `DS_PDF08_ML1:p056:L002` 56
- `DS_PDF08_ML1:p056:L003` 제목
- `DS_PDF08_ML1:p056:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)-데이터의 실제 클래스(𝑌)와 모델에 의해 예측된 클래스(/𝑌)를 비교하는 행렬-클래스 별로 잘 분류된 포인트와 잘못 분류된 포인트의 수를 정리한 행렬

## PAGE 057

- `DS_PDF08_ML1:p057:L001` 제목
- `DS_PDF08_ML1:p057:L002` 57
- `DS_PDF08_ML1:p057:L003` 제목
- `DS_PDF08_ML1:p057:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)-데이터의 실제 클래스(𝑌)와 모델에 의해 예측된 클래스(/𝑌)를 비교하는 행렬-클래스 별로 잘 분류된 포인트와 잘못 분류된 포인트의 수를 정리한 행렬

## PAGE 058

- `DS_PDF08_ML1:p058:L001` 제목
- `DS_PDF08_ML1:p058:L002` 58
- `DS_PDF08_ML1:p058:L003` 제목
- `DS_PDF08_ML1:p058:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)-데이터의 실제 클래스(𝑌)와 모델에 의해 예측된 클래스(/𝑌)를 비교하는 행렬-클래스 별로 잘 분류된 포인트와 잘못 분류된 포인트의 수를 정리한 행렬

## PAGE 059

- `DS_PDF08_ML1:p059:L001` 제목
- `DS_PDF08_ML1:p059:L002` 59
- `DS_PDF08_ML1:p059:L003` 제목
- `DS_PDF08_ML1:p059:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)-데이터의 실제 클래스(𝑌)와 모델에 의해 예측된 클래스(/𝑌)를 비교하는 행렬-클래스 별로 잘 분류된 포인트와 잘못 분류된 포인트의 수를 정리한 행렬

## PAGE 060

- `DS_PDF08_ML1:p060:L001` 제목
- `DS_PDF08_ML1:p060:L002` 60
- `DS_PDF08_ML1:p060:L003` 제목
- `DS_PDF08_ML1:p060:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)-데이터의 실제 클래스(𝑌)와 모델에 의해 예측된 클래스(/𝑌)를 비교하는 행렬-클래스 별로 잘 분류된 포인트와 잘못 분류된 포인트의 수를 정리한 행렬

## PAGE 061

- `DS_PDF08_ML1:p061:L001` 제목
- `DS_PDF08_ML1:p061:L002` 61
- `DS_PDF08_ML1:p061:L003` 제목
- `DS_PDF08_ML1:p061:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)-데이터의 실제 클래스(𝑌)와 모델에 의해 예측된 클래스(/𝑌)를 비교하는 행렬-클래스 별로 잘 분류된 포인트와 잘못 분류된 포인트의 수를 정리한 행렬

## PAGE 062

- `DS_PDF08_ML1:p062:L001` 제목
- `DS_PDF08_ML1:p062:L002` 62
- `DS_PDF08_ML1:p062:L003` 제목
- `DS_PDF08_ML1:p062:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)

## PAGE 063

- `DS_PDF08_ML1:p063:L001` 제목
- `DS_PDF08_ML1:p063:L002` 63
- `DS_PDF08_ML1:p063:L003` 제목
- `DS_PDF08_ML1:p063:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)

## PAGE 064

- `DS_PDF08_ML1:p064:L001` 제목
- `DS_PDF08_ML1:p064:L002` 64
- `DS_PDF08_ML1:p064:L003` 제목
- `DS_PDF08_ML1:p064:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)

## PAGE 065

- `DS_PDF08_ML1:p065:L001` 제목
- `DS_PDF08_ML1:p065:L002` 65
- `DS_PDF08_ML1:p065:L003` 제목
- `DS_PDF08_ML1:p065:L004` Classification Algorithm –Logistic Regression분류 모델 평가 –성능 (Confusion Matrix)

## PAGE 066

- `DS_PDF08_ML1:p066:L001` 제목
- `DS_PDF08_ML1:p066:L002` 66
- `DS_PDF08_ML1:p066:L003` 제목
- `DS_PDF08_ML1:p066:L004` Classification Algorithm –Logistic Regression분류 모델간 평가
