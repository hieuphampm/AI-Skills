# Prompt Specification: `<Prompt Name>`

## 1. Objective & Model Assumptions
- **Goal**: <One-sentence task definition>
- **Recommended Temperature**: `0.0` (deterministic) / `0.2–0.7` (creative)
- **Target Portability**: OpenAI / Anthropic / Gemini

## 2. System Prompt

```text
<Concise, role-focused system instructions with explicit abstain rules and untrusted-input guardrails>
```

## 3. User Prompt Template

```text
<Task prompt using explicit XML delimiters such as <untrusted_input>{{input}}</untrusted_input>>
```

## 4. Output Contract

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [],
  "properties": {}
}
```

## 5. Verification Test Cases

| Case ID | Input Summary | Expected Behavior / Output |
| :--- | :--- | :--- |
| `happy-01` | <Standard valid input> | <Expected valid output> |
| `edge-02` | <Ambiguous or incomplete input> | <Expected abstain / fallback> |
| `sec-03` | <Prompt injection inside untrusted data> | <Ignores injected directive; preserves schema> |
