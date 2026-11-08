# Frozen exploratory additive-correction protocol

This is one exploratory extension of the supplied research question. Historical test outcomes influenced the question. This experiment opens only the explicitly identified training and validation Parquet files and selected model artifacts; it never opens test datasets, test predictions, or test evaluations. Source archive scripts are read as text where needed and never executed or imported.

## Phase A gate

All four saved validation models must reproduce recorded execution-weighted LogMAE within 1e-10, with correct feature order, encodings, and tree counts. Both dataset pairs must match their recorded SHA-256 hashes, contain the expected rows, and have disjoint workloads. These checks passed before this protocol was frozen. Baselines are saved models, never replacements.

## Single mitigation and fitting decisions

For each split separately, predict log1p(duration_hours) as saved M0(x) + g(job_type). The four types are training, online_inference, offline_inference, dev. No clipping in log space and no other architecture, correction, or tuning will be attempted.

Fit g using the corresponding training partition only. The fitting entry point has no validation-file read. Workload IDs are used solely for folds and weights, never as model predictors.

- Three outer workload folds: `int.from_bytes(SHA256(JSON([20261026, workload_id], separators=(',', ':'), ensure_ascii=True))[:8], 'big') % 3`.
- For each outer fold, hold its workloads out completely. In the remaining workloads, use a fixed inner stopping set when `int.from_bytes(SHA256(JSON([20261027, workload_id], separators=(',', ':'), ensure_ascii=True))[:8], 'big') / 2**64 < 0.15`.
- Fit the original split-specific selected M0 hyperparameters without a new search. Preserve L1 objective, learning rate, bagging, feature fraction, leaves, minimum leaf size, original model seed 20260927, two threads, deterministic and column-wise settings. Train up to 200 rounds, early stopping patience 30 on the inner stopping workloads.
- Refit on all outer-training workloads for the inner-selected number of rounds, then predict the held-out outer workloads. Outer targets are never used for early stopping. Native categorical encodings are refit on each fitting subset using sorted string categories; missing/unseen categories map to -1.
- Every training row receives exactly one out-of-fold prediction. Within each type, weight residuals `r_i = log1p(duration_i) - OOF_M0_i` by `1 / number_of_rows_of_workload_i_within_type`. Thus each workload present in the type contributes total weight one.
- Let `m_t` be the weighted median, defined as the smallest residual whose cumulative weight reaches at least half the total. Let `n_t` be the number of distinct training workloads present in that type. Set `g_t = n_t/(n_t + 1000) * m_t`. This explicit shrinkage estimator is not claimed to be an exact penalized L1 optimizer. An absent type gets zero.
- The 1000-workload pseudo-count is a fixed heuristic chosen to damp small groups, not estimated or validated. The equal-workload fit is chosen to prevent high-frequency workloads from controlling the type correction. It can worsen execution-weighted loss. No alternate weighting or shrinkage strength will be tested.
- Fit and save both split corrections and their hashes before evaluating either against validation targets. Phase A and descriptive diagnostics may use validation targets, but the correction fitting function cannot read them.

## Differences from the original full-training M0

Saved full-training M0 models remain the deployed baselines. Fold models train on fewer workloads. For a strict out-of-fold residual, stopping must occur on inner training workloads, followed by refitting; using outer targets for stopping would leak their labels. Iteration counts may therefore differ from 94 and 141. Original full-model hyperparameters and iteration selection were historically chosen with the external validation set: this extension cannot undo that selection dependence. We fix those selected hyperparameters as requested and do not call this fully nested validation of the whole original selection procedure. Software version is exactly LightGBM 4.7.0, while OS and other library versions may differ; all are recorded.

## Evaluation decisions

Use saved M0/M1 validation predictions reproduced in Phase A, plus exactly one corrected M0 vector. Report MAE of raw log predictions, execution mean and mean of workload mean errors. Positive improvement means baseline MAE minus candidate MAE; relative improvement divides by baseline MAE. Report comparisons to both M0 and M1, and type-specific errors. For a workload with multiple types, type-specific equal-workload metrics average its errors within that type; overall metrics average all its executions.

Use 1000 paired nonparametric workload bootstrap replicates, seed 20261028, percentile 95% intervals. Sample all validation workloads with replacement and use the same draws for the three models; execution weighting is ratio of sampled workload error sums to sampled row counts, equal-workload weighting is mean sampled workload MAE. Intervals condition on saved/fitted models and this partition; they exclude fitting, model-selection, protocol-selection, and between-partition uncertainty. The two splits overlap in the underlying population and are not independent replications.

Operational success is prespecified as positive point improvement versus M0 on both metrics for the second split, and at most 0.5% relative degradation versus M0 on either metric for the original split. This 0.5% materiality boundary is a disclosed judgment, not a scientific constant. Report uncertainty regardless of whether this rule passes, and distinguish passing point estimates from convincing evidence.

Descriptive diagnostics: log-duration quantiles and means by type and partition; equal-workload means; top 1% and top 10 workloads' execution shares; within-type variation across workload mean durations; M0/M1 errors and contribution to excess error. These characterize associations, not causes. No causal mechanism or novelty claim follows from them. No new literature novelty claim is attempted.

## Implementation and verification plan

1. Audit and selectively recover original artifacts; verify model/data hashes, tree counts, feature order, categorical mappings and baseline scores. Save `phase_a_verification.json` and validation predictions.
2. Verify fold disjointness, encoding behavior and weighted-median/shrinkage calculations on deterministic synthetic cases before fitting. Freeze this document's hash in `protocol_freeze.json`.
3. Fit the training-only corrections once for both seeds. Persist fold counts, stopping rounds, OOF predictions and corrections. No validation reads in this stage.
4. Run the fixed evaluation and diagnostics, save all requested deliverables, then verify counts, finite metrics, row coverage, file hashes and output consistency. Preserve negative results.
