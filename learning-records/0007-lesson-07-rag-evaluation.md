---
name: lesson-07-rag-evaluation
description: Completed Lesson 07 — built full RAG eval harness, LLM-as-judge, debugged judge inconsistency, temperature, rubric design
metadata:
  type: project
---

Completed Lesson 07 on 2026-06-15. Built a working eval harness for the lesson 6 RAG pipeline.

**What was built:**
- `invoice-extractor/lesson_007/eval.py` — full eval harness with three metrics: faithfulness, answer relevance, context relevance
- `@dataclass TestCase` with `must_contain` and `expect_refusal` fields
- Separate OpenAI client for the judge (gpt-4o) vs. the RAG model (llama3.2)

**Bugs hit and fixed:**
- `{r_score>5}` instead of `{r_score:>5}` — boolean comparison printed "False" instead of score
- `pass rate` print inside the for loop (wrong indentation)
- Distance threshold `0.5` too strict — lesson 6 uses `0.8`, all RAG results were filtered out
- `must_contain=""` overloaded to mean both "unanswerable question" and "no keyword" — split into `expect_refusal: bool`
- Refusal rubric fighting the main rubric — fixed by giving refusal cases a completely separate judge prompt

**Key insights:**
- Local model (llama3.2) as its own judge is unreliable — inconsistent faithfulness scores. Fix: use a stronger separate model (gpt-4o) as judge.
- `temperature=0` needed on BOTH the RAG model and the judge — judge determinism alone isn't enough if the model being tested is still sampling randomly.
- False positive on Q3: hallucinated date (May→June) passed eval with faithfulness=4. Demonstrates that LLM-as-judge is not a perfect safety net.
- Rubric design matters: "5 = directly answers it" conflicts with a correct refusal. Separate prompts for separate cases.
- User independently added `score_context_relevance` (challenge 3) and integrated it cleanly into the harness.

**Implications:**
- Understands full eval triad end-to-end (faithfulness, answer relevance, context relevance)
- Understands judge model selection and temperature as correctness levers
- Ready for stateful agents — the 4th project on the roadmap
