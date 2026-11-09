# Evidence guide

This guide binds new documentation to saved artifacts. Percent improvements use `100 × (M0 − M1) / M0`; older tables labeled deterioration use the opposite sign. Verifications check saved-record consistency without fitting or reconstructing predictions.

| Claim | Source | Check and boundary |
| --- | --- | --- |
| Experiment 1: 4,709,624 executions / 473,265 workloads | [Completed checkpoint](../experiments/experiment-1/exp1_checkpoint_original.md), canonical-population section | Historical counts also agree with Experiment 3's original-population audit. Canonical dataset was not opened. |
| About 5.88% R+P test gain | [Saved results summary](../experiments/experiment-1/archived-source/resume_reports/results-summary.json) | Mean of broad R+P gains for three model seeds; one fixed split. |
| Stronger-control gains 0.81–1.38%, intervals crossing zero | Same summary, broad R+P+A records; [compact CSV](../experiments/experiment-1/exp1_historical_report_values.csv) | Match all three saved gains and interval bounds. Historical held-out test summaries only. |
| Worse broad MAE in hours with stronger controls | [Completed checkpoint](../experiments/experiment-1/exp1_checkpoint_original.md), original-runtime results table | Compare the three broad rows' saved M0/M1 MAE; no new prediction scoring. |
| Experiment 2 gains +2.084% / −4.907% | [Validation CSV](../experiments/experiment-2/exp2_reported_validation_values.csv), [phase-one findings](../experiments/experiment-2/exp2_phase1_findings_original.md) | CSV improvements match report deterioration values with sign reversed. Validation-only. |
| Experiment 3 restricted population | [Population audit](../experiments/experiment-3/archived-source/population_audit.json), [registration](../experiments/experiment-3/exp3_preregistration_original.json) | Original minus excluded union agrees with eligible executions/workloads. ID-only exclusion provenance retained; no new dataset check. |
| Ten seeds, 12 candidates per model family, 240 outcomes | [Original report](../experiments/experiment-3/exp3_report_original.json), [registration](../experiments/experiment-3/exp3_preregistration_original.json) | Exactly ten registered seeds and 12 candidate IDs for each seed/role; selected winner is the minimum validation loss with lowest-ID tie breaking. |
| M1 wins 8/10 execution and 9/10 equal-workload comparisons | Original report and [selected table](../experiments/experiment-3/exp3_selected_validation.csv) | Recompute signs and relative changes from saved selected metrics; agree with saved report summaries. Not independent replication evidence. |
| Negative partitions, with seed 20261102 changing sign under weighting | Same report/table | Execution gains negative for 20261101 and 20261102; equal-workload gain for 20261102 positive. |
| Original runner bound to saved Experiment 3 registration | [Runner](../experiments/experiment-3/archived-source/exp3_runner.py), original registration `spec.runner_sha256` | Byte SHA-256 equality; frozen reference/protocol hashes also checked. |

The [static verifier](../analysis/verify_repository.py) performs reproducible consistency checks and does not open datasets, model binaries, prediction arrays or test outcomes. Original reports and frozen scientific files are unchanged. [Source gaps](source-gaps.md) records claims whose original backing is incomplete.
