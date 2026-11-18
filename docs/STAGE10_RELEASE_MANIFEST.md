# Stage 10 — source-to-release verification manifest

**Date:** 2026-11-19 · **Stage:** frozen-source first-use DLULIB external validation · **Scope:** one new building, three known floors, test measurements at the original 650 training RP coordinates.

These are source-file SHA-256 digests from the locally verified Stage 10 public package. They permit independent comparison of repository files with the preserved release ZIP. They do not authenticate underlying empirical data, which remain restricted.

| Public repository path | SHA-256 |
|---|---|
| `README_STAGE10.md` | `a695143936d16d0e4b754b4ca7cf8931ec1690072f7f067598bea7f2ccefc6e9` |
| `docs/STAGE10_DLULIB_FIRST_USE_EXTERNAL_VALIDATION.md` | `4d7714103337aaf4de0aea3ca186be021eb3c693c6a14285216fa30fdc95ba70` |
| `docs/STAGE10_EXPERIMENT_TO_EVIDENCE_INDEX.md` | `46188a0a40b3b6f54a2ba86db5a34948d30669c44cbd980fd26261e9b5f0bfc5` |
| `src/jepformer/dlulib_features.py` | `4db011f55c5930989c334b811fc351b4c5fd0fdc76cadf8f6bb22037a03035eb` |
| `src/jepformer/dlulib_stage10_models.py` | `c9f69d84202c79ebada947b9d6b6b991b6a5639c11284a40078daa6caebcc151` |
| `tests/test_dlulib_stage10.py` | `b79110dde0488f4d5a05bb30e3c8e07621f7e2788791d544bc34025f4b272adb` |
| `scripts/dlulib_prepare.py` | `46d809f0db418eed4619ac5014168f1d01676f090729e55a676373bb233c0c87` |
| `scripts/dlulib_fit_positions.py` | `b73026b961cf29f94ae17e509c6d70b42f6d9c14f6a069df55fe8b6848209309` |
| `scripts/dlulib_predict_frozen.py` | `80a30cece93902b43b2805bd7de76553a8d4066f210e59a0e9f22779e1b160b0` |
| `scripts/dlulib_score_frozen.py` | `d0cf2e1c1cfb56e45d2de415d00e44ab4c6f9c75c7b526de82c7f92c4d8dbf30` |
| `results/aggregated/stage10_external_aggregate_summary.json` | `efef0af11f295fc32003aa631342330f898e9835732d422e614faa13043e5088` |
| `results/aggregated/stage10_external_pooled_seeds.csv` | `dd76853b8a07bed92516983c32c60474cb16d38e3e9e0944b6987f0cd8219660` |
| `results/aggregated/stage10_external_by_floor.csv` | `30d2db03c8dbd29a356c4c0fcccd7a37aceb5bd41c060fb02a253bceac16fafe` |
| `results/aggregated/stage10_external_by_estimator_and_floor.csv` | `5230428e7e2778e5fc79c5ae5a37a992c572b71dd0e49ad58410cedd918f66b5` |

## Source and pre-score commitments

- Original DLULIB source archive SHA-256: `bfa13bd1ae48dd9b636fcf1313ceb4ce25aa4b6495880ab8b4f689dbafad0953`
- Pre-score protocol SHA-256: `bef6f21829dd78c7c438e174c984b0098549592fd6f72a41b5fe98f14fe5a922`
- Prediction-freeze manifest SHA-256: `619979a10551064e17531fabeb8fc04ede35314ded6db474ffbe89c8a75df100`
- Owner-only complete research capsule SHA-256: `4a04a636fece5d420e378c6994eff0c34c82ab9335726cb924fae3cc83f7cc22`

## Release verification

- The public Stage 10 standalone synthetic tests: **5 passed** using `pytest -q tests/test_dlulib_stage10.py` on the extracted public ZIP.
- The published protocol, frozen code, and four non-identifying aggregate result tables are committed to the public repository.
- The complete original DLULIB dataset, sealed test coordinates, trained location estimators, source-trained numerical-error models, per-scan predictions, and restricted scientific logs are **not** distributed in the public repository.
- Portable input parser, model architecture, source-feature checks, and hash-based scorer were checked against their source predecessors in the owner-only research environment. Public reproduction of the original empirical outcome remains **conditional on authorized access to original source checkpoint weights**.
- No evidence of unseen-RP interpolation, unknown-floor inference, a calibrated statistical protection level, or universal model superiority is claimed.
- DLULIB has been inspected/scored once and is **no longer an untouched test** for future tuning.

## Journal source linkage

The manuscript v10 (28 pp), anonymous v10 (28 pp), supplement v10 (41 pp), original LaTeX source, and restricted research archive are preserved as separate checksum-registered files in the versioned owner-controlled Google Drive research checkpoint. Do not upload the manuscript or original dataset to the public code repository without a separate release and rights review.
