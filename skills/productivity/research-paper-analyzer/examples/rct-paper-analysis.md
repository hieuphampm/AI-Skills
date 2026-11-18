# Example: Single-Paper Analysis (Clinical NLP Retrieval Study)

## Input
- `paper_source`: Accessible excerpt/PDF of *Chen et al. (2025), "Retrieval-Augmented Clinical Summarization in Outpatient Primary Care: A Multi-Site Randomized Controlled Trial"*, Journal of Biomedical Informatics, pp. 104–112 (PDF pp. 1–9), `DOI: 10.1016/j.jbi.2025.04.012`.
- `analysis_task`: `"Full research paper analysis with quantitative extraction and verification status."`

## Excerpted Expected Output (`analysis_report`)

### A. Paper Information
- **Title**: Retrieval-Augmented Clinical Summarization in Outpatient Primary Care: A Multi-Site Randomized Controlled Trial
- **Authors**: Chen, L., Patel, R., & Gomez, M.
- **Publication year**: 2025
- **Journal/conference**: *Journal of Biomedical Informatics*
- **DOI**: `https://doi.org/10.1016/j.jbi.2025.04.012`
- **Research domain**: Clinical Natural Language Processing / Health Informatics
- **Citation format**: APA 7th edition

### E. Key Quantitative Findings

| Metric | Reported value | Unit/context | Source |
| :--- | :--- | :--- | :--- |
| Sample size | `N = 240` | Outpatient encounters (`n = 120` intervention, `n = 120` control across 3 clinics) | Section 2.2, Printed p. 106 (PDF p. 3) |
| Documentation time reduction | `-2.4` minutes (`mean = 4.1` vs `6.5` min, `SD = 1.2` vs `1.6`) | Mean clinician charting time per encounter | Table 2, Printed p. 108 (PDF p. 5) |
| Primary statistical test | `t(238) = -13.15, p < 0.001, d = 1.70` | Independent-samples t-test, Cohen's `d` effect size | Section 3.1, Printed p. 108 (PDF p. 5) |
| Hallucination rate | `1.7%` vs `4.2%` (`2/120` vs `5/120`, `p = 0.45`) | Unsupported clinical claims audited by blinded physicians (`2.5` percentage-point difference; *AI-calculated*: `4.2 - 1.7 = 2.5` pp) | Table 3, Printed p. 109 (PDF p. 6) |
| Long-term 6-month retention | Not reported in the paper. | Follow-up beyond immediate encounter not measured | Section 4.2, Printed p. 110 (PDF p. 7) |

### G. Evidence and Citation Table

| ID | Finding | Evidence | Location | Status |
| :--- | :--- | :--- | :--- | :--- |
| `E01` | Intervention reduced mean encounter charting time from `6.5` to `4.1` minutes (`N = 240`). | `"Mean charting duration was 4.1 min (SD = 1.2) in the RAG arm versus 6.5 min (SD = 1.6) in usual care (p < 0.001)."` | Section 3.1, Printed p. 108 (PDF p. 5), Table 2 | `Verified` |
| `E02` | Difference in unsupported claim rate (`1.7%` vs `4.2%`) was not statistically significant. | `"Unsupported claim incidence did not differ significantly between arms (2/120 vs. 5/120, Fisher's exact p = 0.45)."` | Section 3.2, Printed p. 109 (PDF p. 6), Table 3 | `Verified` |
| `E03` | Subgroup breakdown by clinic EHR vendor. | Appendix S2 referenced in text, but supplementary file was not included in accessible PDF. | Section 2.1, Printed p. 105 (PDF p. 2) | `Unverified` *(Unable to verify from the original source)* |

### H. Critical Evaluation (Excerpt)
- **Author-acknowledged limitations**: Short study window (4 weeks), single regional health network, and lack of 6-month longitudinal follow-up (Section 4.2, Printed p. 110).
- **Analyst-identified methodological concerns**: Physicians were not blinded to using the summarization tool during encounters, introducing potential Hawthorne/novelty bias; hallucination comparison (`2` vs `5` events) is statistically underpowered (`p = 0.45`).
- **Unevaluable aspects**: Clinic-level heterogeneity cannot be assessed because Appendix S2 is not in the accessible document.

### K. References
Chen, L., Patel, R., & Gomez, M. (2025). Retrieval-augmented clinical summarization in outpatient primary care: A multi-site randomized controlled trial. *Journal of Biomedical Informatics*, 104–112. https://doi.org/10.1016/j.jbi.2025.04.012
