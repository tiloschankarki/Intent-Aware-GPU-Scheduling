# Phase 1: prediction instability in Alibaba ASI GPU workloads

## Scope, verification and central conclusion

The three diagnostic investigations are complete. No models were trained, tuned, optimized or selected. Only the original saved M0/M1 models and allowlisted training/validation data were used. Test partitions, test predictions and test evaluations were not opened. The aborted encoded feasibility file was not used. The prior additive correction was not used as evidence for a mechanism and was not rerun.

**Measured conclusion:** execution weighting is highly concentrated, but the workloads dominating a duration shift are not automatically the workloads on which M1 fails. On the second split, two very short, extremely frequent online-inference workloads materially depress its execution-weighted duration mean while M1 improves on them. Offline-inference deterioration is instead concentrated in high-frequency workloads with XPU-B/unknown-model features and overprediction; longer online-inference populations exhibit underprediction. The same saved-predictor sensitivity also appears on records shared by both validation partitions. These facts localize the failure; they do not establish why the five-tree model was selected or a causal mechanism.

Signed residual = actual log1p(hours) minus prediction: positive means underprediction. Delta error = M1 absolute error minus M0 absolute error: positive means M1 worse. Every normalized net contribution uses the signed global M1−M0 absolute-error sum. Such shares are not probabilities: they can be negative or exceed 100% when beneficial and harmful workloads cancel. Contributions in LogMAE units always divide by the complete validation execution count.

All four original saved predictors reproduce cached validation predictions **exactly row for row** (maximum absolute difference zero). Feature order, categorical mappings, model hashes and 94/190/141/5 tree counts were verified under LightGBM 4.7.0. Dataset SHA-256 hashes match the prior verified bindings; SHA-256 membership was independently recomputed for every unique training/validation workload. Workload overlap and row-ordinal overlap within each seed are zero. Source hashes were rechecked after analysis. Canonical identity was checked by opaque hashing and footer/schema metadata only, with zero canonical scientific rows read.

| seed | partition | rows | workloads |
| --- | --- | --- | --- |
| 20260927 | train | 3339542 | 331486 |
| 20260927 | validation | 658761 | 71074 |
| 20261020 | train | 3223597 | 330836 |
| 20261020 | validation | 752865 | 70929 |

Aggregate validation verification (positive deterioration means worse):

| seed | weighting | M0_LogMAE | M1_LogMAE | M1_minus_M0 | M1_deterioration_percent |
| --- | --- | --- | --- | --- | --- |
| 20260927 | execution | 0.776974 | 0.760785 | -0.016189 | -2.083576 |
| 20260927 | equal_workload | 0.769928 | 0.741714 | -0.028214 | -3.664494 |
| 20261020 | execution | 0.785266 | 0.823796 | 0.038530 | 4.906626 |
| 20261020 | equal_workload | 0.791115 | 0.812909 | 0.021795 | 2.754915 |

## A. Workload concentration

**A small fraction of workloads dominates execution-weighted metrics in both partitions.** The top 1% by frequency covers 62.446% of original validation executions and 65.936% of second-split executions. Top 5% covers 82.959% and 84.989%; top 10% covers 87.211% and 88.787%. Online and offline inference are still more concentrated. Counts use ceil(fraction × scope workloads); ties are broken by workload ID.

| split_seed | scope | fraction_percent | selected_workloads | selected_executions | execution_percent | global_mae_gap_contribution |
| --- | --- | --- | --- | --- | --- | --- |
| 20260927 | ALL | 1.000000 | 711 | 411372 | 62.446320 | -0.006725 |
| 20260927 | ALL | 5.000000 | 3554 | 546501 | 82.958918 | -0.009446 |
| 20260927 | ALL | 10.000000 | 7108 | 574510 | 87.210688 | -0.010964 |
| 20260927 | online_inference | 1.000000 | 62 | 71548 | 74.842570 | -0.006594 |
| 20260927 | online_inference | 5.000000 | 310 | 83380 | 87.219398 | -0.007586 |
| 20260927 | online_inference | 10.000000 | 619 | 86225 | 90.195402 | -0.008103 |
| 20260927 | offline_inference | 1.000000 | 227 | 98618 | 74.890457 | 0.000339 |
| 20260927 | offline_inference | 5.000000 | 1132 | 109768 | 83.357761 | -0.000149 |
| 20260927 | offline_inference | 10.000000 | 2264 | 111313 | 84.531033 | -0.000169 |
| 20261020 | ALL | 1.000000 | 710 | 496410 | 65.936124 | 0.016580 |
| 20261020 | ALL | 5.000000 | 3547 | 639849 | 84.988544 | 0.031162 |
| 20261020 | ALL | 10.000000 | 7093 | 668450 | 88.787498 | 0.034457 |
| 20261020 | online_inference | 1.000000 | 62 | 129479 | 83.892056 | -0.010674 |
| 20261020 | online_inference | 5.000000 | 309 | 142111 | 92.076584 | -0.000828 |
| 20261020 | online_inference | 10.000000 | 618 | 144847 | 93.849294 | 0.000965 |
| 20261020 | offline_inference | 1.000000 | 227 | 113212 | 77.188772 | 0.020772 |
| 20261020 | offline_inference | 5.000000 | 1133 | 124730 | 85.041829 | 0.022064 |
| 20261020 | offline_inference | 10.000000 | 2265 | 126288 | 86.104085 | 0.022012 |

![Workload frequency concentration](workload_frequency_concentration.png)

**Frequency ranking is not error ranking.** The following top-1% rankings use the same number of workloads but different selection rules. Positive-excess share is the fraction of the sum of positive workload-level error differences, not the fraction of a signed net total. Error-ranked groups are selected on observed error and are descriptive.

| split_seed | ranking | selected_workloads | execution_percent | delta_sum | global_net_delta_share | positive_excess_percent |
| --- | --- | --- | --- | --- | --- | --- |
| 20260927 | frequency | 711 | 62.446320 | -4429.868432 | 0.415382 | 40.359017 |
| 20260927 | excess_error | 711 | 17.205329 | 8827.169381 | -0.827709 | 62.778739 |
| 20260927 | absolute_duration_tilt | 711 | 58.388854 | -4212.721761 | 0.395020 | 43.636321 |
| 20261020 | frequency | 710 | 65.936124 | 12482.133786 | 0.430301 | 56.457422 |
| 20261020 | excess_error | 710 | 26.427049 | 65037.926021 | 2.242074 | 77.634581 |
| 20261020 | absolute_duration_tilt | 710 | 61.018642 | 21031.459682 | 0.725024 | 60.823514 |

On the second split, the frequency-top-1% and error-top-1% sets intersect in 259 of 710 workloads (36.479%). The frequency-selected set covers 65.936% of executions but 56.457% of positive workload excess; the error-selected set covers 26.427% of executions and 77.635% of positive excess. Its signed error sum is 224.207% of the net global deterioration because beneficial workloads offset much of the gross worsening. The original split also contains harmful workloads despite an overall improvement.

Within second-split offline inference, 227 frequency-top-1% workloads cover 77.189% of executions and 86.145% of positive workload-level excess error. Frequency/error top-1% overlap is 120/227 (52.863%). For online inference, 62 frequency-top-1% workloads cover 83.892% of executions, but their **net** contribution is beneficial (−0.010674 global LogMAE units); the remaining online workloads reverse that into a positive online total. Overlap by count alone misses this cancellation.

Representative second-split workloads (full IDs; these are cases, not general population claims):

| case | workload_id | executions | mean_log_duration | residual_m0 | residual_m1 | mae_m0 | mae_m1 | delta_sum | global_mae_gap_contribution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Two most frequent online workloads | 587316dd2a861952b26bf344145d646c | 38216 | 0.033267 | -1.065774 | -0.783945 | 1.066128 | 0.784328 | -10769.267549 | -0.014304 |
| Two most frequent online workloads | ad7c4cb4a11306cb7e653e2d96bfd4a0 | 38159 | 0.033831 | -1.065205 | -0.783382 | 1.065556 | 0.783762 | -10752.966965 | -0.014283 |
| Three largest offline error contributors | a7eeffaba10b628c10dc5d2ddfab494c | 18244 | 0.334726 | 0.119735 | -0.271123 | 0.322153 | 0.573995 | 4594.607415 | 0.006103 |
| Three largest offline error contributors | 332d94fec14f56c6576c2df285fec70a | 8089 | 0.086906 | 0.007868 | -0.456900 | 0.069686 | 0.525466 | 3686.805803 | 0.004897 |
| Three largest offline error contributors | 2709af8061a257ca8557709bb74456f0 | 10165 | 0.559022 | 0.341235 | -0.047636 | 0.494848 | 0.656661 | 1644.832711 | 0.002185 |

The three listed offline workloads account for 57.723% of net offline excess and 34.219% of net global excess. A workload may have multiple observed GPU/feature values; the detailed per-workload mixtures are in influential_workload_feature_profiles.csv, rather than assigning every execution its modal feature.

The required workload_error_attribution.csv contains each workload’s execution count, actual mean/median log-duration, M0/M1 mean signed residuals and MAE, mean/summed delta, frequency and excess ranks, and normalized contributions. ALL and type-specific scopes are separate analyses: do not sum duplicate scopes. Some workloads contain multiple types, so type workload counts need not add to the overall unique workload count.

## B. Prediction failure by type and observed features

All six single-feature tables and all 15 two-way families retain every observed category, including sparse groups. Three semantic three-way families were selected before inspecting their errors. Headline comparisons require at least 1000 executions and 50 distinct workloads, with support in both validation partitions for cross-split comparisons. These thresholds bound descriptive reliability; they do not confer statistical significance.

| split_seed | job_type_public | executions | workloads | mae_m0 | mae_m1 | delta_mean | global_mae_gap_contribution | net_delta_percent | residual_m0 | residual_m1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20260927 | online_inference | 95598 | 6186 | 1.577030 | 1.512187 | -0.064844 | -0.009410 | 58.126495 | 0.262364 | 0.031160 |
| 20260927 | training | 426146 | 40459 | 0.696276 | 0.687666 | -0.008610 | -0.005569 | 34.403283 | 0.248273 | 0.250299 |
| 20260927 | offline_inference | 131683 | 22634 | 0.419527 | 0.414788 | -0.004738 | -0.000947 | 5.850745 | 0.214769 | 0.243295 |
| 20260927 | dev | 5334 | 2027 | 1.709659 | 1.677280 | -0.032379 | -0.000262 | 1.619477 | -0.419572 | -0.560793 |
| 20261020 | online_inference | 154340 | 6174 | 1.410245 | 1.435969 | 0.025724 | 0.005273 | 13.686677 | -0.209152 | 0.481150 |
| 20261020 | training | 447930 | 40344 | 0.679711 | 0.693574 | 0.013863 | 0.008248 | 21.406964 | 0.271754 | 0.367983 |
| 20261020 | offline_inference | 146669 | 22646 | 0.428605 | 0.545850 | 0.117245 | 0.022841 | 59.281055 | 0.177350 | -0.081454 |
| 20261020 | dev | 3926 | 1985 | 1.583274 | 1.998909 | 0.415635 | 0.002167 | 5.625304 | 0.448682 | 1.648317 |

![Type-specific contributions to aggregate error difference](workload_type_error_contributions.png)

Offline inference contributes 59.281% of the second split’s net M1 excess; training 21.407%, online inference 13.687%, and dev 5.625%. Every type improves execution-weighted error on the original split and deteriorates on the second. Mean residuals reveal different directions: offline M1 moves from underprediction (+0.177350 M0) to overprediction (−0.081454 M1); online M1 underpredicts (+0.481150), while M0 overpredicts on average (−0.209152). Mean signed residuals can cancel opposite errors, so subgroup detail matters.

Largest supported second-split type×GPU contributions (within this family, cells partition all executions; each listed contribution uses the same global denominator):

| cell | executions | workloads | mae_m0 | mae_m1 | delta_mean | global_mae_gap_contribution | residual_m0 | residual_m1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ["offline_inference","XPU-B"] | 42652 | 234 | 0.261431 | 0.553759 | 0.292328 | 0.016561 | 0.159147 | -0.291344 |
| ["online_inference","XPU-A"] | 11946 | 625 | 1.528299 | 2.538041 | 1.009742 | 0.016022 | 0.109324 | 2.195503 |
| ["training","XPU-E"] | 259893 | 12983 | 0.652326 | 0.672334 | 0.020008 | 0.006907 | 0.231250 | 0.383074 |
| ["online_inference","L20"] | 9221 | 702 | 1.754156 | 2.138807 | 0.384651 | 0.004711 | 0.281542 | 1.918080 |
| ["offline_inference","H20"] | 28905 | 3008 | 0.364673 | 0.466033 | 0.101360 | 0.003892 | 0.133109 | -0.111054 |
| ["online_inference","A10"] | 9076 | 691 | 2.446900 | 2.731106 | 0.284206 | 0.003426 | 1.450514 | 2.364675 |
| ["online_inference","XPU-B"] | 23588 | 314 | 1.632907 | 1.726815 | 0.093908 | 0.002942 | 0.261087 | 1.402992 |
| ["online_inference","XPU-C"] | 3141 | 285 | 1.162010 | 1.852511 | 0.690501 | 0.002881 | -0.125125 | 1.539082 |

Offline-inference/XPU-B contributes +0.016561 global LogMAE, with 42,652 executions and 234 workloads. Its residual shifts from +0.159147 to −0.291344: a mean shift toward overprediction. Online-inference/XPU-A contributes +0.016022 with 11,946 executions and 625 workloads; residual +2.195503 indicates severe mean underprediction. These are different observed populations and error directions. By contrast, online-inference/XPU-E contributes −0.025345, offsetting substantial errors elsewhere.

Other interpretable second-split combinations include online inference with gpu_request=1 (74,350 rows / 5,797 workloads; +0.032967 global LogMAE), online inference with model_type=rec (+0.025224), offline inference with model_type=unknown (+0.022096), and offline inference with priority_class=Other (+0.017985). They overlap with type×GPU cells and **must not be added across families**.

Supported type×GPU patterns compared across partitions:

| cell | executions_20260927 | workloads_20260927 | delta_mean_20260927 | executions_20261020 | workloads_20261020 | delta_mean_20261020 | direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ["offline_inference","XPU-B"] | 13178.000000 | 223.000000 | -0.004466 | 42652.000000 | 234.000000 | 0.292328 | sign_reversal |
| ["online_inference","XPU-A"] | 6209.000000 | 593.000000 | -0.019673 | 11946.000000 | 625.000000 | 1.009742 | sign_reversal |
| ["training","XPU-E"] | 242479.000000 | 13070.000000 | -0.006248 | 259893.000000 | 12983.000000 | 0.020008 | sign_reversal |
| ["online_inference","L20"] | 7493.000000 | 747.000000 | -0.019463 | 9221.000000 | 702.000000 | 0.384651 | sign_reversal |
| ["offline_inference","H20"] | 24377.000000 | 3014.000000 | -0.017242 | 28905.000000 | 3008.000000 | 0.101360 | sign_reversal |
| ["online_inference","A10"] | 20698.000000 | 689.000000 | -0.026998 | 9076.000000 | 691.000000 | 0.284206 | sign_reversal |
| ["online_inference","XPU-B"] | 40201.000000 | 299.000000 | 0.013700 | 23588.000000 | 314.000000 | 0.093908 | M1_worse_both |
| ["online_inference","XPU-C"] | 2741.000000 | 335.000000 | 0.003647 | 3141.000000 | 285.000000 | 0.690501 | M1_worse_both |

The offline-XPU-B and online-XPU-A deterioration patterns reverse sign between splits; they are not stable harmful effects of those features. Some marginal patterns persist: offline/unknown and offline/non-genai are slightly worse on the original split and much worse on the second. Among 342 cross-split-supported cells across overlapping families, 195 reverse sign, 84 are worse on both and 63 are better on both. These counts are descriptive and highly dependent; they are not 342 independent tests.

Selected supported type×GPU×model cells (interpret support carefully):

| cell | executions | workloads | mae_m0 | mae_m1 | delta_mean | global_mae_gap_contribution | residual_m0 | residual_m1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ["offline_inference","XPU-B","unknown"] | 42470 | 52 | 0.261225 | 0.554103 | 0.292878 | 0.016522 | 0.161065 | -0.290599 |
| ["online_inference","XPU-A","rec"] | 8313 | 64 | 1.627015 | 2.796040 | 1.169025 | 0.012908 | -0.136110 | 2.527237 |
| ["training","XPU-E","rec"] | 216211 | 3063 | 0.648967 | 0.671207 | 0.022240 | 0.006387 | 0.253923 | 0.421365 |
| ["online_inference","L20","rec"] | 6768 | 108 | 1.808555 | 2.236682 | 0.428127 | 0.003849 | -0.113415 | 1.997912 |
| ["offline_inference","H20","unknown"] | 24469 | 492 | 0.363753 | 0.477578 | 0.113825 | 0.003699 | 0.184598 | -0.093391 |
| ["online_inference","XPU-B","rec"] | 22140 | 243 | 1.550701 | 1.657047 | 0.106346 | 0.003127 | 0.096493 | 1.324678 |

The offline/XPU-B/unknown cell has only 52 distinct workloads, just above the threshold, despite 42,470 executions. Its +0.016522 global contribution must not be described as evidence from 42,470 independent observations. Similarly online/XPU-A/rec has 8,313 rows but 64 workloads. Three-way cells excluded for insufficient support are summarized in subgroup_coverage.csv. This is consequential: the retained type×GPU×model cells cover only 85.775% of second-split executions and their worsening sum exceeds the global net because the omitted cells are beneficial overall. Sparse cells are not silently discarded from aggregate metrics.

| split_seed | family | retained_cells | execution_coverage | total_delta_sum | retained_delta_sum | omitted_delta_sum |
| --- | --- | --- | --- | --- | --- | --- |
| 20260927 | job_type_public × gpu_spec_public × model_type_public | 40 | 0.963856 | -10664.577874 | -5196.061616 | -5468.516258 |
| 20260927 | job_type_public × gpu_spec_public × gpu_request | 39 | 0.910436 | -10664.577874 | -12035.617275 | 1371.039401 |
| 20260927 | job_type_public × model_type_public × gpu_request | 24 | 0.970643 | -10664.577874 | -12640.420783 | 1975.842909 |
| 20261020 | job_type_public × gpu_spec_public × model_type_public | 40 | 0.857753 | 29007.934364 | 47757.701411 | -18749.767047 |
| 20261020 | job_type_public × gpu_spec_public × gpu_request | 39 | 0.820615 | 29007.934364 | 40330.753238 | -11322.818874 |
| 20261020 | job_type_public × model_type_public × gpu_request | 24 | 0.861521 | 29007.934364 | 45531.434489 | -16523.500125 |

There are zero missing values in the six observed validation analysis features under both seeds. The legitimate model_type_public=unknown category is retained: 125,087 original rows / 9,879 workloads and 139,471 second-split rows / 9,862 workloads. Its overall delta sum changes from +66.315 to +17,981.233. unknown is neither missing data nor a new inferred lifecycle class. Missing/unknown support, including explicit zero missing counts, is saved in missing_unknown_category_support.csv.

## C. Connection between duration shift and prediction deterioration

### Population means and execution-frequency association

For each partition and type, E is the execution-weighted duration mean, W is the equal-workload duration mean and F=E−W. The exact identity is ΔE=ΔW+ΔF. It separates reweighting association from the mean of workload means; it does not by itself identify a causal process. Workload IDs are never matched between training and validation.

| split_seed | scope | execution_mean_train | execution_mean_validation | mu_train | mu_validation | equal_workload_mean_change | frequency_duration_association_component | duration_mean_gap_contribution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20260927 | training | 1.067654 | 1.071925 | 0.873197 | 0.873571 | 0.000375 | 0.003896 | 0.004271 |
| 20260927 | online_inference | 2.020626 | 2.120042 | 2.268233 | 2.269223 | 0.000989 | 0.098427 | 0.099416 |
| 20260927 | offline_inference | 0.584473 | 0.568414 | 0.665875 | 0.653063 | -0.012812 | -0.003246 | -0.016058 |
| 20260927 | dev | 2.668332 | 1.993785 | 2.462424 | 2.487400 | 0.024975 | -0.699523 | -0.674547 |
| 20261020 | training | 1.067721 | 1.089979 | 0.874337 | 0.875724 | 0.001388 | 0.020871 | 0.022259 |
| 20261020 | online_inference | 2.198889 | 1.350214 | 2.262834 | 2.293845 | 0.031011 | -0.879686 | -0.848675 |
| 20261020 | offline_inference | 0.572232 | 0.533732 | 0.661393 | 0.663716 | 0.002324 | -0.040823 | -0.038500 |
| 20261020 | dev | 2.366042 | 2.570564 | 2.478722 | 2.457134 | -0.021588 | 0.226109 | 0.204521 |

Second-split online inference has ΔE=−0.848675, ΔW=+0.031011 and ΔF=−0.879686. Thus the execution mean drops despite a slightly higher equal-workload mean. Offline inference has ΔE=−0.038500, ΔW=+0.002324 and ΔF=−0.040823: a relatively stable marginal duration mean coexists with pronounced prediction deterioration. This rejects the inference that stable means imply stable prediction difficulty.

![Duration mean change decomposition](duration_shift_decomposition.png)

The feature-cell decomposition uses fractional workload mass, allowing a workload to span multiple cells without double-counting its equal-workload weight. Within common cells, ΔW is split symmetrically into observed-cell composition and within-cell duration changes; unmatched cells are explicit. Adding those terms to ΔF reconciles with the overall execution-mean change. This decomposition is repeated separately for each family; families are not additive.

| split_seed | scope | family | equal_workload_composition_component | within_observed_cell_component | unmatched_cell_component | frequency_duration_association_component | duration_mean_gap_contribution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20260927 | online_inference | type × gpu_spec_public × model_type_public | 0.004258 | -0.001149 | -0.002120 | 0.098427 | 0.099416 |
| 20260927 | offline_inference | type × gpu_spec_public × model_type_public | 0.000309 | -0.013108 | -0.000013 | -0.003246 | -0.016058 |
| 20261020 | online_inference | type × gpu_spec_public × model_type_public | 0.050510 | -0.017494 | -0.002004 | -0.879686 | -0.848675 |
| 20261020 | offline_inference | type × gpu_spec_public × model_type_public | -0.001442 | 0.003846 | -0.000080 | -0.040823 | -0.038500 |

For online inference under type×GPU×model stratification, the equal-workload composition term is +0.050510, within-cell change −0.017494, and unmatched-cell contribution −0.002004. They sum to +0.031011, while the frequency term is −0.879686. Coarse observed features do not erase all duration heterogeneity. Within-cell shifts compare different workloads and may reflect unmeasured composition; they are not longitudinal change of the same workload or causal conditional-distribution effects.

### The dominant short online workloads improve, rather than drive, M1 error

The two frequency-leading online workloads contain 76,375 executions (49.485% of online executions). Their mean log-durations are 0.033267 and 0.033831; M1 reduces their total absolute-error sum by 21522.235, a beneficial contribution of -0.028587 global LogMAE. Together, their centered frequency-duration contributions sum to -1.117773, compared with the complete online F of −0.943631. Other workloads offset part of that downward weighting association. These contemporaneous contributions are relative to the validation equal-workload mean, not estimated causal train→validation effects.

Most executions of both workloads are XPU-E, cv, gpu_request=16, HP, non-genai. The complete online/XPU-E/cv cell has 76,368 validation executions but only **three workloads**, versus six training executions from three different workloads. It is an important concentrated case, not a well-supported general interaction. It is deliberately absent from the supported three-way rankings, but fully reported in duration_shift_vs_error.csv and the influential workload profiles:

| cell | executions_train | workloads_train | executions_validation | workloads_validation | execution_mean_train | execution_mean_validation | mae_m0 | mae_m1 | delta_mean | global_error_gap_contribution | supported_both |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ["XPU-E","cv"] | 6.000000 | 3.000000 | 76368.000000 | 3.000000 | 3.441982 | 0.033612 | 1.065876 | 0.784067 | -0.281809 | -0.028586 | False |

A cell’s duration-mass term p×mean duration can be positive even when its short workloads depress the global mean: their increased share dilutes other cells. Accordingly, the supplemental workload influence uses a centered term (n/N−1/W)×(workload mean−W), which sums to F and is invariant to adding a constant to all durations. The initial raw terms and centered terms are retained separately; see supplemental_method_note.md. The two strongest downward centered-duration contributors are exactly the two short workloads on which M1 improves. The leading harmful online workloads instead have much larger mean log-duration (4.700573 and 4.829005) and large positive M1 residuals (3.198704 and 3.327137): underprediction of longer records. Therefore the online shift-driving and error-driving populations overlap imperfectly and can contribute in opposite directions.

Offline inference differs: the three biggest net-error workloads are also its frequency ranks 1, 3 and 2. Their detailed profiles are predominantly XPU-B/unknown/Other/non-genai, with gpu_request 1 or 0.5; feature values are not constant within each workload. For this type, high concentration and error have substantial overlap. The evidence does not support one uniform concentration→failure explanation across workload types.

### Supplemental check on records shared by the two validation partitions

The two validation sets share 10,632 workloads and 100,221 executions. Their source row ordinals, workload IDs, all six observed features and duration targets were verified exactly equal. This matching is **validation to validation only**, never training to validation. Under the original saved pair, M1−M0 MAE on these records is −0.003294; under the second saved pair it is +0.021352. Error changes on identical observed records cannot be attributed solely to the composition of those evaluated records. They reflect changed saved predictors, including all differences in their selected complexity/parameters. They do not identify why those predictors differ.

| scope | shared_workloads | shared_executions | shared_mae_m0_a | shared_mae_m1_a | shared_mae_m0_b | shared_mae_m1_b | shared_delta_change |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ALL | 10632 | 100221 | 0.854011 | 0.850717 | 0.839569 | 0.860921 | 0.024646 |
| training | 6023 | 65379 | 0.708461 | 0.703228 | 0.711324 | 0.727497 | 0.021406 |
| online_inference | 918 | 22436 | 1.471861 | 1.476999 | 1.390298 | 1.422655 | 0.027219 |
| offline_inference | 3429 | 11630 | 0.416331 | 0.405415 | 0.424456 | 0.471044 | 0.057504 |
| dev | 294 | 776 | 1.812826 | 1.843372 | 1.942812 | 1.704090 | -0.269269 |

On shared offline validation executions, M0/M1 MAE changes from 0.416331/0.405415 to 0.424456/0.471044, flipping the M1 difference from −0.010916 to +0.046588. On shared dev records the direction goes the other way, reinforcing that type-level aggregate changes are not universal across records. No subgroup result identifies a causal metadata interaction.

For the overall cross-partition M1−M0 change of +0.054719, the exact descriptive decomposition is −0.000172 from the changed weight of the common subset, +0.003515 from changed predictors on that common subset, and +0.051375 from exclusive validation portions (which mix different records and predictors). The last component must not be labeled a pure composition effect. The shared-record check was added after inspecting the initial tables and is explicitly exploratory.

## D. Evidence strength and unresolved mechanism

Supported measurements: extreme frequency concentration; signed and reconciled workload/type/feature-cell error contributions; opposite over/underprediction directions in important cells; failure of online mean-shift alone to account for deterioration; different predictor behavior on identical shared validation records. The five-tree M1 is an independently reproduced saved artifact, not an identified coding discrepancy.

Tentative interpretations: concentrated execution weighting makes partition summaries and aggregate model comparisons sensitive to which workload populations are present. Changed selected model complexity is consistent with representation/selection sensitivity. Neither claim isolates how training distribution, feature interactions, L1 fitting, early stopping and finite-sample selection produced the observed functions. No intervention or retraining was performed to isolate them.

Uncertainty is conditional, paired workload-cluster resampling (1000 replicates, seed 20261027). Positive percentages below denote M1 deterioration; negative percentages denote improvement. Intervals condition on fixed predictors and observed partition/type memberships. They omit training/selection/design uncertainty, are not multiplicity-adjusted and are not confirmatory tests. Error-selected workload rankings receive no independent inferential claim.

| split_seed | scope | metric | point | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| 20260927 | ALL | execution_deterioration_percent | -2.083576 | -4.089371 | -0.302477 |
| 20260927 | ALL | equal_workload_deterioration_percent | -3.664494 | -3.961778 | -3.394426 |
| 20260927 | training | execution_deterioration_percent | -1.236527 | -1.510713 | -0.946344 |
| 20260927 | training | equal_workload_deterioration_percent | -5.248478 | -5.575566 | -4.922676 |
| 20260927 | online_inference | execution_deterioration_percent | -4.111771 | -10.869726 | 1.437157 |
| 20260927 | online_inference | equal_workload_deterioration_percent | 1.836867 | 0.541765 | 3.005114 |
| 20260927 | offline_inference | execution_deterioration_percent | -1.129446 | -2.090318 | 0.072914 |
| 20260927 | offline_inference | equal_workload_deterioration_percent | -4.334903 | -4.688196 | -3.978316 |
| 20260927 | dev | execution_deterioration_percent | -1.893894 | -5.644764 | 0.003589 |
| 20260927 | dev | equal_workload_deterioration_percent | -1.728221 | -2.818792 | -0.618679 |
| 20261020 | ALL | execution_deterioration_percent | 4.906626 | -0.931480 | 11.349136 |
| 20261020 | ALL | equal_workload_deterioration_percent | 2.754915 | 2.484678 | 3.043885 |
| 20261020 | training | execution_deterioration_percent | 2.039565 | 0.930683 | 3.053113 |
| 20261020 | training | equal_workload_deterioration_percent | -4.149692 | -4.398452 | -3.906353 |
| 20261020 | online_inference | execution_deterioration_percent | 1.824071 | -9.250180 | 22.787676 |
| 20261020 | online_inference | equal_workload_deterioration_percent | 13.166381 | 12.146858 | 14.110027 |
| 20261020 | offline_inference | execution_deterioration_percent | 27.355050 | 12.209587 | 43.468497 |
| 20261020 | offline_inference | equal_workload_deterioration_percent | 5.067116 | 4.638995 | 5.476163 |
| 20261020 | dev | execution_deterioration_percent | 26.251636 | 9.119774 | 40.621870 |
| 20261020 | dev | equal_workload_deterioration_percent | 32.149135 | 28.981892 | 35.280683 |

Second-split overall execution deterioration is +4.907%, with a conditional 95% interval [−0.931%, +11.349%], crossing zero because a few workloads strongly affect the ratio. Equal-workload deterioration is +2.755%, interval [+2.485%, +3.044%]. Online execution deterioration is imprecise (+1.824%, interval [−9.250%, +22.788%]), while online equal-workload deterioration is +13.166%, interval [+12.147%, +14.110%]. Offline deterioration is +27.355% execution-weighted and +5.067% equal-workload. Broad subgroup searches and the overlapping two partitions prevent confirmatory or independent-replication claims.

**Mechanism status: unresolved.** The diagnostics establish locations and arithmetic sources of sensitivity, not the causal reason for training/selection instability. Stable marginal means do not imply stable conditional prediction difficulty. Workload concentration can amplify either benefits or harms. The additive correction’s prior failure supplies no causal explanation here.

## E. Implications for the existing paper

The diagnostics strengthen the fixed research question by replacing a single aggregate sign reversal with auditable workload-level attribution, supported feature-cell localization, weighting decomposition and a shared-validation-record control. A defensible claim is that the predictive value of broad workload-type metadata in these two observed partitions is sensitive to execution weighting, workload composition and the resulting selected predictor functions. The paper should distinguish performance at the execution and workload units, rather than treating one weighting as a universal answer.

The paper cannot claim that online inference causes instability, that a specific GPU/model interaction is causal, that the five-tree selection is itself the established mechanism, that all additive metadata models fail, or that these exploratory diagnostics validate a new mitigation. No mitigation is proposed or run here. job_type_public is broad workload type, not fine-grained lifecycle phase; guaranteed availability before scheduling has not been established. These results therefore do not independently validate use as a deployable scheduling-time input. Duration_hours is the supplied target, not independently verified pure GPU-compute duration. No novelty or external-validity claim is made.

## Reproduction, denominators and files

Run phase1_analysis.py in a fresh copy of this output directory with generated output tables removed from that copy; it refuses to overwrite the workload attribution table. Its input paths are derived from the verified sibling experiment directory and recorded manifests. Then run build_findings.py --calculate and build_findings.py --report. The latter two add explicitly labeled exploratory checks and regenerate this report/manifest. Run test_phase1.py and test_phase1_supplement.py for the deterministic calculation checks. Required scientific dependencies are Python, NumPy, pandas, PyArrow, SciPy, LightGBM 4.7.0 and Matplotlib, with exact versions/source paths recorded in run_manifest.json. No archived code is executed or imported.

- workload_concentration.csv: separate frequency/excess/raw-tilt top 1/5/10% rankings with within-scope coverage and global/scope contributions.
- workload_error_attribution.csv: complete overall and within-type per-workload tables.
- feature_combination_errors.csv: complete one/two-way families, selected supported-either three-way cells and support flags; subgroup_coverage.csv supplies the omitted remainder so all families reconcile.
- duration_shift_vs_error.csv: training/validation feature populations, fractional workload weights, duration and validation error summaries, exact decomposition components.
- cross_split_subgroup_comparison.csv: cell support and sign consistency across partitions, without paired-workload claims.
- centered_workload_duration_attribution.csv and centered_duration_error_overlap.csv: origin-invariant supplemental duration influence and error overlap.
- influential_workload_feature_profiles.csv and ranked_population_profiles.csv: observed characteristics of selected influential workloads/populations, with support.
- shared_validation_predictor_comparison.csv and shared_validation_workloads.csv: matched validation-only record/population checks.
- workload_cluster_uncertainty.csv: conditional paired cluster intervals.
- verification_results.json, supplemental_verification.json and run_manifest.json: source identity, models, row counts, reconciliation, stages and output hashes.

Never add overlapping families, ALL/type duplicate workload scopes, or normalized net shares as if they were disjoint probabilities. Type cells partition executions; a workload may span types or other feature cells. Cells with missing/unknown values remain explicit. All source scientific artifacts are left unchanged.
