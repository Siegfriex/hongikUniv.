# Local Agent Grading Cycle Framework

이 문서는 이번 `gate1.ipynb` 작업에서 수행한 협업 사이클을 범용 스킬로 만들기 위한 구조화 초안이다. ML 노트북에 한정하지 않고, 사용자가 작성한 산출물과 외부 채점표/리뷰를 받아 로컬 에이전트가 정답본, 보완본, 주석본을 생성하는 절차를 일반화한다.

## 역할 정의

사용자:

- 원본 산출물을 작성한다.
- 채점 에이전트, 튜터, 리뷰어, 평가표 등 외부 피드백을 제공한다.
- 원본 보존, 새 파일 생성, 기존 파일 통합 같은 산출 방식 요구를 지정한다.

로컬 에이전트:

- 실제 로컬 파일을 읽어 현재 디스크 상태를 확인한다.
- 사용자의 원답을 보존한다.
- 채점표를 해석해 정답, 부분정답, 오답, 누락, 용어 오류, 근거 오류를 분리한다.
- 수정본을 로컬 파일로 생성하거나 통합한다.
- 마지막에 생성 경로와 검증 결과를 보고한다.

## 이번 작업의 실제 입력

사용자가 제공한 입력은 세 종류였다.

1. 원본 노트북 경로
   - `ML/workshop/gate1.ipynb`
   - 사용자가 직접 문제를 풀어 둔 Jupyter notebook

2. 외부 채점표
   - C-1, C-2, C-3, C-5에 대한 점수와 교정
   - 이후 보완 1, 2, 3, 6에 대한 추가 채점표

3. 산출 방식 지시
   - 처음에는 기존 답안 옆에 색상/주석을 추가하길 원함
   - 이후 원본에 직접 주석을 붙이는 방식이 혼란스러워 새 정답본 노트북 생성을 요청함
   - 마지막에는 기존 정답본 `gate1_corrected.ipynb` 하나에 통합하길 요청함

## 이번 작업에서 로컬 에이전트가 한 일

1. 파일 상태 확인
   - `git status --short --branch`로 브랜치와 untracked 상태 확인
   - `python3 -m json.tool`로 `.ipynb` JSON 무결성 확인
   - 노트북 셀 목록을 읽어 답안 셀 위치 파악

2. 첫 번째 시도
   - 원본 `gate1.ipynb`의 답안 셀 뒤에 채점 주석 Markdown 셀 추가
   - 사용자가 “달라진 게 없다”고 피드백
   - 원인: Jupyter/VSCode의 열린 버퍼 reload 문제 또는 별도 셀 방식이 사용자의 기대와 불일치

3. 두 번째 시도
   - 기존 답안 셀 하단에 직접 채점 주석을 붙임
   - 그러나 사용자가 최종적으로 “새 ipynb 생성”을 선호한다고 변경 지시

4. 정답본 생성
   - `gate1_corrected.ipynb` 생성
   - 본문은 정답으로 작성
   - 이전 답안의 오류는 `이전 오답 주석`으로 분리
   - C-4는 채점 제외이므로 제외

5. 보완문제 정답본 생성
   - 사용자가 새 보완 답안을 썼다고 했지만 디스크의 `gate1.ipynb`에는 저장된 보완문제가 없었음
   - 이 사실을 확인하고 보고
   - 그래도 사용자가 제공한 채점표만으로 `gate1_supplement_corrected.ipynb` 생성

6. 통합
   - `gate1_supplement_corrected.ipynb`의 보완 1, 2, 3, 6과 최종 기준표를 `gate1_corrected.ipynb` 뒤에 통합
   - 통합 구간에 marker comment를 넣어 재실행 시 중복 삽입을 방지

7. 검증
   - 생성/수정된 `.ipynb`를 JSON parser로 확인
   - 주요 제목과 `이전 오답 주석` 존재 여부 검색
   - 최종 파일 경로를 사용자에게 보고

## 범용 워크플로우

### 1. Source Snapshot

항상 현재 로컬 파일을 먼저 확인한다.

- 대상 파일 존재 여부
- 파일 형식 무결성
- 최근 수정 상태
- git branch/worktree 상태
- 사용자가 말한 내용이 실제 디스크에 저장되어 있는지

중요 원칙:

- 사용자가 “방금 썼다”고 해도 저장되지 않았을 수 있다.
- 노트북/문서 편집기는 열린 버퍼와 디스크 파일이 다를 수 있다.
- 로컬 에이전트는 디스크 기준으로만 확정 판단한다.

### 2. Feedback Parsing

외부 채점표에서 다음 정보를 추출한다.

- 평가 대상 문항
- 제외 대상 문항
- 점수/판정
- 핵심 오류
- 정답 문장
- 부분정답으로 인정할 수 있는 표현
- 오답 또는 위험한 표현
- 최종 기준표나 반복 적용할 rule

채점표가 길어도 문항별로 같은 구조로 정리한다.

### 3. Preservation Policy

원답 보존 방식을 명확히 정한다.

- 원본 파일 보존
- 새 정답본 파일 생성
- 기존 파일에 별도 주석 셀 추가
- 기존 답안 셀 내부 하단에 주석 추가
- 하나의 통합본 파일로 병합

혼동을 줄이려면 기본값은 새 파일 생성이다.

권장 파일명:

- `<original>_corrected.ipynb`
- `<original>_reviewed.ipynb`
- `<original>_annotated.ipynb`
- `<original>_supplement_corrected.ipynb`

### 4. Correction Artifact

정답본의 기본 구조:

```text
문항 제목
정답
근거
이전 오답 주석
최종 답안형
```

`이전 오답 주석`에는 다음을 쓴다.

- 사용자가 맞게 잡은 부분
- 오답인 부분
- 누락한 부분
- 용어가 부정확한 부분
- 해석 근거가 잘못 이동한 부분
- 다음에 같은 실수를 막는 기준

### 5. Validation

파일 생성 후 반드시 검증한다.

- `.ipynb`: JSON parse
- Markdown: 경로 존재와 주요 heading 검색
- 코드 파일: lint/test/build 등 요청 범위에 맞는 gate
- 노트북: 필요하면 셀 제목/개수/핵심 키워드 검사

검증 결과는 최종 응답에 짧게 보고한다.

## Skill 초안

아래는 실제 Codex skill로 옮길 때의 `SKILL.md` 초안이다.

```markdown
---
name: artifact-grading-cycle
description: Use when the user provides a local artifact plus a rubric, grading table, review feedback, or evaluator comments and wants the agent to preserve the original while creating corrected, annotated, or consolidated local artifacts. Applies to notebooks, markdown docs, reports, code answers, essays, and structured assignments.
---

# Artifact Grading Cycle

## Goal

Turn a user-authored local artifact plus external feedback into a verified corrected or annotated artifact while preserving the original.

## Workflow

1. Snapshot the target
   - Confirm path, file type, parseability, branch/worktree state, and whether the user's latest edits are saved to disk.
   - If the user claims content exists but it is not on disk, say so and either ask for the saved file or proceed from the pasted rubric if sufficient.

2. Parse feedback
   - Extract evaluated items, excluded items, scores, core mistakes, correct answer forms, and reusable rules.
   - Keep item boundaries stable.

3. Choose output mode
   - Prefer a new corrected artifact unless the user explicitly asks to edit in place.
   - Preserve the user's original answer as evidence, not as the final answer.
   - Put corrections in a clearly named file such as `_corrected`, `_annotated`, or `_reviewed`.

4. Write corrections
   - For each item: write the corrected answer first.
   - Add `Previous Answer Notes` or equivalent to identify prior errors, omissions, terminology issues, and weak reasoning.
   - Keep reviewer/rubric logic traceable.

5. Verify
   - Parse generated files.
   - Search for required headings and notes.
   - Report exact output paths and verification performed.

## Default Output Structure

```text
Title
Scope and source note
Item N
Correct answer
Reasoning
Previous answer notes
Final answer form
Summary table
```

## Guardrails

- Do not overwrite the user's original unless explicitly requested.
- Do not assume notebook/editor buffers are saved; verify disk content.
- Do not silently merge new feedback into stale files without checking for duplicates.
- If rerunning a merge, use markers or search keys to avoid duplicate sections.
- Keep domain-specific reasoning in the artifact, but keep the workflow domain-neutral.
```

## 이 프레임워크의 핵심 일반화

이번 작업은 ML 분류/회귀 문제가 본질이 아니라, 다음 패턴이 본질이다.

```text
사용자 원본 산출물
+ 외부 평가/채점표
+ 로컬 파일 시스템 접근
= 원본 보존형 정답/보완 산출물 생성
```

따라서 같은 구조는 다음에도 적용된다.

- 코딩 테스트 풀이 + 리뷰어 채점표
- 논문 요약문 + 교수 피드백
- 보고서 초안 + 평가 루브릭
- SQL 과제 + 채점 로그
- 설계 문서 + 시니어 리뷰
- 프론트엔드 QA 결과 + 수정 가이드
- 법/정책 리서치 답안 + 검토 의견

## 운영상 중요한 교훈

- “보이는 화면”과 “디스크에 저장된 파일”은 다를 수 있다.
- 주석을 기존 셀 옆에 넣는 방식은 사용자가 못 볼 수 있다.
- 학습/복습 목적이면 새 정답본이 가장 덜 혼란스럽다.
- 원답을 고치지 말고, 원답 오류를 별도 주석으로 기록해야 학습 효과가 남는다.
- 통합본을 만들 때는 중복 삽입 방지 marker가 필요하다.
