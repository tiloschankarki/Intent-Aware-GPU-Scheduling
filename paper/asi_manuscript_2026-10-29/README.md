# ASI manuscript package

Start with **manuscript_plan.md** for research questions, contributions, prior-work positioning, section structure and figure captions. **initial_draft.md** is the initial manuscript prose. This is an empirical case study, not a finished submission or an independently confirmed general improvement.

## Figures

| File stem | Content |
|---|---|
| fig01_historical_test | Historical test gain with weak/rich controls and reported conditional intervals |
| fig02_partition_weighting | All ten restricted-population selected-validation comparisons |
| fig03_concentration_attribution | Frequency concentration and signed aggregate loss attribution |
| fig04_selection_context | Selected boosting rounds and all candidates for one negative partition |
| fig05_evidence_map | Boundaries between the three experiments |
| fig06_historical_validation | Experiment 2 reversal and the shared-record diagnostic |

Every figure is supplied as vector PDF/SVG and 300-dpi PNG. Figures have publication-oriented styling; final dimensions and captions should follow the chosen venue. They do not imply submission readiness.

## Evidence provenance

| Local source | Original source | Use and evidence level |
|---|---|---|
| data/exp3_report_original.json | [Original consolidated report](https://drive.google.com/file/d/1Ntk1MhpLtjSHCcPceswH1Rikjack0aHs/view) | Directly retrieved saved aggregates, 240 candidates, ten winners per side and diagnostics |
| data/exp3_preregistration_original.json | [Original documented plan](https://drive.google.com/file/d/1ds2nOIhZPlORSfbwnM8ZgRnIxhRLHaqO/view) | Design, selection, excluded historical holdouts and secondary metric |
| data/exp1_checkpoint_original.md | [Historical completed checkpoint](https://drive.google.com/file/d/1wdEwx54Y-rF9ZSiopj0zuDek5LJ991Ra/view) | Historical test strong-control results and intervals; no test files reopened |
| data/exp2_phase1_findings_original.md | Existing October 26 phase-one saved report | Historical validation diagnostics and their stated verification; not rerun |
| data/audit_retrieved_prefix.txt | Referenced Research Question Selection conversation, audit user message | Retrieved first 20,000 characters; weak-control Figure 1 numbers are transcribed from this audit, not independently recovered from their original results-summary |

The full audit was longer than the conversation retrieval limit. No claim of complete line-by-line incorporation is made. The current package does not contain the ten original validation workload-loss Parquets. Its concentration panels reproduce saved report diagnostics rather than newly reconstructing workload-level losses. The manuscript distinguishes the prior audit's stronger workload-table checks from the aggregate checks performed here.

No synthetic-run outputs, model fits, saved prediction files, raw scientific rows or reserved holdout files were used to generate this package. Original scientific sources were left unchanged.

## Reproduce the figures

Run `python reproduce_figures.py` from this directory using Python with NumPy, pandas and Matplotlib. The generation environment used Python from the existing local Miniconda installation and Matplotlib 3.10.0. Exact versions are recorded in environment.json. The script reads only packaged reports, exports exact companion tables, verifies the candidate selections/metrics, and regenerates figures. It never trains or evaluates a predictor. The copies of original Markdown reports contain historical paths and instructions as source data; the plot script does not execute them.

`verification.json` records checks performed. `manifest.json` gives file hashes. Figure binary hashes can vary with renderer metadata/fonts; plotted values and semantic checks are the scientific reproducibility target. The weak-control results retain the audit's six-decimal precision.

## Needed only for extensions or submission provenance

- The full untruncated audit, to incorporate its remaining qualifications verbatim or line by line.
- Experiment 1 original weak-control aggregate results and inventory binding, to upgrade Figure 1 from audit-transcribed provenance.
- The ten original validation-only loss-sum Parquets and matching commits, if adding workload-level distribution figures or repeating the audit's hash/reconstruction checks.

No reserved holdout access or new model training is needed for the supplied draft or figures.
