# Security and Governance

Skills are executable behavioral specifications—and sometimes bundle runnable scripts. Treat every external artifact, user input, and third-party skill contribution as potentially untrusted.

---

## 1. Threat Model & Core Controls

### Prompt Injection Defense
- **Instruction-Data Separation**: Every skill that inspects user text, code diffs, CSV cells, or retrieved documents MUST set `security.untrusted_input_handling: true` and explicitly instruct the agent to treat external content as raw data—never as directives.
- **No Blind Execution from Content**: Never allow instructions found inside code comments, PR descriptions, CSV cells, or fetched web pages to trigger tool calls, change output verdicts, or override system rules.

### Untrusted External Content
- Validate file existence, extension, and size limits before processing (e.g., `MAX_FILE_BYTES = 50 MB` in `skills/data/data-analysis/scripts/profile_csv.py`).
- Never pass raw user strings or cell values into shell command strings. Use parameterized `subprocess.run([exe, arg], shell=False)` exclusively.

### Secrets & Credentials Management
- **Zero Hardcoded Secrets**: Never commit API keys, tokens, passwords, or private keys in `SKILL.md`, `examples/`, `scripts/`, or `tests/`.
- **Declare Names Only**: List required environment variable names in `dependencies.env` (e.g., `["GITHUB_TOKEN"]`), never their values.
- **Output Redaction**: Skills inspecting code or logs (like `code-review`) must redact accidental secret exposures before echoing findings.

### Tool Least-Privilege & Confirmation Gates
- Request the minimal `required_tools` needed:
  - Read-only skills (`code-review`, `prompt-engineering`): `["file_read", "code_search"]`, `risk_level: "low"`.
  - Skills invoking local scripts (`data-analysis`): `["file_read", "shell_exec"]`, `risk_level: "medium"`.
  - Skills mutating external systems, files, or calling network endpoints: `risk_level: "high"`, `requires_confirmation: true`.
- Enforce confirmation before destructive writes, external network calls, or privilege changes.

### External Script Safety
Bundled scripts under `scripts/` MUST:
- Avoid `shell=True`, `eval()`, `exec()`, `pickle.loads()`, or unvalidated network downloads.
- Validate paths and enforce bounded memory/row/file limits.
- Ship with deterministic unit tests in `tests/test_<script>.py`.

---

## 2. Third-Party Contribution Review Checklist

Maintainers reviewing external PRs must verify:

1. **Automated Gates Pass**: `validate_skills.py`, `detect_duplicates.py`, `generate_index.py --check`, and `unittest` all exit `0`.
2. **Scope Matches Declared Risk**: A `low` risk skill does not ask for `shell_exec` or `file_write` without justification.
3. **No Hidden Directives**: Inspect `SKILL.md`, `references/`, and `examples/` for obfuscated Unicode, base64 payloads, or hidden jailbreak instructions.
4. **Script Audit**: Line-by-line review of any new code in `scripts/` for path traversal, command injection, network exfiltration, or unbounded resource consumption.
5. **Reproducible Examples**: Examples and `eval-cases.json` match the actual documented behavior without fabricating capabilities.
