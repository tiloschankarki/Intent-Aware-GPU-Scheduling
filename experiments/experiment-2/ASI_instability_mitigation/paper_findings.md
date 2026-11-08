# Manuscript-ready exploratory findings

## Established results

The saved validation baselines were independently reproduced using their archived categorical encodings and LightGBM 4.7.0. Execution-weighted validation LogMAE was 0.776974 (M0) versus 0.760785 (M1) on seed 20260927, and 0.785266 versus 0.823796 on seed 20261020. The selected M1 contained 190 trees on the original split and five on the second. Training and validation workloads were disjoint in both partitions.

A single prespecified additive type correction was estimated from strictly workload-disjoint, out-of-fold training residuals. Its type-specific weighted median residual was shrunk by n/(n+1000), with each workload receiving equal total weight inside its type. The same fixed rule was used on both splits, with no validation-driven correction tuning.

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

For seed 20260927 under execution weighting, the additive correction changed M0 LogMAE by an improvement of -0.038702 (-4.981%; paired workload-bootstrap 95% interval for absolute improvement [-0.051368, -0.026553]). Positive values denote lower error.
For seed 20260927 under equal workload weighting, the additive correction changed M0 LogMAE by an improvement of 0.015161 (1.969%; paired workload-bootstrap 95% interval for absolute improvement [0.013852, 0.016476]). Positive values denote lower error.
For seed 20261020 under execution weighting, the additive correction changed M0 LogMAE by an improvement of -0.097868 (-12.463%; paired workload-bootstrap 95% interval for absolute improvement [-0.159534, -0.036765]). Positive values denote lower error.
For seed 20261020 under equal workload weighting, the additive correction changed M0 LogMAE by an improvement of 0.025843 (3.267%; paired workload-bootstrap 95% interval for absolute improvement [0.023898, 0.027693]). Positive values denote lower error.

The correction worsened execution-weighted error by 4.981% and 12.463% on the original and second splits, respectively, despite equal-workload gains of 1.969% and 3.267%. All four paired conditional correction-versus-M0 intervals exclude zero. These results show an empirical tradeoff under this equal-workload-fitted correction, not performance-preserving stabilization.

## Interpretation and hypotheses

The correction did not meet the frozen point-estimate criterion of improving both second-split metrics while limiting original-split degradation to 0.5%. The result applies to this fixed correction and these two partitions. It does not identify a causal instability mechanism.

The difference between execution-weighted and equal-workload duration summaries is consistent with concentration of executions in particular workloads. However, offline-inference excess prediction error despite relatively stable marginal duration means, together with the large change in selected M1 tree count, argues against attributing all deterioration to online-inference mean shift. Conditional relationships, workload heterogeneity and selection/model-capacity effects remain plausible explanations that this experiment does not isolate.

## Limitations and permissible claims

This is an exploratory extension: historical test outcomes influenced its motivation, and validation data had previously been used for model selection. No test data, predictions or evaluations were accessed in this extension. Conditional bootstrap intervals omit model-fitting and model-selection uncertainty. The two partitions share a parent population and are not independent replications.

The extension strengthens the empirical paper by documenting a reproducible, bounded mitigation test and the limits of a simple distribution-shift explanation. It supports claims about observed partition sensitivity and the measured behavior of this one additive correction. It does not support causal attribution, broad robustness, a new confirmatory claim, or methodological novelty. No further mitigation search was launched.
