# Windows Local Runtime Runbook

이 문서는 Windows PC에서 Private LLM for AX 실습 환경을 실제로 검증하는 순서를 정리합니다.

목표는 설치 자체가 아니라 다음 Runtime Gate를 순서대로 통과하는 것입니다.

```text
Offline Test
→ LM Studio Server
→ Chat
→ Embedding
→ RAG
→ Negative Test
→ Streamlit
→ Failure Case
```

---

## 0. 사전 준비

필요한 프로그램:

```text
Git
Python 3.11 이상
VS Code
LM Studio
```

권장:

```text
RAM 16GB 이상
전용 GPU가 있다면 VRAM 4GB 이상
```

PC 사양이 낮다면 큰 모델보다 4B급 Quantized Model을 우선 사용합니다.

---

## 1. Repository Clone

PowerShell:

```powershell
cd C:\dev
git clone https://github.com/GilbertMoon/private-llm-for-ax-course.git
cd private-llm-for-ax-course
code .
```

이미 Clone했다면:

```powershell
git pull origin main
```

---

## 2. Python 가상환경

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

정상 확인:

```powershell
python --version
pip --version
```

---

## 3. Gate 0 — Offline Test

LM Studio를 실행하기 전에 먼저 Repository 자체를 확인합니다.

```powershell
pytest -q
```

정상:

```text
모든 test PASS
```

추가 문법 검사:

```powershell
python -m compileall chapter03 chapter04 chapter05 scripts tests
```

---

## 4. LM Studio — Chat Model 준비

LM Studio에서 Chat용 Local Model을 준비합니다.

수업 기본 후보:

```text
Qwen3-4B-Instruct-2507
Quantization: Q4_K_M
```

PC 자원이 충분하면 8B급 모델도 사용할 수 있습니다.

중요:

```text
인터넷에서 본 Model ID를 코드에 복사하지 않습니다.
```

실제 LM Studio가 제공하는 ID를 이후 `/v1/models`로 확인합니다.

---

## 5. LM Studio — Embedding Model 준비

Embedding Model도 별도로 준비합니다.

수업 후보:

```text
BGE-m3-ko
Quantization: Q8_0
```

역할:

```text
Chat Model
→ 답변 생성

Embedding Model
→ Text를 Vector로 변환
```

---

## 6. LM Studio Local Server 시작

LM Studio에서 Local Server를 시작합니다.

수업 기본 URL:

```text
http://localhost:1234
```

기본 실습에서는 LAN 공개를 하지 않습니다.

---

## 7. Gate 1 — Server / Model List

```powershell
python scripts/runtime_preflight.py
```

또는:

```powershell
Invoke-RestMethod http://localhost:1234/v1/models
```

반드시 다음 두 ID를 기록합니다.

```text
CHAT_MODEL_ID
EMBEDDING_MODEL_ID
```

---

## 8. 환경변수 설정

예시는 실제 ID로 교체합니다.

```powershell
$env:CHAT_MODEL_ID="<실제 Chat Model ID>"
$env:EMBEDDING_MODEL_ID="<실제 Embedding Model ID>"
```

확인:

```powershell
echo $env:CHAT_MODEL_ID
echo $env:EMBEDDING_MODEL_ID
```

---

## 9. Gate 2~3 — Chat + Embedding

```powershell
python scripts/runtime_validate.py
```

확인:

```text
Chat Completion PASS
Embedding PASS
Vector Dimension 확인
```

실패하면 먼저 다음을 확인합니다.

```text
LM Studio Server Running?
Model Load 상태?
Model ID 정확한가?
localhost:1234 맞는가?
```

---

## 10. Gate 4~6 — RAG

Chapter 04 starter의 Model ID placeholder를 실제 ID로 바꾸거나 강의 지시에 따라 환경변수 방식으로 수정합니다.

실행:

```powershell
python chapter04/starter/rag.py
```

정상 질문:

```text
서울 출장 시 숙박비 한도는 얼마인가요?
```

확인:

```text
관련 출장규정 Chunk 검색
Similarity Score 표시
Source 표시
답변이 문서 내용과 일치
```

Negative Test:

```text
회사에서 제주도 렌터카를 하루 얼마까지 지원하나요?
```

문서에 근거가 없다면 추측하지 않아야 합니다.

---

## 11. Gate 7 — Streamlit

```powershell
streamlit run chapter05/starter/app.py
```

브라우저에서 확인:

```text
질문 입력
Loading
Answer
Source
Retrieval Evidence
No Evidence
```

---

## 12. Gate 8 — Failure Case

Streamlit이 열린 상태에서 LM Studio Server를 중지합니다.

다시 질문합니다.

확인:

```text
무한 대기하지 않는가?
오류를 사용자가 확인할 수 있는가?
Application 전체가 비정상 종료되지 않는가?
```

---

## 13. Evidence 기록

다음 문서를 복사해 실제 결과를 기록합니다.

```text
docs/RUNTIME_EVIDENCE_TEMPLATE.md
```

반드시 기록할 것:

```text
Windows / CPU / RAM / GPU / VRAM
Python Version
LM Studio Version
실제 Chat Model ID
실제 Embedding Model ID
각 Gate PASS / FAIL
실패 원인
수정 내용
재검증 결과
```

---

## 14. 최종 판정

모든 Gate 통과 시:

```text
RUNTIME RELEASE / PASS
```

하나라도 실패하면:

```text
FIX REQUIRED
```

실패한 Gate부터 수정하고 다시 검증합니다.
