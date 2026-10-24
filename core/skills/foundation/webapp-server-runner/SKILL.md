---
name: webapp-server-runner
description: "Use when executing local web application test suites, managing multi-server background lifecycles via with_server.py, polling sockets for readiness, and executing Playwright browser automation with guaranteed cleanup."
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# webapp-server-runner

## Core Rules

1. **Atomic Socket Readiness Polling:** Never launch end-to-end tests using fixed sleep timers. Always poll server port sockets via `with_server.py` before beginning test execution.
2. **Multi-Server Lifecycle Coordination:** Manage backend APIs, frontend dev servers, and mock services concurrently via repeatable `--server` and `--port` CLI arguments.
3. **Guaranteed Process Termination:** All background server processes must be launched in isolated process groups (`os.setsid`) and terminated cleanly via `atexit` handlers (`SIGTERM` followed by `SIGKILL`). Zero orphan processes are tolerated.
4. **Exit Code Propagation:** The runner must strictly exit with the exact return code emitted by the executed test command, preserving CI test pass/fail semantics.
5. **Tripartite Evidence Collection on Failure:** On test failure, capture screenshot, DOM snapshot, and browser console logs via `playwright-evidence-qa`.

## Suggested Process

1. **Service Dependency Identification:** Identify required services (e.g. backend on port 8000, frontend on port 3000).
2. **Command Assembly:** Formulate the execution command using `with_server.py`:
   ```bash
   python3 scripts/with_server.py \
     --server "php artisan serve --port 8000" --port 8000 \
     --server "npm run dev -- --port 3000" --port 3000 \
     -- pytest tests/e2e/test_checkout.py
   ```
3. **Execution & Port Verification:** The runner launches processes, verifies TCP socket readiness, and executes the test command.
4. **Cleanup & Teardown:** Once complete, process groups are killed immediately, releasing socket bindings.
5. **Reporting:** Emit test results into `test-report.json`.

## Checklist

- [ ] Every required server command has a corresponding `--port` flag.
- [ ] Fixed sleep delays are eliminated in favor of atomic socket polling.
- [ ] Process cleanup handles SIGTERM/SIGINT signals cleanly without socket collisions.
- [ ] Test command returncode propagates accurately to the caller.
- [ ] Test execution failures capture tripartite evidence (screenshot + DOM + console).

## Related Skills

- **playwright-evidence-qa**: Triages test failures and captures diagnostic artifacts.
- **hostile-component-stress-testing**: Stresses frontend component behavior across hostile boundary axes.
- **interactive-component-workbench**: Runs isolated scratch-route UI tests.

## Output Contracts

When completing test suite execution, emit:
- **Test Report:** `core/contracts/schemas/test-report.json`
- **Validation Result:** `core/contracts/schemas/validation-result.json`
