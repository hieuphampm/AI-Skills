"""Discovers and runs unit test suites embedded inside individual skills."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[1] / "skills"


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: str) -> unittest.TestSuite:
    suite = unittest.TestSuite()
    for test_file in sorted(SKILLS_ROOT.glob("*/*/tests/test_*.py")):
        module_name = f"skill_test_{test_file.parents[1].name.replace('-', '_')}_{test_file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, test_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            suite.addTests(loader.loadTestsFromModule(module))
    return suite
