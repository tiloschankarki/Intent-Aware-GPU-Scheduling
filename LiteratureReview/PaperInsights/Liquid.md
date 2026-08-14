# Liquid: Intelligent Resource Estimation and Network-Efficient Scheduling for Deep Learning Jobs

## Problem

Users frequently overestimate resource requirements for distributed deep learning jobs. This causes poor GPU utilization and unnecessary network communication overhead.

## Main Contribution

Liquid combines ML-based resource estimation with network-aware scheduling to improve GPU utilization and reduce job completion time.

## ML or AI Model Used

- Random forest resource prediction
- Compared against linear regression, decision tree, and AdaBoost
- Genetic algorithm for batch-job scheduling

## Inputs or Signals

- Batch size
- Number of workers
- Number of parameter servers
- Number of batches
- Training configuration
- Structured job metadata

## Outputs

- Resource demand vector
- GPU utilization estimate
- Network bandwidth usage estimate

## Scheduling Strategy

Liquid uses different scheduling strategies for different job types:

- Immediate jobs use Best-Fit scheduling.
- Batch jobs use a genetic algorithm.
- Scheduling is network-aware and uses predicted resource demand.

## Strengths

- Accurate resource prediction.
- Reduces network overhead.
- Improves cluster utilization.
- Improves job completion time.
- Strong evidence that pre-scheduling ML prediction can help scheduling.

## Limitations

- Heavy scheduling optimization.
- Focuses mainly on structured configuration data.
- Does not use workload semantics.
- Does not use explicit user intent.

## Relation to My Research

Liquid validates that ML before scheduling works. My research extends this direction by adding user intent, historical metadata, and lightweight prediction before scheduling.

## Biggest Takeaway

Better resource prediction leads to better scheduling. The missing signal is explicit user intent.
