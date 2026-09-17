# Cellular Topology, Shuffle Sharding & Mathematical Capacity Sizing Reference

This reference provides canonical mathematical formulas, routing algorithms, and worked examples for designing Cell-Based Architectures (CBA), Shuffle Sharding routers, and exact capacity/GPU sizing models in enterprise platforms.

---

## 1. Cell-Based Failure Domain Isolation (FDI)

### 1.1 The Cellular Architecture Principle
Platforms requiring $\ge 99.95\%$ availability must be partitioned into shared-nothing, independent operating units called **Cells**.
- **Shared-Nothing Invariant**: Each cell hosts its own compute, caching, and dedicated database shards. No synchronous RPC or database transactions may cross cellular boundaries.
- **Blast Radius Containment**: A critical failure, memory leak, or poison pill request in Cell $i$ impacts at most $1/N$ of the total platform capacity (where $N$ is the number of cells).

### 1.2 Shuffle Sharding Combinatorics
To protect multi-tenant platforms against noisy neighbors and malicious tenants, tenants are assigned to a subset of $K$ cells out of $N$ total cells (called a **Shard**).
The total number of unique shards is:
$$S = \binom{N}{K} = \frac{N!}{K!(N - K)!}$$

#### Tenant Collision Probability
If Tenant A experiences a catastrophic failure or DDoS attack that degrades all $K$ cells in their shard, the probability that any other Tenant B shares the exact same $K$ cells and also experiences a full outage is:
$$P(\text{Full Overlap}) = \frac{1}{\binom{N}{K}}$$

**Example**: With $N = 16$ cells and $K = 4$ cells per tenant:
$$\binom{16}{4} = \frac{16 \times 15 \times 14 \times 13}{4 \times 3 \times 2 \times 1} = 1,820 \text{ unique shards}$$
$$P(\text{Full Overlap}) = \frac{1}{1,820} \approx 0.055\%$$

If $N = 24$ and $K = 4$:
$$\binom{24}{4} = 10,626 \implies P(\text{Full Overlap}) \approx 0.0094\%$$

### 1.3 Highest Random Weight (HRW) Rendezvous Hashing Router
To map a tenant deterministically to their $K$ cells without maintaining centralized lookup tables, Envoy Gateway or edge routers use HRW rendezvous hashing:

```go
package router

import (
	"crypto/sha256"
	"encoding/binary"
	"sort"
)

type CellScore struct {
	CellID string
	Score  uint64
}

func GetTenantCells(tenantID string, cells []string, k int) []string {
	scores := make([]CellScore, len(cells))
	for i, cell := range cells {
		h := sha256.New()
		h.Write([]byte(tenantID + ":" + cell))
		digest := h.Sum(nil)
		scores[i] = CellScore{
			CellID: cell,
			Score:  binary.BigEndian.Uint64(digest[:8]),
		}
	}
	sort.Slice(scores, func(i, j int) bool {
		return scores[i].Score > scores[j].Score
	})
	selected := make([]string, k)
	for i := 0; i < k; i++ {
		selected[i] = scores[i].CellID
	}
	return selected
}
```

### 1.4 Monotonic Epoch Fencing Tokens
To eliminate split-brain dual-master state mutations during cell router network partitions:
1. Every cell assignment update carries an incrementing 64-bit monotonic epoch fencing token ($E$).
2. Database instances and stateful storage nodes reject any write carrying an epoch $E_{req} < E_{active}$.
3. When leadership transitions, the new leader increments the epoch in etcd via a transactional Compare-And-Swap (CAS) operation before accepting traffic.

---

## 2. Mathematical Capacity Sizing

### 2.1 Little's Law for Concurrency & Connection Pools
The average number of concurrent requests in a system ($L$) equals the arrival rate ($\lambda$, requests/sec) multiplied by the average response time ($W$, seconds):
$$L = \lambda \times W$$

#### Goroutine & Worker Dimensioning
- Target peak arrival rate: $\lambda = 5,000 \text{ req/sec}$
- Average service latency: $W = 40\text{ms} = 0.04\text{sec}$
- Required concurrent worker capacity:
  $$L = 5,000 \times 0.04 = 200 \text{ active goroutines}$$
- With a safety headroom multiplier of $2.5\times$ for traffic bursts:
  $$\text{Worker Pool Cap} = 200 \times 2.5 = 500$$

#### Database Connection Pool Sizing (PgBouncer)
PostgreSQL query latency: $W_{db} = 8\text{ms} = 0.008\text{sec}$. Queries per HTTP request: $Q = 2$.
$$\lambda_{db} = 5,000 \times 2 = 10,000 \text{ queries/sec}$$
$$L_{db} = 10,000 \times 0.008 = 80 \text{ active DB connections}$$
Using transaction pooling mode in PgBouncer, a pool of 100 physical connections supports 5,000 peak HTTP RPS.

---

## 3. GPU VRAM Memory Allocation & AI Workload Sizing

### 3.1 The Canonical 4-Component GPU VRAM Equation
$$VRAM_{total} = VRAM_{weights} + VRAM_{KV} + VRAM_{activation} + VRAM_{overhead}$$

Where:
1. **Model Weights ($VRAM_{weights}$)**:
   $$VRAM_{weights} = P \times BPE$$
   - $P$: Parameter count (e.g., 70 Billion for Llama 3.1 70B).
   - $BPE$: Bytes per element (FP16/BF16 = 2 bytes, FP8 = 1 byte, INT4 AWQ/GPTQ = 0.5 bytes).
   - *Example*: 70B in BF16 $\implies 70 \times 10^9 \times 2 / 1024^3 \approx 130.38\text{ GB}$.

2. **Paged KV-Cache ($VRAM_{KV}$)**:
   For Grouped-Query Attention (GQA) with $n_{layers}$, $n_{kv\_heads}$, $d_{head}$, context length $L_{ctx} = L_{prompt} + L_{gen}$, and batch concurrency $B$:
   $$VRAM_{KV} = 2 \times n_{layers} \times n_{kv\_heads} \times d_{head} \times L_{ctx} \times B \times BPE_{KV}$$
   With PagedAttention fragmentation overhead $\mu_{frag} \approx 3\%$:
   $$VRAM_{KV\_paged} = VRAM_{KV} \times (1 + \mu_{frag})$$

3. **Activation Memory ($VRAM_{activation}$)**:
   With FlashAttention-2 or FlashAttention-3 and Chunked Prefill (chunk size $C_{prefill} = 2,048$):
   $$VRAM_{activation} \approx 2 \times C_{prefill} \times d_{model} \times n_{layers} \times BPE$$
   Typically sizes between $2\text{ GB}$ and $6\text{ GB}$ across tensor-parallel ranks.

4. **Runtime Overhead ($VRAM_{overhead}$)**:
   CUDA runtime context, NCCL communication buffers, and PyTorch workspace memory:
   $$VRAM_{overhead} \approx 0.15 \times VRAM_{GPU\_capacity}$$
   A mandatory minimum $15\%$ safety headroom must be reserved to prevent OOM termination under unexpected prompt length bursts.

### 3.2 Latency Dynamics: TTFT and TBT

#### Time To First Token (TTFT)
Governed by Model FLOPs Utilization ($MFU$) during prompt processing:
$$TTFT = \frac{2 \times P \times L_{prompt}}{N_{GPU} \times \text{Peak TFLOPS} \times MFU} + \text{Scheduling Latency}$$
Target: $TTFT_{P95} \le 800\text{ms}$.

#### Time Between Tokens (TBT)
Governed by Memory Bandwidth Utilization ($MBU$) during token generation:
$$TBT = \frac{VRAM_{weights} / N_{GPU}}{\text{HBM Bandwidth} \times MBU} + \text{All-Reduce Comm Overhead}$$
Target: $TBT_{P95} \le 25\text{ms}$ ($> 40\text{ tokens/sec}$ per user stream).

---

## 4. Token Economics & Value-Per-Token (VPT)

### 4.1 Cost-Per-Token (CPT)
$$CPT = \frac{\text{Hourly GPU Cluster Cost}}{\text{Sustained Output Tokens / Hour}}$$
For an 8x H100 SXM5 instance at \$24.00/hour producing 1,000,000 output tokens/hour:
$$CPT = \frac{\$24.00}{1,000,000} = \$0.000024 \text{ per token} = \$0.024 \text{ per 1K tokens}$$

### 4.2 Value-Per-Token (VPT) Business Threshold
$$VPT = \frac{\text{Direct Business Revenue Generated}}{\text{Total Tokens Consumed}}$$
A business solution is economically viable only when:
$$\text{ROI}_{token} = \frac{VPT - CPT}{CPT} \ge 3.0 \implies VPT \ge 4 \times CPT$$
