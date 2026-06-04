# ML 8-15강 최종 검증·디벨롭 리포트

## 1. 결론

`ML/final_brief`와 `ML/final_record`에서 생성한 8-15강 인벤토리/RAG/DOCX 산출물에 대해 원문 보존, sidecar id 정합, 전사 줄 보존, evidence line range, annotated transcript, DOCX 구조 검증을 완료했다.

최종 판정은 다음과 같다.

| lecture_id | 최종 판정 | 비고 |
|------------|-----------|------|
| `20260430_8` | PASS | 중복 node id 수정 후 통과 |
| `20260507_10` | PASS | 통과 |
| `20260514_11` | PASS | 통과 |
| `20260521_12` | PASS | 통과 |
| `20260528_13` | PASS | 중복 node id 수정 후 통과 |
| `20260529_14` | PASS | 보조 전사 conflict 기록 유지 |
| `20260604_15` | PASS | 초기 heading 순서 정렬 오류 발견 후 CNN/종강 구간으로 transcript evidence 수동 재매핑 |

## 2. 발견한 문제와 수정

### 2.1 중복 node_id

초기 배치 산출물에서 다음 중복 `node_id`를 발견했다.

| lecture_id | 중복 id | 원인 | 조치 |
|------------|---------|------|------|
| `20260430_8` | `n_ML8.neural_network`, `n_ML8.perceptron` | 서로 다른 heading이 같은 영문 slug로 정규화됨 | 중복 시 anchor index suffix를 붙이도록 생성 규칙 수정 |
| `20260528_13` | `n_ML13.dnn` | 서로 다른 DNN heading이 같은 slug로 정규화됨 | 동일 조치 |

수정 후 모든 강의에서 `node_id`, `anchor_id`, `segment_id`, `evidence_id` 중복은 0건이다.

### 2.2 marker block 재수집 방지

`20260430_8강.md`에 이전 생성 marker block이 남아 있을 경우, 그 block의 heading이 다시 anchor/node로 수집되는 문제가 있었다.

조치:
- 재생성 전 `<!-- INVENTORY_MARKERS:<lecture_id> -->` 이후 block을 제거하고 다시 insert-only marker index를 붙이도록 처리
- anchor parser가 marker block을 만나면 heading 수집을 중단하도록 처리

수정 후 marker index는 강의 본문 node로 재수집되지 않는다.

## 3. 최종 검증 항목

| 검증 항목 | 기준 | 결과 |
|-----------|------|------|
| 원문 md 보존 | `final_brief` 본문과 SSOT md의 marker 이전 본문 동일 | PASS |
| 전사 보존 | `final_record`와 SSOT transcript 동일 | PASS |
| raw mirror 보존 | raw mirror가 원본 복사본으로 존재 | PASS |
| id 중복 | node/anchor/segment/evidence id 중복 0 | PASS |
| node 참조 | `nodes.anchor_ids`, `nodes.segment_ids`가 sidecar 실존 id | PASS |
| edge 참조 | `edges.from`, `edges.to`가 nodes 실존 id | PASS |
| segment text | `segments.text_raw`가 전사 줄 범위와 동일 | PASS |
| evidence ref | `evidence.ref.file`, `ref.lines`, `segment_id` 정합 | PASS |
| annotated transcript | marker line 제거 시 원본 전사와 동일 | PASS |
| derived md ghost | RAG/로데이터 md의 id가 sidecar 실존 id | PASS |
| DOCX 구조 | 각 강의별 DOCX 2개, zip 구조 및 `word/document.xml` 존재 | PASS |
| whitespace | `git diff --check` 통과 | PASS |

## 4. 최종 수량

| lecture_id | nodes | segments | evidence | DOCX |
|------------|------:|---------:|---------:|-----:|
| `20260430_8` | 24 | 23 | 45 | 2 |
| `20260507_10` | 8 | 9 | 16 | 2 |
| `20260514_11` | 17 | 18 | 34 | 2 |
| `20260521_12` | 11 | 12 | 22 | 2 |
| `20260528_13` | 11 | 12 | 20 | 2 |
| `20260529_14` | 16 | 16 | 31 | 2 |
| `20260604_15` | 23 | 20 | 40 | 2 |

DOCX 총계: 14개.

## 5. 산출물 위치

| 산출물 | 위치 |
|--------|------|
| 강별 sidecar | `ML/_inventory/<lecture_id>/` |
| RAG md | `ML/_inventory/<lecture_id>/{YYYYMMDD}_{N}강_래그.md` |
| 로데이터 디벨롭 md | `ML/_inventory/<lecture_id>/{YYYYMMDD}_{N}강_로데이터디벨롭.md` |
| annotated transcript | `ML/_inventory/<lecture_id>/{YYYYMMDD}_{N}강_annotated_transcript.txt` |
| 검증 리포트 | `ML/_inventory/<lecture_id>/_verify_report.md` |
| DOCX | `docx-export/ML/_inventory-derived/<lecture_id>/` |
| 전체 검증 플랜 | `ML/_inventory/verification_plan_8_15.md` |

## 6. 남은 주의사항

| 항목 | 상태 | 설명 |
|------|------|------|
| `0522ml.txt` | skipped | matching `final_brief`가 없어 배치 대상에서 제외 |
| `0529이용오교수님.txt` | conflict/secondary | `20260529_14`의 primary transcript는 `0529_ml.txt`; 보조 전사는 conflict로 기록 |
| 의미 경계 QA | 권장 | 현재 segment는 자동 분할 기반이다. 배포 전 강별 핵심 segment의 시작/끝 의미 경계 수동 QA를 권장 |

## 7. 최종 판정

현재 산출물은 id·원문보존·문서생성 기준으로 배포 가능한 상태다. `20260604_15`는 추가 의미 QA에서 자동 순차 정렬 오류를 발견해 transcript evidence를 CNN/종강 구간으로 재매핑했다.

판정: `FINAL PASS`
