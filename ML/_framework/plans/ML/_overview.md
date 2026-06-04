# ML `final_brief` / `final_record` → 인벤토리 배치 개요

> **WSL 정본 경로(실파일):** `~/projects-wsl/hongikUniv.-26_1/ML/`
> Windows UNC: `\\wsl.localhost\Ubuntu-24.04\home\sieg\projects-wsl\hongikUniv.-26_1\ML\`

## 입력 디렉터리 (고정)

| 역할 | WSL 경로 | 내용 |
|------|----------|------|
| **구조 SSOT 원본** (보완 강의록 md) | `ML/final_brief/*.md` | 사람이 정리한 강의록 본문 |
| **내용 SSOT 원본** (녹음 전사 txt) | `ML/final_record/*.txt` | Clova 등 전사 **실파일 전부** |

프레임워크 표준 SSOT는 부트스트랩 후 **`ML/{YYYYMMDD}_{N}강.md`** · **`ML/{YYYYMMDD}_{N}강_강의록.txt`** 이다. `final_*` 는 **읽기 전용 소스**로 두고, 복사만 한다.

## 날짜·전사 페어링 (1차 매핑 — 에이전트가 H1에서 `N` 확인)

| `final_brief` | `lecture_id` (권장) | `final_record` 전사 (1차) | 비고 |
|---------------|---------------------|---------------------------|------|
| `20260430.md` | `20260430_<N>` | `기계학습0430.txt` | H1에서 N강 번호 추출 |
| `20260507.md` | `20260507_<N>` | `기계학습0507.txt` | |
| `20260514.md` | `20260514_11` (예: 11강) | `0514ml.txt` | 실측 H1: «11강» |
| `20260521.md` | `20260521_<N>` | `0521Ml.txt` | |
| `20260528.md` | `20260528_<N>` | `0528ml.txt` | |
| `20260529.md` | `20260529_<N>` | `0529_ml.txt` | 보조: `0529이용오교수님.txt` → `conflicts` |
| `20260604.md` | `20260604_<N>` | `0604ml.txt` | |
| *(brief 없음)* | — | `0522ml.txt` | **고아 전사** — brief 유무·회차를 `conflicts`에 기록 |

`lecture_id` = `YYYYMMDD_N` (`N` = 과목 **회차 숫자만**, `_강` 없음). sidecar 파일명 = `{YYYYMMDD}_{N}강_*`.

## 과목 Δ

| 항목 | 값 |
|------|-----|
| `<course>` | `ML` |
| `COURSE_PREFIX` | `ML` |
| `anchor_id` | `ML{N}.A.{k}` |
| `node_id` | `n_ML{N}.{snake}` |
| `evidence_id` | `ev_{lecture_id}_{seq}` |
| `segment_type` 추가 권장 | `code_demo`, `interactive_html` (슬라이드·노트북 시연) |

## DOCX (WSL)

```bash
cd ~/projects-wsl/hongikUniv.-26_1
npm install
node docs.js --inventory-derived-only --inventory-course ML
# 출력: docx-export/ML/_inventory-derived/<lecture_id>/*.docx
```

## 에이전트 프롬프트

- 마스터 지시: [`../../prompts/00_ML_final_batch_ubuntu_agent.prompt.md`](../../prompts/00_ML_final_batch_ubuntu_agent.prompt.md)
