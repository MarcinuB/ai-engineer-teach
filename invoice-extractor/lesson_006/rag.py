import chromadb
from pathlib import Path
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL  = "llama3.2"

DB_DIR = Path(__file__).parent / "chroma_db"
chroma = chromadb.PersistentClient(path=str(DB_DIR))
collection = chroma.get_collection(name="invoices")


def embed(text: str) -> list[float]:
    resp = client.embeddings.create(model = EMBED_MODEL, input=text)
    return resp.data[0].embedding

def search(query: str, top_k: int = 3, max_distance: float = 0.8) -> list[dict]:
    results = collection.query(
        query_embeddings=[embed(query)],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    chunks = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]
    print(f"raw distances: {dists}")   # ← add this
    return [
        {"text": c, "source": m["source"], "distance": d}
        for c,m,d in zip(chunks, metas, dists)
        if d <= max_distance
    ] 
    
def rag_query(question: str) -> str:
    results = search(question)
    
    for i, r in enumerate(results):
        print(f". [{i+1}] dist={r['distance']:.3f} src={r['source']} | {r['text'][:80]}")
    
    sources = ""
    if(len(results) > 0):
        sources = "\n".join(
            f"{r['source']}" for i, r in enumerate(results)
        )
        
    context = "\n\n".join(
        f"[Source: {r['source']}]\n{r['text']}" for r in results
    )
    
    system_prompt = f"""You are an invoice assistant. Answer using ONLY documents below.
    If the answer is not in the documents, say so explicitly.
    
    Documents:
    {context}
    """
    
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    result = resp.choices[0].message.content.join(["\n", sources])
    
    return result

if __name__ == "__main__":
    questions = [
        "Which invoices are overdue?",
        "Did Beta Ltd receive any credit notes?",
        "What is the weather in Warsaw today?"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {rag_query(q)}")