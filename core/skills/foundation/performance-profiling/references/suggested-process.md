# Performance Profiling — Suggested Process (Reference)

Detailed profiling workflow extracted from `SKILL.md` to keep the main file
under 200 lines. Load this file when authoring a new profiling session,
writing an incident postmortem, or training a new performance engineer.

## First Questions To Answer

1. What symptom matters most: latency, throughput, CPU, memory, or contention?
2. Under what workload does it happen?
3. Is the issue local to one code path, one dependency, or one environment?
4. What is the current baseline?
5. What metric will prove the change helped?

## Step 1: Define The Baseline

Capture the current state before changing code:

- median and tail latency
- throughput
- error rate
- CPU and memory usage
- allocation or query counts when relevant

Use the repo's normal observability and benchmark tools where possible.

## Step 2: Reproduce The Problem

Find the smallest repeatable workload that exposes the issue:

- one endpoint or handler
- one background job
- one query-heavy path
- one batch or import path

If you cannot reproduce it, reduce the scope until you can.

## Step 3: Identify The Hot Path

Use the local profiling tools that fit the stack, such as:

- language-native CPU or heap profilers
- benchmark or microbenchmark tools
- tracing or flame graphs
- query analyzers
- load-testing tools

Look for:

- expensive functions
- repeated allocations
- lock contention
- chatty network calls
- slow queries
- repeated serialization or parsing work

## Step 4: Form A Narrow Hypothesis

Examples:

- a query pattern is causing N+1 behavior
- repeated object allocation is driving GC pressure
- an external dependency is dominating latency
- a lock or queue is throttling concurrency
- payload size is causing serialization overhead

Test one hypothesis at a time.

## Step 5: Apply The Smallest Meaningful Optimization

Prefer targeted fixes such as:

- batching or pagination
- caching
- reducing duplicate work
- narrowing lock scope
- reusing objects where appropriate
- improving query shape or indexing
- moving work off the request path

Avoid broad refactors unless measurement shows they are necessary.

## Step 6: Measure Again

Re-run the same workload and compare:

- before and after latency
- before and after throughput
- memory and CPU changes
- error rate impact

If the improvement is not measurable, treat the optimization as unproven.

## Step 7: Check Secondary Effects

After optimizing, verify:

- correctness did not regress
- tail latency did not worsen
- memory use stayed acceptable
- downstream systems are not now the bottleneck

## Tool Guidance

Use the tools that match the repo and language. Examples:

- language-native profilers for CPU, memory, goroutines, threads, or heap
- benchmark commands for hot functions or packages
- tracing for cross-service latency
- query plans for data bottlenecks
- load generators for realistic traffic

If the repo already has profiling or benchmark scripts, use those first.
