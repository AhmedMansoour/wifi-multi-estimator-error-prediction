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
