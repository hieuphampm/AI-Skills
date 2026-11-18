# Changelog

All notable changes to the AI Skills Repository are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and both the repository and individual skills adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-18

### Added
- Core repository architecture with JSON Schemas (`schemas/skill-metadata.schema.json`, `schemas/registry-index.schema.json`).
- Canonical category registry (`registry/categories.json`) and deterministic skill index (`registry/skills-index.json`).
- Standardized skill and documentation templates (`templates/skill-template/`, `templates/documentation-template/`).
- Automation CLI suite in `scripts/` (`create_skill.py`, `validate_skills.py`, `detect_duplicates.py`, `generate_index.py`, `skill_utils.py`).
- Automated unit, quality, and integration test suite in `tests/` plus GitHub Actions CI workflow (`.github/workflows/validate-skills.yml`).
- Four production-ready reference skills:
  - `development/code-review` (`1.0.0`)
  - `ai-engineering/prompt-engineering` (`1.0.0`)
  - `data/data-analysis` (`1.0.0`, including deterministic `scripts/profile_csv.py` and unit tests)
  - `productivity/research-paper-analyzer` (`1.0.0`, academic evidence extraction, methodology appraisal, and source-traceable citations)
- Full architectural, specification, security, integration, QA, tooling, and roadmap documentation in `docs/`.
