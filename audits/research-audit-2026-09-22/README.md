# Public GPU/ML trace audit evidence — 2026-09-22

These are descriptive data-audit outputs, not prediction results.

- `coverage.json`: raw-file counts for Acme, Helios, Alibaba PAI 2020, 2023 and 2025. GPU cohorts use a positive GPU request/count as appropriate; these are not universally completed jobs.
- `pai-eligible-coverage.json`: PAI tasks with positive requested GPUs, finite recorded start/end, positive duration, status Terminated, and literal task_name in worker/ps/evaluator; joined to the job and group tables. This cohort is conditional on successful completion. No model was fitted.
- `nasbench-prefix-audit.json`: ONLY the first 4 MiB of the full NAS-Bench-101 file, which contains epoch-4 records. Whole-dataset budget coverage is documented by the authors, not measured by this prefix sample.
- `source-manifest.json`: downloaded evidence sizes, sources and SHA-256 hashes. It is a download manifest, not a complete search log. Raw downloads remain in /tmp/gpu-scope-audit and are not copied into this project.

Additional direct MIT counts: slurm-log.csv has 395914 rows and 29 columns; labelled_jobids.csv has 3430 rows, all joining to the scheduler table. All 3430 have job_type OTHER, id_array_task 4294967294, and the same anonymized id_array_job. They span three anonymized users. The documentation's counts describe a different reported total and must not be substituted for these file counts.

No provenance-ambiguous field has been certified as prospective merely from its name. The written report distinguishes platform task-role inputs from job-level experiment objectives.
