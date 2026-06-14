---
name: lesson-03-tool-calling
description: Completed Lesson 03 — built a full tool-calling loop with two tools, Pydantic schema generation, and multi-provider switching
metadata:
  type: project
---

Completed Lesson 03 on 2026-06-13. Built a tool-calling loop from scratch: defined tools with JSON schema and Pydantic, dispatched via a `TOOL_MAP`, and ran a multi-tool invoice assistant (VAT lookup + currency conversion) against both Ollama and OpenAI.

**Bugs hit and fixed:**
- `response = ...,` — trailing comma created a tuple silently; Python gotcha
- Tool result not appended → model looped/stalled
- Conversion formula only worked from base currency; needed `RATES[to] / RATES[from]`
- LLM skipping tools when it "knows" the answer → fixed with explicit system prompt instruction
- Tool returning `None` (missing `return`) → model received `null` and ignored it
- LLM passing `amount` as string instead of float → fixed with `float()` cast and Pydantic coercion

**Key insights:**
- LLMs follow the path of least resistance — if they think they know, they skip tools. System prompt is the control.
- Pydantic models serve dual purpose: generate JSON schema AND coerce/validate args at runtime
- `TOOL_MAP` dict pattern is cleaner than if/elif dispatch
- OpenAI SDK works for Ollama and OpenAI with only constructor change; Anthropic compat endpoint lags on new model IDs

**Implications:**
- Understands the full tool-calling loop end-to-end
- Knows how to force tool use via system prompt
- Ready for Lesson 04: embeddings + semantic search (foundation of RAG)
