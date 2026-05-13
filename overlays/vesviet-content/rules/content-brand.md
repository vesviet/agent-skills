# Vesviet Content Brand Rules

Voice, style, and publishing constraints for the Vesviet portfolio site and the Learn notes site.

## Voice and Tone

| Site | Language | Tone |
|------|----------|------|
| Vesviet (`tanhdev.com`) | English | Professional, authoritative, technical deep-dive. Write for Senior Engineers and Architects. |
| Learn (`learn.tanhdev.com`) | Vietnamese (primary), English (series) | Conversational-technical. Use Vietnamese colloquial phrasing where it aids clarity, but keep terminology in English (e.g., "Context Window", "Prompt Injection"). |

## Style Constraints

- **Meta description:** ≤ 160 characters. Must contain the primary keyword.
- **Title:** Use sentence case. Series parts must include the part number (e.g., "Part 1 — ...").
- **Headings:** Use numbered sections for series parts (e.g., `## 1.1.`, `## 3.4.`). Use plain headings for standalone posts.
- **Code snippets:** Always include a module-level comment or docstring explaining the code's purpose. Specify the language in fenced blocks.
- **Production Failure stories:** Use the standardized template:
  ```
  > 🔥 **[Production Failure]: <Title>**
  > **Symptom:** ...
  > **Root Cause:** ...
  > 📊 **Impact:** ...
  > 📈 **Resolution:** ...
  > *(Source: ...)*
  ```
- **Internal links:** Use relative paths within the same Hugo site. Use absolute URLs (`https://tanhdev.com/...`) when linking cross-site (e.g., Learn → Vesviet radar).
- **Prerequisite block:** Every series part must open with a `> **Prerequisite:**` blockquote linking to the foundational article.
- **CTA / Next Step:** Every series part must close with a `🔗 **Next Step:**` or `🔗 **Bước tiếp theo:**` transition linking to the next part.

## Publishing Constraints

- Do not publish with `draft: true` unless intentionally staging content.
- All dates must use `+07:00` timezone offset (Asia/Ho_Chi_Minh).
- Series index (`_index.md`) must be `draft: false` before any child part goes live.
- Frontmatter field ordering: `title`, `date`, `draft`, `description`, `ShowToc`, `TocOpen`, `weight`, `categories`, `tags`.

## Prohibited Patterns

- No placeholder images or "lorem ipsum" text in published content.
- No hardcoded absolute paths in code snippets (use environment variables or config).
- No unused imports in code snippets — all code must pass basic linting for its language.
- No Vietnamese-only technical terms without the English equivalent on first mention (e.g., "Personally Identifiable Information (PII)").
