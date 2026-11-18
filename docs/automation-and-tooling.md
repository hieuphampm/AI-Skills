# Automation and Tooling

The repository ships a zero-framework Python CLI suite in `scripts/` and a GitHub Actions pipeline in `.github/workflows/validate-skills.yml`.

---

## 1. CLI Tooling Reference

| Script | Responsibility | Usage |
| :--- | :--- | :--- |
| `scripts/create_skill.py` | Scaffolds a new skill from `templates/skill-template` with validated slug and category. | `python scripts/create_skill.py --name api-design --category development --description "..."` |
| `scripts/validate_skills.py` | Validates JSON Schema, folder structure, required Markdown sections, relative links, token budget, eval cases, and security patterns. | `python scripts/validate_skills.py` or `--skill skills/data/data-analysis` |
| `scripts/detect_duplicates.py` | Detects duplicate skill names and flags overlapping descriptions/tags/triggers via Jaccard similarity. | `python scripts/detect_duplicates.py --threshold 0.55` |
| `scripts/generate_index.py` | Deterministically generates `registry/skills-index.json` and validates it against `schemas/registry-index.schema.json`. | `python scripts/generate_index.py` (or `--check` in CI) |
| `scripts/skill_utils.py` | Shared parsing, discovery, link extraction, and token estimation module used by all CLIs and tests. | Imported by scripts and tests |

---

## 2. Continuous Integration

`.github/workflows/validate-skills.yml` runs on every push and pull request targeting `main`:
1. `python scripts/validate_skills.py`
2. `python scripts/detect_duplicates.py`
3. `python scripts/generate_index.py --check`
4. `python -m unittest discover -s tests -v`

---

## 3. Technology Choices & Trade-offs

| Decision | Chosen Approach | Alternative Considered | Trade-off Rationale |
| :--- | :--- | :--- | :--- |
| **CLI Language** | Python 3.10+ (`pyyaml`, `jsonschema`, stdlib `unittest`) | Node.js / TypeScript CLI | Python is ubiquitous in AI/data teams, runs natively on CI without build steps, and pairs cleanly with data/ML helper scripts. Trade-off: requires Python 3.10+ locally. |
| **Skill Format** | Markdown + YAML Frontmatter (`SKILL.md`) | Pure JSON / Python classes | Human-readable, diff-friendly in Git, natively supported by Claude Code, Cursor, Codex, and Antigravity. Trade-off: requires frontmatter parsing & schema validation. |
| **Registry Index** | Static deterministic JSON (`registry/skills-index.json`) | SQLite or vector DB | Zero runtime infrastructure, instant Git-versioned diffs, and `generate_index.py --check` catches stale indexes in CI. Trade-off: semantic/embedding search requires an optional runtime layer once catalog grows >100 skills. |
| **Duplicate Detection** | Tokenized Jaccard similarity on descriptions, tags, and triggers | Embedding-based cosine similarity | Zero API keys or external model dependencies in CI, fast and deterministic. Trade-off: catches lexical overlap well; subtle semantic synonyms still benefit from human PR review. |
| **Test Runner** | Python stdlib `unittest` (with `pyproject.toml` pytest compatibility) | Mandatory `pytest` + Node tools | Works out-of-the-box with zero extra dev installs while remaining `pytest`-compatible. |
