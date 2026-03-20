# ML, Forecasting & Scenario Findings

## XGBoost + SHAP Feature Importance

### Landfill Model (target: tons_landfill)
- **Model CV R² = 0.9448 ± 0.0568** (216,930 observations)
- Top feature: **tons_surplus** (mean |SHAP| = 1,924.9) — the volume of surplus food is overwhelmingly the strongest predictor of landfill waste
- #2: **sector** (481.7) — sector type determines waste routing infrastructure
- #3: **tons_supply** (400.4) — total food supply drives waste volume
- #4: **state** (246.6) — geographic/policy variation matters
- #5: **food_type** (221.8) — some food types (Prepared Foods) landfill at much higher rates
- #6: **year** (52.4) — modest temporal trend
- #7: **ban_active** (24.7) — organic waste bans have a detectable but modest direct SHAP contribution

**Insight:** Reducing surplus at the source (especially in Foodservice/Residential sectors) has far greater leverage than end-of-pipe policy alone.

### Diversion Rate Model (target: diversion_rate)
- **Model CV R² = 0.9714 ± 0.0131**
- Top feature: **state** (mean |SHAP| = 0.177) — state-level infrastructure and policy environment is the dominant predictor of diversion success
- #2: **sector** (0.031) — some sectors (Farm, Manufacturing) achieve far higher diversion
- #3: **ban_active** (0.028) — bans rank #3 for diversion rate, confirming policy relevance
- #4: **tons_surplus** (0.026)

**Insight:** State-level infrastructure investment is the strongest lever for improving diversion rates, with bans providing a meaningful policy signal.

## State Clusters

- **Cluster 0 "Agricultural States"** (5 states): CA, ID, OR, WA, WI — lowest landfill rate (20.7%), high farm share (46%), 3 ban states. These are policy leaders with strong composting/feed diversion.
- **Cluster 1 "Landfill-Dependent"** (22 states): TX, OH, CO, VA, NV, etc. — highest landfill rate (53.9%), urban-consumer profile. 6 ban states but 16 without — these are the **highest-impact targets** for ban expansion.
- **Cluster 2 "Diversion Leaders"** (4 states): IA, LA, NE, ND — high feed diversion (52.1%), high composting (31.3%), NO ban states. These achieve diversion through agricultural infrastructure without mandates.
- **Cluster 3 "Mixed Economy States"** (19 states): FL, GA, IL, NY, PA, etc. — moderate landfill rate (43.4%). 3 ban states, 16 without.

**Priority targets for ban expansion:** Texas, Florida, Ohio, Georgia, Illinois, North Carolina, Michigan, Arizona, Virginia, Tennessee — all in clusters alongside successful ban states but without bans themselves.

## Forecast (Business as Usual)

- **Method:** Prophet time-series model (2010-2024 historical)
- **By 2030: 26.5M tons to landfill** (up 15.3% from 23.0M in 2024)
- Key sector trends:
  - Residential: largest and growing contributor
  - Foodservice: second largest, volatile post-COVID
  - Retail: smaller but steadily increasing

## DiD-Calibrated Scenarios

| Scenario | Tons Diverted | GHG Saved (MT CO2e) | Dollars Saved | Meals Recovered |
|----------|-------------|-----------|---------------|-----------------|
| A: Date Labels | 425,000 | 1.9M | $2.8B | 745M |
| B: Nationwide Ban | 779,441 | 3.4M | $4.7B | 1.52B |
| C: Combined | 1,023,775 | 4.5M | $6.4B | 1.93B |

- **Scenario A** (Federal Date Label Standardization): Based on ReFED's 425K tons/year estimate, apportioned by state Retail+Residential waste share. Top impact states: California, Texas, Florida.
- **Scenario B** (Nationwide Organic Waste Ban): Uses DiD coefficient (β = 0.0203) applied to 38 non-ban states. Top impact: Florida (85.7K tons), Texas (82.6K tons), Wisconsin (54.2K tons).
- **Scenario C** (Combined with 15% overlap discount): Over 1M tons diverted, $6.4B saved, nearly 2 billion meals recovered.

## Key Takeaway

Policymakers should pursue a **dual strategy**: (1) federal date label standardization as a low-cost, immediate-impact intervention and (2) expansion of organic waste bans to the 38 states without them — prioritizing **Texas, Florida, Ohio, Georgia, and Illinois**, which are landfill-dependent states in the same clusters as successful ban states. Together, these policies could divert over **1 million tons** of food from landfills annually, saving **$6.4 billion** and preventing **4.5 million MT CO2e** in greenhouse gas emissions. The XGBoost SHAP analysis confirms that while surplus volume is the strongest predictor of landfill waste, state-level policy and infrastructure (the lever policymakers control) is the dominant driver of diversion success, validating the causal DiD finding that bans meaningfully shift waste management behavior.
