import pandas as pd
import numpy as np
import pyarrow.parquet as pq

PATH = "part-000.parquet"

print("Reading duration + lifecycle...", flush=True)

df = pd.read_parquet(
    PATH,
    columns=[
        "duration_hours",
        "job_type_public",
        "model_type_public",
    ]
)

d = df["duration_hours"].astype(float)

print("\n=== BASIC TARGET AUDIT ===")
print(f"Rows: {len(df):,}")
print(f"Unique durations: {d.nunique():,}")
print(f"Min: {d.min():.9f} h")
print(f"Max: {d.max():.9f} h")

# --------------------------------------------------
# Convert duration to seconds.
# This tells us the underlying resolution.
# --------------------------------------------------

seconds = d * 3600

distance_from_integer = np.abs(
    seconds - np.round(seconds)
)

print("\n=== RESOLUTION ===")
print(
    "Fraction effectively integer seconds:",
    f"{(distance_from_integer < 1e-6).mean():.6%}"
)

rounded_seconds = np.round(seconds).astype("int64")

print(
    "Smallest positive duration:",
    f"{rounded_seconds[rounded_seconds > 0].min():,} sec"
)

# --------------------------------------------------
# Most common exact durations
# --------------------------------------------------

print("\n=== MOST COMMON EXACT DURATIONS ===")

common = (
    rounded_seconds.value_counts()
    .head(30)
)

for sec, n in common.items():
    print(
        f"{sec:10,d} sec = "
        f"{sec/3600:10.4f} h | "
        f"{n:12,d} rows"
    )

# --------------------------------------------------
# Check suspicious round-hour boundaries
# --------------------------------------------------

print("\n=== ROUND-HOUR MASS ===")

for hours in [
    1, 2, 4, 6, 8, 12, 24,
    48, 72, 168, 336, 720,
    1440, 1800, 1824
]:
    exact = np.isclose(d, hours, atol=1/3600)
    print(
        f"{hours:5d} h : "
        f"{exact.sum():10,d} "
        f"({exact.mean():.6%})"
    )

# --------------------------------------------------
# Upper tail
# --------------------------------------------------

print("\n=== UPPER TAIL ===")

for q in [
    .99, .995, .999, .9995,
    .9999, .99995, .99999
]:
    print(
        f"q={q:.5f}: "
        f"{d.quantile(q):.6f} h"
    )

# --------------------------------------------------
# Inspect values near the apparent 1824-hour ceiling
# --------------------------------------------------

print("\n=== NEAR 1824-HOUR CEILING ===")

for threshold in [
    1800,
    1810,
    1820,
    1823,
    1823.5,
    1823.9,
    1823.99,
    1824,
]:
    n = (d >= threshold).sum()

    print(
        f">= {threshold:8.2f} h : "
        f"{n:8,d}"
    )

# Exact largest observed duration values
print("\nLargest 30 distinct duration values:")

largest = np.sort(d.unique())[-30:]

for x in largest[::-1]:
    print(f"{x:.9f} h")


# --------------------------------------------------
# Ceiling behavior by lifecycle
# --------------------------------------------------

print("\n=== CEILING BY JOB TYPE ===")

for jt, g in df.groupby("job_type_public"):

    x = g["duration_hours"].astype(float)

    print(f"\n{jt}")
    print(f"N:       {len(x):,}")
    print(f"Max:     {x.max():.6f} h")
    print(f"P99:     {x.quantile(.99):.6f} h")
    print(f"P99.9:   {x.quantile(.999):.6f} h")
    print(
        f">=1800h: {(x >= 1800).sum():,}"
    )
    print(
        f">=1823h: {(x >= 1823).sum():,}"
    )


# --------------------------------------------------
# Ceiling behavior by model type
# --------------------------------------------------

print("\n=== CEILING BY MODEL TYPE ===")

for mt, g in df.groupby("model_type_public"):

    x = g["duration_hours"].astype(float)

    print(f"\n{mt}")
    print(f"N:       {len(x):,}")
    print(f"Max:     {x.max():.6f} h")
    print(f"P99.9:   {x.quantile(.999):.6f} h")
    print(
        f">=1800h: {(x >= 1800).sum():,}"
    )


# --------------------------------------------------
# Histogram of extreme durations
# --------------------------------------------------

print("\n=== EXTREME-DURATION BINS ===")

bins = [
    0,
    1,
    6,
    24,
    72,
    168,
    336,
    720,
    1000,
    1500,
    1800,
    1820,
    1823,
    1824.0001,
]

labels = [
    "<1h",
    "1-6h",
    "6-24h",
    "1-3d",
    "3-7d",
    "1-2wk",
    "2-4wk",
    "30-42d",
    "42-62d",
    "62-75d",
    "75-75.8d",
    "75.8-76d",
    "~76d",
]

bucket = pd.cut(
    d,
    bins=bins,
    labels=labels,
    right=False
)

counts = bucket.value_counts().sort_index()

for label, n in counts.items():
    print(
        f"{str(label):12s}: "
        f"{n:12,d} "
        f"({n/len(df):.6%})"
    )

print("\nTARGET AUDIT COMPLETE")