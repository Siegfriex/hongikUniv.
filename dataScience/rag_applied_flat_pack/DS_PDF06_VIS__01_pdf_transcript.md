# DS_PDF06_VIS — annotated PDF transcript

- title: DS06 데이터시각화
- source_pdf: `dataScience/pdf_raw/[Lecture][DS][06][01] 데이터시각화 (3).pdf`
- transcript: `dataScience/txt_raw/DS_PDF01__data_visualization__full_transcript.txt`

## PAGE 001

- `DS_PDF06_VIS:p001:L001` 데이터시각화
- `DS_PDF06_VIS:p001:L002` [140316] DATA SCIENCE
- `DS_PDF06_VIS:p001:L003` Hunsik Shin
- `DS_PDF06_VIS:p001:L004` Department of Industrial and Data Engineering
- `DS_PDF06_VIS:p001:L005` {hunsik.shin}@hongik.ac.kr

## PAGE 002

- `DS_PDF06_VIS:p002:L001` 제목
- `DS_PDF06_VIS:p002:L002` 3
- `DS_PDF06_VIS:p002:L003` 제목
- `DS_PDF06_VIS:p002:L004` 데이터시각화
- `DS_PDF06_VIS:p002:L005` •단변량
- `DS_PDF06_VIS:p002:L006` -양적변수: 히스토그램, 박스플롯(상자그림)
- `DS_PDF06_VIS:p002:L007` -범주형변수: 막대그래프, 파이차트
- `DS_PDF06_VIS:p002:L008` •이변량
- `DS_PDF06_VIS:p002:L009` -양적vs. 양적: 산점도, 산점도행렬, 버블차트등
- `DS_PDF06_VIS:p002:L010` -범주형vs. 범주형: mosaic plot
- `DS_PDF06_VIS:p002:L011` -양적vs. 범주형: 박스플롯들
- `DS_PDF06_VIS:p002:L012` •다변량
- `DS_PDF06_VIS:p002:L013` -Radar/Spyder 차트, 나이팅게일차트, heatmap

## PAGE 003

- `DS_PDF06_VIS:p003:L001` 제목
- `DS_PDF06_VIS:p003:L002` 4
- `DS_PDF06_VIS:p003:L003` 제목
- `DS_PDF06_VIS:p003:L004` 데이터시각화
- `DS_PDF06_VIS:p003:L005` •Histogram
- `DS_PDF06_VIS:p003:L006` 출처: https://www.r-graph-gallery.com/

## PAGE 004

- `DS_PDF06_VIS:p004:L001` 제목
- `DS_PDF06_VIS:p004:L002` 5
- `DS_PDF06_VIS:p004:L003` 제목
- `DS_PDF06_VIS:p004:L004` 데이터시각화
- `DS_PDF06_VIS:p004:L005` •Histogram
- `DS_PDF06_VIS:p004:L006` 출처: https://www.r-graph-gallery.com/
- `DS_PDF06_VIS:p004:L007` • binwidth: The width of the bins. Can be specified as a
- `DS_PDF06_VIS:p004:L008` numeric value or as a function that takes x after scale
- `DS_PDF06_VIS:p004:L009` transformation as input and returns a single numeric
- `DS_PDF06_VIS:p004:L010` value.
- `DS_PDF06_VIS:p004:L011` • bins: Number of bins. Overridden bybinwidth. Defaults
- `DS_PDF06_VIS:p004:L012` to 30.

## PAGE 005

- `DS_PDF06_VIS:p005:L001` 제목
- `DS_PDF06_VIS:p005:L002` 6
- `DS_PDF06_VIS:p005:L003` 제목
- `DS_PDF06_VIS:p005:L004` 데이터시각화
- `DS_PDF06_VIS:p005:L005` •Density plot
- `DS_PDF06_VIS:p005:L006` 밀도추정그래프(주로커널밀도추정, Kernel Density Estimation)는히스토그램을부드러운곡선형태로만든것
- `DS_PDF06_VIS:p005:L007` 각데이터포인트에커널함수(주로가우시안)를적용해합친결과물.
- `DS_PDF06_VIS:p005:L008` >표현방식:연속적인곡선
- `DS_PDF06_VIS:p005:L009` >Y축:밀도(Density) (곡선아래의전체면적의합 = 1)
- `DS_PDF06_VIS:p005:L010` 출처: https://www.r-graph-gallery.com/

## PAGE 006

- `DS_PDF06_VIS:p006:L001` 제목
- `DS_PDF06_VIS:p006:L002` 7
- `DS_PDF06_VIS:p006:L003` 제목
- `DS_PDF06_VIS:p006:L004` 데이터시각화
- `DS_PDF06_VIS:p006:L005` •Scatter Plot(산점도)
- `DS_PDF06_VIS:p006:L006` 출처: https://www.r-graph-gallery.com/

## PAGE 007

- `DS_PDF06_VIS:p007:L001` 제목
- `DS_PDF06_VIS:p007:L002` 8
- `DS_PDF06_VIS:p007:L003` 제목
- `DS_PDF06_VIS:p007:L004` 데이터시각화
- `DS_PDF06_VIS:p007:L005` •Scatterplot matrix
- `DS_PDF06_VIS:p007:L006` 출처: https://www.r-graph-gallery.com/

## PAGE 008

- `DS_PDF06_VIS:p008:L001` 제목
- `DS_PDF06_VIS:p008:L002` 9
- `DS_PDF06_VIS:p008:L003` 제목
- `DS_PDF06_VIS:p008:L004` 데이터시각화
- `DS_PDF06_VIS:p008:L005` •Bubble Plot
- `DS_PDF06_VIS:p008:L006` - 산점도(Scatter Plot)에데이터의크기차원을하나더추가한그래프
- `DS_PDF06_VIS:p008:L007` - 산점도가두변수사이의관계(좌표)만보여준다면, 버블차트는그지점에놓인원의크기(면적)를통해세번째정보를시각화
- `DS_PDF06_VIS:p008:L008` 출처: https://www.r-graph-gallery.com/

## PAGE 009

- `DS_PDF06_VIS:p009:L001` 제목
- `DS_PDF06_VIS:p009:L002` 10
- `DS_PDF06_VIS:p009:L003` 제목
- `DS_PDF06_VIS:p009:L004` 데이터시각화
- `DS_PDF06_VIS:p009:L005` •Radar/Spyder Chart
- `DS_PDF06_VIS:p009:L006` 출처: https://www.r-graph-gallery.com/

## PAGE 010

- `DS_PDF06_VIS:p010:L001` 제목
- `DS_PDF06_VIS:p010:L002` 11
- `DS_PDF06_VIS:p010:L003` 제목
- `DS_PDF06_VIS:p010:L004` 데이터시각화
- `DS_PDF06_VIS:p010:L005` •Box Plot
- `DS_PDF06_VIS:p010:L006` 출처: https://www.r-graph-gallery.com/

## PAGE 011

- `DS_PDF06_VIS:p011:L001` 제목
- `DS_PDF06_VIS:p011:L002` 12
- `DS_PDF06_VIS:p011:L003` 제목
- `DS_PDF06_VIS:p011:L004` 데이터시각화
- `DS_PDF06_VIS:p011:L005` •Box Plot
- `DS_PDF06_VIS:p011:L006` 출처: https://www.r-graph-gallery.com/

## PAGE 012

- `DS_PDF06_VIS:p012:L001` 제목
- `DS_PDF06_VIS:p012:L002` 13
- `DS_PDF06_VIS:p012:L003` 제목
- `DS_PDF06_VIS:p012:L004` 데이터시각화
- `DS_PDF06_VIS:p012:L005` •Heatmap
- `DS_PDF06_VIS:p012:L006` 출처: https://www.r-graph-gallery.com/
- `DS_PDF06_VIS:p012:L007` <Heatmap with Dendrogram>

## PAGE 013

- `DS_PDF06_VIS:p013:L001` 제목
- `DS_PDF06_VIS:p013:L002` 14
- `DS_PDF06_VIS:p013:L003` 제목
- `DS_PDF06_VIS:p013:L004` 데이터시각화
- `DS_PDF06_VIS:p013:L005` •Pie Chart
- `DS_PDF06_VIS:p013:L006` 출처: https://www.r-graph-gallery.com/

## PAGE 014

- `DS_PDF06_VIS:p014:L001` 제목
- `DS_PDF06_VIS:p014:L002` 15
- `DS_PDF06_VIS:p014:L003` 제목
- `DS_PDF06_VIS:p014:L004` 데이터시각화
- `DS_PDF06_VIS:p014:L005` •Circular stacked barchart
- `DS_PDF06_VIS:p014:L006` 출처: https://www.r-graph-gallery.com/

## PAGE 015

- `DS_PDF06_VIS:p015:L001` 제목
- `DS_PDF06_VIS:p015:L002` 16
- `DS_PDF06_VIS:p015:L003` 제목
- `DS_PDF06_VIS:p015:L004` 데이터시각화
- `DS_PDF06_VIS:p015:L005` The R Graph Gallery
- `DS_PDF06_VIS:p015:L006` 출처: https://www.r-graph-gallery.com/

## PAGE 016

- `DS_PDF06_VIS:p016:L001` 제목
- `DS_PDF06_VIS:p016:L002` 17
- `DS_PDF06_VIS:p016:L003` 제목
- `DS_PDF06_VIS:p016:L004` 데이터시각화활용

## PAGE 017

- `DS_PDF06_VIS:p017:L001` 제목
- `DS_PDF06_VIS:p017:L002` 18
- `DS_PDF06_VIS:p017:L003` 제목
- `DS_PDF06_VIS:p017:L004` 데이터시각화활용
- `DS_PDF06_VIS:p017:L005` •질병관리청
- `DS_PDF06_VIS:p017:L006` -COVID-19 Dashboard
- `DS_PDF06_VIS:p017:L007` -https://ncv.kdca.go.kr/covdash/biz/dsbd/covDsbdOcrn.do
- `DS_PDF06_VIS:p017:L008` •Centers for Disease Control and Prevention
- `DS_PDF06_VIS:p017:L009` -CDC COVID Data Tracker
- `DS_PDF06_VIS:p017:L010` -https://covid.cdc.gov/covid-data-tracker

## PAGE 018

- `DS_PDF06_VIS:p018:L001` 제목
- `DS_PDF06_VIS:p018:L002` 19
- `DS_PDF06_VIS:p018:L003` 제목
- `DS_PDF06_VIS:p018:L004` 데이터시각화활용

## PAGE 019

- `DS_PDF06_VIS:p019:L001` 제목
- `DS_PDF06_VIS:p019:L002` 20
- `DS_PDF06_VIS:p019:L003` 제목
- `DS_PDF06_VIS:p019:L004` 데이터시각화활용

## PAGE 020

- `DS_PDF06_VIS:p020:L001` 제목
- `DS_PDF06_VIS:p020:L002` 21
- `DS_PDF06_VIS:p020:L003` 제목
- `DS_PDF06_VIS:p020:L004` Google
- `DS_PDF06_VIS:p020:L005` •구글검색을할때우리는빅데이터를사용
- `DS_PDF06_VIS:p020:L006` •구글색인-검색할수있는모든웹페이지에대한아카이브의크기는대략100페타바이트(또는1억기가바이트).
- `DS_PDF06_VIS:p020:L007` •1997년창립된구글을전세계적으로유명하게만든것은구글페이지랭크(pagerank)로알고리즘
- `DS_PDF06_VIS:p020:L008` •페이지랭크는구글의창업자인래리페이지와세르게이브린이구글을만들기전, 스탠퍼드대학에서연구할때
- `DS_PDF06_VIS:p020:L009` 개발

## PAGE 021

- `DS_PDF06_VIS:p021:L001` 제목
- `DS_PDF06_VIS:p021:L002` 22
- `DS_PDF06_VIS:p021:L003` 제목
- `DS_PDF06_VIS:p021:L004` Google
- `DS_PDF06_VIS:p021:L005` •원리는더많은페이지들이특정페이지에링크될수록그특정페이지의우선순위가높아진다는것
- `DS_PDF06_VIS:p021:L006` •권위가높은페이지일수록인용될가능성이높아짐
- `DS_PDF06_VIS:p021:L007` •그사이트에링크된비슷한키워드를얼마나많은사이트들이사용했는가?, 그리고그링크페이지는얼마나권
- `DS_PDF06_VIS:p021:L008` 위있는(자주링크되는) 것인가를기준으로, 구글은인덱스의모든페이지에순위를매겨서첫검색알고리즘을
- `DS_PDF06_VIS:p021:L009` 만듬
- `DS_PDF06_VIS:p021:L010` •현재구글은전체인터넷검색사용량의89%를차지하고있다.

## PAGE 022

- `DS_PDF06_VIS:p022:L001` 제목
- `DS_PDF06_VIS:p022:L002` 23
- `DS_PDF06_VIS:p022:L003` 제목PageRank

## PAGE 023

- `DS_PDF06_VIS:p023:L001` 제목
- `DS_PDF06_VIS:p023:L002` 24
- `DS_PDF06_VIS:p023:L003` 제목PageRank

## PAGE 024

- `DS_PDF06_VIS:p024:L001` 제목
- `DS_PDF06_VIS:p024:L002` 25
- `DS_PDF06_VIS:p024:L003` 제목PageRank

## PAGE 025

- `DS_PDF06_VIS:p025:L001` 제목
- `DS_PDF06_VIS:p025:L002` 26
- `DS_PDF06_VIS:p025:L003` 제목PageRank

## PAGE 026

- `DS_PDF06_VIS:p026:L001` 제목
- `DS_PDF06_VIS:p026:L002` 27
- `DS_PDF06_VIS:p026:L003` 제목PageRank

## PAGE 027

- `DS_PDF06_VIS:p027:L001` 제목
- `DS_PDF06_VIS:p027:L002` 28
- `DS_PDF06_VIS:p027:L003` 제목PageRank
- `DS_PDF06_VIS:p027:L004` https://en.wikipedia.org/wiki/PageRank#/media/File:PageRanks-Example.svg

## PAGE 028

- `DS_PDF06_VIS:p028:L001` 제목
- `DS_PDF06_VIS:p028:L002` 29
- `DS_PDF06_VIS:p028:L003` 제목PageRank
- `DS_PDF06_VIS:p028:L004` https://en.wikipedia.org/wiki/PageRank#/media/File:PageRanks-Example.svg

## PAGE 029

- `DS_PDF06_VIS:p029:L001` 제목
- `DS_PDF06_VIS:p029:L002` 30
- `DS_PDF06_VIS:p029:L003` 제목PageRank
- `DS_PDF06_VIS:p029:L004` https://en.wikipedia.org/wiki/PageRank#/media/File:PageRanks-Example.svg

## PAGE 030

- `DS_PDF06_VIS:p030:L001` 제목
- `DS_PDF06_VIS:p030:L002` 31
- `DS_PDF06_VIS:p030:L003` 제목PageRank

## PAGE 031

- `DS_PDF06_VIS:p031:L001` 제목
- `DS_PDF06_VIS:p031:L002` 32
- `DS_PDF06_VIS:p031:L003` 제목PageRank

## PAGE 032

- `DS_PDF06_VIS:p032:L001` 제목
- `DS_PDF06_VIS:p032:L002` 33
- `DS_PDF06_VIS:p032:L003` 제목PageRank

## PAGE 033

- `DS_PDF06_VIS:p033:L001` 제목
- `DS_PDF06_VIS:p033:L002` 34
- `DS_PDF06_VIS:p033:L003` 제목PageRank

## PAGE 034

- `DS_PDF06_VIS:p034:L001` 제목
- `DS_PDF06_VIS:p034:L002` 35
- `DS_PDF06_VIS:p034:L003` 제목PageRank

## PAGE 035

- `DS_PDF06_VIS:p035:L001` 제목
- `DS_PDF06_VIS:p035:L002` 36
- `DS_PDF06_VIS:p035:L003` 제목PageRank

## PAGE 036

- `DS_PDF06_VIS:p036:L001` 제목
- `DS_PDF06_VIS:p036:L002` 37
- `DS_PDF06_VIS:p036:L003` 제목
- `DS_PDF06_VIS:p036:L004` Google
- `DS_PDF06_VIS:p036:L005` Google의독감예보
- `DS_PDF06_VIS:p036:L006` •2013년미국에서계절인플루엔자(독감)가유행. 독감으로인한사망자가이미100명을넘어서자일부지역에서공중보건
- `DS_PDF06_VIS:p036:L007` 비상사태를선포
- `DS_PDF06_VIS:p036:L008` •미질병통제예방센터(CDC)에따르면122개도시의사망자를조사한결과, 전체사망자중7.3%가감기나폐렴으로숨진
- `DS_PDF06_VIS:p036:L009` 것으로파악
- `DS_PDF06_VIS:p036:L010` •CDC가발표하는독감관련보고서보다더앞서독감바이러스확산을예측하는곳이있었는데바로세계적인IT 기업구
- `DS_PDF06_VIS:p036:L011` 글
- `DS_PDF06_VIS:p036:L012` •구글은독감증세환자가늘면'감기'와관련된단어를검색하는빈도가함께증가한다는패턴을발견
- `DS_PDF06_VIS:p036:L013` •이를질병통제예방센터데이터와비교해본결과검색빈도와실제독감증세를보인환자숫자사이에밀접한상관관계가
- `DS_PDF06_VIS:p036:L014` 있다는사실을밝힘
- `DS_PDF06_VIS:p036:L015` •구글은이같은분석을바탕으로웹사이트를통해시간및지역별독감유행정보를미국보건당국보다한발앞서제공하
- `DS_PDF06_VIS:p036:L016` 고있다

## PAGE 037

- `DS_PDF06_VIS:p037:L001` 제목
- `DS_PDF06_VIS:p037:L002` 38
- `DS_PDF06_VIS:p037:L003` 제목
- `DS_PDF06_VIS:p037:L004` Google
- `DS_PDF06_VIS:p037:L005` Google의독감예보
- `DS_PDF06_VIS:p037:L006` •구글이지난2008년11월부터선보인'독감트렌드' 서비스는전세계각지에서'독감증세', '독감치료' 등독감과관련된
- `DS_PDF06_VIS:p037:L007` 검색어의입력빈도를지역별로파악해독감유행수준을'매우낮음'부터'매우높음'까지5개등급으로구분해표시한다.
- `DS_PDF06_VIS:p037:L008` •특정지역에서발열이나기침등독감관련검색이늘어나면검색어와관련된IP 주소를지도에추가해해당지역의독감
- `DS_PDF06_VIS:p037:L009` 유행수준등급이거의실시간으로표시된다.
- `DS_PDF06_VIS:p037:L010` 출처: https://smart.science.go.kr/scienceStory/view.action

## PAGE 038

- `DS_PDF06_VIS:p038:L001` 제목
- `DS_PDF06_VIS:p038:L002` 39
- `DS_PDF06_VIS:p038:L003` 제목
- `DS_PDF06_VIS:p038:L004` 지진예보– 지진희갤러리

## PAGE 039

- `DS_PDF06_VIS:p039:L001` 제목
- `DS_PDF06_VIS:p039:L002` 40
- `DS_PDF06_VIS:p039:L003` 제목
- `DS_PDF06_VIS:p039:L004` 지진예보– 지진희갤러리
