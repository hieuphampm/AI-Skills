# Code Review Skill

Structured, security-aware code review skill for diffs, pull requests, and source files.

## What It Does

- Standardizes reviews across four severity tiers (`Critical`, `Major`, `Minor`, `Question`).
- Enforces evidence-based findings tied to exact `file:line` references and concrete fixes.
- Guards against prompt injection hidden inside reviewed code comments or PR text.

## Included Files

| File | Role |
| :--- | :--- |
| [SKILL.md](SKILL.md) | Agent instructions, inputs/outputs, and execution workflow |
| [references/review-checklist.md](references/review-checklist.md) | Prioritized correctness, security, performance, and testing checklist |
| [assets/review-report-template.md](assets/review-report-template.md) | Standard markdown report format |
| [examples/python-api-review.md](examples/python-api-review.md) | End-to-end Python endpoint review example |
| [tests/eval-cases.json](tests/eval-cases.json) | Trigger and edge-case test suite |

## Quick Test

Validate structure and metadata:

```bash
python scripts/validate_skills.py --skill skills/development/code-review
```
