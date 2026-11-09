import pandas as pd
import numpy as np

PATH = "part-000.parquet"   # change if needed

# ============================================================
# 1. LOAD ONLY THE FIELDS NEEDED FOR THE KILL TEST
# ============================================================

cols = [
    "pod_id",
    "workload_id",
    "job_type_public",
    "model_type_public",
    "gpu_spec_public",
    "priority_class",
    "gpu_request",
    "duration_hours",
]

df = pd.read_parquet(PATH, columns=cols)

print("\n" + "=" * 80)
print("ASI EXECUTION-SUMMARY AUDIT")
print("=" * 80)

print(f"\nRows:              {len(df):,}")
print(f"Unique pods:       {df['pod_id'].nunique():,}")
print(f"Unique workloads:  {df['workload_id'].nunique(dropna=True):,}")


# ============================================================
# 2. MISSINGNESS / COVERAGE
# ============================================================

print("\n" + "=" * 80)
print("1. FIELD COVERAGE")
print("=" * 80)

for c in cols:
    nonnull = df[c].notna().sum()
    print(
        f"{c:22s} "
        f"{nonnull:12,} / {len(df):,} "
        f"({nonnull / len(df):7.2%})"
    )


# ============================================================
# 3. JOB TYPE DISTRIBUTION
# ============================================================

print("\n" + "=" * 80)
print("2. JOB TYPE DISTRIBUTION")
print("=" * 80)

jt = df["job_type_public"].value_counts(dropna=False)
print(pd.DataFrame({
    "count": jt,
    "fraction": jt / len(df)
}))


# ============================================================
# 4. MODEL TYPE DISTRIBUTION
# ============================================================

print("\n" + "=" * 80)
print("3. MODEL TYPE DISTRIBUTION")
print("=" * 80)

mt = df["model_type_public"].value_counts(dropna=False)
print(pd.DataFrame({
    "count": mt,
    "fraction": mt / len(df)
}))


# ============================================================
# 5. DURATION SANITY CHECK
# ============================================================

print("\n" + "=" * 80)
print("4. DURATION SANITY")
print("=" * 80)

print(df["duration_hours"].describe(
    percentiles=[.01, .05, .25, .5, .75, .95, .99, .999]
))

print("\nZero durations:",
      (df["duration_hours"] == 0).sum())

print("Negative durations:",
      (df["duration_hours"] < 0).sum())

print("Missing durations:",
      df["duration_hours"].isna().sum())

print("Unique duration values:",
      df["duration_hours"].nunique())


# ============================================================
# 6. DURATION BY JOB TYPE
# DESCRIPTIVE ONLY — NOT EVIDENCE OF INCREMENTAL VALUE
# ============================================================

print("\n" + "=" * 80)
print("5. DURATION BY JOB TYPE")
print("=" * 80)

duration_by_type = (
    df.groupby("job_type_public")["duration_hours"]
      .agg(["count", "mean", "median", "std", "min", "max"])
      .sort_values("count", ascending=False)
)

print(duration_by_type)


# ============================================================
# 7. WORKLOAD REPETITION
# ============================================================

print("\n" + "=" * 80)
print("6. WORKLOAD REPETITION")
print("=" * 80)

valid_w = df.dropna(subset=["workload_id"]).copy()

workload_sizes = valid_w.groupby("workload_id").size()

print("Rows with workload_id:",
      f"{len(valid_w):,}",
      f"({len(valid_w)/len(df):.2%})")

print("Unique workload_ids:",
      f"{valid_w['workload_id'].nunique():,}")

for n in [2, 5, 10, 20, 50, 100]:
    count = (workload_sizes >= n).sum()
    frac = count / len(workload_sizes) if len(workload_sizes) else np.nan

    print(
        f"Workloads with >= {n:3d} executions: "
        f"{count:10,} ({frac:7.2%})"
    )


# ============================================================
# 8. THE MAIN KILL TEST:
# HOW OFTEN DOES JOB TYPE VARY WITHIN WORKLOAD?
# ============================================================

print("\n" + "=" * 80)
print("7. WITHIN-WORKLOAD JOB-TYPE VARIATION  <-- MAIN TEST")
print("=" * 80)

usable = valid_w[
    valid_w["job_type_public"].notna()
    & ~valid_w["job_type_public"].isin(["unknown", "other"])
].copy()

types_per_workload = (
    usable.groupby("workload_id")["job_type_public"]
          .nunique()
)

multi_type = types_per_workload[types_per_workload >= 2]

print("Workloads with usable job type:",
      f"{len(types_per_workload):,}")

print("Workloads with >=2 job types:",
      f"{len(multi_type):,}")

if len(types_per_workload):
    print(
        "Fraction of workloads crossing job types:",
        f"{len(multi_type)/len(types_per_workload):.4%}"
    )


# ============================================================
# 9. IMPORTANT: WEIGHT BY EXECUTION ROWS TOO
# ============================================================

multi_ids = set(multi_type.index)

rows_multi = usable[
    usable["workload_id"].isin(multi_ids)
]

print("\nExecutions belonging to multi-type workloads:",
      f"{len(rows_multi):,}")

if len(usable):
    print(
        "Fraction of usable executions in multi-type workloads:",
        f"{len(rows_multi)/len(usable):.4%}"
    )


# ============================================================
# 10. WHICH JOB-TYPE COMBINATIONS OCCUR WITHIN WORKLOAD?
# ============================================================

print("\n" + "=" * 80)
print("8. WITHIN-WORKLOAD TYPE COMBINATIONS")
print("=" * 80)

if len(multi_type):

    combos = (
        usable[usable["workload_id"].isin(multi_ids)]
        .groupby("workload_id")["job_type_public"]
        .agg(lambda x: " + ".join(sorted(set(x))))
        .value_counts()
    )

    print(combos.head(30))

else:
    print("NO multi-type workloads found.")


# ============================================================
# 11. DIRECT PAIR COUNTS WE CARE ABOUT
# ============================================================

print("\n" + "=" * 80)
print("9. IMPORTANT WITHIN-WORKLOAD PAIRS")
print("=" * 80)

pairs = [
    ("training", "offline_inference"),
    ("training", "dev"),
    ("training", "online_inference"),
    ("offline_inference", "dev"),
    ("offline_inference", "online_inference"),
    ("dev", "online_inference"),
]

workload_type_sets = (
    usable.groupby("workload_id")["job_type_public"]
          .agg(set)
)

for a, b in pairs:

    ids = workload_type_sets[
        workload_type_sets.apply(
            lambda s: a in s and b in s
        )
    ].index

    pair_rows = usable[
        usable["workload_id"].isin(ids)
        & usable["job_type_public"].isin([a, b])
    ]

    print(
        f"{a:20s} <-> {b:20s} "
        f"workloads={len(ids):8,} "
        f"executions={len(pair_rows):10,}"
    )


# ============================================================
# 12. MODEL TYPE x JOB TYPE
# ============================================================

print("\n" + "=" * 80)
print("10. MODEL TYPE x JOB TYPE")
print("=" * 80)

cross = pd.crosstab(
    df["model_type_public"],
    df["job_type_public"]
)

print(cross)


# ============================================================
# 13. WITHIN WORKLOAD + MODEL:
# STRONGER TEST OF WHETHER JOB TYPE STILL VARIES
# ============================================================

print("\n" + "=" * 80)
print("11. WITHIN WORKLOAD + MODEL TYPE VARIATION")
print("=" * 80)

wm = usable.dropna(
    subset=["model_type_public"]
).copy()

wm = wm[
    wm["model_type_public"] != "unknown"
]

wm_variation = (
    wm.groupby(
        ["workload_id", "model_type_public"]
    )["job_type_public"]
    .nunique()
)

wm_multi = wm_variation[
    wm_variation >= 2
]

print("Workload/model groups:",
      f"{len(wm_variation):,}")

print("Groups containing >=2 job types:",
      f"{len(wm_multi):,}")

if len(wm_variation):
    print(
        "Fraction:",
        f"{len(wm_multi)/len(wm_variation):.4%}"
    )


# ============================================================
# 14. RESOURCE DIFFERENCES BY JOB TYPE
# ============================================================

print("\n" + "=" * 80)
print("12. GPU REQUEST BY JOB TYPE")
print("=" * 80)

print(
    df.groupby("job_type_public")["gpu_request"]
      .agg(["count", "mean", "median", "std", "min", "max"])
)


# ============================================================
# 15. GPU MODEL x JOB TYPE
# ============================================================

print("\n" + "=" * 80)
print("13. GPU MODEL x JOB TYPE")
print("=" * 80)

print(
    pd.crosstab(
        df["gpu_spec_public"],
        df["job_type_public"]
    )
)


# ============================================================
# 16. PRIORITY x JOB TYPE
# ============================================================

print("\n" + "=" * 80)
print("14. PRIORITY x JOB TYPE")
print("=" * 80)

print(
    pd.crosstab(
        df["priority_class"],
        df["job_type_public"]
    )
)


# ============================================================
# 17. SAVE THE INTERESTING SUBSET
# ============================================================

if len(multi_ids):

    audit_subset = usable[
        usable["workload_id"].isin(multi_ids)
    ].sort_values(
        ["workload_id", "job_type_public"]
    )

    audit_subset.to_csv(
        "asi_multitype_workloads.csv",
        index=False
    )

    print(
        "\nSaved multi-type workload rows to:"
        "\nasi_multitype_workloads.csv"
    )


print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)