---
name: lesson-04-embeddings
description: Completed Lesson 04 — built semantic search from scratch, deep discussion on how embeddings work
metadata:
  type: project
---

Completed Lesson 04 on 2026-06-13. Built a full semantic search pipeline: embed function, cosine similarity from scratch (no numpy), document store, ranked search with sorted()+zip().

**Deep discussion covered:**
- Why "unpaid" matches "overdue" — co-occurrence in training data, not explicit synonym mapping
- How transformers encode whole sentences (attention: every token attends to every other token)
- Real measurements: finance context "overdue" (0.760) vs scheduling "overdue" (0.662) — model correctly separates domains
- Why 768 dimensions: BERT's 12 heads × 64 dims, empirical sweet spot
- Attention heads: 12 parallel specialisations, roles emerge from training
- Domain-specialised models: separate training, not a slice of general model's space

**Expressed interest in (for future lessons):**
- Transformer architecture internals (Q/K/V matrices, positional encoding)
- Tokens — how text is split, why token count ≠ word count
- Context windows and how they affect embedding of long documents

**Python nuggets absorbed:** list[float] type hints, zip(), generator expressions, list comprehensions, sorted() vs .sort() gotcha

**Implications:**
- Understands semantic search end-to-end
- Understands why cosine similarity (not dot product) — magnitude normalisation
- Ready for Lesson 05: full RAG pipeline (load files → retrieve → inject → answer)
