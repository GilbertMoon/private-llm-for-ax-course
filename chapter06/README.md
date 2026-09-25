# Chapter 06. 기업 적용과 운영 전략

## 이번 강의에서 할 일

Chapter 05에서는 개인 PC에서 동작하는 Private AI Assistant Prototype을 만들었습니다.

이번 강의에서는 이 시스템을 실제 회사에서 운영하려면 무엇이 더 필요한지 검토합니다.

```text
Prototype
→ Multi-user Service
→ Security / Authorization
→ Model Serving
→ Monitoring
→ Backup
→ TCO
→ Public / Private / Hybrid Decision
```

## 학습 목표

- 개인 Local LLM과 기업 Private LLM의 차이를 설명한다.
- 동시 사용자와 Capacity Planning의 필요성을 설명한다.
- Authentication과 Authorization을 구분한다.
- 문서 권한이 Retrieval 전에 적용되어야 하는 이유를 설명한다.
- Logging / Monitoring / Backup / Update의 운영 필요성을 설명한다.
- Public / Private / Hybrid를 업무별로 판단한다.
- Mini AX Proposal을 작성한다.

## Prototype과 Enterprise Service 비교

```text
개인 실습
나 → Streamlit → RAG → Local LLM
```

실제 조직에서는 다음 요소가 추가될 수 있습니다.

```text
직원
→ Authentication
→ Application
→ Authorization
→ RAG
→ Vector Store
→ Model Serving
→ GPU Server
→ Logging / Monitoring / Backup
```

## Authentication vs Authorization

```text
Authentication
= 누구인가?

Authorization
= 무엇을 볼 수 있는가?
```

RAG에서 중요한 원칙:

> 권한이 없는 문서를 먼저 검색한 뒤 답변에서 숨기는 것이 아니라, **Retrieval 전에 문서 권한을 적용**해야 합니다.

## 운영에서 추가되는 질문

```text
동시에 몇 명이 사용할까?
평균 질문량은 얼마인가?
응답시간 목표는 얼마인가?
GPU 한 대로 충분한가?
모델 장애 시 어떻게 복구하는가?
누가 Model/Document를 업데이트하는가?
Prompt/Response Log를 얼마나 보관하는가?
민감정보가 Log에 남지 않는가?
Backup은 있는가?
```

## 비용 / TCO

```text
Private LLM TCO
= GPU / Server
+ 전력
+ Storage
+ Network
+ Backup
+ Monitoring
+ Security
+ Software / License
+ Model 유지보수
+ RAG 유지보수
+ 운영 인력
```

중요:

```text
Token Fee가 없다
≠
Inference Cost가 0이다
```

## Public / Private / Hybrid 판단

### Public이 유리할 수 있는 경우

- 민감도가 낮은 일반 업무
- 사용량이 적음
- 최신 최고성능 모델이 중요함
- 내부 운영 인력이 부족함

### Private가 유리할 수 있는 경우

- 외부 전송이 제한되는 데이터
- 폐쇄망 / 내부망 요구
- 반복적인 내부 문서 질의
- 내부 운영 역량이 있음

### Hybrid가 유리할 수 있는 경우

```text
일반 보고서 작성 → Public
민감 내부 문서 검색 → Private
외부 공개자료 요약 → Public
내부 계약서 분석 → Private
```

## 최종 실습 — Mini AX Proposal

[`MINI_AX_PROPOSAL_TEMPLATE.md`](./MINI_AX_PROPOSAL_TEMPLATE.md)를 복사하여 자신의 업무 주제로 작성합니다.

## Proposal에서 반드시 설명할 것

```text
업무 문제
사용자
데이터와 민감도
Data Flow
Public / Private / Hybrid 선택
RAG 필요 여부
문서 권한
Security / Privacy
운영 방식
Evidence / Monitoring
비용 / TCO
Risk
Pilot 범위
KPI
```

## Evidence

이번 Chapter의 Evidence는 실행 화면이 아니라 **의사결정 근거가 포함된 Proposal**입니다.

## 완료 기준

```text
[ ] Prototype과 Enterprise Service 차이를 설명할 수 있다.
[ ] Authentication / Authorization을 구분할 수 있다.
[ ] Retrieval 전 권한 적용 이유를 설명할 수 있다.
[ ] 운영 비용을 TCO로 설명할 수 있다.
[ ] Public / Private / Hybrid를 선택했다.
[ ] 선택 이유를 설명할 수 있다.
[ ] Pilot 범위와 KPI를 제안했다.
[ ] Mini AX Proposal을 완성했다.
```

## 과정 마무리

이 과정의 최종 목표는 특정 Local LLM 도구를 외우는 것이 아닙니다.

> **AI가 구현을 도울 수 있지만, 데이터 흐름·보안 경계·비용·정상 동작의 근거와 도입 판단은 내가 설명할 수 있어야 합니다.**
