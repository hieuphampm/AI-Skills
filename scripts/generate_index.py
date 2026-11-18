#!/usr/bin/env python3
"""Deterministically generate and validate registry/skills-index.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from skill_utils import (
    REGISTRY_DIR,
    REPO_ROOT,
    SCHEMAS_DIR,
    SKILLS_DIR,
    discover_skill_dirs,
    list_resource_files,
    load_json,
    parse_skill_markdown,
)


def build_index(skills_dir: Path = SKILLS_DIR, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Build deterministic skills index payload from validated skill directories."""
    entries: list[dict[str, Any]] = []
    for skill_dir in discover_skill_dirs(skills_dir):
        parsed = parse_skill_markdown(skill_dir)
        fm = parsed.frontmatter
        rel_path = skill_dir.relative_to(repo_root).as_posix()
        security = fm.get("security") if isinstance(fm.get("security"), dict) else {}
        entries.append(
            {
                "id": f"{fm['category']}/{fm['name']}",
                "name": fm["name"],
                "title": fm.get("title") or fm["name"],
                "category": fm["category"],
                "version": fm["version"],
                "description": fm["description"],
                "tags": sorted(fm.get("tags") or []),
                "required_tools": list(fm.get("required_tools") or []),
                "compatibility": list(fm.get("compatibility") or []),
                "risk_level": security.get("risk_level", "low"),
                "path": rel_path,
                "entrypoint": f"{rel_path}/SKILL.md",
                "resources": {
                    "references": list_resource_files(skill_dir, "references"),
                    "scripts": list_resource_files(skill_dir, "scripts"),
                    "assets": list_resource_files(skill_dir, "assets"),
                    "examples": list_resource_files(skill_dir, "examples"),
                    "tests": list_resource_files(skill_dir, "tests"),
                },
            }
        )

    entries.sort(key=lambda item: item["id"])
    return {
        "schema_version": "1.0.0",
        "skill_count": len(entries),
        "skills": entries,
    }


def validate_index_payload(payload: dict[str, Any], schemas_dir: Path = SCHEMAS_DIR) -> None:
    schema = load_json(schemas_dir / "registry-index.schema.json")
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(payload))
    if errors:
        messages = "; ".join(err.message for err in errors)
        raise ValueError(f"Generated index failed schema validation: {messages}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or verify registry/skills-index.json.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify registry/skills-index.json is up to date without writing.",
    )
    args = parser.parse_args(argv)

    index_path = REGISTRY_DIR / "skills-index.json"
    payload = build_index()
    validate_index_payload(payload)
    rendered = json.dumps(payload, indent=2) + "\n"

    if args.check:
        if not index_path.is_file():
            print(f"Error: {index_path} does not exist. Run python scripts/generate_index.py", file=sys.stderr)
            return 1
        existing = index_path.read_text(encoding="utf-8")
        if existing != rendered:
            print("Error: registry/skills-index.json is stale. Run python scripts/generate_index.py", file=sys.stderr)
            return 1
        print(f"registry/skills-index.json is up to date ({payload['skill_count']} skills).")
        return 0

    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(rendered, encoding="utf-8")
    print(f"Generated {index_path} with {payload['skill_count']} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
