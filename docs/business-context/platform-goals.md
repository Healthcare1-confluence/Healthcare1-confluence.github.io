# Platform Goals

## Strategic Objectives

The platform provides a structured and intelligent approach to healthcare contact automation with the following objectives:

### Primary Goals

✓ **Automate 60–70%** of Tier-1 calls with zero human agent involvement

✓ **Classify caller intent accurately** on every turn using Azure OpenAI

✓ **Enforce Human-in-the-Loop gates** to ensure no member is mis-served due to missing data

✓ **Preserve multi-turn conversation state** durably across HTTP requests using MongoDB

✓ **Support appointment lifecycle management** with pre-authorization enforcement

✓ **Deliver HIPAA-aligned PHI handling** across every system boundary

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Response Latency (General Intent) | P95 ≤ 3 seconds | Target |
| Response Latency (Specialist Agents) | P95 ≤ 5 seconds | Target |
| Tier-1 Call Automation Rate | 60–70% | Target |
| Intent Classification Accuracy | ≥ 95% | Target |
| Appointment Booking Handle Time | ≤ 30 seconds | Target |
| HITL Escalation Rate | ≤ 15% | Target |

## Solution Direction

To achieve these goals, the platform is designed to:

1. **Classify** the caller's intent on every turn using a structured LLM call
2. **Enrich** state with member identifiers extracted from the conversation
3. **Route** to specialist agents that combine tool use and LLM reasoning
4. **Deliver** plain-English answers via TTS

This approach transitions healthcare contact handling from a manual, agent-driven activity to a system-assisted, intelligence-driven process.

