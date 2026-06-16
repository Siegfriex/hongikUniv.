# DS_PDF09_LLM — annotated PDF transcript

- title: DS09 언어모델과 LLM
- source_pdf: `dataScience/pdf_raw/[Lecture][DS][09]언어모델과 LLM.pdf`
- transcript: `dataScience/txt_raw/DS_PDF07__language_models_llm__full_transcript.txt`

## PAGE 001

- `DS_PDF09_LLM:p001:L001` 언어모델과 LLM[140316]DATA SCIENCE
- `DS_PDF09_LLM:p001:L002` HunsikShinDepartment of Industrial and Data Engineering{hunsik.shin}@hongik.ac.kr

## PAGE 002

- `DS_PDF09_LLM:p002:L001` 제목
- `DS_PDF09_LLM:p002:L002` 2
- `DS_PDF09_LLM:p002:L003` 제목
- `DS_PDF09_LLM:p002:L004` 언어모델 (Language Model, LM)왜 언어 모델이 필요한가?
- `DS_PDF09_LLM:p002:L005` "참 데이터사이언스 산업·데이터공학과에서 홍익대학교 수업은 재밌다."
- `DS_PDF09_LLM:p002:L006` ＂수업은 홍익대학교 재밌다 참 산업·데이터공학과에서 데이터사이언스”
- `DS_PDF09_LLM:p002:L007` ＂홍익대학교 산업·데이터공학과에서 데이터사이언스 수업은 참재밌다”

## PAGE 003

- `DS_PDF09_LLM:p003:L001` 제목
- `DS_PDF09_LLM:p003:L002` 3
- `DS_PDF09_LLM:p003:L003` 제목
- `DS_PDF09_LLM:p003:L004` 언어모델 (Language Model, LM)언어모델의 발전~1980: 규칙기반 시스템Rule-based System인간이 정의한 문법 규칙과 사전 정의된 로직에 의존
- `DS_PDF09_LLM:p003:L005` ~1990: 통계적 언어모델Statistical Language ModelN-gram 등 단어의 빈도수를 기반으로 다음에 올 단어의 확률을 계산하는 방식
- `DS_PDF09_LLM:p003:L006` 2003: 신경망기반 언어모델Neural Network Language Model*단어를 고정된 차원의 벡터로 표현하는'단어 임베딩'개념을 도입
- `DS_PDF09_LLM:p003:L007` 2013~16: 시퀀스 모델링Recurrent Neural Network (RNN)Long Short-Term Memory(LSTM)Sequence to Sequence (Seq2Seq)**문장을 시퀀스 단위로 학습, 장기 의존성 개선 시도
- `DS_PDF09_LLM:p003:L008` 2017: Transformer*** 혁명현재 모든 LLM의 근간기존 RNN의 순차적 처리 방식에서 벗어나,Attention 메커니즘을 통해 문장 내 모든 단어 간의 관계를 동시에 파악하고 병렬 처리를 가능
- `DS_PDF09_LLM:p003:L009` 2018~20: 사전 학습모델BERT****GPT*****방대한 텍스트 데이터를 먼저 학습시킨 후 특정 작업에 맞게 조정하는 방식
- `DS_PDF09_LLM:p003:L010` 2023~: LLM 등장 및 대중화
- `DS_PDF09_LLM:p003:L011` GPT-4, LLaMA(Meta) 등 파라미터가 수천억 개에 달하는 거대 언어 모델들이 등장
- `DS_PDF09_LLM:p003:L012` * Bengio, Y., Ducharme, R., Vincent, P., & Jauvin, C. (2003). A neural probabilistic language model.Journal of machine learning research,3(Feb), 1137-1155.** Sutskever, I., Vinyals, O., & Le, Q. V. (2014). Sequence to sequence learning with neural networks.Advances in neural information processing systems,27..*** Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need.Advances in neural information processing systems,30****Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019, June). Bert: Pre-training of deep bidirectional transformers for language understanding. InProceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)(pp. 4171-4186).***** Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). Language models are few-shot learners.Advances in neural information processing systems,33, 1877-1901.

## PAGE 004

- `DS_PDF09_LLM:p004:L001` 제목
- `DS_PDF09_LLM:p004:L002` 4
- `DS_PDF09_LLM:p004:L003` 제목
- `DS_PDF09_LLM:p004:L004` 언어모델 (Language Model, LM)기본 개념과 용어•임베딩Embedding- 단어(토큰)를 모델이 계산할 수 있는연속적인 벡터 공간 표현으로 변환하는 단계- 의미적으로 유사한 단어들이벡터 공간에서도 가깝게 위치하도록 학습
- `DS_PDF09_LLM:p004:L005` •Encoder- 입력 문장을 받아 각 토큰을문맥을 반영한 표현(contextual representation)으로 변환-  문장의 의미를이해하고 요약된 상태 표현으로 압축하는 역할
- `DS_PDF09_LLM:p004:L006` •Decoder- 이전까지 생성된 토큰과 입력 정보를 바탕으로다음 토큰을 순차적으로 생성- 언어모델에서는 확률적으로가장 적절한 출력 문장을 만들어내는 생성기역할
- `DS_PDF09_LLM:p004:L007` •Attention- 문장 내에서어떤 토큰이 다른 토큰을 볼지 가중치를 학습하는 메커니즘- 거리와 상관없이중요한 단어들에 직접 집중해 문맥 의존성을 효과적으로 모델

## PAGE 005

- `DS_PDF09_LLM:p005:L001` 제목
- `DS_PDF09_LLM:p005:L002` 5
- `DS_PDF09_LLM:p005:L003` 제목
- `DS_PDF09_LLM:p005:L004` 언어모델 (Language Model, LM)언어모델(Language Model) 이란?문장 또는 단어 시퀀스가 나타날 확률을 계산하는 모델주어진 단어들의 등장 확률을 기반으로, 자연스러운 문장을 생성하거나 다음 단어를 예측하는 모델목표: 기계에게 많은 말뭉치를 훈련시켜서 언어 모델을 통해 현실에서의 확률 분포를 근사하는 것1. P(w₁, w₂, …, wₙ)—문장 전체의 확률 계산2. P(wₙ| w₁, …, wₙ₋₁)—이전 단어들을 보고 다음 단어의 확률 예측à확률을 통해 자연스러운 문장 생성 가능
- `DS_PDF09_LLM:p005:L005` 기계 번역 (Machine Translation)-P[‘나는 버스를 탔다’ | ‘I took the bus’] > P[‘나는 버스를 탄다’ | ‘I took the bus’]
- `DS_PDF09_LLM:p005:L006` 오타-띄어쓰기 교정 (Spell & Space Correction)-P[‘아버지가 방에 들어가신다’ | ‘아버지가방에들어가신다’] > P[‘아버지 가방에 들어가신다’ | ‘아버지가방에들어가신다’]

## PAGE 006

- `DS_PDF09_LLM:p006:L001` 제목
- `DS_PDF09_LLM:p006:L002` 6
- `DS_PDF09_LLM:p006:L003` 제목
- `DS_PDF09_LLM:p006:L004` 언어모델 (Language Model, LM)언어모델(Language Model) 이란?문장 또는 단어 시퀀스가 나타날 확률을 계산하는 모델à전체 말뭉치에서 문장을 구성하는 단어들이 등장한 확률을 통해 문장의 확률을 계산
- `DS_PDF09_LLM:p006:L005` P[‘나는 버스를 탔다’] = P[‘나는’, ‘버스를’, ‘탔다’]
- `DS_PDF09_LLM:p006:L006` Mathematical Form문서 = 단어 시퀀스 𝑊가 n개의 단어(𝑤!,𝑖=1,2,…,𝑛)들로 구성단어 시퀀스 𝑊가 등장할 확률은 아래와 같이 표현 가능𝑃(𝑊)=𝑃(𝑤",𝑤#,…,𝑤$)

## PAGE 007

- `DS_PDF09_LLM:p007:L001` 제목
- `DS_PDF09_LLM:p007:L002` 7
- `DS_PDF09_LLM:p007:L003` 제목
- `DS_PDF09_LLM:p007:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)Language Model은 다음과 같이 조건부 확률을 활용하여 표현 가능단어 시퀀스 𝑊가 n개의 단어(𝑤!,𝑖=1,2,…,𝑛)들로 구성단어 시퀀스 𝑊가 등장할 확률은 아래와 같이 표현 가능
- `DS_PDF09_LLM:p007:L005` 𝑃(𝑊)=𝑃(𝑤!,𝑤",…,𝑤#)=𝑃𝑤"%&!,&"%&!%&!,&",&#%&!,&"···%&!,&",&#,···&$%&!,&",&#,···&$%!=𝑃𝑤!𝑃𝑤"𝑤!𝑃𝑤$𝑤!,𝑤"···𝑃𝑤#𝑤!,…,𝑤#%!=∏&'!#𝑃𝑤&|𝑤!,𝑤",···𝑤&%!
- `DS_PDF09_LLM:p007:L006` 1)P(“학다홍 수업 터산다익업 참 교인과에 데·이서공재학는사트”)2)P(“수업은 산업 참 데이터공학과에서 홍익대학교 데이터사이언스재밌다”)3)P(“홍익대학교 산업·데이터공학과에서 데이터사이언스 수업은 참재밌다.”)

## PAGE 008

- `DS_PDF09_LLM:p008:L001` 제목
- `DS_PDF09_LLM:p008:L002` 8
- `DS_PDF09_LLM:p008:L003` 제목
- `DS_PDF09_LLM:p008:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)이전 단어들이 주어졌을 때, 다음 단어를 예측하는 방법 à Next Token Prediction (NTP)주어진 단어들로부터 그 다음에 올 단어에 대한 확률을 계산 à 가장 높은 확률에 해당하는 단어 선택
- `DS_PDF09_LLM:p008:L005` 예시

## PAGE 009

- `DS_PDF09_LLM:p009:L001` 제목
- `DS_PDF09_LLM:p009:L002` 9
- `DS_PDF09_LLM:p009:L003` 제목
- `DS_PDF09_LLM:p009:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)이전 단어들이 주어졌을 때, 다음 단어를 예측하는 방법 à Next Token Prediction (NTP)주어진 단어들로부터 그 다음에 올 단어에 대한 확률을 계산 à 가장 높은 확률에 해당하는 단어 선택
- `DS_PDF09_LLM:p009:L005` 예시

## PAGE 010

- `DS_PDF09_LLM:p010:L001` 제목
- `DS_PDF09_LLM:p010:L002` 10
- `DS_PDF09_LLM:p010:L003` 제목
- `DS_PDF09_LLM:p010:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)이전 단어들이 주어졌을 때, 다음 단어를 예측하는 방법 à Next Token Prediction (NTP)주어진 단어들로부터 그 다음에 올 단어에 대한 확률을 계산 à 가장 높은 확률에 해당하는 단어 선택
- `DS_PDF09_LLM:p010:L005` 예시

## PAGE 011

- `DS_PDF09_LLM:p011:L001` 제목
- `DS_PDF09_LLM:p011:L002` 11
- `DS_PDF09_LLM:p011:L003` 제목
- `DS_PDF09_LLM:p011:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)이전 단어들이 주어졌을 때, 다음 단어를 예측하는 방법 à Next Token Prediction (NTP)주어진 단어들로부터 그 다음에 올 단어에 대한 확률을 계산 à 가장 높은 확률에 해당하는 단어 선택
- `DS_PDF09_LLM:p011:L005` 예시

## PAGE 012

- `DS_PDF09_LLM:p012:L001` 제목
- `DS_PDF09_LLM:p012:L002` 12
- `DS_PDF09_LLM:p012:L003` 제목
- `DS_PDF09_LLM:p012:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)각각의 조건부 확률을 빈도(Count) 기반으로 부여: co-occurrence와 frequency
- `DS_PDF09_LLM:p012:L005` 예) 특정 말뭉치(Corpus)에서 ’나는 버스를’ 뒤에 ‘탔다’가 총 50번 등장 했고, ‘나는 버스를’가 100번 등장했다면?à P(‘탔다’ | ＇나는 버스를’) = P(‘나는 버스를 탔다’ | ’나는 버스를’) = 0.5

## PAGE 013

- `DS_PDF09_LLM:p013:L001` 제목
- `DS_PDF09_LLM:p013:L002` 13
- `DS_PDF09_LLM:p013:L003` 제목
- `DS_PDF09_LLM:p013:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)언어모델의 목표기계에게 많은 말뭉치를 훈련시켜서 언어 모델을 통해 현실에서의 확률 분포를 근사하는 것count기반으로 확률을 잘 부여하려면 매우 방대한 양의 말뭉치가 필요예시) 학습한 Corpus에 ‘나는 버스를 탔다’라는 문장이 없으면, 이 확률은 0이 됨충분하지 않은 말뭉치로 인한 낮은 확률에 해당하는 문장이 잘못된 문장은 아닐 수있음
- `DS_PDF09_LLM:p013:L005` Sparsity Problem (희소 문제)충분한 데이터를 관측하지 못하여 언어를 정확히 모델링하지 못하는 문제완화하는 방법으로 n-gram language 모델이 활용됨

## PAGE 014

- `DS_PDF09_LLM:p014:L001` 제목
- `DS_PDF09_LLM:p014:L002` 14
- `DS_PDF09_LLM:p014:L003` 제목
- `DS_PDF09_LLM:p014:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)Sparsity Problem (희소 문제)충분한 데이터를 관측하지 못하여 언어를 정확히 모델링하지 못하는 문제완화하는 방법으로 n-gram language 모델이 활용됨

## PAGE 015

- `DS_PDF09_LLM:p015:L001` 제목
- `DS_PDF09_LLM:p015:L002` 15
- `DS_PDF09_LLM:p015:L003` 제목
- `DS_PDF09_LLM:p015:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)Sparsity Problem (희소 문제)충분한 데이터를 관측하지 못하여 언어를 정확히 모델링하지 못하는 문제완화하는 방법으로 n-gram language 모델이 활용됨

## PAGE 016

- `DS_PDF09_LLM:p016:L001` 제목
- `DS_PDF09_LLM:p016:L002` 16
- `DS_PDF09_LLM:p016:L003` 제목
- `DS_PDF09_LLM:p016:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)Sparsity Problem (희소 문제)충분한 데이터를 관측하지 못하여 언어를 정확히 모델링하지 못하는 문제완화하는 방법으로 n-gram language 모델이 활용됨

## PAGE 017

- `DS_PDF09_LLM:p017:L001` 제목
- `DS_PDF09_LLM:p017:L002` 17
- `DS_PDF09_LLM:p017:L003` 제목
- `DS_PDF09_LLM:p017:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)Sparsity Problem (희소 문제)충분한 데이터를 관측하지 못하여 언어를 정확히 모델링하지 못하는 문제완화하는 방법으로 n-gram language 모델이 활용됨

## PAGE 018

- `DS_PDF09_LLM:p018:L001` 제목
- `DS_PDF09_LLM:p018:L002` 18
- `DS_PDF09_LLM:p018:L003` 제목
- `DS_PDF09_LLM:p018:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)Sparsity Problem (희소 문제)충분한 데이터를 관측하지 못하여 언어를 정확히 모델링하지 못하는 문제완화하는 방법으로 n-gram language 모델이 활용됨

## PAGE 019

- `DS_PDF09_LLM:p019:L001` 제목
- `DS_PDF09_LLM:p019:L002` 19
- `DS_PDF09_LLM:p019:L003` 제목
- `DS_PDF09_LLM:p019:L004` 언어모델 (Language Model, LM)Statistical Language Model(통계적 언어 모델, SLM)Sparsity Problem (희소 문제)충분한 데이터를 관측하지 못하여 언어를 정확히 모델링하지 못하는 문제완화하는 방법으로 n-gram language 모델이 활용됨

## PAGE 020

- `DS_PDF09_LLM:p020:L001` 제목
- `DS_PDF09_LLM:p020:L002` 20
- `DS_PDF09_LLM:p020:L003` 제목
- `DS_PDF09_LLM:p020:L004` 언어모델 (Language Model, LM)Neural Network Language Model(NNLM)
- `DS_PDF09_LLM:p020:L005` 배경- 당시 주류였던 N-gram모델 (통계적 언어 모델) 은 단어의 빈도수를 기반으로 확률을 계산à 학습 데이터에 없는 단어 조합이 나오면 확률이 0이 되는 '희소 문제(Sparsity Problem)’가 발생
- `DS_PDF09_LLM:p020:L006` - N-gram은 '강아지'와 '개'가 의미적으로 유사하다는 것을 알지 못하고 완전히 다른 단어로 취급 단어 유사성 고려 X)

## PAGE 021

- `DS_PDF09_LLM:p021:L001` 제목
- `DS_PDF09_LLM:p021:L002` 21
- `DS_PDF09_LLM:p021:L003` 제목
- `DS_PDF09_LLM:p021:L004` 언어모델 (Language Model, LM)Neural Network Language Model(NNLM)
- `DS_PDF09_LLM:p021:L005` •핵심 아이디어-신경망을 통한 확률 예측:이전 단어들의 벡터를 신경망의 입력으로 넣어, 다음에 올 단어의 확률을 계산- 단어의 분산 표현 (Distributed Representation):단어를 단순히 숫자로 세는 것이 아니라, 다차원 공간상의 밀집 벡터(Dense Vector)로 표현. à의미가 비슷한 단어들은 벡터 공간에서 가까이 위치 (현재의Word Embedding모태)
- `DS_PDF09_LLM:p021:L006` * https://suriyadeepan.github.io/
- `DS_PDF09_LLM:p021:L007` Word vector space 예시Neural Network를 통한 확률 예측예시

## PAGE 022

- `DS_PDF09_LLM:p022:L001` 제목
- `DS_PDF09_LLM:p022:L002` 22
- `DS_PDF09_LLM:p022:L003` 제목
- `DS_PDF09_LLM:p022:L004` 언어모델 (Language Model, LM)Neural Network Language Model(NNLM)
- `DS_PDF09_LLM:p022:L005` 모델 구조1. Input Layer:예측하려는 단어(𝑤𝑜𝑟𝑑() 앞의n−1개 단어들((𝑤𝑜𝑟𝑑(%!,…,𝑤𝑜𝑟𝑑(%#)!) 을 입력2. Projection Layer (C):각 단어를 미리 정의된 크기(m차원)의 벡터로 변환(Look-up table을 이용한 Embedding) à모든 단어는 동일한 행렬C를 공유하여 벡터화3. Hidden Layer:변환된 벡터들을 하나로 이어 붙여(Concatenate) 비선형 활성화 함수(주로tanh)를 통과à단어 간의 복잡한 관계(=비선형 관계)를 학습4. Output Layer:Softmax함수를 사용하여 전체 단어 집합(Vocabulary) 중 어떤 단어가 올지 확률 분포로 출력

## PAGE 023

- `DS_PDF09_LLM:p023:L001` 제목
- `DS_PDF09_LLM:p023:L002` 23
- `DS_PDF09_LLM:p023:L003` 제목
- `DS_PDF09_LLM:p023:L004` 언어모델 (Language Model, LM)Neural Network Language Model(NNLM)
- `DS_PDF09_LLM:p023:L005` 𝑤𝑜𝑟𝑑!"#
- `DS_PDF09_LLM:p023:L006` 𝑤𝑜𝑟𝑑!"$
- `DS_PDF09_LLM:p023:L007` 𝑤𝑜𝑟𝑑!"%
- `DS_PDF09_LLM:p023:L008` 𝑤𝑜𝑟𝑑!"&
- `DS_PDF09_LLM:p023:L009` 𝑤𝑜𝑟𝑑!"'
- `DS_PDF09_LLM:p023:L010` ＂A young girl plays with __?__” à[Language Model] à“dog”𝑤𝑜𝑟𝑑!"#𝑤𝑜𝑟𝑑!"$ 𝑤𝑜𝑟𝑑!"'… 𝑤𝑜𝑟𝑑!

## PAGE 024

- `DS_PDF09_LLM:p024:L001` 제목
- `DS_PDF09_LLM:p024:L002` 24
- `DS_PDF09_LLM:p024:L003` 제목
- `DS_PDF09_LLM:p024:L004` 언어모델 (Language Model, LM)Distributed Representation –Word2Vec (Mikolovet al., 2013)Distributed Representation은 의미적으로 유사한 단어가벡터 공간에서 가까운 위치에 놓이도록 학습하는 방법
- `DS_PDF09_LLM:p024:L005` 2
- `DS_PDF09_LLM:p024:L006` Learning model –prediction of target word

## PAGE 025

- `DS_PDF09_LLM:p025:L001` 제목
- `DS_PDF09_LLM:p025:L002` 25
- `DS_PDF09_LLM:p025:L003` 제목
- `DS_PDF09_LLM:p025:L004` 언어모델 (Language Model, LM)Distributed Representation –Word2Vec (Mikolovet al., 2013)Distributed Representation은 의미적으로 유사한 단어가벡터 공간에서 가까운 위치에 놓이도록 학습하는 방법
- `DS_PDF09_LLM:p025:L005` 2
- `DS_PDF09_LLM:p025:L006` Learning model –prediction of target word

## PAGE 026

- `DS_PDF09_LLM:p026:L001` 제목
- `DS_PDF09_LLM:p026:L002` 26
- `DS_PDF09_LLM:p026:L003` 제목
- `DS_PDF09_LLM:p026:L004` 언어모델 (Language Model, LM)Distributed Representation –Word2Vec (Mikolovet al., 2013)Distributed Representation은 의미적으로 유사한 단어가벡터 공간에서 가까운 위치에 놓이도록 학습하는 방법
- `DS_PDF09_LLM:p026:L005` 2
- `DS_PDF09_LLM:p026:L006` Learning model –prediction of target word

## PAGE 027

- `DS_PDF09_LLM:p027:L001` 제목
- `DS_PDF09_LLM:p027:L002` 27
- `DS_PDF09_LLM:p027:L003` 제목
- `DS_PDF09_LLM:p027:L004` 언어모델 (Language Model, LM)Distributed Representation –Word2Vec (Mikolovet al., 2013)Distributed Representation은 의미적으로 유사한 단어가벡터 공간에서 가까운 위치에 놓이도록 학습하는 방법
- `DS_PDF09_LLM:p027:L005` 2
- `DS_PDF09_LLM:p027:L006` Learning model –prediction of target word

## PAGE 028

- `DS_PDF09_LLM:p028:L001` 제목
- `DS_PDF09_LLM:p028:L002` 28
- `DS_PDF09_LLM:p028:L003` 제목
- `DS_PDF09_LLM:p028:L004` 언어모델 (Language Model, LM)Distributed Representation –Word2Vec (Mikolovet al., 2013)Distributed Representation은 의미적으로 유사한 단어가벡터 공간에서 가까운 위치에 놓이도록 학습하는 방법
- `DS_PDF09_LLM:p028:L005` 2
- `DS_PDF09_LLM:p028:L006` Learning model –prediction of target word

## PAGE 029

- `DS_PDF09_LLM:p029:L001` 제목
- `DS_PDF09_LLM:p029:L002` 29
- `DS_PDF09_LLM:p029:L003` 제목
- `DS_PDF09_LLM:p029:L004` 언어모델 (Language Model, LM)Distributed Representation –Word2Vec (Mikolovet al., 2013)Distributed Representation은 의미적으로 유사한 단어가벡터 공간에서 가까운 위치에 놓이도록 학습하는 방법
- `DS_PDF09_LLM:p029:L005` 2
- `DS_PDF09_LLM:p029:L006` Learning model –prediction of target word

## PAGE 030

- `DS_PDF09_LLM:p030:L001` 제목
- `DS_PDF09_LLM:p030:L002` 30
- `DS_PDF09_LLM:p030:L003` 제목
- `DS_PDF09_LLM:p030:L004` 언어모델 (Language Model, LM)Distributed Representation –Word2Vec (Mikolovet al., 2013)Distributed Representation은 의미적으로 유사한 단어가벡터 공간에서 가까운 위치에 놓이도록 학습하는 방법
- `DS_PDF09_LLM:p030:L005` 2
- `DS_PDF09_LLM:p030:L006` Learning model –prediction of target word

## PAGE 031

- `DS_PDF09_LLM:p031:L001` 제목
- `DS_PDF09_LLM:p031:L002` 31
- `DS_PDF09_LLM:p031:L003` 제목
- `DS_PDF09_LLM:p031:L004` 언어모델 (Language Model, LM)Distributed Representation –Word2Vec (Mikolovet al., 2013)Distributed Representation은 의미적으로 유사한 단어가벡터 공간에서 가까운 위치에 놓이도록 학습하는 방법
- `DS_PDF09_LLM:p031:L005` 2
- `DS_PDF09_LLM:p031:L006` Learning model –prediction of target word

## PAGE 032

- `DS_PDF09_LLM:p032:L001` 제목
- `DS_PDF09_LLM:p032:L002` 32
- `DS_PDF09_LLM:p032:L003` 제목
- `DS_PDF09_LLM:p032:L004` 언어모델 (Language Model, LM)Recurrent Neural Network언어 모델은 문장 내에서 단어의 순서에 확률을 할당하는 모델à 이전까지 등장한 단어들(𝑤!, 𝑤", ... , 𝑤(%!)이 주어졌을 때, 다음에 올 단어𝑤(예측
- `DS_PDF09_LLM:p032:L005` 배경전통적인 통계적 언어 모델(N-gram)이나 일반적인 Feed-forward 신경망은 고정된 길이의 입력만 처리할 수 있다는 한계문장은 길이가 제각각 다른 경우 처리할 수 있는 방안 필요
- `DS_PDF09_LLM:p032:L006` 모델 : ℎ(=tanh(𝑊**ℎ(%!𝑊*+𝑥(+𝑏*)•𝑥": 현재 시점의 단어 벡터 (Embedding)•ℎ"#$: 이전 시점까지의 맥락을 담고 있는 은닉 상태 (Hidden State)•𝑊: 학습해야 할 가중치 매개변수•ℎ": 현재까지의 정보를 업데이트한 새로운 은닉 상태 <RNN 구조>

## PAGE 033

- `DS_PDF09_LLM:p033:L001` 제목
- `DS_PDF09_LLM:p033:L002` 33
- `DS_PDF09_LLM:p033:L003` 제목
- `DS_PDF09_LLM:p033:L004` 언어모델 (Language Model, LM)Recurrent Neural Network

## PAGE 034

- `DS_PDF09_LLM:p034:L001` 제목
- `DS_PDF09_LLM:p034:L002` 34
- `DS_PDF09_LLM:p034:L003` 제목
- `DS_PDF09_LLM:p034:L004` 언어모델 (Language Model, LM)Long Short-Term Memory배경RNN 모델의 장기 의존성 문제를 해결하기 위해 등장Cell State'라는 통로를 추가하여, 어떤 정보를 장기적으로 유지할지(Forget gate, Input gate) 정교하게 제어•Gate의 역할-forget gate : 과거 정보를 얼마나 유지할 것인지?-input gate : 새로 입력된 정보는 얼만큼 활용할 것인지?-output gate : 두 정보를 계산하여 나온 출력 정보를 얼마만큼 넘겨줄 것인지?- cell-state: 역전파 과정에서 활성화 함수를 거치지 않아 정보 손실이 없기 때문에 뒷 쪽 시퀀스와 앞쪽 시퀀스의 정보를 모두 가지고 있음

## PAGE 035

- `DS_PDF09_LLM:p035:L001` 제목
- `DS_PDF09_LLM:p035:L002` 35
- `DS_PDF09_LLM:p035:L003` 제목
- `DS_PDF09_LLM:p035:L004` 언어모델 (Language Model, LM)•Sequence to Sequence Model (Seq2Seq)- 길이가 다른 입력 시퀀스를 받아, 또 다른 시퀀스를 출력하는 모델 구조
- `DS_PDF09_LLM:p035:L005` - Encoder입력 문장을한 단어씩 순서대로 읽음• 보통 RNN / LSTM 사용• 마지막 hidden state가 입력 전체의 요약à 요약 벡터를Context Vector라고 부름
- `DS_PDF09_LLM:p035:L006` - Decoder (출력 생성)• Context Vector를 받아서 단어를하나씩 생성• 이전에 생성한 단어를 다시 입력으로 사용

## PAGE 036

- `DS_PDF09_LLM:p036:L001` 제목
- `DS_PDF09_LLM:p036:L002` 36
- `DS_PDF09_LLM:p036:L003` 제목
- `DS_PDF09_LLM:p036:L004` 언어모델 (Language Model, LM)Transformer-인코더에서 입력 시퀀스를 입력받고, 디코더에서 출력 시퀀스를 출력-인코더와 디코더라는 단위가 N개로 구성되는 구조-트랜스포머를 제안한 논문에서는 인코더와 디코더의 개수를 각각 6개 사용#멀티 헤드 어텐션, #셀프 어텐션
- `DS_PDF09_LLM:p036:L005` * https://wikidocs.net/31379

## PAGE 037

- `DS_PDF09_LLM:p037:L001` 제목
- `DS_PDF09_LLM:p037:L002` 37
- `DS_PDF09_LLM:p037:L003` 제목
- `DS_PDF09_LLM:p037:L004` 언어모델 (Language Model, LM)Generative Pre-trained Transformer, GPT-트랜스포머의디코더(Decoder)구조를 사용-문장을 한 방향(Unidirectional)으로 읽으며 다음에 올 단어를 예측
- `DS_PDF09_LLM:p037:L005` 학습 방식- 이전 단어들을 보고 다음 단어를 생성하는 'Causal Language Modeling' 방식- 문장의 흐름이 자연스럽고 창의적인 텍스트를 생성하는 능력이 좋음

## PAGE 038

- `DS_PDF09_LLM:p038:L001` 제목
- `DS_PDF09_LLM:p038:L002` 38
- `DS_PDF09_LLM:p038:L003` 제목
- `DS_PDF09_LLM:p038:L004` 대형언어모델 (Large Language Model, LLM)Large Language Model- LLM은 Transformer 계열(특히 self-attention)을 기반으로, 방대한 텍스트(및 경우에 따라 코드·이미지·표 등)를 이용해대규모 사전학습(pre-training)을 수행- 언어를 넘어 다양한 작업을 수행할 수 있는범용 기반 모델(foundation model)로서 동작- Transformer 구조를 사용하여 긴 거리 의존성에 강할 뿐 아니라 GPU에서 병렬 처리가 쉬워, 모델 파라미터 수·데이터 규모·연산량을 함께 키우는 스케일업이 가능

## PAGE 039

- `DS_PDF09_LLM:p039:L001` 제목
- `DS_PDF09_LLM:p039:L002` 39
- `DS_PDF09_LLM:p039:L003` 제목
- `DS_PDF09_LLM:p039:L004` 대형언어모델 (Large Language Model, LLM)Large Language ModelInstruction Tuning- LLM이문장을 생성하는 모델에서 “지시를 이해하고 수행하는 모델”로 바뀌는 핵심 학습 단계- 기존 언어모델처럼 여전히 next-token prediction 방식으로 학습되지만, 예측 대상은 “다음에 자연스럽게 나올 문장”이 아니라 “주어진 지시에 대해 사람이 실제로 쓸 법한 응답”으로 목적이 달라짐
- `DS_PDF09_LLM:p039:L005` 예) 기존 언어 모델Input: “Translate the following sentence into ______”Output: ”Korean”LLM –instruction tuningInstruction:Translate the following sentence into Korean.Input:Machine learning improves decision making.Response:머신러닝은 의사결정을 향상시킨다.

## PAGE 040

- `DS_PDF09_LLM:p040:L001` 제목
- `DS_PDF09_LLM:p040:L002` 40
- `DS_PDF09_LLM:p040:L003` 제목
- `DS_PDF09_LLM:p040:L004` 대형언어모델 (Large Language Model, LLM)
