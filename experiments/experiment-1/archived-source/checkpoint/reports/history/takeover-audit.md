# Windows takeover gate: BLOCKED

Inspected project: C:\Users\agraj\Desktop\asi_dataset
Date: 2026-10-06

The takeover audit cannot pass. No data downloads, installations, model training, or scientific results were produced. Original files were not modified.

## Blocking transfer defects

- The entire asi_pipeline implementation package is absent. Transferred scripts/tests import asi_pipeline.dataset, modeling, train_cli, safety, temporal, remote_temporal and other helpers. Frozen split implementation, feature guards, training behavior and bootstrap mechanics therefore cannot be verified or executed.
- Scripts are under scripts/scripts and tests under tests/tests. Their parents[1]-relative imports/config paths do not resolve to the project root. This is a transfer-layout defect; no relocation or code changes were made.
- README_PIPELINE.md explicitly states candidate-level training resume is not implemented. The requested restartable scientific pipeline cannot be certified from this checkpoint.
- Referenced protocol history, results/audits manifests, and dependency lock/environment specification are absent from the supplied tree. Historical 35-pass status is unverified here. Full test execution/import validation was not completed.

## Frozen definitions readable from config

Four physical lifecycle labels; non-null workload primary grouping; SHA-256 JSON [seed, workload_id] first-64-bit threshold split with seed 20260927. Exact serialization/implementation cannot be certified without the package.

Twelve explicit candidates: leaves 15/31/63, min_data_in_leaf 20/100, feature_fraction 0.8/1.0 in config order. Candidate 6 is 31/20/1.0. Seeds 20260927/20260928/20260929; selection per model and seed; validation LogMAE; lowest candidate index tie-break; 200 rounds and patience 30. Train-only native categorical dictionaries; unseen/missing code -1. Target log1p(duration_hours). Primary R+P+A / R+P+A+O comparison excludes workload identity. Seven blacklisted predictors match the request.

Bootstrap specification: 1000 paired workload resamples, row-weighted aggregate losses, percentile 95% intervals, seed 20260927. Eight duration bins match the request. These are specification findings, not implementation verification.

## Scope reconciliation needed before execution

Frozen docs/config retain required R and R+P ablations in addition to the principal pair. The new request describes exactly five/six predictors for its M0/M1 comparison. Preserve this distinction and resolve execution scope before science if the request is intended to exclude those required ablations.

Config retains historical execution_permissions.remote_transfer=false and full_model_training=false. The current request explicitly authorizes staged execution, but no gates/config were changed; implementation must be available to determine how to apply current authorization while preserving scientific hashes and provenance.

## Historical environment evidence only

DATASET_AUDIT.md records PyArrow 25.0.1, DuckDB 1.5.5, pandas 3.0.6 and NumPy 2.5.3 on the former machine. The current request specifies LightGBM 4.7.0, SciPy 1.18.1 and PyYAML 6.0.3. No new Windows environment was created because the mandatory takeover gate is blocked.

## Required recovery

Provide the complete authoritative project transfer, especially asi_pipeline/, with original directory structure, dependency/version records, and any newer checkpoint/resume or full-population feasibility implementation. Do not reconstruct missing scientific code from the prompt. Then resume the takeover audit before downloading data.

Data, feasibility, science, final triage, and portable experiment export: NOT RUN. This is not a feasibility failure or a scientific KILL decision.

See takeover-file-manifest.json for SHA-256 inventory of every transferred file found.
