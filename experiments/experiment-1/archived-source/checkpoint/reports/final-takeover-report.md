# WINDOWS FULL WORKLOAD-DISJOINT NOT FEASIBLE

The run stopped at the Windows feasibility preflight. No M0 or M1 feasibility worker started and no scientific training, test comparison, bootstrap, or scientific triage was performed. This is a safety decision under the observed machine state, not an empirical claim that the hardware can never run the experiment.

## Takeover and engineering

All 54 tests passed, including all original 35 tests and 19 added safeguard tests. Frozen protocol/config, metrics, original dataset builder, scientific feature/encoding/split helpers, candidates, seeds and thresholds remain unchanged. Engineering safeguards and their independent review are detailed in engineering-change-report.md. The only original-test edit adds required synthetic selection setup and extra restart assertions; all original assertions were preserved.

Fresh Windows environment: Python 3.12.14, CPU LightGBM 4.7.0, SciPy 1.18.1, PyYAML 6.0.3, PyArrow 25.0.1, DuckDB 1.5.5, NumPy 2.5.3, pandas 3.0.6. No GPU training.

## Official data

URL: https://tre-clusterdata.oss-cn-hangzhou.aliyuncs.com/cluster-trace-gpu-v2026/data/asi_opensource_job_execution_summary.zip
Download started: 2026-10-06T19:11:37.745010+00:00
Download completed: 2026-10-06T19:12:25.585636+00:00
Archive bytes: 1,188,295,031
Archive SHA-256: 2dd48db5c5a532d0b1504c67522ed7f6929df6efd5c22abc4a921349aa37ff4f
Extracted bytes: 1,188,294,827
Extracted SHA-256: acd868090a64c8852ee2586510a0384111aed0378905f5405d2be6779062e963

Source reproduction PASSED: 40,522,321 rows, exact 14-field schema, all six expected lifecycle counts, 36,685,018 unique pod IDs, 501,183 unique workloads and 4,792,402 non-null workload rows. No missing/nonfinite/nonpositive durations. Median 0.4222222222 h; p95 9.6888888889 h; p99 59.6222222222 h; maximum 1824 h. Raw archive/Parquet hashes are recorded and files marked read-only.

Primary population PASSED: 4,709,624 rows and 473,265 workloads. No sampling, aggregation, imputed IDs, target encoding or category changes.

| Split | Rows | Workloads | Training | Offline inference | Online inference | Dev |
|---|---:|---:|---:|---:|---:|---:|
| Train | 3,339,542 | 331,486 | 2,091,126 | 764,755 | 465,571 | 18,090 |
| Validation | 658,761 | 71,074 | 426,146 | 131,683 | 95,598 | 5,334 |
| Test | 711,321 | 70,705 | 442,275 | 134,873 | 128,791 | 5,382 |

All counts match exactly, with zero workload overlap. Split seed remains 20260927 and the original assignment function is used.

Canonical artifact PASSED fresh-process reopen validation, independent split-map comparison, frozen per-workload assignment verification and streaming exact source-value/physical-row correspondence.
Artifact bytes: 85,907,015
Artifact SHA-256: 10a3a86c977701c3c26f0bdce231aeb294676d71fef772b96309ceab3d21b0a0
Compression: ZSTD; 406 row groups, each at most 100,000 rows. Exact row-group sizes/schema/code/config/protocol/source hashes are in canonical-data-manifest.json.
Canonical manifest SHA-256: 57a2fb4187084d8121f77532d7cfbb1519c757106780901072334021ccc8bced

## Feasibility

Status: FAILED — preflight safety refusal.
Available physical memory: 3.879 GiB.
Available commit headroom: 2.258 GiB.
Required preflight headroom: at least 3 GiB in both.
Worker launch: none. Worker RSS, preparation/training/prediction time, model size and M1 resources: not measured, because no worker started. No worker was killed and no OOM was attempted. Worker exit status is null (not launched).

The supervisor's resource trace records system commit/limit and the available paging observation. The first PDH sample needs a sampling interval, so this preflight-only run has no sustained-paging measurement. Direct pagefile-use bytes were unavailable. No pagefile settings were changed. The earlier live PDH probe confirmed the counter was callable; it does not establish paging behavior during full training.

The gate remains failed and blocks scientific execution. Safety thresholds were not relaxed, and no data, feature, split, target, candidate or CPU setting was altered in response.

## Science and decision

Scientific selected candidates, per-seed metrics, bootstrap intervals, strata, finite-execution results and final contribution triage: NOT RUN. No CONTINUE/KILL research classification is justified. The required execution outcome is WINDOWS FULL WORKLOAD-DISJOINT NOT FEASIBLE.

## Preserved checkpoint

The project, fresh environment, raw files, canonical artifact, split map, code, tests and manifests remain under C:\Users\agraj\Desktop\asi_dataset. The downloadable stopped-run checkpoint includes canonical data, code/tests, split map, environment specifications and all evidence needed to resume after a separately authorized change in machine conditions. It omits the virtual environment, raw archive/Parquet, caches and spill files. It is not the final scientific-results package.
