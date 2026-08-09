---
name: setup-gpu-finops
description: Configure GPU telemetry, DCGM metrics, and Kubecost to attribute AI compute costs to specific namespaces or teams.
---

# Setup GPU FinOps

Use this skill to implement cost transparency for self-hosted AI models and GPU workloads in Kubernetes clusters.

## Core Rules
- **DCGM Integration**: Deploy the NVIDIA DCGM Exporter to expose low-level GPU metrics (utilization, memory, power) to Prometheus.
- **Namespace Attribution**: Use Kubecost (or OpenCost) custom pricing sheets to map GPU node costs down to the pod and namespace level.
- **Idle Optimization**: Implement KEDA (Kubernetes Event-driven Autoscaling) or Karpenter to scale GPU nodes to zero when inference queues are empty.
- **Alerting**: Configure Slack/PagerDuty alerts for teams exceeding their daily GPU compute budget.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/deployment-plan.json`** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run` output proving Prometheus is scraping DCGM metrics successfully.

## Checklist
- [ ] DCGM Exporter deployed to GPU nodes.
- [ ] Prometheus relabeling rules configured for namespace mapping.
- [ ] Kubecost pricing sheet updated for GPU instances.
- [ ] Scale-to-zero autoscaling (KEDA/Karpenter) verified.
- [ ] `deployment-plan.json` emitted.
