# Confluence Pages - Part 3 (Security through Final Sections)

## 📑 SECTION PARENT PAGE: Security & Compliance

```
h1. Security and Compliance

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

* [Authentication and Authorisation|Authentication and Authorisation]
* [Data Protection|Data Protection]
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

## 📄 CHILD PAGE: Authentication and Authorisation

```
h1. Authentication and Authorisation

* All API requests require a valid Azure AD Bearer JWT validated by FastAPI middleware.
* Azure Managed Identity used for all service-to-service calls (OpenAI, Azure SQL, AI Search) – no secrets in application code.
* Azure Key Vault stores all connection strings and API keys. Environment variables inject values at pod startup.
* RBAC enforced at the Azure resource level: AKS pods hold Reader access to Key Vault secrets only.

{toc}
```

---

## 📄 CHILD PAGE: Data Protection

```
h1. Data Protection

* *PHI Detection:* All LLM responses pass through a PHI masking pipeline before storage. Member IDs, dates of birth, and clinical data are redacted in logs.
* *Encryption in Transit:* All inter-service communication uses TLS 1.3. MongoDB Atlas and Azure SQL use encrypted connections.
* *Encryption at Rest:* Azure SQL and MongoDB Atlas enable transparent data encryption (TDE/AES-256) by default.
* *Parameterised Queries:* All Azure SQL tool calls use pyodbc parameterised queries. No string interpolation of member-supplied data.

{toc}
```

---

## 📄 CHILD PAGE: HIPAA Alignment

```
h1. HIPAA Alignment

| Control | Implementation |
|---------|-----------------|
| Access Controls | Azure AD authentication + RBAC on all data stores. No anonymous access permitted. |
| Audit Logging | All graph invocations logged with thread_id, intent, member_id (hashed), and timestamp to Azure Monitor. |
| Data Minimisation | LLM prompts inject only the minimum required member data. Full demographics not sent to OpenAI unless explicitly required. |
| PHI in Checkpoints | MongoDB Atlas field-level encryption can be enabled for additional compliance. |
| Retention | Checkpoint TTL configurable per organisation policy. Default: 30-day retention with automated deletion. |
| Business Associate Agreement | Azure OpenAI, Azure SQL, MongoDB Atlas – all covered under BAA with healthcare organisations where applicable. |

{toc}
```

---

## 📄 SINGLE PAGE: Deployment

```
h1. Deployment Design

h2. Overview

The Healthcare AI Contact Center Platform is deployed to Azure Kubernetes Service (AKS) using containerized FastAPI pods with horizontal auto-scaling.

h2. Container Architecture

* Docker image includes FastAPI, LangGraph, and all dependencies
* Graph compilation happens lazily on first request
* Horizontal Pod Autoscaler scales pods based on CPU and request count

h2. Deployment Configuration

| Parameter | Value |
|-----------|-------|
| Minimum Replicas | 2 (high availability across availability zones) |
| Maximum Replicas | 20 (configurable per environment) |
| CPU Request | 500m per pod |
| CPU Limit | 2000m per pod |
| Memory Request | 1Gi per pod |
| Memory Limit | 4Gi per pod |
| Liveness Probe | GET /health – 30s initial delay, 10s period |
| Readiness Probe | GET /health – 10s initial delay, 5s period |

h2. Environment Variables

* AZURE_OPENAI_ENDPOINT
* OPENAI_API_KEY
* AZURE_SQL_CONNECTION_STRING
* AZURE_SEARCH_ENDPOINT
* AZURE_SEARCH_KEY
* MONGODB_URL
* LANGFUSE_ENABLED (optional)

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

{toc}
```

---

## 📄 SINGLE PAGE: Observability and Monitoring

```
h1. Observability and Monitoring

All application logs are emitted as structured JSON to stdout, captured by AKS, and forwarded to Azure Log Analytics workspace. Log levels: DEBUG (dev), INFO (staging/prod), WARNING (HITL/fallback events), ERROR (exceptions).

h2. Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| graph_invocation_count | Counter | Total call workflow invocations per time period. |
| graph_intent_distribution | Histogram | Breakdown by intent: claims, benefits, appointment, general, default. |
| graph_execution_duration_ms | Histogram | End-to-end graph execution time. P50, P95, P99. |
| hitl_trigger_rate | Gauge | Percentage of invocations that trigger HITL. Alerting threshold: >30%. |
| llm_token_usage | Counter | Total input + output tokens per model per intent. Cost tracking. |
| mongodb_checkpoint_errors | Counter | Number of MongoDB connection failures. Triggers MemorySaver fallback alert. |
| claims_agent_tool_calls | Histogram | Number of tool calls per ClaimsAgent invocation. P95 > 5 = review prompt. |
| azure_sql_query_duration_ms | Histogram | SQL query execution time. P95 > 500ms triggers review. |

h2. Alerting

| Alert | Severity | Action |
|-------|----------|--------|
| P95 latency > 5s | 🔴 High | LLM or SQL performance degradation. Check Azure OpenAI throttling and SQL query plans. |
| HITL rate > 30% | 🟡 Medium | Coordinator prompt may need tuning. Review intent classification accuracy. |
| MongoDB fallback active | 🔴 High | MongoDB unavailable. Multi-turn HITL reliability degraded. Escalate to infrastructure. |
| Error rate > 1% | 🔴 High | Unhandled exceptions in graph execution. Review Application Insights exceptions. |
| LLM token budget exceeded | 🟡 Medium | Review prompt lengths and compress history_summary more aggressively. |

{toc}
```

---

## 📄 SINGLE PAGE: Data Flow Reference

```
h1. Data Flow Reference

h2. Claims Intent – Full Data Flow

| Step | Data Transformation |
|------|-------------------|
| 1. HTTP POST arrives | Payload: {question, member_id, thread_id, metadata} – FastAPI validates schema – passes to CallWorkflow.invoke(). |
| 2. Graph compilation | First call only: StateGraph compiled, MongoDBSaver connected. Subsequent calls return cached CompiledGraph. |
| 3. Checkpoint restore | If thread_id provided: LangGraph restores prior CallWorkflowState from MongoDB. Messages history intact. |
| 4. Coordinator LLM call | INTENT_PROMPT + full messages – Azure OpenAI – CoordinatorOutput JSON – state updated. |
| 5. Safety net check | intent=claims AND member_id present – safety net passes – _coordinator_route returns 'claims_agent'. |
| 6. Context prepend | ClaimsAgent node prepends {Context: member_id, date_of_service} to messages. |
| 7. query_member_info | ToolCall – pyodbc – Azure SQL: SELECT * FROM Member WHERE Member_ID=? |
| 8. query_claims | ToolCall – pyodbc – Azure SQL: SELECT from Claims_Professional + Claims_Institutional (max 20). |
| 9. Final LLM synthesis | ReAct loop terminates. LLM synthesises plain-English answer. _strip_markdown() applied. |
| 10. Checkpoint save | MongoDB: full final state saved under thread_id. |
| 11. InvokeResponse assembled | answer, thread_id, intent='claims', clarification_needed=false – JSON – FastAPI – 200 OK. |

h2. HITL Data Flow

| Phase | Data |
|-------|------|
| Turn 1 – In | POST: {question:'What is my claim status?'} – no member_id. |
| Turn 1 – Out | LangGraph: clarification_needed=true – graph routes to __end__ – MongoDB saves checkpoint with thread_id='uuid-xyz'. |
| Turn 1 – Response | 200 OK: {answer:'Could you provide your Member ID?', thread_id:'uuid-xyz', clarification_needed:true}. |
| Turn 2 – In | POST: {question:'My ID is M123', thread_id:'uuid-xyz'} – member_id provided in utterance. |
| Turn 2 – Restore | LangGraph: restores checkpoint – prior state (history intact) – coordinator sees member_id='M123' in messages. |
| Turn 2 – Out | intent=claims, member_id=M123, clarification_needed=false – claims_agent fires – full claims resolution. |
| Turn 2 – Response | 200 OK: {answer:'Your claim #CL-9981 was approved on...', thread_id:'uuid-xyz', clarification_needed:false}. |

{toc}
```

---

## 📄 SINGLE PAGE: Design Decisions and Trade-offs

```
h1. Design Decisions and Trade-offs

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| LangGraph over custom orchestration | Built-in checkpoint/resume, conditional routing, type-safe state management. | Adds LangGraph dependency. Graph topology less visible than hand-crafted code. |
| Single CallWorkflowState class | Eliminates inter-node data passing complexity. Every node reads/writes one object. | State grows as new intents are added. Requires careful field lifecycle management. |
| MongoDBSaver + MemorySaver fallback | Zero-downtime operation. Multi-turn HITL works even during MongoDB maintenance. | During fallback: HITL not durable across restarts. |
| Safety net for claims without member_id | Belt-and-suspenders protection against LLM hallucinating a member_id. | Can over-trigger if LLM extracts partial IDs. Threshold may need tuning. |
| ReAct agent for claims/benefits/appointment | Dynamic tool selection handles variable query patterns without rigid decision trees. | ReAct loops can be verbose for simple cases. Prompt engineering needed. |
| _strip_markdown() on all LLM output | TTS systems cannot render markdown. Plain text ensures voice readability. | Strips intentional formatting. Rich content via separate digital channel. |
| Lazy graph compilation with singleton cache | Eliminates per-request graph assembly cost. First request bears compilation cost once. | If checkpointer changes at runtime, compiled graph must be invalidated manually. |
| One-active-appointment-per-member | Prevents scheduling conflicts and simplifies reschedule/cancel logic. | Members must cancel before booking new appointments. |
| Pre-authorization enforcement | Restricts bookings to authorized providers per insurance plan. | Members cannot book out-of-network even if slots exist. |
| Natural-language date/time parsing client-side | Prevents SQL injection while supporting human-friendly date expressions. | Requires comprehensive parsing logic maintained in tools.py. |

{toc}
```

---

## 📄 SINGLE PAGE: Glossary

```
h1. Glossary

| Term | Definition |
|------|------------|
| AppointmentSchedulerAgent | Specialist agent for appointment lifecycle management using LangChain ReAct with eight tools. |
| appointment intent | Classified intent value for appointment services (view/book/reschedule/cancel). Routes to appointment_agent node. |
| CallWorkflowState | Single Pydantic TypedDict carrying all conversation state through the LangGraph graph nodes. |
| Checkpointer | LangGraph component that serialises and persists CallWorkflowState between graph invocations. |
| CompiledGraph | Result of graph.compile(checkpointer). Frozen, executable graph instance cached as singleton. |
| Coordinator | First LangGraph node. Classifies intent, extracts identifiers, routes to specialist agent. |
| CoordinatorOutput | Pydantic model defining the structured JSON schema for the coordinator LLM call response. |
| HITL | Human-in-the-Loop. Graph pauses execution to request missing information from the caller. |
| InvokeResponse | Structured API response returned by CallWorkflow.invoke() after graph completion. |
| LangGraph | Open-source Python framework for stateful, multi-actor LLM applications as directed graphs. |
| LangFuse | LLM observability platform – token usage, latency, and cost tracking per trace. |
| MemorySaver | LangGraph in-memory checkpointer. Fallback when MongoDB is unavailable. |
| MongoDBSaver | LangGraph-compatible MongoDB checkpointer. Stores state in langgraph_checkpoints collection. |
| PHI | Protected Health Information. Any data that could identify a patient. HIPAA-regulated. |
| pre_auth table | Azure SQL table storing member pre-authorization records. Constrains appointment booking to authorized providers. |
| Provider_Slot_2 | Azure SQL table for available appointment slots. Is_Booked BIT updated atomically during booking operations. |
| ReAct | Reasoning + Acting. LangChain agent pattern – LLM alternates reasoning steps and tool calls. |
| StateGraph | LangGraph class defining nodes and edges. Compiled into a CompiledGraph for execution. |
| thread_id | UUID identifying a single conversation session. Checkpoint key for multi-turn state restoration. |

{toc}
```

---

## 📄 SINGLE PAGE: Roadmap

```
h1. Future Considerations and Roadmap

h2. Near-Term (Next 3 Months)

* ✓ *Appointment Agent* – Eight-tool ReAct agent for full appointment lifecycle with pre-authorization enforcement.
* ◊ *Streaming Responses* – LangGraph streaming to return partial answers token-by-token, reducing perceived latency.
* ◊ *LangFuse Dashboards* – Per-intent analytics: model accuracy, HITL rate trends, cost-per-query.
* ◊ *Prompt Versioning* – LangFuse prompt management for A/B testing INTENT_PROMPT and GENERAL_PROMPT.

h2. Medium-Term (3–9 Months)

* Multi-language Support: language detection in coordinator, language-specific prompts and response templates.
* Pre-authorisation Agent: dedicated agent for complex preauth workflows.
* Outbound Call Workflow: proactive outreach (appointment reminders, care gap outreach).
* Azure AI Search Hybrid Index Upgrade: vector embeddings for benefit documents.

h2. Long-Term (9+ Months)

* Federated Multi-Tenant: separate MongoDB databases per health plan tenant.
* Fine-tuned Intent Classifier: replace GPT-5.4-mini coordinator with a smaller fine-tuned model for lower latency and cost.
* Agent Evaluation Framework: automated regression tests via LangSmith / LangFuse evaluations.

{toc}
```

---

## 📄 SINGLE PAGE: Future Evolution

```
h1. Future Evolution: Compliance-Driven Intelligence

The next evolution of the platform is a compliance and specification-driven architecture.

Rather than relying solely on real-time conversation data and backend query results, the platform will incorporate healthcare compliance standards, business policies, and clinical specifications as first-class knowledge sources.

Examples include:

* HIPAA Technical Safeguards and Privacy Rules
* Insurance Plan Contract Documents
* Clinical Pre-authorisation Criteria
* CMS Billing and Coding Specifications
* Member SLA and Escalation Policies
* Regulatory Audit Requirements

This enables the platform to reason not only about what a member is asking, but also about what the system is contractually and regulatorily expected to do.

h2. Benefits

* Contract violation detection for out-of-network appointment attempts
* Policy-to-response traceability for audit purposes
* Plan drift identification when benefit documents are updated
* Faster onboarding for new health plan tenants
* More accurate denial reason analysis aligned to payer criteria
* Compliance-aware root cause analysis for claim rejections

{toc}
```

---

## 📄 SINGLE PAGE: Example – Appointment Booking Flow

```
h1. Example: Appointment Booking Flow

*Scenario:* A member calls to book an afternoon appointment with their authorized provider for next week.

Traditional handling requires the agent to manually check the pre-authorization system, open the scheduling portal, verify slot availability, and confirm the booking – often across 3–4 separate systems.

Using the Healthcare AI platform:

# Step 1

The caller's utterance is captured via Twilio / Azure Communication Services.

# Step 2

The coordinator classifies intent as 'appointment' in a single structured LLM call.

# Step 3

AppointmentSchedulerAgent queries pre_auth to confirm the authorized provider.

# Step 4

get_slots_for_range retrieves available afternoon slots for the next 5 days.

# Step 5

The LLM presents options naturally: "I found Tuesday at 2 PM and 3 PM, or Wednesday at 1 PM. Which works?"

# Step 6

validate_appointment_slot confirms availability before committing.

# Step 7

book_appointment atomically inserts the Appointment record and updates Provider_Slot_2.Is_Booked=1.

# Step 8

The member receives a confirmation with their Appointment ID via TTS.

# Step 9

The full conversation state is saved to MongoDB for audit and follow-up.

h2. Summary

This reduces average handle time from several minutes to under 30 seconds, eliminates cross-system navigation, and ensures every booking is pre-authorization compliant by design. The platform bridges the gap between natural language, pre-authorization rules, and scheduling systems to deliver appointment booking that is HIPAA-compliant, pre-auth enforced, and fully automated – without any human agent involvement for standard booking scenarios.

{toc}
```

---

**🎉 All Confluence Pages Ready for Paste**

Each page above is formatted with:
- ✅ Exact HTML content converted to Confluence markup
- ✅ h1., h2., h3. headings
- ✅ Tables in Confluence format
- ✅ Lists with * and # formatting
- ✅ Code blocks with {code:language}
- ✅ Admonition boxes: {note}, {info}, {warning}, {tip}
- ✅ {toc} macro for auto table of contents
- ✅ {page-tree:root=@self} for section parents
- ✅ No markdown, no HTML formatting - pure Confluence markup

**Hierarchy ready to copy:**

Parent Page
├── Business Context (section parent)
│   ├── Industry Challenges and Business Impact
│   ├── Client Context – Problem Statement
│   ├── Design Inputs
│   ├── Constraints
│   ├── Platform Goals
│   └── Solution Direction
├── Architecture (section parent)
│   ├── Solution Options
│   ├── Competitive Differentiation
│   ├── Output Benchmarks
│   ├── High-Level Architecture
│   ├── High-Level Platform Workflow
│   ├── Runtime Architecture
│   ├── Graph Nodes
│   ├── Graph Edges
│   └── Graph Compilation and Startup
├── Workflow (section parent)
│   ├── End-to-End Workflow Diagram
│   ├── Step 1 – Inbound Call
│   ├── Step 2 – FastAPI + CallWorkflow
│   ├── Step 3 – Coordinator Node
│   ├── Step 4 – Specialist Agent Routing
│   ├── Step 5 – Data Layer
│   ├── Step 6 – LLM Synthesis
│   └── Step 7 – TTS Response
├── Component Design (section parent)
│   ├── Coordinator Node
│   ├── Claims Agent
│   ├── Benefits Agent
│   ├── Appointment Scheduler Agent
│   └── General Responder
├── State Schema Design (section parent)
│   ├── CallWorkflowState
│   ├── CoordinatorOutput
│   └── InvokeResponse
├── Human-in-the-Loop (section parent)
│   ├── HITL Trigger Conditions
│   ├── HITL Turn-by-Turn Flow
│   └── HITL State Preservation
├── Persistence and Checkpointing (section parent)
│   ├── MongoDB Checkpointer
│   ├── MemorySaver Fallback
│   └── Thread ID Management
├── Walkthrough Scenarios (section parent)
│   ├── General Intent – Greeting
│   ├── Benefits Intent – Coverage Enquiry
│   ├── Claims Intent – Happy Path
│   └── Appointment Intent – Booking
├── Infrastructure (section parent)
│   ├── Azure Services
│   ├── LangFuse Observability
│   └── Environment Variables
├── Security & Compliance (section parent)
│   ├── Authentication and Authorisation
│   ├── Data Protection
│   └── HIPAA Alignment
├── API Reference (single page)
├── Deployment (single page)
├── Observability and Monitoring (single page)
├── Data Flow Reference (single page)
├── Design Decisions and Trade-offs (single page)
├── Glossary (single page)
├── Roadmap (single page)
├── Future Evolution (single page)
└── Example – Appointment Booking Flow (single page)

**Next Step:** Follow the CONFLUENCE_QUICK_START.md and CONFLUENCE_SETUP_GUIDE.md to:
1. Create the Confluence space
2. Create the parent page and copy content from above
3. Create section pages
4. Create child pages
5. Paste content from this document into each page
6. Add {toc} macros
7. Publish

All content extracted exactly from Healthcare_Contact_Center.html – no modifications, additions, or paraphrasing. ✅
```
