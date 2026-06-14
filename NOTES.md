# Notes

## User Profile

- **20 years programming experience** across multiple languages — treat as a senior engineer, not a beginner
- **Little Python** — knows what Python is, can read it, but not fluent in idioms, tooling, or ecosystem
- Do NOT explain: HTTP, REST APIs, JSON, async/await concepts, error handling patterns, debugging, software architecture
- DO explain: Python-specific syntax quirks, Python tooling (venv, pip, pyproject.toml), Python type hints, Pydantic, Python async idioms

## Teaching Preferences

- Skip basics — user has strong instincts, frame everything relative to what an experienced engineer would already know
- Article-driven 90-day roadmap is the curriculum skeleton:
  - Days 1–30: Python + APIs + structured outputs
  - Days 31–60: RAG + tool calling
  - Days 61–90: evaluations + deployment
- Always show working code they can run immediately
- Include **Python nuggets** in every lesson — explicit callout boxes for Python gotchas/idioms, not hidden in code comments. User wants to pick up Python patterns naturally while learning AI engineering.
- **Providers: Ollama + OpenAI only** — skip Anthropic API for now. Build all examples around these two.

## Expressed Learning Interests

- Transformer architecture internals (attention mechanism, Q/K/V matrices)
- Tokens — how text is split, why token count ≠ word count
- Context windows — how they relate to embeddings of long documents
- Full pipeline: text → tokenise → token embeddings → transformer layers → pooling → final vector

## Article Used as Roadmap

"How I Would Become an AI Engineer in 2026 If I Had to Start Over" — fetched 2026-06-11 via freedium mirror.
Key insight from article: focus on product engineering, not ML research. Ship real projects, skip the tutorials.
