# DS_PDF09_LLM — rawdata develop

## One-line source role

언어모델은 다음 토큰 확률을 학습하고, Transformer/사전학습/Instruction tuning/RAG로 지시 수행형 LLM까지 확장된다.

## Source policy

- PDF raw: `dataScience/pdf_raw/[Lecture][DS][09]언어모델과 LLM.pdf`
- TXT raw transcript: `dataScience/txt_raw/DS_PDF07__language_models_llm__full_transcript.txt`
- PDF page images are derived visual raw data, not a replacement for the PDF.
- 숫자·공식·최적값은 전사와 이미지가 충돌하면 원본 PDF 대조가 우선이다.

## Visual raw intake

- `DS_PDF09_LLM:p003:L001` lm_history: 규칙기반에서 LLM까지 언어모델 발전사 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p003__lm_history.png`
- `DS_PDF09_LLM:p004:L001` embedding_encoder_decoder: embedding/encoder/decoder 기본 용어 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p004__embedding_encoder_decoder.png`
- `DS_PDF09_LLM:p007:L001` conditional_probability_lm: 조건부 확률 기반 언어모델 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p007__conditional_probability_lm.png`
- `DS_PDF09_LLM:p022:L001` nnlm_structure: NNLM 구조 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p022__nnlm_structure.png`
- `DS_PDF09_LLM:p035:L001` seq2seq: encoder-decoder seq2seq -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p035__seq2seq.png`
- `DS_PDF09_LLM:p037:L001` gpt_decoder: GPT decoder-only 다음 단어 예측 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p037__gpt_decoder.png`
- `DS_PDF09_LLM:p038:L001` large_language_model: Transformer 기반 LLM과 foundation model -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p038__large_language_model.png`
- `DS_PDF09_LLM:p039:L001` instruction_tuning: instruction tuning 예시 -> `dataScience/visual_raw/DS_PDF09_LLM/DS_PDF09_LLM_p039__instruction_tuning.png`

## Deep rawdata development by node

### 언어모델과 문장 확률

- 현재 노드: `n_DS_LLM.sequence_probability`
- 관련 파일: `DS_PDF09_LLM` / `DS_PDF07__language_models_llm__full_transcript.txt`
- 근거 anchor: `DS_PDF09_LLM:p007:L004` / `ev_DS_PDF09_LLM_001`
- 한 줄 정의: 언어모델은 단어/토큰 시퀀스의 가능도와 다음 토큰의 조건부 확률을 모델링한다.
- 쉬운 직관: 문장이 자연스럽게 이어질 가능성을 확률로 계산한다.
- 수식/절차: P(w1...wn)=product P(w_t | context)
- 데이터프레임 구조: row=document/sentence, column/token sequence or vectorized representation
- 코드 관점: tokenizer -> model logits -> softmax probabilities
- 강의 예제 연결: LLM PDF의 조건부 확률 페이지가 통계 Gate와 직접 연결된다.
- 자주 하는 실수: LLM이 검색엔진처럼 사실을 조회한다고 생각하고 확률 생성 구조를 무시하는 오류.
- 선행 노드: `n_DS_STATS.conditional_independence`
- 후속 노드: `n_DS_LLM.ngram_language_model`, `n_DS_LLM.attention_transformer`
- 유사 노드: -
- evidence snippet: 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)Language Model은 다음과 같이 조건부 확률을 활용하여 표현 가능단어 시퀀스 𝑊가 n개의 단어(𝑤!,𝑖=1,2,…,𝑛)들로 구성단어 시퀀스 𝑊가 등장할 확률은 아래와 같이 표현 가능
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### N-gram 통계적 언어모델

- 현재 노드: `n_DS_LLM.ngram_language_model`
- 관련 파일: `DS_PDF09_LLM` / `DS_PDF07__language_models_llm__full_transcript.txt`
- 근거 anchor: `DS_PDF09_LLM:p003:L005` / `ev_DS_PDF09_LLM_002`
- 한 줄 정의: 앞의 n-1개 단어를 조건으로 다음 단어 확률을 추정하는 통계적 언어모델이다.
- 쉬운 직관: 가까운 몇 단어만 보고 다음 단어를 예측하는 빈도 기반 모델이다.
- 수식/절차: P(w_t | w_{t-n+1},...,w_{t-1}) estimated from counts
- 데이터프레임 구조: 텍스트를 n-gram count table로 바꾼다.
- 코드 관점: CountVectorizer(ngram_range=...), frequency table
- 강의 예제 연결: 언어모델 발전사에서 통계적 언어모델이 신경망/Transformer 이전 단계로 제시된다.
- 자주 하는 실수: n이 커지면 항상 좋아진다고 보고 sparse data 문제를 무시하는 오류.
- 선행 노드: `n_DS_LLM.sequence_probability`, `n_DS_STATS.frequency_histogram`
- 후속 노드: `n_DS_LLM.embedding_contextual_representation`
- 유사 노드: -
- evidence snippet: ~1990: 통계적 언어모델Statistical Language ModelN-gram 등 단어의 빈도수를 기반으로 다음에 올 단어의 확률을 계산하는 방식
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Embedding과 문맥 표현

- 현재 노드: `n_DS_LLM.embedding_contextual_representation`
- 관련 파일: `DS_PDF09_LLM` / `DS_PDF07__language_models_llm__full_transcript.txt`
- 근거 anchor: `DS_PDF09_LLM:p004:L004` / `ev_DS_PDF09_LLM_003`
- 한 줄 정의: 토큰을 계산 가능한 연속 벡터로 바꾸고 문맥에 따라 의미 표현을 갱신하는 방식이다.
- 쉬운 직관: 단어를 좌표로 바꾸어 의미적으로 가까운 단어가 공간에서도 가까워지게 한다.
- 수식/절차: token -> embedding vector; contextual model updates representation with surrounding tokens
- 데이터프레임 구조: text row가 token sequence 또는 embedding matrix로 변환된다.
- 코드 관점: Embedding layer, tokenizer, transformer hidden states
- 강의 예제 연결: LLM PDF의 embedding/encoder/decoder 용어 페이지가 ML1 text vectorization의 후속이다.
- 자주 하는 실수: embedding을 사람이 정한 사전 코드처럼 고정 의미로 보는 오류.
- 선행 노드: `n_DS_ML1.text_vectorization_features`
- 후속 노드: `n_DS_LLM.attention_transformer`, `n_DS_ML3.kmeans_distance_metrics`
- 유사 노드: -
- evidence snippet: 언어모델 (Language Model, LM)기본 개념과 용어•임베딩Embedding- 단어(토큰)를 모델이 계산할 수 있는연속적인 벡터 공간 표현으로 변환하는 단계- 의미적으로 유사한 단어들이벡터 공간에서도 가깝게 위치하도록 학습
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Encoder/Decoder와 Seq2Seq

- 현재 노드: `n_DS_LLM.encoder_decoder_seq2seq`
- 관련 파일: `DS_PDF09_LLM` / `DS_PDF07__language_models_llm__full_transcript.txt`
- 근거 anchor: `DS_PDF09_LLM:p003:L007` / `ev_DS_PDF09_LLM_004`
- 한 줄 정의: 입력 시퀀스를 표현으로 압축하는 encoder와 출력 시퀀스를 생성하는 decoder를 결합한 구조다.
- 쉬운 직관: 문장을 이해하는 쪽과 문장을 내보내는 쪽을 나눈 번역기 구조다.
- 수식/절차: encoder(input sequence)->context representation; decoder(context)->output sequence
- 데이터프레임 구조: 입력 텍스트와 출력 텍스트가 paired rows로 구성된다.
- 코드 관점: seq2seq model, encoder outputs, decoder generation
- 강의 예제 연결: Seq2Seq 페이지는 길이가 다른 입력/출력 시퀀스 처리 구조를 설명한다.
- 자주 하는 실수: encoder/decoder를 단순 전처리/후처리 함수로만 보는 오류.
- 선행 노드: `n_DS_LLM.embedding_contextual_representation`
- 후속 노드: `n_DS_LLM.attention_transformer`
- 유사 노드: -
- evidence snippet: 2013~16: 시퀀스 모델링Recurrent Neural Network (RNN)Long Short-Term Memory(LSTM)Sequence to Sequence (Seq2Seq)**문장을 시퀀스 단위로 학습, 장기 의존성 개선 시도
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Attention과 Transformer

- 현재 노드: `n_DS_LLM.attention_transformer`
- 관련 파일: `DS_PDF09_LLM` / `DS_PDF07__language_models_llm__full_transcript.txt`
- 근거 anchor: `DS_PDF09_LLM:p038:L004` / `ev_DS_PDF09_LLM_005`
- 한 줄 정의: attention은 토큰들이 서로 얼마나 참고해야 하는지 가중치를 계산하고, Transformer는 recurrence 없이 attention 중심으로 시퀀스를 처리한다.
- 쉬운 직관: 문장 안 모든 단어가 서로를 보며 중요한 연결에 집중하게 하는 구조다.
- 수식/절차: Attention(Q,K,V)=softmax(QK^T/sqrt(d_k))V
- 데이터프레임 구조: token sequence가 Q/K/V 행렬과 hidden states로 변환된다.
- 코드 관점: Transformer encoder/decoder, multi-head self-attention
- 강의 예제 연결: LLM PDF는 Transformer가 self-attention 기반 LLM의 근간이라고 연결한다.
- 자주 하는 실수: attention weight를 곧바로 인간적 설명 또는 인과로 단정하는 오류.
- 선행 노드: `n_DS_LLM.encoder_decoder_seq2seq`
- 후속 노드: `n_DS_LLM.bert_gpt_pretraining`, `n_DS_LLM.foundation_instruction_tuning`
- 유사 노드: -
- evidence snippet: 대형언어모델 (Large Language Model, LLM)Large Language Model- LLM은 Transformer 계열(특히 self-attention)을 기반으로, 방대한 텍스트(및 경우에 따라 코드·이미지·표 등)를 이용해대규모 사전학습(pre-training)을 수행- 언어를 넘어 다양한 작업을...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### BERT/GPT와 사전학습

- 현재 노드: `n_DS_LLM.bert_gpt_pretraining`
- 관련 파일: `DS_PDF09_LLM` / `DS_PDF07__language_models_llm__full_transcript.txt`
- 근거 anchor: `DS_PDF09_LLM:p037:L004` / `ev_DS_PDF09_LLM_006`
- 한 줄 정의: BERT는 encoder 계열 양방향 문맥 표현, GPT는 decoder 계열 다음 토큰 생성을 중심으로 한 Transformer 사전학습 모델이다.
- 쉬운 직관: 많은 텍스트로 먼저 언어 패턴을 익히고, 이후 작업별로 조정한다.
- 수식/절차: pre-train on large corpus -> fine-tune or prompt for downstream task
- 데이터프레임 구조: 문서 corpus rows가 토큰 시퀀스 학습 데이터가 된다.
- 코드 관점: BERT encoder, GPT decoder, pretraining/fine-tuning
- 강의 예제 연결: LLM PDF의 BERT/GPT 발전사와 GPT decoder 페이지가 이 대비를 제공한다.
- 자주 하는 실수: BERT와 GPT를 같은 생성 모델로만 묶거나 encoder/decoder 차이를 지우는 오류.
- 선행 노드: `n_DS_LLM.attention_transformer`
- 후속 노드: `n_DS_LLM.foundation_instruction_tuning`
- 유사 노드: -
- evidence snippet: 언어모델 (Language Model, LM)Generative Pre-trained Transformer, GPT-트랜스포머의디코더(Decoder)구조를 사용-문장을 한 방향(Unidirectional)으로 읽으며 다음에 올 단어를 예측
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### Foundation model과 instruction tuning

- 현재 노드: `n_DS_LLM.foundation_instruction_tuning`
- 관련 파일: `DS_PDF09_LLM` / `DS_PDF07__language_models_llm__full_transcript.txt`
- 근거 anchor: `DS_PDF09_LLM:p039:L005` / `ev_DS_PDF09_LLM_007`
- 한 줄 정의: Foundation model은 대규모 사전학습 기반 범용 모델이고, instruction tuning은 지시를 이해하고 수행하도록 추가 학습하는 절차다.
- 쉬운 직관: 문장 생성기가 사용자의 지시를 따르는 작업 수행자로 바뀌는 단계다.
- 수식/절차: pretrained LM -> supervised instruction data/RLHF preference optimization -> aligned assistant behavior
- 데이터프레임 구조: prompt/input/response가 학습·평가 단위가 된다.
- 코드 관점: instruction dataset, supervised fine-tuning, preference/RLHF pipeline
- 강의 예제 연결: LLM PDF의 instruction tuning 예시는 Translate instruction을 명시적으로 따른다.
- 자주 하는 실수: instruction tuning이 factual grounding을 자동 보장한다고 보는 오류.
- 선행 노드: `n_DS_LLM.bert_gpt_pretraining`
- 후속 노드: `n_DS_LLM.rag_grounding`
- 유사 노드: -
- evidence snippet: 예) 기존 언어 모델Input: “Translate the following sentence into ______”Output: ”Korean”LLM –instruction tuningInstruction:Translate the following sentence into Korean.Input:Machine lea...
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?

### RAG와 근거 기반 튜터링

- 현재 노드: `n_DS_LLM.rag_grounding`
- 관련 파일: `DS_PDF09_LLM` / `DS_PDF07__language_models_llm__full_transcript.txt`
- 근거 anchor: `WEB:web_rag_2020` / `ev_DS_PDF09_LLM_008`
- 한 줄 정의: RAG는 모델의 생성 능력에 외부 검색 근거를 결합해 답변의 출처성, 갱신성, 검증 가능성을 높이는 설계다.
- 쉬운 직관: 머릿속 기억만 말하지 않고 책장을 찾아 근거를 붙여 대답하게 하는 구조다.
- 수식/절차: query -> retrieve source chunks -> rerank/route -> generate with citations -> verify
- 데이터프레임 구조: 문서 chunk table, embedding index, metadata/source anchors가 필요하다.
- 코드 관점: vector store, hybrid retrieval, reranker, source trace table
- 강의 예제 연결: 이번 DS flat-pack 자체가 PDF 전사와 웹 근거를 결합한 로컬 RAG 소스다.
- 자주 하는 실수: 검색 결과가 있으면 답이 무조건 맞다고 보거나, PDF 근거와 웹 보강을 섞어 출처 우선순위를 잃는 오류.
- 선행 노드: `n_DS_LLM.foundation_instruction_tuning`, `n_DS_ML3.support_confidence_lift`
- 후속 노드: `n_DS_GLOBAL.tutor_operating_modes`
- 유사 노드: -
- evidence snippet: 강의 PDF 전사에서 직접 키워드가 약해 `web_rag_2020`를 확장 근거로 사용: RAG as parametric model plus non-parametric retrieval memory.
- 확인 질문: 이 노드를 현실 언어, 수식/절차 언어, pandas/sklearn 언어로 각각 설명할 수 있는가?
