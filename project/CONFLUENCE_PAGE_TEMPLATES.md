# Confluence Page Templates - Ready to Paste

Copy and paste these templates into Confluence for each section. Replace `[content here]` with actual content from your markdown files.

---

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
* [State Management|State Management] — Multi-turn conversation persistence
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
* [Problem Statement|Problem Statement]
* [Design Inputs|Design Inputs]
* [Platform Goals|Platform Goals]

---

h2. 📌 Key Takeaways

* Healthcare contact centres handle millions of calls annually across claims, benefits, and appointments
* Manual handling costs $X per call and introduces error and compliance risk
* HIPAA compliance must be maintained across every interaction
* 60-70% of Tier-1 calls can be fully automated using intelligent agents
* Multi-turn conversation state must be durable across HTTP requests

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
* [High-Level Architecture|High-Level Architecture]
* [Runtime Architecture|Runtime Architecture]
* [Graph Design|Graph Design]

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

## 📑 SECTION PARENT PAGE: Workflow

```
h1. Workflow

h2. Overview

The platform processes every inbound call through a seven-step pipeline:

# Channel Ingestion
# FastAPI + LangGraph Compilation
# Intent Classification (Coordinator)
# Specialist Agent Routing
# Data Layer Queries
# LLM Synthesis
# TTS Response Delivery

Each step is designed to minimise latency, maximise accuracy, and ensure HIPAA compliance.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [End-to-End Workflow|End-to-End Workflow]
* [Step-by-Step Breakdown|Step-by-Step Breakdown]

---

h2. 📊 Performance Targets

* General Intent: P95 ≤ 3 seconds
* Specialist Agents: P95 ≤ 5 seconds
* HITL Escalation: ≤ 15% of calls

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
* [Appointment Scheduler|Appointment Scheduler]
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

## 📑 SECTION PARENT PAGE: State Management

```
h1. State Management

h2. Overview

All data flowing through the graph is carried in a single `CallWorkflowState` object. LangGraph merges partial state updates returned by each node into the running state object. No node receives anything except state — there are no side channels or global variables.

This design ensures:
* Complete traceability of data flow
* Easy checkpointing and resumption
* Strong typing and validation
* HIPAA-compliant audit trails

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [State Schema|State Schema]
* [Checkpointing|Checkpointing]

---

h2. 📋 State Lifecycle

# Initial state created with caller utterance
# Coordinator enriches with intent and identifiers
# Specialist agent adds tool results
# Final state saved to MongoDB
# Next turn restores checkpoint and resumes

{toc}
```

---

## 📑 SECTION PARENT PAGE: Human-in-the-Loop

```
h1. Human-in-the-Loop (HITL)

h2. Overview

HITL in this system refers to the pattern where the AI workflow pauses mid-execution to request additional information from the human caller. It is not a human agent takeover — it is a structured clarification request that allows the graph to resume with complete data on the next conversational turn.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [HITL Design|HITL Design]
* [Trigger Conditions|Trigger Conditions]

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

## 📑 SECTION PARENT PAGE: Infrastructure

```
h1. Infrastructure

h2. Overview

The platform is built on Azure cloud services, providing enterprise-grade scalability, reliability, and security. This section covers the Azure services used, deployment architecture, and observability strategy.

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [Azure Services|Azure Services]
* [Observability|Observability]

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

## 📑 SECTION PARENT PAGE: Security & Compliance

```
h1. Security & Compliance

h2. Overview

Healthcare data is subject to HIPAA regulations and stringent security requirements. This platform is designed with compliance as a first-class concern, not an afterthought.

Every interaction includes:
* PHI detection and masking
* Parameterised queries (no SQL injection risk)
* Encrypted data in transit and at rest
* Audit logging with full traceability
* Role-based access controls

---

h2. 🗂️ In This Section

{page-tree:root=@self}

* [Security Overview|Security Overview]
* [HIPAA Alignment|HIPAA Alignment]

---

h2. 🔐 Key Controls

* *Authentication* — Azure AD JWT validation on all requests
* *Data Minimisation* — Only required data sent to LLMs
* *Encryption* — TLS in transit, AES-256 at rest
* *Audit Trail* — Every invocation logged with thread_id and intent
* *Retention Policies* — Configurable data lifecycle management

{toc}
```

---

## 📄 SINGLE PAGE: API Reference

```
h1. API Reference

h2. Endpoint

{toc:style=none}

| Property | Value |
|----------|-------|
| Path | POST /workflows/call_workflow |
| Auth | Bearer token (Azure AD JWT) |
| Content-Type | application/json |
| Idempotency | Not idempotent |

---

h2. Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| question | string | Yes | The caller's utterance for this turn |
| member_id | string | No | Pre-populated member ID from channel integration |
| thread_id | string | No | UUID of existing conversation thread (for multi-turn) |
| metadata | object | No | Arbitrary key-value pairs passed through to response |

---

h2. Response Body

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

---

h2. Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 400 | Bad Request | Missing required field 'question' |
| 401 | Unauthorized | Invalid or expired Azure AD JWT |
| 422 | Unprocessable | Request schema violation |
| 500 | Internal Error | Unhandled exception — check logs |
| 503 | Unavailable | LLM or database unavailable — retry with backoff |

---

h2. Example Flows

{warning}
Complete API documentation available in main documentation
{warning}
```

---

## 📄 SINGLE PAGE: Deployment

```
h1. Deployment

h2. Overview

The Healthcare AI Contact Center Platform is deployed to Azure Kubernetes Service (AKS) using containerized FastAPI pods with horizontal auto-scaling.

---

h2. Container Architecture

* Docker image includes FastAPI, LangGraph, and all dependencies
* Graph compilation happens lazily on first request
* Horizontal Pod Autoscaler scales pods based on CPU and request count

---

h2. Deployment Configuration

| Parameter | Value |
|-----------|-------|
| Minimum Replicas | 2 (high availability) |
| Maximum Replicas | 20 (configurable) |
| CPU Request | 500m per pod |
| CPU Limit | 2000m per pod |
| Memory Request | 1Gi per pod |
| Memory Limit | 4Gi per pod |

---

h2. Environment Variables

* AZURE_OPENAI_ENDPOINT
* OPENAI_API_KEY
* AZURE_SQL_CONNECTION_STRING
* AZURE_SEARCH_ENDPOINT
* AZURE_SEARCH_KEY
* MONGODB_URL
* LANGFUSE_ENABLED (optional)

---

h2. Deployment Steps

# Build Docker image
# Push to Azure Container Registry
# Create Kubernetes deployment manifest
# Apply manifest to AKS cluster
# Configure horizontal pod autoscaler
# Set up monitoring alerts

{warning}
Detailed deployment instructions in main documentation
{warning}
```

---

## 📄 SINGLE PAGE: Glossary

```
h1. Glossary

h2. Key Terms

{toc}

---

h3. AppointmentSchedulerAgent

Specialist agent for appointment lifecycle management using LangChain ReAct with eight tools. Handles view, book, reschedule, and cancel operations.

---

h3. CallWorkflowState

Single Pydantic TypedDict carrying all conversation state through the LangGraph graph nodes. Includes messages, identifiers, intent, and metadata.

---

h3. Checkpointer

LangGraph component that serialises and persists CallWorkflowState between graph invocations. Primary: MongoDBSaver. Fallback: MemorySaver.

---

h3. CompiledGraph

Result of `graph.compile(checkpointer)`. Frozen, executable graph instance cached as singleton for performance.

---

h3. Coordinator

First LangGraph node. Classifies intent, extracts identifiers, applies HITL safety gates, and routes to specialist agents.

---

h3. HITL (Human-in-the-Loop)

Graph pauses execution to request missing information from the caller. Not an agent takeover — a structured clarification request.

---

h3. LangGraph

Open-source Python framework for stateful, multi-actor LLM applications as directed graphs. Enables reproducible, observable agentic systems.

---

h3. MongoDBSaver

LangGraph-compatible MongoDB checkpointer. Stores `CallWorkflowState` in `langgraph_checkpoints` and `langgraph_checkpoint_writes` collections.

---

h3. PHI (Protected Health Information)

Any data that could identify a patient. HIPAA-regulated. Examples: member ID, date of birth, diagnosis codes.

---

h3. ReAct

Reasoning + Acting. LangChain agent pattern where LLM alternates between reasoning steps and tool invocations.

---

h3. StateGraph

LangGraph class defining nodes and edges. Compiled into a CompiledGraph for execution.

---

h3. thread_id

UUID identifying a single conversation session. Used as checkpoint key for multi-turn state restoration. Passed back to caller.

{toc}
```

---

## 🎯 How to Use These Templates

1. **Copy the template** for each page above
2. **Create the page** in Confluence (Create → Blank Page)
3. **Paste the content** into the editor
4. **Click Source** to see it as Confluence markup
5. **Replace placeholder text** with content from your markdown files
6. **Insert TOC macro** at the bottom of each page
7. **Publish** the page

---

## ✅ Formatting Checklist

- [ ] All `h1.` headings are page titles
- [ ] `h2.` and `h3.` used for section hierarchy
- [ ] Code blocks use `{code:language}` format
- [ ] Tables created in Confluence format
- [ ] Links use `[text|page-name]` format
- [ ] TOC macro inserted on all pages
- [ ] Page Tree macro on parent pages
- [ ] Bold text uses `*text*` format
- [ ] Info/warning boxes use `{info}` and `{warning}` macros

---

**Start with the parent page and work your way down the hierarchy!** 🚀
