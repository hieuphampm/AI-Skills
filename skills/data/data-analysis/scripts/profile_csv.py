#!/usr/bin/env python3
"""Deterministic, zero-dependency CSV profiler for the data-analysis skill."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

MAX_FILE_BYTES = 50 * 1024 * 1024  # 50 MB safety cap
MISSING_TOKENS = {"", "na", "n/a", "null", "none", "nan"}


def _parse_float(value: str) -> float | None:
    """Return finite float if value parses cleanly, otherwise None."""
    cleaned = value.strip().replace(",", "")
    if not cleaned:
        return None
    try:
        parsed = float(cleaned)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def _percentile(sorted_vals: list[float], pct: float) -> float:
    """Compute linear-interpolated percentile on an already-sorted non-empty list."""
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    pos = (len(sorted_vals) - 1) * pct
    low = math.floor(pos)
    high = math.ceil(pos)
    if low == high:
        return sorted_vals[low]
    weight = pos - low
    return sorted_vals[low] * (1.0 - weight) + sorted_vals[high] * weight


def _profile_column(name: str, raw_values: list[str]) -> dict[str, Any]:
    """Compute missingness, inferred type, and distribution summary for one column."""
    total = len(raw_values)
    non_missing = [v.strip() for v in raw_values if v.strip().lower() not in MISSING_TOKENS]
    missing_count = total - len(non_missing)

    numeric_vals: list[float] = []
    for val in non_missing:
        parsed = _parse_float(val)
        if parsed is None:
            numeric_vals = []
            break
        numeric_vals.append(parsed)

    is_numeric = bool(non_missing) and len(numeric_vals) == len(non_missing)
    profile: dict[str, Any] = {
        "name": name,
        "inferred_type": "numeric" if is_numeric else ("empty" if not non_missing else "categorical"),
        "non_null_count": len(non_missing),
        "missing_count": missing_count,
        "missing_pct": round((missing_count / total) * 100, 2) if total else 0.0,
        "unique_count": len(set(non_missing)),
    }

    if is_numeric:
        sorted_vals = sorted(numeric_vals)
        q1 = _percentile(sorted_vals, 0.25)
        q3 = _percentile(sorted_vals, 0.75)
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        outliers = sum(1 for x in sorted_vals if x < lower_fence or x > upper_fence)
        profile["numeric_summary"] = {
            "min": sorted_vals[0],
            "q1": round(q1, 4),
            "median": round(statistics.median(sorted_vals), 4),
            "mean": round(statistics.mean(sorted_vals), 4),
            "q3": round(q3, 4),
            "max": sorted_vals[-1],
            "stdev": round(statistics.stdev(sorted_vals), 4) if len(sorted_vals) > 1 else 0.0,
            "iqr_outlier_count": outliers,
        }
    else:
        counts = Counter(non_missing)
        profile["top_values"] = [
            {"value": value, "count": count} for value, count in counts.most_common(5)
        ]

    return profile


def profile_csv(path: Path, max_rows: int = 200_000) -> dict[str, Any]:
    """Profile a CSV file and return structured quality & summary statistics."""
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError(f"File exceeds {MAX_FILE_BYTES // (1024 * 1024)} MB safety limit: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            headers = next(reader)
        except StopIteration as exc:
            raise ValueError(f"CSV file is empty: {path}") from exc

        headers = [h.strip() or f"column_{idx}" for idx, h in enumerate(headers)]
        columns: list[list[str]] = [[] for _ in headers]
        seen_rows: Counter[tuple[str, ...]] = Counter()
        row_count = 0
        malformed_rows = 0

        for row in reader:
            if row_count >= max_rows:
                break
            row_count += 1
            if len(row) != len(headers):
                malformed_rows += 1
                padded = (row + [""] * len(headers))[: len(headers)]
            else:
                padded = row
            seen_rows[tuple(padded)] += 1
            for idx, cell in enumerate(padded):
                columns[idx].append(cell)

    duplicate_rows = sum(count - 1 for count in seen_rows.values() if count > 1)
    return {
        "file": str(path),
        "row_count": row_count,
        "column_count": len(headers),
        "duplicate_row_count": duplicate_rows,
        "malformed_row_count": malformed_rows,
        "truncated_at_max_rows": row_count >= max_rows,
        "columns": [_profile_column(name, vals) for name, vals in zip(headers, columns)],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Profile a CSV dataset deterministically.")
    parser.add_argument("--input", required=True, help="Path to CSV file.")
    parser.add_argument("--max-rows", type=int, default=200_000, help="Maximum rows to inspect.")
    args = parser.parse_args(argv)

    try:
        result = profile_csv(Path(args.input), max_rows=args.max_rows)
    except (FileNotFoundError, ValueError, UnicodeDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
