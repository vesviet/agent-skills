# Keep a Changelog & SemVer 2.0.0 Governance (2026)

## 1. Standards Overview

High-velocity engineering teams adhere to **Keep a Changelog 1.1.0** and **Semantic Versioning 2.0.0** specifications, combining automated commit parsing with human editorial curation.

```
       Conventional Commits 1.0
  (feat, fix, feat!, BREAKING CHANGE)
                   │
                   ▼
  Automated Extraction (changesets / changelogen)
                   │
                   ▼
  Editorial Human Review (De-noise & Polish)
                   │
                   ▼
  Keep a Changelog 1.1.0 Multi-Audience Release
```

## 2. Semantic Versioning Specification (SemVer 2.0.0)

Given a version number `MAJOR.MINOR.PATCH`:
- **MAJOR (`x.0.0`)**: Incompatible API breaking changes, schema drops, removed features, deprecated protocol sunsetting.
- **MINOR (`0.x.0`)**: Backwards-compatible new features, new non-mandatory fields, new endpoints, performance enhancements.
- **PATCH (`0.0.x`)**: Backwards-compatible defect and security fixes.

## 3. Keep a Changelog Section Standards

A compliant release changelog partitions changes into distinct, standardized categories:
1. **Added**: for new user-facing features or capabilities.
2. **Changed**: for changes in existing functionality.
3. **Deprecated**: for soon-to-be removed features, with mandatory ISO 8601 sunset date.
4. **Removed**: for now removed features.
5. **Fixed**: for any bug fixes.
6. **Security**: in case of vulnerabilities (referencing CVE ID and upgrade instructions without exploit details).

## 4. Multi-Audience Release Structure

Every production release communication must strictly isolate:
- **User-Facing Product Notes**: Focus on business value, UI/UX changes, and workflow improvements.
- **API & Integrator Notes**: Focus on contract updates, deprecation warnings, and SDK upgrades.
- **Operator & Infrastructure Notes**: Focus on database migrations, environment variable changes, resource sizing, and rollback runbooks.
