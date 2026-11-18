# Stage 9 — public methodological delta

**Stage status:** retrospective severe-error discrimination and numerical-bias audit completed on already examined source-test evidence; new DLULIB dataset intake/scoring **not executed**.

## Files

- `src/jepformer/tail_diagnostics.py`: post-inference, ground-truth-dependent numerical-error and severe-event diagnostics (MAE, signed bias, AUROC, AP, severe underprediction), using explicit availability masks; no calibration or protection bounds.
- `src/jepformer/dlulib_gate.py`: source-archive MD5/SHA-256 and ZIP layout gate. Does **not** read Excel test records or ground truth.
- `tests/test_stage9_tail_diagnostics.py` and `tests/test_stage9_dlulib_gate.py`: deterministic synthetic tests; no observed research data.
- `results/aggregated/stage9_severe_error_aggregate.csv`: 48 summary combinations of model/training × missing count × severe threshold (7/10/20 m), including means across pre-existing seeds and patterns.
- `results/aggregated/stage9_severe_error_by_family.csv`: six anonymized historical source families, 24 learner/training/family summaries.
- `docs/STAGE9_SEVERE_ERROR_VALIDATION.md`: evidence class, denominators, caveats and complete metric table.
- `docs/DLULIB_EXTERNAL_VALIDATION_FREEZE_GATE.md`: future first-use benchmark protocol and binary-data availability barrier.

Run `python -m pytest -q tests` in the combined repository: 15 tests passed locally after adding the Stage 9 methods (9 prior, 6 new). The disclosed code cannot recreate paper accuracy without the restricted empirical source tensors and frozen prediction arrays. Raw observed Wi-Fi data, source-test labels, indoor floor plans, true locations, and original fitted weights must not be committed to the public repository.
