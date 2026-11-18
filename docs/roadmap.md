# Roadmap

A phased evolution plan balancing immediate production utility with scalable multi-agent ecosystem growth.

---

## Phase 1 — Foundation (v1.0 — Current)
- Canonical repository layout, JSON Schemas (`skill-metadata`, `registry-index`), and category taxonomy.
- Standardized `SKILL.md` specification and reusable templates.
- Automation CLIs (`create_skill.py`, `validate_skills.py`, `detect_duplicates.py`, `generate_index.py`).
- GitHub Actions CI validation + unit/quality test suite.
- Three reference skills across `development`, `ai-engineering`, and `data`.

## Phase 2 — Catalog Expansion & Live Eval Runner (v1.5)
- Expand core catalog across remaining categories (`development/api-design`, `ai-engineering/rag-development`, `ai-engineering/llm-evaluation`, `business/documentation`, `productivity/research`).
- Add an optional `scripts/run_evals.py` harness that executes `tests/eval-cases.json` against configurable LLM providers (OpenAI, Anthropic, Gemini) to benchmark trigger accuracy and assertion pass rates.
- Add semantic embedding index export (`registry/skills-embeddings.jsonl`) alongside `skills-index.json` for large catalogs (>50 skills).

## Phase 3 — MCP Server & Package Distribution (v2.0)
- Ship a lightweight read-only **MCP Server** (`mcp-ai-skills`) serving `skills://index` and `skills://<category>/<name>` resources directly to IDE and desktop agents.
- Add `scripts/export_bundle.py` to compile/install subsets of skills directly into `.claude/skills/`, `.cursor/rules/`, or `.agent/skills/` targets.
- Add automated skill changelog and version-bump helpers (`scripts/bump_version.py`).

## Phase 4 — Governance & Composable Pipelines (v3.0)
- Dependency graph resolver for multi-skill composition (`dependencies.skills`) with cycle detection.
- Signed skill manifests / checksum verification for high-security enterprise deployments.
- Telemetry adapters (token usage, activation precision, failure rate) for continuous skill optimization.
