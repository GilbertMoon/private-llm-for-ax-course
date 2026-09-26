# Runtime Validation Evidence Report

상태: **LOCAL RUNTIME VALIDATION READY**

이 문서는 실제 Windows + LM Studio 환경에서 Chapter 02~05 실행 결과를 기록하기 위한 템플릿입니다.

---

## 1. 실행 환경

```text
Date:
Windows Version:
CPU:
RAM:
GPU:
VRAM:
Python Version:
LM Studio Version:
```

리소스 Evidence 수집 보조 스크립트:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/windows_resource_evidence.ps1
```

가능하면 LM Studio 모델 Load 전과 후에 각각 한 번 실행하여 RAM / VRAM 변화를 비교합니다.

---

## 2. 사용 모델

### Chat Model

```text
Model Name:
LM Studio Model ID:
Quantization:
```

### Embedding Model

```text
Model Name:
LM Studio Model ID:
Quantization:
```

주의:

실제 코드에는 인터넷 예제의 Model ID를 복사하지 않고 `/v1/models`에서 확인한 값을 사용합니다.

2026-09-26 실제 검증 예시는 다음 조합으로 통과했습니다.

```text
Chat Model ID: qwen/qwen3-4b-2507
Chat Quantization: Q4_K_M
Embedding Model ID: text-embedding-nomic-embed-text-v1.5
LM Studio: 0.4.25
Windows 11
Python 3.12.10
```

---

## 3. Gate 1 — LM Studio Server / Models

실행:

```powershell
python scripts/runtime_preflight.py
```

또는:

```powershell
Invoke-RestMethod http://localhost:1234/v1/models
```

결과:

```text
PASS / FAIL
```

Evidence:

```text
Server URL:
Detected Model IDs:
Error if any:
```

---

## 4. Gate 2 — Chat Completion

환경변수:

```powershell
$env:CHAT_MODEL_ID="<실제 Chat Model ID>"
```

실행:

```powershell
python scripts/runtime_validate.py
```

결과:

```text
PASS / FAIL
```

Evidence:

```text
Prompt:
Response:
Elapsed Time:
Error if any:
```

---

## 5. Gate 3 — Embedding

환경변수:

```powershell
$env:EMBEDDING_MODEL_ID="<실제 Embedding Model ID>"
```

결과:

```text
PASS / FAIL
```

Evidence:

```text
Vector Dimension:
First Values:
Error if any:
```

Nomic 계열 Embedding을 사용할 때는 retrieval task prefix가 필요할 수 있습니다. 현재 Starter는 `text-embedding-nomic-embed-text-v1.5` 사용 시 문서에는 `search_document:`, 질문에는 `search_query:`를 자동 적용합니다.

---

## 6. Gate 4 — RAG Retrieval

실행:

```powershell
python chapter04/starter/rag.py
```

Positive Test 권장 질문:

```text
지방 출장 숙박비 한도는 얼마인가요?
```

기대:

```text
국내 출장 숙박비 Chunk가 Top-k에 포함된다.
Source와 Similarity Score를 확인할 수 있다.
```

결과:

```text
PASS / FAIL
```

Evidence:

```text
Matched Chunk:
Score:
Source:
```

---

## 7. Gate 5 — Grounded Answer

기대:

```text
검색된 Context에 있는 정보만 사용해 답한다.
답변이 Sample Policy와 일치한다.
```

결과:

```text
PASS / FAIL
```

Evidence:

```text
Question:
Retrieved Context:
Answer:
Source:
```

---

## 8. Gate 6 — Negative Test

질문 예:

```text
해외 출장 시 항공권은 비즈니스석으로 이용할 수 있나요?
```

Sample Policy에 근거가 없다면 기대 답변:

```text
제공된 문서에서 확인할 수 없습니다.
```

결과:

```text
PASS / FAIL
```

---

## 9. Gate 7 — Streamlit UI

실행:

```powershell
streamlit run chapter05/starter/app.py
```

확인:

```text
[ ] 질문 입력 가능
[ ] Loading 표시
[ ] 답변 표시
[ ] Source 표시
[ ] Retrieval Evidence 확인
[ ] 문서에 없는 질문 처리
```

결과:

```text
PASS / FAIL
```

---

## 10. Gate 8 — Failure Case

LM Studio Server를 중지한 뒤 다시 질문합니다.

기대:

```text
Application이 무한 대기하거나 종료되지 않는다.
사용자가 이해할 수 있는 연결 오류 안내가 표시된다.
```

현재 Starter의 기대 안내:

```text
LM Studio Local Server에 연결할 수 없습니다.
LM Studio의 Developer > Local Server에서 서버가 Running 상태인지 확인해 주세요.
```

결과:

```text
PASS / FAIL
```

---

## 11. RAM / VRAM Evidence

LM Studio Server가 Running이고 모델이 Load된 상태에서 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/windows_resource_evidence.ps1
```

Evidence:

```text
RAM Total:
RAM Used before model load:
RAM Used after model load:
GPU Name:
VRAM Total:
VRAM Used before model load:
VRAM Used after model load:
GPU Utilization during inference:
```

NVIDIA가 아닌 경우 Windows 작업 관리자 > 성능 > GPU에서 `전용 GPU 메모리` 사용량을 캡처합니다.

---

## 12. 최종 판정

```text
Gate 1 /v1/models          PASS / FAIL
Gate 2 Chat Completion     PASS / FAIL
Gate 3 Embedding           PASS / FAIL
Gate 4 Retrieval           PASS / FAIL
Gate 5 Grounded Answer     PASS / FAIL
Gate 6 Negative Test       PASS / FAIL
Gate 7 Streamlit           PASS / FAIL
Gate 8 Failure Case        PASS / FAIL
RAM / VRAM Evidence        COMPLETE / PENDING
```

최종:

```text
RUNTIME RELEASE / PASS
또는
FIX REQUIRED
```

---

## 13. 발견된 문제와 수정 기록

```text
Issue:
Cause:
Fix:
Re-test Evidence:
```

필요한 만큼 반복합니다.
