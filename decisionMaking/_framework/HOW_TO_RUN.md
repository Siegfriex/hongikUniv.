# HOW_TO_RUN — 실제 명령 (Windows PowerShell 기준)

본 작업은 **노드 스크립트와 파일 편집만** 사용한다. 외부 컨테이너·GPU·DB 가 필요 없으므로 Windows PowerShell 또는 WSL 어디서 실행해도 같은 결과가 나온다.

---

## 0. 사전 준비 (1회)

```powershell
# 워크스페이스 이동
Set-Location "c:\Users\6sieg\OneDrive\바탕 화면\hongikUniv.-26_1"

# 의존성 설치 (한 번만)
npm install
```

WSL 에서 한다면:

```bash
cd /mnt/c/Users/6sieg/OneDrive/바탕\ 화면/hongikUniv.-26_1
npm install
```

> 사용자 전역 룰상 GCP/Docker/Java/Python/GPU 작업은 WSL 전용이다. 본 인벤토리 작업은 그런 의존성이 없다.

---

## 1. DOCX 빌드 명령

| 목적 | 명령 (PowerShell) |
|------|--------------------|
| 강의 md + 인벤토리 파생 md 모두 docx | `node docs.js` |
| 인벤토리 파생만 (강별 폴더) | `node docs.js --inventory-derived-only` |
| ML 인벤토리 파생만 | `node docs.js --inventory-derived-only --inventory-course ML` |
| 로데이터 디벨롭(+5강 인용보강) 한 폴더에 모음 | `node docs.js --inventory-raw-develop-flat` |
| 인벤토리 중 `*_래그.md` 만 (구 호환) | `node docs.js --rag-only` |
| 위 + `DS_global_patterns.md` (`_root/` 폴더) | `node docs.js --inventory-derived-only --inventory-root` |
| 강의 md 만 (인벤토리 스킵) | `node docs.js --no-inventory` |

또는 npm 별칭:

```powershell
npm run docx
npm run docx:inventory
npm run docx:inventory:ml
npm run docx:raw-develop-flat
npm run docx:rag
npm run docx:inventory+patterns
```

도움말:

```powershell
node docs.js --help
```

---

## 2. PowerShell 실행 시 주의

- `&&` 체이닝이 `cmd` 와 다르게 동작하므로 명령은 **세미콜론** 또는 **별도 줄**로 분리한다.

  ```powershell
  Set-Location "c:\Users\6sieg\OneDrive\바탕 화면\hongikUniv.-26_1"; node docs.js --inventory-derived-only
  ```

- 경로에 한글/공백이 있으면 **반드시 큰따옴표**로 감싼다.

---

## 3. 출력 경로 (생성 위치)

- 강의 md:
  ```
  docx-export/<course>/{YYYYMMDD}_{N}강.docx
  ```
- 인벤토리 파생 (강별):
  ```
  docx-export/dataScience/_inventory-derived/<lecture_id>/*.docx
  ```
- 로데이터 디벨롭 한곳 모음:
  ```
  docx-export/dataScience/_inventory-raw-develop-flat/*.docx
  ```
- 루트 보고용 (옵션):
  ```
  docx-export/dataScience/_inventory-derived/_root/*.docx
  ```

> 인벤토리 스캔 기본은 `dataScience/_inventory`. ML은 `--inventory-course ML` 또는 `npm run docx:inventory:ml`. 다과목은 `_framework/COURSE_OVERRIDES.md` §7 참조.

---

## 4. 한 강을 “0에서 끝까지” — 명령 순서

1. **부트스트랩 (수작업)**
   - `_framework/skeleton/` 9개 파일을 `<course>/_inventory/<lecture_id>/` 로 복사.
   - 각 파일 첫 줄의 `_skeleton_note` 키/문구를 삭제.
   - `manifest.json` 의 `lecture_id`·`sources[].path` 채움.
2. **단계 01–04 (세션에서 프롬프트 사용)**
   - 단계마다 `_framework/prompts/0X_*.prompt.md` 의 “한 줄 미션” 그대로 진행.
   - 자가 검증 표를 답변에 포함.
3. **단계 05 검증 (사람·LLM 둘 다)**
   - `_framework/prompts/05_verify_and_export.prompt.md` 의 검증 항목 1–8을 표로 통과.
4. **DOCX 내보내기**
   ```powershell
   node docs.js --inventory-derived-only
   ```
5. **인덱스 갱신**
   - `_framework/INVENTORY_INDEX.md` §2(또는 §1) 표에 행 추가.
   - 해당 과목의 `<COURSE>_global_patterns.md` 의 Rule A 표·P-패턴 행 추가.

---

## 5. 자주 쓰는 점검 명령

| 목적 | 명령 |
|------|------|
| 인벤토리 파일 한눈에 보기 | `Get-ChildItem -Recurse "<course>\_inventory" -File | Select-Object FullName, Length` |
| 한 강 sidecar 누락 점검 (PowerShell) | `Get-ChildItem "<course>\_inventory\<lecture_id>" -Name` |
| 파생 md 만 빠르게 docx 갱신 | `node docs.js --inventory-derived-only` |
| 로데이터 디벨롭 묶음만 갱신 | `node docs.js --inventory-raw-develop-flat` |

---

## 6. 실패 시 대응

| 증상 | 대응 |
|------|------|
| `docs.js` 가 `Cannot find module 'docx'` | 루트에서 `npm install` |
| docx 가 만들어지지 않고 `fail:` 출력 | 콘솔에 출력된 md 경로 열어 형식(코드블록 미닫힘 등) 확인 |
| 한글 파일명이 깨짐 | PowerShell 코드페이지 65001(UTF-8) 또는 WSL 사용 |
| 빈 docx 가 출력됨 | 단계 03/04 의 md 가 진짜 비어 있는지 확인 (헤더만 있고 본문 없음) |

---

## 7. 본 작업이 사용하지 않는 명령 (참고)

- `gcloud`, `gsutil`, `docker`, `kubectl` — 본 폴더 작업과 무관.
- `python` / `pip` — `dataScience/_inventory/*.py` 같은 도우미 스크립트가 있긴 하지만 **본 5단계 파이프라인을 진행하는 데 필수는 아니다**(있으면 보조).
