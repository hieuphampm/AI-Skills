# Naming Conventions

Consistent naming ensures deterministic discovery, clean diffs, and zero collisions across multi-agent ecosystems.

---

## 1. Skill Directories & Slugs

- **Pattern**: `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$` (lowercase `kebab-case`, 2–64 chars).
- **Rule**: Frontmatter `name` MUST exactly equal the directory name, and `category` MUST match the parent folder under `skills/`.
  - Valid: `skills/development/code-review/SKILL.md` (`name: code-review`, `category: development`)
  - Invalid: `skills/development/CodeReview/`, `code_review`, or `cr`
- **Action-Domain Clarity**: Prefer clear domain nouns or verb-noun pairs (`code-review`, `data-analysis`, `prompt-engineering`, `api-design`). Avoid vague names like `helper`, `utils`, or `general-ai`.

---

## 2. Registry Skill IDs

Canonical fully qualified IDs use `<category>/<name>`:
- `development/code-review`
- `ai-engineering/prompt-engineering`
- `data/data-analysis`

---

## 3. Files Inside a Skill Directory

| Artifact | Convention | Example |
| :--- | :--- | :--- |
| Agent spec | Exact uppercase filename | `SKILL.md` |
| Human guide | Exact uppercase filename | `README.md` |
| Reference docs | Lowercase `kebab-case.md` in `references/` | `references/review-checklist.md` |
| Output templates / assets | Lowercase `kebab-case.<ext>` in `assets/` | `assets/review-report-template.md` |
| Usage examples | Lowercase `kebab-case.md` in `examples/` | `examples/python-api-review.md` |
| Executable Python scripts | Lowercase `snake_case.py` in `scripts/` | `scripts/profile_csv.py` |
| Eval cases | Fixed JSON filename in `tests/` | `tests/eval-cases.json` |
| Script unit tests | `test_<script_name>.py` in `tests/` | `tests/test_profile_csv.py` |

---

## 4. Frontmatter Keys, Inputs, Outputs & Tags

- **Frontmatter keys, `inputs[].name`, `outputs[].name`**: `snake_case` (`target_code`, `required_tools`, `untrusted_input_handling`).
- **`tags`**: Lowercase `kebab-case`, 2–12 unique tags per skill (`code-review`, `static-analysis`).
- **`dependencies.env`**: `UPPER_SNAKE_CASE` variable names only (`OPENAI_API_KEY`, `GITHUB_TOKEN`).
- **`required_tools`**: Use only canonical portable capability identifiers:
  - `file_read`, `file_write`, `code_search`, `shell_exec`, `web_search`, `http_fetch`, `user_prompt`, `mcp_tool`.
