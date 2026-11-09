# Experiment 2 — Partition sensitivity

## What was executed

This post-hoc sensitivity study compares lifecycle-metadata additions across workload-disjoint partition seeds 20260927 and 20261020. M0 uses resource, priority and application/model controls; M1 adds `job_type_public`. The second partition's original cloud runner keeps model seed 20260927, train-only categorical encoding, twelve candidates per family, a 200-round cap and 30-round early stopping.

The two saved execution-weighted validation gains are **+2.083576% and −4.906626%**. Equal-workload gains are **+3.664494% and −2.754915%**. The phase-one report uses *deterioration* `(M1 − M0)` for some tables; the compact CSV uses *improvement* `(M0 − M1)`. These signs are opposite by definition, not conflicting observations.

All reported evidence here is **validation-only**. The saved source contains a later proposed held-out evaluation phase, but the inspected result export contains selection/freeze artifacts, not a completed independent test evaluation. The planning document is not evidence that its proposed phase ran.

## File guide

| Path | Role |
| --- | --- |
| [notebooks/exp02_colab_execution_original.ipynb](notebooks/exp02_colab_execution_original.ipynb) | Original 20-cell Colab execution record |
| [notebooks/exp02_colab_diagnostics_original.ipynb](notebooks/exp02_colab_diagnostics_original.ipynb) | Original 38-cell execution and follow-up diagnostic record |
| [notebooks/exp02_colab_execution.ipynb](notebooks/exp02_colab_execution.ipynb) | Presentation copy with Markdown overview/setup/section headings |
| [notebooks/exp02_colab_diagnostics.ipynb](notebooks/exp02_colab_diagnostics.ipynb) | Presentation copy separating execution from post-run diagnostics |
| [archived-source/cloud_package/](archived-source/cloud_package/) | Original cloud runner, pipeline, Dockerfile, requirements, protocol and provenance |
| [results/cloud-results/run_colab_02/](results/cloud-results/run_colab_02/) | Original binding, freeze, environment, encodings, selection and candidate JSON records; models omitted |
| [exp2_reported_validation_values.csv](exp2_reported_validation_values.csv) | Two-partition compact historical values |
| [ASI_phase1_prediction_instability_diagnostics/](ASI_phase1_prediction_instability_diagnostics/) | Original phase-one analysis source, protocol, findings and supplemental method note |
| [ASI_instability_mitigation/](ASI_instability_mitigation/) | Historical diagnostic/mitigation reports and protocol; not a new successful mitigation claim |
| [provenance/](provenance/) | Original reassessment review and small execution/memory logs |

`exp2_phase1_findings_original.md` and the same report within the diagnostic folder are intentionally retained at established paths; the manuscript package also keeps its frozen input copy.

## Reproduction and provenance

The originals came from `experiment_2_source.zip`. The nested original selection tarball supplied source plus checksums. Both local `asi_colab_source_audit` archives independently match its recovered source byte-for-byte. No missing execution code was rewritten.

The notebooks retain their exact code, outputs, execution counts and metadata. Markdown was added only in the presentation copies. They use Colab `/content` paths; the main selection cell trains if run. Later cells retain historical `run`, `run_colab_01` and `run_colab_02` path checks rather than automatically following a new run directory.

The original tarball and its train/validation Parquets remain external. `SHA256SUMS` and `FREEZE.json` still refer to original dataset/model artifacts omitted from this repository: full freeze or package verification requires restoring those exact external artifacts. Compact JSON evidence does not substitute for fitted models or prediction arrays. The original first-partition training implementation has not been separately bound to a complete original execution package here; later diagnostic code and historical first-partition values are preserved.

Inspect saved outputs first. The historical cloud plan describes the original sequence and environment, including a proposed test-release phase; this pass neither executed it nor accessed held-out data. Static repository checks are documented in the [root README](../../README.md).
