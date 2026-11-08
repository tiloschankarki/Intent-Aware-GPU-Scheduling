# Supplemental interpretation checks

These checks were added after inspecting the initial exploratory tables; they are not confirmatory or prespecified in analysis_protocol.md. No model was trained or changed.

The raw per-workload frequency-duration term in the initial code is (n/N−1/W)×mean_y. It sums correctly but individual ranks depend on the outcome origin. For interpretable downward/upward influence, the supplementary centered term is (n/N−1/W)×(mean_y−Wmean_y). It has the same total frequency-duration association and is invariant to an additive shift of all log-durations. Raw and centered rankings are retained separately. Negative centered contributions pull the execution mean below the equal-workload mean within that partition; they are not causal train-to-validation effects.

The second check pairs only records/workloads shared by the two validation partitions. Common source row ordinals, all six observed analysis features, workload IDs and targets were verified exactly equal. No training workload was paired to validation. Differences on common rows reflect differences between the two fixed saved predictor pairs (including all their selected parameters/tree counts), not record composition. They do not identify which training or selection mechanism produced those predictors. Exclusive validation portions mix population and predictor changes and are labeled accordingly.

Influential workload profiles are descriptive top-five-frequency or top-five-excess cases within each type/overall scope; their small workload support is shown explicitly. They are not ranked as generalizable feature interactions.
