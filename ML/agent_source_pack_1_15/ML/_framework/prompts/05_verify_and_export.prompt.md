# 05 — 검증 + DOCX 내보내기 프롬프트

**입력:** 단계 01–04 산출물 일체
**출력:** (a) 검증 리포트 (콘솔 또는 `_inventory/<id>/_verify_report.md`), (b) `docx-export/<course>/_inventory-derived/<id>/*.docx`, (c) `README_inventory.md` 갱신

---

## 시스템/역할

너는 한 강의 인벤토리·파생 md를 **id 정합·고스트 id·정책 위반** 기준으로 검증하고, 통과 후 DOCX로 내보내는 에이전트다. 새 sidecar 데이터는 만들지 않는다.

---

## 검증 항목 (모두 통과해야 EXPORT)

1. **manifest 무결성**
   - `manifest.sources[].path` 가 실제 파일로 존재.
   - `lecture_id` 가 디렉터리명과 일치.
2. **anchor 무결성**
   - `nodes[].anchor_ids` ⊆ `anchors_md.anchors[].anchor_id`
   - `alignments[].anchor_id` ⊆ 동일 집합
3. **segment 무결성**
   - `nodes[].segment_ids` ⊆ `segments[].segment_id`
   - `alignments[].segment_id` ⊆ 동일 집합
   - `segments[].local_seq` 가 같은 `section_id` 안에서 1..N 단조 증가
4. **edge 무결성**
   - `edges[].from`, `edges[].to` 의 강 접두사가 가리키는 강의 `nodes.json` 에 실재.
   - `prerequisite` 의 방향이 선행→후속.
5. **evidence 무결성**
   - `evidence[].node_id` ⊆ `nodes[].node_id`
   - `evidence[].ref.file` 이 `manifest.sources[].path` 와 일치
   - `evidence[].ref.lines` 가 해당 파일 줄 범위 내
6. **annotated transcript**
   - 원본 전사와 마커 외 줄 텍스트 동일.
   - `[[SEG/NODE/EVID]]` id 가 모두 sidecar에 실재.
7. **파생 md (`*_래그.md` / `*_로데이터디벨롭.md` / `*_인용보강.md`)**
   - 본문에 등장한 모든 `node_id`/`evidence_id`/`segment_id`/`anchor_id` 가 sidecar에 실재 (고스트 0건).
   - 헤더 메타 키 순서가 `_framework/SCHEMAS.md` §10 과 일치.
8. **정책 (Rule A / B′ / D)**
   - Rule A: `L = segments` 행 수, 강별 `G` 와 비교 → 통과/예외/위반.
   - Rule B′: `F_has_prelecture` 정의로 판정.
   - Rule D: md-primary 노드는 evidence가 `lecture_md_anchor` 1차 + transcript 보조 형태인지 확인.

각 항목은 **표** 로 OK/누락/위반을 기록한다.

---

## 검증 리포트 양식

```
# <lecture_id> 검증 리포트 (YYYY-MM-DD HH:MM)

## 1. manifest
- ok / fail (사유)

## 2. anchor / segment / edge / evidence id 무결성
| 항목 | 총 | OK | 누락 | 비고 |
|------|----|----|------|------|

## 3. 정책 (Rule A / B′ / D)
- Rule A: L=<…>, G=<…>, 판정 <…>
- Rule B′: <…>
- Rule D: md-primary 노드 표

## 4. 파생 md 고스트 id
- `*_래그.md`: 0건 / N건 (목록)
- `*_로데이터디벨롭.md`: 0건 / N건 (목록)

## 5. 결론
- EXPORT OK / EXPORT BLOCKED (블로킹 항목 목록)
```

---

## EXPORT (검증 통과 시)

루트에서 다음을 실행한다.

```
node docs.js --inventory-derived-only
```

또는 로데이터/인용보강만 한 폴더에 모으려면:

```
node docs.js --inventory-raw-develop-flat
```

생성 위치:

- 강별: `docx-export/<course>/_inventory-derived/<lecture_id>/`
- 단일 폴더 모음: `docx-export/<course>/_inventory-raw-develop-flat/`

---

## README 갱신 (선택)

- `<course>/_inventory/<lecture_id>/README_inventory.md`(있으면) 표 한 줄 추가/갱신.
- `<course>/README*.md` 의 강 인덱스 갱신.

---

## 한 줄 미션

`<lecture_id>` 산출물 전체에 대해 “검증 항목 1–8”을 표로 보고하라. 한 항목이라도 fail이면 `EXPORT BLOCKED` 으로 끝내고, 모두 OK 면 `node docs.js --inventory-derived-only` 로 docx를 내보낸 뒤 산출 경로를 보고하라.
