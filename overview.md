# Private LLM for AX — 학생용 전체 과정 개요

이 과정은 생성형 AI를 업무에 활용하는 실무자가 **Private LLM을 이해하고, Local LLM 실행부터 RAG 기반 업무 서비스 구성까지 직접 경험**하도록 설계되었습니다.

## 이 과정에서 답해야 할 질문

```text
왜 Private LLM이 필요한가?
어떤 데이터가 어디로 이동하는가?
Local과 Private는 무엇이 다른가?
모델은 어디에서 실행되는가?
사내 문서는 어떻게 연결하는가?
답변의 근거를 어떻게 확인하는가?
비용과 운영 부담은 어떻게 판단하는가?
우리 업무에 Public / Private / Hybrid 중 무엇이 맞는가?
```

## 전체 학습 흐름

```text
Chapter 01
Private LLM 이해와 도입 판단
        ↓
Chapter 02
Local LLM 실행
        ↓
Chapter 03
Python에서 Local LLM API 호출
        ↓
Chapter 04
RAG로 사내 문서 연결
        ↓
Chapter 05
Private AI Assistant 구축
        ↓
Chapter 06
기업 적용과 운영 판단
```

## Chapter별 결과물

| Chapter | 핵심 주제 | 결과물 |
|---|---|---|
| 01 | Public / Private / Hybrid 판단 | 업무 적용 후보 + Data Flow + 판단표 |
| 02 | Local LLM 실행 | Local Model 실행 Evidence |
| 03 | Local API 호출 | Python → Local LLM API |
| 04 | RAG | 문서 검색 + Answer + Source |
| 05 | 업무 서비스 | Streamlit Private AI Assistant |
| 06 | 기업 적용 | Private LLM Mini AX Proposal |

## 과정 전체의 공통 원칙

### 1. 코드를 먼저 보지 않습니다

```text
문제
→ 구조
→ 완료 기준
→ Evidence
→ 구현
→ 실행
→ 검증
```

### 2. 모든 주요 STEP에서 확인합니다

```text
무엇을 하는가?
왜 하는가?
정상 결과는 무엇인가?
데이터는 어디로 이동하는가?
어떤 Evidence로 확인하는가?
```

### 3. Local = Private가 아닙니다

Local은 실행 위치에 대한 표현입니다.

Private 여부는 다음 전체 흐름을 확인해야 합니다.

```text
Prompt
Document
Embedding
Vector Store
LLM
Log
Monitoring
Telemetry
External API
```

### 4. RAG에서는 답변보다 근거를 먼저 봅니다

```text
Question
→ Retrieved Chunk
→ Similarity / Source
→ Context
→ Answer
```

### 5. 모르는 질문에 답하지 않는 것도 기능입니다

문서에 근거가 없는 경우에는 추측하지 않고 다음과 같이 처리합니다.

```text
제공된 문서에서 확인할 수 없습니다.
```

### 6. Private LLM은 공짜가 아닙니다

자체 모델 실행 시 Public API처럼 토큰당 별도 과금이 없을 수 있지만 다음 비용이 발생합니다.

```text
GPU / Server
전력
Storage
Network
Backup
Security
Monitoring
Model / RAG 유지보수
운영 인력
```

즉 비용은 TCO(Total Cost of Ownership) 관점으로 판단합니다.

## 최종 프로젝트

과정 전체에서 다음 프로젝트를 단계적으로 완성합니다.

```text
회사 규정 문서
   ↓
Chunk
   ↓
Embedding
   ↓
Similarity Search
   ↓
Retrieved Context
   ↓
Local LLM
   ↓
Streamlit UI
   ↓
Answer + Source
```

실제 회사 문서 대신 공개 가능한 교육용 문서를 사용합니다.

## GitHub 학습 방식

각 Chapter가 끝나면 다음 흐름을 권장합니다.

```text
Task
→ 실행
→ Evidence 확인
→ git status
→ git add .
→ git commit
→ git push
```

GitHub는 단순 코드 보관소가 아니라 **학습 과정과 검증 결과를 남기는 Evidence**로 사용합니다.
