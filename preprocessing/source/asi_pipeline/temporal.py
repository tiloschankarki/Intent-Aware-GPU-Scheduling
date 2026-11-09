"""Source-backed validation of the historical D109H00 map."""
import duckdb
import pyarrow.parquet as pq


def verify_legacy(source, legacy, valid_labels, memory_limit='1GB', threads=2):
    """One narrow source scan, restricted to legacy IDs before aggregation.

    Returns a sorted Arrow table and diagnostics. Does not mutate any file.
    Multiplicity is counted from source rows, never inferred from an audit table.
    """
    con = duckdb.connect(':memory:')
    try:
        con.execute('SET memory_limit = ?', [memory_limit])
        con.execute('SET threads = ?', [threads])
        table = pq.read_table(legacy)
        if set(table.column_names) != {'pod_id','first_seen_day','first_seen_hour'}:
            raise ValueError('Unexpected legacy map schema')
        con.register('legacy', table)
        total, distinct, bad = con.execute('''SELECT count(*), count(DISTINCT pod_id),
            count(*) FILTER (WHERE pod_id IS NULL OR first_seen_day IS NULL OR first_seen_hour IS NULL
              OR first_seen_day != 109 OR first_seen_hour != 0) FROM legacy''').fetchone()
        if not total or total != distinct or bad:
            raise ValueError('Legacy map has duplicate/null IDs or unexpected timestamps')
        con.execute('''CREATE TEMP TABLE matched AS
            SELECT s.pod_id, count(*) AS source_count,
                   min(s.job_type_public) AS job_type_public
            FROM read_parquet(?) s SEMI JOIN legacy l ON s.pod_id=l.pod_id
            GROUP BY s.pod_id''', [str(source)])
        found, repeated = con.execute('SELECT count(*), count(*) FILTER (WHERE source_count>1) FROM matched').fetchone()
        missing = total - found
        invalid = con.execute('''SELECT count(*) FROM matched WHERE source_count=1
            AND (job_type_public IS NULL OR job_type_public NOT IN (SELECT unnest(?)))''', [valid_labels]).fetchone()[0]
        if missing or invalid:
            raise ValueError(f'Source verification failed: missing={missing}, invalid_unique_labels={invalid}')
        eligible = con.execute('''SELECT l.pod_id, l.first_seen_day, l.first_seen_hour,
            m.job_type_public FROM legacy l JOIN matched m USING(pod_id)
            WHERE m.source_count=1 ORDER BY l.pod_id''').to_arrow_table()
        labels = dict(con.execute('''SELECT job_type_public,count(*) FROM matched
            WHERE source_count=1 GROUP BY job_type_public ORDER BY job_type_public''').fetchall())
        return eligible, {'legacy_pods':total, 'source_matched_pods':found,
            'missing_source_pods':missing, 'excluded_repeated_pods':repeated,
            'invalid_unique_lifecycle_labels':invalid, 'eligible_pods':eligible.num_rows,
            'eligible_lifecycle_counts':labels,
            'method':'one source pod_id/job_type_public scan; semi-join legacy IDs; count every source occurrence; retain count=1'}
    finally:
        con.close()
