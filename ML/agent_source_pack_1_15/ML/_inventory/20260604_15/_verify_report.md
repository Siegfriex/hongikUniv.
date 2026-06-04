# 20260604_15 검증 리포트 (2026-06-04 semantic QA)

## 1. manifest
- ok: source paths exist and lecture_id matches directory

## 2. anchor / segment / edge / evidence id 무결성
| 항목 | 총 | OK | 누락 | 비고 |
|------|----|----|------|------|
| anchors | 42 | 42 | 0 | heading grid |
| nodes | 23 | 23 | 0 | anchor/segment refs checked |
| edges | 22 | 22 | 0 | internal only |
| segments | 20 | 20 | 0 | local_seq checked; source transcript lines fully preserved |
| evidence | 40 | 40 | 0 | line ranges checked |

## 3. 의미 정렬 QA
- 초기 자동 정렬의 주요 오류: CNN transcript가 전처리/정규화 heading에 순차 배정됨.
- 조치: transcript L6-L165를 CNN 구성요소, channel/kernel, padding/stride/pooling, classifier, Fashion-MNIST, ImageNet, 오늘 정리 노드로 재매핑.
- 전처리/정규화/regularization 일부 섹션은 현재 transcript 직접 근거 없이 `lecture_md_anchor` evidence만 유지.

## 4. 정책 (Rule A / B′ / D)
- Rule A: L=20, G=[8,32], 판정 OK
- Rule B′: True
- Rule D: every node has lecture_md_anchor evidence; transcript evidence exists only for semantically aligned chunks.

## 5. 파생 md 고스트 id
- ghost/fail count: 0

## 6. 결론
- EXPORT OK
- SEMANTIC ALIGNMENT OK for 20260604_15 full transcript remap
