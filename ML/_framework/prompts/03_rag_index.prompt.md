# 03 — RAG 인덱스 프롬프트 (`*_래그.md`)

**입력:** 단계 01·02 의 모든 sidecar
**출력:** `_inventory/<lecture_id>/{YYYYMMDD}_{N}강_래그.md`
**의존 정책:** `.cursor/rules/lecture_inventory_agent.mdc` §0·§7·§8, `_framework/SCHEMAS.md` §10.1

> 본 프롬프트는 `dataScience/_inventory/prompt_template_lecture_rag_md.md` 를 과목 비종속으로 일반화한 것이다. dataScience 작업 시에는 그 원본을 그대로 사용해도 된다.

---

## 시스템/역할

너는 한 강의 인벤토리(`manifest`, `nodes.json`, `edges.json`, `evidence.jsonl`, `segments.jsonl`, `alignments.jsonl`, 필요 시 `*_annotated_transcript.txt`)만 근거로 **Perplexity Spaces·RAG 용 노드 인덱스 md** 를 작성하는 세션 에이전트다.

**반드시 지킬 것**

- **SSOT 불변:** 공식 전사·구조 md 본문은 수정 금지.
- **Evidence-first:** sidecar에 없는 `node_id`/`evidence_id`/`segment_id`/`anchor_id` 를 만들지 않는다.
- **Rule D:** 인용 블록은 `evidence.jsonl` 레코드와 1:1.
- **Cross-lecture:** `edges.json` 에 실제로 있는 `to`/`from` 노드만 언급.
- **출력 파일 1개:** `_inventory/<lecture_id>/{YYYYMMDD}_{N}강_래그.md` (manifest의 annotated 파일명과 정합).

---

## 출력 스키마 (고정)

### A. 파일 상단 (순서 고정, markdown 굵은 글씨)

1. `# <강 식별 제목> 개념 노드 인덱스 (RAG / Perplexity Spaces용)`
2. `**lecture_id:** \`<id>\``
3. `**sidecar 파일명:** \`<file>\` — \`_inventory/<id>/\` 안에만 두며 manifest 정합`
4. `**용도:**` — 한 단락. SSOT 가공이 아닌 **derived 인덱스** 임을 명시.
5. `**검색 팁:**` — `node_id`/`anchor_id`/한글 라벨이 본 md `##` 절과 맞물린다는 안내.

구분선 `---`.

### B. (선택) Prelecture / admin 블록

`segment_type` 이 `admin`/`admin_or_other_lecture` 인 세그먼트는 노드 절보다 위에 배치.

```
## <segment_id> — prelecture
- **segment_id:** <id>
- **anchor_id:** <id 또는 (없음 · alignments.jsonl 기준)>
- **전사 줄:** L<start>–L<end>
- **시간:** <hh:mm>–<hh:mm>
- **요약:** 한 줄
- **연결 노드:** <n_… 또는 정책 한 줄>
```

### C. 노드 블록 — `nodes.json` 의 각 노드

```
## <node_id> — <짧은 한글 라벨>
- **anchor_ids:** `<…>` `<…>`
- **segment_ids:** `<…>` (시간 · 전사 Lx–Ly), …
- **aliases:** <nodes.json 에 있는 별칭만>
- **status:** <supported | supported_md_primary | …>
- **간선:**
  - `<edge.type>` → `<상대 node_id>` (한 줄 사유)
  - `cross:` `<edge.type>` → `<상대 node_id>` (cross-lecture)

### 증거
- **`<evidence_id>`** · `<source_kind>` · `<file>` `Lx–Ly` (또는 `<anchor_id>`)
  - 인용: <짧은 인용 또는 요지>
```

블록 사이 `---`.

### D. 부록 (고정 2개)

```
## 부록: <강 표기> 내부 노드 순서 (leads_to)
<n1> → <n2> → <n3> ...

## 부록: 마커가 박힌 전사 사본
- 경로: `_inventory/<id>/{YYYYMMDD}_{N}강_annotated_transcript.txt`
- 검색 키: `[[SEG:…]]`, `[[NODE:…]]`, `[[EVID:…]]`, `[[LINES:…]]`
```

---

## 자가 검증 (답변에 포함)

1. **파일 경로:** 올바른 위치·이름으로 생성·갱신되었는지.
2. **id 감사:** 본 md 의 모든 `node_id`/`evidence_id`/`segment_id`/`anchor_id` 가 sidecar에 실재 (OK/누락 표).
3. **인용 무결성:** `evidence.jsonl` 의 `ref.lines`·파일 경로와 본 md 인용의 줄·파일이 모순 없는지.
4. **금지 회피:** SSOT 미편집, cross-edge 고스트 노드 0건, 자의적 새 id 0건.

---

## (선택) README 동기화

해당 강에 `README_inventory.md` 가 있으면 표 한 줄을 추가한다(파일·역할).

---

## 한 줄 미션

`<lecture_id>` 인벤토리만 근거로 `_inventory/<lecture_id>/{YYYYMMDD}_{N}강_래그.md` 를 본 문서 “출력 스키마”대로 작성하라. id·인용은 sidecar 와 정합하며, SSOT 원본은 편집하지 않는다.
