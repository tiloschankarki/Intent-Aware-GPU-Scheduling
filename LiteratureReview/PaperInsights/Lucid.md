# Lucid: A Non-intrusive, Scalable and Interpretable Scheduler for Deep Learning Training Jobs

## Problem

GPU clusters suffer from low utilization because job duration is hard to estimate and intrusive profiling can be expensive or impractical.

## Main Contribution

Lucid provides a lightweight and interpretable scheduler that predicts job duration from historical execution data without intrusive profiling.

## ML or AI Model Used

Lucid is not centered on a novel ML model. It relies on historical duration forecasting and interpretable scheduling logic.

## Inputs or Signals

- Historical job executions
- Scheduling history
- Past duration patterns

## Outputs

- Predicted job duration
- Scheduling guidance for job packing

## Scheduling Strategy

Lucid uses historical duration prediction to improve scheduling and job packing while remaining non-intrusive.

## Strengths

- Lightweight.
- Interpretable.
- Non-intrusive.
- Easier to deploy than systems requiring expensive profiling.
- Shows that historical execution information alone can improve scheduling.

## Limitations

- Depends heavily on historical similarity.
- Does not use semantic understanding.
- Does not use explicit user intent.

## Relation to My Research

Lucid shows that historical information alone improves scheduling. My hypothesis is that combining history, metadata, and user intent will outperform history alone.

## Biggest Takeaway

Historical execution information is valuable. The remaining question is whether explicit user intent adds predictive value beyond history.
