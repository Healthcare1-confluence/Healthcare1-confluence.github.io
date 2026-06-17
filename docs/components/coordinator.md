# Coordinator Node

## Responsibilities

The coordinator is the first node in the graph, responsible for:

1. **Intent Classification** — Issue a structured LLM call to classify the caller's intent
2. **Identifier Extraction** — Extract member_id, plan_id, date_of_service from conversation
3. **Safety Validation** — Apply Python safety net for edge cases (member_id missing)
4. **State Merging** — Return updated state slice for LangGraph to merge

## LLM Call Details

| Property | Value |
|----------|-------|
| **Model** | Azure OpenAI GPT-5.4-mini |
| **Prompt** | INTENT_PROMPT system message + full messages history |
| **Output Format** | Structured JSON (CoordinatorOutput schema) |
| **Context** | Full message list + injected variables (member_id, plan_id, date_of_service) |

## Safety Net

**Python Validation Layer:**
```python
if output.intent == 'claims' and output.member_id is None:
    output.clarification_needed = True
```

This belt-and-suspenders check prevents mis-serving a member due to missing identifiers.

