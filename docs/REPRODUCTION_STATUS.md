# Reproduction completeness status

**What executes publicly:** synthetic-only feature generation and six-candidate Transformer/CatBoost smoke tests. Automated tests verify dimensions, the four candidate-shared geometry features, and missingness indicators.

**What has been executed privately:** recovered original Stage13 checkpoint replay; Stage3 descriptor-group controls; Stage4 direct-attention and pooled/independent comparisons. Only their aggregate metrics and method protocols are described publicly.

**What cannot yet be replayed publicly from this repository:** original full empirical error-prediction pipeline on all datasets, original per-scan results, every radio-map adapter, source-derived exact normalizer/weights, and incomplete legacy experiments. No private data or third-party benchmark is bundled.

**Proposed completeness gates:** dataset licenses, train-only data adapters, source script/version lineage, saved split SHA256, exact feature schema, model/target configuration, seed/config metadata, checkpoint SHA256, committed predictions before independent scoring, grouped statistics, CI replay, figure/SM linkage, privacy review and archived release DOI. Do not claim completed gates until verified.

### Stage 8 reproduction boundary

Generic availability-aware training utilities and synthetic invariance tests now run publicly. Aggregate source-test comparisons and a post hoc matched-budget control are in three nonidentifying CSV tables. Exact empirical reproduction requires the restricted source radio maps, original checkpoint/feature-provenance records, original anchor coordinate derivation, frozen weights, private validation outputs and archived scoring scripts stored in owner-only Drive. The repository is not a substitute for all raw empirical artifacts. Dataset licenses and indoor geometry/privacy checks remain release blockers.

### Stage9 public verification status

Combined Stage8 plus Stage9 synthetic tests passed 15/15 locally. Stage9 adds no source-model fitting or adjustment, only post-inference metrics and an archive-file listing gate. The 48-row model/outage/threshold aggregate and six-family outputs are public; empirical raw inputs and 168 frozen scenario prediction arrays remain restricted. The proposed DLULIB ZIP was not retrieved; its original worksheet schema, feature-equivalence checks, and independent external MAE are not verified. Thus full empirical public reproducibility and prospective generalization remain OPEN.


### Stage 10 — source-compatible external pipeline added

The repository now includes complete **public reference source** for the DLULIB workbook importer, six coordinate-estimator fitting settings, 33-descriptor construction, source-model-compatible Transformer, source-only frozen inference, SHA-256 verification and a separate aggregate scorer. It also includes the Stage10 synthetic verification tests (five passed locally) and pooled, seed-specific, floor-specific and estimator-specific non-identifying results. The upstream 14-scan-feature parity test used the ESWA native extractor on synthetic records, and the portable workbook reader/scorer exactly matched the original frozen arrays and summary scores in a separate private replay.

**Public full empirical end-to-end reproduction is still CONDITIONAL**, not independently runnable from a checkout, because original Stage8 error-model checkpoint weights and source normalizer, the raw DLULIB source archive and the frozen per-scan evidence are not packaged publicly. Authorized users may obtain DLULIB from its original Zenodo record under applicable rights; source-trained weights and private research outputs require the user's permission and final privacy clearance. The owner-only Drive v10 checkpoint holds the original inputs and SHA-256 manifests; users should preserve a separate working folder and keep all sensitive outputs out of Git history. Stage9's earlier data-readiness status was superseded by the Stage10 first-use score, but its documented protocol remains part of the audit trail.
