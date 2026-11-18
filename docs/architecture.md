# System Architecture

The AI Skills Repository is designed as a **layered, progressive-disclosure skill registry**. Its primary goal is maximizing agent accuracy and portability while minimizing context-window bloat.

---

## 1. Architectural Principles

1. **Progressive Disclosure (3-Tier Loading)**: Loading dozens of full skill prompts into every LLM turn wastes tokens and degrades attention. Agents load skills in three lightweight stages:
   - **Tier 1 — Discovery (`registry/skills-index.json`)**: ~80–120 tokens per skill (`id`, `name`, `description`, `tags`, `required_tools`, `risk_level`). Used for routing.
   - **Tier 2 — Activation (`skills/<category>/<name>/SKILL.md`)**: <2,000 tokens. Loaded only after the agent selects a skill for the current task.
   - **Tier 3 — On-Demand Resources (`references/`, `assets/`, `scripts/`, `examples/`)**: Loaded or executed only during specific workflow steps.
2. **Framework-Agnostic Core**: Skills are plain Markdown + YAML + optional standard CLI scripts—never tied to a proprietary SDK or single LLM vendor.
3. **Capability Abstraction**: Skills declare abstract `required_tools` (`file_read`, `shell_exec`, etc.) instead of host-specific names (`read_file`, `Bash`, `run_command`). Host adapters map capabilities to concrete tools.
4. **Deterministic Offloading**: Calculations, parsing, and schema checks belong in `scripts/` (e.g., `skills/data/data-analysis/scripts/profile_csv.py`) rather than LLM arithmetic.

---

## 2. Progressive Disclosure Flow

```text
User Request
     │
     ▼
[Tier 1] Agent scans registry/skills-index.json (descriptions + tags)
     │
     ├── No match ──▶ Handle with base agent capabilities
     │
     └── Match found (e.g., data/data-analysis)
             │
             ▼
[Tier 2] Agent loads skills/data/data-analysis/SKILL.md
             │  Checks Activation Conditions & Inputs
             ▼
[Tier 3] Agent runs scripts/profile_csv.py & reads references/statistical-checks.md
             │
             ▼
Structured Output returned using assets/analysis-report-template.md
```

---

## 3. Directory Design Decisions

| Directory | Purpose | Why Separated? |
| :--- | :--- | :--- |
| `schemas/` | Formal JSON Schemas (Draft 2020-12) | Single source of truth for CI validation and external index consumers. |
| `registry/` | `categories.json` & generated `skills-index.json` | Enables instant O(1) discovery without walking the filesystem at runtime. |
| `templates/` | Canonical scaffolds for new skills and guides | Guarantees uniform layout and eliminates boilerplate drift. |
| `skills/` | Domain-organized, self-contained skill modules | Clean 2-level hierarchy (`<category>/<skill-name>`) avoids flat-folder sprawl and deep nesting. |
| `scripts/` | Repository maintenance CLIs | Keeps validation, duplicate detection, and index generation deterministic. |
| `tests/` | Automated structural, script, and quality tests | Ensures repository integrity before any PR merges. |
| `docs/` | Architecture, spec, security, and integration docs | Separates platform engineering docs from runtime agent context. |

### Why Only Active Skills Live in `skills/`
Empty placeholder directories create noise in discovery indexes and invite stale metadata. New categories are declared in `registry/categories.json`, and individual skill directories are created via `scripts/create_skill.py` only when an implementation is authored.

---

## 4. Category Taxonomy

Defined in [registry/categories.json](../registry/categories.json):

- `development`: Code review, API design, frontend/backend engineering, testing, refactoring.
- `data`: Exploratory data analysis, visualization, statistical auditing, data pipelines.
- `business`: Requirements/business analysis, project planning, product documentation.
- `ai-engineering`: Prompt engineering, RAG pipelines, agent orchestration, LLM evaluation.
- `productivity`: Literature/web research synthesis, technical writing, workflow automation.
