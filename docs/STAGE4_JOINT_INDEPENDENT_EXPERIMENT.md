# Retrospective Stage 4: joint vs independent learning

**Original splits:** 5,450 source-development, 4,089 source-calibration, 4,090 historically examined source-test scans (24,540 candidate-error targets; six dataset families). Test is **not untouched** for the 2026-11-18 experiments.

## Controlled comparisons

1. Transformer with full six-token self-attention vs identical architecture with *off-diagonal attention blocked*, same three seeds (11, 21, 31), training loss and descriptors. Geometry features retain cross-estimator information in both cases.
2. Single pooled estimator-aware CatBoost vs six independently trained CatBoost regressors, same descriptor subset and supervised error targets; pooled learner uses numeric estimator identity, independent learner uses a separate model for each estimator. The total number of trees differs.

| Input set | Learner | Joint/pooled MAE (m) | Masked/independent MAE (m) |
|---|---|---:|---:|
| 33 descriptors | Transformer, 3 seeds | 1.894 | 1.939 |
| 33 descriptors | CatBoost, fixed seed | 1.970 | 1.924 |
| 21 scan + local descriptors | Transformer, 3 seeds | 2.670 | 2.692 |
| 21 scan + local descriptors | CatBoost, fixed seed | 2.747 | 2.677 |

For 33 descriptors, paired seed-specific Transformer attention gains are **0.0022, 0.0561 and 0.0775 m**. Six independent CatBoost regressors improve MAE by **0.0459 m** over pooled CatBoost; the pooled advantage's descriptive paired family-bootstrap interval is **[-0.0698,-0.0098] m**. All intervals involve only six historical source dataset families; they do not establish prospective transfer.

**Interpretation:** The large improvement from 12 geometry descriptors (approximately 0.78 m in both architectures) dominates the smaller cross-token attention effect. Joint parameter sharing does not necessarily improve tabular accuracy. These are distinct mechanistic claims. Original frozen checkpoints and later externally evaluated BA1 CatBoost are different model versions.
