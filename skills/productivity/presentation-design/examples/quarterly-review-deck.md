# Example: Quarterly Review Deck

## Input
- `presentation_brief`: "A 6-slide quarterly review for our engineering leadership. Goal: show what shipped, what's at risk, and what we need next quarter."
- `source_notes`: `q3-notes.md` (a rough list of shipped features and open risks).
- `brand_theme`: "Primary #2563EB, dark text #111827, sans-serif."

## Expected Output (`slide_deck_spec`)

# Slide Deck Spec

## Meta
- **Title**: Q3 Engineering Review
- **Audience**: Engineering leadership.
- **Goal**: Show what shipped, what's at risk, and what we need next quarter.
- **Slide Count**: 6
- **Theme**: Primary #2563EB, dark text #111827, sans-serif.

## Slides

### Slide 1 — Title
- **Title**: Q3 Engineering Review
- **Subtitle**: What shipped, what's at risk, what's next
- **Content**:
  - Engineering Team
  - Q3
- **Speaker Notes**: Frame the review: three questions we'll answer — shipped, at risk, next.

### Slide 2 — Agenda
- **Title**: Today's Agenda
- **Content**:
  - What we shipped
  - What's at risk
  - What we need next quarter
- **Speaker Notes**: Keep it to three buckets so leadership can track the story.

### Slide 3 — What We Shipped
- **Title**: We shipped 4 major features
- **Content**:
  - Instant Reports
  - New onboarding flow
  - API v2
  - Mobile offline mode
- **Speaker Notes**: Highlight the two with the biggest user impact first.

### Slide 4 — What's At Risk
- **Title**: Two risks need attention
- **Content**:
  - Search latency above SLO
  - Single point of failure in billing
- **Speaker Notes**: Be specific about impact and the mitigation already underway.

### Slide 5 — What We Need Next Quarter
- **Title**: Three asks for Q4
- **Content**:
  - +2 backend engineers
  - Search infra budget
  - Billing redundancy plan
- **Speaker Notes**: Tie each ask to a risk or a shipped-feature follow-up.

### Slide 6 — Summary
- **Title**: Summary
- **Content**:
  - Strong quarter on shipping
  - Two risks to close
  - Three asks to approve
- **Speaker Notes**: Close by asking leadership to approve the three asks.

## Notes
- **Theme applied**: Primary #2563EB, dark text #111827, sans-serif across all slides.
- **Assumptions**: Assumed 4 shipped features and 2 risks from `q3-notes.md`; verify counts before presenting.
