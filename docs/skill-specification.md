# Skill Specification

Every skill in `skills/<category>/<skill-name>/` is a self-contained module conforming to this specification and validated against [schemas/skill-metadata.schema.json](../schemas/skill-metadata.schema.json).

---

## 1. Required vs. Optional Components

| Component | Status | Purpose |
| :--- | :--- | :--- |
| `SKILL.md` | **Required** | YAML frontmatter + concise agent execution instructions (<2,000 est. tokens recommended; 4,000 hard cap). |
| `README.md` | **Required** | Human-facing overview, file inventory, and quick local test instructions. |
| `tests/eval-cases.json` | **Required** | Minimum 3 cases covering `positive_trigger`, `negative_trigger`, and `edge_case` or `security`. |
| `examples/` | **Recommended** | Concrete input-to-output walkthroughs demonstrating expected quality. |
| `references/` | **Optional** | Deep domain checklists, rubrics, or lookup guides loaded on demand. |
| `scripts/` | **Optional** | Deterministic helper utilities (must include unit tests in `tests/test_*.py` when present). |
| `assets/` | **Optional** | Output report templates, JSON schemas, or static starter artifacts. |

---

## 2. YAML Frontmatter Schema

All fields below are defined formally in [schemas/skill-metadata.schema.json](../schemas/skill-metadata.schema.json).

### Required Fields

| Field | Type | Rules |
| :--- | :--- | :--- |
| `name` | `string` | Lowercase `kebab-case` (2–64 chars), must match the skill directory name. |
| `description` | `string` | 30–500 chars; describes *what* the skill does and *when* to activate it. |
| `category` | `string` | Must match parent folder and exist in `registry/categories.json`. |
| `version` | `string` | Semantic Version (`MAJOR.MINOR.PATCH`, e.g. `1.0.0`). |
| `author` | `string` or `object` | Maintainer name or `{name, handle, url}`. |
| `tags` | `string[]` | 2–12 unique lowercase `kebab-case` keywords. |
| `dependencies` | `object` | `{skills: [], packages: [], env: []}` — declare dependencies explicitly (never store secret values in `env`). |
| `required_tools` | `string[]` | Subset of `["file_read", "file_write", "code_search", "shell_exec", "web_search", "http_fetch", "user_prompt", "mcp_tool"]`. Use `[]` for pure reasoning. |
| `inputs` | `object[]` | Non-empty list of `{name, type, required, description}`. |
| `outputs` | `object[]` | Non-empty list of `{name, type, description}`. |

### Recommended Optional Fields

| Field | Type | Rules |
| :--- | :--- | :--- |
| `title` | `string` | Human-readable display title (2–80 chars). |
| `license` | `string` | SPDX identifier (defaults to `MIT`). |
| `activation` | `object` | `{triggers: [...], non_triggers: [...]}` for deterministic routing and evaluation. |
| `compatibility` | `string[]` | Target runtimes (`openai`, `anthropic`, `google-gemini`, `cursor`, `claude-code`, `codex`, `antigravity`, `mcp`, `generic-llm`). |
| `security` | `object` | `{risk_level: "low"|"medium"|"high", untrusted_input_handling: bool, requires_confirmation: bool}`. |

---

## 3. Required `SKILL.md` Body Sections

`validate_skills.py` enforces the presence of these level-2 Markdown headings:

1. `## Purpose` — Single clear responsibility in 2–3 sentences.
2. `## Activation Conditions` — Concrete *Use This Skill When* and *Do Not Use This Skill When* criteria.
3. `## Inputs & Outputs` — Tabular contract matching the YAML frontmatter.
4. `## Execution Instructions` — Numbered, deterministic step-by-step workflow.
5. `## Error Handling & Edge Cases` — Explicit fallbacks for missing inputs, large inputs, or tool failures.
6. `## Security & Safety Guardrails` — Untrusted-data isolation, secret redaction, and safe tool boundaries.

Recommended trailing sections: `## Examples` and `## Resources` linking to files in `examples/`, `references/`, `assets/`, and `scripts/`.
