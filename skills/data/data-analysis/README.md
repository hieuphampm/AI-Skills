# Exploratory Data Analysis Skill

Audits CSV datasets deterministically using a zero-dependency Python profiler before generating data quality and statistical findings.

## What It Does

- Computes exact row/column counts, missingness rates, duplicate rows, and inferred types.
- Calculates numeric distributions (`min`, `max`, `mean`, `median`, `stdev`, `q1`, `q3`, IQR outlier count) and top categorical frequencies.
- Enforces statistical rigor (median/IQR for skewed data, correlation vs. causation disclaimers, PII redaction).

## Included Files

| File | Role |
| :--- | :--- |
| [SKILL.md](SKILL.md) | Agent workflow, guardrails, and output contract |
| [scripts/profile_csv.py](scripts/profile_csv.py) | Deterministic zero-dependency CSV profiler CLI |
| [references/statistical-checks.md](references/statistical-checks.md) | Data quality thresholds and statistical pitfalls |
| [assets/analysis-report-template.md](assets/analysis-report-template.md) | Standardized EDA report template |
| [examples/ecommerce-cohort-analysis.md](examples/ecommerce-cohort-analysis.md) | Worked e-commerce order analysis example |
| [tests/eval-cases.json](tests/eval-cases.json) | Agent trigger & edge-case evaluations |
| [tests/test_profile_csv.py](tests/test_profile_csv.py) | Automated unit tests for `profile_csv.py` |

## Quick Usage

Run the profiler directly:

```bash
python skills/data/data-analysis/scripts/profile_csv.py --input path/to/data.csv
```

Run unit tests:

```bash
python -m unittest skills/data/data-analysis/tests/test_profile_csv.py
```
