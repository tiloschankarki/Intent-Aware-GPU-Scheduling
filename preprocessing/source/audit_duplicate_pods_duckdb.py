import duckdb
import os

PARQUET = "part-000.parquet"
DB = "asi_audit.duckdb"

con = duckdb.connect(DB)

# Keep memory bounded on the MacBook.
con.execute("SET memory_limit = '6GB'")
con.execute("SET threads = 4")
con.execute("SET temp_directory = '/tmp/duckdb_asi_temp'")

print("DuckDB connected.")
print(f"Input: {PARQUET}")
print()

# ------------------------------------------------------------
# 1. Basic multiplicity
# ------------------------------------------------------------

print("=== POD MULTIPLICITY ===")

q = f"""
WITH counts AS (
    SELECT pod_id, COUNT(*) AS n
    FROM read_parquet('{PARQUET}')
    GROUP BY pod_id
)
SELECT
    SUM(n) AS rows,
    COUNT(*) AS unique_pods,
    COUNT(*) FILTER (WHERE n = 1) AS pods_eq_1,
    COUNT(*) FILTER (WHERE n >= 2) AS pods_ge_2,
    COUNT(*) FILTER (WHERE n >= 3) AS pods_ge_3,
    COUNT(*) FILTER (WHERE n >= 5) AS pods_ge_5,
    COUNT(*) FILTER (WHERE n >= 10) AS pods_ge_10,
    MAX(n) AS max_rows_per_pod
FROM counts
"""

print(con.execute(q).df().to_string(index=False))


# ------------------------------------------------------------
# 2. Persist ONLY duplicate pod IDs
# ------------------------------------------------------------

print("\nBuilding compact duplicate-pod table...")

con.execute(f"""
CREATE OR REPLACE TABLE duplicate_pods AS
SELECT pod_id, COUNT(*) AS row_count
FROM read_parquet('{PARQUET}')
GROUP BY pod_id
HAVING COUNT(*) > 1
""")

n_dup = con.execute(
    "SELECT COUNT(*) FROM duplicate_pods"
).fetchone()[0]

print(f"Duplicated pod IDs: {n_dup:,}")


# ------------------------------------------------------------
# 3. Number of execution-summary rows belonging to duplicates
# ------------------------------------------------------------

q = f"""
SELECT COUNT(*)
FROM read_parquet('{PARQUET}') s
INNER JOIN duplicate_pods d USING (pod_id)
"""

duplicate_rows = con.execute(q).fetchone()[0]

print(f"Rows belonging to duplicated pods: {duplicate_rows:,}")


# ------------------------------------------------------------
# 4. Within-pod variation
# ------------------------------------------------------------

print("\n=== WITHIN-POD VARIATION ===")

columns = [
    "workload_id",
    "server_id",
    "gpu_spec_public",
    "priority_class",
    "job_type_public",
    "model_type_public",
    "is_genai_request",
    "gpu_request",
    "duration_hours",
    "schedule_delay_sec",
    "ready_delay_sec",
    "ready_status",
    "schedule_status",
]

for col in columns:

    q = f"""
    WITH variation AS (
        SELECT
            s.pod_id,
            COUNT(DISTINCT COALESCE(CAST(s.{col} AS VARCHAR), '__NULL__')) AS n
        FROM read_parquet('{PARQUET}') s
        INNER JOIN duplicate_pods d USING (pod_id)
        GROUP BY s.pod_id
    )
    SELECT COUNT(*)
    FROM variation
    WHERE n > 1
    """

    changing = con.execute(q).fetchone()[0]
    pct = 100.0 * changing / n_dup if n_dup else 0

    print(
        f"{col:<24} "
        f"{changing:>10,} pods change "
        f"({pct:6.2f}%)"
    )


# ------------------------------------------------------------
# 5. Candidate key uniqueness
# ------------------------------------------------------------

print("\n=== CANDIDATE KEY UNIQUENESS ===")

total_rows = con.execute(
    f"SELECT COUNT(*) FROM read_parquet('{PARQUET}')"
).fetchone()[0]

keys = [
    ["pod_id"],
    ["pod_id", "server_id"],
    ["pod_id", "workload_id"],
    ["pod_id", "server_id", "workload_id"],
    ["pod_id", "server_id", "duration_hours"],
    ["pod_id", "workload_id", "duration_hours"],
]

for key in keys:

    fields = ", ".join(key)

    q = f"""
    SELECT COUNT(*)
    FROM (
        SELECT DISTINCT {fields}
        FROM read_parquet('{PARQUET}')
    )
    """

    unique = con.execute(q).fetchone()[0]

    print(
        f"{' + '.join(key):<45}"
        f"{unique:>12,} / {total_rows:,} "
        f"({100.0 * unique / total_rows:6.3f}%)"
    )


# ------------------------------------------------------------
# 6. Exact duplicate rows
# ------------------------------------------------------------

print("\n=== EXACT ROW DUPLICATION ===")

q = f"""
SELECT COUNT(*) - COUNT(*)
FROM read_parquet('{PARQUET}')
"""

# More efficient formulation: group all physical columns and count extras.
schema = con.execute(
    f"DESCRIBE SELECT * FROM read_parquet('{PARQUET}')"
).fetchall()

all_cols = [row[0] for row in schema]

quoted_cols = ", ".join(
    '"' + c.replace('"', '""') + '"'
    for c in all_cols
)

q = f"""
SELECT COALESCE(SUM(n - 1), 0)
FROM (
    SELECT COUNT(*) AS n
    FROM read_parquet('{PARQUET}')
    GROUP BY {quoted_cols}
    HAVING COUNT(*) > 1
)
"""

exact_removable = con.execute(q).fetchone()[0]

print(f"Exact duplicate rows removable: {exact_removable:,}")


# ------------------------------------------------------------
# 7. Top repeated pods
# ------------------------------------------------------------

print("\n=== TOP REPEATED PODS ===")

print(
    con.execute("""
        SELECT pod_id, row_count
        FROM duplicate_pods
        ORDER BY row_count DESC
        LIMIT 20
    """).df().to_string(index=False)
)


# ------------------------------------------------------------
# 8. Save a small audit artifact
# ------------------------------------------------------------

con.execute("""
COPY (
    SELECT pod_id, row_count
    FROM duplicate_pods
    ORDER BY row_count DESC
)
TO 'duplicate_pod_counts.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD)
""")

print("\n=== SAVED ===")
print("asi_audit.duckdb")
print("duplicate_pod_counts.parquet")

if os.path.exists(DB):
    print(
        f"DuckDB database size: "
        f"{os.path.getsize(DB) / 1024**2:.2f} MiB"
    )

if os.path.exists("duplicate_pod_counts.parquet"):
    print(
        f"Duplicate counts size: "
        f"{os.path.getsize('duplicate_pod_counts.parquet') / 1024**2:.2f} MiB"
    )

con.close()