---
name: ipynb-problem-generation
description: Create Korean Jupyter Notebook problem sets and matching answer notebooks for a learning Gate/Phase. Use when the user asks to generate IPYNB study problems, drills, worksheets, phase notebooks, code-hint notebooks, or paired problem/answer notebooks while keeping each Phase to exactly one solved/problem notebook and one answer notebook.
---

# IPYNB Problem Generation Skill

## Purpose

Act as a local agent that creates learning Jupyter Notebook problem sets. Given a Gate, Phase, topic, learning goal, problem direction, and code-hint level, create a problem `.ipynb` plus a separate answer `.ipynb`.

This skill is domain-neutral. Default naming examples use Machine Learning / Data Science Foundations.

## Language

Write all user-facing output, notebook Markdown, problem text, grading criteria, and answer explanations in Korean.

Keep code identifiers, variable names, function names, library names, file paths, CLI output, official errors, direct quotes, and clearer English technical terms as-is.

## Fixed Artifact Policy

Keep each Phase to at most two artifacts:

```text
1. Problem/solving notebook: <COURSE>_<GATE>_<PHASE>.ipynb
2. Answer notebook: <COURSE>_<GATE>_<PHASE>_answer.ipynb
```

Example:

```text
ML_G0_P0001.ipynb
ML_G0_P0001_answer.ipynb
```

Do not create separate `corrected`, `annotated`, `mistake_review`, or `report` files unless the user explicitly requests additional files.

## Auxiliary Dataset Policy

The default notebook artifact count remains two files per Phase:

```text
1. Problem/solving notebook: <COURSE>_<GATE>_<PHASE>.ipynb
2. Answer notebook: <COURSE>_<GATE>_<PHASE>_answer.ipynb
```

However, when the Phase requires hands-on code practice, the skill may also generate small importable local data assets.

These data assets are not counted as additional notebook artifacts. They must be stored under a phase-specific data directory:

```text
data/<COURSE>_<GATE>_<PHASE>/
```

Example:

```text
ML_G0_P0002.ipynb
ML_G0_P0002_answer.ipynb
data/ML_G0_P0002/students_scores.csv
data/ML_G0_P0002/customer_purchase.csv
data/ML_G0_P0002/traffic_congestion.csv
data/ML_G0_P0002/mock_images.npz
```

Do not create separate grading reports, corrected notebooks, annotated notebooks, or mistake-review notebooks unless explicitly requested.

## Dataset Generation Rule

If the user asks for problems that require immediate notebook execution, generate deterministic local datasets that the problem notebook can import directly.

Dataset generation requirements:

```text
1. Use small, deterministic datasets.
2. Use fixed seeds for synthetic arrays.
3. Keep schemas simple and documented in the notebook.
4. Store all data files under data/<COURSE>_<GATE>_<PHASE>/.
5. Ensure the problem notebook can import the data with relative paths.
6. Include a setup/check cell that verifies file existence and shape.
7. Do not put answer logic in the problem notebook.
```

Recommended relative path pattern:

```python
DATA_DIR = "data/ML_G0_P0002"
```

Allowed data file types:

```text
.csv   # tabular practice data
.json  # small metadata or label mapping
.npy   # single NumPy array
.npz   # multiple NumPy arrays
```

Avoid large binary files.

## Problem Notebook Data Setup Cell

When data assets are generated, the problem notebook should include an early setup cell.

The setup cell may include import and file existence checks. This is not considered solution code.

Allowed setup code:

```python
from pathlib import Path
import pandas as pd
import numpy as np

DATA_DIR = Path("data/ML_G0_P0002")

print(DATA_DIR.exists())
print(sorted(p.name for p in DATA_DIR.iterdir()))
```

Allowed data loading hints:

```python
# 힌트:
# students = pd.read_csv(DATA_DIR / "students_scores.csv")
# customers = pd.read_csv(DATA_DIR / "customer_purchase.csv")
# traffic = pd.read_csv(DATA_DIR / "traffic_congestion.csv")
# images = np.load(DATA_DIR / "mock_images.npz")
```

Forbidden in the problem notebook:

```python
# 정답 로직
# 완성된 feature_cols / target_col 전체 정답
# 모든 shape 해석 출력
# 문제의 정답을 직접 말하는 코드
```

## Answer Notebook Data Policy

The answer notebook may include full data loading and short corrected code examples when useful.

The answer notebook should include:

```text
1. Dataset schema
2. Correct X/y split
3. Expected dtypes
4. Expected shapes
5. Common wrong code patterns
6. Corrected code snippets if needed
```

## Data Asset Validation

After generating notebooks and data assets, validate all files.

Required validation:

```bash
python3 -m json.tool <COURSE>_<GATE>_<PHASE>.ipynb > /dev/null
python3 -m json.tool <COURSE>_<GATE>_<PHASE>_answer.ipynb > /dev/null
```

Also run a lightweight data import check:

```python
from pathlib import Path
import pandas as pd
import numpy as np

data_dir = Path("data/ML_G0_P0002")

assert (data_dir / "students_scores.csv").exists()
assert (data_dir / "customer_purchase.csv").exists()
assert (data_dir / "traffic_congestion.csv").exists()
assert (data_dir / "mock_images.npz").exists()

students = pd.read_csv(data_dir / "students_scores.csv")
customers = pd.read_csv(data_dir / "customer_purchase.csv")
traffic = pd.read_csv(data_dir / "traffic_congestion.csv")
images = np.load(data_dir / "mock_images.npz")

assert students.shape[0] > 0
assert customers.shape[0] > 0
assert traffic.shape[0] > 0
assert "images_gray" in images.files
assert "images_flat" in images.files
```

## Final Report Addition

When data assets are generated, the final Korean report must include them.

Example:

```text
생성 파일:
- ML_G0_P0002.ipynb
- ML_G0_P0002_answer.ipynb

생성 데이터:
- data/ML_G0_P0002/students_scores.csv
- data/ML_G0_P0002/customer_purchase.csv
- data/ML_G0_P0002/traffic_congestion.csv
- data/ML_G0_P0002/mock_images.npz

검증:
- ipynb JSON parse 통과
- CSV import 통과
- NPZ import 통과
- 풀이용 노트북 정답 미포함 확인
```

## Naming Rules

Use:

```text
<COURSE>_<GATE>_<PHASE>.ipynb
<COURSE>_<GATE>_<PHASE>_answer.ipynb
```

Default Phase codes:

```text
P0001 = Phase 0-0~0-1
P0002 = Phase 0-2
P0003 = Phase 0-3
P0004 = Phase 0-4
P0005 = Phase 0-5
```

Honor user-specified names over defaults.

## Inputs

Expected inputs:

```text
Course code:
Gate:
Phase:
Topic:
Learning goal:
Problem type:
Code hint level:
Answer included in problem notebook: yes/no
Web grounding allowed: yes/no
Reference materials:
Output directory:
```

Defaults:

```text
Course code = ML
Output language = Korean
Code hint level = hint_only
Answer included in problem notebook = no
Web grounding allowed = no unless current docs/facts are needed
Output count = 2 files max
```

## Problem Notebook Structure

Use this structure for `<COURSE>_<GATE>_<PHASE>.ipynb`:

```text
# <COURSE>_<GATE>_<PHASE>

## 0. 학습 범위
- Gate:
- Phase:
- Topic:
- Goal:
- Source basis:
- Output language: Korean
- Code mode: hint_only

## 1. 작성 규칙
- 문항별 답안 형식
- 코드 셀 사용 규칙
- 정답 미포함 안내

## 2. 채점 기준
- 핵심 구분 기준
- feature/target 또는 입력/출력 구분
- 문제 유형 판단
- 근거 설명
- 코드 구조 확인

## 3. 문제 세트
### 문항 N-1
문제 원문

### 코드 힌트
힌트 수준의 code cell

### 내 답안
빈 Markdown 답안 템플릿
```

Each item should normally have three cells:

```text
1. Markdown problem cell
2. Code hint cell
3. Markdown answer template cell
```

## Code Hint Policy

Default code mode is `hint_only`.

Allowed in the problem notebook:

```python
# 힌트:
# 필요한 라이브러리
# 확인할 객체
# shape 확인 방향
# DataFrame 생성 방향
# target column 후보
```

Forbidden in the problem notebook:

```python
# 완성된 정답 코드
# 전체 pipeline
# 모든 변수 정의가 완료된 solution cell
# 정답이 드러나는 출력
```

Only include full solution code in the answer notebook when the user requests `full_code`, `정답 코드 포함`, or `실행 가능한 정답 노트북 생성`.

## Answer Notebook Structure

Use this structure for `<COURSE>_<GATE>_<PHASE>_answer.ipynb`:

```text
# <COURSE>_<GATE>_<PHASE>_answer

## 0. 정답본 범위
- Gate:
- Phase:
- Topic:
- Problem notebook:
- Correct answers included: Yes
- Output language: Korean

## 1. 핵심 기준표
- 이 Phase에서 반드시 가져갈 판별 기준

## 2. 문항별 정답
### N-1
- 정답
- 근거
- 자주 하는 오답
- 최종 답안형

## 3. 채점 기준
- 문항별 scoring guide
- 부분점 기준
- 오답 판정 기준

## 4. 오답튜터 기준표
- 어떤 오류가 나오면 어떻게 설명할지
- 재시도 문제 생성 기준

## 5. 다음 Phase 연결
- 후속 개념
- 다음 노트북 추천
```

Clearly tell the user that the answer notebook exists because they may not want to open it before solving.

## Problem Design

Include more than memorization:

```text
1. 기본 식별 문제
2. 함정 문제
3. 애매한 판단 문제
4. 코드 구조 확인 문제
5. 실제 적용 시나리오 문제
6. 최종 요약 문제
```

## Web Grounding

Default to provided lecture materials, user plan, and prior local context. Use web only for current API/library syntax, official documentation, user-requested web grounding, or time-sensitive fact verification. If web is used, summarize sources in Korean in the answer notebook or final report.

## Validation

After generation, validate:

```bash
python3 -m json.tool <COURSE>_<GATE>_<PHASE>.ipynb > /dev/null
python3 -m json.tool <COURSE>_<GATE>_<PHASE>_answer.ipynb > /dev/null
```

If available, also use `nbformat.validate()`.

Check:

```text
1. Both ipynb files parse as JSON
2. Exactly two default files exist for the Phase
3. Problem notebook contains no answers
4. Answer notebook contains answers and grading criteria
5. Required headings exist
6. User-facing text is Korean
```

## Final Report

Report concisely in Korean:

```text
문제 노트북 생성 완료.

생성 파일:
- <COURSE>_<GATE>_<PHASE>.ipynb
- <COURSE>_<GATE>_<PHASE>_answer.ipynb

풀이용 노트북 포함:
- 문제 원문
- 코드 힌트
- 빈 답안 셀
- 채점 기준

정답본 포함:
- 문항별 정답
- 근거
- 자주 하는 오답
- 채점 기준
- 오답튜터 기준표

검증:
- ipynb JSON parse 통과
- 주요 heading 확인
- 풀이용 노트북 정답 미포함 확인
```

## Execution Prompt Template

```text
너는 IPYNB Problem Generation Skill을 수행하는 로컬 에이전트다.

입력:
- Course code:
- Gate:
- Phase:
- Phase code:
- Topic:
- Learning goal:
- Problem set source:
- Output directory:
- Code mode: hint_only
- Output language: Korean
- Web grounding allowed:

작업:
1. 출력 파일명을 결정한다.
2. 풀이용 노트북에는 문제 원문, 코드 힌트, 빈 답안 셀, 채점 기준만 넣는다.
3. 풀이용 노트북에는 정답을 넣지 않는다.
4. 정답본 노트북에는 문항별 정답, 근거, 자주 하는 오답, 채점 기준, 오답튜터 기준표를 넣는다.
5. 모든 Markdown 설명은 한국어로 작성한다.
6. code cell은 기본적으로 hint_only로 작성한다.
7. 두 ipynb 파일을 JSON parse로 검증한다.
8. 생성 파일 경로와 검증 결과를 한국어로 보고한다.
```
