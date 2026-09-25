from __future__ import annotations

import os
import sys

from openai import OpenAI


BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
CHAT_MODEL_ID = os.getenv("CHAT_MODEL_ID", "").strip()
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID", "").strip()


client = OpenAI(
    base_url=BASE_URL,
    api_key="lm-studio",
)


def require_model_ids() -> None:
    missing = []
    if not CHAT_MODEL_ID:
        missing.append("CHAT_MODEL_ID")
    if not EMBEDDING_MODEL_ID:
        missing.append("EMBEDDING_MODEL_ID")

    if missing:
        print("FAIL: 다음 환경변수가 설정되지 않았습니다.")
        for name in missing:
            print(f"- {name}")

        print("\nPowerShell 예:")
        print('$env:CHAT_MODEL_ID="실제-chat-model-id"')
        print('$env:EMBEDDING_MODEL_ID="실제-embedding-model-id"')
        print("python scripts/runtime_validate.py")
        raise SystemExit(1)


def validate_models_endpoint() -> None:
    print("=== Gate 1. Models Endpoint ===")
    models = client.models.list()
    ids = [model.id for model in models.data]
    print(f"PASS: {len(ids)}개 모델 확인")

    for model_id in ids:
        print(f"- {model_id}")

    if CHAT_MODEL_ID not in ids:
        print(f"FAIL: CHAT_MODEL_ID를 찾을 수 없습니다: {CHAT_MODEL_ID}")
        raise SystemExit(1)

    if EMBEDDING_MODEL_ID not in ids:
        print(f"FAIL: EMBEDDING_MODEL_ID를 찾을 수 없습니다: {EMBEDDING_MODEL_ID}")
        raise SystemExit(1)


def validate_chat() -> None:
    print("\n=== Gate 2. Chat Completion ===")
    response = client.chat.completions.create(
        model=CHAT_MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": "다음 문장에 한국어로 한 문장만 답하세요: Local LLM Runtime Validation PASS",
            }
        ],
        temperature=0,
    )

    text = response.choices[0].message.content or ""
    if not text.strip():
        print("FAIL: Chat 응답이 비어 있습니다.")
        raise SystemExit(1)

    print("PASS: Chat Completion 응답 확인")
    print(text.strip())


def validate_embedding() -> None:
    print("\n=== Gate 3. Embedding ===")
    response = client.embeddings.create(
        model=EMBEDDING_MODEL_ID,
        input="부산 출장 숙박비 한도",
    )

    vector = response.data[0].embedding
    if not vector:
        print("FAIL: Embedding Vector가 비어 있습니다.")
        raise SystemExit(1)

    print("PASS: Embedding Vector 생성")
    print(f"dimension: {len(vector)}")
    print(f"first 5 values: {vector[:5]}")


def main() -> None:
    print("Private LLM for AX — Runtime Validator")
    print(f"Base URL: {BASE_URL}\n")

    require_model_ids()

    try:
        validate_models_endpoint()
        validate_chat()
        validate_embedding()
    except Exception as exc:
        print(f"\nFAIL: {type(exc).__name__}: {exc}")
        raise SystemExit(1) from exc

    print("\n=== RESULT ===")
    print("PASS: Chapter 03 API와 Chapter 04 Embedding의 최소 Runtime Gate를 통과했습니다.")
    print("다음 단계: Chapter 04 RAG → Chapter 05 Streamlit 검증")


if __name__ == "__main__":
    main()
