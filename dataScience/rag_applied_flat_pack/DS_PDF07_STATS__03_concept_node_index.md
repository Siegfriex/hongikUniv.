# DS_PDF07_STATS — concept node index

## Graph location

시각화의 해석 근거이자 ML 평가와 LLM 확률 모델의 수학적 바닥.

| node_id | label | gate | prerequisites | followups | evidence |
|---|---|---|---|---|---|
| `n_DS_STATS.population_sample_parameter_statistic` | 모집단/표본/모수/통계량 | Gate 1 통계/확률 | - | `n_DS_STATS.statistical_inference`, `n_DS_ML1.train_test_generalization` | `DS_PDF07_STATS:p002:L007` |
| `n_DS_STATS.statistical_inference` | 통계적 추론 | Gate 1 통계/확률 | `n_DS_STATS.population_sample_parameter_statistic` | `n_DS_STATS.bootstrap_imputation`, `n_DS_ML1.train_test_generalization` | `DS_PDF07_STATS:p055:L004` |
| `n_DS_STATS.frequency_histogram` | 도수분포/상대도수/히스토그램 | Gate 1 통계/확률 | `n_DS_STATS.population_sample_parameter_statistic` | `n_DS_VIS.histogram_kde`, `n_DS_STATS.distribution_family` | `DS_PDF07_STATS:p010:L004` |
| `n_DS_STATS.probability_random_variable` | 확률/확률변수 | Gate 1 통계/확률 | `n_DS_STATS.population_sample_parameter_statistic` | `n_DS_STATS.conditional_independence`, `n_DS_LLM.sequence_probability` | `DS_PDF07_STATS:p015:L004` |
| `n_DS_STATS.conditional_independence` | 조건부확률과 독립 | Gate 1 통계/확률 | `n_DS_STATS.probability_random_variable` | `n_DS_STATS.contingency_table`, `n_DS_LLM.sequence_probability` | `DS_PDF07_STATS:p012:L004` |
| `n_DS_STATS.distribution_family` | 이산/연속 확률분포 | Gate 1 통계/확률 | `n_DS_STATS.probability_random_variable` | `n_DS_ML1.loss_metric`, `n_DS_LLM.ngram_language_model` | `DS_PDF07_STATS:p014:L004` |
| `n_DS_STATS.contingency_table` | 분할표 | Gate 1 통계/확률 | `n_DS_STATS.conditional_independence` | `n_DS_ML3.association_rule` | `DS_PDF07_STATS:p012:L004` |
| `n_DS_STATS.bootstrap_imputation` | Bootstrap과 Imputation | Gate 1 통계/확률 | `n_DS_STATS.statistical_inference` | `n_DS_ML1.preprocessing_leakage`, `n_DS_ML3.kmeanspp_local_optimum` | `DS_PDF07_STATS:p056:L004` |

## Visual anchors

- `DS_PDF07_STATS:p002` 모집단/표본/모수/통계량 핵심 용어 -> `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p002__population_sample_terms.png`
- `DS_PDF07_STATS:p008` 도수분포표 -> `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p008__frequency_distribution.png`
- `DS_PDF07_STATS:p010` 히스토그램과 상대도수 -> `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p010__histogram_frequency.png`
- `DS_PDF07_STATS:p012` 두 범주형 변수의 분할표 -> `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p012__contingency_table.png`
- `DS_PDF07_STATS:p014` 이산/연속 확률분포 개요 -> `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p014__distribution_overview.png`
- `DS_PDF07_STATS:p015` 베르누이 시행 -> `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p015__bernoulli_trial.png`
- `DS_PDF07_STATS:p055` bootstrap 재표본추출 -> `dataScience/visual_raw/DS_PDF07_STATS/DS_PDF07_STATS_p055__bootstrap.png`
