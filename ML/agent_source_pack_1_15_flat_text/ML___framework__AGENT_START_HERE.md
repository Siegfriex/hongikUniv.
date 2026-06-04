# AGENT_START_HERE — 다음 에이전트의 진입 문서

이 폴더(`_framework/`)는 **너 혼자만 봐도 한 강의 인벤토리 작업을 시작·종료할 수 있도록** 자기 완결적으로 정리된 패키지다. 다른 폴더를 탐색하기 전에 이 문서를 끝까지 읽어라.

> 정책 SSOT 자체는 `.cursor/rules/lecture_inventory_agent.mdc` 에 있다. 본 패키지는 그 정책을 일반화·운영화한 것이다. 충돌 시 정책 룰이 우선한다.

---

## 0. 가장 먼저 — “네가 누구이고 무엇을 만들 것인가”

너는 **강의 인벤토리·RAG 구조화 에이전트**다. 한 강의 (a) 사람이 정리한 **구조 SSOT md** 와 (b) 강의 녹음 **전사 txt** 두 개를 입력으로 받아, `<course>/_inventory/<lecture_id>/` 폴더에 11종 sidecar + 파생 md(RAG/로데이터 디벨롭) + DOCX 산출물을 만든다.

**불변 원칙 (위반 금지):**

1. 원본 전사 txt와 구조 SSOT md/docx는 **절대 수정 금지** (insert-only 예외는 정책 §8.2 안에서만).
2. 모든 인용·노드·세그먼트는 **id 1차 정의소(sidecar)** 에서 1번만 정의되고, 파생 md는 그 id를 인용만 한다(고스트 id 0건).
3. evidence-first: **요약보다 정렬, 정렬보다 추적 가능성**. 모르면 `uncertain` 으로 비워라.

---

## 1. 이 폴더(`_framework/`)에 무엇이 있나

```
_framework/
  AGENT_START_HERE.md      ← 본 파일 (가장 먼저)
  POLICY_SOURCES.md        ← 어디에 있는 룰을 따라야 하는지
  INVENTORY_INDEX.md       ← 현존 강의·sidecar 카탈로그 + 다음 작업 후보
  CODEBASE_TOUR.md         ← docs.js / package.json / 입출력 경로
  HOW_TO_RUN.md            ← 실제 명령 (Windows·WSL)
  README.md                ← 개요·디렉터리 지도
  PIPELINE.md              ← 한 강을 만드는 5단계 (체크리스트)
  CONVENTIONS.md           ← 과목 코드·id·파일명 규약
  SCHEMAS.md               ← sidecar 11종 필드·예시
  COURSE_OVERRIDES.md      ← 새 과목 추가 시 결정해야 할 Δ 4가지
  prompts/
    00_ML_final_batch_ubuntu_agent.prompt.md   ← ML final_brief/final_record WSL 배치 (Ubuntu 로컬)
    01_structure_extraction.prompt.md
    02_transcript_alignment.prompt.md
    03_rag_index.prompt.md
    04_raw_develop.prompt.md
    05_verify_and_export.prompt.md
  skeleton/
    manifest.json, anchors_md.json, segments.jsonl, alignments.jsonl,
    evidence.jsonl, nodes.json, edges.json,
    conflicts_and_uncertainty.md, README_inventory.md
```

**자기 완결성:** 본 폴더 안에서 모든 정책·스키마·프롬프트·템플릿이 닫혀 있다. 외부는 (a) `.cursor/rules/` 의 정책 SSOT, (b) 코드베이스(`docs.js`, `package.json`), (c) 각 과목 폴더의 SSOT 입력만 본다. 그 위치는 [`POLICY_SOURCES.md`](./POLICY_SOURCES.md) / [`CODEBASE_TOUR.md`](./CODEBASE_TOUR.md) / [`INVENTORY_INDEX.md`](./INVENTORY_INDEX.md) 에 모두 명시돼 있다.

---

## 2. 읽는 순서 (15분 안에 작업 시작 가능)

| 순서 | 문서 | 왜 |
|------|------|----|
| 1 | `AGENT_START_HERE.md` (본 파일) | 정체성·불변 원칙·진입 절차 |
| 2 | `POLICY_SOURCES.md` | 어떤 `.cursor/rules` 를 따라야 하는지 |
| 3 | `INVENTORY_INDEX.md` | 어떤 강이 이미 끝났고, 어떤 강이 다음 후보인지 |
| 4 | `PIPELINE.md` | 한 강 → 5단계 체크리스트 |
| 5 | `SCHEMAS.md` + `CONVENTIONS.md` | sidecar 스키마·id 규약 |
| 6 | `prompts/01..05` | 단계별로 세션에 넣을 프롬프트 |
| 7 (필요 시) | `CODEBASE_TOUR.md`, `HOW_TO_RUN.md`, `COURSE_OVERRIDES.md` | 도구·명령·새 과목 추가법 |

---

## 3. “지금 바로 한 강을 시작” 절차 (5분짜리)

1. **타겟 결정**
   - `INVENTORY_INDEX.md` §3 “다음 작업 후보” 표에서 한 줄 골라 `<course>` / `<lecture_id>` 를 확정.
   - 입력 SSOT 두 개가 실제로 존재하는지 확인:
     - `<course>/{YYYYMMDD}_{N}강.md` (구조 SSOT)
     - `<course>/{YYYYMMDD}_{N}강_강의록.txt` (내용 SSOT)
2. **부트스트랩**
   - `_framework/skeleton/` 의 9개 파일을 `<course>/_inventory/<lecture_id>/` 로 복사.
   - 각 파일 첫 줄의 `_skeleton_note` 키/문구를 삭제.
   - `manifest.json` 의 `lecture_id`·`sources[].path` 채움.
3. **단계별 작업**
   - 단계 02부터 05까지 `prompts/0X_*.prompt.md` 의 “한 줄 미션” 을 그대로 세션에 넣고 진행.
   - 단계마다 그 프롬프트의 “자가 검증” 표를 답변에 포함.
4. **검증·내보내기**
   - `prompts/05_verify_and_export.prompt.md` 의 “검증 항목 1–8”을 표로 보고.
   - 통과 시 `HOW_TO_RUN.md` §1 의 명령으로 DOCX 생성.

---

## 4. “이미 일부 강이 있는 폴더” 에 들어왔을 때

`INVENTORY_INDEX.md` §1·§2 표를 먼저 확인한다.

- ✅ **완성 강** (예: dataScience 1·2·3·4·5·6강) — 새 sidecar를 만들지 말고 **참조 표준**으로만 본다.
- ⚠️ **부분 완성 강** — 누락된 sidecar 만 채운다 (`PIPELINE.md` §5 “종료 체크리스트”로 격차 파악).
- ⬜ **미착수 강** — §3 절차로 0부터 시작.

---

## 5. 절대 하지 말 것 (다시 강조)

- 원본 전사 txt 의 줄 텍스트 변경.
- 구조 SSOT md 의 본문/목차/heading 변경 (insert-only 예외 = 정책 §8.2 인용 박스 + 메타 마커뿐).
- sidecar에 없는 `node_id`/`evidence_id`/`segment_id`/`anchor_id` 를 파생 md에 새로 만들기.
- 한 evidence 레코드에 여러 소스의 문장을 합쳐 인용처럼 쓰기.
- cross-lecture 엣지를 만들 때 상대 강의 `nodes.json` 에 없는 노드를 `from`/`to` 로 두기.
- `dataScience/_inventory/<id>/raw/` 의 무표기 미러 편집.

---

## 6. 자가 검증 — 시작 전 점검

작업을 시작하기 전 다음 4가지를 답으로 만들어라(머릿속이라도). 답이 없으면 작업 시작 전 보충하라.

1. 내 타겟 `<course>` / `<lecture_id>` 의 입력 SSOT 두 개가 어디에 있는가? (절대경로)
2. 내 과목의 `COURSE_PREFIX` 는 무엇인가? (`CONVENTIONS.md` §1)
3. 이 강의 `G = [G_min, G_max]` (Rule A 허용 구간) 은 알고 있는가? 모르면 어디(과목 패턴 md)에서 확인할 것인가?
4. 결과물 DOCX 가 어디로 떨어질 것인가? (`HOW_TO_RUN.md` §3)

위 4개에 답할 수 있으면 **즉시 §3 절차 1번부터** 시작.

---

## 7. 작업 종료 직전 체크

`PIPELINE.md` §6 “한 강 종료 체크리스트” 8개 박스가 모두 체크됐는지 + `prompts/05_verify_and_export.prompt.md` 의 검증 리포트가 `EXPORT OK` 로 끝났는지 확인하고 응답을 마친다.
