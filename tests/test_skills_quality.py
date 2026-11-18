"""Quality assurance and registry consistency checks for shipped skills."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from generate_index import build_index  # noqa: E402
from skill_utils import REGISTRY_DIR, SKILLS_DIR, discover_skill_dirs, estimate_tokens, parse_skill_markdown  # noqa: E402


class TestSkillsQuality(unittest.TestCase):
    def test_registry_index_is_synchronized(self) -> None:
        index_path = REGISTRY_DIR / "skills-index.json"
        self.assertTrue(index_path.is_file(), "registry/skills-index.json must exist")
        on_disk = json.loads(index_path.read_text(encoding="utf-8"))
        generated = build_index()
        self.assertEqual(on_disk, generated, "Run python scripts/generate_index.py to sync registry/skills-index.json")

    def test_every_skill_has_examples_and_eval_coverage(self) -> None:
        for skill_dir in discover_skill_dirs(SKILLS_DIR):
            parsed = parse_skill_markdown(skill_dir)
            self.assertLessEqual(
                estimate_tokens(parsed.raw_text),
                2000,
                f"{skill_dir.name}/SKILL.md should stay under 2000 tokens for progressive disclosure efficiency",
            )
            examples_dir = skill_dir / "examples"
            self.assertTrue(examples_dir.is_dir() and any(examples_dir.glob("*.md")), f"{skill_dir.name} needs >=1 example")

            eval_data = json.loads((skill_dir / "tests" / "eval-cases.json").read_text(encoding="utf-8"))
            case_types = {case["type"] for case in eval_data["cases"]}
            self.assertIn("positive_trigger", case_types)
            self.assertIn("negative_trigger", case_types)
            self.assertTrue("edge_case" in case_types or "security" in case_types)


if __name__ == "__main__":
    unittest.main()
