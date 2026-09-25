# Chapter 01. Private LLM 이해와 도입 판단

## 이번 강의에서 할 일

이번 강의에서는 아직 모델을 설치하지 않습니다. 먼저 **왜 Private LLM이 필요한지, 우리 업무에 정말 적합한지 판단하는 기준**을 만듭니다.

## 학습 목표

- Public LLM, Local LLM, Private LLM의 차이를 설명한다.
- `Local = Private`가 아닌 이유를 설명한다.
- 업무 데이터의 이동 경로를 Data Flow로 그린다.
- 비용을 Token Fee가 아니라 TCO 관점에서 본다.
- Public / Private / Hybrid 중 적절한 후보를 선택한다.

## 핵심 판단 기준

```text
Data / Privacy
Cost / TCO
Performance
Operation
```

## 실습

### STEP 1. 업무 후보 하나 선택

예:

```text
출장규정 검색
사내 FAQ
제품 매뉴얼 Q&A
품질 SOP 검색
IT Helpdesk 문서 검색
```

### STEP 2. 데이터 분류

아래 질문에 답합니다.

```text
어떤 데이터가 필요한가?
공개 가능한가?
개인정보가 있는가?
회사 내부 정보인가?
외부 전송이 가능한가?
```

### STEP 3. Data Flow 작성

예:

```text
직원 질문
→ 사내 Application
→ RAG
→ Vector Store
→ LLM
→ 답변
```

필요하면 다음도 표시합니다.

```text
Embedding
Log
Monitoring
External API
```

### STEP 4. 도입 판단표 작성

| 항목 | 확인 내용 |
|---|---|
| 업무 | 어떤 문제를 해결하는가? |
| 사용자 | 누가 사용하는가? |
| 데이터 | 어떤 문서를 사용하는가? |
| 민감도 | 공개/내부/민감 데이터인가? |
| 외부 전송 | 가능한가? |
| 사용량 | 사용자와 질문량은 어느 정도인가? |
| 성능 | 어느 정도 품질이 필요한가? |
| 운영 | 누가 관리할 수 있는가? |
| 후보 | Public / Private / Hybrid |

## Evidence

이번 강의의 완료 Evidence는 다음 세 가지입니다.

```text
1. 업무 적용 후보
2. Data Flow
3. 도입 판단표
```

## 혼자 해보기

자신이 아는 업무 하나를 골라 아래를 작성합니다.

1. 업무 문제
2. 사용 데이터
3. Data Flow
4. Public / Private / Hybrid 판단
5. 판단 근거 3개

## 완료 기준

```text
[ ] 적용 업무를 하나 정했다.
[ ] 데이터 민감도를 설명할 수 있다.
[ ] Data Flow를 그렸다.
[ ] Local과 Private 차이를 설명할 수 있다.
[ ] Public / Private / Hybrid 중 하나를 선택했다.
[ ] 선택 이유를 설명할 수 있다.
```

## 다음 강의

Chapter 02에서는 실제로 **내 PC에서 Local LLM을 실행**합니다.
