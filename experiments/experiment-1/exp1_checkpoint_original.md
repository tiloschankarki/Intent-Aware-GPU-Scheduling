# Completed ASI scientific checkpoint — 2026-10-13

**Decision: KILL AS STANDALONE CONTRIBUTION. Execution PASS is not hypothesis PASS.**

This is a completed predictive/information-contribution experiment, not a causal study. The decision is the user’s explicit research judgment: the frozen triage protocol did not specify how to resolve mixed per-seed outcomes near the 1% boundary. The primary gains straddle that boundary, every principal four-lifecycle confidence interval includes zero, and separately trained finite gains are below 1%. No cross-seed aggregation, new threshold, or causal-independence claim has been introduced. The result does not establish that lifecycle metadata has universally zero predictive value.

This document supersedes the *execution status and undecided triage* of the preserved October 6 handoff and earlier completed resume report. Those historical documents are retained unchanged. No fitting, retuning, data download, or modification of scientific outputs was performed while creating this archive. Verification recomputes metrics and bootstrap samples from already frozen test predictions without retraining.

## Research question and constructs

Exact frozen question in docs/protocol.md: “Does prospective execution/lifecycle type add predictive information for individual GPU/ML execution duration beyond available prospective controls, including on unseen workloads?”

Original handoff question: “Does prospective execution/lifecycle type provide incremental predictive value for individual GPU/ML job runtime beyond other prospective information?” The ASI question is whether job_type_public improves individual execution-duration prediction beyond ASI’s available prospective controls, and whether that improvement persists for unseen workloads.

| Construct | Meaning | ASI role |
|---|---|---|
| L1 | Prospective execution/lifecycle type: training, development/debugging, evaluation, online/offline inference | job_type_public, variable of interest |
| L2 | Planned computational scope: epochs, steps, iterations, trials, token budgets | Desired controls inadequately exposed publicly; not invented or implied controlled |
| L3 | Application/model semantics | model_type_public, prospective control |
| L4 | Workload/configuration identity | workload_id, configuration proxy and split group; not a user ID |

ASI also lacks the desired user/tenant/history controls. Do not infer lifecycle from runtime/outcomes, treat L3/L4 labels as L1, or describe this as generic “experimental objective.”

## Documented prior-art audit and rejected directions

The following are inherited findings in docs/HANDOFF_ORIGINAL.txt and the October 6 checkpoint, not new literature searches. The broad experimental-objective direction was narrowed because public traces lacked a clean prospective label. AcmeTrace was rejected because the handoff reports author correspondence that its labels used post-execution job-name/duration information; the underlying correspondence was not supplied. PAI semantics were primarily L3/L4/task-role information, not a clean prospective job-level L1 label. Completion-aware/scheduler-feedback work was dropped after prior-art auditing found substantial precedent. Generic semantics-improves-runtime-prediction is too broad; the surviving study is incremental lifecycle information under prospective controls and strong generalization.

The bounded prior-art search is not proof of absence of related work; lifecycle metadata itself is not claimed novel. Historical 46-configuration/784-row matched-cohort data were not transferred and cannot replace the primary population. D109H00 linkage and D108–D110 temporal/pod_hourly work are historical, separate directions and were not executed in this experiment.

## Dataset provenance, identity and limitations

Attribution: Alibaba ASI / GPU Cluster Trace v2026, execution summary. Official recorded source URL: https://tre-clusterdata.oss-cn-hangzhou.aliyuncs.com/cluster-trace-gpu-v2026/data/asi_opensource_job_execution_summary.zip

The October 6 run freshly downloaded 1188295031 bytes, SHA-256 `2dd48db5c5a532d0b1504c67522ed7f6929df6efd5c22abc4a921349aa37ff4f`. Member `asi_opensource_job_execution_summary/part-000.parquet` was 1188294827 bytes, SHA-256 `acd868090a64c8852ee2586510a0384111aed0378905f5405d2be6779062e963`. Recorded download start 2026-10-06T19:11:37.745010+00:00; completion 2026-10-06T19:12:25.585636+00:00.

No independent publisher-signed checksum/release identifier was supplied, and source Arrow metadata had no independent release identifier. Hashes establish the bytes used, not independently authenticated release attribution. The source has 40,522,321 rows, 36,685,018 unique pods and 501,183 unique workloads; 4,792,402 rows have non-null workloads. These are recorded October 6 source-audit results, not a fresh raw-source reread during this archive task.

The canonical file is 85907015 bytes with SHA-256 `10a3a86c977701c3c26f0bdce231aeb294676d71fef772b96309ceab3d21b0a0`. Canonical manifest SHA-256 `57a2fb4187084d8121f77532d7cfbb1519c757106780901072334021ccc8bced`; split manifest SHA-256 `9552fafdd83a38aa5996b311a3b68cbb1b78d2f7b804cd4dc81a506a0b4ecde6`. Canonical data, independent split map, source provenance, schema, construction record and original audits are included. Raw ZIP/Parquet were intentionally omitted from the transfer and remain omitted; no raw data was downloaded. Historical streaming source-to-canonical lossless validation is preserved; it cannot be newly repeated without raw bytes.

## Authoritative frozen protocol

Protocol ID `asi-lifecycle-frozen-v2-pretraining`. Config byte SHA-256 `4908e86e7526c8ecc298facd46089ac94fd4dec5094eee47af24987237653e61`. Protocol document SHA-256 `7c58289899902417fe9cdba0bac93309d231eb7248b1b077414e1efd02b3d71c`. Semantic config-content SHA-256 `a8d8a96556b2868067db7af63e04201c7da0c509afc4c101fdc5638d09b6d2ea`. config/protocol.yaml and docs/protocol.md remain authoritative; this completed status document does not amend them.

Primary population: non-null workload_id and job_type_public in training, offline_inference, online_inference, dev. Retain every qualifying execution, heavy tails, rare categories and repeated-pod rows. No sampling, aggregation, deduplication, trimming or manufactured workload IDs. Unknown/other and null workloads are excluded from this primary population.

Principal M0 = R+P+A: gpu_request, gpu_spec_public, priority_class, model_type_public, is_genai_request. Principal M1 adds only job_type_public. Required control ablations are R vs R+O and R+P vs R+P+O. R = GPU resource controls, P = priority, A = application/model controls, O = lifecycle. workload_id and row_ordinal never enter primary predictors.

Target duration_hours; fit log1p(duration_hours). Blacklisted predictors: duration_hours (target only), schedule_delay_sec, ready_delay_sec, ready_status, schedule_status, server_id, pod_id. No utilization telemetry, outcome-derived lifecycle, target/frequency encoding or invented L2/user/history controls.

Primary split: workload-disjoint, seed 20260927, 70/15/15 thresholds on the first 64 bits of SHA-256 of compact UTF-8 JSON [seed, workload_id], ensure_ascii=False. Use asi_pipeline.safety.assign_workload exactly. Model seeds 20260927, 20260928, 20260929 never alter split membership. No random/temporal scientific experiment was added. Driver label broad means only this four-lifecycle canonical population, not the full 40-million-row experiment.

CPU LightGBM 4.7.0, two threads. Native categorical GPU specification, priority, model type, is_genai_request, and M1 lifecycle; dictionaries fit on training only. Preserve original string conversion and integer coding. Missing/unseen categories use -1; numeric missing values use NaN. Objective regression_l1, metric l1, learning rate 0.05, bagging_fraction 0.8, bagging_freq 1, deterministic true, force_col_wise true, feature_pre_filter false, verbosity -1. Maximum 200 boosting rounds and validation early stopping patience 30. The candidate grid is frozen:

| Candidate | num_leaves | min_data_in_leaf | feature_fraction |
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

Selection is separate for each population/comparison/seed/model side, with equal 12-candidate budgets. Minimize validation LogMAE; ties choose lowest candidate index. All 36 individual selections were frozen into the global selection manifest before any scientific test prediction. No test-driven selection or subsequent tuning occurred. The design entails 432 candidate fits, 36 selected model units and 18 paired evaluations.

Primary metric: MAE on raw predicted log1p duration. Absolute gain = MAE(M0) − MAE(M1); relative gain percent = 100 × absolute gain / MAE(M0). Spearman and original-runtime MAE/median absolute error use expm1(max(predicted_log1p,0)) with implemented overflow handling. Prediction pairs preserve ordered physical row locators and metadata.

Bootstrap: 1,000 paired test-workload-ID resamples with replacement, seed 20260927. Include every execution for each occurrence, preserving workload multiplicity and execution-row weighting through aggregate loss sums/counts. No retraining. Percentile 95% intervals at [2.5,97.5] for absolute/relative LogMAE gain; zero-M0 relative gain is null with counts reported. No separate per-tail bootstrap intervals were computed by the frozen implementation.

Required secondary finite-execution population: training versus offline inference with the same frozen split, both separately fitted finite-only models and finite subsets of four-lifecycle models. Eight left-closed/right-open descriptive duration bins: <1h, 1–6h, 6–24h, 1–3d, 3–7d, 7–14d, 14–28d, >=28d. No separate tail models.

Pre-frozen triage: approximately >=3% primary unseen-workload gain OR clearly >=5% important finite/tail gain with stable seed/bootstrap evidence supports STRONG; approximately 1–3% supports WEAK/needs mechanism; <=1% (including boundary), disappearance under unseen workloads, or predominantly trivial Dev/Online separation without meaningful finite evidence supports KILL AS STANDALONE CONTRIBUTION. Significance alone is insufficient. The protocol did not prescribe a seed aggregation or mixed-boundary resolution. The explicit final KILL judgment is conservative research interpretation of the completed marginal results, not an invented exact numerical decision rule.

## Exact primary validation and counts

| Split | Rows | Workloads | Training | Offline inference | Online inference | Dev |
|---|---:|---:|---:|---:|---:|---:|
| train | 3339542 | 331486 | 2091126 | 764755 | 465571 | 18090 |
| validation | 658761 | 71074 | 426146 | 131683 | 95598 | 5334 |
| test | 711321 | 70705 | 442275 | 134873 | 128791 | 5382 |

Total 4,709,624 rows, 473,265 workloads, zero null workloads and zero workload overlap. Fresh ADARSH validation reopened the canonical Parquet/split manifest; checked hashes, schema, target validity, split agreement, row-locator uniqueness/range/order, feature/population constraints and every frozen workload assignment against the independent source split map. It matched every split/lifecycle count. Every canonical row locator was streamed. Archival verification repeats read-only canonical/count/assignment checks on the independently extracted package; it never rebuilds canonical data or splits.

## October 6 history and stopped 16-GB feasibility

Original Mac work supplied the frozen scientific implementation; 35 historical Mac tests and the Mac feasibility failure are handoff/user-reported history, with original Mac logs absent. The Windows takeover initially lacked code and had nested folders, later corrected. The engineering update added atomic checkpoint binding, validation/global selection freezes and Windows memory/commit/paging supervision. The original and updated source snapshots, manifests and engineering test evidence are preserved; no Git repository/history was supplied.

The October 6 Windows machine was an AMD Ryzen 9 8945HS with measured visible RAM 16,413,143,040 bytes. Feasibility failed preflight: physical available 4,165,435,392 bytes; commit available 2,424,729,600 bytes, below the unchanged 3-GiB minimum. Neither M0 nor M1 started. This was a resource-safety refusal, not scientific evidence or a universal statement about all 16-GB configurations. The failed manifests/logs remain immutable.

## ADARSH resume and completed execution

ADARSH: Lenovo 82Y5, AMD Ryzen 7 7840HS, Windows 11 x64, physical RAM 33,492,422,656 bytes (about 31.2 GiB usable physical capacity, consistent with 32 GB installed). Native Microsoft-compiled AMD64 CPython 3.12.10 was explicitly authorized as a portability exception to historical 3.12.14, because Python 3.12.14 was source-only with no official Windows installer. Official Python 3.12.10 AMD64 installer Authenticode signature verified as Python Software Foundation; installer SHA-256 67b5635e80ea51072b87941312d00ec8927c4db9ba18938f7ad2d27b328b95fb. No MSYS2 interpreter was used for scientific execution. Frozen config and source bytes were not changed to encode the exception; versions/authorization/provenance retain it.

Completed runtime dependency pins: duckdb==1.5.5, lightgbm==4.7.0, narwhals==2.26.0, numpy==2.5.3, pandas==3.0.6, pyarrow==25.0.1, python-dateutil==2.9.0.post0, PyYAML==6.0.3, scipy==1.18.1, six==1.17.0, tzdata==2026.5. Python 3.12.10; bootstrap pip 25.0.1 is recorded in the installer/environment history. UTF-8 mode was enabled. Exact pins, pip download/install metadata, signature report, installer logs and interpreter report are included; virtual environments and installer binaries are omitted.

LightGBM 4.7.0 imported and passed a CPU synthetic check; pip check passed; 54 transferred tests passed with zero failures. Synthetic tests are not scientific effect evidence. Full-population candidate-6 feasibility passed M0 and M1 under unchanged thresholds. Preflight required >=3 GiB physical AND commit headroom; <1 GiB was a hard stop; sustained soft memory/commit/paging pressure for 15 seconds was a stop. No thresholds were weakened, pagefile changes made, or sampling/GPU substitutions used.

Execution started 2026-10-14T00:36:54.019244+00:00 and completed 2026-10-14T04:10:54.701970+00:00 (UTC; local session date October 13). It published 432 candidate units, 36 selections/global freeze, 36 test prediction units, 18 paired evaluations, all bootstrap and lifecycle/finite/tail reports, and the completion seal. Final audit verified 524 sealed units and 72 scientific supervised workers passed. Canonical data and all prediction/model/encoding bytes are included.

Minimum observed scientific available physical memory 7656431616 bytes; minimum observed commit headroom 7642333184 bytes. There were 2 monitoring sample gaps >5 seconds, maximum 2595.0150000000012 seconds. No continuous observation through those gaps is claimed and their cause is not inferred. Direct pagefile-use bytes were unavailable. Supervisor RSS can reflect the venv launcher rather than the full native process tree; preserve worker self-reported feasibility peaks and system-headroom logs. Windows directory fsync has documented portability/durability limits. These limitations remain attached to execution PASS.

## Exact principal results

Positive gain means M1 improves LogMAE. Values below use the stored float representations, not rounded aggregate summaries. Confidence intervals are separately computed paired workload-bootstrap intervals. Every four-lifecycle principal absolute and relative interval includes zero. Every separately trained finite-execution principal relative point gain is below 1%.

| Population | Seed | M0 LogMAE | M1 LogMAE | Absolute gain | Relative gain % | Absolute 95% CI | Relative 95% CI % |
|---|---:|---:|---:|---:|---:|---|---|
| broad | 20260927 | 0.7261954034509834 | 0.7193243747061635 | 0.006871028744819929 | 0.9461680302805315 | [-0.008309408919933162, 0.018835636174297007] | [-1.1556693288810944, 2.5580923336846935] |
| broad | 20260928 | 0.7247167338206858 | 0.7188126704978293 | 0.005904063322856534 | 0.8146718638233289 | [-0.009404987293254233, 0.01781361400982062] | [-1.3238907068013972, 2.402525207340963] |
| broad | 20260929 | 0.7275455167118866 | 0.7175150409233099 | 0.010030475788576743 | 1.3786733005941791 | [-0.005543398826097409, 0.022185252766721963] | [-0.7554450700737221, 3.014961178061143] |
| finite | 20260927 | 0.6267133119122376 | 0.6247405762283561 | 0.0019727356838814547 | 0.3147748175098136 | [0.0011230962651153059, 0.002798202902266236] | [0.1817765609117613, 0.4422583781727329] |
| finite | 20260928 | 0.6286086241778802 | 0.6246674417033529 | 0.003941182474527349 | 0.6269692019707472 | [0.0019938915919907596, 0.005998999031790583] | [0.32233177864478185, 0.9429028992743582] |
| finite | 20260929 | 0.6286813898540174 | 0.6267301939301874 | 0.0019511959238300847 | 0.31036323888689643 | [0.0011535462392951335, 0.0027341698399157037] | [0.18363740770744272, 0.43817310970430856] |

The finite subset of four-lifecycle-trained principal models has relative gains 1.039514538214001%, 1.074631715813759%, 1.1218493388042958%. This is distinct from separately fitted finite-only results; both are retained.

## Original-runtime and rank metrics

| Population | Seed | M0 runtime MAE h | M1 runtime MAE h | M0 median AE h | M1 median AE h | M0 Spearman | M1 Spearman |
|---|---:|---:|---:|---:|---:|---:|---:|
| broad | 20260927 | 15.483917926098439 | 15.667915373681765 | 0.8752040262790746 | 0.8777776242136794 | 0.5004211575470264 | 0.5155119417398165 |
| broad | 20260928 | 15.455450950470114 | 15.650745444950394 | 0.8760628676026736 | 0.8777776579048706 | 0.5011912642500564 | 0.515868158333762 |
| broad | 20260929 | 15.489592719281092 | 15.56878597876428 | 0.8720202827922074 | 0.8777781326257179 | 0.5015283645083675 | 0.5167911997585888 |
| finite | 20260927 | 3.431234481837399 | 3.427609073325842 | 0.8482706721053503 | 0.8555554754035803 | 0.3664146069791041 | 0.36983261027044056 |
| finite | 20260928 | 3.437395365169251 | 3.4274244332655055 | 0.8389041463669854 | 0.8517955289755916 | 0.36585621417940933 | 0.3692293449887338 |
| finite | 20260929 | 3.4376379326827284 | 3.4344866200069832 | 0.838894959318878 | 0.8444443756366272 | 0.3657367447243446 | 0.37140831707263694 |

Principal four-lifecycle original-runtime MAE worsens in every seed. Finite-only runtime MAE improves slightly, while median absolute error worsens in all three seeds. No runtime overflow rows were reported. LogMAE remains the frozen primary metric; the metric was not changed after seeing these differences.

## Duration-tail findings

These are descriptive principal-model relative LogMAE gains; the three seed values are listed separately, not a confidence interval. Tail counts are execution rows. No tail-specific bootstrap evidence or causal mechanism is claimed.

| Population | Tail | Test rows | Seed 20260927 gain % | Seed 20260928 gain % | Seed 20260929 gain % |
|---|---|---:|---:|---:|---:|
| broad | <1 hour | 354126 | -7.638271425294446 | -7.426899005383738 | -6.885124746699381 |
| broad | 1–6 hours | 217286 | -1.5773831868144674 | -0.6183208383769089 | -2.426605685752017 |
| broad | 6–24 hours | 91428 | 1.0264665092784646 | 0.9148725666002163 | 1.515482871884945 |
| broad | 1–3 days | 21380 | 7.802751491934356 | 7.585111722190685 | 8.416813560847945 |
| broad | 3–7 days | 12903 | 16.505334997627312 | 14.89780209974937 | 17.613740767282014 |
| broad | 7–14 days | 5040 | 10.621896594879654 | 8.709299576350087 | 11.790885278746808 |
| broad | 14–28 days | 5889 | 14.134128252035692 | 12.068662069834803 | 15.015410572230751 |
| broad | >=28 days | 3269 | 8.961310802247073 | 7.5383988926285275 | 9.929046104426702 |
| finite | <1 hour | 277739 | -0.14032381670952634 | -2.880364219674481 | 0.19594085041725984 |
| finite | 1–6 hours | 206203 | 0.1719156265850033 | 0.19089673553058908 | 0.4649854791122827 |
| finite | 6–24 hours | 77642 | 0.7351979000996949 | 3.311158577135007 | 0.29181836891210183 |
| finite | 1–3 days | 13063 | 0.5266225015853473 | 2.215115560202687 | 0.2797930239281498 |
| finite | 3–7 days | 2103 | 0.5666942047357282 | 1.371869081406361 | 0.3445772231063957 |
| finite | 7–14 days | 312 | 0.5347172583066804 | 0.7644857538152421 | 0.5446820621933168 |
| finite | 14–28 days | 72 | 0.6834134720141924 | 0.4220352434157621 | 0.3491014553881602 |
| finite | >=28 days | 14 | 0.42264917186263556 | 0.5034299458892256 | 0.5054321676121958 |

Four-lifecycle principal tail gains exceed 5% for several >=1-day bins, but <1h and 1–6h errors worsen. They do not establish the strong tail exception without the required stability/uncertainty evidence. Finite-only principal tail gains stay below 5%; longest bins contain only 312, 72 and 14 executions. Larger gains in weak-control ablations do not replace the principal strong-control result. All 18 full evaluation JSONs retain exact lifecycle, finite, tail, rank and original-runtime metrics; bootstrap samples retain paired sampled losses and execution counts.

## Final research judgment

**KILL AS STANDALONE CONTRIBUTION.** This is the final user-directed research judgment, not a new deterministic aggregation of seeds. Two primary seed gains are below 1%, the third is 1.379%, all principal intervals include zero, finite-only principal effects are below 1%, and original-runtime MAE worsens for the primary population. Descriptive tail gains and weak-control ablations are acknowledged but do not justify a strong independent lifecycle contribution. Execution PASS certifies completion/integrity under the recorded gates, not support for the hypothesis. No causal independence, universal null effect, or unseen result is inferred.

## Portable file map and reproducibility

The ZIP contains regular files only: a content-addressed objects/ store, FILE_INVENTORY.json mapping every logical path to SHA-256/size, complete package SHA256SUMS.txt, this document, ARCHIVE_README.md and portable_archive.py. No external blob store, hardlink, original machine path, virtual environment or network service is required. Materialization makes isolated byte-identical copies of every logical path. Historical absolute strings are preserved in immutable sealed manifests but are never used for artifact access by the portable verifier.

| Materialized logical path | Role |
|---|---|
| checkpoint/config, docs, asi_pipeline, scripts, tests | Unchanged authoritative design/current implementation and tests |
| checkpoint/provenance/pre-engineering | Preserved earlier implementation/tests/docs, including initial Windows flush portability change |
| checkpoint/windows_run/canonical, audit, raw/source-manifest.json | Exact canonical data, split map and source identity |
| checkpoint/windows_run/feasibility | Immutable October 6 failed run |
| october6/upload | Exact original ZIP and external checksum/verification/handoff files |
| october6/extracted | Losslessly preserved full original payload; identical contents share object bytes |
| completed_run/authorization.json, feasibility | ADARSH authorization and passed gate/logs/models |
| completed_run/science/models | Every candidate, individual selection, selected model/encoding, test predictions, legacy aliases/manifests |
| completed_run/science/selection-freeze, complete | Global freeze and completion seal |
| completed_run/science/evaluations | All 18 paired metric/strata reports and bootstrap Parquets |
| completed_run/science/monitor | All 72 worker supervisor manifests/resource traces/stdout/stderr |
| resume_reports | Environment/tests/validation/final audit/results/provisioning reports and resume orchestration history |

Verify hashes and reconstruct into a new directory: `python -B portable_archive.py verify --package . --workspace reconstructed --report ../portable-structure-verification.json`. Standard-library Python suffices for archive/seal checks. The package manifest excludes only itself, avoiding self-hash circularity. External SHA256SUMS.txt covers the finished ZIP and standalone reports. Reproduce every stored result and 1,000 bootstrap samples from the frozen predictions using the exact native Python 3.12.10/dependency environment: `python -B portable_archive.py reproduce --package . --workspace reconstructed --report ../metric-reproduction.json`. This reopens canonical data and verifies assignments/counts, but does not train or regenerate data/splits. Floating comparison tolerance is 1e-12 absolute and relative; timing, timestamp and provenance fields are preserved rather than numerically re-created.

If training reproduction is separately requested in the future: use an isolated materialized copy and a fresh native Windows CPython 3.12.10 environment under the recorded exception, install checkpoint/environment/requirements-windows.txt exactly, enable PYTHONUTF8=1, run all 54 tests, validate canonical bytes/counts/splits, and create a new authorization bound to the unchanged config with fresh absolute feasibility/science-freeze destinations. Run the existing supervised windows_feasibility.py gate first and only then run run_windows_science.py. Do not reuse historical absolute authorization paths or overwrite sealed units; relocation changes execution bindings. The README gives exact command templates. Other operating systems need a reviewed engineering monitoring port; never disable safeguards.

Do not change research question/L1 terminology, population/tails/duplicates, grouping/split function/seed, features/blacklist, target/encoding, CPU model/version/two threads, candidates/seeds, validation-only selection/tie break/global test gate, metrics/bootstrap weighting/unit/count/seed/CI, finite analysis/strata or triage thresholds. Do not add invented controls, samples, a model zoo, GPU training, full-source broad runs or temporal/pod_hourly work. Preserve the October 6 failed gate and completed marginal results. Any future experiment is a new explicitly distinguished run; never backfill outputs into this checkpoint.

Referenced but not supplied historical artifacts remain absent: docs/protocol_versions/checkpoint1, original Mac feasibility/test logs, original local_validation/delivery files, temporal maps, duplicate-pod database/artifacts, matched-cohort sources and original AcmeTrace correspondence. These absences are documented and are not newly created omissions. No Git history or independently authenticated source release was supplied. No Google Drive upload is claimed.
