# AI Skills Repository

A modular, portable, production-ready **AI Skills Repository** that enables LLM-powered agents and coding assistants to dynamically discover, load, execute, and verify specialized skills.

Built on **progressive disclosure**, **strict JSON Schema validation**, and **zero-lock-in Markdown + YAML specifications**, every skill works seamlessly across OpenAI GPT models, Anthropic Claude, Google Gemini, Cursor, Claude Code, Codex, Antigravity, MCP servers, and custom agent runtimes.

---

## Key Capabilities

- **Modular & Independent**: Each skill lives in `skills/<category>/<skill-name>/` with a single clear responsibility and explicit inputs/outputs.
- **Progressive Disclosure**: Agents scan `registry/skills-index.json` (~100 tokens/skill) first, load `SKILL.md` (<2,000 tokens) only when activated, and read `references/`, `scripts/`, or `assets/` strictly on demand.
- **Portable Across Models & Frameworks**: Capability-based `required_tools` (e.g., `file_read`, `shell_exec`) replace vendor-specific tool names.
- **Automated Quality & Security Gates**: Built-in CLI and GitHub Actions CI validate metadata schemas, folder conventions, relative links, token budgets, duplicate/overlapping triggers, secret leaks, and evaluation cases.

---

## Repository Structure

```text
AI-Skills/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── .github/workflows/validate-skills.yml
├── schemas/
│   ├── skill-metadata.schema.json
│   └── registry-index.schema.json
├── registry/
│   ├── categories.json
│   └── skills-index.json
├── templates/
│   ├── skill-template/
│   └── documentation-template/
├── skills/
│   ├── development/code-review/
│   ├── ai-engineering/prompt-engineering/
│   ├── data/data-analysis/
│   └── productivity/research-paper-analyzer/
├── scripts/
│   ├── skill_utils.py
│   ├── create_skill.py
│   ├── validate_skills.py
│   ├── detect_duplicates.py
│   └── generate_index.py
├── tests/
│   ├── test_validation.py
│   ├── test_scripts.py
│   ├── test_skills_quality.py
│   └── test_skill_scripts.py
└── docs/
    ├── architecture.md
    ├── skill-specification.md
    ├── skill-development-guide.md
    ├── naming-conventions.md
    ├── testing-and-validation.md
    ├── installation-and-integration.md
    ├── security-and-governance.md
    ├── automation-and-tooling.md
    └── roadmap.md
```

---

## Shipped Skills Catalog

| Skill | Category | Version | Risk Level | Description |
| :--- | :--- | :--- | :--- | :--- |
| [code-review](skills/development/code-review/SKILL.md) | `development` | `1.0.0` | `low` | Structured, security-aware code reviews for diffs, PRs, and source files. |
| [prompt-engineering](skills/ai-engineering/prompt-engineering/SKILL.md) | `ai-engineering` | `1.0.0` | `low` | Designs, refactors, and hardens LLM prompts with schemas and anti-injection guards. |
| [data-analysis](skills/data/data-analysis/SKILL.md) | `data` | `1.0.0` | `medium` | Exploratory CSV data analysis backed by deterministic Python profiling (`profile_csv.py`). |
| [research-paper-analyzer](skills/productivity/research-paper-analyzer/SKILL.md) | `productivity` | `1.0.0` | `low` | Source-traceable academic paper analysis, quantitative evidence extraction, methodology appraisal, and APA 7th citations. |

Planned category taxonomy (`development`, `data`, `business`, `ai-engineering`, `productivity`) is defined in [registry/categories.json](registry/categories.json).

---

## Quickstart

### 1. Prerequisites

Python 3.10+ with `pyyaml` and `jsonschema`:

```bash
pip install pyyaml jsonschema
```

### 2. Validate All Skills & Run Tests

```bash
python scripts/validate_skills.py
python scripts/detect_duplicates.py
python scripts/generate_index.py --check
python -m unittest discover -s tests -v
```

### 3. Create a New Skill

```bash
python scripts/create_skill.py \
  --name api-design \
  --category development \
  --description "Designs consistent REST and GraphQL APIs with OpenAPI contracts, pagination, and error standards." \
  --with-references \
  --with-assets
```

Then edit `skills/development/api-design/SKILL.md`, regenerate the registry index (`python scripts/generate_index.py`), and re-run validation.

---

## Documentation Index

- **Architecture & Discovery**: [docs/architecture.md](docs/architecture.md)
- **Skill Format & Metadata Schema**: [docs/skill-specification.md](docs/skill-specification.md)
- **Creating & Versioning Skills**: [docs/skill-development-guide.md](docs/skill-development-guide.md)
- **Naming Conventions**: [docs/naming-conventions.md](docs/naming-conventions.md)
- **QA & Testing Framework**: [docs/testing-and-validation.md](docs/testing-and-validation.md)
- **Agent & Model Integrations**: [docs/installation-and-integration.md](docs/installation-and-integration.md)
- **Security & Governance**: [docs/security-and-governance.md](docs/security-and-governance.md)
- **Automation & Tooling Trade-offs**: [docs/automation-and-tooling.md](docs/automation-and-tooling.md)
- **Roadmap**: [docs/roadmap.md](docs/roadmap.md)
