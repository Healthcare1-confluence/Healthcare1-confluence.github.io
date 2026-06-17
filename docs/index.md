# Healthcare AI Contact Center Platform

**Solution & Technical Design Document**  
*Agentic Call Workflow Engine — LangGraph + Azure*

**Version 1.0 | 2026**

## Overview

The Healthcare AI Contact Center Platform is a solution designed to automate healthcare contact centre interactions across claims status, benefits enquiries, appointment scheduling, and general member assistance using an agentic multi-agent architecture built on LangGraph and Azure.

## Key Features

- **Intelligent Intent Classification**: Automatically classifies caller intent using Azure OpenAI
- **Multi-Agent Routing**: Specialized agents for claims, benefits, appointments, and general inquiries
- **HIPAA-Compliant**: Built-in PHI masking and secure data handling
- **Durable Multi-Turn State**: MongoDB checkpointing enables seamless conversation continuity
- **Pre-Authorization Enforcement**: Ensures appointment compliance with insurance rules
- **Human-in-the-Loop Safety**: HITL gates prevent mis-service of members

## Quick Links

- [Business Context](business-context/overview.md) — Industry challenges and design inputs
- [Architecture Overview](architecture/overview.md) — System design and components
- [Workflow Design](workflow/e2e-workflow.md) — End-to-end call processing
- [API Reference](api-reference.md) — Integration details
- [Deployment Guide](deployment.md) — Infrastructure setup

## Platform Goals

✓ Automate 60–70% of Tier-1 calls with zero human involvement  
✓ Maintain 95%+ intent classification accuracy  
✓ Enforce HIPAA compliance across every interaction  
✓ Complete responses within 3s (general intent) / 5s (specialist agents)  
✓ Support full appointment lifecycle with pre-auth enforcement  

## Architecture at a Glance

The platform follows a layered architecture:

```
Channel Layer (Twilio/ACS)
        ↓
FastAPI + LangGraph
        ↓
Coordinator Node (Intent Classification)
        ↓
Specialist Agents (Claims/Benefits/Appointment/General)
        ↓
Data Layer (Azure SQL, AI Search)
        ↓
Durable State (MongoDB)
        ↓
TTS Response
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Orchestration | LangGraph, LangChain |
| LLM | Azure OpenAI (GPT-5.4-mini) |
| API Framework | FastAPI |
| State Persistence | MongoDB Atlas |
| Databases | Azure SQL Server |
| Search | Azure AI Search |
| Deployment | Azure Kubernetes Service (AKS) |
| Observability | Azure Monitor, LangFuse |

## What's Inside

This documentation covers:

- **Business Context** — Industry challenges, constraints, and design inputs
- **Architecture** — Component design, graph topology, runtime architecture
- **Workflow** — Seven-step end-to-end call processing pipeline
- **Component Design** — Deep dive into coordinator, agents, and sub-agents
- **State Management** — Schema design and checkpoint architecture
- **HITL Design** — Safety nets for missing data scenarios
- **API Reference** — Request/response formats and error handling
- **Infrastructure** — Azure services, environment setup, observability
- **Security & Compliance** — HIPAA alignment, data protection, audit logging
- **Deployment** — Container architecture, AKS configuration
- **Roadmap** — Near-term, medium-term, and long-term enhancements

---

**Ready to dive deeper?** Start with [Business Context](business-context/overview.md) to understand the problem domain, or jump to [Architecture Overview](architecture/overview.md) for the technical design.

