# Experiment 3 — Robustness across predefined partitions

## What was executed

The restricted population contains **3,372,430 executions and 341,617 workloads** after excluding the union of both historical test workload sets using ID-only maps. Ten predefined workload-disjoint split seeds run from 20261028 through 20261106. Model seed remains 20260927. These are split repetitions conditional on one model seed, not ten independent model-seed studies.

M0 is resource + priority + application/model controls; M1 adds `job_type_public`. Each family has twelve LightGBM candidates per seed (240 total), selected by execution-weighted validation LogMAE with lowest-ID tie breaking. Equal-workload LogMAE is secondary. Original source, grid, encoding, patience, caps and preregistration are unchanged.

## Saved findings and boundaries

The original report records ten completed seeds: **8/10** execution-weighted wins and **9/10** equal-workload wins for M1. Seeds 20261101 and 20261102 have negative execution-weighted gains (−6.119481% and −2.015370%); 20261101 also has a negative equal-workload gain. For 20261102, equal-workload weighting gives +0.978313% on the same selected predictions.

All scores are **validation-only**, on data used for selection. Historical holdouts and new confirmatory test outcomes were not evaluated according to the saved report. Repeated partitions overlap; seed summaries and win counts are descriptive. Neither causality nor scheduling improvement follows from them.

## File guide

| Path | Role |
| --- | --- |
| [exp3_preregistration_original.json](exp3_preregistration_original.json) | Original registered specification and environment |
| [exp3_report_original.json](exp3_report_original.json) | Authoritative original report: 10 seed outcomes, 240 candidates, diagnostics and failure history |
| [exp3_selected_validation.csv](exp3_selected_validation.csv) | Historical per-seed selected model metrics |
| [exp3_candidate_records.csv](exp3_candidate_records.csv) | Compact historical candidate table |
| [exp3_concentration_attribution.csv](exp3_concentration_attribution.csv) | Historical concentration/attribution values, with existing conventions retained |
| [archived-source/exp3_runner.py](archived-source/exp3_runner.py) | Original CPU runner |
| [archived-source/frozen_reference.py](archived-source/frozen_reference.py) | Original frozen feature/split helper implementation |
| [archived-source/reference_source/](archived-source/reference_source/) | Original supporting source, including eligible-input preparation |
| [archived-source/original_protocol.json](archived-source/original_protocol.json) | Unmodified archived protocol |
| [archived-source/population_audit.json](archived-source/population_audit.json) | Population exclusions, source paths and hashes |
| [archived-source/PACKAGE_MANIFEST.json](archived-source/PACKAGE_MANIFEST.json) | Original bundle-member hashes; includes externally retained eligible data |
| [notebooks/exp03_colab_cpu_original.ipynb](notebooks/exp03_colab_cpu_original.ipynb) | Original uploaded execution/diagnostic notebook |
| [notebooks/exp03_colab_cpu.ipynb](notebooks/exp03_colab_cpu.ipynb) | Presentation copy; original cells and all metadata retained |
| [provenance/Experiment3_bundle.sha256](provenance/Experiment3_bundle.sha256) | Original full-bundle checksum |

## Provenance and reproduction

The original local `Experiment3_bundle.zip` has SHA-256 `f102a8de54e37fbd5e065135f6717e2a4e7489b170117fdf8e683f38279e5ea0`. The small `experiment_3_runner_source.zip` independently matches all recovered source members. The original report/registration's runner hash binds the recovered `exp3_runner.py` to the recorded implementation. The 41 MB `inputs/eligible.parquet` is deliberately excluded; the full external bundle is retained.

The archived bundle README and `verification.json` describe the **pre-run software-verification stage**, when research fits were still pending. The later saved registered report documents completion. Both records are historical and must remain distinct; the old “not executed” statement is not a claim that the later research did not happen.

Read the notebook without running it. Original execution caveats remain visible in presentation Markdown:

- `ZIP_PATH` is `/content/Experiment3_bundle.zip` despite original prose suggesting a Drive upload; the file must exist at the configured path.
- The saved sweep flag is already `RUN_REMAINING = True`; executing that cell can launch fits after the pilot gate.
- The final workload-composition cell references `sensitivity`, which is not defined in the notebook. Its final consistency assertions need an external table.
- Diagnostics use a hard-coded Drive run directory and require external saved workload-level Parquets.

Exact full-run reproduction requires the original input/environment and omitted per-candidate commits/models and workload-loss summaries. This source-only tree is not the full Colab run directory. Original manifest verification cannot succeed against a deliberately reduced data/model tree. No training, installation, new report generation or test evaluation was performed in this organization pass.
