# Reproduction completeness status

**What executes publicly:** synthetic-only feature generation and six-candidate Transformer/CatBoost smoke tests. Automated tests verify dimensions, the four candidate-shared geometry features, and missingness indicators.

**What has been executed privately:** recovered original Stage13 checkpoint replay; Stage3 descriptor-group controls; Stage4 direct-attention and pooled/independent comparisons. Only their aggregate metrics and method protocols are described publicly.

**What cannot yet be replayed publicly from this repository:** original full empirical error-prediction pipeline on all datasets, original per-scan results, every radio-map adapter, source-derived exact normalizer/weights, and incomplete legacy experiments. No private data or third-party benchmark is bundled.

**Proposed completeness gates:** dataset licenses, train-only data adapters, source script/version lineage, saved split SHA256, exact feature schema, model/target configuration, seed/config metadata, checkpoint SHA256, committed predictions before independent scoring, grouped statistics, CI replay, figure/SM linkage, privacy review and archived release DOI. Do not claim completed gates until verified.
