#!/usr/bin/env python3
"""Detect duplicate skill names and semantically overlapping descriptions/tags."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from skill_utils import SKILLS_DIR, discover_skill_dirs, parse_skill_markdown

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "into", "is", "it", "of", "on", "or", "that", "the", "this", "to", "use",
    "when", "with", "your",
}
TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> set[str]:
    return {tok for tok in TOKEN_RE.findall(text.lower()) if tok not in STOPWORDS and len(tok) > 1}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_duplicates(
    skill_dirs: list[Path],
    similarity_threshold: float = 0.55,
) -> tuple[list[str], list[str]]:
    """Return (hard_errors, overlap_warnings) across discovered skills."""
    errors: list[str] = []
    warnings: list[str] = []

    by_name: dict[str, list[Path]] = defaultdict(list)
    profiles: list[tuple[str, str, set[str]]] = []

    for skill_dir in skill_dirs:
        parsed = parse_skill_markdown(skill_dir)
        fm = parsed.frontmatter
        raw_name = fm.get("name")
        raw_category = fm.get("category")
        if not raw_name or not raw_category:
            errors.append(f"Missing required 'name' or 'category' in {skill_dir / 'SKILL.md'}")
            continue
        name = str(raw_name)
        skill_id = f"{raw_category}/{name}"
        by_name[name].append(skill_dir)

        desc_tokens = _tokenize(str(fm.get("description") or ""))
        tag_tokens = {str(t).lower() for t in (fm.get("tags") or [])}
        activation = fm.get("activation") or {}
        triggers = activation.get("triggers") if isinstance(activation, dict) else []
        trigger_text = " ".join(str(t) for t in (triggers or []))
        combined_tokens = desc_tokens | tag_tokens | _tokenize(trigger_text)
        profiles.append((skill_id, name, combined_tokens))

    for name, paths in sorted(by_name.items()):
        if len(paths) > 1:
            joined = ", ".join(str(p) for p in paths)
            errors.append(f"Duplicate skill name '{name}' found in: {joined}")

    for i in range(len(profiles)):
        id_a, _, tokens_a = profiles[i]
        for j in range(i + 1, len(profiles)):
            id_b, _, tokens_b = profiles[j]
            sim = _jaccard(tokens_a, tokens_b)
            if sim >= similarity_threshold:
                warnings.append(
                    f"High overlap ({sim:.2f} >= {similarity_threshold:.2f}) between '{id_a}' and '{id_b}'"
                )

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect duplicate or overlapping AI skills.")
    parser.add_argument("--threshold", type=float, default=0.55, help="Jaccard overlap warning threshold (0-1).")
    args = parser.parse_args(argv)

    skill_dirs = discover_skill_dirs(SKILLS_DIR)
    errors, warnings = find_duplicates(skill_dirs, similarity_threshold=args.threshold)

    for warn in warnings:
        print(f"WARN: {warn}")
    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)

    if not errors and not warnings:
        print(f"No duplicate names or overlapping skills detected across {len(skill_dirs)} skill(s).")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
