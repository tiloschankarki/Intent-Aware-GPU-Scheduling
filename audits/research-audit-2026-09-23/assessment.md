# Field-level evidence assessment — 23 September 2026

**Verdict: 3. SUPPORTING EVIDENCE ONLY.** No certified public prospective DIRECT OBJECTIVE field was found in the recovered evidence. Public task roles and planned budgets support narrower questions; they do not establish the original experimental-objective hypothesis.

Read the [18-column matrix](field-evidence-matrix.html) first. The [Markdown record](field-evidence-matrix.md) exposes every cell without horizontal scrolling; the [JSON](field-evidence-matrix.json) preserves all columns and evidence references. There are 141 rows, including explicitly marked absence checks and evidence gaps, not 141 verified dataset fields.

## Evidence boundary

No new literature search or dataset download was performed. Evidence comes from the prior conversation, existing downloaded sources in /tmp/gpu-scope-audit, saved audit outputs, and the current user-supplied Acme author clarification. Existing field-level audit notes in this folder were also recovered and retained unchanged. This assessment does not certify that every named paper has been audited: ORA, F-DATA, PREP, Park & Hong, unspecified workflow datasets, and SchedMate/Mars's extraction schema remain evidence gaps. UNKNOWN is not proof of absence.

Objective means the stated reason for this particular launch. Planned scope means intended work or execution plan. Application/model identity, configuration identity, resource requests, and user histories are controls, not purpose labels. An execution graph does not by itself identify purpose. CORE is reserved for evidence capable of testing the original hypothesis; no row qualifies. SUPPORTING ONLY does not automatically certify every proposed runtime experiment.

Prospective admissibility here concerns information timing, not legal permission. Dataset licenses and permissions were not independently audited. Predictive association is also not identification of a causal effect of changing objective.

## A. DIRECT-OBJECTIVE inventory

**Empty among verified public fields.** No recovered field simultaneously gives a trustworthy per-launch objective measurement and the necessary prospective provenance.

Acme's unavailable names are not certified direct labels: the actual strings and naming rule are unavailable. Its released type is not a prospective substitute. Model labels and constant benchmark-wide purposes do not supply varying per-execution objective observations.

## B. PLANNED-SCOPE inventory

- **NAS-Bench-101: record `epochs`, backed by `config['train_epochs']`.** Independently configured budgets 4/12/36/108 are documented; only epoch-4 rows were measured in the local prefix audit. The benchmark provides measured training time, but uses TPU hardware. It supports a budget-runtime study, not GPU-cluster objective prediction.
- **NATS-Bench: `--hyper` / `hp`.** Topology launcher explicitly selects 12/200 training schedules. This is genuine planned scope. However, the inspected collector uses `reset_pseudo_train_times`; these processed timing targets cannot automatically support an independent measured-runtime effect claim.
- **LCBench: fixed 50-epoch protocol.** Prospective but constant. Intermediate epoch observations are progress along that protocol, not evidence of independently assigned shorter run budgets.
- **MLPerf LoRA configuration: `LOAD_CKPT`, `WARMUP_TRAIN_STEPS`, `WARMUP_VALIDATION_STEPS`, `VAL_CHECK_INTERVAL`.** Genuine declared execution-plan settings. Checkpoint initialization is not evidence of interrupted-run recovery. A public configuration/result pair is insufficient to establish variable-cohort coverage or that warm-up is included in scored runtime.
- **GenTD26: `num_inference_steps`, `num_images_per_prompt`.** Scope-shaped request fields paired with execution time. Strict requested-versus-realized count provenance remains incomplete; prospective use is conditional.

Walltime limits are not included as planned training work. Worker counts and task counts are resource/structure metadata, not number of experimental trials. Actual stop steps are outcomes.

## C. Objective-adjacent inventory

1. **PAI `task_name`:** only the documented task-function distinction earns adjacency. The paper connects worker/ps with training and evaluator with inference. This is closer to execution purpose than BERT/ResNet because it describes function within execution. It still does not establish debugging versus final training, profiling, or checkpoint evaluation. Other literal names such as TVMTuneMain must not be promoted to certified purpose labels from spelling alone. Full job-submission availability of all eventual task roles remains unverified.
2. **Acme original job-name hints:** reportedly contributed purpose hints, but names and sanitized names are unavailable. No reproducible prospective predictor can use them.
3. **Alibaba GPU 2026 `job_type_public`:** training/inference/dev activity buckets plausibly relate to purpose. Construction, timing, and submission-snapshot provenance are not sufficiently established for the original experiment.

These are not multiple validated independent proxies suitable for triangulation.

## D. False friends

- PAI `group`: composite configuration hash, not experimental objective. Raw script, arguments, sources and sinks are unavailable.
- PAI `workload`, MIT `model`, Alibaba `model_type_public`: application/model semantics.
- Desensitized `job_name`, job IDs, user IDs, organization IDs, virtual clusters: identities.
- Resource requirements and worker multiplicities: scheduler metadata.
- ATLAS encodings and duration histories: transformed controls; no new purpose observation.
- Acme `type`: retrospective label using actual duration. Values Debug/Eval do not rescue it.
- GenTD26 `predict_type`: generation operation, not debugging/evaluation/production purpose; checkpoint_model_version_id identifies a model version, not checkpoint-evaluation intent.
- MLPerf `run_stop.metadata.step`: realized stopping point.
- LCBench epoch positions and NATS `iepoch`: trajectory/query position, not necessarily a distinct prospective budget.
- MIT array indices: array mechanics, not certified hyperparameter trials. All 3,430 labelled jobs in the saved audit share the sentinel array-task value; no purpose interpretation follows.
- Generic source code, user prompts, and workflow graphs: possible containers of information, not verified objective observations without actual contents and provenance.

PAI already compares Group/User/Resource/GPU feature combinations for duration prediction (section 5.2, Figure 12). Reproducing that result would not demonstrate the value of objectives.

## E. Public-data intersection

| Candidate | Prospective | Public | Runtime paired | Adequate provenance for proposed claim | Result |
|---|---|---|---|---|---|
| DIRECT OBJECTIVE | None verified | — | — | — | Empty intersection |
| PAI task_name | Before task execution; parent submission conditional | Yes | Yes, task timestamps | Functional role documented; objective mapping absent | Supports task-role experiment only |
| Acme name hints | Plausible, not fully verified | No | No released pairing | Insufficient | Fails |
| Acme type | No: duration-derived | Yes | Yes | Known outcome dependence | Fails |
| Alibaba 2026 activity bucket | Unknown | Yes | Sampled execution spans | Insufficient | Fails strict intersection |
| NAS-Bench-101 epochs | Yes | Yes | Yes, measured training time | Yes for declared budget; TPU domain | Passes narrow scope intersection, not GPU/objective hypothesis |
| NATS hp | Yes | Yes | Processed timing present | Pseudo-time replacement compromises independent measurement claim | Do not certify measured-runtime ablation |
| LCBench 50-epoch protocol | Yes | Yes | Yes | Constant, no independent budget variation | No incremental scope experiment |
| MLPerf scope settings | Yes | Yes | Public result example | Variable cohort and timing alignment unverified | Not yet certified |
| GenTD26 steps/images | Plausible request inputs | Yes | Same table | Requested-versus-realized not fully established | Conditional, not certified |

No field passes the objective intersection. One external benchmark provides a clear narrow budget intersection; that is not evidence for latent objective. Availability does not guarantee enough variation, independent observations, or generalizability.

## F. Dataset-level feasibility

YES/NO below means established feasible from this evidence record. For sources marked NOT ESTABLISHED, NO is an evidence-status verdict, not a demonstrated dataset absence. “Supporting” means a separate relevant analysis, not identification of objective.

| Dataset/source | Direct objective? | Planned-scope experiment? | Supporting/indirect evidence? | Why |
|---|---|---|---|---|
| PAI 2020 | NO | NO | YES | Role, recurrence and controls; no released verified epochs/trial budget |
| ATLAS | NO | NO | YES | Derived PAI features do not create purpose observations |
| Acme | NO | NO | YES | Retrospective characterization only; type cannot be prospective input |
| Helios/QSSF | NO | NO | YES | Metadata/history controls; private names and Helios estimator unavailable |
| Philly | NO | NO | YES | Metadata and attempt durations; no objective/budget field |
| MIT Supercloud | NO | NO | YES | Model identity and scheduler controls, not execution purpose |
| Alibaba GPU 2026 | NO | NO | YES | Activity characterization; temporal provenance incomplete |
| Alibaba GPU 2023 | NO | NO | YES | Resource/placement trace |
| Alibaba GPU 2025 | NO | NO | YES | Serving component/application data; no launch-purpose measure |
| Alibaba spot GPU | NO | NO | YES | HP/Spot is service priority, not objective |
| GenTD26 | NO | NO—prospective certification incomplete | YES | Request-scope candidate; separate serving problem |
| NAS-Bench-101 | NO | YES—TPU benchmark only | YES | Explicit varying epoch budgets and measured time |
| NATS-Bench processed topology data | NO | NO—independent measured-time test not certified | YES | Genuine budgets; pseudo-time targets |
| LCBench | NO | NO—budget constant | YES | Configuration/learning-curve analysis |
| MLPerf inspected configuration/result | NO | NO—varying matched cohort not established | YES | Prospective settings, incomplete timing alignment |
| Menear/Eagle | NO—objective not established | NO—scope not established | YES | Known requested wallclock/user controls; exact raw mapping not recovered |
| SchedMate/Mars | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | Only local summary; extraction schema and public pairing missing |
| ORA | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | Primary field evidence not recovered |
| F-DATA | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | Primary field evidence not recovered |
| PREP | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | Primary field evidence not recovered |
| Park & Hong | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | Primary field evidence not recovered |
| Unspecified workflow datasets | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | No exact released schema/semantics recovered |
| HPOBench / IBM AI4DL | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | Search leads, not certified field audits |
| CloudBrain-I | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | YES—paper-level only | Raw launch-command artifact unavailable in prior notes |
| Chakra | NO | NO—NOT ESTABLISHED | YES—execution structure only | Observed runtime graph is not prospective purpose |
| Borg | NO—NOT ESTABLISHED | NO—NOT ESTABLISHED | YES—generic controls only | No verified ML purpose mapping |

## G. Final empirical kill test

**Choose 3: SUPPORTING EVIDENCE ONLY.** The original experimental-objective hypothesis is not identified by this evidence. No CORE field is certified.

Choice 2 would require multiple genuinely purpose-related prospective observables with a defensible mapping; several generic identities, or one task role plus epoch budgets from a different benchmark, do not satisfy that. Choice 4 would overstate the case if read as a claim about every existing public dataset: there are genuine scope/role observables, and several named sources remain unaudited. Within the fully inspected production GPU schemas, the specific latent objective remains unobserved or outcome-contaminated.

A model may predict runtime from Group because configuration repeats. It may predict runtime from evaluator because the executable function differs. It may predict runtime from epochs because work amount differs. None of those results establishes added value from why the user launched this execution, conditional on the controls.

**Download decision:** no additional files are justified for a direct-objective or triangulation experiment, because neither condition is met. Do not download whole traces hoping to recover missing names or unhashed arguments. The needed missing evidence is a genuinely prospective purpose measurement with independently established provenance and runtime pairing—not more copies of the existing metadata.
