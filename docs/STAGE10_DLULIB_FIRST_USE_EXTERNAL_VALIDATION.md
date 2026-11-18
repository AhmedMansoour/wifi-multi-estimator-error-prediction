# Stage 10 — Frozen-source first-use DLULIB external evaluation

**Study:** multi-estimator numerical Wi-Fi position-error prediction. **Date:** 19 November 2026. **Status:** genuinely first use of DLULIB in this research; original test-position labels were accessed for scoring only after the predictions had been committed by SHA-256 and uploaded to a restricted Google Drive checkpoint.

## What is independently tested

The numerical-error predictors JEPFormer (three fixed seeds 11, 21, 31) and pooled CatBoost (one fixed seed 2026) were trained before the DLULIB dataset was opened. Their parameters, architecture, source-only normalization, feature definitions, and estimator identities were **not tuned using DLULIB test outcomes**. The six underlying *coordinate-estimating* Wi-Fi methods necessarily used each DLULIB floor's **training** radio map, without accessing the test XY. This evaluates transfer of a source-trained **error predictor** to a new Wi-Fi collection with a locally trained radio map. It is **not** zero-shot positioning and is not calibrated integrity estimation.

**Original source:** DLULIB, Nguyen-Huu et al. (2026), *Data in Brief*, article 113292, DOI: https://doi.org/10.1016/j.dib.2026.113292 ; archive DOI https://doi.org/10.5281/zenodo.19434712. Official ZIP MD5 `e30071a2f4bf14ed96f5f46f20468ac3`, observed ZIP SHA-256 `bfa13bd1ae48dd9b636fcf1313ceb4ce25aa4b6495880ab8b4f689dbafad0953`. Original data are **not redistributed here**.

| Floor | Training scans | Distinct training RPs | Test scans | Independent spatial RPs? |
|---|---:|---:|---:|---|
| 1 | 6,280 | 314 | 3,140 | No — same physical RP positions |
| 2 | 3,720 | 186 | 1,860 | No — same physical RP positions |
| 3 | 3,000 | 150 | 1,500 | No — same physical RP positions |
| **Total** | **13,000** | **650** | **6,500** | **One new building, three floors** |

Each input has 17 RSS columns. `-100` denotes no AP observation; RSS feature maps replace missing with `-110`, while the archived coordinate-estimating models use `0` for missing. No unknown-floor inference was performed; floor was given by the test workbook/floor session. No test ground-truth coordinates entered feature construction, coordinate-estimator fitting, or numerical-error forecasting.

## Frozen scientific protocol

The full prescore lock is separately archived as `STAGE10_PRE_SCORE_LOCK.md` with SHA-256 `bef6f21829dd78c7c438e174c984b0098549592fd6f72a41b5fe98f14fe5a922`.

Six position estimators were fitted **per known floor**, using only its original training records: CatBoost MultiRMSE 800 trees depth 6 lr 0.05; Extra Trees 250 trees; HistGradientBoosting 120 iterations; Random Forest 80 trees; KNN and inverse-square WKNN with `k=6`. All were fixed before reading external test measurements. The 33 observable diagnostic descriptors comprise 14 scan/radio-map features, 12 candidate geometry features, and 7 candidate-local features. A source-equivalence test compared the 14 scan indicators and diagnostic anchors against the separately archived ESWA native implementation: maximum absolute scan feature difference **2.8e-4** (all-observed synthetic test), with an additional synthetic 18%-missing-AP regression test difference **6.01e-5** (performed after scoring, no feature code changes). Features are transformed using the **unchanged source-only** median/clipping/mean/std values and 33 missingness flags (66 neural inputs). All six candidate estimates and all source predictor forecasts were produced and hash-locked for **6,500 scans x 6 estimators = 39,000** candidate-error endpoints.

All three frozen prediction files were uploaded to an owner-only Drive checkpoint **before** the separate scorer opened sealed test labels:

- Floor 1 prediction SHA-256: `bd29240372ca830bc81b8193bc648dbb4225c068e6473c838351467d15006c95`.
- Floor 2 prediction SHA-256: `0b6db0b26a6876915feaa46d34c3de141b616cb83151010e2faf79a3c49654cf`.
- Floor 3 prediction SHA-256: `17ede6a13a891466440ba87793c8d3d2a9581e865a85dcdd79a2cfb7cb07dfa9`.
- Prediction-freeze manifest SHA-256: `619979a10551064e17531fabeb8fc04ede35314ded6db474ffbe89c8a75df100`.
- Immutable prescore manifest SHA-256: `a9f364bc33b46519c6c4019de65e3bb5293d918fdf0448a8a7c2df3b36982e4f`.

This is a procedural prediction-before-scoring separation within one research workspace, **not a cryptographically blinded independent-party audit**. The original test coordinates were accessible in the supplied ZIP but withheld from the forecasting process.

## First-use scored results

| Indicator | JEPFormer (3 individual-seed metric mean) | CatBoost (one model) |
|---|---:|---:|
| Numerical error-forecast MAE (m) | **2.4260** | 2.5465 |
| Numerical error-forecast RMSE (m) | 3.4651 | **3.4254** |
| Forecast minus realized error bias (m) | −0.6586 | +0.2299 |
| Spearman predicted vs realized error | 0.4088 | 0.3484 |
| Actual-error ≥10 m AUROC | 0.7757 | 0.7490 |
| Actual-error ≥10 m average precision | 0.2829 | 0.2684 |
| Conditional forecast MAE, actual error ≥10 m (m) | 7.1252 | **6.6743** |
| Underpredicted among actual errors ≥10 m | **96.42%** | 98.22% |

There are 3,363 candidate endpoints with realized error ≥10 m (8.62% of 39,000), and their average actual error is approximately 13.53 m. The realized positioning MAE of the six position-producing methods is **4.8327 m**, a separate quantity from forecast MAE. **No improvement in final coordinate positioning** is asserted based solely on these error-forecast metrics.

JEPFormer seed-specific forecast MAE: seed 11, 2.3729 m; seed 21, 2.4870 m; seed 31, 2.4181 m. These are separate repeated-seed model evaluations, **not an ensemble**.

The paired comparison of the two forecast MAEs, resampling **650 physical RPs** (ten test scans each x six estimates), yields a descriptive mean JEPFormer-minus-CatBoost difference of **−0.1204 m**, with 95% RP-cluster bootstrap interval **[−0.1621, −0.0778] m** (4,000 replicates, fixed random seed 241119). This interval accounts for repeated scans at the same RP but **not** new-building sampling uncertainty: three floors are not three independent building families.

### Floor-wise forecast MAE (m)

| Floor | JEPFormer 3-seed average | CatBoost | Scientific reading |
|---|---:|---:|---|
| 1 | 2.5873 | 2.6109 | Very small overall advantage |
| 2 | 2.5666 | 2.7105 | Moderate JEPFormer advantage |
| 3 | 1.9142 | 2.2083 | Larger JEPFormer advantage |

For the individual position methods, JEPFormer has a lower forecast MAE for CatBoost, Extra Trees, Gradient Boosting and Random Forest positions, but CatBoost is better on **KNN and WKNN positions**. Overall numerical-error forecasting MAE favors JEPFormer whereas RMSE and conditional severe-error magnitude MAE favor CatBoost; **universal superiority is not justified**.

## Strong limitations that must accompany citation

The test locations **coincide with positions used in the DLULIB training radio map**; this evaluation therefore does not isolate extrapolation to previously unknown RPs. Three floors belong to **one building**. Floor identity was supplied. The different AP count, RSS population, survey method, and topology can affect both classes of models. Severe errors are underpredicted by **96–98%** of candidate endpoints that exceed 10 m, so numerical predictions are **not** confidence bounds or actionable integrity guarantees. This new first-use test must NOT be reused for tuning future models and described later as untouched. The empirically fitted source error-predictor checkpoints and raw DLULIB measurements cannot yet be distributed publicly without further rights/privacy clearance.

## Evidence and reconstruction

The public repository includes: (i) synthetic-safe exact feature construction, (ii) DLULIB input parsing, candidate model fitting, frozen original-source error prediction, separate hash-verified scoring scripts, (iii) synthetic unit tests, and (iv) non-identifying aggregate tables and SHA-256 references. The original source error-prediction model checkpoints **are not included**, so the complete empirical Stage10 run cannot be reproduced from this GitHub checkout alone. The model weights, original ZIP, per-scan candidate predictions, sealed test ground truth, private RP-level errors, and exact original stage scripts are preserved in the **unshared research Drive checkpoint**. A reproducibility claim must distinguish downloadable public code from restricted original research artifacts.

### Public local run after obtaining required data and authorized source model checkpoints

```bash
pip install numpy scipy scikit-learn catboost torch pytest openpyxl
python scripts/dlulib_prepare.py --zip /path/to/DLULIB.zip --workspace /private/work
python scripts/dlulib_fit_positions.py --workspace /private/work
python scripts/dlulib_predict_frozen.py --workspace /private/work --source-models /private/source-stage8 --source-scaler /private/source-only-scaler.npz
# BEFORE scoring: independently record SHA-256 of all prediction files and archive hashes.
python scripts/dlulib_score_frozen.py --workspace /private/work
pytest -q tests/test_dlulib_stage10.py
```

**Required safeguards:** the manual prediction hashes must be archived and verified before scoring; the scorer also verifies forecast file hashes. Keep work directory outside the public checkout and do not commit local source models, derived site geometry, sealed GT, or raw RSS.
