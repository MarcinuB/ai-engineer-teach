---
name: lesson-02-retry-error-handling
description: Completed Lesson 02 — retry logic, JSON repair, self-correction loop for production extractors
metadata:
  type: project
---

Completed Lesson 02 on 2026-06-13. Built retry utilities, JSON repair helpers, and a self-correction loop where the LLM fixes its own invalid output.

**Why notable:** Bridges structured outputs into production: LLMs are probabilistic, so extraction pipelines need retry+repair layers, not just happy-path code. The self-correction pattern (feed the error back to the model) is reusable across any extraction task.

**Implications:**
- Understands retry strategies for LLM APIs (transient errors vs validation errors)
- Understands JSON repair and partial extraction fallbacks
- Ready for Lesson 03: tool calling (the LLM decides when to call functions)
