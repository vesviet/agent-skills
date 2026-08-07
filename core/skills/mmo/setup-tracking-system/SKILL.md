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

- **TRACKING-LOCK**: Never rely solely on client-side JavaScript pixels. Always implement and verify a Server-to-Server (S2S) fallback.
- **DATA-VALIDATION**: Always run a test conversion to verify that the S2S postback fires with the correct click ID (e.g., `cid`, `subid`) and payout value before launching a campaign.

## Suggested Process

1. **Server-to-Server (S2S) Configuration**: Set up postback URLs in your tracker (e.g., Voluum, Binom) to transmit conversion data directly between servers (Affiliate Network -> Tracker -> Ad Network).
2. **Meta CAPI / Datasets Integration**: Implement the Conversion API to ensure platforms like Facebook receive high-quality event match rates, bypassing browser ad blockers and iOS tracking restrictions.
3. **Traffic Filtering Rules**: Configure tracker rules to filter bot traffic or cloak the destination URL from ad network reviewers based on IP, ASN, or behavioral patterns.
4. **End-to-End Testing**: Trigger a manual conversion and verify data flow across all hops.

## Checklist

- [ ] S2S postback URLs are configured and verified with correct click ID parameters.
- [ ] Meta CAPI (or equivalent API) is integrated and receiving payloads.
- [ ] Traffic filtering rules (cloaking/bot blocking) are active.
- [ ] Test conversion successfully registered in both tracker and ad network.
- [ ] Data flow validated end-to-end across all hops before scaling budget.
- [ ] Postback firing rate is above 80% (flag if below for attribution investigation).

## Related Skills

- **analyze-campaign-roi**: Analyze the data collected by this tracking system for ROI optimization.
- **integrate-api-client**: Write frontend integration code if client-side component is required.
