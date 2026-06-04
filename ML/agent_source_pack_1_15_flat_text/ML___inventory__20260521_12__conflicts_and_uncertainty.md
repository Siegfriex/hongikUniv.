# 20260521_12 conflicts / 불확실성

## 1. 전사 vs md 충돌

- 자동 정렬 결과는 heading 순서 기반 1차 정렬이다. 세밀한 시간 단위 조정은 후속 수동 QA 대상.

## 2. 노드 / 엣지 보류 (uncertain)

- cross-lecture edge는 상대 강 nodes.json 실존 여부가 배치 완료 전 불안정하므로 내부 leads_to만 생성했다.

## 3. 정책 위반 / 예외 (Rule A / B′ / D)

- Rule A: L=12, G=[8,32], pass=True
- Rule B′: F_has_prelecture=True
- Rule D: md-primary evidence 생성 완료

## 4. 파일명 / 인코딩 패턴 (P-시리즈)

- Framework path exception: task text says `REPO_ROOT/_framework`, actual path is `ML/_framework`.
- `0522ml.txt`: brief 없음, batch에서 skip.


## 5. 외부 자료 의존 (`grounded_by`) 항목

- 없음.
