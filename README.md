# Private LLM for AX Course

> AX 실무자를 위한 Private LLM 실습 과정 — Student Edition

이 저장소는 교육생이 **Private LLM의 개념을 이해하고, Local LLM을 직접 실행하며, 사내 문서 기반 RAG와 간단한 업무용 AI Assistant까지 구현**하기 위한 공개 실습 저장소입니다.

강의는 단순히 코드를 따라 입력하는 방식이 아니라 다음 흐름으로 진행합니다.

```text
개념 / 구조
→ 강사 Demo
→ 학생 직접 실습
→ Evidence 확인
→ 혼자 해보기
→ Commit / Push
```

## 전체 과정

1. [Chapter 01. Private LLM 이해와 도입 판단](./chapter01/README.md)
2. [Chapter 02. Local LLM 직접 실행](./chapter02/README.md)
3. [Chapter 03. Local LLM API 활용](./chapter03/README.md)
4. [Chapter 04. RAG와 사내 문서 연결](./chapter04/README.md)
5. [Chapter 05. Private AI 업무 서비스 구축](./chapter05/README.md)
6. [Chapter 06. 기업 적용과 운영 전략](./chapter06/README.md)

상세 과정 개요는 [overview.md](./overview.md)를 참고하세요.

## 최종 결과물

과정 전체에서 하나의 프로젝트를 단계적으로 확장합니다.

```text
Local LLM
→ Local API
→ RAG
→ Vector Search
→ Local LLM
→ Streamlit UI
→ Private AI Assistant
→ Enterprise 적용 판단
```

최종 프로젝트 예시는 **사내 규정 Private AI Assistant**입니다.

## 기본 환경

- Windows 10/11 기준
- VS Code
- Python 3.11~3.13 권장
- Git / GitHub
- LM Studio
- Streamlit

실제 모델과 LM Studio 화면은 버전에 따라 달라질 수 있습니다. 강의에서는 특정 모델 이름을 외우기보다 **Model / Runtime / API / RAG / Evidence의 구조**를 이해하는 것을 우선합니다.

## 시작 방법

### 1. 이 저장소 Fork

GitHub에서 `Fork`를 눌러 자신의 계정으로 복사합니다.

### 2. Clone

```powershell
git clone https://github.com/<YOUR_GITHUB_ID>/private-llm-for-ax-course.git
cd private-llm-for-ax-course
```

### 3. VS Code에서 열기

```powershell
code .
```

### 4. Python 가상환경

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Chapter 순서대로 진행

각 Chapter의 `README.md`에는 다음이 포함됩니다.

```text
무엇을 배우는가?
왜 필요한가?
실습 순서
정상 결과
Evidence
혼자 해보기
```

## Runtime Validation

Chapter 02 이후에는 다음 문서를 기준으로 실제 실행 환경을 검증합니다.

- [Runtime Validation Guide](./docs/RUNTIME_VALIDATION_GUIDE.md)

LM Studio Local Server를 시작한 뒤 먼저 실행합니다.

```powershell
python scripts/runtime_preflight.py
```

정상적으로 `/v1/models`가 확인되면 실제 출력된 Model ID를 사용합니다.

PowerShell 예:

```powershell
$env:CHAT_MODEL_ID="실제-chat-model-id"
$env:EMBEDDING_MODEL_ID="실제-embedding-model-id"
python scripts/runtime_validate.py
```

검증 순서:

```text
LM Studio Server
→ /v1/models
→ Chat Completion
→ Embedding
→ RAG
→ Streamlit
```

## AI 활용 원칙

이 과정은 ChatGPT, Claude, Gemini 등 LLM 사용을 제한하지 않습니다.

다만 다음 방식으로 사용합니다.

```text
전체 코드 만들어줘              X

현재 단계의 문제를 설명해줘       O
오류 원인을 확인할 순서를 알려줘   O
이 코드가 무슨 역할인지 설명해줘   O
테스트할 Case를 제안해줘           O
```

핵심 원칙:

> **AI가 구현을 도울 수 있지만, 왜 필요한지와 정상적으로 동작한다는 근거는 학생이 설명할 수 있어야 합니다.**

## Evidence 원칙

실습 완료는 단순히 화면이 보이는 것으로 판단하지 않습니다.

```text
실행 결과
+ Retrieval 결과
+ Source
+ 오류/실패 Case
+ Git History
```

처럼 단계에 맞는 Evidence를 확인합니다.

## 주의

- 실제 회사의 민감 문서를 이 Public 저장소에 올리지 마세요.
- API Key, Password, Token 등 Secret을 Commit하지 마세요.
- 실습용 데이터는 `data/sample/`의 공개용 샘플만 사용합니다.
- Local Server를 다른 PC에서 접근 가능하게 열 경우 인증, 방화벽, 접근 범위를 반드시 검토하세요.
