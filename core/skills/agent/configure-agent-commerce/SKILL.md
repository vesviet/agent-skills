---
name: configure-agent-commerce
description: Use when implementing agentic commerce standards like x402, MPP, UCP, and ACP for transactional checkout flows.
---

# Configure Agent Commerce

Use this skill when integrating agent-driven checkout and commerce discovery flows.

## Core Rules
- Adhere strictly to the x402 and Merchant Payment Protocol (MPP) metadata requirements.
- Expose the User Context Protocol (UCP) endpoint appropriately.
- Maintain up-to-date `.well-known` endpoints for Agentic Commerce Protocol (ACP).

## Suggested Process
1. Define the checkout actions and paywall scopes for agent integration.
2. Structure the payment and pricing metadata according to the x402 specification.
3. Expose the Merchant Payment Protocol endpoint to handle token payments.
4. Mount the User Context Protocol endpoints to resolve consumer preferences.

## Checklist
- [ ] x402 endpoints are operational and tested.
- [ ] Payment parameters match Merchant Payment Protocol specs.
- [ ] User Context endpoints correctly resolve consumer preferences.
- [ ] API responses use correct media types for agent consumption.
- [ ] Client validation checks are secure and performant.

## Related Skills
- **configure-oauth-metadata**: Configure agentic authorization metadata blocks.
- **manage-api-catalog**: Wire up linkset endpoints for discovery.
