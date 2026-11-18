# Presentation Design

Human-facing overview and usage guide for the `presentation-design` skill.

## Overview

`presentation-design` turns a topic, outline, or set of notes into a clear, audience-focused PowerPoint deck. It produces two artifacts:

1. **`slide_deck_spec`** — a slide-by-slide outline with titles, bullet content, and speaker notes.
2. **`build_deck_script`** — a `python-pptx` script that generates the actual `.pptx` file from the spec.

## Directory Structure

- `SKILL.md` — Agent-facing specification, metadata, and execution instructions.
- `README.md` — Human-facing documentation and integration notes.
- `references/slide-design-guide.md` — Slide structure, content density, and theming guide.
- `assets/slide-deck-template.md` — Output template for the deck spec.
- `assets/build_deck_template.py` — `python-pptx` script template.
- `examples/quarterly-review-deck.md` — End-to-end brief-to-deck walkthrough.
- `tests/eval-cases.json` — Trigger and behavioral evaluation cases.

## Quick Usage

Invoke this skill in any compatible agent by referencing `skills/productivity/presentation-design/SKILL.md`. To build a deck locally:

```bash
pip install python-pptx
python build_deck.py   # generates the .pptx from the spec
```
