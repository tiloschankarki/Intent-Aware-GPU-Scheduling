# Completed ASI archive

The full frozen experiment completed successfully, but prospective lifecycle metadata did not support a strong standalone contribution beyond the principal controls: unseen-workload LogMAE gains were 0.946%, 0.815% and 1.379%, every principal 95% workload-bootstrap interval included zero, and separately fitted finite-execution gains were 0.315%, 0.627% and 0.310%. Primary original-runtime MAE worsened. Final decision: **KILL AS STANDALONE CONTRIBUTION**, explicitly a research judgment because the frozen protocol did not resolve mixed seeds near the 1% boundary. Execution PASS is not hypothesis PASS; no causal independence or universal zero effect is established.

## Package map

- CHECKPOINT_COMPLETED.md: self-contained scientific history, protocol, results and final judgment.
- FILE_INVENTORY.json: every logical artifact path, exact size and SHA-256, plus historical source location.
- objects/<sha256>: one ordinary file per unique content; all essential canonical/model/prediction/bootstrap bytes are local.
- SHA256SUMS.txt: every package file except this checksum manifest itself.
- portable_archive.py: standard-library package reconstruction/seal checker; optional exact-dependency metric reproduction.
- SOURCE_DISCOVERY.json, OMISSIONS.json, PACKAGE_VERIFICATION.json: inputs, explicit exclusions and pre-ZIP structure audit.

Materialized paths: checkpoint/ (current frozen code/config/docs/tests/data and historical provenance), october6/upload/ (the exact original archive and sidecars), october6/extracted/ (its complete payload), completed_run/ (authorization, passed feasibility and all scientific outputs), resume_reports/ (ADARSH environment/tests/audit/driver history). Identical logical files share a blob in the ZIP and become independent copies when materialized. No hardlinks or external storage are required. Historical absolute path strings are immutable provenance, not access instructions.

## Verify and extract

First compare the ZIP SHA-256 with the external SHA256SUMS.txt. Extract using an ordinary ZIP utility into any new directory, on any drive. Enter the extracted ASI_COMPLETED_2026-10-13 folder. With a trusted Python 3 interpreter:

```powershell
python -B portable_archive.py verify --package . --workspace reconstructed --report ../portable-structure-verification.json
```

The workspace must not already exist. This verifies complete package inventory/checksums, materializes every original logical file, checks 524 seals and artifacts, 432 candidates, 36 selections/test units, 18 paired evaluations, candidate selection rules, authorization/hash relationships and global freeze ordering using only relative paths. It does not execute archived orchestration scripts, train, download or edit historical artifacts. The independently extracted ZIP was additionally checked on ADARSH with full scientific verification; see external ARCHIVE_VERIFICATION.json.

## Reproduce metrics without retraining

Use native Windows CPython 3.12.10 (the explicitly recorded portability exception), not MSYS2. Create a fresh venv outside the package and install the exact pins in reconstructed/checkpoint/environment/requirements-windows.txt. Use its Python as `python` below. No install/download is performed by the verification tool.

```powershell
python -B portable_archive.py reproduce --package . --workspace reconstructed --report ../metric-reproduction.json
```

This freshly reads the canonical Parquet/counts/assignments, pairs saved predictions, recomputes overall/lifecycle/finite/eight-tail-bin metrics and all 1,000 bootstrap samples for each of 18 evaluations, and compares with stored values at 1e-12 absolute/relative tolerance. It imports the frozen metric implementation from the reconstructed package, never uses original absolute paths and never fits models. Paired losses are reproducible from duration_hours plus the two ordered prediction Parquets; stored bootstrap Parquets additionally retain paired sampled losses/counts. Timing and timestamp fields are historical, not re-created metrics.

## Training reproduction, only if separately needed

Do not execute the archived resume_driver.py: it is historical orchestration with old paths. Work from a fresh independent materialization, native Windows CPython 3.12.10, exact pins and two CPU threads. Enable UTF-8, run pip check and all 54 tests, and perform read-only canonical validation first. Do not rebuild splits/canonical data. Create a *new*, absent output directory and a new authorization manifest from the archived authorization, retaining full_execution_authorized=true and the unchanged protocol SHA-256 while changing feasibility_manifest and experiment_freeze to fresh absolute destinations. Never edit/reuse the archived sealed authorization or old output units. Example from reconstructed/checkpoint with $py bound to the fresh native venv:

```powershell
$env:PYTHONUTF8 = '1'
& $py -m pip install -r environment/requirements-windows.txt
& $py -m pip check
& $py -B -m unittest discover -s tests -v
# After the read-only canonical validation and fresh authorization preparation:
& $py -B scripts/windows_feasibility.py run --dataset windows_run/canonical --output NEW_RUN/feasibility --config config/protocol.yaml --authorization NEW_RUN/authorization.json
# Only with a matching PASSED feasibility manifest and both workers complete:
& $py -B scripts/run_windows_science.py run --dataset windows_run/canonical --output NEW_RUN/science --config config/protocol.yaml --authorization NEW_RUN/authorization.json
```

The scientific driver performs all validation-only selections, global freezing, test predictions and paired bootstrap/secondary reports in order. Stop at a failed gate or unsafe resource conditions; never relax thresholds or change scientific design for a result. Other operating systems need separately reviewed engineering monitoring support. Raw source data is unnecessary for this canonical experiment and is not included. Fetching raw for a new independent source audit would require its recorded official URL/hashes and a separate purpose; nothing in this archive downloads it automatically.

Upload only the finished ZIP, external SHA256SUMS.txt, ARCHIVE_VERIFICATION.json, CHECKPOINT_COMPLETED.md and this ARCHIVE_README.md to a **new** Google Drive folder. Do not overwrite the October 6 checkpoint. No Drive upload has been performed or claimed.
