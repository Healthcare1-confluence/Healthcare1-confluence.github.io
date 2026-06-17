# Architecture Overview

## Architecture Pattern: Agentic Multi-Agent System

The platform follows an **agentic multi-agent architecture** pattern, combining structured intent classification with specialist agent tool use.

## Why This Approach?

### Alternative Approaches Evaluated

**Rule-Based IVR Systems**
- ✗ Rely on fixed decision trees and touch-tone menus
- ✗ Unsuitable for natural language queries and multi-intent conversations

**Single LLM Chatbots**
- ✗ Flexible but lack structured tool use
- ✗ Do not enforce HITL safety nets
- ✗ Cannot maintain durable multi-turn state

**Monitoring and Observability Platforms**
- ✗ Provide call analytics but do not reason over backend data
- ✗ Cannot classify healthcare-specific intents

**Agentic Multi-Agent Architecture (Recommended)** ✓
- ✓ Combines structured intent classification with specialist agent tool use
- ✓ Bridges the gap between natural language and backend data systems
- ✓ Best fit for multi-intent, multi-turn, HIPAA-compliant healthcare automation

## Key Components

### Orchestration Layer (Tier 0)
- **Coordinator Node** — Intent classification and routing
- **HITL Guard** — Safety validation for missing data

### Agent Layer (Tier 1)
- **Claims Agent** — Claim status and pre-authorization queries
- **Benefits Agent** — Plan coverage and benefit lookup
- **Appointment Agent** — Appointment lifecycle management
- **General Responder** — Greeting and miscellaneous queries

### Data Layer
- **Azure SQL** — Member, claims, appointments, pre-authorization data
- **Azure AI Search** — Benefit document corpus
- **MongoDB Atlas** — Conversation state and checkpoints

## Architecture Benefits

| Benefit | Impact |
|---------|--------|
| **Structured Routing** | Reduces error surface by limiting agent access to relevant tools |
| **Durable State** | Enables HITL gates and multi-turn conversations |
| **Healthcare-Specific** | Built-in HIPAA compliance and pre-auth enforcement |
| **Transactional Tool Use** | Can both read and write to backend systems (bookings, cancellations) |

