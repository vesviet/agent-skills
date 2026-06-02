# Core Pack

This directory is the portable source of truth for the global engineering pack.

Everything in `core/` should satisfy these rules:

- no repo-specific absolute paths
- no brand-specific content assumptions
- no site-specific publish logic
- reusable across multiple repositories with local adaptation only

## Structure

- [rules](rules/README.md)
- [roles](roles/README.md)
- [skills](skills/README.md)
- [workflows](workflows/README.md)
- [contracts](contracts/README.md)
- [policies](policies/README.md)
- [a2a](a2a/README.md)
- [prompts](prompts/README.md)
- [scripts](scripts/README.md)
- [config](config/README.md)
- [adapter-parity](adapter-parity.md)

Use `core/` when you want the generic engineering foundation without any org-local overlay.
