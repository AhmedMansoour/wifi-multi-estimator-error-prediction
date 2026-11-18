# Aggregate evidence only

These CSVs contain pooled metrics from new **retrospective** retraining on the historical source partition (4,090 scans, six candidates each, six source families). They do not contain observed BSSIDs, coordinates, per-scan identifiers, private tensors or model weights.

- `stage3_descriptor_comparison.csv`: exact feature-group controls, three-seed Transformer vs fixed-seed CatBoost.
- `stage4_comparison.csv`: original joint-attention or pooled model versus diagonal-masked attention or six independently fitted regressors.

The original 1.862 m shared CatBoost and new 1.970 m CatBoost are **not** identical model checkpoints. The per-family statistical comparisons and precise reproducibility protocol reside in the accompanying research supplement; six-family intervals are descriptive and do not establish independent family transfer.
