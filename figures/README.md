# Figures

The canonical historical PDF, PNG and SVG exports are in [the frozen manuscript package](../paper/asi_manuscript_2026-10-29/figures/). All eighteen former `figures/historical/` convenience files were byte-identical to those exports and have been consolidated there. No unique figure was removed or regenerated.

| Figure stem | Topic |
| --- | --- |
| `fig01_historical_test` | Experiment 1 baseline dependence and historical test intervals |
| `fig02_partition_weighting` | Experiment 3 partition/weighting comparison |
| `fig03_concentration_attribution` | Historical concentration diagnostics |
| `fig04_selection_context` | Selected validation candidate context |
| `fig05_evidence_map` | Evidence/population boundaries |
| `fig06_historical_validation` | Experiment 2 validation sign reversal |

[reproduce_figures_historical.py](reproduce_figures_historical.py) is the original convenience script; the identical [manuscript script](../paper/asi_manuscript_2026-10-29/reproduce_figures.py) keeps the correct relative `data/` and `figures/` layout. Use the manuscript copy in a separate scratch directory if needed. It overwrites derived CSVs and metadata as well as figures. No figure reproduction was run in this pass.
