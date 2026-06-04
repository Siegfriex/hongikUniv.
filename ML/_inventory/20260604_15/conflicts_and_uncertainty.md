# 20260604_15 conflicts / 불확실성

## 1. 전사 vs md 충돌

- 초기 자동 정렬은 heading 순서 기반이어서 CNN 녹취가 전처리/정규화 heading에 붙는 오류가 있었다.
- 2026-06-04 수동 의미 QA로 transcript evidence를 CNN/모델계보/종강정리 구간에 재매핑했다.
- 전처리, scaling, encoding, train/validation/test, regularization 앞부분은 PDF/노트북 기반 md-primary 섹션이며 현재 transcript evidence를 붙이지 않는다.

## 2. 노드 / 엣지 보류 (uncertain)

- cross-lecture edge는 상대 강 nodes.json 실존 여부가 배치 완료 전 불안정하므로 내부 leads_to만 생성했다.

## 3. 정책 위반 / 예외 (Rule A / B′ / D)

- Rule A: L=21, G=[8,32], pass=True
- Rule B′: F_has_prelecture=True
- Rule D: md-primary evidence 생성 완료; transcript evidence는 의미 일치 구간에만 연결.

## 4. 파일명 / 인코딩 패턴 (P-시리즈)

- Framework path exception: task text says `REPO_ROOT/_framework`, actual path is `ML/_framework`.
- `0522ml.txt`: brief 없음, batch에서 skip.
