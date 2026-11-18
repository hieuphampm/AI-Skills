# Testing and Validation Framework

Every skill in the AI Skills Repository undergoes both **deterministic structural validation** and **behavioral evaluation** before acceptance.

---

## 1. Nine-Dimension Quality Rubric

| Dimension | Evaluation Standard | Verification Method |
| :--- | :--- | :--- |
| **Instruction Clarity** | Imperative, unambiguous steps; explicit abstain/clarify behavior. | Human review + `eval-cases.json` |
| **Task Completion Accuracy** | Produces valid, evidence-backed outputs matching `examples/` and `outputs`. | Behavioral eval / unit tests |
| **Reusability** | Parameterized inputs/outputs; zero hardcoded project-specific paths or URLs. | Review + `inputs` schema |
| **Modularity** | Single clear responsibility; composes other skills via `dependencies.skills` rather than duplicating them. | `detect_duplicates.py` |
| **Reliability** | Explicit handling for empty/missing/oversized inputs and unavailable tools. | `## Error Handling & Edge Cases` + `edge_case` tests |
| **Maintainability** | Clean separation between `SKILL.md`, `references/`, `scripts/`, and `assets/`. | `validate_skills.py` |
| **Token Efficiency** | `SKILL.md` under 2,000 est. tokens (hard cap 4,000); heavy details offloaded to `references/`. | `validate_skills.py` token counter |
| **Security** | Untrusted-data guardrails, zero leaked secrets, no `shell=True`/`eval`/`exec` in `scripts/`. | Static scanner + `security` eval cases |
| **Compatibility** | Portable capability-based `required_tools` and vendor-neutral Markdown instructions. | Schema check + integration tests |

---

## 2. Automated Validation Checklist

Running `python scripts/validate_skills.py` verifies all of the following automatically:

1. **Frontmatter & JSON Schema**: YAML frontmatter exists and conforms strictly to [schemas/skill-metadata.schema.json](../schemas/skill-metadata.schema.json).
2. **Path & Taxonomy Integrity**: `name` matches folder slug, `category` matches parent directory and exists in `registry/categories.json`.
3. **Required Artifacts**: `SKILL.md`, `README.md`, and `tests/eval-cases.json` are present.
4. **Required Sections**: All 6 required level-2 Markdown headings exist in `SKILL.md`.
5. **Link Integrity**: Every relative Markdown link in `SKILL.md` and `README.md` resolves to an existing file.
6. **No Leftover Placeholders**: Zero `{{TOKEN}}` strings remain anywhere in the skill directory.
7. **Token Budget**: `SKILL.md` passes the soft (`2,000`) and hard (`4,000`) estimated token thresholds.
8. **Security Static Scan**: No API key/private-key patterns and no unsafe Python patterns (`shell=True`, `eval(`, `exec(`) inside `scripts/`.
9. **Eval Suite Completeness**: `tests/eval-cases.json` contains >= 3 cases including at least one `positive_trigger` and one `negative_trigger`.

---

## 3. Testing Methodology

### Layer A: Repository & Script Unit Tests (Deterministic)
Run via Python's built-in `unittest` runner:

```bash
python -m unittest discover -s tests -v
```

This executes:
- [tests/test_validation.py](../tests/test_validation.py): Schema, link, placeholder, and security-gate tests.
- [tests/test_scripts.py](../tests/test_scripts.py): Scaffolding, duplicate detection, and index generation tests.
- [tests/test_skills_quality.py](../tests/test_skills_quality.py): Index synchronization, token budgets, and eval coverage checks.
- [tests/test_skill_scripts.py](../tests/test_skill_scripts.py): Auto-discovers and runs `skills/*/*/tests/test_*.py` (such as `skills/data/data-analysis/tests/test_profile_csv.py`).

### Layer B: Behavioral & Trigger Evaluation (`tests/eval-cases.json`)
Every skill defines structured cases in `tests/eval-cases.json`:
- **`positive_trigger`**: Verifies the agent selects the skill when relevant and satisfies `expected_assertions`.
- **`negative_trigger`**: Verifies the skill does *not* falsely activate on adjacent out-of-scope prompts.
- **`edge_case` / `security`**: Verifies safe fallback on empty/missing inputs and resistance to prompt injection.

Teams using an external LLM eval harness (e.g., Promptfoo, Ragas, or a custom pytest-LLM runner) can load `registry/skills-index.json` + each skill's `tests/eval-cases.json` to score activation precision/recall and assertion pass rates across target models.
