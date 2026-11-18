# {{SKILL_TITLE}}

Human-facing overview and usage guide for the `{{SKILL_NAME}}` skill.

## Overview

Describe the problem this skill solves, its target audience, and when to prefer it over general-purpose prompting.

## Directory Structure

- `SKILL.md` — Agent-facing specification, metadata, and execution instructions.
- `README.md` — Human-facing documentation and integration notes.
- `examples/` — Practical input/output walkthroughs.
- `tests/` — Structured trigger and behavioral evaluation cases.
- `references/` *(optional)* — Domain checklists, standards, and reference docs.
- `scripts/` *(optional)* — Deterministic helper scripts.
- `assets/` *(optional)* — Output templates and schemas.

## Quick Usage

Invoke this skill in any compatible agent by referencing `skills/{{CATEGORY}}/{{SKILL_NAME}}/SKILL.md`, or run validation with:

```bash
python scripts/validate_skills.py --skill skills/{{CATEGORY}}/{{SKILL_NAME}}
```
