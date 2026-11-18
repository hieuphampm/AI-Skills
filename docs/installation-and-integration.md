# Installation and Integration Guide

Skills in this repository use portable Markdown + YAML frontmatter (`SKILL.md`) and a machine-readable catalog (`registry/skills-index.json`), making them easy to integrate across models, IDE assistants, and custom runtimes.

---

## 1. Capability-to-Tool Mapping

Skills declare abstract capabilities in `required_tools`. Map them to your host agent's native tools:

| Portable Capability | Claude Code / Antigravity | Cursor | OpenAI / Custom Function Calling |
| :--- | :--- | :--- | :--- |
| `file_read` | `Read` / `read_file` | `@Files` / Read tool | `read_file(path)` |
| `file_write` | `Write` / `Edit` / `write_file` | Edit / Apply tool | `write_file(path, content)` |
| `code_search` | `Grep` / `Glob` / `grep` | Codebase Search | `search_files(pattern)` |
| `shell_exec` | `Bash` / `run_command` | Terminal tool | `run_command(cmd)` *(sandboxed)* |
| `web_search` | `WebSearch` / `search_web` | Web search | Search tool |
| `http_fetch` | `WebFetch` | Fetch URL | Sandboxed HTTP client |
| `user_prompt` | `AskUserQuestion` / `ask_question` | Chat follow-up | Interactive clarification |
| `mcp_tool` | MCP server tools | MCP integration | MCP client bridge |

---

## 2. Assistant & IDE Integrations

### Claude Code & Codex
Symlink or copy individual skill folders (or the entire `skills/` categories) into your project or user skills directory:
- **Project-local**: `.claude/skills/<skill-name>/` or `.agents/skills/<skill-name>/`
- **User-global**: `~/.claude/skills/<skill-name>/`

Example (Linux/macOS):
```bash
ln -s /path/to/AI-Skills/skills/development/code-review .claude/skills/code-review
```

Example (Windows PowerShell):
```powershell
Copy-Item -Recurse G:\AI-Skills\skills\development\code-review .claude\skills\code-review
```

### Cursor
Reference `SKILL.md` directly in `.cursor/rules/` or `@`-mention `skills/<category>/<name>/SKILL.md` in chat. For automatic routing across all skills, add a lightweight `.cursor/rules/skills-router.mdc` rule pointing Cursor to `registry/skills-index.json`.

### Google Gemini & Antigravity (AGY)
Copy or link a skill folder into `.agent/skills/<skill-name>/` (workspace) or `~/.gemini/antigravity/skills/<skill-name>/` (global). Antigravity discovers `SKILL.md` frontmatter (`name`, `description`) automatically and loads full instructions on activation.

---

## 3. Programmatic Integration (OpenAI, Anthropic, Gemini SDKs)

Use a 3-step progressive loader in any custom Python agent:

```python
import json
from pathlib import Path

repo = Path("path/to/AI-Skills")
index = json.loads((repo / "registry" / "skills-index.json").read_text(encoding="utf-8"))

# Step 1: Inject compact discovery catalog into the router/system prompt
catalog_lines = [
    f"- {s['id']}: {s['description']} (tools: {', '.join(s['required_tools'])})"
    for s in index["skills"]
]
router_context = "Available skills:\n" + "\n".join(catalog_lines)

# Step 2: Once the model selects a skill ID (e.g., 'development/code-review'), load SKILL.md
selected = next(s for s in index["skills"] if s["id"] == "development/code-review")
skill_instructions = (repo / selected["entrypoint"]).read_text(encoding="utf-8")

# Step 3: Load references/ or execute scripts/ only when the skill step requires them
```

This pattern works identically with:
- **OpenAI** (`responses.create` / `chat.completions.create` with a `load_skill(skill_id)` tool)
- **Anthropic Claude** (`messages.create` with a `load_skill` tool)
- **Google Gemini** (`google-genai` `generate_content` with a `load_skill` function declaration)

---

## 4. MCP-Compatible Agent Systems

To expose this repository over the **Model Context Protocol (MCP)**:
1. Expose `registry/skills-index.json` as an MCP **Resource** (`skills://index`) and each `SKILL.md` + `references/*` as `skills://<category>/<name>/<file>`.
2. Expose a read-only MCP **Tool** `get_skill(skill_id)` returning `SKILL.md` and resource paths.
3. For skills with `scripts/` (like `data/data-analysis`), wrap verified scripts behind typed, parameterized MCP tools rather than exposing arbitrary shell execution.
