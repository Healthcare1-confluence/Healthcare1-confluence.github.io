# High-Level Architecture

## Layered Architecture Pattern

The platform follows a layered architecture with seven distinct layers:

### Layer 1: Channel & Ingestion
- **Components**: Twilio, Azure Communication Services
- **Responsibility**: Inbound voice calls, STT transcription, JWT auth via APIM, member_id injection, thread_id routing
- **Output**: Structured JSON payload with caller utterance

### Layer 2 & 3: FastAPI + LangGraph
- **Components**: FastAPI service, LangGraph StateGraph
- **Responsibility**: Request validation, lazy graph compilation, checkpoint restoration, state orchestration
- **Output**: Graph state updates, compiled graph instance

### Layer 4: Coordinator + HITL Gate
- **Components**: Coordinator LLM Node, HITL Safety Net
- **Responsibility**: Intent classification, identifier extraction, safety validation, agent routing
- **Output**: Classified intent, member identifiers, clarification requests

### Layer 5: Multi-Agent Reasoning
- **Components**: Claims Agent, Benefits Agent, Appointment Agent, General Responder
- **Responsibility**: ReAct tool-use loops, backend data access, LLM synthesis
- **Output**: Plain-English member responses

### Layer 6: Unified State & Knowledge Storage
- **Components**: MongoDB Atlas (checkpoints), Azure SQL (operational data), Azure AI Search (benefit documents)
- **Responsibility**: Durable conversation state, member data, claim data, appointment slots, plan benefits
- **Output**: Persisted state, retrieved data

### Layer 7: Delivery Layer
- **Components**: InvokeResponse, Twilio/ACS TTS
- **Responsibility**: Response formatting, TTS conversion, member delivery
- **Output**: Spoken response to caller

## Data Flow

```
Channel (Voice/STT)
        ↓
FastAPI + Validation
        ↓
LangGraph Compilation & Checkpoint Restore
        ↓
Coordinator (Intent + HITL)
        ↓
[Route to Specialist Agent OR HITL Gate]
        ↓
Agent ReAct Loops (Backend Access)
        ↓
LLM Synthesis & _strip_markdown()
        ↓
MongoDB Checkpoint Save
        ↓
InvokeResponse Assembly
        ↓
TTS Delivery
```

## Key Design Principles

1. **Single State Object** — All data flows through `CallWorkflowState`
2. **Lazy Compilation** — Graph compiled once on first request, cached thereafter
3. **HITL-First Safety** — Missing data triggers clarification before agent invocation
4. **Tool-Use Boundaries** — Each agent has access only to its domain-specific tools
5. **Durable State** — MongoDB checkpoints enable seamless multi-turn conversations

