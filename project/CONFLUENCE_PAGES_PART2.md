# Confluence Pages - Part 2 (Component Design through End)

## 📄 CHILD PAGE: Coordinator Node

```
h1. Coordinator Node

h2. Responsibilities

* Issue a single structured LLM call (Azure OpenAI) with the full conversation history and an intent classification prompt.
* Parse the CoordinatorOutput JSON response and merge extracted fields into CallWorkflowState.
* Apply a safety net: if intent == 'claims' and member_id is absent, force clarification_needed = True regardless of LLM output.
* Return the updated state slice – LangGraph merges it into the running state.

h2. LLM Call Details

| Property | Value |
|----------|-------|
| Model | Azure OpenAI (AZURE_OPENAI_ENDPOINT + OPENAI_API_KEY) |
| Prompt | INTENT_PROMPT system message + full messages history + injected variables: message, history_summary, member_id, plan_id, date_of_service |
| Output Format | Structured JSON conforming to CoordinatorOutput schema. Enforced via function calling / JSON mode. |
| Context Window | Full messages list passed. history_summary compresses prior context for long conversations. |
| Safety Net | Post-LLM Python check: intent='claims' AND member_id=None – override clarification_needed=True |

{toc}
```

---

## 📄 CHILD PAGE: Claims Agent

```
h1. Claims Agent

ClaimsAgent is a LangChain ReAct agent with three Azure SQL tools. It runs an autonomous tool-use loop: it selects tools, inspects results, and continues until it has enough information to formulate a complete plain-English answer.

h2. Tools

| Tool | Backend | Description |
|------|---------|-------------|
| query_member_info | Azure SQL | SELECT * FROM Member WHERE Member_ID=? Returns member demographics JSON. Called first to validate member existence. |
| query_claims | Azure SQL | SELECT from Claims_Professional + Claims_Institutional filtered by member_id and optional date_from. Returns list of claims (max 20 records). |
| query_preauth | Azure SQL | SELECT preauthorisation records for member. Called when caller asks about pending approvals or preauth status. |

h2. Context Enrichment

Before entering the ReAct loop, the claims agent node prepends a context message to the messages list: {Context: member_id, date_of_service}. This ensures the LLM inside ClaimsAgent always has these identifiers available without re-parsing the conversation history.

h2. Database Connectivity

| Property | Value |
|----------|-------|
| Driver | pyodbc with SQL Server ODBC driver. Connection pooling managed at application level. |
| Connection | Parameterised via AZURE_SQL_CONNECTION_STRING environment variable. |
| Execution | run_in_executor wraps synchronous pyodbc calls for async compatibility with LangGraph's asyncio loop. |
| Security | All queries use parameterised placeholders (?). No string interpolation. Principle of least privilege on the DB service account. |

{toc}
```

---

## 📄 CHILD PAGE: Benefits Agent

```
h1. Benefits Agent

BenefitsAgent is a LangChain ReAct agent with two tools covering Azure SQL for plan metadata and Azure AI Search for benefit document retrieval. This hybrid approach ensures both structured plan data and unstructured benefit content are available to the LLM.

h2. Tools

| Tool | Backend | Description |
|------|---------|-------------|
| get_member_plan_id | Azure SQL | SELECT Plan_ID, Plan_Type, Line_of_Business FROM Member WHERE Member_ID=? Resolves the member's active plan. |
| search_plan_benefits | Azure AI Search | Semantic or keyword search over the plan benefits corpus. Filtered by plan_id. Returns top-5 benefit document chunks with relevance scores. |

h2. Search Index Configuration

| Property | Value |
|----------|-------|
| Index Name | Configured via AZURE_SEARCH_INDEX_NAME environment variable. |
| Search Type | Hybrid (keyword + vector semantic re-rank) for maximum recall on natural-language benefit queries. |
| Filter | plan_id filter applied on every search to prevent cross-plan data leakage. |
| Result Count | Top-5 chunks returned. Each chunk carries content text and relevance score. |

{toc}
```

---

## 📄 CHILD PAGE: Appointment Scheduler Agent

```
h1. Appointment Scheduler Agent

AppointmentSchedulerAgent is a LangChain ReAct agent with eight specialised tools covering appointment lifecycle management. It enables members to view, book, reschedule, and cancel appointments while respecting pre-authorization constraints and provider availability windows.

The agent handles:

* *Availability queries* – search by date, date range, provider, or time-of-day preference.
* *Booking operations* – create appointments with authorization validation and one-active-appointment-per-member enforcement.
* *Modifications* – reschedule or cancel existing appointments with atomic slot updates.
* *Smart suggestions* – recommend alternatives when requested slots are unavailable.

h2. Tools

| Tool | Backend | Description |
|------|---------|-------------|
| get_available_slots | Provider_Slot_2 | Fetch available slots for a date, filtered by provider_name and time_of_day. Returns up to 20 slots. |
| validate_appointment_slot | Provider_Slot_2 | Verify a specific date+time slot is available before booking. Returns slot_id, provider info, availability status. |
| book_appointment | Appointment + Provider_Slot_2 | Create Appointment record + set Is_Booked=1. Validates pre-auth. Enforces one-active-appointment constraint. Returns appointment_id or alternatives. |
| reschedule_appointment | Appointment + Provider_Slot_2 | Atomically release old slot, book new slot, update Appointment record. Validates new availability before committing. |
| cancel_appointment | Appointment + Provider_Slot_2 | Set Appointment.Status='Cancelled' and release Provider_Slot_2.Is_Booked=0. Frees slot for future bookings. |
| get_slots_for_range | Provider_Slot_2 | Fetch available slots across a date range. Supports 'next 5 days', 'this week', date range expressions. |
| get_earliest_available_slot | Provider_Slot_2 | Find single earliest available slot from today or a given start date. |
| get_member_appointments | Appointment | Retrieve all upcoming scheduled appointments for a member with full details. |

h2. Database Schema

*Provider_Slot_2 Table – Available appointment slots*

| Column | Type | Purpose |
|--------|------|---------|
| Slot_ID | UUID | Primary key. Unique slot identifier. |
| Provider_Name | VARCHAR(255) | Matched against pre_auth.Provider_Name. |
| Date | DATETIME | Queried with CAST(Date AS DATE) for comparison. |
| Start_Time | VARCHAR(10) | 12-hour format e.g. '06:00 PM'. Filtered by time_of_day range. |
| Is_Booked | BIT | 0=available, 1=booked, NULL=available. Updated atomically by book/cancel tools. |
| Appointment_ID | VARCHAR(20) | NULL if unbooked. Set by book_appointment. |

*Appointment Table – Booked member appointments*

| Column | Type | Purpose |
|--------|------|---------|
| Appointment_ID | VARCHAR(20) | Primary key e.g. 'APTU1A2B3C4D5'. Returned as booking confirmation. |
| Member_ID | VARCHAR(20) | Foreign key to Member table. |
| Status | VARCHAR(20) | Scheduled or Cancelled. |
| Appointment_booking_timestamp | FLOAT | Unix timestamp. Audit trail for HIPAA compliance. |

*pre_auth Table – Pre-authorization constraints*

| Column | Purpose |
|--------|---------|
| Member_ID | Constrains which provider a member may book with. |
| Provider_Name | Authorized provider. Matched against Provider_Slot_2.Provider_Name. |
| Status | Approved / In Review = booking permitted. Expired = blocked. |

h2. Natural Language Support

The appointment tools parse natural-language date and time expressions before issuing SQL queries. All parsing is performed client-side to prevent injection.

| Input Type | Examples |
|------------|----------|
| Keywords | 'today', 'tomorrow', 'next Monday', 'this weekend', 'end of month' |
| Explicit dates | '29 June 2026', '2026-06-29', '6/29/2026' |
| Date ranges | 'next 5 days', 'this week', 'between June 1 and June 5' |
| Time periods | 'morning' (06:00–11:59), 'afternoon' (12:00–16:59), 'evening' (17:00–20:59) |
| Explicit times | '6 PM', '18:00', '6:00 PM' – normalised via _format_time() |

{toc}
```

---

## 📄 CHILD PAGE: General Responder

```
h1. General Responder

The general responder handles all non-claims, non-benefits, non-appointment intents. It makes a single LLM call – no tool use – and is optimised for low latency and concise output.

| Property | Value |
|----------|-------|
| LLM Call | Single ainvoke() with GENERAL_PROMPT system message. |
| Variables | message (current utterance), history_summary (compressed prior turns). |
| Output Format | Plain English. 1-2 sentences maximum. No markdown. _strip_markdown() applied post-generation. |
| Intent Routing | Receives all intent='general' and intent='default' traffic from coordinator. |
| No HITL Gate | General intent never triggers clarification_needed. No member identifiers required. |

{toc}
```

---

## 📑 SECTION PARENT PAGE: State Schema Design

```
h1. State Schema Design

All data flowing through the graph is carried in a single Pydantic TypedDict subclass, CallWorkflowState. LangGraph merges partial state updates returned by each node into the running state object. No node receives anything except state – there are no side channels or global variables.

---

h2. 📋 State Fields

{page-tree:root=@self}

* [CallWorkflowState|CallWorkflowState]
* [CoordinatorOutput|CoordinatorOutput]
* [InvokeResponse|InvokeResponse]

---

h2. 🔑 Key Concepts

* Single state object carries all conversation context
* Append-only messages history with add_messages reducer
* State reducers ensure idempotent merging across node boundaries
* Type-safe Pydantic validation on every update

{toc}
```

---

## 📄 CHILD PAGE: CallWorkflowState

```
h1. CallWorkflowState

| Field | Type | Purpose |
|-------|------|---------|
| messages | list[BaseMessage] | Append-only conversation history. Uses add_messages reducer. Every node appends its AIMessage output. |
| member_id | Optional[str] | Healthcare member identifier extracted by coordinator. Required for claims and benefits intents. |
| plan_id | Optional[str] | Insurance plan identifier. Resolved by BenefitsAgent via get_member_plan_id tool. |
| date_of_service | Optional[str] | Service date string. Used by ClaimsAgent to filter claim results. |
| intent | Optional[str] | Classified intent: 'claims', 'benefits', 'appointment', 'general', or 'default'. Set by coordinator LLM call. |
| clarification_needed | bool | True when intent requires member_id but none was provided. Triggers HITL pause. |
| clarification_question | Optional[str] | Natural-language question to return to the caller when clarification_needed is True. |
| agent_response | Optional[str] | Final plain-English answer. _strip_markdown() applied before storage. |
| thread_id | str | UUID identifying the conversation thread. LangGraph checkpoint config key. |
| metadata | Dict[str, Any] | LangFuse trace IDs, channel identifiers, and operator-defined tags. |

{toc}
```

---

## 📄 CHILD PAGE: CoordinatorOutput

```
h1. CoordinatorOutput

CoordinatorOutput is a Pydantic BaseModel used as the structured output schema for the coordinator LLM call. Azure OpenAI is instructed to return JSON conforming to this schema.

| Field | Description |
|-------|-------------|
| intent | str – Classified intent. One of: claims, benefits, appointment, general, default. |
| member_id | str | null – Member ID extracted from utterance, or null if absent. |
| plan_id | str | null – Plan ID if mentioned, or null. |
| date_of_service | str | null – Date of service if mentioned, or null. |
| clarification_needed | bool – True if required data absent from utterance and state. |
| clarification_question | str | null – Question to ask the caller when clarification_needed is True. |

{toc}
```

---

## 📄 CHILD PAGE: InvokeResponse

```
h1. InvokeResponse

InvokeResponse is assembled by CallWorkflow.invoke() from the final CallWorkflowState once the graph terminates. It is serialised to JSON and returned to the FastAPI route handler.

| Field | Description |
|-------|-------------|
| answer | str – The agent_response or clarification_question. This is what the TTS engine speaks to the caller. |
| thread_id | str – The thread UUID. Must be passed back by the client on the next turn. |
| intent | str | null – The classified intent from this turn. |
| clarification_needed | bool – True if this response is a clarification request. |
| clarification_question | str | null – The clarification question text if applicable. |
| metadata | dict – Pass-through of state.metadata, enriched with LangFuse trace data. |

{toc}
```

---

## 📑 SECTION PARENT PAGE: Human-in-the-Loop (HITL)

```
h1. Human-in-the-Loop (HITL)

h2. Overview

HITL in this system refers to the pattern where the AI workflow pauses mid-execution to request additional information from the human caller. It is not a human agent takeover – it is a structured clarification request that allows the graph to resume with complete data on the next conversational turn.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [Trigger Conditions|HITL Trigger Conditions]
* [Turn-by-Turn Flow|HITL Turn-by-Turn Flow]
* [State Preservation|HITL State Preservation]

---

h2. ⚠️ Safety Gates

The HITL pattern provides a belt-and-suspenders safety net:

* Coordinator LLM detects missing identifiers
* Python safety net overrides LLM output if required data absent
* Graph terminates early and requests clarification
* State preserved in MongoDB for seamless resumption
* No specialist agent invoked until data is complete

{toc}
```

---

## 📄 CHILD PAGE: HITL Trigger Conditions

```
h1. HITL Trigger Conditions

| Trigger | Description |
|---------|-------------|
| Missing member_id for claims intent | Coordinator classifies intent='claims' but member_id is absent from both the current utterance and existing state. Safety net forces clarification_needed=True. |
| LLM-detected ambiguity | Coordinator LLM may set clarification_needed=True with a specific question for any intent where key data cannot be inferred. |

{toc}
```

---

## 📄 CHILD PAGE: HITL Turn-by-Turn Flow

```
h1. HITL Turn-by-Turn Flow

h2. Turn 1 – Missing Information Detected

* Caller sends POST /workflows/call_workflow with question: 'What is my claim status?' – no member_id provided.
* CallWorkflow.invoke() calls compile() – retrieves/builds CompiledGraph.
* LangGraph ainvoke(initial_state) – coordinator node fires.
* LLM returns CoordinatorOutput: {intent:'claims', member_id:null, clarification_needed:true, clarification_question:'Could you provide your Member ID?'}.
* Python safety net confirms: intent=claims and member_id=None – clarification_needed forced True.
* _coordinator_route returns '__end__'. Graph terminates early – no specialist agent is invoked.
* LangGraph saves checkpoint to MongoDB with the generated thread_id.
* CallWorkflow assembles InvokeResponse: answer='Could you provide your Member ID?', clarification_needed=True, thread_id='uuid-xyz'.
* FastAPI returns 200 OK. TTS speaks clarification question to caller.

h2. Turn 2 – Caller Provides Missing Data

* Caller sends POST /workflows/call_workflow with question: 'My ID is M123', thread_id: 'uuid-xyz'.
* LangGraph restores prior checkpoint for thread_id='uuid-xyz' – full message history intact.
* Coordinator re-fires with enriched state (member_id='M123' now present in messages).
* LLM returns: {intent:'claims', member_id:'M123', clarification_needed:false}.
* Safety net passes – member_id is present. _coordinator_route returns 'claims_agent'.
* ClaimsAgent executes ReAct loop, queries Azure SQL, returns claim status.
* Graph terminates normally. Full InvokeResponse returned. Thread_id preserved for further turns.

{toc}
```

---

## 📄 CHILD PAGE: HITL State Preservation

```
h1. HITL State Preservation

{note}
*Checkpoint Architecture* — The MongoDBSaver stores a full serialised snapshot of CallWorkflowState (including all messages) keyed by thread_id. When LangGraph resumes with the same thread_id, it deserialises the prior state before invoking any node. This means the coordinator on Turn 2 sees the complete conversation history from Turn 1 – enabling coherent multi-turn reasoning without any client-side state management.
{note}

{toc}
```

---

## 📑 SECTION PARENT PAGE: Persistence and Checkpointing

```
h1. Persistence and Checkpointing

h2. Overview

All conversation state is durably persisted to enable seamless multi-turn HITL workflows and full audit trails.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [MongoDB Checkpointer|MongoDB Checkpointer]
* [MemorySaver Fallback|MemorySaver Fallback]
* [Thread ID Management|Thread ID Management]

---

h2. 🔑 Persistence Strategy

* Primary: MongoDB Atlas – durable across service restarts
* Fallback: In-memory MemorySaver – zero-downtime service continuity
* Indexed: thread_id – fast checkpoint lookup and restoration
* Compressed: history_summary – token efficiency for long conversations

{toc}
```

---

## 📄 CHILD PAGE: MongoDB Checkpointer

```
h1. MongoDB Checkpointer (Primary)

The MongoDBSaver is the primary persistence backend, providing durable cross-request state for all HITL scenarios and multi-turn conversations.

| Property | Value | Notes |
|----------|-------|-------|
| Database | directline_db | Dedicated database for call workflow state. |
| Collection 1 | langgraph_checkpoints | Stores complete serialised CallWorkflowState snapshot per thread_id and checkpoint version. |
| Collection 2 | langgraph_checkpoint_writes | Stores incremental write operations between full checkpoints. Enables efficient partial state recovery. |
| Connection Timeout | 5 seconds | MongoClient constructor timeout. Prevents startup blocking on unavailable MongoDB. |
| Connection String | MONGODB_URL env var | Injected at runtime. Supports MongoDB Atlas or self-hosted deployments. |

{toc}
```

---

## 📄 CHILD PAGE: MemorySaver Fallback

```
h1. MemorySaver Fallback

If MongoClient fails to connect within 5 seconds, CallWorkflow falls back to LangGraph's built-in MemorySaver. MemorySaver stores checkpoints in process memory – state is not durable across application restarts, but the service continues to function for single-session interactions.

{toc}
```

---

## 📄 CHILD PAGE: Thread ID Management

```
h1. Thread ID Management

The thread_id is a UUID generated on the first invocation of a new conversation. It is:

* Returned to the caller in every InvokeResponse.
* Passed back by the client in subsequent requests to the same conversation.
* Used as the LangGraph config key (config={'configurable': {'thread_id': thread_id}}) to select the correct checkpoint.
* Scoped to a single member contact session – a new call generates a new thread_id.

{toc}
```

---

## 📑 SECTION PARENT PAGE: Walkthrough Scenarios

```
h1. Intent Flow Walkthroughs

The following scenarios demonstrate how the platform handles different intent types end-to-end.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [General Intent – Greeting|General Intent – Greeting]
* [Benefits Intent – Coverage Enquiry|Benefits Intent – Coverage Enquiry]
* [Claims Intent – Happy Path|Claims Intent – Happy Path]
* [Appointment Intent – Booking|Appointment Intent – Booking]

{toc}
```

---

## 📄 CHILD PAGE: General Intent – Greeting

```
h1. General Intent – Greeting / Account Updates

This is the simplest and fastest path through the graph. It demonstrates the baseline routing logic.

# Step 1

Client invokes with question: "Hello, how can you help me?"

LangGraph ainvoke(initial_state) triggered.

# Step 2

LLM classifies {intent:'general', clarification_needed:false}

_coordinator_route evaluates – returns 'general_responder'.

# Step 3

Single LLM call with GENERAL_PROMPT – 1-2 sentence reply

_strip_markdown(answer) called. No tools, no database queries.

# Step 4

InvokeResponse assembled and returned to caller

Lowest latency path in the graph. No HITL gate required.

{toc}
```

---

## 📄 CHILD PAGE: Benefits Intent – Coverage Enquiry

```
h1. Benefits Intent – Coverage Enquiry

Example: Caller asks 'Is acupuncture covered?' with member_id='M456' pre-populated.

# Step 1

Coordinator LLM: {intent:'benefits', member_id:'M456', clarification_needed:false}

_coordinator_route – 'benefits_agent'.

# Step 2

ReAct iteration 1: get_member_plan_id – Azure SQL

Returns {plan_id:'PLN-001', plan_type:'PPO', ...}.

# Step 3

ReAct iteration 2: search_plan_benefits – Azure AI Search

Filter plan_id='PLN-001' – returns top-5 benefit chunks with relevance scores.

# Step 4

LLM synthesises plain-English answer. State updated. 200 OK.

{toc}
```

---

## 📄 CHILD PAGE: Claims Intent – Happy Path

```
h1. Claims Intent – Happy Path (Full Lifecycle)

Example: Caller provides member_id='M123' upfront. Intent classified as claims. All required data present – no HITL required.

# Step 1

POST /workflows/call_workflow with question, member_id='M123', thread_id

compile() called – first call only: MongoDBSaver connected, StateGraph assembled, compiled, cached.

# Step 2

Coordinator LLM: {intent:'claims', member_id:'M123', clarification_needed:false}

Safety net passes. _coordinator_route returns 'claims_agent'.

# Step 3

ReAct: query_member_info – Azure SQL: SELECT * FROM Member WHERE Member_ID=?

# Step 4

ReAct: query_claims – Claims_Professional + Claims_Institutional (max 20 records)

# Step 5

LLM synthesises plain-English answer. MongoDB checkpoint saved.

FastAPI returns 200 OK with {answer, thread_id, intent:'claims', clarification_needed:false}.

{toc}
```

---

## 📄 CHILD PAGE: Appointment Intent – Booking

```
h1. Appointment Intent – Booking Scenario (Happy Path)

Example: Caller asks 'I'd like to book an appointment for next Tuesday afternoon.' with member_id='M456'.

# Step 1

Coordinator LLM: {intent:'appointment', member_id:'M456', clarification_needed:false}

_coordinator_route returns 'appointment_agent'. Context prepended: [Member ID: M456, Member Name: Jane Smith].

# Step 2

ReAct 1: get_slots_for_range('next 5 days', time_of_day='afternoon')

Queries pre_auth – finds authorized provider 'Dr. Smith'. Filters Provider_Slot_2 for afternoon slots. Returns: Tuesday 6/17 at 2 PM and 3 PM, Wednesday 6/18 at 1 PM.

# Step 3

LLM presents options to caller

'I found afternoon availability for you next Tuesday at 2 PM and 3 PM, or Wednesday at 1 PM. Which would work best for you?'

# Step 4

ReAct 2: validate_appointment_slot('2026-06-17', '2 PM', 'Dr. Smith')

Returns: {available: true, slot_id: 'SLT-xyz'}.

# Step 5

ReAct 3: book_appointment(member_id='M456', date='2026-06-17', time='2 PM')

INSERTs Appointment record (ID: APTU1A2B3C). UPDATEs Provider_Slot_2.Is_Booked=1.

# Step 6

LLM confirms booking. MongoDB checkpoint saved. 200 OK.

'Your appointment with Dr. Smith is booked for Tuesday, 17 June 2026 at 2:00 PM. Appointment ID: APTU1A2B3C.'

{toc}
```

---

## 📄 SINGLE PAGE: API Reference

```
h1. API Reference

h2. Endpoint

| Property | Value |
|----------|-------|
| Path | POST /workflows/call_workflow |
| Auth | Bearer token (Azure AD JWT) – validated by FastAPI dependency injection. |
| Content-Type | application/json |
| Idempotency | Not idempotent. Each POST creates a new graph invocation or continues an existing thread. |

h2. Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| question | string | Yes | The caller's utterance for this turn. |
| member_id | string | No | Pre-populated member ID from channel integration (CRM lookup). |
| thread_id | string | No | UUID of existing conversation thread. Null or absent = new conversation. |
| metadata | object | No | Arbitrary key-value pairs. Passed through to InvokeResponse.metadata. |

h2. Response Body

Returns InvokeResponse serialised as JSON. HTTP 200 on success.

{code:json}
{
  "answer": "Your claim #CL-9981 was approved on June 1, 2026 for $240.00.",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "intent": "claims",
  "clarification_needed": false,
  "clarification_question": null,
  "metadata": {}
}
{code}

h2. Error Handling

| Status | Meaning |
|--------|---------|
| 400 Bad Request | Missing required field 'question'. Response includes field-level validation error from Pydantic. |
| 401 Unauthorized | Invalid or expired Azure AD JWT. Re-authenticate and retry. |
| 422 Unprocessable | Request body schema violation (Pydantic validation failure on non-required fields). |
| 500 Internal Error | Unhandled exception in graph execution. Full stack trace logged to Application Insights. |
| 503 Unavailable | LangGraph or Azure OpenAI unavailable. Caller should retry with exponential backoff. |

{toc}
```

---

## 📑 SECTION PARENT PAGE: Infrastructure

```
h1. Infrastructure and Integrations

h2. Overview

The platform is built on Azure cloud services, providing enterprise-grade scalability, reliability, and security. This section covers the Azure services used, deployment architecture, and observability strategy.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [Azure Services|Azure Services]
* [LangFuse Observability|LangFuse Observability]
* [Environment Variables|Environment Variables]

---

h2. ☁️ Core Services

* *Azure OpenAI* — LLM inference for intent classification and agent reasoning
* *Azure SQL Database* — Member, claims, benefits, and appointment data
* *Azure AI Search* — Semantic search over plan benefits documents
* *MongoDB Atlas* — Durable checkpoint storage for multi-turn state
* *Azure Kubernetes Service* — Container orchestration with auto-scaling
* *Azure API Management* — API gateway with JWT validation and rate limiting
* *Azure Monitor* — Structured logging and custom metrics

{toc}
```

---

## 📄 CHILD PAGE: Azure Services

```
h1. Azure Services

| Service | SKU/Variant | Usage |
|---------|-------------|-------|
| Azure OpenAI | GPT-5.4-mini | All LLM calls – coordinator, ClaimsAgent, BenefitsAgent, AppointmentSchedulerAgent, GeneralResponder. |
| Azure SQL Database | SQL Server | Member, Claims_Professional, Claims_Institutional, pre_auth, Provider_Slot_2, Appointment tables. Accessed via pyodbc. |
| Azure AI Search | Semantic + Keyword | Plan benefits corpus. Filtered by plan_id. Top-k chunks with relevance scores. |
| Azure Kubernetes Service | AKS | Container orchestration for FastAPI pods. HPA configured for CPU and request-rate metrics. |
| Azure API Management | APIM | Unified API gateway. JWT validation, rate limiting, throttling, and request logging. |
| Azure Monitor | Log Analytics + App Insights | Structured logging, custom metrics, intent distribution, and HITL rate tracking. |
| MongoDB Atlas | MongoDB 7.x | LangGraph checkpoint storage. Collections: langgraph_checkpoints, langgraph_checkpoint_writes. |

{toc}
```

---

## 📄 CHILD PAGE: LangFuse Observability

```
h1. LangFuse Observability (Optional)

LangFuse provides LLM-native observability: per-call trace spans with token usage, latency, model parameters, and cost. It is enabled via the LANGFUSE_ENABLED environment variable. When active, each graph invocation creates a root trace; coordinator and agent nodes create child spans. Traces are queryable by thread_id, intent, and member_id.

{toc}
```

---

## 📄 CHILD PAGE: Environment Variables

```
h1. Environment Variables

| Variable | Description |
|----------|-------------|
| AZURE_OPENAI_ENDPOINT | Azure OpenAI resource endpoint URL. |
| OPENAI_API_KEY | Azure OpenAI API key. |
| AZURE_SQL_CONNECTION_STRING | pyodbc connection string for Azure SQL. |
| AZURE_SEARCH_ENDPOINT | Azure AI Search service endpoint URL. |
| AZURE_SEARCH_KEY | Azure AI Search admin or query key. |
| AZURE_SEARCH_INDEX_NAME | Name of the benefits document search index. |
| MONGODB_URL | MongoDB connection string (Atlas or self-hosted). |
| LANGFUSE_ENABLED | Boolean flag (true/false). Enables LangFuse tracing when true. |
| LANGFUSE_PUBLIC_KEY | LangFuse project public key (required when LANGFUSE_ENABLED=true). |
| LANGFUSE_SECRET_KEY | LangFuse project secret key (required when LANGFUSE_ENABLED=true). |

{toc}
```

---

[Continues with Security & Compliance, Deployment, Observability, Data Flow, Design Decisions, Glossary, Roadmap, and Future Evolution sections...]
```
