import math
import os
from openai import OpenAI


# Ollama
BASE_URL = "http://localhost:11434/v1"
API_KEY="ollama"
EMBED_MODEL = "nomic-embed-text"


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def embed(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x*y for x, y in zip(a,b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(y*y for y in b))
    return dot / (norm_a * norm_b)


DOCS = [
    "Invoice #1001 from Acme Corp — €500 for consulting. Status: paid.",
    "Invoice #1002 from Beta Ltd — €1,200 for software licences. Status: overdue.",
    "Invoice #1003 from Gamma GmbH — €350 for hardware maintenance. Status: paid.",
    "Invoice #1004 from Delta SA — €8,400 for annual support contract. Status: overdue.",
    "Credit note #CN-01 issued to Beta Ltd for €200 — duplicate charge refund.",
]

doc_embeddings = [embed(doc) for doc in DOCS]

def search(query: str, top_k: int=3) -> list[tuple[str, float]]:
    query_vec = embed(query)
    scores = [cosine_similarity(query_vec, dv) for dv in doc_embeddings]
    ranked = sorted(zip(DOCS, scores), key=lambda pair: pair[1], reverse=True)
    return ranked[:top_k]


if __name__ == "__main__":
    queries = [
        "Which invoices are unpaid?",
        "Any credit notes issued?",
        "The library book is overdue.",
        "Large contracts over €5000?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        for doc, score in search(query, top_k=2):
            print (f". [{score:.3f}] {doc}")
        
        
    print()
    print('vectors test')
    sentences = [
        "Invoice is overdue. Please pay.",
        "Our meeting is long overdue.",
        "The library book is overdue.",
        "Invoice #1002 from Beta Ltd. Status: overdue.",
    ]
    vecs = [embed(s) for s in sentences]
    
    #compare everything against the first sentence
    ref = vecs[0]
    for s, v in zip(sentences, vecs):
        score = cosine_similarity(ref, v)
        print(f"{score:.3f}  {s}")