# Private LLM Mini AX Proposal

## 1. 업무 문제

- 현재 어떤 업무 문제가 있는가?
- 누가 이 문제를 겪고 있는가?

## 2. 사용자

- 주요 사용자:
- 예상 사용자 수:
- 예상 질문/요청량:

## 3. 데이터

- 사용할 데이터/문서:
- 데이터 민감도:
- 개인정보 포함 여부:
- 외부 전송 가능 여부:

## 4. 현재 업무 방식

```text
현재 사용자가 문제를 해결하는 흐름을 작성합니다.
```

## 5. 제안 Data Flow / Architecture

```text
User
→ Application
→ Retrieval / RAG
→ Model
→ Answer
```

필요한 요소를 추가합니다.

```text
Authentication
Authorization
Vector Store
Logging
Monitoring
External API
```

## 6. 도입 방식 선택

- [ ] Public LLM
- [ ] Private LLM
- [ ] Hybrid

### 선택 이유

1. 
2. 
3. 

## 7. RAG 필요 여부

- [ ] 필요
- [ ] 불필요

이유:

## 8. 문서 권한

- 누가 어떤 문서를 볼 수 있는가?
- Retrieval 전에 어떤 권한 확인이 필요한가?

## 9. Security / Privacy

다음 항목을 확인합니다.

```text
Prompt 저장 여부
Response 저장 여부
Log 보존 기간
민감정보 포함 가능성
외부 API 호출 여부
Embedding 위치
Vector Store 위치
Model 실행 위치
```

## 10. 운영 방식

- Model Runtime / Serving:
- 운영 담당자:
- Backup:
- 장애 대응:
- Model Update:
- Document Update / Re-index:

## 11. Monitoring / Evidence

확인할 지표:

```text
응답시간
오류율
Retrieval 성공률
근거 없는 답변 비율
사용량
GPU / Memory 사용률
```

## 12. 비용 / TCO

예상 비용 요소:

| 항목 | 내용 |
|---|---|
| GPU / Server |  |
| 전력 |  |
| Storage |  |
| Network |  |
| Backup |  |
| Monitoring |  |
| Software / License |  |
| 운영 인력 |  |
| 기타 |  |

## 13. 기대 효과

1. 
2. 
3. 

## 14. 주요 Risk

1. 
2. 
3. 

## 15. Pilot 제안

- Pilot 사용자:
- 기간:
- 대상 문서:
- 범위:

### KPI

```text
예: 평균 문서 검색 시간 감소
예: 근거 있는 답변 비율
예: 사용자 만족도
예: 평균 응답시간
```

## 16. 최종 판단

```text
왜 이 방식으로 시작해야 하는가?
무엇을 먼저 검증해야 하는가?
어떤 조건이면 확대/중단할 것인가?
```
