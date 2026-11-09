import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.compute as pc
import os

# --------------------------------------------------
# INPUTS
# --------------------------------------------------

hourly_path = "/tmp/day109_hour00.parquet"
summary_path = "part-000.parquet"

day = 109
hour = 0

output_path = "temporal_map.parquet"


# --------------------------------------------------
# 1. LOAD UNIQUE POD IDS FROM THIS HOUR
# --------------------------------------------------

print(f"Processing day={day}, hour={hour:02d}")

hourly_table = pq.read_table(
    hourly_path,
    columns=["pod_id"]
)

hourly_ids = pc.unique(
    pc.drop_null(hourly_table["pod_id"])
)

print(f"Hourly rows:       {hourly_table.num_rows:,}")
print(f"Unique hourly IDs: {len(hourly_ids):,}")


# --------------------------------------------------
# 2. STREAM EXECUTION SUMMARY
# --------------------------------------------------

print("Scanning execution summary...")

summary_pf = pq.ParquetFile(summary_path)

matched_ids = set()
rows_scanned = 0

for i, batch in enumerate(
    summary_pf.iter_batches(
        batch_size=500_000,
        columns=["pod_id"]
    ),
    start=1
):
    arr = batch.column(0)

    rows_scanned += len(arr)

    mask = pc.is_in(
        arr,
        value_set=hourly_ids
    )

    hits = pc.filter(arr, mask)

    if len(hits):
        matched_ids.update(
            x for x in hits.to_pylist()
            if x is not None
        )

    if i % 10 == 0:
        print(
            f"Scanned {rows_scanned:,} summary rows | "
            f"matched unique: {len(matched_ids):,}"
        )


print()
print(f"Matched execution-summary pods: {len(matched_ids):,}")


# --------------------------------------------------
# 3. CREATE THIS HOUR'S TEMPORAL MAP
# --------------------------------------------------

matched_sorted = sorted(matched_ids)

new_table = pa.table({
    "pod_id": pa.array(matched_sorted, type=pa.string()),
    "first_seen_day": pa.array(
        [day] * len(matched_sorted),
        type=pa.int16()
    ),
    "first_seen_hour": pa.array(
        [hour] * len(matched_sorted),
        type=pa.int8()
    ),
})


# --------------------------------------------------
# 4. MERGE WITH EXISTING MAP IF PRESENT
# --------------------------------------------------

if os.path.exists(output_path):

    print("Existing temporal map found; merging...")

    old = pq.read_table(output_path)

    combined = pa.concat_tables([old, new_table])

    # Sort chronologically so the earliest observation comes first.
    combined = combined.sort_by([
        ("first_seen_day", "ascending"),
        ("first_seen_hour", "ascending"),
    ])

    # Deduplicate by pod_id, keeping earliest occurrence.
    pod_ids = combined["pod_id"].to_pylist()

    keep = []
    seen = set()

    for idx, pod_id in enumerate(pod_ids):
        if pod_id not in seen:
            seen.add(pod_id)
            keep.append(idx)

    combined = combined.take(
        pa.array(keep, type=pa.int64())
    )

    result = combined

else:
    print("Creating new temporal map...")
    result = new_table


# --------------------------------------------------
# 5. SAVE COMPACT RESULT
# --------------------------------------------------

pq.write_table(
    result,
    output_path,
    compression="zstd"
)

print()
print("=== RESULT ===")
print(f"Temporal-map pods: {result.num_rows:,}")
print(f"Saved: {output_path}")

size_mb = os.path.getsize(output_path) / 1024**2
print(f"Map size: {size_mb:.2f} MiB")


# --------------------------------------------------
# 6. DELETE SOURCE HOURLY PARQUET
# --------------------------------------------------

print()
answer = input(
    f"Delete processed source {hourly_path}? [y/N]: "
).strip().lower()

if answer == "y":
    os.remove(hourly_path)
    print("Deleted source hourly Parquet.")
else:
    print("Source retained.")