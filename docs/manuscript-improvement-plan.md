# Manuscript improvement plan — 1 November 2026

## Central argument

Working title: **Partition and Weighting Sensitivity in ASI Execution-Duration Prediction: A Case Study**.

Question: Under the documented ASI populations, baseline controls, workload-disjoint partitions and validation-selection procedure, how much incremental predictive value does `job_type_public` provide?

M0 already includes semantic model/application controls. M1 adds one coarse public type field; this is not a comparison of semantics against no semantics, nor direct measurement of user intent. The target is released execution span, not demonstrated useful training work, queue time or scheduler performance.

## Connect the three experiments

| Experiment | Precise claim | Evidence and limits |
|---|---|---|
| 1: baseline dependence | Historical type-field gains shrink from roughly 5.88% with resource plus priority controls to 1.05% with richer application/model controls. | Three model seeds on one historical workload-disjoint split; informal averages, not three independent datasets. Historical test summaries only; principal intervals include zero and original-runtime MAE worsens. Report all seed values and distinguish secondary populations. No causal redundancy claim. |
| 2: partition sensitivity | Selected-validation relative improvements change from +2.083576% to −4.906626% across two partitions. | Saved verification and phase-one reports. Shared-record diagnostics indicate changed predictor behavior beyond evaluation-record composition, without isolating training or selection causes. Exploratory attribution is not a causal explanation. |
| 3: weighting and selection | On ten restricted-population partitions, M1 wins 8/10 execution-weighted and 9/10 equal-workload comparisons; seed 20261102 changes from −2.015% to +0.978% under reweighting of the same selected predictions. | Original report, registration and candidate records plus historical audit reconstructions. Models were selected on execution-weighted validation and evaluated on reused validation. Partitions overlap; counts are descriptive, not independent replications or future-success probabilities. |

These experiments are a sequence of increasingly careful questions, not one pooled effect or independent confirmations. Explicitly tabulate every population transition, exclusion, split role, feature set, model seed, selection metric and evaluation metric. Experiment 3's restricted population (341,617 workloads / 3,372,430 executions) must not be conflated with Experiment 1's population.

## Revision sequence

1. Replace the original intent-aware scheduler framing in the abstract/introduction with the bounded empirical question. Define LogMAE on log1p(hours), positive relative improvement as 100(L0−L1)/L0, and workload identity.
2. Add a protocol/evidence table before results. Separate historical test results from selected-validation diagnostics and frozen-plan analyses from exploratory analyses. Do not touch reserved outcomes.
3. Present Experiment 1 as motivation for stronger baselines; Experiment 2 as motivation for partition sensitivity; Experiment 3 as the scoped characterization. Use the six preserved figures only with explicit population and selection-status captions.
4. Report execution loss sum(S_g)/N and equal-workload loss mean(S_g/n_g) together. Neither is GPU-hour weighting or a fairness measure. A percent change in LogMAE is not a percent change in runtime or cost.
5. Describe selected retained rounds as associations with outcomes. Do not claim early stopping, concentration, or two workloads caused the reversal. Retained iterations differ from attempted iterations; no per-round curves were recovered.
6. Resolve the top-1% boundary tie convention: use ceil(0.01G), a documented workload-ID tie rule and the identical selected set for share/loss. Preserve historical differing values with explanation; do not silently harmonize them.
7. Omit the exact 0.2915 versus 0.2142 within-M1 attribution and 76,366 exact-profile count unless the original saved source is located. The prior audit marks these unverified.
8. Integrate the complete October 29 audit, replacing the historical package's audit-prefix limitation. Bind Experiment 1 weak-control numbers to the imported hash-verified results-summary. Verify citations from primary sources before submission; local literature notes are leads, not novelty clearance.
9. End with narrow external validity: one trace, restricted population, incomplete prediction-time provenance/source-to-split lineage, dependent partitions and validation reuse. No causal mechanism, new predictor, independently confirmed generalization or scheduling gain is established.

## Review gate using existing evidence only

Before circulation, every number needs a source path and evidence level (original summary, historical verification or derived table). Check captions against those sources, reconcile the tie convention, audit feature timing and record unresolved items. No retraining, new experiments or reserved holdout access is part of this plan.

The defensible deliverable is an empirical case study or technical report. Stronger prose cannot turn selected-validation results into independent generalization evidence.
