from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from openai import OpenAI


BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
CHAT_MODEL_ID = os.getenv("CHAT_MODEL_ID", "").strip()
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID", "").strip()
DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "sample" / "company_policy.txt"


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
        names = ", ".join(missing)
        raise RuntimeError(
            f"필수 환경변수가 없습니다: {names}. "
            "scripts/runtime_preflight.py로 실제 Model ID를 확인한 뒤 설정하세요."
        )


def load_document(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_into_chunks(text: str) -> list[str]:
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


def prepare_embedding_input(text: str, task: str) -> str:
    """Add task prefixes required by Nomic Embed retrieval models."""
    if "nomic-embed-text" not in EMBEDDING_MODEL_ID.lower():
        return text

    if task == "document":
        return f"search_document: {text}"
    if task == "query":
        return f"search_query: {text}"
    raise ValueError(f"지원하지 않는 embedding task입니다: {task}")


def embed_text(text: str, task: str) -> list[float]:
    require_model_ids()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL_ID,
        input=prepare_embedding_input(text, task),
    )
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a_vec = np.array(a)
    b_vec = np.array(b)
    denominator = np.linalg.norm(a_vec) * np.linalg.norm(b_vec)
    if denominator == 0:
        return 0.0
    return float(np.dot(a_vec, b_vec) / denominator)


def build_index(chunks: list[str]) -> list[dict]:
    return [
        {
            "chunk_id": i,
            "text": chunk,
            "embedding": embed_text(chunk, task="document"),
            "source": DATA_PATH.name,
        }
        for i, chunk in enumerate(chunks)
    ]


def retrieve(question: str, index: list[dict], top_k: int = 3) -> list[dict]:
    question_embedding = embed_text(question, task="query")
    scored = []

    for item in index:
        score = cosine_similarity(question_embedding, item["embedding"])
        scored.append({**item, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def answer_question(question: str, retrieved: list[dict]) -> str:
    require_model_ids()
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
    return response.choices[0].message.content or ""


def main() -> None:
    require_model_ids()
    document = load_document(DATA_PATH)
    chunks = split_into_chunks(document)
    index = build_index(chunks)

    question = input("질문을 입력하세요: ").strip()
    retrieved = retrieve(question, index)

    print("\n=== Retrieval Evidence ===")
    for item in retrieved:
        print(f"\n[score={item['score']:.4f}] {item['source']} / chunk {item['chunk_id']}")
        print(item["text"])

    answer = answer_question(question, retrieved)

    print("\n=== Answer ===")
    print(answer)


if __name__ == "__main__":
    main()
