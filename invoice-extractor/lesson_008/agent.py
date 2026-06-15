from pathlib import Path
from openai import OpenAI
import chromadb

import sys
DEBUG = "--debug" in sys.argv

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL  = "llama3.2"

DB_DIR = Path(__file__).parent.parent / "lesson_006" / "chroma_db"
chroma = chromadb.PersistentClient(path=str(DB_DIR))
collection = chroma.get_collection(name="invoices")


def embed(text: str) -> list[float]:
    return client.embeddings.create(model=EMBED_MODEL, input=text).data[0].embedding


def retrieve(question: str) -> str:
    results = collection.query(
        query_embeddings=[embed(question)],
        n_results=3,
        include=["documents", "distances"],
    )
    chunks = [
        doc
        for doc, dist in zip(results["documents"][0], results["distances"][0])
        if dist <= 0.8
    ]
    return "\n\n".join(chunks)


def chat(messages: list[dict]) -> str:
    return (
        client.chat.completions
        .create(model=CHAT_MODEL, messages=messages, temperature=0)
        .choices[0].message.content
    )


def main():
    messages = [
        {
            "role": "system",
            "content": (
                "You are an invoice assistant. When context is provided in a user message, "
                "answer using ONLY that context. If no context is provided, use the conversation history. "
                "If you don't have enough information, say so."
            ),
        }
    ]

    print("Invoice assistant ready. Type 'quit' to exit.\n")
    i = 0
    while True:
        i += 1
        messages = [messages[0]] + messages[1:][-6:]
        try:
            question = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break

        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        if not question:
            continue

        context = retrieve(question)
        if context:
            user_content = f"Context:\n{context}\n\nQuestion: {question}"
        else:
            user_content = question

        if DEBUG:
            print(f"[context]: {context}\n")
        messages.append({"role": "user", "content": user_content})
        reply = chat(messages)
        messages.append({"role": "assistant", "content": reply})
        print(f"Assistant: {reply}\n")
        print (f"[turn {i} - {len(messages) - 1} messages]")
        


if __name__ == "__main__":
    main()
