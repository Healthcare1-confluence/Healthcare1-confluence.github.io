# End-to-End Workflow

## Seven-Step Pipeline

The platform processes every inbound call through a seven-step pipeline — from channel ingestion through intent classification, specialist agent tool use, data retrieval, LLM synthesis, and durable checkpoint persistence.

### Step 1: Inbound Call

**Input:** Member calls via Twilio or Azure Communication Services

- Voice audio stream captured
- STT (Speech-to-Text) transcription
- JWT authentication via Azure API Management
- Member_ID injection from CRM (if available)
- Thread_ID routing for conversation continuity

**Output:** Structured JSON payload with caller's utterance

### Step 2: FastAPI + LangGraph

**Input:** HTTP POST /workflows/call_workflow with:
- `question` — caller's utterance
- `member_id` — optional pre-populated identifier
- `thread_id` — optional UUID for returning calls

**Process:**
- Validate JWT and schema via FastAPI
- Delegate to `CallWorkflow.invoke()`
- First request: compile and cache LangGraph StateGraph
- If thread_id provided: restore prior checkpoint from MongoDB
- Initialize or merge CallWorkflowState

**Output:** Ready-to-execute graph state

### Step 3: Coordinator Node

**Input:** Current CallWorkflowState with conversation history

**Process:**
- Issue single structured LLM call (Azure OpenAI GPT-5.4-mini)
- INTENT_PROMPT system message + full conversation history
- Output format: CoordinatorOutput JSON schema (enforced)

**LLM Extracts:**
- `intent` — claims, benefits, appointment, general, or default
- `member_id` — extracted from utterance (if present)
- `plan_id` — extracted from utterance (if present)
- `date_of_service` — extracted from utterance (if present)
- `clarification_needed` — boolean flag

**Safety Net (Python):**
- If intent='claims' AND member_id=None → force clarification_needed=True
- Override LLM output to prevent member mis-service

**Output:** Updated CallWorkflowState with extracted identifiers and classification

### Step 4: Specialist Agent Routing

**Process:** _coordinator_route() conditional logic

| Route | Condition | Handler |
|-------|-----------|---------|
| `claims_agent` | intent='claims' AND clarification_needed=false | ReAct tool-use loop |
| `benefits_agent` | intent='benefits' AND clarification_needed=false | ReAct tool-use loop |
| `appointment_agent` | intent='appointment' AND clarification_needed=false | ReAct tool-use loop |
| `general_responder` | intent='general' OR 'default' AND clarification_needed=false | Single LLM call |
| `__end__` (HITL) | clarification_needed=true | Early termination → clarification question |

### Step 5: Data Layer Access

**Query Backends:**

- **Azure SQL** (pyodbc, parameterised queries)
  - Member table: demographics, plan_id
  - Claims_Professional & Claims_Institutional: claim status, amounts, denial reasons
  - pre_auth table: authorization constraints
  - Provider_Slot_2: available appointment slots
  - Appointment table: booked appointments

- **Azure AI Search** (hybrid keyword + semantic)
  - Plan benefits corpus
  - Filtered by plan_id on every search
  - Returns top-5 chunks with relevance scores

**Agent ReAct Loop:**
- LLM selects tools based on query
- Tool results returned to agent
- LLM evaluates if more information needed
- Repeat until answer is complete (max 5 iterations)

### Step 6: LLM Synthesis

**Process:**
- ReAct loop completes after agent has sufficient information
- Agent LLM synthesises plain-English response
- `_strip_markdown()` applied to ensure TTS readability
- No markdown formatting symbols in output

**Result:** Clean, voice-ready answer

### Step 7: Persistence & Delivery

**MongoDB Checkpoint:**
- Full final CallWorkflowState saved under thread_id
- Collections: langgraph_checkpoints + langgraph_checkpoint_writes
- Enables seamless resumption on next call

**InvokeResponse Assembly:**
- `answer` — agent response or clarification question
- `thread_id` — conversation UUID (to be passed back by client)
- `intent` — classified intent from this turn
- `clarification_needed` — HITL flag
- `metadata` — LangFuse trace IDs, channel info

**TTS Delivery:**
- JSON response returned as HTTP 200 OK
- Channel layer converts `answer` field to speech
- Spoken response delivered to caller

---

## Complete Flow Diagram

```
1. Voice Call → STT Transcription
        ↓
2. FastAPI Validation
        ↓
3. Graph Compilation (first call only)
        ↓
4. Checkpoint Restore (if thread_id provided)
        ↓
5. Coordinator LLM Call
        ↓
6. Safety Net Check (member_id validation)
        ↓
    [clarification_needed?]
         ↙        ↘
    YES: HITL     NO: Agent Route
    Gate          ↓
    (early        7. Specialist Agent
    return)       ReAct Loop
                  ↓
                  8. Tool Calls
                  (SQL/Search)
                  ↓
                  9. LLM Synthesis
                  ↓
                  10. _strip_markdown()
                  ↓
                  11. MongoDB Checkpoint
                  ↓
                  12. InvokeResponse
                  ↓
    ←─────────────┘
                  ↓
13. TTS Conversion → Caller
```

