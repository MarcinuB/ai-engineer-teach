import chromadb
from pathlib import Path
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
EMBED_MODEL = "nomic-embed-text"

DOCS_DIR = Path(__file__).parent / "docs"
DB_DIR   = Path(__file__).parent / "chroma_db"

chroma = chromadb.PersistentClient(path=str(DB_DIR))
collection = chroma.get_or_create_collection(name="invoices")
# collection = chroma.get_or_create_collection(name="invoices", metadata={"hnsw:space": "cosine"},)


def chunk_text(text: str, size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start += size - overlap
    return chunks

def embed(text: str) -> list[float]:
    resp = client.embeddings.create(model=EMBED_MODEL, input=text)
    return resp.data[0].embedding

def ingest():
    for path in sorted(DOCS_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        chunks = chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            doc_id = f"{path.stem}_chunk{i}"
            existing_items = collection.get(ids=[doc_id])
            if(len(existing_items['ids']) > 0):
                print("Already ingested")
                continue
            print("Ingesting")
            collection.add(
                ids=[doc_id],
                documents=[chunk],
                embeddings=[embed(chunk)],
                metadatas=[{"source": path.name, "chunk": i}]    
            )
            
            print(f". stored {doc_id}")
            
        print(f"Ingested {path.name}: {len(chunks)} chunks")
        
if __name__ == "__main__":
    ingest()
            