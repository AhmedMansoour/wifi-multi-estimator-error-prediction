# Stage 9 — Retrospective severe-error behavior of frozen v8 predictors

**Status:** Executed and independently replayed from archived frozen Stage 8 prediction tensors. **NOT** a new externally unseen dataset or prespecified prospective test. The final v8 architecture, predictors, and source-test labels were previously examined in the research program; these calculations are post hoc diagnostics of previously stored forecasts. No models were retrained, reweighted, recalibrated, or chosen based on these findings.

## Scientific question

Does availability-aware training retain the ability to distinguish true large positioning errors when one to three of the fixed six candidate estimators are absent, and does good discrimination imply accurate *magnitude* forecasting?

## Exact evaluation protocol

- Source evaluation: 4,090 historically inspected test scans, six candidate error targets per scan, six dataset families, four model configurations (outage-trained vs fourfold repeated-full inputs, JEPFormer vs CatBoost).
- Original frozen Stage 8 prediction tensors are indexed by learner, seed, missing-estimator combination and source scan. The 168 learner/seed/pattern combinations were replayed against the original source-test true errors; there are 41 distinct outage patterns plus full availability.
- The same target mask is used for compared models. Absent candidates are excluded from both denominators and sums; no unavailable coordinate or test ground truth is an inference feature.
- The **actual** horizontal positioning error determines the retrospective severe-error event (`error >= 7`, `>= 10`, or `>= 20 m`) *only after predictions have been frozen*. The primary diagnostic reported here uses `>= 10 m`, distinct from the auxiliary classification head's 7-m label.
- For each model/seed/outage pattern: report overall forecast MAE, conditional MAE on severe targets, signed prediction-minus-actual bias, underprediction fraction on severe targets, AUROC and AP using predicted numerical error as the severity score. ROC recall at an empirical 5% false-positive operating point is **post hoc ranking analysis**, not a fixed operational decision threshold.
- Each missing-count condition averages metrics **equally across combinations**, not by the number of surviving candidates; JEPFormer then reports mean across seeds 11/21/31, and CatBoost is a single fixed seed. Per-family summaries use the original six family memberships and contain only aggregates.
- The **fourfold repeated-full control was designed after the initial Stage 8 results** and cannot be described as independently preregistered. The historical test was repeatedly inspected and is not a newly untouched external benchmark.

## Key findings at actual error >= 10 m

| Model and training | Missing candidates | Tail MAE (m) | Tail underprediction | AUROC | AP |
|---|---:|---:|---:|---:|---:|
| JEPFormer, outage-trained | 0 | 5.212 | 65.7% | .956 | .846 |
| JEPFormer, outage-trained | 1 | 5.334 | 66.8% | .955 | .842 |
| JEPFormer, outage-trained | 2 | 5.466 | 68.8% | .952 | .832 |
| JEPFormer, outage-trained | 3 | 5.823 | 70.3% | .948 | .817 |
| JEPFormer, fourfold repeated-full | 0 | 5.399 | 72.4% | .955 | .842 |
| JEPFormer, fourfold repeated-full | 1 | 6.404 | 75.5% | .947 | .806 |
| JEPFormer, fourfold repeated-full | 2 | 7.426 | 77.8% | .935 | .760 |
| JEPFormer, fourfold repeated-full | 3 | 8.325 | 77.7% | .922 | .714 |
| CatBoost, outage-trained | 0 | 5.291 | 74.5% | .954 | .831 |
| CatBoost, outage-trained | 1 | 5.368 | 72.9% | .954 | .827 |
| CatBoost, outage-trained | 2 | 5.513 | 74.3% | .952 | .820 |
| CatBoost, outage-trained | 3 | 5.860 | 76.0% | .950 | .811 |
| CatBoost, fourfold repeated-full | 0 | 5.154 | 72.3% | .956 | .836 |
| CatBoost, fourfold repeated-full | 1 | 5.548 | 71.8% | .953 | .819 |
| CatBoost, fourfold repeated-full | 2 | 6.007 | 71.5% | .948 | .798 |
| CatBoost, fourfold repeated-full | 3 | 6.637 | 74.0% | .944 | .779 |

The actual severe-case prevalence is 3,947 / 24,540 (16.1%) at full availability. Source errors range as high as ~163 m. Discrimination remains relatively strong while severe-case numerical underprediction remains common. Availability-aware training especially improves **conditional tail MAE under outages** compared with the repeated-full control. It does not uniformly improve signed bias or underprediction frequency, especially for CatBoost. **Do not infer calibrated risk scores, protection levels, safe acceptance probabilities, or improved downstream position selection.**

## Reproducibility and confidentiality

The public release includes `src/jepformer/tail_diagnostics.py`, deterministic unit tests, this protocol, the 48-row aggregated threshold-by-outage table, and a six-family summary (anonymous family identifiers). It does **not** contain raw site-specific scans, BSSIDs, reported coordinates, empirical predictions or true-error vectors. The private Drive archive records the two original Stage 8 prediction tensor hashes, full per-pattern and per-seed outcomes, the exact analysis script, and a SHA-256 inventory. An external independent observer cannot reproduce paper numerical results from the public code alone until licensed/cleared research datasets or a secure reproducibility route becomes available.

**No additional benchmark was scored in this stage.** A separately documented DLULIB dataset is proposed for a future *first-use external* test, subject to source file availability, model/feature alignment, privacy/rights audit and pre-score prediction freeze.
