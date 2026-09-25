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

## STEP 1. 패키지 설치

루트에서 가상환경을 활성화한 뒤:

```powershell
pip install -r requirements.txt
```

## STEP 2. Model ID 설정

`starter/rag.py`의 다음 값을 실제 LM Studio 환경에 맞게 변경합니다.

```text
CHAT_MODEL_ID
EMBEDDING_MODEL_ID
```

## STEP 3. Streamlit 실행

```powershell
streamlit run chapter05\starter\app.py
```

정상적으로 실행되면 Browser에서 질문 입력 UI가 열립니다.

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

## 정상 질문 예

```text
부산 출장 숙박비 한도는 얼마인가요?
```

확인할 것:

```text
답변
Source
Retrieved Chunk
Similarity Score
```

## Negative Test

```text
제주도 렌터카 지원 한도는 얼마인가요?
```

문서에 근거가 없으면 이를 명확히 알려야 합니다.

## Failure Test

LM Studio Local Server를 중지한 뒤 같은 질문을 실행합니다.

기대 결과:

```text
Application이 비정상 종료되는 대신
사용자에게 Error 상태를 표시
```

## Evidence

```text
Streamlit UI
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
[ ] UI와 RAG 책임을 구분할 수 있다.
```

## 다음 강의

Chapter 06에서는 이 Prototype을 실제 기업 환경에 적용하려면 무엇이 더 필요한지 검토합니다.
