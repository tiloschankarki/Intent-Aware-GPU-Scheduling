# Frozen ASI lifecycle predictive-information protocol

Status: materialized before model training or lifecycle-ablation results. The original research handoff is preserved verbatim in `HANDOFF_ORIGINAL.txt`; this document and `config/protocol.yaml` operationalize it. No main experiment has run.

## Approved schema clarification

**Schema/label clarification made before model training and before observing lifecycle-ablation results.**

| Conceptual lifecycle | Authoritative physical ASI value |
|---|---|
| offline inference | `offline_inference` |
| online inference | `online_inference` |
| training | `training` |
| dev | `dev` |

The handoff's “offline” and “online” were shorthand. This is a schema/encoding clarification, NOT a scientific-protocol or population change: all six observed category counts exactly match the earlier audit. Filters, configuration, outputs and reproducibility artifacts use physical strings. Do not recode source data.

## Question and limits

Does prospective execution/lifecycle type add predictive information for individual GPU/ML execution duration beyond available prospective controls, including on unseen workloads? Compare M0=f(X) with M1=f(X,O). This is predictive, not causal.

L1 is lifecycle; L2 is planned computational scope; L3 is model/application semantics; L4 is workload/configuration identity. Do not conflate these or call L2–L4 experimental objective. ASI lacks adequate public scope, user/tenant identity and user-history controls. `workload_id` is a configuration proxy, not a user ID. Prior-art novelty is only a bounded negative search, not proof that no related paper exists. See original handoff for rejected directions and provenance.

## Populations and features

Primary broad lifecycle: training, offline_inference, online_inference, dev. Exclude unknown/other from primary modeling, retain descriptive counts. Secondary finite-execution: training versus offline_inference. Preserve rare categories and heavy tails. Do not remove repeated-pod rows from the non-temporal main experiment or invent composite execution IDs. No automatic exact-row deduplication is introduced.

R = gpu_request + gpu_spec_public; P = priority_class; A = model_type_public + is_genai_request; O = job_type_public; W = workload_id.

Required matched comparisons: R vs R+O; R+P vs R+P+O; R+P+A vs R+P+A+O. Where meaningful in seen-workload analysis: R+P+A+W vs R+P+A+W+O. Every pair uses identical population/split rows and equivalent selection budgets.

Forbidden predictors: duration_hours, schedule_delay_sec, ready_delay_sec, ready_status, schedule_status, server_id, pod_id. The target is used only as target; IDs may support joins/splits but never bypass feature guards. Telemetry and inferred lifecycle are forbidden. Use an explicit allowlist as well as the blacklist.

## Splits, models and metrics

Primary generalization: non-null workload IDs, approximately 70/15/15 percent of workload groups, deterministic and disjoint. Group fractions need not equal row fractions. Implementation seed 20260927 is recorded before training/results; deterministic SHA-256 assignment is order-independent. Never group null workloads under a fake ID. Broad random-execution analysis retains null-workload rows and is a secondary reference, not the strongest generalization test. Chronological evaluation stays disabled pending separate research approval after Track A.

Primary model: LightGBM; target log1p(duration_hours); primary metric LogMAE. Select on training/validation only. Fit preprocessing on training only and keep held-out categories safe. Test data is for final evaluation only. No model zoo or test-driven selection.

Report absolute delta = MAE(M0)−MAE(M1), relative delta = 100×delta/MAE(M0), Spearman, interpretable runtime errors, lifecycle, finite-execution and tail summaries. Positive delta means improvement. Cluster uncertainty by workload for workload-disjoint evaluation; row bootstrap is not acceptable there.

Continue if approximately ≥3% primary strong-generalization improvement OR ≥5% important finite/tail improvement, with stable direction across seeds/bootstrap/robustness. Approximately 1–3% requires strong mechanism analysis. ≤1%, disappearance on unseen workloads, or mostly trivial Dev/Online separation without meaningful finite evidence kills the standalone contribution. These are frozen triage criteria, not universal laws; statistical significance does not replace magnitude.

## Track A temporal feasibility

Hard bound D108–D110, hourly members only. About 5.644 GiB of full-member transfer was previously estimated. Source eligibility requires pod_id to occur exactly once in execution summary. Lifecycle stratification retains all six recognized physical labels, including unknown/other descriptively; temporal eligibility itself does not add the primary modeling filter.

Preserve legacy temporal_map.parquet unchanged. It contains all-summary matches, not the eligible population. The separate D109H00 artifact must verify source membership, multiplicity exactly one, and recognized non-null lifecycle directly. Missing source IDs or invalid labels stop publication; repeated IDs are explicitly excluded and counted.

Build reusable eligible lookup once; do not scan 40.5M summary rows per hour. Validate status 206, exact Content-Range/object size and bounded body lengths before consumption. Abort on ignored Range, unexpected compression, truncation or bounds violation. Process one validated Parquet member at a time, parse day/hour from member path, track transferred bytes, and checkpoint durable map/diagnostics/member completion before deleting disposable raw files. Never redownload completed members automatically. The new local validator makes no remote requests and does not declare the legacy extraction a fully checkpointed remote hour.

Record per-hour unique pods, matched/new/cumulative eligible summary pods, day/hour, bytes and status. Report lifecycle coverage, per-day gains, abrupt changes, failures and projected expansion costs, then await a research decision. Observations are earliest within the scanned window, not proven submission/start times. The earlier 7.618% is reverse-direction single-hour linkage, not summary temporal coverage.

## Reproducibility and approvals

Preserve source schema, paths, counts/exclusions, categories, exact features/populations/splits, seeds, parameters, software versions, timestamps, hashes, elapsed time and failures in machine-readable manifests. Config is JSON-compatible YAML 1.2, allowing dependency-free loading for these checks. Hash protocol/config for every run; never rewrite frozen choices after seeing results without an explicit versioned amendment.

The handoff does not specify exact hyperparameter grid, bootstrap repetitions/CI/weighting, tail boundaries, extra seeds or all encoding rules. They remain visibly pending in config, rather than being falsely described as previously frozen. Resolve and record before main training. This stage implements only protocol materialization, safety helpers and local validation; the training/remote pipeline remains future work.

No package installs, network transfers or model training are authorized in this stage. Full execution requires readiness estimates and approval. Any data/design conflict stops execution for an explicit research decision.
