# Methodology

## Scope

The case asks whether TileShield Insurance should enter AI liability insurance. The analysis links company underwriting, external incident severity, and conditional entry economics. It is an academic case study rather than an actuarial rate filing or a capital-adequacy assessment.

The original 2021–2025 financial period and 2026 competition identity are preserved. External sources support interpretation and product questions; later market developments are not used to rewrite the competition facts.

## Financial calculations

Exhibit A monetary inputs are CAD thousands. `load_exhibits()` multiplies monetary inputs by 1,000 and leaves counts and exposure unchanged. The analysis recomputes ratios from primitive inputs rather than relying on cached spreadsheet formulas.

For each line and year:

```text
Frequency = Claim count / Exposure
Average severity = Incurred losses / Claim count
Pure premium = Incurred losses / Exposure
Premium per exposure = Earned premium / Exposure
Loss ratio = Incurred losses / Earned premium
Expense ratio = Operating expenses / Earned premium
Combined ratio = Loss ratio + Expense ratio
Underwriting profit = Earned premium - Incurred losses - Operating expenses
```

Company ratios use summed losses, expenses and premiums. A simple average of line ratios is incorrect when premium weights differ. Exposure units can differ across lines, so they are not summed to derive a company claim frequency or a unique customer count.

Historical profit is a flow. It does not establish available capital, reserve adequacy, liquidity, reinsurance support or a permissible AI risk budget.

Cyber's 2021–2025 changes distinguish absolute frequency points from relative severity and unit-cost growth. Premium per exposure reflects rates, coverage and business mix. The difference between two growth rates is a descriptive diagnostic; it is not itself a change in the loss ratio.

## Incident data checks and severity

The source contains 135 distinct incident IDs. Required fields are complete and estimated losses are positive. The separate Exhibit B workbook was checked against the combined workbook during preparation and is unnecessary for the public workflow.

Grouped summaries retain sample counts, arithmetic means, medians, ranges and totals. Nine autonomous failures account for 40.15% of total estimated loss. A 1.5×IQR upper threshold of CAD 9.4235M identifies the same nine observations. They are retained as economically meaningful events, not removed as inconvenient outliers.

The full sample is a mixture of mechanisms with different severity scales. Its skewness does not by itself establish a heavy-tailed distribution within each proposed underwriting segment. The observed maximum is not a maximum possible loss.

Incident counts have no denominator of deployed systems or policy-years. The analysis therefore does not estimate event or insured claim frequency from Exhibit B.

## Candidate group

The candidate descriptive subgroup consists of incidents with `human_oversight == Yes` and failure type `Hallucinated Output` or `Misinformation`. It contains 28 observations: 22 hallucination and 6 misinformation incidents. Its mean estimated loss is CAD 167,643.

This is a pre-screening subgroup, not 28 verified covered claims. Each event still needs mapping to the insured's role, professional service or product, type of harm, relevant policy and exclusions. The source mean is not a contract-adjusted pricing severity.

## Additive log-loss model

```text
ln(estimated insured loss) = intercept
                          + categorical industry
                          + categorical failure type
                          + categorical human oversight
                          + error
```

Ordinary least squares uses dummy variables with the alphabetically first category as the reference. Coefficients are computed with `numpy.linalg.lstsq`. The model uses 135 observations, 13 estimated coefficients and 122 residual degrees of freedom.

R² is 95.009% and adjusted R² is 94.518%. These describe fit to log loss, not accuracy of future dollar claims or prices.

### Sequential attribution

Each sequential share is the incremental reduction in squared error divided by the same total log-loss sum of squares. Changing term order changes the allocation of shared information:

| Order | Industry | Failure type | Oversight | Residual |
|---|---:|---:|---:|---:|
| Industry, failure type, oversight | 22.243% | 71.136% | 1.630% | 4.991% |
| Failure type, industry, oversight | 0.318% | 93.061% | 1.630% | 4.991% |

Extra-sum-of-squares comparisons also remove each factor from the full model. Industry's unique contribution is about 0.274% of total log variance. These unique contributions do not generally sum to overall R² because factors share information.

The model supports strong mechanism segmentation in this sample. It does not support treating the industry-first 22.243% as an independent causal contribution or a mechanical industry premium multiplier.

### Oversight interpretation

The fitted oversight coefficient is approximately −0.42975. Its exponent is 0.65067, a conditional geometric-mean loss ratio under this additive log model. It corresponds to an approximately 34.9% association with lower modeled geometric mean loss, holding included categories fixed.

The raw arithmetic means are CAD 4.227M without oversight and CAD 2.395M with oversight. The latter is approximately 43.3% lower; reversing the comparison makes the former about 76.4% higher. Different denominators and adjustments explain the different percentages.

Neither comparison proves causation. Returning from log predictions to expected arithmetic dollar loss requires attention to residual retransformation. Frequency, expenses, contract terms and accumulation remain separate, so no automatic premium discount is inferred.

### Validation

A deterministic random five-fold split uses seed 42, with the same factor schema across folds. The implementation checks that training folds retain full category support. Random-fold log-loss R² is approximately 93.6%.

This checks within-sample generalization only. Similar descriptions or common event templates may appear across folds, the category schema is observed globally, and random folds do not test a later year or new customer population. No causal validity, future claim frequency, temporal stability or capital adequacy follows from this score. No p-values or coefficient confidence intervals are claimed in this revision.

## Pilot economics

The pilot uses independent, editable assumptions. Annual frequency is expected claims per policy and may exceed one in general; the illustrated range is small. Mean covered cost includes defence in the example and must reflect the selected contract.

```text
Annual profit = N × premium × (1 − variable expense ratio)
              − N × claim frequency × mean covered cost
              − fixed costs

Break-even frequency = [N × premium × (1 − expense ratio) − fixed costs]
                       / [N × mean covered cost]
```

Negative break-even frequency means fixed and variable costs exhaust premium before any claims. A common-vendor scenario separately multiplies affected policies by average covered cost. It is a deterministic gross stress, not a probabilistic capital or reinsurance model.

See [pilot-design.md](pilot-design.md) for assumptions, launch rules and omitted costs.
