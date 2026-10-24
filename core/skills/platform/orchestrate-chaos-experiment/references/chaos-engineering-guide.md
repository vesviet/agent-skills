# Chaos Engineering & Resilience Verification Guide

This guide establishes the 2026–2027 SOTA technical specifications for orchestrating chaos experiments, authoring declarative fault injection manifests, establishing steady-state hypotheses, enforcing blast-radius guardrails, and managing production Game Day drills.

---

## 1. Steady-State Hypothesis Engineering

A chaos experiment verifies that a distributed system maintains normal service quality when subjected to turbulent conditions. Experiments must never be initiated without a pre-computed steady-state baseline.

### 1.1 Mathematical Formulation of Steady State
Steady state is defined across three primary service dimensions:
1. **Request Availability & Error Rate ($E_{\text{rate}}$)**:
   $$\text{Availability} = \frac{\sum \text{Successful Requests}}{\sum \text{Total Requests}} \ge 99.9\% \implies E_{\text{rate}} \le 0.1\%$$
2. **Latency Distribution ($L_{P99}$)**:
   $$P99(\text{latency}) \le 200\text{ ms} \quad (\text{API Gateways}), \quad P95(\text{latency}) \le 50\text{ ms} \quad (\text{Internal RPC})$$
3. **Throughput Invariance**:
   $$RPS_{\text{actual}} \ge 0.95 \times RPS_{\text{baseline}}$$

### 1.2 Pre-Flight Telemetry Sampling
Capture a 15-minute sliding baseline of the Four Golden Signals (Latency, Traffic, Errors, Saturation) plus kernel-level eBPF socket drop rates prior to injecting any perturbation.

---

## 2. Declarative Fault Injection Manifests

All experiments must be declared as version-controlled Kubernetes Custom Resources. Ad-hoc shell scripting on live nodes is strictly prohibited.

### 2.1 Chaos Mesh CRD Manifests

#### Pod Failure (`PodChaos`)
Simulates sudden ungraceful container crash or pod eviction:
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: canary-pod-failure
  namespace: production
  labels:
    tier: reliability-verification
spec:
  action: pod-failure
  mode: fixed
  value: "1"
  duration: "3m"
  selector:
    namespaces:
      - production
    labelSelectors:
      app: checkout-service
      canary: "true"
```

#### Network Latency & Jitter (`NetworkChaos`)
Injects 150ms delay with 20ms jitter to verify circuit breakers and timeouts:
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: order-db-network-latency
  namespace: production
spec:
  action: delay
  mode: fixed-percent
  value: "10%"
  duration: "4m"
  delay:
    latency: "150ms"
    jitter: "20ms"
    correlation: "50"
  selector:
    namespaces:
      - production
    labelSelectors:
      app: order-processor
  direction: to
  target:
    selector:
      namespaces:
        - production
      labelSelectors:
        app: postgres-primary
```

#### Resource Saturation (`StressChaos`)
Injects CPU burn (80% load) across targeted worker nodes:
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: cpu-worker-stress
  namespace: staging
spec:
  mode: one
  duration: "5m"
  stressors:
    cpu:
      workers: 2
      load: 80
  selector:
    namespaces:
      - staging
    labelSelectors:
      app: search-indexer
```

#### I/O Delay & Error (`IOChaos`)
Simulates slow disk storage and read/write timeouts:
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: IOChaos
metadata:
  name: disk-io-delay
  namespace: staging
spec:
  action: latency
  mode: all
  duration: "3m"
  delay: "100ms"
  path: "/data/*"
  percent: 50
  selector:
    namespaces:
      - staging
    labelSelectors:
      app: cache-datastore
```

### 2.2 LitmusChaos Workflow Manifest (`ChaosEngine`)

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: engine-pod-delete
  namespace: production
spec:
  appinfo:
    appns: "production"
    applabel: "app=payment-gateway,canary=true"
    appkind: "deployment"
  engineState: "active"
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "180"
            - name: CHAOS_INTERVAL
              value: "30"
            - name: FORCE
              value: "false"
```

---

## 3. Blast Radius Guardrails & Isolation Topology

### 3.1 Strict Percentage Capping
The number of simultaneously targeted replicas $N_{\text{fault}}$ must never exceed 10% of the active serving pool:
$$N_{\text{fault}} \le \max\left(1, \left\lfloor 0.10 \times N_{\text{replicas}} \right\rfloor\right)$$

### 3.2 Namespace and Canary Isolation
- Faults must target exclusively pods marked with label `canary=true` or running in dedicated chaos namespaces.
- Never inject unpartitioned stateful disk faults into primary database instances without hot streaming replication and zero-RPO failover confirmed.

---

## 4. Automated Rollback Criteria & Emergency Abort Circuits

### 4.1 Automated Abort Rules (Prometheus Alertmanager Webhook)
When an active chaos experiment is detected, Prometheus alert rules automatically invoke the chaos abort webhook if any of the following boundaries are breached:
1. **MWMBR 14.4x Burn Rate Alert (1h window)**:
   ```promql
   (
     sum(rate(http_requests_total{status=~"5.."}[1h]))
     /
     sum(rate(http_requests_total[1h]))
   ) > (14.4 * (1 - 0.999))
   ```
2. **User-Facing Error Rate Spike**:
   ```promql
   sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m])) > 0.01
   ```

### 4.2 Emergency Kill Switch Script (`chaos-kill-switch.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail
echo ">>> EMERGENCY CHAOS ABORT INITIATED <<<"
# Delete all active Chaos Mesh resources
kubectl delete podchaos,networkchaos,stresschaos,iochaos,dnschaos --all --all-namespaces --timeout=30s || true
# Stop active Litmus engines
kubectl patch chaosengine --all -n production --type merge -p '{"spec":{"engineState":"stop"}}' || true
echo ">>> ALL CHAOS EXPERIMENTS HALTED <<<"
```

---

## 5. Game Day Drill Operational Protocol & RACI Matrix

### 5.1 RACI Matrix
| Role | Accountable / Responsible / Consulted / Informed |
| :--- | :--- |
| **Drill Lead (SRE)** | **Accountable**: Charter, hypothesis validation, final go/no-go |
| **Chaos Operator (SRE)** | **Responsible**: Applies manifests, monitors kill switch |
| **Observer (QA / DevOps)** | **Responsible**: Captures metrics, verifies logs, notes timeline |
| **Incident Commander** | **Responsible**: Directs on-call engineers, calls abort if necessary |
| **Product Stakeholders** | **Informed**: Schedule, customer impact window |

### 5.2 4-Phase Drill Timeline
1. **Briefing (T - 30m)**: Review charter, verify rollback scripts, confirm on-call staffing.
2. **Baseline (T - 10m)**: Sample steady-state SLIs, check error budgets.
3. **Execution (T = 0 to T + 15m)**: Apply fault manifest, observe alert propagation and auto-healing.
4. **Teardown & Debrief (T + 15m to T + 45m)**: Revert fault, verify full recovery, record actual MTTD/MTTM.

---

## 6. Game Day Drill Report & Action Item Template

```markdown
# Chaos Drill Outcome Report: [DRILL-ID]

- **Date / Time**: 2026-10-05T10:00:00Z
- **Target Service**: checkout-service
- **Fault Type**: NetworkChaos (150ms delay to postgres-primary)
- **Steady-State Hypothesis**: P99 latency <= 250ms, error rate <= 0.05%
- **Actual Outcome**: PASSED (Circuit breaker tripped at 3.2s, fallback cache served 99.96% requests)
- **Empirical Metrics**:
  - MTTD (Detection): 28 seconds
  - MTTM (Mitigation): 42 seconds
  - Peak Burn Rate: 0.8x (No error budget exhausted)
- **Remediation Action Items**:
  - ACT-01: Increase connection pool timeout buffer in checkout-worker (Owner: Backend Developer, Priority: P2)
```
