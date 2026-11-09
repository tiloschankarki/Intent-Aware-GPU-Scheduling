# Windows engineering-change report

Safeguards validated on 2026-10-06. Full suite: **54 passed, 0 failed** (all original 35 tests retained, plus 19 new tests). Original test names and assertion ASTs were programmatically verified as preserved. Independent code review found no remaining blockers after fixes. No ASI research data was downloaded during implementation.

## Scientific invariance

config/protocol.yaml, docs/protocol.md, docs/DATASET_AUDIT.md, asi_pipeline/metrics.py and the original asi_pipeline/dataset.py are byte-for-byte unchanged from the baseline. Frozen feature, encoding, workload-assignment and row-hash helper ASTs are unchanged. All 12 candidate records, selected candidates and test predictions are exactly identical between baseline and updated fitting paths on an independent synthetic fixture for M0 and M1, seed 20260927. This is engineering evidence, not an ASI result. Expected LightGBM missing-category warnings occurred equally in both paths.

No population, split seed, features, categorical dictionary rules, target transform, model parameters/candidates, model seeds, selection criterion, metrics, bootstrap or thresholds were altered. LightGBM remains 4.7.0 on CPU. Authorization is recorded separately in windows_run/authorization.json; historical frozen permission flags were not rewritten.

## Files added

- asi_pipeline/checkpoints.py: atomic completed directories, manifest seals, artifact hashes, source/data/protocol/split/code/version/context binding. Incomplete staging directories never count as complete; incompatible completed units fail closed.
- asi_pipeline/execution.py: per-candidate training checkpoints; validation-only selection saved before test access; validated model/encoding reuse; separate prediction; experiment-wide freeze enforcement; strict data-file inventory; compatible output aliases. A cooperative stop callback only aborts unsafe execution and never changes fitting parameters.
- asi_pipeline/windows_monitor.py: fresh-process supervision, worker RSS/peak RSS/commit/fault counts, system physical/commit headroom, live PDH hard-paging disk-read counter, wall time, logs, spill growth, exit status and fail-closed sensor errors. Windows job-object cleanup prevents orphan workers if the supervisor dies.
- asi_pipeline/feasibility.py: exact candidate 6, seed 20260927, 2-thread M0 then M1, separate workers. Reports resources only, never effect estimates. Prediction timing uses validation; test data remains untouched. Entire canonical population is validated first.
- asi_pipeline/primary_data.py: official execution-summary acquisition and hashing; exact source/population/split gates; streamed lossless primary-only canonical Parquet; fresh-process reopen/count checks; exact split-function/map and retained source-value/row-order verification. Physical row ordinal is provenance only.
- asi_pipeline/scientific_run.py: required R, R+P, R+P+A pairs for broad and finite workload-disjoint populations and three seeds; all 36 model selections freeze before any test worker. Does not run broad 40M/random or temporal science.
- scripts/prepare_windows.py, windows_feasibility.py, run_windows_science.py: explicit phase entry points.
- tests/test_engineering.py, tests/test_primary_data.py: checkpoint, freeze, resume, stale/partial/tampered input, monitor, exact-gate, split/content validation coverage.

## Files modified

- asi_pipeline/modeling.py: unchanged scientific helpers; train_one delegates to the checkpointed compatibility wrapper; low-level test loading now demands validated selection.
- asi_pipeline/train_cli.py: explicit select/test phases and separately supplied authorization; reuses verified compatible completed units.
- scripts/06_generalization.py: requires a valid individual/global selection before full-data evaluation; publishes evaluation and bootstrap atomically with hashes. Metric formulas unchanged.
- tests/test_metrics.py: existing fixture now creates the required synthetic selection manifest; every original assertion remains; adds interruption/retry assertions.

Earlier Windows portability fix (before this engineering baseline): safety.py uses a writable staged-file handle for Windows fsync, retains exclusive hard-link publication, and skips unsupported directory fsync on Windows. Windows directory metadata power-loss durability is not asserted equivalent to POSIX directory fsync. UTF-8 mode is enabled for execution.

## Safety policy fixed before feasibility

Preflight requires at least 3 GiB available physical memory and 3 GiB commit headroom. Immediate stop below 1 GiB in either; stop after 15 seconds below 2 GiB. Sustained hard paging stops after 15 seconds at over 1,000 disk reads/second, or over 200 with less than 3 GiB available RAM. Worker gets a cooperative stop marker, then forced termination after 5 seconds if necessary. A safety stop or monitoring error yields FAILED and blocks science. No retry with smaller data or altered scientific inputs. Direct pagefile-use bytes are unavailable; PDH hard-paging activity and commit are recorded separately, without claiming equivalence.

## Evidence

engineering-tests.txt: complete passing suite.
engineering-change-manifest.json: exact file inventory, changes, scientific hashes, code state and package versions.
scientific-invariance-probe.json: original-versus-updated synthetic fitting comparison.
requirements-windows.txt and windows-environment.json: Windows environment record.

Engineering safeguards pass. Next authorized stage: acquire only the official ASI execution-summary archive, then enforce the mandatory numerical and feasibility gates. No scientific feasibility or outcome is claimed by this report.
