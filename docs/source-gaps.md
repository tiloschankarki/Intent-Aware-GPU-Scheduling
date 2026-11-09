# Source availability and reproduction limits

## Recovered and verified in this pass

- Experiment 1's original checkpoint package, scripts/tests, protocol and historical engineering records were recovered from `experiment_1_source.zip`. The original saved results summary was already present and retained.
- Experiment 2's two original notebooks, cloud runner/pipeline, Dockerfile, requirements, protocol, freeze/selection/candidate records and small execution logs were recovered from `experiment_2_source.zip`. Both source-audit archive copies match the recovered code.
- Experiment 3's original CPU runner, frozen helpers, supporting source and original protocol were recovered from the full `Experiment3_bundle.zip` and independently matched against `experiment_3_runner_source.zip`. The full bundle checksum matches the saved checksum. The saved registration binds the recovered runner and helper hashes. Original saved report/CSV/registration files match `experiment_3_source.zip`.
- The preprocessing source snapshot matches the corresponding files in `~/Desktop/asi_dataset` byte-for-byte.
- All three presentation notebooks match the originals' code cells, outputs, execution order/counts and notebook metadata. Added Markdown is distinguishable from the original record.

## External or missing artifacts

| Item | Status and consequence |
| --- | --- |
| Raw ASI trace, canonical datasets and historical split maps | Deliberately external. Original paths/hashes are retained in provenance; complete input construction and split-lineage verification were not performed here. |
| Trained models, candidate checkpoints, prediction arrays | Excluded from this compact repository. Original source archives remain untouched externally. A partial source/results tree cannot pass the original whole-run freeze verifier without these artifacts. |
| Experiment 1 original executed notebook | Not found in the inspected source archive. Original Python execution source is present; no unrelated notebook was substituted. |
| Experiment 1 exact 55–56% single-workload weak-baseline attribution | Context supplied by the owner, but an original supporting saved artifact was not verified in this pass. Omitted from new headline findings. |
| Experiment 2 original first-partition complete execution package | Not separately bound here. Historical validation values, saved diagnostics and the second-partition execution package are present. |
| Experiment 3 eligible input | The external original bundle contains `inputs/eligible.parquet`; it is excluded from the repository. The bundle remains at its original local location. Its input hash is recorded in the original manifest; the dataset bytes were not opened for this pass. |
| Experiment 3 ten workload-loss Parquets and complete per-seed COMMIT tree | Absent from the inspected compact source/results archives. Aggregate report/table consistency can be checked; full workload-level reconstructions and checkpoint verification require external run artifacts. |
| Per-round learning curves | Not recovered. Selected retained iteration counts do not establish early-stopping mechanisms. |
| Exact 0.2915/0.2142 decomposition and 76,366 profile count | Remain unverified as noted in the earlier audit; not added to headline findings. |
| External citations and prediction-time field provenance | Historical audits retained; no new external citation verification or complete feature-time/source-to-split certification. |

## Execution caveats

Original source and notebooks remain unchanged, including historical absolute paths and development-stage “not executed” statements. In Experiment 3, those statements describe the package-preparation stage; the later saved report documents the completed validation sweep. The notebook's configured local ZIP path differs from its Drive-upload prose, its remaining-seed toggle is already true, and the final diagnostic refers to an externally defined `sensitivity` table. These caveats are documented rather than silently fixed.

Original manifests and checksum files describe larger packages, including deliberately omitted datasets and models. The new file manifest verifies this compact organized tree; it does not imply the original whole-run package is complete here. Package pins/platform information are preserved as recorded; installation availability and cross-platform numerical equivalence were not tested.

No training, dataset construction, remote access, experimental report regeneration or new holdout evaluation was performed. Static checks and arithmetic on existing summaries do not constitute full computational reproduction. No Git operation was performed.
