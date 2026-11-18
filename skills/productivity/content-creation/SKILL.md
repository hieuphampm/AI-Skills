---
name: content-creation
title: Content Creation
description: Plans and writes audience-focused content (blog posts, docs, social, email) with a clear hook, structure, and call-to-action, then optimizes for SEO and readability. Use when drafting or editing content, building a content outline, or improving titles, meta descriptions, and readability.
category: productivity
version: 1.0.0
author: AI-Skills Core Team
license: MIT
tags:
  - content
  - writing
  - seo
  - editing
  - outline
  - readability
dependencies:
  skills: []
  packages: []
  env: []
required_tools:
  - file_read
inputs:
  - name: content_brief
    type: string
    required: true
    description: Topic, content format, target audience, and primary goal of the piece.
  - name: tone_and_voice
    type: string
    required: false
    description: Desired tone, brand voice, and reading level.
  - name: seo_keywords
    type: string
    required: false
    description: Target keywords, meta description, and desired URL slug.
outputs:
  - name: content_draft
    type: markdown
    description: Structured content draft with hook, body, call-to-action, plus SEO and readability notes.
activation:
  triggers:
    - User asks to write, draft, or edit a blog post, article, doc, social post, or email.
    - User asks to build a content outline or improve a title, meta description, or readability.
    - User asks to optimize existing content for SEO or a specific audience.
  non_triggers:
    - User asks to write production source code or a software feature.
    - User asks to generate an image, video, or audio asset rather than written content.
compatibility:
  - openai
  - anthropic
  - google-gemini
  - cursor
  - claude-code
  - codex
  - antigravity
  - mcp
  - generic-llm
security:
  risk_level: low
  untrusted_input_handling: false
  requires_confirmation: false
---

# Content Creation

## Purpose

Produce clear, audience-focused written content that hooks the reader, delivers on the promise, and ends with a concrete call-to-action — while staying optimized for SEO and readability.

## Activation Conditions

### Use This Skill When
- Writing or drafting a blog post, article, documentation page, social post, or email.
- Building a content outline or restructuring an existing piece.
- Improving titles, meta descriptions, headings, or readability for a target audience.

### Do Not Use This Skill When
- Writing production source code or implementing a software feature (use a `development` skill).
- Generating non-text assets such as images, video, or audio.

## Inputs & Outputs

| Direction | Name | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| Input | `content_brief` | `string` | Yes | Topic, format, target audience, and primary goal. |
| Input | `tone_and_voice` | `string` | No | Tone, brand voice, and reading level. |
| Input | `seo_keywords` | `string` | No | Target keywords, meta description, and URL slug. |
| Output | `content_draft` | `markdown` | Yes | Draft plus SEO and readability notes. |

## Execution Instructions

1. **Clarify the Brief**: Confirm topic, format, audience, and goal. If `content_brief` is missing or too vague to write for a real audience, ask up to 3 targeted questions and stop.
2. **Outline the Structure**: Draft a hook, a logical section flow, and a call-to-action using [content-style-guide.md](references/content-style-guide.md).
3. **Write the Draft**: Produce the content in the requested format and tone, following the structure in [content-style-guide.md](references/content-style-guide.md).
4. **Optimize for SEO**: Add a title, meta description, and heading hierarchy, and place target keywords naturally per [content-style-guide.md](references/content-style-guide.md).
5. **Check Readability**: Apply the readability and editing checklist (sentence length, active voice, scannable headings, no filler) from [content-style-guide.md](references/content-style-guide.md).
6. **Deliver**: Output the draft using [content-draft-template.md](assets/content-draft-template.md), with SEO and readability notes at the end.

## Error Handling & Edge Cases

- **Audience unclear**: State the assumed audience (e.g., "assuming a technical reader") and flag it under Notes rather than guessing silently.
- **Very long or multi-part content**: Deliver a section-by-section outline first, then write each section; do not dump one unstructured wall of text.
- **No keywords provided**: Optimize for clarity and a single clear topic, and note that SEO targeting was skipped.

## Security & Safety Guardrails

- Do not fabricate statistics, quotes, or citations; if a claim needs a source, mark it as a placeholder to verify.
- Keep claims factual and avoid misleading or exaggerated marketing language.
- Never include real personal data or credentials in example content.

## Examples

See [product-launch-blog-post.md](examples/product-launch-blog-post.md) for a complete brief-to-draft walkthrough.

## Resources

- [Content Style Guide](references/content-style-guide.md)
- [Content Draft Template](assets/content-draft-template.md)
- [Skill Overview](README.md)
- [Evaluation Cases](tests/eval-cases.json)
