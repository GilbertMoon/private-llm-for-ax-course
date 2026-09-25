# Runtime Validation Guide

기준일: 2026-09-25

이 문서는 Chapter 02~05 실습을 실제 Windows + LM Studio 환경에서 검증하기 위한 기준입니다.

## 1. 수업용 기본 환경

권장 기준:

```text
OS: Windows 10/11
RAM: 16GB 이상 권장
GPU: 전용 VRAM 4GB 이상 권장
Python: 3.11~3.13 권장
LM Studio: 수업 직전 최신 안정 버전 확인
Local API: http://localhost:1234/v1
```

학생 PC 사양은 서로 다를 수 있으므로 모델 이름보다 **현재 PC에서 안정적으로 실행 가능한 크기**를 우선합니다.

---

## 2. Chat Model 기준

### 기본 수업 후보

```text
Qwen3-4B-Instruct-2507
Quantization: Q4_K_M
```

목적:

- 16GB RAM 수준의 일반 교육용 PC에서 부담을 낮춘다.
- 한국어 질의와 기본 업무 문서 Q&A를 실습한다.
- Chapter 02~05의 구조 학습에 집중한다.

### 여유 있는 PC 선택 후보

```text
Qwen3-8B
Quantization: Q4_K_M
```

8B 모델은 4B보다 메모리 사용량이 커질 수 있으므로 모든 학생의 공통 기본값으로 강제하지 않는다.

> 모델은 수업 직전 LM Studio의 Device Fit과 실제 학생 PC에서 다시 확인한다.

---

## 3. Embedding Model 기준

한국어 문서 Retrieval 실습의 우선 후보:

```text
BGE-m3-ko
Quantization: Q8_0
```

대체 후보:

```text
BGE-M3 계열 GGUF
```

Embedding Model은 Chat Model과 역할이 다르다.

```text
Chat Model
→ 답변 생성

Embedding Model
→ Text를 Vector로 변환
```

---

## 4. Model ID는 직접 확인한다

강의 코드에 인터넷에서 본 Model ID를 그대로 입력하지 않는다.

LM Studio Server를 실행한 뒤 다음으로 실제 ID를 확인한다.

```powershell
Invoke-RestMethod http://localhost:1234/v1/models
```

또는 제공된 Preflight Script를 사용한다.

```powershell
python scripts/runtime_preflight.py
```

정상 결과:

```text
LM Studio server: PASS
Available models:
- ...
```

실제 출력된 ID를 Chapter 코드의 `MODEL_ID`, `CHAT_MODEL_ID`, `EMBEDDING_MODEL_ID`에 사용한다.

---

## 5. Chapter별 Release Gate

### Chapter 02 — Local Runtime

```text
[ ] LM Studio 설치
[ ] Chat Model 다운로드
[ ] Model Load 성공
[ ] 한국어 Prompt 응답
[ ] CPU/RAM 또는 GPU 사용 확인
[ ] Model / Runtime 차이 설명 가능
```

### Chapter 03 — Local API

```text
[ ] LM Studio Local Server Running
[ ] /v1/models 응답
[ ] Python OpenAI Client 연결
[ ] 한국어 Chat Completion 성공
[ ] Server Stop 시 Connection Error 재현
[ ] Wrong Model ID 오류 재현
```

### Chapter 04 — RAG

```text
[ ] Embedding Model 사용 가능
[ ] /v1/embeddings 호출 성공
[ ] Sample Document Chunk 생성
[ ] Chunk Embedding 생성
[ ] Question Embedding 생성
[ ] Top-k Retrieval 확인
[ ] 정답 관련 Chunk 검색
[ ] Answer + Source 확인
[ ] 문서에 없는 질문 Negative Test
```

### Chapter 05 — Streamlit

```text
[ ] streamlit run 실행
[ ] 질문 입력
[ ] Loading 상태
[ ] Answer 표시
[ ] Source / Retrieval Evidence 표시
[ ] No Evidence 상태
[ ] LM Studio Stop 시 Error 상태
```

---

## 6. 권장 Runtime Validation 순서

```text
Gate 1. PC / Python 확인
        ↓
Gate 2. LM Studio Server 확인
        ↓
Gate 3. /v1/models 확인
        ↓
Gate 4. Chat Completion
        ↓
Gate 5. Embedding
        ↓
Gate 6. RAG Retrieval
        ↓
Gate 7. Grounded Answer
        ↓
Gate 8. Streamlit UI
        ↓
Gate 9. Failure Cases
```

앞 Gate가 실패하면 다음 단계로 넘어가지 않는다.

---

## 7. 수업 직전 반드시 다시 확인할 항목

Local AI 도구와 모델은 빠르게 변한다.

수업 직전에는 다음을 다시 확인한다.

```text
[ ] LM Studio 설치 화면과 메뉴
[ ] Local Server 시작 방법
[ ] 기본 Port
[ ] OpenAI-compatible Endpoint
[ ] 추천 Chat Model 존재 여부
[ ] 추천 Embedding Model 존재 여부
[ ] 학생 PC Device Fit
[ ] Python Package 설치 호환성
```

강의 목표는 특정 제품 메뉴를 암기하는 것이 아니라 다음 구조를 이해하는 것이다.

```text
Application
→ Local API
→ Runtime
→ Model
→ Retrieval
→ Evidence
```
