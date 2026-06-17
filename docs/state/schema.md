# State Schema Design

## CallWorkflowState

All data flowing through the graph is carried in a single Pydantic TypedDict subclass.

| Field | Type | Purpose |
|-------|------|---------|
| `messages` | list[BaseMessage] | Append-only conversation history. Uses add_messages reducer. Every node appends its AIMessage output. |
| `member_id` | Optional[str] | Healthcare member identifier extracted by coordinator. Required for claims and benefits intents. |
| `plan_id` | Optional[str] | Insurance plan identifier. Resolved by BenefitsAgent via get_member_plan_id tool. |
| `date_of_service` | Optional[str] | Service date string. Used by ClaimsAgent to filter claim results. |
| `intent` | Optional[str] | Classified intent: 'claims', 'benefits', 'appointment', 'general', or 'default'. |
| `clarification_needed` | bool | True when intent requires data but none was provided. Triggers HITL pause. |
| `clarification_question` | Optional[str] | Natural-language question to return to caller when clarification_needed is True. |
| `agent_response` | Optional[str] | Final plain-English answer. _strip_markdown() applied before storage. |
| `thread_id` | str | UUID identifying the conversation thread. LangGraph checkpoint config key. |
| `metadata` | Dict[str, Any] | LangFuse trace IDs, channel identifiers, operator-defined tags. |

## CoordinatorOutput

Structured output schema for the coordinator LLM call.

```python
class CoordinatorOutput(BaseModel):
    intent: str  # claims, benefits, appointment, general, default
    member_id: Optional[str]  # Extracted from utterance, or null
    plan_id: Optional[str]  # Extracted from utterance, or null
    date_of_service: Optional[str]  # Extracted from utterance, or null
    clarification_needed: bool  # True if required data absent
    clarification_question: Optional[str]  # Question for caller if clarification needed
```

## InvokeResponse

Final API response structure.

```python
class InvokeResponse(BaseModel):
    answer: str  # The agent_response or clarification_question
    thread_id: str  # Conversation UUID to pass back on next turn
    intent: Optional[str]  # Classified intent from this turn
    clarification_needed: bool  # HITL flag
    clarification_question: Optional[str]  # Clarification text if applicable
    metadata: dict  # Pass-through with LangFuse enrichment
```

