# ASI research checkpoint — 2026-10-06

**SCIENTIFIC EXPERIMENT HAS NOT YET RUN.**

**WINDOWS FULL WORKLOAD-DISJOINT NOT FEASIBLE** is the preserved engineering outcome. Neither full-population feasibility M0 nor M1 started. There is currently **NO scientific evidence for or against the lifecycle-type hypothesis from this experiment**. Tests and synthetic fitting checks are not research results. Do not convert this execution stop into a negative scientific conclusion or a CONTINUE/KILL contribution decision.

This checkpoint is archival/provenance only. No training or feasibility retry was run while preparing it. Existing artifacts were not deleted or rewritten. The original project is `C:UsersagrajDesktopasi_dataset`. Paths below are relative to the extracted `asi_checkpoint_2026-10-06/` root unless identified as historical absolute paths. Read this file first; the old READMEs describe earlier implementation checkpoints.

## Authority and evidence

**config/protocol.yaml remains authoritative.** `docs/protocol.md` explains the frozen scientific design. This summary does not replace either. A material scientific conflict requires stopping for an explicit research decision.

- Protocol ID: `asi-lifecycle-frozen-v2-pretraining`.
- Config file SHA-256: `4908e86e7526c8ecc298facd46089ac94fd4dec5094eee47af24987237653e61`.
- Protocol document SHA-256: `7c58289899902417fe9cdba0bac93309d231eb7248b1b077414e1efd02b3d71c`.
- Semantic config-content SHA-256: `a8d8a96556b2868067db7af63e04201c7da0c509afc4c101fdc5638d09b6d2ea` (distinct from the byte hash).
- Current evidence: `windows_run/raw/source-manifest.json`, `windows_run/audit/`, `windows_run/canonical/`, `windows_run/feasibility/`, and `reports/final-takeover-report.md`.
- Engineering record: `reports/engineering-change-report.md`, `reports/engineering-change-manifest.json`, `reports/engineering-tests.txt`.
- Earlier reports in `reports/history/` are retained as dated history; their missing-code/dependency/readiness statements are superseded by the final reports.
- `provenance/requests/` preserves the Windows takeover request, engineering authorization and this archival request. Absolute paths in old manifests are historical provenance, not instructions to recreate the old machine's directory layout.

## Frozen research question and constructs

`docs/protocol.md` asks: “Does prospective execution/lifecycle type add predictive information for individual GPU/ML execution duration beyond available prospective controls, including on unseen workloads?”

The exact general question in `docs/HANDOFF_ORIGINAL.txt`, section 1, is: “Does prospective execution/lifecycle type provide incremental predictive value for individual GPU/ML job runtime beyond other prospective information?” Its ASI-specific question is: “Does job_type_public improve individual execution-duration prediction beyond the prospective controls available in ASI, and does that improvement persist under stronger generalization settings such as unseen workloads?”

This is a predictive/information-contribution study, not a causal study. Preserve **prospective execution/lifecycle type**, not generic “experimental objective.”

| Construct | Meaning | ASI role |
|---|---|---|
| L1 | Prospective execution/lifecycle type: training, development/debugging, evaluation, online/offline inference, etc. | `job_type_public`, variable of interest |
| L2 | Planned computational scope: epochs, steps, iterations, trials, token budgets, etc. | Desired controls are not adequately public in ASI |
| L3 | Application/model semantics | `model_type_public`, control |
| L4 | Workload/configuration identity | `workload_id`, configuration proxy; not a user ID |

ASI does not expose all desired L2, user/tenant or history controls. Do not invent them, imply they were controlled, or infer lifecycle from runtime/outcomes.

## What was already ruled out or narrowed

These are inherited project conclusions from `docs/HANDOFF_ORIGINAL.txt`, sections 3–4, not new experiments or independently repeated literature searches:

- The original broad “experimental objective” idea was narrowed because public traces lacked a sufficiently clean prospective label.
- AcmeTrace was rejected: the handoff reports author correspondence that labels used post-execution job-name/duration information, creating target-leakage concerns for duration prediction. The original correspondence is not in this transfer.
- PAI semantics were primarily L3/L4/task-role information, not a clean prospective job-level L1 label; do not stretch them into L1.
- The completion-aware/scheduler-feedback direction was dropped after prior-art auditing found substantial precedent.
- Generic “semantics improves runtime prediction” is too broad; the surviving question is incremental lifecycle information under strong controls/generalization.
- The bounded prior-art search is not proof that no related paper exists, and lifecycle metadata itself is not claimed novel.
- The historical exact matched cohort (46 configurations, 784 rows) is only a secondary diagnostic, never a substitute for the primary population. Its source artifacts were not transferred.
- The D109H00 temporal linkage and D108–D110 plan are historical, separate work. No temporal study or `pod_hourly` download is authorized by this checkpoint's execution path.

The lifecycle hypothesis itself has not been ruled in or ruled out.

## Dataset and provenance

Dataset attribution: **Alibaba ASI / GPU Cluster Trace v2026**, execution summary. The Windows run downloaded the official named archive freshly:

https://tre-clusterdata.oss-cn-hangzhou.aliyuncs.com/cluster-trace-gpu-v2026/data/asi_opensource_job_execution_summary.zip

| Item | Recorded value |
|---|---|
| Download started UTC | 2026-10-06T19:11:37.745010+00:00 |
| Download completed UTC | 2026-10-06T19:12:25.585636+00:00 |
| Archive bytes | 1,188,295,031 |
| Archive SHA-256 | `2dd48db5c5a532d0b1504c67522ed7f6929df6efd5c22abc4a921349aa37ff4f` |
| ZIP member | `asi_opensource_job_execution_summary/part-000.parquet` |
| Extracted Parquet bytes | 1,188,294,827 |
| Extracted Parquet SHA-256 | `acd868090a64c8852ee2586510a0384111aed0378905f5405d2be6779062e963` |

Fresh download, exact hashes, schema and reproduced statistics establish the bytes used. The transfer did not contain an independent publisher-signed checksum/release identifier, and source Arrow metadata lacked an independent release identifier. Do not turn release attribution into a stronger independently authenticated claim.

Source schema (exact required 14 columns):

| Column | Type |
|---|---|
| `pod_id` | string |
| `workload_id` | string |
| `server_id` | string |
| `gpu_spec_public` | string |
| `priority_class` | string |
| `job_type_public` | string |
| `model_type_public` | string |
| `is_genai_request` | bool |
| `gpu_request` | double |
| `duration_hours` | double |
| `schedule_delay_sec` | int64 |
| `ready_delay_sec` | int64 |
| `ready_status` | bool |
| `schedule_status` | bool |

Independently reproduced lifecycle values/counts:

| Physical lifecycle value | Source rows |
|---|---:|
| `online_inference` | 5,054,990 |
| `training` | 2,999,580 |
| `other` | 70,130 |
| `offline_inference` | 32,194,936 |
| `unknown` | 170,977 |
| `dev` | 31,708 |

Blacklisted prospective predictors: `duration_hours` (target only), `schedule_delay_sec`, `ready_delay_sec`, `ready_status`, `schedule_status`, `server_id`, `pod_id`. No utilization telemetry, outcome-derived lifecycle, target encoding or frequency encoding. `workload_id` and physical `row_ordinal` never enter primary predictors.

## Frozen scientific protocol

Primary population: `workload_id IS NOT NULL` AND `job_type_public` in `training`, `offline_inference`, `online_inference`, `dev`. Preserve all qualifying rows, heavy tails, rare categories and repeated-pod rows. No sampling, aggregation, deduplication or manufactured workload IDs.

- Principal M0 = R+P+A: exactly `gpu_request`, `gpu_spec_public`, `priority_class`, `model_type_public`, `is_genai_request`.
- Principal M1 = those same five predictors plus `job_type_public`, and nothing else.
- Target `duration_hours`; fit `y = log1p(duration_hours)`.
- Primary split is workload-disjoint, fixed seed **20260927**, 70/15/15 thresholds on the first 64 bits of SHA-256 of compact UTF-8 JSON `[seed, workload_id]`; `ensure_ascii=False`. Reuse `asi_pipeline.safety.assign_workload`, not an approximate reimplementation.
- Model seeds: **20260927, 20260928, 20260929**; they never change split membership.
- **CPU LightGBM 4.7.0**, two threads. Do not substitute GPU training.
- Native categoricals: `gpu_spec_public`, `priority_class`, `model_type_public`, `is_genai_request`, plus M1's `job_type_public`. Dictionaries fit on train only; missing/unseen categories use -1; numeric missing uses NaN. Preserve the existing string conversion and integer coding.
- Objective `regression_l1`; metric `l1`; learning rate 0.05; bagging fraction 0.8/frequency 1; deterministic true; force-column-wise true; feature-pre-filter false; verbosity -1. Maximum 200 rounds, validation early-stopping patience 30.
- The exact 12 candidates are read from config, not reconstructed from this summary:

| Candidate ID | num_leaves | min_data_in_leaf | feature_fraction |
|---:|---:|---:|---:|
| 1 | 15 | 20 | 0.8 |
| 2 | 15 | 20 | 1.0 |
| 3 | 15 | 100 | 0.8 |
| 4 | 15 | 100 | 1.0 |
| 5 | 31 | 20 | 0.8 |
| 6 | 31 | 20 | 1.0 |
| 7 | 31 | 100 | 0.8 |
| 8 | 31 | 100 | 1.0 |
| 9 | 63 | 20 | 0.8 |
| 10 | 63 | 20 | 1.0 |
| 11 | 63 | 100 | 0.8 |
| 12 | 63 | 100 | 1.0 |

Selection is separate for each model side, population/comparison and model seed; same 12-candidate budget. Minimize validation LogMAE only; ties use lowest candidate index. No test-driven selection. Candidate checkpoints and frozen individual selections must validate, and **all experiment selections must be frozen before any scientific test prediction/evaluation**.

Required subsidiary control ablations remain R vs R+O and R+P vs R+P+O; they do not replace the principal five/six-feature pair. The driver includes these and the principal pair for four-lifecycle and finite-execution populations: 36 selected model units, 432 candidate fits if no completed work is reused, 18 paired evaluations across the three seeds. Its `broad` label means the four-lifecycle population within this primary-only canonical file, **not the 40M/null-workload broad experiment**. Optional seen-workload W predictors/random/temporal analyses remain outside this resumed execution scope.

Primary metric: MAE on raw predicted log1p runtime. Absolute improvement = MAE(M0) - MAE(M1); relative improvement percent = 100 × that difference / MAE(M0). Report Spearman and original-runtime MAE/median absolute error using `expm1(max(predicted_log1p, 0))`, with overflow handling as implemented.

Bootstrap: **1,000 replicates**, seed **20260927**, sampling TEST workload IDs with replacement; include all executions for each occurrence; pair M0/M1 using identical sampled IDs/multiplicities. Existing aggregate error sums/counts implement execution-row weighting exactly. Do not retrain. Percentile 95% intervals [2.5,97.5] for absolute/relative LogMAE improvement; zero M0 error yields null relative improvement with valid counts reported. This means 1,000 resamples, not a sample restricted to 1,000 workloads.

Secondary finite-execution analysis: training versus offline inference, retaining the frozen split. Preserve both the finite-only training analysis and finite error summaries supplied by the implementation. It is not a replacement primary analysis. Tail bins are left-closed/right-open: `<1h`, `1–6h`, `6–24h`, `1–3d`, `3–7d`, `7–14d`, `14–28d`, `>=28d`. Lifecycle/tail analyses are descriptive strata, not separate tail models. The current code bootstraps overall paired results per population/comparison; do not invent separate per-tail bootstrap evidence.

Pre-frozen triage: approximately >=3% primary unseen-workload improvement, OR clearly >=5% important finite/tail improvement with stable seed/bootstrap evidence, supports STRONG; approximately 1–3% supports WEAK/needs mechanism; <=1% (including 1% boundary), disappearance under unseen workloads, or predominantly trivial Dev/Online separation without meaningful finite evidence kills the standalone contribution. Statistical significance alone is insufficient. Apply the original criteria after all frozen analyses; never move thresholds after seeing results.

## Exact Windows reproduction results

Source rows **40,522,321**; unique pods **36,685,018**; unique workloads **501,183**; non-null-workload rows **4,792,402**. No missing/nonfinite/nonpositive durations; median 0.4222222222222222 h, p95 9.688888888888888 h, p99 59.62222222222222 h, maximum 1824 h. These are independently reproduced Windows values in `windows_run/audit/source-audit.json`.

Primary rows **4,709,624**; workloads **473,265**; null workloads **0**; overlapping workloads **0**.

| Split | Rows | Workloads | Training | Offline inference | Online inference | Dev |
|---|---:|---:|---:|---:|---:|---:|
| train | 3,339,542 | 331,486 | 2,091,126 | 764,755 | 465,571 | 18,090 |
| validation | 658,761 | 71,074 | 426,146 | 131,683 | 95,598 | 5,334 |
| test | 711,321 | 70,705 | 442,275 | 134,873 | 128,791 | 5,382 |

All counts match exactly. The canonical validation also compared every workload assignment to the frozen function and independent source split map, and streamed every retained source value and physical row ordinal against the canonical file. Descriptive/data-integrity inspection of the future test rows is not predictive evaluation; no research test predictions or metrics exist.

## Implementation history and validation

1. Original Mac work materialized the pretraining protocol, safety helpers, streamed dataset builder, LightGBM selection/evaluation and temporal fixture machinery. Historical Mac test state was 35 passed, per the takeover request; the raw Mac test log was not supplied.
2. **Mac full-population feasibility failure is user-reported history** in the archival request. No corresponding Mac feasibility execution report or measured resource log was found in the transferred files. Its exact failure mode, candidate, timing and resource figures must not be invented. This is not a scientific result.
3. Transfer to Windows initially lacked `asi_pipeline` and had nested script/test folders; the user supplied/corrected them. Earlier audit reports retain this history.
4. A fresh Windows environment was created; no Mac virtual environment was reused. Machine: Windows 11 build 26200, AMD Ryzen 9 8945HS, 16 logical CPUs, measured visible RAM 16,413,143,040 bytes. The pre-run environment snapshot differs in time from the definitive feasibility trace.
5. A minimal portability change in `safety.publish_new` uses a writable staged-file handle for Windows flush, preserves atomic no-overwrite publication, and skips unsupported directory fsync on Windows. Do not claim POSIX-equivalent directory-metadata power-loss durability.
6. **35/35 original tests passed before safeguard work**, recorded in `reports/windows-tests.txt`.
7. Engineering-only safeguards added: atomic candidate/model units; input/source/canonical/split/protocol/code/version/seed/candidate/features binding; compatible-only resume; partial/stale/tampered rejection; validation-selection freeze; experiment-wide gate before test access; atomic evaluation/bootstraps; Windows RSS/commit/paging monitoring, stop markers and job-object cleanup. `reports/engineering-change-report.md` gives the file-level changes.
8. **Final total = 54 tests passed, 0 failed**, recorded in `reports/engineering-tests.txt`. All original test names and assertions remain. Added tests cover checkpoint compatibility, partial/tampered units, interrupted resume, selection creation, denied/permitted test access, mismatches, monitoring, exact data and lossless/split checks. An original metric-test fixture acquired mandatory selection metadata and extra assertions; no old assertions were removed.
9. A separate synthetic original-versus-updated comparison produced identical records for all 12 candidates, selected candidates and predictions for M0/M1 at seed 20260927. This supports implementation invariance; it is not empirical lifecycle evidence. Independent code review findings were addressed before data acquisition.
10. **config/protocol.yaml was not scientifically modified; its bytes are unchanged.** `docs/protocol.md`, `docs/DATASET_AUDIT.md`, metrics and original dataset builder bytes also remain unchanged. Scientific feature/encoding/split helper ASTs were compared. `reports/engineering-change-manifest.json` records hashes.

Exact recorded environment:

| Package/runtime entry | Version |
|---|---|
| Python | 3.12.14 |
| duckdb | 1.5.5 |
| lightgbm | 4.7.0 |
| narwhals | 2.26.0 |
| numpy | 2.5.3 |
| pandas | 3.0.6 |
| pip | 25.0.1 |
| pyarrow | 25.0.1 |
| python-dateutil | 2.9.0.post0 |
| PyYAML | 6.0.3 |
| scipy | 1.18.1 |
| six | 1.17.0 |
| tzdata | 2026.5 |

`environment/requirements-windows.txt` pins installed runtime dependencies, including transitives. Pip 25.0.1 is recorded in the environment snapshot; no virtual environment is archived. UTF-8 mode (`PYTHONUTF8=1`) is required for the documented Windows commands. Do not silently change unavailable versions.

## Preserved Windows feasibility result

**WINDOWS FULL WORKLOAD-DISJOINT NOT FEASIBLE**

The feasibility preflight observed **2.26 GiB commit headroom** (exactly 2,424,729,600 bytes; approximately 2.258 GiB), below the **predeclared 3 GiB minimum**. Available physical RAM was 4,165,435,392 bytes (3.879 GiB); commit limit 22,855,593,984 bytes; committed memory 20,430,864,384 bytes. Evidence: `windows_run/feasibility/manifest.json` and `m0-monitor/resources.jsonl`.

Therefore **neither M0 nor M1 started**, and scientific execution stopped as required. The M0 monitor's exit code is null because no worker launched; M1 was not attempted. No full-population preparation/training/prediction timing, worker peak RSS, models or M0–M1 metric comparison exists. No intentional OOM, worker kill or pagefile modification occurred. Preflight ended before a second PDH sample; sustained paging was not measured for this run. Do not infer direct pagefile-use bytes from commit.

Feasibility design remains exact full primary data, candidate 6 (31 leaves, min leaf 20, feature fraction 1.0), seed 20260927, CPU/two threads, M0 once then M1 once in fresh workers. Validation-only prediction is timed; test data remains untouched. Fixed monitor policy is documented in the engineering report (3 GiB preflight headroom; 1 GiB hard and 2 GiB sustained-pressure thresholds, plus hard-paging limits). A resource failure is not permission to sample, drop features/rows or alter candidates.

This is a resource-safety refusal under that machine state, not evidence against the hypothesis and not proof that every possible configuration of a 16 GiB machine is impossible. **Preserve the failed report.**

## Validated canonical artifact

- Archive/project-relative path: `windows_run/canonical/data/primary.parquet`.
- Original absolute path: `C:UsersagrajDesktopasi_datasetwindows_runcanonicaldataprimary.parquet`.
- Exactly **4,709,624 rows**, **473,265 workloads**; all exact split/lifecycle counts above.
- Size: **85,907,015 bytes**.
- SHA-256: `10a3a86c977701c3c26f0bdce231aeb294676d71fef772b96309ceab3d21b0a0`.
- Compression: ZSTD with dictionary encoding; **406 row groups**. Exact group sizes are in `windows_run/canonical/manifest.json`; the writer's upper bound is 100,000 rows/group.
- Columns/types: `workload_id` string; `duration_hours` double; `gpu_request` double; `gpu_spec_public` string; `priority_class` string; `model_type_public` string; `is_genai_request` bool; `job_type_public` string; `row_ordinal` int64; `split` string; `grouped_split` string. Pandas schema metadata is preserved. `split` and `grouped_split` agree; `row_ordinal` is a raw-file physical locator, never a feature or manufactured execution identity.
- Canonical manifest SHA-256: `57a2fb4187084d8121f77532d7cfbb1519c757106780901072334021ccc8bced`.
- Split manifest SHA-256: `9552fafdd83a38aa5996b311a3b68cbb1b78d2f7b804cd4dc81a506a0b4ecde6`.
- Raw source relationship: `acd868090a64c8852ee2586510a0384111aed0378905f5405d2be6779062e963`; frozen config/document hashes above.
- Preparation-script SHA-256: `576b97ccc56986caba479eea7fac26b871d715f673a35398f054f6eea7b6c9ec`; execution code-state SHA-256: `4c63406472c5e70349715feccf51ebc99773aa176e5df19e85ee860038e7d739`.
- Construction was closed before a new process reopened/validated the artifact. `construction.json` and the canonical manifest retain that provenance.

Canonical data is included in this archive. The 1.19 GB raw Parquet and archive remain on the current laptop but are deliberately omitted from the portable archive: the canonical data, official URL, exact raw hashes and reproducible preparation code suffice to transfer this checkpoint. Fetch the raw file only if needed for a new independent source/lossless audit. Do not regenerate/overwrite the validated canonical bytes merely because a path changed.

## Next execution machine

The user's planned next environment is **>=32 GiB RAM**, with **64 GiB preferable if conveniently available**, and CPU LightGBM. GPU acceleration is not required and must not replace the frozen CPU protocol. RAM capacity alone is not a feasibility pass: actual free memory, commit, paging and safety behavior still matter.

The included native resource monitor and supervised driver currently target **Windows**. A sufficiently provisioned Windows machine is the direct command-compatible path. A Mac/Linux machine requires a separately documented engineering-only monitor/supervision port and complete validation before feasibility; do not disable safeguards or claim these Windows commands already work there. The historical Unix `scripts/run_dry_run.py` is not a substitute for the full-population gate.

## Exact resume procedure — future machine only

These instructions are documentation, not authorization to restart work on this borrowed laptop. Preserve the archived failure and use a **new run directory** on the next machine. No scientific candidates, selections, predictions or bootstrap outputs currently exist to resume; only validated data and engineering state are available.

1. **Copy/extract** `asi_checkpoint_2026-10-06.zip`. Enter its `asi_checkpoint_2026-10-06` directory. Keep the uploaded ZIP/checksums and an unchanged archive copy.
2. **Verify SHA-256.** Before extraction compare the ZIP to the adjacent upload `SHA256SUMS.txt`. After extraction, use a trusted Python 3 interpreter: `python archive_tools/verify_checkpoint.py .`. It checks every payload file against internal `SHA256SUMS.txt` and returns nonzero on mismatch. Internal sums exclude themselves; external sums cover the finished ZIP. Do not continue after a mismatch.
3. **Create a fresh environment** with Python 3.12.14; do not copy either old virtual environment. On Windows: `py -3.12 -m venv .venv-resume` (first verify that the selected interpreter really is 3.12.14), then `$py = ".\.venv-resume\Scripts\python.exe"` and `$env:PYTHONUTF8 = "1"`. On a different OS complete the engineering compatibility work first.
4. **Install the exact dependencies:** `& $py -m pip install -r environment/requirements-windows.txt`; then `& $py -m pip check`. Record OS/CPU/RAM/free disk/commit/pagefile observations, Python and all installed versions in a new environment report. Stop rather than silently substitute a different LightGBM or unavailable pinned version.
5. **Run the complete suite:** `& $py -B -m unittest discover -s tests -v`. Expect **54 passing tests**, including synthetic model-fit tests; no scientific training is involved. Document legitimate platform-specific differences; never weaken invariants. Any new engineering port needs its own added tests and refreshed code provenance.
6. **Verify frozen config/protocol hashes** against this checkpoint and internal sums. Verify current scientific files still match `reports/engineering-change-manifest.json`. Historical `execution_permissions.full_model_training=false` and `remote_transfer=false` remain in config; **do not edit them**. The current engineering execution layer uses a separate authorization manifest.
7. **Locate canonical/source data.** Use `windows_run/canonical/` as delivered. Its `manifest.json` and `split-manifest.json` are immutable. Historical absolute raw paths in `construction.json` are provenance only. If raw data is needed, download the one official execution-summary archive into a fresh directory and require the archive/source hashes above; never download `pod_hourly`. `prepare_windows.py acquire --output NEW_RAW_DIRECTORY` is the provided downloader.
8. **Verify data hashes/counts/splits.** Confirm canonical and split-manifest SHA-256 values, then run the following read-only data checks (temporary DuckDB spill directory creation is expected). If raw is available at a new path, additionally call `verify_lossless(raw_path, canonical_path, p)` after checking the raw hash. Do not call the write/finalize commands against completed artifact directories.

   ```powershell
   @'
   import json
   from pathlib import Path
   from asi_pipeline.dataset import sha256
   from asi_pipeline.primary_data import inspect_primary, verify_assignments, EXPECTED
   root=Path.cwd(); data=root/'windows_run/canonical'
   p=json.loads((root/'config/protocol.yaml').read_bytes())
   m=json.loads((data/'manifest.json').read_bytes())
   for item in m['files']:
       assert sha256(data/item['path'])==item['sha256']
   assert sha256(data/'split-manifest.json')==m['split_manifest_sha256']
   audit=json.loads((root/'windows_run/audit/population-split-audit.json').read_bytes())
   splitmap=root/'windows_run/audit/split-map.parquet'
   assert sha256(splitmap)==audit['split_map_sha256']
   assert inspect_primary(data/'data/primary.parquet', EXPECTED)==EXPECTED
   verify_assignments(data/'data/primary.parquet',p,splitmap)
   print('Exact canonical and split checks passed')
   '@ | & $py -B -
   ```

9. **Create a new machine/run authorization and run full-population feasibility.** Keep `windows_run/authorization.json` and `windows_run/feasibility/` unchanged. The old authorization contains old absolute paths. Write a new manifest pointing to new absolute feasibility and global-freeze destinations, bound to the unchanged protocol. Do this before any workers; once units exist its hash is part of their identity. A fresh `next_run` must not already exist:

   ```powershell
   @'
   import json,platform
   from pathlib import Path
   from asi_pipeline.dataset import sha256
   root=Path.cwd().resolve(); dest=root/'next_run'; dest.mkdir(exist_ok=False)
   auth=json.loads((root/'windows_run/authorization.json').read_bytes())
   assert auth['protocol_sha256']==sha256(root/'config/protocol.yaml')
   auth.update(feasibility_manifest=str(dest/'feasibility/manifest.json'),
               experiment_freeze=str(dest/'science/selection-freeze'),
               resume_machine=platform.platform(),
               historical_windows_outcome='FAILED preflight; neither worker started')
   with (dest/'authorization.json').open('x',encoding='utf-8') as out:
       json.dump(auth,out,indent=2)
   '@ | & $py -B -
   & $py -B scripts/windows_feasibility.py run --dataset windows_run/canonical --output next_run/feasibility --config config/protocol.yaml --authorization next_run/authorization.json
   ```

   This calls candidate 6, seed 20260927, two CPU threads, M0 once then M1 once, with the exact full primary artifact. Do not invoke unmonitored worker mode directly. On a non-Windows port use its reviewed equivalent and record the engineering changes; do not spoof a passing Windows report.
10. **If feasibility fails, stop.** Preserve its new report and logs; do not change the old Windows result, lower thresholds, sample, change features/splits/candidates, or continue to science. A process exiting zero is insufficient without a valid matching report whose `status` is `PASSED` and both workers completed safely.
11. **Only if feasibility passes**, run the frozen experiment on the new machine:

   ```powershell
   & $py -B scripts/run_windows_science.py run --dataset windows_run/canonical --output next_run/science --config config/protocol.yaml --authorization next_run/authorization.json
   ```

   The driver performs steps 12–17 automatically in the order below. Do not separately call test phases out of order. Reusing this same driver/run root after interruption reuses only compatible completed units; changed config/data/code/version/authorization is rejected. Partial units are not complete; preserve them for diagnosis. Never overwrite incompatible units—stop and resolve their provenance.
12. **Validation-only selection:** train all frozen candidates for each required population/pair/seed/side, with identical budgets. No test-performance inspection.
13. **Persist/freeze selections:** each model's `selection/manifest.json` records candidates and choice; `next_run/science/selection-freeze/manifest.json` seals all 36 model selections before any test worker. The lower-level prediction and full-data evaluation paths also require this global freeze.
14. **Evaluate untouched test:** produce paired predictions with workload IDs and physical row locators. Verify compatible metadata/order, features and manifests. Test results cannot alter remaining execution choices.
15. **Paired 1,000-replicate workload bootstrap:** apply the frozen aggregate loss-sum/count resampling to completed predictions; no retraining. Retain predictions sufficient to reconstruct paired losses and all bootstrap outputs.
16. **Training-vs-Offline secondary analysis:** retain its separate finite-only population results and principal-population finite error summaries, across the three seeds; never replace the primary result.
17. **Frozen lifecycle/tail analyses:** retain Spearman, original-duration errors, lifecycle errors and all eight tail bins. Driver outputs live under `next_run/science/models/` and `next_run/science/evaluations/`; its `complete/` marker is published after the required paired evaluations. Do not claim an analysis/CI that the frozen implementation has not produced.
18. **Apply the PRE-FROZEN triage thresholds** only after the entire frozen experiment completes. Report magnitude, per-seed stability, paired workload CIs, finite-execution evidence and whether Dev/Online separation dominates. Preserve all failures/limitations. Package actual models, candidate records, selections, predictions, bootstrap/strata and final interpretation with new checksums; never backfill fabricated outputs into this pretraining archive.
19. **Return exactly one high-level research classification**, supported by those complete results: `CONTINUE — STRONG`, `CONTINUE — WEAK / NEEDS MECHANISM`, or `KILL AS STANDALONE CONTRIBUTION`. None is justified at this checkpoint.

## Do not change to obtain a result

Do not change the research question/L1 terminology; population, missing-workload exclusion, full row counts or duplicate/tail policy; grouped split/function/seed; M0/M1 features or blacklist; target/log transform; native categories/train-only dictionaries/missing handling; CPU LightGBM 4.7.0 or frozen fit parameters; the exact 12 candidates or model seeds; validation-only selection/tie break and test isolation; metrics, workload-bootstrap unit/weighting/replicates/seed/CI; finite analysis or strata; or triage thresholds. Do not add invented L2/user/history controls, telemetry, outcome-derived lifecycle, a model zoo, target/frequency encoding, GPU replacement, samples, the broad 40M scientific run, or D108–D110/pod_hourly execution. Do not rewrite failed feasibility as passed. Engineering compatibility fixes require documentation, invariant tests and fresh provenance, never silent scientific amendments.

## Important file map and portability limits

| Path | Role |
|---|---|
| `CHECKPOINT.md` | Current archival handoff; read first; does not replace frozen config |
| `config/protocol.yaml`, `docs/protocol.md` | Authoritative frozen design and exact candidates/semantics |
| `docs/DATASET_AUDIT.md`, `docs/HANDOFF_ORIGINAL.txt` | Historical dataset/prior-art context; distinguish inherited and independently verified claims |
| `asi_pipeline/` | Frozen scientific helpers plus documented engineering checkpoint/selection/supervision/data layers |
| `scripts/prepare_windows.py` | Acquisition/audit/build/fresh-reopen stages; do not overwrite completed outputs |
| `scripts/windows_feasibility.py`, `scripts/run_windows_science.py` | Current supervised Windows gates/driver |
| `scripts/06_generalization.py` | Guarded paired metrics/bootstrap, atomically published |
| `tests/` | Current 54-test suite; includes synthetic training fixtures |
| `windows_run/canonical/` | Validated modeling Parquet, canonical/split/construction manifests |
| `windows_run/audit/` | Fresh source/count/split audit and exact workload split map |
| `windows_run/raw/source-manifest.json` | Official URL and raw cryptographic identity; large raw files omitted |
| `windows_run/feasibility/` | Immutable failed preflight report and monitor logs; preserve null/not-run fields |
| `windows_run/authorization.json` | Historical authorization with old absolute paths; create new run-specific copy, never edit this one |
| `environment/` | Exact dependency specification and measured Windows environment |
| `reports/` | Final takeover/feasibility, implementation, tests and invariance evidence |
| `reports/history/` | Superseded takeover reports and prior package metadata, retained for provenance |
| `provenance/requests/` | Original user request/authorization/archive instructions; also evidence for user-reported Mac failure |
| `provenance/pre-engineering/` | Preserved Windows pre-engineering source/tests/docs snapshot; already includes the initial Windows flush portability fix, so not a pristine Mac checkout |
| `provenance/scientific-invariance-probe.py` | Historical synthetic-comparison probe; contains original absolute paths, not a portable resume entry point |
| `archive_tools/verify_checkpoint.py` | Standard-library checksum verifier; does not run training or modify artifacts |
| `SHA256SUMS.txt` | All archived payload-file checksums except the checksum file itself |

The old READMEs and `docs/protocol.md` historical approval/pending paragraphs describe earlier stages; the protocol's pre-training completion section and exact config govern science. Current engineering authorization and implementation report explain the separate execution layer. Preserve their bytes rather than “updating” frozen history.

Referenced but not supplied: `docs/protocol_versions/checkpoint1/`, original Mac feasibility/test logs, old `results/audits/local_validation.json`/`delivery.json`, temporal maps, duplicate-pod DB/artifacts and matched-cohort source artifacts. Their absence does not invalidate the independently reproduced primary data, but prevents claiming those historical checks were newly rerun. No Git repository/history was supplied; source snapshots and cryptographic manifests provide the preserved code state.

No scientific model/candidate-selection/test/bootstrap result files are missing from this archive: **they have not been generated on research data**. The archive includes all existing validated primary data, current code/tests, provenance and failure evidence needed for an honest next-machine handoff, with the Windows portability limitation explicitly recorded.

## Archive/upload status

The upload-ready directory contains the final ZIP, a standalone copy of this file, external `SHA256SUMS.txt`, `WINDOWS_TAKEOVER_FEASIBILITY_REPORT.md`, and `ARCHIVE_VERIFICATION.json`. The expanded archival directory is separate to avoid uploading the canonical data twice accidentally. The archive verifier reopens the ZIP and checks every stored payload hash and required entry. The adjacent external checksums cover the finished ZIP and standalone handoff/report/verification files; the ZIP cannot contain its own final hash.

No authenticated Google Drive upload tool was exposed in this session. **No upload is claimed.** Manually upload those files into a new Drive folder such as `ASI Research Checkpoint 2026-10-06`; preserve older checkpoints. Exact local output paths and final ZIP size/hash are reported in `ARCHIVE_VERIFICATION.json` and the final chat response.
