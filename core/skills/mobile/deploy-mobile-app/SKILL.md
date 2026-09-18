---
name: deploy-mobile-app
description: Configure and execute mobile deployment pipelines using EAS Build, native code signing credentials, OTA updates via EAS Update, App Store and Google Play compliance, AI content disclosures, and crash symbolication. Use when configuring EAS build profiles, publishing OTA updates, preparing store releases, or validating Apple 4.3(b) and Google Play AI compliance.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Deploy Mobile App

Use this skill to orchestrate mobile builds, code signing credentials, over-the-air (OTA) updates, store review compliance, and release symbolication across iOS and Android ecosystems.

## When to Use

- configuring `eas.json` multi-environment build profiles (`development`, `preview`, `production`)
- provisioning and rotating iOS Distribution Certificates, Provisioning Profiles, and Android Keystores
- publishing over-the-air updates with EAS Update and enforcing runtime version safety boundaries
- auditing App Store compliance under Apple Guideline 4.3(b) (anti-wrapper) and Guideline 1.2 (AI UGC)
- compiling Apple `PrivacyInfo.xcprivacy` manifests and Google Play Data Safety SDK disclosures
- configuring Hermes bytecode sourcemap and native dSYM symbolication for crash reporting

## Core Rules

- **Enforce EAS Multi-Environment Isolation**: configure `eas.json` with strict profile separation (`development`, `preview`, `production`); isolate bundle identifiers, provisioning profiles, and environment variables
- **Enforce OTA Update Safety Boundaries**: EAS Update releases must enforce strict runtime version policies (`runtimeVersion: { policy: "fingerprint" }` or `"appVersion"`); never deploy native binary changes, new native modules, or permission alterations over OTA
- **Mandate Emergency OTA Rollback Channels**: maintain dedicated rollback branches or rollback channels in EAS Update to instantly revert faulty JS bundles without app store review delays
- **Zero-Trust Credential Management**: store iOS Distribution Certificates, Push Keys, and Android Keystores exclusively in EAS Credentials or encrypted key vaults; never commit `.p12`, `.keystore`, `.jks`, or passwords to git
- **Apple App Store AI Compliance**:
  - *Guideline 4.3(b) (Anti-Wrapper)*: verify the app demonstrates differentiated native functionality (device hardware, offline persistence, rich interactive UI) beyond basic LLM prompt wrappers
  - *Guideline 1.2 (AI UGC Moderation)*: AI-generated user content must feature real-time content filtering, user reporting mechanisms, and offensive content blocking
  - *AI Content Labeling & Privacy*: label all AI-generated outputs; declare all AI SDKs in `PrivacyInfo.xcprivacy` with required reason APIs
- **Google Play AI & Data Safety Compliance**:
  - *AI Disclosure Mandate*: declare generative AI features in the Google Play Console declaration form and display prominent in-app notices
  - *Data Safety Inventory*: document every third-party SDK's data collection, transmission, and encryption practices
- **Crash Symbolication & Debug Symbols**: upload Hermes sourcemaps, native iOS dSYMs, and Android ProGuard/R8 mapping files to Sentry or Bugsnag during release builds
- detailed build profiles and compliance checklists: [`references/eas-build-ota-and-store-compliance-specs.md`](references/eas-build-ota-and-store-compliance-specs.md)

## Suggested Process

### 1. Configure EAS Build Environment
Define `eas.json` with distinct `development`, `preview`, and `production` profiles. Configure native package names (`com.company.app.dev`, `com.company.app`) and inject environment variables via EAS Secrets.

### 2. Configure Code Signing Credentials
Run `eas credentials` to securely generate or import Apple Distribution Certificates and Android Release Keystores. Verify Apple Developer Team credentials and Google Play Service Account keys.

### 3. Establish EAS Update & Runtime Versioning
Set `runtimeVersion: { policy: "fingerprint" }` in `app.json`. Bind update channels (`production`, `preview`) to deployment branches. Verify emergency rollback mechanisms.

### 4. Audit Third-Party SDKs & Author Privacy Manifests
Inventory all installed native SDKs. Author iOS `PrivacyInfo.xcprivacy` declaring NSPrivacyAccessedAPITypes (UserDefaults, File timestamps) and tracking domains. Populate Google Play Data Safety form.

### 5. Validate Store AI Review Guidelines
Verify in-app AI disclosure banners, test the user-reporting and content-flagging workflow for AI responses (Apple 1.2), and document differentiated native capabilities (Apple 4.3(b)).

### 6. Build, Symbolicate & Submit
Trigger release build via `eas build --platform all --profile production`. Ensure Hermes sourcemaps and dSYMs are uploaded to monitoring tools. Submit to TestFlight / Play Console track.

## Checklist

- [ ] `eas.json` defines isolated `development`, `preview`, and `production` build profiles
- [ ] code signing certificates and keystores securely managed in EAS Credentials; zero secrets in repo
- [ ] `runtimeVersion` policy configured with `fingerprint` or `appVersion` preventing broken OTA updates
- [ ] emergency OTA rollback channel and rollback procedure documented and verified
- [ ] iOS `PrivacyInfo.xcprivacy` contains all required reason API declarations and tracking disclosures
- [ ] Apple Guideline 4.3(b) audit passed: app delivers differentiated native features beyond wrapper
- [ ] Apple Guideline 1.2 / Google Play AI compliance passed: in-app AI disclosure and user reporting active
- [ ] Google Play Data Safety section audited against third-party SDK network behaviors
- [ ] Hermes sourcemaps and native dSYM symbols uploaded to crash reporting platforms
- [ ] `contracts/schemas/edge-deployment-spec.json` and `contracts/schemas/implementation-result.json` emitted

## Output Contracts

When completing release or build engineering tasks, emit:

- **`contracts/schemas/edge-deployment-spec.json`** — Specifies target platforms, build profiles, runtime versions, signing status, and rollback boundaries.
- **`contracts/schemas/implementation-result.json`** — Documents configuration files modified (`eas.json`, `app.json`, `PrivacyInfo.xcprivacy`) and validation results.

## Failure Modes

- **Runtime Version Mismatch Crash**: an OTA update targeting native version N is applied to binary version N-1, causing immediate native module crash. Mitigation: mandate `runtimeVersion: { policy: "fingerprint" }` so updates only execute on matching native binaries.
- **Apple Guideline 4.3(b) Rejection**: reviewer rejects app as a thin web or LLM wrapper. Mitigation: document offline capabilities, native device sensors, widgets, and differentiated value in app review notes.
- **Missing Privacy Manifest Rejection**: build rejected on App Store Connect due to missing `PrivacyInfo.xcprivacy` required reason APIs. Mitigation: audit all CocoaPods and NPM packages with automated privacy manifest checkers.
- **Hermes Obfuscated Crash Stacks**: production crash reports show illegible bytecode offsets (`address at 0x...`). Mitigation: automate Hermes sourcemap upload in the EAS post-build hook.

## Related Skills

- **develop-mobile-app**: Implement native mobile logic, performance tuning, and offline persistence
- **setup-deployment**: Configure general CI/CD pipeline automation and deployment scripts
- **manage-secrets**: Secure deployment API keys, EAS tokens, and signing passphrase secrets
- **security-audit**: Audit third-party SDK vulnerabilities, permissions, and network payloads
- **release-notes**: Compile store release notes, changelogs, and version upgrade documentation
