# Interactive Human-In-The-Loop (HITL) Setup Wizard Reference

When operational onboarding, OAuth provisioning, KMS rotation, or DNS/database cutover requires sequential human actions mixed with automated verification, generate an idempotent, stage-checkpointed Bash wizard rather than fragile copy-paste checklists.

---

## 1. Core Architectural Invariants

1. **Strict Shell Safety (`set -euo pipefail`):** Fail fast on unset variables or broken pipes. Never use unquoted variable expansion or dangerous pipelines.
2. **Stage Checkpoint Persistence:** Store completed stage IDs in a local state file (e.g. `.wizard-state` ignored by Git) so humans can safely abort (`Ctrl-C` / `SIGINT`) and resume at the exact interrupted step without repeating earlier steps.
3. **Zero Plaintext Secret Leakage:**
   - Capture tokens, passwords, and API keys via silent terminal prompts (`read -rsp`).
   - Never print secrets to `stdout`/`stderr`, command history, or LLM agent logs.
   - Persist captured secrets directly into gitignored `.env` files (`chmod 600`) or secret managers (`gh secret set`, AWS Secrets Manager, HashiCorp Vault).
4. **Trap & Clean Interrupted Output:** Register a `trap cleanup EXIT INT TERM` handler that prints exact resume status without dumping environment variables.

---

## 2. Canonical Skeleton Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

STATE_FILE="${STATE_FILE:-.hitl-wizard.state}"
touch "$STATE_FILE"

cleanup() {
  local rc=$?
  stty echo 2>/dev/null || true
  if [[ $rc -ne 0 ]]; then
    echo "[wizard] Interrupted (exit $rc). Progress saved in $STATE_FILE — re-run to resume." >&2
  fi
}
trap cleanup EXIT INT TERM

stage_done() { grep -qxF "$1" "$STATE_FILE" 2>/dev/null; }
mark_done() { echo "$1" >> "$STATE_FILE"; }

run_stage() {
  local id="$1" title="$2" fn="$3"
  if stage_done "$id"; then
    echo "[skip] $id: $title (already completed)"
    return 0
  fi
  echo "=== Stage $id: $title ==="
  "$fn"
  mark_done "$id"
}
```

---

## 3. Verification Before Proceeding
Each stage MUST end with a deterministic health check (`curl -sf`, CLI `whoami`, dry-run validation, or container health probe) before calling `mark_done`. Never mark a human step complete without checking its external post-condition.
