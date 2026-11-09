# Organization record — 7 November 2026

## Delivery status

This is a **prepared, validated filesystem copy**, not a claim that the Desktop repository has already been changed. The session's permitted write locations exclude `~/Desktop/Intent-Aware-GPU-Scheduling`. The owner chose to reopen that repository as a writable project. Apply the reviewed changes in that project, preserving its `.git` directory; do not replace the whole directory or perform Git operations.

The prepared copy excludes `.git`. Original source archives and the Desktop repository remain untouched. An external review/recovery folder contains the original baseline hashes, replaced documentation, removed proposal, file-by-file changes, duplicate review and final tree. A guarded apply script is supplied there for a session with Desktop write access; it refuses changes when the prepared copy or existing repository differs from its recorded baseline.

## Changes prepared

- Replaced the outdated root proposal with the current runtime-prediction research landing page, precise questions, dataset/evidence boundaries, mixed/negative findings and reproducibility limits.
- Added experiment-level READMEs distinguishing historical test evidence from selected-validation evidence.
- Imported original Experiment 1 checkpoint execution source, scripts, tests, protocol/environment and historical engineering records. Consolidated the previous byte-identical `preprocessing/archived-source/checkpoint/` source under the complete Experiment 1 checkpoint.
- Imported the independent earlier preprocessing/audit snapshot under `preprocessing/source/`, with a byte comparison to the local `asi_dataset` source.
- Imported Experiment 2's original cloud package source, Dockerfile, protocol, compact freeze/selection/candidate records and small logs; retained historical diagnostic/mitigation evidence at existing paths.
- Imported Experiment 3's original runner, frozen reference, supporting source/protocol and provenance, independently cross-checked against both local source archives and registered code hashes.
- Added original executed notebooks and all three presentation copies under experiment `notebooks/` directories. No original code, output, metadata or scientific claim was rewritten.
- Added a standard-library static/evidence verifier, evidence guide, current source gaps and file/source manifests. Updated preprocessing, analysis, literature, figures and documentation indexes.
- Strengthened `.gitignore` for raw datasets, trained model assets, archives and generated caches.

Exact created/edited/removed/moved file paths are in the external review package's `changes.json` and this tree's [organization provenance](organization-provenance.json).

## Consolidation and retained duplicates

Eighteen duplicate figure exports formerly under `figures/historical/` matched the frozen manuscript exports byte-for-byte and were consolidated into `paper/asi_manuscript_2026-10-29/figures/`. The manuscript's script and all its inputs keep their original relative paths. The duplicate `archive-records/CHECKPOINT_COMPLETED.md` matches `exp1_checkpoint_original.md` and was removed from the prepared copy only after hash verification.

The obsolete `docs/README.original-2026-11-01.md` contains the old scheduler proposal and no ASI experiment evidence; its exact original bytes were moved to the external recovery package. Finder metadata and the empty obsolete `References/` directory are excluded from the prepared copy.

Frozen manuscript data copies, original/presentation notebook pairs, independently versioned source snapshots and established phase-one report paths are intentional duplicates. Hash matches do not justify destroying a self-contained frozen package or silently changing historical source layout. Every duplicate hash group is listed in the external duplicate review. Existing source/docs that describe earlier stages remain historical, rather than being rewritten to imply later results were available then.

## Sources integrated and exclusions

All four requested source archives were found: `experiment_1_source.zip`, `experiment_2_source.zip`, `experiment_3_runner_source.zip`, `asi_dataset_source.zip`. Also inspected/integrated: both Experiment 2 source-audit copies, `experiment_3_source.zip` and the original `Experiment3_bundle.zip`. Their archive hashes, member paths, selected-file hashes and exclusions are recorded in [provenance](organization-provenance.json).

Datasets, trained model files and large/generated checkpoint outputs remain external. The full Experiment 3 bundle's recorded checksum matches. Its compact source members match their original member hashes; the excluded Parquet input was not opened for analysis. Original historical checksum manifests are preserved even where they refer to deliberately omitted external artifacts.

## Validation scope

Run `python3 -B analysis/verify_repository.py` to verify this compact tree. It checks file hashes, Python syntax, notebook JSON structure and preservation, authored local links, saved summary arithmetic/selection and the absence of data/model/cache/large-file additions. The organization process additionally compared imports to archive bytes, verified consolidation destinations and checked that all prior files are retained, accounted for at identical destinations, or preserved in recovery.

The original Desktop baseline is checked again before any application. No training, experiments, dataset construction, imports of historical research modules, new test evaluation, figure regeneration or Git commands were run. All baseline scientific source/results/protocol files retain their original bytes or verified identical relocated bytes. Historical absolute/external links remain in immutable research records; authored landing-page/document links are checked within this compact tree.

## Remaining review items

[Source gaps](source-gaps.md) separates recovered execution code from missing data/artifacts. In particular, the original exact 55–56% Experiment 1 single-workload attribution was not verified and is omitted from new headline findings; no original Experiment 1 notebook was found; Experiment 3's complete workload-loss/COMMIT tree and an external `sensitivity` table remain unavailable. The manuscript stays a historical draft; citation verification, source-to-split lineage, feature timing, tie conventions and unresolved exact decompositions remain research limitations.

**Required owner action:** reopen the Desktop repository with write access, apply/review this prepared file set, and handle all Git operations personally. No scientific design decision was changed or delegated to the owner merely for naming/formatting approval.
