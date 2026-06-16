# DS_PDF08_ML3 — annotated PDF transcript

- title: DS08 머신러닝 Part 3
- source_pdf: `dataScience/pdf_raw/[Lecture][DS][08][03] 머신러닝_Part_3.pdf`
- transcript: `dataScience/txt_raw/DS_PDF06__machine_learning_part_3__full_transcript.txt`

## PAGE 001

- `DS_PDF08_ML3:p001:L001` Machine Learning (3)[140316]DATA SCIENCE
- `DS_PDF08_ML3:p001:L002` HunsikShinDepartment of Industrial and Data Engineering{hunsik.shin}@hongik.ac.kr

## PAGE 002

- `DS_PDF08_ML3:p002:L001` 제목
- `DS_PDF08_ML3:p002:L002` 2
- `DS_PDF08_ML3:p002:L003` 제목
- `DS_PDF08_ML3:p002:L004` Introduction to ClusteringClustering군집화(Clustering)는 데이터 안에서 서로 비슷한 특성을 가진 객체들을 하나의 그룹 혹은 군집(cluster)으로 묶는 기법군집화에서는 각 객체가 어떤 그룹에 속해야 하는지에 대한정답 레이블(y)이 존재하지 않기 때문에, 비지도 학습(unsupervised learning)알고리즘군집화 알고리즘은 주로객체 간 유사도(similarity) 또는 거리(distance)정보를 활용서로 유사한 객체는 같은 군집,서로 다른 객체는 다른 군집으로 분류

## PAGE 003

- `DS_PDF08_ML3:p003:L001` 제목
- `DS_PDF08_ML3:p003:L002` 3
- `DS_PDF08_ML3:p003:L003` 제목
- `DS_PDF08_ML3:p003:L004` Introduction to ClusteringClustering좋은 군집의 기준은 여러 가지가 있지만, 공통적으로 군집 내부의 데이터들은 서로 유사하고(intra-cluster similarity), 군집 간의 객체들은 서로 이질적(inter-cluster dissimilarity)이어야 함à 군집 내 거리(intra-cluster distance)는 작고 군집 간 거리(inter-cluster distance)는 멀어야 함
- `DS_PDF08_ML3:p003:L005` 군집화 알고리즘을 적용하기 전에, 데이터 표현(Representation)과 데이터 간의 유사도/거리 정의가 중요
- `DS_PDF08_ML3:p003:L006` 출처: 이훈영, 연구조사방법론, 청람, 2012

## PAGE 004

- `DS_PDF08_ML3:p004:L001` 제목
- `DS_PDF08_ML3:p004:L002` 4
- `DS_PDF08_ML3:p004:L003` 제목
- `DS_PDF08_ML3:p004:L004` 𝒌-means clustering-비지도 학습의 대표적인 분석 방법으로 Clustering 방법들 중 가장 기본이 되는 기법-주어진 데이터를 유사한 K개의 군집으로 묶는 알고리즘-군집을 나누는 방법에 따라 여러 종류로 구분됨. -데이터에 대한 이해 단계인 (EDA, exploratory data analysis)단계에서 부터 고객 세그멘테이션, 이미지 분할 등에 광범위하게 적용 가능-모집단 또는 범주에 대한 사전 정보가 없을 때Ø주어진 관측값들 사이의 거리 측정Ø유사성을 이용하여 분석

## PAGE 005

- `DS_PDF08_ML3:p005:L001` 제목
- `DS_PDF08_ML3:p005:L002` 5
- `DS_PDF08_ML3:p005:L003` 제목
- `DS_PDF08_ML3:p005:L004` 𝒌-means clustering𝑛개의 데이터가 주어졌을 때, 두 데이터𝑥!와𝑥"사이의 유사성을 측정하기 위해Cosine,Euclidean, 혹은 임의로 정의한 거리d(𝑥!𝑥")를 사용모든 데이터는k개의 군집으로 나누어진다고 가정하며, 각 군집은 하나의 대표값 벡터(centroid)를 가짐
- `DS_PDF08_ML3:p005:L005` - 알고리즘: 군집의 대표값 벡터를 초기화(1) 군집화 과정에서 각 데이터 점을가장 가까운 대표값 벡터에 재할당(reassign)(2) 이후 각 군집에 속한 데이터들의 평균을 다시 계산하여 대표값 벡터를 업데이트(update)하는 과정을 반복
- `DS_PDF08_ML3:p005:L006` reassignupdate Centroid #1Centroid #2Data

## PAGE 006

- `DS_PDF08_ML3:p006:L001` 제목
- `DS_PDF08_ML3:p006:L002` 6
- `DS_PDF08_ML3:p006:L003` 제목
- `DS_PDF08_ML3:p006:L004` 𝒌-means clustering

## PAGE 007

- `DS_PDF08_ML3:p007:L001` 제목
- `DS_PDF08_ML3:p007:L002` 7
- `DS_PDF08_ML3:p007:L003` 제목
- `DS_PDF08_ML3:p007:L004` 𝒌-means clustering

## PAGE 008

- `DS_PDF08_ML3:p008:L001` 제목
- `DS_PDF08_ML3:p008:L002` 8
- `DS_PDF08_ML3:p008:L003` 제목
- `DS_PDF08_ML3:p008:L004` 𝒌-means clustering

## PAGE 009

- `DS_PDF08_ML3:p009:L001` 제목
- `DS_PDF08_ML3:p009:L002` 9
- `DS_PDF08_ML3:p009:L003` 제목
- `DS_PDF08_ML3:p009:L004` 𝒌-means clustering

## PAGE 010

- `DS_PDF08_ML3:p010:L001` 제목
- `DS_PDF08_ML3:p010:L002` 10
- `DS_PDF08_ML3:p010:L003` 제목
- `DS_PDF08_ML3:p010:L004` 𝒌-means clustering

## PAGE 011

- `DS_PDF08_ML3:p011:L001` 제목
- `DS_PDF08_ML3:p011:L002` 11
- `DS_PDF08_ML3:p011:L003` 제목
- `DS_PDF08_ML3:p011:L004` 𝒌-means clustering

## PAGE 012

- `DS_PDF08_ML3:p012:L001` 제목
- `DS_PDF08_ML3:p012:L002` 12
- `DS_PDF08_ML3:p012:L003` 제목
- `DS_PDF08_ML3:p012:L004` 𝒌-means clustering
- `DS_PDF08_ML3:p012:L005` 출처: https://commons.m.wikimedia.org/wiki/File:K-means_convergence.gif

## PAGE 013

- `DS_PDF08_ML3:p013:L001` 제목
- `DS_PDF08_ML3:p013:L002` 13
- `DS_PDF08_ML3:p013:L003` 제목
- `DS_PDF08_ML3:p013:L004` 𝒌-means clustering𝒌-means clustering 특징•𝑘-means은 local optimal을 찾는 heuristic 알고리즘 (매우 빠른 알고리즘으로 널리 사용)•계산 복잡도가 비교적 낮아, 전체 복잡도는 대략 𝑂(𝑛⋅𝑖⋅𝑘)로 표현 (𝑛=데이터 수,𝑖=반복(iteration) 수,𝑘=군집 수)•모든 데이터 간 거리를 계산하는pairwise distance matrix가 필요 없음 à 대규모 데이터셋에 특히 적합•데이터row 단위로 업데이트가 가능하므로, mini-batch 학습이나 분산 환경(distributed setting)에서 구현가능

## PAGE 014

- `DS_PDF08_ML3:p014:L001` 제목
- `DS_PDF08_ML3:p014:L002` 14
- `DS_PDF08_ML3:p014:L003` 제목
- `DS_PDF08_ML3:p014:L004` 𝒌-means clusteringMagnitude of vector•p−norm: 벡터의 크기를 정의하는 방식•|𝑋|#=!|𝑋$|#+…+|𝑋%|#•예시2-norm: |(3,0,4)|#&'="|3|'+|0|'+|4|'=51-norm: |(3,0,−4)|#&$=#|3|$+|0|$+|−4|$=70-norm: |(3,0,4|)#&(=|3|(+|4|(=2(à# of non-zero elements)
- `DS_PDF08_ML3:p014:L005` Inner product•내적은 두 벡터 간의 관계를 정의하는 방식•3,0,4)1,2,3=3∗1+0∗2+4∗3=3+0+12=15

## PAGE 015

- `DS_PDF08_ML3:p015:L001` 제목
- `DS_PDF08_ML3:p015:L002` 15
- `DS_PDF08_ML3:p015:L003` 제목
- `DS_PDF08_ML3:p015:L004` 𝒌-means clustering
- `DS_PDF08_ML3:p015:L005` tuhinmukherjee74.medium.com

## PAGE 016

- `DS_PDF08_ML3:p016:L001` 제목
- `DS_PDF08_ML3:p016:L002` 16
- `DS_PDF08_ML3:p016:L003` 제목
- `DS_PDF08_ML3:p016:L004` 𝒌-means clusteringSpherical 𝒌-means•Cosine similarity을 거리로 사용하는 𝑘–means•학습 방법은 앞서 설명한 방식과 동일, 거리 측정 기준만 변경 (거리 기준 변경으로도 결과가 확연히 달라짐)•scikit-learn 라이브러이 내 k-means 알고리즘의 거리 metric은 Euclidean으로 고정되어 있음

## PAGE 017

- `DS_PDF08_ML3:p017:L001` 제목
- `DS_PDF08_ML3:p017:L002` 17
- `DS_PDF08_ML3:p017:L003` 제목
- `DS_PDF08_ML3:p017:L004` 𝒌-means clusteringEuclidean Distance•두 벡터의 차이의 2−norm•
- `DS_PDF08_ML3:p017:L005` Cosine Similarity•두 벡터 간의 거리를 유닛 벡터 간의 내적으로 정의•
- `DS_PDF08_ML3:p017:L006` •
- `DS_PDF08_ML3:p017:L007` •유닛 벡터의 Euclidean 거리의 순서는 Cosine 유사도 순서 반대

## PAGE 018

- `DS_PDF08_ML3:p018:L001` 제목
- `DS_PDF08_ML3:p018:L002` 18
- `DS_PDF08_ML3:p018:L003` 제목
- `DS_PDF08_ML3:p018:L004` 𝒌-means clusteringLimitations1.Initial points 에 따라 군집의 모양이 달라짐2.적절한 군집의 개수 정의 필요3.노이즈 데이터에 민감함

## PAGE 019

- `DS_PDF08_ML3:p019:L001` 제목
- `DS_PDF08_ML3:p019:L002` 19
- `DS_PDF08_ML3:p019:L003` 제목
- `DS_PDF08_ML3:p019:L004` 𝒌-means clusteringLimitations1.Initial points 에 따라 군집의 모양이 달라짐

## PAGE 020

- `DS_PDF08_ML3:p020:L001` 제목
- `DS_PDF08_ML3:p020:L002` 20
- `DS_PDF08_ML3:p020:L003` 제목
- `DS_PDF08_ML3:p020:L004` 𝒌-means clusteringLimitations1.Initial points 에 따라 군집의 모양이 달라짐à좋은 initial points를 찾기 위해 k-means++ 사용à순차적으로 기존의 centroid에서 멀리 떨어진 점을 새로운 centroid로 선정
- `DS_PDF08_ML3:p020:L005` [scikit-learn 구현 내용]: init=‘k-means++’

## PAGE 021

- `DS_PDF08_ML3:p021:L001` 제목
- `DS_PDF08_ML3:p021:L002` 21
- `DS_PDF08_ML3:p021:L003` 제목
- `DS_PDF08_ML3:p021:L004` 𝒌-means clusteringLimitations2.적절한 군집의 개수 정의 필요à군집의 개수 k는 사용자가 직접 설정해야하는 hyper-parameteràSihlhouette score을 기반으로 군집화 품질의 척도를 계산집
- `DS_PDF08_ML3:p021:L005` •s ≈1: 군집 내부에 가깝고, 다른 군집과 멀다 à 군집화 잘 됨•s ≈0: 군집간 경계에 위치•s < 0: 잘못된 군집, 다른 군집과 가깝고 군집 내부에서는 멀다

## PAGE 022

- `DS_PDF08_ML3:p022:L001` 제목
- `DS_PDF08_ML3:p022:L002` 22
- `DS_PDF08_ML3:p022:L003` 제목
- `DS_PDF08_ML3:p022:L004` 𝒌-means clusteringLimitations2.적절한 군집의 개수 정의 필요à군집의 개수 k는 사용자가 직접 설정해야하는 hyper-parameteràSihlhouette score을 기반으로 군집화 품질의 척도를 계산집

## PAGE 023

- `DS_PDF08_ML3:p023:L001` 제목
- `DS_PDF08_ML3:p023:L002` 23
- `DS_PDF08_ML3:p023:L003` 제목
- `DS_PDF08_ML3:p023:L004` 𝒌-means clusteringLimitations2.적절한 군집의 개수 정의 필요à군집의 개수 k는 사용자가 직접 설정해야하는 hyper-parameteràSihlhouette score을 기반으로 군집화 품질의 척도를 계산집

## PAGE 024

- `DS_PDF08_ML3:p024:L001` 제목
- `DS_PDF08_ML3:p024:L002` 24
- `DS_PDF08_ML3:p024:L003` 제목
- `DS_PDF08_ML3:p024:L004` 𝒌-means clusteringLimitations2.적절한 군집의 개수 정의 필요à군집의 개수 k는 사용자가 직접 설정해야하는 hyper-parameteràSihlhouette score을 기반으로 군집화 품질의 척도를 계산집

## PAGE 025

- `DS_PDF08_ML3:p025:L001` 제목
- `DS_PDF08_ML3:p025:L002` 25
- `DS_PDF08_ML3:p025:L003` 제목
- `DS_PDF08_ML3:p025:L004` 𝒌-means clusteringLimitations3.노이즈 데이터에 민감함모든 점을 반드시 한 개 이상의 군집으로 assign 하기 때문에, 일단 가장 가까운 군집에 할당되어 centroid 를 크게 움직임

## PAGE 026

- `DS_PDF08_ML3:p026:L001` 제목
- `DS_PDF08_ML3:p026:L002` 26
- `DS_PDF08_ML3:p026:L003` 제목
- `DS_PDF08_ML3:p026:L004` 𝒌-means clusteringLimitations3.노이즈 데이터에 민감함모든 점을 반드시 한 개 이상의 군집으로 assign 하기 때문에, 일단 가장 가까운 군집에 할당되어 centroid 를 크게 움직임à 사전에 데이터의 노이즈를 미리 제거

## PAGE 027

- `DS_PDF08_ML3:p027:L001` 제목
- `DS_PDF08_ML3:p027:L002` 27
- `DS_PDF08_ML3:p027:L003` 제목
- `DS_PDF08_ML3:p027:L004` 𝒌-means clusteringLimitations4.원형(spherical)이 아닌 군집을 찾는데는 적절하지 않음.

## PAGE 028

- `DS_PDF08_ML3:p028:L001` 제목
- `DS_PDF08_ML3:p028:L002` 28
- `DS_PDF08_ML3:p028:L003` 제목
- `DS_PDF08_ML3:p028:L004` Association Analysis월마트(Walmart) 사례-90년대 중반, 매주 수요일 저녁마다 기저귀와 맥주의 매출이 함께 높아지는 현상 발견.-담당자가 맥주와 기저귀 진열대를 일부러 가까운 곳에 붙여 놓았더니 두 제품의 매출이 전날보다 5배 증가.-전혀 관련성이 없는 맥주와 기저귀의 연결고리를 알게 됨으로써 마케팅 전략을 새롭게 구성하여 기업의 매출 향상의 중요한 도구가 될 수 있음.
- `DS_PDF08_ML3:p028:L005` 출처: https://lifeindigital.org/

## PAGE 029

- `DS_PDF08_ML3:p029:L001` 제목
- `DS_PDF08_ML3:p029:L002` 29
- `DS_PDF08_ML3:p029:L003` 제목
- `DS_PDF08_ML3:p029:L004` Association Analysis연관성분석-데이터 내부에 존재하는 연관성, 항목 간의 상호 관계 혹은 종속 관계를 찾아내는 분석-하나의 거래나 사건에 포함되어 있는 항목들의 경향을 파악해서 상호연관성을 발견-어떤 개인이나 그룹에 의해 수행된 활동들 중에서 함께 발생하는(co-occurrence) 것들의 관계를 찾아내는 데이터 분석예) 고객이 구매한 장바구니를 분석하여 거래되는 상품들의 연관성(규칙)을 발견, 분석à관련 상품끼리의 묶음 상품, 어떤 상품을 사기 위해 가는 동선에 관련 상품을 진열.à누가 어떤 상품을 구매할 것인지를 예측, 이를 통한 매출의 극대화à장바구니 분석(Market basket analysis) 이라고도 함.

## PAGE 030

- `DS_PDF08_ML3:p030:L001` 제목
- `DS_PDF08_ML3:p030:L002` 30
- `DS_PDF08_ML3:p030:L003` 제목
- `DS_PDF08_ML3:p030:L004` Association Analysis연관성 분석 활용-유통업 : 고객들이 함께 구매할 상품을 제안할 수 있음-호텔/숙박업 : 고객들이 특정 서비스를 받은 후 어떤 서비스를 다음으로 원하는지 선제안 할 수 있음-금융사: 기존 금융 서비스 내역을 통해 대출 같은 특정 서비스를 받을 가능성이 높은 고객을 발굴할 수 있음-보험사 : 정상적인 청구 패턴과 다른 패턴을 보이는 고객을 찾아 추가 조사 실시할 수 있음
- `DS_PDF08_ML3:p030:L005` https://brunch.co.kr/@beusable/190

## PAGE 031

- `DS_PDF08_ML3:p031:L001` 제목
- `DS_PDF08_ML3:p031:L002` 31
- `DS_PDF08_ML3:p031:L003` 제목
- `DS_PDF08_ML3:p031:L004` Association Analysis연관성 분석활용
- `DS_PDF08_ML3:p031:L005` 출처: https://zephyrus1111.tistory.com/119

## PAGE 032

- `DS_PDF08_ML3:p032:L001` 제목
- `DS_PDF08_ML3:p032:L002` 32
- `DS_PDF08_ML3:p032:L003` 제목
- `DS_PDF08_ML3:p032:L004` Association Analysis연관성 분석활용
- `DS_PDF08_ML3:p032:L005` 출처: https://blog.naver.com/rosa2070/222071917780
- `DS_PDF08_ML3:p032:L006` 트랜잭션데이터(transaction data)

## PAGE 033

- `DS_PDF08_ML3:p033:L001` 제목
- `DS_PDF08_ML3:p033:L002` 33
- `DS_PDF08_ML3:p033:L003` 제목
- `DS_PDF08_ML3:p033:L004` Association Analysis연관성 분석활용-연관성 분석을 위해서는 연관 규칙 Association Rule을 찾아내야 함.Ø연관규칙: 특정 사건이 발생하였을 때 함께 발생되는 또 다른 사건의 규칙.-연관규칙을 알기 위해서는 -사건들이 여러 개 있어야 하며, -사건들 중 공통적으로 일어나는 사건들을 조합하여 하나의 규칙을 완성-여러 개의 항목집합들 중에서 공통적으로 자주 발생하는 빈발 항목집합(Frequent itemset) 찾기-이러한 항목들을 통해 만든 규칙을 빈발 패턴(Frequent pattern)이라고 함

## PAGE 034

- `DS_PDF08_ML3:p034:L001` 제목
- `DS_PDF08_ML3:p034:L002` 34
- `DS_PDF08_ML3:p034:L003` 제목
- `DS_PDF08_ML3:p034:L004` Association Analysis연관성규칙-A라는 상품과 B라는 상품이 서로 연관성이 있다고 하면 AàB라고 하는 연관 규칙 생성.•{조건} à{결과}예) 품목 A와 품목 B를 구매한 고객은 품목 C를 구매한다: (품목 A) & (품목 B) à(품목 C)-상품의 수가 증가할 수록 연관 규칙도 증가하게 됨. 그 중 과연 어떤 연관 규칙이 가장 크리티컬하게 사용될 수 있는지 평가가 필요함.

## PAGE 035

- `DS_PDF08_ML3:p035:L001` 제목
- `DS_PDF08_ML3:p035:L002` 35
- `DS_PDF08_ML3:p035:L003` 제목
- `DS_PDF08_ML3:p035:L004` Association Analysis연관성규칙-연관 규칙 평가 기준 : 지지도(support), 신뢰도(confidence), 향상도(lift)-규칙이라는 특성 상 많이 일어나지 않는 희박한 항목에 대해서는 그 규칙을 일반화하거나 신뢰할 수 없다는 단점-연관성을 일반화하거나 신뢰할 수 있는 판단 기준이 필요-연관 규칙의 유용성과 효율성 입증 기준

## PAGE 036

- `DS_PDF08_ML3:p036:L001` 제목
- `DS_PDF08_ML3:p036:L002` 36
- `DS_PDF08_ML3:p036:L003` 제목
- `DS_PDF08_ML3:p036:L004` Association Analysis연관성규칙 평가-지지도(Support)-전체거래(transaction)중 연관성 규칙을 구성하는 항목들(조건과 결과항목)이 포함된 거래의 비율을 의미-전체 거래항목 중 상품 A와 상품 B를 동시에 포함하여 거래하는 비율-A àB 라고 하는 규칙이 전체 거래 중 차지하는 비율을 통해 해당 연관 규칙이 얼마나 의미가 있는 규칙인지를 확인-지지도 = 𝑃(𝐴∩𝐵): A와 B가 동시에 포함된 거래 수 / 전체 거래 수-어느 정도 지지도가 있는 항목들 중에서 연관성 규칙을 알아보는 것이 바람직

## PAGE 037

- `DS_PDF08_ML3:p037:L001` 제목
- `DS_PDF08_ML3:p037:L002` 37
- `DS_PDF08_ML3:p037:L003` 제목
- `DS_PDF08_ML3:p037:L004` Association Analysis연관성규칙 평가-신뢰도(Confidence)-조건이 발생했을 때 결과가 동시에 일어날 확률, 신뢰도가 1에 가까울수록 의미있는 연관성을 가지고 있다고 할 수 있음-상품 A를 포함하는 거래 중 A와 B가 동시에 거래되는 비중-상품 A를 구매 했을 때 상품 B를 구매할 확률이 어느정도 되는지를 확인-신뢰도 = 𝑃(𝐵|𝐴)=𝑃(𝐴∩𝐵)/𝑃(𝐴)= A와 B가 동시에 포함된 거래 수 / A가 포함된  거래 수

## PAGE 038

- `DS_PDF08_ML3:p038:L001` 제목
- `DS_PDF08_ML3:p038:L002` 38
- `DS_PDF08_ML3:p038:L003` 제목
- `DS_PDF08_ML3:p038:L004` Association Analysis연관성규칙평가-향상도(Lift)-상품 A의 거래 중 항목 B가 포함된 거래의 비율 / 전체 상품 거래 중 상품 B가 거래된 비율-A가 주어지지 않았을 때 B의 확률 대비 A가 주어졌을 때 B의 확률 증가 비율-향상도 = *+∩-*+∗*-=*(-|+)*-→A와 B가 동시에 일어날 확률(지지도) / A, B가 독립된 사건일 때 A,B가 동시에 일어날 확률•향상도 = 1 : 조건과 결과는 우연에 의한 관계. 품목 A와 B사이에 아무런 관계가 상호 관계가 없다.•향상도 > 1 : 연관성이 높다. 우연이 아닌 의미있는 관계.

## PAGE 039

- `DS_PDF08_ML3:p039:L001` 제목
- `DS_PDF08_ML3:p039:L002` 39
- `DS_PDF08_ML3:p039:L003` 제목
- `DS_PDF08_ML3:p039:L004` Association Analysis연관성규칙예제 –지지도, 신뢰도, 향상도 계산-거래내역 데이터를 통한 구매 행렬 계산
- `DS_PDF08_ML3:p039:L005` -어느 대형 마트의 거래 내역
- `DS_PDF08_ML3:p039:L006` -거래 내역을 기반으로 만든 구매 행렬
- `DS_PDF08_ML3:p039:L007` 출처: https://zephyrus1111.tistory.com/119

## PAGE 040

- `DS_PDF08_ML3:p040:L001` 제목
- `DS_PDF08_ML3:p040:L002` 40
- `DS_PDF08_ML3:p040:L003` 제목
- `DS_PDF08_ML3:p040:L004` Association Analysis연관성규칙예제 –지지도, 신뢰도, 향상도 계산지지도 : A와B를 동시에 포함하는 비율이 높아야 한다.“A이면 B이다.” 라는 규칙이 지지받기 위해서는 실제로 A, B를 동시에 포함하는 비율 𝑃(𝐴∩𝐵)값이 커야 함을 의미. 이러한의미에서𝑃𝐴∩𝐵를지지도라고 함.
- `DS_PDF08_ML3:p040:L005` 예)- 사이다와 상추를 동시에 구입하는 거래는 5건 중 1건 뿐이다.- 따라서, “상추를 사는 사람은 사이다도 구입한다”라는 규칙은 지지받기에는 발생 횟수가 충분하지 않다.- “A이면 B이다” 라는 규칙이 지지받기 위해서는 실제로 A, B를 동시에 포함하는 비율이 높아야 한다는 것.

## PAGE 041

- `DS_PDF08_ML3:p041:L001` 제목
- `DS_PDF08_ML3:p041:L002` 41
- `DS_PDF08_ML3:p041:L003` 제목
- `DS_PDF08_ML3:p041:L004` Association Analysis연관성규칙예제 –지지도, 신뢰도, 향상도 계산신뢰도: A를 포함하는 거래 내역 중, B가 포함된 비율이 높아야 한다“A이면 B이다.” 라는 규칙이 지지받기 위해서는 실제로 A, B를 동시에 포함하는 비율 𝑃(𝐴∩𝐵)값이 커야 함을 의미. 이러한의미에서𝑃𝐴∩𝐵를지지도라고 함.
- `DS_PDF08_ML3:p041:L005` 예)-“삼겹살을 사는 사람은 상추도 구입한다” 라는 규칙의 신뢰도 :  𝑃상추삼겹살=!"#"=$%.
- `DS_PDF08_ML3:p041:L006` -“상추를 사는 사람은 사이다도 구입한다”라는 규칙의 신뢰도 : 𝑃사이다상추=$"!"=&$.-따라서, “상추를 사는 사람은 사이다도 구입한다” 라는 규칙이 “삼겹살을 사는 사람은 상추도 구입한다”라는 규칙보다 신뢰도가 더 높다.

## PAGE 042

- `DS_PDF08_ML3:p042:L001` 제목
- `DS_PDF08_ML3:p042:L002` 42
- `DS_PDF08_ML3:p042:L003` 제목
- `DS_PDF08_ML3:p042:L004` Association Analysis연관성규칙예제 –지지도, 신뢰도, 향상도 계산향상도: AàB라는 규칙이 있을 때, A는 B를 설명하기에 의미있는 사건/변수인가?만약 B가 발생한 비율이 𝑃𝐵=0.9 라면, 𝑃𝐵𝐴=𝑃(𝐵).즉, A와 B는 독립이 되어 A는 B를 설명하는데 아무런 도움을 주지 못함.따라서, 주어진 규칙이 진짜로 의미가 있는지 알아보기 위해서는 𝑃𝐵𝐴/𝑃(𝐵)를 계산해야함
- `DS_PDF08_ML3:p042:L005` 예)“삼겹살을 사는 사람은 상추도 구입한다” 라는 규칙의 향상도 :  !상추삼겹살!상추=!"!#="#.
- `DS_PDF08_ML3:p042:L006` 향상도 = 1 : A와 B는 아무런 관계가 없음.향상도 > 1 : A가 B의 발생 확률을 A를 고려하지 않을 경우보다 증가시킨다는 의미. 즉, A가 B의 발생을 예측하는데 유의미함.향상도 < 1 : A가 B의 발생 확률을 A를 고려하지 않을 경우보다 감소시킨다는 의미. 즉, A가 B의 발생 감소를 예측하는데 유의미함. 일종의 음의 상관관계
