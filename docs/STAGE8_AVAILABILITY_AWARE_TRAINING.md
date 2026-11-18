# Stage 8 scientific report: Availability-aware numerical error prediction

**19 November 2026 · Working evidence, not a prospectively new external evaluation**

## Research question and evidence lineage

The previously frozen six-estimator numerical error-prediction models showed progressively worse forecast accuracy when one to three position estimators were made unavailable (Stage 7). Stage 8 evaluates whether simulating method outages during training makes the existing six-token representation more robust, as compared with the original trained models and a matched-budget repeated-full-input control. This is a distinct exploratory extension; the EAAI main manuscript continues to identify cross-estimator geometry and its cross-learner contribution as the primary demonstrated advance.

The source splits are 5,450 development scans, 4,089 calibration scans, and 4,090 historical test scans. Six existing candidate estimators yield up to six scalar error targets per scan. The original 33-value descriptors comprise 14 scan/radio-map measurements, 12 cross-estimator geometry measurements, and seven candidate-local reference descriptors; missingness flags are applied after normalization. The source test and all its six families were previously inspected: no result here qualifies as a newly untouched-family test.

## Exact controlled protocol

The new availability-aware branch creates four examples per development scan: one fully available plus one randomly selected configuration of 1, 2, and 3 missing estimators. All 6, 15, and 20 respective outage combinations are included at evaluation. Feature geometry for surviving candidates is recomputed from available coordinates only, with the original training-map diagnostic anchor; an unavailable reference estimator makes its corresponding features undefined. Dropped candidates do not contribute to the numerical-error loss; JEPFormer attention excludes missing keys and loss contributions, including pairwise supervision when WKNN is missing. The original source normalization parameters are retained and the training/test estimators are not recalibrated with test truth. Models and metadata were SHA-256 committed before historical-test prediction/scoring, and prediction files committed before target-error scoring. This is procedural source-test label isolation, not independently blind validation.

JEPFormer uses three independently fitted seeds (11, 21, 31); CatBoost one fixed seed (2026). The repeated-full-control trains with four full-availability copies per development scan using otherwise matched learners and update budgets. That control was formulated after initial availability-aware results (post hoc); its calibration distribution differs, so the comparison cannot isolate a unique augmentation mechanism beyond all training-control differences.

## Numerical forecast error MAE (m), historical source test

| Unavailable candidates | Patterns | Frozen JEPFormer | Repeat-full JEPFormer | Outage-trained JEPFormer | Frozen CatBoost | Repeat-full CatBoost | Outage-trained CatBoost |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1.894 | 1.896 | 1.832 | 1.970 | 1.948 | 1.991 |
| 1 | 6 | 2.222 | 2.239 | 1.873 | 2.183 | 2.160 | 2.044 |
| 2 | 15 | 2.611 | 2.655 | 1.937 | 2.455 | 2.435 | 2.125 |
| 3 | 20 | 3.011 | 3.082 | 2.052 | 2.636 | 2.615 | 2.209 |

Values are equally averaged over combinations of an outage size and scored over surviving candidate positions; the full-input result scores all candidates. JEPFormer rows average three seeds. CatBoost does not use repeated-seed uncertainty. Relative to the repeated-full control, JEPFormer improves by 0.064, 0.366, 0.718, and 1.030 m for 0–3 unavailable candidates. CatBoost changes by −0.043, +0.115, +0.310, and +0.406 m. Six-family descriptive bootstrap intervals for these changes respectively are JEP [0.034,0.086], [0.250,0.447], [0.502,0.886], [0.732,1.226], and Cat [−0.065,−0.002], [0.065,0.173], [0.183,0.433], [0.240,0.562]. They are not independent-sample confidence bounds. Both methods show positive retrospective outage benefits in all six historical families for 1–3 missing candidates; for CatBoost the 1-missing effect is positive in five of six specific missing-estimator combinations. Severe-error underprediction persists.

## Exact-geometry correction and audit trail

An initial scoring implementation reconstructed one diagnostic anchor-distance descriptor from clipped normalized inputs, causing small deviations from the original geometry construction. The original first scoring outputs and script have been preserved in the *private* archive for a full audit, but they are superseded by the corrected `score_stage8_sealed_exact.py`. That version restores the source diagnostic radio-map anchor directly, does not consult query ground truth for geometry, and was compared against the original construction with max discrepancy below 5e−7 in the checked conditions. The frozen trained weights were **not changed**. Their final corrected predictions are separately hashed and retained.

## Reproducibility and publication boundary

Public GitHub receives only the synthesized feature logic, availability-aware training and masking utilities, tests, non-identifying aggregate tables, study protocol, and caveats. The *private* Drive checkpoint retains exact input adapters, code, checkpoint SHA-256 records, frozen model weights, inference outputs, per-scan historical predictions, scoring scripts, and seed-level/family-level experiment records. Neither simulated labels nor synthetic demo performance are reported as measured scientific accuracy. Data-license clearance and an independent geometric/identifier audit are required before empirical release.

**Still unresolved:** prospectively unused site or independently acquired family evaluated after all model choices are frozen; estimator replacement and variable-cardinality tests beyond fixed six identities; loss calibration and persistent >10 m error underprediction; full inference and feature construction runtime; rights to distribute every dataset and figure. Version 8 is a research checkpoint, not final journal submission approval.

## Public quickstart

`pytest -q tests` verifies synthetic feature and mask invariants. The archive contains no private weights or raw empirical data.
