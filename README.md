# Wi-Fi multi-estimator positioning-error prediction

**JEPFormer + CatBoost | reproducibility workspace | pre-release**

This research models the *realized positioning error* of six existing Wi-Fi fingerprinting position estimators. Inputs combine **14 scan/radio-map descriptors, 12 cross-estimator spatial-geometry descriptors, and 7 candidate-local support descriptors**, with missingness flags. The learning alternatives include a six-token Transformer (JEPFormer), pooled CatBoost, and six estimator-specific CatBoost regressors.

### Verified retrospective source experiments

| Retained features | Transformer MAE, 3-seed mean (m) | Pooled CatBoost MAE (m) |
| --- | ---: | ---: |
| Scan only (14) | 3.094 | 3.238 |
| Scan + local (21) | 2.670 | 2.747 |
| Scan + geometry (26) | 1.947 | 2.004 |
| Full 33 | 1.894 | 1.970 |

With all 33 features, a Transformer with direct cross-token attention achieves **1.894 m** source-test MAE; an otherwise matched diagonal-attention control achieves **1.939 m** (three-seed means). Six individually trained CatBoost models achieve **1.924 m**, versus **1.970 m** for pooled CatBoost. Cross-estimator geometry is the principal validated descriptor contribution. All these new experiments use an **already inspected historical source test**; they are not new independent external-family confirmation.

### Critical scientific boundaries

- A numerical error estimate is **not** an integrity bound, statistical protection level, or guaranteed-safe position.
- The original archived historical CatBoost (1.862 m), later source-trained BA1 transfer checkpoint, and new 1.970 m pooled CatBoost are **different models**. Do not equate them.
- The original locked UVIndoorLoc comparison favors CatBoost (1.523 m versus JEPFormer 2.247 m), while the earlier 10W reference-map holdout favors JEPFormer (3.138 m versus CatBoost 3.572 m).
- The old 22-feature ablation subset and final raw-radio-map alternative checkpoints are not completely recovered. Do not represent them as fully replayable.
- Direct cross-token attention is not synonymous with cross-estimator geometric information: the latter is already encoded into the descriptors, even in the masked-attention control.

### Repository scope

The repository was initialized before the full empirical release audit. **Only privacy-cleared, text-only method descriptions and synthetic code are appropriate for this public development stage**. The full research code and synthetic executable demo are also available in the accompanying local repository ZIP.

**Not released:** private Hong Kong BSSIDs, observed scans, floor-plan images/vectors, reconstructable building geometry or coordinates, private empirical tensors, or uncleared checkpoints. Public benchmark data will be obtained from their publishers according to licenses; synthetic examples are not substitutes for experimental validation.

See the source-evidence notes and privacy policy before using this work. The manuscript and supplementary files will be versioned after scientific and confidentiality clearance.

### Stage 6: retrospective whole-family-exclusion validation (18 November 2026)

A newly completed six-family exclusion analysis retrains both learners on five historical dataset families and evaluates on the sixth, with 33 versus 21 descriptors. Scan-weighted full-input forecast MAE: **JEPFormer 2.359 m (three-seed average)**; **CatBoost 2.489 m (one seed)**. Removing the 12 cross-estimator geometry descriptors increases these values to 3.261 m and 3.356 m, respectively. Each of the six source families was previously inspected in historical development; these results are **retrospective transfer diagnostics, not a newly untouched independent test**. [Protocol and all aggregate family results](docs/STAGE6_RETROSPECTIVE_FAMILY_EXCLUSION.md).

### Stage 7: estimator availability and missing-method stress (18 November 2026)

The original six-estimator models were subjected to 41 retrospective outage patterns on the **previously inspected 4,090-scan source test**, without retraining. When one, two, or three candidate methods are unavailable, error-forecast MAE rises to **2.183/2.455/2.636 m** for CatBoost and **2.222/2.611/3.011 m** for JEPFormer with masked unavailable attention keys, compared with full-input baselines of 1.970/1.894 m. The experiment exposes a genuine **fixed-estimator-set limitation**; it does not demonstrate validated variable-cardinality operation. [Scientific protocol and aggregate results](docs/STAGE7_MISSING_ESTIMATOR_STRESS.md). [Synthetic-safe adapter](src/jepformer/availability.py) and [invariance tests](tests/test_availability.py) are available, while raw empirical data and checkpoints remain private.


### Stage 8: availability-aware training, controlled retrospectively (19 November 2026)

The six-slot Transformer and pooled CatBoost models were retrained with one fully observed and three **simulated estimator-outage** versions of each original source-development scan. A subsequent **post hoc** fourfold full-input repetition control tested whether the performance gains merely reflected an increased training budget. On the *previously examined* 4,090-scan historical source test, the outage-trained Transformer achieved **1.832, 1.873, 1.937, 2.052 m** forecast MAE with 0–3 missing estimators, compared with **1.896, 2.239, 2.655, 3.082 m** for the repeated-full control (three-seed means). CatBoost achieved **1.991, 2.044, 2.125, 2.209 m** versus **1.948, 2.160, 2.435, 2.615 m** for its control (one seed).

The extra robustness has a full-input accuracy trade-off for CatBoost. The matched control was devised after the initial Stage 8 outcomes; these observations cannot be claimed as prospective independent validation. Model identities remain fixed to six slots and severe-error underprediction persists. No empirical measurements or weights are included here.

[Exact scientific protocol and provenance](docs/STAGE8_AVAILABILITY_AWARE_TRAINING.md) · [Synthetic-safe augmentation code](src/jepformer/availability_training.py) · [Automated tests](tests/test_stage8_availability_training.py) · [Matched-control summary](results/aggregated/stage8_matched_budget_aggregate.csv) · [Outage-trained seed summaries](results/aggregated/stage8_outage_trained_seeds.csv) · [Repeated-full seed summaries](results/aggregated/stage8_repeated_full_seeds.csv)

### Stage 9: severe-error behavior and new-dataset readiness (19 November 2026)

Frozen Stage8 forecasts were retrospectively audited for actual positioning errors >=7, >=10 and >=20 m, including 41 estimator outage patterns. At full availability, severe-error ranking at >=10 m has AUROC 0.956 for availability-aware JEPFormer (3-seed mean) and 0.954 for CatBoost (one seed), yet 65.7% and 74.5% of such realized errors are numerically underpredicted. These are NOT calibrated bounds, protection levels or prospectively validated warnings.

[Stage9 scoring utilities](src/jepformer/tail_diagnostics.py), [scientific evidence](docs/STAGE9_SEVERE_ERROR_VALIDATION.md), [48-row aggregate table](results/aggregated/stage9_severe_error_aggregate.csv), [six-family summary](results/aggregated/stage9_severe_error_by_family.csv), [DLULIB benchmark freeze gate](docs/DLULIB_EXTERNAL_VALIDATION_FREEZE_GATE.md). DLULIB's official data archive was not retrieved or scored; no external numerical claim is made. The public ZIP verifier reads filenames/hashes only, not test labels. All primary empirical model weights, RSS records, positions and individual predictions remain outside GitHub.
