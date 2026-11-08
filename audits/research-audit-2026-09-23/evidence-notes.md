# Evidence boundary and source key

Audit date: 2026-09-23. No new web/literature search was performed. This matrix reuses the previous inspected primary-source record, locally downloaded data/code, current user-supplied author clarification, and explicitly identified local research notes.

## Verdict

**SUPPORTING EVIDENCE ONLY.** No certified public prospective field directly measures experimental objective in the audited record. PAI task roles and planned training budgets can support separate, narrower studies. They do not identify the original latent experimental-objective construct.

The previous CONTINUE verdict applied to expanded experiment-scope eligibility, particularly task roles. It must not be read as evidence that the original objective hypothesis is observable.

## Interpretation rules

- The CSV and Markdown contain the same 18 columns and 84 rows, including explicit evidence-gap rows. Not all 84 rows represent verified released columns. Some name documented private information sources, protocol settings, local-note-only inputs, or missing source coverage.
- Each row has exactly one primary classification. A semantic classification such as PLANNED SCOPE does not certify the released field's timing, variation, outcome independence, or adequacy. Consult eligibility and usability columns.
- CORE: directly supports testing the objective hypothesis. No row qualifies.
- SUPPORTING ONLY: can support a related but distinct statement, or document genuine planned scope. It does not imply a valid runtime experiment in every case: NATS timing normalization and LCBench's constant budget are explicit exclusions.
- CONTROL ONLY: not evidence of objective. This label does not override temporal-provenance restrictions. For example, workload labels whose timing is unresolved cannot enter a certified prospective model merely because they are controls.
- UNUSABLE: unusable for the requested objective hypothesis on the inspected public evidence, not a universal claim that the source has no scientific value.
- NOT ESTABLISHED is not a negative literature finding. It records absence of sufficient inspected evidence.
- Prospective eligibility addresses temporal/causal use as a feature, not causal identification of an intervention effect. Data license, consent, and legal clearance were not audited and are UNKNOWN where not established by separate review.
- We did not independently inspect an author email. The current request supplies the author clarification that Acme type uses job-name hints AND duration and that original/sanitized names cannot be released. The matrix uses that clarification and explicitly identifies its source.

## Evidence gaps

ORA, F-DATA, PREP, Park & Hong, Menear/Eagle, and unspecified workflow datasets are not supported by identifiable inspected primary documents in the available audit record. HPOBench/IBM AI4DL were search leads, not complete field-level audits. None is silently certified or ruled out.

SchedMate has a local summary listing user prompts, code, logs, history, and hardware metrics. That is not the paper or artifact. There is no verified extraction schema for model identity, dataset identity, planned versus observed steps, task/mode, hardware requirements, or stated purpose. Such outputs cannot be invented from the summary. The matrix records known claimed input sources as UNKNOWN and does not combine them into an asserted objective feature.

## Source key

- **P1**: [PAI v2020 official schema and lifecycle](https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2020).
- **P2**: [MLaaS in the Wild, author-hosted paper](https://qzweng.github.io/assets/pdf/2022.NSDI-MLaaS-Weng.pdf), section 5.2 and Figure 12. This already evaluates Group/User/Resource/GPU feature combinations for duration prediction.
- **A1**: [Acme NSDI 2024 paper](https://www.usenix.org/system/files/nsdi24-hu.pdf), section 3.2; [released repository](https://github.com/InternLM/AcmeTrace).
- **A2**: User-supplied author clarification in the 2026-09-23 request: type constructed using job-name hints and job duration; original and sanitized names cannot be released. No independently inspected author correspondence.
- **H1**: [Helios artifact](https://github.com/S-Lab-System-Group/HeliosArtifact), explicit non-release of job names and unavailable estimator/QSSF components.
- **H2**: [Helios public data](https://github.com/S-Lab-System-Group/HeliosData).
- **PH**: [Philly public schema](https://github.com/msr-fiddle/philly-traces).
- **AT**: [ATLAS artifact](https://github.com/zhiyunjiang0810/non-clairvoyant-with-predictions), Dataset_demonstration notebook and Prediction+Scheduling notebook. Source-table aggregation and prediction features were inspected. This does not certify the artifact's leakage-free claims.
- **MIT**: [Dataset documentation](https://github.com/MIT-AI-Accelerator/MIT-Supercloud-Dataset), [scheduler file](https://mit-supercloud-dataset.s3.amazonaws.com/datacenter-challenge/202201/slurm-log.csv), [model-label file](https://mit-supercloud-dataset.s3.amazonaws.com/datacenter-challenge/202201/labelled_jobids.csv). Downloaded scheduler: 395914 rows; labeled jobs: 3430, all OTHER, all sharing array identifiers/index values; three labeled users.
- **SLURM**: [Official array semantics](https://slurm.schedmd.com/job_array.html). This establishes native array semantics, not experiment semantics or the anonymization mapping of MIT's release.
- **ALI26**: [GPU 2026 schema](https://github.com/alibaba/clusterdata/blob/master/cluster-trace-gpu-v2026/docs/schema.md) and [README](https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2026).
- **ALI23**: [GPU 2023 schema/data/conversion](https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2023).
- **ALI25**: [GPU 2025 serving trace](https://github.com/alibaba/clusterdata/tree/master/cluster-trace-gpu-v2025).
- **SPOT**: [Spot GPU 2026](https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-spot-gpu).
- **NAS**: [NAS-Bench-101 paper](https://proceedings.mlr.press/v97/ying19a/ying19a.pdf), [API](https://github.com/google-research/nasbench/blob/master/nasbench/api.py), [training implementation](https://github.com/google-research/nasbench/blob/master/nasbench/lib/evaluate.py). Independent planned epoch budgets and measured training times; TPU v2. The locally parsed prefix only contains epoch-4 records; the four-budget full coverage is author-documented, not counted from the prefix.
- **NATS**: [NATS-Bench](https://github.com/D-X-Y/NATS-Bench), [collector with pseudo-time replacement](https://github.com/D-X-Y/AutoDL-Projects/blob/main/exps/NATS-Bench/tss-collect.py).
- **LC**: [LCBench README](https://github.com/automl/LCBench), fixed 50-epoch runs and seven sampled configuration parameters.
- **MP**: [Inspected MLPerf configuration](https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/benchmarks/llama2_70b_lora/implementations/nemo/config_common.sh), [result example](https://github.com/mlcommons/training_results_v5.1/blob/main/NVIDIA/results/tyche_ngpu8_ngc25.09_nemo/llama2_70b_lora/result_0.txt). Do not conflate checkpoint initialization with recovery or warm-up duration with benchmark-scored time.
- **GEN**: [GenTD26 documentation/data](https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-GenAI). Serving request configuration is not experiment purpose; exported planned-versus-completed count provenance remains incomplete.
- **SM-NOTES**: Local LiteratureReview/PaperInsights/SchedMate.md and Comparison_Table.md. These are research notes, not primary proof of extraction fields, absence of objective use, or empirical novelty.
- **CB**: [CloudBrain-I paper](https://tianweiz07.github.io/Papers/22-iccd.pdf); linked raw artifact was inaccessible during the prior audit.
- **CH**: [Meta Chakra description](https://engineering.fb.com/2023/09/07/networking-traffic/chakra-execution-traces-benchmarking-network-performance-optimization/).
- **BORG**: [Google cluster-data repository](https://github.com/google/cluster-data).

## Existing numerical evidence

See ../research-audit-2026-09-22/README.md, coverage.json, pai-eligible-coverage.json, and source-manifest.json. The conservative PAI role cohort has 229469 successful GPU task records from 212046 jobs and 624 users; it is conditional on successful completion. Those counts demonstrate a feasible role study, not observation of experimental objective.
