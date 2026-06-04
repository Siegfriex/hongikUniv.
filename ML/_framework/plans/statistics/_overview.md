# 통계 1~6강 인벤토리 개요 (`plans/_overview.md` v2)

> **출처:** Perplexity 웹 에이전트 V2 BATCH 1 산출. IDE에 보존용. 실측치와 불일치하는 항목은 §1.1 주석 참조.
> **경로:** `_framework/plans/statistics/_overview.md`

## 0. 분기 요약: no-transcript + deep_dive

- INVENTORY_INDEX에 따르면 `statistics/` 과목은 현재 sidecar 트리가 없고, SSOT는 `statistics/{YYYYMMDD}_{N}강.md` 만 존재하는 상태다.
- PIPELINE 상 단계 02(segments/alignments/evidence from transcript, annotated_transcript.txt)는 전사 txt 부재로 수행할 수 없으므로, 본 분기는 **`branch: "no-transcript"`**로 고정하고 `segments.jsonl`, `alignments.jsonl`, `*_annotated_transcript.txt` 를 생성하지 않는다.
- manifest 템플릿에서 `lecture_md_anchor` 소스만 구조 SSOT로 사용하며, `transcript_ssot` 항목은 경로만 남기거나 제거하되, `inventory_quality_min_bar.rule_d_evidence` 를 통해 **md-primary 노드**의 근거를 `lecture_md_anchor` 기반 evidence로만 만족시킨다.
- PIPELINE §4에 정의된 파생 md 중 본 분기에서 실제로 생성하는 것은 각 강별 `YYYYMMDD_{N}강_심화.md` 뿐이며, dataScience 코스에서 사용하는 `*_래그.md`, `*_로데이터디벨롭.md`는 **형식 참고용 레퍼런스**로만 취급한다.
- evidence 레벨에서 허용하는 `source_kind`는 `lecture_md_anchor`와 `web_grounding` 두 가지이며, transcript/lecturedocx 기반 evidence는 사용하지 않는다.

---

## 1. 통계 1~6강 SSOT md 계량 요약

### 1.1 파일별 라인 수·heading 수·LaTeX/공식 블록 수 (실측치로 갱신 예정)

> 주: 아래 수치는 웹 에이전트의 근사값이며, IDE에서 실측 후 §1.2 표로 덮어쓴다.

| lecture_id  | SSOT 파일명        | 대략 줄 수 | heading 수 (H1–H3) | 수식/LaTeX·공식 블록 수 | 주요 개념 축 요약 |
|------------|-------------------|-----------:|--------------------:|-------------------------:|-------------------|
| 20250303_1 | 20250303_1강.md   | ≈ 400–450  | ≈ 10–15             | ≈ 5–10                   | 통계/통계학 정의, 통계의 어원과 역사(Statistik, Staatenkunde, Political Arithmetic), DIKW, 데이터사이언스 3기둥, population/sample/parameter/statistic, sampling error, 빅데이터·ML/AI 맥락, Galton/Pearson/Gosset/Fisher 소개. |
| 20250310_2 | 20250310_2강.md   | ≈ 150–200  | ≈ 8–12              | ≈ 3–5                    | 기술 vs 추론 통계, 모수 기호(μ, σ, p) vs 통계량(x̄, s, p̂), GIGO, 변수/개체, 범주형/수치형, NA, Likert 척도, 공공 데이터 포털, Excel 기본 함수와 Data Analysis ToolPak. |
| 20260317_3 | 20260317_3강.md   | ≈ 550–650  | ≈ 15–20             | ≈ 20–30                  | EDA 정의, 도수분포표·히스토그램, PivotTable/Chart, 중심경향(Mean/Median/Mode), 산포(Range, Variance, Std, CV), 자유도와 Bessel 보정, 분위수·IQR, 왜도·첨도, Excel 기술통계 도구, 외부 참고 링크. |
| 20260324_4 | 20260324_4강.md   | ≈ 120–160  | ≈ 8–10              | ≈ 5–8                    | 3강 복습(IQR, outlier), 확률의 기본(표본공간, 사건, 공리), 조건부확률, 곱셈·덧셈법칙, 전확률/베이즈 예비, RAND를 이용한 시뮬레이션·연습문제 안내. |
| 20260407_5 | 20260407_5강.md   | ≈ 500–600  | ≈ 15–20             | ≈ 20–30                  | 확률법칙 복습, 확률변수 X와 분포 정의, 이산형 분포(Bernoulli, Binomial, Hypergeometric, Poisson), 연속형 분포(Normal), PMF/PDF, 기대값·분산 정의와 성질, 표본분포·CLT 입구, Excel BINOM.DIST/NORM.DIST. |
| 20260414_6 | 20260414_6강.md   | ≈ 350–420  | ≈ 12–16             | ≈ 15–20                  | 이산/연속 분포 비교, Poisson/Binomial/Hypergeometric/Normal 심화, 정규분포 성질(선형변환·합의 분포, 68–95–99.7 rule), 표준정규 Z와 z-값, 표본평균의 분포와 standard error, CLT, 이항의 정규 근사, 결합분포·공분산. |

### 1.2 IDE 실측치 (2026-04 측정)

> 측정: `Select-String -Pattern '^#{1,3} '` 기준 H1~H3 heading 개수, `Get-Content | Count` 기준 줄 수.
> LaTeX/수식 블록 수는 별도 실측 필요(현재 미측정 — 각 강 배치 v2 작성 시 채움).

| lecture_id  | lines (실측) | H1–H3 (실측) | 근사치와의 차이 | 비고 |
|------------|-------------:|-------------:|-----------------|------|
| 20250303_1 | 663 | 52 | lines +213 / H +37 | 근사(400~450, 10~15) 대비 **50% 이상 큼**. 1강 md가 역사·인물·배경을 크게 다룸 |
| 20250310_2 | 247 | 13 | lines +47 / H +1  | 근사(150~200, 8~12) 대비 줄 수만 초과. 큰 차이 없음 |
| 20260317_3 | 579 | 14 | lines ≈ / H −1    | 근사(550~650, 15~20) 대비 lines 일치. H 수 소폭 미달 |
| 20260324_4 | 133 | 14 | lines ≈ / H +4    | 근사(120~160, 8~10) 대비 일치. H는 소폭 초과(4강이 짧지만 소단원 많음) |
| 20260407_5 | 1036 | 51 | lines +436 / H +31 | 근사(500~600, 15~20) 대비 **거의 2배**. 5강이 실질 최대 분량 |
| 20260414_6 | 745 | 46 | lines +325 / H +30 | 근사(350~420, 12~16) 대비 **2배 가까이 큼** |

**불일치 경보 (BATCH 2~7 작성 시 반영):**

- 1강·5강·6강은 근사치 대비 실측이 **2배 가까이** 많다. 노드 수 추정·`deep_dive_plan.estimated_lines` 재산정 필요.
- 특히 **5강**(1036줄, 51 heading) 은 6강(745)보다 큰 실질 본편이다. 배치 6이 가장 큰 배치가 될 것.
- 2강·4강은 근사와 큰 차이 없음(작고 농축).
- heading 수가 실측에서 큰 강(1강·5강·6강)은 노드를 과소 추정할 위험. `nodes[]` 최소 15~20개로 상향 검토.

---

## 2. 전역 개념 체인: node_id 레벨 골격

> 여기서는 각 강에서 가장 중요한 개념을 **후보 node_id** 형태로만 정의한다. 실제 nodes.json에 넣을 필드(증거·공식·예제 등)는 각 강 directives.json v2에서 확정한다.

### 2.1 통계학·데이터·모수/통계량 축

- `n_STAT1.statistics_definition_scope` — 통계(statistics)와 통계학(discipline) 정의, "collection, analysis, interpretation of masses of numerical data" 원문 인용 기반 노드.
- `n_STAT1.population_sample_parameter_statistic` — 모집단/표본/모수/통계량/표본오차 정의와 관계.
- `n_STAT2.parameter_vs_statistic_notation` — μ, σ, p vs x̄, s, p̂ 기호 구분과 역할.
- `n_STAT2.descriptive_vs_inferential_statistics` — 기술통계 vs 추론통계 정의와 예시.
- (cross to DS) `n_DS1.dikw_pyramid` / `n_DS*.data_science_three_pillars` — DIKW, 데이터사이언스 3기둥과 통계 1강 요소를 `extends`/`prerequisite`로 연결.

### 2.2 EDA·기술통계량 축

- `n_STAT3.frequency_distribution_and_histogram` — 도수분포표·계급·히스토그램 작성 규칙.
- `n_STAT3.measures_of_central_tendency` — 평균·중앙값·최빈값 정의, skewness와의 관계.
- `n_STAT3.measures_of_dispersion` — 범위, 분산, 표준편차, 변동계수, IQR.
- `n_STAT3.sample_variance_and_bessel_correction` — n vs n−1, 자유도, 편향 보정.
- `n_STAT3.skewness_and_kurtosis` — 분포의 비대칭성과 꼬리/뾰족함 지표.
- (cross to DS) `n_DS*.summary_statistics_numeric`, `n_DS*.distribution_shape_metrics`.

### 2.3 확률·확률변수·분포 축

- `n_STAT4.probability_axioms_and_sample_space` — 표본공간, 사건, 공리 3가지.
- `n_STAT4.conditional_probability_and_independence` — P(A|B), 곱셈법칙, 독립 사건.
- `n_STAT4.law_of_total_probability_and_bayes_intro`.
- `n_STAT5.random_variable_and_distribution_definition` — 확률변수 X, 값 공간, 분포, PMF/PDF 정의.
- `n_STAT5.binomial_distribution_definition`, `n_STAT5.hypergeometric_distribution`, `n_STAT5.poisson_distribution`, `n_STAT5.normal_distribution_basics`.
- `n_STAT5.expectation_and_variance_properties`.
- (cross to DS) `n_DS*.probability_basics`, `n_DS*.bayesian_reasoning_intro`.

### 2.4 표본분포·정규·CLT·근사·결합분포 축

- `n_STAT6.standard_normal_distribution_and_z_score`.
- `n_STAT6.sampling_distribution_of_sample_mean`.
- `n_STAT6.standard_error_of_mean`.
- `n_STAT6.central_limit_theorem_for_sample_mean`.
- `n_STAT6.normal_approximation_to_binomial_with_continuity_correction`.
- `n_STAT6.joint_distribution_and_covariance`.
- (cross to DS) `n_DS6.covariance_correlation`, `n_DS12.correlation_vs_causation`, `n_DS*.linear_regression_gaussian_noise`.

---

## 3. 전역 cross-lecture 엣지 (node 단위 설계 초안)

> edge_id는 실제 edges.json 에서 `e_STAT{N}_<from_short>_to_<to_short>` 패턴을 따르며, 여기서는 from/to와 type, 이유만 정의한다.

### 3.1 선행(기초 개념) → 후속(응용) 체인

- `n_STAT1.population_sample_parameter_statistic` → `n_STAT2.parameter_vs_statistic_notation`
  - type: `prerequisite`
  - why: 1강에서 개념을 정의하고 2강에서 기호·예시를 부여.

- `n_STAT2.descriptive_vs_inferential_statistics` → `n_STAT3.measures_of_central_tendency`
  - type: `prerequisite`
  - why: "기술통계"라는 기능적 구분 뒤에 실제 지표(평균/중앙값/최빈값)를 3강에서 도입.

- `n_STAT3.measures_of_dispersion` → `n_STAT6.standard_error_of_mean`
  - type: `extends`
  - why: 표본의 산포(표준편차)가 6강에서 표본평균의 표준오차 SE(X̄)에 직접 사용된다.

- `n_STAT4.conditional_probability_and_independence` → `n_STAT5.binomial_distribution_definition`
  - type: `prerequisite`
  - why: 독립 베르누이 시행의 정의가 곱셈법칙 P(A∩B)=P(A)P(B)에 기반하기 때문.

- `n_STAT5.normal_distribution_basics` → `n_STAT6.central_limit_theorem_for_sample_mean`
  - type: `prerequisite`
  - why: CLT 결론이 "정규분포에 수렴"이므로 정규분포의 성질이 선행되어야 한다.

### 3.2 통계 ↔ dataScience cross-코스 엣지(대표 축)

- `n_STAT3.sample_variance_and_bessel_correction` → `n_DS6.covariance_correlation`
  - type: `prerequisite`
  - why: 공분산과 상관계수 정의가 각각 분산 개념과 자유도 조정에 의존.

- `n_STAT4.law_of_total_probability_and_bayes_intro` → `n_DS*.bayes_theorem_applications`
  - type: `prerequisite`
  - why: dataScience 쪽 베이즈 응용 노트는 전확률법칙 분해와 posterior 계산을 전제로 한다.

- `n_STAT6.joint_distribution_and_covariance` → `n_DS*.multivariate_regression_model`
  - type: `extends`
  - why: 회귀 모형의 추정/해석은 (X,Y)의 결합분포와 공분산 구조 이해에 기반.

---

## 4. 공통 웹그라운딩 전략 (v2 기준)

> 각 강 directives.json에서 node별 `web_grounding_candidates` 레코드를 채울 때, 다음 pool에서 도메인을 고르고 **서로 다른 independence_group 최소 2개**를 만족시키도록 한다.

### 4.1 independence_group 후보

- `psu_stat_notes`: Pennsylvania State University STAT 코스 온라인 노트 (`online.stat.psu.edu`).
- `statlect`: Statlect 이론 노트 (`statlect.com`).
- `wiki_ko`: 한국어 위키피디아(`ko.wikipedia.org`) 통계 관련 항목.
- `wiki_en_aux`: 영어 위키피디아(`en.wikipedia.org`) — 수리 보조.
- `kostat_official`: 통계청(`kostat.go.kr`) 정의·용어집·공식 통계 설명.
- `kr_univ_stats`: 국내 대학 통계 강의노트/슬라이드 (예: `stat.snu.ac.kr`, `stat.kaist.ac.kr` 등).
- `textbook_ref`: 교과서(예: Casella & Berger, Wasserman, Rice) 장·절 번호로만 참조.

### 4.2 예시 레코드 스케치 (실제 URL·quote는 각 강에서 확정)

- EX for `n_STAT3.sample_variance_and_bessel_correction`
  - `online.stat.psu.edu`의 sample variance 편: sample variance가 n−1로 나누는 이유를 unbiasedness 관점에서 설명하는 섹션.
  - `statlect.com` variance estimator 페이지: 자유도와 편향에 대한 증명 개요.

- EX for `n_STAT6.central_limit_theorem_for_sample_mean`
  - Statlect CLT page(독립·동일분포·유한 분산 가정 나열).
  - PSU STAT 414/510 CLT 노트(정규/비정규 모집단 예시).

모든 노드는 `grounding_ids`에 서로 다른 `independence_group`을 최소 2개 포함하도록 지시하고, 한 도메인에만 의존한 경우 `self_score.has_two_independent_sources=false`로 플래그한다.

---

## 5. 전역 리팩터링 위험 요약(심화 md 공통 가이드)

> 이 섹션은 각 강 directive.md §6의 "공통 위험" 배경이 된다.

1. **표본분산의 분모(n vs n−1)와 자유도**
   - 현상: 3강 md는 Bessel 보정, degrees of freedom을 상세히 설명하면서도, 일부 표/예제에서는 n과 n−1이 혼용될 여지가 있다.
   - 지침: 심화 md에서는 "표본분산: n−1, 모분산: N"을 일관되게 유지하고, 예제마다 "어떤 분산인지"를 명시한다. n=1에서 s²가 정의되지 않는 boundary case를 분명히 언급한다.

2. **PMF vs PDF 및 '확률' 용어 혼용**
   - 현상: 5·6강 md는 PMF/PDF를 표로 비교하지만, 설명 문단에서는 "확률"이라는 단어가 이산/연속 문맥에서 혼용될 수 있다.
   - 지침: 심화 md의 모든 연속형 예제에서 "구간 확률" 표현을 사용하고, PDF 값 자체는 "밀도"로만 지칭한다.

3. **정규분포 표기와 파라미터 해석**
   - 현상: N(μ,σ²) 표기가 기본이지만, Excel 함수나 예제에서 σ를 표준편차/분산 하나로만 강조할 때 독자가 혼동할 여지가 있다.
   - 지침: 심화 md에서는 location parameter(μ), scale parameter(σ), variance(σ²)를 모두 명시하고, N(μ,σ²)를 기본 표기로 고정한다.

4. **데이터 타입 용어의 다중 표기**
   - 현상: 2강에서 정성/정량, 범주형/수치형, 명목/순서/등간/비율 등 다양한 분류 체계가 섞여 등장한다.
   - 지침: node canonical_label과 심화 md 본문에서는 `범주형(categorical) / 수치형(numeric)`을 1차 구분으로 사용하고, 다른 용어는 모두 이 체계에 매핑된 형태로만 소개한다.

5. **표본 vs 모집단 용어 일관성**
   - 현상: 1·2·3·6강 전반에서 "데이터 전체"를 지칭할 때 모집단/표본 표현이 문맥에 따라 다르게 쓰일 위험이 있다.
   - 지침: 심화 md의 모든 예제에서 "이건 모집단, 이건 표본"을 명시하고, 통계량/모수 기호와 맞물리게 통일한다.

---

## 6. 구현 에이전트용 전역 체크리스트

1. `statistics/_inventory/`에 각 lecture_id별 스켈레톤 디렉터리 생성 후, manifest/anchors_md/nodes/edges/evidence/conflicts/README_inventory 생성.
2. `manifest.json.policy_note`에 `"branch: no-transcript, no segments/alignments/annotated_transcript, md-only lineage"` 명시.
3. 각 강 directives.json v2에서 정의된 anchors/nodes/edges에 따라 `anchors_md.json`, `nodes.json`, `edges.json` 작성.
4. `evidence.jsonl`에는 `source_kind: lecture_md_anchor`·`web_grounding`만 사용하고, 각 node가 v2 Depth Spec을 만족하도록 `md_evidence`와 `web_grounding.jsonl`을 채움.
5. `{lecture_id}_심화.md`는 dataScience `_래그.md`/`_로데이터디벨롭.md` 형식을 참고해, node 단위로 정의·직관·예제·오해·cross-link를 sections로 구현.
6. `conflicts_and_uncertainty.md`에는 본 개요 §5의 리스크와 각 강 directive.md §6의 강별 리스크를 요약 기록.
