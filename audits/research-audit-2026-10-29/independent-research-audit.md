# Independent novelty and methodological validity audit
Date: 29 October 2026. Scope: complete ASI Experiments 1–3, with explicit evidence limits.

## A. Executive verdict

**Proceed only with narrower claims.**

The artifacts support an empirical case study of how the measured incremental value of one coarse workload-type field varies with workload-disjoint partitions, evaluation weighting, and the models selected using validation data. They do not establish a new predictor, a new scheduling method, a causal explanation of instability, or an independently confirmed general improvement.

There is a coherent manuscript here, but its scientific contribution is smaller than “discovering pitfalls in GPU runtime prediction.” Feature ablation, group-aware evaluation, weighting sensitivity, selection bias, and temporal generalization already have substantial precedent. The potentially distinct contribution is their concrete interaction in the ASI execution-span prediction task, documented with reproducible loss attribution. That is a bounded empirical extension, not an established major methodological advance.

The current title is broad. A more accurate title is **“Partition and Weighting Sensitivity in ASI Execution-Duration Prediction: A Case Study.”** This describes demonstrated behavior without suggesting a general theory of GPU prediction failures.

A workshop, short empirical paper, or technical report is a reasonable target. The present evidence does not justify positioning this as an OSDI/NSDI/EuroSys/MLSys main-track contribution. HPDC, SC, or SoCC main tracks are not automatic alternatives with a lower novelty requirement.

## Evidence standard and what was actually checked

This audit performed literature searches, read original documentation and saved artifacts, and verified arithmetic from existing validation workload loss sums. It did **not** train a model, generate predictions, modify a protocol, run a new robustness experiment, or evaluate reserved holdouts.

Evidence levels:

- **V — verified from saved original artifacts in this audit:** Experiment 3 summary results and candidate records, ten downloaded validation workload loss-sum tables, their committed hashes, and reconstruction of their aggregate losses.
- **R — read in historical original reports/aggregate artifacts:** Experiments 1–2 numerical summaries and their historical verification reports. Their models/predictions were not rerun.
- **U — not independently located/verified:** the exact 0.2915 versus 0.2142 within-M1 decomposition and associated 76,366 exact-profile count; full certification of prediction-time feature provenance; complete source-to-split lineage for Experiment 3.

Primary artifact entry points:

1. [Experiment 3 preregistration result.json](https://drive.google.com/file/d/1ds2nOIhZPlORSfbwnM8ZgRnIxhRLHaqO/view).
2. [Experiment 3 consolidated report](https://drive.google.com/file/d/1Ntk1MhpLtjSHCcPceswH1Rikjack0aHs/view).
3. [All ten seed folders](https://drive.google.com/drive/folders/1DML5EJ5UQlBqDW1ui_lvt0j8HaPoU6CB).
4. [Historical completed checkpoint](https://drive.google.com/file/d/1wdEwx54Y-rF9ZSiopj0zuDek5LJ991Ra/view).
5. [Experiment 2 saved verification](/Users/tiloschan/Documents/Codex/2026-10-26/referenced-chatgpt-conversation-this-is-an-5/outputs/ASI_instability_mitigation/phase_a_verification.json).
6. [Experiment 2 phase-one findings](/Users/tiloschan/Documents/Codex/2026-10-26/referenced-chatgpt-conversation-this-is-an-5/outputs/ASI_phase1_prediction_instability_diagnostics/phase1_findings.md).
7. [Experiment 1 archive inventory](/Users/tiloschan/Downloads/asi_completed_2026-10-13/FILE_INVENTORY.json): the inspected inventory maps **resume_reports/results-summary.json** to content object SHA-256 **2609e8a3168b482e8d5051954d96a885be453ab90eb099afaf78954bc31c1588**.

Checks passed: all ten validation Parquet hashes matched their SUMMARY/COMMIT.json entries; 40 reconstructed M0/M1 execution/equal-workload metrics matched saved results within 1e-12; the 240 candidate records contain 12 candidates per side per seed; all 20 reported winners match minimum execution-weighted validation loss with candidate-ID tie breaking. This establishes internal consistency, not an independent audit of every raw row, training execution, or source label.

The preregistration file specifies the restricted population, ten seeds, fixed model seed, grid, early stopping, selection metric, secondary metric, and test-exclusion policy. The uploaded registration precedes uploaded seed-result folders and includes a registration timestamp. That is evidence of a documented frozen plan; it is not an independently timestamped public registry proving every analysis was specified before any local result inspection.

### Verified Experiment 3 headline

Positive percentages mean lower M1 LogMAE. Both metrics evaluate the execution-weighted-selected models.

| Split seed | Execution-weighted improvement | Equal-workload improvement |
|---|---:|---:|
| 20261028 | +2.621% | +2.285% |
| 20261029 | +0.952% | +3.771% |
| 20261030 | +1.799% | +3.392% |
| 20261031 | +1.381% | +4.286% |
| 20261101 | −6.119% | −2.457% |
| 20261102 | −2.015% | +0.978% |
| 20261103 | +2.099% | +3.515% |
| 20261104 | +1.369% | +2.925% |
| 20261105 | +1.167% | +3.723% |
| 20261106 | +3.001% | +2.909% |

M1 wins 8/10 and 9/10, respectively. Mean signed M0−M1 differences are **+0.00449751** and **+0.01946433**. “Mean absolute difference” is potentially misleading: these are means of signed differences in absolute-error metrics, not means of absolute model gaps.

Seeds are identifiers, not execution dates. The presence of seeds labeled November does not imply experiments occurred after this audit's date.

## B. Novelty overlap matrix

Search covered GPU/HPC runtime prediction, learning-augmented scheduling, Alibaba traces, semantic feature ablations, group/temporal evaluation, concentration and weighted metrics, leakage, and model selection. Primary papers, author/publisher pages and official implementations were used. Prior local literature notes supplied leads, not independent evidence.

“Not found” below means not established in the inspected sources, not proof of worldwide absence. An exact duplicate was not verified; neither was a broad first-of-kind claim.

| Prior work: authors and publication status | Exact inspected contribution | Overlap with Experiments 1–3 | Remaining distinction and scientific significance |
|---|---|---|---|
| **Smith, Foster & Taylor, “Predicting Application Run Times Using Historical Information,” JSSPP 1998.** [Full text](https://www.globus.org/sites/default/files/runtime.pdf) | Historical similarity templates selected using search methods; application/context attributes include execution/job metadata, users, executables and arguments. | Runtime metadata and feature-selection value are old ideas. Exp1 is not a new semantic-prediction premise. | ASI's public coarse type under the stated controls and workload-disjoint design differs. It is a modern empirical extension, not a new principle. |
| **Weng et al., “MLaaS in the Wild,” NSDI 2022.** [Publisher](https://www.usenix.org/conference/nsdi22/presentation/weng), [paper](https://www.usenix.org/system/files/nsdi22-weng.pdf) | §5.2/Fig.12 evaluates duration prediction with CART and Group/User/Resource/GPU feature combinations on recurrent PAI tasks, followed by scheduling simulation. | Direct overlap with Alibaba duration prediction and feature ablations. Treating this as characterization alone would conceal close prior art. | PAI recurrence/group features differ from ASI job-type increments on unseen workload IDs. Your split targets a harder/different transfer question, but does not demonstrate that the earlier paper's estimand was invalid. |
| **Menear & Duplyakin, “Is Knowledge About Running Applications Helping Improve Runtime Prediction of HPC Jobs?”, PEARC23 poster, 2023.** [Laboratory record](https://research-hub.nlr.gov/en/publications/is-knowledge-about-running-applications-helping-improve-runtime-p/) | Explicitly studies adding primary application as a predictor; the primary abstract reports variable benefits by application and runtime length. | Very close conceptual precedent for Exp1's semantic-feature increment. | Application identity differs from lifecycle type. Exact ASI feature/control comparison remains distinct, but “adding semantics helps” is already studied. **Access limit:** poster PDF was inaccessible; exact splits/models/numbers are not asserted. |
| **Menear, Nag, Perr-Sauer, Lunacek, Potter & Duplyakin, “Mastering HPC Runtime Prediction: From Observing Patterns to a Methodological Approach,” PEARC 2023.** [Laboratory preprint record](https://research-hub.nlr.gov/en/publications/mastering-hpc-runtime-prediction-from-observing-patterns-to-a-met/), [proceedings DOI](https://doi.org/10.1145/3569951.3593598) | Runtime-prediction best practices and empirical methodology on the 11-million-job Eagle dataset, with released data/code. | Directly limits novelty of a general “evaluation pitfalls” framing. | ASI frequency concentration and selected-complexity patterns are a different case. **Access limit:** original full PDF was not retrievable; detailed claims from indexed excerpts are not used to establish exact equivalence. |
| **Hu, Zhang, Sun, Wen & Zhang, “Lucid,” ASPLOS 2023.** [Full text](https://tianweiz07.github.io/Papers/23-asplos.pdf) | GA²M duration estimation uses job/user/GPU-related submission attributes and name representations within a scheduler that also profiles and updates jobs. | Metadata prediction is established; the systems contribution depends on actual scheduling behavior. | No inspected isolated ASI job-type increment. Your project is an offline empirical analysis, not a competing scheduler. |
| **Jiang, Zhao, Xia & Zomaya, “ATLAS: Alibaba Dataset and Benchmark for Learning-Augmented Scheduling,” ICLR 2026.** [Published paper](https://proceedings.iclr.cc/paper_files/paper/2026/file/de15d58b049530fe7df634f71e47164b-Paper-Conference.pdf) | PAI-derived prediction/scheduling benchmark; LightGBM log-duration models with metadata/history, temporal partitioning, calibration, feature analysis and scheduler objectives. | Substantial overlap with model family, target transformation, metadata ablation and realistic benchmarking. | ASI, strict workload-ID-disjoint partitions, micro/macro contrast and selected-round sensitivity remain different. This can support a focused companion case study; it does not displace ATLAS or reveal that its evaluations are wrong. |
| **Li et al., “Heterogeneity at Hyperscale,” OSDI 2026, Operational Systems.** [Publisher paper](https://www.usenix.org/system/files/osdi26-li-suyi.pdf) | Introduces ASI characterization and deployed resource-management mechanisms; Fig.7 already distinguishes execution distributions by job/model types. | The exact trace already links type categories with duration distributions. | Conditional out-of-group prediction value after controls is not the same as marginal characterization. This is a substantive estimand distinction, but it still needs credible estimation. |
| **Xiao, Wu, Lu, Wang, Zhao & He, “TARE: Tail Aware Evaluation of HPC Job Runtime Prediction,” arXiv v1, 6 July 2026.** [Full text](https://arxiv.org/html/2607.04935v1), [metadata](https://arxiv.org/abs/2607.04935) | Resource-weighted GeoAccuracy, tail/decile evaluation, rolling splits, and a scheduling replay show that aggregate prediction conclusions depend on weighting and operational objectives. | Closest challenge to claiming that weighting-sensitive runtime evaluation itself is novel. | TARE weights jobs by resource consumption; your comparison weights execution rows versus workload identities. Frequency concentration is not the same as runtime-tail or node-hour concentration. The exact phenomenon differs, but the broad evaluation lesson is known. Publication: submitted to ICPP26 according to arXiv; acceptance was not independently verified from the official schedule/booklet. |
| **Shafin & Ahmed, “Leakage-Safe and Scheduler-Aware Machine Learning for Grid Job Runtime Prediction,” September 2026 arXiv preprint.** [Full text](https://arxiv.org/html/2609.13701v1) | Submission-time feature policy; temporal and cold-start evaluation, categorical models, feature ablations and a simplified scheduling study on AuverGrid. | Direct contemporary overlap with leakage-aware runtime benchmarking and generalization framing. | Different dataset, feature construct and concentration diagnostics. Do not present chronology or cold-start evaluation as a new method. This preprint's existence does not certify all its methodological claims. |
| **Pourali & Khazaei, “ORION,” ICPE 2026.** [Conference paper](https://icpe2026.spec.org/preprint/ORION_Integrated_Runtime_Modelling_for_Predicting_Deep_Learning_training_time.pdf) | Iteration-time modelling couples GPU computation with CPU/data-loading/storage effects; evaluates held-out hardware/configurations. | Relevant GPU runtime/generalization literature, but limited overlap with coarse execution-span metadata. | Different target granularity and richer mechanistic inputs. Shows why “GPU execution-duration prediction” must specify the prediction task rather than lumping all GPU predictors together. |
| **Romero Ugalde, Faqir-Rhazoui, Funk & Gorroñogoitia Cruz, “Evaluating Runtime Prediction and Conservative Walltime Policies in HPC Systems,” October 2026 manuscript.** [Full text](https://arxiv.org/html/2610.27755v1), [metadata](https://arxiv.org/abs/2610.27755) | Rolling temporal prediction, seen/unseen workload regimes and conservative walltime recommendation on Fugaku/Eagle. | Further overlap with deployment/generalization evaluation and the distinction between prediction and operational decisions. | No inspected ASI job-type ablation. The manuscript states SBAC-PAD 2026 acceptance; this audit verified that statement, not an independently located proceedings entry. |
| **Cawley & Talbot, JMLR 2010.** [Paper](https://www.jmlr.org/papers/v11/cawley10a.html) | Selection criteria can be overfit, creating evaluation bias comparable to algorithm differences. | Direct precedent for validation reuse and selection instability. | Your saved candidates instantiate this concern; they do not supply a new theory or quantify selection bias without independent evaluation. |
| **Bengio & Grandvalet, JMLR 2004.** [Paper](https://www.jmlr.org/papers/v5/grandvalet04a.html) | Establishes limitations of variance estimation for K-fold cross-validation under correlated errors. | Supports caution about shared-data dependence. | Their theorem is about K-fold CV, not a proof specific to your ten repeated group partitions. Do not overstate the transfer of the theorem. |
| **Roberts et al., Ecography 2017.** [Author record and original abstract](https://florianhartig.github.io/publications/roberts2017cross/) | Evaluation blocking must match structured dependence and the intended prediction task; blocking can induce extrapolation. | Workload-disjoint evaluation is an application of established group/blocking principles. | The appropriate ASI grouping and its consequences are empirical questions. Group separation itself is not methodological novelty. |
| **Kapoor & Narayanan, Patterns 2023.** [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856/) | Leakage taxonomy connects data dependence, temporal availability and mismatched evaluation distributions with overclaimed validity. | Direct precedent for the feature-timing and unit-of-analysis audit. | Your potential contribution is specific evidence, not discovery of leakage as a general issue. |

**Novelty conclusion:** none of the generic ingredients is new. The conjunction could still yield a useful empirical contribution if it reveals a consequential, well-documented failure of a common interpretation. The strongest specific observation is that the same extra public category has unstable selected-validation value across workload-disjoint partitions, and that evaluation-unit changes can alter ranking while broad concentration alone cannot explain the sign. There is no verified evidence that this exact ASI result is already published. That is weaker than proving it is novel enough for a major conference.

## C. Claim-by-claim validity audit

| Proposed claim | Supporting artifact | Evidence | Skeptical verdict |
|---|---|---|---|
| “Job type yields about 5.88% benefit, declining to 1.05% with application controls.” | Experiment 1 archived results-summary and completed checkpoint | R; weak-control model-seed gains 5.949393%, 5.844247%, 5.848031%; strong-control gains 0.946168%, 0.814672%, 1.378673% | Survives as an informal descriptive summary over three model seeds on one split. It is not a protocol-defined pooled effect or independent replication. The weaker baseline was **resource plus priority**, not resource only. |
| “Application information explains most of job type's independent information.” | Same ablations | R, predictive comparison | Too strong. Gains shrink under richer controls, consistent with predictive redundancy and/or changes in model fit. No conditional-information quantity or causal explanation was identified. |
| “M0 is a no-semantics baseline.” | Feature lists in original code, selections and summaries | V/R | False. Model type and GenAI detection already carry semantics. M1 adds one coarse lifecycle/type field to an already semantic baseline. |
| “Selected M1 ranking reverses across the original two partitions.” | Experiment 2 verification and phase-one findings | R; +2.083576% versus −4.906626%; model counts and input hashes documented | Survives as a saved validation result. The audit did not rerun predictions. Both partitions share the same fixed model seed; this is partition sensitivity. |
| “190 versus 5 trees identifies early stopping as the cause.” | Experiment 2 selection records | R | Unsupported causally. Selected leaves/minimum leaf settings also change. Training populations and validation populations change together. |
| “Two workloads caused the M1-versus-M0 reversal.” | Phase-one workload attribution | R, directly contradictory to that assertion | Rejected. Those workloads benefit from M1 versus M0. Their influence on a separate within-M1 comparison cannot establish the cross-model mechanism. |
| “Those workloads contribute 0.2915 against a net 0.2142 within M1.” | Researcher summary only in this audit | U | The arithmetic could exceed 100% of net because other workloads offset it. But the exact saved source was not located, so retain as unverified and do not promote it to a causal result. |
| “M1 wins 8/10 execution and 9/10 workload partitions.” | Ten SUMMARY files and validation-loss Parquets | V | Survives exactly as a descriptive count of these selected-validation outcomes. Not 80%/90% probability of success on future clusters or independent statistical replications. |
| “The mean effect is +0.00450 / +0.01946.” | Consolidated report and reconstructed metrics | V | Survives for the fixed collection of dependent partitions. No naive across-seed standard error, binomial significance, or generic population confidence interval is justified. |
| “Weighting can reverse the ranking.” | Seed 20261102 workload losses | V | Demonstrated for fixed selected predictions: execution-weighted M1 worsens 2.015%, equal-workload improves 0.978%. This is an estimand change, not evidence that one metric is correct. |
| “Concentration explains negative model rankings.” | Top-frequency shares, signed contributions, positive control | V | Rejected as a sufficient explanation. All ten are highly concentrated; seed 20261106 is most concentrated among the supplied examples and favors M1. Other factors remain unresolved. |
| “Capping at 100 or 1,000 fixes negative rankings.” | Recalculated capped fixed-loss means | V | False. Both negative seeds remain negative under both caps. This does not prove that retraining with different weights would fail; no such training was performed. |
| “M1 retained iterations are much lower in the two negative partitions than in the inspected positive control.” | All-candidate records and inspected selection summaries | V | Survives descriptively. M1 best iterations span 1–5 and 3–9, versus 169–200 in the positive control. This identifies a pattern in validation selection, not its cause or a systematic rule for every positive partition. |
| “Only 45.24% favor M1 in 20261101; 53.83% in 20261102.” | Workload loss tables | V | Survives: 45.2434% and 53.8265%, with ties included in the denominator and not counted as wins. A majority-win count and a macro-average improvement are different summaries. |
| “The 101–1,000 execution band contributes heavily to losses.” | Workload-frequency bands | V | Survives. Signed M0−M1 sums are −26,439.874 and −7,334.051. In 20261101 the >1,000 band contributes +9,589.006, offsetting losses. These are attribution identities, not causal frequency effects. |
| “Conditional duration distribution shift is established.” | Partition profiles, means, residuals and selection behavior | R/V but not identifying | Unsupported as a specific mechanism. Different workload mixtures can change coarse conditional summaries; unobserved configuration differences remain. A selected-model error change is not itself proof of conditional target shift. |
| “The field is certified available before scheduling.” | ASI paper §3.1, public schema, historical audit | Partial documentation only | Plausible for user-provided job/model metadata, but not fully certified for each released normalized field at each historical decision time. GPU specification is particularly ambiguous between requested and assigned hardware. |
| “Historical tests were never touched.” | Exp3 preregistration versus historical completed checkpoint | Conflicting scope if phrased globally | Use precise language: Exp3 says historical test outcomes were excluded/not opened, and this audit did not evaluate them. Exp1's completed checkpoint already contains historical test evaluations. Global never-used language is incorrect. |
| “Better LogMAE implies better scheduling.” | No scheduler result for these experiments | Absent | Rejected. Neither aggregate prediction error nor macro loss implies queue-time, completion-time, utilization, backfilling or fairness gains. |
| “The combined project is a major new methodology.” | Three-experiment progression plus literature | Inference | Not established. More diagnostics do not automatically accumulate into a novel general method. The empirical case may still be useful under narrow positioning. |

### Experiment 1: fairness and effect size

Exact principal M0: gpu_request, gpu_spec_public, priority_class, model_type_public, is_genai_request. M1 adds job_type_public. R+P removes the last two application controls; the lifecycle counterpart then adds job type. Resource-only is a different weaker comparison, with historically reported gains around 10.7–11.2%.

The archived grid and selection budgets are matched. That is a defensible comparison of two feature-conditioned learning pipelines. Separately selected models do not isolate an information-theoretic value of the new field. Adding a feature also changes feature subsampling when feature_fraction=0.8 and changes possible tree partitions. Matching a numerical hyperparameter grid does not make all stochastic or representational choices identical.

The inspected Experiment 1 aggregate file explicitly reports historical **test** metrics, whereas Experiment 2's +2.084%/−4.907% and Experiment 3's table report **selected-validation** metrics. These are different evaluation sets and selection relationships. Do not narrate 1.05% → 2.084% → the ten-seed mean as a directly comparable progression of effect sizes.

Historical primary intervals include zero; finite-only point gains are below 1%. The completed checkpoint also records worse original-hour MAE for the broad principal models. These are existing historical aggregate statements, not newly evaluated holdout outcomes. They prevent presenting the original finding as a stable large benefit or a universal null.

### Experiment 2: precisely what the influential workloads establish

The saved reports independently document whole-workload counts of **76,375** across two short online workloads. The broader online/XPU-E/cv cell has **76,368** rows across three workloads, versus six training rows from three other workloads. The request's **76,366** is apparently a narrower full-profile count, but its exact provenance was not found.

These numbers must not be interchanged. Whole workload, coarse feature cell, and exact six-feature profile use different denominators.

The phase-one report records that M1 lowers the two complete workloads' aggregate absolute error by 21,522.235, a beneficial global contribution around 0.028587 LogMAE. Thus a concentration-related duration shift can coexist with improvement on those workloads. The supplied within-M1 190-versus-5 comparison, if verified, addresses a different question.

Comparing saved predictors on records common to both validation sets in the historical phase-one report also shows changed predictor behavior. That rules out explaining the whole observed change solely by the composition of those common evaluated records. It still does not isolate training composition, hyperparameters, or stopping as the mechanism.

### Experiment 3: what the validation reuse means

Validation labels select both the retained iteration and the candidate. Reporting on those labels is expected to be optimistic for selected model performance. Equal candidate budgets are a fairness strength, but do not guarantee equal selection optimism for M0 and M1, or remove bias from their difference. The magnitude and sign of that differential bias were not estimated. [Cawley & Talbot](https://www.jmlr.org/papers/v11/cawley10a.html)

That does not make Exp3 worthless. It is legitimate to study how a specified selection procedure behaves on its selection data. It becomes overclaiming when those same numbers are described as independently validated generalization gains. Macro evaluation uses the same selected models and outcomes; it is less directly optimized than the primary metric, but not a fresh holdout.

## Methodological findings across the 13 required dimensions

### 1. Dataset provenance and unit of analysis

The official release describes execution-summary rows as **pod/workload execution spans** and duration as derived from observed samples. Multiple pods can share workload IDs. The ASI paper distinguishes submitted jobs, tasks and pod instances. Therefore “individual completed GPU job runtime,” “pure GPU compute duration,” and the released target are not interchangeable. [Official schema](https://raw.githubusercontent.com/alibaba/clusterdata/master/cluster-trace-gpu-v2026/docs/schema.md)

This audit did not establish observation-window censoring, time resolution, repeated-pod segmentation, failure/preemption termination semantics or whole-job aggregation. These are major limitations for operational interpretation. They do not prevent an honest study of the released duration target.

The historical source audit reports 40,522,321 execution-summary rows, whereas the original primary population is 4,709,624. Requiring non-null workload identity and four recognized types selects a small, metadata-rich subset. Exp3 further restricts to 3,372,430 executions/341,617 workloads. Its conclusions must not be generalized to all ASI records or the full fleet.

### 2. Identity and group-disjoint split integrity

Historical verification reports zero workload overlap and checked SHA-256 split membership. Exp3 registration references source/split-map hashes and derives an exclusion union of 131,648 workloads: 70,705 + 71,500 − 10,557.

The ten validation loss tables contain one unique row per workload and positive execution counts; aggregate counts match summaries. That does not independently prove train/validation disjointness, because training membership and split maps were not reopened for all ten seeds.

A stable owner/workload ID need not equal an exact configuration, user, tenant or semantic application family. Related variants can remain across the split, while different pods of one logical workload are grouped. The valid claim is transfer to held-out released workload IDs under this grouping rule, not complete removal of all related-workload information.

### 3–4. Feature availability, leakage and proxy concerns

| Predictor | Evidence of plausible prospective meaning | Unresolved qualification |
|---|---|---|
| gpu_request | Resource request is a natural submission-time field. | Need assurance that the released span value is the initial request, rather than a later changed/aggregated value. |
| priority_class | ASI documents user-specified priorities. | Public mapping and time of snapshot should be traced. |
| job_type_public | Paper describes user-provided application metadata. | Exact normalization, enrichment timing, edits and absence of outcome-based rules are not fully audited. |
| model_type_public | Coarse model/application metadata is documented. | Public rule construction and initial availability require provenance. |
| is_genai_request | Schema says request matches public GenAI detection rules. | Rule inputs and timing need certification; overlap with model_type is legitimate redundancy, not automatically leakage. |
| gpu_spec_public | A known requested GPU type could be legitimate. | Schema calls it a GPU model bucket, also exposed with hosting server facts. Assigned hardware may be unavailable before placement. Before scheduling and before execution are different prediction times. |

No direct target field, delays, ready/status fields, utilization, server ID or pod ID appears in the principal feature lists. Train-only categorical vocabularies reduce preprocessing leakage. These are real strengths.

“Proxy leakage” should not be used as a synonym for a useful correlated predictor. Model/type redundancy is not leakage unless its construction uses unavailable information. Conversely, a retrospective field may be leakage even if its column name sounds prospective. The audit found incomplete certification, not proof that the current experiment leaked.

### 5. Separation and restricted-population interpretation

Excluding both historical test-ID sets is a sensible contamination precaution for Exp3. The registration says it selected eligible rows before returning features/outcomes and did not open historical test files. This audit verified the saved policy, not process-level proof that no historical access ever occurred.

The restriction changes the sampled population. Exp3 is a new restricted-population robustness study, not a direct full-population replication of Exp1/2. Its available rows may also have informed earlier development as historical training/validation data. New seeds and a frozen grid do not erase that research history.

### 6. Selection fairness and stopping

All 240 outcomes exist in the consolidated report, with matched grid/budgets, fixed model seed, common objectives and 200-round cap. Winner reconstruction passes.

The reported ranges are **best retained iterations**, not necessarily iterations attempted. With patience 30, a best iteration of one ordinarily entails additional rounds before the lack of improvement triggers stopping. A best retained iteration of 200 establishes reaching the imposed cap; near-cap retained iterations may be cap-limited, but attempted-round records were not recovered. Performance beyond the cap is unknown. [Official early-stopping behavior](https://lightgbm.readthedocs.io/en/stable/pythonapi/lightgbm.early_stopping.html)

Absence of saved per-round curves limits explanation. It does not license regenerating them under this audit. “Partition-dependent selected complexity” is supported; “early stopping is broken” or “causes the reversal” is not.

### 7. Metrics and aggregation

Let S_mg be model m's sum of absolute errors on predicted log1p(hours), n_g its execution count, N total rows, and G workload count.

- Execution loss: sum_g S_mg / N.
- Equal-workload loss: sum_g (S_mg / n_g) / G.
- Cap-c workload loss: sum_g min(n_g,c)(S_mg/n_g) / sum_g min(n_g,c).
- Relative M1 improvement: 100(L0−L1)/L0.

All ten primary/macro calculations reconcile. Signed contributions must add before normalization; positive and negative terms can cancel. Contributions greater than 100% of a signed net are possible and not probabilities.

Log1p(hours) error is unit dependent near zero. A 2% reduction in that loss is not 2% lower duration error, runtime, cost or completion time. Execution weighting is also not GPU-hour weighting, and equal-workload weighting is not user fairness.

For top-1% diagnostics, choose ceil(0.01G), specify the tie breaker, and keep the same selected set for share and loss calculations. In 20261101, a deterministic workload-ID tie rule gives **−11,929.751** top-group and **−12,459.704** remainder, matching the request. The saved SUMMARY instead reports **−12,004.268** for the top-group contribution while reporting the same execution share. Equal-frequency boundary ties can change the chosen members without changing that share. This is consistent with tie-order differences; the exact original ordering implementation was not located. It does not affect primary losses or the conclusion that both portions favor M0, but the manuscript should resolve the reporting definition.

### 8–9. Dependence and effect sizes

Ten overlapping partitions share much of the same finite trace, so their win counts are descriptive sensitivity evidence. They are not ten independent datasets or ten confirmatory replications. Their observed range is not a confidence interval.

Millions of rows do not create millions of independent workload-level observations. Conversely, a workload-level bootstrap conditional on saved predictors would not incorporate retraining, selection and research-design uncertainty. The existing Exp2 conditional intervals must retain that qualification.

The nested information sets are another important limit: an ideal predictor with access to M1's features could ignore job type. In an unrestricted population-risk sense, adding information cannot force an increased optimal loss. An empirical M1 loss identifies limitations of this finite learning/selection pipeline, not “negative information” intrinsic to lifecycle metadata.

### 10–11. Reproducibility and analysis status

Strengths include saved candidates/selections, category mappings, hashes, paired workload loss sums, explicit seed lists and clear warnings in the report. They are better than an unauditable single-score comparison.

The audit package preserves source links, extracted summaries and arithmetic checks. It does not reproduce fitting or certify complete release/source lineage. Original model/candidate binaries and runner code were not all hash-checked against a fully reconstructed execution environment. Registration contains runner/source hashes but hashing an unavailable implementation is not inspecting it.

The ten seeds, grid, execution-weighted selection and macro evaluation are documented in the registration. Capped evaluations, targeted negative seeds, control choice, frequency bands and detailed workload diagnostics are exploratory unless a separate earlier frozen plan proves otherwise. Being read-only or arithmetically correct does not make an analysis preregistered.

### 12. Concentration and distribution-shift claims

Top-1% shares range from 58.519% to 68.334%. This is a verified concentration fact, not an identified cause of failures.

The negative partitions have different patterns. In 20261101, even equal-workload loss is worse and only 45.24% of workload IDs improve. In 20261102, 53.83% improve and macro loss improves, while high-frequency losses outweigh these gains under execution weighting. Both remain negative under caps 100 and 1,000. In 20261106 every examined frequency band favors M1 despite high concentration.

This supports an exact accounting explanation for aggregate signs and an association between partition and selected models. It does not identify a causal concentration effect or conditional distribution-shift mechanism. Broad high-concentration characterizations cannot determine the sign of paired predictive value.

### 13. Scheduling relevance

No scheduling benefit is established. Prediction errors are symmetric in log space here; scheduler costs can be asymmetric, resource weighted, deadline dependent and sensitive to arrival order or interference. Even correct duration prediction may be irrelevant for an online service with administratively determined lifetime.

This is a limit on claims, not a request to run simulation or pivot the research. The manuscript can remain an offline evaluation case study and state that scheduling outcomes are outside its evidence.

## D. Ranked critical weaknesses

| Severity | Weakness | Consequence under the current evidence |
|---|---|---|
| **Fatal to broad claims** | Treating selected-validation scores as independent generalization confirmation | Cannot publish “robust predictive improvement on unseen future jobs” from Exp3. Descriptive selection sensitivity remains valid. |
| **Fatal to causal claims** | Assigning concentration, two workloads, or early stopping as the cause of M0/M1 reversal | Existing comparisons do not identify the cause; influential workloads can actually favor M1. |
| **Fatal to scheduling claims** | No downstream operational result for the compared predictors | No claims of utilization, queue-time, completion-time, safety or fairness improvement. |
| **Major** | Limited distinctive novelty relative to ATLAS, TARE, Weng, Menear and established evaluation literature | The project is currently a trace-specific empirical extension. Three experiments do not by themselves establish a new general methodology. |
| **Major** | Target and prediction-time provenance incomplete | Operational pre-scheduling interpretation is not fully certified; use released execution-span terminology. |
| **Major** | Single source system, selected identity-rich population and restricted Exp3 population | External validity is narrow, despite the large row count. |
| **Major** | Dependence, selection reuse and post-hoc diagnostic search | Naive significance and mechanism claims are invalid. |
| **Moderate** | Incomplete audit of raw split lineage, all model binaries, and unavailable precise within-M1 attribution source | Qualify verified scope; do not claim full computational replication. |
| **Moderate** | No loss curves; retained rounds conflated with rounds attempted; cap reached | Selection-behavior diagnosis is incomplete. |
| **Moderate** | Coarse controls and missing planned scope/user/history | “Beyond available controls” is valid; “independent of all conventional information” is not. |
| **Minor to moderate** | Top-1% ties and mixed profile/workload denominators | Exact attribution claims can drift while aggregate metrics stay correct. |
| **Minor** | Mean signed loss difference called “mean absolute difference”; model seeds described as replications | Correct terminology and restore all per-seed values. |

No verified evidence requires discarding the entire dataset or declaring all results invalid. The fatal items apply to particular expansive claims; they are avoidable by narrowing the manuscript.

## E. Publication positioning

These are reviewer judgments about the current evidence, not acceptance probabilities or claims about future calls.

| Venue category | Realistic assessment |
|---|---|
| OSDI / NSDI / EuroSys main track | Not competitive as presented. No new system, demonstrated operational improvement, or sufficiently broad/decisive measurement result. |
| MLSys main track | Weak fit currently: no new learning method, benchmark standard established across settings, or major generalizable failure established independently. |
| SoCC / HPDC / SC main track | Still a substantial bar. A one-trace selected-validation case study with an unresolved mechanism is unlikely to carry a full paper. |
| Systems/HPC/ML-systems workshop, short empirical or reproducibility track | Plausible if the scoped case study and artifact are the contribution. Acceptance still depends on whether the observed interaction is insightful beyond applying known cautions. |
| Technical report / thesis chapter / negative-result record | Appropriate now, with exact provenance and limitations. This is the lowest-risk way to preserve the completed scientific work without inflating novelty. |

Do not market the work as an alternative to ATLAS or a refutation of TARE. ATLAS studies a different trace/benchmark; TARE's resource weighting and your workload-frequency weighting target different quantities. Neither can be “invalidated” by your sign reversal.

## F. Strongest defensible contribution statement

> We present a trace-specific audit of incremental workload-type metadata in Alibaba ASI execution-duration prediction. Using matched LightGBM search budgets and a documented ten-partition workload-ID-disjoint validation study on a restricted population, we find that the selected-model comparison varies across partitions and evaluation units. M1 improves execution-weighted validation LogMAE in eight partitions and equal-workload LogMAE in nine, with one ranking reversal under reweighting. Saved workload-level loss decompositions show distinct failure patterns and demonstrate that high execution-frequency concentration alone does not determine the sign of the comparison. Candidate records associate negative partitions with much shorter retained M1 models. These results characterize the behavior of this prediction and validation-selection pipeline; they do not establish a causal mechanism, independent test-set improvement, or downstream scheduling benefit.

This is scientifically defensible but deliberately does not assert “first,” “general,” or “new methodology.” Historical Exp1 and Exp2 supply context and supporting examples; they are not independent confirmations of this statement.

## G. Final recommendation

**Write a narrowly scoped empirical manuscript or technical report. Do not submit the current broad framing to a major systems conference.**

Keep the project together: baseline strengthening, the two-partition sign reversal, the ten-partition restricted study, and the reconciled workload attribution form one coherent investigation. A sequence of negative or unstable findings can be worth publishing; the worth depends on the lesson being precise, credible and distinct from already-known advice.

Before circulation, the required work is primarily documentary: state the actual target and prediction time, separate historical test results from selected-validation results, make all population transitions explicit, label exploratory diagnostics, fix the top-1% tie rule, and attach the missing source for the precise within-M1 decomposition or omit its numerical claim. These actions do not require retraining, changing the protocol or opening reserved holdouts.

The research currently demonstrates **a bounded evaluation-sensitivity case**, not a general explanation of GPU runtime prediction instability. If a publishable outcome must mean a top-tier full paper from the current evidence alone, the honest answer is **no**. If a rigorous empirical/workshop contribution is acceptable, the answer is **possibly, under the narrower statement above**. More experiments have not been prescribed or performed by this audit.

## Audit files

- artifact-evidence.json — extracted registration, seed summaries and Drive source locations.
- selection-and-hash-checks.json — candidate-winner consistency checks and original summary commit hashes.
- arithmetic-verification.json — reconstructed micro/macro/capped losses, workload win rates, deterministic top-1% contributions and frequency bands.
- verify_saved_validation_sums.py — arithmetic-only inspection script; inputs are the ten saved validation loss-sum Parquets, never raw holdouts. A temporary DuckDB reader was used for this audit; it is not the scientific training environment.

Literature access limitations are stated per source. This is a thorough bounded search, not a proof of exhaustive prior-art clearance.

