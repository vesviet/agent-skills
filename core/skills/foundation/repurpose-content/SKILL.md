---
name: repurpose-content
description: Extract and format micro-content variants (social threads, newsletters, short video scripts) from a core long-form article or asset. Use when creating derivative content for omnichannel distribution.
---

# Repurpose Content

**Context:** Modern content distribution requires a single narrative to be adapted into multiple native formats. This skill ensures that when an agent writes a core piece of content (like a blog post or whitepaper), it extracts high-value micro-content variants for omnichannel distribution without losing the core message or tone.

## Core Rules

- **Native Format Alignment:** A LinkedIn post is not just a shortened article; it requires a hook, spaced lines, and a professional-insight tone. A Twitter thread requires numbered segments, tight constraints, and an engaging opener.
- **Do Not Hallucinate Constraints:** If repurposing an article into a script, explicitly denote visual cues (e.g., `[B-Roll: ... ]`). Do not invent facts that were not in the original text.
- **Maintain E-E-A-T / Information Gain:** Ensure the unique insight from the main article is preserved in the short-form variant.

## Suggested Process

1. **Analyze Source:** Read the primary article/document. Identify the core thesis, the top 3 most interesting statistics/facts, and the call to action (CTA).
2. **Select Variants:** Based on the requested channels (e.g., Twitter, LinkedIn, Newsletter, TikTok).
3. **Draft Variants:** 
   - *Twitter/X Thread:* 5-7 tweets. Hook -> Problem -> Insight 1 -> Insight 2 -> Conclusion/CTA.
   - *LinkedIn Post:* Text-only format or carousel script. Use an engaging question hook, bulleted insights, and a community-driven closing question.
   - *Short Video Script (TikTok/Reels/Shorts):* 30-60 second read time (~75-150 words). Include `[Visual/Hook]`, `[Body]`, and `[Outro/CTA]` markers.
4. **Review against constraints:** Are the variants too long? Do they sound like AI or do they sound like native social content?
5. **Handoff:** Output the variants clearly labeled for the requester.

## Related Skills

- **write-article**: Use when drafting the core content from scratch.
- **optimize-seo**: Use when ensuring the core content is search-friendly before repurposing.

## Checklist

- [ ] Source article's core thesis and key facts identified.
- [ ] Variants drafted using channel-native formatting (spacing, hooks, threads).
- [ ] No new/unverified facts were invented during shortening.
- [ ] CTA (Call to Action) is present and context-appropriate in each variant.
- [ ] Visual cues or multimedia prompts are properly formatted.
