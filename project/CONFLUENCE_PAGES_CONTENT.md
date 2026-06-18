# Confluence Pages - Ready to Paste

## 📄 PARENT PAGE: Healthcare AI Contact Center Platform

```
h1. Healthcare AI Contact Center Platform

*Solution & Technical Design Document — Agentic Call Workflow Engine — LangGraph + Azure*

Version 1.0 | 2026

---

h2. Welcome

Healthcare contact centres handle millions of calls annually covering claims status, benefits enquiries, appointment scheduling, member account updates, and general assistance. Manual handling is expensive, error-prone, and creates compliance risk.

This platform provides an intelligent, agentic approach to healthcare contact automation using LangGraph, Azure OpenAI, and MongoDB.

---

h2. 📚 Documentation Overview

{page-tree:root=@self}

---

h2. 🗺️ Quick Navigation

* [Business Context|Business Context] — Industry challenges and platform goals
* [Architecture|Architecture] — System design and technology stack
* [Workflow|Workflow] — End-to-end call processing pipeline
* [Component Design|Component Design] — Specialist agents and tools
* [State Schema Design|State Schema Design] — Multi-turn conversation state
* [Human-in-the-Loop|Human-in-the-Loop] — HITL safety gates and clarification
* [Infrastructure|Infrastructure] — Azure services and deployment
* [Security & Compliance|Security & Compliance] — HIPAA alignment and security
* [API Reference|API Reference] — Endpoint specifications and examples
* [Deployment|Deployment] — Kubernetes deployment design
* [Design Decisions|Design Decisions] — Architectural trade-offs
* [Roadmap|Roadmap] — Future enhancements and timeline
* [Glossary|Glossary] — Technical terminology reference

---

h2. 🎯 Key Features

* *Intent Classification* — Accurate routing to specialist agents (claims, benefits, appointment, general)
* *Multi-Turn Conversations* — Durable MongoDB checkpointing for seamless HITL workflows
* *Specialist Agents* — ReAct agents with real-time access to Azure SQL, AI Search, and scheduling systems
* *HIPAA Compliance* — Built-in PHI masking, parameterised queries, and audit logging
* *Pre-Auth Enforcement* — Appointment bookings respect insurance pre-authorization constraints
* *60-70% Automation* — Designed to eliminate human agent involvement for routine Tier-1 calls

---

h2. 📊 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| LLM | Azure OpenAI (GPT-5.4-mini) | Intent classification & agent reasoning |
| Orchestration | LangGraph (Python) | Stateful multi-agent graph engine |
| Persistence | MongoDB Atlas | Thread-based checkpoint storage |
| Data Access | Azure SQL, Azure AI Search | Member records, claims, benefits, appointments |
| Deployment | Azure Kubernetes Service (AKS) | Container orchestration & auto-scaling |
| Observability | Azure Monitor, LangFuse | Logging, metrics, and LLM tracing |

---

h2. ✅ Use This Documentation To:

* Understand the system architecture and design decisions
* Integrate with the FastAPI call workflow service
* Extend the platform with new intent types or agents
* Deploy to production on Kubernetes
* Troubleshoot multi-turn conversation flows
* Ensure HIPAA compliance during integration

---

{toc}
```

---

## 📑 SECTION PARENT PAGE: Business Context

```
h1. Business Context

h2. Overview

The healthcare contact centre industry faces significant operational and compliance challenges. This section covers the business drivers, problem statement, design inputs, and platform goals that shape the Healthcare AI Contact Center Platform.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [Industry Challenges and Business Impact|Industry Challenges and Business Impact]
* [Client Context – Problem Statement|Client Context – Problem Statement]
* [Design Inputs|Design Inputs]
* [Constraints|Constraints]
* [Platform Goals|Platform Goals]
* [Solution Direction|Solution Direction]

---

h2. 📌 Key Takeaways

* Healthcare contact centres handle millions of calls annually across claims, benefits, and appointments
* Manual handling is expensive, error-prone, and creates compliance risk
* HIPAA compliance must be maintained across every interaction
* 60–70% of Tier-1 calls can be fully automated using intelligent agents
* Multi-turn conversation state must be durable across HTTP requests

{toc}
```

---

## 📄 CHILD PAGE: Industry Challenges and Business Impact

```
h1. Industry Challenges and Business Impact

h2. Industry Challenges

Healthcare contact centres handle millions of calls annually covering claims status, benefits enquiries, appointment scheduling, member account updates, and general assistance. Manual handling is expensive, error-prone, and creates compliance risk.

Common challenges include:

* Long Mean Time To Resolution (MTTR) for member queries
* Limited visibility across intent classification boundaries
* Difficulty correlating member requests with accurate backend data
* Dependency on senior agents and tribal knowledge for complex cases
* High operational costs associated with Tier-1 and Tier-2 interactions

These challenges impact healthcare payers, providers, and members across:

* Health Insurance and Managed Care
* Hospital Systems and Provider Networks
* Pharmacy Benefit Management
* Medicare and Medicaid Programmes
* Employer-Sponsored Health Plans

---

h2. Business Impact of Production Failures

Industry studies consistently show that unautomated or poorly automated contact centre interactions result in significant operational and financial costs.

| Impact Area | Typical Business Impact |
|-------------|------------------------|
| Manual claim lookups | Increased agent handle time and cost-per-call |
| Missed appointment bookings | Provider revenue loss and patient dissatisfaction |
| Benefits misquotation | Member complaints, rework, and compliance risk |
| Escalations to senior agents | Higher operational costs and longer resolution times |
| HIPAA non-compliance | Regulatory penalties and reputational damage |

Automating Tier-1 and Tier-2 interactions directly reduces cost-per-contact, improves first-call resolution rates, and ensures consistent HIPAA-compliant handling of Protected Health Information (PHI).

{toc}
```

---

## 📄 CHILD PAGE: Client Context – Problem Statement

```
h1. Client Context – Problem Statement

A healthcare contact centre team handles thousands of daily calls across claims, benefits, and appointment management. Members call with specific questions but agents must navigate multiple disconnected systems – a claims portal, a benefits document repository, an EHR scheduling system – to answer them.

The process becomes time-consuming because:

* No unified AI layer exists to classify intent and route to the correct backend.
* Multi-turn conversations lose context across HTTP requests.
* Appointment scheduling requires checking pre-authorization before booking.
* HIPAA compliance must be maintained across every interaction without exception.

In such scenarios, handling quality depends on individual agent knowledge, making it difficult to consistently and quickly serve members at scale.

{toc}
```

---

## 📄 CHILD PAGE: Design Inputs

```
h1. Design Inputs

The following realities of healthcare contact centre operations define the design inputs for this platform:

| System Characteristics | Operational Realities | Platform Considerations |
|------------------------|----------------------|------------------------|
| Multiple intent domains across a single conversation | Intent routing is manual and agent-driven | Automated LLM-based intent classification required |
| Backend data spread across SQL, search, and EHR | No unified data access layer | Agent-specific tool sets per intent domain |
| HIPAA-regulated member data in every interaction | PHI exposure risk in logs and LLM prompts | PHI masking and parameterised queries mandatory |
| Multi-turn conversations common for complex queries | Context is lost between calls | Durable MongoDB checkpointing required |

{toc}
```

---

## 📄 CHILD PAGE: Constraints

```
h1. Constraints

The system must operate within the following constraints:

* Handle concurrent calls across claims, benefits, appointment, and general intents.
* Never invoke a specialist agent without required member identifiers being present or requested.
* Not rely on manual intervention during live call processing.
* Maintain HIPAA compliance in all LLM prompts, logs, and stored checkpoints.
* Produce responses readable by TTS engines – no markdown, no formatting symbols.
* Complete responses within 3 seconds P95 for general intent; under 5 seconds for specialist agents.

{toc}
```

---

## 📄 CHILD PAGE: Platform Goals

```
h1. Platform Goals

The platform provides a structured and intelligent approach to healthcare contact automation with the following objectives:

* Automate 60–70% of Tier-1 calls with zero human agent involvement.
* Classify caller intent accurately on every turn using Azure OpenAI.
* Enforce Human-in-the-Loop (HITL) gates to ensure no member is mis-served due to missing data.
* Preserve multi-turn conversation state durably across HTTP requests using MongoDB.
* Support appointment lifecycle management with pre-authorization enforcement.
* Deliver HIPAA-aligned PHI handling across every system boundary.

With this context in place, the next step is to understand how the system approaches solving it.

{toc}
```

---

## 📄 CHILD PAGE: Solution Direction

```
h1. Solution Direction

To achieve these goals, the platform is designed to:

* Classify the caller's intent on every turn using a structured LLM call.
* Enrich state with member identifiers extracted from the conversation.
* Route to specialist agents that combine tool use and LLM reasoning.
* Use this combined understanding to deliver plain-English answers via TTS.

This approach transitions healthcare contact handling from a manual, agent-driven activity to a system-assisted, intelligence-driven process.

{toc}
```

---

## 📑 SECTION PARENT PAGE: Architecture

```
h1. Architecture

h2. Overview

The platform follows a layered, agentic architecture pattern. An inbound HTTP request from the voice/channel integration layer hits the FastAPI service, which delegates to the LangGraph orchestrator. The graph routes through the coordinator and selected specialist agent, then returns a structured response.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [Solution Options|Solution Options]
* [Competitive Differentiation|Competitive Differentiation]
* [Output Benchmarks|Output Benchmarks]
* [High-Level Architecture|High-Level Architecture]
* [High-Level Platform Workflow|High-Level Platform Workflow]
* [Runtime Architecture|Runtime Architecture]
* [Graph Nodes|Graph Nodes]
* [Graph Edges|Graph Edges]
* [Graph Compilation and Startup|Graph Compilation and Startup]

---

h2. 🔑 Core Concepts

* *Coordinator Node* — Classifies intent and enforces HITL safety gates
* *Specialist Agents* — ReAct agents with domain-specific tool sets (Claims, Benefits, Appointments)
* *State Management* — Single CallWorkflowState object flows through all nodes
* *Tool Use* — Agents query Azure SQL, AI Search, and EHR systems in real-time
* *Durable Checkpointing* — MongoDB preserves multi-turn conversation state

{toc}
```

---

## 📄 CHILD PAGE: Solution Options

```
h1. Solution Options

Multiple approaches were evaluated for automating healthcare contact centre interactions.

h2. Rule-Based IVR Systems

These rely on fixed decision trees and touch-tone menus, making them unsuitable for natural language queries and multi-intent conversations.

h2. Single LLM Chatbots

While flexible, they lack structured tool use, do not enforce HITL safety nets, and cannot maintain durable multi-turn state.

h2. Monitoring and Observability Platforms

These provide call analytics but do not reason over backend data or classify healthcare-specific intents.

h2. Agentic Multi-Agent Architecture (Recommended)

* Combines structured intent classification with specialist agent tool use.
* Bridges the gap between natural language and backend data systems.
* Best fit for multi-intent, multi-turn, HIPAA-compliant healthcare automation.

{toc}
```

---

## 📄 CHILD PAGE: Competitive Differentiation

```
h1. How This Solution Differs from Existing Market Options

The healthcare AI contact centre market includes a range of offerings – from generic large-language-model chatbots to legacy interactive voice response systems and call analytics dashboards. While each addresses a narrow slice of the problem, none combines healthcare-domain intelligence, durable multi-turn state, live backend integration, and built-in compliance enforcement in a single cohesive platform. The table below maps the five most meaningful differentiators across solution categories.

| Differentiator | Rule-Based IVR | Generic LLM Chatbot | Analytics / Observability Platform | This Platform |
|---|---|---|---|---|
| *Healthcare-Domain Specificity* | Scripted responses only; no HIPAA enforcement by design | General-purpose; PHI handling and pre-auth logic must be custom-built and maintained separately | Reads call data; does not act on it or enforce compliance | HIPAA-aligned PHI masking, parameterised queries, and pre-authorisation enforcement built into every agent and tool |
| *Multi-Agent Orchestration* | Single decision tree; no agent composition | Single LLM call per turn; no structured routing to specialist logic | Not applicable – passive observation only | LangGraph StateGraph with coordinator node routing to dedicated specialist agents (Claims, Benefits, Appointment, General) per classified intent |
| *Durable Multi-Turn State* | Stateless between DTMF inputs; no conversation memory | Typically session-scoped; state lost on disconnect or timeout | Stores transcripts but does not carry live state across turns | MongoDB checkpointing persists full CallWorkflowState across HTTP requests, enabling seamless multi-turn resumption and audit replay |
| *Live Backend Integration via Tool Use* | Reads from a single static script; no real-time data access | RAG retrieval from static documents; no transactional write capability | Read-only analytics on historical data | ReAct agents invoke typed tools against Azure SQL (claims, appointments), Azure AI Search (benefits), and EHR systems in real time – including transactional writes such as booking and cancellation |
| *Human-in-the-Loop (HITL) Safety Gates* | Escalates on unrecognised input only; no structured safety net | HITL, if present, is a post-hoc add-on requiring custom prompt engineering per use case | Flags calls after the fact; cannot intervene during live handling | HITL is a first-class graph node: the coordinator pauses execution and requests missing identifiers before any specialist agent is invoked, preventing member mis-service by design |

h2. Healthcare-Domain Specificity

Generic AI platforms require extensive custom development to handle healthcare-specific requirements such as PHI masking, pre-authorisation enforcement, and HIPAA-compliant audit logging. This platform encodes those requirements directly into its agent prompts, tool implementations, and state schema – meaning compliance is structural, not a layer applied after the fact. Every LLM prompt is designed to avoid logging raw member data, and every SQL tool uses parameterised queries to prevent injection and inadvertent PHI exposure.

h2. Orchestrated Multi-Agent Reasoning vs. Single-Model Approaches

Single LLM chatbots handle all intents within one prompt context, which degrades accuracy as conversation complexity grows and makes it difficult to enforce intent-specific data access boundaries. This platform separates concerns explicitly: the coordinator performs one focused structured classification call, and each specialist agent operates within a scoped tool set appropriate to its domain. This means a benefits query never has access to appointment booking tools, and vice versa – reducing both error surface and compliance risk.

h2. Transactional Tool Use vs. Retrieval-Only Architectures

Most RAG-based healthcare bots retrieve content from static benefit documents and surface it as text. This platform goes further: specialist agents read *and write* to live backend systems. The AppointmentSchedulerAgent, for example, validates pre-authorisation, checks real-time slot availability, atomically books the appointment, and updates the provider slot record – all within a single ReAct agent loop. This closes the loop between natural language and operational outcome without requiring a human agent to execute the backend steps.

{toc}
```

---

## 📄 CHILD PAGE: Output Benchmarks

```
h1. Output Benchmarks

The following benchmarks define the measurable performance envelope the platform is designed to operate within. Metrics are classified as *Target* (design goal, to be validated post-deployment) or *Measured* (empirically confirmed). Formal instrumentation for all metrics is planned via LangFuse dashboards as part of the near-term roadmap.

| Metric | Benchmark | Status | Source / Rationale |
|--------|-----------|--------|-------------------|
| *Response Latency – General Intent* | P95 ≤ 3 seconds end-to-end | Target | Defined in system constraints. General intent requires a single coordinator LLM call with no specialist agent invocation. |
| *Response Latency – Specialist Agents* | P95 ≤ 5 seconds end-to-end | Target | Defined in system constraints. Includes coordinator classification, ReAct agent tool calls against Azure SQL / Azure AI Search, and TTS-ready response assembly. |
| *Tier-1 Call Automation Rate* | 60–70% of inbound Tier-1 calls fully automated with zero human agent involvement | Target | Platform goal. Covers claims status, benefit lookups, and standard appointment booking scenarios that do not require clinical judgement or exception handling. |
| *Intent Classification Accuracy* | ≥ 95% correct intent classification across claims, benefits, appointment, and general intents | Target | Derived from coordinator design using structured JSON output via Azure OpenAI. To be validated against a labelled call transcript evaluation set via LangFuse prompt versioning. |
| *Appointment Booking Handle Time* | ≤ 30 seconds for standard pre-authorised booking scenarios | Target | Referenced in the Example Appointment Booking Flow. Compared against a baseline of several minutes for manual agent-driven cross-system booking. |
| *HITL Escalation Rate* | ≤ 15% of calls requiring human-in-the-loop intervention for missing identifiers or unresolvable intents | Target | HITL is a safety net, not a routine path. Escalation rate above 20% would indicate degraded member experience or upstream identifier-injection failures from the channel layer. |
| *Cost per Query* | To be baselined post-deployment | Target | LangFuse token-usage tracing per intent will enable cost-per-query reporting. Coordinator uses gpt-4o-mini to minimise cost on high-frequency classification calls. |
| *LangGraph Graph Compilation Overhead* | One-time cost on first request; ≤ 0 ms on all subsequent requests (singleton cache) | Target | Lazy compilation with singleton CompiledGraph cache eliminates per-request assembly cost. Cold-start compilation is borne once per service instance lifecycle. |
| *State Checkpoint Restore Latency* | ≤ 50 ms for MongoDB checkpoint retrieval on returning calls | Target | MongoDB langgraph_checkpoints collection indexed on thread_id. In-memory MemorySaver fallback used when MongoDB is unavailable, with sub-millisecond restore. |

h2. Benchmark Monitoring Strategy

Once deployed, all latency, accuracy, and cost benchmarks will be tracked through LangFuse distributed traces. Each graph invocation emits a trace covering the coordinator LLM call, any specialist agent ReAct loop iterations, individual tool call durations, and the final response assembly step. Per-intent dashboards will surface HITL rate trends over time, allowing the team to tune intent prompts and HITL thresholds based on real traffic patterns rather than design assumptions.

Prompt versioning via LangFuse will support A/B evaluation of INTENT_PROMPT and GENERAL_PROMPT variants, enabling data-driven improvement of classification accuracy without requiring full redeployment cycles. Cost-per-query reporting will be broken down by intent domain to identify optimisation opportunities – for example, replacing the coordinator model with a fine-tuned smaller model once sufficient training data is available, as noted in the long-term roadmap.

{toc}
```

---

## 📄 CHILD PAGE: High-Level Architecture

```
h1. High-Level Architecture

The platform follows a layered architecture pattern. An inbound HTTP request from the voice/channel integration layer hits the FastAPI service, which delegates to the CallWorkflow orchestrator. CallWorkflow compiles and caches the LangGraph StateGraph, then invokes it with the caller's question and context. The graph routes through the coordinator and selected specialist agent, then returns a structured InvokeResponse to the API caller.

{toc}
```

---

## 📄 CHILD PAGE: High-Level Platform Workflow

```
h1. High-Level Platform Workflow

The platform processes inbound calls through a structured, multi-layer architecture:

*Layer 1: Channel & Ingestion* — Inbound voice calls from Twilio or Azure Communication Services. STT transcription, JWT auth via APIM, member_id injection, thread_id routing.

*Layer 2 & 3: FastAPI + LangGraph* — CallWorkflow orchestrator with lazy graph compilation, singleton CompiledGraph cache, checkpoint restore, and coordinator routing.

*Layer 4: Coordinator + HITL Gate* — Intent classification via Azure OpenAI LLM. HITL safety net checks for clarification_needed. Agent router dispatches to claims / benefits / appointment / general responder.

*Layer 5: Multi-Agent Reasoning* — ReAct loops with specialist agents: Claims Agent, Benefits Agent, Appointment Agent, General Responder. Tool use with pyodbc and AI Search.

*Layer 6: Unified State & Knowledge Storage* — MongoDB Atlas (CallWorkflowState checkpoints), Azure SQL (member, claims, appointment data), Azure AI Search (plan benefits), thread_id checkpoints, LangFuse traces.

*Layer 7: Actionable Member Response* — Claim status & denial reason, benefits coverage detail, appointment booking ID, HITL clarification question, HIPAA-compliant TTS output.

{toc}
```

---

## 📄 CHILD PAGE: Runtime Architecture

```
h1. Runtime Architecture

The platform is organised into three logical tiers:

*Tier 0 – Orchestration Agents* — Azure OpenAI GPT-5.4-mini orchestration only. IntentClassifier (fast + cheap, called once per query), Coordinator (reasoning, agent dispatch), HITLGuard (safety check, clarification_needed), ReflectionGuard (max 200 tokens, PHI check, strip_markdown).

*Tier 1 – Primary Agents* — Azure OpenAI GPT-5.4-mini multi-turn ReAct loop (max 5 tool calls). ClaimsAgent (why denied? + RiskAgent parallel), BenefitsAgent (what's covered? sequential, SQL + AI Search), AppointmentAgent (book / reschedule, pre-auth enforced, sequential), GeneralAgent (greetings / misc, single LLM call, no tools), CausalityAgent (denial chain – FixAgent, sequential).

*Tier 2 – Sub-agents* — Azure OpenAI GPT-5.4-mini single tool call, no loop.

Spawned by ClaimsAgent: MemberLookupSubAgent (query_member_info, validates member existence), ClaimsQuerySubAgent (query_claims tool, professional + institutional), PreAuthSubAgent (query_preauth tool, approval status lookup).

Spawned by BenefitsAgent: PlanResolverSubAgent (get_member_plan_id, resolves plan_id from SQL), BenefitsSearchSubAgent (search_plan_benefits, Azure AI Search, top-5 chunks).

Spawned by AppointmentAgent: SlotFinderSubAgent (get_available_slots, get_slots_for_range), BookingSubAgent (validate + book_appointment, atomic SQL write), RescheduleSubAgent (reschedule / cancel, slot release + rebook), AppointmentFetchSubAgent (get_member_appointments, upcoming schedule lookup).

{toc}
```

---

## 📄 CHILD PAGE: Graph Nodes

```
h1. Graph Nodes

The graph topology is a one-shot decision tree: every invocation enters at __start__, passes through the coordinator, and terminates at __end__. There are no cycles except the internal ReAct tool-use loop inside specialist agent sub-graphs.

| Node | Type | Responsibility |
|------|------|-----------------|
| __start__ | Virtual | LangGraph entry point. Injects initial CallWorkflowState. |
| coordinator | Custom Node | Classifies intent via LLM. Extracts member_id, plan_id, date_of_service. Sets clarification_needed flag. |
| claims_agent | Agent Node | Invokes ClaimsAgent.ainvoke(). Executes ReAct loop with query_member_info, query_claims, query_preauth tools against Azure SQL. |
| benefits_agent | Agent Node | Invokes BenefitsAgent.ainvoke(). Executes ReAct loop with get_member_plan_id (Azure SQL) and search_plan_benefits (Azure AI Search). |
| appointment_agent | Agent Node | Invokes AppointmentSchedulerAgent.ainvoke(). Executes ReAct loop with 8 tools against Azure SQL (Provider_Slot_2, Appointment, pre_auth tables). |
| general_responder | Custom Node | Single LLM call with GENERAL_PROMPT system message. Returns 1-2 sentence plain-English reply. |
| __end__ | Virtual | LangGraph terminal node. Graph suspends here and returns final state to CallWorkflow.invoke(). |

{toc}
```

---

## 📄 CHILD PAGE: Graph Edges

```
h1. Graph Edges

| Edge | Condition |
|------|-----------|
| START → coordinator | Unconditional. Every invocation enters coordinator first. |
| coordinator → claims_agent | Conditional. Fires when intent = 'claims' AND clarification_needed = false. |
| coordinator → benefits_agent | Conditional. Fires when intent = 'benefits' AND clarification_needed = false. |
| coordinator → appointment_agent | Conditional. Fires when intent = 'appointment' AND clarification_needed = false. |
| coordinator → general_responder | Conditional. Fires when intent = 'general' or 'default' AND clarification_needed = false. |
| coordinator → __end__ | Conditional. Fires when clarification_needed = true. Graph terminates early; clarification question returned to caller. |
| claims_agent → __end__ | Unconditional. Agent completes and graph terminates. |
| benefits_agent → __end__ | Unconditional. Agent completes and graph terminates. |
| appointment_agent → __end__ | Unconditional. Agent completes and graph terminates. |
| general_responder → __end__ | Unconditional. Responder completes and graph terminates. |

{toc}
```

---

## 📄 CHILD PAGE: Graph Compilation and Startup

```
h1. Graph Compilation and Startup

Graph compilation is an expensive one-time operation. CallWorkflow implements a lazy singleton pattern: the first call to compile() performs full graph assembly; subsequent calls return the cached _compiled_graph instance.

* FastAPI startup fires – calls CallWorkflow.compile().
* CallWorkflow checks _compiled_graph; if already compiled, returns immediately (fast path).
* On first compile: _get_checkpointer() initialises the persistence backend.
* MongoClient is created with MONGODB_URL and a 5-second connection timeout.
* If connection succeeds: MongoDBSaver is instantiated targeting directline_db database.
* If connection times out: MemorySaver is used as in-process fallback.
* Five nodes added: coordinator, claims_agent, benefits_agent, appointment_agent, general_responder.
* graph.compile(checkpointer=checkpointer) produces the CompiledGraph.
* CompiledGraph cached to _compiled_graph and returned to FastAPI startup.

{toc}
```

---

## 📑 SECTION PARENT PAGE: Workflow

```
h1. Workflow

h2. Overview

The platform processes every inbound call through a seven-step pipeline – from channel ingestion through intent classification, specialist agent tool use, data retrieval, LLM synthesis, and durable checkpoint persistence – before delivering a plain-English TTS response to the caller.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [End-to-End Workflow Diagram|End-to-End Workflow Diagram]
* [Step 1 – Inbound Call|Step 1 – Inbound Call]
* [Step 2 – FastAPI + CallWorkflow|Step 2 – FastAPI + CallWorkflow]
* [Step 3 – Coordinator Node|Step 3 – Coordinator Node]
* [Step 4 – Specialist Agent Routing|Step 4 – Specialist Agent Routing]
* [Step 5 – Data Layer|Step 5 – Data Layer]
* [Step 6 – LLM Synthesis|Step 6 – LLM Synthesis]
* [Step 7 – TTS Response|Step 7 – TTS Response]

---

h2. 📊 Performance Targets

* General Intent: P95 ≤ 3 seconds
* Specialist Agents: P95 ≤ 5 seconds
* HITL Escalation: ≤ 15% of calls

{toc}
```

---

## 📄 CHILD PAGE: End-to-End Workflow Diagram

```
h1. End-to-End Workflow Diagram

The platform processes every inbound call through a seven-step pipeline – from channel ingestion through intent classification, specialist agent tool use, data retrieval, LLM synthesis, and durable checkpoint persistence – before delivering a plain-English TTS response to the caller.

{note}
The visual diagram is embedded in the HTML documentation. This text-based description captures the workflow steps and data flow.
{note}

*Seven-step workflow from inbound call through intent classification, specialist agents, data retrieval, HITL gate, MongoDB persistence, and TTS response delivery.*

{toc}
```

---

## 📄 CHILD PAGE: Step 1 – Inbound Call

```
h1. Step 1 – Inbound Call

Every interaction begins when a member call arrives via Twilio or Azure Communication Services. The channel layer converts the audio stream to text and forwards the utterance to the FastAPI endpoint as a structured JSON payload.

{toc}
```

---

## 📄 CHILD PAGE: Step 2 – FastAPI + CallWorkflow

```
h1. Step 2 – FastAPI + CallWorkflow

The FastAPI service validates the JWT and delegates to the CallWorkflow orchestrator. On the first request, the LangGraph StateGraph is compiled and cached. If a thread_id is provided, the prior checkpoint is restored from MongoDB Atlas before any node executes.

{toc}
```

---

## 📄 CHILD PAGE: Step 3 – Coordinator Node

```
h1. Step 3 – Coordinator Node

A single structured Azure OpenAI call classifies the caller's intent and extracts identifiers (member_id, plan_id, date_of_service). A Python safety net then inspects the result – if intent is claims and member_id is absent, clarification_needed is forced to true regardless of LLM output, triggering the HITL gate.

{toc}
```

---

## 📄 CHILD PAGE: Step 4 – Specialist Agent Routing

```
h1. Step 4 – Specialist Agent Routing

The coordinator routes to one of four paths based on classified intent:

* *Claims agent* – ReAct loop against Azure SQL (Claims_Professional, Claims_Institutional, Member tables).
* *Benefits agent* – hybrid ReAct loop combining Azure SQL plan lookup with Azure AI Search semantic retrieval.
* *Appointment agent* – eight-tool ReAct loop against Provider_Slot_2, Appointment, and pre_auth tables.
* *General responder* – single LLM call, no tool use, lowest latency path.
* *HITL gate* – graph terminates early, clarification question returned to caller, full state checkpointed to MongoDB.

{toc}
```

---

## 📄 CHILD PAGE: Step 5 – Data Layer

```
h1. Step 5 – Data Layer

Each specialist agent issues parameterised queries to its designated backend. All Azure SQL access uses pyodbc wrapped in run_in_executor for async compatibility. Azure AI Search applies a plan_id filter on every search to prevent cross-plan data leakage.

{toc}
```

---

## 📄 CHILD PAGE: Step 6 – LLM Synthesis

```
h1. Step 6 – LLM Synthesis

Tool results are passed back to the agent's LLM, which synthesises a plain-English response. _strip_markdown() is applied to ensure TTS readability. The complete CallWorkflowState is then persisted to MongoDB Atlas under the caller's thread_id.

{toc}
```

---

## 📄 CHILD PAGE: Step 7 – TTS Response

```
h1. Step 7 – TTS Response

The InvokeResponse object is serialised to JSON and returned as HTTP 200 OK. The channel layer converts the answer field to speech via the TTS engine. The thread_id is passed back to the caller for use in subsequent turns.

{toc}
```

---

## 📑 SECTION PARENT PAGE: Component Design

```
h1. Component Design

h2. Overview

The system comprises five major components:

* *Coordinator Node* — Single LLM call for intent classification and identifier extraction
* *Claims Agent* — ReAct agent with Azure SQL tool set for claim status queries
* *Benefits Agent* — Hybrid agent combining SQL plan lookups with semantic search
* *Appointment Agent* — Eight-tool ReAct agent for appointment lifecycle management
* *General Responder* — Single LLM call handler for greetings and miscellaneous intents

Each component is designed to be independently testable and deployable.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [Coordinator Node|Coordinator Node]
* [Claims Agent|Claims Agent]
* [Benefits Agent|Benefits Agent]
* [Appointment Scheduler Agent|Appointment Scheduler Agent]
* [General Responder|General Responder]

---

h2. 🔧 Key Design Patterns

* *ReAct Loop* — Agents alternate reasoning and tool calling
* *Tool Use* — Parameterised queries prevent SQL injection
* *Context Enrichment* — Extracted identifiers prepended to agent prompts
* *Output Sanitisation* — Markdown stripped for TTS readability

{toc}
```

---

[Content continues with Component Design child pages, State Schema, HITL, API Reference, Infrastructure, Security, Deployment, Observability, Data Flow, Design Decisions, Glossary, and Roadmap...]
```
