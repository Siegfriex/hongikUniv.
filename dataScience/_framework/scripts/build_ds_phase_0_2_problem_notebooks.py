#!/usr/bin/env python3
"""Build DS Phase 0-2 Korean problem/answer notebooks.

The notebooks follow the local ipynb-problem-generation skill:
- one hint-only problem notebook per Phase
- one separated answer notebook per Phase
- no answer logic in the problem notebook
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "dataScience" / "workshop" / "ipynb"
CELL_COUNTER = 0


COMMON_SOURCE_BASIS = [
    "dataScience/rag_applied_flat_pack/DS_PDF06_CODE__04_rag.md",
    "dataScience/rag_applied_flat_pack/DS_PDF06_VIS__04_rag.md",
    "dataScience/rag_applied_flat_pack/DS_PDF07_STATS__04_rag.md",
    "dataScience/rag_applied_flat_pack/DS_PDF08_ML1__04_rag.md",
]


def md_cell(text: str) -> dict:
    global CELL_COUNTER
    CELL_COUNTER += 1
    return {
        "cell_type": "markdown",
        "id": f"md-{CELL_COUNTER:04d}",
        "metadata": {},
        "source": dedent(text).strip() + "\n",
    }


def code_cell(text: str) -> dict:
    global CELL_COUNTER
    CELL_COUNTER += 1
    return {
        "cell_type": "code",
        "id": f"code-{CELL_COUNTER:04d}",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(text).strip() + "\n",
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


PHASES = [
    {
        "base": "DS_G0_P0001",
        "phase": "Phase 0",
        "topic": "데이터 spine·기호 세팅",
        "goal": "데이터를 unit, row/column, feature/target, identifier, leakage 후보, mu/pi/xbar/phat/X/y로 번역한다.",
        "anchors": [
            "DS_PDF06_CODE:p013:L007",
            "DS_PDF08_ML1:p045:L004",
            "DS_PDF06_CODE:p036:L013",
            "DS_PDF07_STATS:p002:L007",
        ],
        "criteria": [
            "unit of analysis와 row meaning을 먼저 쓴다.",
            "target, feature 후보, 제외 후보를 분리한다.",
            "mu/pi는 모집단 모수, xbar/phat는 표본 통계량으로 구분한다.",
            "통계의 X와 ML의 feature matrix X를 문맥으로 구분한다.",
            "random_state는 재현성 장치로 해석한다.",
        ],
        "problem_types": [
            {
                "label": "A",
                "title": "데이터 구조 번역 문제",
                "problems": [
                    {
                        "id": "A-1",
                        "title": "Customer churn 도메인",
                        "difficulty": "1.5",
                        "context": "고객 이탈 예측을 위한 작은 테이블 설계를 검토한다.",
                        "given": "`customer_id, age, income, usage_time, payment_delay, complaints, plan_type, churn`",
                        "questions": [
                            "unit of analysis는 무엇인가?",
                            "row 하나는 현실에서 무엇인가?",
                            "target은 무엇인가?",
                            "feature 후보는 무엇인가?",
                            "feature로 쓰면 위험하거나 의미 없는 column은 무엇인가?",
                        ],
                        "check": "identifier를 feature로 넣는 오류를 잡는다.",
                        "tutor": "이 데이터에서 row 하나가 현실의 누구 또는 무엇을 뜻하나?",
                        "hint": """
                        # 힌트 전용: 정답을 출력하지 않는다.
                        columns = ["customer_id", "age", "income", "usage_time", "payment_delay", "complaints", "plan_type", "churn"]
                        # TODO: unit, target_col, feature_candidates, excluded_cols를 직접 적어라.
                        """,
                        "answer": """
                        - unit of analysis: 고객 1명.
                        - row meaning: 고객 한 명의 관측치.
                        - target: `churn`.
                        - feature 후보: `age`, `income`, `usage_time`, `payment_delay`, `complaints`, `plan_type`.
                        - 제외 후보: `customer_id`는 식별자라 일반화 가능한 패턴이 아니므로 feature에서 제외한다.
                        - 근거: DataFrame 행은 관측 단위, 열은 변수이며 X/y 구조는 feature와 target을 분리해야 한다.
                        - 자주 하는 오답: `customer_id`까지 모델에 넣고 성능이 좋아졌다고 해석하는 것.
                        """,
                    },
                    {
                        "id": "A-2",
                        "title": "병원 예약 노쇼 도메인",
                        "difficulty": "2.0",
                        "context": "예약 환자의 노쇼 여부를 예측하려 한다.",
                        "given": "`patient_id, age, department, previous_no_show_count, appointment_day, reminder_sent, no_show`",
                        "questions": [
                            "target은 무엇인가?",
                            "classification인가 regression인가?",
                            "`appointment_day`는 그대로 써도 되는가, 전처리가 필요한가?",
                            "`reminder_sent`는 feature로 쓸 수 있는가? 정보 발생 시점을 기준으로 설명하라.",
                        ],
                        "check": "feature는 column 이름만 보고 고르지 않고 정보 발생 시점을 확인한다.",
                        "tutor": "예측 시점에 이미 알고 있던 정보와 예측 이후에 생긴 정보를 어떻게 나눌까?",
                        "hint": """
                        # 힌트 전용
                        # 1) target 후보를 먼저 찾는다.
                        # 2) target의 값이 범주인지 연속값인지 판단한다.
                        # 3) 날짜 column은 보통 year/month/day/weekday 같은 파생변수 후보가 된다.
                        # 4) reminder_sent의 기록 시점이 예약 전인지 예약 후인지 확인한다.
                        """,
                        "answer": """
                        - target: `no_show`.
                        - 문제 유형: 노쇼/방문 같은 범주를 맞히므로 classification.
                        - `appointment_day`: 날짜 문자열 그대로보다 요일, 시간대, 예약까지 남은 일수 같은 파생변수로 전처리한다.
                        - `reminder_sent`: 예약 전에 발송 여부가 결정된 정보라면 feature 가능. 노쇼 후 사후 처리 기록이라면 leakage라서 제외한다.
                        - 자주 하는 오답: 모든 column을 자동으로 feature로 보고, 정보 발생 시점을 무시하는 것.
                        """,
                    },
                    {
                        "id": "A-3",
                        "title": "온라인 강의 수료 예측 도메인",
                        "difficulty": "2.5",
                        "context": "1주차 종료 시점에 온라인 강의 최종 수료 여부를 예측하려 한다.",
                        "given": "`student_id, login_count_week1, video_watch_time_week1, quiz_score_final, assignment_submitted, completed`",
                        "questions": [
                            "`completed`를 예측할 때 `quiz_score_final`은 feature로 써도 되는가?",
                            "왜 leakage 후보인지 설명하라.",
                            "모델링 시점이 1주차 종료 시점이면 feature로 쓸 수 있는 column만 골라라.",
                        ],
                        "check": "사후 정보와 target leakage를 구분한다.",
                        "tutor": "1주차 종료 시점에 실제로 관측 가능한 column만 남기면 무엇이 남나?",
                        "hint": """
                        # 힌트 전용
                        # 예측 기준 시점: 1주차 종료 시점
                        # TODO: before_prediction_cols와 after_prediction_cols를 나눠라.
                        """,
                        "answer": """
                        - `quiz_score_final`은 최종 평가 후 생기는 정보이므로 1주차 종료 시점 예측에서는 feature로 쓰면 안 된다.
                        - 이유: target인 `completed`와 시간적으로 너무 가까운 사후 정보가 들어가 모델이 미래 정보를 본다.
                        - 사용 가능 후보: `login_count_week1`, `video_watch_time_week1`; `assignment_submitted`는 1주차 과제 제출 여부라면 가능하지만 최종 과제 제출 여부라면 제외한다.
                        - 제외: `student_id`, `quiz_score_final`, target인 `completed`.
                        """,
                    },
                ],
            },
            {
                "label": "B",
                "title": "기호 매핑 문제",
                "problems": [
                    {
                        "id": "B-1",
                        "title": "이탈률의 pi와 phat",
                        "difficulty": "1.5",
                        "context": "전체 고객 50,000명 중 진짜 이탈률은 모른다. 표본 400명에서 이탈 고객이 92명이다.",
                        "given": "`population_size=50000`, `sample_size=400`, `churn_count=92`",
                        "questions": [
                            "모집단 비율 기호를 써라.",
                            "표본 비율을 계산하라.",
                            "`pi`와 `phat`의 차이를 문장으로 설명하라.",
                        ],
                        "check": "표본 비율을 모집단 비율로 단정하지 않는다.",
                        "tutor": "지금 계산할 수 있는 값은 전체의 진짜 값인가, 표본에서 나온 값인가?",
                        "hint": """
                        # 힌트 전용
                        sample_size = 400
                        churn_count = 92
                        # phat = churn_count / sample_size
                        # pi는 계산값이 아니라 모집단의 알 수 없는 진짜 비율을 뜻한다.
                        """,
                        "answer": """
                        - 모집단 비율: `pi_churn`.
                        - 표본 비율: `phat_churn = 92 / 400 = 0.23`.
                        - 해석: 표본에서는 이탈률이 23%이고, 이는 모집단의 진짜 이탈률 `pi_churn`을 추정한 값이다.
                        - 오답: `pi_churn = 0.23`이라고 단정하는 것.
                        """,
                    },
                    {
                        "id": "B-2",
                        "title": "사용시간 평균의 mu와 xbar",
                        "difficulty": "1.5",
                        "context": "표본 고객 5명의 `usage_time`이 주어졌다.",
                        "given": "`12, 18, 21, 9, 30`",
                        "questions": [
                            "표본 평균 `xbar`를 계산하라.",
                            "이 값은 어떤 모수의 추정값인가?",
                            "이 값을 전체 고객 평균이라고 단정하면 왜 틀리는가?",
                        ],
                        "check": "xbar와 mu를 구분한다.",
                        "tutor": "계산한 평균은 표본에서 나온 값인가, 모집단 전체의 값인가?",
                        "hint": """
                        # 힌트 전용
                        values = [12, 18, 21, 9, 30]
                        # xbar = sum(values) / len(values)
                        """,
                        "answer": """
                        - `xbar_usage = (12 + 18 + 21 + 9 + 30) / 5 = 90 / 5 = 18`.
                        - 이 값은 모집단 평균 `mu_usage`의 추정값이다.
                        - 표본 5명만 본 값이므로 전체 고객의 진짜 평균 `mu_usage`가 정확히 18이라고 단정할 수 없다.
                        """,
                    },
                    {
                        "id": "B-3",
                        "title": "베르누이 확률변수 X와 ML feature matrix X",
                        "difficulty": "2.0",
                        "context": "고객 이탈 여부를 확률변수 `X`로 둔다. `X=1`이면 churn, `X=0`이면 non-churn이다.",
                        "given": "`p = 0.28`",
                        "questions": [
                            "`E[X]`는 얼마인가?",
                            "이 값이 현실에서 뜻하는 것은 무엇인가?",
                            "이 `X`와 ML에서의 feature matrix `X`는 같은 뜻인가?",
                        ],
                        "check": "통계 확률변수 X와 ML 입력행렬 X를 문맥으로 구분한다.",
                        "tutor": "여기서 X는 한 고객의 0/1 결과인가, 여러 feature column을 가진 행렬인가?",
                        "hint": """
                        # 힌트 전용
                        # Bernoulli random variable: X in {0, 1}
                        # E[X] = p
                        # ML feature matrix X는 보통 rows x features 형태다.
                        """,
                        "answer": """
                        - `E[X] = p = 0.28`.
                        - 현실 해석: 고객 1명이 이탈하는 사건을 성공으로 코딩하면 기대값은 이탈 확률이다.
                        - 통계의 `X`는 하나의 0/1 확률변수이고, ML의 `X`는 여러 row와 feature column으로 된 입력 행렬이다.
                        """,
                    },
                ],
            },
            {
                "label": "C",
                "title": "코드 skeleton 판단 문제",
                "problems": [
                    {
                        "id": "C-1",
                        "title": "X/y skeleton 채우기",
                        "difficulty": "1.5",
                        "context": "고객 이탈 예측용 DataFrame에서 입력과 정답을 분리하려 한다.",
                        "given": "빈칸이 있는 pandas skeleton",
                        "questions": [
                            "`X`에 들어갈 객체를 채워라.",
                            "`y`에 들어갈 객체를 채워라.",
                            "`X`와 `y`가 각각 현실에서 무엇을 뜻하는지 한 문장으로 설명하라.",
                        ],
                        "check": "feature matrix와 target vector를 분리한다.",
                        "tutor": "무엇을 근거로 무엇을 맞히는 구조인가?",
                        "hint": """
                        # 힌트 전용
                        feature_cols = ["age", "income", "usage_time", "payment_delay", "complaints"]
                        X = df[_____]
                        y = df[_____]
                        """,
                        "answer": """
                        ```python
                        X = df[feature_cols]
                        y = df["churn"]
                        ```
                        - `X`: 고객 속성 feature matrix.
                        - `y`: 고객별 이탈 여부 target vector.
                        - 오답: `X`에 `churn`을 넣어 target leakage를 만드는 것.
                        """,
                    },
                    {
                        "id": "C-2",
                        "title": "feature list에서 제거할 column 찾기",
                        "difficulty": "2.0",
                        "context": "아래 feature list를 그대로 모델에 넣으려 한다.",
                        "given": "`customer_id, age, income, usage_time, payment_delay, complaints, plan_type, churn`",
                        "questions": [
                            "반드시 제거해야 할 column을 고르라.",
                            "각 column을 제거해야 하는 이유를 설명하라.",
                            "남은 feature가 모두 바로 모델에 들어갈 수 있는지 dtype 관점에서 설명하라.",
                        ],
                        "check": "identifier, target 포함, 범주형 인코딩 필요성을 구분한다.",
                        "tutor": "이 column이 새 고객에게 일반화 가능한 설명변수인가, 정답 자체인가, 식별자인가?",
                        "hint": """
                        # 힌트 전용
                        feature_cols = ["customer_id", "age", "income", "usage_time", "payment_delay", "complaints", "plan_type", "churn"]
                        # TODO: 제거 후보를 identifier / target / dtype 처리 필요로 나눠라.
                        """,
                        "answer": """
                        - 제거: `customer_id`는 식별자, `churn`은 target 자체다.
                        - `plan_type`은 feature 후보지만 문자열 범주형이면 one-hot encoding 같은 전처리가 필요하다.
                        - 오답: `customer_id`를 숫자처럼 넣거나, `churn`을 X에 포함하는 것.
                        """,
                    },
                    {
                        "id": "C-3",
                        "title": "random_state 해석",
                        "difficulty": "2.0",
                        "context": "같은 데이터로 모델 비교 실험을 반복하려 한다.",
                        "given": "`train_test_split(..., test_size=0.2, random_state=42)`",
                        "questions": [
                            "`random_state=42`는 단순 장식 코드인가?",
                            "이 값을 빼면 어떤 문제가 생길 수 있는가?",
                            "모델 A와 모델 B를 비교할 때 왜 같은 split이 필요한가?",
                        ],
                        "check": "난수 고정은 재현성과 공정한 비교를 위한 장치다.",
                        "tutor": "실험을 다시 실행했을 때 train/test 구성이 바뀌면 무엇을 비교하기 어려워질까?",
                        "hint": """
                        # 힌트 전용
                        # random_state는 split, sampling, initialization의 재현성과 연결된다.
                        # TODO: 결과 재현 / 모델 비교 / 난수 변동을 구분해서 써라.
                        """,
                        "answer": """
                        - `random_state=42`는 장식이 아니라 난수 분할을 고정하는 재현성 장치다.
                        - 제거하면 실행할 때마다 train/test 구성이 바뀌어 metric 변동이 생길 수 있다.
                        - 모델 A/B 비교에서는 같은 split을 써야 모델 차이와 데이터 분할 운을 구분할 수 있다.
                        """,
                    },
                ],
            },
        ],
        "misconceptions": [
            "식별자인 `customer_id`를 feature로 넣는다.",
            "`churn` 같은 target을 `X`에 섞는다.",
            "`phat`를 `pi`라고 단정한다.",
            "통계 확률변수 `X`와 ML feature matrix `X`를 같은 것으로 본다.",
            "`random_state`를 결과와 무관한 장식으로 본다.",
        ],
        "tutor_hints": [
            "항상 unit -> row -> column -> target -> feature 순서로 묻는다.",
            "시간 기준점을 물어 leakage를 진단한다.",
            "기호가 나오면 모집단 값인지 표본 값인지 먼저 말하게 한다.",
        ],
    },
    {
        "base": "DS_G0_P0002",
        "phase": "Phase 1",
        "topic": "통계·EDA 압축",
        "goal": "표본에서 통계량을 계산하고, 상대도수·분할표·조건부비율·그래프 선택으로 EDA 질문을 번역한다.",
        "anchors": [
            "DS_PDF07_STATS:p002:L007",
            "DS_PDF07_STATS:p010:L004",
            "DS_PDF07_STATS:p012:L004",
            "DS_PDF06_VIS:p002:L005",
            "DS_PDF06_VIS:p006:L005",
            "DS_PDF06_VIS:p012:L007",
        ],
        "criteria": [
            "모집단/표본/모수/통계량을 구분한다.",
            "상대도수와 조건부비율을 계산하고 해석한다.",
            "P(A|B)와 P(B|A)의 방향을 분리한다.",
            "변수 유형과 질문에 맞는 그래프를 선택한다.",
            "상관, binwidth, 색상 scale의 해석 한계를 표시한다.",
        ],
        "problem_types": [
            {
                "label": "A",
                "title": "모수·통계량·기호 문제",
                "problems": [
                    {
                        "id": "A-1",
                        "title": "고객 사용시간 평균과 이탈률",
                        "difficulty": "1.5",
                        "context": "표본 고객 8명의 `usage_time`과 `churn`이 주어졌다.",
                        "given": "`usage_time = [10, 12, 15, 18, 18, 22, 25, 30]`, `churn = [0, 0, 1, 0, 1, 0, 0, 1]`",
                        "questions": [
                            "`xbar_usage`를 계산하라.",
                            "`phat_churn`을 계산하라.",
                            "`xbar_usage`와 `phat_churn`은 각각 어떤 모수를 추정하는가?",
                            "`sigma` 또는 `sigma^2`와 `s` 또는 `s^2`가 무엇이 다른지 설명하라.",
                        ],
                        "check": "표본 통계량과 모집단 모수를 구분한다.",
                        "tutor": "지금 손으로 계산한 값은 표본에서 나온 값인가, 전체 모집단의 진짜 값인가?",
                        "hint": """
                        # 힌트 전용
                        usage_time = [10, 12, 15, 18, 18, 22, 25, 30]
                        churn = [0, 0, 1, 0, 1, 0, 0, 1]
                        # xbar = sum(usage_time) / len(usage_time)
                        # phat = sum(churn) / len(churn)
                        """,
                        "answer": """
                        - `xbar_usage = 150 / 8 = 18.75`.
                        - `phat_churn = 3 / 8 = 0.375`.
                        - `xbar_usage`는 모집단 평균 `mu_usage`를 추정한다.
                        - `phat_churn`은 모집단 이탈률 `pi_churn`을 추정한다.
                        - `sigma`, `sigma^2`는 모집단 표준편차/분산이고 `s`, `s^2`는 표본 표준편차/분산이다.
                        - 오답: 표본 8명의 결과를 전체 고객의 진짜 평균/이탈률로 단정하는 것.
                        """,
                    },
                    {
                        "id": "A-2",
                        "title": "제조 불량 베르누이 변수",
                        "difficulty": "2.0",
                        "context": "제품 1개가 불량이면 `X=1`, 정상이면 `X=0`인 베르누이 확률변수로 둔다.",
                        "given": "`p = 0.08`",
                        "questions": [
                            "`E[X]`를 구하라.",
                            "이 `p`는 어떤 확률인가?",
                            "이 `X`와 ML feature matrix `X`를 혼동하면 어떤 문제가 생기는가?",
                        ],
                        "check": "베르누이 성공확률 p와 feature matrix X를 구분한다.",
                        "tutor": "여기서 X는 제품 하나의 0/1 결과인가, 여러 feature를 담은 입력행렬인가?",
                        "hint": """
                        # 힌트 전용
                        # Bernoulli X in {0, 1}
                        # E[X] = p
                        """,
                        "answer": """
                        - `E[X] = p = 0.08`.
                        - `p`는 제품 1개가 불량일 성공확률이다.
                        - 통계의 `X`는 0/1 확률변수이고 ML의 `X`는 `rows x features` 입력행렬이다. 혼동하면 target/feature 구조를 잘못 잡는다.
                        """,
                    },
                    {
                        "id": "A-3",
                        "title": "병원 재입원률 비교",
                        "difficulty": "2.5",
                        "context": "전체 퇴원 환자의 30일 내 재입원률 `pi`를 알고 싶다.",
                        "given": "A병원 표본 400명 중 80명 재입원, B병원 표본 120명 중 36명 재입원",
                        "questions": [
                            "A병원과 B병원의 표본 재입원률을 계산하라.",
                            "어느 병원이 높아 보이는가?",
                            "표본 크기 차이를 무시하고 단정하면 왜 위험한가?",
                            "이것은 인과 주장인가, 기술적 비교인가?",
                        ],
                        "check": "표본 비율 비교와 인과 주장을 분리한다.",
                        "tutor": "두 비율이 다르게 보일 때, 그것이 원인까지 말해 주나?",
                        "hint": """
                        # 힌트 전용
                        # A_phat = A_readmit / A_n
                        # B_phat = B_readmit / B_n
                        # 표본 구성과 병원 특성 차이를 함께 고려해야 한다.
                        """,
                        "answer": """
                        - A병원: `phat_A = 80 / 400 = 0.20`.
                        - B병원: `phat_B = 36 / 120 = 0.30`.
                        - 표본 기준으로는 B가 높아 보인다.
                        - 그러나 표본 크기, 환자 중증도, 병원 구성 차이를 확인하지 않으면 원인을 단정할 수 없다.
                        - 이는 인과 주장이 아니라 기술적 비교다.
                        """,
                    },
                ],
            },
            {
                "label": "B",
                "title": "도수분포·상대도수·분할표 문제",
                "problems": [
                    {
                        "id": "B-1",
                        "title": "앱 사용시간 상대도수",
                        "difficulty": "1.5",
                        "context": "30명의 하루 앱 사용시간을 구간별로 나눴다.",
                        "given": "`0~10: 6`, `10~20: 9`, `20~30: 8`, `30~40: 5`, `40~50: 2`",
                        "questions": [
                            "각 구간의 상대도수를 계산하라.",
                            "상대도수의 합이 얼마인지 확인하라.",
                            "이 자료에 적절한 그래프는 무엇인가?",
                        ],
                        "check": "relative frequency와 histogram을 연결한다.",
                        "tutor": "도수만 보지 말고 전체 30명 중 비율로 바꾸면 무엇이 보이나?",
                        "hint": """
                        # 힌트 전용
                        freq = [6, 9, 8, 5, 2]
                        total = sum(freq)
                        # rel_freq = [f / total for f in freq]
                        """,
                        "answer": """
                        - 상대도수: `0~10 = 6/30 = 0.20`, `10~20 = 9/30 = 0.30`, `20~30 = 8/30 = 0.267`, `30~40 = 5/30 = 0.167`, `40~50 = 2/30 = 0.067`.
                        - 합은 반올림 전 1.0이고, 소수 반올림 후에는 약간 벗어날 수 있다.
                        - 수치형 구간별 분포이므로 histogram이 적절하다.
                        """,
                    },
                    {
                        "id": "B-2",
                        "title": "요금제와 이탈 분할표",
                        "difficulty": "2.0",
                        "context": "요금제별 이탈 현황 분할표가 있다.",
                        "given": "Basic: churn=1 42, churn=0 78, 합계 120 / Plus: 30, 170, 200 / Premium: 12, 168, 180",
                        "questions": [
                            "각 요금제별 이탈률을 계산하라.",
                            "행비율인가 열비율인가?",
                            "어떤 요금제의 이탈률이 가장 높아 보이는가?",
                            "이 결과만으로 요금제가 이탈을 유발한다고 말할 수 있는가?",
                        ],
                        "check": "분할표에서 행 기준 조건부비율과 인과 해석을 구분한다.",
                        "tutor": "분모가 각 요금제의 합계인지, 전체 이탈자의 합계인지 먼저 확인했나?",
                        "hint": """
                        # 힌트 전용
                        # plan별 이탈률은 각 row 안에서 churn=1 / row_total로 계산한다.
                        """,
                        "answer": """
                        - Basic: `42 / 120 = 0.35`.
                        - Plus: `30 / 200 = 0.15`.
                        - Premium: `12 / 180 = 0.067`.
                        - 각 요금제 row 안에서 계산한 행 기준 조건부비율이다.
                        - Basic이 가장 높아 보이지만, 이 결과만으로 인과를 주장할 수 없다.
                        """,
                    },
                    {
                        "id": "B-3",
                        "title": "채널별 구매 전환 조건부확률",
                        "difficulty": "2.5",
                        "context": "마케팅 채널별 구매 전환 표가 있다.",
                        "given": "Search: purchase=1 90, purchase=0 210 / Social: 75, 425 / Email: 60, 140",
                        "questions": [
                            "`P(purchase=1 | channel=Search)`를 계산하라.",
                            "`P(channel=Search | purchase=1)`를 계산하라.",
                            "두 값이 왜 다른가?",
                            "마케팅 의사결정에서 더 중요한 값은 무엇인가? 상황을 가정해 설명하라.",
                        ],
                        "check": "P(A|B)와 P(B|A)의 방향을 혼동하지 않는다.",
                        "tutor": "조건부확률의 조건은 분모에 들어간다. 이번 분모는 무엇인가?",
                        "hint": """
                        # 힌트 전용
                        # P(purchase | Search): Search row 안에서 구매 비율
                        # P(Search | purchase): purchase=1 column 안에서 Search 비율
                        """,
                        "answer": """
                        - `P(purchase=1 | Search) = 90 / 300 = 0.30`.
                        - `P(Search | purchase=1) = 90 / (90 + 75 + 60) = 90 / 225 = 0.40`.
                        - 첫 값은 Search 유입자의 전환율이고, 둘째 값은 구매자 중 Search 출신 비중이다.
                        - 채널 효율을 비교하려면 보통 `P(purchase | channel)`이 중요하고, 구매자 구성 분석에는 `P(channel | purchase)`가 중요하다.
                        """,
                    },
                ],
            },
            {
                "label": "C",
                "title": "그래프 선택·해석 한계 문제",
                "problems": [
                    {
                        "id": "C-1",
                        "title": "income 단변량 분포",
                        "difficulty": "1.5",
                        "context": "변수 하나 `income`의 분포와 이상치 후보를 보고 싶다.",
                        "given": "`income`은 수치형 변수다.",
                        "questions": [
                            "어떤 그래프를 쓸 것인가?",
                            "각 그래프가 보여 주는 정보는 무엇인가?",
                            "히스토그램 해석에서 조심할 점은 무엇인가?",
                        ],
                        "check": "수치형 단변량에는 histogram/KDE/boxplot을 연결하고 binwidth 함정을 표시한다.",
                        "tutor": "변수가 하나인가 두 개인가, 그리고 수치형인가 범주형인가?",
                        "hint": """
                        # 힌트 전용
                        # numeric single variable -> distribution / spread / outlier 후보
                        # binwidth 또는 bins 설정에 따른 모양 변화도 확인한다.
                        """,
                        "answer": """
                        - 적절한 그래프: histogram, KDE, boxplot.
                        - histogram/KDE는 값의 몰림과 분포 모양을 보고, boxplot은 중앙값, IQR, 이상치 후보를 본다.
                        - 히스토그램은 binwidth/bins에 따라 모양이 달라질 수 있어 한 설정만 보고 분포를 단정하면 안 된다.
                        """,
                    },
                    {
                        "id": "C-2",
                        "title": "usage_time과 monthly_spend 관계",
                        "difficulty": "2.0",
                        "context": "`usage_time`이 늘수록 `monthly_spend`도 늘어나는지 보고 싶다.",
                        "given": "`usage_time`, `monthly_spend`는 둘 다 수치형 변수다.",
                        "questions": [
                            "어떤 그래프를 쓸 것인가?",
                            "그래프에서 확인할 패턴은 무엇인가?",
                            "상관이 보여도 바로 말하면 안 되는 해석은 무엇인가?",
                        ],
                        "check": "수치형-수치형 관계에는 scatter plot을 선택하고 상관과 인과를 구분한다.",
                        "tutor": "두 수치형 변수가 같이 움직이는지 보려면 어떤 좌표 그림이 필요한가?",
                        "hint": """
                        # 힌트 전용
                        # x축과 y축에 각각 하나의 수치형 변수를 둔다.
                        # 방향, 형태, 이상치, 군집을 따로 본다.
                        """,
                        "answer": """
                        - 산점도(scatter plot)가 적절하다.
                        - 방향, 선형/비선형 형태, 이상치, 군집을 본다.
                        - 상관이 보여도 `usage_time`이 `monthly_spend`를 원인으로 증가시킨다고 단정하면 안 된다.
                        """,
                    },
                    {
                        "id": "C-3",
                        "title": "plan_type, region, churn 다변량 패턴",
                        "difficulty": "2.5",
                        "context": "`plan_type`, `region`, `churn`을 함께 보고 싶다.",
                        "given": "`plan_type`, `region`, `churn`은 범주형 변수다.",
                        "questions": [
                            "어떤 집계 구조를 먼저 만들 것인가?",
                            "어떤 시각화 접근이 적절한가?",
                            "색상 scale이나 비율 해석에서 조심할 점은 무엇인가?",
                        ],
                        "check": "crosstab/pivot과 heatmap을 연결하고 색상 scale 과해석을 피한다.",
                        "tutor": "세 범주형 변수의 조합을 한 번에 보려면 먼저 어떤 표를 만들어야 할까?",
                        "hint": """
                        # 힌트 전용
                        # pd.crosstab 또는 pivot_table로 행렬형 값을 만든 뒤 색으로 볼 수 있다.
                        # normalize 기준이 index인지 columns인지 확인한다.
                        """,
                        "answer": """
                        - `pd.crosstab([region, plan_type], churn, normalize=\"index\")` 또는 pivot table로 조합별 이탈률을 만든다.
                        - 행렬형 값은 heatmap으로 볼 수 있다.
                        - normalize 기준과 색상 scale을 확인해야 하며, 색이 진하다고 인과나 중요도를 단정하면 안 된다.
                        """,
                    },
                ],
            },
        ],
        "misconceptions": [
            "표본 평균을 모집단 평균으로 단정한다.",
            "표본 비율을 모집단 비율로 단정한다.",
            "행비율과 열비율을 바꿔 해석한다.",
            "히스토그램 binwidth를 바꾸지 않고 분포 모양을 단정한다.",
            "상관을 인과로 말한다.",
        ],
        "tutor_hints": [
            "계산 전 기호가 모수인지 통계량인지 말하게 한다.",
            "조건부확률은 조건을 분모로 쓰게 한다.",
            "그래프 선택은 변수 수와 변수 타입부터 묻게 한다.",
        ],
    },
    {
        "base": "DS_G0_P0003",
        "phase": "Phase 2",
        "topic": "지도학습 입구와 평가 지표",
        "goal": "정답 y가 있는 문제를 X/y, train/test, classification/regression, leakage, confusion matrix, metric으로 번역한다.",
        "anchors": [
            "DS_PDF08_ML1:p002:L005",
            "DS_PDF08_ML1:p034:L004",
            "DS_PDF08_ML1:p045:L004",
            "DS_PDF08_ML1:p017:L005",
            "DS_PDF06_CODE:p036:L013",
        ],
        "criteria": [
            "target 유형으로 classification/regression을 판별한다.",
            "X/y를 분리하고 target leakage를 피한다.",
            "train/test split 뒤 train 기준으로 전처리를 fit한다.",
            "TP/TN/FP/FN에서 accuracy, precision, recall, F1을 계산한다.",
            "baseline, class imbalance, FN/FP 비용을 현실 문제와 연결한다.",
        ],
        "problem_types": [
            {
                "label": "A",
                "title": "문제 유형 라우팅 문제",
                "problems": [
                    {
                        "id": "A-1",
                        "title": "고객 이탈 예측",
                        "difficulty": "1.5",
                        "context": "고객 이탈 방지 캠페인을 위해 `churn`을 예측하려 한다.",
                        "given": "unit: 고객 / target: `churn={0,1}` / features: `age, income, usage_time, payment_delay, complaints`",
                        "questions": [
                            "classification인가 regression인가?",
                            "`X`와 `y`를 정의하라.",
                            "이탈 고객을 놓치는 비용이 크면 어떤 metric을 우선 볼 것인가?",
                            "전체 고객의 80%가 non-churn이면 baseline을 어떻게 생각해야 하는가?",
                        ],
                        "check": "숫자형 0/1 target을 regression으로 착각하지 않는다.",
                        "tutor": "target이 숫자로 저장되어 있다는 사실과 target이 범주라는 사실을 구분했나?",
                        "hint": """
                        # 힌트 전용
                        # target 값이 0/1 숫자여도 의미가 class label이면 분류 문제일 수 있다.
                        # baseline은 가장 단순한 규칙의 성능과 비교한다.
                        """,
                        "answer": """
                        - `churn`은 0/1 class label이므로 classification.
                        - `X = df[["age", "income", "usage_time", "payment_delay", "complaints"]]`, `y = df["churn"]`.
                        - 이탈 고객을 놓치는 FN 비용이 크면 recall을 우선 본다.
                        - non-churn이 80%이면 전부 non-churn으로 예측해도 accuracy 0.80 baseline이 가능하므로 accuracy만 보면 부족하다.
                        """,
                    },
                    {
                        "id": "A-2",
                        "title": "전력 수요 예측",
                        "difficulty": "2.0",
                        "context": "내일 전력 사용량을 예측하려 한다.",
                        "given": "unit: 시간 단위 관측치 / target: `next_day_power_usage_kwh` / features: `temperature, humidity, weekday, previous_usage`",
                        "questions": [
                            "classification인가 regression인가?",
                            "target이 연속형이라는 근거는 무엇인가?",
                            "accuracy를 쓰면 왜 안 되는가?",
                        ],
                        "check": "연속형 target에는 회귀 지표를 써야 한다.",
                        "tutor": "맞혀야 하는 값이 class 이름인가, kWh라는 연속 숫자인가?",
                        "hint": """
                        # 힌트 전용
                        # continuous target -> regression
                        # 분류 metric과 회귀 metric을 구분한다.
                        """,
                        "answer": """
                        - `next_day_power_usage_kwh`는 kWh 단위의 연속값이므로 regression.
                        - 예측값이 0/1 class가 아니라 실수량이다.
                        - accuracy는 class label의 맞고 틀림을 세는 지표라 회귀 문제에 직접 맞지 않는다. MAE, RMSE, R2 같은 회귀 지표를 쓴다.
                        """,
                    },
                    {
                        "id": "A-3",
                        "title": "뉴스 기사 주제 분류",
                        "difficulty": "2.5",
                        "context": "기사 1개의 주제를 맞히려 한다.",
                        "given": "unit: 기사 1개 / target: `topic={politics, economy, sports, tech}` / feature 후보: `article_text`",
                        "questions": [
                            "text는 그대로 모델에 들어가는가?",
                            "`X`는 어떻게 만들어야 하는가?",
                            "이 문제는 supervised인가 unsupervised인가?",
                            "train/test 경계와 text vectorization은 어떻게 연결되는가?",
                        ],
                        "check": "텍스트를 수치 feature로 바꾸고, 벡터화도 train/test 경계를 지킨다.",
                        "tutor": "문자열 원문을 모델이 바로 계산할 수 있는 숫자 행렬로 보나?",
                        "hint": """
                        # 힌트 전용
                        # text -> token/count/TF-IDF/embedding -> numeric feature matrix
                        # vectorizer도 train 기준으로 fit해야 한다.
                        """,
                        "answer": """
                        - 일반적인 ML 모델에는 raw text를 그대로 넣지 않고 Bag-of-Words, TF-IDF, embedding 같은 수치 feature로 변환한다.
                        - `X`는 문서별 수치 벡터 행렬이고 `y`는 topic label이다.
                        - 정답 topic이 있으므로 supervised classification.
                        - vectorizer는 train text에 fit하고 test text에는 transform만 적용해야 leakage를 피한다.
                        """,
                    },
                ],
            },
            {
                "label": "B",
                "title": "confusion matrix 계산 문제",
                "problems": [
                    {
                        "id": "B-1",
                        "title": "이탈 예측 기본형",
                        "difficulty": "1.5",
                        "context": "고객 이탈 모델의 test 결과가 confusion matrix 숫자로 주어졌다.",
                        "given": "`TP=32`, `TN=140`, `FP=18`, `FN=10`",
                        "questions": [
                            "Accuracy를 계산하라.",
                            "Precision을 계산하라.",
                            "Recall을 계산하라.",
                            "F1을 계산하라.",
                            "FN의 현실 의미를 설명하라.",
                        ],
                        "check": "공식 대입과 현실 오류 해석을 연결한다.",
                        "tutor": "TP, FP, FN이 각각 어떤 현실 오류 또는 성공을 뜻하는지 먼저 말해볼까?",
                        "hint": """
                        # 힌트 전용
                        TP, TN, FP, FN = 32, 140, 18, 10
                        # total = TP + TN + FP + FN
                        # accuracy = (TP + TN) / total
                        # precision = TP / (TP + FP)
                        # recall = TP / (TP + FN)
                        # f1 = 2 * precision * recall / (precision + recall)
                        """,
                        "answer": """
                        - Total = `32 + 140 + 18 + 10 = 200`.
                        - Accuracy = `(32 + 140) / 200 = 0.86`.
                        - Precision = `32 / (32 + 18) = 32 / 50 = 0.64`.
                        - Recall = `32 / (32 + 10) = 32 / 42 = 0.762`.
                        - F1 = `2 * 0.64 * 0.762 / (0.64 + 0.762) = 0.696`.
                        - FN은 실제 이탈 고객인데 모델이 non-churn이라고 놓친 경우다.
                        """,
                    },
                    {
                        "id": "B-2",
                        "title": "의료 재입원 예측",
                        "difficulty": "2.0",
                        "context": "30일 내 재입원 위험 환자를 찾는 모델이다.",
                        "given": "`TP=45`, `TN=820`, `FP=60`, `FN=75`",
                        "questions": [
                            "Accuracy가 높아 보이는가?",
                            "Recall은 얼마인가?",
                            "의료 현장에서 왜 recall이 중요할 수 있는가?",
                            "accuracy만 보고 좋은 모델이라고 판단하면 어떤 문제가 있는가?",
                        ],
                        "check": "class imbalance에서 accuracy와 recall을 분리한다.",
                        "tutor": "실제 재입원 환자 중 모델이 잡아낸 비율은 어느 metric인가?",
                        "hint": """
                        # 힌트 전용
                        # recall = TP / (TP + FN)
                        # 고위험 환자를 놓치는 FN 비용을 생각한다.
                        """,
                        "answer": """
                        - Total = 1000, Accuracy = `(45 + 820) / 1000 = 0.865`.
                        - Recall = `45 / (45 + 75) = 45 / 120 = 0.375`.
                        - 정확도는 86.5%로 높아 보이지만 실제 재입원 환자의 37.5%만 잡았다.
                        - 의료에서는 고위험 환자를 놓치는 FN 비용이 클 수 있어 recall을 함께 봐야 한다.
                        """,
                    },
                    {
                        "id": "B-3",
                        "title": "사기 거래 탐지",
                        "difficulty": "2.5",
                        "context": "사기 거래 탐지 모델의 요약 결과가 주어졌다.",
                        "given": "전체 거래 10,000건, 실제 사기 80건, 모델이 사기라고 예측한 거래 100건, 그중 실제 사기 50건",
                        "questions": [
                            "TP, FP, FN, TN을 채워라.",
                            "Precision과 Recall을 계산하라.",
                            "Accuracy를 계산하라.",
                            "accuracy만 보면 왜 위험한가?",
                        ],
                        "check": "불균형 데이터에서 confusion matrix 전체를 복원한다.",
                        "tutor": "모델이 사기라고 한 100건 안에서 진짜 사기와 아닌 거래를 먼저 나눌 수 있나?",
                        "hint": """
                        # 힌트 전용
                        total = 10000
                        actual_fraud = 80
                        predicted_fraud = 100
                        true_fraud_in_predicted = 50
                        # TP부터 정한 뒤 FP, FN, TN 순서로 채운다.
                        """,
                        "answer": """
                        - TP = 50.
                        - FP = `100 - 50 = 50`.
                        - FN = `80 - 50 = 30`.
                        - TN = `10000 - 50 - 50 - 30 = 9870`.
                        - Precision = `50 / (50 + 50) = 0.50`.
                        - Recall = `50 / (50 + 30) = 0.625`.
                        - Accuracy = `(50 + 9870) / 10000 = 0.992`.
                        - accuracy는 99.2%지만 사기가 매우 드문 불균형 데이터라 대부분 정상이라고 해도 높아 보일 수 있다.
                        """,
                    },
                ],
            },
            {
                "label": "C",
                "title": "pipeline·leakage 판단 문제",
                "problems": [
                    {
                        "id": "C-1",
                        "title": "올바른 학습 파이프라인",
                        "difficulty": "1.5",
                        "context": "아래 학습 순서가 적절한지 판단한다.",
                        "given": "`X/y 분리 -> train/test split -> train에 scaler fit -> train/test transform -> model fit -> test predict -> metric`",
                        "questions": [
                            "이 순서는 맞는가?",
                            "`fit`, `transform`, `predict`, `metric`의 역할을 각각 설명하라.",
                            "전처리를 train 기준으로 fit하는 이유를 설명하라.",
                        ],
                        "check": "전처리와 평가가 train/test 경계를 지키는지 본다.",
                        "tutor": "scaler가 test data의 평균과 표준편차를 미리 보면 어떤 문제가 생길까?",
                        "hint": """
                        # 힌트 전용
                        # fit: 학습 데이터에서 규칙/파라미터를 배운다.
                        # transform: 배운 변환 규칙을 적용한다.
                        # predict: 학습된 모델로 추론한다.
                        # metric: test 결과를 평가한다.
                        """,
                        "answer": """
                        - 순서는 맞다.
                        - `fit`: train data에서 scaler나 model의 규칙을 배운다.
                        - `transform`: 학습된 변환 규칙을 train/test에 적용한다.
                        - `predict`: 학습된 모델로 test target을 예측한다.
                        - `metric`: test 예측과 정답을 비교해 성능을 해석한다.
                        - test 정보가 전처리에 들어가면 일반화 평가가 오염된다.
                        """,
                    },
                    {
                        "id": "C-2",
                        "title": "결측치 대체 leakage",
                        "difficulty": "2.0",
                        "context": "다음 전처리 순서의 오류를 찾는다.",
                        "given": "`전체 df에서 income 평균 계산 -> 전체 df의 결측치를 income 평균으로 채움 -> train/test split -> model fit`",
                        "questions": [
                            "어떤 점이 잘못되었는가?",
                            "올바른 순서로 고쳐 써라.",
                            "이 오류가 test metric에 어떤 영향을 줄 수 있는가?",
                        ],
                        "check": "imputer를 split 전에 전체 데이터에 fit하는 leakage를 찾는다.",
                        "tutor": "결측치 대체에 쓴 평균값이 test data까지 보고 계산된 값인가?",
                        "hint": """
                        # 힌트 전용
                        # split first -> imputer.fit(train) -> imputer.transform(train/test)
                        """,
                        "answer": """
                        - 전체 df에서 평균을 계산했으므로 test 정보가 전처리에 들어갔다.
                        - 올바른 순서: `X/y 분리 -> train/test split -> train income 평균으로 imputer fit -> train/test transform -> model fit -> test metric`.
                        - test 정보를 미리 본 효과가 생겨 metric이 실제 새 데이터 성능보다 좋아 보일 수 있다.
                        """,
                    },
                    {
                        "id": "C-3",
                        "title": "target 포함과 scaler leakage가 함께 있는 코드",
                        "difficulty": "2.5",
                        "context": "아래 코드에서 모델링 오류를 찾는다.",
                        "given": "feature list와 scaling 코드",
                        "questions": [
                            "`feature_cols`에서 잘못된 column이 있는가?",
                            "scaler 적용 순서에 어떤 leakage가 있는가?",
                            "올바른 순서를 문장으로 다시 써라.",
                            "이 오류가 특히 왜 위험한가?",
                        ],
                        "check": "target을 X에 넣는 오류와 split 전 scaling 오류를 동시에 찾는다.",
                        "tutor": "이 코드는 정답을 feature에 넣거나, test 정보를 전처리에 미리 쓰고 있나?",
                        "hint": """
                        # 힌트 전용
                        feature_cols = ["age", "income", "usage_time", "payment_delay", "complaints", "churn"]
                        X = df[feature_cols]
                        y = df["churn"]

                        # 아래 순서에서 fit 시점을 확인하라.
                        scaler = StandardScaler()
                        X_scaled = scaler.fit_transform(X[numeric_cols])

                        X_train, X_test, y_train, y_test = train_test_split(
                            X_scaled, y, test_size=0.2, random_state=42
                        )
                        """,
                        "answer": """
                        - `feature_cols`에 target인 `churn`이 들어가 있어 target leakage가 발생한다.
                        - `scaler.fit_transform`을 train/test split 전에 전체 X에 적용했으므로 preprocessing leakage도 있다.
                        - 올바른 순서: `feature_cols`에서 `churn` 제거 -> `X/y` 분리 -> train/test split -> train에 scaler fit -> train/test transform -> model fit -> test predict -> metric.
                        - target을 X에 넣으면 모델이 정답을 보고 학습하는 수준이므로 test 성능이 비정상적으로 높아질 수 있다.
                        """,
                    },
                ],
            },
        ],
        "misconceptions": [
            "0/1로 저장된 target을 연속형 회귀 target으로 착각한다.",
            "train/test split 전에 scaler나 imputer를 fit한다.",
            "target을 feature에 포함한다.",
            "accuracy만 보고 좋은 모델이라고 판단한다.",
            "FN과 FP의 현실 비용을 구분하지 않는다.",
        ],
        "tutor_hints": [
            "문제마다 unit, target, target type을 먼저 말하게 한다.",
            "fit은 train에서만, transform은 train/test에 적용이라는 문장을 반복한다.",
            "metric은 현실 오류 비용과 연결해 고르게 한다.",
        ],
    },
]


QUALITY_CHECKLIST = [
    "Phase별 문제 유형이 3개 이하인가?",
    "각 유형 문항이 3개 이하인가?",
    "난이도 1.5 이상 문제에 계산 또는 함정이 있는가?",
    "μ, π, x̄, p̂, X, y가 모두 등장하는가?",
    "feature/target 구분 문제가 있는가?",
    "relative frequency 또는 contingency table 문제가 있는가?",
    "chart selection 문제가 있는가?",
    "train/test leakage 문제가 있는가?",
    "confusion matrix 문제가 있는가?",
    "각 문제에 현실 해석 질문이 있는가?",
]


SYMBOL_TABLE = """
## 기호 고정표

이 Phase 묶음에서는 아래 기호를 일관되게 쓴다.

| 기호 | 뜻 | 사용 맥락 |
|---|---|---|
| `μ` | 모집단 평균, population mean | 전체 고객의 진짜 평균 사용시간 |
| `σ`, `σ²` | 모집단 표준편차와 분산 | 전체 모집단의 퍼짐 |
| `π` | 모집단 비율, population proportion | 전체 고객의 진짜 이탈률 |
| `p` | 확률 또는 베르누이 성공확률 | 고객 1명이 이탈할 확률 |
| `x̄` | 표본 평균, sample mean | 표본 고객의 평균 사용시간 |
| `s`, `s²` | 표본 표준편차와 분산 | 표본의 퍼짐 |
| `p̂` | 표본 비율, sample proportion | 표본 고객 중 이탈자 비율 |
| `X` | 통계에서는 확률변수, ML에서는 feature matrix | 문맥으로 구분한다 |
| `y` | target vector | 모델이 맞히려는 정답 |

주의: `π`는 모집단의 알 수 없는 진짜 비율이고, `p̂`는 표본에서 계산한 비율이다. 통계의 `X`와 ML의 `X`도 같은 글자지만 뜻이 다르다.
"""


def problem_markdown(phase: dict, ptype: dict, problem: dict) -> str:
    questions = "\n".join(f"{idx}. {q}" for idx, q in enumerate(problem["questions"], 1))
    return f"""
    ### {problem['id']}. {problem['title']} / 난이도 {problem['difficulty']}

    **문제 맥락**
    {problem['context']}

    **주어진 데이터 또는 숫자**
    {problem['given']}

    **질문**
    {questions}

    **의도된 함정 또는 확인 개념**
    {problem['check']}

    **튜터가 학생에게 던질 첫 질문**
    {problem['tutor']}
    """


def answer_markdown(problem: dict) -> str:
    return f"""
    ### {problem['id']}. {problem['title']}

    **정답**

    {dedent(problem['answer']).strip()}

    **근거**
    - 문제의 unit, target, feature, 통계량/모수 또는 metric을 먼저 고정한다.
    - 관련 source anchor는 노트북 상단의 source anchors를 따른다.

    **자주 하는 오답**
    - {problem['check']}를 놓치고 표면적인 column 이름이나 큰 metric 값만 보고 판단한다.

    **최종 답안형**
    - 계산 문제는 `공식 -> 대입 -> 계산 -> 단위/비율 -> 현실 해석` 순서로 쓴다.
    - 구조 판단 문제는 `unit -> target -> feature -> 제외/주의 column -> 이유` 순서로 쓴다.
    """


def make_problem_nb(phase: dict) -> dict:
    source_basis = "\n".join(f"- {p}" for p in COMMON_SOURCE_BASIS)
    anchors = "\n".join(f"- `{a}`" for a in phase["anchors"])
    criteria = "\n".join(f"- {c}" for c in phase["criteria"])
    cells: list[dict] = [
        md_cell(
            f"""
            # {phase['base']}

            ## 0. 학습 범위
            - Gate: G0~G4 데이터사이언스 입구 고정
            - Phase: {phase['phase']}
            - Topic: {phase['topic']}
            - Goal: {phase['goal']}
            - Source basis:
            {source_basis}
            - Output language: Korean
            - Code mode: hint_only

            ## source anchors
            {anchors}
            """
        ),
        md_cell(
            """
            ## 1. 작성 규칙
            - 풀이용 노트북에는 정답이 포함되어 있지 않다.
            - 문항별로 `개념 -> 계산 또는 판단 -> 현실 해석 -> 오답 위험` 순서로 답한다.
            - code cell은 힌트 전용이다. 빈칸, TODO, 확인 방향만 제공한다.
            - 답안을 쓰기 전 항상 `unit -> row/column -> feature/target -> 통계량/모수 -> EDA -> X/y -> train/test -> metric` 중 현재 문제가 어디에 있는지 표시한다.
            """
        ),
        md_cell(
            f"""
            ## 2. 채점 기준
            {criteria}
            """
        ),
        md_cell(
            """
            ## 공통 mock customer dataset
            실제 데이터가 아닌 학습용 mock schema다.

            ```text
            customer_id, age, income, usage_time, payment_delay, complaints,
            plan_type, region, tenure_months, monthly_spend, review_text, churn
            ```

            기본 해석:
            - row meaning: 고객 1명
            - target 후보: `churn`
            - feature 후보: 고객의 행동, 결제, 요금제, 지역, 사용량 관련 변수
            - 제외 후보: `customer_id`
            - text feature 후보: `review_text`
            - `churn`은 0/1 범주형 target이므로 classification 문제
            """
        ),
        md_cell(SYMBOL_TABLE),
        md_cell("## 3. 문제 세트"),
    ]

    for ptype in phase["problem_types"]:
        cells.append(md_cell(f"## 문제 유형 {ptype['label']}. {ptype['title']}"))
        for problem in ptype["problems"]:
            cells.append(md_cell(problem_markdown(phase, ptype, problem)))
            cells.append(code_cell(problem["hint"]))
            cells.append(
                md_cell(
                    f"""
                    ### 내 답안: {problem['id']}

                    - 현재 노드/개념:
                    - unit:
                    - row/column 해석:
                    - feature/target 또는 모수/통계량:
                    - 계산 또는 판단:
                    - 현실 해석:
                    - 오답 위험:
                    """
                )
            )

    misconceptions = "\n".join(f"- {m}" for m in phase["misconceptions"])
    tutor_hints = "\n".join(f"- {h}" for h in phase["tutor_hints"])
    checklist = "\n".join(f"- [x] {item}" for item in QUALITY_CHECKLIST)
    cells.extend(
        [
            md_cell(
                f"""
                ## 오답 위험 요약
                {misconceptions}
                """
            ),
            md_cell(
                f"""
                ## 튜터용 힌트
                {tutor_hints}
                """
            ),
            md_cell(
                f"""
                ## 정답본 분리 여부
                - 정답본은 `{phase['base']}_answer.ipynb`에만 있다.
                - 먼저 이 문제지를 풀고, 채점 또는 오답 진단 때만 정답본을 연다.
                """
            ),
            md_cell(
                f"""
                ## 최종 품질 체크
                {checklist}
                """
            ),
        ]
    )
    return notebook(cells)


def make_answer_nb(phase: dict) -> dict:
    anchors = "\n".join(f"- `{a}`" for a in phase["anchors"])
    criteria = "\n".join(f"- {c}" for c in phase["criteria"])
    cells: list[dict] = [
        md_cell(
            f"""
            # {phase['base']}_answer

            ## 0. 정답본 범위
            - Gate: G0~G4 데이터사이언스 입구 고정
            - Phase: {phase['phase']}
            - Topic: {phase['topic']}
            - Problem notebook: `{phase['base']}.ipynb`
            - Correct answers included: Yes
            - Output language: Korean

            이 파일은 정답본이다. 먼저 `{phase['base']}.ipynb`를 푼 뒤 채점 또는 오답 진단용으로 연다.

            ## source anchors
            {anchors}
            """
        ),
        md_cell(SYMBOL_TABLE),
        md_cell(
            f"""
            ## 1. 핵심 기준표
            {criteria}
            """
        ),
        md_cell("## 2. 문항별 정답"),
    ]

    for ptype in phase["problem_types"]:
        cells.append(md_cell(f"## 문제 유형 {ptype['label']}. {ptype['title']}"))
        for problem in ptype["problems"]:
            cells.append(md_cell(answer_markdown(problem)))

    scoring = []
    for ptype in phase["problem_types"]:
        for problem in ptype["problems"]:
            scoring.append(
                f"- {problem['id']}: 핵심 개념 식별 30%, 계산/코드 판단 30%, 현실 해석 25%, 오답 위험 언급 15%"
            )
    scoring_md = "\n".join(scoring)
    misconceptions = "\n".join(f"- {m}: 오류가 나오면 정의를 다시 말하게 한 뒤, 같은 구조의 숫자나 column을 바꾼 재시도 문제를 낸다." for m in phase["misconceptions"])
    next_phase = {
        "Phase 0": "다음은 Phase 1 통계·EDA 압축으로 넘어가 표본 평균, 표본 비율, 상대도수, 분할표, 그래프 선택을 푼다.",
        "Phase 1": "다음은 Phase 2 지도학습 입구로 넘어가 X/y, train/test, metric, leakage를 푼다.",
        "Phase 2": "다음은 선형회귀/로지스틱 회귀, threshold, SVM/kNN/tree 비교로 넘어간다.",
    }[phase["phase"]]
    checklist = "\n".join(f"- [x] {item}" for item in QUALITY_CHECKLIST)
    cells.extend(
        [
            md_cell(
                f"""
                ## 3. 채점 기준
                {scoring_md}

                부분점 기준:
                - 계산값만 맞고 해석이 없으면 감점한다.
                - 구조 판단에서 unit 또는 target을 쓰지 않으면 감점한다.
                - leakage 문제에서 정보 발생 시점이나 train/test 경계를 설명하지 않으면 감점한다.
                """
            ),
            md_cell(
                f"""
                ## 4. 오답튜터 기준표
                {misconceptions}
                """
            ),
            md_cell(
                f"""
                ## 5. 다음 Phase 연결
                {next_phase}
                """
            ),
            md_cell(
                f"""
                ## 최종 품질 체크
                {checklist}
                """
            ),
        ]
    )
    return notebook(cells)


def validate_notebook(path: Path) -> None:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["nbformat"] == 4
    assert data["cells"], f"empty notebook: {path}"
    headings = "\n".join("".join(cell.get("source", "")) for cell in data["cells"] if cell.get("cell_type") == "markdown")
    assert "## 0. 학습 범위" in headings or "## 0. 정답본 범위" in headings
    if not path.name.endswith("_answer.ipynb"):
        forbidden = ["**정답**", "## 2. 문항별 정답", "최종 답안형"]
        for token in forbidden:
            assert token not in headings, f"problem notebook leaks answer marker {token}: {path}"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for phase in PHASES:
        problem_path = OUT_DIR / f"{phase['base']}.ipynb"
        answer_path = OUT_DIR / f"{phase['base']}_answer.ipynb"
        problem_path.write_text(json.dumps(make_problem_nb(phase), ensure_ascii=False, indent=1), encoding="utf-8")
        answer_path.write_text(json.dumps(make_answer_nb(phase), ensure_ascii=False, indent=1), encoding="utf-8")
        written.extend([problem_path, answer_path])

    for path in written:
        validate_notebook(path)

    print(json.dumps({"written": [str(p.relative_to(ROOT)) for p in written]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
