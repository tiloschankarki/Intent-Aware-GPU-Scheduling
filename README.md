# GPU Runtime Prediction: Lifecycle Metadata, Workload Generalization, and Evaluation Robustness

Independent Computer Science research on the Alibaba ASI GPU trace. This repository studies the incremental predictive value of the public lifecycle field `job_type_public`, and how its apparent value changes with baseline controls, workload partitions and evaluation weighting.

The target is released execution duration, transformed as `log1p(duration_hours)`. The work does not establish a scheduling policy, user-intent measurement, causal mechanism or operational scheduling improvement. The local directory's legacy name does not describe the current research scope.

## Research questions

1. How much does lifecycle metadata add to resource and priority predictors, and how does that gain change after including application/model controls?
2. How sensitive is the incremental validation performance to workload-disjoint partition composition?
3. Across ten predefined partitions of a restricted population, how do execution-weighted and equal-workload comparisons differ, and how concentrated are the observed gains and losses?

## Dataset and scope

The original canonical study population contains **4,709,624 executions and 473,265 workload IDs**, with four recognized lifecycle categories and workload-disjoint splits. It is a metadata-rich subset of the ASI trace, not the entire GPU fleet. See the [original checkpoint](experiments/experiment-1/exp1_checkpoint_original.md).

Experiment 3 excludes the union of the two historical test workload sets using saved ID-only split maps: **1,337,194 executions / 131,648 workloads** are excluded, leaving **3,372,430 executions / 341,617 workloads**. This is a restricted-population study, not a direct full-population replication; see its [population audit](experiments/experiment-3/archived-source/population_audit.json).

## Experiments and main findings

| Experiment | Saved evidence | Finding | Evidence boundary |
| --- | --- | --- | --- |
| [1 — Lifecycle metadata value](experiments/experiment-1/README.md) | Historical held-out test summary and frozen Windows execution source | Mean relative LogMAE gain of about **5.88%** against resource + priority controls across three model seeds on one split. With stronger application/model controls, gains are **0.81–1.38%**, and all three saved 95% intervals include zero. | Historical held-out test evidence; model seeds share a split and are not independent datasets. |
| [2 — Partition sensitivity](experiments/experiment-2/README.md) | Two saved validation comparisons, Colab execution/diagnostic notebooks, original cloud runner and follow-up reports | Execution-weighted relative gains change from **+2.084%** to **−4.907%** across two partitions. | Validation-only, post-hoc sensitivity analysis; no independent test result. |
| [3 — Predefined partition robustness](experiments/experiment-3/README.md) | Original registration/report, **240 candidate records**, CPU runner and notebook | M1 wins **8/10** execution-weighted and **9/10** equal-workload comparisons. Execution-weighted reversals occur for seeds 20261101 and 20261102; the latter favors M1 under equal-workload weighting. | Twelve candidates per model family per split seed; selected-validation results on a restricted population. No independent test result. |

Lifecycle metadata does **not** consistently improve prediction. The stronger-control effect is small and uncertain in Experiment 1; Experiment 2 reverses sign; Experiment 3 retains negative partitions. Saved concentration and support diagnostics help characterize these patterns, but do not establish their causes. The original-runtime MAE in Experiment 1's broad stronger-control comparison worsens despite lower LogMAE; the metrics answer different questions.

Source numbers and arithmetic checks are indexed in [the evidence guide](docs/evidence-guide.md). Unsupported exact attributions are recorded in [source gaps](docs/source-gaps.md), rather than promoted to findings.

## Metrics and interpretation

LogMAE is absolute prediction error on `log1p(hours)`, not error measured in hours. Relative improvement is `100 × (L0 − L1) / L0`, with positive values favoring M1. Execution weighting gives each execution one vote; equal-workload weighting averages within workload and then across workloads. Neither is GPU-hour weighting or a fairness measure.

In Experiments 2 and 3, M0 includes resource, priority and application/model features; M1 adds `job_type_public`. Experiment 3 selects models on execution-weighted validation loss and reports both metrics on that same validation data. Overlapping splits are dependent, and win counts are descriptive, not independent-replication probabilities or significance tests.

## Repository structure

```text
preprocessing/              Earlier source-backed preprocessing and audit snapshot
experiments/
  experiment-1/             Historical test evidence and frozen execution source
  experiment-2/             Validation sensitivity, source, notebooks and diagnostics
  experiment-3/             Restricted-population robustness, source and registration
analysis/                   Static integrity/evidence verifier and audit index
audits/                   Dated research and artifact audits
figures/                    Index and historical reproduction script
literature/                 Index of retained ASI-related prior-art audits
paper/                      Frozen October 29 manuscript, data and figure package
docs/                       Evidence guide, provenance, limitations and organization record
```

Original experiment result filenames remain at their existing paths so that historical references and manuscript scripts stay usable. Original and presentation notebooks have distinct filenames. Historical source layouts are retained where imports and relative paths rely on them.

## Reproducibility

**Review and verify without training:**

```sh
python3 -B analysis/verify_repository.py
```

The new standard-library verifier parses Python and notebook JSON, checks recorded file hashes and notebook preservation, and verifies arithmetic/selection consistency from saved summaries. It does not import experiment modules, execute notebooks, train models or open datasets/holdouts.

Start with the [experiment index](experiments/README.md), each experiment README and the [source gaps](docs/source-gaps.md). Historical source is preserved byte-for-byte, including its original environment and execution instructions. Those instructions describe earlier stages and are not current completion certificates.

Full computational reproduction requires external raw/canonical or train/validation data, original environments and omitted run artifacts. Dataset paths and hashes remain in frozen provenance. Do not silently substitute inputs, protocols or package versions. No installation, training, new experiment or holdout evaluation was performed for this organization pass.

The [historical figure script](paper/asi_manuscript_2026-10-29/reproduce_figures.py) regenerates figures from saved reports and also rewrites derived CSVs/manifests in its own directory. Use a separate scratch copy if reproducing it; this pass did not run it or regenerate figures.

## Limitations

- One trace and selected populations limit external validity; workload-disjoint splitting does not establish temporal or cross-cluster generalization.
- A public lifecycle field is not direct user intent. Prediction-time availability and source-to-split lineage are not fully certified.
- Stronger controls materially reduce apparent value. A positive LogMAE change does not establish lower runtime, cost, queue delay or scheduling benefit.
- Validation reuse and dependent splits limit inference in Experiments 2 and 3.
- Missing per-workload aggregates, original model binaries and some source provenance prevent complete numerical reproduction from this compact repository alone.
- Retained audits identify prior-art and methodological limits; this pass did not newly verify external citations or establish novelty.

## Current status

Experiments 1–3 have saved evidence. The repository is an empirical research record and manuscript work in progress, with explicit reproduction gaps. It is not presented as publication-ready or as an independently confirmed scheduler improvement. See the [organization record](docs/organization-report.md) for this pass and the [historical manuscript revision plan](docs/manuscript-improvement-plan.md) for remaining scientific/editorial work.

The existing [license](LICENSE) is retained. Dataset and third-party material remain subject to their own terms.
