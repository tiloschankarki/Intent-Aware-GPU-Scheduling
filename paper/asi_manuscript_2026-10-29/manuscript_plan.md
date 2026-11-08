# Manuscript plan — 29 October 2026

**Working title:** Partition and Weighting Sensitivity in ASI Execution-Duration Prediction: A Case Study

**Recommended form:** an empirical workshop paper, short paper, or technical report. A full systems venue would require a substantially stronger contribution than the existing evidence establishes. Venue acceptance cannot be inferred from having three experiments or polished figures.

## Argument and alternatives

The paper asks how much one coarse public workload-type field adds to a specified predictor, and how that measured increment changes across baseline controls, workload partitions, selection outcomes, and evaluation units. The central result is conditional sensitivity, not a new predictor or scheduler.

Three possible narratives were considered. A “semantics improves runtime prediction” narrative is too broad and too close to Menear and Weng. A “concentration causes instability” narrative exceeds the diagnostic evidence and is contradicted by influential workloads that help M1. The recommended narrative is a bounded ASI case study: a small baseline-dependent historical increment motivates partition diagnostics, followed by a restricted-population sensitivity study with explicit selection and weighting qualifications. This narrative connects the experiments without pretending they estimate one pooled effect.

## Research questions

1. **RQ1 — incremental value under controls:** On the historical workload-disjoint test split, how does adding `job_type_public` change LogMAE beyond resource plus priority controls, and beyond additional model/application controls?
2. **RQ2 — partition and predictor sensitivity:** Across the two historical validation partitions, where does the selected M1/M0 ranking change, and what do saved-predictor diagnostics establish about error localization and predictor differences?
3. **RQ3 — weighting and restricted-population robustness:** Across ten documented group partitions of the restricted population, how do execution-weighted and equal-workload selected-validation comparisons differ for the same selected models?
4. **RQ4 — explanatory limits:** How much of the aggregate signed loss gap is attributable arithmetically to frequency-selected groups, and which proposed explanations remain unsupported?

RQ4 is descriptive attribution. It is not causal identification. RQ2 diagnostics were exploratory. RQ3's documented plan is stronger evidence of a frozen protocol than an improvised analysis, but not an independently timestamped public registration.

## Precisely scoped contributions

- An ASI-specific comparison showing that the historical test increment from one coarse type field is substantially smaller with richer application/model controls: approximately 5.88% versus 1.05% across three model seeds on one fixed group split. These are informal means, not a prespecified pooled effect.
- A saved-predictor diagnostic account of a two-partition selected-validation reversal, with reconciled workload/subgroup attribution and differing performance on identical shared validation records. This rules out an explanation based solely on the composition of those shared evaluation records; it does not isolate training or selection causes.
- A ten-partition restricted-population selected-validation characterization in which M1 improves 8/10 execution-weighted and 9/10 equal-workload comparisons, including a fixed-prediction ranking reversal under reweighting. These are dependent descriptive outcomes, not future win probabilities.
- A transparent evidence package separating historical test results, selected-validation results, loss attribution, and unresolved provenance or mechanism claims. The package is an empirical reporting contribution, not a new evaluation theory.

## Evidence and experiment table

| Experiment | Population and variation | Evidence used | Main finding | Inference boundary |
|---|---|---|---|---|
| 1 | Four-type canonical population; one workload-disjoint split; three model seeds | Historical checkpoint plus audit-reported weak-control numbers | Strong-control test gains 0.815–1.379%; weak resource+priority gains 5.844–5.949% | Same test population across seeds; conditional intervals; no universal null or causal redundancy claim |
| 2 | Two historical group partitions; fixed model seed | Existing phase-one findings and saved verification reports | Execution-weighted selected-validation gains +2.084% and −4.907%; shared-record ranking also changes | Evaluation reuses selection validation; diagnostics do not identify why predictors differ |
| 3 | 341,617 workloads / 3,372,430 executions; ten group partitions; fixed model seed | Original consolidated report with 240 candidates and registration | 8/10 and 9/10 wins; seed 20261102 changes sign across weighting | Excludes historical holdout union; about 72% retained; overlapping partitions; no new test evaluation |

Do not combine the three rows into a meta-analysis, an aggregate win count, or a single performance estimate. Seed numbers that resemble future dates are identifiers.

## Section-by-section outline

| Section | Purpose and required content | Approximate allocation |
|---|---|---|
| Abstract | Task, evidence distinction, strongest numbers, limitations | 180–220 words |
| 1. Introduction | Why a public type label's marginal predictive value is a useful systems measurement; state bounded contributions | 0.75 page |
| 2. Task and prior work | ASI execution span, feature semantics, grouping; compare Weng, Li, ATLAS, TARE and Menear | 1 page |
| 3. Study design | Population, target, M0/M1, grid, selection, formulas, experiment-specific evidence levels and holdout exclusion | 1–1.25 pages |
| 4. Historical test increment | Weak versus rich controls; all three seeds; strong-control conditional intervals and original-hour MAE caveat | 0.5 page |
| 5. Two-partition diagnostics | Reversal; frequency versus signed error; shared-record control; complexity caveat | 0.75–1 page |
| 6. Ten-partition study | Every seed and both metrics; restriction; same winners; concentration and candidate context | 1 page |
| 7. Implications and validity | What benchmark users can take away; external validity, selection, timing/provenance and mechanism limits | 0.75 page |
| 8. Conclusion | One bounded empirical conclusion; no scheduler promise | 100–150 words |
| Appendix/artifact | Full tables, candidates, hashes, definitions, environment, exclusions, exploratory status | As needed |

The initial draft is a content draft, not a venue-formatted submission. Fit figures and references after choosing a venue. Do not remove evidence qualifications just to meet a page limit.

## Figure specifications and captions

All current figures have vector PDF and SVG plus 300-dpi PNG. Use PDF for submission. Typography is embedded in PDF; colorblind-friendly blue/orange is reinforced by marker shape or position. Signed comparisons retain a zero reference. No decorative GPU illustration is needed: it adds no evidence.

**Figure 1 — historical test and baseline dependence.** Two panels: paired weak/strong-control point gains for all three model seeds, then strong-control gains with the historical paired workload-bootstrap 95% intervals. Weak-control values come from the retrieved audit excerpt, rounded there to six decimals; strong-control values/intervals come from the historical checkpoint. No weak-control intervals are fabricated. Caption: “Historical test comparisons on one workload-disjoint split. Model seeds vary fitting randomness, not test membership. Richer controls reduce the measured incremental benefit; all principal strong-control conditional intervals cross zero. Intervals condition on fitted models and omit training/selection uncertainty.”

**Figure 2 — ten-partition comparison.** Horizontal paired dots for every seed; execution and equal-workload relative improvement on a common signed percentage axis; retain full seed identifiers and exact values in the companion CSV. Caption: “Experiment 3 selected-validation comparisons. Positive values indicate lower M1 LogMAE. Both metrics evaluate models chosen by execution-weighted validation loss. Seed 20261102 reverses ranking under reweighting. Partitions overlap; points are not independent replications.” This is the lead result figure.

**Figure 3 — concentration and signed attribution.** Left: frequency-top-1% execution share against selected-validation relative gain for all ten partitions, without fitted regression or significance test. Right: separately signed top-1% and remaining-workload contributions for positive-control seed 20261028 and negative seeds 20261101/20261102. Caption: “High frequency concentration coexists with both model rankings. Signed contributions use the full validation execution count as denominator and sum across disjoint workload groups to M0−M1 LogMAE. Cases are selected descriptively; concentration is not identified as a cause.” Values are taken from original report diagnostics, not newly recomputed from workload Parquets.

**Figure 4 — selection context.** Selected boosting rounds for both models across all ten partitions; all 12 candidate losses per model for seed 20261101. Points at 200 rounds are at the protocol cap. Caption: “Selected model complexity and candidate outcomes vary across partitions. The negative seed's M1 winner uses one boosting round. Rounds are only one dimension of complexity: leaves, leaf support and feature fraction can change too. The plot does not identify an early-stopping mechanism or estimate selection bias.” Do not connect candidate IDs with a trend line: they are categorical grid entries.

**Figure 5 — evidence map.** Three separate boxes, labeled historical test versus selected validation, with no causal arrows. Caption: “The three experiments address related but distinct questions and populations. Their results are not pooled.” Use as an overview or appendix figure if space is tight.

**Figure 6 — historical selected-validation reversal.** Two panels: both metrics on the two historical partitions, followed by M0 and M1 LogMAE on the identical 100,221 shared validation records under each saved predictor pair. Source: existing phase-one findings; shared-record numbers retain the report's six-decimal precision. Caption: “Experiment 2 selected-validation comparisons. The same shared evaluation records favor M1 under the original saved pair and M0 under the second pair. This shows changed predictor behavior beyond the composition of those records, without isolating the training or selection cause. The shared-record diagnostic is exploratory.” Lower error is better in the right panel; positive M1 improvement is better in the left panel, as explicitly labeled.

**Optional figure needing original workload tables:** full signed per-workload contribution distribution or cumulative frequency/error attribution for Experiment 3, with negative and positive gross components distinguished. Required files are the ten original `SUMMARY/validation_workload_loss_sums.parquet` tables and matching `COMMIT.json` records. Not needed for the six supplied figures; do not recreate missing workload points from aggregates or use synthetic runner test outputs.

## What was found, why helpful, potential impact

The historical increment is baseline-dependent. The selected-validation comparison is partition-sensitive. The evaluation unit can change the ranking even when predictions stay fixed. Frequency concentration magnifies the influence of repeated workloads, but does not determine whether that influence helps or harms M1. Shared-record diagnostics demonstrate predictor sensitivity beyond the composition of those evaluated records. The training/selection mechanism remains unresolved.

This helps researchers avoid reporting a small metadata gain as an intrinsic property of the field. A benchmark can report its unit of averaging, baseline controls and selection status alongside the score, making comparisons interpretable. For systems builders, the result is a warning to validate the intended deployment population and objective before relying on a coarse category. No measured utilization, throughput, cost, energy or scheduling improvement follows from these experiments. Those are potential downstream motivations, not demonstrated impact.

## Remaining submission work (no new experiments authorized)

1. Obtain the untruncated remainder of the October 29 audit before claiming complete line-by-line incorporation: the conversation tool returned only its first 20,000 characters. Existing originals support the current core draft.
2. Bind the weak-control Figure 1 numbers directly to the Experiment 1 results-summary object if submission requires original-artifact rather than audit-transcribed provenance. The draft preserves this evidence distinction.
3. Check exact source-to-population/split lineage for Experiment 3 and prediction-time availability of each feature using existing records; unresolved items stay limitations.
4. If including the optional workload-level figure, obtain its original validation-only loss tables and commits. Do not inspect reserved holdouts, retrain, alter grids, or add diagnostics requiring new fits.
5. Check citations, venue length/style, anonymization, dataset release/license terms, and artifact portability. Current numerical checks establish aggregate consistency only.
