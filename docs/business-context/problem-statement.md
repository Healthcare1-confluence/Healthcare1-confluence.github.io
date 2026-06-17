# Problem Statement

## Design Inputs

The following realities of healthcare contact centre operations define the design inputs:

| System Characteristics | Operational Realities | Platform Considerations |
|------------------------|----------------------|------------------------|
| Multiple intent domains across a single conversation | Intent routing is manual and agent-driven | Automated LLM-based intent classification required |
| Backend data spread across SQL, search, and EHR | No unified data access layer | Agent-specific tool sets per intent domain |
| HIPAA-regulated member data in every interaction | PHI exposure risk in logs and LLM prompts | PHI masking and parameterised queries mandatory |
| Multi-turn conversations common for complex queries | Context is lost between calls | Durable MongoDB checkpointing required |

## Constraints

The system must operate within the following constraints:

- Handle concurrent calls across claims, benefits, appointment, and general intents
- Never invoke a specialist agent without required member identifiers being present or requested
- Not rely on manual intervention during live call processing
- Maintain HIPAA compliance in all LLM prompts, logs, and stored checkpoints
- Produce responses readable by TTS engines — no markdown, no formatting symbols
- Complete responses within **3 seconds P95** for general intent; under **5 seconds** for specialist agents

