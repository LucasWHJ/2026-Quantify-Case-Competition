# Data access and provenance

## Organizer inputs

The analysis uses the combined **Exhibits 2026 Quantify Case Study.xlsx** supplied for the Quantify Case Competition 2026:

- **Exhibit A:** five lines of business over 2021–2025. Source monetary amounts are CAD thousands. Exposure and claim counts are not monetary values.
- **Exhibit B:** 135 external AI incidents with industry, failure type, oversight flag and estimated insured loss in CAD. It is not TSI's historical claims book.
- **Exhibit C:** strategic context. It does not supply the exposure denominator needed to estimate insured claim frequency.

The original PDF and workbooks are not bundled because redistribution authorization has not been established. Obtain an authorized copy from the organizer or your own competition materials. No public download link is invented.

## Local setup

Copy the combined workbook to `data/raw/exhibits.xlsx`. Alternatively set `QUANTIFY_WORKBOOK` to its local path. `data/raw/` is ignored by Git. The separate Exhibit B workbook is unnecessary because it repeats the combined workbook's incident data.

Source coordinates: Exhibit A uses line anchors A3, A13, A23, A33 and A43. Years occupy columns B:F; exposure is anchor+2, premium +4, claim count +5, incurred losses +6, operating expenses +8. Exhibit B headers are A2:G2 and observations A3:G137.

## Public derived outputs

`processed/` contains aggregate analytical outputs, not incident descriptions or row-level records. `key_results.json` records a SHA-256 digest of the workbook used for this revision. Exact source verification requires the same authorized workbook; different formatting may alter its file hash without changing values.

| File | Measure |
|---|---|
| `company_annual.csv` | Amount-weighted company financial results |
| `line_metrics.csv` | Calculated rates, severities and margins by line and year |
| `severity_by_failure.csv` | Incident severity summaries by failure mechanism |
| `severity_by_oversight.csv` | Unadjusted oversight groups |
| `severity_by_failure_and_oversight.csv` | Mechanism-specific oversight comparisons |
| `candidate_subset.csv` | Supervised hallucination/misinformation subgroup before coverage screening |
| `anova_order_sensitivity.csv` | Sequential sums of squares in two variable orders |
| `unique_model_contributions.csv` | Extra sum of squares after controlling all other modeled factors |
| `failure_industry_counts.csv` | Cross-tabulation exposing mechanism/industry overlap |
| `key_results.json` | Core figures, model specification and labeled pilot assumptions |

No raw AIID/CSET severe-harm extract or DAIL litigation snapshot was supplied. Their historical percentages cannot be independently reproduced from this repository and are excluded from its quantitative conclusions.
