# SchedMate: Semantic-Aware Scheduling for GPU Clusters with Large Language Models

## Problem

Current GPU schedulers are blind to semantic information contained in source code, runtime logs, historical jobs, and user-provided prompts. As a result, they can suffer from inaccurate runtime prediction, expensive profiling, poor observability, and weak failure handling.

## Main Contribution

SchedMate introduces an LLM-powered scheduling advisor that extracts semantic information before or around scheduling time and augments existing GPU schedulers without requiring the scheduler itself to be redesigned.

## ML or AI Model Used

- Large language models
- Embedding models
- Retrieval-based similarity search
- LLM-based resource estimation

## Inputs or Signals

- User prompt
- Source code
- Runtime logs
- Historical jobs
- Hardware metrics

## Outputs

- Predicted runtime
- Resource utilization estimates
- Failure diagnosis
- Training progress information
- Similar historical jobs
- Scheduling advice

## Scheduling Strategy

The existing scheduler remains unchanged. SchedMate acts as an intelligence layer that provides richer semantic and predictive information to improve downstream scheduling decisions.

## Strengths

- Uses semantic information that conventional schedulers ignore.
- Can reduce or replace expensive profiling.
- Improves runtime estimation and observability.
- Helps diagnose failures.
- Plug-and-play design makes it easier to add to existing systems.

## Limitations

- Heavy dependence on LLM inference.
- Increased computational cost.
- Requires access to prompts, source code, logs, or other rich context.
- Does not use explicit user intent as a distinct first-class scheduler input.

## Relation to My Research

SchedMate proves that adding a pre-scheduling intelligence layer can improve scheduling decisions. My work differs by focusing on explicit user intent, structured metadata, historical jobs, and lightweight ML instead of expensive LLM inference.

## Biggest Takeaway

Semantic information improves scheduling. The unanswered question is whether explicit user intent can provide similar benefits at significantly lower cost.
