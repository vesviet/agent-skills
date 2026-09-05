# Adversarial Code Review Rubric & AI Bug Detection — Reference

This reference establishes the 2027 Adversarial Code Review standard designed to uncover subtle AI bugs, eliminate "vibe slop", detect resource leaks, verify backward compatibility, and secure the software supply chain.

---

## 1. Adversarial Review Rubric & Anti-"Vibe Slop" Protocol

### 1.1 What is "Vibe Slop"?
In modern agentic development, AI-generated code often possesses pristine syntax, impeccable formatting, high unit test counts, and extensive docstrings, yet contains fatal structural defects:
- **Phantom Validations**: Validation routines that evaluate regexes or conditions whose return values are never checked or that trivially evaluate to true.
- **Silent Error Swallowing**: Indiscriminate `try { ... } catch (e) { return null; }` or empty catch blocks that suppress underlying infrastructure failures and corrupt downstream state.
- **Mock Collusion**: Tests that mock out the faulty logic or tautologically assert what the mock returns rather than verifying genuine system behavior.
- **Hollow Abstractions**: Multi-layered factory patterns or interfaces wrapping a single function that do not isolate failure domains or add domain value.

### 1.2 The Adversarial Mindset
Reviewers must adopt an adversarial posture: **Assume the diff was generated to pass the build and tests with minimal effort rather than genuine correctness.**
- Do not trust green test suites until you verify the test assertions and test independence.
- Verify whether the code behaves correctly under failure, network partition, and corrupted input conditions.

---

## 2. AI Bug Detection Heuristics

AI models suffer from characteristic cognitive biases and defect patterns. Audit diffs specifically for these signatures:

| Defect Pattern | Manifestation | Adversarial Audit Method |
|---|---|---|
| **Hallucinated APIs & Options** | Use of plausible-sounding function names, flags, or configuration keys that do not exist in the referenced package version. | Verify function signature against the exact pinned dependency version docs or installed typings. |
| **Async & Concurrency Hazards** | Missing `await`, unhandled Promise rejections, race conditions in shared mutable state, missing lock releases in error branches. | Trace all error paths inside async functions; verify mutex unlock in `defer` / `finally` blocks. |
| **Context-Window Truncation** | Dropped `switch` cases, missing enum branch handlers, or half-refactored methods where old and new parameters collide. | Compare the modified block against the original file; check for dropped default or edge branches. |
| **Over-Defensive Null Coalescing** | Liberal use of `?.` and `?? []` masking `null`/`undefined` bugs until deep in the call stack. | Question why an expected required value could be nil; eliminate defensive masking at the root. |
| **Tautological Assertions** | Tests asserting `expect(mockService.call).toHaveBeenCalled()` without verifying output correctness. | Reject tests that only verify mock invocation without validating state transitions. |

---

## 3. Systematic Resource Leak Audit

Examine every lifecycle boundary to ensure complete resource cleanup under both success and error paths:

### 3.1 File Descriptors & Network Streams
- **HTTP Response Bodies**: Ensure response bodies are explicitly drained and closed (e.g. `resp.Body.Close()` in Go, stream destruction in Node.js, `with` context managers in Python).
- **File Handles**: Files must be opened within scoped resource blocks or explicitly closed in `finally` blocks.

### 3.2 Concurrency & Worker Lifecycles
- **Goroutine / Thread Leaks**: Ensure every spawned background worker listens to a cancellation context (`ctx.Done()`) or termination channel. Reject unmanaged background spawns.
- **Worker Pools & Queues**: Verify thread pools, task runners, and queues have explicit shutdown and flush routines.

### 3.3 Memory & Connection Management
- **Unbounded Collections**: In-memory caches, lookup tables, and maps must have size limits and TTL eviction policies.
- **Event Listeners**: Verify event listeners, pub/sub subscriptions, and socket hooks are deregistered when objects are destroyed.
- **Database Connection Pools**: Ensure transactions and client handles are released back to the pool in error/defer branches. Confirm connection acquisition timeouts are configured.

---

## 4. Backward Compatibility & Wire Verification

Public interfaces and persisted structures must guarantee zero-downtime evolution:

### 4.1 Public APIs & Protocols
- **Additive Evolution**: New fields must be optional or have backwards-compatible defaults.
- **Forbidden Changes**: Never remove fields, narrow types, or alter serialized JSON key casing on active API versions.
- **Enum Changes**: Adding enum variants must account for existing clients whose parsers fail on unknown enums.

### 4.2 Database Migrations (Expand / Contract Pattern)
- **Zero-Downtime Rule**: Single-phase column renames or destructive drops are forbidden.
- **Phase 1 (Expand)**: Add new column as nullable; dual-write to old and new columns.
- **Phase 2 (Backfill & Migrate)**: Asynchronously backfill historical records; transition reads to new column.
- **Phase 3 (Contract)**: Stop writing to old column and deprecate/drop in a subsequent release.

---

## 5. Supply Chain Security (OWASP ASI04 & ASI05)

Third-party dependencies represent an acute attack vector in autonomous SWE:

- **Typosquatting Verification**: Scrutinize all newly introduced package names for phonetic or orthographic similarity to popular packages (e.g. `cross-env` vs `crossenv`).
- **Lockfile Integrity**: Ensure lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`, `go.sum`) are committed alongside manifest changes. Flag unpinned version specifiers (`*`, `latest`, unbounded ranges).
- **Install Hook Audit**: Scrutinize packages containing lifecycle scripts (`postinstall`, `preinstall`, `setup.py`, `build.rs`). Verify they do not execute untrusted external network requests or shell scripts.
- **Provenance & Age**: Review repository stars, maintainer activity, and package publication date. New packages published within days or weeks must be flagged for security lead review.
