# 04 — 로데이터 디벨롭 프롬프트 (`*_로데이터디벨롭.md` / `*_인용보강.md`)

**입력:** 단계 01·02·03 산출물 + 구조 SSOT md
**출력:** `_inventory/<lecture_id>/{YYYYMMDD}_{N}강_로데이터디벨롭.md` (또는 `*_인용보강.md`)
**의존 정책:** `.cursor/rules/lecture_inventory_agent.mdc` §8 (특히 §8.2 “insert-only”)

> 본 프롬프트는 `dataScience/_inventory/prompt_template_lecture_raw_develop.md` 를 과목 비종속으로 일반화한 것이다.

> **DecisionMaking PDF-only 배치:** 구조 SSOT는 PDF full transcript md와 PDF anchors다. 출력은 `_inventory/DM_PDFxx__<slug>/DM_PDFxx__<slug>__rawdata_develop.md`로 둔다. 설명은 원문 전사 보존, 표/수식 재구성, 기존 1~7강 노트와의 연결을 모두 포함한다.

---

## 시스템/역할

너는 §8 “로데이터 디벨롭” 단계의 세션 에이전트다. **루트 구조 SSOT md** 본문은 건드리지 않고, sidecar 사본(`*_로데이터디벨롭.md`) 에 §8.2 패턴 A 인용·메타 마커를 **insert-only** 로 추가해 학습·검색용 보강 노트를 만든다.

DecisionMaking PDF-only 배치에서는 루트 md를 수정하지 않고, PDF transcript 기반 derived view를 새로 쓴다. 즉 원문 PDF/transcript는 불변이고, rawdata develop md 안에서 정의·직관·수식·예제·오류 포인트를 보강한다.

**반드시 지킬 것**

- 루트 md 본문·목차·heading 순서 **삭제·재작성 금지**.
- 새 본문 단락을 추가하지 않는다 — **인용 박스 + 메타 마커**만 추가.
- 모든 `[[NODE]]`/`[[SEG]]`/`[[EVID]]` 는 sidecar에 실재하는 id만.
- 인용 줄 번호 정본은 정책 박스에 명시한 단일 기준(예: `루트 md 기준` 또는 `raw 미러 기준`) 으로 일관.
- 5강처럼 인용만 보강하는 변형 파일명은 `*_인용보강.md` 사용 가능.

---

## 입력 파일 표

| 파일 | 용도 |
|------|------|
| `<course>/{YYYYMMDD}_{N}강.md` | 루트 구조 SSOT (읽기 전용 — 본 작업에 직접 인용) |
| `_inventory/<id>/raw/...md` | 무표기 미러 (있을 때) |
| `_inventory/<id>/nodes.json` / `evidence.jsonl` | 인용·마커 id |
| `_inventory/<id>/{YYYYMMDD}_{N}강_annotated_transcript.txt` | 전사 줄·시간 교차검증 |

---

## 출력 스키마 (고정)

### A. 헤더

```
# <과목·회차 표기> — 로데이터 디벨롭

| 항목 | 값 |
|------|----|
| **세션 목표** | … (한 단락) |
| **구조 md 로데이터 원본 (디벨롭 기준)** | `<루트 md 또는 raw 미러 경로>` — 줄 번호 정본 |
| **공식 전사** | `<전사 path>` (불변) |
| **인벤토리 sidecar** | `manifest.json`, `nodes.json`, `evidence.jsonl`, … |

**정책:** 공식 전사·루트 구조 md는 임의 수정하지 않음(루트 md는 §8.2 insert-only 만). 본 로데이터 문서는 파생 보강이며, `[[NODE]]`·`[[SEG]]`·`[[EVID]]` 는 `evidence.jsonl` 에 있는 id만 단다. md 인용 줄번호는 항상 `<정본 경로>` 기준이다.
```

### B. 본문 — 루트 md 절 순서 그대로

각 절(예: `## 2. 데이터 준비와 Raw Data`) 아래에 다음 패턴만 추가:

```
> [전사 L<start>–L<end>] <짧은 인용>
> `[[SEG:<segment_id>]] [[NODE:<node_id>]] [[EVID:<evidence_id>]]`
```

또는 md 인용:

```
> [md L<start>–L<end>] <짧은 인용>
> `[[NODE:<node_id>]] [[EVID:<evidence_id>]]`
```

### C. 마지막 절 — `### 부록: 전사 로데이터 인용 (인벤토리 §8)`

- `*_annotated_transcript.txt` 경로
- 마커 검색 키 (`[[SEG]]`, `[[NODE]]`, `[[EVID]]`)

---

## 자가 검증 (답변에 포함)

1. **루트 md 미수정:** 본 작업 도중 루트 `<course>/{YYYYMMDD}_{N}강.md` 의 변경 0줄.
2. **id 감사:** 본 md 의 모든 마커 id 가 sidecar에 실재 (OK/누락 표).
3. **줄번호 정본:** 인용에 쓴 `L<start>–L<end>` 가 정책 박스의 “정본 경로” 줄 번호와 일치.
4. **insert-only:** 추가된 줄은 인용 박스 + 마커뿐, 새 본문 단락 0건.

---

## 한 줄 미션

`<lecture_id>` 의 루트 md 본문은 그대로 두고, `_inventory/<id>/{YYYYMMDD}_{N}강_로데이터디벨롭.md` 를 본 문서 “출력 스키마”대로 작성하라. 인용·마커는 evidence/segments/nodes 와 정합해야 하며, 줄번호 정본은 정책 박스에 박은 단일 기준으로 일관시킨다.
