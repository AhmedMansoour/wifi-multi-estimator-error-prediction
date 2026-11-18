# Evidence provenance and reproducibility register

| Experiment | Verification level | Legitimate inference |
|---|---|---|
| Original Stage 13 frozen JEPFormer | Original weights, normalization and partition recovered; source error MAE replayed 1.843848 m | Historical source comparator |
| Original 1.862 m shared CatBoost | Historically documented, different checkpoint from BA1 and new CatBoost | Historical comparison only |
| Stage 3 four-group descriptor ablations | Newly retrained, original source tensors; Transformer three seeds and CatBoost fixed seed | Descriptive historical representation benefit |
| Stage 4 masked Transformer attention | Newly retrained across seeds 11/21/31 | Direct token interaction benefit conditional on geometric inputs |
| Stage 4 independent CatBoost | Newly retrained six separate models vs one pooled model | Parameter-sharing comparison, unequal total model capacity |
| TUJI1, UVIndoorLoc | Originally locked external frozen-model evaluations | Original frozen-model transfer behavior only |
| 10W | Committed site RP-group holdout; originally related to ESWA | Limited historical local site evidence |
| SOD / NearLink | Repeatedly inspected development history | Retrospective evaluations, not untouched validation |
| Original 22-descriptor ablation | Exact reduced feature indices unavailable | Do not attribute group-specific effect |
| Stage 19 raw attention | Some final checkpoints unavailable | Report-level information, not fully replayed |
| Fresh unseen-family test for v3/v4 learners | **Not performed** | No independent confirmation claim |
| Missing-estimator robustness | **Not performed** | Fixed six-estimator assumption remains |

**Primary inputs:** 14 scan/radio-map descriptors, 12 cross-estimator geometry, 7 local RP descriptors + 33 missingness flags, six candidate estimates in fixed estimator order. Ground-truth coordinates/true errors are training targets or evaluation labels, never inference features. Original source split: 5,450 / 4,089 / 4,090 scans across ten units and six families. Preserve source SHA256 and per-run prediction hashes privately until release permissions are verified.

**Scientific boundary:** Numerical error forecasts are not calibrated integrity bounds, and a lower error-forecast MAE does not establish lower selected-coordinate error.

## Stage 8 retrospective availability-aware retraining (19 November 2026)

- Method: four versions per source-development scan (full, 1-, 2-, 3-estimator outage), three JEPFormer seeds and one pooled CatBoost seed; retrospective source test only.
- A fourfold full-input repetition comparator was added AFTER the initial Stage8 scores (post hoc). A causal effect attributable uniquely to augmentation is therefore not fully isolated.
- Evidence: exact original diagnostic-anchor geometry restored; frozen checkpoint/prediction hashes and seed-level metrics saved only in owner-only research Drive archive. Public: aggregate model comparisons, generic augmentation/masking code, tests, methods and limitations.
- Scientific classification: retrospective robustness stress; DOES NOT validate a new untouched environment, arbitrary estimator set size, replacement methods, safety bounds or selected-coordinate accuracy.

## Stage9 — frozen-model severe-error audit and external data eligibility

Completed: post hoc diagnostic replay from Stage8 immutable prediction tensors and the previously inspected historical source-test labels, using actual-error thresholds >=7/10/20 m and all 41 outage patterns. Public: deterministic scoring code, synthetic tests, two non-identifying aggregate tables and scientific limitations. Restricted: exact source labels, per-scan predictions, radio maps, and hashes in owner-only Drive.

DLULIB first-use external candidate has documented three-floor separate training/test observations; the 6.1 MB archive has not been downloaded or scored in this runtime, so exact feature schema and all JEPFormer/CatBoost external metrics remain UNVERIFIED. A future independent test must freeze source-compatible features and original model outputs before reading any test XY.
