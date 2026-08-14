# Research Gap Summary

## Top 10 must-read papers
1. Semantic-Aware Scheduling for GPU Clusters with Large Language Models (2025, arXiv) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.
2. Liquid: Intelligent Resource Estimation and Network-Efficient Scheduling for Deep Learning Jobs on Distributed GPU Clusters (2021, IEEE Transactions on Parallel and Distributed Systems) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.
3. Sia: Heterogeneity-aware, goodput-optimized ML-cluster scheduling (2023, SOSP) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.
4. Heterogeneity-Aware Cluster Scheduling Policies for Deep Learning Workloads (2020, OSDI) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.
5. Gandiva: Introspective Cluster Scheduling for Deep Learning (2018, OSDI) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.
6. Optimus: An Efficient Dynamic Resource Scheduler for Deep Learning Clusters (2018, EuroSys) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.
7. Tiresias: A GPU Cluster Manager for Distributed Deep Learning (2019, NSDI) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.
8. Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning (2020, arXiv (Cornell University)) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.
9. Characterization and prediction of deep learning workloads in large-scale GPU datacenters (2021, SC) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.
10. Analysis of Large-Scale Multi-Tenant GPU Clusters for DNN Training Workloads (2019, arXiv (Cornell University)) - High relevance to GPU/HPC scheduling and/or strong venue; directly frames your baseline.

## Strongest evidence that history / metadata / telemetry are already used
- History and job metadata: Liquid, Improving HPC System Performance by Predicting Job Resources, 3Sigma, Tiresias, and Analysis of Large-Scale Multi-Tenant GPU Clusters all center prediction or scheduling on historical workloads, job characteristics, or trace-derived distributions.
- Telemetry/profiling: Gandiva, Pollux, Sia, Optimus, Horus, Lucid, and Host-Side Telemetry use runtime introspection, progress/goodput models, interference signals, or telemetry as scheduling/prediction inputs.
- Workload traces: SC 2021 characterization/prediction and HPCA 2022 AI-enabling workload characterization provide strong evidence that production traces are a standard empirical basis for cluster scheduling research.

## Strongest evidence that explicit user intent is underexplored
- In the examined papers so far, explicit user intent appears underexplored as a first-class scheduler input.
- Papers that involve users usually use resource estimates, job submission parameters, or incentives. Those are not the same as intent.
- New semantic/LLM papers use code/log/task semantics or natural-language constraints as proxies. These are related, but not identical to explicit user intent such as priority rationale, flexibility, deadline meaning, experiment phase, tolerance for approximation, or willingness to trade speed for cost/fairness.

## Weakest points in the novelty claim
- Semantic-aware and LLM-assisted scheduling is already emerging, so the novelty cannot be simply 'using language models for scheduling.'
- User-provided estimates have a long history in HPC schedulers and memory/runtime prediction; you must distinguish intent from estimates very explicitly.
- Some production schedulers already infer priorities from queues, accounts, QoS classes, reservations, deadlines, and fairness policies. Those are institutional intent proxies and need to be discussed.
- Several papers optimize scheduling with rich telemetry and profiling; your claim must be about the missing intent signal and its measured marginal value over those baselines.

## Recommended next steps before writing the paper
1. Read the ten must-read papers first and annotate exact input features, datasets, and limits.
2. For the semantic/LLM papers, verify whether they use user-stated goals or only semantic/code/log proxies.
3. Define a precise intent schema: deadline reason, flexibility, job criticality, experiment phase, accuracy/cost tradeoff, reproducibility need, interruption tolerance, and preferred scheduling mode.
4. Design an ablation study: metadata only; history only; telemetry/profiling only; resource estimates only; intent only; all signals combined.
5. Avoid a broad novelty claim. Claim a narrower gap: measuring whether explicit user intent improves pre-execution demand prediction and scheduling decisions beyond established history/metadata/telemetry/resource-estimate baselines.

## Closest papers to your idea
- Semantic-Aware Scheduling for GPU Clusters with Large Language Models - Closest semantic precedent; gap is to make explicit user intent a first-class, separable input and test pre-execution prediction/scheduling value.
- Liquid: Intelligent Resource Estimation and Network-Efficient Scheduling for Deep Learning Jobs on Distributed GPU Clusters - Supports history/metadata prediction baseline, but does not treat user intent separately from resource estimates.
- Helping HPC Users Specify Job Memory Requirements via Machine Learning - Supports history/metadata prediction baseline, but does not treat user intent separately from resource estimates.
- Lucid: A Non-intrusive, Scalable and Interpretable Scheduler for Deep Learning Training Jobs - Supports history/metadata prediction baseline, but does not treat user intent separately from resource estimates.
- Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning - Strong scheduling baseline; optimizes with traces/profiles/metadata but leaves explicit user intent underexplored.

## Current viability judgment
The idea still looks viable, but only as a careful marginal-contribution paper. The safe framing is not 'no one has used user signals.' The safer claim is: explicit user intent appears underexplored in the papers examined so far, especially as a distinct first-class input separated from resource estimates, queue metadata, code/log semantics, and runtime telemetry.