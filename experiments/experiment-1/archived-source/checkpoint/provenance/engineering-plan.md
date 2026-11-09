# Windows safeguards implementation plan

Goal: implement the user's 2026-10-06 engineering authorization without changing any frozen scientific decision.
Spec: authorization attachment fec11788-667f-4165-8a63-e33eefab4a53/Pasted text.txt plus original takeover prompt.
Architecture: new execution modules reuse the existing feature/encoding/split/metric helpers. Atomic completed directories bind data, protocol, split, code, versions and context. Selection and prediction are separate phases. A separate Windows supervisor monitors fresh workers.

Constraints: preserve config/protocol.yaml bytes; CPU LightGBM 4.7.0; exact 12 candidates/seeds; exact population and split; all original 35 assertions/tests retained. No research downloads until safeguard tests pass. No git repository supplied; preserve baseline copy and hash manifests instead of creating commits/worktrees.

1. Checkpoints/selection (checkpoints.py, execution.py, modeling.py, train_cli.py): write failing tests for stale/partial/tampered units, missing selection, and interrupted candidate restart. Implement atomic unit directories with manifest-last publication and validate every referenced hash. Fit all candidates unchanged; freeze minimum validation LogMAE, candidate-index tie break. Test prediction must load a validated selection. Existing train_one becomes a compatibility wrapper; science orchestrator uses separate selection/test phases.
2. Windows monitor (windows_monitor.py, feasibility.py): write tests for conservative hard memory limits, sustained pressure, process exit failures, input preservation and safety latch. Monitor RSS, commit, memory, process I/O/page faults, system paging when obtainable, spill, time and logs. Fail closed on monitoring failure. Candidate 6 only, M0/M1 fresh processes, no predictive effect output.
3. Primary data (primary_data.py, prepare_windows.py): test schema/count mismatch and canonical reopening using synthetic fixtures. Official acquisition only after safeguards pass. Stream narrow audits, disk-backed exact distinct counts, original assign_workload function, exact expected counts. Canonical parquet retains workload and physical row ordinal. Fresh-process validation plus source/config/script hashes.
4. Audit: all original tests plus new tests; verify scientific file hashes and frozen configuration; review changes and record evidence. Only then download the official archive, perform numeric gates, then feasibility, then science if safe.

Review focus: partially published candidate; modified model file; config changed between freeze and test; resumed dataset changed; monitor failure/low commit before worker spawn. Each must fail closed and have regression coverage.

Progress: baseline saved; environment already validated; implementation pending.
