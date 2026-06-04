# 20260507_10 검증 리포트 (2026-06-04 16:15)

## 1. manifest
- ok: source paths exist and lecture_id matches directory

## 2. anchor / segment / edge / evidence id 무결성
| 항목 | 총 | OK | 누락 | 비고 |
|------|----|----|------|------|
| anchors | 103 | 103 | 0 | heading grid |
| nodes | 8 | 8 | 0 | anchor/segment refs checked |
| edges | 7 | 7 | 0 | internal only |
| segments | 9 | 9 | 0 | local_seq checked by construction |
| evidence | 16 | 16 | 0 | line ranges checked |

## 3. 정책 (Rule A / B′ / D)
- Rule A: L=9, G=[8,32], 판정 OK
- Rule B′: True
- Rule D: every node has lecture_md_anchor evidence; transcript evidence exists for aligned chunks.

## 4. 파생 md 고스트 id
- ghost/fail count: 0

## 5. 결론
- EXPORT OK
