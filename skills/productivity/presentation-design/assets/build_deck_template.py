"""Generate a PowerPoint deck from the slide_deck_spec using python-pptx.

Fill in the SLIDES list below from the deck spec, then run:

    pip install python-pptx
    python build_deck.py

The script writes `output.pptx` in the current directory.
"""

from __future__ import annotations

import sys

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
except ImportError:
    sys.exit("python-pptx is required. Install it with: pip install python-pptx")

# Theme (edit to match brand_theme)
PRIMARY = 0x2563EB  # accent
DARK = 0x111827     # body text
LIGHT = 0x6B7280    # secondary text

# Each entry: (title, [bullets], speaker_notes)
SLIDES: list[tuple[str, list[str], str]] = [
    ("Talk Title", ["Subtitle", "Presenter", "Date"], "Welcome and framing."),
    ("Agenda", ["Point one", "Point two", "Point three"], "Preview the flow."),
    ("Summary", ["Key takeaway one", "Key takeaway two", "Next step"], "Close and CTA."),
]


def _add_title_slide(prs: Presentation, title: str, bullets: list[str], notes: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    if slide.placeholders and len(slide.placeholders) > 1:
        body = slide.placeholders[1]
        body.text = "\n".join(bullets)
    if notes:
        slide.notes_slide.notes_text_frame.text = notes


def _add_content_slide(prs: Presentation, title: str, bullets: list[str], notes: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    body = slide.placeholders[1]
    tf = body.text_frame
    tf.text = bullets[0] if bullets else ""
    for bullet in bullets[1:]:
        p = tf.add_paragraph()
        p.text = bullet
        p.level = 0
    if notes:
        slide.notes_slide.notes_text_frame.text = notes


def build(output_path: str = "output.pptx") -> None:
    prs = Presentation()
    for index, (title, bullets, notes) in enumerate(SLIDES):
        if index == 0:
            _add_title_slide(prs, title, bullets, notes)
        else:
            _add_content_slide(prs, title, bullets, notes)
    prs.save(output_path)
    print(f"Wrote {len(SLIDES)} slides to {output_path}")


if __name__ == "__main__":
    build()
