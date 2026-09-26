# Chapter 03. Local LLM API 활용

## 이번 강의에서 할 일

Chapter 02에서는 사람이 LM Studio Chat에서 Local Model과 대화했습니다.

이번에는 Python Application이 Local API를 호출합니다.

```text
Python Application
→ localhost
→ LM Studio Server
→ Local Model
→ Response
```

## 학습 목표

- Application, API Server, Runtime, Model을 구분한다.
- `localhost`와 Port의 의미를 설명한다.
- LM Studio Local Server를 시작한다.
- `/v1/models`로 실제 Model ID를 확인한다.
- Python OpenAI Client의 `base_url`을 Local Server로 변경해 호출한다.
- Server Stop과 Wrong Model ID 오류를 구분한다.

## STEP 1. Local Server 시작

LM Studio에서 다음 화면으로 이동합니다.

```text
Developer
→ Local Server
→ Status: Running
```

기본 실습 주소:

```text
http://localhost:1234
```

PowerShell에서 Port를 확인합니다.

```powershell
Test-NetConnection localhost -Port 1234
```

정상 목표:

```text
TcpTestSucceeded : True
```

> `::1` IPv6 연결 경고가 먼저 나오더라도 최종적으로 `127.0.0.1`에 대해 `TcpTestSucceeded : True`이면 정상입니다.

## STEP 2. 실제 Model ID 확인

PowerShell:

```powershell
(Invoke-RestMethod http://localhost:1234/v1/models).data.id
```

또는 프로젝트 Preflight:

```powershell
python scripts/runtime_preflight.py
```

인터넷 예제의 Model 이름을 복사하지 말고 **현재 LM Studio가 반환한 실제 Model ID**를 사용합니다.

2026-09-26 실제 검증 예:

```text
qwen/qwen3-4b-2507
text-embedding-nomic-embed-text-v1.5
```

Chapter 03에서는 Chat Model ID를 사용합니다.

## STEP 3. Python 환경 준비

이 저장소의 **루트 폴더**에서 실행합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

이미 Chapter 02에서 가상환경과 패키지를 준비했다면 다시 만들 필요는 없습니다.

정상 확인:

```powershell
python -m pip show openai
```

## STEP 4. Chat Model 환경변수 설정

Starter 코드를 직접 수정하지 않습니다.

STEP 2에서 확인한 실제 Chat Model ID를 PowerShell 환경변수로 설정합니다.

실제 검증 예:

```powershell
$env:CHAT_MODEL_ID="qwen/qwen3-4b-2507"
```

필요한 경우 Base URL도 명시할 수 있습니다.

```powershell
$env:LM_STUDIO_BASE_URL="http://localhost:1234/v1"
```

현재 값 확인:

```powershell
$env:CHAT_MODEL_ID
$env:LM_STUDIO_BASE_URL
```

> PowerShell 환경변수는 현재 Terminal 세션에 적용됩니다. 새 Terminal을 열면 다시 설정할 수 있습니다.

## STEP 5. Runtime Validator 실행

먼저 최소 Runtime Gate를 확인합니다.

```powershell
python scripts/runtime_validate.py
```

Chapter 04용 Embedding Model까지 준비되어 있다면 Models / Chat / Embedding 세 Gate가 모두 PASS할 수 있습니다.

Chapter 03의 핵심 확인은 다음입니다.

```text
/v1/models 응답
Chat Completion 응답
```

## STEP 6. Starter 실행

저장소 루트에서 실행합니다.

```powershell
python chapter03\starter\app.py
```

정상 결과:

```text
Python
→ localhost:1234/v1
→ Local Model
→ Response
```

## 핵심 코드

[`starter/app.py`](./starter/app.py)는 다음 구조를 사용합니다.

```python
client = OpenAI(
    base_url=BASE_URL,
    api_key="lm-studio",
)
```

그리고 실제 모델은 코드에 하드코딩하지 않고:

```python
MODEL_ID = os.getenv("CHAT_MODEL_ID", "").strip()
```

로 읽습니다.

이번 장에서 가장 중요한 것은 `base_url`과 Model ID의 출처입니다.

```text
Public API
→ 외부 Provider Endpoint

Local API
→ localhost Endpoint

Model ID
→ /v1/models 실제 응답
```

## 실패 실습 1. Server Stop

LM Studio Server를 중지한 뒤 다시 실행합니다.

```powershell
python chapter03\starter\app.py
```

예상:

```text
Connection Error
```

다시 LM Studio Local Server를 `Running`으로 되돌린 후 정상 실행되는지 재검증합니다.

## 실패 실습 2. Wrong Model ID

현재 값을 먼저 확인합니다.

```powershell
$env:CHAT_MODEL_ID
```

존재하지 않는 Model ID를 임시로 설정합니다.

```powershell
$env:CHAT_MODEL_ID="not-a-real-model"
python chapter03\starter\app.py
```

예상:

```text
Model 관련 오류
```

실습 후 실제 ID로 복원합니다.

```powershell
$env:CHAT_MODEL_ID="qwen/qwen3-4b-2507"
```

따라서:

```text
Server 연결 실패
≠
Model 선택 실패
```

## Evidence

```text
Local Server Running
TcpTestSucceeded : True
/v1/models 응답
실제 Chat Model ID
runtime_validate.py Chat PASS
chapter03/starter/app.py 실행 결과
Server Stop 오류
Wrong Model ID 오류
```

## 혼자 해보기

업무 문장을 세 줄로 요약하는 Prompt로 변경합니다.

입력 예:

```text
오늘 고객 문의 중 배송 지연 관련 문의가 증가했고,
원인은 물류센터 시스템 점검으로 확인되었습니다.
내일 오전까지 정상화 예정입니다.
```

## 완료 기준

```text
[ ] Local Server를 시작했다.
[ ] Port 1234 연결을 확인했다.
[ ] /v1/models를 확인했다.
[ ] 실제 Chat Model ID를 환경변수로 설정했다.
[ ] Python에서 Local LLM을 호출했다.
[ ] Server Stop 오류를 확인했다.
[ ] Wrong Model ID 오류를 확인했다.
[ ] Application과 Model Runtime을 구분할 수 있다.
```

## 다음 강의

Chapter 04에서는 Local LLM 앞에 **문서 검색(Retrieval)** 단계를 추가합니다.
