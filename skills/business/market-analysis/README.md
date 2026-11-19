# Market Analysis

Human-facing overview and usage guide for the `market-analysis` skill.

## Overview

`market-analysis` produces a structured, source-cited analysis of a stock, sector, or overall market. It combines three lenses:

1. **Fundamental** — valuation, financial health, competitive position.
2. **Technical** — trend, support/resistance, momentum.
3. **Risk** — top risks, catalysts, and a confidence level.

Every report ends with a clear disclaimer that the output is **informational analysis, not investment advice**.

## Directory Structure

- `SKILL.md` — Agent-facing specification, metadata, and execution instructions.
- `README.md` — Human-facing documentation and integration notes.
- `references/analysis-framework.md` — Frameworks for fundamental, technical, and risk analysis.
- `assets/analysis-report-template.md` — Output template for the analysis report.
- `examples/nvda-analysis.md` — End-to-end ticker-to-report walkthrough.
- `tests/eval-cases.json` — Trigger and behavioral evaluation cases.

## Data Sources

The skill uses `web_search` and `http_fetch` to gather current market data. Provide a `market_data` file (price history or financials) for reproducible, offline analysis.

## Disclaimer

This skill is for research and education. It does not provide personalized investment advice, and it never guarantees returns.

## Quick Test

Validate structure and metadata:

```bash
python scripts/validate_skills.py --skill skills/business/market-analysis
```
