# Contributing to AI Skills Repository

Thank you for contributing! Every skill in this repository is treated as a production software module: it must be focused, portable, token-efficient, safe against untrusted inputs, and backed by automated tests.

## Contribution Workflow

1. **Check for Existing Coverage**: Search [registry/skills-index.json](registry/skills-index.json) or run `python scripts/detect_duplicates.py` to verify your skill does not duplicate an existing skill.
2. **Scaffold from Template**:
   ```bash
   python scripts/create_skill.py --name <kebab-case-name> --category <category-id> --description "<30-500 char trigger-rich summary>"
   ```
   See [docs/naming-conventions.md](docs/naming-conventions.md) and [docs/skill-development-guide.md](docs/skill-development-guide.md).
3. **Author `SKILL.md` & Supporting Files**:
   - Keep `SKILL.md` concise (<2,000 estimated tokens) and move detailed checklists or tables into `references/`.
   - Include at least one realistic worked example in `examples/`.
   - Define at least 3 evaluation cases (`positive_trigger`, `negative_trigger`, and `edge_case` or `security`) in `tests/eval-cases.json`.
   - If adding scripts under `scripts/`, write unit tests in `tests/test_<script>.py` inside the skill folder.
4. **Regenerate the Registry Index**:
   ```bash
   python scripts/generate_index.py
   ```
5. **Run Full Verification Before Opening a PR**:
   ```bash
   python scripts/validate_skills.py
   python scripts/detect_duplicates.py
   python scripts/generate_index.py --check
   python -m unittest discover -s tests -v
   ```

## Pull Request Checklist

- [ ] Skill solves one cohesive problem and does not overlap existing skills.
- [ ] `SKILL.md` frontmatter validates cleanly against `schemas/skill-metadata.schema.json`.
- [ ] All relative links in `SKILL.md` and `README.md` resolve to existing files.
- [ ] No hardcoded secrets, credentials, or unsafe script patterns (`shell=True`, `eval`, `exec`).
- [ ] Security guardrails explicitly treat external/user inputs as untrusted data.
- [ ] `registry/skills-index.json` has been regenerated and committed.
- [ ] Version bumped according to SemVer in `SKILL.md` and documented in `CHANGELOG.md`.

## Security Review Policy

All third-party contributions—especially skills introducing `scripts/` or requesting `shell_exec` / `http_fetch` capabilities—require maintainer review against [docs/security-and-governance.md](docs/security-and-governance.md) before merge.
