# Stage 10 source-to-result traceability

This register is **not** a substitute for the nonpublic empirical evidence archive. File-hash commitments were deposited in a private Google Drive checkpoint *before* scoring.

| Claim / exhibit | Experimental provenance | Public evidence | Private replay evidence | Status |
|---|---|---|---|---|
| Input data 17 AP, 650 RPs, three floors | Original DLULIB official ZIP MD5 check; train-only intake and sealed test split | `docs/STAGE10_DLULIB_FIRST_USE_EXTERNAL_VALIDATION.md` | Original ZIP, XLSX sources, train array hashes, sealed test label array hashes | Verified; original ZIP not redistributed |
| Six candidate positioning methods | Train only, six source-aligned model settings with fixed k=6 | `dlulib_stage10_models.py`, `dlulib_fit_positions.py` | 18 position-model weights and SHA-256 manifest | Trained on DLULIB training only |
| Exactly 33 descriptors and anchor | Original Stage9 descriptor definitions; synthetic 14-descriptor ESWA-native parity checks | `dlulib_features.py`, `tests/test_dlulib_stage10.py` | Source parity tests, check logs, 33 feature tensors in frozen prediction files | Source-equivalence confirmed synthetically; no direct raw-site release |
| Three JEPFormer seeds and CatBoost | Original source-trained Stage8 checkpoints, no DLULIB retraining | `dlulib_stage10_models.py`, `dlulib_predict_frozen.py` | Original weights/checkpoint hashes in private Stage8 capsule | Source-only weights reused unchanged |
| Predictions before ground truth | Distinct inference-only and sealed-label files; prescore SHA commitments and Drive upload | Method scripts, listed SHA hashes and protocol | Frozen no-GT predictions, prescore immutable manifests, upload metadata | Completed before first score, procedural separation |
| Prediction MAE/RMSE/bias/rank AUROC | Complete 6,500 test records, 39,000 candidates, all three floors | Aggregates CSV/JSON, `dlulib_score_frozen.py` | Full per-scan predictions and originally sealed GT, exact scorer outputs | Frozen external first-use complete |
| 95% MAE paired RP bootstrap | 650 RPs, 10 repeated test scans/RP, 4,000 bootstrap draws | CI reported in aggregate summary and method description | RP-level private per-RP forecast error differences and scorer | Descriptive, single-building inference only |
| Severe error underestimation | 3,363 candidate endpoints with error >=10 m | Full pooled model summary and by-floor/model aggregate files | Original error and model prediction arrays | Important limitation confirmed; not integrity bounds |
| Prospective unfamiliar building and unseen-RP transfer | DLULIB is one new building with same train/test reference coordinates | Disclosure in all Stage10 reports | Dataset source checks | Does NOT test unseen RP or multiple independent buildings |

For downstream model changes, DLULIB is now **used**. Do not reuse its score for model selection and later describe it as independent.
