# Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning

## Problem

Static GPU allocation causes inefficient resource utilization because deep learning workload performance changes during training.

## Main Contribution

Pollux introduces goodput optimization, dynamically reallocating GPUs during execution to maximize overall training efficiency.

## ML or AI Model Used

Pollux does not center on a predictive ML model. It is best understood as an optimization-based goodput scheduler.

## Inputs or Signals

- Batch size
- Learning rate
- Number of GPUs
- Worker placement
- Runtime throughput
- Training statistics

## Outputs

- Dynamic GPU allocation
- Runtime resource adaptation decisions

## Scheduling Strategy

Pollux performs adaptive runtime scheduling based on goodput optimization. It changes resource allocation after execution has already started.

## Strengths

- Runtime adaptation.
- Elastic GPU allocation.
- Better utilization.
- Improved throughput.
- Shows that scheduler decisions should respond to changing job behavior.

## Limitations

- No predictive ML model for pre-execution scheduling.
- No workload semantics.
- No explicit user intent.
- Focused mainly on runtime optimization after the job starts.

## Relation to My Research

Pollux optimizes scheduling after execution starts. My work focuses on improving scheduling before execution starts. The two approaches could complement each other: better initial predictions could reduce avoidable adaptation, while runtime adaptation could correct remaining prediction error.

## Biggest Takeaway

Runtime adaptation is useful. The open question is whether better pre-execution prediction can reduce the need for later adaptation.
