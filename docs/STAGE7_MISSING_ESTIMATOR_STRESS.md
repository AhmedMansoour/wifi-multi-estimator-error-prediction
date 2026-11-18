# Stage 7: retrospective estimator-outage stress test

**Study date:** 18 November 2026. **Scope:** Previously inspected source test (4,090 scans, six candidate positioning methods). This is not a previously unseen external benchmark, and **no model was retrained**.

We evaluated all 41 sets of one, two, or three unavailable methods. The six methods are CatBoost, Extra Trees, Gradient Boosting, KNN, Random Forest, and WKNN. For each absent-method configuration, input geometry was regenerated using only the remaining candidate coordinates. The seven local radio-map support descriptors were preserved for remaining methods. The two reference-to-method geometric features are marked missing when KNN or WKNN is unavailable; other scan-level observations do not change. The original source-fitted imputation and normalization remain fixed. JEPFormer also applies an attention key-padding mask for the unavailable tokens, compared with a diagnostic unmasked-placeholder control. Numerical MAE scores **only available** estimates, and all configurations are compared with the unchanged model on exactly the same remaining estimates. Neither ground-truth location nor realized positioning error is an inference input.

## Forecast MAE (m)

| Missing methods | Patterns | CatBoost | JEPFormer attention masked | JEPFormer unmasked placeholder |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 1.970 | 1.894 | 1.894 |
| 1 | 6 | 2.183 | 2.222 | 2.442 |
| 2 | 15 | 2.455 | 2.611 | 2.884 |
| 3 | 20 | 2.636 | 3.011 | 3.284 |

JEPFormer values average three original model seeds (11, 21, 31); CatBoost uses the fixed seed 2026. Pattern values are equally weighted. Outages of KNN and WKNN are especially harmful because the original geometry representation uses those methods as fixed references. The results demonstrate a **deployment limitation**, not that the fixed-trained models are robust to missing or replacement estimator types.

A synthetic-safe pure-numpy reference implementation is provided in `src/jepformer/availability.py`, with deterministic non-dependence tests in `tests/test_availability.py`. The original source inputs, trained checkpoints, per-scan predictions, and exact scenario logs are restricted in the owner's scientific archive and are **not** included in this public repository.

### Scientific caveats

- The models were trained with all six candidate-method outputs. Applying missingness flags and attention masks does not confer independently validated robustness.
- Equal-weighted outage patterns on the same test scans are not independent datasets or field failures; uncertainty from repeated configurations must not be interpreted as population-level confidence.
- The figures concern error-forecast MAE, not positioning accuracy, coverage, certified integrity, or uncertainty bounds.
- Replacing an estimator with a new model changes its identity/behavior and requires a separately designed training and validation protocol.
