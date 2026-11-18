#!/usr/bin/env python3
"""Scaffold a new AI skill from templates/skill-template."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from skill_utils import FRONTMATTER_RE, KEBAB_CASE_RE, REGISTRY_DIR, SKILLS_DIR, TEMPLATES_DIR, load_categories


def _title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def _escape_for_quoted_scalar(value: str) -> str:
    """Escape a string so it is safe inside double-quoted YAML/JSON literals."""
    single_line = " ".join(value.splitlines()).strip()
    return json.dumps(single_line)[1:-1]


def _apply_replacements(text: str, replacements: dict[str, str]) -> str:
    for token, value in replacements.items():
        text = text.replace(token, value)
    return text


def create_skill(
    name: str,
    category: str,
    description: str,
    author: str = "AI-Skills Contributor",
    title: str | None = None,
    skills_dir: Path = SKILLS_DIR,
    templates_dir: Path = TEMPLATES_DIR,
    registry_dir: Path = REGISTRY_DIR,
    with_references: bool = False,
    with_scripts: bool = False,
    with_assets: bool = False,
) -> Path:
    """Create a new skill directory from the canonical skill template."""
    if not KEBAB_CASE_RE.match(name):
        raise ValueError(f"Skill name '{name}' must be lowercase kebab-case (e.g., api-design).")

    categories = load_categories(registry_dir)
    if category not in categories:
        allowed = ", ".join(sorted(categories))
        raise ValueError(f"Invalid category '{category}'. Allowed categories: {allowed}")

    if len(description.strip()) < 30:
        raise ValueError("Description must be at least 30 characters to support reliable agent discovery.")

    target_dir = skills_dir / category / name
    if target_dir.exists():
        raise FileExistsError(f"Skill directory already exists: {target_dir}")

    template_root = templates_dir / "skill-template"
    if not template_root.is_dir():
        raise FileNotFoundError(f"Skill template not found at {template_root}")

    resolved_title = " ".join((title.strip() if title else _title_from_slug(name)).splitlines())
    clean_description = " ".join(description.strip().splitlines())
    clean_author = " ".join(author.strip().splitlines())

    raw_replacements = {
        "{{SKILL_NAME}}": name,
        "{{SKILL_TITLE}}": resolved_title,
        "{{SKILL_DESCRIPTION}}": clean_description,
        "{{CATEGORY}}": category,
        "{{AUTHOR}}": clean_author,
    }
    escaped_replacements = {k: _escape_for_quoted_scalar(v) for k, v in raw_replacements.items()}

    for src_file in template_root.rglob("*"):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(template_root)
        dest_file = target_dir / rel
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        content = src_file.read_text(encoding="utf-8")
        if dest_file.suffix.lower() == ".json":
            content = _apply_replacements(content, escaped_replacements)
        elif dest_file.name == "SKILL.md":
            fm_match = FRONTMATTER_RE.match(content)
            if fm_match:
                fm_rendered = _apply_replacements(fm_match.group(1), escaped_replacements)
                body_rendered = _apply_replacements(fm_match.group(2), raw_replacements)
                content = f"---\n{fm_rendered}\n---\n{body_rendered}"
            else:
                content = _apply_replacements(content, raw_replacements)
        else:
            content = _apply_replacements(content, raw_replacements)
        dest_file.write_text(content, encoding="utf-8")

    if with_references:
        ref_dir = target_dir / "references"
        ref_dir.mkdir(parents=True, exist_ok=True)
        guide_src = templates_dir / "documentation-template" / "skill-guide-template.md"
        if guide_src.is_file():
            (ref_dir / "domain-guide.md").write_text(guide_src.read_text(encoding="utf-8"), encoding="utf-8")

    if with_scripts:
        scripts_dir = target_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        (scripts_dir / "run_helper.py").write_text(
            '#!/usr/bin/env python3\n"""Deterministic helper script for '
            f'{name}."""\n\n\ndef main() -> int:\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n',
            encoding="utf-8",
        )

    if with_assets:
        assets_dir = target_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        (assets_dir / "output-template.md").write_text(
            f"# {resolved_title} Output\n\n## Summary\n\n- Key finding\n",
            encoding="utf-8",
        )

    return target_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new AI skill from template.")
    parser.add_argument("--name", required=True, help="Kebab-case skill name (e.g., api-design).")
    parser.add_argument("--category", required=True, help="Category ID from registry/categories.json.")
    parser.add_argument("--description", required=True, help="Trigger-oriented description (>=30 chars).")
    parser.add_argument("--author", default="AI-Skills Contributor", help="Author or maintainer name.")
    parser.add_argument("--title", default=None, help="Optional human-readable title.")
    parser.add_argument("--with-references", action="store_true", help="Scaffold references/domain-guide.md.")
    parser.add_argument("--with-scripts", action="store_true", help="Scaffold scripts/run_helper.py.")
    parser.add_argument("--with-assets", action="store_true", help="Scaffold assets/output-template.md.")
    args = parser.parse_args(argv)

    try:
        created = create_skill(
            name=args.name,
            category=args.category,
            description=args.description,
            author=args.author,
            title=args.title,
            with_references=args.with_references,
            with_scripts=args.with_scripts,
            with_assets=args.with_assets,
        )
    except (ValueError, FileExistsError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Created skill scaffold at: {created}")
    print(f"Next steps:\n  1. Edit {created / 'SKILL.md'}\n  2. Run: python scripts/validate_skills.py --skill {created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
