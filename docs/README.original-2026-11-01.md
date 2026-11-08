# Intent-Aware GPU Scheduling

**Status: Work in Progress**

This repository contains the work I have been doing around GPU scheduling and resource prediction. Right now, it mainly contains my paper notes, literature comparison, research gap, and the research idea I am trying to develop.

The idea started while I was reading papers about GPU clusters and HPC systems. One problem that kept coming up was resource allocation. Users have to request things like GPUs, memory, and expected runtime before their jobs run, but those estimates are not always accurate. If someone asks for too much, resources can sit unused. If they ask for too little, the job might fail or take longer than expected.

A lot of research already tries to solve this using job history, metadata, profiling, runtime information, and more recently even LLMs.

While reading these papers, one thing I kept thinking about was:

> **What if the scheduler also knew why the user was running the job?**

That became the starting point for this research idea.

## The idea

Two users can submit technically similar jobs but have completely different goals.

For example, one person might be testing an idea:

> "This is just an exploratory run. I don't care if it takes longer and I don't want to use more GPUs than necessary."

Another person could be running the final experiment for a paper:

> "This is my final training run and I need the results before tomorrow."

The jobs might look similar based on normal metadata, but the intent behind them is different.

My idea is to see whether this kind of information can actually help with resource prediction and scheduling.

The current research question is:

> **Can user intent, together with job history and metadata, improve resource prediction and GPU scheduling using a relatively lightweight ML model?**

I specifically want to see whether user intent gives us useful information that we cannot already get from job history and metadata.

## What I have looked at so far

I started by reading work around resource prediction and GPU scheduling.

### Liquid

Liquid was important because it showed that machine learning can predict resource requirements before scheduling. It uses information about the training job and predicts the resources it will need.

This made me interested in the idea of putting a prediction layer **before** the scheduler.

### Pollux

Pollux takes a different approach. Instead of trying to make the perfect decision before the job starts, it watches how training is going and changes GPU allocation while the job is running.

This made me think that the two ideas could work together.

A better prediction could give the scheduler a better starting point, while something like Pollux could still adjust resources later if the prediction was wrong.

### Lucid

Lucid was interesting because it uses previous job history to help predict how long future jobs will take.

It is also relatively lightweight and does not require expensive profiling.

This gives me an important comparison for my idea:

**If history already works well, does adding user intent actually make it better?**

### SchedMate

SchedMate is probably the closest paper I have found to this idea so far.

It uses LLMs along with information such as user prompts, source code, logs, previous jobs, and hardware information to give better information to the scheduler.

This changed my original idea quite a bit.

At first, I was thinking more broadly about using semantic information for scheduling. But SchedMate already explores that direction.

So the question became more specific:

**Can we take explicit user intent, represent it in a simpler way, and find out whether it adds useful information without needing an LLM to understand the entire job?**

That is where the project currently stands.

## What do I mean by "intent"?

I am still working on the exact definition.

Some examples could be:

- Is this an exploratory experiment or a final run?
- Is there actually a deadline?
- How flexible is that deadline?
- Is finishing quickly more important than saving resources?
- Can the job be interrupted?
- Is reproducibility important for this run?
- Would the user accept different hardware if it means waiting less?

Not all of these will necessarily be useful.

Part of the research is figuring out which information actually matters instead of simply asking users for more information.

I also don't want "intent" to just become another priority system where everyone says their job is important. It needs to provide something useful that the scheduler cannot already figure out from normal job information.

## What I am thinking of building

The current idea is not to build an entirely new GPU scheduler.

Instead, I want to build something that sits before an existing scheduler:

```text
User Intent
     +
Job Metadata
     +
Previous Jobs
     |
     v
Lightweight ML Model
     |
     v
Resource Prediction
     |
     v
Existing Scheduler
```

The model could help predict things like GPU requirements, memory requirements, or runtime.

The scheduler itself could stay mostly unchanged.

This is one of the ideas I liked from some of the papers I read: instead of replacing the whole scheduling system, give it better information.

## How I would test it

The most important experiment for me is actually pretty simple.

I want to compare:

```text
Job information only

vs.

Job information + history

vs.

Job information + history + user intent
```

If the third version performs better, then I can look at **how much better it is and why**.

If it doesn't perform better, that is useful too because it would show that user intent may not provide enough extra information to justify collecting it.

Some things I would like to measure are:

- prediction error
- GPU utilization
- wasted GPU time
- queue time
- job completion time
- failed or restarted jobs

I will most likely start with existing workload traces and simulation instead of trying to get access to a large GPU cluster immediately.

## Research gap so far

I want to be careful about claiming that nobody has done this before.

There is already a lot of work using:

- job history
- metadata
- user resource estimates
- runtime information
- profiling
- source code
- logs
- semantic information

There are also real schedulers that already use things like priorities, queues, deadlines, and QoS rules.

So my claim is **not** that schedulers have never used information from users.

What I have found so far is that **explicit user intent seems to be less explored as its own input**, separate from resource estimates, job history, code, logs, and runtime information.

That is the gap I am currently investigating, and it may change as I read more papers.

## Current progress

So far I have:

- read and taken detailed notes on several related papers
- compared their inputs, models, scheduling methods, and limitations
- created a literature comparison table
- worked on identifying the research gap
- narrowed down the original idea
- formed an initial research question

The next steps are to read more of the closest related work, define exactly what counts as user intent, find a suitable workload dataset, and start designing the first experiment.

## Repository

Most of the repository right now is my research notes.

```text
LiteratureReview/
    Comparison_Table.md
    research_gap_summary.md

    PaperInsights/
        SchedMate.md
        Liquid.md
        Pollux.md
        Lucid.md
```

I will add the proposal, experiments, code, and results as the project develops.

## Papers currently shaping this idea

Some of the papers I am currently using as starting points are:

- SchedMate: Semantic-Aware Scheduling for GPU Clusters with Large Language Models
- Liquid: Intelligent Resource Estimation and Network-Efficient Scheduling for Deep Learning Jobs
- Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning
- Lucid: A Non-intrusive, Scalable and Interpretable Scheduler for Deep Learning Training Jobs
- Helping HPC Users Specify Job Memory Requirements via Machine Learning

There are several others I still need to study more closely.

---

This is an ongoing research project, so the research question, approach, and even the main idea may change as I learn more and start experimenting.

For now, this repository is mainly a record of **how the idea is developing and where I am with it.**
