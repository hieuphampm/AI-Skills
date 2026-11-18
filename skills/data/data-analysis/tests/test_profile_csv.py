"""Unit tests for skills/data/data-analysis/scripts/profile_csv.py."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "profile_csv.py"
SPEC = importlib.util.spec_from_file_location("profile_csv", SCRIPT_PATH)
assert SPEC and SPEC.loader
profile_csv_mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(profile_csv_mod)


class TestProfileCsv(unittest.TestCase):
    def _write_csv(self, content: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        tmp.write(content)
        tmp.close()
        self.addCleanup(lambda p=Path(tmp.name): p.unlink(missing_ok=True))
        return Path(tmp.name)

    def test_profiles_numeric_categorical_missing_and_duplicates(self) -> None:
        csv_path = self._write_csv(
            "id,amount,region\n"
            "1,10.0,us\n"
            "1,10.0,us\n"
            "2,12.0,us\n"
            "3,11.0,eu\n"
            "4,10.5,eu\n"
            "5,1000.0,apac\n"
            "6,NA,\n"
        )
        result = profile_csv_mod.profile_csv(csv_path)
        self.assertEqual(result["row_count"], 7)
        self.assertEqual(result["column_count"], 3)
        self.assertEqual(result["duplicate_row_count"], 1)
        self.assertEqual(result["malformed_row_count"], 0)

        amount_col = result["columns"][1]
        self.assertEqual(amount_col["inferred_type"], "numeric")
        self.assertEqual(amount_col["missing_count"], 1)
        self.assertGreaterEqual(amount_col["numeric_summary"]["iqr_outlier_count"], 1)

        region_col = result["columns"][2]
        self.assertEqual(region_col["inferred_type"], "categorical")
        self.assertEqual(region_col["missing_count"], 1)

    def test_header_only_csv(self) -> None:
        csv_path = self._write_csv("col_a,col_b\n")
        result = profile_csv_mod.profile_csv(csv_path)
        self.assertEqual(result["row_count"], 0)
        self.assertEqual(result["columns"][0]["inferred_type"], "empty")

    def test_empty_file_raises_value_error(self) -> None:
        csv_path = self._write_csv("")
        with self.assertRaises(ValueError):
            profile_csv_mod.profile_csv(csv_path)

    def test_missing_file_raises_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            profile_csv_mod.profile_csv(Path("nonexistent_file_12345.csv"))


if __name__ == "__main__":
    unittest.main()
