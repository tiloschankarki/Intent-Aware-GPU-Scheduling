# Preprocessing and dataset audit source

[source/](source/) preserves `asi_dataset_source.zip` faithfully: pipeline, dataset/temporal builders, original audit utilities, frozen configuration, tests, dataset audit and historical documentation. Every imported file was compared byte-for-byte with the corresponding file under the local `~/Desktop/asi_dataset` tree; all matched. No local raw trace, dataset export, model, environment or cache was copied.

Read [the pipeline README](source/README_PIPELINE.md), [protocol](source/docs/protocol.md), [dataset audit](source/docs/DATASET_AUDIT.md) and [configuration](source/config/protocol.yaml). These are earlier development-stage records and should be interpreted in their historical context. They are not the final Windows execution package.

The later frozen execution package is preserved separately under [Experiment 1's checkpoint source](../experiments/experiment-1/archived-source/checkpoint/). The old `preprocessing/archived-source/checkpoint/` files were byte-identical to that checkpoint and consolidated there. Earlier preprocessing implementations are not silently replaced by the later ones; the snapshots contain real implementation differences.

Original scripts can download data, write outputs, fit models or prompt for deletion of a processed source file. They are archival source, not steps run during repository organization. External source data and historical environment setup are necessary for computational reproduction. Use the root static verifier for syntax and integrity checks without importing or executing these modules.
