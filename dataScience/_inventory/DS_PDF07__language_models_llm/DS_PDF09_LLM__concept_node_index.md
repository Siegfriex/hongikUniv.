# DS_PDF09_LLM — concept node index

## Graph location

확률·벡터화·딥러닝·검색근거를 하나로 묶는 최종 응용 계층.

| node_id | label | gate | prerequisites | followups | evidence |
|---|---|---|---|---|---|
| `n_DS_LLM.sequence_probability` | 언어모델과 문장 확률 | Gate 6 NLP/LLM | `n_DS_STATS.conditional_independence` | `n_DS_LLM.ngram_language_model`, `n_DS_LLM.attention_transformer` | `DS_PDF09_LLM:p007:L004` |
| `n_DS_LLM.ngram_language_model` | N-gram 통계적 언어모델 | Gate 6 NLP/LLM | `n_DS_LLM.sequence_probability`, `n_DS_STATS.frequency_histogram` | `n_DS_LLM.embedding_contextual_representation` | `DS_PDF09_LLM:p003:L005` |
| `n_DS_LLM.embedding_contextual_representation` | Embedding과 문맥 표현 | Gate 6 NLP/LLM | `n_DS_ML1.text_vectorization_features` | `n_DS_LLM.attention_transformer`, `n_DS_ML3.kmeans_distance_metrics` | `DS_PDF09_LLM:p004:L004` |
| `n_DS_LLM.encoder_decoder_seq2seq` | Encoder/Decoder와 Seq2Seq | Gate 6 NLP/LLM | `n_DS_LLM.embedding_contextual_representation` | `n_DS_LLM.attention_transformer` | `DS_PDF09_LLM:p003:L007` |
| `n_DS_LLM.attention_transformer` | Attention과 Transformer | Gate 6 NLP/LLM | `n_DS_LLM.encoder_decoder_seq2seq` | `n_DS_LLM.bert_gpt_pretraining`, `n_DS_LLM.foundation_instruction_tuning` | `DS_PDF09_LLM:p038:L004` |
| `n_DS_LLM.bert_gpt_pretraining` | BERT/GPT와 사전학습 | Gate 6 NLP/LLM | `n_DS_LLM.attention_transformer` | `n_DS_LLM.foundation_instruction_tuning` | `DS_PDF09_LLM:p037:L004` |
| `n_DS_LLM.foundation_instruction_tuning` | Foundation model과 instruction tuning | Gate 6 NLP/LLM | `n_DS_LLM.bert_gpt_pretraining` | `n_DS_LLM.rag_grounding` | `DS_PDF09_LLM:p039:L005` |
| `n_DS_LLM.rag_grounding` | RAG와 근거 기반 튜터링 | Gate 6 NLP/LLM | `n_DS_LLM.foundation_instruction_tuning`, `n_DS_ML3.support_confidence_lift` | `n_DS_GLOBAL.tutor_operating_modes` | `WEB:web_rag_2020` |

## Visual anchors

- `DS_PDF09_LLM:p003` 규칙기반에서 LLM까지 언어모델 발전사 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p003__lm_history.png`
- `DS_PDF09_LLM:p004` embedding/encoder/decoder 기본 용어 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p004__embedding_encoder_decoder.png`
- `DS_PDF09_LLM:p007` 조건부 확률 기반 언어모델 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p007__conditional_probability_lm.png`
- `DS_PDF09_LLM:p022` NNLM 구조 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p022__nnlm_structure.png`
- `DS_PDF09_LLM:p035` encoder-decoder seq2seq -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p035__seq2seq.png`
- `DS_PDF09_LLM:p037` GPT decoder-only 다음 단어 예측 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p037__gpt_decoder.png`
- `DS_PDF09_LLM:p038` Transformer 기반 LLM과 foundation model -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p038__large_language_model.png`
- `DS_PDF09_LLM:p039` instruction tuning 예시 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p039__instruction_tuning.png`
