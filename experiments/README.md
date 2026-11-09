# Experiment index

| Experiment | Primary question | Evaluation evidence | Start here |
| --- | --- | --- | --- |
| 1 | Lifecycle metadata value under stronger baseline controls | Historical held-out test results; three model seeds on one workload split | [Experiment 1](experiment-1/README.md) |
| 2 | Sensitivity to workload partition composition | Two selected-validation partitions | [Experiment 2](experiment-2/README.md) |
| 3 | Robustness and weighting across predefined restricted-population partitions | Ten selected-validation partitions; fixed model seed | [Experiment 3](experiment-3/README.md) |

These experiments have different populations and evidence levels. They are not pooled independent replications. Original summaries retain their existing filenames. `archived-source/` contains historical implementations, not newly rewritten equivalents; `notebooks/` distinguishes originals from presentation copies. Source/protocol/output files preserve their original bytes.

Source archive identities, exclusions and consolidation mappings are in [organization provenance](../docs/organization-provenance.json). Dataset/model archives remain outside the compact repository. Reading the notebooks' saved outputs does not require running their training cells.
