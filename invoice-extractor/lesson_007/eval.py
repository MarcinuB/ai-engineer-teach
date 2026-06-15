from dataclasses import dataclass
import json
import os
from pathlib import Path
from openai import OpenAI
import chromadb

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2"

DB_DIR = Path(__file__).parent.parent / "lesson_006" / "chroma_db"
chroma = chromadb.PersistentClient(path=str(DB_DIR))
collection = chroma.get_collection(name="invoices")

# Open AI
EVAL_BASE_URL = "https://api.openai.com/v1"
EVAL_API_KEY = os.getenv("OPENAI_API_KEY")
EVAL_MODEL = "gpt-4o"
client_eval = OpenAI(base_url=EVAL_BASE_URL, api_key=EVAL_API_KEY)


# -- Test cases ----------------------


@dataclass
class TestCase:
    question: str
    must_contain: str  # key fact the answer should include; empty = expect refusal
    expect_refusal: bool = False


TEST_CASES = [
    TestCase("What is the amount on invoice 1002?", "1,200"),
    TestCase("Who is the client on invoice 1004?", "Delta"),
    TestCase("What is the due date for invoice 1002?", "2026-05-31"),
    TestCase("Is invoice 1004 overdue?", "overdue"),
    TestCase("What is credit note CN-01 for?", "duplicate"),
    TestCase("What is the weather in Warsaw?", "", expect_refusal=True),
    TestCase("When is the company picnic?", "15th May"),
    TestCase("What is the CN-01 credit note amount?", "200"),
]


# -- RAG ---------------


def embed(text: str) -> list[float]:
    return client.embeddings.create(model=EMBED_MODEL, input=text).data[0].embedding


def rag(question: str) -> tuple[str, str]:
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

    context = "\n\n".join(chunks)

    if not context:
        return "", "I don't have relevant information to answer that."

    messages = [
        {"role": "system", "content": f"Answer using ONLY this context:\n\n{context}"},
        {"role": "user", "content": question},
    ]

    answer = (
        client.chat.completions.create(
            model=CHAT_MODEL, messages=messages, temperature=0
        )
        .choices[0]
        .message.content
    )
    return context, answer


# -- LLM-as-judge


def judge(prompt: str) -> tuple[int, str]:
    resp = client_eval.chat.completions.create(
        model=EVAL_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0,
    )
    data = json.loads(resp.choices[0].message.content)
    return int(data["score"]), data["reason"]


def score_context_relevance(question: str, context: str) -> tuple[int, str]:
    return judge(f"""Rate how relevant this context is for answering the question.
5 = context directly contains the information needed. 1 = context is off-topic or empty.
Return JSON: {{"score": <1-5>, "reason": "<one sentence>"}}

Question: {question}
Context: {context}
""")


def score_faithfulness(context: str, answer: str) -> tuple[int, str]:
    return judge(f"""Rate how faithful this answer is to the context.
5 = fully supported, no hallucinations. 1 = contradicts or ignores context.
Return JSON: {{"score": <1-5>, "reason": "<one sentence>"}}
Note: concise answers are fine — score on grounding only, not completeness.
Context: {context}
Answer: {answer}""")


def score_relevance(
    question: str, answer: str, must_contain: str, expect_refusal: bool = False
) -> tuple[int, str]:
    if expect_refusal:
        return judge(f"""This question cannot be answered from the available documents.
Rate whether the model correctly refused to answer.
5 = model says it has no relevant information (correct).
1 = model attempts to answer anyway (incorrect).
Return JSON: {{"score": <1-5>, "reason": "<one sentence>"}}

Question: {question}
Answer: {answer}""")

    hint = f"The answer should mention: {must_contain}" if must_contain else ""
    return judge(f"""Rate how well this answer addresses the question.
5 = directly and completely answers it. 1 = misses the point entirely.
{hint}
Return JSON: {{"score": <1-5>, "reason": "<one sentence>"}}

Question: {question}
Answer: {answer}""")


# -- Main -----------

PASS_THRESHOLD = 4

if __name__ == "__main__":
    passed = 0

    print(f"\n{'#':3} {'Question':42} {'Faith':>5} {'Relev':>5} {'Ctx':>5} {'OK?':>4}")
    print("─" * 65)

    for i, tc in enumerate(TEST_CASES, 1):
        context, answer = rag(tc.question)

        if context:
            f_score, _ = score_faithfulness(context, answer)
            cr_score, _ = score_context_relevance(tc.question, context)
        else:
            f_score = 5  # refusal is always faithful - nothing was hallucinated
            cr_score = 5

        r_score, r_reason = score_relevance(
            tc.question, answer, tc.must_contain, tc.expect_refusal
        )
        ok = (
            f_score >= PASS_THRESHOLD
            and r_score >= PASS_THRESHOLD
            and cr_score >= PASS_THRESHOLD
        )

        if ok:
            passed += 1

        q = tc.question[:39] + "..." if len(tc.question) > 39 else tc.question
        print(
            f"{i:3} {q:42} {f_score:>5} {r_score:>5} {cr_score:>5} {'✓' if ok else '✗':>4}"
        )
        print(f"    A: {answer[:90]}")
        if not ok:
            print(f"   ↳ {r_reason}")
        print()

    rate = passed / len(TEST_CASES) * 100
    print(f"Pass rate: {passed}/{len(TEST_CASES)} ({rate:.0f}%)")
