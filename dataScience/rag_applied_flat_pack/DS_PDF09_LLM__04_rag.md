# DS_PDF09_LLM — RAG tutor source

## Retrieval Routing Table

| route | when to use | primary files |
|---|---|---|
| `DS_PDF09_LLM` | 언어모델은 다음 토큰 확률을 학습하고, Transformer/사전학습/Instruction tuning/RAG로 지시 수행형 LLM까지 확장된다. | `__01_pdf_transcript`, `__02_rawdata_develop`, `__03_concept_node_index`, this `__04_rag` |

## Core Concept Node Cards

### `n_DS_LLM.sequence_probability` — 언어모델과 문장 확률

- 정의: 언어모델은 단어/토큰 시퀀스의 가능도와 다음 토큰의 조건부 확률을 모델링한다.
- 직관: 문장이 자연스럽게 이어질 가능성을 확률로 계산한다.
- 수식/절차: P(w1...wn)=product P(w_t | context)
- pandas/sklearn 언어: tokenizer -> model logits -> softmax probabilities
- 오답위험: LLM이 검색엔진처럼 사실을 조회한다고 생각하고 확률 생성 구조를 무시하는 오류.
- 연결: 선행 n_DS_STATS.conditional_independence / 후속 n_DS_LLM.ngram_language_model, n_DS_LLM.attention_transformer / 유사 -
- source trace: `DS_PDF09_LLM:p007:L004`, `ev_DS_PDF09_LLM_001`

### `n_DS_LLM.ngram_language_model` — N-gram 통계적 언어모델

- 정의: 앞의 n-1개 단어를 조건으로 다음 단어 확률을 추정하는 통계적 언어모델이다.
- 직관: 가까운 몇 단어만 보고 다음 단어를 예측하는 빈도 기반 모델이다.
- 수식/절차: P(w_t | w_{t-n+1},...,w_{t-1}) estimated from counts
- pandas/sklearn 언어: CountVectorizer(ngram_range=...), frequency table
- 오답위험: n이 커지면 항상 좋아진다고 보고 sparse data 문제를 무시하는 오류.
- 연결: 선행 n_DS_LLM.sequence_probability, n_DS_STATS.frequency_histogram / 후속 n_DS_LLM.embedding_contextual_representation / 유사 -
- source trace: `DS_PDF09_LLM:p003:L005`, `ev_DS_PDF09_LLM_002`

### `n_DS_LLM.embedding_contextual_representation` — Embedding과 문맥 표현

- 정의: 토큰을 계산 가능한 연속 벡터로 바꾸고 문맥에 따라 의미 표현을 갱신하는 방식이다.
- 직관: 단어를 좌표로 바꾸어 의미적으로 가까운 단어가 공간에서도 가까워지게 한다.
- 수식/절차: token -> embedding vector; contextual model updates representation with surrounding tokens
- pandas/sklearn 언어: Embedding layer, tokenizer, transformer hidden states
- 오답위험: embedding을 사람이 정한 사전 코드처럼 고정 의미로 보는 오류.
- 연결: 선행 n_DS_ML1.text_vectorization_features / 후속 n_DS_LLM.attention_transformer, n_DS_ML3.kmeans_distance_metrics / 유사 -
- source trace: `DS_PDF09_LLM:p004:L004`, `ev_DS_PDF09_LLM_003`

### `n_DS_LLM.encoder_decoder_seq2seq` — Encoder/Decoder와 Seq2Seq

- 정의: 입력 시퀀스를 표현으로 압축하는 encoder와 출력 시퀀스를 생성하는 decoder를 결합한 구조다.
- 직관: 문장을 이해하는 쪽과 문장을 내보내는 쪽을 나눈 번역기 구조다.
- 수식/절차: encoder(input sequence)->context representation; decoder(context)->output sequence
- pandas/sklearn 언어: seq2seq model, encoder outputs, decoder generation
- 오답위험: encoder/decoder를 단순 전처리/후처리 함수로만 보는 오류.
- 연결: 선행 n_DS_LLM.embedding_contextual_representation / 후속 n_DS_LLM.attention_transformer / 유사 -
- source trace: `DS_PDF09_LLM:p003:L007`, `ev_DS_PDF09_LLM_004`

### `n_DS_LLM.attention_transformer` — Attention과 Transformer

- 정의: attention은 토큰들이 서로 얼마나 참고해야 하는지 가중치를 계산하고, Transformer는 recurrence 없이 attention 중심으로 시퀀스를 처리한다.
- 직관: 문장 안 모든 단어가 서로를 보며 중요한 연결에 집중하게 하는 구조다.
- 수식/절차: Attention(Q,K,V)=softmax(QK^T/sqrt(d_k))V
- pandas/sklearn 언어: Transformer encoder/decoder, multi-head self-attention
- 오답위험: attention weight를 곧바로 인간적 설명 또는 인과로 단정하는 오류.
- 연결: 선행 n_DS_LLM.encoder_decoder_seq2seq / 후속 n_DS_LLM.bert_gpt_pretraining, n_DS_LLM.foundation_instruction_tuning / 유사 -
- source trace: `DS_PDF09_LLM:p038:L004`, `ev_DS_PDF09_LLM_005`

### `n_DS_LLM.bert_gpt_pretraining` — BERT/GPT와 사전학습

- 정의: BERT는 encoder 계열 양방향 문맥 표현, GPT는 decoder 계열 다음 토큰 생성을 중심으로 한 Transformer 사전학습 모델이다.
- 직관: 많은 텍스트로 먼저 언어 패턴을 익히고, 이후 작업별로 조정한다.
- 수식/절차: pre-train on large corpus -> fine-tune or prompt for downstream task
- pandas/sklearn 언어: BERT encoder, GPT decoder, pretraining/fine-tuning
- 오답위험: BERT와 GPT를 같은 생성 모델로만 묶거나 encoder/decoder 차이를 지우는 오류.
- 연결: 선행 n_DS_LLM.attention_transformer / 후속 n_DS_LLM.foundation_instruction_tuning / 유사 -
- source trace: `DS_PDF09_LLM:p037:L004`, `ev_DS_PDF09_LLM_006`

### `n_DS_LLM.foundation_instruction_tuning` — Foundation model과 instruction tuning

- 정의: Foundation model은 대규모 사전학습 기반 범용 모델이고, instruction tuning은 지시를 이해하고 수행하도록 추가 학습하는 절차다.
- 직관: 문장 생성기가 사용자의 지시를 따르는 작업 수행자로 바뀌는 단계다.
- 수식/절차: pretrained LM -> supervised instruction data/RLHF preference optimization -> aligned assistant behavior
- pandas/sklearn 언어: instruction dataset, supervised fine-tuning, preference/RLHF pipeline
- 오답위험: instruction tuning이 factual grounding을 자동 보장한다고 보는 오류.
- 연결: 선행 n_DS_LLM.bert_gpt_pretraining / 후속 n_DS_LLM.rag_grounding / 유사 -
- source trace: `DS_PDF09_LLM:p039:L005`, `ev_DS_PDF09_LLM_007`

### `n_DS_LLM.rag_grounding` — RAG와 근거 기반 튜터링

- 정의: RAG는 모델의 생성 능력에 외부 검색 근거를 결합해 답변의 출처성, 갱신성, 검증 가능성을 높이는 설계다.
- 직관: 머릿속 기억만 말하지 않고 책장을 찾아 근거를 붙여 대답하게 하는 구조다.
- 수식/절차: query -> retrieve source chunks -> rerank/route -> generate with citations -> verify
- pandas/sklearn 언어: vector store, hybrid retrieval, reranker, source trace table
- 오답위험: 검색 결과가 있으면 답이 무조건 맞다고 보거나, PDF 근거와 웹 보강을 섞어 출처 우선순위를 잃는 오류.
- 연결: 선행 n_DS_LLM.foundation_instruction_tuning, n_DS_ML3.support_confidence_lift / 후속 n_DS_GLOBAL.tutor_operating_modes / 유사 -
- source trace: `WEB:web_rag_2020`, `ev_DS_PDF09_LLM_008`

## Visual Example Cards

- `lm_history`: 규칙기반에서 LLM까지 언어모델 발전사 / anchor `DS_PDF09_LLM:p003:L001` / image `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p003__lm_history.png`
- `embedding_encoder_decoder`: embedding/encoder/decoder 기본 용어 / anchor `DS_PDF09_LLM:p004:L001` / image `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p004__embedding_encoder_decoder.png`
- `conditional_probability_lm`: 조건부 확률 기반 언어모델 / anchor `DS_PDF09_LLM:p007:L001` / image `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p007__conditional_probability_lm.png`
- `nnlm_structure`: NNLM 구조 / anchor `DS_PDF09_LLM:p022:L001` / image `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p022__nnlm_structure.png`
- `seq2seq`: encoder-decoder seq2seq / anchor `DS_PDF09_LLM:p035:L001` / image `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p035__seq2seq.png`
- `gpt_decoder`: GPT decoder-only 다음 단어 예측 / anchor `DS_PDF09_LLM:p037:L001` / image `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p037__gpt_decoder.png`
- `large_language_model`: Transformer 기반 LLM과 foundation model / anchor `DS_PDF09_LLM:p038:L001` / image `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p038__large_language_model.png`
- `instruction_tuning`: instruction tuning 예시 / anchor `DS_PDF09_LLM:p039:L001` / image `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p039__instruction_tuning.png`

## Code Mapping

- row = observation, column = variable, feature matrix = `X`, target vector = `y`.
- `fit` = 학습, `predict` = 추론, `transform` = 표현 변환, `metric` = 평가 함수.
- 시각화/통계 노드는 pandas 집계와 plot으로, ML 노드는 sklearn estimator/pipeline으로, LLM 노드는 tokenizer/embedding/retrieval로 매핑한다.

## Misconception Bank

- 언어모델과 문장 확률: LLM이 검색엔진처럼 사실을 조회한다고 생각하고 확률 생성 구조를 무시하는 오류.
- N-gram 통계적 언어모델: n이 커지면 항상 좋아진다고 보고 sparse data 문제를 무시하는 오류.
- Embedding과 문맥 표현: embedding을 사람이 정한 사전 코드처럼 고정 의미로 보는 오류.
- Encoder/Decoder와 Seq2Seq: encoder/decoder를 단순 전처리/후처리 함수로만 보는 오류.
- Attention과 Transformer: attention weight를 곧바로 인간적 설명 또는 인과로 단정하는 오류.
- BERT/GPT와 사전학습: BERT와 GPT를 같은 생성 모델로만 묶거나 encoder/decoder 차이를 지우는 오류.
- Foundation model과 instruction tuning: instruction tuning이 factual grounding을 자동 보장한다고 보는 오류.
- RAG와 근거 기반 튜터링: 검색 결과가 있으면 답이 무조건 맞다고 보거나, PDF 근거와 웹 보강을 섞어 출처 우선순위를 잃는 오류.

## Web Grounding Notes

- `web_bert_2018` BERT: Pre-training of Deep Bidirectional Transformers: https://arxiv.org/abs/1810.04805 — Encoder-style bidirectional pre-training and downstream fine-tuning.
- `web_transformer_2017` Attention Is All You Need: https://arxiv.org/abs/1706.03762 — Transformer as attention-based sequence architecture.
- `web_instructgpt_2022` Training language models to follow instructions with human feedback: https://arxiv.org/abs/2203.02155 — Instruction tuning/RLHF as user-intent alignment extension.
- `web_rag_2020` Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks: https://arxiv.org/abs/2005.11401 — RAG as parametric model plus non-parametric retrieval memory.

## Source Trace Table

| node_id | evidence_id | transcript_anchor | snippet |
|---|---|---|---|
| `n_DS_LLM.sequence_probability` | `ev_DS_PDF09_LLM_001` | `DS_PDF09_LLM:p007:L004` | 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)Language Model은 다음과 같이 조건부 확률을 활용하여 표현 가능단어 시퀀스 𝑊가 n개의 단어(𝑤!,𝑖=1,2,…,𝑛)들로 구성단어 시퀀스 𝑊가 등장할 확률은 아래와 같이 표현 가능 |
| `n_DS_LLM.ngram_language_model` | `ev_DS_PDF09_LLM_002` | `DS_PDF09_LLM:p003:L005` | ~1990: 통계적 언어모델Statistical Language ModelN-gram 등 단어의 빈도수를 기반으로 다음에 올 단어의 확률을 계산하는 방식 |
| `n_DS_LLM.embedding_contextual_representation` | `ev_DS_PDF09_LLM_003` | `DS_PDF09_LLM:p004:L004` | 언어모델 (Language Model, LM)기본 개념과 용어•임베딩Embedding- 단어(토큰)를 모델이 계산할 수 있는연속적인 벡터 공간 표현으로 변환하는 단계- 의미적으로 유사한 단어들이벡터 공간에서도 가깝게 위치하도록 학습 |
| `n_DS_LLM.encoder_decoder_seq2seq` | `ev_DS_PDF09_LLM_004` | `DS_PDF09_LLM:p003:L007` | 2013~16: 시퀀스 모델링Recurrent Neural Network (RNN)Long Short-Term Memory(LSTM)Sequence to Sequence (Seq2Seq)**문장을 시퀀스 단위로 학습, 장기 의존성 개선 시도 |
| `n_DS_LLM.attention_transformer` | `ev_DS_PDF09_LLM_005` | `DS_PDF09_LLM:p038:L004` | 대형언어모델 (Large Language Model, LLM)Large Language Model- LLM은 Transformer 계열(특히 self-attention)을 기반으로, 방대한 텍스트(및 경우에 따라 코드·이미지·표 등)를 이용해대규모 사전학습(pre-training)을 수행- 언어를 넘어 다양한 작업을... |
| `n_DS_LLM.bert_gpt_pretraining` | `ev_DS_PDF09_LLM_006` | `DS_PDF09_LLM:p037:L004` | 언어모델 (Language Model, LM)Generative Pre-trained Transformer, GPT-트랜스포머의디코더(Decoder)구조를 사용-문장을 한 방향(Unidirectional)으로 읽으며 다음에 올 단어를 예측 |
| `n_DS_LLM.foundation_instruction_tuning` | `ev_DS_PDF09_LLM_007` | `DS_PDF09_LLM:p039:L005` | 예) 기존 언어 모델Input: “Translate the following sentence into ______”Output: ”Korean”LLM –instruction tuningInstruction:Translate the following sentence into Korean.Input:Machine lea... |
| `n_DS_LLM.rag_grounding` | `ev_DS_PDF09_LLM_008` | `WEB:web_rag_2020` | 강의 PDF 전사에서 직접 키워드가 약해 `web_rag_2020`를 확장 근거로 사용: RAG as parametric model plus non-parametric retrieval memory. |
