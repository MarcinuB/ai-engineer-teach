import math
import os
from pathlib import Path
from openai import OpenAI

# Ollama
BASE_URL = "http://localhost:11434/v1"
API_KEY = "ollama"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2"


def embed(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x*y for x, y in zip(a,b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(y*y for y in b))
    return dot / (norm_a * norm_b)


DOCS_DIR = Path(__file__).parent / "docs"

docs = [p.read_text(encoding="utf-8") for p in sorted(DOCS_DIR.glob("*.txt"))]
doc_embeddings = [embed(doc) for doc in docs]

print(f"Loaded {len(docs)} documents.")


def search(
    query: str, top_k: int = 2, threshold: float = 0.6
) -> list[tuple[str, float]]:
    query_vec = embed(query)
    scores = [cosine_similarity(query_vec, dv) for dv in doc_embeddings]
    ranked = sorted(zip(docs, scores), key=lambda p: p[1], reverse=True)
    return [(doc, score) for doc, score in ranked[:top_k] if score >= threshold]


def build_context(results: list[tuple[str, float]]) -> str:
    return "\n\n".join(
        f"[Document {i + 1}]\n{doc}" for i, (doc, score) in enumerate(results)
    )


def rag_query(question: str) -> str:
    results = search(question)
    for i, (txt, score) in enumerate(results):
        print(f"[result {i + 1}]: {txt.splitlines()[0]} ({score}) ")
    
    if not results:
        return "I couldn't find any relevant documents to answer that question."

    context = build_context(results)

    system_prompt = f""" you are an invoice assistant. Answer the user's question using ONLY \
the documents provided below. If the answer is not in the documents, say so explicitly \
- do not use your training knowledge.
        
Documents:
{context}"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    questions = [
        "Which invoices are overdue?",
        "Did Beta Ltd receive any credit notes?",
        "Has Delta SA responded to the overdue notice?",
        "What is the weather in Warsaw today?",  # should say "not in documents"
        "When is the company picnic?"
    ]

    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {rag_query(q)}")
