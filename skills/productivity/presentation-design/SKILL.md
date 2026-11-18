---
name: presentation-design
title: Presentation Design
description: Designs a clear, audience-focused PowerPoint deck from a topic or outline — slide-by-slide structure, speaker notes, and a python-pptx script to generate the .pptx. Use when creating slide decks, pitch decks, or turning notes into a presentable PowerPoint.
category: productivity
version: 1.0.0
author: AI-Skills Core Team
license: MIT
tags:
  - presentation
  - slides
  - powerpoint
  - pitch-deck
  - python-pptx
dependencies:
  skills: []
  packages:
    - python-pptx
  env: []
required_tools:
  - file_read
  - file_write
  - shell_exec
inputs:
  - name: presentation_brief
    type: string
    required: true
    description: Topic, audience, goal of the talk, and desired number of slides.
  - name: source_notes
    type: file
    required: false
    description: Optional outline, notes, or source document to base the deck on.
  - name: brand_theme
    type: string
    required: false
    description: Colors, fonts, logo, and any brand guidelines to apply.
outputs:
  - name: slide_deck_spec
    type: markdown
    description: Slide-by-slide outline with titles, bullet content, and speaker notes.
  - name: build_deck_script
    type: file
    description: A python-pptx script that generates the .pptx from the spec.
activation:
  triggers:
    - User asks to create, design, or build a PowerPoint deck or slide presentation.
    - User asks to turn notes, an outline, or a document into slides or a pitch deck.
    - User asks to generate a .pptx file or a python-pptx script for a presentation.
  non_triggers:
    - User asks to write a blog post, article, or other non-slided written content.
    - User asks to design a UI mockup, poster, or image rather than a slide deck.
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
  risk_level: medium
  untrusted_input_handling: false
  requires_confirmation: true
---

# Presentation Design

## Purpose

Turn a topic, outline, or set of notes into a clear, audience-focused PowerPoint deck — a slide-by-slide structure with speaker notes, plus a `python-pptx` script that generates the actual `.pptx` file.

## Activation Conditions

### Use This Skill When
- Creating, designing, or building a PowerPoint deck or slide presentation.
- Turning notes, an outline, or a document into slides or a pitch deck.
- Generating a `.pptx` file or a `python-pptx` script for a presentation.

### Do Not Use This Skill When
- Writing a blog post, article, or other non-slided written content (use `content-creation`).
- Designing a UI mockup, poster, or static image rather than a slide deck.

## Inputs & Outputs

| Direction | Name | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| Input | `presentation_brief` | `string` | Yes | Topic, audience, goal, and desired slide count. |
| Input | `source_notes` | `file` | No | Optional outline, notes, or source document. |
| Input | `brand_theme` | `string` | No | Colors, fonts, logo, and brand guidelines. |
| Output | `slide_deck_spec` | `markdown` | Yes | Slide-by-slide outline with titles, bullets, and speaker notes. |
| Output | `build_deck_script` | `file` | Yes | A `python-pptx` script that builds the `.pptx`. |

## Execution Instructions

1. **Clarify the Brief**: Confirm topic, audience, goal, and slide count. If `presentation_brief` is missing or too vague, ask up to 3 targeted questions and stop.
2. **Outline the Deck**: Design the slide flow (title, agenda, one idea per slide, summary, CTA) using [slide-design-guide.md](references/slide-design-guide.md).
3. **Write Speaker Notes**: Add concise speaker notes for each slide so the deck is presentable, not just readable.
4. **Apply the Theme**: Map `brand_theme` (colors, fonts) into the design; if none is given, use a clean default from [slide-design-guide.md](references/slide-design-guide.md).
5. **Generate the Script**: Produce a `python-pptx` script from [build_deck_template.py](assets/build_deck_template.py) that builds the deck from the spec.
6. **Deliver**: Output the `slide_deck_spec` using [slide-deck-template.md](assets/slide-deck-template.md) and the `build_deck_script` file.

## Error Handling & Edge Cases

- **Too much content per slide**: Split into multiple slides; keep to the 6x6 rule (max ~6 bullets, ~6 words per bullet) from [slide-design-guide.md](references/slide-design-guide.md).
- **No audience given**: Assume a general professional audience and flag the assumption under Notes.
- **`python-pptx` not installed**: The script should fail fast with a clear message to `pip install python-pptx`; do not silently skip generation.

## Security & Safety Guardrails

- The generated script only writes a local `.pptx` file; it must not read secrets, access the network, or execute arbitrary user input.
- Do not embed real credentials, tokens, or personal data into slides or the script.
- Because this skill runs a build script, confirm the output path with the user before generating files.

## Examples

See [quarterly-review-deck.md](examples/quarterly-review-deck.md) for a complete brief-to-deck walkthrough.

## Resources

- [Slide Design Guide](references/slide-design-guide.md)
- [Slide Deck Template](assets/slide-deck-template.md)
- [Build Deck Script Template](assets/build_deck_template.py)
- [Skill Overview](README.md)
- [Evaluation Cases](tests/eval-cases.json)
