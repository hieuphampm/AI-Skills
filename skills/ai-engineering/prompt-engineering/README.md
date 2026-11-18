# Prompt Engineering Skill

Designs, refactors, and hardens LLM prompts for deterministic outputs, token efficiency, and prompt-injection resistance.

## What It Does

- Separates system instructions from untrusted user/RAG payloads using explicit delimiters.
- Replaces vague prose with strict output contracts, abstain rules, and boundary few-shot examples.
- Ships every prompt with a mini evaluation suite (happy path, edge case, injection defense).

## Included Files

| File | Role |
| :--- | :--- |
| [SKILL.md](SKILL.md) | Agent instructions and prompt design workflow |
| [references/prompt-patterns.md](references/prompt-patterns.md) | Reusable prompt architecture & anti-injection patterns |
| [assets/prompt-spec-template.md](assets/prompt-spec-template.md) | Standardized prompt specification deliverable template |
| [examples/classifier-prompt-refactor.md](examples/classifier-prompt-refactor.md) | Before/after refactoring of a support ticket classifier |
| [tests/eval-cases.json](tests/eval-cases.json) | Trigger and behavioral evaluation cases |

## Quick Test

```bash
python scripts/validate_skills.py --skill skills/ai-engineering/prompt-engineering
```
