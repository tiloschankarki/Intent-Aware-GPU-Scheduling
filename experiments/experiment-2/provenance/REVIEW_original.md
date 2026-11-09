# Memory gate reassessment — local full training remains stopped

## What changed in the assessment

The 2.5 GiB worker cap is an operational safety policy, not part of the scientific protocol. It was **not raised or bypassed**. The previous 80-byte native-memory allowance and 25% margin were heuristic, not empirical bounds. Its small benchmark also used a different loader and retained raw frames through fitting. Consequently the prior 2.73 GiB estimate should not be described as proof that full training cannot fit.

A larger benchmark was justified by improved launch-time headroom. It used the recovered DuckDB loader settings (1 GiB query memory, two threads), original feature/encoding/fitting functions, candidate 10 (63 leaves, minimum leaf size 20, feature fraction 1), model seed 20260927, 200 maximum rounds and 30-round early stopping. Raw frames were released before fitting, as in the original pipeline. Sampling evenly spaced physical ranks is diagnostic only; it adds query/window overhead and is not identical to a full-size load. The scientific dataset and protocol were not altered.

## Measurements actually obtained

| Measurement | Result |
|---|---:|
| Benchmark train / validation rows | 1,000,000 / 233,548 |
| Roles run | M0 and M1, sequentially |
| Worker peak RSS from getrusage | 1.312 GiB |
| Peak sampled RSS | 1.312 GiB |
| Minimum system available memory | 2.120 GiB |
| macOS pressure levels | 1 throughout (normal) |
| Swap allocated before / after | 0 / 0 bytes |
| Compressor growth | 0.666 GiB |
| Supervised elapsed time | 15.34 seconds |

`vm_stat` reported cumulative Swapins=0 and Swapouts=0 both before the benchmark and at the subsequent recorded preflight. Thus no true swap I/O was observed over this interval. The initial supervisor's psutil `sin/sout` fields did not match those native counters; preserve those raw logs but do not label them true swap activity. The revised supervisor records native counters directly. Compression grew despite zero allocated swap, so “no swap” does not imply absence of memory cost.

Both diagnostic fits selected best iteration 1 and stopped after the original early-stopping patience. They were not 200-round stress tests and do not establish the peak cost of the entire 24-candidate full-data selection. The benchmark validation scores are not held-out scientific results.

## Why full training was not started

A proposed 1.25-million-training-row run retained the 2.5 GiB cap, a 1 GiB available-memory reserve, normal-pressure requirement, and a 128 MiB new-swap stop threshold. It required 2.65 GiB available at launch. Available memory had fallen to **2.354 GiB**, so it was stopped **before creating a worker**. Its raw preflight record is preserved.

The one-million-row run shows that the Mac can execute that bounded workload. It does not establish that all 3,976,462 train+validation rows and all 24 candidate fits remain below the unchanged cap and preserve headroom. No extrapolation alone is being treated as definitive. Since the next bounded step could not meet its reserve, this session stops rather than repeatedly probing until a favorable snapshot or weakening thresholds.

**Full scientific training, model selection, selected-model freeze and held-out evaluation have not run.** There are no new scientific predictions, LogMAE results or uncertainty intervals. Test remains mode 000, and an access-denial check passed. The original archive's size/mtime snapshot and all recovered source hashes still match.

## Cloud continuation prepared, not executed

`cloud_package/` contains a pinned Python/LightGBM container recipe, the unchanged original pipeline, the existing configuration and train/validation files, a selection/evaluation runner, and exact commands in `CLOUD_PLAN.md`. The package excludes test data, recovered canonical data and original archive objects. Selection receives no test mount and emits a hash-verified joint freeze only after both 12-candidate selections finish. Evaluation refuses to open test data before validating both selections.

Use a dedicated CPU host with at least 16 GiB RAM, retain two training threads, and preserve all input/configuration hashes. The plan applies a separate 10 GiB container cap with container swap disabled on that larger host; this does not change or bypass the Mac's cap. It records environment, every candidate model and parameter set, timings, peak RSS, both selected models, freeze hashes, predictions and paired workload-bootstrap metrics. The evaluation retains 1,000 replicates and seed 20260927, adds equal-workload reporting, and labels the result post-hoc internal split sensitivity.

Runner syntax and missing-freeze access guards were checked locally. **The cloud image has not been built, full training has not been executed, and no files have been uploaded to a cloud provider.** Platform differences must be recorded; deterministic settings do not promise bitwise equivalence across operating systems or architectures.

## Exact locations

- Review root: `/Users/tiloschan/Downloads/asi_robustness_20261020/reassessment`
- Measurements: `monitor/one_million/memory.jsonl`, `monitor/one_million/result.json`, `benchmark_1000000/result.json`
- Failed launch preflight: `monitor/one_quarter_million/result.json` (label denotes the proposed 1.25-million run; no worker ran)
- Updated decision: `decision.json`
- Reproducible instructions: `cloud_package/CLOUD_PLAN.md`
- Selection-only archive: `asi_robustness_cloud_selection.tar.gz`
- Original report and gate remain unchanged at the experiment root.
