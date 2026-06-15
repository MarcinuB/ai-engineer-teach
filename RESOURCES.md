# Resources

## Knowledge

### Core Roadmap
- [How I Would Become an AI Engineer in 2026](https://medium.com/data-science-collective/how-i-would-become-an-ai-engineerin-2026-if-i-had-to-start-over-c80bd754c753) — The article that seeded this curriculum. Covers 4-stage progression, 5 essential projects, 90-day timeline, and traps to avoid. High signal, product-engineering focused.

### APIs & SDKs
- [Anthropic Claude API Docs](https://docs.anthropic.com) — Primary LLM API used in lessons. Covers messages API, tool use, structured outputs, streaming, and model tiers.
- [OpenAI API Docs](https://platform.openai.com/docs) — Alternative API; same patterns apply. Good for comparison.

### Python Ecosystem
- [Pydantic Docs](https://docs.pydantic.dev) — Schema validation library. Essential for structured outputs from LLMs.
- [FastAPI Docs](https://fastapi.tiangolo.com) — Async web framework for building LLM-backed APIs.
- [httpx Docs](https://www.python-httpx.org) — Async HTTP client for calling external APIs.

### Agent Frameworks
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/) — State machine framework for building stateful LLM workflows and agents.
- [LangSmith](https://docs.smith.langchain.com) — Observability and tracing for LLM applications.

### Observability
- [Helicone](https://docs.helicone.ai) — LLM observability proxy. Tracks cost, latency, quality.

## Wisdom (Communities)

- [r/LocalLLaMA](https://reddit.com/r/LocalLLaMA) — Active practitioner community. Good signal on what's actually working in production.
- [Latent Space / AI Engineer Foundation](https://www.latent.space) — Podcast + community for AI engineers. High quality practitioners.
- [Hugging Face Discord](https://discord.gg/huggingface) — Large community, good for model questions.

### Evaluation
- [RAGAS Docs](https://docs.ragas.io) — RAG evaluation framework. Implements faithfulness, answer relevance, context relevance metrics. Good reference for extending the hand-built eval harness from lesson 7.
- [LLM-as-a-Judge (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685) — Original paper establishing LLM-as-judge as a scalable evaluation pattern. Covers agreement with human raters and prompt design for judges.
