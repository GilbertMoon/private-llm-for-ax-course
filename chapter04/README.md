# Chapter 04. RAG와 사내 문서 연결

## 이번 강의에서 할 일

Local LLM이 회사 문서를 자동으로 알고 있는 것은 아닙니다.

이번 강의에서는 질문과 관련된 문서를 먼저 찾고, 그 근거를 Local LLM에 전달합니다.

```text
Document
→ Chunk
→ Embedding
→ Similarity Search
→ Retrieved Context
→ Local LLM
→ Answer + Source
```

## 학습 목표

- RAG와 Fine-tuning을 구분한다.
- Chunk, Embedding, Vector, Similarity Search를 설명한다.
- Chat Model과 Embedding Model 역할을 구분한다.
- Retrieval 결과를 답변보다 먼저 검증한다.
- Source를 표시한다.
- 문서에 없는 질문에서 추측을 억제한다.

## 핵심 원칙

```text
Retrieval
= 어떤 근거를 가져올 것인가?

Generation
= 그 근거를 바탕으로 어떻게 답할 것인가?
```

## 실습 데이터

공개용 샘플 문서를 사용합니다.

[`../data/sample/company_policy.txt`](../data/sample/company_policy.txt)

실제 회사의 민감 문서는 Public GitHub에 올리지 않습니다.

## STEP 1. Chapter 03 상태 확인

```powershell
Invoke-RestMethod http://localhost:1234/v1/models
```

Chat Model과 Embedding Model이 준비되어 있는지 확인합니다.

## STEP 2. Embedding Model 준비

LM Studio에서 Embedding Model을 사용할 수 있도록 준비합니다.

```text
Chat Model
→ 답변 생성

Embedding Model
→ Text → Vector
```

## STEP 3. Starter 코드 확인

[`starter/rag.py`](./starter/rag.py)를 엽니다.

다음 값을 실제 환경에 맞게 바꿉니다.

```text
CHAT_MODEL_ID
EMBEDDING_MODEL_ID
```

## STEP 4. 실행

```powershell
python starter\rag.py
```

## 먼저 확인할 것

LLM 답변보다 Retrieval 결과를 먼저 봅니다.

```text
Question
→ Retrieved Chunk
→ Similarity Score
→ Source
→ 그 다음 Answer
```

## 정상 질문 예

```text
부산 출장 숙박비 한도는 얼마인가요?
```

샘플 문서 기준 기대 근거:

```text
지방: 1박 최대 100,000원
```

## Negative Test

```text
제주도 렌터카 지원 한도는 얼마인가요?
```

샘플 문서에 근거가 없다면 기대 답변은 다음과 같은 형태입니다.

```text
제공된 문서에서 확인할 수 없습니다.
```

## RAG / Answer Contract

```text
1. 관련 Chunk를 먼저 검색한다.
2. 검색된 Context 안의 정보만 사용한다.
3. 근거가 없으면 모른다고 답한다.
4. Source를 표시한다.
5. Retrieval 결과를 직접 확인할 수 있어야 한다.
```

## Evidence

```text
원문
Chunk
Embedding 생성
Top-k Retrieval
Similarity Score
Prompt Context
Answer
Source
Negative Test
```

## 혼자 해보기

샘플 문서의 다른 규정을 질문합니다.

예:

```text
사내 비밀번호를 분실하면 어떻게 해야 하나요?
반차는 어떤 형태로 사용할 수 있나요?
```

그리고 실제로 검색된 Chunk가 정답 근거인지 확인합니다.

## 완료 기준

```text
[ ] 문서를 Chunk로 나눴다.
[ ] Local Embedding을 생성했다.
[ ] 질문 Embedding을 생성했다.
[ ] Similarity Search를 실행했다.
[ ] Retrieved Chunk를 직접 확인했다.
[ ] Local LLM 답변을 생성했다.
[ ] Source를 확인했다.
[ ] 문서에 없는 질문을 테스트했다.
```

## 다음 강의

Chapter 05에서는 Terminal 기반 RAG에 **Streamlit UI**를 추가합니다.
