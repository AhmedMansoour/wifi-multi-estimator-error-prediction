# Stage 6 — Whole-family-exclusion study (retrospective)

**Research status:** Completed 18 November 2026. All six source families had been previously examined in earlier development stages. This is a *retrospective dataset-family exclusion stress test*, **not** a newly prospectively untouched external benchmark.

## Protocol and scope

The archived source contains 13,629 scans spanning ten units and six dataset families, with six existing candidate positions for each scan. For each fold, an entire family is excluded from numerical error-predictor training, calibration, feature normalization, early stopping, and hyperparameter selection. The retained families provide their original development and calibration scans; evaluation comprises all records of the excluded family.

The six base positioning estimators and candidate descriptors were generated using each dataset family's own training radio map. This is a test of *error-predictor transfer under a locally available radio map*, not zero-shot positioning in an unmapped building.

Models are compared using either (a) full 33 descriptors—14 scan, 12 geometry, 7 candidate-local—or (b) 21 scan+local descriptors, excluding all 12 geometry descriptors. Each input retains its corresponding missingness indicators. Original Stage 13 architecture uses three trained seeds **11, 21, 31**, consistent multitask losses and calibration-only checkpoint selection. Shared method-aware CatBoost uses one fixed seed **2026**, 500-tree cap, depth six, learning rate 0.05 and independent non-target calibration early stopping.

## Aggregated held-out family MAE (m)

| Family label | Scans | JEPFormer full (mean ± SD) | JEPFormer no geometry | CatBoost full | CatBoost no geometry |
|---|---:|---:|---:|---:|---:|
| F01 | 831 | 2.050 ± 0.132 | 3.034 | 2.062 | 2.590 |
| F02 | 343 | 2.019 ± 0.094 | 2.493 | 2.040 | 2.595 |
| F03 | 4,025 | 0.752 ± 0.018 | 1.552 | 0.991 | 1.670 |
| F04 | 3,934 | 1.182 ± 0.023 | 2.233 | 1.454 | 2.464 |
| F05 | 286 | 1.855 ± 0.020 | 2.354 | 1.829 | 2.290 |
| F06 | 4,210 | 5.118 ± 0.122 | 6.025 | 5.054 | 6.085 |
| Scan-weighted mean | **13,629** | **2.359** | **3.261** | **2.489** | **3.356** |

The geometry contribution has the same sign in **6/6** held-out families for both learning approaches. The reduction in scan-weighted MAE from adding geometry is approximately 0.902 m for the Transformer and 0.867 m for CatBoost. The F06 family remains difficult for both, so the results do not establish universally transferable accuracy.

## What this does and does not support

- **Supports:** cross-estimator geometry provides useful error-prediction information under retrospective complete-family exclusion for both learning models.
- **Does not establish:** prospectively independent new-family superiority, transferable accuracy on every indoor site, end-to-end unmapped-environment generalization, calibrated uncertainty, or certified integrity bounds.
- **Does not involve:** adaptive ensemble averaging or using true query coordinates at inference time.

## Artifact provenance

Exact per-scan prediction-error pairs, source scan IDs, original candidate coordinates, raw source reconstruction archives, internal checkpoints, seed/fold scripts, hashes, and a full versioned research capsule are preserved in a restricted, owner-only Google Drive research checkpoint. These records are intentionally **not present in the public repository**. The public repository provides synthetic runnable illustrations, aggregate evidence, and this protocol, but is **not yet a fully executable reproduction of all empirical results**. The planned full public release remains subject to source licensing, confidential survey safeguards, and independent privacy review.

**Main outstanding tasks:** genuinely prospectively unused external data family for the newly retrained learners; robustness to missing/replaced estimator; rights and dataset-adapter clearance; fuller source-linked supplementary evidentiary records.
