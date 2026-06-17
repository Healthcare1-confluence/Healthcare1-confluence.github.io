# Workflow Step-by-Step Breakdown

## Step-by-Step Flow

1. **Inbound Call** — Voice captured, transcribed, member_id injected
2. **FastAPI + LangGraph** — Compilation, checkpoint restore
3. **Coordinator Node** — Intent classification, identifier extraction
4. **Specialist Agent Routing** — Route to appropriate agent or HITL
5. **Data Layer** — Query Azure SQL, AI Search
6. **LLM Synthesis** — Plain-English response assembly
7. **TTS Delivery** — Voice response to caller

