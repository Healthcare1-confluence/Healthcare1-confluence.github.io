# Glossary

## Platform Components

| Term | Definition |
|------|-----------|
| **AppointmentSchedulerAgent** | Specialist agent for appointment lifecycle management using LangChain ReAct with eight tools (booking, rescheduling, cancellation). |
| **BenefitsAgent** | Specialist agent for plan coverage and benefit enquiries. Uses Azure SQL and Azure AI Search. |
| **CallWorkflow** | Python orchestrator class that compiles the LangGraph StateGraph and delegates to it. Handles checkpoint restoration. |
| **CallWorkflowState** | Single Pydantic TypedDict carrying all conversation state (messages, identifiers, intent, clarification flag) through the graph nodes. |
| **CheckPointer** | LangGraph component that serialises and persists CallWorkflowState between graph invocations. |
| **ClaimsAgent** | Specialist agent for claim status and denial reason queries. Queries Azure SQL. |
| **CompiledGraph** | Result of `graph.compile(checkpointer)`. Frozen, executable graph instance cached as singleton. |
| **Coordinator** | First LangGraph node. Classifies intent, extracts identifiers, routes to specialist agent or HITL gate. |
| **CoordinatorOutput** | Pydantic model defining structured JSON schema for coordinator LLM call response. |
| **GeneralResponder** | Lightweight handler for general intent (greetings, miscellaneous). Single LLM call, no tool use. |
| **HITL** | Human-in-the-Loop. Graph pauses to request missing information from caller (e.g., Member ID). |
| **InvokeResponse** | Structured API response returned by CallWorkflow.invoke() after graph completion. Includes answer, thread_id, intent. |

## Technologies

| Term | Definition |
|------|-----------|
| **Azure AI Search** | Microsoft's managed search service. Indexes benefit documents, supports hybrid keyword + semantic search. |
| **Azure OpenAI** | Microsoft's hosted OpenAI models. Used for coordinator, agent, and synthesis LLM calls. |
| **Azure SQL** | Managed SQL Server database. Stores member, claims, appointments, pre-auth data. |
| **Checkpointing** | Process of serialising and persisting graph state for durability and resumption. |
| **LangChain** | Python framework for building LLM applications. Provides agents, tools, memory, chains. |
| **LangFuse** | LLM observability platform. Tracks token usage, latency, cost per trace. |
| **LangGraph** | Open-source framework for stateful, multi-actor LLM applications as directed graphs. |
| **MemorySaver** | LangGraph in-memory checkpointer. Fallback when MongoDB unavailable. No durability. |
| **MongoDB Atlas** | Managed MongoDB cloud database. Stores CallWorkflowState checkpoints. |
| **MongoDBSaver** | LangGraph-compatible MongoDB checkpointer. Stores state in `langgraph_checkpoints` collection. |
| **pyodbc** | Python library for ODBC database connectivity. Used to query Azure SQL. |
| **ReAct** | Reasoning + Acting. LangChain agent pattern where LLM alternates between reasoning steps and tool calls. |
| **StateGraph** | LangGraph class defining nodes and conditional edges. Compiled into CompiledGraph. |

## Healthcare Terms

| Term | Definition |
|------|-----------|
| **Claim** | Request for payment from healthcare provider. Includes claim ID, status (approved/denied/pending), amount. |
| **HIPAA** | Health Insurance Portability and Accountability Act. US regulation on healthcare data privacy and security. |
| **Member ID** | Unique identifier for an insured person. Required to access claims and benefits. |
| **PHI** | Protected Health Information. Any data that could identify a patient. HIPAA-regulated. |
| **Plan** | Insurance plan type (PPO, HMO, etc.). Determines coverage rules, benefits, pre-auth requirements. |
| **Pre-Authorization** | Approval requirement before member can book certain appointment types. Enforced by appointment agent. |
| **Provider** | Healthcare provider (doctor, hospital, clinic). Must be pre-authorized for appointment booking. |
| **Tier-1 Support** | First-level customer service. High volume, routine inquiries. Target for automation. |

## Data Schema

| Term | Definition |
|------|-----------|
| **Appointment Table** | Azure SQL table storing booked member appointments (ID, Member_ID, Status, booking_timestamp). |
| **Claims Table** | Azure SQL tables (Claims_Professional, Claims_Institutional) storing claim records (claim_id, member_id, status, amount, denial_reason). |
| **Member Table** | Azure SQL table storing member demographics (Member_ID, Name, Plan_ID, DOB). |
| **pre_auth Table** | Azure SQL table storing pre-authorization constraints (Member_ID, Provider_Name, Status, approval_date). |
| **Provider_Slot_2** | Azure SQL table storing available appointment slots (Slot_ID, Provider_Name, Date, Start_Time, Is_Booked). |

## Process Terms

| Term | Definition |
|------|-----------|
| **Checkpoint** | Serialised snapshot of CallWorkflowState persisted to MongoDB. Used to resume conversations. |
| **Compilation** | Process of building the LangGraph StateGraph from node and edge definitions. Expensive one-time cost. |
| **Intent** | Classified type of caller request: claims, benefits, appointment, general, or default. |
| **ReAct Loop** | Iterative process where LLM selects a tool, executes it, inspects the result, and repeats until satisfied. |
| **Safety Net** | Python validation that overrides LLM output in edge cases (e.g., forcing clarification if member_id missing). |
| **Thread ID** | UUID identifying a single conversation session. LangGraph config key for checkpoint selection. |
| **Tool** | Callable function available to agents (e.g., query_claims, get_available_slots). Each agent has domain-specific tools. |

## Metrics

| Term | Definition |
|------|-----------|
| **Handle Time** | Time to resolve a caller's query from start to finish. Target: 30s for appointments, <5s for others. |
| **HITL Rate** | Percentage of calls requiring human-in-the-loop clarification. Target: ≤15%. |
| **Intent Accuracy** | Percentage of intents correctly classified. Target: ≥95%. |
| **MTTR** | Mean Time To Resolution. Average time to resolve member queries. Goal: reduce via automation. |
| **P95 Latency** | 95th percentile response time. Target: 3s general, 5s specialist agents. |
| **Token Usage** | Total tokens (input + output) consumed by LLM calls. Tracked per intent for cost analysis. |

