# Methodology & Numerical Accuracy Protocol

Consult this reference during Steps 3–8 of `research-paper-analyzer`.

---

## 1. Academic Paper & Methodology Extraction Checklist

### 1.1 Paper Understanding
- Title and authors; publication year and journal/conference; DOI and publication details.
- Abstract and keywords; background and motivation; research questions, objectives, and hypotheses.
- Research gaps; theoretical/conceptual frameworks; contributions; main findings and conclusions.

### 1.2 Research Methodology
- Research design; study population; sample size (`N`); sampling techniques; data collection methods.
- Independent variables, dependent variables, control variables, measurement instruments.
- Experimental procedures, statistical methods, software, and analytical tools.
- Assess explicitly whether the selected methodology appropriately addresses the research questions.

### 1.3 Quantitative Data Categories
Extract exact reported values with original value, unit, statistical notation, sample size, comparison condition, model/variable, and measurement context:
- **Descriptive**: Sample size (`N`), mean, median, standard deviation (SD), variance, min/max, frequency, percentage.
- **Inferential**: Correlation coefficients, regression coefficients, standard errors (SE), confidence intervals (CI), p-values, t-statistics, F-statistics, chi-square statistics, degrees of freedom, effect sizes.
- **ML & Experimental**: Accuracy, precision, recall, F1-score, AUC-ROC, RMSE, MAE, R-squared, training vs. testing performance.
- **Domain-specific**: Any additional discipline-specific measurements.

---

## 2. Numerical Accuracy Protocol (10 Steps)

For every extracted numerical value:
1. Locate the original statement, table, or figure.
2. Read the surrounding context.
3. Identify the metric and its definition.
4. Preserve the original value and notation.
5. Identify the unit and denominator.
6. Record the sample size when available.
7. Verify the comparison group or experimental condition.
8. Record the source location.
9. Cross-check against other occurrences in the paper.
10. Mark the verification status (`VERIFIED`, `PARTIALLY VERIFIED`, or `UNVERIFIED`).

### Critical Statistical Distinctions (Never Confuse)
1. **Percentage** vs. **Percentage points**
2. **Mean** vs. **Median**
3. **Standard deviation (SD)** vs. **Standard error (SE)**
4. **Correlation** vs. **Causation**
5. **Statistical significance** vs. **Practical significance**
6. **Confidence intervals** vs. **Prediction intervals**
7. **Relative improvement** vs. **Absolute improvement**
8. **Training performance** vs. **Testing performance**
9. **Author-reported results** vs. **Independently calculated results**

If you compute a derived figure, label it explicitly as **`AI-calculated`** and show the calculation method. Never silently alter authors' reported values.

---

## 3. Critical Research Appraisal

Evaluate:
- Research design appropriateness, sample representativeness, sample size adequacy.
- Measurement validity and reliability, selection bias, confounding variables, statistical assumptions.
- Internal validity, external validity, reproducibility, generalizability.
- Conflicts of interest, funding sources, and potential bias.

Always separate into three distinct buckets (never attribute analyst critiques to the authors):
1. Limitations explicitly acknowledged by the authors.
2. Additional methodological limitations identified through critical analysis.
3. Issues that cannot be evaluated from the available information.

---

## 4. Multi-Paper Comparison Protocol

When multiple papers are provided, build a comparative evidence matrix comparing:
- Research objectives, contexts, designs, sample sizes, variables, analytical methods, quantitative findings, conclusions, limitations, and research gaps.

Rules:
- Clearly distinguish findings per paper; never combine statistics across studies without individual source attribution.
- Explicitly highlight consistent findings, contradictory findings, design differences, measurement differences, and candidate explanations for discrepancies.
- Do not perform a meta-analysis unless sufficient comparable data and appropriate statistical methods exist.

---

## 5. Final Quality Checklist (Verify Before Submission)

- [ ] Bibliographic information is accurate.
- [ ] Research objectives are correctly identified.
- [ ] Methodology is accurately described.
- [ ] Important numerical values match the original paper.
- [ ] Units and statistical notation are preserved.
- [ ] Sample sizes are correctly reported.
- [ ] Tables and figures are correctly identified.
- [ ] Important claims have traceable evidence.
- [ ] Page numbers are not fabricated.
- [ ] Quotations match the original document.
- [ ] Author-reported limitations are distinguished from AI assessments.
- [ ] Unverified information is clearly disclosed.
- [ ] References are correctly formatted.
