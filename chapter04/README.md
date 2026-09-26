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

## STEP 1. LM Studio 상태 확인

LM Studio Local Server가 `Running`인지 확인합니다.

PowerShell:

```powershell
Test-NetConnection localhost -Port 1234
```

정상 목표:

```text
TcpTestSucceeded : True
```

실제 Model ID 확인:

```powershell
(Invoke-RestMethod http://localhost:1234/v1/models).data.id
```

2026-09-26 실제 검증 예:

```text
qwen/qwen3-4b-2507
text-embedding-nomic-embed-text-v1.5
```

## STEP 2. Chat / Embedding Model 환경변수 설정

Starter 코드를 직접 수정하지 않습니다.

PowerShell에서 실제 `/v1/models` 응답을 기준으로 설정합니다.

실제 검증 예:

```powershell
$env:CHAT_MODEL_ID="qwen/qwen3-4b-2507"
$env:EMBEDDING_MODEL_ID="text-embedding-nomic-embed-text-v1.5"
$env:LM_STUDIO_BASE_URL="http://localhost:1234/v1"
```

현재 값 확인:

```powershell
$env:CHAT_MODEL_ID
$env:EMBEDDING_MODEL_ID
```

## STEP 3. Runtime Gate 확인

```powershell
python scripts/runtime_preflight.py
python scripts/runtime_validate.py
```

실제 검증 기준 정상 결과:

```text
Gate 1. Models Endpoint   PASS
Gate 2. Chat Completion   PASS
Gate 3. Embedding         PASS
```

Embedding이 정상이라면 Vector dimension도 출력됩니다.

2026-09-26 실제 Nomic Embedding 검증에서는:

```text
dimension: 768
```

을 확인했습니다.

## STEP 4. Starter 코드 확인

[`starter/rag.py`](./starter/rag.py)를 엽니다.

데이터 흐름을 확인합니다.

```text
company_policy.txt
→ Chunk
→ Document Embedding

Question
→ Query Embedding
→ Cosine Similarity
→ Top-k Retrieval
→ Context
→ Chat Model
→ Answer
```

### Nomic Embedding 사용 시 중요한 점

현재 검증된 `text-embedding-nomic-embed-text-v1.5`는 검색 목적에 맞게 task prefix를 구분합니다.

```text
문서: search_document: ...
질문: search_query: ...
```

Starter 코드는 Nomic 모델 ID를 사용하는 경우 이 prefix를 자동 적용합니다.

이 구분이 없으면 관련 없는 Chunk가 높은 점수를 받을 수 있으므로, **Embedding이 생성된다는 사실만으로 Retrieval 품질이 보장되지는 않습니다.**

## STEP 5. RAG 실행

저장소 루트에서 실행합니다.

```powershell
python chapter04\starter\rag.py
```

## STEP 6. Retrieval을 먼저 확인

LLM 답변보다 Retrieval 결과를 먼저 봅니다.

```text
Question
→ Retrieved Chunk
→ Similarity Score
→ Source
→ 그 다음 Answer
```

Positive Test:

```text
지방 출장 숙박비 한도는 얼마인가요?
```

샘플 문서 기준 정답 근거:

```text
1. 국내 출장 숙박비
- 서울: 1박 최대 120,000원
- 지방: 1박 최대 100,000원
```

2026-09-26 실제 검증에서는 정답 Chunk가 Top-k에 포함되었고 다음 답변을 확인했습니다.

```text
1박 최대 100,000원
```

> 정답 Chunk가 반드시 Top-1이어야 하는 것은 아니지만, 현재 교육용 Gate에서는 Top-k에 정답 근거가 포함되고 최종 답변이 그 근거와 일치하는지 확인합니다.

## STEP 7. Negative Test

다시 실행합니다.

```powershell
python chapter04\starter\rag.py
```

문서에 없는 질문 예:

```text
해외 출장 시 항공권은 비즈니스석으로 이용할 수 있나요?
```

샘플 문서에 근거가 없으므로 기대 답변:

```text
제공된 문서에서 확인할 수 없습니다.
```

중요:

```text
관련 없는 Chunk가 Top-k에 검색될 수 있음
        ↓
그래도 Context에 답이 없다면
        ↓
추측하지 않고 No Evidence 응답
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
Vector Dimension
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
[ ] LM Studio Local Server가 Running이다.
[ ] 실제 Chat / Embedding Model ID를 환경변수로 설정했다.
[ ] Embedding Runtime Gate를 통과했다.
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
