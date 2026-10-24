# deploy-mobile-app — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Expo SDK Evolution (2026)
- **SDK 52+**: New Architecture enabled by default for all new projects (November 2024)
- **SDK 53**: New Architecture enabled by default; opt-out possible
- **SDK 55+**: New Architecture **always enabled**, cannot be disabled (React Native 0.82+)
- **SDK 56** (May 2026): React Native 0.85 + React 19.2, Hermes bytecode diffing default, Expo UI production-ready
- **SDK 57** (June 2026): React Native 0.86, Hermes V1 regressions resolved in 57.0.9/57.0.17
- **Expo Go**: Only supports New Architecture (JSC removed, Hermes mandatory)
- **Expo Router**: Replaces React Navigation; file-based routing with new features

### EAS Build & Update Evolution (2026)
- **EAS Update channels/branches/runtime versions**: Mature deployment patterns with channel mapping to Git branches
- **Runtime version policy**: `runtimeVersion: { policy: "appVersion" }` recommended (matches native app version)
- **Emergency rollback channels**: Dedicated rollback branches in EAS Update for instant JS bundle revert
- **Auto-submit**: `eas build --auto-submit` manages native code signing automatically
- **EAS CLI 14+**: Required for latest features

### Apple App Store Compliance (2026)
- **Guideline 4.3(b) Anti-Wrapper**: Must demonstrate differentiated native functionality beyond LLM prompt wrappers (device hardware, offline persistence, rich interactive UI)
- **Guideline 1.2 AI UGC Moderation**: Real-time content filtering, user reporting, offensive content blocking for AI-generated content
- **AI Content Labeling**: All AI-generated outputs must be labeled; AI SDKs declared in `PrivacyInfo.xcprivacy` with required reason APIs
- **PrivacyInfo.xcprivacy**: Mandatory required reason API declarations (UserDefaults, File timestamps) and tracking domains
- **iPad rendering**: Test on iPad simulator even if `ios.supportsTablet: false`

### Google Play Compliance (2026)
- **Target API 36 (Android 16)** mandatory from August 31, 2026 for new apps/updates
- **AI Disclosure Mandate**: Declare generative AI features in Play Console; display prominent in-app notices
- **Data Safety**: Document every third-party SDK's data collection, transmission, encryption practices
- **Sensitive categories**: AI-generated content, financial features require feature-specific review
- **Release gate**: Data safety reconciled to declarations; store listing matches functionality; reviewer access working

### Crash Reporting & Symbolication (2026)
- **Hermes sourcemaps**: Automated upload in EAS post-build hook
- **Native dSYMs**: iOS debug symbols uploaded to Sentry/Bugsnag
- **Android ProGuard/R8 mappings**: Uploaded for crash symbolication
- **Hermes bytecode diffing**: Enabled by default in SDK 56+

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| New Architecture optional | **New Architecture mandatory**: SDK 55+ always enabled, cannot be disabled; SDK 52+ default for new projects |
| EAS Update basic patterns | **Mature EAS Update patterns**: channels/branches/runtime versions, emergency rollback channels, auto-submit |
| Apple 4.3(b) basic | **Apple 4.3(b) + 1.2 AI compliance**: Differentiated native features + AI UGC moderation + labeling |
| Google Play basic | **Google Play Target API 36 + AI Disclosure + Data Safety**: API 36 mandatory, AI features declared |
| Crash symbolication basic | **Hermes bytecode diffing + automated sourcemap/dSYM/ProGuard upload** |

### 2. New 2026 Patterns to Add
- **Expo SDK Version Matrix**: SDK 52/53/54/55/56/57 feature progression and migration requirements
- **EAS Update Advanced Patterns**: Channel-branch mapping, runtime version policies, rollback channels, channel distribution (`internal` vs `store`)
- **Apple AI Compliance Checklist**: 4.3(b) native differentiation evidence, 1.2 UGC moderation flow, AI labeling, PrivacyInfo.xcprivacy completeness
- **Google Play 2026 Compliance**: Target API 36 deadline, AI disclosure form, Data Safety SDK inventory, sensitive category review gates
- **Hermes V1 Management**: Bytecode diffing, memory regression workarounds (57.0.9), startup time fixes (57.0.17)
- **Expo Router Migration**: File-based routing replacing React Navigation; brownfield integration
- **EAS CLI 14+ Requirements**: Version pinning, auto-submit, credential management

### 3. Checklist Additions
- [ ] Expo SDK version confirmed (55+ = New Architecture mandatory, cannot disable)
- [ ] `eas.json` defines isolated `development`, `preview`, `production` profiles with correct distribution (`internal`/`store`)
- [ ] `runtimeVersion: { policy: "appVersion" }` configured; runtime version matches native app version
- [ ] Emergency OTA rollback channel documented and verified (dedicated branch in EAS Update)
- [ ] Code signing credentials managed in EAS Credentials; zero secrets in repo
- [ ] iOS `PrivacyInfo.xcprivacy` complete: all required reason API declarations + tracking domains
- [ ] Apple Guideline 4.3(b) audit: documented offline capabilities, native sensors, widgets, differentiated value
- [ ] Apple Guideline 1.2 / Google Play AI compliance: in-app AI disclosure + user reporting + content filtering active
- [ ] Google Play Target API 36 (Android 16) configured for new apps/updates (deadline Aug 31, 2026)
- [ ] Google Play Data Safety section reconciled against third-party SDK network behaviors
- [ ] Google Play AI disclosure form submitted; prominent in-app notices displayed
- [ ] Hermes sourcemaps + native dSYMs + Android ProGuard/R8 mappings uploaded to Sentry/Bugsnag
- [ ] Hermes bytecode diffing enabled (SDK 56+); memory regression mitigated (expo@57.0.9+)
- [ ] Expo Router file-based routing implemented; React Navigation replaced
- [ ] EAS CLI version pinned (>= 14.0.0)
- [ ] iPad rendering tested even if `ios.supportsTablet: false`
- [ ] `contracts/schemas/edge-deployment-spec.json` and `implementation-result.json` emitted

### 4. Failure Mode Additions
- **SDK 55+ New Architecture lock-in**: Cannot revert to legacy architecture. Mitigation: Test migration on SDK 53/54 first; audit all dependencies for New Architecture support via Expo Doctor.
- **Hermes V1 memory regression**: Drastic memory increase with `react-native-worklets`/`reanimated`. Mitigation: Update to `expo@57.0.9+` (React Native 0.86.2).
- **Hermes V1 dev startup regression**: Increased startup time in development. Mitigation: Update to `expo@57.0.17+` (React Native 0.86.3).
- **OTA update feature creep**: Pushing new features via EAS Update violates Apple 2.5.2. Mitigation: Strict channel policy — only bug fixes, improvements, content updates via OTA.
- **AI wrapper rejection**: App rejected as thin LLM wrapper. Mitigation: Document native sensors, offline persistence, widgets, rich UI in review notes.
- **Target API 36 missed**: App becomes undiscoverable to new users. Mitigation: Plan build/dependency/permission work before Aug 31, 2026 deadline.
- **Google Play AI disclosure missing**: Rejection for undeclared generative AI. Mitigation: Submit AI disclosure form; display in-app notices.
- **PrivacyInfo.xcprivacy incomplete**: Build rejected on App Store Connect. Mitigation: Automated privacy manifest checkers for all CocoaPods/NPM packages.

### 5. Output Contract Updates
- Update `contracts/schemas/edge-deployment-spec.json` with Expo SDK version, New Architecture status, Hermes version, EAS CLI version
- Update `contracts/schemas/implementation-result.json` with Apple/Google AI compliance evidence, OTA rollback verification

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Expo SDK 55+ New Architecture mandatory enforcement | High |
| P0 | Apple 4.3(b) + 1.2 AI compliance checklist | High |
| P0 | Google Play Target API 36 + AI Disclosure + Data Safety | High |
| P0 | EAS Update advanced patterns (channels, rollback, auto-submit) | High |
| P1 | Hermes V1 management (bytecode diffing, memory/startup fixes) | Medium |
| P1 | Expo Router migration from React Navigation | Medium |
| P1 | EAS CLI 14+ pinning and credential management | Medium |
| P2 | iPad rendering test requirement | Low |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test EAS Update rollback channel with simulated faulty bundle
- Validate Apple 4.3(b) evidence package with sample app
- Validate Google Play Data Safety reconciliation against SDK inventory
- Test Hermes sourcemap upload in EAS post-build hook