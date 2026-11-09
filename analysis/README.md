# Analysis and verification

[verify_repository.py](verify_repository.py) is a new organizational verifier using only the Python standard library. From the repository root:

```sh
python3 -B analysis/verify_repository.py
```

It checks recorded inventory hashes, syntax, notebook cell preservation, authored Markdown links, and arithmetic/selection consistency of saved evidence. It does not import research code, run notebook cells, fit models or read datasets/holdouts. Checks establish consistency of retained artifacts, not independent scientific reproduction.

Historical analyses remain at their established paths:

- [Experiment 2 phase-one source and reports](../experiments/experiment-2/ASI_phase1_prediction_instability_diagnostics/).
- [October 29 audit](../audits/research-audit-2026-10-29/), including the original saved-validation-sums verifier. That verifier requires external workload Parquets; it was not executed here.
- [Experiment 3 saved diagnostics](../experiments/experiment-3/exp3_report_original.json).

See [evidence guide](../docs/evidence-guide.md) for numerical source bindings and [source gaps](../docs/source-gaps.md) for the unavailable artifacts.
