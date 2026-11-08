# Worked Example: Adversarial Two-Axis Code Review Walkthrough

This worked example demonstrates an Adversarial Two-Axis Pull Request Review of an AI-generated pull request, contrasting Standards (code smells, concurrency, security, resource leaks) against Specification (contract conformance, edge cases), and emitting the standard `contracts/schemas/code-review-finding.json` payload.

---

## 1. Incoming Pull Request Diff (`PR #418: Add User Profile Sync`)

```diff
--- a/package.json
+++ b/package.json
@@ -24,7 +24,8 @@
     "express": "^4.21.0",
-    "zod": "^3.23.0"
+    "zod": "^3.23.0",
+    "telemetry-collect": "^0.1.2"
   }
 }

--- a/src/services/user-sync.ts
+++ b/src/services/user-sync.ts
@@ -10,18 +10,38 @@
 export class UserSyncService {
   constructor(private db: Database, private client: HttpClient) {}

+  async syncUserProfile(userId: string, payload: any): Promise<any> {
+    // Validate email format
+    if (payload.email) {
+      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email);
+    }
+
+    // Fetch current user from external CRM
+    const response = await this.client.get(`https://crm.internal/api/v1/users/${userId}`);
+    // Note: Stream not closed
+    const crmData = await response.json();
+
+    // Update local database
+    try {
+      const updated = await this.db.users.update({
+        where: { id: userId },
+        data: {
+          email: payload.email || crmData.email,
+          name: payload.name || crmData.name
+        }
+      });
+      return updated;
+    } catch (err) {
+      // Silent error swallowing
+      return null;
+    }
+  }
```

---

## 2. Axis 1 — Standards Sub-Agent Report

```markdown
### Standards Review Findings

1. **[Fowler Smell: Dead Code / Phantom Validation]** (`src/services/user-sync.ts:15`)
   - **Finding**: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email);` evaluates the regular expression, but the boolean result is completely discarded. Invalid emails silently pass through to the database.
   - **Remediation**: Check the return value or replace with schema-first validation: `if (!EMAIL_REGEX.test(payload.email)) throw new ValidationError("Invalid email format");`.

2. **[Resource Leak: Unclosed HTTP Stream]** (`src/services/user-sync.ts:19`)
   - **Finding**: `this.client.get` opens an HTTP connection. If `response.json()` throws a JSON parse exception, the underlying socket handle is not destroyed, leading to connection pool exhaustion under load.
   - **Remediation**: Wrap in `try ... finally` and invoke `response.body.destroy()` or use an auto-disposing HTTP client.

3. **[AI Anti-Pattern: Silent Error Swallowing]** (`src/services/user-sync.ts:33`)
   - **Finding**: Indiscriminate `catch (err) { return null; }` suppresses database unique constraint violations, connection timeouts, and disk failures, returning `null` as if the update succeeded.
   - **Remediation**: Catch specific business errors, rethrow unexpected exceptions, and propagate an RFC 9457 structured problem details envelope.

4. **[Supply Chain Hazard: Unpinned & Unverified Dependency]** (`package.json:28`)
   - **Finding**: Introduces `telemetry-collect: ^0.1.2`. Package has no repository stars, was published 48 hours ago, and uses loose carat (`^`) pinning.
   - **Remediation**: Remove dependency immediately. Re-evaluate utility against vetted organizational libraries.
```

---

## 3. Axis 2 — Specification Sub-Agent Report

```markdown
### Specification Review Findings

1. **[Missing Acceptance Criteria: Atomic Idempotency]**
   - **Finding**: Specification Requirement AC-2 mandates that concurrent sync requests for the same `userId` must not cause race conditions or overwriting with stale CRM data. The PR lacks distributed locking or version precondition checks (`If-Match` / `ETag`).

2. **[Contract Violation: Return Types]**
   - **Finding**: Feature contract `api-contract-spec.json` defines return type as `UserProfile` with mandatory `updatedAt` and `syncStatus` fields. Returning `null` on failure violates the non-nullable API schema contract.
```

---

## 4. Aggregated Side-by-Side Review Report

| Axis | Domain | File & Line | Severity | Description | Actionable Suggestion |
|---|---|---|---|---|---|
| **Standards** | Correctness | `user-sync.ts:15` | `blocking` | Phantom regex validation result is discarded. | Enforce check or validate with Zod boundary schema. |
| **Standards** | Reliability | `user-sync.ts:19` | `important` | HTTP response body stream is not protected by finally cleanup. | Add scoped resource disposal. |
| **Standards** | Maintainability | `user-sync.ts:33` | `blocking` | Error swallowed returning null without logging or metrics. | Bubble up typed domain error with trace_id. |
| **Standards** | Security | `package.json:28` | `blocking` | Unvetted dependency `telemetry-collect` introduced. | Remove package and audit supply chain provenance. |
| **Spec** | Conformance | `user-sync.ts:13` | `blocking` | Lacks concurrency locks and violates return contract. | Add atomic optimistic concurrency check. |

---

## 5. Emitted Structured Contract Payload (`contracts/schemas/code-review-finding.json`)

```json
{
  "contract_type": "code-review-finding",
  "review_id": "2026-11-08-pr-418-user-profile-sync",
  "created_at": "2026-11-08T11:00:00Z",
  "change_ref": "PR #418 — Add User Profile Sync",
  "change_type": "feature",
  "findings": [
    {
      "finding_id": "F-01",
      "file": "src/services/user-sync.ts",
      "line": 15,
      "severity": "blocking",
      "domain": "correctness",
      "description": "Phantom regex validation: return value of RegExp.test() is discarded.",
      "suggestion": "Validate with Zod schema or early-return 400 error if regex fails.",
      "confidence": "confirmed"
    },
    {
      "finding_id": "F-02",
      "file": "package.json",
      "line": 28,
      "severity": "blocking",
      "domain": "security",
      "description": "Unvetted third-party package 'telemetry-collect' added with loose carat pin.",
      "suggestion": "Remove dependency and require Security Lead approval for new packages.",
      "confidence": "confirmed"
    },
    {
      "finding_id": "F-03",
      "file": "src/services/user-sync.ts",
      "line": 33,
      "severity": "blocking",
      "domain": "reliability",
      "description": "Silent error swallowing masks database write failures and returns null.",
      "suggestion": "Remove empty catch; map to RFC 9457 structured error with trace_id.",
      "confidence": "confirmed"
    }
  ],
  "review_matrix": {
    "correctness": "fail",
    "security": "fail",
    "data_safety": "fail",
    "reliability": "fail",
    "compatibility": "pass",
    "maintainability": "fail",
    "tests": "fail",
    "observability": "fail"
  },
  "blast_radius_assessment": {
    "shared_code_paths_checked": true,
    "downstream_consumers_checked": true,
    "adjacent_flows_checked": true,
    "notes": "User sync affects CRM synchronization and billing notifications downstream."
  },
  "merge_recommendation": "request_changes",
  "residual_risk": "High data corruption risk due to unvalidated input and silent database error suppression.",
  "ai_code_intent_check": true
}
```
