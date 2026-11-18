# Research Paper Analyzer Skill

Rigorous academic research analysis skill focused on verifiable evidence extraction, numerical accuracy, methodological appraisal, and source-traceable citations.

## What It Does

- Extracts bibliographic metadata, research questions, methodology, and qualitative/quantitative findings directly from accessible academic papers.
- Enforces three explicit verification tiers (`VERIFIED`, `PARTIALLY VERIFIED`, `UNVERIFIED`) and strict anti-hallucination disclosures.
- Preserves units, sample sizes, statistical notation, and experimental conditions while guarding against common statistical confusions.
- Supports both single-paper deep analysis and multi-paper comparative evidence matrices.

## Included Files

| File | Role |
| :--- | :--- |
| [SKILL.md](SKILL.md) | Core workflow, verification tiers, anti-hallucination rules, and guardrails |
| [references/methodology-and-numerical-protocol.md](references/methodology-and-numerical-protocol.md) | Extraction checklists, 10-step numerical protocol, statistical distinctions, appraisal rubric, multi-paper rules, and final QA checklist |
| [references/citation-and-evidence-rules.md](references/citation-and-evidence-rules.md) | 12-field citation schema, 10 citation rules, and table/figure reading rules |
| [assets/analysis-report-template.md](assets/analysis-report-template.md) | Standard report structure (Sections A–K) and multi-paper comparison matrix |
| [examples/rct-paper-analysis.md](examples/rct-paper-analysis.md) | End-to-end worked example demonstrating traceable citations and verification tags |
| [tests/eval-cases.json](tests/eval-cases.json) | Trigger, numerical accuracy, anti-hallucination, and security evaluation suite |

## Quick Test

```bash
python scripts/validate_skills.py --skill skills/productivity/research-paper-analyzer
```
