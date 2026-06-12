---
name: lesson-01-structured-output
description: Completed Lesson 01 — built working invoice extractor with nested Pydantic models and debugged a real validation error
metadata:
  type: project
---

Completed Lesson 01 on 2026-06-11. Built the structured output extractor, extended the schema with nested `LineItem` model and `line_items: list[LineItem]`, and ran it against the overdue invoice challenge text.

**Why notable:** Hit a real production-class bug immediately — `date: str` failing when the model returned `null` because the invoice had no date. Fixed by making it `Optional[str] = None`. Also discovered that the system prompt must explicitly describe all fields you want extracted — the model won't infer `line_items` from the Pydantic schema alone.

**Implications:**
- Understands structured output extraction end-to-end
- Understands Pydantic required vs optional fields
- Understands that system prompt must match schema (model doesn't see Python code)
- Ready for Lesson 02: retry logic + error handling, or tool calling
