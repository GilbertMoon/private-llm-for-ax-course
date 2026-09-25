from __future__ import annotations

import os

from openai import OpenAI


BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
MODEL_ID = os.getenv("CHAT_MODEL_ID", "").strip()


if not MODEL_ID:
    raise SystemExit(
        "CHAT_MODEL_ID가 설정되지 않았습니다. "
        "먼저 python scripts/runtime_preflight.py로 실제 Model ID를 확인한 뒤 "
        '$env:CHAT_MODEL_ID="실제-chat-model-id" 를 설정하세요.'
    )


client = OpenAI(
    base_url=BASE_URL,
    api_key="lm-studio",
)


response = client.chat.completions.create(
    model=MODEL_ID,
    messages=[
        {
            "role": "user",
            "content": "Private LLM의 장점을 세 가지로 설명해 주세요.",
        }
    ],
)

print(response.choices[0].message.content)
