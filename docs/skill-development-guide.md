# Skill Development Guide

Follow this end-to-end workflow to design, implement, verify, and version a production skill.

---

## Step 1: Scope & De-duplication Check

Before creating files, ensure the skill follows the **Single Responsibility Principle**:
- Can you state its core job in one sentence without using "and everything related to..."?
- Does [registry/skills-index.json](../registry/skills-index.json) already contain an overlapping skill?

If an existing skill covers 80% of the workflow, prefer extending or composing it via `dependencies.skills` rather than creating a near-duplicate.

---

## Step 2: Scaffold from the Template

Run `create_skill.py` with optional resource flags only when needed:

```bash
python scripts/create_skill.py \
  --name api-design \
  --category development \
  --description "Designs consistent REST and GraphQL API contracts with OpenAPI schemas, versioning, and error handling." \
  --author "Your Name" \
  --with-references \
  --with-assets
```

Available flags:
- `--with-references`: Creates `references/domain-guide.md`.
- `--with-scripts`: Creates `scripts/run_helper.py` (use when deterministic computation, parsing, or validation beats LLM guessing).
- `--with-assets`: Creates `assets/output-template.md`.

---

## Step 3: Author `SKILL.md` for Token Efficiency

Keep `SKILL.md` crisp and imperative:
- Target **600–1,500 tokens** (soft warning at `2,000`, hard failure at `4,000`).
- Put long checklists, rubrics, or lookup tables in `references/` and link them directly from the step where the agent needs them.
- Use active imperatives ("Verify X before Y", "If missing, ask Z and stop") instead of vague advice ("Try to be helpful and consider X").

---

## Step 4: Add Concrete Examples & Tests

1. Replace the template content in `examples/` with a **realistic input and complete expected output** (see [skills/development/code-review/examples/python-api-review.md](../skills/development/code-review/examples/python-api-review.md)).
2. Author at least 3 cases in `tests/eval-cases.json`:
   - `positive_trigger`: Realistic user prompt that must activate the skill.
   - `negative_trigger`: Adjacent out-of-scope prompt that must NOT activate it.
   - `edge_case` / `security`: Missing input, empty artifact, or prompt-injection attempt.
3. If you added Python utilities under `scripts/`, write unit tests under `tests/test_<module>.py` inside the skill folder. `tests/test_skill_scripts.py` automatically discovers and executes them.

---

## Step 5: Validate & Update Registry

```bash
python scripts/validate_skills.py --skill skills/<category>/<name>
python scripts/detect_duplicates.py
python scripts/generate_index.py
python -m unittest discover -s tests -v
```

---

## Versioning Strategy (Semantic Versioning)

Both the repository and each individual skill use `MAJOR.MINOR.PATCH`:

- **PATCH (`1.0.x`)**: Typo fixes, clarified examples, tightened edge-case instructions, or internal script bug fixes with no contract change.
- **MINOR (`1.x.0`)**: New optional inputs, expanded checklist coverage, or new supporting scripts/templates backward-compatible with existing integrations.
- **MAJOR (`x.0.0`)**: Breaking changes to `inputs`, `outputs`, `required_tools`, or core behavioral scope.

Document every change in [CHANGELOG.md](../CHANGELOG.md) when bumping versions.
