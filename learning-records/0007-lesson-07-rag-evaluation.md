---
name: lesson-07-rag-evaluation
description: Lesson 07 delivered — RAG evaluation with LLM-as-judge pattern, @dataclass, JSON mode, f-string alignment
metadata:
  type: project
---

Lesson 07 delivered on 2026-06-14. Taught RAG evaluation — moving from vibes-based testing to a repeatable eval harness with numeric metrics.

**Core concepts taught:**
- The two primary RAG metrics: faithfulness (answer grounded in context?) and answer relevance (does it answer the question?)
- LLM-as-judge pattern: use `response_format={"type": "json_object"}` to get structured scores from the same local model
- Eval harness pattern: a `TEST_CASES` list of `@dataclass` instances, run through RAG, scored, summarised as pass rate

**Code built:**
- `invoice-extractor/lesson_007/eval.py` — full eval harness reusing lesson_006's ChromaDB

**Python nuggets taught:**
- `@dataclass` decorator — auto-generates `__init__`, `__repr__`, `__eq__`; Python's equivalent of a TypeScript interface
- `json.loads()` / `json.dumps()` — parse JSON strings from API responses
- f-string alignment: `f"{value:<42}"` (left), `f"{value:>5}"` (right), `f"{value:.0f}"` (float precision)

**Challenges set:**
1. Raise `PASS_THRESHOLD` to 4 and observe which cases drop
2. Add test cases for picnic date, CN-01 amount, contact email
3. Add a third metric: context relevance (`score_context_relevance(question, context)`)

**Implications:**
- Knows how to set up a repeatable, automated eval suite for RAG
- Understands LLM-as-judge as the practical way to score open-ended answers
- Understands the faithfulness/relevance triad (context relevance left as challenge)
- Next natural step: deployment — FastAPI wrapper around the RAG + eval, or stateful agents
