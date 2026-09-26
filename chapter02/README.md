# Chapter 02. Local LLM 직접 실행

> 기준 Runtime Lab: **Windows 11 / LM Studio 0.4.25**  
> 기준 확인일: **2026-09-26**

## 이번 강의에서 할 일

이번 강의에서는 **LM Studio를 이용해 Local LLM을 내 PC에서 직접 실행**합니다.

핵심 흐름:

```text
LM Studio 설치
→ Developer Mode 설정
→ Model Search
→ Model Download
→ Local Storage
→ Runtime Load
→ Prompt
→ Inference
→ Response
```

이번 Chapter의 목적은 LM Studio 버튼 위치를 외우는 것이 아닙니다.

다음 구조를 이해하는 것이 핵심입니다.

```text
Model
≠ Runtime
≠ Application
```

---

## 학습 목표

- Model과 Runtime의 차이를 설명한다.
- RAM / VRAM이 왜 필요한지 설명한다.
- Quantization의 목적을 설명한다.
- LM Studio를 설치하고 Developer Mode를 활성화한다.
- 수업용 Local Model을 검색하고 다운로드한다.
- Model을 Runtime에 Load한다.
- Local Model에 Prompt를 보내고 Response를 확인한다.
- 실행 Evidence를 남긴다.
- Chapter 03에서 사용할 Local Server의 역할을 미리 설명할 수 있다.

---

## 중요 개념

```text
Model
= 학습된 가중치/파라미터

Runtime
= Model을 메모리에 올리고 실행하는 소프트웨어

Application
= 사용자가 모델과 상호작용하는 프로그램
```

또 하나 반드시 구분합니다.

```text
Download
≠
Load
```

```text
Download
= Model File을 Disk에 저장

Load
= Runtime이 Model을 RAM / VRAM에 올림
```

---

# STEP 1. PC 환경 확인

Windows에서 작업 관리자를 열어 다음을 확인합니다.

```text
RAM
GPU
GPU Memory(VRAM)
Windows Version
```

작업 관리자:

```text
Ctrl + Shift + Esc
→ Performance
→ Memory
→ GPU
```

PowerShell 예:

```powershell
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM
```

기록:

```text
RAM: ______ GB
GPU: ______
VRAM: ______ GB
OS: Windows ______
```

---

# STEP 2. LM Studio 설치

공식 LM Studio 다운로드 페이지에서 Windows용 프로그램을 설치합니다.

현재 다운로드 화면에는 다음 두 제품이 함께 보일 수 있습니다.

```text
LM Studio Bionic
LM Studio
```

이번 수업에서 사용하는 것은 **LM Studio**입니다.

이유는 다음 기능을 직접 사용하기 때문입니다.

```text
Local Model Download
Local Runtime
Chat
Developer Mode
Local API Server
```

현재 확인된 실습 기준:

```text
LM Studio 0.4.25
Windows
x86
```

> UI와 버전은 바뀔 수 있으므로 실제 수업 시점에는 강사가 다시 확인합니다.

### 정상 결과

LM Studio가 설치되고 실행됩니다.

---

# STEP 3. 첫 실행 추천 모델은 건너뛰기

LM Studio를 처음 실행하면 `Your first model` 화면에서 추천 모델 다운로드를 제안할 수 있습니다.

이번 과정에서는 강사가 검증한 모델을 사용하므로:

```text
Skip for now
```

를 선택합니다.

### 왜 하나요?

첫 화면 추천 모델은 학생마다 다를 수 있고, 수업용 기준보다 큰 모델이 제안될 수 있기 때문입니다.

```text
추천 모델
≠
수업 검증 모델
```

---

# STEP 4. Developer Mode 설정

`Advanced settings` 화면이 나오면 다음처럼 설정합니다.

```text
Turn on Developer Mode              ON
Start local LLM service on login    ON 권장
```

그 다음:

```text
Continue to LM Studio
```

를 선택합니다.

### 왜 Developer Mode를 켜나요?

Chapter 03에서 다음 구조를 사용할 예정이기 때문입니다.

```text
Python Application
→ HTTP
→ localhost:1234
→ LM Studio Local Server
→ Local Model
```

Chapter 02에서는 먼저 Local Model 실행 자체에 집중합니다.

---

# STEP 5. 수업용 Local Model 검색

LM Studio 메인 화면에서 모델 검색 / Discover 화면으로 이동합니다.

검색어:

```text
Qwen3 4B Instruct
```

2026-09-26 실습 기준으로 확인된 기본 후보:

```text
Model ID      : qwen/qwen3-4b-2507
Parameter     : 4B
Format        : GGUF
Variant       : Qwen3 4B Instruct 2507
Quantization  : Q4_K_M
File Size     : 약 2.50 GB
```

### 왜 4B급을 사용하나요?

```text
학생 PC 사양 편차
다운로드 시간
RAM / VRAM 부담
수업 시간 내 실행 가능성
```

을 고려하기 때문입니다.

처음부터 가장 큰 모델을 고르는 것이 목표가 아닙니다.

---

# STEP 6. Quantization 확인

현재 실습 기본값은:

```text
Q4_K_M
```

입니다.

Quantization은 모델 Weight를 더 적은 비트로 표현해 메모리와 파일 크기 부담을 줄이는 방법입니다.

이번 Chapter에서는 세부 알고리즘보다 다음을 이해하면 충분합니다.

```text
Memory 부담 ↓
Local 실행 가능성 ↑
품질 손실 가능성 존재
```

핵심:

> Q4_K_M은 첫 Local LLM 실습에서 용량과 품질의 균형을 확인하기 위한 실용적인 선택지입니다.

---

# STEP 7. Model Download

현재 확인된 화면 기준:

```text
GGUF
Qwen3 4B Instruct 2507
Q4_K_M
약 2.50 GB
```

`Download`를 선택합니다.

다운로드 전에 다음 정보를 기록합니다.

```text
Model ID
Parameter Size
Format
Quantization
File Size
```

Evidence 예:

```text
Model ID      : qwen/qwen3-4b-2507
Parameter     : 4B
Format        : GGUF
Quantization  : Q4_K_M
File Size     : 약 2.50 GB
LM Studio     : 0.4.25
```

> 모델과 다운로드 크기는 수업 시점에 달라질 수 있습니다. 실제 화면 값을 우선합니다.

---

# STEP 8. Model Load

다운로드가 끝나면 모델을 Runtime에 Load합니다.

```text
Download
≠
Load
```

```text
Disk에 Model File 있음
        ≠
Memory에 Model Load됨
```

Load가 완료되면 RAM 또는 VRAM 사용량이 증가할 수 있습니다.

### 정상 결과

```text
Model Load 성공
Chat에서 모델 사용 가능
Task Manager에서 Memory / GPU 변화 확인 가능
```

---

# STEP 9. 첫 Prompt 실행

예:

```text
Private LLM과 Public LLM의 차이를
초보자에게 3문장으로 설명해 주세요.
```

이번 단계는 모델 성능 평가가 아니라 **Local Inference가 실제로 정상 동작하는지 확인**하는 실습입니다.

### 정상 결과

```text
Prompt 입력
→ Local Model Inference
→ Response 출력
```

응답이 나온 뒤 다음 질문에 답해 봅니다.

```text
어떤 Model이 응답했나요?
Model File은 어디에 있나요?
어떤 Runtime이 실행했나요?
어떤 Memory 자원을 사용했나요?
```

---

# STEP 10. Resource Evidence 확인

질문 전후의 RAM / GPU 사용량을 비교합니다.

```text
Task Manager
→ Performance
→ Memory
→ GPU
```

목표는 정확한 Benchmark가 아니라 다음 사실을 확인하는 것입니다.

> **Local LLM 추론은 내 PC의 실제 컴퓨팅 자원을 사용합니다.**

---

# STEP 11. Offline 의미 확인

이미 다운로드한 모델은 Local Runtime에서 실행할 수 있습니다.

```text
모델 다운로드
→ Internet 필요

이미 다운로드한 모델 실행
→ Local 실행 가능
```

하지만 다음은 반드시 구분합니다.

```text
Local Model 실행 가능
≠
전체 시스템이 자동으로 Private
```

Telemetry, Log, 외부 Embedding, 외부 API 등의 Data Flow는 별도로 확인해야 합니다.

---

# STEP 12. Chapter 03을 위한 Local Server 확인

Chapter 02 마지막에는 Chapter 03과 연결하기 위해 Local Server 개념을 확인합니다.

기본 구조:

```text
Python Application
→ HTTP
→ localhost:1234
→ LM Studio Local Server
→ Local Model
```

기본 Port:

```text
1234
```

PowerShell 확인:

```powershell
Test-NetConnection localhost -Port 1234
```

Server가 실행 중이면 목표:

```text
TcpTestSucceeded : True
```

Model 목록 확인:

```powershell
Invoke-RestMethod http://localhost:1234/v1/models
```

프로젝트 Runtime Preflight:

```powershell
python scripts/runtime_preflight.py
```

> Local API 호출 실습은 Chapter 03에서 본격적으로 진행합니다.

---

## 흔한 문제

### 1. `TcpTestSucceeded : False`

의미:

```text
localhost는 존재하지만
해당 Port에서 Server가 Listening하지 않음
```

확인 순서:

```text
1. LM Studio가 실행 중인가?
2. Developer Mode가 켜져 있는가?
3. Local Server가 실행 중인가?
4. 실제 Port가 1234인가?
```

코드를 먼저 수정하지 않습니다.

---

### 2. LM Studio가 설치되지 않음

PowerShell 예:

```powershell
Get-ChildItem "$env:LOCALAPPDATA\Programs" -Directory -ErrorAction SilentlyContinue |
Where-Object { $_.Name -match "LM Studio" }
```

실행 파일 검색 예:

```powershell
Get-ChildItem C:\ -Filter "LM Studio.exe" -Recurse -ErrorAction SilentlyContinue
```

아무 결과도 없다면 설치 여부부터 확인합니다.

---

### 3. Model이 너무 큼

증상:

```text
Load 실패
Memory 부족
매우 느린 응답
```

확인:

```text
Model Size
Parameter Size
Quantization
RAM
VRAM
```

---

### 4. Download와 Load 혼동

```text
Model File 다운로드 완료
≠
Runtime Load 완료
```

Chat에서 실제 Loaded Model을 확인합니다.

---

## Evidence

이번 Chapter에서 최소 다음 Evidence를 남깁니다.

```text
LM Studio Version
Developer Mode 상태
Model ID
Parameter Size
Format
Quantization
File Size
Model Load 성공
Prompt / Response
RAM 또는 GPU 변화
```

현재 실습 예:

```text
LM Studio     : 0.4.25
Model ID      : qwen/qwen3-4b-2507
Parameter     : 4B
Format        : GGUF
Quantization  : Q4_K_M
File Size     : 약 2.50 GB
```

---

## 혼자 해보기

현재 모델과 다른 Local Model 후보 1개를 조사합니다.

| 항목 | 현재 실습 모델 | 비교 후보 |
|---|---|---|
| Model | qwen/qwen3-4b-2507 | |
| Parameter Size | 4B | |
| Quantization | Q4_K_M | |
| File Size | 약 2.50 GB | |
| 예상 RAM/VRAM 부담 | | |
| 한국어 사용 목적 | | |
| 선택 이유 | | |

마지막에 답합니다.

```text
내 PC에서는 어느 모델이 더 적절한가?
왜 그렇게 판단했는가?
```

---

## 완료 기준

```text
[ ] LM Studio를 설치했다.
[ ] Developer Mode를 켰다.
[ ] 수업용 Model을 검색했다.
[ ] Model ID를 확인했다.
[ ] GGUF를 확인했다.
[ ] Quantization을 확인했다.
[ ] Model을 다운로드했다.
[ ] Model을 Load했다.
[ ] Prompt / Response를 확인했다.
[ ] RAM / GPU Evidence를 확인했다.
[ ] Model과 Runtime 차이를 설명할 수 있다.
[ ] Download와 Load 차이를 설명할 수 있다.
[ ] Local과 Private 차이를 다시 설명할 수 있다.
```

---

## GitHub 기록 예

```text
chapter02/
└─ local-llm-evidence.md
```

예:

```markdown
# Chapter 02 Local LLM Evidence

## PC 환경

## LM Studio Version

## 사용한 Model

## Quantization

## Download / Load 결과

## Prompt / Response

## RAM / GPU 확인

## Model과 Runtime 차이

## 알게 된 점
```

Commit 예:

```powershell
git status
git add .
git commit -m "chapter02: verify local llm runtime"
git push
```

---

## 다음 강의

Chapter 03에서는 채팅창을 넘어 **Python 프로그램이 Local Model을 API로 호출**합니다.

```text
Chapter 02
사용자
→ LM Studio Chat
→ Local Model

Chapter 03
Python Application
→ HTTP API
→ LM Studio Local Server
→ Local Model
```
