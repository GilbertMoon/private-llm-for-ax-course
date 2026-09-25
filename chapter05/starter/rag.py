from pathlib import Path

import numpy as np
from openai import OpenAI


BASE_URL = "http://localhost:1234/v1"
CHAT_MODEL_ID = "YOUR_CHAT_MODEL_ID"
EMBEDDING_MODEL_ID = "YOUR_EMBEDDING_MODEL_ID"
DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "sample" / "company_policy.txt"


client = OpenAI(base_url=BASE_URL, api_key="lm-studio")


def load_document() -> str:
    return DATA_PATH.read_text(encoding="utf-8")


def split_into_chunks(text: str) -> list[str]:
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL_ID,
        input=text,
    )
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a_vec = np.array(a)
    b_vec = np.array(b)
    denominator = np.linalg.norm(a_vec) * np.linalg.norm(b_vec)
    if denominator == 0:
        return 0.0
    return float(np.dot(a_vec, b_vec) / denominator)


def build_index() -> list[dict]:
    chunks = split_into_chunks(load_document())
    return [
        {
            "chunk_id": i,
            "text": chunk,
            "embedding": embed_text(chunk),
            "source": DATA_PATH.name,
        }
        for i, chunk in enumerate(chunks)
    ]


def retrieve(question: str, index: list[dict], top_k: int = 3) -> list[dict]:
    question_embedding = embed_text(question)
    scored = []

    for item in index:
        score = cosine_similarity(question_embedding, item["embedding"])
        scored.append({**item, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def generate_answer(question: str, retrieved: list[dict]) -> str:
    context = "\n\n".join(
        f"[Source: {item['source']} / Chunk: {item['chunk_id']}]\n{item['text']}"
        for item in retrieved
    )

    prompt = f"""
아래 Context만 사용해서 질문에 답하세요.
Context에 답이 없으면 "제공된 문서에서 확인할 수 없습니다."라고 답하세요.
추측하지 마세요.

[Context]
{context}

[Question]
{question}
""".strip()

    response = client.chat.completions.create(
        model=CHAT_MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
