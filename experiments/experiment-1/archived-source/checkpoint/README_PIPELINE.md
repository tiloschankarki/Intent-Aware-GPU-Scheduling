# Frozen ASI pipeline checkpoint

Read docs/protocol.md and config/protocol.yaml first. Previous protocol versions are preserved under docs/protocol_versions/checkpoint1. The source and historical temporal/audit artifacts remain unchanged.

## Commands

From the project directory, using its existing environment:

```sh
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B scripts/03_build_dataset.py --source part-000.parquet --output artifacts/datasets/smoke-new --limit 10000
.venv/bin/python -B scripts/04_train_baselines.py --dataset artifacts/datasets/smoke-new --output-root artifacts/models/smoke-new
.venv/bin/python -B scripts/05_lifecycle_ablation.py --dataset artifacts/datasets/smoke-new --output-root artifacts/models/smoke-new
.venv/bin/python -B scripts/06_generalization.py --m0-dir artifacts/models/smoke-new/workload_disjoint/broad/R+P+A/20260927/m0 --m1-dir artifacts/models/smoke-new/workload_disjoint/broad/R+P+A/20260927/m1 --config config/protocol.yaml --output-dir results/smoke-new
```

The training CLIs use all three model seeds. Repeat evaluation per seed; --population finite and --evaluation random_execution select frozen secondary analyses. Required R and R+P ablations are available for separately approved full runs; the current bounded dry-run scope is the principal R+P+A comparison. Test data is loaded only after validation-based selection is fixed.

`run_dry_run.py --source part-000.parquet --output artifacts/dry_run_NEW` executes all four population/evaluation combinations, three seeds, two model sides and all twelve candidate configurations. It reports mechanics/resources only. Output paths must be new; existing artifacts are never overwritten. Completed manifests are completion markers. Incomplete directories with failure.json should be retained and a fresh run root selected. Candidate-level training resume is not implemented; temporal scanning resumes per completed hour.

`02_build_temporal_map.py` implements selective, bounded remote ZIP access and per-hour DuckDB checkpoints. Both remote permission gates are false; no remote execution is authorized. Local synthetic fixture mode must use a source of at most 10000 rows. The authoritative map is a table in the new output's temporal.duckdb; historical temporal_map.parquet and eligible D109H00 Parquet are never modified. Received response body bytes and conservative request reservations are logged separately; HTTP/TLS overhead and historical transfer remain unknown. Raw files with `.raw.parquet` suffix in the output are disposable staging only after successful checkpoint; failed raw files are preserved.

## Resource limitations

Dataset construction streams batches and writes compact reusable Parquet; it never loads all 40M rows into pandas. Training currently loads the selected training and validation populations into memory, then test rows after selection. This is suitable for a bounded dry run; full broad-population runs on an 8-GiB laptop require separate measured sizing and likely a more memory-efficient loader or a larger machine. Do not treat the small smoke run as certification that full training fits.

No dataset release metadata was inferred. SHA-256 identifies the local source bytes, not an independently verified release version. Source ordinals are storage locators only; no outcome-based execution key is manufactured. The random reference can have repeated pods/workloads across splits; it is explicitly weaker than workload-disjoint evaluation.
