# Field-level evidence matrix

141 rows. EVIDENCE GAP, UNVERIFIED EXTRACTION COMPONENT, and ABSENCE CHECK rows are explicitly not observed raw fields. UNKNOWN is not NO. CORE requires evidence about the original objective hypothesis, so planned scope alone is SUPPORTING ONLY.

Prospective admissibility is an information-timing judgment, not a license/legal opinion. No independent license audit was performed. Prior-use and isolation columns say what is established, not what is absent worldwide.

## F001 — MLaaS in the Wild: pai_group_tag_table.group

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** pai_group_tag_table.group
- **4. Example values, if documented:** Hashed tag; 316,956 distinct in saved audit
- **5. Meaning according to source:** Hash of entry scripts, command-line parameters, data sources and sinks identifying recurring configurations.
- **6. Generator:** researcher/platform hash construction; exact producer time unknown
- **7. When it exists:** Inputs pre-execution; released hash generation time unknown
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived opaque hash; raw components not released
- **10. Outcome/runtime used in construction:** No duration input described; full implementation not certified
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Same configuration can serve multiple purposes; hash does not expose purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL: documented input-only hash plausible; freeze mapping and history
- **15. Prior runtime-prediction use:** YES: CART duration predictor; also ATLAS
- **16. Incremental contribution isolated:** YES: PAI Fig. 12 feature-set comparison, not objective ablation
- **17. Reproducible from public data:** YES for configuration-based comparison; exact replication needs protocol/artifact checks
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020; PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F002 — MLaaS in the Wild: pai_group_tag_table.workload

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** pai_group_tag_table.workload
- **4. Example values, if documented:** bert, ctr, nmt, inception, graphlearn, resnet
- **5. Meaning according to source:** Researcher-identified application based on customized inputs; sparsely populated.
- **6. Generator:** researcher annotation
- **7. When it exists:** Annotation timing unknown; input application exists before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released application label
- **10. Outcome/runtime used in construction:** Customized inputs described; duration use not described
- **11. Primary category:** APPLICATION SEMANTICS
- **12. Classification explanation:** Identifies application, not why this execution is launched.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL; prospective annotation procedure unverified
- **15. Prior runtime-prediction use:** YES in ATLAS workload encoding; not an objective experiment
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F003 — MLaaS in the Wild: pai_task_table.task_name

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** pai_task_table.task_name
- **4. Example values, if documented:** worker, ps, evaluator; also tensorflow, PyTorchWorker, TVMTuneMain
- **5. Meaning according to source:** Platform task names/roles. Paper connects worker/ps to training and evaluator to inference. Other literal names are not independently validated purpose labels.
- **6. Generator:** framework/platform task generation; user configuration upstream
- **7. When it exists:** Task definition before task launch; full job-submission snapshot not verified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Literal released task-name category
- **10. Outcome/runtime used in construction:** No outcome-based role construction described
- **11. Primary category:** OBJECTIVE-ADJACENT
- **12. Classification explanation:** Documented functional role relates to training/inference activity; does not distinguish debugging versus full training or checkpoint-evaluation intent.
- **13. Relationship to latent experimental objective:** plausible proxy
- **14. Prospective runtime-prediction admissibility:** YES for pre-task-launch role-based study; CONDITIONAL at parent-job submission
- **15. Prior runtime-prediction use:** Role analysis verified; standalone runtime-prediction ablation not established
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES for task-role comparison with execution times; job-level purpose experiment NO
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020; PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F004 — MLaaS in the Wild: pai_job_table.job_name

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** pai_job_table.job_name
- **4. Example values, if documented:** 4b3f04b66a525d2df903eb16
- **5. Meaning according to source:** Desensitized submitted-job name / identifier.
- **6. Generator:** user/platform original; release anonymization
- **7. When it exists:** at submission (original); release transformation later
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Desensitized identifier
- **10. Outcome/runtime used in construction:** No outcome dependence documented
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Opaque identifier; original lexical purpose hints cannot be recovered.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Join key; not evidence of objective
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F005 — MLaaS in the Wild: Entry script underlying Group

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** Entry script underlying Group
- **4. Example values, if documented:** Raw values not released
- **5. Meaning according to source:** Executable/script input to configuration hash
- **6. Generator:** user / framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** NO
- **9. Raw or derived/anonymized:** Only composite Group hash released
- **10. Outcome/runtime used in construction:** Input metadata described; no duration input described
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Potential container of information; no released objective/scope measurement.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Potentially before execution if accessible; unavailable here
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** NO for raw-feature experiment
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf; PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F006 — MLaaS in the Wild: Command-line parameters underlying Group

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** Command-line parameters underlying Group
- **4. Example values, if documented:** Raw values not released
- **5. Meaning according to source:** Argument input to configuration hash; may contain scope but raw values unavailable
- **6. Generator:** user / framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** NO
- **9. Raw or derived/anonymized:** Only composite Group hash released
- **10. Outcome/runtime used in construction:** Input metadata described; no duration input described
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Potential container of information; no released objective/scope measurement.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Potentially before execution if accessible; unavailable here
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** NO for raw-feature experiment
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf; PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F007 — MLaaS in the Wild: Data sources underlying Group

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** Data sources underlying Group
- **4. Example values, if documented:** Raw values not released
- **5. Meaning according to source:** Input dataset/source identifiers used in configuration hash
- **6. Generator:** user / framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** NO
- **9. Raw or derived/anonymized:** Only composite Group hash released
- **10. Outcome/runtime used in construction:** Input metadata described; no duration input described
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Potential container of information; no released objective/scope measurement.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Potentially before execution if accessible; unavailable here
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** NO for raw-feature experiment
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf; PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F008 — MLaaS in the Wild: Data sinks underlying Group

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** Data sinks underlying Group
- **4. Example values, if documented:** Raw values not released
- **5. Meaning according to source:** Output destination identifiers used in configuration hash
- **6. Generator:** user / framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** NO
- **9. Raw or derived/anonymized:** Only composite Group hash released
- **10. Outcome/runtime used in construction:** Input metadata described; no duration input described
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Potential container of information; no released objective/scope measurement.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Potentially before execution if accessible; unavailable here
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** NO for raw-feature experiment
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf; PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F009 — MLaaS in the Wild: user

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** user
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Submitter identity
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission for requests; inst_num snapshot provenance requires verification
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** YES: User/Resource or ATLAS aggregated inputs
- **16. Incremental contribution isolated:** PAI feature families compared; per-field effects not all isolated
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020; PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf

## F010 — MLaaS in the Wild: gpu_type_spec

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** gpu_type_spec
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Requested GPU type
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission for requests; inst_num snapshot provenance requires verification
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** YES: User/Resource or ATLAS aggregated inputs
- **16. Incremental contribution isolated:** PAI feature families compared; per-field effects not all isolated
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020; PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf

## F011 — MLaaS in the Wild: plan_gpu

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** plan_gpu
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Requested GPUs, expressed as percentages
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission for requests; inst_num snapshot provenance requires verification
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** YES: User/Resource or ATLAS aggregated inputs
- **16. Incremental contribution isolated:** PAI feature families compared; per-field effects not all isolated
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020; PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf

## F012 — MLaaS in the Wild: plan_cpu

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** plan_cpu
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Requested CPUs, expressed as percentages
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission for requests; inst_num snapshot provenance requires verification
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** YES: User/Resource or ATLAS aggregated inputs
- **16. Incremental contribution isolated:** PAI feature families compared; per-field effects not all isolated
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020; PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf

## F013 — MLaaS in the Wild: plan_mem

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** plan_mem
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Requested memory
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission for requests; inst_num snapshot provenance requires verification
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** YES: User/Resource or ATLAS aggregated inputs
- **16. Incremental contribution isolated:** PAI feature families compared; per-field effects not all isolated
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020; PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf

## F014 — MLaaS in the Wild: inst_num

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** inst_num
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Task instance multiplicity; launch count is not trial count
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission for requests; inst_num snapshot provenance requires verification
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** YES: User/Resource or ATLAS aggregated inputs
- **16. Incremental contribution isolated:** PAI feature families compared; per-field effects not all isolated
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020; PAIP: https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf

## F015 — MLaaS in the Wild: pai_job_table.start_time

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** pai_job_table.start_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Documented JOB SUBMISSION time, despite name
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F016 — MLaaS in the Wild: pai_task_table.gpu_type

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** pai_task_table.gpu_type
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Assigned GPU hardware
- **6. Generator:** user / scheduler
- **7. When it exists:** after placement
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** Placement-derived; not necessarily runtime-derived
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** NO at submission unless separately requested
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F017 — MLaaS in the Wild: pai_task_table.start_time

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** pai_task_table.start_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Task launch time
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F018 — MLaaS in the Wild: pai_task_table.end_time

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** pai_task_table.end_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Task completion time
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F019 — MLaaS in the Wild: pai_job_table.end_time

- **1. Paper/system:** MLaaS in the Wild
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** pai_job_table.end_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Job completion time
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F020 — Acme characterization: type

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** type
- **4. Example values, if documented:** Debug, Eval, Pretrain, SFT, MLLM, Other, CPU
- **5. Meaning according to source:** Released category uses job-name hints AND actual duration, per supplied author clarification.
- **6. Generator:** retrospective annotation
- **7. When it exists:** after runtime observation; final label not submission-certified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: job duration
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Duration participates in construction; purpose-like category names do not make it prospective.
- **13. Relationship to latent experimental objective:** plausible proxy
- **14. Prospective runtime-prediction admissibility:** NO for prospective prediction of the same runtime
- **15. Prior runtime-prediction use:** Characterization verified; prospective runtime use not established
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Can reproduce retrospective association only; invalid objective test
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** AUTHOR: User-supplied author clarification in current request: type uses job-name hints AND duration; raw/sanitized names cannot be released. No independent correspondence inspected.; ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F021 — Acme characterization: Original job-name purpose hints (unreleased)

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** Original job-name purpose hints (unreleased)
- **4. Example values, if documented:** Exact strings unavailable; do not infer them from type names
- **5. Meaning according to source:** Names contributed hints to category assignment. No original or sanitized names can be released.
- **6. Generator:** presumably user/framework; exact producer unverified
- **7. When it exists:** Original name plausibly before submission; version/timing unverified
- **8. Publicly available in released dataset:** NO
- **9. Raw or derived/anonymized:** Neither raw nor sanitized names available
- **10. Outcome/runtime used in construction:** Name itself not reported duration-derived; resulting type IS
- **11. Primary category:** OBJECTIVE-ADJACENT
- **12. Classification explanation:** Potential purpose-bearing text, but no strings or reliable mapping certify direct execution-purpose measurement.
- **13. Relationship to latent experimental objective:** plausible proxy
- **14. Prospective runtime-prediction admissibility:** Unavailable; prospective interpretation unverified
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** NO
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** AUTHOR: User-supplied author clarification in current request: type uses job-name hints AND duration; raw/sanitized names cannot be released. No independent correspondence inspected.

## F022 — Acme characterization: job_id

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** job_id
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Opaque job ID, not the withheld original job name
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F023 — Acme characterization: user

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** user
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Hashed submitter ID
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F024 — Acme characterization: gpu_num

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** gpu_num
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Requested GPU count
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F025 — Acme characterization: cpu_num

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** cpu_num
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Requested CPU count
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F026 — Acme characterization: node_num

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** node_num
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Number of nodes
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F027 — Acme characterization: mem_per_pod_GB

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** mem_per_pod_GB
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Pod memory configuration (Kalos)
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F028 — Acme characterization: shared_mem_per_pod

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** shared_mem_per_pod
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Shared-memory configuration (Kalos)
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F029 — Acme characterization: duration

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** duration
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Recorded duration; Seren and Kalos differ in observed formula
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F030 — Acme characterization: queue

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** queue
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Waiting time
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F031 — Acme characterization: gpu_time

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** gpu_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Duration multiplied by GPU count
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F032 — Acme characterization: state

- **1. Paper/system:** Acme characterization
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** state
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Terminal status
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F033 — Helios / QSSF: user

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** user
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Hashed user identity
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** QSSF uses historical job attributes; exact per-field inclusion not all verified
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData; QSSF: https://tianweiz07.github.io/Papers/21-sc.pdf

## F034 — Helios / QSSF: vc

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** vc
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Virtual cluster identity
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** QSSF uses historical job attributes; exact per-field inclusion not all verified
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData; QSSF: https://tianweiz07.github.io/Papers/21-sc.pdf

## F035 — Helios / QSSF: job_id

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** job_id
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Scheduler identifier reflecting submission order
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** QSSF uses historical job attributes; exact per-field inclusion not all verified
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData; QSSF: https://tianweiz07.github.io/Papers/21-sc.pdf

## F036 — Helios / QSSF: gpu_num

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** gpu_num
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** GPU requirement
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** QSSF uses historical job attributes; exact per-field inclusion not all verified
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData; QSSF: https://tianweiz07.github.io/Papers/21-sc.pdf

## F037 — Helios / QSSF: cpu_num

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** cpu_num
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** CPU requirement
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** QSSF uses historical job attributes; exact per-field inclusion not all verified
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData; QSSF: https://tianweiz07.github.io/Papers/21-sc.pdf

## F038 — Helios / QSSF: node_num

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** node_num
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Node count
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** QSSF uses historical job attributes; exact per-field inclusion not all verified
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData; QSSF: https://tianweiz07.github.io/Papers/21-sc.pdf

## F039 — Helios / QSSF: submit_time

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** submit_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Submission timestamp
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** QSSF uses historical job attributes; exact per-field inclusion not all verified
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData; QSSF: https://tianweiz07.github.io/Papers/21-sc.pdf

## F040 — Helios / QSSF: duration

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** duration
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Execution duration
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData

## F041 — Helios / QSSF: queue

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** queue
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Queueing delay
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData

## F042 — Helios / QSSF: state

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** state
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Final status
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData

## F043 — Philly characterization: user

- **1. Paper/system:** Philly characterization
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** user
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Hashed submitter ID
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F044 — Philly characterization: vc

- **1. Paper/system:** Philly characterization
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** vc
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Virtual cluster ID
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F045 — Philly characterization: jobid

- **1. Paper/system:** Philly characterization
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** jobid
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Opaque job identifier
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F046 — Philly characterization: submitted_time

- **1. Paper/system:** Philly characterization
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** submitted_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Submission timestamp
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F047 — Philly characterization: attempts[].detail[].gpus

- **1. Paper/system:** Philly characterization
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** attempts[].detail[].gpus
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** GPUs actually used in a scheduling attempt
- **6. Generator:** user / scheduler
- **7. When it exists:** after placement
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** NO as submission request; this is actual assignment
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F048 — Philly characterization: attempts[].detail[].ip

- **1. Paper/system:** Philly characterization
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** attempts[].detail[].ip
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Assigned machine
- **6. Generator:** user / scheduler
- **7. When it exists:** after placement
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** NO as submission request; this is actual assignment
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F049 — Philly characterization: attempts[].start_time

- **1. Paper/system:** Philly characterization
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** attempts[].start_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Start of individual attempt
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F050 — Philly characterization: attempts[].end_time

- **1. Paper/system:** Philly characterization
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** attempts[].end_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** End of individual attempt; can be missing
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F051 — Philly characterization: status

- **1. Paper/system:** Philly characterization
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** status
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Pass, Killed, Failed terminal outcome
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F052 — ATLAS / LASched: group_code

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** group_code
- **4. Example values, if documented:** Integer category codes
- **5. Meaning according to source:** Encoding of PAI Group
- **6. Generator:** researcher preprocessing
- **7. When it exists:** Fitted encoding after training-data assembly; underlying field timing inherited
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived encoded field
- **10. Outcome/runtime used in construction:** Codes need no runtime; source provenance inherited
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Encoding does not add objective information.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL on source and train-only mapping
- **15. Prior runtime-prediction use:** YES in inspected notebook
- **16. Incremental contribution isolated:** No objective-specific incremental test
- **17. Reproducible from public data:** YES notebook; completion-aware timeline needs audit
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb; PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F053 — ATLAS / LASched: workload_code

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** workload_code
- **4. Example values, if documented:** Integer category codes
- **5. Meaning according to source:** Encoding of PAI application label
- **6. Generator:** researcher preprocessing
- **7. When it exists:** Fitted encoding after training-data assembly; underlying field timing inherited
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived encoded field
- **10. Outcome/runtime used in construction:** Codes need no runtime; source provenance inherited
- **11. Primary category:** APPLICATION SEMANTICS
- **12. Classification explanation:** Encoding does not add objective information.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL on source and train-only mapping
- **15. Prior runtime-prediction use:** YES in inspected notebook
- **16. Incremental contribution isolated:** No objective-specific incremental test
- **17. Reproducible from public data:** YES notebook; completion-aware timeline needs audit
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb; PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F054 — ATLAS / LASched: user_code

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** user_code
- **4. Example values, if documented:** Integer category codes
- **5. Meaning according to source:** Encoding of submitter identity
- **6. Generator:** researcher preprocessing
- **7. When it exists:** Fitted encoding after training-data assembly; underlying field timing inherited
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived encoded field
- **10. Outcome/runtime used in construction:** Codes need no runtime; source provenance inherited
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Encoding does not add objective information.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL on source and train-only mapping
- **15. Prior runtime-prediction use:** YES in inspected notebook
- **16. Incremental contribution isolated:** No objective-specific incremental test
- **17. Reproducible from public data:** YES notebook; completion-aware timeline needs audit
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb; PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F055 — ATLAS / LASched: gpu_type_spec_code

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** gpu_type_spec_code
- **4. Example values, if documented:** Integer category codes
- **5. Meaning according to source:** Encoding of GPU request
- **6. Generator:** researcher preprocessing
- **7. When it exists:** Fitted encoding after training-data assembly; underlying field timing inherited
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived encoded field
- **10. Outcome/runtime used in construction:** Codes need no runtime; source provenance inherited
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Encoding does not add objective information.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL on source and train-only mapping
- **15. Prior runtime-prediction use:** YES in inspected notebook
- **16. Incremental contribution isolated:** No objective-specific incremental test
- **17. Reproducible from public data:** YES notebook; completion-aware timeline needs audit
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb; PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F056 — ATLAS / LASched: gro_hist_mean

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** gro_hist_mean
- **4. Example values, if documented:** Computed values
- **5. Meaning according to source:** Group historical log-duration mean
- **6. Generator:** researcher feature construction
- **7. When it exists:** After source jobs complete under a valid protocol
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived statistic
- **10. Outcome/runtime used in construction:** YES: prior runtime labels or availability of them
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Execution history is a baseline/control, not purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL: completion-aware history; submission shift alone insufficient
- **15. Prior runtime-prediction use:** YES
- **16. Incremental contribution isolated:** Feature configurations exist; no objective ablation
- **17. Reproducible from public data:** YES; audit exact timeline
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb

## F057 — ATLAS / LASched: use_hist_mean

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** use_hist_mean
- **4. Example values, if documented:** Computed values
- **5. Meaning according to source:** User historical log-duration mean
- **6. Generator:** researcher feature construction
- **7. When it exists:** After source jobs complete under a valid protocol
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived statistic
- **10. Outcome/runtime used in construction:** YES: prior runtime labels or availability of them
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Execution history is a baseline/control, not purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL: completion-aware history; submission shift alone insufficient
- **15. Prior runtime-prediction use:** YES
- **16. Incremental contribution isolated:** Feature configurations exist; no objective ablation
- **17. Reproducible from public data:** YES; audit exact timeline
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb

## F058 — ATLAS / LASched: sig_mean

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** sig_mean
- **4. Example values, if documented:** Computed values
- **5. Meaning according to source:** Mean log-duration for a configuration/resource signature
- **6. Generator:** researcher feature construction
- **7. When it exists:** After source jobs complete under a valid protocol
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived statistic
- **10. Outcome/runtime used in construction:** YES: prior runtime labels or availability of them
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Execution history is a baseline/control, not purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL: completion-aware history; submission shift alone insufficient
- **15. Prior runtime-prediction use:** YES
- **16. Incremental contribution isolated:** Feature configurations exist; no objective ablation
- **17. Reproducible from public data:** YES; audit exact timeline
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb

## F059 — ATLAS / LASched: gro_hist_count

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** gro_hist_count
- **4. Example values, if documented:** Computed values
- **5. Meaning according to source:** Count contributing to group runtime history
- **6. Generator:** researcher feature construction
- **7. When it exists:** After source jobs complete under a valid protocol
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived statistic
- **10. Outcome/runtime used in construction:** YES: prior runtime labels or availability of them
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Execution history is a baseline/control, not purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL: completion-aware history; submission shift alone insufficient
- **15. Prior runtime-prediction use:** YES
- **16. Incremental contribution isolated:** Feature configurations exist; no objective ablation
- **17. Reproducible from public data:** YES; audit exact timeline
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb

## F060 — ATLAS / LASched: num_tasks

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** num_tasks
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Number of task roles observed in a job
- **6. Generator:** user / scheduler
- **7. When it exists:** Derived from task table; planned job-submission snapshot unverified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL; not automatically planned number of trials
- **15. Prior runtime-prediction use:** YES
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb

## F061 — ATLAS / LASched: total_inst_num

- **1. Paper/system:** ATLAS / LASched
- **2. Dataset/trace:** PAI-derived ATLAS
- **3. Exact raw field or information source:** total_inst_num
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Aggregated task multiplicities
- **6. Generator:** user / scheduler
- **7. When it exists:** Derived from task table; planned job-submission snapshot unverified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL; not automatically planned number of trials
- **15. Prior runtime-prediction use:** YES
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** ATLAS: https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions/blob/main/Prediction%2BScheduling.ipynb

## F062 — MIT Supercloud dataset: model

- **1. Paper/system:** MIT Supercloud dataset
- **2. Dataset/trace:** MIT labelled_jobids.csv
- **3. Exact raw field or information source:** model
- **4. Example values, if documented:** dimenet, schnet
- **5. Meaning according to source:** Known application/model label in researcher-run workload subset.
- **6. Generator:** researcher workload labeling
- **7. When it exists:** Known application setup before run; released annotation timing unspecified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Public model string
- **10. Outcome/runtime used in construction:** No runtime-derived construction established
- **11. Primary category:** APPLICATION SEMANTICS
- **12. Classification explanation:** Model identity does not indicate per-execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL for runtime prediction; not objective
- **15. Prior runtime-prediction use:** Inspected notebook predicts model label from telemetry, not runtime
- **16. Incremental contribution isolated:** NO objective-specific experiment
- **17. Reproducible from public data:** YES model-label associations; no objective experiment
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** MIT: https://github.com/MIT-AI-Accelerator/MIT-Supercloud-Dataset; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F063 — MIT Supercloud dataset: job_type

- **1. Paper/system:** MIT Supercloud dataset
- **2. Dataset/trace:** MIT slurm-log.csv
- **3. Exact raw field or information source:** job_type
- **4. Example values, if documented:** OTHER
- **5. Meaning according to source:** Scheduler category; OTHER for all 3,430 joined labelled jobs in saved audit
- **6. Generator:** user / scheduler
- **7. When it exists:** Record snapshot; category provenance not certified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** Not certified; observed subset provides no objective variation
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** MIT: https://github.com/MIT-AI-Accelerator/MIT-Supercloud-Dataset; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F064 — MIT Supercloud dataset: id_array_task

- **1. Paper/system:** MIT Supercloud dataset
- **2. Dataset/trace:** MIT slurm-log.csv
- **3. Exact raw field or information source:** id_array_task
- **4. Example values, if documented:** 4294967294 sentinel in labelled subset
- **5. Meaning according to source:** Array task index; not planned number of trials
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** Only after sentinel/array semantics checked
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** MIT: https://github.com/MIT-AI-Accelerator/MIT-Supercloud-Dataset; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F065 — MIT Supercloud dataset: id_array_job

- **1. Paper/system:** MIT Supercloud dataset
- **2. Dataset/trace:** MIT slurm-log.csv
- **3. Exact raw field or information source:** id_array_job
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Anonymized array-job identifier, not experiment purpose
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Anonymized ID
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** MIT: https://github.com/MIT-AI-Accelerator/MIT-Supercloud-Dataset; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F066 — MIT Supercloud dataset: timelimit

- **1. Paper/system:** MIT Supercloud dataset
- **2. Dataset/trace:** MIT slurm-log.csv
- **3. Exact raw field or information source:** timelimit
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Scheduler walltime cap, not epochs or intended training work
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL on encoding and request provenance
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** MIT: https://github.com/MIT-AI-Accelerator/MIT-Supercloud-Dataset; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F067 — NAS-Bench-101: epochs (record budget); config[train_epochs] in evaluator

- **1. Paper/system:** NAS-Bench-101
- **2. Dataset/trace:** NAS-Bench-101 full TFRecord
- **3. Exact raw field or information source:** epochs (record budget); config[train_epochs] in evaluator
- **4. Example values, if documented:** 4, 12, 36, 108 documented; local prefix observed 4 only
- **5. Meaning according to source:** Preconfigured training epoch budget.
- **6. Generator:** researcher experimental design / framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Public budget value
- **10. Outcome/runtime used in construction:** NO: budget controls training
- **11. Primary category:** PLANNED SCOPE
- **12. Classification explanation:** Explicit amount of training selected before execution, not observed progress or objective.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for budget-conditioned benchmark runtime prediction
- **15. Prior runtime-prediction use:** Runtime exposed for NAS cost accounting; runtime-regression use not established
- **16. Incremental contribution isolated:** No objective contribution isolated
- **17. Reproducible from public data:** YES scope-runtime analysis; NAS-Bench-101 timings are TPU, not GPU
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** NAS: https://github.com/google-research/nasbench/blob/master/nasbench/api.py; NASE: https://github.com/google-research/nasbench/blob/master/nasbench/lib/evaluate.py; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F068 — NAS-Bench-101: module_adjacency

- **1. Paper/system:** NAS-Bench-101
- **2. Dataset/trace:** NAS-Bench-101
- **3. Exact raw field or information source:** module_adjacency
- **4. Example values, if documented:** conv3x3-bn-relu; maxpool3x3 (operations)
- **5. Meaning according to source:** Architecture graph
- **6. Generator:** researcher
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Architecture specification does not encode run purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** NAS: https://github.com/google-research/nasbench/blob/master/nasbench/api.py

## F069 — NAS-Bench-101: module_operations

- **1. Paper/system:** NAS-Bench-101
- **2. Dataset/trace:** NAS-Bench-101
- **3. Exact raw field or information source:** module_operations
- **4. Example values, if documented:** conv3x3-bn-relu; maxpool3x3 (operations)
- **5. Meaning according to source:** Architecture operation choices
- **6. Generator:** researcher
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Architecture specification does not encode run purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** NAS: https://github.com/google-research/nasbench/blob/master/nasbench/api.py

## F070 — NAS-Bench-101: final_training_time

- **1. Paper/system:** NAS-Bench-101
- **2. Dataset/trace:** NAS-Bench-101
- **3. Exact raw field or information source:** final_training_time
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Measured cumulative training time on benchmark hardware
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** NAS: https://github.com/google-research/nasbench/blob/master/nasbench/api.py

## F071 — NATS-Bench: --hyper / hp training-budget setting

- **1. Paper/system:** NATS-Bench
- **2. Dataset/trace:** Topology benchmark
- **3. Exact raw field or information source:** --hyper / hp training-budget setting
- **4. Example values, if documented:** 12, 200 verified in topology launcher
- **5. Meaning according to source:** Selected training schedule/epoch budget before launch.
- **6. Generator:** researcher/framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Budget key and training recipe
- **10. Outcome/runtime used in construction:** NO for budget; released timing processing needs separate audit
- **11. Primary category:** PLANNED SCOPE
- **12. Classification explanation:** Explicit run budget; not user purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as scope input
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Scope study possible; inspected collector rewrites timing via reset_pseudo_train_times, so independent empirical timing validation not certified
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** NATST: https://github.com/D-X-Y/AutoDL-Projects/blob/main/scripts/NATS-Bench/train-topology.sh; NATS: https://github.com/D-X-Y/AutoDL-Projects/blob/main/exps/NATS-Bench/tss-collect.py

## F072 — NATS-Bench: iepoch

- **1. Paper/system:** NATS-Bench
- **2. Dataset/trace:** NATS-Bench API
- **3. Exact raw field or information source:** iepoch
- **4. Example values, if documented:** Epoch index
- **5. Meaning according to source:** Query-time selection of a learning-curve position.
- **6. Generator:** researcher querying completed trajectory
- **7. When it exists:** after execution (query)
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Uses recorded trajectory position
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** A queried intermediate epoch is not proof that a separate run was prospectively assigned that budget.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** NO as evidence of independently launched planned budget
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** NATS: https://github.com/D-X-Y/AutoDL-Projects/blob/main/exps/NATS-Bench/tss-collect.py

## F073 — NATS-Bench: train_times

- **1. Paper/system:** NATS-Bench
- **2. Dataset/trace:** Processed topology release
- **3. Exact raw field or information source:** train_times
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Timing data; inspected collector resets pseudo-times using averaged/scaled timings
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** NATS: https://github.com/D-X-Y/AutoDL-Projects/blob/main/exps/NATS-Bench/tss-collect.py

## F074 — LCBench / Auto-PyTorch: Fixed 50-epoch run protocol

- **1. Paper/system:** LCBench / Auto-PyTorch
- **2. Dataset/trace:** LCBench
- **3. Exact raw field or information source:** Fixed 50-epoch run protocol
- **4. Example values, if documented:** 50 epochs
- **5. Meaning according to source:** All configurations documented as evaluated over 50 epochs.
- **6. Generator:** researcher/framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Documented protocol constant
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** PLANNED SCOPE
- **12. Classification explanation:** Prospective fixed budget, but no between-run budget variation in this documented design.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES constant; cannot identify incremental budget effect
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** NO varying planned-budget experiment from fixed protocol alone
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** LC: https://github.com/automl/LCBench

## F075 — LCBench / Auto-PyTorch: Per-epoch log position

- **1. Paper/system:** LCBench / Auto-PyTorch
- **2. Dataset/trace:** LCBench
- **3. Exact raw field or information source:** Per-epoch log position
- **4. Example values, if documented:** 1..50 trajectory positions
- **5. Meaning according to source:** Repeated measurements along a fixed-budget run.
- **6. Generator:** framework logger
- **7. When it exists:** after launch
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Recorded execution progress
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Progress observations do not establish independently assigned stopping budgets.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** NO as independent planned-budget label
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** LC: https://github.com/automl/LCBench

## F076 — LCBench / Auto-PyTorch: Batch size (documented configuration item; exact serialized key not verified)

- **1. Paper/system:** LCBench / Auto-PyTorch
- **2. Dataset/trace:** LCBench
- **3. Exact raw field or information source:** Batch size (documented configuration item; exact serialized key not verified)
- **4. Example values, if documented:** See documented sampled ranges
- **5. Meaning according to source:** Architecture/optimization configuration sampled before run.
- **6. Generator:** researcher/framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Configuration value, not reason for execution or total work budget.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as configuration control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public data documented; serialized keys not inspected
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** LC: https://github.com/automl/LCBench

## F077 — LCBench / Auto-PyTorch: Learning rate (documented configuration item; exact serialized key not verified)

- **1. Paper/system:** LCBench / Auto-PyTorch
- **2. Dataset/trace:** LCBench
- **3. Exact raw field or information source:** Learning rate (documented configuration item; exact serialized key not verified)
- **4. Example values, if documented:** See documented sampled ranges
- **5. Meaning according to source:** Architecture/optimization configuration sampled before run.
- **6. Generator:** researcher/framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Configuration value, not reason for execution or total work budget.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as configuration control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public data documented; serialized keys not inspected
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** LC: https://github.com/automl/LCBench

## F078 — LCBench / Auto-PyTorch: Momentum (documented configuration item; exact serialized key not verified)

- **1. Paper/system:** LCBench / Auto-PyTorch
- **2. Dataset/trace:** LCBench
- **3. Exact raw field or information source:** Momentum (documented configuration item; exact serialized key not verified)
- **4. Example values, if documented:** See documented sampled ranges
- **5. Meaning according to source:** Architecture/optimization configuration sampled before run.
- **6. Generator:** researcher/framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Configuration value, not reason for execution or total work budget.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as configuration control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public data documented; serialized keys not inspected
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** LC: https://github.com/automl/LCBench

## F079 — LCBench / Auto-PyTorch: Weight decay (documented configuration item; exact serialized key not verified)

- **1. Paper/system:** LCBench / Auto-PyTorch
- **2. Dataset/trace:** LCBench
- **3. Exact raw field or information source:** Weight decay (documented configuration item; exact serialized key not verified)
- **4. Example values, if documented:** See documented sampled ranges
- **5. Meaning according to source:** Architecture/optimization configuration sampled before run.
- **6. Generator:** researcher/framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Configuration value, not reason for execution or total work budget.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as configuration control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public data documented; serialized keys not inspected
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** LC: https://github.com/automl/LCBench

## F080 — LCBench / Auto-PyTorch: Number of layers (documented configuration item; exact serialized key not verified)

- **1. Paper/system:** LCBench / Auto-PyTorch
- **2. Dataset/trace:** LCBench
- **3. Exact raw field or information source:** Number of layers (documented configuration item; exact serialized key not verified)
- **4. Example values, if documented:** See documented sampled ranges
- **5. Meaning according to source:** Architecture/optimization configuration sampled before run.
- **6. Generator:** researcher/framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Configuration value, not reason for execution or total work budget.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as configuration control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public data documented; serialized keys not inspected
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** LC: https://github.com/automl/LCBench

## F081 — LCBench / Auto-PyTorch: Maximum number of units per layer (documented configuration item; exact serialized key not verified)

- **1. Paper/system:** LCBench / Auto-PyTorch
- **2. Dataset/trace:** LCBench
- **3. Exact raw field or information source:** Maximum number of units per layer (documented configuration item; exact serialized key not verified)
- **4. Example values, if documented:** See documented sampled ranges
- **5. Meaning according to source:** Architecture/optimization configuration sampled before run.
- **6. Generator:** researcher/framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Configuration value, not reason for execution or total work budget.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as configuration control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public data documented; serialized keys not inspected
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** LC: https://github.com/automl/LCBench

## F082 — LCBench / Auto-PyTorch: Dropout (documented configuration item; exact serialized key not verified)

- **1. Paper/system:** LCBench / Auto-PyTorch
- **2. Dataset/trace:** LCBench
- **3. Exact raw field or information source:** Dropout (documented configuration item; exact serialized key not verified)
- **4. Example values, if documented:** See documented sampled ranges
- **5. Meaning according to source:** Architecture/optimization configuration sampled before run.
- **6. Generator:** researcher/framework
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** NO
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Configuration value, not reason for execution or total work budget.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as configuration control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public data documented; serialized keys not inspected
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** LC: https://github.com/automl/LCBench

## F083 — Alibaba GenTD26: num_inference_steps

- **1. Paper/system:** Alibaba GenTD26
- **2. Dataset/trace:** lora_request_trace.csv
- **3. Exact raw field or information source:** num_inference_steps
- **4. Example values, if documented:** 30, 40
- **5. Meaning according to source:** Diffusion step count
- **6. Generator:** user/API/framework; exact logger provenance not exposed
- **7. When it exists:** Normally request configuration; released snapshot not proven immutable
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Public numeric request field
- **10. Outcome/runtime used in construction:** No outcome dependence described; requested-vs-realized needs confirmation
- **11. Primary category:** PLANNED SCOPE
- **12. Classification explanation:** Request workload amount, not why user performs inference.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL: verify planned request value rather than realized work
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES associations with exec_time_seconds; strict prospective scope certification incomplete
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** GENAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI

## F084 — Alibaba GenTD26: num_images_per_prompt

- **1. Paper/system:** Alibaba GenTD26
- **2. Dataset/trace:** lora_request_trace.csv
- **3. Exact raw field or information source:** num_images_per_prompt
- **4. Example values, if documented:** 1
- **5. Meaning according to source:** Images per request
- **6. Generator:** user/API/framework; exact logger provenance not exposed
- **7. When it exists:** Normally request configuration; released snapshot not proven immutable
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Public numeric request field
- **10. Outcome/runtime used in construction:** No outcome dependence described; requested-vs-realized needs confirmation
- **11. Primary category:** PLANNED SCOPE
- **12. Classification explanation:** Request workload amount, not why user performs inference.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL: verify planned request value rather than realized work
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES associations with exec_time_seconds; strict prospective scope certification incomplete
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** GENAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI

## F085 — Alibaba GenTD26: predict_type

- **1. Paper/system:** Alibaba GenTD26
- **2. Dataset/trace:** lora_request_trace.csv
- **3. Exact raw field or information source:** predict_type
- **4. Example values, if documented:** TXT_2_IMG, IMG_2_IMG, INPAINTING
- **5. Meaning according to source:** Generation operation chosen by request.
- **6. Generator:** API/framework
- **7. When it exists:** request specification; versioning unknown
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** No outcome dependence indicated
- **11. Primary category:** APPLICATION SEMANTICS
- **12. Classification explanation:** Operation identity; does not distinguish debugging, evaluation or production use of that operation.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL as request operation control
- **15. Prior runtime-prediction use:** Not established
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** GENAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI

## F086 — Alibaba GenTD26: checkpoint_model_version_id

- **1. Paper/system:** Alibaba GenTD26
- **2. Dataset/trace:** lora_request_trace.csv
- **3. Exact raw field or information source:** checkpoint_model_version_id
- **4. Example values, if documented:** M0000 / numeric values
- **5. Meaning according to source:** Anonymized base-model identity; not resume/checkpoint-evaluation purpose
- **6. Generator:** user/API inputs; logger-derived representation
- **7. When it exists:** Request inputs exist before execution; logged snapshot unspecified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** No duration dependence described
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Describes configured model/input; does not measure execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL as control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** GENAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI

## F087 — Alibaba GenTD26: num_lora

- **1. Paper/system:** Alibaba GenTD26
- **2. Dataset/trace:** lora_request_trace.csv
- **3. Exact raw field or information source:** num_lora
- **4. Example values, if documented:** M0000 / numeric values
- **5. Meaning according to source:** Adapter count/configuration
- **6. Generator:** user/API inputs; logger-derived representation
- **7. When it exists:** Request inputs exist before execution; logged snapshot unspecified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** No duration dependence described
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Describes configured model/input; does not measure execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL as control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** GENAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI

## F088 — Alibaba GenTD26: prompt_length

- **1. Paper/system:** Alibaba GenTD26
- **2. Dataset/trace:** lora_request_trace.csv
- **3. Exact raw field or information source:** prompt_length
- **4. Example values, if documented:** M0000 / numeric values
- **5. Meaning according to source:** Input text length, not purpose or prompt meaning
- **6. Generator:** user/API inputs; logger-derived representation
- **7. When it exists:** Request inputs exist before execution; logged snapshot unspecified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** No duration dependence described
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Describes configured model/input; does not measure execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL as control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** GENAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI

## F089 — Alibaba GenTD26: negative_prompt_length

- **1. Paper/system:** Alibaba GenTD26
- **2. Dataset/trace:** lora_request_trace.csv
- **3. Exact raw field or information source:** negative_prompt_length
- **4. Example values, if documented:** M0000 / numeric values
- **5. Meaning according to source:** Negative text prompt length
- **6. Generator:** user/API inputs; logger-derived representation
- **7. When it exists:** Request inputs exist before execution; logged snapshot unspecified
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** No duration dependence described
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** Describes configured model/input; does not measure execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL as control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** GENAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI

## F090 — Alibaba GenTD26: groupId

- **1. Paper/system:** Alibaba GenTD26
- **2. Dataset/trace:** lora_request_trace.csv
- **3. Exact raw field or information source:** groupId
- **4. Example values, if documented:** G0000
- **5. Meaning according to source:** Anonymized user/group identity
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** GENAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI

## F091 — Alibaba GenTD26: exec_time_seconds

- **1. Paper/system:** Alibaba GenTD26
- **2. Dataset/trace:** lora_request_trace.csv
- **3. Exact raw field or information source:** exec_time_seconds
- **4. Example values, if documented:** 32.0
- **5. Meaning according to source:** Request execution time
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** GENAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI

## F092 — Alibaba ASI characterization: job_type_public

- **1. Paper/system:** Alibaba ASI characterization
- **2. Dataset/trace:** GPU v2026
- **3. Exact raw field or information source:** job_type_public
- **4. Example values, if documented:** training, online_inference, offline_inference, dev, other, unknown
- **5. Meaning according to source:** Broad workload activity bucket; dev includes notebooks/IDE sessions.
- **6. Generator:** public bucketing pipeline; source label generator unknown
- **7. When it exists:** Hourly/summary release; prospective availability unknown
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived public bucket
- **10. Outcome/runtime used in construction:** UNKNOWN
- **11. Primary category:** OBJECTIVE-ADJACENT
- **12. Classification explanation:** Activity mode relates to execution purpose but does not measure user reason; classification construction and timing unverified.
- **13. Relationship to latent experimental objective:** plausible proxy
- **14. Prospective runtime-prediction admissibility:** NOT CERTIFIED; cannot treat hourly state as submission snapshot
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Descriptive associations possible; prospective objective test NO
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** A26: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2026/docs/schema.md

## F093 — Alibaba ASI characterization: model_type_public

- **1. Paper/system:** Alibaba ASI characterization
- **2. Dataset/trace:** GPU v2026
- **3. Exact raw field or information source:** model_type_public
- **4. Example values, if documented:** genai, rec, cv, embedding, dev, unknown
- **5. Meaning according to source:** Public model-family bucket.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived bucket
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** APPLICATION SEMANTICS
- **12. Classification explanation:** Model family is not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** Not certified prospective
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** A26: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2026/docs/schema.md

## F094 — Alibaba ASI characterization: is_genai_request

- **1. Paper/system:** Alibaba ASI characterization
- **2. Dataset/trace:** GPU v2026
- **3. Exact raw field or information source:** is_genai_request
- **4. Example values, if documented:** true / false
- **5. Meaning according to source:** Membership in public GenAI detection rules.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Derived boolean
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** APPLICATION SEMANTICS
- **12. Classification explanation:** Application-family detector, not objective.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** Not certified prospective
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** A26: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2026/docs/schema.md

## F095 — Alibaba ASI characterization: workload_id

- **1. Paper/system:** Alibaba ASI characterization
- **2. Dataset/trace:** GPU v2026
- **3. Exact raw field or information source:** workload_id
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Anonymized owner/workload identity shared by pods
- **6. Generator:** user / scheduler
- **7. When it exists:** Hourly snapshot; source availability unknown
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** Not certified as submission descriptor
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** A26: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2026/docs/schema.md

## F096 — Alibaba ASI characterization: priority_class

- **1. Paper/system:** Alibaba ASI characterization
- **2. Dataset/trace:** GPU v2026
- **3. Exact raw field or information source:** priority_class
- **4. Example values, if documented:** HP, LP, Other
- **5. Meaning according to source:** HP/LP resource-priority class
- **6. Generator:** user / scheduler
- **7. When it exists:** Hourly snapshot; original priority may exist at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL on original request
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** A26: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2026/docs/schema.md

## F097 — Alibaba ASI characterization: duration_hours

- **1. Paper/system:** Alibaba ASI characterization
- **2. Dataset/trace:** GPU v2026
- **3. Exact raw field or information source:** duration_hours
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Execution span derived from observed samples, not guaranteed exact job runtime
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** A26: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2026/docs/schema.md

## F098 — Alibaba fragmentation trace: name

- **1. Paper/system:** Alibaba fragmentation trace
- **2. Dataset/trace:** GPU v2023
- **3. Exact raw field or information source:** name
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Pod identifier
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** A23: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2023/csv/openb_pod_list_default.csv

## F099 — Alibaba fragmentation trace: qos

- **1. Paper/system:** Alibaba fragmentation trace
- **2. Dataset/trace:** GPU v2023
- **3. Exact raw field or information source:** qos
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Resource-service class
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** A23: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2023/csv/openb_pod_list_default.csv

## F100 — Alibaba fragmentation trace: num_gpu

- **1. Paper/system:** Alibaba fragmentation trace
- **2. Dataset/trace:** GPU v2023
- **3. Exact raw field or information source:** num_gpu
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** GPU request count
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** A23: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2023/csv/openb_pod_list_default.csv

## F101 — Alibaba fragmentation trace: gpu_spec

- **1. Paper/system:** Alibaba fragmentation trace
- **2. Dataset/trace:** GPU v2023
- **3. Exact raw field or information source:** gpu_spec
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** GPU specification
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** A23: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2023/csv/openb_pod_list_default.csv

## F102 — Alibaba fragmentation trace: pod_phase

- **1. Paper/system:** Alibaba fragmentation trace
- **2. Dataset/trace:** GPU v2023
- **3. Exact raw field or information source:** pod_phase
- **4. Example values, if documented:** Not supplied
- **5. Meaning according to source:** Observed pod phase
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** A23: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2023/csv/openb_pod_list_default.csv

## F103 — Alibaba DLRM disaggregation: role

- **1. Paper/system:** Alibaba DLRM disaggregation
- **2. Dataset/trace:** GPU v2025
- **3. Exact raw field or information source:** role
- **4. Example values, if documented:** HN observed
- **5. Meaning according to source:** Serving component role; exact role semantics not established in recovered field evidence.
- **6. Generator:** framework/platform
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Do not infer user objective from an undecomposed serving-component role.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Not certified
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** A25: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2025/disaggregated_DLRM_trace.csv; LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F104 — Alibaba DLRM disaggregation: app_name

- **1. Paper/system:** Alibaba DLRM disaggregation
- **2. Dataset/trace:** GPU v2025
- **3. Exact raw field or information source:** app_name
- **4. Example values, if documented:** app_0
- **5. Meaning according to source:** Anonymized serving application identity.
- **6. Generator:** platform; release anonymization
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Anonymized ID
- **10. Outcome/runtime used in construction:** No outcome dependence established
- **11. Primary category:** APPLICATION SEMANTICS
- **12. Classification explanation:** Identity of service, not purpose of this execution.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** CONDITIONAL as application control
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** A25: https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2025/disaggregated_DLRM_trace.csv

## F105 — GFS spot trace: job_type

- **1. Paper/system:** GFS spot trace
- **2. Dataset/trace:** GPU v2026 spot
- **3. Exact raw field or information source:** job_type
- **4. Example values, if documented:** HP / Spot
- **5. Meaning according to source:** Priority/spot class, NOT training purpose
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** SPOT: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-spot-gpu

## F106 — GFS spot trace: organization

- **1. Paper/system:** GFS spot trace
- **2. Dataset/trace:** GPU v2026 spot
- **3. Exact raw field or information source:** organization
- **4. Example values, if documented:** Numeric
- **5. Meaning according to source:** Administrative organization identifier
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** SPOT: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-spot-gpu

## F107 — GFS spot trace: worker_num

- **1. Paper/system:** GFS spot trace
- **2. Dataset/trace:** GPU v2026 spot
- **3. Exact raw field or information source:** worker_num
- **4. Example values, if documented:** Numeric
- **5. Meaning according to source:** Requested worker count; not number of trials
- **6. Generator:** user / scheduler
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released scalar/category
- **10. Outcome/runtime used in construction:** No target dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Describes identity, timing, or resources, not execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES for documented submission value; preserve time ordering
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** SPOT: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-spot-gpu

## F108 — ORA: EVIDENCE GAP — exact candidate field not established

- **1. Paper/system:** ORA
- **2. Dataset/trace:** Exact release not established in recovered evidence
- **3. Exact raw field or information source:** EVIDENCE GAP — exact candidate field not established
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** No inspectable field-level provenance recovered in this task.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** UNKNOWN
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** A source name is not evidence of a released prospective field.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F109 — F-DATA: EVIDENCE GAP — exact candidate field not established

- **1. Paper/system:** F-DATA
- **2. Dataset/trace:** Exact release not established in recovered evidence
- **3. Exact raw field or information source:** EVIDENCE GAP — exact candidate field not established
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** No inspectable field-level provenance recovered in this task.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** UNKNOWN
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** A source name is not evidence of a released prospective field.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F110 — PREP: EVIDENCE GAP — exact candidate field not established

- **1. Paper/system:** PREP
- **2. Dataset/trace:** Exact release not established in recovered evidence
- **3. Exact raw field or information source:** EVIDENCE GAP — exact candidate field not established
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** No inspectable field-level provenance recovered in this task.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** UNKNOWN
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** A source name is not evidence of a released prospective field.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F111 — Park & Hong: EVIDENCE GAP — exact candidate field not established

- **1. Paper/system:** Park & Hong
- **2. Dataset/trace:** Exact release not established in recovered evidence
- **3. Exact raw field or information source:** EVIDENCE GAP — exact candidate field not established
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** No inspectable field-level provenance recovered in this task.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** UNKNOWN
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** A source name is not evidence of a released prospective field.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F112 — Workflow datasets (unspecified): EVIDENCE GAP — exact candidate field not established

- **1. Paper/system:** Workflow datasets (unspecified)
- **2. Dataset/trace:** Exact release not established in recovered evidence
- **3. Exact raw field or information source:** EVIDENCE GAP — exact candidate field not established
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** No inspectable field-level provenance recovered in this task.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** UNKNOWN
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** A source name is not evidence of a released prospective field.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F113 — HPOBench (repository inventory only): EVIDENCE GAP — exact candidate field not established

- **1. Paper/system:** HPOBench (repository inventory only)
- **2. Dataset/trace:** Exact release not established in recovered evidence
- **3. Exact raw field or information source:** EVIDENCE GAP — exact candidate field not established
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** No inspectable field-level provenance recovered in this task.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** UNKNOWN
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** A source name is not evidence of a released prospective field.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F114 — MLPerf (partial configuration evidence only): EVIDENCE GAP — exact candidate field not established

- **1. Paper/system:** MLPerf (partial configuration evidence only)
- **2. Dataset/trace:** Exact release not established in recovered evidence
- **3. Exact raw field or information source:** EVIDENCE GAP — exact candidate field not established
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** No inspectable field-level provenance recovered in this task.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** UNKNOWN
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** A source name is not evidence of a released prospective field.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** LOCAL: research-audit-2026-09-22/coverage.json; pai-eligible-coverage.json; README.md; source-manifest.json

## F115 — SchedMate / Mars: User prompt (information source, not verified raw column)

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Exact public release not established
- **3. Exact raw field or information source:** User prompt (information source, not verified raw column)
- **4. Example values, if documented:** Not documented in recovered primary evidence
- **5. Meaning according to source:** Local summary lists prompt input; no actual prompt strings or labels recovered
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot identify extracted objective, scope, or application fields from a high-level local summary.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN; logs/metrics require separate time audit
- **15. Prior runtime-prediction use:** Local summary claims runtime estimation; primary evidence unavailable
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F116 — SchedMate / Mars: Source code (information source, not verified raw column)

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Exact public release not established
- **3. Exact raw field or information source:** Source code (information source, not verified raw column)
- **4. Example values, if documented:** Not documented in recovered primary evidence
- **5. Meaning according to source:** Local summary lists code input; exact extractor schema unavailable
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot identify extracted objective, scope, or application fields from a high-level local summary.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN; logs/metrics require separate time audit
- **15. Prior runtime-prediction use:** Local summary claims runtime estimation; primary evidence unavailable
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F117 — SchedMate / Mars: Runtime logs (information source, not verified raw column)

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Exact public release not established
- **3. Exact raw field or information source:** Runtime logs (information source, not verified raw column)
- **4. Example values, if documented:** Not documented in recovered primary evidence
- **5. Meaning according to source:** Local summary lists runtime logs
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot identify extracted objective, scope, or application fields from a high-level local summary.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN; logs/metrics require separate time audit
- **15. Prior runtime-prediction use:** Local summary claims runtime estimation; primary evidence unavailable
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F118 — SchedMate / Mars: Historical jobs (information source, not verified raw column)

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Exact public release not established
- **3. Exact raw field or information source:** Historical jobs (information source, not verified raw column)
- **4. Example values, if documented:** Not documented in recovered primary evidence
- **5. Meaning according to source:** Local summary lists historical information
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot identify extracted objective, scope, or application fields from a high-level local summary.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN; logs/metrics require separate time audit
- **15. Prior runtime-prediction use:** Local summary claims runtime estimation; primary evidence unavailable
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F119 — SchedMate / Mars: Hardware metrics (information source, not verified raw column)

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Exact public release not established
- **3. Exact raw field or information source:** Hardware metrics (information source, not verified raw column)
- **4. Example values, if documented:** Not documented in recovered primary evidence
- **5. Meaning according to source:** Local summary lists hardware metrics
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot identify extracted objective, scope, or application fields from a high-level local summary.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN; logs/metrics require separate time audit
- **15. Prior runtime-prediction use:** Local summary claims runtime estimation; primary evidence unavailable
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F120 — SchedMate / Mars: UNVERIFIED EXTRACTION COMPONENT — model identity

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Extractor schema not recovered
- **3. Exact raw field or information source:** UNVERIFIED EXTRACTION COMPONENT — model identity
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Requested decomposition slot; NOT an assertion that the paper extracts this item.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot invent exact keys or extracted features. If verified, model/dataset identity is application/configuration; steps/epochs are scope; purpose requires explicit evidence.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F121 — SchedMate / Mars: UNVERIFIED EXTRACTION COMPONENT — dataset identity

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Extractor schema not recovered
- **3. Exact raw field or information source:** UNVERIFIED EXTRACTION COMPONENT — dataset identity
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Requested decomposition slot; NOT an assertion that the paper extracts this item.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot invent exact keys or extracted features. If verified, model/dataset identity is application/configuration; steps/epochs are scope; purpose requires explicit evidence.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F122 — SchedMate / Mars: UNVERIFIED EXTRACTION COMPONENT — training steps

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Extractor schema not recovered
- **3. Exact raw field or information source:** UNVERIFIED EXTRACTION COMPONENT — training steps
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Requested decomposition slot; NOT an assertion that the paper extracts this item.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot invent exact keys or extracted features. If verified, model/dataset identity is application/configuration; steps/epochs are scope; purpose requires explicit evidence.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F123 — SchedMate / Mars: UNVERIFIED EXTRACTION COMPONENT — task / execution-purpose text

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Extractor schema not recovered
- **3. Exact raw field or information source:** UNVERIFIED EXTRACTION COMPONENT — task / execution-purpose text
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Requested decomposition slot; NOT an assertion that the paper extracts this item.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot invent exact keys or extracted features. If verified, model/dataset identity is application/configuration; steps/epochs are scope; purpose requires explicit evidence.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F124 — SchedMate / Mars: UNVERIFIED EXTRACTION COMPONENT — hardware requirements

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Extractor schema not recovered
- **3. Exact raw field or information source:** UNVERIFIED EXTRACTION COMPONENT — hardware requirements
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Requested decomposition slot; NOT an assertion that the paper extracts this item.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot invent exact keys or extracted features. If verified, model/dataset identity is application/configuration; steps/epochs are scope; purpose requires explicit evidence.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F125 — SchedMate / Mars: UNVERIFIED EXTRACTION COMPONENT — epochs / trial count

- **1. Paper/system:** SchedMate / Mars
- **2. Dataset/trace:** Extractor schema not recovered
- **3. Exact raw field or information source:** UNVERIFIED EXTRACTION COMPONENT — epochs / trial count
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Requested decomposition slot; NOT an assertion that the paper extracts this item.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Cannot invent exact keys or extracted features. If verified, model/dataset identity is application/configuration; steps/epochs are scope; purpose requires explicit evidence.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** UNKNOWN
- **15. Prior runtime-prediction use:** UNKNOWN
- **16. Incremental contribution isolated:** UNKNOWN
- **17. Reproducible from public data:** UNKNOWN
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** SCHED: LiteratureReview/PaperInsights/SchedMate.md (local summary only; not a verified extraction schema)

## F126 — Menear et al., PEARC 2023: User-provided requested wallclock (exact raw column not recovered)

- **1. Paper/system:** Menear et al., PEARC 2023
- **2. Dataset/trace:** Eagle
- **3. Exact raw field or information source:** User-provided requested wallclock (exact raw column not recovered)
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Time-limit estimate supplied for scheduling.
- **6. Generator:** user
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** Dataset released; exact field mapping not recovered
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Not current-job outcome; user estimate
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** Requested walltime is a runtime estimate/cap, not epoch budget or execution purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as documented pre-submit estimate
- **15. Prior runtime-prediction use:** YES: runtime-prediction study
- **16. Incremental contribution isolated:** Exact field ablation not established
- **17. Reproducible from public data:** Dataset/code published; exact experiment not checked
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** EAGLE: https://docs.nlr.gov/docs/fy23osti/86526.pdf

## F127 — Menear et al., PEARC 2023: User (feature label; exact raw column not recovered)

- **1. Paper/system:** Menear et al., PEARC 2023
- **2. Dataset/trace:** Eagle
- **3. Exact raw field or information source:** User (feature label; exact raw column not recovered)
- **4. Example values, if documented:** User identity
- **5. Meaning according to source:** Submitter categorical feature.
- **6. Generator:** scheduler/user account
- **7. When it exists:** at submission
- **8. Publicly available in released dataset:** Dataset published; mapping not recovered
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** No current-job outcome dependence indicated
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** User identity is not purpose.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES with valid encoding
- **15. Prior runtime-prediction use:** YES; feature-set analysis
- **16. Incremental contribution isolated:** Feature-set comparison, not objective isolation
- **17. Reproducible from public data:** Field analysis possible; exact prior experiment not established
- **18. Final usability for original hypothesis:** CONTROL ONLY
- **Evidence:** EAGLE: https://docs.nlr.gov/docs/fy23osti/86526.pdf

## F128 — Helios / QSSF: ABSENCE CHECK — explicit objective / epochs / max_steps / trial budget

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** ABSENCE CHECK — explicit objective / epochs / max_steps / trial budget
- **4. Example values, if documented:** No such released raw column established
- **5. Meaning according to source:** Inspected schemas do not expose verified per-execution purpose or these planned-scope fields.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** NO in inspected schemas
- **9. Raw or derived/anonymized:** Absent
- **10. Outcome/runtime used in construction:** Not applicable
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Absence of named observables in audited schemas; do not infer values from IDs or durations.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** NO
- **15. Prior runtime-prediction use:** Not applicable
- **16. Incremental contribution isolated:** NO
- **17. Reproducible from public data:** NO for these variables
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** HELIOS: https://github.com/S-Lab-System-Group/HeliosData

## F129 — Philly: ABSENCE CHECK — explicit objective / epochs / max_steps / trial budget

- **1. Paper/system:** Philly
- **2. Dataset/trace:** Philly
- **3. Exact raw field or information source:** ABSENCE CHECK — explicit objective / epochs / max_steps / trial budget
- **4. Example values, if documented:** No such released raw column established
- **5. Meaning according to source:** Inspected schemas do not expose verified per-execution purpose or these planned-scope fields.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** NO in inspected schemas
- **9. Raw or derived/anonymized:** Absent
- **10. Outcome/runtime used in construction:** Not applicable
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Absence of named observables in audited schemas; do not infer values from IDs or durations.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** NO
- **15. Prior runtime-prediction use:** Not applicable
- **16. Incremental contribution isolated:** NO
- **17. Reproducible from public data:** NO for these variables
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PHILLY: https://github.com/msr-fiddle/philly-traces

## F130 — PAI: ABSENCE CHECK — explicit objective / epochs / max_steps / trial budget

- **1. Paper/system:** PAI
- **2. Dataset/trace:** PAI 2020
- **3. Exact raw field or information source:** ABSENCE CHECK — explicit objective / epochs / max_steps / trial budget
- **4. Example values, if documented:** No such released raw column established
- **5. Meaning according to source:** Inspected schemas do not expose verified per-execution purpose or these planned-scope fields.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** NO in inspected schemas
- **9. Raw or derived/anonymized:** Absent
- **10. Outcome/runtime used in construction:** Not applicable
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Absence of named observables in audited schemas; do not infer values from IDs or durations.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** NO
- **15. Prior runtime-prediction use:** Not applicable
- **16. Incremental contribution isolated:** NO
- **17. Reproducible from public data:** NO for these variables
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** PAI: https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020

## F131 — Acme: ABSENCE CHECK — explicit objective / epochs / max_steps / trial budget

- **1. Paper/system:** Acme
- **2. Dataset/trace:** AcmeTrace
- **3. Exact raw field or information source:** ABSENCE CHECK — explicit objective / epochs / max_steps / trial budget
- **4. Example values, if documented:** No such released raw column established
- **5. Meaning according to source:** Inspected schemas do not expose verified per-execution purpose or these planned-scope fields.
- **6. Generator:** unknown
- **7. When it exists:** unknown
- **8. Publicly available in released dataset:** NO in inspected schemas
- **9. Raw or derived/anonymized:** Absent
- **10. Outcome/runtime used in construction:** Not applicable
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Absence of named observables in audited schemas; do not infer values from IDs or durations.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** NO
- **15. Prior runtime-prediction use:** Not applicable
- **16. Incremental contribution isolated:** NO
- **17. Reproducible from public data:** NO for these variables
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** ACME: https://github.com/InternLM/AcmeTrace/blob/master/README.md; AUTHOR: User-supplied author clarification in current request: type uses job-name hints AND duration; raw/sanitized names cannot be released. No independent correspondence inspected.

## F132 — Helios / QSSF: Original job-name information (withheld)

- **1. Paper/system:** Helios / QSSF
- **2. Dataset/trace:** Helios
- **3. Exact raw field or information source:** Original job-name information (withheld)
- **4. Example values, if documented:** Unavailable
- **5. Meaning according to source:** Private job-name predictor input; artifact explicitly withholds Helios estimator/QSSF components because names are not released.
- **6. Generator:** user/platform
- **7. When it exists:** Submission-side name; exact snapshot unknown
- **8. Publicly available in released dataset:** NO
- **9. Raw or derived/anonymized:** Withheld, unlike public job_id
- **10. Outcome/runtime used in construction:** Not established
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** Unknown private name semantics cannot establish execution purpose.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** NO from public data
- **15. Prior runtime-prediction use:** YES: private QSSF name-based information
- **16. Incremental contribution isolated:** Not publicly reproducible
- **17. Reproducible from public data:** NO for original name-based Helios QSSF
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** HELART: https://github.com/S-Lab-System-Group/HeliosArtifact

## F133 — MLPerf / NVIDIA: LOAD_CKPT

- **1. Paper/system:** MLPerf / NVIDIA
- **2. Dataset/trace:** Training v5.1 LoRA configuration
- **3. Exact raw field or information source:** LOAD_CKPT
- **4. Example values, if documented:** True
- **5. Meaning according to source:** Initialize from checkpoint; not proof of resuming a failed run
- **6. Generator:** benchmark submitter
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Launch-script setting
- **10. Outcome/runtime used in construction:** NO for configuration
- **11. Primary category:** PLANNED SCOPE
- **12. Classification explanation:** Specified execution plan; not a per-run purpose label.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as prospective configuration; target interval alignment unresolved
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public config/result pair; varying cohort and warm-up inclusion in runtime not established
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** MLPERF: https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/benchmarks/llama2_70b_lora/implementations/nemo/config_common.sh; MLRESULT: https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/results/tyche_ngpu8_ngc25.09_nemo/llama2_70b_lora/result_0.txt

## F134 — MLPerf / NVIDIA: WARMUP_TRAIN_STEPS

- **1. Paper/system:** MLPerf / NVIDIA
- **2. Dataset/trace:** Training v5.1 LoRA configuration
- **3. Exact raw field or information source:** WARMUP_TRAIN_STEPS
- **4. Example values, if documented:** 5
- **5. Meaning according to source:** Planned warm-up training steps
- **6. Generator:** benchmark submitter
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Launch-script setting
- **10. Outcome/runtime used in construction:** NO for configuration
- **11. Primary category:** PLANNED SCOPE
- **12. Classification explanation:** Specified execution plan; not a per-run purpose label.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as prospective configuration; target interval alignment unresolved
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public config/result pair; varying cohort and warm-up inclusion in runtime not established
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** MLPERF: https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/benchmarks/llama2_70b_lora/implementations/nemo/config_common.sh; MLRESULT: https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/results/tyche_ngpu8_ngc25.09_nemo/llama2_70b_lora/result_0.txt

## F135 — MLPerf / NVIDIA: WARMUP_VALIDATION_STEPS

- **1. Paper/system:** MLPerf / NVIDIA
- **2. Dataset/trace:** Training v5.1 LoRA configuration
- **3. Exact raw field or information source:** WARMUP_VALIDATION_STEPS
- **4. Example values, if documented:** 5
- **5. Meaning according to source:** Planned warm-up validation steps
- **6. Generator:** benchmark submitter
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Launch-script setting
- **10. Outcome/runtime used in construction:** NO for configuration
- **11. Primary category:** PLANNED SCOPE
- **12. Classification explanation:** Specified execution plan; not a per-run purpose label.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as prospective configuration; target interval alignment unresolved
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public config/result pair; varying cohort and warm-up inclusion in runtime not established
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** MLPERF: https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/benchmarks/llama2_70b_lora/implementations/nemo/config_common.sh; MLRESULT: https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/results/tyche_ngpu8_ngc25.09_nemo/llama2_70b_lora/result_0.txt

## F136 — MLPerf / NVIDIA: VAL_CHECK_INTERVAL

- **1. Paper/system:** MLPerf / NVIDIA
- **2. Dataset/trace:** Training v5.1 LoRA configuration
- **3. Exact raw field or information source:** VAL_CHECK_INTERVAL
- **4. Example values, if documented:** 384
- **5. Meaning according to source:** Validation frequency setting
- **6. Generator:** benchmark submitter
- **7. When it exists:** before execution
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Launch-script setting
- **10. Outcome/runtime used in construction:** NO for configuration
- **11. Primary category:** PLANNED SCOPE
- **12. Classification explanation:** Specified execution plan; not a per-run purpose label.
- **13. Relationship to latent experimental objective:** weakly related
- **14. Prospective runtime-prediction admissibility:** YES as prospective configuration; target interval alignment unresolved
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** Public config/result pair; varying cohort and warm-up inclusion in runtime not established
- **18. Final usability for original hypothesis:** SUPPORTING ONLY
- **Evidence:** MLPERF: https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/benchmarks/llama2_70b_lora/implementations/nemo/config_common.sh; MLRESULT: https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/results/tyche_ngpu8_ngc25.09_nemo/llama2_70b_lora/result_0.txt

## F137 — MLPerf / NVIDIA: run_stop.metadata.step

- **1. Paper/system:** MLPerf / NVIDIA
- **2. Dataset/trace:** Training v5.1 result log
- **3. Exact raw field or information source:** run_stop.metadata.step
- **4. Example values, if documented:** 384
- **5. Meaning according to source:** Actual termination step; not a requested maximum
- **6. Generator:** scheduler / runtime monitor
- **7. When it exists:** after launch or after completion
- **8. Publicly available in released dataset:** YES
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** YES: measured outcome or its derivative
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** Outcome of this run; cannot be its own prospective input.
- **13. Relationship to latent experimental objective:** unrelated
- **14. Prospective runtime-prediction admissibility:** NO as current-job input; target or completed-history label only
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** YES as label, subject to target semantics
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** MLRESULT: https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/results/tyche_ngpu8_ngc25.09_nemo/llama2_70b_lora/result_0.txt

## F138 — CloudBrain-I: Submission launch command

- **1. Paper/system:** CloudBrain-I
- **2. Dataset/trace:** See prior audit notes
- **3. Exact raw field or information source:** Submission launch command
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Prior audit notes say launch command; linked raw artifact was inaccessible
- **6. Generator:** unknown
- **7. When it exists:** After launch for observed graph; otherwise unknown
- **8. Publicly available in released dataset:** Not verified accessible
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** CONFIGURATION IDENTITY
- **12. Classification explanation:** No certified prospective experimental-objective observable.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Not certified
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** No certified objective experiment
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** RECOVERED: research-audit-2026-09-23/evidence-notes.md and field-level-evidence-matrix.csv (pre-existing audit notes; underlying primary documents not all recovered)

## F139 — Meta Chakra: Observed execution graph

- **1. Paper/system:** Meta Chakra
- **2. Dataset/trace:** See prior audit notes
- **3. Exact raw field or information source:** Observed execution graph
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Runtime graph described in prior audit notes; not user purpose
- **6. Generator:** unknown
- **7. When it exists:** After launch for observed graph; otherwise unknown
- **8. Publicly available in released dataset:** Public trace framework; eligible cohort not verified
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** RETROSPECTIVE / UNUSABLE
- **12. Classification explanation:** No certified prospective experimental-objective observable.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Not certified
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** No certified objective experiment
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** RECOVERED: research-audit-2026-09-23/evidence-notes.md and field-level-evidence-matrix.csv (pre-existing audit notes; underlying primary documents not all recovered)

## F140 — Google Borg: Collection relationships (exact raw key not recovered)

- **1. Paper/system:** Google Borg
- **2. Dataset/trace:** See prior audit notes
- **3. Exact raw field or information source:** Collection relationships (exact raw key not recovered)
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Platform grouping; no audited mapping to experimental purpose
- **6. Generator:** unknown
- **7. When it exists:** After launch for observed graph; otherwise unknown
- **8. Publicly available in released dataset:** Generic trace public; eligible objective cohort not verified
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** ORDINARY SCHEDULER METADATA
- **12. Classification explanation:** No certified prospective experimental-objective observable.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Not certified
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** No certified objective experiment
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** RECOVERED: research-audit-2026-09-23/evidence-notes.md and field-level-evidence-matrix.csv (pre-existing audit notes; underlying primary documents not all recovered)

## F141 — IBM AI4DL: EVIDENCE GAP — exact field not established

- **1. Paper/system:** IBM AI4DL
- **2. Dataset/trace:** See prior audit notes
- **3. Exact raw field or information source:** EVIDENCE GAP — exact field not established
- **4. Example values, if documented:** Not established
- **5. Meaning according to source:** Prior search lead only
- **6. Generator:** unknown
- **7. When it exists:** After launch for observed graph; otherwise unknown
- **8. Publicly available in released dataset:** UNKNOWN
- **9. Raw or derived/anonymized:** Released value; representation as described
- **10. Outcome/runtime used in construction:** Unknown; not certified
- **11. Primary category:** UNKNOWN
- **12. Classification explanation:** No certified prospective experimental-objective observable.
- **13. Relationship to latent experimental objective:** unknown
- **14. Prospective runtime-prediction admissibility:** Not certified
- **15. Prior runtime-prediction use:** Not established in inspected evidence
- **16. Incremental contribution isolated:** Not established in inspected evidence
- **17. Reproducible from public data:** No certified objective experiment
- **18. Final usability for original hypothesis:** UNUSABLE
- **Evidence:** RECOVERED: research-audit-2026-09-23/evidence-notes.md and field-level-evidence-matrix.csv (pre-existing audit notes; underlying primary documents not all recovered)
