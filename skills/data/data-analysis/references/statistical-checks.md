# Statistical & Data Quality Checks

Consult this reference during Step 3 and Step 4 of `data-analysis`.

## 1. Data Quality Thresholds
- **Missingness < 5%**: Usually safe for complete-case analysis if missingness is random; still document it.
- **Missingness 5%–20%**: Investigate whether missingness concentrates in a specific segment (non-random missingness).
- **Missingness > 20%**: Treat conclusions involving this column as tentative unless missingness mechanism is explained.
- **Duplicate rows > 0**: Verify whether duplicates represent valid repeated events or ingestion bugs before aggregating sums/counts.

## 2. Summary Statistic Selection
- **Symmetric / low-skew numeric data**: Mean and standard deviation are informative.
- **Skewed numeric data** (revenue, latency, order size) or high IQR outliers: Always highlight **median** and **IQR (`Q3 - Q1`)** alongside mean.

## 3. Analytical Guardrails
- **Simpson's Paradox**: Always verify key ratios across major segments (e.g., region, plan tier, device) before concluding an overall trend.
- **Correlation != Causation**: Label observational relationships as associations unless randomized/causal design exists.
- **Zero-row or tiny-sample segments (`n < 30`)**: Flag wide uncertainty instead of reporting noisy percentages as stable trends.
