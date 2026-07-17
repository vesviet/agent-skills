# Donthan Web Overlay

Project-specific conventions for **Donthan.com** — a web-first live-streaming platform with desktop-priority UX.

**Status:** Active (standalone — no stack overlay dependency)

## Scope

This overlay applies when working on the Donthan.com front-end. It overrides or extends `core/` defaults for:

- Layout architecture (web-first, no mobile-first bottom-nav patterns)
- UX conventions for desktop livestream interfaces
- Component and navigation patterns optimised for wide-viewport streaming layouts

## Rules

| Rule file | Applies to |
|---|---|
| [donthan-web-ux-conventions.md](rules/donthan-web-ux-conventions.md) | UI/UX Designer, Frontend Developer |

## Activation

Load this overlay when the active repository is `donthan-web` or when the user explicitly references Donthan.com UX work. No pack currently wraps this overlay — activate manually or create `packs/donthan-team/manifest.yaml` when a team pack is needed.
