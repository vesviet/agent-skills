---
name: setup-tracking-system
description: Configure advanced privacy-first tracking including Server-to-Server (S2S) postbacks, Meta Conversion API (CAPI), and tracker setups (Voluum/Binom) without relying solely on client-side cookies. Use when launching a new campaign, migrating from pixel-only to server-side tracking, or diagnosing attribution gaps.
---

# Setup Tracking System

Use this skill to deploy highly accurate, privacy-first tracking systems necessary for MMO operations in a cookieless landscape.

## When to Use

- launching a new campaign and wiring conversion postbacks
- migrating from pixel-only to Server-to-Server (S2S) tracking
- integrating Meta Conversion API (CAPI) for higher match quality
- diagnosing attribution gaps or low postback fire rates
- configuring cloaking / bot-traffic filtering rules in a tracker

## Example (S2S postback with click ID + payout)

```
# Voluum/Binom postback URL fired by the affiliate network on conversion
https://tracker.example.com/postback?cid={clickid}&payout={payout}&txid={txid}

# Meta CAPI server-side event (Node)
await fetch(`https://graph.facebook.com/v19.0/${PIXEL_ID}/events?access_token=${CAPI_TOKEN}`, {
  method: "POST",
  body: JSON.stringify({
    data: [{ event_name: "Purchase", event_time: Math.floor(Date.now()/1000),
             user_data: { em: [hash(email)] }, custom_data: { value: payout, currency: "USD" } }]
  })
});
```

## Core Rules

- **TRACKING-LOCK**: Never rely solely on client-side JavaScript pixels. Always implement and verify a Server-to-Server (S2S) fallback. Pixel-only tracking suffers > 35% signal loss from Safari ITP, Brave, uBlock Origin, and iOS restrictions.
- **DATA-VALIDATION**: Always run a test conversion to verify that the S2S postback fires with the correct click ID (e.g., `cid`, `subid`) and payout value before launching a campaign.
- **META-CAPI-EMQ**: Target Event Match Quality (EMQ) ≥ 8.0/10 for lower-funnel events. Send server-side `fbp` (browser cookie), `fbc` (click ID from `fbclid`), `em` (SHA-256 lowercase email), `ph` (E.164 SHA-256 phone), `client_ip_address`, and `client_user_agent`. Capture `fbclid` from landing page URL and persist in an HTTP-only first-party cookie for 90 days.
- **PII-NORMALIZATION**: Before SHA-256 hashing, all strings MUST be lowercased, stripped of leading/trailing whitespace, and phone numbers must use E.164 format (`+14155552671`) — no dashes, spaces, or parentheses.
- **EVENT-DEDUPLICATION**: Share the same UUID v4 `event_id` between the client-side pixel event and the CAPI server-side event. The 48-hour deduplication window requires exact matching — never use separate IDs per channel.
- **CTIT-FRAUD-FILTER**: Reject S2S postbacks where Click-To-Conversion-Time < 2.5 seconds (programmatic injection). Flag conversions > 7 days on performance offers as potential organic hijacking.
- **IDEMPOTENT-POSTBACK-QUEUE**: S2S postback receivers MUST use durable, idempotent queues (SQS/Kafka/RabbitMQ) with unique constraint on `(transaction_id, event_type)` to prevent double attribution from network retries.
- **IOS18-AAK**: For iOS app campaigns, migrate from SKAdNetwork (SKAN 4.0) to Apple AdAttributionKit (AAK); support re-engagement attribution and 4-tier crowd anonymity coarse/fine conversion values.

## Suggested Process

1. **Server-to-Server (S2S) Configuration**: Set up postback URLs in your tracker (e.g., Voluum, Binom) to transmit conversion data directly between servers (Affiliate Network → Tracker → Ad Network).
2. **Click ID Capture at Edge**: On landing, capture `fbclid`, `gclid`, `ttclid`, and affiliate click IDs at the edge/gateway and write to first-party HTTP-only cookies (`_fbc`, `_gcl_aw`) on the apex domain.
3. **Meta CAPI / Datasets Integration**: Implement CAPI v20+ with normalized, SHA-256 hashed PII. Verify EMQ ≥ 8.0 in Events Manager. Set `event_id` to match pixel `event_id` exactly.
4. **CTIT Fraud Filtering**: Add conversion time validation layer; reject sub-2.5s postbacks and flag anomalous tail distributions.
5. **Traffic Filtering Rules**: Configure tracker rules to filter bot traffic or cloak destination URLs from ad network reviewers based on IP, ASN, or behavioral patterns.
6. **End-to-End Testing**: Trigger a manual conversion and verify data flow across all hops including CAPI deduplication in Events Manager.

## Checklist

- [ ] S2S postback URLs configured and verified with correct click ID parameters.
- [ ] Meta CAPI v20+ integrated with `fbp`, `fbc`, `em`, `ph`, `client_ip_address`, and `event_id`.
- [ ] EMQ score verified ≥ 8.0/10 in Events Manager for key conversion events.
- [ ] PII SHA-256 hashed after lowercasing and normalization (E.164 phones).
- [ ] `event_id` matches exactly between pixel and CAPI for deduplication.
- [ ] Landing page edge captures `fbclid`/`gclid` to first-party HTTP-only cookies.
- [ ] CTIT fraud filter active: sub-2.5s conversions rejected.
- [ ] Idempotent postback queue with unique `(transaction_id, event_type)` constraint active.
- [ ] Traffic filtering rules (cloaking/bot blocking) are active.
- [ ] Test conversion successfully registered in both tracker and ad network.
- [ ] Postback firing rate above 80% (flag if below for attribution investigation).
- [ ] iOS 18+ AdAttributionKit migration plan documented for app campaigns.

## Output Contracts

When the tracking system is consumed by a campaign operator, a data
analyst, or a cross-role handoff, emit:

- **`contracts/schemas/deployment-plan.json`** capturing the S2S endpoints, the postback handlers, the event dedup keys, the consent capture, and the rollback path.
- For human-readable reports, a markdown summary of the tracking topology, the data classification, and the compliance boundaries.

Skip emission for local tracking experiments that do not cross a role boundary.

## Failure Modes

- **Event dedup missing**: a pixel event and a CAPI/S2S postback use different `event_id` values, inflating conversion counts. Mitigation: enforce the same UUID v4 `event_id` across pixel and S2S; reject mismatched IDs.
- **First-party cookie not set**: `_fbc` and `_gcl_aw` are missing on landing, breaking attribution. Mitigation: capture `fbclid`, `gclid`, `ttclid` at the edge; persist 90-day first-party cookies.
- **CTIT fraud filter bypass**: sub-2.5s conversions are included in the conversion count. Mitigation: filter CTIT < 2.5s as SIVT; surface the excluded count.
- **Consent capture skipped**: a user event is tracked without a recorded consent. Mitigation: capture consent before any tracking event; reject unconsented events.
- **Compliance boundary crossed**: a tracking pattern violates the documented Legal & Compliance Notice. Mitigation: keep the compliance boundary visible; reject any pattern outside the boundary.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: customer identifiers and PII used for matching must be hashed before transmission; never store unhashed PII in tracking systems.
- **ASI04 Supply Chain**: tracking SDKs and S2S postback libraries must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct S2S postback payloads, pixel events, or consent prompts from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the deployment plan is consumed by data and marketing roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the tracking system as "compliant" without naming the Legal & Compliance boundary; surface the residual risk honestly.

## Related Skills

- **analyze-campaign-roi**: Analyze the data collected by this tracking system for ROI optimization.
- **integrate-api-client**: Write frontend integration code if client-side component is required.
