# API Reference

## Endpoint

| Property | Value |
|----------|-------|
| **Method** | POST |
| **Path** | `/workflows/call_workflow` |
| **Auth** | Bearer token (Azure AD JWT) |
| **Content-Type** | application/json |
| **Idempotency** | Not idempotent. Each POST creates a new invocation or continues a thread. |

## Request Body

```json
{
  "question": "What is my claim status?",
  "member_id": "M123456",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "metadata": {
    "channel": "twilio",
    "session_id": "sess_xyz"
  }
}
```

### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | ✓ Yes | The caller's utterance for this turn. |
| `member_id` | string | No | Pre-populated member ID from channel integration (CRM lookup). |
| `thread_id` | string | No | UUID of existing conversation thread. Null or absent = new conversation. |
| `metadata` | object | No | Arbitrary key-value pairs passed through to response. |

## Response Body

**HTTP 200 Success**

```json
{
  "answer": "Your claim #CL-9981 was approved on June 1, 2026 for $240.00.",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "intent": "claims",
  "clarification_needed": false,
  "clarification_question": null,
  "metadata": {
    "langfuse_trace_id": "trace_abc123"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | The agent response or HITL clarification question. This is what TTS speaks to the caller. |
| `thread_id` | string | Conversation UUID. Must be passed back on next request to continue the conversation. |
| `intent` | string | Classified intent: 'claims', 'benefits', 'appointment', 'general', or 'default'. |
| `clarification_needed` | boolean | True if this response is a clarification request (HITL gate). |
| `clarification_question` | string \| null | The clarification question text if applicable. |
| `metadata` | object | Pass-through of request metadata enriched with LangFuse trace data. |

## Error Handling

| Status | Meaning | Example |
|--------|---------|---------|
| **400** | Bad Request | Missing required field `question`. |
| **401** | Unauthorized | Invalid or expired Azure AD JWT. Re-authenticate and retry. |
| **422** | Unprocessable Entity | Request body schema violation (Pydantic validation). |
| **500** | Internal Error | Unhandled exception in graph execution. Full trace logged to Application Insights. |
| **503** | Service Unavailable | LangGraph or Azure OpenAI unavailable. Retry with exponential backoff. |

## Example: Claims Intent Flow

### Turn 1: Initial Query (No Member ID)

**Request:**
```json
{
  "question": "What is my claim status?",
  "thread_id": null
}
```

**Response:**
```json
{
  "answer": "Could you please provide your Member ID?",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "intent": "claims",
  "clarification_needed": true,
  "clarification_question": "Could you please provide your Member ID?"
}
```

### Turn 2: Member Provides ID

**Request:**
```json
{
  "question": "My ID is M123",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "answer": "Your claim #CL-9981 was approved on June 1, 2026 for $240.00.",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "intent": "claims",
  "clarification_needed": false,
  "clarification_question": null
}
```

## Example: Appointment Booking

### Request:

```json
{
  "question": "I'd like to book an appointment for next Tuesday afternoon.",
  "member_id": "M456",
  "thread_id": null
}
```

### Response:

```json
{
  "answer": "I found afternoon availability for you next Tuesday at 2 PM and 3 PM. Which would work best for you?",
  "thread_id": "550e8400-e29b-41d4-a716-446655440001",
  "intent": "appointment",
  "clarification_needed": false,
  "metadata": {
    "available_slots": [
      {
        "date": "2026-06-17",
        "time": "14:00",
        "provider": "Dr. Smith"
      },
      {
        "date": "2026-06-17",
        "time": "15:00",
        "provider": "Dr. Smith"
      }
    ]
  }
}
```

