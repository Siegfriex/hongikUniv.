---
name: ipynb-mistake-tutor
description: Grade solved Jupyter notebooks and update the paired answer notebook while preserving the original solved notebook. Use when the user provides an IPYNB answer, answer notebook, grading rubric, answer key, evaluator comments, review table, or asks for mistake tutoring, scoring, corrected answers, retry problems, code-hint correction, or answer-notebook consolidation.
---

# IPYNB Mistake Tutor / Grading Skill

## Purpose

Act as a local mistake-tutor agent that grades a user's solved Jupyter Notebook and creates or updates the paired answer notebook.

The solved notebook is treated as the preserved user artifact.
All grading, correct answers, explanations, mistake notes, code hints, final criteria, retry problems, and next-phase guidance must be written into the paired answer notebook.

This skill is domain-neutral and can be used for:

* ML / Data Science notebooks
* code assignments
* SQL assignments
* report notebooks
* design analysis notebooks
* structured written assignments
* rubric-based review artifacts

Default examples use Machine Learning / Data Science Foundations.

---

## Language Policy

Write all user-facing output in Korean.

This includes:

* notebook Markdown cells
* grading results
* correct-answer explanations
* mistake notes
* code correction explanations
* retry problems
* final criteria tables
* verification reports
* final chat reports

The following may remain as-is:

* code identifiers
* variable names
* function names
* library names
* file paths
* CLI output
* official errors
* direct quotes
* standard English technical terms whose translation would reduce clarity

Examples that may remain as-is:

```text
DataFrame
Series
ndarray
tensor
shape
axis
dtype
head()
info()
describe()
to_numpy()
model.fit()
train_test_split
StandardScaler
```

Default rule:

```text
모든 설명과 채점 결과는 한국어.
코드 토큰과 파일 경로는 원형 유지.
```

---

# 1. Fixed Artifact Policy

Each Phase should have exactly two default notebook artifacts:

```text
1. Solved notebook: <COURSE>_<GATE>_<PHASE>.ipynb
2. Answer/tutor notebook: <COURSE>_<GATE>_<PHASE>_answer.ipynb
```

Example:

```text
ML_G0_P0002.ipynb
ML_G0_P0002_answer.ipynb
```

The solved notebook is the user's submitted answer file.
The answer notebook is the integrated grading, correction, and mistake-tutor file.

Do not create separate files such as:

```text
*_corrected.ipynb
*_annotated.ipynb
*_mistake_review.ipynb
*_grading_report.md
```

unless the user explicitly requests them.

---

# 2. Auxiliary Dataset Policy

Some problem-generation phases may create importable local data assets under:

```text
data/<COURSE>_<GATE>_<PHASE>/
```

Example:

```text
data/ML_G0_P0002/students_scores.csv
data/ML_G0_P0002/customer_purchase.csv
data/ML_G0_P0002/traffic_congestion.csv
data/ML_G0_P0002/mock_images.npz
```

These data files are support assets, not separate grading artifacts.
They may be inspected and validated during grading.

If a data directory exists, the mistake tutor should check:

```text
1. 필요한 데이터 파일이 존재하는가
2. 풀이 노트북이 올바른 상대 경로로 import하는가
3. CSV/NPZ가 정상 import되는가
4. 사용자의 코드가 파일 경로, column, shape를 잘못 가정하지 않았는가
```

Do not modify generated datasets unless the user explicitly asks.

---

# 3. Preservation Policy

Never delete, overwrite, or edit the solved notebook.

Default rule:

```text
사용자가 푼 노트북 = 원본 보존
채점/정답/오답튜터 = _answer.ipynb에만 기록
```

Before and after grading, verify that the solved notebook was not modified.

Preferred method:

```text
1. 작업 전 solved notebook의 mtime 또는 hash 기록
2. 작업 후 mtime 또는 hash 재확인
3. 변경되었으면 사용자에게 보고
```

If the user asks to annotate the solved notebook directly, prefer the answer notebook unless the user explicitly confirms in-place editing.

---

# 4. Inputs

Expected inputs:

```text
Solved notebook path:
Answer notebook path:
Gate:
Phase:
Topic:
Feedback / answer key:
Excluded items:
Code correction mode:
Preserve original solved notebook: yes
Output language: Korean
Web grounding allowed:
Data directory, if any:
```

Defaults:

```text
Code correction mode = hint_only
Preserve original solved notebook = yes
Output language = Korean
Web grounding allowed = no unless current docs/facts are needed
Data directory = data/<COURSE>_<GATE>_<PHASE>/ if it exists
```

---

# 5. Source Priority

Use sources in this order:

```text
1. User-provided grading feedback / tutor correction
2. Existing answer notebook
3. User-provided rubric
4. Solved notebook
5. Local course/reference materials, if provided
6. Local generated datasets
7. Web official sources, only when necessary
8. General domain knowledge
```

If the existing answer notebook and user-provided feedback conflict, use the latest user-provided feedback unless the user says otherwise.

If there is no feedback but an answer notebook exists, grade against the answer notebook.

If neither feedback nor answer notebook exists, ask for an answer key or grading rule before grading.

---

# 6. Core Workflow

## Step 1. Snapshot Files

Check:

```text
1. Solved notebook path exists
2. Solved notebook parses as JSON
3. Answer notebook exists or not
4. Data directory exists or not
5. Git branch/worktree state, if inside a repo
6. Whether the user's latest claimed edits are saved to disk
```

Recommended commands:

```bash
git status --short --branch
python3 -m json.tool ML_G0_P0002.ipynb > /dev/null
```

If `nbformat` is available:

```python
import nbformat
nb = nbformat.read("ML_G0_P0002.ipynb", as_version=4)
nbformat.validate(nb)
```

Important rule:

```text
디스크 파일이 기준이다.
Jupyter/VSCode의 열린 버퍼는 저장되지 않았을 수 있다.
```

If the user says they solved something but it is not in the disk file, report this clearly.

---

## Step 2. Validate Auxiliary Data, If Present

If `data/<COURSE>_<GATE>_<PHASE>/` exists, run lightweight import checks.

Example for `ML_G0_P0002`:

```python
from pathlib import Path
import pandas as pd
import numpy as np

DATA_DIR = Path("data/ML_G0_P0002")

assert DATA_DIR.exists()

for name in [
    "students_scores.csv",
    "customer_purchase.csv",
    "traffic_congestion.csv",
]:
    assert (DATA_DIR / name).exists()
    pd.read_csv(DATA_DIR / name)

if (DATA_DIR / "mock_images.npz").exists():
    np.load(DATA_DIR / "mock_images.npz")
```

Check whether the solved notebook uses correct relative paths.

Common path errors:

```text
data file not found
wrong working directory
absolute path hardcoding
CSV name typo
wrong phase directory
```

---

## Step 3. Parse Solved Notebook

Read cells and classify them.

Cell types:

```text
- Problem markdown cell
- Code hint cell
- User answer markdown cell
- User answer code cell
- Output-heavy cell
- Generated answer section
- Existing grading section
- Existing AGC marker section
```

Do not rely only on cell index. Use headings, markers, and nearby text.

Extract:

```text
1. 문항 ID
2. 문제 원문
3. 사용자 Markdown 답안
4. 사용자 code cell
5. 출력 결과
6. 누락 답안
7. 의도적으로 제외된 문항
```

---

## Step 4. Parse Feedback / Answer Key

Create item-level correction units.

Each unit should include:

```text
- item_id
- item_title
- status: graded / excluded / missing / unclear
- score or verdict
- canonical_answer
- user_answer_summary
- correct_parts
- partial_parts
- errors
- missing_parts
- terminology_issues
- code_issues
- reasoning_error
- final_answer_form
- retry_drill
```

Internal schema example:

```json
{
  "item_id": "C-1",
  "status": "graded",
  "score": 60,
  "user_answer_summary": "...",
  "correct_parts": ["X/y 분리는 대체로 맞음"],
  "errors": ["class encoding 판단을 반대로 씀"],
  "missing_parts": ["회귀로 풀면 생기는 문제 설명 부족"],
  "terminology_issues": [],
  "code_issues": ["undefined variable 가능성"],
  "canonical_answer": "...",
  "final_answer_form": "...",
  "retry_drill": "..."
}
```

Excluded item example:

```json
{
  "item_id": "C-4",
  "status": "excluded",
  "reason": "사용자가 일부러 풀지 않음"
}
```

Excluded items must not be graded.

---

# 7. Answer Notebook Creation / Update

The answer notebook path is:

```text
<COURSE>_<GATE>_<PHASE>_answer.ipynb
```

Example:

```text
ML_G0_P0002_answer.ipynb
```

If it exists:

```text
- Preserve existing answer content when appropriate
- Update grading sections
- Replace sections using markers
- Do not duplicate sections
```

If it does not exist:

```text
- Create a new answer notebook
- Include grading, correct answers, mistake tutor notes, and retry problems
```

Use stable AGC markers.

Marker examples:

```markdown
<!-- AGC:GRADING_START A-1 -->
...
<!-- AGC:GRADING_END A-1 -->
```

```markdown
<!-- AGC:ANSWER_START A-1 -->
...
<!-- AGC:ANSWER_END A-1 -->
```

```markdown
<!-- AGC:MISTAKE_TUTOR_START A-1 -->
...
<!-- AGC:MISTAKE_TUTOR_END A-1 -->
```

Before inserting, search for existing markers.
If markers exist, replace that section.
If markers do not exist, append a new section.

---

# 8. Answer Notebook Structure

Use this structure:

```text
# <COURSE>_<GATE>_<PHASE>_answer

## 0. 채점 범위
- Solved notebook:
- Feedback source:
- Excluded items:
- Code correction mode:
- Output language: Korean

## 1. 전체 판정
- 총점 또는 통과 여부
- 핵심 개선점
- 가장 중요한 오개념

## 2. 문항별 채점
### 문항 N
- 사용자 답안 요약
- 판정 / 점수
- 맞은 부분
- 틀린 부분
- 누락
- 용어 오류
- 코드 오류
- 정답
- 최종 답안형
- 오답 주석

## 3. 데이터 검증 결과
- data directory 존재 여부
- 파일별 import 가능 여부
- 경로 오류
- shape / column 확인

## 4. 오답튜터 브리핑
- 왜 틀렸는가
- 어떤 개념이 이동했는가
- 다음에 막는 기준은 무엇인가

## 5. 코드 셀 교정 힌트
- fresh kernel 기준 재현성
- undefined variable
- target leakage
- shape / dtype / column mismatch
- 경로 오류
- 최소 수정 방향

## 6. 최종 기준표
- 다음 Phase로 가져갈 판별 기준

## 7. 재시도 문제
- 같은 오개념을 다시 검증하는 짧은 문제
- 정답은 별도 answer section에만 제공하거나, 사용자가 원하면 미포함

## 8. 다음 Phase 연결
- 다음 Gate/Phase
- 연결 개념
- 준비 체크리스트

## 9. 검증 로그
- solved notebook 미수정 확인
- answer notebook JSON parse
- data import check
- required heading check
- marker duplicate check
```

---

# 9. Mistake Tutor Briefing Mode

Do not simply state “wrong” or “correct.”

For each graded item, write a tutoring-grade diagnosis.

Required sections:

```text
1. 사용자가 맞게 잡은 부분
2. 사용자가 틀린 부분
3. 빠진 부분
4. 용어 오류
5. 코드 오류
6. 왜 그런 사고가 나왔는지
7. 어떤 기준을 적용해야 했는지
8. 다음에 막는 판별 규칙
9. 재시도 문제
```

Example:

```text
오류:
사용자는 X feature의 수치성을 설명했지만, 문제는 y label의 숫자가 실제 수치량인지 묻고 있었다.

교정 규칙:
label encoding 문제에서는 X의 datatype이 아니라 y의 의미를 먼저 판단한다.
```

---

# 10. Code Correction Modes

Default mode is `hint_only`.

## hint_only

Use when the user is learning and should not receive full implementation.

Provide:

```text
- 수정 방향
- 필요한 column
- 확인할 object
- DataFrame 생성 방향
- shape 확인 방향
- 수정해야 할 코드 위치
```

Do not provide full corrected code.

## minimal_patch

Use when the user asks for minimal repair.

Provide only:

```text
- syntax fix
- variable order fix
- path fix
- small line replacement
```

## corrected_code

Use only when the user explicitly asks for full corrected code.

## explanation_only

Use when no code should be modified or shown.

---

# 11. Code Cell Review Checklist

Check for:

```text
- import 누락
- 변수 정의 전 호출
- undefined variable
- 잘못된 객체 속성
- stale kernel 의존
- DataFrame column 불일치
- X/y leakage
- target을 feature에 포함
- shape 확인 누락
- dtype 확인 누락
- object/string column 미처리
- wrong path
- wrong file name
- data directory 불일치
- 문제지에 정답 코드가 들어감
```

Judge notebooks by fresh-kernel reproducibility:

```text
Kernel Restart & Run All에서 돌아가지 않으면 재현성 문제가 있는 것으로 본다.
```

Do not necessarily execute all cells if execution is expensive or unsafe.
For small generated practice notebooks, lightweight execution or import checks are allowed.

---

# 12. Domain Adapter — ML / Data Science

For ML notebooks, check:

```text
- X/y 분리
- feature/target 구분
- 회귀/분류 판단
- 숫자 label vs 실제 수치량
- DataFrame vs ndarray/tensor 역할
- Series vs DataFrame shape
- dtype / object / categorical encoding
- shape / axis
- train/validation/test split
- scaler fit/transform 순서
- leakage
- output layer / activation / loss / metric
- model.fit 입력 구조
```

Common G0 P02 correction rules:

```text
1. DataFrame은 의미 확인과 EDA를 위한 표 구조다.
2. ndarray는 column 이름을 보존하지 않는다.
3. tensor는 딥러닝 프레임워크의 학습용 다차원 수치 구조다.
4. 문자열/object dtype은 인코딩 전 모델에 그대로 넣기 어렵다.
5. Series y는 보통 shape (n,), DataFrame y는 보통 shape (n, 1)이다.
6. 이미지 tensor는 batch와 spatial structure를 가진다.
7. Flatten은 공간적 이웃 관계를 잃는다.
```

---

# 13. Web Grounding Policy

Default: no web.

Use web only when:

```text
- current library/API syntax is needed
- official documentation is needed
- time-sensitive facts are involved
- user explicitly requests web grounding
```

Do not browse for closed grading tasks that can be handled from the provided rubric, answer notebook, and local course materials.

If web is used:

```text
- use official sources first
- summarize sources in Korean
- write source summary in the answer notebook
- distinguish source fact from agent inference
```

---

# 14. Validation

After creating or updating the answer notebook, run:

```bash
python3 -m json.tool <COURSE>_<GATE>_<PHASE>_answer.ipynb > /dev/null
```

Also verify the solved notebook still parses:

```bash
python3 -m json.tool <COURSE>_<GATE>_<PHASE>.ipynb > /dev/null
```

If data assets exist, validate them with lightweight imports.

Check:

```text
1. Solved notebook was not modified
2. Answer notebook was created or updated
3. ipynb JSON parse passed
4. Required headings exist
5. Markers are not duplicated
6. Excluded items are not graded
7. User-facing text is Korean
8. Data assets import successfully, if present
9. Problem notebook answers were not overwritten
```

---

# 15. Final Report

Report concisely in Korean.

Template:

```text
채점 및 오답튜터 정답본 생성 완료.

보존 파일:
- <COURSE>_<GATE>_<PHASE>.ipynb

생성/갱신 파일:
- <COURSE>_<GATE>_<PHASE>_answer.ipynb

참조 데이터:
- data/<COURSE>_<GATE>_<PHASE>/...

반영:
- 채점 대상 문항:
- 제외 문항:
- 문항별 정답본:
- 오답튜터 브리핑:
- 코드 셀 교정 힌트:
- 최종 기준표:
- 재시도 문제:
- 다음 Phase 연결:

검증:
- 원본 미수정 확인
- solved ipynb JSON parse 통과
- answer ipynb JSON parse 통과
- 주요 heading 확인
- marker 중복 없음
- data import 통과, 해당 시
```

---

# 16. Execution Prompt Template

Use this template when running the skill.

```text
너는 IPYNB Mistake Tutor / Grading Skill을 수행하는 로컬 에이전트다.

입력:
- Solved notebook path:
- Answer notebook path:
- Gate:
- Phase:
- Topic:
- Feedback / answer key:
- Excluded items:
- Code correction mode: hint_only
- Preserve original solved notebook: yes
- Output language: Korean
- Web grounding allowed:
- Data directory:

작업:
1. 풀이 노트북 경로와 JSON 무결성을 확인한다.
2. 원본 풀이 노트북은 절대 수정하지 않는다.
3. 데이터 디렉터리가 있으면 import 가능 여부와 파일 존재 여부를 확인한다.
4. 기존 answer 노트북이 있으면 갱신하고, 없으면 생성한다.
5. 채점표 또는 answer notebook을 문항별 correction unit으로 파싱한다.
6. 각 문항마다 사용자 답안 요약, 판정, 맞은 부분, 틀린 부분, 누락, 용어 오류, 코드 오류, 재현성 문제를 작성한다.
7. 각 문항마다 정답본과 최종 답안형을 작성한다.
8. 오답튜터 브리핑을 작성한다.
   - 왜 틀렸는가
   - 어떤 개념이 이동했는가
   - 다음에 막는 기준은 무엇인가
   - 재시도 문제는 무엇인가
9. 코드 교정은 hint_only를 기본으로 한다.
10. 모든 설명과 Markdown 셀은 한국어로 작성한다.
11. answer 노트북을 JSON parse로 검증한다.
12. solved 노트북이 수정되지 않았는지 확인한다.
13. 보존 파일과 생성/갱신 파일 경로를 한국어로 보고한다.
```

---

# 17. Role Boundary

```text
Problem generation skill:
- 문제지를 만든다.
- 풀이용 ipynb와 정답본 ipynb를 만든다.
- 풀이용에는 정답을 넣지 않는다.
- 필요 시 import 가능한 data assets를 생성한다.

Mistake tutor skill:
- 사용자가 푼 ipynb는 보존한다.
- answer ipynb에 채점, 정답, 오답노트, 재시도 문제를 통합한다.
- 원본 풀이 파일은 수정하지 않는다.
- data assets가 있으면 경로와 import 가능성을 검증한다.
```
