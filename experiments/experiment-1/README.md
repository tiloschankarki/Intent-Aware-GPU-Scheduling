# Experiment 1 — Lifecycle metadata value

## What was executed

The frozen workload-disjoint study used 4,709,624 executions and 473,265 workloads, split by SHA-256 workload assignment with split seed 20260927 and 70/15/15 thresholds. Model seeds 20260927, 20260928 and 20260929 vary fitting randomness on that fixed split. The primary comparison adds `job_type_public` to resource + priority + application/model controls; weaker R and R+P controls and the finite population are historical secondary comparisons.

This experiment contains historical **held-out test** evidence. The full population count is not the test-set size; the broad summary reports 711,321 test executions.

## Saved findings

- R+P relative LogMAE improvements are 5.949393%, 5.844247% and 5.848031% (mean about 5.88%).
- R+P+A improvements are 0.946168%, 0.814672% and 1.378673%. All three relative-gain 95% intervals include zero.
- The original checkpoint also reports worse broad-population MAE in hours under the stronger-control comparison. Lower LogMAE is not uniform improvement across loss functions.

These are historical saved summaries, not newly recomputed predictions or independent confirmations. A claimed exact single-workload attribution of 55–56% is not repeated here because its original supporting artifact has not been verified in this pass.

## File guide

| Path | Role |
| --- | --- |
| [exp1_checkpoint_original.md](exp1_checkpoint_original.md) | Historical completed-run report: population, protocol, split rules, results, environment and archive boundaries |
| [exp1_historical_report_values.csv](exp1_historical_report_values.csv) | Compact historical figure/report values |
| [archived-source/resume_reports/results-summary.json](archived-source/resume_reports/results-summary.json) | Original saved test summary for controls, populations and model seeds |
| [archived-source/checkpoint/](archived-source/checkpoint/) | Original checkpoint Python package, scripts, tests, frozen config, environment and historical engineering/provenance records |
| [archived-source/checkpoint/config/protocol.yaml](archived-source/checkpoint/config/protocol.yaml) | Unchanged frozen protocol |
| [archive-records/](archive-records/) | Original content-addressed archive inventory and archival README |

## Reproduction and provenance

The source archive `experiment_1_source.zip` supplied the checkpoint tree. The previously imported pipeline under `preprocessing/archived-source/checkpoint/asi_pipeline/` was byte-identical to this checkpoint and has been consolidated here. Original relative layout within `checkpoint/` is preserved, so scripts still find their package/configuration. Historical source and pre-engineering variants remain explicitly separated.

Read `archived-source/checkpoint/README_PIPELINE.md`, `docs/protocol.md`, `config/protocol.yaml`, `environment/requirements-windows.txt` and the completed-run report before attempting reproduction. They refer to different historical stages; the Windows completion report and frozen protocol govern interpretation. Historical commands can train models or access outcomes; none were run in this pass.

The compact repository omits canonical data, split maps, fitted models, prediction arrays and resource checkpoint outputs. The archive inventory and historical SHA256SUMS describe the original larger packages, not a completeness claim for this selected source tree. Original source alone cannot reproduce every test statistic without those external artifacts and the original environment. No original Experiment 1 notebook was found in the inspected source archive; none was substituted or invented.

Run `python3 -B analysis/verify_repository.py` from the repository root for static integrity checks only. See [source gaps](../../docs/source-gaps.md) for unresolved evidence and environment limits.
