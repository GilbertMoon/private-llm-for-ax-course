from openai import OpenAI


BASE_URL = "http://localhost:1234/v1"
MODEL_ID = "YOUR_MODEL_ID"


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
