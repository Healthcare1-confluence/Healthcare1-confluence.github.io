# Human-in-the-Loop (HITL) Design

## Overview

HITL is a structured clarification pattern where the AI workflow pauses to request additional information from the caller.

It is NOT a human agent takeover — it is a natural clarification request that allows the graph to resume with complete data on the next turn.

## Trigger Conditions

1. **Missing member_id for claims intent** — Coordinator classifies claims but member_id absent
2. **LLM-detected ambiguity** — Coordinator sets clarification_needed=True with specific question

