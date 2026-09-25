# Runtime Validation Evidence Report

상태: **PENDING LOCAL EXECUTION**

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

---

## 6. Gate 4 — RAG Retrieval

실행:

```powershell
python chapter04/starter/rag.py
```

질문 예:

```text
서울 출장 시 숙박비 한도는 얼마인가요?
```

기대:

```text
출장규정 관련 Chunk가 Top-k에 포함된다.
Source와 Similarity Score를 확인할 수 있다.
```

결과:

```text
PASS / FAIL
```

Evidence:

```text
Top-1 Chunk:
Top-1 Score:
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
회사에서 제주도 렌터카를 하루 얼마까지 지원하나요?
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
Application이 무한 대기하거나 종료되지 않고 오류를 사용자가 확인할 수 있다.
```

결과:

```text
PASS / FAIL
```

---

## 11. 최종 판정

```text
Gate 1 /v1/models          PASS / FAIL
Gate 2 Chat Completion     PASS / FAIL
Gate 3 Embedding           PASS / FAIL
Gate 4 Retrieval           PASS / FAIL
Gate 5 Grounded Answer     PASS / FAIL
Gate 6 Negative Test       PASS / FAIL
Gate 7 Streamlit           PASS / FAIL
Gate 8 Failure Case        PASS / FAIL
```

최종:

```text
RUNTIME RELEASE / PASS
또는
FIX REQUIRED
```

---

## 12. 발견된 문제와 수정 기록

```text
Issue:
Cause:
Fix:
Re-test Evidence:
```

필요한 만큼 반복합니다.
