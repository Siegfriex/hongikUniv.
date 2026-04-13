# MiriArt Q(x) 연구계획서 v7

**디자인은 학습이다: 일반 시각 판단 구조 규명을 위한 스트레스 도메인 기반 초기 모델링 연구**

*Design as Learning: Modeling the Universal Structure of Visual Judgment via a High-Stakes Domain*

**제출 대상**: 홍익대학교 산업·데이터공학과 신훈식 교수 연구실
**제출자**: 류지환 (홍익대학교 데이터사이언스 전공)
**작성일**: 2026. 04. 06.
**버전**: v7 — 상위 철학 명제 통합 · 스트레스 도메인 프레이밍 완성 · 2024–2026 선행연구 웹그라운딩 교차검증

> **버전 이력**: v1–v3 탐색 → v4 기반 구조 확립 → v5 통계 강화 · 도메인 확장 → v6 이론축 재정립 · 직접인용 통합 → v7 상위 철학 명제 통합 · 스트레스 도메인 프레이밍 완성

---

## Abstract

본 연구는 하나의 철학적 명제에서 출발한다.

> **디자이너는 수용자 효용을 최대화하는 방향으로 반복 학습하는 행위자이며, 디자인 결과물은 특정 도메인 내에서 수용자 반응을 유도하도록 조정된 함수적 산물이다.**

이 명제가 성립하려면, 개별 도메인 안에서는 시각적 구조와 수용자 반응 사이에 **추정 가능한 함수 관계**가 존재해야 한다. 그러나 일반 시각 전반에서는 결과 레이블이 연속적이고 암묵적이며, 평가 규칙 또한 약하고 맥락 의존적이어서, 시각 판단이 구조를 가진 현상인지 아니면 개인 취향의 집합인지 실증적으로 분리하기 어렵다.

따라서 본 연구는 **평가 기준이 강하게 작동하고 결과 레이블이 비교적 명확한 미대입시(美大入試)를 스트레스 도메인(stress-test domain)으로 설정**한다. 본 연구의 직접적 목적은 이 도메인에서 시각 판단이 순수한 취향 잡음이 아니라 평가자 간 합의 가능한 구조를 가지는지, 그리고 그 구조가 **보편 코어(*Q_core*)와 도메인 조건부 성분(*Q_domain*)으로 분해 가능한지**를 검증하는 데 있다. 미대입시는 연구의 최종 목적이 아니라 **검증의 출발 도메인**이며, 이 도메인에서 확인된 구조는 이후 일반 시각 선호, UI/UX, 패션, 인테리어 등 더 넓은 시각 평가 문제로 확장 가능한 기초 모델로 기능한다.

이를 위해 본 연구는 합의도, 예측 가능성, 분해 가능성, 일반화 가능성을 단계적으로 검증한다. **핵심 검증 지표**는 ICC ≥ 0.60 (보편 코어 합의도), F1 ≥ 0.65 (도메인 조건부 예측), Pearson *r* ≥ 0.60 (개인화 잔차, *k* ≤ 20 shots), SRCC > 0.70 (cross-domain 일반화)로 설정한다.

---

## 1. 출발 명제: 디자인은 학습이다

### 1-1. 상위 철학 가정

본 연구의 이론적 출발점은 다음 세 개의 연결된 가정이다.

**가정 1 — 디자이너는 학습 행위자다.**
디자이너는 각 도메인에서 주어지는 평가 규칙, 피드백, 수용자 반응을 반복적으로 학습하며, 결과물을 점진적으로 조정해 나간다. 이는 Dreyfus(2004)의 기술 습득 5단계 모형이나 Fitts & Posner(1967)의 인간 수행 학습 곡선과 유사한 구조를 가진다. Lu, Marghetis & Yang(2025)은 동기·피로·노력의 다중 시간 스케일을 통합하여 인간 학습이 멱법칙(power-law)과 S-곡선을 따름을 수학적으로 도출했으며[^1], 이는 디자이너의 도메인 내 최적화 과정과 일맥상통한다.

**가정 2 — 디자인 결과물은 함수적 산물이다.**
디자인 결과물은 임의의 산출물이 아니라, 특정 수용자 집단의 효용 반응을 상대적으로 높이는 방향으로 조정된 시각 함수로 볼 수 있다. 이 관점에서 디자인 작품 *x*는 수용자 *u*의 반응 *Y(u,x)*를 최대화하도록 최적화된 함수 *f_d(x)*의 산물이다. Koyama(2017)는 미적 선호를 최적화 목적함수로 사용하는 계산 설계(computational design) 프레임워크를 제시하여 이 관점의 기술적 실현 가능성을 보였다[^2].

**가정 3 — 도메인별 최적해는 다르다.**
그러나 이 최적화는 도메인 *d*에 따라 다른 방향으로 작동한다. 미대입시의 학과 A(동양화)와 학과 B(시각디자인)가 서로 다른 평가 기준을 갖듯, 동일한 시각 구조라도 도메인 맥락에 따라 판단 가중치가 달라진다. 이것이 *Q_domain(x,d)*를 독립적으로 추정해야 하는 이유다.

이 세 가정을 종합하면 다음 핵심 연구 명제가 된다.

> **만약 디자인이 수용자 효용 최대화를 향한 학습 과정이라면, 그 결과물 안에는 도메인을 가로질러 공통적으로 작동하는 시각 구조(*Q_core*)와 도메인별로 다르게 작동하는 구조(*Q_domain*)가 함께 존재해야 한다. 이 두 구조를 데이터로 분리하고 검증하는 것이 본 연구의 핵심이다.**

### 1-2. 왜 미대입시인가 — 스트레스 도메인 논리

일반 시각 판단 구조를 검증하기 위해서는 다음 조건이 필요하다.

| 필요 조건 | 일반 시각 영역 | 미대입시 도메인 |
|---------|-------------|--------------|
| 명확한 결과 레이블 | 없음 (선호는 연속적·암묵적) | 있음 (합격/불합격, 실기 점수) |
| 강한 평가 규칙 존재 | 약함 (맥락 의존) | 있음 (학과별 채점 기준, 전문가 집단) |
| 도메인 경계 명확성 | 불분명 | 있음 (학과별 구분) |
| 관측 가능한 피드백 | 없음 | 있음 (합격·불합격 반복 피드백) |

미대입시는 이 네 조건을 동시에 충족하는 **고압 검증 환경**이다. 이 도메인에서 *Q_core*와 *Q_domain*의 분리 가능성을 확인한 뒤, 그 구조를 더 일반적인 시각 판단 문제로 확장하는 것이 본 연구의 로드맵이다.

**중요한 정의**: 미대입시는 본 연구의 **도메인 출발점**이지, 최종 목적이 아니다. 본 연구는 미대입시를 잘 예측하는 시스템을 만드는 것이 아니라, 그 도메인 안에서 시각 판단의 보편 구조와 조건부 분기가 데이터로 확인되는지를 검증하는 것이다.

### 1-3. 문제정의 — 무엇을 검증하려는가

본 연구의 문제는 "디자인은 학습이다"라는 상위 명제 자체를 철학적으로 선언하는 데 있지 않다. 보다 직접적으로는, **시각 판단이 실제 도메인 안에서 구조를 가진 판단 체계인지, 아니면 설명 불가능한 개인 취향의 합인지**를 실증적으로 가려내는 데 있다.

이 문제는 일반 시각 전체를 대상으로 할 때 곧바로 다루기 어렵다. 일반 시각 선호 영역에서는 결과 레이블이 약하고, 평가 기준이 불분명하며, 무엇이 성공적 반응인지에 대한 사회적 합의도 낮기 때문이다. 반면 미대입시는 합격/불합격, 실기 점수, 전문가 평가 루브릭, 반복 피드백이라는 관측 가능한 신호를 제공한다. 따라서 이 도메인은 보편 구조의 존재 여부를 처음 시험해 보기 위한 **고신뢰 검증장치**로 기능한다.

이 관점에서 본 연구의 문제정의는 다음과 같이 정리된다.

> **미대입시라는 스트레스 도메인에서 시각 판단은 통계적으로 수렴하는 합의 구조를 가지는가? 그리고 그 구조는 보편적으로 작동하는 시각 코어(*Q_core*)와 도메인 맥락에 따라 달라지는 조건부 성분(*Q_domain*)으로 분해 가능한가?**

이 정의는 본 연구가 단순히 "합격 예측 모델"을 만드는 작업이 아님을 분명히 한다. 예측은 연구의 일부 산출물이지만 최종 목적은 아니다. 본 연구의 목적은 예측 성능, 평가자 간 합의도, 설명 가능성, 교차 도메인 일반화 성능을 함께 사용해 **시각 판단 구조의 존재와 분해 가능성 자체를 검증**하는 데 있다.

또한 이 문제정의는 데이터사이언스 절차와 직접 연결된다. 기술적 분석 단계에서는 미대입시 평가 데이터의 분포와 합의 수준을 확인하고, 진단적 분석 단계에서는 어떤 시각 피처가 판단에 기여하는지 추적하며, 예측적 분석 단계에서는 *Q_d(x)*의 학습 가능성을 검증하고, 처방적 분석 단계에서는 확인된 구조를 학습 피드백과 도메인 확장 전략으로 전환한다. 즉, 본 연구의 흐름은 "문제 정의 -> 데이터 확보 -> 모델 검증 -> 결과 적용"의 절차를 따르되, 그 중심 질문을 **시각 판단 구조의 검증**에 둔다.

---

## 2. 이론적 배경

### 2-1. 공유 미감 (Shared Taste)

Vessel, Maurer, Denker & Starr(2018)는 얼굴·풍경·건축·회화 등 복수 도메인에서 개인 간 미적 합의 비율을 비교했다. 자연 자극(얼굴, 풍경)은 shared taste 비중이 높은 반면, 문화적 인공물(건축, 회화)은 개인차가 강했으며, 이를 통해 도메인에 따라 공유 미감의 비중이 체계적으로 달라진다는 결론을 얻었다[^3].

> *"The degree of shared versus individual aesthetic preference differs systematically across visual domains, even for photographic images of real-world content."*
> — Vessel, E.A., Maurer, N., Denker, A.H. & Starr, G.G. (2018). *Cognition*, 179, 121–131.

이 발견은 *Q_core(x)*의 경험적 토대가 된다. 도메인 조건 이전에도 이미지 수준에서 공유 판단 구조가 존재할 수 있다는 근거다.

최근 Lee et al.(2025)은 10개국 4,835명 참가자로부터 401,403건의 선호 판단을 수집한 대규모 교차문화 연구에서, 형태/곡률/대칭 선호에서는 보편적 패턴이, 색채와 선율에서는 문화적 분산이 나타남을 보고하여 *Q_core*와 *Q_domain*의 분리 가능성에 대한 대규모 실증 근거를 제공했다[^4].

### 2-2. 전형성 (Taste Typicality)

Chen et al.(2022)은 시각·청각 두 모달리티에서 개인 취향 차이가 임의적이지 않고 taste typicality(개인 취향과 평균 취향의 일치도)로 구조화된다는 것을 보였다. 이 typicality가 미적 경험의 설명 가능한 분산 대부분을 포착하는 기초 차원이다[^5].

> *"Taste typicality captured most of the explainable variance in people's impressions, showing that it is the primary dimension along which aesthetic tastes systematically vary."*
> — Chen, Y.-C. et al. (2022). "'Taste typicality' is a foundational and multi-modal dimension of ordinary aesthetic experience." *Current Biology*, 32(8), 1837–1842.

이는 개인 잔차 *r_personal(u,x)*이 완전한 노이즈가 아니라 typicality 축으로 부분 구조화된다는 근거다.

### 2-3. 도메인 조건성 (Domain Conditionality)

Roth, Kawabata & Leder(2026)는 일본·유럽 참가자 간 예술적 자극에 대한 shared taste 비율이 유의미하게 달랐으며, 이 차이가 개인의 집단주의 성향을 넘어서는 문화적 효과였다고 보고했다[^6].

> *"Congruence in personal taste meaningfully differed between cultures, showing higher shared taste in Japanese participants for artistic stimuli. These effects reached beyond comparisons by individual collectivistic tendencies."*
> — Roth, L.H.O., Kawabata, H. & Leder, H. (2026). *Empirical Studies of the Arts*. DOI: 10.1177/02762374251334962.

Mikuni et al.(2024)은 54개 서양 미술작품에 대해 일본어·독일어 화자의 beauty judgment를 ML(extreme randomized trees)로 분석했다. SHAP 분석 결과 복잡도 선호에서 두 문화권이 유의하게 갈렸으며(일본: 단순함, 독일: 복잡함), 이는 도메인 및 문화 맥락에 따라 시각 속성의 기여 구조가 달라진다는 직접 증거다[^7].

> *"Our findings illuminate the nuanced role that cultural context plays in shaping aesthetic judgments and demonstrate the utility of machine learning in unravelling these complex dynamics."*
> — Mikuni, J. et al. (2024). *Scientific Reports*, 14, 15948.

Van Geert, Ding & Wagemans(2025)은 중국-네덜란드 교차문화 비교에서 정돈된 구성에 대한 선호조차 문화적으로 조절됨을 보여, 저수준 구성 선호에서도 도메인 조건성이 존재함을 확인했다[^8].

### 2-4. 습속 (Habitus)

Bourdieu(1984)의 habitus 개념에 따르면 취향은 순수한 심리적 편차가 아니라 교육·계급·문화적 노출의 구조를 내면화한 결과다[^9]. 본 연구에서 Tier 3 변수(education_type, prep_duration, studio_type, cultural_exposure)는 단순 공변량이 아니라 *r_personal(u,x)*의 구조적 예측 변수로 기능한다.

### 2-5. 미감의 신경 기반 (Neural Basis of Aesthetic Value)

Iigaya et al.(2021; 2023)은 미적 가치가 저수준(V1/V2) 및 고수준(V4/두정엽/전두엽) 시각 특징의 가중 통합을 통해 계층적으로 계산됨을 fMRI로 확인했다. 이 계산 구조가 객체 인식에 훈련된 심층 CNN과 유사하다는 발견은 *Q(x)* 분해의 신경과학적 정당성을 제공한다[^10].

> *"Aesthetic value is computed via a hierarchical weighted integration over low- and high-level visual features."*
> — Iigaya, K. et al. (2021). *Nature Human Behaviour*, 5, 1113–1123; (2023). *Nature Communications*, 14, 127.

### 2-6. 계산미학의 시대 구분과 현재 위치

| 단계 | 시기 | 핵심 특징 | 대표 연구 |
|-----|-----|---------|---------|
| **1.0** 계산미학 | ~2012 | hand-crafted feature, SVM | Datta et al. (2006)[^11] |
| **2.0** 딥러닝 미학 | 2012–2021 | CNN/ViT, 평균 점수 분포 예측 | NIMA (Talebi & Milanfar, 2018)[^12], MUSIQ (Ke et al., 2021)[^13] |
| **3.0** Foundation Aesthetics | 2021–2023 | CLIP 기반 표현, zero-shot transfer | VILA (Ke et al., 2023)[^14], CLIP-IAA (Xu, Xu, Yang et al., 2023)[^15] |
| **4.0** Conditional / Personalized | 2023–현재 | task vector, meta-learning, MLLM, cross-domain | Yun & Choo (2024)[^16], Q-Align (Wu et al., 2024)[^17], AesExpert (Huang et al., 2024)[^18] |

본 연구는 4.0 단계의 문제의식 위에 서 있다. 기존 4.0 연구들이 개인화 성능 향상에 집중한다면, 본 연구는 **보편 코어와 조건부 분기의 경계 자체를 이론–실증으로 확인**하는 데 목적이 있다.

성숙 포인트는 "미를 처음 계산할 수 있게 됐다"가 아니라, **"보편 코어와 조건부 분기를 동시에 실험할 수 있게 됐다"**는 데 있다. CLIP 기반 표현은 저데이터 상황에서도 superior aesthetic feature를 제공하고(Xu et al., 2023), task vector는 unseen domain 일반화를 가능하게 했다(Yun & Choo, 2024). 최근 Wu et al.(2025)의 체계적 문헌 리뷰(184편 분석)는 현 시점의 IAA 최고 정확도가 91.5%에 도달했으나, 설명가능성·도메인 적응·데이터셋 품질이 여전히 미해결 과제임을 확인했다[^19].

> *"Our extensive experiments demonstrate the effectiveness of our approach in generalizing to previously unseen domains — a challenge previous approaches have struggled to achieve."*
> — Yun, J. & Choo, J. (2024). "Scaling Up Personalized Image Aesthetic Assessment via Task Vector Customization." *ECCV 2024*.

---

## 3. 이론 모형: Q(x, d, u, a)

### 3-1. 핵심 분해식

$$Y_{u,x,d,a} = Q_{core}(x) + Q_{domain}(x,d) + r_{personal}(u,x) + Q_{affect}(x,a) + \varepsilon$$

| 항 | 의미 | 이론 근거 |
|----|------|---------|
| *Q_core(x)* | 이미지 *x*의 보편 미감 기저 — 도메인·개인 조건 이전의 공유 판단 구조 | Vessel et al. (2018)[^3], Chen et al. (2022)[^5], Iigaya et al. (2021)[^10] |
| *Q_domain(x,d)* | 도메인 *d* 맥락에서 *x*의 조건부 판단 재가중 | Mikuni et al. (2024)[^7], Roth et al. (2026)[^6], Lee et al. (2025)[^4] |
| *r_personal(u,x)* | 사용자 *u*의 개인 잔차 — typicality 및 habitus 구조 반영 | Chen et al. (2022)[^5], Bourdieu (1984)[^9], Yun & Choo (2024)[^16] |
| *Q_affect(x,a)* | 정서 상태 *a*에 따른 판단 변형 | Brielmann & Pelli (2017)[^20], Chen & Shao (2024)[^21] |

### 3-2. 상위 명제와의 연결

"디자이너는 학습 행위자" 명제와 이 수식의 관계는 다음과 같다.

- *Q_core(x)* → 디자이너들이 도메인을 가로질러 공통적으로 학습하게 되는 보편 시각 원리.
- *Q_domain(x,d)* → 각 도메인의 평가 규칙이 만들어내는 도메인 특화 최적화 방향.
- *r_personal(u,x)* → 개인 학습 이력·경험·habitus가 만들어내는 취향 편차.
- *Q_affect(x,a)* → 판단 맥락의 정서 상태에 따른 변동.

### 3-3. 수식과 AI의 관계

**수식은 의미론(semantics)이다**: 무엇을 추정할지, 어떤 관계를 가정하는지를 정의한다.

**AI는 함수 근사기(approximator)다**: 같은 *Q_core(x)*라도 Stage 0에서는 Logistic Regression으로, Stage 3에서는 CNN/CLIP fusion으로 근사 방식을 발전시킨다. 최근 Q-Align(Wu et al., 2024)은 텍스트 정의 등급(text-defined levels)으로 인간 평가자의 이산 판단을 모사하여 IQA·IAA·VQA를 단일 모델로 통합했고[^17], AesExpert(Huang et al., 2024)는 다중 세분도(coarse → fine) 미학 인식을 MLLM으로 구현하여 GPT-4V를 초과했다[^18].

**설명도구(SHAP, Grad-CAM, CJS)는 해석 보조층이다**: 완전한 모델 투명성을 보증하지 않지만, 어떤 시각 특성이 어느 맥락에서 기여했는지를 사후적으로 추적한다.

이 구분이 없으면 연구는 "딥러닝 모델 하나 만든 것"으로 읽힌다.

### 3-4. 핵심 가정

1. *E[r_personal(u,x)] = 0* — 개인 잔차는 *Q_core*에 대해 평균적으로 편향되지 않는다.
2. *Cov(Q_core(x), Q_domain(x,d)) ≈ 0* — 보편 코어와 도메인 조건부는 근사적으로 직교한다.
3. *Q_affect(x,a)*는 *Q_core*와 *Q_domain*에 곱셈적(multiplicative)이 아닌 가산적(additive)으로 작동한다.
4. 유한 평가자(*n* ≥ 5)에서 *Q_core*가 ICC ≥ 0.60 수준의 수렴 속도를 보인다.

---

## 4. 연구 질문 및 가설 체계

### 4-1. 기초 연구 질문 (Phase 1–3)

**RQ1 — 시각 판단의 합의 구조 존재 여부**
> "동일 도메인 조건(*D = d*)에서 복수의 독립 평가자 간 평가는 통계적으로 수렴하는 공통 구조를 가지는가?"

- **H₀**: ICC < 0.6 — *Q_core(x)*가 존재하지 않으며, 시각 미술 평가는 순수 개인 취향에 지배된다.
- **H₁**: ICC ≥ 0.6이며 3인 이상 평가자의 합의 점수가 유의미한 공통 구조를 가진다.
- 검증 지표: ICC(two-way mixed, absolute agreement), Krippendorff's α

**RQ2 — 도메인 내부 예측 구조의 학습 가능성**
> "도메인을 고정했을 때 피처 벡터 *x*에서 평가 결과 *Y*를 예측하는 *Q_d(x)*를 지도학습으로 안정적으로 근사할 수 있는가?"

- **H₀**: 분류 F1 개선폭 < 10%p (랜덤 베이스라인 대비)
- **H₁**: F1 ≥ 0.65, SHAP Top 3 피처가 도메인 전문가에게 해석 가능

**RQ3 — 보편 코어와 도메인 분기의 분해 가능성**
> "서로 다른 도메인 *d₁, d₂*에서 추정한 판단 구조는 공통 코어(*Q_core*)와 도메인 조건부 분기(*Q_domain*)로 분해될 수 있는가?"

- **H₁**: Multi-domain SHAP Top 5 중 ≥ 3 공통 피처 (보편 코어 존재)
- **H₀**: 공통 피처 < 2 → "도메인 특이 *Q_D*가 지배" 명제로 전환

### 4-2. 확장 연구 질문 (Phase 4–5)

**RQ4 — r_personal의 few-shot 학습 가능성**
> "*r_personal(u,x)*를 *k* ≤ 20건의 개인 라벨로 학습할 수 있는가?"

- 검증: Pearson *r* ≥ 0.60 달성
- 방법: task vector(Yun & Choo, 2024)[^16] 또는 VAE + meta-learning(Li et al., 2025)[^22]

**RQ5 — Q_affect의 독립적 기여**
> "정서 상태 *a*가 *Q_core*와 *Q_domain*을 통제한 후에도 추가적 설명력을 제공하는가?"

- 검증: *Q_affect* 추가 시 *ΔR²* > 0.05, *p* < .01
- 근거: Brielmann & Pelli(2017)의 미적 쾌감 인지 요건[^20], Chen & Shao(2024)의 감정 인지 분기가 IAA 성능을 향상시킨 실증[^21]

### 4-3. 가정 간 의존 구조 (DAG)

```
[가정 A0] Y는 수용자 효용의 함수다
  │
  ▼
[가정 A1] 동일 D에서 Y는 평가자 간 합의를 가진다
  │ 검증: ICC ≥ 0.6 (A1 게이트) ← 연구 전체의 선행 관문
  │ 실패 시: 도메인 더 축소, 루브릭 재설계, 또는 "취향 클러스터 분류" 대안 명제
  ▼
[가정 A2] Q_core(x)는 추정 가능한 분포를 가진다
  │ 검증: Q_core의 분산 > 노이즈 분산
  ▼
[가정 A3] 지도학습으로 Q_d(x)를 근사할 수 있다
  │ 검증: F1 ≥ 0.65 (분류), SRCC ≥ 0.50 (회귀)
  ▼
[확장 E1] D를 바꾸어 Q_D(x)들의 공통 코어를 분해할 수 있다
  │ 검증: Multi-domain SHAP Top 5 중 ≥ 3 공통 피처
  ▼
[확장 E2] r_personal(u,x)를 few-shot으로 학습할 수 있다
  │ 검증: k=20건으로 Pearson r ≥ 0.60
  ▼
[확장 E3] Q_affect(x|a)를 조건부로 정의하여 정동 기반 생성 가능
  │ 검증: 생성 작품의 목표 affect 유발률 ≥ 70%
```

**A1이 실패(ICC < 0.6)하면 A2 이후 전체가 무효화된다.** 따라서 **A1 검증(Phase 2)은 연구 전체의 선행 게이트**다.

---

## 5. 변수 체계 (Tier 구조)

### Tier 1: 이미지 고유 피처 (→ Q_core, Q_domain)

| 변수 | 조작적 정의 | 측정 방법 |
|------|----------|---------|
| 구도 (composition) | 시선 흐름, 비례, 무게 중심 | 전문가 루브릭 + CNN saliency |
| 색채 (color) | 색상 조화, 명도 대비, 채도 범위 | 전문가 루브릭 + HSV 히스토그램 |
| 형태 (form) | 선의 정확도, 비례, 공간감 | 전문가 루브릭 + edge detection |
| 밀도 (density) | 단위 면적당 시각 정보량 | 전문가 루브릭 + entropy 측정 |
| 완성도 (finish) | 의도된 마감 수준 달성 | 전문가 루브릭 주관 |

### Tier 2: 이미지 임베딩 (→ Q_core deep feature)

| 소스 | 차원 | 용도 |
|------|-----|------|
| CLIP ViT-L/14 | 768 | Foundation aesthetic feature[^15] |
| DINOv2 | 768 | Self-supervised structural feature |
| CNN (ResNet-50) 중간층 | 2048 | Texture/low-level feature |

### Tier 3: 사용자 메타데이터 (→ r_personal)

| 변수 | 유형 | 이론 근거 |
|------|-----|---------|
| education_type | 범주형 | Bourdieu habitus[^9] |
| prep_duration | 연속형 | 학습 기간 효과 |
| studio_type | 범주형 | 교육 환경 조건 |
| cultural_exposure | 순서형 | 문화 자본 proxy |
| taste_typicality | 연속형 | Chen et al. (2022)[^5] |

### Tier 4: 정동 변수 (→ Q_affect)

| 변수 | 측정 | 근거 |
|------|-----|------|
| valence | SAM 척도 | Russell (1980) |
| arousal | SAM 척도 | Russell (1980) |
| aesthetic_pleasure | 7점 리커트 | Brielmann & Pelli (2017)[^20] |

---

## 6. 연구 설계 및 방법론

### 6-0. 문제정의와 성공 기준의 운영화

앞선 문제정의를 연구 설계 수준으로 운영화하면, 본 연구는 다음 네 가지 의사결정 질문으로 분해된다.

| 유형 | 연구 내 질문 | 산출물 |
|------|-------------|-------|
| **기술적 분석** | 미대입시 평가 데이터에는 어떤 분포와 합의 구조가 나타나는가? | 합격/불합격 분포, ICC, 기초 EDA |
| **진단적 분석** | 어떤 시각 피처와 도메인 조건이 평가 차이를 설명하는가? | SHAP, 루브릭-피처 대응, 도메인 비교 |
| **예측적 분석** | 작품 *x*에서 평가 결과 *Y*를 얼마나 안정적으로 근사할 수 있는가? | F1, SRCC, 베이스라인 대비 향상폭 |
| **처방적 분석** | 확인된 구조를 학습 피드백과 확장 도메인 전략으로 어떻게 전환할 수 있는가? | 개인화 피드백 규칙, 확장 가능성 판단 |

따라서 본 연구의 성공은 단일 모델 정확도로만 판단되지 않는다. 최소 성공 기준은 다음 네 축이 동시에 충족될 때 성립한다: (1) 평가자 간 합의가 ICC 기준을 넘는가, (2) 도메인 내부에서 *Q_d(x)*가 기준선 대비 유의하게 예측 가능한가, (3) 설명도구를 통해 공통 코어와 도메인 분기의 해석이 가능한가, (4) 일부 구조가 다른 도메인으로 확장 가능한 신호를 보이는가. 이 네 기준은 이후 Phase와 Stage 설계의 관문으로 사용된다.

### 6-1. 데이터 수집

**목표 표본**: *N* = 600 작품 (합격 300 + 불합격 300), 5개 이상 학과, 3개 이상 연도.

| 데이터 소스 | 수집 방법 | 예상 규모 |
|-----------|---------|---------|
| 학원 MOU 파트너 | 실합격·불합격 작품 제공 | 400+ |
| MiriArt 플랫폼 유저 | 플랫폼 내 업로드 작품 | 200+ |
| 전문가 평가 데이터 | 3인 이상 pairwise + 루브릭 | 전체 작품 대상 |

**선발 편향 관리**: MOU 데이터는 특정 학원 편향 가능성이 있으므로, 학원·지역·연도별 층화 추출(stratified sampling)을 적용하고, 방법론 절에 선발 편향 프로파일을 별도 기술한다.

### 6-2. Phase 구조

| Phase | 기간 | 목표 | 관문 |
|-------|-----|------|-----|
| **Phase 1** (M0–3) | 데이터 수집 + 전처리 | *N* ≥ 300, 3개 학과 | 데이터 충분성 |
| **Phase 2** (M3–6) | A1 게이트 검증 | ICC ≥ 0.60 | **연구 진행/중단 결정** |
| **Phase 3** (M6–12) | *Q_d(x)* 모델링 | F1 ≥ 0.65 | 학습 가능성 |
| **Phase 4** (M12–18) | Cross-domain + 개인화 | SRCC > 0.70, Pearson *r* ≥ 0.60 | 분리·일반화 |
| **Phase 5** (M18–24) | 정동 + 확장 도메인 | *ΔR²* > 0.05 | 확장 타당성 |

### 6-3. 모델링 전략 (Stage별 누적)

| Stage | 입력 | 모델 | 목표 |
|-------|-----|------|-----|
| **Stage 0** | Tier 1 (구조화 점수) | Logistic Regression, Random Forest | 베이스라인 F1 |
| **Stage 1** | Tier 1 + Tier 2 (CNN 임베딩) | Gradient Boosting + CNN feature | F1 향상, 임베딩 기여 측정 |
| **Stage 2** | Tier 1–2 + multi-domain | Domain-adaptive model, SHAP cross-domain | 공통 코어 vs 도메인 분기 분리 |
| **Stage 3** | Tier 1–4 전체 | CLIP/DINOv2 fine-tuning, AesMamba[^23] | 최종 *Q(x,d,u,a)* 통합 모델 |

**Stage E1** (개인화): Task vector customization(Yun & Choo, 2024)[^16] 또는 GNN + collaborative filtering(Wang et al., 2024)[^24]
**Stage E2** (정동): Emotion-aware multi-branch(Chen & Shao, 2024)[^21] 또는 EAHI-NET(Li et al., 2024)[^25]

### 6-4. 설명도구 프로토콜

| 도구 | 적용 대상 | 해석 목표 |
|------|---------|---------|
| SHAP (TreeExplainer / DeepExplainer) | Stage 0–2 구조화 모델 | Tier 1 피처 기여도, cross-domain 공통성 |
| Grad-CAM | Stage 3 CNN/ViT | 시각적 주목 영역, *Q_core* vs *Q_domain* 영역 차이 |
| CJS (Cross-domain Jensen–Shannon) | Stage 2 다중 도메인 | 도메인 간 피처 분포 발산 정도 |
| LIME | 개별 예측 해석 | 사례 수준 설명 |

---

## 7. 선행연구 통합 맵

### 7-1. 기존 인용 문헌 — 교차검증 결과

모든 기존 인용 문헌은 웹 기반 1:1 교차검증을 거쳤다. 아래 표는 검증 결과를 반영한 최종 정확 인용이다.

| 문헌 | 검증 상태 | Tier | Q(x) 연결 |
|------|---------|------|----------|
| Vessel, Maurer, Denker & Starr (2018). "Stronger shared taste for natural aesthetic domains than for artifacts of human culture." *Cognition*, 179, 121–131. | CORRECTED (제목 수정) | **S** | *Q_core* 존재 근거 |
| Chen et al. (2022). "'Taste typicality' is a foundational and multi-modal dimension of ordinary aesthetic experience." *Current Biology*, 32(8), 1837–1842. | CORRECTED (전체 제목 보완) | **S** | *Q_core* + typicality 이론 |
| Roth, Kawabata & Leder (2026). *Empirical Studies of the Arts*. DOI: 10.1177/02762374251334962. | CORRECTED (연도 2025→2026) | **A** | *Q_domain* 문화 맥락 |
| Mikuni et al. (2024). *Scientific Reports*, 14, 15948. | VERIFIED | **A** | *Q_domain* ML 분석 선례 |
| Xu, Xu, Yang, Wang, Huang & Li (2023). "CLIP Brings Better Features to Visual Aesthetics Learners." arXiv:2307.15640. | CORRECTED (저자 Wang→Xu) | **A** | Tier 4 CLIP feature |
| Yun & Choo (2024). "Scaling Up Personalized Image Aesthetic Assessment via Task Vector Customization." *ECCV 2024*. | VERIFIED | **A** | Stage E1 개인화 설계 |
| Bourdieu (1984). *Distinction*. Harvard University Press. | VERIFIED | **S** | Tier 3, *r_personal* 이론 |
| Lu, Marghetis & Yang (2025). *npj Complexity*, 2, 15. | VERIFIED | **B** | 학습 곡선 수학적 근거 |
| Brielmann & Pelli (2017). "Beauty Requires Thought." *Current Biology*, 27(10), 1506–1513. | VERIFIED | **A** | *Q_affect* 인지 요건 |
| Talebi & Milanfar (2018). "NIMA." *IEEE Trans. Image Processing*, 27(8), 3998–4011. | VERIFIED | **S** | IAA 2.0 기준선 |
| Ke et al. (2021). "MUSIQ." *ICCV 2021*. | VERIFIED | **S** | IAA 2.0 multi-scale |
| Ke et al. (2023). "VILA." *CVPR 2023*. | VERIFIED | **S** | IAA 3.0 vision-language |
| Dreyfus (2004). *Bulletin of Science, Technology & Society*, 24(3), 177–181. | VERIFIED | **A** | 기술 습득 5단계 |
| Fitts & Posner (1967). *Human Performance*. Brooks/Cole. | VERIFIED | **B** | 일반 학습 이론 |
| Koyama (2017). PhD thesis. The University of Tokyo. | CORRECTED (연도 2016→2017) | **B** | 계산 설계 선호 |
| Datta et al. (2006). *ECCV 2006*, pp. 288–301. | VERIFIED | **S** | 계산미학 1.0 기원 |

### 7-2. 2024–2026 신규 선행연구 — 웹그라운딩 교차검증 결과

아래 문헌들은 2024–2026년 발표된 최신 연구로, 웹 검색 및 원문 교차검증을 거쳐 Q(x) 모형의 각 구성요소별로 분류·등급화하였다.

#### S-Tier (필수 인용)

| 문헌 | 학회/저널 | Q(x) 연결 |
|------|---------|----------|
| Wu et al. (2025). "Deep Learning Based Image Aesthetic Quality Assessment: A Review." *ACM Computing Surveys*. | 서베이 | *Q_core* 방법론 전경 |
| Wu et al. (2024). "Q-Align: Teaching LMMs for Visual Scoring via Discrete Text-Defined Levels." *ICML 2024*. | ICML | *Q_core* LMM 통합 |
| Huang et al. (2024). "AesExpert: Towards Multi-modality Foundation Model for Image Aesthetics Perception." *ACM MM 2024*. | ACM MM | *Q_core* MLLM 기반 |
| Lee et al. (2025). "Visual and Auditory Aesthetic Preferences Across Cultures." arXiv:2502.14439 (Max Planck). | Max Planck | *Q_core* vs *Q_domain* 대규모 분리 |
| Iigaya et al. (2021; 2023). *Nature Human Behaviour* 5; *Nature Communications* 14. | Nature | Q(x) 전체 신경 기반 |

#### A-Tier (강력 지지)

| 문헌 | 학회/저널 | Q(x) 연결 |
|------|---------|----------|
| Gao et al. (2024). "AesMamba: Universal Image Aesthetic Assessment with State Space Models." *ACM MM 2024* (Oral). | ACM MM | *Q_core* 아키텍처 |
| Liu et al. (2025). "Advancing Comprehensive Aesthetic Insight with Multi-Scale Text-Guided Self-Supervised Learning." *AAAI 2025*. | AAAI | *Q_core* 자기지도학습 |
| Li et al. (2025). "Multimodal LLMs Can Reason about Aesthetics in Zero-Shot." *ACM MM 2025*. | ACM MM | 방법론 (분해적 추론) |
| Li et al. (2025). "Personalized Design Aesthetic Preference Modeling: A VAE and Meta-Learning Approach." *Scientific Reports*. | Sci. Rep. | *r_personal* meta-learning |
| Wang et al. (2024). "Personalized IAA Based on Graph Neural Network and Collaborative Filtering." *Knowledge-Based Systems*. | KBS | *r_personal* GNN |
| Chen & Shao (2024). "Image Aesthetics Assessment With Emotion-Aware Multibranch Network." *IEEE Trans. Instrumentation and Measurement*, 73. | IEEE TIM | *Q_affect* 감정 분기 |
| Li et al. (2024). "Emotion-aware Hierarchical Interaction Network for Multimodal Image Aesthetics Assessment." *Pattern Recognition*. | PR | *Q_affect* 다층 상호작용 |
| Sardenberg et al. (2025). "A Computational Framework for Aesthetic Preferences in Architecture." *SAGE*. | SAGE | *Q_domain* 건축 도메인 |
| Hertzmann (2025). "Generative Models for the Psychology of Art and Aesthetics." *Empirical Studies of the Arts*. | ESOA | 이론 프레임워크 |
| Wang et al. (2026). "An AI-Generated Art Evaluation Model Integrating Computational Aesthetics and Cognitive Psychology." *Scientific Reports*. | Sci. Rep. | *Q_core* + 인지심리 통합 |

#### B-Tier (보조 지지)

| 문헌 | 학회/저널 | Q(x) 연결 |
|------|---------|----------|
| Yang et al. (2026). "Fine-grained Image Aesthetic Assessment." *CVPR 2026*. | CVPR | *Q_core* 세분도 |
| Van Geert, Ding & Wagemans (2025). "Cross-Cultural Comparison of Aesthetic Preferences." *Empirical Studies of the Arts*. | ESOA | *Q_domain* 저수준 문화 조절 |
| Wu et al. (2025). "DesignPref: Capturing Personal Preferences in Visual Design Generation." arXiv:2511.20513. | arXiv | *r_personal* 디자이너 개인차 |
| Zhang et al. (2025). "UniQA: Unified Vision-Language Pre-training for Image Quality and Aesthetic Assessment." arXiv:2406.01069. | arXiv | 방법론 (품질+미학 통합) |
| Zhou et al. (2024). "UNIAA: A Unified Multi-modal Image Aesthetic Assessment Baseline and Benchmark." arXiv:2404.09619. | arXiv | *Q_core* 벤치마크 |

### 7-3. 본 연구의 차별점

| 기존 연구 축 | 본 연구 |
|-----------|--------|
| IAA: 평균 점수 예측 성능 향상 | 보편 코어와 조건부 분기의 경계 실증 |
| Personalization: 개인화 SRCC 향상 | 공유 구조 + 개인 잔차 분리 가능성 검증 |
| 문화 미학: 국가 간 취향 비교 | 도메인 내부의 평가 구조 함수적 추정 |
| 계산미학: 특징 기반 분류 | 이론–수식–AI–설명을 단계적으로 연결 |
| MLLM 미학: 단일 모델 성능 극대화 | 분해 구조(Q_core + Q_domain + r_personal + Q_affect)의 이론적 정당화 및 실증 |

---

## 8. 한계 및 위험 요인

### 데이터 한계
- *N* = 600 목표에도 학과별·연도별 편중 가능성.
- 합격 데이터는 학원 MOU 의존 → **선발 편향 문서화 필수**.
- MOU 현황과 수집 파이프라인을 방법론 절 앞에 별도 기술해야 한다.

### 평가 신뢰도
- ICC 0.60 기준 미달 시 *Q_core* 주장 약화 — A1 관문.
- 전문가 역할 갈등(입시 실무 vs 연구 맥락) 관리 필요.
- **Tier 1 루브릭의 조작적 정의와 평가자 훈련 프로토콜 미완이 현재 가장 큰 약점**.
- Wu et al.(2025) DesignPref에서 전문 디자이너 간 Krippendorff's α = 0.25가 보고됨[^26] — 전문가 합의가 도메인에 따라 매우 낮을 수 있음을 시사.

### 모델 위험
- 딥러닝 과적합 및 calibration 문제 (표본 부족 시 overconfidence).
- SHAP/Grad-CAM은 설명의 보조 수단이며 모델 투명성 보증이 아님.
- External validity: Phase 4–5에서 별도 검증 필요.

### 사회적 위험
- 미감의 정답화 위험 → 본 연구는 보조 의사결정 도구 맥락에서만 적용.
- 창의성 다양성 축소 가능성 인지 및 명시.

---

## 9. 기대 기여

### 학문적 기여

| 층위 | 내용 |
|-----|-----|
| 이론 | "디자인은 학습이다" 명제를 계산 구조로 operationalize |
| 방법론 | 이론–수식–AI–설명도구를 단계적으로 연결하는 누적 검증 설계 |
| 데이터 | 미대입시 실합격·불합격 작품 + 전문가 pairwise 평가 데이터셋 |
| 응용 | 시각 판단 보조 의사결정 지원 시스템 (DSS) 프로토타입 |

### 출판 로드맵

| 단계 | 기간 | 목표 |
|-----|-----|-----|
| Stage 0–1 | M0–6 | KCI: HCI Korea, 디자인학연구 |
| Stage 2 | M6–12 | Expert Systems with Applications (SCIE) |
| Stage 3 | M12–18 | AI in Education, ESA |
| Stage E1 | M18+ | IEEE Trans. Affective Computing |
| Stage E2 | M18+ | CVPR / ECCV Workshop |
| Stage E3 | M24+ | CHI, DIS |

### 확장 비전

```
[미대입시 스트레스 도메인]
        ↓ Qcore 검증
[일반 시각 선호 · 평가]
        ↓ domain adapter 교체
[UI/UX] [패션] [인테리어] [제품 디자인]
        ↓ universal preference engine
[시각 판단 기반 DSS 인프라]
```

---

## 10. Summary Map

```
"디자이너는 수용자 효용을 최대화하는 학습 행위자다"
                    │
         ┌──────────┴──────────┐
    공유 구조                도메인 분기
   Qcore(x)              Qdomain(x,d)
 (shared taste,         (문화·도메인·
  typicality,            평가 규칙)
  neural hierarchy)
         └──────────┬──────────┘
                    │
               Q(x,d,u,a)
                    │
          rpersonal(u,x)  +  Qaffect(x,a)
          (habitus,          (Kansei, 정서,
           typicality,        emotion-aware)
           task vector)
                    │
         ┌──────────┴──────────┐
   [스트레스 도메인]        [일반 시각 판단]
    미대입시                UI/UX · 패션 · etc.
   (Stage 0–4)             (Stage E1–E3)
                    │
           MiriArt Calibration Engine
              + DSS (의사결정 지원)
```

---

## 11. 핵심 직접인용 모음

> *"The degree of shared versus individual aesthetic preference differs systematically across visual domains, even for photographic images of real-world content."*
> — Vessel, E.A., Maurer, N., Denker, A.H. & Starr, G.G. (2018). "Stronger shared taste for natural aesthetic domains than for artifacts of human culture." *Cognition*, 179, 121–131.

> *"Taste typicality captured most of the explainable variance in people's impressions, showing that it is the primary dimension along which aesthetic tastes systematically vary."*
> — Chen, Y.-C. et al. (2022). "'Taste typicality' is a foundational and multi-modal dimension of ordinary aesthetic experience." *Current Biology*, 32(8), 1837–1842.

> *"Congruence in personal taste meaningfully differed between cultures, showing higher shared taste in Japanese participants for artistic stimuli. These effects reached beyond comparisons by individual collectivistic tendencies."*
> — Roth, L.H.O., Kawabata, H. & Leder, H. (2026). "Universal, Cultural, or Individual? An Intercultural Assessment of Shared Proportions of Private Taste in Aesthetic Appreciation." *Empirical Studies of the Arts*. DOI: 10.1177/02762374251334962.

> *"Our findings illuminate the nuanced role that cultural context plays in shaping aesthetic judgments and demonstrate the utility of machine learning in unravelling these complex dynamics."*
> — Mikuni, J. et al. (2024). "Cross-cultural comparison of beauty judgments in visual art using machine learning analysis." *Scientific Reports*, 14, 15948.

> *"CLIP can provide better aesthetic features for the IAA downstream task."*
> — Xu, L., Xu, J., Yang, Y., Wang, X., Huang, Y. & Li, Y. (2023). "CLIP Brings Better Features to Visual Aesthetics Learners." arXiv:2307.15640.

> *"Our extensive experiments demonstrate the effectiveness of our approach in generalizing to previously unseen domains — a challenge previous approaches have struggled to achieve."*
> — Yun, J. & Choo, J. (2024). "Scaling Up Personalized Image Aesthetic Assessment via Task Vector Customization." *ECCV 2024*.

> *"Aesthetic value is computed via a hierarchical weighted integration over low- and high-level visual features."*
> — Iigaya, K. et al. (2021). *Nature Human Behaviour*, 5, 1113–1123.

---

## 12. 참고문헌

[^1]: Lu, M., Marghetis, T. & Yang, V.C. (2025). "A first-principles mathematical model integrates the disparate timescales of human learning." *npj Complexity*, 2, 15.

[^2]: Koyama, Y. (2017). *Computational Design Driven by Visual Aesthetic Preference*. PhD thesis, The University of Tokyo.

[^3]: Vessel, E.A., Maurer, N., Denker, A.H. & Starr, G.G. (2018). "Stronger shared taste for natural aesthetic domains than for artifacts of human culture." *Cognition*, 179, 121–131.

[^4]: Lee, H. et al. (2025). "Visual and Auditory Aesthetic Preferences Across Cultures." arXiv:2502.14439. Max Planck Institute for Empirical Aesthetics.

[^5]: Chen, Y.-C. et al. (2022). "'Taste typicality' is a foundational and multi-modal dimension of ordinary aesthetic experience." *Current Biology*, 32(8), 1837–1842.

[^6]: Roth, L.H.O., Kawabata, H. & Leder, H. (2026). "Universal, Cultural, or Individual? An Intercultural Assessment of Shared Proportions of Private Taste in Aesthetic Appreciation." *Empirical Studies of the Arts*. DOI: 10.1177/02762374251334962.

[^7]: Mikuni, J. et al. (2024). "Cross-cultural comparison of beauty judgments in visual art using machine learning analysis of art attribute predictors among Japanese and German speakers." *Scientific Reports*, 14, 15948.

[^8]: Van Geert, E., Ding, X. & Wagemans, J. (2025). "A Cross-Cultural Comparison of Aesthetic Preferences for Neatly Organized Compositions: Chinese vs. Dutch." *Empirical Studies of the Arts*.

[^9]: Bourdieu, P. (1984). *Distinction: A Social Critique of the Judgement of Taste*. Harvard University Press.

[^10]: Iigaya, K. et al. (2021). "Aesthetic preference for art can be predicted from a mixture of low- and high-level visual features." *Nature Human Behaviour*, 5, 1113–1123. — (2023). "Neural mechanisms underlying the hierarchical construction of perceived aesthetic value." *Nature Communications*, 14, 127.

[^11]: Datta, R., Joshi, D., Li, J. & Wang, J.Z. (2006). "Studying Aesthetics in Photographic Images Using a Computational Approach." *ECCV 2006*, LNCS 3953, pp. 288–301.

[^12]: Talebi, H. & Milanfar, P. (2018). "NIMA: Neural Image Assessment." *IEEE Transactions on Image Processing*, 27(8), 3998–4011.

[^13]: Ke, J., Wang, Q., Wang, Y., Milanfar, P. & Yang, F. (2021). "MUSIQ: Multi-Scale Image Quality Transformer." *ICCV 2021*.

[^14]: Ke, J., Ye, K., Yu, J., Wu, Y., Milanfar, P. & Yang, F. (2023). "VILA: Learning Image Aesthetics from User Comments with Vision-Language Pretraining." *CVPR 2023*.

[^15]: Xu, L., Xu, J., Yang, Y., Wang, X., Huang, Y. & Li, Y. (2023). "CLIP Brings Better Features to Visual Aesthetics Learners." arXiv:2307.15640.

[^16]: Yun, J. & Choo, J. (2024). "Scaling Up Personalized Image Aesthetic Assessment via Task Vector Customization." *ECCV 2024*.

[^17]: Wu, H. et al. (2024). "Q-Align: Teaching LMMs for Visual Scoring via Discrete Text-Defined Levels." *ICML 2024*.

[^18]: Huang, Y. et al. (2024). "AesExpert: Towards Multi-modality Foundation Model for Image Aesthetics Perception." *ACM MM 2024*.

[^19]: Wu, S. et al. (2025). "Deep Learning Based Image Aesthetic Quality Assessment: A Review." *ACM Computing Surveys*.

[^20]: Brielmann, A.A. & Pelli, D.G. (2017). "Beauty Requires Thought." *Current Biology*, 27(10), 1506–1513.

[^21]: Chen, G. & Shao, F. (2024). "Image Aesthetics Assessment With Emotion-Aware Multibranch Network." *IEEE Trans. Instrumentation and Measurement*, 73, 1–15.

[^22]: Li, X. et al. (2025). "Personalized Design Aesthetic Preference Modeling: A VAE and Meta-Learning Approach." *Scientific Reports*.

[^23]: Gao, Y. et al. (2024). "AesMamba: Universal Image Aesthetic Assessment with State Space Models." *ACM MM 2024* (Oral).

[^24]: Wang, Z. et al. (2024). "Personalized Image Aesthetics Assessment Based on Graph Neural Network and Collaborative Filtering." *Knowledge-Based Systems*.

[^25]: Li, J. et al. (2024). "Emotion-aware Hierarchical Interaction Network for Multimodal Image Aesthetics Assessment." *Pattern Recognition*.

[^26]: Wu, Y. et al. (2025). "DesignPref: Capturing Personal Preferences in Visual Design Generation." arXiv:2511.20513.

[^27]: Liu, Z. et al. (2025). "Advancing Comprehensive Aesthetic Insight with Multi-Scale Text-Guided Self-Supervised Learning." *AAAI 2025*.

[^28]: Li, Q. et al. (2025). "Multimodal LLMs Can Reason about Aesthetics in Zero-Shot." *ACM MM 2025*.

[^29]: Hertzmann, A. (2025). "Generative Models for the Psychology of Art and Aesthetics." *Empirical Studies of the Arts*.

[^30]: Wang, Y. et al. (2026). "An AI-Generated Art Evaluation Model Integrating Computational Aesthetics and Cognitive Psychology." *Scientific Reports*.

[^31]: Sardenberg, V. et al. (2025). "A Computational Framework for Aesthetic Preferences in Architecture Using Computer Vision and ANNs." *SAGE*.

[^32]: Yang, S. et al. (2026). "Fine-grained Image Aesthetic Assessment: Learning Discriminative Scores from Relative Ranks." *CVPR 2026*.

[^33]: Zhou, Y. et al. (2024). "UNIAA: A Unified Multi-modal Image Aesthetic Assessment Baseline and Benchmark." arXiv:2404.09619.

[^34]: Zhang, H. et al. (2025). "UniQA: Unified Vision-Language Pre-training for Image Quality and Aesthetic Assessment." arXiv:2406.01069.

[^35]: Darda, K. & Chatterjee, A. (2024). "Aesthetic Contextualism and Ingroup Bias." *Journal of Comparative Literature and Aesthetics*, 47(3).

[^36]: Dreyfus, S.E. (2004). "The Five-Stage Model of Adult Skill Acquisition." *Bulletin of Science, Technology & Society*, 24(3), 177–181.

[^37]: Fitts, P.M. & Posner, M.I. (1967). *Human Performance*. Brooks/Cole.

---

*v7 — 2026. 04. 06. | MiriArt Research Initiative*
*v4(기반) → v5(통계 강화) → v6(이론축·직접인용) → v7(상위 철학 명제·스트레스 도메인 완성·2024–2026 선행연구 웹그라운딩 교차검증)*
