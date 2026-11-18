"""Tests for skill validation rules, security checks, and schema enforcement."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from skill_utils import REGISTRY_DIR, SCHEMAS_DIR, SKILLS_DIR, discover_skill_dirs, load_categories, load_json  # noqa: E402
from validate_skills import validate_all, validate_skill  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402


class TestSkillValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = load_json(SCHEMAS_DIR / "skill-metadata.schema.json")
        self.validator = Draft202012Validator(self.schema)
        self.categories = load_categories(REGISTRY_DIR)

    def _copy_valid_skill_to_temp(self) -> Path:
        tmp_root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(tmp_root, ignore_errors=True))
        target = tmp_root / "development" / "code-review"
        shutil.copytree(SKILLS_DIR / "development" / "code-review", target)
        return target

    def test_all_repository_skills_pass_validation(self) -> None:
        skill_dirs = discover_skill_dirs(SKILLS_DIR)
        self.assertGreaterEqual(len(skill_dirs), 3)
        results = validate_all(skill_dirs)
        for res in results:
            self.assertTrue(res.ok, msg=f"{res.skill_path} failed: {res.errors}")

    def test_rejects_mismatched_directory_and_name(self) -> None:
        skill_dir = self._copy_valid_skill_to_temp()
        renamed = skill_dir.parent / "different-slug"
        skill_dir.rename(renamed)
        res = validate_skill(renamed, self.validator, self.categories)
        self.assertFalse(res.ok)
        self.assertTrue(any("must match directory name" in err for err in res.errors))

    def test_rejects_broken_relative_link(self) -> None:
        skill_dir = self._copy_valid_skill_to_temp()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(skill_md.read_text(encoding="utf-8") + "\nSee [missing](references/nope.md).\n", encoding="utf-8")
        res = validate_skill(skill_dir, self.validator, self.categories)
        self.assertFalse(res.ok)
        self.assertTrue(any("Broken relative link" in err for err in res.errors))

    def test_rejects_unresolved_template_placeholder(self) -> None:
        skill_dir = self._copy_valid_skill_to_temp()
        readme = skill_dir / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\nTODO: {{SKILL_TITLE}}\n", encoding="utf-8")
        res = validate_skill(skill_dir, self.validator, self.categories)
        self.assertFalse(res.ok)
        self.assertTrue(any("Unresolved template placeholder" in err for err in res.errors))

    def test_rejects_hardcoded_secret_pattern(self) -> None:
        skill_dir = self._copy_valid_skill_to_temp()
        leak_file = skill_dir / "examples" / "python-api-review.md"
        leak_file.write_text("AKIAIOSFODNN7EXAMPLE\n", encoding="utf-8")
        res = validate_skill(skill_dir, self.validator, self.categories)
        self.assertFalse(res.ok)
        self.assertTrue(any("Potential hardcoded secret" in err for err in res.errors))

    def test_rejects_unsafe_subprocess_shell_true_in_scripts(self) -> None:
        skill_dir = self._copy_valid_skill_to_temp()
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "bad.py").write_text("import subprocess\nsubprocess.run('ls', shell=True)\n", encoding="utf-8")
        res = validate_skill(skill_dir, self.validator, self.categories)
        self.assertFalse(res.ok)
        self.assertTrue(any("Unsafe Python pattern" in err for err in res.errors))


if __name__ == "__main__":
    unittest.main()
