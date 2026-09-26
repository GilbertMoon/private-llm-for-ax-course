# Runtime Validation Evidence — 2026-09-26

상태: **RUNTIME RELEASE / PASS**

이 문서는 `private-llm-for-ax-course`를 실제 Windows + LM Studio 환경에서 실행하여 확인한 Runtime Evidence입니다.

## 1. 실행 환경

```text
Date: 2026-09-26
OS: Microsoft Windows 11 Pro
Python: 3.12.10
LM Studio: 0.4.25
RAM: 31.43 GB
GPU: NVIDIA GeForce RTX 5060 Laptop GPU
VRAM: 8151 MB (nvidia-smi 기준)
Base URL: http://localhost:1234/v1
```

Windows CIM의 AdapterRAM 값은 NVIDIA 실제 VRAM과 다르게 보일 수 있으므로 NVIDIA GPU의 VRAM Evidence는 `nvidia-smi` 값을 우선했습니다.

## 2. 사용 모델

### Chat Model

```text
Model ID: qwen/qwen3-4b-2507
Model: Qwen3 4B Instruct 2507
Format: GGUF
Quantization: Q4_K_M
File Size: 약 2.50 GB
```

### Embedding Model

```text
Model ID: text-embedding-nomic-embed-text-v1.5
Vector Dimension: 768
```

Nomic Embedding을 Retrieval에 사용할 때 Starter는 task prefix를 구분합니다.

```text
Document: search_document: ...
Query:    search_query: ...
```

## 3. Gate 결과

```text
Gate 0A Offline Static CI                    PASS
Gate 0B OpenAI-compatible Mock Integration   PASS
Gate 1   실제 LM Studio /v1/models            PASS
Gate 2   실제 Chat Completion                 PASS
Gate 3   실제 Embedding                       PASS
Gate 4   실제 RAG Retrieval                   PASS
Gate 5   Grounded Answer                      PASS
Gate 6   Negative Test                        PASS
Gate 7   Streamlit                            PASS
Gate 8   Failure Case                         PASS
```

## 4. Gate 1 — Models Endpoint

실행:

```powershell
python scripts/runtime_preflight.py
```

실제 Model ID:

```text
qwen/qwen3-4b-2507
text-embedding-nomic-embed-text-v1.5
```

결과: **PASS**

## 5. Gate 2 — Chat Completion

실행:

```powershell
$env:CHAT_MODEL_ID="qwen/qwen3-4b-2507"
$env:EMBEDDING_MODEL_ID="text-embedding-nomic-embed-text-v1.5"
python scripts/runtime_validate.py
```

실제 결과:

```text
PASS: Chat Completion 응답 확인
로컬 LLM 런타임 검증 통과
```

결과: **PASS**

## 6. Gate 3 — Embedding

실제 결과:

```text
PASS: Embedding Vector 생성
dimension: 768
```

결과: **PASS**

## 7. Gate 4 — RAG Retrieval

실행:

```powershell
python chapter04/starter/rag.py
```

Positive Test:

```text
지방 출장 숙박비 한도는 얼마인가요?
```

실제 Retrieval Evidence:

```text
[score=0.7653] company_policy.txt / chunk 3
1. 국내 출장 숙박비
- 서울: 1박 최대 120,000원
- 지방: 1박 최대 100,000원
```

정답 Chunk가 Top-k 안에 포함됨을 확인했습니다.

결과: **PASS**

## 8. Gate 5 — Grounded Answer

위 Positive Test 실제 답변:

```text
1박 최대 100,000원
```

Retrieved Context의 근거와 일치합니다.

결과: **PASS**

## 9. Gate 6 — Negative Test

질문:

```text
해외 출장 시 항공권은 비즈니스석으로 이용할 수 있나요?
```

실제 답변:

```text
제공된 문서에서 확인할 수 없습니다.
```

문서에 없는 정보를 추측하지 않는 Grounding Contract를 확인했습니다.

결과: **PASS**

## 10. Gate 7 — Streamlit

실행:

```powershell
streamlit run chapter05/starter/app.py
```

확인 결과:

```text
localhost:8501 UI 정상 로드
질문 입력 정상
Retrieval Evidence / Source 표시
Grounded Answer 표시
```

Positive Test 답변:

```text
지방 출장 숙박비 한도는 1박 최대 100,000원입니다.
```

결과: **PASS**

## 11. Gate 8 — Failure Case

LM Studio Local Server를 `Stopped`로 바꾸고 Streamlit에서 다시 질문했습니다.

앱은 크래시하거나 무한 대기하지 않고 Error 상태를 표시했습니다.

이후 Starter의 연결 오류 안내도 다음처럼 개선했습니다.

```text
LM Studio Local Server에 연결할 수 없습니다.
LM Studio의 Developer > Local Server에서 서버가 Running 상태인지 확인해 주세요.
```

결과: **PASS**

## 12. RAM / VRAM Evidence

실행:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/windows_resource_evidence.ps1
```

모델이 Load된 상태의 실제 측정값:

```text
RAM Total: 31.43 GB
RAM Used : 22.51 GB
RAM Free : 8.92 GB

GPU: NVIDIA GeForce RTX 5060 Laptop GPU
VRAM Total: 8151 MB
VRAM Used : 4432 MB
VRAM Free : 3468 MB
GPU Utilization: 0%
```

`GPU Utilization: 0%`는 측정 순간 추론이 진행 중이지 않은 idle 시점의 값입니다. 모델이 Load된 상태에서 약 4.4 GB VRAM 점유가 확인되었습니다.

## 13. README / CI 재현성 최종 확인

Release 전 문서 검수에서 Chapter 03~05의 오래된 '코드에 Model ID 직접 입력' 설명을 실제 구현과 동일한 환경변수 방식으로 정리했습니다.

기준 실행 흐름:

```text
Clone / Fork
→ venv
→ requirements 설치
→ LM Studio 설치
→ Chat / Embedding Model 준비
→ Local Server Running
→ /v1/models
→ 환경변수 설정
→ runtime_preflight.py
→ runtime_validate.py
→ Chapter 03 API
→ Chapter 04 RAG
→ Chapter 05 Streamlit
→ Failure Test
```

최신 문서 수정 후 Public 저장소 `Course CI`도 PASS했습니다.

```text
Run ID: 36206747443
Head SHA: 31328d1e8f3da9b98e30582e29ff744e21d1103f
Conclusion: success
```

## 14. 최종 판정

```text
RUNTIME RELEASE / PASS
RELEASE READY
```

현재 검증 환경에서 수업용 기능 Runtime Gate, 문서 재현성, 자동 CI를 모두 통과했습니다.

낮은 사양의 별도 학생 PC 실측은 향후 호환성 범위 확대를 위한 추가 검증으로 관리하며, 현재 Release Ready 판정의 차단 조건으로 두지 않습니다.
