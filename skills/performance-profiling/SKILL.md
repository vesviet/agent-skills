---
name: performance-profiling
description: Investigate latency, throughput, memory, and contention issues by baselining, profiling hot paths, and validating improvements with repo-local tools
---

# Performance Profiling Skill

Use this skill when investigating slow paths, memory growth, concurrency bottlenecks, or capacity limits.

## When to Use

- latency is rising or unstable
- throughput is lower than expected
- memory usage keeps growing
- CPU spikes under load
- a change needs before/after performance comparison
- a service is approaching scaling or capacity limits

## Core Rules

- baseline before optimizing
- profile the real hot path, not an assumed one
- prefer repo-local and language-native tooling first
- do not profile production without explicit approval and a safety plan
- validate improvements with repeatable measurements, not intuition

## First Questions To Answer

1. What symptom matters most: latency, throughput, CPU, memory, or contention?
2. Under what workload does it happen?
3. Is the issue local to one code path, one dependency, or one environment?
4. What is the current baseline?
5. What metric will prove the change helped?

## Suggested Process

### Step 1: Define The Baseline

Capture the current state before changing code:

- median and tail latency
- throughput
- error rate
- CPU and memory usage
- allocation or query counts when relevant

Use the repo's normal observability and benchmark tools where possible.

### Step 2: Reproduce The Problem

Find the smallest repeatable workload that exposes the issue:

- one endpoint or handler
- one background job
- one query-heavy path
- one batch or import path

If you cannot reproduce it, reduce the scope until you can.

### Step 3: Identify The Hot Path

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

### Step 4: Form A Narrow Hypothesis

Examples:

- a query pattern is causing N+1 behavior
- repeated object allocation is driving GC pressure
- an external dependency is dominating latency
- a lock or queue is throttling concurrency
- payload size is causing serialization overhead

Test one hypothesis at a time.

### Step 5: Apply The Smallest Meaningful Optimization

Prefer targeted fixes such as:

- batching or pagination
- caching
- reducing duplicate work
- narrowing lock scope
- reusing objects where appropriate
- improving query shape or indexing
- moving work off the request path

Avoid broad refactors unless measurement shows they are necessary.

### Step 6: Measure Again

Re-run the same workload and compare:

- before and after latency
- before and after throughput
- memory and CPU changes
- error rate impact

If the improvement is not measurable, treat the optimization as unproven.

### Step 7: Check Secondary Effects

After optimizing, verify:

- correctness did not regress
- tail latency did not worsen
- memory use stayed acceptable
- downstream systems are not now the bottleneck

## Tool Guidance

Use the tools that match the repo and language.

Examples:

- language-native profilers for CPU, memory, goroutines, threads, or heap
- benchmark commands for hot functions or packages
- tracing for cross-service latency
- query plans for data bottlenecks
- load generators for realistic traffic

If the repo already has profiling or benchmark scripts, use those first.

## Production Safety

If profiling a shared or production environment:

- get explicit approval first
- use the least invasive method that answers the question
- keep profiling duration short
- make sure profiling endpoints or admin tooling are access-controlled
- coordinate with owners if the workload is customer-facing

## Common Performance Patterns

### Request Path Bottlenecks

- repeated downstream calls
- repeated serialization
- oversized payloads
- synchronous work that could be deferred

### Data Bottlenecks

- N+1 reads
- missing indexes
- large scans
- long transactions

### Memory Bottlenecks

- repeated allocations
- retained references
- goroutine or worker leaks
- unbounded buffers or caches

### Concurrency Bottlenecks

- coarse locks
- queue buildup
- insufficient backpressure
- too much parallelism on a shared dependency

## What To Capture In Your Output

When reporting performance work, include:

- workload used
- baseline metrics
- hotspot identified
- optimization applied
- measured result after the change
- remaining risks or next bottlenecks

## Checklist

- [ ] baseline recorded
- [ ] issue reproduced
- [ ] hot path identified with measurement
- [ ] narrow hypothesis tested
- [ ] optimization applied
- [ ] before/after comparison recorded
- [ ] correctness and secondary effects checked

## Related Skills

- **troubleshoot-service**: Debug runtime and dependency issues
- **review-code**: Review risky optimizations and trade-offs
- **write-tests**: Add regression or benchmark coverage
- **navigate-service**: Map the hot path before optimizing
- **meeting-review**: Review performance trade-offs across roles
