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

LM Studio에서 Local Server를 시작합니다.

기본 실습 주소 예:

```text
http://localhost:1234
```

## STEP 2. Model 목록 확인

PowerShell:

```powershell
Invoke-RestMethod http://localhost:1234/v1/models
```

정상 결과:

```text
현재 Server가 인식하는 Model 목록 반환
```

인터넷 예제의 Model 이름을 복사하지 말고 **여기서 확인한 실제 Model ID**를 사용합니다.

## STEP 3. Python 환경 준비

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r ..\requirements.txt
```

## STEP 4. Starter 코드 확인

[`starter/app.py`](./starter/app.py)를 엽니다.

`YOUR_MODEL_ID`를 STEP 2에서 확인한 값으로 바꿉니다.

## STEP 5. 실행

```powershell
python starter\app.py
```

정상 결과:

```text
Python
→ localhost:1234/v1
→ Local Model
→ Response
```

## 핵심 코드

```python
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
)
```

이번 장에서 가장 중요한 것은 `base_url`입니다.

```text
Public
→ 외부 Provider Endpoint

Local
→ localhost Endpoint
```

## 실패 실습 1. Server Stop

LM Studio Server를 중지한 뒤 다시 실행합니다.

예상:

```text
Connection Error
```

## 실패 실습 2. Wrong Model ID

존재하지 않는 Model ID로 변경합니다.

예상:

```text
Model 관련 오류
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
/v1/models 응답
실제 Model ID
python starter/app.py 실행 결과
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
[ ] /v1/models를 확인했다.
[ ] 실제 Model ID를 사용했다.
[ ] Python에서 Local LLM을 호출했다.
[ ] Server Stop 오류를 확인했다.
[ ] Wrong Model ID 오류를 확인했다.
[ ] Application과 Model Runtime을 구분할 수 있다.
```

## 다음 강의

Chapter 04에서는 Local LLM 앞에 **문서 검색(Retrieval)** 단계를 추가합니다.
