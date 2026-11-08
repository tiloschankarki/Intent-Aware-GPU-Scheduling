# ASI instability diagnosis and one additive mitigation

Exploratory experiment. The one prespecified mitigation **did not meet** the point-estimate success rule. Its mechanism remains **unresolved causally**; the descriptive evidence below supports a role for execution concentration and within-type heterogeneity but does not identify their causal contribution.

## Scope and integrity

Only the two identified training and validation datasets were read. No test dataset, prediction, or evaluation was opened. No archive script was executed or imported. Selected archived source code was inspected as text to reproduce encoding/training semantics. Source archive and completed experiments were not modified. File-name inventories can contain test paths; those entries were not opened.

Exact input paths, SHA-256 hashes, counts, categorical mappings, feature orders, model selection parameters, software versions, output hashes and stages appear in run_manifest.json and phase_a_verification.json. Original saved model artifacts are selectively recovered in artifacts/20260927 and artifacts/20261020. Hash checks establish consistency with local inventories/freeze files, not independent authentication of archival claims.

The original model binding canonical_dataset_sha256 is the digest of the canonical file inventory, not the physical Parquet digest. The file inventory resolves to the recovered canonical object 10a3a86c977701c3c26f0bdce231aeb294676d71fef772b96309ceab3d21b0a0. Its compact sorted-JSON inventory digest is 5116073f80325cfed8f0afc80d7b4a2dd8309b4d8129188ad254bb627d5a4c5a. These differing hashes are consistent, not a data mismatch.

## Main result

The correction worsened execution-weighted validation LogMAE by **4.981%** on the original split and **12.463%** on the second split, while improving equal-workload LogMAE by **1.969%** and **3.267%**, respectively. This is a weighting tradeoff, not a successful stabilization without baseline damage. Conditional workload-bootstrap intervals exclude zero for all four correction-versus-M0 changes. No alternate correction was fitted.

## Phase A: original baseline reproduction

| split_seed | model | trees | recorded_LogMAE | reproduced_LogMAE | difference |
| --- | --- | --- | --- | --- | --- |
| 20260927 | m0 | 94 | 0.776974 | 0.776974 | -0.000000 |
| 20260927 | m1 | 190 | 0.760785 | 0.760785 | -0.000000 |
| 20261020 | m0 | 141 | 0.785266 | 0.785266 | 0.000000 |
| 20261020 | m1 | 5 | 0.823796 | 0.823796 | 0.000000 |

Validation scores reproduce within 1e-10. Native categorical mappings, unknown/missing code -1, fixed feature order and all saved tree counts were checked. LightGBM is exactly 4.7.0 in both archived environments and the local environment. The original environment was Windows/Python 3.12.10 and the second Colab environment Linux/Python 3.13.16; the current environment is recorded separately. No new baseline was substituted.

- Seed 20260927: training 3,339,542 rows / 331,486 workloads; validation 658,761 rows / 71,074 workloads; workload overlap 0.
- Seed 20261020: training 3,223,597 rows / 330,836 workloads; validation 752,865 rows / 70,929 workloads; workload overlap 0.

## Phase B: distribution and concentration evidence

All durations below are log1p(hours). Execution weighting gives every execution one vote. Equal-workload weighting first averages inside each workload, then averages workloads. Workload-mean quantiles expose heterogeneity that one type-wide mean hides.

| split_seed | partition | job_type | execution_mean_log_duration | equal_workload_mean_log_duration | execution_median | execution_q90 | workload_mean_q10 | workload_mean_q90 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20260927 | train | training | 1.067654 | 0.873197 | 0.693147 | 2.434588 | 0.069733 | 2.323731 |
| 20260927 | train | online_inference | 2.020626 | 2.268233 | 1.003487 | 5.695190 | 0.100348 | 4.976859 |
| 20260927 | train | offline_inference | 0.584473 | 0.665875 | 0.316431 | 1.609438 | 0.021979 | 1.834358 |
| 20260927 | train | dev | 2.668332 | 2.462424 | 2.544659 | 5.496763 | 0.149377 | 4.763032 |
| 20260927 | validation | training | 1.071925 | 0.873571 | 0.693147 | 2.470451 | 0.069733 | 2.316398 |
| 20260927 | validation | online_inference | 2.120042 | 2.269223 | 1.467618 | 5.531735 | 0.100348 | 4.976910 |
| 20260927 | validation | offline_inference | 0.568414 | 0.653063 | 0.287682 | 1.688454 | 0.021979 | 1.837016 |
| 20260927 | validation | dev | 1.993785 | 2.487400 | 1.389760 | 5.202143 | 0.134919 | 4.730027 |
| 20261020 | train | training | 1.067721 | 0.874337 | 0.693147 | 2.456736 | 0.069733 | 2.323654 |
| 20261020 | train | online_inference | 2.198889 | 2.262834 | 1.314321 | 5.838943 | 0.095310 | 4.955174 |
| 20261020 | train | offline_inference | 0.572232 | 0.661393 | 0.304211 | 1.609438 | 0.021979 | 1.833732 |
| 20261020 | train | dev | 2.366042 | 2.478722 | 2.356126 | 5.406474 | 0.144581 | 4.751608 |
| 20261020 | validation | training | 1.089979 | 0.875724 | 0.723245 | 2.449088 | 0.069733 | 2.334641 |
| 20261020 | validation | online_inference | 1.350214 | 2.293845 | 0.038152 | 4.795791 | 0.100348 | 5.023069 |
| 20261020 | validation | offline_inference | 0.533732 | 0.663716 | 0.218689 | 1.589235 | 0.021979 | 1.833470 |
| 20261020 | validation | dev | 2.570564 | 2.457134 | 2.487219 | 5.529374 | 0.144581 | 4.742987 |

Execution concentration shares below range from 0 to 1. The top 1% uses ceil(0.01 × type-specific workload count). These are descriptive summaries, not an outlier deletion rule.

| split_seed | partition | job_type | rows | workloads | top_1pct_workload_execution_share | top_10_workload_execution_share | max_workload_executions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20260927 | train | training | 2091126 | 188092 | 0.538902 | 0.031444 | 10989 |
| 20260927 | train | online_inference | 465571 | 29000 | 0.755749 | 0.359110 | 38159 |
| 20260927 | train | offline_inference | 764755 | 106113 | 0.792309 | 0.182834 | 20397 |
| 20260927 | train | dev | 18090 | 9355 | 0.135379 | 0.042399 | 148 |
| 20260927 | validation | training | 426146 | 40459 | 0.520814 | 0.075397 | 4466 |
| 20260927 | validation | online_inference | 95598 | 6186 | 0.748426 | 0.551654 | 17267 |
| 20260927 | validation | offline_inference | 131683 | 22634 | 0.748905 | 0.401115 | 22903 |
| 20260927 | validation | dev | 5334 | 2027 | 0.367079 | 0.332583 | 1302 |
| 20261020 | train | training | 2053504 | 187968 | 0.532696 | 0.027774 | 8843 |
| 20261020 | train | online_inference | 402542 | 28877 | 0.715125 | 0.271619 | 30758 |
| 20261020 | train | offline_inference | 746545 | 105701 | 0.787667 | 0.179445 | 22903 |
| 20261020 | train | dev | 21006 | 9393 | 0.250738 | 0.162287 | 1302 |
| 20261020 | validation | training | 447930 | 40344 | 0.524142 | 0.076876 | 5997 |
| 20261020 | validation | online_inference | 154340 | 6174 | 0.838921 | 0.696022 | 38216 |
| 20261020 | validation | offline_inference | 146669 | 22646 | 0.771888 | 0.408266 | 18244 |
| 20261020 | validation | dev | 3926 | 1985 | 0.151554 | 0.120988 | 244 |

On the second split, online-inference execution-weighted mean log-duration fell from **2.198889** in training to **1.350214** in validation, while equal-workload means were **2.262834** and **2.293845**. Its top ten workloads accounted for **27.162%** and **69.602%** of executions, respectively; the execution median fell from **1.314321** to **0.038152**. This directly supports a concentration/composition account for the marginal mean discrepancy, but not a causal account of model failure.

Offline-inference mean log-duration was **0.572232 → 0.533732** under execution weighting and **0.661393 → 0.663716** under equal-workload weighting. Nevertheless, it accounts for **59.281%** of M1 excess validation absolute-error sum; online inference accounts for **13.687%**. Stable marginal means therefore do not imply stable predictive difficulty. Its top-ten execution share also changed from **17.945%** to **40.827%**.

Second-split M1 excess error decomposition (negative improvement means M1 is worse):

| job_type | m1_absolute_improvement_vs_m0 | m1_excess_error_share |
| --- | --- | --- |
| training | -0.013863 | 0.214070 |
| online_inference | -0.025724 | 0.136867 |
| offline_inference | -0.117245 | 0.592811 |
| dev | -0.415635 | 0.056253 |

A type can have nearly unchanged average log-duration and still produce higher prediction error: its conditional feature–duration relationship, tails, workload composition, or model fit can differ. A marginal mean is not sufficient evidence for conditional stability. Online-inference concentration therefore cannot explain away offline-inference deterioration. The selected M1 also changes from 190 trees on the first partition to five on the second, while M0 changes from 94 to 141. This changes model capacity along with partition composition; the present comparisons cannot separate those effects.

## Phase C: frozen single mitigation

Prediction = saved M0 prediction + type correction. The detailed frozen formula, exact hash folds, seeds and shrinkage are in mitigation_protocol.md. Three outer workload folds provide strict out-of-fold training residuals. Inner workload holdouts alone select stopping iterations; each outer fit is then refit on its full outer-training set. Neither the held-out outer targets nor validation targets enter correction fitting. Every training row has exactly one finite OOF prediction.

Per type, use the equal-workload-weighted median OOF residual and multiply it by n/(n+1000), with n distinct type-specific training workloads. This fixed heuristic does not minimize validation error and was not changed after results. A single type shift cannot adjust interactions with GPU/model/resource features.

| split_seed | job_type | workloads | weighted_median | shrinkage | correction |
| --- | --- | --- | --- | --- | --- |
| 20260927 | training | 188092 | -0.200623 | 0.994712 | -0.199562 |
| 20260927 | online_inference | 29000 | 0.326417 | 0.966667 | 0.315536 |
| 20260927 | offline_inference | 106113 | -0.120776 | 0.990664 | -0.119649 |
| 20260927 | dev | 9355 | 0.161583 | 0.903428 | 0.145978 |
| 20261020 | training | 187968 | -0.245478 | 0.994708 | -0.244179 |
| 20261020 | online_inference | 28877 | 0.579270 | 0.966529 | 0.559882 |
| 20261020 | offline_inference | 105701 | -0.183496 | 0.990628 | -0.181776 |
| 20261020 | dev | 9393 | 0.372553 | 0.903781 | 0.336706 |

Fold-specific rounds (no new hyperparameter search):

| split_seed | fold | inner_train_rows | inner_stop_rows | outer_fit_rows | outer_hold_rows | selected_rounds | seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20260927 | 0 | 1858106 | 347781 | 2205887 | 1133655 | 114 | 37.352045 |
| 20260927 | 1 | 1926208 | 372865 | 2299073 | 1040469 | 44 | 22.553447 |
| 20260927 | 2 | 1826524 | 347600 | 2174124 | 1165418 | 63 | 25.208193 |
| 20261020 | 0 | 1838847 | 305139 | 2143986 | 1079611 | 181 | 39.669655 |
| 20261020 | 1 | 1875978 | 333158 | 2209136 | 1014461 | 84 | 24.907511 |
| 20261020 | 2 | 1768839 | 325233 | 2094072 | 1129525 | 200 | 38.923349 |

Saved original M0 models remain the baselines applied at validation. Fold models necessarily train on fewer workloads and use inner stopping; their iteration counts can differ from the saved full-training M0. Original fixed hyperparameters were historically chosen using validation, so this procedure is not independent validation of the entire original selection pipeline.

## Validation results

Positive absolute/relative improvement means lower MAE than M0. Zero is the M0 reference. Both weighting schemes use the same prediction vectors.

| split_seed | weighting | model | log_mae | absolute_improvement_vs_m0 | relative_improvement_vs_m0_percent |
| --- | --- | --- | --- | --- | --- |
| 20260927 | execution | m0 | 0.776974 | 0.000000 | 0.000000 |
| 20260927 | execution | m1 | 0.760785 | 0.016189 | 2.083576 |
| 20260927 | execution | additive | 0.815676 | -0.038702 | -4.981158 |
| 20260927 | equal_workload | m0 | 0.769928 | 0.000000 | 0.000000 |
| 20260927 | equal_workload | m1 | 0.741714 | 0.028214 | 3.664494 |
| 20260927 | equal_workload | additive | 0.754766 | 0.015161 | 1.969170 |
| 20261020 | execution | m0 | 0.785266 | 0.000000 | 0.000000 |
| 20261020 | execution | m1 | 0.823796 | -0.038530 | -4.906626 |
| 20261020 | execution | additive | 0.883133 | -0.097868 | -12.462993 |
| 20261020 | equal_workload | m0 | 0.791115 | 0.000000 | 0.000000 |
| 20261020 | equal_workload | m1 | 0.812909 | -0.021795 | -2.754915 |
| 20261020 | equal_workload | additive | 0.765271 | 0.025843 | 3.266678 |

The second-split correction produced a 12.463% execution-weighted deterioration (conditional 95% interval: **4.811% to 19.502% deterioration**) and a 3.267% equal-workload improvement (**3.011% to 3.501% improvement**). The M1-versus-M0 second-split execution-weighted interval crosses zero; its observed deterioration should not be presented as precisely estimated under workload resampling.

Paired 95% workload-bootstrap intervals for improvement versus M0:

| split_seed | weighting | model | improvement_ci_low | improvement_ci_high | relative_improvement_ci_low_percent | relative_improvement_ci_high_percent |
| --- | --- | --- | --- | --- | --- | --- |
| 20260927 | execution | m1 | 0.002258 | 0.030465 | 0.290351 | 3.885251 |
| 20260927 | execution | additive | -0.051368 | -0.026553 | -6.737948 | -3.390581 |
| 20260927 | equal_workload | m1 | 0.026268 | 0.030621 | 3.412459 | 3.972501 |
| 20260927 | equal_workload | additive | 0.013852 | 0.016476 | 1.797947 | 2.142283 |
| 20261020 | execution | m1 | -0.084073 | 0.007166 | -11.211773 | 0.884728 |
| 20261020 | execution | additive | -0.159534 | -0.036765 | -19.502087 | -4.811290 |
| 20261020 | equal_workload | m1 | -0.024079 | -0.019457 | -3.041986 | -2.456053 |
| 20261020 | equal_workload | additive | 0.023898 | 0.027693 | 3.011000 | 3.500712 |

1000 workload resamples, seed 20261028. Execution bootstrap metrics use sampled workload error sums divided by sampled execution counts; equal-workload metrics average sampled workload means. The same draws pair all three models. Per-model intervals and comparisons against M1 are in mitigation_results.csv and uncertainty.json. Intervals condition on the fitted models and these partitions; they do not cover fitting/selection uncertainty or generalization to new partition seeds.

The second-split additive correction worsens execution-weighted online-inference error by **20.133%**, training by **8.120%**, and offline inference by **8.372%**, while improving dev by **2.026%**. It improves equal-workload error for all four types on both splits. Thus the aggregate weighting tradeoff is not merely a change in type mixture. The correction deliberately fits equal-workload residuals; shrinkage is weak for common types because n is much larger than 1000. This negative result cannot be generalized to all additive models or stronger shrinkage rules, which were not tried.

Per-type validation results:

| split_seed | weighting | job_type | m0 | m1 | additive | additive_absolute_improvement_vs_m0 | additive_relative_improvement_vs_m0_percent |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20260927 | execution | training | 0.696276 | 0.687666 | 0.728895 | -0.032620 | -4.684859 |
| 20260927 | equal_workload | training | 0.754939 | 0.715317 | 0.738660 | 0.016280 | 2.156413 |
| 20260927 | execution | online_inference | 1.577030 | 1.512187 | 1.641822 | -0.064792 | -4.108478 |
| 20260927 | equal_workload | online_inference | 1.467918 | 1.494881 | 1.445871 | 0.022047 | 1.501915 |
| 20260927 | execution | offline_inference | 0.419527 | 0.414788 | 0.458944 | -0.039417 | -9.395639 |
| 20260927 | equal_workload | offline_inference | 0.552617 | 0.528662 | 0.540796 | 0.011821 | 2.139073 |
| 20260927 | execution | dev | 1.709659 | 1.677280 | 1.749088 | -0.039429 | -2.306242 |
| 20260927 | equal_workload | dev | 1.354896 | 1.331481 | 1.352221 | 0.002675 | 0.197431 |
| 20261020 | execution | training | 0.679711 | 0.693574 | 0.734905 | -0.055194 | -8.120288 |
| 20261020 | equal_workload | training | 0.766733 | 0.734916 | 0.742790 | 0.023944 | 3.122815 |
| 20261020 | execution | online_inference | 1.410245 | 1.435969 | 1.694169 | -0.283923 | -20.132899 |
| 20261020 | equal_workload | online_inference | 1.561660 | 1.767275 | 1.501631 | 0.060029 | 3.843928 |
| 20261020 | execution | offline_inference | 0.428605 | 0.545850 | 0.464489 | -0.035884 | -8.372303 |
| 20261020 | equal_workload | offline_inference | 0.567934 | 0.596712 | 0.549256 | 0.018678 | 3.288844 |
| 20261020 | execution | dev | 1.583274 | 1.998909 | 1.551191 | 0.032083 | 2.026392 |
| 20261020 | equal_workload | dev | 1.421848 | 1.878959 | 1.390583 | 0.031265 | 2.198871 |

## Research assessment

- **Mechanism:** supported descriptively in parts, not established. Execution weighting and workload concentration expose composition sensitivity; offline-inference error and changes in selected model complexity prevent a single-mechanism attribution.
- **Mitigation:** fails the frozen operational rule: improve second-split M0 under both weightings and avoid more than 0.5% original-split degradation under either weighting. This judgment uses point estimates; bootstrap intervals show the precision limits.
- **Paper value:** this extension adds a reproducible bounded comparison and constrains explanations of instability. It does not repair the original paper into a confirmatory test and does not establish a general solution. A negative result is useful as a documented limit of this particular additive correction, not proof that every restricted metadata model fails.
- **Claim boundary:** report these two observed partitions, fixed model seed, selected M0/M1 models and this one frozen shrinkage rule. Do not claim causal identification, novelty, external replication, universal robustness, or fresh held-out confirmation.

## Limitations

- Historical test findings motivated this extension. They were supplied as context and were neither reloaded nor recomputed. Validation already participated in original model selection and later diagnosis.
- The two partitions overlap in the underlying dataset; they are not independent replications and their uncertainty intervals cannot be combined as independent evidence.
- One model seed and two partition seeds do not estimate a distribution of partition sensitivity. The 0.5% materiality boundary and 1000-workload shrinkage are disclosed judgments.
- Marginal duration summaries cannot establish covariate/conditional shift or distinguish it from training randomness, early-stopping effects, selection instability, or misspecification. No causal intervention isolates a mechanism.
- Equal-workload correction fitting targets workload balance; it may hurt execution-weighted performance. Out-of-fold residuals from smaller fitted datasets need not match the saved full-training M0 residual distribution.
- Bootstrap intervals condition on fitted predictors; they exclude training, selection and exploratory design uncertainty. Subgroup comparisons are descriptive and no multiple-testing claims are made.
- The target is the archived duration field. These results do not independently validate duration semantics as pure GPU computation time. No novelty claim or literature review is made.

## Reproduction

Use the saved Python environment versions in run_manifest.json. `phase_a_reproduce.py` reproduces the audit with the original local source paths; `mitigation_experiment.py fit` then `mitigation_experiment.py evaluate` runs the frozen experiment in a clean copy of this directory after removing only generated fit/evaluation outputs in that copy. The scripts intentionally refuse to overwrite existing fit/evaluation results. No source archive changes are needed. Generate the reports and final manifest with `python build_reports.py`. Delivered helper tests run as `python test_mitigation.py`.
