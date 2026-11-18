"""Shared utilities for AI-Skills validation, indexing, scaffolding, and deduplication."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
TEMPLATES_DIR = REPO_ROOT / "templates"
SCHEMAS_DIR = REPO_ROOT / "schemas"
REGISTRY_DIR = REPO_ROOT / "registry"

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
KEBAB_CASE_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class ParsedSkill:
    """Parsed representation of a skill directory and its SKILL.md."""

    skill_dir: Path
    category_dir: str
    slug: str
    frontmatter: dict[str, Any]
    body: str
    raw_text: str


def load_json(path: Path) -> dict[str, Any]:
    """Load and parse a UTF-8 JSON file."""
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def load_categories(registry_dir: Path = REGISTRY_DIR) -> dict[str, dict[str, str]]:
    """Return mapping of category id -> category definition."""
    data = load_json(registry_dir / "categories.json")
    return {item["id"]: item for item in data.get("categories", [])}


def discover_skill_dirs(skills_root: Path = SKILLS_DIR) -> list[Path]:
    """Find all skill directories laid out as skills/<category>/<skill-name>."""
    if not skills_root.exists():
        return []
    discovered: list[Path] = []
    for category_path in sorted(skills_root.iterdir()):
        if not category_path.is_dir() or category_path.name.startswith("."):
            continue
        for skill_path in sorted(category_path.iterdir()):
            if skill_path.is_dir() and not skill_path.name.startswith("."):
                discovered.append(skill_path)
    return discovered


def parse_skill_markdown(skill_dir: Path) -> ParsedSkill:
    """Parse SKILL.md YAML frontmatter and Markdown body from a skill directory."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"Missing SKILL.md in {skill_dir}")

    raw_text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(raw_text)
    if not match:
        raise ValueError(f"{skill_md} must begin with valid YAML frontmatter delimited by '---'")

    yaml_text, body = match.group(1), match.group(2)
    loaded = yaml.safe_load(yaml_text)
    if not isinstance(loaded, dict):
        raise ValueError(f"YAML frontmatter in {skill_md} must parse to a mapping")

    return ParsedSkill(
        skill_dir=skill_dir,
        category_dir=skill_dir.parent.name,
        slug=skill_dir.name,
        frontmatter=loaded,
        body=body,
        raw_text=raw_text,
    )


def extract_h2_headings(markdown_body: str) -> list[str]:
    """Return all level-2 (##) headings in a Markdown body."""
    return [match.group(2).strip() for match in HEADING_RE.finditer(markdown_body) if match.group(1) == "##"]


def extract_relative_links(markdown_text: str) -> list[str]:
    """Return non-URL, non-anchor relative paths referenced via Markdown links."""
    links: list[str] = []
    for match in MARKDOWN_LINK_RE.finditer(markdown_text):
        target = match.group(1).strip().split("#", 1)[0]
        if not target:
            continue
        if target.startswith(("http://", "https://", "mailto:", "file://")):
            continue
        links.append(target)
    return links


def estimate_tokens(text: str) -> int:
    """Approximate LLM token count (~1.33 tokens per whitespace-delimited word)."""
    words = len(text.split())
    return int(round(words * 1.33))


def list_resource_files(skill_dir: Path, subdir: str) -> list[str]:
    """Return sorted POSIX relative paths of files inside a skill subdirectory."""
    folder = skill_dir / subdir
    if not folder.is_dir():
        return []
    return sorted(
        path.relative_to(skill_dir).as_posix()
        for path in folder.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )
