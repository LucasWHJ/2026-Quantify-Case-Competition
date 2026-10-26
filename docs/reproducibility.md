# Reproduction and validation

## Executed analysis

All three notebooks were executed from their first code cell through their last code cell without retained error outputs. The two historical analyses used the authorized source workbook identified by the SHA-256 digest in `data/processed/key_results.json`. The pilot notebook uses only its explicit assumptions.

Python: 3.12. Direct dependency versions are pinned in `requirements.txt`. The project uses NumPy linear algebra for its additive log-loss model and Matplotlib for the standalone figures. A temporary Jupyter kernelspec allows execution without installing a named kernel globally.

The public repository retains all notebook outputs and aggregate tables. Source-record recomputation requires the organizer workbook; no synthetic replacement is passed off as the original data. The public CI workflow runs the independent tests, regenerates charts from the aggregate tables, and executes the pilot notebook. It cannot recompute the raw-data notebooks without access to the workbook.

## Calculation checks

Seven unit tests check amount-weighted accounting, the frequency/severity identity, sequential attribution under correlated factors, pilot break-even and target-margin thresholds, deductible/limit boundaries, concentration-budget boundaries and invalid assumptions. Key case outputs were reconciled to the supplied workbook. Tests do not establish representativeness, causal effects or insurance pricing adequacy.

## Presentation checks

The presentation has 14 slides: 10 main slides including the cover, followed by four appendix slides. Six charts and seven tables are native editable objects. Chart values are embedded snapshots and were checked against their packaged data. The PDF has 14 searchable pages. All exported PDF pages were visually inspected for clipping, overlap and missing assets.

The original cover names and 2026 competition identity were checked against the source presentation. Historical source dates remain in the evidence record. The files were not opened and tested in desktop Microsoft PowerPoint; structural validation and export inspection do not claim that native application test.

When source data change, regenerate the analysis and figures, then separately refresh and review the presentation. Re-running Python does not automatically update the PPTX.
