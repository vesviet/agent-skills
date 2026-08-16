---
name: setup-gpu-finops
description: Configure GPU telemetry, DCGM metrics, and Kubecost to attribute AI compute costs to specific namespaces or teams. Use when managing GPU infrastructure budgets, tracking AI workload unit economics, or optimizing accelerator capacity.
---

# Setup GPU FinOps

Use this skill to implement cost transparency for self-hosted AI models and GPU workloads in Kubernetes clusters.

## Core Rules

- **DCGM Integration**: Deploy the NVIDIA DCGM Exporter to expose low-level GPU metrics (utilization, memory, power) to Prometheus.
- **Namespace Attribution**: Use Kubecost (or OpenCost) custom pricing sheets to map GPU node costs down to the pod and namespace level.
- **Idle Optimization**: Implement KEDA (Kubernetes Event-driven Autoscaling) or Karpenter to scale GPU nodes to zero when inference queues are empty.
- **Alerting**: Configure Slack/PagerDuty alerts for teams exceeding their daily GPU compute budget.
- **Metric Standardization**: Normalize GPU metric names with `hw.gpu.*` prefixes via OpenTelemetry Collector processors.

## Suggested Process

### 1. Deploy NVIDIA DCGM Exporter DaemonSet

Install hardware telemetry infrastructure:
- Deploy the NVIDIA DCGM (Data Center GPU Manager) Exporter as a DaemonSet across GPU-enabled Kubernetes nodes.
- Configure profiling metrics: GPU utilization (`DCGM_FI_DEV_GPU_UTIL`), framebuffer memory used (`DCGM_FI_DEV_FB_USED`), and power draw (`DCGM_FI_DEV_POWER_USAGE`).
- Verify the exporter exposes Prometheus metrics on port 9400.

### 2. Configure Prometheus Metric Scraping & Relabeling

Wire metrics into the monitoring cluster:
- Add a Prometheus `PodMonitor` or `ServiceMonitor` targeting DCGM exporter endpoints.
- Configure metric relabeling rules to attach Kubernetes pod, namespace, model name, and node group labels.
- Set up an OpenTelemetry Collector pipeline to transform and export metrics with standardized `hw.gpu.*` naming conventions.

### 3. Integrate Kubecost / OpenCost Pricing Sheets

Configure cost allocation models:
- Define custom GPU pricing tables in Kubecost/OpenCost reflecting cloud provider or on-premise hourly rates per accelerator type (A100, H100, L4, T4).
- Configure allocation algorithms to split node base cost by fractional GPU sharing (MIG or time-slicing) when multiple pods share an accelerator.
- Validate that cost breakdown dashboards attribute dollar spend accurately by namespace, team, and model deployment.

### 4. Implement Scale-to-Zero & Dynamic Autoscaling

Optimize GPU compute efficiency:
- Configure Karpenter node pools or Cluster Autoscaler to dynamically provision GPU instances on demand.
- Deploy KEDA ScaledObjects driven by inference request queue depth (vLLM / Triton metrics) to scale model replicas down to zero during idle periods.
- Configure node termination grace periods to allow in-flight inference requests to drain cleanly.

### 5. Establish Budget Thresholds & Anomaly Alerting

Protect against cost overruns:
- Define PrometheusRule alert thresholds for low utilization on allocated GPUs (e.g., utilization < 15% for > 30 minutes).
- Configure budget alert notifications via Slack or PagerDuty when daily/monthly cost burn rates exceed target limits.
- Set up automated scaling circuit breakers for runaway experimental batch jobs.

### 6. Validate Pipeline & Dashboards

Use skill: `performance-profiling`
- Generate synthetic inference load to verify Prometheus records utilization spikes in real time.
- Verify Kubecost allocation reports reflect cost per inference request.
- Confirm idle scale-down shuts down unneeded GPU nodes within the configured TTL.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/deployment-plan.json`** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run` output proving Prometheus is scraping DCGM metrics successfully.

## Checklist

- [ ] NVIDIA DCGM Exporter DaemonSet deployed and exposing metrics on GPU nodes.
- [ ] Prometheus scraping and relabeling rules configured with pod and namespace metadata.
- [ ] Kubecost / OpenCost custom GPU pricing sheets configured and verified.
- [ ] Scale-to-zero autoscaling (KEDA/Karpenter) configured for inference queues.
- [ ] Low-utilization and budget-overrun alerting rules active.
- [ ] Grafana and cost attribution dashboards verified under active load.
- [ ] `deployment-plan.json` emitted.

## Related Skills

- **setup-llm-gateway**: Correlate GPU infrastructure spend with model token usage and routing policies
- **add-telemetry-instrumentation**: Standardize GPU metric collection using OTel Collector and DCGM conventions
- **aws-infrastructure**: Provision GPU EC2 instances, EKS node groups, and FinOps cost allocation tags
- **system-design**: Model GPU capacity requirements and inference compute topology
- **setup-deployment**: Apply Kubernetes manifests, DaemonSets, and KEDA autoscalers to deployment sources
- **performance-profiling**: Analyze GPU memory bandwidth, compute utilization, and kernel execution latency
