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
