# Protocol materialization and local safety validation

> Execute inline against the user-approved handoff and label clarification. No additional research-design approval is inferred.

Goal: materialize the frozen protocol, implement tested local safeguards, and verify legacy D109H00 eligibility directly against the source.
Architecture: immutable historical inputs; JSON-compatible YAML configuration; bounded DuckDB source join; new artifacts plus manifests; stdlib unittest safety checks.
Spec: ../../HANDOFF_ORIGINAL.txt and ../../protocol.md.

Constraints: no installs, network, training, deletion, or rewriting historical scripts/artifacts. No synthetic execution keys. Physical lifecycle strings are authoritative. Research conflicts stop work.

Review focus: missing/duplicated source pods; invalid lifecycle labels; full-body HTTP responses; workload overlap/null grouping; accidental replacement of existing artifacts.

- [x] Materialize config/protocol.yaml, docs/protocol.md, docs/DATASET_AUDIT.md; preserve original handoff.
- [x] Write tests before helpers: forbidden/unknown features fail; split assignment is deterministic and group-disjoint; null workload fails; temporal bounds enforce 108–110; range reads reject bad headers before reading bodies; source validation counts duplicates from source and rejects missing/invalid entries.
- [x] Implement asi_pipeline/safety.py and asi_pipeline/temporal.py, using bounded memory and no remote CLI.
- [x] Implement scripts/validate_local.py: metadata/schema, small sample, source-filtered legacy map, manifests and preservation hashes. Source membership requires one narrow pod/lifecycle scan, not rerunning all audits.
- [x] Run complete unittest suite and local validation; record verified counts separately from handoff claims.
- [x] Deliver additive files to project, verify original hashes, and report dependency command without executing it.

No Git repository exists; no commits or worktree changes are planned. Stage new files in /tmp because the selected project is outside this task's writable roots. Request filesystem approval only for concrete additive delivery/execution.

## Execution record

- Safety and temporal fixtures were written first; initial failures confirmed missing implementation. After implementation, 13 tests passed.
- End-to-end CLI fixtures failed before the validator existed; then 15 tests passed.
- Source-backed validation completed in 3.51 seconds: 113443 present, 50870 repeated, 62573 unique with recognized lifecycle. All 12 original root files retained identical hashes.
- Independent read-only review reran 15 tests and identified config-hash timing risk. A nested-config mutation regression failed before the fix and passed after. Final suite: 16 tests pass.
- Ruling: use JSON-compatible YAML to avoid an unauthorized package install. This is formatting, not a protocol change.
- Ruling: temporal stratification includes unknown/other descriptively; the frozen unique-source-pod eligibility rule is separate from primary modeling exclusions.
- Ruling: split seed 20260927 is an implementation choice recorded before training, not a handoff-specified seed.
- Existing source run preceded the config-hash guard fix; config bytes remained unchanged, and its recorded hash matches the delivered config. No expensive audit rerun was needed.
- Additive filesystem delivery is recorded separately in results/audits/delivery.json, including before/after historical hashes and final destination hashes.
