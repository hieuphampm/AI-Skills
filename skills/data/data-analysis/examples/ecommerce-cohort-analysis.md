# Example: E-Commerce Orders Quality & Revenue Audit

## Input
- `dataset_path`: `orders_q3.csv`
- `business_question`: `"Summarize order value distribution and flag data quality issues before forecasting Q4 revenue."`

## Profiler Output Summary (`profile_csv.py`)
```json
{
  "file": "orders_q3.csv",
  "row_count": 1200,
  "column_count": 4,
  "duplicate_row_count": 18,
  "malformed_row_count": 0,
  "columns": [
    { "name": "order_id", "inferred_type": "categorical", "missing_pct": 0.0, "unique_count": 1182 },
    { "name": "order_total", "inferred_type": "numeric", "missing_pct": 1.5, "numeric_summary": { "min": -25.0, "q1": 34.0, "median": 58.0, "mean": 112.4, "q3": 96.0, "max": 4850.0, "iqr_outlier_count": 42 } },
    { "name": "channel", "inferred_type": "categorical", "missing_pct": 24.0, "top_values": [{ "value": "web", "count": 610 }, { "value": "mobile", "count": 302 }] }
  ]
}
```

## Expected Output (`analysis_report`)

# Exploratory Data Analysis Report

## 1. Dataset Overview
- **Source File**: `orders_q3.csv`
- **Dimensions**: `1,200` rows × `4` columns
- **Duplicate Rows**: `18` | **Malformed Rows**: `0`

## 2. Data Quality Findings
| Column | Type | Missing (%) | Unique | Quality Notes |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | `categorical` | `0.0%` | `1,182` | 18 duplicate rows inflate raw row count |
| `order_total` | `numeric` | `1.5%` | — | Right-skewed (`mean` 112.4 vs `median` 58.0); contains negative value (`-25.0`) and 42 IQR outliers |
| `channel` | `categorical` | `24.0%` | `2` | Exceeds 20% missingness threshold; channel attribution is unreliable |

## 3. Key Quantitative Findings
- **Order Value Skewness**: Typical order value is `$58.00` (median, IQR `$34.00–$96.00`), whereas mean order value (`$112.40`) is nearly double due to high-value outliers up to `$4,850.00`.
- **Negative Totals**: `min = -25.0` indicates refunds or credit adjustments are mixed into `orders_q3.csv`.

## 4. Limitations & Next Steps
- Deduplicate `order_id` (removing the 18 exact duplicates) and separate refunds (`order_total < 0`) before forecasting Q4 gross revenue.
- Audit tracking instrumentation for `channel` (`24.0%` missing) before attributing revenue by acquisition channel.
