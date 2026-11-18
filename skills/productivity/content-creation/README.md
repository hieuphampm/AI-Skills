# Content Creation

Human-facing overview and usage guide for the `content-creation` skill.

## Overview

`content-creation` turns a topic and an audience into a clear, well-structured piece of written content — blog post, article, documentation page, social post, or email. It always starts from a hook, follows a logical outline, and ends with a concrete call-to-action, then optimizes the result for SEO and readability.

## Directory Structure

- `SKILL.md` — Agent-facing specification, metadata, and execution instructions.
- `README.md` — Human-facing documentation and integration notes.
- `references/content-style-guide.md` — Structure, SEO, and readability decision guide.
- `assets/content-draft-template.md` — Output template for the delivered draft.
- `examples/product-launch-blog-post.md` — End-to-end brief-to-draft walkthrough.
- `tests/eval-cases.json` — Trigger and behavioral evaluation cases.

## Quick Usage

Invoke this skill in any compatible agent by referencing `skills/productivity/content-creation/SKILL.md`, or run validation with:

```bash
python scripts/validate_skills.py --skill skills/productivity/content-creation
```
