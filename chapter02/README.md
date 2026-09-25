# Chapter 02. Local LLM 직접 실행

## 이번 강의에서 할 일

이번 강의에서는 **LM Studio를 이용해 Local LLM을 내 PC에서 직접 실행**합니다.

핵심 흐름:

```text
Model Download
→ Local Storage
→ Runtime Load
→ Prompt
→ Inference
→ Response
```

## 학습 목표

- Model과 Runtime의 차이를 설명한다.
- RAM / VRAM이 왜 필요한지 설명한다.
- Quantization의 목적을 설명한다.
- LM Studio에서 모델을 다운로드하고 Load한다.
- Local Model에 Prompt를 보내고 Response를 확인한다.
- 실행 Evidence를 남긴다.

## 중요 개념

```text
Model
= 학습된 가중치/파라미터

Runtime
= Model을 메모리에 올리고 실행하는 소프트웨어

Application
= 사용자가 모델과 상호작용하는 프로그램
```

## 실습 순서

### STEP 1. PC 환경 확인

Windows에서 작업 관리자를 열어 다음을 확인합니다.

```text
RAM
GPU
GPU Memory(VRAM)
```

### STEP 2. LM Studio 설치

공식 사이트에서 현재 운영체제에 맞는 버전을 설치합니다.

> 수업 시점의 메뉴와 지원 환경은 공식 문서를 기준으로 확인합니다.

### STEP 3. Local Model 선택

처음부터 가장 큰 모델을 선택하지 않습니다.

확인 항목:

```text
Model Size
Parameter 규모
Quantization
내 PC Memory 여유
```

### STEP 4. Model Download

모델을 다운로드한 뒤 모델 파일이 Local에 존재하는 상태를 확인합니다.

### STEP 5. Model Load

모델을 Runtime에 Load합니다.

```text
Download
≠
Load
```

### STEP 6. 첫 Prompt 실행

예:

```text
Private LLM이 필요한 이유를 세 가지로 설명해 주세요.
```

### STEP 7. Resource Evidence 확인

질문 전후의 RAM/GPU 사용량을 비교합니다.

### STEP 8. Offline 의미 확인

이미 다운로드한 모델이 인터넷 없이 실행될 수 있다는 의미를 이해합니다.

> 실제 Network 격리 여부는 Model 외의 Telemetry, Update, 외부 API 등 전체 Data Flow를 별도로 확인해야 합니다.

## 정상 결과

```text
LM Studio 실행
→ Model Load 성공
→ Prompt 입력
→ Local Response 출력
```

## 흔한 문제

### Model이 너무 큼

증상:

```text
Load 실패
메모리 부족
매우 느린 응답
```

해결 방향:

```text
더 작은 Model
더 낮은 Quantization
Memory 여유 확인
```

## Evidence

```text
사용 Model ID
Model / Quantization 정보
Load 성공
Prompt / Response
RAM 또는 GPU 사용 확인
```

## 혼자 해보기

서로 다른 두 Prompt를 실행하고 다음을 기록합니다.

```text
Model
Prompt
Response
응답 속도 체감
Resource 사용 변화
```

## 완료 기준

```text
[ ] Model을 다운로드했다.
[ ] Model을 Load했다.
[ ] Prompt/Response를 확인했다.
[ ] Model과 Runtime 차이를 설명할 수 있다.
[ ] RAM/VRAM 관계를 설명할 수 있다.
[ ] Local과 Private 차이를 다시 설명할 수 있다.
```

## 다음 강의

Chapter 03에서는 채팅창을 넘어 **Python 프로그램이 Local Model을 API로 호출**합니다.
