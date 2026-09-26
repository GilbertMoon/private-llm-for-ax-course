# Chapter 05. Private AI 업무 서비스 구축

## 이번 강의에서 할 일

Chapter 04의 Terminal 기반 RAG에 Streamlit UI를 연결합니다.

```text
User
→ Streamlit UI
→ Question
→ Retrieval
→ Retrieved Evidence
→ Local LLM
→ Answer + Source
```

이번 장의 목표는 예쁜 챗봇이 아니라 **근거와 상태를 확인할 수 있는 업무용 AI Assistant**입니다.

## 학습 목표

- Streamlit의 역할을 설명한다.
- UI와 RAG 로직의 책임을 구분한다.
- Ready / Loading / Success / No Evidence / Error 상태를 구분한다.
- Retrieval Evidence와 Source를 UI에 표시한다.
- Local Server 중지 등 실패 상황을 처리한다.

## 프로젝트 구조

```text
chapter05/
├─ README.md
└─ starter/
   ├─ app.py
   └─ rag.py
```

## STEP 1. 실행 환경 확인

저장소 루트에서 가상환경을 활성화합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

필요한 패키지가 설치되어 있지 않다면:

```powershell
python -m pip install -r requirements.txt
```

LM Studio Local Server도 `Running` 상태여야 합니다.

```powershell
Test-NetConnection localhost -Port 1234
```

정상 목표:

```text
TcpTestSucceeded : True
```

## STEP 2. 실제 Model ID 확인

```powershell
(Invoke-RestMethod http://localhost:1234/v1/models).data.id
```

2026-09-26 실제 검증 예:

```text
qwen/qwen3-4b-2507
text-embedding-nomic-embed-text-v1.5
```

## STEP 3. 환경변수 설정

`starter/rag.py`를 직접 수정하지 않습니다.

PowerShell에서 실제 Model ID를 설정합니다.

```powershell
$env:CHAT_MODEL_ID="qwen/qwen3-4b-2507"
$env:EMBEDDING_MODEL_ID="text-embedding-nomic-embed-text-v1.5"
$env:LM_STUDIO_BASE_URL="http://localhost:1234/v1"
```

> 위 Model ID는 실제 검증 예입니다. 수업 시점에는 `/v1/models`에서 확인한 값을 우선합니다.

## STEP 4. Runtime Gate 재확인

Streamlit을 실행하기 전에 API와 Embedding이 정상인지 확인합니다.

```powershell
python scripts/runtime_validate.py
```

정상 목표:

```text
Gate 1. Models Endpoint   PASS
Gate 2. Chat Completion   PASS
Gate 3. Embedding         PASS
```

## STEP 5. Streamlit 실행

저장소 루트에서 실행합니다.

```powershell
streamlit run chapter05\starter\app.py
```

정상적으로 실행되면 Browser에서 보통 다음 주소가 열립니다.

```text
http://localhost:8501
```

## 상태 모델

```text
Ready
→ 질문 입력 대기

Loading
→ Retrieval / Generation 진행

Success
→ 근거와 답변 표시

No Evidence
→ 문서 근거 부족

Error
→ Server / Model / Application 오류
```

중요:

```text
No Evidence
≠
Error
```

문서에 없는 질문에 답하지 않는 것은 정상 동작일 수 있습니다.

## STEP 6. Positive Test

질문:

```text
지방 출장 숙박비 한도는 얼마인가요?
```

확인할 것:

```text
질문 입력 가능
Loading 상태
답변 표시
Retrieval Evidence / Source 표시
정답 Chunk 포함
Similarity Score 표시
```

2026-09-26 실제 검증 답변:

```text
지방 출장 숙박비 한도는 1박 최대 100,000원입니다.
```

실제 Evidence에는 다음 정답 Chunk가 포함되었습니다.

```text
company_policy.txt / chunk 3
1. 국내 출장 숙박비
- 서울: 1박 최대 120,000원
- 지방: 1박 최대 100,000원
```

## STEP 7. Negative Test

문서에 없는 질문 예:

```text
해외 출장 시 항공권은 비즈니스석으로 이용할 수 있나요?
```

기대 결과:

```text
제공된 문서에서 확인할 수 없습니다.
```

이 상태는 Application Error가 아니라 **근거가 없는 정상적인 No Evidence 처리**입니다.

## STEP 8. Failure Test

LM Studio Developer 화면에서 Local Server를 중지합니다.

```text
Status: Running
→ Status: Stopped
```

Streamlit은 그대로 두고 다시 질문합니다.

기대 결과:

```text
Application이 비정상 종료되거나 무한 대기하지 않고
사용자에게 Error 상태를 표시
```

현재 Starter는 연결 오류일 때 다음과 같이 안내합니다.

```text
LM Studio Local Server에 연결할 수 없습니다.
LM Studio의 Developer > Local Server에서 서버가 Running 상태인지 확인해 주세요.
```

테스트 후에는 Local Server를 다시 `Running` 상태로 복원합니다.

## Evidence

```text
Streamlit UI
localhost:8501
질문 입력
Loading 상태
Retrieved Evidence
Answer
Source
No Evidence
Server Stop Error
```

## 혼자 해보기

다음 중 하나를 추가합니다.

- Source 표시 영역 개선
- 대화 기록 유지
- 검색된 Chunk 3개 표시
- Reset 버튼
- 현재 Model ID 표시

단, UI를 수정한 뒤에도 Retrieval과 Answer가 정상인지 다시 검증합니다.

## 완료 기준

```text
[ ] Streamlit UI를 실행했다.
[ ] 질문을 입력할 수 있다.
[ ] Retrieval Evidence를 볼 수 있다.
[ ] Answer와 Source가 표시된다.
[ ] 문서에 없는 질문을 테스트했다.
[ ] Local Server 오류를 테스트했다.
[ ] 오류 후 Server를 복원하고 다시 정상 동작을 확인했다.
[ ] UI와 RAG 책임을 구분할 수 있다.
```

## 다음 강의

Chapter 06에서는 이 Prototype을 실제 기업 환경에 적용하려면 무엇이 더 필요한지 검토합니다.
