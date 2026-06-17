# Design Inputs

The platform is built on the following design inputs:

## System Characteristics

1. **Multiple Intent Domains** — A single conversation may span claims status, benefits eligibility, and appointment scheduling
2. **Distributed Backend Data** — Member data exists across Azure SQL (claims), Azure AI Search (benefits), and EHR systems (appointments)
3. **HIPAA Regulation** — Every interaction involves Protected Health Information (PHI) that must be handled compliantly
4. **Multi-Turn Conversations** — Members often have follow-up questions requiring full conversation context

## Operational Realities

- **Intent routing is manual** — Agents must manually determine the right system to query
- **No unified data layer** — Each system has its own access patterns and authentication
- **PHI exposure risk** — LLM prompts and logs can inadvertently leak sensitive member data
- **Context loss** — Multi-turn conversations lose state between HTTP requests

## Platform Considerations

The solution must address:

- **Automated Intent Classification** — LLM-based classification with structured output
- **Intent-Specific Tooling** — Each agent has access only to tools relevant to its domain
- **PHI Masking and Security** — Parameterised queries and field-level data redaction
- **Durable State Management** — MongoDB checkpointing for conversation continuity

