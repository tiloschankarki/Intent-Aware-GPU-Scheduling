# Pre-training completion and bounded end-to-end implementation

Goal: implement the user-approved frozen design without full training or remote transfer.
Spec: docs/protocol.md and config/protocol.yaml v2; prior versions archived before installing/training.
Architecture: streamed reusable Parquet dataset with source-row locators and immutable split membership; shared native LightGBM training for M0/M1; paired held-out evaluation with clustered bootstrap; independent bounded/resumable temporal pipeline.

- [x] Archive and complete protocol: seed, 12 candidates, native categorical handling, tails, paired bootstrap.
- [ ] Install exactly lightgbm scipy PyYAML (transitive dependencies permitted); record resolved environment.
- [x] Delegate independent temporal and metrics implementations with tests first; no real network in tests.
- [ ] Test then implement dataset construction, feature guard, native category dictionaries, fixed split logic and M0/M1 trainer.
- [ ] Unit/integration full suite; independent review for leakage/contamination/provenance.
- [ ] Bounded dry run: first 10000 raw source rows, principal pair, broad+finite, grouped+random, all 12 candidates, all 3 seeds. No scientific interpretation.
- [ ] Record wall time, peak memory, exact retained/split counts, models/artifact sizes and resource estimates. Stop for checkpoint.

Safety: no test selection, no lifecycle-derived encoding, no workload feature in primary, no full remote/full modeling gates enabled, no removal of historical artifacts, source/schema hashes in manifests. Config mutation midrun fails. Small source ordinal is storage location only, never execution identity or feature. Full-run resources remain estimates until separately approved profiling.
