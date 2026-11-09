# ASI dataset audit and provenance

This document separates inherited evidence from checks performed in this implementation. Historical scripts and artifacts remain unchanged. The complete handoff is retained in `HANDOFF_ORIGINAL.txt`; no lifecycle-ablation results have been observed.

## Schema/encoding clarification

**Schema/label clarification made before model training and before observing lifecycle-ablation results.**

| Conceptual label | Authoritative physical ASI value |
|---|---|
| offline inference | offline_inference |
| online inference | online_inference |
| training | training |
| dev | dev |

The handoff used offline/online as shorthand. The user explicitly approved this clarification. It is NOT a scientific-protocol or population change; counts match exactly. No source recoding is permitted. Primary physical categories are training, offline_inference, online_inference, dev; unknown/other are excluded from primary lifecycle modeling.

## INDEPENDENTLY VERIFIED IN CURRENT IMPLEMENTATION

### Observed facts from initial read-only inspection

- Source `part-000.parquet`: 1,188,294,827 bytes; 40,522,321 rows; 346 row groups.
- The schema matches all 14 expected fields. Strings: pod_id, workload_id, server_id, gpu_spec_public, priority_class, job_type_public, model_type_public. Boolean: is_genai_request, ready_status, schedule_status. Double: gpu_request, duration_hours. Int64: schedule_delay_sec, ready_delay_sec.
- Arrow schema metadata is absent. No independent dataset-release identifier/checksum manifest was found locally. Attribution to v2026 / ASI comes from the handoff, not verified release metadata.
- A narrow lifecycle-column aggregation gave the exact counts below. No aliases were introduced.

| Physical lifecycle | Rows |
|---|---:|
| offline_inference | 32,194,936 |
| online_inference | 5,054,990 |
| training | 2,999,580 |
| unknown | 170,977 |
| other | 70,130 |
| dev | 31,708 |

- `asi_audit.duckdb`, opened read-only, contains only `duplicate_pods` (pod_id VARCHAR, row_count BIGINT). Stored counts: 2,184,460 entries, sum(row_count)=6,021,763, max(row_count)=658. This verifies stored audit aggregates, not their completeness against a fresh global source aggregation.
- `duplicate_pod_counts.parquet`: 2,184,460 rows, 18 row groups, pod_id string and row_count int64. A full equality comparison to the DuckDB table was not run.
- Legacy `temporal_map.parquet`: 113,443 rows and distinct pods, all day 109/hour 0; schema pod_id string, first_seen_day int16, first_seen_hour int8. 50,870 legacy IDs intersect the stored duplicate-pod table. Subtraction initially produced only a candidate 62,573.
- Initial 10,000-row Arrow sample: no missing/nonpositive duration; minimum 0.005555555555555556 h, maximum 1703.9888888888888 h. This is a first-batch smoke check, not a representative sample or complete target audit.
- Installed at inspection: PyArrow 25.0.1, DuckDB 1.5.5, pandas 3.0.6, NumPy 2.5.3. LightGBM, SciPy, scikit-learn and PyYAML absent. No packages installed.
- Approximately 66 GiB disk free at inspection. RAM query denied by sandbox; hardware RAM is not inferred.

### Interpretations and design consequences

- Matching schema/counts support compatibility with the handoff; they do not independently establish the release version. This provenance limitation remains open.
- The legacy temporal artifact is historical extraction/join validation, NOT an eligible temporal population. Source-backed verification is documented below, separately from initial subtraction.
- Existing remote readers can consume an unbounded body if Range is ignored; they must not be run unchanged. Existing temporal script rescans the summary each hour, accepts repeated pods, and lacks durable checkpoints. Preserve these scripts rather than overwriting them.
- Initial audit scripts load whole multi-column data into pandas; reuse their analytical definitions selectively, not their memory strategy. `asi_audit.py` already uses physical inference names in its pair checks.

## HANDOFF-REPORTED / PREVIOUSLY AUDITED

These results have not all been independently reproduced. They remain inherited evidence unless specifically marked above or in the current validation manifest.

### Population, target and workload observations

- Expected source rows 40,522,321; unique pod IDs 36,685,018.
- Workload non-null rows 4,792,402 (~11.83%), distinct workloads 501,183.
- Model types: genai 32,077,913; cv 3,660,094; rec 2,867,756; unknown 1,393,920; embedding 496,787; dev 25,851.
- Duration hours: mean ~5.153373, median ~0.422222, p95 ~9.688889, p99 ~59.62222, p99.9 ~799.5, maximum 1824. No zero/negative/missing duration observed in prior full audit; ~95,804 distinct durations, effectively second resolution. Only ~104 executions near extreme 76-day boundary; no massive generic pile-up.
- Workloads with ≥2/5/10/20/50/100 executions: 136,822 / 50,870 / 28,637 / 18,521 / 11,438 / 7,490.
- Earlier usable workloads: 473,265; multi-lifecycle workloads 1,544 (~0.326%); their executions 389,236 (~8.265%). Only 51 workload+model groups span ≥2 lifecycle types.
- Strict known-model training/offline-inference matched cohort: 46 configurations, 784 executions (355 training, 429 offline inference), effectively all GenAI.

### Duplicate audit observations

| Pod multiplicity | Pods |
|---|---:|
| exactly 1 | 34,500,558 |
| ≥2 | 2,184,460 |
| ≥3 | 369,193 |
| ≥5 | 142,003 |
| ≥10 | 52,498 |

Maximum 658 rows/pod; rows in duplicated pods 6,021,763. Exact duplicate rows removable: 5,644 (no removal policy inferred).

| Field varying within duplicated pods | Pods |
|---|---:|
| workload_id | 74,440 |
| server_id | 296,263 |
| gpu_spec_public | 11,792 |
| priority_class | 5,972 |
| job_type_public | 108,002 |
| model_type_public | 77,583 |
| is_genai_request | 104,580 |
| gpu_request | 463 |
| duration_hours | 2,179,948 |
| schedule_delay_sec | 858,957 |
| ready_delay_sec | 1,723,425 |
| ready_status | 1,288,618 |
| schedule_status | 606,234 |

Distinct candidate-key counts: pod 36,685,018; pod+server 37,459,836; pod+workload 36,759,688; pod+server+workload 37,532,436; pod+server+duration 40,253,190; pod+workload+duration 40,068,540. These are historical diagnostics, not permission to manufacture execution keys.

### Remote/temporal observations

- Remote ZIP 351,803,513,445 bytes; prior HTTP 206/range access validated.
- 4,440 hourly members, days 0–184, 24/day, all ZIP_STORED, ~327.64 GiB payload. Hourly ~35.57–106.76 MiB; day ~1.3–2.2 GiB.
- D109H00 extracted member ~78.70 MiB, 1,489,135 rows, 1,489,134 unique pods. 113,443 matched all-summary pods, ~7.618052%.
- Prior temporary hourly raw Parquet was deleted after successful processing (handoff claim; no new deletion).
- D108/D109/D110 estimates: 1.831/1.875/1.938 GiB, total ~5.644 GiB. No new remote probe/download performed.
- Hourly schema has 23 physical columns; day/hour are ZIP-path partitions, not physical columns. Full schema and extraction provenance remain in original handoff.

### Interpretations and frozen consequences inherited from handoff

Do not trim the heavy tail. Distinguish long-lived dev/online processes from finite training/offline execution with a secondary finite analysis. Workload/lifecycle association motivates unseen-workload testing, not a causal within-workload claim. The tiny matched cohort is diagnostic only. Unique-pod restriction applies only to temporal reconstruction. Null-workload exclusion applies only to primary grouped evaluation. The single-hour 7.618% is P(summary membership | hourly observation), not P(timestamp recoverable | summary row). The released summary population need not match production population proportions.

Prior-art search and metadata provenance claims (including user-provided lifecycle metadata and rejected AcmeTrace labels) are inherited research context, not reverified literature findings in this implementation.

## INDEPENDENTLY VERIFIED IN CURRENT IMPLEMENTATION — source-backed D109H00 validation

The validator scanned only source `pod_id` and `job_type_public`, semi-joined all legacy IDs, and counted every source occurrence before filtering. It did not use the stored duplicate table to decide multiplicity.

| Check | Verified count |
|---|---:|
| Distinct legacy IDs | 113,443 |
| Legacy IDs found in source | 113,443 |
| Missing from source | 0 |
| IDs occurring more than once in source, excluded | 50,870 |
| Unique-source IDs with missing/unrecognized lifecycle | 0 |
| Eligible retained IDs | **62,573** |

| Physical lifecycle of eligible IDs | Pods |
|---|---:|
| dev | 414 |
| offline_inference | 32,788 |
| online_inference | 24,432 |
| other | 129 |
| training | 4,649 |
| unknown | 161 |

`unknown` and `other` are recognized physical labels and retained for descriptive temporal stratification. They remain excluded from primary lifecycle modeling. The temporal eligibility rule itself is source multiplicity exactly one; no extra scientific population filter was applied.

Output: `artifacts/temporal/d109h00_eligible.parquet`, with pod_id, first_seen_day, first_seen_hour, job_type_public. This is a separate artifact; `temporal_map.parquet` is untouched.

Evidence: `results/audits/local_validation.json` records schemas, SHA-256 digests, software versions, source and output paths, split/feature smoke checks, counts, exclusions, elapsed time and zero remote bytes/models. Local validation took about 3.51 seconds on this machine (including input hashing; not a projection of full training performance). Every original top-level file was SHA-256 identical before and after validation.

Validation was executed in a temporary staging directory because the actual project lies outside the task's writable roots. Its manifest preserves the actual execution paths. `results/audits/delivery.json` maps staged artifacts to final project paths and verifies hashes; no provenance paths are retroactively fabricated.

The source-backed check verifies multiplicity for legacy IDs only. It does not independently re-establish global unique-pod/workload totals or the full duration distribution.
