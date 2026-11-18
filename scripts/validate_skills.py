#!/usr/bin/env python3
"""Validate AI skills for schema compliance, structure, links, token budget, and security."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from skill_utils import (
    REGISTRY_DIR,
    SCHEMAS_DIR,
    SKILLS_DIR,
    discover_skill_dirs,
    estimate_tokens,
    extract_h2_headings,
    extract_relative_links,
    is_within_directory,
    load_categories,
    load_json,
    parse_skill_markdown,
)

REQUIRED_H2_SECTIONS = (
    "Purpose",
    "Activation Conditions",
    "Inputs & Outputs",
    "Execution Instructions",
    "Error Handling & Edge Cases",
    "Security & Safety Guardrails",
)

SECRET_PATTERNS = (
    ("OpenAI/Anthropic-style key", re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}\b")),
    ("AWS Access Key ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub PAT", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)

UNSAFE_SCRIPT_PATTERNS = (
    ("shell=True subprocess call", re.compile(r"shell\s*=\s*True")),
    ("dynamic eval() call", re.compile(r"\beval\s*\(")),
    ("dynamic exec() call", re.compile(r"\bexec\s*\(")),
)

PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
MAX_SKILL_TOKENS_WARN = 2000
MAX_SKILL_TOKENS_FAIL = 4000


@dataclass
class ValidationResult:
    skill_path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    estimated_tokens: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def _validate_eval_cases(skill_dir: Path, skill_name: str, errors: list[str]) -> None:
    eval_path = skill_dir / "tests" / "eval-cases.json"
    if not eval_path.is_file():
        errors.append("Missing required evaluation suite: tests/eval-cases.json")
        return

    try:
        data = json.loads(eval_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in tests/eval-cases.json: {exc}")
        return

    if data.get("skill_name") != skill_name:
        errors.append(f"tests/eval-cases.json skill_name '{data.get('skill_name')}' != '{skill_name}'")

    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 3:
        errors.append("tests/eval-cases.json must define at least 3 evaluation cases")
        return

    case_types: set[str] = set()
    for idx, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"tests/eval-cases.json case[{idx}] must be a JSON object")
            continue
        case_type = case.get("type")
        if isinstance(case_type, str) and case_type:
            case_types.add(case_type)
        else:
            errors.append(f"tests/eval-cases.json case[{idx}] missing non-empty 'type'")
        if not isinstance(case.get("id"), str) or not case["id"].strip():
            errors.append(f"tests/eval-cases.json case[{idx}] missing non-empty 'id'")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"tests/eval-cases.json case[{idx}] missing non-empty 'prompt'")
        if not isinstance(case.get("expected_activation"), bool):
            errors.append(f"tests/eval-cases.json case[{idx}] missing boolean 'expected_activation'")
        assertions = case.get("expected_assertions")
        if not isinstance(assertions, list) or not assertions or not all(isinstance(a, str) and a.strip() for a in assertions):
            errors.append(f"tests/eval-cases.json case[{idx}] must define a non-empty list of string 'expected_assertions'")

    if "positive_trigger" not in case_types:
        errors.append("tests/eval-cases.json must include at least one 'positive_trigger' case")
    if "negative_trigger" not in case_types:
        errors.append("tests/eval-cases.json must include at least one 'negative_trigger' case")


def _scan_security_and_placeholders(skill_dir: Path, errors: list[str]) -> None:
    for file_path in sorted(skill_dir.rglob("*")):
        if not file_path.is_file() or "__pycache__" in file_path.parts:
            continue
        if file_path.suffix.lower() not in {".md", ".py", ".json", ".yaml", ".yml", ".sh", ".txt"}:
            continue
        content = file_path.read_text(encoding="utf-8")
        rel = file_path.relative_to(skill_dir).as_posix()

        if PLACEHOLDER_RE.search(content):
            errors.append(f"Unresolved template placeholder found in {rel}")

        for label, pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"Potential hardcoded secret ({label}) detected in {rel}")

        if file_path.suffix.lower() == ".py" and file_path.parent.name == "scripts":
            for label, pattern in UNSAFE_SCRIPT_PATTERNS:
                if pattern.search(content):
                    errors.append(f"Unsafe Python pattern ({label}) detected in {rel}")


def validate_skill(
    skill_dir: Path,
    validator: Draft202012Validator,
    categories: dict[str, dict[str, str]],
) -> ValidationResult:
    """Run all structural, schema, link, token-budget, and security checks on one skill."""
    result = ValidationResult(skill_path=skill_dir)

    try:
        parsed = parse_skill_markdown(skill_dir)
    except (FileNotFoundError, ValueError, yaml.YAMLError) as exc:
        result.errors.append(str(exc))
        return result

    for err in sorted(validator.iter_errors(parsed.frontmatter), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "<root>"
        result.errors.append(f"Frontmatter schema error at '{loc}': {err.message}")

    fm_name = parsed.frontmatter.get("name")
    fm_category = parsed.frontmatter.get("category")

    if fm_name != parsed.slug:
        result.errors.append(f"Frontmatter name '{fm_name}' must match directory name '{parsed.slug}'")
    if fm_category != parsed.category_dir:
        result.errors.append(f"Frontmatter category '{fm_category}' must match parent folder '{parsed.category_dir}'")
    if fm_category not in categories:
        result.errors.append(f"Category '{fm_category}' is not registered in registry/categories.json")

    if not (skill_dir / "README.md").is_file():
        result.errors.append("Missing required documentation file: README.md")

    headings = set(extract_h2_headings(parsed.body))
    for section in REQUIRED_H2_SECTIONS:
        if section not in headings:
            result.errors.append(f"SKILL.md is missing required section: '## {section}'")

    for doc_name in ("SKILL.md", "README.md"):
        doc_path = skill_dir / doc_name
        if doc_path.is_file():
            for rel_link in extract_relative_links(doc_path.read_text(encoding="utf-8")):
                target_path = skill_dir / rel_link
                if not is_within_directory(skill_dir, target_path):
                    result.errors.append(f"Relative link escapes skill directory in {doc_name}: '{rel_link}'")
                elif not target_path.exists():
                    result.errors.append(f"Broken relative link in {doc_name}: '{rel_link}'")

    result.estimated_tokens = estimate_tokens(parsed.raw_text)
    if result.estimated_tokens > MAX_SKILL_TOKENS_FAIL:
        result.errors.append(
            f"SKILL.md exceeds hard token limit ({result.estimated_tokens} > {MAX_SKILL_TOKENS_FAIL}). Move details to references/."
        )
    elif result.estimated_tokens > MAX_SKILL_TOKENS_WARN:
        result.warnings.append(
            f"SKILL.md is approaching token budget ({result.estimated_tokens} > {MAX_SKILL_TOKENS_WARN}). Consider offloading details to references/."
        )

    _validate_eval_cases(skill_dir, str(fm_name or parsed.slug), result.errors)
    _scan_security_and_placeholders(skill_dir, result.errors)

    return result


def validate_all(
    skill_dirs: list[Path],
    schemas_dir: Path = SCHEMAS_DIR,
    registry_dir: Path = REGISTRY_DIR,
) -> list[ValidationResult]:
    """Validate a list of skill directories and return their results."""
    schema = load_json(schemas_dir / "skill-metadata.schema.json")
    validator = Draft202012Validator(schema)
    categories = load_categories(registry_dir)
    return [validate_skill(path, validator, categories) for path in skill_dirs]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate AI skills in the repository.")
    parser.add_argument("--skill", help="Optional path to a single skill directory.")
    args = parser.parse_args(argv)

    if args.skill:
        target = Path(args.skill).resolve()
        if not target.is_dir():
            print(f"Error: skill directory not found: {target}", file=sys.stderr)
            return 1
        targets = [target]
    else:
        targets = discover_skill_dirs(SKILLS_DIR)

    if not targets:
        print("Error: no skill directories found under skills/", file=sys.stderr)
        return 1

    results = validate_all(targets)
    failures = 0
    for res in results:
        rel = res.skill_path
        status = "PASS" if res.ok else "FAIL"
        print(f"[{status}] {rel} (~{res.estimated_tokens} tokens)")
        for warn in res.warnings:
            print(f"  WARN: {warn}")
        for err in res.errors:
            print(f"  ERROR: {err}")
        if not res.ok:
            failures += 1

    print(f"\nValidated {len(results)} skill(s): {len(results) - failures} passed, {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
