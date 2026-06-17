---
name: sandbox-sdk
description: Builds secure, isolated code execution environments on Cloudflare Workers using the Cloudflare Sandbox SDK — enabling AI code interpreters, interactive dev environments, and sandboxed application runtimes. Use when implementing LLM-generated code execution, user-submitted script running, or any scenario requiring isolated compute with file system access on the Cloudflare edge.
---

# Sandbox SDK

Build secure, isolated code execution environments on Cloudflare Workers.

## Core Rules
- Do NOT use internal clients (`CommandClient`, `FileClient`) - use standard `sandbox.*` wrapper methods.
- The Worker entrypoint script MUST explicitly include `export { Sandbox } from '@cloudflare/sandbox'`.
- Do not skip `destroy()` calls on temporary sandboxes to avoid resource leaks.
- Keep container images lean in the Dockerfile to optimize startup and prevent cold start latency.

## Retrieval Sources

Your knowledge of the Sandbox SDK may be outdated. **Prefer retrieval over pre-training** for any Sandbox SDK task.

| Resource | URL |
|----------|-----|
| Docs | https://developers.cloudflare.com/sandbox/ |
| API Reference | https://developers.cloudflare.com/sandbox/api/ |
| Examples | https://github.com/cloudflare/sandbox-sdk/tree/main/examples |
| Get Started | https://developers.cloudflare.com/sandbox/get-started/ |

When implementing features, fetch the relevant doc page or example first.

## Required Configuration

**wrangler.jsonc** (exact - do not modify structure):

```jsonc
{
  "containers": [{
    "class_name": "Sandbox",
    "image": "./Dockerfile",
    "instance_type": "lite",
    "max_instances": 1
  }],
  "durable_objects": {
    "bindings": [{ "class_name": "Sandbox", "name": "Sandbox" }]
  },
  "migrations": [{ "new_sqlite_classes": ["Sandbox"], "tag": "v1" }]
}
```

**Worker entry** - must re-export Sandbox class:

```typescript
import { getSandbox } from '@cloudflare/sandbox';
export { Sandbox } from '@cloudflare/sandbox';  // Required export
```

## Quick Reference

| Task | Method |
|------|--------|
| Get sandbox | `getSandbox(env.Sandbox, 'user-123')` |
| Run command | `await sandbox.exec('python script.py')` |
| Run code (interpreter) | `await sandbox.runCode(code, { language: 'python' })` |
| Write file | `await sandbox.writeFile('/workspace/app.py', content)` |
| Read file | `await sandbox.readFile('/workspace/app.py')` |
| Create directory | `await sandbox.mkdir('/workspace/src', { recursive: true })` |
| List files | `await sandbox.listFiles('/workspace')` |
| Expose port | `await sandbox.exposePort(8080)` |
| Destroy | `await sandbox.destroy()` |

## Core Patterns

### Execute Commands

```typescript
const sandbox = getSandbox(env.Sandbox, 'user-123');
const result = await sandbox.exec('python --version');
// result: { stdout, stderr, exitCode, success }
```

### Code Interpreter (Recommended for AI)

Use `runCode()` for executing LLM-generated code with rich outputs:

```typescript
const ctx = await sandbox.createCodeContext({ language: 'python' });

await sandbox.runCode('import pandas as pd; data = [1,2,3]', { context: ctx });
const result = await sandbox.runCode('sum(data)', { context: ctx });
// result.results[0].text = "6"
```

**Languages**: `python`, `javascript`, `typescript`

State persists within context. Create explicit contexts for production.

### File Operations

```typescript
await sandbox.mkdir('/workspace/project', { recursive: true });
await sandbox.writeFile('/workspace/project/main.py', code);
const file = await sandbox.readFile('/workspace/project/main.py');
const files = await sandbox.listFiles('/workspace/project');
```

## Suggested Process
1. Verify prerequisites by running `docker info` to ensure daemon availability.
2. Initialize container layouts and configure wrangler.jsonc containers binding block.
3. Establish custom workspace directories and write required scripts in the container volume.
4. Call `runCode` or `exec` to run isolated computations inside the sandbox.
5. Invoke `destroy` on the active sandbox instance to free server resources.

## Checklist
- [ ] Sandbox SDK package is installed and Docker is operational.
- [ ] Wrangler config declares the containers block and matching DO migration.
- [ ] Worker code includes the explicit export statement for Sandbox class.
- [ ] Code interpreter context is correctly initialized.
- [ ] Sandbox instances are cleaned up or destroyed after operations.

## Related Skills
- **wrangler**: Deploy containers bindings and monitor edge variables.
- **debug-workers-edge**: Diagnose runtime execution issues on Cloudflare.
