# GPU Scheduler Literature Review Comparison

## Comparison Table

| Paper | Problem | Model | Inputs | Scheduling Style | Uses Intent | Main Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| SchedMate | GPU schedulers miss semantic information that could improve prediction, observability, and failure handling. | LLM-based resource estimation, embeddings, retrieval-based similarity search | User prompt, source code, runtime logs, historical jobs, hardware metrics | Advisor layer that augments an existing scheduler | No explicit intent; user prompt is treated as an input/proxy | LLM inference cost, code/log access requirements, and no distinct intent model |
| Liquid | Users overestimate resources, causing poor GPU utilization and network overhead. | Random forest resource prediction; genetic algorithm for batch scheduling | Batch size, workers, parameter servers, number of batches, training configuration | Resource prediction plus network-aware scheduling | No | Uses structured configuration only; no semantics or explicit intent |
| Pollux | Static GPU allocation fails because training performance changes during execution. | No predictive ML model; optimization-based goodput scheduler | Batch size, learning rate, GPUs, placement, runtime throughput, training statistics | Runtime adaptive goodput optimization | No | Optimizes after execution starts; no pre-execution prediction or explicit intent |
| Lucid | Poor duration estimates and intrusive profiling reduce GPU cluster utilization. | Historical duration forecasting and interpretable scheduling | Historical job executions, scheduling history, past duration patterns | Non-intrusive duration prediction for job packing | No | Depends on historical similarity; no semantic understanding or explicit intent |
| Helping HPC Users Specify Job Memory Requirements via Machine Learning | Users misestimate memory requirements, causing wasted resources or job failures. | Random forest, MLP, SVM, kNN, and ensemble voting predictor | Historical scheduler logs, job metadata, user submission information | Pre-scheduler ML prediction layer; scheduler itself is not modified | No | Predicts only memory; no scheduling optimization, semantics, or explicit intent |

## Overall Summary

The papers show a clear evolution in GPU and HPC scheduling research. Earlier work focuses on helping users or schedulers estimate a specific resource more accurately, such as memory or runtime. The memory-prediction paper is especially important because it places a lightweight prediction layer before the scheduler without modifying the scheduler itself. Liquid extends this idea into distributed deep learning by predicting a richer resource demand vector and combining that prediction with network-aware scheduling.

Later GPU-cluster schedulers shift from static prediction to adaptive scheduling. Pollux is the strongest example here: it does not try to predict everything before execution, but instead observes training behavior and reallocates GPUs dynamically using goodput optimization. Lucid takes a lighter-weight path by using historical duration forecasting to improve job packing without intrusive profiling. SchedMate moves the field toward semantic scheduling by using LLMs, embeddings, code, logs, and historical jobs to provide richer scheduling advice.

Across these papers, the dominant inputs are historical jobs, scheduler logs, structured job metadata, runtime telemetry, training configuration, code, and logs. These are all useful, and the literature already provides strong evidence that prediction and scheduling improve when these signals are used. The missing piece is explicit user intent as a separate scheduler input. User resource estimates are not the same as intent. Code and log semantics are also not the same as intent. A user prompt can contain intent, but SchedMate still appears to use it mainly as semantic context rather than as a structured, first-class scheduling signal.

The evolved research idea is therefore viable if stated carefully: build a lightweight pre-scheduling advisor that augments existing schedulers using explicit user intent, historical job information, and structured metadata. The safe claim is not that no prior work uses user signals. The safer and stronger claim is that explicit user intent appears underexplored in the papers examined so far, especially as a distinct input separated from resource estimates, historical traces, queue metadata, code semantics, and runtime telemetry.

The research question becomes:

> Can explicit user intent, combined with historical job information and structured metadata, improve resource-demand prediction and scheduling decisions while using a lightweight ML model instead of expensive semantic analysis?
