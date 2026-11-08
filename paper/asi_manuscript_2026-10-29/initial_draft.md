# Partition and Weighting Sensitivity in ASI Execution-Duration Prediction: A Case Study

*Initial empirical manuscript draft, 29 October 2026. Results are drawn from existing saved artifacts. No new models, predictions or holdout evaluations were produced for this draft. Editorial evidence notes below must be resolved or retained before submission.*

## Abstract

Public workload categories can distinguish duration distributions without providing stable incremental predictive value beyond other metadata. We study the addition of one coarse workload-type field to an ASI execution-duration predictor using three existing experiments. On a historical workload-disjoint test split, the reported mean relative LogMAE gain across three model seeds decreases from approximately 5.88% with resource and priority controls to 1.05% with additional model/application controls. These means are descriptive, and all principal strong-control conditional intervals include zero. Two historical selected-validation comparisons reverse ranking, while saved-predictor diagnostics show that influential short workloads can improve rather than harm the augmented model. A subsequent ten-partition study excludes both historical holdout populations. In this restricted population, the augmented model improves selected-validation LogMAE in eight execution-weighted and nine equal-workload comparisons. One partition reverses ranking solely under evaluation reweighting. The experiments document a bounded interaction among baseline specification, group partitioning, selected predictors and evaluation weighting. They neither establish a new predictor nor identify a causal mechanism or scheduling benefit. Their practical contribution is an auditable case for reporting the evaluation unit and selection status alongside small metadata ablation gains.

## 1. Introduction

Runtime prediction is often discussed as an input to resource management, yet an offline improvement is meaningful only relative to a specific task and evaluation design. A field that separates marginal duration distributions may add little beyond an existing predictor. A model that improves the average execution may worsen the average workload, because workloads contribute different numbers of execution records. Moreover, a validation score used to choose a model is evidence about selected validation performance, rather than an independent assessment of that model's generalization.

We investigate these issues through an ASI case study. The variable of interest is `job_type_public`, a coarse public category covering training, development, online inference and offline inference. Our principal baseline already includes resource requests, GPU specification, priority, model type and a GenAI indicator. Thus the comparison concerns one added category within an already semantic feature set. Calling it “semantics versus no semantics” would misdescribe the experiment.

The three experiments form an evidence sequence, not three independent replications. Experiment 1 establishes a small, baseline-dependent increment on a historical test split. Experiment 2 examines a reversal between two selected-validation outcomes and localizes the saved predictors' errors. Experiment 3 describes sensitivity over ten group partitions of a restricted population, retaining historical holdouts outside the study. Figure 5 summarizes these distinctions.

Our contributions are an ASI-specific baseline comparison, saved-predictor diagnostics that constrain explanations of a partition reversal, and a ten-partition account of selected-validation ranking under two evaluation units. We do not claim novelty for ablation, group separation, weighting sensitivity or model-selection caution individually. The contribution lies in the documented empirical conjunction and its implications for interpreting this particular metadata increment.

## 2. Task and related work

The ASI source study characterizes a heterogeneous production AI fleet and already shows execution-time distributions by job and model type in Figure 7. Our question is narrower: whether adding the public type field improves prediction after specified controls on workloads separated by identity. Marginal separation of duration distributions does not answer that question. Conversely, our offline prediction experiment does not evaluate the deployed management mechanisms in the source paper. [Li et al., OSDI 2026](https://www.usenix.org/system/files/osdi26-li-suyi.pdf).

Workload metadata prediction has close precedent. Weng et al. study duration prediction for recurring PAI tasks using group, user and resource information, with feature-combination comparisons and scheduling analysis. Our ASI workload-ID-disjoint task addresses a different transfer regime; this difference does not invalidate their recurring-task evaluation. We cite that work as direct predictive prior art, not merely a trace characterization. [Weng et al., NSDI 2022](https://www.usenix.org/conference/nsdi22/presentation/weng).

ATLAS provides a PAI-derived dataset and prediction/scheduling benchmark, including submission-time feature design, histories, feature analysis and temporal partitioning. Our case study complements that program through a different trace, workload separation and a comparison between execution and workload averaging. It does not introduce realistic runtime benchmarking or establish superior prediction performance across the datasets. [Jiang et al., ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/file/de15d58b049530fe7df634f71e47164b-Paper-Conference.pdf).

TARE directly demonstrates that runtime-prediction conclusions depend on the weighting and operational objectives used for evaluation. Its resource-usage weighting and tail analysis differ from our frequency-driven distinction between executions and workload identities. The broad lesson is shared; the averaging unit and empirical setting are different. We refer to the inspected arXiv v1 rather than claiming independently verified conference acceptance. [Xiao et al., TARE, 2026 preprint](https://arxiv.org/html/2607.04935v1).

Menear and Duplyakin explicitly study the predictive value of adding the primary application, reporting variable benefit by application and runtime length. That is close conceptual precedent, although application identity differs from ASI's coarse type field. The inspected laboratory abstract supports this comparison; we do not infer its exact split or model protocol without the poster. Menear et al. also codify runtime-prediction methodology and best practices on Eagle, limiting the novelty of a general “evaluation pitfalls” claim. [Menear and Duplyakin, PEARC23 poster record](https://research-hub.nlr.gov/en/publications/is-knowledge-about-running-applications-helping-improve-runtime-p/), [Menear et al., PEARC 2023](https://research-hub.nlr.gov/en/publications/mastering-hpc-runtime-prediction-from-observing-patterns-to-a-met-2/).

Finally, selection criteria can themselves be overfit. We therefore label evaluations on selection data explicitly and do not convert repeated validation wins into an unbiased generalization estimate. This is an application of established selection-bias concerns, not a new statistical result. [Cawley and Talbot, JMLR 2010](https://www.jmlr.org/papers/v11/cawley10a.html).

## 3. Study design and evidence scope

### 3.1 Population, target and predictors

The historical canonical population contains 4,709,624 executions and 473,265 workloads with non-null workload identities and one of the four retained type values. The historical protocol retains qualifying execution records, including repeated-pod rows and long durations; the analysis is therefore not automatically an analysis of unique jobs. The historical test partition contains 711,321 executions from 70,705 workloads. We use previously saved reports of this test; we do not reopen its predictions or outcomes.

The target is `log1p(duration_hours)`, where the duration is an execution-span label supplied by the dataset. We do not equate it with pure GPU computation time or assume every long-lived online service has a conventional completed-job runtime. The principal M0 features are `gpu_request`, `gpu_spec_public`, `priority_class`, `model_type_public`, and `is_genai_request`; M1 adds `job_type_public`. Workload identity defines groups and is excluded from model inputs. Planned computational scope, user identity and historical execution controls desired by a richer prediction study are not fully available here. Guaranteed availability of all feature values before scheduling is not independently certified.

### 3.2 Model selection and experiment differences

The recorded implementation uses CPU LightGBM 4.7.0 with L1 objective, a learning rate of 0.05, a 200-round cap and validation early stopping with patience 30. Each side receives 12 candidates spanning 15/31/63 leaves, minimum leaf counts 20/100 and feature fractions 0.8/1.0. Candidate selection minimizes execution-weighted validation LogMAE, breaking ties by candidate ID. Encodings are fit using training data only.

Experiment 1 varies three model seeds on one fixed workload-disjoint 70/15/15 split and reports the historical test comparison after selection. Its weak-control comparison uses resources plus priority, whereas its principal comparison includes application/model controls. Experiment 2 varies two workload partitions while keeping the model seed fixed and analyzes the resulting selected validation predictions. It is not a repeated-training-randomness experiment.

Experiment 3 removes the union of both historical test-workload sets, leaving 341,617 workloads and 3,372,430 executions: 72.18% and 71.61% of the original counts, respectively. It applies ten group partition seeds and one fixed model seed, with 12 candidates per side per partition. Both reported metrics evaluate the execution-weighted-selected winners. The equal-workload metric is secondary and never used to reselect models. Historical holdouts and new per-partition test outcomes remain unevaluated in this study. The documented registration precedes the uploaded results, but is not a public independent timestamp proving that every local analysis preceded inspection.

### 3.3 Metrics and attribution

For workload w with n_w execution records, let S_mw be the sum of absolute errors in log1p(hours) for model m, and let N=sum_w n_w and W be the number of workloads. Define

`L_execution(m) = sum_w S_mw / N`

`L_workload(m) = (1/W) sum_w (S_mw / n_w)`.

The first is the mean error of an observed execution; the second first averages within each workload and then weights workload identities equally. Equal-workload averaging is not equal-user, fairness, GPU-hour or deployment-cost weighting. Neither metric is universally correct.

We report signed gain `D = L(M0) − L(M1)` and relative gain `100 D / L(M0)`. Positive values favor M1 throughout the new figures. For a disjoint workload subset G, its contribution to the execution-weighted gain is `sum_(w in G)(S_0w − S_1w)/N`. These signed contributions sum to the total gain. A ratio to a signed net gain may be negative or exceed 100% when beneficial and harmful contributions cancel; it is not a probability or a fraction of uniformly harmful error.

### 3.4 Verification scope

The October 29 audit reports hash matching for ten validation workload-loss tables and reconstruction of 40 selected metrics, as well as checking 240 candidate records and 20 winners. Those are inherited audit findings, not new raw-data verification in this drafting task. For the supplied figure package we independently check the original consolidated report's 20 winners against its candidate records and reconcile all 40 winner metrics and both reported mean signed gaps. This establishes aggregate consistency within those saved records. Complete training execution, feature timing and Experiment 3 source-to-split lineage are not certified by this check.

## 4. Experiment 1: the historical increment depends on baseline controls

With resource plus priority controls, audit-reported relative test gains are 5.949%, 5.844% and 5.848% for the three model seeds. With additional application/model controls, the checkpoint reports gains of 0.946%, 0.815% and 1.379%. Their informal arithmetic means are approximately 5.88% and 1.05%. These are descriptive summaries, not a protocol-defined pooled estimator. Figure 1 presents individual results.

All three principal strong-control paired workload-bootstrap intervals include zero. These intervals resample workloads conditional on the historical fitted models; they do not account for all training and model-selection variation. The principal models also worsen original-hour MAE in every model seed despite the positive LogMAE point gains. Consequently, the results do not support an unqualified claim that adding type improves runtime prediction across objectives.

The smaller gain under richer controls is consistent with predictive overlap and changes in model fit. It does not establish a conditional-information quantity or demonstrate that application metadata causally explains the type field. Separately fitted finite-only models have principal gains below 1%; they must not be confused with evaluating the finite subset of models trained on all four types. The historical judgment that the field was insufficient as a standalone contribution remains compatible with a useful later sensitivity case study.

## 5. Experiment 2: localizing a selected-validation reversal

The two historical selected-validation execution-weighted gains are +2.084% and −4.907%. Equal-workload gains are +3.664% and −2.755% (Figure 6). The original baseline and augmented models contain 94 and 190 trees, respectively; the second pair contains 141 and 5. These are saved selection outcomes, not evidence that tree count alone causes the reversal.

Frequency is highly concentrated in both partitions: the most frequent 1% of validation workloads account for 62.446% and 65.936% of executions. But the influential workloads that alter a duration summary need not be the workloads that harm M1. In the second partition, the two most frequent short online-inference workloads improve under M1. Offline inference contributes 59.281% of net M1 excess error, with important deterioration concentrated in high-frequency populations; longer online-inference records show a different residual direction. These observations reject the simple claim that the short online workloads cause the cross-model failure. They localize errors rather than identify a causal metadata interaction.

An exploratory shared-record comparison further constrains interpretation. The validation partitions share 100,221 execution records from 10,632 workloads, with matching observed features and targets. On these same records, the saved original predictor pair has M1−M0 LogMAE −0.003294, whereas the second pair has +0.021352. Thus the changed ranking on those records cannot be explained solely by their evaluated composition. The saved predictors behave differently. Their differences may reflect changed training populations, selected hyperparameters and rounds; the check does not separate these sources. Nor does it show that the full-partition reversal is exclusively a predictor effect.

## 6. Experiment 3: partition and weighting sensitivity

In the ten restricted-population partitions, M1 improves execution-weighted selected-validation LogMAE in eight cases and equal-workload LogMAE in nine. The unweighted mean signed gaps across the ten partitions are +0.00449751 and +0.01946433 LogMAE units. These are means of signed differences in absolute-error metrics, not means of absolute model gaps and not pooled row-level effects.

| Partition seed | Execution-weighted gain (%) | Equal-workload gain (%) |
|---|---:|---:|
| 20261028 | +2.621 | +2.285 |
| 20261029 | +0.952 | +3.771 |
| 20261030 | +1.799 | +3.392 |
| 20261031 | +1.381 | +4.286 |
| 20261101 | −6.119 | −2.457 |
| 20261102 | −2.015 | +0.978 |
| 20261103 | +2.099 | +3.515 |
| 20261104 | +1.369 | +2.925 |
| 20261105 | +1.167 | +3.723 |
| 20261106 | +3.001 | +2.909 |

Figure 2 retains every partition rather than highlighting only wins. In seed 20261102, M1 worsens execution-weighted LogMAE by 2.015% but improves equal-workload LogMAE by 0.978%. Predictions and selected winners are held fixed; the evaluation weighting changes. This is a direct example of two averaging units supporting different rankings. It does not establish that either unit is the right operational objective.

The concentration summaries and signed contributions in Figure 3 show why frequency alone is insufficient as an explanation. Strong concentration appears alongside positive and negative comparisons, and the frequent-workload component can benefit or harm M1. Arithmetic attribution states where the observed loss difference accumulates; it does not establish why those prediction errors arose.

Selected complexity also changes. The M1 winners in seeds 20261101 and 20261102 use one and nine boosting rounds, respectively; several positive comparisons use substantially more rounds, including capped 200-round selections. Figure 4 reports these outcomes and the full candidate losses for one negative case. The pattern motivates caution about selection sensitivity, but does not isolate early stopping from other hyperparameters or population changes. No causal experiment fixing those factors was performed.

The ten partitions overlap in their underlying data and use validation outcomes for both early stopping/selection and reporting. Consequently, 8/10 and 9/10 are descriptive counts, not 80% or 90% probabilities of future success. We report no binomial test, naive standard error over seeds, or independent-replication confidence interval. The secondary metric also evaluates selected models on the same validation records; avoiding selection on that metric does not turn it into a held-out test.

## 7. Implications and limitations

For benchmark authors, the case supports reporting a feature increment together with baseline controls, grouping rule, selection status and averaging unit. A headline percentage alone conceals whether it concerns a historical test or selected validation, whether frequent workloads dominate, and whether the baseline already contains related semantics. These are practical reporting lessons grounded in this case, not claims that the literature lacked such principles.

For system builders, a coarse label's marginal offline value should be checked against the intended population and decision objective before it informs a management policy. We measure no scheduling policy, queueing response, utilization, energy or monetary outcome. Neither a smaller LogMAE nor a workload-weighted win establishes an operational improvement. ATLAS and TARE illustrate why prediction evaluation and scheduling evaluation require separate evidence.

Several limits bound the findings. First, this is one trace, one feature increment and one model family/grid. Workload-ID separation is not temporal deployment evaluation and does not guarantee separation of every latent application family or tenant. Second, the canonical population is narrower than the source trace, and Experiment 3 further excludes historical holdout workloads. Its findings cannot be asserted for the excluded population. Third, execution span and coarse type are imperfect proxies for pure compute demand and fine-grained lifecycle intent. Fourth, available controls omit computational scope and other potentially relevant metadata, while full prediction-time provenance remains unresolved. Fifth, selected-validation outcomes are potentially optimistic, and their M0/M1 gap is not a quantified estimate of selection bias. Sixth, diagnostics and error-selected subgroups are exploratory and can be affected by multiplicity and cancellation. Finally, internal hash/metric consistency cannot independently establish every source label or training action.

We omit the unlocated within-M1 0.2915-versus-0.2142 decomposition and its associated exact-profile count as evidence. It is not interchangeable with the verified M1-versus-M0 attribution. Nothing in this manuscript requires retraining or evaluating reserved holdouts.

## 8. Conclusion

The measured value of ASI's public workload-type field is conditional on the baseline, partition, selected predictors and evaluation weighting. A historical test shows a small increment under richer controls; subsequent validation studies show reversals and weighting sensitivity without an identified causal mechanism. The contribution is a reproducible empirical account of those distinctions. It supports more interpretable runtime-prediction reporting while leaving general deployment benefit and scheduling impact unestablished.

## Editorial evidence notes

- The conversation interface returned a 20,000-character prefix of the October 29 audit. The draft incorporates the accessible audit and original checkpoint, phase-one findings, registration and consolidated report; complete line-by-line incorporation of the missing audit remainder is not claimed.
- Figure 1's weak-control values are audit-transcribed; strong-control values and intervals are directly checkpoint-reported. Original aggregate binding of weak-control results remains a submission provenance task.
- The supplied plots use saved aggregates/candidate records. The audit's workload-Parquet reconstruction is attributed to that audit and was not repeated here.
- Figures, captions and exact companion tables are specified in `manuscript_plan.md`; reference links above are primary publisher, author/laboratory or paper sources. No first-of-kind or exhaustive-literature claim is made.
