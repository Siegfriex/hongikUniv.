# DS_PDF06_CODE — annotated PDF transcript

- title: DS06 R/Python
- source_pdf: `dataScience/pdf_raw/[Lecture][DS][06][02] RPython (1).pdf`
- transcript: `dataScience/txt_raw/DS_PDF02__r_python__full_transcript.txt`

## PAGE 001

- `DS_PDF06_CODE:p001:L001` R & Python
- `DS_PDF06_CODE:p001:L002` Introduction to programming, R language, RStudio installation
- `DS_PDF06_CODE:p001:L003` [140316] DATA SCIENCE
- `DS_PDF06_CODE:p001:L004` Hunsik Shin
- `DS_PDF06_CODE:p001:L005` Department of Industrial and Data Engineering
- `DS_PDF06_CODE:p001:L006` {hunsik.shin}@hongik.ac.kr

## PAGE 002

- `DS_PDF06_CODE:p002:L001` 제목
- `DS_PDF06_CODE:p002:L002` 2
- `DS_PDF06_CODE:p002:L003` 제목
- `DS_PDF06_CODE:p002:L004` Table of Contents
- `DS_PDF06_CODE:p002:L005` 1. What is Programming?
- `DS_PDF06_CODE:p002:L006` 2. Introduction to R Language
- `DS_PDF06_CODE:p002:L007` 3. Introduction to Python

## PAGE 003

- `DS_PDF06_CODE:p003:L001` 제목
- `DS_PDF06_CODE:p003:L002` 3
- `DS_PDF06_CODE:p003:L003` 제목
- `DS_PDF06_CODE:p003:L004` Table of Contents
- `DS_PDF06_CODE:p003:L005` 1. What is Programming?
- `DS_PDF06_CODE:p003:L006` 2. Introduction to R Language
- `DS_PDF06_CODE:p003:L007` 3. Introduction to Python

## PAGE 004

- `DS_PDF06_CODE:p004:L001` 제목
- `DS_PDF06_CODE:p004:L002` 4
- `DS_PDF06_CODE:p004:L003` 제목
- `DS_PDF06_CODE:p004:L004` What is Programming?
- `DS_PDF06_CODE:p004:L005` Why Learn Programming?
- `DS_PDF06_CODE:p004:L006` • 컴퓨팅 사고(Computational Thinking): : 컴퓨터가 문제를 분석하고 해결하는 방식으로 사고하는 것으로 복잡한 문제를
- `DS_PDF06_CODE:p004:L007` 단순화하고, 논리적이고 효율적으로 해결하는 사고 방식
- `DS_PDF06_CODE:p004:L008` → 컴퓨팅 사고는더 빠르고 효율적인 문제 해결을 가능하게 함
- `DS_PDF06_CODE:p004:L009` • Programming: 컴퓨터가 처리할 수 있도록 문제 해결 절차를 체계적으로 기술하고, 컴퓨터에서 실행되는 소프트웨어를
- `DS_PDF06_CODE:p004:L010` 만드는 과정
- `DS_PDF06_CODE:p004:L011` → 프로그래밍은컴퓨팅 사고를 학습하는 핵심적인 방법
- `DS_PDF06_CODE:p004:L012` “인간과 달리 컴퓨터는 본래 지능을 가지고 있지 않음. 그러나 문제 해결 과정을 구조적이고 논리적으
- `DS_PDF06_CODE:p004:L013` 로 표현하면, 컴퓨터는 이를 빠르고 오류 없이 실행할 수 있다.
- `DS_PDF06_CODE:p004:L014` 이 때문에 프로그래밍은 컴퓨터가 이해할 수 있는 명확하고 단계적인 지시를 설계하는 데 초점을 둔다.

## PAGE 005

- `DS_PDF06_CODE:p005:L001` 제목
- `DS_PDF06_CODE:p005:L002` 5
- `DS_PDF06_CODE:p005:L003` 제목
- `DS_PDF06_CODE:p005:L004` What is Programming?
- `DS_PDF06_CODE:p005:L005` 컴퓨터의구성: 하드웨어(Hardware)와소프트웨어(Software)
- `DS_PDF06_CODE:p005:L006` • 하드웨어: 키보드, 모니터, 마우스와 같은 외부 장치와 CPU, 메모리, 하드디스크와 같은 내부 장치를 포함하는, 물리적인 형
- `DS_PDF06_CODE:p005:L007` 태를 가진 장치들.
- `DS_PDF06_CODE:p005:L008` • 소프트웨어: 하드웨어가 원활하게 작동하도록 하는 ‘명령어의 집합 (set of instructions)’으로 Excel, PowerPoint, KakaoTalk,
- `DS_PDF06_CODE:p005:L009` Facebook과 같은 프로그램을 포함
- `DS_PDF06_CODE:p005:L010` <Hardware and Software of humanity>

## PAGE 006

- `DS_PDF06_CODE:p006:L001` 제목
- `DS_PDF06_CODE:p006:L002` 6
- `DS_PDF06_CODE:p006:L003` 제목
- `DS_PDF06_CODE:p006:L004` What is Programming?
- `DS_PDF06_CODE:p006:L005` 컴퓨터의구성: 하드웨어(Hardware)와소프트웨어(Software)
- `DS_PDF06_CODE:p006:L006` • 동일한 하드웨어에서 다양한 작업을 수행할 수 있는 것은 소프트웨어 덕분
- `DS_PDF06_CODE:p006:L007` • 컴퓨터의 활용은 어떤 소프트웨어가 설치되어 있는지에 따라 달라짐
- `DS_PDF06_CODE:p006:L008` • 소프트웨어는 실행되는 동안 CPU와 메모리와 같은 하드웨어 자원이 필요
- `DS_PDF06_CODE:p006:L009` • 프로그래밍 능력을 갖추면 필요한 소프트웨어를 직접 만들 수 있음
- `DS_PDF06_CODE:p006:L010` Playing game
- `DS_PDF06_CODE:p006:L011` Writing documents
- `DS_PDF06_CODE:p006:L012` Same software on different hardware
- `DS_PDF06_CODE:p006:L013` Example of useful software

## PAGE 007

- `DS_PDF06_CODE:p007:L001` 제목
- `DS_PDF06_CODE:p007:L002` 7
- `DS_PDF06_CODE:p007:L003` 제목
- `DS_PDF06_CODE:p007:L004` What is Programming?
- `DS_PDF06_CODE:p007:L005` 프로그래밍과프로그래밍언어
- `DS_PDF06_CODE:p007:L006` • 프로그래밍은 요리 과정에 비유할 수 있으며, [그림 1 & 2]와 같이 정해진 순서의 단계에 따라 수행되어야 한다
- `DS_PDF06_CODE:p007:L007` Input Expected Output Result
- `DS_PDF06_CODE:p007:L008` [중요]
- `DS_PDF06_CODE:p007:L009` 단계의 순서가 명확하게 정의되지 않으면, 컴퓨터는 기대한 결과
- `DS_PDF06_CODE:p007:L010` 를 만들어낼 수 없다.
- `DS_PDF06_CODE:p007:L011` 요리와 마찬가지로, 단계를 생략하거나 순서를 바꾸면 실패로 이
- `DS_PDF06_CODE:p007:L012` 어질 수 있으며, 이는 실패한 요리의 예에서 확인 할 수 있다.

## PAGE 008

- `DS_PDF06_CODE:p008:L001` 제목
- `DS_PDF06_CODE:p008:L002` 8
- `DS_PDF06_CODE:p008:L003` 제목
- `DS_PDF06_CODE:p008:L004` What is Programming?
- `DS_PDF06_CODE:p008:L005` 프로그래밍과프로그래밍언어
- `DS_PDF06_CODE:p008:L006` • 프로그래밍은 요리 과정에 비유할 수 있으며, [그림 1 & 2]와 같이 정해진 순서의 단계에 따라 수행되어야 한다

## PAGE 009

- `DS_PDF06_CODE:p009:L001` 제목
- `DS_PDF06_CODE:p009:L002` 9
- `DS_PDF06_CODE:p009:L003` 제목
- `DS_PDF06_CODE:p009:L004` What is Programming?
- `DS_PDF06_CODE:p009:L005` Programming and Programming Languages
- `DS_PDF06_CODE:p009:L006` • 컴퓨터에게 어떤 작업을 수행하도록 지시하기 위해서는 요리 레시피와 마찬가지로 작업의 순서와 방법을 논리적으
- `DS_PDF06_CODE:p009:L007` 로 설명해야 한다. 이 과정을 프로그래밍(programming)이라고 한다.
- `DS_PDF06_CODE:p009:L008` • 일상적인 언어로 컴퓨터에게 명령할 수 있다면 편리하겠지만, 인간의 언어에는 많은 모호성(ambiguity)이 존재한다.
- `DS_PDF06_CODE:p009:L009` • 그 결과, 컴퓨터는 일반적으로 자연어로 작성된 지시를 이해하거나 실행할 수 없다.
- `DS_PDF06_CODE:p009:L010` → 하지만 최근의 대규모 언어 모델(Large Language Models, 예: ChatGPT)을 통해 일상적인 언어로 의도를 표현함으
- `DS_PDF06_CODE:p009:L011` 로써 유용한 코드를 훨씬 쉽게 생성할 수 있게 되었다.

## PAGE 010

- `DS_PDF06_CODE:p010:L001` 제목
- `DS_PDF06_CODE:p010:L002` 10
- `DS_PDF06_CODE:p010:L003` 제목
- `DS_PDF06_CODE:p010:L004` What is Programming?
- `DS_PDF06_CODE:p010:L005` Programming and Programming Languages
- `DS_PDF06_CODE:p010:L006` • Programming Language: 컴퓨터가 작업을 수행하도록 지시하는 프로그램을 작성하기 위해 사용되는 언어
- `DS_PDF06_CODE:p010:L007` • [그림 1-5]에 나타난 것처럼, 프로그래밍 언어는 간단한 영어 단어와 기호로 구성되어 있으며, 각 언어마다 고유한 문
- `DS_PDF06_CODE:p010:L008` 법(grammar)을 가지고 있다.
- `DS_PDF06_CODE:p010:L009` • 프로그래밍을 공부한다는 것은 프로그래밍 언어의 문법 구조를 학습하고, 이를 이용해 컴퓨터를 위한 ‘지침서
- `DS_PDF06_CODE:p010:L010` (instruction manual)’, 즉 프로그램을 작성하는 방법을 배우는 것을 의미
- `DS_PDF06_CODE:p010:L011` → 자연어와 달리, 프로그래밍 언어에는 방언, 속어, 신조어가 존재하지 않는다.

## PAGE 011

- `DS_PDF06_CODE:p011:L001` 제목
- `DS_PDF06_CODE:p011:L002` 11
- `DS_PDF06_CODE:p011:L003` 제목
- `DS_PDF06_CODE:p011:L004` What is Programming?
- `DS_PDF06_CODE:p011:L005` 프로그래밍과프로그래밍언어 – What is the best programming language ?
- `DS_PDF06_CODE:p011:L006` • 대표적인 프로그래밍 언어: C, Java, Python 등
- `DS_PDF06_CODE:p011:L007` • 소프트웨어를 만들기 위해서는 이러한 언어 중최소하나는반드시배워야한다.
- `DS_PDF06_CODE:p011:L008` < PYPL PopularitY of Programming Language >*
- `DS_PDF06_CODE:p011:L009` * The PYPL PopularitY of Programming Language Index is created by analyzing how often language tutorials are searched on Google.

## PAGE 012

- `DS_PDF06_CODE:p012:L001` 제목
- `DS_PDF06_CODE:p012:L002` 12
- `DS_PDF06_CODE:p012:L003` 제목
- `DS_PDF06_CODE:p012:L004` What is Programming?
- `DS_PDF06_CODE:p012:L005` 프로그래밍과프로그래밍언어– Why we learn R&Python?
- `DS_PDF06_CODE:p012:L006` • 많은 사람들에게 프로그래밍은 매우 어렵게 느껴질 수 있음
- `DS_PDF06_CODE:p012:L007` • 컴퓨터공학 전공자가 아니더라도 쉽게 배우고 자신의 업무에 적용할 수 있는 프로그래밍 언어가 필요
- `DS_PDF06_CODE:p012:L008` • 이러한 목적을 위해 개발된 언어가 R과 Python

## PAGE 013

- `DS_PDF06_CODE:p013:L001` 제목
- `DS_PDF06_CODE:p013:L002` 13
- `DS_PDF06_CODE:p013:L003` 제목
- `DS_PDF06_CODE:p013:L004` What is Programming?
- `DS_PDF06_CODE:p013:L005` 프로그래밍과프로그래밍언어– (예시) C언어와 R비교
- `DS_PDF06_CODE:p013:L006` • Problem Statement:
- `DS_PDF06_CODE:p013:L007` 2차원 10×10 배열이 주어졌을 때, 2번째 행(row)과 5번째 열(column)을 제거하는 코드를 작성하시오.
- `DS_PDF06_CODE:p013:L008` 해당 문제의 해결 방법을 C와 R 프로그래밍 언어를 사용하여 각각 구현하시오.
- `DS_PDF06_CODE:p013:L009` <Array Manipulation in R>: 3 lines!<Array Manipulation in C>: 20 lines!

## PAGE 014

- `DS_PDF06_CODE:p014:L001` 제목
- `DS_PDF06_CODE:p014:L002` 14
- `DS_PDF06_CODE:p014:L003` 제목
- `DS_PDF06_CODE:p014:L004` Table of Contents
- `DS_PDF06_CODE:p014:L005` 1. What is Programming?
- `DS_PDF06_CODE:p014:L006` 2. Introduction to R Language
- `DS_PDF06_CODE:p014:L007` 3. Introduction to Python

## PAGE 015

- `DS_PDF06_CODE:p015:L001` 제목
- `DS_PDF06_CODE:p015:L002` 15
- `DS_PDF06_CODE:p015:L003` 제목
- `DS_PDF06_CODE:p015:L004` Table of Contents
- `DS_PDF06_CODE:p015:L005` 1. What is Programming?
- `DS_PDF06_CODE:p015:L006` 2. Introduction to R Language
- `DS_PDF06_CODE:p015:L007` 3. Introduction to Python

## PAGE 016

- `DS_PDF06_CODE:p016:L001` 제목
- `DS_PDF06_CODE:p016:L002` 16
- `DS_PDF06_CODE:p016:L003` 제목
- `DS_PDF06_CODE:p016:L004` Introduction to R Language
- `DS_PDF06_CODE:p016:L005` Characteristics of R Language
- `DS_PDF06_CODE:p016:L006` • R은 비교적 최근에 등장한 프로그래밍 언어 중 하나
- `DS_PDF06_CODE:p016:L007` • R은 1993년 뉴질랜드 오클랜드 대학교에서 Ross Ihaka와 Robert Gentleman에 의해 통계 프로그래밍
- `DS_PDF06_CODE:p016:L008` 언어 S-PLUS의 무료 버전으로 개발
- `DS_PDF06_CODE:p016:L009` <Ross Ihaka> <Robert Gentleman>

## PAGE 017

- `DS_PDF06_CODE:p017:L001` 제목
- `DS_PDF06_CODE:p017:L002` 17
- `DS_PDF06_CODE:p017:L003` 제목
- `DS_PDF06_CODE:p017:L004` Introduction to R Language
- `DS_PDF06_CODE:p017:L005` Characteristics of R Language (1)
- `DS_PDF06_CODE:p017:L006` • 데이터 분석에 특화
- `DS_PDF06_CODE:p017:L007` - R은 통계를 포함한 데이터 분석 작업을 위해 개발 됨
- `DS_PDF06_CODE:p017:L008` - 컴파일 과정 없이 코드를 바로 실행하고 결과를 확인 할 수 있음
- `DS_PDF06_CODE:p017:L009` - R로 작성된 코드는 일반적으로 프로그램(program)보다는 스크립트(script)라고 함
- `DS_PDF06_CODE:p017:L010` • 강력한 사용자 커뮤니티
- `DS_PDF06_CODE:p017:L011` - R은 방대한 사용자층을 보유하고 있어, 활발한 커뮤니티가 다수 존재
- `DS_PDF06_CODE:p017:L012` - 초보자도 활용할 수 있는 학습 자료가 매우 풍부
- `DS_PDF06_CODE:p017:L013` - 국내 검색 엔진을 통해 접근할 수 있는 한글 자료의 양도 지속적으로 증가하고 있다.

## PAGE 018

- `DS_PDF06_CODE:p018:L001` 제목
- `DS_PDF06_CODE:p018:L002` 18
- `DS_PDF06_CODE:p018:L003` 제목
- `DS_PDF06_CODE:p018:L004` Introduction to R Language
- `DS_PDF06_CODE:p018:L005` Characteristics of R Language (1)

## PAGE 019

- `DS_PDF06_CODE:p019:L001` 제목
- `DS_PDF06_CODE:p019:L002` 19
- `DS_PDF06_CODE:p019:L003` 제목
- `DS_PDF06_CODE:p019:L004` Introduction to R Language
- `DS_PDF06_CODE:p019:L005` Characteristics of R Language (2)
- `DS_PDF06_CODE:p019:L006` • 다양한 패키지 제공
- `DS_PDF06_CODE:p019:L007` - R은 데이터 분석을 위한 기능들을 카테고리별로 묶은 패키
- `DS_PDF06_CODE:p019:L008` 지 형태로 제공
- `DS_PDF06_CODE:p019:L009` - 데이터 분석에 필요한 거의 모든 기능을 제공
- `DS_PDF06_CODE:p019:L010` - 새로운 이론이 발표되면, 이를 반영한 R 패키지가 빠르게
- `DS_PDF06_CODE:p019:L011` 개발되어 최신 기법을 지체 없이 데이터 분석에 적용할 수
- `DS_PDF06_CODE:p019:L012` 있음
- `DS_PDF06_CODE:p019:L013` * https://agstats.io/post/intro-to-ggplot/
- `DS_PDF06_CODE:p019:L014` <San Francisco rent prices visualization with ggplot2 package>*

## PAGE 020

- `DS_PDF06_CODE:p020:L001` 제목
- `DS_PDF06_CODE:p020:L002` 20
- `DS_PDF06_CODE:p020:L003` 제목
- `DS_PDF06_CODE:p020:L004` Introduction to R Language
- `DS_PDF06_CODE:p020:L005` Characteristics of R Language (3)
- `DS_PDF06_CODE:p020:L006` • 미적이고 기능적인 통계 그래픽 (Aesthetic and Functional Statistical Graphics)
- `DS_PDF06_CODE:p020:L007` - 데이터 분석에서 분석 결과를 시각적으로 표현하는 것은 매우 중요
- `DS_PDF06_CODE:p020:L008` - R에서는 ggplot 패키지를 활용하여 시각적으로 아름답고 기능적으로 우수한 그래프를 쉽게 만들 수 있다.
- `DS_PDF06_CODE:p020:L009` * ggplot2 is a system for declaratively creating graphics, based onThe Grammar of Graphics.
- `DS_PDF06_CODE:p020:L010` *

## PAGE 021

- `DS_PDF06_CODE:p021:L001` 제목
- `DS_PDF06_CODE:p021:L002` 21
- `DS_PDF06_CODE:p021:L003` 제목
- `DS_PDF06_CODE:p021:L004` Introduction to R Language
- `DS_PDF06_CODE:p021:L005` Characteristics of R Language (4)
- `DS_PDF06_CODE:p021:L006` • 편리한 프로그래밍 환경
- `DS_PDF06_CODE:p021:L007` - 프로그램을 작성하고, 실행하며, 수정하는 작업에는 편리한 작업 환경이 필요
- `DS_PDF06_CODE:p021:L008` - RStudio는 R 프로그래밍을 위한 통합 개발 환경(IDE)을 제공하여 모든 작업이 RStudio 안에서 처리 가능
- `DS_PDF06_CODE:p021:L009` - 이러한 환경을 통합 개발 환경(Integrated Development Environment, IDE)이라고 한다.

## PAGE 022

- `DS_PDF06_CODE:p022:L001` 제목
- `DS_PDF06_CODE:p022:L002` 22
- `DS_PDF06_CODE:p022:L003` 제목
- `DS_PDF06_CODE:p022:L004` Introduction to R Language
- `DS_PDF06_CODE:p022:L005` Characteristics of R Language (4)
- `DS_PDF06_CODE:p022:L006` • 무료 사용 가능 (Free to Use)
- `DS_PDF06_CODE:p022:L007` - R은 오픈소스 소프트웨어로, 무료로 사용 가능
- `DS_PDF06_CODE:p022:L008` - 정기적으로 업데이트되며(연 1~2회), 기능이 지속적으로 개선
- `DS_PDF06_CODE:p022:L009` - R은 Windows뿐만 아니라 Linux와 macOS 환경에서도 설치하여 사용 가능

## PAGE 023

- `DS_PDF06_CODE:p023:L001` 제목
- `DS_PDF06_CODE:p023:L002` 23
- `DS_PDF06_CODE:p023:L003` 제목
- `DS_PDF06_CODE:p023:L004` Example of R (1)
- `DS_PDF06_CODE:p023:L005` Scatter Plot
- `DS_PDF06_CODE:p023:L006` Create a scatter plot using the Petal.Length and Petal.Width variables from the Iris dataset.
- `DS_PDF06_CODE:p023:L007` [Code 12-12]
- `DS_PDF06_CODE:p023:L008` • plot.title: applies theme settings to the title created by ggtitle().
- `DS_PDF06_CODE:p023:L009` • size = 25: sets the font size of the title.
- `DS_PDF06_CODE:p023:L010` • face = "bold": displays the title in bold.
- `DS_PDF06_CODE:p023:L011` • colour = "steelblue": sets the font color of the title.
- `DS_PDF06_CODE:p023:L012` To vary the point shape by species, add shape = Species inside the aes() function.
- `DS_PDF06_CODE:p023:L013` library(ggplot2)
- `DS_PDF06_CODE:p023:L014` ggplot(data=iris, aes(x=Petal.Length, y=Petal.Width,
- `DS_PDF06_CODE:p023:L015` color=Species)) +
- `DS_PDF06_CODE:p023:L016` geom_point(size=3) +
- `DS_PDF06_CODE:p023:L017` ggtitle('꽃잎의 길이와 폭') + # 그래프의 제목 지정
- `DS_PDF06_CODE:p023:L018` theme(plot.title = element_text(size=25, face='bold',
- `DS_PDF06_CODE:p023:L019` colour='steelblue'))

## PAGE 024

- `DS_PDF06_CODE:p024:L001` 제목
- `DS_PDF06_CODE:p024:L002` 24
- `DS_PDF06_CODE:p024:L003` 제목
- `DS_PDF06_CODE:p024:L004` Example of R (1)
- `DS_PDF06_CODE:p024:L005` Scatter Plot
- `DS_PDF06_CODE:p024:L006` Create a scatter plot using the Petal.Length and Petal.Width variables from the Iris dataset.
- `DS_PDF06_CODE:p024:L007` [Code 12-12]
- `DS_PDF06_CODE:p024:L008` • plot.title: applies theme settings to the title created by ggtitle().
- `DS_PDF06_CODE:p024:L009` • size = 25: sets the font size of the title.
- `DS_PDF06_CODE:p024:L010` • face = "bold": displays the title in bold.
- `DS_PDF06_CODE:p024:L011` • colour = "steelblue": sets the font color of the title.
- `DS_PDF06_CODE:p024:L012` To vary the point shape by species, add shape = Species inside the aes() function.
- `DS_PDF06_CODE:p024:L013` library(ggplot2)
- `DS_PDF06_CODE:p024:L014` ggplot(data=iris, aes(x=Petal.Length, y=Petal.Width,
- `DS_PDF06_CODE:p024:L015` color=Species)) +
- `DS_PDF06_CODE:p024:L016` geom_point(size=3) +
- `DS_PDF06_CODE:p024:L017` ggtitle('꽃잎의 길이와 폭') + # 그래프의 제목 지정
- `DS_PDF06_CODE:p024:L018` theme(plot.title = element_text(size=25, face='bold',
- `DS_PDF06_CODE:p024:L019` colour='steelblue'))

## PAGE 025

- `DS_PDF06_CODE:p025:L001` 제목
- `DS_PDF06_CODE:p025:L002` 25
- `DS_PDF06_CODE:p025:L003` 제목
- `DS_PDF06_CODE:p025:L004` Example of R (2)
- `DS_PDF06_CODE:p025:L005` Box Plot
- `DS_PDF06_CODE:p025:L006` Create a box plot using the Petal.Length variable by Species from the Iris dataset.
- `DS_PDF06_CODE:p025:L007` [Code 12-14]
- `DS_PDF06_CODE:p025:L008` When boxplots are drawn by species, the default order of categories is alphabetical: setosa → versicolor → virginica.
- `DS_PDF06_CODE:p025:L009` If we want to change the display order (e.g., versicolor → virginica → setosa), we must modify the levels of the factor variable Species.
- `DS_PDF06_CODE:p025:L010` Once the factor levels are changed, the boxplots will appear in the new order along the x -axis.
- `DS_PDF06_CODE:p025:L011` library(ggplot2)
- `DS_PDF06_CODE:p025:L012` ggplot(data=iris, aes(x=Species, y=Petal.Length, fill=Species))
- `DS_PDF06_CODE:p025:L013` +
- `DS_PDF06_CODE:p025:L014` geom_boxplot( )
- `DS_PDF06_CODE:p025:L015` iris.new <- iris
- `DS_PDF06_CODE:p025:L016` iris.new$Species <- factor(iris.new$Species,
- `DS_PDF06_CODE:p025:L017` levels=c('versicolor','virginica','setosa’))
- `DS_PDF06_CODE:p025:L018` ggplot(data=iris.new, aes(x=Species, y=Petal.Length, fill=Species)) +
- `DS_PDF06_CODE:p025:L019` geom_boxplot( )

## PAGE 026

- `DS_PDF06_CODE:p026:L001` 제목
- `DS_PDF06_CODE:p026:L002` 26
- `DS_PDF06_CODE:p026:L003` 제목
- `DS_PDF06_CODE:p026:L004` Example of R (3)
- `DS_PDF06_CODE:p026:L005` Treemaps
- `DS_PDF06_CODE:p026:L006` [Code 12-1] (2)
- `DS_PDF06_CODE:p026:L007` The area of each tile is proportional to the population of the country.
- `DS_PDF06_CODE:p026:L008` The color of each tile represents GNI (Gross National Income).
- `DS_PDF06_CODE:p026:L009` • Higher income → darker green
- `DS_PDF06_CODE:p026:L010` • Lower income → closer to yellow
- `DS_PDF06_CODE:p026:L011` > library(treemap) # treemap 패키지 불러오기
- `DS_PDF06_CODE:p026:L012` > data(GNI2014)  # 데이터 불러오기
- `DS_PDF06_CODE:p026:L013` > head(GNI2014)  # 데이터 내용 보기
- `DS_PDF06_CODE:p026:L014` treemap(GNI2014,
- `DS_PDF06_CODE:p026:L015` index=c('continent','iso3’),  # 계층 구조 설정(대륙-국가)
- `DS_PDF06_CODE:p026:L016` vSize='population’,           # 타일의 크기
- `DS_PDF06_CODE:p026:L017` vColor='GNI',      # 타일의 컬러
- `DS_PDF06_CODE:p026:L018` type='value',      # 타일 컬러링 방법
- `DS_PDF06_CODE:p026:L019` bg.labels='yellow’,     # 레이블의 배경색
- `DS_PDF06_CODE:p026:L020` title="World's GNI")     # 나무지도 제목

## PAGE 027

- `DS_PDF06_CODE:p027:L001` 제목
- `DS_PDF06_CODE:p027:L002` 27
- `DS_PDF06_CODE:p027:L003` 제목
- `DS_PDF06_CODE:p027:L004` Table of Contents
- `DS_PDF06_CODE:p027:L005` 1. What is Programming?
- `DS_PDF06_CODE:p027:L006` 2. Introduction to R Language
- `DS_PDF06_CODE:p027:L007` 3. Introduction to Python

## PAGE 028

- `DS_PDF06_CODE:p028:L001` 제목
- `DS_PDF06_CODE:p028:L002` 28
- `DS_PDF06_CODE:p028:L003` 제목
- `DS_PDF06_CODE:p028:L004` Table of Contents
- `DS_PDF06_CODE:p028:L005` 1. What is Programming?
- `DS_PDF06_CODE:p028:L006` 2. Introduction to R Language
- `DS_PDF06_CODE:p028:L007` 3. Introduction to Python

## PAGE 029

- `DS_PDF06_CODE:p029:L001` 제목
- `DS_PDF06_CODE:p029:L002` 29
- `DS_PDF06_CODE:p029:L003` 제목
- `DS_PDF06_CODE:p029:L004` Introduction to Python Language
- `DS_PDF06_CODE:p029:L005` Characteristics Python Language
- `DS_PDF06_CODE:p029:L006` • 인터프리터 방식의 객체지향 프로그래밍 언어로서 1989년 귀도 반 로썸(Guido Van Rossum)이 개발
- `DS_PDF06_CODE:p029:L007` • 귀도 반 로썸이 좋아했던 영국 코미디 영화 "몬티 파이썬의 날아다니는 서커스(Monty Python's Flying
- `DS_PDF06_CODE:p029:L008` Circus)"에서 따온 이름

## PAGE 030

- `DS_PDF06_CODE:p030:L001` 제목
- `DS_PDF06_CODE:p030:L002` 30
- `DS_PDF06_CODE:p030:L003` 제목
- `DS_PDF06_CODE:p030:L004` Introduction to Python Language
- `DS_PDF06_CODE:p030:L005` Characteristics Python Language
- `DS_PDF06_CODE:p030:L006` • 인터프리터 방식의 객체지향 프로그래밍 언어로서 1989년 귀도 반 로썸(Guido Van Rossum)이 개발
- `DS_PDF06_CODE:p030:L007` • 귀도 반 로썸이 좋아했던 영국 코미디 영화 "몬티 파이썬의 날아다니는 서커스(Monty Python's Flying
- `DS_PDF06_CODE:p030:L008` Circus)"에서 따온 이름

## PAGE 031

- `DS_PDF06_CODE:p031:L001` 제목
- `DS_PDF06_CODE:p031:L002` 31
- `DS_PDF06_CODE:p031:L003` 제목
- `DS_PDF06_CODE:p031:L004` Introduction to Python Language
- `DS_PDF06_CODE:p031:L005` Characteristics Python Language
- `DS_PDF06_CODE:p031:L006` • 인터프리터 방식의 객체지향 프로그래밍 언어로서 1989년 귀도 반 로썸(Guido Van Rossum)이 개발
- `DS_PDF06_CODE:p031:L007` 1) 컴파일방식: 소스 코드를 기계어로 번역한 후 이 기계어 명령을 실행하는 방식
- `DS_PDF06_CODE:p031:L008` 예) C, C++, 파스칼 등의 언어

## PAGE 032

- `DS_PDF06_CODE:p032:L001` 제목
- `DS_PDF06_CODE:p032:L002` 32
- `DS_PDF06_CODE:p032:L003` 제목
- `DS_PDF06_CODE:p032:L004` Introduction to Python Language
- `DS_PDF06_CODE:p032:L005` Characteristics Python Language
- `DS_PDF06_CODE:p032:L006` • 인터프리터 방식의 객체지향 프로그래밍 언어로서 1989년 귀도 반 로썸(Guido Van Rossum)이 개발
- `DS_PDF06_CODE:p032:L007` 2) 인터프리터방식: 프로그램 명령어를 한 번에 한 줄씩 읽어 번역한 후 바로 실행
- `DS_PDF06_CODE:p032:L008` 예) 파이썬, BASIC 등의 언어가 있음

## PAGE 033

- `DS_PDF06_CODE:p033:L001` 제목
- `DS_PDF06_CODE:p033:L002` 33
- `DS_PDF06_CODE:p033:L003` 제목
- `DS_PDF06_CODE:p033:L004` Introduction to Python Language
- `DS_PDF06_CODE:p033:L005` Characteristics Python Language
- `DS_PDF06_CODE:p033:L006` • 컴파일 방식과 인터프리터 방식 비교
- `DS_PDF06_CODE:p033:L007` 인터프리터방식 컴파일방식
- `DS_PDF06_CODE:p033:L008` 정의 명령어들을 한번에 한 줄씩 읽어 들여
- `DS_PDF06_CODE:p033:L009` 서 실행하는 방식이다.
- `DS_PDF06_CODE:p033:L010` 명령을 기계어로 번역하여 실행파일을
- `DS_PDF06_CODE:p033:L011` 생성하고 이것을 동작시키는 방식이다.
- `DS_PDF06_CODE:p033:L012` 장점
- `DS_PDF06_CODE:p033:L013` 컴파일 단계를 거칠 필요가 없기 때문
- `DS_PDF06_CODE:p033:L014` 에 코드의 수행 결과를 바로 확인할 수
- `DS_PDF06_CODE:p033:L015` 있다.
- `DS_PDF06_CODE:p033:L016` 기계어 코드를 바로 실행시키므로 일
- `DS_PDF06_CODE:p033:L017` 반적인 경우 속도가 더 빠르다
- `DS_PDF06_CODE:p033:L018` 단점 실행 시간이 느리다.
- `DS_PDF06_CODE:p033:L019` 원시 프로그램의 크기가 크다면 번역
- `DS_PDF06_CODE:p033:L020` 과정에 상당한 시간이 소요된다. 코드
- `DS_PDF06_CODE:p033:L021` 의 결과를 즉시 확인할 수 없다.
- `DS_PDF06_CODE:p033:L022` 사용되는
- `DS_PDF06_CODE:p033:L023` 언어 파이썬, BASIC 등 C/C++, 자바, FORTRAN, PASCAL 등

## PAGE 034

- `DS_PDF06_CODE:p034:L001` 제목
- `DS_PDF06_CODE:p034:L002` 34
- `DS_PDF06_CODE:p034:L003` 제목
- `DS_PDF06_CODE:p034:L004` Introduction to Python Language
- `DS_PDF06_CODE:p034:L005` Characteristics Python Language
- `DS_PDF06_CODE:p034:L006` • 직관적이고 단순한 문법으로 축약된 코딩이 가능함
- `DS_PDF06_CODE:p034:L007` • 짧은 코딩으로 많은 기능을 수행할 수 있음
- `DS_PDF06_CODE:p034:L008` • 오픈소스Open source 방식을 채택 → 방대한 라이브러리들이 무료
- `DS_PDF06_CODE:p034:L009` • 객체지향 프로그래밍 언어의 특징을 가짐

## PAGE 035

- `DS_PDF06_CODE:p035:L001` 제목
- `DS_PDF06_CODE:p035:L002` 35
- `DS_PDF06_CODE:p035:L003` 제목
- `DS_PDF06_CODE:p035:L004` Example of Python (1)
- `DS_PDF06_CODE:p035:L005` Numpy
- `DS_PDF06_CODE:p035:L006` - NumPy는 Python에서 수치 계산과 배열 연산을 효율적으로 수행하기 위한 핵심 라이브러리
- `DS_PDF06_CODE:p035:L007` - 리스트(list)에 비해 대규모 데이터 처리 속도가 빠르고, 벡터·행렬 연산을 간결한 코드로 표현할 수 있어 데이터 분석, 머신러
- `DS_PDF06_CODE:p035:L008` 닝, 시뮬레이션의 기초 도구로 널리 사용
- `DS_PDF06_CODE:p035:L009` [Code 12-12]

## PAGE 036

- `DS_PDF06_CODE:p036:L001` 제목
- `DS_PDF06_CODE:p036:L002` 36
- `DS_PDF06_CODE:p036:L003` 제목
- `DS_PDF06_CODE:p036:L004` Example of Python (2)
- `DS_PDF06_CODE:p036:L005` Scikit-learn
- `DS_PDF06_CODE:p036:L006` - scikit-learn은 Python에서 가장 널리 사용되는 머신러닝 라이브러리
- `DS_PDF06_CODE:p036:L007` - 데이터 전처리, 회귀, 분류, 군집화, 모델 평가까지 일관된 인터페이스로 제공
- `DS_PDF06_CODE:p036:L008` - 복잡한 알고리즘도 몇 줄의 코드로 적용할 수 있어 실무와 교육 모두에서 표준처럼 활용
- `DS_PDF06_CODE:p036:L009` import numpy as np
- `DS_PDF06_CODE:p036:L010` import matplotlib.pyplot as plt
- `DS_PDF06_CODE:p036:L011` from sklearn.datasets import make_regression
- `DS_PDF06_CODE:p036:L012` from sklearn.linear_model import LinearRegression
- `DS_PDF06_CODE:p036:L013` from sklearn.model_selection import train_test_split
- `DS_PDF06_CODE:p036:L014` # 1. 가상 회귀 데이터 생성
- `DS_PDF06_CODE:p036:L015` X, y = make_regression(
- `DS_PDF06_CODE:p036:L016` n_samples=100,
- `DS_PDF06_CODE:p036:L017` n_features=1,
- `DS_PDF06_CODE:p036:L018` noise=10,
- `DS_PDF06_CODE:p036:L019` random_state=42
- `DS_PDF06_CODE:p036:L020` )
- `DS_PDF06_CODE:p036:L021` # 2. 학습 / 테스트 데이터 분할
- `DS_PDF06_CODE:p036:L022` X_train, X_test, y_train, y_test = train_test_split(
- `DS_PDF06_CODE:p036:L023` X, y, test_size=0.2, random_state=42)
- `DS_PDF06_CODE:p036:L024` # 3. 선형 회귀 모델 학습
- `DS_PDF06_CODE:p036:L025` model = LinearRegression()
- `DS_PDF06_CODE:p036:L026` model.fit(X_train, y_train)
- `DS_PDF06_CODE:p036:L027` # 4. 예측 (시각화를 위해 정렬)
- `DS_PDF06_CODE:p036:L028` X_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
- `DS_PDF06_CODE:p036:L029` y_line = model.predict(X_line)

## PAGE 037

- `DS_PDF06_CODE:p037:L001` 제목
- `DS_PDF06_CODE:p037:L002` 37
- `DS_PDF06_CODE:p037:L003` 제목
- `DS_PDF06_CODE:p037:L004` Example of Python (2)
- `DS_PDF06_CODE:p037:L005` Scikit-learn
- `DS_PDF06_CODE:p037:L006` - scikit-learn은 Python에서 가장 널리 사용되는 머신러닝 라이브러리
- `DS_PDF06_CODE:p037:L007` - 데이터 전처리, 회귀, 분류, 군집화, 모델 평가까지 일관된 인터페이스로 제공
- `DS_PDF06_CODE:p037:L008` - 복잡한 알고리즘도 몇 줄의 코드로 적용할 수 있어 실무와 교육 모두에서 표준처럼 활용
- `DS_PDF06_CODE:p037:L009` # 5. 시각화
- `DS_PDF06_CODE:p037:L010` plt.figure()
- `DS_PDF06_CODE:p037:L011` plt.scatter(X_train, y_train, label="Training data")
- `DS_PDF06_CODE:p037:L012` plt.scatter(X_test, y_test, label="Test data")
- `DS_PDF06_CODE:p037:L013` plt.plot(X_line, y_line, label="Regression line")
- `DS_PDF06_CODE:p037:L014` plt.xlabel("X")
- `DS_PDF06_CODE:p037:L015` plt.ylabel("y")
- `DS_PDF06_CODE:p037:L016` plt.legend()
- `DS_PDF06_CODE:p037:L017` plt.show()

## PAGE 038

- `DS_PDF06_CODE:p038:L001` 제목
- `DS_PDF06_CODE:p038:L002` 38
- `DS_PDF06_CODE:p038:L003` 부록
- `DS_PDF06_CODE:p038:L004` 1. R 설치
- `DS_PDF06_CODE:p038:L005` 2. Python 설치

## PAGE 039

- `DS_PDF06_CODE:p039:L001` 제목
- `DS_PDF06_CODE:p039:L002` 39
- `DS_PDF06_CODE:p039:L003` 제목R 설치
- `DS_PDF06_CODE:p039:L004` Installing R
- `DS_PDF06_CODE:p039:L005` 1. https://www.r-project.org 접속
- `DS_PDF06_CODE:p039:L006` 2. [Download] 클릭 → [CRAN], [Korea] 링크 선택 → [Download R for Windows] 선택

## PAGE 040

- `DS_PDF06_CODE:p040:L001` 제목
- `DS_PDF06_CODE:p040:L002` 40
- `DS_PDF06_CODE:p040:L003` 제목R 설치
- `DS_PDF06_CODE:p040:L004` Installing R (on Windows)
- `DS_PDF06_CODE:p040:L005` 3. [install R for the first time] 링크 선택 → [Download R 4.5.1 for Windows]  선택

## PAGE 041

- `DS_PDF06_CODE:p041:L001` 제목
- `DS_PDF06_CODE:p041:L002` 41
- `DS_PDF06_CODE:p041:L003` 제목R 설치
- `DS_PDF06_CODE:p041:L004` Installing R (on Mac)
- `DS_PDF06_CODE:p041:L005` 2. [R-4.5.1-amd64.pkg] or [R-4.5.1-x86_64.pkg] 선택 (맥 버전에 따라)

## PAGE 042

- `DS_PDF06_CODE:p042:L001` 제목
- `DS_PDF06_CODE:p042:L002` 42
- `DS_PDF06_CODE:p042:L003` 제목R 설치
- `DS_PDF06_CODE:p042:L004` Installing R
- `DS_PDF06_CODE:p042:L005` 4. [Korean] 선택 및 [OK] 선택
- `DS_PDF06_CODE:p042:L006` → 다른 언어가 편한 경우, 원하는 언어 선택 가능

## PAGE 043

- `DS_PDF06_CODE:p043:L001` 제목
- `DS_PDF06_CODE:p043:L002` 43
- `DS_PDF06_CODE:p043:L003` 제목R 설치
- `DS_PDF06_CODE:p043:L004` Installing R
- `DS_PDF06_CODE:p043:L005` 5. [Next] 클릭

## PAGE 044

- `DS_PDF06_CODE:p044:L001` 제목
- `DS_PDF06_CODE:p044:L002` 44
- `DS_PDF06_CODE:p044:L003` 제목R 설치
- `DS_PDF06_CODE:p044:L004` Installing R
- `DS_PDF06_CODE:p044:L005` 6. 구성요소 설치 단계에서 필요한 요소를 선택하고 [Next] 클릭.
- `DS_PDF06_CODE:p044:L006` → 스타트 옵션은, [No] 선택하고 [Next] 클릭.

## PAGE 045

- `DS_PDF06_CODE:p045:L001` 제목
- `DS_PDF06_CODE:p045:L002` 45
- `DS_PDF06_CODE:p045:L003` 제목R 설치
- `DS_PDF06_CODE:p045:L004` Installing R
- `DS_PDF06_CODE:p045:L005` 7. [Next] [Next] [Next] [Next] [Next] [Next] [Next] 클릭 → [Finish] .

## PAGE 046

- `DS_PDF06_CODE:p046:L001` 제목
- `DS_PDF06_CODE:p046:L002` 46
- `DS_PDF06_CODE:p046:L003` 제목R 설치
- `DS_PDF06_CODE:p046:L004` Installing R
- `DS_PDF06_CODE:p046:L005` 8. 설치 후, R을 실행하면 아래와 같은 스크립트가 실행

## PAGE 047

- `DS_PDF06_CODE:p047:L001` 제목
- `DS_PDF06_CODE:p047:L002` 47
- `DS_PDF06_CODE:p047:L003` 제목
- `DS_PDF06_CODE:p047:L004` Python 설치
- `DS_PDF06_CODE:p047:L005` 공식홈페이지에서설치
- `DS_PDF06_CODE:p047:L006` 1) 홈페이지 접속: http://www.python.org/

## PAGE 048

- `DS_PDF06_CODE:p048:L001` 제목
- `DS_PDF06_CODE:p048:L002` 48
- `DS_PDF06_CODE:p048:L003` 제목
- `DS_PDF06_CODE:p048:L004` Python 설치
- `DS_PDF06_CODE:p048:L005` 공식홈페이지에서설치
- `DS_PDF06_CODE:p048:L006` 2) 다운로드 파일 선택 및 설치
- `DS_PDF06_CODE:p048:L007` → 운영체제와 최신 버전의 파이썬 파일 선택

## PAGE 049

- `DS_PDF06_CODE:p049:L001` 제목
- `DS_PDF06_CODE:p049:L002` 49
- `DS_PDF06_CODE:p049:L003` 제목
- `DS_PDF06_CODE:p049:L004` Python 설치
- `DS_PDF06_CODE:p049:L005` 공식홈페이지에서설치
- `DS_PDF06_CODE:p049:L006` 2) 또는 Google에서 “Python Download” 검색
- `DS_PDF06_CODE:p049:L007` → 다운로드 페이지에서 "Download Python 3.11.4"를 선택(최신 버전 다운로드)
- `DS_PDF06_CODE:p049:L008` → 운영체제(macOS, Windows, Linux 등)를 선택 후 다운

## PAGE 050

- `DS_PDF06_CODE:p050:L001` 제목
- `DS_PDF06_CODE:p050:L002` 50
- `DS_PDF06_CODE:p050:L003` 제목
- `DS_PDF06_CODE:p050:L004` Python 설치
- `DS_PDF06_CODE:p050:L005` 설치파일실행및사용
- `DS_PDF06_CODE:p050:L006` 3) python-3.11.4.exe 실행
- `DS_PDF06_CODE:p050:L007` → “Install launcher for all users(recommended)“
- `DS_PDF06_CODE:p050:L008` → PATH 환경 변수에 파이썬 실행 파일이 위치한 경로를 등록 : “Add Python.eye to PATH“ 선택
- `DS_PDF06_CODE:p050:L009` → “Install Now"를 눌러 설치를 시작

## PAGE 051

- `DS_PDF06_CODE:p051:L001` 제목
- `DS_PDF06_CODE:p051:L002` 51
- `DS_PDF06_CODE:p051:L003` 제목
- `DS_PDF06_CODE:p051:L004` Python 설치
- `DS_PDF06_CODE:p051:L005` 설치파일실행및사용
- `DS_PDF06_CODE:p051:L006` 4) python 실행
- `DS_PDF06_CODE:p051:L007` - 시작 버튼을 눌러 “id”를 검색, IDLE을 눌러서 실행

## PAGE 052

- `DS_PDF06_CODE:p052:L001` 제목
- `DS_PDF06_CODE:p052:L002` 52
- `DS_PDF06_CODE:p052:L003` 제목
- `DS_PDF06_CODE:p052:L004` Python 설치
- `DS_PDF06_CODE:p052:L005` 설치파일실행및사용
- `DS_PDF06_CODE:p052:L006` 4) python 실행
- `DS_PDF06_CODE:p052:L007` - 프롬프트에 print('Hello Python!!') 을 입력 후 Enter → 프롬프트 아래에 Hello Python!!이 출력

## PAGE 053

- `DS_PDF06_CODE:p053:L001` 제목
- `DS_PDF06_CODE:p053:L002` 53
- `DS_PDF06_CODE:p053:L003` 제목
- `DS_PDF06_CODE:p053:L004` Python 설치
- `DS_PDF06_CODE:p053:L005` 설치파일실행및사용
- `DS_PDF06_CODE:p053:L006` 4) python 실행 (MacOS)
- `DS_PDF06_CODE:p053:L007` - Terminal에서 python을 입력하여 실행
- `DS_PDF06_CODE:p053:L008` - 프롬프트에 print('Hello Python!!') 을 입력 후 Enter → 프롬프트 아래에 Hello Python!!이 출력
- `DS_PDF06_CODE:p053:L009` macOS 운영체제의터미널과파이썬대화형모드

## PAGE 054

- `DS_PDF06_CODE:p054:L001` 제목
- `DS_PDF06_CODE:p054:L002` 54
- `DS_PDF06_CODE:p054:L003` 제목
- `DS_PDF06_CODE:p054:L004` References
- `DS_PDF06_CODE:p054:L005` • 난생처음 R코딩 데이터분석 강의교안. 한빛미디어, 2024
- `DS_PDF06_CODE:p054:L006` • 으뜸파이썬 강의교안. 생능출판서, 2024
