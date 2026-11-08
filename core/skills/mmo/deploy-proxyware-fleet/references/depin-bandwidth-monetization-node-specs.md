# DePIN Bandwidth Monetization & Light Node Specifications (2026)

## 1. DePIN Protocol Landscape

Decentralized Physical Infrastructure Networks (DePIN) for bandwidth monetization (Grass / Wynd Network, Dawn, Nodepay, Gradient) replace legacy centralized proxy networks by rewarding residential node operators with verifiable cryptographic tokens:

```
┌────────────────────────────────────────────────────────┐
│                   DePIN ARCHITECTURE                   │
├────────────────────────────────────────────────────────┤
│ Solana / EVM Wallet (Ed25519 / Secp256k1)              │
│   - Delegated session-scoped auth signature (Off-chain)│
├────────────────────────────────────────────────────────┤
│ Light Node Client Container                            │
│   - Read-only rootfs (`readOnlyRootFilesystem: true`)   │
│   - Ephemeral tmpfs (`/tmp`, `/dev/shm` 512MB)         │
│   - Strict cgroups (CPU <= 0.25, Memory <= 256MB)      │
├────────────────────────────────────────────────────────┤
│ Residential Network Gateway                            │
│   - SOCKS5 / WireGuard Remote DNS Resolution           │
│   - Verified Residential ISP (Zero Datacenter ASNs)    │
├────────────────────────────────────────────────────────┤
│ DePIN Protocol Telemetry (WebSocket wss://)            │
│   - Continuous ping/pong heartbeat (Uptime > 98%)      │
│   - Epoch reward scoring and point multipliers         │
└────────────────────────────────────────────────────────┘
```

## 2. Cryptographic Wallet Authentication

- **Zero Private Keys in Containers**: Private keys are kept in secure offline KMS or cold wallets.
- **Session Signature Protocol**:
  ```
  Message = "DePIN-Auth:" + challenge_nonce + ":" + timestamp_epoch
  Signature = Ed25519_Sign(Private_Key, Message)
  ```
- Containers receive only the public address, challenge nonce, and session signature.

## 3. Container Hardening & Resource Isolation

- `read_only: true` with `tmpfs` mounts to prevent unconstrained logging and disk space exhaustion.
- Enforce strict resource limits per node: `cpus: "0.25"`, `memory: 256M`.
- Prometheus/Grafana exporter scraping connection state, ping latency, and epoch score multipliers.
