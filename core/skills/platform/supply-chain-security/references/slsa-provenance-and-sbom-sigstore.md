# SLSA Level 3 Provenance, CycloneDX v1.6 SBOM, and Sigstore Signing (2026)

## 1. SLSA Level 3+ Build Provenance

### 1.1 Hermetic Isolated Build Environments
Production workloads must satisfy SLSA v1.2 Build Level 3 invariants:
- **Build Isolation**: Builds execute within dedicated ephemeral runners preventing cross-build cache pollution or unauthorized network tampering.
- **Source Verification**: All build steps pin dependencies and actions to immutable 40-character Git commit SHAs rather than mutable tag references.
- **Signed in-toto Attestations**: Build systems emit tamper-evident in-toto provenance statements (`provenance.intoto.jsonl`) cryptographically linking the output container digest to the source commit.

---

## 2. CycloneDX v1.6 SBOM & AI Model Attestations

### 2.1 Software and AI/ML Bill of Materials
- **Comprehensive Dependency Inventory**: Every component (direct, transitive, build tools) must record its Package URL (pURL), cryptographic hash (SHA-256), and validated license.
- **AI/ML BOM Requirements (EU AI Act Article 13)**:
  CycloneDX v1.6 includes dedicated schema definitions for machine learning assets:
  - Model weights SHA-256 digests.
  - Training dataset lineage and preprocessing pipeline hashes.
  - Quantization precision metadata (e.g. FP8, INT4 AWQ).

---

## 3. Keyless Artifact Signing via Sigstore & Cosign

### 3.1 Ephemeral OIDC Workload Identity
Cosign keyless signing binds signatures to the CI/CD pipeline's OpenID Connect (OIDC) identity without requiring long-lived private keys:
- **Fulcio CA**: Issues short-lived X.509 signing certificates (valid for 10 minutes) bound to GitHub Actions / GitLab CI OIDC identity tokens.
- **Rekor Transparency Log**: Publishes immutable cryptographic proofs of signature creation to a public transparency ledger.
- **Verification Gate**:
  ```bash
  cosign verify \
    --certificate-identity "https://github.com/my-org/my-repo/.github/workflows/release.yaml@refs/heads/main" \
    --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
    ghcr.io/my-org/my-service:v2.0.0
  ```

---

## 4. OpenVEX Vulnerability Context

Every release publishes OpenVEX context alongside the SBOM, preventing false alarms on dead or unreachable transitive code paths:
```json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://corp.example/vex/release-2.0.0",
  "author": "SecOps Automation",
  "timestamp": "2026-11-08T09:00:00Z",
  "statements": [
    {
      "vulnerability": {"name": "CVE-2024-45338"},
      "products": [{"@id": "pkg:golang/golang.org/x/net@0.33.0"}],
      "status": "not_affected",
      "justification": "code_not_reachable",
      "impact_statement": "The vulnerable HTTP/2 rapid reset handler is not invoked in this gRPC-only daemon."
    }
  ]
}
```
