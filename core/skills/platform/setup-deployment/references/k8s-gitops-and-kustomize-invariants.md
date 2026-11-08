# Kubernetes GitOps & Kustomize Production Invariants (2026)

## 1. Kustomize Multi-Tier Architecture

### 1.1 Four-Tier Folder Hierarchy
Production Kubernetes deployments avoid copy-paste drift by enforcing a strict four-tier hierarchy:
```
deploy/
├── base/                   # Canonical workload definition (Deployment, Service, ServiceAccount)
├── components/             # Optional composable traits (ingress, hpa, network-policy, tracing)
└── overlays/
    ├── dev/                # Single replica, debug logging, local ingress
    ├── staging/            # Multi-replica, external secrets, synthetic monitoring
    └── production/         # Multi-AZ HPA, PodDisruptionBudget, strict NetworkPolicy
```

---

## 2. Workload Resilience & Probe Specifications

### 2.1 Three-Probe Architecture for Microservices
- **`startupProbe`**: Handles slow initialization (e.g. JVM warm-up or Go database migration runs). Prevents aggressive liveness probes from prematurely killing pods during boot:
  ```yaml
  startupProbe:
    httpGet:
      path: /health/live
      port: 8080
    failureThreshold: 30
    periodSeconds: 2
  ```
- **`livenessProbe`**: Checks process deadlock and internal thread health (`periodSeconds: 10`, `timeoutSeconds: 3`).
- **`readinessProbe`**: Evaluates downstream connectivity (database pool availability, cache connectivity). Pod is removed from Service endpoints during degraded windows without restarting the container.

---

## 3. High-Availability Release Gates

- **Immutable Tag Invariant**: `:latest` tags are strictly blocked in production manifests. Every image reference must pin an immutable Git commit SHA or SemVer release tag (`ghcr.io/org/svc:v2.4.0@sha256:...`).
- **PodDisruptionBudget (PDB)**: Every replicated service must configure a PDB (`minAvailable: 1` or `maxUnavailable: 25%`) to guarantee availability during voluntary node drain operations and cluster upgrades.
- **Resource Limits & Requests**: CPU and Memory requests must equal limits for burst-sensitive workloads, or specify explicit requests to enable Kubernetes fair-share scheduling.
