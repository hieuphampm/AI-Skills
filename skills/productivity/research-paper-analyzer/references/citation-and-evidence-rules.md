# Citation & Evidence Traceability Rules

Evidence traceability is the highest-priority requirement of `research-paper-analyzer`.

---

## 1. Standard 12-Field Citation Structure

Track every critical claim and numerical result with these fields:

| Field | Description |
| :--- | :--- |
| **Finding ID** | Unique evidence identifier (e.g., `E01`, `E02`) |
| **Finding** | Extracted research finding |
| **Numerical value** | Exact reported value (or `N/A` for qualitative claims) |
| **Unit** | Original measurement unit / scale |
| **Source paper** | Paper title or short identifier |
| **Section** | Original paper section name/number |
| **Page** | Printed page number when available |
| **PDF page** | Physical PDF viewer page index when useful |
| **Table/Figure** | Relevant table or figure identifier |
| **Evidence quotation** | Short verbatim quotation from the paper |
| **Citation** | Academic citation (APA 7th edition by default) |
| **Verification status** | `Verified`, `Partially verified`, or `Unverified` |

---

## 2. Mandatory Citation Rules

1. Always prioritize the original research paper over secondary summaries.
2. Never fabricate authors, publication years, DOIs, or page numbers.
3. Explicitly distinguish **printed page numbers** from **PDF viewer page indices**.
4. Provide Section and Table/Figure identifiers whenever possible.
5. Use short verbatim quotations to support key findings and keep quotes faithful to the original text.
6. Use **APA 7th edition** by default unless the user requests another style.
7. Include DOI links only when directly verified in the accessible document.
8. Distinguish references *cited by the paper* from papers *directly analyzed*.
9. Clearly identify missing or inaccessible source information.
10. If a precise page number cannot be established, cite Section or Table/Figure instead—never guess.

---

## 3. Table & Figure Inspection Rules

For each relevant table or figure, record:
- Table/Figure number and exact title/caption.
- Variables, indicators, units, measurement scales, and comparison groups.
- Exact numerical results (for tables) and corresponding text discussion.
- **Chart approximation rule**: Never infer exact numbers from a plot/chart if unreadable; label chart-derived estimates explicitly as **approximate**.
- **Inaccessible visuals**: If tables, figures, or supplements cannot be inspected, report *"Not found in the accessible document"* or *"Unable to verify from the original source."*

---

## 4. Mandatory Anti-Hallucination Disclosures

When information is missing or unverifiable, state explicitly:
- `"Not reported in the paper."`
- `"Not found in the accessible document."`
- `"Unable to verify from the original source."`
- `"The available evidence is insufficient to establish this claim."`
