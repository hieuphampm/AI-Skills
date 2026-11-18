"""Integration tests for repository automation scripts."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from create_skill import create_skill  # noqa: E402
from detect_duplicates import find_duplicates  # noqa: E402
from generate_index import build_index, validate_index_payload  # noqa: E402
from skill_utils import REGISTRY_DIR, SCHEMAS_DIR, SKILLS_DIR, TEMPLATES_DIR, load_categories, load_json  # noqa: E402
from validate_skills import validate_skill  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402


class TestAutomationScripts(unittest.TestCase):
    def test_create_skill_scaffolds_valid_structure(self) -> None:
        tmp_skills = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(tmp_skills, ignore_errors=True))

        created = create_skill(
            name="api-design",
            category="development",
            description="Designs consistent REST and GraphQL API contracts with OpenAPI schemas and error standards.",
            author="Test Engineer",
            skills_dir=tmp_skills,
            templates_dir=TEMPLATES_DIR,
            registry_dir=REGISTRY_DIR,
            with_references=True,
            with_scripts=True,
            with_assets=True,
        )

        self.assertTrue((created / "SKILL.md").is_file())
        self.assertTrue((created / "README.md").is_file())
        self.assertTrue((created / "examples" / "example-usage.md").is_file())
        self.assertTrue((created / "tests" / "eval-cases.json").is_file())
        self.assertTrue((created / "references" / "domain-guide.md").is_file())
        self.assertTrue((created / "scripts" / "run_helper.py").is_file())
        self.assertTrue((created / "assets" / "output-template.md").is_file())

        schema = load_json(SCHEMAS_DIR / "skill-metadata.schema.json")
        res = validate_skill(created, Draft202012Validator(schema), load_categories(REGISTRY_DIR))
        self.assertTrue(res.ok, msg=f"Scaffolded skill failed validation: {res.errors}")

    def test_detect_duplicates_catches_identical_skill_names(self) -> None:
        tmp_skills = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(tmp_skills, ignore_errors=True))

        shutil.copytree(SKILLS_DIR / "development" / "code-review", tmp_skills / "development" / "code-review")
        dup_target = tmp_skills / "ai-engineering" / "code-review"
        shutil.copytree(SKILLS_DIR / "development" / "code-review", dup_target)

        errors, _ = find_duplicates([tmp_skills / "development" / "code-review", dup_target])
        self.assertEqual(len(errors), 1)
        self.assertIn("Duplicate skill name 'code-review'", errors[0])

    def test_build_index_matches_schema(self) -> None:
        payload = build_index()
        validate_index_payload(payload)
        self.assertEqual(payload["skill_count"], len(payload["skills"]))
        self.assertGreaterEqual(payload["skill_count"], 4)

    def test_create_skill_handles_colons_and_quotes_safely(self) -> None:
        tmp_skills = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(tmp_skills, ignore_errors=True))

        created = create_skill(
            name="log-triage",
            category="development",
            title='Log Triage: "Fast" Mode',
            description='Analyzes service logs: detects "5xx" spikes, timeouts, and retry storms reliably.',
            author='Platform "Core" Team',
            skills_dir=tmp_skills,
            templates_dir=TEMPLATES_DIR,
            registry_dir=REGISTRY_DIR,
        )

        schema = load_json(SCHEMAS_DIR / "skill-metadata.schema.json")
        res = validate_skill(created, Draft202012Validator(schema), load_categories(REGISTRY_DIR))
        self.assertTrue(res.ok, msg=f"Special-char scaffold failed validation: {res.errors}")

    def test_detect_duplicates_and_index_tolerate_null_optional_fields(self) -> None:
        tmp_root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(tmp_root, ignore_errors=True))
        skill_dir = tmp_root / "development" / "code-review"
        shutil.copytree(SKILLS_DIR / "development" / "code-review", skill_dir)

        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        text = text.split("activation:")[0] + "activation: null\nsecurity: null\n---\n" + text.split("\n---\n", 1)[1]
        skill_md.write_text(text, encoding="utf-8")

        errors, _ = find_duplicates([skill_dir])
        self.assertEqual(errors, [])
        payload = build_index(skills_dir=tmp_root, repo_root=tmp_root)
        self.assertEqual(payload["skills"][0]["risk_level"], "low")


if __name__ == "__main__":
    unittest.main()
