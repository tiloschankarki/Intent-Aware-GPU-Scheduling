# Reproducible cloud continuation — NOT EXECUTED

This is the same post-hoc internal split-sensitivity experiment, not independent external replication. No cloud machine has been provisioned, charged, or trained by this audit.

## Resource and scientific contract

Use a dedicated Linux CPU machine with at least 16 GiB RAM, 4 vCPUs and 20 GiB free disk. No GPU is needed. Run one candidate at a time, with the original two LightGBM threads. Use the container limit below to leave host headroom. If that host fails its memory checks or is OOM-killed, preserve logs and stop; do not reduce rows, features, candidates or boosting budget.

Preserve the existing split files and their SHA-256 hashes; do not reconstruct the split. Use model seed 20260927, split seed 20261020, original M0 R+P+A and M1 R+P+A+O, train-only categorical encoding, all 12 candidates per role, 200 maximum rounds, 30-round early stopping, and lowest-candidate-index tie breaking. No train+validation refit is added. `run_experiment.py` directly calls the unchanged archived `execution.fit_candidate` and encoding helpers. It writes every candidate model, parameters, validation score and timing, then freezes BOTH selections before any test access.

The Python 3.12.2 container and requirements pin the Mac experiment's package versions, including LightGBM 4.7.0. The image has not been built here. Package/image availability and successful installation must be verified during build; do not substitute versions silently. Save the built image ID/digest and package listing. Architecture and OS differences must be reported; no bitwise cross-platform equivalence is claimed. Several supporting versions already differ from the original Windows archive, as recorded in environment.json.

## Phase 1: deploy only this selection package

This directory contains train/validation Parquet files, original pipeline code, configuration, metadata and runner. It contains NO test Parquet, canonical Parquet or original object archive. The split audit includes only the expected test count/hash/path, not its contents. Upload only the selection tarball, not the whole experiment directory. No upload has been performed.

On the cloud host after extracting the tarball:

```sh
cd cloud_package
sha256sum --check SHA256SUMS
mkdir -p ../cloud-results ../cloud-logs
docker build -t asi-robustness:20261020 . > ../cloud-logs/build.log 2>&1
docker image inspect asi-robustness:20261020 > ../cloud-logs/image.json
docker run --rm --entrypoint pip asi-robustness:20261020 freeze > ../cloud-logs/packages.txt
free -b > ../cloud-logs/memory-before.txt
```

Require at least 12 GiB available before starting this dedicated 16 GiB host. This is a new-host operational requirement, not a change to the scientific protocol or the Mac cap. Docker's 10 GiB memory limit and equal swap limit below disable container swap and leave host headroom. Confirm Docker supports and enforces those limits on the chosen host.

```sh
docker create --name asi-selection-20261020 \
  --cpus 2 --memory 10g --memory-swap 10g --network none \
  --mount "type=bind,src=$PWD,dst=/app,readonly" \
  --mount "type=bind,src=$(cd ../cloud-results && pwd),dst=/results" \
  asi-robustness:20261020 select --out /results/run

docker start asi-selection-20261020
while [ "$(docker inspect -f '{{.State.Running}}' asi-selection-20261020)" = true ]; do
  date -u '+%Y-%m-%dT%H:%M:%SZ' >> ../cloud-logs/memory.log
  docker stats --no-stream --format '{{json .}}' asi-selection-20261020 >> ../cloud-logs/memory.log
  free -b >> ../cloud-logs/memory.log
  sleep 1
done
docker wait asi-selection-20261020 > ../cloud-logs/exit-code.txt
docker logs asi-selection-20261020 > ../cloud-logs/training.log 2>&1
docker inspect asi-selection-20261020 > ../cloud-logs/container.json
```

Stop if exit code is not zero, OOMKilled is true, either role is missing, or any hash check fails. Leave the stopped container/logs available for inspection. Do not interpret a partial selection as a successful experiment.

Verify the freeze with the same image and read-only mounts:

```sh
docker run --rm --network none \
  --mount "type=bind,src=$PWD,dst=/app,readonly" \
  --mount "type=bind,src=$(cd ../cloud-results && pwd),dst=/results,readonly" \
  asi-robustness:20261020 verify-freeze --out /results/run
```

The verifier requires complete 12-candidate records for both roles, the original parameter grid and feature definitions, validation-only selection, minimum-score/tie-break agreement, selected-model equality to the winning candidate, matching configuration and hashes for every frozen artifact. Save the terminal output.

## Phase 2: release held-out data only after both selections freeze

Download all frozen results and logs for review and run the verifier again. Only after successful verification may the separately held test file be made readable and securely transferred to a separate cloud directory. Its required SHA-256 is in `split_audit.json`. The local `sealed_test/test.parquet` remains mode 000 now; no release or upload has happened. Restore mode 000 after transfer. Never put test data into the selection package or restart selection after test inspection.

Mount the test directory only into the evaluation container:

```sh
# TEST_DIRECTORY must be an absolute directory containing the hash-matched test.parquet.
docker run --name asi-evaluation-20261020 \
  --cpus 2 --memory 10g --memory-swap 10g --network none \
  --mount "type=bind,src=$PWD,dst=/app,readonly" \
  --mount "type=bind,src=$(cd ../cloud-results && pwd),dst=/results" \
  --mount "type=bind,src=$TEST_DIRECTORY,dst=/heldout,readonly" \
  asi-robustness:20261020 evaluate --out /results/run --test /heldout/test.parquet \
  > ../cloud-logs/evaluation.log 2>&1
```

The evaluation runner validates BOTH frozen selections before opening test data, verifies the test-file hash, row/workload counts and disjointness, and never trains a model. It saves M0/M1 predictions, execution-weighted and equal-workload LogMAE, absolute and percentage improvements, and paired workload-bootstrap 95% intervals (1,000 replicates, seed 20260927). Positive improvement favors M1. Raw log predictions are scored against log1p(duration_hours), without clipping. The bootstrap conditions on one pair of fitted models; it does not establish external replication or training-seed stability.

Archive the entire `cloud-results/` and `cloud-logs/` directories, image digest, runner and input checksums. Success requires actual completed selections, valid FREEZE.json, both final prediction files and a valid evaluation/results.json—not merely a successful image build or benchmark.

## Validation performed locally

Runner syntax and fail-closed freeze/test access were checked without training scientific models or opening the sealed test. Package hashes and exclusion of held-out/canonical data were checked. Cloud image build, full selection and evaluation remain UNEXECUTED.
