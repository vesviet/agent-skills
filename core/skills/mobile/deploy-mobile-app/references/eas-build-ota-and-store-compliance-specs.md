# EAS Build, OTA Governance & App Store Compliance Specifications

## 1. EAS Build Multi-Profile Configuration

### 1.1 `eas.json` Profile Hierarchy
Expo Application Services (EAS) Build provides managed and bare workflow compilation across cloud and self-hosted runners. Build configurations must enforce strict multi-environment isolation:

```json
{
  "cli": {
    "version": ">= 12.0.0",
    "appVersionSource": "remote"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      },
      "env": {
        "APP_ENV": "development",
        "API_URL": "https://dev-api.example.com"
      },
      "channel": "development"
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "enterpriseProvisioning": "adhoc"
      },
      "android": {
        "buildType": "apk"
      },
      "env": {
        "APP_ENV": "staging",
        "API_URL": "https://staging-api.example.com"
      },
      "channel": "preview"
    },
    "production": {
      "distribution": "store",
      "ios": {
        "provisioningProfile": "app-store"
      },
      "android": {
        "buildType": "app-bundle"
      },
      "env": {
        "APP_ENV": "production",
        "API_URL": "https://api.example.com"
      },
      "channel": "production",
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "apple-dev@example.com",
        "ascAppId": "1234567890",
        "appleTeamId": "TEAM123456"
      },
      "android": {
        "serviceAccountKeyPath": "./keys/play-store-key.json",
        "track": "internal"
      }
    }
  }
}
```

### 1.2 Environment Isolation & Native Package Naming
- Separate development, staging, and production installations on the same physical device:
  - Development: `com.example.app.dev` / App Name: "App (Dev)"
  - Preview/Staging: `com.example.app.staging` / App Name: "App (Staging)"
  - Production: `com.example.app` / App Name: "App"
- Inject environment variables securely using EAS Secrets (`eas secret:create`) rather than hardcoding credentials into source control.

---

## 2. Native Code Signing & Credential Management

### 2.1 iOS Code Signing Architecture
- **Distribution Certificate**: Required to sign iOS binaries for TestFlight and App Store distribution. Managed securely via EAS Credentials or Apple Developer API keys.
- **Provisioning Profiles**:
  - Development: Bound to development certificates and registered device UDIDs.
  - Ad-Hoc / Internal: Used for preview builds distributed via internal testing links.
  - App Store: Bound to the distribution certificate for TestFlight and public release.
- **Push Notification Certificates & APNs Keys**: Auth Key (`.p8`) configured with Push Notifications service enabled.

### 2.2 Android Code Signing Architecture
- **Upload Keystore**: Generated locally or by EAS Credentials. Signs the Android App Bundle (`.aab`) before transmission to Google Play.
- **Google Play App Signing (PEP)**: Google Play manages the final app signing key used to deliver APKs to end-user devices. The developer upload key signs the bundle sent to Google Play.
- **Zero-Trust Rule**: Never commit `.keystore`, `.jks`, `.p12`, or provisioning profiles to git. Enforce `.gitignore` checks for credential extensions.

---

## 3. EAS Update Architecture & OTA Safety Boundaries

### 3.1 Runtime Versioning Policies
Over-The-Air (OTA) updates push JavaScript bundles and asset deltas without going through app store review. To prevent crashes, EAS Update must strictly isolate updates by runtime version:
- **Fingerprint Policy (Mandatory Default)**:
  `"runtimeVersion": { "policy": "fingerprint" }`
  EAS generates a cryptographic hash of all native files, dependencies, Expo config plugins, and native source code. If any native code changes, the fingerprint changes, preventing incompatible JS bundles from downloading to incompatible native binaries.
- **Binary Barrier Invariant**:
  The following changes CANNOT be delivered via OTA and mandate a full store binary release:
  1. Adding, updating, or removing native modules (`npm install` packages with native iOS/Android code).
  2. Modifying native permissions in `Info.plist` or `AndroidManifest.xml`.
  3. Altering app configuration plugins or build scripts.
  4. Updating the React Native, Hermes, or Expo SDK core version.

### 3.2 Deployment Channels & Emergency Rollbacks
- Updates are published to branches linked to release channels:
  `eas update --branch production --message "Fix checkout tax calculation"`
- **Emergency Rollback Mechanics**:
  If an OTA release causes runtime regressions:
  1. Re-publish the prior known-good update:
     `eas update:re-publish --group <PRIOR_HEALTHY_GROUP_ID> --branch production`
  2. Alternatively, rollback to the embedded native binary bundle:
     `eas update:rollback --branch production`

---

## 4. App Store & Google Play Review Compliance

### 4.1 Apple Guideline 4.3(b) (Minimum Functionality & Anti-Wrapper)
Apple rejects apps that serve as thin wrappers around websites or basic LLM prompt endpoints. To guarantee approval:
- **Demonstrate Differentiated Native Value**:
  - Offline-first data caching and local persistence.
  - Hardware integration: Camera, Biometrics (FaceID/TouchID), Accelerometer, Haptics.
  - Platform integration: iOS Home Screen Widgets, Live Activities, App Intents / Siri Shortcuts, Spotlight Indexing.
  - Interactive, fluid canvas / gesture interactions that cannot be replicated in a standard mobile web browser.
- **App Review Notes**: Include explicit video demonstrations and technical explanations in App Store Connect review notes showing offline features and native capabilities.

### 4.2 Apple Guideline 1.2 (User-Generated Content & AI Moderation)
If an application generates content using AI (chat, images, summaries, voice), it is classified under User-Generated Content rules:
1. **Terms of Service (EULA)**: Users must accept terms prohibiting abusive, obscene, or harmful content.
2. **Real-Time AI Output Filtering**: Input prompts and model responses must pass through moderation filters (e.g. Llama Guard, OpenAI Moderation API, or on-device safety heuristics).
3. **In-App User Reporting**: Every AI response must provide a visible "Flag / Report" button allowing users to report inappropriate generation.
4. **Blocking Mechanism**: Users must have the ability to block content or mute conversational agents.
5. **24-Hour Review SLA**: The publisher must maintain a process to inspect reported content and update guardrails within 24 hours.

### 4.3 Google Play AI Disclosures & Policy Compliance
- **Generative AI Declaration**: Complete the GenAI declaration in Google Play Console indicating whether the app generates synthetic text, image, or audio content.
- **In-App Disclosure Notice**: Prominently display a notice informing users that content is AI-generated and may contain inaccuracies.
- **Zero-Tolerance for AI Spam**: Never use AI to mass-generate store descriptions, screenshots, or automated reviews.

### 4.4 Apple Privacy Manifest (`PrivacyInfo.xcprivacy`)
Apple requires an explicit privacy manifest declaring all accessed APIs and data tracking practices:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <dict>
            <key>NSPrivacyCollectedDataType</key>
            <string>NSPrivacyCollectedDataTypeCrashData</string>
            <key>NSPrivacyCollectedDataTypeLinked</key>
            <false/>
            <key>NSPrivacyCollectedDataTypeTracking</key>
            <false/>
            <key>NSPrivacyCollectedDataTypePurposes</key>
            <array>
                <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
            </array>
        </dict>
    </array>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>C617.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

### 4.5 Google Play Data Safety & Third-Party SDK Audit
- Audit every bundled SDK (Sentry, Firebase, analytics, ad networks).
- Document whether data is:
  - Collected vs. shared.
  - Encrypted in transit (HTTPS/TLS 1.3).
  - Subject to user account deletion requests.
- Verify that no third-party SDK accesses Advertising ID (AAID) without proper declaration.

---

## 5. Production Symbolication & Crash Telemetry

### 5.1 Hermes Bytecode Sourcemaps
When Hermes compiles JS to bytecode, runtime crash stack traces reference bytecode instructions rather than source line numbers. To de-obfuscate:
- Enable sourcemap generation in EAS build hooks:
  `eas build --platform all --profile production`
- Upload `index.android.bundle.map` and `index.ios.bundle.map` to Sentry or Bugsnag via CLI plugins.

### 5.2 Native Debug Symbols (dSYM & ProGuard/R8)
- **iOS dSYMs**: Download dSYM archive from App Store Connect or EAS Build artifacts and upload to crash reporting services:
  `sentry-cli upload-dif --org my-org --project my-app path/to/dSYMs`
- **Android ProGuard/R8 Mappings**: Ensure `mapping.txt` from `android/app/build/outputs/mapping/release/` is uploaded during EAS post-build step.
