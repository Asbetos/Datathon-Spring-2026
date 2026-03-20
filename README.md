# Food Excess Analysis & Policy Framework

**First causal evidence that bans without infrastructure fail — the Massachusetts model shows how to fix it**

*GW DSA Datathon 2026*

---

## Problem Statement

The United States wastes 70.7 million tons of food annually ($384B), sending 23.0 million tons to landfills and generating 221 million MT CO2e — while 44 million Americans face food insecurity. Current organic waste bans have paradoxically *increased* landfill rates because they lack processing infrastructure.

## Methodology: Four-Pillar Approach

| Pillar | Method | Key Output |
|--------|--------|------------|
| **National EDA** | 9 visualizations across sectors, causes, destinations, trends | Crisis quantification: 70.7M tons, $141B residential blind spot |
| **Machine Learning** | XGBoost + SHAP (CV R²=0.94, N=216,930); K-Means clustering | Infrastructure > mandates (6x SHAP ratio); 4 state archetypes |
| **Causal Inference** | DiD (TWFE), Event Study, Synthetic Control on 50-state x 15-year panel | B = +2.03 pp on landfill rate (p=0.008); only MA succeeds |
| **Policy Framework** | Three-tier federal/state/sector recommendations, DiD-calibrated projections | 1.02M tons diverted, $6.37B value, 4.47M MT CO2e saved |

## Key Findings

- **Bans alone fail:** DiD shows organic waste bans *increase* landfill rates by 2.03 pp (p=0.008, 95% CI: [0.54, 3.52 pp]) — independently validated by UCSD study in *Science* (2024)
- **Infrastructure is key:** SHAP analysis shows state infrastructure (0.177) is 6x more predictive of diversion than ban status (0.028)
- **Massachusetts exception:** Only state to succeed — 350K tons diverted, 1,670+ jobs, $194M value — because it paired mandates with processing facilities
- **22 "Landfill-Dependent" states** (53.9% avg rate) are highest-priority targets for infrastructure-backed expansion
- **Residential blind spot:** 23.5M tons surplus, $141B value, ZERO donations — largest sector with no diversion infrastructure
- **Date labels most cost-effective:** 425K tons/yr, $1.82B net benefit from standardization alone
- **Combined framework:** Diverts 1,023,775 tons/yr, saves 4.47M MT CO2e, recovers 1.93B meals, generates $6.37B value

## Policy Recommendation Summary

| Tier | Action | Impact |
|------|--------|--------|
| **Federal** | Date Label Standardization Act | 425K tons/yr, $1.82B net benefit |
| **Federal** | National Organic Waste Mandate + Infrastructure Fund | 779K tons/yr shifted |
| **State** | Expand infrastructure-backed bans to 38 states | Priority: FL (86K), TX (83K), WI (54K) |
| **State** | Municipal donation & composting infrastructure | Close $141B residential gap |
| **Sector** | Residential: labels + composting + education | 33% of surplus, 0 donations |
| **Sector** | Foodservice: waste tracking mandates | 42% of landfill waste |
| **Sector** | Farm: gleaning incentives + secondary markets | 13.4M tons not harvested |

## Repository Structure

```
├── data/                          # ReFED source data (national + state CSVs)
│   ├── ReFED_US_Food_Surplus_Summary.csv
│   ├── ReFED_US_Food_Surplus_Cause_Summary.csv
│   ├── ReFED_US_Food_Surplus_Detail.csv
│   ├── ReFED_US_State_Food_Surplus_Summary.csv
│   ├── ReFED_US_State_Food_Surplus_Detail.csv
│   └── policy_timeline.csv
├── notebooks/                     # Reproducible analysis notebooks
│   ├── 01_data_loading.ipynb      # Load & clean all 5 ReFED datasets
│   ├── 02_national_eda.ipynb      # National EDA, 9 charts, eda_report.json
│   ├── 03_state_eda.ipynb         # State-level EDA, ban vs non-ban analysis
│   ├── 04_ml_shap.ipynb           # XGBoost + SHAP feature importance
│   ├── 05_clustering.ipynb        # K-Means state clustering
│   ├── 06_forecasting.ipynb       # 2030 landfill forecast
│   ├── 07_did_causal.ipynb        # DiD, event study, synthetic control
│   ├── 08_scenario_simulation.ipynb # DiD-calibrated policy scenarios
│   └── 09_covid_analysis.ipynb    # COVID resilience analysis
├── utils/                         # Shared utility modules
│   ├── data_loader.py             # Dataset loading & cleaning
│   └── causal_inference.py        # DiD, event study, synthetic control
├── outputs/
│   ├── analysis/                  # EDA outputs
│   │   ├── charts/                # 9 visualization PNGs
│   │   ├── cleaned_data/          # Cleaned parquet files
│   │   └── eda_report.json
│   ├── causal/                    # Causal inference outputs
│   │   ├── charts/                # Event study, synthetic control, etc.
│   │   ├── did_results.json
│   │   ├── event_study_results.json
│   │   └── synthetic_control_results.json
│   ├── ml/                        # Machine learning outputs
│   │   ├── charts/                # SHAP, clusters, scenarios
│   │   ├── shap_results.json
│   │   ├── cluster_results.json
│   │   ├── forecast_results.json
│   │   └── scenario_results.json
│   ├── policy/                    # Policy synthesis
│   │   ├── policy_data.json
│   │   ├── policy_brief.md
│   │   └── external_evidence.md
│   └── final/                     # Competition deliverables
│       ├── presentation.pptx
│       └── policy_brief.docx
└── requirements.txt
```

## Reproduction

```bash
pip install -r requirements.txt

# Run notebooks in order:
# 01 → 02 → (03, 04, 07, 09) → (05, 06) → 08
# Notebooks 03/04/07/09 can run in parallel after 01+02 complete.
```

## Data Sources

- **ReFED Food Waste Monitor** — National and state-level food waste tracking data (2010-2024), 50 states x 15 years, covering surplus, waste, destinations, causes, and sectors. https://refed.org/food-waste/the-problem
- **Policy timeline** — Organic waste ban adoption dates compiled from state legislation records
- **UCSD / Science (2024)** — Independent validation of ban effectiveness findings

## Team

GW Data Science — Datathon Spring 2026
