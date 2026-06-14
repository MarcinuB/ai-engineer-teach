---
name: lesson-05-rag-pipeline
description: Completed Lesson 05 — built full RAG pipeline, debugged system prompt delivery, tuned similarity threshold
metadata:
  type: project
---

Completed Lesson 05 on 2026-06-14. Built a full RAG pipeline from scratch: load docs → embed → semantic search → inject into system prompt → LLM answer.

**Bugs caught and fixed:**
- `extra_body={"system": prompt}` — Ollama silently ignores this field; system prompt was never reaching the model. Fix: pass as `{"role": "system", "content": prompt}` in messages list.
- `if not results:` early return placed after the debug print loop — cosmetic issue, moved before.

**Key insight — threshold tuning:**
- Default threshold 0.5 caused the "what's the weather in Warsaw?" question to match invoice documents (irrelevant hit).
- User independently identified and fixed: raised threshold to 0.6, which correctly returned no results for unrelated queries.
- This is real RAG calibration work — threshold is a dial between recall (lower) and precision (higher).

**Python nuggets absorbed:** f-strings with method calls (`txt.splitlines()[0]`), `enumerate()` start index, `Path(__file__).parent` for relative file paths.

**Implications:**
- Understands full RAG loop end-to-end
- Understands threshold as a precision/recall tradeoff knob
- Next natural step: chunking (embedding whole documents is a toy — real RAG needs chunks) + vector stores (ChromaDB)
