# DLULIB first-use external validation — Stage 10

**Status:** completed 19 Nov 2026, manuscript v10. The source-trained numerical error predictors were evaluated on 6,500 independent-collection DLULIB Wi-Fi test scans, 650 physical reference points, and 39,000 candidate forecast targets across three floors in **one building**. Floor was known and test positions repeat training RPs.

- JEPFormer forecast MAE **2.426 m** (three individual seed metrics averaged; no ensemble); pooled CatBoost forecast MAE **2.546 m**.
- JEPFormer minus CatBoost paired RP-cluster difference **−0.120 m**, descriptive 95% interval **[−0.162, −0.078] m**.
- **Mixed outcome:** CatBoost has lower forecast RMSE and lower MAE conditional on large realized errors. Severe cases ≥10 m were underpredicted in **96.4%** of JEPFormer and **98.2%** of CatBoost forecasts.
- DLULIB is now USED and cannot serve as untouched data for future tuned models.
- Candidate-estimator training uses DLULIB training records; original Stage8 error-prediction weights remain fixed. Original raw DLULIB and private models, coordinates and predictions are not included.

Read [scientific validation protocol](docs/STAGE10_DLULIB_FIRST_USE_EXTERNAL_VALIDATION.md), [claim-to-evidence register](docs/STAGE10_EXPERIMENT_TO_EVIDENCE_INDEX.md), and [public aggregate results](results/aggregated/stage10_external_aggregate_summary.json). The accompanying scripts implement a privacy-safe, portable reconstruction; the exact historic data run is archived separately in private Drive. Full empirical reproduction additionally requires permission to access the original model checkpoints and source data.
