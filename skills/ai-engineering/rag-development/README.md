# RAG Development

Human-facing overview and usage guide for the `rag-development` skill.

## Overview

`rag-development` turns a document corpus and a set of questions into a concrete, production-ready Retrieval-Augmented Generation (RAG) design. It covers the full pipeline — ingestion, chunking, embedding, retrieval, reranking, and grounded generation — and always pairs the architecture with an evaluation plan so quality is measurable rather than assumed.

Prefer this skill over general-purpose prompting whenever the answer must be grounded in retrieved documents. For the generation prompt itself, it composes `ai-engineering/prompt-engineering`.

## Directory Structure

- `SKILL.md` — Agent-facing specification, metadata, and execution instructions.
- `README.md` — Human-facing documentation and integration notes.
- `references/rag-design-checklist.md` — Chunking, retrieval, reranking, and evaluation decision guide.
- `assets/rag-design-template.md` — Output template for the delivered RAG design.
- `examples/support-kb-rag-design.md` — End-to-end input-to-output walkthrough.
- `tests/eval-cases.json` — Trigger and behavioral evaluation cases.

## Quick Usage

Invoke this skill in any compatible agent by referencing `skills/ai-engineering/rag-development/SKILL.md`, or run validation with:

```bash
python scripts/validate_skills.py --skill skills/ai-engineering/rag-development
```
