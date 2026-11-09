# Experiment 3 — restricted-population split robustness

This is a new restricted-population robustness study, **not** a direct replication of the original full-population results. No historical test file or test outcome was opened to build this package. No prior artifact was modified. The saved historical split maps were used only for exclusion membership and exclusion bookkeeping; historical holdout IDs are not included in the delivered input.

## Population

| Population | Executions | Workloads |
|---|---:|---:|
| Original | 4,709,624 | 473,265 |
| Historical test union excluded | 1,337,194 | 131,648 |
| Eligible for Experiment 3 | 3,372,430 | 341,617 |

The historical test sets contain 70,705 and 71,500 workloads, with 10,557 in common. Eligible data retain 71.61% of executions and 72.18% of workloads. The remaining population can differ in feature/outcome composition and estimand. This package makes no claim that full-population performance transfers. Historical outcome distributions were not examined to characterize that difference.

Only original seed-20260927 train/validation exports were queried, joined to the eligible ID mask before returning any feature or outcome values. The historical seed-20261020 test workloads present in those exports were excluded. The original full canonical file and historical test files were not opened. Input checksums and counts are in `population_audit.json`.

## Use in Google Colab

1. Upload **Experiment3_bundle.zip** to Google Drive, for example `MyDrive/ASI_Experiment3/Experiment3_bundle.zip`. Do not upload historical archives or test files.
2. Open **Experiment3_Colab_CPU.ipynb** in Colab. Select a CPU runtime with about 12 GB RAM. A GPU is unnecessary.
3. Run installation, Drive mount and setup cells. Edit only `ZIP_PATH` and `RUN_DIR` if needed. Use a new, empty run directory the first time; reuse the same directory only to resume the same registered run. Allow the Drive mount when Colab requests it.
4. Run the registration cell. It saves the immutable study definition to Drive **before any research fit**. It fixes ten new split seeds, the data/code checksums, hyperparameter grid, model seed, metrics, resource bounds and failure policy.
5. Run the **one-seed pilot** cell. It runs the complete 12-candidate grid for M0 and M1 (24 fits), checkpoints every candidate to Drive, freezes both selections, and reports sampled peak RAM, available RAM and time. The pilot is the first of the ten seeds, not an extra seed that can be replaced after seeing results.
6. Inspect the pilot. The notebook requires sampled process RSS at most 8 GiB and at least 2 GiB available system RAM. The estimated compute time excludes some loading/diagnostic/Drive overhead and is not a Colab availability guarantee. A failed pilot prohibits the remaining seeds. There is no smaller-grid or subsampling fallback.
7. Set `RUN_REMAINING = True` in the sweep cell and run it to execute the other nine seeds sequentially. This toggle does not change the registered study. Stop if you do not have enough session time; resume the same run later. Do not replace seeds or change the scientific settings.
8. Run the report cell at any time, including after an interruption. It lists all ten seed statuses. Research scores are absent until actually computed.

After a Colab disconnect, reconnect/mount Drive, rerun setup and registration with the **same** `RUN_DIR`, then rerun the pilot/sweep cells. Completed candidates are verified and reused. A candidate interrupted before its commit marker is retained with an `.incomplete-*` name and retrained. A checksum mismatch in a committed candidate stops the run; do not edit or delete committed research evidence. Use only one active notebook per run directory.

The runner uses fresh worker processes for each seed so memory returns between seeds. It keeps one seed's data and one candidate model at a time, loads only feature/target columns needed, retains native numeric dtypes, and does not cache full datasets or 24 models in memory. Source data are copied to local Colab storage for reads; all scientific checkpoints go directly to Drive. A quarter-second resource sampler plus per-round checks can miss brief peaks; this is explicitly sampled memory evidence, not a guaranteed process limit. Colab/runtime termination can interrupt a candidate, which is why candidate checkpoints exist. Drive acknowledgments/checksums do not guarantee immediate remote cloud durability during a sudden disconnect; verify committed artifacts on resume.

## Frozen scientific procedure

- **Ten split seeds:** 20261028 through 20261106, inclusive. These were chosen before Experiment 3 outcomes were computed. **Model seed stays 20260927**, as in experiment 2. This measures split sensitivity conditional on one model seed; it is not a ten-model-seed study.
- Workload assignment uses the archived SHA-256 of compact JSON `[split_seed, workload_id]`, first 64 bits, with the original 70/15/15 thresholds. Seeds apply only to the eligible pool. No identity is a predictor.
- **M0:** gpu_request, gpu_spec_public, priority_class, model_type_public, is_genai_request. **M1:** M0 plus job_type_public.
- Archived feature selection and categorical processing are copied verbatim into `frozen_reference.py`. Sorted category vocabularies are fit on the current seed's training data only; missing/unseen categories map to -1; categorical columns use int32 and numeric features use float64.
- Target is `numpy.log1p(duration_hours)`. Native LightGBM 4.7.0 `regression_l1`, metric `l1`, learning rate .05, bagging fraction .8/frequency 1, deterministic column-wise training, two threads, no feature prefilter. The original 12 candidate IDs and ordering are preserved, as are 200 maximum rounds and native early stopping with patience 30.
- Select M0 and M1 independently by **execution-weighted validation LogMAE**, then lowest candidate ID on ties. Equal-workload LogMAE is secondary and never used to select candidates or rounds.
- The native Dataset/train/early-stop/predict sequence is preserved. The platform-specific stop-file hook is replaced by a resource-check callback at the same callback order; neither changes gradients, objective, encoding, sampling or selection. Original sources and checksums are included for review.

## Outputs and interpretation

`RUN_DIR/PREREGISTRATION/` stores the frozen definition and registration environment. Each `seeds/SEED/ROLE/candidate_NN/` contains result, selected boosting round, timing, sampled resources and model, with checksums and a commit marker. `SELECTION/` freezes the role's winner, all 12 candidate records and training vocabulary. `SUMMARY/` contains both winner metrics, diagnostics and eligible validation workload loss aggregates. `PILOT/` stores the pilot resource/time gate. `FAILURE_*.json` preserves invocation failures. `reports/` contains timestamped CSV/JSON snapshots and all completed candidate records.

LogMAE is mean absolute error on `log1p(hours)`, not MAE in hours. Execution-weighted LogMAE averages per execution. Equal-workload LogMAE first averages errors within each workload, then gives each workload equal weight. Positive M0-minus-M1 differences favor M1. No clipping is applied.

Diagnostics include per-partition workload/execution counts, lifecycle counts, top workload execution share, top 1% share, HHI/effective workloads, exact encoded-profile support, unseen-category fractions, selected validation error concentration and positive/negative workload contributions. Diagnostics use eligible training/validation data only. New test partitions receive membership counts only; no test predictions, loss summaries or label diagnostics are produced.

**All model metrics are validation results on data used for selection. They are not confirmatory test results.** New per-seed tests remain untouched, as do the excluded historical holdouts. A later confirmatory test evaluation would require a separately specified protocol and explicit authorization. Overlapping repeated splits are dependent; descriptive across-seed summaries are not independent replication evidence or p-values. Improvements do not establish scheduler benefit or causality.

## Verification boundary

The delivered notebook has no saved research metrics. The full eligible-data pilot and sweep must run in Colab. Local checks cover exclusion union, metric weighting, encoding, checkpoint integrity/recovery and synthetic-only training parity with the archived native training function; see `verification.json`. Synthetic checks are software tests, not research evidence or a 12 GB feasibility pilot.
