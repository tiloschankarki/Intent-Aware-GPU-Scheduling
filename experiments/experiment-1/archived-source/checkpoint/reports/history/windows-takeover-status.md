# Windows environment and takeover status

Date: 2026-10-06. Project: C:\Users\agraj\Desktop\asi_dataset.

## Completed

The missing asi_pipeline package and nested folder defects have been corrected by the user. A fresh Windows virtual environment was created at .venv-windows. User-approved exact versions installed successfully: LightGBM 4.7.0, SciPy 1.18.1, PyYAML 6.0.3, PyArrow 25.0.1, DuckDB 1.5.5, NumPy 2.5.3, pandas 3.0.6. Python is 3.12.14. Transitive dependencies are recorded in requirements-windows.txt and windows-environment.json. pip check reports no broken requirements.

Full transferred suite: 35 passed, 0 failed, 0 skipped. This includes real LightGBM training on synthetic test fixtures only. No research-data model was trained. All 21 Python files parse, and every asi_pipeline module imports. Tests ran with PYTHONUTF8=1 and -B to avoid Windows default-text-encoding differences and bytecode writes.

Portability modification remains limited to asi_pipeline/safety.py: Windows staged-file flush uses r+b; atomic no-overwrite hard-link publication remains unchanged; unsupported POSIX directory fsync is skipped on Windows. Existing no-overwrite test passes. No scientific definitions or tests changed. Windows directory metadata power-loss durability is not asserted equivalent to POSIX directory fsync. scripts/run_dry_run.py still uses Unix-only resource and is not a Windows feasibility worker.

## Takeover gate: NOT PASSED

Passing the transferred tests does not establish readiness for the newly required execution sequence. The supplied implementation is a smoke-run checkpoint and lacks mandatory full-run safeguards:

1. asi_pipeline/modeling.py train_one keeps candidate scores and the selected model only in memory until AFTER test data is loaded and predictions are produced. candidates.json and the selected-candidate manifest are written afterward. This conflicts with the requested stage C persisted selection before stage D test evaluation. The code does select using validation only; no test-driven selection was observed. The failure is durable sequencing, not evidence of leakage.
2. Candidate training has no checkpoint/resume. train_cli.py rejects even completed output paths, and README_PIPELINE.md explicitly documents candidate-level resume as unimplemented. This fails the requested restartability contract.
3. The existing dataset builder retains null-workload rows for the broad reference dataset. It is not the requested 4,709,624-row primary-only canonical artifact builder. The primary loader correctly filters grouped_split non-null, but construction needs a dedicated primary artifact path with fresh-disk exact validation.
4. No full-population Windows feasibility controller implementing the required candidate-6-only workers and RAM/commit/paging termination behavior is supplied.

These are execution-engineering gaps, beyond the single portability fix already applied. Do not claim the takeover gate passed or download/train past it. The frozen config also still has historical full_model_training=false; current user authorization must be represented explicitly without silently rewriting the authoritative protocol.

The frozen protocol includes required R and R+P pairs as well as the principal five/six-feature pair. Preserve those definitions; do not quietly delete them when implementing the narrowed full-population execution plan.

## Environment snapshot

Windows 11 build 26200; AMD Ryzen 9 8945HS; 16 logical CPUs. Visible physical RAM 15.29 GiB, available about 3.26 GiB at measurement; system commit headroom about 2.79 GiB. Disk free about 546.75 GiB. Pagefile registry reports ?: pagefile.sys (full literal stored in JSON). Direct pagefile usage was not measurable via CIM (access denied); system commit is not pagefile usage. These are a snapshot, not a full-population feasibility result. No OOM probe was attempted.

## Not run

Official source download; source/population/split reproduction; canonical artifact construction; candidate-6 full-population feasibility; scientific selection/test/bootstrap; scientific triage; final portable research package. There is no basis for any of the three scientific triage classifications, or for declaring Windows full-population infeasibility.

## Recovery

Use a newer authoritative execution checkpoint if available, or explicitly authorize an execution-layer amendment adding durable validation-only selection/checkpoints, primary canonical construction/validation, and Windows safety monitoring while preserving the frozen scientific definitions. Reaudit and rerun tests before advancing to data acquisition.

Evidence: windows-tests.txt, requirements-windows.txt, windows-environment.json, takeover-current-hashes.json. Earlier reports remain historical and are superseded for environment and test status by this report.
