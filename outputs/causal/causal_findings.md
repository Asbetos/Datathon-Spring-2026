# Causal Inference Findings: Organic Waste Bans

## 1. Difference-in-Differences (DiD) Analysis

Using a two-way fixed effects model with state and year fixed effects, clustered standard errors:

| Outcome | Effect (β) | Std. Error | p-value | 95% CI | Significance |
|---------|-----------|------------|---------|--------|--------------|
| Landfill Rate | 0.020266 | 0.007602 | 0.0077 | [0.005366, 0.035166] | *** |
| Diversion Rate | -0.051783 | 0.009769 | 0.0000 | [-0.070931, -0.032636] | *** |
| Tons Landfilled | 30690 | 41152 | 0.4558 | [-49967, 111348] | n.s. |

**Interpretation:** Organic waste bans are associated with a 0.0203 pp increase in landfill rate (proportion) (significant at 5% level, p=0.0077)

- Model: Y_st = α + β×BanActive_st + γ_s + δ_t + ε_st
- N = 750 state-year observations (2010-2024)
- 12 treated states, 38 control states
- R² (landfill_rate model): 0.9893

## 2. Event Study: Dynamic Treatment Effects

The event study plots treatment effects relative to ban adoption year (t=-1 as reference).

**Key findings:**
- Pre-treatment coefficients (t=-5 to t=-2) are close to zero → parallel trends assumption supported
- Post-treatment effects show sustained effects over time
- Largest post-treatment effect at t=6: β=0.0472

## 3. Synthetic Control: California SB 1383

California enacted SB 1383 (effective 2022) — the most ambitious US food waste policy.

- **Pre-treatment MSE:** 0.00172622 (good fit)
- **Post-treatment gap:** 0.0283 (actual minus synthetic)
- **Treatment effect (2024):** 0.0242
- **Top donor states:** Wisconsin (1.00), Alabama (0.00), Arizona (0.00)

**Interpretation:** California's landfill rate increased by 0.0242 percentage points relative to its synthetic counterfactual after SB 1383.

## 4. COVID Resilience

Comparing waste management resilience during COVID-19 (2019-2022):

| Metric | Ban States | Non-Ban States |
|--------|-----------|----------------|
| Mean 2019→2020 Change | -27.9% | -40.4% |
| Mean 2020→2022 Recovery | 70.7% | 55.9% |

## 5. Nationwide Policy Extrapolation

**If all 50 states adopted organic waste bans:**
- DiD estimated effect on landfill rate: 0.0203 pp
- Projected additional tons diverted from landfill: **-0.78M tons/year**
- This represents a change across the 38 non-ban states

## Methodology Notes

- **Identification strategy:** Staggered adoption of organic waste bans across US states (2014-2025)
- **Treatment:** Binary indicator for whether a state has an active organic waste ban in a given year
- **Fixed effects:** State FE (control for time-invariant state characteristics) + Year FE (control for national trends)
- **Standard errors:** Clustered at state level to account for serial correlation
- **Robustness:** Event study validates parallel trends; synthetic control provides case-study evidence for California
