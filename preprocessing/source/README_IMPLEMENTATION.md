# Local protocol and safety implementation

Read `docs/protocol.md`, `docs/DATASET_AUDIT.md` and `config/protocol.yaml` first. The config uses JSON-compatible YAML and requires no YAML dependency for current checks.

Run fixture tests from the project directory:

```sh
.venv/bin/python -B -m unittest discover -s tests -v
```

The completed source-backed D109H00 validation is recorded in `results/audits/local_validation.json`; delivery provenance is in `results/audits/delivery.json`. Original audit scripts and artifacts were preserved. The eligible output has 62,573 IDs; it is distinct from the historical 113,443-ID map.

If a repeat local check is needed, use a fresh output directory (existing output is never overwritten):

```sh
.venv/bin/python -B scripts/validate_local.py --output-root /tmp/asi-validation-new-run
```

Current scope: local schema/sample/split/feature checks, direct source-backed temporal eligibility, manifests, and tested safety helpers. No training scripts or remote downloader are implemented yet. `read_range` validates an already-open response; its eventual caller must enforce timeouts, bounded requests, transfer budgets and checkpoints. Do not run the historical remote readers unchanged.

Proposed future dependency installation, NOT executed or approved in this stage:

```sh
/Users/tiloschan/Desktop/asi_dataset/.venv/bin/python -m pip install lightgbm scipy PyYAML
```

No scikit-learn dependency is currently needed; add it only if future code actually requires it. After an approved install, verify LightGBM import and record exact resolved versions before freezing the training environment. If its macOS OpenMP runtime is missing, report the import failure and propose that separate prerequisite rather than silently installing system software.

Before training, resolve the explicit pending implementation choices in config, finish paired training/evaluation scripts, verify a bounded dry run, and report measured resource estimates for approval. No scientific results are implied by these smoke checks.
